---
source_hash: d8a428a87fe13f87
source_path: lib/std/typedthreads.nim
---

# typedthreads

[ref: #module-typedthreads]

Thread support for Nim. Threads allow multiple functions to execute concurrently.

In Nim, threads are a low-level construct and using a library like malebolgia, taskpools or weave is recommended.

When creating a thread, you can pass arguments to it. As Nim's garbage collector does not use atomic references, sharing ref and other variables managed by the garbage collector between threads is not supported. Use global variables to do so, or pointers.

Memory allocated using [`sharedAlloc`](./system.html#allocShared.t%2CNatural) can be used and shared between threads.

To communicate between threads, consider using [channels](./system.html#Channel)

# [Examples](#examples)

```
import std/locks

var
  thr: array[0..4, Thread[tuple[a,b: int]]]
  L: Lock

proc threadFunc(interval: tuple[a,b: int]) {.thread.} =
  for i in interval.a..interval.b:
    acquire(L) # lock stdout
    echo i
    release(L)

initLock(L)

for i in 0..high(thr):
  createThread(thr[i], threadFunc, (i*10, i*10+5))
joinThreads(thr)

deinitLock(L)
```

When using a memory management strategy that supports shared heaps like arc or boehm, you can pass pointer to threads and share memory between them, but the memory must outlive the thread. The default memory management strategy, orc, supports this. The example below is **not valid** for memory management strategies that use local heaps like refc!

```
import locks

var l: Lock

proc threadFunc(obj: ptr seq[int]) {.thread.} =
  withLock l:
    for i in 0..<100:
      obj[].add(obj[].len * obj[].len)

proc threadHandler() =
  var thr: array[0..4, Thread[ptr seq[int]]]
  var s = newSeq[int]()
  
  for i in 0..high(thr):
    createThread(thr[i], threadFunc, s.addr)
  joinThreads(thr)
  echo s

initLock(l)
threadHandler()
deinitLock(l)
```

## Examples

```nim
import std/locks

var
  thr: array[0..4, Thread[tuple[a,b: int]]]
  L: Lock

proc threadFunc(interval: tuple[a,b: int]) {.thread.} =
  for i in interval.a..interval.b:
    acquire(L) # lock stdout
    echo i
    release(L)

initLock(L)

for i in 0..high(thr):
  createThread(thr[i], threadFunc, (i*10, i*10+5))
joinThreads(thr)

deinitLock(L)
```

```nim
import locks

var l: Lock

proc threadFunc(obj: ptr seq[int]) {.thread.} =
  withLock l:
    for i in 0..<100:
      obj[].add(obj[].len * obj[].len)

proc threadHandler() =
  var thr: array[0..4, Thread[ptr seq[int]]]
  var s = newSeq[int]()
  
  for i in 0..high(thr):
    createThread(thr[i], threadFunc, s.addr)
  joinThreads(thr)
  echo s

initLock(l)
threadHandler()
deinitLock(l)
```

## Proc

### createThread

[ref: #symbol-createthread]

Creates a new thread t and starts its execution.

**Input:**
- `t: var Thread[TArg]`
- `tp: proc (arg: TArg) {.thread, nimcall.}`
- `param: TArg`

**Output:** *(none)*
**Generic parameters:** `TArg`

Creates a new thread t and starts its execution.

Entry point is the proc tp. param is passed to tp. TArg can be void if you don't need to pass any data to the thread.

### createThread

[ref: #symbol-createthread]

**Input:**
- `t: var Thread[void]`
- `tp: proc () {.thread, nimcall.}`

**Output:** *(none)*
**Pragmas:** `raises: [ResourceExhaustedError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ResourceExhaustedError`, `tags: `, `forbids: `

### handle

[ref: #symbol-handle]

**Input:**
- `t: Thread[TArg]`

**Output:** `SysThread`
**Generic parameters:** `TArg`

**Pragmas:** `inline`

Returns the thread handle of t.

### joinThread

[ref: #symbol-jointhread]

**Input:**
- `t: Thread[TArg]`

**Output:** *(none)*
**Generic parameters:** `TArg`

**Pragmas:** `inline`

Waits for the thread t to finish.

### joinThreads

[ref: #symbol-jointhreads]

**Input:**
- `t: varargs[Thread[TArg]]`

**Output:** *(none)*
**Generic parameters:** `TArg`

Waits for every thread in t to finish.

### pinToCpu

[ref: #symbol-pintocpu]

Pins a thread to a CPU.

**Input:**
- `t: var Thread[Arg]`
- `cpu: Natural`

**Output:** *(none)*
**Generic parameters:** `Arg`

Pins a thread to a CPU.

In other words sets a thread's affinity. If you don't know what this means, you shouldn't use this proc.

### running

[ref: #symbol-running]

**Input:**
- `t: Thread[TArg]`

**Output:** `bool`
**Generic parameters:** `TArg`

**Pragmas:** `inline`

Returns true if t is running.
