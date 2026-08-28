---
---

# Naming

PEP 8 names everywhere: no builtin shadowing, CapWords classes, snake_case functions, and unambiguous aliases.

## Rule of thumb

1. Use `snake_case` for modules, functions, methods, arguments, and variables; use `CapWords` for classes and end custom exceptions with `Error`.
2. Never shadow builtins, stdlib modules, or imports; pick a synonym or add a suffix instead.
3. Name method receivers `self` for instance methods and `cls` for class methods.
4. Keep import aliases in the same naming family as the imported name: constants stay `UPPER_CASE`, classes stay `CapWords`, functions stay `snake_case`.
5. Use ASCII-only identifiers and module names; avoid `l`, `O`, and `I` as names.

## Example: Builtin shadowing

**Config:** pair1

A config loader that names things after builtins and collides with the standard library.

### Bad

```python
# File: json.py  # A005

from rich import print  # A004
from collections import OrderedDict as dict  # A004,N813


def load_config(input, id):  # A002
    id = 1  # A001
    print(f"{input}: {id}")
    return id


class ConfigParser:
    def dict(self):
        return {}

    def parse(self) -> dict[str, str]:  # A003
        return {}


first = (lambda list: list[0])(["a", "b"])  # A006
print(first)
```

### Good

```python
# File: config_loader.py
"""Load JSON configs with rich output."""

from rich import print as rich_print


def load_config(user_input, request_id):
    rich_print(f"{user_input}: {request_id}")
    return request_id


class ConfigParser:
    def to_dict(self):
        return {}

    def parse(self) -> dict[str, str]:
        return {}


first = (lambda items: items[0])(["a", "b"])
rich_print(first)
```

### Violations

1. **A001** — `id = 1`; local variable shadows the builtin `id`.
2. **A002** — `input`, `id`; function arguments shadow the builtins `input` and `id`.
3. **A003** — `-> dict[str, str]` in a class defining `dict()`; the class attribute shadows the builtin where it is referenced.
4. **A004** — `from rich import print`, `from collections import OrderedDict as dict`; imports shadow the builtins `print` and `dict`.
5. **A005** — `json.py`; module name shadows the standard-library `json`.
6. **A006** — `lambda list`; lambda argument shadows the builtin `list`.

## Example: Ambiguous single-letter names

A helper that uses visually confusable letters as class, function, and variable names.

### Bad

```python
class I:  # E742
    pass


def l(items):  # E743
    return len(items)


def count(lines):
    O = len(lines)  # E741,N806
    for l in lines:  # E741
        O += l  # E741,N806
    return O
```

### Good

```python
class Index:
    pass


def length(items):
    return len(items)


def count(lines):
    offset = len(lines)
    for line in lines:
        offset += line
    return offset
```

### Violations

1. **E741** — `l`, `O`; ambiguous single-letter variable names look like digits.
2. **E742** — `class I`; ambiguous single-letter class name.
3. **E743** — `def l`; ambiguous single-letter function name.

## Example: PEP 8 casing

A module that ignores PEP 8 casing rules for classes, functions, variables, and exceptions.

### Bad

```python
myVariable = "global"  # N816


class my_class:  # N801
    defaultTimeout = 30  # N815

    @classmethod
    def create(self, name):  # N804
        return self(name)

    def ComputeTotal(cls, Price):  # N802,N803,N805
        Tax = Price * 0.2  # N806
        return Price + Tax

    def __str__(self):
        return "my_class"


class Validation(Exception):  # N818
    pass


def __internal_helper__():  # N807
    return 42
```

### Good

```python
my_variable = "global"


class MyClass:
    default_timeout = 30

    @classmethod
    def create(cls, name):
        return cls(name)

    def compute_total(self, price):
        tax = price * 0.2
        return price + tax

    def internal_helper(self):
        return 42


class ValidationError(Exception):
    pass
```

### Violations

1. **N801** — `class my_class`; class names should use CapWords.
2. **N802** — `ComputeTotal`; function names should be snake_case.
3. **N803** — `Price`; argument names should be snake_case.
4. **N804** — `self` in `@classmethod def create`; classmethod first argument should be `cls`.
5. **N805** — `cls` in instance method `ComputeTotal`; instance method first argument should be `self`.
6. **N806** — `Tax`; local variable in function should be lowercase.
7. **N807** — `def __internal_helper__()`; only documented dunder methods are allowed.
8. **N815** — `defaultTimeout`; class-scope variable should not be mixedCase.
9. **N816** — `myVariable`; global variable should not be mixedCase.
10. **N818** — `Validation`; custom exception names should end with `Error`.

## Example: Import alias casing

A junior's model layer that renames imports into the wrong naming family.

### Bad

```python
from config import MAX_RETRIES as MaxRetries  # N811
from utils import my_helper as MyHelper  # N812
from models import UserAccount as useraccount  # N813
from models import UserAccount as USER_ACCOUNT  # N814
from models import UserAccount as UA  # N817
```

### Good

```python
from config import MAX_RETRIES
from utils import my_helper
from models import UserAccount
```

### Violations

1. **N811** — `MAX_RETRIES as MaxRetries`; constant imported as non-constant.
2. **N812** — `my_helper as MyHelper`; lowercase imported as non-lowercase.
3. **N813** — `UserAccount as useraccount`; CamelCase imported as lowercase.
4. **N814** — `UserAccount as USER_ACCOUNT`; CamelCase imported as constant.
5. **N817** — `UserAccount as UA`; CamelCase imported as acronym.

## Example: Invalid module name

**Config:** pair5

A utility file saved with a hyphenated, CamelCase name that is not a valid Python module.

### Bad

```python
# File: My-Module.py  # N999

"""Helper utilities."""


def run():
    pass
```

### Good

```python
# File: my_module.py
"""Helper utilities."""


def run():
    pass
```

### Violations

1. **N999** — `My-Module.py`; module name is not a valid lowercase snake_case identifier.

## Example: Non-ASCII identifiers

A snippet that uses accented characters in an imported module name and a variable.

### Bad

```python
import bár  # PLC2403

ápple_count = 5  # PLC2401
bár.process(ápple_count)
```

### Good

```python
import bar

apple_count = 5
bar.process(apple_count)
```

### Violations

1. **PLC2401** — `ápple_count`; variable name contains a non-ASCII character.
2. **PLC2403** — `bár`; imported module name contains a non-ASCII character.
