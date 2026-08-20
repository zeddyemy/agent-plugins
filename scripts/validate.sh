#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 - <<'PY2' "$ROOT"
import json, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
marketplace = json.loads((root / '.claude-plugin/marketplace.json').read_text())
plugin = json.loads((root / 'plugins/pstack/.claude-plugin/plugin.json').read_text())
marketplace_plugin = next(item for item in marketplace['plugins'] if item['name'] == 'pstack')
assert plugin['version'] == marketplace_plugin['version'], 'pstack version mismatch between plugin and marketplace manifests'
assert re.fullmatch(r'\d+\.\d+\.\d+', plugin['version']), 'pstack version must be SemVer x.y.z'

skills = list((root / 'plugins/pstack/skills').glob('*/SKILL.md'))
assert skills, 'no skills found'
for path in skills:
    text = path.read_text()
    assert text.startswith('---\n'), f'missing frontmatter: {path}'
    assert '\nname:' in text and '\ndescription:' in text, f'incomplete frontmatter: {path}'

config = json.loads((root / 'upstreams/pstack.json').read_text())
lock = json.loads((root / 'upstreams/pstack.lock.json').read_text())
assert config['name'] == lock['name'] == 'pstack'
assert config['repository'] == lock['repository']
assert len(lock['commit']) == 40, 'upstream lock must pin a full commit SHA'
assert config['tracked_paths'], 'upstream tracked_paths cannot be empty'
assert set(config['overlay_paths']).issubset(set(config['tracked_paths'])), 'overlay paths must be tracked upstream'
for required in [
    'scripts/sync-upstream.py',
    'scripts/check-upstream.sh',
    'scripts/check-plugin-version.py',
    'scripts/bump-plugin-version.py',
    'docs/UPSTREAM_SYNC.md',
    '.github/workflows/sync-pstack.yml',
    '.github/workflows/validate.yml',
]:
    assert (root / required).exists(), f'missing repository artifact: {required}'
print(f"validated {len(skills)} skills, pstack {plugin['version']}, and upstream sync metadata")
PY2
