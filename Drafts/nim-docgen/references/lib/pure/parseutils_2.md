---
source_hash: 53ce8b9f2450523b
source_path: lib/pure/parseutils.nim
---

### parseSaturatedNatural

[ref: #symbol-parsesaturatednatural]

**Input:**
- `s: string`
- `b: var int`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a natural number into b. This cannot raise an overflow error. high(int) is returned for an overflow. The number of processed character is returned. This is usually what you really want to use instead of parseInt.

### parseSize

[ref: #symbol-parsesize]

Parse a size qualified by binary or metric units into size. This format is often called "human readable". Result is the number of processed chars or 0 on parse errors and size is rounded to the nearest integer. Trailing garbage like "/s" in "1k/s" is allowed and detected by result < s.len.

**Input:**
- `s: openArray[char]`
- `size: var int64`
- `alwaysBin:  = false`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parse a size qualified by binary or metric units into size. This format is often called "human readable". Result is the number of processed chars or 0 on parse errors and size is rounded to the nearest integer. Trailing garbage like "/s" in "1k/s" is allowed and detected by result < s.len.

To simplify use, following non-rare wild conventions, and since fractional data like milli-bytes is so rare, unit matching is case-insensitive but for the 'i' distinguishing binary-metric from metric (which cannot be 'I').

An optional trailing 'B|b' is ignored but processed. I.e., you must still know if units are bytes | bits or infer this fact via the case of s**[[1]](#footnote-1)** (if users can even be relied upon to use 'B' for byte and 'b' for bit or have that be s**[[1]](#footnote-1)**).

If alwaysBin==true then scales are always binary-metric, but e.g. "KiB" is still accepted for clarity. If the value would exceed the range of int64, size saturates to int64.high. Supported metric prefix chars include k, m, g, t, p, e, z, y (but z & y saturate unless the number is a small fraction).

**See also:**

* <https://en.wikipedia.org/wiki/Binary_prefix>
* [formatSize module](strutils.html) for formatting

### parseUInt

[ref: #symbol-parseuint]

**Input:**
- `s: openArray[char]`
- `number: var uint`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npuParseUInt"`, `noSideEffect`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses an unsigned integer and stores the value into number. ValueError is raised if the parsed integer is out of the valid range.

### parseUInt

[ref: #symbol-parseuint]

**Input:**
- `s: string`
- `number: var uint`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses an unsigned integer starting at start and stores the value into number. ValueError is raised if the parsed integer is out of the valid range.

### parseUntil

[ref: #symbol-parseuntil]

**Input:**
- `s: openArray[char]`
- `token: var string`
- `until: set[char]`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a token and stores it in token. Returns the number of the parsed characters or 0 in case of an error. A token consists of the characters notin until.

### parseUntil

[ref: #symbol-parseuntil]

**Input:**
- `s: openArray[char]`
- `token: var string`
- `until: char`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a token and stores it in token. Returns the number of the parsed characters or 0 in case of an error. A token consists of any character that is not the until character.

### parseUntil

[ref: #symbol-parseuntil]

**Input:**
- `s: openArray[char]`
- `token: var string`
- `until: string`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a token and stores it in token. Returns the number of the parsed characters or 0 in case of an error. A token consists of any character that comes before the until token.

### parseUntil

[ref: #symbol-parseuntil]

**Input:**
- `s: string`
- `token: var string`
- `until: set[char]`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a token and stores it in token. Returns the number of the parsed characters or 0 in case of an error. A token consists of the characters notin until.

### parseUntil

[ref: #symbol-parseuntil]

**Input:**
- `s: string`
- `token: var string`
- `until: char`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a token and stores it in token. Returns the number of the parsed characters or 0 in case of an error. A token consists of any character that is not the until character.

### parseUntil

[ref: #symbol-parseuntil]

**Input:**
- `s: string`
- `token: var string`
- `until: string`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a token and stores it in token. Returns the number of the parsed characters or 0 in case of an error. A token consists of any character that comes before the until token.

### parseWhile

[ref: #symbol-parsewhile]

**Input:**
- `s: openArray[char]`
- `token: var string`
- `validChars: set[char]`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a token and stores it in token. Returns the number of the parsed characters or 0 in case of an error. A token consists of the characters in validChars.

### parseWhile

[ref: #symbol-parsewhile]

**Input:**
- `s: string`
- `token: var string`
- `validChars: set[char]`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a token and stores it in token. Returns the number of the parsed characters or 0 in case of an error. A token consists of the characters in validChars.

### skip

[ref: #symbol-skip]

**Input:**
- `s: openArray[char]`
- `token: openArray[char]`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips the token starting at s[start]. Returns the length of token or 0 if there was no token at s[start].

### skip

[ref: #symbol-skip]

**Input:**
- `s: string`
- `token: string`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips the token starting at s[start]. Returns the length of token or 0 if there was no token at s[start].

### skipIgnoreCase

[ref: #symbol-skipignorecase]

**Input:**
- `s: openArray[char]`
- `token: openArray[char]`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as skip but case is ignored for token matching.

### skipIgnoreCase

[ref: #symbol-skipignorecase]

**Input:**
- `s: string`
- `token: string`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as skip but case is ignored for token matching.

### skipUntil

[ref: #symbol-skipuntil]

**Input:**
- `s: openArray[char]`
- `until: set[char]`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips all characters until one char from the set until is found or the end is reached. Returns number of characters skipped.

### skipUntil

[ref: #symbol-skipuntil]

**Input:**
- `s: openArray[char]`
- `until: char`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips all characters until the char until is found or the end is reached. Returns number of characters skipped.

### skipUntil

[ref: #symbol-skipuntil]

**Input:**
- `s: string`
- `until: set[char]`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips all characters until one char from the set until is found or the end is reached. Returns number of characters skipped.

### skipUntil

[ref: #symbol-skipuntil]

**Input:**
- `s: string`
- `until: char`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips all characters until the char until is found or the end is reached. Returns number of characters skipped.

### skipWhile

[ref: #symbol-skipwhile]

**Input:**
- `s: openArray[char]`
- `toSkip: set[char]`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips all characters while one char from the set toSkip is found. Returns number of characters skipped.

### skipWhile

[ref: #symbol-skipwhile]

**Input:**
- `s: string`
- `toSkip: set[char]`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips all characters while one char from the set toSkip is found. Returns number of characters skipped.

### skipWhitespace

[ref: #symbol-skipwhitespace]

**Input:**
- `s: openArray[char]`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips the whitespace starting at s[start]. Returns the number of skipped characters.

### skipWhitespace

[ref: #symbol-skipwhitespace]

**Input:**
- `s: string`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Skips the whitespace starting at s[start]. Returns the number of skipped characters.

## Type

### InterpolatedKind

[ref: #symbol-interpolatedkind]

```nim
InterpolatedKind = enum
  ikStr,                    ## ``str`` part of the interpolated string
  ikDollar,                 ## escaped ``$`` part of the interpolated string
  ikVar,                    ## ``var`` part of the interpolated string
  ikExpr                     ## ``expr`` part of the interpolated string
```

Describes for interpolatedFragments which part of the interpolated string is yielded; for example in "str$$$var${expr}"

[Prev](parseutils_1.md)
