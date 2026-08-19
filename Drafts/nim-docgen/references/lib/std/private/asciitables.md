---
source_hash: b00d7045387a9dfb
source_path: lib/std/private/asciitables.nim
---

# asciitables

[ref: #module-asciitables]

## Iterator

### parseTableCells

[ref: #symbol-parsetablecells]

**Input:**
- `s: string`
- `delim:  = '\t'`

**Output:** `Cell`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over all cells in a delim-delimited s, after a 1st pass that computes number of rows, columns, and width of each column.

## Proc

### alignTable

[ref: #symbol-aligntable]

**Input:**
- `s: string`
- `delim:  = '\t'`
- `fill:  = ' '`
- `sep:  = " "`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Formats a delim-delimited s representing a table; each cell is aligned to a width that's computed for each column; consecutive columns are delimited by sep, and alignment space is filled using fill. More customized formatting can be done by calling parseTableCells directly.

## Type

### Cell

[ref: #symbol-cell]

```nim
Cell = object
  text*: string
  width*, row*, col*, ncols*, nrows*: int
```
