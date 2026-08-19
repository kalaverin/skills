---
source_hash: 945b3db34022b93b
source_path: lib/packages/docutils/rst.nim
---

# rst

[ref: #module-rst]

This module implements a reStructuredText (RST) and Markdown parser. User's manual on supported markup syntax and command line usage can be found in [Nim-flavored Markdown and reStructuredText](markdown_rst.html).

* See also [Nim DocGen Tools Guide](docgen.html) for handling of .nim files.
* See also [packages/docutils/rstgen module](rstgen.html) to know how to generate HTML or Latex strings (for embedding them into custom documents).

Choice between Markdown and RST as well as optional additional features are turned on by passing options: [RstParseOptions](#RstParseOptions) to [proc rstParse](#proc rstParse).

## Const

### ColRstInit

[ref: #symbol-colrstinit]

```nim
ColRstInit = 0
```

Initial column number for standalone RST text (Nim global reporting adds ColOffset=1)

### ColRstOffset

[ref: #symbol-colrstoffset]

```nim
ColRstOffset = 1
```

1: a replica of ColOffset for internal use

### LineRstInit

[ref: #symbol-linerstinit]

```nim
LineRstInit = 1
```

Initial line number for standalone RST text

## Proc

### addAnchorNim

[ref: #symbol-addanchornim]

**Input:**
- `s: var PRstSharedState`
- `external: bool`
- `refn: string`
- `tooltip: string`
- `langSym: LangSymbol`
- `priority: int`
- `info: TLineInfo`
- `module: FileIndex`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds an anchor refn, which follows the rule arNim (i.e. a symbol in \*.nim file)

### addFilename

[ref: #symbol-addfilename]

**Input:**
- `s: PRstSharedState`
- `file1: string`

**Output:** `FileIndex`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns index of filename, adding it if it has not been used before

### addNodes

[ref: #symbol-addnodes]

**Input:**
- `n: PRstNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### completePass2

[ref: #symbol-completepass2]

**Input:**
- `s: PRstSharedState`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception`, `tags: RootEffect`, `forbids: `

### defaultFindFile

[ref: #symbol-defaultfindfile]

**Input:**
- `filename: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadDirEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadDirEffect`, `forbids: `

### defaultFindRefFile

[ref: #symbol-defaultfindreffile]

**Input:**
- `filename: string`

**Output:** `(string, string)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### defaultMsgHandler

[ref: #symbol-defaultmsghandler]

**Input:**
- `filename: string`
- `line: int`
- `col: int`
- `msgkind: MsgKind`
- `arg: string`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError, EParseError, IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: ValueError, EParseError, IOError`, `tags: WriteIOEffect`, `forbids: `

### getArgument

[ref: #symbol-getargument]

**Input:**
- `n: PRstNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getFieldValue

[ref: #symbol-getfieldvalue]

**Input:**
- `n: PRstNode`
- `fieldname: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getFieldValue

[ref: #symbol-getfieldvalue]

Returns the value of a specific rnField node.

**Input:**
- `n: PRstNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the value of a specific rnField node.

This proc will assert if the node is not of the expected type. The empty string will be returned as a minimum. Any value in the rst will be stripped form leading/trailing whitespace.

### newRstSharedState

[ref: #symbol-newrstsharedstate]

**Input:**
- `options: RstParseOptions`
- `filename: string`
- `findFile: FindFileHandler`
- `findRefFile: FindRefFileHandler`
- `msgHandler: MsgHandler`
- `hasToc: bool`

**Output:** `PRstSharedState`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### preparePass2

[ref: #symbol-preparepass2]

**Input:**
- `s: var PRstSharedState`
- `mainNode: PRstNode`
- `importdoc:  = true`

**Output:** *(none)*
**Pragmas:** `raises: [Exception, ValueError, KeyError]`, `tags: [RootEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, KeyError`, `tags: RootEffect, ReadIOEffect`, `forbids: `

Records titles in node mainNode and orders footnotes.

### resolveSubs

[ref: #symbol-resolvesubs]

**Input:**
- `s: PRstSharedState`
- `n: PRstNode`

**Output:** `PRstNode`
**Pragmas:** `raises: [ValueError, Exception, KeyError]`, `tags: [ReadEnvEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception, KeyError`, `tags: ReadEnvEffect, RootEffect`, `forbids: `

Makes pass 2 of RST parsing. Resolves substitutions and anchor aliases, groups footnotes. Takes input node n and returns the same node with recursive substitutions in n.sons to result.

### rstMessage

[ref: #symbol-rstmessage]

**Input:**
- `filenames: RstFileTable`
- `f: MsgHandler`
- `info: TLineInfo`
- `msgKind: MsgKind`
- `arg: string`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, Exception`, `tags: RootEffect`, `forbids: `

Print warnings using info, i.e. in 2nd-pass warnings for footnotes/substitutions/references or from rstgen.nim.

### rstnodeToRefname

[ref: #symbol-rstnodetorefname]

**Input:**
- `n: PRstNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### rstParse

[ref: #symbol-rstparse]

**Input:**
- `text: string`
- `filename: string`
- `line: int`
- `column: int`
- `options: RstParseOptions`
- `findFile: FindFileHandler = nil`
- `findRefFile: FindRefFileHandler = nil`
- `msgHandler: MsgHandler = nil`

**Output:** `tuple[node: PRstNode, filenames: RstFileTable, hasToc: bool]`
**Pragmas:** `raises: [Exception, ValueError, KeyError]`, `tags: [RootEffect, ReadIOEffect, ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, KeyError`, `tags: RootEffect, ReadIOEffect, ReadEnvEffect`, `forbids: `

Parses the whole text. The result is ready for rstgen.renderRstToOut, note that 2nd tuple element should be fed to initRstGenerator argument filenames (it is being filled here at least with filename and possibly with other files from RST .. include:: statement).

### rstParsePass1

[ref: #symbol-rstparsepass1]

**Input:**
- `fragment: string`
- `line: int`
- `column: int`
- `sharedState: PRstSharedState`

**Output:** `PRstNode`
**Pragmas:** `raises: [Exception, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError`, `tags: RootEffect`, `forbids: `

Parses an RST fragment. The result should be further processed by [preparePass2](#preparePass2) and [resolveSubs](#resolveSubs) (which is pass 2).

### safeProtocol

[ref: #symbol-safeprotocol]

**Input:**
- `linkStr: var string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setCurrFilename

[ref: #symbol-setcurrfilename]

**Input:**
- `s: PRstSharedState`
- `file1: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### whichMsgClass

[ref: #symbol-whichmsgclass]

**Input:**
- `k: MsgKind`

**Output:** `MsgClass`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns which message class k belongs to.

## Type

### EParseError

[ref: #symbol-eparseerror]

```nim
EParseError = object of ValueError
```

### FindFileHandler

[ref: #symbol-findfilehandler]

```nim
FindFileHandler = proc (filename: string): string {.closure, gcsafe.}
```

### FindRefFileHandler

[ref: #symbol-findreffilehandler]

```nim
FindRefFileHandler = proc (targetRelPath: string): tuple[targetPath: string,
    linkRelPath: string] {.closure, gcsafe.}
```

returns where .html or .idx file should be found by its relative path; linkRelPath is a prefix to be added before a link anchor from such file

### MsgClass

[ref: #symbol-msgclass]

```nim
MsgClass = enum
  mcHint = "Hint", mcWarning = "Warning", mcError = "Error"
```

### MsgHandler

[ref: #symbol-msghandler]

```nim
MsgHandler = proc (filename: string; line, col: int; msgKind: MsgKind;
                   arg: string) {.closure, gcsafe.}
```

what to do in case of an error

### MsgKind

[ref: #symbol-msgkind]

```nim
MsgKind = enum
  meCannotOpenFile = "cannot open \'$1\'", meExpected = "\'$1\' expected",
  meMissingClosing = "$1",
  meGridTableNotImplemented = "grid table is not implemented",
  meMarkdownIllformedTable = "illformed delimiter row of a Markdown table",
  meIllformedTable = "Illformed table: $1",
  meNewSectionExpected = "new section expected $1",
  meGeneralParseError = "general parse error",
  meInvalidDirective = "invalid directive: \'$1\'",
  meInvalidField = "invalid field: $1",
  meFootnoteMismatch = "mismatch in number of footnotes and their refs: $1",
  mwRedefinitionOfLabel = "redefinition of label \'$1\'",
  mwUnknownSubstitution = "unknown substitution \'$1\'",
  mwAmbiguousLink = "ambiguous doc link $1",
  mwBrokenLink = "broken link \'$1\'",
  mwUnsupportedLanguage = "language \'$1\' not supported",
  mwUnsupportedField = "field \'$1\' not supported",
  mwRstStyle = "RST style: $1",
  mwUnusedImportdoc = "importdoc for \'$1\' is not used",
  meSandboxedDirective = "disabled directive: \'$1\'"
```

the possible messages

### PRstSharedState

[ref: #symbol-prstsharedstate]

```nim
PRstSharedState = ref RstSharedState
```

### RstFileTable

[ref: #symbol-rstfiletable]

```nim
RstFileTable = object
  filenameToIdx*: Table[string, FileIndex]
  idxToFilename*: seq[string]
```

### RstParseOption

[ref: #symbol-rstparseoption]

```nim
RstParseOption = enum
  roSupportSmilies,         ## make the RST parser support smilies like ``:)``
  roSupportRawDirective,    ## support the ``raw`` directive (don't support
                             ## it for sandboxing)
  roSupportMarkdown,        ## support additional features of Markdown
  roPreferMarkdown,         ## parse as Markdown (keeping RST as "extension"
                             ## to Markdown) -- implies `roSupportMarkdown`
  roNimFile,                ## set for Nim files where default interpreted
                             ## text role should be :nim:
  roSandboxDisabled          ## this option enables certain options
                             ## (e.g. raw, include, importdoc)
                             ## which are disabled by default as they can
                             ## enable users to read arbitrary data and
                             ## perform XSS if the parser is used in a web
                             ## app.
```

options for the RST parser

### RstParseOptions

[ref: #symbol-rstparseoptions]

```nim
RstParseOptions = set[RstParseOption]
```
