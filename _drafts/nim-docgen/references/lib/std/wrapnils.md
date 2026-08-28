---
source_hash: bc380de9c34e9135
source_path: lib/std/wrapnils.nim
---

# wrapnils

[ref: #module-wrapnils]

This module allows evaluating expressions safely against the following conditions:

* nil dereferences
* field accesses with incorrect discriminant in case objects

default(T) is returned in those cases when evaluating an expression of type T. This simplifies code by reducing need for if-else branches.

Note: experimental module, unstable API.

## Examples

```nim
import std/wrapnils
type Foo = ref object
  x1: string
  x2: Foo
  x3: ref int

var f: Foo
assert ?.f.x2.x1 == "" # returns default value since `f` is nil

var f2 = Foo(x1: "a")
f2.x2 = f2
assert ?.f2.x1 == "a" # same as f2.x1 (no nil LHS in this chain)
assert ?.Foo(x1: "a").x1 == "a" # can use constructor inside

# when you know a sub-expression doesn't involve a `nil` (e.g. `f2.x2.x2`),
# you can scope it as follows:
assert ?.(f2.x2.x2).x3[] == 0

assert (?.f2.x2.x2).x3 == nil  # this terminates ?. early
```

```nim
import std/wrapnils
# ?. also allows case object
type B = object
  b0: int
  case cond: bool
  of false: discard
  of true:
    b1: float

var b = B(cond: false, b0: 3)
doAssertRaises(FieldDefect): discard b.b1 # wrong discriminant
doAssert ?.b.b1 == 0.0 # safe
b = B(cond: true, b1: 4.5)
doAssert ?.b.b1 == 4.5

# lvalue semantics are preserved:
if (let p = ?.b.b1.addr; p != nil): p[] = 4.7
doAssert b.b1 == 4.7
```

```nim
import std/options
type Foo = ref object
  x1: ref int
  x2: int
# `?.` can't distinguish between a valid vs invalid default value, but `??.` can:
var f1 = Foo(x1: int.new, x2: 2)
doAssert (??.f1.x1[]).get == 0 # not enough to tell when the chain was valid.
doAssert (??.f1.x1[]).isSome # a nil didn't occur in the chain
doAssert (??.f1.x2).get == 2

var f2: Foo
doAssert not (??.f2.x1[]).isSome # f2 was nil

doAssertRaises(UnpackDefect): discard (??.f2.x1[]).get
doAssert ?.f2.x1[] == 0 # in contrast, this returns default(int)
```

## Macro

### `?.`

[ref: #symbol-]

**Input:**
- `a: typed`

**Output:** `auto`
Transforms a into an expression that can be safely evaluated even in presence of intermediate nil pointers/references, in which case a default value is produced.

### `??.`

[ref: #symbol-]

**Input:**
- `a: typed`

**Output:** `Option`
**Generic parameters:** `Option`

Same as ?. but returns an Option.

## Proc

### `[]`

[ref: #symbol-]

**Input:**
- `a: Option[T]`
- `i: I`

**Output:** `auto`
**Generic parameters:** `T`, `I`

**Pragmas:** `inline`

See top-level example.

### `[]`

[ref: #symbol-]

**Input:**
- `a: Option[U]`

**Output:** `auto`
**Generic parameters:** `U`

**Pragmas:** `inline`

See top-level example.

## Template

### fakeDot

[ref: #symbol-fakedot]

**Input:**
- `a: Option`
- `b: `

**Output:** `untyped`
**Generic parameters:** `Option`

See top-level example.
