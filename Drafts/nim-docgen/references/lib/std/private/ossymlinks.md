---
source_hash: ad38597b0d22d20f
source_path: lib/std/private/ossymlinks.nim
---

# ossymlinks

[ref: #module-ossymlinks]

## Proc

### createSymlink

[ref: #symbol-createsymlink]

Create a symbolic link at dest which points to the item specified by src. On most operating systems, will fail if a link already exists.

**Input:**
- `src: string`
- `dest: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

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
- `symlinkPath: string`

**Output:** `string`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns the stored target of the symbolic link symlinkPath.

This expands exactly one level of indirection, like POSIX readlink. If the target is itself a symbolic link, it is returned as-is rather than being expanded further.

On POSIX, raises OSError if symlinkPath is not a symbolic link or if the target cannot be read.

On Windows, this supports symbolic links and junctions by reading the reparse point payload directly. Unsupported reparse tags raise OSError.

On Nintendo Switch this is currently a noop: symlinkPath is simply returned, without checking whether it is actually a symbolic link.

See also:

* [createSymlink](#createSymlink)
