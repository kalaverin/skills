---
source_hash: 2b5206e98babb20c
source_path: lib/pure/math.nim
---

# math

[ref: #module-math]

*Constructive mathematics is naturally typed.* -- Simon Thompson

Basic math routines for Nim.

Note that the trigonometric functions naturally operate on radians. The helper functions [degToRad](#degToRad,T) and [radToDeg](#radToDeg,T) provide conversion between radians and degrees.

This module is available for the [JavaScript target](backends.html#backends-the-javascript-target).

# [See also](#see-also)

* [complex module](complex.html) for complex numbers and their mathematical operations
* [rationals module](rationals.html) for rational numbers and their mathematical operations
* [fenv module](fenv.html) for handling of floating-point rounding and exceptions (overflow, zero-divide, etc.)
* [random module](random.html) for a fast and tiny random number generator
* [stats module](stats.html) for statistical analysis
* [strformat module](strformat.html) for formatting floats for printing
* [system module](system.html) for some very basic and trivial math operators (shr, shl, xor, clamp, etc.)

this func uses bitwise comparisons from C compilers, which are not always available.

## Examples

```nim
import std/math
from std/fenv import epsilon
from std/random import rand

proc generateGaussianNoise(mu: float = 0.0, sigma: float = 1.0): (float, float) =
  # Generates values from a normal distribution.
  # Translated from https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform#Implementation.
  var u1: float
  var u2: float
  while true:
    u1 = rand(1.0)
    u2 = rand(1.0)
    if u1 > epsilon(float): break
  let mag = sigma * sqrt(-2 * ln(u1))
  let z0 = mag * cos(2 * PI * u2) + mu
  let z1 = mag * sin(2 * PI * u2) + mu
  (z0, z1)

echo generateGaussianNoise()
```

```nim
doAssert almostEqual(5.5 ^ 2.2, 42.540042248725975)
doAssert 1.0 ^ Inf == 1.0
```

```nim
doAssert -3 ^ 0 == 1
doAssert -3 ^ 1 == -3
doAssert -3 ^ 2 == 9
```

```nim
doAssert almostEqual(PI, 3.14159265358979)
doAssert almostEqual(Inf, Inf)
doAssert not almostEqual(NaN, NaN)
```

```nim
doAssert almostEqual(radToDeg(arccos(0.0)), 90.0)
doAssert almostEqual(radToDeg(arccos(1.0)), 0.0)
```

```nim
doAssert almostEqual(radToDeg(arcsin(0.0)), 0.0)
doAssert almostEqual(radToDeg(arcsin(1.0)), 90.0)
```

```nim
doAssert almostEqual(arctan(1.0), 0.7853981633974483)
doAssert almostEqual(radToDeg(arctan(1.0)), 45.0)
```

```nim
doAssert almostEqual(arctan2(1.0, 0.0), PI / 2.0)
doAssert almostEqual(radToDeg(arctan2(1.0, 0.0)), 90.0)
```

```nim
doAssert binom(6, 2) == 15
doAssert binom(-6, 2) == 1
doAssert binom(6, 0) == 1
```

```nim
doAssert almostEqual(cbrt(8.0), 2.0)
doAssert almostEqual(cbrt(2.197), 1.3)
doAssert almostEqual(cbrt(-27.0), -3.0)
```

```nim
doAssert ceil(2.1)  == 3.0
doAssert ceil(2.9)  == 3.0
doAssert ceil(-2.1) == -2.0
```

```nim
assert ceilDiv(12, 3) ==  4
assert ceilDiv(13, 3) ==  5
```

```nim
assert clamp(10, 1 .. 5) == 5
assert clamp(1, 1 .. 3) == 1
type A = enum a0, a1, a2, a3, a4, a5
assert a1.clamp(a2..a4) == a2
assert clamp((3, 0), (1, 0) .. (2, 9)) == (2, 9)
doAssertRaises(AssertionDefect): discard clamp(1, 3..2) # invalid bounds
```

```nim
doAssert classify(0.3) == fcNormal
doAssert classify(0.0) == fcZero
doAssert classify(0.3 / 0.0) == fcInf
doAssert classify(-0.3 / 0.0) == fcNegInf
doAssert classify(5.0e-324) == fcSubnormal
```

```nim
doAssert copySign(10.0, 1.0) == 10.0
doAssert copySign(10.0, -1.0) == -10.0
doAssert copySign(-Inf, -0.0) == -Inf
doAssert copySign(NaN, 1.0).isNaN
doAssert copySign(1.0, copySign(NaN, -1.0)) == -1.0
```

```nim
doAssert almostEqual(cos(2 * PI), 1.0)
doAssert almostEqual(cos(degToRad(60.0)), 0.5)
```

```nim
doAssert almostEqual(cosh(0.0), 1.0)
doAssert almostEqual(cosh(1.0), 1.543080634815244)
```

```nim
var a = [1, 2, 3, 4]
cumprod(a)
doAssert a == @[1, 2, 6, 24]
```

```nim
let a = [1, 2, 3, 4]
doAssert cumproded(a) == @[1, 2, 6, 24]
```

```nim
var a = [1, 2, 3, 4]
cumsum(a)
doAssert a == @[1, 3, 6, 10]
```

```nim
doAssert cumsummed([1, 2, 3, 4]) == @[1, 3, 6, 10]
```

```nim
doAssert almostEqual(degToRad(180.0), PI)
```

```nim
doAssert divmod(5, 2) == (2, 1)
doAssert divmod(5, -3) == (-1, 2)
```

```nim
doAssert euclDiv(13, 3) == 4
doAssert euclDiv(-13, 3) == -5
doAssert euclDiv(13, -3) == -4
doAssert euclDiv(-13, -3) == 5
```

```nim
doAssert euclMod(13, 3) == 1
doAssert euclMod(-13, 3) == 2
doAssert euclMod(13, -3) == 1
doAssert euclMod(-13, -3) == 2
```

```nim
doAssert almostEqual(exp(1.0), E)
doAssert almostEqual(ln(exp(4.0)), 4.0)
doAssert almostEqual(exp(0.0), 1.0)
```

```nim
doAssert fac(0) == 1
doAssert fac(4) == 24
doAssert fac(10) == 3628800
```

```nim
doAssert floor(2.1)  == 2.0
doAssert floor(2.9)  == 2.0
doAssert floor(-3.5) == -4.0
```

```nim
doAssert floorDiv( 13,  3) ==  4
doAssert floorDiv(-13,  3) == -5
doAssert floorDiv( 13, -3) == -5
doAssert floorDiv(-13, -3) ==  4
```

```nim
doAssert floorMod( 13,  3) ==  1
doAssert floorMod(-13,  3) ==  2
doAssert floorMod( 13, -3) == -2
doAssert floorMod(-13, -3) == -1
```

```nim
doAssert frexp(8.0) == (0.5, 4)
doAssert frexp(-8.0) == (-0.5, 4)
doAssert frexp(0.0) == (0.0, 0)

# special cases:
when sizeof(int) == 8:
  doAssert frexp(-0.0).frac.signbit # signbit preserved for +-0
  doAssert frexp(Inf).frac == Inf # +- Inf preserved
  doAssert frexp(NaN).frac.isNaN
```

```nim
var x: int
doAssert frexp(5.0, x) == 0.625
doAssert x == 3
```

```nim
doAssert almostEqual(gamma(1.0), 1.0)
doAssert almostEqual(gamma(4.0), 6.0)
doAssert almostEqual(gamma(11.0), 3628800.0)
```

```nim
doAssert gcd(12, 8) == 4
doAssert gcd(17, 63) == 1
```

```nim
doAssert gcd(13.5, 9.0) == 4.5
```

```nim
doAssert gcd(@[13.5, 9.0]) == 4.5
```

```nim
doAssert almostEqual(hypot(3.0, 4.0), 5.0)
```

```nim
doAssert NaN.isNaN
doAssert not Inf.isNaN
doAssert not isNaN(3.1415926)
```

```nim
doAssert isPowerOfTwo(16)
doAssert not isPowerOfTwo(5)
doAssert not isPowerOfTwo(0)
doAssert not isPowerOfTwo(-16)
```

```nim
doAssert lcm(24, 30) == 120
doAssert lcm(13, 39) == 39
```

```nim
doAssert lcm(@[24, 30]) == 120
```

```nim
doAssert almostEqual(ln(exp(4.0)), 4.0)
doAssert almostEqual(ln(1.0), 0.0)
doAssert almostEqual(ln(0.0), -Inf)
doAssert ln(-7.0).isNaN
```

```nim
doAssert almostEqual(log(9.0, 3.0), 2.0)
doAssert almostEqual(log(0.0, 2.0), -Inf)
doAssert log(-7.0, 4.0).isNaN
doAssert log(8.0, -2.0).isNaN
```

```nim
doAssert almostEqual(log2(8.0), 3.0)
doAssert almostEqual(log2(1.0), 0.0)
doAssert almostEqual(log2(0.0), -Inf)
doAssert log2(-2.0).isNaN
```

```nim
doAssert almostEqual(log10(100.0) , 2.0)
doAssert almostEqual(log10(0.0), -Inf)
doAssert log10(-100.0).isNaN
```

```nim
doAssert  6.5 mod  2.5 ==  1.5
doAssert -6.5 mod  2.5 == -1.5
doAssert  6.5 mod -2.5 ==  1.5
doAssert -6.5 mod -2.5 == -1.5
```

```nim
doAssert nextPowerOfTwo(16) == 16
doAssert nextPowerOfTwo(5) == 8
doAssert nextPowerOfTwo(0) == 1
doAssert nextPowerOfTwo(-16) == 1
```

```nim
doAssert almostEqual(pow(100, 1.5), 1000.0)
doAssert almostEqual(pow(16.0, 0.5), 4.0)
```

```nim
doAssert prod([1, 2, 3, 4]) == 24
doAssert prod([-4, 3, 5]) == -60
```

```nim
doAssert almostEqual(radToDeg(2 * PI), 360.0)
```

```nim
doAssert round(3.4) == 3.0
doAssert round(3.5) == 4.0
doAssert round(4.5) == 5.0
```

```nim
doAssert round(PI, 2) == 3.14
doAssert round(PI, 4) == 3.1416
```

```nim
doAssert sgn(5) == 1
doAssert sgn(0) == 0
doAssert sgn(-4.1) == -1
```

```nim
doAssert not signbit(0.0)
doAssert signbit(-0.0)
doAssert signbit(-0.1)
doAssert not signbit(0.1)
```

```nim
doAssert almostEqual(sin(PI / 6), 0.5)
doAssert almostEqual(sin(degToRad(90.0)), 1.0)
```

```nim
doAssert almostEqual(sinh(0.0), 0.0)
doAssert almostEqual(sinh(1.0), 1.175201193643801)
```

```nim
doAssert splitDecimal(5.25) == (intpart: 5.0, floatpart: 0.25)
doAssert splitDecimal(-2.73) == (intpart: -2.0, floatpart: -0.73)
```

```nim
doAssert almostEqual(sqrt(4.0), 2.0)
doAssert almostEqual(sqrt(1.44), 1.2)
```

```nim
doAssert sum([1, 2, 3, 4]) == 10
doAssert sum([-4, 3, 5]) == 4
```

```nim
doAssert almostEqual(tan(degToRad(45.0)), 1.0)
doAssert almostEqual(tan(PI / 4), 1.0)
```

```nim
doAssert almostEqual(tanh(0.0), 0.0)
doAssert almostEqual(tanh(1.0), 0.7615941559557649)
```

```nim
doAssert trunc(PI) == 3.0
doAssert trunc(-1.85) == -1.0
```

## Const

### E

[ref: #symbol-e]

```nim
E = 2.718281828459045
```

Euler's number.

### MaxFloat32Precision

[ref: #symbol-maxfloat32precision]

```nim
MaxFloat32Precision = 8
```

Maximum number of meaningful digits after the decimal point for Nim's float32 type.

### MaxFloat64Precision

[ref: #symbol-maxfloat64precision]

```nim
MaxFloat64Precision = 16
```

Maximum number of meaningful digits after the decimal point for Nim's float64 type.

### MaxFloatPrecision

[ref: #symbol-maxfloatprecision]

```nim
MaxFloatPrecision = 16
```

Maximum number of meaningful digits after the decimal point for Nim's float type.

### MinFloatNormal

[ref: #symbol-minfloatnormal]

```nim
MinFloatNormal = 2.225073858507201e-308
```

Smallest normal number for Nim's float type (= 2^-1022).

### PI

[ref: #symbol-pi]

```nim
PI = 3.141592653589793
```

The circle constant PI (Ludolph's number).

### TAU

[ref: #symbol-tau]

```nim
TAU = 6.283185307179586
```

The circle constant TAU (= 2 \* PI).

## Proc

### `^`

[ref: #symbol-]

Computes x to the power of y.

**Input:**
- `x: T`
- `y: Natural`

**Output:** `T`
**Generic parameters:** `T`

Computes x to the power of y.

The exponent y must be non-negative, use [pow](#pow,float64,float64) for negative exponents.

**See also:**

* [^ func](#^,T,U) for negative exponent or floats
* [pow func](#pow,float64,float64) for float32 or float64 output
* [sqrt func](#sqrt,float64)
* [cbrt func](#cbrt,float64)

### `^`

[ref: #symbol-]

Computes x to the power of y.

**Input:**
- `x: T`
- `y: U`

**Output:** `float`
**Generic parameters:** `T`, `U`

Computes x to the power of y.

Error handling follows the C++ specification even for the JS backend <https://en.cppreference.com/w/cpp/numeric/math/pow>

**See also:**

* [^ func](#^,T,Natural)
* [pow func](#pow,float64,float64) for float32 or float64 output
* [sqrt func](#sqrt,float64)
* [cbrt func](#cbrt,float64)

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `importc: "fmodf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `mod`

[ref: #symbol-mod]

Computes the modulo operation for float values (the remainder of x divided by y).

**Input:**
- `x: float64`
- `y: float64`

**Output:** `float64`
**Pragmas:** `importc: "fmod"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the modulo operation for float values (the remainder of x divided by y).

**See also:**

* [floorMod func](#floorMod,T,T) for Python-like (% operator) behavior

### almostEqual

[ref: #symbol-almostequal]

Checks if two float values are almost equal, using the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon).

**Input:**
- `x: T`
- `y: T`
- `unitsInLastPlace: Natural = 4`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`

Checks if two float values are almost equal, using the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon).

unitsInLastPlace is the max number of [units in the last place](https://en.wikipedia.org/wiki/Unit_in_the_last_place) difference tolerated when comparing two numbers. The larger the value, the more error is allowed. A 0 value means that two numbers must be exactly the same to be considered equal.

The machine epsilon has to be scaled to the magnitude of the values used and multiplied by the desired precision in ULPs unless the difference is subnormal.

### arccos

[ref: #symbol-arccos]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "acosf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### arccos

[ref: #symbol-arccos]

Computes the arc cosine of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "acos"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the arc cosine of x.

**See also:**

* [cos func](#cos,float64)

### arccosh

[ref: #symbol-arccosh]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "acoshf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### arccosh

[ref: #symbol-arccosh]

Computes the inverse hyperbolic cosine of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "acosh"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the inverse hyperbolic cosine of x.

**See also:**

* [cosh func](#cosh,float64)

### arccot

[ref: #symbol-arccot]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the inverse cotangent of x (arctan(1/x)).

### arccoth

[ref: #symbol-arccoth]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the inverse hyperbolic cotangent of x (arctanh(1/x)).

### arccsc

[ref: #symbol-arccsc]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the inverse cosecant of x (arcsin(1/x)).

### arccsch

[ref: #symbol-arccsch]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the inverse hyperbolic cosecant of x (arcsinh(1/x)).

### arcsec

[ref: #symbol-arcsec]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the inverse secant of x (arccos(1/x)).

### arcsech

[ref: #symbol-arcsech]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the inverse hyperbolic secant of x (arccosh(1/x)).

### arcsin

[ref: #symbol-arcsin]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "asinf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### arcsin

[ref: #symbol-arcsin]

Computes the arc sine of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "asin"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the arc sine of x.

**See also:**

* [sin func](#sin,float64)

### arcsinh

[ref: #symbol-arcsinh]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "asinhf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### arcsinh

[ref: #symbol-arcsinh]

Computes the inverse hyperbolic sine of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "asinh"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the inverse hyperbolic sine of x.

**See also:**

* [sinh func](#sinh,float64)

### arctan

[ref: #symbol-arctan]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "atanf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### arctan

[ref: #symbol-arctan]

Calculate the arc tangent of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "atan"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Calculate the arc tangent of x.

**See also:**

* [arctan2 func](#arctan2,float64,float64)
* [tan func](#tan,float64)

### arctan2

[ref: #symbol-arctan2]

**Input:**
- `y: float32`
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "atan2f"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### arctan2

[ref: #symbol-arctan2]

Calculate the arc tangent of y/x.

**Input:**
- `y: float64`
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "atan2"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Calculate the arc tangent of y/x.

It produces correct results even when the resulting angle is near PI/2 or -PI/2 (x near 0).

**See also:**

* [arctan func](#arctan,float64)

### arctanh

[ref: #symbol-arctanh]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "atanhf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### arctanh

[ref: #symbol-arctanh]

Computes the inverse hyperbolic tangent of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "atanh"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the inverse hyperbolic tangent of x.

**See also:**

* [tanh func](#tanh,float64)

### binom

[ref: #symbol-binom]

**Input:**
- `n: int`
- `k: int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the [binomial coefficient](https://en.wikipedia.org/wiki/Binomial_coefficient).

### cbrt

[ref: #symbol-cbrt]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "cbrtf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cbrt

[ref: #symbol-cbrt]

Computes the cube root of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "cbrt"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the cube root of x.

**See also:**

* [sqrt func](#sqrt,float64) for the square root

### ceil

[ref: #symbol-ceil]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "ceilf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ceil

[ref: #symbol-ceil]

Computes the ceiling function (i.e. the smallest integer not smaller than x).

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "ceil"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the ceiling function (i.e. the smallest integer not smaller than x).

**See also:**

* [floor func](#floor,float64)
* [round func](#round,float64)
* [trunc func](#trunc,float64)

### ceilDiv

[ref: #symbol-ceildiv]

Ceil division is conceptually defined as ceil(x / y).

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Ceil division is conceptually defined as ceil(x / y).

Assumes x >= 0 and y > 0 (and x + y - 1 <= high(T) if T is SomeUnsignedInt).

This is different from the [system.div](system.html#div,int,int) operator, which works like trunc(x / y). That is, div rounds towards 0 and ceilDiv rounds up.

This function has the above input limitation, because that allows the compiler to generate faster code and it is rarely used with negative values or unsigned integers close to high(T)/2. If you need a ceilDiv that works with any input, see: <https://github.com/demotomohiro/divmath>.

**See also:**

* [system.div proc](system.html#div,int,int) for integer division
* [floorDiv func](#floorDiv,T,T) for integer division which rounds down.


[Next](math_2.md)
