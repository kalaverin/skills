---
source_hash: 5b62c8f5f3f83af3
source_path: lib/system/dollars.nim
---

# dollars

[ref: #module-dollars]

$ is Nim's general way of spelling toString.

## Examples

```nim
import system/dollars
assert $0.1 == "0.1"
assert $(-2*3) == "-6"
```

```nim
doAssert $(typeof(42)) == "int"
doAssert $(typeof("Foo")) == "string"
static: doAssert $(typeof(@['A', 'B'])) == "seq[char]"
```

```nim
assert $'c' == "c"
```

```nim
$(1 .. 5) == "1 .. 5"
```

```nim
$(23, 45) == "(23, 45)"
$(a: 23, b: 45) == "(a: 23, b: 45)"
$() == "()"
```

```nim
$(@[23, 45].toOpenArray(0, 1)) == "[23, 45]"
```

```nim
$(@[23, 45]) == "@[23, 45]"
```

```nim
${23, 45} == "{23, 45}"
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `x: float | float32`

**Output:** `string`
**Generic parameters:** `x:type`

Outplace version of addFloat.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym0: int`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Outplace version of addInt.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym1: int8`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Outplace version of addInt.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym2: int16`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Outplace version of addInt.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym3: int32`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Outplace version of addInt.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym4: int64`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Outplace version of addInt.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym5: uint`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Outplace version of addInt.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym6: uint8`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Outplace version of addInt.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym7: uint16`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Outplace version of addInt.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym8: uint32`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Outplace version of addInt.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym9: uint64`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Outplace version of addInt.

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym10: `{}`(int, lit)`

**Output:** `string`
**Pragmas:** `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym11: `{}`(uint64, lit)`

**Output:** `string`
**Pragmas:** `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `$`

[ref: #symbol-]

**Input:**
- `x`gensym12: `{}`(int64, lit)`

**Output:** `string`
**Pragmas:** `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `$`

[ref: #symbol-]

**Input:**
- `x: bool`

**Output:** `string`
**Pragmas:** `magic: "BoolToStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The stringify operator for a boolean argument. Returns x converted to the string "false" or "true".

### `$`

[ref: #symbol-]

The stringify operator for a character argument. Returns x converted to a string.

**Input:**
- `x: char`

**Output:** `string`
**Pragmas:** `magic: "CharToStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The stringify operator for a character argument. Returns x converted to a string.

```
assert $'c' == "c"
```

### `$`

[ref: #symbol-]

**Input:**
- `x: cstring`

**Output:** `string`
**Pragmas:** `magic: "CStrToStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The stringify operator for a CString argument. Returns x converted to a string.

### `$`

[ref: #symbol-]

**Input:**
- `x: string`

**Output:** `string`
**Pragmas:** `magic: "StrToStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The stringify operator for a string argument. Returns x as it is. This operator is useful for generic code, so that $expr also works if expr is already a string.

### `$`

[ref: #symbol-]

The stringify operator for an enumeration argument. This works for any enumeration type thanks to compiler magic.

**Input:**
- `x: Enum`

**Output:** `string`
**Generic parameters:** `Enum`

**Pragmas:** `magic: "EnumToStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The stringify operator for an enumeration argument. This works for any enumeration type thanks to compiler magic.

If a $ operator for a concrete enumeration is provided, this is used instead. (In other words: *Overwriting* is possible.)

### `$`

[ref: #symbol-]

Returns the name of the given type.

**Input:**
- `t: typedesc`

**Output:** `string`
**Generic parameters:** `t:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the name of the given type.

For more procedures dealing with typedesc, see [typetraits module](typetraits.html).

```
doAssert $(typeof(42)) == "int"
doAssert $(typeof("Foo")) == "string"
static: doAssert $(typeof(@['A', 'B'])) == "seq[char]"
```

### `$`

[ref: #symbol-]

Generic $ operator for tuples that is lifted from the components of x. Example:

**Input:**
- `x: T`

**Output:** `string`
**Generic parameters:** `T`

Generic $ operator for tuples that is lifted from the components of x. Example:

```
$(23, 45) == "(23, 45)"
$(a: 23, b: 45) == "(a: 23, b: 45)"
$() == "()"
```

### `$`

[ref: #symbol-]

Generic $ operator for sets that is lifted from the components of x. Example:

**Input:**
- `x: set[T]`

**Output:** `string`
**Generic parameters:** `T`

Generic $ operator for sets that is lifted from the components of x. Example:

```
${23, 45} == "{23, 45}"
```

### `$`

[ref: #symbol-]

Generic $ operator for seqs that is lifted from the components of x. Example:

**Input:**
- `x: seq[T]`

**Output:** `string`
**Generic parameters:** `T`

Generic $ operator for seqs that is lifted from the components of x. Example:

```
$(@[23, 45]) == "@[23, 45]"
```

### `$`

[ref: #symbol-]

Generic $ operator for slices that is lifted from the components of x. Example:

**Input:**
- `x: HSlice[T, U]`

**Output:** `string`
**Generic parameters:** `T`, `U`

Generic $ operator for slices that is lifted from the components of x. Example:

```
$(1 .. 5) == "1 .. 5"
```

### `$`

[ref: #symbol-]

**Input:**
- `x: array[IDX, T]`

**Output:** `string`
**Generic parameters:** `T`, `IDX`

Generic $ operator for arrays that is lifted from the components.

### `$`

[ref: #symbol-]

Generic $ operator for openarrays that is lifted from the components of x. Example:

**Input:**
- `x: openArray[T]`

**Output:** `string`
**Generic parameters:** `T`

Generic $ operator for openarrays that is lifted from the components of x. Example:

```
$(@[23, 45].toOpenArray(0, 1)) == "[23, 45]"
```
