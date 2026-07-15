---
source_hash: eb7d02e2f6abea83
source_path: lib/pure/complex.nim
---

# complex

[ref: #module-complex]

This module implements complex numbers and basic mathematical operations on them.

Complex numbers are currently generic over 64-bit or 32-bit floats.

## Examples

```nim
import std/complex
from std/math import almostEqual, sqrt

let
  z1 = complex(1.0, 2.0)
  z2 = complex(3.0, -4.0)

assert almostEqual(z1 + z2, complex(4.0, -2.0))
assert almostEqual(z1 - z2, complex(-2.0, 6.0))
assert almostEqual(z1 * z2, complex(11.0, 2.0))
assert almostEqual(z1 / z2, complex(-0.2, 0.4))

assert almostEqual(abs(z1), sqrt(5.0))
assert almostEqual(conjugate(z1), complex(1.0, -2.0))

let (r, phi) = z1.polar
assert almostEqual(rect(r, phi), z1)
```

```nim
doAssert $complex(1.0, 2.0) == "(1.0, 2.0)"
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `z: Complex`

**Output:** `string`
**Generic parameters:** `Complex`

Returns z's string representation as "(re, im)".

### `*=`

[ref: #symbol-]

**Input:**
- `x: var Complex[T]`
- `y: Complex[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Multiplies x by y.

### `*`

[ref: #symbol-]

**Input:**
- `x: T`
- `y: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Multiplies a real number with a complex number.

### `*`

[ref: #symbol-]

**Input:**
- `x: Complex[T]`
- `y: T`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Multiplies a complex number with a real number.

### `*`

[ref: #symbol-]

**Input:**
- `x: Complex[T]`
- `y: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Multiplies two complex numbers.

### `+=`

[ref: #symbol-]

**Input:**
- `x: var Complex[T]`
- `y: Complex[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Adds y to x.

### `+`

[ref: #symbol-]

**Input:**
- `x: T`
- `y: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Adds a real number to a complex number.

### `+`

[ref: #symbol-]

**Input:**
- `x: Complex[T]`
- `y: T`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Adds a complex number to a real number.

### `+`

[ref: #symbol-]

**Input:**
- `x: Complex[T]`
- `y: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Adds two complex numbers.

### `-=`

[ref: #symbol-]

**Input:**
- `x: var Complex[T]`
- `y: Complex[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Subtracts y from x.

### `-`

[ref: #symbol-]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Unary minus for complex numbers.

### `-`

[ref: #symbol-]

**Input:**
- `x: T`
- `y: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Subtracts a complex number from a real number.

### `-`

[ref: #symbol-]

**Input:**
- `x: Complex[T]`
- `y: T`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Subtracts a real number from a complex number.

### `-`

[ref: #symbol-]

**Input:**
- `x: Complex[T]`
- `y: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Subtracts two complex numbers.

### `/=`

[ref: #symbol-]

**Input:**
- `x: var Complex[T]`
- `y: Complex[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Divides x by y in place.

### `/`

[ref: #symbol-]

**Input:**
- `x: Complex[T]`
- `y: T`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Divides a complex number by a real number.

### `/`

[ref: #symbol-]

**Input:**
- `x: T`
- `y: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Divides a real number by a complex number.

### `/`

[ref: #symbol-]

**Input:**
- `x: Complex[T]`
- `y: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Divides two complex numbers.

### `==`

[ref: #symbol-]

**Input:**
- `x: Complex[T]`
- `y: Complex[T]`

**Output:** `bool`
**Generic parameters:** `T`

Compares two complex numbers for equality.

### abs

[ref: #symbol-abs]

**Input:**
- `z: Complex[T]`

**Output:** `T`
**Generic parameters:** `T`

Returns the absolute value of z, that is the distance from (0, 0) to z.

### abs2

[ref: #symbol-abs2]

**Input:**
- `z: Complex[T]`

**Output:** `T`
**Generic parameters:** `T`

Returns the squared absolute value of z, that is the squared distance from (0, 0) to z. This is more efficient than abs(z) ^ 2.

### almostEqual

[ref: #symbol-almostequal]

Checks if two complex values are almost equal, using the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon).

**Input:**
- `x: Complex[T]`
- `y: Complex[T]`
- `unitsInLastPlace: Natural = 4`

**Output:** `bool`
**Generic parameters:** `T`

Checks if two complex values are almost equal, using the [machine epsilon](https://en.wikipedia.org/wiki/Machine_epsilon).

Two complex values are considered almost equal if their real and imaginary components are almost equal.

unitsInLastPlace is the max number of [units in the last place](https://en.wikipedia.org/wiki/Unit_in_the_last_place) difference tolerated when comparing two numbers. The larger the value, the more error is allowed. A 0 value means that two numbers must be exactly the same to be considered equal.

The machine epsilon has to be scaled to the magnitude of the values used and multiplied by the desired precision in ULPs unless the difference is subnormal.

### arccos

[ref: #symbol-arccos]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse cosine of z.

### arccosh

[ref: #symbol-arccosh]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse hyperbolic cosine of z.

### arccot

[ref: #symbol-arccot]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse cotangent of z.

### arccoth

[ref: #symbol-arccoth]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse hyperbolic cotangent of z.

### arccsc

[ref: #symbol-arccsc]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse cosecant of z.

### arccsch

[ref: #symbol-arccsch]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse hyperbolic cosecant of z.

### arcsec

[ref: #symbol-arcsec]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse secant of z.

### arcsech

[ref: #symbol-arcsech]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse hyperbolic secant of z.

### arcsin

[ref: #symbol-arcsin]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse sine of z.

### arcsinh

[ref: #symbol-arcsinh]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse hyperbolic sine of z.

### arctan

[ref: #symbol-arctan]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse tangent of z.

### arctanh

[ref: #symbol-arctanh]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the inverse hyperbolic tangent of z.

### complex

[ref: #symbol-complex]

**Input:**
- `re: T`
- `im: T = 0.0`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns a Complex[T] with real part re and imaginary part im.

### complex32

[ref: #symbol-complex32]

**Input:**
- `re: float32`
- `im: float32 = 0.0`

**Output:** `Complex32`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a Complex32 with real part re and imaginary part im.

### complex64

[ref: #symbol-complex64]

**Input:**
- `re: float64`
- `im: float64 = 0.0`

**Output:** `Complex64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a Complex64 with real part re and imaginary part im.

### conjugate

[ref: #symbol-conjugate]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the complex conjugate of z (complex(z.re, -z.im)).

### cos

[ref: #symbol-cos]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the cosine of z.

### cosh

[ref: #symbol-cosh]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the hyperbolic cosine of z.

### cot

[ref: #symbol-cot]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the cotangent of z.

### coth

[ref: #symbol-coth]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the hyperbolic cotangent of z.

### csc

[ref: #symbol-csc]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the cosecant of z.

### csch

[ref: #symbol-csch]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the hyperbolic cosecant of z.

### exp

[ref: #symbol-exp]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Computes the exponential function (e^z).

### formatValue

[ref: #symbol-formatvalue]

**Input:**
- `result: var string`
- `value: Complex`
- `specifier: string`

**Output:** *(none)*
**Generic parameters:** `Complex`

Standard format implementation for Complex. It makes little sense to call this directly, but it is required to exist by the & macro. For complex numbers, we add a specific 'j' specifier, which formats the value as (A+Bj) like in mathematics.

### inv

[ref: #symbol-inv]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the multiplicative inverse of z (1/z).

### ln

[ref: #symbol-ln]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the ([principal value](https://en.wikipedia.org/wiki/Complex_logarithm#Principal_value) of the) natural logarithm of z.

### log10

[ref: #symbol-log10]

Returns the logarithm base 10 of z.

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the logarithm base 10 of z.

**See also:**

* [ln func](#ln,Complex[T])

### log2

[ref: #symbol-log2]

Returns the logarithm base 2 of z.

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the logarithm base 2 of z.

**See also:**

* [ln func](#ln,Complex[T])

### phase

[ref: #symbol-phase]

Returns the phase (or argument) of z, that is the angle in polar representation.

**Input:**
- `z: Complex[T]`

**Output:** `T`
**Generic parameters:** `T`

Returns the phase (or argument) of z, that is the angle in polar representation.

result = arctan2(z.im, z.re)

### polar

[ref: #symbol-polar]

Returns z in polar coordinates.

**Input:**
- `z: Complex[T]`

**Output:** `tuple[r, phi: T]`
**Generic parameters:** `T`

Returns z in polar coordinates.

result.r = abs(z)  
result.phi = phase(z)

**See also:**

* [rect func](#rect,T,T) for the inverse operation

### pow

[ref: #symbol-pow]

**Input:**
- `x: Complex[T]`
- `y: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

x raised to the power of y.

### pow

[ref: #symbol-pow]

**Input:**
- `x: Complex[T]`
- `y: T`

**Output:** `Complex[T]`
**Generic parameters:** `T`

The complex number x raised to the power of the real number y.

### rect

[ref: #symbol-rect]

Returns the complex number with polar coordinates r and phi.

**Input:**
- `r: T`
- `phi: T`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the complex number with polar coordinates r and phi.

result.re = r \* cos(phi)  
result.im = r \* sin(phi)

**See also:**

* [polar func](#polar,Complex[T]) for the inverse operation

### sec

[ref: #symbol-sec]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the secant of z.

### sech

[ref: #symbol-sech]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the hyperbolic secant of z.

### sgn

[ref: #symbol-sgn]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the phase of z as a unit complex number, or 0 if z is 0.

### sin

[ref: #symbol-sin]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the sine of z.

### sinh

[ref: #symbol-sinh]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the hyperbolic sine of z.

### sqrt

[ref: #symbol-sqrt]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Computes the ([principal](https://en.wikipedia.org/wiki/Square_root#Principal_square_root_of_a_complex_number)) square root of a complex number z.

### tan

[ref: #symbol-tan]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the tangent of z.

### tanh

[ref: #symbol-tanh]

**Input:**
- `z: Complex[T]`

**Output:** `Complex[T]`
**Generic parameters:** `T`

Returns the hyperbolic tangent of z.

## Template

### im

[ref: #symbol-im]

**Input:**
- `arg: typedesc[float32]`

**Output:** `Complex32`
**Generic parameters:** `arg:type`

Returns the imaginary unit (complex32(0, 1)).

### im

[ref: #symbol-im]

**Input:**
- `arg: typedesc[float64]`

**Output:** `Complex64`
**Generic parameters:** `arg:type`

Returns the imaginary unit (complex64(0, 1)).

### im

[ref: #symbol-im]

**Input:**
- `arg: float32`

**Output:** `Complex32`
Returns arg as an imaginary number (complex32(0, arg)).

### im

[ref: #symbol-im]

**Input:**
- `arg: float64`

**Output:** `Complex64`
Returns arg as an imaginary number (complex64(0, arg)).

## Type

### Complex

[ref: #symbol-complex]

```nim
Complex[T] = object
  re*, im*: T
```

A complex number, consisting of a real and an imaginary part.

### Complex32

[ref: #symbol-complex32]

```nim
Complex32 = Complex[float32]
```

Alias for a complex number using 32-bit floats.

### Complex64

[ref: #symbol-complex64]

```nim
Complex64 = Complex[float64]
```

Alias for a complex number using 64-bit floats.
