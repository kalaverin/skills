---
source_hash: e9548362291e48fd
source_path: lib/std/isolation.nim
---

# isolation

[ref: #module-isolation]

This module implements the Isolated[T] type for safe construction of isolated subgraphs that can be passed efficiently to different channels and threads.

**Warning:**
This module is experimental and its interface may change.

## Proc

### `=copy`

[ref: #symbol-copy]

**Input:**
- `dest: var Isolated[T]`
- `src: Isolated[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `error`

### `=destroy`

[ref: #symbol-destroy]

**Input:**
- `dest: var Isolated[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`, `raises: []`

**Effects:** `raises: `

### `=sink`

[ref: #symbol-sink]

**Input:**
- `dest: var Isolated[T]`
- `src: Isolated[T]`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `inline`

### extract

[ref: #symbol-extract]

**Input:**
- `src: var Isolated[T]`

**Output:** `T`
**Generic parameters:** `T`

Returns the internal value of src. The value is moved from src.

### isolate

[ref: #symbol-isolate]

Creates an isolated subgraph from the expression value. Isolation is checked at compile time.

**Input:**
- `value: sink T`

**Output:** `Isolated[T]`
**Generic parameters:** `T`

**Pragmas:** `magic: "Isolate"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates an isolated subgraph from the expression value. Isolation is checked at compile time.

Please read <https://github.com/nim-lang/RFCs/issues/244> for more details.

### unsafeIsolate

[ref: #symbol-unsafeisolate]

Creates an isolated subgraph from the expression value.

**Input:**
- `value: sink T`

**Output:** `Isolated[T]`
**Generic parameters:** `T`

Creates an isolated subgraph from the expression value.

**Warning:**
The proc doesn't check whether value is isolated.

## Type

### Isolated

[ref: #symbol-isolated]

```nim
Isolated[T] {.sendable.} = object
```

Isolated data can only be moved, not copied.
