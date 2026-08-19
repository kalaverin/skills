---
source_hash: e41790bda5da29d9
source_path: lib/std/private/osseps.nim
---

# osseps

[ref: #module-osseps]

## Const

### AltSep

[ref: #symbol-altsep]

```nim
AltSep = '/'
```

An alternative character used by the operating system to separate pathname components, or the same as [DirSep](#DirSep) if only one separator character exists. This is set to '/' on Windows systems where [DirSep](#DirSep) is a backslash ('\\').

### CurDir

[ref: #symbol-curdir]

The constant character used by the operating system to refer to the current directory.

```nim
CurDir = '.'
```

The constant character used by the operating system to refer to the current directory.

For example: '.' for POSIX or ':' for the classic Macintosh.

### DirSep

[ref: #symbol-dirsep]

```nim
DirSep = '/'
```

The character used by the operating system to separate pathname components, for example: '/' for POSIX, ':' for the classic Macintosh, and '\\' on Windows.

### doslikeFileSystem

[ref: #symbol-doslikefilesystem]

```nim
doslikeFileSystem = false
```

### DynlibFormat

[ref: #symbol-dynlibformat]

```nim
DynlibFormat = "lib$1.dylib"
```

The format string to turn a filename into a DLL file (also called shared object on some operating systems).

### ExeExt

[ref: #symbol-exeext]

```nim
ExeExt = ""
```

The file extension of native executables. For example: "" for POSIX, "exe" on Windows (without a dot).

### ExtSep

[ref: #symbol-extsep]

```nim
ExtSep = '.'
```

The character which separates the base filename from the extension; for example, the '.' in os.nim.

### FileSystemCaseSensitive

[ref: #symbol-filesystemcasesensitive]

```nim
FileSystemCaseSensitive = false
```

True if the file system is case sensitive, false otherwise. Used by [cmpPaths](#cmpPaths) to compare filenames properly.

### ParDir

[ref: #symbol-pardir]

The constant string used by the operating system to refer to the parent directory.

```nim
ParDir = ".."
```

The constant string used by the operating system to refer to the parent directory.

For example: ".." for POSIX or "::" for the classic Macintosh.

### PathSep

[ref: #symbol-pathsep]

```nim
PathSep = ':'
```

The character conventionally used by the operating system to separate search path components (as in PATH), such as ':' for POSIX or ';' for Windows.

### ScriptExt

[ref: #symbol-scriptext]

```nim
ScriptExt = ""
```

The file extension of a script file. For example: "" for POSIX, "bat" on Windows.
