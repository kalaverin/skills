---
source_hash: 0296283b4c2cdfe4
source_path: lib/pure/concurrency/cpuload.nim
---

# cpuload

[ref: #module-cpuload]

This module implements a helper for a thread pool to determine whether creating a thread is a good idea.

Unstable API.

## Proc

### advice

[ref: #symbol-advice]

**Input:**
- `s: var ThreadPoolState`

**Output:** `ThreadPoolAdvice`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### ThreadPoolAdvice

[ref: #symbol-threadpooladvice]

```nim
ThreadPoolAdvice = enum
  doNothing, doCreateThread, doShutdownThread
```

### ThreadPoolState

[ref: #symbol-threadpoolstate]

```nim
ThreadPoolState = object
  when defined(windows):
  calls*: int
```
