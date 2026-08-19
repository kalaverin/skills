---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

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

### `+`

[ref: #symbol-]

**Input:**
- `x: set[T]`
- `y: set[T]`

**Output:** `set[T]`
**Generic parameters:** `T`

**Pragmas:** `magic: "PlusSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This operator computes the union of two sets.

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

### `-`

[ref: #symbol-]

**Input:**
- `x: set[T]`
- `y: set[T]`

**Output:** `set[T]`
**Generic parameters:** `T`

**Pragmas:** `magic: "MinusSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This operator computes the difference of two sets.

### `-`

[ref: #symbol-]

**Input:**
- `a: AllocStats`
- `b: AllocStats`

**Output:** `AllocStats`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `..`

[ref: #symbol-]

Binary slice operator that constructs an interval [a, b], both a and b are inclusive.

**Input:**
- `a: sink T`
- `b: sink U`

**Output:** `HSlice[T, U]`
**Generic parameters:** `T`, `U`

**Pragmas:** `noSideEffect`, `inline`, `magic: "DotDot"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Binary slice operator that constructs an interval [a, b], both a and b are inclusive.

Slices can also be used in the set constructor and in ordinal case statements, but then they are special-cased by the compiler.

```
let a = [10, 20, 30, 40, 50]
echo a[2 .. 3] # @[30, 40]
```

### `..`

[ref: #symbol-]

Unary slice operator that constructs an interval [default(int), b].

**Input:**
- `b: sink T`

**Output:** `HSlice[int, T]`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `inline`, `magic: "DotDot"`, `deprecated: "replace `..b` with `0..b`"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unary slice operator that constructs an interval [default(int), b].

```
let a = [10, 20, 30, 40, 50]
echo a[.. 2] # @[10, 20, 30]
```

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

### `/`

[ref: #symbol-]

Division of integers that results in a float.

**Input:**
- `x: int`
- `y: int`

**Output:** `float`
**Pragmas:** `inline`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Division of integers that results in a float.

```
echo 7 / 5 # => 1.4
```

See also:

* [div](system.html#div,int,int)
* [mod](system.html#mod,int,int)

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


[Prev](system_3.md) | [Next](system_5.md)
