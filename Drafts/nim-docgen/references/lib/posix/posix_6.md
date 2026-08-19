---
source_hash: fcacb532bbcaa46f
source_path: lib/posix/posix.nim
---

### S_ISREG

[ref: #symbol-s-isreg]

**Input:**
- `m: Mode`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test for a regular file.

### S_ISSOCK

[ref: #symbol-s-issock]

**Input:**
- `m: Mode`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test for a socket.

### S_TYPEISMQ

[ref: #symbol-s-typeismq]

**Input:**
- `buf: var Stat`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test for a message queue.

### S_TYPEISSEM

[ref: #symbol-s-typeissem]

**Input:**
- `buf: var Stat`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test for a semaphore.

### S_TYPEISSHM

[ref: #symbol-s-typeisshm]

**Input:**
- `buf: var Stat`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test for a shared memory object.

### S_TYPEISTMO

[ref: #symbol-s-typeistmo]

**Input:**
- `buf: var Stat`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test macro for a typed memory object.

### sched_get_priority_max

[ref: #symbol-sched-get-priority-max]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sched_get_priority_min

[ref: #symbol-sched-get-priority-min]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sched_getparam

[ref: #symbol-sched-getparam]

**Input:**
- `a1: Pid`
- `a2: var Sched_param`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sched_getscheduler

[ref: #symbol-sched-getscheduler]

**Input:**
- `a1: Pid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sched_rr_get_interval

[ref: #symbol-sched-rr-get-interval]

**Input:**
- `a1: Pid`
- `a2: var Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sched_setparam

[ref: #symbol-sched-setparam]

**Input:**
- `a1: Pid`
- `a2: var Sched_param`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sched_setscheduler

[ref: #symbol-sched-setscheduler]

**Input:**
- `a1: Pid`
- `a2: cint`
- `a3: var Sched_param`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sched_yield

[ref: #symbol-sched-yield]

**Input:**
- *(none)*

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### seekdir

[ref: #symbol-seekdir]

**Input:**
- `a1: ptr DIR`
- `a2: int`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<dirent.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### select

[ref: #symbol-select]

**Input:**
- `a1: cint | SocketHandle`
- `a2: ptr TFdSet`
- `a3: ptr TFdSet`
- `a4: ptr TFdSet`
- `a5: ptr Timeval`

**Output:** `cint`
**Generic parameters:** `a1:type`

**Pragmas:** `importc`, `header: "<sys/select.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sem_close

[ref: #symbol-sem-close]

**Input:**
- `a1: ptr Sem`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<semaphore.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sem_destroy

[ref: #symbol-sem-destroy]

**Input:**
- `a1: ptr Sem`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<semaphore.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sem_getvalue

[ref: #symbol-sem-getvalue]

**Input:**
- `a1: ptr Sem`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<semaphore.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sem_init

[ref: #symbol-sem-init]

**Input:**
- `a1: ptr Sem`
- `a2: cint`
- `a3: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<semaphore.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sem_open

[ref: #symbol-sem-open]

**Input:**
- `a1: cstring`
- `a2: cint`

**Output:** `ptr Sem`
**Pragmas:** `varargs`, `importc`, `header: "<semaphore.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sem_post

[ref: #symbol-sem-post]

**Input:**
- `a1: ptr Sem`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<semaphore.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sem_timedwait

[ref: #symbol-sem-timedwait]

**Input:**
- `a1: ptr Sem`
- `a2: ptr Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<semaphore.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sem_trywait

[ref: #symbol-sem-trywait]

**Input:**
- `a1: ptr Sem`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<semaphore.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sem_unlink

[ref: #symbol-sem-unlink]

**Input:**
- `a1: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<semaphore.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sem_wait

[ref: #symbol-sem-wait]

**Input:**
- `a1: ptr Sem`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<semaphore.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### send

[ref: #symbol-send]

**Input:**
- `a1: SocketHandle`
- `a2: pointer`
- `a3: int`
- `a4: cint`

**Output:** `int`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sendmsg

[ref: #symbol-sendmsg]

**Input:**
- `a1: SocketHandle`
- `a2: ptr Tmsghdr`
- `a3: cint`

**Output:** `int`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sendto

[ref: #symbol-sendto]

**Input:**
- `a1: SocketHandle`
- `a2: pointer`
- `a3: int`
- `a4: cint`
- `a5: ptr SockAddr`
- `a6: SockLen`

**Output:** `int`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setcontext

[ref: #symbol-setcontext]

**Input:**
- `a1: var Ucontext`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<ucontext.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setegid

[ref: #symbol-setegid]

**Input:**
- `a1: Gid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### seteuid

[ref: #symbol-seteuid]

**Input:**
- `a1: Uid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setgid

[ref: #symbol-setgid]

**Input:**
- `a1: Gid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setgrent

[ref: #symbol-setgrent]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<grp.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sethostent

[ref: #symbol-sethostent]

**Input:**
- `a1: cint`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setlocale

[ref: #symbol-setlocale]

**Input:**
- `a1: cint`
- `a2: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<locale.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setnetent

[ref: #symbol-setnetent]

**Input:**
- `a1: cint`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setpgid

[ref: #symbol-setpgid]

**Input:**
- `a1: Pid`
- `a2: Pid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setpgrp

[ref: #symbol-setpgrp]

**Input:**
- *(none)*

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setprotoent

[ref: #symbol-setprotoent]

**Input:**
- `a1: cint`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setpwent

[ref: #symbol-setpwent]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<pwd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setregid

[ref: #symbol-setregid]

**Input:**
- `a1: Gid`
- `a2: Gid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setreuid

[ref: #symbol-setreuid]

**Input:**
- `a1: Uid`
- `a2: Uid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setrlimit

[ref: #symbol-setrlimit]

**Input:**
- `resource: cint`
- `rlp: var RLimit`

**Output:** `cint`
**Pragmas:** `importc: "setrlimit"`, `header: "<sys/resource.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The setrlimit() system calls sets resource limits.

### setservent

[ref: #symbol-setservent]

**Input:**
- `a1: cint`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setsid

[ref: #symbol-setsid]

**Input:**
- *(none)*

**Output:** `Pid`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setsockopt

[ref: #symbol-setsockopt]

**Input:**
- `a1: SocketHandle`
- `a2: cint`
- `a3: cint`
- `a4: pointer`
- `a5: SockLen`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setuid

[ref: #symbol-setuid]

**Input:**
- `a1: Uid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### shm_open

[ref: #symbol-shm-open]

**Input:**
- `a1: cstring`
- `a2: cint`
- `a3: Mode`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### shm_unlink

[ref: #symbol-shm-unlink]

**Input:**
- `a1: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### shutdown

[ref: #symbol-shutdown]

**Input:**
- `a1: SocketHandle`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigaction

[ref: #symbol-sigaction]

**Input:**
- `a1: cint`
- `a2: var Sigaction`
- `a3: var Sigaction`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigaction

[ref: #symbol-sigaction]

**Input:**
- `a1: cint`
- `a2: var Sigaction`
- `a3: ptr Sigaction = nil`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigaddset

[ref: #symbol-sigaddset]

**Input:**
- `a1: var Sigset`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigaltstack

[ref: #symbol-sigaltstack]

**Input:**
- `a1: var Stack`
- `a2: var Stack`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigdelset

[ref: #symbol-sigdelset]

**Input:**
- `a1: var Sigset`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigemptyset

[ref: #symbol-sigemptyset]

**Input:**
- `a1: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigfillset

[ref: #symbol-sigfillset]

**Input:**
- `a1: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sighold

[ref: #symbol-sighold]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigignore

[ref: #symbol-sigignore]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### siginterrupt

[ref: #symbol-siginterrupt]

**Input:**
- `a1: cint`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigismember

[ref: #symbol-sigismember]

**Input:**
- `a1: var Sigset`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### signal

[ref: #symbol-signal]

**Input:**
- `a1: cint`
- `a2: Sighandler`

**Output:** `Sighandler`
**Pragmas:** `importc`, `discardable`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigpause

[ref: #symbol-sigpause]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigpending

[ref: #symbol-sigpending]

**Input:**
- `a1: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigprocmask

[ref: #symbol-sigprocmask]

**Input:**
- `a1: cint`
- `a2: var Sigset`
- `a3: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigqueue

[ref: #symbol-sigqueue]

**Input:**
- `a1: Pid`
- `a2: cint`
- `a3: SigVal`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigrelse

[ref: #symbol-sigrelse]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigset

[ref: #symbol-sigset]

**Input:**
- `a1: int`
- `a2: proc (x: cint) {.noconv.}`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigsuspend

[ref: #symbol-sigsuspend]

**Input:**
- `a1: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigtimedwait

[ref: #symbol-sigtimedwait]

**Input:**
- `a1: var Sigset`
- `a2: var SigInfo`
- `a3: var Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigwait

[ref: #symbol-sigwait]

**Input:**
- `a1: var Sigset`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sigwaitinfo

[ref: #symbol-sigwaitinfo]

**Input:**
- `a1: var Sigset`
- `a2: var SigInfo`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sleep

[ref: #symbol-sleep]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sockatmark

[ref: #symbol-sockatmark]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### socket

[ref: #symbol-socket]

**Input:**
- `a1: cint`
- `a2: cint`
- `a3: cint`

**Output:** `SocketHandle`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Prev](posix_5.md) | [Next](posix_7.md)
