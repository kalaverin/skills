---
name: pytest-design
description: MANDATORY skill for writing, editing, running, and reviewing Python unit tests, integration tests, and pytest suites. Use when the user asks for pytest, unit tests, integration tests, test fixtures, conftest files, parametrization, mocking, markers, test isolation, faker in tests, async tests, pytest plugins, pytest configuration, coverage, xdist, or any Python testing task. Apply only to Python projects.
triggers:
  all:
    files: "fd -e py -e pyi --max-results 1 | wc -l | grep -q 1"
    request: "pytest, unit test, integration test, test fixture, conftest, parametrization, mocking, markers, test isolation, faker in tests, async test, pytest plugin, pytest configuration, coverage, xdist, python test, python tests, тест, тесты, юнит-тест, интеграционный тест, фикстура, параметризация, мок, маркер, покрытие тестами"
requires:
  - frontmatter-protocol
  - python-lang
---

# SKILL: Pytest Engineering for Python Tests

This skill owns how the agent writes, edits, runs, and reviews Python test code with `pytest`.
It applies to unit tests, integration tests, fixtures, parametrization, markers, mocking, async tests, test configuration, and related tooling.

## 1. Mandatory Rules and Constraints

Every rule in this section carries the weight of MUST unless it explicitly uses SHOULD.
Violations of absolute constraints make the generated test suite unacceptable.

### 1.1 Absolute Constraints

1. **Python version**: Strictly Python 3.12+. Use `typing` features: `@override`, `TypedDict`, `Required`, `NotRequired`, `Unpack`. Use PEP 695 type parameter syntax (`type Alias = ...`, `def func[T](x: T) -> T`) freely. Do NOT use `TypeAliasType` directly — prefer PEP 695 `type` statement. The `type` statement desugars to `TypeAliasType` internally; only the explicit constructor is banned.
2. **No hardcoded values in test data**. EVER. All test data MUST be generated via `faker` with specific, semantically appropriate provider methods.
3. **`random` (stdlib) is FORBIDDEN in test code, fixtures, and factories.** The ONLY permitted use of `random` is inside the `fake` fixture for seed initialization: read `PYTEST_FAKER_SEED` from the environment; if it is unset, use `random.randint(0, 2**32)` to generate the seed. In ALL other contexts — `random.randint`, `random.choice`, `random.shuffle`, `random.sample`, and every other `random` function — are CRITICAL failures. Faker provides seeded, reproducible randomness; stdlib `random` does not.
4. **Every test function MUST be isolated**. No shared mutable state. No side effects leaking between tests.
5. **No `print()` statements in tests**. Use `capsys`, `capfd`, or `caplog` fixtures.
6. **No bare `except:` or `except Exception:`**. Explicit exception types only. Use `pytest.raises()` with `match` parameter.
7. **No `time.sleep()` or `asyncio.sleep()` in tests**. For sync code, use `time-machine` (or `freezegun` as legacy fallback). For async code, mock the clock at application level. Use `pytest-timeout` for hanging test protection.
8. **No global state mutations without cleanup**. Every monkeypatch MUST be reverted. Every temp resource MUST be cleaned up.
9. **NEVER create a new fixture without first checking if an equivalent or overlapping fixture already exists** in the project's conftest hierarchy. Duplicate fixtures are a critical failure. If you lack filesystem access to verify, add a `# TODO: verify no duplicate fixture exists` comment.
10. **NEVER assume Faker API from memory**. Before using any Faker provider method, verify it exists in the current version's documentation. Faker API changes between versions.

### 1.2 Constant Usage Rule

**NO magic / unnamed constants in test or production code.**
Named module-level constants, enums, and configuration objects are expected and encouraged.
Before using any literal value inline, check for an existing application-level source: `Enum` / `StrEnum` / `IntEnum`, module-level constants, configuration objects, or any other application-level constant definition.
Magic literals (bare numbers, strings, ports, timeouts used directly in expressions) MUST be named and imported from application-level sources.
Hardcoding unnamed magic values is strictly forbidden.

### 1.3 Rule Severity Levels

**MUST (Absolute Requirement):** Violations are critical failures.
- Test isolation: no shared mutable state, no side effects leaking between tests.
- No hardcoded values in test data — use semantically specific Faker providers.
- No bare `except:` or `except Exception:` — explicit exception types only.
- No `print()` in tests — use `capsys`, `capfd`, or `caplog`.
- No `time.sleep()` or `asyncio.sleep()` — use time control libraries or application-level clock injection.
- Every monkeypatch MUST be reverted; every temp resource cleaned up.
- Never duplicate fixtures; never test private methods directly.
- Verify Faker API before using; verify fixture uniqueness before creating.

