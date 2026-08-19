---
source_hash: 2323233bd80a530f
source_path: lib/std/formatfloat.nim
---

# formatfloat

[ref: #module-formatfloat]

This module implements formatting floats as strings.

## Examples

```nim
var
  s = "foo:"
  b = 45.67
s.addFloat(45.67)
assert s == "foo:45.67"
```

## Proc

### addFloat

[ref: #symbol-addfloat]

**Input:**
- `result: var string`
- `x: float | float32`

**Output:** *(none)*
**Generic parameters:** `x:type`

**Pragmas:** `inline`

Converts float to its string representation and appends it to result.

### addFloatRoundtrip

[ref: #symbol-addfloatroundtrip]

**Input:**
- `result: var string`
- `x: float | float32`

**Output:** *(none)*
**Generic parameters:** `x:type`

### addFloatSprintf

[ref: #symbol-addfloatsprintf]

**Input:**
- `result: var string`
- `x: float`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### writeFloatToBuffer

[ref: #symbol-writefloattobuffer]

**Input:**
- `buf: var array[65, char]`
- `value: BiggestFloat | float32`

**Output:** `int`
**Generic parameters:** `value:type`

**Pragmas:** `inline`

### writeFloatToBufferRoundtrip

[ref: #symbol-writefloattobufferroundtrip]

This is the implementation to format floats.

**Input:**
- `buf: var array[65, char]`
- `value: BiggestFloat`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This is the implementation to format floats.

returns the amount of bytes written to buf not counting the terminating '0' character.

### writeFloatToBufferRoundtrip

[ref: #symbol-writefloattobufferroundtrip]

**Input:**
- `buf: var array[65, char]`
- `value: float32`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### writeFloatToBufferSprintf

[ref: #symbol-writefloattobuffersprintf]

This is the implementation to format floats.

**Input:**
- `buf: var array[65, char]`
- `value: BiggestFloat`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This is the implementation to format floats.

returns the amount of bytes written to buf not counting the terminating '0' character.
