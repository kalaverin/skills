---
source_hash: a3eceb54c3efb82c
source_path: lib/pure/os.nim
---

# os

[ref: #module-os]

This module contains basic operating system facilities like retrieving environment variables, working with directories, running shell commands, etc.**See also:**

* [paths](paths.html) and [files](files.html) modules for high-level file manipulation
* [osproc module](osproc.html) for process communication beyond [execShellCmd](#execShellCmd)
* [uri module](uri.html)
* [distros module](distros.html)
* [dynlib module](dynlib.html)
* [streams module](streams.html)

## Examples

```nim
import std/os
let myFile = "/path/to/my/file.nim"
assert splitPath(myFile) == (head: "/path/to/my", tail: "file.nim")
when defined(posix):
  assert parentDir(myFile) == "/path/to/my"
assert splitFile(myFile) == (dir: "/path/to/my", name: "file", ext: ".nim")
assert myFile.changeFileExt("c") == "/path/to/my/file.c"
```

```nim
setFilePermissions(filename, getFilePermissions(filename)-permissions)
```

```nim
discard execShellCmd("ls -la")
```

```nim
assert expandTilde("~" / "appname.cfg") == getHomeDir() / "appname.cfg"
assert expandTilde("~/foo/bar") == getHomeDir() / "foo/bar"
assert expandTilde("/foo/bar") == "/foo/bar"
```

```nim
setFilePermissions(filename, getFilePermissions(filename)+permissions)
```

```nim
when defined(posix):
  assert ".foo".isHidden
  assert not ".foo/bar".isHidden
  assert not ".".isHidden
  assert not "..".isHidden
  assert not "".isHidden
  assert ".foo/".isHidden
```

```nim
assert not isValidFilename(" foo")     # Leading white space
assert not isValidFilename("foo ")     # Trailing white space
assert not isValidFilename("foo.")     # Ends with dot
assert not isValidFilename("con.txt")  # "CON" is invalid (Windows)
assert not isValidFilename("OwO:UwU")  # ":" is invalid (Mac)
assert not isValidFilename("aux.bat")  # "AUX" is invalid (Windows)
assert not isValidFilename("")         # Empty string
assert not isValidFilename("foo/")     # Filename is empty
```

```nim
when defined(posix):
  assert quoteShellCommand(["aaa", "", "c d"]) == "aaa '' 'c d'"
when defined(windows):
  assert quoteShellCommand(["aaa", "", "c d"]) == "aaa \"\" \"c d\""
```

## Const

### ExeExts

[ref: #symbol-exeexts]

```nim
ExeExts = [""]
```

Platform specific file extension for executables. On Windows ["exe", "cmd", "bat"], on Posix [""].

### invalidFilenameChars

[ref: #symbol-invalidfilenamechars]

```nim
invalidFilenameChars = {'/', '\\', ':', '*', '?', '\"', '<', '>', '|', '^',
                        '\x00'}
```

Characters that may produce invalid filenames across Linux, Windows and Mac. You can check if your filename contains any of these chars and strip them for safety. Mac bans ':', Linux bans '/', Windows bans all others.

### invalidFilenames

[ref: #symbol-invalidfilenames]

```nim
invalidFilenames = ["CON", "PRN", "AUX", "NUL", "COM0", "COM1", "COM2", "COM3",
                    "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT0",
                    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7",
                    "LPT8", "LPT9"]
```

Filenames that may be invalid across Linux, Windows, Mac, etc. You can check if your filename match these and rename it for safety (Currently all invalid filenames are from Windows only).

## Proc

### createHardlink

[ref: #symbol-createhardlink]

Create a hard link at dest which points to the item specified by src.

**Input:**
- `src: string`
- `dest: string`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Create a hard link at dest which points to the item specified by src.

**Warning:**
Some OS's restrict the creation of hard links to root users (administrators).

See also:

* [createSymlink](#createSymlink)

### exclFilePermissions

[ref: #symbol-exclfilepermissions]

A convenience proc for:

**Input:**
- `filename: string`
- `permissions: set[FilePermission]`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadDirEffect, WriteDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect, WriteDirEffect`, `raises: OSError`, `forbids: `

A convenience proc for:

```
setFilePermissions(filename, getFilePermissions(filename)-permissions)
```

### execShellCmd

[ref: #symbol-execshellcmd]

Executes a shell command.

**Input:**
- `command: string`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ExecIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ExecIOEffect`, `raises: `, `forbids: `

Executes a shell command.

Command has the form 'program args' where args are the command line arguments given to program. The proc returns the error code of the shell when it has finished (zero if there is no error). The proc does not return until the process has finished.

To execute a program without having a shell involved, use [osproc.execProcess proc](osproc.html#execProcess,string,string,openArray[string],StringTableRef,set[ProcessOption]).

**Examples:**

```
discard execShellCmd("ls -la")
```

### exitStatusLikeShell

[ref: #symbol-exitstatuslikeshell]

**Input:**
- `status: cint`

**Output:** `cint`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts exit code from c\_system into a shell exit code.

### expandFilename

[ref: #symbol-expandfilename]

Returns the full (absolute) path of an existing file filename.

**Input:**
- `filename: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect`, `raises: OSError`, `forbids: `

Returns the full (absolute) path of an existing file filename.

Raises OSError in case of an error. Follows symlinks.

### expandTilde

[ref: #symbol-expandtilde]

Expands ~ or a path starting with ~/ to a full path, replacing ~ with [getHomeDir](#getHomeDir) (otherwise returns path unmodified).

**Input:**
- `path: string`

**Output:** `string`
**Pragmas:** `tags: [ReadEnvEffect, ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadEnvEffect, ReadIOEffect`, `raises: `, `forbids: `

Expands ~ or a path starting with ~/ to a full path, replacing ~ with [getHomeDir](#getHomeDir) (otherwise returns path unmodified).

Windows: this is still supported despite the Windows platform not having this convention; also, both ~/ and ~\ are handled.

See also:

* [getHomeDir](#getHomeDir)
* [getConfigDir](#getConfigDir)
* [getTempDir](#getTempDir)
* [getCurrentDir](#getCurrentDir)
* [setCurrentDir](#setCurrentDir)

### fileNewer

[ref: #symbol-filenewer]

Returns true if the file a is newer than file b, i.e. if a's modification time is later than b's.

**Input:**
- `a: string`
- `b: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns true if the file a is newer than file b, i.e. if a's modification time is later than b's.

See also:

* [getLastModificationTime](#getLastModificationTime)
* [getLastAccessTime](#getLastAccessTime)
* [getCreationTime](#getCreationTime)

### findExe

[ref: #symbol-findexe]

Searches for exe in the current working directory and then in directories listed in the PATH environment variable.

**Input:**
- `exe: string`
- `followSymlinks: bool = true`
- `extensions: openArray[string] = ExeExts`

**Output:** `string`
**Pragmas:** `tags: [ReadDirEffect, ReadEnvEffect, ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect, ReadEnvEffect, ReadIOEffect`, `raises: OSError`, `forbids: `

Searches for exe in the current working directory and then in directories listed in the PATH environment variable.

Returns "" if the exe cannot be found. exe is added the [ExeExts](#ExeExts) file extensions if it has none.

If the system supports symlinks it also resolves them until it meets the actual file. This behavior can be disabled if desired by setting followSymlinks = false.

### getAppDir

[ref: #symbol-getappdir]

Returns the directory of the application's executable.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Returns the directory of the application's executable.

See also:

* [getAppFilename](#getAppFilename)

### getAppFilename

[ref: #symbol-getappfilename]

Returns the filename of the application's executable. This proc will resolve symlinks.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: `, `forbids: `

Returns the filename of the application's executable. This proc will resolve symlinks.

Returns empty string when name is unavailable

See also:

* [getAppDir](#getAppDir)
* [getCurrentCompilerExe](#getCurrentCompilerExe)

### getCreationTime

[ref: #symbol-getcreationtime]

Returns the file's creation time.

**Input:**
- `file: string`

**Output:** `times.Time`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns the file's creation time.

**Note:** Under POSIX OS's, the returned time may actually be the time at which the file's attribute's were last modified. See [here](https://github.com/nim-lang/Nim/issues/1058) for details.

See also:

* [getLastModificationTime](#getLastModificationTime)
* [getLastAccessTime](#getLastAccessTime)
* [fileNewer](#fileNewer)

### getCurrentCompilerExe

[ref: #symbol-getcurrentcompilerexe]

Returns the path of the currently running Nim compiler or nimble executable.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `compileTime`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the path of the currently running Nim compiler or nimble executable.

Can be used to retrieve the currently executing Nim compiler from a Nim or nimscript program, or the nimble binary inside a nimble program (likewise with other binaries built from compiler API).

### getCurrentProcessId

[ref: #symbol-getcurrentprocessid]

Return current process ID.

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Return current process ID.

See also:

* [osproc.processID(p: Process)](osproc.html#processID,Process)

### getFileInfo

[ref: #symbol-getfileinfo]

Retrieves file information for the file object represented by the given handle.

**Input:**
- `handle: FileHandle`

**Output:** `FileInfo`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Retrieves file information for the file object represented by the given handle.

If the information cannot be retrieved, such as when the file handle is invalid, OSError is raised.

See also:

* [getFileInfo](#getFileInfo)
* [getFileInfo](#getFileInfo)

### getFileInfo

[ref: #symbol-getfileinfo]

Retrieves file information for the file object.

**Input:**
- `file: File`

**Output:** `FileInfo`
**Pragmas:** `raises: [IOError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: `, `forbids: `

Retrieves file information for the file object.

See also:

* [getFileInfo](#getFileInfo)
* [getFileInfo](#getFileInfo)

### getFileInfo

[ref: #symbol-getfileinfo]

Retrieves file information for the file object pointed to by path.

**Input:**
- `path: string`
- `followSymlink:  = true`

**Output:** `FileInfo`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Retrieves file information for the file object pointed to by path.

Due to intrinsic differences between operating systems, the information contained by the returned [FileInfo](#FileInfo) will be slightly different across platforms, and in some cases, incomplete or inaccurate.

When followSymlink is true (default), symlinks are followed and the information retrieved is information related to the symlink's target. Otherwise, information on the symlink itself is retrieved (however, field isSpecial is still determined from the target on Unix).

If the information cannot be retrieved, such as when the path doesn't exist, or when permission restrictions prevent the program from retrieving file information, OSError is raised.

See also:

* [getFileInfo](#getFileInfo)
* [getFileInfo](#getFileInfo)

### getFileSize

[ref: #symbol-getfilesize]

**Input:**
- `file: string`

**Output:** `BiggestInt`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadIOEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: OSError`, `forbids: `

Returns the file size of file (in bytes). OSError is raised in case of an error.

### getLastAccessTime

[ref: #symbol-getlastaccesstime]

Returns the file's last read or write access time.

**Input:**
- `file: string`

**Output:** `times.Time`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns the file's last read or write access time.

See also:

* [getLastModificationTime](#getLastModificationTime)
* [getCreationTime](#getCreationTime)
* [fileNewer](#fileNewer)

### getLastModificationTime

[ref: #symbol-getlastmodificationtime]

Returns the file's last modification time.

**Input:**
- `file: string`

**Output:** `times.Time`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns the file's last modification time.

See also:

* [getLastAccessTime](#getLastAccessTime)
* [getCreationTime](#getCreationTime)
* [fileNewer](#fileNewer)

### inclFilePermissions

[ref: #symbol-inclfilepermissions]

A convenience proc for:

**Input:**
- `filename: string`
- `permissions: set[FilePermission]`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadDirEffect, WriteDirEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: ReadDirEffect, WriteDirEffect`, `raises: OSError`, `forbids: `

A convenience proc for:

```
setFilePermissions(filename, getFilePermissions(filename)+permissions)
```

### isAdmin

[ref: #symbol-isadmin]

**Input:**
- *(none)*

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns whether the caller's process is a member of the Administrators local group (on Windows) or a root (on POSIX), via geteuid() == 0.

### isHidden

[ref: #symbol-ishidden]

Determines whether path is hidden or not, using [this reference](https://en.wikipedia.org/wiki/Hidden_file_and_hidden_directory).

**Input:**
- `path: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Determines whether path is hidden or not, using [this reference](https://en.wikipedia.org/wiki/Hidden_file_and_hidden_directory).

On Windows: returns true if it exists and its "hidden" attribute is set.

On posix: returns true if lastPathPart(path) starts with . and is not . or ...

**Note**: paths are not normalized to determine isHidden.

### isValidFilename

[ref: #symbol-isvalidfilename]

Returns true if filename is valid for crossplatform use.

**Input:**
- `filename: string`
- `maxLen:  = 259.Positive`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if filename is valid for crossplatform use.

This is useful if you want to copy or save files across Windows, Linux, Mac, etc. It uses invalidFilenameChars, invalidFilenames and maxLen to verify the specified filename.

See also:

* <https://docs.microsoft.com/en-us/dotnet/api/system.io.pathtoolongexception>
* <https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file>
* <https://msdn.microsoft.com/en-us/library/windows/desktop/aa365247%28v=vs.85%29.aspx>

**Warning:**
This only checks filenames, not whole paths (because basically you can mount anything as a path on Linux).

### quoteShell

[ref: #symbol-quoteshell]

Quote s, so it can be safely passed to shell.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nosp$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Quote s, so it can be safely passed to shell.

When on Windows, it calls [quoteShellWindows](#quoteShellWindows). Otherwise, calls [quoteShellPosix](#quoteShellPosix).

### quoteShellCommand

[ref: #symbol-quoteshellcommand]

**Input:**
- `args: openArray[string]`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Concatenates and quotes shell arguments args.

### quoteShellPosix

[ref: #symbol-quoteshellposix]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nosp$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Quote s, so it can be safely passed to POSIX shell.

### quoteShellWindows

[ref: #symbol-quoteshellwindows]

Quote s, so it can be safely passed to Windows API.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `noSideEffect`, `gcsafe`, `extern: "nosp$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Quote s, so it can be safely passed to Windows API.

Based on Python's subprocess.list2cmdline. See [this link](https://msdn.microsoft.com/en-us/library/17w5ykft.aspx) for more details.

### sameFileContent

[ref: #symbol-samefilecontent]

Returns true if both pathname arguments refer to files with identical binary content.

**Input:**
- `path1: string`
- `path2: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [ReadIOEffect]`, `raises: [IOError, OSError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError, OSError`, `forbids: `

Returns true if both pathname arguments refer to files with identical binary content.

See also:

* [sameFile](#sameFile)

### setLastModificationTime

[ref: #symbol-setlastmodificationtime]

**Input:**
- `file: string`
- `t: times.Time`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Sets the file's last modification time. OSError is raised in case of an error.

### sleep

[ref: #symbol-sleep]

**Input:**
- `milsecs: int`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nos$1"`, `tags: [TimeEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: TimeEffect`, `raises: `, `forbids: `

Sleeps milsecs milliseconds. A negative milsecs causes sleep to return immediately.

## Template

### existsDir

[ref: #symbol-existsdir]

**Input:**
- `args: varargs[untyped]`

**Output:** `untyped`
**Pragmas:** `deprecated: "use dirExists"`

### existsFile

[ref: #symbol-existsfile]

**Input:**
- `args: varargs[untyped]`

**Output:** `untyped`
**Pragmas:** `deprecated: "use fileExists"`

## Type

### cuint32

[ref: #symbol-cuint32]

```nim
cuint32 {.importc: "unsigned int", nodecl.} = int
```

### DeviceId

[ref: #symbol-deviceid]

```nim
DeviceId = Dev
```

### FileId

[ref: #symbol-fileid]

```nim
FileId = Ino
```

### FileInfo

[ref: #symbol-fileinfo]

Contains information associated with a file object.

```nim
FileInfo = object
  id*: tuple[device: DeviceId, file: FileId] ## Device and file id.
  kind*: PathComponent       ## Kind of file object - directory, symlink, etc.
  size*: BiggestInt          ## Size of file.
  permissions*: set[FilePermission] ## File permissions
  linkCount*: BiggestInt     ## Number of hard links the file object has.
  lastAccessTime*: times.Time ## Time file was last accessed.
  lastWriteTime*: times.Time ## Time file was last modified/written to.
  creationTime*: times.Time  ## Time file was created. Not supported on all systems!
  blockSize*: int            ## Preferred I/O block size for this object.
                             ## In some filesystems, this may vary from file to file.
  isSpecial*: bool           ## Is file special? (on Unix some "files"
                             ## can be special=non-regular like FIFOs,
                             ## devices); for directories `isSpecial`
                             ## is always `false`, for symlinks it is
                             ## the same as for the link's target.
```

Contains information associated with a file object.

See also:

* [getFileInfo](#getFileInfo)
* [getFileInfo](#getFileInfo)
* [getFileInfo](#getFileInfo)
