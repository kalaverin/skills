---
source_hash: c46878539b1f0061
source_path: lib/pure/asyncstreams.nim
---

# asyncstreams

[ref: #module-asyncstreams]

Unstable API.

## Proc

### callback=

[ref: #symbol-callback]

Sets the callback proc to be called when data was placed inside the future stream.

**Input:**
- `future: FutureStream[T]`
- `cb: proc (future: FutureStream[T]) {.closure, gcsafe.}`

**Output:** *(none)*
**Generic parameters:** `T`

Sets the callback proc to be called when data was placed inside the future stream.

The callback is also called when the future is completed. So you should use finished to check whether data is available.

If the future stream already has data or is finished then cb will be called immediately.

### complete

[ref: #symbol-complete]

**Input:**
- `future: FutureStream[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Completes a FutureStream signalling the end of data.

### fail

[ref: #symbol-fail]

**Input:**
- `future: FutureStream[T]`
- `error: ref Exception`

**Output:** *(none)*
**Generic parameters:** `T`

Completes future with error.

### failed

[ref: #symbol-failed]

**Input:**
- `future: FutureStream[T]`

**Output:** `bool`
**Generic parameters:** `T`

Determines whether future completed with an error.

### finished

[ref: #symbol-finished]

**Input:**
- `future: FutureStream[T]`

**Output:** `bool`
**Generic parameters:** `T`

Check if a FutureStream is finished. true value means that no more data will be placed inside the stream *and* that there is no data waiting to be retrieved.

### len

[ref: #symbol-len]

**Input:**
- `future: FutureStream[T]`

**Output:** `int`
**Generic parameters:** `T`

Returns the amount of data pieces inside the stream.

### newFutureStream

[ref: #symbol-newfuturestream]

Create a new FutureStream. This future's callback is activated when two events occur:

**Input:**
- `fromProc:  = "unspecified"`

**Output:** `FutureStream[T]`
**Generic parameters:** `T`

Create a new FutureStream. This future's callback is activated when two events occur:

* New data is written into the future stream.
* The future stream is completed (this means that no more data will be written).

Specifying fromProc, which is a string specifying the name of the proc that this future belongs to, is a good habit as it helps with debugging.

**Note:** The API of FutureStream is still new and so has a higher likelihood of changing in the future.

### read

[ref: #symbol-read]

Returns a future that will complete when the FutureStream has data placed into it. The future will be completed with the oldest value stored inside the stream. The return value will also determine whether data was retrieved, false means that the future stream was completed and no data was retrieved.

**Input:**
- `future: FutureStream[T]`

**Output:** `owned(Future[(bool, T)])`
**Generic parameters:** `T`

Returns a future that will complete when the FutureStream has data placed into it. The future will be completed with the oldest value stored inside the stream. The return value will also determine whether data was retrieved, false means that the future stream was completed and no data was retrieved.

This function will remove the data that was returned from the underlying FutureStream.

### write

[ref: #symbol-write]

Writes the specified value inside the specified future stream.

**Input:**
- `future: FutureStream[T]`
- `value: T`

**Output:** `Future[void]`
**Generic parameters:** `T`

Writes the specified value inside the specified future stream.

This will raise ValueError if future is finished.

## Type

### FutureStream

[ref: #symbol-futurestream]

```nim
FutureStream[T] = ref object
  error*: ref Exception
```

Special future that acts as a queue. Its API is still experimental and so is subject to change.
