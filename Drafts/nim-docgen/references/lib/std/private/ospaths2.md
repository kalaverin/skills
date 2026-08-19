---
source_hash: 27134941b86b61ea
source_path: lib/std/private/ospaths2.nim
---

# ospaths2

[ref: #module-ospaths2]

## Examples

```nim
when defined(posix):
  assert "usr" / "" == "usr"
  assert "" / "lib" == "lib"
  assert "" / "/lib" == "/lib"
  assert "usr/" / "/lib/" == "usr/lib/"
  assert "usr" / "lib" / "../bin" == "usr/bin"
```

```nim
when defined(posix):
  assert "a/b/c" /../ "d/e" == "a/b/d/e"
  assert "a" /../ "d/e" == "a/d/e"
```

```nim
assert absolutePath("a") == getCurrentDir() / "a"
```

```nim
assert addFileExt("foo.bar", "baz") == "foo.bar"
assert addFileExt("foo.bar", "") == "foo.bar"
assert addFileExt("foo", "baz") == "foo.baz"
```

```nim
assert changeFileExt("foo.bar", "baz") == "foo.baz"
assert changeFileExt("foo.bar", "") == "foo"
assert changeFileExt("foo", "baz") == "foo.baz"
```

```nim
when defined(macosx):
  assert cmpPaths("foo", "Foo") == 0
elif defined(posix):
  assert cmpPaths("foo", "Foo") > 0
```

```nim
assert extractFilename("foo/bar/") == ""
assert extractFilename("foo/bar") == "bar"
assert extractFilename("foo/bar.baz") == "bar.baz"
```

```nim
assert not "".isAbsolute
assert not ".".isAbsolute
when defined(posix):
  assert "/".isAbsolute
  assert not "a/".isAbsolute
  assert "/a/".isAbsolute
```

```nim
doAssert isRelativeTo("./foo//bar", "foo")
doAssert isRelativeTo("foo/bar", ".")
doAssert isRelativeTo("/foo/bar.nim", "/foo/bar.nim")
doAssert not isRelativeTo("foo/bar.nims", "foo/bar.nim")
```

```nim
assert isRootDir("")
assert isRootDir(".")
assert isRootDir("/")
assert isRootDir("a")
assert not isRootDir("/a")
assert not isRootDir("a/b/c")
```

```nim
when defined(posix):
  assert joinPath("usr", "lib") == "usr/lib"
  assert joinPath("usr", "lib/") == "usr/lib/"
  assert joinPath("usr", "") == "usr"
  assert joinPath("usr/", "") == "usr/"
  assert joinPath("", "") == ""
  assert joinPath("", "lib") == "lib"
  assert joinPath("", "/lib") == "/lib"
  assert joinPath("usr/", "/lib") == "usr/lib"
  assert joinPath("usr/lib", "../bin") == "usr/bin"
```

```nim
when defined(posix):
  assert joinPath("a") == "a"
  assert joinPath("a", "b", "c") == "a/b/c"
  assert joinPath("usr/lib", "../../var", "log") == "var/log"
```

```nim
assert lastPathPart("foo/bar/") == "bar"
assert lastPathPart("foo/bar") == "bar"
```

```nim
when defined(posix):
  assert normalizedPath("a///b//..//c///d") == "a/c/d"
```

```nim
import std/sugar
when defined(posix):
  doAssert "foo".dup(normalizeExe) == "./foo"
  doAssert "foo/../bar".dup(normalizeExe) == "foo/../bar"
doAssert "".dup(normalizeExe) == ""
```

```nim
when defined(posix):
  var a = "a///b//..//c///d"
  a.normalizePath()
  assert a == "a/c/d"
```

```nim
when defined(posix):
  assert normalizePathEnd("/lib//.//", trailingSep = true) == "/lib/"
  assert normalizePathEnd("lib/./.", trailingSep = false) == "lib"
  assert normalizePathEnd(".//./.", trailingSep = false) == "."
  assert normalizePathEnd("", trailingSep = true) == "" # not / !
  assert normalizePathEnd("/", trailingSep = false) == "/" # not "" !
```

```nim
assert parentDir("") == ""
when defined(posix):
  assert parentDir("/usr/local/bin") == "/usr/local"
  assert parentDir("foo/bar//") == "foo"
  assert parentDir("//foo//bar//.") == "/foo"
  assert parentDir("./foo") == "."
  assert parentDir("/./foo//./") == "/"
  assert parentDir("a//./") == "."
  assert parentDir("a/b/c/..") == "a"
```

```nim
assert relativePath("/Users/me/bar/z.nim", "/Users/other/bad", '/') == "../../me/bar/z.nim"
assert relativePath("/Users/me/bar/z.nim", "/Users/other", '/') == "../me/bar/z.nim"
when not doslikeFileSystem: # On Windows, UNC-paths start with `//`
  assert relativePath("/Users///me/bar//z.nim", "//Users/", '/') == "me/bar/z.nim"
assert relativePath("/Users/me/bar/z.nim", "/Users/me", '/') == "bar/z.nim"
assert relativePath("", "/users/moo", '/') == ""
assert relativePath("foo", ".", '/') == "foo"
assert relativePath("foo", "foo", '/') == "."
```

```nim
assert searchExtPos("a/b/c") == -1
assert searchExtPos("c.nim") == 1
assert searchExtPos("a/b/c.nim") == 5
assert searchExtPos("a.b.c.nim") == 5
assert searchExtPos(".nim") == -1
assert searchExtPos("..nim") == -1
assert searchExtPos("a..nim") == 2
```

```nim
var (dir, name, ext) = splitFile("usr/local/nimc.html")
assert dir == "usr/local"
assert name == "nimc"
assert ext == ".html"
(dir, name, ext) = splitFile("/usr/local/os")
assert dir == "/usr/local"
assert name == "os"
assert ext == ""
(dir, name, ext) = splitFile("/usr/local/")
assert dir == "/usr/local"
assert name == ""
assert ext == ""
(dir, name, ext) = splitFile("/tmp.txt")
assert dir == "/"
assert name == "tmp"
assert ext == ".txt"
```

```nim
assert splitPath("usr/local/bin") == ("usr/local", "bin")
assert splitPath("usr/local/bin/") == ("usr/local/bin", "")
assert splitPath("/bin/") == ("/bin", "")
when (NimMajor, NimMinor) <= (1, 0):
  assert splitPath("/bin") == ("", "bin")
else:
  assert splitPath("/bin") == ("/", "bin")
assert splitPath("bin") == ("", "bin")
assert splitPath("") == ("", "")
```

```nim
assert tailDir("/bin") == "bin"
assert tailDir("bin") == ""
assert tailDir("bin/") == ""
assert tailDir("/usr/local/bin") == "usr/local/bin"
assert tailDir("//usr//local//bin//") == "usr//local//bin//"
assert tailDir("./usr/local/bin") == "usr/local/bin"
assert tailDir("usr/local/bin") == "local/bin"
```

```nim
let g = "a/b/c"

for p in g.parentDirs:
  echo p
  # a/b/c
  # a/b
  # a

for p in g.parentDirs(fromRoot=true):
  echo p
  # a/
  # a/b/
  # a/b/c

for p in g.parentDirs(inclusive=false):
  echo p
  # a/b
  # a
```

## Iterator

### parentDirs

[ref: #symbol-parentdirs]

Walks over all parent directories of a given path.

**Input:**
- `path: string`
- `fromRoot:  = false`
- `inclusive:  = true`

**Output:** `string`
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
- `head: string`
- `tail: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as parentDir(head) / tail, unless there is no parent directory. Then head / tail is performed instead.

See also:

* [/](#/)
* [parentDir](#parentDir)

### `/`

[ref: #symbol-]

The same as [joinPath](#joinPath).

**Input:**
- `head: string`
- `tail: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as [joinPath](#joinPath).

See also:

* [/](#/)
* [joinPath](#joinPath)
* [joinPath](#joinPath)
* [splitPath](#splitPath)
* [uri.combine proc](uri.html#combine,Uri,Uri)
* [uri./ proc](uri.html#/,Uri,string)

### absolutePath

[ref: #symbol-absolutepath]

Returns the absolute path of path, rooted at root (which must be absolute; default: current directory). If path is absolute, return it, ignoring root.

**Input:**
- `path: string`
- `root:  = when supportedSystem:
  getCurrentDir()
else:
  ""`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Returns the absolute path of path, rooted at root (which must be absolute; default: current directory). If path is absolute, return it, ignoring root.

See also:

* [normalizedPath](#normalizedPath)
* [normalizePath](#normalizePath)

### addFileExt

[ref: #symbol-addfileext]

Adds the file extension ext to filename, unless filename already has an extension.

**Input:**
- `filename: string`
- `ext: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds the file extension ext to filename, unless filename already has an extension.

Ext should be given without the leading '.', because some filesystems may use a different character. (Although I know of none such beast.)

See also:

* [searchExtPos](#searchExtPos)
* [splitFile](#splitFile)
* [extractFilename](#extractFilename)
* [lastPathPart](#lastPathPart)
* [changeFileExt](#changeFileExt)

### changeFileExt

[ref: #symbol-changefileext]

Changes the file extension to ext.

**Input:**
- `filename: string`
- `ext: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Changes the file extension to ext.

If the filename has no extension, ext will be added. If ext == "" then any extension is removed.

Ext should be given without the leading '.', because some filesystems may use a different character. (Although I know of none such beast.)

See also:

* [searchExtPos](#searchExtPos)
* [splitFile](#splitFile)
* [extractFilename](#extractFilename)
* [lastPathPart](#lastPathPart)
* [addFileExt](#addFileExt)

### cmpPaths

[ref: #symbol-cmppaths]

Compares two paths.

**Input:**
- `pathA: string`
- `pathB: string`

**Output:** `int`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two paths.

On a case-sensitive filesystem this is done case-sensitively otherwise case-insensitively. Returns:

0 if pathA == pathB  
< 0 if pathA < pathB  
> 0 if pathA > pathB

### extractFilename

[ref: #symbol-extractfilename]

Extracts the filename of a given path.

**Input:**
- `path: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Extracts the filename of a given path.

This is the same as name & ext from [splitFile](#splitFile).

See also:

* [searchExtPos](#searchExtPos)
* [splitFile](#splitFile)
* [lastPathPart](#lastPathPart)
* [changeFileExt](#changeFileExt)
* [addFileExt](#addFileExt)

### getCurrentDir

[ref: #symbol-getcurrentdir]

Returns the current working directory i.e. where the built binary is run.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: []`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: `, `raises: OSError`, `forbids: `

Returns the current working directory i.e. where the built binary is run.

So the path returned by this proc is determined at run time.

See also:

* [getHomeDir](#getHomeDir)
* [getConfigDir](#getConfigDir)
* [getTempDir](#getTempDir)
* [setCurrentDir](#setCurrentDir)
* [currentSourcePath template](system.html#currentSourcePath.t)
* [getProjectPath proc](macros.html#getProjectPath)

### isAbsolute

[ref: #symbol-isabsolute]

Checks whether a given path is absolute.

**Input:**
- `path: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `noSideEffect`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether a given path is absolute.

On Windows, network paths are considered absolute too.

### isRelativeTo

[ref: #symbol-isrelativeto]

**Input:**
- `path: string`
- `base: string`

**Output:** `bool`
**Pragmas:** `raises: [ValueError, OSError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, OSError`, `tags: RootEffect`, `forbids: `

Returns true if path is relative to base.

### isRootDir

[ref: #symbol-isrootdir]

**Input:**
- `path: string`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks whether a given path is a root directory.

### joinPath

[ref: #symbol-joinpath]

Joins two directory names to one.

**Input:**
- `head: string`
- `tail: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Joins two directory names to one.

returns normalized path concatenation of head and tail, preserving whether or not tail has a trailing slash (or, if tail if empty, whether head has one).

See also:

* [joinPath](#joinPath)
* [/](#/)
* [splitPath](#splitPath)
* [uri.combine proc](uri.html#combine,Uri,Uri)
* [uri./ proc](uri.html#/,Uri,string)

### joinPath

[ref: #symbol-joinpath]

The same as [joinPath](#joinPath), but works with any number of directory parts.

**Input:**
- `parts: varargs[string]`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1OpenArray"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as [joinPath](#joinPath), but works with any number of directory parts.

You need to pass at least one element or the proc will assert in debug builds and crash on release builds.

See also:

* [joinPath](#joinPath)
* [/](#/)
* [/](#/)
* [splitPath](#splitPath)

### lastPathPart

[ref: #symbol-lastpathpart]

Like [extractFilename](#extractFilename), but ignores trailing dir separator; aka: baseName in some other languages.

**Input:**
- `path: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Like [extractFilename](#extractFilename), but ignores trailing dir separator; aka: baseName in some other languages.

See also:

* [searchExtPos](#searchExtPos)
* [splitFile](#splitFile)
* [extractFilename](#extractFilename)
* [changeFileExt](#changeFileExt)
* [addFileExt](#addFileExt)

### normalizedPath

[ref: #symbol-normalizedpath]

Returns a normalized path for the current OS.

**Input:**
- `path: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: []`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Returns a normalized path for the current OS.

See also:

* [absolutePath](#absolutePath)
* [normalizePath](#normalizePath) for the in-place version

### normalizeExe

[ref: #symbol-normalizeexe]

**Input:**
- `file: var string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

on posix, prepends ./ if file doesn't contain / and is not "", ".", "..".

### normalizePath

[ref: #symbol-normalizepath]

Normalize a path.

**Input:**
- `path: var string`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: []`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Normalize a path.

Consecutive directory separators are collapsed, including an initial double slash.

On relative paths, double dot (..) sequences are collapsed if possible. On absolute paths they are always collapsed.

**Warning:**
URL-encoded and Unicode attempts at directory traversal are not detected. Triple dot is not handled.

See also:

* [absolutePath](#absolutePath)
* [normalizedPath](#normalizedPath) for outplace version
* [normalizeExe](#normalizeExe)

### normalizePathEnd

[ref: #symbol-normalizepathend]

**Input:**
- `path: var string`
- `trailingSep:  = false`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Ensures path has exactly 0 or 1 trailing DirSep, depending on trailingSep, and taking care of edge cases: it preservers whether a path is absolute or relative, and makes sure trailing sep is DirSep, not AltSep. Trailing /. are compressed, see examples.

### normalizePathEnd

[ref: #symbol-normalizepathend]

**Input:**
- `path: string`
- `trailingSep:  = false`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

outplace overload

### parentDir

[ref: #symbol-parentdir]

Returns the parent directory of path.

**Input:**
- `path: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

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
- `path: string`
- `base: string`
- `sep:  = DirSep`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `raises: [ValueError, OSError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, OSError`, `tags: RootEffect`, `forbids: `

Converts path to a path relative to base.

The sep (default: [DirSep](#DirSep)) is used for the path normalizations, this can be useful to ensure the relative path only contains '/' so that it can be used for URL constructions.

On Windows, if a root of path and a root of base are different, returns path as is because it is impossible to make a relative path. That means an absolute path can be returned.

See also:

* [splitPath](#splitPath)
* [parentDir](#parentDir)
* [tailDir](#tailDir)

### sameFile

[ref: #symbol-samefile]

Returns true if both pathname arguments refer to the same physical file or directory.

**Input:**
- `path1: string`
- `path2: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: OSError`, `forbids: `

Returns true if both pathname arguments refer to the same physical file or directory.

Raises OSError if any of the files does not exist or information about it can not be obtained.

This proc will return true if given two alternative hard-linked or sym-linked paths to the same file or directory.

See also:

* [sameFileContent](#sameFileContent)

### searchExtPos

[ref: #symbol-searchextpos]

Returns index of the '.' char in path if it signifies the beginning of the file extension. Returns -1 otherwise.

**Input:**
- `path: string`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns index of the '.' char in path if it signifies the beginning of the file extension. Returns -1 otherwise.

See also:

* [splitFile](#splitFile)
* [extractFilename](#extractFilename)
* [lastPathPart](#lastPathPart)
* [changeFileExt](#changeFileExt)
* [addFileExt](#addFileExt)

### splitFile

[ref: #symbol-splitfile]

Splits a filename into (dir, name, extension) tuple.

**Input:**
- `path: string`

**Output:** `tuple[dir, name, ext: string]`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits a filename into (dir, name, extension) tuple.

dir does not end in [DirSep](#DirSep) unless it's /. extension includes the leading dot.

If path has no extension, ext is the empty string. If path has no directory component, dir is the empty string. If path has no filename component, name and ext are empty strings.

See also:

* [searchExtPos](#searchExtPos)
* [extractFilename](#extractFilename)
* [lastPathPart](#lastPathPart)
* [changeFileExt](#changeFileExt)
* [addFileExt](#addFileExt)

### splitPath

[ref: #symbol-splitpath]

Splits a directory into (head, tail) tuple, so that head / tail == path (except for edge cases like "/usr").

**Input:**
- `path: string`

**Output:** `tuple[head, tail: string]`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits a directory into (head, tail) tuple, so that head / tail == path (except for edge cases like "/usr").

See also:

* [joinPath](#joinPath)
* [joinPath](#joinPath)
* [/](#/)
* [/](#/)
* [relativePath](#relativePath)

### tailDir

[ref: #symbol-taildir]

Returns the tail part of path.

**Input:**
- `path: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

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
- `path: string`
- `drive:  = ""`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nos$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts an UNIX-like path to a native one.

On an UNIX system this does nothing. Else it converts '/', '.', '..' to the appropriate things.

On systems with a concept of "drives", drive is used to determine which drive label to use during absolute path conversion. drive defaults to the drive of the current working directory, and is ignored on systems that do not have a concept of "drives".
