---
source_hash: ecb888946202a5f6
source_path: lib/system/ctypes.nim
---

# ctypes

[ref: #module-ctypes]

Some type definitions for compatibility between different backends and platforms.

## Type

### BiggestFloat

[ref: #symbol-biggestfloat]

```nim
BiggestFloat = float64
```

is an alias for the biggest floating point type the Nim compiler supports. Currently this is float64, but it is platform-dependent in general.

### BiggestInt

[ref: #symbol-biggestint]

```nim
BiggestInt = int64
```

is an alias for the biggest signed integer type the Nim compiler supports. Currently this is int64, but it is platform-dependent in general.

### BiggestUInt

[ref: #symbol-biggestuint]

```nim
BiggestUInt = uint64
```

is an alias for the biggest unsigned integer type the Nim compiler supports. Currently this is uint64, but it is platform-dependent in general.

### ByteAddress

[ref: #symbol-byteaddress]

```nim
ByteAddress {.deprecated: "use `uint`".} = int
```

is the signed integer type that should be used for converting pointers to integer addresses for readability.

### cchar

[ref: #symbol-cchar]

```nim
cchar {.importc: "char", nodecl.} = char
```

This is the same as the type char in *C*.

### cdouble

[ref: #symbol-cdouble]

```nim
cdouble {.importc: "double", nodecl.} = float64
```

This is the same as the type double in *C*.

### cfloat

[ref: #symbol-cfloat]

```nim
cfloat {.importc: "float", nodecl.} = float32
```

This is the same as the type float in *C*.

### cint

[ref: #symbol-cint]

```nim
cint {.importc: "int", nodecl.} = int32
```

This is the same as the type int in *C*.

### clong

[ref: #symbol-clong]

Represents the *C* long type, used for interoperability.

```nim
clong = ClongImpl
```

Represents the *C* long type, used for interoperability.

Its purpose is to match the *C* long for the target platform's Application Binary Interface (ABI).

Typically, the compiler resolves it to one of the following Nim types based on the target:

* [int32](system.html#int32) on Windows using MSVC or MinGW compilers.
* [int](system.html#int) on Linux, macOS and other platforms that use the LP64 or ILP32 [data models](https://en.wikipedia.org/wiki/64-bit_computing#64-bit_data_models).

**Warning:**
The underlying Nim type is an implementation detail and should not be relied upon.

### clongdouble

[ref: #symbol-clongdouble]

```nim
clongdouble {.importc: "long double", nodecl.} = BiggestFloat
```

This is the same as the type long double in *C*. This C type is not supported by Nim's code generator.

### clonglong

[ref: #symbol-clonglong]

```nim
clonglong {.importc: "long long", nodecl.} = int64
```

This is the same as the type long long in *C*.

### cschar

[ref: #symbol-cschar]

```nim
cschar {.importc: "signed char", nodecl.} = int8
```

This is the same as the type signed char in *C*.

### cshort

[ref: #symbol-cshort]

```nim
cshort {.importc: "short", nodecl.} = int16
```

This is the same as the type short in *C*.

### csize_t

[ref: #symbol-csize-t]

```nim
csize_t {.importc: "size_t", nodecl.} = uint
```

This is the same as the type size\_t in *C*.

### cstringArray

[ref: #symbol-cstringarray]

```nim
cstringArray {.importc: "char**", nodecl.} = ptr UncheckedArray[cstring]
```

This is binary compatible to the type char\*\* in *C*. The array's high value is large enough to disable bounds checking in practice. Use [cstringArrayToSeq proc](#cstringArrayToSeq,cstringArray,Natural) to convert it into a seq[string].

### cuchar

[ref: #symbol-cuchar]

```nim
cuchar {.importc: "unsigned char", nodecl,
         deprecated: "Use `char` or `uint8` instead".} = char
```

### cuint

[ref: #symbol-cuint]

```nim
cuint {.importc: "unsigned int", nodecl.} = uint32
```

This is the same as the type unsigned int in *C*.

### culong

[ref: #symbol-culong]

Represents the *C* unsigned long type, used for interoperability.

```nim
culong = CulongImpl
```

Represents the *C* unsigned long type, used for interoperability.

Its purpose is to match the *C* unsigned long for the target platform's Application Binary Interface (ABI).

Typically, the compiler resolves it to one of the following Nim types based on the target:

* [uint32](system.html#uint32) on Windows using MSVC or MinGW compilers.
* [uint](system.html#uint) on Linux, macOS and other platforms that use the LP64 or ILP32 [data models](https://en.wikipedia.org/wiki/64-bit_computing#64-bit_data_models).

**Warning:**
The underlying Nim type is an implementation detail and should not be relied upon.

### culonglong

[ref: #symbol-culonglong]

```nim
culonglong {.importc: "unsigned long long", nodecl.} = uint64
```

This is the same as the type unsigned long long in *C*.

### cushort

[ref: #symbol-cushort]

```nim
cushort {.importc: "unsigned short", nodecl.} = uint16
```

This is the same as the type unsigned short in *C*.

### PFloat32

[ref: #symbol-pfloat32]

```nim
PFloat32 {.deprecated: "use `ptr float32`".} = ptr float32
```

An alias for ptr float32.

### PFloat64

[ref: #symbol-pfloat64]

```nim
PFloat64 {.deprecated: "use `ptr float64`".} = ptr float64
```

An alias for ptr float64.

### PInt32

[ref: #symbol-pint32]

```nim
PInt32 {.deprecated: "use `ptr int32`".} = ptr int32
```

An alias for ptr int32.

### PInt64

[ref: #symbol-pint64]

```nim
PInt64 {.deprecated: "use `ptr int64`".} = ptr int64
```

An alias for ptr int64.
