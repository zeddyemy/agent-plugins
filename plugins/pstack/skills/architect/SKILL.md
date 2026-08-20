---
name: architect
description: Resolve a design before implementing code that crosses function, module, service, persistence, or protocol boundaries.
---

# Architect

Map callers, data shapes, ownership, error boundaries, and state transitions before editing code.
Generate at least two plausible designs when the choice is material. Compare reader load, illegal
states, migration cost, failure behavior, concurrency, and verification strategy. Prefer the design
that makes the domain obvious and removes special cases. Return a concrete implementation shape,
not a generic architecture essay.
