---
source_hash: 5c879c5b6aa93b9f
source_path: lib/std/logic.nim
---

# logic

[ref: #module-logic]

This module provides further logic operators like 'forall' and 'exists' They are only supported in .ensures etc pragmas.

## Proc

### `&lt;-&gt;`

[ref: #symbol-lt-gt]

**Input:**
- `a: bool`
- `b: bool`

**Output:** `bool`
**Pragmas:** `magic: "Iff"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-&gt;`

[ref: #symbol-gt]

**Input:**
- `a: bool`
- `b: bool`

**Output:** `bool`
**Pragmas:** `magic: "Implies"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### exists

[ref: #symbol-exists]

**Input:**
- `args: varargs[untyped]`

**Output:** `bool`
**Pragmas:** `magic: "Exists"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### forall

[ref: #symbol-forall]

**Input:**
- `args: varargs[untyped]`

**Output:** `bool`
**Pragmas:** `magic: "Forall"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### old

[ref: #symbol-old]

**Input:**
- `x: T`

**Output:** `T`
**Generic parameters:** `T`

**Pragmas:** `magic: "Old"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `
