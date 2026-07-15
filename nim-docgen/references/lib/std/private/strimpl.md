---
source_hash: ac13e83d65ca86e1
source_path: lib/std/private/strimpl.nim
---

# strimpl

[ref: #module-strimpl]

## Proc

### cmpNimIdentifier

[ref: #symbol-cmpnimidentifier]

**Input:**
- `a: T`
- `b: T`

**Output:** `int`
**Generic parameters:** `T`

### find

[ref: #symbol-find]

Searches for sub in s inside the range start..last (both ends included). If last is unspecified, it defaults to s.high (the last element).

**Input:**
- `s: cstring`
- `sub: char`
- `start: Natural = 0`
- `last:  = 0`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Searches for sub in s inside the range start..last (both ends included). If last is unspecified, it defaults to s.high (the last element).

Searching is case-sensitive. If sub is not in s, -1 is returned. Otherwise the index returned is relative to s[0], not start. Use s[start..last].rfind for a start-origin index.

### find

[ref: #symbol-find]

Searches for sub in s inside the range start..last (both ends included). If last is unspecified, it defaults to s.high (the last element).

**Input:**
- `s: cstring`
- `sub: cstring`
- `start: Natural = 0`
- `last:  = 0`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Searches for sub in s inside the range start..last (both ends included). If last is unspecified, it defaults to s.high (the last element).

Searching is case-sensitive. If sub is not in s, -1 is returned. Otherwise the index returned is relative to s[0], not start. Use s[start..last].find for a start-origin index.

### toLowerAscii

[ref: #symbol-tolowerascii]

**Input:**
- `c: char`

**Output:** `char`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### cmpIgnoreCaseImpl

[ref: #symbol-cmpignorecaseimpl]

**Input:**
- `a: T`
- `b: T`
- `firstCharCaseSensitive: static bool = false`

**Output:** *(none)*
**Generic parameters:** `T`, `firstCharCaseSensitive:type`

### cmpIgnoreStyleImpl

[ref: #symbol-cmpignorestyleimpl]

**Input:**
- `a: T`
- `b: T`
- `firstCharCaseSensitive: static bool = false`

**Output:** *(none)*
**Generic parameters:** `T`, `firstCharCaseSensitive:type`

### endsWithImpl

[ref: #symbol-endswithimpl]

**Input:**
- `s: T`
- `suffix: T`

**Output:** *(none)*
**Generic parameters:** `T`

### startsWithImpl

[ref: #symbol-startswithimpl]

**Input:**
- `s: T`
- `prefix: T`

**Output:** *(none)*
**Generic parameters:** `T`
