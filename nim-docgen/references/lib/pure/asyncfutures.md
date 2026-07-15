---
source_hash: 5fd86164ef54875b
source_path: lib/pure/asyncfutures.nim
---

# asyncfutures

[ref: #module-asyncfutures]

## Const

### isFutureLoggingEnabled

[ref: #symbol-isfutureloggingenabled]

```nim
isFutureLoggingEnabled = false
```

### NimAsyncContinueSuffix

[ref: #symbol-nimasynccontinuesuffix]

```nim
NimAsyncContinueSuffix = "NimAsyncContinue"
```

For internal usage. Do not use.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `stackTraceEntries: seq[StackTraceEntry]`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `fut1: Future[T]`
- `fut2: Future[Y]`

**Output:** `Future[void]`
**Generic parameters:** `T`, `Y`

Returns a future which will complete once both fut1 and fut2 complete.

### `or`

[ref: #symbol-or]

**Input:**
- `fut1: Future[T]`
- `fut2: Future[Y]`

**Output:** `Future[void]`
**Generic parameters:** `T`, `Y`

Returns a future which will complete once either fut1 or fut2 complete.

### addCallback

[ref: #symbol-addcallback]

Adds the callbacks proc to be called when the future completes.

**Input:**
- `future: FutureBase`
- `cb: proc () {.closure, gcsafe.}`

**Output:** *(none)*
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Adds the callbacks proc to be called when the future completes.

If future has already completed then cb will be called immediately.

### addCallback

[ref: #symbol-addcallback]

Adds the callbacks proc to be called when the future completes.

**Input:**
- `future: Future[T]`
- `cb: proc (future: Future[T]) {.closure, gcsafe.}`

**Output:** *(none)*
**Generic parameters:** `T`

Adds the callbacks proc to be called when the future completes.

If future has already completed then cb will be called immediately.

### all

[ref: #symbol-all]

Returns a future which will complete once all futures in futs complete. If the argument is empty, the returned future completes immediately.

**Input:**
- `futs: varargs[Future[T]]`

**Output:** `auto`
**Generic parameters:** `T`

Returns a future which will complete once all futures in futs complete. If the argument is empty, the returned future completes immediately.

If the awaited futures are not Future[void], the returned future will hold the values of all awaited futures in a sequence.

If the awaited futures *are* Future[void], this proc returns Future[void].

### asyncCheck

[ref: #symbol-asynccheck]

Sets a callback on future which raises an exception if the future finished with an error.

**Input:**
- `future: Future[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Sets a callback on future which raises an exception if the future finished with an error.

This should be used instead of discard to discard void futures, or use waitFor if you need to wait for the future's completion.

### callback=

[ref: #symbol-callback]

Clears the list of callbacks and sets the callback proc to be called when the future completes.

**Input:**
- `future: FutureBase`
- `cb: proc () {.closure, gcsafe.}`

**Output:** *(none)*
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Clears the list of callbacks and sets the callback proc to be called when the future completes.

If future has already completed then cb will be called immediately.

It's recommended to use addCallback or then instead.

### callback=

[ref: #symbol-callback]

Sets the callback proc to be called when the future completes.

**Input:**
- `future: Future[T]`
- `cb: proc (future: Future[T]) {.closure, gcsafe.}`

**Output:** *(none)*
**Generic parameters:** `T`

Sets the callback proc to be called when the future completes.

If future has already completed then cb will be called immediately.

### callSoon

[ref: #symbol-callsoon]

Call cbproc "soon".

**Input:**
- `cbproc: proc () {.gcsafe.}`

**Output:** *(none)*
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Call cbproc "soon".

If async dispatcher is running, cbproc will be executed during next dispatcher tick.

If async dispatcher is not running, cbproc will be executed immediately.

### clean

[ref: #symbol-clean]

**Input:**
- `future: FutureVar[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Resets the finished status of future.

### clearCallbacks

[ref: #symbol-clearcallbacks]

**Input:**
- `future: FutureBase`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### complete

[ref: #symbol-complete]

**Input:**
- `future: Future[T]`
- `val: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

Completes future with value val.

### complete

[ref: #symbol-complete]

**Input:**
- `future: Future[void]`
- `val:  = Future[void].default`

**Output:** *(none)*
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

### complete

[ref: #symbol-complete]

**Input:**
- `future: FutureVar[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Completes a FutureVar.

### complete

[ref: #symbol-complete]

Completes a FutureVar with value val.

**Input:**
- `future: FutureVar[T]`
- `val: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

Completes a FutureVar with value val.

Any previously stored value will be overwritten.

### fail

[ref: #symbol-fail]

**Input:**
- `future: Future[T]`
- `error: ref Exception`

**Output:** *(none)*
**Generic parameters:** `T`

Completes future with error.

### failed

[ref: #symbol-failed]

**Input:**
- `future: FutureBase`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether future completed with an error.

### finished

[ref: #symbol-finished]

Determines whether future has completed.

**Input:**
- `future: FutureBase | FutureVar`

**Output:** `bool`
**Generic parameters:** `future:type`

Determines whether future has completed.

True may indicate an error or a value. Use failed to distinguish.

### getCallSoonProc

[ref: #symbol-getcallsoonproc]

**Input:**
- *(none)*

**Output:** `(proc (cbproc: proc ()) {.gcsafe.})`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get current implementation of callSoon.

### mget

[ref: #symbol-mget]

Returns a mutable value stored in future.

**Input:**
- `future: FutureVar[T]`

**Output:** `var T`
**Generic parameters:** `T`

Returns a mutable value stored in future.

Unlike read, this function will not raise an exception if the Future has not been finished.

### newFuture

[ref: #symbol-newfuture]

Creates a new future.

**Input:**
- `fromProc: string = "unspecified"`

**Output:** `owned(Future[T])`
**Generic parameters:** `T`

Creates a new future.

Specifying fromProc, which is a string specifying the name of the proc that this future belongs to, is a good habit as it helps with debugging.

### newFutureVar

[ref: #symbol-newfuturevar]

Create a new FutureVar. This Future type is ideally suited for situations where you want to avoid unnecessary allocations of Futures.

**Input:**
- `fromProc:  = "unspecified"`

**Output:** `owned(FutureVar[T])`
**Generic parameters:** `T`

Create a new FutureVar. This Future type is ideally suited for situations where you want to avoid unnecessary allocations of Futures.

Specifying fromProc, which is a string specifying the name of the proc that this future belongs to, is a good habit as it helps with debugging.

### read

[ref: #symbol-read]

Retrieves the value of future. Future must be finished otherwise this function will fail with a ValueError exception.

**Input:**
- `future: Future[T] | FutureVar[T]`

**Output:** `lent T`
**Generic parameters:** `T`, `future:type`

Retrieves the value of future. Future must be finished otherwise this function will fail with a ValueError exception.

If the result of the future is an error then that error will be raised.

### read

[ref: #symbol-read]

**Input:**
- `future: Future[void] | FutureVar[void]`

**Output:** *(none)*
**Generic parameters:** `future:type`

### readError

[ref: #symbol-readerror]

Retrieves the exception stored in future.

**Input:**
- `future: Future[T]`

**Output:** `ref Exception`
**Generic parameters:** `T`

Retrieves the exception stored in future.

An ValueError exception will be thrown if no exception exists in the specified Future.

### setCallSoonProc

[ref: #symbol-setcallsoonproc]

**Input:**
- `p: (proc (cbproc: proc ()) {.gcsafe.})`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Change current implementation of callSoon. This is normally called when dispatcher from asyncdispatcher is initialized.

## Type

### Future

[ref: #symbol-future]

```nim
Future[T] = ref object of FutureBase
```

Typed future.

### FutureBase

[ref: #symbol-futurebase]

```nim
FutureBase = ref object of RootObj
  error*: ref Exception      ## Stored exception
  errorStackTrace*: string
  when not defined(release) or defined(futureLogging):
```

Untyped future.

### FutureError

[ref: #symbol-futureerror]

```nim
FutureError = object of Defect
  cause*: FutureBase
```

### FutureVar

[ref: #symbol-futurevar]

```nim
FutureVar[T] = distinct Future[T]
```
