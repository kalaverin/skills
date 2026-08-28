---
source_hash: 9299840a0d5ad466
source_path: lib/pure/collections/lists.nim
---

### initSinglyLinkedList

[ref: #symbol-initsinglylinkedlist]

Creates a new singly linked list that is empty.

**Input:**
- *(none)*

**Output:** `SinglyLinkedList[T]`
**Generic parameters:** `T`

Creates a new singly linked list that is empty.

Singly linked lists are initialized by default, so it is not necessary to call this function explicitly.

### initSinglyLinkedRing

[ref: #symbol-initsinglylinkedring]

Creates a new singly linked ring that is empty.

**Input:**
- *(none)*

**Output:** `SinglyLinkedRing[T]`
**Generic parameters:** `T`

Creates a new singly linked ring that is empty.

Singly linked rings are initialized by default, so it is not necessary to call this function explicitly.

### newDoublyLinkedNode

[ref: #symbol-newdoublylinkednode]

**Input:**
- `value: T`

**Output:** `DoublyLinkedNode[T]`
**Generic parameters:** `T`

Creates a new doubly linked node with the given value.

### newSinglyLinkedNode

[ref: #symbol-newsinglylinkednode]

**Input:**
- `value: T`

**Output:** `SinglyLinkedNode[T]`
**Generic parameters:** `T`

Creates a new singly linked node with the given value.

### prepend

[ref: #symbol-prepend]

Prepends a shallow copy of b to the beginning of a.

**Input:**
- `a: var T`
- `b: T`

**Output:** *(none)*
**Generic parameters:** `T`

Prepends a shallow copy of b to the beginning of a.

**See also:**

* [prependMoved proc](#prependMoved,T,T) for moving the second list instead of copying

### prepend

[ref: #symbol-prepend]

Prepends (adds to the beginning) a node to L. Efficiency: O(1).

**Input:**
- `L: var SinglyLinkedList[T]`
- `n: SinglyLinkedNode[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Prepends (adds to the beginning) a node to L. Efficiency: O(1).

**See also:**

* [add proc](#add,SinglyLinkedList[T],SinglyLinkedNode[T]) for appending a node
* [add proc](#add,SinglyLinkedList[T],T) for appending a value
* [prepend proc](#prepend,SinglyLinkedList[T],T) for prepending a value

### prepend

[ref: #symbol-prepend]

Prepends (adds to the beginning) a node to L. Efficiency: O(1).

**Input:**
- `L: var SinglyLinkedList[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Prepends (adds to the beginning) a node to L. Efficiency: O(1).

**See also:**

* [add proc](#add,SinglyLinkedList[T],SinglyLinkedNode[T]) for appending a node
* [add proc](#add,SinglyLinkedList[T],T) for appending a value
* [prepend proc](#prepend,SinglyLinkedList[T],SinglyLinkedNode[T]) for prepending a node

### prepend

[ref: #symbol-prepend]

Prepends (adds to the beginning) a node n to L. Efficiency: O(1).

**Input:**
- `L: var DoublyLinkedList[T]`
- `n: DoublyLinkedNode[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Prepends (adds to the beginning) a node n to L. Efficiency: O(1).

**See also:**

* [add proc](#add,DoublyLinkedList[T],DoublyLinkedNode[T]) for appending a node
* [add proc](#add,DoublyLinkedList[T],T) for appending a value
* [prepend proc](#prepend,DoublyLinkedList[T],T) for prepending a value
* [remove proc](#remove,DoublyLinkedList[T],DoublyLinkedNode[T]) for removing a node

### prepend

[ref: #symbol-prepend]

Prepends (adds to the beginning) a value to L. Efficiency: O(1).

**Input:**
- `L: var DoublyLinkedList[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

Prepends (adds to the beginning) a value to L. Efficiency: O(1).

**See also:**

* [add proc](#add,DoublyLinkedList[T],DoublyLinkedNode[T]) for appending a node
* [add proc](#add,DoublyLinkedList[T],T) for appending a value
* [prepend proc](#prepend,DoublyLinkedList[T],DoublyLinkedNode[T]) for prepending a node
* [remove proc](#remove,DoublyLinkedList[T],DoublyLinkedNode[T]) for removing a node

### prepend

[ref: #symbol-prepend]

Prepends (adds to the beginning) a node n to L. Efficiency: O(1).

**Input:**
- `L: var SinglyLinkedRing[T]`
- `n: SinglyLinkedNode[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Prepends (adds to the beginning) a node n to L. Efficiency: O(1).

**See also:**

* [add proc](#add,SinglyLinkedRing[T],SinglyLinkedNode[T]) for appending a node
* [add proc](#add,SinglyLinkedRing[T],T) for appending a value
* [prepend proc](#prepend,SinglyLinkedRing[T],T) for prepending a value

### prepend

[ref: #symbol-prepend]

Prepends (adds to the beginning) a value to L. Efficiency: O(1).

**Input:**
- `L: var SinglyLinkedRing[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

Prepends (adds to the beginning) a value to L. Efficiency: O(1).

**See also:**

* [add proc](#add,SinglyLinkedRing[T],SinglyLinkedNode[T]) for appending a node
* [add proc](#add,SinglyLinkedRing[T],T) for appending a value
* [prepend proc](#prepend,SinglyLinkedRing[T],SinglyLinkedNode[T]) for prepending a node

### prepend

[ref: #symbol-prepend]

Prepends (adds to the beginning) a node n to L. Efficiency: O(1).

**Input:**
- `L: var DoublyLinkedRing[T]`
- `n: DoublyLinkedNode[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Prepends (adds to the beginning) a node n to L. Efficiency: O(1).

**See also:**

* [add proc](#add,DoublyLinkedRing[T],DoublyLinkedNode[T]) for appending a node
* [add proc](#add,DoublyLinkedRing[T],T) for appending a value
* [prepend proc](#prepend,DoublyLinkedRing[T],T) for prepending a value
* [remove proc](#remove,DoublyLinkedRing[T],DoublyLinkedNode[T]) for removing a node

### prepend

[ref: #symbol-prepend]

Prepends (adds to the beginning) a value to L. Efficiency: O(1).

**Input:**
- `L: var DoublyLinkedRing[T]`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

Prepends (adds to the beginning) a value to L. Efficiency: O(1).

**See also:**

* [add proc](#add,DoublyLinkedRing[T],DoublyLinkedNode[T]) for appending a node
* [add proc](#add,DoublyLinkedRing[T],T) for appending a value
* [prepend proc](#prepend,DoublyLinkedRing[T],DoublyLinkedNode[T]) for prepending a node
* [remove proc](#remove,DoublyLinkedRing[T],DoublyLinkedNode[T]) for removing a node

### prependMoved

[ref: #symbol-prependmoved]

Moves b before the head of a. Efficiency: O(1). Note that b becomes empty after the operation unless it has the same address as a. Self-prepending results in a cycle.

**Input:**
- `a: var T`
- `b: var T`

**Output:** *(none)*
**Generic parameters:** `T`

Moves b before the head of a. Efficiency: O(1). Note that b becomes empty after the operation unless it has the same address as a. Self-prepending results in a cycle.

**See also:**

* [prepend proc](#prepend,T,T) for prepending a copy of a list

### remove

[ref: #symbol-remove]

**Input:**
- `L: var SinglyLinkedList[T]`
- `n: SinglyLinkedNode[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `discardable`

Removes a node n from L. Returns true if n was found in L. Efficiency: O(n); the list is traversed until n is found. Attempting to remove an element not contained in the list is a no-op. When the list is cyclic, the cycle is preserved after removal.

### remove

[ref: #symbol-remove]

**Input:**
- `L: var DoublyLinkedList[T]`
- `n: DoublyLinkedNode[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Removes a node n from L. Efficiency: O(1). This function assumes, for the sake of efficiency, that n is contained in L, otherwise the effects are undefined. When the list is cyclic, the cycle is preserved after removal.

### remove

[ref: #symbol-remove]

**Input:**
- `L: var DoublyLinkedRing[T]`
- `n: DoublyLinkedNode[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Removes n from L. Efficiency: O(1). This function assumes, for the sake of efficiency, that n is contained in L, otherwise the effects are undefined.

### toDoublyLinkedList

[ref: #symbol-todoublylinkedlist]

**Input:**
- `elems: openArray[T]`

**Output:** `DoublyLinkedList[T]`
**Generic parameters:** `T`

Creates a new DoublyLinkedList from the members of elems.

### toDoublyLinkedRing

[ref: #symbol-todoublylinkedring]

**Input:**
- `elems: openArray[T]`

**Output:** `DoublyLinkedRing[T]`
**Generic parameters:** `T`

Creates a new DoublyLinkedRing from the members of elems.

### toSinglyLinkedList

[ref: #symbol-tosinglylinkedlist]

**Input:**
- `elems: openArray[T]`

**Output:** `SinglyLinkedList[T]`
**Generic parameters:** `T`

Creates a new SinglyLinkedList from the members of elems.

### toSinglyLinkedRing

[ref: #symbol-tosinglylinkedring]

**Input:**
- `elems: openArray[T]`

**Output:** `SinglyLinkedRing[T]`
**Generic parameters:** `T`

Creates a new SinglyLinkedRing from the members of elems.

## Type

### DoublyLinkedList

[ref: #symbol-doublylinkedlist]

```nim
DoublyLinkedList[T] = object
  head*: DoublyLinkedNode[T]
  tail* {.cursor.}: DoublyLinkedNode[T]
```

A doubly linked list.

### DoublyLinkedNode

[ref: #symbol-doublylinkednode]

```nim
DoublyLinkedNode[T] = ref DoublyLinkedNodeObj[T]
```

### DoublyLinkedNodeObj

[ref: #symbol-doublylinkednodeobj]

A node of a doubly linked list.

```nim
DoublyLinkedNodeObj[T] = object
  next*: DoublyLinkedNode[T]
  prev* {.cursor.}: DoublyLinkedNode[T]
  value*: T
```

A node of a doubly linked list.

It consists of a value field, and pointers to next and prev.

### DoublyLinkedRing

[ref: #symbol-doublylinkedring]

```nim
DoublyLinkedRing[T] = object
  head*: DoublyLinkedNode[T]
```

A doubly linked ring.

### SinglyLinkedList

[ref: #symbol-singlylinkedlist]

```nim
SinglyLinkedList[T] = object
  head*: SinglyLinkedNode[T]
  tail* {.cursor.}: SinglyLinkedNode[T]
```

A singly linked list.

### SinglyLinkedNode

[ref: #symbol-singlylinkednode]

```nim
SinglyLinkedNode[T] = ref SinglyLinkedNodeObj[T]
```

### SinglyLinkedNodeObj

[ref: #symbol-singlylinkednodeobj]

A node of a singly linked list.

```nim
SinglyLinkedNodeObj[T] = object
  next*: SinglyLinkedNode[T]
  value*: T
```

A node of a singly linked list.

It consists of a value field, and a pointer to next.

### SinglyLinkedRing

[ref: #symbol-singlylinkedring]

```nim
SinglyLinkedRing[T] = object
  head*: SinglyLinkedNode[T]
  tail* {.cursor.}: SinglyLinkedNode[T]
```

A singly linked ring.

### SomeLinkedCollection

[ref: #symbol-somelinkedcollection]

```nim
SomeLinkedCollection[T] = SomeLinkedList[T] | SomeLinkedRing[T]
```

### SomeLinkedList

[ref: #symbol-somelinkedlist]

```nim
SomeLinkedList[T] = SinglyLinkedList[T] | DoublyLinkedList[T]
```

### SomeLinkedNode

[ref: #symbol-somelinkednode]

```nim
SomeLinkedNode[T] = SinglyLinkedNode[T] | DoublyLinkedNode[T]
```

### SomeLinkedRing

[ref: #symbol-somelinkedring]

```nim
SomeLinkedRing[T] = SinglyLinkedRing[T] | DoublyLinkedRing[T]
```

[Prev](lists_1.md)