**SHOULD (Strong Recommendation):** Violations are warnings or tech-debt, not blockers.
- Coverage threshold (`fail_under=50`) — coverage is a side effect of quality tests, not the target.
- xdist `--dist=loadfile` — use only after proving full test isolation under parallel execution.
- CI-friendly CLI defaults such as `--tb=short`.

## 2. Pre-Flight Planning Check-List

For EVERY test file you generate, provide:

1. **Production code analysis**: Inspect `src/` (or `app/`) to understand public APIs, types, and dependencies before deciding what to test.
2. **Architecture plan** (before code): what components, what scopes, what factories, what fixtures from the existing hierarchy will be reused.
3. **Existing fixture audit**: List all relevant fixtures in the conftest hierarchy that will be reused or extended.
4. **Fixture dependency graph**: Which fixtures depend on which, with scope and location.
5. **The code**: Following all rules above.
6. **Self-check questions** (answer before finalizing):
   - Am I testing the RIGHT things (invariants) or just chasing coverage?
   - Did I verify each Faker method against current documentation?
   - Are all test data randomized via faker with specific, semantically appropriate methods?
   - Is every test isolated with no shared mutable state?
   - Did I check for existing fixtures before creating new ones?
   - Are all fixtures at correct scope and placed in the correct conftest?
   - Does file path reflect component + scope + type?
   - Are all asserts focused on single logical concept?
   - Is faker uniqueness strategy appropriate for the suite size (function-scoped for unique, session-scoped for random)?
   - Are async tests properly marked?
   - Are private methods tested only through public API?
   - Are emails always generated by Faker.fake_email()?

Continuous reminders:
- **Before writing ANY fixture**: Scan existing conftest files. A duplicate fixture is a critical failure.
- **Before using ANY Faker method**: Verify it exists in the current Faker version's API. An incorrect Faker method call is a critical failure.
- **Before mocking**: Consider whether a Fake implementation would be more maintainable.
- **Before creating a test file**: Know where it lives in the hierarchy, what conftest files feed it, and what fixtures it inherits.

## 3. Lazy-Load Protocol for Reference Files

Do not read every file under `pytest-design/references/`.
After this skill triggers, the agent MUST batch-extract the YAML frontmatter of every reference file in a single shell command, evaluate the index cards, and load only the matching anchor sections.

### 3.1 Frontmatter Routing (Two Commands)

Run the canonical two-command funnel from `frontmatter-protocol` `[ref: #lazy-load-routing]` from the `pytest-design/` skill directory. Command 1 prints the complete routing map: every reference file with its `subject`, one line per file (28 lines — the agent sees every file at a glance).
Use the `subject` and the request plus the inferred session context (Section 3.2) to shortlist the candidate files.

Command 2 prints the full YAML frontmatter of ONLY the shortlisted files — the §6 Form 1 primitive, per `frontmatter-protocol` `[ref: #lazy-load-routing]` (the exact command lives there, never restated here).
Replace `<FILE-1> <FILE-2> ... <FILE-n>` in the canonical form with the shortlisted file paths.

The output prints each chosen file path followed by its YAML frontmatter block.
Reading only the shortlisted files keeps the agent well under the single-read limit while exposing every card of those files.

#### 3.1.1 Routing stays in the main agent

All card evaluation happens in the main agent; do not delegate it to subagents, because the inferred session context (Section 3.2) cannot be serialized to a subagent without losing detail.
Shortlist generously from Command 1: when a file might be relevant, add it to the file list rather than risk missing a recipe.
If the shortlist is too small or uncertain, expand the file list (up to every file in a group) and re-run Command 2; per-file frontmatter is small, so reading more files stays safe.

The agent MUST parse the frontmatter fields per the lazyload standard — top-level fields (`subject`, `index`, `libraries`) per `[ref: #lazyload-frontmatter-schema]`, the six card keys and their semantics (including convergence: several cards MAY share one anchor) per `[ref: #lazyload-cards]`, and card field style per `[ref: #lazyload-problem-style]` and `[ref: #lazyload-dedup]`. The agent reads the cards to decide WHICH anchors apply, then loads the HOW from the referenced `[ref: #<anchor>]` sections. Any inline `**Selection criteria / anti-patterns:**` blocks in a reference body MUST NOT exist: that content lives in the cards. Selection among recipes is entirely a frontmatter function: a reference body is pure HOW for an already-selected recipe and MAY contain that recipe's own content tables, but MUST NOT contain a cross-recipe decision/routing table.

### 3.2 Index Card Evaluation

Routing is semantic, not keyword-based. The matching input is NOT the literal user request alone — it is the request PLUS the work context the agent infers for this session: the tests it is about to write or edit, and the questions that may arise from the problem under investigation. The agent anticipates needs instead of reacting only to the user's phrasing. For each reference file:

