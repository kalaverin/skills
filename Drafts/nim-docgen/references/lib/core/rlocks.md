---
source_hash: b52d4715b9577eba
source_path: lib/core/rlocks.nim
---

# rlocks

[ref: #module-rlocks]

This module contains Nim's support for reentrant locks.

## Proc

### acquire

[ref: #symbol-acquire]

**Input:**
- `lock: var RLock`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Acquires the given lock.

### deinitRLock

[ref: #symbol-deinitrlock]

**Input:**
- `lock: RLock`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Frees the resources associated with the lock.

### initRLock

[ref: #symbol-initrlock]

**Input:**
- `lock: var RLock`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Initializes the given lock.

### release

[ref: #symbol-release]

**Input:**
- `lock: var RLock`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Releases the given lock.

### tryAcquire

[ref: #symbol-tryacquire]

**Input:**
- `lock: var RLock`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Tries to acquire the given lock. Returns true on success.

## Template

### withRLock

[ref: #symbol-withrlock]

**Input:**
- `lock: RLock`
- `code: untyped`

**Output:** *(none)*
Acquires the given lock and then executes the code.

## Type

### RLock

[ref: #symbol-rlock]

```nim
RLock = SysLock
```

Nim lock, re-entrant
