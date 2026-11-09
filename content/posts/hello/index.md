+++
title = "ブログを始めました"
date = 2026-11-05
description = "azihsoyn.dev を始めました。このブログの構成について書きます。"
draft = true

[taxonomies]
tags = ["blog"]
+++

この記事は雛形です。公開する前に書き直し、`draft = true` を消してください。

## 構成

Zola で HTML を生成し、Cloudflare Workers の静的アセット配信で公開しています。

```rust
fn main() {
    println!("hello, azihsoyn.dev");
}
```

### 配信

静的なファイルを置くだけなので、[Cloudflare Workers の静的アセット配信](https://developers.cloudflare.com/workers/static-assets/)を使っています。

| 項目 | 内容 |
| --- | --- |
| 生成 | Zola |
| 検索 | Pagefind |

> 引用はこのように表示されます。

## 今後

生成ツールは、いずれ自作のものに置き換える予定です。
