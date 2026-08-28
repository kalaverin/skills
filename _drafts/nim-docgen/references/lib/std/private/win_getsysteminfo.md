---
source_hash: ba2943503d50d56a
source_path: lib/std/private/win_getsysteminfo.nim
---

# win_getsysteminfo

[ref: #module-win_getsysteminfo]

## Proc

### getSystemInfo

[ref: #symbol-getsysteminfo]

**Input:**
- `lpSystemInfo: ptr SystemInfo`

**Output:** *(none)*
**Pragmas:** `stdcall`, `dynlib: "kernel32"`, `importc: "GetSystemInfo"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### SystemInfo

[ref: #symbol-systeminfo]

```nim
SystemInfo = object
  dwNumberOfProcessors*: uint32
  dwAllocationGranularity*: uint32
```
