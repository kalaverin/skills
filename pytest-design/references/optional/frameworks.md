---
subject: "Test Django, FastAPI, and Flask through their public HTTP surface and framework fixtures: Django `django_db`/`transaction=True`/query-count/`on_commit`/`--reuse-db`, FastAPI `TestClient`/`httpx.AsyncClient`+`ASGITransport`/`LifespanManager`/dependency overrides, Flask application factory/`test_client`/`session_transaction`/uploads/CLI runner; indirect parametrization over roles, HTTP methods, status codes, and dependency overrides."
index:
  - anchor: frameworks-django
    what: "Testing a Django project with pytest fixtures and marks via `pytest-django` instead of `django.test.TestCase` subclasses, where database access is disabled by default and any ORM-touching test must carry `@pytest.mark.django_db` or request a database-aware fixture (`db`, `transactional_db`, `client`, `admin_client`, `admin_user`)."
    problem: "ORM-touching Django test must run with pytest idioms while plugin keeps database off by default and isolates each test in rolled-back atomic block; database off default, mark or fixture, rollback isolation, mail settings urlconf, query budget, on-commit callback."
    use_when: "Django test touches ORM, pytest idioms replace TestCase subclasses, and plugin keeps database off unless explicitly requested; database off default, mark or fixture, rollback isolation, mail settings urlconf, query budget, on commit callback, django db."
    avoid_when: "Do not treat a query-count assertion as a coverage target (keep the wrapped block small and treat the number as a deliberate invariant), do not assert mail through the global `mail.outbox` (use the `mailoutbox` fixture), and do not mutate `settings.ROOT_URLCONF` directly (use `@pytest.mark.urls`)."
    expected: "ORM-touching tests are explicitly marked or fixtured and isolated in rolled-back transactions, while mail, settings, URLconf, on-commit callbacks, and query budgets are asserted through auto-reverting pytest-django fixtures and helpers."
  - anchor: frameworks-django-variety-booster
    what: "Covering many Django access and CRUD cases from a few tests by driving an `authenticated_client` fixture that builds a user via `User.objects.create_user`/`create_superuser`, calls `client.force_login(user)`, and is parametrized indirectly over staff status and over HTTP method plus expected status."
    problem: "View authorization and routing across roles and HTTP methods duplicate test bodies unless collapsed into parametrized cases with unique identifiers; staff matrix, method matrix, indirect client, factory payload, unique slug, one body many cases."
    use_when: "Django authorization and CRUD vary across roles and methods, one parametrized client body can cover matrix with unique identifiers; staff matrix, method matrix, indirect client, factory payload, unique slug, one body many cases, role coverage."
    avoid_when: "Do not write one test per role/method/status combination (collapse them into parametrized cases), and do not hand-roll identifiers that can collide within a session (use `fake.unique.slug()` or an equivalent unique provider)."
    expected: "A single parametrized Django test body covers staff vs non-staff and all relevant HTTP methods with the correct status per case, and factory-driven fixtures keep identifiers unique across the session."
  - anchor: frameworks-fastapi
    what: "Testing a FastAPI application through its public HTTP surface — synchronous endpoints via `fastapi.testclient.TestClient`, asynchronous endpoints via `httpx.AsyncClient` over `ASGITransport(app=...)` wrapped in `asgi_lifespan.LifespanManager`, isolating dependencies by swapping and restoring `app.dependency_overrides`, and validating payloads against `pydantic.BaseModel`."
    problem: "Sync and async endpoints must run over HTTP honoring lifespan, each async test on own loop, dependencies swapped without patching database layer, responses validated against schemas; lifespan manager, dependency override, model validate, rejection path, loop isolation, public http surface."
    use_when: "FastAPI endpoints must run through public HTTP surface, lifespan matters, dependencies swap cleanly, and responses validate against schemas; lifespan manager, dependency override, model validate, rejection path, loop isolation, public http surface, test client."
    avoid_when: "Do not assume `ASGITransport` triggers lifespan events by default (wrap in `LifespanManager` when they initialize state), do not use a sync `TestClient` inside an async test or reuse an async fixture across loops (`Task attached to a different loop`), do not leave `app.dependency_overrides` unrestored, do not patch the database layer instead of swapping dependencies, and do not validate only well-formed responses (also assert the rejection path)."
    expected: "Sync and async FastAPI endpoints are exercised over HTTP with lifespan honored and loops isolated, dependencies are swapped through reverted overrides, and responses are validated against Pydantic schemas with both acceptance and rejection covered."
  - anchor: frameworks-fastapi-variety-booster
    what: "Covering FastAPI authorization and schema invariants from a few tests by parametrizing roles and expected statuses against `app.dependency_overrides[get_current_user]` and validating every response against Pydantic, optionally collapsing role clients into one indirect `authorized_client` fixture."
    problem: "Per-role authorization and per-endpoint schemas across many routes multiply tests unless one parametrized body covers role matrix with restored overrides; role status matrix, override restore, schema per endpoint, authorized client, no leak, response validation."
    use_when: "FastAPI routes repeat role and schema checks, one parametrized body with restored overrides can cover many endpoints; role status matrix, override restore, schema per endpoint, authorized client, no leak, response validation, route matrix."
    avoid_when: "Do not create separate user records per role (use dependency-override matrices), do not leave `app.dependency_overrides` mutated after the test (restore in the same test or in fixture teardown), and do not skip response-schema validation on the parametrized paths."
    expected: "One parametrized test covers every role's authorization outcome and each endpoint's response schema, with overrides restored so no role or fake leaks between cases."
  - anchor: frameworks-flask
    what: "Testing a Flask application built through an application factory (`create_app(config=...)`) with `app.test_client()` (`FlaskClient`) for HTTP routes, `app.test_request_context()` and `g` for request-context code, `client.session_transaction()` to pre-seed sessions, `follow_redirects`/`response.history` for redirect chains, `(BytesIO, filename)` uploads, and `app.test_cli_runner()` (`CliRunner`) for CLI commands — isolated with `TESTING=True` and faker-generated secrets and database URIs."
    problem: "Routes, sessions, request context, uploads, redirect chains, and CLI commands must run in isolated factory-built app rather than globally constructed app with hardcoded secrets; application factory, testing flag, generated secrets, session seed, upload tuple, redirect history."
    use_when: "Flask app can be built through factory, routes sessions uploads redirects and CLI commands need isolation from global app; application factory, testing flag, generated secrets, session seed, upload tuple, redirect history, request context."
    avoid_when: "Do not test against a globally constructed app instead of an application factory, do not hardcode secrets or database URIs (generate with faker and set `TESTING=True`), and do not read or write the session outside a kept-alive request context (`with client:` and `session_transaction`)."
    expected: "An isolated, factory-built test app with `TESTING=True` and generated secrets exercises HTTP routes, session and request context, file uploads, redirect chains, and CLI commands through the test client and CLI runner without leaking global state."
  - anchor: frameworks-flask-variety-booster
    what: "Covering many Flask configurations and roles from a few tests by parametrizing the factory fixture over distinct config objects (feature flags or database backends), deriving anonymous/member/admin clients from `client` by pre-seeding the session, and combining `follow_redirects=True` with parametrized expected statuses."
    problem: "Multiple configurations and role-based access rules (success and authorization redirect) duplicate route tests unless factory fixture and role clients are parametrized; config matrix, role clients, follow redirects, feature flags, backend vary, shared assertions."
    use_when: "Flask configurations and role based rules multiply route tests, factory fixture and seeded role clients can collapse them; config matrix, role clients, follow redirects, feature flags, backend vary, shared assertions, route coverage."
    avoid_when: "Do not duplicate route tests per configuration or per role (parametrize the factory fixture and derive role clients from `client`), and do not assert redirect outcomes separately from success outcomes when one parametrized status covers both."
    expected: "One parametrized Flask test body exercises several configurations and all roles (including authorization redirects) with shared assertions, and configurations and roles are varied through fixtures rather than duplicated tests."
