---
source_hash: b369e8146afa8f75
source_path: lib/pure/parsexml.nim
---

# parsexml

[ref: #module-parsexml]

This module implements a simple high performance XML / HTML parser. The only encoding that is supported is UTF-8. The parser has been designed to be somewhat error correcting, so that even most "wild HTML" found on the web can be parsed with it. **Note:** This parser does not check that each <tag> has a corresponding </tag>! These checks have do be implemented by the client code for various reasons:

* Old HTML contains tags that have no end tag: <br> for example.
* HTML tags are case insensitive, XML tags are case sensitive. Since this library can parse both, only the client knows which comparison is to be used.
* Thus the checks would have been very difficult to implement properly with little benefit, especially since they are simple to implement in the client. The client should use the errorMsgExpected proc to generate a nice error message that fits the other error messages this library creates.

# [Example 1: Retrieve HTML title](#example-1colon-retrieve-html-title)

The file examples/htmltitle.nim demonstrates how to use the XML parser to accomplish a simple task: To determine the title of an HTML document.

```
# Example program to show the parsexml module
# This program reads an HTML file and writes its title to stdout.
# Errors and whitespace are ignored.

import std/[os, streams, parsexml, strutils]

if paramCount() < 1:
  quit("Usage: htmltitle filename[.html]")

var filename = addFileExt(paramStr(1), "html")
var s = newFileStream(filename, fmRead)
if s == nil: quit("cannot open the file " & filename)
var x: XmlParser
open(x, s, filename)
while true:
  x.next()
  case x.kind
  of xmlElementStart:
    if cmpIgnoreCase(x.elementName, "title") == 0:
      var title = ""
      x.next()  # skip "<title>"
      while x.kind == xmlCharData:
        title.add(x.charData)
        x.next()
      if x.kind == xmlElementEnd and cmpIgnoreCase(x.elementName, "title") == 0:
        echo("Title: " & title)
        quit(0) # Success!
      else:
        echo(x.errorMsgExpected("/title"))
  
  of xmlEof: break # end of file reached
  else: discard # ignore other events

x.close()
quit("Could not determine title!")
```

# [Example 2: Retrieve all HTML links](#example-2colon-retrieve-all-html-links)

The file examples/htmlrefs.nim demonstrates how to use the XML parser to accomplish another simple task: To determine all the links an HTML document contains.

```
# Example program to show the new parsexml module
# This program reads an HTML file and writes all its used links to stdout.
# Errors and whitespace are ignored.

import std/[os, streams, parsexml, strutils]

proc `=?=` (a, b: string): bool =
  # little trick: define our own comparator that ignores case
  return cmpIgnoreCase(a, b) == 0

if paramCount() < 1:
  quit("Usage: htmlrefs filename[.html]")

var links = 0 # count the number of links
var filename = addFileExt(paramStr(1), "html")
var s = newFileStream(filename, fmRead)
if s == nil: quit("cannot open the file " & filename)
var x: XmlParser
open(x, s, filename)
next(x) # get first event
block mainLoop:
  while true:
    case x.kind
    of xmlElementOpen:
      # the <a href = "xyz"> tag we are interested in always has an attribute,
      # thus we search for ``xmlElementOpen`` and not for ``xmlElementStart``
      if x.elementName =?= "a":
        x.next()
        if x.kind == xmlAttribute:
          if x.attrKey =?= "href":
            var link = x.attrValue
            inc(links)
            # skip until we have an ``xmlElementClose`` event
            while true:
              x.next()
              case x.kind
              of xmlEof: break mainLoop
              of xmlElementClose: break
              else: discard
            x.next() # skip ``xmlElementClose``
            # now we have the description for the ``a`` element
            var desc = ""
            while x.kind == xmlCharData:
              desc.add(x.charData)
              x.next()
            echo(desc & ": " & link)
      else:
        x.next()
    of xmlEof: break # end of file reached
    of xmlError:
      echo(errorMsg(x))
      x.next()
    else: x.next() # skip other events

echo($links & " link(s) found!")
x.close()
```

## Examples

```nim
# Example program to show the parsexml module
# This program reads an HTML file and writes its title to stdout.
# Errors and whitespace are ignored.

import std/[os, streams, parsexml, strutils]

if paramCount() < 1:
  quit("Usage: htmltitle filename[.html]")

var filename = addFileExt(paramStr(1), "html")
var s = newFileStream(filename, fmRead)
if s == nil: quit("cannot open the file " & filename)
var x: XmlParser
open(x, s, filename)
while true:
  x.next()
  case x.kind
  of xmlElementStart:
    if cmpIgnoreCase(x.elementName, "title") == 0:
      var title = ""
      x.next()  # skip "<title>"
      while x.kind == xmlCharData:
        title.add(x.charData)
        x.next()
      if x.kind == xmlElementEnd and cmpIgnoreCase(x.elementName, "title") == 0:
        echo("Title: " & title)
        quit(0) # Success!
      else:
        echo(x.errorMsgExpected("/title"))
  
  of xmlEof: break # end of file reached
  else: discard # ignore other events

x.close()
quit("Could not determine title!")
```

```nim
# Example program to show the new parsexml module
# This program reads an HTML file and writes all its used links to stdout.
# Errors and whitespace are ignored.

import std/[os, streams, parsexml, strutils]

proc `=?=` (a, b: string): bool =
  # little trick: define our own comparator that ignores case
  return cmpIgnoreCase(a, b) == 0

if paramCount() < 1:
  quit("Usage: htmlrefs filename[.html]")

var links = 0 # count the number of links
var filename = addFileExt(paramStr(1), "html")
var s = newFileStream(filename, fmRead)
if s == nil: quit("cannot open the file " & filename)
var x: XmlParser
open(x, s, filename)
next(x) # get first event
block mainLoop:
  while true:
    case x.kind
    of xmlElementOpen:
      # the <a href = "xyz"> tag we are interested in always has an attribute,
      # thus we search for ``xmlElementOpen`` and not for ``xmlElementStart``
      if x.elementName =?= "a":
        x.next()
        if x.kind == xmlAttribute:
          if x.attrKey =?= "href":
            var link = x.attrValue
            inc(links)
            # skip until we have an ``xmlElementClose`` event
            while true:
              x.next()
              case x.kind
              of xmlEof: break mainLoop
              of xmlElementClose: break
              else: discard
            x.next() # skip ``xmlElementClose``
            # now we have the description for the ``a`` element
            var desc = ""
            while x.kind == xmlCharData:
              desc.add(x.charData)
              x.next()
            echo(desc & ": " & link)
      else:
        x.next()
    of xmlEof: break # end of file reached
    of xmlError:
      echo(errorMsg(x))
      x.next()
    else: x.next() # skip other events

echo($links & " link(s) found!")
x.close()
```

## Proc

### close

[ref: #symbol-close]

**Input:**
- `my: var XmlParser`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

closes the parser my and its associated input stream.

### errorMsg

[ref: #symbol-errormsg]

**Input:**
- `my: XmlParser`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns a helpful error message for the event xmlError

### errorMsg

[ref: #symbol-errormsg]

**Input:**
- `my: XmlParser`
- `msg: string`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns an error message with text msg in the same format as the other error messages

### errorMsgExpected

[ref: #symbol-errormsgexpected]

**Input:**
- `my: XmlParser`
- `tag: string`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns an error message "<tag> expected" in the same format as the other error messages

### getColumn

[ref: #symbol-getcolumn]

**Input:**
- `my: XmlParser`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

get the current column the parser has arrived at.

### getFilename

[ref: #symbol-getfilename]

**Input:**
- `my: XmlParser`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

get the filename of the file that the parser processes.

### getLine

[ref: #symbol-getline]

**Input:**
- `my: XmlParser`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

get the current line the parser has arrived at.

### kind

[ref: #symbol-kind]

**Input:**
- `my: XmlParser`

**Output:** `XmlEventKind`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the current event type for the XML parser

### next

[ref: #symbol-next]

**Input:**
- `my: var XmlParser`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

retrieves the first/next event. This controls the parser.

### open

[ref: #symbol-open]

**Input:**
- `my: var XmlParser`
- `input: Stream`
- `filename: string`
- `options: set[XmlParseOption] = {}`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

initializes the parser with an input stream. Filename is only used for nice error messages. The parser's behaviour can be controlled by the options parameter: If options contains reportWhitespace a whitespace token is reported as an xmlWhitespace event. If options contains reportComments a comment token is reported as an xmlComment event.

### rawData

[ref: #symbol-rawdata]

**Input:**
- `my: var XmlParser`

**Output:** `lent string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the underlying 'data' string by reference. This is only used for speed hacks.

### rawData2

[ref: #symbol-rawdata2]

**Input:**
- `my: var XmlParser`

**Output:** `lent string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the underlying second 'data' string by reference. This is only used for speed hacks.

## Template

### attrKey

[ref: #symbol-attrkey]

**Input:**
- `my: XmlParser`

**Output:** `string`
returns the attribute key for the event xmlAttribute Raises an assertion in debug mode if my.kind is not xmlAttribute. In release mode, this will not trigger an error but the value returned will not be valid.

### attrValue

[ref: #symbol-attrvalue]

**Input:**
- `my: XmlParser`

**Output:** `string`
returns the attribute value for the event xmlAttribute Raises an assertion in debug mode if my.kind is not xmlAttribute. In release mode, this will not trigger an error but the value returned will not be valid.

### charData

[ref: #symbol-chardata]

**Input:**
- `my: XmlParser`

**Output:** `string`
returns the character data for the events: xmlCharData, xmlWhitespace, xmlComment, xmlCData, xmlSpecial Raises an assertion in debug mode if my.kind is not one of those events. In release mode, this will not trigger an error but the value returned will not be valid.

### elementName

[ref: #symbol-elementname]

**Input:**
- `my: XmlParser`

**Output:** `string`
returns the element name for the events: xmlElementStart, xmlElementEnd, xmlElementOpen Raises an assertion in debug mode if my.kind is not one of those events. In release mode, this will not trigger an error but the value returned will not be valid.

### entityName

[ref: #symbol-entityname]

**Input:**
- `my: XmlParser`

**Output:** `string`
returns the entity name for the event: xmlEntity Raises an assertion in debug mode if my.kind is not xmlEntity. In release mode, this will not trigger an error but the value returned will not be valid.

### piName

[ref: #symbol-piname]

**Input:**
- `my: XmlParser`

**Output:** `string`
returns the processing instruction name for the event xmlPI Raises an assertion in debug mode if my.kind is not xmlPI. In release mode, this will not trigger an error but the value returned will not be valid.

### piRest

[ref: #symbol-pirest]

**Input:**
- `my: XmlParser`

**Output:** `string`
returns the rest of the processing instruction for the event xmlPI Raises an assertion in debug mode if my.kind is not xmlPI. In release mode, this will not trigger an error but the value returned will not be valid.

## Type

### XmlErrorKind

[ref: #symbol-xmlerrorkind]

```nim
XmlErrorKind = enum
  errNone,                  ## no error
  errEndOfCDataExpected,    ## ``]]>`` expected
  errNameExpected,          ## name expected
  errSemicolonExpected,     ## ``;`` expected
  errQmGtExpected,          ## ``?>`` expected
  errGtExpected,            ## ``>`` expected
  errEqExpected,            ## ``=`` expected
  errQuoteExpected,         ## ``"`` or ``'`` expected
  errEndOfCommentExpected,  ## ``-->`` expected
  errAttributeValueExpected  ## non-empty attribute value expected
```

enumeration that lists all errors that can occur

### XmlEventKind

[ref: #symbol-xmleventkind]

```nim
XmlEventKind = enum
  xmlError,                 ## an error occurred during parsing
  xmlEof,                   ## end of file reached
  xmlCharData,              ## character data
  xmlWhitespace,            ## whitespace has been parsed
  xmlComment,               ## a comment has been parsed
  xmlPI,                    ## processing instruction (``<?name something ?>``)
  xmlElementStart,          ## ``<elem>``
  xmlElementEnd,            ## ``</elem>``
  xmlElementOpen,           ## ``<elem
  xmlAttribute,             ## ``key = "value"`` pair
  xmlElementClose,          ## ``>``
  xmlCData,                 ## ``<![CDATA[`` ... data ... ``]]>``
  xmlEntity,                ## &entity;
  xmlSpecial                 ## ``<! ... data ... >``
```

enumeration of all events that may occur when parsing

### XmlParseOption

[ref: #symbol-xmlparseoption]

```nim
XmlParseOption = enum
  reportWhitespace,         ## report whitespace
  reportComments,           ## report comments
  allowUnquotedAttribs,     ## allow unquoted attribute values (for HTML)
  allowEmptyAttribs          ## allow empty attributes (without explicit value)
```

options for the XML parser

### XmlParser

[ref: #symbol-xmlparser]

```nim
XmlParser = object of BaseLexer
```

the parser object.
