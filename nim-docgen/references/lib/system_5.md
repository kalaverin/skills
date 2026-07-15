---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

### `==`

[ref: #symbol-]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `bool`
**Pragmas:** `magic: "EqI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `bool`
**Pragmas:** `magic: "EqF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: float`
- `y: float`

**Output:** `bool`
**Pragmas:** `magic: "EqF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: array[I, T]`
- `y: array[I, T]`

**Output:** `bool`
**Generic parameters:** `I`, `T`

### `==`

[ref: #symbol-]

**Input:**
- `x: openArray[T]`
- `y: openArray[T]`

**Output:** `bool`
**Generic parameters:** `T`

### `==`

[ref: #symbol-]

**Input:**
- `x: seq[T]`
- `y: seq[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Generic equals operator for sequences: relies on a equals operator for the element type T.

### `==`

[ref: #symbol-]

**Input:**
- `x: T`
- `y: T`

**Output:** `bool`
**Generic parameters:** `T`

Generic == operator for tuples that is lifted from the components. of x and y.

### `==`

[ref: #symbol-]

**Input:**
- `x: cstring`
- `y: cstring`

**Output:** `bool`
**Pragmas:** `magic: "EqCString"`, `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks for equality between two cstring variables.

### `=`

[ref: #symbol-]

**Input:**
- `dest: var T`
- `src: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `magic: "Asgn"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `=copy`

[ref: #symbol-copy]

**Input:**
- `dest: var T`
- `src: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `magic: "Asgn"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `=destroy`

[ref: #symbol-destroy]

**Input:**
- `x: var T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `magic: "Destroy"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic destructor implementation that can be overridden.

### `=destroy`

[ref: #symbol-destroy]

**Input:**
- `x: string`

**Output:** *(none)*
**Pragmas:** `inline`, `magic: "Destroy"`, `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `=destroy`

[ref: #symbol-destroy]

**Input:**
- `x: seq[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `magic: "Destroy"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `=destroy`

[ref: #symbol-destroy]

**Input:**
- `x: ref T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `magic: "Destroy"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `=dup`

[ref: #symbol-dup]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`, `magic: "Dup"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic dup implementation that can be overridden.

### `=sink`

[ref: #symbol-sink]

**Input:**
- `x: var T`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `nodestroy`, `magic: "Asgn"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic sink implementation that can be overridden.

### `=trace`

[ref: #symbol-trace]

**Input:**
- `x: var T`
- `env: pointer`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `magic: "Trace"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic trace implementation that can be overridden.

### `=wasMoved`

[ref: #symbol-wasmoved]

**Input:**
- `obj: var T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "WasMoved"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic wasMoved implementation that can be overridden.

### `@`

[ref: #symbol-]

Turns an array into a sequence.

**Input:**
- `a: sink array[IDX, T]`

**Output:** `seq[T]`
**Generic parameters:** `IDX`, `T`

**Pragmas:** `magic: "ArrToSeq"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Turns an array into a sequence.

This most often useful for constructing sequences with the array constructor: @[1, 2, 3] has the type seq[int], while [1, 2, 3] has the type array[0..2, int].

```
let
  a = [1, 3, 5]
  b = "foo"

echo @a # => @[1, 3, 5]
echo @b # => @['f', 'o', 'o']
```

### `@`

[ref: #symbol-]

Turns an *openArray* into a sequence.

**Input:**
- `a: openArray[T]`

**Output:** `seq[T]`
**Generic parameters:** `T`

**Pragmas:** `magic: "OpenArrayToSeq"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Turns an *openArray* into a sequence.

This is not as efficient as turning a fixed length array into a sequence as it always copies every element of a.

### `[]=`

[ref: #symbol-]

**Input:**
- `a: T`
- `i: I`
- `x: sink S`

**Output:** *(none)*
**Generic parameters:** `I`, `T`, `S`

**Pragmas:** `noSideEffect`, `magic: "ArrPut"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]=`

[ref: #symbol-]

**Input:**
- `s: var openArray[T]`
- `i: BackwardsIndex`
- `x: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `systemRaisesDefect`

### `[]=`

[ref: #symbol-]

**Input:**
- `a: var array[Idx, T]`
- `i: BackwardsIndex`
- `x: T`

**Output:** *(none)*
**Generic parameters:** `Idx`, `T`

**Pragmas:** `inline`, `systemRaisesDefect`

### `[]=`

[ref: #symbol-]

**Input:**
- `s: var string`
- `i: BackwardsIndex`
- `x: char`

**Output:** *(none)*
**Pragmas:** `inline`, `systemRaisesDefect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]=`

[ref: #symbol-]

Slice assignment for strings.

**Input:**
- `s: var string`
- `x: HSlice[T, U]`
- `b: string`

**Output:** *(none)*
**Generic parameters:** `T`, `U`

**Pragmas:** `systemRaisesDefect`

Slice assignment for strings.

If b.len is not exactly the number of elements that are referred to by x, a splice is performed:

### `[]=`

[ref: #symbol-]

Slice assignment for arrays.

**Input:**
- `a: var array[Idx, T]`
- `x: HSlice[U, V]`
- `b: openArray[T]`

**Output:** *(none)*
**Generic parameters:** `Idx`, `T`, `U`, `V`

**Pragmas:** `systemRaisesDefect`

Slice assignment for arrays.

```
var a = [10, 20, 30, 40, 50]
a[1..2] = @[99, 88]
assert a == [10, 99, 88, 40, 50]
```

### `[]=`

[ref: #symbol-]

Slice assignment for sequences.

**Input:**
- `s: var seq[T]`
- `x: HSlice[U, V]`
- `b: openArray[T]`

**Output:** *(none)*
**Generic parameters:** `T`, `U`, `V`

**Pragmas:** `systemRaisesDefect`

Slice assignment for sequences.

If b.len is not exactly the number of elements that are referred to by x, a splice is performed.

### `[]`

[ref: #symbol-]

**Input:**
- `a: T`
- `i: I`

**Output:** `T`
**Generic parameters:** `I`, `T`

**Pragmas:** `noSideEffect`, `magic: "ArrGet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]`

[ref: #symbol-]

**Input:**
- `s: openArray[T]`
- `i: BackwardsIndex`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`, `systemRaisesDefect`

### `[]`

[ref: #symbol-]

**Input:**
- `a: array[Idx, T]`
- `i: BackwardsIndex`

**Output:** `T`
**Generic parameters:** `Idx`, `T`

**Pragmas:** `inline`, `systemRaisesDefect`

### `[]`

[ref: #symbol-]

**Input:**
- `s: string`
- `i: BackwardsIndex`

**Output:** `char`
**Pragmas:** `inline`, `systemRaisesDefect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]`

[ref: #symbol-]

**Input:**
- `s: var openArray[T]`
- `i: BackwardsIndex`

**Output:** `var T`
**Generic parameters:** `T`

**Pragmas:** `inline`, `systemRaisesDefect`

### `[]`

[ref: #symbol-]

**Input:**
- `a: var array[Idx, T]`
- `i: BackwardsIndex`

**Output:** `var T`
**Generic parameters:** `Idx`, `T`

**Pragmas:** `inline`, `systemRaisesDefect`

### `[]`

[ref: #symbol-]

**Input:**
- `s: var string`
- `i: BackwardsIndex`

**Output:** `var char`
**Pragmas:** `inline`, `systemRaisesDefect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]`

[ref: #symbol-]

Slice operation for strings. Returns the inclusive range [s[x.a], s[x.b]]:

**Input:**
- `s: string`
- `x: HSlice[T, U]`

**Output:** `string`
**Generic parameters:** `T`, `U`

**Pragmas:** `inline`, `systemRaisesDefect`

Slice operation for strings. Returns the inclusive range [s[x.a], s[x.b]]:

```
var s = "abcdef"
assert s[1..3] == "bcd"
```

### `[]`

[ref: #symbol-]

Slice operation for arrays. Returns the inclusive range [a[x.a], a[x.b]]:

**Input:**
- `a: array[Idx, T]`
- `x: HSlice[U, V]`

**Output:** `seq[T]`
**Generic parameters:** `Idx`, `T`, `U`, `V`

**Pragmas:** `systemRaisesDefect`

Slice operation for arrays. Returns the inclusive range [a[x.a], a[x.b]]:

```
var a = [1, 2, 3, 4]
assert a[0..2] == @[1, 2, 3]
```

See also:

* [toOpenArray(array[I, T];I,I)](#toOpenArray,array[I,T],I,I)

### `[]`

[ref: #symbol-]

Slice operation for sequences. Returns the inclusive range [s[x.a], s[x.b]]:

**Input:**
- `s: openArray[T]`
- `x: HSlice[U, V]`

**Output:** `seq[T]`
**Generic parameters:** `T`, `U`, `V`

**Pragmas:** `systemRaisesDefect`

Slice operation for sequences. Returns the inclusive range [s[x.a], s[x.b]]:

```
var s = @[1, 2, 3, 4]
assert s[0..2] == @[1, 2, 3]
```

See also:

* [toOpenArray(openArray[T];int,int)](#toOpenArray,openArray[T],int,int)

### `addr`

[ref: #symbol-addr]

Builtin addr operator for taking the address of a memory location.

**Input:**
- `x: T`

**Output:** `ptr T`
**Generic parameters:** `T`

**Pragmas:** `magic: "Addr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Builtin addr operator for taking the address of a memory location.

**Note:**
This works for let variables or parameters for better interop with C. When you use it to write a wrapper for a C library and take the address of let variables or parameters, you should always check that the original library does never write to data behind the pointer that is returned from this procedure.

Cannot be overloaded.

```
var
  buf: seq[char] = @['a','b','c']
  p = buf[1].addr
echo p.repr # ref 0x7faa35c40059 --> 'b'
echo p[]    # b
```

### `and`

[ref: #symbol-and]

Boolean and; returns true if x == y == true (if both arguments are true).

**Input:**
- `x: bool`
- `y: bool`

**Output:** `bool`
**Pragmas:** `magic: "And"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Boolean and; returns true if x == y == true (if both arguments are true).

Evaluation is lazy: if x is false, y will not even be evaluated.

### `and`

[ref: #symbol-and]

**Input:**
- `a: typedesc`
- `b: typedesc`

**Output:** `typedesc`
**Generic parameters:** `a:type`, `b:type`, `result:type`

**Pragmas:** `magic: "TypeTrait"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructs an and meta class.

### `and`

[ref: #symbol-and]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise and of numbers x and y.

### `and`

[ref: #symbol-and]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `uint`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise and of numbers x and y.

### `and`

[ref: #symbol-and]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "BitandI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

Computes the integer division.

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "DivI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the integer division.

This is roughly the same as math.trunc(x/y).int.

### `div`

[ref: #symbol-div]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "DivI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "DivI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "DivI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "DivI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: uint`
- `y: uint`

**Output:** `uint`
**Pragmas:** `magic: "DivU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the integer division for unsigned integers. This is roughly the same as trunc(x/y).

### `div`

[ref: #symbol-div]

**Input:**
- `x: uint8`
- `y: uint8`

**Output:** `uint8`
**Pragmas:** `magic: "DivU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: uint16`
- `y: uint16`

**Output:** `uint16`
**Pragmas:** `magic: "DivU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: uint32`
- `y: uint32`

**Output:** `uint32`
**Pragmas:** `magic: "DivU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: uint64`
- `y: uint64`

**Output:** `uint64`
**Pragmas:** `magic: "DivU"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `is`

[ref: #symbol-is]

Checks if T is of the same type as S.

**Input:**
- `x: T`
- `y: S`

**Output:** `bool`
**Generic parameters:** `T`, `S`

**Pragmas:** `magic: "Is"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if T is of the same type as S.

For a negated version, use [isnot](#isnot.t,untyped,untyped).

```
assert 42 is int
assert @[1, 2] is seq

proc test[T](a: T): int =
  when (T is int):
    return a
  else:
    return 0

assert(test[int](3) == 3)
assert(test[string]("xyz") == 0)
```

### `mod`

[ref: #symbol-mod]

Computes the integer modulo operation (remainder).

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "ModI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the integer modulo operation (remainder).

This is the same as x - (x div y) \* y.


[Prev](system_4.md) | [Next](system_6.md)
