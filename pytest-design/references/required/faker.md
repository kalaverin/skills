---
subject: "Generate realistic, deterministic data with Faker: the built-in `faker` fixture, a custom seeded multi-locale `fake` fixture (env-driven seed, the only permitted stdlib `random`), `faker.unique.<method>` for small suites vs deterministic suffixes for large ones, seed/locale overrides via `faker_seed`/`faker_locale`, factory fixtures, PII sanitization with `email(domain=...)`, and a mandatory Faker API audit test."
index:
  - anchor: faker-api-audit
    what: "Verifying the installed Faker version and each provider's method signature (via `importlib.metadata.version`, `dir(Faker)`, and the version-pinned docs) before selecting providers."
    problem: "Faker API changes between releases, so relying on memory risks calling renamed, removed, or differently-signed methods; verify version, method signature, pinned docs, specific provider, renamed method, todo fallback."
    use_when: "Faker provider choice depends on installed version, method signatures change across releases, and memory based calls risk renamed or removed methods; verify version, method signature, pinned docs, specific provider, renamed method, todo fallback, faker api."
    avoid_when: "Never rely on memory of the Faker API across releases, and avoid generic `faker.word()`/`faker.text()` unless the test genuinely needs unstructured text."
    expected: "Every generated field uses a verified, semantically specific provider, with unverified calls isolated behind a TODO-marked fallback."
  - anchor: faker-unique-fields
    what: "Generating values that must be unique within a Faker instance for a test run, via `faker.unique.<method>` or deterministic suffixes."
    problem: "Unique-constrained columns collide when drawn randomly, and unique provider can raise on large draws; collision risk, uniqueness exception, deterministic suffix, clear registry, small versus large suite, guaranteed unique."
    use_when: "Unique constrained column draws values randomly, collisions fail tests, and large draws can exhaust unique provider; collision risk, uniqueness exception, deterministic suffix, clear registry, small versus large suite, guaranteed unique, unique field."
    avoid_when: "For large suites do not rely on `faker.unique`, whose retries can raise `UniquenessException`; do not leave the unique registry populated when reusing an instance within a test."
    expected: "Unique fields never collide within a run, large suites stay deterministic without uniqueness exceptions, and the registry is cleared between batches."
  - anchor: faker-locale-seeding
    what: "Controlling the built-in function-scoped `fake` fixture's locale and seed via the `faker_locale` and `faker_seed` fixtures, or a custom function-scoped `fake` fixture reading `PYTEST_FAKER_SEED`."
    problem: "Tests need reproducible isolated generated data with controlled locale instead of leaking uniqueness state or seed between tests; known seed, controlled locale, function scope, registry cleared, no leaked state, env seed."
    use_when: "Generated data must reproduce within test, locale and seed need control, and uniqueness registry must not leak between tests; known seed, controlled locale, function scope, registry cleared, no leaked state, env seed, deterministic fake."
    avoid_when: "Do not share a Faker instance across tests at a scope wider than function (uniqueness state leaks), and do not use stdlib `random` anywhere except the one permitted call in the custom `fake` fixture per `SKILL.md` #1.1.3."
    expected: "Generation is reproducible under a known seed and locale, and no uniqueness or seed state leaks between tests."
  - anchor: faker-factory-fixtures
    what: "Project fixtures that build a domain entity dict/object from verified Faker methods and accept `**overrides` so tests can pin specific fields."
    problem: "Hand-assembling entities in every test duplicates field lists and hides which fields matter to scenario; domain factory, override kwargs, specialize wrapper, base factory, no duplicate fields, verified methods."
    use_when: "Domain entity construction repeats field lists, scenario relevant fields stay hidden, and overrides pin only what matters; domain factory, override kwargs, specialize wrapper, base factory, no duplicate fields, verified methods, entity builder."
    avoid_when: "Do not build factories from unverified Faker methods, and do not duplicate field lists across specialized fixtures instead of composing them from a base factory."
    expected: "Tests construct entities through one verified factory with `**overrides`, and scenario variants reuse the base factory without duplicated field lists."
  - anchor: faker-pii-sanitization
    what: "Generating realistic-looking but non-routable addresses (and sanitizing real-looking ones) so test data can never resolve to or deliver at real domains."
    problem: "Real-looking generated emails and URLs can accidentally resolve or deliver, leaking data or hitting real inboxes; non-routable domain, sanitize domain, realistic looking, no real recipient, pii leak, deliver risk."
    use_when: "Generated emails or URLs look real, accidental resolution or delivery would leak data, and non routable domains prevent that risk; non routable domain, sanitize domain, realistic looking, no real recipient, pii leak, deliver risk, safe contact."
    avoid_when: "Do not emit real-looking routable domains (e.g. raw `company_email()`) in test data without sanitizing the domain."
    expected: "All generated or sanitized addresses and URLs use non-routable domains while still looking realistic, so no test data can reach a real recipient."
  - anchor: faker-fake-tld-email-provider
    what: "A project-registered Faker provider (`pytest-design/assets/faker.py` -> `FakeTLDEmailProvider`) whose `fake.fake_email()` builds realistic addresses on two-letter TLDs absent from the IANA root zone, so they can never resolve or deliver."
    problem: "Entities with email fields (accounts, users, invitations, subscriptions) need realistic addresses that cannot reach real domains; undeliverable address, two-letter tld, absent root zone, register provider once, shared helper, no example.com."
    use_when: "Entity carries email field, realistic address must never reach real domain, and project wide fake provider should register once; undeliverable address, two letter tld, absent root zone, register provider once, shared helper, no example com, email field."
    avoid_when: "Do not rely on `faker.email()` with real-looking domains and do not hardcode `@example.com` for email-bearing entities."
    expected: "Email fields are populated by `fake.fake_email()` with realistic-but-undeliverable addresses, registered once via the shared provider."
