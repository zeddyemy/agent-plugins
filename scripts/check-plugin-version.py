#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_MANIFEST = Path("plugins/pstack/.claude-plugin/plugin.json")
MARKETPLACE_MANIFEST = Path(".claude-plugin/marketplace.json")
PLUGIN_ROOT = "plugins/pstack/"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def current_versions() -> tuple[str, str]:
    plugin = json.loads((ROOT / PLUGIN_MANIFEST).read_text())
    marketplace = json.loads((ROOT / MARKETPLACE_MANIFEST).read_text())
    marketplace_plugin = next(item for item in marketplace["plugins"] if item["name"] == "pstack")
    return plugin["version"], marketplace_plugin["version"]


def version_at(ref: str) -> str:
    raw = git("show", f"{ref}:{PLUGIN_MANIFEST.as_posix()}")
    return json.loads(raw)["version"]


def changed_plugin_files(base: str) -> list[str]:
    names = git("diff", "--name-only", f"{base}...HEAD").splitlines()
    ignored = {PLUGIN_MANIFEST.as_posix()}
    return [name for name in names if name.startswith(PLUGIN_ROOT) and name not in ignored]


def main() -> int:
    parser = argparse.ArgumentParser(description="Require pstack version bumps when plugin contents change.")
    parser.add_argument("--base", default="origin/main")
    args = parser.parse_args()

    plugin_version, marketplace_version = current_versions()
    if plugin_version != marketplace_version:
        raise SystemExit(
            f"version mismatch: plugin.json={plugin_version}, marketplace.json={marketplace_version}"
        )

    changed = changed_plugin_files(args.base)
    if not changed:
        print(f"pstack version {plugin_version}; no versioned plugin content changed")
        return 0

    previous = version_at(args.base)
    if previous == plugin_version:
        files = "\n  - ".join(changed)
        raise SystemExit(
            "pstack contents changed without a version bump.\n"
            f"current version: {plugin_version}\n"
            f"changed files:\n  - {files}\n"
            "Run: python3 scripts/bump-plugin-version.py <major|minor|patch>"
        )

    print(f"pstack version bumped: {previous} -> {plugin_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
