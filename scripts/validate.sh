#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 - <<'PY' "$ROOT"
import json, pathlib, sys
root = pathlib.Path(sys.argv[1])
json.loads((root / '.claude-plugin/marketplace.json').read_text())
json.loads((root / 'plugins/pstack/.claude-plugin/plugin.json').read_text())
skills = list((root / 'plugins/pstack/skills').glob('*/SKILL.md'))
assert skills, 'no skills found'
for path in skills:
    text = path.read_text()
    assert text.startswith('---\n'), f'missing frontmatter: {path}'
    assert '\nname:' in text and '\ndescription:' in text, f'incomplete frontmatter: {path}'
print(f'validated {len(skills)} skills')
PY
