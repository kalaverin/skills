---
---

# Lint suppression

Keep `noqa` and ruff config selectors precise, current, and matched to the rules they disable.

## Rule of thumb

1. Name the exact code or rule in every suppression comment; never use bare `noqa` or `type: ignore`.
2. Use canonical, current rule names and codes; remove redirected, stale, or invented suppressions.
3. Prefer `ruff: ignore[rule-name]` over legacy `noqa` comments, and use rule names inside Ruff-native suppression comments.
4. Place formatter suppression comments in valid positions and avoid non-Ruff formatter directives.
5. Pair every `# ruff: disable[...]` with a matching `# ruff: enable[...]`.
6. Write `pyproject.toml` project metadata and ruff selectors with valid schema and readable rule names.

## Example: Inline suppression comments

A legacy CLI module littered with blanket, stale, and invented suppression comments.

### Bad

```python
# File: legacy/cli.py
from __future__ import annotations

from typing import Any  # type: ignore  # PGH003
from .base import *  # noqa  # PGH004,RUF100
import json  # noqa: F401  # RUF100
import getopt  # ruff: ignore[XYZ999]  # RUF102


def main(argv: Any) -> Any:
    user_command = " ".join(argv[1:])
    options, _ = getopt.getopt(argv[1:], "h")
    result = eval(user_command)  # noqa: PGH001  # RUF100,RUF101
    size = len(user_command)  # type: ignore  # noqa: PGH003  # RUF105
    second = eval(user_command)  # ruff: ignore[S307]  # RUF100,RUF106
    config = load_config()
    return result, size, second, config, options


def load_config():
    if os.path.exists("config.json"):
        with open("config.json") as fh:
            return json.load(fh)
    return {}
```

### Good

```python
# File: legacy/cli.py
from __future__ import annotations

import ast
import getopt
import json
import os

from legacy.base import public_api


def main(argv: list[str]):
    user_command = " ".join(argv[1:])
    options, _ = getopt.getopt(argv[1:], "h")
    result = ast.literal_eval(user_command)
    size = len(user_command)
    second = ast.literal_eval(user_command)
    config = load_config()
    return result, size, second, config, options


def load_config() -> dict:
    path = "config.json"
    if os.path.exists(path):
        return json.loads(public_api.read(path))
    return {}
```

### Violations

1. **PGH003** — `from typing import Any  # type: ignore`; blanket `type: ignore` hides every type-checker warning on the line.
2. **PGH004** — `from .base import *  # noqa`; blanket `noqa` suppresses every diagnostic on the line.
3. **RUF100** — `import json  # noqa: F401`; the import is used, so the suppression no longer matches any violation.
4. **RUF101** — `result = eval(user_command)  # noqa: PGH001`; `PGH001` is a redirected code, use the canonical `S307`.
5. **RUF102** — `import getopt  # ruff: ignore[XYZ999]`; `XYZ999` is not a known rule code.
6. **RUF105** — `size = len(user_command)  # noqa: PGH003`; an active `noqa` suppressing a real diagnostic belongs in a `ruff: ignore` comment.
7. **RUF106** — `eval(user_command)  # ruff: ignore[S307]`; use rule names instead of codes in ruff-native suppression comments.

## Example: Formatter and range suppression comments

**Config:** pair2

A report formatter that misplaces formatter suppression comments and leaves a range suppression open.

### Bad

```python
# File: reports/table.py
from __future__ import annotations


def decorator(func):
    return func


def make_table():
    @decorator
    # fmt: off  # RUF028
    def header():
        # ruff: disable  # RUF103
        row = {"name": "Alice", "value": 42}
        # ruff: disable[E501]  # RUF104,RUF106
        title = "This is a really long table header that exceeds the configured line length limit"
        # fmt: skip  # RUF028
        print(row, title)
```

### Good

```python
# File: reports/table.py
from __future__ import annotations


def decorator(func):
    return func


def make_table():
    @decorator
    def header():
        # ruff: disable[line-too-long]
        title = "This is a really long table header that exceeds the configured line length limit"
        # ruff: enable[line-too-long]
        row = {"name": "Alice", "value": 42}
        print(row, title)
```

### Violations

1. **RUF028** — `# fmt: off` before a decorator and `# fmt: skip` on its own line; these formatter suppression comments are invalid or ignored by Ruff.
2. **RUF103** — `# ruff: disable`; a range suppression comment is missing its selector.
3. **RUF104** — `# ruff: disable[E501]` with no matching `# ruff: enable[E501]`; an unclosed range suppression can silence violations across the rest of the scope.

## Example: Project configuration

A pyproject.toml that mixes invalid project metadata with opaque rule codes in ruff selectors.

### Bad

```toml
# File: pyproject.toml
[build-system]
requires = ["setuptools>=75.0"]

[project]
name = "demo"
version = "0.1.0"
description = "Demo project"
authors = ["Acme Corp <dev@example.org>"]  # RUF200
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = ["F401", "E501"]  # RUF201
ignore = ["module-import-not-at-top-of-file"]
```

### Good

```toml
# File: pyproject.toml
[build-system]
requires = ["setuptools>=75.0"]

[project]
name = "demo"
version = "0.1.0"
description = "Demo project"
authors = [
  { name = "Acme Corp", email = "dev@example.org" }
]
readme = "README.md"
requires-python = ">=3.12"
license = { text = "MIT" }

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = ["unused-import", "line-too-long"]
ignore = ["module-import-not-at-top-of-file"]
```

### Violations

1. **RUF200** — `authors = ["Acme Corp <dev@example.org>"]"; project metadata does not conform to the pyproject.toml schema.
2. **RUF201** — `select = ["F401", "E501"]"; use readable rule names instead of codes in ruff selectors.
