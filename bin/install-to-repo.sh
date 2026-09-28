#!/usr/bin/env bash
set -euo pipefail
REPO="${1:-}"
if [[ -z "$REPO" || ! -d "$REPO" ]]; then
  echo "Usage: $0 /path/to/repo" >&2
  exit 1
fi
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/skills"
DESTS=("$REPO/.agents/skills" "$REPO/.claude/skills" "$REPO/.cursor/skills")
copied=0
install_skills() {
  local d="$1"
  mkdir -p "$d"
  for s in setup-agent-guards enrich-tickets provenance-check before-implement; do
    rm -rf "$d/$s"
    cp -R "$SRC/$s" "$d/$s"
  done
  mkdir -p "$REPO/docs/agents"
  # optional checker for agents that shell out
  mkdir -p "$REPO/docs/agents/_agent-guards-lib"
  cp -f "$ROOT/lib/check_provenance.py" "$REPO/docs/agents/_agent-guards-lib/"
  echo "Installed into $d"
}
for d in "${DESTS[@]}"; do
  parent="$(dirname "$d")"
  if [[ -d "$parent" ]] || [[ "$d" == "$REPO/.agents/skills" ]]; then
    install_skills "$d"
    copied=1
  fi
done
if [[ $copied -eq 0 ]]; then
  install_skills "$REPO/.agents/skills"
fi
echo "Next: in agent run /setup-agent-guards (and install Matt skills if missing)"
