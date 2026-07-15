---
source_hash: 55b03b42193d07cc
source_path: lib/std/private/dragonbox.nim
---

# dragonbox

[ref: #module-dragonbox]

Copyright 2020 Junekey Jeon Copyright 2020 Alexander Bolz

Distributed under the Boost Software License, Version 1.0. (See accompanying file LICENSE\_1\_0.txt or copy at <https://www.boost.org/LICENSE_1_0.txt>)

char\* output\_end = Dtoa(buffer, value);

Converts the given double-precision number into decimal form and stores the result in the given buffer.

The buffer must be large enough, i.e. >= DtoaMinBufferLength. The output format is similar to printf("%g"). The output is \_[not](#not) null-terminted.

The output is optimal, i.e. the output string

1. rounds back to the input number when read in (using round-to-nearest-even)
2. is as short as possible,
3. is as close to the input number as possible.

Note: This function may temporarily write up to DtoaMinBufferLength characters into the buffer.

This file contains an implementation of Junekey Jeon's Dragonbox algorithm.

It is a simplified version of the reference implementation found here: <https://github.com/jk-jeon/dragonbox>

The reference implementation also works with single-precision floating-point numbers and has options to configure the rounding mode.

namespace Returns floor(x / 2^n).

Technically, right-shift of negative integers is implementation defined... Should easily be optimized into SAR (or equivalent) instruction.

Returns whether value is divisible by 2^e2Returns whether value is divisible by 5^e5Returns (x \* y) / 2^128

## Const

### dtoaMinBufferLength

[ref: #symbol-dtoaminbufferlength]

```nim
dtoaMinBufferLength: cint = 64
```

### exponentBias

[ref: #symbol-exponentbias]

```nim
exponentBias: int32 = 1075'i32
```

### exponentMask

[ref: #symbol-exponentmask]

```nim
exponentMask: BitsType = 9218868437227405312'u64
```

### hiddenBit

[ref: #symbol-hiddenbit]

```nim
hiddenBit: BitsType = 4503599627370496'u64
```

### maxIeeeExponent

[ref: #symbol-maxieeeexponent]

```nim
maxIeeeExponent: BitsType = 2047'u
```

### significandMask

[ref: #symbol-significandmask]

```nim
significandMask: BitsType = 4503599627370495'u64
```

### significandSize

[ref: #symbol-significandsize]

```nim
significandSize: int32 = 53
```

### signMask

[ref: #symbol-signmask]

```nim
signMask: BitsType = 9223372036854775808'u64
```

## Proc

### computeDelta

[ref: #symbol-computedelta]

**Input:**
- `pow10: uint64x2`
- `betaMinus1: int32`

**Output:** `uint32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### computePow10

[ref: #symbol-computepow10]

**Input:**
- `k: int32`

**Output:** `uint64x2`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### constructDouble

[ref: #symbol-constructdouble]

**Input:**
- `bits: BitsType`

**Output:** `Double`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### constructDouble

[ref: #symbol-constructdouble]

**Input:**
- `value: ValueType`

**Output:** `Double`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### decimalLength

[ref: #symbol-decimallength]

**Input:**
- `v: uint64`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### floorDivPow2

[ref: #symbol-floordivpow2]

**Input:**
- `x: int32`
- `n: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### floorLog10Pow2

[ref: #symbol-floorlog10pow2]

**Input:**
- `e: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### floorLog10ThreeQuartersPow2

[ref: #symbol-floorlog10threequarterspow2]

**Input:**
- `e: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### floorLog2Pow10

[ref: #symbol-floorlog2pow10]

**Input:**
- `e: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### formatDigits

[ref: #symbol-formatdigits]

**Input:**
- `buffer: var openArray[char]`
- `pos: T`
- `digits: uint64`
- `decimalExponent: int`
- `forceTrailingDotZero:  = false`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `inline`

Prepare the buffer.

### hi32

[ref: #symbol-hi32]

**Input:**
- `x: uint64`

**Output:** `uint32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isFinite

[ref: #symbol-isfinite]

**Input:**
- `this: Double`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isInf

[ref: #symbol-isinf]

**Input:**
- `this: Double`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isIntegralEndpoint

[ref: #symbol-isintegralendpoint]

**Input:**
- `twoF: uint64`
- `e2: int32`
- `minusK: int32`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isIntegralMidpoint

[ref: #symbol-isintegralmidpoint]

**Input:**
- `twoF: uint64`
- `e2: int32`
- `minusK: int32`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isNaN

[ref: #symbol-isnan]

**Input:**
- `this: Double`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isZero

[ref: #symbol-iszero]

**Input:**
- `this: Double`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### lo32

[ref: #symbol-lo32]

**Input:**
- `x: uint64`

**Output:** `uint32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mul128

[ref: #symbol-mul128]

**Input:**
- `a: uint64`
- `b: uint64`

**Output:** `uint64x2`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mulParity

[ref: #symbol-mulparity]

**Input:**
- `twoF: uint64`
- `pow10: uint64x2`
- `betaMinus1: int32`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

1 mulx, 1 mul

### mulShift

[ref: #symbol-mulshift]

**Input:**
- `x: uint64`
- `y: uint64x2`

**Output:** `uint64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

2 mulx

### multipleOfPow2

[ref: #symbol-multipleofpow2]

**Input:**
- `value: uint64`
- `e2: int32`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### multipleOfPow5

[ref: #symbol-multipleofpow5]

**Input:**
- `value: uint64`
- `e5: int32`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### physicalExponent

[ref: #symbol-physicalexponent]

**Input:**
- `this: Double`

**Output:** `BitsType`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### physicalSignificand

[ref: #symbol-physicalsignificand]

**Input:**
- `this: Double`

**Output:** `BitsType`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### printDecimalDigitsBackwards

[ref: #symbol-printdecimaldigitsbackwards]

**Input:**
- `buf: var openArray[char]`
- `pos: int`
- `output64: uint64`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

number of trailing zeros removed.

### signBit

[ref: #symbol-signbit]

**Input:**
- `this: Double`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toChars

[ref: #symbol-tochars]

**Input:**
- `buffer: var openArray[char]`
- `v: float`
- `forceTrailingDotZero:  = false`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toDecimal64

[ref: #symbol-todecimal64]

**Input:**
- `ieeeSignificand: uint64`
- `ieeeExponent: uint64`

**Output:** `FloatingDecimal64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

10^(kappa + 1)

### toDecimal64AsymmetricInterval

[ref: #symbol-todecimal64asymmetricinterval]

**Input:**
- `e2: int32`

**Output:** `FloatingDecimal64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

NB: accept\_lower\_endpoint = true accept\_upper\_endpoint = true

### utoa8DigitsSkipTrailingZeros

[ref: #symbol-utoa8digitsskiptrailingzeros]

**Input:**
- `buf: var openArray[char]`
- `pos: int`
- `digits: uint32`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### dragonbox_Assert

[ref: #symbol-dragonbox-assert]

**Input:**
- `x: untyped`

**Output:** `untyped`
## Type

### BitsType

[ref: #symbol-bitstype]

```nim
BitsType = uint64
```

### Double

[ref: #symbol-double]

```nim
Double = object
  bits*: BitsType
```

### FloatingDecimal64

[ref: #symbol-floatingdecimal64]

```nim
FloatingDecimal64 {.bycopy.} = object
  significand*: uint64
  exponent*: int32
```

### uint64x2

[ref: #symbol-uint64x2]

```nim
uint64x2 {.bycopy.} = object
  hi*: uint64
  lo*: uint64
```

### ValueType

[ref: #symbol-valuetype]

```nim
ValueType = float
```
