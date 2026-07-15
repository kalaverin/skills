---
source_hash: 9299840a0d5ad466
source_path: lib/pure/collections/lists.nim
---

# lists

[ref: #module-lists]

Implementation of:

* [singly linked lists](#SinglyLinkedList)
* [doubly linked lists](#DoublyLinkedList)
* [singly linked rings](#SinglyLinkedRing) (circular lists)
* [doubly linked rings](#DoublyLinkedRing) (circular lists)

# [Basic Usage](#basic-usage)

Because it makes no sense to do otherwise, the next and prev pointers are not hidden from you and can be manipulated directly for efficiency.

## [Lists](#basic-usage-lists)

## [Rings](#basic-usage-rings)

# [See also](#see-also)

* [deques module](deques.html) for double-ended queues

## Examples

```nim
import std/lists
var list = initDoublyLinkedList[int]()
let
  a = newDoublyLinkedNode[int](3)
  b = newDoublyLinkedNode[int](7)
  c = newDoublyLinkedNode[int](9)

list.add(a)
list.add(b)
list.prepend(c)

assert a.next == b
assert a.prev == c
assert c.next == a
assert c.next.next == b
assert c.prev == nil
assert b.next == nil
```

```nim
import std/lists
var ring = initSinglyLinkedRing[int]()
let
  a = newSinglyLinkedNode[int](3)
  b = newSinglyLinkedNode[int](7)
  c = newSinglyLinkedNode[int](9)

ring.add(a)
ring.add(b)
ring.prepend(c)

assert c.next == a
assert a.next == b
assert c.next.next == b
assert b.next == c
assert c.next.next.next == c
```

```nim
let a = [1, 2, 3, 4].toSinglyLinkedList
assert $a == "[1, 2, 3, 4]"
```

```nim
from std/sequtils import toSeq
var a = [1, 2, 3].toSinglyLinkedList
let b = [4, 5].toSinglyLinkedList
a.add(b)
assert a.toSeq == [1, 2, 3, 4, 5]
assert b.toSeq == [4, 5]
a.add(a)
assert a.toSeq == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
```

```nim
var a = initDoublyLinkedList[int]()
let n = newDoublyLinkedNode[int](9)
a.add(n)
assert a.contains(9)
```

```nim
var a = initDoublyLinkedList[int]()
a.add(9)
a.add(8)
assert a.contains(9)
```

```nim
var a = initDoublyLinkedRing[int]()
let n = newDoublyLinkedNode[int](9)
a.add(n)
assert a.contains(9)
```

```nim
var a = initDoublyLinkedRing[int]()
a.add(9)
a.add(8)
assert a.contains(9)
```

```nim
var a = initSinglyLinkedList[int]()
let n = newSinglyLinkedNode[int](9)
a.add(n)
assert a.contains(9)
```

```nim
var a = initSinglyLinkedList[int]()
a.add(9)
a.add(8)
assert a.contains(9)
```

```nim
var a = initSinglyLinkedRing[int]()
let n = newSinglyLinkedNode[int](9)
a.add(n)
assert a.contains(9)
```

```nim
var a = initSinglyLinkedRing[int]()
a.add(9)
a.add(8)
assert a.contains(9)
```

```nim
import std/[sequtils, enumerate, sugar]
var
  a = [1, 2, 3].toDoublyLinkedList
  b = [4, 5].toDoublyLinkedList
  c = [0, 1].toDoublyLinkedList
a.addMoved(b)
assert a.toSeq == [1, 2, 3, 4, 5]
assert b.toSeq == []
c.addMoved(c)
let s = collect:
  for i, ci in enumerate(c):
    if i == 6: break
    ci
assert s == [0, 1, 0, 1, 0, 1]
```

```nim
import std/[sequtils, enumerate, sugar]
var
  a = [1, 2, 3].toSinglyLinkedList
  b = [4, 5].toSinglyLinkedList
  c = [0, 1].toSinglyLinkedList
a.addMoved(b)
assert a.toSeq == [1, 2, 3, 4, 5]
assert b.toSeq == []
c.addMoved(c)
let s = collect:
  for i, ci in enumerate(c):
    if i == 6: break
    ci
assert s == [0, 1, 0, 1, 0, 1]
```

```nim
let a = [9, 8].toSinglyLinkedList
assert a.contains(9)
assert 8 in a
assert(not a.contains(1))
assert 2 notin a
```

```nim
from std/sequtils import toSeq
type Foo = ref object
  x: int
var
  f = Foo(x: 1)
  a = [f].toDoublyLinkedList
let b = a.copy
a.add([f].toDoublyLinkedList)
assert a.toSeq == [f, f]
assert b.toSeq == [f] # b isn't modified...
f.x = 42
assert a.head.value.x == 42
assert b.head.value.x == 42 # ... but the elements are not deep copied

let c = [1, 2, 3].toDoublyLinkedList
assert $c == $c.copy
```

```nim
from std/sequtils import toSeq
type Foo = ref object
  x: int
var
  f = Foo(x: 1)
  a = [f].toSinglyLinkedList
let b = a.copy
a.add([f].toSinglyLinkedList)
assert a.toSeq == [f, f]
assert b.toSeq == [f] # b isn't modified...
f.x = 42
assert a.head.value.x == 42
assert b.head.value.x == 42 # ... but the elements are not deep copied

let c = [1, 2, 3].toSinglyLinkedList
assert $c == $c.copy
```

```nim
let a = [9, 8].toSinglyLinkedList
assert a.find(9).value == 9
assert a.find(1) == nil
```

```nim
let a = initDoublyLinkedList[int]()
```

```nim
let a = initDoublyLinkedRing[int]()
```

```nim
let a = initSinglyLinkedList[int]()
```

```nim
let a = initSinglyLinkedRing[int]()
```

```nim
let n = newDoublyLinkedNode[int](5)
assert n.value == 5
```

```nim
let n = newSinglyLinkedNode[int](5)
assert n.value == 5
```

```nim
from std/sequtils import toSeq
var a = [4, 5].toSinglyLinkedList
let b = [1, 2, 3].toSinglyLinkedList
a.prepend(b)
assert a.toSeq == [1, 2, 3, 4, 5]
assert b.toSeq == [1, 2, 3]
a.prepend(a)
assert a.toSeq == [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
```

```nim
var a = initDoublyLinkedList[int]()
let n = newDoublyLinkedNode[int](9)
a.prepend(n)
assert a.contains(9)
```

```nim
var a = initDoublyLinkedList[int]()
a.prepend(9)
a.prepend(8)
assert a.contains(9)
```

```nim
var a = initDoublyLinkedRing[int]()
let n = newDoublyLinkedNode[int](9)
a.prepend(n)
assert a.contains(9)
```

```nim
var a = initDoublyLinkedRing[int]()
a.prepend(9)
a.prepend(8)
assert a.contains(9)
```

```nim
var a = initSinglyLinkedList[int]()
let n = newSinglyLinkedNode[int](9)
a.prepend(n)
assert a.contains(9)
```

```nim
var a = initSinglyLinkedList[int]()
a.prepend(9)
a.prepend(8)
assert a.contains(9)
```

```nim
var a = initSinglyLinkedRing[int]()
let n = newSinglyLinkedNode[int](9)
a.prepend(n)
assert a.contains(9)
```

```nim
var a = initSinglyLinkedRing[int]()
a.prepend(9)
a.prepend(8)
assert a.contains(9)
```

```nim
import std/[sequtils, enumerate, sugar]
var
  a = [4, 5].toSinglyLinkedList
  b = [1, 2, 3].toSinglyLinkedList
  c = [0, 1].toSinglyLinkedList
a.prependMoved(b)
assert a.toSeq == [1, 2, 3, 4, 5]
assert b.toSeq == []
c.prependMoved(c)
let s = collect:
  for i, ci in enumerate(c):
    if i == 6: break
    ci
assert s == [0, 1, 0, 1, 0, 1]
```

```nim
import std/[sequtils, enumerate, sugar]
var a = [0, 1, 2].toSinglyLinkedList
let n = a.head.next
assert n.value == 1
a.remove(n)
assert a.toSeq == [0, 2]
a.remove(n)
assert a.toSeq == [0, 2]
a.addMoved(a) # cycle: [0, 2, 0, 2, ...]
a.remove(a.head)
let s = collect:
  for i, ai in enumerate(a):
    if i == 4: break
    ai
assert s == [2, 2, 2, 2]
```

```nim
var a = initDoublyLinkedRing[int]()
let n = newDoublyLinkedNode[int](5)
a.add(n)
assert 5 in a
a.remove(n)
assert 5 notin a
```

```nim
import std/[sequtils, enumerate, sugar]
var a = [0, 1, 2].toSinglyLinkedList
let n = a.head.next
assert n.value == 1
assert a.remove(n) == true
assert a.toSeq == [0, 2]
assert a.remove(n) == false
assert a.toSeq == [0, 2]
a.addMoved(a) # cycle: [0, 2, 0, 2, ...]
a.remove(a.head)
let s = collect:
  for i, ai in enumerate(a):
    if i == 4: break
    ai
assert s == [2, 2, 2, 2]
```

```nim
from std/sequtils import toSeq
let a = [1, 2, 3, 4, 5].toDoublyLinkedList
assert a.toSeq == [1, 2, 3, 4, 5]
```

```nim
from std/sequtils import toSeq
let a = [1, 2, 3, 4, 5].toDoublyLinkedRing
assert a.toSeq == [1, 2, 3, 4, 5]
```

```nim
from std/sequtils import toSeq
let a = [1, 2, 3, 4, 5].toSinglyLinkedList
assert a.toSeq == [1, 2, 3, 4, 5]
```

```nim
from std/sequtils import toSeq
let a = [1, 2, 3, 4, 5].toSinglyLinkedRing
assert a.toSeq == [1, 2, 3, 4, 5]
```

```nim
from std/sugar import collect
from std/sequtils import toSeq
let a = collect(initSinglyLinkedList):
  for i in 1..3: 10 * i
assert toSeq(items(a)) == toSeq(a)
assert toSeq(a) == @[10, 20, 30]
```

```nim
from std/sugar import collect
from std/sequtils import toSeq
let a = collect(initSinglyLinkedRing):
  for i in 1..3: 10 * i
assert toSeq(items(a)) == toSeq(a)
assert toSeq(a) == @[10, 20, 30]
```

```nim
var a = initSinglyLinkedList[int]()
for i in 1..5:
  a.add(10 * i)
assert $a == "[10, 20, 30, 40, 50]"
for x in mitems(a):
  x = 5 * x - 1
assert $a == "[49, 99, 149, 199, 249]"
```

```nim
var a = initSinglyLinkedRing[int]()
for i in 1..5:
  a.add(10 * i)
assert $a == "[10, 20, 30, 40, 50]"
for x in mitems(a):
  x = 5 * x - 1
assert $a == "[49, 99, 149, 199, 249]"
```

```nim
var a = initDoublyLinkedList[int]()
for i in 1..5:
  a.add(10 * i)
assert $a == "[10, 20, 30, 40, 50]"
for x in nodes(a):
  if x.value == 30:
    a.remove(x)
  else:
    x.value = 5 * x.value - 1
assert $a == "[49, 99, 199, 249]"
```

```nim
var a = initDoublyLinkedRing[int]()
for i in 1..5:
  a.add(10 * i)
assert $a == "[10, 20, 30, 40, 50]"
for x in nodes(a):
  if x.value == 30:
    a.remove(x)
  else:
    x.value = 5 * x.value - 1
assert $a == "[49, 99, 199, 249]"
```

## Iterator

### items

[ref: #symbol-items]

Yields every value of L.

**Input:**
- `L: SomeLinkedList[T]`

**Output:** `T`
**Generic parameters:** `T`

Yields every value of L.

**See also:**

* [mitems iterator](#mitems.i,SomeLinkedList[T])
* [nodes iterator](#nodes.i,SomeLinkedList[T])

### items

[ref: #symbol-items]

Yields every value of L.

**Input:**
- `L: SomeLinkedRing[T]`

**Output:** `T`
**Generic parameters:** `T`

Yields every value of L.

**See also:**

* [mitems iterator](#mitems.i,SomeLinkedRing[T])
* [nodes iterator](#nodes.i,SomeLinkedRing[T])

### mitems

[ref: #symbol-mitems]

Yields every value of L so that you can modify it.

**Input:**
- `L: var SomeLinkedList[T]`

**Output:** `var T`
**Generic parameters:** `T`

Yields every value of L so that you can modify it.

**See also:**

* [items iterator](#items.i,SomeLinkedList[T])
* [nodes iterator](#nodes.i,SomeLinkedList[T])

### mitems

[ref: #symbol-mitems]

Yields every value of L so that you can modify it.

**Input:**
- `L: var SomeLinkedRing[T]`

**Output:** `var T`
**Generic parameters:** `T`

Yields every value of L so that you can modify it.

**See also:**

* [items iterator](#items.i,SomeLinkedRing[T])
* [nodes iterator](#nodes.i,SomeLinkedRing[T])

### nodes

[ref: #symbol-nodes]

Iterates over every node of x. Removing the current node from the list during traversal is supported.

**Input:**
- `L: SomeLinkedList[T]`

**Output:** `SomeLinkedNode[T]`
**Generic parameters:** `T`

Iterates over every node of x. Removing the current node from the list during traversal is supported.

**See also:**

* [items iterator](#items.i,SomeLinkedList[T])
* [mitems iterator](#mitems.i,SomeLinkedList[T])

### nodes

[ref: #symbol-nodes]

Iterates over every node of x. Removing the current node from the list during traversal is supported.

**Input:**
- `L: SomeLinkedRing[T]`

**Output:** `SomeLinkedNode[T]`
**Generic parameters:** `T`

Iterates over every node of x. Removing the current node from the list during traversal is supported.

**See also:**

* [items iterator](#items.i,SomeLinkedRing[T])
* [mitems iterator](#mitems.i,SomeLinkedRing[T])

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `L: SomeLinkedCollection[T]`

**Output:** `string`
**Generic parameters:** `T`

Turns a list into its string representation for logging and printing.

### add

[ref: #symbol-add]

Appends (adds to the end) a node n to L. Efficiency: O(1).

**Input:**
- `L: var SinglyLinkedList[T]`
- `n: SinglyLinkedNode[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Appends (adds to the end) a node n to L. Efficiency: O(1).

**See also:**

* [add proc](#add,SinglyLinkedList[T],T) for appending a value
* [prepend proc](#prepend,SinglyLinkedList[T],SinglyLinkedNode[T]) for prepending a node
* [prepend proc](#prepend,SinglyLinkedList[T],T) for prepending a value

### add

[ref: #symbol-add]

Appends (adds to the end) a value to L. Efficiency: O(1).

**Input:**
- `L: var SinglyLinkedList[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Appends (adds to the end) a value to L. Efficiency: O(1).

**See also:**

* [add proc](#add,SinglyLinkedList[T],T) for appending a value
* [prepend proc](#prepend,SinglyLinkedList[T],SinglyLinkedNode[T]) for prepending a node
* [prepend proc](#prepend,SinglyLinkedList[T],T) for prepending a value

### add

[ref: #symbol-add]

Appends (adds to the end) a node n to L. Efficiency: O(1).

**Input:**
- `L: var DoublyLinkedList[T]`
- `n: DoublyLinkedNode[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Appends (adds to the end) a node n to L. Efficiency: O(1).

**See also:**

* [add proc](#add,DoublyLinkedList[T],T) for appending a value
* [prepend proc](#prepend,DoublyLinkedList[T],DoublyLinkedNode[T]) for prepending a node
* [prepend proc](#prepend,DoublyLinkedList[T],T) for prepending a value
* [remove proc](#remove,DoublyLinkedList[T],DoublyLinkedNode[T]) for removing a node

### add

[ref: #symbol-add]

Appends (adds to the end) a value to L. Efficiency: O(1).

**Input:**
- `L: var DoublyLinkedList[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

Appends (adds to the end) a value to L. Efficiency: O(1).

**See also:**

* [add proc](#add,DoublyLinkedList[T],DoublyLinkedNode[T]) for appending a node
* [prepend proc](#prepend,DoublyLinkedList[T],DoublyLinkedNode[T]) for prepending a node
* [prepend proc](#prepend,DoublyLinkedList[T],T) for prepending a value
* [remove proc](#remove,DoublyLinkedList[T],DoublyLinkedNode[T]) for removing a node

### add

[ref: #symbol-add]

Appends a shallow copy of b to the end of a.

**Input:**
- `a: var T`
- `b: T`

**Output:** *(none)*
**Generic parameters:** `T`

Appends a shallow copy of b to the end of a.

**See also:**

* [addMoved proc](#addMoved,SinglyLinkedList[T],SinglyLinkedList[T])
* [addMoved proc](#addMoved,DoublyLinkedList[T],DoublyLinkedList[T]) for moving the second list instead of copying

### add

[ref: #symbol-add]

Appends (adds to the end) a node n to L. Efficiency: O(1).

**Input:**
- `L: var SinglyLinkedRing[T]`
- `n: SinglyLinkedNode[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Appends (adds to the end) a node n to L. Efficiency: O(1).

**See also:**

* [add proc](#add,SinglyLinkedRing[T],T) for appending a value
* [prepend proc](#prepend,SinglyLinkedRing[T],SinglyLinkedNode[T]) for prepending a node
* [prepend proc](#prepend,SinglyLinkedRing[T],T) for prepending a value

### add

[ref: #symbol-add]

Appends (adds to the end) a value to L. Efficiency: O(1).

**Input:**
- `L: var SinglyLinkedRing[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

Appends (adds to the end) a value to L. Efficiency: O(1).

**See also:**

* [add proc](#add,SinglyLinkedRing[T],SinglyLinkedNode[T]) for appending a node
* [prepend proc](#prepend,SinglyLinkedRing[T],SinglyLinkedNode[T]) for prepending a node
* [prepend proc](#prepend,SinglyLinkedRing[T],T) for prepending a value

### add

[ref: #symbol-add]

Appends (adds to the end) a node n to L. Efficiency: O(1).

**Input:**
- `L: var DoublyLinkedRing[T]`
- `n: DoublyLinkedNode[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Appends (adds to the end) a node n to L. Efficiency: O(1).

**See also:**

* [add proc](#add,DoublyLinkedRing[T],T) for appending a value
* [prepend proc](#prepend,DoublyLinkedRing[T],DoublyLinkedNode[T]) for prepending a node
* [prepend proc](#prepend,DoublyLinkedRing[T],T) for prepending a value
* [remove proc](#remove,DoublyLinkedRing[T],DoublyLinkedNode[T]) for removing a node

### add

[ref: #symbol-add]

Appends (adds to the end) a value to L. Efficiency: O(1).

**Input:**
- `L: var DoublyLinkedRing[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

Appends (adds to the end) a value to L. Efficiency: O(1).

**See also:**

* [add proc](#add,DoublyLinkedRing[T],DoublyLinkedNode[T]) for appending a node
* [prepend proc](#prepend,DoublyLinkedRing[T],DoublyLinkedNode[T]) for prepending a node
* [prepend proc](#prepend,DoublyLinkedRing[T],T) for prepending a value
* [remove proc](#remove,DoublyLinkedRing[T],DoublyLinkedNode[T]) for removing a node

### addMoved

[ref: #symbol-addmoved]

Moves b to the end of a. Efficiency: O(1). Note that b becomes empty after the operation unless it has the same address as a. Self-adding results in a cycle.

**Input:**
- `a: var SinglyLinkedList[T]`
- `b: var SinglyLinkedList[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Moves b to the end of a. Efficiency: O(1). Note that b becomes empty after the operation unless it has the same address as a. Self-adding results in a cycle.

**See also:**

* [add proc](#add,T,T) for adding a copy of a list

### addMoved

[ref: #symbol-addmoved]

Moves b to the end of a. Efficiency: O(1). Note that b becomes empty after the operation unless it has the same address as a. Self-adding results in a cycle.

**Input:**
- `a: var DoublyLinkedList[T]`
- `b: var DoublyLinkedList[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Moves b to the end of a. Efficiency: O(1). Note that b becomes empty after the operation unless it has the same address as a. Self-adding results in a cycle.

**See also:**

* [add proc](#add,T,T) for adding a copy of a list

### append

[ref: #symbol-append]

Alias for a.add(b).

**Input:**
- `a: var (SinglyLinkedList[T] | SinglyLinkedRing[T])`
- `b: SinglyLinkedList[T] | SinglyLinkedNode[T] | T`

**Output:** *(none)*
**Generic parameters:** `T`, `a:type`, `b:type`

Alias for a.add(b).

**See also:**

* [add proc](#add,SinglyLinkedList[T],SinglyLinkedNode[T])
* [add proc](#add,SinglyLinkedList[T],T)
* [add proc](#add,T,T)

### append

[ref: #symbol-append]

Alias for a.add(b).

**Input:**
- `a: var (DoublyLinkedList[T] | DoublyLinkedRing[T])`
- `b: DoublyLinkedList[T] | DoublyLinkedNode[T] | T`

**Output:** *(none)*
**Generic parameters:** `T`, `a:type`, `b:type`

Alias for a.add(b).

**See also:**

* [add proc](#add,DoublyLinkedList[T],DoublyLinkedNode[T])
* [add proc](#add,DoublyLinkedList[T],T)
* [add proc](#add,T,T)

### appendMoved

[ref: #symbol-appendmoved]

Alias for a.addMoved(b).

**Input:**
- `a: var T`
- `b: var T`

**Output:** *(none)*
**Generic parameters:** `T`

Alias for a.addMoved(b).

**See also:**

* [addMoved proc](#addMoved,SinglyLinkedList[T],SinglyLinkedList[T])
* [addMoved proc](#addMoved,DoublyLinkedList[T],DoublyLinkedList[T])

### contains

[ref: #symbol-contains]

Searches in the list for a value. Returns false if the value does not exist, true otherwise. This allows the usage of the in and notin operators.

**Input:**
- `L: SomeLinkedCollection[T]`
- `value: T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`

Searches in the list for a value. Returns false if the value does not exist, true otherwise. This allows the usage of the in and notin operators.

**See also:**

* [find proc](#find,SomeLinkedCollection[T],T)

### copy

[ref: #symbol-copy]

**Input:**
- `a: SinglyLinkedList[T]`

**Output:** `SinglyLinkedList[T]`
**Generic parameters:** `T`

Creates a shallow copy of a.

### copy

[ref: #symbol-copy]

**Input:**
- `a: DoublyLinkedList[T]`

**Output:** `DoublyLinkedList[T]`
**Generic parameters:** `T`

Creates a shallow copy of a.

### find

[ref: #symbol-find]

Searches in the list for a value. Returns nil if the value does not exist.

**Input:**
- `L: SomeLinkedCollection[T]`
- `value: T`

**Output:** `SomeLinkedNode[T]`
**Generic parameters:** `T`

Searches in the list for a value. Returns nil if the value does not exist.

**See also:**

* [contains proc](#contains,SomeLinkedCollection[T],T)

### initDoublyLinkedList

[ref: #symbol-initdoublylinkedlist]

Creates a new doubly linked list that is empty.

**Input:**
- *(none)*

**Output:** `DoublyLinkedList[T]`
**Generic parameters:** `T`

Creates a new doubly linked list that is empty.

Doubly linked lists are initialized by default, so it is not necessary to call this function explicitly.

### initDoublyLinkedRing

[ref: #symbol-initdoublylinkedring]

Creates a new doubly linked ring that is empty.

**Input:**
- *(none)*

**Output:** `DoublyLinkedRing[T]`
**Generic parameters:** `T`

Creates a new doubly linked ring that is empty.

Doubly linked rings are initialized by default, so it is not necessary to call this function explicitly.


[Next](lists_2.md)
