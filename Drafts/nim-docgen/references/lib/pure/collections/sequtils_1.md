---
source_hash: 162643718a1bce1f
source_path: lib/pure/collections/sequtils.nim
---

# sequtils

[ref: #module-sequtils]

Although this module has seq in its name, it implements operations not only for the seq type, but for three built-in container types under the openArray umbrella:

* sequences
* strings
* array

The system module defines several common functions, such as:

* newSeq[T] for creating new sequences of type T
* @ for converting arrays and strings to sequences
* add for adding new elements to strings and sequences
* & for string and seq concatenation
* in (alias for contains) and notin for checking if an item is in a container

This module builds upon that, providing additional functionality in form of procs, iterators and templates inspired by functional programming languages.

For functional style programming you have different options at your disposal:

* the [sugar.collect macro](sugar.html#collect.m%2Cuntyped%2Cuntyped)
* pass an [anonymous proc](manual.html#procedures-anonymous-procs)
* import the [sugar module](sugar.html) and use the [=> macro](sugar.html#%3D>.m,untyped,untyped)
* use [...It templates](#18) ([mapIt](#mapIt.t,typed,untyped), [filterIt](#filterIt.t,untyped,untyped), etc.)

Chaining of functions is possible thanks to the [method call syntax](manual.html#procedures-method-call-syntax).

# [See also](#see-also)

* [strutils module](strutils.html) for common string functions
* [sugar module](sugar.html) for syntactic sugar macros
* [algorithm module](algorithm.html) for common generic algorithms
* [json module](json.html) for a structure which allows heterogeneous members

## Examples

```nim
import std/sequtils
import std/sugar

# Creating a sequence from 1 to 10, multiplying each member by 2,
# keeping only the members which are not divisible by 6.
let
  foo = toSeq(1..10).map(x => x * 2).filter(x => x mod 6 != 0)
  bar = toSeq(1..10).mapIt(it * 2).filterIt(it mod 6 != 0)
  baz = collect:
    for i in 1..10:
      let j = 2 * i
      if j mod 6 != 0:
        j

doAssert foo == bar
doAssert foo == baz
doAssert foo == @[2, 4, 8, 10, 14, 16, 20]

doAssert foo.any(x => x > 17)
doAssert not bar.allIt(it < 20)
doAssert foo.foldl(a + b) == 74 # sum of all members
```

```nim
import std/sequtils
from std/strutils import join

let
  vowels = @"aeiou"
  foo = "sequtils is an awesome module"

doAssert (vowels is seq[char]) and (vowels == @['a', 'e', 'i', 'o', 'u'])
doAssert foo.filterIt(it notin vowels).join == "sqtls s n wsm mdl"
```

```nim
var a = @[1, 2, 3]
a.addUnique(4)
a.addUnique(4)
assert a == @[1, 2, 3, 4]
```

```nim
let numbers = @[1, 4, 5, 8, 9, 7, 4]
assert all(numbers, proc (x: int): bool = x < 10) == true
assert all(numbers, proc (x: int): bool = x < 9) == false
```

```nim
let numbers = @[1, 4, 5, 8, 9, 7, 4]
assert any(numbers, proc (x: int): bool = x > 8) == true
assert any(numbers, proc (x: int): bool = x > 9) == false
```

```nim
var message: string
apply([0, 1, 2, 3, 4], proc(item: int) = message.addInt item)
assert message == "01234"
```

```nim
var a = @["1", "2", "3", "4"]
apply(a, proc(x: string): string = x & "42")
assert a == @["142", "242", "342", "442"]
```

```nim
var a = @["1", "2", "3", "4"]
apply(a, proc(x: var string) = x &= "42")
assert a == @["142", "242", "342", "442"]
```

```nim
let
  s1 = @[1, 2, 3]
  s2 = @[4, 5]
  s3 = @[6, 7]
  total = concat(s1, s2, s3)
assert total == @[1, 2, 3, 4, 5, 6, 7]
```

```nim
let
  a = @[1, 2, 2, 3, 2, 4, 2]
  b = "abracadabra"
assert count(a, 2) == 4
assert count(a, 99) == 0
assert count(b, 'r') == 2
```

```nim
let
  s = @[1, 2, 3]
  total = s.cycle(3)
assert total == @[1, 2, 3, 1, 2, 3, 1, 2, 3]
```

```nim
let
  dup1 = @[1, 1, 3, 4, 2, 2, 8, 1, 4]
  dup2 = @["a", "a", "c", "d", "d"]
  unique1 = deduplicate(dup1)
  unique2 = deduplicate(dup2, isSorted = true)
assert unique1 == @[1, 3, 4, 2, 8]
assert unique2 == @["a", "c", "d"]
```

```nim
let outcome = @[1, 1, 1, 1, 1, 1, 1, 1]
var dest = @[1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
dest.delete(3, 8)
assert outcome == dest
```

```nim
var a = @[10, 11, 12, 13, 14]
doAssertRaises(IndexDefect): a.delete(4..5)
assert a == @[10, 11, 12, 13, 14]
a.delete(4..4)
assert a == @[10, 11, 12, 13]
a.delete(1..2)
assert a == @[10, 13]
a.delete(1..<1) # empty slice
assert a == @[10, 13]
```

```nim
let numbers = @[1, 2, 3, 4, 5, 6, 7]
assert numbers.distribute(3) == @[@[1, 2, 3], @[4, 5], @[6, 7]]
assert numbers.distribute(3, false) == @[@[1, 2, 3], @[4, 5, 6], @[7]]
assert numbers.distribute(6)[0] == @[1, 2]
assert numbers.distribute(6)[1] == @[3]
```

```nim
let
  colors = @["red", "yellow", "black"]
  f1 = filter(colors, proc(x: string): bool = x.len < 6)
  f2 = filter(colors, proc(x: string): bool = x.contains('y'))
assert f1 == @["red", "black"]
assert f2 == @["yellow"]
```

```nim
var dest = @[1, 1, 1, 1, 1, 1, 1, 1]
let
  src = @[2, 2, 2, 2, 2, 2]
  outcome = @[1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
dest.insert(src, 3)
assert dest == outcome
```

```nim
var floats = @[13.0, 12.5, 5.8, 2.0, 6.1, 9.9, 10.1]
keepIf(floats, proc(x: float): bool = x > 10)
assert floats == @[13.0, 12.5, 10.1]
```

```nim
let
  a = @[1, 2, 3, 4]
  b = map(a, proc(x: int): string = $x)
assert b == @["1", "2", "3", "4"]
```

```nim
let
  a = @[1, 2, 3, 4]
  b = @[6, 5, 4, 3]
  c = [2, -7, 8, -5]
  d = "ziggy"
assert maxIndex(a) == 3
assert maxIndex(b) == 0
assert maxIndex(c) == 2
assert maxIndex(d) == 0
```

```nim
import std/sugar

let s1 = @["foo","bar", "hello"]
let s2 = @[2..4, 1..3, 6..10]
assert maxIndex(s1, proc (a, b: string): int = a.len - b.len) == 2
assert maxIndex(s2, (a, b) => a.a - b.a) == 2
```

```nim
let
  a = @[1, 2, 3, 4]
  b = @[6, 5, 4, 3]
  c = [2, -7, 8, -5]
  d = "ziggy"
assert minIndex(a) == 0
assert minIndex(b) == 3
assert minIndex(c) == 1
assert minIndex(d) == 2
```

```nim
import std/sugar

let s1 = @["foo","bar", "hello"]
let s2 = @[2..4, 1..3, 6..10]
assert minIndex(s1, proc (a, b: string): int = a.len - b.len) == 0
assert minIndex(s2, (a, b) => a.a - b.a) == 1
```

```nim
let
  total = repeat(5, 3)
assert total == @[5, 5, 5]
```

```nim
let
  zipped = @[(1, 'a'), (2, 'b'), (3, 'c')]
  unzipped1 = @[1, 2, 3]
  unzipped2 = @['a', 'b', 'c']
assert zipped.unzip() == (unzipped1, unzipped2)
assert zip(unzipped1, unzipped2).unzip() == (unzipped1, unzipped2)
```

```nim
let
  short = @[1, 2, 3]
  long = @[6, 5, 4, 3, 2, 1]
  words = @["one", "two", "three"]
  letters = "abcd"
  zip1 = zip(short, long)
  zip2 = zip(short, words)
assert zip1 == @[(1, 6), (2, 5), (3, 4)]
assert zip2 == @[(1, "one"), (2, "two"), (3, "three")]
assert zip1[2][0] == 3
assert zip2[1][1] == "two"
when (NimMajor, NimMinor) <= (1, 0):
  let
    zip3 = zip(long, letters)
  assert zip3 == @[(a: 6, b: 'a'), (5, 'b'), (4, 'c'), (3, 'd')]
  assert zip3[0].b == 'a'
else:
  let
    zip3: seq[tuple[num: int, letter: char]] = zip(long, letters)
  assert zip3 == @[(6, 'a'), (5, 'b'), (4, 'c'), (3, 'd')]
  assert zip3[0].letter == 'a'
```

```nim
let numbers = @[1, 4, 5, 8, 9, 7, 4]
var evens = newSeq[int]()
for n in filter(numbers, proc (x: int): bool = x mod 2 == 0):
  evens.add(n)
assert evens == @[4, 8, 4]
```

```nim
let x = mapLiterals([0.1, 1.2, 2.3, 3.4], int)
doAssert x is array[4, int]
doAssert x == [int(0.1), int(1.2), int(2.3), int(3.4)]
```

```nim
let a = mapLiterals((1.2, (2.3, 3.4), 4.8), int)
let b = mapLiterals((1.2, (2.3, 3.4), 4.8), int, nested=false)
assert a == (1, (2, 3), 4)
assert b == (1, (2.3, 3.4), 4)

let c = mapLiterals((1, (2, 3), 4, (5, 6)), `$`)
let d = mapLiterals((1, (2, 3), 4, (5, 6)), `$`, nested=false)
assert c == ("1", ("2", "3"), "4", ("5", "6"))
assert d == ("1", (2, 3), "4", (5, 6))
```

```nim
let numbers = @[1, 4, 5, 8, 9, 7, 4]
assert numbers.allIt(it < 10) == true
assert numbers.allIt(it < 9) == false
```

```nim
let numbers = @[1, 4, 5, 8, 9, 7, 4]
assert numbers.anyIt(it > 8) == true
assert numbers.anyIt(it > 9) == false
```

```nim
var nums = @[1, 2, 3, 4]
nums.applyIt(it * 3)
assert nums[0] + nums[3] == 15
```

```nim
let numbers = @[-3, -2, -1, 0, 1, 2, 3, 4, 5, 6]
iterator iota(n: int): int =
  for i in 0..<n: yield i
assert numbers.countIt(it < 0) == 3
assert countIt(iota(10), it < 2) == 2
```

```nim
let
  temperatures = @[-272.15, -2.0, 24.5, 44.31, 99.9, -113.44]
  acceptable = temperatures.filterIt(it < 50 and it > -10)
  notAcceptable = temperatures.filterIt(it > 50 or it < -10)
assert acceptable == @[-2.0, 24.5, 44.31]
assert notAcceptable == @[-272.15, 99.9, -113.44]
```

```nim
let
  numbers = @[0, 8, 1, 5]
  digits = foldl(numbers, a & (chr(b + ord('0'))), "")
assert digits == "0815"
```

```nim
let
  numbers = @[5, 9, 11]
  addition = foldl(numbers, a + b)
  subtraction = foldl(numbers, a - b)
  multiplication = foldl(numbers, a * b)
  words = @["nim", "is", "cool"]
  concatenation = foldl(words, a & b)
  procs = @["proc", "Is", "Also", "Fine"]


func foo(acc, cur: string): string =
  result = acc & cur

assert addition == 25, "Addition is (((5)+9)+11)"
assert subtraction == -15, "Subtraction is (((5)-9)-11)"
assert multiplication == 495, "Multiplication is (((5)*9)*11)"
assert concatenation == "nimiscool"
assert foldl(procs, foo(a, b)) == "procIsAlsoFine"
```

```nim
let
  numbers = @[5, 9, 11]
  addition = foldr(numbers, a + b)
  subtraction = foldr(numbers, a - b)
  multiplication = foldr(numbers, a * b)
  words = @["nim", "is", "cool"]
  concatenation = foldr(words, a & b)
assert addition == 25, "Addition is (5+(9+(11)))"
assert subtraction == 7, "Subtraction is (5-(9-(11)))"
assert multiplication == 495, "Multiplication is (5*(9*(11)))"
assert concatenation == "nimiscool"
```

```nim
var candidates = @["foo", "bar", "baz", "foobar"]
candidates.keepItIf(it.len == 3 and it[0] == 'b')
assert candidates == @["bar", "baz"]
```

```nim
let
  nums = @[1, 2, 3, 4]
  strings = nums.mapIt($(4 * it))
assert strings == @["4", "8", "12", "16"]
```

```nim
## Creates a seq containing 5 bool seqs, each of length of 3.
var seq2D = newSeqWith(5, newSeq[bool](3))
assert seq2D.len == 5
assert seq2D[0].len == 3
assert seq2D[4][2] == false

## Creates a seq with random numbers
import std/random
var seqRand = newSeqWith(20, rand(1.0))
assert seqRand[0] != seqRand[1]
```

```nim
let
  myRange = 1..5
  mySet: set[int8] = {5'i8, 3, 1}
assert typeof(myRange) is HSlice[system.int, system.int]
assert typeof(mySet) is set[int8]

let
  mySeq1 = toSeq(myRange)
  mySeq2 = toSeq(mySet)
assert mySeq1 == @[1, 2, 3, 4, 5]
assert mySeq2 == @[1'i8, 3, 5]
```

## Iterator

### filter

[ref: #symbol-filter]

Iterates through a container s and yields every item that fulfills the predicate pred (a function that returns a bool).

**Input:**
- `s: openArray[T]`
- `pred: proc (x: T): bool {.closure.}`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `effectsOf: pred`

Iterates through a container s and yields every item that fulfills the predicate pred (a function that returns a bool).

Instead of using map and filter, consider using the collect macro from the sugar module.

**See also:**

* [sugar.collect macro](sugar.html#collect.m%2Cuntyped%2Cuntyped)
* [filter proc](#filter,openArray[T],proc(T))
* [filterIt template](#filterIt.t,untyped,untyped)

### items

[ref: #symbol-items]

**Input:**
- `xs: iterator (): T`

**Output:** `T`
**Generic parameters:** `T`

Iterates over each element yielded by a closure iterator. This may not seem particularly useful on its own, but this allows closure iterators to be used by the mapIt, filterIt, allIt, anyIt, etc. templates.

## Macro

### mapLiterals

[ref: #symbol-mapliterals]

**Input:**
- `constructor: untyped`
- `op: untyped`
- `nested:  = true`

**Output:** `untyped`
Applies op to each of the **atomic** literals like 3 or "abc" in the specified constructor AST. This can be used to map every array element to some target type:

## Proc

### addUnique

[ref: #symbol-addunique]

**Input:**
- `s: var seq[T]`
- `x: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

Adds x to the container s if it is not already present. Uses == to check if the item is already present.

### all

[ref: #symbol-all]

Iterates through a container and checks if every item fulfills the predicate.

**Input:**
- `s: openArray[T]`
- `pred: proc (x: T): bool {.closure.}`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `effectsOf: pred`

Iterates through a container and checks if every item fulfills the predicate.

**See also:**

* [allIt template](#allIt.t,untyped,untyped)
* [any proc](#any,openArray[T],proc(T))

### any

[ref: #symbol-any]

Iterates through a container and checks if at least one item fulfills the predicate.

**Input:**
- `s: openArray[T]`
- `pred: proc (x: T): bool {.closure.}`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `effectsOf: pred`

Iterates through a container and checks if at least one item fulfills the predicate.

**See also:**

* [anyIt template](#anyIt.t,untyped,untyped)
* [all proc](#all,openArray[T],proc(T))

### apply

[ref: #symbol-apply]

Applies op to every item in s, modifying it directly.

**Input:**
- `s: var openArray[T]`
- `op: proc (x: var T) {.closure.}`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `effectsOf: op`

Applies op to every item in s, modifying it directly.

Note that the container s must be declared as a var, since s is modified in-place. The parameter function takes a var T type parameter.

**See also:**

* [applyIt template](#applyIt.t,untyped,untyped)
* [map proc](#map,openArray[T],proc(T))

### apply

[ref: #symbol-apply]

Applies op to every item in s modifying it directly.

**Input:**
- `s: var openArray[T]`
- `op: proc (x: T): T {.closure.}`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `effectsOf: op`

Applies op to every item in s modifying it directly.

Note that the container s must be declared as a var and it is required for your input and output types to be the same, since s is modified in-place. The parameter function takes and returns a T type variable.

**See also:**

* [applyIt template](#applyIt.t,untyped,untyped)
* [map proc](#map,openArray[T],proc(T))

### apply

[ref: #symbol-apply]

**Input:**
- `s: openArray[T]`
- `op: proc (x: T) {.closure.}`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `effectsOf: op`

Same as apply but for a proc that does not return anything and does not mutate s directly.

### concat

[ref: #symbol-concat]

Takes several sequences' items and returns them inside a new sequence. All sequences must be of the same type.

**Input:**
- `seqs: varargs[seq[T]]`

**Output:** `seq[T]`
**Generic parameters:** `T`

Takes several sequences' items and returns them inside a new sequence. All sequences must be of the same type.

**See also:**

* [distribute func](#distribute,seq[T],Positive) for a reverse operation

### count

[ref: #symbol-count]

**Input:**
- `s: openArray[T]`
- `x: T`

**Output:** `int`
**Generic parameters:** `T`

Returns the number of occurrences of the item x in the container s.

### cycle

[ref: #symbol-cycle]

**Input:**
- `s: openArray[T]`
- `n: Natural`

**Output:** `seq[T]`
**Generic parameters:** `T`

Returns a new sequence with the items of the container s repeated n times. n must be a non-negative number (zero or more).

### deduplicate

[ref: #symbol-deduplicate]

Returns a new sequence without duplicates.

**Input:**
- `s: openArray[T]`
- `isSorted: bool = false`

**Output:** `seq[T]`
**Generic parameters:** `T`

Returns a new sequence without duplicates.

Setting the optional argument isSorted to true (default: false) uses a faster algorithm for deduplication.

### delete

[ref: #symbol-delete]

Deletes the items s[slice], raising IndexDefect if the slice contains elements out of range.

**Input:**
- `s: var seq[T]`
- `slice: Slice[int]`

**Output:** *(none)*
**Generic parameters:** `T`

Deletes the items s[slice], raising IndexDefect if the slice contains elements out of range.

This operation moves all elements after s[slice] in linear time.

### delete

[ref: #symbol-delete]

**Input:**
- `s: var seq[T]`
- `first: Natural`
- `last: Natural`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `deprecated: "use `delete(s, first..last)`"`

Deletes the items of a sequence s at positions first..last (including both ends of the range). This modifies s itself, it does not return a copy.

### distribute

[ref: #symbol-distribute]

Splits and distributes a sequence s into num sub-sequences.

**Input:**
- `s: seq[T]`
- `num: Positive`
- `spread:  = true`

**Output:** `seq[seq[T]]`
**Generic parameters:** `T`

Splits and distributes a sequence s into num sub-sequences.

Returns a sequence of num sequences. For *some* input values this is the inverse of the [concat](#concat,varargs[seq[T]]) func. The input sequence s can be empty, which will produce num empty sequences.

If spread is false and the length of s is not a multiple of num, the func will max out the first sub-sequence with 1 + len(s) div num entries, leaving the remainder of elements to the last sequence.

On the other hand, if spread is true, the func will distribute evenly the remainder of the division across all sequences, which makes the result more suited to multithreading where you are passing equal sized work units to a thread pool and want to maximize core usage.

### filter

[ref: #symbol-filter]

Returns a new sequence with all the items of s that fulfill the predicate pred (a function that returns a bool).

**Input:**
- `s: openArray[T]`
- `pred: proc (x: T): bool {.closure.}`

**Output:** `seq[T]`
**Generic parameters:** `T`

**Pragmas:** `inline`, `effectsOf: pred`

Returns a new sequence with all the items of s that fulfill the predicate pred (a function that returns a bool).

Instead of using map and filter, consider using the collect macro from the sugar module.

**See also:**

* [sugar.collect macro](sugar.html#collect.m%2Cuntyped%2Cuntyped)
* [filterIt template](#filterIt.t,untyped,untyped)
* [filter iterator](#filter.i,openArray[T],proc(T))
* [keepIf proc](#keepIf,seq[T],proc(T)) for the in-place version

### insert

[ref: #symbol-insert]

Inserts items from src into dest at position pos. This modifies dest itself, it does not return a copy.

**Input:**
- `dest: var seq[T]`
- `src: openArray[T]`
- `pos:  = 0`

**Output:** *(none)*
**Generic parameters:** `T`

Inserts items from src into dest at position pos. This modifies dest itself, it does not return a copy.

Note that the elements of src and dest must be of the same type.

### keepIf

[ref: #symbol-keepif]

Keeps the items in the passed sequence s if they fulfill the predicate pred (a function that returns a bool).

**Input:**
- `s: var seq[T]`
- `pred: proc (x: T): bool {.closure.}`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `effectsOf: pred`

Keeps the items in the passed sequence s if they fulfill the predicate pred (a function that returns a bool).

Note that s must be declared as a var.

Similar to the [filter proc](#filter,openArray[T],proc(T)), but modifies the sequence directly.

**See also:**

* [keepItIf template](#keepItIf.t,seq,untyped)
* [filter proc](#filter,openArray[T],proc(T))

### map

[ref: #symbol-map]

Returns a new sequence with the results of the op proc applied to every item in the container s.

**Input:**
- `s: openArray[T]`
- `op: proc (x: T): S {.closure.}`

**Output:** `seq[S]`
**Generic parameters:** `T`, `S`

**Pragmas:** `inline`, `effectsOf: op`

Returns a new sequence with the results of the op proc applied to every item in the container s.

Since the input is not modified, you can use it to transform the type of the elements in the input container.

Instead of using map and filter, consider using the collect macro from the sugar module.

**See also:**

* [sugar.collect macro](sugar.html#collect.m%2Cuntyped%2Cuntyped)
* [mapIt template](#mapIt.t,typed,untyped)
* [apply proc](#apply,openArray[T],proc(T)_2) for the in-place version

### max

[ref: #symbol-max]

**Input:**
- `x: openArray[T]`
- `cmp: proc (a, b: T): int`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `effectsOf: cmp`

The maximum value of x.

### maxIndex

[ref: #symbol-maxindex]

**Input:**
- `s: openArray[T]`

**Output:** `int`
**Generic parameters:** `T`

Returns the index of the maximum value of s. T needs to have a < operator.

### maxIndex

[ref: #symbol-maxindex]

**Input:**
- `s: openArray[T]`
- `cmp: proc (a, b: T): int`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `effectsOf: cmp`

Returns the index of the maximum value of s.

### min

[ref: #symbol-min]

**Input:**
- `x: openArray[T]`
- `cmp: proc (a, b: T): int`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `effectsOf: cmp`

The minimum value of x.

### minIndex

[ref: #symbol-minindex]

**Input:**
- `s: openArray[T]`

**Output:** `int`
**Generic parameters:** `T`

Returns the index of the minimum value of s. T needs to have a < operator.

### minIndex

[ref: #symbol-minindex]

**Input:**
- `s: openArray[T]`
- `cmp: proc (a, b: T): int`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `effectsOf: cmp`

Returns the index of the minimum value of s.

### minmax

[ref: #symbol-minmax]

**Input:**
- `x: openArray[T]`

**Output:** `(T, T)`
**Generic parameters:** `T`

The minimum and maximum values of x. T needs to have a < operator.

### minmax

[ref: #symbol-minmax]

**Input:**
- `x: openArray[T]`
- `cmp: proc (a, b: T): int`

**Output:** `(T, T)`
**Generic parameters:** `T`

**Pragmas:** `effectsOf: cmp`

The minimum and maximum values of x.

### repeat

[ref: #symbol-repeat]

**Input:**
- `x: T`
- `n: Natural`

**Output:** `seq[T]`
**Generic parameters:** `T`

Returns a new sequence with the item x repeated n times. n must be a non-negative number (zero or more).

### unzip

[ref: #symbol-unzip]

**Input:**
- `s: openArray[(S, T)]`

**Output:** `(seq[S], seq[T])`
**Generic parameters:** `S`, `T`

Returns a tuple of two sequences split out from a sequence of 2-field tuples.

### zip

[ref: #symbol-zip]

Returns a new sequence with a combination of the two input containers.

**Input:**
- `s1: openArray[S]`
- `s2: openArray[T]`

**Output:** `seq[(S, T)]`
**Generic parameters:** `S`, `T`

Returns a new sequence with a combination of the two input containers.

The input containers can be of different types. If one container is shorter, the remaining items in the longer container are discarded.

**Note**: For Nim 1.0.x and older version, zip returned a seq of named tuples with fields a and b. For Nim versions 1.1.x and newer, zip returns a seq of unnamed tuples.

## Template

### allIt

[ref: #symbol-allit]

Iterates through a container and checks if every item fulfills the predicate.

**Input:**
- `s: untyped`
- `pred: untyped`

**Output:** `bool`
Iterates through a container and checks if every item fulfills the predicate.

Unlike the [all proc](#all,openArray[T],proc(T)), the predicate needs to be an expression using the it variable for testing, like: allIt("abba", it == 'a').

**See also:**

* [all proc](#all,openArray[T],proc(T))
* [anyIt template](#anyIt.t,untyped,untyped)


[Next](sequtils_2.md)
