---
source_hash: 1e5a80bf0c8d5c42
source_path: lib/pure/collections/intsets.nim
---

# intsets

[ref: #module-intsets]

Specialization of the generic [packedsets module](packedsets.html) (see its documentation for more examples) for ordinal sparse sets.

## Proc

### initIntSet

[ref: #symbol-initintset]

**Input:**
- *(none)*

**Output:** `IntSet`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toIntSet

[ref: #symbol-tointset]

**Input:**
- `x: openArray[int]`

**Output:** `IntSet`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### IntSet

[ref: #symbol-intset]

```nim
IntSet = PackedSet[int]
```
