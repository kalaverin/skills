---
source_hash: 0fb2cbae4faf5a8b
source_path: lib/pure/rationals.nim
---

# rationals

[ref: #module-rationals]

This module implements rational numbers, consisting of a numerator and a denominator. The denominator can not be 0.

## Examples

```nim
import std/rationals
let
  r1 = 1 // 2
  r2 = -3 // 4

doAssert r1 + r2 == -1 // 4
doAssert r1 - r2 ==  5 // 4
doAssert r1 * r2 == -3 // 8
doAssert r1 / r2 == -2 // 3
```

```nim
doAssert $(1 // 2) == "1/2"
```

```nim
let x = 1 // 3 + 1 // 5
doAssert x == 8 // 15
```

```nim
doAssert (-3 // 5) ^ 0 == (1 // 1)
doAssert (-3 // 5) ^ 1 == (-3 // 5)
doAssert (-3 // 5) ^ 2 == (9 // 25)
doAssert (-3 // 5) ^ -2 == (25 // 9)
```

```nim
doAssert abs(1 // 2) == 1 // 2
doAssert abs(-1 // 2) == 1 // 2
```

```nim
var r = Rational[int](num: 2, den: 4) # 1/2
reduce(r)
doAssert r.num == 1
doAssert r.den == 2
```

```nim
let x = 1.2
doAssert x.toRational.toFloat == x
```

```nim
doAssert toRational(42) == 42 // 1
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `x: Rational[T]`

**Output:** `string`
**Generic parameters:** `T`

Turns a rational number into a string.

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: Rational`
- `y: Rational`

**Output:** `bool`
**Generic parameters:** `Rational`

Returns tue if x is less than or equal to y.

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: Rational`
- `y: Rational`

**Output:** `bool`
**Generic parameters:** `Rational`

Returns true if x is less than y.

### `*=`

[ref: #symbol-]

**Input:**
- `x: var Rational[T]`
- `y: Rational[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Multiplies the rational x by y in-place.

### `*=`

[ref: #symbol-]

**Input:**
- `x: var Rational[T]`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

Multiplies the rational x by the int y in-place.

### `*`

[ref: #symbol-]

**Input:**
- `x: Rational[T]`
- `y: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Multiplies two rational numbers.

### `*`

[ref: #symbol-]

**Input:**
- `x: Rational[T]`
- `y: T`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Multiplies the rational x with the int y.

### `*`

[ref: #symbol-]

**Input:**
- `x: T`
- `y: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Multiplies the int x with the rational y.

### `+=`

[ref: #symbol-]

**Input:**
- `x: var Rational[T]`
- `y: Rational[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Adds the rational y to the rational x in-place.

### `+=`

[ref: #symbol-]

**Input:**
- `x: var Rational[T]`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

Adds the int y to the rational x in-place.

### `+`

[ref: #symbol-]

**Input:**
- `x: Rational[T]`
- `y: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Adds two rational numbers.

### `+`

[ref: #symbol-]

**Input:**
- `x: Rational[T]`
- `y: T`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Adds the rational x to the int y.

### `+`

[ref: #symbol-]

**Input:**
- `x: T`
- `y: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Adds the int x to the rational y.

### `-=`

[ref: #symbol-]

**Input:**
- `x: var Rational[T]`
- `y: Rational[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Subtracts the rational y from the rational x in-place.

### `-=`

[ref: #symbol-]

**Input:**
- `x: var Rational[T]`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

Subtracts the int y from the rational x in-place.

### `-`

[ref: #symbol-]

**Input:**
- `x: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Unary minus for rational numbers.

### `-`

[ref: #symbol-]

**Input:**
- `x: Rational[T]`
- `y: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Subtracts two rational numbers.

### `-`

[ref: #symbol-]

**Input:**
- `x: Rational[T]`
- `y: T`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Subtracts the int y from the rational x.

### `-`

[ref: #symbol-]

**Input:**
- `x: T`
- `y: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Subtracts the rational y from the int x.

### `//`

[ref: #symbol-]

**Input:**
- `num: T`
- `den: T`

**Output:** `Rational[T]`
**Generic parameters:** `T`

A friendlier version of [initRational](#initRational,T,T).

### `/=`

[ref: #symbol-]

**Input:**
- `x: var Rational[T]`
- `y: Rational[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Divides the rational x by the rational y in-place.

### `/=`

[ref: #symbol-]

**Input:**
- `x: var Rational[T]`
- `y: T`

**Output:** *(none)*
**Generic parameters:** `T`

Divides the rational x by the int y in-place.

### `/`

[ref: #symbol-]

**Input:**
- `x: Rational[T]`
- `y: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Divides the rational x by the rational y.

### `/`

[ref: #symbol-]

**Input:**
- `x: Rational[T]`
- `y: T`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Divides the rational x by the int y.

### `/`

[ref: #symbol-]

**Input:**
- `x: T`
- `y: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Divides the int x by the rational y.

### `==`

[ref: #symbol-]

**Input:**
- `x: Rational`
- `y: Rational`

**Output:** `bool`
**Generic parameters:** `Rational`

Compares two rationals for equality.

### `^`

[ref: #symbol-]

Computes x to the power of y.

**Input:**
- `x: Rational[T]`
- `y: T`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Computes x to the power of y.

The exponent y must be an integer. Negative exponents are supported but floating point exponents are not.

### `div`

[ref: #symbol-div]

**Input:**
- `x: Rational[T]`
- `y: Rational[T]`

**Output:** `T`
**Generic parameters:** `T`

Computes the rational truncated division.

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: Rational[T]`
- `y: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Computes the rational modulo by truncated division (remainder). This is same as x - (x div y) \* y.

### abs

[ref: #symbol-abs]

**Input:**
- `x: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Returns the absolute value of x.

### cmp

[ref: #symbol-cmp]

Compares two rationals. Returns

**Input:**
- `x: Rational`
- `y: Rational`

**Output:** `int`
**Generic parameters:** `Rational`

Compares two rationals. Returns

* a value less than zero, if x < y
* a value greater than zero, if x > y
* zero, if x == y

### floorDiv

[ref: #symbol-floordiv]

Computes the rational floor division.

**Input:**
- `x: Rational[T]`
- `y: Rational[T]`

**Output:** `T`
**Generic parameters:** `T`

Computes the rational floor division.

Floor division is conceptually defined as floor(x / y). This is different from the div operator, which is defined as trunc(x / y). That is, div rounds towards 0 and floorDiv rounds down.

### floorMod

[ref: #symbol-floormod]

Computes the rational modulo by floor division (modulo).

**Input:**
- `x: Rational[T]`
- `y: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Computes the rational modulo by floor division (modulo).

This is same as x - floorDiv(x, y) \* y. This func behaves the same as the % operator in Python.

### hash

[ref: #symbol-hash]

**Input:**
- `x: Rational[T]`

**Output:** `Hash`
**Generic parameters:** `T`

Computes the hash for the rational x.

### initRational

[ref: #symbol-initrational]

Creates a new rational number with numerator num and denominator den. den must not be 0.

**Input:**
- `num: T`
- `den: T`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Creates a new rational number with numerator num and denominator den. den must not be 0.

**Note:** den != 0 is not checked when assertions are turned off.

### reciprocal

[ref: #symbol-reciprocal]

**Input:**
- `x: Rational[T]`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Calculates the reciprocal of x (1/x). If x is 0, raises DivByZeroDefect.

### reduce

[ref: #symbol-reduce]

Reduces the rational number x, so that the numerator and denominator have no common divisors other than 1 (and -1). If x is 0, raises DivByZeroDefect.

**Input:**
- `x: var Rational[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Reduces the rational number x, so that the numerator and denominator have no common divisors other than 1 (and -1). If x is 0, raises DivByZeroDefect.

**Note:** This is called automatically by the various operations on rationals.

### toFloat

[ref: #symbol-tofloat]

**Input:**
- `x: Rational[T]`

**Output:** `float`
**Generic parameters:** `T`

Converts a rational number x to a float.

### toInt

[ref: #symbol-toint]

**Input:**
- `x: Rational[T]`

**Output:** `int`
**Generic parameters:** `T`

Converts a rational number x to an int. Conversion rounds towards 0 if x does not contain an integer value.

### toRational

[ref: #symbol-torational]

**Input:**
- `x: T`

**Output:** `Rational[T]`
**Generic parameters:** `T`

Converts some integer x to a rational number.

### toRational

[ref: #symbol-torational]

Calculates the best rational approximation of x, where the denominator is smaller than n (default is the largest possible int for maximal resolution).

**Input:**
- `x: float`
- `n: int = high(int) shr 32`

**Output:** `Rational[int]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Calculates the best rational approximation of x, where the denominator is smaller than n (default is the largest possible int for maximal resolution).

The algorithm is based on the theory of continued fractions.

## Type

### Rational

[ref: #symbol-rational]

```nim
Rational[T] = object
  num*, den*: T
```

A rational number, consisting of a numerator num and a denominator den.
