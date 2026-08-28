---
source_hash: d87af7c4a79b060e
source_path: lib/pure/xmlparser.nim
---

# xmlparser

[ref: #module-xmlparser]

This module parses an XML document and creates its XML tree representation.

## Proc

### loadXml

[ref: #symbol-loadxml]

**Input:**
- `path: string`
- `errors: var seq[string]`
- `options: set[XmlParseOption] = {reportComments}`

**Output:** `XmlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, Exception]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, Exception`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Loads and parses XML from file specified by path, and returns a XmlNode. Every occurred parsing error is added to the errors sequence.

### loadXml

[ref: #symbol-loadxml]

**Input:**
- `path: string`
- `options: set[XmlParseOption] = {reportComments}`

**Output:** `XmlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, Exception, XmlError]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, Exception, XmlError`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Loads and parses XML from file specified by path, and returns a XmlNode. All parsing errors are turned into an XmlError exception.

### parseXml

[ref: #symbol-parsexml]

**Input:**
- `s: Stream`
- `filename: string`
- `errors: var seq[string]`
- `options: set[XmlParseOption] = {reportComments}`

**Output:** `XmlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, Exception]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, Exception`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Parses the XML from stream s and returns a XmlNode. Every occurred parsing error is added to the errors sequence.

### parseXml

[ref: #symbol-parsexml]

**Input:**
- `s: Stream`
- `options: set[XmlParseOption] = {reportComments}`

**Output:** `XmlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, Exception, XmlError]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, Exception, XmlError`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Parses the XML from stream s and returns a XmlNode. All parsing errors are turned into an XmlError exception.

### parseXml

[ref: #symbol-parsexml]

**Input:**
- `str: string`
- `options: set[XmlParseOption] = {reportComments}`

**Output:** `XmlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, Exception, XmlError]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, Exception, XmlError`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Parses the XML from string str and returns a XmlNode. All parsing errors are turned into an XmlError exception.

## Type

### XmlError

[ref: #symbol-xmlerror]

```nim
XmlError = object of ValueError
  errors*: seq[string]       ## All detected parsing errors.
```

Exception that is raised for invalid XML.
