---
source_hash: 2ba8f613261c18d0
source_path: lib/system/repr_v2.nim
---

# repr_v2

[ref: #module-repr_v2]

## Examples

```nim
assert repr('c') == "'c'"
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

### repr

[ref: #symbol-repr]

**Input:**
- `x: NimNode`

**Output:** `string`
**Pragmas:** `magic: "Repr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym0: int`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym1: int8`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym2: int16`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym3: int32`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym4: int64`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym5: uint`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym6: uint8`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym7: uint16`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym8: uint32`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym9: uint64`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym10: float`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x`gensym11: float32`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as $x

### repr

[ref: #symbol-repr]

**Input:**
- `x: bool`

**Output:** `string`
**Pragmas:** `magic: "BoolToStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

repr for a boolean argument. Returns x converted to the string "false" or "true".

### repr

[ref: #symbol-repr]

repr for a character argument. Returns x converted to an escaped string.

**Input:**
- `x: char`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

repr for a character argument. Returns x converted to an escaped string.

```
assert repr('c') == "'c'"
```

### repr

[ref: #symbol-repr]

**Input:**
- `x: string | cstring`

**Output:** `string`
**Generic parameters:** `x:type`

**Pragmas:** `noSideEffect`, `raises: []`

**Effects:** `raises: `

repr for a string argument. Returns x converted to a quoted and escaped string.

### repr

[ref: #symbol-repr]

repr for an enumeration argument. This works for any enumeration type thanks to compiler magic.

**Input:**
- `x: Enum`

**Output:** `string`
**Generic parameters:** `Enum`

**Pragmas:** `magic: "EnumToStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

repr for an enumeration argument. This works for any enumeration type thanks to compiler magic.

If a repr operator for a concrete enumeration is provided, this is used instead. (In other words: *Overwriting* is possible.)

### repr

[ref: #symbol-repr]

**Input:**
- `p: pointer`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

repr of pointer as its hexadecimal value

### repr

[ref: #symbol-repr]

**Input:**
- `p: proc | iterator {.closure.}`

**Output:** `string`
**Generic parameters:** `p:type`

repr of a proc as its address

### repr

[ref: #symbol-repr]

Generic repr operator for tuples that is lifted from the components of x. Example:

**Input:**
- `x: T`

**Output:** `string`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `raises: []`

**Effects:** `raises: `

Generic repr operator for tuples that is lifted from the components of x. Example:

```
$(23, 45) == "(23, 45)"
$(a: 23, b: 45) == "(a: 23, b: 45)"
$() == "()"
```

### repr

[ref: #symbol-repr]

**Input:**
- `x: ref T | ptr T`

**Output:** `string`
**Generic parameters:** `T`, `x:type`

**Pragmas:** `noSideEffect`, `raises: []`

**Effects:** `raises: `

### repr

[ref: #symbol-repr]

Generic repr operator for sets that is lifted from the components of x. Example:

**Input:**
- `x: set[T]`

**Output:** `string`
**Generic parameters:** `T`

Generic repr operator for sets that is lifted from the components of x. Example:

```
${23, 45} == "{23, 45}"
```

### repr

[ref: #symbol-repr]

Generic repr operator for seqs that is lifted from the components of x. Example:

**Input:**
- `x: seq[T]`

**Output:** `string`
**Generic parameters:** `T`

Generic repr operator for seqs that is lifted from the components of x. Example:

```
$(@[23, 45]) == "@[23, 45]"
```

### repr

[ref: #symbol-repr]

**Input:**
- `x: array[IDX, T]`

**Output:** `string`
**Generic parameters:** `T`, `IDX`

Generic repr operator for arrays that is lifted from the components.

### repr

[ref: #symbol-repr]

Generic repr operator for openarrays that is lifted from the components of x. Example:

**Input:**
- `x: openArray[T]`

**Output:** `string`
**Generic parameters:** `T`

Generic repr operator for openarrays that is lifted from the components of x. Example:

```
$(@[23, 45].toOpenArray(0, 1)) == "[23, 45]"
```

### repr

[ref: #symbol-repr]

**Input:**
- `x: UncheckedArray[T]`

**Output:** `string`
**Generic parameters:** `T`

### reprDiscriminant

[ref: #symbol-reprdiscriminant]

**Input:**
- `e: int`

**Output:** `string`
**Pragmas:** `compilerproc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### repr

[ref: #symbol-repr]

**Input:**
- `x: T`

**Output:** `string`
**Generic parameters:** `T`

### repr

[ref: #symbol-repr]

**Input:**
- `t: typedesc`

**Output:** `string`
**Generic parameters:** `t:type`
