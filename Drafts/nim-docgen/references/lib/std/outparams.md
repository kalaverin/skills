---
source_hash: 345964a2729de890
source_path: lib/std/outparams.nim
---

# outparams

[ref: #module-outparams]

outParamsAt macro for easy writing code that works with both 2.0 and 1.x.

## Examples

```nim
proc p(x: var int) {.outParamsAt: [1].} =
  discard "x is really an 'out int' if the Nim compiler supports 'out' parameters"
```

## Macro

### outParamsAt

[ref: #symbol-outparamsat]

**Input:**
- `positions: static openArray[int]`
- `n: untyped`

**Output:** `untyped`
**Generic parameters:** `positions:type`

Use this macro to annotate out parameters in a portable way.
