---
source_hash: fcacb532bbcaa46f
source_path: lib/posix/posix.nim
---

### pipe

[ref: #symbol-pipe]

**Input:**
- `a: array[0 .. 1, cint]`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### poll

[ref: #symbol-poll]

**Input:**
- `a1: ptr TPollfd`
- `a2: Tnfds`
- `a3: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<poll.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### popen

[ref: #symbol-popen]

**Input:**
- `a1: cstring`
- `a2: cstring`

**Output:** `File`
**Pragmas:** `importc`, `header: "<stdio.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_fadvise

[ref: #symbol-posix-fadvise]

**Input:**
- `a1: cint`
- `a2: Off`
- `a3: Off`
- `a4: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fcntl.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_fallocate

[ref: #symbol-posix-fallocate]

**Input:**
- `a1: cint`
- `a2: Off`
- `a3: Off`

**Output:** `cint`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_madvise

[ref: #symbol-posix-madvise]

**Input:**
- `a1: pointer`
- `a2: int`
- `a3: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_mem_offset

[ref: #symbol-posix-mem-offset]

**Input:**
- `a1: pointer`
- `a2: int`
- `a3: var Off`
- `a4: var int`
- `a5: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_memalign

[ref: #symbol-posix-memalign]

**Input:**
- `memptr: pointer`
- `alignment: csize_t`
- `size: csize_t`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<stdlib.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawn

[ref: #symbol-posix-spawn]

**Input:**
- `a1: var Pid`
- `a2: cstring`
- `a3: var Tposix_spawn_file_actions`
- `a4: var Tposix_spawnattr`
- `a5: cstringArray`
- `a6: cstringArray`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawn_file_actions_addclose

[ref: #symbol-posix-spawn-file-actions-addclose]

**Input:**
- `a1: var Tposix_spawn_file_actions`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawn_file_actions_adddup2

[ref: #symbol-posix-spawn-file-actions-adddup2]

**Input:**
- `a1: var Tposix_spawn_file_actions`
- `a2: cint`
- `a3: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawn_file_actions_addopen

[ref: #symbol-posix-spawn-file-actions-addopen]

**Input:**
- `a1: var Tposix_spawn_file_actions`
- `a2: cint`
- `a3: cstring`
- `a4: cint`
- `a5: Mode`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawn_file_actions_destroy

[ref: #symbol-posix-spawn-file-actions-destroy]

**Input:**
- `a1: var Tposix_spawn_file_actions`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawn_file_actions_init

[ref: #symbol-posix-spawn-file-actions-init]

**Input:**
- `a1: var Tposix_spawn_file_actions`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_destroy

[ref: #symbol-posix-spawnattr-destroy]

**Input:**
- `a1: var Tposix_spawnattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_getflags

[ref: #symbol-posix-spawnattr-getflags]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: var cshort`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_getpgroup

[ref: #symbol-posix-spawnattr-getpgroup]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: var Pid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_getschedparam

[ref: #symbol-posix-spawnattr-getschedparam]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: var Sched_param`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_getschedpolicy

[ref: #symbol-posix-spawnattr-getschedpolicy]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_getsigdefault

[ref: #symbol-posix-spawnattr-getsigdefault]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_getsigmask

[ref: #symbol-posix-spawnattr-getsigmask]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_init

[ref: #symbol-posix-spawnattr-init]

**Input:**
- `a1: var Tposix_spawnattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_setflags

[ref: #symbol-posix-spawnattr-setflags]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_setpgroup

[ref: #symbol-posix-spawnattr-setpgroup]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: Pid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_setschedparam

[ref: #symbol-posix-spawnattr-setschedparam]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: var Sched_param`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_setschedpolicy

[ref: #symbol-posix-spawnattr-setschedpolicy]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_setsigdefault

[ref: #symbol-posix-spawnattr-setsigdefault]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnattr_setsigmask

[ref: #symbol-posix-spawnattr-setsigmask]

**Input:**
- `a1: var Tposix_spawnattr`
- `a2: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_spawnp

[ref: #symbol-posix-spawnp]

**Input:**
- `a1: var Pid`
- `a2: cstring`
- `a3: var Tposix_spawn_file_actions`
- `a4: var Tposix_spawnattr`
- `a5: cstringArray`
- `a6: cstringArray`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<spawn.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_typed_mem_get_info

[ref: #symbol-posix-typed-mem-get-info]

**Input:**
- `a1: cint`
- `a2: var Posix_typed_mem_info`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### posix_typed_mem_open

[ref: #symbol-posix-typed-mem-open]

**Input:**
- `a1: cstring`
- `a2: cint`
- `a3: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pread

[ref: #symbol-pread]

**Input:**
- `a1: cint`
- `a2: pointer`
- `a3: int`
- `a4: Off`

**Output:** `int`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pselect

[ref: #symbol-pselect]

**Input:**
- `a1: cint`
- `a2: ptr TFdSet`
- `a3: ptr TFdSet`
- `a4: ptr TFdSet`
- `a5: ptr Timespec`
- `a6: var Sigset`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/select.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_atfork

[ref: #symbol-pthread-atfork]

**Input:**
- `a1: proc () {.noconv.}`
- `a2: proc () {.noconv.}`
- `a3: proc () {.noconv.}`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_destroy

[ref: #symbol-pthread-attr-destroy]

**Input:**
- `a1: ptr Pthread_attr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_getdetachstate

[ref: #symbol-pthread-attr-getdetachstate]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_getguardsize

[ref: #symbol-pthread-attr-getguardsize]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_getinheritsched

[ref: #symbol-pthread-attr-getinheritsched]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_getschedparam

[ref: #symbol-pthread-attr-getschedparam]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: ptr Sched_param`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_getschedpolicy

[ref: #symbol-pthread-attr-getschedpolicy]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_getscope

[ref: #symbol-pthread-attr-getscope]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_getstack

[ref: #symbol-pthread-attr-getstack]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: var pointer`
- `a3: var int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_getstackaddr

[ref: #symbol-pthread-attr-getstackaddr]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: var pointer`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_getstacksize

[ref: #symbol-pthread-attr-getstacksize]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: var int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_init

[ref: #symbol-pthread-attr-init]

**Input:**
- `a1: ptr Pthread_attr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setdetachstate

[ref: #symbol-pthread-attr-setdetachstate]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setguardsize

[ref: #symbol-pthread-attr-setguardsize]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setinheritsched

[ref: #symbol-pthread-attr-setinheritsched]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setschedparam

[ref: #symbol-pthread-attr-setschedparam]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: ptr Sched_param`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setschedpolicy

[ref: #symbol-pthread-attr-setschedpolicy]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setscope

[ref: #symbol-pthread-attr-setscope]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setstack

[ref: #symbol-pthread-attr-setstack]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: pointer`
- `a3: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setstackaddr

[ref: #symbol-pthread-attr-setstackaddr]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: pointer`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setstacksize

[ref: #symbol-pthread-attr-setstacksize]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_barrier_destroy

[ref: #symbol-pthread-barrier-destroy]

**Input:**
- `a1: ptr Pthread_barrier`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_barrier_init

[ref: #symbol-pthread-barrier-init]

**Input:**
- `a1: ptr Pthread_barrier`
- `a2: ptr Pthread_barrierattr`
- `a3: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_barrier_wait

[ref: #symbol-pthread-barrier-wait]

**Input:**
- `a1: ptr Pthread_barrier`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_barrierattr_destroy

[ref: #symbol-pthread-barrierattr-destroy]

**Input:**
- `a1: ptr Pthread_barrierattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_barrierattr_getpshared

[ref: #symbol-pthread-barrierattr-getpshared]

**Input:**
- `a1: ptr Pthread_barrierattr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_barrierattr_init

[ref: #symbol-pthread-barrierattr-init]

**Input:**
- `a1: ptr Pthread_barrierattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_barrierattr_setpshared

[ref: #symbol-pthread-barrierattr-setpshared]

**Input:**
- `a1: ptr Pthread_barrierattr`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_cancel

[ref: #symbol-pthread-cancel]

**Input:**
- `a1: Pthread`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_cleanup_pop

[ref: #symbol-pthread-cleanup-pop]

**Input:**
- `a1: cint`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_cleanup_push

[ref: #symbol-pthread-cleanup-push]

**Input:**
- `a1: proc (x: pointer) {.noconv.}`
- `a2: pointer`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_cond_broadcast

[ref: #symbol-pthread-cond-broadcast]

**Input:**
- `a1: ptr Pthread_cond`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_cond_destroy

[ref: #symbol-pthread-cond-destroy]

**Input:**
- `a1: ptr Pthread_cond`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_cond_init

[ref: #symbol-pthread-cond-init]

**Input:**
- `a1: ptr Pthread_cond`
- `a2: ptr Pthread_condattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_cond_signal

[ref: #symbol-pthread-cond-signal]

**Input:**
- `a1: ptr Pthread_cond`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_cond_timedwait

[ref: #symbol-pthread-cond-timedwait]

**Input:**
- `a1: ptr Pthread_cond`
- `a2: ptr Pthread_mutex`
- `a3: ptr Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_cond_wait

[ref: #symbol-pthread-cond-wait]

**Input:**
- `a1: ptr Pthread_cond`
- `a2: ptr Pthread_mutex`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_condattr_destroy

[ref: #symbol-pthread-condattr-destroy]

**Input:**
- `a1: ptr Pthread_condattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_condattr_getclock

[ref: #symbol-pthread-condattr-getclock]

**Input:**
- `a1: ptr Pthread_condattr`
- `a2: var ClockId`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_condattr_getpshared

[ref: #symbol-pthread-condattr-getpshared]

**Input:**
- `a1: ptr Pthread_condattr`
- `a2: var cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_condattr_init

[ref: #symbol-pthread-condattr-init]

**Input:**
- `a1: ptr Pthread_condattr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_condattr_setclock

[ref: #symbol-pthread-condattr-setclock]

**Input:**
- `a1: ptr Pthread_condattr`
- `a2: ClockId`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Prev](posix_3.md) | [Next](posix_5.md)