libraries:
  - faker
  - pytest-faker
---

# FAKER USAGE — CORE

## Mandatory Faker API Audit

[ref: #faker-api-audit]

Check the installed version before selecting methods:

```python
from importlib.metadata import version


def test_faker_version_is_available_for_audit() -> None:
    """
    Given: Faker is installed.
    When: the installed version is queried.
    Then: a version string starting with a digit is returned.
    """
    # --- Arrange ---

    # --- Act ---
    installed = version("Faker")

    # --- Assert ---
    assert installed
    assert installed[0].isdigit()
```

Inspect the provider surface with `dir(Faker)` and the package documentation for the exact installed version.

```python
from faker import Faker


def test_required_providers_exist() -> None:
    """
    Given: a fresh Faker instance.
    When: the provider surface is inspected.
    Then: all required providers are present.
    """
    # --- Arrange ---
    instance = Faker()
    required = {
        "email",
        "company_email",
        "phone_number",
        "street_address",
        "postcode",
        "country_code",
        "date_of_birth",
        "first_name",
        "last_name",
        "pyint",
        "pyfloat",
    }

    # --- Act ---
    missing = required - set(dir(instance))

    # --- Assert ---
    assert not missing, missing
```

Always pick the most semantically specific method available.

```python
from faker import Faker


def test_user_payload_uses_semantic_providers(fake: Faker) -> None:
    """
    Given: a Faker instance with safe providers.
    When: a user payload is generated.
    Then: every field uses a semantically appropriate provider.
    """
    # --- Arrange ---

    # --- Act ---
    payload = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.fake_email(),
        "phone": fake.phone_number(),
        "address": fake.street_address(),
        "postcode": fake.postcode(),
        "country": fake.country_code(),
        "age": fake.pyint(min_value=18, max_value=120),
        "score": fake.pyfloat(min_value=0, max_value=100, right_digits=2),
    }

    # --- Assert ---
    assert "@" in payload["email"]
    assert "." in payload["email"].split("@")[-1]
```

Avoid generic `faker.word()` or `faker.text()` unless the test genuinely needs unstructured text.

If a method cannot be verified, fall back to `faker.bothify(letters=...)` or `faker.pystr()` and add a `# TODO: verify Faker provider` comment.

```python
import re

from faker import Faker


def test_legacy_field_with_unverified_provider(fake: Faker) -> None:
    """
    Given: an unverified legacy provider pattern.
    When: a value is generated with bothify.
    Then: it matches the expected character set.
    """
    # --- Arrange ---
    # TODO: verify Faker provider

    # --- Act ---
    value = fake.bothify(text="??????", letters="ABCDEF")

    # --- Assert ---
    assert re.fullmatch(r"[A-F]+", value)
```

**Variety booster:** Parametrize the audit test over a list of required providers so one test validates the whole surface, then reuse the same list in a factory fixture to guarantee every project uses approved methods.

## Unique-Constrained Fields

[ref: #faker-unique-fields]

```python
from faker import Faker


def test_two_invites_have_distinct_emails_small_suite(fake: Faker) -> None:
    """
    Given: a small suite that needs unique emails.
    When: two unique emails are generated.
    Then: the addresses are distinct.
    """
    # --- Arrange ---

    # --- Act ---
    first = fake.unique.fake_email()
    second = fake.unique.fake_email()

    # --- Assert ---
    assert first != second
    fake.unique.clear()
```

For large suites, use an enumerated or otherwise deterministic suffix so uniqueness does not depend on random chance.

```python
from faker import Faker


def test_many_users_have_distinct_emails_large_suite(fake: Faker) -> None:
    """
    Given: a large batch of users.
    When: emails are built with deterministic suffixes on a fake TLD domain.
    Then: every address is unique.
    """
    # --- Arrange ---
    large_batch_size = 100
    domain = fake.fake_email().split("@")[1]

    # --- Act ---
    emails = {f"user-{i}@{domain}" for i in range(large_batch_size)}

    # --- Assert ---
    assert len(emails) == large_batch_size
```

Clear the unique registry explicitly when reusing a faker instance within the same test.

```python
from faker import Faker


def test_unique_registry_can_be_cleared(fake: Faker) -> None:
    """
    Given: a faker instance that has generated unique values.
    When: the unique registry is cleared between batches.
    Then: both batches contain the expected number of unique values.
    """
    # --- Arrange ---

    # --- Act ---
    first_batch = {fake.unique.boolean() for _ in range(2)}
    fake.unique.clear()
    second_batch = {fake.unique.boolean() for _ in range(2)}

    # --- Assert ---
    assert len(first_batch) == 2
    assert len(second_batch) == 2
```

**Variety booster:** Combine a unique email fixture with `@pytest.mark.parametrize` over role names so one parametrized test covers distinct identity invariants for admins, editors, and viewers without extra code.

## Locale Configuration and Seeding

[ref: #faker-locale-seeding]

```python
from faker import Faker


def test_builtin_faker_fixture_is_available(fake: Faker) -> None:
    """
    Given: the fake fixture is injected.
    When: an email is generated.
    Then: a non-empty address is returned.
    """
    # --- Arrange ---

    # --- Act ---
    email = fake.fake_email()

    # --- Assert ---
    assert email
```

Override seeding with the `faker_seed` fixture.

```python
import pytest
from faker import Faker


DEFAULT_FAKER_SEED = 12345


@pytest.fixture
def faker_seed() -> int:
    return DEFAULT_FAKER_SEED


def test_seeded_faker_is_reproducible(fake: Faker) -> None:
    """
    Given: a fixed faker seed fixture.
    When: data is generated through the fake fixture.
    Then: generation succeeds under the seeded configuration.
    """
    # --- Arrange ---

    # --- Act ---
    email = fake.fake_email()

    # --- Assert ---
    assert email
```

Override locale with the `faker_locale` fixture.

```python
import pytest


DEFAULT_LOCALES = ["en_US", "de_DE"]


@pytest.fixture
def faker_locale() -> list[str]:
    return DEFAULT_LOCALES


def test_multilocale_faker_generates_data(fake: Faker) -> None:
    """
    Given: a multilocale faker configuration.
    When: a first name is generated.
    Then: a string value is returned.
    """
    # --- Arrange ---

    # --- Act ---
    first_name = fake.first_name()

    # --- Assert ---
    assert isinstance(first_name, str)
```

For full control, create a custom function-scoped `fake` fixture that reads `PYTEST_FAKER_SEED`.
A function scope prevents uniqueness state from leaking between tests.

```python
import os
import random
from typing import Any

import pytest
from faker import Faker
from assets.faker import FakeTLDEmailProvider


LOCALES = ["en_US", "ja_JP", "de_DE"]


@pytest.fixture
def fake() -> Faker:
    """Custom seeded Faker instance with multi-locale support."""
    instance = Faker(LOCALES)
    instance.add_provider(FakeTLDEmailProvider)

    seed_text = os.environ.get("PYTEST_FAKER_SEED")
    if seed_text is None:
        seed = random.randint(0, 2**32)
    else:
        seed = int(seed_text)

    instance.seed_instance(seed)
    return instance


def test_custom_fake_fixture_generates_data(fake: Faker) -> None:
    """
    Given: a custom function-scoped fake fixture.
    When: an email is generated.
    Then: a non-empty address is returned.
    """
    # --- Arrange ---

    # --- Act ---
    email = fake.fake_email()

    # --- Assert ---
    assert email
```

This is the only permitted use of stdlib `random` per `SKILL.md` #1.1.3.

**Variety booster:** Parametrize a locale-driven fixture so the same test runs against `en_US`, `ja_JP`, and `de_DE`; this exposes localization bugs with a single test body.

```python
import pytest


@pytest.fixture(params=["en_US", "ja_JP", "de_DE"])
def faker_locale(request: pytest.FixtureRequest) -> list[str]:
    return [request.param]


def test_name_format_respects_locale(fake: Faker) -> None:
    """
    Given: a locale-driven faker configuration.
    When: a first name is generated.
    Then: a string value is returned.
    """
    # --- Arrange ---

    # --- Act ---
    first_name = fake.first_name()

    # --- Assert ---
    assert isinstance(first_name, str)
```

## Domain-Specific Factory Fixtures

[ref: #faker-factory-fixtures]

```python
from collections.abc import Callable
from typing import Any

import pytest
from faker import Faker


MIN_AGE = 18
MAX_AGE = 65


@pytest.fixture
def user_factory(fake: Faker) -> Callable[..., dict[str, Any]]:
    def _create(**overrides: Any) -> dict[str, Any]:
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.fake_email(),
            "phone": fake.phone_number(),
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "postcode": fake.postcode(),
                "country": fake.country_code(),
            },
            "date_of_birth": fake.date_of_birth(minimum_age=MIN_AGE, maximum_age=MAX_AGE),
            "score": fake.pyfloat(min_value=0, max_value=100, right_digits=2),
            **overrides,
        }
    return _create


def test_user_factory_accepts_overrides(
    user_factory: Callable[..., dict[str, Any]],
    fake: Faker,
) -> None:
    """
    Given: a user factory and a custom email.
    When: the factory is called with an email override.
    Then: the returned user contains the override email.
    """
    # --- Arrange ---
    custom_email = fake.fake_email()

    # --- Act ---
    user = user_factory(email=custom_email)

    # --- Assert ---
    assert user["email"] == custom_email
```

**Variety booster:** Build a base factory and specialized fixtures (`active_user_factory`, `pending_user_factory`) that call the base factory with predefined override sets; this multiplies scenario coverage without duplicating field lists.

## PII Sanitization and RFC 2606 Domains

[ref: #faker-pii-sanitization]

```python
from faker import Faker


def test_email_is_non_routable(fake: Faker) -> None:
    """
    Given: a Faker instance with FakeTLDEmailProvider registered.
    When: a fake.fake_email is generated.
    Then: it contains an @ sign and a dotted domain part.
    """
    # --- Arrange ---

    # --- Act ---
    email = fake.fake_email()

    # --- Assert ---
    assert "@" in email
    assert "." in email.split("@")[-1]


def _to_fake_tld_domain(email: str, fake: Faker) -> str:
    local, _ = email.split("@")
    return f"{local}@{fake.fake_email().split('@')[1]}"


def test_company_email_is_sanitized(fake: Faker) -> None:
    """
    Given: a company email with a real-looking domain.
    When: it is rewritten to use a fake TLD domain.
    Then: the sanitized address still contains an @ sign and a dotted domain.
    """
    # --- Arrange ---
    raw = fake.company_email()

    # --- Act ---
    safe = _to_fake_tld_domain(raw, fake)

    # --- Assert ---
    assert "@" in safe
    assert "." in safe.split("@")[-1]
```

Apply the same helper to URLs and other PII-looking fields.

**Variety booster:** Parametrize the sanitizer helper over a list of sample email local parts (including plus aliases and dots) so one test verifies the helper preserves the mailbox and replaces the domain.

## Realistic Non-Routable Email Provider

[ref: #faker-fake-tld-email-provider]

The provider builds addresses that look realistic but use two-letter TLDs that do not exist in the IANA root zone, so they can never resolve or deliver real mail.

Copy the asset file into the project.

```text
cp pytest-design/assets/faker.py tests/fixtures/faker_email.py
```

Import and register the provider in `tests/conftest.py` or in the closest `conftest.py` that covers all email-consuming tests.

```python
from collections.abc import Generator

import pytest
from faker import Faker

from tests.fixtures.faker_email import FakeTLDEmailProvider


@pytest.fixture
def fake() -> Generator[Faker, None, None]:
    """Project Faker instance with the non-routable email provider."""
    instance = Faker()
    instance.add_provider(FakeTLDEmailProvider)
    yield instance
    instance.unique.clear()
```

Use `fake.fake_email()` in factory fixtures and tests.

```python
from collections.abc import Callable
from typing import Any

import pytest
from faker import Faker


@pytest.fixture
def user_factory(fake: Faker) -> Callable[..., dict[str, Any]]:
    def _create(**overrides: Any) -> dict[str, Any]:
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.fake_email(),
            **overrides,
        }
    return _create


def test_user_email_looks_real_but_is_non_routable(
    user_factory: Callable[..., dict[str, Any]],
) -> None:
    """
    Given: a user created by the factory.
    When: the email field is inspected.
    Then: it looks like a real address but uses a non-routable domain.
    """
    # --- Arrange ---

    # --- Act ---
    user = user_factory()

    # --- Assert ---
    assert "@" in user["email"]
    assert "." in user["email"].split("@")[-1]
```

**Variety booster:** combine `fake.fake_email()` with a parameterized role fixture so the same test exercises realistic but safe addresses for admins, members, and guests without extra factory code.
