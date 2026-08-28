---
source_hash: ea2d6f014d7bb717
source_path: lib/pure/concurrency/atomics.nim
---

# atomics

[ref: #module-atomics]

Types and operations for atomic operations and lockless algorithms.

Unstable API.

By default, C++ uses C11 atomic primitives. To use C++ std::atomic, -d:nimUseCppAtomics can be defined.

## Examples

```nim
import std/atomics
# Atomic
var loc: Atomic[int]
loc.store(4)
assert loc.load == 4
loc.store(2)
assert loc.load(moRelaxed) == 2
loc.store(9)
assert loc.load(moAcquire) == 9
loc.store(0, moRelease)
assert loc.load == 0

assert loc.exchange(7) == 0
assert loc.load == 7

var expected = 7
assert loc.compareExchange(expected, 5, moRelaxed, moRelaxed)
assert expected == 7
assert loc.load == 5

assert not loc.compareExchange(expected, 12, moRelaxed, moRelaxed)
assert expected == 5
assert loc.load == 5

assert loc.fetchAdd(1) == 5
assert loc.fetchAdd(2) == 6
assert loc.fetchSub(3) == 8

loc.atomicInc(1)
assert loc.load == 6

# AtomicFlag
var flag: AtomicFlag

assert not flag.testAndSet
assert flag.testAndSet
flag.clear(moRelaxed)
assert not flag.testAndSet
```

## Proc

### `+=`

[ref: #symbol-]

**Input:**
- `location: var Atomic[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Atomically increments the atomic integer by some value.

### `-=`

[ref: #symbol-]

**Input:**
- `location: var Atomic[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Atomically decrements the atomic integer by some value.

### atomicDec

[ref: #symbol-atomicdec]

**Input:**
- `location: var Atomic[T]`
- `value: T = 1`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Atomically decrements the atomic integer by some value.

### atomicInc

[ref: #symbol-atomicinc]

**Input:**
- `location: var Atomic[T]`
- `value: T = 1`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Atomically increments the atomic integer by some value.

### clear

[ref: #symbol-clear]

**Input:**
- `location: var AtomicFlag`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.clear(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically sets the value of the atomic flag to false.

### compareExchange

[ref: #symbol-compareexchange]

**Input:**
- `location: var Atomic[T]`
- `expected: var T`
- `desired: T`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.compare_exchange_strong(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically compares the value of the atomic object with the expected value and performs exchange with the desired one if equal or load if not. Returns true if the exchange was successful.

### compareExchange

[ref: #symbol-compareexchange]

**Input:**
- `location: var Atomic[T]`
- `expected: var T`
- `desired: T`
- `success: MemoryOrder`
- `failure: MemoryOrder`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.compare_exchange_strong(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as above, but allows for different memory orders for success and failure.

### compareExchangeWeak

[ref: #symbol-compareexchangeweak]

**Input:**
- `location: var Atomic[T]`
- `expected: var T`
- `desired: T`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.compare_exchange_weak(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as above, but is allowed to fail spuriously.

### compareExchangeWeak

[ref: #symbol-compareexchangeweak]

**Input:**
- `location: var Atomic[T]`
- `expected: var T`
- `desired: T`
- `success: MemoryOrder`
- `failure: MemoryOrder`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.compare_exchange_weak(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as above, but allows for different memory orders for success and failure.

### exchange

[ref: #symbol-exchange]

**Input:**
- `location: var Atomic[T]`
- `desired: T`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.exchange(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically replaces the value of the atomic object with the desired value and returns the old value.

### fence

[ref: #symbol-fence]

**Input:**
- `order: MemoryOrder`

**Output:** *(none)*
**Pragmas:** `importcpp: "std::atomic_thread_fence(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Ensures memory ordering without using atomic operations.

### fetchAdd

[ref: #symbol-fetchadd]

**Input:**
- `location: var Atomic[T]`
- `value: T`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.fetch_add(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically adds a value to the atomic integer and returns the original value.

### fetchAnd

[ref: #symbol-fetchand]

**Input:**
- `location: var Atomic[T]`
- `value: T`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.fetch_and(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically replaces the atomic integer with it's bitwise AND with the specified value and returns the original value.

### fetchOr

[ref: #symbol-fetchor]

**Input:**
- `location: var Atomic[T]`
- `value: T`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.fetch_or(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically replaces the atomic integer with it's bitwise OR with the specified value and returns the original value.

### fetchSub

[ref: #symbol-fetchsub]

**Input:**
- `location: var Atomic[T]`
- `value: T`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.fetch_sub(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically subtracts a value to the atomic integer and returns the original value.

### fetchXor

[ref: #symbol-fetchxor]

**Input:**
- `location: var Atomic[T]`
- `value: T`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.fetch_xor(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically replaces the atomic integer with it's bitwise XOR with the specified value and returns the original value.

### load

[ref: #symbol-load]

**Input:**
- `location: var Atomic[T]`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.load(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically obtains the value of the atomic object.

### signalFence

[ref: #symbol-signalfence]

**Input:**
- `order: MemoryOrder`

**Output:** *(none)*
**Pragmas:** `importcpp: "std::atomic_signal_fence(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Prevents reordering of accesses by the compiler as would fence, but inserts no CPU instructions for memory ordering.

### store

[ref: #symbol-store]

**Input:**
- `location: var Atomic[T]`
- `desired: T`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `importcpp: "#.store(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically replaces the value of the atomic object with the desired value.

### testAndSet

[ref: #symbol-testandset]

**Input:**
- `location: var AtomicFlag`
- `order: MemoryOrder = moSequentiallyConsistent`

**Output:** `bool`
**Pragmas:** `importcpp: "#.test_and_set(@)"`, `header: "<atomic>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Atomically sets the atomic flag to true and returns the original value.

## Type

### Atomic

[ref: #symbol-atomic]

```nim
Atomic[T] {.importcpp: "std::atomic", completeStruct.} = object
```

An atomic object with underlying type T.

### AtomicFlag

[ref: #symbol-atomicflag]

```nim
AtomicFlag {.importcpp: "std::atomic_flag", size: 1.} = object
```

An atomic boolean state.

### MemoryOrder

[ref: #symbol-memoryorder]

```nim
MemoryOrder {.importcpp: "std::memory_order".} = enum
  moRelaxed, ## No ordering constraints. Only the atomicity and ordering against
              ## other atomic operations is guaranteed.
  moConsume, ## This ordering is currently discouraged as it's semantics are
              ## being revised. Acquire operations should be preferred.
  moAcquire, ## When applied to a load operation, no reads or writes in the
              ## current thread can be reordered before this operation.
  moRelease, ## When applied to a store operation, no reads or writes in the
              ## current thread can be reorderd after this operation.
  moAcquireRelease, ## When applied to a read-modify-write operation, this behaves like
                     ## both an acquire and a release operation.
  moSequentiallyConsistent ## Behaves like Acquire when applied to load, like Release when
                           ## applied to a store and like AcquireRelease when applied to a
                           ## read-modify-write operation.
                           ## Also guarantees that all threads observe the same total ordering
                           ## with other moSequentiallyConsistent operations.
```

Specifies how non-atomic operations can be reordered around atomic operations.
