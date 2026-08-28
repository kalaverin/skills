---
source_hash: f9c227f8341facce
source_path: lib/pure/streams.nim
---

# streams

[ref: #module-streams]

This module provides a stream interface and two implementations thereof: the [FileStream](#FileStream) and the [StringStream](#StringStream) which implement the stream interface for Nim file objects (File) and strings.

Other modules may provide other implementations for this standard stream interface.

**Warning:**
Due to the use of pointer, the readData, peekData and writeData interfaces are not available on the compile-time VM, and must be cast from a ptr string on the JS backend. However, readDataStr is available generally in place of readData.

# [Basic usage](#basic-usage)

The basic flow of using this module is:

1. Open input stream
2. Read or write stream
3. Close stream

## [StringStream example](#basic-usage-stringstream-example)

```
import std/streams

var strm = newStringStream("""The first line
the second line
the third line""")

var line = ""

while strm.readLine(line):
  echo line

# Output:
# The first line
# the second line
# the third line

strm.close()
```

## [FileStream example](#basic-usage-filestream-example)

Write file stream example:

```
import std/streams

var strm = newFileStream("somefile.txt", fmWrite)
var line = ""

if not isNil(strm):
  strm.writeLine("The first line")
  strm.writeLine("the second line")
  strm.writeLine("the third line")
  strm.close()

# Output (somefile.txt):
# The first line
# the second line
# the third line
```

Read file stream example:

```
import std/streams

var strm = newFileStream("somefile.txt", fmRead)
var line = ""

if not isNil(strm):
  while strm.readLine(line):
    echo line
  strm.close()

# Output:
# The first line
# the second line
# the third line
```

# [See also](#see-also)

* [asyncstreams module](asyncstreams.html)
* [io module](syncio.html) for [FileMode enum](syncio.html#FileMode)

## Examples

```nim
import std/streams

var strm = newStringStream("""The first line
the second line
the third line""")

var line = ""

while strm.readLine(line):
  echo line

# Output:
# The first line
# the second line
# the third line

strm.close()
```

```nim
import std/streams

var strm = newFileStream("somefile.txt", fmWrite)
var line = ""

if not isNil(strm):
  strm.writeLine("The first line")
  strm.writeLine("the second line")
  strm.writeLine("the third line")
  strm.close()

# Output (somefile.txt):
# The first line
# the second line
# the third line
```

```nim
import std/streams

var strm = newFileStream("somefile.txt", fmRead)
var line = ""

if not isNil(strm):
  while strm.readLine(line):
    echo line
  strm.close()

# Output:
# The first line
# the second line
# the third line
```

```nim
var strm = newStringStream("The first line\nthe second line\nthe third line")
var line = ""
doAssert strm.atEnd() == false
while strm.readLine(line):
  discard
doAssert strm.atEnd() == true
strm.close()
```

```nim
block:
  let strm = newStringStream("The first line\nthe second line\nthe third line")
  ## do something...
  strm.close()

block:
  let strm = newFileStream("amissingfile.txt")
  # deferring works even if newFileStream fails
  defer: strm.close()
  if not isNil(strm):
    ## do something...
```

```nim
from std/os import removeFile

var strm = newFileStream("somefile.txt", fmWrite)

doAssert "Before write:" & readFile("somefile.txt") == "Before write:"
strm.write("hello")
doAssert "After  write:" & readFile("somefile.txt") == "After  write:"

strm.flush()
doAssert "After  flush:" & readFile("somefile.txt") == "After  flush:hello"
strm.write("HELLO")
strm.flush()
doAssert "After  flush:" & readFile("somefile.txt") == "After  flush:helloHELLO"

strm.close()
doAssert "After  close:" & readFile("somefile.txt") == "After  close:helloHELLO"
removeFile("somefile.txt")
```

```nim
var strm = newStringStream("The first line\nthe second line\nthe third line")
doAssert strm.getPosition() == 0
discard strm.readLine()
doAssert strm.getPosition() == 15
strm.close()
```

```nim
## Input (somefile.txt):
## The first line
## the second line
## the third line
var f: File
if open(f, "somefile.txt", fmRead, -1):
  var strm = newFileStream(f)
  var line = ""
  while strm.readLine(line):
    echo line
  ## Output:
  ## The first line
  ## the second line
  ## the third line
  strm.close()
```

```nim
from std/os import removeFile
var strm = newFileStream("somefile.txt", fmWrite)
if not isNil(strm):
  strm.writeLine("The first line")
  strm.writeLine("the second line")
  strm.writeLine("the third line")
  strm.close()
  ## Output (somefile.txt)
  ## The first line
  ## the second line
  ## the third line
  removeFile("somefile.txt")
```

```nim
var strm = newStringStream("The first line\nthe second line\nthe third line")
doAssert strm.readLine() == "The first line"
doAssert strm.readLine() == "the second line"
doAssert strm.readLine() == "the third line"
strm.close()
```

```nim
try:
  ## Input (somefile.txt):
  ## The first line
  ## the second line
  ## the third line
  var strm = openFileStream("somefile.txt")
  echo strm.readLine()
  ## Output:
  ## The first line
  strm.close()
except:
  stderr.write getCurrentExceptionMsg()
```

```nim
var strm = newStringStream("012")
## peekInt
var i: int8
strm.peek(i)
doAssert i == 48
## peekData
var buffer: array[2, char]
strm.peek(buffer)
doAssert buffer == ['0', '1']
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(true)
strm.write(false)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekBool() == true
## not false
doAssert strm.peekBool() == true
doAssert strm.readBool() == true
doAssert strm.peekBool() == false
strm.close()
```

```nim
var strm = newStringStream("12\n3")
doAssert strm.peekChar() == '1'
doAssert strm.peekChar() == '1'
discard strm.readAll()
doAssert strm.peekChar() == '\x00'
strm.close()
```

```nim
var strm = newStringStream("abcde")
var buffer: array[6, char]
doAssert strm.peekData(addr(buffer), 1024) == 5
doAssert buffer == ['a', 'b', 'c', 'd', 'e', '\x00']
doAssert strm.atEnd() == false
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'f32)
strm.write(2'f32)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekFloat32() == 1'f32
## not 2'f32
doAssert strm.peekFloat32() == 1'f32
doAssert strm.readFloat32() == 1'f32
doAssert strm.peekFloat32() == 2'f32
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'f64)
strm.write(2'f64)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekFloat64() == 1'f64
## not 2'f64
doAssert strm.peekFloat64() == 1'f64
doAssert strm.readFloat64() == 1'f64
doAssert strm.peekFloat64() == 2'f64
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'i8)
strm.write(2'i8)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekInt8() == 1'i8
## not 2'i8
doAssert strm.peekInt8() == 1'i8
doAssert strm.readInt8() == 1'i8
doAssert strm.peekInt8() == 2'i8
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'i16)
strm.write(2'i16)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekInt16() == 1'i16
## not 2'i16
doAssert strm.peekInt16() == 1'i16
doAssert strm.readInt16() == 1'i16
doAssert strm.peekInt16() == 2'i16
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'i32)
strm.write(2'i32)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekInt32() == 1'i32
## not 2'i32
doAssert strm.peekInt32() == 1'i32
doAssert strm.readInt32() == 1'i32
doAssert strm.peekInt32() == 2'i32
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'i64)
strm.write(2'i64)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekInt64() == 1'i64
## not 2'i64
doAssert strm.peekInt64() == 1'i64
doAssert strm.readInt64() == 1'i64
doAssert strm.peekInt64() == 2'i64
strm.close()
```

```nim
var strm = newStringStream("The first line\nthe second line\nthe third line")
doAssert strm.peekLine() == "The first line"
## not "the second line"
doAssert strm.peekLine() == "The first line"
doAssert strm.readLine() == "The first line"
doAssert strm.peekLine() == "the second line"
strm.close()
```

```nim
var strm = newStringStream("The first line\nthe second line\nthe third line")
var line = ""
doAssert strm.peekLine(line) == true
doAssert line == "The first line"
doAssert strm.peekLine(line) == true
## not "the second line"
doAssert line == "The first line"
doAssert strm.readLine(line) == true
doAssert line == "The first line"
doAssert strm.peekLine(line) == true
doAssert line == "the second line"
strm.close()
```

```nim
var strm = newStringStream("abcde")
doAssert strm.peekStr(2) == "ab"
## not "cd
doAssert strm.peekStr(2) == "ab"
doAssert strm.readStr(2) == "ab"
doAssert strm.peekStr(2) == "cd"
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'u8)
strm.write(2'u8)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekUint8() == 1'u8
## not 2'u8
doAssert strm.peekUint8() == 1'u8
doAssert strm.readUint8() == 1'u8
doAssert strm.peekUint8() == 2'u8
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'u16)
strm.write(2'u16)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekUint16() == 1'u16
## not 2'u16
doAssert strm.peekUint16() == 1'u16
doAssert strm.readUint16() == 1'u16
doAssert strm.peekUint16() == 2'u16
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'u32)
strm.write(2'u32)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekUint32() == 1'u32
## not 2'u32
doAssert strm.peekUint32() == 1'u32
doAssert strm.readUint32() == 1'u32
doAssert strm.peekUint32() == 2'u32
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'u64)
strm.write(2'u64)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.peekUint64() == 1'u64
## not 2'u64
doAssert strm.peekUint64() == 1'u64
doAssert strm.readUint64() == 1'u64
doAssert strm.peekUint64() == 2'u64
strm.close()
```

```nim
var strm = newStringStream("012")
## readInt
var i: int8
strm.read(i)
doAssert i == 48
## readData
var buffer: array[2, char]
strm.read(buffer)
doAssert buffer == ['1', '2']
strm.close()
```

```nim
var strm = newStringStream("The first line\nthe second line\nthe third line")
doAssert strm.readAll() == "The first line\nthe second line\nthe third line"
doAssert strm.atEnd() == true
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(true)
strm.write(false)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.readBool() == true
doAssert strm.readBool() == false
doAssertRaises(IOError): discard strm.readBool()
strm.close()
```

```nim
var strm = newStringStream("12\n3")
doAssert strm.readChar() == '1'
doAssert strm.readChar() == '2'
doAssert strm.readChar() == '\n'
doAssert strm.readChar() == '3'
doAssert strm.readChar() == '\x00'
strm.close()
```

```nim
var strm = newStringStream("abcde")
var buffer: array[6, char]
doAssert strm.readData(addr(buffer), 1024) == 5
doAssert buffer == ['a', 'b', 'c', 'd', 'e', '\x00']
doAssert strm.atEnd() == true
strm.close()
```

```nim
var strm = newStringStream("abcde")
var buffer = "12345"
doAssert strm.readDataStr(buffer, 0..3) == 4
doAssert buffer == "abcd5"
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'f32)
strm.write(2'f32)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.readFloat32() == 1'f32
doAssert strm.readFloat32() == 2'f32
doAssertRaises(IOError): discard strm.readFloat32()
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'f64)
strm.write(2'f64)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.readFloat64() == 1'f64
doAssert strm.readFloat64() == 2'f64
doAssertRaises(IOError): discard strm.readFloat64()
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'i8)
strm.write(2'i8)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.readInt8() == 1'i8
doAssert strm.readInt8() == 2'i8
doAssertRaises(IOError): discard strm.readInt8()
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'i16)
strm.write(2'i16)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.readInt16() == 1'i16
doAssert strm.readInt16() == 2'i16
doAssertRaises(IOError): discard strm.readInt16()
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'i32)
strm.write(2'i32)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.readInt32() == 1'i32
doAssert strm.readInt32() == 2'i32
doAssertRaises(IOError): discard strm.readInt32()
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'i64)
strm.write(2'i64)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.readInt64() == 1'i64
doAssert strm.readInt64() == 2'i64
doAssertRaises(IOError): discard strm.readInt64()
strm.close()
```

```nim
var strm = newStringStream("The first line\nthe second line\nthe third line")
doAssert strm.readLine() == "The first line"
doAssert strm.readLine() == "the second line"
doAssert strm.readLine() == "the third line"
doAssertRaises(IOError): discard strm.readLine()
strm.close()
```

```nim
var strm = newStringStream("The first line\nthe second line\nthe third line")
var line = ""
doAssert strm.readLine(line) == true
doAssert line == "The first line"
doAssert strm.readLine(line) == true
doAssert line == "the second line"
doAssert strm.readLine(line) == true
doAssert line == "the third line"
doAssert strm.readLine(line) == false
doAssert line == ""
strm.close()
```

```nim
var strm = newStringStream("abcde")
doAssert strm.readStr(2) == "ab"
doAssert strm.readStr(2) == "cd"
doAssert strm.readStr(2) == "e"
doAssert strm.readStr(2) == ""
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'u8)
strm.write(2'u8)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.readUint8() == 1'u8
doAssert strm.readUint8() == 2'u8
doAssertRaises(IOError): discard strm.readUint8()
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'u16)
strm.write(2'u16)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.readUint16() == 1'u16
doAssert strm.readUint16() == 2'u16
doAssertRaises(IOError): discard strm.readUint16()
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'u32)
strm.write(2'u32)
strm.flush()
strm.setPosition(0)

## get data
doAssert strm.readUint32() == 1'u32
doAssert strm.readUint32() == 2'u32
doAssertRaises(IOError): discard strm.readUint32()
strm.close()
```

```nim
var strm = newStringStream()
## setup for reading data
strm.write(1'u64)
strm.write(2'u64)
strm.flush()
strm.setPosition(0)
## get data
doAssert strm.readUint64() == 1'u64
doAssert strm.readUint64() == 2'u64
doAssertRaises(IOError): discard strm.readUint64()
strm.close()
```

```nim
var strm = newStringStream("The first line\nthe second line\nthe third line")
strm.setPosition(4)
doAssert strm.readLine() == "first line"
strm.setPosition(0)
doAssert strm.readLine() == "The first line"
strm.close()
```

```nim
var strm = newStringStream("")
strm.write(1, 2, 3, 4)
strm.setPosition(0)
doAssert strm.readLine() == "1234"
strm.close()
```

```nim
var strm = newStringStream("")
strm.write("THE FIRST LINE")
strm.setPosition(0)
doAssert strm.readLine() == "THE FIRST LINE"
strm.close()
```

```nim
s.writeData(s, unsafeAddr(x), sizeof(x))
```

```nim
var strm = newStringStream("")
strm.write("abcde")
strm.setPosition(0)
doAssert strm.readAll() == "abcde"
strm.close()
```

```nim
## writeData
var strm = newStringStream("")
var buffer = ['a', 'b', 'c', 'd', 'e']
strm.writeData(addr(buffer), sizeof(buffer))
doAssert strm.atEnd() == true
## readData
strm.setPosition(0)
var buffer2: array[6, char]
doAssert strm.readData(addr(buffer2), sizeof(buffer2)) == 5
doAssert buffer2 == ['a', 'b', 'c', 'd', 'e', '\x00']
strm.close()
```

```nim
var strm = newStringStream("")
strm.writeLine(1, 2)
strm.writeLine(3, 4)
strm.setPosition(0)
doAssert strm.readAll() == "12\n34\n"
strm.close()
```

```nim
var strm = newStringStream("The first line\nthe second line\nthe third line")
var lines: seq[string]
for line in strm.lines():
  lines.add line
doAssert lines == @["The first line", "the second line", "the third line"]
strm.close()
```

## Iterator

### lines

[ref: #symbol-lines]

Iterates over every line in the stream. The iteration is based on readLine.

**Input:**
- `s: Stream`

**Output:** `string`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Iterates over every line in the stream. The iteration is based on readLine.

See also:

* [readLine(Stream) proc](#readLine,Stream)
* [readLine(Stream, string) proc](#readLine,Stream,string)

## Proc

### atEnd

[ref: #symbol-atend]

**Input:**
- `s: Stream`

**Output:** `bool`
**Pragmas:** `raises: [IOError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: `, `forbids: `

Checks if more data can be read from s. Returns true if all data has been read.

### close

[ref: #symbol-close]

Closes the stream s.

**Input:**
- `s: Stream`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Closes the stream s.

See also:

* [flush proc](#flush,Stream)

### flush

[ref: #symbol-flush]

Flushes the buffers that the stream s might use.

**Input:**
- `s: Stream`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Flushes the buffers that the stream s might use.

This procedure causes any unwritten data for that stream to be delivered to the host environment to be written to the file.

See also:

* [close proc](#close,Stream)

### getPosition

[ref: #symbol-getposition]

**Input:**
- `s: Stream`

**Output:** `int`
**Pragmas:** `raises: [IOError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: `, `forbids: `

Retrieves the current position in the stream s.

### newFileStream

[ref: #symbol-newfilestream]

Creates a new stream from the file f.

**Input:**
- `f: File`

**Output:** `owned FileStream`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new stream from the file f.

**Note:** Not available for JS backend.

See also:

* [newStringStream proc](#newStringStream,string) creates a new stream from string.
* [newFileStream proc](#newFileStream,string,FileMode,int) is the same as using [open proc](syncio.html#open,File,string,FileMode,int) on Examples.
* [openFileStream proc](#openFileStream,string,FileMode,int) creates a file stream from the file name and the mode.

### newFileStream

[ref: #symbol-newfilestream]

Creates a new stream from the file named filename with the mode mode.

**Input:**
- `filename: string`
- `mode: FileMode = fmRead`
- `bufSize: int = -1`

**Output:** `owned FileStream`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new stream from the file named filename with the mode mode.

If the file cannot be opened, nil is returned. See the [io module](syncio.html) for a list of available [FileMode enums](syncio.html#FileMode).

**Note:**

* **This function returns nil in case of failure.** To prevent unexpected behavior and ensure proper error handling, use [openFileStream proc](#openFileStream,string,FileMode,int) instead.
* Not available for JS backend.

See also:

* [newStringStream proc](#newStringStream,string) creates a new stream from string.
* [newFileStream proc](#newFileStream,File) creates a file stream from opened File.
* [openFileStream proc](#openFileStream,string,FileMode,int) creates a file stream from the file name and the mode.

### newStringStream

[ref: #symbol-newstringstream]

Creates a new stream from the string s.

**Input:**
- `s: sink string = ""`

**Output:** `owned StringStream`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new stream from the string s.

See also:

* [newFileStream proc](#newFileStream,File) creates a file stream from opened File.
* [newFileStream proc](#newFileStream,string,FileMode,int) creates a file stream from the file name and the mode.
* [openFileStream proc](#openFileStream,string,FileMode,int) creates a file stream from the file name and the mode.


[Next](streams_2.md)
