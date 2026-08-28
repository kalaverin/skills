---
source_hash: fcacb532bbcaa46f
source_path: lib/posix/posix.nim
---

### pthread_condattr_setpshared

[ref: #symbol-pthread-condattr-setpshared]

**Input:**
- `a1: ptr Pthread_condattr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_create

[ref: #symbol-pthread-create]

**Input:**
- `a1: ptr Pthread`
- `a2: ptr Pthread_attr`
- `a3: proc (x: pointer): pointer {.noconv.}`
- `a4: pointer`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_detach

[ref: #symbol-pthread-detach]

**Input:**
- `a1: Pthread`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_equal

[ref: #symbol-pthread-equal]

**Input:**
- `a1: Pthread`
- `a2: Pthread`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_exit

[ref: #symbol-pthread-exit]

**Input:**
- `a1: pointer`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_getconcurrency

[ref: #symbol-pthread-getconcurrency]

**Input:**
- *(none)*

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_getcpuclockid

[ref: #symbol-pthread-getcpuclockid]

**Input:**
- `a1: Pthread`
- `a2: var ClockId`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_getschedparam

[ref: #symbol-pthread-getschedparam]

**Input:**
- `a1: Pthread`
- `a2: var cint`
- `a3: ptr Sched_param`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_getspecific

[ref: #symbol-pthread-getspecific]

**Input:**
- `a1: Pthread_key`

**Output:** `pointer`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_join

[ref: #symbol-pthread-join]

**Input:**
- `a1: Pthread`
- `a2: ptr pointer`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_key_create

[ref: #symbol-pthread-key-create]

**Input:**
- `a1: ptr Pthread_key`
- `a2: proc (x: pointer) {.noconv.}`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_key_delete

[ref: #symbol-pthread-key-delete]

**Input:**
- `a1: Pthread_key`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_kill

[ref: #symbol-pthread-kill]

**Input:**
- `a1: Pthread`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutex_destroy

[ref: #symbol-pthread-mutex-destroy]

**Input:**
- `a1: ptr Pthread_mutex`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutex_getprioceiling

[ref: #symbol-pthread-mutex-getprioceiling]

**Input:**
- `a1: ptr Pthread_mutex`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutex_init

[ref: #symbol-pthread-mutex-init]

**Input:**
- `a1: ptr Pthread_mutex`
- `a2: ptr Pthread_mutexattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutex_lock

[ref: #symbol-pthread-mutex-lock]

**Input:**
- `a1: ptr Pthread_mutex`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutex_setprioceiling

[ref: #symbol-pthread-mutex-setprioceiling]

**Input:**
- `a1: ptr Pthread_mutex`
- `a2: cint`
- `a3: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutex_timedlock

[ref: #symbol-pthread-mutex-timedlock]

**Input:**
- `a1: ptr Pthread_mutex`
- `a2: ptr Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutex_trylock

[ref: #symbol-pthread-mutex-trylock]

**Input:**
- `a1: ptr Pthread_mutex`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutex_unlock

[ref: #symbol-pthread-mutex-unlock]

**Input:**
- `a1: ptr Pthread_mutex`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutexattr_destroy

[ref: #symbol-pthread-mutexattr-destroy]

**Input:**
- `a1: ptr Pthread_mutexattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutexattr_getprioceiling

[ref: #symbol-pthread-mutexattr-getprioceiling]

**Input:**
- `a1: ptr Pthread_mutexattr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutexattr_getprotocol

[ref: #symbol-pthread-mutexattr-getprotocol]

**Input:**
- `a1: ptr Pthread_mutexattr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutexattr_getpshared

[ref: #symbol-pthread-mutexattr-getpshared]

**Input:**
- `a1: ptr Pthread_mutexattr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutexattr_gettype

[ref: #symbol-pthread-mutexattr-gettype]

**Input:**
- `a1: ptr Pthread_mutexattr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutexattr_init

[ref: #symbol-pthread-mutexattr-init]

**Input:**
- `a1: ptr Pthread_mutexattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutexattr_setprioceiling

[ref: #symbol-pthread-mutexattr-setprioceiling]

**Input:**
- `a1: ptr Pthread_mutexattr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutexattr_setprotocol

[ref: #symbol-pthread-mutexattr-setprotocol]

**Input:**
- `a1: ptr Pthread_mutexattr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutexattr_setpshared

[ref: #symbol-pthread-mutexattr-setpshared]

**Input:**
- `a1: ptr Pthread_mutexattr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_mutexattr_settype

[ref: #symbol-pthread-mutexattr-settype]

**Input:**
- `a1: ptr Pthread_mutexattr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_once

[ref: #symbol-pthread-once]

**Input:**
- `a1: ptr Pthread_once`
- `a2: proc () {.noconv.}`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlock_destroy

[ref: #symbol-pthread-rwlock-destroy]

**Input:**
- `a1: ptr Pthread_rwlock`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlock_init

[ref: #symbol-pthread-rwlock-init]

**Input:**
- `a1: ptr Pthread_rwlock`
- `a2: ptr Pthread_rwlockattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlock_rdlock

[ref: #symbol-pthread-rwlock-rdlock]

**Input:**
- `a1: ptr Pthread_rwlock`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlock_timedrdlock

[ref: #symbol-pthread-rwlock-timedrdlock]

**Input:**
- `a1: ptr Pthread_rwlock`
- `a2: ptr Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlock_timedwrlock

[ref: #symbol-pthread-rwlock-timedwrlock]

**Input:**
- `a1: ptr Pthread_rwlock`
- `a2: ptr Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlock_tryrdlock

[ref: #symbol-pthread-rwlock-tryrdlock]

**Input:**
- `a1: ptr Pthread_rwlock`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlock_trywrlock

[ref: #symbol-pthread-rwlock-trywrlock]

**Input:**
- `a1: ptr Pthread_rwlock`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlock_unlock

[ref: #symbol-pthread-rwlock-unlock]

**Input:**
- `a1: ptr Pthread_rwlock`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlock_wrlock

[ref: #symbol-pthread-rwlock-wrlock]

**Input:**
- `a1: ptr Pthread_rwlock`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlockattr_destroy

[ref: #symbol-pthread-rwlockattr-destroy]

**Input:**
- `a1: ptr Pthread_rwlockattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlockattr_getpshared

[ref: #symbol-pthread-rwlockattr-getpshared]

**Input:**
- `a1: ptr Pthread_rwlockattr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlockattr_init

[ref: #symbol-pthread-rwlockattr-init]

**Input:**
- `a1: ptr Pthread_rwlockattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_rwlockattr_setpshared

[ref: #symbol-pthread-rwlockattr-setpshared]

**Input:**
- `a1: ptr Pthread_rwlockattr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_self

[ref: #symbol-pthread-self]

**Input:**
- *(none)*

**Output:** `Pthread`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_setcancelstate

[ref: #symbol-pthread-setcancelstate]

**Input:**
- `a1: cint`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_setcanceltype

[ref: #symbol-pthread-setcanceltype]

**Input:**
- `a1: cint`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_setconcurrency

[ref: #symbol-pthread-setconcurrency]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_setschedparam

[ref: #symbol-pthread-setschedparam]

**Input:**
- `a1: Pthread`
- `a2: cint`
- `a3: ptr Sched_param`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_setschedprio

[ref: #symbol-pthread-setschedprio]

**Input:**
- `a1: Pthread`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_setspecific

[ref: #symbol-pthread-setspecific]

**Input:**
- `a1: Pthread_key`
- `a2: pointer`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_sigmask

[ref: #symbol-pthread-sigmask]

**Input:**
- `a1: cint`
- `a2: var Sigset`
- `a3: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_spin_destroy

[ref: #symbol-pthread-spin-destroy]

**Input:**
- `a1: ptr Pthread_spinlock`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_spin_init

[ref: #symbol-pthread-spin-init]

**Input:**
- `a1: ptr Pthread_spinlock`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_spin_lock

[ref: #symbol-pthread-spin-lock]

**Input:**
- `a1: ptr Pthread_spinlock`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_spin_trylock

[ref: #symbol-pthread-spin-trylock]

**Input:**
- `a1: ptr Pthread_spinlock`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_spin_unlock

[ref: #symbol-pthread-spin-unlock]

**Input:**
- `a1: ptr Pthread_spinlock`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_testcancel

[ref: #symbol-pthread-testcancel]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pwrite

[ref: #symbol-pwrite]

**Input:**
- `a1: cint`
- `a2: pointer`
- `a3: int`
- `a4: Off`

**Output:** `int`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### read

[ref: #symbol-read]

**Input:**
- `a1: cint`
- `a2: pointer`
- `a3: int`

**Output:** `int`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readdir

[ref: #symbol-readdir]

**Input:**
- `a1: ptr DIR`

**Output:** `ptr Dirent`
**Pragmas:** `importc`, `header: "<dirent.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readdir_r

[ref: #symbol-readdir-r]

**Input:**
- `a1: ptr DIR`
- `a2: ptr Dirent`
- `a3: ptr ptr Dirent`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<dirent.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readlink

[ref: #symbol-readlink]

**Input:**
- `a1: cstring`
- `a2: cstring`
- `a3: int`

**Output:** `int`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readv

[ref: #symbol-readv]

**Input:**
- `a1: cint`
- `a2: ptr IOVec`
- `a3: cint`

**Output:** `int`
**Pragmas:** `importc`, `header: "<sys/uio.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### realpath

[ref: #symbol-realpath]

**Input:**
- `name: cstring`
- `resolved: cstring`

**Output:** `cstring`
**Pragmas:** `importc: "realpath"`, `header: "<stdlib.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### recv

[ref: #symbol-recv]

**Input:**
- `a1: SocketHandle`
- `a2: pointer`
- `a3: int`
- `a4: cint`

**Output:** `int`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### recvfrom

[ref: #symbol-recvfrom]

**Input:**
- `a1: SocketHandle`
- `a2: pointer`
- `a3: int`
- `a4: cint`
- `a5: ptr SockAddr`
- `a6: ptr SockLen`

**Output:** `int`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### recvmsg

[ref: #symbol-recvmsg]

**Input:**
- `a1: SocketHandle`
- `a2: ptr Tmsghdr`
- `a3: cint`

**Output:** `int`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### rewinddir

[ref: #symbol-rewinddir]

**Input:**
- `a1: ptr DIR`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<dirent.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### rmdir

[ref: #symbol-rmdir]

**Input:**
- `a1: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### S_ISBLK

[ref: #symbol-s-isblk]

**Input:**
- `m: Mode`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test for a block special file.

### S_ISCHR

[ref: #symbol-s-ischr]

**Input:**
- `m: Mode`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test for a character special file.

### S_ISDIR

[ref: #symbol-s-isdir]

**Input:**
- `m: Mode`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test for a directory.

### S_ISFIFO

[ref: #symbol-s-isfifo]

**Input:**
- `m: Mode`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test for a pipe or FIFO special file.

### S_ISLNK

[ref: #symbol-s-islnk]

**Input:**
- `m: Mode`

**Output:** `bool`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Test for a symbolic link.


[Prev](posix_4.md) | [Next](posix_6.md)
