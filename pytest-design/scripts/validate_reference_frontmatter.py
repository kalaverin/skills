"""Conformance checker for pytest-design reference frontmatter (index-card catalog)."""

import re
import sys
from pathlib import Path

import yaml

EXPECTED_CARD_KEYS = {"anchor", "what", "problem", "use_when", "avoid_when", "expected"}
ALLOWED_TOP_KEYS = {"subject", "index", "libraries"}


def words(text: str) -> list[str]:
    """Whitespace tokens containing at least 3 ASCII letters."""
    return [t for t in text.split() if len(re.findall(r"[A-Za-z]", t)) >= 3]


def strip_code(text: str) -> str:
    return re.sub(r"`[^`]*`", "", text)


def main() -> int:
    path = Path(sys.argv[1])
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

    top = set(fm.keys())
    if not top <= ALLOWED_TOP_KEYS:
        errors.append(f"top-level keys {top} not subset of {ALLOWED_TOP_KEYS}")

    subject = fm.get("subject", "")
    cards = fm.get("index", []) or []
    libraries = [str(lib).lower() for lib in (fm.get("libraries") or [])]
    banned_cloud_libs = set(libraries) | {"pytest", "faker"}

    subj_n = len(words(subject))
    if not 30 <= subj_n <= 50:
        errors.append(f"subject word count {subj_n} outside 30-50")
    for m in re.finditer(r"\b(a|the)\b", strip_code(subject), re.IGNORECASE):
        errors.append(f"subject: article '{m.group(0)}'")

    refs = re.findall(r"^\[ref: #([A-Za-z0-9-]+)\]\s*$", body, re.M)

    problem_counts: list[int] = []
    for i, card in enumerate(cards):
        keys = set(card.keys())
        if keys != EXPECTED_CARD_KEYS:
            errors.append(f"card {i}: keys {sorted(keys)} != {sorted(EXPECTED_CARD_KEYS)}")
            continue
        anchor = card["anchor"]
        if refs.count(anchor) != 1:
            errors.append(f"card {i}: anchor '{anchor}' has {refs.count(anchor)} body refs (need 1)")

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
        phrases = [p.strip().lower().strip("`") for p in cloud_str.split(",") if p.strip()]
        if len(phrases) != len(set(phrases)):
            errors.append(f"card {i} ({anchor}): duplicate phrases inside cloud")
        for ph in phrases:
            for lib in banned_cloud_libs:
                if lib in ph:
                    errors.append(f"card {i} ({anchor}): library name '{lib}' in cloud phrase '{ph}'")
            if " " in ph:
                for field in ("what", "use_when", "avoid_when", "expected"):
                    if ph in card[field].lower():
                        errors.append(f"card {i} ({anchor}): cloud phrase '{ph}' leaks into {field}")

        if re.match(r"^(load when|use when)", card["use_when"].strip().lower()):
            errors.append(f"card {i} ({anchor}): use_when opens with banned lead-in")
        if re.match(r"^(do not|don't|never)", card["avoid_when"].strip().lower()):
            errors.append(f"card {i} ({anchor}): avoid_when opens with banned lead-in")

    card_anchors = {c["anchor"] for c in cards if isinstance(c, dict) and "anchor" in c}
    for ref in set(refs):
        if ref not in card_anchors:
            errors.append(f"body ref '{ref}' has no declaring card")

    print(f"{path.name}: {len(cards)} cards, subject {subj_n}w, problems {problem_counts}")
    print_report(errors)
    return 1 if errors else 0


def print_report(errors: list[str]) -> None:
    if errors:
        print("FAIL")
        for err in errors:
            print(" -", err)
    else:
        print("PASS")


if __name__ == "__main__":
    sys.exit(main())
