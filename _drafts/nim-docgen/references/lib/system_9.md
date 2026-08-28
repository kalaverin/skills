---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

### inc

[ref: #symbol-inc]

Increments the ordinal x by y.

**Input:**
- `x: var T`
- `y: V = 1`

**Output:** *(none)*
**Generic parameters:** `T`, `V`

**Pragmas:** `magic: "Inc"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Increments the ordinal x by y.

If such a value does not exist, OverflowDefect is raised or a compile time error occurs. This is a short notation for: x = succ(x, y).

### incl

[ref: #symbol-incl]

Includes element y in the set x.

**Input:**
- `x: var set[T]`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "Incl"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Includes element y in the set x.

This is the same as x = x + {y}, but it might be more efficient.

### insert

[ref: #symbol-insert]

Inserts item into x at position i.

**Input:**
- `x: var seq[T]`
- `item: sink T`
- `i:  = 0.Natural`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Inserts item into x at position i.

```
var i = @[1, 3, 5]
i.insert(99, 0) # i <- @[99, 1, 3, 5]
```

### insert

[ref: #symbol-insert]

Inserts item into x at position i.

**Input:**
- `x: var string`
- `item: string`
- `i:  = 0.Natural`

**Output:** *(none)*
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Inserts item into x at position i.

```
var a = "abc"
a.insert("zz", 0) # a <- "zzabc"
```

### instantiationInfo

[ref: #symbol-instantiationinfo]

Provides access to the compiler's instantiation stack line information of a template.

**Input:**
- `index:  = -1`
- `fullPaths:  = false`

**Output:** `tuple[filename: string, line: int, column: int]`
**Pragmas:** `magic: "InstantiationInfo"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Provides access to the compiler's instantiation stack line information of a template.

While similar to the caller info of other languages, it is determined at compile time.

This proc is mostly useful for meta programming (eg. assert template) to retrieve information about the current filename and line number. Example:

```
import std/strutils

template testException(exception, code: untyped): typed =
  try:
    let pos = instantiationInfo()
    discard(code)
    echo "Test failure at $1:$2 with '$3'" % [pos.filename,
      $pos.line, astToStr(code)]
    assert false, "A test expecting failure succeeded?"
  except exception:
    discard

proc tester(pos: int): int =
  let
    a = @[1, 2, 3]
  result = a[pos]

when isMainModule:
  testException(IndexDefect, tester(30))
  testException(IndexDefect, tester(1))
  # --> Test failure at example.nim:20 with 'tester(1)'
```

### isNil

[ref: #symbol-isnil]

**Input:**
- `x: string`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `error: "\'isNil\' is invalid for \'string\'"`

### isNil

[ref: #symbol-isnil]

**Input:**
- `x: ref T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `magic: "IsNil"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isNil

[ref: #symbol-isnil]

**Input:**
- `x: ptr T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `magic: "IsNil"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isNil

[ref: #symbol-isnil]

**Input:**
- `x: pointer`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `magic: "IsNil"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isNil

[ref: #symbol-isnil]

**Input:**
- `x: cstring`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `magic: "IsNil"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isNil

[ref: #symbol-isnil]

**Input:**
- `x: T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `magic: "IsNil"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Fast check whether x is nil. This is sometimes more efficient than == nil.

### isNotForeign

[ref: #symbol-isnotforeign]

**Input:**
- `x: ForeignCell`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isUniqueRef

[ref: #symbol-isuniqueref]

**Input:**
- `x: ref T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`, `raises: []`

**Effects:** `raises: `

Returns true if the object x points to is uniquely referenced. Such an object can potentially be passed over to a different thread safely, if great care is taken. This queries the internal reference count of the object which is subject to lots of optimizations! In other words the value of isUniqueRef can depend on the used compiler version and optimizer setting. Nevertheless it can be used as a very valuable debugging tool and can be used to specify the constraints of a threading related API via assert isUniqueRef(x).

### iterToProc

[ref: #symbol-itertoproc]

**Input:**
- `iter: typed`
- `envType: typedesc`
- `procName: untyped`

**Output:** *(none)*
**Generic parameters:** `envType:type`

**Pragmas:** `magic: "Plugin"`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### len

[ref: #symbol-len]

**Input:**
- `x: TOpenArray`

**Output:** `int`
**Generic parameters:** `TOpenArray`

**Pragmas:** `magic: "LengthOpenArray"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the length of an openArray.

### len

[ref: #symbol-len]

**Input:**
- `x: string`

**Output:** `int`
**Pragmas:** `magic: "LengthStr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the length of a string.

### len

[ref: #symbol-len]

Returns the length of a compatible string. This is an O(n) operation except in js at runtime.

**Input:**
- `x: cstring`

**Output:** `int`
**Pragmas:** `magic: "LengthStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the length of a compatible string. This is an O(n) operation except in js at runtime.

**Note:** On the JS backend this currently counts UTF-16 code points instead of bytes at runtime (not at compile time). For now, if you need the byte length of the UTF-8 encoding, convert to string with $ first then call len.

### len

[ref: #symbol-len]

**Input:**
- `x: (type array) | array`

**Output:** `int`
**Generic parameters:** `x:type`

**Pragmas:** `magic: "LengthArray"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the length of an array or an array type. This is roughly the same as high(T)-low(T)+1.

### len

[ref: #symbol-len]

**Input:**
- `x: seq[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `magic: "LengthSeq"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the length of x.

### len

[ref: #symbol-len]

**Input:**
- `x: set[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `magic: "Card"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

An alias for card(x).

### len

[ref: #symbol-len]

Length of ordinal slice. When x.b < x.a returns zero length.

**Input:**
- `x: HSlice[U, V]`

**Output:** `int`
**Generic parameters:** `U`, `V`

**Pragmas:** `noSideEffect`, `inline`

Length of ordinal slice. When x.b < x.a returns zero length.

```
assert((0..5).len == 6)
assert((5..2).len == 0)
```

### locals

[ref: #symbol-locals]

Generates a tuple constructor expression listing all the local variables in the current scope.

**Input:**
- *(none)*

**Output:** `RootObj`
**Pragmas:** `magic: "Plugin"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generates a tuple constructor expression listing all the local variables in the current scope.

This is quite fast as it does not rely on any debug or runtime information. Note that in contrast to what the official signature says, the return type is *not* RootObj but a tuple of a structure that depends on the current scope. Example:

```
proc testLocals() =
  var
    a = "something"
    b = 4
    c = locals()
    d = "super!"
  
  b = 1
  for name, value in fieldPairs(c):
    echo "name ", name, " with value ", value
  echo "B is ", b
# -> name a with value something
# -> name b with value 4
# -> B is 1
```

### low

[ref: #symbol-low]

Returns the lowest possible value of an ordinal value x. As a special semantic rule, x may also be a type identifier.

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `magic: "Low"`, `noSideEffect`, `deprecated: "Deprecated since v1.4; there should not be `low(value)`. Use `low(type)`."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the lowest possible value of an ordinal value x. As a special semantic rule, x may also be a type identifier.

**This proc is deprecated**, use this one instead:

* [low(typedesc)](#low,typedesc[T])

```
low(2) # => -9223372036854775808
```

### low

[ref: #symbol-low]

Returns the lowest possible value of an ordinal or enum type.

**Input:**
- `x: typedesc[T]`

**Output:** `T`
**Generic parameters:** `T`, `x:type`

**Pragmas:** `magic: "Low"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the lowest possible value of an ordinal or enum type.

low(int) is Nim's way of writing INT\_MIN or MIN\_INT.

```
low(int) # => -9223372036854775808
```

See also:

* [high(typedesc)](#high,typedesc[T])

### low

[ref: #symbol-low]

Returns the lowest possible index of a sequence x.

**Input:**
- `x: openArray[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `magic: "Low"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the lowest possible index of a sequence x.

```
var s = @[1, 2, 3, 4, 5, 6, 7]
low(s) # => 0
for i in low(s)..high(s):
  echo s[i]
```

See also:

* [high(openArray)](#high,openArray[T])

### low

[ref: #symbol-low]

Returns the lowest possible index of an array x.

**Input:**
- `x: array[I, T]`

**Output:** `I`
**Generic parameters:** `I`, `T`

**Pragmas:** `magic: "Low"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the lowest possible index of an array x.

For empty arrays, the return type is int.

```
var arr = [1, 2, 3, 4, 5, 6, 7]
low(arr) # => 0
for i in low(arr)..high(arr):
  echo arr[i]
```

See also:

* [high(array)](#high,array[I,T])

### low

[ref: #symbol-low]

Returns the lowest possible index of an array type.

**Input:**
- `x: typedesc[array[I, T]]`

**Output:** `I`
**Generic parameters:** `I`, `T`, `x:type`

**Pragmas:** `magic: "Low"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the lowest possible index of an array type.

For empty arrays, the return type is int.

```
low(array[7, int]) # => 0
```

See also:

* [high(typedesc[array])](#high,typedesc[array[I,T]])

### low

[ref: #symbol-low]

Returns the lowest possible index of a compatible string x.

**Input:**
- `x: cstring`

**Output:** `int`
**Pragmas:** `magic: "Low"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the lowest possible index of a compatible string x.

See also:

* [high(cstring)](#high,cstring)

### low

[ref: #symbol-low]

Returns the lowest possible index of a string x.

**Input:**
- `x: string`

**Output:** `int`
**Pragmas:** `magic: "Low"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the lowest possible index of a string x.

```
var str = "Hello world!"
low(str) # => 0
```

See also:

* [high(string)](#high,string)

### low

[ref: #symbol-low]

**Input:**
- `T: typedesc[SomeFloat]`

**Output:** `T:type`
**Generic parameters:** `T:type`

### max

[ref: #symbol-max]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "MaxI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "MaxI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "MaxI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "MaxI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "MaxI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The maximum value of two integers.

### max

[ref: #symbol-max]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: float64`
- `y: float64`

**Output:** `float64`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Generic maximum operator of 2 values based on <=.

### max

[ref: #symbol-max]

**Input:**
- `x: openArray[T]`

**Output:** `T`
**Generic parameters:** `T`

The maximum value of x. T needs to have a < operator.

### min

[ref: #symbol-min]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "MinI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "MinI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "MinI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "MinI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "MinI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The minimum value of two integers.

### min

[ref: #symbol-min]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: float64`
- `y: float64`

**Output:** `float64`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Generic minimum operator of 2 values based on <=.

### min

[ref: #symbol-min]

**Input:**
- `x: openArray[T]`

**Output:** `T`
**Generic parameters:** `T`

The minimum value of x. T needs to have a < operator.

### move

[ref: #symbol-move]

**Input:**
- `x: var T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `magic: "Move"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### moveMem

[ref: #symbol-movemem]

Copies the contents from the memory at source to the memory at dest.

**Input:**
- `dest: pointer`
- `source: pointer`
- `size: Natural`

**Output:** *(none)*
**Pragmas:** `inline`, `gcsafe`, `tags: []`, `raises: []`, `enforceNoRaises`, `noSideEffect`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Copies the contents from the memory at source to the memory at dest.

Exactly size bytes will be copied. The memory regions may overlap, moveMem handles this case appropriately and is thus somewhat more safe than copyMem. Like any procedure dealing with raw memory this is still **unsafe**, though.

### new

[ref: #symbol-new]

Creates a new object of type T and returns a safe (traced) reference to it in a.

**Input:**
- `a: var ref T`
- `finalizer: proc (x: T) {.nimcall.}`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "NewFinalize"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new object of type T and returns a safe (traced) reference to it in a.

When the garbage collector frees the object, finalizer is called. The finalizer may not keep a reference to the object pointed to by x. The finalizer cannot prevent the GC from freeing the object.

**Note**: The finalizer refers to the type T, not to the object! This means that for each object of type T the finalizer will be called!

### new

[ref: #symbol-new]

**Input:**
- `a: var ref T`
- `finalizer: proc (x: ref T) {.nimcall.}`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "NewFinalize"`, `noSideEffect`, `deprecated: "pass a finalizer of the \'proc (x: T) {.nimcall.}\' type"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### new

[ref: #symbol-new]

**Input:**
- `a: var ref T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "New"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new object of type T and returns a safe (traced) reference to it in a.

### new

[ref: #symbol-new]

Creates a new object of type T and returns a safe (traced) reference to it as result value.

**Input:**
- `t: typedesc`

**Output:** `auto`
**Generic parameters:** `t:type`

Creates a new object of type T and returns a safe (traced) reference to it as result value.

When T is a ref type then the resulting type will be T, otherwise it will be ref T.

### newSeq

[ref: #symbol-newseq]

Creates a new sequence of type seq[T] with length len.

**Input:**
- `s: var seq[T]`
- `len: Natural`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "NewSeq"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new sequence of type seq[T] with length len.

This is equivalent to s = @[]; setlen(s, len), but more efficient since no reallocation is needed.

Note that the sequence will be filled with zeroed entries. After the creation of the sequence you should assign entries to the sequence instead of adding them. Example:

```
var inputStrings: seq[string]
newSeq(inputStrings, 3)
assert len(inputStrings) == 3
inputStrings[0] = "The fourth"
inputStrings[1] = "assignment"
inputStrings[2] = "would crash"
#inputStrings[3] = "out of bounds"
```


[Prev](system_8.md) | [Next](system_10.md)
