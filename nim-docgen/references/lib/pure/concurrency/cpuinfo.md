---
source_hash: bb906e0befae0584
source_path: lib/pure/concurrency/cpuinfo.nim
---

# cpuinfo

[ref: #module-cpuinfo]

This module implements a proc to determine the number of CPUs / cores.

## Examples

```nim
import std/cpuinfo
doAssert countProcessors() > 0
```

## Proc

### countProcessors

[ref: #symbol-countprocessors]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "ncpi$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of the processors/cores the machine has. Returns 0 if it cannot be detected.
