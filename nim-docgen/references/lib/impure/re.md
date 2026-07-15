---
source_hash: d79a508c6f7e7dd4
source_path: lib/impure/re.nim
---

# re

[ref: #module-re]

Regular expression support for Nim.

This module is implemented by providing a wrapper around the [PCRE (Perl-Compatible Regular Expressions)](https://www.pcre.org) C library. This means that your application will depend on the PCRE library's licence when using this module, which should not be a problem though.

**Note:**
There are also alternative nimble packages such as [tinyre](https://github.com/khchen/tinyre) and [regex](https://github.com/nitely/nim-regex).

PCRE's licence follows:

# [Licence of the PCRE library](#licence-of-the-pcre-library)

PCRE is a library of functions to support regular expressions whose syntax and semantics are as close as possible to those of the Perl 5 language.

Written by Philip Hazel  
Copyright (c) 1997-2005 University of Cambridge

---

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of the University of Cambridge nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# [Regular expression syntax and semantics](#regular-expression-syntax-and-semantics)

As the regular expressions supported by this module are enormous, the reader is referred to <https://perldoc.perl.org/perlre.html> for the full documentation of Perl's regular expressions.

Because the backslash \ is a meta character both in the Nim programming language and in regular expressions, it is strongly recommended that one uses the *raw* strings of Nim, so that backslashes are interpreted by the regular expression engine:

```
  r"\S"  # matches any character that is not whitespace
```

A regular expression is a pattern that is matched against a subject string from left to right. Most characters stand for themselves in a pattern, and match the corresponding characters in the subject. As a trivial example, the pattern:

```
The quick brown fox
```

matches a portion of a subject string that is identical to itself. The power of regular expressions comes from the ability to include alternatives and repetitions in the pattern. These are encoded in the pattern by the use of metacharacters, which do not stand for themselves but instead are interpreted in some special way.

There are two different sets of metacharacters: those that are recognized anywhere in the pattern except within square brackets, and those that are recognized in square brackets. Outside square brackets, the metacharacters are as follows:

| meta character | meaning |
| --- | --- |
| \ | general escape character with several uses |
| ^ | assert start of string (or line, in multiline mode) |
| $ | assert end of string (or line, in multiline mode) |
| . | match any character except newline (by default) |
| [ | start character class definition |
| | | start of alternative branch |
| ( | start subpattern |
| ) | end subpattern |
| { | start min/max quantifier |
| ? | extends the meaning of ( also 0 or 1 quantifier (equal to {0,1}) also quantifier minimizer |
| \* | 0 or more quantifier (equal to {0,}) |
| + | 1 or more quantifier (equal to {1,}) also "possessive quantifier" |

Part of a pattern that is in square brackets is called a "character class". In a character class the only metacharacters are:

| meta character | meaning |
| --- | --- |
| \ | general escape character |
| ^ | negate the class, but only if the first character |
| - | indicates character range |
| [ | POSIX character class (only if followed by POSIX syntax) |
| ] | terminates the character class |

The following sections describe the use of each of the metacharacters.

## [Backslash](#regular-expression-syntax-and-semantics-backslash)

The backslash character has several uses. Firstly, if it is followed by a non-alphanumeric character, it takes away any special meaning that character may have. This use of backslash as an escape character applies both inside and outside character classes.

For example, if you want to match a \* character, you write \\* in the pattern. This escaping action applies whether or not the following character would otherwise be interpreted as a metacharacter, so it is always safe to precede a non-alphanumeric with backslash to specify that it stands for itself. In particular, if you want to match a backslash, you write \\.

## [Non-printing characters](#regular-expression-syntax-and-semantics-nonminusprinting-characters)

A second use of backslash provides a way of encoding non-printing characters in patterns in a visible manner. There is no restriction on the appearance of non-printing characters, apart from the binary zero that terminates a pattern, but when a pattern is being prepared by text editing, it is usually easier to use one of the following escape sequences than the binary character it represents:

| character | meaning |
| --- | --- |
| \a | alarm, that is, the BEL character (hex 07) |
| \e | escape (hex 1B) |
| \f | formfeed (hex 0C) |
| \n | newline (hex 0A) |
| \r | carriage return (hex 0D) |
| \t | tab (hex 09) |
| \ddd | character with octal code ddd, or backreference |
| \xhh | character with hex code hh |

After \x, from zero to two hexadecimal digits are read (letters can be in upper or lower case). In UTF-8 mode, any number of hexadecimal digits may appear between \x{ and }, but the value of the character code must be less than 2^31 (that is, the maximum hexadecimal value is 7FFFFFFF). If characters other than hexadecimal digits appear between \x{ and }, or if there is no terminating }, this form of escape is not recognized. Instead, the initial \x will be interpreted as a basic hexadecimal escape, with no following digits, giving a character whose value is zero.

After \0 up to two further octal digits are read. In both cases, if there are fewer than two digits, just those that are present are used. Thus the sequence \0\x\07 specifies two binary zeros followed by a BEL character (code value 7). Make sure you supply two digits after the initial zero if the pattern character that follows is itself an octal digit.

The handling of a backslash followed by a digit other than 0 is complicated. Outside a character class, PCRE reads it and any following digits as a decimal number. If the number is less than 10, or if there have been at least that many previous capturing left parentheses in the expression, the entire sequence is taken as a back reference. A description of how this works is given later, following the discussion of parenthesized subpatterns.

Inside a character class, or if the decimal number is greater than 9 and there have not been that many capturing subpatterns, PCRE re-reads up to three octal digits following the backslash, and generates a single byte from the least significant 8 bits of the value. Any subsequent digits stand for themselves. For example:

| example | meaning |
| --- | --- |
| \040 | is another way of writing a space |
| \40 | is the same, provided there are fewer than 40 previous capturing subpatterns |
| \7 | is always a back reference |
| \11 | might be a back reference, or another way of writing a tab |
| \011 | is always a tab |
| \0113 | is a tab followed by the character "3" |
| \113 | might be a back reference, otherwise the character with octal code 113 |
| \377 | might be a back reference, otherwise the byte consisting entirely of 1 bits |
| \81 | is either a back reference, or a binary zero followed by the two characters "8" and "1" |

Note that octal values of 100 or greater must not be introduced by a leading zero, because no more than three octal digits are ever read.

All the sequences that define a single byte value or a single UTF-8 character (in UTF-8 mode) can be used both inside and outside character classes. In addition, inside a character class, the sequence \b is interpreted as the backspace character (hex 08), and the sequence \X is interpreted as the character "X". Outside a character class, these sequences have different meanings (see below).

## [Generic character types](#regular-expression-syntax-and-semantics-generic-character-types)

The third use of backslash is for specifying generic character types. The following are always recognized:

| character type | meaning |
| --- | --- |
| \d | any decimal digit |
| \D | any character that is not a decimal digit |
| \s | any whitespace character |
| \S | any character that is not a whitespace character |
| \w | any "word" character |
| \W | any "non-word" character |

Each pair of escape sequences partitions the complete set of characters into two disjoint sets. Any given character matches one, and only one, of each pair.

These character type sequences can appear both inside and outside character classes. They each match one character of the appropriate type. If the current matching point is at the end of the subject string, all of them fail, since there is no character to match.

For compatibility with Perl, \s does not match the VT character (code 11). This makes it different from the POSIX "space" class. The \s characters are HT (9), LF (10), FF (12), CR (13), and space (32).

A "word" character is an underscore or any character less than 256 that is a letter or digit. The definition of letters and digits is controlled by PCRE's low-valued character tables, and may vary if locale-specific matching is taking place (see "Locale support" in the pcreapi page). For example, in the "fr\_FR" (French) locale, some character codes greater than 128 are used for accented letters, and these are matched by \w.

In UTF-8 mode, characters with values greater than 128 never match \d, \s, or \w, and always match \D, \S, and \W. This is true even when Unicode character property support is available.

## [Simple assertions](#regular-expression-syntax-and-semantics-simple-assertions)

The fourth use of backslash is for certain simple assertions. An assertion specifies a condition that has to be met at a particular point in a match, without consuming any characters from the subject string. The use of subpatterns for more complicated assertions is described below. The backslashed assertions are:

| assertion | meaning |
| --- | --- |
| \b | matches at a word boundary |
| \B | matches when not at a word boundary |
| \A | matches at start of subject |
| \Z | matches at end of subject or before newline at end |
| \z | matches at end of subject |
| \G | matches at first matching position in subject |

These assertions may not appear in character classes (but note that \b has a different meaning, namely the backspace character, inside a character class).

A word boundary is a position in the subject string where the current character and the previous character do not both match \w or \W (i.e. one matches \w and the other matches \W), or the start or end of the string if the first or last character matches \w, respectively.

The \A, \Z, and \z assertions differ from the traditional circumflex and dollar in that they only ever match at the very start and end of the subject string, whatever options are set. The difference between \Z and \z is that \Z matches before a newline that is the last character of the string as well as at the end of the string, whereas \z matches only at the end.

## Examples

```nim
  r"\S"  # matches any character that is not whitespace
```

```nim
import std/re
## Unless specified otherwise, `start` parameter in each proc indicates
## where the scan starts, but outputs are relative to the start of the input
## string, not to `start`:
doAssert find("uxabc", re"(?<=x|y)ab", start = 1) == 2 # lookbehind assertion
doAssert find("uxabc", re"ab", start = 3) == -1 # we're past `start` => not found
doAssert not match("xabc", re"^abc$", start = 1)
  # can't match start of string since we're starting at 1
```

```nim
doAssert find("abcdefg", re"cde") == 2
doAssert find("abcdefg", re"abc") == 0
doAssert find("abcdefg", re"zz") == -1 # not found
doAssert find("abcdefg", re"cde", start = 2) == 2 # still 2
doAssert find("abcdefg", re"cde", start = 3) == -1 # we're past the start position
doAssert find("xabc", re"(?<=x|y)abc", start = 1) == 1
  # lookbehind assertion `(?<=x|y)` can look behind `start`
```

```nim
var matches = newSeq[tuple[first, last: int]](1)
let (first, last) = findBounds("Hello World", re"(\w+)", matches)
doAssert first == 0
doAssert last == 4
doAssert matches[0] == (0, 4)
```

```nim
var matches = newSeq[string](1)
let (first, last) = findBounds("Hello World", re"(W\w+)", matches)
doAssert first == 6
doAssert last == 10
doAssert matches[0] == "World"
```

```nim
assert findBounds("01234abc89", re"abc") == (5,7)
```

```nim
import std/sequtils
var matches: array[2, string]
if match("abcdefg", re"c(d)ef(g)", matches, 2):
  doAssert toSeq(matches) == @["d", "g"]
```

```nim
doAssert matchLen("abcdefg", re"cde", 2) == 3
doAssert matchLen("abcdefg", re"abcde") == 5
doAssert matchLen("abcdefg", re"cde") == -1
```

```nim
doAssert "var1=key; var2=key2".replace(re"(\w+)=(\w+)") == "; "
doAssert "var1=key; var2=key2".replace(re"(\w+)=(\w+)", "?") == "?; ?"
```

```nim
doAssert "var1=key; var2=key2".replacef(re"(\w+)=(\w+)", "$1<-$2$2") ==
  "var1<-keykey; var2<-key2key2"
```

```nim
import std/sequtils
doAssert toSeq(split("00232this02939is39an22example111", re"\d+")) ==
  @["", "this", "is", "an", "example", ""]
```

```nim
proc parse(line: string): string =
  if line =~ re"\s*(\w+)\s*\=\s*(\w+)": # matches a key=value pair:
    result = $(matches[0], matches[1])
  elif line =~ re"\s*(\#.*)": # matches a comment
    # note that the implicit `matches` array is different from 1st branch
    result = $(matches[0],)
  else: raiseAssert "unreachable"
  doAssert not declared(matches)
doAssert parse("NAME = LENA") == """("NAME", "LENA")"""
doAssert parse("   # comment ... ") == """("# comment ... ",)"""
```

## Const

### MaxReBufSize

[ref: #symbol-maxrebufsize]

```nim
MaxReBufSize = 2147483647'i32
```

Maximum PCRE (API 1) buffer start/size equal to high(cint), which even for 64-bit systems can be either 231-1 or 263-1.

### MaxSubpatterns

[ref: #symbol-maxsubpatterns]

```nim
MaxSubpatterns = 20
```

defines the maximum number of subpatterns that can be captured. This limit still exists for replacef and parallelReplace.

## Iterator

### findAll

[ref: #symbol-findall]

Yields all matching *substrings* of s that match pattern.

**Input:**
- `s: string`
- `pattern: Regex`
- `start:  = 0`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Yields all matching *substrings* of s that match pattern.

Note that since this is an iterator you should not modify the string you are iterating over: bad things could happen.

### findAll

[ref: #symbol-findall]

Yields all matching substrings of s that match pattern.

**Input:**
- `buf: cstring`
- `pattern: Regex`
- `start:  = 0`
- `bufSize: int`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Yields all matching substrings of s that match pattern.

Note that since this is an iterator you should not modify the string you are iterating over: bad things could happen.

### split

[ref: #symbol-split]

Splits the string s into substrings.

**Input:**
- `s: string`
- `sep: Regex`
- `maxsplit:  = -1`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s into substrings.

Substrings are separated by the regular expression sep (and the portion matched by sep is not returned).

## Proc

### contains

[ref: #symbol-contains]

**Input:**
- `s: string`
- `pattern: Regex`
- `start:  = 0`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

same as find(s, pattern, start) >= 0

### contains

[ref: #symbol-contains]

same as find(s, pattern, matches, start) >= 0

**Input:**
- `s: string`
- `pattern: Regex`
- `matches: var openArray[string]`
- `start:  = 0`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

same as find(s, pattern, matches, start) >= 0

**Note:**
The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### endsWith

[ref: #symbol-endswith]

**Input:**
- `s: string`
- `suffix: Regex`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns true if s ends with the pattern suffix

### escapeRe

[ref: #symbol-escapere]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

escapes s so that it is matched verbatim when used as a regular expression.

### find

[ref: #symbol-find]

returns the starting position of pattern in buf and the captured substrings in the array matches. If it does not match, nothing is written into matches and -1 is returned. buf has length bufSize (not necessarily '\0' terminated).

**Input:**
- `buf: cstring`
- `pattern: Regex`
- `matches: var openArray[string]`
- `start:  = 0`
- `bufSize: int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the starting position of pattern in buf and the captured substrings in the array matches. If it does not match, nothing is written into matches and -1 is returned. buf has length bufSize (not necessarily '\0' terminated).

**Note:**
The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### find

[ref: #symbol-find]

returns the starting position of pattern in s and the captured substrings in the array matches. If it does not match, nothing is written into matches and -1 is returned.

**Input:**
- `s: string`
- `pattern: Regex`
- `matches: var openArray[string]`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the starting position of pattern in s and the captured substrings in the array matches. If it does not match, nothing is written into matches and -1 is returned.

**Note:**
The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### find

[ref: #symbol-find]

**Input:**
- `buf: cstring`
- `pattern: Regex`
- `start:  = 0`
- `bufSize: int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the starting position of pattern in buf, where buf has length bufSize (not necessarily '\0' terminated). If it does not match, -1 is returned.

### find

[ref: #symbol-find]

**Input:**
- `s: string`
- `pattern: Regex`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the starting position of pattern in s. If it does not match, -1 is returned. We start the scan at start.

### findAll

[ref: #symbol-findall]

**Input:**
- `s: string`
- `pattern: Regex`
- `start:  = 0`

**Output:** `seq[string]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns all matching substrings of s that match pattern. If it does not match, @[] is returned.

### findBounds

[ref: #symbol-findbounds]

returns the starting position and end position of pattern in buf (where buf has length bufSize and is not necessarily '\0' terminated), and the captured substrings in the array matches. If it does not match, nothing is written into matches and (-1,0) is returned.

**Input:**
- `buf: cstring`
- `pattern: Regex`
- `matches: var openArray[string]`
- `start:  = 0`
- `bufSize: int`

**Output:** `tuple[first, last: int]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the starting position and end position of pattern in buf (where buf has length bufSize and is not necessarily '\0' terminated), and the captured substrings in the array matches. If it does not match, nothing is written into matches and (-1,0) is returned.

Note: The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### findBounds

[ref: #symbol-findbounds]

returns the starting position and end position of pattern in s and the captured substrings in the array matches. If it does not match, nothing is written into matches and (-1,0) is returned.

**Input:**
- `s: string`
- `pattern: Regex`
- `matches: var openArray[string]`
- `start:  = 0`

**Output:** `tuple[first, last: int]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the starting position and end position of pattern in s and the captured substrings in the array matches. If it does not match, nothing is written into matches and (-1,0) is returned.

**Note:**
The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### findBounds

[ref: #symbol-findbounds]

returns the starting position and end position of pattern in buf (where buf has length bufSize and is not necessarily '\0' terminated), and the captured substrings in the array matches. If it does not match, nothing is written into matches and (-1,0) is returned.

**Input:**
- `buf: cstring`
- `pattern: Regex`
- `matches: var openArray[tuple[first, last: int]]`
- `start:  = 0`
- `bufSize: int`

**Output:** `tuple[first, last: int]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the starting position and end position of pattern in buf (where buf has length bufSize and is not necessarily '\0' terminated), and the captured substrings in the array matches. If it does not match, nothing is written into matches and (-1,0) is returned.

**Note:**
The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### findBounds

[ref: #symbol-findbounds]

returns the starting position and end position of pattern in s and the captured substrings in the array matches. If it does not match, nothing is written into matches and (-1,0) is returned.

**Input:**
- `s: string`
- `pattern: Regex`
- `matches: var openArray[tuple[first, last: int]]`
- `start:  = 0`

**Output:** `tuple[first, last: int]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the starting position and end position of pattern in s and the captured substrings in the array matches. If it does not match, nothing is written into matches and (-1,0) is returned.

**Note:**
The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### findBounds

[ref: #symbol-findbounds]

**Input:**
- `buf: cstring`
- `pattern: Regex`
- `start:  = 0`
- `bufSize: int`

**Output:** `tuple[first, last: int]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the first and last position of pattern in buf, where buf has length bufSize (not necessarily '\0' terminated). If it does not match, (-1,0) is returned.

### findBounds

[ref: #symbol-findbounds]

returns the first and last position of pattern in s. If it does not match, (-1,0) is returned.

**Input:**
- `s: string`
- `pattern: Regex`
- `start:  = 0`

**Output:** `tuple[first, last: int]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the first and last position of pattern in s. If it does not match, (-1,0) is returned.

Note: there is a speed improvement if the matches do not need to be captured.

### match

[ref: #symbol-match]

**Input:**
- `s: string`
- `pattern: Regex`
- `start:  = 0`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns true if s[start..] matches the pattern.

### match

[ref: #symbol-match]

returns true if s[start..] matches the pattern and the captured substrings in the array matches. If it does not match, nothing is written into matches and false is returned.

**Input:**
- `s: string`
- `pattern: Regex`
- `matches: var openArray[string]`
- `start:  = 0`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns true if s[start..] matches the pattern and the captured substrings in the array matches. If it does not match, nothing is written into matches and false is returned.

**Note:**
The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### match

[ref: #symbol-match]

returns true if buf[start..<bufSize] matches the pattern and the captured substrings in the array matches. If it does not match, nothing is written into matches and false is returned. buf has length bufSize (not necessarily '\0' terminated).

**Input:**
- `buf: cstring`
- `pattern: Regex`
- `matches: var openArray[string]`
- `start:  = 0`
- `bufSize: int`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns true if buf[start..<bufSize] matches the pattern and the captured substrings in the array matches. If it does not match, nothing is written into matches and false is returned. buf has length bufSize (not necessarily '\0' terminated).

**Note:**
The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### matchLen

[ref: #symbol-matchlen]

the same as match, but it returns the length of the match, if there is no match, -1 is returned. Note that a match length of zero can happen.

**Input:**
- `s: string`
- `pattern: Regex`
- `matches: var openArray[string]`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

the same as match, but it returns the length of the match, if there is no match, -1 is returned. Note that a match length of zero can happen.

**Note:**
The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### matchLen

[ref: #symbol-matchlen]

the same as match, but it returns the length of the match, if there is no match, -1 is returned. Note that a match length of zero can happen.

**Input:**
- `buf: cstring`
- `pattern: Regex`
- `matches: var openArray[string]`
- `start:  = 0`
- `bufSize: int`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

the same as match, but it returns the length of the match, if there is no match, -1 is returned. Note that a match length of zero can happen.

**Note:**
The memory for matches needs to be allocated before this function is called, otherwise it will just remain empty.

### matchLen

[ref: #symbol-matchlen]

**Input:**
- `s: string`
- `pattern: Regex`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

the same as match, but it returns the length of the match, if there is no match, -1 is returned. Note that a match length of zero can happen.

### matchLen

[ref: #symbol-matchlen]

**Input:**
- `buf: cstring`
- `pattern: Regex`
- `start:  = 0`
- `bufSize: int`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

the same as match, but it returns the length of the match, if there is no match, -1 is returned. Note that a match length of zero can happen.

### multiReplace

[ref: #symbol-multireplace]

**Input:**
- `s: string`
- `subs: openArray[tuple[pattern: Regex, repl: string]]`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Returns a modified copy of s with the substitutions in subs applied in parallel.

### re

[ref: #symbol-re]

Constructor of regular expressions.

**Input:**
- `s: string`
- `flags:  = {reStudy}`

**Output:** `Regex`
**Pragmas:** `raises: [RegexError]`, `tags: []`, `forbids: []`

**Effects:** `raises: RegexError`, `tags: `, `forbids: `

Constructor of regular expressions.

Note that Nim's extended raw string literals support the syntax re"[abc]" as a short form for re(r"[abc]"). Also note that since this compiles the regular expression, which is expensive, you should avoid putting it directly in the arguments of the functions like the examples show below if you plan to use it a lot of times, as this will hurt performance immensely. (e.g. outside a loop, ...)

### replace

[ref: #symbol-replace]

**Input:**
- `s: string`
- `sub: Regex`
- `by:  = ""`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Replaces sub in s by the string by. Captures cannot be accessed in by.

### replacef

[ref: #symbol-replacef]

**Input:**
- `s: string`
- `sub: Regex`
- `by: string`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Replaces sub in s by the string by. Captures can be accessed in by with the notation $i and $# (see strutils.`%`).

### rex

[ref: #symbol-rex]

Constructor for extended regular expressions.

**Input:**
- `s: string`
- `flags:  = {reStudy, reExtended}`

**Output:** `Regex`
**Pragmas:** `raises: [RegexError]`, `tags: []`, `forbids: []`

**Effects:** `raises: RegexError`, `tags: `, `forbids: `

Constructor for extended regular expressions.

The extended means that comments starting with # and whitespace are ignored.

### split

[ref: #symbol-split]

Splits the string s into a seq of substrings.

**Input:**
- `s: string`
- `sep: Regex`
- `maxsplit:  = -1`

**Output:** `seq[string]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string s into a seq of substrings.

The portion matched by sep is not returned.

### startsWith

[ref: #symbol-startswith]

**Input:**
- `s: string`
- `prefix: Regex`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns true if s starts with the pattern prefix

### transformFile

[ref: #symbol-transformfile]

**Input:**
- `infile: string`
- `outfile: string`
- `subs: openArray[tuple[pattern: Regex, repl: string]]`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, ValueError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, ValueError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

reads in the file infile, performs a parallel replacement (calls parallelReplace) and writes back to outfile. Raises IOError if an error occurs. This is supposed to be used for quick scripting.

## Template

### `=~`

[ref: #symbol-]

**Input:**
- `s: string`
- `pattern: Regex`

**Output:** `untyped`
This calls match with an implicit declared matches array that can be used in the scope of the =~ call:

## Type

### Regex

[ref: #symbol-regex]

```nim
Regex = ref RegexDesc
```

a compiled regular expression

### RegexError

[ref: #symbol-regexerror]

```nim
RegexError = object of ValueError
```

is raised if the pattern is no valid regular expression.

### RegexFlag

[ref: #symbol-regexflag]

```nim
RegexFlag = enum
  reIgnoreCase = 0,         ## do caseless matching
  reMultiLine = 1,          ## `^` and `$` match newlines within data
  reDotAll = 2,             ## `.` matches anything including NL
  reExtended = 3,           ## ignore whitespace and `#` comments
  reStudy = 4                ## study the expression (may be omitted if the
                             ## expression will be used only once)
```

options for regular expressions
