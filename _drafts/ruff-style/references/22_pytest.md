---
---

# Pytest

Write idiomatic pytest: clean fixture decorators, structured parametrize, precise raises/marks, and no legacy unittest idioms.

## Rule of thumb

1. Import pytest as `import pytest` and access every member through the module; no aliases and no `from pytest import ...`.
2. Keep fixtures minimal: bare decorator when argument-free, keyword arguments for config, omit default `scope="function"`, use `yield` only when there is teardown, and never apply test-only marks to fixtures.
3. Parametrize cleanly: a single name is a string, multiple names are a tuple, values are a list of tuple rows, and duplicate cases are removed.
4. Prefer native pytest assertions: plain `assert`, `pytest.raises`, `pytest.warns`, and `pytest.fail`; avoid unittest assertions and `assert False`.
5. Scope `raises`/`warns` tightly: pass the expected exception or warning, narrow it with `match`, and keep the context block to one simple statement.
6. Make side-effect dependencies explicit with `@pytest.mark.usefixtures`; do not inject fixtures whose values are unused, and never give test parameters default arguments.
7. When patching, use `return_value=` instead of a dummy `lambda` that ignores its arguments.

## Example: Fixtures

A junior's test module mixes old fixture syntax, redundant configuration, and marks that belong on tests.

### Bad

```python
import pytest as pt  # PT013
from pytest import fixture  # PT013


@fixture()  # PT001
def _clean_temp():
    yield  # PT022


@pt.fixture("module")  # PT002
def module_db():
    return "db"


@pt.fixture(scope="function")  # PT003
def user():
    return "user"


@pt.yield_fixture()  # PT001,PT020
def legacy_resource():
    obj = "resource"
    yield obj
    obj = None


@pt.fixture()  # PT001
def finalized_resource(request):
    resource = "acquired"
    request.addfinalizer(lambda: print("cleanup"))  # PT021
    return resource


@pt.fixture()  # PT001
def no_teardown_data():
    value = {"key": "val"}
    yield value  # PT022


@pt.mark.asyncio()  # PT023,PT024
@pt.fixture()  # PT001
async def token():
    return "token"


@pt.fixture()  # PT001
def base():
    return "base"


@pt.mark.usefixtures("base")  # PT025
@pt.fixture()  # PT001
def derived(base):
    return base + "-derived"
```

### Good

```python
import pytest


@pytest.fixture
def _clean_temp():
    return None


@pytest.fixture(scope="module")
def module_db():
    return "db"


@pytest.fixture
def user():
    return "user"


@pytest.fixture
def legacy_resource():
    obj = "resource"
    yield obj
    obj = None


@pytest.fixture
def finalized_resource():
    resource = "acquired"
    yield resource
    print("cleanup")


@pytest.fixture
def no_teardown_data():
    return {"key": "val"}


@pytest.fixture
async def token():
    return "token"


@pytest.fixture
def base():
    return "base"


@pytest.fixture
def derived(base):
    return base + "-derived"
```

### Violations

1. **PT001** — `@fixture()`, `@pt.fixture()` on `finalized_resource`, `no_teardown_data`, `token`, `base`, `derived`, and `@pt.yield_fixture()`; argument-free fixture decorators should be bare.
2. **PT002** — `@pt.fixture("module")`; fixture configuration should use keyword arguments.
3. **PT003** — `@pt.fixture(scope="function")`; default scope is noise.
4. **PT013** — `import pytest as pt` and `from pytest import fixture`; pytest should be imported as `import pytest`.
5. **PT020** — `@pt.yield_fixture()`; the yield_fixture decorator is deprecated.
6. **PT021** — `request.addfinalizer(lambda: print("cleanup"))`; prefer `yield` teardown over callbacks.
7. **PT022** — bare `yield` in `_clean_temp` and `yield value` in `no_teardown_data`; no teardown follows, so use `return`.
8. **PT023** — `@pt.mark.asyncio()`; empty marker parentheses are unnecessary.
9. **PT024** — `@pt.mark.asyncio()` on a fixture; the asyncio mark is for tests, not fixtures.
10. **PT025** — `@pt.mark.usefixtures("base")` on a fixture; `usefixtures` has no effect on fixtures.

