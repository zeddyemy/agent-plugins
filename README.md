# Agent Plugins

A portable collection of reusable agent plugins for **Claude Code** and **OpenAI Codex**.

The repository keeps plugin behavior separate from harness-specific packaging so the same engineering workflows can be installed into multiple coding agents without maintaining divergent copies.

## Plugins

### pstack

A portable adaptation of Lauren Tan's [`pstack`](https://github.com/cursor/plugins/tree/main/pstack), focused on rigorous engineering workflows, verification, architecture, parallel investigation, and concise implementation.

This initial port includes:

- `poteto-mode`
- `architect`
- `tdd`
- `interrogate`
- `blast-radius`
- `how`
- `swarm`
- `arena`
- the `poteto-agent` Claude subagent

See [`plugins/pstack/README.md`](plugins/pstack/README.md) for details.

## Install

### Claude Code

This repository is a Claude Code plugin marketplace.

```text
/plugin marketplace add zeddyemy/agent-plugins
/plugin install pstack@zeddyemy-agent-plugins
```

For local development or project-scoped installation, use the installer below.

### Codex

Install a plugin into your user-level Codex skills directory:

```bash
./scripts/install.sh pstack --agent codex --scope user
```

Install into the current project:

```bash
./scripts/install.sh pstack --agent codex --scope project
```

### Claude Code via script

```bash
./scripts/install.sh pstack --agent claude --scope user
```

or:

```bash
./scripts/install.sh pstack --agent claude --scope project
```

## Repository layout

```text
agent-plugins/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── pstack/
│       ├── .claude-plugin/
│       ├── agents/
│       └── skills/
├── docs/
│   └── PORTABILITY.md
└── scripts/
    ├── install.sh
    └── validate.sh
```

Each plugin owns its portable skills. Harness-specific metadata stays at the edges.

## Design goals

1. **Portable first.** Skills should describe intent and engineering policy rather than vendor-specific tool calls.
2. **Thin adapters.** Claude Code, Codex, and future harnesses should require minimal packaging glue.
3. **Upstream-friendly.** Adapted plugins retain attribution and can be periodically resynced from their source projects.
4. **Verifiable.** Installation and repository structure are validated by scripts rather than documentation alone.
5. **Composable.** This is a collection, not a monolithic agent personality. Install only the plugins you want.

## Validate

```bash
./scripts/validate.sh
```

## License

This collection is MIT licensed. Adapted plugins retain their upstream notices and licensing. See [`NOTICE.md`](NOTICE.md).
