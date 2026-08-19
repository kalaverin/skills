---
source_hash: 5332a27e9b552abf
source_path: lib/std/editdistance.nim
---

# editdistance

[ref: #module-editdistance]

This module implements an algorithm to compute the edit distance between two Unicode strings.

## Examples

```nim
static: doAssert editdistance("Kitten", "Bitten") == 1
```

```nim
static: doAssert editDistanceAscii("Kitten", "Bitten") == 1
```

## Proc

### editDistance

[ref: #symbol-editdistance]

Returns the **unicode-rune** edit distance between a and b.

**Input:**
- `a: string`
- `b: string`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the **unicode-rune** edit distance between a and b.

This uses the Levenshtein distance algorithm with only a linear memory overhead.

### editDistanceAscii

[ref: #symbol-editdistanceascii]

Returns the edit distance between a and b.

**Input:**
- `a: string`
- `b: string`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the edit distance between a and b.

This uses the Levenshtein distance algorithm with only a linear memory overhead.
