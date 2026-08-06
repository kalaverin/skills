---
---

# Hygiene

Keep the tree clean: no commented-out code, debug prints, or sloppy TODO/FIXME comments; correct shebangs and executable entry points.

## Rule of thumb

1. Delete commented-out code and debug aids (`breakpoint`, `print`, `pprint`); use logging, tests, and type checkers to observe behavior.
2. Match the executable bit to the shebang: executable scripts need a correct Python shebang at the very top; non-executable modules must not have one.
3. Treat mock assertions as method calls; never read `assert_called` as an attribute.
4. Do not ship `FIXME`, `TODO`, `XXX`, or `HACK` markers; resolve the issue or delete the comment.
5. If a TODO must remain, write it as `TODO(<author>): <description>` with an issue link, a space after the colon, and correct capitalization.

## Example: Debug session leftovers

A junior's executable script that still has the debug session's prints, breakpoint, dead code, and an unchecked mock assertion.

### Bad

```python
# File: scripts/debug_runner.py (executable, no shebang)  # EXE002
"""Debug runner."""

import pprint
from unittest import mock


def run(values: list[int]) -> int:
    """Sum values with debug noise."""
    # result = sum(values)  # ERA001
    breakpoint()  # T100
    print(f"values: {values}")  # T201
    total = sum(values)
    pprint.pprint({"total": total})  # T203
    return total


def check(callee: mock.Mock) -> None:
    """Verify the mock was called."""
    callee.assert_called  # PGH005


def main() -> None:
    run([1, 2, 3])
```

### Good

```python
#!/usr/bin/env python3
"""Debug runner."""

import logging
from unittest import mock

logger = logging.getLogger(__name__)


def run(values: list[int]) -> int:
    """Sum values."""
    total = sum(values)
    logger.debug("total=%d", total)
    return total


def check(callee: mock.Mock) -> None:
    """Verify the mock was called."""
    callee.assert_called()


def main() -> None:
    run([1, 2, 3])
```

### Violations

1. **ERA001** — `# result = sum(values)`; commented-out code is dead code.
2. **EXE002** — `scripts/debug_runner.py`; executable file has no shebang.
3. **PGH005** — `callee.assert_called`; mock assertion must be called as a method.
4. **T100** — `breakpoint()`; debugger call halts production execution.
5. **T201** — `print(f"values: {values}")`; `print` is not a logging mechanism.
6. **T203** — `pprint.pprint({"total": total})`; `pprint` is a debug print.

## Example: Broken shebang

A script that looks executable but is not, with shebangs in the wrong places, using the wrong interpreter, and indented with whitespace.

### Bad

```python
 #!/bin/sh  # EXE001,EXE003,EXE004
"""Entry point."""

#!/usr/bin/env python  # EXE001,EXE005


def main() -> None:
    """Say hello."""
    message = "hello"
    return message.upper()


def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"


def describe() -> str:
    """Return a description."""
    return "misleading script"


if __name__ == "__main__":
    main()
```

### Good

```python
"""Correct entry point."""


def main() -> None:
    """Say hello."""
    message = "hello"
    return message.upper()


def greet(name: str) -> str:
    """Greet someone."""
    return f"Hello, {name}!"


def describe() -> str:
    """Return a description."""
    return "correct script"


if __name__ == "__main__":
    main()
```

### Violations

1. **EXE001** — ` #!/bin/sh` and `#!/usr/bin/env python`; shebang present but the file is not executable.
2. **EXE003** — `#!/bin/sh`; shebang does not contain `python`.
3. **EXE004** — leading whitespace before `#!/bin/sh`; `#!` must be the first two characters.
4. **EXE005** — `#!/usr/bin/env python` after the docstring; the shebang must be on the first line.

## Example: Sloppy task tags

A helper module littered with FIXME/TODO/XXX/HACK markers and malformed TODO comments.

### Bad

```python
"""Task tracker helpers."""


def speed(distance: float, time: float) -> float:
    # FIXME(ruff): division by zero here  # FIX001,TD001,TD003
    return distance / time


def greet(name: str) -> str:
    # TODO: add custom greetings  # FIX002,TD002,TD003
    return f"Hello, {name}!"


def platform_check() -> bool:
    # XXX(ruff): use sys.platform  # FIX003,TD001,TD003
    import os
    return os.name == "nt"  # HACK: fragile  # FIX004


def validate(items: list[int]) -> bool:
    # todo(ruff): validate bounds  # FIX002,TD003,TD006
    # TODO  # FIX002,TD002,TD003,TD004,TD005
    # TODO(ruff) missing colon  # FIX002,TD003,TD004
    # TODO(ruff):no space  # FIX002,TD003,TD007
    # TODO(ruff):  # FIX002,TD003,TD005
    return all(i > 0 for i in items)
```

### Good

```python
"""Task tracker helpers."""


def speed(distance: float, time: float) -> float:
    if time == 0:
        raise ValueError("time must be non-zero")
    return distance / time


def greet(name: str, greeting: str = "Hello") -> str:
    return f"{greeting}, {name}!"


def platform_check() -> bool:
    import sys
    return sys.platform.startswith("win")


def validate(items: list[int]) -> bool:
    return all(i > 0 for i in items)
```

### Violations

1. **FIX001** — `# FIXME(ruff): division by zero here`; FIXME marks a real bug, resolve or delete.
2. **FIX002** — `# TODO: add custom greetings`, `# TODO`, `# TODO(ruff) missing colon`, `# TODO(ruff):no space`, `# TODO(ruff):`; TODO comments should be resolved or deleted.
3. **FIX003** — `# XXX(ruff): use sys.platform`; XXX is ambiguous, resolve or rewrite.
4. **FIX004** — `# HACK: fragile`; HACK documents a workaround that should not survive review.
5. **TD001** — `# FIXME(ruff): division by zero here`, `# XXX(ruff): use sys.platform`; only `TODO` is the canonical tag.
6. **TD002** — `# TODO: add custom greetings`, `# TODO`; TODO needs an author.
7. **TD003** — `# TODO: add custom greetings` and every other TODO above; TODO needs an issue link.
8. **TD004** — `# TODO`, `# TODO(ruff) missing colon`; TODO tag must be followed by a colon.
9. **TD005** — `# TODO`, `# TODO(ruff):`; TODO must include a description.
10. **TD006** — `# todo(ruff): validate bounds`; TODO tag must be uppercase.
11. **TD007** — `# TODO(ruff):no space`; colon must be followed by a space.
