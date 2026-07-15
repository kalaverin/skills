---
source_hash: e7b138491b69fee6
source_path: lib/std/private/threadtypes.nim
---

# threadtypes

[ref: #module-threadtypes]

## Const

### emulatedThreadVars

[ref: #symbol-emulatedthreadvars]

```nim
emulatedThreadVars = false
```

### hasAllocStack

[ref: #symbol-hasallocstack]

```nim
hasAllocStack = false
```

### hasSharedHeap

[ref: #symbol-hassharedheap]

```nim
hasSharedHeap = false
```

### pthreadh

[ref: #symbol-pthreadh]

```nim
pthreadh = "#define _GNU_SOURCE\n#include <pthread.h>"
```

## Proc

### `=copy`

[ref: #symbol-copy]

**Input:**
- `x: var Thread[TArg]`
- `y: Thread[TArg]`

**Output:** *(none)*
**Generic parameters:** `TArg`

**Pragmas:** `error`

### cpusetIncl

[ref: #symbol-cpusetincl]

**Input:**
- `cpu: cint`
- `s: var CpuSet`

**Output:** *(none)*
**Pragmas:** `importc: "CPU_SET"`, `header: "#define _GNU_SOURCE\n#include <sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cpusetZero

[ref: #symbol-cpusetzero]

**Input:**
- `s: var CpuSet`

**Output:** *(none)*
**Pragmas:** `importc: "CPU_ZERO"`, `header: "#define _GNU_SOURCE\n#include <sched.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_destroy

[ref: #symbol-pthread-attr-destroy]

**Input:**
- `a1: var Pthread_attr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "#define _GNU_SOURCE\n#include <pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_init

[ref: #symbol-pthread-attr-init]

**Input:**
- `a1: var Pthread_attr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "#define _GNU_SOURCE\n#include <pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setstack

[ref: #symbol-pthread-attr-setstack]

**Input:**
- `a1: ptr Pthread_attr`
- `a2: pointer`
- `a3: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "#define _GNU_SOURCE\n#include <pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_attr_setstacksize

[ref: #symbol-pthread-attr-setstacksize]

**Input:**
- `a1: var Pthread_attr`
- `a2: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "#define _GNU_SOURCE\n#include <pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_cancel

[ref: #symbol-pthread-cancel]

**Input:**
- `a1: SysThread`

**Output:** `cint`
**Pragmas:** `importc: "pthread_cancel"`, `header: "#define _GNU_SOURCE\n#include <pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_create

[ref: #symbol-pthread-create]

**Input:**
- `a1: var SysThread`
- `a2: var Pthread_attr`
- `a3: proc (x: pointer): pointer {.noconv.}`
- `a4: pointer`

**Output:** `cint`
**Pragmas:** `importc: "pthread_create"`, `header: "#define _GNU_SOURCE\n#include <pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pthread_join

[ref: #symbol-pthread-join]

**Input:**
- `a1: SysThread`
- `a2: ptr pointer`

**Output:** `cint`
**Pragmas:** `importc`, `header: "#define _GNU_SOURCE\n#include <pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setAffinity

[ref: #symbol-setaffinity]

**Input:**
- `thread: SysThread`
- `setsize: csize_t`
- `s: var CpuSet`

**Output:** *(none)*
**Pragmas:** `importc: "pthread_setaffinity_np"`, `header: "#define _GNU_SOURCE\n#include <pthread.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### CpuSet

[ref: #symbol-cpuset]

```nim
CpuSet {.importc: "cpu_set_t", header: "#define _GNU_SOURCE\n#include <sched.h>".} = object
  when defined(linux) and defined(amd64):
```

### GcThread

[ref: #symbol-gcthread]

```nim
GcThread {.pure, inheritable.} = object
  when emulatedThreadVars:
    tls*: ThreadLocalStorage
  else:
    nil
  when hasSharedHeap:
    next*, prev*: PGcThread
    stackBottom*, stackTop*: pointer
    stackSize*: int
  else:
    nil
```

### PGcThread

[ref: #symbol-pgcthread]

```nim
PGcThread = ptr GcThread
```

### Pthread_attr

[ref: #symbol-pthread-attr]

```nim
Pthread_attr {.importc: "pthread_attr_t", header: "<sys/types.h>".} = object
```

### SysThread

[ref: #symbol-systhread]

```nim
SysThread {.importc: "pthread_t", header: "<sys/types.h>".} = int
```

### Thread

[ref: #symbol-thread]

```nim
Thread[TArg] = object
  core*: PGcThread
  sys*: SysThread
  when TArg is void:
    dataFn*: proc () {.nimcall, gcsafe.}
  else:
    dataFn*: proc (m: TArg) {.nimcall, gcsafe.}
    data*: TArg
  when hasAllocStack:
    rawStack*: pointer
```

### ThreadLocalStorage

[ref: #symbol-threadlocalstorage]

```nim
ThreadLocalStorage = array[0 .. (nimTlsSize div 8), float]
```

### Timespec

[ref: #symbol-timespec]

```nim
Timespec {.importc: "struct timespec", header: "<time.h>".} = object
  tv_sec*: Time
  tv_nsec*: clong
```
