---
source_hash: b30ffc484dd6ad8c
source_path: lib/pure/collections/heapqueue.nim
---

# heapqueue

[ref: #module-heapqueue]

The heapqueue module implements a [binary heap data structure](https://en.wikipedia.org/wiki/Binary_heap) that can be used as a [priority queue](https://en.wikipedia.org/wiki/Priority_queue). They are represented as arrays for which a[k] <= a[2\*k+1] and a[k] <= a[2\*k+2] for all indices k (counting elements from 0). The interesting property of a heap is that a[0] is always its smallest element.

# [Basic usage](#basic-usage)

# [Usage with custom objects](#usage-with-custom-objects)

To use a HeapQueue with a custom object, the < operator must be implemented.

## Examples

```nim
import std/heapqueue
var heap = [8, 2].toHeapQueue
heap.push(5)
# the first element is the lowest element
assert heap[0] == 2
# remove and return the lowest element
assert heap.pop() == 2
# the lowest element remaining is 5
assert heap[0] == 5
```

```nim
import std/heapqueue
type Job = object
  priority: int

proc `<`(a, b: Job): bool = a.priority < b.priority

var jobs = initHeapQueue[Job]()
jobs.push(Job(priority: 1))
jobs.push(Job(priority: 2))

assert jobs[0].priority == 1
```

```nim
let heap = [1, 2].toHeapQueue
assert $heap == "[1, 2]"
```

```nim
var heap = [9, 5, 8].toHeapQueue
heap.clear()
assert heap.len == 0
```

```nim
var heap = [9, 5, 8].toHeapQueue
heap.del(1)
assert heap[0] == 5
assert heap[1] == 8
```

```nim
let heap = [9, 5, 8].toHeapQueue
assert heap.find(5) == 0
assert heap.find(9) == 1
assert heap.find(777) == -1
```

```nim
let heap = [9, 5, 8].toHeapQueue
assert heap.len == 3
```

```nim
var heap = [9, 5, 8].toHeapQueue
assert heap.pop() == 5
```

```nim
var heap = [5, 12].toHeapQueue
assert heap.pushpop(6) == 5
assert heap.len == 2
assert heap[0] == 6
assert heap.pushpop(4) == 4
```

```nim
var heap = [5, 12].toHeapQueue
assert heap.replace(6) == 5
assert heap.len == 2
assert heap[0] == 6
assert heap.replace(4) == 6
```

```nim
var heap = [9, 5, 8].toHeapQueue
assert heap.pop() == 5
assert heap[0] == 8
```

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `heap: HeapQueue[T]`

**Output:** `lent T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Iterates over each item of heap.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `heap: HeapQueue[T]`

**Output:** `string`
**Generic parameters:** `T`

Turns a heap into its string representation.

### `[]`

[ref: #symbol-]

**Input:**
- `heap: HeapQueue[T]`
- `i: Natural`

**Output:** `lent T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Accesses the i-th element of heap.

### clear

[ref: #symbol-clear]

**Input:**
- `heap: var HeapQueue[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Removes all elements from heap, making it empty.

### contains

[ref: #symbol-contains]

**Input:**
- `heap: HeapQueue[T]`
- `x: T`

**Output:** `bool`
**Generic parameters:** `T`

Returns true if x is in heap or false if not found. This is a shortcut for find(heap, x) >= 0.

### del

[ref: #symbol-del]

**Input:**
- `heap: var HeapQueue[T]`
- `index: Natural`

**Output:** *(none)*
**Generic parameters:** `T`

Removes the element at index from heap, maintaining the heap invariant.

### find

[ref: #symbol-find]

**Input:**
- `heap: HeapQueue[T]`
- `x: T`

**Output:** `int`
**Generic parameters:** `T`

Linear scan to find the index of the item x or -1 if not found.

### initHeapQueue

[ref: #symbol-initheapqueue]

Creates a new empty heap.

**Input:**
- *(none)*

**Output:** `HeapQueue[T]`
**Generic parameters:** `T`

Creates a new empty heap.

Heaps are initialized by default, so it is not necessary to call this function explicitly.

**See also:**

* [toHeapQueue proc](#toHeapQueue,openArray[T])

### len

[ref: #symbol-len]

**Input:**
- `heap: HeapQueue[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the number of elements of heap.

### pop

[ref: #symbol-pop]

**Input:**
- `heap: var HeapQueue[T]`

**Output:** `T`
**Generic parameters:** `T`

Pops and returns the smallest item from heap, maintaining the heap invariant.

### push

[ref: #symbol-push]

**Input:**
- `heap: var HeapQueue[T]`
- `item: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

Pushes item onto heap, maintaining the heap invariant.

### pushpop

[ref: #symbol-pushpop]

Fast version of a push() followed by a pop().

**Input:**
- `heap: var HeapQueue[T]`
- `item: sink T`

**Output:** `T`
**Generic parameters:** `T`

Fast version of a push() followed by a pop().

**See also:**

* [replace proc](#replace,HeapQueue[T],sinkT)

### replace

[ref: #symbol-replace]

Pops and returns the current smallest value, and add the new item. This is more efficient than pop() followed by push(), and can be more appropriate when using a fixed-size heap. Note that the value returned may be larger than item! That constrains reasonable uses of this routine unless written as part of a conditional replacement.

**Input:**
- `heap: var HeapQueue[T]`
- `item: sink T`

**Output:** `T`
**Generic parameters:** `T`

Pops and returns the current smallest value, and add the new item. This is more efficient than pop() followed by push(), and can be more appropriate when using a fixed-size heap. Note that the value returned may be larger than item! That constrains reasonable uses of this routine unless written as part of a conditional replacement.

**See also:**

* [pushpop proc](#pushpop,HeapQueue[T],sinkT)

### toHeapQueue

[ref: #symbol-toheapqueue]

Creates a new HeapQueue that contains the elements of x.

**Input:**
- `x: openArray[T]`

**Output:** `HeapQueue[T]`
**Generic parameters:** `T`

Creates a new HeapQueue that contains the elements of x.

**See also:**

* [initHeapQueue proc](#initHeapQueue)

## Type

### HeapQueue

[ref: #symbol-heapqueue]

```nim
HeapQueue[T] = object
```

A heap queue, commonly known as a priority queue.
