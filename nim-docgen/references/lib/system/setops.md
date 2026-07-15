---
source_hash: c91d1dfe560354f0
source_path: lib/system/setops.nim
---

# setops

[ref: #module-setops]

## Proc

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

### card

[ref: #symbol-card]

**Input:**
- `x: set[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `magic: "Card"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the cardinality of the set x, i.e. the number of elements in the set.

### contains

[ref: #symbol-contains]

One should overload this proc if one wants to overload the in operator.

**Input:**
- `x: set[T]`
- `y: T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "InSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

One should overload this proc if one wants to overload the in operator.

The parameters are in reverse order! a in b is a template for contains(b, a). This is because the unification algorithm that Nim uses for overload resolution works from left to right. But for the in operator that would be the wrong direction for this piece of code:

### excl

[ref: #symbol-excl]

Excludes element y from the set x.

**Input:**
- `x: var set[T]`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "Excl"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Excludes element y from the set x.

This is the same as x = x - {y}, but it might be more efficient.

### incl

[ref: #symbol-incl]

Includes element y in the set x.

**Input:**
- `x: var set[T]`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "Incl"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Includes element y in the set x.

This is the same as x = x + {y}, but it might be more efficient.

### len

[ref: #symbol-len]

**Input:**
- `x: set[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `magic: "Card"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

An alias for card(x).

## Template

### excl

[ref: #symbol-excl]

**Input:**
- `x: var set[T]`
- `y: set[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `callsite`

Excludes the set y from the set x.

### incl

[ref: #symbol-incl]

**Input:**
- `x: var set[T]`
- `y: set[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `callsite`

Includes the set y in the set x.
