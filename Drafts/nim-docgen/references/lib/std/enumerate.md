---
source_hash: 1a8303c0dc422363
source_path: lib/std/enumerate.nim
---

# enumerate

[ref: #module-enumerate]

This module implements enumerate syntactic sugar based on Nim's macro system.

## Examples

```nim
let a = [10, 20, 30]
var b: seq[(int, int)] = @[]
for i, x in enumerate(a):
  b.add((i, x))
assert b == @[(0, 10), (1, 20), (2, 30)]

let c = "abcd"
var d: seq[(int, char)]
for (i, x) in enumerate(97, c):
  d.add((i, x))
assert d == @[(97, 'a'), (98, 'b'), (99, 'c'), (100, 'd')]
```

## Macro

### enumerate

[ref: #symbol-enumerate]

Enumerating iterator for collections.

**Input:**
- `x: ForLoopStmt`

**Output:** `untyped`
Enumerating iterator for collections.

It yields (count, value) tuples (which must be immediately unpacked). The default starting count 0 can be manually overridden if needed.
