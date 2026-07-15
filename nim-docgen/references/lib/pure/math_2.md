---
source_hash: 2b5206e98babb20c
source_path: lib/pure/math.nim
---

### clamp

[ref: #symbol-clamp]

**Input:**
- `val: T`
- `bounds: Slice[T]`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Like system.clamp, but takes a slice, so you can easily clamp within a range.

### classify

[ref: #symbol-classify]

Classifies a floating point value.

**Input:**
- `x: float`

**Output:** `FloatClass`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Classifies a floating point value.

Returns x's class as specified by the [FloatClass enum](#FloatClass).

### copySign

[ref: #symbol-copysign]

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns a value with the magnitude of x and the sign of y; this works even if x or y are NaN, infinity or zero, all of which can carry a sign.

### cos

[ref: #symbol-cos]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "cosf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cos

[ref: #symbol-cos]

Computes the cosine of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "cos"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the cosine of x.

**See also:**

* [arccos func](#arccos,float64)

### cosh

[ref: #symbol-cosh]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "coshf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cosh

[ref: #symbol-cosh]

Computes the [hyperbolic cosine](https://en.wikipedia.org/wiki/Hyperbolic_function#Definitions) of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "cosh"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the [hyperbolic cosine](https://en.wikipedia.org/wiki/Hyperbolic_function#Definitions) of x.

**See also:**

* [arccosh func](#arccosh,float64)

### cot

[ref: #symbol-cot]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the cotangent of x (1/tan(x)).

### coth

[ref: #symbol-coth]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the hyperbolic cotangent of x (1/tanh(x)).

### csc

[ref: #symbol-csc]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the cosecant of x (1/sin(x)).

### csch

[ref: #symbol-csch]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the hyperbolic cosecant of x (1/sinh(x)).

### cumprod

[ref: #symbol-cumprod]

Transforms x in-place (must be declared as var) into its product.

**Input:**
- `x: var openArray[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Transforms x in-place (must be declared as var) into its product.

See also:

* [prod proc](#sum,openArray[T])
* [cumproded proc](#cumproded,openArray[T]) for a version which returns cumproded sequence

### cumproded

[ref: #symbol-cumproded]

Return cumulative (aka prefix) product of x.

**Input:**
- `x: openArray[T]`

**Output:** `seq[T]`
**Generic parameters:** `T`

Return cumulative (aka prefix) product of x.

See also:

* [prod proc](#prod,openArray[T])
* [cumprod proc](#cumprod,openArray[T]) for the in-place version

### cumsum

[ref: #symbol-cumsum]

Transforms x in-place (must be declared as var) into its cumulative (aka prefix) summation.

**Input:**
- `x: var openArray[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Transforms x in-place (must be declared as var) into its cumulative (aka prefix) summation.

**See also:**

* [sum func](#sum,openArray[T])
* [cumsummed func](#cumsummed,openArray[T]) for a version which returns a cumsummed sequence

### cumsummed

[ref: #symbol-cumsummed]

Returns the cumulative (aka prefix) summation of x.

**Input:**
- `x: openArray[T]`

**Output:** `seq[T]`
**Generic parameters:** `T`

Returns the cumulative (aka prefix) summation of x.

If x is empty, @[] is returned.

**See also:**

* [sum func](#sum,openArray[T])
* [cumsum func](#cumsum,openArray[T]) for the in-place version

### degToRad

[ref: #symbol-degtorad]

Converts from degrees to radians.

**Input:**
- `d: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Converts from degrees to radians.

**See also:**

* [radToDeg func](#radToDeg,T)

### divmod

[ref: #symbol-divmod]

**Input:**
- `x: T`
- `y: T`

**Output:** `(T, T)`
**Generic parameters:** `T`

**Pragmas:** `inline`

Specialized instructions for computing both division and modulus. Return structure is: (quotient, remainder)

### erf

[ref: #symbol-erf]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "erff"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### erf

[ref: #symbol-erf]

Computes the [error function](https://en.wikipedia.org/wiki/Error_function) for x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "erf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the [error function](https://en.wikipedia.org/wiki/Error_function) for x.

**Note:** Not available for the JS backend.

### erfc

[ref: #symbol-erfc]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "erfcf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### erfc

[ref: #symbol-erfc]

Computes the [complementary error function](https://en.wikipedia.org/wiki/Error_function#Complementary_error_function) for x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "erfc"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the [complementary error function](https://en.wikipedia.org/wiki/Error_function#Complementary_error_function) for x.

**Note:** Not available for the JS backend.

### euclDiv

[ref: #symbol-eucldiv]

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

Returns euclidean division of x by y.

### euclMod

[ref: #symbol-euclmod]

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

Returns euclidean modulo of x by y. euclMod(x, y) is non-negative.

### exp

[ref: #symbol-exp]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "expf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### exp

[ref: #symbol-exp]

Computes the exponential function of x (e^x).

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "exp"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the exponential function of x (e^x).

**See also:**

* [ln func](#ln,float64)

### fac

[ref: #symbol-fac]

Computes the [factorial](https://en.wikipedia.org/wiki/Factorial) of a non-negative integer n.

**Input:**
- `n: int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the [factorial](https://en.wikipedia.org/wiki/Factorial) of a non-negative integer n.

**See also:**

* [prod func](#prod,openArray[T])

### floor

[ref: #symbol-floor]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "floorf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### floor

[ref: #symbol-floor]

Computes the floor function (i.e. the largest integer not greater than x).

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "floor"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the floor function (i.e. the largest integer not greater than x).

**See also:**

* [ceil func](#ceil,float64)
* [round func](#round,float64)
* [trunc func](#trunc,float64)

### floorDiv

[ref: #symbol-floordiv]

Floor division is conceptually defined as floor(x / y).

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

Floor division is conceptually defined as floor(x / y).

This is different from the [system.div](system.html#div,int,int) operator, which is defined as trunc(x / y). That is, div rounds towards 0 and floorDiv rounds down.

**See also:**

* [system.div proc](system.html#div,int,int) for integer division
* [floorMod func](#floorMod,T,T) for Python-like (% operator) behavior

### floorMod

[ref: #symbol-floormod]

Floor modulo is conceptually defined as x - (floorDiv(x, y) \* y).

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

Floor modulo is conceptually defined as x - (floorDiv(x, y) \* y).

This func behaves the same as the % operator in Python.

**See also:**

* [mod func](#mod,float64,float64)
* [floorDiv func](#floorDiv,T,T)

### frexp

[ref: #symbol-frexp]

**Input:**
- `x: T`

**Output:** `tuple[frac: T, exp: int]`
**Generic parameters:** `T`

**Pragmas:** `inline`

Splits x into a normalized fraction frac and an integral power of 2 exp, such that abs(frac) in 0.5..<1 and x == frac \* 2 ^ exp, except for special cases shown below.

### frexp

[ref: #symbol-frexp]

**Input:**
- `x: T`
- `exponent: var int`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Overload of frexp that calls (result, exponent) = frexp(x).

### gamma

[ref: #symbol-gamma]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "tgammaf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gamma

[ref: #symbol-gamma]

Computes the [gamma function](https://en.wikipedia.org/wiki/Gamma_function) for x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "tgamma"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the [gamma function](https://en.wikipedia.org/wiki/Gamma_function) for x.

**Note:** Not available for the JS backend.

**See also:**

* [lgamma func](#lgamma,float64) for the natural logarithm of the gamma function

### gcd

[ref: #symbol-gcd]

Computes the greatest common (positive) divisor of x and y.

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the greatest common (positive) divisor of x and y.

Note that for floats, the result cannot always be interpreted as "greatest decimal z such that z\*N == x and z\*M == y where N and M are positive integers".

**See also:**

* [gcd func](#gcd,SomeInteger,SomeInteger) for an integer version
* [lcm func](#lcm,T,T)

### gcd

[ref: #symbol-gcd]

Computes the greatest common (positive) divisor of x and y, using the binary GCD (aka Stein's) algorithm.

**Input:**
- `x: SomeInteger`
- `y: SomeInteger`

**Output:** `SomeInteger`
**Generic parameters:** `SomeInteger`

Computes the greatest common (positive) divisor of x and y, using the binary GCD (aka Stein's) algorithm.

**See also:**

* [gcd func](#gcd,T,T) for a float version
* [lcm func](#lcm,T,T)

### gcd

[ref: #symbol-gcd]

Computes the greatest common (positive) divisor of the elements of x.

**Input:**
- `x: openArray[T]`

**Output:** `T`
**Generic parameters:** `T`

Computes the greatest common (positive) divisor of the elements of x.

**See also:**

* [gcd func](#gcd,T,T) for a version with two arguments

### hypot

[ref: #symbol-hypot]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `importc: "hypotf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### hypot

[ref: #symbol-hypot]

**Input:**
- `x: float64`
- `y: float64`

**Output:** `float64`
**Pragmas:** `importc: "hypot"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the length of the hypotenuse of a right-angle triangle with x as its base and y as its height. Equivalent to sqrt(x\*x + y\*y).

### isNaN

[ref: #symbol-isnan]

**Input:**
- `x: SomeFloat`

**Output:** `bool`
**Generic parameters:** `SomeFloat`

**Pragmas:** `inline`

Returns whether x is a NaN, more efficiently than via classify(x) == fcNan. Works even with --passc:-ffast-math.

### isPowerOfTwo

[ref: #symbol-ispoweroftwo]

Returns true, if x is a power of two, false otherwise.

**Input:**
- `x: int`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true, if x is a power of two, false otherwise.

Zero and negative numbers are not a power of two.

**See also:**

* [nextPowerOfTwo func](#nextPowerOfTwo,int)

### lcm

[ref: #symbol-lcm]

Computes the least common multiple of x and y.

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the least common multiple of x and y.

**See also:**

* [gcd func](#gcd,T,T)

### lcm

[ref: #symbol-lcm]

Computes the least common multiple of the elements of x.

**Input:**
- `x: openArray[T]`

**Output:** `T`
**Generic parameters:** `T`

Computes the least common multiple of the elements of x.

**See also:**

* [lcm func](#lcm,T,T) for a version with two arguments

### lgamma

[ref: #symbol-lgamma]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "lgammaf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### lgamma

[ref: #symbol-lgamma]

Computes the natural logarithm of the gamma function for x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "lgamma"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the natural logarithm of the gamma function for x.

**Note:** Not available for the JS backend.

**See also:**

* [gamma func](#gamma,float64) for gamma function

### ln

[ref: #symbol-ln]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "logf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ln

[ref: #symbol-ln]

Computes the [natural logarithm](https://en.wikipedia.org/wiki/Natural_logarithm) of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "log"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the [natural logarithm](https://en.wikipedia.org/wiki/Natural_logarithm) of x.

**See also:**

* [log func](#log,T,T)
* [log10 func](#log10,float64)
* [log2 func](#log2,float64)
* [exp func](#exp,float64)

### log

[ref: #symbol-log]

Computes the logarithm of x to base base.

**Input:**
- `x: T`
- `base: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the logarithm of x to base base.

**See also:**

* [ln func](#ln,float64)
* [log10 func](#log10,float64)
* [log2 func](#log2,float64)

### log10

[ref: #symbol-log10]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "log10f"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### log10

[ref: #symbol-log10]

Computes the common logarithm (base 10) of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "log10"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the common logarithm (base 10) of x.

**See also:**

* [ln func](#ln,float64)
* [log func](#log,T,T)
* [log2 func](#log2,float64)

### log2

[ref: #symbol-log2]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "log2f"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### log2

[ref: #symbol-log2]

Computes the binary logarithm (base 2) of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "log2"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the binary logarithm (base 2) of x.

**See also:**

* [log func](#log,T,T)
* [log10 func](#log10,float64)
* [ln func](#ln,float64)

### nextPowerOfTwo

[ref: #symbol-nextpoweroftwo]

Returns x rounded up to the nearest power of two.

**Input:**
- `x: int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns x rounded up to the nearest power of two.

Zero and negative numbers get rounded up to 1.

**See also:**

* [isPowerOfTwo func](#isPowerOfTwo,int)

### pow

[ref: #symbol-pow]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `importc: "powf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pow

[ref: #symbol-pow]

Computes x raised to the power of y.

**Input:**
- `x: float64`
- `y: float64`

**Output:** `float64`
**Pragmas:** `importc: "pow"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes x raised to the power of y.

You may use the [^ func](#^, T, U) instead.

**See also:**

* [^ (SomeNumber, Natural) func](#^,T,Natural)
* [^ (SomeNumber, SomeFloat) func](#^,T,U)
* [sqrt func](#sqrt,float64)
* [cbrt func](#cbrt,float64)

### prod

[ref: #symbol-prod]

Computes the product of the elements in x.

**Input:**
- `x: openArray[T]`

**Output:** `T`
**Generic parameters:** `T`

Computes the product of the elements in x.

If x is empty, 1 is returned.

**See also:**

* [sum func](#sum,openArray[T])
* [fac func](#fac,int)

### radToDeg

[ref: #symbol-radtodeg]

Converts from radians to degrees.

**Input:**
- `d: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Converts from radians to degrees.

**See also:**

* [degToRad func](#degToRad,T)

### round

[ref: #symbol-round]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "roundf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Prev](math_1.md) | [Next](math_3.md)
