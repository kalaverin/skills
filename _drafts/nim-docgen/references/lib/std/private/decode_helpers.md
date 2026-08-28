---
source_hash: e6970fea52c34305
source_path: lib/std/private/decode_helpers.nim
---

# decode_helpers

[ref: #module-decode_helpers]

## Examples

```nim
var x = 0
assert handleHexChar('a', x)
assert x == 10

assert handleHexChar('B', x)
assert x == 171 # 10 shl 4 + 11

assert not handleHexChar('?', x)
assert x == 171 # unchanged
```

## Proc

### decodePercent

[ref: #symbol-decodepercent]

Converts %xx hexadecimal to the character with ordinal number xx.

**Input:**
- `s: openArray[char]`
- `i: var int`

**Output:** `char`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts %xx hexadecimal to the character with ordinal number xx.

If xx is not a valid hexadecimal value, it is left intact: only the leading % is returned as-is, and xx characters will be processed in the next step (e.g. in uri.decodeUrl) as regular characters.

### handleHexChar

[ref: #symbol-handlehexchar]

Converts %xx hexadecimal to the ordinal number and adds the result to x. Returns true if c is hexadecimal.

**Input:**
- `c: char`
- `x: var int`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts %xx hexadecimal to the ordinal number and adds the result to x. Returns true if c is hexadecimal.

When c is hexadecimal, the proc is equal to x = x shl 4 + hex2Int(c).

### handleHexChar

[ref: #symbol-handlehexchar]

**Input:**
- `c: char`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `
