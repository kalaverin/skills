---
source_hash: 3d5b83feeeb94364
source_path: lib/pure/fenv.nim
---

# fenv

[ref: #module-fenv]

Floating-point environment. Handling of floating-point rounding and exceptions (overflow, division by zero, etc.). The types, vars and procs are bindings for the C standard library [<fenv.h>](https://en.cppreference.com/w/c/numeric/fenv) header.

## Proc

### feclearexcept

[ref: #symbol-feclearexcept]

**Input:**
- `excepts: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Clear the supported exceptions represented by excepts.

### fegetenv

[ref: #symbol-fegetenv]

**Input:**
- `envp: ptr Tfenv`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Store the current floating-point environment in the object pointed to by envp.

### fegetexceptflag

[ref: #symbol-fegetexceptflag]

**Input:**
- `flagp: ptr Tfexcept`
- `excepts: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Store implementation-defined representation of the exception flags indicated by excepts in the object pointed to by flagp.

### fegetround

[ref: #symbol-fegetround]

**Input:**
- *(none)*

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get current rounding direction.

### feholdexcept

[ref: #symbol-feholdexcept]

**Input:**
- `envp: ptr Tfenv`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Save the current environment in the object pointed to by envp, clear exception flags and install a non-stop mode (if available) for all exceptions.

### feraiseexcept

[ref: #symbol-feraiseexcept]

**Input:**
- `excepts: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Raise the supported exceptions represented by excepts.

### fesetenv

[ref: #symbol-fesetenv]

**Input:**
- `a1: ptr Tfenv`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Establish the floating-point environment represented by the object pointed to by envp.

### fesetexceptflag

[ref: #symbol-fesetexceptflag]

**Input:**
- `flagp: ptr Tfexcept`
- `excepts: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set complete status for exceptions indicated by excepts according to the representation in the object pointed to by flagp.

### fesetround

[ref: #symbol-fesetround]

**Input:**
- `roundingDirection: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Establish the rounding direction represented by roundingDirection.

### fetestexcept

[ref: #symbol-fetestexcept]

**Input:**
- `excepts: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determine which of subset of the exceptions specified by excepts are currently set.

### feupdateenv

[ref: #symbol-feupdateenv]

**Input:**
- `envp: ptr Tfenv`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<fenv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Save current exceptions in temporary storage, install environment represented by object pointed to by envp and raise exceptions according to saved exceptions.

## Template

### digits

[ref: #symbol-digits]

**Input:**
- `T: typedesc[float32]`

**Output:** `int`
**Generic parameters:** `T:type`

Number of decimal digits that can be represented in a 32-bit floating-point type without losing precision.

### digits

[ref: #symbol-digits]

**Input:**
- `T: typedesc[float64]`

**Output:** `int`
**Generic parameters:** `T:type`

Number of decimal digits that can be represented in a 64-bit floating-point type without losing precision.

### epsilon

[ref: #symbol-epsilon]

**Input:**
- `T: typedesc[float32]`

**Output:** `float32`
**Generic parameters:** `T:type`

The difference between 1.0 and the smallest number greater than 1.0 that can be represented in a 32-bit floating-point type.

### epsilon

[ref: #symbol-epsilon]

**Input:**
- `T: typedesc[float64]`

**Output:** `float64`
**Generic parameters:** `T:type`

The difference between 1.0 and the smallest number greater than 1.0 that can be represented in a 64-bit floating-point type.

### fpRadix

[ref: #symbol-fpradix]

**Input:**
- *(none)*

**Output:** `int`
The (integer) value of the radix used to represent any floating point type on the architecture used to build the program.

### mantissaDigits

[ref: #symbol-mantissadigits]

**Input:**
- `T: typedesc[float32]`

**Output:** `int`
**Generic parameters:** `T:type`

Number of digits (in base floatingPointRadix) in the mantissa of 32-bit floating-point numbers.

### mantissaDigits

[ref: #symbol-mantissadigits]

**Input:**
- `T: typedesc[float64]`

**Output:** `int`
**Generic parameters:** `T:type`

Number of digits (in base floatingPointRadix) in the mantissa of 64-bit floating-point numbers.

### max10Exponent

[ref: #symbol-max10exponent]

**Input:**
- `T: typedesc[float32]`

**Output:** `int`
**Generic parameters:** `T:type`

Maximum (positive) exponent in base 10 for 32-bit floating-point numbers.

### max10Exponent

[ref: #symbol-max10exponent]

**Input:**
- `T: typedesc[float64]`

**Output:** `int`
**Generic parameters:** `T:type`

Maximum (positive) exponent in base 10 for 64-bit floating-point numbers.

### maxExponent

[ref: #symbol-maxexponent]

**Input:**
- `T: typedesc[float32]`

**Output:** `int`
**Generic parameters:** `T:type`

Maximum (positive) exponent for 32-bit floating-point numbers.

### maxExponent

[ref: #symbol-maxexponent]

**Input:**
- `T: typedesc[float64]`

**Output:** `int`
**Generic parameters:** `T:type`

Maximum (positive) exponent for 64-bit floating-point numbers.

### maximumPositiveValue

[ref: #symbol-maximumpositivevalue]

**Input:**
- `T: typedesc[float32]`

**Output:** `float32`
**Generic parameters:** `T:type`

The largest positive number that can be represented in a 32-bit floating-point type.

### maximumPositiveValue

[ref: #symbol-maximumpositivevalue]

**Input:**
- `T: typedesc[float64]`

**Output:** `float64`
**Generic parameters:** `T:type`

The largest positive number that can be represented in a 64-bit floating-point type.

### min10Exponent

[ref: #symbol-min10exponent]

**Input:**
- `T: typedesc[float32]`

**Output:** `int`
**Generic parameters:** `T:type`

Minimum (negative) exponent in base 10 for 32-bit floating-point numbers.

### min10Exponent

[ref: #symbol-min10exponent]

**Input:**
- `T: typedesc[float64]`

**Output:** `int`
**Generic parameters:** `T:type`

Minimum (negative) exponent in base 10 for 64-bit floating-point numbers.

### minExponent

[ref: #symbol-minexponent]

**Input:**
- `T: typedesc[float32]`

**Output:** `int`
**Generic parameters:** `T:type`

Minimum (negative) exponent for 32-bit floating-point numbers.

### minExponent

[ref: #symbol-minexponent]

**Input:**
- `T: typedesc[float64]`

**Output:** `int`
**Generic parameters:** `T:type`

Minimum (negative) exponent for 64-bit floating-point numbers.

### minimumPositiveValue

[ref: #symbol-minimumpositivevalue]

**Input:**
- `T: typedesc[float32]`

**Output:** `float32`
**Generic parameters:** `T:type`

The smallest positive (nonzero) number that can be represented in a 32-bit floating-point type.

### minimumPositiveValue

[ref: #symbol-minimumpositivevalue]

**Input:**
- `T: typedesc[float64]`

**Output:** `float64`
**Generic parameters:** `T:type`

The smallest positive (nonzero) number that can be represented in a 64-bit floating-point type.

## Type

### Tfenv

[ref: #symbol-tfenv]

```nim
Tfenv {.importc: "fenv_t", header: "<fenv.h>", final, pure.} = object
```

Represents the entire floating-point environment. The floating-point environment refers collectively to any floating-point status flags and control modes supported by the implementation.

### Tfexcept

[ref: #symbol-tfexcept]

```nim
Tfexcept {.importc: "fexcept_t", header: "<fenv.h>", final, pure.} = object
```

Represents the floating-point status flags collectively, including any status the implementation associates with the flags. A floating-point status flag is a system variable whose value is set (but never cleared) when a floating-point exception is raised, which occurs as a side effect of exceptional floating-point arithmetic to provide auxiliary information. A floating-point control mode is a system variable whose value may be set by the user to affect the subsequent behavior of floating-point arithmetic.

## Var

### FE_ALL_EXCEPT

[ref: #symbol-fe-all-except]

```nim
FE_ALL_EXCEPT {.importc, header: "<fenv.h>".}: cint
```

bitwise OR of all supported exceptions

### FE_DFL_ENV

[ref: #symbol-fe-dfl-env]

```nim
FE_DFL_ENV {.importc, header: "<fenv.h>".}: cint
```

macro of type pointer to fenv\_t to be used as the argument to functions taking an argument of type fenv\_t; in this case the default environment will be used

### FE_DIVBYZERO

[ref: #symbol-fe-divbyzero]

```nim
FE_DIVBYZERO {.importc, header: "<fenv.h>".}: cint
```

division by zero

### FE_DOWNWARD

[ref: #symbol-fe-downward]

```nim
FE_DOWNWARD {.importc, header: "<fenv.h>".}: cint
```

round toward -Inf

### FE_INEXACT

[ref: #symbol-fe-inexact]

```nim
FE_INEXACT {.importc, header: "<fenv.h>".}: cint
```

inexact result

### FE_INVALID

[ref: #symbol-fe-invalid]

```nim
FE_INVALID {.importc, header: "<fenv.h>".}: cint
```

invalid operation

### FE_OVERFLOW

[ref: #symbol-fe-overflow]

```nim
FE_OVERFLOW {.importc, header: "<fenv.h>".}: cint
```

result not representable due to overflow

### FE_TONEAREST

[ref: #symbol-fe-tonearest]

```nim
FE_TONEAREST {.importc, header: "<fenv.h>".}: cint
```

round to nearest

### FE_TOWARDZERO

[ref: #symbol-fe-towardzero]

```nim
FE_TOWARDZERO {.importc, header: "<fenv.h>".}: cint
```

round toward 0

### FE_UNDERFLOW

[ref: #symbol-fe-underflow]

```nim
FE_UNDERFLOW {.importc, header: "<fenv.h>".}: cint
```

result not representable due to underflow

### FE_UPWARD

[ref: #symbol-fe-upward]

```nim
FE_UPWARD {.importc, header: "<fenv.h>".}: cint
```

round toward +Inf
