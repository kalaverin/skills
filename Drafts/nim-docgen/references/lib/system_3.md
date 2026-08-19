---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: int`
- `y: int`

**Output:** `bool`
**Pragmas:** `magic: "LeI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if x is less than or equal to y.

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `bool`
**Pragmas:** `magic: "LeI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `bool`
**Pragmas:** `magic: "LeI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `bool`
**Pragmas:** `magic: "LeI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `bool`
**Pragmas:** `magic: "LeI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `bool`
**Pragmas:** `magic: "LeU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if x <= y.

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `bool`
**Pragmas:** `magic: "LeU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `bool`
**Pragmas:** `magic: "LeU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `bool`
**Pragmas:** `magic: "LeU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `bool`
**Pragmas:** `magic: "LeU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `bool`
**Pragmas:** `magic: "LeF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: float`
- `y: float`

**Output:** `bool`
**Pragmas:** `magic: "LeF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: T`
- `y: T`

**Output:** `bool`
**Generic parameters:** `T`

Generic lexicographic <= operator for tuples that is lifted from the components of x and y. This implementation uses cmp.

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: Enum`
- `y: Enum`

**Output:** `bool`
**Generic parameters:** `Enum`

**Pragmas:** `magic: "LtEnum"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: string`
- `y: string`

**Output:** `bool`
**Pragmas:** `magic: "LtStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two strings and returns true if x is lexicographically before y (uppercase letters come before lowercase letters).

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: char`
- `y: char`

**Output:** `bool`
**Pragmas:** `magic: "LtCh"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two chars and returns true if x is lexicographically before y (uppercase letters come before lowercase letters).

### `&lt;`

[ref: #symbol-lt]

Returns true if x is a strict or proper subset of y.

**Input:**
- `x: set[T]`
- `y: set[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "LtSet"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if x is a strict or proper subset of y.

A strict or proper subset x has all of its members in y but y has more elements than y.

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: bool`
- `y: bool`

**Output:** `bool`
**Pragmas:** `magic: "LtB"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: ref T`
- `y: ref T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "LtPtr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: ptr T`
- `y: ptr T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "LtPtr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: pointer`
- `y: pointer`

**Output:** `bool`
**Pragmas:** `magic: "LtPtr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: int`
- `y: int`

**Output:** `bool`
**Pragmas:** `magic: "LtI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if x is less than y.

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `bool`
**Pragmas:** `magic: "LtI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `bool`
**Pragmas:** `magic: "LtI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `bool`
**Pragmas:** `magic: "LtI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `bool`
**Pragmas:** `magic: "LtI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `bool`
**Pragmas:** `magic: "LtU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if x < y.

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `bool`
**Pragmas:** `magic: "LtU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `bool`
**Pragmas:** `magic: "LtU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `bool`
**Pragmas:** `magic: "LtU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `bool`
**Pragmas:** `magic: "LtU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `bool`
**Pragmas:** `magic: "LtF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: float`
- `y: float`

**Output:** `bool`
**Pragmas:** `magic: "LtF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: T`
- `y: T`

**Output:** `bool`
**Generic parameters:** `T`

Generic lexicographic < operator for tuples that is lifted from the components of x and y. This implementation uses cmp.

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

### `*`

[ref: #symbol-]

**Input:**
- `x: set[T]`
- `y: set[T]`

**Output:** `set[T]`
**Generic parameters:** `T`

**Pragmas:** `magic: "MulSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This operator computes the intersection of two sets.

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


[Prev](system_2.md) | [Next](system_4.md)
