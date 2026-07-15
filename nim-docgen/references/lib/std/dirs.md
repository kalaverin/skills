---
source_hash: 5b27eaa940819600
source_path: lib/std/dirs.nim
---

# dirs

[ref: #module-dirs]

This module implements directory handling.

## Iterator

### walkDir

[ref: #symbol-walkdir]

Walks over the directory dir and yields for each directory or file in dir. The component type and full path for each item are returned.

**Input:**
- `dir: Path`
- `relative:  = false`
- `checkDir:  = false`
- `skipSpecial:  = false`

**Output:** `tuple[kind: PathComponent, path: Path]`
**Pragmas:** `tags: [ReadDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: OSError`, `forbids: `

Walks over the directory dir and yields for each directory or file in dir. The component type and full path for each item are returned.

Walking is not recursive.

* If relative is true (default: false) the resulting path is shortened to be relative to dir, otherwise the full path is returned.
* If checkDir is true, OSError is raised when dir doesn't exist.
* If skipSpecial is true, then (besides all directories) only *regular* files (**without** special "file" objects like FIFOs, device files, etc) will be yielded on Unix.

### walkDirRec

[ref: #symbol-walkdirrec]

Recursively walks over the directory dir and yields for each file or directory in dir.

**Input:**
- `dir: Path`
- `yieldFilter:  = {pcFile}`
- `followFilter:  = {pcDir}`
- `relative:  = false`
- `checkDir:  = false`
- `skipSpecial:  = false`

**Output:** `Path`
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

* [walkDir](#walkDir)

## Proc

### copyDir

[ref: #symbol-copydir]

Copies a directory from source to dest.

**Input:**
- `source: Path`
- `dest: Path`
- `skipSpecial:  = false`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: [ReadDirEffect, WriteIOEffect, ReadIOEffect]`, `raises: [OSError, IOError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect, WriteIOEffect, ReadIOEffect`, `raises: OSError, IOError`, `forbids: `

Copies a directory from source to dest.

On non-Windows OSes, symlinks are copied as symlinks. On Windows, symlinks are skipped.

If skipSpecial is true, then (besides all directories) only *regular* files (**without** special "file" objects like FIFOs, device files, etc) will be copied on Unix.

If this fails, OSError is raised.

On the Windows platform this proc will copy the attributes from source into dest.

On other platforms created files and directories will inherit the default permissions of a newly created file/directory for the user. Use [copyDirWithPermissions](#copyDirWithPermissions) to preserve attributes recursively on these platforms.

See also:

* [copyDirWithPermissions](#copyDirWithPermissions)

### copyDirWithPermissions

[ref: #symbol-copydirwithpermissions]

Copies a directory from source to dest preserving file permissions.

**Input:**
- `source: Path`
- `dest: Path`
- `ignorePermissionErrors:  = true`
- `skipSpecial:  = false`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: [ReadDirEffect, WriteIOEffect, ReadIOEffect]`, `raises: [OSError, IOError, Exception]`, `forbids: []`

**Effects:** `tags: ReadDirEffect, WriteIOEffect, ReadIOEffect`, `raises: OSError, IOError, Exception`, `forbids: `

Copies a directory from source to dest preserving file permissions.

On non-Windows OSes, symlinks are copied as symlinks. On Windows, symlinks are skipped.

If skipSpecial is true, then (besides all directories) only *regular* files (**without** special "file" objects like FIFOs, device files, etc) will be copied on Unix.

If this fails, OSError is raised. This is a wrapper proc around [copyDir](#copyDir) and [copyFileWithPermissions](#copyFileWithPermissions) procs on non-Windows platforms.

On Windows this proc is just a wrapper for [copyDir](#copyDir) since that proc already copies attributes.

On non-Windows systems permissions are copied after the file or directory itself has been copied, which won't happen atomically and could lead to a race condition. If ignorePermissionErrors is true (default), errors while reading/setting file attributes will be ignored, otherwise will raise OSError.

See also:

* [copyDir](#copyDir)

### createDir

[ref: #symbol-createdir]

Creates the directory dir.

**Input:**
- `dir: Path`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: [WriteDirEffect, ReadDirEffect]`, `raises: [OSError, IOError]`, `forbids: []`

**Effects:** `tags: WriteDirEffect, ReadDirEffect`, `raises: OSError, IOError`, `forbids: `

Creates the directory dir.

The directory may contain several subdirectories that do not exist yet. The full path is created. If this fails, OSError is raised.

It does **not** fail if the directory already exists because for most usages this does not indicate an error.

See also:

* [removeDir](#removeDir)
* [existsOrCreateDir](#existsOrCreateDir)
* [moveDir](#moveDir)

### dirExists

[ref: #symbol-direxists]

**Input:**
- `dir: Path`

**Output:** `bool`
**Pragmas:** `inline`, `tags: [ReadDirEffect]`, `sideEffect`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: `, `forbids: `

Returns true if the directory dir exists. If dir is a file, false is returned. Follows symlinks.

### existsOrCreateDir

[ref: #symbol-existsorcreatedir]

Checks if a directory dir exists, and creates it otherwise.

**Input:**
- `dir: Path`

**Output:** `bool`
**Pragmas:** `inline`, `tags: [WriteDirEffect, ReadDirEffect]`, `raises: [OSError, IOError]`, `forbids: []`

**Effects:** `tags: WriteDirEffect, ReadDirEffect`, `raises: OSError, IOError`, `forbids: `

Checks if a directory dir exists, and creates it otherwise.

Does not create parent directories (raises OSError if parent directories do not exist). Returns true if the directory already exists, and false otherwise.

See also:

* [removeDir](#removeDir)
* [createDir](#createDir)
* [moveDir](#moveDir)

### moveDir

[ref: #symbol-movedir]

Moves a directory from source to dest.

**Input:**
- `source: Path`
- `dest: Path`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: [ReadIOEffect, WriteIOEffect]`, `raises: [OSError, IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect, WriteIOEffect`, `raises: OSError, IOError`, `forbids: `

Moves a directory from source to dest.

Symlinks are not followed: if source contains symlinks, they themself are moved, not their target.

If this fails, OSError is raised.

See also:

* [moveFile proc](files.html#moveFile)
* [removeDir](#removeDir)
* [existsOrCreateDir](#existsOrCreateDir)
* [createDir](#createDir)

### removeDir

[ref: #symbol-removedir]

Removes the directory dir including all subdirectories and files in dir (recursively).

**Input:**
- `dir: Path`
- `checkDir:  = false`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: [WriteDirEffect, ReadDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteDirEffect, ReadDirEffect`, `raises: OSError`, `forbids: `

Removes the directory dir including all subdirectories and files in dir (recursively).

If this fails, OSError is raised. This does not fail if the directory never existed in the first place, unless checkDir = true.

See also:

* [removeFile proc](files.html#removeFile)
* [existsOrCreateDir](#existsOrCreateDir)
* [createDir](#createDir)
* [moveDir](#moveDir)

### setCurrentDir

[ref: #symbol-setcurrentdir]

Sets the current working directory; OSError is raised if newDir cannot been set.

**Input:**
- `newDir: Path`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Sets the current working directory; OSError is raised if newDir cannot been set.

See also:

* [getCurrentDir proc](paths.html#getCurrentDir)
