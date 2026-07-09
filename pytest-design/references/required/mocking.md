---
subject: "Pick the lightest double and isolate boundaries: prefer fakes/stubs, then spies, then mocks; `mocker.patch.object` over string-path `mocker.patch`, `autospec=True`/`spec_set=True`/`spec=...`, `mocker.spy`/`mocker.stub`, `return_value`/`side_effect`, `monkeypatch` for env/config/attributes, `mock_open` for text reads, `AsyncMock` for async boundaries; `Mock`/`MagicMock`/`PropertyMock`/`ANY`/`DEFAULT`/`call`/`sentinel`."
index:
  - anchor: mocking-test-double-hierarchy
    what: "Choosing the lightest test double (fake < stub < mock/spy) that satisfies the scenario, because heavier doubles couple tests to implementation details."
    problem: "Over-using mocks and spies ties tests to internal interactions and makes refactors break tests unnecessarily; lightest double, fake cheap, stub canned, mock boundary, public api only, no private patch."
    use_when: "Collaborator stand in can be fake, stub, spy, or mock, heavier doubles couple to implementation, and lightest working double protects refactors; lightest double, fake cheap, stub canned, mock boundary, public api only, no private patch."
    avoid_when: "Never patch or assert on private methods — test through the public API; do not reach for a mock when a fake or stub would do."
    expected: "Each test uses the lightest double that meets the need, interactions are verified only at system boundaries, and the public API is the only surface under test."
  - anchor: mocking-mocker-fixture
    what: "The `pytest-mock` `mocker` fixture that wraps `unittest.mock` (exposing `mocker.patch`, `mocker.patch.object`, `mocker.patch.multiple`, `mocker.patch.dict`, `mocker.stopall`, `mocker.resetall`, `mocker.spy`, `mocker.stub`, and the `Mock`/`MagicMock`/`AsyncMock`/`PropertyMock`/`ANY`/`DEFAULT`/`call`/`sentinel`/`mock_open` objects) and stops every patch automatically at test end."
    problem: "Manual patch start without guaranteed stop leaks patches across failures and into later tests; automatic stop, no manual start, wrap mock, cleanup on failure, no leaked patch, fixture managed."
    use_when: "Test replaces attributes objects or dict entries, manual patch start may leak after failure, and fixture managed stop cleans automatically; automatic stop, no manual start, wrap mock, cleanup on failure, no leaked patch, fixture managed, mocker."
    avoid_when: "Do not mix `mocker` with manually created `patcher.start()` calls that may leak across failures."
    expected: "Every patch is stopped automatically when the test ends, with no manual start/stop and no leaked patches."
  - anchor: mocking-patch-object-vs-patch
    what: "Patching the namespace where an object is looked up (the consumer) rather than where it is defined, via `mocker.patch.object(target, 'attr')` or string-path `mocker.patch('module.attr')`."
    problem: "Patching definition module instead of consumer leaves real dependency in place, so test silently exercises production code; consumer patch, object direct, string path fallback, real dependency bound, definition-site trap, exact reference."
    use_when: "Dependency is imported into consumer namespace, patching definition module leaves real object bound, and consumer patch replaces exact reference; consumer patch, object direct, string path fallback, real dependency bound, definition site trap, exact reference."
    avoid_when: "Do not patch the definition module when the consumer imported the name — the real dependency stays bound in the consumer and the patch has no effect."
    expected: "The patch replaces the exact reference the code under test uses, so the real dependency is never exercised by accident."
  - anchor: mocking-autospec-spec-specset
    what: "Constraining a mock's shape to the real object: `autospec=True` derives API and enforces signatures, `spec=SomeClass` checks shape without signatures, and `spec_set=True` rejects attribute assignment beyond the real object."
    problem: "Unconstrained mocks accept any attribute or call signature, so tests pass against APIs that do not exist; autospec signature, spec shape, spec_set reject, stable boundary, api drift caught, dynamic attr."
    use_when: "Mock accepts any attribute or call signature, missing API would still pass, and spec constraints enforce shape; autospec signature, spec shape, spec set reject, stable boundary, api drift caught, dynamic attr, constrained mock."
    avoid_when: "Do not leave mocks unconstrained at stable boundaries (they accept non-existent methods and wrong signatures), and do not use `spec_set` when legitimate dynamic attributes are required."
    expected: "Mocks reject non-existent methods and wrong call signatures at stable boundaries, catching API drift at test time."
  - anchor: mocking-spy-and-stub
    what: "`mocker.spy` wraps a real method to record calls without replacing behavior; `mocker.stub` is a permissive callback mock that returns a configured value."
    problem: "Some tests must verify real side effect still happens, others only need controllable return value with no call verification; spy record real, stub return value, call verify, safe side effect, no call count, controllable result."
    use_when: "Real side effect must still happen and calls need recording, or only controllable return value matters without call count; spy record real, stub return value, call verify, safe side effect, no call count, controllable result."
    avoid_when: "Do not spy on a method whose real behavior is slow, non-deterministic, or mutates global state."
    expected: "Spies record real, safe side-effect calls for verification, and stubs provide simple return values where call counts do not matter."
  - anchor: mocking-side-effect-return-value
    what: "Configuring a mock's outcome via `return_value` (static) or `side_effect` (raise an exception, call a function, or iterate a sequence for sequential calls)."
    problem: "Tests need both stable results and dynamic, sequential, or exceptional behavior from same mock surface; static return, raise side effect, iterable sequence, one mock sequential, dynamic response, no stacked mocks."
    use_when: "Mock outcome must be stable, exceptional, sequential, or dynamic, and one mock surface can express each behavior; static return, raise side effect, iterable sequence, one mock sequential, dynamic response, no stacked mocks, mock outcome."
    avoid_when: "Do not use `return_value` when each call must differ or raise, and do not build sequential behavior by stacking multiple mocks when one iterable `side_effect` suffices."
    expected: "Static results use `return_value`, while exceptions and sequences use `side_effect`, giving one mock stable, dynamic, or sequential behavior as needed."
  - anchor: mocking-monkeypatch
    what: "Using the built-in `monkeypatch` fixture for temporary environment variables, configuration values, and dotted attribute replacement, all auto-reverted."
    problem: "Environment and config changes must be temporary and reverted, and mixing two cleanup mechanisms in one test causes confusion; env setattr, one mechanism, auto revert, no patch dict environ, config temporary, single cleanup."
    use_when: "Environment or config must change temporarily, two cleanup mechanisms in one test confuse teardown, and monkeypatch auto reverts; env setattr, one mechanism, auto revert, no patch dict environ, config temporary, single cleanup, monkeypatch."
    avoid_when: "Avoid using `mocker.patch.dict(os.environ, ...)` in the same test that already uses `monkeypatch` — two cleanup mechanisms invite confusion."
    expected: "Environment and config changes are applied via one mechanism (`monkeypatch`) and reverted automatically, with no competing cleanup path."
  - anchor: mocking-mock-open
    what: "`mock_open` as a configurable stand-in for built-in `open` (with iteration and context-manager support) for small text reads."
    problem: "Tests reading small text via open do not need real file, but large, binary, or stable content fits real temp file better; small text read, configurable open, iteration context, real temp large, binary content, faithful file."
    use_when: "Code reads small text through open, real file is unnecessary, and large binary or stable content fits temp file better; small text read, configurable open, iteration context, real temp large, binary content, faithful file, mock open."
    avoid_when: "Do not use `mock_open` for large, binary, or version-controlled content where a real `tmp_path` file is clearer and more faithful."
    expected: "Small text reads are patched with `mock_open`, while substantial or binary content uses a real `tmp_path` file."
  - anchor: mocking-async-mock
    what: "`AsyncMock` for coroutine and `async for` boundaries, integrating with `mocker.patch` (e.g. `new_callable=AsyncMock`) like synchronous mocks."
    problem: "Async boundaries must mock as awaitables; plain mock is not awaitable and forgotten await makes await assertion fail; awaitable mock, always await, async for boundary, assert awaited, not plain mock, coroutine expected."
    use_when: "Async boundary must mock as awaitable, plain mock is not awaitable, and forgotten await makes assertion fail; awaitable mock, always await, async for boundary, assert awaited, not plain mock, coroutine expected, async mock."
    avoid_when: "Do not forget to `await` the mock inside the test (`assert_awaited_once` will not pass on a call never awaited), and do not use `MagicMock` where a coroutine is expected."
    expected: "Async boundaries are mocked as awaitables, always awaited, and verified with await-aware assertions."