1. Use `subject` to decide whether the file is relevant to the request AND the inferred session context; skip irrelevant files.
2. Within each relevant file, read every `index` card and match that combined context (request + inferred session work) against the card's `what`, `use_when`, and `avoid_when` (semantic match, not substring). Load anchors a competent test author would need for the upcoming work even when the user did not name them.
3. Mark the `anchor` of every matching card for loading. Deduplicate anchors: when several cards share the same `anchor`, load that anchor body once.
4. Evaluate all cards independently — a match on any card marks its anchor (OR semantics within and across files).

Do not rely on training data or file names to decide which sections to read.
The `index` cards are the authoritative routing index, read from the Command 2 output for the shortlisted files.

### 3.3 Anchor Section Extraction

For each marked anchor, extract the section that begins with `[ref: #<anchor>]` from the file that declared it.
Stop reading when you reach the next `[ref: #...]` marker or the end of the relevant subsection.

Example:

Extract per the canonical loader mechanics in `frontmatter-protocol` `[ref: #lazy-load-routing]` (bounded extraction — never a blind `rg -A N` window; the exact command lives there, not here). Extraction stops automatically at the next `[ref: #...]` marker or end of file.

## 4. Master Execution Workflow

1. **Load dependencies.** Confirm `python-lang` are active.
2. **Run the pre-flight check-list.** Follow Section 2 before writing any code.
3. **Route references.** Run the two frontmatter commands from Section 3.1 (the subject map, then the shortlisted files).
4. **Evaluate index cards.** Match each card's `what`/`use_when`/`avoid_when` against the user request AND the session work context the agent infers (the tests it is about to write or edit, the questions that may arise from the problem under investigation) — not against the literal request alone. Collect every matching `anchor` (deduplicated).
5. **Load anchors.** Extract and read only the marked `[ref: #...]` sections.
6. **Analyze project context.** Inspect the target Python project, existing test tree, and `conftest.py` hierarchy before writing tests.
7. **Generate or edit tests.** Follow the rules from Section 1 and the loaded reference sections.
8. **Run mandatory lint and verification.** Follow Section 5 while writing tests and again after finishing or fixing them.
9. **Verify scope.** Confirm the diff touches only intended test files and production code required by the test design.

## 5. Mandatory Lint and Verification Protocol

Run this protocol continuously while writing tests and again after the test files are complete or repaired.
Do not treat a linter warning as optional: read it, understand it, and fix it if it touches code the agent wrote or changed.
If a warning points to unmodified code, ignore it.

### 5.1 Discover Target Python Version

Determine the project's target Python version before linting by executing:

```bash
uv run python -c "import sys; print(f'py{sys.version_info.major}{sys.version_info.minor}')"
```

Use this exact value for `<PYVER>` in the subsequent steps.

### 5.2 Read Linter Suggestions

Run the following command targeting **ONLY the files you modified**:

```bash
uvx ruff check --select ALL --ignore D,CPY,DOC,ARG001,ARG002,ASYNC109,COM812,EM101,ERA001,FBT001,FBT002,FIX001,FIX002,PLR0912,PLR0913,S101,S105,TC002,TC003,TD001,TD002,TD003,TD004,TD005,TRY003 --target-version <PYVER> --output-format concise <changed_files>
```

Read every suggestion carefully. Apply fixes ONLY to the code you altered.

### 5.3 Verify Diff Scope

After applying fixes, verify the diff touches **ONLY changed code**:

```bash
uvx ruff check --select ALL --ignore D,CPY,DOC,ARG001,ARG002,ASYNC109,COM812,EM101,ERA001,FBT001,FBT002,FIX001,FIX002,PLR0912,PLR0913,S101,S105,TC002,TC003,TD001,TD002,TD003,TD004,TD005,TRY003 --target-version <PYVER> --diff <changed_files>
```

### 5.4 Rule Lookup

If you are uncertain about any rule code generated by the linter, use:

```bash
uvx ruff rule <RULE_CODE>
```

Example: `uvx ruff rule E501`.

## 6. Do Not

- Do not read entire reference files; use the batch frontmatter extraction and anchor extraction only.
- Do not apply this skill to non-Python test frameworks.
- Do not invent fixture or Faker APIs without verifying them against the project or current documentation.
- Do not generate tests that violate the absolute constraints in Section 1.

## 7. Practical Notes

- **Adapting `assets/faker.py`:** If you copy `assets/faker.py` into the target project, expect to adapt the code slightly. The file is a reusable template, not a drop-in module. Package prefixes, import paths, or project-specific seed configuration may need tuning. Do not treat an import error as a blocker — fix the local integration and move on.
- **Handling import errors from reference recipes:** When applying patterns from the `references/` files, the agent MAY encounter `ImportError`, `ModuleNotFoundError`, or similar runtime failures. This is expected. Each reference file lists the relevant `libraries` in its YAML frontmatter. Use that list to identify and install the missing package, or swap the import for an equivalent the project already uses. Do not abandon the recipe because the first import failed.
