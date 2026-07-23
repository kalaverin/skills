#!/usr/bin/env python3
"""Stub: validate YAML frontmatter and naming of all Serena memory files.

TODO: implement full validation:
  - recursive scan of --memories-dir
  - enforce file and directory naming: ^[a-zA-Z0-9]+(_[a-zA-Z0-9]+)*$
  - parse YAML frontmatter between the first '---' markers
  - check mandatory fields: title, created_at, updated_at, repo, branch,
    commit, committed_at, source
  - detect and auto-fix the 'commited_at' -> 'committed_at' typo
  - verify title matches the first Markdown H1
  - verify timestamps are UTC ISO 8601 ending in 'Z'
  - verify commit is a 7-character hex string
  - normalize source paths to project-relative
  - detect legacy plain-text headers (Recorded, Date, Git branch, Branch,
    Latest commit, Latest commit date/datetime, Location)
  - detect no-H1 files and suggest generated titles
  - emit a JSON report and non-zero exit code on invalid files
  - keep report small; full per-file details can go to /tmp/serena_audit_full.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def scan_memories(memories_dir: Path) -> list[dict]:
    """Return a list of validation result dicts, one per .md file."""
    results = []
    for path in sorted(memories_dir.rglob("*.md")):
        results.append(
            {
                "path": str(path.relative_to(memories_dir)),
                "status": "stub",
                "errors": ["validation not yet implemented"],
            }
        )
    return results


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate Serena memory frontmatter and naming. (stub)"
    )
    parser.add_argument(
        "--memories-dir",
        type=Path,
        default=Path(".serena/memories"),
        help="Path to the Serena memories directory",
    )
    args = parser.parse_args(argv)

    if not args.memories_dir.is_dir():
        print(
            json.dumps({"error": f"memories directory not found: {args.memories_dir}"}),
            file=sys.stderr,
        )
        return 2

    results = scan_memories(args.memories_dir)
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
