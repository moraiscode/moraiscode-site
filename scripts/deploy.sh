#!/usr/bin/env bash
# CD — sincroniza os arquivos do site (whitelist) do repositório para o docroot da Hostinger.
# Uso: bash scripts/deploy.sh   (rodar de dentro do clone ~/deploys/moraiscode-site)
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DEST="${DEPLOY_DEST:-$HOME/domains/moraiscode.com/public_html}"
FILTER='^(index\.html$|\.htaccess$|robots\.txt$|llms\.txt$|curriculo\.(md|txt|pdf)$|favicon[^/]*$|apple-touch-icon\.png$|curriculo/|css/|assets/)'

cd "$REPO"

if [ ! -w "$DEST" ]; then
  echo "docroot inacessível: $DEST" >&2
  exit 1
fi

git ls-files -z | tr '\0' '\n' | grep -E "$FILTER" | tr '\n' '\0' \
  | xargs -0 -r cp --parents -t "$DEST"

echo "deploy ok — $(git log --oneline -1)"
