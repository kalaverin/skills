---
source_hash: 4239fe023f00ab0f
source_path: lib/impure/nre.nim
---

# nre

[ref: #module-nre]

# [What is NRE?](#what-is-nreqmark)

A regular expression library for Nim using PCRE to do the hard work.

For documentation on how to write patterns, there exists [the official PCRE pattern documentation](https://www.pcre.org/original/doc/html/pcrepattern.html). You can also search the internet for a wide variety of third-party documentation and tools.

**Warning:**
If you love sequtils.toSeq we have bad news for you. This library doesn't work with it due to documented compiler limitations. As a workaround, use this:

**Note:**
There are also alternative nimble packages such as [tinyre](https://github.com/khchen/tinyre) and [regex](https://github.com/nitely/nim-regex).

## [Licencing](#what-is-nreqmark-licencing)

PCRE has [some additional terms](https://pcre.sourceforge.net/license.txt) that you must agree to in order to use this module.

## Examples

```nim
import std/nre
# either `import std/nre except toSeq` or fully qualify `sequtils.toSeq`:
import std/sequtils
iterator iota(n: int): int =
  for i in 0..<n: yield i
assert sequtils.toSeq(iota(3)) == @[0, 1, 2]
```

```nim
import std/nre
import std/sugar
let vowels = re"[aeoui]"
let bounds = collect:
  for match in "moiga".findIter(vowels): match.matchBounds
assert bounds == @[1 .. 1, 2 .. 2, 4 .. 4]
from std/sequtils import toSeq
let s = sequtils.toSeq("moiga".findIter(vowels))
  # fully qualified to avoid confusion with nre.toSeq
assert s.len == 3

let firstVowel = "foo".find(vowels)
let hasVowel = firstVowel.isSome()
assert hasVowel
let matchBounds = firstVowel.get().captureBounds[-1]
assert matchBounds.a == 1

# as with module `re`, unless specified otherwise, `start` parameter in each
# proc indicates where the scan starts, but outputs are relative to the start
# of the input string, not to `start`:
assert find("uxabc", re"(?<=x|y)ab", start = 1).get.captures[-1] == "ab"
assert find("uxabc", re"ab", start = 3).isNone
```

```nim
assert "abc".contains(re"bc")
assert not "abc".contains(re"cd")
assert not "abc".contains(re"a", start = 1)
```

```nim
assert escapeRe("fly+wind") == "fly\\+wind"
assert escapeRe("!") == "\\!"
assert escapeRe("nim*") == "nim\\*"
```

```nim
assert "foo".match(re"f").isSome
assert "foo".match(re"o").isNone

assert "abc".match(re"(\w)").get.captures[0] == "a"
assert "abc".match(re"(?<letter>\w)").get.captures["letter"] == "a"
assert "abc".match(re"(\w)\w").get.captures[-1] == "ab"

assert "abc".match(re"(\w)").get.captureBounds[0] == 0 .. 0
assert 0 in "abc".match(re"(\w)").get.captureBounds
assert "abc".match(re"").get.captureBounds[-1] == 0 .. -1
assert "abc".match(re"abc").get.captureBounds[-1] == 0 .. 2
```

```nim
# -  If the match is zero-width, then the string is still split:
assert "123".split(re"") == @["1", "2", "3"]

# -  If the pattern has a capture in it, it is added after the string
#    split:
assert "12".split(re"(\d)") == @["", "1", "", "2", ""]

# -  If `maxsplit != -1`, then the string will only be split
#    `maxsplit - 1` times. This means that there will be `maxsplit`
#    strings in the output seq.
assert "1.2.3".split(re"\.", maxsplit = 2) == @["1", "2.3"]
```

```nim
import std/sugar
assert collect(for a in "2222".findIter(re"22"): a.match) == @["22", "22"]
 # not @["22", "22", "22"]
```

## Iterator

### findIter

[ref: #symbol-finditer]

**Input:**
- `str: string`
- `pattern: Regex`
- `start:  = 0`
- `endpos:  = int.high`

**Output:** `RegexMatch`
**Pragmas:** `raises: [ValueError, RegexInternalError, InvalidUnicodeError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError, RegexInternalError, InvalidUnicodeError`, `tags: `, `forbids: `

Works the same as [find(...)](#find,string,Regex,int), but finds every non-overlapping match:

### items

[ref: #symbol-items]

**Input:**
- `pattern: CaptureBounds`
- `default:  = none(HSlice[int, int])`

**Output:** `Option[HSlice[int, int]]`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### items

[ref: #symbol-items]

**Input:**
- `pattern: Captures`
- `default: Option[string] = none(string)`

**Output:** `Option[string]`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `pattern: RegexMatch`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `a: Regex`
- `b: Regex`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `==`

[ref: #symbol-]

**Input:**
- `a: RegexMatch`
- `b: RegexMatch`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]`

[ref: #symbol-]

**Input:**
- `pattern: CaptureBounds`
- `i: int`

**Output:** `HSlice[int, int]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]`

[ref: #symbol-]

**Input:**
- `pattern: Captures`
- `i: int`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]`

[ref: #symbol-]

**Input:**
- `pattern: CaptureBounds`
- `name: string`

**Output:** `HSlice[int, int]`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

### `[]`

[ref: #symbol-]

**Input:**
- `pattern: Captures`
- `name: string`

**Output:** `string`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

### captureBounds

[ref: #symbol-capturebounds]

**Input:**
- `pattern: RegexMatch`

**Output:** `CaptureBounds`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### captureCount

[ref: #symbol-capturecount]

**Input:**
- `pattern: Regex`

**Output:** `int`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### captureNameId

[ref: #symbol-capturenameid]

**Input:**
- `pattern: Regex`

**Output:** `Table[string, int]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### captures

[ref: #symbol-captures]

**Input:**
- `pattern: RegexMatch`

**Output:** `Captures`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### contains

[ref: #symbol-contains]

**Input:**
- `pattern: CaptureBounds`
- `i: int`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### contains

[ref: #symbol-contains]

**Input:**
- `pattern: Captures`
- `i: int`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### contains

[ref: #symbol-contains]

**Input:**
- `pattern: CaptureBounds`
- `name: string`

**Output:** `bool`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

### contains

[ref: #symbol-contains]

**Input:**
- `pattern: Captures`
- `name: string`

**Output:** `bool`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

### contains

[ref: #symbol-contains]

**Input:**
- `str: string`
- `pattern: Regex`
- `start:  = 0`
- `endpos:  = int.high`

**Output:** `bool`
**Pragmas:** `raises: [ValueError, RegexInternalError, InvalidUnicodeError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError, RegexInternalError, InvalidUnicodeError`, `tags: `, `forbids: `

Determine if the string contains the given pattern between the end and start positions: This function is equivalent to isSome(str.find(pattern, start, endpos)).

### escapeRe

[ref: #symbol-escapere]

Escapes the string so it doesn't match any special characters. Incompatible with the Extra flag (X).

**Input:**
- `str: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Escapes the string so it doesn't match any special characters. Incompatible with the Extra flag (X).

Escaped char: \ + \* ? [ ^ ] $ ( ) { } = ! < > | : -

### find

[ref: #symbol-find]

Finds the given pattern in the string between the end and start positions.

**Input:**
- `str: string`
- `pattern: Regex`
- `start:  = 0`
- `endpos:  = int.high`

**Output:** `Option[RegexMatch]`
**Pragmas:** `raises: [ValueError, RegexInternalError, InvalidUnicodeError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError, RegexInternalError, InvalidUnicodeError`, `tags: `, `forbids: `

Finds the given pattern in the string between the end and start positions.

start
:   The start point at which to start matching. |abc is 0; a|bc is 1

endpos
:   The maximum index for a match; int.high means the end of the string, otherwise it’s an inclusive upper bound.

### findAll

[ref: #symbol-findall]

**Input:**
- `str: string`
- `pattern: Regex`
- `start:  = 0`
- `endpos:  = int.high`

**Output:** `seq[string]`
**Pragmas:** `raises: [ValueError, RegexInternalError, InvalidUnicodeError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError, RegexInternalError, InvalidUnicodeError`, `tags: `, `forbids: `

### match

[ref: #symbol-match]

**Input:**
- `pattern: RegexMatch`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### match

[ref: #symbol-match]

**Input:**
- `str: string`
- `pattern: Regex`
- `start:  = 0`
- `endpos:  = int.high`

**Output:** `Option[RegexMatch]`
**Pragmas:** `raises: [ValueError, RegexInternalError, InvalidUnicodeError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError, RegexInternalError, InvalidUnicodeError`, `tags: `, `forbids: `

Like [find(...)](#find,string,Regex,int), but anchored to the start of the string.

### matchBounds

[ref: #symbol-matchbounds]

**Input:**
- `pattern: RegexMatch`

**Output:** `HSlice[int, int]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### re

[ref: #symbol-re]

**Input:**
- `pattern: string`

**Output:** `Regex`
**Pragmas:** `raises: [KeyError, SyntaxError, StudyError, ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError, SyntaxError, StudyError, ValueError`, `tags: `, `forbids: `

### replace

[ref: #symbol-replace]

Replaces each match of Regex in the string with subproc, which should never be or return nil.

**Input:**
- `str: string`
- `pattern: Regex`
- `subproc: proc (match: RegexMatch): string`

**Output:** `string`
**Pragmas:** `raises: [ValueError, RegexInternalError, InvalidUnicodeError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, RegexInternalError, InvalidUnicodeError, Exception`, `tags: RootEffect`, `forbids: `

Replaces each match of Regex in the string with subproc, which should never be or return nil.

If subproc is a proc (RegexMatch): string, then it is executed with each match and the return value is the replacement value.

If subproc is a proc (string): string, then it is executed with the full text of the match and the return value is the replacement value.

If subproc is a string, the syntax is as follows:

* $$ - literal $
* $123 - capture number 123
* $foo - named capture foo
* ${foo} - same as above
* $1$# - first and second captures
* $# - first capture
* $0 - full match

If a given capture is missing, IndexDefect thrown for un-named captures and KeyError for named captures.

### replace

[ref: #symbol-replace]

**Input:**
- `str: string`
- `pattern: Regex`
- `subproc: proc (match: string): string`

**Output:** `string`
**Pragmas:** `raises: [ValueError, RegexInternalError, InvalidUnicodeError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, RegexInternalError, InvalidUnicodeError, Exception`, `tags: RootEffect`, `forbids: `

### replace

[ref: #symbol-replace]

**Input:**
- `str: string`
- `pattern: Regex`
- `sub: string`

**Output:** `string`
**Pragmas:** `raises: [ValueError, RegexInternalError, InvalidUnicodeError, KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError, RegexInternalError, InvalidUnicodeError, KeyError`, `tags: `, `forbids: `

### split

[ref: #symbol-split]

Splits the string with the given regex. This works according to the rules that Perl and Javascript use.

**Input:**
- `str: string`
- `pattern: Regex`
- `maxSplit:  = -1`
- `start:  = 0`

**Output:** `seq[string]`
**Pragmas:** `raises: [ValueError, RegexInternalError, InvalidUnicodeError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError, RegexInternalError, InvalidUnicodeError`, `tags: `, `forbids: `

Splits the string with the given regex. This works according to the rules that Perl and Javascript use.

start behaves the same as in [find(...)](#find,string,Regex,int).

### toSeq

[ref: #symbol-toseq]

**Input:**
- `pattern: CaptureBounds`
- `default:  = none(HSlice[int, int])`

**Output:** `seq[Option[HSlice[int, int]]]`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### toSeq

[ref: #symbol-toseq]

**Input:**
- `pattern: Captures`
- `default: Option[string] = none(string)`

**Output:** `seq[Option[string]]`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### toTable

[ref: #symbol-totable]

**Input:**
- `pattern: Captures`

**Output:** `Table[string, string]`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

### toTable

[ref: #symbol-totable]

**Input:**
- `pattern: CaptureBounds`

**Output:** `Table[string, HSlice[int, int]]`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

## Type

### CaptureBounds

[ref: #symbol-capturebounds]

```nim
CaptureBounds = distinct RegexMatch
```

### Captures

[ref: #symbol-captures]

```nim
Captures = distinct RegexMatch
```

### InvalidUnicodeError

[ref: #symbol-invalidunicodeerror]

```nim
InvalidUnicodeError = ref object of RegexError
  pos*: int                  ## the location of the invalid unicode in bytes
```

Thrown when matching fails due to invalid unicode in strings

### Regex

[ref: #symbol-regex]

Represents the pattern that things are matched against, constructed with re(string). Examples: re"foo", re(r"(\*ANYCRLF)(?x)foo # comment".

```nim
Regex = ref RegexDesc
```

Represents the pattern that things are matched against, constructed with re(string). Examples: re"foo", re(r"(\*ANYCRLF)(?x)foo # comment".

pattern: string
:   the string that was used to create the pattern. For details on how to write a pattern, please see [the official PCRE pattern documentation.](https://www.pcre.org/original/doc/html/pcrepattern.html)

captureCount: int
:   the number of captures that the pattern has.

captureNameId: Table[string, int]
:   a table from the capture names to their numeric id.

### [Options](#licencing-options)

The following options may appear anywhere in the pattern, and they affect the rest of it.

* (?i) - case insensitive
* (?m) - multi-line: ^ and $ match the beginning and end of lines, not of the subject string
* (?s) - . also matches newline (*dotall*)
* (?U) - expressions are not greedy by default. ? can be added to a qualifier to make it greedy
* (?x) - whitespace and comments (#) are ignored (*extended*)
* (?X) - character escapes without special meaning (\w vs. \a) are errors (*extra*)

One or a combination of these options may appear only at the beginning of the pattern:

* (\*UTF8) - treat both the pattern and subject as UTF-8
* (\*UCP) - Unicode character properties; \w matches я
* (\*U) - a combination of the two options above
* (\*FIRSTLINE\*) - fails if there is not a match on the first line
* (\*NO\_AUTO\_CAPTURE) - turn off auto-capture for groups; (?<name>...) can be used to capture
* (\*CR) - newlines are separated by \r
* (\*LF) - newlines are separated by \n (UNIX default)
* (\*CRLF) - newlines are separated by \r\n (Windows default)
* (\*ANYCRLF) - newlines are separated by any of the above
* (\*ANY) - newlines are separated by any of the above and Unicode newlines:

  single characters VT (vertical tab, U+000B), FF (form feed, U+000C), NEL (next line, U+0085), LS (line separator, U+2028), and PS (paragraph separator, U+2029). For the 8-bit library, the last two are recognized only in UTF-8 mode. — man pcre
* (\*JAVASCRIPT\_COMPAT) - JavaScript compatibility
* (\*NO\_STUDY) - turn off studying; study is enabled by default

For more details on the leading option groups, see the [Option Setting](https://man7.org/linux/man-pages/man3/pcresyntax.3.html#OPTION_SETTING) and the [Newline Convention](https://man7.org/linux/man-pages/man3/pcresyntax.3.html#NEWLINE_CONVENTION) sections of the [PCRE syntax manual](https://man7.org/linux/man-pages/man3/pcresyntax.3.html).

Some of these options are not part of PCRE and are converted by nre into PCRE flags. These include NEVER\_UTF, ANCHORED, DOLLAR\_ENDONLY, FIRSTLINE, NO\_AUTO\_CAPTURE, JAVASCRIPT\_COMPAT, U, NO\_STUDY. In other PCRE wrappers, you will need to pass these as separate flags to PCRE.

### RegexDesc

[ref: #symbol-regexdesc]

```nim
RegexDesc = object
  pattern*: string
```

### RegexError

[ref: #symbol-regexerror]

```nim
RegexError = ref object of CatchableError
```

### RegexInternalError

[ref: #symbol-regexinternalerror]

```nim
RegexInternalError = ref object of RegexError
```

Internal error in the module, this probably means that there is a bug

### RegexMatch

[ref: #symbol-regexmatch]

Usually seen as Option[RegexMatch](#RegexMatch), it represents the result of an execution. On failure, it is none, on success, it is some.

```nim
RegexMatch = object
  pattern*: Regex            ## The regex doing the matching.
                             ## Not nil.
  str*: string               ## The string that was matched against.
```

Usually seen as Option[RegexMatch](#RegexMatch), it represents the result of an execution. On failure, it is none, on success, it is some.

pattern: Regex
:   the pattern that is being matched

str: string
:   the string that was matched against

captures[]: string
:   the string value of whatever was captured at that id. If the value is invalid, then behavior is undefined. If the id is -1, then the whole match is returned. If the given capture was not matched, nil is returned. See examples for match.

captureBounds[]: HSlice[int, int]
:   gets the bounds of the given capture according to the same rules as the above. If the capture is not filled, then None is returned. The bounds are both inclusive. See examples for match.

match: string
:   the full text of the match.

matchBounds: HSlice[int, int]
:   the bounds of the match, as in captureBounds[]

(captureBounds|captures).toTable
:   returns a table with each named capture as a key.

(captureBounds|captures).toSeq
:   returns all the captures by their number.

$: string
:   same as match

### StudyError

[ref: #symbol-studyerror]

```nim
StudyError = ref object of RegexError
```

Thrown when studying the regular expression fails for whatever reason. The message contains the error code.

### SyntaxError

[ref: #symbol-syntaxerror]

```nim
SyntaxError = ref object of RegexError
  pos*: int                  ## the location of the syntax error in bytes
  pattern*: string           ## the pattern that caused the problem
```

Thrown when there is a syntax error in the regular expression string passed in
