---
source_hash: ff9c3630b49038f3
source_path: lib/pure/asyncfile.nim
---

# asyncfile

[ref: #module-asyncfile]

This module implements asynchronous file reading and writing.

```
import std/[asyncfile, asyncdispatch, os]

proc main() {.async.} =
  var file = openAsync(getTempDir() / "foobar.txt", fmReadWrite)
  await file.write("test")
  file.setFilePos(0)
  let data = await file.readAll()
  doAssert data == "test"
  file.close()

waitFor main()
```

## Examples

```nim
import std/[asyncfile, asyncdispatch, os]

proc main() {.async.} =
  var file = openAsync(getTempDir() / "foobar.txt", fmReadWrite)
  await file.write("test")
  file.setFilePos(0)
  let data = await file.readAll()
  doAssert data == "test"
  file.close()

waitFor main()
```

## Proc

### close

[ref: #symbol-close]

**Input:**
- `f: AsyncFile`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Closes the file specified.

### getFilePos

[ref: #symbol-getfilepos]

**Input:**
- `f: AsyncFile`

**Output:** `int64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the current position of the file pointer that is used to read from the specified file. The file's first byte has the index zero.

### getFileSize

[ref: #symbol-getfilesize]

**Input:**
- `f: AsyncFile`

**Output:** `int64`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Retrieves the specified file's size.

### newAsyncFile

[ref: #symbol-newasyncfile]

**Input:**
- `fd: AsyncFD`

**Output:** `AsyncFile`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Creates AsyncFile with a previously opened file descriptor fd.

### openAsync

[ref: #symbol-openasync]

**Input:**
- `filename: string`
- `mode:  = fmRead`

**Output:** `AsyncFile`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Opens a file specified by the path in filename using the specified FileMode mode asynchronously.

### read

[ref: #symbol-read]

Read size bytes from the specified file asynchronously starting at the current position of the file pointer. size should be greater than zero.

**Input:**
- `f: AsyncFile`
- `size: int`

**Output:** `Future[string]`
**Pragmas:** `raises: [ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception`, `tags: RootEffect`, `forbids: `

Read size bytes from the specified file asynchronously starting at the current position of the file pointer. size should be greater than zero.

If the file pointer is past the end of the file then an empty string is returned.

### readAll

[ref: #symbol-readall]

**Input:**
- `f: AsyncFile`

**Output:** `Future[string]`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError`, `tags: RootEffect`, `forbids: `

Reads all data from the specified file.

### readBuffer

[ref: #symbol-readbuffer]

Read size bytes from the specified file asynchronously starting at the current position of the file pointer.

**Input:**
- `f: AsyncFile`
- `buf: pointer`
- `size: int`

**Output:** `Future[int]`
**Pragmas:** `raises: [ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception`, `tags: RootEffect`, `forbids: `

Read size bytes from the specified file asynchronously starting at the current position of the file pointer.

If the file pointer is past the end of the file then zero is returned and no bytes are read into buf

### readLine

[ref: #symbol-readline]

**Input:**
- `f: AsyncFile`

**Output:** `Future[string]`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError`, `tags: RootEffect`, `forbids: `

Reads a single line from the specified file asynchronously.

### readToStream

[ref: #symbol-readtostream]

**Input:**
- `f: AsyncFile`
- `fs: FutureStream[string]`

**Output:** `owned(Future[void])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError`, `tags: RootEffect`, `forbids: `

Writes data to the specified future stream as the file is read.

### setFilePos

[ref: #symbol-setfilepos]

**Input:**
- `f: AsyncFile`
- `pos: int64`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the position of the file pointer that is used for read/write operations. The file's first byte has the index zero.

### setFileSize

[ref: #symbol-setfilesize]

**Input:**
- `f: AsyncFile`
- `length: int64`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Set a file length.

### write

[ref: #symbol-write]

Writes data to the file specified asynchronously.

**Input:**
- `f: AsyncFile`
- `data: string`

**Output:** `Future[void]`
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Writes data to the file specified asynchronously.

The returned Future will complete once all data has been written to the specified file.

### writeBuffer

[ref: #symbol-writebuffer]

Writes size bytes from buf to the file specified asynchronously.

**Input:**
- `f: AsyncFile`
- `buf: pointer`
- `size: int`

**Output:** `Future[void]`
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Writes size bytes from buf to the file specified asynchronously.

The returned Future will complete once all data has been written to the specified file.

### writeFromStream

[ref: #symbol-writefromstream]

Reads data from the specified future stream until it is completed. The data which is read is written to the file immediately and freed from memory.

**Input:**
- `f: AsyncFile`
- `fs: FutureStream[string]`

**Output:** `owned(Future[void])`
**Pragmas:** `stackTrace: false`, `raises: [Exception, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError`, `tags: RootEffect`, `forbids: `

Reads data from the specified future stream until it is completed. The data which is read is written to the file immediately and freed from memory.

This procedure is perfect for saving streamed data to a file without wasting memory.

## Type

### AsyncFile

[ref: #symbol-asyncfile]

```nim
AsyncFile = ref object
```
