#!/usr/bin/env python3
# ruff: noqa: E501 — the markdown template below carries intentionally unwrapped lines (no-wrap rule).
"""Apply the compressed on-demand manifest to produce _on_demand/SKILL.md.

Run from the repository root after `.manifest.compressed.yaml` has been
reviewed and approved:

    uv run --no-project --with pyyaml python _on_demand/scripts/apply_manifest.py

The script reads `_on_demand/.manifest.compressed.yaml`, wraps the entries in the
`ondemand:` manifest frontmatter, and writes `_on_demand/SKILL.md` with the
canonical body instructions.
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
        "_on_demand/scripts/apply_manifest.py"
    ) from exc


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ONDEMAND_DIR = REPO_ROOT / "_on_demand"
TMP_ONDEMAND_DIR = REPO_ROOT / ".tmp" / "_on_demand"
COMPRESSED_PATH = TMP_ONDEMAND_DIR / ".manifest.compressed.yaml"
OUTPUT_PATH = ONDEMAND_DIR / "SKILL.md"

BODY_TEMPLATE = """# On-Demand Skill Manifest
[ref: #ondemand-intro]

> Runtime, header-only manifest: no task rules here. The frontmatter `ondemand:` block is the compressed registry of rarely used skills in `_on_demand/<skill>/`, matched without reading every on-demand `SKILL.md` header at startup.

## How the manifest is used
[ref: #ondemand-usage]

1. At bootstrap, the `_on_demand/SKILL.md` frontmatter is batch-extracted like any skill header; `runtime: true` keeps this body unread until the user asks about the on-demand mechanism.
2. During runtime re-evaluation (every new user message, every path touch), each `ondemand:` entry with `runtime: true` is evaluated as a discovered skill header under the same trigger grammar (`any`, `all`, `files`, `request`); on a match, read `_on_demand/<name>/SKILL.md` in full and resolve its `requires`.
3. Entries without `runtime: true` evaluate once at bootstrap, never mid-session.
4. `_on_demand/<skill>/SKILL.md` bodies are read only after their manifest entry matched.

## Mapping
[ref: #ondemand-mapping]

> **DEPRECATED 2026-08-31T20:08:13Z:** the table duplicated the frontmatter `ondemand:` registry verbatim and drifted stale. The manifest above is the single machine registry; the human index lives in `_on_demand/README.md`. See [ref: #ondemand-readme-index] in `_on_demand/README.md`.
"""


def load_compressed() -> dict[str, Any]:
    if not COMPRESSED_PATH.exists():
        raise SystemExit(
            f"{COMPRESSED_PATH} not found. Run harvest_manifest.py first, then compress and review."
        )
    data = yaml.safe_load(COMPRESSED_PATH.read_text(encoding="utf-8"))
    return data or {}


def main() -> int:
    data = load_compressed()
    entries = data.get("ondemand", [])
    if not entries:
        print("warning: no on-demand entries found", file=sys.stderr)

    frontmatter = {
        "name": "ondemand",
        "description": (
            "Runtime header-only manifest for on-demand skills. "
            "The frontmatter carries a compressed trigger registry so the agent can match requests "
            "without reading each on-demand SKILL.md header at startup."
        ),
        "runtime": True,
        "triggers": {
            "reason": "Header-only manifest; entries are evaluated during runtime re-evaluation."
        },
        "requires": ["frontmatter-protocol"],
        "ondemand": entries,
    }

    manifest_text = (
        "---\n"
        + yaml.safe_dump(
            frontmatter,
            sort_keys=False,
            allow_unicode=True,
            width=sys.maxsize,
            default_flow_style=False,
        )
        + "---\n\n"
        + BODY_TEMPLATE
    )

    OUTPUT_PATH.write_text(manifest_text, encoding="utf-8")
    print(
        f"wrote {OUTPUT_PATH} with {len(entries)} on-demand entr{'y' if len(entries) == 1 else 'ies'}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
