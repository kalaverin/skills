---
subject: "Baseline style for concise, high-quality tests: plain `assert`, module-level functions by default (classes only for class-scoped fixtures/tight grouping), exercise privates through public API, `pathlib.Path`, `faulthandler_timeout`, two-test rule for confirmed bugs, AAA dividers, one concept per test, `test_<unit>_<condition>_<expected>` naming, GWT docstrings, Faker data, exact invariants, fakes over mocks."
index:
  - anchor: testing-practices-plain-assert-only
    what: "pytest-style tests use plain `assert` statements rather than `unittest.TestCase` assertion methods."
    problem: "unittest assertion methods add boilerplate and reduce introspection quality in pytest tests, and failures show less detail than rewritten plain assertions; plain assert, no self assert, maximal introspection, no boilerplate, rewriter diff, even with mock."
    use_when: "The project writes pytest-style tests and needs maximal assertion introspection; `unittest.TestCase` assertion methods are currently used or likely to be introduced."
    avoid_when: "The test inherits from `unittest.TestCase` by design; the project standard requires `self.assert*` methods; pytest introspection is not available."
    expected: "All assertions are plain `assert`, giving detailed introspection with no `unittest` boilerplate."
  - anchor: testing-practices-test-functions-vs-test-classes
    what: "Default to plain test functions; use test classes only for class-scoped fixtures or tight grouping around a shared class-scoped resource."
    problem: "Classes used purely for organization add nesting without benefit, duplicate what files and directories already provide, and obscure which tests share one fixture; function default, class fixture, file grouping, no nesting, scope-bound resource, dedicated file."
    use_when: "A class-scoped fixture or shared class-scoped resource is needed; otherwise logical grouping should be handled by files and directories."
    avoid_when: "A class is used only to group related test names; module-level functions with clear file names suffice; no class-scoped resource exists."
    expected: "Classes appear only where a class-scoped fixture is required; logical grouping lives in files/directories."
  - anchor: testing-practices-private-method-policy
    what: "Never call `_private`/`__dunder` methods directly in tests; exercise them only through the public API, and refactor untestable privates into public units."
    problem: "Testing privates couples tests to implementation details, hides design smells, forces rewrites when internals change, and makes suites brittle during refactoring; public entry, refactor to public, no private call, encapsulation, design smell, extract unit."
    use_when: "A private method is reachable only through public API; tests should verify behavior, not implementation; a private method feels untestable and needs extraction."
    avoid_when: "A test calls `_private` or `__dunder` directly; reaching the behavior requires weakening encapsulation rather than refactoring."
    expected: "All private behavior is verified through public APIs; untestable privates are extracted into public, separately tested units."
  - anchor: testing-practices-doctests-policy
    what: "Write doctests only when the project already runs `pytest --doctest-modules` in CI; otherwise write plain unit tests."
    problem: "Doctests without project infrastructure go unrun and silently rot, while plain unit tests support fixtures, parametrization, and rich assertions; ci runs doctest, plain unit otherwise, fixtures parametrize, no unrun doctest, infrastructure gate, rich assert."
    use_when: "The project already runs `pytest --doctest-modules` in CI and wants usage examples in docstrings; otherwise plain unit tests are needed."
    avoid_when: "Doctests are introduced where CI does not run them; fixture-dependent scenarios are placed in docstrings; edge cases belong in doctests."
    expected: "Doctests exist only where CI runs them; everything else is a plain unit test."
  - anchor: testing-practices-pathlib-vs-str
    what: "Prefer `pathlib.Path` everywhere and convert to `str` only at external boundaries (C extensions, CLIs that require strings)."
    problem: "Mixing Path and str without explicit conversion causes type errors and boundary ambiguity, letting paths break at system edges and complicating path manipulation; path end-to-end, convert at boundary, c extension string, no mix, explicit conversion, tmp_path."
    use_when: "The codebase handles filesystem paths; `pathlib.Path` is preferred; conversion to `str` should happen only at external boundaries."
    avoid_when: "Legacy code requires `str` paths everywhere; mixing `Path` and `str` without declared conversion is acceptable; `pathlib` is not available."
    expected: "Tests pass `Path` end-to-end and convert to `str` only at the documented external boundary."
  - anchor: testing-practices-dependency-marker-forbidden
    what: "Tests must not depend on each other; `@pytest.mark.dependency` is forbidden so every test is independently runnable and order-independent."
    problem: "Chained tests create hidden coupling where failures and order dependence mask real bugs, making bisection and parallel runs unreliable; no dependency marker, fresh fixtured state, order irrelevant, independent run, no previous test, hidden coupling."
    use_when: "Every test must be independently runnable; execution order must not matter; `@pytest.mark.dependency` is present or being considered."
    avoid_when: "Tests intentionally build on each other's state; order is guaranteed by the framework; `@pytest.mark.dependency` is required by project policy."
    expected: "Every test runs in isolation with clean fixtured state; execution order is irrelevant."
  - anchor: testing-practices-dependencies-policy
    what: "Do not add dependencies yourself; verify optional plugins via `uv pip freeze` and ask the user before referencing an uninstalled plugin, falling back to an alternative if refused."
    problem: "Importing uninstalled plugins or auto-installing in CI breaks reproducible builds, surprises other contributors, and makes generated code fail in real environments without explicit approval; verify freeze, ask user install, fallback if refused, no auto install, installed only, reproducible."
    use_when: "A generated test wants to use an optional plugin; the agent must check installed packages and ask before adding new dependencies."
    avoid_when: "The plugin is already in the project's dependency set; the user has explicitly approved its use; a fallback is unnecessary."
    expected: "Only installed/approved plugins are referenced; missing ones have user approval or a fallback, and CI never auto-installs."
  - anchor: testing-practices-production-incident-debugging
    what: "Enable `faulthandler_timeout` (and `PYTHONFAULTHANDLER=1`) for suites that hang or crash in CI to dump Python tracebacks."
    problem: "Remote hangs and segfaults fail silently and are not reproducible manually, leaving production incidents without diagnostic data and slowing on-call resolution; faulthandler, dump traceback, ci crash, diagnose incident, no silent fail, remote reproduce."
    use_when: "The suite hangs or crashes in remote CI; failures are not reproducible locally; tracebacks are needed for diagnosis."
    avoid_when: "Failures are deterministic and reproducible locally; the suite never hangs or crashes; adding timeout overhead is unacceptable."
    expected: "CI hangs/crashes emit Python tracebacks via faulthandler, making production incidents diagnosable."
  - anchor: testing-practices-bug-driven-testing
    what: "For every confirmed bug write two tests: an `xfail(strict=True)` correct-behavior test and a non-xfail bug-documentation sentinel that locks the current broken behavior."
    problem: "Single test encoding broken behavior hides bug and lets regressions ship silently while masking progress once fixed; two-test rule, strict xfail, bug sentinel, lock broken, fail on fix, remove pair together."
    use_when: "A confirmed bug must be documented; both current broken behavior and correct behavior must be represented; accidental fixes must surface loudly."
    avoid_when: "Only one test exists for the bug; the bug is in a third-party dependency without an upstream link; the xfail marker is omitted."
    expected: "Each confirmed bug has a strict-xfail correct-behavior test plus a documented sentinel that fails loudly when the bug is fixed."
  - anchor: testing-practices-aaa-pattern
    what: "Every test is structured with explicit `# --- Arrange ---`, `# --- Act ---`, `# --- Assert ---` dividers; a single operation, one logical concept."
    problem: "Collapsing setup, operation, and verification into dense block hides what is being tested and makes failures harder to locate; arrange act assert, three phases, visual divider, gwt docstring, single step, no dense block."
    use_when: "Tests need explicit visual structure; setup/act/assert phases must be separated; one logical action per test is required."
    avoid_when: "Dense blocks are acceptable; multiple actions are tested together; GWT syntax is mixed inside the function body."
    expected: "Every test shows three clearly separated phases whose docstring (GWT) and body (AAA) describe the same scenario."
  - anchor: testing-practices-one-logical-concept-per-test
    what: "Limit each test to a single behavior or state transition; multiple asserts are allowed only for different aspects of the same object state."
    problem: "Bundling unrelated responsibilities produces confusing failures and hidden regressions, forcing reviewers to guess which behavior broke and complicating debugging; single concept, aspects of same state, split unrelated, parametrize, one behavior, failure points one."
    use_when: "A test covers multiple independent behaviors; failures should point to one concept; related state aspects may be asserted together."
    avoid_when: "Unrelated responsibilities are bundled; multiple concepts are tested together; parametrization could split them."
    expected: "Each test verifies exactly one concept; failures point to a single behavior."
  - anchor: testing-practices-naming-convention
    what: "Name tests `test_<unit_under_test>_<condition_or_state>_<expected_result>` so intent is readable without opening the body."
    problem: "Vague names like test_ok or test_case_1 hide unit, condition, and expected result, forcing readers to open every body to understand intent; unit condition expected, readable name, no vague, intent from name, helper names too, no test_ok."
    use_when: "Test names must encode unit, condition, and expected result; names like `test_ok` are present or being introduced; fixtures and helpers also need semantic names."
    avoid_when: "Names are generated by convention outside the test author; the project uses numeric IDs; readability from name is not valued."
    expected: "Test, fixture, and helper names all encode unit + condition + expected result."
  - anchor: testing-practices-bdd-style-docstrings
    what: "Every test has a Given-When-Then docstring expressing business intent, paired with an Arrange-Act-Assert body describing the same scenario."
    problem: "Missing or mismatched docstrings decouple business intent from technical execution, making tests hard to review, maintain, and onboard; given when then, bdd intent, matches aaa body, derive fixtures given, no mismatch, no gwt in body."
    use_when: "Tests need business-facing intent in docstrings; GWT must align with AAA body; fixtures and data should derive from the Given clause."
    avoid_when: "Docstrings are absent or contradict the body; GWT syntax appears inside the function body; business-facing intent is not needed."
    expected: "Every test's GWT docstring matches its AAA body and derives fixtures/data from the Given clause."
  - anchor: testing-practices-test-isolation
    what: "Tests are independent with no shared mutable state; use fixtures with correct scopes (function for mutable, wider only for immutable/expensive read-only) and prove independence with `-n auto`."
    problem: "Shared mutable state makes order matter and produces parallelism-only failures, masking real bugs until CI runs under xdist and frustrating debugging; independent data, function mutable, wider immutable, xdist prove, no leaked state, any order."
    use_when: "Tests fail only under parallel execution or change behavior when reordered; mutable state must be isolated per function; wider scopes are needed for immutable resources."
    avoid_when: "Tests intentionally share mutable state; fixture scopes are chosen without considering mutability; parallel runs are not required."
    expected: "Every test passes under `pytest-xdist -n auto` with no leaked mutable state."
  - anchor: testing-practices-public-api-only
    what: "Import and exercise only public API; treat `_`/`__` methods as implementation details exercised through public methods."
    problem: "Reaching into private state couples tests to internals that may change without warning, increasing maintenance cost and discouraging refactoring; exported surface, private detail, seam hook, hard case factory, no private target, stable surface."
    use_when: "Tests should reference only public API; boundary cases are hard to reach and need a new public seam; private methods are treated as implementation details."
    avoid_when: "Tests import or call `_`/`__` methods directly; a public seam is possible but ignored; stability of internal API is assumed."
    expected: "Tests reference only public APIs; hard-to-reach cases get a new public helper rather than private access."
  - anchor: testing-practices-common-test-smells-and-anti-patterns
    what: "Avoid hardcoded data, magic numbers, broad assertions, over-mocking, multiple concepts per test, and time-dependent assertions."
    problem: "Each smell drifts tests toward fragility or low value, hiding intent, letting tests pass for wrong reasons, and producing flakes in CI; generated data, named constants, precise invariant, controlled time, one concept, real fake collaborator."
    use_when: "A review checklist is needed to catch hardcoded literals, magic numbers, broad assertions, over-mocking, multiple concepts, or time-dependent assertions."
    avoid_when: "Smells are accepted as style; no checklist exists; reviewers ignore these patterns."
    expected: "Tests avoid hardcoded data and magic numbers, assert exact invariants, use real or fake collaborators, stay focused on one behavior each, and control time."
  - anchor: testing-practices-mocking-and-fakes
    what: "Prefer real objects or fakes for internal logic; reserve `unittest.mock`/`pytest-mock` for external boundaries (HTTP, DBs, third-party SDKs) that are expensive or non-deterministic."
    problem: "Mocking internal collaborators tests implementation rather than behavior, letting refactorings break tests that should still pass; real or fake internal, mock external boundary, http db sdk, deterministic fake, behavior not impl, boundary only."
    use_when: "Internal collaborators are deterministic and can be real or faked; mocks should be reserved for external boundaries such as HTTP, databases, or third-party SDKs."
    avoid_when: "Internal logic is mocked; real objects are too expensive or nondeterministic but not faked; mocks leak into every layer."
    expected: "Internal collaborators are real objects or reusable fakes; mocks appear only at external boundaries."
  - anchor: testing-practices-assertion-introspection
    what: "Writing assertions that pytest's rewriter can explain: compare values directly with `assert expr`, avoid `assert expr is True`/`== True`, and avoid assert messages that hide the generated diff."
    problem: "Noisy predicates and hand-written messages defeat assertion introspection, make failures harder to read, and hide actual values behind custom text during debugging; compare directly, no is true, no assert message, showlocals, operands shown, rewritten diff."
    use_when: "Failures are hard to read because of `is True`, `== True`, or custom assert messages; pytest's rewritten diff should show operands."
    avoid_when: "The project disables assertion rewriting; custom messages are required by policy; operands are intentionally hidden."
    expected: "Failures show the compared operands through rewriting, with no redundant `is True`/`== True` noise and no hand-written assert messages."
  - anchor: testing-practices-fixtures-over-setup-teardown
    what: "Preferring pytest fixtures over xUnit `setup_method`/`teardown_method` (and `setUp`/`tearDown`) for arranging state, because fixtures compose by dependency injection and scope."
    problem: "setup_method hides where shared state comes from, runs implicitly per method, cannot reuse across classes without inheritance, and makes test dependencies invisible; fixture function, declared scope, inject dependency, no xunit setup, no class attr mutable, compose."
    use_when: "Tests currently use `setup_method`/`teardown_method` or `setUp`/`tearDown`; shared state should be explicit and composable via dependency injection."
    avoid_when: "xUnit setup is mandated by framework; fixtures are not available; class attributes are the intended sharing mechanism."
    expected: "All arrangement flows through fixtures with explicit scopes; no implicit xUnit setup/teardown remains."
  - anchor: testing-practices-no-test-branching
    what: "Forbidding `if`/`for` constructs that change which assertions run inside a test; moving outcome variation into `pytest.mark.parametrize` so each case is a single straight-line assertion."
    problem: "Branching inside test lets one case pass while another silently fails, hides which path produced failure, and complicates coverage reporting; single path, parametrize outcomes, loop only arrange, no if assert, no loop assert, one path."
    use_when: "Outcome variation is currently expressed with `if`/`for` around assertions; each case should become a parametrized straight-line test."
    avoid_when: "Loops are only in the Arrange phase; branches configure setup but do not gate assertions; parametrization would explode the matrix."
    expected: "Each test is a straight line to one assertion; outcome differences live in the parametrization table, not in branches."
  - anchor: testing-practices-regression-pinning
    what: "After a bug is fixed and the xfail-plus-sentinel pair is removed, keeping a durable regression test that pins the corrected behavior across edge cases and references the issue ID in its name."
    problem: "Once temporary xfail and bug-documentation tests are deleted, nothing guards against bug returning in future refactor, allowing silent regressions; fixed bug guard, issue id name, edge coverage, remove stale xfail, pin corrected, guard return."
    use_when: "A bug has been fixed and its xfail-plus-sentinel pair removed; a durable regression test must guard against recurrence; edge cases and issue ID should be encoded in the name."
    avoid_when: "The bug's tests are deleted entirely after fixing; old `xfail`/sentinel markers are left in place; no edge cases are covered."
    expected: "Every fixed bug leaves a durable, clearly named regression test over edge cases, with obsolete xfail or sentinel removed."
