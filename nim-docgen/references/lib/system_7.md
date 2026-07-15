---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

### abs

[ref: #symbol-abs]

**Input:**
- `x: int32`

**Output:** `int32`
**Pragmas:** `magic: "AbsI"`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### abs

[ref: #symbol-abs]

Returns the absolute value of x.

**Input:**
- `x: int64`

**Output:** `int64`
**Pragmas:** `magic: "AbsI"`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the absolute value of x.

If x is low(x) (that is -MININT for its type), an overflow exception is thrown (if overflow checking is turned on).

### add

[ref: #symbol-add]

Appends y to x in place.

**Input:**
- `x: var string`
- `y: char`

**Output:** *(none)*
**Pragmas:** `magic: "AppendStrCh"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Appends y to x in place.

```
var tmp = ""
tmp.add('a')
tmp.add('b')
assert(tmp == "ab")
```

### add

[ref: #symbol-add]

Concatenates x and y in place.

**Input:**
- `x: var string`
- `y: string`

**Output:** *(none)*
**Pragmas:** `magic: "AppendStrStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenates x and y in place.

See also strbasics.add.

### add

[ref: #symbol-add]

Generic proc for adding a container y to a container x.

**Input:**
- `x: var seq[T]`
- `y: openArray[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Generic proc for adding a container y to a container x.

For containers that have an order, add means *append*. New generic containers should also call their adding proc add for consistency. Generic code becomes much easier to write if the Nim naming scheme is respected.

See also:

* [& proc](#&,seq[T],seq[T])

### add

[ref: #symbol-add]

Generic proc for adding a data item y to a container x.

**Input:**
- `x: var seq[T]`
- `y: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "AppendSeqElem"`, `noSideEffect`, `nodestroy`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic proc for adding a data item y to a container x.

For containers that have an order, add means *append*. New generic containers should also call their adding proc add for consistency. Generic code becomes much easier to write if the Nim naming scheme is respected.

### add

[ref: #symbol-add]

**Input:**
- `x: var string`
- `y: cstring`

**Output:** *(none)*
**Pragmas:** `asmNoStackFrame`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Appends y to x in place.

### add

[ref: #symbol-add]

**Input:**
- `x: var cstring`
- `y: cstring`

**Output:** *(none)*
**Pragmas:** `magic: "AppendStrStr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Appends y to x in place. Only implemented for JS backend.

### addEscapedChar

[ref: #symbol-addescapedchar]

Adds a char to string s and applies the following escaping:

**Input:**
- `s: var string`
- `c: char`

**Output:** *(none)*
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds a char to string s and applies the following escaping:

* replaces any \ by \\
* replaces any ' by \'
* replaces any " by \"
* replaces any \a by \\a
* replaces any \b by \\b
* replaces any \t by \\t
* replaces any \n by \\n
* replaces any \v by \\v
* replaces any \f by \\f
* replaces any \r by \\r
* replaces any \e by \\e
* replaces any other character not in the set {\21..\126} by \xHH where HH is its hexadecimal value

The procedure has been designed so that its output is usable for many different common syntaxes.

**Warning:**
This is **not correct** for producing ANSI C code!

### addQuitProc

[ref: #symbol-addquitproc]

Adds/registers a quit procedure.

**Input:**
- `quitProc: proc () {.noconv.}`

**Output:** *(none)*
**Pragmas:** `importc: "atexit"`, `header: "<stdlib.h>"`, `deprecated: "use exitprocs.addExitProc"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds/registers a quit procedure.

Each call to addQuitProc registers another quit procedure. Up to 30 procedures can be registered. They are executed on a last-in, first-out basis (that is, the last function registered is the first to be executed). addQuitProc raises an EOutOfIndex exception if quitProc cannot be registered.

### addQuoted

[ref: #symbol-addquoted]

Appends x to string s in place, applying quoting and escaping if x is a string or char.

**Input:**
- `s: var string`
- `x: T`

**Output:** *(none)*
**Generic parameters:** `T`

Appends x to string s in place, applying quoting and escaping if x is a string or char.

See [addEscapedChar](#addEscapedChar,string,char) for the escaping scheme. When x is a string, characters in the range {\128..\255} are never escaped so that multibyte UTF-8 characters are untouched (note that this behavior is different from addEscapedChar).

The Nim standard library uses this function on the elements of collections when producing a string representation of a collection. It is recommended to use this function as well for user-side collections. Users may overload addQuoted for custom (string-like) types if they want to implement a customized element representation.

```
var tmp = ""
tmp.addQuoted(1)
tmp.add(", ")
tmp.addQuoted("string")
tmp.add(", ")
tmp.addQuoted('c')
assert(tmp == """1, "string", 'c'""")
```

### alignof

[ref: #symbol-alignof]

**Input:**
- `x: T`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `magic: "AlignOf"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### alignof

[ref: #symbol-alignof]

**Input:**
- `x: typedesc`

**Output:** `int`
**Generic parameters:** `x:type`

**Pragmas:** `magic: "AlignOf"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### alloc0Impl

[ref: #symbol-alloc0impl]

**Input:**
- `size: Natural`

**Output:** `pointer`
**Pragmas:** `noconv`, `gcsafe`, `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

### allocCStringArray

[ref: #symbol-alloccstringarray]

**Input:**
- `a: openArray[string]`

**Output:** `cstringArray`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a NULL terminated cstringArray from a. The result has to be freed with deallocCStringArray after it's not needed anymore.

### allocImpl

[ref: #symbol-allocimpl]

**Input:**
- `size: Natural`

**Output:** `pointer`
**Pragmas:** `noconv`, `gcsafe`, `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

### allocShared0Impl

[ref: #symbol-allocshared0impl]

**Input:**
- `size: Natural`

**Output:** `pointer`
**Pragmas:** `noconv`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### allocSharedImpl

[ref: #symbol-allocsharedimpl]

**Input:**
- `size: Natural`

**Output:** `pointer`
**Pragmas:** `noconv`, `compilerproc`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### arrayWith

[ref: #symbol-arraywith]

**Input:**
- `y: T`
- `size: static int`

**Output:** `array[size, T]`
**Generic parameters:** `T`, `size:type`

**Pragmas:** `noinit`, `nodestroy`, `raises: []`

**Effects:** `raises: `

Creates a new array filled with y.

### arrayWithDefault

[ref: #symbol-arraywithdefault]

**Input:**
- `size: static int`

**Output:** `array[size, T]`
**Generic parameters:** `T`, `size:type`

**Pragmas:** `noinit`, `nodestroy`, `raises: []`

**Effects:** `raises: `

Creates a new array filled with default(T).

### ashr

[ref: #symbol-ashr]

Shifts right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off. y (the number of positions to shift) is reduced to modulo sizeof(x) \* 8. That is ashr(15'i32, 35) is equivalent to ashr(15'i32, 3).

**Input:**
- `x: int`
- `y: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Shifts right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off. y (the number of positions to shift) is reduced to modulo sizeof(x) \* 8. That is ashr(15'i32, 35) is equivalent to ashr(15'i32, 3).

Note that ashr is not an operator so use the normal function call syntax for it.

See also:

* [shr func](#shr,int,SomeInteger)

### ashr

[ref: #symbol-ashr]

**Input:**
- `x: int8`
- `y: SomeInteger`

**Output:** `int8`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ashr

[ref: #symbol-ashr]

**Input:**
- `x: int16`
- `y: SomeInteger`

**Output:** `int16`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ashr

[ref: #symbol-ashr]

**Input:**
- `x: int32`
- `y: SomeInteger`

**Output:** `int32`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ashr

[ref: #symbol-ashr]

**Input:**
- `x: int64`
- `y: SomeInteger`

**Output:** `int64`
**Generic parameters:** `SomeInteger`

**Pragmas:** `magic: "AshrI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### astToStr

[ref: #symbol-asttostr]

**Input:**
- `x: T`

**Output:** `string`
**Generic parameters:** `T`

**Pragmas:** `magic: "AstToStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the AST of x into a string representation. This is very useful for debugging.

### capacity

[ref: #symbol-capacity]

**Input:**
- `self: string`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the current capacity of the string.

### capacity

[ref: #symbol-capacity]

**Input:**
- `self: seq[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the current capacity of the seq.

### card

[ref: #symbol-card]

**Input:**
- `x: set[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `magic: "Card"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the cardinality of the set x, i.e. the number of elements in the set.

### chr

[ref: #symbol-chr]

**Input:**
- `u: range[0 .. 255]`

**Output:** `char`
**Pragmas:** `magic: "Chr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts u to a char, same as char(u).

### clamp

[ref: #symbol-clamp]

Limits the value x within the interval [a, b]. This proc is equivalent to but faster than max(a, min(b, x)).

**Input:**
- `x: T`
- `a: T`
- `b: T`

**Output:** `T`
**Generic parameters:** `T`

Limits the value x within the interval [a, b]. This proc is equivalent to but faster than max(a, min(b, x)).

**Warning:**
a <= b is assumed and will not be checked (currently).

**See also:** math.clamp for a version that takes a Slice[T] instead.

### close

[ref: #symbol-close]

**Input:**
- `c: var Channel[TMsg]`

**Output:** *(none)*
**Generic parameters:** `TMsg`

**Pragmas:** `raises: []`, `gcsafe`

**Effects:** `raises: `

Closes a channel c and frees its associated resources.

### cmp

[ref: #symbol-cmp]

Generic compare proc.

**Input:**
- `x: T`
- `y: T`

**Output:** `int`
**Generic parameters:** `T`

Generic compare proc.

Returns:

* a value less than zero, if x < y
* a value greater than zero, if x > y
* zero, if x == y

This is useful for writing generic algorithms without performance loss. This generic implementation uses the == and < operators.

```
import std/algorithm
echo sorted(@[4, 2, 6, 5, 8, 7], cmp[int])
```

### cmp

[ref: #symbol-cmp]

Compare proc for strings. More efficient than the generic version.

**Input:**
- `x: string`
- `y: string`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compare proc for strings. More efficient than the generic version.

**Note**: The precise result values depend on the used C runtime library and can differ between operating systems!

### cmpMem

[ref: #symbol-cmpmem]

Compares the memory blocks a and b. size bytes will be compared.

**Input:**
- `a: pointer`
- `b: pointer`
- `size: Natural`

**Output:** `int`
**Pragmas:** `inline`, `gcsafe`, `tags: []`, `raises: []`, `enforceNoRaises`, `noSideEffect`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Compares the memory blocks a and b. size bytes will be compared.

Returns:

* a value less than zero, if a < b
* a value greater than zero, if a > b
* zero, if a == b

Like any procedure dealing with raw memory this is **unsafe**.

### compileOption

[ref: #symbol-compileoption]

Can be used to determine an on|off compile-time option.

**Input:**
- `option: string`

**Output:** `bool`
**Pragmas:** `magic: "CompileOption"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Can be used to determine an on|off compile-time option.

See also:

* [compileOption](#compileOption,string,string) for enum options
* [defined](#defined,untyped)
* [std/compilesettings module](compilesettings.html)

### compileOption

[ref: #symbol-compileoption]

Can be used to determine an enum compile-time option.

**Input:**
- `option: string`
- `arg: string`

**Output:** `bool`
**Pragmas:** `magic: "CompileOptionArg"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Can be used to determine an enum compile-time option.

See also:

* [compileOption](#compileOption,string) for on|off options
* [defined](#defined,untyped)
* [std/compilesettings module](compilesettings.html)

### compiles

[ref: #symbol-compiles]

Special compile-time procedure that checks whether x can be compiled without any semantic error. This can be used to check whether a type supports some operation:

**Input:**
- `x: untyped`

**Output:** `bool`
**Pragmas:** `magic: "Compiles"`, `noSideEffect`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Special compile-time procedure that checks whether x can be compiled without any semantic error. This can be used to check whether a type supports some operation:

```
when compiles(3 + 4):
  echo "'+' for integers is available"
```

### contains

[ref: #symbol-contains]

One should overload this proc if one wants to overload the in operator.

**Input:**
- `x: set[T]`
- `y: T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "InSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

One should overload this proc if one wants to overload the in operator.

The parameters are in reverse order! a in b is a template for contains(b, a). This is because the unification algorithm that Nim uses for overload resolution works from left to right. But for the in operator that would be the wrong direction for this piece of code:

### contains

[ref: #symbol-contains]

Checks if value is within the range of s; returns true if value >= s.a and value <= s.b.

**Input:**
- `s: HSlice[U, V]`
- `value: W`

**Output:** `bool`
**Generic parameters:** `U`, `V`, `W`

**Pragmas:** `noSideEffect`, `inline`

Checks if value is within the range of s; returns true if value >= s.a and value <= s.b.

```
assert((1..3).contains(1) == true)
assert((1..3).contains(2) == true)
assert((1..3).contains(4) == false)
```

### contains

[ref: #symbol-contains]

Returns true if item is in a or false if not found. This is a shortcut for find(a, item) >= 0.

**Input:**
- `a: openArray[T]`
- `item: T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns true if item is in a or false if not found. This is a shortcut for find(a, item) >= 0.

This allows the in operator: a.contains(item) is the same as item in a.

```
var a = @[1, 3, 5]
assert a.contains(5)
assert 3 in a
assert 99 notin a
```

### copyMem

[ref: #symbol-copymem]

**Input:**
- `dest: pointer`
- `source: pointer`
- `size: Natural`

**Output:** *(none)*
**Pragmas:** `inline`, `gcsafe`, `tags: []`, `raises: []`, `enforceNoRaises`, `noSideEffect`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Copies the contents from the memory at source to the memory at dest. Exactly size bytes will be copied. The memory regions may not overlap. Like any procedure dealing with raw memory this is **unsafe**.

### create

[ref: #symbol-create]

Allocates a new memory block with at least T.sizeof \* size bytes.

**Input:**
- `T: typedesc`
- `size:  = 1.Positive`

**Output:** `ptr T:type`
**Generic parameters:** `T:type`

**Pragmas:** `inline`, `gcsafe`, `raises: []`

**Effects:** `raises: `

Allocates a new memory block with at least T.sizeof \* size bytes.

The block has to be freed with [resize(block, 0)](#resize,ptr.T,Natural) or [dealloc(block)](#dealloc,pointer). The block is initialized with all bytes containing zero, so it is somewhat safer than [createU](#createU,typedesc).

The allocated memory belongs to its allocating thread! Use [createShared](#createShared,typedesc) to allocate from a shared heap.

### createShared

[ref: #symbol-createshared]

Allocates a new memory block on the shared heap with at least T.sizeof \* size bytes.

**Input:**
- `T: typedesc`
- `size:  = 1.Positive`

**Output:** `ptr T:type`
**Generic parameters:** `T:type`

**Pragmas:** `inline`

Allocates a new memory block on the shared heap with at least T.sizeof \* size bytes.

The block has to be freed with [resizeShared(block, 0)](#resizeShared,ptr.T,Natural) or [freeShared(block)](#freeShared,ptr.T).

The block is initialized with all bytes containing zero, so it is somewhat safer than [createSharedU](#createSharedU,typedesc).

### createSharedU

[ref: #symbol-createsharedu]

Allocates a new memory block on the shared heap with at least T.sizeof \* size bytes.

**Input:**
- `T: typedesc`
- `size:  = 1.Positive`

**Output:** `ptr T:type`
**Generic parameters:** `T:type`

**Pragmas:** `inline`, `tags: []`, `gcsafe`, `raises: []`

**Effects:** `tags: `, `raises: `

Allocates a new memory block on the shared heap with at least T.sizeof \* size bytes.

The block has to be freed with [resizeShared(block, 0)](#resizeShared,ptr.T,Natural) or [freeShared(block)](#freeShared,ptr.T).

The block is not initialized, so reading from it before writing to it is undefined behaviour!

See also:

* [createShared](#createShared,typedesc)

### createU

[ref: #symbol-createu]

Allocates a new memory block with at least T.sizeof \* size bytes.

**Input:**
- `T: typedesc`
- `size:  = 1.Positive`

**Output:** `ptr T:type`
**Generic parameters:** `T:type`

**Pragmas:** `inline`, `gcsafe`, `raises: []`

**Effects:** `raises: `

Allocates a new memory block with at least T.sizeof \* size bytes.

The block has to be freed with [resize(block, 0)](#resize,ptr.T,Natural) or [dealloc(block)](#dealloc,pointer). The block is not initialized, so reading from it before writing to it is undefined behaviour!

The allocated memory belongs to its allocating thread! Use [createSharedU](#createSharedU,typedesc) to allocate from a shared heap.

See also:

* [create](#create,typedesc)

### cstringArrayToSeq

[ref: #symbol-cstringarraytoseq]

**Input:**
- `a: cstringArray`
- `len: Natural`

**Output:** `seq[string]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a cstringArray to a seq[string]. a is supposed to be of length len.

### cstringArrayToSeq

[ref: #symbol-cstringarraytoseq]

**Input:**
- `a: cstringArray`

**Output:** `seq[string]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a cstringArray to a seq[string]. a is supposed to be terminated by nil.

### dealloc

[ref: #symbol-dealloc]

Frees the memory allocated with alloc, alloc0, realloc, create or createU.

**Input:**
- `p: pointer`

**Output:** *(none)*
**Pragmas:** `noconv`, `compilerproc`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Frees the memory allocated with alloc, alloc0, realloc, create or createU.

**This procedure is dangerous!** If one forgets to free the memory a leak occurs; if one tries to access freed memory (or just freeing it twice!) a core dump may happen or other memory may be corrupted.

The freed memory must belong to its allocating thread! Use [deallocShared](#deallocShared,pointer) to deallocate from a shared heap.

### deallocCStringArray

[ref: #symbol-dealloccstringarray]

**Input:**
- `a: cstringArray`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Frees a NULL terminated cstringArray.

### deallocImpl

[ref: #symbol-deallocimpl]

**Input:**
- `p: pointer`

**Output:** *(none)*
**Pragmas:** `noconv`, `gcsafe`, `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

### deallocShared

[ref: #symbol-deallocshared]

Frees the memory allocated with allocShared, allocShared0 or reallocShared.

**Input:**
- `p: pointer`

**Output:** *(none)*
**Pragmas:** `noconv`, `compilerproc`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Frees the memory allocated with allocShared, allocShared0 or reallocShared.

**This procedure is dangerous!** If one forgets to free the memory a leak occurs; if one tries to access freed memory (or just freeing it twice!) a core dump may happen or other memory may be corrupted.

### deallocSharedImpl

[ref: #symbol-deallocsharedimpl]

**Input:**
- `p: pointer`

**Output:** *(none)*
**Pragmas:** `noconv`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### debugEcho

[ref: #symbol-debugecho]

**Input:**
- `x: varargs[typed, `$`]`

**Output:** *(none)*
**Pragmas:** `magic: "Echo"`, `noSideEffect`, `tags: []`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Same as [echo](#echo,varargs[typed,]), but as a special semantic rule, debugEcho pretends to be free of side effects, so that it can be used for debugging routines marked as [noSideEffect](manual.html#pragmas-nosideeffect-pragma).


[Prev](system_6.md) | [Next](system_8.md)
