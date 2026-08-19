"""Dump all ruff rules into per-group Markdown files for the distill pipeline.

Fetches `ruff rule --all --output-format json` (cached in `cache/`), groups the
rules deterministically by linter (splitting oversized groups by code prefix,
merging tiny ones into `misc`), and writes `groups/*.md`, `manifest.json`, and
`_UPDATES.md`. Re-render from an unchanged cache is byte-identical: the only
timestamp comes from the cache's `fetched_at`.
"""

# ruff: noqa: INP001
# scripts/ is a collection of standalone executables, not an importable package.

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum, auto
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / ".tmp" / "ruff-rules"
DUMP_SOURCE = "uvx ruff rule --all --output-format json"
SPLIT_THRESHOLD = 50
MERGE_THRESHOLD = 5


class RuleStatus(StrEnum):
    """Lifecycle status of a ruff rule (Removed rules never reach here)."""

    STABLE = auto()
    PREVIEW = auto()


@dataclass(frozen=True)
class Rule:
    """One normalized ruff rule ready for grouping and rendering."""

    code: str
    prefix: str
    linter: str
    name: str
    status: RuleStatus
    fix: str
    summary: str
    messages: tuple[str, ...]
    explanation: str
    sha1: str


@dataclass(frozen=True)
class Group:
    """A named set of rules rendered into one `groups/<slug>.md` file."""

    slug: str
    linter: str
    rules: tuple[Rule, ...]
    misc_sections: tuple[tuple[str, tuple[Rule, ...]], ...] = ()


@dataclass(frozen=True)
class RuleDump:
    """The full normalized dump plus its provenance metadata."""

    version: str
    fetched_at: str
    rules: tuple[Rule, ...]
    removed: tuple[str, ...]


@dataclass(frozen=True)
class ManifestEntry:
    """One rule's fingerprint as stored in `manifest.json`."""

    code: str
    linter: str
    status: str
    sha1: str
    group: str


@dataclass(frozen=True)
class Manifest:
    """The persisted snapshot of the previous run, if any."""

    version: str
    entries: tuple[ManifestEntry, ...]


@dataclass(frozen=True)
class Updates:
    """The diff between the previous manifest and the current dump."""

    added: tuple[tuple[str, str], ...] = ()  # (code, group)
    removed: tuple[tuple[str, str], ...] = ()  # (code, old group)
    changed: tuple[tuple[str, str], ...] = ()  # (code, group)
    moved: tuple[tuple[str, str, str], ...] = ()  # (code, old group, new group)
    affected_groups: tuple[str, ...] = ()


@dataclass(frozen=True)
class Theme:
    """One thematic category from `themes.json`."""

    slug: str
    title: str
    essence: str
    codes: tuple[str, ...]


@dataclass(frozen=True)
class ThemeSet:
    """The approved taxonomy: themes plus consciously dropped codes."""

    themes: tuple[Theme, ...]
    dropped: tuple[tuple[str, str], ...]  # (code, reason)


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="ignore the cache and fetch a fresh dump from ruff",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="output directory (default: %(default)s)",
    )
    parser.add_argument(
        "--assemble",
        action="store_true",
        help="build themes/*.md from themes.json using the cache only",
    )
    parser.add_argument(
        "--themes",
        type=Path,
        default=None,
        help="path to themes.json (default: <out-dir>/themes.json)",
    )
    return parser.parse_args(argv)


