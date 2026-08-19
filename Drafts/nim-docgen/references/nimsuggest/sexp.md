---
source_hash: fb57c058035917c7
source_path: nimsuggest/sexp.nim
---

# sexp

[ref: #module-sexp]

**Note:** Import nimsuggest/sexp to use this module

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `node: SexpNode`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterator for the items of node. node has to be a SList.

### mitems

[ref: #symbol-mitems]

**Input:**
- `node: var SexpNode`

**Output:** `var SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterator for the items of node. node has to be a SList. Items can be modified.

## Macro

### convertSexp

[ref: #symbol-convertsexp]

**Input:**
- `x: untyped`

**Output:** `untyped`
Convert an expression to a SexpNode directly, without having to specify % for every element.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `node: SexpNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts node to its SEXP Representation on one line.

### `==`

[ref: #symbol-]

**Input:**
- `a: SexpNode`
- `b: SexpNode`

**Output:** `bool`
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Check two nodes for equality

### `[]`

[ref: #symbol-]

**Input:**
- `node: SexpNode`
- `index: int`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the node at index in a List. Result is undefined if index is out of bounds

### add

[ref: #symbol-add]

**Input:**
- `father: SexpNode`
- `child: SexpNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds child to a SList node father.

### close

[ref: #symbol-close]

**Input:**
- `my: var SexpParser`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: [IOError, OSError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: WriteIOEffect`, `forbids: `

closes the parser my and its associated input stream.

### copy

[ref: #symbol-copy]

**Input:**
- `p: SexpNode`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Performs a deep copy of a.

### errorMsg

[ref: #symbol-errormsg]

**Input:**
- `my: SexpParser`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns a helpful error message for the event sexpError

### errorMsgExpected

[ref: #symbol-errormsgexpected]

**Input:**
- `my: SexpParser`
- `e: string`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns an error message "e expected" in the same format as the other error messages

### escapeJson

[ref: #symbol-escapejson]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a string s to its JSON representation.

### getColumn

[ref: #symbol-getcolumn]

**Input:**
- `my: SexpParser`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

get the current column the parser has arrived at.

### getCons

[ref: #symbol-getcons]

Retrieves the cons value of a SList SexpNode.

**Input:**
- `n: SexpNode`
- `defaults: Cons = (newSNil(), newSNil())`

**Output:** `Cons`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the cons value of a SList SexpNode.

Returns default if n is not a SList.

### getElems

[ref: #symbol-getelems]

Retrieves the int value of a SList SexpNode.

**Input:**
- `n: SexpNode`
- `default: seq[SexpNode] = @[]`

**Output:** `seq[SexpNode]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the int value of a SList SexpNode.

Returns default if n is not a SList.

### getFloat

[ref: #symbol-getfloat]

**Input:**
- `my: SexpParser`

**Output:** `float`
**Pragmas:** `inline`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns the number for the event: sexpFloat

### getFNum

[ref: #symbol-getfnum]

Retrieves the float value of a SFloat SexpNode.

**Input:**
- `n: SexpNode`
- `default: float = 0.0`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the float value of a SFloat SexpNode.

Returns default if n is not a SFloat.

### getInt

[ref: #symbol-getint]

**Input:**
- `my: SexpParser`

**Output:** `BiggestInt`
**Pragmas:** `inline`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

returns the number for the event: sexpInt

### getLine

[ref: #symbol-getline]

**Input:**
- `my: SexpParser`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

get the current line the parser has arrived at.

### getNum

[ref: #symbol-getnum]

Retrieves the int value of a SInt SexpNode.

**Input:**
- `n: SexpNode`
- `default: BiggestInt = 0`

**Output:** `BiggestInt`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the int value of a SInt SexpNode.

Returns default if n is not a SInt.

### getStr

[ref: #symbol-getstr]

Retrieves the string value of a SString SexpNode.

**Input:**
- `n: SexpNode`
- `default: string = ""`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the string value of a SString SexpNode.

Returns default if n is not a SString.

### getSymbol

[ref: #symbol-getsymbol]

Retrieves the int value of a SList SexpNode.

**Input:**
- `n: SexpNode`
- `default: string = ""`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the int value of a SList SexpNode.

Returns default if n is not a SList.

### hash

[ref: #symbol-hash]

**Input:**
- `n: SexpNode`

**Output:** `Hash`
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Compute the hash for a SEXP node

### kind

[ref: #symbol-kind]

**Input:**
- `my: SexpParser`

**Output:** `SexpEventKind`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the current event type for the SEXP parser

### len

[ref: #symbol-len]

**Input:**
- `n: SexpNode`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

If n is a SList, it returns the number of elements. If n is a JObject, it returns the number of pairs. Else it returns 0.

### newSCons

[ref: #symbol-newscons]

**Input:**
- `car: SexpNode`
- `cdr: SexpNode`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new SCons SexpNode

### newSFloat

[ref: #symbol-newsfloat]

**Input:**
- `n: float`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new SFloat SexpNode.

### newSInt

[ref: #symbol-newsint]

**Input:**
- `n: BiggestInt`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new SInt SexpNode.

### newSList

[ref: #symbol-newslist]

**Input:**
- *(none)*

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new SList SexpNode

### newSNil

[ref: #symbol-newsnil]

**Input:**
- *(none)*

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new SNil SexpNode.

### newSString

[ref: #symbol-newsstring]

**Input:**
- `s: string`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new SString SexpNode.

### newSSymbol

[ref: #symbol-newssymbol]

**Input:**
- `s: string`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### open

[ref: #symbol-open]

**Input:**
- `my: var SexpParser`
- `input: Stream`

**Output:** *(none)*
**Pragmas:** `raises: [IOError, OSError]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError`, `tags: ReadIOEffect`, `forbids: `

initializes the parser with an input stream.

### parseSexp

[ref: #symbol-parsesexp]

**Input:**
- `s: Stream`

**Output:** `SexpNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, SexpParsingError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, SexpParsingError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Parses from a buffer s into a SexpNode.

### parseSexp

[ref: #symbol-parsesexp]

**Input:**
- `buffer: string`

**Output:** `SexpNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, SexpParsingError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, SexpParsingError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Parses Sexp from buffer.

### pretty

[ref: #symbol-pretty]

**Input:**
- `node: SexpNode`
- `indent:  = 2`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts node to its Sexp Representation, with indentation and on multiple lines.

### raiseParseErr

[ref: #symbol-raiseparseerr]

**Input:**
- `p: SexpParser`
- `msg: string`

**Output:** *(none)*
**Pragmas:** `noinline`, `noreturn`, `raises: [SexpParsingError, ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: SexpParsingError, ValueError`, `tags: `, `forbids: `

raises an ESexpParsingError exception.

### sexp

[ref: #symbol-sexp]

**Input:**
- `s: string`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for SEXP data. Creates a new SString SexpNode.

### sexp

[ref: #symbol-sexp]

**Input:**
- `n: BiggestInt`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for SEXP data. Creates a new SInt SexpNode.

### sexp

[ref: #symbol-sexp]

**Input:**
- `n: float`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for SEXP data. Creates a new SFloat SexpNode.

### sexp

[ref: #symbol-sexp]

**Input:**
- `b: bool`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for SEXP data. Creates a new SSymbol SexpNode with value t or SNil SexpNode.

### sexp

[ref: #symbol-sexp]

**Input:**
- `elements: openArray[SexpNode]`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for SEXP data. Creates a new SList SexpNode

### sexp

[ref: #symbol-sexp]

**Input:**
- `s: SexpNode`

**Output:** `SexpNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### str

[ref: #symbol-str]

**Input:**
- `my: SexpParser`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the character data for the events: sexpInt, sexpFloat, sexpString

## Type

### SexpError

[ref: #symbol-sexperror]

```nim
SexpError = enum
  errNone,                  ## no error
  errInvalidToken,          ## invalid token
  errParensRiExpected,      ## ``)`` expected
  errQuoteExpected,         ## ``"`` expected
  errEofExpected             ## EOF expected
```

enumeration that lists all errors that can occur

### SexpEventKind

[ref: #symbol-sexpeventkind]

```nim
SexpEventKind = enum
  sexpError,                ## an error occurred during parsing
  sexpEof,                  ## end of file reached
  sexpString,               ## a string literal
  sexpSymbol,               ## a symbol
  sexpInt,                  ## an integer literal
  sexpFloat,                ## a float literal
  sexpNil,                  ## the value ``nil``
  sexpDot,                  ## the dot to separate car/cdr
  sexpListStart,            ## start of a list: the ``(`` token
  sexpListEnd                ## end of a list: the ``)`` token
```

enumeration of all events that may occur when parsing

### SexpNode

[ref: #symbol-sexpnode]

```nim
SexpNode = ref SexpNodeObj
```

SEXP node

### SexpNodeKind

[ref: #symbol-sexpnodekind]

```nim
SexpNodeKind = enum
  SNil, SInt, SFloat, SString, SSymbol, SList, SCons
```

possible SEXP node types

### SexpNodeObj

[ref: #symbol-sexpnodeobj]

```nim
SexpNodeObj {.acyclic.} = object
  case kind*: SexpNodeKind
  of SString:
    str*: string
  of SSymbol:
    symbol*: string
  of SInt:
    num*: BiggestInt
  of SFloat:
    fnum*: float
  of SList:
    elems*: seq[SexpNode]
  of SCons:
  of SNil:
    nil
```

### SexpParser

[ref: #symbol-sexpparser]

```nim
SexpParser = object of BaseLexer
```

the parser object.

### SexpParsingError

[ref: #symbol-sexpparsingerror]

```nim
SexpParsingError = object of ValueError
```

is raised for a SEXP error
