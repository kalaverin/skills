---
source_hash: 3c32a13cf2f9bcf5
source_path: lib/pure/unicode.nim
---

### isWhiteSpace

[ref: #symbol-iswhitespace]

Returns true if c is a Unicode whitespace code point.

**Input:**
- `c: Rune`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if c is a Unicode whitespace code point.

See also:

* [isLower proc](#isLower,Rune)
* [isUpper proc](#isUpper,Rune)
* [isTitle proc](#isTitle,Rune)
* [isAlpha proc](#isAlpha,Rune)

### lastRune

[ref: #symbol-lastrune]

**Input:**
- `s: openArray[char]`
- `last: int`

**Output:** `(Rune, int)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Length of the last rune in s[0..last]. Returns the rune and its length in bytes.

### lastRune

[ref: #symbol-lastrune]

**Input:**
- `s: string`
- `last: int`

**Output:** `(Rune, int)`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Length of the last rune in s[0..last]. Returns the rune and its length in bytes.

### repeat

[ref: #symbol-repeat]

Returns a string of count Runes c.

**Input:**
- `c: Rune`
- `count: Natural`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nucRepeatRune"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a string of count Runes c.

The returned string will have a rune-length of count.

### reversed

[ref: #symbol-reversed]

Returns the reverse of s, interpreting it as runes.

**Input:**
- `s: openArray[char]`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the reverse of s, interpreting it as runes.

Unicode combining characters are correctly interpreted as well.

### reversed

[ref: #symbol-reversed]

Returns the reverse of s, interpreting it as runes.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the reverse of s, interpreting it as runes.

Unicode combining characters are correctly interpreted as well.

### runeAt

[ref: #symbol-runeat]

Returns the rune in s at **byte index** i.

**Input:**
- `s: openArray[char]`
- `i: Natural`

**Output:** `Rune`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the rune in s at **byte index** i.

See also:

* [runeAtPos proc](#runeAtPos,string,int)
* [runeStrAtPos proc](#runeStrAtPos,string,Natural)
* [fastRuneAt template](#fastRuneAt.t,string,int,untyped)

### runeAt

[ref: #symbol-runeat]

Returns the rune in s at **byte index** i.

**Input:**
- `s: string`
- `i: Natural`

**Output:** `Rune`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the rune in s at **byte index** i.

See also:

* [runeAtPos proc](#runeAtPos,string,int)
* [runeStrAtPos proc](#runeStrAtPos,string,Natural)
* [fastRuneAt template](#fastRuneAt.t,string,int,untyped)

### runeAtPos

[ref: #symbol-runeatpos]

Returns the rune at position pos.

**Input:**
- `s: openArray[char]`
- `pos: int`

**Output:** `Rune`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the rune at position pos.

**Beware:** This can lead to unoptimized code and slow execution! Most problems can be solved more efficiently by using an iterator or conversion to a seq of Rune.

See also:

* [runeAt proc](#runeAt,string,Natural)
* [runeStrAtPos proc](#runeStrAtPos,string,Natural)
* [fastRuneAt template](#fastRuneAt.t,string,int,untyped)

### runeAtPos

[ref: #symbol-runeatpos]

Returns the rune at position pos.

**Input:**
- `s: string`
- `pos: int`

**Output:** `Rune`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the rune at position pos.

**Beware:** This can lead to unoptimized code and slow execution! Most problems can be solved more efficiently by using an iterator or conversion to a seq of Rune.

See also:

* [runeAt proc](#runeAt,string,Natural)
* [runeStrAtPos proc](#runeStrAtPos,string,Natural)
* [fastRuneAt template](#fastRuneAt.t,string,int,untyped)

### runeLen

[ref: #symbol-runelen]

**Input:**
- `s: openArray[char]`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of runes of the string s.

### runeLen

[ref: #symbol-runelen]

**Input:**
- `s: string`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of runes of the string s.

### runeLenAt

[ref: #symbol-runelenat]

Returns the number of bytes the rune starting at s[i] takes.

**Input:**
- `s: openArray[char]`
- `i: Natural`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of bytes the rune starting at s[i] takes.

See also:

* [fastRuneAt template](#fastRuneAt.t,string,int,untyped)

### runeLenAt

[ref: #symbol-runelenat]

Returns the number of bytes the rune starting at s[i] takes.

**Input:**
- `s: string`
- `i: Natural`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of bytes the rune starting at s[i] takes.

See also:

* [fastRuneAt template](#fastRuneAt.t,string,int,untyped)

### runeOffset

[ref: #symbol-runeoffset]

Returns the byte position of rune at position pos in s with an optional start byte position. Returns the special value -1 if it runs out of the string.

**Input:**
- `s: openArray[char]`
- `pos: Natural`
- `start: Natural = 0`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the byte position of rune at position pos in s with an optional start byte position. Returns the special value -1 if it runs out of the string.

**Beware:** This can lead to unoptimized code and slow execution! Most problems can be solved more efficiently by using an iterator or conversion to a seq of Rune.

See also:

* [runeReverseOffset proc](#runeReverseOffset,string,Positive)

### runeOffset

[ref: #symbol-runeoffset]

Returns the byte position of rune at position pos in s with an optional start byte position. Returns the special value -1 if it runs out of the string.

**Input:**
- `s: string`
- `pos: Natural`
- `start: Natural = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the byte position of rune at position pos in s with an optional start byte position. Returns the special value -1 if it runs out of the string.

**Beware:** This can lead to unoptimized code and slow execution! Most problems can be solved more efficiently by using an iterator or conversion to a seq of Rune.

See also:

* [runeReverseOffset proc](#runeReverseOffset,string,Positive)

### runeReverseOffset

[ref: #symbol-runereverseoffset]

Returns a tuple with the byte offset of the rune at position rev in s, counting from the end (starting with 1) and the total number of runes in the string.

**Input:**
- `s: openArray[char]`
- `rev: Positive`

**Output:** `(int, int)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a tuple with the byte offset of the rune at position rev in s, counting from the end (starting with 1) and the total number of runes in the string.

Returns a negative value for offset if there are too few runes in the string to satisfy the request.

**Beware:** This can lead to unoptimized code and slow execution! Most problems can be solved more efficiently by using an iterator or conversion to a seq of Rune.

See also:

* [runeOffset proc](#runeOffset,string,Natural,Natural)

### runeReverseOffset

[ref: #symbol-runereverseoffset]

Returns a tuple with the byte offset of the rune at position rev in s, counting from the end (starting with 1) and the total number of runes in the string.

**Input:**
- `s: string`
- `rev: Positive`

**Output:** `(int, int)`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a tuple with the byte offset of the rune at position rev in s, counting from the end (starting with 1) and the total number of runes in the string.

Returns a negative value for offset if there are too few runes in the string to satisfy the request.

**Beware:** This can lead to unoptimized code and slow execution! Most problems can be solved more efficiently by using an iterator or conversion to a seq of Rune.

See also:

* [runeOffset proc](#runeOffset,string,Natural,Natural)

### runeStrAtPos

[ref: #symbol-runestratpos]

Returns the rune at position pos as UTF8 String.

**Input:**
- `s: openArray[char]`
- `pos: Natural`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the rune at position pos as UTF8 String.

**Beware:** This can lead to unoptimized code and slow execution! Most problems can be solved more efficiently by using an iterator or conversion to a seq of Rune.

See also:

* [runeAt proc](#runeAt,string,Natural)
* [runeAtPos proc](#runeAtPos,string,int)
* [fastRuneAt template](#fastRuneAt.t,string,int,untyped)

### runeStrAtPos

[ref: #symbol-runestratpos]

Returns the rune at position pos as UTF8 String.

**Input:**
- `s: string`
- `pos: Natural`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the rune at position pos as UTF8 String.

**Beware:** This can lead to unoptimized code and slow execution! Most problems can be solved more efficiently by using an iterator or conversion to a seq of Rune.

See also:

* [runeAt proc](#runeAt,string,Natural)
* [runeAtPos proc](#runeAtPos,string,int)
* [fastRuneAt template](#fastRuneAt.t,string,int,untyped)

### runeSubStr

[ref: #symbol-runesubstr]

Returns the UTF-8 substring starting at code point pos with len code points.

**Input:**
- `s: openArray[char]`
- `pos: int`
- `len: int = int.high`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the UTF-8 substring starting at code point pos with len code points.

If pos or len is negative they count from the end of the string. If len is not given it means the longest possible string.

### runeSubStr

[ref: #symbol-runesubstr]

Returns the UTF-8 substring starting at code point pos with len code points.

**Input:**
- `s: string`
- `pos: int`
- `len: int = int.high`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the UTF-8 substring starting at code point pos with len code points.

If pos or len is negative they count from the end of the string. If len is not given it means the longest possible string.

### size

[ref: #symbol-size]

**Input:**
- `r: Rune`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of bytes the rune r takes.

### split

[ref: #symbol-split]

**Input:**
- `s: openArray[char]`
- `seps: openArray[Rune] = unicodeSpaces`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nucSplitRunes"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [split iterator](#split.i,string,openArray[Rune],int), but is a proc that returns a sequence of substrings.

### split

[ref: #symbol-split]

**Input:**
- `s: openArray[char]`
- `sep: Rune`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nucSplitRune"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [split iterator](#split.i,string,Rune,int), but is a proc that returns a sequence of substrings.

### split

[ref: #symbol-split]

**Input:**
- `s: string`
- `seps: openArray[Rune] = unicodeSpaces`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [split iterator](#split.i,string,openArray[Rune],int), but is a proc that returns a sequence of substrings.

### split

[ref: #symbol-split]

**Input:**
- `s: string`
- `sep: Rune`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [split iterator](#split.i,string,Rune,int), but is a proc that returns a sequence of substrings.

### splitWhitespace

[ref: #symbol-splitwhitespace]

**Input:**
- `s: openArray[char]`

**Output:** `seq[string]`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "ncuSplitWhitespace"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [splitWhitespace](#splitWhitespace.i,string) iterator, but is a proc that returns a sequence of substrings.

### splitWhitespace

[ref: #symbol-splitwhitespace]

**Input:**
- `s: string`

**Output:** `seq[string]`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [splitWhitespace](#splitWhitespace.i,string) iterator, but is a proc that returns a sequence of substrings.

### strip

[ref: #symbol-strip]

Strips leading or trailing runes from s and returns the resulting string.

**Input:**
- `s: openArray[char]`
- `leading:  = true`
- `trailing:  = true`
- `runes: openArray[Rune] = unicodeSpaces`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nucStrip"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Strips leading or trailing runes from s and returns the resulting string.

If leading is true (default), leading runes are stripped. If trailing is true (default), trailing runes are stripped. If both are false, the string is returned unchanged.

### strip

[ref: #symbol-strip]

Strips leading or trailing runes from s and returns the resulting string.

**Input:**
- `s: string`
- `leading:  = true`
- `trailing:  = true`
- `runes: openArray[Rune] = unicodeSpaces`

**Output:** `string`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Strips leading or trailing runes from s and returns the resulting string.

If leading is true (default), leading runes are stripped. If trailing is true (default), trailing runes are stripped. If both are false, the string is returned unchanged.

### swapCase

[ref: #symbol-swapcase]

Swaps the case of runes in s.

**Input:**
- `s: openArray[char]`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Swaps the case of runes in s.

Returns a new string such that the cases of all runes are swapped if possible.

### swapCase

[ref: #symbol-swapcase]

Swaps the case of runes in s.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Swaps the case of runes in s.

Returns a new string such that the cases of all runes are swapped if possible.

### title

[ref: #symbol-title]

Converts s to a unicode title.

**Input:**
- `s: openArray[char]`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts s to a unicode title.

Returns a new string such that the first character in each word inside s is capitalized.

### title

[ref: #symbol-title]

Converts s to a unicode title.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts s to a unicode title.

Returns a new string such that the first character in each word inside s is capitalized.

### toLower

[ref: #symbol-tolower]

Converts c into lower case. This works for any rune.

**Input:**
- `c: Rune`

**Output:** `Rune`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts c into lower case. This works for any rune.

If possible, prefer toLower over toUpper.

See also:

* [toUpper proc](#toUpper,Rune)
* [toTitle proc](#toTitle,Rune)
* [isLower proc](#isLower,Rune)

### toLower

[ref: #symbol-tolower]

**Input:**
- `s: openArray[char]`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nuc$1Str"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts s into lower-case runes.

### toLower

[ref: #symbol-tolower]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts s into lower-case runes.

### toRunes

[ref: #symbol-torunes]

Obtains a sequence containing the Runes in s.

**Input:**
- `s: openArray[char]`

**Output:** `seq[Rune]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Obtains a sequence containing the Runes in s.

See also:

* [$ proc](#$,Rune) for a reverse operation

### toRunes

[ref: #symbol-torunes]

Obtains a sequence containing the Runes in s.

**Input:**
- `s: string`

**Output:** `seq[Rune]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Obtains a sequence containing the Runes in s.

See also:

* [$ proc](#$,Rune) for a reverse operation

### toTitle

[ref: #symbol-totitle]

Converts c to title case.

**Input:**
- `c: Rune`

**Output:** `Rune`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts c to title case.

See also:

* [toLower proc](#toLower,Rune)
* [toUpper proc](#toUpper,Rune)
* [isTitle proc](#isTitle,Rune)

### toUpper

[ref: #symbol-toupper]

Converts c into upper case. This works for any rune.

**Input:**
- `c: Rune`

**Output:** `Rune`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts c into upper case. This works for any rune.

If possible, prefer toLower over toUpper.

See also:

* [toLower proc](#toLower,Rune)
* [toTitle proc](#toTitle,Rune)
* [isUpper proc](#isUpper,Rune)

### toUpper

[ref: #symbol-toupper]

**Input:**
- `s: openArray[char]`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nuc$1Str"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts s into upper-case runes.

### toUpper

[ref: #symbol-toupper]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts s into upper-case runes.

### toUTF8

[ref: #symbol-toutf8]

Converts a rune into its UTF-8 representation.

**Input:**
- `c: Rune`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a rune into its UTF-8 representation.

See also:

* [validateUtf8 proc](#validateUtf8,string)
* [$ proc](#$,Rune) alias for toUTF8
* [utf8 iterator](#utf8.i,string)
* [fastToUTF8Copy template](#fastToUTF8Copy.t,Rune,string,int)

### translate

[ref: #symbol-translate]

Translates words in a string using the replacements proc to substitute words inside s with their replacements.

**Input:**
- `s: openArray[char]`
- `replacements: proc (key: string): string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `effectsOf: replacements`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Translates words in a string using the replacements proc to substitute words inside s with their replacements.

replacements is any proc that takes a word and returns a new word to fill it's place.

### translate

[ref: #symbol-translate]

Translates words in a string using the replacements proc to substitute words inside s with their replacements.

**Input:**
- `s: string`
- `replacements: proc (key: string): string`

**Output:** `string`
**Pragmas:** `effectsOf: replacements`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Translates words in a string using the replacements proc to substitute words inside s with their replacements.

replacements is any proc that takes a word and returns a new word to fill it's place.

### validateUtf8

[ref: #symbol-validateutf8]

Returns the position of the invalid byte in s if the string s does not hold valid UTF-8 data. Otherwise -1 is returned.

**Input:**
- `s: openArray[char]`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the position of the invalid byte in s if the string s does not hold valid UTF-8 data. Otherwise -1 is returned.

See also:

* [toUTF8 proc](#toUTF8,Rune)
* [$ proc](#$,Rune) alias for toUTF8
* [fastToUTF8Copy template](#fastToUTF8Copy.t,Rune,string,int)

### validateUtf8

[ref: #symbol-validateutf8]

Returns the position of the invalid byte in s if the string s does not hold valid UTF-8 data. Otherwise -1 is returned.

**Input:**
- `s: string`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the position of the invalid byte in s if the string s does not hold valid UTF-8 data. Otherwise -1 is returned.

See also:

* [toUTF8 proc](#toUTF8,Rune)
* [$ proc](#$,Rune) alias for toUTF8
* [fastToUTF8Copy template](#fastToUTF8Copy.t,Rune,string,int)

## Template

### fastRuneAt

[ref: #symbol-fastruneat]

Returns the rune s[i] in result.

**Input:**
- `s: openArray[char] or string`
- `i: int`
- `result: untyped`
- `doInc:  = true`

**Output:** *(none)*
**Generic parameters:** `s:type`

Returns the rune s[i] in result.

If doInc == true (default), i is incremented by the number of bytes that have been processed.


[Prev](unicode_1.md) | [Next](unicode_3.md)
