---
source_hash: b90d8688e711e070
source_path: lib/std/vmutils.nim
---

# vmutils

[ref: #module-vmutils]

Experimental API, subject to change.

## Examples

```nim
static: vmTrace(true)
proc fn =
  var a = 1
  vmTrace(false)
static: fn()
```

## Proc

### vmTrace

[ref: #symbol-vmtrace]

**Input:**
- `on: bool`

**Output:** *(none)*
**Pragmas:** `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `
