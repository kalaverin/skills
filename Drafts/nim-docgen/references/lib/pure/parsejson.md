---
source_hash: f05a47fe6e7f19d2
source_path: lib/pure/parsejson.nim
---

# parsejson

[ref: #module-parsejson]

This module implements a json parser. It is used and exported by the json standard library module, but can also be used in its own right.

## Const

### errorMessages

[ref: #symbol-errormessages]

```nim
errorMessages: array[JsonError, string] = ["no error", "invalid token",
    "string expected", "\':\' expected", "\',\' expected", "\']\' expected",
    "\'}\' expected", "\'\"\' or \"\'\" expected", "\'*/\' expected",
    "EOF expected", "expression expected"]
```

## Proc

### close

[ref: #symbol-close]

**Input:**
- `my: var JsonParser`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

closes the parser my and its associated input stream.

### eat

[ref: #symbol-eat]

**Input:**
- `p: var JsonParser`
- `tok: TokKind`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError, JsonParsingError, ValueError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, JsonParsingError, ValueError`, `tags: ReadIOEffect`, `forbids: `

### errorMsg

[ref: #symbol-errormsg]

**Input:**
- `my: JsonParser`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns a helpful error message for the event jsonError

### errorMsgExpected

[ref: #symbol-errormsgexpected]

**Input:**
- `my: JsonParser`
- `e: string`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns an error message "e expected" in the same format as the other error messages

### getColumn

[ref: #symbol-getcolumn]

**Input:**
- `my: JsonParser`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

get the current column the parser has arrived at.

### getFilename

[ref: #symbol-getfilename]

**Input:**
- `my: JsonParser`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

get the filename of the file that the parser processes.

### getFloat

[ref: #symbol-getfloat]

**Input:**
- `my: JsonParser`

**Output:** `float`
**Pragmas:** `inline`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns the number for the event: jsonFloat

### getInt

[ref: #symbol-getint]

**Input:**
- `my: JsonParser`

**Output:** `BiggestInt`
**Pragmas:** `inline`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns the number for the event: jsonInt

### getLine

[ref: #symbol-getline]

**Input:**
- `my: JsonParser`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

get the current line the parser has arrived at.

### getTok

[ref: #symbol-gettok]

**Input:**
- `my: var JsonParser`

**Output:** `TokKind`
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

### kind

[ref: #symbol-kind]

**Input:**
- `my: JsonParser`

**Output:** `JsonEventKind`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the current event type for the JSON parser

### next

[ref: #symbol-next]

**Input:**
- `my: var JsonParser`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

retrieves the first/next event. This controls the parser.

### open

[ref: #symbol-open]

**Input:**
- `my: var JsonParser`
- `input: Stream`
- `filename: string`
- `rawStringLiterals:  = false`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

initializes the parser with an input stream. Filename is only used for nice error messages. If rawStringLiterals is true, string literals are kept with their surrounding quotes and escape sequences in them are left untouched too.

### parseEscapedUTF16

[ref: #symbol-parseescapedutf16]

**Input:**
- `buf: cstring`
- `pos: var int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### raiseParseErr

[ref: #symbol-raiseparseerr]

**Input:**
- `p: JsonParser`
- `msg: string`

**Output:** *(none)*
**Pragmas:** `noinline`, `noreturn`, `raises: [JsonParsingError, ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: JsonParsingError, ValueError`, `tags: `, `forbids: `

raises an EJsonParsingError exception.

### str

[ref: #symbol-str]

**Input:**
- `my: JsonParser`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the character data for the events: jsonInt, jsonFloat, jsonString

## Type

### JsonError

[ref: #symbol-jsonerror]

```nim
JsonError = enum
  errNone,                  ## no error
  errInvalidToken,          ## invalid token
  errStringExpected,        ## string expected
  errColonExpected,         ## `:` expected
  errCommaExpected,         ## `,` expected
  errBracketRiExpected,     ## `]` expected
  errCurlyRiExpected,       ## `}` expected
  errQuoteExpected,         ## `"` or `'` expected
  errEOC_Expected,          ## `*/` expected
  errEofExpected,           ## EOF expected
  errExprExpected            ## expr expected
```

enumeration that lists all errors that can occur

### JsonEventKind

[ref: #symbol-jsoneventkind]

```nim
JsonEventKind = enum
  jsonError,                ## an error occurred during parsing
  jsonEof,                  ## end of file reached
  jsonString,               ## a string literal
  jsonInt,                  ## an integer literal
  jsonFloat,                ## a float literal
  jsonTrue,                 ## the value `true`
  jsonFalse,                ## the value `false`
  jsonNull,                 ## the value `null`
  jsonObjectStart,          ## start of an object: the `{` token
  jsonObjectEnd,            ## end of an object: the `}` token
  jsonArrayStart,           ## start of an array: the `[` token
  jsonArrayEnd               ## end of an array: the `]` token
```

enumeration of all events that may occur when parsing

### JsonKindError

[ref: #symbol-jsonkinderror]

```nim
JsonKindError = object of ValueError
```

raised by the to macro if the JSON kind is incorrect.

### JsonParser

[ref: #symbol-jsonparser]

```nim
JsonParser = object of BaseLexer
  a*: string
  tok*: TokKind
```

the parser object.

### JsonParsingError

[ref: #symbol-jsonparsingerror]

```nim
JsonParsingError = object of ValueError
```

is raised for a JSON error

### TokKind

[ref: #symbol-tokkind]

```nim
TokKind = enum
  tkError, tkEof, tkString, tkInt, tkFloat, tkTrue, tkFalse, tkNull, tkCurlyLe,
  tkCurlyRi, tkBracketLe, tkBracketRi, tkColon, tkComma
```
