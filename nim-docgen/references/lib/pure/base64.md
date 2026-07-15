---
source_hash: a6d37421098f19c2
source_path: lib/pure/base64.nim
---

# base64

[ref: #module-base64]

This module implements a base64 encoder and decoder.

Unstable API.

Base64 is an encoding and decoding technique used to convert binary data to an ASCII string format. Each Base64 digit represents exactly 6 bits of data. Three 8-bit bytes (i.e., a total of 24 bits) can therefore be represented by four 6-bit Base64 digits.

# [Basic usage](#basic-usage)

## [Encoding data](#basic-usage-encoding-data)

Apart from strings you can also encode lists of integers or characters:

## [Decoding data](#basic-usage-decoding-data)

## [URL Safe Base64](#basic-usage-url-safe-base64)

# [See also](#see-also)

* [hashes module](hashes.html) for efficient computations of hash values for diverse Nim types
* [md5 module](md5.html) for the MD5 checksum algorithm
* [sha1 module](sha1.html) for the SHA-1 checksum algorithm

## Examples

```nim
import std/base64
let encoded = encode("Hello World")
assert encoded == "SGVsbG8gV29ybGQ="
```

```nim
import std/base64
let encodedInts = encode([1'u8,2,3])
assert encodedInts == "AQID"
let encodedChars = encode(['h','e','y'])
assert encodedChars == "aGV5"
```

```nim
import std/base64
let decoded = decode("SGVsbG8gV29ybGQ=")
assert decoded == "Hello World"
```

```nim
import std/base64
assert encode("c\xf7>", safe = true) == "Y_c-"
assert encode("c\xf7>", safe = false) == "Y/c+"
```

```nim
assert decode("SGVsbG8gV29ybGQ=") == "Hello World"
assert decode("  SGVsbG8gV29ybGQ=") == "Hello World"
```

```nim
assert encode("Hello World") == "SGVsbG8gV29ybGQ="
assert encode(['n', 'i', 'm']) == "bmlt"
assert encode(@['n', 'i', 'm']) == "bmlt"
assert encode([1'u8, 2, 3, 4, 5]) == "AQIDBAU="
```

```nim
assert encodeMime("Hello World", 4, "\n") == "SGVs\nbG8g\nV29y\nbGQ="
```

## Proc

### decode

[ref: #symbol-decode]

Decodes string s in base64 representation back into its original form. The initial whitespace is skipped.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Decodes string s in base64 representation back into its original form. The initial whitespace is skipped.

**See also:**

* [encode proc](#encode,openArray[T]) for encoding an openarray

### encode

[ref: #symbol-encode]

Encodes s into base64 representation.

**Input:**
- `s: openArray[T]`
- `safe:  = false`

**Output:** `string`
**Generic parameters:** `T`

Encodes s into base64 representation.

If safe is true then it will encode using the URL-Safe and Filesystem-safe standard alphabet characters, which substitutes - instead of + and \_ instead of /.

* <https://en.wikipedia.org/wiki/Base64#URL_applications>
* <https://tools.ietf.org/html/rfc4648#page-7>

**See also:**

* [decode proc](#decode,string) for decoding a string

### encode

[ref: #symbol-encode]

**Input:**
- `s: openArray[T]`
- `safe:  = false`

**Output:** `string`
**Generic parameters:** `T`

**Pragmas:** `deprecated: "use `byte` or `char` instead"`

### encodeMime

[ref: #symbol-encodemime]

Encodes s into base64 representation as lines. Used in email MIME format, use lineLen and newline.

**Input:**
- `s: string`
- `lineLen:  = 75.Positive`
- `newLine:  = "\r\n"`
- `safe:  = false`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Encodes s into base64 representation as lines. Used in email MIME format, use lineLen and newline.

This procedure encodes a string according to MIME spec.

If safe is true then it will encode using the URL-Safe and Filesystem-safe standard alphabet characters, which substitutes - instead of + and \_ instead of /.

* <https://en.wikipedia.org/wiki/Base64#URL_applications>
* <https://tools.ietf.org/html/rfc4648#page-7>

**See also:**

* [encode proc](#encode,openArray[T]) for encoding an openArray
* [decode proc](#decode,string) for decoding a string

### initDecodeTable

[ref: #symbol-initdecodetable]

**Input:**
- *(none)*

**Output:** `array[256, char]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `
