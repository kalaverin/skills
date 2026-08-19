---
source_hash: a14267597984ab7d
source_path: lib/std/genasts.nim
---

# genasts

[ref: #module-genasts]

This module implements AST generation using captured variables for macros.

## Examples

```nim
# This example shows how one could write a simplified version of `unittest.check`.
import std/[macros, strutils]
macro check2(cond: bool): untyped =
  assert cond.kind == nnkInfix, "$# not implemented" % $cond.kind
  result = genAst(cond, s = repr(cond), lhs = cond[1], rhs = cond[2]):
    # each local symbol we access must be explicitly captured
    if not cond:
      raiseAssert "'$#'' failed: lhs: '$#', rhs: '$#'" % [s, $lhs, $rhs]
let a = 3
check2 a*2 == a+3
if false: check2 a*2 < a+1 # would error with: 'a * 2 < a + 1'' failed: lhs: '6', rhs: '4'
```

```nim
# This example goes in more details about the capture semantics.
macro fun(a: string, b: static bool): untyped =
  let c = 'z'
  var d = 11 # implicitly {.gensym.} and needs to be captured for use in `genAst`.
  proc localFun(): auto = 12 # implicitly {.inject.}, doesn't need to be captured.
  genAst(a, b, c = true):
    # `a`, `b` are captured explicitly, `c` is a local definition masking `c = 'z'`.
    const b2 = b # macro static param `b` is forwarded here as a static param.
    # `echo d` would give: `var not init` because `d` is not captured.
    (a & a, b, c, localFun()) # localFun can be called without capture.
assert fun("ab", false) == ("abab", false, true, 12)
```

## Macro

### genAstOpt

[ref: #symbol-genastopt]

**Input:**
- `options: static set[GenAstOpt]`
- `args: varargs[untyped]`

**Output:** `untyped`
**Generic parameters:** `options:type`

Accepts a list of captured variables a=b or a and a block and returns the AST that represents it. Local {.inject.} symbols (e.g. procs) are captured unless kDirtyTemplate in options.

## Template

### genAst

[ref: #symbol-genast]

**Input:**
- `args: varargs[untyped]`

**Output:** `untyped`
Convenience wrapper around genAstOpt.

## Type

### GenAstOpt

[ref: #symbol-genastopt]

```nim
GenAstOpt = enum
  kDirtyTemplate, kNoNewLit
```
