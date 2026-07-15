---
source_hash: 7af115281a5fbb3b
source_path: lib/system/iterators_1.nim
---

# iterators_1

[ref: #module-iterators_1]

## Iterator

### `..&lt;`

[ref: #symbol-lt]

**Input:**
- `a: T`
- `b: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

### `..&lt;`

[ref: #symbol-lt]

**Input:**
- `a: int64`
- `b: int64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of ..< for convenience so that mixing integer types works better.

### `..&lt;`

[ref: #symbol-lt]

**Input:**
- `a: int32`
- `b: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of ..< for convenience so that mixing integer types works better.

### `..&lt;`

[ref: #symbol-lt]

**Input:**
- `a: uint64`
- `b: uint64`

**Output:** `uint64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of ..< for convenience so that mixing integer types works better.

### `..&lt;`

[ref: #symbol-lt]

**Input:**
- `a: uint32`
- `b: uint32`

**Output:** `uint32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of ..< for convenience so that mixing integer types works better.

### `..`

[ref: #symbol-]

An alias for countup(a, b, 1).

**Input:**
- `a: T`
- `b: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

An alias for countup(a, b, 1).

See also:

* [..<](#..<.i,T,T)

### `..`

[ref: #symbol-]

A type specialized version of .. for convenience so that mixing integer types works better.

**Input:**
- `a: int64`
- `b: int64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of .. for convenience so that mixing integer types works better.

See also:

* [..<](#..<.i,T,T)

### `..`

[ref: #symbol-]

A type specialized version of .. for convenience so that mixing integer types works better.

**Input:**
- `a: int32`
- `b: int32`

**Output:** `int32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of .. for convenience so that mixing integer types works better.

See also:

* [..<](#..<.i,T,T)

### `..`

[ref: #symbol-]

A type specialized version of .. for convenience so that mixing integer types works better.

**Input:**
- `a: uint64`
- `b: uint64`

**Output:** `uint64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of .. for convenience so that mixing integer types works better.

See also:

* [..<](#..<.i,T,T)

### `..`

[ref: #symbol-]

A type specialized version of .. for convenience so that mixing integer types works better.

**Input:**
- `a: uint32`
- `b: uint32`

**Output:** `uint32`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A type specialized version of .. for convenience so that mixing integer types works better.

See also:

* [..<](#..<.i,T,T)

### `||`

[ref: #symbol-]

OpenMP parallel loop iterator. Same as .. but the loop may run in parallel.

**Input:**
- `a: S`
- `b: T`
- `annotation: static string = "parallel for"`

**Output:** `T`
**Generic parameters:** `S`, `T`, `annotation:type`

**Pragmas:** `inline`, `magic: "OmpParFor"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

OpenMP parallel loop iterator. Same as .. but the loop may run in parallel.

annotation is an additional annotation for the code generator to use. The default annotation is parallel for. Please refer to the [OpenMP Syntax Reference](https://www.openmp.org/wp-content/uploads/OpenMP-4.5-1115-CPP-web.pdf) for further information.

Note that the compiler maps that to the #pragma omp parallel for construct of OpenMP and as such isn't aware of the parallelism in your code! Be careful! Later versions of || will get proper support by Nim's code generator and GC.

### `||`

[ref: #symbol-]

OpenMP parallel loop iterator with stepping.  Same as countup but the loop may run in parallel.

**Input:**
- `a: S`
- `b: T`
- `step: Positive`
- `annotation: static string = "parallel for"`

**Output:** `T`
**Generic parameters:** `S`, `T`, `annotation:type`

**Pragmas:** `inline`, `magic: "OmpParFor"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

OpenMP parallel loop iterator with stepping.  Same as countup but the loop may run in parallel.

annotation is an additional annotation for the code generator to use. The default annotation is parallel for. Please refer to the [OpenMP Syntax Reference](https://www.openmp.org/wp-content/uploads/OpenMP-4.5-1115-CPP-web.pdf) for further information.

Note that the compiler maps that to the #pragma omp parallel for construct of OpenMP and as such isn't aware of the parallelism in your code! Be careful! Later versions of || will get proper support by Nim's code generator and GC.

### countdown

[ref: #symbol-countdown]

Counts from ordinal value a down to b (inclusive) with the given step count.

**Input:**
- `a: T`
- `b: T`
- `step: Positive = 1`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Counts from ordinal value a down to b (inclusive) with the given step count.

T may be any ordinal type, step may only be positive.

**Note**: This fails to count to low(int) if T = int for efficiency reasons.

### countup

[ref: #symbol-countup]

Counts from ordinal value a to b (inclusive) with the given step count.

**Input:**
- `a: T`
- `b: T`
- `step: Positive = 1`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Counts from ordinal value a to b (inclusive) with the given step count.

T may be any ordinal type, step may only be positive.

**Note**: This fails to count to high(int) if T = int for efficiency reasons.
