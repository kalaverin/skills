---
source_hash: c4fd142d959e46bc
source_path: lib/posix/inotify.nim
---

# inotify

[ref: #module-inotify]

## Examples

```nim
import std/inotify
when defined(linux):
  let inotifyFd = inotify_init()  # create and get new inotify FileHandle
  doAssert inotifyFd >= 0         # check for errors

  let wd = inotifyFd.inotify_add_watch("/tmp", IN_CREATE or IN_DELETE)  # Add new watch
  doAssert wd >= 0                 # check for errors

  discard inotifyFd.inotify_rm_watch(wd) # remove watch
```

```nim
when defined(linux):
   import std/posix  # needed for FileHandle read procedure
   const MaxWatches = 8192

   let inotifyFd = inotify_init()  # create new inotify instance and get it's FileHandle
   let wd = inotifyFd.inotify_add_watch("/tmp", IN_CREATE or IN_DELETE)  # Add new watch

   var events: array[MaxWatches, byte]  # event buffer
   while (let n = read(inotifyFd, addr events, MaxWatches); n) > 0:  # blocks until any events have been read
     for e in inotify_events(addr events, n):
       echo (e[].wd, e[].mask, cast[cstring](addr e[].name))    # echo watch id, mask, and name value of each event
```

## Const

### IN_ACCESS

[ref: #symbol-in-access]

```nim
IN_ACCESS = 0x00000001
```

File was accessed.

### IN_ALL_EVENTS

[ref: #symbol-in-all-events]

```nim
IN_ALL_EVENTS = 4095
```

### IN_ATTRIB

[ref: #symbol-in-attrib]

```nim
IN_ATTRIB = 0x00000004
```

Metadata changed.

### IN_CLOSE

[ref: #symbol-in-close]

```nim
IN_CLOSE = 24
```

Close.

### IN_CLOSE_NOWRITE

[ref: #symbol-in-close-nowrite]

```nim
IN_CLOSE_NOWRITE = 0x00000010
```

Unwrittable file closed.

### IN_CLOSE_WRITE

[ref: #symbol-in-close-write]

```nim
IN_CLOSE_WRITE = 0x00000008
```

Writtable file was closed.

### IN_CREATE

[ref: #symbol-in-create]

```nim
IN_CREATE = 0x00000100
```

Subfile was created.

### IN_DELETE

[ref: #symbol-in-delete]

```nim
IN_DELETE = 0x00000200
```

Subfile was deleted.

### IN_DELETE_SELF

[ref: #symbol-in-delete-self]

```nim
IN_DELETE_SELF = 0x00000400
```

Self was deleted.

### IN_DONT_FOLLOW

[ref: #symbol-in-dont-follow]

```nim
IN_DONT_FOLLOW = 0x02000000
```

Do not follow a sym link.

### IN_EXCL_UNLINK

[ref: #symbol-in-excl-unlink]

```nim
IN_EXCL_UNLINK = 0x04000000
```

Exclude events on unlinked objects.

### IN_IGNORED

[ref: #symbol-in-ignored]

```nim
IN_IGNORED = 0x00008000
```

File was ignored.

### IN_ISDIR

[ref: #symbol-in-isdir]

```nim
IN_ISDIR = 0x40000000
```

Event occurred against dir.

### IN_MASK_ADD

[ref: #symbol-in-mask-add]

```nim
IN_MASK_ADD = 0x20000000
```

Add to the mask of an already existing watch.

### IN_MODIFY

[ref: #symbol-in-modify]

```nim
IN_MODIFY = 0x00000002
```

File was modified.

### IN_MOVE

[ref: #symbol-in-move]

```nim
IN_MOVE = 192
```

Moves.

### IN_MOVE_SELF

[ref: #symbol-in-move-self]

```nim
IN_MOVE_SELF = 0x00000800
```

Self was moved.

### IN_MOVED_FROM

[ref: #symbol-in-moved-from]

```nim
IN_MOVED_FROM = 0x00000040
```

File was moved from X.

### IN_MOVED_TO

[ref: #symbol-in-moved-to]

```nim
IN_MOVED_TO = 0x00000080
```

File was moved to Y.

### IN_ONESHOT

[ref: #symbol-in-oneshot]

```nim
IN_ONESHOT = 0x0000000080000000'i64
```

Only send event once.

### IN_ONLYDIR

[ref: #symbol-in-onlydir]

```nim
IN_ONLYDIR = 0x01000000
```

Only watch the path if it is a directory.

### IN_OPEN

[ref: #symbol-in-open]

```nim
IN_OPEN = 0x00000020
```

File was opened.

### IN_Q_OVERFLOW

[ref: #symbol-in-q-overflow]

```nim
IN_Q_OVERFLOW = 0x00004000
```

Event queued overflowed.

### IN_UNMOUNT

[ref: #symbol-in-unmount]

```nim
IN_UNMOUNT = 0x00002000
```

Backing fs was unmounted.

## Iterator

### inotify_events

[ref: #symbol-inotify-events]

**Input:**
- `evs: pointer`
- `n: int`

**Output:** `ptr InotifyEvent`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Abstract the packed buffer interface to yield event object pointers.

## Proc

### inotify_add_watch

[ref: #symbol-inotify-add-watch]

**Input:**
- `fd: cint`
- `name: cstring`
- `mask: uint32`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "inotify_add_watch"`, `header: "<sys/inotify.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Add watch of object NAME to inotify instance FD. Notify about events specified by MASK.

### inotify_init

[ref: #symbol-inotify-init]

**Input:**
- *(none)*

**Output:** `FileHandle`
**Pragmas:** `cdecl`, `importc: "inotify_init"`, `header: "<sys/inotify.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create and initialize inotify instance.

### inotify_init1

[ref: #symbol-inotify-init1]

**Input:**
- `flags: cint`

**Output:** `FileHandle`
**Pragmas:** `cdecl`, `importc: "inotify_init1"`, `header: "<sys/inotify.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Like [inotify\_init](#inotify_init) , but has a flags argument that provides access to some extra functionality.

### inotify_rm_watch

[ref: #symbol-inotify-rm-watch]

**Input:**
- `fd: cint`
- `wd: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `importc: "inotify_rm_watch"`, `header: "<sys/inotify.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Remove the watch specified by WD from the inotify instance FD.

## Type

### InotifyEvent

[ref: #symbol-inotifyevent]

```nim
InotifyEvent {.pure, final, importc: "struct inotify_event",
               header: "<sys/inotify.h>", completeStruct.} = object
  wd* {.importc: "wd".}: FileHandle ## Watch descriptor.
  mask* {.importc: "mask".}: uint32 ## Watch mask.
  cookie* {.importc: "cookie".}: uint32 ## Cookie to synchronize two events.
  len* {.importc: "len".}: uint32 ## Length (including NULs) of name.
  name* {.importc: "name".}: UncheckedArray[char] ## Name.
```

An Inotify event.
