---
source_hash: d071b96af0fcd642
source_path: lib/std/stackframes.nim
---

# stackframes

[ref: #module-stackframes]

## Template

### getPFrame

[ref: #symbol-getpframe]

**Input:**
- *(none)*

**Output:** `PFrame`
avoids a function call (unlike getFrame())

### procName

[ref: #symbol-procname]

**Input:**
- *(none)*

**Output:** `string`
returns current C/C++ function name

### setFrameMsg

[ref: #symbol-setframemsg]

**Input:**
- `msg: string`
- `prefix:  = " "`

**Output:** *(none)*
attach a msg to current PFrame. This can be called multiple times in a given PFrame. Noop unless passing --stacktraceMsgs and --stacktrace
