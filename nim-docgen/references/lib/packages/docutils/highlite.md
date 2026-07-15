---
source_hash: 6c37de724a6d3120
source_path: lib/packages/docutils/highlite.nim
---

# highlite

[ref: #module-highlite]

Source highlighter for programming or markup languages. Currently only few languages are supported, other languages may be added. The interface supports one language nested in another.

You can use this to build your own syntax highlighting, check this example:

```
let code = """for x in $int.high: echo x.ord mod 2 == 0"""
var toknizr: GeneralTokenizer
initGeneralTokenizer(toknizr, code)
while true:
  getNextToken(toknizr, langNim)
  case toknizr.kind
  of gtEof: break  # End Of File (or string)
  of gtWhitespace:
    echo gtWhitespace # Maybe you want "visible" whitespaces?.
    echo substr(code, toknizr.start, toknizr.length + toknizr.start - 1)
  of gtOperator:
    echo gtOperator # Maybe you want Operators to use a specific color?.
    echo substr(code, toknizr.start, toknizr.length + toknizr.start - 1)
  # of gtSomeSymbol: syntaxHighlight("Comic Sans", "bold", "99px", "pink")
  else:
    echo toknizr.kind # All the kinds of tokens can be processed here.
    echo substr(code, toknizr.start, toknizr.length + toknizr.start - 1)
```

The proc getSourceLanguage can get the language enum from a string:

```
for l in ["C", "c++", "jAvA", "Nim", "c#"]: echo getSourceLanguage(l)
```

There is also a Cmd pseudo-language supported, which is a simple generic shell/cmdline tokenizer (UNIX shell/Powershell/Windows Command): no escaping, no programming language constructs besides variable definition at the beginning of line. It supports these operators:

```
&  &&  |  ||  (  )  ''  ""  ;  # for comments
```

Instead of escaping always use quotes like here nimgrep --ext:'nim|nims' file.name shows how to input |. Any argument that contains . or / or \ will be treated as a file or directory.

In addition to Cmd there is also Console language for displaying interactive sessions. Lines with a command should start with $, other lines are considered as program output.

## Examples

```nim
let code = """for x in $int.high: echo x.ord mod 2 == 0"""
var toknizr: GeneralTokenizer
initGeneralTokenizer(toknizr, code)
while true:
  getNextToken(toknizr, langNim)
  case toknizr.kind
  of gtEof: break  # End Of File (or string)
  of gtWhitespace:
    echo gtWhitespace # Maybe you want "visible" whitespaces?.
    echo substr(code, toknizr.start, toknizr.length + toknizr.start - 1)
  of gtOperator:
    echo gtOperator # Maybe you want Operators to use a specific color?.
    echo substr(code, toknizr.start, toknizr.length + toknizr.start - 1)
  # of gtSomeSymbol: syntaxHighlight("Comic Sans", "bold", "99px", "pink")
  else:
    echo toknizr.kind # All the kinds of tokens can be processed here.
    echo substr(code, toknizr.start, toknizr.length + toknizr.start - 1)
```

```nim
for l in ["C", "c++", "jAvA", "Nim", "c#"]: echo getSourceLanguage(l)
```

```nim
&  &&  |  ||  (  )  ''  ""  ;  # for comments
```

## Const

### sourceLanguageToAlpha

[ref: #symbol-sourcelanguagetoalpha]

```nim
sourceLanguageToAlpha: array[SourceLanguage, string] = ["none", "Nim", "cpp",
    "csharp", "C", "Java", "Yaml", "Python", "Cmd", "Console"]
```

list of languages spelled with alpabetic characters

### sourceLanguageToStr

[ref: #symbol-sourcelanguagetostr]

```nim
sourceLanguageToStr: array[SourceLanguage, string] = ["none", "Nim", "C++",
    "C#", "C", "Java", "Yaml", "Python", "Cmd", "Console"]
```

### tokenClassToStr

[ref: #symbol-tokenclasstostr]

```nim
tokenClassToStr: array[TokenClass, string] = ["Eof", "None", "Whitespace",
    "DecNumber", "BinNumber", "HexNumber", "OctNumber", "FloatNumber",
    "Identifier", "Keyword", "StringLit", "LongStringLit", "CharLit",
    "EscapeSequence", "Operator", "Punctuation", "Comment", "LongComment",
    "RegularExpression", "TagStart", "TagEnd", "Key", "Value", "RawData",
    "Assembler", "Preprocessor", "Directive", "Command", "Rule", "Hyperlink",
    "Label", "Reference", "Prompt", "ProgramOutput", "program", "option",
    "Other"]
```

## Proc

### deinitGeneralTokenizer

[ref: #symbol-deinitgeneraltokenizer]

**Input:**
- `g: var GeneralTokenizer`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getNextToken

[ref: #symbol-getnexttoken]

**Input:**
- `g: var GeneralTokenizer`
- `lang: SourceLanguage`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getSourceLanguage

[ref: #symbol-getsourcelanguage]

**Input:**
- `name: string`

**Output:** `SourceLanguage`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### initGeneralTokenizer

[ref: #symbol-initgeneraltokenizer]

**Input:**
- `g: var GeneralTokenizer`
- `buf: cstring`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### initGeneralTokenizer

[ref: #symbol-initgeneraltokenizer]

**Input:**
- `g: var GeneralTokenizer`
- `buf: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### tokenize

[ref: #symbol-tokenize]

**Input:**
- `text: string`
- `lang: SourceLanguage`

**Output:** `seq[(string, TokenClass)]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### GeneralTokenizer

[ref: #symbol-generaltokenizer]

```nim
GeneralTokenizer = object of RootObj
  kind*: TokenClass
  start*, length*: int
```

### SourceLanguage

[ref: #symbol-sourcelanguage]

```nim
SourceLanguage = enum
  langNone, langNim, langCpp, langCsharp, langC, langJava, langYaml, langPython,
  langCmd, langConsole
```

### TokenClass

[ref: #symbol-tokenclass]

```nim
TokenClass = enum
  gtEof, gtNone, gtWhitespace, gtDecNumber, gtBinNumber, gtHexNumber,
  gtOctNumber, gtFloatNumber, gtIdentifier, gtKeyword, gtStringLit,
  gtLongStringLit, gtCharLit, gtEscapeSequence, gtOperator, gtPunctuation,
  gtComment, gtLongComment, gtRegularExpression, gtTagStart, gtTagEnd, gtKey,
  gtValue, gtRawData, gtAssembler, gtPreprocessor, gtDirective, gtCommand,
  gtRule, gtHyperlink, gtLabel, gtReference, gtPrompt, gtProgramOutput,
  gtProgram, gtOption, gtOther
```
