---
source_hash: cb4ccbba274e9de8
source_path: lib/system.nim
---

## Const

### appType

[ref: #symbol-apptype]

```nim
appType {.magic: "AppType".}: string = ""
```

A string that describes the application type. Possible values: "console", "gui", "lib".

### CompileDate

[ref: #symbol-compiledate]

```nim
CompileDate {.magic: "CompileDate".}: string = "0000-00-00"
```

The date (in UTC) of compilation as a string of the form YYYY-MM-DD. This works thanks to compiler magic.

### CompileTime

[ref: #symbol-compiletime]

```nim
CompileTime {.magic: "CompileTime".}: string = "00:00:00"
```

The time (in UTC) of compilation as a string of the form HH:MM:SS. This works thanks to compiler magic.

### cpuEndian

[ref: #symbol-cpuendian]

```nim
cpuEndian {.magic: "CpuEndian".}: Endianness = littleEndian
```

The endianness of the target CPU. This is a valuable piece of information for low-level code only. This works thanks to compiler magic.

### hostCPU

[ref: #symbol-hostcpu]

A string that describes the host CPU.

```nim
hostCPU {.magic: "HostCPU".}: string = ""
```

A string that describes the host CPU.

Possible values: "i386", "alpha", "powerpc", "powerpc64", "powerpc64el", "sparc", "amd64", "mips", "mipsel", "arm", "arm64", "mips64", "mips64el", "riscv32", "riscv64", "loongarch64", "s390x".

### hostOS

[ref: #symbol-hostos]

A string that describes the host operating system.

```nim
hostOS {.magic: "HostOS".}: string = ""
```

A string that describes the host operating system.

Possible values: "windows", "macosx", "linux", "netbsd", "freebsd", "openbsd", "solaris", "aix", "haiku", "standalone".

### Inf

[ref: #symbol-inf]

```nim
Inf = 0x7FF0000000000000'f64
```

Contains the IEEE floating point value of positive infinity.

### isMainModule

[ref: #symbol-ismainmodule]

```nim
isMainModule {.magic: "IsMainModule".}: bool = false
```

True only when accessed in the main module. This works thanks to compiler magic. It is useful to embed testing code in a module.

### NaN

[ref: #symbol-nan]

Contains an IEEE floating point value of *Not A Number*.

```nim
NaN = 0x7FF7FFFFFFFFFFFF'f64
```

Contains an IEEE floating point value of *Not A Number*.

Note that you cannot compare a floating point value to this value and expect a reasonable result - use the isNaN or classify procedure in the [math module](math.html) for checking for NaN.

### NegInf

[ref: #symbol-neginf]

```nim
NegInf = 0xFFF0000000000000'f64
```

Contains the IEEE floating point value of negative infinity.

### NimMajor

[ref: #symbol-nimmajor]

is the major number of Nim's version. Example:

```nim
NimMajor {.intdefine.}: int = 2
```

is the major number of Nim's version. Example:

```
when (NimMajor, NimMinor, NimPatch) >= (1, 3, 1): discard
```

### NimMinor

[ref: #symbol-nimminor]

```nim
NimMinor {.intdefine.}: int = 2
```

is the minor number of Nim's version. Odd for devel, even for releases.

### NimPatch

[ref: #symbol-nimpatch]

```nim
NimPatch {.intdefine.}: int = 11
```

is the patch number of Nim's version. Odd for devel, even for releases.

### NimVersion

[ref: #symbol-nimversion]

```nim
NimVersion: string = "2.2.11"
```

is the version of Nim as a string.

### off

[ref: #symbol-off]

```nim
off = false
```

Alias for false.

### on

[ref: #symbol-on]

```nim
on = true
```

Alias for true.

### QuitFailure

[ref: #symbol-quitfailure]

```nim
QuitFailure = 1
```

is the value that should be passed to [quit](#quit,int) to indicate failure.

### QuitSuccess

[ref: #symbol-quitsuccess]

```nim
QuitSuccess = 0
```

is the value that should be passed to [quit](#quit,int) to indicate success.

## Iterator

### `..&lt;`

[ref: #symbol-lt]

**Input:**
- `a: T`
- `b: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

### `..&lt;`

[ref: #symbol-lt]

**Input:**
- `a: int64`
- `b: int64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of ..< for convenience so that mixing integer types works better.

### `..&lt;`

[ref: #symbol-lt]

**Input:**
- `a: int32`
- `b: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of ..< for convenience so that mixing integer types works better.

### `..&lt;`

[ref: #symbol-lt]

**Input:**
- `a: uint64`
- `b: uint64`

**Output:** `uint64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of ..< for convenience so that mixing integer types works better.

### `..&lt;`

[ref: #symbol-lt]

**Input:**
- `a: uint32`
- `b: uint32`

**Output:** `uint32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of ..< for convenience so that mixing integer types works better.

### `..`

[ref: #symbol-]

An alias for countup(a, b, 1).

**Input:**
- `a: T`
- `b: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

An alias for countup(a, b, 1).

See also:

* [..<](#..<.i,T,T)

### `..`

[ref: #symbol-]

A type specialized version of .. for convenience so that mixing integer types works better.

**Input:**
- `a: int64`
- `b: int64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of .. for convenience so that mixing integer types works better.

See also:

* [..<](#..<.i,T,T)

### `..`

[ref: #symbol-]

A type specialized version of .. for convenience so that mixing integer types works better.

**Input:**
- `a: int32`
- `b: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of .. for convenience so that mixing integer types works better.

See also:

* [..<](#..<.i,T,T)

### `..`

[ref: #symbol-]

A type specialized version of .. for convenience so that mixing integer types works better.

**Input:**
- `a: uint64`
- `b: uint64`

**Output:** `uint64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of .. for convenience so that mixing integer types works better.

See also:

* [..<](#..<.i,T,T)

### `..`

[ref: #symbol-]

A type specialized version of .. for convenience so that mixing integer types works better.

**Input:**
- `a: uint32`
- `b: uint32`

**Output:** `uint32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of .. for convenience so that mixing integer types works better.

See also:

* [..<](#..<.i,T,T)

### `||`

[ref: #symbol-]

OpenMP parallel loop iterator. Same as .. but the loop may run in parallel.

**Input:**
- `a: S`
- `b: T`
- `annotation: static string = "parallel for"`

**Output:** `T`
**Generic parameters:** `S`, `T`, `annotation:type`

**Pragmas:** `inline`, `magic: "OmpParFor"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

OpenMP parallel loop iterator. Same as .. but the loop may run in parallel.

annotation is an additional annotation for the code generator to use. The default annotation is parallel for. Please refer to the [OpenMP Syntax Reference](https://www.openmp.org/wp-content/uploads/OpenMP-4.5-1115-CPP-web.pdf) for further information.

Note that the compiler maps that to the #pragma omp parallel for construct of OpenMP and as such isn't aware of the parallelism in your code! Be careful! Later versions of || will get proper support by Nim's code generator and GC.

### `||`

[ref: #symbol-]

OpenMP parallel loop iterator with stepping.  Same as countup but the loop may run in parallel.

**Input:**
- `a: S`
- `b: T`
- `step: Positive`
- `annotation: static string = "parallel for"`

**Output:** `T`
**Generic parameters:** `S`, `T`, `annotation:type`

**Pragmas:** `inline`, `magic: "OmpParFor"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

OpenMP parallel loop iterator with stepping.  Same as countup but the loop may run in parallel.

annotation is an additional annotation for the code generator to use. The default annotation is parallel for. Please refer to the [OpenMP Syntax Reference](https://www.openmp.org/wp-content/uploads/OpenMP-4.5-1115-CPP-web.pdf) for further information.

Note that the compiler maps that to the #pragma omp parallel for construct of OpenMP and as such isn't aware of the parallelism in your code! Be careful! Later versions of || will get proper support by Nim's code generator and GC.

### countdown

[ref: #symbol-countdown]

Counts from ordinal value a down to b (inclusive) with the given step count.

**Input:**
- `a: T`
- `b: T`
- `step: Positive = 1`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Counts from ordinal value a down to b (inclusive) with the given step count.

T may be any ordinal type, step may only be positive.

**Note**: This fails to count to low(int) if T = int for efficiency reasons.

### countup

[ref: #symbol-countup]

Counts from ordinal value a to b (inclusive) with the given step count.

**Input:**
- `a: T`
- `b: T`
- `step: Positive = 1`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Counts from ordinal value a to b (inclusive) with the given step count.

T may be any ordinal type, step may only be positive.

**Note**: This fails to count to high(int) if T = int for efficiency reasons.

## Let

### nimvm

[ref: #symbol-nimvm]

```nim
nimvm {.magic: "Nimvm", compileTime.}: bool = false
```

May be used only in when expression. It is true in Nim VM context and false otherwise.

## Macro

### varargsLen

[ref: #symbol-varargslen]

**Input:**
- `x: varargs[untyped]`

**Output:** `int`
returns number of variadic arguments in x

## Proc

### `%%`

[ref: #symbol-]

Treats x and y as unsigned and compute the modulo of x and y.

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Treats x and y as unsigned and compute the modulo of x and y.

The result is truncated to fit into the result. This implements modulo arithmetic. No overflow errors are possible.

### `%%`

[ref: #symbol-]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `%%`

[ref: #symbol-]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `%%`

[ref: #symbol-]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `%%`

[ref: #symbol-]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&amp;=`

[ref: #symbol-amp]

Appends in place to a string.

**Input:**
- `x: var string`
- `y: string`

**Output:** *(none)*
**Pragmas:** `magic: "AppendStrStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Appends in place to a string.

```
var a = "abc"
a &= "de" # a <- "abcde"
```

### `&amp;`

[ref: #symbol-amp]

Concatenates x with y.

**Input:**
- `x: string`
- `y: char`

**Output:** `string`
**Pragmas:** `magic: "ConStrStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenates x with y.

```
assert("ab" & 'c' == "abc")
```

### `&amp;`

[ref: #symbol-amp]

Concatenates characters x and y into a string.

**Input:**
- `x: char`
- `y: char`

**Output:** `string`
**Pragmas:** `magic: "ConStrStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenates characters x and y into a string.

```
assert('a' & 'b' == "ab")
```

### `&amp;`

[ref: #symbol-amp]

Concatenates strings x and y.

**Input:**
- `x: string`
- `y: string`

**Output:** `string`
**Pragmas:** `magic: "ConStrStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenates strings x and y.

```
assert("ab" & "cd" == "abcd")
```

### `&amp;`

[ref: #symbol-amp]

Concatenates x with y.

**Input:**
- `x: char`
- `y: string`

**Output:** `string`
**Pragmas:** `magic: "ConStrStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenates x with y.

```
assert('a' & "bc" == "abc")
```

### `&amp;`

[ref: #symbol-amp]

Concatenates two sequences.

**Input:**
- `x: sink seq[T]`
- `y: sink seq[T]`

**Output:** `seq[T]`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Concatenates two sequences.

Requires copying of the sequences.

```
assert(@[1, 2, 3, 4] & @[5, 6] == @[1, 2, 3, 4, 5, 6])
```

See also:

* [add(var seq[T], openArray[T])](#add,seq[T],openArray[T])

### `&amp;`

[ref: #symbol-amp]

Appends element y to the end of the sequence.

**Input:**
- `x: sink seq[T]`
- `y: sink T`

**Output:** `seq[T]`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Appends element y to the end of the sequence.

Requires copying of the sequence.

```
assert(@[1, 2, 3] & 4 == @[1, 2, 3, 4])
```

See also:

* [add(var seq[T], T)](#add,seq[T],sinkT)

### `&amp;`

[ref: #symbol-amp]

Prepends the element x to the beginning of the sequence.

**Input:**
- `x: sink T`
- `y: sink seq[T]`

**Output:** `seq[T]`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Prepends the element x to the beginning of the sequence.

Requires copying of the sequence.

```
assert(1 & @[2, 3, 4] == @[1, 2, 3, 4])
```

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `x: int`
- `y: int`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Treats x and y as unsigned and compares them. Returns true if unsigned(x) < unsigned(y).

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `x: int`
- `y: int`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Treats x and y as unsigned and compares them. Returns true if unsigned(x) <= unsigned(y).

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: Enum`
- `y: Enum`

**Output:** `bool`
**Generic parameters:** `Enum`

**Pragmas:** `magic: "LeEnum"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: string`
- `y: string`

**Output:** `bool`
**Pragmas:** `magic: "LeStr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two strings and returns true if x is lexicographically before y (uppercase letters come before lowercase letters).

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: char`
- `y: char`

**Output:** `bool`
**Pragmas:** `magic: "LeCh"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two chars and returns true if x is lexicographically before y (uppercase letters come before lowercase letters).

### `&lt;=`

[ref: #symbol-lt]

Returns true if x is a subset of y.

**Input:**
- `x: set[T]`
- `y: set[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "LeSet"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if x is a subset of y.

A subset x has all of its members in y and y doesn't necessarily have more members than x. That is, x can be equal to y.

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: bool`
- `y: bool`

**Output:** `bool`
**Pragmas:** `magic: "LeB"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: ref T`
- `y: ref T`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `magic: "LePtr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: pointer`
- `y: pointer`

**Output:** `bool`
**Pragmas:** `magic: "LePtr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Prev](system_1.md) | [Next](system_3.md)
