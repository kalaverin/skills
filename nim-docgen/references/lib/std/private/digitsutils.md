---
source_hash: f2a88dc8673851e9
source_path: lib/std/private/digitsutils.nim
---

# digitsutils

[ref: #module-digitsutils]

## Examples

```nim
var s = "foo"
s.addInt(45)
assert s == "foo45"
```

## Proc

### addInt

[ref: #symbol-addint]

**Input:**
- `result: var string`
- `x: uint64`

**Output:** *(none)*
**Pragmas:** `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### addInt

[ref: #symbol-addint]

**Input:**
- `result: var string`
- `x: int64`

**Output:** *(none)*
**Pragmas:** `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts integer to its string representation and appends it to result.

### addInt

[ref: #symbol-addint]

**Input:**
- `result: var string`
- `x: int`

**Output:** *(none)*
**Pragmas:** `inline`, `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### trailingZeros2Digits

[ref: #symbol-trailingzeros2digits]

**Input:**
- `digits: uint32`

**Output:** `int`
**Pragmas:** `inline`, `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### utoa2Digits

[ref: #symbol-utoa2digits]

**Input:**
- `buf: var openArray[char]`
- `pos: int`
- `digits: uint32`

**Output:** *(none)*
**Pragmas:** `inline`, `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `
