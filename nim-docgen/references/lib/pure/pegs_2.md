---
source_hash: e01119a17c5e0759
source_path: lib/pure/pegs.nim
---

### nonterminal

[ref: #symbol-nonterminal]

**Input:**
- `n: NonTerminal`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a PEG that consists of the nonterminal symbol

### nt

[ref: #symbol-nt]

**Input:**
- `p: Peg`

**Output:** `NonTerminal`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the *NonTerminal* object of a given *Peg* variant object where present.

### parallelReplace

[ref: #symbol-parallelreplace]

**Input:**
- `s: string`
- `subs: varargs[tuple[pattern: Peg, repl: string]]`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: [ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: RootEffect`, `forbids: `

Returns a modified copy of s with the substitutions in subs applied in parallel.

### parsePeg

[ref: #symbol-parsepeg]

**Input:**
- `pattern: string`
- `filename:  = "pattern"`
- `line:  = 1`
- `col:  = 0`

**Output:** `Peg`
**Pragmas:** `raises: [EInvalidPeg]`, `gcsafe`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: EInvalidPeg`, `tags: RootEffect`, `forbids: `

constructs a Peg object from pattern. filename, line, col are used for error messages, but they only provide start offsets. parsePeg keeps track of line and column numbers within pattern.

### peg

[ref: #symbol-peg]

constructs a Peg object from the pattern. The short name has been chosen to encourage its use as a raw string modifier:

**Input:**
- `pattern: string`

**Output:** `Peg`
**Pragmas:** `raises: [EInvalidPeg]`, `gcsafe`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: EInvalidPeg`, `tags: RootEffect`, `forbids: `

constructs a Peg object from the pattern. The short name has been chosen to encourage its use as a raw string modifier:

```
peg"{\ident} \s* '=' \s* {.*}"
```

### rawMatch

[ref: #symbol-rawmatch]

**Input:**
- `s: string`
- `p: Peg`
- `start: int`
- `c: var Captures`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

low-level matching proc that implements the PEG interpreter. Use this for maximum efficiency (every other PEG operation ends up calling this proc). Returns -1 if it does not match, else the length of the match

### replace

[ref: #symbol-replace]

**Input:**
- `s: string`
- `sub: Peg`
- `by:  = ""`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Replaces sub in s by the string by. Captures cannot be accessed in by.

### replace

[ref: #symbol-replace]

Replaces sub in s by the resulting strings from the callback. The callback proc receives the index of the current match (starting with 0), the count of captures and an open array with the captures of each match. Examples:

**Input:**
- `s: string`
- `sub: Peg`
- `cb: proc (match: int; cnt: int; caps: openArray[string]): string {.gcsafe.}`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "npegs$1cb"`, `effectsOf: cb`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Replaces sub in s by the resulting strings from the callback. The callback proc receives the index of the current match (starting with 0), the count of captures and an open array with the captures of each match. Examples:

```
func handleMatches*(m: int, n: int, c: openArray[string]): string =
  result = ""
  if m > 0:
    result.add ", "
  result.add case n:
    of 2: c[0].toLower & ": '" & c[1] & "'"
    of 1: c[0].toLower & ": ''"
    else: ""

let s = "Var1=key1;var2=Key2;   VAR3"
echo s.replace(peg"{\ident}('='{\ident})* ';'* \s*", handleMatches)
```

Results in:

```
"var1: 'key1', var2: 'Key2', var3: ''"
```

### replacef

[ref: #symbol-replacef]

Replaces sub in s by the string by. Captures can be accessed in by with the notation $i and $# (see strutils.%). Examples:

**Input:**
- `s: string`
- `sub: Peg`
- `by: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: [ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: RootEffect`, `forbids: `

Replaces sub in s by the string by. Captures can be accessed in by with the notation $i and $# (see strutils.%). Examples:

```
"var1=key; var2=key2".replacef(peg"{\ident}'='{\ident}", "$1<-$2$2")
```

Results in:

```
"var1<-keykey; val2<-key2key2"
```

### rule

[ref: #symbol-rule]

**Input:**
- `nt: NonTerminal`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the *Peg* object representing the rule definition of the parent *Peg* object variant of a given *NonTerminal*.

### sequence

[ref: #symbol-sequence]

**Input:**
- `a: varargs[Peg]`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a sequence with all the PEGs from a

### split

[ref: #symbol-split]

**Input:**
- `s: string`
- `sep: Peg`

**Output:** `seq[string]`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Splits the string s into substrings.

### startAnchor

[ref: #symbol-startanchor]

**Input:**
- *(none)*

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs the PEG ^ which matches the start of the input.

### startsWith

[ref: #symbol-startswith]

**Input:**
- `s: string`
- `prefix: Peg`
- `start:  = 0`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

returns true if s starts with the pattern prefix

### term

[ref: #symbol-term]

**Input:**
- `p: Peg`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the *string* representation of a given *Peg* variant object where present.

### term

[ref: #symbol-term]

**Input:**
- `t: string`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegs$1Str"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a PEG from a terminal string

### term

[ref: #symbol-term]

**Input:**
- `t: char`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegs$1Char"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a PEG from a terminal char

### termIgnoreCase

[ref: #symbol-termignorecase]

**Input:**
- `t: string`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a PEG from a terminal string; ignore case for matching

### termIgnoreStyle

[ref: #symbol-termignorestyle]

**Input:**
- `t: string`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a PEG from a terminal string; ignore style for matching

### transformFile

[ref: #symbol-transformfile]

reads in the file infile, performs a parallel replacement (calls parallelReplace) and writes back to outfile. Raises IOError if an error occurs. This is supposed to be used for quick scripting.

**Input:**
- `infile: string`
- `outfile: string`
- `subs: varargs[tuple[pattern: Peg, repl: string]]`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `raises: [ValueError, IOError]`, `gcsafe`, `gcsafe`, `tags: [ReadIOEffect, WriteIOEffect, RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, IOError`, `tags: ReadIOEffect, WriteIOEffect, RootEffect`, `forbids: `

reads in the file infile, performs a parallel replacement (calls parallelReplace) and writes back to outfile. Raises IOError if an error occurs. This is supposed to be used for quick scripting.

**Note**: this proc does not exist while using the JS backend.

### unicodeLetter

[ref: #symbol-unicodeletter]

**Input:**
- *(none)*

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs the PEG \letter which matches any Unicode letter.

### unicodeLower

[ref: #symbol-unicodelower]

**Input:**
- *(none)*

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs the PEG \lower which matches any Unicode lowercase letter.

### unicodeTitle

[ref: #symbol-unicodetitle]

**Input:**
- *(none)*

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs the PEG \title which matches any Unicode title letter.

### unicodeUpper

[ref: #symbol-unicodeupper]

**Input:**
- *(none)*

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs the PEG \upper which matches any Unicode uppercase letter.

### unicodeWhitespace

[ref: #symbol-unicodewhitespace]

**Input:**
- *(none)*

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs the PEG \white which matches any Unicode whitespace character.

## Template

### `=~`

[ref: #symbol-]

This calls match with an implicit declared matches array that can be used in the scope of the =~ call:

**Input:**
- `s: string`
- `pattern: Peg`

**Output:** `bool`
This calls match with an implicit declared matches array that can be used in the scope of the =~ call:

```
if line =~ peg"\s* {\w+} \s* '=' \s* {\w+}":
  # matches a key=value pair:
  echo("Key: ", matches[0])
  echo("Value: ", matches[1])
elif line =~ peg"\s*{'#'.*}":
  # matches a comment
  # note that the implicit ``matches`` array is different from the
  # ``matches`` array of the first branch
  echo("comment: ", matches[0])
else:
  echo("syntax error")
```

### digits

[ref: #symbol-digits]

**Input:**
- *(none)*

**Output:** `Peg`
expands to charset({'0'..'9'})

### eventParser

[ref: #symbol-eventparser]

Generates an interpreting event parser *proc* according to the specified PEG AST and handler code blocks. The *proc* can be called with a string to be parsed and will execute the handler code blocks whenever their associated grammar element is matched. It returns -1 if the string does not match, else the length of the total match. The following example code evaluates an arithmetic expression defined by a simple PEG:

**Input:**
- `pegAst: untyped`
- `handlers: untyped`

**Output:** `(proc (s: string): int)`
Generates an interpreting event parser *proc* according to the specified PEG AST and handler code blocks. The *proc* can be called with a string to be parsed and will execute the handler code blocks whenever their associated grammar element is matched. It returns -1 if the string does not match, else the length of the total match. The following example code evaluates an arithmetic expression defined by a simple PEG:

```
import std/[strutils, pegs]

let
  pegAst = """
Expr    <- Sum
Sum     <- Product (('+' / '-')Product)*
Product <- Value (('*' / '/')Value)*
Value   <- [0-9]+ / '(' Expr ')'
  """.peg
  txt = "(5+3)/2-7*22"

var
  pStack: seq[string] = @[]
  valStack: seq[float] = @[]
  opStack = ""
let
  parseArithExpr = pegAst.eventParser:
    pkNonTerminal:
      enter:
        pStack.add p.nt.name
      leave:
        pStack.setLen pStack.high
        if length > 0:
          let matchStr = s.substr(start, start+length-1)
          case p.nt.name
          of "Value":
            try:
              valStack.add matchStr.parseFloat
              echo valStack
            except ValueError:
              discard
          of "Sum", "Product":
            try:
              let val = matchStr.parseFloat
            except ValueError:
              if valStack.len > 1 and opStack.len > 0:
                valStack[^2] = case opStack[^1]
                of '+': valStack[^2] + valStack[^1]
                of '-': valStack[^2] - valStack[^1]
                of '*': valStack[^2] * valStack[^1]
                else: valStack[^2] / valStack[^1]
                valStack.setLen valStack.high
                echo valStack
                opStack.setLen opStack.high
                echo opStack
    pkChar:
      leave:
        if length == 1 and "Value" != pStack[^1]:
          let matchChar = s[start]
          opStack.add matchChar
          echo opStack

let pLen = parseArithExpr(txt)
```

The *handlers* parameter consists of code blocks for *PegKinds*, which define the grammar elements of interest. Each block can contain handler code to be executed when the parser enters and leaves text matching the grammar element. An *enter* handler can access the specific PEG AST node being matched as *p*, the entire parsed string as *s* and the position of the matched text segment in *s* as *start*. A *leave* handler can access *p*, *s*, *start* and also the length of the matched text segment as *length*. For an unsuccessful match, the *enter* and *leave* handlers will be executed, with *length* set to -1.

Symbols declared in an *enter* handler can be made visible in the corresponding *leave* handler by annotating them with an *inject* pragma.

### ident

[ref: #symbol-ident]

**Input:**
- *(none)*

**Output:** `Peg`
same as [a-zA-Z\_][a-zA-z\_0-9]\*; standard identifier

### identChars

[ref: #symbol-identchars]

**Input:**
- *(none)*

**Output:** `Peg`
expands to charset({'a'..'z', 'A'..'Z', '0'..'9', '\_'})

### identStartChars

[ref: #symbol-identstartchars]

**Input:**
- *(none)*

**Output:** `Peg`
expands to charset({'A'..'Z', 'a'..'z', '\_'})

### letters

[ref: #symbol-letters]

**Input:**
- *(none)*

**Output:** `Peg`
expands to charset({'A'..'Z', 'a'..'z'})

### natural

[ref: #symbol-natural]

**Input:**
- *(none)*

**Output:** `Peg`
same as \d+

### whitespace

[ref: #symbol-whitespace]

**Input:**
- *(none)*

**Output:** `Peg`
expands to charset({' ', '\9'..'\13'})

## Type

### Captures

[ref: #symbol-captures]

```nim
Captures = object
```

contains the captured substrings.

### EInvalidPeg

[ref: #symbol-einvalidpeg]

```nim
EInvalidPeg = object of ValueError
```

raised if an invalid PEG has been detected

### NonTerminal

[ref: #symbol-nonterminal]

```nim
NonTerminal = ref NonTerminalObj
```

### NonTerminalFlag

[ref: #symbol-nonterminalflag]

```nim
NonTerminalFlag = enum
  ntDeclared, ntUsed
```

### Peg

[ref: #symbol-peg]

```nim
Peg {.shallow.} = object
  case
  of pkEmpty .. pkWhitespace:
    nil
  of pkTerminal, pkTerminalIgnoreCase, pkTerminalIgnoreStyle:
  of pkChar, pkGreedyRepChar:
  of pkCharChoice, pkGreedyRepSet:
  of pkNonTerminal:
  of pkBackRef .. pkBackRefIgnoreStyle:
  else:
```

type that represents a PEG

### PegKind

[ref: #symbol-pegkind]

```nim
PegKind = enum
  pkEmpty, pkAny,           ## any character (.)
  pkAnyRune,                ## any Unicode character (_)
  pkNewLine,                ## CR-LF, LF, CR
  pkLetter,                 ## Unicode letter
  pkLower,                  ## Unicode lower case letter
  pkUpper,                  ## Unicode upper case letter
  pkTitle,                  ## Unicode title character
  pkWhitespace,             ## Unicode whitespace character
  pkTerminal, pkTerminalIgnoreCase, pkTerminalIgnoreStyle, pkChar, ## single character to match
  pkCharChoice, pkNonTerminal, pkSequence, ## a b c ... --> Internal DSL: peg(a, b, c)
  pkOrderedChoice,          ## a / b / ... --> Internal DSL: a / b or /[a, b, c]
  pkGreedyRep,              ## a*     --> Internal DSL: *a
                             ## a+     --> (a a*)
  pkGreedyRepChar,          ## x* where x is a single character (superop)
  pkGreedyRepSet,           ## [set]* (superop)
  pkGreedyAny,              ## .* or _* (superop)
  pkOption,                 ## a?     --> Internal DSL: ?a
  pkAndPredicate,           ## &a     --> Internal DSL: &a
  pkNotPredicate,           ## !a     --> Internal DSL: !a
  pkCapture,                ## {a}    --> Internal DSL: capture(a)
  pkBackRef,                ## $i     --> Internal DSL: backref(i)
  pkBackRefIgnoreCase, pkBackRefIgnoreStyle, pkSearch, ## @a     --> Internal DSL: !*a
  pkCapturedSearch,         ## {@} a  --> Internal DSL: !*\a
  pkRule,                   ## a <- b
  pkList,                   ## a, b
  pkStartAnchor              ## ^      --> Internal DSL: startAnchor()
```

[Prev](pegs_1.md)
