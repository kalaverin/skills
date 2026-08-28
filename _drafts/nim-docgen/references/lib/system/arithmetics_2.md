---
source_hash: f63c7223ff29ae5d
source_path: lib/system/arithmetics.nim
---

### `-`

[ref: #symbol-]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `magic: "UnaryMinusF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `magic: "SubF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: float`

**Output:** `float`
**Pragmas:** `magic: "UnaryMinusF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: float`
- `y: float`

**Output:** `float`
**Pragmas:** `magic: "SubF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `/%`

[ref: #symbol-]

Treats x and y as unsigned and divides them.

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Treats x and y as unsigned and divides them.

The result is truncated to fit into the result. This implements modulo arithmetic. No overflow errors are possible.

### `/%`

[ref: #symbol-]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `/%`

[ref: #symbol-]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `/%`

[ref: #symbol-]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `/%`

[ref: #symbol-]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `/=`

[ref: #symbol-]

**Input:**
- `x: var float64`
- `y: float64`

**Output:** *(none)*
**Pragmas:** `inline`, `noSideEffect`, `systemRaisesDefect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Divides in place a floating point number.

### `/=`

[ref: #symbol-]

**Input:**
- `x: var T`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `noSideEffect`, `systemRaisesDefect`

Divides in place a floating point number.

### `/`

[ref: #symbol-]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `magic: "DivF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `/`

[ref: #symbol-]

**Input:**
- `x: float`
- `y: float`

**Output:** `float`
**Pragmas:** `magic: "DivF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise and of numbers x and y.

### `and`

[ref: #symbol-and]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `uint`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise and of numbers x and y.

### `and`

[ref: #symbol-and]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

Computes the integer division.

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "DivI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the integer division.

This is roughly the same as math.trunc(x/y).int.

### `div`

[ref: #symbol-div]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "DivI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "DivI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "DivI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "DivI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `uint`
**Pragmas:** `magic: "DivU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the integer division for unsigned integers. This is roughly the same as trunc(x/y).

### `div`

[ref: #symbol-div]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "DivU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "DivU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "DivU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "DivU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `mod`

[ref: #symbol-mod]

Computes the integer modulo operation (remainder).

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "ModI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the integer modulo operation (remainder).

This is the same as x - (x div y) \* y.

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "ModI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "ModI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "ModI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "ModI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `uint`
**Pragmas:** `magic: "ModU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the integer modulo operation (remainder) for unsigned integers. This is the same as x - (x div y) \* y.

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "ModU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "ModU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "ModU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "ModU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `not`

[ref: #symbol-not]

**Input:**
- `x: int`

**Output:** `int`
**Pragmas:** `magic: "BitnotI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise complement of the integer x.

### `not`

[ref: #symbol-not]

**Input:**
- `x: int8`

**Output:** `int8`
**Pragmas:** `magic: "BitnotI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `not`

[ref: #symbol-not]

**Input:**
- `x: int16`

**Output:** `int16`
**Pragmas:** `magic: "BitnotI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `not`

[ref: #symbol-not]

**Input:**
- `x: int32`

**Output:** `int32`
**Pragmas:** `magic: "BitnotI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `not`

[ref: #symbol-not]

**Input:**
- `x: int64`

**Output:** `int64`
**Pragmas:** `magic: "BitnotI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `not`

[ref: #symbol-not]

**Input:**
- `x: uint`

**Output:** `uint`
**Pragmas:** `magic: "BitnotI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise complement of the integer x.

### `not`

[ref: #symbol-not]

**Input:**
- `x: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "BitnotI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `not`

[ref: #symbol-not]

**Input:**
- `x: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "BitnotI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `not`

[ref: #symbol-not]

**Input:**
- `x: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "BitnotI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `not`

[ref: #symbol-not]

**Input:**
- `x: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "BitnotI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `or`

[ref: #symbol-or]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "BitorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise or of numbers x and y.

### `or`

[ref: #symbol-or]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "BitorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `or`

[ref: #symbol-or]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "BitorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `or`

[ref: #symbol-or]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "BitorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `or`

[ref: #symbol-or]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "BitorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `or`

[ref: #symbol-or]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `uint`
**Pragmas:** `magic: "BitorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise or of numbers x and y.

### `or`

[ref: #symbol-or]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "BitorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `or`

[ref: #symbol-or]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "BitorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `or`

[ref: #symbol-or]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "BitorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `or`

[ref: #symbol-or]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "BitorI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shl`

[ref: #symbol-shl]

Computes the shift left operation of x and y. y (the number of positions to shift) is reduced to modulo sizeof(x) \* 8. That is 15'i32 shl 35 is equivalent to 15'i32 shl 3.

**Input:**
- `x: int`
- `y: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShlI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the shift left operation of x and y. y (the number of positions to shift) is reduced to modulo sizeof(x) \* 8. That is 15'i32 shl 35 is equivalent to 15'i32 shl 3.

**Note**: [Operator precedence](manual.html#syntax-precedence) is different than in *C*.

### `shl`

[ref: #symbol-shl]

**Input:**
- `x: int8`
- `y: SomeInteger`

**Output:** `int8`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShlI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shl`

[ref: #symbol-shl]

**Input:**
- `x: int16`
- `y: SomeInteger`

**Output:** `int16`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShlI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shl`

[ref: #symbol-shl]

**Input:**
- `x: int32`
- `y: SomeInteger`

**Output:** `int32`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShlI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shl`

[ref: #symbol-shl]

**Input:**
- `x: int64`
- `y: SomeInteger`

**Output:** `int64`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShlI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shl`

[ref: #symbol-shl]

**Input:**
- `x: uint`
- `y: SomeInteger`

**Output:** `uint`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShlI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the shift left operation of x and y.

### `shl`

[ref: #symbol-shl]

**Input:**
- `x: uint8`
- `y: SomeInteger`

**Output:** `uint8`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShlI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shl`

[ref: #symbol-shl]

**Input:**
- `x: uint16`
- `y: SomeInteger`

**Output:** `uint16`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShlI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shl`

[ref: #symbol-shl]

**Input:**
- `x: uint32`
- `y: SomeInteger`

**Output:** `uint32`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "ShlI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Prev](arithmetics_1.md) | [Next](arithmetics_3.md)
