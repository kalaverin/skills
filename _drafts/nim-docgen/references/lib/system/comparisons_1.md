---
source_hash: 64a68082d80164b4
source_path: lib/system/comparisons.nim
---

# comparisons

[ref: #module-comparisons]

## Proc

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `x: int`
- `y: int`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Treats x and y as unsigned and compares them. Returns true if unsigned(x) < unsigned(y).

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `x: int`
- `y: int`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Treats x and y as unsigned and compares them. Returns true if unsigned(x) <= unsigned(y).

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: Enum`
- `y: Enum`

**Output:** `bool`
**Generic parameters:** `Enum`

**Pragmas:** `magic: "LeEnum"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: string`
- `y: string`

**Output:** `bool`
**Pragmas:** `magic: "LeStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two strings and returns true if x is lexicographically before y (uppercase letters come before lowercase letters).

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: char`
- `y: char`

**Output:** `bool`
**Pragmas:** `magic: "LeCh"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two chars and returns true if x is lexicographically before y (uppercase letters come before lowercase letters).

### `&lt;=`

[ref: #symbol-lt]

Returns true if x is a subset of y.

**Input:**
- `x: set[T]`
- `y: set[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "LeSet"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if x is a subset of y.

A subset x has all of its members in y and y doesn't necessarily have more members than x. That is, x can be equal to y.

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: bool`
- `y: bool`

**Output:** `bool`
**Pragmas:** `magic: "LeB"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: ref T`
- `y: ref T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "LePtr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: pointer`
- `y: pointer`

**Output:** `bool`
**Pragmas:** `magic: "LePtr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

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

### `==`

[ref: #symbol-]

**Input:**
- `x: Enum`
- `y: Enum`

**Output:** `bool`
**Generic parameters:** `Enum`

**Pragmas:** `magic: "EqEnum"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether values within the *same enum* have the same underlying value.

### `==`

[ref: #symbol-]

**Input:**
- `x: pointer`
- `y: pointer`

**Output:** `bool`
**Pragmas:** `magic: "EqRef"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks for equality between two pointer variables.

### `==`

[ref: #symbol-]

**Input:**
- `x: string`
- `y: string`

**Output:** `bool`
**Pragmas:** `magic: "EqStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks for equality between two string variables.

### `==`

[ref: #symbol-]

**Input:**
- `x: char`
- `y: char`

**Output:** `bool`
**Pragmas:** `magic: "EqCh"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks for equality between two char variables.

### `==`

[ref: #symbol-]

**Input:**
- `x: bool`
- `y: bool`

**Output:** `bool`
**Pragmas:** `magic: "EqB"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks for equality between two bool variables.

### `==`

[ref: #symbol-]

**Input:**
- `x: set[T]`
- `y: set[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "EqSet"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks for equality between two variables of type set.

### `==`

[ref: #symbol-]

**Input:**
- `x: ref T`
- `y: ref T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "EqRef"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks that two ref variables refer to the same item.

### `==`

[ref: #symbol-]

**Input:**
- `x: ptr T`
- `y: ptr T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "EqRef"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks that two ptr variables refer to the same item.

### `==`

[ref: #symbol-]

**Input:**
- `x: T`
- `y: T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "EqProc"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks that two proc variables refer to the same procedure.

### `==`

[ref: #symbol-]

**Input:**
- `x: string`
- `y: typeof(nil) | typeof(nil)`

**Output:** `bool`
**Generic parameters:** `y:type`

**Pragmas:** `error: "\'nil\' is invalid for \'string\'"`

### `==`

[ref: #symbol-]

**Input:**
- `x: typeof(nil) | typeof(nil)`
- `y: string`

**Output:** `bool`
**Generic parameters:** `x:type`

**Pragmas:** `error: "\'nil\' is invalid for \'string\'"`

### `==`

[ref: #symbol-]

**Input:**
- `x: int`
- `y: int`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two integers for equality.

### `==`

[ref: #symbol-]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two unsigned integers for equality.

### `==`

[ref: #symbol-]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Next](comparisons_2.md)
