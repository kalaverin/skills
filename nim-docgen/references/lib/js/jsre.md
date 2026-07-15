---
source_hash: 649036281e4d4cc5
source_path: lib/js/jsre.nim
---

# jsre

[ref: #module-jsre]

Regular Expressions for the JavaScript target.

* <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions>

## Examples

```nim
import std/jsre
let jsregex: RegExp = newRegExp(r"\s+", r"i")
jsregex.compile(r"\w+", r"i")
assert "nim javascript".contains jsregex
assert jsregex.exec(r"nim javascript") == @["nim".cstring]
assert jsregex.toCstring() == r"/\w+/i"
jsregex.compile(r"[0-9]", r"i")
assert "0123456789abcd".contains jsregex
assert $jsregex == "/[0-9]/i"
jsregex.compile(r"abc", r"i")
assert "abcd".startsWith jsregex
assert "dabc".endsWith jsregex
jsregex.compile(r"\d", r"i")
assert "do1ne".split(jsregex) == @["do".cstring, "ne".cstring]
jsregex.compile(r"[lw]", r"i")
assert "hello world".replace(jsregex,"X") == "heXlo world"
jsregex.compile(r"([a-z])\1*", r"g")
assert "abbcccdddd".replace(jsregex, proc (m: varargs[cstring]): cstring = ($m[0] & $(m.len)).cstring) == "a1b2c3d4"
let digitsRegex: RegExp = newRegExp(r"\d")
assert "foo".match(digitsRegex) == @[]
```

```nim
let jsregex: RegExp = newRegExp(r"bc$", r"i")
assert jsregex in r"abc"
assert jsregex notin r"abcd"
assert "xabc".contains jsregex
```

```nim
let jsregex: RegExp = newRegExp(r"bcd", r"i")
assert "abcd".endsWith jsregex
```

```nim
let jsregex: RegExp = newRegExp(r"abc", r"i")
assert "abcd".startsWith jsregex
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `self: RegExp`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### compile

[ref: #symbol-compile]

**Input:**
- `self: RegExp`
- `pattern: cstring`
- `flags: cstring`

**Output:** *(none)*
**Pragmas:** `importjs: "#.compile(@)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Recompiles a regular expression during execution of a script.

### contains

[ref: #symbol-contains]

**Input:**
- `pattern: cstring`
- `self: RegExp`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Tests for a substring match in its string parameter.

### endsWith

[ref: #symbol-endswith]

**Input:**
- `pattern: cstring`
- `self: RegExp`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Tests if string ends with given RegExp

### exec

[ref: #symbol-exec]

**Input:**
- `self: RegExp`
- `pattern: cstring`

**Output:** `seq[cstring]`
**Pragmas:** `importjs: "(#.exec(#) || [])"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Executes a search for a match in its string parameter.

### match

[ref: #symbol-match]

**Input:**
- `pattern: cstring`
- `self: RegExp`

**Output:** `seq[cstring]`
**Pragmas:** `importjs: "(#.match(#) || [])"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns an array of matches of a RegExp against given string

### newRegExp

[ref: #symbol-newregexp]

**Input:**
- `pattern: cstring`
- `flags: cstring`

**Output:** `RegExp`
**Pragmas:** `importjs: "new RegExp(@)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new RegExp object.

### newRegExp

[ref: #symbol-newregexp]

**Input:**
- `pattern: cstring`

**Output:** `RegExp`
**Pragmas:** `importjs: "new RegExp(@)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### replace

[ref: #symbol-replace]

**Input:**
- `pattern: cstring`
- `self: RegExp`
- `replacement: cstring`

**Output:** `cstring`
**Pragmas:** `importjs: "#.replace(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a new string with some or all matches of a pattern replaced by given replacement

### replace

[ref: #symbol-replace]

**Input:**
- `pattern: cstring`
- `self: RegExp`
- `cb: proc (args: varargs[cstring]): cstring`

**Output:** `cstring`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a new string with some or all matches of a pattern replaced by given callback function

### split

[ref: #symbol-split]

**Input:**
- `pattern: cstring`
- `self: RegExp`

**Output:** `seq[cstring]`
**Pragmas:** `importjs: "(#.split(#) || [])"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Divides a string into an ordered list of substrings and returns the array

### startsWith

[ref: #symbol-startswith]

**Input:**
- `pattern: cstring`
- `self: RegExp`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Tests if string starts with given RegExp

### toCstring

[ref: #symbol-tocstring]

**Input:**
- `self: RegExp`

**Output:** `cstring`
**Pragmas:** `importjs: "#.toString()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a string representing the RegExp object.

## Type

### RegExp

[ref: #symbol-regexp]

```nim
RegExp = ref object of JsRoot
  flags*: cstring            ## cstring that contains the flags of the RegExp object.
  dotAll*: bool              ## Whether `.` matches newlines or not.
  global*: bool              ## Whether to test against all possible matches in a string, or only against the first.
  ignoreCase*: bool          ## Whether to ignore case while attempting a match in a string.
  multiline*: bool           ## Whether to search in strings across multiple lines.
  source*: cstring           ## The text of the pattern.
  sticky*: bool              ## Whether the search is sticky.
  unicode*: bool             ## Whether Unicode features are enabled.
  lastIndex*: cint           ## Index at which to start the next match (read/write property).
  input*: cstring            ## Read-only and modified on successful match.
  lastMatch*: cstring        ## Ditto.
  lastParen*: cstring        ## Ditto.
  leftContext*: cstring      ## Ditto.
  rightContext*: cstring     ## Ditto.
  hasIndices*: bool          ## https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp/hasIndices
```

Regular Expressions for JavaScript target. See <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/RegExp>
