---
subject: "Keep suites fast and detect regressions: memory ceilings with `limit_memory`, leak detection with `limit_leaks`, allocation reports via `--memray`, benchmarking with `benchmark` fixture/`pedantic`/`--benchmark-compare-fail`, per-test and session timeouts with `pytest-timeout`, slow-test triage via `--durations`, profiling with `--profile`/`cProfile`/`py-spy`, broader fixture scopes for immutable resources, in-memory fakes, parametrized input sizes."
index:
  - anchor: performance-memray
    what: "The `@pytest.mark.limit_memory('24 MB')` marker from pytest-memray that sets a hard peak-memory ceiling on a single test and fails it if the budget is exceeded."
    problem: "Long-running or batch test crosses explicit peak-memory ceiling silently and later causes OOM in CI instead of failing at the boundary; peak ceiling, fail on exceed, headroom allocator, exclude background thread, memory budget, catch regression, ci oom guard."
    use_when: "A single test allocates a large or unbounded amount of memory; peak memory must stay below a known budget; background threads unrelated to the test should be excluded from measurement."
    avoid_when: "The budget is set tight enough to catch normal allocator retention; the test needs to measure growth across iterations rather than a single peak; background thread allocation is the behavior under test."
    expected: "A test that exceeds its peak-memory ceiling fails while tests within budget pass; background threads are excluded with `current_thread_only=True` and the limit tolerates CPython allocator retention."
  - anchor: performance-memray
    what: "The `@pytest.mark.limit_leaks('1 MB')` marker from pytest-memray that runs the test body in a loop so interpreter noise does not hide real growth, failing the test if leaked memory exceeds the budget."
    problem: "Genuine memory leak grows too slowly for single peak ceiling to catch, so incremental growth is hidden across runs; incremental leak growth, peak ceiling blind, loop inside test, interpreter noise averaged, allocation diagnosis, steady state."
    use_when: "A single test allocates memory repeatedly and must show growth per iteration rather than a peak; interpreter noise must be averaged out; the leak budget is calibrated against steady-state allocation."
    avoid_when: "The goal is to catch a one-time peak allocation; per-iteration payload is allocated outside the loop; the budget is set without a steady-state baseline."
    expected: "Real per-iteration growth is surfaced as a failure above the leak budget while steady interpreter noise is averaged out, and `pytest --memray` provides the allocation report for diagnosis."
  - anchor: performance-benchmark
    what: "The `benchmark` fixture that runs a target function and records timing statistics, called as `benchmark(func, *args)`, with per-test tuning via `@pytest.mark.benchmark(min_rounds=...)`."
    problem: "Function timing matters for regression detection, but mixing timing assertions with functional correctness checks makes suite flaky and hard to read; microbenchmark regression, functional separation, round count tuning, noise reduction, target function timing, baseline comparison, repeatable runner."
    use_when: "A function needs repeatable timing measurement; regression detection matters more than a single run; functional correctness is asserted in a separate test."
    avoid_when: "The test is meant to assert functional correctness, not timing; timing measurement is mixed with behavior assertions; no baseline exists for regression comparison."
    expected: "Timing statistics are recorded for the target function, functional behavior is asserted elsewhere, and individual tests can raise their round count via the marker when needed."
  - anchor: performance-benchmark
    what: "The `benchmark.pedantic(target, args=..., rounds=..., iterations=..., warmup_rounds=...)` calling convention that runs setup outside the timed region and controls rounds, iterations, and warmup rounds."
    problem: "Expensive arrange distorts timing when included in measured region, and cold-cache effects add noise before benchmark stabilizes; arrange cost isolation, setup outside timer, cache warmup control, cold cache, iterations, measurement window, build input first."
    use_when: "Arrange cost is significant compared to target execution; setup must not be counted; cold-cache warmup needs explicit control."
    avoid_when: "The callable passed to `pedantic` builds its own input; no warmup rounds are configured despite cold-cache skew; setup cost is negligible."
    expected: "Only the target function is timed, with setup excluded and results stabilized by the configured `rounds`, `iterations`, and `warmup_rounds`."
  - anchor: performance-benchmark
    what: "The `--benchmark-only`, `--benchmark-disable`, `--benchmark-autosave`, `--benchmark-compare`, and `--benchmark-compare-fail=ratio:0.1` command-line options that select, skip, persist, compare, and gate benchmark runs."
    problem: "Benchmark results vary between CI runs, so regressions are hard to gate without persisted historical baselines and explicit deviation tolerance; ci regression gate, benchmark-only run, baseline persistence, deviation tolerance, no source edit, noise versus slowdown."
    use_when: "Benchmarks run as a dedicated CI job or local step; results must persist and compare across runs; regression should fail the build without editing tests."
    avoid_when: "No baseline exists for comparison; `--benchmark-compare-fail` threshold is tighter than runner noise; benchmarks are mixed with normal tests in the same CI job."
    expected: "Benchmarks run or are skipped as intended, results are saved and compared across runs, and CI fails only when a regression exceeds the configured ratio."
  - anchor: performance-timeout
    what: "The `@pytest.mark.timeout(N)` marker (with optional `method='signal'` or `method='thread'`) and the global `timeout = N` default in `pyproject.toml` that abort a test exceeding a duration; `signal` is the POSIX default and allows teardown, while `thread` always works but terminates the whole process."
    problem: "Deadlocks and hangs block entire run if no abort mechanism exists, yet timeout must remain a safety net rather than a precise performance assertion; hang guardrail, platform method choice, teardown preservation, process termination fallback, SLA value, performance assertion confusion."
    use_when: "A test can hang under load or blocking calls; timeout is needed as a safety net, not as a precise performance check; POSIX signal method with teardown is acceptable."
    avoid_when: "Timeout is used to assert an exact performance SLA; `method='thread'` is chosen where teardown must run; marker is applied to merely slow tests with no hang risk."
    expected: "A hung test is aborted before it blocks the run, teardown still runs under `signal` on POSIX, and passing timing is never asserted by the marker."
  - anchor: performance-timeout
    what: "The `--session-timeout` option that caps the entire pytest session so a CI job cannot run indefinitely."
    problem: "CI job runs indefinitely when per-test timeouts are absent or insufficient, so whole session needs an absolute ceiling; session ceiling, terminate runaway, per-test gap, ci runner budget, infinite job prevention, global ceiling, runaway suite killer."
    use_when: "CI job must have an absolute runtime ceiling; per-test timeouts may miss some hangs; whole session needs runaway protection."
    avoid_when: "Session timeout replaces per-test timeouts on hang-prone tests; long CI jobs are left uncapped; per-test timeout is removed because session cap exists."
    expected: "The session is bounded so CI jobs terminate within the cap, while per-test markers continue to catch individual hangs."
  - anchor: performance-durations
    what: "The `pytest --durations=N --durations-min=S` report that lists the N slowest tests, setups, and teardowns exceeding the threshold S."
    problem: "Slowest tests, setups, and teardowns remain hidden until suite speed degrades, so they need explicit surfacing for triage; slow test leaderboard, noise threshold, fixture scope culprit, integration marker migration, review cadence, regression hotspot."
    use_when: "Suite speed is degrading or needs monitoring; an ordered list of slow tests, setups, and teardowns is needed; threshold filters noise and identifies optimization candidates."
    avoid_when: "`--durations` is treated as a pass/fail gate instead of triage input; threshold is set so low it drowns signal; slow tests are never reviewed after surfacing."
    expected: "Tests above the durations threshold are reviewed regularly and refactored via broader fixtures, fakes, or an integration marker."
  - anchor: performance-profiling
    what: "Per-test and deeper profiling options: `pytest --profile --profile-svg` via pytest-profiling for per-test cProfile output, `cProfile` with `snakeviz` for flamegraph-style exploration, and `py-spy` for low-overhead sampling of production-like behavior."
    problem: "Test runtime is dominated by unknown hotspots, and wrong profiler choice either lacks resolution or slows normal suite runs; per-test profile, flamegraph explore, sampling profiler, svg output, profiling resolution, normal run fast, sampling overhead tradeoff."
    use_when: "Time attribution is needed at function level; deterministic per-test cProfile or low-overhead sampling is acceptable; normal runs must stay fast."
    avoid_when: "`py-spy` sampling is used when deterministic per-test attribution is needed; `--profile-svg` artifacts are produced on the default fast path; profiling tests are not gated out of normal runs."
    expected: "The chosen profiler yields per-test cProfile data, flamegraph exploration, or low-overhead samples appropriate to the investigation depth, without slowing normal runs."
  - anchor: performance-profiling
    what: "Keeping profiling tests separate and optional behind `@pytest.mark.profile` and `@pytest.mark.slow`, then running them selectively with `pytest -m profile` or `pytest -m slow`."
    problem: "Expensive profiling runs slow normal suite and CI if they execute by default, yet they must remain runnable on demand; marker gated, selective run, default fast path, slow marker, on-demand profile, separate suite, ci skip profiling, local fast feedback."
    use_when: "Profiling tests are expensive; default suite must stay fast locally and in CI; markers keep them runnable on demand."
    avoid_when: "Profiling tests execute in unmarked normal runs; `profile`/`slow` selection is forgotten when profiling is needed; expensive profiling is not marked at all."
    expected: "Profiling tests run only when their marker is selected, so normal runs stay fast and profiling remains available on demand."
  - anchor: performance-design
    what: "Widening a fixture to a broader scope such as `scope='session'` for an expensive resource so setup is amortized across tests, valid only when the resource is immutable or properly reset between tests."
    problem: "Expensive resource setup repeats for every test and makes suite runtime grow linearly, but sharing mutable state breaks isolation; setup cost amortization, immutable shared resource, resettable state, session scope fixture, shared mutable hazard, isolation preservation."
    use_when: "Resource setup is expensive; the resource is immutable or can be reset between tests; amortization outweighs isolation risk."
    avoid_when: "Scope is broadened for a mutable resource that is not reset between tests; shared mutable state leaks between tests; setup cost is saved at the expense of isolation."
    expected: "Expensive setup runs once per scope instead of once per test, and isolation holds because the shared resource is immutable or reset between tests."
  - anchor: performance-design
    what: "Replacing real network or disk calls with fakes or in-memory implementations in unit tests when the test target is the business logic rather than the I/O layer."
    problem: "Unit test slows and flakes because of heavy I/O that is not the behavior under test; memory-backed stub, network call avoidance, disk io avoidance, business logic target, real io integration, deterministic execution, integration boundary."
    use_when: "Unit target is business logic, not the I/O layer; real network or disk would slow or flake; a fake keeps the test deterministic."
    avoid_when: "Real network or disk I/O is performed in unit tests targeting business logic; the I/O layer is not covered by dedicated integration tests; fakes are not used where real I/O is irrelevant."
    expected: "Unit tests run against in-memory fakes and stay fast and deterministic, while real I/O is confined to tests that target the I/O layer."
  - anchor: performance-variety-booster
    what: "Applying custom markers (for example a `unit` marker) to slow or integration tests and running those subsets selectively so the fast path stays fast."
    problem: "Default run slows because slow or integration tests execute unconditionally, hurting local feedback and CI cadence; fast default run, integration test split, slow test exclusion, marker-based selection, on-demand execution, fixture scope optimization, local ci speed."
    use_when: "Default run must stay fast; slow or integration tests can run selectively; markers encode the split."
    avoid_when: "Slow or integration tests run on the default path; tests are left unmarked so they cannot be excluded; fixture scope is not optimized for immutable resources."
    expected: "The default run excludes slow or integration tests via markers, and those tests run only when their subset is selected."
