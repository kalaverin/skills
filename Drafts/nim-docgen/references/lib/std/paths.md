---
source_hash: 7532d29e4d3ea8a3
source_path: lib/std/paths.nim
---

# paths

[ref: #module-paths]

This module implements path handling.

**See also:**

* [files module](files.html) for file access

## Examples

```nim
import std/appdirs
assert expandTilde(Path("~") / Path("appname.cfg")) == getHomeDir() / Path("appname.cfg")
assert expandTilde(Path("~/foo/bar")) == getHomeDir() / Path("foo/bar")
assert expandTilde(Path("/foo/bar")) == Path("/foo/bar")
```

## Iterator

### parentDirs

[ref: #symbol-parentdirs]

Walks over all parent directories of a given path.

**Input:**
- `path: Path`
- `fromRoot:  = false`
- `inclusive:  = true`

**Output:** `Path`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Walks over all parent directories of a given path.

If fromRoot is true (default: false), the traversal will start from the file system root directory. If inclusive is true (default), the original argument will be included in the traversal.

Relative paths won't be expanded by this iterator. Instead, it will traverse only the directories appearing in the relative path.

See also:

* [parentDir](#parentDir)

## Proc

### `/../`

[ref: #symbol-]

The same as parentDir(head) / tail, unless there is no parent directory. Then head / tail is performed instead.

**Input:**
- `head: Path`
- `tail: Path`

**Output:** `Path`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as parentDir(head) / tail, unless there is no parent directory. Then head / tail is performed instead.

See also:

* [/](#/)
* [parentDir](#parentDir)

### `/`

[ref: #symbol-]

Joins two directory names to one.

**Input:**
- `head: Path`
- `tail: Path`

**Output:** `Path`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Joins two directory names to one.

returns normalized path concatenation of head and tail, preserving whether or not tail has a trailing slash (or, if tail if empty, whether head has one).

See also:

* [splitPath](#splitPath)
* [uri.combine proc](uri.html#combine,Uri,Uri)
* [uri./ proc](uri.html#/,Uri,string)

### `==`

[ref: #symbol-]

Compares two paths.

**Input:**
- `x: Path`
- `y: Path`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two paths.

On a case-sensitive filesystem this is done case-sensitively otherwise case-insensitively.

### absolutePath

[ref: #symbol-absolutepath]

Returns the absolute path of path, rooted at root (which must be absolute; default: current directory). If path is absolute, return it, ignoring root.

**Input:**
- `path: Path`
- `root:  = getCurrentDir()`

**Output:** `Path`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Returns the absolute path of path, rooted at root (which must be absolute; default: current directory). If path is absolute, return it, ignoring root.

See also:

* [normalizePath](#normalizePath)

### add

[ref: #symbol-add]

**Input:**
- `x: var Path`
- `y: Path`

**Output:** *(none)*
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### addFileExt

[ref: #symbol-addfileext]

Adds the file extension ext to filename, unless filename already has an extension.

**Input:**
- `filename: Path`
- `ext: string`

**Output:** `Path`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds the file extension ext to filename, unless filename already has an extension.

Ext should be given without the leading '.', because some filesystems may use a different character. (Although I know of none such beast.)

See also:

* [splitFile](#splitFile)
* [extractFilename](#extractFilename)
* [lastPathPart](#lastPathPart)
* [changeFileExt](#changeFileExt)

### changeFileExt

[ref: #symbol-changefileext]

Changes the file extension to ext.

**Input:**
- `filename: Path`
- `ext: string`

**Output:** `Path`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Changes the file extension to ext.

If the filename has no extension, ext will be added. If ext == "" then any extension is removed.

Ext should be given without the leading '.', because some filesystems may use a different character. (Although I know of none such beast.)

See also:

* [splitFile](#splitFile)
* [extractFilename](#extractFilename)
* [lastPathPart](#lastPathPart)
* [addFileExt](#addFileExt)

### expandTilde

[ref: #symbol-expandtilde]

Expands ~ or a path starting with ~/ to a full path, replacing ~ with [getHomeDir()](appdirs.html#getHomeDir) (otherwise returns path unmodified).

**Input:**
- `path: Path`

**Output:** `Path`
**Pragmas:** `inline`, `tags: [ReadEnvEffect, ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadEnvEffect, ReadIOEffect`, `raises: `, `forbids: `

Expands ~ or a path starting with ~/ to a full path, replacing ~ with [getHomeDir()](appdirs.html#getHomeDir) (otherwise returns path unmodified).

Windows: this is still supported despite the Windows platform not having this convention; also, both ~/ and ~\ are handled.

### extractFilename

[ref: #symbol-extractfilename]

Extracts the filename of a given path.

**Input:**
- `path: Path`

**Output:** `Path`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Extracts the filename of a given path.

This is the same as name & ext from [splitFile](#splitFile).

See also:

* [splitFile](#splitFile)
* [lastPathPart](#lastPathPart)
* [changeFileExt](#changeFileExt)
* [addFileExt](#addFileExt)

### getCurrentDir

[ref: #symbol-getcurrentdir]

Returns the current working directory i.e. where the built binary is run.

**Input:**
- *(none)*

**Output:** `Path`
**Pragmas:** `inline`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Returns the current working directory i.e. where the built binary is run.

So the path returned by this proc is determined at run time.

See also:

* [getHomeDir proc](appdirs.html#getHomeDir)
* [getConfigDir proc](appdirs.html#getConfigDir)
* [getTempDir proc](appdirs.html#getTempDir)
* [setCurrentDir proc](dirs.html#setCurrentDir)
* [currentSourcePath template](system.html#currentSourcePath.t)
* [getProjectPath proc](macros.html#getProjectPath)

### hash

[ref: #symbol-hash]

**Input:**
- `x: Path`

**Output:** `Hash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isAbsolute

[ref: #symbol-isabsolute]

Checks whether a given path is absolute.

**Input:**
- `path: Path`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether a given path is absolute.

On Windows, network paths are considered absolute too.

### isRelativeTo

[ref: #symbol-isrelativeto]

**Input:**
- `path: Path`
- `base: Path`

**Output:** `bool`
**Pragmas:** `inline`, `raises: [ValueError, OSError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, OSError`, `tags: RootEffect`, `forbids: `

Returns true if path is relative to base.

### isRootDir

[ref: #symbol-isrootdir]

**Input:**
- `path: Path`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether a given path is a root directory.

### lastPathPart

[ref: #symbol-lastpathpart]

Like [extractFilename](#extractFilename), but ignores trailing dir separator; aka: baseName in some other languages.

**Input:**
- `path: Path`

**Output:** `Path`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Like [extractFilename](#extractFilename), but ignores trailing dir separator; aka: baseName in some other languages.

See also:

* [splitFile](#splitFile)
* [extractFilename](#extractFilename)
* [changeFileExt](#changeFileExt)
* [addFileExt](#addFileExt)

### normalizeExe

[ref: #symbol-normalizeexe]

**Input:**
- `file: var Path`

**Output:** *(none)*
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### normalizePath

[ref: #symbol-normalizepath]

**Input:**
- `path: var Path`

**Output:** *(none)*
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### normalizePathEnd

[ref: #symbol-normalizepathend]

**Input:**
- `path: var Path`
- `trailingSep:  = false`

**Output:** *(none)*
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### parentDir

[ref: #symbol-parentdir]

Returns the parent directory of path.

**Input:**
- `path: Path`

**Output:** `Path`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the parent directory of path.

This is similar to splitPath(path).head when path doesn't end in a dir separator, but also takes care of path normalizations. The remainder can be obtained with [lastPathPart](#lastPathPart).

See also:

* [relativePath](#relativePath)
* [splitPath](#splitPath)
* [tailDir](#tailDir)
* [parentDirs](#parentDirs)

### relativePath

[ref: #symbol-relativepath]

Converts path to a path relative to base.

**Input:**
- `path: Path`
- `base: Path`
- `sep:  = DirSep`

**Output:** `Path`
**Pragmas:** `inline`, `raises: [ValueError, OSError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, OSError`, `tags: RootEffect`, `forbids: `

Converts path to a path relative to base.

The sep (default: DirSep) is used for the path normalizations, this can be useful to ensure the relative path only contains '/' so that it can be used for URL constructions.

On Windows, if a root of path and a root of base are different, returns path as is because it is impossible to make a relative path. That means an absolute path can be returned.

See also:

* [splitPath](#splitPath)
* [parentDir](#parentDir)
* [tailDir](#tailDir)

### splitFile

[ref: #symbol-splitfile]

Splits a filename into (dir, name, extension) tuple.

**Input:**
- `path: Path`

**Output:** `tuple[dir, name: Path, ext: string]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits a filename into (dir, name, extension) tuple.

dir does not end in DirSep unless it's /. extension includes the leading dot.

If path has no extension, ext is the empty string. If path has no directory component, dir is the empty string. If path has no filename component, name and ext are empty strings.

See also:

* [extractFilename](#extractFilename)
* [lastPathPart](#lastPathPart)
* [changeFileExt](#changeFileExt)
* [addFileExt](#addFileExt)

### splitPath

[ref: #symbol-splitpath]

Splits a directory into (head, tail) tuple, so that head / tail == path (except for edge cases like "/usr").

**Input:**
- `path: Path`

**Output:** `tuple[head, tail: Path]`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits a directory into (head, tail) tuple, so that head / tail == path (except for edge cases like "/usr").

See also:

* [add](#add)
* [/](#/)
* [/](#/)
* [relativePath](#relativePath)

### tailDir

[ref: #symbol-taildir]

Returns the tail part of path.

**Input:**
- `path: Path`

**Output:** `Path`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the tail part of path.

See also:

* [relativePath](#relativePath)
* [splitPath](#splitPath)
* [parentDir](#parentDir)

### unixToNativePath

[ref: #symbol-unixtonativepath]

Converts an UNIX-like path to a native one.

**Input:**
- `path: Path`
- `drive:  = Path("")`

**Output:** `Path`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts an UNIX-like path to a native one.

On an UNIX system this does nothing. Else it converts '/', '.', '..' to the appropriate things.

On systems with a concept of "drives", drive is used to determine which drive label to use during absolute path conversion. drive defaults to the drive of the current working directory, and is ignored on systems that do not have a concept of "drives".

## Template

### `$`

[ref: #symbol-]

**Input:**
- `x: Path`

**Output:** `string`
## Type

### Path

[ref: #symbol-path]

```nim
Path = distinct string
```
