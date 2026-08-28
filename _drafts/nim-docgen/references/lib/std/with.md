---
source_hash: 7e90bc5db403a1be
source_path: lib/std/with.nim
---

# with

[ref: #module-with]

This module implements the with macro for easy function chaining. See <https://github.com/nim-lang/RFCs/issues/193> and <https://github.com/nim-lang/RFCs/issues/192> for details leading to this particular design.

**Since:** version 1.2.

## Examples

```nim
var x = "yay"
with x:
  add "abc"
  add "efg"
doAssert x == "yayabcefg"

var a = 44
with a:
  += 4
  -= 5
doAssert a == 43

# Nesting works for object types too!
var foo = (bar: 1, qux: (baz: 2))
with foo:
  bar = 2
  with qux:
    baz = 3
doAssert foo.bar == 2
doAssert foo.qux.baz == 3
```

## Macro

### with

[ref: #symbol-with]

This macro provides chaining of function calls. It does so by patching every call in calls to use arg as the first argument.

**Input:**
- `arg: typed`
- `calls: varargs[untyped]`

**Output:** `untyped`
This macro provides chaining of function calls. It does so by patching every call in calls to use arg as the first argument.

**Caution:**
This evaluates arg multiple times!
