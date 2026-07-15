---
source_hash: 622c033b18a3a357
source_path: lib/std/wordwrap.nim
---

# wordwrap

[ref: #module-wordwrap]

This module contains an algorithm to wordwrap a Unicode string.

## Examples

```nim
doAssert "12345678901234567890".wrapWords() == "12345678901234567890"
doAssert "123456789012345678901234567890".wrapWords(20) == "12345678901234567890\n1234567890"
doAssert "Hello Bob. Hello John.".wrapWords(13, false) == "Hello Bob.\nHello John."
doAssert "Hello Bob. Hello John.".wrapWords(13, true, {';'}) == "Hello Bob. He\nllo John."
```

## Proc

### wrapWords

[ref: #symbol-wrapwords]

**Input:**
- `s: string`
- `maxLineWidth:  = 80`
- `splitLongWords:  = true`
- `seps: set[char] = Whitespace`
- `newLine:  = "\n"`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Word wraps s.
