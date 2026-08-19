---
source_hash: eb86ceb47295aa6e
source_path: lib/std/strbasics.nim
---

# strbasics

[ref: #module-strbasics]

This module provides some high performance string operations.

Experimental API, subject to change.

## Examples

```nim
import std/sugar

var a = "Hello, Nim!"
doAssert a.dup(setSlice(7 .. 9)) == "Nim"
doAssert a.dup(setSlice(0 .. 0)) == "H"
doAssert a.dup(setSlice(0 .. 1)) == "He"
doAssert a.dup(setSlice(0 .. 10)) == a
doAssert a.dup(setSlice(1 .. 0)).len == 0
doAssert a.dup(setSlice(20 .. -1)).len == 0


doAssertRaises(AssertionDefect):
  discard a.dup(setSlice(-1 .. 1))

doAssertRaises(AssertionDefect):
  discard a.dup(setSlice(1 .. 11))
```

```nim
var a = "  vhellov   "
strip(a)
assert a == "vhellov"

a = "  vhellov   "
a.strip(leading = false)
assert a == "  vhellov"

a = "  vhellov   "
a.strip(trailing = false)
assert a == "vhellov   "

var c = "blaXbla"
c.strip(chars = {'b', 'a'})
assert c == "laXbl"
c = "blaXbla"
c.strip(chars = {'b', 'a', 'l'})
assert c == "X"
```

## Proc

### add

[ref: #symbol-add]

**Input:**
- `x: var string`
- `y: openArray[char]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenates x and y in place. y must not overlap with x to allow future memcpy optimizations.

### setSlice

[ref: #symbol-setslice]

**Input:**
- `s: var string`
- `slice: Slice[int]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Inplace version of substr.

### strip

[ref: #symbol-strip]

Inplace version of strip. Strips leading or trailing chars (default: whitespace characters).

**Input:**
- `a: var string`
- `leading:  = true`
- `trailing:  = true`
- `chars: set[char] = whitespaces`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Inplace version of strip. Strips leading or trailing chars (default: whitespace characters).

If leading is true (default), leading chars are stripped. If trailing is true (default), trailing chars are stripped. If both are false, the string is unchanged.
