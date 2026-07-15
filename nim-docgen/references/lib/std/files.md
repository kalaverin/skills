---
source_hash: 78fa8b90979d2ba0
source_path: lib/std/files.nim
---

# files

[ref: #module-files]

This module implements file handling.

**See also:**

* [paths module](paths.html) for path manipulation

## Proc

### copyFile

[ref: #symbol-copyfile]

Copies a file from source to dest, where dest.parentDir must exist.

**Input:**
- `source: Path`
- `dest: Path`
- `options:  = cfSymlinkFollow`
- `bufferSize:  = 16384`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: [ReadDirEffect, ReadIOEffect, WriteIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect, ReadIOEffect, WriteIOEffect`, `raises: OSError`, `forbids: `

Copies a file from source to dest, where dest.parentDir must exist.

On non-Windows OSes, options specify the way file is copied; by default, if source is a symlink, copies the file symlink points to. options is ignored on Windows: symlinks are skipped.

If this fails, OSError is raised.

On the Windows platform this proc will copy the source file's attributes into dest.

On other platforms you need to use [getFilePermissions](#getFilePermissions) and [setFilePermissions](#setFilePermissions) procs to copy them by hand (or use the convenience [copyFileWithPermissions](#copyFileWithPermissions)), otherwise dest will inherit the default permissions of a newly created file for the user.

If dest already exists, the file attributes will be preserved and the content overwritten.

On OSX, copyfile C api will be used (available since OSX 10.5) unless -d:nimLegacyCopyFile is used.

copyFile allows to specify bufferSize to improve I/O performance.

See also:

* [copyFileWithPermissions](#copyFileWithPermissions)

### copyFileToDir

[ref: #symbol-copyfiletodir]

Copies a file source into directory dir, which must exist.

**Input:**
- `source: Path`
- `dir: Path`
- `options:  = cfSymlinkFollow`
- `bufferSize:  = 16384`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: [ValueError, OSError]`, `tags: [ReadDirEffect, ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: ValueError, OSError`, `tags: ReadDirEffect, ReadIOEffect, WriteIOEffect`, `forbids: `

Copies a file source into directory dir, which must exist.

On non-Windows OSes, options specify the way file is copied; by default, if source is a symlink, copies the file symlink points to. options is ignored on Windows: symlinks are skipped.

copyFileToDir allows to specify bufferSize to improve I/O performance.

### copyFileWithPermissions

[ref: #symbol-copyfilewithpermissions]

Copies a file from source to dest preserving file permissions.

**Input:**
- `source: Path`
- `dest: Path`
- `ignorePermissionErrors:  = true`
- `options:  = cfSymlinkFollow`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: [OSError, Exception]`, `tags: [ReadDirEffect, ReadIOEffect, WriteIOEffect, WriteDirEffect]`, `forbids: []`

**Effects:** `raises: OSError, Exception`, `tags: ReadDirEffect, ReadIOEffect, WriteIOEffect, WriteDirEffect`, `forbids: `

Copies a file from source to dest preserving file permissions.

On non-Windows OSes, options specify the way file is copied; by default, if source is a symlink, copies the file symlink points to. options is ignored on Windows: symlinks are skipped.

This is a wrapper proc around [copyFile](#copyFile), [getFilePermissions](#getFilePermissions) and [setFilePermissions](#setFilePermissions) procs on non-Windows platforms.

On Windows this proc is just a wrapper for [copyFile](#copyFile) since that proc already copies attributes.

On non-Windows systems permissions are copied after the file itself has been copied, which won't happen atomically and could lead to a race condition. If ignorePermissionErrors is true (default), errors while reading/setting file attributes will be ignored, otherwise will raise OSError.

See also:

* [copyFile](#copyFile)

### fileExists

[ref: #symbol-fileexists]

Returns true if filename exists and is a regular file or symlink.

**Input:**
- `filename: Path`

**Output:** `bool`
**Pragmas:** `inline`, `tags: [ReadDirEffect]`, `sideEffect`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: `, `forbids: `

Returns true if filename exists and is a regular file or symlink.

Directories, device files, named pipes and sockets return false.

### getFilePermissions

[ref: #symbol-getfilepermissions]

Retrieves file permissions for filename.

**Input:**
- `filename: Path`

**Output:** `set[FilePermission]`
**Pragmas:** `inline`, `tags: [ReadDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: OSError`, `forbids: `

Retrieves file permissions for filename.

OSError is raised in case of an error. On Windows, only the readonly flag is checked, every other permission is available in any case.

See also:

* [setFilePermissions](#setFilePermissions)

### moveFile

[ref: #symbol-movefile]

Moves a file from source to dest.

**Input:**
- `source: Path`
- `dest: Path`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: [ReadDirEffect, ReadIOEffect, WriteIOEffect]`, `raises: [OSError, Exception]`, `forbids: []`

**Effects:** `tags: ReadDirEffect, ReadIOEffect, WriteIOEffect`, `raises: OSError, Exception`, `forbids: `

Moves a file from source to dest.

Symlinks are not followed: if source is a symlink, it is itself moved, not its target.

If this fails, OSError is raised. If dest already exists, it will be overwritten.

Can be used to rename files.

See also:

* [moveDir proc](dirs.html#moveDir)
* [removeFile](#removeFile)

### removeFile

[ref: #symbol-removefile]

Removes the file.

**Input:**
- `file: Path`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: [WriteDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteDirEffect`, `raises: OSError`, `forbids: `

Removes the file.

If this fails, OSError is raised. This does not fail if the file never existed in the first place.

On Windows, ignores the read-only attribute.

See also:

* [removeDir proc](dirs.html#removeDir)
* [moveFile](#moveFile)
* [tryRemoveFile](#tryRemoveFile)

### setFilePermissions

[ref: #symbol-setfilepermissions]

Sets the file permissions for filename.

**Input:**
- `filename: Path`
- `permissions: set[FilePermission]`
- `followSymlinks:  = true`

**Output:** *(none)*
**Pragmas:** `inline`, `tags: [ReadDirEffect, WriteDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect, WriteDirEffect`, `raises: OSError`, `forbids: `

Sets the file permissions for filename.

If followSymlinks set to true (default) and filename points to a symlink, permissions are set to the file symlink points to. followSymlinks set to false is a noop on Windows and some POSIX systems (including Linux) on which lchmod is either unavailable or always fails, given that symlinks permissions there are not observed.

OSError is raised in case of an error. On Windows, only the readonly flag is changed, depending on fpUserWrite permission.

See also:

* [getFilePermissions](#getFilePermissions)

### tryRemoveFile

[ref: #symbol-tryremovefile]

Removes the file.

**Input:**
- `file: Path`

**Output:** `bool`
**Pragmas:** `inline`, `tags: [WriteDirEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: WriteDirEffect`, `raises: `, `forbids: `

Removes the file.

If this fails, returns false. This does not fail if the file never existed in the first place.

On Windows, ignores the read-only attribute.

See also:

* [removeFile](#removeFile)
