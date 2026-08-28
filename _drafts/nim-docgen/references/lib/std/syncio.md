---
source_hash: 34e3c2307207f46a
source_path: lib/std/syncio.nim
---

# syncio

[ref: #module-syncio]

This module implements various synchronized I/O operations.

## Examples

```nim
proc countZeros(filename: File): tuple[lines, zeros: int] =
  for line in filename.lines:
    for letter in line:
      if letter == '0':
        result.zeros += 1
    result.lines += 1
```

```nim
import std/strutils

proc transformLetters(filename: string) =
  var buffer = ""
  for line in filename.lines:
    buffer.add(line.replace("a", "0") & '\n')
  writeFile(filename, buffer)
```

## Iterator

### lines

[ref: #symbol-lines]

Iterates over any line in the file named filename.

**Input:**
- `filename: string`

**Output:** `string`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [IOError, IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError, IOError`, `forbids: `

Iterates over any line in the file named filename.

If the file does not exist IOError is raised. The trailing newline character(s) are removed from the iterated lines. Example:

### lines

[ref: #symbol-lines]

Iterates over any line in the file f.

**Input:**
- `f: File`

**Output:** `string`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError`, `forbids: `

Iterates over any line in the file f.

The trailing newline character(s) are removed from the iterated lines.

## Proc

### close

[ref: #symbol-close]

**Input:**
- `f: File`

**Output:** *(none)*
**Pragmas:** `tags: []`, `gcsafe`, `sideEffect`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Closes the file.

### endOfFile

[ref: #symbol-endoffile]

**Input:**
- `f: File`

**Output:** `bool`
**Pragmas:** `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Returns true if f is at the end.

### flushFile

[ref: #symbol-flushfile]

**Input:**
- `f: File`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: `, `forbids: `

Flushes f's buffer.

### getFileHandle

[ref: #symbol-getfilehandle]

**Input:**
- `f: File`

**Output:** `FileHandle`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the file handle of the file f. This is only useful for platform specific programming. Note that on Windows this doesn't return the Windows-specific handle, but the C library's notion of a handle, whatever that means. Use getOsFileHandle instead.

### getFilePos

[ref: #symbol-getfilepos]

**Input:**
- `f: File`

**Output:** `int64`
**Pragmas:** `gcsafe`, `raises: [IOError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError`, `tags: `, `forbids: `

Retrieves the current position of the file pointer that is used to read from the file f. The file's first byte has the index zero.

### getFileSize

[ref: #symbol-getfilesize]

**Input:**
- `f: File`

**Output:** `int64`
**Pragmas:** `tags: [ReadIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError`, `forbids: `

Retrieves the file size (in bytes) of f.

### getOsFileHandle

[ref: #symbol-getosfilehandle]

**Input:**
- `f: File`

**Output:** `FileHandle`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the OS file handle of the file f. This is only useful for platform specific programming.

### open

[ref: #symbol-open]

Opens a file named filename with given mode.

**Input:**
- `f: var File`
- `filename: string`
- `mode: FileMode = fmRead`
- `bufSize: int = -1`

**Output:** `bool`
**Pragmas:** `tags: []`, `raises: []`, `gcsafe`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Opens a file named filename with given mode.

Default mode is readonly. Returns true if the file could be opened. This throws no exception if the file could not be opened.

The file handle associated with the resulting File is not inheritable.

### open

[ref: #symbol-open]

Creates a File from a filehandle with given mode.

**Input:**
- `f: var File`
- `filehandle: FileHandle`
- `mode: FileMode = fmRead`

**Output:** `bool`
**Pragmas:** `tags: []`, `raises: []`, `gcsafe`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Creates a File from a filehandle with given mode.

Default mode is readonly. Returns true if the file could be opened.

The passed file handle will no longer be inheritable.

### open

[ref: #symbol-open]

Opens a file named filename with given mode.

**Input:**
- `filename: string`
- `mode: FileMode = fmRead`
- `bufSize: int = -1`

**Output:** `File`
**Pragmas:** `raises: [IOError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError`, `tags: `, `forbids: `

Opens a file named filename with given mode.

Default mode is readonly. Raises an IOError if the file could not be opened.

The file handle associated with the resulting File is not inheritable.

### readAll

[ref: #symbol-readall]

Reads all data from the stream file.

**Input:**
- `file: File`

**Output:** `string`
**Pragmas:** `tags: [ReadIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError`, `forbids: `

Reads all data from the stream file.

Raises an IO exception in case of an error. It is an error if the current file position is not at the beginning of the file.

### readBuffer

[ref: #symbol-readbuffer]

**Input:**
- `f: File`
- `buffer: pointer`
- `len: Natural`

**Output:** `int`
**Pragmas:** `tags: [ReadIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError`, `forbids: `

Reads len bytes into the buffer pointed to by buffer. Returns the actual number of bytes that have been read which may be less than len (if not as many bytes are remaining), but not greater.

### readBytes

[ref: #symbol-readbytes]

**Input:**
- `f: File`
- `a: var openArray[int8 | uint8]`
- `start: Natural`
- `len: Natural`

**Output:** `int`
**Generic parameters:** `a:type`

**Pragmas:** `tags: [ReadIOEffect]`, `gcsafe`

**Effects:** `tags: ReadIOEffect`

Reads len bytes into the buffer a starting at a[start]. Returns the actual number of bytes that have been read which may be less than len (if not as many bytes are remaining), but not greater.

### readChar

[ref: #symbol-readchar]

**Input:**
- `f: File`

**Output:** `char`
**Pragmas:** `tags: [ReadIOEffect]`, `raises: [IOError, EOFError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError, EOFError`, `forbids: `

Reads a single character from the stream f. Should not be used in performance sensitive code.

### readChars

[ref: #symbol-readchars]

**Input:**
- `f: File`
- `a: var openArray[char]`

**Output:** `int`
**Pragmas:** `tags: [ReadIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError`, `forbids: `

Reads up to a.len bytes into the buffer a. Returns the actual number of bytes that have been read which may be less than a.len (if not as many bytes are remaining), but not greater.

### readChars

[ref: #symbol-readchars]

**Input:**
- `f: File`
- `a: var openArray[char]`
- `start: Natural`
- `len: Natural`

**Output:** `int`
**Pragmas:** `tags: [ReadIOEffect]`, `gcsafe`, `deprecated: "use other `readChars` overload, possibly via: readChars(toOpenArray(buf, start, len-1))"`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError`, `forbids: `

Reads len bytes into the buffer a starting at a[start]. Returns the actual number of bytes that have been read which may be less than len (if not as many bytes are remaining), but not greater.

### readFile

[ref: #symbol-readfile]

**Input:**
- `filename: string`

**Output:** `string`
**Pragmas:** `tags: [ReadIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError`, `forbids: `

Opens a file named filename for reading, calls [readAll](#readAll,File) and closes the file afterwards. Returns the string. Raises an IO exception in case of an error. If you need to call this inside a compile time macro you can use [staticRead](system.html#staticRead,string).

### readLine

[ref: #symbol-readline]

**Input:**
- `f: File`
- `line: var string`

**Output:** `bool`
**Pragmas:** `tags: [ReadIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError`, `forbids: `

Reads a line of text from the file f into line. May throw an IO exception. A line of text may be delimited by LF or CRLF. The newline character(s) are not part of the returned string. Returns false if the end of the file has been reached, true otherwise. If false is returned line contains no new data.

### readLine

[ref: #symbol-readline]

**Input:**
- `f: File`

**Output:** `string`
**Pragmas:** `tags: [ReadIOEffect]`, `gcsafe`, `raises: [IOError, EOFError]`, `forbids: []`

**Effects:** `tags: ReadIOEffect`, `raises: IOError, EOFError`, `forbids: `

Reads a line of text from the file f. May throw an IO exception. A line of text may be delimited by LF or CRLF. The newline character(s) are not part of the returned string.

### readLines

[ref: #symbol-readlines]

**Input:**
- `filename: string`
- `n: Natural`

**Output:** `seq[string]`
**Pragmas:** `raises: [IOError, EOFError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, EOFError`, `tags: ReadIOEffect`, `forbids: `

Reads n lines from the file named filename. Raises an IO exception in case of an error. Raises EOF if file does not contain at least n lines. Available at compile time. A line of text may be delimited by LF or CRLF. The newline character(s) are not part of the returned strings.

### reopen

[ref: #symbol-reopen]

Reopens the file f with given filename and mode. This is often used to redirect the stdin, stdout or stderr file variables.

**Input:**
- `f: File`
- `filename: string`
- `mode: FileMode = fmRead`

**Output:** `bool`
**Pragmas:** `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Reopens the file f with given filename and mode. This is often used to redirect the stdin, stdout or stderr file variables.

Default mode is readonly. Returns true if the file could be reopened.

The file handle associated with f won't be inheritable.

### setFilePos

[ref: #symbol-setfilepos]

**Input:**
- `f: File`
- `pos: int64`
- `relativeTo: FileSeekPos = fspSet`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `sideEffect`, `raises: [IOError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError`, `tags: `, `forbids: `

Sets the position of the file pointer that is used for read/write operations. The file's first byte has the index zero.

### setInheritable

[ref: #symbol-setinheritable]

Controls whether a file handle can be inherited by child processes. Returns true on success. This requires the OS file handle, which can be retrieved via [getOsFileHandle](#getOsFileHandle,File).

**Input:**
- `f: FileHandle`
- `inheritable: bool`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Controls whether a file handle can be inherited by child processes. Returns true on success. This requires the OS file handle, which can be retrieved via [getOsFileHandle](#getOsFileHandle,File).

This procedure is not guaranteed to be available for all platforms. Test for availability with [declared()](system.html#declared,untyped).

### setStdIoUnbuffered

[ref: #symbol-setstdiounbuffered]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `tags: []`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: `, `raises: `, `forbids: `

Configures stdin, stdout and stderr to be unbuffered.

### write

[ref: #symbol-write]

**Input:**
- `f: File`
- `c: cstring`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

Writes a value to the file f. May throw an IO exception.

### write

[ref: #symbol-write]

**Input:**
- `f: File`
- `s: string`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

### write

[ref: #symbol-write]

**Input:**
- `f: File`
- `i: int`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

### write

[ref: #symbol-write]

**Input:**
- `f: File`
- `i: BiggestInt`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

### write

[ref: #symbol-write]

**Input:**
- `f: File`
- `b: bool`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

### write

[ref: #symbol-write]

**Input:**
- `f: File`
- `r: float32`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

### write

[ref: #symbol-write]

**Input:**
- `f: File`
- `r: BiggestFloat`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

### write

[ref: #symbol-write]

**Input:**
- `f: File`
- `c: char`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: []`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: `, `forbids: `

### write

[ref: #symbol-write]

**Input:**
- `f: File`
- `a: varargs[string, `$`]`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

### writeBuffer

[ref: #symbol-writebuffer]

**Input:**
- `f: File`
- `buffer: pointer`
- `len: Natural`

**Output:** `int`
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

Writes the bytes of buffer pointed to by the parameter buffer to the file f. Returns the number of actual written bytes, which may be less than len in case of an error.

### writeBytes

[ref: #symbol-writebytes]

**Input:**
- `f: File`
- `a: openArray[int8 | uint8]`
- `start: Natural`
- `len: Natural`

**Output:** `int`
**Generic parameters:** `a:type`

**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`

**Effects:** `tags: WriteIOEffect`

Writes the bytes of a[start..start+len-1] to the file f. Returns the number of actual written bytes, which may be less than len in case of an error.

### writeChars

[ref: #symbol-writechars]

**Input:**
- `f: File`
- `a: openArray[char]`
- `start: Natural`
- `len: Natural`

**Output:** `int`
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

Writes the bytes of a[start..start+len-1] to the file f. Returns the number of actual written bytes, which may be less than len in case of an error.

### writeFile

[ref: #symbol-writefile]

**Input:**
- `filename: string`
- `content: string`

**Output:** *(none)*
**Pragmas:** `tags: [WriteIOEffect]`, `gcsafe`, `raises: [IOError]`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: IOError`, `forbids: `

Opens a file named filename for writing. Then writes the content completely to the file and closes the file afterwards. Raises an IO exception in case of an error.

### writeFile

[ref: #symbol-writefile]

**Input:**
- `filename: string`
- `content: openArray[byte]`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Opens a file named filename for writing. Then writes the content completely to the file and closes the file afterwards. Raises an IO exception in case of an error.

### writeLine

[ref: #symbol-writeline]

**Input:**
- `f: File`
- `x: varargs[Ty, `$`]`

**Output:** *(none)*
**Generic parameters:** `Ty`

**Pragmas:** `inline`, `tags: [WriteIOEffect]`, `gcsafe`

**Effects:** `tags: WriteIOEffect`

Writes the values x to f and then writes "\n". May throw an IO exception.

## Template

### `&amp;=`

[ref: #symbol-amp]

**Input:**
- `f: File`
- `x: typed`

**Output:** *(none)*
An alias for write.

### readLines

[ref: #symbol-readlines]

**Input:**
- `filename: string`

**Output:** `seq[string]`
**Pragmas:** `deprecated: "use readLines with two arguments"`

### stdmsg

[ref: #symbol-stdmsg]

**Input:**
- *(none)*

**Output:** `File`
Template which expands to either stdout or stderr depending on useStdoutAsStdmsg compile-time switch.

## Type

### File

[ref: #symbol-file]

```nim
File = ptr CFile
```

The type representing a file handle.

### FileHandle

[ref: #symbol-filehandle]

```nim
FileHandle = cint
```

The type that represents an OS file handle; this is useful for low-level file access.

### FileMode

[ref: #symbol-filemode]

```nim
FileMode = enum
  fmRead,                   ## Open the file for read access only.
                             ## If the file does not exist, it will not
                             ## be created.
  fmWrite,                  ## Open the file for write access only.
                             ## If the file does not exist, it will be
                             ## created. Existing files will be cleared!
  fmReadWrite,              ## Open the file for read and write access.
                             ## If the file does not exist, it will be
                             ## created. Existing files will be cleared!
  fmReadWriteExisting,      ## Open the file for read and write access.
                             ## If the file does not exist, it will not be
                             ## created. The existing file will not be cleared.
  fmAppend                   ## Open the file for writing only; append data
                             ## at the end. If the file does not exist, it
                             ## will be created.
```

The file mode when opening a file.

### FileSeekPos

[ref: #symbol-fileseekpos]

```nim
FileSeekPos = enum
  fspSet,                   ## Seek to absolute value
  fspCur,                   ## Seek relative to current position
  fspEnd                     ## Seek relative to end
```

Position relative to which seek should happen.

## Var

### stderr

[ref: #symbol-stderr]

```nim
stderr {.importc: "__stderrp", header: "<stdio.h>".}: File
```

The standard error stream.

### stdin

[ref: #symbol-stdin]

```nim
stdin {.importc: "__stdinp", header: "<stdio.h>".}: File
```

The standard input stream.

### stdout

[ref: #symbol-stdout]

```nim
stdout {.importc: "__stdoutp", header: "<stdio.h>".}: File
```

The standard output stream.
