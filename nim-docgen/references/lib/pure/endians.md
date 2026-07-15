---
source_hash: a2258b4cef89bfee
source_path: lib/pure/endians.nim
---

# endians

[ref: #module-endians]

This module contains helpers that deal with different byte orders (endian).

Endianness is the order of bytes of a value in memory. Big-endian means that the most significant byte is stored at the smallest memory address, while little endian means that the least-significant byte is stored at the smallest address. See also <https://en.wikipedia.org/wiki/Endianness>.

Unstable API.

## Examples

```nim
var a = [1'u8, 2]
var b: array[2, uint8]
swapEndian16(addr b, addr a)
assert b == [2'u8, 1]
```

```nim
var a = [1'u8, 2, 3, 4]
var b: array[4, uint8]
swapEndian32(addr b, addr a)
assert b == [4'u8, 3, 2, 1]
```

```nim
var a = [1'u8, 2, 3, 4, 5, 6, 7, 8]
var b: array[8, uint8]
swapEndian64(addr b, addr a)
assert b == [8'u8, 7, 6, 5, 4, 3, 2, 1]
```

## Proc

### bigEndian16

[ref: #symbol-bigendian16]

**Input:**
- `outp: pointer`
- `inp: pointer`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copies inp to outp, storing it in 16-bit big-endian order. Both buffers are supposed to contain at least 2 bytes.

### bigEndian32

[ref: #symbol-bigendian32]

**Input:**
- `outp: pointer`
- `inp: pointer`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copies inp to outp, storing it in 32-bit big-endian order. Both buffers are supposed to contain at least 4 bytes.

### bigEndian64

[ref: #symbol-bigendian64]

**Input:**
- `outp: pointer`
- `inp: pointer`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copies inp to outp, storing it in 64-bit big-endian order. Both buffers are supposed to contain at least 8 bytes.

### littleEndian16

[ref: #symbol-littleendian16]

**Input:**
- `outp: pointer`
- `inp: pointer`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copies inp to outp, storing it in 16-bit little-endian order. Both buffers are supposed to contain at least 2 bytes.

### littleEndian32

[ref: #symbol-littleendian32]

**Input:**
- `outp: pointer`
- `inp: pointer`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copies inp to outp, storing it in 32-bit little-endian order. Both buffers are supposed to contain at least 4 bytes.

### littleEndian64

[ref: #symbol-littleendian64]

**Input:**
- `outp: pointer`
- `inp: pointer`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copies inp to outp, storing it in 64-bit little-endian order. Both buffers are supposed to contain at least 8 bytes.

### swapEndian16

[ref: #symbol-swapendian16]

**Input:**
- `outp: pointer`
- `inp: pointer`

**Output:** *(none)*
**Pragmas:** `inline`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copies inp to outp, reversing the byte order. Both buffers are supposed to contain at least 2 bytes.

### swapEndian32

[ref: #symbol-swapendian32]

**Input:**
- `outp: pointer`
- `inp: pointer`

**Output:** *(none)*
**Pragmas:** `inline`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copies inp to outp, reversing the byte order. Both buffers are supposed to contain at least 4 bytes.

### swapEndian64

[ref: #symbol-swapendian64]

**Input:**
- `outp: pointer`
- `inp: pointer`

**Output:** *(none)*
**Pragmas:** `inline`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copies inp to outp, reversing the byte order. Both buffers are supposed to contain at least 8 bytes.
