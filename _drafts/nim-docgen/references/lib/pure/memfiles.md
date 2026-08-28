---
source_hash: 74b34fdb0201e924
source_path: lib/pure/memfiles.nim
---

# memfiles

[ref: #module-memfiles]

|  |  |
| --- | --- |
| Authors: | Zahary Karadjov, Andreas Rumpf |

This module provides support for memory mapped files (Posix's mmap) on the different operating systems.

It also provides some fast iterators over lines in text files (or other "line-like", variable length, delimited records).

## Examples

```nim
var
  mm, mm_full, mm_half: MemFile

mm = memfiles.open("/tmp/test.mmap", mode = fmWrite, newFileSize = 1024)    # Create a new file
mm.close()

# Read the whole file, would fail if newFileSize was set
mm_full = memfiles.open("/tmp/test.mmap", mode = fmReadWrite, mappedSize = -1)

# Read the first 512 bytes
mm_half = memfiles.open("/tmp/test.mmap", mode = fmReadWrite, mappedSize = 512)
```

```nim
var buffer: string = ""
for line in lines(memfiles.open("foo"), buffer):
  echo line
```

```nim
for line in lines(memfiles.open("foo")):
  echo line
```

```nim
var count = 0
for slice in memSlices(memfiles.open("foo")):
  if slice.size > 0 and cast[cstring](slice.data)[0] != '#':
    inc(count)
echo count
```

## Iterator

### lines

[ref: #symbol-lines]

Replace contents of passed buffer with each new line, like [readLine(File)](syncio.html#readLine,File,string). delim, eat, and delimiting logic is exactly as for [memSlices](#memSlices.i,MemFile,char,char), but Nim strings are returned.

**Input:**
- `mfile: MemFile`
- `buf: var string`
- `delim:  = '\n'`
- `eat:  = '\r'`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Replace contents of passed buffer with each new line, like [readLine(File)](syncio.html#readLine,File,string). delim, eat, and delimiting logic is exactly as for [memSlices](#memSlices.i,MemFile,char,char), but Nim strings are returned.

Example:

```
var buffer: string = ""
for line in lines(memfiles.open("foo"), buffer):
  echo line
```

### lines

[ref: #symbol-lines]

Return each line in a file as a Nim string, like [lines(File)](syncio.html#lines.i,File). delim, eat, and delimiting logic is exactly as for [memSlices](#memSlices.i,MemFile,char,char), but Nim strings are returned.

**Input:**
- `mfile: MemFile`
- `delim:  = '\n'`
- `eat:  = '\r'`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Return each line in a file as a Nim string, like [lines(File)](syncio.html#lines.i,File). delim, eat, and delimiting logic is exactly as for [memSlices](#memSlices.i,MemFile,char,char), but Nim strings are returned.

Example:

```
for line in lines(memfiles.open("foo")):
  echo line
```

### memSlices

[ref: #symbol-memslices]

Iterates over [optional eat] delim-delimited slices in MemFile mfile.

**Input:**
- `mfile: MemFile`
- `delim:  = '\n'`
- `eat:  = '\r'`

**Output:** `MemSlice`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over [optional eat] delim-delimited slices in MemFile mfile.

Default parameters parse lines ending in either Unix(\l) or Windows(\r\l) style on on a line-by-line basis. I.e., not every line needs the same ending. Unlike readLine(File) & lines(File), archaic MacOS9 \r-delimited lines are not supported as a third option for each line. Such archaic MacOS9 files can be handled by passing delim='\r', eat='\0', though.

Delimiters are not part of the returned slice. A final, unterminated line or record is returned just like any other.

Non-default delimiters can be passed to allow iteration over other sorts of "line-like" variable length records. Pass eat='\0' to be strictly delim-delimited. (Eating an optional prefix equal to '\0' is not supported.)

This zero copy, memchr-limited interface is probably the fastest way to iterate over line-like records in a file. However, returned (data,size) objects are not Nim strings, bounds checked Nim arrays, or even terminated C strings. So, care is required to access the data (e.g., think C mem\* functions, not str\* functions).

Example:

```
var count = 0
for slice in memSlices(memfiles.open("foo")):
  if slice.size > 0 and cast[cstring](slice.data)[0] != '#':
    inc(count)
echo count
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `ms: MemSlice`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Return a Nim string built from a MemSlice.

### `==`

[ref: #symbol-]

**Input:**
- `x: MemSlice`
- `y: MemSlice`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compare a pair of MemSlice for strict equality.

### close

[ref: #symbol-close]

**Input:**
- `f: var MemFile`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

closes the memory mapped file f. All changes are written back to the file system, if f was opened with write access.

### flush

[ref: #symbol-flush]

**Input:**
- `f: var MemFile`
- `attempts: Natural = 3`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Flushes f's buffer for the number of attempts equal to attempts. If were errors an exception OSError will be raised.

### mapMem

[ref: #symbol-mapmem]

returns a pointer to a mapped portion of MemFile m

**Input:**
- `m: var MemFile`
- `mode: FileMode = fmRead`
- `mappedSize:  = -1`
- `offset:  = 0`
- `mapFlags:  = cint(-1)`

**Output:** `pointer`
**Pragmas:** `raises: [IOError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: `, `forbids: `

returns a pointer to a mapped portion of MemFile m

mappedSize of -1 maps to the whole file, and offset must be multiples of the PAGE SIZE of your OS

### newMemMapFileStream

[ref: #symbol-newmemmapfilestream]

**Input:**
- `filename: string`
- `mode: FileMode = fmRead`
- `fileSize: int = -1`

**Output:** `MemMapFileStream`
**Pragmas:** `raises: [IOError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: `, `forbids: `

creates a new stream from the file named filename with the mode mode. Raises ## OSError if the file cannot be opened. See the [system](system.html) module for a list of available FileMode enums. fileSize can only be set if the file does not exist and is opened with write access (e.g., with fmReadWrite).

### open

[ref: #symbol-open]

opens a memory mapped file. If this fails, OSError is raised.

**Input:**
- `filename: string`
- `mode: FileMode = fmRead`
- `mappedSize:  = -1`
- `offset:  = 0`
- `newFileSize:  = -1`
- `allowRemap:  = false`
- `mapFlags:  = cint(-1)`

**Output:** `MemFile`
**Pragmas:** `raises: [IOError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: `, `forbids: `

opens a memory mapped file. If this fails, OSError is raised.

newFileSize can only be set if the file does not exist and is opened with write access (e.g., with fmReadWrite).

mappedSize and offset can be used to map only a slice of the file.

offset must be multiples of the PAGE SIZE of your OS (usually 4K or 8K but is unique to your OS)

allowRemap only needs to be true if you want to call mapMem on the resulting MemFile; else file handles are not kept open.

mapFlags allows callers to override default choices for memory mapping flags with a bitwise mask of a variety of likely platform-specific flags which may be ignored or even cause open to fail if misspecified.

Example:

```
var
  mm, mm_full, mm_half: MemFile

mm = memfiles.open("/tmp/test.mmap", mode = fmWrite, newFileSize = 1024)    # Create a new file
mm.close()

# Read the whole file, would fail if newFileSize was set
mm_full = memfiles.open("/tmp/test.mmap", mode = fmReadWrite, mappedSize = -1)

# Read the first 512 bytes
mm_half = memfiles.open("/tmp/test.mmap", mode = fmReadWrite, mappedSize = 512)
```

### resize

[ref: #symbol-resize]

**Input:**
- `f: var MemFile`
- `newFileSize: int`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: `, `forbids: `

Resize & re-map the file underlying an allowRemap MemFile. If the OS/FS supports it, file space is reserved to ensure room for new virtual pages. Caller should wait often enough for flush to finish to limit use of system RAM for write buffering, perhaps just prior to this call. **Note**: this assumes the entire file is mapped read-write at offset 0. Also, the value of .mem will probably change.

### unmapMem

[ref: #symbol-unmapmem]

unmaps the memory region (p, <p+size) of the mapped file f. All changes are written back to the file system, if f was opened with write access.

**Input:**
- `f: var MemFile`
- `p: pointer`
- `size: int`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

unmaps the memory region (p, <p+size) of the mapped file f. All changes are written back to the file system, if f was opened with write access.

size must be of exactly the size that was requested via mapMem.

## Type

### MemFile

[ref: #symbol-memfile]

```nim
MemFile = object
  mem*: pointer              ## a pointer to the memory mapped file. The pointer
                             ## can be used directly to change the contents of the
                             ## file, if it was opened with write access.
  size*: int                 ## size of the memory mapped file
  when defined(windows):
    fHandle*: Handle ## **Caution**: Windows specific public field to allow
                     ## even more low level trickery.
    mapHandle*: Handle       ## **Caution**: Windows specific public field.
    wasOpened*: bool         ## **Caution**: Windows specific public field.
  else:
    handle*: cint            ## **Caution**: Posix specific public field.
    when nimUseFallBack:
```

represents a memory mapped file

### MemMapFileStream

[ref: #symbol-memmapfilestream]

```nim
MemMapFileStream = ref MemMapFileStreamObj
```

a stream that encapsulates a MemFile

### MemMapFileStreamObj

[ref: #symbol-memmapfilestreamobj]

```nim
MemMapFileStreamObj = object of Stream
```

### MemSlice

[ref: #symbol-memslice]

```nim
MemSlice = object
  data*: pointer
  size*: int
```

represent slice of a MemFile for iteration over delimited lines/records
