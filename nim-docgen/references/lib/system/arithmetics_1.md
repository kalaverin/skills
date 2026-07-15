---
source_hash: f63c7223ff29ae5d
source_path: lib/system/arithmetics.nim
---

# arithmetics

[ref: #module-arithmetics]

## Proc

### `%%`

[ref: #symbol-]

Treats x and y as unsigned and compute the modulo of x and y.

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Treats x and y as unsigned and compute the modulo of x and y.

The result is truncated to fit into the result. This implements modulo arithmetic. No overflow errors are possible.

### `%%`

[ref: #symbol-]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `%%`

[ref: #symbol-]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `%%`

[ref: #symbol-]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `%%`

[ref: #symbol-]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*%`

[ref: #symbol-]

Treats x and y as unsigned and multiplies them.

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Treats x and y as unsigned and multiplies them.

The result is truncated to fit into the result. This implements modulo arithmetic. No overflow errors are possible.

### `*%`

[ref: #symbol-]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*%`

[ref: #symbol-]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*%`

[ref: #symbol-]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*%`

[ref: #symbol-]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*=`

[ref: #symbol-]

**Input:**
- `x: var T`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `noSideEffect`, `systemRaisesDefect`

Binary \*= operator for integers.

### `*=`

[ref: #symbol-]

**Input:**
- `x: var T`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `noSideEffect`, `systemRaisesDefect`

Multiplies in place a floating point number.

### `*`

[ref: #symbol-]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "MulI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Binary \* operator for an integer.

### `*`

[ref: #symbol-]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "MulI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "MulI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "MulI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "MulI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `uint`
**Pragmas:** `magic: "MulU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Binary \* operator for unsigned integers.

### `*`

[ref: #symbol-]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "MulU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "MulU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "MulU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "MulU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `magic: "MulF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: float`
- `y: float`

**Output:** `float`
**Pragmas:** `magic: "MulF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+%`

[ref: #symbol-]

Treats x and y as unsigned and adds them.

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Treats x and y as unsigned and adds them.

The result is truncated to fit into the result. This implements modulo arithmetic. No overflow errors are possible.

### `+%`

[ref: #symbol-]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+%`

[ref: #symbol-]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+%`

[ref: #symbol-]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+%`

[ref: #symbol-]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+=`

[ref: #symbol-]

**Input:**
- `x: var T`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "Inc"`, `noSideEffect`, `systemRaisesDefect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Increments an integer.

### `+=`

[ref: #symbol-]

**Input:**
- `x: var T`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `noSideEffect`

Increments in place a floating point number.

### `+`

[ref: #symbol-]

**Input:**
- `x: int`

**Output:** `int`
**Pragmas:** `magic: "UnaryPlusI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unary + operator for an integer. Has no effect.

### `+`

[ref: #symbol-]

**Input:**
- `x: int8`

**Output:** `int8`
**Pragmas:** `magic: "UnaryPlusI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: int16`

**Output:** `int16`
**Pragmas:** `magic: "UnaryPlusI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: int32`

**Output:** `int32`
**Pragmas:** `magic: "UnaryPlusI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: int64`

**Output:** `int64`
**Pragmas:** `magic: "UnaryPlusI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "AddI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Binary + operator for an integer.

### `+`

[ref: #symbol-]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "AddI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "AddI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "AddI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "AddI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `uint`
**Pragmas:** `magic: "AddU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Binary + operator for unsigned integers.

### `+`

[ref: #symbol-]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "AddU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "AddU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "AddU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "AddU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `magic: "UnaryPlusF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `magic: "AddF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: float`

**Output:** `float`
**Pragmas:** `magic: "UnaryPlusF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: float`
- `y: float`

**Output:** `float`
**Pragmas:** `magic: "AddF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-%`

[ref: #symbol-]

Treats x and y as unsigned and subtracts them.

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Treats x and y as unsigned and subtracts them.

The result is truncated to fit into the result. This implements modulo arithmetic. No overflow errors are possible.

### `-%`

[ref: #symbol-]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-%`

[ref: #symbol-]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-%`

[ref: #symbol-]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-%`

[ref: #symbol-]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-=`

[ref: #symbol-]

**Input:**
- `x: var T`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "Dec"`, `noSideEffect`, `systemRaisesDefect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Decrements an integer.

### `-=`

[ref: #symbol-]

**Input:**
- `x: var T`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `noSideEffect`, `systemRaisesDefect`

Decrements in place a floating point number.

### `-`

[ref: #symbol-]

**Input:**
- `x: int`

**Output:** `int`
**Pragmas:** `magic: "UnaryMinusI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unary - operator for an integer. Negates x.

### `-`

[ref: #symbol-]

**Input:**
- `x: int8`

**Output:** `int8`
**Pragmas:** `magic: "UnaryMinusI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: int16`

**Output:** `int16`
**Pragmas:** `magic: "UnaryMinusI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: int32`

**Output:** `int32`
**Pragmas:** `magic: "UnaryMinusI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: int64`

**Output:** `int64`
**Pragmas:** `magic: "UnaryMinusI64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "SubI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Binary - operator for an integer.

### `-`

[ref: #symbol-]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "SubI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "SubI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "SubI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "SubI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `uint`
**Pragmas:** `magic: "SubU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Binary - operator for unsigned integers.

### `-`

[ref: #symbol-]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "SubU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "SubU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "SubU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "SubU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Next](arithmetics_2.md)
