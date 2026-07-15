---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

### offsetOf

[ref: #symbol-offsetof]

**Input:**
- `t: typedesc[T]`
- `member: untyped`

**Output:** `int`
**Generic parameters:** `T`, `t:type`

### offsetOf

[ref: #symbol-offsetof]

**Input:**
- `value: T`
- `member: untyped`

**Output:** `int`
**Generic parameters:** `T`

### once

[ref: #symbol-once]

Executes a block of code only once (the first time the block is reached).

**Input:**
- `body: untyped`

**Output:** `untyped`
Executes a block of code only once (the first time the block is reached).

```
proc draw(t: Triangle) =
  once:
    graphicsInit()
  line(t.p1, t.p2)
  line(t.p2, t.p3)
  line(t.p3, t.p1)
```

### rangeCheck

[ref: #symbol-rangecheck]

**Input:**
- `cond: `

**Output:** *(none)*
Helper for performing user-defined range checks. Such checks will be performed only when the rangechecks compile-time option is enabled.

### realloc

[ref: #symbol-realloc]

Grows or shrinks a given memory block.

**Input:**
- `p: pointer`
- `newSize: Natural`

**Output:** `pointer`
Grows or shrinks a given memory block.

If p is **nil** then a new memory block is returned. In either way the block has at least newSize bytes. If newSize == 0 and p is not **nil** realloc calls dealloc(p). In other cases the block has to be freed with [dealloc(block)](#dealloc,pointer).

The allocated memory belongs to its allocating thread! Use [reallocShared](#reallocShared.t,pointer,Natural) to reallocate from a shared heap.

### realloc0

[ref: #symbol-realloc0]

Grows or shrinks a given memory block.

**Input:**
- `p: pointer`
- `oldSize: Natural`
- `newSize: Natural`

**Output:** `pointer`
Grows or shrinks a given memory block.

If p is **nil** then a new memory block is returned. In either way the block has at least newSize bytes. If newSize == 0 and p is not **nil** realloc calls dealloc(p). In other cases the block has to be freed with [dealloc(block)](#dealloc,pointer).

The block is initialized with all bytes containing zero, so it is somewhat safer then realloc

The allocated memory belongs to its allocating thread! Use [reallocShared](#reallocShared.t,pointer,Natural) to reallocate from a shared heap.

### reallocShared

[ref: #symbol-reallocshared]

Grows or shrinks a given memory block on the heap.

**Input:**
- `p: pointer`
- `newSize: Natural`

**Output:** `pointer`
Grows or shrinks a given memory block on the heap.

If p is **nil** then a new memory block is returned. In either way the block has at least newSize bytes. If newSize == 0 and p is not **nil** reallocShared calls deallocShared(p). In other cases the block has to be freed with [deallocShared](#deallocShared,pointer).

### reallocShared0

[ref: #symbol-reallocshared0]

Grows or shrinks a given memory block on the heap.

**Input:**
- `p: pointer`
- `oldSize: Natural`
- `newSize: Natural`

**Output:** `pointer`
Grows or shrinks a given memory block on the heap.

When growing, the new bytes of the block is initialized with all bytes containing zero, so it is somewhat safer then reallocShared

If p is **nil** then a new memory block is returned. In either way the block has at least newSize bytes. If newSize == 0 and p is not **nil** reallocShared calls deallocShared(p). In other cases the block has to be freed with [deallocShared](#deallocShared,pointer).

### setupForeignThreadGc

[ref: #symbol-setupforeignthreadgc]

**Input:**
- *(none)*

**Output:** *(none)*
With --mm:arc a nop.

### tearDownForeignThreadGc

[ref: #symbol-teardownforeignthreadgc]

**Input:**
- *(none)*

**Output:** *(none)*
With --mm:arc a nop.

### unlikely

[ref: #symbol-unlikely]

Hints the optimizer that val is likely going to be false.

**Input:**
- `val: bool`

**Output:** `bool`
Hints the optimizer that val is likely going to be false.

You can use this proc to decorate a branch condition. On certain platforms this can help the processor predict better which branch is going to be run. Example:

```
for value in inputValues:
  if unlikely(value > 100):
    echo "Value too big!"
  else:
    process(value)
```

On backends without branch prediction (JS and the nimscript VM), this template will not affect code execution.

### unown

[ref: #symbol-unown]

**Input:**
- `x: typed`

**Output:** `untyped`
## Type

### `ptr`

[ref: #symbol-ptr]

```nim
ptr[T] {.magic: Pointer.}
```

Built-in generic untraced pointer type.

### `ref`

[ref: #symbol-ref]

```nim
ref[T] {.magic: Pointer.}
```

Built-in generic traced pointer type.

### `static`

[ref: #symbol-static]

Meta type representing all values that can be evaluated at compile-time.

```nim
static[T] {.magic: "Static".}
```

Meta type representing all values that can be evaluated at compile-time.

The type coercion static(x) can be used to force the compile-time evaluation of the given expression x.

### `type`

[ref: #symbol-type]

Meta type representing the type of all type values.

```nim
type[T] {.magic: "Type".}
```

Meta type representing the type of all type values.

The coercion type(x) can be used to obtain the type of the given expression x.

### AllocStats

[ref: #symbol-allocstats]

```nim
AllocStats = object
```

### any

[ref: #symbol-any]

```nim
any {.deprecated: "Deprecated since v1.5; Use auto instead.".} = distinct auto
```

Deprecated; Use auto instead. See <https://github.com/nim-lang/RFCs/issues/281>

### array

[ref: #symbol-array]

```nim
array[I; T] {.magic: "Array".}
```

Generic type to construct fixed-length arrays.

### auto

[ref: #symbol-auto]

```nim
auto {.magic: Expr.}
```

Meta type for automatic type determination.

### BackwardsIndex

[ref: #symbol-backwardsindex]

```nim
BackwardsIndex = distinct int
```

Type that is constructed by ^ for reversed array accesses. (See [^ template](#^.t,int))

### bool

[ref: #symbol-bool]

```nim
bool {.magic: "Bool".} = enum
  false = 0, true = 1
```

Built-in boolean type.

### byte

[ref: #symbol-byte]

```nim
byte = uint8
```

This is an alias for uint8, that is an unsigned integer, 8 bits wide.

### CatchableError

[ref: #symbol-catchableerror]

```nim
CatchableError = object of Exception
```

Abstract class for all exceptions that are catchable.

### Channel

[ref: #symbol-channel]

```nim
Channel[TMsg] {.gcsafe.} = RawChannel
```

a channel for thread communication

### char

[ref: #symbol-char]

```nim
char {.magic: Char.}
```

Built-in 8 bit character type (unsigned).

### csize

[ref: #symbol-csize]

```nim
csize {.importc: "size_t", nodecl, deprecated: "use `csize_t` instead".} = int
```

This isn't the same as size\_t in *C*. Don't use it.

### cstring

[ref: #symbol-cstring]

```nim
cstring {.magic: Cstring.}
```

Built-in cstring (*compatible string*) type.

### Defect

[ref: #symbol-defect]

```nim
Defect = object of Exception
```

Abstract base class for all exceptions that Nim's runtime raises but that are strictly uncatchable as they can also be mapped to a quit / trap / exit operation.

### Endianness

[ref: #symbol-endianness]

```nim
Endianness = enum
  littleEndian, bigEndian
```

Type describing the endianness of a processor.

### Exception

[ref: #symbol-exception]

Base exception class.

```nim
Exception {.compilerproc, magic: "Exception".} = object of RootObj
  parent*: ref Exception     ## Parent exception (can be used as a stack).
  name*: cstring             ## The exception's name is its Nim identifier.
                             ## This field is filled automatically in the
                             ## `raise` statement.
  msg* {.exportc: "message".}: string ## The exception's message. Not
                                      ## providing an exception message
                                      ## is bad style.
  when defined(js):
    trace*: string
  else:
    trace*: seq[StackTraceEntry]
```

Base exception class.

Each exception has to inherit from Exception. See the full [exception hierarchy](manual.html#exception-handling-exception-hierarchy).

### float

[ref: #symbol-float]

```nim
float {.magic: Float.}
```

Default floating point type.

### float32

[ref: #symbol-float32]

```nim
float32 {.magic: Float32.}
```

32 bit floating point type.

### float64

[ref: #symbol-float64]

```nim
float64 {.magic: Float.}
```

64 bit floating point type.

### ForeignCell

[ref: #symbol-foreigncell]

```nim
ForeignCell = object
  data*: pointer
```

### ForLoopStmt

[ref: #symbol-forloopstmt]

```nim
ForLoopStmt {.compilerproc.} = object
```

A special type that marks a macro as a for-loop macro. See ["For Loop Macro"](manual.html#macros-for-loop-macro).

### GC_Strategy

[ref: #symbol-gc-strategy]

```nim
GC_Strategy = enum
  gcThroughput,             ## optimize for throughput
  gcResponsiveness,         ## optimize for responsiveness (default)
  gcOptimizeTime,           ## optimize for speed
  gcOptimizeSpace            ## optimize for memory footprint
```

The strategy the GC should use for the application.

### HSlice

[ref: #symbol-hslice]

```nim
HSlice[T; U] = object
  a*: T                      ## The lower bound (inclusive).
  b*: U                      ## The upper bound (inclusive).
```

"Heterogeneous" slice type.

### int

[ref: #symbol-int]

```nim
int {.magic: Int.}
```

Default integer type; bitwidth depends on architecture, but is always the same as a pointer.

### int16

[ref: #symbol-int16]

```nim
int16 {.magic: Int16.}
```

Signed 16 bit integer type.

### int32

[ref: #symbol-int32]

```nim
int32 {.magic: Int32.}
```

Signed 32 bit integer type.

### int64

[ref: #symbol-int64]

```nim
int64 {.magic: Int64.}
```

Signed 64 bit integer type.

### int8

[ref: #symbol-int8]

```nim
int8 {.magic: Int8.}
```

Signed 8 bit integer type.

### iterable

[ref: #symbol-iterable]

```nim
iterable[T] {.magic: IterableType.}
```

Represents an expression that yields T

### JsRoot

[ref: #symbol-jsroot]

```nim
JsRoot = ref object of RootObj
```

Root type of the JavaScript object hierarchy

### lent

[ref: #symbol-lent]

```nim
lent[T] {.magic: "BuiltinType".}
```

### Natural

[ref: #symbol-natural]

```nim
Natural = range[0 .. high(int)]
```

is an int type ranging from zero to the maximum value of an int. This type is often useful for documentation and debugging.

### NimNode

[ref: #symbol-nimnode]

```nim
NimNode {.magic: "PNimrodNode".} = ref NimNodeObj
```

Represents a Nim AST node. Macros operate on this type.

### NimSeqV2

[ref: #symbol-nimseqv2]

```nim
NimSeqV2[T] = object
```

### openArray

[ref: #symbol-openarray]

```nim
openArray[T] {.magic: "OpenArray".}
```

Generic type to construct open arrays. Open arrays are implemented as a pointer to the array data and a length field.

### Ordinal

[ref: #symbol-ordinal]

```nim
Ordinal[T] {.magic: Ordinal.}
```

Generic ordinal type. Includes integer, bool, character, and enumeration types as well as their subtypes. See also SomeOrdinal.

### owned

[ref: #symbol-owned]

```nim
owned[T] {.magic: "BuiltinType".}
```

type constructor to mark a ref/ptr or a closure as owned.

### PFrame

[ref: #symbol-pframe]

```nim
PFrame = ptr TFrame
```

Represents a runtime frame of the call stack; part of the debugger API.

### pointer

[ref: #symbol-pointer]

```nim
pointer {.magic: Pointer.}
```

Built-in pointer type, use the addr operator to get a pointer to a variable.

### Positive

[ref: #symbol-positive]

```nim
Positive = range[1 .. high(int)]
```

is an int type ranging from one to the maximum value of an int. This type is often useful for documentation and debugging.

### range

[ref: #symbol-range]

```nim
range[T] {.magic: "Range".}
```

Generic type to construct range types.

### RootEffect

[ref: #symbol-rooteffect]

Base effect class.

```nim
RootEffect {.compilerproc.} = object of RootObj
```

Base effect class.

Each effect should inherit from RootEffect unless you know what you're doing.

### RootObj

[ref: #symbol-rootobj]

The root of Nim's object hierarchy.

```nim
RootObj {.compilerproc, inheritable.} = object
```

The root of Nim's object hierarchy.

Objects should inherit from RootObj or one of its descendants. However, objects that have no ancestor are also allowed.

### RootRef

[ref: #symbol-rootref]

```nim
RootRef = ref RootObj
```

Reference to RootObj.

### seq

[ref: #symbol-seq]

```nim
seq[T] {.magic: "Seq".}
```

Generic type to construct sequences.

### set

[ref: #symbol-set]

```nim
set[T] {.magic: "Set".}
```

Generic type to construct bit sets.

### sink

[ref: #symbol-sink]

```nim
sink[T] {.magic: "BuiltinType".}
```

### Slice

[ref: #symbol-slice]

```nim
Slice[T] = HSlice[T, T]
```

An alias for HSlice[T, T].

### SomeFloat

[ref: #symbol-somefloat]

```nim
SomeFloat = float | float32 | float64
```

Type class matching all floating point number types.

### SomeInteger

[ref: #symbol-someinteger]

```nim
SomeInteger = SomeSignedInt | SomeUnsignedInt
```

Type class matching all integer types.

### SomeNumber

[ref: #symbol-somenumber]

```nim
SomeNumber = SomeInteger | SomeFloat
```

Type class matching all number types.

### SomeOrdinal

[ref: #symbol-someordinal]

```nim
SomeOrdinal = int | int8 | int16 | int32 | int64 | bool | enum | uint | uint8 |
    uint16 |
    uint32 |
    uint64
```

Type class matching all ordinal types; however this includes enums with holes. See also Ordinal

### SomeSignedInt

[ref: #symbol-somesignedint]

```nim
SomeSignedInt = int | int8 | int16 | int32 | int64
```

Type class matching all signed integer types.

### SomeUnsignedInt

[ref: #symbol-someunsignedint]

```nim
SomeUnsignedInt = uint | uint8 | uint16 | uint32 | uint64
```

Type class matching all unsigned integer types.

### StackTraceEntry

[ref: #symbol-stacktraceentry]

```nim
StackTraceEntry = object
  procname*: cstring         ## Name of the proc that is currently executing.
  line*: int                 ## Line number of the proc that is currently executing.
  filename*: cstring         ## Filename of the proc that is currently executing.
  when NimStackTraceMsgs:
    frameMsg*: string ## When a stacktrace is generated in a given frame and
                      ## rendered at a later time, we should ensure the stacktrace
                      ## data isn't invalidated; any pointer into PFrame is
                      ## subject to being invalidated so shouldn't be stored.
  when defined(nimStackTraceOverride):
    programCounter*: uint ## Program counter - will be used to get the rest of the info,
                          ## when `$` is called on this type. We can't use
                          ## "cuintptr_t" in here.
    procnameStr*, filenameStr*: string ## GC-ed alternatives to "procname" and "filename"
```

In debug mode exceptions store the stack trace that led to them. A StackTraceEntry is a single entry of the stack trace.

### string

[ref: #symbol-string]

```nim
string {.magic: String.}
```

Built-in string type.

### TaintedString

[ref: #symbol-taintedstring]

```nim
TaintedString {.deprecated: "Deprecated since 1.5".} = string
```

### TFrame

[ref: #symbol-tframe]

```nim
TFrame {.importc, nodecl, final.} = object
  prev*: PFrame              ## Previous frame; used for chaining the call stack.
  procname*: cstring         ## Name of the proc that is currently executing.
  line*: int                 ## Line number of the proc that is currently executing.
  filename*: cstring         ## Filename of the proc that is currently executing.
  len*: int16                ## Length of the inspectable slots.
  calldepth*: int16          ## Used for max call depth checking.
  when NimStackTraceMsgs:
    frameMsgLen*: int        ## end position in frameMsgBuf for this frame.
```

The frame itself.

### typed

[ref: #symbol-typed]

```nim
typed {.magic: Stmt.}
```

Meta type to denote an expression that is resolved (for templates).

### typedesc

[ref: #symbol-typedesc]

```nim
typedesc {.magic: TypeDesc.}
```

Meta type to denote a type description.

### TypeOfMode

[ref: #symbol-typeofmode]

```nim
TypeOfMode = enum
  typeOfProc,               ## Prefer the interpretation that means `x` is a proc call.
  typeOfIter                 ## Prefer the interpretation that means `x` is an iterator call.
```

Possible modes of typeof.

### TypeOfModifiers

[ref: #symbol-typeofmodifiers]

```nim
TypeOfModifiers = enum
  CompatibleTypeModifiers,  ## Remove or keep type modifiers in the same way as old typeof. That means keep `sink` but remove `var` and `lent`.
  RemoveTypeModifiers,      ## Remove type modifiers.
  KeepTypeModifiers          ## Keep type modifiers.
```

Modes to handle type modifiers var, sink and lent.

### uint

[ref: #symbol-uint]

```nim
uint {.magic: UInt.}
```

Unsigned default integer type.

### uint16

[ref: #symbol-uint16]

```nim
uint16 {.magic: UInt16.}
```

Unsigned 16 bit integer type.

### uint32

[ref: #symbol-uint32]

```nim
uint32 {.magic: UInt32.}
```

Unsigned 32 bit integer type.

### uint64

[ref: #symbol-uint64]

```nim
uint64 {.magic: UInt64.}
```

Unsigned 64 bit integer type.

### uint8

[ref: #symbol-uint8]

```nim
uint8 {.magic: UInt8.}
```

Unsigned 8 bit integer type.

### UncheckedArray

[ref: #symbol-uncheckedarray]

```nim
UncheckedArray[T] {.magic: "UncheckedArray".}
```

### untyped

[ref: #symbol-untyped]

```nim
untyped {.magic: Expr.}
```

Meta type to denote an expression that is not resolved (for templates).

### varargs

[ref: #symbol-varargs]

```nim
varargs[T] {.magic: "Varargs".}
```

Generic type to construct a varargs type.

### void

[ref: #symbol-void]

```nim
void {.magic: "VoidType".}
```

Meta type to denote the absence of any type.

## Var

### errorMessageWriter

[ref: #symbol-errormessagewriter]

```nim
errorMessageWriter: (proc (msg: string) {.tags: [WriteIOEffect], gcsafe,
    nimcall, raises: [].})
```

Function that will be called instead of stdmsg.write when printing stacktrace. Unstable API.


[Prev](system_11.md) | [Next](system_13.md)
