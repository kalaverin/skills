---
---

# Security: Runtime

Keep untrusted data away from `eval`/`exec`, `assert`, unsafe deserializers, predictable temp paths, loose permissions, and hardcoded secrets.

## Rule of thumb

1. Replace `eval` with `ast.literal_eval` and `exec` with data-driven dispatch; never execute strings that came from outside the process.
2. Enforce runtime contracts with `raise`, never with `assert` — assertions vanish under `python -O`.
3. Deserialize untrusted data only through safe parsers: `json`, `yaml.safe_load`, `tarfile.extractall(filter="data")`; treat `pickle`/`marshal` as audit sinks that demand a written justification.
4. Create scratch files through `tempfile` helpers; never hard-code `/tmp` paths and never call `tempfile.mktemp`.
5. Default file permissions to the narrowest mask that works; widen only deliberately.
6. Pull secrets from the environment or a vault, never from literals in source — not in assignments, call arguments, or parameter defaults.

## Example: Plugin loader

A plugin host evaluates user-supplied settings, validates them with `assert`, starts a remote logging listener, and executes plugin code.

### Bad

```python
"""Load and run user-supplied plugin snippets."""

import logging.config


def load_settings(raw: str) -> dict:
    config = eval(raw)  # S307
    assert isinstance(config, dict), "settings must be a dict"  # S101
    return config


def run_plugin(code: str) -> None:
    logging.config.listen(9999)  # S612
    exec(code)  # S102
```

### Good

```python
"""Load and run user-supplied plugin snippets."""

import logging
from ast import literal_eval


def load_settings(raw: str) -> dict:
    config = literal_eval(raw)
    if not isinstance(config, dict):
        raise ValueError("settings must be a dict")
    return config


def run_plugin(name: str) -> None:
    logging.basicConfig(level=logging.INFO)
    commands = {
        "hello": lambda: print("Hello, World!"),
    }
    commands.get(name, lambda: print("Unknown command"))()
```

### Violations

1. **S101** — `assert isinstance(config, dict), ...`; the check disappears when Python runs with `-O`.
2. **S102** — `exec(code)`; runs arbitrary Python from an untrusted string.
3. **S307** — `eval(raw)`; evaluates any expression, not just literals.
4. **S612** — `logging.config.listen(9999)`; the config socket server passes incoming payloads through `eval`, enabling remote code execution.

## Example: Cache and bundle loader

A service restores cached objects with `pickle`/`marshal`, parses YAML with the full loader, and unpacks a tarball without an extraction filter.

### Bad

```python
"""Load cached payloads, state snapshots, and configs."""

import marshal
import pickle  # S403
import tarfile

import yaml


def load_cache(path: str):
    with open(path, "rb") as file:
        return pickle.load(file)  # S301


def load_state(path: str):
    with open(path, "rb") as file:
        return marshal.load(file)  # S302


def load_config(raw: str):
    return yaml.load(raw)  # S506


def unpack_bundle(archive: str, dest: str) -> None:
    with tarfile.open(archive) as tar:
        tar.extractall(path=dest)  # S202
```

### Good

```python
"""Load cached payloads, state snapshots, and configs."""

import json
import tarfile

import yaml


def load_cache(path: str):
    with open(path, "rb") as file:
        return json.load(file)


def load_state(path: str):
    with open(path, "rb") as file:
        return json.load(file)


def load_config(raw: str):
    return yaml.safe_load(raw)


def unpack_bundle(archive: str, dest: str) -> None:
    with tarfile.open(archive) as tar:
        tar.extractall(path=dest, filter="data")  # noqa: S202  # filter="data" blocks unsafe members
```

### Violations

1. **S202** — `tar.extractall(path=dest)`; unfiltered extraction lets absolute or `../` members escape the target directory.
2. **S301** — `pickle.load(file)`; unpickling untrusted bytes can construct arbitrary objects and execute code.
3. **S302** — `marshal.load(file)`; the internal `marshal` format carries the same arbitrary-object risk as `pickle`.
4. **S403** — `import pickle`; importing `pickle`/`cPickle`/`dill`/`shelve` flags a deserialization audit sink.
5. **S506** — `yaml.load(raw)`; the full YAML loader instantiates arbitrary Python objects, use `safe_load`.

## Example: Scratch files for a report

A reporting job writes output to predictable `/tmp` paths, opens them up to every user, and races on `mktemp`.

### Bad

```python
"""Write a report to a scratch file."""

import os
import tempfile


def write_report(payload: str) -> str:
    path = "/tmp/report.txt"  # S108
    with open(path, "w") as file:
        file.write(payload)
    os.chmod(path, 0o666)  # S103
    return path


def stage_upload(payload: str) -> str:
    path = tempfile.mktemp()  # S306
    with open(path, "w") as file:
        file.write(payload)
    return path
```

### Good

```python
"""Write a report to a scratch file."""

import os
import tempfile


def write_report(payload: str) -> str:
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w") as file:
        file.write(payload)
    return path


def stage_upload(payload: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as file:
        file.write(payload)
        return file.name
```

### Violations

1. **S103** — `os.chmod(path, 0o666)`; world-writable permissions let other users read or poison the report.
2. **S108** — `"/tmp/report.txt"`; a predictable temp path can be squatted, symlinked, or overwritten between processes.
3. **S306** — `tempfile.mktemp()`; the path does not exist yet, so another process can claim it first.

## Example: Database connector

A connector ships credentials as a module constant, a call argument, and a parameter default.

### Bad

```python
"""Database connector."""

DB_PASSWORD = "hunter2"  # S105


def connect(host: str, password: str = "admin123"):  # S107
    ...


def main() -> None:
    connect("db.internal", password="hunter2")  # S106
```

### Good

```python
"""Database connector."""

import os

DB_PASSWORD = os.environ["DB_PASSWORD"]


def connect(host: str, password: str | None = None) -> None:
    if password is None:
        password = os.environ["DB_PASSWORD"]
    ...


def main() -> None:
    connect("db.internal", password=os.environ["DB_PASSWORD"])
```

### Violations

1. **S105** — `DB_PASSWORD = "hunter2"`; a secret in source is visible to anyone with repository access.
2. **S106** — `password="hunter2"` in the call; hardcoded arguments leak into logs, traces, and history.
3. **S107** — `password: str = "admin123"`; a credential baked into the signature ships with every checkout.
