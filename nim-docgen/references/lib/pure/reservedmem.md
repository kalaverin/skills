---
source_hash: d0a2b8fa253be077
source_path: lib/pure/reservedmem.nim
---

# reservedmem

[ref: #module-reservedmem]

|  |  |
| --- | --- |
| Authors: | Zahary Karadjov |

This module provides utilities for reserving portions of the address space of a program without consuming physical memory. It can be used to implement a dynamically resizable buffer that is guaranteed to remain in the same memory location. The buffer will be able to grow up to the size of the initially reserved portion of the address space.

Unstable API.

## Let

### memExec

[ref: #symbol-memexec]

```nim
memExec = MemAccessFlags(PROT_EXEC)
```

### memExecRead

[ref: #symbol-memexecread]

```nim
memExecRead = MemAccessFlags(PROT_EXEC or PROT_READ)
```

### memExecReadWrite

[ref: #symbol-memexecreadwrite]

```nim
memExecReadWrite = MemAccessFlags(PROT_EXEC or PROT_READ or PROT_WRITE)
```

### memRead

[ref: #symbol-memread]

```nim
memRead = MemAccessFlags(PROT_READ)
```

### memReadWrite

[ref: #symbol-memreadwrite]

```nim
memReadWrite = MemAccessFlags(PROT_READ or PROT_WRITE)
```

## Proc

### `[]`

[ref: #symbol-]

**Input:**
- `s: ReservedMemSeq[T]`
- `pos: Natural`

**Output:** `lent T`
**Generic parameters:** `T`

### `[]`

[ref: #symbol-]

**Input:**
- `s: var ReservedMemSeq[T]`
- `pos: Natural`

**Output:** `var T`
**Generic parameters:** `T`

### `[]`

[ref: #symbol-]

**Input:**
- `s: ReservedMemSeq[T]`
- `rpos: BackwardsIndex`

**Output:** `lent T`
**Generic parameters:** `T`

### `[]`

[ref: #symbol-]

**Input:**
- `s: var ReservedMemSeq[T]`
- `rpos: BackwardsIndex`

**Output:** `var T`
**Generic parameters:** `T`

### add

[ref: #symbol-add]

**Input:**
- `s: var ReservedMemSeq[T]`
- `val: T`

**Output:** *(none)*
**Generic parameters:** `T`

### commitedLen

[ref: #symbol-commitedlen]

**Input:**
- `m: ReservedMem`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### commitedLen

[ref: #symbol-commitedlen]

**Input:**
- `s: ReservedMemSeq[T]`

**Output:** `int`
**Generic parameters:** `T`

### init

[ref: #symbol-init]

**Input:**
- `T: type ReservedMem`
- `maxLen: Natural`
- `initLen: Natural = 0`
- `initCommitLen:  = initLen`
- `memStart:  = pointer(nil)`
- `accessFlags:  = memReadWrite`
- `maxCommittedAndUnusedPages:  = 3`

**Output:** `ReservedMem`
**Generic parameters:** `T:type`

### init

[ref: #symbol-init]

**Input:**
- `SeqType: type ReservedMemSeq`
- `maxLen: Natural`
- `initLen: Natural = 0`
- `initCommitLen: Natural = 0`
- `memStart:  = pointer(nil)`
- `accessFlags:  = memReadWrite`
- `maxCommittedAndUnusedPages:  = 3`

**Output:** `SeqType:type`
**Generic parameters:** `SeqType:type`

### len

[ref: #symbol-len]

**Input:**
- `m: ReservedMem`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### len

[ref: #symbol-len]

**Input:**
- `s: ReservedMemSeq[T]`

**Output:** `int`
**Generic parameters:** `T`

### maxLen

[ref: #symbol-maxlen]

**Input:**
- `m: ReservedMem`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### maxLen

[ref: #symbol-maxlen]

**Input:**
- `s: ReservedMemSeq[T]`

**Output:** `int`
**Generic parameters:** `T`

### pop

[ref: #symbol-pop]

**Input:**
- `s: var ReservedMemSeq[T]`

**Output:** `T`
**Generic parameters:** `T`

### setLen

[ref: #symbol-setlen]

**Input:**
- `m: var ReservedMem`
- `newLen: int`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

### setLen

[ref: #symbol-setlen]

**Input:**
- `s: var ReservedMemSeq[T]`
- `newLen: int`

**Output:** *(none)*
**Generic parameters:** `T`

## Template

### distance

[ref: #symbol-distance]

**Input:**
- `lhs: pointer`
- `rhs: pointer`

**Output:** `int`
### shift

[ref: #symbol-shift]

**Input:**
- `p: pointer`
- `distance: int`

**Output:** `pointer`
## Type

### MemAccessFlags

[ref: #symbol-memaccessflags]

```nim
MemAccessFlags = int
```

### ReservedMem

[ref: #symbol-reservedmem]

```nim
ReservedMem = object
```

### ReservedMemSeq

[ref: #symbol-reservedmemseq]

```nim
ReservedMemSeq[T] = object
```
