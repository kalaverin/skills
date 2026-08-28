#!/usr/bin/env python3
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

This skill is a **runtime, header-only manifest**. It does not contain task rules; it carries a registry of rarely used skills stored in `_on_demand/<skill>/` so the agent can match requests without reading every on-demand `SKILL.md` header at startup.

## How the manifest is used
[ref: #ondemand-usage]

1. At bootstrap, `_on_demand/SKILL.md` is discovered and its frontmatter is batch-extracted like any other skill header.
2. Because it carries `runtime: true`, its body is not read until the user explicitly asks about the on-demand mechanism.
3. During runtime re-evaluation (after every new user message and path touch), evaluate each entry in `ondemand:` that carries `runtime: true` as if it were a discovered skill header:
   - apply the same trigger grammar (`any`, `all`, `files`, `request`);
   - if an entry matches, read `_on_demand/<name>/SKILL.md` in full and resolve its `requires`.
   - entries without `runtime: true` are evaluated once at bootstrap and are not re-evaluated mid-session.
4. Do not read `_on_demand/<skill>/SKILL.md` bodies unless their manifest entry matched.

## Mapping
[ref: #ondemand-mapping]

| Skill | Runtime | Description |
|-------|---------|-------------|
"""


def load_compressed() -> dict[str, Any]:
    if not COMPRESSED_PATH.exists():
        raise SystemExit(
            f"{COMPRESSED_PATH} not found. Run harvest_manifest.py first, then compress and review."
        )
    data = yaml.safe_load(COMPRESSED_PATH.read_text(encoding="utf-8"))
    return data or {}


def render_body(entries: list[dict[str, Any]]) -> str:
    rows: list[str] = []
    for entry in entries:
        runtime = "yes" if entry.get("runtime") else "no"
        desc = str(entry.get("description", "")).replace("|", "\\|")
        rows.append(f"| `{entry['name']}` | {runtime} | {desc} |")
    return BODY_TEMPLATE + "\n".join(rows) + "\n"


def main() -> int:
    data = load_compressed()
    entries = data.get("skills", [])
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

    body = render_body(entries)
    manifest_text = (
        "---\n"
        + yaml.safe_dump(
            frontmatter,
            sort_keys=False,
            allow_unicode=True,
            width=120,
            default_flow_style=False,
        )
        + "---\n\n"
        + body
    )

    OUTPUT_PATH.write_text(manifest_text, encoding="utf-8")
    print(
        f"wrote {OUTPUT_PATH} with {len(entries)} on-demand entr{'y' if len(entries) == 1 else 'ies'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
