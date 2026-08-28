---
source_hash: fcacb532bbcaa46f
source_path: lib/posix/posix.nim
---

### socketpair

[ref: #symbol-socketpair]

**Input:**
- `a1: cint`
- `a2: cint`
- `a3: cint`
- `a4: var array[0 .. 1, cint]`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### st_atime

[ref: #symbol-st-atime]

**Input:**
- `s: Stat`

**Output:** `Time`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Second-granularity time of last access.

### st_ctime

[ref: #symbol-st-ctime]

**Input:**
- `s: Stat`

**Output:** `Time`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Second-granularity time of last status change.

### st_mtime

[ref: #symbol-st-mtime]

**Input:**
- `s: Stat`

**Output:** `Time`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Second-granularity time of last data modification.

### stat

[ref: #symbol-stat]

**Input:**
- `a1: cstring`
- `a2: var Stat`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### statvfs

[ref: #symbol-statvfs]

**Input:**
- `a1: cstring`
- `a2: var Statvfs`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/statvfs.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### strerror

[ref: #symbol-strerror]

**Input:**
- `errnum: cint`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<string.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### strfmon

[ref: #symbol-strfmon]

**Input:**
- `a1: cstring`
- `a2: int`
- `a3: cstring`

**Output:** `int`
**Pragmas:** `varargs`, `importc`, `header: "<monetary.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### strftime

[ref: #symbol-strftime]

**Input:**
- `a1: cstring`
- `a2: int`
- `a3: cstring`
- `a4: var Tm`

**Output:** `int`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### strptime

[ref: #symbol-strptime]

**Input:**
- `a1: cstring`
- `a2: cstring`
- `a3: var Tm`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### swab

[ref: #symbol-swab]

**Input:**
- `a1: pointer`
- `a2: pointer`
- `a3: int`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### swapcontext

[ref: #symbol-swapcontext]

**Input:**
- `a1: var Ucontext`
- `a2: var Ucontext`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<ucontext.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### symlink

[ref: #symbol-symlink]

**Input:**
- `a1: cstring`
- `a2: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sync

[ref: #symbol-sync]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sysconf

[ref: #symbol-sysconf]

**Input:**
- `a1: cint`

**Output:** `int`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tcgetpgrp

[ref: #symbol-tcgetpgrp]

**Input:**
- `a1: cint`

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tcsetpgrp

[ref: #symbol-tcsetpgrp]

**Input:**
- `a1: cint`
- `a2: Pid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### telldir

[ref: #symbol-telldir]

**Input:**
- `a1: ptr DIR`

**Output:** `int`
**Pragmas:** `importc`, `header: "<dirent.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### time

[ref: #symbol-time]

**Input:**
- `a1: var Time`

**Output:** `Time`
**Pragmas:** `importc`, `header: "<time.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### timegm

[ref: #symbol-timegm]

**Input:**
- `a1: var Tm`

**Output:** `Time`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### timer_create

[ref: #symbol-timer-create]

**Input:**
- `a1: ClockId`
- `a2: var SigEvent`
- `a3: var Timer`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### timer_delete

[ref: #symbol-timer-delete]

**Input:**
- `a1: Timer`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### timer_getoverrun

[ref: #symbol-timer-getoverrun]

**Input:**
- `a1: Timer`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### timer_gettime

[ref: #symbol-timer-gettime]

**Input:**
- `a1: Timer`
- `a2: var Itimerspec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### timer_settime

[ref: #symbol-timer-settime]

**Input:**
- `a1: Timer`
- `a2: cint`
- `a3: var Itimerspec`
- `a4: var Itimerspec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### truncate

[ref: #symbol-truncate]

**Input:**
- `a1: cstring`
- `a2: Off`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ttyname

[ref: #symbol-ttyname]

**Input:**
- `a1: cint`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ttyname_r

[ref: #symbol-ttyname-r]

**Input:**
- `a1: cint`
- `a2: cstring`
- `a3: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tzset

[ref: #symbol-tzset]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ualarm

[ref: #symbol-ualarm]

**Input:**
- `a1: Useconds`
- `a2: Useconds`

**Output:** `Useconds`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### umask

[ref: #symbol-umask]

**Input:**
- `a1: Mode`

**Output:** `Mode`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### uname

[ref: #symbol-uname]

**Input:**
- `a1: var Utsname`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/utsname.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### unlink

[ref: #symbol-unlink]

**Input:**
- `a1: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### usleep

[ref: #symbol-usleep]

**Input:**
- `a1: Useconds`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### utimes

[ref: #symbol-utimes]

Sets file access and modification times.

**Input:**
- `path: cstring`
- `times: ptr array[2, Timeval]`

**Output:** `int`
**Pragmas:** `importc: "utimes"`, `header: "<sys/time.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets file access and modification times.

Pass the filename and an array of times to set the access and modification times respectively. If you pass nil as the array both attributes will be set to the current time.

Returns zero on success.

For more information read <https://www.unix.com/man-page/posix/3/utimes/>.

### vfork

[ref: #symbol-vfork]

**Input:**
- *(none)*

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### wait

[ref: #symbol-wait]

**Input:**
- `a1: ptr cint`

**Output:** `Pid`
**Pragmas:** `importc`, `discardable`, `header: "<sys/wait.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### wait4

[ref: #symbol-wait4]

**Input:**
- `pid: Pid`
- `status: ptr cint`
- `options: cint`
- `rusage: ptr Rusage`

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<sys/wait.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### waitid

[ref: #symbol-waitid]

**Input:**
- `a1: cint`
- `a2: Id`
- `a3: var SigInfo`
- `a4: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/wait.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### waitpid

[ref: #symbol-waitpid]

**Input:**
- `a1: Pid`
- `a2: var cint`
- `a3: cint`

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<sys/wait.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### WEXITSTATUS

[ref: #symbol-wexitstatus]

**Input:**
- `s: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/wait.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Exit code, if WIFEXITED(s)

### WIFCONTINUED

[ref: #symbol-wifcontinued]

**Input:**
- `s: cint`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/wait.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

True if child has been continued.

### WIFEXITED

[ref: #symbol-wifexited]

**Input:**
- `s: cint`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/wait.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

True if child exited normally.

### WIFSIGNALED

[ref: #symbol-wifsignaled]

**Input:**
- `s: cint`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/wait.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

True if child exited due to uncaught signal.

### WIFSTOPPED

[ref: #symbol-wifstopped]

**Input:**
- `s: cint`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/wait.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

True if child is currently stopped.

### write

[ref: #symbol-write]

**Input:**
- `a1: cint`
- `a2: pointer`
- `a3: int`

**Output:** `int`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### writev

[ref: #symbol-writev]

**Input:**
- `a1: cint`
- `a2: ptr IOVec`
- `a3: cint`

**Output:** `int`
**Pragmas:** `importc`, `header: "<sys/uio.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### WSTOPSIG

[ref: #symbol-wstopsig]

**Input:**
- `s: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/wait.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Stop signal, if WIFSTOPPED(s)

### WTERMSIG

[ref: #symbol-wtermsig]

**Input:**
- `s: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/wait.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Termination signal, if WIFSIGNALED(s)

## Template

### onSignal

[ref: #symbol-onsignal]

Setup code to be executed when Unix signals are received. The currently handled signal is injected as sig into the calling scope.

**Input:**
- `signals: varargs[cint]`
- `body: untyped`

**Output:** *(none)*
Setup code to be executed when Unix signals are received. The currently handled signal is injected as sig into the calling scope.

Example:

```
from std/posix import SIGINT, SIGTERM, onSignal
onSignal(SIGINT, SIGTERM):
  echo "bye from signal ", sig
```

## Type

### AddrInfo

[ref: #symbol-addrinfo]

```nim
AddrInfo {.importc: "struct addrinfo", pure, final, header: "<netdb.h>".} = object
  ai_flags*: cint            ## Input flags.
  ai_family*: cint           ## Address family of socket.
  ai_socktype*: cint         ## Socket type.
  ai_protocol*: cint         ## Protocol of socket.
  ai_addrlen*: SockLen       ## Length of socket address.
  ai_addr*: ptr SockAddr     ## Socket address of socket.
  ai_canonname*: cstring     ## Canonical name of service location.
  ai_next*: ptr AddrInfo     ## Pointer to next in list.
```

struct addrinfo

### Blkcnt

[ref: #symbol-blkcnt]

```nim
Blkcnt {.importc: "blkcnt_t", header: "<sys/types.h>".} = int
```

used for file block counts

### Blksize

[ref: #symbol-blksize]

```nim
Blksize {.importc: "blksize_t", header: "<sys/types.h>".} = int32
```

used for block sizes

### Clock

[ref: #symbol-clock]

```nim
Clock {.importc: "clock_t", header: "<sys/types.h>".} = int
```

### ClockId

[ref: #symbol-clockid]

```nim
ClockId {.importc: "clockid_t", header: "<sys/types.h>".} = int
```

### Dev

[ref: #symbol-dev]

```nim
Dev {.importc: "dev_t", header: "<sys/types.h>".} = (when defined(freebsd):
  uint32
 else:
  int32)
```

### DIR

[ref: #symbol-dir]

```nim
DIR {.importc: "DIR", header: "<dirent.h>", incompleteStruct.} = object
```

A type representing a directory stream.

### Dirent

[ref: #symbol-dirent]

```nim
Dirent {.importc: "struct dirent", header: "<dirent.h>", final, pure.} = object
  when defined(haiku):
    d_dev*: Dev              ## Device (not POSIX)
    d_pdev*: Dev             ## Parent device (only for queries) (not POSIX)
  d_ino*: Ino                ## File serial number.
  when defined(dragonfly):
    d_type*: uint8
  elif defined(linux) or defined(macosx) or defined(freebsd) or defined(netbsd) or
      defined(openbsd) or
      defined(genode):
    d_reclen*: cshort        ## Length of this record. (not POSIX)
    d_type*: int8 ## Type of file; not supported by all filesystem types.
                  ## (not POSIX)
    when defined(linux) or defined(openbsd):
      d_off*: Off            ## Not an offset. Value that `telldir()` would return.
  elif defined(haiku):
    d_pino*: Ino             ## Parent inode (only for queries) (not POSIX)
    d_reclen*: cushort       ## Length of this record. (not POSIX)
  d_name*: array[0 .. 255, char] ## Name of entry.
```

dirent\_t struct

### Fsblkcnt

[ref: #symbol-fsblkcnt]

```nim
Fsblkcnt {.importc: "fsblkcnt_t", header: "<sys/types.h>".} = int
```

### Fsfilcnt

[ref: #symbol-fsfilcnt]

```nim
Fsfilcnt {.importc: "fsfilcnt_t", header: "<sys/types.h>".} = int
```

### FTW

[ref: #symbol-ftw]

```nim
FTW {.importc: "struct FTW", header: "<ftw.h>", final, pure.} = object
  base*: cint
  level*: cint
```

### Gid

[ref: #symbol-gid]

```nim
Gid {.importc: "gid_t", header: "<sys/types.h>".} = uint32
```

### Glob

[ref: #symbol-glob]

```nim
Glob {.importc: "glob_t", header: "<glob.h>", final, pure.} = object
  gl_pathc*: int             ## Count of paths matched by pattern.
  gl_pathv*: cstringArray    ## Pointer to a list of matched pathnames.
  gl_offs*: int              ## Slots to reserve at the beginning of gl_pathv.
```

glob\_t

### Group

[ref: #symbol-group]

```nim
Group {.importc: "struct group", header: "<grp.h>", final, pure.} = object
  gr_name*: cstring          ## The name of the group.
  gr_gid*: Gid               ## Numerical group ID.
  gr_mem*: cstringArray      ## Pointer to a null-terminated array of character
                             ## pointers to member names.
```

struct group

### Hostent

[ref: #symbol-hostent]

```nim
Hostent {.importc: "struct hostent", pure, final, header: "<netdb.h>".} = object
  h_name*: cstring           ## Official name of the host.
  h_aliases*: cstringArray   ## A pointer to an array of pointers to
                             ## alternative host names, terminated by a
                             ## null pointer.
  h_addrtype*: cint          ## Address type.
  h_length*: cint            ## The length, in bytes, of the address.
  h_addr_list*: cstringArray ## A pointer to an array of pointers to network
                             ## addresses (in network byte order) for the
                             ## host, terminated by a null pointer.
```

struct hostent

### Iconv

[ref: #symbol-iconv]

```nim
Iconv {.importc: "iconv_t", header: "<iconv.h>", final, pure.} = object
```

Identifies the conversion from one codeset to another.

### Id

[ref: #symbol-id]

```nim
Id {.importc: "id_t", header: "<sys/types.h>".} = int
```

### In6Addr

[ref: #symbol-in6addr]

```nim
In6Addr {.importc: "struct in6_addr", pure, final, header: "<netinet/in.h>".} = object
  s6_addr*: array[0 .. 15, char]
```

struct in6\_addr

### InAddr

[ref: #symbol-inaddr]

```nim
InAddr {.importc: "struct in_addr", pure, final, header: "<netinet/in.h>".} = object
  s_addr*: InAddrScalar
```

struct in\_addr

### InAddrScalar

[ref: #symbol-inaddrscalar]

```nim
InAddrScalar = uint32
```

### InAddrT

[ref: #symbol-inaddrt]

```nim
InAddrT {.importc: "in_addr_t", pure, final, header: "<netinet/in.h>".} = uint32
```

### Ino

[ref: #symbol-ino]

```nim
Ino {.importc: "ino_t", header: "<sys/types.h>".} = int
```

### InPort

[ref: #symbol-inport]

```nim
InPort = uint16
```

### IOVec

[ref: #symbol-iovec]

```nim
IOVec {.importc: "struct iovec", pure, final, header: "<sys/uio.h>".} = object
  iov_base*: pointer         ## Base address of a memory region for input or output.
  iov_len*: csize_t          ## The size of the memory pointed to by iov_base.
```

struct iovec

### Ipc_perm

[ref: #symbol-ipc-perm]

```nim
Ipc_perm {.importc: "struct ipc_perm", header: "<sys/ipc.h>", final, pure.} = object
  uid*: Uid                  ## Owner's user ID.
  gid*: Gid                  ## Owner's group ID.
  cuid*: Uid                 ## Creator's user ID.
  cgid*: Gid                 ## Creator's group ID.
  mode*: Mode                ## Read/write permission.
```

struct ipc\_perm

### Itimerspec

[ref: #symbol-itimerspec]

```nim
Itimerspec {.importc: "struct itimerspec", header: "<time.h>", final, pure.} = object
  it_interval*: Timespec     ## Timer period.
  it_value*: Timespec        ## Timer expiration.
```

struct itimerspec

### Key

[ref: #symbol-key]

```nim
Key {.importc: "key_t", header: "<sys/types.h>".} = int
```


[Prev](posix_6.md) | [Next](posix_8.md)
