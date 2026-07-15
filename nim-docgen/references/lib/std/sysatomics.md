---
source_hash: 4fb2a6514c48125d
source_path: lib/std/sysatomics.nim
---

# sysatomics

[ref: #module-sysatomics]

Perform the operation return the new value, all memory models are validPerform the operation return the old value, all memory models are valid

## Proc

### atomicAddFetch

[ref: #symbol-atomicaddfetch]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_add_fetch"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicAlwaysLockFree

[ref: #symbol-atomicalwayslockfree]

**Input:**
- `size: int`
- `p: pointer`

**Output:** `bool`
**Pragmas:** `importc: "__atomic_always_lock_free"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This built-in function returns true if objects of size bytes always generate lock free atomic instructions for the target architecture. size must resolve to a compile-time constant and the result also resolves to a compile-time constant. ptr is an optional pointer to the object that may be used to determine alignment. A value of 0 indicates typical alignment should be used. The compiler may also ignore this parameter.

### atomicAndFetch

[ref: #symbol-atomicandfetch]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_and_fetch"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicClear

[ref: #symbol-atomicclear]

**Input:**
- `p: pointer`
- `mem: AtomMemModel`

**Output:** *(none)*
**Pragmas:** `importc: "__atomic_clear"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This built-in function performs an atomic clear operation at p. After the operation, at p contains 0. ATOMIC\_RELAXED, ATOMIC\_SEQ\_CST, ATOMIC\_RELEASE

### atomicCompareExchange

[ref: #symbol-atomiccompareexchange]

**Input:**
- `p: ptr T`
- `expected: ptr T`
- `desired: ptr T`
- `weak: bool`
- `success_memmodel: AtomMemModel`
- `failure_memmodel: AtomMemModel`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_compare_exchange"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This proc implements the generic version of atomic\_compare\_exchange. The proc is virtually identical to atomic\_compare\_exchange\_n, except the desired value is also a pointer.

### atomicCompareExchangeN

[ref: #symbol-atomiccompareexchangen]

**Input:**
- `p: ptr T`
- `expected: ptr T`
- `desired: T`
- `weak: bool`
- `success_memmodel: AtomMemModel`
- `failure_memmodel: AtomMemModel`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_compare_exchange_n"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This proc implements an atomic compare and exchange operation. This compares the contents at p with the contents at expected and if equal, writes desired at p. If they are not equal, the current contents at p is written into expected. Weak is true for weak compare\_exchange, and false for the strong variation. Many targets only offer the strong variation and ignore the parameter. When in doubt, use the strong variation. True is returned if desired is written at p and the execution is considered to conform to the memory model specified by success\_memmodel. There are no restrictions on what memory model can be used here. False is returned otherwise, and the execution is considered to conform to failure\_memmodel. This memory model cannot be \_\_ATOMIC\_RELEASE nor \_\_ATOMIC\_ACQ\_REL. It also cannot be a stronger model than that specified by success\_memmodel.

### atomicDec

[ref: #symbol-atomicdec]

**Input:**
- `memLoc: var int`
- `x: int = 1`

**Output:** `int`
**Pragmas:** `inline`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically decrements the integer by some x. It returns the new value.

### atomicExchange

[ref: #symbol-atomicexchange]

**Input:**
- `p: ptr T`
- `val: ptr T`
- `ret: ptr T`
- `mem: AtomMemModel`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_exchange"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This is the generic version of an atomic exchange. It stores the contents at val at p. The original value at p is copied into ret.

### atomicExchangeN

[ref: #symbol-atomicexchangen]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_exchange_n"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This proc implements an atomic exchange operation. It writes val at p, and returns the previous contents at p. ATOMIC\_RELAXED, ATOMIC\_SEQ\_CST, ATOMIC\_ACQUIRE, ATOMIC\_RELEASE, ATOMIC\_ACQ\_REL

### atomicFetchAdd

[ref: #symbol-atomicfetchadd]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_fetch_add"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicFetchAnd

[ref: #symbol-atomicfetchand]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_fetch_and"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicFetchNand

[ref: #symbol-atomicfetchnand]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_fetch_nand"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicFetchOr

[ref: #symbol-atomicfetchor]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_fetch_or"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicFetchSub

[ref: #symbol-atomicfetchsub]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_fetch_sub"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicFetchXor

[ref: #symbol-atomicfetchxor]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_fetch_xor"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicInc

[ref: #symbol-atomicinc]

**Input:**
- `memLoc: var int`
- `x: int = 1`

**Output:** `int`
**Pragmas:** `inline`, `discardable`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically increments the integer by some x. It returns the new value.

### atomicIsLockFree

[ref: #symbol-atomicislockfree]

**Input:**
- `size: int`
- `p: pointer`

**Output:** `bool`
**Pragmas:** `importc: "__atomic_is_lock_free"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This built-in function returns true if objects of size bytes always generate lock free atomic instructions for the target architecture. If it is not known to be lock free a call is made to a runtime routine named \_\_atomic\_is\_lock\_free. ptr is an optional pointer to the object that may be used to determine alignment. A value of 0 indicates typical alignment should be used. The compiler may also ignore this parameter.

### atomicLoad

[ref: #symbol-atomicload]

**Input:**
- `p: ptr T`
- `ret: ptr T`
- `mem: AtomMemModel`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_load"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This is the generic version of an atomic load. It returns the contents at p in ret.

### atomicLoadN

[ref: #symbol-atomicloadn]

**Input:**
- `p: ptr T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_load_n"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This proc implements an atomic load operation. It returns the contents at p. ATOMIC\_RELAXED, ATOMIC\_SEQ\_CST, ATOMIC\_ACQUIRE, ATOMIC\_CONSUME.

### atomicNandFetch

[ref: #symbol-atomicnandfetch]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_nand_fetch"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicOrFetch

[ref: #symbol-atomicorfetch]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_or_fetch"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicSignalFence

[ref: #symbol-atomicsignalfence]

**Input:**
- `mem: AtomMemModel`

**Output:** *(none)*
**Pragmas:** `importc: "__atomic_signal_fence"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This built-in function acts as a synchronization fence between a thread and signal handlers based in the same thread. All memory orders are valid.

### atomicStore

[ref: #symbol-atomicstore]

**Input:**
- `p: ptr T`
- `val: ptr T`
- `mem: AtomMemModel`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_store"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This is the generic version of an atomic store. It stores the value of val at p

### atomicStoreN

[ref: #symbol-atomicstoren]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_store_n"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This proc implements an atomic store operation. It writes val at p. ATOMIC\_RELAXED, ATOMIC\_SEQ\_CST, and ATOMIC\_RELEASE.

### atomicSubFetch

[ref: #symbol-atomicsubfetch]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_sub_fetch"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### atomicTestAndSet

[ref: #symbol-atomictestandset]

**Input:**
- `p: pointer`
- `mem: AtomMemModel`

**Output:** `bool`
**Pragmas:** `importc: "__atomic_test_and_set"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This built-in function performs an atomic test-and-set operation on the byte at p. The byte is set to some implementation defined nonzero "set" value and the return value is true if and only if the previous contents were "set". All memory models are valid.

### atomicThreadFence

[ref: #symbol-atomicthreadfence]

**Input:**
- `mem: AtomMemModel`

**Output:** *(none)*
**Pragmas:** `importc: "__atomic_thread_fence"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This built-in function acts as a synchronization fence between threads based on the specified memory model. All memory orders are valid.

### atomicXorFetch

[ref: #symbol-atomicxorfetch]

**Input:**
- `p: ptr T`
- `val: T`
- `mem: AtomMemModel`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importc: "__atomic_xor_fetch"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cas

[ref: #symbol-cas]

**Input:**
- `p: ptr T`
- `oldValue: T`
- `newValue: T`

**Output:** `bool`
**Generic parameters:** `T`

### cpuRelax

[ref: #symbol-cpurelax]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### fence

[ref: #symbol-fence]

**Input:**
- *(none)*

**Output:** *(none)*
## Type

### AtomMemModel

[ref: #symbol-atommemmodel]

```nim
AtomMemModel = distinct cint
```

### AtomType

[ref: #symbol-atomtype]

```nim
AtomType = SomeNumber | pointer | ptr | char | bool
```

Type Class representing valid types for use with atomic procs

## Var

### ATOMIC_ACQ_REL

[ref: #symbol-atomic-acq-rel]

```nim
ATOMIC_ACQ_REL {.importc: "__ATOMIC_ACQ_REL", nodecl.}: AtomMemModel
```

Full barrier in both directions and synchronizes with acquire loads and release stores in another thread.

### ATOMIC_ACQUIRE

[ref: #symbol-atomic-acquire]

```nim
ATOMIC_ACQUIRE {.importc: "__ATOMIC_ACQUIRE", nodecl.}: AtomMemModel
```

Barrier to hoisting of code and synchronizes with release (or stronger) semantic stores from another thread.

### ATOMIC_CONSUME

[ref: #symbol-atomic-consume]

```nim
ATOMIC_CONSUME {.importc: "__ATOMIC_CONSUME", nodecl.}: AtomMemModel
```

Data dependency only for both barrier and synchronization with another thread.

### ATOMIC_RELAXED

[ref: #symbol-atomic-relaxed]

```nim
ATOMIC_RELAXED {.importc: "__ATOMIC_RELAXED", nodecl.}: AtomMemModel
```

No barriers or synchronization.

### ATOMIC_RELEASE

[ref: #symbol-atomic-release]

```nim
ATOMIC_RELEASE {.importc: "__ATOMIC_RELEASE", nodecl.}: AtomMemModel
```

Barrier to sinking of code and synchronizes with acquire (or stronger) semantic loads from another thread.

### ATOMIC_SEQ_CST

[ref: #symbol-atomic-seq-cst]

```nim
ATOMIC_SEQ_CST {.importc: "__ATOMIC_SEQ_CST", nodecl.}: AtomMemModel
```

Full barrier in both directions and synchronizes with acquire loads and release stores in all threads.
