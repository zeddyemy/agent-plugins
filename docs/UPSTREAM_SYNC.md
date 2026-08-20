# Upstream sync

Adapted plugins use a **snapshot + portable overlay** model.

- `upstreams/<plugin>.json` describes the upstream repository and paths we track.
- `upstreams/<plugin>.lock.json` pins the exact imported upstream commit.
- `upstream/<plugin>/` contains the generated, unmodified upstream snapshot.
- `plugins/<plugin>/` contains the installable Claude Code/Codex adaptation.
- `.sync-reports/<plugin>.md` lists portable overlays whose upstream source changed.

The importer never writes into `plugins/<plugin>/`. Upstream changes therefore cannot silently replace portability work.

## Check for updates

```bash
./scripts/check-upstream.sh pstack
```

Exit code `0` means the lock matches upstream. Exit code `1` means a newer upstream revision exists.

## Import the latest upstream revision

```bash
./scripts/sync-upstream.py pstack
./scripts/validate.sh
```

Review `.sync-reports/pstack.md`, port relevant upstream changes into `plugins/pstack/`, then commit the snapshot, lock, report, and any portability updates together.

## Automated sync

`.github/workflows/sync-pstack.yml` runs weekly and can also be triggered manually. When upstream changes, it refreshes the snapshot and opens a draft PR. The PR is intentionally review-gated because Cursor-specific instructions may not map safely to Claude Code or Codex.

## Add another upstream plugin

Create `upstreams/<name>.json` with the repository, ref, source subdirectory, snapshot directory, portable directory, tracked paths, and overlay paths. Then run:

```bash
./scripts/sync-upstream.py <name>
```

Keep harness-specific behavior at the adapter edge rather than modifying the upstream snapshot.
