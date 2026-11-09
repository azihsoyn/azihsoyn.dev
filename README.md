# azihsoyn.dev

azihsoyn の技術ブログ。[Zola](https://www.getzola.org/) で HTML を生成し、Cloudflare Workers の静的アセット配信で公開する。

構成（URL・ページ・記事の書き方）は [docs/site-structure.md](docs/site-structure.md) にまとめてある。

## 準備

ツールのバージョンは `mise.toml` で固定している。

```sh
mise install
```

## 記事を書く

`content/posts/<slug>.md`（画像を伴う時は `content/posts/<slug>/index.md`）を作る。
書き方は [docs/site-structure.md](docs/site-structure.md#記事) を参照。

```sh
zola serve --drafts     # 下書きも含めて手元で確認する（検索は動かない）
```

## ビルドと確認

```sh
scripts/build.sh                 # public/ に出力し、検索の索引を作る
python3 scripts/check.py         # 構成の約束を守れているか確かめる
python3 scripts/check.py --update  # 記事を足した時など、URL の一覧を記録し直す
```

検索も含めて手元で確かめる時:

```sh
scripts/build.sh --drafts --base-url http://localhost:1414
pagefind_extended --site public --serve
```

## 表示の設定

既定は方眼・藍・JetBrains Mono。テーマ・印の色・等幅フォントは、それぞれ `static/style.css` の `[data-style]`・`[data-accent]`・`[data-font]` に書き、`zola.toml` の `extra.styles`・`accents`・`fonts` に並べる。どれも先頭のものが既定になる。
`extra.picker = true` にすると、ヘッダーに設定のボタンが出て、読む人が選べるようになる。

## 公開

`main` に push すると GitHub Actions がビルドとチェックを行い、`wrangler deploy` で公開する。
公開を有効にするには、リポジトリに次を設定する。

- 変数 `DEPLOY_ENABLED` = `true`
- シークレット `CLOUDFLARE_API_TOKEN`、`CLOUDFLARE_ACCOUNT_ID`

独自ドメイン azihsoyn.dev は `wrangler.jsonc` の `routes` で設定している（ドメインは Cloudflare Registrar で取得し、同じアカウントにある）。
