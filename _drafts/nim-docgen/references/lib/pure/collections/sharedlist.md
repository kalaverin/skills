---
source_hash: 73e580f8f0dedb0f
source_path: lib/pure/collections/sharedlist.nim
---

# sharedlist

[ref: #module-sharedlist]

Shared list support.

Unstable API.

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `x: var SharedList[A]`

**Output:** `A`
**Generic parameters:** `A`

## Proc

### add

[ref: #symbol-add]

**Input:**
- `x: var SharedList[A]`
- `y: A`

**Output:** *(none)*
**Generic parameters:** `A`

### clear

[ref: #symbol-clear]

**Input:**
- `t: var SharedList[A]`

**Output:** *(none)*
**Generic parameters:** `A`

### deinitSharedList

[ref: #symbol-deinitsharedlist]

**Input:**
- `t: var SharedList[A]`

**Output:** *(none)*
**Generic parameters:** `A`

### init

[ref: #symbol-init]

**Input:**
- `t: var SharedList[A]`

**Output:** *(none)*
**Generic parameters:** `A`

### iterAndMutate

[ref: #symbol-iterandmutate]

Iterates over the list. If action returns true, the current item is removed from the list.

**Input:**
- `x: var SharedList[A]`
- `action: proc (x: A): bool`

**Output:** *(none)*
**Generic parameters:** `A`

Iterates over the list. If action returns true, the current item is removed from the list.

**Warning:**
It may not preserve the element order after some modifications.

## Type

### SharedList

[ref: #symbol-sharedlist]

```nim
SharedList[A] = object
  lock*: Lock
```

generic shared list
