---
source_hash: 794ae9f402085998
source_path: lib/pure/options.nim
---

# options

[ref: #module-options]

This module implements types which encapsulate an optional value.

A value of type Option[T] either contains a value x (represented as some(x)) or is empty (none(T)).

This can be useful when you have a value that can be present or not. The absence of a value is often represented by nil, but that is not always available, nor is it always a good solution.

# [Basic usage](#basic-usage)

Let's start with an example: a procedure that finds the index of a character in a string.

The get operation demonstrated above returns the underlying value, or raises UnpackDefect if there is no value. Note that UnpackDefect inherits from system.Defect and should therefore never be caught. Instead, rely on checking if the option contains a value with the [isSome](#isSome,Option[T]) and [isNone](#isNone,Option[T]) procs.

# [Pattern matching](#pattern-matching)

**Note:**
This requires the [fusion](https://github.com/nim-lang/fusion) package.

[fusion/matching](https://nim-lang.github.io/fusion/src/fusion/matching.html) supports pattern matching on Options, with the Some(<pattern>) and None() patterns.

```
{.experimental: "caseStmtMacros".}

import fusion/matching

case some(42)
of Some(@a):
  assert a == 42
of None():
  assert false

assertMatch(some(some(none(int))), Some(Some(None())))
```

## Examples

```nim
import std/options
proc find(haystack: string, needle: char): Option[int] =
  for i, c in haystack:
    if c == needle:
      return some(i)
  return none(int)  # This line is actually optional,
                    # because the default is empty

let found = "abc".find('c')
assert found.isSome and found.get() == 2
```

```nim
{.experimental: "caseStmtMacros".}

import fusion/matching

case some(42)
of Some(@a):
  assert a == 42
of None():
  assert false

assertMatch(some(some(none(int))), Some(Some(None())))
```

```nim
assert $some(42) == "some(42)"
assert $none(int) == "none(int)"
```

```nim
let
  a = some(42)
  b = none(int)
  c = some(42)
  d = none(int)

assert a == c
assert b == d
assert not (a == b)
```

```nim
proc isEven(x: int): bool =
  x mod 2 == 0

assert some(42).filter(isEven) == some(42)
assert none(int).filter(isEven) == none(int)
assert some(-11).filter(isEven) == none(int)
```

```nim
proc doublePositives(x: int): Option[int] =
  if x > 0:
    some(2 * x)
  else:
    none(int)

assert some(42).flatMap(doublePositives) == some(84)
assert none(int).flatMap(doublePositives) == none(int)
assert some(-11).flatMap(doublePositives) == none(int)
```

```nim
assert flatten(some(some(42))) == some(42)
assert flatten(none(Option[int])) == none(int)
```

```nim
assert some(42).get == 42
doAssertRaises(UnpackDefect):
  echo none(string).get
```

```nim
assert some(42).get(9999) == 42
assert none(int).get(9999) == 9999
```

```nim
var
  a = some(42)
  b = none(string)
inc(a.get)
assert a.get == 43
doAssertRaises(UnpackDefect):
  echo b.get
```

```nim
assert not some(42).isNone
assert none(string).isNone
```

```nim
assert some(42).isSome
assert not none(string).isSome
```

```nim
proc isEven(x: int): bool =
  x mod 2 == 0

assert some(42).map(isEven) == some(true)
assert none(int).map(isEven) == none(bool)
```

```nim
var d = 0
proc saveDouble(x: int) =
  d = 2 * x

none(int).map(saveDouble)
assert d == 0
some(42).map(saveDouble)
assert d == 84
```

```nim
assert none(int).isNone
```

```nim
type
  Foo = ref object
    a: int
    b: string

assert option[Foo](nil).isNone
assert option(42).isSome
```

```nim
let a = some("abc")

assert a.isSome
assert a.get == "abc"
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `self: Option[T]`

**Output:** `string`
**Generic parameters:** `T`

Get the string representation of the Option.

### `==`

[ref: #symbol-]

**Input:**
- `a: Option[T]`
- `b: Option[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns true if both Options are none, or if they are both some and have equal values.

### filter

[ref: #symbol-filter]

Applies a callback to the value of the Option.

**Input:**
- `self: Option[T]`
- `callback: proc (input: T): bool`

**Output:** `Option[T]`
**Generic parameters:** `T`

**Pragmas:** `inline`, `effectsOf: callback`

Applies a callback to the value of the Option.

If the callback returns true, the option is returned as some. If it returns false, it is returned as none.

**See also:**

* [flatMap proc](#flatMap,Option[A],proc(A))

### flatMap

[ref: #symbol-flatmap]

Applies a callback function to the value of the Option and returns the new value.

**Input:**
- `self: Option[T]`
- `callback: proc (input: T): Option[R]`

**Output:** `Option[R]`
**Generic parameters:** `T`, `R`

**Pragmas:** `inline`, `effectsOf: callback`

Applies a callback function to the value of the Option and returns the new value.

If the Option has no value, none(R) will be returned.

This is similar to map, with the difference that the callback returns an Option, not a raw value. This allows multiple procs with a signature of A -> Option[B] to be chained together.

See also:

* [flatten proc](#flatten,Option[Option[A]])
* [filter proc](#filter,Option[T],proc(T))

### flatten

[ref: #symbol-flatten]

Remove one level of structure in a nested Option.

**Input:**
- `self: Option[Option[T]]`

**Output:** `Option[T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Remove one level of structure in a nested Option.

**See also:**

* [flatMap proc](#flatMap,Option[T],proc(T))

### get

[ref: #symbol-get]

Returns the content of an Option. If it has no value, an UnpackDefect exception is raised.

**Input:**
- `self: Option[T]`

**Output:** `lent T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the content of an Option. If it has no value, an UnpackDefect exception is raised.

**See also:**

* [get proc](#get,Option[T],T) with a default return value

### get

[ref: #symbol-get]

**Input:**
- `self: Option[T]`
- `otherwise: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the content of the Option or otherwise if the Option has no value.

### get

[ref: #symbol-get]

**Input:**
- `self: var Option[T]`

**Output:** `var T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the content of the var Option mutably. If it has no value, an UnpackDefect exception is raised.

### isNone

[ref: #symbol-isnone]

Checks if an Option is empty.

**Input:**
- `self: Option[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`

Checks if an Option is empty.

**See also:**

* [isSome proc](#isSome,Option[T])
* [none proc](#none,typedesc)

### isSome

[ref: #symbol-issome]

Checks if an Option contains a value.

**Input:**
- `self: Option[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`

Checks if an Option contains a value.

**See also:**

* [isNone proc](#isNone,Option[T])
* [some proc](#some,T)

### map

[ref: #symbol-map]

Applies a callback function to the value of the Option, if it has one.

**Input:**
- `self: Option[T]`
- `callback: proc (input: T)`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `effectsOf: callback`

Applies a callback function to the value of the Option, if it has one.

**See also:**

* [map proc](#map,Option[T],proc(T)_2) for a version with a callback which returns a value

### map

[ref: #symbol-map]

Applies a callback function to the value of the Option and returns an Option containing the new value.

**Input:**
- `self: Option[T]`
- `callback: proc (input: T): R`

**Output:** `Option[R]`
**Generic parameters:** `T`, `R`

**Pragmas:** `inline`, `effectsOf: callback`

Applies a callback function to the value of the Option and returns an Option containing the new value.

If the Option has no value, none(R) will be returned.

**See also:**

* [map proc](#map,Option[T],proc(T))
* [flatMap proc](#flatMap,Option[T],proc(T)) for a version with a callback that returns an Option

### none

[ref: #symbol-none]

Returns an Option for this type that has no value.

**Input:**
- `T: typedesc`

**Output:** `Option[T]`
**Generic parameters:** `T:type`

**Pragmas:** `inline`

Returns an Option for this type that has no value.

**See also:**

* [option proc](#option,T)
* [some proc](#some,T)
* [isNone proc](#isNone,Option[T])

### none

[ref: #symbol-none]

**Input:**
- *(none)*

**Output:** `Option[T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Alias for [none(T)](#none,typedesc).

### option

[ref: #symbol-option]

Can be used to convert a pointer type (ptr, pointer, ref or proc) to an option type. It converts nil to none(T). When T is no pointer type, this is equivalent to some(val).

**Input:**
- `val: sink T`

**Output:** `Option[T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Can be used to convert a pointer type (ptr, pointer, ref or proc) to an option type. It converts nil to none(T). When T is no pointer type, this is equivalent to some(val).

**See also:**

* [some proc](#some,T)
* [none proc](#none,typedesc)

### some

[ref: #symbol-some]

Returns an Option that has the value val.

**Input:**
- `val: sink T`

**Output:** `Option[T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns an Option that has the value val.

**See also:**

* [option proc](#option,T)
* [none proc](#none,typedesc)
* [isSome proc](#isSome,Option[T])

### unsafeGet

[ref: #symbol-unsafeget]

Returns the value of a some. The behavior is undefined for none.

**Input:**
- `self: Option[T]`

**Output:** `lent T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the value of a some. The behavior is undefined for none.

**Note:** Use this only when you are **absolutely sure** the value is present (e.g. after checking with [isSome](#isSome,Option[T])). Generally, using the [get proc](#get,Option[T]) is preferred.

## Type

### Option

[ref: #symbol-option]

```nim
Option[T] = object
  when T is SomePointer:
  else:
```

An optional type that may or may not contain a value of type T. When T is a a pointer type (ptr, pointer, ref, proc or iterator {.closure.}), none(T) is represented as nil.

### UnpackDefect

[ref: #symbol-unpackdefect]

```nim
UnpackDefect = object of Defect
```

### UnpackError

[ref: #symbol-unpackerror]

```nim
UnpackError {.deprecated: "See corresponding Defect".} = UnpackDefect
```
