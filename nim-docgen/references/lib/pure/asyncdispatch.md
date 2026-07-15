---
source_hash: 79fdd06ef3c5c561
source_path: lib/pure/asyncdispatch.nim
---

# asyncdispatch

[ref: #module-asyncdispatch]

This module implements asynchronous IO. This includes a dispatcher, a Future type implementation, and an async macro which allows asynchronous code to be written in a synchronous style with the await keyword.

The dispatcher acts as a kind of event loop. You must call poll on it (or a function which does so for you such as waitFor or runForever) in order to poll for any outstanding events. The underlying implementation is based on epoll on Linux, IO Completion Ports on Windows and select on other operating systems.

The poll function will not, on its own, return any events. Instead an appropriate Future object will be completed. A Future is a type which holds a value which is not yet available, but which *may* be available in the future. You can check whether a future is finished by using the finished function. When a future is finished it means that either the value that it holds is now available or it holds an error instead. The latter situation occurs when the operation to complete a future fails with an exception. You can distinguish between the two situations with the failed function.

Future objects can also store a callback procedure which will be called automatically once the future completes.

Futures therefore can be thought of as an implementation of the proactor pattern. In this pattern you make a request for an action, and once that action is fulfilled a future is completed with the result of that action. Requests can be made by calling the appropriate functions. For example: calling the recv function will create a request for some data to be read from a socket. The future which the recv function returns will then complete once the requested amount of data is read **or** an exception occurs.

Code to read some data from a socket may look something like this:

```
var future = socket.recv(100)
future.addCallback(
  proc () =
    echo(future.read)
)
```

All asynchronous functions returning a Future will not block. They will not however return immediately. An asynchronous function will have code which will be executed before an asynchronous request is made, in most cases this code sets up the request.

In the above example, the recv function will return a brand new Future instance once the request for data to be read from the socket is made. This Future instance will complete once the requested amount of data is read, in this case it is 100 bytes. The second line sets a callback on this future which will be called once the future completes. All the callback does is write the data stored in the future to stdout. The read function is used for this and it checks whether the future completes with an error for you (if it did, it will simply raise the error), if there is no error, however, it returns the value of the future.

# [Asynchronous procedures](#asynchronous-procedures)

Asynchronous procedures remove the pain of working with callbacks. They do this by allowing you to write asynchronous code the same way as you would write synchronous code.

An asynchronous procedure is marked using the {.async.} pragma. When marking a procedure with the {.async.} pragma it must have a Future[T] return type or no return type at all. If you do not specify a return type then Future[void] is assumed.

Inside asynchronous procedures await can be used to call any procedures which return a Future; this includes asynchronous procedures. When a procedure is "awaited", the asynchronous procedure it is awaited in will suspend its execution until the awaited procedure's Future completes. At which point the asynchronous procedure will resume its execution. During the period when an asynchronous procedure is suspended other asynchronous procedures will be run by the dispatcher.

The await call may be used in many contexts. It can be used on the right hand side of a variable declaration: var data = await socket.recv(100), in which case the variable will be set to the value of the future automatically. It can be used to await a Future object, and it can be used to await a procedure returning a Future[void]: await socket.send("foobar").

If an awaited future completes with an error, then await will re-raise this error. To avoid this, you can use the yield keyword instead of await. The following section shows different ways that you can handle exceptions in async procs.

**Caution:**
Procedures marked {.async.} do not support mutable parameters such as var int. References such as ref int should be used instead.

## [Handling Exceptions](#asynchronous-procedures-handling-exceptions)

You can handle exceptions in the same way as in ordinary Nim code; by using the try statement:

```
try:
  let data = await sock.recv(100)
  echo("Received ", data)
except:
  # Handle exception
```

An alternative approach to handling exceptions is to use yield on a future then check the future's failed property. For example:

```
var future = sock.recv(100)
yield future
if future.failed:
  # Handle exception
```

# [Discarding futures](#discarding-futures)

Futures should **never** be discarded directly because they may contain errors. If you do not care for the result of a Future then you should use the asyncCheck procedure instead of the discard keyword. Note that this does not wait for completion, and you should use waitFor or await for that purpose.

**Note:**
await also checks if the future fails, so you can safely discard its result.

# [Handling futures](#handling-futures)

There are many different operations that apply to a future. The three primary high-level operations are asyncCheck, waitFor, and await.

* asyncCheck: Raises an exception if the future fails. It neither waits for the future to finish nor returns the result of the future.
* waitFor: Polls the event loop and blocks the current thread until the future finishes. This is often used to call an async procedure from a synchronous context and should never be used in an async proc.
* await: Pauses execution in the current async procedure until the future finishes. While the current procedure is paused, other async procedures will continue running. Should be used instead of waitFor in an async procedure.

Here is a handy quick reference chart showing their high-level differences:

| Procedure | Context | Blocking |
| --- | --- | --- |
| asyncCheck | non-async and async | non-blocking |
| waitFor | non-async | blocks current thread |
| await | async | suspends current proc |

# [Examples](#examples)

For examples take a look at the documentation for the modules implementing asynchronous IO. A good place to start is the [asyncnet module](asyncnet.html).

# [Investigating pending futures](#investigating-pending-futures)

It's possible to get into a situation where an async proc, or more accurately a Future[T] gets stuck and never completes. This can happen for various reasons and can cause serious memory leaks. When this occurs it's hard to identify the procedure that is stuck.

Thankfully there is a mechanism which tracks the count of each pending future. All you need to do to enable it is compile with -d:futureLogging and use the getFuturesInProgress procedure to get the list of pending futures together with the stack traces to the moment of their creation.

You may also find it useful to use this [prometheus package](https://github.com/dom96/prometheus) which will log the pending futures into prometheus, allowing you to analyse them via a nice graph.

# [Limitations/Bugs](#limitationsslashbugs)

* The effect system (raises: []) does not work with async procedures.
* Mutable parameters are not supported by async procedures.

# [Multiple async backend support](#multiple-async-backend-support)

Thanks to its powerful macro support, Nim allows async/await to be implemented in libraries with only minimal support from the language - as such, multiple async libraries exist, including asyncdispatch and chronos, and more may come to be developed in the future.

Libraries built on top of async/await may wish to support multiple async backends - the best way to do so is to create separate modules for each backend that may be imported side-by-side.

An alternative way is to select backend using a global compile flag - this method makes it difficult to compose applications that use both backends as may happen with transitive dependencies, but may be appropriate in some cases - libraries choosing this path should call the flag asyncBackend, allowing applications to choose the backend with -d:asyncBackend=<backend\_name>.

Known async backends include:

* -d:asyncBackend=none: disable async support completely
* -d:asyncBackend=asyncdispatch: <https://nim-lang.org/docs/asyncdispatch.html>
* -d:asyncBackend=chronos: <https://github.com/status-im/nim-chronos/>

none can be used when a library supports both a synchronous and asynchronous API, to disable the latter.

## Examples

```nim
var future = socket.recv(100)
future.addCallback(
  proc () =
    echo(future.read)
)
```

```nim
try:
  let data = await sock.recv(100)
  echo("Received ", data)
except:
  # Handle exception
```

```nim
var future = sock.recv(100)
yield future
if future.failed:
  # Handle exception
```

## Proc

### `==`

[ref: #symbol-]

**Input:**
- `x: AsyncFD`
- `y: AsyncFD`

**Output:** `bool`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### accept

[ref: #symbol-accept]

Accepts a new connection. Returns a future containing the client socket corresponding to that connection.

**Input:**
- `socket: AsyncFD`
- `flags:  = {SafeDisconn}`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `owned(Future[AsyncFD])`
**Pragmas:** `raises: [ValueError, OSError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, OSError, Exception`, `tags: RootEffect`, `forbids: `

Accepts a new connection. Returns a future containing the client socket corresponding to that connection.

If inheritable is false (the default), the resulting client socket will not be inheritable by child processes.

The future will complete when the connection is successfully accepted.

### acceptAddr

[ref: #symbol-acceptaddr]

Accepts a new connection. Returns a future containing the client socket corresponding to that connection and the remote address of the client. The future will complete when the connection is successfully accepted.

**Input:**
- `socket: AsyncFD`
- `flags:  = {SafeDisconn}`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `owned(Future[tuple[address: string, client: AsyncFD]])`
**Pragmas:** `gcsafe`, `raises: [ValueError, OSError, Exception, ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, OSError, Exception, ValueError, Exception`, `tags: RootEffect`, `forbids: `

Accepts a new connection. Returns a future containing the client socket corresponding to that connection and the remote address of the client. The future will complete when the connection is successfully accepted.

The resulting client socket is automatically registered to the dispatcher.

If inheritable is false (the default), the resulting client socket will not be inheritable by child processes.

The accept call may result in an error if the connecting socket disconnects during the duration of the accept. If the SafeDisconn flag is specified then this error will not be raised and instead accept will be called again.

### activeDescriptors

[ref: #symbol-activedescriptors]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the current number of active file descriptors for the current event loop. This is a cheap operation that does not involve a system call.

### addEvent

[ref: #symbol-addevent]

**Input:**
- `ev: AsyncEvent`
- `cb: Callback`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Registers callback cb to be called when ev will be signaled

### addProcess

[ref: #symbol-addprocess]

**Input:**
- `pid: int`
- `cb: Callback`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Registers callback cb to be called when process with process ID pid exited.

### addRead

[ref: #symbol-addread]

Start watching the file descriptor for read availability and then call the callback cb.

**Input:**
- `fd: AsyncFD`
- `cb: Callback`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Start watching the file descriptor for read availability and then call the callback cb.

This is not pure mechanism for Windows Completion Ports (IOCP), so if you can avoid it, please do it. Use addRead only if really need it (main usecase is adaptation of unix-like libraries to be asynchronous on Windows).

If you use this function, you don't need to use asyncdispatch.recv() or asyncdispatch.accept(), because they are using IOCP, please use nativesockets.recv() and nativesockets.accept() instead.

Be sure your callback cb returns true, if you want to remove watch of read notifications, and false, if you want to continue receiving notifications.

### addTimer

[ref: #symbol-addtimer]

Registers callback cb to be called when timer expired.

**Input:**
- `timeout: int`
- `oneshot: bool`
- `cb: Callback`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Registers callback cb to be called when timer expired.

Parameters:

* timeout - timeout value in milliseconds.
* oneshot
  + true - generate only one timeout event
  + false - generate timeout events periodically

### addWrite

[ref: #symbol-addwrite]

Start watching the file descriptor for write availability and then call the callback cb.

**Input:**
- `fd: AsyncFD`
- `cb: Callback`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Start watching the file descriptor for write availability and then call the callback cb.

This is not pure mechanism for Windows Completion Ports (IOCP), so if you can avoid it, please do it. Use addWrite only if really need it (main usecase is adaptation of unix-like libraries to be asynchronous on Windows).

If you use this function, you don't need to use asyncdispatch.send() or asyncdispatch.connect(), because they are using IOCP, please use nativesockets.send() and nativesockets.connect() instead.

Be sure your callback cb returns true, if you want to remove watch of write notifications, and false, if you want to continue receiving notifications.

### callSoon

[ref: #symbol-callsoon]

**Input:**
- `cbproc: proc () {.gcsafe.}`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Schedule cbproc to be called as soon as possible. The callback is called when control returns to the event loop.

### close

[ref: #symbol-close]

**Input:**
- `ev: AsyncEvent`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Closes event ev.

### closeSocket

[ref: #symbol-closesocket]

**Input:**
- `socket: AsyncFD`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Closes a socket and ensures that it is unregistered.

### connect

[ref: #symbol-connect]

**Input:**
- `socket: AsyncFD`
- `address: string`
- `port: Port`
- `domain:  = Domain.AF_INET`

**Output:** `owned(Future[void])`
**Pragmas:** `raises: [OSError, IOError, ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: OSError, IOError, ValueError, Exception`, `tags: RootEffect`, `forbids: `

### contains

[ref: #symbol-contains]

**Input:**
- `disp: PDispatcher`
- `fd: AsyncFD`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createAsyncNativeSocket

[ref: #symbol-createasyncnativesocket]

**Input:**
- `domain: cint`
- `sockType: cint`
- `protocol: cint`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `AsyncFD`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

### createAsyncNativeSocket

[ref: #symbol-createasyncnativesocket]

**Input:**
- `domain: Domain = Domain.AF_INET`
- `sockType: SockType = SOCK_STREAM`
- `protocol: Protocol = IPPROTO_TCP`
- `inheritable:  = defined(nimInheritHandles)`

**Output:** `AsyncFD`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

### dial

[ref: #symbol-dial]

**Input:**
- `address: string`
- `port: Port`
- `protocol: Protocol = IPPROTO_TCP`

**Output:** `owned(Future[AsyncFD])`
**Pragmas:** `raises: [OSError, ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: OSError, ValueError, Exception`, `tags: RootEffect`, `forbids: `

Establishes connection to the specified address:port pair via the specified protocol. The procedure iterates through possible resolutions of the address until it succeeds, meaning that it seamlessly works with both IPv4 and IPv6. Returns the async file descriptor, registered in the dispatcher of the current thread, ready to send or receive data.

### drain

[ref: #symbol-drain]

**Input:**
- `timeout:  = 500`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError, Exception, OSError]`, `tags: [TimeEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception, OSError`, `tags: TimeEffect, RootEffect`, `forbids: `

Waits for completion of **all** events and processes them. Raises ValueError if there are no pending operations. In contrast to poll this processes as many events as are available until the timeout has elapsed.

### getGlobalDispatcher

[ref: #symbol-getglobaldispatcher]

**Input:**
- *(none)*

**Output:** `PDispatcher`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getIoHandler

[ref: #symbol-getiohandler]

**Input:**
- `disp: PDispatcher`

**Output:** `Handle`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the underlying IO Completion Port handle (Windows) or selector (Unix) for the specified dispatcher.

### hasPendingOperations

[ref: #symbol-haspendingoperations]

**Input:**
- *(none)*

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if the global dispatcher has pending operations.

### maxDescriptors

[ref: #symbol-maxdescriptors]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `raises: OSError`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns the maximum number of active file descriptors for the current process. This involves a system call. For now maxDescriptors is supported on the following OSes: Windows, Linux, OSX, BSD, Solaris.

### newAsyncEvent

[ref: #symbol-newasyncevent]

Creates a new thread-safe AsyncEvent object.

**Input:**
- *(none)*

**Output:** `AsyncEvent`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Creates a new thread-safe AsyncEvent object.

New AsyncEvent object is not automatically registered with dispatcher like AsyncSocket.

### newCustom

[ref: #symbol-newcustom]

**Input:**
- *(none)*

**Output:** `CustomRef`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newDispatcher

[ref: #symbol-newdispatcher]

**Input:**
- *(none)*

**Output:** `owned PDispatcher`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new Dispatcher instance.

### poll

[ref: #symbol-poll]

**Input:**
- `timeout:  = 500`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError, Exception, OSError]`, `tags: [TimeEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception, OSError`, `tags: TimeEffect, RootEffect`, `forbids: `

Waits for completion events and processes them. Raises ValueError if there are no pending operations. This runs the underlying OS epoll or kqueue primitive only once.

### readAll

[ref: #symbol-readall]

**Input:**
- `future: FutureStream[string]`

**Output:** `owned(Future[string])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError`, `tags: RootEffect`, `forbids: `

Returns a future that will complete when all the string data from the specified future stream is retrieved.

### recv

[ref: #symbol-recv]

Reads **up to** size bytes from socket. Returned future will complete once all the data requested is read, a part of the data has been read, or the socket has disconnected in which case the future will complete with a value of "".

**Input:**
- `socket: AsyncFD`
- `size: int`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[string])`
**Pragmas:** `raises: [ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception`, `tags: RootEffect`, `forbids: `

Reads **up to** size bytes from socket. Returned future will complete once all the data requested is read, a part of the data has been read, or the socket has disconnected in which case the future will complete with a value of "".

**Warning:**
The Peek socket flag is not supported on Windows.

### recvFromInto

[ref: #symbol-recvfrominto]

**Input:**
- `socket: AsyncFD`
- `data: pointer`
- `size: int`
- `saddr: ptr SockAddr`
- `saddrLen: ptr SockLen`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[int])`
**Pragmas:** `raises: [ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception`, `tags: RootEffect`, `forbids: `

Receives a datagram data from socket into buf, which must be at least of size size, address of datagram's sender will be stored into saddr and saddrLen. Returned future will complete once one datagram has been received, and will return size of packet received.

### recvInto

[ref: #symbol-recvinto]

Reads **up to** size bytes from socket into buf, which must at least be of that size. Returned future will complete once all the data requested is read, a part of the data has been read, or the socket has disconnected in which case the future will complete with a value of 0.

**Input:**
- `socket: AsyncFD`
- `buf: pointer`
- `size: int`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[int])`
**Pragmas:** `raises: [ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception`, `tags: RootEffect`, `forbids: `

Reads **up to** size bytes from socket into buf, which must at least be of that size. Returned future will complete once all the data requested is read, a part of the data has been read, or the socket has disconnected in which case the future will complete with a value of 0.

**Warning:**
The Peek socket flag is not supported on Windows.

### register

[ref: #symbol-register]

**Input:**
- `fd: AsyncFD`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Registers fd with the dispatcher.

### runForever

[ref: #symbol-runforever]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: [ValueError, Exception, OSError]`, `tags: [TimeEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception, OSError`, `tags: TimeEffect, RootEffect`, `forbids: `

Begins a never ending global dispatcher poll loop.

### send

[ref: #symbol-send]

Sends size bytes from buf to socket. The returned future will complete once all data has been sent.

**Input:**
- `socket: AsyncFD`
- `buf: pointer`
- `size: int`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[void])`
**Pragmas:** `raises: [ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception`, `tags: RootEffect`, `forbids: `

Sends size bytes from buf to socket. The returned future will complete once all data has been sent.

**Warning:**
Use it with caution. If buf refers to GC'ed object, you must use GC\_ref/GC\_unref calls to avoid early freeing of the buffer.

### send

[ref: #symbol-send]

**Input:**
- `socket: AsyncFD`
- `data: string`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[void])`
**Pragmas:** `raises: [ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception`, `tags: RootEffect`, `forbids: `

Sends data to socket. The returned future will complete once all data has been sent.

### sendTo

[ref: #symbol-sendto]

**Input:**
- `socket: AsyncFD`
- `data: pointer`
- `size: int`
- `saddr: ptr SockAddr`
- `saddrLen: SockLen`
- `flags:  = {SafeDisconn}`

**Output:** `owned(Future[void])`
**Pragmas:** `raises: [ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception`, `tags: RootEffect`, `forbids: `

Sends data to specified destination saddr, using socket socket. The returned future will complete once all data has been sent.

### setGlobalDispatcher

[ref: #symbol-setglobaldispatcher]

**Input:**
- `disp: sink PDispatcher`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setInheritable

[ref: #symbol-setinheritable]

Control whether a file handle can be inherited by child processes. Returns true on success.

**Input:**
- `fd: AsyncFD`
- `inheritable: bool`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Control whether a file handle can be inherited by child processes. Returns true on success.

This procedure is not guaranteed to be available for all platforms. Test for availability with [declared()](system.html#declared,untyped).

### sleepAsync

[ref: #symbol-sleepasync]

**Input:**
- `ms: int | float`

**Output:** `owned(Future[void])`
**Generic parameters:** `ms:type`

Suspends the execution of the current async procedure for the next ms milliseconds.

### trigger

[ref: #symbol-trigger]

**Input:**
- `ev: AsyncEvent`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Set event ev to signaled state.

### unregister

[ref: #symbol-unregister]

**Input:**
- `fd: AsyncFD`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unregisters fd.

### unregister

[ref: #symbol-unregister]

**Input:**
- `ev: AsyncEvent`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Unregisters event ev.

### waitFor

[ref: #symbol-waitfor]

**Input:**
- `fut: Future[T]`

**Output:** `T`
**Generic parameters:** `T`

**Blocks** the current thread until the specified future completes.

### withTimeout

[ref: #symbol-withtimeout]

Returns a future which will complete once fut completes or after timeout milliseconds has elapsed.

**Input:**
- `fut: Future[T]`
- `timeout: int`

**Output:** `owned(Future[bool])`
**Generic parameters:** `T`

Returns a future which will complete once fut completes or after timeout milliseconds has elapsed.

If fut completes first the returned future will hold true, otherwise, if timeout milliseconds has elapsed first, the returned future will hold false.

## Type

### AsyncEvent

[ref: #symbol-asyncevent]

```nim
AsyncEvent = ptr AsyncEventImpl
```

### AsyncFD

[ref: #symbol-asyncfd]

```nim
AsyncFD = distinct int
```

### Callback

[ref: #symbol-callback]

```nim
Callback = proc (fd: AsyncFD): bool {.closure, gcsafe.}
```

### CompletionData

[ref: #symbol-completiondata]

```nim
CompletionData = object
  fd*: AsyncFD
  cb*: owned(proc (fd: AsyncFD; bytesTransferred: DWORD; errcode: OSErrorCode) {.
      closure, gcsafe.})
  cell*: ForeignCell
```

### CustomRef

[ref: #symbol-customref]

```nim
CustomRef = ref CustomObj
```

### PDispatcher

[ref: #symbol-pdispatcher]

```nim
PDispatcher = ref object of PDispatcherBase
  handles*: HashSet[AsyncFD]
```
