---
source_hash: 2b142430525f19f7
source_path: lib/pure/concurrency/threadpool.nim
---

# threadpool

[ref: #module-threadpool]

Implements Nim's [parallel & spawn statements](manual_experimental.html#parallel-amp-spawn).

Unstable API.

# [See also](#see-also)

* [threads module](typedthreads.html) for basic thread support
* [locks module](locks.html) for locks and condition variables
* [asyncdispatch module](asyncdispatch.html) for asynchronous IO

## Const

### MaxDistinguishedThread

[ref: #symbol-maxdistinguishedthread]

```nim
MaxDistinguishedThread {.intdefine.} = 32
```

Maximum number of "distinguished" threads.

### MaxThreadPoolSize

[ref: #symbol-maxthreadpoolsize]

```nim
MaxThreadPoolSize {.intdefine.} = 256
```

Maximum size of the thread pool. 256 threads should be good enough for anybody ;-)

## Proc

### `^`

[ref: #symbol-]

**Input:**
- `fv: FlowVar[T]`

**Output:** `T`
**Generic parameters:** `T`

Blocks until the value is available and then returns this value.

### awaitAndThen

[ref: #symbol-awaitandthen]

Blocks until fv is available and then passes its value to action.

**Input:**
- `fv: FlowVar[T]`
- `action: proc (x: T) {.closure.}`

**Output:** *(none)*
**Generic parameters:** `T`

Blocks until fv is available and then passes its value to action.

Note that due to Nim's parameter passing semantics, this means that T doesn't need to be copied, so awaitAndThen can sometimes be more efficient than the [^ proc](#^,FlowVar[T]).

### blockUntil

[ref: #symbol-blockuntil]

Waits until the value for fv arrives.

**Input:**
- `fv: var FlowVarBaseObj`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Waits until the value for fv arrives.

Usually it is not necessary to call this explicitly.

### blockUntilAny

[ref: #symbol-blockuntilany]

Awaits any of the given flowVars. Returns the index of one flowVar for which a value arrived.

**Input:**
- `flowVars: openArray[FlowVarBase]`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Awaits any of the given flowVars. Returns the index of one flowVar for which a value arrived.

A flowVar only supports one call to blockUntilAny at the same time. That means if you blockUntilAny([a,b]) and blockUntilAny([b,c]) the second call will only block until c. If there is no flowVar left to be able to wait on, -1 is returned.

**Note:** This results in non-deterministic behaviour and should be avoided.

### isReady

[ref: #symbol-isready]

Determines whether the specified FlowVarBase's value is available.

**Input:**
- `fv: FlowVarBase`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether the specified FlowVarBase's value is available.

If true, awaiting fv will not block.

### parallel

[ref: #symbol-parallel]

A parallel section can be used to execute a block in parallel.

**Input:**
- `body: untyped`

**Output:** *(none)*
**Pragmas:** `magic: "Parallel"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A parallel section can be used to execute a block in parallel.

body has to be in a DSL that is a particular subset of the language.

Please refer to [the manual](manual_experimental.html#parallel-amp-spawn) for further information.

### pinnedSpawn

[ref: #symbol-pinnedspawn]

Always spawns a new task on the worker thread with id, so that the call is **always** executed on the thread.

**Input:**
- `id: ThreadId`
- `call: sink typed`

**Output:** *(none)*
**Pragmas:** `magic: "Spawn"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Always spawns a new task on the worker thread with id, so that the call is **always** executed on the thread.

call has to be a proc call p(...) where p is gcsafe and has a return type that is either void or compatible with FlowVar[T].

### preferSpawn

[ref: #symbol-preferspawn]

Use this proc to determine quickly if a spawn or a direct call is preferable.

**Input:**
- *(none)*

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Use this proc to determine quickly if a spawn or a direct call is preferable.

If it returns true, a spawn may make sense. In general it is not necessary to call this directly; use the [spawnX template](#spawnX.t) instead.

### setMaxPoolSize

[ref: #symbol-setmaxpoolsize]

**Input:**
- `size: range[1 .. MaxThreadPoolSize]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the maximum thread pool size. The default value of this is [MaxThreadPoolSize](#MaxThreadPoolSize).

### setMinPoolSize

[ref: #symbol-setminpoolsize]

**Input:**
- `size: range[1 .. MaxThreadPoolSize]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the minimum thread pool size. The default value of this is 4.

### spawn

[ref: #symbol-spawn]

Always spawns a new task, so that the call is never executed on the calling thread.

**Input:**
- `call: sink typed`

**Output:** *(none)*
**Pragmas:** `magic: "Spawn"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Always spawns a new task, so that the call is never executed on the calling thread.

call has to be a proc call p(...) where p is gcsafe and has a return type that is either void or compatible with FlowVar[T].

### sync

[ref: #symbol-sync]

A simple barrier to wait for all spawned tasks.

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: [TimeEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: TimeEffect`, `forbids: `

A simple barrier to wait for all spawned tasks.

If you need more elaborate waiting, you have to use an explicit barrier.

### unsafeRead

[ref: #symbol-unsaferead]

**Input:**
- `fv: FlowVar[ref T]`

**Output:** `ptr T`
**Generic parameters:** `T`

Blocks until the value is available and then returns this value.

## Template

### spawnX

[ref: #symbol-spawnx]

Spawns a new task if a CPU core is ready, otherwise executes the call in the calling thread.

**Input:**
- `call: `

**Output:** *(none)*
Spawns a new task if a CPU core is ready, otherwise executes the call in the calling thread.

Usually, it is advised to use the [spawn proc](#spawn,sinktyped) in order to not block the producer for an unknown amount of time.

call has to be a proc call p(...) where p is gcsafe and has a return type that is either 'void' or compatible with FlowVar[T].

## Type

### FlowVar

[ref: #symbol-flowvar]

```nim
FlowVar[T] {.compilerproc.} = ref FlowVarObj[T]
```

A data flow variable.

### FlowVarBase

[ref: #symbol-flowvarbase]

```nim
FlowVarBase = ref FlowVarBaseObj
```

Untyped base class for [FlowVar[T]](#FlowVar).

### ThreadId

[ref: #symbol-threadid]

```nim
ThreadId = range[0 .. MaxDistinguishedThread - 1]
```

A thread identifier.
