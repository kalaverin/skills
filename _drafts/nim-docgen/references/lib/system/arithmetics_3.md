---
source_hash: f63c7223ff29ae5d
source_path: lib/system/arithmetics.nim
---

### `shl`

[ref: #symbol-shl]

**Input:**
- `x: uint64`
- `y: SomeInteger`

**Output:** `uint64`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShlI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shr`

[ref: #symbol-shr]

Computes the shift right operation of x and y, filling vacant bit positions with the sign bit. y (the number of positions to shift) is reduced to modulo sizeof(x) \* 8. That is 15'i32 shr 35 is equivalent to 15'i32 shr 3 bitmasked to always be in the range 0 ..< sizeof(int).

**Input:**
- `x: int`
- `y: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the shift right operation of x and y, filling vacant bit positions with the sign bit. y (the number of positions to shift) is reduced to modulo sizeof(x) \* 8. That is 15'i32 shr 35 is equivalent to 15'i32 shr 3 bitmasked to always be in the range 0 ..< sizeof(int).

**Note**: [Operator precedence](manual.html#syntax-precedence) is different than in *C*.

See also:

* [ashr func](#ashr,int,SomeInteger) for arithmetic shift right

### `shr`

[ref: #symbol-shr]

**Input:**
- `x: int8`
- `y: SomeInteger`

**Output:** `int8`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shr`

[ref: #symbol-shr]

**Input:**
- `x: int16`
- `y: SomeInteger`

**Output:** `int16`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shr`

[ref: #symbol-shr]

**Input:**
- `x: int32`
- `y: SomeInteger`

**Output:** `int32`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shr`

[ref: #symbol-shr]

**Input:**
- `x: int64`
- `y: SomeInteger`

**Output:** `int64`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shr`

[ref: #symbol-shr]

**Input:**
- `x: uint`
- `y: SomeInteger`

**Output:** `uint`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the shift right operation of x and y.

### `shr`

[ref: #symbol-shr]

**Input:**
- `x: uint8`
- `y: SomeInteger`

**Output:** `uint8`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shr`

[ref: #symbol-shr]

**Input:**
- `x: uint16`
- `y: SomeInteger`

**Output:** `uint16`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shr`

[ref: #symbol-shr]

**Input:**
- `x: uint32`
- `y: SomeInteger`

**Output:** `uint32`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shr`

[ref: #symbol-shr]

**Input:**
- `x: uint64`
- `y: SomeInteger`

**Output:** `uint64`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "BitxorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise xor of numbers x and y.

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "BitxorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "BitxorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "BitxorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "BitxorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `uint`
**Pragmas:** `magic: "BitxorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise xor of numbers x and y.

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "BitxorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "BitxorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "BitxorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "BitxorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ashr

[ref: #symbol-ashr]

Shifts right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off. y (the number of positions to shift) is reduced to modulo sizeof(x) \* 8. That is ashr(15'i32, 35) is equivalent to ashr(15'i32, 3).

**Input:**
- `x: int`
- `y: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Shifts right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off. y (the number of positions to shift) is reduced to modulo sizeof(x) \* 8. That is ashr(15'i32, 35) is equivalent to ashr(15'i32, 3).

Note that ashr is not an operator so use the normal function call syntax for it.

See also:

* [shr func](#shr,int,SomeInteger)

### ashr

[ref: #symbol-ashr]

**Input:**
- `x: int8`
- `y: SomeInteger`

**Output:** `int8`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ashr

[ref: #symbol-ashr]

**Input:**
- `x: int16`
- `y: SomeInteger`

**Output:** `int16`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ashr

[ref: #symbol-ashr]

**Input:**
- `x: int32`
- `y: SomeInteger`

**Output:** `int32`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ashr

[ref: #symbol-ashr]

**Input:**
- `x: int64`
- `y: SomeInteger`

**Output:** `int64`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dec

[ref: #symbol-dec]

Decrements the ordinal x by y.

**Input:**
- `x: var T`
- `y: V = 1`

**Output:** *(none)*
**Generic parameters:** `T`, `V`

**Pragmas:** `magic: "Dec"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Decrements the ordinal x by y.

If such a value does not exist, OverflowDefect is raised or a compile time error occurs. This is a short notation for: x = pred(x, y).

### inc

[ref: #symbol-inc]

Increments the ordinal x by y.

**Input:**
- `x: var T`
- `y: V = 1`

**Output:** *(none)*
**Generic parameters:** `T`, `V`

**Pragmas:** `magic: "Inc"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Increments the ordinal x by y.

If such a value does not exist, OverflowDefect is raised or a compile time error occurs. This is a short notation for: x = succ(x, y).

### pred

[ref: #symbol-pred]

Returns the y-th predecessor (default: 1) of the value x.

**Input:**
- `x: T`
- `y: V = 1`

**Output:** `T`
**Generic parameters:** `T`, `V`

**Pragmas:** `magic: "Pred"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the y-th predecessor (default: 1) of the value x.

If such a value does not exist, OverflowDefect is raised or a compile time error occurs.

### succ

[ref: #symbol-succ]

Returns the y-th successor (default: 1) of the value x.

**Input:**
- `x: T`
- `y: V = 1`

**Output:** `T`
**Generic parameters:** `T`, `V`

**Pragmas:** `magic: "Succ"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the y-th successor (default: 1) of the value x.

If such a value does not exist, OverflowDefect is raised or a compile time error occurs.

[Prev](arithmetics_2.md)
