---
source_hash: 1c7078c3c06dc29a
source_path: lib/std/exitprocs.nim
---

# exitprocs

[ref: #module-exitprocs]

This module allows adding hooks to program exit.

## Proc

### addExitProc

[ref: #symbol-addexitproc]

**Input:**
- `cl: proc () {.closure.}`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds/registers a quit procedure. Each call to addExitProc registers another quit procedure. They are executed on a last-in, first-out basis.

### addExitProc

[ref: #symbol-addexitproc]

**Input:**
- `cl: proc () {.noconv.}`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

overload for noconv procs.

### getProgramResult

[ref: #symbol-getprogramresult]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setProgramResult

[ref: #symbol-setprogramresult]

**Input:**
- `a: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `
