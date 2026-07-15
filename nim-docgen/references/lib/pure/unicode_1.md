---
source_hash: 3c32a13cf2f9bcf5
source_path: lib/pure/unicode.nim
---

# unicode

[ref: #module-unicode]

This module provides support to handle the Unicode UTF-8 encoding.

There are no specialized insert, delete, add and contains procedures for seq[Rune] in this module because the generic variants of these procedures in the system module already work with it.

The current version is compatible with Unicode v12.0.0.

**See also:**

* [strutils module](strutils.html)
* [unidecode module](unidecode.html)
* [encodings module](encodings.html)

## Examples

```nim
let
  someString = "öÑ"
  someRunes = toRunes(someString)
doAssert $someRunes == someString
```

```nim
let
  a = "ú".runeAt(0)
  b = "ü".runeAt(0)
doAssert a <% b
```

```nim
let
  a = "ú".runeAt(0)
  b = "ü".runeAt(0)
doAssert a <=% b
```

```nim
var s = "abc"
let c = "ä".runeAt(0)
s.add(c)
doAssert s == "abcä"
```

```nim
assert align("abc", 4) == " abc"
assert align("a", 0) == "a"
assert align("1232", 6) == "  1232"
assert align("1232", 6, '#'.Rune) == "##1232"
assert align("Åge", 5) == "  Åge"
assert align("×", 4, '_'.Rune) == "___×"
```

```nim
assert align("abc", 4) == " abc"
assert align("a", 0) == "a"
assert align("1232", 6) == "  1232"
assert align("1232", 6, '#'.Rune) == "##1232"
assert align("Åge", 5) == "  Åge"
assert align("×", 4, '_'.Rune) == "___×"
```

```nim
assert alignLeft("abc", 4) == "abc "
assert alignLeft("a", 0) == "a"
assert alignLeft("1232", 6) == "1232  "
assert alignLeft("1232", 6, '#'.Rune) == "1232##"
assert alignLeft("Åge", 5) == "Åge  "
assert alignLeft("×", 4, '_'.Rune) == "×___"
```

```nim
assert alignLeft("abc", 4) == "abc "
assert alignLeft("a", 0) == "a"
assert alignLeft("1232", 6) == "1232  "
assert alignLeft("1232", 6, '#'.Rune) == "1232##"
assert alignLeft("Åge", 5) == "Åge  "
assert alignLeft("×", 4, '_'.Rune) == "×___"
```

```nim
doAssert capitalize("βeta") == "Βeta"
```

```nim
doAssert capitalize("βeta") == "Βeta"
```

```nim
let a = "añyóng"
doAssert a.graphemeLen(1) == 2 ## ñ
doAssert a.graphemeLen(2) == 1
doAssert a.graphemeLen(4) == 2 ## ó
```

```nim
let a = "añyóng"
doAssert a.graphemeLen(1) == 2 ## ñ
doAssert a.graphemeLen(2) == 1
doAssert a.graphemeLen(4) == 2 ## ó
```

```nim
let a = "añyóng"
doAssert a.isAlpha
```

```nim
let a = "añyóng"
doAssert a.isAlpha
```

```nim
let a = "\t\l \v\r\f"
doAssert a.isSpace
```

```nim
let a = "\t\l \v\r\f"
doAssert a.isSpace
```

```nim
let a = "ñ".runeAt(0)
doAssert a.repeat(5) == "ñññññ"
```

```nim
assert reversed("Reverse this!") == "!siht esreveR"
assert reversed("先秦兩漢") == "漢兩秦先"
assert reversed("as⃝df̅") == "f̅ds⃝a"
assert reversed("a⃞b⃞c⃞") == "c⃞b⃞a⃞"
```

```nim
assert reversed("Reverse this!") == "!siht esreveR"
assert reversed("先秦兩漢") == "漢兩秦先"
assert reversed("as⃝df̅") == "f̅ds⃝a"
assert reversed("a⃞b⃞c⃞") == "c⃞b⃞a⃞"
```

```nim
let a = "añyóng"
doAssert a.runeAt(1) == "ñ".runeAt(0)
doAssert a.runeAt(2) == "ñ".runeAt(1)
doAssert a.runeAt(3) == "y".runeAt(0)
```

```nim
let a = "añyóng"
doAssert a.runeAt(1) == "ñ".runeAt(0)
doAssert a.runeAt(2) == "ñ".runeAt(1)
doAssert a.runeAt(3) == "y".runeAt(0)
```

```nim
let a = "añyóng"
doAssert a.runeLen == 6
## note: a.len == 8
```

```nim
let a = "añyóng"
doAssert a.runeLen == 6
## note: a.len == 8
```

```nim
let a = "añyóng"
doAssert a.runeLenAt(0) == 1
doAssert a.runeLenAt(1) == 2
```

```nim
let a = "añyóng"
doAssert a.runeLenAt(0) == 1
doAssert a.runeLenAt(1) == 2
```

```nim
let a = "añyóng"
doAssert a.runeOffset(1) == 1
doAssert a.runeOffset(3) == 4
doAssert a.runeOffset(4) == 6
```

```nim
let a = "añyóng"
doAssert a.runeOffset(1) == 1
doAssert a.runeOffset(3) == 4
doAssert a.runeOffset(4) == 6
```

```nim
let s = "Hänsel  ««: 10,00€"
doAssert(runeSubStr(s, 0, 2) == "Hä")
doAssert(runeSubStr(s, 10, 1) == ":")
doAssert(runeSubStr(s, -6) == "10,00€")
doAssert(runeSubStr(s, 10) == ": 10,00€")
doAssert(runeSubStr(s, 12, 5) == "10,00")
doAssert(runeSubStr(s, -6, 3) == "10,")
```

```nim
let s = "Hänsel  ««: 10,00€"
doAssert(runeSubStr(s, 0, 2) == "Hä")
doAssert(runeSubStr(s, 10, 1) == ":")
doAssert(runeSubStr(s, -6) == "10,00€")
doAssert(runeSubStr(s, 10) == ": 10,00€")
doAssert(runeSubStr(s, 12, 5) == "10,00")
doAssert(runeSubStr(s, -6, 3) == "10,")
```

```nim
let a = toRunes "aá"
doAssert size(a[0]) == 1
doAssert size(a[1]) == 2
```

```nim
let a = "\táñyóng   "
doAssert a.strip == "áñyóng"
doAssert a.strip(leading = false) == "\táñyóng"
doAssert a.strip(trailing = false) == "áñyóng   "
```

```nim
let a = "\táñyóng   "
doAssert a.strip == "áñyóng"
doAssert a.strip(leading = false) == "\táñyóng"
doAssert a.strip(trailing = false) == "áñyóng   "
```

```nim
doAssert swapCase("Αlpha Βeta Γamma") == "αLPHA βETA γAMMA"
```

```nim
doAssert swapCase("Αlpha Βeta Γamma") == "αLPHA βETA γAMMA"
```

```nim
doAssert title("αlpha βeta γamma") == "Αlpha Βeta Γamma"
```

```nim
doAssert title("αlpha βeta γamma") == "Αlpha Βeta Γamma"
```

```nim
doAssert toLower("ABΓ") == "abγ"
```

```nim
doAssert toLower("ABΓ") == "abγ"
```

```nim
let a = toRunes("aáä")
doAssert a == @["a".runeAt(0), "á".runeAt(0), "ä".runeAt(0)]
```

```nim
let a = toRunes("aáä")
doAssert a == @["a".runeAt(0), "á".runeAt(0), "ä".runeAt(0)]
```

```nim
doAssert toUpper("abγ") == "ABΓ"
```

```nim
doAssert toUpper("abγ") == "ABΓ"
```

```nim
let a = "añyóng"
doAssert a.runeAt(1).toUTF8 == "ñ"
```

```nim
proc wordToNumber(s: string): string =
  case s
  of "one": "1"
  of "two": "2"
  else: s
let a = "one two three four"
doAssert a.translate(wordToNumber) == "1 2 three four"
```

```nim
proc wordToNumber(s: string): string =
  case s
  of "one": "1"
  of "two": "2"
  else: s
let a = "one two three four"
doAssert a.translate(wordToNumber) == "1 2 three four"
```

```nim
import std/sequtils

assert toSeq(split(";;hÃllo;this;is;an;;example;;;是", ";".runeAt(0))) ==
  @["", "", "hÃllo", "this", "is", "an", "", "example", "", "", "是"]
```

```nim
import std/sequtils

assert toSeq("hÃllo\lthis\lis an\texample\l是".split) ==
  @["hÃllo", "this", "is", "an", "example", "是"]

# And the following code splits the same string using a sequence of Runes.
assert toSeq(split("añyóng:hÃllo;是$example", ";:$".toRunes)) ==
  @["añyóng", "hÃllo", "是", "example"]

# example with a `Rune` separator and unused one `;`:
assert toSeq(split("ab是de:f:", ";:是".toRunes)) == @["ab", "de", "f", ""]

# Another example that splits a string containing a date.
let date = "2012-11-20T22:08:08.398990"

assert toSeq(split(date, " -:T".toRunes)) ==
  @["2012", "11", "20", "22", "08", "08.398990"]
```

```nim
import std/sequtils

assert toSeq(split(";;hÃllo;this;is;an;;example;;;是", ";".runeAt(0))) ==
  @["", "", "hÃllo", "this", "is", "an", "", "example", "", "", "是"]
```

```nim
import std/sequtils

assert toSeq("hÃllo\lthis\lis an\texample\l是".split) ==
  @["hÃllo", "this", "is", "an", "example", "是"]

# And the following code splits the same string using a sequence of Runes.
assert toSeq(split("añyóng:hÃllo;是$example", ";:$".toRunes)) ==
  @["añyóng", "hÃllo", "是", "example"]

# example with a `Rune` separator and unused one `;`:
assert toSeq(split("ab是de:f:", ";:是".toRunes)) == @["ab", "de", "f", ""]

# Another example that splits a string containing a date.
let date = "2012-11-20T22:08:08.398990"

assert toSeq(split(date, " -:T".toRunes)) ==
  @["2012", "11", "20", "22", "08", "08.398990"]
```

## Iterator

### runes

[ref: #symbol-runes]

**Input:**
- `s: openArray[char]`

**Output:** `Rune`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over any rune of the string s returning runes.

### runes

[ref: #symbol-runes]

**Input:**
- `s: string`

**Output:** `Rune`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over any rune of the string s returning runes.

### split

[ref: #symbol-split]

Splits the unicode string s into substrings using a group of separators.

**Input:**
- `s: openArray[char]`
- `seps: openArray[Rune] = unicodeSpaces`
- `maxsplit: int = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the unicode string s into substrings using a group of separators.

Substrings are separated by a substring containing only seps.

### split

[ref: #symbol-split]

**Input:**
- `s: openArray[char]`
- `sep: Rune`
- `maxsplit: int = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the unicode string s into substrings using a single separator. Substrings are separated by the rune sep.

### split

[ref: #symbol-split]

Splits the unicode string s into substrings using a group of separators.

**Input:**
- `s: string`
- `seps: openArray[Rune] = unicodeSpaces`
- `maxsplit: int = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the unicode string s into substrings using a group of separators.

Substrings are separated by a substring containing only seps.

### split

[ref: #symbol-split]

**Input:**
- `s: string`
- `sep: Rune`
- `maxsplit: int = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the unicode string s into substrings using a single separator. Substrings are separated by the rune sep.

### splitWhitespace

[ref: #symbol-splitwhitespace]

**Input:**
- `s: openArray[char]`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits a unicode string at whitespace runes.

### splitWhitespace

[ref: #symbol-splitwhitespace]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits a unicode string at whitespace runes.

### utf8

[ref: #symbol-utf8]

Iterates over any rune of the string s returning utf8 values.

**Input:**
- `s: openArray[char]`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over any rune of the string s returning utf8 values.

See also:

* [validateUtf8 proc](#validateUtf8,string)
* [toUTF8 proc](#toUTF8,Rune)
* [$ proc](#$,Rune) alias for toUTF8
* [fastToUTF8Copy template](#fastToUTF8Copy.t,Rune,string,int)

### utf8

[ref: #symbol-utf8]

Iterates over any rune of the string s returning utf8 values.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over any rune of the string s returning utf8 values.

See also:

* [validateUtf8 proc](#validateUtf8,string)
* [toUTF8 proc](#toUTF8,Rune)
* [$ proc](#$,Rune) alias for toUTF8
* [fastToUTF8Copy template](#fastToUTF8Copy.t,Rune,string,int)

## Proc

### `$`

[ref: #symbol-]

An alias for [toUTF8](#toUTF8,Rune).

**Input:**
- `rune: Rune`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

An alias for [toUTF8](#toUTF8,Rune).

See also:

* [validateUtf8 proc](#validateUtf8,string)
* [fastToUTF8Copy template](#fastToUTF8Copy.t,Rune,string,int)

### `$`

[ref: #symbol-]

Converts a sequence of Runes to a string.

**Input:**
- `runes: seq[Rune]`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a sequence of Runes to a string.

See also:

* [toRunes](#toRunes,string) for a reverse operation

### `&lt;%`

[ref: #symbol-lt]

**Input:**
- `a: Rune`
- `b: Rune`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if code point of a is smaller than code point of b.

### `&lt;=%`

[ref: #symbol-lt]

**Input:**
- `a: Rune`
- `b: Rune`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if code point of a is smaller or equal to code point of b.

### `==`

[ref: #symbol-]

**Input:**
- `a: Rune`
- `b: Rune`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if two runes are equal.

### add

[ref: #symbol-add]

**Input:**
- `s: var string`
- `c: Rune`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds a rune c to a string s.

### align

[ref: #symbol-align]

Aligns a unicode string s with padding, so that it has a rune-length of count.

**Input:**
- `s: openArray[char]`
- `count: Natural`
- `padding:  = ' '.Rune`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nucAlignString"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Aligns a unicode string s with padding, so that it has a rune-length of count.

padding characters (by default spaces) are added before s resulting in right alignment. If s.runelen >= count, no spaces are added and s is returned unchanged. If you need to left align a string use the [alignLeft proc](#alignLeft,string,Natural).

### align

[ref: #symbol-align]

Aligns a unicode string s with padding, so that it has a rune-length of count.

**Input:**
- `s: string`
- `count: Natural`
- `padding:  = ' '.Rune`

**Output:** `string`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Aligns a unicode string s with padding, so that it has a rune-length of count.

padding characters (by default spaces) are added before s resulting in right alignment. If s.runelen >= count, no spaces are added and s is returned unchanged. If you need to left align a string use the [alignLeft proc](#alignLeft,string,Natural).

### alignLeft

[ref: #symbol-alignleft]

Left-aligns a unicode string s with padding, so that it has a rune-length of count.

**Input:**
- `s: openArray[char]`
- `count: Natural`
- `padding:  = ' '.Rune`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Left-aligns a unicode string s with padding, so that it has a rune-length of count.

padding characters (by default spaces) are added after s resulting in left alignment. If s.runelen >= count, no spaces are added and s is returned unchanged. If you need to right align a string use the [align proc](#align,string,Natural).

### alignLeft

[ref: #symbol-alignleft]

Left-aligns a unicode string s with padding, so that it has a rune-length of count.

**Input:**
- `s: string`
- `count: Natural`
- `padding:  = ' '.Rune`

**Output:** `string`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Left-aligns a unicode string s with padding, so that it has a rune-length of count.

padding characters (by default spaces) are added after s resulting in left alignment. If s.runelen >= count, no spaces are added and s is returned unchanged. If you need to right align a string use the [align proc](#align,string,Natural).

### capitalize

[ref: #symbol-capitalize]

**Input:**
- `s: openArray[char]`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the first character of s into an upper-case rune.

### capitalize

[ref: #symbol-capitalize]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the first character of s into an upper-case rune.

### cmpRunesIgnoreCase

[ref: #symbol-cmprunesignorecase]

Compares two UTF-8 strings and ignores the case. Returns:

**Input:**
- `a: openArray[char]`
- `b: openArray[char]`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two UTF-8 strings and ignores the case. Returns:

0 if a == b  
< 0 if a < b  
> 0 if a > b

### cmpRunesIgnoreCase

[ref: #symbol-cmprunesignorecase]

Compares two UTF-8 strings and ignores the case. Returns:

**Input:**
- `a: string`
- `b: string`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two UTF-8 strings and ignores the case. Returns:

0 if a == b  
< 0 if a < b  
> 0 if a > b

### graphemeLen

[ref: #symbol-graphemelen]

**Input:**
- `s: openArray[char]`
- `i: Natural`

**Output:** `Natural`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The number of bytes belonging to byte index s[i], including following combining code units.

### graphemeLen

[ref: #symbol-graphemelen]

**Input:**
- `s: string`
- `i: Natural`

**Output:** `Natural`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The number of bytes belonging to byte index s[i], including following combining code unit.

### isAlpha

[ref: #symbol-isalpha]

Returns true if c is an *alpha* rune (i.e., a letter).

**Input:**
- `c: Rune`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if c is an *alpha* rune (i.e., a letter).

See also:

* [isLower proc](#isLower,Rune)
* [isTitle proc](#isTitle,Rune)
* [isAlpha proc](#isAlpha,Rune)
* [isWhiteSpace proc](#isWhiteSpace,Rune)
* [isCombining proc](#isCombining,Rune)

### isAlpha

[ref: #symbol-isalpha]

**Input:**
- `s: openArray[char]`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nuc$1Str"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s contains all alphabetic runes.

### isAlpha

[ref: #symbol-isalpha]

**Input:**
- `s: string`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s contains all alphabetic runes.

### isCombining

[ref: #symbol-iscombining]

Returns true if c is a Unicode combining code unit.

**Input:**
- `c: Rune`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if c is a Unicode combining code unit.

See also:

* [isLower proc](#isLower,Rune)
* [isUpper proc](#isUpper,Rune)
* [isTitle proc](#isTitle,Rune)
* [isAlpha proc](#isAlpha,Rune)

### isLower

[ref: #symbol-islower]

Returns true if c is a lower case rune.

**Input:**
- `c: Rune`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if c is a lower case rune.

If possible, prefer isLower over isUpper.

See also:

* [toLower proc](#toLower,Rune)
* [isUpper proc](#isUpper,Rune)
* [isTitle proc](#isTitle,Rune)

### isSpace

[ref: #symbol-isspace]

**Input:**
- `s: openArray[char]`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nuc$1Str"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s contains all whitespace runes.

### isSpace

[ref: #symbol-isspace]

**Input:**
- `s: string`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s contains all whitespace runes.

### isTitle

[ref: #symbol-istitle]

Returns true if c is a Unicode titlecase code point.

**Input:**
- `c: Rune`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if c is a Unicode titlecase code point.

See also:

* [toTitle proc](#toTitle,Rune)
* [isLower proc](#isLower,Rune)
* [isUpper proc](#isUpper,Rune)
* [isAlpha proc](#isAlpha,Rune)
* [isWhiteSpace proc](#isWhiteSpace,Rune)

### isUpper

[ref: #symbol-isupper]

Returns true if c is a upper case rune.

**Input:**
- `c: Rune`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nuc$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if c is a upper case rune.

If possible, prefer isLower over isUpper.

See also:

* [toUpper proc](#toUpper,Rune)
* [isLower proc](#isLower,Rune)
* [isTitle proc](#isTitle,Rune)
* [isAlpha proc](#isAlpha,Rune)
* [isWhiteSpace proc](#isWhiteSpace,Rune)


[Next](unicode_2.md)
