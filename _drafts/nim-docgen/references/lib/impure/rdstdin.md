---
source_hash: 184a78537612730c
source_path: lib/impure/rdstdin.nim
---

# rdstdin

[ref: #module-rdstdin]

This module contains code for reading from stdin. On UNIX the linenoise library is wrapped and set up to provide default key bindings (e.g. you can navigate with the arrow keys). On Windows system.readLine is used. This suffices because Windows' console already provides the wanted functionality.

## Examples

```nim
import std/rdstdin
echo readLineFromStdin("Is Nim awesome? (Y/n): ")
var line: string
while true:
  let ok = readLineFromStdin("How are you? ", line)
  if not ok: break # ctrl-C or ctrl-D will cause a break
  if line.len > 0: echo line
echo "exiting"
```

## Proc

### readLineFromStdin

[ref: #symbol-readlinefromstdin]

**Input:**
- `prompt: string`
- `line: var string`

**Output:** `bool`
**Pragmas:** `tags: [ReadIOEffect, WriteIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect, WriteIOEffect`, `raises: `, `forbids: `

### readLineFromStdin

[ref: #symbol-readlinefromstdin]

**Input:**
- `prompt: string`

**Output:** `string`
**Pragmas:** `inline`, `raises: [IOError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `
