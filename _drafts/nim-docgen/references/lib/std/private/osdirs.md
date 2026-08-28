---
source_hash: 2e337c8cfdd49a95
source_path: lib/std/private/osdirs.nim
---

# osdirs

[ref: #module-osdirs]

## Examples

```nim
import std/[strutils, sugar]
# note: order is not guaranteed
# this also works at compile time
assert collect(for k in walkDir("dirA"): k.path).join(" ") ==
                      "dirA/dirB dirA/dirC dirA/fileA2.txt dirA/fileA1.txt"
```

```nim
import std/os
import std/sequtils
let paths = toSeq(walkDirs("lib/pure/*")) # works on Windows too
assert "lib/pure/concurrency".unixToNativePath in paths
```

```nim
import std/os
import std/sequtils
assert "lib/pure/os.nim".unixToNativePath in toSeq(walkFiles("lib/pure/*.nim")) # works on Windows too
```

```nim
import std/os
import std/sequtils
let paths = toSeq(walkPattern("lib/pure/*")) # works on Windows too
assert "lib/pure/concurrency".unixToNativePath in paths
assert "lib/pure/os.nim".unixToNativePath in paths
```

## Iterator

### walkDir

[ref: #symbol-walkdir]

Walks over the directory dir and yields for each directory or file in dir. The component type and full path for each item are returned.

**Input:**
- `dir: string`
- `relative:  = false`
- `checkDir:  = false`
- `skipSpecial:  = false`

**Output:** `tuple[kind: PathComponent, path: string]`
**Pragmas:** `tags: [ReadDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: OSError`, `forbids: `

Walks over the directory dir and yields for each directory or file in dir. The component type and full path for each item are returned.

Walking is not recursive.

* If relative is true (default: false) the resulting path is shortened to be relative to dir, otherwise the full path is returned.
* If checkDir is true, OSError is raised when dir doesn't exist.
* If skipSpecial is true, then (besides all directories) only *regular* files (**without** special "file" objects like FIFOs, device files, etc) will be yielded on Unix.

**Example:**

This directory structure:

```
dirA / dirB / fileB1.txt
     / dirC
     / fileA1.txt
     / fileA2.txt
```

and this code:

### walkDirRec

[ref: #symbol-walkdirrec]

Recursively walks over the directory dir and yields for each file or directory in dir.

**Input:**
- `dir: string`
- `yieldFilter:  = {pcFile}`
- `followFilter:  = {pcDir}`
- `relative:  = false`
- `checkDir:  = false`
- `skipSpecial:  = false`

**Output:** `string`
**Pragmas:** `tags: [ReadDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: OSError`, `forbids: `

Recursively walks over the directory dir and yields for each file or directory in dir.

Options relative, checkdir, skipSpecial are explained in [walkDir iterator](#walkDir iterator) description.

**Warning:**
Modifying the directory structure while the iterator is traversing may result in undefined behavior!

Walking is recursive. followFilter controls the behaviour of the iterator:

| yieldFilter | meaning |
| --- | --- |
| pcFile | yield real files (default) |
| pcLinkToFile | yield symbolic links to files |
| pcDir | yield real directories |
| pcLinkToDir | yield symbolic links to directories |

| followFilter | meaning |
| --- | --- |
| pcDir | follow real directories (default) |
| pcLinkToDir | follow symbolic links to directories |

See also:

* [walkPattern](#walkPattern)
* [walkFiles](#walkFiles)
* [walkDirs](#walkDirs)
* [walkDir](#walkDir)

### walkDirs

[ref: #symbol-walkdirs]

Iterate over all the directories that match the pattern.

**Input:**
- `pattern: string`

**Output:** `string`
**Pragmas:** `tags: [ReadDirEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: `, `forbids: `

Iterate over all the directories that match the pattern.

On POSIX this uses the glob call. pattern is OS dependent, but at least the "\*.ext" notation is supported.

See also:

* [walkPattern](#walkPattern)
* [walkFiles](#walkFiles)
* [walkDir](#walkDir)
* [walkDirRec](#walkDirRec)

### walkFiles

[ref: #symbol-walkfiles]

Iterate over all the files that match the pattern.

**Input:**
- `pattern: string`

**Output:** `string`
**Pragmas:** `tags: [ReadDirEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: `, `forbids: `

Iterate over all the files that match the pattern.

On POSIX this uses the glob call. pattern is OS dependent, but at least the "\*.ext" notation is supported.

See also:

* [walkPattern](#walkPattern)
* [walkDirs](#walkDirs)
* [walkDir](#walkDir)
* [walkDirRec](#walkDirRec)

### walkPattern

[ref: #symbol-walkpattern]

Iterate over all the files and directories that match the pattern.

**Input:**
- `pattern: string`

**Output:** `string`
**Pragmas:** `tags: [ReadDirEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: `, `forbids: `

Iterate over all the files and directories that match the pattern.

On POSIX this uses the glob call. pattern is OS dependent, but at least the "\*.ext" notation is supported.

See also:

* [walkFiles](#walkFiles)
* [walkDirs](#walkDirs)
* [walkDir](#walkDir)
* [walkDirRec](#walkDirRec)

## Proc

### copyDir

[ref: #symbol-copydir]

Copies a directory from source to dest.

**Input:**
- `source: string`
- `dest: string`
- `skipSpecial:  = false`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadDirEffect, WriteIOEffect, ReadIOEffect]`, `gcsafe`, `raises: [OSError, IOError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect, WriteIOEffect, ReadIOEffect`, `raises: OSError, IOError`, `forbids: `

Copies a directory from source to dest.

On non-Windows OSes, symlinks are copied as symlinks. On Windows, symlinks are skipped.

If skipSpecial is true, then (besides all directories) only *regular* files (**without** special "file" objects like FIFOs, device files, etc) will be copied on Unix.

If this fails, OSError is raised.

On the Windows platform this proc will copy the attributes from source into dest.

On other platforms created files and directories will inherit the default permissions of a newly created file/directory for the user. Use [copyDirWithPermissions](#copyDirWithPermissions) to preserve attributes recursively on these platforms.

See also:

* [copyDirWithPermissions](#copyDirWithPermissions)
* [copyFile](#copyFile)
* [copyFileWithPermissions](#copyFileWithPermissions)
* [removeDir](#removeDir)
* [existsOrCreateDir](#existsOrCreateDir)
* [createDir](#createDir)
* [moveDir](#moveDir)

### copyDirWithPermissions

[ref: #symbol-copydirwithpermissions]

Copies a directory from source to dest preserving file permissions.

**Input:**
- `source: string`
- `dest: string`
- `ignorePermissionErrors:  = true`
- `skipSpecial:  = false`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadDirEffect, WriteIOEffect, ReadIOEffect]`, `gcsafe`, `raises: [OSError, IOError, Exception]`, `forbids: []`

**Effects:** `tags: ReadDirEffect, WriteIOEffect, ReadIOEffect`, `raises: OSError, IOError, Exception`, `forbids: `

Copies a directory from source to dest preserving file permissions.

On non-Windows OSes, symlinks are copied as symlinks. On Windows, symlinks are skipped.

If skipSpecial is true, then (besides all directories) only *regular* files (**without** special "file" objects like FIFOs, device files, etc) will be copied on Unix.

If this fails, OSError is raised. This is a wrapper proc around [copyDir](#copyDir) and [copyFileWithPermissions](#copyFileWithPermissions) procs on non-Windows platforms.

On Windows this proc is just a wrapper for [copyDir](#copyDir) since that proc already copies attributes.

On non-Windows systems permissions are copied after the file or directory itself has been copied, which won't happen atomically and could lead to a race condition. If ignorePermissionErrors is true (default), errors while reading/setting file attributes will be ignored, otherwise will raise OSError.

See also:

* [copyDir](#copyDir)
* [copyFile](#copyFile)
* [copyFileWithPermissions](#copyFileWithPermissions)
* [removeDir](#removeDir)
* [moveDir](#moveDir)
* [existsOrCreateDir](#existsOrCreateDir)
* [createDir](#createDir)

### createDir

[ref: #symbol-createdir]

Creates the directory dir.

**Input:**
- `dir: string`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [WriteDirEffect, ReadDirEffect]`, `raises: [OSError, IOError]`, `forbids: []`

**Effects:** `tags: WriteDirEffect, ReadDirEffect`, `raises: OSError, IOError`, `forbids: `

Creates the directory dir.

The directory may contain several subdirectories that do not exist yet. The full path is created. If this fails, OSError is raised.

It does **not** fail if the directory already exists because for most usages this does not indicate an error.

See also:

* [removeDir](#removeDir)
* [existsOrCreateDir](#existsOrCreateDir)
* [copyDir](#copyDir)
* [copyDirWithPermissions](#copyDirWithPermissions)
* [moveDir](#moveDir)

### existsOrCreateDir

[ref: #symbol-existsorcreatedir]

Checks if a directory dir exists, and creates it otherwise.

**Input:**
- `dir: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [WriteDirEffect, ReadDirEffect]`, `raises: [OSError, IOError]`, `forbids: []`

**Effects:** `tags: WriteDirEffect, ReadDirEffect`, `raises: OSError, IOError`, `forbids: `

Checks if a directory dir exists, and creates it otherwise.

Does not create parent directories (raises OSError if parent directories do not exist). Returns true if the directory already exists, and false otherwise.

See also:

* [removeDir](#removeDir)
* [createDir](#createDir)
* [copyDir](#copyDir)
* [copyDirWithPermissions](#copyDirWithPermissions)
* [moveDir](#moveDir)

### moveDir

[ref: #symbol-movedir]

Moves a directory from source to dest.

**Input:**
- `source: string`
- `dest: string`

**Output:** *(none)*
**Pragmas:** `tags: [ReadIOEffect, WriteIOEffect]`, `raises: [OSError, IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect, WriteIOEffect`, `raises: OSError, IOError`, `forbids: `

Moves a directory from source to dest.

Symlinks are not followed: if source contains symlinks, they themself are moved, not their target.

If this fails, OSError is raised.

See also:

* [moveFile](#moveFile)
* [copyDir](#copyDir)
* [copyDirWithPermissions](#copyDirWithPermissions)
* [removeDir](#removeDir)
* [existsOrCreateDir](#existsOrCreateDir)
* [createDir](#createDir)

### removeDir

[ref: #symbol-removedir]

Removes the directory dir including all subdirectories and files in dir (recursively).

**Input:**
- `dir: string`
- `checkDir:  = false`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [WriteDirEffect, ReadDirEffect]`, `gcsafe`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteDirEffect, ReadDirEffect`, `raises: OSError`, `forbids: `

Removes the directory dir including all subdirectories and files in dir (recursively).

If this fails, OSError is raised. This does not fail if the directory never existed in the first place, unless checkDir = true.

See also:

* [tryRemoveFile](#tryRemoveFile)
* [removeFile](#removeFile)
* [existsOrCreateDir](#existsOrCreateDir)
* [createDir](#createDir)
* [copyDir](#copyDir)
* [copyDirWithPermissions](#copyDirWithPermissions)
* [moveDir](#moveDir)

### setCurrentDir

[ref: #symbol-setcurrentdir]

Sets the current working directory; OSError is raised if newDir cannot been set.

**Input:**
- `newDir: string`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Sets the current working directory; OSError is raised if newDir cannot been set.

See also:

* [getHomeDir](#getHomeDir)
* [getConfigDir](#getConfigDir)
* [getTempDir](#getTempDir)
* [getCurrentDir](#getCurrentDir)
