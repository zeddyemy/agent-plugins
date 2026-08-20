---
name: swarm
description: Parallelize independent slices of investigation, review, migration, or verification and aggregate one result.
---

# Swarm

Partition work so each worker owns a distinct slice and overlapping writes are avoided. Give every worker
the same output contract and acceptance criteria. Run slices in parallel when supported. Aggregate the
results centrally, reconcile contradictions, and verify the combined conclusion or diff before reporting.
