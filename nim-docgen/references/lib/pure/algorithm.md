---
source_hash: 4d9dab363e874e5a
source_path: lib/pure/algorithm.nim
---

# algorithm

[ref: #module-algorithm]

This module implements some common generic algorithms on openArrays.

# [Basic usage](#basic-usage)

# [See also](#see-also)

* [sequtils module](sequtils.html) for working with the built-in seq type
* [tables module](tables.html) for sorting tables

## Examples

```nim
import std/algorithm
type People = tuple
  year: int
  name: string

var a: seq[People]

a.add((2000, "John"))
a.add((2005, "Marie"))
a.add((2010, "Jane"))

# Sorting with default system.cmp
a.sort()
assert a == @[(year: 2000, name: "John"), (year: 2005, name: "Marie"),
              (year: 2010, name: "Jane")]

proc myCmp(x, y: People): int =
  cmp(x.name, y.name)

# Sorting with custom proc
a.sort(myCmp)
assert a == @[(year: 2010, name: "Jane"), (year: 2000, name: "John"),
              (year: 2005, name: "Marie")]
```

```nim
assert -123 * Descending == 123
assert 123 * Descending == -123
assert -123 * Ascending == -123
assert 123 * Ascending == 123
```

```nim
assert binarySearch(["a", "b", "c", "d"], "d", system.cmp[string]) == 3
assert binarySearch(["a", "b", "c", "d"], "c", system.cmp[string]) == 2
```

```nim
assert binarySearch([0, 1, 2, 3, 4], 4) == 4
assert binarySearch([0, 1, 2, 3, 4], 2) == 2
```

```nim
var a: array[6, int]
a.fill(1, 3, 9)
assert a == [0, 9, 9, 9, 0, 0]
a.fill(3, 5, 7)
assert a == [0, 9, 9, 7, 7, 7]
doAssertRaises(IndexDefect, a.fill(1, 7, 9))
```

```nim
var a: array[6, int]
a.fill(9)
assert a == [9, 9, 9, 9, 9, 9]
a.fill(4)
assert a == [4, 4, 4, 4, 4, 4]
```

```nim
let
  a = [2, 3, 1, 5, 4]
  b = [1, 2, 3, 4, 5]
  c = [5, 4, 3, 2, 1]
  d = ["adam", "brian", "cat", "dande"]
  e = ["adam", "dande", "brian", "cat"]
assert isSorted(a) == false
assert isSorted(b) == true
assert isSorted(c) == false
assert isSorted(c, Descending) == true
assert isSorted(d) == true
assert isSorted(e) == false
```

```nim
let
  a = [2, 3, 1, 5, 4]
  b = [1, 2, 3, 4, 5]
  c = [5, 4, 3, 2, 1]
  d = ["adam", "brian", "cat", "dande"]
  e = ["adam", "dande", "brian", "cat"]
assert isSorted(a) == false
assert isSorted(b) == true
assert isSorted(c) == false
assert isSorted(c, Descending) == true
assert isSorted(d) == true
assert isSorted(e) == false
```

```nim
var arr = @[1, 2, 3, 5, 6, 7, 8, 9]
assert arr.lowerBound(3, system.cmp[int]) == 2
assert arr.lowerBound(4, system.cmp[int]) == 3
assert arr.lowerBound(5, system.cmp[int]) == 3
arr.insert(4, arr.lowerBound(4, system.cmp[int]))
assert arr == [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

```nim
let x = [5, 10, 15, 20, 25]
let y = [50, 40, 30, 20, 10].sorted

var merged: seq[int]
merged.merge(x, y)
assert merged.isSorted
assert merged == @[5, 10, 10, 15, 20, 20, 25, 30, 40, 50]
```

```nim
let x = @[1, 3, 6]
let y = @[2, 3, 4]

block:
  var merged = @[7] # new data is appended to merged sequence
  merged.merge(x, y, system.cmp[int])
  assert merged == @[7, 1, 2, 3, 3, 4, 6]

block:
  var merged = @[7] # if you only want new data, clear merged sequence first
  merged.setLen(0)
  merged.merge(x, y, system.cmp[int])
  assert merged.isSorted
  assert merged == @[1, 2, 3, 3, 4, 6]

import std/sugar

var res: seq[(int, int)]
res.merge([(1, 1)], [(1, 2)], (a, b) => a[0] - b[0])
assert res == @[(1, 1), (1, 2)]

assert seq[int].default.dup(merge([1, 3], [2, 4])) == @[1, 2, 3, 4]
```

```nim
var v = @[0, 1, 2, 3]
assert v.nextPermutation() == true
assert v == @[0, 1, 3, 2]
assert v.nextPermutation() == true
assert v == @[0, 2, 1, 3]
assert v.prevPermutation() == true
assert v == @[0, 1, 3, 2]
v = @[3, 2, 1, 0]
assert v.nextPermutation() == false
assert v == @[3, 2, 1, 0]
```

```nim
var v = @[0, 1, 2, 3]
assert v.prevPermutation() == false
assert v == @[0, 1, 2, 3]
assert v.nextPermutation() == true
assert v == @[0, 1, 3, 2]
assert v.prevPermutation() == true
assert v == @[0, 1, 2, 3]
```

```nim
assert product(@[@[1], @[2]]) == @[@[1, 2]]
assert product(@[@["A", "K"], @["Q"]]) == @[@["K", "Q"], @["A", "Q"]]
```

```nim
var a = [1, 2, 3, 4, 5, 6]
a.reverse()
assert a == [6, 5, 4, 3, 2, 1]
a.reverse()
assert a == [1, 2, 3, 4, 5, 6]
```

```nim
var a = [1, 2, 3, 4, 5, 6]
a.reverse(1, 3)
assert a == [1, 4, 3, 2, 5, 6]
a.reverse(1, 3)
assert a == [1, 2, 3, 4, 5, 6]
doAssertRaises(IndexDefect, a.reverse(1, 7))
```

```nim
assert [10, 11, 12].reversed == @[12, 11, 10]
assert seq[string].default.reversed == @[]
```

```nim
var a = @[1, 2, 3, 4, 5]
a = rotatedLeft(a, 2)
assert a == @[3, 4, 5, 1, 2]
a = rotatedLeft(a, 4)
assert a == @[2, 3, 4, 5, 1]
a = rotatedLeft(a, -6)
assert a == @[1, 2, 3, 4, 5]
```

```nim
var a = @[1, 2, 3, 4, 5]
a = rotatedLeft(a, 1 .. 4, 3)
assert a == @[1, 5, 2, 3, 4]
a = rotatedLeft(a, 1 .. 3, 2)
assert a == @[1, 3, 5, 2, 4]
a = rotatedLeft(a, 1 .. 3, -2)
assert a == @[1, 5, 2, 3, 4]
```

```nim
var a = [1, 2, 3, 4, 5]
a.rotateLeft(2)
assert a == [3, 4, 5, 1, 2]
a.rotateLeft(4)
assert a == [2, 3, 4, 5, 1]
a.rotateLeft(-6)
assert a == [1, 2, 3, 4, 5]
```

```nim
var a = [0, 1, 2, 3, 4, 5]
a.rotateLeft(1 .. 4, 3)
assert a == [0, 4, 1, 2, 3, 5]
a.rotateLeft(1 .. 4, 3)
assert a == [0, 3, 4, 1, 2, 5]
a.rotateLeft(1 .. 4, -3)
assert a == [0, 4, 1, 2, 3, 5]
doAssertRaises(IndexDefect, a.rotateLeft(1 .. 7, 2))
```

```nim
sort(myIntArray, system.cmp[int])
# do not use cmp[string] here as we want to use the specialized
# overload:
sort(myStrArray, system.cmp)
```

```nim
people.sort do (x, y: Person) -> int:
  result = cmp(x.surname, y.surname)
  if result == 0:
    result = cmp(x.name, y.name)
```

```nim
var d = ["boo", "fo", "barr", "qux"]
proc myCmp(x, y: string): int =
  if x.len() > y.len() or x.len() == y.len(): 1
  else: -1
sort(d, myCmp)
assert d == ["fo", "qux", "boo", "barr"]
```

```nim
let
  a = [2, 3, 1, 5, 4]
  b = sorted(a, system.cmp[int])
  c = sorted(a, system.cmp[int], Descending)
  d = sorted(["adam", "dande", "brian", "cat"], system.cmp[string])
assert b == @[1, 2, 3, 4, 5]
assert c == @[5, 4, 3, 2, 1]
assert d == @["adam", "brian", "cat", "dande"]
```

```nim
let
  a = [2, 3, 1, 5, 4]
  b = sorted(a)
  c = sorted(a, Descending)
  d = sorted(["adam", "dande", "brian", "cat"])
assert b == @[1, 2, 3, 4, 5]
assert c == @[5, 4, 3, 2, 1]
assert d == @["adam", "brian", "cat", "dande"]
```

```nim
var arr = @[1, 2, 3, 5, 6, 7, 8, 9]
assert arr.upperBound(2, system.cmp[int]) == 2
assert arr.upperBound(3, system.cmp[int]) == 3
assert arr.upperBound(4, system.cmp[int]) == 3
arr.insert(4, arr.upperBound(3, system.cmp[int]))
assert arr == [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

```nim
type Person = tuple[name: string, age: int]
var
  p1: Person = (name: "p1", age: 60)
  p2: Person = (name: "p2", age: 20)
  p3: Person = (name: "p3", age: 30)
  p4: Person = (name: "p4", age: 30)
  people = @[p1, p2, p4, p3]

assert people.sortedByIt(it.name) == @[(name: "p1", age: 60), (name: "p2",
    age: 20), (name: "p3", age: 30), (name: "p4", age: 30)]
# Nested sort
assert people.sortedByIt((it.age, it.name)) == @[(name: "p2", age: 20),
   (name: "p3", age: 30), (name: "p4", age: 30), (name: "p1", age: 60)]
```

## Proc

### `*`

[ref: #symbol-]

Flips the sign of x if order == Descending. If order == Ascending then x is returned.

**Input:**
- `x: int`
- `order: SortOrder`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Flips the sign of x if order == Descending. If order == Ascending then x is returned.

x is supposed to be the result of a comparator, i.e.

< 0 for *less than*,  
== 0 for *equal*,  
> 0 for *greater than*.

### binarySearch

[ref: #symbol-binarysearch]

Binary search for key in a. Return the index of key or -1 if not found. Assumes that a is sorted according to cmp.

**Input:**
- `a: openArray[T]`
- `key: K`
- `cmp: proc (x: T; y: K): int {.closure.}`

**Output:** `int`
**Generic parameters:** `T`, `K`

**Pragmas:** `effectsOf: cmp`

Binary search for key in a. Return the index of key or -1 if not found. Assumes that a is sorted according to cmp.

cmp is the comparator function to use, the expected return values are the same as those of system.cmp.

### binarySearch

[ref: #symbol-binarysearch]

**Input:**
- `a: openArray[T]`
- `key: T`

**Output:** `int`
**Generic parameters:** `T`

Binary search for key in a. Return the index of key or -1 if not found. Assumes that a is sorted.

### fill

[ref: #symbol-fill]

Assigns value to all elements of the slice a[first..last].

**Input:**
- `a: var openArray[T]`
- `first: Natural`
- `last: Natural`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

Assigns value to all elements of the slice a[first..last].

If an invalid range is passed, it raises IndexDefect.

### fill

[ref: #symbol-fill]

**Input:**
- `a: var openArray[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

Assigns value to all elements of the container a.

### isSorted

[ref: #symbol-issorted]

Checks to see whether a is already sorted in order using cmp for the comparison. The parameters are identical to sort. Requires O(n) time.

**Input:**
- `a: openArray[T]`
- `cmp: proc (x, y: T): int {.closure.}`
- `order:  = SortOrder.Ascending`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `effectsOf: cmp`

Checks to see whether a is already sorted in order using cmp for the comparison. The parameters are identical to sort. Requires O(n) time.

**See also:**

* [isSorted proc](#isSorted,openArray[T])

### isSorted

[ref: #symbol-issorted]

Shortcut version of isSorted that uses system.cmp[T] as the comparison function.

**Input:**
- `a: openArray[T]`
- `order:  = SortOrder.Ascending`

**Output:** `bool`
**Generic parameters:** `T`

Shortcut version of isSorted that uses system.cmp[T] as the comparison function.

**See also:**

* [isSorted func](#isSorted,openArray[T],proc(T,T))

### lowerBound

[ref: #symbol-lowerbound]

Returns the index of the first element in a that is not less than (i.e. greater or equal to) key, or last if no such element is found. In other words if you have a sorted sequence and you call insert(thing, elm, lowerBound(thing, elm)) the sequence will still be sorted. Assumes that a is sorted according to cmp.

**Input:**
- `a: openArray[T]`
- `key: K`
- `cmp: proc (x: T; k: K): int {.closure.}`

**Output:** `int`
**Generic parameters:** `T`, `K`

**Pragmas:** `effectsOf: cmp`

Returns the index of the first element in a that is not less than (i.e. greater or equal to) key, or last if no such element is found. In other words if you have a sorted sequence and you call insert(thing, elm, lowerBound(thing, elm)) the sequence will still be sorted. Assumes that a is sorted according to cmp.

If an invalid range is passed, it raises IndexDefect.

This version uses cmp to compare the elements. The expected return values are the same as those of system.cmp.

**See also:**

* [upperBound proc](#upperBound,openArray[T],K,proc(T,K)) sorted by cmp in the specified order
* [upperBound proc](#upperBound,openArray[T],T)

### lowerBound

[ref: #symbol-lowerbound]

Returns the index of the first element in a that is not less than (i.e. greater or equal to) key, or last if no such element is found. In other words if you have a sorted sequence and you call insert(thing, elm, lowerBound(thing, elm)) the sequence will still be sorted. Assumes that a is sorted.

**Input:**
- `a: openArray[T]`
- `key: T`

**Output:** `int`
**Generic parameters:** `T`

Returns the index of the first element in a that is not less than (i.e. greater or equal to) key, or last if no such element is found. In other words if you have a sorted sequence and you call insert(thing, elm, lowerBound(thing, elm)) the sequence will still be sorted. Assumes that a is sorted.

This version uses the default comparison function cmp.

**See also:**

* [upperBound proc](#upperBound,openArray[T],K,proc(T,K)) sorted by cmp in the specified order
* [upperBound proc](#upperBound,openArray[T],T)

### merge

[ref: #symbol-merge]

Merges two sorted openArray. x and y are assumed to be sorted. If you do not wish to provide your own cmp, you may use system.cmp or instead call the overloaded version of merge, which uses system.cmp.

**Input:**
- `result: var seq[T]`
- `x: openArray[T]`
- `y: openArray[T]`
- `cmp: proc (x, y: T): int {.closure.}`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `effectsOf: cmp`

Merges two sorted openArray. x and y are assumed to be sorted. If you do not wish to provide your own cmp, you may use system.cmp or instead call the overloaded version of merge, which uses system.cmp.

**Note:**
The original data of result is not cleared, new data is appended to result.

**See also:**

* [merge proc](#merge,seq[T],openArray[T],openArray[T])

### merge

[ref: #symbol-merge]

Shortcut version of merge that uses system.cmp[T] as the comparison function.

**Input:**
- `result: var seq[T]`
- `x: openArray[T]`
- `y: openArray[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Shortcut version of merge that uses system.cmp[T] as the comparison function.

**See also:**

* [merge proc](#merge,seq[T],openArray[T],openArray[T],proc(T,T))

### nextPermutation

[ref: #symbol-nextpermutation]

Calculates the next lexicographic permutation, directly modifying x. The result is whether a permutation happened, otherwise we have reached the last-ordered permutation.

**Input:**
- `x: var openArray[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `discardable`

Calculates the next lexicographic permutation, directly modifying x. The result is whether a permutation happened, otherwise we have reached the last-ordered permutation.

If you start with an unsorted array/seq, the repeated permutations will **not** give you all permutations but stop with the last.

**See also:**

* [prevPermutation proc](#prevPermutation,openArray[T])

### prevPermutation

[ref: #symbol-prevpermutation]

Calculates the previous lexicographic permutation, directly modifying x. The result is whether a permutation happened, otherwise we have reached the first-ordered permutation.

**Input:**
- `x: var openArray[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `discardable`

Calculates the previous lexicographic permutation, directly modifying x. The result is whether a permutation happened, otherwise we have reached the first-ordered permutation.

**See also:**

* [nextPermutation proc](#nextPermutation,openArray[T])

### product

[ref: #symbol-product]

Produces the Cartesian product of the array. Every element of the result is a combination of one element from each seq in x, with the ith element coming from x[i].

**Input:**
- `x: openArray[seq[T]]`

**Output:** `seq[seq[T]]`
**Generic parameters:** `T`

Produces the Cartesian product of the array. Every element of the result is a combination of one element from each seq in x, with the ith element coming from x[i].

**Warning:**
complexity may explode.

### reverse

[ref: #symbol-reverse]

Reverses the slice a[first..last].

**Input:**
- `a: var openArray[T]`
- `first: Natural`
- `last: Natural`

**Output:** *(none)*
**Generic parameters:** `T`

Reverses the slice a[first..last].

If an invalid range is passed, it raises IndexDefect.

**See also:**

* [reversed proc](#reversed,openArray[T],Natural,int) reverse a slice and returns a seq[T]
* [reversed proc](#reversed,openArray[T]) reverse and returns a seq[T]

### reverse

[ref: #symbol-reverse]

Reverses the contents of the container a.

**Input:**
- `a: var openArray[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Reverses the contents of the container a.

**See also:**

* [reversed proc](#reversed,openArray[T],Natural,int) reverse a slice and returns a seq[T]
* [reversed proc](#reversed,openArray[T]) reverse and returns a seq[T]

### reversed

[ref: #symbol-reversed]

Returns the elements of a in reverse order.

**Input:**
- `a: openArray[T]`

**Output:** `seq[T]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the elements of a in reverse order.

**See also:**

* [reverse proc](#reverse,openArray[T])

### reversed

[ref: #symbol-reversed]

**Input:**
- `a: openArray[T]`
- `first: Natural`
- `last: int`

**Output:** `seq[T]`
**Generic parameters:** `T`

**Pragmas:** `inline`, `deprecated: "use: `reversed(toOpenArray(a, first, last))`"`

### rotatedLeft

[ref: #symbol-rotatedleft]

Same as rotateLeft, just with the difference that it does not modify the argument. It creates a new seq instead.

**Input:**
- `arg: openArray[T]`
- `slice: HSlice[int, int]`
- `dist: int`

**Output:** `seq[T]`
**Generic parameters:** `T`

Same as rotateLeft, just with the difference that it does not modify the argument. It creates a new seq instead.

Elements outside of slice will be left unchanged. If an invalid range (HSlice) is passed, it raises IndexDefect.

slice
:   The indices of the element range that should be rotated.

dist
:   The distance in amount of elements that the data should be rotated. Can be negative, can be any number.

**See also:**

* [rotateLeft proc](#rotateLeft,openArray[T],HSlice[int,int],int) for the in-place version of this proc
* [rotatedLeft proc](#rotatedLeft,openArray[T],int) for a version which rotates the whole container

### rotatedLeft

[ref: #symbol-rotatedleft]

Same as rotateLeft, just with the difference that it does not modify the argument. It creates a new seq instead.

**Input:**
- `arg: openArray[T]`
- `dist: int`

**Output:** `seq[T]`
**Generic parameters:** `T`

Same as rotateLeft, just with the difference that it does not modify the argument. It creates a new seq instead.

**See also:**

* [rotateLeft proc](#rotateLeft,openArray[T],int) for the in-place version of this proc
* [rotatedLeft proc](#rotatedLeft,openArray[T],HSlice[int,int],int) for a version which rotates a range

### rotateLeft

[ref: #symbol-rotateleft]

Performs a left rotation on a range of elements. If you want to rotate right, use a negative dist. Specifically, rotateLeft rotates the elements at slice by dist positions.

**Input:**
- `arg: var openArray[T]`
- `slice: HSlice[int, int]`
- `dist: int`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `discardable`

Performs a left rotation on a range of elements. If you want to rotate right, use a negative dist. Specifically, rotateLeft rotates the elements at slice by dist positions.

The element at index slice.a + dist will be at index slice.a.  
The element at index slice.b will be at slice.a + dist - 1.  
The element at index slice.a will be at slice.b + 1 - dist.  
The element at index slice.a + dist - 1 will be at slice.b.

Elements outside of slice will be left unchanged. The time complexity is linear to slice.b - slice.a + 1. If an invalid range (HSlice) is passed, it raises IndexDefect.

slice
:   The indices of the element range that should be rotated.

dist
:   The distance in amount of elements that the data should be rotated. Can be negative, can be any number.

**See also:**

* [rotateLeft proc](#rotateLeft,openArray[T],int) for a version which rotates the whole container
* [rotatedLeft proc](#rotatedLeft,openArray[T],HSlice[int,int],int) for a version which returns a seq[T]

### rotateLeft

[ref: #symbol-rotateleft]

Same as rotateLeft, but with default arguments for slice, so that this procedure operates on the entire arg, and not just on a part of it.

**Input:**
- `arg: var openArray[T]`
- `dist: int`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `discardable`

Same as rotateLeft, but with default arguments for slice, so that this procedure operates on the entire arg, and not just on a part of it.

**See also:**

* [rotateLeft proc](#rotateLeft,openArray[T],HSlice[int,int],int) for a version which rotates a range
* [rotatedLeft proc](#rotatedLeft,openArray[T],int) for a version which returns a seq[T]

### sort

[ref: #symbol-sort]

Default Nim sort (an implementation of merge sort). The sorting is guaranteed to be stable (that is, equal elements stay in the same order) and the worst case is guaranteed to be O(n log n). Sorts by cmp in the specified order.

**Input:**
- `a: var openArray[T]`
- `cmp: proc (x, y: T): int {.closure.}`
- `order:  = SortOrder.Ascending`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `effectsOf: cmp`

Default Nim sort (an implementation of merge sort). The sorting is guaranteed to be stable (that is, equal elements stay in the same order) and the worst case is guaranteed to be O(n log n). Sorts by cmp in the specified order.

The current implementation uses an iterative mergesort to achieve this. It uses a temporary sequence of length a.len div 2. If you do not wish to provide your own cmp, you may use system.cmp or instead call the overloaded version of sort, which uses system.cmp.

```
sort(myIntArray, system.cmp[int])
# do not use cmp[string] here as we want to use the specialized
# overload:
sort(myStrArray, system.cmp)
```

You can inline adhoc comparison procs with the [do notation](manual.html#procedures-do-notation). Example:

```
people.sort do (x, y: Person) -> int:
  result = cmp(x.surname, y.surname)
  if result == 0:
    result = cmp(x.name, y.name)
```

**See also:**

* [sort proc](#sort,openArray[T])
* [sorted proc](#sorted,openArray[T],proc(T,T)) sorted by cmp in the specified order
* [sorted proc](#sorted,openArray[T])
* [sortedByIt template](#sortedByIt.t,untyped,untyped)

### sort

[ref: #symbol-sort]

Shortcut version of sort that uses system.cmp[T] as the comparison function.

**Input:**
- `a: var openArray[T]`
- `order:  = SortOrder.Ascending`

**Output:** *(none)*
**Generic parameters:** `T`

Shortcut version of sort that uses system.cmp[T] as the comparison function.

**See also:**

* [sort func](#sort,openArray[T],proc(T,T))
* [sorted proc](#sorted,openArray[T],proc(T,T)) sorted by cmp in the specified order
* [sorted proc](#sorted,openArray[T])
* [sortedByIt template](#sortedByIt.t,untyped,untyped)

### sorted

[ref: #symbol-sorted]

Returns a sorted by cmp in the specified order.

**Input:**
- `a: openArray[T]`
- `cmp: proc (x, y: T): int {.closure.}`
- `order:  = SortOrder.Ascending`

**Output:** `seq[T]`
**Generic parameters:** `T`

**Pragmas:** `effectsOf: cmp`

Returns a sorted by cmp in the specified order.

**See also:**

* [sort func](#sort,openArray[T],proc(T,T))
* [sort proc](#sort,openArray[T])
* [sortedByIt template](#sortedByIt.t,untyped,untyped)

### sorted

[ref: #symbol-sorted]

Shortcut version of sorted that uses system.cmp[T] as the comparison function.

**Input:**
- `a: openArray[T]`
- `order:  = SortOrder.Ascending`

**Output:** `seq[T]`
**Generic parameters:** `T`

Shortcut version of sorted that uses system.cmp[T] as the comparison function.

**See also:**

* [sort func](#sort,openArray[T],proc(T,T))
* [sort proc](#sort,openArray[T])
* [sortedByIt template](#sortedByIt.t,untyped,untyped)

### upperBound

[ref: #symbol-upperbound]

Returns the index of the first element in a that is greater than key, or last if no such element is found. In other words if you have a sorted sequence and you call insert(thing, elm, upperBound(thing, elm)) the sequence will still be sorted. Assumes that a is sorted according to cmp.

**Input:**
- `a: openArray[T]`
- `key: K`
- `cmp: proc (x: T; k: K): int {.closure.}`

**Output:** `int`
**Generic parameters:** `T`, `K`

**Pragmas:** `effectsOf: cmp`

Returns the index of the first element in a that is greater than key, or last if no such element is found. In other words if you have a sorted sequence and you call insert(thing, elm, upperBound(thing, elm)) the sequence will still be sorted. Assumes that a is sorted according to cmp.

If an invalid range is passed, it raises IndexDefect.

This version uses cmp to compare the elements. The expected return values are the same as those of system.cmp.

**See also:**

* [lowerBound proc](#lowerBound,openArray[T],K,proc(T,K)) sorted by cmp in the specified order
* [lowerBound proc](#lowerBound,openArray[T],T)

### upperBound

[ref: #symbol-upperbound]

Returns the index of the first element in a that is greater than key, or last if no such element is found. In other words if you have a sorted sequence and you call insert(thing, elm, upperBound(thing, elm)) the sequence will still be sorted. Assumes that a is sorted.

**Input:**
- `a: openArray[T]`
- `key: T`

**Output:** `int`
**Generic parameters:** `T`

Returns the index of the first element in a that is greater than key, or last if no such element is found. In other words if you have a sorted sequence and you call insert(thing, elm, upperBound(thing, elm)) the sequence will still be sorted. Assumes that a is sorted.

This version uses the default comparison function cmp.

**See also:**

* [lowerBound proc](#lowerBound,openArray[T],K,proc(T,K)) sorted by cmp in the specified order
* [lowerBound proc](#lowerBound,openArray[T],T)

## Template

### sortedByIt

[ref: #symbol-sortedbyit]

Convenience template around the sorted proc to reduce typing.

**Input:**
- `seq1: untyped`
- `op: untyped`

**Output:** `untyped`
Convenience template around the sorted proc to reduce typing.

The template injects the it variable which you can use directly in an expression.

Because the underlying cmp() is defined for tuples you can also do a nested sort.

**See also:**

* [sort func](#sort,openArray[T],proc(T,T))
* [sort proc](#sort,openArray[T])
* [sorted proc](#sorted,openArray[T],proc(T,T)) sorted by cmp in the specified order
* [sorted proc](#sorted,openArray[T])

## Type

### SortOrder

[ref: #symbol-sortorder]

```nim
SortOrder = enum
  Descending, Ascending
```
