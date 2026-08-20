# agent-plugins

A collection of portable engineering plugins for coding agents. One workflow source, thin runtime adapters.

## Plugins

### pstack

A portability-oriented adaptation of Lauren Tan's `pstack`, focused on rigorous engineering workflows,
verification, architecture, adversarial review, and safe parallelism.

Upstream: https://github.com/cursor/plugins/tree/main/pstack

## Claude Code

Once this repository is on GitHub:

```text
/plugin marketplace add zeddyemy/agent-plugins
/plugin install pstack@zeddyemy-agent-plugins
```

For local development:

```bash
claude plugin marketplace add .
claude plugin validate .
```

You can also install the skill files directly:

```bash
./scripts/install.sh pstack --agent claude --scope user
```

## Codex

Install at user scope:

```bash
./scripts/install.sh pstack --agent codex --scope user
```

Or into a repository:

```bash
./scripts/install.sh pstack --agent codex --scope project --project /path/to/repo
```

The default user destination is `~/.agents/skills`. Set `AGENT_SKILLS_HOME` if your Codex setup uses
a different skills root.

## Design

```text
agent-plugins/
├── .claude-plugin/marketplace.json
├── plugins/
│   └── pstack/
│       ├── .claude-plugin/plugin.json
│       ├── agents/
│       └── skills/
├── scripts/
│   ├── install.sh
│   └── validate.sh
└── docs/PORTABILITY.md
```

The core rule is simple: plugin skills describe intent and engineering policy. Harness-specific
packaging stays at the edge.

## Upstream sync

Adapted plugins can track their source projects without overwriting portability changes. For pstack:

```bash
./scripts/check-upstream.sh pstack
./scripts/sync-upstream.py pstack
```

The exact upstream revision is pinned in `upstreams/pstack.lock.json`. Imported source stays separate from `plugins/pstack/`, and `.sync-reports/pstack.md` flags overlays that need manual Claude/Codex review. A scheduled GitHub Action checks weekly and opens a draft sync PR when upstream moves. See `docs/UPSTREAM_SYNC.md`.

## Status

`pstack` is an experimental first port, not a byte-for-byte mirror of upstream. The initial version
contains the highest-leverage workflows while we validate behavior across Claude Code and Codex.

## License and attribution

This repository is MIT licensed. See `NOTICE.md` for upstream attribution.
