---
source_hash: 7497f90741c73172
source_path: lib/pure/collections/deques.nim
---

# deques

[ref: #module-deques]

An implementation of a deque (double-ended queue). The underlying implementation uses a seq.

**Note:**
None of the procs that get an individual value from the deque should be used on an empty deque.

If compiled with the boundChecks option, those procs will raise an IndexDefect on such access. This should not be relied upon, as -d:danger or --checks:off will disable those checks and then the procs may return garbage or crash the program.

As such, a check to see if the deque is empty is needed before any access, unless your program logic guarantees it indirectly.

# [See also](#see-also)

* [lists module](lists.html) for singly and doubly linked lists and rings

## Examples

```nim
import std/deques
var a = [10, 20, 30, 40].toDeque

doAssertRaises(IndexDefect, echo a[4])

a.addLast(50)
assert $a == "[10, 20, 30, 40, 50]"

assert a.peekFirst == 10
assert a.peekLast == 50
assert len(a) == 5

assert a.popFirst == 10
assert a.popLast == 50
assert len(a) == 3

a.addFirst(11)
a.addFirst(22)
a.addFirst(33)
assert $a == "[33, 22, 11, 20, 30, 40]"

a.shrink(fromFirst = 1, fromLast = 2)
assert $a == "[22, 11, 20]"
```

```nim
let a = [10, 20, 30].toDeque
assert $a == "[10, 20, 30]"
```

```nim
var a, b = initDeque[int]()
a.addFirst(2)
a.addFirst(1)
b.addLast(1)
b.addLast(2)
doAssert a == b
```

```nim
let a = [10, 20, 30, 40, 50].toDeque
assert a[^1] == 50
assert a[^4] == 20
doAssertRaises(IndexDefect, echo a[^9])
```

```nim
let a = [10, 20, 30, 40, 50].toDeque
assert a[0] == 10
assert a[3] == 40
doAssertRaises(IndexDefect, echo a[8])
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
inc(a[^1])
assert a[^1] == 51
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
inc(a[0])
assert a[0] == 11
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
a[^1] = 99
a[^3] = 77
assert $a == "[10, 20, 77, 40, 99]"
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
a[0] = 99
a[3] = 66
assert $a == "[99, 20, 30, 66, 50]"
```

```nim
var a = initDeque[int]()
for i in 1 .. 5:
  a.addFirst(10 * i)
assert $a == "[50, 40, 30, 20, 10]"
```

```nim
var a = initDeque[int]()
for i in 1 .. 5:
  a.addLast(10 * i)
assert $a == "[10, 20, 30, 40, 50]"
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
assert $a == "[10, 20, 30, 40, 50]"
clear(a)
assert len(a) == 0
```

```nim
let q = [7, 9].toDeque
assert 7 in q
assert q.contains(7)
assert 8 notin q
```

```nim
let a = [10, 20, 30, 40, 50].toDeque
assert $a == "[10, 20, 30, 40, 50]"
assert a.peekFirst == 10
assert len(a) == 5
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
a.peekFirst() = 99
assert $a == "[99, 20, 30, 40, 50]"
```

```nim
let a = [10, 20, 30, 40, 50].toDeque
assert $a == "[10, 20, 30, 40, 50]"
assert a.peekLast == 50
assert len(a) == 5
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
a.peekLast() = 99
assert $a == "[10, 20, 30, 40, 99]"
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
assert $a == "[10, 20, 30, 40, 50]"
assert a.popFirst == 10
assert $a == "[20, 30, 40, 50]"
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
assert $a == "[10, 20, 30, 40, 50]"
assert a.popLast == 50
assert $a == "[10, 20, 30, 40]"
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
assert $a == "[10, 20, 30, 40, 50]"
a.shrink(fromFirst = 2, fromLast = 1)
assert $a == "[30, 40]"
```

```nim
let a = toDeque([7, 8, 9])
assert len(a) == 3
assert $a == "[7, 8, 9]"
```

```nim
from std/sequtils import toSeq

let a = [10, 20, 30, 40, 50].toDeque
assert toSeq(a.items) == @[10, 20, 30, 40, 50]
```

```nim
var a = [10, 20, 30, 40, 50].toDeque
assert $a == "[10, 20, 30, 40, 50]"
for x in mitems(a):
  x = 5 * x - 1
assert $a == "[49, 99, 149, 199, 249]"
```

```nim
from std/sequtils import toSeq

let a = [10, 20, 30].toDeque
assert toSeq(a.pairs) == @[(0, 10), (1, 20), (2, 30)]
```

## Const

### defaultInitialSize

[ref: #symbol-defaultinitialsize]

```nim
defaultInitialSize = 4
```

## Iterator

### items

[ref: #symbol-items]

Yields every element of deq.

**Input:**
- `deq: Deque[T]`

**Output:** `lent T`
**Generic parameters:** `T`

Yields every element of deq.

**See also:**

* [mitems iterator](#mitems.i,Deque[T])

### mitems

[ref: #symbol-mitems]

Yields every element of deq, which can be modified.

**Input:**
- `deq: var Deque[T]`

**Output:** `var T`
**Generic parameters:** `T`

Yields every element of deq, which can be modified.

**See also:**

* [items iterator](#items.i,Deque[T])

### pairs

[ref: #symbol-pairs]

**Input:**
- `deq: Deque[T]`

**Output:** `tuple[key: int, val: T]`
**Generic parameters:** `T`

Yields every (position, value)-pair of deq.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `deq: Deque[T]`

**Output:** `string`
**Generic parameters:** `T`

Turns a deque into its string representation.

### `==`

[ref: #symbol-]

**Input:**
- `deq1: Deque[T]`
- `deq2: Deque[T]`

**Output:** `bool`
**Generic parameters:** `T`

The == operator for Deque. Returns true if both deques contains the same values in the same order.

### `[]=`

[ref: #symbol-]

**Input:**
- `deq: var Deque[T]`
- `i: Natural`
- `val: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Sets the i-th element of deq to val.

### `[]=`

[ref: #symbol-]

Sets the backwards indexed i-th element of deq to x.

**Input:**
- `deq: var Deque[T]`
- `i: BackwardsIndex`
- `x: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Sets the backwards indexed i-th element of deq to x.

deq[^1] is the last element.

### `[]`

[ref: #symbol-]

**Input:**
- `deq: Deque[T]`
- `i: Natural`

**Output:** `lent T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Accesses the i-th element of deq.

### `[]`

[ref: #symbol-]

**Input:**
- `deq: var Deque[T]`
- `i: Natural`

**Output:** `var T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Accesses the i-th element of deq and returns a mutable reference to it.

### `[]`

[ref: #symbol-]

Accesses the backwards indexed i-th element.

**Input:**
- `deq: Deque[T]`
- `i: BackwardsIndex`

**Output:** `lent T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Accesses the backwards indexed i-th element.

deq[^1] is the last element.

### `[]`

[ref: #symbol-]

Accesses the backwards indexed i-th element and returns a mutable reference to it.

**Input:**
- `deq: var Deque[T]`
- `i: BackwardsIndex`

**Output:** `var T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Accesses the backwards indexed i-th element and returns a mutable reference to it.

deq[^1] is the last element.

### addFirst

[ref: #symbol-addfirst]

Adds an item to the beginning of deq.

**Input:**
- `deq: var Deque[T]`
- `item: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

Adds an item to the beginning of deq.

**See also:**

* [addLast proc](#addLast,Deque[T],sinkT)

### addLast

[ref: #symbol-addlast]

Adds an item to the end of deq.

**Input:**
- `deq: var Deque[T]`
- `item: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

Adds an item to the end of deq.

**See also:**

* [addFirst proc](#addFirst,Deque[T],sinkT)

### clear

[ref: #symbol-clear]

Resets the deque so that it is empty.

**Input:**
- `deq: var Deque[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Resets the deque so that it is empty.

**See also:**

* [shrink proc](#shrink,Deque[T],int,int)

### contains

[ref: #symbol-contains]

Returns true if item is in deq or false if not found.

**Input:**
- `deq: Deque[T]`
- `item: T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns true if item is in deq or false if not found.

Usually used via the in operator. It is the equivalent of deq.find(item) >= 0.

### hash

[ref: #symbol-hash]

**Input:**
- `deq: Deque[T]`

**Output:** `Hash`
**Generic parameters:** `T`

Hashing of Deque.

### initDeque

[ref: #symbol-initdeque]

Creates a new empty deque.

**Input:**
- `initialSize: int = defaultInitialSize`

**Output:** `Deque[T]`
**Generic parameters:** `T`

Creates a new empty deque.

Optionally, the initial capacity can be reserved via initialSize as a performance optimization (default: [defaultInitialSize](#defaultInitialSize)). The length of a newly created deque will still be 0.

**See also:**

* [toDeque proc](#toDeque,openArray[T])

### len

[ref: #symbol-len]

**Input:**
- `deq: Deque[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the number of elements of deq.

### peekFirst

[ref: #symbol-peekfirst]

Returns the first element of deq, but does not remove it from the deque.

**Input:**
- `deq: Deque[T]`

**Output:** `lent T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the first element of deq, but does not remove it from the deque.

**See also:**

* [peekFirst proc](#peekFirst,Deque[T]_2) which returns a mutable reference
* [peekLast proc](#peekLast,Deque[T])

### peekFirst

[ref: #symbol-peekfirst]

Returns a mutable reference to the first element of deq, but does not remove it from the deque.

**Input:**
- `deq: var Deque[T]`

**Output:** `var T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns a mutable reference to the first element of deq, but does not remove it from the deque.

**See also:**

* [peekFirst proc](#peekFirst,Deque[T])
* [peekLast proc](#peekLast,Deque[T]_2)

### peekLast

[ref: #symbol-peeklast]

Returns the last element of deq, but does not remove it from the deque.

**Input:**
- `deq: Deque[T]`

**Output:** `lent T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the last element of deq, but does not remove it from the deque.

**See also:**

* [peekLast proc](#peekLast,Deque[T]_2) which returns a mutable reference
* [peekFirst proc](#peekFirst,Deque[T])

### peekLast

[ref: #symbol-peeklast]

Returns a mutable reference to the last element of deq, but does not remove it from the deque.

**Input:**
- `deq: var Deque[T]`

**Output:** `var T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns a mutable reference to the last element of deq, but does not remove it from the deque.

**See also:**

* [peekFirst proc](#peekFirst,Deque[T]_2)
* [peekLast proc](#peekLast,Deque[T])

### popFirst

[ref: #symbol-popfirst]

Removes and returns the first element of the deq.

**Input:**
- `deq: var Deque[T]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`, `discardable`

Removes and returns the first element of the deq.

See also:

* [popLast proc](#popLast,Deque[T])
* [shrink proc](#shrink,Deque[T],int,int)

### popLast

[ref: #symbol-poplast]

Removes and returns the last element of the deq.

**Input:**
- `deq: var Deque[T]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`, `discardable`

Removes and returns the last element of the deq.

**See also:**

* [popFirst proc](#popFirst,Deque[T])
* [shrink proc](#shrink,Deque[T],int,int)

### shrink

[ref: #symbol-shrink]

Removes fromFirst elements from the front of the deque and fromLast elements from the back.

**Input:**
- `deq: var Deque[T]`
- `fromFirst:  = 0`
- `fromLast:  = 0`

**Output:** *(none)*
**Generic parameters:** `T`

Removes fromFirst elements from the front of the deque and fromLast elements from the back.

If the supplied number of elements exceeds the total number of elements in the deque, the deque will remain empty.

**See also:**

* [clear proc](#clear,Deque[T])
* [popFirst proc](#popFirst,Deque[T])
* [popLast proc](#popLast,Deque[T])

### toDeque

[ref: #symbol-todeque]

Creates a new deque that contains the elements of x (in the same order).

**Input:**
- `x: openArray[T]`

**Output:** `Deque[T]`
**Generic parameters:** `T`

Creates a new deque that contains the elements of x (in the same order).

**See also:**

* [initDeque proc](#initDeque,int)

## Type

### Deque

[ref: #symbol-deque]

A double-ended queue backed with a ringed seq buffer.

```nim
Deque[T] = object
```

A double-ended queue backed with a ringed seq buffer.

To initialize an empty deque, use the [initDeque proc](#initDeque,int).
