---
source_hash: 1764e576ea290ca2
source_path: lib/pure/prelude.nim
---

# prelude

[ref: #module-prelude]

This is an include file that simply imports common modules for your convenience.

## Examples

```nim
import std/prelude
include std/prelude
  # same as:
  # import std/[os, strutils, times, parseutils, hashes, tables, sets, sequtils, parseopt, strformat]
let x = 1
assert "foo $# $#" % [$x, "bar"] == "foo 1 bar"
assert toSeq(1..3) == @[1, 2, 3]
when not defined(js) or defined(nodejs):
  assert getCurrentDir().len > 0
  assert ($now()).startsWith "20"
```
