---
source_hash: 4da5c29ccac95ae6
source_path: lib/system/countbits_impl.nim
---

# countbits_impl

[ref: #module-countbits_impl]

Contains the used algorithms for counting bits.

## Const

### arch64

[ref: #symbol-arch64]

```nim
arch64 = true
```

### noUndefined

[ref: #symbol-noundefined]

```nim
noUndefined = false
```

### useBuiltins

[ref: #symbol-usebuiltins]

```nim
useBuiltins = true
```

### useGCC_builtins

[ref: #symbol-usegcc-builtins]

```nim
useGCC_builtins = true
```

### useICC_builtins

[ref: #symbol-useicc-builtins]

```nim
useICC_builtins = false
```

### useVCC_builtins

[ref: #symbol-usevcc-builtins]

```nim
useVCC_builtins = false
```

## Proc

### countBits32

[ref: #symbol-countbits32]

**Input:**
- `n: uint32`

**Output:** `int`
**Pragmas:** `compilerproc`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### countBits64

[ref: #symbol-countbits64]

**Input:**
- `n: uint64`

**Output:** `int`
**Pragmas:** `compilerproc`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### countSetBitsImpl

[ref: #symbol-countsetbitsimpl]

**Input:**
- `x: SomeInteger`

**Output:** `int`
**Generic parameters:** `SomeInteger`

**Pragmas:** `inline`

Counts the set bits in an integer (also called Hamming weight).
