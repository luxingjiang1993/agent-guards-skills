#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=(
  "$HOME/.agents/skills"
  "$HOME/.claude/skills"
  "$HOME/.cursor/skills"
)
for d in "${DESTS[@]}"; do
  mkdir -p "$d"
  for s in setup-agent-guards enrich-tickets provenance-check before-implement; do
    rm -rf "$d/$s"
    cp -R "$ROOT/skills/$s" "$d/$s"
  done
  echo "Installed into $d"
done
mkdir -p "$HOME/.agents/agent-guards-lib"
cp -f "$ROOT/lib/check_provenance.py" "$HOME/.agents/agent-guards-lib/"
echo "Provenance checker: $HOME/.agents/agent-guards-lib/check_provenance.py"
echo "Also install Matt: npx skills add mattpocock/skills"
