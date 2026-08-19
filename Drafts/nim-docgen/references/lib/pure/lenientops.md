---
source_hash: cfef61b8c1be694c
source_path: lib/pure/lenientops.nim
---

# lenientops

[ref: #module-lenientops]

This module offers implementations of common binary operations like +, -, \*, / and comparison operations, which work for mixed float/int operands. All operations convert the integer operand into the type of the float operand. For numerical expressions, the return type is always the type of the float involved in the expression, i.e., there is no auto conversion from float32 to float64.

**Note:** In general, auto-converting from int to float loses information, which is why these operators live in a separate module. Use with care.

Regarding binary comparison, this module only provides unequal operators. The equality operator == is omitted, because depending on the use case either casting to float or rounding to int might be preferred, and users should make an explicit choice.

## Proc

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `i: I`
- `f: F`

**Output:** `bool`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `f: F`
- `i: I`

**Output:** `bool`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `i: I`
- `f: F`

**Output:** `bool`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `f: F`
- `i: I`

**Output:** `bool`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `*`

[ref: #symbol-]

**Input:**
- `i: I`
- `f: F`

**Output:** `F`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `*`

[ref: #symbol-]

**Input:**
- `f: F`
- `i: I`

**Output:** `F`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `+`

[ref: #symbol-]

**Input:**
- `i: I`
- `f: F`

**Output:** `F`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `+`

[ref: #symbol-]

**Input:**
- `f: F`
- `i: I`

**Output:** `F`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `-`

[ref: #symbol-]

**Input:**
- `i: I`
- `f: F`

**Output:** `F`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `-`

[ref: #symbol-]

**Input:**
- `f: F`
- `i: I`

**Output:** `F`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `/`

[ref: #symbol-]

**Input:**
- `i: I`
- `f: F`

**Output:** `F`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`

### `/`

[ref: #symbol-]

**Input:**
- `f: F`
- `i: I`

**Output:** `F`
**Generic parameters:** `I`, `F`

**Pragmas:** `inline`
