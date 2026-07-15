---
source_hash: 64a68082d80164b4
source_path: lib/system/comparisons.nim
---

### `==`

[ref: #symbol-]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `bool`
**Pragmas:** `magic: "EqF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: float`
- `y: float`

**Output:** `bool`
**Pragmas:** `magic: "EqF64"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `x: array[I, T]`
- `y: array[I, T]`

**Output:** `bool`
**Generic parameters:** `I`, `T`

### `==`

[ref: #symbol-]

**Input:**
- `x: openArray[T]`
- `y: openArray[T]`

**Output:** `bool`
**Generic parameters:** `T`

### `==`

[ref: #symbol-]

**Input:**
- `x: seq[T]`
- `y: seq[T]`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Generic equals operator for sequences: relies on a equals operator for the element type T.

### clamp

[ref: #symbol-clamp]

Limits the value x within the interval [a, b]. This proc is equivalent to but faster than max(a, min(b, x)).

**Input:**
- `x: T`
- `a: T`
- `b: T`

**Output:** `T`
**Generic parameters:** `T`

Limits the value x within the interval [a, b]. This proc is equivalent to but faster than max(a, min(b, x)).

**Warning:**
a <= b is assumed and will not be checked (currently).

**See also:** math.clamp for a version that takes a Slice[T] instead.

### isNil

[ref: #symbol-isnil]

**Input:**
- `x: string`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `error: "\'isNil\' is invalid for \'string\'"`

### max

[ref: #symbol-max]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "MaxI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "MaxI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "MaxI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "MaxI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "MaxI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The maximum value of two integers.

### max

[ref: #symbol-max]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: float64`
- `y: float64`

**Output:** `float64`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### max

[ref: #symbol-max]

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Generic maximum operator of 2 values based on <=.

### max

[ref: #symbol-max]

**Input:**
- `x: openArray[T]`

**Output:** `T`
**Generic parameters:** `T`

The maximum value of x. T needs to have a < operator.

### min

[ref: #symbol-min]

**Input:**
- `x: int`
- `y: int`

**Output:** `int`
**Pragmas:** `magic: "MinI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: int8`
- `y: int8`

**Output:** `int8`
**Pragmas:** `magic: "MinI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: int16`
- `y: int16`

**Output:** `int16`
**Pragmas:** `magic: "MinI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: int32`
- `y: int32`

**Output:** `int32`
**Pragmas:** `magic: "MinI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: int64`
- `y: int64`

**Output:** `int64`
**Pragmas:** `magic: "MinI"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The minimum value of two integers.

### min

[ref: #symbol-min]

**Input:**
- `x: float32`
- `y: float32`

**Output:** `float32`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: float64`
- `y: float64`

**Output:** `float64`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### min

[ref: #symbol-min]

**Input:**
- `x: T`
- `y: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Generic minimum operator of 2 values based on <=.

### min

[ref: #symbol-min]

**Input:**
- `x: openArray[T]`

**Output:** `T`
**Generic parameters:** `T`

The minimum value of x. T needs to have a < operator.

## Template

### `!=`

[ref: #symbol-]

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
**Pragmas:** `callsite`

Unequals operator. This is a shorthand for not (x == y).

### `&gt;%`

[ref: #symbol-gt]

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
Treats x and y as unsigned and compares them. Returns true if unsigned(x) > unsigned(y).

### `&gt;=%`

[ref: #symbol-gt]

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
Treats x and y as unsigned and compares them. Returns true if unsigned(x) >= unsigned(y).

### `&gt;=`

[ref: #symbol-gt]

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
**Pragmas:** `callsite`

"is greater or equals" operator. This is the same as y <= x.

### `&gt;`

[ref: #symbol-gt]

**Input:**
- `x: untyped`
- `y: untyped`

**Output:** `untyped`
**Pragmas:** `callsite`

"is greater" operator. This is the same as y < x.

[Prev](comparisons_1.md)
