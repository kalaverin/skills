---
source_hash: df3dd18dd7183b0a
source_path: lib/pure/coro.nim
---

# coro

[ref: #module-coro]

Nim coroutines implementation, supports several context switching methods:

|  |  |
| --- | --- |
| ucontext | available on unix and alike (default) |
| setjmp | available on unix and alike (x86/64 only) |
| fibers | available and required on windows. |

-d:nimCoroutines

Required to build this module.

-d:nimCoroutinesUcontext

Use ucontext backend.

-d:nimCoroutinesSetjmp

Use setjmp backend.

-d:nimCoroutinesSetjmpBundled

Use bundled setjmp implementation.

Unstable API.

Timer support for the realtime GC. Based on <https://github.com/jckarter/clay/blob/master/compiler/hirestimer.cpp>

## Proc

### alive

[ref: #symbol-alive]

**Input:**
- `c: CoroutineRef`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if coroutine has not returned, false otherwise.

### nimGC_setStackBottom

[ref: #symbol-nimgc-setstackbottom]

**Input:**
- `theStackBottom: pointer`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### run

[ref: #symbol-run]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: [TimeEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: TimeEffect`, `forbids: `

Starts main coroutine scheduler loop which exits when all coroutines exit. Calling this proc starts execution of first coroutine.

### start

[ref: #symbol-start]

**Input:**
- `c: proc ()`
- `stacksize: int = defaultStackSize`

**Output:** `CoroutineRef`
**Pragmas:** `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Schedule coroutine for execution. It does not run immediately.

### suspend

[ref: #symbol-suspend]

**Input:**
- `sleepTime: float = 0.0`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Stops coroutine execution and resumes no sooner than after sleeptime seconds. Until then other coroutines are executed.

### wait

[ref: #symbol-wait]

**Input:**
- `c: CoroutineRef`
- `interval:  = 0.01`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns only after coroutine c has returned. interval is time in seconds how often.

## Type

### CoroutineRef

[ref: #symbol-coroutineref]

```nim
CoroutineRef = ref object
```

CoroutineRef holds a pointer to actual coroutine object. Public API always returns CoroutineRef instead of CoroutinePtr in order to allow holding a reference to coroutine object while it can be safely deallocated by coroutine scheduler loop. In this case Coroutine.reference.coro is set to nil. Public API checks for it being nil and gracefully fails if it is nil.
