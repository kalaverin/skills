---
source_hash: 98d663ac5164f65b
source_path: lib/std/private/miscdollars.nim
---

# miscdollars

[ref: #module-miscdollars]

## Template

### toLocation

[ref: #symbol-tolocation]

**Input:**
- `result: var string`
- `file: string | cstring`
- `line: int`
- `col: int`

**Output:** *(none)*
**Generic parameters:** `file:type`

avoids spurious allocations

### tupleObjectDollar

[ref: #symbol-tupleobjectdollar]

**Input:**
- `result: var string`
- `x: T`

**Output:** *(none)*
**Generic parameters:** `T`
