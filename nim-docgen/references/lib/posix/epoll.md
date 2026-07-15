---
source_hash: d195ece9494c2204
source_path: lib/posix/epoll.nim
---

# epoll

[ref: #module-epoll]

## Const

### EPOLL_CTL_ADD

[ref: #symbol-epoll-ctl-add]

```nim
EPOLL_CTL_ADD = 1
```

### EPOLL_CTL_DEL

[ref: #symbol-epoll-ctl-del]

```nim
EPOLL_CTL_DEL = 2
```

### EPOLL_CTL_MOD

[ref: #symbol-epoll-ctl-mod]

```nim
EPOLL_CTL_MOD = 3
```

### EPOLLERR

[ref: #symbol-epollerr]

```nim
EPOLLERR = 0x00000008
```

### EPOLLET

[ref: #symbol-epollet]

```nim
EPOLLET = 2147483648
```

### EPOLLEXCLUSIVE

[ref: #symbol-epollexclusive]

```nim
EPOLLEXCLUSIVE = 268435456
```

### EPOLLHUP

[ref: #symbol-epollhup]

```nim
EPOLLHUP = 0x00000010
```

### EPOLLIN

[ref: #symbol-epollin]

```nim
EPOLLIN = 0x00000001
```

### EPOLLMSG

[ref: #symbol-epollmsg]

```nim
EPOLLMSG = 0x00000400
```

### EPOLLONESHOT

[ref: #symbol-epolloneshot]

```nim
EPOLLONESHOT = 1073741824
```

### EPOLLOUT

[ref: #symbol-epollout]

```nim
EPOLLOUT = 0x00000004
```

### EPOLLPRI

[ref: #symbol-epollpri]

```nim
EPOLLPRI = 0x00000002
```

### EPOLLRDBAND

[ref: #symbol-epollrdband]

```nim
EPOLLRDBAND = 0x00000080
```

### EPOLLRDHUP

[ref: #symbol-epollrdhup]

```nim
EPOLLRDHUP = 0x00002000
```

### EPOLLRDNORM

[ref: #symbol-epollrdnorm]

```nim
EPOLLRDNORM = 0x00000040
```

### EPOLLWAKEUP

[ref: #symbol-epollwakeup]

```nim
EPOLLWAKEUP = 536870912
```

### EPOLLWRBAND

[ref: #symbol-epollwrband]

```nim
EPOLLWRBAND = 0x00000200
```

### EPOLLWRNORM

[ref: #symbol-epollwrnorm]

```nim
EPOLLWRNORM = 0x00000100
```

## Proc

### epoll_create

[ref: #symbol-epoll-create]

Creates an epoll instance. Returns an fd for the new instance.

**Input:**
- `size: cint`

**Output:** `cint`
**Pragmas:** `importc: "epoll_create"`, `header: "<sys/epoll.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates an epoll instance. Returns an fd for the new instance.

The "size" parameter is a hint specifying the number of file descriptors to be associated with the new instance. The fd returned by epoll\_create() should be closed with close().

### epoll_create1

[ref: #symbol-epoll-create1]

**Input:**
- `flags: cint`

**Output:** `cint`
**Pragmas:** `importc: "epoll_create1"`, `header: "<sys/epoll.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as epoll\_create but with an FLAGS parameter. The unused SIZE parameter has been dropped.

### epoll_ctl

[ref: #symbol-epoll-ctl]

Manipulate an epoll instance "epfd". Returns 0 in case of success, -1 in case of error (the "errno" variable will contain the specific error code).

**Input:**
- `epfd: cint`
- `op: cint`
- `fd: cint | SocketHandle`
- `event: ptr EpollEvent`

**Output:** `cint`
**Generic parameters:** `fd:type`

**Pragmas:** `importc: "epoll_ctl"`, `header: "<sys/epoll.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Manipulate an epoll instance "epfd". Returns 0 in case of success, -1 in case of error (the "errno" variable will contain the specific error code).

The "op" parameter is one of the EPOLL\_CTL\_\* constants defined above. The "fd" parameter is the target of the operation. The "event" parameter describes which events the caller is interested in and any associated user data.

### epoll_wait

[ref: #symbol-epoll-wait]

Wait for events on an epoll instance "epfd". Returns the number of triggered events returned in "events" buffer. Or -1 in case of error with the "errno" variable set to the specific error code. The "events" parameter is a buffer that will contain triggered events. The "maxevents" is the maximum number of events to be returned ( usually size of "events" ). The "timeout" parameter specifies the maximum wait time in milliseconds (-1 == infinite).

**Input:**
- `epfd: cint`
- `events: ptr EpollEvent`
- `maxevents: cint`
- `timeout: cint`

**Output:** `cint`
**Pragmas:** `importc: "epoll_wait"`, `header: "<sys/epoll.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Wait for events on an epoll instance "epfd". Returns the number of triggered events returned in "events" buffer. Or -1 in case of error with the "errno" variable set to the specific error code. The "events" parameter is a buffer that will contain triggered events. The "maxevents" is the maximum number of events to be returned ( usually size of "events" ). The "timeout" parameter specifies the maximum wait time in milliseconds (-1 == infinite).

This function is a cancellation point and therefore not marked with \_\_THROW.

## Type

### EpollData

[ref: #symbol-epolldata]

```nim
EpollData {.importc: "epoll_data_t", header: "<sys/epoll.h>", pure, final, union.} = object
  fd* {.importc: "fd".}: cint
  u32* {.importc: "u32".}: uint32
  u64* {.importc: "u64".}: uint64
```

### EpollEvent

[ref: #symbol-epollevent]

```nim
EpollEvent {.importc: "struct epoll_event", header: "<sys/epoll.h>", pure, final.} = object
  events*: uint32
  data*: EpollData
```
