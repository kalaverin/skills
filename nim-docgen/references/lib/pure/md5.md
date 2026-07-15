---
source_hash: edf2cf049cbd0c67
source_path: lib/pure/md5.nim
---

# md5

[ref: #module-md5]

Module for computing [MD5 checksums](https://en.wikipedia.org/wiki/MD5).

This module also works at compile time and in JavaScript.

# [See also](#see-also)

* [base64 module](base64.html) for a Base64 encoder and decoder
* [sha1 module](sha1.html) for the SHA-1 checksum algorithm
* [hashes module](hashes.html) for efficient computations of hash values for diverse Nim types

## Examples

```nim
assert getMD5("abc") == "900150983cd24fb0d6963f7d28e17f72"
```

```nim
assert $toMD5("abc") == "900150983cd24fb0d6963f7d28e17f72"
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `d: MD5Digest`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a MD5Digest value into its string representation.

### `==`

[ref: #symbol-]

**Input:**
- `D1: MD5Digest`
- `D2: MD5Digest`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if two MD5Digest values are identical.

### getMD5

[ref: #symbol-getmd5]

Computes an MD5 value of s and returns its string representation.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes an MD5 value of s and returns its string representation.

**See also:**

* [toMD5 proc](#toMD5,string) which returns the MD5Digest of a string

### md5Final

[ref: #symbol-md5final]

**Input:**
- `c: var MD5Context`
- `digest: var MD5Digest`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `gcsafe`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### md5Init

[ref: #symbol-md5init]

**Input:**
- `c: var MD5Context`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `gcsafe`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### md5Update

[ref: #symbol-md5update]

**Input:**
- `c: var MD5Context`
- `input: openArray[uint8]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `gcsafe`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### md5Update

[ref: #symbol-md5update]

Updates the MD5Context with the input data of length len.

**Input:**
- `c: var MD5Context`
- `input: cstring`
- `len: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `gcsafe`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Updates the MD5Context with the input data of length len.

If you use the [toMD5 proc](#toMD5,string), there's no need to call this function explicitly.

### toMD5

[ref: #symbol-tomd5]

Computes the MD5Digest value for a string s.

**Input:**
- `s: string`

**Output:** `MD5Digest`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes the MD5Digest value for a string s.

**See also:**

* [getMD5 proc](#getMD5,string) which returns a string representation of the MD5Digest
* [$ proc](#$,MD5Digest) for converting MD5Digest to string

## Type

### MD5Context

[ref: #symbol-md5context]

```nim
MD5Context {.final.} = object
```

### MD5Digest

[ref: #symbol-md5digest]

```nim
MD5Digest = array[0 .. 15, uint8]
```

MD5 checksum of a string, obtained with the [toMD5 proc](#toMD5,string).
