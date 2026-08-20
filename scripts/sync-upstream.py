#!/usr/bin/env python3
"""Import a pinned upstream plugin snapshot and report portability review points."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def run(*args: str, cwd: Path | None = None) -> str:
    """Run a command and return stripped stdout."""
    result = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk."""
    return json.loads(path.read_text())


def write_json(path: Path, value: dict[str, Any]) -> None:
    """Write deterministic, human-readable JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def copy_path(source: Path, destination: Path) -> None:
    """Copy a file or directory, replacing an existing destination."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        shutil.rmtree(destination) if destination.is_dir() else destination.unlink()
    shutil.copytree(source, destination) if source.is_dir() else shutil.copy2(source, destination)


def changed_overlay_paths(config: dict[str, Any], previous_snapshot: Path, new_snapshot: Path) -> list[str]:
    """Return overlays whose upstream source changed since the previous snapshot."""
    changed: list[str] = []
    for relative in config.get("overlay_paths", []):
        old = previous_snapshot / relative
        new = new_snapshot / relative
        if not old.exists() or not new.exists():
            changed.append(relative)
            continue
        if old.is_dir() != new.is_dir():
            changed.append(relative)
            continue
        if old.is_file():
            if old.read_bytes() != new.read_bytes():
                changed.append(relative)
            continue
        old_files = {p.relative_to(old) for p in old.rglob("*") if p.is_file()}
        new_files = {p.relative_to(new) for p in new.rglob("*") if p.is_file()}
        if old_files != new_files or any((old / p).read_bytes() != (new / p).read_bytes() for p in old_files & new_files):
            changed.append(relative)
    return changed


def render_report(name: str, old_commit: str | None, new_commit: str, changed: list[str]) -> str:
    """Render the review report for an imported upstream revision."""
    lines = [
        f"# {name} upstream sync report",
        "",
        f"- Previous commit: `{old_commit or 'none'}`",
        f"- Imported commit: `{new_commit}`",
        f"- Generated: `{datetime.now(timezone.utc).isoformat()}`",
        "",
    ]
    if changed:
        lines += [
            "## Portable overlays requiring review",
            "",
            "Upstream changed these source paths. Review and manually port relevant behavior into `plugins/pstack/`.",
            "",
            *[f"- `{path}`" for path in changed],
        ]
    else:
        lines += ["## Portable overlays", "", "No tracked overlay source changed in this sync."]
    lines += [
        "",
        "The sync process never overwrites portable files automatically.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plugin", nargs="?", default="pstack")
    parser.add_argument("--check", action="store_true", help="Only check whether upstream moved")
    parser.add_argument("--ref", help="Override the configured upstream ref")
    args = parser.parse_args()

    config_path = ROOT / "upstreams" / f"{args.plugin}.json"
    lock_path = ROOT / "upstreams" / f"{args.plugin}.lock.json"
    if not config_path.exists():
        print(f"Unknown upstream plugin: {args.plugin}", file=sys.stderr)
        return 2

    config = load_json(config_path)
    lock = load_json(lock_path) if lock_path.exists() else {}
    ref = args.ref or config["ref"]

    with tempfile.TemporaryDirectory(prefix=f"sync-{args.plugin}-") as temp:
        checkout = Path(temp) / "repo"
        run("git", "clone", "--quiet", "--depth", "1", "--branch", ref, config["repository"], str(checkout))
        commit = run("git", "rev-parse", "HEAD", cwd=checkout)
        previous_commit = lock.get("commit")

        if args.check:
            if previous_commit == commit:
                print(f"{args.plugin}: up to date at {commit}")
                return 0
            print(f"{args.plugin}: update available {previous_commit or 'none'} -> {commit}")
            return 1

        staging = Path(temp) / "snapshot"
        source_root = checkout / config["source_subdir"]
        for relative in config["tracked_paths"]:
            source = source_root / relative
            if not source.exists():
                raise FileNotFoundError(f"Configured upstream path does not exist: {relative}")
            copy_path(source, staging / relative)

        snapshot = ROOT / config["snapshot_dir"]
        changed = changed_overlay_paths(config, snapshot, staging) if snapshot.exists() else list(config.get("overlay_paths", []))
        if snapshot.exists():
            shutil.rmtree(snapshot)
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(staging, snapshot)

        write_json(
            lock_path,
            {
                "name": args.plugin,
                "repository": config["repository"],
                "ref": ref,
                "commit": commit,
                "imported_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        report = ROOT / ".sync-reports" / f"{args.plugin}.md"
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(render_report(args.plugin, previous_commit, commit, changed))
        print(f"{args.plugin}: imported {commit}")
        print(f"review report: {report.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
