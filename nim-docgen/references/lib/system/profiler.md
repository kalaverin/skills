---
source_hash: 66fdd1faea6740f4
source_path: lib/system/profiler.nim
---

# profiler

[ref: #module-profiler]

## Proc

### `[]`

[ref: #symbol-]

**Input:**
- `st: StackTrace`
- `i: int`

**Output:** `cstring`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### ProfilerHook

[ref: #symbol-profilerhook]

```nim
ProfilerHook = proc (st: StackTrace) {.nimcall.}
```

### StackTrace

[ref: #symbol-stacktrace]

```nim
StackTrace = object
  lines*: array[0 .. 20 - 1, cstring]
  files*: array[0 .. 20 - 1, cstring]
```

## Var

### profilerHook

[ref: #symbol-profilerhook]

```nim
profilerHook: ProfilerHook
```

set this variable to provide a procedure that implements a profiler in user space. See the nimprof module for a reference implementation.

### profilingRequestedHook

[ref: #symbol-profilingrequestedhook]

```nim
profilingRequestedHook: proc (): bool {.nimcall, gcsafe.}
```

set this variable to provide a procedure that implements a profiler in user space. See the nimprof module for a reference implementation.
