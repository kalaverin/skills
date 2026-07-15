---
source_hash: 5e2b8a820bf402ab
source_path: lib/std/private/syslocks.nim
---

# syslocks

[ref: #module-syslocks]

## Proc

### initSysLockAttr

[ref: #symbol-initsyslockattr]

**Input:**
- `a: var SysLockAttr`

**Output:** *(none)*
**Pragmas:** `importc: "pthread_mutexattr_init"`, `header: "<pthread.h>"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setSysLockType

[ref: #symbol-setsyslocktype]

**Input:**
- `a: var SysLockAttr`
- `t: SysLockType`

**Output:** *(none)*
**Pragmas:** `importc: "pthread_mutexattr_settype"`, `header: "<pthread.h>"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### acquireSys

[ref: #symbol-acquiresys]

**Input:**
- `L: var SysLock`

**Output:** *(none)*
### broadcastSysCond

[ref: #symbol-broadcastsyscond]

**Input:**
- `cond: var SysCond`

**Output:** *(none)*
### deinitSys

[ref: #symbol-deinitsys]

**Input:**
- `L: SysLock`

**Output:** *(none)*
### deinitSysCond

[ref: #symbol-deinitsyscond]

**Input:**
- `cond: SysCond`

**Output:** *(none)*
### initSysCond

[ref: #symbol-initsyscond]

**Input:**
- `cond: var SysCond`
- `cond_attr: ptr SysCondAttr = nil`

**Output:** *(none)*
### initSysLock

[ref: #symbol-initsyslock]

**Input:**
- `L: var SysLock`
- `attr: ptr SysLockAttr = nil`

**Output:** *(none)*
### releaseSys

[ref: #symbol-releasesys]

**Input:**
- `L: var SysLock`

**Output:** *(none)*
### signalSysCond

[ref: #symbol-signalsyscond]

**Input:**
- `cond: var SysCond`

**Output:** *(none)*
### tryAcquireSys

[ref: #symbol-tryacquiresys]

**Input:**
- `L: var SysLock`

**Output:** `bool`
### waitSysCond

[ref: #symbol-waitsyscond]

**Input:**
- `cond: var SysCond`
- `lock: var SysLock`

**Output:** *(none)*
## Type

### SysCond

[ref: #symbol-syscond]

```nim
SysCond = SysCondObj
```

### SysLock

[ref: #symbol-syslock]

```nim
SysLock = SysLockObj
```

### SysLockAttr

[ref: #symbol-syslockattr]

```nim
SysLockAttr {.importc: "pthread_mutexattr_t", pure, final, header: """#include <sys/types.h>
                          #include <pthread.h>""".} = object
  when defined(linux) and defined(amd64):
```

## Var

### SysLockType_Reentrant

[ref: #symbol-syslocktype-reentrant]

```nim
SysLockType_Reentrant {.importc: "PTHREAD_MUTEX_RECURSIVE",
                        header: "<pthread.h>".}: SysLockType
```
