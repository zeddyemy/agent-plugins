# Portability contract

Portable plugin content should express capabilities rather than harness APIs.

Use semantic instructions such as:

- delegate a read-only investigation
- run independent slices in parallel
- ask the user only for genuine product preferences
- verify the real artifact
- keep writes isolated

Avoid hard dependencies on names such as Cursor `Task`, `AskQuestion`, `subagent_type`, or fixed model IDs.
Runtime-specific metadata belongs in adapter/plugin manifests, not in the core workflow.

## Claude Code

Claude Code consumes this repository as a plugin marketplace. The pstack plugin also includes a
`poteto-agent` subagent. Users can add the marketplace from GitHub and install pstack by name.

## Codex

Codex follows the Agent Skills model. The installer copies the plugin skills to `.agents/skills`
at user or project scope. Codex plugin packaging is evolving, so the skills directory remains the
portable baseline while plugin metadata can be added without changing skill content.