libraries:
  - pytest-asyncio
  - pytest-mock
---

# MOCKING

## Test Double Hierarchy

[ref: #mocking-test-double-hierarchy]

Arrange tests with the lightest double that satisfies the scenario, because heavier doubles couple tests to implementation details.

```python
from typing import Any

import pytest
from faker import Faker


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[str, dict[str, Any]] = {}

    def add(self, user_id: str, data: dict[str, Any]) -> None:
        self._users[user_id] = data

    def get(self, user_id: str) -> dict[str, Any] | None:
        return self._users.get(user_id)


GREETING_TEMPLATE: str = "Hello, {name}"


class UserService:
    def __init__(self, repo: InMemoryUserRepository) -> None:
        self._repo = repo

    def greet(self, user_id: str) -> str:
        user = self._repo.get(user_id)
        if user is None:
            raise ValueError("Unknown user")
        return GREETING_TEMPLATE.format(name=user["name"])


def test_greet_uses_fake_repository(fake: Faker) -> None:
    """
    Given: fake repository prepopulated with a user.
    When: service greets the user.
    Then: greeting contains the user's name.
    """
    # --- Arrange ---
    repo = InMemoryUserRepository()
    service = UserService(repo)
    user_id = str(fake.uuid4())
    name = fake.name()
    repo.add(user_id, {"name": name})

    # --- Act ---
    result = service.greet(user_id)

    # --- Assert ---
    assert result == GREETING_TEMPLATE.format(name=name)
```

**Variety booster:** Replace the Fake repository with a Stub that returns a fixed record when the contract is read-only and the test only needs a single lookup path.

## `mocker` Fixture and Cleanup

[ref: #mocking-mocker-fixture]

The `mocker` fixture from `pytest-mock` wraps `unittest.mock` and automatically stops every patch when the test ends.

```python
from typing import Any

from faker import Faker
from pytest_mock import MockerFixture
from unittest.mock import ANY


class PaymentGateway:
    def charge(self, amount: int, currency: str) -> dict[str, str]:
        raise NotImplementedError


class Checkout:
    def __init__(self, gateway: PaymentGateway) -> None:
        self._gateway = gateway

    def complete(self, amount: int, currency: str) -> str:
        result = self._gateway.charge(amount, currency)
        return result["transaction_id"]


def test_checkout_uses_patched_gateway(mocker: MockerFixture, fake: Faker) -> None:
    """
    Given: patched gateway returns a transaction id.
    When: checkout completes a payment.
    Then: gateway is called with amount and currency, and transaction id is returned.
    """
    # --- Arrange ---
    gateway = PaymentGateway()
    mock_charge = mocker.patch.object(gateway, "charge", autospec=True)
    transaction_id = fake.uuid4()
    mock_charge.return_value = {"transaction_id": str(transaction_id), "status": fake.word()}
    checkout = Checkout(gateway)
    amount = fake.pyint(min_value=1, max_value=1000)
    currency = fake.currency_code()

    # --- Act ---
    result = checkout.complete(amount, currency)

    # --- Assert ---
    mock_charge.assert_called_once_with(amount, currency)
    assert result == str(transaction_id)
```

**Variety booster:** Combine `mocker.patch.multiple` with `autospec=True` to replace several attributes of the same target in a single call.

## `mocker.patch.object` versus `mocker.patch`

[ref: #mocking-patch-object-vs-patch]

Patch the namespace where the object is looked up, not the namespace where it is defined.

```python
from types import ModuleType
from unittest.mock import ANY

from faker import Faker
from pytest_mock import MockerFixture


def send_email(to: str, subject: str, body: str) -> None:
    raise NotImplementedError


billing = ModuleType("billing")
billing.send_email = send_email


INVOICE_SUBJECT: str = "Invoice"
INVOICE_BODY: str = "You owe us"


class BillingService:
    def invoice_customer(self, email: str) -> None:
        billing.send_email(email, INVOICE_SUBJECT, INVOICE_BODY)


def test_invoice_customer_patches_consumer_namespace(mocker: MockerFixture, fake: Faker) -> None:
    """
    Given: billing send_email is patched in the consumer namespace.
    When: service invoices a customer.
    Then: send_email is called with email, subject, and body.
    """
    # --- Arrange ---
    mock_send = mocker.patch.object(billing, "send_email", autospec=True)
    email = fake.fake_email()

    # --- Act ---
    BillingService().invoice_customer(email)

    # --- Assert ---
    mock_send.assert_called_once_with(email, INVOICE_SUBJECT, INVOICE_BODY)
```

**Variety booster:** Parameterize the patch target across tests that exercise both success and failure paths at the same boundary.

## `autospec`, `spec`, and `spec_set`

[ref: #mocking-autospec-spec-specset]

`autospec=True` derives the mock's API from the real object, so tests fail when non-existent methods or wrong signatures are used.

```python
from typing import Any

import pytest
from faker import Faker
from pytest_mock import MockerFixture
from unittest.mock import Mock


class AuditLogger:
    def log_event(self, event: str, user_id: str) -> None:
        raise NotImplementedError


def test_autospec_rejects_wrong_signature(mocker: MockerFixture, fake: Faker) -> None:
    """
    Given: logger method is patched with autospec.
    When: method is called with valid arguments.
    Then: mock records the expected call.
    """
    # --- Arrange ---
    logger = AuditLogger()
    mock_log = mocker.patch.object(logger, "log_event", autospec=True)
    event = fake.word()
    user_id = str(fake.uuid4())

    # --- Act ---
    logger.log_event(event, user_id)

    # --- Assert ---
    mock_log.assert_called_once_with(event, user_id)


def test_spec_set_rejects_unknown_attributes() -> None:
    """
    Given: mock logger created with spec_set=AuditLogger.
    When: existing method is accessed and unknown method is accessed.
    Then: existing method works, unknown method raises AttributeError.
    """
    # --- Arrange ---
    mock_logger = Mock(spec_set=AuditLogger)

    # --- Act ---
    _ = mock_logger.log_event

    # --- Assert ---
    with pytest.raises(AttributeError):
        _ = mock_logger.nonexistent_method
```

**Variety booster:** Pass `spec_set=True` when the mock represents an immutable configuration object to catch accidental attribute creation.

## `mocker.spy` and `mocker.stub`

[ref: #mocking-spy-and-stub]

A spy wraps a real method to record calls without replacing behavior; a stub is a permissive callback mock that can stand in for a function with a custom return value.

```python
from faker import Faker
from pytest_mock import MockerFixture


class MetricsClient:
    def increment(self, counter: str) -> None:
        return None


class OrderProcessor:
    _STARTED_COUNTER: str = "order.started"

    def __init__(self, metrics: MetricsClient) -> None:
        self._metrics = metrics

    def process(self, order_id: str) -> str:
        self._metrics.increment(self._STARTED_COUNTER)
        return order_id


def test_spy_records_real_call(mocker: MockerFixture, fake: Faker) -> None:
    """
    Given: order processor with real metrics client and a spy on increment.
    When: order is processed.
    Then: spy records the counter call and order id is returned.
    """
    # --- Arrange ---
    metrics = MetricsClient()
    processor = OrderProcessor(metrics)
    spy = mocker.spy(metrics, "increment")
    order_id = str(fake.uuid4())

    # --- Act ---
    result = processor.process(order_id)

    # --- Assert ---
    spy.assert_called_once_with(OrderProcessor._STARTED_COUNTER)
    assert result == order_id


def test_stub_provides_callback_value(mocker: MockerFixture, fake: Faker) -> None:
    """
    Given: stub configured to return a generated price.
    When: stub is called with a product id.
    Then: configured price is returned.
    """
    # --- Arrange ---
    stub = mocker.stub(name="price_resolver")
    product_id = str(fake.uuid4())
    price = fake.pyint(min_value=1, max_value=1000)
    stub.return_value = price

    # --- Act ---
    result = stub(product_id)

    # --- Assert ---
    assert result == price
```

**Variety booster:** Inspect `spy_return_list` when the spied method is called multiple times with different outcomes.

## `side_effect` and Return-Value Patterns

[ref: #mocking-side-effect-return-value]

`return_value` pins a static result, while `side_effect` can raise exceptions, call a function, or iterate over a sequence.

```python
import re
from typing import Any

import pytest
from faker import Faker
from pytest_mock import MockerFixture


class PaymentGateway:
    def charge(self, amount: int, currency: str) -> dict[str, str]:
        raise NotImplementedError


class Checkout:
    def __init__(self, gateway: PaymentGateway) -> None:
        self._gateway = gateway

    def complete(self, amount: int, currency: str) -> str:
        result = self._gateway.charge(amount, currency)
        return result["transaction_id"]


def test_side_effect_iterable_yields_sequential_values(mocker: MockerFixture, fake: Faker) -> None:
    """
    Given: patched gateway returns a sequence of transaction ids.
    When: checkout is invoked for each expected id.
    Then: each call returns the next id and total call count matches.
    """
    # --- Arrange ---
    gateway = PaymentGateway()
    mock_charge = mocker.patch.object(gateway, "charge", autospec=True)
    call_count = fake.pyint(min_value=2, max_value=5)
    returns = [str(fake.uuid4()) for _ in range(call_count)]
    mock_charge.side_effect = [
        {"transaction_id": tid, "status": fake.word()} for tid in returns
    ]
    checkout = Checkout(gateway)

    # --- Act ---
    for expected_tid in returns:
        amount = fake.pyint(min_value=1, max_value=100)
        currency = fake.currency_code()
        result = checkout.complete(amount, currency)
        assert result == expected_tid

    # --- Assert ---
    assert mock_charge.call_count == call_count


def test_side_effect_raises_configurable_exception(mocker: MockerFixture, fake: Faker) -> None:
    """
    Given: patched gateway raises RuntimeError with generated message.
    When: checkout completes a payment.
    Then: RuntimeError is raised with the configured message.
    """
    # --- Arrange ---
    gateway = PaymentGateway()
    mock_charge = mocker.patch.object(gateway, "charge", autospec=True)
    message = fake.sentence()
    mock_charge.side_effect = RuntimeError(message)
    checkout = Checkout(gateway)

    # --- Act ---
    with pytest.raises(RuntimeError, match=re.escape(message)):
        checkout.complete(fake.pyint(min_value=1, max_value=100), fake.currency_code())

    # --- Assert ---
    # Exception raised as expected; assertion handled by pytest.raises context.
```

**Variety booster:** Build the iterable `side_effect` from a faker-generated list so the test exercises a variable-length sequence.

## `monkeypatch` for Environment and Config

[ref: #mocking-monkeypatch]

The built-in `monkeypatch` fixture is the right tool for temporary state changes such as environment variables, configuration values, and dotted attribute replacement.

```python
import os

import pytest
from faker import Faker


class Settings:
    API_TIMEOUT_SECONDS: int = 30
    FEATURE_FLAG: bool = False


def test_monkeypatch_changes_config(monkeypatch: pytest.MonkeyPatch, fake: Faker) -> None:
    """
    Given: settings timeout and environment variable are patched.
    When: settings and environment are read.
    Then: patched values are returned.
    """
    # --- Arrange ---
    timeout = fake.pyint(min_value=1, max_value=60)
    monkeypatch.setattr(Settings, "API_TIMEOUT_SECONDS", timeout)
    key = fake.pystr(min_chars=12, max_chars=16).upper()
    value = fake.password(length=32)
    monkeypatch.setenv(key, value)

    # --- Act ---
    timeout_result = Settings.API_TIMEOUT_SECONDS
    env_result = os.environ[key]

    # --- Assert ---
    assert timeout_result == timeout
    assert env_result == value


def test_monkeypatch_can_remove_env(monkeypatch: pytest.MonkeyPatch, fake: Faker) -> None:
    """
    Given: environment variable is set and then deleted.
    When: environment is checked.
    Then: variable is no longer present.
    """
    # --- Arrange ---
    key = fake.pystr(min_chars=12, max_chars=16).upper()
    value = fake.password(length=32)
    monkeypatch.setenv(key, value)
    monkeypatch.delenv(key)

    # --- Act ---
    present = key in os.environ

    # --- Assert ---
    assert not present
```

**Variety booster:** Yield a typed `NamedTuple` or `TypedDict` from a fixture that applies a bundle of monkeypatches and reports the patched values.

## `mock_open` for File Patching

[ref: #mocking-mock-open]

`mock_open` creates a configurable stand-in for the built-in `open` function, including iteration and context-manager support.

```python
from pathlib import Path
from unittest.mock import mock_open

from faker import Faker
from pytest_mock import MockerFixture


def _read_text_file(path: Path) -> str:
    with open(path) as handle:
        return handle.read()


def test_mock_open_reads_generated_content(mocker: MockerFixture, fake: Faker) -> None:
    """
    Given: builtins.open is patched to return generated content.
    When: text file is read through the helper.
    Then: content matches the generated text.
    """
    # --- Arrange ---
    content = fake.paragraph(nb_sentences=3)
    mocker.patch("builtins.open", mock_open(read_data=content))
    path = Path(str(fake.uuid4()))

    # --- Act ---
    result = _read_text_file(path)

    # --- Assert ---
    assert result == content
```

**Variety booster:** Parameterize `read_data` through a fixture to exercise line iteration, empty files, and decoding errors.

## Async Mocks with `AsyncMock`

[ref: #mocking-async-mock]

`AsyncMock` models coroutines and async iterators, and it integrates with `mocker.patch` exactly like synchronous mocks.

```python
import pytest
from faker import Faker
from pytest_mock import MockerFixture
from unittest.mock import AsyncMock


class AsyncStore:
    async def fetch(self, key: str) -> str:
        raise NotImplementedError


class Cache:
    def __init__(self, store: AsyncStore) -> None:
        self._store = store

    async def get(self, key: str) -> str:
        return await self._store.fetch(key)


@pytest.mark.asyncio
async def test_async_mock_for_awaitable_boundary(
    mocker: MockerFixture,
    fake: Faker,
) -> None:
    """
    Given: async store fetch is patched with AsyncMock.
    When: cache retrieves a value.
    Then: fetch is awaited once with the key and value is returned.
    """
    # --- Arrange ---
    store = AsyncStore()
    mock_fetch = mocker.patch.object(store, "fetch", new_callable=AsyncMock)
    value = fake.sentence()
    mock_fetch.return_value = value
    cache = Cache(store)
    key = fake.word()

    # --- Act ---
    result = await cache.get(key)

    # --- Assert ---
    mock_fetch.assert_awaited_once_with(key)
    assert result == value
```

**Variety booster:** Combine `AsyncMock` with `side_effect` returning an async generator to simulate paginated async responses.
