---
source_hash: dd5d94abe10b6ed9
source_path: lib/pure/collections/sets.nim
---

# sets

[ref: #module-sets]

The sets module implements an efficient hash set and ordered hash set.

Hash sets are different from the [built in set type](manual.html#types-set-type). Sets allow you to store any value that can be [hashed](hashes.html) and they don't contain duplicate entries.

Common usages of sets:

* removing duplicates from a container by converting it with [toHashSet proc](#toHashSet,openArray[A]) (see also [sequtils.deduplicate func](sequtils.html#deduplicate,openArray[T],bool))
* membership testing
* mathematical operations on two sets, such as [union](#union,HashSet[A],HashSet[A]), [intersection](#intersection,HashSet[A],HashSet[A]), [difference](#difference,HashSet[A],HashSet[A]), and [symmetric difference](#symmetricDifference,HashSet[A],HashSet[A])

**Examples:**

```
echo toHashSet([9, 5, 1])     # {9, 1, 5}
echo toOrderedSet([9, 5, 1])  # {9, 5, 1}

let
  s1 = toHashSet([9, 5, 1])
  s2 = toHashSet([3, 5, 7])

echo s1 + s2    # {9, 1, 3, 5, 7}
echo s1 - s2    # {1, 9}
echo s1 * s2    # {5}
echo s1 -+- s2  # {9, 1, 3, 7}
```

Note: The data types declared here have *value semantics*: This means that = performs a copy of the set.

**See also:**

* [intsets module](intsets.html) for efficient int sets
* [tables module](tables.html) for hash tables

## Examples

```nim
echo toHashSet([9, 5, 1])     # {9, 1, 5}
echo toOrderedSet([9, 5, 1])  # {9, 5, 1}

let
  s1 = toHashSet([9, 5, 1])
  s2 = toHashSet([3, 5, 7])

echo s1 + s2    # {9, 1, 3, 5, 7}
echo s1 - s2    # {1, 9}
echo s1 * s2    # {5}
echo s1 -+- s2  # {9, 1, 3, 7}
```

```nim
echo toHashSet([2, 4, 5])
# --> {2, 4, 5}
echo toHashSet(["no", "esc'aping", "is \" provided"])
# --> {no, esc'aping, is " provided}
```

```nim
echo toOrderedSet([2, 4, 5])
# --> {2, 4, 5}
echo toOrderedSet(["no", "esc'aping", "is \" provided"])
# --> {no, esc'aping, is " provided}
```

```nim
let
  a = toHashSet(["a", "b"])
  b = toHashSet(["b", "c"])
  c = intersection(a, b)
assert c < a and c < b
assert(not (a < a))
```

```nim
let
  a = toHashSet(["a", "b"])
  b = toHashSet(["b", "c"])
  c = intersection(a, b)
assert c <= a and c <= b
assert a <= a
```

```nim
var
  a = toHashSet([1, 2])
  b = toHashSet([2, 1])
assert a == b
```

```nim
let
  a = toOrderedSet([1, 2])
  b = toOrderedSet([2, 1])
assert(not (a == b))
```

```nim
var s = toHashSet([3, 5, 7])
clear(s)
assert len(s) == 0
```

```nim
var s = toOrderedSet([3, 5, 7])
clear(s)
assert len(s) == 0
```

```nim
var values = initHashSet[int]()
assert(not values.contains(2))
assert 2 notin values

values.incl(2)
assert values.contains(2)
assert 2 in values
```

```nim
var values = initOrderedSet[int]()
assert(not values.contains(2))
assert 2 notin values

values.incl(2)
assert values.contains(2)
assert 2 in values
```

```nim
var values = initHashSet[int]()
assert values.containsOrIncl(2) == false
assert values.containsOrIncl(2) == true
assert values.containsOrIncl(3) == false
```

```nim
var values = initOrderedSet[int]()
assert values.containsOrIncl(2) == false
assert values.containsOrIncl(2) == true
assert values.containsOrIncl(3) == false
```

```nim
let
  a = toHashSet(["a", "b"])
  b = toHashSet(["b", "c"])
  c = difference(a, b)
assert c == toHashSet(["a"])
```

```nim
let
  a = toHashSet(["a", "b"])
  b = toHashSet(["b", "c"])
assert disjoint(a, b) == false
assert disjoint(a, b - a) == true
```

```nim
var s = toHashSet([2, 3, 6, 7])
s.excl(2)
s.excl(2)
assert s.len == 3
```

```nim
var
  numbers = toHashSet([1, 2, 3, 4, 5])
  even = toHashSet([2, 4, 6, 8])
numbers.excl(even)
assert len(numbers) == 3
## numbers == {1, 3, 5}
```

```nim
var s = toOrderedSet([2, 3, 6, 7])
s.excl(2)
s.excl(2)
assert s.len == 3
```

```nim
var values = initHashSet[int]()
values.incl(2)
values.incl(2)
assert values.len == 1
```

```nim
var
  values = toHashSet([1, 2, 3])
  others = toHashSet([3, 4, 5])
values.incl(others)
assert values.len == 5
```

```nim
var
  values = toHashSet([1, 2, 3])
  others = toOrderedSet([3, 4, 5])
values.incl(others)
assert values.len == 5
```

```nim
var values = initOrderedSet[int]()
values.incl(2)
values.incl(2)
assert values.len == 1
```

```nim
var a: HashSet[int]
init(a)
```

```nim
var a: OrderedSet[int]
init(a)
```

```nim
var a = initHashSet[int]()
a.incl(3)
assert len(a) == 1
```

```nim
var a = initOrderedSet[int]()
a.incl(3)
assert len(a) == 1
```

```nim
let
  a = toHashSet(["a", "b"])
  b = toHashSet(["b", "c"])
  c = intersection(a, b)
assert c == toHashSet(["b"])
```

```nim
proc savePreferences(options: HashSet[string]) =
  assert options.isValid, "Pass an initialized set!"
  # Do stuff here, may crash in release builds!
```

```nim
var a: HashSet[string]
assert len(a) == 0
let s = toHashSet([3, 5, 7])
assert len(s) == 3
```

```nim
var a: OrderedSet[string]
assert len(a) == 0
let s = toHashSet([3, 5, 7])
assert len(s) == 3
```

```nim
let
  a = toHashSet([1, 2, 3])
  b = a.map(proc (x: int): string = $x)
assert b == toHashSet(["1", "2", "3"])
```

```nim
var s = toHashSet([2, 3, 6, 7])
assert s.missingOrExcl(4) == true
assert s.missingOrExcl(6) == false
assert s.missingOrExcl(6) == true
```

```nim
var s = toOrderedSet([2, 3, 6, 7])
assert s.missingOrExcl(4) == true
assert s.missingOrExcl(6) == false
assert s.missingOrExcl(6) == true
```

```nim
var s = toHashSet([2, 1])
assert [s.pop, s.pop] in [[1, 2], [2,1]] # order unspecified
doAssertRaises(KeyError, echo s.pop)
```

```nim
let
  a = toHashSet(["a", "b"])
  b = toHashSet(["b", "c"])
  c = symmetricDifference(a, b)
assert c == toHashSet(["a", "c"])
```

```nim
let
  a = toHashSet([5, 3, 2])
  b = toHashSet("abracadabra")
assert len(a) == 3
## a == {2, 3, 5}
assert len(b) == 5
## b == {'a', 'b', 'c', 'd', 'r'}
```

```nim
let
  a = toOrderedSet([5, 3, 2])
  b = toOrderedSet("abracadabra")
assert len(a) == 3
## a == {5, 3, 2} # different than in HashSet
assert len(b) == 5
## b == {'a', 'b', 'r', 'c', 'd'} # different than in HashSet
```

```nim
let
  a = toHashSet(["a", "b"])
  b = toHashSet(["b", "c"])
  c = union(a, b)
assert c == toHashSet(["a", "b", "c"])
```

```nim
type
  pair = tuple[a, b: int]
var
  a, b = initHashSet[pair]()
a.incl((2, 3))
a.incl((3, 2))
a.incl((2, 3))
for x, y in a.items:
  b.incl((x - 2, y + 1))
assert a.len == 2
echo b
# --> {(a: 1, b: 3), (a: 0, b: 4)}
```

```nim
var a = initOrderedSet[int]()
for value in [9, 2, 1, 5, 1, 8, 4, 2]:
  a.incl(value)
for value in a.items:
  echo "Got ", value
# --> Got 9
# --> Got 2
# --> Got 1
# --> Got 5
# --> Got 8
# --> Got 4
```

```nim
let a = toOrderedSet("abracadabra")
var p = newSeq[(int, char)]()
for x in pairs(a):
  p.add(x)
assert p == @[(0, 'a'), (1, 'b'), (2, 'r'), (3, 'c'), (4, 'd')]
```

## Const

### defaultInitialSize

[ref: #symbol-defaultinitialsize]

```nim
defaultInitialSize = 64
```

## Iterator

### items

[ref: #symbol-items]

Iterates over elements of the set s.

**Input:**
- `s: HashSet[A]`

**Output:** `lent A`
**Generic parameters:** `A`

Iterates over elements of the set s.

If you need a sequence with the elements you can use [sequtils.toSeq template](sequtils.html#toSeq.t,untyped).

```
type
  pair = tuple[a, b: int]
var
  a, b = initHashSet[pair]()
a.incl((2, 3))
a.incl((3, 2))
a.incl((2, 3))
for x, y in a.items:
  b.incl((x - 2, y + 1))
assert a.len == 2
echo b
# --> {(a: 1, b: 3), (a: 0, b: 4)}
```

### items

[ref: #symbol-items]

Iterates over keys in the ordered set s in insertion order.

**Input:**
- `s: OrderedSet[A]`

**Output:** `lent A`
**Generic parameters:** `A`

Iterates over keys in the ordered set s in insertion order.

If you need a sequence with the elements you can use [sequtils.toSeq template](sequtils.html#toSeq.t,untyped).

```
var a = initOrderedSet[int]()
for value in [9, 2, 1, 5, 1, 8, 4, 2]:
  a.incl(value)
for value in a.items:
  echo "Got ", value
# --> Got 9
# --> Got 2
# --> Got 1
# --> Got 5
# --> Got 8
# --> Got 4
```

### pairs

[ref: #symbol-pairs]

**Input:**
- `s: OrderedSet[A]`

**Output:** `tuple[a: int, b: A]`
**Generic parameters:** `A`

Iterates through (position, value) tuples of OrderedSet s.

## Proc

### `$`

[ref: #symbol-]

Converts the set s to a string, mostly for logging and printing purposes.

**Input:**
- `s: HashSet[A]`

**Output:** `string`
**Generic parameters:** `A`

Converts the set s to a string, mostly for logging and printing purposes.

Don't use this proc for serialization, the representation may change at any moment and values are not escaped.

**Examples:**

```
echo toHashSet([2, 4, 5])
# --> {2, 4, 5}
echo toHashSet(["no", "esc'aping", "is \" provided"])
# --> {no, esc'aping, is " provided}
```

### `$`

[ref: #symbol-]

Converts the ordered hash set s to a string, mostly for logging and printing purposes.

**Input:**
- `s: OrderedSet[A]`

**Output:** `string`
**Generic parameters:** `A`

Converts the ordered hash set s to a string, mostly for logging and printing purposes.

Don't use this proc for serialization, the representation may change at any moment and values are not escaped.

**Examples:**

```
echo toOrderedSet([2, 4, 5])
# --> {2, 4, 5}
echo toOrderedSet(["no", "esc'aping", "is \" provided"])
# --> {no, esc'aping, is " provided}
```

### `&lt;=`

[ref: #symbol-lt]

Returns true if s is a subset of t.

**Input:**
- `s: HashSet[A]`
- `t: HashSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if s is a subset of t.

A subset s has all of its members in t and t doesn't necessarily have more members than s. That is, s can be equal to t.

### `&lt;`

[ref: #symbol-lt]

Returns true if s is a strict or proper subset of t.

**Input:**
- `s: HashSet[A]`
- `t: HashSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if s is a strict or proper subset of t.

A strict or proper subset s has all of its members in t but t has more elements than s.

### `*`

[ref: #symbol-]

**Input:**
- `s1: HashSet[A]`
- `s2: HashSet[A]`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

**Pragmas:** `inline`

Alias for [intersection(s1, s2)](#intersection,HashSet[A],HashSet[A]).

### `+`

[ref: #symbol-]

**Input:**
- `s1: HashSet[A]`
- `s2: HashSet[A]`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

**Pragmas:** `inline`

Alias for [union(s1, s2)](#union,HashSet[A],HashSet[A]).

### `-+-`

[ref: #symbol-]

**Input:**
- `s1: HashSet[A]`
- `s2: HashSet[A]`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

**Pragmas:** `inline`

Alias for [symmetricDifference(s1, s2)](#symmetricDifference,HashSet[A],HashSet[A]).

### `-`

[ref: #symbol-]

**Input:**
- `s1: HashSet[A]`
- `s2: HashSet[A]`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

**Pragmas:** `inline`

Alias for [difference(s1, s2)](#difference,HashSet[A],HashSet[A]).

### `==`

[ref: #symbol-]

**Input:**
- `s: HashSet[A]`
- `t: HashSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if both s and t have the same members and set size.

### `==`

[ref: #symbol-]

**Input:**
- `s: OrderedSet[A]`
- `t: OrderedSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

Equality for ordered sets.

### `[]`

[ref: #symbol-]

Returns the element that is actually stored in s which has the same value as key or raises the KeyError exception.

**Input:**
- `s: var HashSet[A]`
- `key: A`

**Output:** `var A`
**Generic parameters:** `A`

Returns the element that is actually stored in s which has the same value as key or raises the KeyError exception.

This is useful when one overloaded hash and == but still needs reference semantics for sharing.

### card

[ref: #symbol-card]

Alias for [len()](#len,HashSet[A]).

**Input:**
- `s: HashSet[A]`

**Output:** `int`
**Generic parameters:** `A`

Alias for [len()](#len,HashSet[A]).

Card stands for the [cardinality](https://en.wikipedia.org/wiki/Cardinality) of a set.

### card

[ref: #symbol-card]

Alias for [len()](#len,OrderedSet[A]).

**Input:**
- `s: OrderedSet[A]`

**Output:** `int`
**Generic parameters:** `A`

**Pragmas:** `inline`

Alias for [len()](#len,OrderedSet[A]).

Card stands for the [cardinality](https://en.wikipedia.org/wiki/Cardinality) of a set.

### clear

[ref: #symbol-clear]

Clears the HashSet back to an empty state, without shrinking any of the existing storage.

**Input:**
- `s: var HashSet[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Clears the HashSet back to an empty state, without shrinking any of the existing storage.

O(n) operation, where n is the size of the hash bucket.

See also:

* [pop proc](#pop,HashSet[A])

### clear

[ref: #symbol-clear]

Clears the OrderedSet back to an empty state, without shrinking any of the existing storage.

**Input:**
- `s: var OrderedSet[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Clears the OrderedSet back to an empty state, without shrinking any of the existing storage.

O(n) operation where n is the size of the hash bucket.

### contains

[ref: #symbol-contains]

Returns true if key is in s.

**Input:**
- `s: HashSet[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if key is in s.

This allows the usage of in operator.

See also:

* [incl proc](#incl,HashSet[A],A)
* [containsOrIncl proc](#containsOrIncl,HashSet[A],A)

### contains

[ref: #symbol-contains]

Returns true if key is in s.

**Input:**
- `s: OrderedSet[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if key is in s.

This allows the usage of in operator.

See also:

* [incl proc](#incl,OrderedSet[A],A)
* [containsOrIncl proc](#containsOrIncl,OrderedSet[A],A)

### containsOrIncl

[ref: #symbol-containsorincl]

Includes key in the set s and tells if key was already in s.

**Input:**
- `s: var HashSet[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Includes key in the set s and tells if key was already in s.

The difference with regards to the [incl proc](#incl,HashSet[A],A) is that this proc returns true if s already contained key. The proc will return false if key was added as a new value to s during this call.

See also:

* [incl proc](#incl,HashSet[A],A) for including an element
* [incl proc](#incl,HashSet[A],HashSet[A]) for including other set
* [missingOrExcl proc](#missingOrExcl,HashSet[A],A)

### containsOrIncl

[ref: #symbol-containsorincl]

Includes key in the set s and tells if key was already in s.

**Input:**
- `s: var OrderedSet[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Includes key in the set s and tells if key was already in s.

The difference with regards to the [incl proc](#incl,OrderedSet[A],A) is that this proc returns true if s already contained key. The proc will return false if key was added as a new value to s during this call.

See also:

* [incl proc](#incl,OrderedSet[A],A) for including an element
* [missingOrExcl proc](#missingOrExcl,OrderedSet[A],A)

### difference

[ref: #symbol-difference]

Returns the difference of the sets s1 and s2.

**Input:**
- `s1: HashSet[A]`
- `s2: HashSet[A]`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

Returns the difference of the sets s1 and s2.

The same as [s1 - s2](#-,HashSet[A],HashSet[A]).

The difference of two sets is represented mathematically as *A ∖ B* and is the set of all objects that are members of s1 and not members of s2.

See also:

* [union proc](#union,HashSet[A],HashSet[A])
* [intersection proc](#intersection,HashSet[A],HashSet[A])
* [symmetricDifference proc](#symmetricDifference,HashSet[A],HashSet[A])

### disjoint

[ref: #symbol-disjoint]

**Input:**
- `s1: HashSet[A]`
- `s2: HashSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if the sets s1 and s2 have no items in common.

### excl

[ref: #symbol-excl]

Excludes key from the set s.

**Input:**
- `s: var HashSet[A]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`

Excludes key from the set s.

This doesn't do anything if key is not found in s.

See also:

* [incl proc](#incl,HashSet[A],A) for including an element
* [excl proc](#excl,HashSet[A],HashSet[A]) for excluding other set
* [missingOrExcl proc](#missingOrExcl,HashSet[A],A)

### excl

[ref: #symbol-excl]

Excludes all elements of other set from s.

**Input:**
- `s: var HashSet[A]`
- `other: HashSet[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Excludes all elements of other set from s.

This is the in-place version of [s - other](#-,HashSet[A],HashSet[A]).

See also:

* [incl proc](#incl,HashSet[A],HashSet[A]) for including other set
* [excl proc](#excl,HashSet[A],A) for excluding an element
* [missingOrExcl proc](#missingOrExcl,HashSet[A],A)

### excl

[ref: #symbol-excl]

Excludes key from the set s. Efficiency: O(n).

**Input:**
- `s: var OrderedSet[A]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`

Excludes key from the set s. Efficiency: O(n).

This doesn't do anything if key is not found in s.

See also:

* [incl proc](#incl,OrderedSet[A],A) for including an element
* [missingOrExcl proc](#missingOrExcl,OrderedSet[A],A)

### hash

[ref: #symbol-hash]

**Input:**
- `s: HashSet[A]`

**Output:** `Hash`
**Generic parameters:** `A`

Hashing of HashSet.

### hash

[ref: #symbol-hash]

**Input:**
- `s: OrderedSet[A]`

**Output:** `Hash`
**Generic parameters:** `A`

Hashing of OrderedSet.

### incl

[ref: #symbol-incl]

Includes an element key in s.

**Input:**
- `s: var HashSet[A]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`

Includes an element key in s.

This doesn't do anything if key is already in s.

See also:

* [excl proc](#excl,HashSet[A],A) for excluding an element
* [incl proc](#incl,HashSet[A],HashSet[A]) for including other set
* [containsOrIncl proc](#containsOrIncl,HashSet[A],A)

### incl

[ref: #symbol-incl]

Includes all elements from other set into s (must be declared as var).

**Input:**
- `s: var HashSet[A]`
- `other: HashSet[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Includes all elements from other set into s (must be declared as var).

This is the in-place version of [s + other](#+,HashSet[A],HashSet[A]).

See also:

* [excl proc](#excl,HashSet[A],HashSet[A]) for excluding other set
* [incl proc](#incl,HashSet[A],A) for including an element
* [containsOrIncl proc](#containsOrIncl,HashSet[A],A)


[Next](sets_2.md)
