# サイト構成

azihsoyn.dev の構成。生成ツールが何であっても、この文書の URL とページを守る。
ツールを入れ替える時は、ビルド結果の URL 一覧がこの文書と一致することを確かめる。

## 方針

- 技術記事のみ。技術以外の話題は当面書かない
- 日本語のみ（`<html lang="ja">`）
- 記事の種類は 1 つ。シリーズは当面作らない

## URL

| URL | ページ |
| --- | --- |
| `/` | トップ。新着記事の一覧と短い自己紹介 |
| `/posts/<slug>/` | 記事 |
| `/posts/` | 記事一覧（年ごとのアーカイブ） |
| `/tags/` | タグの一覧 |
| `/tags/<tag>/` | タグごとの記事一覧 |
| `/about/` | About |
| `/search/` | 全文検索 |
| `/feed.xml` | Atom フィード |
| `/sitemap.xml` | サイトマップ |
| `/robots.txt` | robots.txt（サイトマップの場所を示す） |
| `/404.html` | 404 ページ |

- `slug` と `tag` は英小文字・数字・ハイフンのみ（例: `zola-to-moonbit`）
- 末尾のスラッシュを付けた形を正とする
- 一度公開した URL は変えない。変える時はリダイレクトを置く
- このほか、CSS・JS・画像と、検索の索引（`/pagefind/` 以下）を配信する。これらは URL の約束の対象外
- 約束は `scripts/check.py` が確かめる。今の URL の一覧は `tests/urls.txt`

## 記事

記事は `content/posts/<slug>.md` に置く。画像を伴う記事は `content/posts/<slug>/index.md` とし、画像を同じディレクトリに置く。

先頭のメタ情報は `+++` で囲んだ TOML で書く:

| 項目 | 必須 | 内容 |
| --- | --- | --- |
| `title` | 必須 | 題名 |
| `date` | 必須 | 公開日（`YYYY-MM-DD`） |
| `tags` | 必須 | タグの配列。1 つ以上。Zola の決まりで `[taxonomies]` の下に書く |
| `description` | 必須 | 一覧と OGP に使う 1〜2 文 |
| `updated` | 任意 | 最終更新日 |
| `draft` | 任意 | `true` なら本番に出さない |

```toml
+++
title = "題名"
date = 2026-11-05
description = "一覧と OGP に使う説明"

[taxonomies]
tags = ["rust"]
+++
```

ツール独自の記法（ショートコードやコンポーネントなど）は本文で使わない。本文は CommonMark と GFM の範囲で書く。
見出しのアンカーは見出しの文字のまま（例: `#今後`）にする。

## About

- GitHub: [azihsoyn](https://github.com/azihsoyn)
- SNS へのリンク（`zola.toml` の `extra.social` に書く。アカウントは追って記入）

## 機能

| 機能 | 内容 |
| --- | --- |
| ダークモード | OS の設定に従い、手動の切り替えも記憶する |
| 見た目 | テーマは方眼、印の色は藍、等幅フォントは JetBrains Mono。ほかの候補（墨、白黒・赤紫・青・朱、OS の等幅）も CSS に残しており、`zola.toml` の `extra.picker = true` で読む人が選べるようになる。一覧と既定は `extra.styles` / `accents` / `fonts`（どれも先頭が既定） |
| フォント | 日本語は OS のフォント。等幅の英字だけを Web フォント（JetBrains Mono、英字のみ 40KB）として自分のサイトから配信し、先読みする。届くまでは字幅と行の高さを合わせた OS の等幅で出す。ライセンスは `static/fonts/` の各ディレクトリ（OFL） |
| 日本語の組版 | 見出しを文節で改行し（`word-break: auto-phrase`）、和欧の間を自動で空ける（`text-autospace`）。対応していないブラウザでは何もしない |
| ページの移動 | カーソルを乗せたリンクを先読みし（Speculation Rules）、ページの切り替えをつなぐ（View Transitions） |
| コードのハイライト | ビルド時に処理する |
| OGP | 記事ごとに題名・説明を出す。画像は後で用意する |
| 全文検索 | Pagefind の拡張版（`pagefind_extended`）で日本語を分割して索引し、ブラウザ側で検索する |
| 目次 | 記事ページに見出しの目次を出す |
| 読了時間 | 文字数から計算する（Zola の日本語向けの計算に従う） |
| アクセス解析 | Cloudflare Web Analytics |

## 配信

- Cloudflare Workers の静的アセット配信（Worker のスクリプトは置かない）
- HTML はキャッシュの既定値（`max-age=0, must-revalidate`）のまま
- ハッシュ付きのファイル名にした CSS・JS・フォントは `_headers` で長期キャッシュにする

## 生成ツールを入れ替える時

- 記事（`content/`）と画像はそのまま使う
- テンプレート（`templates/`）は書き直す。Zola 0.23 のテンプレートは Tera v2 で、Jinja2 とは互換でない部分がある（コンポーネントなど）。持ち運びやすさのため、コンポーネントは最小限にしている
- `scripts/check.py` が通り、`tests/urls.txt` と URL が一致することを確かめる
