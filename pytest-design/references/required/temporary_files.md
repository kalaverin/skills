---
subject: "Create isolated, reproducible filesystem fixtures: function-scoped `tmp_path` for per-test dirs, build files with `joinpath`/`write_text`/`write_bytes` and explicit encoding, organize with `mkdir`, shared immutable artifacts via `tmp_path_factory.mktemp`, avoid legacy `tmpdir` (`-p no:legacypath`), tune retention with `tmp_path_retention_count`/`tmp_path_retention_policy`, `--basetemp`, and `PYTEST_DEBUG_TEMPROOT`; parametrize extensions/encodings/counts/nesting."
index:
  - anchor: temporary-files-tmp-path
    what: "The `tmp_path` fixture returns a unique `pathlib.Path` directory for every test invocation, created under the pytest temp root and cleaned up automatically."
    problem: "Per-test filesystem state must isolate so it never leaks into other tests, and assertions must not depend on leftover files from previous invocations; unique dir, per-test, auto removed, no leak, local state, clean slate."
    use_when: "A test needs an isolated writable directory created automatically and cleaned up after the run; no other test may read or write the same directory."
    avoid_when: "Several tests must read the same expensive artifact; the directory contents must persist after the test for manual inspection outside retention; mutable state must be shared across tests."
    expected: "Each test writes to its own directory that is cleaned up automatically, with no filesystem state leaking between tests."
  - anchor: temporary-files-text-and-binary
    what: "Creating files with `write_text(encoding=...)`/`write_bytes()` and reading back via `read_text`/`read_bytes` (content-focused assertions instead of mocks)."
    problem: "Implicit platform encodings and mock-based reads make file tests flaky and unfocused, and assertions should exercise real read path instead of stubbing it; explicit encoding, content round-trip, binary payload, production reader, content assertion, no implicit codec, no py.path."
    use_when: "A test reads or writes text/binary files and assertions must exercise the real file content rather than mocks; encoding must be explicit."
    avoid_when: "`open(..., 'w')` is used without an encoding; legacy `py.path.local` write methods are used; assertions target the mock instead of the actual file content."
    expected: "Files are written with declared encodings and read back via the production abstraction, keeping assertions on content rather than mocks."
  - anchor: temporary-files-subdirectories
    what: "Using `mkdir()` under `tmp_path` to create named subdirectories that group artifacts by role (input, output, cache)."
    problem: "Dumping every artifact into root temp directory makes multi-role tests harder to diagnose on failure and lets unrelated outputs hide real culprit; group by role, input output cache, mkdir, diagnose failure, no flatten, purpose subdirs."
    use_when: "A single test produces multiple artifact kinds and grouping them by role simplifies diagnosis."
    avoid_when: "All artifacts are flattened into the root `tmp_path` when distinct roles exist; only one artifact kind is produced; subdirectories add no diagnostic value."
    expected: "Multi-role tests organize artifacts into input/output/cache subdirectories, so failures point to the right role."
  - anchor: temporary-files-tmp-path-factory
    what: "The session-scoped `tmp_path_factory.mktemp()` for directories shared across tests, holding only immutable/read-only data to preserve isolation."
    problem: "Expensive shared artifacts regenerated per test waste time and hide failures, but shared mutable state breaks isolation between invocations; session base, immutable read-only, create once, no function dependency, no mutable shared, mktemp."
    use_when: "Several tests need the same expensive immutable setup and a session-scoped read-only directory is acceptable."
    avoid_when: "A session-scoped fixture depends on a function-scoped fixture such as `fake`; mutable data is placed in the shared directory; artifacts are written by individual tests."
    expected: "Expensive immutable artifacts are built once per session and shared read-only, with no function-scoped dependency leaking into session scope."
  - anchor: temporary-files-legacy-tmpdir
    what: "Preferring `tmp_path`/`tmp_path_factory` (standard `pathlib.Path`) over legacy `tmpdir`/`tmpdir_factory` (`py.path.local`), and disabling the legacy fixtures with `-p no:legacypath`."
    problem: "Mixing legacy and pathlib paths in one codebase adds conversion friction, lets legacy APIs creep back, and forces new contributors to learn deprecated types; pathlib only, disable legacy, ci grep, no conversion, no mix, modernize."
    use_when: "The codebase still contains `tmpdir`/`tmpdir_factory` or `py.path.local` and must be migrated to `pathlib.Path`."
    avoid_when: "New code uses `tmpdir`/`tmpdir_factory`; `py.path.local` is mixed with `pathlib.Path` in the same test; legacy fixtures are not disabled project-wide."
    expected: "All temp paths are `pathlib.Path` with no format conversion, and legacy fixtures are disabled project-wide and guarded in CI."
  - anchor: temporary-files-retention
    what: "Configuring how many temp roots pytest keeps (`tmp_path_retention_count`/`tmp_path_retention_policy`) and where they live (`--basetemp`, `PYTEST_DEBUG_TEMPROOT`), with unique base dirs for concurrent/xdist runs."
    problem: "Default retention keeps only last three runs and may hide failing artifacts, while custom temp root must place and clean safely without deleting valuable data; retention count, basetemp, debug temproot, collision-free xdist, blind remove warning, post-failure inspect."
    use_when: "The suite needs to keep more or fewer temp roots than the default, use a custom temp root, or run concurrently without base-dir collisions."
    avoid_when: "`--basetemp` points at a directory containing valuable data; retention is set without considering post-failure inspection; unique base dirs are not provided for concurrent runs."
    expected: "Retention keeps enough temp roots for debugging after failure, custom roots are placed and cleaned safely, and concurrent/xdist runs get collision-free base dirs."
  - anchor: temporary-files-factory-fixture
    what: "A fixture that returns a callable which mints a fresh subdirectory under one session base on every call, combining shared setup with per-test isolation."
    problem: "Tests need many isolated directories sharing expensive parent, but creating session base per call or sharing one mutable directory breaks isolation; callable mints subdir, fresh per call, shared base, isolated workspace, no same dir, no write outside."
    use_when: "Many tests need fresh subdirectories under one shared parent that is expensive to build."
    avoid_when: "The callable returns the same directory from every call; it writes outside the parent directory; the parent directory is not created session-wide."
    expected: "Each call yields a unique subdirectory under one session base, so callers stay isolated while sharing the parent."
  - anchor: temporary-files-path-containment
    what: "Asserting that every path the code under test computes stays inside `tmp_path` by resolving operands and checking `Path.is_relative_to`."
    problem: "Code building output paths from input can escape intended directory (path traversal) and write outside test workspace, causing false passes and disk pollution; resolve both, is_relative_to, no string prefix, symlink safe, traversal fails, contained path."
    use_when: "The code under test computes output paths from input paths and must be proven to stay inside the test workspace."
    avoid_when: "String prefixes (e.g. `str(path).startswith(...)`) are used for containment; symlinks are ignored; the test does not verify path boundaries."
    expected: "Computed output paths are provably contained inside `tmp_path`, and any traversal escapes fail the assertion."
  - anchor: temporary-files-readonly-shared
    what: "Marking session-shared immutable artifacts read-only with `Path.chmod(0o444)` so accidental writes during the suite fail loudly instead of silently corrupting shared state."
    problem: "Session-shared directory documented as immutable can still mutate via buggy test, poisoning later tests without obvious failure at mutation site and producing hard-to-reproduce flakes; chmod read-only, write bits off, fail at mutation, no convention only, no corrupt downstream."
    use_when: "Session-shared immutable artifacts must be protected from accidental writes by filesystem permissions."
    avoid_when: "Convention alone is relied on to keep shared data immutable; files that tests legitimately update are made read-only; accidental writes are allowed to corrupt downstream tests."
    expected: "Shared immutable artifacts are read-only on disk, and any accidental write raises at the mutation site rather than corrupting downstream tests."
