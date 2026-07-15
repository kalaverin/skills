---
source_hash: 1acf620426767cf4
source_path: lib/pure/sugar.nim
---

# sugar

[ref: #module-sugar]

This module implements nice syntactic sugar based on Nim's macro system.

## Examples

```nim
proc passTwoAndTwo(f: (int, int) -> int): int = f(2, 2)
# is the same as:
# proc passTwoAndTwo(f: proc (x, y: int): int): int = f(2, 2)

assert passTwoAndTwo((x, y) => x + y) == 4

proc passOne(f: (int {.noSideEffect.} -> int)): int = f(1)
# is the same as:
# proc passOne(f: proc (x: int): int {.noSideEffect.}): int = f(1)

assert passOne(x {.noSideEffect.} => x + 1) == 2
```

```nim
proc passTwoAndTwo(f: (int, int) -> int): int = f(2, 2)

assert passTwoAndTwo((x, y) => x + y) == 4

type
  Bot = object
    call: (string {.noSideEffect.} -> string)

var myBot = Bot()

myBot.call = (name: string) {.noSideEffect.} => "Hello " & name & ", I'm a bot."
assert myBot.call("John") == "Hello John, I'm a bot."

let f = () => (discard) # simplest proc that returns void
f()
```

```nim
import std/strformat

var myClosure: () -> string
for i in 5..7:
  for j in 7..9:
    if i * j == 42:
      capture i, j:
        myClosure = () => fmt"{i} * {j} = 42"
assert myClosure() == "6 * 7 = 42"
```

```nim
import std/[sets, tables]
let data = @["bird", "word"]

# seq:
let k = collect:
  for i, d in data.pairs:
    if i mod 2 == 0: d
assert k == @["bird"]

## HashSet:
let n = collect:
  for d in data.items: {d}
assert n == data.toHashSet

## Table:
let m = collect:
  for i, d in data.pairs: {i: d}
assert m == {0: "bird", 1: "word"}.toTable
```

```nim
import std/[sets, tables]

let data = @["bird", "word"]

## seq:
let k = collect(newSeq):
  for i, d in data.pairs:
    if i mod 2 == 0: d
assert k == @["bird"]

## seq with initialSize:
let x = collect(newSeqOfCap(4)):
  for i, d in data.pairs:
    if i mod 2 == 0: d
assert x == @["bird"]

## HashSet:
let y = collect(initHashSet()):
  for d in data.items: {d}
assert y == data.toHashSet

## Table:
let z = collect(initTable(2)):
  for i, d in data.pairs: {i: d}
assert z == {0: "bird", 1: "word"}.toTable
```

```nim
let
  x = 10
  y = 20
dump(x + y) # prints: `x + y = 30`
```

```nim
const a = 1
let x = 10
assert dumpToString(a + 2) == "a + 2: 3 = 3"
assert dumpToString(a + x) == "a + x: 1 + x = 11"
template square(x): untyped = x * x
assert dumpToString(square(x)) == "square(x): x * x = 100"
assert not compiles dumpToString(1 + nonexistent)
import std/strutils
assert "failedAssertImpl" in dumpToString(assert true) # example with a statement
```

```nim
import std/algorithm

let a = @[1, 2, 3, 4, 5, 6, 7, 8, 9]
assert a.dup(sort) == sorted(a)

# Chaining:
var aCopy = a
aCopy.insert(10)
assert a.dup(insert(10), sort) == sorted(aCopy)

let s1 = "abc"
let s2 = "xyz"
assert s1 & s2 == s1.dup(&= s2)

# An underscore (_) can be used to denote the place of the argument you're passing:
assert "".dup(addQuoted(_, "foo")) == "\"foo\""
# but `_` is optional here since the substitution is in 1st position:
assert "".dup(addQuoted("foo")) == "\"foo\""

proc makePalindrome(s: var string) =
  for i in countdown(s.len-2, 0):
    s.add(s[i])

let c = "xyz"

# chaining:
let d = dup c:
  makePalindrome # xyzyx
  sort(_, SortOrder.Descending) # zyyxx
  makePalindrome # zyyxxxyyz
assert d == "zyyxxxyyz"
```

## Macro

### `-&gt;`

[ref: #symbol-gt]

Syntax sugar for procedure types. It also supports pragmas.

**Input:**
- `p: untyped`
- `b: untyped`

**Output:** `untyped`
Syntax sugar for procedure types. It also supports pragmas.

**Warning:**
Semicolons can not be used to separate procedure arguments.

### `=&gt;`

[ref: #symbol-gt]

Syntax sugar for anonymous procedures. It also supports pragmas.

**Input:**
- `p: untyped`
- `b: untyped`

**Output:** `untyped`
Syntax sugar for anonymous procedures. It also supports pragmas.

**Warning:**
Semicolons can not be used to separate procedure arguments.

### capture

[ref: #symbol-capture]

**Input:**
- `locals: varargs[typed]`
- `body: untyped`

**Output:** `untyped`
Useful when creating a closure in a loop to capture some local loop variables by their current iteration values.

### collect

[ref: #symbol-collect]

Comprehension for seqs/sets/tables.

**Input:**
- `init: untyped`
- `body: untyped`

**Output:** `untyped`
Comprehension for seqs/sets/tables.

The last expression of body has special syntax that specifies the collection's add operation. Use {e} for set's incl, {k: v} for table's []= and e for seq's add.

### collect

[ref: #symbol-collect]

Same as collect but without an init parameter.

**Input:**
- `body: untyped`

**Output:** `untyped`
Same as collect but without an init parameter.

**See also:**

* [sequtils.toSeq proc](sequtils.html#toSeq.t%2Cuntyped)
* [sequtils.mapIt template](sequtils.html#mapIt.t%2Ctyped%2Cuntyped)

### dump

[ref: #symbol-dump]

Dumps the content of an expression, useful for debugging. It accepts any expression and prints a textual representation of the tree representing the expression - as it would appear in source code - together with the value of the expression.

**Input:**
- `x: untyped`

**Output:** `untyped`
Dumps the content of an expression, useful for debugging. It accepts any expression and prints a textual representation of the tree representing the expression - as it would appear in source code - together with the value of the expression.

See also: dumpToString which is more convenient and useful since it expands intermediate templates/macros, returns a string instead of calling echo, and works with statements and expressions.

### dumpToString

[ref: #symbol-dumptostring]

**Input:**
- `x: untyped`

**Output:** `string`
Returns the content of a statement or expression x after semantic analysis, useful for debugging.

### dup

[ref: #symbol-dup]

Turns an in-place algorithm into one that works on a copy and returns this copy, without modifying its input.

**Input:**
- `arg: T`
- `calls: varargs[untyped]`

**Output:** `T`
**Generic parameters:** `T`

Turns an in-place algorithm into one that works on a copy and returns this copy, without modifying its input.

This macro also allows for (otherwise in-place) function chaining.

**Since:** Version 1.2.
