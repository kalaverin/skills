---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

### dec

[ref: #symbol-dec]

Decrements the ordinal x by y.

**Input:**
- `x: var T`
- `y: V = 1`

**Output:** *(none)*
**Generic parameters:** `T`, `V`

**Pragmas:** `magic: "Dec"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Decrements the ordinal x by y.

If such a value does not exist, OverflowDefect is raised or a compile time error occurs. This is a short notation for: x = pred(x, y).

### declared

[ref: #symbol-declared]

Special compile-time procedure that checks whether x is declared. x has to be an identifier or a qualified identifier.

**Input:**
- `x: untyped`

**Output:** `bool`
**Pragmas:** `magic: "Declared"`, `noSideEffect`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Special compile-time procedure that checks whether x is declared. x has to be an identifier or a qualified identifier.

This can be used to check whether a library provides a certain feature or not:

```
when not declared(strutils.toUpper):
  # provide our own toUpper proc here, because strutils is
  # missing it.
```

See also:

* [declaredInScope](#declaredInScope,untyped)

### declaredInScope

[ref: #symbol-declaredinscope]

**Input:**
- `x: untyped`

**Output:** `bool`
**Pragmas:** `magic: "DeclaredInScope"`, `noSideEffect`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Special compile-time procedure that checks whether x is declared in the current scope. x has to be an identifier.

### deepCopy

[ref: #symbol-deepcopy]

Performs a deep copy of y and copies it into x.

**Input:**
- `x: out T`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `magic: "DeepCopy"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Performs a deep copy of y and copies it into x.

This is also used by the code generator for the implementation of spawn.

For --mm:arc or --mm:orc deepcopy support has to be enabled via --deepcopy:on.

### deepCopy

[ref: #symbol-deepcopy]

**Input:**
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

Convenience wrapper around deepCopy overload.

### default

[ref: #symbol-default]

Returns the default value of the type T. Contrary to zeroDefault, it takes default fields of an object into consideration.

**Input:**
- `_: typedesc[T]`

**Output:** `T`
**Generic parameters:** `T`, `_`gensym33556022:type`

**Pragmas:** `magic: "Default"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the default value of the type T. Contrary to zeroDefault, it takes default fields of an object into consideration.

See also:

* [zeroDefault](#zeroDefault,typedesc[T])

### defined

[ref: #symbol-defined]

Special compile-time procedure that checks whether x is defined.

**Input:**
- `x: untyped`

**Output:** `bool`
**Pragmas:** `magic: "Defined"`, `noSideEffect`, `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Special compile-time procedure that checks whether x is defined.

x is an external symbol introduced through the compiler's [-d:x switch](nimc.html#compiler-usage-compileminustime-symbols) to enable build time conditionals:

```
when not defined(release):
  # Do here programmer friendly expensive sanity checks.
# Put here the normal code
```

See also:

* [compileOption](#compileOption,string) for on|off options
* [compileOption](#compileOption,string,string) for enum options
* [define pragmas](manual.html#implementation-specific-pragmas-compileminustime-define-pragmas)

### del

[ref: #symbol-del]

Deletes the item at index i by putting x[high(x)] into position i.

**Input:**
- `x: var seq[T]`
- `i: Natural`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Deletes the item at index i by putting x[high(x)] into position i.

This is an O(1) operation.

See also:

* [delete](#delete,seq[T],Natural) for preserving the order

### delete

[ref: #symbol-delete]

Deletes the item at index i by moving all x[i+1..^1] items by one position.

**Input:**
- `x: var seq[T]`
- `i: Natural`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `systemRaisesDefect`

Deletes the item at index i by moving all x[i+1..^1] items by one position.

This is an O(n) operation.

See also:

* [del](#del,seq[T],Natural) for O(1) operation

### dispose

[ref: #symbol-dispose]

**Input:**
- `x: ForeignCell`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### echo

[ref: #symbol-echo]

Writes and flushes the parameters to the standard output.

**Input:**
- `x: varargs[typed, `$`]`

**Output:** *(none)*
**Pragmas:** `magic: "Echo"`, `gcsafe`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Writes and flushes the parameters to the standard output.

Special built-in that takes a variable number of arguments. Each argument is converted to a string via $, so it works for user-defined types that have an overloaded $ operator. It is roughly equivalent to writeLine(stdout, x); flushFile(stdout), but available for the JavaScript target too.

Unlike other IO operations this is guaranteed to be thread-safe as echo is very often used for debugging convenience. If you want to use echo inside a [proc without side effects](manual.html#pragmas-nosideeffect-pragma) you can use [debugEcho](#debugEcho,varargs[typed,]) instead.

### ensureMove

[ref: #symbol-ensuremove]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `magic: "EnsureMove"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Ensures that x is moved to the new location, otherwise it gives an error at the compile time.

### equalMem

[ref: #symbol-equalmem]

Compares the memory blocks a and b. size bytes will be compared.

**Input:**
- `a: pointer`
- `b: pointer`
- `size: Natural`

**Output:** `bool`
**Pragmas:** `inline`, `gcsafe`, `tags: []`, `raises: []`, `enforceNoRaises`, `noSideEffect`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Compares the memory blocks a and b. size bytes will be compared.

If the blocks are equal, true is returned, false otherwise. Like any procedure dealing with raw memory this is **unsafe**.

### excl

[ref: #symbol-excl]

Excludes element y from the set x.

**Input:**
- `x: var set[T]`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `magic: "Excl"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Excludes element y from the set x.

This is the same as x = x - {y}, but it might be more efficient.

### find

[ref: #symbol-find]

**Input:**
- `a: T`
- `item: S`

**Output:** `int`
**Generic parameters:** `T`, `S`

**Pragmas:** `inline`

Returns the first index of item in a or -1 if not found. This requires appropriate items and == operations to work.

### finished

[ref: #symbol-finished]

**Input:**
- `x: T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`, `inline`, `magic: "Finished"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

It can be used to determine if a first class iterator has finished.

### freeShared

[ref: #symbol-freeshared]

Frees the memory allocated with createShared, createSharedU or resizeShared.

**Input:**
- `p: ptr T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `gcsafe`, `raises: []`

**Effects:** `raises: `

Frees the memory allocated with createShared, createSharedU or resizeShared.

**This procedure is dangerous!** If one forgets to free the memory a leak occurs; if one tries to access freed memory (or just freeing it twice!) a core dump may happen or other memory may be corrupted.

### GC_disableMarkAndSweep

[ref: #symbol-gc-disablemarkandsweep]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

For --mm:orc an alias for GC\_disableOrc.

### GC_disableOrc

[ref: #symbol-gc-disableorc]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Disables the cycle collector subsystem of --mm:orc. This is a --mm:orc specific API. Check with when defined(gcOrc) for its existence.

### GC_enableMarkAndSweep

[ref: #symbol-gc-enablemarkandsweep]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

For --mm:orc an alias for GC\_enableOrc.

### GC_enableOrc

[ref: #symbol-gc-enableorc]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Enables the cycle collector subsystem of --mm:orc. This is a --mm:orc specific API. Check with when defined(gcOrc) for its existence.

### GC_fullCollect

[ref: #symbol-gc-fullcollect]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Forces a full garbage collection pass. With --mm:orc triggers the cycle collector. This is an alias for GC\_runOrc.

### GC_getStatistics

[ref: #symbol-gc-getstatistics]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### GC_partialCollect

[ref: #symbol-gc-partialcollect]

**Input:**
- `limit: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

### GC_prepareOrc

[ref: #symbol-gc-prepareorc]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### GC_ref

[ref: #symbol-gc-ref]

**Input:**
- `x: ref T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `raises: []`

**Effects:** `raises: `

New runtime only supports this operation for 'ref T'.

### GC_runOrc

[ref: #symbol-gc-runorc]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Forces a cycle collection pass.

### GC_unref

[ref: #symbol-gc-unref]

**Input:**
- `x: ref T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `raises: []`

**Effects:** `raises: `

New runtime only supports this operation for 'ref T'.

### getAllocStats

[ref: #symbol-getallocstats]

**Input:**
- *(none)*

**Output:** `AllocStats`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getCurrentException

[ref: #symbol-getcurrentexception]

**Input:**
- *(none)*

**Output:** `ref Exception`
**Pragmas:** `compilerproc`, `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the current exception; if there is none, nil is returned.

### getCurrentExceptionMsg

[ref: #symbol-getcurrentexceptionmsg]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the error message that was attached to the current exception; if there is none, "" is returned.

### getFrame

[ref: #symbol-getframe]

**Input:**
- *(none)*

**Output:** `PFrame`
**Pragmas:** `compilerproc`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getFrameState

[ref: #symbol-getframestate]

**Input:**
- *(none)*

**Output:** `FrameState`
**Pragmas:** `compilerproc`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getFreeMem

[ref: #symbol-getfreemem]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of bytes that are owned by the process, but do not hold any meaningful data.

### getFreeSharedMem

[ref: #symbol-getfreesharedmem]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of bytes that are owned by the process on the shared heap, but do not hold any meaningful data. This is only available when threads are enabled.

### getMaxMem

[ref: #symbol-getmaxmem]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getOccupiedMem

[ref: #symbol-getoccupiedmem]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of bytes that are owned by the process and hold data.

### getOccupiedSharedMem

[ref: #symbol-getoccupiedsharedmem]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of bytes that are owned by the process on the shared heap and hold data. This is only available when threads are enabled.

### getStackTrace

[ref: #symbol-getstacktrace]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the current stack trace. This only works for debug builds.

### getStackTrace

[ref: #symbol-getstacktrace]

**Input:**
- `e: ref Exception`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the stack trace associated with e, which is the stack that lead to the raise statement. This only works for debug builds.

### getStackTraceEntries

[ref: #symbol-getstacktraceentries]

**Input:**
- `e: ref Exception`

**Output:** `lent seq[StackTraceEntry]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getStackTraceEntries

[ref: #symbol-getstacktraceentries]

**Input:**
- *(none)*

**Output:** `seq[StackTraceEntry]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the stack trace entries for the current stack trace. This is not yet available for the JS backend.

### getThreadId

[ref: #symbol-getthreadid]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `raises: []`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the ID of the currently running thread.

### getTotalMem

[ref: #symbol-gettotalmem]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of bytes that are owned by the process.

### getTotalSharedMem

[ref: #symbol-gettotalsharedmem]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of bytes on the shared heap that are owned by the process. This is only available when threads are enabled.

### getTypeInfo

[ref: #symbol-gettypeinfo]

Get type information for x.

**Input:**
- `x: T`

**Output:** `pointer`
**Generic parameters:** `T`

**Pragmas:** `magic: "GetTypeInfo"`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get type information for x.

Ordinary code should not use this, but the [typeinfo module](typeinfo.html) instead.

### gorge

[ref: #symbol-gorge]

**Input:**
- `command: string`
- `input:  = ""`
- `cache:  = ""`

**Output:** `string`
**Pragmas:** `magic: "StaticExec"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This is an alias for [staticExec](#staticExec,string,string,string).

### gorgeEx

[ref: #symbol-gorgeex]

**Input:**
- `command: string`
- `input:  = ""`
- `cache:  = ""`

**Output:** `tuple[output: string, exitCode: int]`
**Pragmas:** `noinit`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Similar to [gorge](#gorge,string,string,string) but also returns the precious exit code.

### grow

[ref: #symbol-grow]

**Input:**
- `x: var seq[T]`
- `newLen: Natural`
- `value: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `nodestroy`

### high

[ref: #symbol-high]

Returns the highest possible value of an ordinal value x.

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `magic: "High"`, `noSideEffect`, `deprecated: "Deprecated since v1.4; there should not be `high(value)`. Use `high(type)`."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the highest possible value of an ordinal value x.

As a special semantic rule, x may also be a type identifier.

**This proc is deprecated**, use this one instead:

* [high(typedesc)](#high,typedesc[T])

```
high(2) # => 9223372036854775807
```

### high

[ref: #symbol-high]

Returns the highest possible value of an ordinal or enum type.

**Input:**
- `x: typedesc[T]`

**Output:** `T`
**Generic parameters:** `T`, `x:type`

**Pragmas:** `magic: "High"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the highest possible value of an ordinal or enum type.

high(int) is Nim's way of writing INT\_MAX or MAX\_INT.

```
high(int) # => 9223372036854775807
```

See also:

* [low(typedesc)](#low,typedesc[T])

### high

[ref: #symbol-high]

Returns the highest possible index of a sequence x.

**Input:**
- `x: openArray[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `magic: "High"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the highest possible index of a sequence x.

```
var s = @[1, 2, 3, 4, 5, 6, 7]
high(s) # => 6
for i in low(s)..high(s):
  echo s[i]
```

See also:

* [low(openArray)](#low,openArray[T])

### high

[ref: #symbol-high]

Returns the highest possible index of an array x.

**Input:**
- `x: array[I, T]`

**Output:** `I`
**Generic parameters:** `I`, `T`

**Pragmas:** `magic: "High"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the highest possible index of an array x.

For empty arrays, the return type is int.

```
var arr = [1, 2, 3, 4, 5, 6, 7]
high(arr) # => 6
for i in low(arr)..high(arr):
  echo arr[i]
```

See also:

* [low(array)](#low,array[I,T])

### high

[ref: #symbol-high]

Returns the highest possible index of an array type.

**Input:**
- `x: typedesc[array[I, T]]`

**Output:** `I`
**Generic parameters:** `I`, `T`, `x:type`

**Pragmas:** `magic: "High"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the highest possible index of an array type.

For empty arrays, the return type is int.

```
high(array[7, int]) # => 6
```

See also:

* [low(typedesc[array])](#low,typedesc[array[I,T]])

### high

[ref: #symbol-high]

Returns the highest possible index of a compatible string x. This is sometimes an O(n) operation.

**Input:**
- `x: cstring`

**Output:** `int`
**Pragmas:** `magic: "High"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the highest possible index of a compatible string x. This is sometimes an O(n) operation.

See also:

* [low(cstring)](#low,cstring)

### high

[ref: #symbol-high]

Returns the highest possible index of a string x.

**Input:**
- `x: string`

**Output:** `int`
**Pragmas:** `magic: "High"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the highest possible index of a string x.

```
var str = "Hello world!"
high(str) # => 11
```

See also:

* [low(string)](#low,string)

### high

[ref: #symbol-high]

**Input:**
- `T: typedesc[SomeFloat]`

**Output:** `T:type`
**Generic parameters:** `T:type`


[Prev](system_7.md) | [Next](system_9.md)
