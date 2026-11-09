#!/usr/bin/env bash
# サイトをビルドし、全文検索の索引を作る。引数はそのまま zola build に渡す（例: --drafts）
set -euo pipefail
cd "$(dirname "$0")/.."

zola build "$@"
pagefind_extended --site public
