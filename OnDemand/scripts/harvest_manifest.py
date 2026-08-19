#!/usr/bin/env python3
"""Harvest raw OnDemand skill headers into a manifest file.

Run from the repository root:

    uv run --no-project --with pyyaml python OnDemand/scripts/harvest_manifest.py

This produces OnDemand/.manifest.raw.yaml with verbatim copies of every
on-demand skill's frontmatter fields needed for trigger evaluation. The raw
manifest is then compressed by a subagent before being applied to
OnDemand/SKILL.md.
"""

from __future__ import annotations

import pathlib
import sys
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyYAML is required. Run: uv run --no-project --with pyyaml python "
        "OnDemand/scripts/harvest_manifest.py"
    ) from exc


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ONDEMAND_DIR = REPO_ROOT / "OnDemand"
TMP_ONDEMAND_DIR = REPO_ROOT / ".tmp" / "OnDemand"
RAW_PATH = TMP_ONDEMAND_DIR / ".manifest.raw.yaml"


def extract_frontmatter(path: pathlib.Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path} has no frontmatter")
    lines = text.splitlines()
    for idx in range(1, len(lines)):
        if lines[idx].rstrip() == "---":
            frontmatter_text = "\n".join(lines[1:idx])
            return yaml.safe_load(frontmatter_text) or {}
    raise ValueError(f"{path} has unclosed frontmatter")


def harvest() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for skill_dir in sorted(ONDEMAND_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name in {"scripts", "prompts"}:
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            print(
                f"warning: {skill_dir.name}/ has no SKILL.md, skipping", file=sys.stderr
            )
            continue
        header = extract_frontmatter(skill_file)
        entry: dict[str, Any] = {
            "name": header.get("name", skill_dir.name),
            "description": header.get("description", ""),
            "triggers": header.get("triggers", {}),
        }
        if header.get("runtime"):
            entry["runtime"] = True
        entries.append(entry)
    return entries


def main() -> int:
    TMP_ONDEMAND_DIR.mkdir(parents=True, exist_ok=True)
    entries = harvest()
    RAW_PATH.write_text(
        yaml.safe_dump(
            {"skills": entries},
            sort_keys=False,
            allow_unicode=True,
            width=120,
            default_flow_style=False,
        ),
        encoding="utf-8",
    )
    print(
        f"wrote {RAW_PATH} with {len(entries)} raw entr{'y' if len(entries) == 1 else 'ies'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
