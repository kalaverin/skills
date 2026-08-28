---
source_hash: 97896ba07a4391bb
source_path: lib/core/locks.nim
---

# locks

[ref: #module-locks]

This module contains Nim's support for locks and condition vars.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `lock: Lock`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### acquire

[ref: #symbol-acquire]

**Input:**
- `lock: var Lock`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Acquires the given lock.

### broadcast

[ref: #symbol-broadcast]

**Input:**
- `cond: var Cond`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unblocks all threads currently blocked on the specified condition variable cond.

### deinitCond

[ref: #symbol-deinitcond]

**Input:**
- `cond: Cond`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Frees the resources associated with the condition variable.

### deinitLock

[ref: #symbol-deinitlock]

**Input:**
- `lock: Lock`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Frees the resources associated with the lock.

### initCond

[ref: #symbol-initcond]

**Input:**
- `cond: var Cond`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Initializes the given condition variable.

### initLock

[ref: #symbol-initlock]

**Input:**
- `lock: var Lock`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Initializes the given lock.

### release

[ref: #symbol-release]

**Input:**
- `lock: var Lock`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Releases the given lock.

### signal

[ref: #symbol-signal]

**Input:**
- `cond: var Cond`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sends a signal to the condition variable cond.

### tryAcquire

[ref: #symbol-tryacquire]

**Input:**
- `lock: var Lock`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Tries to acquire the given lock. Returns true on success.

### wait

[ref: #symbol-wait]

**Input:**
- `cond: var Cond`
- `lock: var Lock`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Waits on the condition variable cond.

## Template

### withLock

[ref: #symbol-withlock]

**Input:**
- `a: Lock`
- `body: untyped`

**Output:** *(none)*
Acquires the given lock, executes the statements in body and releases the lock after the statements finish executing.

## Type

### Cond

[ref: #symbol-cond]

```nim
Cond = SysCond
```

Nim condition variable

### Lock

[ref: #symbol-lock]

```nim
Lock = SysLock
```

Nim lock; whether this is re-entrant or not is unspecified!
