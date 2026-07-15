---
source_hash: 47f6f646c0362c02
source_path: lib/pure/strutils.nim
---

### removePrefix

[ref: #symbol-removeprefix]

Remove the first matching prefix (in-place) from a string.

**Input:**
- `s: var string`
- `prefix: string`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nsuRemovePrefixString"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Remove the first matching prefix (in-place) from a string.

See also:

* [removeSuffix func](#removeSuffix,string,string)
* [startsWith func](#startsWith,string,string)

### removeSuffix

[ref: #symbol-removesuffix]

Removes all characters from chars from the end of the string s (in-place).

**Input:**
- `s: var string`
- `chars: set[char] = Newlines`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nsuRemoveSuffixCharSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Removes all characters from chars from the end of the string s (in-place).

See also:

* [removePrefix func](#removePrefix,string,set[char])

### removeSuffix

[ref: #symbol-removesuffix]

Removes all occurrences of a single character (in-place) from the end of a string.

**Input:**
- `s: var string`
- `c: char`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nsuRemoveSuffixChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Removes all occurrences of a single character (in-place) from the end of a string.

See also:

* [removePrefix func](#removePrefix,string,char)
* [endsWith func](#endsWith,string,char)

### removeSuffix

[ref: #symbol-removesuffix]

Remove the first matching suffix (in-place) from a string.

**Input:**
- `s: var string`
- `suffix: string`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nsuRemoveSuffixString"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Remove the first matching suffix (in-place) from a string.

See also:

* [removePrefix func](#removePrefix,string,string)
* [endsWith func](#endsWith,string,string)

### repeat

[ref: #symbol-repeat]

**Input:**
- `c: char`
- `count: Natural`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuRepeatChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a string of length count consisting only of the character c.

### repeat

[ref: #symbol-repeat]

**Input:**
- `s: string`
- `n: Natural`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuRepeatStr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns string s concatenated n times.

### replace

[ref: #symbol-replace]

Replaces every occurrence of the string sub in s with the string by.

**Input:**
- `s: string`
- `sub: string`
- `by:  = ""`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuReplaceStr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Replaces every occurrence of the string sub in s with the string by.

See also:

* [find func](#find,string,string,Natural,int)
* [replace func](#replace,string,char,char) for replacing single characters
* [replaceWord func](#replaceWord,string,string,string)
* [multiReplace func](#multiReplace,string,varargs[]) for substrings
* [multiReplace func](#multiReplace,openArray[char],varargs[]) for single characters

### replace

[ref: #symbol-replace]

Replaces every occurrence of the character sub in s with the character by.

**Input:**
- `s: string`
- `sub: char`
- `by: char`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuReplaceChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Replaces every occurrence of the character sub in s with the character by.

Optimized version of [replace](#replace,string,string,string) for characters.

See also:

* [find func](#find,string,char,Natural,int)
* [replaceWord func](#replaceWord,string,string,string)
* [multiReplace func](#multiReplace,string,varargs[]) for substrings
* [multiReplace func](#multiReplace,openArray[char],varargs[]) for single characters

### replaceWord

[ref: #symbol-replaceword]

Replaces every occurrence of the string sub in s with the string by.

**Input:**
- `s: string`
- `sub: string`
- `by:  = ""`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuReplaceWord"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Replaces every occurrence of the string sub in s with the string by.

Each occurrence of sub has to be surrounded by word boundaries (comparable to \b in regular expressions), otherwise it is not replaced.

### rfind

[ref: #symbol-rfind]

Searches for sub in s inside range start..last (both ends included) in reverse -- starting at high indexes and moving lower to the first character or start. If last is unspecified, it defaults to s.high (the last element).

**Input:**
- `s: string`
- `sub: char`
- `start: Natural = 0`
- `last:  = -1`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuRFindChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Searches for sub in s inside range start..last (both ends included) in reverse -- starting at high indexes and moving lower to the first character or start. If last is unspecified, it defaults to s.high (the last element).

Searching is case-sensitive. If sub is not in s, -1 is returned. Otherwise the index returned is relative to s[0], not start. Subtract start from the result for a start-origin index.

See also:

* [find func](#find,string,char,Natural,int)

### rfind

[ref: #symbol-rfind]

Searches for chars in s inside range start..last (both ends included) in reverse -- starting at high indexes and moving lower to the first character or start. If last is unspecified, it defaults to s.high (the last element).

**Input:**
- `s: string`
- `chars: set[char]`
- `start: Natural = 0`
- `last:  = -1`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuRFindCharSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Searches for chars in s inside range start..last (both ends included) in reverse -- starting at high indexes and moving lower to the first character or start. If last is unspecified, it defaults to s.high (the last element).

If s contains none of the characters in chars, -1 is returned. Otherwise the index returned is relative to s[0], not start. Subtract start from the result for a start-origin index.

See also:

* [find func](#find,string,set[char],Natural,int)

### rfind

[ref: #symbol-rfind]

Searches for sub in s inside range start..last (both ends included) included) in reverse -- starting at high indexes and moving lower to the first character or start. If last is unspecified, it defaults to s.high (the last element).

**Input:**
- `s: string`
- `sub: string`
- `start: Natural = 0`
- `last:  = -1`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuRFindStr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Searches for sub in s inside range start..last (both ends included) included) in reverse -- starting at high indexes and moving lower to the first character or start. If last is unspecified, it defaults to s.high (the last element).

Searching is case-sensitive. If sub is not in s, -1 is returned. Otherwise the index returned is relative to s[0], not start. Subtract start from the result for a start-origin index.

See also:

* [find func](#find,string,string,Natural,int)

### rsplit

[ref: #symbol-rsplit]

The same as the [rsplit iterator](#rsplit.i,string,char,int), but is a func that returns a sequence of substrings in original order.

**Input:**
- `s: string`
- `sep: char`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `gcsafe`, `extern: "nsuRSplitChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [rsplit iterator](#rsplit.i,string,char,int), but is a func that returns a sequence of substrings in original order.

A possible common use case for rsplit is path manipulation, particularly on systems that don't use a common delimiter.

For example, if a system had # as a delimiter, you could do the following to get the tail of the path:

```
var tailSplit = rsplit("Root#Object#Method#Index", '#', maxsplit=1)
```

Results in tailSplit containing:

```
@["Root#Object#Method", "Index"]
```

See also:

* [rsplit iterator](#rsplit.i,string,char,int)
* [split func](#split,string,char,int)
* [splitLines func](#splitLines,string)
* [splitWhitespace func](#splitWhitespace,string,int)

### rsplit

[ref: #symbol-rsplit]

The same as the [rsplit iterator](#rsplit.i,string,set[char],int), but is a func that returns a sequence of substrings in original order.

**Input:**
- `s: string`
- `seps: set[char] = Whitespace`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `gcsafe`, `extern: "nsuRSplitCharSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [rsplit iterator](#rsplit.i,string,set[char],int), but is a func that returns a sequence of substrings in original order.

A possible common use case for rsplit is path manipulation, particularly on systems that don't use a common delimiter.

For example, if a system had # as a delimiter, you could do the following to get the tail of the path:

```
var tailSplit = rsplit("Root#Object#Method#Index", {'#'}, maxsplit=1)
```

Results in tailSplit containing:

```
@["Root#Object#Method", "Index"]
```

**Note:**
Empty separator set results in returning an original string, following the interpretation "split by no element".

See also:

* [rsplit iterator](#rsplit.i,string,set[char],int)
* [split func](#split,string,set[char],int)
* [splitLines func](#splitLines,string)
* [splitWhitespace func](#splitWhitespace,string,int)

### rsplit

[ref: #symbol-rsplit]

The same as the [rsplit iterator](#rsplit.i,string,string,int,bool), but is a func that returns a sequence of substrings in original order.

**Input:**
- `s: string`
- `sep: string`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `gcsafe`, `extern: "nsuRSplitString"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [rsplit iterator](#rsplit.i,string,string,int,bool), but is a func that returns a sequence of substrings in original order.

A possible common use case for rsplit is path manipulation, particularly on systems that don't use a common delimiter.

For example, if a system had # as a delimiter, you could do the following to get the tail of the path:

```
var tailSplit = rsplit("Root#Object#Method#Index", "#", maxsplit=1)
```

Results in tailSplit containing:

```
@["Root#Object#Method", "Index"]
```

**Note:**
Empty separator string results in returning an original string, following the interpretation "split by no element".

See also:

* [rsplit iterator](#rsplit.i,string,string,int,bool)
* [split func](#split,string,string,int)
* [splitLines func](#splitLines,string)
* [splitWhitespace func](#splitWhitespace,string,int)

### spaces

[ref: #symbol-spaces]

Returns a string with n space characters. You can use this func to left align strings.

**Input:**
- `n: Natural`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a string with n space characters. You can use this func to left align strings.

See also:

* [align func](#align,string,Natural,char)
* [alignLeft func](#alignLeft,string,Natural,char)
* [indent func](#indent,string,Natural,string)
* [center func](#center,string,int,char)

### split

[ref: #symbol-split]

The same as the [split iterator](#split.i,string,char,int) (see its documentation), but is a func that returns a sequence of substrings.

**Input:**
- `s: string`
- `sep: char`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `gcsafe`, `extern: "nsuSplitChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [split iterator](#split.i,string,char,int) (see its documentation), but is a func that returns a sequence of substrings.

See also:

* [split iterator](#split.i,string,char,int)
* [rsplit func](#rsplit,string,char,int)
* [splitLines func](#splitLines,string)
* [splitWhitespace func](#splitWhitespace,string,int)

### split

[ref: #symbol-split]

The same as the [split iterator](#split.i,string,set[char],int) (see its documentation), but is a func that returns a sequence of substrings.

**Input:**
- `s: string`
- `seps: set[char] = Whitespace`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `gcsafe`, `extern: "nsuSplitCharSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [split iterator](#split.i,string,set[char],int) (see its documentation), but is a func that returns a sequence of substrings.

**Note:**
Empty separator set results in returning an original string, following the interpretation "split by no element".

See also:

* [split iterator](#split.i,string,set[char],int)
* [rsplit func](#rsplit,string,set[char],int)
* [splitLines func](#splitLines,string)
* [splitWhitespace func](#splitWhitespace,string,int)

### split

[ref: #symbol-split]

Splits the string s into substrings using a string separator.

**Input:**
- `s: string`
- `sep: string`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `gcsafe`, `extern: "nsuSplitString"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s into substrings using a string separator.

Substrings are separated by the string sep. This is a wrapper around the [split iterator](#split.i,string,string,int).

**Note:**
Empty separator string results in returning an original string, following the interpretation "split by no element".

See also:

* [split iterator](#split.i,string,string,int)
* [rsplit func](#rsplit,string,string,int)
* [splitLines func](#splitLines,string)
* [splitWhitespace func](#splitWhitespace,string,int)

### splitLines

[ref: #symbol-splitlines]

The same as the [splitLines iterator](#splitLines.i,string) (see its documentation), but is a func that returns a sequence of substrings.

**Input:**
- `s: string`
- `keepEol:  = false`

**Output:** `seq[string]`
**Pragmas:** `gcsafe`, `extern: "nsuSplitLines"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [splitLines iterator](#splitLines.i,string) (see its documentation), but is a func that returns a sequence of substrings.

See also:

* [splitLines iterator](#splitLines.i,string)
* [splitWhitespace func](#splitWhitespace,string,int)
* [countLines func](#countLines,string)

### splitWhitespace

[ref: #symbol-splitwhitespace]

The same as the [splitWhitespace iterator](#splitWhitespace.i,string,int) (see its documentation), but is a func that returns a sequence of substrings.

**Input:**
- `s: string`
- `maxsplit: int = -1`

**Output:** `seq[string]`
**Pragmas:** `gcsafe`, `extern: "nsuSplitWhitespace"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as the [splitWhitespace iterator](#splitWhitespace.i,string,int) (see its documentation), but is a func that returns a sequence of substrings.

See also:

* [splitWhitespace iterator](#splitWhitespace.i,string,int)
* [splitLines func](#splitLines,string)

### startsWith

[ref: #symbol-startswith]

Returns true if s starts with character prefix.

**Input:**
- `s: string`
- `prefix: char`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s starts with character prefix.

See also:

* [endsWith func](#endsWith,string,char)
* [continuesWith func](#continuesWith,string,string,Natural)
* [removePrefix func](#removePrefix,string,char)

### startsWith

[ref: #symbol-startswith]

Returns true if s starts with string prefix.

**Input:**
- `s: string`
- `prefix: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuStartsWith"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s starts with string prefix.

If prefix == "" true is returned.

See also:

* [endsWith func](#endsWith,string,string)
* [continuesWith func](#continuesWith,string,string,Natural)
* [removePrefix func](#removePrefix,string,string)

### strip

[ref: #symbol-strip]

Strips leading or trailing chars (default: whitespace characters) from s and returns the resulting string.

**Input:**
- `s: string`
- `leading:  = true`
- `trailing:  = true`
- `chars: set[char] = Whitespace`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuStrip"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Strips leading or trailing chars (default: whitespace characters) from s and returns the resulting string.

If leading is true (default), leading chars are stripped. If trailing is true (default), trailing chars are stripped. If both are false, the string is returned unchanged.

See also:

* [strip proc](strbasics.html#strip,string,set[char]) Inplace version.
* [stripLineEnd func](#stripLineEnd,string)

### stripLineEnd

[ref: #symbol-striplineend]

**Input:**
- `s: var string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Strips one of these suffixes from s in-place: \r, \n, \r\n, \f, \v (at most once instance). For example, can be useful in conjunction with osproc.execCmdEx. aka: chomp

### toBin

[ref: #symbol-tobin]

Converts x into its binary representation.

**Input:**
- `x: BiggestInt`
- `len: Positive`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuToBin"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts x into its binary representation.

The resulting string is always len characters long. No leading 0b prefix is generated.

### toHex

[ref: #symbol-tohex]

Converts x to its hexadecimal representation.

**Input:**
- `x: T`
- `len: Positive`

**Output:** `string`
**Generic parameters:** `T`

Converts x to its hexadecimal representation.

The resulting string will be exactly len characters long. No prefix like 0x is generated. x is treated as an unsigned value.

### toHex

[ref: #symbol-tohex]

**Input:**
- `x: T`

**Output:** `string`
**Generic parameters:** `T`

Shortcut for toHex(x, T.sizeof \* 2)

### toHex

[ref: #symbol-tohex]

Converts a bytes string to its hexadecimal representation.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a bytes string to its hexadecimal representation.

The output is twice the input long. No prefix like 0x is generated.

See also:

* [parseHexStr func](#parseHexStr,string) for the reverse operation

### toLowerAscii

[ref: #symbol-tolowerascii]

Returns the lower case version of character c.

**Input:**
- `c: char`

**Output:** `char`
**Pragmas:** `gcsafe`, `extern: "nsuToLowerAsciiChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the lower case version of character c.

This works only for the letters A-Z. See [unicode.toLower](unicode.html#toLower,Rune) for a version that works for any Unicode character.

See also:

* [isLowerAscii func](#isLowerAscii,char)
* [toLowerAscii func](#toLowerAscii,string) for converting a string

### toLowerAscii

[ref: #symbol-tolowerascii]

Converts string s into lower case.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuToLowerAsciiStr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts string s into lower case.

This works only for the letters A-Z. See [unicode.toLower](unicode.html#toLower,string) for a version that works for any Unicode character.

See also:

* [normalize func](#normalize,string)

### toOct

[ref: #symbol-tooct]

Converts x into its octal representation.

**Input:**
- `x: BiggestInt`
- `len: Positive`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuToOct"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts x into its octal representation.

The resulting string is always len characters long. No leading 0o prefix is generated.

Do not confuse it with [toOctal func](#toOctal,char).

### toOctal

[ref: #symbol-tooctal]

Converts a character c to its octal representation.

**Input:**
- `c: char`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuToOctal"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a character c to its octal representation.

The resulting string may not have a leading zero. Its length is always exactly 3.

Do not confuse it with [toOct func](#toOct,BiggestInt,Positive).

### toUpperAscii

[ref: #symbol-toupperascii]

Converts character c into upper case.

**Input:**
- `c: char`

**Output:** `char`
**Pragmas:** `gcsafe`, `extern: "nsuToUpperAsciiChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts character c into upper case.

This works only for the letters A-Z. See [unicode.toUpper](unicode.html#toUpper,Rune) for a version that works for any Unicode character.

See also:

* [isUpperAscii func](#isUpperAscii,char)
* [toUpperAscii func](#toUpperAscii,string) for converting a string
* [capitalizeAscii func](#capitalizeAscii,string)

### toUpperAscii

[ref: #symbol-toupperascii]

Converts string s into upper case.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuToUpperAsciiStr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts string s into upper case.

This works only for the letters A-Z. See [unicode.toUpper](unicode.html#toUpper,string) for a version that works for any Unicode character.

See also:

* [capitalizeAscii func](#capitalizeAscii,string)

### trimZeros

[ref: #symbol-trimzeros]

Trim trailing zeros from a formatted floating point value x (must be declared as var).

**Input:**
- `x: var string`
- `decimalSep:  = '.'`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Trim trailing zeros from a formatted floating point value x (must be declared as var).

This modifies x itself, it does not return a copy.

### unescape

[ref: #symbol-unescape]

Unescapes a string s.

**Input:**
- `s: string`
- `prefix:  = "\""`
- `suffix:  = "\""`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuUnescape"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Unescapes a string s.

This complements [escape func](#escape,string,string,string) as it performs the opposite operations.

If s does not begin with prefix and end with suffix a ValueError exception will be raised.

### unindent

[ref: #symbol-unindent]

Unindents each line in s by count amount of padding.

**Input:**
- `s: string`
- `count: Natural = int.high`
- `padding: string = " "`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuUnindent"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unindents each line in s by count amount of padding.

**Note:** This does not preserve the new line characters used in s.

See also:

* [dedent func](#dedent,string,Natural)
* [align func](#align,string,Natural,char)
* [alignLeft func](#alignLeft,string,Natural,char)
* [spaces func](#spaces,Natural)
* [indent func](#indent,string,Natural,string)

### validIdentifier

[ref: #symbol-valididentifier]

Returns true if s is a valid identifier.

**Input:**
- `s: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuValidIdentifier"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s is a valid identifier.

A valid identifier starts with a character of the set IdentStartChars and is followed by any number of characters of the set IdentChars.

## Type

### BinaryPrefixMode

[ref: #symbol-binaryprefixmode]

```nim
BinaryPrefixMode = enum
  bpIEC, bpColloquial
```

The different names for binary prefixes.

### FloatFormatMode

[ref: #symbol-floatformatmode]

```nim
FloatFormatMode = enum
  ffDefault,                ## use the shorter floating point notation
  ffDecimal,                ## use decimal floating point notation
  ffScientific               ## use scientific notation (using `e` character)
```

The different modes of floating point formatting.

### SkipTable

[ref: #symbol-skiptable]

```nim
SkipTable = array[char, int]
```

Character table for efficient substring search.

[Prev](strutils_3.md)
