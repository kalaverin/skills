---
source_hash: 2b5206e98babb20c
source_path: lib/pure/math.nim
---

### round

[ref: #symbol-round]

Rounds a float to zero decimal places.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "round"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Rounds a float to zero decimal places.

Used internally by the [round func](#round,T,int) when the specified number of places is 0.

**See also:**

* [round func](#round,T,int) for rounding to the specific number of decimal places
* [floor func](#floor,float64)
* [ceil func](#ceil,float64)
* [trunc func](#trunc,float64)

### round

[ref: #symbol-round]

Decimal rounding on a binary floating point number.

**Input:**
- `x: T`
- `places: int`

**Output:** `T`
**Generic parameters:** `T`

Decimal rounding on a binary floating point number.

This function is NOT reliable. Floating point numbers cannot hold non integer decimals precisely. If places is 0 (or omitted), round to the nearest integral value following normal mathematical rounding rules (e.g. round(54.5) -> 55.0). If places is greater than 0, round to the given number of decimal places, e.g. round(54.346, 2) -> 54.350000000000001421…. If places is negative, round to the left of the decimal place, e.g. round(537.345, -1) -> 540.0.

### sec

[ref: #symbol-sec]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the secant of x (1/cos(x)).

### sech

[ref: #symbol-sech]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

Computes the hyperbolic secant of x (1/cosh(x)).

### sgn

[ref: #symbol-sgn]

Sign function.

**Input:**
- `x: T`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `inline`

Sign function.

Returns:

* -1 for negative numbers and NegInf,
* 1 for positive numbers and Inf,
* 0 for positive zero, negative zero and NaN

### signbit

[ref: #symbol-signbit]

**Input:**
- `x: SomeFloat`

**Output:** `bool`
**Generic parameters:** `SomeFloat`

**Pragmas:** `inline`

Returns true if x is negative, false otherwise.

### sin

[ref: #symbol-sin]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "sinf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sin

[ref: #symbol-sin]

Computes the sine of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "sin"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the sine of x.

**See also:**

* [arcsin func](#arcsin,float64)

### sinh

[ref: #symbol-sinh]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "sinhf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sinh

[ref: #symbol-sinh]

Computes the [hyperbolic sine](https://en.wikipedia.org/wiki/Hyperbolic_function#Definitions) of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "sinh"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the [hyperbolic sine](https://en.wikipedia.org/wiki/Hyperbolic_function#Definitions) of x.

**See also:**

* [arcsinh func](#arcsinh,float64)

### splitDecimal

[ref: #symbol-splitdecimal]

Breaks x into an integer and a fractional part.

**Input:**
- `x: T`

**Output:** `tuple[intpart: T, floatpart: T]`
**Generic parameters:** `T`

Breaks x into an integer and a fractional part.

Returns a tuple containing intpart and floatpart, representing the integer part and the fractional part, respectively.

Both parts have the same sign as x. Analogous to the modf function in C.

### sqrt

[ref: #symbol-sqrt]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "sqrtf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sqrt

[ref: #symbol-sqrt]

Computes the square root of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "sqrt"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the square root of x.

**See also:**

* [cbrt func](#cbrt,float64) for the cube root

### sum

[ref: #symbol-sum]

Computes the sum of the elements in x.

**Input:**
- `x: openArray[T]`

**Output:** `T`
**Generic parameters:** `T`

Computes the sum of the elements in x.

If x is empty, 0 is returned.

**See also:**

* [prod func](#prod,openArray[T])
* [cumsum func](#cumsum,openArray[T])
* [cumsummed func](#cumsummed,openArray[T])

### tan

[ref: #symbol-tan]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "tanf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tan

[ref: #symbol-tan]

Computes the tangent of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "tan"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the tangent of x.

**See also:**

* [arctan func](#arctan,float64)

### tanh

[ref: #symbol-tanh]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "tanhf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tanh

[ref: #symbol-tanh]

Computes the [hyperbolic tangent](https://en.wikipedia.org/wiki/Hyperbolic_function#Definitions) of x.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "tanh"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the [hyperbolic tangent](https://en.wikipedia.org/wiki/Hyperbolic_function#Definitions) of x.

**See also:**

* [arctanh func](#arctanh,float64)

### trunc

[ref: #symbol-trunc]

**Input:**
- `x: float32`

**Output:** `float32`
**Pragmas:** `importc: "truncf"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### trunc

[ref: #symbol-trunc]

Truncates x to the decimal point.

**Input:**
- `x: float64`

**Output:** `float64`
**Pragmas:** `importc: "trunc"`, `header: "<math.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Truncates x to the decimal point.

**See also:**

* [floor func](#floor,float64)
* [ceil func](#ceil,float64)
* [round func](#round,float64)

## Type

### FloatClass

[ref: #symbol-floatclass]

```nim
FloatClass = enum
  fcNormal,                 ## value is an ordinary nonzero floating point value
  fcSubnormal,              ## value is a subnormal (a very small) floating point value
  fcZero,                   ## value is zero
  fcNegZero,                ## value is the negative zero
  fcNan,                    ## value is Not a Number (NaN)
  fcInf,                    ## value is positive infinity
  fcNegInf                   ## value is negative infinity
```

Describes the class a floating point value belongs to. This is the type that is returned by the [classify func](#classify,float).

[Prev](math_2.md)
