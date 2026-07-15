---
source_hash: 018c2b626a6a35be
source_path: lib/std/enumutils.nim
---

# enumutils

[ref: #module-enumutils]

## Examples

```nim
type B = enum
  b0 = (10, "kb0")
  b1 = "kb1"
  b2
let b = B.low
assert b.symbolName == "b0"
assert $b == "kb0"
static: assert B.high.symbolName == "b2"
type C = enum # HoleyEnum
  c0 = -3
  c1 = 4
  c2 = 20
assert c1.symbolName == "c1"
```

```nim
type
  A = enum
    a0 = 2
    a1 = 4
    a2
  B[T] = enum
    b0 = 2
    b1 = 4
from std/sequtils import toSeq
assert A.toSeq == [a0, a1, a2]
assert B[float].toSeq == [B[float].b0, B[float].b1]
```

```nim
type
  A = enum # HoleyEnum
    a0 = -3
    a1 = 10
    a2
    a3 = (20, "f3Alt")
  B = enum # OrdinalEnum
    b0
    b1
    b2
  C = enum # OrdinalEnum
    c0 = 10
    c1
    c2
assert a2.symbolRank == 2
assert b2.symbolRank == 2
assert c2.symbolRank == 2
assert c2.ord == 12
assert a2.ord == 11
var invalid = 7.A
doAssertRaises(IndexDefect): discard invalid.symbolRank
```

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `E: typedesc[T]`

**Output:** `T`
**Generic parameters:** `T`, `E:type`

Iterates over an enum with holes.

## Macro

### genEnumCaseStmt

[ref: #symbol-genenumcasestmt]

**Input:**
- `typ: typedesc`
- `argSym: typed`
- `default: typed`
- `userMin: static[int]`
- `userMax: static[int]`
- `normalizer: static[proc (s: string): string]`

**Output:** `untyped`
**Generic parameters:** `typ:type`, `userMin:type`, `userMax:type`, `normalizer:type`

## Proc

### symbolName

[ref: #symbol-symbolname]

Returns the symbol name of an enum.

**Input:**
- `a: T`

**Output:** `string`
**Generic parameters:** `T`

Returns the symbol name of an enum.

This uses symbolRank.

## Template

### symbolRank

[ref: #symbol-symbolrank]

Returns the index in which a is listed in T.

**Input:**
- `a: T`

**Output:** `int`
**Generic parameters:** `T`

Returns the index in which a is listed in T.

The cost for a HoleyEnum is implementation defined, currently optimized for small enums, otherwise is O(T.enumLen).
