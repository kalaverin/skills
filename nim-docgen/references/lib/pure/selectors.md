---
source_hash: 3d1c0f3dce7773d4
source_path: lib/pure/selectors.nim
---

# selectors

[ref: #module-selectors]

This module allows high-level and efficient I/O multiplexing.

Supported OS primitives: epoll, kqueue, poll and Windows select.

To use threadsafe version of this module, it needs to be compiled with both -d:threadsafe and --threads:on options.

Supported features: files, sockets, pipes, timers, processes, signals and user events.

Fully supported OS: MacOSX, FreeBSD, OpenBSD, NetBSD, Linux (except for Android).

Partially supported OS: Windows (only sockets and user events), Solaris (files, sockets, handles and user events). Android (files, sockets, handles and user events).

By default, the implementation is chosen based on the target platform; you can pass -d:nimIoselector=value to override it. Accepted values are "epoll", "kqueue", "poll", and "select".

TODO: /dev/poll, event ports and filesystem events.

## Examples

```nim
s.withData(fd, value) do:
  # block is executed only if `fd` registered in selector `s`.
  value.uid = 1000
do:
  # block is executed if `fd` not registered in selector `s`.
  raise
```

```nim
s.withData(fd, value) do:
  # block is executed only if `fd` registered in selector `s`
  value.uid = 1000
```

## Const

### ioselSupportedPlatform

[ref: #symbol-ioselsupportedplatform]

```nim
ioselSupportedPlatform = true
```

This constant is used to determine whether the destination platform is fully supported by ioselectors module.

## Proc

### close

[ref: #symbol-close]

**Input:**
- `s: Selector[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Closes the selector.

### close

[ref: #symbol-close]

**Input:**
- `ev: SelectEvent`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Closes user-defined event ev.

### contains

[ref: #symbol-contains]

**Input:**
- `s: Selector[T]`
- `fd: SocketHandle | int`

**Output:** `bool`
**Generic parameters:** `T`, `fd:type`

**Pragmas:** `inline`

Determines whether selector contains a file descriptor.

### getData

[ref: #symbol-getdata]

**Input:**
- `s: Selector[T]`
- `fd: SocketHandle | int`

**Output:** `var T`
**Generic parameters:** `T`, `fd:type`

Retrieves application-defined data associated with descriptor fd. If specified descriptor fd is not registered, empty/default value will be returned.

### getFd

[ref: #symbol-getfd]

Retrieves the underlying selector's file descriptor.

**Input:**
- `s: Selector[T]`

**Output:** `int`
**Generic parameters:** `T`

Retrieves the underlying selector's file descriptor.

For *poll* and *select* selectors -1 is returned.

### newSelectEvent

[ref: #symbol-newselectevent]

**Input:**
- *(none)*

**Output:** `SelectEvent`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new user-defined event.

### newSelector

[ref: #symbol-newselector]

**Input:**
- *(none)*

**Output:** `Selector[T]`
**Generic parameters:** `T`

Creates a new selector

### registerEvent

[ref: #symbol-registerevent]

Registers selector event ev in selector s.

**Input:**
- `s: Selector[T]`
- `ev: SelectEvent`
- `data: T`

**Output:** *(none)*
**Generic parameters:** `T`

Registers selector event ev in selector s.

The data is application-defined data, which will be passed when ev happens.

### registerHandle

[ref: #symbol-registerhandle]

**Input:**
- `s: Selector[T]`
- `fd: int | SocketHandle`
- `events: set[Event]`
- `data: T`

**Output:** *(none)*
**Generic parameters:** `T`, `fd:type`

Registers file/socket descriptor fd to selector s with events set in events. The data is application-defined data, which will be passed when an event is triggered.

### registerProcess

[ref: #symbol-registerprocess]

Registers a process id (pid) notification (when process has exited) in selector s.

**Input:**
- `s: Selector[T]`
- `pid: int`
- `data: T`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `discardable`

Registers a process id (pid) notification (when process has exited) in selector s.

The data is application-defined data, which will be passed when process with pid has exited.

Returns the file descriptor for the registered signal.

### registerSignal

[ref: #symbol-registersignal]

Registers Unix signal notification with signal to selector s.

**Input:**
- `s: Selector[T]`
- `signal: int`
- `data: T`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `discardable`

Registers Unix signal notification with signal to selector s.

The data is application-defined data, which will be passed when signal raises.

Returns the file descriptor for the registered signal.

**Note:** This function is not supported on Windows.

### registerTimer

[ref: #symbol-registertimer]

Registers timer notification with timeout (in milliseconds) to selector s.

**Input:**
- `s: Selector[T]`
- `timeout: int`
- `oneshot: bool`
- `data: T`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `discardable`

Registers timer notification with timeout (in milliseconds) to selector s.

If oneshot is true, timer will be notified only once.

Set oneshot to false if you want periodic notifications.

The data is application-defined data, which will be passed, when the timer is triggered.

Returns the file descriptor for the registered timer.

### registerVnode

[ref: #symbol-registervnode]

Registers selector BSD/MacOSX specific vnode events for file descriptor fd and events events. data application-defined data, which to be passed, when vnode event happens.

**Input:**
- `s: Selector[T]`
- `fd: cint`
- `events: set[Event]`
- `data: T`

**Output:** *(none)*
**Generic parameters:** `T`

Registers selector BSD/MacOSX specific vnode events for file descriptor fd and events events. data application-defined data, which to be passed, when vnode event happens.

**Note:** This function is supported only by BSD and MacOSX.

### select

[ref: #symbol-select]

Waits for events registered in selector s.

**Input:**
- `s: Selector[T]`
- `timeout: int`

**Output:** `seq[ReadyKey]`
**Generic parameters:** `T`

Waits for events registered in selector s.

The timeout argument specifies the maximum number of milliseconds the function will be blocked for if no events are ready. Specifying a timeout of -1 causes the function to block indefinitely.

Returns a list of triggered events.

### selectInto

[ref: #symbol-selectinto]

Waits for events registered in selector s.

**Input:**
- `s: Selector[T]`
- `timeout: int`
- `results: var openArray[ReadyKey]`

**Output:** `int`
**Generic parameters:** `T`

Waits for events registered in selector s.

The timeout argument specifies the maximum number of milliseconds the function will be blocked for if no events are ready. Specifying a timeout of -1 causes the function to block indefinitely. All available events will be stored in results array.

Returns number of triggered events.

### setData

[ref: #symbol-setdata]

Associate application-defined data with descriptor fd.

**Input:**
- `s: Selector[T]`
- `fd: SocketHandle | int`
- `data: var T`

**Output:** `bool`
**Generic parameters:** `T`, `fd:type`

Associate application-defined data with descriptor fd.

Returns true, if data was successfully updated, false otherwise.

### trigger

[ref: #symbol-trigger]

**Input:**
- `ev: SelectEvent`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Trigger event ev.

### unregister

[ref: #symbol-unregister]

**Input:**
- `s: Selector[T]`
- `ev: SelectEvent`

**Output:** *(none)*
**Generic parameters:** `T`

Unregisters user-defined event ev from selector s.

### unregister

[ref: #symbol-unregister]

**Input:**
- `s: Selector[T]`
- `fd: int | SocketHandle | cint`

**Output:** *(none)*
**Generic parameters:** `T`, `fd:type`

Unregisters file/socket descriptor fd from selector s.

### updateHandle

[ref: #symbol-updatehandle]

**Input:**
- `s: Selector[T]`
- `fd: int | SocketHandle`
- `events: set[Event]`

**Output:** *(none)*
**Generic parameters:** `T`, `fd:type`

Update file/socket descriptor fd, registered in selector s with new events set event.

## Template

### isEmpty

[ref: #symbol-isempty]

**Input:**
- `s: Selector[T]`

**Output:** `bool`
**Generic parameters:** `T`

Returns true, if there are no registered events or descriptors in selector.

### withData

[ref: #symbol-withdata]

Retrieves the application-data assigned with descriptor fd to value. This value can be modified in the scope of the withData call.

**Input:**
- `s: Selector[T]`
- `fd: SocketHandle | int`
- `value: untyped`
- `body: untyped`

**Output:** *(none)*
**Generic parameters:** `T`, `fd:type`

Retrieves the application-data assigned with descriptor fd to value. This value can be modified in the scope of the withData call.

```
s.withData(fd, value) do:
  # block is executed only if `fd` registered in selector `s`
  value.uid = 1000
```

### withData

[ref: #symbol-withdata]

Retrieves the application-data assigned with descriptor fd to value. This value can be modified in the scope of the withData call.

**Input:**
- `s: Selector[T]`
- `fd: SocketHandle | int`
- `value: untyped`
- `body1: untyped`
- `body2: untyped`

**Output:** *(none)*
**Generic parameters:** `T`, `fd:type`

Retrieves the application-data assigned with descriptor fd to value. This value can be modified in the scope of the withData call.

```
s.withData(fd, value) do:
  # block is executed only if `fd` registered in selector `s`.
  value.uid = 1000
do:
  # block is executed if `fd` not registered in selector `s`.
  raise
```

## Type

### Event

[ref: #symbol-event]

```nim
Event {.pure.} = enum
  Read,                     ## Descriptor is available for read
  Write,                    ## Descriptor is available for write
  Timer,                    ## Timer descriptor is completed
  Signal,                   ## Signal is raised
  Process,                  ## Process is finished
  Vnode,                    ## BSD specific file change
  User,                     ## User event is raised
  Error,                    ## Error occurred while waiting for descriptor
  VnodeWrite,               ## NOTE_WRITE (BSD specific, write to file occurred)
  VnodeDelete,              ## NOTE_DELETE (BSD specific, unlink of file occurred)
  VnodeExtend,              ## NOTE_EXTEND (BSD specific, file extended)
  VnodeAttrib,              ## NOTE_ATTRIB (BSD specific, file attributes changed)
  VnodeLink,                ## NOTE_LINK (BSD specific, file link count changed)
  VnodeRename,              ## NOTE_RENAME (BSD specific, file renamed)
  VnodeRevoke                ## NOTE_REVOKE (BSD specific, file revoke occurred)
```

An enum which hold event types

### IOSelectorsException

[ref: #symbol-ioselectorsexception]

```nim
IOSelectorsException = object of CatchableError
```

Exception that is raised if an IOSelectors error occurs.

### ReadyKey

[ref: #symbol-readykey]

```nim
ReadyKey = object
  fd*: int                   ## file/socket descriptor
  events*: set[Event]        ## set of events
  errorCode*: OSErrorCode    ## additional error code information for
                             ## Error events
```

An object which holds result for descriptor

### SelectEvent

[ref: #symbol-selectevent]

```nim
SelectEvent = object
```

An object which holds user defined event

### Selector

[ref: #symbol-selector]

```nim
Selector[T] = ref object
```

An object which holds descriptors to be checked for read/write status