## Example: Parametrize and marks

The same junior uses inconsistent parametrize containers, duplicate rows, and empty marker parentheses.

### Bad

```python
import pytest


@pytest.mark.slow()  # PT023
def test_heavy():
    assert True


@pytest.mark.usefixtures()  # PT023,PT026
def test_something():
    assert True


@pytest.mark.parametrize(("param",), [1, 2, 3])  # PT006
def test_single(param): ...


@pytest.mark.parametrize(["a", "b"], [(1, 2)])  # PT006
def test_multi(a, b): ...


@pytest.mark.parametrize("param", (1, 2, 3))  # PT007
def test_tuple_values(param): ...


@pytest.mark.parametrize(("a", "b"), [[1, 2], [3, 4]])  # PT007
def test_list_rows(a, b): ...


@pytest.mark.parametrize(("a", "b"), [(1, 2), (1, 2), (3, 4)])  # PT014
def test_add(a, b):
    assert a + b > 0
```

### Good

```python
import pytest


@pytest.mark.slow
def test_heavy():
    assert True


def test_something():
    assert True


@pytest.mark.parametrize("param", [1, 2, 3])
def test_single(param): ...


@pytest.mark.parametrize(("a", "b"), [(1, 2)])
def test_multi(a, b): ...


@pytest.mark.parametrize("param", [1, 2, 3])
def test_tuple_values(param): ...


@pytest.mark.parametrize(("a", "b"), [(1, 2), (3, 4)])
def test_list_rows(a, b): ...


@pytest.mark.parametrize(("a", "b"), [(1, 2), (3, 4)])
def test_add(a, b):
    assert a + b > 0
```

### Violations

1. **PT006** — `("param",)` and `["a", "b"]`; a single parametrize name should be a string, multiple names should be a tuple.
2. **PT007** — `(1, 2, 3)` and `[[1, 2], [3, 4]]`; parametrize values should be a list and rows should be tuples.
3. **PT014** — `(1, 2), (1, 2)`; duplicate test cases add no coverage.
4. **PT023** — `@pytest.mark.slow()` and `@pytest.mark.usefixtures()`; empty marker parentheses are unnecessary.
5. **PT026** — `@pytest.mark.usefixtures()`; useless without fixture names.

## Example: Native asserts and unittest migration

A test file drags in unittest habits, composite assertions, and forced-failure patterns.

### Bad

```python
import unittest
import pytest


class TestMath(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(1 + 1, 2)  # PT009

    def test_divide(self):
        with self.assertRaises(ZeroDivisionError):  # PT027
            1 / 0


def test_parse():
    try:
        1 / 0
    except ZeroDivisionError as exc:
        assert str(exc) == "division by zero"  # PT017


def test_user(user):
    assert user.is_active and user.is_verified  # PT018


def test_guard(some_condition):
    if some_condition:
        assert False, "unexpected condition"  # PT015


def test_something():
    pytest.fail()  # PT016
```

### Good

```python
import pytest


def test_equal():
    assert 1 + 1 == 2


def test_divide():
    with pytest.raises(ZeroDivisionError):
        1 / 0


def test_parse():
    with pytest.raises(ZeroDivisionError) as exc_info:
        1 / 0
    assert str(exc_info.value) == "division by zero"


def test_user(user):
    assert user.is_active
    assert user.is_verified


def test_guard(some_condition):
    if some_condition:
        pytest.fail("unexpected condition")


def test_something():
    pytest.fail("input did not satisfy precondition")
```

### Violations

1. **PT009** — `self.assertEqual(1 + 1, 2)`; use a plain `assert` for pytest introspection.
2. **PT015** — `assert False, "unexpected condition"`; use `pytest.fail` to force a failure.
3. **PT016** — `pytest.fail()`; `pytest.fail` needs a message.
4. **PT017** — `assert str(exc) == "..."` inside an `except` block; use `pytest.raises` so the test fails when no exception is raised.
5. **PT018** — `assert user.is_active and user.is_verified`; composite assertions hide which condition failed.
6. **PT027** — `self.assertRaises(ZeroDivisionError)`; use `pytest.raises` instead of unittest-style raises.

