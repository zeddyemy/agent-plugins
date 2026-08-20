---
name: blast-radius
description: Determine what a deceptively small change can affect before implementation or merge.
---

# Blast radius

Trace direct callers, shared types, persistence/schema assumptions, generated artifacts, caches,
side effects, public API consumers, and tests. Identify the invariant that makes the change safe and
prove that invariant with code search, runtime evidence, or tests. Do not substitute a list of files
for a causal impact analysis.
