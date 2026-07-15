---
source_hash: 0f5c7e83dfd5f954
source_path: lib/std/private/oscommon.nim
---

# oscommon

[ref: #module-oscommon]

## Const

### maxSymlinkLen

[ref: #symbol-maxsymlinklen]

```nim
maxSymlinkLen = 1024
```

### supportedSystem

[ref: #symbol-supportedsystem]

```nim
supportedSystem = true
```

### weirdTarget

[ref: #symbol-weirdtarget]

```nim
weirdTarget = false
```

## Proc

### dirExists

[ref: #symbol-direxists]

Returns true if the directory dir exists. If dir is a file, false is returned. Follows symlinks.

**Input:**
- `dir: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadDirEffect]`, `sideEffect`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: `, `forbids: `

Returns true if the directory dir exists. If dir is a file, false is returned. Follows symlinks.

See also:

* [fileExists](#fileExists)
* [symlinkExists](#symlinkExists)

### fileExists

[ref: #symbol-fileexists]

Returns true if filename exists and is a regular file or symlink.

**Input:**
- `filename: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadDirEffect]`, `sideEffect`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: `, `forbids: `

Returns true if filename exists and is a regular file or symlink.

Directories, device files, named pipes and sockets return false.

See also:

* [dirExists](#dirExists)
* [symlinkExists](#symlinkExists)

### getSymlinkFileKind

[ref: #symbol-getsymlinkfilekind]

**Input:**
- `path: string`

**Output:** `tuple[pc: PathComponent, isSpecial: bool]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### symlinkExists

[ref: #symbol-symlinkexists]

Returns true if the symlink link exists. Will return true regardless of whether the link points to a directory or file.

**Input:**
- `link: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadDirEffect]`, `sideEffect`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: `, `forbids: `

Returns true if the symlink link exists. Will return true regardless of whether the link points to a directory or file.

See also:

* [fileExists](#fileExists)
* [dirExists](#dirExists)

### tryMoveFSObject

[ref: #symbol-trymovefsobject]

Moves a file (or directory if isDir is true) from source to dest.

**Input:**
- `source: string`
- `dest: string`
- `isDir: bool`

**Output:** `bool`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Moves a file (or directory if isDir is true) from source to dest.

Returns false in case of EXDEV error or AccessDeniedError on Windows (if isDir is true). In case of other errors OSError is raised. Returns true in case of success.

## Type

### ReadDirEffect

[ref: #symbol-readdireffect]

```nim
ReadDirEffect = object of ReadIOEffect
```

Effect that denotes a read operation from the directory structure.

### WriteDirEffect

[ref: #symbol-writedireffect]

```nim
WriteDirEffect = object of WriteIOEffect
```

Effect that denotes a write operation to the directory structure.
