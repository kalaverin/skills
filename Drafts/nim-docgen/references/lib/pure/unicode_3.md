---
source_hash: 3c32a13cf2f9bcf5
source_path: lib/pure/unicode.nim
---

### fastToUTF8Copy

[ref: #symbol-fasttoutf8copy]

Copies UTF-8 representation of c into the preallocated string s starting at position pos.

**Input:**
- `c: Rune`
- `s: var string`
- `pos: int`
- `doInc:  = true`

**Output:** *(none)*
Copies UTF-8 representation of c into the preallocated string s starting at position pos.

If doInc == true (default), pos is incremented by the number of bytes that have been processed.

To be the most efficient, make sure s is preallocated with an additional amount equal to the byte length of c.

See also:

* [validateUtf8 proc](#validateUtf8,string)
* [toUTF8 proc](#toUTF8,Rune)
* [$ proc](#$,Rune) alias for toUTF8

## Type

### Rune

[ref: #symbol-rune]

Type that can hold a single Unicode code point.

```nim
Rune = distinct RuneImpl
```

Type that can hold a single Unicode code point.

A Rune may be composed with other Runes to a character on the screen. RuneImpl is the underlying type used to store Runes, currently int32.

[Prev](unicode_2.md)
