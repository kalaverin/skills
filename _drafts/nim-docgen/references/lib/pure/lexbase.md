---
source_hash: ae288660babbe552
source_path: lib/pure/lexbase.nim
---

# lexbase

[ref: #module-lexbase]

This module implements a base object of a lexer with efficient buffer handling. Only at line endings checks are necessary if the buffer needs refilling.

## Const

### EndOfFile

[ref: #symbol-endoffile]

```nim
EndOfFile = '\x00'
```

end of file marker

### NewLines

[ref: #symbol-newlines]

```nim
NewLines = {'\r', '\n'}
```

## Proc

### close

[ref: #symbol-close]

**Input:**
- `L: var BaseLexer`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

closes the base lexer. This closes L's associated stream too.

### getColNumber

[ref: #symbol-getcolnumber]

**Input:**
- `L: BaseLexer`
- `pos: int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

retrieves the current column.

### getCurrentLine

[ref: #symbol-getcurrentline]

**Input:**
- `L: BaseLexer`
- `marker: bool = true`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

retrieves the current line.

### handleCR

[ref: #symbol-handlecr]

**Input:**
- `L: var BaseLexer`
- `pos: int`

**Output:** `int`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Call this if you scanned over '\c' in the buffer; it returns the position to continue the scanning from. pos must be the position of the '\c'.

### handleLF

[ref: #symbol-handlelf]

**Input:**
- `L: var BaseLexer`
- `pos: int`

**Output:** `int`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Call this if you scanned over '\L' in the buffer; it returns the position to continue the scanning from. pos must be the position of the '\L'.

### handleRefillChar

[ref: #symbol-handlerefillchar]

**Input:**
- `L: var BaseLexer`
- `pos: int`

**Output:** `int`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

Call this if a terminator character other than a new line is scanned at pos; it returns the position to continue the scanning from.

### open

[ref: #symbol-open]

**Input:**
- `L: var BaseLexer`
- `input: Stream`
- `bufLen: int = 8192`
- `refillChars: set[char] = NewLines`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

inits the BaseLexer with a stream to read from.

## Type

### BaseLexer

[ref: #symbol-baselexer]

```nim
BaseLexer = object of RootObj
  bufpos*: int               ## the current position within the buffer
  buf*: string               ## the buffer itself
  lineNumber*: int           ## the current line number
  offsetBase*: int
```

the base lexer. Inherit your lexer from this object.
