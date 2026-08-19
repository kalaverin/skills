---
source_hash: e7666fa62e30d950
source_path: lib/pure/bitops.nim
---

# bitops

[ref: #module-bitops]

This module implements a series of low level methods for bit manipulation.

By default, compiler intrinsics are used where possible to improve performance on supported compilers: GCC, LLVM\_GCC, CLANG, VCC, ICC.

The module will fallback to pure nim procs in case the backend is not supported. You can also use the flag noIntrinsicsBitOpts to disable compiler intrinsics.

This module is also compatible with other backends: JavaScript, NimScript as well as the compiletime VM.

As a result of using optimized functions/intrinsics, some functions can return undefined results if the input is invalid. You can use the flag noUndefinedBitOpts to force predictable behaviour for all input, causing a small performance hit.

At this time only fastLog2, firstSetBit, countLeadingZeroBits and countTrailingZeroBits may return undefined and/or platform dependent values if given invalid input.

## Examples

```nim
var x = 0b101110
x.bitslice(2 .. 4)
doAssert x == 0b011
```

```nim
doAssert 0b10111.bitsliced(2 .. 4) == 0b101
doAssert 0b11100.bitsliced(0 .. 2) == 0b100
doAssert 0b11100.bitsliced(0 ..< 3) == 0b100
```

```nim
var v = 0b0000_0011'u8
v.clearBit(1'u8)
doAssert v == 0b0000_0001'u8
```

```nim
var v = 0b0000_0011'u8
v.clearMask(0b0000_1010'u8)
doAssert v == 0b0000_0001'u8
```

```nim
var v = 0b0000_0011'u8
v.clearMask(1 .. 3)
doAssert v == 0b0000_0001'u8
```

```nim
let v = 0b0000_0011'u8
doAssert v.clearMasked(0b0000_1010'u8) == 0b0000_0001'u8
```

```nim
let v = 0b0000_0011'u8
doAssert v.clearMasked(1 .. 3) == 0b0000_0001'u8
```

```nim
doAssert countLeadingZeroBits(0b0000_0001'u8) == 7
doAssert countLeadingZeroBits(0b0000_0010'u8) == 6
doAssert countLeadingZeroBits(0b0000_0100'u8) == 5
doAssert countLeadingZeroBits(0b0000_1000'u8) == 4
doAssert countLeadingZeroBits(0b0000_1111'u8) == 4
```

```nim
doAssert countSetBits(0b0000_0011'u8) == 2
doAssert countSetBits(0b1010_1010'u8) == 4
```

```nim
doAssert countTrailingZeroBits(0b0000_0001'u8) == 0
doAssert countTrailingZeroBits(0b0000_0010'u8) == 1
doAssert countTrailingZeroBits(0b0000_0100'u8) == 2
doAssert countTrailingZeroBits(0b0000_1000'u8) == 3
doAssert countTrailingZeroBits(0b0000_1111'u8) == 0
```

```nim
doAssert fastLog2(0b0000_0001'u8) == 0
doAssert fastLog2(0b0000_0010'u8) == 1
doAssert fastLog2(0b0000_0100'u8) == 2
doAssert fastLog2(0b0000_1000'u8) == 3
doAssert fastLog2(0b0000_1111'u8) == 3
```

```nim
doAssert firstSetBit(0b0000_0001'u8) == 1
doAssert firstSetBit(0b0000_0010'u8) == 2
doAssert firstSetBit(0b0000_0100'u8) == 3
doAssert firstSetBit(0b0000_1000'u8) == 4
doAssert firstSetBit(0b0000_1111'u8) == 1
```

```nim
var v = 0b0000_0011'u8
v.flipBit(1'u8)
doAssert v == 0b0000_0001'u8

v = 0b0000_0011'u8
v.flipBit(2'u8)
doAssert v == 0b0000_0111'u8
```

```nim
var v = 0b0000_0011'u8
v.flipMask(0b0000_1010'u8)
doAssert v == 0b0000_1001'u8
```

```nim
var v = 0b0000_0011'u8
v.flipMask(1 .. 3)
doAssert v == 0b0000_1101'u8
```

```nim
let v = 0b0000_0011'u8
doAssert v.flipMasked(0b0000_1010'u8) == 0b0000_1001'u8
```

```nim
let v = 0b0000_0011'u8
doAssert v.flipMasked(1 .. 3) == 0b0000_1101'u8
```

```nim
var v = 0b0000_0011'u8
v.mask(0b0000_1010'u8)
doAssert v == 0b0000_0010'u8
```

```nim
var v = 0b0000_1011'u8
v.mask(1 .. 3)
doAssert v == 0b0000_1010'u8
```

```nim
let v = 0b0000_0011'u8
doAssert v.masked(0b0000_1010'u8) == 0b0000_0010'u8
```

```nim
let v = 0b0000_1011'u8
doAssert v.masked(1 .. 3) == 0b0000_1010'u8
```

```nim
doAssert parityBits(0b0000_0000'u8) == 0
doAssert parityBits(0b0101_0001'u8) == 1
doAssert parityBits(0b0110_1001'u8) == 0
doAssert parityBits(0b0111_1111'u8) == 1
```

```nim
doAssert reverseBits(0b10100100'u8) == 0b00100101'u8
doAssert reverseBits(0xdd'u8) == 0xbb'u8
doAssert reverseBits(0xddbb'u16) == 0xddbb'u16
doAssert reverseBits(0xdeadbeef'u32) == 0xf77db57b'u32
```

```nim
doAssert rotateLeftBits(0b0110_1001'u8, 4) == 0b1001_0110'u8
doAssert rotateLeftBits(0b00111100_11000011'u16, 8) ==
  0b11000011_00111100'u16
doAssert rotateLeftBits(0b0000111111110000_1111000000001111'u32, 16) ==
  0b1111000000001111_0000111111110000'u32
doAssert rotateLeftBits(0b00000000111111111111111100000000_11111111000000000000000011111111'u64, 32) ==
  0b11111111000000000000000011111111_00000000111111111111111100000000'u64
```

```nim
doAssert rotateRightBits(0b0110_1001'u8, 4) == 0b1001_0110'u8
doAssert rotateRightBits(0b00111100_11000011'u16, 8) ==
  0b11000011_00111100'u16
doAssert rotateRightBits(0b0000111111110000_1111000000001111'u32, 16) ==
  0b1111000000001111_0000111111110000'u32
doAssert rotateRightBits(0b00000000111111111111111100000000_11111111000000000000000011111111'u64, 32) ==
  0b11111111000000000000000011111111_00000000111111111111111100000000'u64
```

```nim
var v = 0b0000_0011'u8
v.setBit(5'u8)
doAssert v == 0b0010_0011'u8
```

```nim
var v = 0b0000_0011'u8
v.setMask(0b0000_1010'u8)
doAssert v == 0b0000_1011'u8
```

```nim
var v = 0b0000_0011'u8
v.setMask(2 .. 3)
doAssert v == 0b0000_1111'u8
```

```nim
let v = 0b0000_0011'u8
doAssert v.setMasked(0b0000_1010'u8) == 0b0000_1011'u8
```

```nim
let v = 0b0000_0011'u8
doAssert v.setMasked(2 .. 3) == 0b0000_1111'u8
```

```nim
let v = 0b0000_1111'u8
doAssert v.testBit(0)
doAssert not v.testBit(7)
```

```nim
doAssert toMask[int32](1 .. 3) == 0b1110'i32
doAssert toMask[int32](0 .. 3) == 0b1111'i32
```

```nim
var v = 0b1111_1111'u8
v.clearBits(1, 3, 5, 7)
doAssert v == 0b0101_0101'u8
```

```nim
var v = 0b0000_1111'u8
v.flipBits(1, 3, 5, 7)
doAssert v == 0b1010_0101'u8
```

```nim
var v = 0b0000_0011'u8
v.setBits(3, 5, 7)
doAssert v == 0b1010_1011'u8
```

## Macro

### bitand

[ref: #symbol-bitand]

**Input:**
- `x: T`
- `y: T`
- `z: varargs[T]`

**Output:** `T`
**Generic parameters:** `T`

Computes the bitwise and of all arguments collectively.

### bitor

[ref: #symbol-bitor]

**Input:**
- `x: T`
- `y: T`
- `z: varargs[T]`

**Output:** `T`
**Generic parameters:** `T`

Computes the bitwise or of all arguments collectively.

### bitxor

[ref: #symbol-bitxor]

**Input:**
- `x: T`
- `y: T`
- `z: varargs[T]`

**Output:** `T`
**Generic parameters:** `T`

Computes the bitwise xor of all arguments collectively.

### clearBits

[ref: #symbol-clearbits]

**Input:**
- `v: typed`
- `bits: varargs[typed]`

**Output:** `untyped`
Mutates v, with the bits at positions bits set to 0.

### flipBits

[ref: #symbol-flipbits]

**Input:**
- `v: typed`
- `bits: varargs[typed]`

**Output:** `untyped`
Mutates v, with the bits at positions bits set to 0.

### setBits

[ref: #symbol-setbits]

**Input:**
- `v: typed`
- `bits: varargs[typed]`

**Output:** `untyped`
Mutates v, with the bits at positions bits set to 1.

## Proc

### bitnot

[ref: #symbol-bitnot]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `magic: "BitnotI"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the bitwise complement of the integer x.

### bitslice

[ref: #symbol-bitslice]

**Input:**
- `v: var T`
- `slice: Slice[int]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v into an extracted (and shifted) slice of bits from v.

### bitsliced

[ref: #symbol-bitsliced]

**Input:**
- `v: T`
- `slice: Slice[int]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns an extracted (and shifted) slice of bits from v.

### clearBit

[ref: #symbol-clearbit]

**Input:**
- `v: var T`
- `bit: BitsRange[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with the bit at position bit set to 0.

### clearMask

[ref: #symbol-clearmask]

Mutates v, with all the 1 bits from mask set to 0.

**Input:**
- `v: var T`
- `mask: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with all the 1 bits from mask set to 0.

Effectively maps to a [bitand](#bitand.m,T,T,varargs[T]) operation with an *inverted mask*.

### clearMask

[ref: #symbol-clearmask]

Mutates v, with all the 1 bits in the range of slice set to 0.

**Input:**
- `v: var T`
- `slice: Slice[int]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with all the 1 bits in the range of slice set to 0.

Effectively maps to a [bitand](#bitand.m,T,T,varargs[T]) operation with an *inverted mask*.

### clearMasked

[ref: #symbol-clearmasked]

Returns v, with all the 1 bits from mask set to 0.

**Input:**
- `v: T`
- `mask: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns v, with all the 1 bits from mask set to 0.

Effectively maps to a [bitand](#bitand.m,T,T,varargs[T]) operation with an *inverted mask*.

### clearMasked

[ref: #symbol-clearmasked]

Returns v, with all the 1 bits in the range of slice set to 0.

**Input:**
- `v: T`
- `slice: Slice[int]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns v, with all the 1 bits in the range of slice set to 0.

Effectively maps to a [bitand](#bitand.m,T,T,varargs[T]) operation with an *inverted mask*.

### countLeadingZeroBits

[ref: #symbol-countleadingzerobits]

Returns the number of leading zero bits in an integer. If x is zero, when noUndefinedBitOpts is set, the result is 0, otherwise the result is undefined.

**Input:**
- `x: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `inline`

Returns the number of leading zero bits in an integer. If x is zero, when noUndefinedBitOpts is set, the result is 0, otherwise the result is undefined.

**See also:**

* [countTrailingZeroBits proc](#countTrailingZeroBits,SomeInteger)

### countSetBits

[ref: #symbol-countsetbits]

**Input:**
- `x: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `inline`

Counts the set bits in an integer (also called Hamming weight).

### countTrailingZeroBits

[ref: #symbol-counttrailingzerobits]

Returns the number of trailing zeros in an integer. If x is zero, when noUndefinedBitOpts is set, the result is 0, otherwise the result is undefined.

**Input:**
- `x: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `inline`

Returns the number of trailing zeros in an integer. If x is zero, when noUndefinedBitOpts is set, the result is 0, otherwise the result is undefined.

**See also:**

* [countLeadingZeroBits proc](#countLeadingZeroBits,SomeInteger)

### fastLog2

[ref: #symbol-fastlog2]

**Input:**
- `x: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `inline`

Quickly find the log base 2 of an integer. If x is zero, when noUndefinedBitOpts is set, the result is -1, otherwise the result is undefined.

### firstSetBit

[ref: #symbol-firstsetbit]

**Input:**
- `x: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `inline`

Returns the 1-based index of the least significant set bit of x. If x is zero, when noUndefinedBitOpts is set, the result is 0, otherwise the result is undefined.

### flipBit

[ref: #symbol-flipbit]

**Input:**
- `v: var T`
- `bit: BitsRange[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with the bit at position bit flipped.

### flipMask

[ref: #symbol-flipmask]

Mutates v, with all the 1 bits from mask flipped.

**Input:**
- `v: var T`
- `mask: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with all the 1 bits from mask flipped.

Effectively maps to a [bitxor](#bitxor.m,T,T,varargs[T]) operation.

### flipMask

[ref: #symbol-flipmask]

Mutates v, with all the 1 bits in the range of slice flipped.

**Input:**
- `v: var T`
- `slice: Slice[int]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with all the 1 bits in the range of slice flipped.

Effectively maps to a [bitxor](#bitxor.m,T,T,varargs[T]) operation.

### flipMasked

[ref: #symbol-flipmasked]

Returns v, with all the 1 bits from mask flipped.

**Input:**
- `v: T`
- `mask: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns v, with all the 1 bits from mask flipped.

Effectively maps to a [bitxor](#bitxor.m,T,T,varargs[T]) operation.

### flipMasked

[ref: #symbol-flipmasked]

Returns v, with all the 1 bits in the range of slice flipped.

**Input:**
- `v: T`
- `slice: Slice[int]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns v, with all the 1 bits in the range of slice flipped.

Effectively maps to a [bitxor](#bitxor.m,T,T,varargs[T]) operation.

### mask

[ref: #symbol-mask]

Mutates v, with only the 1 bits from mask matching those of v set to 1.

**Input:**
- `v: var T`
- `mask: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with only the 1 bits from mask matching those of v set to 1.

Effectively maps to a [bitand](#bitand.m,T,T,varargs[T]) operation.

### mask

[ref: #symbol-mask]

Mutates v, with only the 1 bits in the range of slice matching those of v set to 1.

**Input:**
- `v: var T`
- `slice: Slice[int]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with only the 1 bits in the range of slice matching those of v set to 1.

Effectively maps to a [bitand](#bitand.m,T,T,varargs[T]) operation.

### masked

[ref: #symbol-masked]

Returns v, with only the 1 bits from mask matching those of v set to 1.

**Input:**
- `v: T`
- `mask: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns v, with only the 1 bits from mask matching those of v set to 1.

Effectively maps to a [bitand](#bitand.m,T,T,varargs[T]) operation.

### masked

[ref: #symbol-masked]

Returns v, with only the 1 bits in the range of slice matching those of v set to 1.

**Input:**
- `v: T`
- `slice: Slice[int]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns v, with only the 1 bits in the range of slice matching those of v set to 1.

Effectively maps to a [bitand](#bitand.m,T,T,varargs[T]) operation.

### parityBits

[ref: #symbol-paritybits]

**Input:**
- `x: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `inline`

Calculate the bit parity in an integer. If the number of 1-bits is odd, the parity is 1, otherwise 0.

### popcount

[ref: #symbol-popcount]

**Input:**
- `x: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `inline`

Alias for [countSetBits](#countSetBits,SomeInteger) (Hamming weight).

### reverseBits

[ref: #symbol-reversebits]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Return the bit reversal of x.

### rotateLeftBits

[ref: #symbol-rotateleftbits]

**Input:**
- `value: T`
- `shift: range[0 .. (sizeof(T) * 8)]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Left-rotate bits in a value.

### rotateRightBits

[ref: #symbol-rotaterightbits]

**Input:**
- `value: T`
- `shift: range[0 .. (sizeof(T) * 8)]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Right-rotate bits in a value.

### setBit

[ref: #symbol-setbit]

**Input:**
- `v: var T`
- `bit: BitsRange[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with the bit at position bit set to 1.

### setMask

[ref: #symbol-setmask]

Mutates v, with all the 1 bits from mask set to 1.

**Input:**
- `v: var T`
- `mask: T`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with all the 1 bits from mask set to 1.

Effectively maps to a [bitor](#bitor.m,T,T,varargs[T]) operation.

### setMask

[ref: #symbol-setmask]

Mutates v, with all the 1 bits in the range of slice set to 1.

**Input:**
- `v: var T`
- `slice: Slice[int]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

Mutates v, with all the 1 bits in the range of slice set to 1.

Effectively maps to a [bitor](#bitor.m,T,T,varargs[T]) operation.

### setMasked

[ref: #symbol-setmasked]

Returns v, with all the 1 bits from mask set to 1.

**Input:**
- `v: T`
- `mask: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns v, with all the 1 bits from mask set to 1.

Effectively maps to a [bitor](#bitor.m,T,T,varargs[T]) operation.

### setMasked

[ref: #symbol-setmasked]

Returns v, with all the 1 bits in the range of slice set to 1.

**Input:**
- `v: T`
- `slice: Slice[int]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns v, with all the 1 bits in the range of slice set to 1.

Effectively maps to a [bitor](#bitor.m,T,T,varargs[T]) operation.

### testBit

[ref: #symbol-testbit]

**Input:**
- `v: T`
- `bit: BitsRange[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns true if the bit in v at positions bit is set to 1.

### toMask

[ref: #symbol-tomask]

**Input:**
- `slice: Slice[int]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Creates a bitmask based on a slice of bits.

## Type

### BitsRange

[ref: #symbol-bitsrange]

```nim
BitsRange[T] = range[0 .. sizeof(T) * 8 - 1]
```

A range with all bit positions for type T.
