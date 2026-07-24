"""Standard-driven conformance checker for reference frontmatter (index-card catalog).

Canonical validator of `frontmatter-protocol`, currently implementing the
**lazyload** profile (`frontmatter-protocol/references/lazyload.md`,
Conformance section). History: copied from the hardened api-design checker
(2026-07-22, P4 hardening) and generalized; moved from
`bootstrap/scripts/validate_reference_frontmatter.py` on 2026-07-23.

Target architecture (decision recorded 2026-07-23, project backlog): ONE
validator with `--expect-extension tracking|lazyload|include` profiles.
Current status: lazyload profile only; tracking and include profiles are
planned growth. Until `--expect-extension` lands, this script validates the
lazyload profile by default.

- Top-level keys are `{subject, index, libraries}` plus any skill-declared
  extras passed via `--allow-extra KEY` (repeatable).
- `--aips` enables the api-design AIP cross-check (frontmatter `aips` list vs
  `AIP-NNN` numbers in body section headings) and implies `--allow-extra aips`.
- `libraries` entries are banned from `problem` clouds (cloud discipline).

Deep dedup checks (per the lazyload standard's Dedup & Convergence section):
- Cloud leak check: every >=2-word normalized sub-gram of each cloud phrase is
  checked against all other card fields.
- Cross-field prose clone check: normalized >=3-word grams shared between any
  two of what/use_when/avoid_when/expected are flagged. 2-word grams are NOT
  checked mechanically (domain nouns dominate); they remain editorial.
- Cloud-vs-situation paraphrase check: a cloud phrase whose every content token
  prefix-matches a token of its own problem situation is flagged.
- Exemption: n-grams containing a backticked identifier token or a
  `(<file> › <topic>)` cross-reference pointer are exempt (identifier
  exemption; both are routing references, not prose).

Normalization: stopwords removed, `ies->y` and one trailing "s" stripped
(singular/plural equivalence per the standard), prefix matching (>=4 chars) for the
paraphrase check.

Usage:
    uv run --no-project --with pyyaml python validate_frontmatter.py \
        [--allow-extra KEY]... [--aips] <FILE.md | DIR>...

Accepts multiple files and/or directories (directories are scanned recursively for *.md).
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

EXPECTED_CARD_KEYS = {"anchor", "what", "problem", "use_when", "avoid_when", "expected"}
BASE_TOP_KEYS = {"subject", "index", "libraries"}

STOPWORDS = frozenset(
    "a an the of to in on for with without within across per vs and or not no nor "
    "is are was were be been being by at from into over under between through during "
    "before after like via than then when while where which who whom whose what that "
    "this these those it its".split()
)

CARD_TEXT_FIELDS = ("what", "use_when", "avoid_when", "expected")


def words(text: str) -> list[str]:
    """Whitespace tokens containing at least 3 ASCII letters."""
    return [t for t in text.split() if len(re.findall(r"[A-Za-z]", t)) >= 3]


def strip_code(text: str) -> str:
    return re.sub(r"`[^`]*`", "", text)


def body_without_fences(body: str) -> str:
    """Remove fenced code blocks so fake headings inside examples are ignored."""
    return re.sub(r"^```.*?^```", "", body, flags=re.M | re.S)


def field_tokens(text: str) -> list[tuple[str, bool]]:
    """Tokenize for dedup checks: (normalized token, is_exempt_reference).

    Exempt tokens: backticked identifiers and `(<file> › <topic>)` cross-reference
    pointers (lazyload identifier exemption; both are routing references, not
    prose).
    """
    spans: list[str] = []

    def _hold(m: re.Match[str]) -> str:
        spans.append(m.group(0))
        return f"\x00{len(spans) - 1}\x00"

    marked = re.sub(r"`[^`]*`", _hold, text)
    marked = re.sub(r"\([^)]*›[^)]*\)", _hold, marked)
    tokens: list[tuple[str, bool]] = []
    for raw in re.findall(r"[a-z0-9_-]+|\x00\d+\x00", marked.lower()):
        hold = re.fullmatch(r"\x00(\d+)\x00", raw)
        if hold:
            ident = spans[int(hold.group(1))].strip("`()").lower()
            tokens.extend((t, True) for t in re.findall(r"[a-z0-9-]+", ident))
            continue
        if raw in STOPWORDS:
            continue
        if len(raw) > 4 and raw.endswith("ies"):
            raw = raw[:-3] + "y"
        elif len(raw) > 3 and raw.endswith("s") and not raw.endswith("ss"):
            raw = raw[:-1]
        tokens.append((raw, False))
    return tokens


def ngrams(tokens: list[tuple[str, bool]], nmin: int, nmax: int) -> dict[str, bool]:
    """Map joined n-gram -> True if any token is an exempt reference."""
    out: dict[str, bool] = {}
    for n in range(nmin, nmax + 1):
        for i in range(len(tokens) - n + 1):
            gram = tokens[i : i + n]
            out[" ".join(t for t, _ in gram)] = any(idf for _, idf in gram)
    return out


def prefix_match(t1: str, t2: str) -> bool:
    """True for equal tokens or >=4-char prefix containment (guess/guesswork)."""
    if t1 == t2:
        return True
    if len(t1) >= 4 and len(t2) >= 4:
        return t1.startswith(t2) or t2.startswith(t1)
    return False


def check_deep_dedup(card: dict, i: int, anchor: str, errors: list[str]) -> None:
    """Deep checks: cloud sub-gram leaks, cross-field clones, situation paraphrase."""
    problem = card["problem"]
    if ";" not in problem:
        return
    situation, cloud = problem.rsplit(";", 1)
    field_grams = {f: ngrams(field_tokens(card[f]), 2, 4) for f in CARD_TEXT_FIELDS}
    cloud_phrases = [
        p.strip().rstrip(".").strip() for p in cloud.split(",") if p.strip()
    ]
    for phrase in cloud_phrases:
        for gram, idf in ngrams(field_tokens(phrase), 2, 4).items():
            if idf:
                continue
            for f in CARD_TEXT_FIELDS:
                if gram in field_grams[f] and not field_grams[f][gram]:
                    errors.append(
                        f"card {i} ({anchor}): cloud '{phrase}' sub-gram '{gram}' leaks into {f}"
                    )
    for pos, f1 in enumerate(CARD_TEXT_FIELDS):
        for f2 in CARD_TEXT_FIELDS[pos + 1 :]:
            for gram, idf in ngrams(field_tokens(card[f1]), 3, 4).items():
                if idf or len(gram.split()) < 3:
                    continue
                if gram in field_grams[f2] and not field_grams[f2][gram]:
                    errors.append(
                        f"card {i} ({anchor}): prose '{gram}' cloned {f1}<->{f2}"
                    )
    situation_tokens = [t for t, _ in field_tokens(situation)]
    for phrase in cloud_phrases:
        phrase_tokens = [t for t, _ in field_tokens(phrase)]
        if len(phrase_tokens) < 2:
            continue
        if all(
            any(prefix_match(pt, st) for st in situation_tokens) for pt in phrase_tokens
        ):
            errors.append(
                f"card {i} ({anchor}): cloud '{phrase}' paraphrases its own situation"
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+", type=Path, help="reference .md file(s) or directorie(s) to validate")
    parser.add_argument(
        "--allow-extra",
        action="append",
        default=[],
        metavar="KEY",
        help="skill-declared extra top-level frontmatter key (repeatable)",
    )
    parser.add_argument(
        "--aips",
        action="store_true",
        help="enable the api-design aips cross-check (implies --allow-extra aips)",
    )
    return parser.parse_args()


def validate_file(path: Path, allowed_top_keys: set, aips: bool) -> int:
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    errors: list[str] = []

    if lines[0].strip() != "---":
        errors.append("frontmatter does not open at line 1")
        print_report(errors)
        return 1
    close = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if close is None:
        errors.append("frontmatter closing --- not found")
        print_report(errors)
        return 1

    try:
        fm = yaml.safe_load("\n".join(lines[1:close]))
    except yaml.YAMLError as exc:
        errors.append(f"YAML invalid: {exc}")
        print_report(errors)
        return 1

    body = "\n".join(lines[close + 1 :])
    clean_body = body_without_fences(body)

    top = set(fm.keys())
    if not top <= allowed_top_keys:
        errors.append(f"top-level keys {top} not subset of {allowed_top_keys}")

    subject = fm.get("subject", "")
    cards = fm.get("index", []) or []
    libraries = [str(lib).lower() for lib in (fm.get("libraries") or [])]
    banned_cloud_libs = set(libraries)

    subj_n = len(words(subject))
    if not 30 <= subj_n <= 50:
        errors.append(f"subject word count {subj_n} outside 30-50")
    for m in re.finditer(r"\b(a|the)\b", strip_code(subject), re.IGNORECASE):
        errors.append(f"subject: article '{m.group(0)}'")

    if aips:
        # aips cross-check: frontmatter list vs AIP numbers in body headings.
        aips = fm.get("aips")
        if aips is None:
            errors.append("aips field missing (--aips mode requires it)")
            aips = []
        if not isinstance(aips, list) or not all(isinstance(x, int) for x in aips):
            errors.append(f"aips must be a flat list of integers, got: {aips!r}")
            aips = []
        heading_aips = {
            int(n) for n in re.findall(r"^#{2,3}\s.*\(AIP-(\d+)", clean_body, re.M)
        }
        if set(aips) != heading_aips:
            errors.append(
                f"aips mismatch: frontmatter {sorted(set(aips))} vs headings {sorted(heading_aips)}"
            )

    refs = re.findall(r"^\[ref: #([A-Za-z0-9-]+)\]\s*$", clean_body, re.M)

    problem_counts: list[int] = []
    for i, card in enumerate(cards):
        keys = set(card.keys())
        if keys != EXPECTED_CARD_KEYS:
            errors.append(
                f"card {i}: keys {sorted(keys)} != {sorted(EXPECTED_CARD_KEYS)}"
            )
            continue
        anchor = card["anchor"]
        if refs.count(anchor) != 1:
            errors.append(
                f"card {i}: anchor '{anchor}' has {refs.count(anchor)} body refs (need 1)"
            )

        problem = card["problem"]
        n = len(words(problem))
        problem_counts.append(n)
        if not 30 <= n <= 50:
            errors.append(f"card {i} ({anchor}): problem word count {n} outside 30-50")
        for m in re.finditer(r"\b(a|the)\b", strip_code(problem), re.IGNORECASE):
            errors.append(f"card {i} ({anchor}): article '{m.group(0)}' in problem")

        if ";" not in problem:
            errors.append(f"card {i} ({anchor}): no ';' cloud separator in problem")
            continue
        cloud_str = problem.rsplit(";", 1)[1]
        phrases = [
            p.strip().lower().strip("`") for p in cloud_str.split(",") if p.strip()
        ]
        if len(phrases) != len(set(phrases)):
            errors.append(f"card {i} ({anchor}): duplicate phrases inside cloud")
        for ph in phrases:
            for lib in banned_cloud_libs:
                if lib in ph:
                    errors.append(
                        f"card {i} ({anchor}): library name '{lib}' in cloud phrase '{ph}'"
                    )
            if " " in ph:
                for field in ("what", "use_when", "avoid_when", "expected"):
                    if ph in card[field].lower():
                        errors.append(
                            f"card {i} ({anchor}): cloud phrase '{ph}' leaks into {field}"
                        )

        if re.match(r"^(load when|use when)", card["use_when"].strip().lower()):
            errors.append(f"card {i} ({anchor}): use_when opens with banned lead-in")
        if re.match(r"^(do not|don't|never)", card["avoid_when"].strip().lower()):
            errors.append(f"card {i} ({anchor}): avoid_when opens with banned lead-in")

        check_deep_dedup(card, i, anchor, errors)

    card_anchors = {c["anchor"] for c in cards if isinstance(c, dict) and "anchor" in c}
    for ref in set(refs):
        if ref not in card_anchors:
            errors.append(f"body ref '{ref}' has no declaring card")

    print(
        f"{path.name}: {len(cards)} cards, subject {subj_n}w, problems {problem_counts}"
    )
    print_report(errors)
    return 1 if errors else 0


def main() -> int:
    args = parse_args()
    allowed_top_keys = BASE_TOP_KEYS | set(args.allow_extra)
    if args.aips:
        allowed_top_keys |= {"aips"}

    targets: list[Path] = []
    for p in args.files:
        if p.is_dir():
            targets.extend(sorted(p.rglob("*.md")))
        else:
            targets.append(p)

    rc = 0
    for t in targets:
        rc |= validate_file(t, allowed_top_keys, args.aips)
    return rc


def print_report(errors: list[str]) -> None:
    if errors:
        print("FAIL")
        for err in errors:
            print(" -", err)
    else:
        print("PASS")


if __name__ == "__main__":
    sys.exit(main())
