#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'TXT'
Usage: ./scripts/install.sh <plugin> --agent <claude|codex> [--scope <user|project>] [--project <path>]

Examples:
  ./scripts/install.sh pstack --agent claude --scope user
  ./scripts/install.sh pstack --agent codex --scope user
  ./scripts/install.sh pstack --agent codex --scope project --project /path/to/repo
TXT
}

PLUGIN="${1:-}"
[[ -n "$PLUGIN" ]] || { usage; exit 2; }
shift || true

AGENT=""
SCOPE="user"
PROJECT="${PWD}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --agent) AGENT="$2"; shift 2 ;;
    --scope) SCOPE="$2"; shift 2 ;;
    --project) PROJECT="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

[[ "$PLUGIN" == "pstack" ]] || { echo "Unknown plugin: $PLUGIN" >&2; exit 2; }
[[ "$AGENT" == "claude" || "$AGENT" == "codex" ]] || { echo "--agent must be claude or codex" >&2; exit 2; }
[[ "$SCOPE" == "user" || "$SCOPE" == "project" ]] || { echo "--scope must be user or project" >&2; exit 2; }

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/plugins/$PLUGIN"

if [[ "$AGENT" == "claude" ]]; then
  if [[ "$SCOPE" == "user" ]]; then
    SKILLS_DEST="$HOME/.claude/skills"
    AGENTS_DEST="$HOME/.claude/agents"
  else
    SKILLS_DEST="$PROJECT/.claude/skills"
    AGENTS_DEST="$PROJECT/.claude/agents"
  fi
else
  if [[ "$SCOPE" == "user" ]]; then
    SKILLS_DEST="${AGENT_SKILLS_HOME:-$HOME/.agents/skills}"
  else
    SKILLS_DEST="$PROJECT/.agents/skills"
  fi
  AGENTS_DEST=""
fi

mkdir -p "$SKILLS_DEST"
for skill in "$SRC"/skills/*; do
  name="$(basename "$skill")"
  rm -rf "$SKILLS_DEST/$name"
  cp -R "$skill" "$SKILLS_DEST/$name"
done

if [[ "$AGENT" == "claude" && -d "$SRC/agents" ]]; then
  mkdir -p "$AGENTS_DEST"
  cp "$SRC"/agents/*.md "$AGENTS_DEST"/
fi

printf 'Installed %s for %s (%s scope)\n' "$PLUGIN" "$AGENT" "$SCOPE"
printf 'Skills: %s\n' "$SKILLS_DEST"
if [[ -n "$AGENTS_DEST" ]]; then
  printf 'Agents: %s\n' "$AGENTS_DEST"
fi
