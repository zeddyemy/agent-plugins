---
name: interrogate
description: Adversarially review a diff or design using independent lenses before shipping high-risk work.
---

# Interrogate

Review the same artifact through independent lenses: correctness, state/concurrency, API boundaries,
security/data integrity where relevant, performance where relevant, and maintainability. Prefer
independent parallel reviewers when the runtime supports them. Aggregate findings yourself. Dismiss
noise with a concrete reason. Rank accepted findings by impact and confidence, then verify fixes.
