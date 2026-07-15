---
source_hash: 66f687f3ae338022
source_path: lib/pure/volatile.nim
---

# volatile

[ref: #module-volatile]

This module contains code for generating volatile loads and stores, which are useful in embedded and systems programming.

## Proc

### volatileLoad

[ref: #symbol-volatileload]

**Input:**
- `src: ptr T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`, `noinit`

Generates a volatile load of the value stored in the container src. Note that this only effects code generation on C like backends.

### volatileStore

[ref: #symbol-volatilestore]

**Input:**
- `dest: ptr T`
- `val: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Generates a volatile store into the container dest of the value val. Note that this only effects code generation on C like backends.
