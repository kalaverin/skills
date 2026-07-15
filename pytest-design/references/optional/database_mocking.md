---
subject: "Choose lightest realistic database backend for repository/ORM tests: in-memory SQLite (sync/async) via SQLAlchemy 2.0 with transactional rollback, ephemeral PostgreSQL via `py-pglite`/`pytest-postgresql`/`testcontainers`, Redis via `fakeredis`, MongoDB via `mongomock`, async fixture lifecycle cleanup, Faker-driven parametrized inputs, isolation anti-patterns."
index:
  - anchor: database-mocking-when-to-mock
    what: "The choice between a lightweight mock or in-memory engine and a real database, based on whether the test target depends on database-specific features."
    problem: "Suite must stay fast by mocking where possible yet still exercise database-specific behavior that lightweight substitute cannot reproduce; fastest failing backend, mock versus real, portable sql, server-specific feature, upgrade path, isolation cost."
    use_when: "Test target is portable business logic, mapping code, or repository methods; lightweight backend can still fail the test; no database-specific feature involved."
    avoid_when: "Starting with a real database when a faster option can fail the test at hand; upgrade to a real database only when a test genuinely requires it."
    expected: "Each test runs against the fastest backend that can exercise its behavior, with real databases reserved for tests that genuinely need PostgreSQL-specific features."
  - anchor: database-mocking-sqlite-in-memory
    what: "An in-memory SQLite engine (`sqlite:///:memory:` sync or `sqlite+aiosqlite:///:memory:` async) reached through SQLAlchemy 2.0 for fast, isolated relational tests."
    problem: "Driver-agnostic portable SQL needs fast isolated relational store without spinning up real database server or paying per-test create-drop churn; in-memory engine, fast startup, per-test isolation, url from settings, throwaway schema, memory-backed suite."
    use_when: "Production SQL is driver-agnostic and portable; isolated relational store with instant bring-up suffices; real server startup would waste suite time."
    avoid_when: "SQLite relied on for PostgreSQL-specific behavior such as JSONB, full-text search, or custom types; route those tests to a real database."
    expected: "Fast, isolated relational tests run against an in-memory SQLite engine via SQLAlchemy 2.0, while PostgreSQL-specific tests route to a real database."
  - anchor: database-mocking-transactional-isolation
    what: "Creating the schema a single time per session and wrapping each test in a connection-level transaction that is rolled back afterward."
    problem: "Creating and dropping schema for every test is slow, yet tests sharing one database still need full isolation; schema once per session, connection transaction rollback, expire on commit, commit leak, savepoint pattern."
    use_when: "Many tests share one real database; per-test create/drop cost dominates suite time; connection-level transaction rolled back per test still gives full isolation."
    avoid_when: "Schema created and dropped in every test; commits leaked between tests; relying on the next test to clean up."
    expected: "The schema is created once per session and every test runs inside a connection-level transaction that is rolled back, giving full isolation without per-test create/drop cost."
  - anchor: database-mocking-pglite
    what: "An in-memory PostgreSQL instance without Docker, driven through `SQLAlchemyPGliteManager`, that gives real PostgreSQL behavior with a minimal startup footprint."
    problem: "Tests need real PostgreSQL server behavior without Docker dependency or full-server startup cost, so suite waits on environment instead of assertions; embedded server, docker-free, instance teardown, production-like engine, daemonless setup, wasm build, extension limit."
    use_when: "Tests need genuine server behavior without container overhead; Docker dependency undesirable; production-only extensions not required."
    avoid_when: "`cleanup_on_exit=True` dropped (leaves the in-memory instance running); treated as a full substitute when a test needs production-only extensions."
    expected: "Tests exercise genuine server behavior after near-instant bring-up without containers, and the embedded instance vanishes at suite end."
  - anchor: database-mocking-pytest-postgresql
    what: "A real PostgreSQL process plus a template database cloned per test for isolation, declared with `factories.postgresql_proc()` and `factories.postgresql(...)`."
    problem: "Constraint, type, and migration behavior must run against real engine while each test stays isolated via fresh cloned database; template clone, real process, unique constraint, explicit failure type, integrity error, migration correctness."
    use_when: "Constraint, type, or migration behavior must run against real PostgreSQL; fresh cloned template must keep each test isolated; asserting integrity failures with explicit exception types."
    avoid_when: "Exceptions caught broadly; expected failure asserted without explicit type — use `pytest.raises(IntegrityError, match=...)` naming the constraint so regressions are not hidden."
    expected: "Each test receives an isolated clone of a template database from a real PostgreSQL process, and expected failures are asserted with explicit types and `match=`."
  - anchor: database-mocking-testcontainers
    what: "A Dockerized PostgreSQL container via `testcontainers[postgresql]`, kept at session scope with state cleared between tests."
    problem: "Production-like containerized server must serve whole suite without recreating container for every test, so startup cost amortizes across run; session-scoped container, state reset, rollback between tests, truncate tables, real engine, shared service."
    use_when: "Suite needs containerized PostgreSQL for the whole run; recreating a container per test would dominate suite time; resetting state between tests preserves isolation."
    avoid_when: "Container run at function scope (recreating it per test is slow); resetting state between tests skipped (rollback or truncation required)."
    expected: "One session-scoped Dockerized PostgreSQL serves the whole run, state is reset between tests, and real behavior is verified without per-test recreation."
  - anchor: database-mocking-fakeredis
    what: "An in-memory implementation of the Redis protocol that is drop-in compatible with `redis-py` and `redis.asyncio.Redis`, via `FakeRedis` or `FakeAsyncRedis`."
    problem: "Redis-dependent code must run in memory without running server, keeping same client API and Lua support; protocol shim, decode responses, flush between tests, resp compatible, client drop-in, serverless cache, keyspace isolation."
    use_when: "Redis-dependent code can run in memory; `redis-py` client API must stay compatible; exercised scripts need Lua support."
    avoid_when: "`fakeredis` installed without the `[lua]` extra when Lua scripting is exercised; treated as a full Redis server for behaviors the in-memory implementation does not cover."
    expected: "Redis-dependent tests run against an in-memory, `redis-py`-compatible store with Lua support that is flushed between tests."
  - anchor: database-mocking-mongomock
    what: "An in-memory substitute for `pymongo.MongoClient` that keeps data in memory."
    problem: "Collection operations need quick in-memory unit test without running document server or obscure server-side aggregation, so feedback loop stays short; document store fake, crud coverage, driver shim, schema-less docs, aggregation gap, roundtrip assert."
    use_when: "Mongo collection operations need quick unit coverage; document server unnecessary for the behavior under test; server aggregation behaviors not exercised."
    avoid_when: "Tests depending on obscure server-side aggregation behaviors — route those to a real MongoDB."
    expected: "MongoDB collection operations are exercised in memory with quick feedback, while aggregation behavior is left to a real MongoDB."
  - anchor: database-mocking-async-database-fixtures
    what: "Async SQLAlchemy fixtures that dispose the `AsyncEngine`, close the `AsyncSession`, and run under `@pytest.mark.asyncio(loop_scope='function')`."
    problem: "Async database tests leak engines and sessions unless full lifecycle (dispose, close, rollback) runs on correct event loop; engine disposal, session close, loop alignment, resource leak, teardown protocol, cross-loop error, cleanup correctness."
    use_when: "Async fixtures own engines and sessions; teardown must dispose and close those resources on the right event loop; rolled-back transaction keeps tests leak-free."
    avoid_when: "Async resource management ignored: async engines and sessions require `await engine.dispose()` and `await session.close()` in fixture teardown, and async tests need `@pytest.mark.asyncio(loop_scope='function')`."
    expected: "Async engines and sessions are disposed and closed in teardown under the correct loop scope, so async database tests stay isolated and leak-free."
  - anchor: database-mocking-anti-patterns
    what: "A checklist of database-test mistakes that break isolation or leak state: reused mutable fixtures, hardcoded connection strings, missing resource cleanup, and production database usage."
    problem: "Database suite reuses mutable sessions between tests, hardcodes connection strings, skips resource cleanup, or points fixtures at production, so tests flake and data leaks; fixture hygiene, url literal, teardown gap, environment config, test database, state bleed."
    use_when: "Reviewing database tests for isolation breakage; fixtures share sessions, clients, or in-memory instances across tests; URLs appear as string literals in fixtures; fixture lacks dispose/close/rollback/flush/drop teardown."
    avoid_when: "Read-only, immutable shared resources — those may be shared safely."
    expected: "Every fixture owns and disposes its resources, URLs come from settings or environment, tests target dedicated databases, and no state crosses test boundaries."
  - anchor: database-mocking-variety-booster
    what: "Faker-driven repository inputs combined with `@pytest.mark.parametrize` and property-based bulk generation to exercise more invariants with fewer tests."
    problem: "Repository tests repeat similar arrange blocks with hardcoded values, so coverage stays shallow and boundary values go unexplored; realistic inputs, parametrized scenarios, property-style bulk, generated data, invariant sweep, edge cases, random payloads, scenario matrix."
    use_when: "Repository tests repeat near-identical arrange blocks; boundary cases (empty strings, maximum lengths, unique identifiers) need coverage; one assertion body should cover many statuses or bulk-generated entities."
    avoid_when: "Bulk generation applied when a test asserts a specific documented edge value; pin those as explicit parametrized cases instead."
    expected: "One assertion body covers every status and randomized bulk scenarios, edges like empty strings and maximum lengths appear regularly, and arrange duplication is gone."
