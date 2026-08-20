# pstack portable

A runtime-neutral adaptation of Lauren Tan's `pstack` for Claude Code and OpenAI Codex.

This first port keeps the highest-leverage workflows and removes Cursor-only tool names,
model IDs, and orchestration assumptions. Upstream remains authoritative for the original
workflow design.

Included skills:

- `poteto-mode`
- `architect`
- `tdd`
- `interrogate`
- `blast-radius`
- `how`
- `swarm`
- `arena`

The port deliberately uses semantic capabilities such as "delegate", "run in parallel",
and "verify against the real artifact" instead of harness-specific APIs. Each runtime is
free to map those capabilities onto its own subagent/tool system.
