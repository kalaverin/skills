---
subject: "Substitute PostgreSQL with `SQLite` at runtime for fast isolated `SQLAlchemy 2.0` async tests: import-time patches (`JSONB`→`JSON`, `Uuid.bind_processor`, `psycopg.errors.UniqueViolation` alias), one function-scoped `db_session` with `NullPool`+`begin_nested` savepoint rollback, strip `postgresql_where` indexes, Faker factories, `flush`+`refresh` (no commit), real `IntegrityError`."
index:
  - anchor: postgres-surrogate-approach
    what: "The runtime substitution of `PostgreSQL` with `SQLite` (real SQL, no mocked repositories, no Docker) for a `SQLAlchemy 2.0` + `psycopg` async production stack, via import-time patches and one scoped-session fixture."
    problem: "Async repositories, services, gRPC servicers hit production `PostgreSQL` through `SQLAlchemy 2.0`, yet full server plus Docker makes every test slow and brittle; mocked repositories test nothing real while Docker per test multiplies startup cost; fast isolated persistence, real sql execution, surrogate engine, no docker, import-time patch, scoped session, savepoint rollback."
    use_when: "Production stack is `SQLAlchemy 2.0` async on `PostgreSQL` with `psycopg`; repository/service/servicer tests need real SQL without a running server; Docker is unavailable or too slow; the goal is fast isolated unit-level persistence tests."
    avoid_when: "Do not use when the test exercises `PostgreSQL`-only behavior (`JSONB` operators, full-text search, ranges, custom types, stored procedures, query plans); route those to a real `PostgreSQL` instead."
    expected: "Database tests run real SQL against `SQLite` with full isolation and no Docker, while truly `PostgreSQL`-specific behavior is reserved for a real database."
  - anchor: postgres-jsonb-to-json
    what: "An import-time swap `pg_dialect.JSONB = sa.JSON`, applied before any model import so every `JSONB` column resolves to `sa.JSON` on `SQLite`."
    problem: "Models declare `sqlalchemy.dialects.postgresql.JSONB` columns at import time, so `metadata.create_all` on `SQLite` raises unsupported type before any test runs; importing models before patch lands silently skips swap and still explodes; column type mismatch, import ordering, dialect type, metadata build, surrogate engine, unsupported construct, schema create."
    use_when: "Models reference `sqlalchemy.dialects.postgresql.JSONB`; tests run on `SQLite`; the patch is placed at the absolute top of `conftest.py` before model modules load."
    avoid_when: "Do not place the patch after model imports (it is silently ignored); do not use this when a test must assert real `JSONB` operator behavior."
    expected: "`metadata.create_all` succeeds on `SQLite` and every `JSONB` column is created as `JSON`, with the original `JSONB` saved for restoration."
  - anchor: postgres-uuid-bind-processor
    what: "A patched `sqltypes.Uuid.bind_processor` that serializes `uuid.UUID` to dashed `str` so `UUID` primary keys match `str` foreign keys inside `SQLite`."
    problem: "SQLAlchemy default `Uuid.bind_processor` serializes `uuid.UUID` into hex without dashes, so foreign-key columns stored as dashed `str` mismatch primary keys on lookups inside `SQLite`; hex versus dashed, identifier serialization, foreign key, primary key, string column, bind processor, join mismatch, identifier format."
    use_when: "Models use `Uuid` columns whose foreign-key counterparts are stored as dashed `str`; lookups or joins compare `uuid.UUID` to `str` on `SQLite`."
    avoid_when: "Do not apply when primary and foreign keys share one representation already; do not forget to restore the original processor after the session."
    expected: "`UUID` values serialize to dashed strings on `SQLite`, joins and lookups match, and the original `bind_processor` is restored at teardown."
  - anchor: postgres-unique-violation-alias
    what: "An alias `psycopg.errors.UniqueViolation = sqlite3.IntegrityError` (guarded by `try/except`) so `isinstance(error.orig, psycopg.errors.UniqueViolation)` succeeds when `psycopg` is absent."
    problem: "Repositories catch `isinstance(error.orig, psycopg.errors.UniqueViolation)` but test run lacks `psycopg` and `SQLite` raises `sqlite3.IntegrityError`, so branch never fires and duplicate handling goes untested; exception alias, dialect-specific error, missing driver, type check, integrity path, error translation, duplicate key, branch coverage."
    use_when: "Production repositories branch on `isinstance(error.orig, psycopg.errors.UniqueViolation)`; the test environment may not install `psycopg`; `SQLite` raises `sqlite3.IntegrityError`."
    avoid_when: "Do not alias unconditionally when `psycopg` is present and its real exception is required; guard with `try/except` and restore the original afterward."
    expected: "Duplicate-key handling branches fire under `SQLite`, the `isinstance` check succeeds, and the original `psycopg.errors.UniqueViolation` is restored."
  - anchor: postgres-restore-patches
    what: "A `_restore_import_time_patches()` helper plus a `session`-scoped `autouse` fixture that restores `JSONB`, `Uuid.bind_processor`, and `psycopg.errors.UniqueViolation` after the run."
    problem: "Import-time swaps mutate global dialect objects for whole run, so leaking patched `JSONB` or `Uuid.bind_processor` past session end corrupts later collection and sibling suites; global singleton, leaked mutation, session teardown, restore original, autouse fixture, cross-suite contamination, saved reference, cleanup hook."
    use_when: "Any import-time patch mutates a global dialect object; the suite shares one Python process with other tests; restoration must run once at session end."
    avoid_when: "Do not skip restoration (leaked globals poison later collection); do not restore `psycopg.errors.UniqueViolation` when its saved original is `None`."
    expected: "Every patched global returns to its saved original at session teardown, so sibling suites and later collection see unmutated dialect objects."
  - anchor: postgres-db-session
    what: "A single `function`-scoped `pytest_asyncio` `db_session` fixture that builds a `SQLite` `AsyncEngine`, overrides `db.get_dsn`/`db.get_ssl_options`, wires `StorageFactory.tr_manager`, runs `create_all`, opens a nested transaction, yields the session, then rolls back and restores every global."
    problem: "One fixture must hand repositories real `AsyncSession` against `SQLite` while bypassing `db.setup()` that would spawn `PostgreSQL` engine, and every patched global plus metadata must restore afterward; session wiring, dsn override, ssl override, setup bypass, transaction manager, metadata restore, global rollback, function scope, leak-free teardown."
    use_when: "Repositories, services, and servicers all need one consistent `AsyncSession`; production code calls `db.setup()`/`db.Session()`; full isolation per test is required."
    avoid_when: "Do not call `db.setup()` inside the fixture or any test (it builds a `PostgreSQL` engine and overwrites the `SQLite` session); do not leak any patched global past `finally`."
    expected: "Each test receives a fresh isolated `AsyncSession` bound to a `SQLite` savepoint, `db.setup()` is bypassed, and all patched globals and metadata are restored in `finally`."
  - anchor: postgres-null-pool
    what: "Creating the `SQLite` engine with `poolclass=sa.pool.NullPool` so each operation opens and closes its own connection against the per-test file."
    problem: "Each test writes fresh `tmp_path` SQLite file, so default connection pool keeps stale descriptors pointing at deleted file and next test reads wrong database; stale handle, per-test file, pool reuse, file descriptor, wrong database, no pooling, ephemeral file, connection lifecycle, fresh file, isolated store."
    use_when: "Each test uses a fresh `tmp_path` database file; the engine must not retain connections across tests; file handles must release immediately."
    avoid_when: "Do not keep a pooled engine bound to a per-test file (stale descriptors cross tests); do not rely on a shared in-memory pool when files rotate."
    expected: "No stale file descriptors leak between tests; every operation uses a fresh connection to the current test's file."
  - anchor: postgres-nested-transaction
    what: "Wrapping each test in `await conn.begin_nested()` (a `SAVEPOINT`) and rolling it back in `finally`, so a test calling `commit` only commits the savepoint and rollback still empties the database."
    problem: "Tables created once per test still need empty start, yet deleting file or re-running `create_all` wastes time, and test calling `commit` would persist data past teardown; savepoint, nested begin, rollback on exit, empty slate, commit isolation, no recreate, data leak, transaction boundary."
    use_when: "Tables are created once per test; production code may call `commit`; isolation must reset state without recreating the file or schema."
    avoid_when: "Do not recreate the file or re-run `create_all` per test (slow); do not rely on the next test to clean up; do not let `commit` escape the savepoint."
    expected: "Every test starts empty, `commit` inside a test only seals the savepoint, and rollback in `finally` leaves a clean slate without recreating schema."
  - anchor: postgres-strip-partial-indexes
    what: "Discarding indexes whose `idx.dialect_options['postgresql']['where']` is set before `create_all`, recording `(table, idx)` pairs, and re-adding them to `table.indexes` in `finally`."
    problem: "Metadata carries partial unique indexes with `postgresql_where` predicate, but `SQLite` grammar lacks `WHERE` inside `CREATE UNIQUE INDEX`, so `create_all` raises syntax error before first assertion; partial index, dialect option, predicate index, metadata singleton, syntax error, index strip, restore metadata, schema build."
    use_when: "Models declare partial unique indexes via `postgresql_where`; `metadata.create_all` runs on `SQLite`; metadata is a global singleton that must not stay corrupted."
    avoid_when: "Do not leave stripped indexes discarded (later tests see incomplete metadata); do not try to create partial indexes on `SQLite`."
    expected: "`create_all` succeeds on `SQLite` without partial-index syntax errors, and every stripped index is restored to metadata in `finally`."
  - anchor: postgres-seeded-fake
    what: "A `session`-scoped `fake` fixture building `Faker([...locales])`, seeding from `randomly_seed` option or `PYTEST_FAKER_SEED` (generating one seed via `random.randint` only when unset), then `fake.seed_instance(seed)`."
    problem: "Factories need reproducible randomized data across locales, but unseeded generator makes flaky snapshots and hardcoded seeds remove entropy when environment variable is absent; seeded instance, locale list, env override, reproducible data, deterministic run, snapshot stability, data seed, unique generator."
    use_when: "Factories and tests draw all data from Faker; runs must be reproducible; an optional seed override arrives via CLI option or environment variable."
    avoid_when: "Do not use stdlib `random` anywhere except the one-time seed initialization; do not hardcode a fixed seed that kills entropy when no override is set."
    expected: "All test data is reproducible under a logged seed, locale coverage is broad, and the only stdlib `random` use is seed initialization."
  - anchor: postgres-model-factories
    what: "Synchronous factory fixtures (`channel_factory`, `contact_factory`) that accept `fake`, return detached (un-persisted) model instances, and fill every non-explicit field from Faker (`fake.unique.*` for unique columns)."
    problem: "Every non-explicit field must come from generator and unique-constrained columns must never collide, yet hardcoded literals or direct `uuid.uuid4()` calls make collisions and non-reproducible runs; detached instance, default generation, unique field, collision free, factory override, seeded data, no literal, domain object."
    use_when: "A model needs many valid instances across tests; fields not under test should vary; unique-constrained columns must not collide."
    avoid_when: "Do not hardcode literals like `'test_user'`; do not call `uuid.uuid4()` or stdlib `random`; do not persist inside the factory (return detached instances)."
    expected: "Factories return valid detached instances with Faker defaults, unique fields never collide, and tests override only the fields they care about."
  - anchor: postgres-add-item
    what: "A generic `add_item(item)` helper that runs `db_session.add(item)` then `await db_session.flush()` then `await db_session.refresh(item)` and intentionally never commits."
    problem: "Helper that persists inside shared session must make row visible and hydrate primary key, but calling `commit` ends savepoint early and leaks row past rollback into sibling tests; flush only, refresh primary key, no commit, nested rollback, visibility inside transaction, hydrated identity, leak prevention, persistence helper."
    use_when: "Tests need a reusable persist helper bound to the shared `db_session`; rows must be visible and have hydrated primary keys within the savepoint."
    avoid_when: "Do not call `commit` inside helper fixtures (breaks nested-transaction isolation); do not skip `refresh` when the test reads generated primary keys."
    expected: "Persisted rows are visible and hydrated inside the savepoint, no commit leaks data, and rollback removes everything after the test."
  - anchor: postgres-sample-fixtures
    what: "Async composite `sample_*` fixtures (e.g. `sample_channels`) that build a canonical dataset via `add_item` + factories, rebuilt fresh per test from the empty database."
    problem: "Many tests share canonical dataset rebuilt per test from empty database, yet fixed identifiers like channel names are domain concepts while every other field must stay generated; composite fixture, canonical dataset, fixed domain name, generated default, autowired build, per-test rebuild, named entity, shared arrangement."
    use_when: "Many tests share a canonical starting dataset; the database is empty at each test start; a few identifiers are fixed domain concepts referenced by name."
    avoid_when: "Do not extend the fixed-name exception beyond true domain concepts (channel types, roles, statuses); every other field must use Faker defaults."
    expected: "Each test gets a fresh canonical dataset, fixed domain names are stable for named lookup, and all non-domain fields remain generated."
  - anchor: postgres-repository-tests
    what: "Repository tests that wrap `db_session` in `PostgresStorage(...).contact_repo()` and assert on persisted entities, executing real SQL against `SQLite`."
    problem: "Repository method needs real SQL executed against surrogate through wrapped session, but mocking repository would test mock instead of mapping, joins, and constraint behavior; direct storage, real query, repository wrap, session injection, mapping fidelity, no mock repo, join behavior, persistence outcome, read model, write path, round trip."
    use_when: "The target is a repository method; mapping, joins, and constraint behavior matter; real SQL against `SQLite` can exercise it."
    avoid_when: "Do not mock the repository (tests the mock, not the SQL); do not assert on driver internals like `rowcount`."
    expected: "Repository methods are exercised by real SQL against `SQLite`, asserting on domain outcomes rather than driver-internal state."
  - anchor: postgres-service-tests
    what: "Service tests that instantiate the service with no explicit session and rely on the patched `StorageFactory`/`TransactionManager` to route `db.Session()` to the `SQLite` session."
    problem: "Service resolves session through `StorageFactory` and `TransactionManager` rather than explicit argument, so unpatched factory would hand it production session and bypass surrogate entirely; factory wiring, hidden session, transaction manager, service layer, implicit dependency, surrogate routing, no argument, integration seam, context bound, factory swap."
    use_when: "The service pulls its session from `StorageFactory`/`TransactionManager`; the fixture already wired `tr_manager` and `db.Session` to `SQLite`."
    avoid_when: "Do not leave `StorageFactory.tr_manager` unpatched (service reaches production); do not pass a session explicitly when the service resolves it implicitly."
    expected: "Services resolve the `SQLite` session transparently through the patched factory, with no production session leaking in."
  - anchor: postgres-grpc-servicer
    what: "gRPC servicer tests that call handler methods directly with a protobuf request and an `AsyncMock` context, exercising the service→`StorageFactory`→`SQLite` chain end-to-end without a running server."
    problem: "gRPC servicer chains service into `StorageFactory` into surrogate, so full request path runs without server while only external context stands as `AsyncMock` stub; end-to-end servicer, request response, context stub, no running server, service chain, surrogate backend, rpc handler, transport-free, unary call, populated message, handler entry."
    use_when: "The target is a gRPC servicer; the only external dependency is the RPC context; the data path runs through `StorageFactory` into `SQLite`."
    avoid_when: "Do not start a real gRPC server; do not mock repositories or services beneath the servicer (only the context is mocked)."
    expected: "Servicer handlers run end-to-end against `SQLite` with only the context mocked, returning populated responses without a server."
  - anchor: postgres-unique-constraint
    what: "Two ways to assert duplicate handling: trigger a real `IntegrityError` by inserting duplicates for non-partial `UNIQUE` columns, or patch `session.flush` to raise for partial-index violations `SQLite` cannot enforce."
    problem: "Plain `UNIQUE` column enforced by `SQLite` must raise real `IntegrityError` on duplicate insert, but broad `except` or wrong type hides regression and lets duplicate through; real constraint, duplicate insert, integrity error, explicit exception, match pattern, no broad catch, uniqueness enforcement, regression signal, database enforced, raised natively."
    use_when: "The constraint is a plain (non-partial) `UNIQUE` column that `SQLite` enforces natively; the test inserts genuine duplicates and asserts the raised error type."
    avoid_when: "Do not catch broadly or assert a wrong exception type; do not mock `flush` for constraints `SQLite` can enforce for real."
    expected: "Non-partial uniqueness is asserted via a real `IntegrityError` from `SQLite`, with explicit type and `match=`."
  - anchor: postgres-unique-constraint
    what: "For partial-index violations only, `mocker.patch.object(repo._session, 'flush', ...)` to raise `IntegrityError(orig=sqlite3.IntegrityError(...))` so the repository maps it to a domain `AlreadyExistsError`."
    problem: "Partial unique index stripped for `SQLite` cannot fire real violation, so repository mapping from integrity error to domain `AlreadyExistsError` stays unreachable unless `session.flush` is patched to raise; partial predicate, unenforceable constraint, flush patch, domain error mapping, simulated violation, translation path, fallback only, last resort, mapped exception, surrogate gap."
    use_when: "The violated constraint is a partial unique index that `SQLite` cannot enforce; the repository's error-to-domain mapping must still be covered."
    avoid_when: "Do not use mock-flush for non-partial constraints (insert real duplicates instead); treat mock-flush strictly as a last-resort fallback."
    expected: "Partial-index violation paths are covered by a narrowly patched `flush` that raises the exact integrity error, verifying the domain-error mapping."
  - anchor: postgres-assert-domain
    what: "Plain `assert` on domain meaning (status, generated timestamps, entity equality), never `self.assert*` and never driver-internal state like `result.rowcount`."
    problem: "Assertion on `result.rowcount` or other driver-internal state ties test to surrogate rather than behavior, so passing suite can still hide broken business outcome; domain meaning, business outcome, internal state, driver detail, status field, generated timestamp, no rowcount, behavior assertion, user-visible result, invariant check."
    use_when: "Assertions describe the business outcome (entity fields, status, timestamps, equality); the test reads like a domain invariant."
    avoid_when: "Do not use `self.assertEqual`/`assertTrue`/`assertRaises`; do not assert on `rowcount` or other `SQLite`-internal state."
    expected: "Tests read as domain invariants, use plain `assert`, and stay independent of surrogate-internal driver details."
  - anchor: postgres-factory-overrides
    what: "Passing only the specific field under test to the factory (e.g. `contact_factory(status=ContactStatus.INACTIVE)`) and letting Faker fill every other field."
    problem: "Single test needs one specific field set while remaining fields should vary, but hardcoding every column removes randomness and masks collision or formatting bugs; explicit override, partial literal, generated rest, one field, vary remainder, no full literal, targeted value, entropy preserved, domain enum, fixed status, boundary input, named argument, selective control."
    use_when: "A test cares about one field (a status, a flag, a boundary value); all other fields should remain generated and varied."
    avoid_when: "Do not hardcode every field (removes entropy, hides collisions); do not bypass the factory to hand-build instances inline."
    expected: "Each test pins exactly the field it cares about and keeps Faker variety everywhere else, preserving entropy and collision coverage."
  - anchor: postgres-time-control
    what: "Freezing the clock with `time_machine.travel(instant, tick=False)` (or `freezegun` as fallback) around `created_at`/`updated_at`/expiry logic, never `time.sleep`/`asyncio.sleep`."
    problem: "Expiry and timestamp logic depends on frozen clock, but `time.sleep` or `asyncio.sleep` slows suite and real clock makes past-and-future assertions nondeterministic; frozen time, clock travel, tick false, expiry check, deterministic instant, no sleep, timestamp logic, clock library, created at, past future."
    use_when: "Logic depends on `created_at`/`updated_at`/expiry; past and future instants must be asserted deterministically within one test."
    avoid_when: "Do not use `time.sleep` or `asyncio.sleep`; do not rely on the real wall clock for time-sensitive assertions."
    expected: "Time-sensitive assertions are deterministic and fast, driven by an explicit frozen instant with `tick=False`."
  - anchor: postgres-zero-warnings
    what: "Running with warnings as errors (`-W error::DeprecationWarning -W error::ResourceWarning`), fixing root causes, and allowing only a single narrow `warnings.filterwarnings(...)` with an upstream-ticket comment when unavoidable."
    problem: "Suite output must carry zero warnings, yet `ResourceWarning` from unclosed engine or `PytestUnknownMarkWarning` from unregistered marker slips in unless treated as error and fixed at root; warnings as errors, resource leak, unknown mark, root cause, narrow filter, upstream ticket, no blanket ignore, clean output, deprecation fix, registered marker."
    use_when: "The suite enforces a zero-warnings policy; leaks, unknown marks, and deprecations must be fixed at the source rather than silenced."
    avoid_when: "Do not use blanket `warnings.filterwarnings('ignore')` or `pytest.mark.filterwarnings('ignore')`; do not suppress without exact class, module regex, and a ticket link."
    expected: "Test output contains zero warnings; any unavoidable warning is filtered by exact class and module with a documented upstream reference."
  - anchor: postgres-anti-patterns
    what: "A review checklist of forbidden surrogate moves (import order, `commit` in helpers, un-restored `tr_manager`, discarded indexes, `random`/`uuid`/literals, mock-flush for non-partial constraints, `db.setup()`, `gc.collect()` instead of real cleanup)."
    problem: "Reviewing surrogate setup for isolation leaks or corrupted metadata needs checklist of forbidden moves, because one missed restore or stray `commit` silently breaks every later test; review checklist, forbidden move, isolation leak, metadata corruption, missed restore, stray commit, zero tolerance, regression hunt, shared state, hardcoded dsn."
    use_when: "Reviewing or refactoring a surrogate `conftest`; hunting for isolation leaks, corrupted metadata, or production-session leakage."
    avoid_when: "Do not treat any listed anti-pattern as acceptable; do not rely on `gc.collect()` as a substitute for explicit `close()`/`dispose()`."
    expected: "Every listed anti-pattern is absent: patches precede imports, helpers never commit, all globals and indexes restore, and cleanup is explicit."
  - anchor: postgres-troubleshooting
    what: "A symptom→cause→fix map for recurring surrogate failures (`JSONB` unsupported, UUID mismatch, missing `psycopg.errors`, partial-index syntax, DSN/SSL leakage, second engine, data leak, scoped-session bind, `database is locked`, `ResourceWarning`)."
    problem: "Failure symptom like `database is locked` or UUID mismatch needs fast map to cause and fix, because guessing wastes cycles and same errors recur across projects adopting surrogate; symptom table, root cause, fix lookup, locked database, type mismatch, dsn leak, diagnostic map, recurring error, quick triage, known failure."
    use_when: "A test failure matches a known surrogate symptom; the goal is fast triage to root cause and the matching fix."
    avoid_when: "Do not guess at causes; do not paper over symptoms with broad ignores instead of applying the mapped fix."
    expected: "Each listed symptom resolves by applying its mapped root-cause fix, restoring green, isolated surrogate tests."
  - anchor: postgres-adapt-pattern
    what: "A five-step port: audit models for dialect-only constructs, place import-time patches first in `conftest.py`, implement `db_session`, write helper fixtures, then decide real-vs-mock for `IntegrityError`."
    problem: "Porting surrogate to another codebase requires auditing models for dialect-only constructs before writing fixtures, because missed `ARRAY` or `INET` column or extra partial index surfaces only at `create_all`; port steps, model audit, dialect construct, index scan, fixture rebuild, project transfer, adaptation order, pre-flight scan, column inventory, extension check."
    use_when: "Adopting the surrogate pattern in a new `SQLAlchemy 2.0` + `PostgreSQL` project; models may use `JSONB`/`ARRAY`/`INET`/`CIDR`, partial indexes, or `psycopg.errors`."
    avoid_when: "Do not write fixtures before auditing models (missed dialect constructs explode at `create_all`); do not skip the per-construct patch decision."
    expected: "The new project gets a working surrogate `conftest` whose patches cover every dialect-only construct found in the model audit."
  - anchor: postgres-copy-paste-template
    what: "The copy-ready asset `assets/pgsql.py` — a `tests/conftest.py` skeleton ordering import-time patches, model-loading imports, `fake`, `db_session`, and `add_item`, with every save/restore wired."
    problem: "Bootstrapping new project needs single conftest skeleton with every patch and fixture in right order, because assembling from scratch risks patch-after-import or missing restore that corrupts run; starter skeleton, conftest order, patch first, fixture block, restore hook, bootstrap file, copy template, wiring order, ready scaffold, minimal edit."
    use_when: "Starting a surrogate test suite from scratch; the patches, model imports, and fixtures must be in the correct relative order."
    avoid_when: "Do not import model modules before the import-time patches; do not omit any save/restore pair from the skeleton."
    expected: "A drop-in `conftest.py` skeleton compiles, patches precede model imports, and every global is saved and restored."
