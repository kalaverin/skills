---
source_hash: f9c227f8341facce
source_path: lib/pure/streams.nim
---

### openFileStream

[ref: #symbol-openfilestream]

Creates a new stream from the file named filename with the mode mode. If the file cannot be opened, an IO exception is raised.

**Input:**
- `filename: string`
- `mode: FileMode = fmRead`
- `bufSize: int = -1`

**Output:** `owned FileStream`
**Pragmas:** `raises: [IOError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError`, `tags: `, `forbids: `

Creates a new stream from the file named filename with the mode mode. If the file cannot be opened, an IO exception is raised.

**Note:** Not available for JS backend.

See also:

* [newStringStream proc](#newStringStream,string) creates a new stream from string.
* [newFileStream proc](#newFileStream,File) creates a file stream from opened File.
* [newFileStream proc](#newFileStream,string,FileMode,int) creates a file stream from the file name and the mode.

### peek

[ref: #symbol-peek]

Generic peek procedure. Peeks result from the stream s.

**Input:**
- `s: Stream`
- `result: var T`

**Output:** *(none)*
**Generic parameters:** `T`

Generic peek procedure. Peeks result from the stream s.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekBool

[ref: #symbol-peekbool]

Peeks a bool from the stream s.

**Input:**
- `s: Stream`

**Output:** `bool`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks a bool from the stream s.

A bool is one byte long and it is true for every non-zero (0000\_0000) value. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekChar

[ref: #symbol-peekchar]

**Input:**
- `s: Stream`

**Output:** `char`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks a char from the stream s. Raises IOError if an error occurred. Returns '\0' as an EOF marker.

### peekData

[ref: #symbol-peekdata]

Low level proc that reads data into an untyped buffer of bufLen size without moving stream position.

**Input:**
- `s: Stream`
- `buffer: pointer`
- `bufLen: int`

**Output:** `int`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Low level proc that reads data into an untyped buffer of bufLen size without moving stream position.

**JS note:** buffer is treated as a ptr string and written to between 0..<bufLen.

### peekFloat32

[ref: #symbol-peekfloat32]

Peeks a float32 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `float32`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks a float32 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekFloat64

[ref: #symbol-peekfloat64]

Peeks a float64 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `float64`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks a float64 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekInt16

[ref: #symbol-peekint16]

Peeks an int16 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `int16`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks an int16 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekInt32

[ref: #symbol-peekint32]

Peeks an int32 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `int32`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks an int32 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekInt64

[ref: #symbol-peekint64]

Peeks an int64 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `int64`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks an int64 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekInt8

[ref: #symbol-peekint8]

Peeks an int8 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `int8`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks an int8 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekLine

[ref: #symbol-peekline]

Peeks a line of text from the stream s into line. line must not be nil! May throw an IO exception.

**Input:**
- `s: Stream`
- `line: var string`

**Output:** `bool`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks a line of text from the stream s into line. line must not be nil! May throw an IO exception.

A line of text may be delimited by CR, LF or CRLF. The newline character(s) are not part of the returned string. Returns false if the end of the file has been reached, true otherwise. If false is returned line contains no new data.

See also:

* [readLine(Stream) proc](#readLine,Stream)
* [readLine(Stream, string) proc](#readLine,Stream,string)
* [peekLine(Stream) proc](#peekLine,Stream)

### peekLine

[ref: #symbol-peekline]

Peeks a line from a stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `string`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks a line from a stream s. Raises IOError if an error occurred.

**Note:** This is not very efficient.

See also:

* [readLine(Stream) proc](#readLine,Stream)
* [readLine(Stream, string) proc](#readLine,Stream,string)
* [peekLine(Stream, string) proc](#peekLine,Stream,string)

### peekStr

[ref: #symbol-peekstr]

**Input:**
- `s: Stream`
- `length: int`
- `str: var string`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks a string of length length from the stream s. Raises IOError if an error occurred.

### peekStr

[ref: #symbol-peekstr]

**Input:**
- `s: Stream`
- `length: int`

**Output:** `string`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks a string of length length from the stream s. Raises IOError if an error occurred.

### peekUint16

[ref: #symbol-peekuint16]

Peeks an uint16 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `uint16`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks an uint16 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekUint32

[ref: #symbol-peekuint32]

Peeks an uint32 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `uint32`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks an uint32 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekUint64

[ref: #symbol-peekuint64]

Peeks an uint64 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `uint64`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks an uint64 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### peekUint8

[ref: #symbol-peekuint8]

Peeks an uint8 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `uint8`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Peeks an uint8 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [peekStr](#peekStr,Stream,int) for now.

### read

[ref: #symbol-read]

Generic read procedure. Reads result from the stream s.

**Input:**
- `s: Stream`
- `result: var T`

**Output:** *(none)*
**Generic parameters:** `T`

Generic read procedure. Reads result from the stream s.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readAll

[ref: #symbol-readall]

**Input:**
- `s: Stream`

**Output:** `string`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads all available data.

### readBool

[ref: #symbol-readbool]

Reads a bool from the stream s.

**Input:**
- `s: Stream`

**Output:** `bool`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads a bool from the stream s.

A bool is one byte long and it is true for every non-zero (0000\_0000) value. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readChar

[ref: #symbol-readchar]

Reads a char from the stream s.

**Input:**
- `s: Stream`

**Output:** `char`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads a char from the stream s.

Raises IOError if an error occurred. Returns '\0' as an EOF marker.

### readData

[ref: #symbol-readdata]

Low level proc that reads data into an untyped buffer of bufLen size.

**Input:**
- `s: Stream`
- `buffer: pointer`
- `bufLen: int`

**Output:** `int`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Low level proc that reads data into an untyped buffer of bufLen size.

**JS note:** buffer is treated as a ptr string and written to between 0..<bufLen.

### readDataStr

[ref: #symbol-readdatastr]

**Input:**
- `s: Stream`
- `buffer: var string`
- `slice: Slice[int]`

**Output:** `int`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Low level proc that reads data into a string buffer at slice.

### readFloat32

[ref: #symbol-readfloat32]

Reads a float32 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `float32`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads a float32 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readFloat64

[ref: #symbol-readfloat64]

Reads a float64 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `float64`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads a float64 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readInt16

[ref: #symbol-readint16]

Reads an int16 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `int16`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads an int16 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readInt32

[ref: #symbol-readint32]

Reads an int32 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `int32`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads an int32 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readInt64

[ref: #symbol-readint64]

Reads an int64 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `int64`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads an int64 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readInt8

[ref: #symbol-readint8]

Reads an int8 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `int8`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads an int8 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readLine

[ref: #symbol-readline]

Reads a line of text from the stream s into line. line must not be nil! May throw an IO exception.

**Input:**
- `s: Stream`
- `line: var string`

**Output:** `bool`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads a line of text from the stream s into line. line must not be nil! May throw an IO exception.

A line of text may be delimited by LF or CRLF. The newline character(s) are not part of the returned string. Returns false if the end of the file has been reached, true otherwise. If false is returned line contains no new data.

See also:

* [readLine(Stream) proc](#readLine,Stream)
* [peekLine(Stream) proc](#peekLine,Stream)
* [peekLine(Stream, string) proc](#peekLine,Stream,string)

### readLine

[ref: #symbol-readline]

Reads a line from a stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `string`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads a line from a stream s. Raises IOError if an error occurred.

**Note:** This is not very efficient.

See also:

* [readLine(Stream, string) proc](#readLine,Stream,string)
* [peekLine(Stream) proc](#peekLine,Stream)
* [peekLine(Stream, string) proc](#peekLine,Stream,string)

### readStr

[ref: #symbol-readstr]

**Input:**
- `s: Stream`
- `length: int`
- `str: var string`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads a string of length length from the stream s. Raises IOError if an error occurred.

### readStr

[ref: #symbol-readstr]

**Input:**
- `s: Stream`
- `length: int`

**Output:** `string`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads a string of length length from the stream s. Raises IOError if an error occurred.

### readUint16

[ref: #symbol-readuint16]

Reads an uint16 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `uint16`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads an uint16 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readUint32

[ref: #symbol-readuint32]

Reads an uint32 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `uint32`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads an uint32 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readUint64

[ref: #symbol-readuint64]

Reads an uint64 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `uint64`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads an uint64 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### readUint8

[ref: #symbol-readuint8]

Reads an uint8 from the stream s. Raises IOError if an error occurred.

**Input:**
- `s: Stream`

**Output:** `uint8`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Reads an uint8 from the stream s. Raises IOError if an error occurred.

**Note:** Not available for JS backend. Use [readStr](#readStr,Stream,int) for now.

### setPosition

[ref: #symbol-setposition]

**Input:**
- `s: Stream`
- `pos: int`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: `, `forbids: `

Sets the position pos of the stream s.

### write

[ref: #symbol-write]

Generic write procedure. Writes x to the stream s. Implementation:

**Input:**
- `s: Stream`
- `x: T`

**Output:** *(none)*
**Generic parameters:** `T`

Generic write procedure. Writes x to the stream s. Implementation:

**Note:** Not available for JS backend. Use [write(Stream, string)](#write,Stream,string) for now.

```
s.writeData(s, unsafeAddr(x), sizeof(x))
```

### write

[ref: #symbol-write]

**Input:**
- `s: Stream`
- `x: string`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Writes the string x to the stream s. No length field or terminating zero is written.

### write

[ref: #symbol-write]

**Input:**
- `s: Stream`
- `args: varargs[string, `$`]`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Writes one or more strings to the the stream. No length fields or terminating zeros are written.

### writeData

[ref: #symbol-writedata]

Low level proc that writes an untyped buffer of bufLen size to the stream s.

**Input:**
- `s: Stream`
- `buffer: pointer`
- `bufLen: int`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Low level proc that writes an untyped buffer of bufLen size to the stream s.

**JS note:** buffer is treated as a ptr string and read between 0..<bufLen.

### writeLine

[ref: #symbol-writeline]

**Input:**
- `s: Stream`
- `args: varargs[string, `$`]`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Writes one or more strings to the the stream s followed by a new line. No length field or terminating zero is written.

## Type

### FileStream

[ref: #symbol-filestream]

A stream that encapsulates a File.

```nim
FileStream = ref FileStreamObj
```

A stream that encapsulates a File.

**Note:** Not available for JS backend.

### FileStreamObj

[ref: #symbol-filestreamobj]

A file stream object.

```nim
FileStreamObj = object of Stream
```

A file stream object.

**Note:** Not available for JS backend.

### Stream

[ref: #symbol-stream]

```nim
Stream = ref StreamObj
```

All procedures of this module use this type. Procedures don't directly use [StreamObj](#StreamObj).

### StreamObj

[ref: #symbol-streamobj]

Stream interface that supports writing or reading.

```nim
StreamObj = object of RootObj
  closeImpl*: proc (s: Stream) {.nimcall, raises: [IOError, OSError],
                                 tags: [WriteIOEffect], gcsafe.}
  atEndImpl*: proc (s: Stream): bool {.nimcall,
                                       raises: [Defect, IOError, OSError],
                                       tags: [], gcsafe.}
  setPositionImpl*: proc (s: Stream; pos: int) {.nimcall,
      raises: [Defect, IOError, OSError], tags: [], gcsafe.}
  getPositionImpl*: proc (s: Stream): int {.nimcall,
      raises: [Defect, IOError, OSError], tags: [], gcsafe.}
  readDataStrImpl*: proc (s: Stream; buffer: var string; slice: Slice[int]): int {.
      nimcall, raises: [Defect, IOError, OSError], tags: [ReadIOEffect], gcsafe.}
  readLineImpl*: proc (s: Stream; line: var string): bool {.nimcall,
      raises: [Defect, IOError, OSError], tags: [ReadIOEffect], gcsafe.}
  readDataImpl*: proc (s: Stream; buffer: pointer; bufLen: int): int {.nimcall,
      raises: [Defect, IOError, OSError], tags: [ReadIOEffect], gcsafe.}
  peekDataImpl*: proc (s: Stream; buffer: pointer; bufLen: int): int {.nimcall,
      raises: [Defect, IOError, OSError], tags: [ReadIOEffect], gcsafe.}
  writeDataImpl*: proc (s: Stream; buffer: pointer; bufLen: int) {.nimcall,
      raises: [Defect, IOError, OSError], tags: [WriteIOEffect], gcsafe.}
  flushImpl*: proc (s: Stream) {.nimcall, raises: [Defect, IOError, OSError],
                                 tags: [WriteIOEffect], gcsafe.}
```

Stream interface that supports writing or reading.

**Note:**

* That these fields here shouldn't be used directly. They are accessible so that a stream implementation can override them.

### StringStream

[ref: #symbol-stringstream]

```nim
StringStream = ref StringStreamObj
```

A stream that encapsulates a string.

### StringStreamObj

[ref: #symbol-stringstreamobj]

```nim
StringStreamObj = object of StreamObj
  data*: string              ## A string data.
                             ## This is updated when called `writeLine` etc.
```

A string stream object.

[Prev](streams_1.md)
