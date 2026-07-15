---
source_hash: acdffbea65313099
source_path: lib/pure/collections/rtarrays.nim
---

# rtarrays

[ref: #module-rtarrays]

Module that implements a fixed length array whose size is determined at runtime. Note: This is not ready for other people to use!

Unstable API.

## Proc

### getRawData

[ref: #symbol-getrawdata]

**Input:**
- `x: var RtArray[T]`

**Output:** `ptr UncheckedArray[T]`
**Generic parameters:** `T`

### initRtArray

[ref: #symbol-initrtarray]

**Input:**
- `len: Natural`

**Output:** `RtArray[T]`
**Generic parameters:** `T`

## Type

### RtArray

[ref: #symbol-rtarray]

```nim
RtArray[T] = object
```