libraries:
  - aiosqlite
  - freezegun
  - psycopg
  - pytest-asyncio
  - pytest-mock
  - sqlalchemy
  - time-machine
---

# POSTGRESQL TESTING VIA SQLITE SURROGATE

Activate this file when testing repositories, services, or gRPC servicers against a `SQLAlchemy 2.0` + `psycopg` async `PostgreSQL` stack by substituting `SQLite` at runtime.

## Surrogate Approach and Absolute Constraints

[ref: #postgres-surrogate-approach]

Use `SQLite` as a runtime surrogate for `PostgreSQL`: execute real SQL against an in-memory or `tmp_path` `SQLite` database shaped by import-time patches and one scoped-session fixture. Never mock repositories or storage layers; never spin up `PostgreSQL`; never require Docker.

Bind every test to a single `function`-scoped `db_session` that builds a fresh `SQLite` engine, patches `db.get_dsn`/`db.get_ssl_options`, wires `StorageFactory.tr_manager`, strips partial indexes, runs `create_all`, opens a nested transaction, yields the session, then rolls back and restores every global in `finally`.

Honor the absolute constraints: no mocked repositories; no hardcoded test data (Faker factories only, `fake.unique` for unique columns); no stdlib `random` except seed initialization; no `commit` inside helper fixtures (`flush` + `refresh` only); no bare `except`; no `db.setup()` in tests or fixtures; restore every patched global and every stripped index; strip `postgresql_where` indexes before `create_all`; keep import-time patches at the top of `conftest.py`; no `time.sleep`/`asyncio.sleep`; no `print()`; zero warnings.

**Variety booster:** Treat the constraints as a review gate: when adding a new repository, service, or servicer test, run the same surrogate fixture unchanged and vary only the factory overrides and assertions, so one fixture covers many domains.

## JSONB to JSON Patch

[ref: #postgres-jsonb-to-json]

Patch `sqlalchemy.dialects.postgresql.JSONB` to `sa.JSON` at the absolute top of `conftest.py`, before any model module is imported, because SQLAlchemy constructs `Column`/`mapped_column` objects at import time. Save the original for restoration.

Apply the patch before models load:

```python
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg_dialect

_ORIG_JSONB = pg_dialect.JSONB
pg_dialect.JSONB = sa.JSON
```

Wrong — patch after model import is silently ignored:

```python
from app import models  # JSONB columns already constructed

pg_dialect.JSONB = sa.JSON  # too late: create_all still sees JSONB
```

**Variety booster:** When a project also uses `ARRAY`/`INET`/`CIDR`, save and swap them in the same block so one patch prelude covers every dialect-only type.

## UUID bind_processor Patch

[ref: #postgres-uuid-bind-processor]

Patch `sqltypes.Uuid.bind_processor` so `uuid.UUID` serializes to a dashed string matching `str` foreign keys on `SQLite`. Save the original processor and restore it at teardown.

Serialize `UUID` to dashed string:

```python
import uuid

from sqlalchemy.sql import sqltypes

_ORIG_UUID_BIND_PROCESSOR = sqltypes.Uuid.bind_processor


def _patched_uuid_bind_processor(self, dialect):
    def process(value):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, uuid.UUID):
            return str(value)
        return value
    return process


sqltypes.Uuid.bind_processor = _patched_uuid_bind_processor
```

**Variety booster:** Cover `None`, `str`, and `uuid.UUID` inputs in one processor so mixed key representations round-trip through a single patch.

## psycopg UniqueViolation Alias

[ref: #postgres-unique-violation-alias]

Alias `psycopg.errors.UniqueViolation` to `sqlite3.IntegrityError` inside a `try/except`, so repository `isinstance(error.orig, psycopg.errors.UniqueViolation)` checks succeed when `psycopg` is not installed and `SQLite` raises `sqlite3.IntegrityError`. Save the original and restore only when it was captured.

Alias the exception safely:

```python
import sqlite3

try:
    import psycopg.errors
    _ORIG_PSYCOPG_UNIQUE_VIOLATION = psycopg.errors.UniqueViolation
    psycopg.errors.UniqueViolation = sqlite3.IntegrityError
except Exception:
    _ORIG_PSYCOPG_UNIQUE_VIOLATION = None
```

**Variety booster:** Extend the same guarded-alias pattern to other `psycopg.errors` members a repository inspects, keeping one `try/except` per alias.

## Restore Import-Time Patches

[ref: #postgres-restore-patches]

Centralize restoration in `_restore_import_time_patches()` and call it from a `session`-scoped `autouse` fixture so patched globals return to their originals exactly once at the end of the run.

Restore every saved original:

```python
def _restore_import_time_patches() -> None:
    pg_dialect.JSONB = _ORIG_JSONB
    sqltypes.Uuid.bind_processor = _ORIG_UUID_BIND_PROCESSOR
    if _ORIG_PSYCOPG_UNIQUE_VIOLATION is not None:
        psycopg.errors.UniqueViolation = _ORIG_PSYCOPG_UNIQUE_VIOLATION


@pytest.fixture(scope="session", autouse=True)
def _restore_patches_after_session() -> None:
    yield
    _restore_import_time_patches()
```

Bad — restoring a `None` original overwrites a real driver class:

```python
psycopg.errors.UniqueViolation = _ORIG_PSYCOPG_UNIQUE_VIOLATION  # None wipes the real class
```

Good — guard the restore:

```python
if _ORIG_PSYCOPG_UNIQUE_VIOLATION is not None:
    psycopg.errors.UniqueViolation = _ORIG_PSYCOPG_UNIQUE_VIOLATION
```

**Variety booster:** Register the autouse restore once per `conftest` layer so nested suites each clean up their own import-time patches.

## The `db_session` Fixture

[ref: #postgres-db-session]

Use one `function`-scoped `pytest_asyncio` `db_session` fixture as the single source of truth. It builds a `SQLite` `AsyncEngine` with `NullPool`, overrides `db.get_dsn`/`db.get_ssl_options`, wires `StorageFactory.tr_manager` to bypass `db.setup()`, strips partial indexes, runs `create_all`, opens a nested transaction, binds `db.Session` to the nested session, yields it, then rolls back and restores every global and index in `finally`.

The canonical fixture:

```python
import gc
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app import storages
from app.storages import sqlalchemy_postgres
from app.storages.sqlalchemy_postgres import db


@pytest_asyncio.fixture(scope="function")
async def db_session(tmp_path: Any) -> AsyncGenerator[AsyncSession, None]:
    db_path = tmp_path / "test.db"
    dsn = f"sqlite+aiosqlite:///{db_path}"
    engine = create_async_engine(dsn, poolclass=sa.pool.NullPool)

    orig_get_dsn = db.get_dsn
    orig_get_ssl = db.get_ssl_options
    orig_session = db.Session
    orig_tr_manager = storages.StorageFactory.tr_manager

    db.get_dsn = lambda: dsn
    db.get_ssl_options = dict

    from app.storages.sqlalchemy_postgres.transaction_manager import TransactionManager
    storages.StorageFactory.tr_manager = TransactionManager()

    stripped_indexes: list[tuple[Any, Any]] = []
    for table in sqlalchemy_postgres.BaseModel.metadata.tables.values():
        for idx in list(table.indexes):
            if idx.dialect_options.get("postgresql", {}).get("where") is not None:
                stripped_indexes.append((table, idx))
                table.indexes.discard(idx)

    async with engine.begin() as conn:
        await conn.run_sync(sqlalchemy_postgres.BaseModel.metadata.create_all)
        nested_trans = await conn.begin_nested()
        session_maker = async_sessionmaker(bind=conn, expire_on_commit=False)
        session = session_maker()
        db.Session = lambda: session

        try:
            yield session
        finally:
            await nested_trans.rollback()
            await session.close()
            await engine.dispose()

            db.Session = orig_session
            db.get_dsn = orig_get_dsn
            db.get_ssl_options = orig_get_ssl
            storages.StorageFactory.tr_manager = orig_tr_manager

            for table, idx in stripped_indexes:
                table.indexes.add(idx)

            gc.collect()
```

Bad — calling `db.setup()` rebuilds a `PostgreSQL` engine and overwrites the `SQLite` session:

```python
await db.setup()  # spawns psycopg engine, destroys the surrogate session
```

Good — bypass `db.setup()` by wiring `TransactionManager` directly:

```python
storages.StorageFactory.tr_manager = TransactionManager()
```

**Variety booster:** Keep this fixture unchanged across repository, service, and servicer tests; vary only downstream factories and assertions so one wiring covers the whole data layer.

## NullPool for Per-Test SQLite Files

[ref: #postgres-null-pool]

Create the engine with `poolclass=sa.pool.NullPool` when each test owns a fresh `tmp_path` file. A pooled engine holds file descriptors that outlive the test file, so the next test can read a stale handle against a deleted path.

Bind the engine to the per-test file with no pooling:

```python
engine = create_async_engine(dsn, poolclass=sa.pool.NullPool)
```

**Variety booster:** Pair `NullPool` with `tmp_path / "test.db"` so file rotation and connection release stay aligned across every test.

## Nested Transaction (Savepoint) Isolation

[ref: #postgres-nested-transaction]

Wrap each test in `await conn.begin_nested()` (a `SAVEPOINT`) and roll it back in `finally`. Tables are created once per test; the test runs inside the savepoint; on exit the savepoint rolls back and leaves the database empty. If production code calls `commit`, SQLAlchemy commits only the savepoint, so rollback still works.

Open and roll back the savepoint:

```python
async with engine.begin() as conn:
    await conn.run_sync(sqlalchemy_postgres.BaseModel.metadata.create_all)
    nested_trans = await conn.begin_nested()
    session_maker = async_sessionmaker(bind=conn, expire_on_commit=False)
    session = session_maker()
    try:
        yield session
    finally:
        await nested_trans.rollback()
        await session.close()
```

**Variety booster:** Cover tests that call `commit`, tests that call `rollback`, and tests that do neither with the same savepoint wrapper; all three leave an empty database.

## Strip and Restore Partial Indexes

[ref: #postgres-strip-partial-indexes]

Discard indexes carrying a `postgresql_where` predicate before `create_all`, record `(table, idx)` pairs, and re-add them in `finally`. Metadata is a global singleton: leaving indexes discarded corrupts later tests that inspect `metadata.tables`.

Strip, record, and restore:

```python
stripped_indexes: list[tuple[Any, Any]] = []
for table in sqlalchemy_postgres.BaseModel.metadata.tables.values():
    for idx in list(table.indexes):
        if idx.dialect_options.get("postgresql", {}).get("where") is not None:
            stripped_indexes.append((table, idx))
            table.indexes.discard(idx)
# ... run create_all and the test ...
for table, idx in stripped_indexes:
    table.indexes.add(idx)
```

Bad — discarding without restoring corrupts the metadata singleton:

```python
table.indexes.discard(idx)  # later tests see incomplete indexes
```

Good — restore in `finally`:

```python
for table, idx in stripped_indexes:
    table.indexes.add(idx)
```

**Variety booster:** Detect partial indexes by `idx.dialect_options.get("postgresql", {})` so the same loop also catches `postgresql_using`/`postgresql_ops` when a project adopts them.

## Seeded `fake` Fixture

[ref: #postgres-seeded-fake]

Build one `session`-scoped `Faker` with a locale list, seed from the `randomly_seed` option or `PYTEST_FAKER_SEED`, and generate a seed via `random.randint` only when neither is set. Log the seed for reproducibility.

Seed the shared Faker:

```python
import logging
import os
import random

import pytest
from faker import Faker


@pytest.fixture(scope="session")
def fake(pytestconfig: pytest.Config) -> Faker:
    fake = Faker(["en_US", "ja_JP", "de_DE"])
    seed = getattr(pytestconfig.option, "randomly_seed", None)
    if seed is None:
        seed = int(os.environ.get("PYTEST_FAKER_SEED", random.randint(0, 2**32)))
        logging.getLogger("faker").info("Faker seed: %s", seed)
    fake.seed_instance(seed)
    return fake
```

**Variety booster:** Add locales to the `Faker([...])` list to widen character coverage (CJK, umlauts) while one seed still reproduces the whole run.

## Model Factories

[ref: #postgres-model-factories]

Write synchronous factory fixtures that accept `fake` and return detached (un-persisted) instances. Every non-explicit field must come from Faker; use `fake.unique.*` for unique-constrained columns; never use `random`, `uuid.uuid4()`, or hardcoded literals.

A Faker-driven detached factory:

```python
from typing import Any

import pytest
from faker import Faker

from app import models


@pytest.fixture
def channel_factory(fake: Faker):
    def create_channel(
        name: str | None = None,
        is_editable: bool = True,
        contact_scheme: dict[str, Any] | None = None,
        flow: dict[str, Any] | None = None,
    ) -> models.Channel:
        return models.Channel(
            name=name or fake.unique.company(),
            contact_scheme=contact_scheme or {},
            flow=flow or {},
            is_editable=is_editable,
        )
    return create_channel
```

Bad — hardcoded literals collide and are non-reproducible:

```python
models.Channel(name="test_user", contact_scheme={}, flow={})
```

Good — Faker defaults with an explicit override only where the test cares:

```python
channel_factory(name="web", is_editable=False)
```

**Variety booster:** Expose every column as a keyword defaulting to `None` and resolve `None` to a Faker provider, so one factory serves minimal and fully-specified cases.

## `add_item` Helper (flush + refresh, no commit)

[ref: #postgres-add-item]

Persist through a generic `add_item(item)` that runs `add` → `flush` → `refresh` and never commits. `flush` makes the row visible inside the savepoint; `refresh` hydrates generated primary keys; the outer `finally` rolls back.

The helper fixture:

```python
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture
def add_item(db_session: AsyncSession):
    async def _factory(item):
        db_session.add(item)
        await db_session.flush()
        await db_session.refresh(item)
        return item
    return _factory
```

Bad — committing inside the helper breaks isolation:

```python
await db_session.commit()  # ends the savepoint; data leaks past rollback
```

Good — flush and refresh only:

```python
await db_session.flush()
await db_session.refresh(item)
```

**Variety booster:** Reuse `add_item` for single entities and for batches (`await asyncio.gather(*(add_item(x) for x in items))`) so one helper covers scalar and bulk seeding.

## Composite `sample_*` Fixtures

[ref: #postgres-sample-fixtures]

Build canonical datasets with async `sample_*` fixtures that wire factories through `add_item`. They are `function`-scoped, so the empty database is repopulated fresh per test. Fixed string identifiers are allowed only for true domain concepts (channel types, roles, statuses); every other field must stay generated.

A composite canonical fixture:

```python
import pytest_asyncio

from app import models


@pytest_asyncio.fixture
async def sample_channels(add_item, channel_factory):
    web = await add_item(channel_factory(name="web", is_editable=False))
    email = await add_item(channel_factory(name="email", is_editable=True))
    return web, email
```

**Variety booster:** Parametrize the canonical set (roles × statuses) by stacking `sample_*` fixtures, so downstream tests inherit richer datasets without rewriting seeding logic.

## Repository Tests

[ref: #postgres-repository-tests]

Wrap `db_session` in `PostgresStorage(...).contact_repo()` and assert on persisted entities. All SQL executes against `SQLite`; never mock the repository.

Direct repository test:

```python
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app import domain
from app.storages import PostgresStorage


@pytest_asyncio.fixture
async def repo(db_session: AsyncSession):
    yield PostgresStorage(db_session).contact_repo()


@pytest.mark.asyncio
async def test_get_contact_by_id_returns_matching_contact(
    repo: PostgresStorage,
    sample_contacts: tuple[domain.Contact, domain.Contact],
) -> None:
    """
    Given: two persisted contacts.
    When: the repository fetches one by id.
    Then: the returned contact matches by id and status.
    """
    # --- Arrange ---
    web_contact, _ = sample_contacts

    # --- Act ---
    result = await repo.get(web_contact.id)

    # --- Assert ---
    assert result.id == web_contact.id
    assert result.status == domain.ContactStatus.ACTIVE
```

**Variety booster:** Parametrize over `ContactStatus` and re-fetch, so one repository test covers every persisted status with the same assertions.

## Service Tests

[ref: #postgres-service-tests]

Instantiate the service with no explicit session and let it resolve `db.Session()` through the patched `StorageFactory`/`TransactionManager`. No session handling appears in the test.

Service test through `StorageFactory`:

```python
import pytest

from app.services import ChannelService


@pytest.mark.asyncio
async def test_get_channel_by_name_returns_matching_channel(
    db_session,
    sample_channels,
) -> None:
    """
    Given: canonical channels persisted via the surrogate session.
    When: the service looks one up by name with no explicit session.
    Then: the returned channel matches the named domain concept.
    """
    # --- Arrange ---
    service = ChannelService()

    # --- Act ---
    channel = await service.get(name="web")

    # --- Assert ---
    assert channel.name == "web"
    assert channel.is_editable is False
```

**Variety booster:** Drive the same service with different canonical `sample_*` fixtures to cover read paths that resolve sessions implicitly.

## gRPC Servicer Tests

[ref: #postgres-grpc-servicer]

Call handler methods directly with a protobuf request and an `AsyncMock` context. The servicer chains into services → `StorageFactory` → `SQLite`; only the RPC context is mocked.

End-to-end servicer test without a server:

```python
from unittest.mock import AsyncMock

import pytest

from app import contact_pb2


@pytest.mark.asyncio
async def test_get_contact_returns_populated_response(
    contact_servicer,
    sample_contacts,
) -> None:
    """
    Given: a persisted contact and a mocked RPC context.
    When: the servicer handles GetContact end-to-end.
    Then: the response carries the persisted contact fields.
    """
    # --- Arrange ---
    web_contact, _ = sample_contacts
    mock_context = AsyncMock()
    request = contact_pb2.GetContactRequest(id=web_contact.id)

    # --- Act ---
    response = await contact_servicer.GetContact(request, mock_context)

    # --- Assert ---
    assert response.contact.id == web_contact.id
    assert response.contact.address == web_contact.address
```

**Variety booster:** Parametrize request variants (found, missing id, invalid id) so one servicer test exercises success and error branches through the same chain.

## Testing Unique-Constraint Violations

[ref: #postgres-unique-constraint]

For non-partial `UNIQUE` columns, insert genuine duplicates and assert the real `IntegrityError` that `SQLite` raises. For partial-index violations that `SQLite` cannot enforce (because partial indexes are stripped), patch `session.flush` to raise and assert the repository maps it to a domain error. Use mock-flush only as a last resort.

Real `IntegrityError` for a non-partial unique column:

```python
import pytest
import sqlalchemy as sa


@pytest.mark.asyncio
async def test_create_contact_fails_on_duplicate_email(
    db_session,
    add_item,
    contact_factory,
) -> None:
    """
    Given: a contact with a unique email already persisted.
    When: another contact with the same email is added.
    Then: a real IntegrityError is raised by the database.
    """
    # --- Arrange ---
    email = "alice@example.test"
    await add_item(contact_factory(email=email))
    duplicate = contact_factory(email=email)

    # --- Act / Assert ---
    with pytest.raises(sa.exc.IntegrityError):
        await add_item(duplicate)
```

Mock-flush fallback for a partial-index violation only:

```python
import sqlite3

import pytest
import sqlalchemy as sa

from app import domain, errors


@pytest.mark.asyncio
async def test_create_contact_raises_already_exists_on_unique_violation(
    repo,
    sample_user,
    sample_channels,
    mocker,
) -> None:
    """
    Given: a repository whose flush raises a partial-index integrity error.
    When: create is called with colliding data.
    Then: the repository maps the error to AlreadyExistsError.
    """
    # --- Arrange ---
    async def _fake_flush() -> None:
        raise sa.exc.IntegrityError(
            "stmt", {}, orig=sqlite3.IntegrityError("UNIQUE constraint failed")
        )
    mocker.patch.object(repo._session, "flush", _fake_flush)

    # --- Act / Assert ---
    with pytest.raises(errors.AlreadyExistsError):
        await repo.create(
            user_id=sample_user.id,
            channel_id=sample_channels[0].id,
            address="dup@example.test",
            meta={},
            status=domain.ContactStatus.ACTIVE,
        )
```

Bad — mocking `flush` for a constraint `SQLite` enforces for real:

```python
mocker.patch.object(repo._session, "flush", _fake_flush)  # tests the mock, not the DB
```

Good — insert duplicates and let `SQLite` raise:

```python
with pytest.raises(sa.exc.IntegrityError):
    await add_item(duplicate)
```

**Variety booster:** Parametrize the colliding field (email, slug, phone) and pair each with the matching `match=` regex so one test family covers every real unique constraint.

## Assert on Domain Meaning

[ref: #postgres-assert-domain]

Use plain `assert` on domain outcomes: entity fields, status, generated timestamps, and equality. Never use `self.assert*`, and never assert on driver-internal state such as `result.rowcount`.

Domain-meaning assertions:

```python
# --- Assert ---
assert contact.status == domain.ContactStatus.ACTIVE
assert contact.created_at is not None
```

Bad — asserting on surrogate-internal state:

```python
assert result.rowcount == 1
```

Good — asserting on business outcome:

```python
assert contact.status == domain.ContactStatus.ACTIVE
```

**Variety booster:** Bundle related domain invariants into one assertion body (status + timestamp + equality) so a single test pins one business outcome end to end.

## Factory Overrides

[ref: #postgres-factory-overrides]

Pass only the field under test to the factory and let Faker fill the rest. Hardcoding every column removes entropy and hides collision or formatting bugs.

One explicit field, the rest generated:

```python
inactive = await add_item(
    contact_factory(status=domain.ContactStatus.INACTIVE)
)
```

Bad — every field hardcoded:

```python
inactive = await add_item(
    contact_factory(name="test", email="test@test.test", status=domain.ContactStatus.INACTIVE)
)
```

Good — single override, Faker remainder:

```python
inactive = await add_item(contact_factory(status=domain.ContactStatus.INACTIVE))
```

**Variety booster:** Parametrize the overridden field across a `StrEnum` so one test pins each status while all other columns stay generated.

## Time Control

[ref: #postgres-time-control]

Freeze the clock with `time_machine.travel(instant, tick=False)` (or `freezegun` as a fallback) around `created_at`/`updated_at`/expiry logic. Never use `time.sleep` or `asyncio.sleep`.

Deterministic expiry assertion:

```python
import time_machine
import pytest


@pytest.mark.asyncio
async def test_subscription_is_expired_for_past_date(
    db_session,
    add_item,
    subscription_factory,
    repo,
) -> None:
    """
    Given: a subscription created in the past.
    When: the clock travels past its expiry.
    Then: the repository reports it as expired.
    """
    # --- Arrange ---
    with time_machine.travel("2023-01-01 00:00:00", tick=False):
        sub = await add_item(subscription_factory(expires_at="2023-01-02"))

    # --- Act ---
    with time_machine.travel("2023-01-03 00:00:00", tick=False):
        expired = await repo.is_expired(sub.id)

    # --- Assert ---
    assert expired is True
```

**Variety booster:** Combine multiple `travel` blocks in one test (create → advance → assert) to cover create-time and check-time instants without sleeping.

## Zero-Warnings Policy

[ref: #postgres-zero-warnings]

Run with warnings as errors and fix root causes. Allow only a single narrow `warnings.filterwarnings(...)` (exact class, module regex, upstream-ticket comment) when a warning is truly unavoidable.

Run warnings as errors:

```bash
pytest -W error::DeprecationWarning -W error::ResourceWarning
```

Bad — blanket ignore hides root causes:

```python
warnings.filterwarnings("ignore")
pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")
```

Good — narrow, documented, ticketed filter:

```python
import warnings

warnings.filterwarnings(
    "ignore",
    message=".*legacy_api is deprecated.*",
    category=DeprecationWarning,
    module=r"some_upstream_lib\.compat",
)
# TODO: remove after https://github.com/vendor/lib/issues/1234 is fixed.
```

Common fixes: `ResourceWarning` for unclosed file → ensure `.close()`/`.dispose()` in fixtures; `PytestUnknownMarkWarning` → register the marker under `[tool.pytest.ini_options] markers`; library `DeprecationWarning` → upgrade or migrate to the new API.

**Variety booster:** Promote warnings to errors per category incrementally (`DeprecationWarning`, then `ResourceWarning`, then `RuntimeWarning`) so the same gate scales from one category to the whole suite.

## Anti-Patterns

[ref: #postgres-anti-patterns]

Use this checklist when reviewing a surrogate `conftest` or hunting isolation leaks. Each row is a forbidden move, why it breaks the suite, and the correct form.

| Anti-pattern | Why it is wrong | Correct approach |
| --- | --- | --- |
| Importing models before `conftest.py` patches | Patches are silently ignored; `JSONB` errors | Keep patches at the top of `conftest.py`; never import models at module level elsewhere |
| `commit()` inside `add_item` or helper fixtures | Breaks nested-transaction isolation; data leaks | `flush` + `refresh` only; rollback in `finally` |
| Forgetting to restore `StorageFactory.tr_manager` | Later tests talk to a stale `SQLite` `TransactionManager` | Save `orig_tr_manager` and restore in `finally` |
| Leaving stripped indexes discarded | Metadata singleton is corrupted for the remaining run | Restore indexes in `finally` |
| Using `random` / `uuid.uuid4()` / hardcoded strings in factories | Non-reproducible tests; violates core rules | Faker with a seeded instance |
| Mocking `session.flush` for non-partial constraints | Tests the mock, not real behavior | Insert duplicate data and assert real `IntegrityError` |
| Calling `db.setup()` in tests | Creates a `PostgreSQL` engine; overwrites the `SQLite` session | Bypass entirely; wire `TransactionManager` manually |
| `gc.collect()` instead of explicit resource cleanup | Unreliable, especially on Windows | `await session.close(); await engine.dispose()` |

**Variety booster:** Turn the table into a review rubric: for each new data-layer test, confirm none of the eight moves appears, so one checklist covers every repository, service, and servicer.

## Troubleshooting Cheat Sheet

[ref: #postgres-troubleshooting]

Map a failure symptom straight to its root cause and fix. Do not guess; apply the mapped fix.

| Symptom | Root cause | Fix |
| --- | --- | --- |
| `JSONB` not supported by `SQLite` | Patch ran after model import | Move `pg_dialect.JSONB = sa.JSON` to the absolute top of `conftest.py` |
| UUID primary key vs string foreign key mismatch | `Uuid.bind_processor` serializes to hex | Patch `bind_processor` to return `str(uuid)`; restore after tests |
| `psycopg.errors.UniqueViolation` missing | Tests run without `psycopg` | Alias `psycopg.errors.UniqueViolation = sqlite3.IntegrityError`; restore after |
| Partial unique indexes break `create_all` | `SQLite` lacks `WHERE` in indexes | Strip indexes with `dialect_options.postgresql.where`; restore in `finally` |
| Production DSN leaks into the test | `db.get_dsn()` reads env/Vault | Monkey-patch `db.get_dsn = lambda: sqlite_dsn`; restore in `finally` |
| SSL options incompatible with `SQLite` | `db.get_ssl_options()` returns an SSL dict | `db.get_ssl_options = dict`; restore in `finally` |
| Second engine created | `db.setup()` spawns a `psycopg` engine | Bypass `setup()`; assign `StorageFactory.tr_manager = TransactionManager()` |
| Data leaks between tests | Missing nested-transaction rollback | Use `begin_nested()` + `rollback()` in `finally` |
| Scoped session uses `PostgreSQL` bind | `db.Session` bound to the `psycopg` engine | Replace with `async_sessionmaker(bind=conn)` bound to the `SQLite` connection |
| `database is locked` under concurrency | `SQLite` single-writer lock | Serialize concurrent writes or use `:memory:` with a shared cache |
| `ResourceWarning` about unclosed file | `SQLite` file handle left open | `await engine.dispose(); await session.close()` before `gc.collect()` |

**Variety booster:** Add project-specific rows (custom types, extra extensions) to the same three-column shape so one table grows into the project's surrogate runbook.

## Adapting the Pattern to Another Project

[ref: #postgres-adapt-pattern]

Port the surrogate in five ordered steps: audit models, place import-time patches first, implement `db_session`, write helper fixtures, then decide real-vs-mock for `IntegrityError`.

Step 1 — audit models for `PostgreSQL`-only constructs:

```python
# Look for: sqlalchemy.dialects.postgresql.JSONB / ARRAY / INET / CIDR
#           postgresql_where on indexes
#           UUID columns whose foreign keys are str
#           direct imports of psycopg.errors
```

Step 2 — place import-time patches before any model import, saving originals.

Step 3 — implement `db_session`: build the `SQLite` DSN from `tmp_path`; override `db.get_dsn` and `db.get_ssl_options`; assign `StorageFactory.tr_manager = TransactionManager()`; strip partial indexes and save them; `create_all` inside `engine.begin()`; `begin_nested()`; yield the nested-bound session; roll back; restore globals and indexes.

Step 4 — write helpers: seeded `fake`, Faker-powered synchronous factories, `add_item` (`flush` + `refresh`, no `commit`), and composite `sample_*` fixtures.

Step 5 — decide `IntegrityError` strategy: non-partial unique constraints against real `SQLite`; partial-index violations via mock-flush only when `SQLite` cannot enforce them.

**Variety booster:** Treat the five steps as a checklist per project: re-run the model audit whenever a new dialect-only column or index lands, so the patch set stays complete.

## Quick Copy-Paste Template

[ref: #postgres-copy-paste-template]

Copy the ready-made asset `assets/pgsql.py` to `tests/conftest.py` and adapt the `app.*` imports plus the `Faker([...])` locales. Patches already precede model imports and every global is saved and restored.

Install the template:

```bash
cp pytest-design/assets/pgsql.py tests/conftest.py
```

What the asset wires, in order:

```text
1. import-time patches (JSONB→JSON, Uuid.bind_processor, psycopg.errors.UniqueViolation) + session-end restore
2. model-loading imports (placed after the patches)
3. session-scoped seeded fake
4. function-scoped db_session (NullPool + begin_nested savepoint, strip/restore partial indexes)
5. add_item helper (flush + refresh, no commit)
```

**Variety booster:** Keep the skeleton verbatim and vary only the `app.*` imports and locale list, so one template seeds every `SQLAlchemy 2.0` + `PostgreSQL` project in the organization.
