---
---

# Async

Structured concurrency: cancel scopes and shields, no blocking calls in async code, task-group patterns, correct create_task usage.

## Rule of thumb

1. Apply timeout context managers at the call site and make sure the body contains an `await`, `async with`, or `async for` checkpoint.
2. Never call blocking I/O inside `async def`: use async HTTP/file/path/subprocess libraries, or offload to a thread pool.
3. Await every trio/anyio call; prefer `Event.wait()` over busy-wait loops, `checkpoint()` over `sleep(0)`, and `sleep_forever()` over very long sleeps.
4. Wrap single-yield context helpers with `@asynccontextmanager`; do not yield inside a raw async context manager.
5. Store strong references to tasks from `create_task`/`ensure_future` and discard them in a done callback.
6. Do not declare a function `async` unless it awaits or otherwise needs async features.

## Example: Cancellation scopes and checkpoints

A trio worker that mixes timeout parameters, no-op cancel scopes, and misleading sleep calls.

### Bad

```python
import logging
import trio


logger = logging.getLogger("source")


async def poll_source(timeout: float):  # ASYNC109
    logger.info("start poll")
    try:
        with trio.move_on_after(timeout):  # ASYNC100
            prepare_query()
            conn = open_sync()
            query = build_query(conn)
            validate(query)
    except Exception:
        logger.exception("poll failed")
        raise

    await trio.sleep(0)  # ASYNC115
    await trio.sleep(86401)  # ASYNC116
    return query
```

### Good

```python
import logging
import trio


logger = logging.getLogger("source")


async def poll_source():
    logger.info("start poll")
    try:
        with trio.fail_after(5):
            conn = await open_async()
            query = await build_query(conn)
            await validate(query)
    except Exception:
        logger.exception("poll failed")
        raise

    await trio.lowlevel.checkpoint()
    await trio.sleep_forever()
```

### Violations

1. **ASYNC100** — `with trio.move_on_after(timeout):`; the scope has no checkpoint, so the timeout can never trigger.
2. **ASYNC109** — `async def poll_source(timeout: float):`; async functions should not take `timeout` parameters, use a scope at the call site.
3. **ASYNC115** — `await trio.sleep(0)`; yield control explicitly with `trio.lowlevel.checkpoint()`.
4. **ASYNC116** — `await trio.sleep(86401)`; a sleep longer than 24 hours should use `trio.sleep_forever()`.

## Example: Trio control flow and generators

A trio service that forgets to await a sleep, busy-waits on a flag, and yields inside a raw context manager.

### Bad

```python
import trio


DONE = False


async def double_sleep(x: float) -> None:
    delay = 2 * x
    trio.sleep(delay)  # ASYNC105
    await trio.lowlevel.checkpoint()


async def wait_for_done():
    while not DONE:  # ASYNC110
        await trio.sleep(0.1)


async def open_connection():
    cfg = load_config()
    async with connect(cfg) as conn:
        print("connected")
        yield conn  # ASYNC119
```

### Good

```python
import trio
from contextlib import asynccontextmanager


DONE = trio.Event()


async def double_sleep(x: float) -> None:
    delay = 2 * x
    await trio.sleep(delay)


async def wait_for_done():
    await DONE.wait()


@asynccontextmanager
async def open_connection():
    cfg = load_config()
    async with connect(cfg) as conn:
        print("connected")
        yield conn
```

### Violations

1. **ASYNC105** — `trio.sleep(delay)`; trio async calls must be awaited.
2. **ASYNC110** — `await trio.sleep(0.1)` inside `while not DONE`; busy-waiting wastes CPU, use `trio.Event.wait()`.
3. **ASYNC119** — `yield conn` inside `async with connect(cfg) as conn`; cleanup may run when `await` is illegal, use `@asynccontextmanager`.

## Example: Blocking network and subprocess I/O

An asyncio health-check service that calls blocking HTTP and subprocess APIs.

### Bad

```python
import os
import subprocess
import urllib.request

import httpx


async def fetch_legacy(url: str) -> bytes:
    await log_start(url)
    with urllib.request.urlopen(url) as resp:  # ASYNC210
        return resp.read()


async def fetch_httpx(url: str) -> bytes:
    await log_start(url)
    client = httpx.Client()
    return client.get(url).content  # ASYNC212


async def spawn_worker(cmd: str) -> None:
    await log_start(cmd)
    os.popen(cmd)  # ASYNC220


async def run_audit(cmd: list[str]) -> int:
    await log_start(cmd)
    proc = subprocess.run(cmd)  # ASYNC221
    return proc.returncode


async def reap(pid: int) -> None:
    await log_start(pid)
    os.waitpid(pid, 0)  # ASYNC222
```