libraries:
  - aiosqlite
  - fakeredis[lua]
  - mongomock
  - psycopg
  - py-pglite[sqlalchemy]
  - pymongo
  - pytest-asyncio
  - pytest-postgresql
  - redis
  - sqlalchemy>=2.0
  - testcontainers[postgresql]
---

# DATABASE MOCKING

## When to Mock vs Use a Real Database
[ref: #database-mocking-when-to-mock]

Prefer a lightweight mock or in-memory engine when the test target is business logic, mapping code, or repository methods that do not depend on database-specific features.

Reach for a real database when the test must verify PostgreSQL JSONB operators, full-text search, custom types, stored procedures, query plans, constraint behavior, or migration correctness.

Start with the fastest option that can fail the test you care about, and upgrade to a real database only when a test genuinely requires it.

## SQLite In-Memory with SQLAlchemy 2.0
[ref: #database-mocking-sqlite-in-memory]

Use an in-memory SQLite engine for fast, isolated tests when the production code is driver-agnostic and the SQL is portable.

Synchronous fixture:

```python
from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from my_app.models import Base


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")  # TODO: source from app settings / env
    Base.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()
```

Asynchronous fixture with `aiosqlite`:

```python
from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from my_app.models import Base


@pytest.fixture
async def async_db_session() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")  # TODO: source from app settings / env
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with session_maker() as session:
        yield session
    await engine.dispose()
```

Usage example:

```python
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio(loop_scope="function")
async def test_repository_creates_user(
    async_db_session: AsyncSession,
    fake: Faker,
) -> None:
    """
    Given: a fresh async database session.
    When: a user is created with generated name and email.
    Then: the persisted user reflects the supplied values.
    """
    # --- Arrange ---
    repo = UserRepository(async_db_session)
    name = fake.first_name()
    email = fake.fake_email()

    # --- Act ---
    user = await repo.create(name=name, email=email)
    await async_db_session.commit()

    # --- Assert ---
    assert user.id is not None
    assert user.name == name
    assert user.email == email
```

## Transactional Test Isolation for SQLAlchemy
[ref: #database-mocking-transactional-isolation]

Create the schema once per session and wrap each test in a connection-level transaction that is rolled back afterward.

This avoids the cost of `metadata.create_all()` and `metadata.drop_all()` for every test while keeping tests isolated.

Synchronous pattern:

```python
from collections.abc import Generator
from typing import Any

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from my_app.models import Base
from my_app.settings import get_test_database_url


@pytest.fixture(scope="session")
def db_engine() -> Generator[Any, None, None]:
    url = get_test_database_url()  # sourced from app settings / env
    engine = create_engine(url.replace("postgresql://", "postgresql+psycopg://"))
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(db_engine: Any) -> Generator[Session, None, None]:
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    yield session
    session.close()
    transaction.rollback()
    connection.close()
```

Asynchronous pattern:

```python
from collections.abc import AsyncGenerator
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from my_app.models import Base
from my_app.settings import get_test_database_url


@pytest.fixture(scope="session")
async def async_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    url = get_test_database_url()  # sourced from app settings / env
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def async_db_session(async_db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with async_db_engine.connect() as connection:
        async with connection.begin() as transaction:
            session_maker = async_sessionmaker(connection, expire_on_commit=False)
            session = session_maker()
            yield session
            await session.close()
            await transaction.rollback()
```

## Ephemeral PostgreSQL with py-pglite
[ref: #database-mocking-pglite]

`py-pglite` runs an in-memory PostgreSQL instance without Docker, giving real PostgreSQL behavior with very fast startup.

Install with the SQLAlchemy extra: `uv add py-pglite[sqlalchemy]`.

```python
from collections.abc import Generator
from typing import Any

import pytest
from py_pglite import PGliteConfig
from py_pglite.sqlalchemy import SQLAlchemyPGliteManager
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from my_app.models import Base


@pytest.fixture(scope="session")
def pglite_engine() -> Generator[Any, None, None]:
    config = PGliteConfig(cleanup_on_exit=True)
    with SQLAlchemyPGliteManager(config=config) as manager:
        engine = manager.get_engine()
        Base.metadata.create_all(engine)
        yield engine
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def pglite_session(pglite_engine: Any) -> Generator[Session, None, None]:
    session_maker = sessionmaker(bind=pglite_engine)
    session = session_maker()
    yield session
    session.close()
```

Usage example:

```python
from faker import Faker
from sqlalchemy.orm import Session


def test_user_repository_pglite(
    pglite_session: Session,
    fake: Faker,
) -> None:
    """
    Given: an ephemeral pglite session.
    When: a user is created.
    Then: the persisted user has an assigned id.
    """
    # --- Arrange ---
    repo = UserRepository(pglite_session)

    # --- Act ---
    user = repo.create(name=fake.first_name(), email=fake.fake_email())
    pglite_session.commit()

    # --- Assert ---
    assert user.id is not None
```

## Ephemeral PostgreSQL with pytest-postgresql
[ref: #database-mocking-pytest-postgresql]

`pytest-postgresql` starts a real PostgreSQL process, creates a template database, and clones it per test for isolation.

Install: `uv add pytest-postgresql psycopg`.

```python
from collections.abc import Generator
from typing import Any

import pytest
from pytest_postgresql import factories
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from my_app.models import Base


postgresql_proc = factories.postgresql_proc()
postgresql = factories.postgresql("postgresql_proc")


@pytest.fixture
def db_session(postgresql: Any) -> Generator[Session, None, None]:
    user = postgresql.info.user
    host = postgresql.info.host
    port = postgresql.info.port
    dbname = postgresql.info.dbname
    url = f"postgresql+psycopg://{user}:@{host}:{port}/{dbname}"
    engine = create_engine(url, poolclass=NullPool)
    Base.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()
```

Usage example:

```python
from faker import Faker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def test_unique_email_constraint(
    db_session: Session,
    fake: Faker,
) -> None:
    """
    Given: a user with a unique email already committed.
    When: another user with the same email is created.
    Then: an IntegrityError matching the unique-constraint message is raised.
    """
    # --- Arrange ---
    repo = UserRepository(db_session)
    email = fake.fake_email()
    repo.create(name=fake.first_name(), email=email)
    db_session.commit()

    # --- Act ---
    with pytest.raises(IntegrityError, match="unique constraint|duplicate key"):
        repo.create(name=fake.first_name(), email=email)
        db_session.commit()

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

## Ephemeral PostgreSQL with Testcontainers
[ref: #database-mocking-testcontainers]

`testcontainers[postgresql]` spins up a real Dockerized PostgreSQL container.

Keep the container at session scope and reset state between tests with transactional rollback or table truncation.

```python
from collections.abc import Generator
from typing import Any

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from my_app.models import Base


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer, None, None]:
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg


@pytest.fixture
def db_session(postgres_container: PostgresContainer) -> Generator[Session, None, None]:
    url = postgres_container.get_connection_url()
    engine = create_engine(url.replace("postgresql://", "postgresql+psycopg://"))
    Base.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
    engine.dispose()
```

Usage example:

```python
from faker import Faker
from sqlalchemy.orm import Session


def test_jsonb_query(
    db_session: Session,
    fake: Faker,
) -> None:
    """
    Given: an event with a JSONB payload.
    When: it is queried by payload key.
    Then: the created event is found in the result set.
    """
    # --- Arrange ---
    repo = EventRepository(db_session)
    event = repo.create(
        payload={
            "source": fake.word(),
            "value": fake.pyint(min_value=1, max_value=100),
        },
    )
    db_session.commit()

    # --- Act ---
    found = repo.find_by_payload_key("source")

    # --- Assert ---
    assert event in found
```

## Non-Relational Mocks: fakeredis
[ref: #database-mocking-fakeredis]

`fakeredis` provides an in-memory implementation of the Redis protocol that is drop-in compatible with `redis-py` and `redis.asyncio.Redis`.

Install with scripting support: `uv add "fakeredis[lua]"`.

Synchronous fixture:

```python
from collections.abc import Generator

import fakeredis
import pytest


@pytest.fixture
def redis_client() -> Generator[fakeredis.FakeRedis, None, None]:
    client = fakeredis.FakeRedis(decode_responses=True)
    yield client
    client.flushall()
    client.close()
```

Asynchronous fixture:

```python
from collections.abc import AsyncGenerator

import fakeredis
import pytest


@pytest.fixture
async def async_redis_client() -> AsyncGenerator[fakeredis.FakeAsyncRedis, None]:
    client = fakeredis.FakeAsyncRedis(decode_responses=True)
    yield client
    await client.flushall()
    await client.close()
```

Usage example:

```python
from faker import Faker
import pytest


@pytest.mark.asyncio(loop_scope="function")
async def test_cache_round_trip(
    async_redis_client: fakeredis.FakeAsyncRedis,
    fake: Faker,
) -> None:
    """
    Given: a fakeredis client and generated key/value pair.
    When: the value is stored and retrieved.
    Then: the retrieved value equals the stored value.
    """
    # --- Arrange ---
    key = fake.uuid4()
    value = fake.text(max_nb_chars=40)

    # --- Act ---
    await async_redis_client.set(key, value)

    # --- Assert ---
    assert await async_redis_client.get(key) == value
```

## Non-Relational Mocks: mongomock
[ref: #database-mocking-mongomock]

`mongomock` is a drop-in replacement for `pymongo.MongoClient` that keeps data in memory.

It is appropriate for unit tests that exercise collection operations but do not depend on obscure server-side aggregation behaviors.

```python
from collections.abc import Generator

import mongomock
import pytest


@pytest.fixture
def mongo_client() -> Generator[mongomock.MongoClient, None, None]:
    client = mongomock.MongoClient()
    yield client
    client.close()
```

Usage example:

```python
from faker import Faker


def test_insert_and_find_user(
    mongo_client: mongomock.MongoClient,
    fake: Faker,
) -> None:
    """
    Given: a mongomock collection.
    When: a user document is inserted.
    Then: the document is retrievable by its id.
    """
    # --- Arrange ---
    db = mongo_client["test_db"]
    collection = db["users"]
    user_id = fake.uuid4()
    document = {"_id": user_id, "name": fake.name(), "email": fake.fake_email()}

    # --- Act ---
    collection.insert_one(document)
    found = collection.find_one({"_id": user_id})

    # --- Assert ---
    assert found == document
```

## Async Database Fixtures
[ref: #database-mocking-async-database-fixtures]

Async fixtures must dispose the `AsyncEngine`, close the `AsyncSession`, and run under `@pytest.mark.asyncio(loop_scope="function")`.

Use `async_sessionmaker` bound to an existing async connection when you want transactional rollback, or bound to the engine when each test owns a fresh in-memory database.

```python
from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from my_app.models import Base
from my_app.settings import get_test_database_url


@pytest.fixture(scope="session")
async def async_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    url = get_test_database_url()  # sourced from app settings / env
    engine = create_async_engine(url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def async_db_session(async_db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with async_db_engine.connect() as connection:
        async with connection.begin() as transaction:
            session_maker = async_sessionmaker(connection, expire_on_commit=False)
            session = session_maker()
            yield session
            await session.close()
            await transaction.rollback()
```

Test example:

```python
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio(loop_scope="function")
async def test_async_repo_returns_created_user(
    async_db_session: AsyncSession,
    fake: Faker,
) -> None:
    """
    Given: a user created in an async session.
    When: the user is fetched by email.
    Then: the fetched user matches the created one.
    """
    # --- Arrange ---
    repo = AsyncUserRepository(async_db_session)
    email = fake.fake_email()

    # --- Act ---
    user = await repo.create(name=fake.name(), email=email)
    await async_db_session.commit()
    fetched = await repo.get_by_email(email)

    # --- Assert ---
    assert fetched is not None
    assert fetched.id == user.id
```

## Anti-Patterns and Common Errors
[ref: #database-mocking-anti-patterns]

Avoid these mistakes that break isolation, leak state, or slow the suite:

- **Shared mutable state across tests.** Never reuse a session, client, or in-memory database instance between tests unless it is read-only and immutable.
- **Hardcoded connection strings.** Source URLs from environment variables, application settings, or fixture-provided values; mark unavoidable placeholders with `# TODO: source from app settings / env`.
- **Missing cleanup.** Every fixture that opens an engine, session, connection, or client must dispose, close, rollback, flush, or drop owned resources.
- **Using the production database in tests.** Tests must target dedicated test resources; never point fixtures at a production connection string.

## Variety Booster: Faker-Driven Inputs
[ref: #database-mocking-variety-booster]

Use `faker` to generate realistic data and combine it with `@pytest.mark.parametrize` or property-style inputs to exercise more invariants with fewer tests.

Parametrized scenario:

```python
import pytest
from faker import Faker
from sqlalchemy.orm import Session


from my_app.models import UserStatus


@pytest.mark.parametrize(
    "status",
    list(UserStatus),
)
def test_user_filter_by_status(
    db_session: Session,
    fake: Faker,
    status: UserStatus,
) -> None:
    """
    Given: a user with the parametrized status.
    When: users are filtered by that status.
    Then: the created user is present in the result set.
    """
    # --- Arrange ---
    repo = UserRepository(db_session)
    user = repo.create(
        name=fake.name(),
        email=fake.fake_email(),
        status=status,
    )
    db_session.commit()

    # --- Act ---
    found = repo.find_by_status(status)

    # --- Assert ---
    assert user in found
```

Property-style input bulk:

```python
from faker import Faker
from sqlalchemy.orm import Session


def test_repository_orders_by_created_at(
    db_session: Session,
    fake: Faker,
) -> None:
    """
    Given: multiple users created in a session.
    When: they are listed ordered by created_at.
    Then: the list length matches the count and is sorted.
    """
    # --- Arrange ---
    repo = UserRepository(db_session)
    count = fake.pyint(min_value=3, max_value=10)
    users = [
        repo.create(name=fake.name(), email=fake.fake_email())
        for _ in range(count)
    ]
    db_session.commit()

    # --- Act ---
    ordered = repo.list_ordered_by_created_at()

    # --- Assert ---
    assert len(ordered) == count
    assert ordered == sorted(ordered, key=lambda u: u.created_at)
```

Variety booster tip: generate boundary values such as empty strings, maximum length names, or unique identifiers with `faker.uuid4()` and assert that the repository preserves them without truncation or collision.
