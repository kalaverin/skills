---
source_hash: fcacb532bbcaa46f
source_path: lib/posix/posix.nim
---

# posix

[ref: #module-posix]

This is a raw POSIX interface module. It does not not provide any convenience: cstrings are used instead of proper Nim strings and return codes indicate errors. If you want exceptions and a proper Nim-like interface, use the OS module or write a wrapper.

For high-level wrappers specialized for Linux and BSDs see: [posix\_utils](posix_utils.html)

Coding conventions: ALL types are named the same as in the POSIX standard except that they start with 'T' or 'P' (if they are pointers) and without the '\_t' suffix to be consistent with Nim conventions. If an identifier is a Nim keyword the `identifier` notation is used.

This library relies on the header files of your C compiler. The resulting C code will just #include <XYZ.h> and *not* define the symbols declared here.

## Examples

```nim
from std/posix import SIGINT, SIGTERM, onSignal
onSignal(SIGINT, SIGTERM):
  echo "bye from signal ", sig
```

## Const

### DT_BLK

[ref: #symbol-dt-blk]

```nim
DT_BLK = 6
```

Block device.

### DT_CHR

[ref: #symbol-dt-chr]

```nim
DT_CHR = 2
```

Character device.

### DT_DIR

[ref: #symbol-dt-dir]

```nim
DT_DIR = 4
```

Directory.

### DT_FIFO

[ref: #symbol-dt-fifo]

```nim
DT_FIFO = 1
```

Named pipe, or FIFO.

### DT_LNK

[ref: #symbol-dt-lnk]

```nim
DT_LNK = 10
```

Symbolic link.

### DT_REG

[ref: #symbol-dt-reg]

```nim
DT_REG = 8
```

Regular file.

### DT_SOCK

[ref: #symbol-dt-sock]

```nim
DT_SOCK = 12
```

UNIX domain socket.

### DT_UNKNOWN

[ref: #symbol-dt-unknown]

```nim
DT_UNKNOWN = 0
```

Unknown file type.

### DT_WHT

[ref: #symbol-dt-wht]

```nim
DT_WHT = 14
```

### INVALID_SOCKET

[ref: #symbol-invalid-socket]

```nim
INVALID_SOCKET = -1'i32
```

### MM_NULLACT

[ref: #symbol-mm-nullact]

```nim
MM_NULLACT = nil
```

### MM_NULLLBL

[ref: #symbol-mm-nulllbl]

```nim
MM_NULLLBL = nil
```

### MM_NULLMC

[ref: #symbol-mm-nullmc]

```nim
MM_NULLMC = 0
```

### MM_NULLSEV

[ref: #symbol-mm-nullsev]

```nim
MM_NULLSEV = 0
```

### MM_NULLTAG

[ref: #symbol-mm-nulltag]

```nim
MM_NULLTAG = nil
```

### MM_NULLTXT

[ref: #symbol-mm-nulltxt]

```nim
MM_NULLTXT = nil
```

### MSG_NOSIGNAL

[ref: #symbol-msg-nosignal]

```nim
MSG_NOSIGNAL = 0'i32
```

### POSIX_SPAWN_USEVFORK

[ref: #symbol-posix-spawn-usevfork]

```nim
POSIX_SPAWN_USEVFORK = 0'i32
```

### RUSAGE_CHILDREN

[ref: #symbol-rusage-children]

```nim
RUSAGE_CHILDREN = -1'i32
```

### RUSAGE_SELF

[ref: #symbol-rusage-self]

```nim
RUSAGE_SELF = 0'i32
```

### RUSAGE_THREAD

[ref: #symbol-rusage-thread]

```nim
RUSAGE_THREAD = 1'i32
```

### SO_REUSEPORT

[ref: #symbol-so-reuseport]

```nim
SO_REUSEPORT = 512'i32
```

Multiple binding: load balancing on incoming TCP connections or UDP packets. (Requires Linux kernel > 3.9)

### Sockaddr_un_path_length

[ref: #symbol-sockaddr-un-path-length]

```nim
Sockaddr_un_path_length = 92
```

### StatHasNanoseconds

[ref: #symbol-stathasnanoseconds]

```nim
StatHasNanoseconds = true
```

Boolean flag that indicates if the system supports nanosecond time resolution in the fields of Stat. Note that the nanosecond based fields (Stat.st\_atim, Stat.st\_mtim and Stat.st\_ctim) can be accessed without checking this flag, because this module defines fallback procs when they are not available.

### STDERR_FILENO

[ref: #symbol-stderr-fileno]

```nim
STDERR_FILENO = 2
```

File number of stderr;

### STDIN_FILENO

[ref: #symbol-stdin-fileno]

```nim
STDIN_FILENO = 0
```

File number of stdin;

### STDOUT_FILENO

[ref: #symbol-stdout-fileno]

```nim
STDOUT_FILENO = 1
```

File number of stdout;

## Proc

### `-`

[ref: #symbol-]

**Input:**
- `a: Time`
- `b: Time`

**Output:** `Time`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `a: Time`
- `b: Time`

**Output:** `bool`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: SocketHandle`
- `y: SocketHandle`

**Output:** `bool`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `raise`

[ref: #symbol-raise]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### accept

[ref: #symbol-accept]

**Input:**
- `a1: SocketHandle`
- `a2: ptr SockAddr`
- `a3: ptr SockLen`

**Output:** `SocketHandle`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### access

[ref: #symbol-access]

**Input:**
- `a1: cstring`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### alarm

[ref: #symbol-alarm]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### asctime

[ref: #symbol-asctime]

**Input:**
- `a1: var Tm`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### asctime_r

[ref: #symbol-asctime-r]

**Input:**
- `a1: var Tm`
- `a2: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### basename

[ref: #symbol-basename]

**Input:**
- `a1: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<libgen.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### bindSocket

[ref: #symbol-bindsocket]

**Input:**
- `a1: SocketHandle`
- `a2: ptr SockAddr`
- `a3: SockLen`

**Output:** `cint`
**Pragmas:** `importc: "bind"`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

is Posix's bind, because bind is a reserved word

### catclose

[ref: #symbol-catclose]

**Input:**
- `a1: Nl_catd`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<nl_types.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### catgets

[ref: #symbol-catgets]

**Input:**
- `a1: Nl_catd`
- `a2: cint`
- `a3: cint`
- `a4: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<nl_types.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### catopen

[ref: #symbol-catopen]

**Input:**
- `a1: cstring`
- `a2: cint`

**Output:** `Nl_catd`
**Pragmas:** `importc`, `header: "<nl_types.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### chdir

[ref: #symbol-chdir]

**Input:**
- `a1: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### chmod

[ref: #symbol-chmod]

**Input:**
- `a1: cstring`
- `a2: Mode`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### chown

[ref: #symbol-chown]

**Input:**
- `a1: cstring`
- `a2: Uid`
- `a3: Gid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clock

[ref: #symbol-clock]

**Input:**
- *(none)*

**Output:** `Clock`
**Pragmas:** `importc`, `header: "<time.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clock_getcpuclockid

[ref: #symbol-clock-getcpuclockid]

**Input:**
- `a1: Pid`
- `a2: var ClockId`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clock_getres

[ref: #symbol-clock-getres]

**Input:**
- `a1: ClockId`
- `a2: var Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clock_gettime

[ref: #symbol-clock-gettime]

**Input:**
- `a1: ClockId`
- `a2: var Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clock_nanosleep

[ref: #symbol-clock-nanosleep]

**Input:**
- `a1: ClockId`
- `a2: cint`
- `a3: var Timespec`
- `a4: var Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clock_settime

[ref: #symbol-clock-settime]

**Input:**
- `a1: ClockId`
- `a2: var Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### close

[ref: #symbol-close]

**Input:**
- `a1: cint | SocketHandle`

**Output:** `cint`
**Generic parameters:** `a1:type`

**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### closedir

[ref: #symbol-closedir]

**Input:**
- `a1: ptr DIR`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<dirent.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### CMSG_DATA

[ref: #symbol-cmsg-data]

**Input:**
- `cmsg: ptr Tcmsghdr`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### CMSG_FIRSTHDR

[ref: #symbol-cmsg-firsthdr]

**Input:**
- `mhdr: ptr Tmsghdr`

**Output:** `ptr Tcmsghdr`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### CMSG_LEN

[ref: #symbol-cmsg-len]

**Input:**
- `len: csize_t`

**Output:** `csize_t`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### CMSG_NXTHDR

[ref: #symbol-cmsg-nxthdr]

**Input:**
- `mhdr: ptr Tmsghdr`
- `cmsg: ptr Tcmsghdr`

**Output:** `ptr Tcmsghdr`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### CMSG_SPACE

[ref: #symbol-cmsg-space]

**Input:**
- `len: csize_t`

**Output:** `csize_t`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### confstr

[ref: #symbol-confstr]

**Input:**
- `a1: cint`
- `a2: cstring`
- `a3: int`

**Output:** `int`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### connect

[ref: #symbol-connect]

**Input:**
- `a1: SocketHandle`
- `a2: ptr SockAddr`
- `a3: SockLen`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### creat

[ref: #symbol-creat]

**Input:**
- `a1: cstring`
- `a2: Mode`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fcntl.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### crypt

[ref: #symbol-crypt]

**Input:**
- `a1: cstring`
- `a2: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ctermid

[ref: #symbol-ctermid]

**Input:**
- `a1: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ctime

[ref: #symbol-ctime]

**Input:**
- `a1: var Time`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ctime_r

[ref: #symbol-ctime-r]

**Input:**
- `a1: var Time`
- `a2: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### difftime

[ref: #symbol-difftime]

**Input:**
- `a1: Time`
- `a2: Time`

**Output:** `cdouble`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dirname

[ref: #symbol-dirname]

**Input:**
- `a1: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<libgen.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dlclose

[ref: #symbol-dlclose]

**Input:**
- `a1: pointer`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<dlfcn.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dlerror

[ref: #symbol-dlerror]

**Input:**
- *(none)*

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<dlfcn.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dlopen

[ref: #symbol-dlopen]

**Input:**
- `a1: cstring`
- `a2: cint`

**Output:** `pointer`
**Pragmas:** `importc`, `header: "<dlfcn.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dlsym

[ref: #symbol-dlsym]

**Input:**
- `a1: pointer`
- `a2: cstring`

**Output:** `pointer`
**Pragmas:** `importc`, `header: "<dlfcn.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dup

[ref: #symbol-dup]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dup2

[ref: #symbol-dup2]

**Input:**
- `a1: cint`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### encrypt

[ref: #symbol-encrypt]

**Input:**
- `a1: array[0 .. 63, char]`
- `a2: cint`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### endgrent

[ref: #symbol-endgrent]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<grp.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### endhostent

[ref: #symbol-endhostent]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### endnetent

[ref: #symbol-endnetent]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### endprotoent

[ref: #symbol-endprotoent]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### endpwent

[ref: #symbol-endpwent]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<pwd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### endservent

[ref: #symbol-endservent]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### execl

[ref: #symbol-execl]

**Input:**
- `a1: cstring`
- `a2: cstring`

**Output:** `cint`
**Pragmas:** `varargs`, `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### execle

[ref: #symbol-execle]

**Input:**
- `a1: cstring`
- `a2: cstring`

**Output:** `cint`
**Pragmas:** `varargs`, `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### execlp

[ref: #symbol-execlp]

**Input:**
- `a1: cstring`
- `a2: cstring`

**Output:** `cint`
**Pragmas:** `varargs`, `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### execv

[ref: #symbol-execv]

**Input:**
- `a1: cstring`
- `a2: cstringArray`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Next](posix_2.md)
