---
source_hash: 3449b1529502946e
source_path: lib/std/symlinks.nim
---

# symlinks

[ref: #module-symlinks]

This module implements symlink (symbolic link) handling.

## Proc

### createSymlink

[ref: #symbol-createsymlink]

Create a symbolic link at dest which points to the item specified by src. On most operating systems, will fail if a link already exists.

**Input:**
- `src: Path`
- `dest: Path`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Create a symbolic link at dest which points to the item specified by src. On most operating systems, will fail if a link already exists.

**Warning:**
Some OS's (such as Microsoft Windows) restrict the creation of symlinks to root users (administrators) or users with developer mode enabled.

See also:

* [createHardlink](#createHardlink)
* [expandSymlink](#expandSymlink)

### expandSymlink

[ref: #symbol-expandsymlink]

Returns the stored target of the symbolic link symlinkPath.

**Input:**
- `symlinkPath: Path`

**Output:** `Path`
**Pragmas:** `inline`, `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns the stored target of the symbolic link symlinkPath.

This expands exactly one level of indirection, like POSIX readlink. If the target is itself a symbolic link, it is returned as-is rather than being expanded further.

On POSIX, raises OSError if symlinkPath is not a symbolic link or if the target cannot be read.

On Windows, this supports symbolic links and junctions by reading the reparse point payload directly. Unsupported reparse tags raise OSError.

On Nintendo Switch this is currently a noop: symlinkPath is simply returned, without checking whether it is actually a symbolic link.

See also:

* [createSymlink](#createSymlink)

### symlinkExists

[ref: #symbol-symlinkexists]

**Input:**
- `link: Path`

**Output:** `bool`
**Pragmas:** `inline`, `tags: [ReadDirEffect]`, `sideEffect`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: `, `forbids: `

Returns true if the symlink link exists. Will return true regardless of whether the link points to a directory or file.
