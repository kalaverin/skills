---
source_hash: d223ea278c65eec0
source_path: lib/std/tempfiles.nim
---

# tempfiles

[ref: #module-tempfiles]

This module creates temporary files and directories.

Experimental API, subject to change.

## Examples

```nim
import std/os
doAssertRaises(OSError): discard createTempDir("", "", "nonexistent")
let dir = createTempDir("tmpprefix_", "_end")
# dir looks like: getTempDir() / "tmpprefix_YEl9VuVj_end"
assert dirExists(dir)
removeDir(dir)
```

```nim
import std/os
doAssertRaises(OSError): discard createTempFile("", "", "nonexistent")
let (cfile, path) = createTempFile("tmpprefix_", "_end.tmp")
# path looks like: getTempDir() / "tmpprefix_FDCIRZA0_end.tmp"
cfile.write "foo"
cfile.setFilePos 0
assert readAll(cfile) == "foo"
close cfile
assert readFile(path) == "foo"
removeFile(path)
```

## Proc

### createTempDir

[ref: #symbol-createtempdir]

Creates a new temporary directory in the directory dir.

**Input:**
- `prefix: string`
- `suffix: string`
- `dir:  = ""`

**Output:** `string`
**Pragmas:** `raises: [OSError, IOError]`, `tags: [ReadEnvEffect, ReadIOEffect, WriteDirEffect, ReadDirEffect]`, `forbids: []`

**Effects:** `raises: OSError, IOError`, `tags: ReadEnvEffect, ReadIOEffect, WriteDirEffect, ReadDirEffect`, `forbids: `

Creates a new temporary directory in the directory dir.

This generates a dir name using genTempPath(prefix, suffix, dir), creates the directory and returns it, possibly after retrying to ensure it doesn't already exist.

If failing to create a temporary directory, OSError will be raised.

**Note:**
It is the caller's responsibility to remove the directory when no longer needed.

**Note:**
dir must exist (empty dir will resolve to [getTempDir](appdirs.html#getTempDir)).

### createTempFile

[ref: #symbol-createtempfile]

Creates a new temporary file in the directory dir.

**Input:**
- `prefix: string`
- `suffix: string`
- `dir:  = ""`

**Output:** `tuple[cfile: File, path: string]`
**Pragmas:** `raises: [OSError]`, `tags: [ReadEnvEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: OSError`, `tags: ReadEnvEffect, ReadIOEffect`, `forbids: `

Creates a new temporary file in the directory dir.

This generates a path name using genTempPath(prefix, suffix, dir) and returns a file handle to an open file and the path of that file, possibly after retrying to ensure it doesn't already exist.

If failing to create a temporary file, OSError will be raised.

**Note:**
It is the caller's responsibility to close result.cfile and remove result.file when no longer needed.

**Note:**
dir must exist (empty dir will resolve to [getTempDir](appdirs.html#getTempDir)).

### genTempPath

[ref: #symbol-gentemppath]

Generates a path name in dir.

**Input:**
- `prefix: string`
- `suffix: string`
- `dir:  = ""`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect, ReadIOEffect`, `forbids: `

Generates a path name in dir.

The path begins with prefix and ends with suffix.

**Note:**
dir must exist (empty dir will resolve to [getTempDir](appdirs.html#getTempDir)).
