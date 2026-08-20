#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_PATH = ROOT / "plugins/pstack/.claude-plugin/plugin.json"
MARKETPLACE_PATH = ROOT / ".claude-plugin/marketplace.json"
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def bump(version: str, part: str) -> str:
    match = SEMVER.fullmatch(version)
    if not match:
        raise SystemExit(f"unsupported version: {version}")
    major, minor, patch = map(int, match.groups())
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump the portable pstack plugin version.")
    parser.add_argument("part", choices=("major", "minor", "patch"))
    args = parser.parse_args()

    plugin = json.loads(PLUGIN_PATH.read_text())
    marketplace = json.loads(MARKETPLACE_PATH.read_text())
    entry = next(item for item in marketplace["plugins"] if item["name"] == "pstack")

    if plugin["version"] != entry["version"]:
        raise SystemExit("plugin and marketplace versions are already out of sync")

    old = plugin["version"]
    new = bump(old, args.part)
    plugin["version"] = new
    entry["version"] = new

    write_json(PLUGIN_PATH, plugin)
    write_json(MARKETPLACE_PATH, marketplace)
    print(f"pstack: {old} -> {new}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
