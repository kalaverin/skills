---
source_hash: 47f6f646c0362c02
source_path: lib/pure/strutils.nim
---

### rsplit

[ref: #symbol-rsplit]

Splits the string s into substrings from the right using a string separator. Works exactly the same as [split iterator](#split.i,string,char,int) except in **reverse** order.

**Input:**
- `s: string`
- `sep: char`
- `maxsplit: int = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s into substrings from the right using a string separator. Works exactly the same as [split iterator](#split.i,string,char,int) except in **reverse** order.

```
for piece in "foo:bar".rsplit(':'):
  echo piece
```

Results in:

```
"bar"
"foo"
```

Substrings are separated from the right by the char sep.

See also:

* [split iterator](#split.i,string,char,int)
* [splitLines iterator](#splitLines.i,string)
* [splitWhitespace iterator](#splitWhitespace.i,string,int)
* [rsplit func](#rsplit,string,char,int)

### rsplit

[ref: #symbol-rsplit]

Splits the string s into substrings from the right using a string separator. Works exactly the same as [split iterator](#split.i,string,char,int) except in **reverse** order.

**Input:**
- `s: string`
- `seps: set[char] = Whitespace`
- `maxsplit: int = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s into substrings from the right using a string separator. Works exactly the same as [split iterator](#split.i,string,char,int) except in **reverse** order.

```
for piece in "foo bar".rsplit(WhiteSpace):
  echo piece
```

Results in:

```
"bar"
"foo"
```

Substrings are separated from the right by the set of chars seps

**Note:**
Empty separator set results in returning an original string, following the interpretation "split by no element".

See also:

* [split iterator](#split.i,string,set[char],int)
* [splitLines iterator](#splitLines.i,string)
* [splitWhitespace iterator](#splitWhitespace.i,string,int)
* [rsplit func](#rsplit,string,set[char],int)

### rsplit

[ref: #symbol-rsplit]

Splits the string s into substrings from the right using a string separator. Works exactly the same as [split iterator](#split.i,string,string,int) except in **reverse** order.

**Input:**
- `s: string`
- `sep: string`
- `maxsplit: int = -1`
- `keepSeparators: bool = false`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s into substrings from the right using a string separator. Works exactly the same as [split iterator](#split.i,string,string,int) except in **reverse** order.

```
for piece in "foothebar".rsplit("the"):
  echo piece
```

Results in:

```
"bar"
"foo"
```

Substrings are separated from the right by the string sep

**Note:**
Empty separator string results in returning an original string, following the interpretation "split by no element".

See also:

* [split iterator](#split.i,string,string,int)
* [splitLines iterator](#splitLines.i,string)
* [splitWhitespace iterator](#splitWhitespace.i,string,int)
* [rsplit func](#rsplit,string,string,int)

### split

[ref: #symbol-split]

Splits the string s into substrings using a single separator.

**Input:**
- `s: string`
- `sep: char`
- `maxsplit: int = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s into substrings using a single separator.

Substrings are separated by the character sep. The code:

```
for word in split(";;this;is;an;;example;;;", ';'):
  writeLine(stdout, word)
```

Results in:

```
""
""
"this"
"is"
"an"
""
"example"
""
""
""
```

See also:

* [rsplit iterator](#rsplit.i,string,char,int)
* [splitLines iterator](#splitLines.i,string)
* [splitWhitespace iterator](#splitWhitespace.i,string,int)
* [split func](#split,string,char,int)

### split

[ref: #symbol-split]

Splits the string s into substrings using a group of separators.

**Input:**
- `s: string`
- `seps: set[char] = Whitespace`
- `maxsplit: int = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s into substrings using a group of separators.

Substrings are separated by a substring containing only seps.

```
for word in split("this\lis an\texample"):
  writeLine(stdout, word)
```

...generates this output:

```
"this"
"is"
"an"
"example"
```

And the following code:

```
for word in split("this:is;an$example", {';', ':', '$'}):
  writeLine(stdout, word)
```

...produces the same output as the first example. The code:

```
let date = "2012-11-20T22:08:08.398990"
let separators = {' ', '-', ':', 'T'}
for number in split(date, separators):
  writeLine(stdout, number)
```

...results in:

```
"2012"
"11"
"20"
"22"
"08"
"08.398990"
```

**Note:**
Empty separator set results in returning an original string, following the interpretation "split by no element".

See also:

* [rsplit iterator](#rsplit.i,string,set[char],int)
* [splitLines iterator](#splitLines.i,string)
* [splitWhitespace iterator](#splitWhitespace.i,string,int)
* [split func](#split,string,set[char],int)

### split

[ref: #symbol-split]

Splits the string s into substrings using a string separator.

**Input:**
- `s: string`
- `sep: string`
- `maxsplit: int = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s into substrings using a string separator.

Substrings are separated by the string sep. The code:

```
for word in split("thisDATAisDATAcorrupted", "DATA"):
  writeLine(stdout, word)
```

Results in:

```
"this"
"is"
"corrupted"
```

**Note:**
Empty separator string results in returning an original string, following the interpretation "split by no element".

See also:

* [rsplit iterator](#rsplit.i,string,string,int,bool)
* [splitLines iterator](#splitLines.i,string)
* [splitWhitespace iterator](#splitWhitespace.i,string,int)
* [split func](#split,string,string,int)

### splitLines

[ref: #symbol-splitlines]

Splits the string s into its containing lines.

**Input:**
- `s: string`
- `keepEol:  = false`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s into its containing lines.

Every [character literal](manual.html#lexical-analysis-character-literals) newline combination (CR, LF, CR-LF) is supported. The result strings contain no trailing end of line characters unless the parameter keepEol is set to true.

Example:

```
for line in splitLines("\nthis\nis\nan\n\nexample\n"):
  writeLine(stdout, line)
```

Results in:

```
""
"this"
"is"
"an"
""
"example"
""
```

See also:

* [splitWhitespace iterator](#splitWhitespace.i,string,int)
* [splitLines func](#splitLines,string)

### splitWhitespace

[ref: #symbol-splitwhitespace]

Splits the string s at whitespace stripping leading and trailing whitespace if necessary. If maxsplit is specified and is positive, no more than maxsplit splits is made.

**Input:**
- `s: string`
- `maxsplit: int = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s at whitespace stripping leading and trailing whitespace if necessary. If maxsplit is specified and is positive, no more than maxsplit splits is made.

The following code:

```
let s = "  foo \t bar  baz  "
for ms in [-1, 1, 2, 3]:
  echo "------ maxsplit = ", ms, ":"
  for item in s.splitWhitespace(maxsplit=ms):
    echo '"', item, '"'
```

...results in:

```
------ maxsplit = -1:
"foo"
"bar"
"baz"
------ maxsplit = 1:
"foo"
"bar  baz  "
------ maxsplit = 2:
"foo"
"bar"
"baz  "
------ maxsplit = 3:
"foo"
"bar"
"baz"
```

See also:

* [splitLines iterator](#splitLines.i,string)
* [splitWhitespace func](#splitWhitespace,string,int)

### tokenize

[ref: #symbol-tokenize]

Tokenizes the string s into substrings.

**Input:**
- `s: string`
- `seps: set[char] = Whitespace`

**Output:** `tuple[token: string, isSep: bool]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Tokenizes the string s into substrings.

Substrings are separated by a substring containing only seps. Example:

```
for word in tokenize("  this is an  example  "):
  writeLine(stdout, word)
```

Results in:

```
("  ", true)
("this", false)
(" ", true)
("is", false)
(" ", true)
("an", false)
("  ", true)
("example", false)
("  ", true)
```

## Proc

### `%`

[ref: #symbol-]

Interpolates a format string with the values from a.

**Input:**
- `formatstr: string`
- `a: openArray[string]`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuFormatOpenArray"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Interpolates a format string with the values from a.

The substitution operator performs string substitutions in formatstr and returns a modified formatstr. This is often called string interpolation.

This is best explained by an example:

```
"$1 eats $2." % ["The cat", "fish"]
```

Results in:

```
"The cat eats fish."
```

The substitution variables (the thing after the $) are enumerated from 1 to a.len. To produce a verbatim $, use $$. The notation $# can be used to refer to the next substitution variable:

```
"$# eats $#." % ["The cat", "fish"]
```

Substitution variables can also be words (that is [A-Za-z\_]+[A-Za-z0-9\_]\*) in which case the arguments in a with even indices are keys and with odd indices are the corresponding values. An example:

```
"$animal eats $food." % ["animal", "The cat", "food", "fish"]
```

Results in:

```
"The cat eats fish."
```

The variables are compared with cmpIgnoreStyle. ValueError is raised if an ill-formed format string has been passed to the % operator.

See also:

* [strformat module](strformat.html) for string interpolation and formatting

### `%`

[ref: #symbol-]

**Input:**
- `formatstr: string`
- `a: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuFormatSingleElem"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

This is the same as formatstr % [a] (see [% func](#%25,string,openArray[string])).

### abbrev

[ref: #symbol-abbrev]

Returns the index of the first item in possibilities which starts with s, if not ambiguous.

**Input:**
- `s: string`
- `possibilities: openArray[string]`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the index of the first item in possibilities which starts with s, if not ambiguous.

Returns -1 if no item has been found and -2 if multiple items match.

### addf

[ref: #symbol-addf]

**Input:**
- `s: var string`
- `formatstr: string`
- `a: varargs[string, `$`]`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nsuAddf"`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

The same as add(s, formatstr % a), but more efficient.

### addSep

[ref: #symbol-addsep]

Adds a separator to dest only if its length is bigger than startLen.

**Input:**
- `dest: var string`
- `sep:  = ", "`
- `startLen: Natural = 0`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds a separator to dest only if its length is bigger than startLen.

A shorthand for:

```
if dest.len > startLen: add(dest, sep)
```

This is often useful for generating some code where the items need to be *separated* by sep. sep is only added if dest is longer than startLen. The following example creates a string describing an array of integers.

### align

[ref: #symbol-align]

Aligns a string s with padding, so that it is of length count.

**Input:**
- `s: string`
- `count: Natural`
- `padding:  = ' '`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuAlignString"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Aligns a string s with padding, so that it is of length count.

padding characters (by default spaces) are added before s resulting in right alignment. If s.len >= count, no spaces are added and s is returned unchanged. If you need to left align a string use the [alignLeft func](#alignLeft,string,Natural,char).

See also:

* [alignLeft func](#alignLeft,string,Natural,char)
* [spaces func](#spaces,Natural)
* [indent func](#indent,string,Natural,string)
* [center func](#center,string,int,char)

### alignLeft

[ref: #symbol-alignleft]

Left-Aligns a string s with padding, so that it is of length count.

**Input:**
- `s: string`
- `count: Natural`
- `padding:  = ' '`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Left-Aligns a string s with padding, so that it is of length count.

padding characters (by default spaces) are added after s resulting in left alignment. If s.len >= count, no spaces are added and s is returned unchanged. If you need to right align a string use the [align func](#align,string,Natural,char).

See also:

* [align func](#align,string,Natural,char)
* [spaces func](#spaces,Natural)
* [indent func](#indent,string,Natural,string)
* [center func](#center,string,int,char)

### allCharsInSet

[ref: #symbol-allcharsinset]

**Input:**
- `s: string`
- `theSet: set[char]`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if every character of s is in the set theSet.

### capitalizeAscii

[ref: #symbol-capitalizeascii]

Converts the first character of string s into upper case.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuCapitalizeAscii"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the first character of string s into upper case.

This works only for the letters A-Z. Use [Unicode module](unicode.html) for UTF-8 support.

See also:

* [toUpperAscii func](#toUpperAscii,char)

### center

[ref: #symbol-center]

Return the contents of s centered in a string width long using fillChar (default: space) as padding.

**Input:**
- `s: string`
- `width: int`
- `fillChar: char = ' '`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuCenterString"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Return the contents of s centered in a string width long using fillChar (default: space) as padding.

The original string is returned if width is less than or equal to s.len.

See also:

* [align func](#align,string,Natural,char)
* [alignLeft func](#alignLeft,string,Natural,char)
* [spaces func](#spaces,Natural)
* [indent func](#indent,string,Natural,string)

### cmpIgnoreCase

[ref: #symbol-cmpignorecase]

Compares two strings in a case insensitive manner. Returns:

**Input:**
- `a: string`
- `b: string`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuCmpIgnoreCase"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two strings in a case insensitive manner. Returns:

0 if a == b  
< 0 if a < b  
> 0 if a > b

### cmpIgnoreStyle

[ref: #symbol-cmpignorestyle]

Semantically the same as cmp(normalize(a), normalize(b)). It is just optimized to not allocate temporary strings. This should NOT be used to compare Nim identifier names. Use [macros.eqIdent](macros.html#eqIdent,string,string) for that.

**Input:**
- `a: string`
- `b: string`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuCmpIgnoreStyle"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Semantically the same as cmp(normalize(a), normalize(b)). It is just optimized to not allocate temporary strings. This should NOT be used to compare Nim identifier names. Use [macros.eqIdent](macros.html#eqIdent,string,string) for that.

Returns:

0 if a == b  
< 0 if a < b  
> 0 if a > b

### contains

[ref: #symbol-contains]

Same as find(s, sub) >= 0.

**Input:**
- `s: string`
- `sub: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as find(s, sub) >= 0.

See also:

* [find func](#find,string,string,Natural,int)

### contains

[ref: #symbol-contains]

Same as find(s, chars) >= 0.

**Input:**
- `s: string`
- `chars: set[char]`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as find(s, chars) >= 0.

See also:

* [find func](#find,string,set[char],Natural,int)

### continuesWith

[ref: #symbol-continueswith]

Returns true if s continues with substr at position start.

**Input:**
- `s: string`
- `substr: string`
- `start: Natural`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuContinuesWith"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s continues with substr at position start.

If substr == "" true is returned.

See also:

* [startsWith func](#startsWith,string,string)
* [endsWith func](#endsWith,string,string)

### count

[ref: #symbol-count]

Counts the occurrences of the character sub in the string s.

**Input:**
- `s: string`
- `sub: char`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuCountChar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Counts the occurrences of the character sub in the string s.

See also:

* [countLines func](#countLines,string)

### count

[ref: #symbol-count]

Counts the occurrences of the group of character subs in the string s.

**Input:**
- `s: string`
- `subs: set[char]`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuCountCharSet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Counts the occurrences of the group of character subs in the string s.

See also:

* [countLines func](#countLines,string)

### count

[ref: #symbol-count]

Counts the occurrences of a substring sub in the string s. Overlapping occurrences of sub only count when overlapping is set to true (default: false).

**Input:**
- `s: string`
- `sub: string`
- `overlapping: bool = false`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuCountString"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Counts the occurrences of a substring sub in the string s. Overlapping occurrences of sub only count when overlapping is set to true (default: false).

See also:

* [countLines func](#countLines,string)

### countLines

[ref: #symbol-countlines]

Returns the number of lines in the string s.

**Input:**
- `s: string`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nsuCountLines"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of lines in the string s.

This is the same as len(splitLines(s)), but much more efficient because it doesn't modify the string creating temporary objects. Every [character literal](manual.html#lexical-analysis-character-literals) newline combination (CR, LF, CR-LF) is supported.

In this context, a line is any string separated by a newline combination. A line can be an empty string.

See also:

* [splitLines func](#splitLines,string)

### dedent

[ref: #symbol-dedent]

Unindents each line in s by count amount of padding. The only difference between this and the [unindent func](#unindent,string,Natural,string) is that this by default only cuts off the amount of indentation that all lines of s share as opposed to all indentation. It only supports spaces as padding.

**Input:**
- `s: string`
- `count: Natural = indentation(s)`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nsuDedent"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unindents each line in s by count amount of padding. The only difference between this and the [unindent func](#unindent,string,Natural,string) is that this by default only cuts off the amount of indentation that all lines of s share as opposed to all indentation. It only supports spaces as padding.

**Note:** This does not preserve the new line characters used in s.

See also:

* [unindent func](#unindent,string,Natural,string)
* [align func](#align,string,Natural,char)
* [alignLeft func](#alignLeft,string,Natural,char)
* [spaces func](#spaces,Natural)
* [indent func](#indent,string,Natural,string)

### delete

[ref: #symbol-delete]

Deletes the items s[slice], raising IndexDefect if the slice contains elements out of range.

**Input:**
- `s: var string`
- `slice: Slice[int]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Deletes the items s[slice], raising IndexDefect if the slice contains elements out of range.

This operation moves all elements after s[slice] in linear time, and is the string analog to sequtils.delete.

### delete

[ref: #symbol-delete]

**Input:**
- `s: var string`
- `first: int`
- `last: int`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nsuDelete"`, `deprecated: "use `delete(s, first..last)`"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Deletes in s the characters at positions first .. last (both ends included).

### endsWith

[ref: #symbol-endswith]

Returns true if s ends with suffix.

**Input:**
- `s: string`
- `suffix: char`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s ends with suffix.

See also:

* [startsWith func](#startsWith,string,char)
* [continuesWith func](#continuesWith,string,string,Natural)
* [removeSuffix func](#removeSuffix,string,char)

### endsWith

[ref: #symbol-endswith]

Returns true if s ends with suffix.

**Input:**
- `s: string`
- `suffix: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nsuEndsWith"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if s ends with suffix.

If suffix == "" true is returned.

See also:

* [startsWith func](#startsWith,string,string)
* [continuesWith func](#continuesWith,string,string,Natural)
* [removeSuffix func](#removeSuffix,string,string)


[Prev](strutils_1.md) | [Next](strutils_3.md)