---



# TEMPORARY FILES AND DIRECTORIES

## tmp_path (Function-Scoped Per-Test Directory)

[ref: #temporary-files-tmp-path]

The `tmp_path` fixture returns a unique `pathlib.Path` directory for every test invocation.

```python
from pathlib import Path

from faker import Faker


CONFIG_ENCODING = "utf-8"


def test_parser_reads_key_value_file(tmp_path: Path, fake: Faker) -> None:
    """
    Given: key-value config file written to tmp_path.
    When: parser reads the file.
    Then: parsed value matches input.
    """
    # --- Arrange ---
    key = fake.pystr(min_chars=3, max_chars=10)
    value = fake.pystr(min_chars=5, max_chars=20)
    config_file = tmp_path / "config.yaml"
    config_file.write_text(f"{key}: {value}\n", encoding=CONFIG_ENCODING)

    # --- Act ---
    result = YamlConfigParser(str(config_file)).parse()  # provided by project code

    # --- Assert ---
    assert result[key] == value
```

The directory is created under the pytest temporary root and removed automatically according to the configured retention policy.

**Variety booster:** Parametrize the file extension and encoding to exercise parser normalization without duplicating the test body.

## Text and Binary Files

[ref: #temporary-files-text-and-binary]

Create text with `write_text` and binary payloads with `write_bytes`.

```python
from pathlib import Path

from faker import Faker


TEXT_ENCODING = "utf-8"
BINARY_PREFIX = b"\x89PNG\r\n\x1a\n"
CHUNK_SIZE = 1024


def test_text_reader_preserves_content(tmp_path: Path, fake: Faker) -> None:
    """
    Given: text file with generated paragraph.
    When: reader reads the file.
    Then: content is preserved.
    """
    # --- Arrange ---
    payload = fake.paragraph(nb_sentences=fake.pyint(min_value=1, max_value=5))
    text_file = tmp_path / "document.txt"
    text_file.write_text(payload, encoding=TEXT_ENCODING)

    # --- Act ---
    reader = TextReader(text_file)  # provided by project code
    result = reader.read()

    # --- Assert ---
    assert result == payload


def test_binary_reader_detects_magic_bytes(tmp_path: Path, fake: Faker) -> None:
    """
    Given: binary file with PNG magic bytes and random suffix.
    When: binary reader checks magic bytes.
    Then: magic bytes match PNG prefix.
    """
    # --- Arrange ---
    suffix = fake.binary(length=fake.pyint(min_value=8, max_value=64))
    payload = BINARY_PREFIX + suffix
    binary_file = tmp_path / "image.png"
    binary_file.write_bytes(payload)

    # --- Act ---
    reader = BinaryReader(  # provided by project code
        binary_file,
        chunk_size=CHUNK_SIZE,
    )

    # --- Assert ---
    assert reader.magic_bytes() == BINARY_PREFIX
    assert binary_file.read_bytes() == payload
```

Reading back via `read_text` and `read_bytes` keeps assertions focused on content rather than mocks.

**Variety booster:** Generate a list of `(encoding, newline, content_factory)` tuples and parametrize both text and binary readers to cover edge cases such as empty files, multi-byte characters, and trailing newlines with one assertion block.

## Subdirectories and Organization

[ref: #temporary-files-subdirectories]

Use `mkdir` to create named subdirectories under `tmp_path` when a test involves multiple roles such as input, output, and cache.

```python
from pathlib import Path

from faker import Faker


TEXT_ENCODING = "utf-8"


def test_processor_writes_output_beside_input(tmp_path: Path, fake: Faker) -> None:
    """
    Given: input directory with one text file and empty output directory.
    When: processor runs.
    Then: output directory contains upper-cased content.
    """
    # --- Arrange ---
    input_dir = tmp_path / "inputs"
    output_dir = tmp_path / "outputs"
    input_dir.mkdir()
    output_dir.mkdir()
    payload = fake.sentence()
    input_file = input_dir / "source.txt"
    input_file.write_text(payload, encoding=TEXT_ENCODING)

    # --- Act ---
    processor = FileProcessor(input_dir, output_dir)  # provided by project code
    processor.run()

    # --- Assert ---
    output_files = list(output_dir.iterdir())
    assert len(output_files) == 1
    assert output_files[0].read_text(encoding=TEXT_ENCODING) == payload.upper()
```

**Variety booster:** Parametrize the number of input files and the nesting depth so one test validates flat layouts, nested trees, and empty directories.

## tmp_path_factory (Shared or Session Data)

[ref: #temporary-files-tmp-path-factory]

`tmp_path_factory` is session-scoped and returns a `pytest.TempPathFactory`.

```python
from pathlib import Path

import pytest
from faker import Faker


TEXT_ENCODING = "utf-8"
DATASET_PREFIX = "dataset"
MAX_ROWS = 5


@pytest.fixture(scope="session")
def session_faker() -> Faker:
    return Faker()


@pytest.fixture(scope="session")
def shared_dataset_dir(
    tmp_path_factory: pytest.TempPathFactory,
    session_faker: Faker,
) -> Path:
    dataset_dir = tmp_path_factory.mktemp(DATASET_PREFIX)
    row_count = session_faker.pyint(min_value=1, max_value=MAX_ROWS)
    for index in range(row_count):
        file_path = dataset_dir / f"row_{index:03d}.csv"
        file_path.write_text(
            f"{session_faker.uuid4()},{session_faker.word()}\n",
            encoding=TEXT_ENCODING,
        )
    return dataset_dir


def test_dataset_loader_counts_rows(shared_dataset_dir: Path) -> None:
    """
    Given: shared dataset directory with generated CSV rows.
    When: loader counts rows.
    Then: count equals number of files in directory.
    """
    # --- Arrange ---
    loader = CsvLoader(shared_dataset_dir)  # provided by project code

    # --- Act ---
    result = loader.count()

    # --- Assert ---
    assert result == len(list(shared_dataset_dir.iterdir()))
```

**Variety booster:** Combine `tmp_path_factory` with a factory fixture that returns a callable; each call generates a fresh subdirectory under the same session base so shared setup and per-test isolation coexist.

## Factory fixtures for fresh subdirectories

[ref: #temporary-files-factory-fixture]

A fixture can return a callable that mints a fresh subdirectory under one session base on every call.

This keeps an expensive shared parent while giving every caller an isolated workspace.

```python
from collections.abc import Callable
from pathlib import Path

import pytest


ARTIFACT_BASE_PREFIX = "artifacts"


@pytest.fixture(scope="session")
def artifact_base(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return tmp_path_factory.mktemp(ARTIFACT_BASE_PREFIX)


@pytest.fixture
def make_artifact_dir(artifact_base: Path) -> Callable[[str], Path]:
    counter = 0

    def _make(label: str) -> Path:
        nonlocal counter
        counter += 1
        path = artifact_base / f"{label}_{counter}"
        path.mkdir()
        return path

    return _make


def test_factory_yields_isolated_dirs(
    make_artifact_dir: Callable[[str], Path],
) -> None:
    """
    Given: factory fixture that mints subdirectories under one base.
    When: two directories are created with the same label.
    Then: paths differ and share the same parent.
    """
    # --- Arrange ---
    # Factory fixture is provided by the argument.

    # --- Act ---
    first = make_artifact_dir("case")
    second = make_artifact_dir("case")

    # --- Assert ---
    assert first != second
    assert first.parent == second.parent
```

**Variety booster:** Expose the counter through the callable so tests can assert ordering, or accept a `files: dict[str, str]` argument to populate each subdirectory in one call.

## Read-only shared artifacts

[ref: #temporary-files-readonly-shared]

After creating a session-shared artifact that must stay immutable, clear its write bits with `chmod`.

Any accidental write then raises at the mutation site instead of corrupting later tests.

```python
from pathlib import Path

import pytest
from faker import Faker


TEXT_ENCODING = "utf-8"
SHARED_READ_ONLY = 0o444
WRITE_PERMISSION_BITS = 0o222


@pytest.fixture(scope="session")
def session_faker() -> Faker:
    return Faker()


@pytest.fixture(scope="session")
def shared_readonly_file(
    tmp_path_factory: pytest.TempPathFactory,
    session_faker: Faker,
) -> Path:
    file_path = tmp_path_factory.mktemp("readonly") / "seed.txt"
    file_path.write_text(session_faker.sentence(), encoding=TEXT_ENCODING)
    file_path.chmod(SHARED_READ_ONLY)
    return file_path


def test_shared_artifact_is_readable_and_immutable(shared_readonly_file: Path) -> None:
    """
    Given: session-shared read-only artifact.
    When: the file is read and its mode is inspected.
    Then: content is non-empty and no write bits are set.
    """
    # --- Arrange ---
    mode_bits = shared_readonly_file.stat().st_mode

    # --- Act ---
    content = shared_readonly_file.read_text(encoding=TEXT_ENCODING)

    # --- Assert ---
    assert content
    assert (mode_bits & WRITE_PERMISSION_BITS) == 0
```

**Variety booster:** Parametrize over `0o444` and `0o555` to document the difference between read-only files and read-only directories in the shared fixture.

## Legacy tmpdir Avoidance

[ref: #temporary-files-legacy-tmpdir]

Avoid `tmpdir` and `tmpdir_factory` in new code because they return `py.path.local` objects.

```python
from pathlib import Path

from faker import Faker


TEXT_ENCODING = "utf-8"


def test_writer_creates_expected_file(tmp_path: Path, fake: Faker) -> None:
    """
    Given: generated payload and target path in tmp_path.
    When: writer writes the file.
    Then: file contains the payload.
    """
    # --- Arrange ---
    payload = fake.sentence()
    target = tmp_path / "output.txt"

    # --- Act ---
    FileWriter(target).write(payload)  # provided by project code

    # --- Assert ---
    assert target.read_text(encoding=TEXT_ENCODING) == payload
```

No conversion between `py.path.local` and `pathlib.Path` is needed.

**Variety booster:** Add a project-level `addopts = "-p no:legacypath"` entry in `pyproject.toml` and a CI check that greps for `tmpdir` in new test files to prevent regressions.

## Path containment assertions

[ref: #temporary-files-path-containment]

Resolve both paths and assert `is_relative_to` to prove the code under test never escapes `tmp_path`.

```python
from pathlib import Path

from faker import Faker


TEXT_ENCODING = "utf-8"
NESTED_OUTPUT = "nested/output.txt"


def test_writer_stays_inside_tmp_path(tmp_path: Path, fake: Faker) -> None:
    """
    Given: target path nested under tmp_path.
    When: writer creates the file.
    Then: resolved target is contained in tmp_path and content matches.
    """
    # --- Arrange ---
    payload = fake.sentence()
    target = tmp_path / NESTED_OUTPUT

    # --- Act ---
    FileWriter(target).write(payload)  # provided by project code

    # --- Assert ---
    assert target.resolve().is_relative_to(tmp_path.resolve())
    assert target.read_text(encoding=TEXT_ENCODING) == payload
```

**Variety booster:** Parametrize a list of malicious relative inputs such as `"../escape.txt"` and assert the writer either rejects them or the resolved path still stays inside `tmp_path`.

## Retention and CLI Options

[ref: #temporary-files-retention]

pytest automatically cleans up temporary directories and retains the last three invocations by default.

Configure retention in `pyproject.toml` with `tmp_path_retention_count` and `tmp_path_retention_policy`.

```toml
[tool.pytest.ini_options]
tmp_path_retention_count = 3
tmp_path_retention_policy = "failed"
```

Use `--basetemp=mydir` to place all temporary directories under a custom parent directory; pytest removes this directory blindly at the start of the run.

Use `PYTEST_DEBUG_TEMPROOT` to override the system temp root for debugging or sandboxed CI environments.

Concurrent and xdist runs receive unique base temporary directories automatically, so collisions are avoided without manual locks.

The configured policy is readable at runtime through the `request` fixture, which guards against drift between code and config.

```python
import pytest


VALID_RETENTION_POLICIES = ("all", "failed", "none")


def test_retention_policy_is_configured(request: pytest.FixtureRequest) -> None:
    """
    Given: pytest configuration with a retention policy.
    When: the policy is read via request.config.
    Then: value is one of the supported policies.
    """
    # --- Arrange ---
    # The request fixture provides access to the pytest config.

    # --- Act ---
    policy = request.config.getini("tmp_path_retention_policy")

    # --- Assert ---
    assert policy in VALID_RETENTION_POLICIES
```

**Variety booster:** Add a project-specific CLI alias in `pyproject.toml` or a `just` recipe that runs the suite with `--basetemp=.pytest-temp` on demand, making it easy to inspect artifacts after failing tests without changing retention settings.
