---
source_hash: 3bd8799b1bc15999
source_path: lib/system/memory.nim
---

# memory

[ref: #module-memory]

## Proc

### nimCmpMem

[ref: #symbol-nimcmpmem]

**Input:**
- `a: pointer`
- `b: pointer`
- `size: Natural`

**Output:** `cint`
**Pragmas:** `nonReloadable`, `inline`, `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### nimCopyMem

[ref: #symbol-nimcopymem]

**Input:**
- `dest: pointer`
- `source: pointer`
- `size: Natural`

**Output:** *(none)*
**Pragmas:** `nonReloadable`, `inline`, `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### nimCStrLen

[ref: #symbol-nimcstrlen]

**Input:**
- `a: cstring`

**Output:** `int`
**Pragmas:** `nonReloadable`, `inline`, `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### nimSetMem

[ref: #symbol-nimsetmem]

**Input:**
- `a: pointer`
- `v: cint`
- `size: Natural`

**Output:** *(none)*
**Pragmas:** `nonReloadable`, `inline`, `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### nimZeroMem

[ref: #symbol-nimzeromem]

**Input:**
- `p: pointer`
- `size: Natural`

**Output:** *(none)*
**Pragmas:** `nonReloadable`, `inline`, `enforceNoRaises`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `
