---
source_hash: 162643718a1bce1f
source_path: lib/pure/collections/sequtils.nim
---

### anyIt

[ref: #symbol-anyit]

Iterates through a container and checks if at least one item fulfills the predicate.

**Input:**
- `s: untyped`
- `pred: untyped`

**Output:** `bool`
Iterates through a container and checks if at least one item fulfills the predicate.

Unlike the [any proc](#any,openArray[T],proc(T)), the predicate needs to be an expression using the it variable for testing, like: anyIt("abba", it == 'a').

**See also:**

* [any proc](#any,openArray[T],proc(T))
* [allIt template](#allIt.t,untyped,untyped)

### applyIt

[ref: #symbol-applyit]

Convenience template around the mutable apply proc to reduce typing.

**Input:**
- `varSeq: untyped`
- `op: untyped`

**Output:** *(none)*
Convenience template around the mutable apply proc to reduce typing.

The template injects the it variable which you can use directly in an expression. The expression has to return the same type as the elements of the sequence you are mutating.

**See also:**

* [apply proc](#apply,openArray[T],proc(T)_2)
* [mapIt template](#mapIt.t,typed,untyped)

### countIt

[ref: #symbol-countit]

Returns a count of all the items that fulfill the predicate.

**Input:**
- `s: untyped`
- `pred: untyped`

**Output:** `int`
Returns a count of all the items that fulfill the predicate.

The predicate needs to be an expression using the it variable for testing, like: countIt(@[1, 2, 3], it > 2).

### filterIt

[ref: #symbol-filterit]

Returns a new sequence with all the items of s that fulfill the predicate pred.

**Input:**
- `s: untyped`
- `pred: untyped`

**Output:** `untyped`
Returns a new sequence with all the items of s that fulfill the predicate pred.

Unlike the [filter proc](#filter,openArray[T],proc(T)) and [filter iterator](#filter.i,openArray[T],proc(T)), the predicate needs to be an expression using the it variable for testing, like: filterIt("abcxyz", it == 'x').

Instead of using mapIt and filterIt, consider using the collect macro from the sugar module.

**See also:**

* [sugar.collect macro](sugar.html#collect.m%2Cuntyped%2Cuntyped)
* [filter proc](#filter,openArray[T],proc(T))
* [filter iterator](#filter.i,openArray[T],proc(T))

### findIt

[ref: #symbol-findit]

Iterates through a container and returns the index of the first item that fulfills the predicate, or -1

**Input:**
- `s: untyped`
- `predicate: untyped`

**Output:** `int`
Iterates through a container and returns the index of the first item that fulfills the predicate, or -1

Unlike the find, the predicate needs to be an expression using the it variable for testing, like: findIt([3, 2, 1], it == 2).

### foldl

[ref: #symbol-foldl]

Template to fold a sequence from left to right, returning the accumulation.

**Input:**
- `sequence: untyped`
- `operation: untyped`

**Output:** `untyped`
Template to fold a sequence from left to right, returning the accumulation.

The sequence is required to have at least a single element. Debug versions of your program will assert in this situation but release versions will happily go ahead. If the sequence has a single element it will be returned without applying operation.

The operation parameter should be an expression which uses the variables a and b for each step of the fold. Since this is a left fold, for non associative binary operations like subtraction think that the sequence of numbers 1, 2 and 3 will be parenthesized as (((1) - 2) - 3).

**See also:**

* [foldl template](#foldl.t,,,) with a starting parameter
* [foldr template](#foldr.t,untyped,untyped)

### foldl

[ref: #symbol-foldl]

Template to fold a sequence from left to right, returning the accumulation.

**Input:**
- `sequence: `
- `operation: `
- `first: `

**Output:** `untyped`
Template to fold a sequence from left to right, returning the accumulation.

This version of foldl gets a **starting parameter**. This makes it possible to accumulate the sequence into a different type than the sequence elements.

The operation parameter should be an expression which uses the variables a and b for each step of the fold. The first parameter is the start value (the first a) and therefore defines the type of the result.

**See also:**

* [foldr template](#foldr.t,untyped,untyped)

### foldr

[ref: #symbol-foldr]

Template to fold a sequence from right to left, returning the accumulation.

**Input:**
- `sequence: untyped`
- `operation: untyped`

**Output:** `untyped`
Template to fold a sequence from right to left, returning the accumulation.

The sequence is required to have at least a single element. Debug versions of your program will assert in this situation but release versions will happily go ahead. If the sequence has a single element it will be returned without applying operation.

The operation parameter should be an expression which uses the variables a and b for each step of the fold. Since this is a right fold, for non associative binary operations like subtraction think that the sequence of numbers 1, 2 and 3 will be parenthesized as (1 - (2 - (3))).

**See also:**

* [foldl template](#foldl.t,untyped,untyped)
* [foldl template](#foldl.t,,,) with a starting parameter

### keepItIf

[ref: #symbol-keepitif]

Keeps the items in the passed sequence (must be declared as a var) if they fulfill the predicate.

**Input:**
- `varSeq: seq`
- `pred: untyped`

**Output:** *(none)*
**Generic parameters:** `seq`

Keeps the items in the passed sequence (must be declared as a var) if they fulfill the predicate.

Unlike the [keepIf proc](#keepIf,seq[T],proc(T)), the predicate needs to be an expression using the it variable for testing, like: keepItIf("abcxyz", it == 'x').

**See also:**

* [keepIf proc](#keepIf,seq[T],proc(T))
* [filterIt template](#filterIt.t,untyped,untyped)

### mapIt

[ref: #symbol-mapit]

Returns a new sequence with the results of the op proc applied to every item in the container s.

**Input:**
- `s: typed`
- `op: untyped`

**Output:** `untyped`
Returns a new sequence with the results of the op proc applied to every item in the container s.

Since the input is not modified you can use it to transform the type of the elements in the input container.

The template injects the it variable which you can use directly in an expression.

Instead of using mapIt and filterIt, consider using the collect macro from the sugar module.

**See also:**

* [sugar.collect macro](sugar.html#collect.m%2Cuntyped%2Cuntyped)
* [map proc](#map,openArray[T],proc(T))
* [applyIt template](#applyIt.t,untyped,untyped) for the in-place version

### newSeqWith

[ref: #symbol-newseqwith]

Creates a new seq of length len, calling init to initialize each value of the seq.

**Input:**
- `len: int`
- `init: untyped`

**Output:** `untyped`
Creates a new seq of length len, calling init to initialize each value of the seq.

Useful for creating "2D" seqs - seqs containing other seqs or to populate fields of the created seq.

### toSeq

[ref: #symbol-toseq]

**Input:**
- `iter: untyped`

**Output:** `untyped`
Transforms any iterable (anything that can be iterated over, e.g. with a for-loop) into a sequence.

[Prev](sequtils_1.md)
