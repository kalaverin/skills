---
---

# Security: Injection

Keep user input out of shells and SQL: use argument lists, parameterized queries, and absolute executable paths.

## Rule of thumb

1. Treat every shell, subprocess, and SQL call as a trust boundary: never let user data become syntax.
2. Build subprocess calls as argument lists and avoid `shell=True`.
3. Validate every executable and argument against an allow-list before it reaches an external program.
4. Invoke programs by absolute path or resolve them with `shutil.which`; do not rely on `PATH` resolution.
5. Replace shell wildcards with Python enumeration; pass matching files as separate arguments.
6. Parameterize SQL queries; keep the statement template and user values in separate arguments.

## Example: Log rotation via shell

A junior rotates logs by shelling out, mixing a partial executable name with shell wildcards.

### Bad

```python
"""Rotate logs by shelling out."""

import subprocess  # S404


def rotate_logs(directory: str) -> None:
    subprocess.run("rm -rf /var/log/app/*.log", shell=True)  # S602,S607
    subprocess.Popen(["/bin/chmod", "777", "*.log"], shell=True)  # S602,S609
```

### Good

```python
"""Rotate logs without subprocess."""

from pathlib import Path


def rotate_logs(directory: Path) -> None:
    for path in Path(directory).glob("*.log"):
        path.unlink()
```

### Violations

1. **S404** — `import subprocess`; importing the subprocess module flags the file as a command-execution sink.
2. **S602** — `subprocess.run(..., shell=True)` and `subprocess.Popen(..., shell=True)`; parsing commands through a shell lets metacharacters run arbitrary commands.
3. **S607** — `rm` in the shell string; partial executable path resolves through an attacker-controllable `PATH`.
4. **S609** — `*.log` in the Popen call; shell wildcard can match unintended or attacker-created files.

## Example: Admin command runner

An admin tool trusts a raw command string and runs it as an argument list without validation.

### Bad

```python
"""Run an operator-supplied command."""

import subprocess  # S404


def run_command(raw: str) -> None:
    parts = raw.split()
    subprocess.run(parts)  # S603
```

### Good

```python
"""Run an operator-supplied command."""

import subprocess  # noqa: S404  # subprocess is the vetted-binary runner here


ALLOWED = {"/usr/bin/git", "/usr/bin/ls"}


def run_command(raw: str) -> None:
    parts = raw.split()
    if not parts:
        raise ValueError("empty command")
    executable = parts[0]
    if executable not in ALLOWED:
        raise ValueError("command not allowed")
    subprocess.run([executable, *parts[1:]], check=True)  # noqa: S603  # executable allow-listed above
```

### Violations

1. **S603** — `subprocess.run(parts)`; untrusted tokens reach a subprocess without validation.

## Example: Legacy OS launchers

A cleanup script shells out through legacy `os` functions instead of using Python APIs.

### Bad

```python
"""Legacy log archiving."""

import os


def archive(src: str, dst: str) -> None:
    os.system(f"cp {src} {dst}")  # S605
    os.spawnlp(os.P_NOWAIT, "gzip", "gzip", src)  # S606
```

### Good

```python
"""Legacy log archiving replaced by Python APIs."""

import gzip
import shutil
from pathlib import Path


def archive(src: str, dst: str) -> None:
    shutil.copy(src, dst)
    path = Path(src)
    with gzip.open(path.with_suffix(".gz"), "wb") as out:
        out.write(path.read_bytes())
```

### Violations

1. **S605** — `os.system(f"cp {src} {dst}")`; shelling out to a formatted string lets user input become shell syntax.
2. **S606** — `os.spawnlp(..., "gzip", "gzip", src)`; arbitrary input reaches an external executable even without a shell.

## Example: Custom runner wrapper

An internal helper wraps `subprocess.run` but callers still pass `shell=True` and a raw string.

### Bad

```python
"""Run commands through an internal wrapper."""

import my_runner


def dispatch(raw: str) -> None:
    my_runner.run(raw, shell=True)  # S604
```

### Good

```python
"""Run commands through an internal wrapper."""

import shutil

import my_runner


ALLOWED = {"/usr/bin/git"}


def dispatch(raw: str) -> None:
    parts = raw.split()
    if not parts:
        raise ValueError("empty command")
    executable = shutil.which(parts[0]) or parts[0]
    if executable not in ALLOWED:
        raise ValueError("command not allowed")
    my_runner.run([executable, *parts[1:]], shell=False)
```

### Violations

1. **S604** — `my_runner.run(raw, shell=True)`; any wrapper forwarding `shell=True` sends user input to a shell.

## Example: User lookup query

A repository function builds a SQL statement with an f-string.

### Bad

```python
"""Fetch a user record by ID."""


def get_user(cursor, user_id: str) -> None:
    query = f"SELECT * FROM users WHERE id = {user_id}"  # S608
    cursor.execute(query)
```

### Good

```python
"""Fetch a user record by ID."""


def get_user(cursor, user_id: str) -> None:
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```

### Violations

1. **S608** — `f"SELECT * FROM users WHERE id = {user_id}"`; interpolated user values become SQL syntax.
