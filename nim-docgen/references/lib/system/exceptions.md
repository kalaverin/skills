---
source_hash: 6699e1e818c4e949
source_path: lib/system/exceptions.nim
---

# exceptions

[ref: #module-exceptions]

Exception and effect types used in Nim code.

## Type

### AccessViolationDefect

[ref: #symbol-accessviolationdefect]

```nim
AccessViolationDefect = object of Defect
```

Raised for invalid memory access errors

### AccessViolationError

[ref: #symbol-accessviolationerror]

```nim
AccessViolationError {.deprecated: "See corresponding Defect".} = AccessViolationDefect
```

### ArithmeticDefect

[ref: #symbol-arithmeticdefect]

```nim
ArithmeticDefect = object of Defect
```

Raised if any kind of arithmetic error occurred.

### ArithmeticError

[ref: #symbol-arithmeticerror]

```nim
ArithmeticError {.deprecated: "See corresponding Defect".} = ArithmeticDefect
```

### AssertionDefect

[ref: #symbol-assertiondefect]

Raised when assertion is proved wrong.

```nim
AssertionDefect = object of Defect
```

Raised when assertion is proved wrong.

Usually the result of using the [assert() template](assertions.html#assert.t,untyped,string).

### AssertionError

[ref: #symbol-assertionerror]

```nim
AssertionError {.deprecated: "See corresponding Defect".} = AssertionDefect
```

### DeadThreadDefect

[ref: #symbol-deadthreaddefect]

```nim
DeadThreadDefect = object of Defect
```

Raised if it is attempted to send a message to a dead thread.

### DeadThreadError

[ref: #symbol-deadthreaderror]

```nim
DeadThreadError {.deprecated: "See corresponding Defect".} = DeadThreadDefect
```

### DivByZeroDefect

[ref: #symbol-divbyzerodefect]

```nim
DivByZeroDefect = object of ArithmeticDefect
```

Raised for runtime integer divide-by-zero errors.

### DivByZeroError

[ref: #symbol-divbyzeroerror]

```nim
DivByZeroError {.deprecated: "See corresponding Defect".} = DivByZeroDefect
```

### EOFError

[ref: #symbol-eoferror]

```nim
EOFError = object of IOError
```

Raised if an IO "end of file" error occurred.

### ExecIOEffect

[ref: #symbol-execioeffect]

```nim
ExecIOEffect = object of IOEffect
```

Effect describing an executing IO operation.

### FieldDefect

[ref: #symbol-fielddefect]

```nim
FieldDefect = object of Defect
```

Raised if a record field is not accessible because its discriminant's value does not fit.

### FieldError

[ref: #symbol-fielderror]

```nim
FieldError {.deprecated: "See corresponding Defect".} = FieldDefect
```

### FloatDivByZeroDefect

[ref: #symbol-floatdivbyzerodefect]

Raised by division by zero.

```nim
FloatDivByZeroDefect = object of FloatingPointDefect
```

Raised by division by zero.

Divisor is zero and dividend is a finite nonzero number.

### FloatDivByZeroError

[ref: #symbol-floatdivbyzeroerror]

```nim
FloatDivByZeroError {.deprecated: "See corresponding Defect".} = FloatDivByZeroDefect
```

### FloatInexactDefect

[ref: #symbol-floatinexactdefect]

Raised for inexact results.

```nim
FloatInexactDefect = object of FloatingPointDefect
```

Raised for inexact results.

The operation produced a result that cannot be represented with infinite precision -- for example: 2.0 / 3.0, log(1.1)

**Note**: Nim currently does not detect these!

### FloatInexactError

[ref: #symbol-floatinexacterror]

```nim
FloatInexactError {.deprecated: "See corresponding Defect".} = FloatInexactDefect
```

### FloatingPointDefect

[ref: #symbol-floatingpointdefect]

```nim
FloatingPointDefect = object of Defect
```

Base class for floating point exceptions.

### FloatingPointError

[ref: #symbol-floatingpointerror]

```nim
FloatingPointError {.deprecated: "See corresponding Defect".} = FloatingPointDefect
```

### FloatInvalidOpDefect

[ref: #symbol-floatinvalidopdefect]

Raised by invalid operations according to IEEE.

```nim
FloatInvalidOpDefect = object of FloatingPointDefect
```

Raised by invalid operations according to IEEE.

Raised by 0.0/0.0, for example.

### FloatInvalidOpError

[ref: #symbol-floatinvalidoperror]

```nim
FloatInvalidOpError {.deprecated: "See corresponding Defect".} = FloatInvalidOpDefect
```

### FloatOverflowDefect

[ref: #symbol-floatoverflowdefect]

Raised for overflows.

```nim
FloatOverflowDefect = object of FloatingPointDefect
```

Raised for overflows.

The operation produced a result that exceeds the range of the exponent.

### FloatOverflowError

[ref: #symbol-floatoverflowerror]

```nim
FloatOverflowError {.deprecated: "See corresponding Defect".} = FloatOverflowDefect
```

### FloatUnderflowDefect

[ref: #symbol-floatunderflowdefect]

Raised for underflows.

```nim
FloatUnderflowDefect = object of FloatingPointDefect
```

Raised for underflows.

The operation produced a result that is too small to be represented as a normal number.

### FloatUnderflowError

[ref: #symbol-floatunderflowerror]

```nim
FloatUnderflowError {.deprecated: "See corresponding Defect".} = FloatUnderflowDefect
```

### IndexDefect

[ref: #symbol-indexdefect]

```nim
IndexDefect = object of Defect
```

Raised if an array index is out of bounds.

### IndexError

[ref: #symbol-indexerror]

```nim
IndexError {.deprecated: "See corresponding Defect".} = IndexDefect
```

### IOEffect

[ref: #symbol-ioeffect]

```nim
IOEffect = object of RootEffect
```

IO effect.

### IOError

[ref: #symbol-ioerror]

```nim
IOError = object of CatchableError
```

Raised if an IO error occurred.

### KeyError

[ref: #symbol-keyerror]

Raised if a key cannot be found in a table.

```nim
KeyError = object of ValueError
```

Raised if a key cannot be found in a table.

Mostly used by the [tables](tables.html) module, it can also be raised by other collection modules like [sets](sets.html) or [strtabs](strtabs.html).

### LibraryError

[ref: #symbol-libraryerror]

```nim
LibraryError = object of OSError
```

Raised if a dynamic library could not be loaded.

### NilAccessDefect

[ref: #symbol-nilaccessdefect]

Raised on dereferences of nil pointers.

```nim
NilAccessDefect = object of Defect
```

Raised on dereferences of nil pointers.

This is only raised if the [segfaults module](segfaults.html) was imported!

### NilAccessError

[ref: #symbol-nilaccesserror]

```nim
NilAccessError {.deprecated: "See corresponding Defect".} = NilAccessDefect
```

### ObjectAssignmentDefect

[ref: #symbol-objectassignmentdefect]

```nim
ObjectAssignmentDefect = object of Defect
```

Raised if an object gets assigned to its parent's object.

### ObjectAssignmentError

[ref: #symbol-objectassignmenterror]

```nim
ObjectAssignmentError {.deprecated: "See corresponding Defect".} = ObjectAssignmentDefect
```

### ObjectConversionDefect

[ref: #symbol-objectconversiondefect]

```nim
ObjectConversionDefect = object of Defect
```

Raised if an object is converted to an incompatible object type. You can use of operator to check if conversion will succeed.

### ObjectConversionError

[ref: #symbol-objectconversionerror]

```nim
ObjectConversionError {.deprecated: "See corresponding Defect".} = ObjectConversionDefect
```

### OSError

[ref: #symbol-oserror]

```nim
OSError = object of CatchableError
  errorCode*: int32          ## OS-defined error code describing this error.
```

Raised if an operating system service failed.

### OutOfMemDefect

[ref: #symbol-outofmemdefect]

```nim
OutOfMemDefect = object of Defect
```

Raised for unsuccessful attempts to allocate memory.

### OutOfMemError

[ref: #symbol-outofmemerror]

```nim
OutOfMemError {.deprecated: "See corresponding Defect".} = OutOfMemDefect
```

### OverflowDefect

[ref: #symbol-overflowdefect]

Raised for runtime integer overflows.

```nim
OverflowDefect = object of ArithmeticDefect
```

Raised for runtime integer overflows.

This happens for calculations whose results are too large to fit in the provided bits.

### OverflowError

[ref: #symbol-overflowerror]

```nim
OverflowError {.deprecated: "See corresponding Defect".} = OverflowDefect
```

### RangeDefect

[ref: #symbol-rangedefect]

```nim
RangeDefect = object of Defect
```

Raised if a range check error occurred.

### RangeError

[ref: #symbol-rangeerror]

```nim
RangeError {.deprecated: "See corresponding Defect".} = RangeDefect
```

### ReadIOEffect

[ref: #symbol-readioeffect]

```nim
ReadIOEffect = object of IOEffect
```

Effect describing a read IO operation.

### ReraiseDefect

[ref: #symbol-reraisedefect]

```nim
ReraiseDefect = object of Defect
```

Raised if there is no exception to reraise.

### ReraiseError

[ref: #symbol-reraiseerror]

```nim
ReraiseError {.deprecated: "See corresponding Defect".} = ReraiseDefect
```

### ResourceExhaustedError

[ref: #symbol-resourceexhaustederror]

```nim
ResourceExhaustedError = object of CatchableError
```

Raised if a resource request could not be fulfilled.

### StackOverflowDefect

[ref: #symbol-stackoverflowdefect]

```nim
StackOverflowDefect = object of Defect
```

Raised if the hardware stack used for subroutine calls overflowed.

### StackOverflowError

[ref: #symbol-stackoverflowerror]

```nim
StackOverflowError {.deprecated: "See corresponding Defect".} = StackOverflowDefect
```

### TimeEffect

[ref: #symbol-timeeffect]

```nim
TimeEffect = object of RootEffect
```

Time effect.

### ValueError

[ref: #symbol-valueerror]

```nim
ValueError = object of CatchableError
```

Raised for string and object conversion errors.

### WriteIOEffect

[ref: #symbol-writeioeffect]

```nim
WriteIOEffect = object of IOEffect
```

Effect describing a write IO operation.
