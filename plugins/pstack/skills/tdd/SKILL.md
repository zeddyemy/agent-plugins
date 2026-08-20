---
name: tdd
description: Reproduce a bug or behavior gap with a cheap deterministic test before implementing the fix.
---

# TDD

Find the narrowest deterministic test surface. Write a failing test that captures the requested
behavior without overfitting implementation details. Run it and preserve the failure evidence. Make
the smallest production change that fixes the root cause. Run the focused test, then the nearest
relevant suite. If a cheap deterministic test does not exist, explain the runtime verification used instead.
