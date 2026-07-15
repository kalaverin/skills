---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

### substr

[ref: #symbol-substr]

Convenience [substr](#substr,string,int,int) overload that returns a substring from first to the end of the string.

**Input:**
- `s: string`
- `first:  = 0`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Convenience [substr](#substr,string,int,int) overload that returns a substring from first to the end of the string.

first value is validated and capped:

* first >= s.len returns an empty string
* Negative first is clamped to 0.

### succ

[ref: #symbol-succ]

Returns the y-th successor (default: 1) of the value x.

**Input:**
- `x: T`
- `y: V = 1`

**Output:** `T`
**Generic parameters:** `T`, `V`

**Pragmas:** `magic: "Succ"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the y-th successor (default: 1) of the value x.

If such a value does not exist, OverflowDefect is raised or a compile time error occurs.

### swap

[ref: #symbol-swap]

Swaps the values a and b.

**Input:**
- `a: var T`
- `b: var T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "Swap"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Swaps the values a and b.

This is often more efficient than tmp = a; a = b; b = tmp. Particularly useful for sorting algorithms.

```
var
  a = 5
  b = 9

swap(a, b)

assert a == 9
assert b == 5
```

### toBiggestFloat

[ref: #symbol-tobiggestfloat]

**Input:**
- `i: BiggestInt`

**Output:** `BiggestFloat`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as [toFloat](#toFloat,int) but for BiggestInt to BiggestFloat.

### toBiggestInt

[ref: #symbol-tobiggestint]

**Input:**
- `f: BiggestFloat`

**Output:** `BiggestInt`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as [toInt](#toInt,float) but for BiggestFloat to BiggestInt.

### toFloat

[ref: #symbol-tofloat]

Converts an integer i into a float. Same as float(i).

**Input:**
- `i: int`

**Output:** `float`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts an integer i into a float. Same as float(i).

If the conversion fails, ValueError is raised. However, on most platforms the conversion cannot fail.

```
let
  a = 2
  b = 3.7

echo a.toFloat + b # => 5.7
```

### toInt

[ref: #symbol-toint]

Converts a floating point number f into an int.

**Input:**
- `f: float`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a floating point number f into an int.

Conversion rounds f half away from 0, see [Round half away from zero](https://en.wikipedia.org/wiki/Rounding#Round_half_away_from_zero), as opposed to a type conversion which rounds towards zero.

Note that some floating point numbers (e.g. infinity or even 1e19) cannot be accurately converted.

```
doAssert toInt(0.49) == 0
doAssert toInt(0.5) == 1
doAssert toInt(-0.5) == -1 # rounding is symmetrical
```

### toOpenArray

[ref: #symbol-toopenarray]

**Input:**
- `x: ptr UncheckedArray[T]`
- `first: int`
- `last: int`

**Output:** `openArray[T]`
**Generic parameters:** `T`

**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toOpenArray

[ref: #symbol-toopenarray]

**Input:**
- `x: cstring`
- `first: int`
- `last: int`

**Output:** `openArray[char]`
**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toOpenArray

[ref: #symbol-toopenarray]

Returns a non-owning slice (a view) of x from the element at index first to last inclusive. Allows passing slices without copying, as opposed to using the slice operator [`[]`](#[],openArray[T],HSlice[U: Ordinal,V: Ordinal]).

**Input:**
- `x: seq[T]`
- `first: int`
- `last: int`

**Output:** `openArray[T]`
**Generic parameters:** `T`

**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a non-owning slice (a view) of x from the element at index first to last inclusive. Allows passing slices without copying, as opposed to using the slice operator [`[]`](#[],openArray[T],HSlice[U: Ordinal,V: Ordinal]).

Example:

```
proc test(x: openArray[int]) =
  doAssert x == [1, 2, 3]

let s = @[0, 1, 2, 3, 4]
s.toOpenArray(1, 3).test
```

### toOpenArray

[ref: #symbol-toopenarray]

**Input:**
- `x: openArray[T]`
- `first: int`
- `last: int`

**Output:** `openArray[T]`
**Generic parameters:** `T`

**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toOpenArray

[ref: #symbol-toopenarray]

**Input:**
- `x: array[I, T]`
- `first: I`
- `last: I`

**Output:** `openArray[T]`
**Generic parameters:** `I`, `T`

**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toOpenArray

[ref: #symbol-toopenarray]

**Input:**
- `x: string`
- `first: int`
- `last: int`

**Output:** `openArray[char]`
**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toOpenArrayByte

[ref: #symbol-toopenarraybyte]

**Input:**
- `x: cstring`
- `first: int`
- `last: int`

**Output:** `openArray[byte]`
**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toOpenArrayByte

[ref: #symbol-toopenarraybyte]

**Input:**
- `x: string`
- `first: int`
- `last: int`

**Output:** `openArray[byte]`
**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toOpenArrayByte

[ref: #symbol-toopenarraybyte]

**Input:**
- `x: openArray[char]`
- `first: int`
- `last: int`

**Output:** `openArray[byte]`
**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toOpenArrayByte

[ref: #symbol-toopenarraybyte]

**Input:**
- `x: seq[char]`
- `first: int`
- `last: int`

**Output:** `openArray[byte]`
**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toOpenArrayChar

[ref: #symbol-toopenarraychar]

**Input:**
- `x: openArray[byte]`
- `first: int`
- `last: int`

**Output:** `openArray[char]`
**Pragmas:** `magic: "Slice"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tryRecv

[ref: #symbol-tryrecv]

Tries to receive a message from the channel c, but this can fail for all sort of reasons, including contention.

**Input:**
- `c: var Channel[TMsg]`

**Output:** `tuple[dataAvailable: bool, msg: TMsg]`
**Generic parameters:** `TMsg`

**Pragmas:** `raises: []`, `gcsafe`

**Effects:** `raises: `

Tries to receive a message from the channel c, but this can fail for all sort of reasons, including contention.

If it fails, it returns (false, default(msg)) otherwise it returns (true, msg).

### trySend

[ref: #symbol-trysend]

Tries to send a message to a thread.

**Input:**
- `c: var Channel[TMsg]`
- `msg: sink TMsg`

**Output:** `bool`
**Generic parameters:** `TMsg`

**Pragmas:** `inline`, `raises: []`, `gcsafe`

**Effects:** `raises: `

Tries to send a message to a thread.

Doesn't block.

Returns false if the message was not sent because number of pending items in the channel exceeded maxItems.

### typeof

[ref: #symbol-typeof]

**Input:**
- `x: untyped`
- `mode:  = typeOfIter`
- `modifierMode:  = CompatibleTypeModifiers`

**Output:** `typedesc`
**Generic parameters:** `result:type`

**Pragmas:** `magic: "TypeOf"`, `noSideEffect`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Builtin typeof operation for accessing the type of an expression. Since version 0.20.0.

### unsafeAddr

[ref: #symbol-unsafeaddr]

**Warning:**

**Input:**
- `x: T`

**Output:** `ptr T`
**Generic parameters:** `T`

**Pragmas:** `magic: "Addr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

**Warning:**
unsafeAddr is a deprecated alias for addr, use addr instead.

### unsafeNew

[ref: #symbol-unsafenew]

Creates a new object of type T and returns a safe (traced) reference to it in a.

**Input:**
- `a: var ref T`
- `size: Natural`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "New"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new object of type T and returns a safe (traced) reference to it in a.

This is **unsafe** as it allocates an object of the passed size. This should only be used for optimization purposes when you know what you're doing!

See also:

* [new](#new,ref.T,proc(ref.T))

### unsetControlCHook

[ref: #symbol-unsetcontrolchook]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Reverts a call to setControlCHook.

### wasMoved

[ref: #symbol-wasmoved]

**Input:**
- `obj: var T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "WasMoved"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Resets an object obj to its initial (binary zero) value to signify it was "moved" and to signify its destructor should do nothing and ideally be optimized away.

### writeStackTrace

[ref: #symbol-writestacktrace]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Writes the current stack trace to stderr. This is only works for debug builds. Since it's usually used for debugging, this is proclaimed to have no IO effect!

### zeroDefault

[ref: #symbol-zerodefault]

Returns the binary zeros representation of the type T. It ignores default fields of an object.

**Input:**
- `_: typedesc[T]`

**Output:** `T`
**Generic parameters:** `T`, `_`gensym33554488:type`

**Pragmas:** `magic: "ZeroDefault"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the binary zeros representation of the type T. It ignores default fields of an object.

See also:

* [default](#default,typedesc[T])

### zeroMem

[ref: #symbol-zeromem]

Overwrites the contents of the memory at p with the value 0.

**Input:**
- `p: pointer`
- `size: Natural`

**Output:** *(none)*
**Pragmas:** `inline`, `gcsafe`, `tags: []`, `raises: []`, `enforceNoRaises`, `noSideEffect`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Overwrites the contents of the memory at p with the value 0.

Exactly size bytes will be overwritten. Like any procedure dealing with raw memory this is **unsafe**.

## Template

### `!=`

[ref: #symbol-]

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
**Pragmas:** `callsite`

Unequals operator. This is a shorthand for not (x == y).

### `&amp;=`

[ref: #symbol-amp]

Generic 'sink' operator for Nim.

**Input:**
- `x: typed`
- `y: typed`

**Output:** *(none)*
Generic 'sink' operator for Nim.

If not specialized further, an alias for add.

### `&gt;%`

[ref: #symbol-gt]

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
Treats x and y as unsigned and compares them. Returns true if unsigned(x) > unsigned(y).

### `&gt;=%`

[ref: #symbol-gt]

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
Treats x and y as unsigned and compares them. Returns true if unsigned(x) >= unsigned(y).

### `&gt;=`

[ref: #symbol-gt]

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
**Pragmas:** `callsite`

"is greater or equals" operator. This is the same as y <= x.

### `&gt;`

[ref: #symbol-gt]

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
**Pragmas:** `callsite`

"is greater" operator. This is the same as y < x.

### `..&lt;`

[ref: #symbol-lt]

A shortcut for a .. pred(b).

**Input:**
- `a: untyped`
- `b: untyped`

**Output:** `untyped`
A shortcut for a .. pred(b).

```
for i in 5 ..< 9:
  echo i # => 5; 6; 7; 8
```

### `..^`

[ref: #symbol-]

**Input:**
- `a: untyped`
- `b: untyped`

**Output:** `untyped`
A shortcut for .. ^ to avoid the common gotcha that a space between '..' and '^' is required.

### `=dispose`

[ref: #symbol-dispose]

**Input:**
- `x: owned(ref T)`

**Output:** *(none)*
**Generic parameters:** `T`

### `[]=`

[ref: #symbol-]

**Input:**
- `s: string`
- `i: int`
- `val: char`

**Output:** *(none)*
### `[]`

[ref: #symbol-]

**Input:**
- `s: string`
- `i: int`

**Output:** `char`
### `^`

[ref: #symbol-]

Builtin roof operator that can be used for convenient array access. a[^x] is a shortcut for a[a.len-x].

**Input:**
- `x: int`

**Output:** `BackwardsIndex`
Builtin roof operator that can be used for convenient array access. a[^x] is a shortcut for a[a.len-x].

```
let
  a = [1, 3, 5, 7, 9]
  b = "abcdefgh"

echo a[^1] # => 9
echo b[^2] # => g
```

### `in`

[ref: #symbol-in]

Sugar for contains.

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
**Pragmas:** `dirty`, `callsite`

Sugar for contains.

```
assert(1 in (1..3) == true)
assert(5 in (1..3) == false)
```

### `isnot`

[ref: #symbol-isnot]

Negated version of [is](#is,T,S). Equivalent to not(x is y).

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
**Pragmas:** `callsite`

Negated version of [is](#is,T,S). Equivalent to not(x is y).

```
assert 42 isnot float
assert @[1, 2] isnot enum
```

### `notin`

[ref: #symbol-notin]

Sugar for not contains.

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
**Pragmas:** `dirty`, `callsite`

Sugar for not contains.

```
assert(1 notin (1..3) == false)
assert(5 notin (1..3) == true)
```

### alloc

[ref: #symbol-alloc]

Allocates a new memory block with at least size bytes.

**Input:**
- `size: Natural`

**Output:** `pointer`
Allocates a new memory block with at least size bytes.

The block has to be freed with [realloc(block, 0)](#realloc.t,pointer,Natural) or [dealloc(block)](#dealloc,pointer). The block is not initialized, so reading from it before writing to it is undefined behaviour!

The allocated memory belongs to its allocating thread! Use [allocShared](#allocShared.t,Natural) to allocate from a shared heap.

See also:

* [alloc0](#alloc0.t,Natural)

### alloc0

[ref: #symbol-alloc0]

Allocates a new memory block with at least size bytes.

**Input:**
- `size: Natural`

**Output:** `pointer`
Allocates a new memory block with at least size bytes.

The block has to be freed with [realloc(block, 0)](#realloc.t,pointer,Natural) or [dealloc(block)](#dealloc,pointer). The block is initialized with all bytes containing zero, so it is somewhat safer than [alloc](#alloc.t,Natural).

The allocated memory belongs to its allocating thread! Use [allocShared0](#allocShared0.t,Natural) to allocate from a shared heap.

### allocShared

[ref: #symbol-allocshared]

Allocates a new memory block on the shared heap with at least size bytes.

**Input:**
- `size: Natural`

**Output:** `pointer`
Allocates a new memory block on the shared heap with at least size bytes.

The block has to be freed with [reallocShared(block, 0)](#reallocShared.t,pointer,Natural) or [deallocShared(block)](#deallocShared,pointer).

The block is not initialized, so reading from it before writing to it is undefined behaviour!

See also:

* [allocShared0](#allocShared0.t,Natural).

### allocShared0

[ref: #symbol-allocshared0]

Allocates a new memory block on the shared heap with at least size bytes.

**Input:**
- `size: Natural`

**Output:** `pointer`
Allocates a new memory block on the shared heap with at least size bytes.

The block has to be freed with [reallocShared(block, 0)](#reallocShared.t,pointer,Natural) or [deallocShared(block)](#deallocShared,pointer).

The block is initialized with all bytes containing zero, so it is somewhat safer than [allocShared](#allocShared.t,Natural).

### closureScope

[ref: #symbol-closurescope]

Useful when creating a closure in a loop to capture local loop variables by their current iteration values.

**Input:**
- `body: untyped`

**Output:** `untyped`
Useful when creating a closure in a loop to capture local loop variables by their current iteration values.

Note: This template may not work in some cases, use [capture](sugar.html#capture.m,varargs[typed],untyped) instead.

Example:

```
var myClosure : proc()
# without closureScope:
for i in 0 .. 5:
  let j = i
  if j == 3:
    myClosure = proc() = echo j
myClosure() # outputs 5. `j` is changed after closure creation
# with closureScope:
for i in 0 .. 5:
  closureScope: # Everything in this scope is locked after closure creation
    let j = i
    if j == 3:
      myClosure = proc() = echo j
myClosure() # outputs 3
```

### currentSourcePath

[ref: #symbol-currentsourcepath]

Returns the full file-system path of the current source.

**Input:**
- *(none)*

**Output:** `string`
Returns the full file-system path of the current source.

To get the directory containing the current source, use it with [ospaths2.parentDir()](ospaths2.html#parentDir%2Cstring) as currentSourcePath.parentDir().

The path returned by this template is set at compile time.

See the docstring of [macros.getProjectPath()](macros.html#getProjectPath) for an example to see the distinction between the currentSourcePath() and getProjectPath().

See also:

* [ospaths2.getCurrentDir() proc](ospaths2.html#getCurrentDir)

### disarm

[ref: #symbol-disarm]

**Input:**
- `x: typed`

**Output:** *(none)*
Useful for disarming dangling pointers explicitly for --newruntime. Regardless of whether --newruntime is used or not this sets the pointer or callback x to nil. This is an experimental API!

### dumpAllocstats

[ref: #symbol-dumpallocstats]

**Input:**
- `code: untyped`

**Output:** *(none)*
### excl

[ref: #symbol-excl]

**Input:**
- `x: var set[T]`
- `y: set[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `callsite`

Excludes the set y from the set x.

### formatErrorIndexBound

[ref: #symbol-formaterrorindexbound]

**Input:**
- `i: T`
- `a: T`
- `b: T`

**Output:** `string`
**Generic parameters:** `T`

### formatErrorIndexBound

[ref: #symbol-formaterrorindexbound]

**Input:**
- `i: T`
- `n: T`

**Output:** `string`
**Generic parameters:** `T`

### formatFieldDefect

[ref: #symbol-formatfielddefect]

**Input:**
- `f: `
- `discVal: `

**Output:** `string`
### incl

[ref: #symbol-incl]

**Input:**
- `x: var set[T]`
- `y: set[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `callsite`

Includes the set y in the set x.

### likely

[ref: #symbol-likely]

Hints the optimizer that val is likely going to be true.

**Input:**
- `val: bool`

**Output:** `bool`
Hints the optimizer that val is likely going to be true.

You can use this template to decorate a branch condition. On certain platforms this can help the processor predict better which branch is going to be run. Example:

```
for value in inputValues:
  if likely(value <= 100):
    process(value)
  else:
    echo "Value too big!"
```

On backends without branch prediction (JS and the nimscript VM), this template will not affect code execution.

### newException

[ref: #symbol-newexception]

**Input:**
- `exceptn: typedesc`
- `message: string`
- `parentException: ref Exception = nil`

**Output:** `untyped`
**Generic parameters:** `exceptn:type`

Creates an exception object of type exceptn and sets its msg field to message. Returns the new exception object.

### nimThreadProcWrapperBody

[ref: #symbol-nimthreadprocwrapperbody]

**Input:**
- `closure: untyped`

**Output:** `untyped`

[Prev](system_10.md) | [Next](system_12.md)
