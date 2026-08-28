---
source_hash: 47f6f646c0362c02
source_path: lib/pure/strutils.nim
---

# strutils

[ref: #module-strutils]

The system module defines several common functions for working with strings, such as:

* $ for converting other data-types to strings
* & for string concatenation
* add for adding a new character or a string to the existing one
* in (alias for contains) and notin for checking if a character is in a string

This module builds upon that, providing additional functionality in form of procedures, iterators and templates for strings.

The chaining of functions is possible thanks to the [method call syntax](manual.html#procedures-method-call-syntax):This module is available for the [JavaScript target](backends.html#backends-the-javascript-target).

---

**See also:**

* [strformat module](strformat.html) for string interpolation and formatting
* [unicode module](unicode.html) for Unicode UTF-8 handling
* [sequtils module](sequtils.html) for operations on container types (including strings)
* [parsecsv module](parsecsv.html) for a high-performance CSV parser
* [parseutils module](parseutils.html) for lower-level parsing of tokens, numbers, identifiers, etc.
* [parseopt module](parseopt.html) for command-line parsing
* [pegs module](pegs.html) for PEG (Parsing Expression Grammar) support
* [strtabs module](strtabs.html) for efficient hash tables (dictionaries, in some programming languages) mapping from strings to strings
* [ropes module](ropes.html) for rope data type, which can represent very long strings efficiently
* [re module](re.html) for regular expression (regex) support
* [strscans](strscans.html) for scanf and scanp macros, which offer easier substring extraction than regular expressions

## Examples

```nim
import std/strutils
let
  numbers = @[867, 5309]
  multiLineString = "first line\nsecond line\nthird line"

let jenny = numbers.join("-")
assert jenny == "867-5309"

assert splitLines(multiLineString) ==
       @["first line", "second line", "third line"]
assert split(multiLineString) == @["first", "line", "second",
                                   "line", "third", "line"]
assert indent(multiLineString, 4) ==
       "    first line\n    second line\n    third line"
assert 'z'.repeat(5) == "zzzzz"
```

```nim
import std/strutils
from std/sequtils import map

let jenny = "867-5309"
assert jenny.split('-').map(parseInt) == @[867, 5309]

assert "Beetlejuice".indent(1).repeat(3).strip ==
       "Beetlejuice Beetlejuice Beetlejuice"
```

```nim
let invalid = AllChars - Digits
doAssert "01234".find(invalid) == -1
doAssert "01A34".find(invalid) == 2
```

```nim
"$1 eats $2." % ["The cat", "fish"]
```

```nim
"The cat eats fish."
```

```nim
"$# eats $#." % ["The cat", "fish"]
```

```nim
"$animal eats $food." % ["animal", "The cat", "food", "fish"]
```

```nim
"The cat eats fish."
```

```nim
doAssert abbrev("fac", ["college", "faculty", "industry"]) == 1
doAssert abbrev("foo", ["college", "faculty", "industry"]) == -1 # Not found
doAssert abbrev("fac", ["college", "faculty", "faculties"]) == -2 # Ambiguous
doAssert abbrev("college", ["college", "colleges", "industry"]) == 0
```

```nim
if dest.len > startLen: add(dest, sep)
```

```nim
var arr = "["
for x in items([2, 3, 5, 7, 11]):
  addSep(arr, startLen = len("["))
  add(arr, $x)
add(arr, "]")
doAssert arr == "[2, 3, 5, 7, 11]"
```

```nim
assert align("abc", 4) == " abc"
assert align("a", 0) == "a"
assert align("1232", 6) == "  1232"
assert align("1232", 6, '#') == "##1232"
```

```nim
assert alignLeft("abc", 4) == "abc "
assert alignLeft("a", 0) == "a"
assert alignLeft("1232", 6) == "1232  "
assert alignLeft("1232", 6, '#') == "1232##"
```

```nim
doAssert allCharsInSet("aeea", {'a', 'e'}) == true
doAssert allCharsInSet("", {'a', 'e'}) == true
```

```nim
doAssert capitalizeAscii("foo") == "Foo"
doAssert capitalizeAscii("-bar") == "-bar"
```

```nim
let a = "foo"
doAssert a.center(2) == "foo"
doAssert a.center(5) == " foo "
doAssert a.center(6) == " foo  "
```

```nim
doAssert cmpIgnoreCase("FooBar", "foobar") == 0
doAssert cmpIgnoreCase("bar", "Foo") < 0
doAssert cmpIgnoreCase("Foo5", "foo4") > 0
```

```nim
doAssert cmpIgnoreStyle("foo_bar", "FooBar") == 0
doAssert cmpIgnoreStyle("foo_bar_5", "FooBar4") > 0
```

```nim
let a = "abracadabra"
doAssert a.continuesWith("ca", 4) == true
doAssert a.continuesWith("ca", 5) == false
doAssert a.continuesWith("dab", 6) == true
```

```nim
doAssert countLines("First line\l and second line.") == 2
```

```nim
let x = """
      Hello
        There
    """.dedent()

doAssert x == "Hello\n  There\n"
```

```nim
var a = "abracadabra"

a.delete(4, 5)
doAssert a == "abradabra"

a.delete(1, 6)
doAssert a == "ara"

a.delete(2, 999)
doAssert a == "ar"
```

```nim
var a = "abcde"
doAssertRaises(IndexDefect): a.delete(4..5)
assert a == "abcde"
a.delete(4..4)
assert a == "abcd"
a.delete(1..2)
assert a == "ad"
a.delete(1..<1) # empty slice
assert a == "ad"
```

```nim
let a = "abracadabra"
doAssert a.endsWith("abra") == true
doAssert a.endsWith("dab") == false
```

```nim
let a = "abracadabra"
doAssert a.endsWith('a') == true
doAssert a.endsWith('b') == false
```

```nim
let x = 123.456
doAssert x.formatBiggestFloat() == "123.4560000000000"
doAssert x.formatBiggestFloat(ffDecimal, 4) == "123.4560"
doAssert x.formatBiggestFloat(ffScientific, 2) == "1.23e+02"
```

```nim
 formatEng(0, 2, trim=false) == "0.00"
 formatEng(0, 2) == "0"
 formatEng(0.053, 0) == "53e-3"
 formatEng(52731234, 2) == "52.73e6"
 formatEng(-52731234, 2) == "-52.73e6"
```

```nim
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

```nim
let x = 123.456
doAssert x.formatFloat() == "123.4560000000000"
doAssert x.formatFloat(ffDecimal, 4) == "123.4560"
doAssert x.formatFloat(ffScientific, 2) == "1.23e+02"
```

```nim
doAssert formatSize((1'i64 shl 31) + (300'i64 shl 20)) == "2.293GiB"
doAssert formatSize((2.234*1024*1024).int) == "2.233MiB"
doAssert formatSize(4096, includeSpace = true) == "4 KiB"
doAssert formatSize(4096, prefix = bpColloquial, includeSpace = true) == "4 kB"
doAssert formatSize(4096) == "4KiB"
doAssert formatSize(5_378_934, prefix = bpColloquial, decimalSep = ',') == "5,129MB"
```

```nim
let s = "0b_0100_1000_1000_1000_1110_1110_1001_1001"
doAssert fromBin[int](s) == 1216933529
doAssert fromBin[int8](s) == 0b1001_1001'i8
doAssert fromBin[int8](s) == -103'i8
doAssert fromBin[uint8](s) == 153
doAssert s.fromBin[:int16] == 0b1110_1110_1001_1001'i16
doAssert s.fromBin[:uint64] == 1216933529'u64
```

```nim
let s = "0x_1235_8df6"
doAssert fromHex[int](s) == 305499638
doAssert fromHex[int8](s) == 0xf6'i8
doAssert fromHex[int8](s) == -10'i8
doAssert fromHex[uint8](s) == 246'u8
doAssert s.fromHex[:int16] == -29194'i16
doAssert s.fromHex[:uint64] == 305499638'u64
```

```nim
let s = "0o_123_456_777"
doAssert fromOct[int](s) == 21913087
doAssert fromOct[int8](s) == 0o377'i8
doAssert fromOct[int8](s) == -1'i8
doAssert fromOct[uint8](s) == 255'u8
doAssert s.fromOct[:int16] == 24063'i16
doAssert s.fromOct[:uint64] == 21913087'u64
```

```nim
doAssert indent("First line\c\l and second line.", 2) ==
         "  First line\l   and second line."
```

```nim
doAssert insertSep("1000000") == "1_000_000"
```

```nim
doAssert intToStr(1984) == "1984"
doAssert intToStr(1984, 6) == "001984"
```

```nim
doAssert isAlphaAscii('e') == true
doAssert isAlphaAscii('E') == true
doAssert isAlphaAscii('8') == false
```

```nim
doAssert isAlphaNumeric('n') == true
doAssert isAlphaNumeric('8') == true
doAssert isAlphaNumeric(' ') == false
```

```nim
doAssert isDigit('n') == false
doAssert isDigit('8') == true
```

```nim
doAssert isLowerAscii('e') == true
doAssert isLowerAscii('E') == false
doAssert isLowerAscii('7') == false
```

```nim
doAssert isSpaceAscii('n') == false
doAssert isSpaceAscii(' ') == true
doAssert isSpaceAscii('\t') == true
```

```nim
doAssert isUpperAscii('e') == false
doAssert isUpperAscii('E') == true
doAssert isUpperAscii('7') == false
```

```nim
doAssert join(["A", "B", "Conclusion"], " -> ") == "A -> B -> Conclusion"
```

```nim
doAssert join([1, 2, 3], " -> ") == "1 -> 2 -> 3"
```

```nim
const WinSanitationRules = [
  ({'\0'..'\31'}, ' '),
  ({'"'}, '\''),
  ({'/', '\\', ':', '|'}, '-'),
  ({'*', '?', '<', '>'}, '_'),
]
# Sanitize a filename with Windows-incompatible characters
const file = "a/file:with?invalid*chars.txt"
doAssert file.multiReplace(WinSanitationRules) == "a-file-with_invalid_chars.txt"
```

```nim
# Swapping occurrences of 'a' and 'b':
doAssert multireplace("abba", [("a", "b"), ("b", "a")]) == "baab"

# The second replacement ("ab") is matched and performed first, the scan then
# continues from 'c', so the "bc" replacement is never matched and thus skipped.
doAssert multireplace("abc", [("bc", "x"), ("ab", "_b")]) == "_bc"
```

```nim
doAssert nimIdentNormalize("Foo_bar") == "Foobar"
```

```nim
doAssert normalize("Foo_bar") == "foobar"
doAssert normalize("Foo Bar") == "foo bar"
```

```nim
let
  a = "0b11_0101"
  b = "111"
doAssert a.parseBinInt() == 53
doAssert b.parseBinInt() == 7
```

```nim
let a = "n"
doAssert parseBool(a) == false
```

```nim
type
  MyEnum = enum
    first = "1st",
    second,
    third = "3rd"

doAssert parseEnum[MyEnum]("1_st") == first
doAssert parseEnum[MyEnum]("second") == second
doAssertRaises(ValueError):
  echo parseEnum[MyEnum]("third")
```

```nim
type
  MyEnum = enum
    first = "1st",
    second,
    third = "3rd"

doAssert parseEnum[MyEnum]("1_st") == first
doAssert parseEnum[MyEnum]("second") == second
doAssert parseEnum[MyEnum]("last", third) == third
```

```nim
doAssert parseFloat("3.14") == 3.14
doAssert parseFloat("inf") == 1.0/0
```

```nim
let
  a = "41"
  b = "3161"
  c = "00ff"
doAssert parseHexStr(a) == "A"
doAssert parseHexStr(b) == "1a"
doAssert parseHexStr(c) == "\0\255"
```

```nim
doAssert parseInt("-0042") == -42
```

```nim
var ident = "pControl"
ident.removePrefix('p')
doAssert ident == "Control"
```

```nim
var userInput = "\r\n*~Hello World!"
userInput.removePrefix
doAssert userInput == "*~Hello World!"
userInput.removePrefix({'~', '*'})
doAssert userInput == "Hello World!"

var otherInput = "?!?Hello!?!"
otherInput.removePrefix({'!', '?'})
doAssert otherInput == "Hello!?!"
```

```nim
var answers = "yesyes"
answers.removePrefix("yes")
doAssert answers == "yes"
```

```nim
var table = "users"
table.removeSuffix('s')
doAssert table == "user"

var dots = "Trailing dots......."
dots.removeSuffix('.')
doAssert dots == "Trailing dots"
```

```nim
var userInput = "Hello World!*~\r\n"
userInput.removeSuffix
doAssert userInput == "Hello World!*~"
userInput.removeSuffix({'~', '*'})
doAssert userInput == "Hello World!"

var otherInput = "Hello!?!"
otherInput.removeSuffix({'!', '?'})
doAssert otherInput == "Hello"
```

```nim
var answers = "yeses"
answers.removeSuffix("es")
doAssert answers == "yes"
```

```nim
let a = 'z'
doAssert a.repeat(5) == "zzzzz"
```

```nim
doAssert "+ foo +".repeat(3) == "+ foo ++ foo ++ foo +"
```

```nim
var tailSplit = rsplit("Root#Object#Method#Index", '#', maxsplit=1)
```

```nim
@["Root#Object#Method", "Index"]
```

```nim
var tailSplit = rsplit("Root#Object#Method#Index", "#", maxsplit=1)
```

```nim
@["Root#Object#Method", "Index"]
```

```nim
doAssert "a  largely    spaced sentence".rsplit(" ", maxsplit = 1) == @[
    "a  largely    spaced", "sentence"]
doAssert "a,b,c".rsplit(",") == @["a", "b", "c"]
doAssert "a man a plan a canal panama".rsplit("a ") == @["", "man ",
    "plan ", "canal panama"]
doAssert "".rsplit("Elon Musk") == @[""]
doAssert "a  largely    spaced sentence".rsplit(" ") == @["a", "",
    "largely", "", "", "", "spaced", "sentence"]
doAssert "empty sep returns unsplit s".rsplit("") == @["empty sep returns unsplit s"]
```

```nim
var tailSplit = rsplit("Root#Object#Method#Index", {'#'}, maxsplit=1)
```

```nim
@["Root#Object#Method", "Index"]
```

```nim
let
  width = 15
  text1 = "Hello user!"
  text2 = "This is a very long string"
doAssert text1 & spaces(max(0, width - text1.len)) & "|" ==
         "Hello user!    |"
doAssert text2 & spaces(max(0, width - text2.len)) & "|" ==
         "This is a very long string|"
```

```nim
doAssert "a,b,c".split(',') == @["a", "b", "c"]
doAssert "".split(' ') == @[""]
```

```nim
doAssert "a,b,c".split(",") == @["a", "b", "c"]
doAssert "a man a plan a canal panama".split("a ") == @["", "man ", "plan ", "canal panama"]
doAssert "".split("Elon Musk") == @[""]
doAssert "a  largely    spaced sentence".split(" ") == @["a", "", "largely",
    "", "", "", "spaced", "sentence"]
doAssert "a  largely    spaced sentence".split(" ", maxsplit = 1) == @["a", " largely    spaced sentence"]
doAssert "empty sep returns unsplit s".split("") == @["empty sep returns unsplit s"]
```

```nim
doAssert "a,b;c".split({',', ';'}) == @["a", "b", "c"]
doAssert "".split({' '}) == @[""]
doAssert "empty seps return unsplit s".split({}) == @["empty seps return unsplit s"]
```

```nim
let a = "abracadabra"
doAssert a.startsWith("abra") == true
doAssert a.startsWith("bra") == false
```

```nim
let a = "abracadabra"
doAssert a.startsWith('a') == true
doAssert a.startsWith('b') == false
```

```nim
let a = "  vhellov   "
let b = strip(a)
doAssert b == "vhellov"

doAssert a.strip(leading = false) == "  vhellov"
doAssert a.strip(trailing = false) == "vhellov   "

doAssert b.strip(chars = {'v'}) == "hello"
doAssert b.strip(leading = false, chars = {'v'}) == "vhello"

let c = "blaXbla"
doAssert c.strip(chars = {'b', 'a'}) == "laXbl"
doAssert c.strip(chars = {'b', 'a', 'l'}) == "X"
```

```nim
var s = "foo\n\n"
s.stripLineEnd
doAssert s == "foo\n"
s = "foo\r\n"
s.stripLineEnd
doAssert s == "foo"
```

```nim
let
  a = 29
  b = 257
doAssert a.toBin(8) == "00011101"
doAssert b.toBin(8) == "00000001"
doAssert b.toBin(9) == "100000001"
```

```nim
let
  a = "1"
  b = "A"
  c = "\0\255"
doAssert a.toHex() == "31"
doAssert b.toHex() == "41"
doAssert c.toHex() == "00FF"
```

```nim
doAssert toHex(1984'i64) == "00000000000007C0"
doAssert toHex(1984'i16) == "07C0"
```

```nim
let
  a = 62'u64
  b = 4097'u64
doAssert a.toHex(3) == "03E"
doAssert b.toHex(3) == "001"
doAssert b.toHex(4) == "1001"
doAssert toHex(62, 3) == "03E"
doAssert toHex(-8, 6) == "FFFFF8"
```

```nim
doAssert toLowerAscii('A') == 'a'
doAssert toLowerAscii('e') == 'e'
```

```nim
doAssert toLowerAscii("FooBar!") == "foobar!"
```

```nim
let
  a = 62
  b = 513
doAssert a.toOct(3) == "076"
doAssert b.toOct(3) == "001"
doAssert b.toOct(5) == "01001"
```

```nim
doAssert toOctal('1') == "061"
doAssert toOctal('A') == "101"
doAssert toOctal('a') == "141"
doAssert toOctal('!') == "041"
```

```nim
doAssert toUpperAscii('a') == 'A'
doAssert toUpperAscii('E') == 'E'
```

```nim
doAssert toUpperAscii("FooBar!") == "FOOBAR!"
```

```nim
var x = "123.456000000"
x.trimZeros()
doAssert x == "123.456"
```

```nim
let x = """
      Hello
        There
    """.unindent()

doAssert x == "Hello\nThere\n"
```

```nim
doAssert "abc_def08".validIdentifier
```

```nim
for piece in "foo:bar".rsplit(':'):
  echo piece
```

```nim
"bar"
"foo"
```

```nim
for piece in "foothebar".rsplit("the"):
  echo piece
```

```nim
"bar"
"foo"
```

```nim
for piece in "foo bar".rsplit(WhiteSpace):
  echo piece
```

```nim
"bar"
"foo"
```

```nim
for word in split(";;this;is;an;;example;;;", ';'):
  writeLine(stdout, word)
```

```nim
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

```nim
for word in split("thisDATAisDATAcorrupted", "DATA"):
  writeLine(stdout, word)
```

```nim
"this"
"is"
"corrupted"
```

```nim
for word in split("this\lis an\texample"):
  writeLine(stdout, word)
```

```nim
"this"
"is"
"an"
"example"
```

```nim
for word in split("this:is;an$example", {';', ':', '$'}):
  writeLine(stdout, word)
```

```nim
let date = "2012-11-20T22:08:08.398990"
let separators = {' ', '-', ':', 'T'}
for number in split(date, separators):
  writeLine(stdout, number)
```

```nim
"2012"
"11"
"20"
"22"
"08"
"08.398990"
```

```nim
for line in splitLines("\nthis\nis\nan\n\nexample\n"):
  writeLine(stdout, line)
```

```nim
""
"this"
"is"
"an"
""
"example"
""
```

```nim
let s = "  foo \t bar  baz  "
for ms in [-1, 1, 2, 3]:
  echo "------ maxsplit = ", ms, ":"
  for item in s.splitWhitespace(maxsplit=ms):
    echo '"', item, '"'
```

```nim
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

```nim
for word in tokenize("  this is an  example  "):
  writeLine(stdout, word)
```

```nim
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

## Const

### AllChars

[ref: #symbol-allchars]

A set with all the possible characters.

```nim
AllChars = {'\x00'..'\xFF'}
```

A set with all the possible characters.

Not very useful by its own, you can use it to create *inverted* sets to make the [find func](#find,string,set[char],Natural,int) find **invalid** characters in strings. Example:

```
let invalid = AllChars - Digits
doAssert "01234".find(invalid) == -1
doAssert "01A34".find(invalid) == 2
```

### Digits

[ref: #symbol-digits]

```nim
Digits = {'0'..'9'}
```

The set of digits.

### HexDigits

[ref: #symbol-hexdigits]

```nim
HexDigits = {'0'..'9', 'A'..'F', 'a'..'f'}
```

The set of hexadecimal digits.

### IdentChars

[ref: #symbol-identchars]

```nim
IdentChars = {'a'..'z', 'A'..'Z', '0'..'9', '_'}
```

The set of characters an identifier can consist of.

### IdentStartChars

[ref: #symbol-identstartchars]

```nim
IdentStartChars = {'a'..'z', 'A'..'Z', '_'}
```

The set of characters an identifier can start with.

### Letters

[ref: #symbol-letters]

```nim
Letters = {'A'..'Z', 'a'..'z'}
```

The set of letters.

### LowercaseLetters

[ref: #symbol-lowercaseletters]

```nim
LowercaseLetters = {'a'..'z'}
```

The set of lowercase ASCII letters.

### Newlines

[ref: #symbol-newlines]

```nim
Newlines = {'\r', '\n'}
```

The set of characters a newline terminator can start with (carriage return, line feed).

### PrintableChars

[ref: #symbol-printablechars]

```nim
PrintableChars = {'\t'..'\r', ' '..'~'}
```

The set of all printable ASCII characters (letters, digits, whitespace, and punctuation characters).

### PunctuationChars

[ref: #symbol-punctuationchars]

```nim
PunctuationChars = {'!'..'/', ':'..'@', '['..'`', '{'..'~'}
```

The set of all ASCII punctuation characters.

### UppercaseLetters

[ref: #symbol-uppercaseletters]

```nim
UppercaseLetters = {'A'..'Z'}
```

The set of uppercase ASCII letters.

### Whitespace

[ref: #symbol-whitespace]

```nim
Whitespace = {' ', '\t', '\v', '\r', '\n', '\f'}
```

All the characters that count as whitespace (space, tab, vertical tab, carriage return, new line, form feed).

## Iterator


[Next](strutils_2.md)
