---
source_hash: 94955b10a8b4492b
source_path: lib/pure/typetraits.nim
---

# typetraits

[ref: #module-typetraits]

This module defines compile-time reflection procs for working with types.

Unstable API.

## Examples

```nim
import std/typetraits
type A = enum a0 = 2, a1 = 4, a2
type B = enum b0 = 2, b1, b2
assert A is enum
assert A is HoleyEnum
assert A isnot OrdinalEnum
assert B isnot HoleyEnum
assert B is OrdinalEnum
assert int isnot HoleyEnum
type C[T] = enum h0 = 2, h1 = 4
assert C[float] is HoleyEnum
```

```nim
doAssert arity(int) == 0
doAssert arity(seq[string]) == 1
doAssert arity(array[3, int]) == 2
doAssert arity((int, int, float, string)) == 4
```

```nim
type MyInt = distinct int
type MyOtherInt = distinct MyInt
doAssert distinctBase(MyInt) is int
doAssert distinctBase(MyOtherInt) is int
doAssert distinctBase(MyOtherInt, false) is MyInt
doAssert distinctBase(int) is int
```

```nim
type
  Foo[T] = object
  FooInst = Foo[int]
  Foo2 = genericHead(FooInst)

doAssert Foo2 is Foo and Foo is Foo2
doAssert genericHead(Foo[seq[string]]) is Foo
doAssert not compiles(genericHead(int))

type Generic = concept f
  type _ = genericHead(typeof(f))

proc bar(a: Generic): typeof(a) = a

doAssert bar(Foo[string].default) == Foo[string]()
doAssert not compiles bar(string.default)

when false: # these don't work yet
  doAssert genericHead(Foo[int])[float] is Foo[float]
  doAssert seq[int].genericHead is seq
```

```nim
{.experimental: "strictNotNil".}
type
  NilableObject = ref object
    a: int
  Object = NilableObject not nil
  RequiresInit[T] = object
    a {.requiresInit.}: T

assert hasDefaultValue(NilableObject)
assert not hasDefaultValue(Object)
assert hasDefaultValue(string)
assert not hasDefaultValue(var string)
assert not hasDefaultValue(RequiresInit[int])
```

```nim
doAssert not isNamedTuple(int)
doAssert not isNamedTuple((string, int))
doAssert isNamedTuple(tuple[name: string, age: int])
```

```nim
doAssert name(int) == "int"
doAssert name(seq[string]) == "seq[string]"
```

```nim
type MyRange = range[0..5]
type MyEnum = enum a, b, c
type MyEnumRange = range[b..c]
doAssert rangeBase(MyRange) is int
doAssert rangeBase(MyEnumRange) is MyEnum
doAssert rangeBase(range['a'..'z']) is char
```

```nim
type Foo[T] = object

doAssert stripGenericParams(Foo[string]) is Foo
doAssert stripGenericParams(int) is int
```

```nim
doAssert tupleLen((int, int, float, string)) == 4
doAssert tupleLen(tuple[name: string, age: int]) == 2
```

```nim
type Foo = enum
  fooItem1
  fooItem2

doAssert Foo.enumLen == 2
```

```nim
type MyInt = distinct int
type MyOtherInt = distinct MyInt
doAssert 12.MyInt.distinctBase == 12
doAssert 12.MyOtherInt.distinctBase == 12
doAssert 12.MyOtherInt.distinctBase(false) is MyInt
doAssert 12.distinctBase == 12
```

```nim
iterator myiter(n: int): auto =
  for i in 0 ..< n:
    yield i

doAssert elementType(@[1,2]) is int
doAssert elementType("asdf") is char
doAssert elementType(myiter(3)) is int
```

```nim
type Foo[T1, T2] = object

doAssert genericParams(Foo[float, string]) is (float, string)

type Bar[N: static float, T] = object

doAssert genericParams(Bar[1.0, string]) is (StaticParam[1.0], string)
doAssert genericParams(Bar[1.0, string]).get(0).value == 1.0
doAssert genericParams(seq[Bar[2.0, string]]).get(0) is Bar[2.0, string]
var s: seq[Bar[3.0, string]]
doAssert genericParams(typeof(s)) is (Bar[3.0, string],)

doAssert genericParams(array[10, int]) is (StaticParam[10], int)
var a: array[10, int]
doAssert genericParams(typeof(a)) is (range[0..9], int)
```

```nim
doAssert get((int, int, float, string), 2) is float
```

```nim
assert (ref int).pointerBase is int
type A = ptr seq[float]
assert A.pointerBase is seq[float]
assert (ref A).pointerBase is A # not seq[float]
assert (var s = "abc"; s[0].addr).typeof.pointerBase is char
```

```nim
type MyRange = range[0..5]
type MyEnum = enum a, b, c
type MyEnumRange = range[b..c]
let x = MyRange(3)
doAssert rangeBase(x) is int
doAssert $typeof(rangeBase(x)) == "int"
doAssert rangeBase(x) == 3
let y: set[MyEnumRange] = {c}
for e in y:
  doAssert rangeBase(e) is MyEnum
  doAssert $typeof(rangeBase(e)) == "MyEnum"
  doAssert rangeBase(e) == c
let z: seq[range['a'..'z']] = @['c']
doAssert rangeBase(z[0]) is char
doAssert $typeof(rangeBase(z[0])) == "char"
doAssert rangeBase(z[0]) == 'c'
```

```nim
assert int8.toSigned is int8
assert uint16.toSigned is int16
# range types are currently unsupported:
assert not compiles(toSigned(range[0..7]))
```

```nim
assert int8.toUnsigned is uint8
assert uint.toUnsigned is uint
assert int.toUnsigned is uint
# range types are currently unsupported:
assert not compiles(toUnsigned(range[0..7]))
```

```nim
doAssert tupleLen((1, 2)) == 2
```

## Macro

### enumLen

[ref: #symbol-enumlen]

**Input:**
- `T: typedesc[enum]`

**Output:** `int`
**Generic parameters:** `T:type`

Returns the number of items in the enum T.

## Proc

### arity

[ref: #symbol-arity]

**Input:**
- `t: typedesc`

**Output:** `int`
**Generic parameters:** `t:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the arity of t. This is the number of "type" components or the number of generic parameters a given type t has.

### distinctBase

[ref: #symbol-distinctbase]

Returns the base type for distinct types, or the type itself otherwise. If recursive is false, only the immediate distinct base will be returned.

**Input:**
- `T: typedesc`
- `recursive: static bool = true`

**Output:** `typedesc`
**Generic parameters:** `T:type`, `recursive:type`, `result:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the base type for distinct types, or the type itself otherwise. If recursive is false, only the immediate distinct base will be returned.

**See also:**

* [distinctBase template](#distinctBase.t,T,static[bool])

### genericHead

[ref: #symbol-generichead]

Accepts an instantiated generic type and returns its uninstantiated form. A compile-time error will be produced if the supplied type is not generic.

**Input:**
- `t: typedesc`

**Output:** `typedesc`
**Generic parameters:** `t:type`, `result:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Accepts an instantiated generic type and returns its uninstantiated form. A compile-time error will be produced if the supplied type is not generic.

**See also:**

* [stripGenericParams proc](#stripGenericParams,typedesc)

### hasClosure

[ref: #symbol-hasclosure]

**Input:**
- `fn: NimNode`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if the func/proc/etc fn has closure. fn has to be a resolved symbol of kind nnkSym. This implies that the macro that calls this proc should accept typed arguments and not untyped arguments.

### hasDefaultValue

[ref: #symbol-hasdefaultvalue]

**Input:**
- `t: typedesc`

**Output:** `bool`
**Generic parameters:** `t:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if t has a valid default value.

### isNamedTuple

[ref: #symbol-isnamedtuple]

**Input:**
- `T: typedesc`

**Output:** `bool`
**Generic parameters:** `T:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true for named tuples, false for any other type.

### name

[ref: #symbol-name]

Returns the name of t.

**Input:**
- `t: typedesc`

**Output:** `string`
**Generic parameters:** `t:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the name of t.

Alias for [system.`$`(t)](dollars.html#$,typedesc) since Nim v0.20.

### rangeBase

[ref: #symbol-rangebase]

Returns the base type for range types, or the type itself otherwise.

**Input:**
- `T: typedesc[range]`

**Output:** `typedesc`
**Generic parameters:** `T:type`, `result:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the base type for range types, or the type itself otherwise.

**See also:**

* [rangeBase template](#rangeBase.t,T)

### stripGenericParams

[ref: #symbol-stripgenericparams]

**Input:**
- `t: typedesc`

**Output:** `typedesc`
**Generic parameters:** `t:type`, `result:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

This trait is similar to [genericHead](#genericHead,typedesc), but instead of producing an error for non-generic types, it will just return them unmodified.

### supportsCopyMem

[ref: #symbol-supportscopymem]

Returns true if t is safe to use for copyMem.

**Input:**
- `t: typedesc`

**Output:** `bool`
**Generic parameters:** `t:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if t is safe to use for copyMem.

Other languages name a type like these blob.

### tupleLen

[ref: #symbol-tuplelen]

Returns the number of elements of the tuple type T.

**Input:**
- `T: typedesc[tuple]`

**Output:** `int`
**Generic parameters:** `T:type`

**Pragmas:** `magic: "TypeTrait"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of elements of the tuple type T.

**See also:**

* [tupleLen template](#tupleLen.t)

## Template

### distinctBase

[ref: #symbol-distinctbase]

**Input:**
- `a: T`
- `recursive: static bool = true`

**Output:** `untyped`
**Generic parameters:** `T`, `recursive:type`

Overload of [distinctBase](#distinctBase,typedesc,static[bool]) for values.

### elementType

[ref: #symbol-elementtype]

**Input:**
- `a: untyped`

**Output:** `typedesc`
**Generic parameters:** `result:type`

Returns the element type of a, which can be any iterable (over which you can iterate).

### genericParams

[ref: #symbol-genericparams]

Returns the tuple of generic parameters for the generic type T.

**Input:**
- `T: typedesc`

**Output:** `untyped`
**Generic parameters:** `T:type`

Returns the tuple of generic parameters for the generic type T.

**Note:** For the builtin array type, the index generic parameter will **always** become a range type after it's bound to a variable.

### get

[ref: #symbol-get]

**Input:**
- `T: typedesc[tuple]`
- `i: static int`

**Output:** `untyped`
**Generic parameters:** `T:type`, `i:type`

Returns the i-th element of T.

### pointerBase

[ref: #symbol-pointerbase]

**Input:**
- `_: typedesc[ptr T | ref T]`

**Output:** `typedesc`
**Generic parameters:** `T`, `_`gensym553648163:type`, `result:type`

Returns T for ref T | ptr T.

### rangeBase

[ref: #symbol-rangebase]

**Input:**
- `a: T`

**Output:** `untyped`
**Generic parameters:** `T`

Overload of [rangeBase](#rangeBase,typedesc,static[bool]) for values.

### toSigned

[ref: #symbol-tosigned]

**Input:**
- `T: typedesc[SomeInteger and not range]`

**Output:** `untyped`
**Generic parameters:** `T:type`

Returns a signed type with same bit size as T.

### toUnsigned

[ref: #symbol-tounsigned]

**Input:**
- `T: typedesc[SomeInteger and not range]`

**Output:** `untyped`
**Generic parameters:** `T:type`

Returns an unsigned type with same bit size as T.

### tupleLen

[ref: #symbol-tuplelen]

Returns the number of elements of the tuple t.

**Input:**
- `t: tuple`

**Output:** `int`
**Generic parameters:** `t:type`

Returns the number of elements of the tuple t.

**See also:**

* [tupleLen proc](#tupleLen,typedesc)

## Type

### HoleyEnum

[ref: #symbol-holeyenum]

```nim
HoleyEnum = (not Ordinal) and enum
```

Enum with holes.

### OrdinalEnum

[ref: #symbol-ordinalenum]

```nim
OrdinalEnum = Ordinal and enum
```

Enum without holes.

### StaticParam

[ref: #symbol-staticparam]

```nim
StaticParam[value] = object
```

Used to wrap a static value in [genericParams](#genericParams.t,typedesc).
