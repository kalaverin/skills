---
source_hash: dd865d58f2a6671a
source_path: lib/std/decls.nim
---

# decls

[ref: #module-decls]

This module implements syntax sugar for some declarations.

## Examples

```nim
var s = @[10, 11, 12]
var a {.byaddr.} = s[0]
a += 100
assert s == @[110, 11, 12]
assert a is int
var b {.byaddr.}: int = s[0]
assert a.addr == b.addr
```

## Macro

### byaddr

[ref: #symbol-byaddr]

Allows a syntax for l-value references, being an exact analog to auto& a = ex; in C++.

**Input:**
- `sect: `

**Output:** *(none)*
Allows a syntax for l-value references, being an exact analog to auto& a = ex; in C++.

**Warning:**
This makes use of 2 experimental features, namely nullary templates instantiated as symbols and variable macro pragmas. For this reason, its behavior is not stable. The current implementation allows redefinition, but this is not an intended consequence.
