---
subject: "Personal rules extending and overriding Google style for this project's Python code; mypy type narrowing traps, enum-class membership, member-tuple pattern, checker limitations, literal unions, typing gotchas, refactor hazards, silent regressions, narrowing preservation, equality chains."
index:
  - anchor: py-pr-enum-membership-narrowing
    what: "The mypy narrowing trap of enum-class membership tests (`x in SomeEnum`) and the member-tuple pattern that preserves narrowing."
    problem: "Agent refactors literal tuple membership into enum-class membership check; type checker silently stops narrowing, downstream branches break or sprout ignores; narrowing loss, silent regression, refactor trap, literal unions, enum pitfall, false confidence."
    use_when: "Refactoring membership tests to enums; reviewing enum-based conditionals; mypy errors downstream of an enum-class membership check."
    avoid_when: "Runtime enum semantics or style questions with no narrowing at stake; code without a type checker — the trap is static-analysis-only."
    expected: "Enum membership checks never silently drop narrowing; the member-tuple pattern is used wherever narrowing matters."
libraries:
  - mypy
---

# Personal Rules (Python)

Project-specific rules that extend or override the Google-style corpora (`01_language_rules.md`, `02_style_rules.md`). Review-focused rules live verbatim in `discuss-first/references/existence_review.md` and win on conflict; this file accumulates personal typing and language practice. On conflict with the Google corpora, this file wins.

## Enum-class membership breaks mypy narrowing
[ref: #py-pr-enum-membership-narrowing]

Refactoring a literal membership test into enum-class membership silently drops mypy type narrowing (mypy issue #13684, open: the enum class is not treated as an iterable value set by the narrowing engine):

Bad — narrowing lost:

```python
if status in Status:  # Python 3.12+ syntax; mypy does NOT narrow `status` here
    handle_open(status)  # downstream sees the unnarrowed type
```

Good — narrowing preserved via a member tuple:

```python
OPEN_STATUSES = (Status.PENDING, Status.IN_PROGRESS)

if status in OPEN_STATUSES:  # narrows to Literal[Status.PENDING, Status.IN_PROGRESS]
    handle_open(status)
```

Rules:

- When replacing literal-tuple membership with enum membership, verify that no downstream code relied on the narrowed type.
- Prefer a named tuple of members (`ALLOWED = (SomeEnum.A, SomeEnum.B)`) — it keeps the clean `in` syntax AND the narrowing.
- An equality chain (`x == SomeEnum.A or x == SomeEnum.B`) also narrows; use it for one or two members.