## Example: Raises

Exception expectations are left broad, empty, or crowded with unrelated statements.

### Bad

```python
import pytest


def open_db():
    return "db"


def write_row(db):
    raise IOError("locked")


def test_fail():
    with pytest.raises():  # PT010
        raise ValueError("boom")


def test_parse():
    with pytest.raises(ValueError):  # PT011
        int("not a number")


def test_save():
    with pytest.raises(IOError):  # PT011,PT012
        open_db()
        write_row("db")
```

### Good

```python
import pytest


def open_db():
    return "db"


def write_row(db):
    raise IOError("locked")


def test_fail():
    with pytest.raises(ValueError, match="boom"):
        raise ValueError("boom")


def test_parse():
    with pytest.raises(ValueError, match="invalid literal"):
        int("not a number")


def test_save():
    db = open_db()
    with pytest.raises(IOError, match="locked"):
        write_row(db)
```

### Violations

1. **PT010** — `pytest.raises()`; missing expected exception.
2. **PT011** — `pytest.raises(ValueError)` and `pytest.raises(IOError)`; too broad, narrow with `match` or a more specific exception.
3. **PT012** — `open_db(); write_row("db")` inside `pytest.raises`; only the statement expected to raise belongs in the block.

## Example: Warns

Warning expectations repeat the same broad-and-crowded mistakes as the raises example.

### Bad

```python
import pytest
import warnings


def deprecated_call():
    warnings.warn("old", DeprecationWarning)


def setup():
    pass


def test_warn_bare():
    with pytest.warns():  # PT029
        deprecated_call()


def test_warn_broad():
    with pytest.warns(Warning):  # PT030
        deprecated_call()


def test_warn_multiple():
    with pytest.warns(DeprecationWarning):  # PT030,PT031
        setup()
        deprecated_call()
```

### Good

```python
import pytest
import warnings


def deprecated_call():
    warnings.warn("old", DeprecationWarning)


def setup():
    pass


def test_warn_bare():
    with pytest.warns(DeprecationWarning, match="old"):
        deprecated_call()


def test_warn_broad():
    with pytest.warns(DeprecationWarning, match="old"):
        deprecated_call()


def test_warn_multiple():
    setup()
    with pytest.warns(DeprecationWarning, match="old"):
        deprecated_call()
```

### Violations

1. **PT029** — `pytest.warns()`; missing expected warning category.
2. **PT030** — `pytest.warns(Warning)` and `pytest.warns(DeprecationWarning)`; too broad, narrow with `match` or a more specific warning.
3. **PT031** — `setup(); deprecated_call()` inside `pytest.warns`; only the statement expected to warn belongs in the block.

## Example: Mocks and test signatures

A junior misuses fixture injection for side effects, patches with a lambda, and gives a test parameter a default value.

### Bad

```python
import pytest


@pytest.fixture
def _patch_env():
    pass


def test_env(_patch_env):  # PT019
    assert True


def test_fetch(mocker):
    mocker.patch("app.client.get", lambda url: {"ok": True})  # PT008


def test_scale(value=1):  # PT028
    assert value > 0
```

### Good

```python
import pytest


@pytest.fixture
def _patch_env():
    pass


@pytest.mark.usefixtures("_patch_env")
def test_env():
    assert True


def test_fetch(mocker):
    mocker.patch("app.client.get", return_value={"ok": True})


def test_scale(value):
    assert value > 0
```

### Violations

1. **PT008** — `mocker.patch(..., lambda url: {"ok": True})`; use `return_value` instead of a dummy lambda.
2. **PT019** — `test_env(_patch_env)`; unused fixture parameter should be replaced by `@pytest.mark.usefixtures`.
3. **PT028** — `test_scale(value=1)`; test parameters must not have default arguments.
