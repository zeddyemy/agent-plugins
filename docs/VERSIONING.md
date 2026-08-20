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

## CI enforcement

Pull requests run `scripts/check-plugin-version.py` against the PR base branch. If pstack contents changed and the version did not, CI fails.

`scripts/validate.sh` also verifies that the marketplace and plugin manifests contain the same valid SemVer version.

This makes Claude Code marketplace updates explicit and prevents plugin changes from landing under an unchanged version.
