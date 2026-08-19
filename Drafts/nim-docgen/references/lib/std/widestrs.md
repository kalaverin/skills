---
source_hash: 3ace22339095635f
source_path: lib/std/widestrs.nim
---

# widestrs

[ref: #module-widestrs]

Nim support for C/C++'s wide strings.

## Proc

### `$`

[ref: #symbol-]

Decodes a length-delimited UTF-16 slice to UTF-8.

**Input:**
- `w: openArray[Utf16Char]`
- `replacement: int = 0x0000FFFD`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Decodes a length-delimited UTF-16 slice to UTF-8.

Unlike the WideCString overloads, this preserves the provided length and does not search for a terminating NUL.

### `$`

[ref: #symbol-]

**Input:**
- `w: WideCString`
- `estimate: int`
- `replacement: int = 0x0000FFFD`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `$`

[ref: #symbol-]

**Input:**
- `s: WideCString`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `$`

[ref: #symbol-]

**Input:**
- `s: WideCStringObj`
- `estimate: int`
- `replacement: int = 0x0000FFFD`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `$`

[ref: #symbol-]

**Input:**
- `s: WideCStringObj`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### len

[ref: #symbol-len]

**Input:**
- `w: WideCString`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the length of a widestring. This traverses the whole string to find the binary zero end marker!

### len

[ref: #symbol-len]

**Input:**
- `w: WideCStringObj`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newWideCString

[ref: #symbol-newwidecstring]

**Input:**
- `size: int`

**Output:** `WideCStringObj`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newWideCString

[ref: #symbol-newwidecstring]

**Input:**
- `source: cstring`
- `L: int`

**Output:** `WideCStringObj`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Warning:: source needs to be preallocated with the length L

### newWideCString

[ref: #symbol-newwidecstring]

**Input:**
- `s: cstring`

**Output:** `WideCStringObj`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newWideCString

[ref: #symbol-newwidecstring]

**Input:**
- `s: string`

**Output:** `WideCStringObj`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Template

### `[]=`

[ref: #symbol-]

**Input:**
- `a: WideCStringObj`
- `idx: int`
- `val: Utf16Char`

**Output:** *(none)*
### `[]`

[ref: #symbol-]

**Input:**
- `a: WideCStringObj`
- `idx: int`

**Output:** `Utf16Char`
## Type

### Utf16Char

[ref: #symbol-utf16char]

```nim
Utf16Char = distinct int16
```

### WideCString

[ref: #symbol-widecstring]

```nim
WideCString = ptr UncheckedArray[Utf16Char]
```

### WideCStringObj

[ref: #symbol-widecstringobj]

```nim
WideCStringObj = object
```
