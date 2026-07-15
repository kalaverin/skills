---
source_hash: 61ef55a63bbe9fcc
source_path: lib/system/iterators.nim
---

# iterators

[ref: #module-iterators]

Default iterators for some Nim types.

## Examples

```nim
type Foo = object
  x1: int
  x2: string
var a1 = Foo(x1: 12, x2: "abc")
var a2: Foo
for name, v1, v2 in fieldPairs(a1, a2):
  when name == "x2": v2 = v1
doAssert a2 == Foo(x1: 0, x2: "abc")
```

```nim
type
  Custom = object
    foo: string
    bar: bool
proc `$`(x: Custom): string =
  result = "Custom:"
  for name, value in x.fieldPairs:
    when value is bool:
      result.add("\n\t" & name & " is " & $value)
    else:
      result.add("\n\t" & name & " '" & value & "'")
```

```nim
var t1 = (1, "foo")
var t2 = default(typeof(t1))
for v1, v2 in fields(t1, t2): v2 = v1
doAssert t1 == t2
```

```nim
var t = (1, "foo")
for v in fields(t): v = default(typeof(v))
doAssert t == (0, "")
```

```nim
from std/sequtils import toSeq
assert toSeq("abc\0def".cstring) == @['a', 'b', 'c']
assert toSeq("abc".cstring) == @['a', 'b', 'c']
```

```nim
type Goo = enum g0 = 2, g1, g2
from std/sequtils import toSeq
assert Goo.toSeq == [g0, g1, g2]
```

```nim
from std/sugar import collect
var a = "abc\0def"
prepareMutation(a)
var b = a.cstring
let s = collect:
  for bi in mitems(b):
    if bi == 'b': bi = 'B'
    bi
assert s == @['a', 'B', 'c']
assert b == "aBc"
assert a == "aBc\0def"
```

## Iterator

### fieldPairs

[ref: #symbol-fieldpairs]

Iterates over every field of x returning their name and value.

**Input:**
- `x: T`

**Output:** `tuple[key: string, val: RootObj]`
**Generic parameters:** `T`

**Pragmas:** `magic: "FieldPairs"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over every field of x returning their name and value.

When you iterate over objects with different field types you have to use the compile time when instead of a runtime if to select the code you want to run for each type. To perform the comparison use the [is operator](manual.html#generics-is-operator). Another way to do the same without when is to leave the task of picking the appropriate code to a secondary proc which you overload for each field type and pass the value to.

**Warning:**
This really transforms the 'for' and unrolls the loop. The current implementation also has a bug that affects symbol binding in the loop body.

### fieldPairs

[ref: #symbol-fieldpairs]

Iterates over every field of x and y.

**Input:**
- `x: S`
- `y: T`

**Output:** `tuple[key: string, a, b: RootObj]`
**Generic parameters:** `S`, `T`

**Pragmas:** `magic: "FieldPairs"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over every field of x and y.

**Warning:**
This really transforms the 'for' and unrolls the loop. The current implementation also has a bug that affects symbol binding in the loop body.

### fields

[ref: #symbol-fields]

Iterates over every field of x.

**Input:**
- `x: T`

**Output:** `RootObj`
**Generic parameters:** `T`

**Pragmas:** `magic: "Fields"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over every field of x.

**Warning:**
This really transforms the 'for' and unrolls the loop. The current implementation also has a bug that affects symbol binding in the loop body.

### fields

[ref: #symbol-fields]

Iterates over every field of x and y.

**Input:**
- `x: S`
- `y: T`

**Output:** `tuple[key: string, val: RootObj]`
**Generic parameters:** `S`, `T`

**Pragmas:** `magic: "Fields"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over every field of x and y.

**Warning:**
This really transforms the 'for' and unrolls the loop. The current implementation also has a bug that affects symbol binding in the loop body.

### items

[ref: #symbol-items]

**Input:**
- `a: openArray[T]`

**Output:** `lent2 T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each item of a.

### items

[ref: #symbol-items]

**Input:**
- `a: openArray[T]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each item of a.

### items

[ref: #symbol-items]

**Input:**
- `a: array[IX, T]`

**Output:** `lent2 T`
**Generic parameters:** `IX`, `T`

**Pragmas:** `inline`

Iterates over each item of a.

### items

[ref: #symbol-items]

**Input:**
- `a: set[T]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each element of a. items iterates only over the elements that are really in the set (and not over the ones the set is able to hold).

### items

[ref: #symbol-items]

**Input:**
- `a: cstring`

**Output:** `char`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over each item of a.

### items

[ref: #symbol-items]

**Input:**
- `E: typedesc[T]`

**Output:** `T`
**Generic parameters:** `T`, `E:type`

Iterates over the values of E. See also enumutils.items for enums with holes.

### items

[ref: #symbol-items]

**Input:**
- `s: Slice[T]`

**Output:** `T`
**Generic parameters:** `T`

Iterates over the slice s, yielding each value between s.a and s.b (inclusively).

### items

[ref: #symbol-items]

**Input:**
- `a: seq[T]`

**Output:** `lent2 T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each item of a.

### items

[ref: #symbol-items]

**Input:**
- `a: string`

**Output:** `char`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over each item of a.

### mitems

[ref: #symbol-mitems]

**Input:**
- `a: var openArray[T]`

**Output:** `var T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each item of a so that you can modify the yielded value.

### mitems

[ref: #symbol-mitems]

**Input:**
- `a: var array[IX, T]`

**Output:** `var T`
**Generic parameters:** `IX`, `T`

**Pragmas:** `inline`

Iterates over each item of a so that you can modify the yielded value.

### mitems

[ref: #symbol-mitems]

**Input:**
- `a: var cstring`

**Output:** `var char`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over each item of a so that you can modify the yielded value.

### mitems

[ref: #symbol-mitems]

**Input:**
- `a: var seq[T]`

**Output:** `var T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each item of a so that you can modify the yielded value.

### mitems

[ref: #symbol-mitems]

**Input:**
- `a: var string`

**Output:** `var char`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over each item of a so that you can modify the yielded value.

### mpairs

[ref: #symbol-mpairs]

**Input:**
- `a: var openArray[T]`

**Output:** `tuple[key: int, val: var T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each item of a. Yields (index, a[index]) pairs. a[index] can be modified.

### mpairs

[ref: #symbol-mpairs]

**Input:**
- `a: var array[IX, T]`

**Output:** `tuple[key: IX, val: var T]`
**Generic parameters:** `IX`, `T`

**Pragmas:** `inline`

Iterates over each item of a. Yields (index, a[index]) pairs. a[index] can be modified.

### mpairs

[ref: #symbol-mpairs]

**Input:**
- `a: var seq[T]`

**Output:** `tuple[key: int, val: var T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each item of a. Yields (index, a[index]) pairs. a[index] can be modified.

### mpairs

[ref: #symbol-mpairs]

**Input:**
- `a: var string`

**Output:** `tuple[key: int, val: var char]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over each item of a. Yields (index, a[index]) pairs. a[index] can be modified.

### mpairs

[ref: #symbol-mpairs]

**Input:**
- `a: var cstring`

**Output:** `tuple[key: int, val: var char]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over each item of a. Yields (index, a[index]) pairs. a[index] can be modified.

### pairs

[ref: #symbol-pairs]

**Input:**
- `a: openArray[T]`

**Output:** `tuple[key: int, val: T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each item of a. Yields (index, a[index]) pairs.

### pairs

[ref: #symbol-pairs]

**Input:**
- `a: array[IX, T]`

**Output:** `tuple[key: IX, val: T]`
**Generic parameters:** `IX`, `T`

**Pragmas:** `inline`

Iterates over each item of a. Yields (index, a[index]) pairs.

### pairs

[ref: #symbol-pairs]

**Input:**
- `a: seq[T]`

**Output:** `tuple[key: int, val: T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each item of a. Yields (index, a[index]) pairs.

### pairs

[ref: #symbol-pairs]

**Input:**
- `a: string`

**Output:** `tuple[key: int, val: char]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over each item of a. Yields (index, a[index]) pairs.

### pairs

[ref: #symbol-pairs]

**Input:**
- `a: cstring`

**Output:** `tuple[key: int, val: char]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over each item of a. Yields (index, a[index]) pairs.