### Good

```python
import asyncio
import os
import subprocess

import aiohttp
import httpx


async def fetch_legacy(url: str) -> bytes:
    await log_start(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.read()


async def fetch_httpx(url: str) -> bytes:
    await log_start(url)
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return resp.content


async def spawn_worker(cmd: str) -> asyncio.subprocess.Process:
    await log_start(cmd)
    return await asyncio.create_subprocess_shell(cmd)


async def run_audit(cmd: list[str]) -> int:
    await log_start(cmd)
    proc = await asyncio.create_subprocess_exec(*cmd)
    await proc.wait()
    return proc.returncode


async def reap(pid: int) -> int:
    await log_start(pid)
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, os.waitpid, pid, 0)
```

### Violations

1. **ASYNC210** — `urllib.request.urlopen(url)`; urllib blocks the event loop, use an async HTTP client.
2. **ASYNC212** — `client.get(url).content`; `httpx.Client` methods are blocking, use `httpx.AsyncClient`.
3. **ASYNC220** — `os.popen(cmd)`; blocking subprocess creation, use `asyncio.create_subprocess_*`.
4. **ASYNC221** — `subprocess.run(cmd)`; blocking process execution, use `asyncio.create_subprocess_*`.
5. **ASYNC222** — `os.waitpid(pid, 0)`; blocking process wait, offload to an executor.

## Example: Blocking file, path, input, and sleep

An anyio-based CLI tool that performs blocking filesystem, user-input, and sleep operations.

### Bad

```python
import os
import time


async def read_config(path: str) -> str:
    await show_prompt(path)
    with open(path) as f:  # ASYNC230
        return f.read()


async def check_exists(path: str) -> bool:
    await show_prompt(path)
    return os.path.exists(path)  # ASYNC240


async def ask_user(prompt: str) -> str:
    await show_prompt(prompt)
    return input(prompt)  # ASYNC250


async def pause(seconds: float) -> None:
    await show_prompt(seconds)
    time.sleep(seconds)  # ASYNC251
```

### Good

```python
import anyio


async def read_config(path: str) -> str:
    await show_prompt(path)
    async with await anyio.open_file(path) as f:
        return await f.read()


async def check_exists(path: str) -> bool:
    await show_prompt(path)
    p = anyio.Path(path)
    return await p.exists()


async def ask_user(prompt: str) -> str:
    await show_prompt(prompt)
    return await anyio.to_thread.run_sync(input, prompt)


async def pause(seconds: float) -> None:
    await show_prompt(seconds)
    await anyio.sleep(seconds)
```

### Violations

1. **ASYNC230** — `with open(path) as f`; builtin file I/O blocks the event loop, use `anyio.open_file` or `aiofiles`.
2. **ASYNC240** — `os.path.exists(path)`; path methods hit the disk synchronously, use `anyio.Path`.
3. **ASYNC250** — `input(prompt)`; interactive input blocks the loop, run it in a thread.
4. **ASYNC251** — `time.sleep(seconds)`; synchronous sleep freezes the loop, use an async sleep.

## Example: Task lifecycle and async honesty

An asyncio orchestrator with a dangling task and a function that lies about being async.

### Bad

```python
import asyncio


async def compute(x: int) -> int:  # RUF029
    result = x * 2
    return result


def fire_and_forget() -> None:
    print("launching workers")
    for i in range(10):
        task_input = build_input(i)
        asyncio.create_task(work(task_input))  # RUF006
    print("workers launched")
```

### Good

```python
import asyncio


def compute(x: int) -> int:
    result = x * 2
    return result


def fire_and_forget() -> None:
    print("launching workers")
    background_tasks: set[asyncio.Task] = set()
    for i in range(10):
        task_input = build_input(i)
        task = asyncio.create_task(work(task_input))
        background_tasks.add(task)
        task.add_done_callback(background_tasks.discard)
    print("workers launched")
```

### Violations

1. **RUF006** — `asyncio.create_task(work(task_input))`; the task is not referenced and may be garbage collected before running.
2. **RUF029** — `async def compute(x: int) -> int`; function is async but never awaits or uses async features.
