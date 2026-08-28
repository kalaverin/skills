---
source_hash: dd34b8a464eb3599
source_path: lib/pure/pathnorm.nim
---

# pathnorm

[ref: #module-pathnorm]

OS-Path normalization. Used by os.nim but also generally useful for dealing with paths.

Unstable API.

## Examples

```nim
when defined(posix):
  doAssert normalizePath("./foo//bar/../baz") == "foo/baz"
```

## Proc

### addNormalizePath

[ref: #symbol-addnormalizepath]

**Input:**
- `x: string`
- `result: var string`
- `state: var int`
- `dirSep:  = DirSep`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Low level proc. Undocumented.

### hasNext

[ref: #symbol-hasnext]

**Input:**
- `it: PathIter`
- `x: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### next

[ref: #symbol-next]

**Input:**
- `it: var PathIter`
- `x: string`

**Output:** `(int, int)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### normalizePath

[ref: #symbol-normalizepath]

* Turns multiple slashes into single slashes.

**Input:**
- `path: string`
- `dirSep:  = DirSep`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

* Turns multiple slashes into single slashes.
* Resolves '/foo/../bar' to '/bar'.
* Removes './' from the path, but "foo/.." becomes ".".

## Type

### PathIter

[ref: #symbol-pathiter]

```nim
PathIter = object
```
