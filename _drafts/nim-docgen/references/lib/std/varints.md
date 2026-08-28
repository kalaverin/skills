---
source_hash: 686fe0454ad274b6
source_path: lib/std/varints.nim
---

# varints

[ref: #module-varints]

A variable length integer encoding implementation inspired by SQLite.

Unstable API.

## Const

### maxVarIntLen

[ref: #symbol-maxvarintlen]

```nim
maxVarIntLen = 9
```

the maximal number of bytes a varint can take

## Proc

### decodeZigzag

[ref: #symbol-decodezigzag]

**Input:**
- `x: uint64`

**Output:** `int64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### encodeZigzag

[ref: #symbol-encodezigzag]

**Input:**
- `x: int64`

**Output:** `uint64`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readVu64

[ref: #symbol-readvu64]

**Input:**
- `z: openArray[byte]`
- `pResult: var uint64`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### writeVu64

[ref: #symbol-writevu64]

**Input:**
- `z: var openArray[byte]`
- `x: uint64`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Write a varint into z. The buffer z must be at least 9 characters long to accommodate the largest possible varint. Returns the number of bytes used.
