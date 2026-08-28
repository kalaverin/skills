---
source_hash: 60647fed823f39e9
source_path: lib/std/packedsets.nim
---

# packedsets

[ref: #module-packedsets]

The packedsets module implements an efficient Ordinal set implemented as a sparse bit set.

Supports any Ordinal type.

# [See also](#see-also)

* [sets module](sets.html) for more general hash sets

## Examples

```nim
let a = [1, 2, 3].toPackedSet
assert $a == "{1, 2, 3}"
```

```nim
let
  a = [1].toPackedSet
  b = [1, 2].toPackedSet
  c = [1, 3].toPackedSet
assert a < b
assert not (b < b)
assert not (c < b)
```

```nim
let
  a = [1].toPackedSet
  b = [1, 2].toPackedSet
  c = [1, 3].toPackedSet
assert a <= b
assert b <= b
assert not (c <= b)
```

```nim
assert [1, 2].toPackedSet == [2, 1].toPackedSet
assert [1, 2].toPackedSet == [2, 1, 2].toPackedSet
```

```nim
var
  a = initPackedSet[int]()
  b = initPackedSet[int]()
b.incl(5)
b.incl(7)
a.assign(b)
assert len(a) == 2
```

```nim
var a = [5, 7].toPackedSet
clear(a)
assert len(a) == 0
```

```nim
type ABCD = enum A, B, C, D

let a = [1, 3, 5].toPackedSet
assert a.contains(3)
assert 3 in a
assert not a.contains(8)
assert 8 notin a

let letters = [A, C].toPackedSet
assert A in letters
assert C in letters
assert B notin letters
```

```nim
var a = initPackedSet[int]()
assert a.containsOrIncl(3) == false
assert a.containsOrIncl(3) == true
assert a.containsOrIncl(4) == false
```

```nim
let
  a = [1, 2, 3].toPackedSet
  b = [3, 4, 5].toPackedSet
  c = difference(a, b)
assert c.len == 2
assert c == [1, 2].toPackedSet
```

```nim
let
  a = [1, 2].toPackedSet
  b = [2, 3].toPackedSet
  c = [3, 4].toPackedSet
assert disjoint(a, b) == false
assert disjoint(a, c) == true
```

```nim
var a = [3].toPackedSet
a.excl(3)
a.excl(3)
a.excl(99)
assert len(a) == 0
```

```nim
var a = [1, 5].toPackedSet
a.excl([5].toPackedSet)
assert len(a) == 1
assert 5 notin a
```

```nim
var a = initPackedSet[int]()
a.incl(3)
a.incl(3)
assert len(a) == 1
```

```nim
var a = [1].toPackedSet
a.incl([5].toPackedSet)
assert len(a) == 2
assert 5 in a
```

```nim
let a = initPackedSet[int]()
assert len(a) == 0

type Id = distinct int
var ids = initPackedSet[Id]()
ids.incl(3.Id)
```

```nim
let
  a = [1, 2, 3].toPackedSet
  b = [3, 4, 5].toPackedSet
  c = intersection(a, b)
assert c.len == 1
assert c == [3].toPackedSet
```

```nim
var a = initPackedSet[int]()
assert a.isNil
a.incl(2)
assert not a.isNil
a.excl(2)
assert a.isNil
```

```nim
let a = [1, 3, 5].toPackedSet
assert len(a) == 3
```

```nim
var a = [5].toPackedSet
assert a.missingOrExcl(5) == false
assert a.missingOrExcl(5) == true
```

```nim
let
  a = [1, 2, 3].toPackedSet
  b = [3, 4, 5].toPackedSet
  c = symmetricDifference(a, b)
assert c.len == 4
assert c == [1, 2, 4, 5].toPackedSet
```

```nim
let a = [5, 6, 7, 8, 8].toPackedSet
assert len(a) == 4
assert $a == "{5, 6, 7, 8}"
```

```nim
let
  a = [1, 2, 3].toPackedSet
  b = [3, 4, 5].toPackedSet
  c = union(a, b)
assert c.len == 5
assert c == [1, 2, 3, 4, 5].toPackedSet
```

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `s: PackedSet[A]`

**Output:** `A`
**Generic parameters:** `A`

**Pragmas:** `inline`

Iterates over any included element of s.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `s: PackedSet[A]`

**Output:** `string`
**Generic parameters:** `A`

Converts s to a string.

### `&lt;=`

[ref: #symbol-lt]

Returns true if s1 is a subset of s2.

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if s1 is a subset of s2.

A subset s1 has all of its elements in s2, but s2 doesn't necessarily have more elements than s1. That is, s1 can be equal to s2.

### `&lt;`

[ref: #symbol-lt]

Returns true if s1 is a proper subset of s2.

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if s1 is a proper subset of s2.

A strict or proper subset s1 has all of its elements in s2, but s2 has more elements than s1.

### `*`

[ref: #symbol-]

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `PackedSet[A]`
**Generic parameters:** `A`

**Pragmas:** `inline`

Alias for [intersection(s1, s2)](#intersection,PackedSet[A],PackedSet[A]).

### `+`

[ref: #symbol-]

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `PackedSet[A]`
**Generic parameters:** `A`

**Pragmas:** `inline`

Alias for [union(s1, s2)](#union,PackedSet[A],PackedSet[A]).

### `-`

[ref: #symbol-]

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `PackedSet[A]`
**Generic parameters:** `A`

**Pragmas:** `inline`

Alias for [difference(s1, s2)](#difference,PackedSet[A],PackedSet[A]).

### `==`

[ref: #symbol-]

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if both s1 and s2 have the same elements and set size.

### `=copy`

[ref: #symbol-copy]

**Input:**
- `dest: var PackedSet[A]`
- `src: PackedSet[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Copies src to dest. dest does not need to be initialized by the [initPackedSet proc](#initPackedSet).

### assign

[ref: #symbol-assign]

**Input:**
- `dest: var PackedSet[A]`
- `src: PackedSet[A]`

**Output:** *(none)*
**Generic parameters:** `A`

**Pragmas:** `inline`, `deprecated`

Copies src to dest. dest does not need to be initialized by the [initPackedSet proc](#initPackedSet).

### card

[ref: #symbol-card]

Alias for [len()](#len,PackedSet[A]).

**Input:**
- `s: PackedSet[A]`

**Output:** `int`
**Generic parameters:** `A`

**Pragmas:** `inline`

Alias for [len()](#len,PackedSet[A]).

Card stands for the [cardinality](https://en.wikipedia.org/wiki/Cardinality) of a set.

### clear

[ref: #symbol-clear]

**Input:**
- `result: var PackedSet[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Clears the PackedSet[A] back to an empty state.

### contains

[ref: #symbol-contains]

Returns true if key is in s.

**Input:**
- `s: PackedSet[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if key is in s.

This allows the usage of the in operator.

### containsOrIncl

[ref: #symbol-containsorincl]

Includes key in the set s and tells if key was already in s.

**Input:**
- `s: var PackedSet[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Includes key in the set s and tells if key was already in s.

The difference with regards to the [incl proc](#incl,PackedSet[A],A) is that this proc returns true if s already contained key. The proc will return false if key was added as a new value to s during this call.

**See also:**

* [incl proc](#incl,PackedSet[A],A) for including an element
* [missingOrExcl proc](#missingOrExcl,PackedSet[A],A)

### difference

[ref: #symbol-difference]

Returns the difference of the sets s1 and s2.

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `PackedSet[A]`
**Generic parameters:** `A`

Returns the difference of the sets s1 and s2.

The same as [s1 - s2](#-,PackedSet[A],PackedSet[A]).

### disjoint

[ref: #symbol-disjoint]

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if the sets s1 and s2 have no items in common.

### excl

[ref: #symbol-excl]

Excludes key from the set s.

**Input:**
- `s: var PackedSet[A]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`

Excludes key from the set s.

This doesn't do anything if key is not found in s.

**See also:**

* [incl proc](#incl,PackedSet[A],A) for including an element
* [excl proc](#excl,PackedSet[A],PackedSet[A]) for excluding a set
* [missingOrExcl proc](#missingOrExcl,PackedSet[A],A)

### excl

[ref: #symbol-excl]

Excludes all elements from other from s.

**Input:**
- `s: var PackedSet[A]`
- `other: PackedSet[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Excludes all elements from other from s.

This is the in-place version of [s - other](#-,PackedSet[A],PackedSet[A]).

**See also:**

* [incl proc](#incl,PackedSet[A],PackedSet[A]) for including a set
* [excl proc](#excl,PackedSet[A],A) for excluding an element
* [missingOrExcl proc](#missingOrExcl,PackedSet[A],A)

### incl

[ref: #symbol-incl]

Includes an element key in s.

**Input:**
- `s: var PackedSet[A]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`

Includes an element key in s.

This doesn't do anything if key is already in s.

**See also:**

* [excl proc](#excl,PackedSet[A],A) for excluding an element
* [incl proc](#incl,PackedSet[A],PackedSet[A]) for including a set
* [containsOrIncl proc](#containsOrIncl,PackedSet[A],A)

### incl

[ref: #symbol-incl]

Includes all elements from other into s.

**Input:**
- `s: var PackedSet[A]`
- `other: PackedSet[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Includes all elements from other into s.

This is the in-place version of [s + other](#+,PackedSet[A],PackedSet[A]).

**See also:**

* [excl proc](#excl,PackedSet[A],PackedSet[A]) for excluding a set
* [incl proc](#incl,PackedSet[A],A) for including an element
* [containsOrIncl proc](#containsOrIncl,PackedSet[A],A)

### initPackedSet

[ref: #symbol-initpackedset]

Returns an empty PackedSet[A]. A must be Ordinal.

**Input:**
- *(none)*

**Output:** `PackedSet[A]`
**Generic parameters:** `A`

Returns an empty PackedSet[A]. A must be Ordinal.

**See also:**

* [toPackedSet proc](#toPackedSet,openArray[A])

### intersection

[ref: #symbol-intersection]

Returns the intersection of the sets s1 and s2.

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `PackedSet[A]`
**Generic parameters:** `A`

Returns the intersection of the sets s1 and s2.

The same as [s1 \* s2](#*,PackedSet[A],PackedSet[A]).

### isNil

[ref: #symbol-isnil]

**Input:**
- `x: PackedSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

**Pragmas:** `inline`

Returns true if x is empty, false otherwise.

### len

[ref: #symbol-len]

**Input:**
- `s: PackedSet[A]`

**Output:** `int`
**Generic parameters:** `A`

**Pragmas:** `inline`

Returns the number of elements in s.

### missingOrExcl

[ref: #symbol-missingorexcl]

Excludes key from the set s and tells if key was already missing from s.

**Input:**
- `s: var PackedSet[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Excludes key from the set s and tells if key was already missing from s.

The difference with regards to the [excl proc](#excl,PackedSet[A],A) is that this proc returns true if key was missing from s. The proc will return false if key was in s and it was removed during this call.

**See also:**

* [excl proc](#excl,PackedSet[A],A) for excluding an element
* [excl proc](#excl,PackedSet[A],PackedSet[A]) for excluding a set
* [containsOrIncl proc](#containsOrIncl,PackedSet[A],A)

### symmetricDifference

[ref: #symbol-symmetricdifference]

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `PackedSet[A]`
**Generic parameters:** `A`

Returns the symmetric difference of the sets s1 and s2.

### toPackedSet

[ref: #symbol-topackedset]

Creates a new PackedSet[A] that contains the elements of x.

**Input:**
- `x: openArray[A]`

**Output:** `PackedSet[A]`
**Generic parameters:** `A`

Creates a new PackedSet[A] that contains the elements of x.

Duplicates are removed.

**See also:**

* [initPackedSet proc](#initPackedSet)

### union

[ref: #symbol-union]

Returns the union of the sets s1 and s2.

**Input:**
- `s1: PackedSet[A]`
- `s2: PackedSet[A]`

**Output:** `PackedSet[A]`
**Generic parameters:** `A`

Returns the union of the sets s1 and s2.

The same as [s1 + s2](#+,PackedSet[A],PackedSet[A]).

## Type

### PackedSet

[ref: #symbol-packedset]

```nim
PackedSet[A] = object
```

An efficient set of Ordinal types implemented as a sparse bit set.
