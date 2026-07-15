---
source_hash: 116468817997f976
source_path: lib/posix/kqueue.nim
---

# kqueue

[ref: #module-kqueue]

## Const

### EV_ADD

[ref: #symbol-ev-add]

```nim
EV_ADD = 0x00000001
```

Add event to queue (implies enable). Re-adding an existing element modifies it.

### EV_CLEAR

[ref: #symbol-ev-clear]

```nim
EV_CLEAR = 0x00000020
```

Clear event state after reporting.

### EV_DELETE

[ref: #symbol-ev-delete]

```nim
EV_DELETE = 0x00000002
```

Delete event from queue.

### EV_DISABLE

[ref: #symbol-ev-disable]

```nim
EV_DISABLE = 0x00000008
```

Disable event (not reported).

### EV_DISPATCH

[ref: #symbol-ev-dispatch]

```nim
EV_DISPATCH = 0x00000080
```

Disable event after reporting.

### EV_DROP

[ref: #symbol-ev-drop]

```nim
EV_DROP = 0x00001000
```

Not should be dropped

### EV_ENABLE

[ref: #symbol-ev-enable]

```nim
EV_ENABLE = 0x00000004
```

Enable event.

### EV_EOF

[ref: #symbol-ev-eof]

```nim
EV_EOF = 0x00008000
```

EOF detected

### EV_ERROR

[ref: #symbol-ev-error]

```nim
EV_ERROR = 0x00004000
```

Error, data contains errno

### EV_FLAG1

[ref: #symbol-ev-flag1]

```nim
EV_FLAG1 = 0x00002000
```

Filter-specific flag

### EV_NODATA

[ref: #symbol-ev-nodata]

```nim
EV_NODATA = 0x00001000
```

EOF and no more data

### EV_ONESHOT

[ref: #symbol-ev-oneshot]

```nim
EV_ONESHOT = 0x00000010
```

Only report one occurrence.

### EV_RECEIPT

[ref: #symbol-ev-receipt]

```nim
EV_RECEIPT = 0x00000040
```

Force EV\_ERROR on success, data == 0

### EV_SYSFLAGS

[ref: #symbol-ev-sysflags]

```nim
EV_SYSFLAGS = 0x0000F000
```

Reserved by system

### EVFILT_AIO

[ref: #symbol-evfilt-aio]

```nim
EVFILT_AIO = -3
```

attached to aio requests

### EVFILT_FS

[ref: #symbol-evfilt-fs]

```nim
EVFILT_FS = -9
```

filesystem events

### EVFILT_MACHPORT

[ref: #symbol-evfilt-machport]

```nim
EVFILT_MACHPORT = -8
```

Mach portsets

### EVFILT_PROC

[ref: #symbol-evfilt-proc]

```nim
EVFILT_PROC = -5
```

attached to struct proc

### EVFILT_READ

[ref: #symbol-evfilt-read]

```nim
EVFILT_READ = -1
```

### EVFILT_SIGNAL

[ref: #symbol-evfilt-signal]

```nim
EVFILT_SIGNAL = -6
```

attached to struct proc

### EVFILT_TIMER

[ref: #symbol-evfilt-timer]

```nim
EVFILT_TIMER = -7
```

timers

### EVFILT_USER

[ref: #symbol-evfilt-user]

```nim
EVFILT_USER = -10
```

user events

### EVFILT_VNODE

[ref: #symbol-evfilt-vnode]

```nim
EVFILT_VNODE = -4
```

attached to vnodes

### EVFILT_WRITE

[ref: #symbol-evfilt-write]

```nim
EVFILT_WRITE = -2
```

### NOTE_ATTRIB

[ref: #symbol-note-attrib]

```nim
NOTE_ATTRIB = 0x00000008
```

attributes changed

### NOTE_CHILD

[ref: #symbol-note-child]

```nim
NOTE_CHILD = 0x00000004'u32
```

am a child process

### NOTE_DELETE

[ref: #symbol-note-delete]

```nim
NOTE_DELETE = 0x00000001
```

vnode was removed

### NOTE_EXEC

[ref: #symbol-note-exec]

```nim
NOTE_EXEC = 0x20000000'u32
```

process exec'd

### NOTE_EXIT

[ref: #symbol-note-exit]

```nim
NOTE_EXIT = 0x80000000'u32
```

process exited

### NOTE_EXTEND

[ref: #symbol-note-extend]

```nim
NOTE_EXTEND = 0x00000004
```

size increased

### NOTE_FFAND

[ref: #symbol-note-ffand]

```nim
NOTE_FFAND = 0x40000000'u32
```

AND fflags

### NOTE_FFCOPY

[ref: #symbol-note-ffcopy]

```nim
NOTE_FFCOPY = 0xC0000000'u32
```

copy fflags

### NOTE_FFCTRLMASK

[ref: #symbol-note-ffctrlmask]

```nim
NOTE_FFCTRLMASK = 0xC0000000'u32
```

masks for operations

### NOTE_FFLAGSMASK

[ref: #symbol-note-fflagsmask]

```nim
NOTE_FFLAGSMASK = 0x00FFFFFF'u32
```

### NOTE_FFNOP

[ref: #symbol-note-ffnop]

```nim
NOTE_FFNOP = 0x00000000'u32
```

ignore input fflags

### NOTE_FFOR

[ref: #symbol-note-ffor]

```nim
NOTE_FFOR = 0x80000000'u32
```

OR fflags

### NOTE_FORK

[ref: #symbol-note-fork]

```nim
NOTE_FORK = 0x40000000'u32
```

process forked

### NOTE_LINK

[ref: #symbol-note-link]

```nim
NOTE_LINK = 0x00000010
```

link count changed

### NOTE_LOWAT

[ref: #symbol-note-lowat]

```nim
NOTE_LOWAT = 0x00000001
```

low water mark

### NOTE_MSECONDS

[ref: #symbol-note-mseconds]

```nim
NOTE_MSECONDS = 0x00000002'u32
```

data is milliseconds

### NOTE_NSECONDS

[ref: #symbol-note-nseconds]

```nim
NOTE_NSECONDS = 0x00000008'u32
```

data is nanoseconds

### NOTE_PCTRLMASK

[ref: #symbol-note-pctrlmask]

```nim
NOTE_PCTRLMASK = 0xF0000000'u32
```

mask for hint bits

### NOTE_PDATAMASK

[ref: #symbol-note-pdatamask]

```nim
NOTE_PDATAMASK = 0x000FFFFF'u32
```

mask for pid

### NOTE_RENAME

[ref: #symbol-note-rename]

```nim
NOTE_RENAME = 0x00000020
```

vnode was renamed

### NOTE_REVOKE

[ref: #symbol-note-revoke]

```nim
NOTE_REVOKE = 0x00000040
```

vnode access was revoked

### NOTE_SECONDS

[ref: #symbol-note-seconds]

```nim
NOTE_SECONDS = 0x00000001'u32
```

data is seconds

### NOTE_TRACK

[ref: #symbol-note-track]

```nim
NOTE_TRACK = 0x00000001'u32
```

follow across forks

### NOTE_TRACKERR

[ref: #symbol-note-trackerr]

```nim
NOTE_TRACKERR = 0x00000002'u32
```

could not track child

### NOTE_TRIGGER

[ref: #symbol-note-trigger]

```nim
NOTE_TRIGGER = 0x01000000'u32
```

Cause the event to be triggered for output.

### NOTE_USECONDS

[ref: #symbol-note-useconds]

```nim
NOTE_USECONDS = 0x00000004'u32
```

data is microseconds

### NOTE_WRITE

[ref: #symbol-note-write]

```nim
NOTE_WRITE = 0x00000002
```

data contents changed

## Proc

### EV_SET

[ref: #symbol-ev-set]

**Input:**
- `event: ptr KEvent`
- `ident: uint`
- `filter: cshort`
- `flags: cushort`
- `fflags: cuint`
- `data: int`
- `udata: pointer`

**Output:** *(none)*
**Pragmas:** `importc: "EV_SET"`, `header: "<sys/event.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Fills event with given data.

### kevent

[ref: #symbol-kevent]

**Input:**
- `kqFD: cint`
- `changelist: ptr KEvent`
- `nchanges: cint`
- `eventlist: ptr KEvent`
- `nevents: cint`
- `timeout: ptr Timespec`

**Output:** `cint`
**Pragmas:** `importc: "kevent"`, `header: "<sys/event.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Manipulates queue for given kqFD descriptor.

### kqueue

[ref: #symbol-kqueue]

**Input:**
- *(none)*

**Output:** `cint`
**Pragmas:** `importc: "kqueue"`, `header: "<sys/event.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates new queue and returns its descriptor.

## Type

### KEvent

[ref: #symbol-kevent]

```nim
KEvent {.importc: "struct kevent", header: """#include <sys/types.h>
                       #include <sys/event.h>
                       #include <sys/time.h>""",
         pure, final.} = object
  ident*: uint               ## identifier for this event  (uintptr_t)
  filter*: cshort            ## filter for event
  flags*: cushort            ## general flags
  fflags*: cuint             ## filter-specific flags
  data*: int                 ## filter-specific data  (intptr_t)
  udata*: pointer            ## opaque user data identifier
```
