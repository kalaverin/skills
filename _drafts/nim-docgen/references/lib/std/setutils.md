---
source_hash: f06063ba4927c983
source_path: lib/std/setutils.nim
---

# setutils

[ref: #module-setutils]

This module adds functionality for the built-in set type.

# [See also](#see-also)

* [std/packedsets](packedsets.html)
* [std/sets](sets.html)

## Examples

```nim
assert {1, 2, 3} -+- {2, 3, 4} == {1, 4}
```

```nim
type A = enum
  a0, a1, a2, a3
var s = {a0, a3}
s[a0] = false
s[a1] = false
assert s == {a3}
s[a2] = true
s[a3] = true
assert s == {a2, a3}
```

```nim
type Colors = enum
  red, green = 3, blue
assert complement({red, blue}) == {green}
assert complement({red, green, blue}).card == 0
assert complement({range[0..10](0), 1, 2, 3}) == {range[0..10](4), 5, 6, 7, 8, 9, 10}
assert complement({'0'..'9'}) == {0.char..255.char} - {'0'..'9'}
```

```nim
assert bool.fullSet == {true, false}
type A = range[1..3]
assert A.fullSet == {1.A, 2, 3}
assert int8.fullSet.len == 256
```

```nim
assert symmetricDifference({1, 2, 3}, {2, 3, 4}) == {1, 4}
```

```nim
var x = {1, 2, 3}
x.toggle({2, 3, 4})
assert x == {1, 4}
```

```nim
assert "helloWorld".toSet == {'W', 'd', 'e', 'h', 'l', 'o', 'r'}
assert toSet([10u16, 20, 30]) == {10u16, 20, 30}
assert [30u8, 100, 10].toSet == {10u8, 30, 100}
assert toSet(@[1321i16, 321, 90]) == {90i16, 321, 1321}
assert toSet([false]) == {false}
assert toSet(0u8..10) == {0u8..10}
```

## Proc

### `-+-`

[ref: #symbol-]

**Input:**
- `x: set[T]`
- `y: set[T]`

**Output:** `set[T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Operator alias for symmetricDifference.

### `[]=`

[ref: #symbol-]

**Input:**
- `t: var set[T]`
- `key: T`
- `val: bool`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Syntax sugar for if val: t.incl key else: t.excl key

### complement

[ref: #symbol-complement]

**Input:**
- `s: set[T]`

**Output:** `set[T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the set complement of a.

### fullSet

[ref: #symbol-fullset]

**Input:**
- `U: typedesc[T]`

**Output:** `set[T]`
**Generic parameters:** `T`, `U:type`

**Pragmas:** `inline`

Returns a set containing all elements in U.

### symmetricDifference

[ref: #symbol-symmetricdifference]

**Input:**
- `x: set[T]`
- `y: set[T]`

**Output:** `set[T]`
**Generic parameters:** `T`

**Pragmas:** `magic: "XorSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This operator computes the symmetric difference of two sets, equivalent to but more efficient than x + y - x \* y or (x - y) + (y - x).

### toggle

[ref: #symbol-toggle]

**Input:**
- `x: var set[T]`
- `y: set[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Toggles the existence of each value of y in x. If any element in y is also in x, it is excluded from x; otherwise it is included. Equivalent to x = symmetricDifference(x, y).

## Template

### toSet

[ref: #symbol-toset]

**Input:**
- `iter: untyped`

**Output:** `untyped`
Returns a built-in set from the elements of the iterable iter.
