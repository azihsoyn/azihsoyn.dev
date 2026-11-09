#!/usr/bin/env python3
"""docs/site-structure.md の約束をビルド結果で確かめる。

1. 記事の先頭のメタ情報に必須項目が揃っているか
2. 出力された URL が決めた形に収まっているか
3. URL が tests/urls.txt から増減していないか（--update で書き換える）

先に scripts/build.sh（下書きなし）を実行しておくこと。
"""
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "content" / "posts"
PUBLIC = ROOT / "public"
SNAPSHOT = ROOT / "tests" / "urls.txt"

NAME = r"[a-z0-9]+(?:-[a-z0-9]+)*"
ALLOWED_URLS = [
    r"/",
    r"/posts/",
    rf"/posts/{NAME}/",
    r"/tags/",
    rf"/tags/{NAME}/",
    r"/about/",
    r"/search/",
    r"/feed\.xml",
    r"/sitemap\.xml",
    r"/robots\.txt",
    r"/404\.html",
]
# 記事に添えた画像などは URL の約束の対象外
ASSET_SUFFIXES = {".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".ico"}
REQUIRED = ("title", "date", "description")


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\+\+\+\n(.*?)\n\+\+\+\n", text, re.S)
    if not m:
        raise ValueError("先頭に +++ で囲んだ TOML のメタ情報がない")
    return tomllib.loads(m.group(1))


def post_files() -> list[Path]:
    files = [p for p in POSTS.glob("*.md") if p.name != "_index.md"]
    files += list(POSTS.glob("*/index.md"))
    return sorted(files)


def check_posts() -> list[str]:
    errors = []
    for path in post_files():
        rel = path.relative_to(ROOT)
        slug = path.parent.name if path.name == "index.md" else path.stem
        if not re.fullmatch(NAME, slug):
            errors.append(f"{rel}: slug '{slug}' は英小文字・数字・ハイフンのみ")
        try:
            fm = front_matter(path)
        except (ValueError, tomllib.TOMLDecodeError) as e:
            errors.append(f"{rel}: {e}")
            continue
        for key in REQUIRED:
            if not fm.get(key):
                errors.append(f"{rel}: '{key}' がない")
        tags = fm.get("taxonomies", {}).get("tags", [])
        if not tags:
            errors.append(f"{rel}: [taxonomies] の tags が 1 つもない")
        for tag in tags:
            if not re.fullmatch(NAME, tag):
                errors.append(f"{rel}: タグ '{tag}' は英小文字・数字・ハイフンのみ")
    return errors


def built_urls() -> list[str]:
    urls = []
    for path in PUBLIC.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(PUBLIC).as_posix()
        if rel.startswith(("pagefind/", "fonts/", "_")) or path.suffix in ASSET_SUFFIXES:
            continue
        if path.name == "index.html":
            parent = rel[: -len("index.html")]
            urls.append("/" + parent)
        else:
            urls.append("/" + rel)
    return sorted(urls)


def main() -> int:
    update = "--update" in sys.argv[1:]
    if not PUBLIC.is_dir():
        print("public/ がない。先に scripts/build.sh を実行する", file=sys.stderr)
        return 1

    errors = check_posts()
    urls = built_urls()
    patterns = [re.compile(p) for p in ALLOWED_URLS]
    for url in urls:
        if not any(p.fullmatch(url) for p in patterns):
            errors.append(f"決めた形にない URL: {url}")

    if update:
        SNAPSHOT.parent.mkdir(exist_ok=True)
        SNAPSHOT.write_text("".join(u + "\n" for u in urls), encoding="utf-8")
        print(f"{SNAPSHOT.relative_to(ROOT)} を更新した（{len(urls)} 件）")
    else:
        expected = SNAPSHOT.read_text(encoding="utf-8").split() if SNAPSHOT.exists() else []
        removed = sorted(set(expected) - set(urls))
        added = sorted(set(urls) - set(expected))
        for url in removed:
            errors.append(f"消えた URL: {url}（意図した変更ならリダイレクトを置く）")
        for url in added:
            errors.append(f"増えた URL: {url}（意図した変更なら --update で記録する）")

    for e in errors:
        print(f"NG {e}", file=sys.stderr)
    if errors:
        return 1
    print(f"OK 記事ファイル {len(post_files())} 件（下書き含む） / URL {len(urls)} 件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
