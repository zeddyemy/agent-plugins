# pstack upstream sync report

- Baseline commit: `fd6dd6f7276956a532bb78a748a8d2818b6eb5f4`
- Snapshot status: not materialized in the bootstrap commit

The first automated or local sync will import the configured pstack paths into `upstream/pstack/` and regenerate this report. Because the initial portable port predates the snapshot, all configured overlays will be review candidates on that first import.

The sync process never overwrites portable files automatically.
