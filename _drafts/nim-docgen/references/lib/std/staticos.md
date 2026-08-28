---
source_hash: e28f9dbf7fd71c53
source_path: lib/std/staticos.nim
---

# staticos

[ref: #module-staticos]

This module implements path handling like os module but works at only compile-time. This module works even when cross compiling to OS that is not supported by os module.

## Proc

### staticDirExists

[ref: #symbol-staticdirexists]

**Input:**
- `dir: string`

**Output:** `bool`
**Pragmas:** `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if the directory dir exists. If dir is a file, false is returned. Follows symlinks.

### staticFileExists

[ref: #symbol-staticfileexists]

Returns true if filename exists and is a regular file or symlink.

**Input:**
- `filename: string`

**Output:** `bool`
**Pragmas:** `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if filename exists and is a regular file or symlink.

Directories, device files, named pipes and sockets return false.

### staticWalkDir

[ref: #symbol-staticwalkdir]

Walks over the directory dir and returns a seq with each directory or file in dir. The component type and full path for each item are returned.

**Input:**
- `dir: string`
- `relative:  = false`

**Output:** `seq[tuple[kind: PathComponent, path: string]]`
**Pragmas:** `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Walks over the directory dir and returns a seq with each directory or file in dir. The component type and full path for each item are returned.

Walking is not recursive.

* If relative is true (default: false) the resulting path is shortened to be relative to dir, otherwise the full path is returned.

## Type

### PathComponent

[ref: #symbol-pathcomponent]

Enumeration specifying a path component.

```nim
PathComponent = enum
  pcFile,                   ## path refers to a file
  pcLinkToFile,             ## path refers to a symbolic link to a file
  pcDir,                    ## path refers to a directory
  pcLinkToDir                ## path refers to a symbolic link to a directory
```

Enumeration specifying a path component.

See also:

* [walkDirRec](#walkDirRec)
* [FileInfo](#FileInfo)