def _run_ruff(args: Sequence[str]) -> str:
    """Run `uv tool run ruff <args>` and return stdout; crash loud on any failure."""
    uv = shutil.which("uv")
    if uv is None:
        raise SystemExit("uvx not found in PATH; cannot fetch ruff rules")
    # Static argument vector against a resolved binary path; no untrusted input.
    result = subprocess.run(  # noqa: S603
        [uv, "tool", "run", "--quiet", "ruff", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = (
            f"ruff {' '.join(args)} failed (exit {result.returncode}):\n"
            f"{result.stderr.strip()}"
        )
        raise SystemExit(message)
    return result.stdout


def _download() -> dict[str, Any]:
    """Fetch the raw dump payload from ruff (the codec's outer edge)."""
    listing = _run_ruff(["rule", "--all", "--output-format", "json"])
    version = _run_ruff(["--version"]).split()[-1]
    fetched_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    return {
        "version": version,
        "fetched_at": fetched_at,
        "rules": json.loads(listing),
    }


def _normalize(raw: dict[str, Any]) -> Rule | str:
    """Turn one raw rule dict into a Rule, or return the code if Removed."""
    status_key = next(iter(raw["status"]))
    if status_key == "Removed":
        return raw["code"]
    fix = raw["fix_availability"]
    return Rule(
        code=raw["code"],
        prefix=re.sub(r"\d+$", "", raw["code"]),
        linter=raw["linter"],
        name=raw["name"],
        status=RuleStatus(status_key.lower()),
        fix="unavailable" if fix == "None" else fix.lower(),
        summary=raw["summary"],
        messages=tuple(raw["message_formats"]),
        explanation=raw["explanation"].rstrip(),
        # Content fingerprint for change detection, not a security primitive.
        sha1=hashlib.sha1(raw["explanation"].encode("utf-8")).hexdigest(),  # noqa: S324
    )


def _to_dump(payload: dict[str, Any]) -> RuleDump:
    """Normalize the raw cache payload across the codec boundary."""
    rules = []
    removed = []
    for raw in payload["rules"]:
        normalized = _normalize(raw)
        if isinstance(normalized, Rule):
            rules.append(normalized)
        else:
            removed.append(normalized)
    return RuleDump(
        version=payload["version"],
        fetched_at=payload["fetched_at"],
        rules=tuple(sorted(rules, key=lambda rule: rule.code)),
        removed=tuple(sorted(removed)),
    )


def fetch_rules(cache: Path, refresh: bool) -> RuleDump:
    """Load the dump from cache or download it; the cache stores raw JSON."""
    if not refresh and cache.exists():
        payload = json.loads(cache.read_text(encoding="utf-8"))
    else:
        payload = _download()
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(payload), encoding="utf-8")
    return _to_dump(payload)


def _slugify(linter: str, prefix: str | None = None) -> str:
    base = linter.lower().replace(" rules", "")
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    if prefix is None:
        return base
    return f"{base}-{prefix.lower()}"


def group_rules(rules: tuple[Rule, ...]) -> tuple[Group, ...]:
    """Group by linter; split >50 with 2+ prefixes; merge <5 into misc."""
    by_linter: dict[str, list[Rule]] = {}
    for rule in rules:
        by_linter.setdefault(rule.linter, []).append(rule)
    groups = []
    small = []
    for linter in sorted(by_linter):
        linter_rules = tuple(sorted(by_linter[linter], key=lambda r: r.code))
        if len(linter_rules) < MERGE_THRESHOLD:
            small.append((linter, linter_rules))
            continue
        prefixes = sorted({rule.prefix for rule in linter_rules})
        if len(linter_rules) > SPLIT_THRESHOLD and len(prefixes) > 1:
            for prefix in prefixes:
                sub = tuple(r for r in linter_rules if r.prefix == prefix)
                groups.append(
                    Group(
                        slug=_slugify(linter, prefix),
                        linter=f"{linter} ({prefix})",
                        rules=sub,
                    ),
                )
        else:
            groups.append(
                Group(slug=_slugify(linter), linter=linter, rules=linter_rules),
            )
    if small:
        small.sort(key=lambda item: (-len(item[1]), item[0]))
        misc_rules = tuple(rule for _, section in small for rule in section)
        groups.append(
            Group(
                slug="misc",
                linter="misc (merged small linters)",
                rules=misc_rules,
                misc_sections=tuple(small),
            ),
        )
    return tuple(sorted(groups, key=lambda group: (-len(group.rules), group.slug)))


def load_manifest(path: Path) -> Manifest | None:
    """Read the previous manifest; None means this is the initial dump."""
    if not path.exists():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    entries = tuple(
        ManifestEntry(
            code=code,
            linter=entry["linter"],
            status=entry["status"],
            sha1=entry["sha1"],
            group=entry["group"],
        )
        for code, entry in raw["rules"].items()
    )
    return Manifest(version=raw["version"], entries=entries)


def diff_manifest(
    old: Manifest | None,
    groups: tuple[Group, ...],
    removed_codes: tuple[str, ...],
) -> Updates:
    """Diff the current groups against the previous manifest."""
    if old is None:
        return Updates(
            affected_groups=tuple(group.slug for group in groups),
        )
    previous = {entry.code: entry for entry in old.entries}
    current: dict[str, ManifestEntry] = {}
    for group in groups:
        for rule in group.rules:
            current[rule.code] = ManifestEntry(
                code=rule.code,
                linter=rule.linter,
                status=rule.status.value,
                sha1=rule.sha1,
                group=group.slug,
            )
    added = []
    changed = []
    moved = []
    affected = set()
    for code in sorted(current):
        entry = current[code]
        former = previous.get(code)
        if former is None:
            added.append((code, entry.group))
            affected.add(entry.group)
        elif former.sha1 != entry.sha1:
            changed.append((code, entry.group))
            affected.add(entry.group)
        if former is not None and former.group != entry.group:
            moved.append((code, former.group, entry.group))
            affected.update((former.group, entry.group))
    removed = []
    vanished = {code for code in previous if code not in current}
    vanished.update(code for code in removed_codes if code in previous)
    for code in sorted(vanished):
        removed.append((code, previous[code].group))
        affected.add(previous[code].group)
    return Updates(
        added=tuple(added),
        removed=tuple(removed),
        changed=tuple(changed),
        moved=tuple(moved),
        affected_groups=tuple(sorted(affected)),
    )


def _render_rule(rule: Rule, level: int) -> list[str]:
    heading = "#" * level
    lines = [f"{heading} {rule.code} — {rule.name}", ""]
    lines.append(f"- status: {rule.status.value}")
    lines.append(f"- fix: {rule.fix}")
    lines.append(f"- summary: {rule.summary}")
    if rule.messages:
        quoted = "; ".join(f'"{message}"' for message in rule.messages)
        lines.append(f"- messages: {quoted}")
    lines.extend(["", rule.explanation, ""])
    return lines


def render_group(group: Group, dump: RuleDump) -> str:
    """Render one `groups/<slug>.md` file; deterministic for a fixed dump."""
    stable = sum(1 for rule in group.rules if rule.status is RuleStatus.STABLE)
    preview = len(group.rules) - stable
    lines = [
        (
            f"# Group: {group.linter} "
            f"({len(group.rules)} rules: {stable} stable, {preview} preview)"
        ),
        "",
        f"- linter: {group.linter}",
        f"- slug: {group.slug}",
        f"- ruff: {dump.version}",
        f"- generated: {dump.fetched_at}",
        f"- source: {DUMP_SOURCE}",
        "",
    ]
    if group.misc_sections:
        for linter, section in group.misc_sections:
            lines.append(f"## {linter} ({len(section)} rules)")
            lines.append("")
            for rule in section:
                lines.extend(_render_rule(rule, level=3))
    else:
        for rule in group.rules:
            lines.extend(_render_rule(rule, level=2))
    return "\n".join(lines).rstrip() + "\n"


def render_manifest(groups: tuple[Group, ...], dump: RuleDump) -> str:
    entries = {}
    for group in groups:
        for rule in group.rules:
            entries[rule.code] = {
                "linter": rule.linter,
                "status": rule.status.value,
                "sha1": rule.sha1,
                "group": group.slug,
            }
    payload = {
        "version": dump.version,
        "generated_at": dump.fetched_at,
        "rules": entries,
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def render_updates(updates: Updates, old: Manifest | None, dump: RuleDump) -> str:
    """Render `_UPDATES.md`: the machine-readable change report per group."""
    lines = ["# Ruff rules update", ""]
    if old is None:
        lines.append(f"- ruff: {dump.version} (initial dump)")
    else:
        lines.append(f"- ruff: {old.version} → {dump.version}")
    lines.append(f"- generated: {dump.fetched_at}")
    lines.extend(["", "## Summary", ""])
    if old is None:
        lines.append(f"initial dump: {len(updates.affected_groups)} groups affected")
    else:
        lines.append(
            f"added: {len(updates.added)} | removed: {len(updates.removed)}"
            f" | changed: {len(updates.changed)} | moved: {len(updates.moved)}",
        )
        lines.append(
            f"affected groups ({len(updates.affected_groups)}): "
            f"{', '.join(updates.affected_groups) or 'none'}",
        )
    if updates.added:
        lines.extend(["", "## Added", ""])
        lines.extend(f"- `{code}` → {group}" for code, group in updates.added)
    if updates.removed:
        lines.extend(["", "## Removed", ""])
        lines.extend(
            f"- `{code}` (was: {group}) — clean from the target corpus"
            for code, group in updates.removed
        )
    if updates.changed:
        lines.extend(["", "## Changed", ""])
        lines.extend(
            f"- `{code}` ({group}) — explanation changed, re-distill"
            for code, group in updates.changed
        )
    if updates.moved:
        lines.extend(["", "## Moved", ""])
        lines.extend(
            f"- `{code}`: {old_group} → {new_group} — update both corpus files"
            for code, old_group, new_group in updates.moved
        )
    return "\n".join(lines).rstrip() + "\n"


def load_themes(path: Path) -> ThemeSet:
    """Parse `themes.json` across the codec boundary."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    return ThemeSet(
        themes=tuple(
            Theme(
                slug=entry["slug"],
                title=entry["title"],
                essence=entry["essence"],
                codes=tuple(entry["codes"]),
            )
            for entry in raw["themes"]
        ),
        dropped=tuple(
            (entry["code"], entry["reason"]) for entry in raw.get("dropped", [])
        ),
    )


def _validate_theme(theme: Theme, known: set[str]) -> tuple[str, ...]:
    problems = []
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", theme.slug):
        problems.append(f"invalid slug (kebab-case required): {theme.slug}")
    if len(set(theme.codes)) != len(theme.codes):
        problems.append(f"{theme.slug}: duplicate codes inside the theme")
    problems.extend(
        f"{theme.slug}: unknown code {code}"
        for code in theme.codes
        if code not in known
    )
    return tuple(problems)


def validate_themes(themes: ThemeSet, dump: RuleDump) -> tuple[str, ...]:
    """Check the taxonomy against the dump; an empty tuple means valid."""
    problems = []
    known = {rule.code for rule in dump.rules}
    covered = set()
    slugs = set()
    for theme in themes.themes:
        if theme.slug in slugs:
            problems.append(f"duplicate slug: {theme.slug}")
        slugs.add(theme.slug)
        problems.extend(_validate_theme(theme, known))
        covered.update(theme.codes)
    dropped_codes = set()
    for code, _reason in themes.dropped:
        dropped_codes.add(code)
        if code not in known and code not in dump.removed:
            problems.append(f"dropped: unknown code {code}")
        if code in covered:
            problems.append(f"dropped code {code} also appears in a theme")
    problems.extend(
        f"code covered by no theme and not dropped: {code}"
        for code in sorted(known - covered - dropped_codes)
    )
    return tuple(problems)


def render_theme(theme: Theme, dump: RuleDump) -> str:
    """Render one `themes/<slug>.md` file; deterministic for a fixed dump."""
    by_code = {rule.code: rule for rule in dump.rules}
    rules = sorted(
        (by_code[code] for code in dict.fromkeys(theme.codes)),
        key=lambda rule: rule.code,
    )
    stable = sum(1 for rule in rules if rule.status is RuleStatus.STABLE)
    preview = len(rules) - stable
    lines = [
        (
            f"# Theme: {theme.title} "
            f"({len(rules)} rules: {stable} stable, {preview} preview)"
        ),
        "",
        f"- slug: {theme.slug}",
        f"- title: {theme.title}",
        f"- essence: {theme.essence}",
        f"- ruff: {dump.version}",
        f"- generated: {dump.fetched_at}",
        f"- codes: {', '.join(sorted(dict.fromkeys(theme.codes)))}",
        "",
    ]
    for rule in rules:
        lines.extend(_render_rule(rule, level=2))
    return "\n".join(lines).rstrip() + "\n"


def assemble(out_dir: Path, themes_path: Path) -> int:
    """Build `themes/*.md` from themes.json and the cache; never refetches."""
    cache = out_dir / "cache" / "rules.json"
    if not cache.exists():
        message = f"cache not found: {cache}; run the dump first"
        raise SystemExit(message)
    if not themes_path.exists():
        message = f"themes.json not found: {themes_path}"
        raise SystemExit(message)
    dump = fetch_rules(cache, refresh=False)
    theme_set = load_themes(themes_path)
    problems = validate_themes(theme_set, dump)
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)  # noqa: T201
        message = f"themes.json validation failed: {len(problems)} problem(s)"
        raise SystemExit(message)
    themes_dir = out_dir / "themes"
    outputs: dict[Path, str] = {}
    for theme in theme_set.themes:
        outputs[themes_dir / f"{theme.slug}.md"] = render_theme(theme, dump)
    themes_dir.mkdir(parents=True, exist_ok=True)
    for stale in set(themes_dir.glob("*.md")) - set(outputs):
        stale.unlink()
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")
    print(f"{len(theme_set.themes)} themes assembled:")  # noqa: T201
    for theme in theme_set.themes:
        print(f"  {len(theme.codes):>4}  {theme.slug}")  # noqa: T201
    print(f"dropped: {len(theme_set.dropped)}")  # noqa: T201
    return 0


def write_outputs(
    out_dir: Path,
    groups: tuple[Group, ...],
    dump: RuleDump,
    old: Manifest | None,
    updates: Updates,
) -> None:
    """Build every output in memory first, then write the whole set at once."""
    groups_dir = out_dir / "groups"
    outputs: dict[Path, str] = {}
    for group in groups:
        outputs[groups_dir / f"{group.slug}.md"] = render_group(group, dump)
    outputs[out_dir / "manifest.json"] = render_manifest(groups, dump)
    if updates.affected_groups:
        outputs[out_dir / "_UPDATES.md"] = render_updates(updates, old, dump)
    groups_dir.mkdir(parents=True, exist_ok=True)
    expected = {path for path in outputs if path.parent == groups_dir}
    for stale in set(groups_dir.glob("*.md")) - expected:
        stale.unlink()
    for path, content in outputs.items():
        path.write_text(content, encoding="utf-8")


def _print_summary(dump: RuleDump, groups: tuple[Group, ...], updates: Updates) -> None:
    # stdout IS the CLI contract here: the summary is the program's output.
    stable = sum(1 for rule in dump.rules if rule.status is RuleStatus.STABLE)
    preview = len(dump.rules) - stable
    print(  # noqa: T201
        f"ruff {dump.version}: {len(dump.rules)} rules "
        f"({stable} stable, {preview} preview), {len(dump.removed)} removed",
    )
    print(f"{len(groups)} group files:")  # noqa: T201
    for group in groups:
        print(f"  {len(group.rules):>4}  {group.slug}")  # noqa: T201
    print(  # noqa: T201
        f"updates: +{len(updates.added)} -{len(updates.removed)}"
        f" ~{len(updates.changed)} >{len(updates.moved)}"
        f" | affected groups: {len(updates.affected_groups)}",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the dump pipeline, or `--assemble` the theme inputs."""
    args = _parse_args(argv)
    out_dir: Path = args.out_dir
    if args.assemble:
        themes_path = args.themes or out_dir / "themes.json"
        return assemble(out_dir, themes_path)
    dump = fetch_rules(out_dir / "cache" / "rules.json", refresh=args.refresh)
    groups = group_rules(dump.rules)
    old = load_manifest(out_dir / "manifest.json")
    updates = diff_manifest(old, groups, dump.removed)
    write_outputs(out_dir, groups, dump, old, updates)
    _print_summary(dump, groups, updates)
    return 0


if __name__ == "__main__":
    sys.exit(main())
