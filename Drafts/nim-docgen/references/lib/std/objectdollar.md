---
source_hash: a5501c130ffac5b7
source_path: lib/std/objectdollar.nim
---

# objectdollar

[ref: #module-objectdollar]

This module implements a generic $ operator to convert objects to strings.

## Examples

```nim
type Foo = object
  a, b: int
let x = Foo(a: 23, b: 45)
assert $x == "(a: 23, b: 45)"
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `x: T`

**Output:** `string`
**Generic parameters:** `T`

Generic $ operator for objects with similar output to $ for named tuples.
