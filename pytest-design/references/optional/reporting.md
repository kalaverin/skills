---
subject: "Produce human and machine test evidence: Allure results via `--alluredir` with `allure.attach` and `environment.properties`, clearer diffs via `pytest-clarity`/`pytest-icdiff`, JUnit XML via `--junit-xml`, HTML via `pytest-html`, JSON via `pytest-json-report`, CI surfacing via `pytest-results-action`, and a flaky-test mitigation hierarchy (reruns, random order, flakefinder) with screenshots/logs on UI failure."
index:
  - anchor: reporting-allure-integration
    what: "Install `allure-pytest`, run with `--alluredir <dir>`, generate/serve with `allure generate`/`allure serve`; use decorators (`feature`/`story`/`severity`/`title`/`description`/`link`/`issue`/`testcase`/`tag`/`label`) and `allure.dynamic.*`, attach via `allure.attach`/`allure.attach.file`, add `environment.properties`, and use `ALLURE_TESTPLAN_PATH` for test plans."
    problem: "Rich navigable report needs structured metadata, runtime labels, attachments, environment context, and test-plan selection; static dynamic metadata, attach file, environment properties, test plan path, severity story, navigable report."
    use_when: "Rich report needs structured metadata, runtime labels, attachments, environment context, and test plan selection for navigable triage; static dynamic metadata, attach file, environment properties, test plan path, severity story, navigable report, allure."
    avoid_when: "Do not attach binary files with `allure.attach` (use `allure.attach.file`), and do not rely on static decorators when a value is only known at runtime (use `allure.dynamic.*`)."
    expected: "Allure reports carry full static/dynamic metadata, attachments, environment context, and support test-plan-scoped runs."
  - anchor: reporting-diff-friendly-assertions
    what: "Use `pytest-clarity` or `pytest-icdiff` (ask the user to install) for side-by-side/colorized diffs on large dict/list comparisons; both auto-activate once installed."
    problem: "Default traceback for large nested payload, row, or API response is hard to read, hiding mismatch; side-by-side diff, colorized diff, nested payload, readable mismatch, plugin install ask, large comparison."
    use_when: "Large nested payload, row, or API response mismatch is unreadable, diff plugin must make mismatch visible without long traceback unfolding; side by side diff, colorized diff, nested payload, readable mismatch, plugin install ask, large comparison, clarity."
    avoid_when: "Do not rely on default assertion output for large nested comparisons, and do not install the plugin yourself — ask the user to install `pytest-clarity`/`pytest-icdiff`."
    expected: "Large comparisons render side-by-side/colorized diffs once a diff plugin is installed and approved."
  - anchor: reporting-junit-xml-and-ci
    what: "Emit JUnit XML with `--junit-xml=path.xml` or the `junit_xml` config key; upload with `if: always()` and publish via `pytest-results-action`/`publish-test-results` so CI annotates PRs and tracks flakiness."
    problem: "CI needs machine-readable results file published even when tests fail; xml artifact, upload always, publish results, annotate pr, flaky trend, never gate on success."
    use_when: "CI needs machine readable results even when tests fail, artifact upload must run always, and PR annotations reveal flaky trend; xml artifact, upload always, publish results, annotate pr, flaky trend, never gate on success, junit report."
    avoid_when: "Do not gate the JUnit upload/publish steps behind test success — use `if: always()` so failures are still reported."
    expected: "JUnit XML is produced and published on every run (pass or fail), surfacing failures and flaky trends in PRs."
  - anchor: reporting-html-and-json-reports
    what: "`pytest-html` produces `--html=report.html --self-contained-html` for human review; `pytest-json-report` emits `--json-report --json-report-file=reports/report.json` for automation."
    problem: "Humans need shareable HTML while dashboards and quality gates need machine-readable JSON; human report, automation input, self-contained, archive artifact, format match consumer, downstream parse."
    use_when: "Humans need shareable HTML, dashboards need JSON, and both artifacts should archive for later inspection; human report, automation input, self contained, archive artifact, format match consumer, downstream parse, html json."
    avoid_when: "Do not use HTML as the automation input or JSON as the human-facing report — match the format to the consumer."
    expected: "HTML reports serve human review and JSON reports feed automation, both archived as CI artifacts."
  - anchor: reporting-flaky-test-handling
    what: "Treat flakiness as an isolation/determinism signal: fix isolation first, expose order bugs with `pytest-randomly`/`pytest-flakefinder`, use `pytest-rerunfailures` (`@pytest.mark.flaky(reruns=N)`) only as a temporary safety net, and `xfail` genuinely broken tests with a linked issue."
    problem: "Retries and single-order passes mask hidden coupling instead of fixing it; isolation first, randomize expose order, temporary rerun, xfail with issue, root cause, hidden dependency."
    use_when: "Retries and single order passes mask coupling, isolation must fix root cause first, and rerun stays temporary safety net; isolation first, randomize expose order, temporary rerun, xfail with issue, root cause, hidden dependency, flake signal."
    avoid_when: "Do not leave reruns in place permanently, and do not treat randomized order as a fix — a suite passing only in one order has hidden bugs."
    expected: "Flakiness is eliminated by isolation/determinism fixes; reruns are temporary and broken tests are tracked via `xfail`."
  - anchor: reporting-screenshots-and-artifacts
    what: "Attach UI evidence (screenshots, videos, DOM snapshots, browser logs) on failure via `allure.attach.file()` or framework helpers (Playwright/Selenium), and store videos in CI artifacts with `if: always()`."
    problem: "UI failure without attached evidence forces local reproduction to triage; screenshot on failure, video artifact, dom snapshot, browser log, store always, triage without reproduce."
    use_when: "UI failure lacks evidence, local reproduction is costly, and screenshot video DOM snapshot or browser log should attach on failure; screenshot on failure, video artifact, dom snapshot, browser log, store always, triage without reproduce, ui evidence."
    avoid_when: "Do not gate artifact storage on test success, and do not rely on screenshots alone for timing-sensitive failures (keep videos too)."
    expected: "Every UI failure carries attached evidence (screenshots/videos/logs) archived in CI, enabling triage without local reproduction."
  - anchor: reporting-variety-booster
    what: "Combine parametrization, property-style assertions, and Faker boundary values to sweep roles/statuses/sizes in one test asserting a single contract instead of one test per happy path."
    problem: "One test per happy path bloats suite and makes failures point to missing test cases rather than missing invariants; contract sweep, role status size, single contract, boundary values, missing invariant, collapse happy paths."
    use_when: "Happy path tests multiply, one contract sweep over roles statuses and sizes finds missing invariants with less code; contract sweep, role status size, single contract, boundary values, missing invariant, collapse happy paths, parametrized invariant."
    avoid_when: "Do not add a separate test per happy path — collapse them into one parametrized contract sweep."
    expected: "A small parametrized suite covers many invariants, with each failure pointing to a missing invariant."
