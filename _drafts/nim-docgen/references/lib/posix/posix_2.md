---
source_hash: fcacb532bbcaa46f
source_path: lib/posix/posix.nim
---

### execve

[ref: #symbol-execve]

**Input:**
- `a1: cstring`
- `a2: cstringArray`
- `a3: cstringArray`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### execvp

[ref: #symbol-execvp]

**Input:**
- `a1: cstring`
- `a2: cstringArray`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### execvpe

[ref: #symbol-execvpe]

**Input:**
- `a1: cstring`
- `a2: cstringArray`
- `a3: cstringArray`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### exitnow

[ref: #symbol-exitnow]

**Input:**
- `code: cint`

**Output:** *(none)*
**Pragmas:** `importc: "_exit"`, `header: "<unistd.h>"`, `noreturn`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fchdir

[ref: #symbol-fchdir]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fchmod

[ref: #symbol-fchmod]

**Input:**
- `a1: cint`
- `a2: Mode`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fchown

[ref: #symbol-fchown]

**Input:**
- `a1: cint`
- `a2: Uid`
- `a3: Gid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fcntl

[ref: #symbol-fcntl]

**Input:**
- `a1: cint | SocketHandle`
- `a2: cint`

**Output:** `cint`
**Generic parameters:** `a1:type`

**Pragmas:** `varargs`, `importc`, `header: "<fcntl.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### FD_CLR

[ref: #symbol-fd-clr]

**Input:**
- `a1: cint`
- `a2: var TFdSet`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<sys/select.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### FD_ISSET

[ref: #symbol-fd-isset]

**Input:**
- `a1: cint | SocketHandle`
- `a2: var TFdSet`

**Output:** `cint`
**Generic parameters:** `a1:type`

**Pragmas:** `importc`, `header: "<sys/select.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### FD_SET

[ref: #symbol-fd-set]

**Input:**
- `a1: cint | SocketHandle`
- `a2: var TFdSet`

**Output:** *(none)*
**Generic parameters:** `a1:type`

**Pragmas:** `importc: "FD_SET"`, `header: "<sys/select.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### FD_ZERO

[ref: #symbol-fd-zero]

**Input:**
- `a1: var TFdSet`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<sys/select.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fdatasync

[ref: #symbol-fdatasync]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fmtmsg

[ref: #symbol-fmtmsg]

**Input:**
- `a1: int`
- `a2: cstring`
- `a3: cint`
- `a4: cstring`
- `a5: cstring`
- `a6: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fmtmsg.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fnmatch

[ref: #symbol-fnmatch]

**Input:**
- `a1: cstring`
- `a2: cstring`
- `a3: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fnmatch.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fork

[ref: #symbol-fork]

**Input:**
- *(none)*

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fpathconf

[ref: #symbol-fpathconf]

**Input:**
- `a1: cint`
- `a2: cint`

**Output:** `int`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### freeAddrInfo

[ref: #symbol-freeaddrinfo]

**Input:**
- `a1: ptr AddrInfo`

**Output:** *(none)*
**Pragmas:** `importc: "freeaddrinfo"`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fstat

[ref: #symbol-fstat]

**Input:**
- `a1: cint`
- `a2: var Stat`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fstatvfs

[ref: #symbol-fstatvfs]

**Input:**
- `a1: cint`
- `a2: var Statvfs`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/statvfs.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### fsync

[ref: #symbol-fsync]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

synchronize a file's buffer cache to the storage device

### ftok

[ref: #symbol-ftok]

**Input:**
- `a1: cstring`
- `a2: cint`

**Output:** `Key`
**Pragmas:** `importc`, `header: "<sys/ipc.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ftruncate

[ref: #symbol-ftruncate]

**Input:**
- `a1: cint`
- `a2: Off`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ftw

[ref: #symbol-ftw]

**Input:**
- `a1: cstring`
- `a2: proc (x1: cstring; x2: ptr Stat; x3: cint): cint {.noconv.}`
- `a3: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<ftw.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gai_strerror

[ref: #symbol-gai-strerror]

**Input:**
- `a1: cint`

**Output:** `cstring`
**Pragmas:** `importc: "(char *)$1"`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getaddrinfo

[ref: #symbol-getaddrinfo]

**Input:**
- `a1: cstring`
- `a2: cstring`
- `a3: ptr AddrInfo`
- `a4: var ptr AddrInfo`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getcontext

[ref: #symbol-getcontext]

**Input:**
- `a1: var Ucontext`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<ucontext.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getcwd

[ref: #symbol-getcwd]

**Input:**
- `a1: cstring`
- `a2: int`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getdate

[ref: #symbol-getdate]

**Input:**
- `a1: cstring`

**Output:** `ptr Tm`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getegid

[ref: #symbol-getegid]

**Input:**
- *(none)*

**Output:** `Gid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the effective group ID of the calling process

### geteuid

[ref: #symbol-geteuid]

**Input:**
- *(none)*

**Output:** `Uid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the effective user ID of the calling process

### getgid

[ref: #symbol-getgid]

**Input:**
- *(none)*

**Output:** `Gid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the real group ID of the calling process

### getgrent

[ref: #symbol-getgrent]

**Input:**
- *(none)*

**Output:** `ptr Group`
**Pragmas:** `importc`, `header: "<grp.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getgrgid

[ref: #symbol-getgrgid]

**Input:**
- `a1: Gid`

**Output:** `ptr Group`
**Pragmas:** `importc`, `header: "<grp.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getgrgid_r

[ref: #symbol-getgrgid-r]

**Input:**
- `a1: Gid`
- `a2: ptr Group`
- `a3: cstring`
- `a4: int`
- `a5: ptr ptr Group`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<grp.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getgrnam

[ref: #symbol-getgrnam]

**Input:**
- `a1: cstring`

**Output:** `ptr Group`
**Pragmas:** `importc`, `header: "<grp.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getgrnam_r

[ref: #symbol-getgrnam-r]

**Input:**
- `a1: cstring`
- `a2: ptr Group`
- `a3: cstring`
- `a4: int`
- `a5: ptr ptr Group`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<grp.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getgroups

[ref: #symbol-getgroups]

**Input:**
- `a1: cint`
- `a2: ptr array[0 .. 255, Gid]`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gethostbyaddr

[ref: #symbol-gethostbyaddr]

**Input:**
- `a1: pointer`
- `a2: SockLen`
- `a3: cint`

**Output:** `ptr Hostent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gethostbyname

[ref: #symbol-gethostbyname]

**Input:**
- `a1: cstring`

**Output:** `ptr Hostent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gethostent

[ref: #symbol-gethostent]

**Input:**
- *(none)*

**Output:** `ptr Hostent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gethostid

[ref: #symbol-gethostid]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gethostname

[ref: #symbol-gethostname]

**Input:**
- `a1: cstring`
- `a2: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getlogin

[ref: #symbol-getlogin]

**Input:**
- *(none)*

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getlogin_r

[ref: #symbol-getlogin-r]

**Input:**
- `a1: cstring`
- `a2: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getnameinfo

[ref: #symbol-getnameinfo]

**Input:**
- `a1: ptr SockAddr`
- `a2: SockLen`
- `a3: cstring`
- `a4: SockLen`
- `a5: cstring`
- `a6: SockLen`
- `a7: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getnetbyaddr

[ref: #symbol-getnetbyaddr]

**Input:**
- `a1: int32`
- `a2: cint`

**Output:** `ptr Tnetent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getnetbyname

[ref: #symbol-getnetbyname]

**Input:**
- `a1: cstring`

**Output:** `ptr Tnetent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getnetent

[ref: #symbol-getnetent]

**Input:**
- *(none)*

**Output:** `ptr Tnetent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getopt

[ref: #symbol-getopt]

**Input:**
- `a1: cint`
- `a2: cstringArray`
- `a3: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getpeername

[ref: #symbol-getpeername]

**Input:**
- `a1: SocketHandle`
- `a2: ptr SockAddr`
- `a3: ptr SockLen`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getpgid

[ref: #symbol-getpgid]

**Input:**
- `a1: Pid`

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getpgrp

[ref: #symbol-getpgrp]

**Input:**
- *(none)*

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getpid

[ref: #symbol-getpid]

**Input:**
- *(none)*

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the process ID (PID) of the calling process

### getppid

[ref: #symbol-getppid]

**Input:**
- *(none)*

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the process ID of the parent of the calling process

### getprotobyname

[ref: #symbol-getprotobyname]

**Input:**
- `a1: cstring`

**Output:** `ptr Protoent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getprotobynumber

[ref: #symbol-getprotobynumber]

**Input:**
- `a1: cint`

**Output:** `ptr Protoent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getprotoent

[ref: #symbol-getprotoent]

**Input:**
- *(none)*

**Output:** `ptr Protoent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getpwent

[ref: #symbol-getpwent]

**Input:**
- *(none)*

**Output:** `ptr Passwd`
**Pragmas:** `importc`, `header: "<pwd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getpwnam

[ref: #symbol-getpwnam]

**Input:**
- `a1: cstring`

**Output:** `ptr Passwd`
**Pragmas:** `importc`, `header: "<pwd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getpwnam_r

[ref: #symbol-getpwnam-r]

**Input:**
- `a1: cstring`
- `a2: ptr Passwd`
- `a3: cstring`
- `a4: int`
- `a5: ptr ptr Passwd`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pwd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getpwuid

[ref: #symbol-getpwuid]

**Input:**
- `a1: Uid`

**Output:** `ptr Passwd`
**Pragmas:** `importc`, `header: "<pwd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getpwuid_r

[ref: #symbol-getpwuid-r]

**Input:**
- `a1: Uid`
- `a2: ptr Passwd`
- `a3: cstring`
- `a4: int`
- `a5: ptr ptr Passwd`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pwd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getrlimit

[ref: #symbol-getrlimit]

**Input:**
- `resource: cint`
- `rlp: var RLimit`

**Output:** `cint`
**Pragmas:** `importc: "getrlimit"`, `header: "<sys/resource.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The getrlimit() system call gets resource limits.

### getrusage

[ref: #symbol-getrusage]

**Input:**
- `who: cint`
- `rusage: ptr Rusage`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/resource.h>"`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getservbyname

[ref: #symbol-getservbyname]

**Input:**
- `a1: cstring`
- `a2: cstring`

**Output:** `ptr Servent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getservbyport

[ref: #symbol-getservbyport]

**Input:**
- `a1: cint`
- `a2: cstring`

**Output:** `ptr Servent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getservent

[ref: #symbol-getservent]

**Input:**
- *(none)*

**Output:** `ptr Servent`
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getsid

[ref: #symbol-getsid]

**Input:**
- `a1: Pid`

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the session ID of the calling process

### getsockname

[ref: #symbol-getsockname]

**Input:**
- `a1: SocketHandle`
- `a2: ptr SockAddr`
- `a3: ptr SockLen`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getsockopt

[ref: #symbol-getsockopt]

**Input:**
- `a1: SocketHandle`
- `a2: cint`
- `a3: cint`
- `a4: pointer`
- `a5: ptr SockLen`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getuid

[ref: #symbol-getuid]

**Input:**
- *(none)*

**Output:** `Uid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the real user ID of the calling process

### getwd

[ref: #symbol-getwd]

**Input:**
- `a1: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### glob

[ref: #symbol-glob]

**Input:**
- `a1: cstring`
- `a2: cint`
- `a3: proc (x1: cstring; x2: cint): cint {.noconv.}`
- `a4: ptr Glob`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<glob.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Filename globbing. Use [os.walkPattern()](os.html#glob_1) and similar.


[Prev](posix_1.md) | [Next](posix_3.md)
