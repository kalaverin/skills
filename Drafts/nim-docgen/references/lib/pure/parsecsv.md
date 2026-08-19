---
source_hash: 7a5efca007e69f32
source_path: lib/pure/parsecsv.nim
---

# parsecsv

[ref: #module-parsecsv]

This module implements a simple high performance CSV (comma separated value) parser.

# [Basic usage](#basic-usage)

```
import std/parsecsv
from std/os import paramStr
from std/streams import newFileStream

var s = newFileStream(paramStr(1), fmRead)
if s == nil:
  quit("cannot open the file" & paramStr(1))

var x: CsvParser
open(x, s, paramStr(1))
while readRow(x):
  echo "new row: "
  for val in items(x.row):
    echo "##", val, "##"
close(x)
```

For CSV files with a header row, the header can be read and then used as a reference for item access with [rowEntry](#rowEntry,CsvParser,string):

```
import std/parsecsv

# Prepare a file
let content = """One,Two,Three,Four
1,2,3,4
10,20,30,40
100,200,300,400
"""
writeFile("temp.csv", content)

var p: CsvParser
p.open("temp.csv")
p.readHeaderRow()
while p.readRow():
  echo "new row: "
  for col in items(p.headers):
    echo "##", col, ":", p.rowEntry(col), "##"
p.close()
```

# [See also](#see-also)

* [streams module](streams.html) for using [open proc](#open,CsvParser,Stream,string,char,char,char) and other stream processing (like [close proc](streams.html#close,Stream))
* [parseopt module](parseopt.html) for a command line parser
* [parsecfg module](parsecfg.html) for a configuration file parser
* [parsexml module](parsexml.html) for a XML / HTML parser
* [parsesql module](parsesql.html) for a SQL parser
* [other parsers](lib.html#pure-libraries-parsers) for other parsers

## Examples

```nim
import std/parsecsv
from std/os import paramStr
from std/streams import newFileStream

var s = newFileStream(paramStr(1), fmRead)
if s == nil:
  quit("cannot open the file" & paramStr(1))

var x: CsvParser
open(x, s, paramStr(1))
while readRow(x):
  echo "new row: "
  for val in items(x.row):
    echo "##", val, "##"
close(x)
```

```nim
import std/parsecsv

# Prepare a file
let content = """One,Two,Three,Four
1,2,3,4
10,20,30,40
100,200,300,400
"""
writeFile("temp.csv", content)

var p: CsvParser
p.open("temp.csv")
p.readHeaderRow()
while p.readRow():
  echo "new row: "
  for col in items(p.headers):
    echo "##", col, ":", p.rowEntry(col), "##"
p.close()
```

```nim
from std/os import removeFile
writeFile("tmp.csv", "One,Two,Three\n1,2,3\n10,20,300")
var parser: CsvParser
parser.open("tmp.csv")
parser.close()
removeFile("tmp.csv")
```

```nim
import std/streams
var strm = newStringStream("One,Two,Three\n1,2,3\n10,20,30")
var parser: CsvParser
parser.open(strm, "tmp.csv")
parser.close()
strm.close()
```

```nim
import std/streams

var strm = newStringStream("One,Two,Three\n1,2,3")
var parser: CsvParser
parser.open(strm, "tmp.csv")
doAssert parser.readRow()
doAssert parser.processedRows() == 1
doAssert parser.readRow()
doAssert parser.processedRows() == 2
## Even if `readRow` arrived at EOF then `processedRows` is incremented.
doAssert parser.readRow() == false
doAssert parser.processedRows() == 3
doAssert parser.readRow() == false
doAssert parser.processedRows() == 4
parser.close()
strm.close()
```

```nim
import std/streams

var strm = newStringStream("One,Two,Three\n1,2,3")
var parser: CsvParser
parser.open(strm, "tmp.csv")

parser.readHeaderRow()
doAssert parser.headers == @["One", "Two", "Three"]
doAssert parser.row == @["One", "Two", "Three"]

doAssert parser.readRow()
doAssert parser.headers == @["One", "Two", "Three"]
doAssert parser.row == @["1", "2", "3"]

parser.close()
strm.close()
```

```nim
import std/streams
var strm = newStringStream("One,Two,Three\n1,2,3\n\n10,20,30")
var parser: CsvParser
parser.open(strm, "tmp.csv")
doAssert parser.readRow()
doAssert parser.row == @["One", "Two", "Three"]
doAssert parser.readRow()
doAssert parser.row == @["1", "2", "3"]
## Blank lines are skipped.
doAssert parser.readRow()
doAssert parser.row == @["10", "20", "30"]

var emptySeq: seq[string]
doAssert parser.readRow() == false
doAssert parser.row == emptySeq
doAssert parser.readRow() == false
doAssert parser.row == emptySeq

parser.close()
strm.close()
```

```nim
import std/streams
var strm = newStringStream("One,Two,Three\n1,2,3\n\n10,20,30")
var parser: CsvParser
parser.open(strm, "tmp.csv")
## Requires calling `readHeaderRow`.
parser.readHeaderRow()
doAssert parser.readRow()
doAssert parser.rowEntry("One") == "1"
doAssert parser.rowEntry("Two") == "2"
doAssert parser.rowEntry("Three") == "3"
doAssertRaises(KeyError):
  discard parser.rowEntry("NonexistentEntry")
parser.close()
strm.close()
```

## Proc

### close

[ref: #symbol-close]

**Input:**
- `self: var CsvParser`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

Closes the parser self and its associated input stream.

### open

[ref: #symbol-open]

Initializes the parser with an input stream. Filename is only used for nice error messages. The parser's behaviour can be controlled by the diverse optional parameters:

**Input:**
- `self: var CsvParser`
- `input: Stream`
- `filename: string`
- `separator:  = ','`
- `quote:  = '\"'`
- `escape:  = '\x00'`
- `skipInitialSpace:  = false`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Initializes the parser with an input stream. Filename is only used for nice error messages. The parser's behaviour can be controlled by the diverse optional parameters:

* separator: character used to separate fields
* quote: Used to quote fields containing special characters like separator, quote or new-line characters. '\0' disables the parsing of quotes.
* escape: removes any special meaning from the following character; '\0' disables escaping; if escaping is disabled and quote is not '\0', two quote characters are parsed one literal quote character.
* skipInitialSpace: If true, whitespace immediately following the separator is ignored.

See also:

* [open proc](#open,CsvParser,string,char,char,char) which creates the file stream for you

### open

[ref: #symbol-open]

**Input:**
- `self: var CsvParser`
- `filename: string`
- `separator:  = ','`
- `quote:  = '\"'`
- `escape:  = '\x00'`
- `skipInitialSpace:  = false`

**Output:** *(none)*
**Pragmas:** `raises: [CsvError, IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: CsvError, IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Similar to the [other open proc](#open,CsvParser,Stream,string,char,char,char), but creates the file stream for you.

### processedRows

[ref: #symbol-processedrows]

Returns number of the processed rows.

**Input:**
- `self: var CsvParser`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns number of the processed rows.

But even if [readRow](#readRow,CsvParser,int) arrived at EOF then processed rows counter is incremented.

### readHeaderRow

[ref: #symbol-readheaderrow]

Reads the first row and creates a look-up table for column numbers See also:

**Input:**
- `self: var CsvParser`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError, CsvError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, CsvError`, `tags: ReadIOEffect`, `forbids: `

Reads the first row and creates a look-up table for column numbers See also:

* [rowEntry proc](#rowEntry,CsvParser,string)

### readRow

[ref: #symbol-readrow]

Reads the next row; if columns > 0, it expects the row to have exactly this many columns. Returns false if the end of the file has been encountered else true.

**Input:**
- `self: var CsvParser`
- `columns:  = 0`

**Output:** `bool`
**Pragmas:** `raises: [IOError, OSError, CsvError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, CsvError`, `tags: ReadIOEffect`, `forbids: `

Reads the next row; if columns > 0, it expects the row to have exactly this many columns. Returns false if the end of the file has been encountered else true.

Blank lines are skipped.

### rowEntry

[ref: #symbol-rowentry]

Accesses a specified entry from the current row.

**Input:**
- `self: var CsvParser`
- `entry: string`

**Output:** `var string`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Accesses a specified entry from the current row.

Assumes that [readHeaderRow](#readHeaderRow,CsvParser) has already been called.

If specified entry does not exist, raises KeyError.

## Type

### CsvError

[ref: #symbol-csverror]

```nim
CsvError = object of IOError
```

An exception that is raised if a parsing error occurs.

### CsvParser

[ref: #symbol-csvparser]

The parser object.

```nim
CsvParser = object of BaseLexer
  row*: CsvRow
  headers*: seq[string]
```

The parser object.

It consists of two public fields:

* row is the current row
* headers are the columns that are defined in the csv file (read using [readHeaderRow](#readHeaderRow,CsvParser)). Used with [rowEntry](#rowEntry,CsvParser,string)).

### CsvRow

[ref: #symbol-csvrow]

```nim
CsvRow = seq[string]
```

A row in a CSV file.