libraries:
  - asgi-lifespan
  - click
  - django
  - fastapi
  - flask
  - httpx
  - pydantic
  - pytest-asyncio
  - pytest-django
---

# Framework-Specific Appendices

Activate the relevant appendix by scanning `pyproject.toml` dependencies and `src/` imports.

## Django (`pytest-django`)

[ref: #frameworks-django]

Use `pytest-django` to test Django projects with pytest fixtures and marks instead of `django.test.TestCase` subclasses.
The plugin disables database access by default, so any test that touches the ORM must either carry `@pytest.mark.django_db` or request a database-aware fixture such as `db`, `transactional_db`, `client`, `admin_client`, or `admin_user`.

The marker is the right choice when you test model methods, managers, or service functions that do not need the test client.
Use `@pytest.mark.django_db(transaction=True)` when the code under test itself commits or rolls back transactions, because the default behavior only wraps each test in an atomic block and rolls it back at the end.
Add `reset_sequences=True` when serial primary keys must restart from one, and use `databases=["default", "other"]` or `databases="__all__"` to allow queries against non-default databases.

The built-in fixtures cover most everyday needs:
`client` and `async_client` for HTTP requests, `admin_client` for an already authenticated superuser, `admin_user` for the superuser itself, `django_user_model` as the active user model, `rf` and `async_rf` as `RequestFactory` instances, `settings` for temporary setting overrides, `mailoutbox` for captured mail, `django_assert_num_queries` / `django_assert_max_num_queries` for query budgets, and `django_capture_on_commit_callbacks` for `transaction.on_commit` assertions.

For template and form assertions, import helpers from `pytest_django.asserts` such as `assertTemplateUsed`, `assertFormError`, and `assertQuerySetEqual`.

To assert on query counts, wrap the work in `django_assert_num_queries(N)` or `django_assert_max_num_queries(N)`.
Keep the wrapped block as small as possible and treat the number as a deliberate invariant, not a coverage target.

`transaction.on_commit` callbacks do not run during a rolled-back test transaction, so pytest-django provides `django_capture_on_commit_callbacks(execute=True)`.
The context manager captures the callbacks and, with `execute=True`, runs them on exit so you can assert their side effects such as sent mail or enqueued tasks.

Always assert mail through the `mailoutbox` fixture rather than the global `mail.outbox`, because the fixture gives each test a fresh outbox and cleans it up automatically.

Override `ROOT_URLCONF` per test with `@pytest.mark.urls("myapp.test_urls")`.
This is safer than mutating `settings.ROOT_URLCONF` directly, because the marker restores the original value after the test.

Use the `settings` fixture to temporarily change any Django setting.
Changes are reverted automatically, so the test cannot leak global state.

Speed up local suites with `--reuse-db` to keep the test database between runs, force recreation with `--create-db`, and skip migrations with `--no-migrations` when the schema is already up to date.
For custom database setup, override the session-scoped `django_db_setup` fixture and configure templates, xdist suffixes, or multi-database routing there.

```python
import pytest
from http import HTTPStatus

from django.contrib.auth.models import AbstractBaseUser
from django.test import Client
from django.urls import reverse
from faker import Faker


@pytest.mark.django_db
def test_signup_persists_user(
    client: Client,
    django_user_model: type[AbstractBaseUser],
    fake: Faker,
) -> None:
    """
    Given: valid signup payload with generated email and password.
    When: the signup endpoint is called.
    Then: the response is CREATED and the user exists in the database.
    """
    # --- Arrange ---
    email = fake.fake_email()
    password = fake.password()

    # --- Act ---
    response = client.post(
        reverse("signup"),
        {"email": email, "password": password},
    )

    # --- Assert ---
    assert response.status_code == HTTPStatus.CREATED
    assert django_user_model.objects.filter(email=email).exists()
```

```python
from http import HTTPStatus

from django.core.mail import EmailMessage
from django.test import Client
from django.urls import reverse
from faker import Faker
from pytest_django import DjangoAssertNumQueries, DjangoCaptureOnCommitCallbacks


@pytest.mark.django_db
def test_invoice_creation_sends_receipt_and_runs_on_commit(
    client: Client,
    mailoutbox: list[EmailMessage],
    django_assert_num_queries: DjangoAssertNumQueries,
    django_capture_on_commit_callbacks: DjangoCaptureOnCommitCallbacks,
    fake: Faker,
) -> None:
    """
    Given: an invoice creation payload.
    When: the endpoint is called under query and on_commit capture.
    Then: the response is CREATED, one callback ran, and one email was sent.
    """
    # --- Arrange ---
    payload = {
        "customer_email": fake.fake_email(),
        "amount": fake.pyint(),
    }

    # --- Act ---
    with django_assert_num_queries(4):
        with django_capture_on_commit_callbacks(execute=True) as callbacks:
            response = client.post(reverse("invoice-create"), payload)

    # --- Assert ---
    assert response.status_code == HTTPStatus.CREATED
    assert len(callbacks) == 1
    assert len(mailoutbox) == 1
    assert payload["customer_email"] in mailoutbox[0].body
```

```python
import pytest
from http import HTTPStatus

from django.conf import LazySettings
from django.test import Client
from django.urls import reverse
from faker import Faker


@pytest.mark.urls("myapp.test_urls")
def test_profile_view_under_alternative_urlconf(
    client: Client,
    fake: Faker,
) -> None:
    """
    Given: an alternative URL configuration.
    When: the profile view is requested.
    Then: the response is OK.
    """
    # --- Arrange ---
    # client uses the alternative urlconf via marker.

    # --- Act ---
    response = client.get(reverse("profile"))

    # --- Assert ---
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_signup_blocked_when_registration_closed(
    client: Client,
    settings: LazySettings,
    fake: Faker,
) -> None:
    """
    Given: registration is disabled via settings.
    When: the signup endpoint is called.
    Then: the response is FORBIDDEN.
    """
    # --- Arrange ---
    settings.REGISTRATION_OPEN = False

    # --- Act ---
    response = client.post(
        reverse("signup"),
        {"email": fake.fake_email()},
    )

    # --- Assert ---
    assert response.status_code == HTTPStatus.FORBIDDEN
```

```python
from http import HTTPStatus

from django.contrib.auth.models import AbstractBaseUser
from django.test import Client, RequestFactory
from django.urls import reverse
from faker import Faker

from myapp.views import dashboard


def test_admin_dashboard_via_client(
    admin_client: Client,
    fake: Faker,
) -> None:
    """
    Given: an authenticated admin client.
    When: the admin dashboard is requested.
    Then: the response is OK.
    """
    # --- Arrange ---
    # admin_client is supplied by pytest-django.

    # --- Act ---
    response = admin_client.get(reverse("admin-dashboard"))

    # --- Assert ---
    assert response.status_code == HTTPStatus.OK


def test_dashboard_view_with_request_factory(
    rf: RequestFactory,
    admin_user: AbstractBaseUser,
    fake: Faker,
) -> None:
    """
    Given: a request factory and an admin user.
    When: the dashboard view is invoked directly.
    Then: the response is OK.
    """
    # --- Arrange ---
    request = rf.get(reverse("dashboard"))
    request.user = admin_user

    # --- Act ---
    response = dashboard(request)

    # --- Assert ---
    assert response.status_code == HTTPStatus.OK
```

### Variety booster

[ref: #frameworks-django-variety-booster]

You can cover many authorization and HTTP invariants with a single test by combining fixtures, `pytest.mark.parametrize`, and small factory helpers.
Indirect parametrization lets the same test run against different user roles, status codes, or HTTP methods without copy-pasting assertions.

```python
import pytest
from http import HTTPStatus

from django.contrib.auth.models import AbstractBaseUser
from django.test import Client
from django.urls import reverse
from faker import Faker


@pytest.fixture
def authenticated_client(
    request: pytest.FixtureRequest,
    client: Client,
    django_user_model: type[AbstractBaseUser],
    fake: Faker,
) -> Client:
    """Create a logged-in user with staff status driven by indirect parametrization."""
    is_staff = bool(request.param)
    user = django_user_model.objects.create_user(
        email=fake.fake_email(),
        password=fake.password(),
        is_staff=is_staff,
    )
    client.force_login(user)
    return client


@pytest.mark.django_db
@pytest.mark.parametrize(
    "authenticated_client, expected",
    [
        (True, HTTPStatus.OK),
        (False, HTTPStatus.FORBIDDEN),
    ],
    indirect=["authenticated_client"],
)
def test_dashboard_access_depends_on_staff_status(
    authenticated_client: Client,
    expected: HTTPStatus,
) -> None:
    """
    Given: an authenticated client with parametrized staff status.
    When: the dashboard is requested.
    Then: the response matches the expected status.
    """
    # --- Arrange ---
    # authenticated_client and expected come from parametrization.

    # --- Act ---
    response = authenticated_client.get(reverse("dashboard"))

    # --- Assert ---
    assert response.status_code == expected
```

Factory fixtures raise the same idea to model instances.
A reusable `article_payload` fixture can feed both create and update tests, while `fake.unique.slug()` guarantees that generated identifiers never collide within a session.
Parametrize over HTTP methods and expected status codes to exercise `GET`, `POST`, `PUT`, and `DELETE` through one test body and catch authorization or routing gaps early.

## FastAPI

[ref: #frameworks-fastapi]

FastAPI applications should be exercised through their public HTTP surface.
Use `fastapi.testclient.TestClient` for synchronous tests and `httpx.AsyncClient` with `ASGITransport` for asynchronous tests.
Always isolate tests by reverting `app.dependency_overrides` in fixture teardown and by keeping async fixtures function-scoped.
Validate request and response payloads against Pydantic models instead of inspecting raw JSON.

### Synchronous tests with `TestClient`

```python
from http import HTTPStatus

import pytest
from faker import Faker
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


def test_read_missing_item_returns_not_found(
    client: TestClient,
    fake: Faker,
) -> None:
    """
    Given: a non-existent item id.
    When: the item endpoint is requested.
    Then: the response is NOT_FOUND.
    """
    # --- Arrange ---
    item_id = fake.uuid4()

    # --- Act ---
    response = client.get(f"/items/{item_id}")

    # --- Assert ---
    assert response.status_code == HTTPStatus.NOT_FOUND
```

### Asynchronous tests with `AsyncClient` and `ASGITransport`

```python
from http import HTTPStatus

import pytest
from asgi_lifespan import LifespanManager
from faker import Faker
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


@pytest.fixture
async def async_client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app) as manager:
        transport = ASGITransport(app=manager.app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest.mark.anyio
async def test_create_item(
    async_client: AsyncClient,
    fake: Faker,
) -> None:
    """
    Given: a JSON payload with generated name and description.
    When: it is posted to the items endpoint.
    Then: the response is CREATED and echoes the name.
    """
    # --- Arrange ---
    payload = {"name": fake.word(), "description": fake.sentence()}

    # --- Act ---
    response = await async_client.post("/items", json=payload)

    # --- Assert ---
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["name"] == payload["name"]
```

`AsyncClient` with `ASGITransport` does not trigger lifespan events by default.
Wrap the application in `asgi_lifespan.LifespanManager` when startup or shutdown handlers initialize state.
Mark async tests with `@pytest.mark.anyio` or `@pytest.mark.asyncio(loop_scope="function")` so each test receives its own event loop.

The error `Task attached to a different loop` usually appears when a sync `TestClient` is used inside an async test or when an async fixture is reused across event loops.
Keep async clients and lifespan managers function-scoped to avoid this.

### Dependency overrides for authentication and repositories

```python
from enum import StrEnum
from http import HTTPStatus
from typing import Annotated

import pytest
from faker import Faker
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient


class Role(StrEnum):
    ADMIN = "admin"
    MEMBER = "member"


class UserRepository:
    async def get(self, user_id: str) -> dict[str, str] | None:
        ...


async def get_repository() -> UserRepository:
    return UserRepository()


async def get_current_user() -> dict[str, str]:
    ...


@app.get("/users/{user_id}")
async def read_user(
    user_id: str,
    repo: Annotated[UserRepository, Depends(get_repository)],
    current_user: Annotated[dict[str, str], Depends(get_current_user)],
) -> dict[str, str]:
    user = await repo.get(user_id)
    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return user


class FakeUserRepository(UserRepository):
    def __init__(self, fake: Faker) -> None:
        self._fake = fake

    async def get(self, user_id: str) -> dict[str, str] | None:
        return {"id": user_id, "name": self._fake.first_name()}


@pytest.fixture
def client(app: FastAPI, fake: Faker) -> TestClient:
    original_overrides = dict(app.dependency_overrides)
    app.dependency_overrides[get_repository] = lambda: FakeUserRepository(fake)
    app.dependency_overrides[get_current_user] = lambda: {
        "id": fake.uuid4(),
        "role": Role.ADMIN,
    }
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = original_overrides


def test_get_user_uses_fake_repository(
    client: TestClient,
    fake: Faker,
) -> None:
    """
    Given: a fake repository override and a generated user id.
    When: the user endpoint is requested.
    Then: the response is OK and the body contains the same id.
    """
    # --- Arrange ---
    user_id = fake.uuid4()

    # --- Act ---
    response = client.get(f"/users/{user_id}")

    # --- Assert ---
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body["id"] == user_id
```

Restore the original overrides in teardown so that mutations do not leak to other tests.
Swap repositories or services instead of patching the database layer directly.

### Request/response validation with Pydantic

```python
from http import HTTPStatus

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError


class ItemResponse(BaseModel):
    id: str
    name: str
    description: str | None


def test_read_item_response_matches_schema(
    client: TestClient,
    fake: Faker,
) -> None:
    """
    Given: an existing item id.
    When: the item endpoint is requested.
    Then: the response validates against the Pydantic schema and matches the id.
    """
    # --- Arrange ---
    item_id = fake.uuid4()

    # --- Act ---
    response = client.get(f"/items/{item_id}")

    # --- Assert ---
    assert response.status_code == HTTPStatus.OK
    item = ItemResponse.model_validate(response.json())
    assert item.id == item_id


def test_item_response_rejects_missing_id(fake: Faker) -> None:
    """
    Given: a payload missing the required id field.
    When: it is validated against ItemResponse.
    Then: a ValidationError matching "id" is raised.
    """
    # --- Arrange ---
    # Payload intentionally omits "id".

    # --- Act / Assert ---
    with pytest.raises(ValidationError, match="id"):
        ItemResponse.model_validate({"name": fake.word()})
```

### Variety booster

[ref: #frameworks-fastapi-variety-booster]

A small set of tests can cover many invariants when the test data and dependencies are parameterized.
Parametrize HTTP methods and expected statuses to verify routing and authorization consistently.

```python
@pytest.mark.parametrize(
    "role, expected_status",
    [
        (Role.ADMIN, HTTPStatus.NO_CONTENT),
        (Role.MEMBER, HTTPStatus.FORBIDDEN),
    ],
)
def test_delete_item_requires_admin(
    app: FastAPI,
    fake: Faker,
    role: Role,
    expected_status: HTTPStatus,
) -> None:
    """
    Given: a parametrized user role and dependency override.
    When: an item deletion is requested.
    Then: the response status matches the role's authorization.
    """
    # --- Arrange ---
    original_overrides = dict(app.dependency_overrides)
    app.dependency_overrides[get_current_user] = lambda: {
        "id": fake.uuid4(),
        "role": role,
    }

    # --- Act ---
    with TestClient(app) as client:
        response = client.delete(f"/items/{fake.uuid4()}")

    # --- Assert ---
    assert response.status_code == expected_status

    # --- Cleanup ---
    app.dependency_overrides = original_overrides
```

Use dependency-override matrices to test authorization without creating separate user records.
Validate responses against Pydantic schemas to catch missing or mistyped fields across every endpoint.
For even less code, define a single `authorized_client` fixture that accepts `request.param` and returns a `TestClient` with the desired override; then parametrize that fixture indirectly across roles.

## Flask

[ref: #frameworks-flask]

Flask ships with a test client and CLI runner that work best when the application is built through an application factory.
Keep the test application isolated by setting `TESTING=True` and generating any secrets or database URIs through `faker`.

```python
from collections.abc import Iterator
from http import HTTPStatus
from io import BytesIO

import pytest
from click.exceptions import UsageError
from click.testing import CliRunner
from faker import Faker
from flask import Flask, current_app, g, request
from flask.testing import FlaskClient

from myapp import create_app


@pytest.fixture
def app(fake: Faker) -> Iterator[Flask]:
    app = create_app(
        config={
            "TESTING": True,
            "SECRET_KEY": fake.sha256(),
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    app.config.update({"WTF_CSRF_ENABLED": False})
    with app.app_context():
        yield app


@pytest.fixture
def client(app: Flask) -> Iterator[FlaskClient]:
    with app.test_client() as client:
        yield client
```

The `with app.app_context():` block ensures that extensions, database models, and `current_app` are available during fixture setup and teardown.
Use the `client` fixture to exercise HTTP endpoints.

```python
def test_create_user(
    client: FlaskClient,
    fake: Faker,
) -> None:
    """
    Given: a valid user creation payload.
    When: it is posted to /users.
    Then: the response is CREATED and echoes the email.
    """
    # --- Arrange ---
    payload = {
        "email": fake.fake_email(),
        "name": fake.name(),
        "password": fake.password(length=16),
    }

    # --- Act ---
    response = client.post("/users", json=payload)

    # --- Assert ---
    assert response.status_code == HTTPStatus.CREATED
    assert response.json is not None
    assert response.json["email"] == payload["email"]


def test_request_context_populates_g(
    app: Flask,
    fake: Faker,
) -> None:
    """
    Given: a Flask test request context.
    When: a request id is stored on g.
    Then: the value is readable from g.
    """
    # --- Arrange ---
    request_id = str(fake.uuid4())

    # --- Act ---
    with app.test_request_context("/items", method="GET"):
        g.request_id = request_id

        # --- Assert ---
        assert g.request_id == request_id
```

For routes that read from or write to the session, wrap the client in a `with` block to keep the request context alive, and use `client.session_transaction()` to pre-seed values without flowing through a login form.

```python
def test_dashboard_renders_for_logged_in_user(
    client: FlaskClient,
    fake: Faker,
) -> None:
    """
    Given: a session pre-seeded with a logged-in user.
    When: the dashboard is requested.
    Then: the response is OK and contains the user's email.
    """
    # --- Arrange ---
    email = fake.fake_email()
    with client.session_transaction() as session:
        session["user_id"] = str(fake.uuid4())
        session["email"] = email

    # --- Act ---
    with client:
        response = client.get("/dashboard")

    # --- Assert ---
    assert response.status_code == HTTPStatus.OK
    assert email in response.get_data(as_text=True)


def test_login_redirects_to_dashboard(
    client: FlaskClient,
    fake: Faker,
) -> None:
    """
    Given: valid login credentials.
    When: the login endpoint is posted with follow_redirects.
    Then: the client lands on the dashboard via one redirect.
    """
    # --- Arrange ---
    payload = {
        "email": fake.fake_email(),
        "password": fake.password(length=16),
    }

    # --- Act ---
    response = client.post("/login", json=payload, follow_redirects=True)

    # --- Assert ---
    assert response.status_code == HTTPStatus.OK
    assert len(response.history) == 1
    assert response.history[0].status_code == HTTPStatus.FOUND
    assert response.request.path == "/dashboard"
```

File uploads pass a tuple of `(BytesIO, filename)` under the form field name, and CLI commands are invoked through the runner returned by `app.test_cli_runner()`.

```python
def test_upload_avatar_redirects_to_profile(
    client: FlaskClient,
    fake: Faker,
) -> None:
    """
    Given: a multipart avatar upload payload.
    When: it is posted to /profile/avatar with follow_redirects.
    Then: the client lands on /profile via one redirect.
    """
    # --- Arrange ---
    file_data = BytesIO(fake.binary(length=128))
    file_name = fake.file_name(extension="png")

    # --- Act ---
    response = client.post(
        "/profile/avatar",
        data={"avatar": (file_data, file_name)},
        content_type="multipart/form-data",
        follow_redirects=True,
    )

    # --- Assert ---
    assert response.status_code == HTTPStatus.OK
    assert len(response.history) == 1
    assert response.history[0].status_code == HTTPStatus.FOUND
    assert response.request.path == "/profile"


@pytest.fixture
def runner(app: Flask) -> Iterator[CliRunner]:
    with app.test_cli_runner() as runner:
        yield runner


def test_create_user_command(
    runner: CliRunner,
    fake: Faker,
) -> None:
    """
    Given: a generated email.
    When: the create-user CLI command is invoked.
    Then: it exits cleanly and echoes the email.
    """
    # --- Arrange ---
    email = fake.fake_email()

    # --- Act ---
    result = runner.invoke(args=["create-user", "--email", email])

    # --- Assert ---
    assert result.exit_code == 0
    assert email in result.output


def test_create_user_command_requires_email(
    runner: CliRunner,
    fake: Faker,
) -> None:
    """
    Given: a CLI runner.
    When: create-user is invoked without --email.
    Then: a UsageError matching the missing option is raised.
    """
    # --- Arrange ---
    # Command intentionally omits required --email.

    # --- Act / Assert ---
    with pytest.raises(UsageError, match="Missing option '--email'"):
        runner.invoke(args=["create-user"], catch_exceptions=False)
```

### Variety booster

[ref: #frameworks-flask-variety-booster]

Parametrize the factory fixture over different configuration objects to exercise behavior under distinct feature flags or database backends with a single test body.
Derive role-based fixtures from `client` by pre-seeding the session, so anonymous, member, and admin clients can reuse the same route tests.
Combine `follow_redirects=True` with `@pytest.mark.parametrize` on the expected status code to cover both success paths and authorization redirects without duplicating assertions.
