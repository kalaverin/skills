---
---

# Resources and environment

Manage files, subprocesses, env vars, and locks safely: context managers, explicit encodings, safe env access.

## Rule of thumb

1. Wrap every file, lock, and resource acquisition in a context manager (`with`) and share the same lock object across threads.
2. Be explicit: pass `encoding="utf-8"`, a valid `open` mode, and `check=True`/`check=False` for subprocesses.
3. Treat environment variables as uppercase strings; pass string defaults to `os.getenv` and copy `os.environ` with its own `.copy()` method.
4. Keep `await` inside `async def` and replace `yield from` in async functions with `async for`.
5. Prefer modern subprocess options like `start_new_session` over `preexec_fn`.

## Example: Deployment script

A small deploy helper that reads config from the environment and disk, then starts a worker.

### Bad

```python
"""Deploy helper."""

import os
import subprocess


def read_manifest(path):
    file = open(path, "rwx")  # PLW1501,PLW1514,SIM115
    data = file.read()
    file.close()
    return data


def worker_port():
    return int(os.getenv("port", 8080))  # PLW1508,SIM112


def worker_token():
    return os.getenv(1)  # PLE1507


def start_worker():
    subprocess.run(["worker", "--daemon"])  # PLW1510
    subprocess.Popen(["worker"], preexec_fn=os.setsid)  # PLW1509


def merge_configs(a, b):
    with open(a) as fa:  # PLW1514,SIM117
        with open(b) as fb:  # PLW1514
            return fa.read() + fb.read()
```

### Good

```python
"""Deploy helper."""

import os
import subprocess


def read_manifest(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def worker_port():
    return int(os.getenv("PORT", "8080"))


def worker_token():
    return os.getenv("TOKEN")


def start_worker():
    subprocess.run(["worker", "--daemon"], check=True)
    subprocess.Popen(["worker"], start_new_session=True)


def merge_configs(a, b):
    with (
        open(a, encoding="utf-8") as fa,
        open(b, encoding="utf-8") as fb,
    ):
        return fa.read() + fb.read()
```

### Violations

1. **PLE1507** — `os.getenv(1)`; the key argument must be a string.
2. **PLW1501** — `open(path, "rwx")`; `"rwx"` is not a valid open mode.
3. **PLW1508** — `os.getenv("port", 8080)`; the default must be a string or `None`.
4. **PLW1509** — `subprocess.Popen(..., preexec_fn=os.setsid)`; `preexec_fn` is unsafe with threads.
5. **PLW1510** — `subprocess.run(["worker", "--daemon"])`; `check` is not explicit.
6. **PLW1514** — `open(...)` calls; text-mode open needs an explicit `encoding`.
7. **SIM112** — `os.getenv("port", ...)`; environment variable names should be uppercase.
8. **SIM115** — `file = open(...)`; use a context manager so the file always closes.
9. **SIM117** — nested `with` statements; combine them into a single `with` line.

## Example: Async job runner

An async job runner that mixes sync/async control flow and protects shared state with a fresh lock each call.

### Bad

```python
"""Async job runner with shared state."""

import asyncio
import copy
import os
import threading


counter = 0


def launch():
    await asyncio.sleep(1)  # PLE1142


async def numbers():
    yield from [1, 2, 3, 4, 5]  # PLE1700


def increment():
    global counter
    with threading.Lock():  # PLW2101
        counter += 1


def snapshot_env():
    return copy.copy(os.environ)  # PLW1507
```

### Good

```python
"""Async job runner with shared state."""

import asyncio
import os
import threading


counter = 0
lock = threading.Lock()


async def launch():
    await asyncio.sleep(1)


async def numbers(source):
    async for number in source:
        yield number


def increment():
    global counter
    with lock:
        counter += 1


def snapshot_env():
    return os.environ.copy()
```

### Violations

1. **PLE1142** — `await asyncio.sleep(1)` inside `def launch()`; `await` is only valid in `async def`.
2. **PLE1700** — `yield from [1, 2, 3, 4, 5]` inside `async def numbers()`; use `async for` instead.
3. **PLW1507** — `copy.copy(os.environ)`; shallow copies of `os.environ` alias the underlying proxy.
4. **PLW2101** — `with threading.Lock():`; a new lock per call provides no mutual exclusion.
