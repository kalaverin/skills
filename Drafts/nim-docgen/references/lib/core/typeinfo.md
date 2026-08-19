---
source_hash: f76003462fcd94bd
source_path: lib/core/typeinfo.nim
---

# typeinfo

[ref: #module-typeinfo]

This module implements an interface to Nim's runtime type information (RTTI). See the [marshal](marshal.html) module for an example of what this allows you to do.

**Note:**
Even though Any and its operations hide the nasty low level details from its users, it remains inherently unsafe! Also, Nim's runtime type information will evolve and may eventually be deprecated. As an alternative approach to programmatically understanding and manipulating types, consider using the [macros](macros.html) module to work with the types' AST representation at compile time. See for example the [getTypeImpl proc](macros.html#getTypeImpl,NimNode). As an alternative approach to storing arbitrary types at runtime, consider using generics.

## Examples

```nim
import std/typeinfo
var x: Any

var i = 42
x = i.toAny
assert x.kind == akInt
assert x.getInt == 42

var s = @[1, 2, 3]
x = s.toAny
assert x.kind == akSequence
assert x.len == 3
```

## Iterator

### elements

[ref: #symbol-elements]

**Input:**
- `x: Any`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over every element of x. x needs to represent a set.

### fields

[ref: #symbol-fields]

**Input:**
- `x: Any`

**Output:** `tuple[name: string, any: Any]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over every active field of x. x needs to represent an object or a tuple.

## Proc

### `[]=`

[ref: #symbol-]

**Input:**
- `x: Any`
- `i: int`
- `y: Any`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Accessor for an any x that represents an array or a sequence.

### `[]=`

[ref: #symbol-]

**Input:**
- `x: Any`
- `fieldName: string`
- `value: Any`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Sets a field of x. x needs to represent an object or a tuple.

### `[]=`

[ref: #symbol-]

**Input:**
- `x: Any`
- `y: Any`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Dereference operator for Any. x needs to represent a ptr or a ref.

### `[]`

[ref: #symbol-]

**Input:**
- `x: Any`
- `i: int`

**Output:** `Any`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Accessor for an any x that represents an array or a sequence.

### `[]`

[ref: #symbol-]

**Input:**
- `x: Any`
- `fieldName: string`

**Output:** `Any`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Gets a field of x. x needs to represent an object or a tuple.

### `[]`

[ref: #symbol-]

**Input:**
- `x: Any`

**Output:** `Any`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Dereference operator for Any. x needs to represent a ptr or a ref.

### assign

[ref: #symbol-assign]

**Input:**
- `x: Any`
- `y: Any`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copies the value of y to x. The assignment operator for Any does NOT do this; it performs a shallow copy instead!

### base

[ref: #symbol-base]

**Input:**
- `x: Any`

**Output:** `Any`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the base type of x (useful for inherited object types).

### baseTypeKind

[ref: #symbol-basetypekind]

**Input:**
- `x: Any`

**Output:** `AnyKind`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the base type's kind. If x has no base type, akNone is returned.

### baseTypeSize

[ref: #symbol-basetypesize]

**Input:**
- `x: Any`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the size of x's base type. If x has no base type, 0 is returned.

### extendSeq

[ref: #symbol-extendseq]

**Input:**
- `x: Any`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Performs setLen(x, x.len+1). x needs to represent a seq.

### getBiggestFloat

[ref: #symbol-getbiggestfloat]

**Input:**
- `x: Any`

**Output:** `BiggestFloat`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the float value out of x. x needs to represent some float. The value is extended to BiggestFloat.

### getBiggestInt

[ref: #symbol-getbiggestint]

**Input:**
- `x: Any`

**Output:** `BiggestInt`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the integer value out of x. x needs to represent some integer, a bool, a char, an enum or a small enough bit set. The value might be sign-extended to BiggestInt.

### getBiggestUint

[ref: #symbol-getbiggestuint]

**Input:**
- `x: Any`

**Output:** `uint64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the unsigned integer value out of x. x needs to represent an unsigned integer.

### getBool

[ref: #symbol-getbool]

**Input:**
- `x: Any`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the bool value out of x. x needs to represent a bool.

### getChar

[ref: #symbol-getchar]

**Input:**
- `x: Any`

**Output:** `char`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the char value out of x. x needs to represent a char.

### getCString

[ref: #symbol-getcstring]

**Input:**
- `x: Any`

**Output:** `cstring`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the cstring value out of x. x needs to represent a cstring.

### getEnumField

[ref: #symbol-getenumfield]

**Input:**
- `x: Any`
- `ordinalValue: int`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the enum field name as a string. x needs to represent an enum but is only used to access the type information. The field name of ordinalValue is returned.

### getEnumField

[ref: #symbol-getenumfield]

**Input:**
- `x: Any`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the enum field name as a string. x needs to represent an enum.

### getEnumOrdinal

[ref: #symbol-getenumordinal]

**Input:**
- `x: Any`
- `name: string`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the enum field ordinal from name. x needs to represent an enum but is only used to access the type information. In case of an error low(int) is returned.

### getFloat

[ref: #symbol-getfloat]

**Input:**
- `x: Any`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the float value out of x. x needs to represent a float.

### getFloat32

[ref: #symbol-getfloat32]

**Input:**
- `x: Any`

**Output:** `float32`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the float32 value out of x. x needs to represent a float32.

### getFloat64

[ref: #symbol-getfloat64]

**Input:**
- `x: Any`

**Output:** `float64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the float64 value out of x. x needs to represent a float64.

### getInt

[ref: #symbol-getint]

**Input:**
- `x: Any`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the int value out of x. x needs to represent an int.

### getInt16

[ref: #symbol-getint16]

**Input:**
- `x: Any`

**Output:** `int16`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the int16 value out of x. x needs to represent an int16.

### getInt32

[ref: #symbol-getint32]

**Input:**
- `x: Any`

**Output:** `int32`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the int32 value out of x. x needs to represent an int32.

### getInt64

[ref: #symbol-getint64]

**Input:**
- `x: Any`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the int64 value out of x. x needs to represent an int64.

### getInt8

[ref: #symbol-getint8]

**Input:**
- `x: Any`

**Output:** `int8`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the int8 value out of x. x needs to represent an int8.

### getPointer

[ref: #symbol-getpointer]

**Input:**
- `x: Any`

**Output:** `pointer`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the pointer value out of x. x needs to be of kind akString, akCString, akProc, akRef, akPtr, akPointer or akSequence.

### getString

[ref: #symbol-getstring]

**Input:**
- `x: Any`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the string value out of x. x needs to represent a string.

### getUInt

[ref: #symbol-getuint]

**Input:**
- `x: Any`

**Output:** `uint`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the uint value out of x. x needs to represent a uint.

### getUInt16

[ref: #symbol-getuint16]

**Input:**
- `x: Any`

**Output:** `uint16`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the uint16 value out of x. x needs to represent a uint16.

### getUInt32

[ref: #symbol-getuint32]

**Input:**
- `x: Any`

**Output:** `uint32`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the uint32 value out of x. x needs to represent a uint32.

### getUInt64

[ref: #symbol-getuint64]

**Input:**
- `x: Any`

**Output:** `uint64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the uint64 value out of x. x needs to represent a uint64.

### getUInt8

[ref: #symbol-getuint8]

**Input:**
- `x: Any`

**Output:** `uint8`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the uint8 value out of x. x needs to represent a uint8.

### inclSetElement

[ref: #symbol-inclsetelement]

**Input:**
- `x: Any`
- `elem: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Includes an element elem in x. x needs to represent a Nim bitset.

### invokeNew

[ref: #symbol-invokenew]

**Input:**
- `x: Any`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Performs new(x). x needs to represent a ref.

### invokeNewSeq

[ref: #symbol-invokenewseq]

**Input:**
- `x: Any`
- `len: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Performs newSeq(x, len). x needs to represent a seq.

### isNil

[ref: #symbol-isnil]

**Input:**
- `x: Any`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

isNil for an x that represents a cstring, proc or some pointer type.

### kind

[ref: #symbol-kind]

**Input:**
- `x: Any`

**Output:** `AnyKind`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the type kind.

### len

[ref: #symbol-len]

**Input:**
- `x: Any`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

len for an any x that represents an array or a sequence.

### setBiggestFloat

[ref: #symbol-setbiggestfloat]

**Input:**
- `x: Any`
- `y: BiggestFloat`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the float value of x. x needs to represent some float.

### setBiggestInt

[ref: #symbol-setbiggestint]

**Input:**
- `x: Any`
- `y: BiggestInt`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the integer value of x. x needs to represent some integer, a bool, a char, an enum or a small enough bit set.

### setBiggestUint

[ref: #symbol-setbiggestuint]

**Input:**
- `x: Any`
- `y: uint64`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the unsigned integer value of x. x needs to represent an unsigned integer.

### setObjectRuntimeType

[ref: #symbol-setobjectruntimetype]

**Input:**
- `x: Any`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This needs to be called to set x's runtime object type field.

### setPointer

[ref: #symbol-setpointer]

**Input:**
- `x: Any`
- `y: pointer`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the pointer value of x. x needs to be of kind akString, akCString, akProc, akRef, akPtr, akPointer or akSequence.

### setString

[ref: #symbol-setstring]

**Input:**
- `x: Any`
- `y: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the string value of x. x needs to represent a string.

### size

[ref: #symbol-size]

**Input:**
- `x: Any`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the size of x's type.

### skipRange

[ref: #symbol-skiprange]

**Input:**
- `x: Any`

**Output:** `Any`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips the range information of x.

### toAny

[ref: #symbol-toany]

**Input:**
- `x: var T`

**Output:** `Any`
**Generic parameters:** `T`

**Pragmas:** `inline`

Constructs an Any object from x. This captures x's address, so x can be modified with its Any wrapper! The caller needs to ensure that the wrapper **does not** live longer than x!

## Type

### Any

[ref: #symbol-any]

A type that can represent any nim value.

```nim
Any = object
  when defined(js):
  else:
```

A type that can represent any nim value.

**Danger:**
The wrapped value can be modified with its wrapper! This means that Any keeps a non-traced pointer to its wrapped value and **must not** live longer than its wrapped value.

### AnyKind

[ref: #symbol-anykind]

```nim
AnyKind = enum
  akNone = 0,               ## invalid
  akBool = 1,               ## bool
  akChar = 2,               ## char
  akEnum = 14,              ## enum
  akArray = 16,             ## array
  akObject = 17,            ## object
  akTuple = 18,             ## tuple
  akSet = 19,               ## set
  akRange = 20,             ## range
  akPtr = 21,               ## ptr
  akRef = 22,               ## ref
  akSequence = 24,          ## sequence
  akProc = 25,              ## proc
  akPointer = 26,           ## pointer
  akString = 28,            ## string
  akCString = 29,           ## cstring
  akInt = 31,               ## int
  akInt8 = 32,              ## int8
  akInt16 = 33,             ## int16
  akInt32 = 34,             ## int32
  akInt64 = 35,             ## int64
  akFloat = 36,             ## float
  akFloat32 = 37,           ## float32
  akFloat64 = 38,           ## float64
  akFloat128 = 39,          ## float128
  akUInt = 40,              ## uint
  akUInt8 = 41,             ## uint8
  akUInt16 = 42,            ## uin16
  akUInt32 = 43,            ## uint32
  akUInt64 = 44              ## uint64
```

The kind of Any.