libraries:
  - allure-pytest
  - pytest-clarity
  - pytest-flakefinder
  - pytest-html
  - pytest-icdiff
  - pytest-json-report
  - pytest-randomly
  - pytest-rerunfailures
---

# Reporting and CI

## Allure Integration
[ref: #reporting-allure-integration]

Install the `allure-pytest` plugin.
Run pytest with `--alluredir <dir>` to collect results.
Generate or serve the report with `allure generate <dir>` or `allure serve <dir>`.

```python
from collections.abc import Callable
from typing import Any

import allure
from faker import Faker


@allure.step("Create user via API")
def create_user_via_api(client, user_data: dict[str, object]) -> dict[str, object]:
    response = client.post("/users", json=user_data)
    allure.attach(
        response.text,
        name="response",
        attachment_type=allure.attachment_type.JSON,
    )
    response.raise_for_status()
    return response.json()


@allure.feature("User Management")
@allure.story("User Registration")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Register a new user with valid data")
@allure.description("Verify that a user can be registered with syntactically valid and unique data.")
@allure.link("https://docs.example.com/user-registration", name="Documentation")
@allure.issue("JIRA-123", name="Related bug")
@allure.testcase("TC-456", name="Registration happy path")
@allure.tag("regression", "smoke")
@allure.label("component", "api")
def test_user_registration_with_valid_data(
    client: Any,
    user_factory: Callable[..., dict[str, object]],
    fake: Faker,
) -> None:
    """
    Given: valid user data from the factory.
    When: the user is created via the API.
    Then: the response email matches the request email.
    """
    # --- Arrange ---
    user_data = user_factory(email=fake.fake_email())

    # --- Act ---
    result = create_user_via_api(client, user_data)

    # --- Assert ---
    assert result["email"] == user_data["email"]
```

Dynamic labels are useful when the value is only known at runtime.
Call `allure.dynamic.*` inside the test body instead of, or together with, static decorators.

```python
from collections.abc import Callable
from typing import Any

import allure
from faker import Faker


@allure.feature("User Management")
@allure.story("Role-based workflow")
def test_user_workflow_by_role(
    user_factory: Callable[..., Any],
    fake: Faker,
    role: str,
) -> None:
    """
    Given: a parametrized role.
    When: a user is created for that role.
    Then: the user's role matches the parametrized value.
    """
    # --- Arrange ---
    allure.dynamic.parameter("role", role)
    allure.dynamic.title(f"Workflow succeeds for role {role}")
    allure.dynamic.tag(role)
    user = user_factory(role=role, email=fake.fake_email())

    # --- Act ---
    actual_role = user.role

    # --- Assert ---
    assert actual_role == role
```

Attach files and arbitrary data to a step or test result.
Binary files should be attached with `allure.attach.file()`.

```python
import json
from pathlib import Path
from typing import Any

import allure
from faker import Faker


def test_exported_report_contains_expected_fields(
    tmp_path: Path,
    fake: Faker,
) -> None:
    """
    Given: a JSON report written to tmp_path.
    When: the report is attached and read back.
    Then: it contains the expected email field.
    """
    # --- Arrange ---
    report_path = tmp_path / "report.json"
    payload = {"name": fake.name(), "email": fake.fake_email()}
    report_path.write_text(json.dumps(payload), encoding="utf-8")

    # --- Act ---
    allure.attach.file(
        str(report_path),
        name="exported-report",
        attachment_type=allure.attachment_type.JSON,
    )
    data = json.loads(report_path.read_text(encoding="utf-8"))

    # --- Assert ---
    assert "email" in data
```

Parametrized test arguments appear in Allure automatically.
Override the display name with `allure.dynamic.parameter()` when the raw value is noisy.

```python
from collections.abc import Callable
from typing import Any

import allure
import pytest
from faker import Faker


@pytest.mark.parametrize(
    ("email_factory", "expected_status"),
    [
        pytest.param(lambda fake: fake.fake_email(), 201, id="valid"),
        pytest.param(lambda fake: "invalid-email", 422, id="malformed"),
    ],
)
def test_registration_parametrized(
    client: Any,
    fake: Faker,
    email_factory: Callable[[Faker], str],
    expected_status: int,
) -> None:
    """
    Given: a parametrized email factory and expected status.
    When: the registration endpoint is called.
    Then: the response status matches the expectation.
    """
    # --- Arrange ---
    email = email_factory(fake)
    allure.dynamic.parameter("email", email)

    # --- Act ---
    response = client.post("/users", json={"email": email})

    # --- Assert ---
    assert response.status_code == expected_status
```

Add environment metadata by writing an `environment.properties` file next to the results.
Allure renders these values in the Environment widget.

```text
Python=3.12.0
Branch=main
Commit=abc123
CI=true
```

Run a subset of tests from a test plan by setting `ALLURE_TESTPLAN_PATH` to a JSON file that lists selected test cases.
This is common in large suites where a release scope is defined in an external system.

```bash
ALLURE_TESTPLAN_PATH=allure-testplan.json pytest --alluredir allure-results
```

## Diff-Friendly Assertions
[ref: #reporting-diff-friendly-assertions]

Large dict and list comparisons produce hard-to-read default tracebacks.
Ask user to install `pytest-clarity` or `pytest-icdiff` to get side-by-side or colorized diffs.
Both plugins activate automatically once installed.

Prefer them for suites that assert on deeply nested payloads, database rows, or API responses.
The diff output makes mismatches visible without unfolding long `AssertionError` messages.

## JUnit XML and CI
[ref: #reporting-junit-xml-and-ci]

pytest emits JUnit XML with `--junit-xml=path.xml` or the `junit_xml` config key.
CI platforms consume this file to annotate pull requests and track flaky tests over time.

```toml
[tool.pytest.ini_options]
junit_xml = "reports/junit.xml"
junit_suite_name = "api-tests"
```

In GitHub Actions, upload the XML artifact with `if: always()` so results are published even when tests fail.
Then use `pytest-results-action` or `publish-test-results` to surface failures in the PR summary.

```yaml
- name: Run tests
  run: pytest --junit-xml=reports/junit.xml

- name: Upload JUnit report
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: junit-report
    path: reports/junit.xml

- name: Publish test results
  if: always()
  uses: pmeier/pytest-results-action@v0.7.0
  with:
    path: reports/junit.xml
```

## HTML and JSON Reports
[ref: #reporting-html-and-json-reports]

`pytest-html` produces a self-contained HTML report via `--html=report.html`.
It is useful for manual inspection and sharing with non-developer stakeholders.

```bash
pytest --html=reports/report.html --self-contained-html
```

`pytest-json-report` emits a machine-readable report.
Dashboards, trend scripts, and downstream quality gates can parse it directly.

```bash
pytest --json-report --json-report-file=reports/report.json
```

Use HTML reports for human review and JSON reports for automation.
Store both as CI artifacts so historical results remain available.

## Flaky Test Handling
[ref: #reporting-flaky-test-handling]

Flaky tests usually indicate uncontrolled state, timing assumptions, or order-dependent code.
Treat the symptom as a signal to improve isolation and determinism before adding retries.

Mitigation hierarchy:

1. Fix isolation first.
Reset databases, caches, filesystem state, and external mocks between tests.
Use function-scoped fixtures for anything that carries state.
2. Expose order-dependent bugs locally.
Run tests with `pytest-randomly` or `pytest-flakefinder` to surface hidden coupling.
3. Use `pytest-rerunfailures` as a temporary safety net.
Mark a known unstable test with `@pytest.mark.flaky(reruns=N)` while the root cause is being fixed.
Do not leave reruns in place permanently.
4. Mark genuinely broken tests as `xfail`.
Link the issue and state the condition so the failure is visible and tracked.

```python
from typing import Any

import pytest
from faker import Faker


@pytest.mark.flaky(reruns=2)
def test_eventual_consistency_of_search_index(
    search_client: Any,
    fake: Faker,
) -> None:
    """
    Given: a generated search query.
    When: the search client returns a result.
    Then: the query appears in the result query.
    """
    # --- Arrange ---
    query = fake.word()

    # --- Act ---
    result = search_client.search(query)

    # --- Assert ---
    assert query in result.query


@pytest.mark.xfail(reason="Race in inventory decrement", strict=False)
def test_concurrent_inventory_update(inventory_client: Any) -> None:
    """
    Given: an inventory client.
    When: concurrent updates are performed.
    Then: expected behavior is documented (currently expected to fail).
    """
    # --- Arrange ---
    # Concurrent update setup goes here.

    # --- Act ---
    ...

    # --- Assert ---
    # Assertion goes here once the race is fixed.
```

Randomizing test order is a diagnostic tool, not a fix.
A suite that passes only in one order is a suite with hidden bugs.

## Screenshots and Artifacts
[ref: #reporting-screenshots-and-artifacts]

UI tests should attach evidence on failure so triage does not require a local reproduction.
Capture screenshots, videos, DOM snapshots, and browser logs.
Use `allure.attach.file()` or helpers provided by Playwright, Selenium, or your framework.

```python
from pathlib import Path

import allure
from faker import Faker


def test_login_page_renders_dashboard(
    page: Any,
    tmp_path: Path,
    fake: Faker,
) -> None:
    """
    Given: a login page with generated credentials.
    When: the login form is submitted.
    Then: the browser navigates to /dashboard; a screenshot is attached on failure.
    """
    # --- Arrange ---
    email = fake.fake_email()
    password = fake.password(length=16)

    # --- Act ---
    page.goto("/login")
    page.fill("input[name=email]", email)
    page.fill("input[name=password]", password)
    page.click("button[type=submit]")

    # --- Assert ---
    try:
        page.wait_for_url("/dashboard")
    except AssertionError:
        screenshot = tmp_path / "failure.png"
        page.screenshot(path=str(screenshot))
        allure.attach.file(
            str(screenshot),
            name="dashboard-failure",
            attachment_type=allure.attachment_type.PNG,
        )
        raise
```

Store videos in CI artifacts with `if: always()`.
Videos are especially valuable for timing-sensitive failures that screenshots alone cannot explain.

## Variety Booster

[ref: #reporting-variety-booster]

Cover more invariants with less code by combining parametrization, property-style assertions, and Faker-generated boundary values.
Instead of one test per happy path, write one parametrized test that sweeps over roles, statuses, and sizes while asserting a single contract.
For example, a single parametrized test can verify that every user role receives a valid dashboard link, that every invalid payload returns `422`, or that every large payload respects pagination limits.
This keeps the suite small and makes each failure point to a missing invariant rather than a missing test case.
