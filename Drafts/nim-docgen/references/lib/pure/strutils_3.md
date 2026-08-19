---
source_hash: 47f6f646c0362c02
source_path: lib/pure/strutils.nim
---

### escape

[ref: #symbol-escape]

Escapes a string s.

**Input:**
- `s: string`
- `prefix:  = "\""`
- `suffix:  = "\""`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuEscape"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Escapes a string s.

**Note:**
The escaping scheme is different from system.addEscapedChar.

* replaces '\0'..'\31' and '\127'..'\255' by \xHH where HH is its hexadecimal value
* replaces \ by \\
* replaces ' by \'
* replaces " by \"

The resulting string is prefixed with prefix and suffixed with suffix. Both may be empty strings.

See also:

* [addEscapedChar proc](system.html#addEscapedChar,string,char)
* [unescape func](#unescape,string,string,string) for the opposite operation

### find

[ref: #symbol-find]

Searches for sub in s inside range start..last using preprocessed table a. If last is unspecified, it defaults to s.high (the last element).

**Input:**
- `a: SkipTable`
- `s: string`
- `sub: string`
- `start: Natural = 0`
- `last:  = -1`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuFindStrA"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Searches for sub in s inside range start..last using preprocessed table a. If last is unspecified, it defaults to s.high (the last element).

Searching is case-sensitive. If sub is not in s, -1 is returned.

See also:

* [initSkipTable func](#initSkipTable,string)
* [initSkipTable func](#initSkipTable,SkipTable,string)

### find

[ref: #symbol-find]

Searches for sub in s inside range start..last (both ends included). If last is unspecified or negative, it defaults to s.high (the last element).

**Input:**
- `s: string`
- `sub: char`
- `start: Natural = 0`
- `last:  = -1`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuFindChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Searches for sub in s inside range start..last (both ends included). If last is unspecified or negative, it defaults to s.high (the last element).

Searching is case-sensitive. If sub is not in s, -1 is returned. Otherwise the index returned is relative to s[0], not start. Subtract start from the result for a start-origin index.

See also:

* [rfind func](#rfind,string,char,Natural,int)
* [replace func](#replace,string,char,char)

### find

[ref: #symbol-find]

Searches for chars in s inside range start..last (both ends included). If last is unspecified or negative, it defaults to s.high (the last element).

**Input:**
- `s: string`
- `chars: set[char]`
- `start: Natural = 0`
- `last:  = -1`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuFindCharSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Searches for chars in s inside range start..last (both ends included). If last is unspecified or negative, it defaults to s.high (the last element).

If s contains none of the characters in chars, -1 is returned. Otherwise the index returned is relative to s[0], not start. Subtract start from the result for a start-origin index.

See also:

* [rfind func](#rfind,string,set[char],Natural,int)
* [multiReplace func](#multiReplace,string,varargs[])

### find

[ref: #symbol-find]

Searches for sub in s inside range start..last (both ends included). If last is unspecified or negative, it defaults to s.high (the last element).

**Input:**
- `s: string`
- `sub: string`
- `start: Natural = 0`
- `last:  = -1`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuFindStr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Searches for sub in s inside range start..last (both ends included). If last is unspecified or negative, it defaults to s.high (the last element).

Searching is case-sensitive. If sub is not in s, -1 is returned. Otherwise the index returned is relative to s[0], not start. Subtract start from the result for a start-origin index.

See also:

* [rfind func](#rfind,string,string,Natural,int)
* [replace func](#replace,string,string,string)

### format

[ref: #symbol-format]

This is the same as formatstr % a (see [% func](#%25,string,openArray[string])) except that it supports auto stringification.

**Input:**
- `formatstr: string`
- `a: varargs[string, `$`]`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuFormatVarargs"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

This is the same as formatstr % a (see [% func](#%25,string,openArray[string])) except that it supports auto stringification.

See also:

* [strformat module](strformat.html) for string interpolation and formatting

### formatBiggestFloat

[ref: #symbol-formatbiggestfloat]

Converts a floating point value f to a string.

**Input:**
- `f: BiggestFloat`
- `format: FloatFormatMode = ffDefault`
- `precision: range[-1 .. 32] = 16`
- `decimalSep:  = '.'`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsu$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a floating point value f to a string.

If format == ffDecimal then precision is the number of digits to be printed after the decimal point. If format == ffScientific then precision is the maximum number of significant digits to be printed. precision's default value is the maximum number of meaningful digits after the decimal point for Nim's biggestFloat type.

If precision == -1, it tries to format it nicely.

### formatEng

[ref: #symbol-formateng]

Converts a floating point value f to a string using engineering notation.

**Input:**
- `f: BiggestFloat`
- `precision: range[0 .. 32] = 10`
- `trim: bool = true`
- `siPrefix: bool = false`
- `unit: string = ""`
- `decimalSep:  = '.'`
- `useUnitSpace:  = false`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a floating point value f to a string using engineering notation.

Numbers in of the range -1000.0<f<1000.0 will be formatted without an exponent. Numbers outside of this range will be formatted as a significand in the range -1000.0<f<1000.0 and an exponent that will always be an integer multiple of 3, corresponding with the SI prefix scale k, M, G, T etc for numbers with an absolute value greater than 1 and m, μ, n, p etc for numbers with an absolute value less than 1.

The default configuration (trim=true and precision=10) shows the **shortest** form that precisely (up to a maximum of 10 decimal places) displays the value. For example, 4.100000 will be displayed as 4.1 (which is mathematically identical) whereas 4.1000003 will be displayed as 4.1000003.

If trim is set to true, trailing zeros will be removed; if false, the number of digits specified by precision will always be shown.

precision can be used to set the number of digits to be shown after the decimal point or (if trim is true) the maximum number of digits to be shown.

```
 formatEng(0, 2, trim=false) == "0.00"
 formatEng(0, 2) == "0"
 formatEng(0.053, 0) == "53e-3"
 formatEng(52731234, 2) == "52.73e6"
 formatEng(-52731234, 2) == "-52.73e6"
```

If siPrefix is set to true, the number will be displayed with the SI prefix corresponding to the exponent. For example 4100 will be displayed as "4.1 k" instead of "4.1e3". Note that u is used for micro- in place of the greek letter mu (μ) as per ISO 2955. Numbers with an absolute value outside of the range 1e-18<f<1000e18 (1a<f<1000E) will be displayed with an exponent rather than an SI prefix, regardless of whether siPrefix is true.

If useUnitSpace is true, the provided unit will be appended to the string (with a space as required by the SI standard). This behaviour is slightly different to appending the unit to the result as the location of the space is altered depending on whether there is an exponent.

```
 formatEng(4100, siPrefix=true, unit="V") == "4.1 kV"
 formatEng(4.1, siPrefix=true, unit="V") == "4.1 V"
 formatEng(4.1, siPrefix=true) == "4.1" # Note lack of space
 formatEng(4100, siPrefix=true) == "4.1 k"
 formatEng(4.1, siPrefix=true, unit="") == "4.1 " # Space with unit=""
 formatEng(4100, siPrefix=true, unit="") == "4.1 k"
 formatEng(4100) == "4.1e3"
 formatEng(4100, unit="V") == "4.1e3 V"
 formatEng(4100, unit="", useUnitSpace=true) == "4.1e3 " # Space with useUnitSpace=true
```

decimalSep is used as the decimal separator.

See also:

* [strformat module](strformat.html) for string interpolation and formatting

### formatFloat

[ref: #symbol-formatfloat]

Converts a floating point value f to a string.

**Input:**
- `f: float`
- `format: FloatFormatMode = ffDefault`
- `precision: range[-1 .. 32] = 16`
- `decimalSep:  = '.'`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsu$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a floating point value f to a string.

If format == ffDecimal then precision is the number of digits to be printed after the decimal point. If format == ffScientific then precision is the maximum number of significant digits to be printed. precision's default value is the maximum number of meaningful digits after the decimal point for Nim's float type.

If precision == -1, it tries to format it nicely.

### formatSize

[ref: #symbol-formatsize]

Rounds and formats bytes.

**Input:**
- `bytes: int64`
- `decimalSep:  = '.'`
- `prefix:  = bpIEC`
- `includeSpace:  = false`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Rounds and formats bytes.

By default, uses the IEC/ISO standard binary prefixes, so 1024 will be formatted as 1KiB. Set prefix to bpColloquial to use the colloquial names from the SI standard (e.g. k for 1000 being reused as 1024).

includeSpace can be set to true to include the (SI preferred) space between the number and the unit (e.g. 1 KiB).

See also:

* [strformat module](strformat.html) for string interpolation and formatting

### fromBin

[ref: #symbol-frombin]

Parses a binary integer value from a string s.

**Input:**
- `s: string`

**Output:** `T`
**Generic parameters:** `T`

Parses a binary integer value from a string s.

If s is not a valid binary integer, ValueError is raised. s can have one of the following optional prefixes: 0b, 0B. Underscores within s are ignored.

Does not check for overflow. If the value represented by s is too big to fit into a return type, only the value of the rightmost binary digits of s is returned without producing an error.

### fromHex

[ref: #symbol-fromhex]

Parses a hex integer value from a string s.

**Input:**
- `s: string`

**Output:** `T`
**Generic parameters:** `T`

Parses a hex integer value from a string s.

If s is not a valid hex integer, ValueError is raised. s can have one of the following optional prefixes: 0x, 0X, #. Underscores within s are ignored.

Does not check for overflow. If the value represented by s is too big to fit into a return type, only the value of the rightmost hex digits of s is returned without producing an error.

### fromOct

[ref: #symbol-fromoct]

Parses an octal integer value from a string s.

**Input:**
- `s: string`

**Output:** `T`
**Generic parameters:** `T`

Parses an octal integer value from a string s.

If s is not a valid octal integer, ValueError is raised. s can have one of the following optional prefixes: 0o, 0O. Underscores within s are ignored.

Does not check for overflow. If the value represented by s is too big to fit into a return type, only the value of the rightmost octal digits of s is returned without producing an error.

### indent

[ref: #symbol-indent]

Indents each line in s by count amount of padding.

**Input:**
- `s: string`
- `count: Natural`
- `padding: string = " "`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuIndent"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Indents each line in s by count amount of padding.

**Note:** This does not preserve the new line characters used in s.

See also:

* [align func](#align,string,Natural,char)
* [alignLeft func](#alignLeft,string,Natural,char)
* [spaces func](#spaces,Natural)
* [unindent func](#unindent,string,Natural,string)
* [dedent func](#dedent,string,Natural)

### indentation

[ref: #symbol-indentation]

**Input:**
- `s: string`

**Output:** `Natural`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the amount of indentation all lines of s have in common, ignoring lines that consist only of whitespace.

### initSkipTable

[ref: #symbol-initskiptable]

Initializes table a for efficient search of substring sub.

**Input:**
- `a: var SkipTable`
- `sub: string`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nsuInitSkipTable"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Initializes table a for efficient search of substring sub.

See also:

* [initSkipTable func](#initSkipTable,string)
* [find func](#find,SkipTable,string,string,Natural,int)

### initSkipTable

[ref: #symbol-initskiptable]

Returns a new table initialized for sub.

**Input:**
- `sub: string`

**Output:** `SkipTable`
**Pragmas:** `noinit`, `gcsafe`, `extern: "nsuInitNewSkipTable"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a new table initialized for sub.

See also:

* [initSkipTable func](#initSkipTable,SkipTable,string)
* [find func](#find,SkipTable,string,string,Natural,int)

### insertSep

[ref: #symbol-insertsep]

Inserts the separator sep after digits characters (default: 3) from right to left.

**Input:**
- `s: string`
- `sep:  = '_'`
- `digits:  = 3`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuInsertSep"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Inserts the separator sep after digits characters (default: 3) from right to left.

Even though the algorithm works with any string s, it is only useful if s contains a number.

### intToStr

[ref: #symbol-inttostr]

Converts x to its decimal representation.

**Input:**
- `x: int`
- `minchars: Positive = 1`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuIntToStr"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts x to its decimal representation.

The resulting string will be minimally minchars characters long. This is achieved by adding leading zeros.

### isAlphaAscii

[ref: #symbol-isalphaascii]

Checks whether or not character c is alphabetical.

**Input:**
- `c: char`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuIsAlphaAsciiChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether or not character c is alphabetical.

This checks a-z, A-Z ASCII characters only. Use [Unicode module](unicode.html) for UTF-8 support.

### isAlphaNumeric

[ref: #symbol-isalphanumeric]

Checks whether or not c is alphanumeric.

**Input:**
- `c: char`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuIsAlphaNumericChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether or not c is alphanumeric.

This checks a-z, A-Z, 0-9 ASCII characters only.

### isDigit

[ref: #symbol-isdigit]

Checks whether or not c is a number.

**Input:**
- `c: char`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuIsDigitChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether or not c is a number.

This checks 0-9 ASCII characters only.

### isEmptyOrWhitespace

[ref: #symbol-isemptyorwhitespace]

**Input:**
- `s: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuIsEmptyOrWhitespace"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if s is empty or consists entirely of whitespace characters.

### isLowerAscii

[ref: #symbol-islowerascii]

Checks whether or not c is a lower case character.

**Input:**
- `c: char`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuIsLowerAsciiChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether or not c is a lower case character.

This checks ASCII characters only. Use [Unicode module](unicode.html) for UTF-8 support.

See also:

* [toLowerAscii func](#toLowerAscii,char)

### isSpaceAscii

[ref: #symbol-isspaceascii]

**Input:**
- `c: char`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuIsSpaceAsciiChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether or not c is a whitespace character.

### isUpperAscii

[ref: #symbol-isupperascii]

Checks whether or not c is an upper case character.

**Input:**
- `c: char`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuIsUpperAsciiChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether or not c is an upper case character.

This checks ASCII characters only. Use [Unicode module](unicode.html) for UTF-8 support.

See also:

* [toUpperAscii func](#toUpperAscii,char)

### join

[ref: #symbol-join]

**Input:**
- `a: openArray[string]`
- `sep: string = ""`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuJoinSep"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenates all strings in the container a, separating them with sep.

### join

[ref: #symbol-join]

**Input:**
- `a: openArray[T]`
- `sep: string = ""`

**Output:** `string`
**Generic parameters:** `T`

Converts all elements in the container a to strings using $, and concatenates them with sep.

### multiReplace

[ref: #symbol-multireplace]

Same as [replace](#replace,string,string,string), but specialized for doing multiple replacements in a single pass through the input string.

**Input:**
- `s: string`
- `replacements: varargs[(string, string)]`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as [replace](#replace,string,string,string), but specialized for doing multiple replacements in a single pass through the input string.

multiReplace scans the input string from left to right and replaces the matching substrings in the same order as passed in the argument list.

The implications of the order of scanning the string and matching the replacements:

* In case of multiple matches at a given position, the earliest replacement is applied.
* Overlaps are not handled. After performing a replacement, the scan continues from the character after the matched substring. If the resulting string then contains a possible match starting in a newly placed substring, the additional replacement is not performed.

If the resulting string is not longer than the original input string, only a single memory allocation is required.

### multiReplace

[ref: #symbol-multireplace]

Performs multiple character replacements in a single pass through the input.

**Input:**
- `s: openArray[char]`
- `replacements: varargs[(set[char], char)]`

**Output:** `string`
**Pragmas:** `noinit`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Performs multiple character replacements in a single pass through the input.

multiReplace scans the input s from left to right and replaces characters based on character sets, applying the first matching replacement at each position. Useful for sanitizing or transforming strings with predefined character mappings.

The order of the replacements matters:

* First matching replacement is applied
* Subsequent replacements are not considered for the same character

See also:

* [multiReplace(s: string; replacements: varargs[(string, string)])](#multiReplace,string,varargs[]),

### nimIdentNormalize

[ref: #symbol-nimidentnormalize]

Normalizes the string s as a Nim identifier.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Normalizes the string s as a Nim identifier.

That means to convert to lower case and remove any '\_' on all characters except first one.

**Warning:**
Backticks (`) are not handled: they remain *as is* and spaces are preserved. See [nimIdentBackticksNormalize](dochelpers.html#nimIdentBackticksNormalize,string) for an alternative approach.

### normalize

[ref: #symbol-normalize]

Normalizes the string s.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuNormalize"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Normalizes the string s.

That means to convert it to lower case and remove any '\_'. This should NOT be used to normalize Nim identifier names.

See also:

* [toLowerAscii func](#toLowerAscii,string)

### parseBiggestInt

[ref: #symbol-parsebiggestint]

Parses a decimal integer value contained in s.

**Input:**
- `s: string`

**Output:** `BiggestInt`
**Pragmas:** `gcsafe`, `extern: "nsuParseBiggestInt"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses a decimal integer value contained in s.

If s is not a valid integer, ValueError is raised.

### parseBiggestUInt

[ref: #symbol-parsebiggestuint]

Parses a decimal unsigned integer value contained in s.

**Input:**
- `s: string`

**Output:** `BiggestUInt`
**Pragmas:** `gcsafe`, `extern: "nsuParseBiggestUInt"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses a decimal unsigned integer value contained in s.

If s is not a valid integer, ValueError is raised.

### parseBinInt

[ref: #symbol-parsebinint]

Parses a binary integer value contained in s.

**Input:**
- `s: string`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuParseBinInt"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses a binary integer value contained in s.

If s is not a valid binary integer, ValueError is raised. s can have one of the following optional prefixes: 0b, 0B. Underscores within s are ignored.

### parseBool

[ref: #symbol-parsebool]

Parses a value into a bool.

**Input:**
- `s: string`

**Output:** `bool`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses a value into a bool.

If s is one of the following values: y, yes, true, 1, on, then returns true. If s is one of the following values: n, no, false, 0, off, then returns false. If s is something else a ValueError exception is raised.

### parseEnum

[ref: #symbol-parseenum]

Parses an enum T. This errors at compile time, if the given enum type contains multiple fields with the same string value.

**Input:**
- `s: string`

**Output:** `T`
**Generic parameters:** `T`

Parses an enum T. This errors at compile time, if the given enum type contains multiple fields with the same string value.

Raises ValueError for an invalid value in s. The comparison is done in a style insensitive way (first letter is still case-sensitive).

### parseEnum

[ref: #symbol-parseenum]

Parses an enum T. This errors at compile time, if the given enum type contains multiple fields with the same string value.

**Input:**
- `s: string`
- `default: T`

**Output:** `T`
**Generic parameters:** `T`

Parses an enum T. This errors at compile time, if the given enum type contains multiple fields with the same string value.

Uses default for an invalid value in s. The comparison is done in a style insensitive way (first letter is still case-sensitive).

### parseFloat

[ref: #symbol-parsefloat]

Parses a decimal floating point value contained in s.

**Input:**
- `s: string`

**Output:** `float`
**Pragmas:** `gcsafe`, `extern: "nsuParseFloat"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses a decimal floating point value contained in s.

If s is not a valid floating point number, ValueError is raised. NAN, INF, -INF are also supported (case insensitive comparison).

### parseHexInt

[ref: #symbol-parsehexint]

Parses a hexadecimal integer value contained in s.

**Input:**
- `s: string`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuParseHexInt"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses a hexadecimal integer value contained in s.

If s is not a valid hex integer, ValueError is raised. s can have one of the following optional prefixes: 0x, 0X, #. Underscores within s are ignored.

### parseHexStr

[ref: #symbol-parsehexstr]

Converts hex-encoded string to byte string, e.g.:

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuParseHexStr"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Converts hex-encoded string to byte string, e.g.:

Raises ValueError for an invalid hex values. The comparison is case-insensitive.

See also:

* [toHex func](#toHex,string) for the reverse operation

### parseInt

[ref: #symbol-parseint]

Parses a decimal integer value contained in s.

**Input:**
- `s: string`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuParseInt"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses a decimal integer value contained in s.

If s is not a valid integer, ValueError is raised.

### parseOctInt

[ref: #symbol-parseoctint]

Parses an octal integer value contained in s.

**Input:**
- `s: string`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuParseOctInt"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses an octal integer value contained in s.

If s is not a valid oct integer, ValueError is raised. s can have one of the following optional prefixes: 0o, 0O. Underscores within s are ignored.

### parseUInt

[ref: #symbol-parseuint]

Parses a decimal unsigned integer value contained in s.

**Input:**
- `s: string`

**Output:** `uint`
**Pragmas:** `gcsafe`, `extern: "nsuParseUInt"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses a decimal unsigned integer value contained in s.

If s is not a valid integer, ValueError is raised.

### removePrefix

[ref: #symbol-removeprefix]

Removes all characters from chars from the start of the string s (in-place).

**Input:**
- `s: var string`
- `chars: set[char] = Newlines`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nsuRemovePrefixCharSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Removes all characters from chars from the start of the string s (in-place).

See also:

* [removeSuffix func](#removeSuffix,string,set[char])

### removePrefix

[ref: #symbol-removeprefix]

Removes all occurrences of a single character (in-place) from the start of a string.

**Input:**
- `s: var string`
- `c: char`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nsuRemovePrefixChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Removes all occurrences of a single character (in-place) from the start of a string.

See also:

* [removeSuffix func](#removeSuffix,string,char)
* [startsWith func](#startsWith,string,char)


[Prev](strutils_2.md) | [Next](strutils_4.md)
