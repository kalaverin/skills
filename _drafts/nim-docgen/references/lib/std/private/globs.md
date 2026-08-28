---
source_hash: 08480fcad89ceebb
source_path: lib/std/private/globs.nim
---

# globs

[ref: #module-globs]

unstable API, internal use only for now. this can eventually be moved to std/os and walkDirRec can be implemented in terms of this to avoid duplication

## Iterator

### walkDirRecFilter

[ref: #symbol-walkdirrecfilter]

**Input:**
- `dir: string`
- `follow: proc (entry: PathEntry): bool = nil`
- `relative:  = false`
- `checkDir:  = true`

**Output:** `PathEntry`
**Pragmas:** `tags: [ReadDirEffect]`, `effectsOf: follow`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: OSError`, `forbids: `

Improved os.walkDirRec.

## Proc

### nativeToUnixPath

[ref: #symbol-nativetounixpath]

**Input:**
- `path: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### PathEntry

[ref: #symbol-pathentry]

```nim
PathEntry = object
  kind*: PathComponent
  path*: string
```