---

# TESTING PRACTICES

## Plain assert only

[ref: #testing-practices-plain-assert-only]

pytest uses plain `assert`.
`unittest.TestCase` assertion methods such as `self.assertEqual`, `self.assertTrue`, and `self.assertRaises` are forbidden in pytest-style tests because they add boilerplate and reduce introspection quality.

```python
from faker import Faker

POSITIVE_MIN: int = 1
POSITIVE_MAX: int = 100


def test_plain_assert_is_the_pytest_idiom(fake: Faker) -> None:
    """
    Given: a generated positive integer.
    When: checking it is positive.
    Then: the assertion uses plain assert.
    """
    # --- Arrange ---
    value = fake.pyint(min_value=POSITIVE_MIN, max_value=POSITIVE_MAX)

    # --- Act ---
    is_positive = value > 0

    # --- Assert ---
    assert is_positive
```

**Variety booster:** Combine plain `assert` with `pytest.raises(match=...)` and custom helper functions that return `bool` for complex domain checks.

## Assertion introspection

[ref: #testing-practices-assertion-introspection]

Write comparisons so pytest's assertion rewriter can show both operands on failure.

Avoid `assert expr is True`, `assert value == True`, and `assert expr, "message"`; they hide the rewritten diff.

```python
from faker import Faker


POSITIVE_MIN: int = 1
POSITIVE_MAX: int = 100


def test_introspection_rewrites_plain_assert(fake: Faker) -> None:
    """
    Given: a generated positive integer.
    When: it is compared with a plain predicate.
    Then: pytest rewriting reports both operands on failure.
    """
    # --- Arrange ---
    value = fake.pyint(min_value=POSITIVE_MIN, max_value=POSITIVE_MAX)
    lower_bound = POSITIVE_MIN - 1

    # --- Act ---
    # Comparison is performed directly in the assertion.

    # --- Assert ---
    assert value > lower_bound
```

**Variety booster:** Reach for `pytest -l`/`--showlocals` when a failure needs local variables, instead of embedding a custom message in the assert.

## Test functions vs test classes

[ref: #testing-practices-test-functions-vs-test-classes]

Default to plain test functions.
Use test classes only when you need `@pytest.fixture(scope="class")` or a tight logical grouping of tests that share a class-scoped resource.
Never use test classes purely for organization — files and directories exist for that purpose.

```python
import pytest

SCHEMA_VERSION: str = "v2"


@pytest.fixture(scope="class")
def schema_version() -> str:
    return SCHEMA_VERSION


class TestSchemaValidation:
    """Group tests that depend on a single class-scoped schema version."""

    def test_schema_version_is_exposed_to_all_tests(self, schema_version: str) -> None:
        """
        Given: a class-scoped schema fixture.
        When: a test reads it.
        Then: it matches the expected version.
        """
        # --- Arrange ---
        observed = schema_version

        # --- Act ---
        # Reading the fixture value is the action under test.

        # --- Assert ---
        assert observed == SCHEMA_VERSION
```

**Variety booster:** When you only need logical grouping, keep tests as module-level functions and move the group into a dedicated file; reserve classes for fixtures that genuinely require class scope.

## Fixtures over setup/teardown

[ref: #testing-practices-fixtures-over-setup-teardown]

Prefer fixtures over `setup_method`/`teardown_method` and `setUp`/`tearDown`.

Fixtures compose through dependency injection and explicit scopes, while xUnit setup runs implicitly and hides sharing.

```python
import pytest
from faker import Faker


EXPECTED_ITEM_COUNT: int = 2


class InMemoryQueue:
    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        self._items.append(item)

    def size(self) -> int:
        return len(self._items)


@pytest.fixture
def seeded_queue(fake: Faker) -> InMemoryQueue:
    queue = InMemoryQueue()
    for _ in range(EXPECTED_ITEM_COUNT):
        queue.push(fake.word())
    return queue


def test_seeded_queue_starts_with_expected_size(seeded_queue: InMemoryQueue) -> None:
    """
    Given: a queue seeded by a fixture instead of setup_method.
    When: the size is read.
    Then: it equals the seeded count.
    """
    # --- Arrange ---
    # Seeding is performed by the seeded_queue fixture, not setup_method.

    # --- Act ---
    observed = seeded_queue.size()

    # --- Assert ---
    assert observed == EXPECTED_ITEM_COUNT
```

**Variety booster:** Pair a function-scoped seeding fixture with a class- or module-scoped immutable resource so expensive setup is shared while mutable state stays fresh per test.

## Private method policy

[ref: #testing-practices-private-method-policy]

Never test `_private` or `__dunder` methods directly.
Test them through the public API that exercises them.
If a private method feels "untestable" through public API, that is a design smell: extract it into a separate class or module with its own public API.

```python
from faker import Faker

PADDING_LENGTH: int = 2


class TagIndex:
    def __init__(self) -> None:
        self._tags: set[str] = set()

    def add(self, tag: str) -> bool:
        canonical = self._canonicalize(tag)
        if canonical in self._tags:
            return False
        self._tags.add(canonical)
        return True

    def _canonicalize(self, tag: str) -> str:
        return tag.strip().lower()


def test_add_detects_canonical_duplicates_through_public_api(fake: Faker) -> None:
    """
    Given: a tag stored with mixed case and whitespace.
    When: the same canonical tag is added again.
    Then: the operation reports a duplicate.
    """
    # --- Arrange ---
    raw_tag = fake.word()
    padding = " " * PADDING_LENGTH
    first_variant = f"{padding}{raw_tag.upper()}{padding}"
    second_variant = raw_tag.lower()
    index = TagIndex()

    # --- Act ---
    first_result = index.add(first_variant)
    second_result = index.add(second_variant)

    # --- Assert ---
    assert first_result is True
    assert second_result is False
```

**Variety booster:** Write a separate unit test for the extracted public helper once the private method is promoted to its own module.

## Doctests policy

[ref: #testing-practices-doctests-policy]

Write doctests only if the project already has an explicit doctest infrastructure (`pytest --doctest-modules` is configured in CI).
Otherwise, write plain unit tests.

```python
from faker import Faker

MIN_PARSE_VALUE: int = 1
MAX_PARSE_VALUE: int = 1000


def test_parse_positive_integer_accepts_valid_string(fake: Faker) -> None:
    """
    Given: a numeric string.
    When: parsing it.
    Then: the parsed integer equals the original value.
    """
    # --- Arrange ---
    value = fake.pyint(min_value=MIN_PARSE_VALUE, max_value=MAX_PARSE_VALUE)
    text = str(value)

    # --- Act ---
    parsed = int(text)

    # --- Assert ---
    assert parsed == value
```

**Variety booster:** Keep any doctests focused on usage examples; move edge cases, error handling, and fixture-dependent scenarios into dedicated test files.

## `pathlib.Path` vs `str`

[ref: #testing-practices-pathlib-vs-str]

Prefer `pathlib.Path` objects everywhere.
Use `str()` only at the system boundary, for example when passing to a C extension or an external CLI that requires strings.
Never mix `Path` and `str` in the same test without explicit conversion.

```python
from pathlib import Path

from faker import Faker

YAML_EXTENSION: str = "yaml"
CONFIG_KEY_SEPARATOR: str = ": "
LINE_TERMINATOR: str = "\n"
CONFIG_ENCODING: str = "utf-8"


class ConfigParser:
    def __init__(self, path: Path) -> None:
        self._path = path

    def parse(self) -> dict[str, str]:
        text = self._path.read_text(encoding=CONFIG_ENCODING)
        key, value = text.strip().split(CONFIG_KEY_SEPARATOR, maxsplit=1)
        return {key: value}


def test_config_file_is_parsed_from_path_object(tmp_path: Path, fake: Faker) -> None:
    """
    Given: a YAML config file created as a Path.
    When: the parser receives the Path.
    Then: it returns the configured value.
    """
    # --- Arrange ---
    config_file = tmp_path / f"{fake.word()}.{YAML_EXTENSION}"
    key = fake.word()
    value = fake.word()
    config_file.write_text(
        f"{key}{CONFIG_KEY_SEPARATOR}{value}{LINE_TERMINATOR}",
        encoding=CONFIG_ENCODING,
    )

    # --- Act ---
    parsed = ConfigParser(config_file).parse()

    # --- Assert ---
    assert parsed[key] == value
```

**Variety booster:** Use `tmp_path` fixtures with different directory depths and file extensions, and centralize path-to-string conversions in a single boundary helper.

## Dependency marker forbidden

[ref: #testing-practices-dependency-marker-forbidden]

Tests must not depend on each other.
Never use `@pytest.mark.dependency`.
Every test must be independently runnable and execution order must not matter.

```python
import pytest
from faker import Faker

ALLOWED_STATUSES: frozenset[str] = frozenset({"active", "pending", "archived"})


@pytest.fixture
def random_status(fake: Faker) -> str:
    return fake.random_element(elements=tuple(ALLOWED_STATUSES))


def test_status_belongs_to_allowed_set(random_status: str) -> None:
    """
    Given: a generated status.
    When: checking membership.
    Then: it belongs to the allowed set.
    """
    # --- Arrange ---
    observed = random_status

    # --- Act ---
    # Membership check is performed in the assertion.

    # --- Assert ---
    assert observed in ALLOWED_STATUSES
```

**Variety booster:** Run the suite with `pytest-randomly` or `pytest-random-order` to prove order independence once you have demonstrated full isolation.

**Plugin:** `pytest-randomly` (or `pytest-random-order`) randomizes test order to surface hidden order dependence; verify it is installed before relying on it.

## Dependencies policy

[ref: #testing-practices-dependencies-policy]

You must not add new dependencies to the project yourself.
Before using any pytest plugin or third-party library in generated tests, check `uv pip freeze`.
If the plugin is not installed, ask the user to install the required library, module, or plugin.
If the user refuses, use an alternative approach that does not require the missing plugin.

```bash
uv pip freeze | grep -E "^(pytest-asyncio|time-machine)="
```

**Variety booster:** Keep a project-specific allow-list of approved plugins in `pyproject.toml` under `[tool.pytest.ini_options] addopts` or a dedicated dependency group.

## Production incident debugging

[ref: #testing-practices-production-incident-debugging]

For tests that hang or segfault in CI, enable `faulthandler` to get traceback dumps.
This outputs Python tracebacks for crashes, which is critical for the "03:00 production incident" scenario.

```toml
[tool.pytest.ini_options]
faulthandler_timeout = 60
```

**Variety booster:** Set `PYTHONFAULTHANDLER=1` in CI environment variables for container-based runners and combine `faulthandler_timeout` with `pytest-timeout` for hard wall-clock limits.

**Plugin:** `pytest-timeout` enforces hard wall-clock limits that complement `faulthandler_timeout`; install it separately.

## Bug-driven testing

[ref: #testing-practices-bug-driven-testing]

Tests are production code.
When you encounter a bug or incorrect behavior in the application under test, you MUST NOT silently work around it or write the test to match the broken behavior.

**The two-test rule for every confirmed bug:**

1. **The "correct behavior" test** — Write the test exactly as the code SHOULD behave according to specs, requirements, or common sense.
Mark it with `@pytest.mark.xfail(strict=True)` and a clear reason linking to the bug (issue ID, ticket, or concise description).
Use `raises` if the expected correct behavior is an exception.

2. **The "bug documentation" test** — Write a separate test that documents and locks the CURRENT broken behavior with precise, narrow assertions.
This test MUST NOT use `xfail`; it passes today and acts as a sentinel.
If the bug is accidentally fixed, this test fails loudly, signaling that the xfail test above should be unmarked and this bug-documentation test should be removed.

**Rules:**

- The bug-documentation test MUST have a comment explicitly stating it documents a bug and should be removed after the fix.
- The xfail test MUST use `strict=True` so that when the bug is fixed, the test suite fails until the xfail marker is removed and the bug-documentation test is deleted.
- NEVER write a single test that asserts the broken behavior without an accompanying "correct behavior" xfail test.
NEVER rewrite the correct-behavior test to match the bug just to make CI green.
- If the bug is in a third-party dependency and cannot be fixed in this repo, the bug-documentation test MAY use `pytest.skip` with a link to the upstream issue, but the xfail test must still exist.

```python
import pytest
from faker import Faker

BUG_42_ID: str = "Bug #42"
BASE_PRICE_MIN: int = 100
BASE_PRICE_MAX: int = 1000
DISCOUNT_PERCENT_MIN: int = 1
DISCOUNT_PERCENT_MAX: int = 99
MIN_DISCOUNT_PERCENT: int = 0
PERCENT_BASE: int = 100
BROKEN_RETURN_VALUE: int = 0


class PriceCalculator:
    def apply_discount(self, base_price: int, discount_percent: int) -> int:
        if discount_percent < MIN_DISCOUNT_PERCENT:
            return BROKEN_RETURN_VALUE  # BUG #42: should raise ValueError
        return int(base_price * (PERCENT_BASE - discount_percent) / PERCENT_BASE)


@pytest.mark.xfail(
    strict=True,
    reason=f"{BUG_42_ID}: negative discount percent should raise ValueError instead of returning {BROKEN_RETURN_VALUE}",
)
def test_apply_discount_with_negative_percent_raises_value_error(fake: Faker) -> None:
    """
    Given: a valid base price and a negative discount percent.
    When: applying the discount.
    Then: raises ValueError.
    """
    # --- Arrange ---
    calculator = PriceCalculator()
    base_price = fake.pyint(min_value=BASE_PRICE_MIN, max_value=BASE_PRICE_MAX)
    discount_percent = -fake.pyint(min_value=DISCOUNT_PERCENT_MIN, max_value=DISCOUNT_PERCENT_MAX)

    # --- Act ---
    with pytest.raises(ValueError):
        calculator.apply_discount(base_price, discount_percent)

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.


def test_apply_discount_with_negative_percent_currently_returns_zero_documenting_bug_42(fake: Faker) -> None:
    """
    Given: a valid base price and a negative discount percent.
    When: applying the discount.
    Then: the current broken implementation returns zero.
    """
    # --- Arrange ---
    calculator = PriceCalculator()
    base_price = fake.pyint(min_value=BASE_PRICE_MIN, max_value=BASE_PRICE_MAX)
    discount_percent = -fake.pyint(min_value=DISCOUNT_PERCENT_MIN, max_value=DISCOUNT_PERCENT_MAX)

    # --- Act ---
    result = calculator.apply_discount(base_price, discount_percent)

    # --- Assert ---
    # DOCUMENTING BUG #42: remove this test once the bug is fixed and the xfail above is unmarked.
    assert result == BROKEN_RETURN_VALUE
```

**Variety booster:** After the fix, delete the bug-documentation test and remove the `xfail` marker; keep a regression test that verifies the fixed behavior across boundary values.

## Regression pinning after a fix

[ref: #testing-practices-regression-pinning]

Once the xfail-plus-sentinel pair is removed, keep a permanent regression test that pins the corrected behavior across boundary values.

Reference the issue ID in the test name so the guard survives future refactors.

```python
import pytest
from faker import Faker


BASE_PRICE_MIN: int = 100
BASE_PRICE_MAX: int = 1000
MIN_DISCOUNT_PERCENT: int = 0
PERCENT_BASE: int = 100


class PriceCalculator:
    def apply_discount(self, base_price: int, discount_percent: int) -> int:
        if discount_percent < MIN_DISCOUNT_PERCENT:
            raise ValueError(discount_percent)
        return int(base_price * (PERCENT_BASE - discount_percent) / PERCENT_BASE)


@pytest.mark.parametrize(
    "negative_percent",
    [
        pytest.param(-1, id="minus-one"),
        pytest.param(-PERCENT_BASE, id="minus-hundred"),
    ],
)
def test_apply_discount_with_negative_percent_raises_value_error_regression_bug_42(
    negative_percent: int,
    fake: Faker,
) -> None:
    """
    Given: a fixed discount calculator and a negative percent.
    When: applying the discount.
    Then: ValueError is raised, pinning the Bug #42 fix.
    """
    # --- Arrange ---
    calculator = PriceCalculator()
    base_price = fake.pyint(min_value=BASE_PRICE_MIN, max_value=BASE_PRICE_MAX)

    # --- Act ---
    with pytest.raises(ValueError):
        calculator.apply_discount(base_price, negative_percent)

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

**Variety booster:** Extend the boundary table with `0`, `PERCENT_BASE`, and `PERCENT_BASE + 1` so the regression test also pins the valid range edges of the fix.

## AAA pattern

[ref: #testing-practices-aaa-pattern]

Every test MUST follow Arrange-Act-Assert with explicit visual separation.

```python
# Template for every test:
# def test_<what>_<condition>_<expected>() -> None:
#     # --- Arrange ---
#     # setup all preconditions
#
#     # --- Act ---
#     # execute single action
#
#     # --- Assert ---
#     # verify single logical concept
```

One logical concept per test.
Multiple asserts are allowed ONLY when verifying different aspects of the SAME object state.
Use `pytest.fail()` with descriptive message for complex conditional failures.

**Synchronization rule:** The docstring uses **Given-When-Then** (BDD-style), while the test body uses **Arrange-Act-Assert** (structural).
They MUST describe the same scenario — the docstring explains the business intent, the body implements the technical execution.
Do not mix GWT syntax inside the function body.

```python
from faker import Faker

OPERAND_MIN: int = 1
OPERAND_MAX: int = 100


class Adder:
    def add(self, a: int, b: int) -> int:
        return a + b


def test_adder_returns_sum_of_operands(fake: Faker) -> None:
    """
    Given: two generated operands.
    When: the adder adds them.
    Then: the result equals the mathematical sum.
    """
    # --- Arrange ---
    left = fake.pyint(min_value=OPERAND_MIN, max_value=OPERAND_MAX)
    right = fake.pyint(min_value=OPERAND_MIN, max_value=OPERAND_MAX)
    adder = Adder()

    # --- Act ---
    result = adder.add(left, right)

    # --- Assert ---
    assert result == left + right
```

**Variety booster:** Use helper functions for repetitive arrange steps, but keep the three comment dividers so the AAA structure remains visible.

## One logical concept per test

[ref: #testing-practices-one-logical-concept-per-test]

One logical concept per test.
Multiple asserts are allowed only for different aspects of the same object state.

```python
from dataclasses import dataclass
from faker import Faker


@dataclass(frozen=True)
class Account:
    owner: str
    balance: int
    currency: str


BALANCE_MIN: int = 0
BALANCE_MAX: int = 10000


def test_account_creation_returns_populated_account(fake: Faker) -> None:
    """
    Given: owner, balance, and currency.
    When: an account is created.
    Then: all fields are stored correctly.
    """
    # --- Arrange ---
    owner = fake.name()
    balance = fake.pyint(min_value=BALANCE_MIN, max_value=BALANCE_MAX)
    currency = fake.currency_code()

    # --- Act ---
    account = Account(owner=owner, balance=balance, currency=currency)

    # --- Assert ---
    assert account.owner == owner
    assert account.balance == balance
    assert account.currency == currency
```

**Variety booster:** When a single entry point produces several independent outcomes, split them into parametrized tests that share a factory fixture.

## No branching inside tests

[ref: #testing-practices-no-test-branching]

Forbid `if`/`for` constructs that change which assertions run.

Drive outcome variation through `pytest.mark.parametrize` so every case is a straight line to one assertion.

```python
import pytest
from faker import Faker


MIN_TOKEN_LENGTH: int = 8


def is_valid_token(token: str) -> bool:
    return len(token) >= MIN_TOKEN_LENGTH


@pytest.mark.parametrize(
    ("token_length", "expected"),
    [
        pytest.param(MIN_TOKEN_LENGTH - 1, False, id="short-token"),
        pytest.param(MIN_TOKEN_LENGTH + 1, True, id="long-token"),
    ],
)
def test_token_validity_matches_length_threshold(
    token_length: int,
    expected: bool,
    fake: Faker,
) -> None:
    """
    Given: a token of a parametrized length.
    When: it is validated against the threshold.
    Then: the result matches the expected outcome.
    """
    # --- Arrange ---
    token = fake.lexify("?" * token_length)

    # --- Act ---
    result = is_valid_token(token)

    # --- Assert ---
    assert result is expected
```

**Variety booster:** Keep loops only in the Arrange phase (for example, seeding a store); the moment a loop or `if` would gate an assertion, promote the variation to a parametrization row.

## Naming convention

[ref: #testing-practices-naming-convention]

Use the strict naming convention:

```text
test_<unit_under_test>_<condition_or_state>_<expected_result>
```

Examples:

- `test_user_service_create_with_valid_data_returns_user_instance`
- `test_payment_gateway_charge_with_expired_card_raises_payment_error`
- `test_order_repository_get_by_id_with_nonexistent_id_returns_none`

```python
from faker import Faker

MIN_TOKEN_LENGTH: int = 8
SHORT_TOKEN_LENGTH: int = MIN_TOKEN_LENGTH - 1
LONG_TOKEN_LENGTH: int = MIN_TOKEN_LENGTH + 1


class TokenValidator:
    def validate(self, token: str) -> bool:
        return len(token) >= MIN_TOKEN_LENGTH


def test_token_validator_validate_with_short_token_returns_false(fake: Faker) -> None:
    """
    Given: a token shorter than the minimum length.
    When: validating it.
    Then: the validator returns False.
    """
    # --- Arrange ---
    token = fake.lexify("?" * SHORT_TOKEN_LENGTH)

    # --- Act ---
    result = TokenValidator().validate(token)

    # --- Assert ---
    assert result is False


def test_token_validator_validate_with_long_token_returns_true(fake: Faker) -> None:
    """
    Given: a token longer than the minimum length.
    When: validating it.
    Then: the validator returns True.
    """
    # --- Arrange ---
    token = fake.lexify("?" * LONG_TOKEN_LENGTH)

    # --- Act ---
    result = TokenValidator().validate(token)

    # --- Assert ---
    assert result is True
```

**Variety booster:** Use the same naming convention for fixtures and helper functions, for example `user_with_expired_card` or `order_repository_with_missing_order`.

## BDD-style docstrings

[ref: #testing-practices-bdd-style-docstrings]

Every test MUST have a Given-When-Then docstring.

```python
def test_user_create_with_duplicate_email_raises_conflict() -> None:
    """
    Given: a user already exists with email
    When: attempting to create another user with the same email
    Then: raises UserAlreadyExistsError with conflict details
    """
    ...
```

```python
import re

import pytest
from faker import Faker

class UserAlreadyExistsError(Exception):
    pass


class UserRepository:
    def __init__(self) -> None:
        self._users: set[str] = set()

    def create(self, email: str) -> None:
        if email in self._users:
            raise UserAlreadyExistsError(email)
        self._users.add(email)


def test_user_create_with_duplicate_email_raises_conflict(fake: Faker) -> None:
    """
    Given: a user already exists with email.
    When: attempting to create another user with the same email.
    Then: raises UserAlreadyExistsError with conflict details.
    """
    # --- Arrange ---
    email = fake.fake_email()
    repository = UserRepository()
    repository.create(email)

    # --- Act ---
    with pytest.raises(UserAlreadyExistsError, match=re.escape(email)):
        repository.create(email)

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

**Variety booster:** Keep docstrings focused on the business scenario; derive the exact fixture names and data generation from the Given clause.

## Test isolation

[ref: #testing-practices-test-isolation]

Tests must be independent.
There must be no shared mutable state and execution order must not matter.
Use fixtures with correct scopes to manage setup/teardown and fresh state.

```python
import pytest
from faker import Faker

ITEMS_PER_TEST: int = 3


class InMemoryStore:
    def __init__(self) -> None:
        self._items: list[str] = []

    def add(self, item: str) -> None:
        self._items.append(item)

    def count(self) -> int:
        return len(self._items)


@pytest.fixture
def store() -> InMemoryStore:
    return InMemoryStore()


def test_adding_items_to_fresh_store_reflects_only_current_test(fake: Faker, store: InMemoryStore) -> None:
    """
    Given: a fresh store fixture.
    When: several items are added.
    Then: the count reflects only those items.
    """
    # --- Arrange ---
    items = [fake.word() for _ in range(ITEMS_PER_TEST)]

    # --- Act ---
    for item in items:
        store.add(item)

    # --- Assert ---
    assert store.count() == ITEMS_PER_TEST
```

**Variety booster:** Run the suite under `pytest-xdist -n auto` to detect shared state; if a test fails only under parallelism, it leaks mutable state.

**Plugin:** `pytest-xdist` provides parallel execution (`-n auto`) that exposes leaked mutable state; install it separately.

## Public API only

[ref: #testing-practices-public-api-only]

Test only public API.
Private methods (`_`, `__`) should be exercised through public methods.
Untestable private methods indicate a design smell.

```python
from faker import Faker

CLAMPED_NEGATIVE_RATE: float = -0.05
AMOUNT_MIN: int = 100
AMOUNT_MAX: int = 1000
MIN_TAX_RATE: float = 0.0
MAX_TAX_RATE: float = 1.0


class Invoice:
    def __init__(self, amount: int) -> None:
        self.amount = amount

    def total_with_tax(self, rate: float) -> float:
        return self.amount * (1 + self._clamp_rate(rate))

    def _clamp_rate(self, rate: float) -> float:
        return max(MIN_TAX_RATE, min(MAX_TAX_RATE, rate))


def test_invoice_total_clamps_negative_tax_rate_through_public_api(fake: Faker) -> None:
    """
    Given: an invoice and a negative tax rate.
    When: calculating total with tax.
    Then: the negative rate is treated as zero.
    """
    # --- Arrange ---
    amount = fake.pyint(min_value=AMOUNT_MIN, max_value=AMOUNT_MAX)
    invoice = Invoice(amount=amount)

    # --- Act ---
    total = invoice.total_with_tax(rate=CLAMPED_NEGATIVE_RATE)

    # --- Assert ---
    assert total == float(amount)
```

**Variety booster:** When a boundary case is hard to reach through public methods, add a new public factory or builder rather than reaching into private state.

## Common test smells and anti-patterns

[ref: #testing-practices-common-test-smells-and-anti-patterns]

Avoid these common anti-patterns: hardcoded data, magic numbers, broad assertions, over-mocking, testing multiple concepts per test, and time-dependent assertions.

| Smell / Anti-pattern | Why it hurts | Preferred alternative |
|---|---|---|
| Hardcoded test data | Hides intent and breaks on unrelated changes | `faker` providers with semantic meaning |
| Magic numbers | Obscures the invariant | Named module-level constants or app-level enums |
| Broad assertions | Passes for wrong reasons | Assert exact invariants with `match` and precise values |
| Over-mocking | Tests implementation, not behavior | Real objects or fakes for internal collaborators |
| Multiple concepts per test | Confusing failures, hidden regressions | Split into focused tests or parametrization |
| Time-dependent assertions | Flaky in CI | `time-machine`, `freezegun`, or injected clocks |

```python
from faker import Faker


class Greeter:
    def greet(self, name: str) -> str:
        return f"Hello, {name}!"


def test_greet_includes_name_in_message(fake: Faker) -> None:
    """
    Given: a generated name.
    When: greeting the user.
    Then: the message contains the name with correct formatting.
    """
    # --- Arrange ---
    name = fake.first_name()

    # --- Act ---
    message = Greeter().greet(name)

    # --- Assert ---
    assert message == f"Hello, {name}!"
```

**Variety booster:** Replace magic numbers with constants derived from app enums, and replace broad `in` assertions with exact shape matchers such as `dirty-equals`.

**Plugin:** `dirty-equals` offers declarative shape matchers for partial structure assertions; install it separately.

## Mocking and fakes

[ref: #testing-practices-mocking-and-fakes]

Prefer real objects or fakes over mocks for internal logic.
Mock only external boundaries.

```python
from abc import ABC, abstractmethod
from faker import Faker


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        ...


class InMemoryNotifier(Notifier):
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)


class NotificationService:
    def __init__(self, notifier: Notifier) -> None:
        self._notifier = notifier

    def notify_user(self, message: str) -> None:
        self._notifier.send(message)


def test_notification_service_sends_message_via_fake_notifier(fake: Faker) -> None:
    """
    Given: a notification service backed by a fake notifier.
    When: a message is sent.
    Then: the fake records the message.
    """
    # --- Arrange ---
    notifier = InMemoryNotifier()
    service = NotificationService(notifier=notifier)
    message = fake.sentence()

    # --- Act ---
    service.notify_user(message)

    # --- Assert ---
    assert notifier.messages == [message]
```

**Variety booster:** Build a small library of fakes for each external boundary and reuse them across tests; use `unittest.mock` only when the boundary is too complex to fake deterministically.