libraries:
  - py-spy
  - pytest-benchmark
  - pytest-memray
  - pytest-profiling
  - pytest-timeout
  - snakeviz
---

# Performance

Performance reference for pytest: memory tracking, benchmarking, timeouts, profiling, and test design that keeps the suite fast.

## Memory tracking with pytest-memray

[ref: #performance-memray]

Use `pytest-memray` to detect memory leaks and unexpected allocations in long-running or batch-processing tests.

Set a hard ceiling with `@pytest.mark.limit_memory`:

```python
import pytest
from faker import Faker


@pytest.mark.limit_memory("24 MB")
def test_large_file_processing_does_not_leak(fake: Faker) -> None:
    """
    Given: a generated filename.
    When: a large file is processed.
    Then: memory usage stays within the memray limit.
    """
    # --- Arrange ---
    filename = f"{fake.pystr(min_chars=3, max_chars=10)}.json"

    # --- Act ---
    process_large_file(filename)

    # --- Assert ---
    # Memory assertion handled by the limit_memory marker.
```

Detect leaks by running the body in a loop so interpreter noise does not hide real growth:

```python
import pytest
from faker import Faker


@pytest.mark.limit_leaks("1 MB")
def test_batch_processor_does_not_accumulate_memory(fake: Faker) -> None:
    """
    Given: repeated batch processing calls.
    When: many batches are processed.
    Then: leaked memory stays within the memray limit.
    """
    # --- Arrange ---
    # payloads will be generated inside the loop.

    # --- Act ---
    for _ in range(100):
        payload = fake.pydict(value_types=["str", "int", "float"])
        process_batch(payload)

    # --- Assert ---
    # Leak assertion handled by the limit_leaks marker.
```

Run with the `--memray` flag to get allocation reports:

```bash
pytest --memray
```

Restrict tracking to the current thread when background threads are unrelated:

```python
import pytest


@pytest.mark.limit_memory("24 MB", current_thread_only=True)
def test_worker_thread_stays_within_budget() -> None:
    """
    Given: a worker that runs in the current thread.
    When: the worker is executed.
    Then: memory usage stays within the limit for the current thread.
    """
    # --- Arrange ---
    # Worker is ready to run.

    # --- Act ---
    run_worker()

    # --- Assert ---
    # Memory assertion handled by the limit_memory marker.
```

Leave headroom in memory limits because CPython's object allocator may not return freed memory to the OS immediately.

## Benchmarking with pytest-benchmark

[ref: #performance-benchmark]

Use `pytest-benchmark` for microbenchmarks and regression detection, not for functional correctness.

The `benchmark` fixture runs the target function and records timing statistics:

```python
from typing import Any

from faker import Faker


def test_serialize_payload_is_fast_enough(
    benchmark: Any,
    fake: Faker,
) -> None:
    """
    Given: a generated payload.
    When: serialization is benchmarked.
    Then: the benchmark runs without functional failure.
    """
    # --- Arrange ---
    payload = fake.pydict(value_types=["str", "int", "float"])

    # --- Act / Assert ---
    benchmark(serialize_payload, payload)
```

Use `benchmark.pedantic` when setup must happen outside the timed region:

```python
from typing import Any

from faker import Faker


def test_sort_stays_fast_across_sizes(
    benchmark: Any,
    fake: Faker,
) -> None:
    """
    Given: a large list of generated integers.
    When: sorting is benchmarked with controlled warmup and rounds.
    Then: the benchmark completes without functional failure.
    """
    # --- Arrange ---
    items = [fake.pyint(min_value=0, max_value=1_000_000) for _ in range(10_000)]

    # --- Act / Assert ---
    benchmark.pedantic(
        sorted,
        args=(items,),
        rounds=20,
        iterations=5,
        warmup_rounds=2,
    )
```

Control benchmark execution from the CLI:

```bash
pytest --benchmark-only              # run only benchmark tests
pytest --benchmark-disable           # skip benchmarks entirely
pytest --benchmark-autosave          # store results to disk
pytest --benchmark-compare           # compare against saved results
pytest --benchmark-compare-fail=ratio:0.1  # fail if deviation exceeds 10%
```

Tune individual tests with the benchmark marker:

```python
from typing import Any

import pytest


@pytest.mark.benchmark(min_rounds=50)
def test_hash_lookup_is_consistent(benchmark: Any) -> None:
    """
    Given: a stable input string.
    When: hash is benchmarked repeatedly.
    Then: the benchmark completes without functional failure.
    """
    # --- Arrange ---
    input_value = "stable-input"

    # --- Act / Assert ---
    benchmark(hash, input_value)
```

## Timeouts with pytest-timeout

[ref: #performance-timeout]

Use `pytest-timeout` as a last-resort safety net against hanging tests, not as a precise performance assertion.

Set a per-test timeout with a marker:

```python
import pytest


@pytest.mark.timeout(30)
def test_report_generation_completes(fake: Faker) -> None:
    """
    Given: a generated company name.
    When: a report is generated.
    Then: the operation completes within the timeout.
    """
    # --- Arrange ---
    company = fake.company()

    # --- Act ---
    generate_report(company)

    # --- Assert ---
    # Timeout assertion handled by the timeout marker.
```

Set global defaults in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
timeout = 60
```

Two timeout methods are available.
`signal` is the default on POSIX and allows teardown to run.
`thread` always works but terminates the whole process, so prefer `signal` on POSIX and reserve `thread` for platforms or cases where `signal` cannot be used.

```python
import pytest


@pytest.mark.timeout(10, method="thread")
def test_blocking_call_fails_fast() -> None:
    """
    Given: a call that may block indefinitely.
    When: it is invoked under a thread-based timeout.
    Then: the test is terminated before the global timeout expires.
    """
    # --- Arrange ---
    # call_that_may_block_forever is expected to hang.

    # --- Act ---
    call_that_may_block_forever()

    # --- Assert ---
    # Timeout assertion handled by the timeout marker.
```

Protect the entire session with `--session-timeout` to prevent CI jobs from running indefinitely.

## Identifying slow tests

[ref: #performance-durations]

Use `--durations=10` in CI to surface the 10 slowest tests and target them for optimization:

```bash
pytest --durations=10 --durations-min=1.0
```

This lists the slowest tests, setups, and teardowns that exceed the threshold.
Review the output regularly to spot regressions and decide which slow tests deserve broader fixtures, fakes, or a move to an integration marker.

## Profiling

[ref: #performance-profiling]

Use the `pytest-profiling` plugin to capture per-test `cProfile` output:

```bash
pytest --profile --profile-svg
```

For deeper investigation, use `cProfile` with `snakeviz` for flamegraph-style exploration or sampling profilers like `py-spy` to inspect production-like behavior with low overhead.

Keep profiling tests separate and optional so they do not slow normal runs:

```python
import pytest


@pytest.mark.profile
@pytest.mark.slow
@pytest.mark.limit_memory("64 MB")
def test_end_to_end_import_profile(fake: Faker) -> None:
    """
    Given: a list of generated filenames.
    When: documents are ingested end-to-end.
    Then: the operation stays within the memory limit and completes for profiling.
    """
    # --- Arrange ---
    filenames = [fake.file_name() for _ in range(100)]

    # --- Act ---
    ingest_documents(filenames)

    # --- Assert ---
    # Memory and profiling assertions handled by markers.
```

Run profiling markers selectively:

```bash
pytest -m profile
pytest -m slow
```

## Performance-friendly test design

[ref: #performance-design]

Prefer broader fixture scopes for expensive resources, but only when the resource is immutable or properly reset between tests.
Avoid heavy I/O in unit tests by using fakes or in-memory implementations.
Mark slow or integration tests with custom markers and run them selectively.

```python
import pytest
from faker import Faker


@pytest.fixture(scope="session")
def search_index() -> SearchIndex:
    index = build_search_index()
    yield index
    index.close()


@pytest.mark.unit
def test_search_returns_matches_for_word(
    fake: Faker,
    search_index: SearchIndex,
) -> None:
    """
    Given: a session-scoped search index and a generated document.
    When: the document is added and searched by its first word.
    Then: the index returns a match.
    """
    # --- Arrange ---
    document = fake.sentence()

    # --- Act ---
    search_index.add(document)

    # --- Assert ---
    assert search_index.find(document.split()[0])
```

Use in-memory fakes instead of real network or disk calls when the test target is the business logic:

```python
from faker import Faker


def test_price_calculation_uses_fake_rates(fake: Faker) -> None:
    """
    Given: a fake rate provider with generated rates.
    When: a conversion is computed.
    Then: the result is positive.
    """
    # --- Arrange ---
    rates = FakeRateProvider({fake.currency_code(): fake.pyfloat(positive=True)})
    calculator = PriceCalculator(rates)
    amount = fake.pyint(min_value=1, max_value=1000)

    # --- Act ---
    result = calculator.convert(amount, "USD", "EUR")

    # --- Assert ---
    assert result > 0
```

## Variety booster

[ref: #performance-variety-booster]

You can cover more invariants with less code by parametrizing benchmark or allocation tests over input sizes and implementation variants.
Let pytest-benchmark or pytest-memray run each variant, and assert that growth stays bounded rather than asserting exact numbers that depend on the interpreter version.

```python
from typing import Any

import pytest
from faker import Faker


@pytest.mark.parametrize("size", [10, 100, 1_000])
def test_merge_sort_scales_linearly(
    benchmark: Any,
    fake: Faker,
    size: int,
) -> None:
    """
    Given: a parametrized list size.
    When: sorting is benchmarked.
    Then: the benchmark completes without functional failure.
    """
    # --- Arrange ---
    items = [fake.pyint(min_value=0, max_value=size) for _ in range(size)]

    # --- Act / Assert ---
    benchmark.pedantic(sorted, args=(items,), rounds=10, iterations=3)
```
