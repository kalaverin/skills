---
source_hash: bff1a741e2f3a855
source_path: lib/std/sha1.nim
---

# sha1

[ref: #module-sha1]

[SHA-1 (Secure Hash Algorithm 1)](https://en.wikipedia.org/wiki/SHA-1) is a cryptographic hash function which takes an input and produces a 160-bit (20-byte) hash value known as a message digest.

# [See also](#see-also)

* [base64 module](base64.html) for a Base64 encoder and decoder
* [hashes module](hashes.html) for efficient computations of hash values for diverse Nim types
* [md5 module](md5.html) for the MD5 checksum algorithm

## Examples

```nim
import std/sha1
let accessName = secureHash("John Doe")
assert $accessName == "AE6E4D1209F17B460503904FAD297B31E9CF6362"
```

```nim
import std/sha1
let
  a = secureHashFile("myFile.nim")
  b = parseSecureHash("10DFAEBF6BFDBC7939957068E2EFACEC4972933C")
assert a == b, "files don't match"
```

```nim
let hash = secureHash("Hello World")
assert $hash == "0A4D55A8D778E5022FAB701977C5D840BBC486D0"
```

```nim
let
  a = secureHash("Hello World")
  b = secureHash("Goodbye World")
  c = parseSecureHash("0A4D55A8D778E5022FAB701977C5D840BBC486D0")
assert a != b
assert a == c
```

```nim
let
  hashStr = "0A4D55A8D778E5022FAB701977C5D840BBC486D0"
  secureHash = secureHash("Hello World")
assert secureHash == parseSecureHash(hashStr)
```

```nim
let hash = secureHash("Hello World")
assert hash == parseSecureHash("0A4D55A8D778E5022FAB701977C5D840BBC486D0")
```

## Proc

### `$`

[ref: #symbol-]

Returns the string representation of a SecureHash.

**Input:**
- `self: SecureHash`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the string representation of a SecureHash.

**See also:**

* [secureHash proc](#secureHash,openArray[char]) for generating a SecureHash from a string

### `==`

[ref: #symbol-]

**Input:**
- `a: SecureHash`
- `b: SecureHash`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if two SecureHash values are identical.

### finalize

[ref: #symbol-finalize]

Finalizes the Sha1State and returns a Sha1Digest.

**Input:**
- `ctx: var Sha1State`

**Output:** `Sha1Digest`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Finalizes the Sha1State and returns a Sha1Digest.

If you use the [secureHash proc](#secureHash,openArray[char]), there's no need to call this function explicitly.

### isValidSha1Hash

[ref: #symbol-isvalidsha1hash]

**Input:**
- `s: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if a string is a valid sha1 hash sum.

### newSha1State

[ref: #symbol-newsha1state]

Creates a Sha1State.

**Input:**
- *(none)*

**Output:** `Sha1State`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a Sha1State.

If you use the [secureHash proc](#secureHash,openArray[char]), there's no need to call this function explicitly.

### parseSecureHash

[ref: #symbol-parsesecurehash]

Converts a string hash to a SecureHash.

**Input:**
- `hash: string`

**Output:** `SecureHash`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Converts a string hash to a SecureHash.

**See also:**

* [secureHash proc](#secureHash,openArray[char]) for generating a SecureHash from a string
* [secureHashFile proc](#secureHashFile,string) for generating a SecureHash from a file

### secureHash

[ref: #symbol-securehash]

Generates a SecureHash from str.

**Input:**
- `str: openArray[char]`

**Output:** `SecureHash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generates a SecureHash from str.

**See also:**

* [secureHashFile proc](#secureHashFile,string) for generating a SecureHash from a file
* [parseSecureHash proc](#parseSecureHash,string) for converting a string hash to SecureHash

### secureHashFile

[ref: #symbol-securehashfile]

Generates a SecureHash from a file.

**Input:**
- `filename: string`

**Output:** `SecureHash`
**Pragmas:** `raises: [IOError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: ReadIOEffect`, `forbids: `

Generates a SecureHash from a file.

**See also:**

* [secureHash proc](#secureHash,openArray[char]) for generating a SecureHash from a string
* [parseSecureHash proc](#parseSecureHash,string) for converting a string hash to SecureHash

### update

[ref: #symbol-update]

Updates the Sha1State with data.

**Input:**
- `ctx: var Sha1State`
- `data: openArray[char]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Updates the Sha1State with data.

If you use the [secureHash proc](#secureHash,openArray[char]), there's no need to call this function explicitly.

## Type

### SecureHash

[ref: #symbol-securehash]

```nim
SecureHash = distinct Sha1Digest
```

### Sha1Digest

[ref: #symbol-sha1digest]

```nim
Sha1Digest = array[0 .. 20 - 1, uint8]
```

### Sha1State

[ref: #symbol-sha1state]

```nim
Sha1State = object
```
