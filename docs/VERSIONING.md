# Plugin versioning

`pstack` uses semantic versioning in both Claude Code manifests:

- `.claude-plugin/marketplace.json`
- `plugins/pstack/.claude-plugin/plugin.json`

The versions must always match.

## When to bump

Any change under `plugins/pstack/` that changes installed plugin behavior must bump the pstack version in the same PR.

Use:

```bash
python3 scripts/bump-plugin-version.py patch
python3 scripts/bump-plugin-version.py minor
python3 scripts/bump-plugin-version.py major
```

Use a patch bump for fixes and small skill changes. Use a minor bump for new skills or backward-compatible capability additions. Use a major bump for incompatible behavior or packaging changes.

## Local validation

Run these checks before publishing a plugin change:

```bash
./scripts/validate.sh
python3 scripts/check-plugin-version.py --base origin/main
```

`scripts/check-plugin-version.py` exits non-zero when installed pstack content changed without a version bump. `scripts/validate.sh` verifies that the marketplace and plugin manifests contain the same valid SemVer version.

These checks stay local by default so GitHub account or Actions availability cannot turn a healthy plugin change into a red PR status.
