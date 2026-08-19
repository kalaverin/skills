---
source_hash: 513ebd9d6503c24b
source_path: lib/pure/cstrutils.nim
---

# cstrutils

[ref: #module-cstrutils]

This module supports helper routines for working with cstring without having to convert cstring to string, in order to save allocations.

# [See also](#see-also)

* [strutils module](strutils.html) for working with string

## Examples

```nim
assert cmpIgnoreCase(cstring"hello", cstring"HeLLo") == 0
assert cmpIgnoreCase(cstring"echo", cstring"hello") < 0
assert cmpIgnoreCase(cstring"yellow", cstring"hello") > 0
```

```nim
assert cmpIgnoreStyle(cstring"hello", cstring"H_e_L_Lo") == 0
```

```nim
assert endsWith(cstring"Hello, Nimion", cstring"Nimion")
assert not endsWith(cstring"Hello, Nimion", cstring"Hello")
assert endsWith(cstring"Hello", cstring"")
```

```nim
assert startsWith(cstring"Hello, Nimion", cstring"Hello")
assert not startsWith(cstring"Hello, Nimion", cstring"Nimion")
assert startsWith(cstring"Hello", cstring"")
```

## Proc

### cmpIgnoreCase

[ref: #symbol-cmpignorecase]

Compares two strings in a case insensitive manner. Returns:

**Input:**
- `a: cstring`
- `b: cstring`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "csuCmpIgnoreCase"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two strings in a case insensitive manner. Returns:

* 0 if a == b
* < 0 if a < b
* > 0 if a > b

### cmpIgnoreStyle

[ref: #symbol-cmpignorestyle]

Semantically the same as cmp(normalize($a), normalize($b)). It is just optimized to not allocate temporary strings. This should NOT be used to compare Nim identifier names, use macros.eqIdent for that. Returns:

**Input:**
- `a: cstring`
- `b: cstring`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "csuCmpIgnoreStyle"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Semantically the same as cmp(normalize($a), normalize($b)). It is just optimized to not allocate temporary strings. This should NOT be used to compare Nim identifier names, use macros.eqIdent for that. Returns:

* 0 if a == b
* < 0 if a < b
* > 0 if a > b

### endsWith

[ref: #symbol-endswith]

Returns true if s ends with suffix.

**Input:**
- `s: cstring`
- `suffix: cstring`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "csuEndsWith"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s ends with suffix.

The JS backend uses the native String.prototype.endsWith function.

### startsWith

[ref: #symbol-startswith]

Returns true if s starts with prefix.

**Input:**
- `s: cstring`
- `prefix: cstring`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "csuStartsWith"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s starts with prefix.

The JS backend uses the native String.prototype.startsWith function.
