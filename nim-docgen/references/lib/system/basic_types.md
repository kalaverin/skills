---
source_hash: dd8238b0d87d9bc5
source_path: lib/system/basic_types.nim
---

# basic_types

[ref: #module-basic_types]

## Const

### off

[ref: #symbol-off]

```nim
off = false
```

Alias for false.

### on

[ref: #symbol-on]

```nim
on = true
```

Alias for true.

## Proc

### `and`

[ref: #symbol-and]

Boolean and; returns true if x == y == true (if both arguments are true).

**Input:**
- `x: bool`
- `y: bool`

**Output:** `bool`
**Pragmas:** `magic: "And"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Boolean and; returns true if x == y == true (if both arguments are true).

Evaluation is lazy: if x is false, y will not even be evaluated.

### `not`

[ref: #symbol-not]

**Input:**
- `x: bool`

**Output:** `bool`
**Pragmas:** `magic: "Not"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Boolean not; returns true if x == false.

### `or`

[ref: #symbol-or]

Boolean or; returns true if not (not x and not y) (if any of the arguments is true).

**Input:**
- `x: bool`
- `y: bool`

**Output:** `bool`
**Pragmas:** `magic: "Or"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Boolean or; returns true if not (not x and not y) (if any of the arguments is true).

Evaluation is lazy: if x is true, y will not even be evaluated.

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: bool`
- `y: bool`

**Output:** `bool`
**Pragmas:** `magic: "Xor"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Boolean exclusive or; returns true if x != y (if either argument is true while the other is false).

## Type

### `ptr`

[ref: #symbol-ptr]

```nim
ptr[T] {.magic: Pointer.}
```

Built-in generic untraced pointer type.

### `ref`

[ref: #symbol-ref]

```nim
ref[T] {.magic: Pointer.}
```

Built-in generic traced pointer type.

### any

[ref: #symbol-any]

```nim
any {.deprecated: "Deprecated since v1.5; Use auto instead.".} = distinct auto
```

Deprecated; Use auto instead. See <https://github.com/nim-lang/RFCs/issues/281>

### auto

[ref: #symbol-auto]

```nim
auto {.magic: Expr.}
```

Meta type for automatic type determination.

### bool

[ref: #symbol-bool]

```nim
bool {.magic: "Bool".} = enum
  false = 0, true = 1
```

Built-in boolean type.

### char

[ref: #symbol-char]

```nim
char {.magic: Char.}
```

Built-in 8 bit character type (unsigned).

### cstring

[ref: #symbol-cstring]

```nim
cstring {.magic: Cstring.}
```

Built-in cstring (*compatible string*) type.

### float

[ref: #symbol-float]

```nim
float {.magic: Float.}
```

Default floating point type.

### float32

[ref: #symbol-float32]

```nim
float32 {.magic: Float32.}
```

32 bit floating point type.

### float64

[ref: #symbol-float64]

```nim
float64 {.magic: Float.}
```

64 bit floating point type.

### int

[ref: #symbol-int]

```nim
int {.magic: Int.}
```

Default integer type; bitwidth depends on architecture, but is always the same as a pointer.

### int16

[ref: #symbol-int16]

```nim
int16 {.magic: Int16.}
```

Signed 16 bit integer type.

### int32

[ref: #symbol-int32]

```nim
int32 {.magic: Int32.}
```

Signed 32 bit integer type.

### int64

[ref: #symbol-int64]

```nim
int64 {.magic: Int64.}
```

Signed 64 bit integer type.

### int8

[ref: #symbol-int8]

```nim
int8 {.magic: Int8.}
```

Signed 8 bit integer type.

### pointer

[ref: #symbol-pointer]

```nim
pointer {.magic: Pointer.}
```

Built-in pointer type, use the addr operator to get a pointer to a variable.

### SomeFloat

[ref: #symbol-somefloat]

```nim
SomeFloat = float | float32 | float64
```

Type class matching all floating point number types.

### SomeInteger

[ref: #symbol-someinteger]

```nim
SomeInteger = SomeSignedInt | SomeUnsignedInt
```

Type class matching all integer types.

### SomeNumber

[ref: #symbol-somenumber]

```nim
SomeNumber = SomeInteger | SomeFloat
```

Type class matching all number types.

### SomeOrdinal

[ref: #symbol-someordinal]

```nim
SomeOrdinal = int | int8 | int16 | int32 | int64 | bool | enum | uint | uint8 |
    uint16 |
    uint32 |
    uint64
```

Type class matching all ordinal types; however this includes enums with holes. See also Ordinal

### SomeSignedInt

[ref: #symbol-somesignedint]

```nim
SomeSignedInt = int | int8 | int16 | int32 | int64
```

Type class matching all signed integer types.

### SomeUnsignedInt

[ref: #symbol-someunsignedint]

```nim
SomeUnsignedInt = uint | uint8 | uint16 | uint32 | uint64
```

Type class matching all unsigned integer types.

### string

[ref: #symbol-string]

```nim
string {.magic: String.}
```

Built-in string type.

### typed

[ref: #symbol-typed]

```nim
typed {.magic: Stmt.}
```

Meta type to denote an expression that is resolved (for templates).

### typedesc

[ref: #symbol-typedesc]

```nim
typedesc {.magic: TypeDesc.}
```

Meta type to denote a type description.

### uint

[ref: #symbol-uint]

```nim
uint {.magic: UInt.}
```

Unsigned default integer type.

### uint16

[ref: #symbol-uint16]

```nim
uint16 {.magic: UInt16.}
```

Unsigned 16 bit integer type.

### uint32

[ref: #symbol-uint32]

```nim
uint32 {.magic: UInt32.}
```

Unsigned 32 bit integer type.

### uint64

[ref: #symbol-uint64]

```nim
uint64 {.magic: UInt64.}
```

Unsigned 64 bit integer type.

### uint8

[ref: #symbol-uint8]

```nim
uint8 {.magic: UInt8.}
```

Unsigned 8 bit integer type.

### untyped

[ref: #symbol-untyped]

```nim
untyped {.magic: Expr.}
```

Meta type to denote an expression that is not resolved (for templates).

### void

[ref: #symbol-void]

```nim
void {.magic: "VoidType".}
```

Meta type to denote the absence of any type.
