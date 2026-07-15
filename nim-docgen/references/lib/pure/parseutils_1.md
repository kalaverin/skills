---
source_hash: 53ce8b9f2450523b
source_path: lib/pure/parseutils.nim
---

# parseutils

[ref: #module-parseutils]

This module contains helpers for parsing tokens, numbers, integers, floats, identifiers, etc.

To unpack raw bytes look at the [streams](streams.html) module.

```
let logs = @["2019-01-10: OK_", "2019-01-11: FAIL_", "2019-01: aaaa"]
var outp: seq[string]

for log in logs:
  var res: string
  if parseUntil(log, res, ':') == 10: # YYYY-MM-DD == 10
    outp.add(res & " - " & captureBetween(log, ' ', '_'))
doAssert outp == @["2019-01-10 - OK", "2019-01-11 - FAIL"]
```

```
from std/strutils import Digits, parseInt

let
  input1 = "2019 school start"
  input2 = "3 years back"
  startYear = input1[0 .. skipWhile(input1, Digits)-1] # 2019
  yearsBack = input2[0 .. skipWhile(input2, Digits)-1] # 3
  examYear = parseInt(startYear) + parseInt(yearsBack)
doAssert "Examination is in " & $examYear == "Examination is in 2022"
```

**See also:**

* [strutils module](strutils.html) for combined and identical parsing proc's
* [json module](json.html) for a JSON parser
* [parsecfg module](parsecfg.html) for a configuration file parser
* [parsecsv module](parsecsv.html) for a simple CSV (comma separated value) parser
* [parseopt module](parseopt.html) for a command line parser
* [parsexml module](parsexml.html) for a XML / HTML parser
* [other parsers](lib.html#pure-libraries-parsers) for other parsers

## Examples

```nim
let logs = @["2019-01-10: OK_", "2019-01-11: FAIL_", "2019-01: aaaa"]
var outp: seq[string]

for log in logs:
  var res: string
  if parseUntil(log, res, ':') == 10: # YYYY-MM-DD == 10
    outp.add(res & " - " & captureBetween(log, ' ', '_'))
doAssert outp == @["2019-01-10 - OK", "2019-01-11 - FAIL"]
```

```nim
from std/strutils import Digits, parseInt

let
  input1 = "2019 school start"
  input2 = "3 years back"
  startYear = input1[0 .. skipWhile(input1, Digits)-1] # 2019
  yearsBack = input2[0 .. skipWhile(input2, Digits)-1] # 3
  examYear = parseInt(startYear) + parseInt(yearsBack)
doAssert "Examination is in " & $examYear == "Examination is in 2022"
```

```nim
doAssert captureBetween("Hello World", 'e') == "llo World"
doAssert captureBetween("Hello World", 'e', 'r') == "llo Wo"
doAssert captureBetween("Hello World".toOpenArray(6, "Hello World".high), 'l') == "d"
```

```nim
doAssert captureBetween("Hello World", 'e') == "llo World"
doAssert captureBetween("Hello World", 'e', 'r') == "llo Wo"
doAssert captureBetween("Hello World", 'l', start = 6) == "d"
```

```nim
var res: BiggestInt
doAssert parseBiggestInt("9223372036854775807", res) == 19
doAssert res == 9223372036854775807
doAssert parseBiggestInt("-2024_05_09", res) == 11
doAssert res == -20240509
```

```nim
var res: BiggestInt
doAssert parseBiggestInt("9223372036854775807", res, 0) == 19
doAssert res == 9223372036854775807
doAssert parseBiggestInt("-2024_05_09", res) == 11
doAssert res == -20240509
doAssert parseBiggestInt("-2024_05_02", res, 7) == 4
doAssert res == 502
```

```nim
var res: BiggestUInt
doAssert parseBiggestUInt("12", res, 0) == 2
doAssert res == 12
doAssert parseBiggestUInt("1111111111111111111", res, 0) == 19
doAssert res == 1111111111111111111'u64
```

```nim
var res: BiggestUInt
doAssert parseBiggestUInt("12", res, 0) == 2
doAssert res == 12
doAssert parseBiggestUInt("1111111111111111111", res, 0) == 19
doAssert res == 1111111111111111111'u64
```

```nim
var num: int
doAssert parseBin("0100_1110_0110_1001_1110_1101", num) == 29
doAssert num == 5138925
doAssert parseBin("3", num) == 0
var num8: int8
doAssert parseBin("0b_0100_1110_0110_1001_1110_1101", num8) == 32
doAssert num8 == 0b1110_1101'i8
doAssert parseBin("0b_0100_1110_0110_1001_1110_1101", num8, 3, 9) == 9
doAssert num8 == 0b0100_1110'i8
var num8u: uint8
doAssert parseBin("0b_0100_1110_0110_1001_1110_1101", num8u) == 32
doAssert num8u == 237
var num64: int64
doAssert parseBin("0100111001101001111011010100111001101001", num64) == 40
doAssert num64 == 336784608873
```

```nim
var num: int
doAssert parseBin("0100_1110_0110_1001_1110_1101", num) == 29
doAssert num == 5138925
doAssert parseBin("3", num) == 0
var num8: int8
doAssert parseBin("0b_0100_1110_0110_1001_1110_1101", num8) == 32
doAssert num8 == 0b1110_1101'i8
doAssert parseBin("0b_0100_1110_0110_1001_1110_1101", num8, 3, 9) == 9
doAssert num8 == 0b0100_1110'i8
var num8u: uint8
doAssert parseBin("0b_0100_1110_0110_1001_1110_1101", num8u) == 32
doAssert num8u == 237
var num64: int64
doAssert parseBin("0100111001101001111011010100111001101001", num64) == 40
doAssert num64 == 336784608873
```

```nim
var c: char
doAssert "nim".parseChar(c, 3) == 0
doAssert c == '\0'
doAssert "nim".parseChar(c, 0) == 1
doAssert c == 'n'
```

```nim
var c: char
doAssert "nim".parseChar(c, 3) == 0
doAssert c == '\0'
doAssert "nim".parseChar(c, 0) == 1
doAssert c == 'n'
```

```nim
var res: float
doAssert parseFloat("32", res, 0) == 2
doAssert res == 32.0
doAssert parseFloat("32.57", res, 0) == 5
doAssert res == 32.57
doAssert parseFloat("32.57", res, 3) == 2
doAssert res == 57.00
```

```nim
var res: float
doAssert parseFloat("32", res, 0) == 2
doAssert res == 32.0
doAssert parseFloat("32.57", res, 0) == 5
doAssert res == 32.57
doAssert parseFloat("32.57", res, 3) == 2
doAssert res == 57.00
```

```nim
var num: int
doAssert parseHex("4E_69_ED", num) == 8
doAssert num == 5138925
doAssert parseHex("X", num) == 0
doAssert parseHex("#ABC", num) == 4
var num8: int8
doAssert parseHex("0x_4E_69_ED", num8) == 11
doAssert num8 == 0xED'i8
doAssert parseHex("0x_4E_69_ED", num8, 3, 2) == 2
doAssert num8 == 0x4E'i8
var num8u: uint8
doAssert parseHex("0x_4E_69_ED", num8u) == 11
doAssert num8u == 237
var num64: int64
doAssert parseHex("4E69ED4E69ED", num64) == 12
doAssert num64 == 86216859871725
```

```nim
var num: int
doAssert parseHex("4E_69_ED", num) == 8
doAssert num == 5138925
doAssert parseHex("X", num) == 0
doAssert parseHex("#ABC", num) == 4
var num8: int8
doAssert parseHex("0x_4E_69_ED", num8) == 11
doAssert num8 == 0xED'i8
doAssert parseHex("0x_4E_69_ED", num8, 3, 2) == 2
doAssert num8 == 0x4E'i8
var num8u: uint8
doAssert parseHex("0x_4E_69_ED", num8u) == 11
doAssert num8u == 237
var num64: int64
doAssert parseHex("4E69ED4E69ED", num64) == 12
doAssert num64 == 86216859871725
```

```nim
doAssert parseIdent("Hello World", 0) == "Hello"
doAssert parseIdent("Hello World", 1) == "ello"
doAssert parseIdent("Hello World", 5) == ""
doAssert parseIdent("Hello World", 6) == "World"
```

```nim
var res: string
doAssert parseIdent("Hello World", res, 0) == 5
doAssert res == "Hello"
doAssert parseIdent("Hello World", res, 1) == 4
doAssert res == "ello"
doAssert parseIdent("Hello World", res, 6) == 5
doAssert res == "World"
```

```nim
var res: string
doAssert parseIdent("Hello World", res, 0) == 5
doAssert res == "Hello"
doAssert parseIdent("Hello World", res, 1) == 4
doAssert res == "ello"
doAssert parseIdent("Hello World", res, 6) == 5
doAssert res == "World"
```

```nim
doAssert parseIdent("Hello World", 0) == "Hello"
doAssert parseIdent("Hello World", 1) == "ello"
doAssert parseIdent("Hello World", 5) == ""
doAssert parseIdent("Hello World", 6) == "World"
```

```nim
var res: int
doAssert parseInt("-2024_05_02", res) == 11
doAssert res == -20240502
```

```nim
var res: int
doAssert parseInt("-2024_05_02", res) == 11
doAssert res == -20240502
doAssert parseInt("-2024_05_02", res, 7) == 4
doAssert res == 502
```

```nim
var num: int
doAssert parseOct("0o23464755", num) == 10
doAssert num == 5138925
doAssert parseOct("8", num) == 0
var num8: int8
doAssert parseOct("0o_1464_755", num8) == 11
doAssert num8 == -19
doAssert parseOct("0o_1464_755", num8, 3, 3) == 3
doAssert num8 == 102
var num8u: uint8
doAssert parseOct("1464755", num8u) == 7
doAssert num8u == 237
var num64: int64
doAssert parseOct("2346475523464755", num64) == 16
doAssert num64 == 86216859871725
```

```nim
var num: int
doAssert parseOct("0o23464755", num) == 10
doAssert num == 5138925
doAssert parseOct("8", num) == 0
var num8: int8
doAssert parseOct("0o_1464_755", num8) == 11
doAssert num8 == -19
doAssert parseOct("0o_1464_755", num8, 3, 3) == 3
doAssert num8 == 102
var num8u: uint8
doAssert parseOct("1464755", num8u) == 7
doAssert num8u == 237
var num64: int64
doAssert parseOct("2346475523464755", num64) == 16
doAssert num64 == 86216859871725
```

```nim
var res = 0
discard parseSaturatedNatural("848", res)
doAssert res == 848
```

```nim
var res = 0
discard parseSaturatedNatural("848", res)
doAssert res == 848
```

```nim
var res: int64  # caller must still know if 'b' refers to bytes|bits
doAssert parseSize("10.5 MB", res) == 7
doAssert res == 10_500_000  # decimal metric Mega prefix
doAssert parseSize("64 mib", res) == 6
doAssert res == 67108864    # 64 shl 20
doAssert parseSize("1G/h", res, true) == 2 # '/' stops parse
doAssert res == 1073741824  # 1 shl 30, forced binary metric
```

```nim
var res: uint
doAssert parseUInt("3450", res) == 4
doAssert res == 3450
doAssert parseUInt("3450", res, 2) == 2
doAssert res == 50
```

```nim
var res: uint
doAssert parseUInt("3450", res) == 4
doAssert res == 3450
doAssert parseUInt("3450", res, 2) == 2
doAssert res == 50
```

```nim
var myToken: string
doAssert parseUntil("Hello World", myToken, 'W') == 6
doAssert myToken == "Hello "
doAssert parseUntil("Hello World", myToken, 'o') == 4
doAssert myToken == "Hell"
doAssert parseUntil("Hello World", myToken, 'o', 2) == 2
doAssert myToken == "ll"
```

```nim
var myToken: string
doAssert parseUntil("Hello World", myToken, {'W', 'o', 'r'}) == 4
doAssert myToken == "Hell"
doAssert parseUntil("Hello World", myToken, {'W', 'r'}) == 6
doAssert myToken == "Hello "
doAssert parseUntil("Hello World", myToken, {'W', 'r'}, 3) == 3
doAssert myToken == "lo "
```

```nim
var myToken: string
doAssert parseUntil("Hello World", myToken, "Wor") == 6
doAssert myToken == "Hello "
doAssert parseUntil("Hello World", myToken, "Wor", 2) == 4
doAssert myToken == "llo "
```

```nim
var myToken: string
doAssert parseUntil("Hello World", myToken, 'W') == 6
doAssert myToken == "Hello "
doAssert parseUntil("Hello World", myToken, 'o') == 4
doAssert myToken == "Hell"
doAssert parseUntil("Hello World", myToken, 'o', 2) == 2
doAssert myToken == "ll"
```

```nim
var myToken: string
doAssert parseUntil("Hello World", myToken, {'W', 'o', 'r'}) == 4
doAssert myToken == "Hell"
doAssert parseUntil("Hello World", myToken, {'W', 'r'}) == 6
doAssert myToken == "Hello "
doAssert parseUntil("Hello World", myToken, {'W', 'r'}, 3) == 3
doAssert myToken == "lo "
```

```nim
var myToken: string
doAssert parseUntil("Hello World", myToken, "Wor") == 6
doAssert myToken == "Hello "
doAssert parseUntil("Hello World", myToken, "Wor", 2) == 4
doAssert myToken == "llo "
```

```nim
var myToken: string
doAssert parseWhile("Hello World", myToken, {'W', 'o', 'r'}, 0) == 0
doAssert myToken.len() == 0
doAssert parseWhile("Hello World", myToken, {'W', 'o', 'r'}, 6) == 3
doAssert myToken == "Wor"
```

```nim
var myToken: string
doAssert parseWhile("Hello World", myToken, {'W', 'o', 'r'}, 0) == 0
doAssert myToken.len() == 0
doAssert parseWhile("Hello World", myToken, {'W', 'o', 'r'}, 6) == 3
doAssert myToken == "Wor"
```

```nim
doAssert skip("2019-01-22", "2019", 0) == 4
doAssert skip("2019-01-22", "19", 0) == 0
doAssert skip("2019-01-22", "19", 2) == 2
doAssert skip("CAPlow", "CAP", 0) == 3
doAssert skip("CAPlow", "cap", 0) == 0
```

```nim
doAssert skip("2019-01-22", "2019", 0) == 4
doAssert skip("2019-01-22", "19", 0) == 0
doAssert skip("2019-01-22", "19", 2) == 2
doAssert skip("CAPlow", "CAP", 0) == 3
doAssert skip("CAPlow", "cap", 0) == 0
```

```nim
doAssert skipIgnoreCase("CAPlow", "CAP", 0) == 3
doAssert skipIgnoreCase("CAPlow", "cap", 0) == 3
```

```nim
doAssert skipIgnoreCase("CAPlow", "CAP", 0) == 3
doAssert skipIgnoreCase("CAPlow", "cap", 0) == 3
```

```nim
doAssert skipUntil("Hello World", 'o', 0) == 4
doAssert skipUntil("Hello World", 'o', 4) == 0
doAssert skipUntil("Hello World", 'W', 0) == 6
doAssert skipUntil("Hello World", 'w', 0) == 11
```

```nim
doAssert skipUntil("Hello World", {'W', 'e'}, 0) == 1
doAssert skipUntil("Hello World", {'W'}, 0) == 6
doAssert skipUntil("Hello World", {'W', 'd'}, 0) == 6
```

```nim
doAssert skipUntil("Hello World", 'o', 0) == 4
doAssert skipUntil("Hello World", 'o', 4) == 0
doAssert skipUntil("Hello World", 'W', 0) == 6
doAssert skipUntil("Hello World", 'w', 0) == 11
```

```nim
doAssert skipUntil("Hello World", {'W', 'e'}, 0) == 1
doAssert skipUntil("Hello World", {'W'}, 0) == 6
doAssert skipUntil("Hello World", {'W', 'd'}, 0) == 6
```

```nim
doAssert skipWhile("Hello World", {'H', 'e'}) == 2
doAssert skipWhile("Hello World", {'e'}) == 0
doAssert skipWhile("Hello World", {'W', 'o', 'r'}, 6) == 3
```

```nim
doAssert skipWhile("Hello World", {'H', 'e'}) == 2
doAssert skipWhile("Hello World", {'e'}) == 0
doAssert skipWhile("Hello World", {'W', 'o', 'r'}, 6) == 3
```

```nim
doAssert skipWhitespace("Hello World", 0) == 0
doAssert skipWhitespace(" Hello World", 0) == 1
doAssert skipWhitespace("Hello World", 5) == 1
doAssert skipWhitespace("Hello  World", 5) == 2
```

```nim
doAssert skipWhitespace("Hello World", 0) == 0
doAssert skipWhitespace(" Hello World", 0) == 1
doAssert skipWhitespace("Hello World", 5) == 1
doAssert skipWhitespace("Hello  World", 5) == 2
```

```nim
var outp: seq[tuple[kind: InterpolatedKind, value: string]]
for k, v in interpolatedFragments("  $this is ${an  example}  $$"):
  outp.add (k, v)
doAssert outp == @[(ikStr, "  "),
                   (ikVar, "this"),
                   (ikStr, " is "),
                   (ikExpr, "an  example"),
                   (ikStr, "  "),
                   (ikDollar, "$")]
```

```nim
var outp: seq[tuple[kind: InterpolatedKind, value: string]]
for k, v in interpolatedFragments("  $this is ${an  example}  $$"):
  outp.add (k, v)
doAssert outp == @[(ikStr, "  "),
                   (ikVar, "this"),
                   (ikStr, " is "),
                   (ikExpr, "an  example"),
                   (ikStr, "  "),
                   (ikDollar, "$")]
```

## Iterator

### interpolatedFragments

[ref: #symbol-interpolatedfragments]

**Input:**
- `s: openArray[char]`

**Output:** `tuple[kind: InterpolatedKind, value: string]`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Tokenizes the string s into substrings for interpolation purposes.

### interpolatedFragments

[ref: #symbol-interpolatedfragments]

**Input:**
- `s: string`

**Output:** `tuple[kind: InterpolatedKind, value: string]`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Tokenizes the string s into substrings for interpolation purposes.

## Proc

### captureBetween

[ref: #symbol-capturebetween]

**Input:**
- `s: openArray[char]`
- `first: char`
- `second:  = '\x00'`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Finds the first occurrence of first, then returns everything from there up to second (if second is '0', then first is used).

### captureBetween

[ref: #symbol-capturebetween]

**Input:**
- `s: string`
- `first: char`
- `second:  = '\x00'`
- `start:  = 0`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Finds the first occurrence of first, then returns everything from there up to second (if second is '0', then first is used).

### parseBiggestFloat

[ref: #symbol-parsebiggestfloat]

**Input:**
- `s: openArray[char]`
- `number: var BiggestFloat`

**Output:** `int`
**Pragmas:** `magic: "ParseBiggestFloat"`, `importc: "nimParseBiggestFloat"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a float and stores the value into number. Result is the number of processed chars or 0 if a parsing error occurred.

### parseBiggestFloat

[ref: #symbol-parsebiggestfloat]

**Input:**
- `s: string`
- `number: var BiggestFloat`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a float starting at start and stores the value into number. Result is the number of processed chars or 0 if a parsing error occurred.

### parseBiggestInt

[ref: #symbol-parsebiggestint]

**Input:**
- `s: openArray[char]`
- `number: var BiggestInt`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npuParseBiggestInt"`, `noSideEffect`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses an integer and stores the value into number. Result is the number of processed chars or 0 if there is no integer. ValueError is raised if the parsed integer is out of the valid range.

### parseBiggestInt

[ref: #symbol-parsebiggestint]

**Input:**
- `s: string`
- `number: var BiggestInt`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses an integer starting at start and stores the value into number. Result is the number of processed chars or 0 if there is no integer. ValueError is raised if the parsed integer is out of the valid range.

### parseBiggestUInt

[ref: #symbol-parsebiggestuint]

**Input:**
- `s: openArray[char]`
- `number: var BiggestUInt`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npuParseBiggestUInt"`, `noSideEffect`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses an unsigned integer and stores the value into number. ValueError is raised if the parsed integer is out of the valid range.

### parseBiggestUInt

[ref: #symbol-parsebiggestuint]

**Input:**
- `s: string`
- `number: var BiggestUInt`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses an unsigned integer starting at start and stores the value into number. ValueError is raised if the parsed integer is out of the valid range.

### parseBin

[ref: #symbol-parsebin]

Parses a binary number and stores its value in number.

**Input:**
- `s: openArray[char]`
- `number: var T`
- `maxLen:  = 0`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Parses a binary number and stores its value in number.

Returns the number of the parsed characters or 0 in case of an error. If error, the value of number is not changed.

If maxLen == 0, the parsing continues until the first non-bin character or to the end of the string. Otherwise, no more than maxLen characters are parsed starting from the start position.

It does not check for overflow. If the value represented by the string is too big to fit into number, only the value of last fitting characters will be stored in number without producing an error.

### parseBin

[ref: #symbol-parsebin]

Parses a binary number and stores its value in number.

**Input:**
- `s: string`
- `number: var T`
- `start:  = 0`
- `maxLen:  = 0`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Parses a binary number and stores its value in number.

Returns the number of the parsed characters or 0 in case of an error. If error, the value of number is not changed.

If maxLen == 0, the parsing continues until the first non-bin character or to the end of the string. Otherwise, no more than maxLen characters are parsed starting from the start position.

It does not check for overflow. If the value represented by the string is too big to fit into number, only the value of last fitting characters will be stored in number without producing an error.

### parseChar

[ref: #symbol-parsechar]

**Input:**
- `s: openArray[char]`
- `c: var char`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a single character, stores it in c and returns 1. In case of error (if start >= s.len) it returns 0 and the value of c is unchanged.

### parseChar

[ref: #symbol-parsechar]

**Input:**
- `s: string`
- `c: var char`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a single character, stores it in c and returns 1. In case of error (if start >= s.len) it returns 0 and the value of c is unchanged.

### parseFloat

[ref: #symbol-parsefloat]

**Input:**
- `s: openArray[char]`
- `number: var float`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npuParseFloat"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a float and stores the value into number. Result is the number of processed chars or 0 if there occurred a parsing error.

### parseFloat

[ref: #symbol-parsefloat]

**Input:**
- `s: string`
- `number: var float`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a float starting at start and stores the value into number. Result is the number of processed chars or 0 if there occurred a parsing error.

### parseHex

[ref: #symbol-parsehex]

Parses a hexadecimal number and stores its value in number.

**Input:**
- `s: openArray[char]`
- `number: var T`
- `maxLen:  = 0`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Parses a hexadecimal number and stores its value in number.

Returns the number of the parsed characters or 0 in case of an error. If error, the value of number is not changed.

If maxLen == 0, the parsing continues until the first non-hex character or to the end of the string. Otherwise, no more than maxLen characters are parsed starting from the start position.

It does not check for overflow. If the value represented by the string is too big to fit into number, only the value of last fitting characters will be stored in number without producing an error.

### parseHex

[ref: #symbol-parsehex]

Parses a hexadecimal number and stores its value in number.

**Input:**
- `s: string`
- `number: var T`
- `start:  = 0`
- `maxLen:  = 0`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Parses a hexadecimal number and stores its value in number.

Returns the number of the parsed characters or 0 in case of an error. If error, the value of number is not changed.

If maxLen == 0, the parsing continues until the first non-hex character or to the end of the string. Otherwise, no more than maxLen characters are parsed starting from the start position.

It does not check for overflow. If the value represented by the string is too big to fit into number, only the value of last fitting characters will be stored in number without producing an error.

### parseIdent

[ref: #symbol-parseident]

**Input:**
- `s: openArray[char]`
- `ident: var string`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses an identifier and stores it in ident. Returns the number of the parsed characters or 0 in case of an error. If error, the value of ident is not changed.

### parseIdent

[ref: #symbol-parseident]

**Input:**
- `s: openArray[char]`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses an identifier and returns it or an empty string in case of an error.

### parseIdent

[ref: #symbol-parseident]

**Input:**
- `s: string`
- `ident: var string`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses an identifier and stores it in ident. Returns the number of the parsed characters or 0 in case of an error. If error, the value of ident is not changed.

### parseIdent

[ref: #symbol-parseident]

**Input:**
- `s: string`
- `start:  = 0`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses an identifier and returns it or an empty string in case of an error.

### parseInt

[ref: #symbol-parseint]

**Input:**
- `s: openArray[char]`
- `number: var int`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npuParseInt"`, `noSideEffect`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses an integer and stores the value into number. Result is the number of processed chars or 0 if there is no integer. ValueError is raised if the parsed integer is out of the valid range.

### parseInt

[ref: #symbol-parseint]

**Input:**
- `s: string`
- `number: var int`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `noSideEffect`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses an integer starting at start and stores the value into number. Result is the number of processed chars or 0 if there is no integer. ValueError is raised if the parsed integer is out of the valid range.

### parseOct

[ref: #symbol-parseoct]

Parses an octal number and stores its value in number.

**Input:**
- `s: openArray[char]`
- `number: var T`
- `maxLen:  = 0`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Parses an octal number and stores its value in number.

Returns the number of the parsed characters or 0 in case of an error. If error, the value of number is not changed.

If maxLen == 0, the parsing continues until the first non-oct character or to the end of the string. Otherwise, no more than maxLen characters are parsed starting from the start position.

It does not check for overflow. If the value represented by the string is too big to fit into number, only the value of last fitting characters will be stored in number without producing an error.

### parseOct

[ref: #symbol-parseoct]

Parses an octal number and stores its value in number.

**Input:**
- `s: string`
- `number: var T`
- `start:  = 0`
- `maxLen:  = 0`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `noSideEffect`

Parses an octal number and stores its value in number.

Returns the number of the parsed characters or 0 in case of an error. If error, the value of number is not changed.

If maxLen == 0, the parsing continues until the first non-oct character or to the end of the string. Otherwise, no more than maxLen characters are parsed starting from the start position.

It does not check for overflow. If the value represented by the string is too big to fit into number, only the value of last fitting characters will be stored in number without producing an error.

### parseSaturatedNatural

[ref: #symbol-parsesaturatednatural]

**Input:**
- `s: openArray[char]`
- `b: var int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses a natural number into b. This cannot raise an overflow error. high(int) is returned for an overflow. The number of processed character is returned. This is usually what you really want to use instead of parseInt.


[Next](parseutils_2.md)
