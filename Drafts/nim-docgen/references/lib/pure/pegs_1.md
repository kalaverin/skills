---
source_hash: e01119a17c5e0759
source_path: lib/pure/pegs.nim
---

# pegs

[ref: #module-pegs]

Simple PEG (Parsing expression grammar) matching. Uses no memorization, but uses superoperators and symbol inlining to improve performance. Note: Matching performance is hopefully competitive with optimized regular expression engines.

# [PEG syntax and semantics](#peg-syntax-and-semantics)

A PEG (Parsing expression grammar) is a simple deterministic grammar, that can be directly used for parsing. The current implementation has been designed as a more powerful replacement for regular expressions. UTF-8 is supported.

The notation used for a PEG is similar to that of EBNF:

| notation | meaning |
| --- | --- |
| A / ... / Z | Ordered choice: Apply expressions A, ..., Z, in this order, to the text ahead, until one of them succeeds and possibly consumes some text. Indicate success if one of expressions succeeded. Otherwise, do not consume any text and indicate failure. |
| A ... Z | Sequence: Apply expressions A, ..., Z, in this order, to consume consecutive portions of the text ahead, as long as they succeed. Indicate success if all succeeded. Otherwise, do not consume any text and indicate failure. The sequence's precedence is higher than that of ordered choice: A B / C means (A B) / C and not A (B / C). |
| (E) | Grouping: Parenthesis can be used to change operator priority. |
| {E} | Capture: Apply expression E and store the substring that matched E into a *capture* that can be accessed after the matching process. |
| {} | Empty capture: Delete the last capture. No character is consumed. |
| $i | Back reference to the ith capture. i counts forwards from 1 or backwards (last capture to first) from ^1. |
| $ | Anchor: Matches at the end of the input. No character is consumed. Same as !.. |
| ^ | Anchor: Matches at the start of the input. No character is consumed. |
| &E | And predicate: Indicate success if expression E matches the text ahead; otherwise indicate failure. Do not consume any text. |
| !E | Not predicate: Indicate failure if expression E matches the text ahead; otherwise indicate success. Do not consume any text. |
| E+ | One or more: Apply expression E repeatedly to match the text ahead, as long as it succeeds. Consume the matched text (if any) and indicate success if there was at least one match. Otherwise, indicate failure. |
| E\* | Zero or more: Apply expression E repeatedly to match the text ahead, as long as it succeeds. Consume the matched text (if any). Always indicate success. |
| E? | Zero or one: If expression E matches the text ahead, consume it. Always indicate success. |
| [s] | Character class: If the character ahead appears in the string s, consume it and indicate success. Otherwise, indicate failure. |
| [a-b] | Character range: If the character ahead is one from the range a through b, consume it and indicate success. Otherwise, indicate failure. |
| 's' | String: If the text ahead is the string s, consume it and indicate success. Otherwise, indicate failure. |
| i's' | String match ignoring case. |
| y's' | String match ignoring style. |
| v's' | Verbatim string match: Use this to override a global \i or \y modifier. |
| i$j | String match ignoring case for back reference. |
| y$j | String match ignoring style for back reference. |
| v$j | Verbatim string match for back reference. |
| . | Any character: If there is a character ahead, consume it and indicate success. Otherwise, (that is, at the end of input) indicate failure. |
| \_ | Any Unicode character: If there is a UTF-8 character ahead, consume it and indicate success. Otherwise, indicate failure. |
| @E | Search: Shorthand for (!E .)\* E. (Search loop for the pattern E.) |
| {@} E | Captured Search: Shorthand for {(!E .)\*} E. (Search loop for the pattern E.) Everything until and excluding E is captured. |
| @@ E | Same as {@} E. |
| A <- E | Rule: Bind the expression E to the *nonterminal symbol* A. **Left recursive rules are not possible and crash the matching engine.** |
| \identifier | Built-in macro for a longer expression. |
| \ddd | Character with decimal code *ddd*. |
| \", etc. | Literal ", etc. |

## [Built-in macros](#peg-syntax-and-semantics-builtminusin-macros)

| macro | meaning |
| --- | --- |
| \d | any decimal digit: [0-9] |
| \D | any character that is not a decimal digit: [^0-9] |
| \s | any whitespace character: [ \9-\13] |
| \S | any character that is not a whitespace character: [^ \9-\13] |
| \w | any "word" character: [a-zA-Z0-9\_] |
| \W | any "non-word" character: [^a-zA-Z0-9\_] |
| \a | same as [a-zA-Z] |
| \A | same as [^a-zA-Z] |
| \n | any newline combination: \10 / \13\10 / \13 |
| \i | ignore case for matching; use this at the start of the PEG |
| \y | ignore style for matching; use this at the start of the PEG |
| \skip pat | skip pattern *pat* before trying to match other tokens; this is useful for whitespace skipping, for example: \skip(\s\*) {\ident} ':' {\ident} matches key value pairs ignoring whitespace around the ':'. |
| \ident | a standard ASCII identifier: [a-zA-Z\_][a-zA-Z\_0-9]\* |
| \letter | any Unicode letter |
| \upper | any Unicode uppercase letter |
| \lower | any Unicode lowercase letter |
| \title | any Unicode title letter |
| \white | any Unicode whitespace character |

A backslash followed by a letter is a built-in macro, otherwise it is used for ordinary escaping:

| notation | meaning |
| --- | --- |
| \\ | a single backslash |
| \\* | same as '\*' |
| \t | not a tabulator, but an (unknown) built-in |

## [Supported PEG grammar](#peg-syntax-and-semantics-supported-peg-grammar)

The PEG parser implements this grammar (written in PEG syntax):

```
# Example grammar of PEG in PEG syntax.
# Comments start with '#'.
# First symbol is the start symbol.

grammar <- rule* / expr

identifier <- [A-Za-z][A-Za-z0-9_]*
charsetchar <- "\\" . / [^\]]
charset <- "[" "^"? (charsetchar ("-" charsetchar)?)+ "]"
stringlit <- identifier? ("\"" ("\\" . / [^"])* "\"" /
                          "'" ("\\" . / [^'])* "'")
builtin <- "\\" identifier / [^\13\10]

comment <- '#' @ \n
ig <- (\s / comment)* # things to ignore

rule <- identifier \s* "<-" expr ig
identNoArrow <- identifier !(\s* "<-")
prefixOpr <- ig '&' / ig '!' / ig '@' / ig '{@}' / ig '@@'
literal <- ig identifier? '$' '^'? [0-9]+ / '$' / '^' /
           ig identNoArrow /
           ig charset /
           ig stringlit /
           ig builtin /
           ig '.' /
           ig '_' /
           (ig "(" expr ig ")") /
           (ig "{" expr? ig "}")
postfixOpr <- ig '?' / ig '*' / ig '+'
primary <- prefixOpr* (literal postfixOpr*)

# Concatenation has higher priority than choice:
# ``a b / c`` means ``(a b) / c``

seqExpr <- primary+
expr <- seqExpr (ig "/" expr)*
```

**Note**: As a special syntactic extension if the whole PEG is only a single expression, identifiers are not interpreted as non-terminals, but are interpreted as verbatim string:

```
abc =~ peg"abc" # is true
```

So it is not necessary to write peg" 'abc' " in the above example.

## [Examples](#peg-syntax-and-semantics-examples)

Check if s matches Nim's "while" keyword:

```
s =~ peg" y'while'"
```

Exchange (key, val)-pairs:

```
"key: val; key2: val2".replacef(peg"{\ident} \s* ':' \s* {\ident}", "$2: $1")
```

Determine the #include'ed files of a C file:

```
for line in lines("myfile.c"):
  if line =~ peg"""s <- ws '#include' ws '"' {[^"]+} '"' ws
                   comment <- '/*' @ '*/' / '//' .*
                   ws <- (comment / \s+)* """:
    echo matches[0]
```

## [PEG vs regular expression](#peg-syntax-and-semantics-peg-vs-regular-expression)

As a regular expression \[.\*\] matches the longest possible text between '[' and ']'. As a PEG it never matches anything, because a PEG is deterministic: .\* consumes the rest of the input, so \] never matches. As a PEG this needs to be written as: \[ ( !\] . )\* \] (or \[ @ \]).

Note that the regular expression does not behave as intended either: in the example \* should not be greedy, so \[.\*?\] should be used instead.

## [PEG construction](#peg-syntax-and-semantics-peg-construction)

There are two ways to construct a PEG in Nim code:

1. Parsing a string into an AST which consists of Peg nodes with the peg proc.
2. Constructing the AST directly with proc calls. This method does not support constructing rules, only simple expressions and is not as convenient. Its only advantage is that it does not pull in the whole PEG parser into your executable.

## Examples

```nim
abc =~ peg"abc" # is true
```

```nim
s =~ peg" y'while'"
```

```nim
"key: val; key2: val2".replacef(peg"{\ident} \s* ':' \s* {\ident}", "$2: $1")
```

```nim
for line in lines("myfile.c"):
  if line =~ peg"""s <- ws '#include' ws '"' {[^"]+} '"' ws
                   comment <- '/*' @ '*/' / '//' .*
                   ws <- (comment / \s+)* """:
    echo matches[0]
```

```nim
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

```nim
"var1: 'key1', var2: 'Key2', var3: ''"
```

```nim
"var1=key; var2=key2".replacef(peg"{\ident}'='{\ident}", "$1<-$2$2")
```

```nim
"var1<-keykey; val2<-key2key2"
```

```nim
for word in split("00232this02939is39an22example111", peg"\d+"):
  writeLine(stdout, word)
```

```nim
"this"
"is"
"an"
"example"
```

```nim
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

```nim
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

## Const

### MaxSubpatterns

[ref: #symbol-maxsubpatterns]

```nim
MaxSubpatterns = 20
```

defines the maximum number of subpatterns that can be captured. More subpatterns cannot be captured!

## Iterator

### findAll

[ref: #symbol-findall]

**Input:**
- `s: string`
- `pattern: Peg`
- `start:  = 0`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

yields all matching *substrings* of s that match pattern.

### items

[ref: #symbol-items]

**Input:**
- `p: Peg`

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Yields the child nodes of a *Peg* variant object where present.

### pairs

[ref: #symbol-pairs]

**Input:**
- `p: Peg`

**Output:** `(int, Peg)`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Yields the indices and child nodes of a *Peg* variant object where present.

### split

[ref: #symbol-split]

Splits the string s into substrings.

**Input:**
- `s: string`
- `sep: Peg`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Splits the string s into substrings.

Substrings are separated by the PEG sep. Examples:

```
for word in split("00232this02939is39an22example111", peg"\d+"):
  writeLine(stdout, word)
```

Results in:

```
"this"
"is"
"an"
"example"
```

## Proc

### `!*\`

[ref: #symbol-]

**Input:**
- `a: Peg`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npgegsCapturedSearch"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a "captured search" for the PEG a

### `!*`

[ref: #symbol-]

**Input:**
- `a: Peg`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegsSearch"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a "search" for the PEG a

### `!`

[ref: #symbol-]

**Input:**
- `a: Peg`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegsNotPredicate"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a "not predicate" with the PEG a

### `$`

[ref: #symbol-]

**Input:**
- `r: Peg`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "npegsToString"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

converts a PEG to its string representation

### `&amp;`

[ref: #symbol-amp]

**Input:**
- `a: Peg`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegsAndPredicate"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs an "and predicate" with the PEG a

### `*`

[ref: #symbol-]

**Input:**
- `a: Peg`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegsGreedyRep"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a "greedy repetition" for the PEG a

### `+`

[ref: #symbol-]

**Input:**
- `a: Peg`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegsGreedyPosRep"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a "greedy positive repetition" with the PEG a

### `/`

[ref: #symbol-]

**Input:**
- `a: varargs[Peg]`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegsOrderedChoice"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs an ordered choice with the PEGs in a

### `?`

[ref: #symbol-]

**Input:**
- `a: Peg`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegsOptional"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs an optional for the PEG a

### any

[ref: #symbol-any]

**Input:**
- *(none)*

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs the PEG any character (.)

### anyRune

[ref: #symbol-anyrune]

**Input:**
- *(none)*

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs the PEG any rune (\_)

### backref

[ref: #symbol-backref]

**Input:**
- `index: range[1 .. MaxSubpatterns]`
- `reverse: bool = false`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a back reference of the given index. index starts counting from 1. reverse specifies whether indexing starts from the end of the capture list.

### backrefIgnoreCase

[ref: #symbol-backrefignorecase]

**Input:**
- `index: range[1 .. MaxSubpatterns]`
- `reverse: bool = false`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a back reference of the given index. index starts counting from 1. reverse specifies whether indexing starts from the end of the capture list. Ignores case for matching.

### backrefIgnoreStyle

[ref: #symbol-backrefignorestyle]

**Input:**
- `index: range[1 .. MaxSubpatterns]`
- `reverse: bool = false`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a back reference of the given index. index starts counting from 1. reverse specifies whether indexing starts from the end of the capture list. Ignores style for matching.

### bounds

[ref: #symbol-bounds]

**Input:**
- `c: Captures`
- `i: range[0 .. 20 - 1]`

**Output:** `tuple[first, last: int]`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns the bounds [first..last] of the i'th capture.

### capture

[ref: #symbol-capture]

**Input:**
- `a: Peg = Peg(kind: pkEmpty)`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegsCapture"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a capture with the PEG a

### ch

[ref: #symbol-ch]

**Input:**
- `p: Peg`

**Output:** `char`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the *char* representation of a given *Peg* variant object where present.

### charChoice

[ref: #symbol-charchoice]

**Input:**
- `p: Peg`

**Output:** `ref set[char]`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the *charChoice* field of a given *Peg* variant object where present.

### charSet

[ref: #symbol-charset]

**Input:**
- `s: set[char]`

**Output:** `Peg`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a PEG from a character set s

### col

[ref: #symbol-col]

**Input:**
- `nt: NonTerminal`

**Output:** `int`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the column number of the definition of the parent *Peg* object variant of a given *NonTerminal*.

### contains

[ref: #symbol-contains]

**Input:**
- `s: string`
- `pattern: Peg`
- `start:  = 0`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

same as find(s, pattern, start) >= 0

### contains

[ref: #symbol-contains]

**Input:**
- `s: string`
- `pattern: Peg`
- `matches: var openArray[string]`
- `start:  = 0`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "npegs$1Capture"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

same as find(s, pattern, matches, start) >= 0

### endAnchor

[ref: #symbol-endanchor]

**Input:**
- *(none)*

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs the PEG $ which matches the end of the input.

### endsWith

[ref: #symbol-endswith]

**Input:**
- `s: string`
- `suffix: Peg`
- `start:  = 0`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

returns true if s ends with the pattern suffix

### escapePeg

[ref: #symbol-escapepeg]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

escapes s so that it is matched verbatim when used as a peg.

### find

[ref: #symbol-find]

**Input:**
- `s: string`
- `pattern: Peg`
- `matches: var openArray[string]`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npegs$1Capture"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

returns the starting position of pattern in s and the captured substrings in the array matches. If it does not match, nothing is written into matches and -1 is returned.

### find

[ref: #symbol-find]

**Input:**
- `s: string`
- `pattern: Peg`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

returns the starting position of pattern in s. If it does not match, -1 is returned.

### findAll

[ref: #symbol-findall]

**Input:**
- `s: string`
- `pattern: Peg`
- `start:  = 0`

**Output:** `seq[string]`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

returns all matching *substrings* of s that match pattern. If it does not match, @[] is returned.

### findBounds

[ref: #symbol-findbounds]

**Input:**
- `s: string`
- `pattern: Peg`
- `matches: var openArray[string]`
- `start:  = 0`

**Output:** `tuple[first, last: int]`
**Pragmas:** `gcsafe`, `extern: "npegs$1Capture"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

returns the starting position and end position of pattern in s and the captured substrings in the array matches. If it does not match, nothing is written into matches and (-1,0) is returned.

### flags

[ref: #symbol-flags]

**Input:**
- `nt: NonTerminal`

**Output:** `set[NonTerminalFlag]`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the *NonTerminalFlag*-typed flags field of the parent *Peg* variant object of a given *NonTerminal*.

### index

[ref: #symbol-index]

**Input:**
- `p: Peg`

**Output:** `range[-20 .. 20 - 1]`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the back-reference index of a captured sub-pattern in the *Captures* object for a given *Peg* variant object where present.

### kind

[ref: #symbol-kind]

**Input:**
- `p: Peg`

**Output:** `PegKind`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the *PegKind* of a given *Peg* object.

### line

[ref: #symbol-line]

**Input:**
- `nt: NonTerminal`

**Output:** `int`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the line number of the definition of the parent *Peg* object variant of a given *NonTerminal*.

### match

[ref: #symbol-match]

**Input:**
- `s: string`
- `pattern: Peg`
- `matches: var openArray[string]`
- `start:  = 0`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "npegs$1Capture"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

returns true if s[start..] matches the pattern and the captured substrings in the array matches. If it does not match, nothing is written into matches and false is returned.

### match

[ref: #symbol-match]

**Input:**
- `s: string`
- `pattern: Peg`
- `start:  = 0`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

returns true if s matches the pattern beginning from start.

### matchLen

[ref: #symbol-matchlen]

**Input:**
- `s: string`
- `pattern: Peg`
- `matches: var openArray[string]`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npegs$1Capture"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

the same as match, but it returns the length of the match, if there is no match, -1 is returned. Note that a match length of zero can happen. It's possible that a suffix of s remains that does not belong to the match.

### matchLen

[ref: #symbol-matchlen]

**Input:**
- `s: string`
- `pattern: Peg`
- `start:  = 0`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

the same as match, but it returns the length of the match, if there is no match, -1 is returned. Note that a match length of zero can happen. It's possible that a suffix of s remains that does not belong to the match.

### name

[ref: #symbol-name]

**Input:**
- `nt: NonTerminal`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the name of the symbol represented by the parent *Peg* object variant of a given *NonTerminal*.

### newLine

[ref: #symbol-newline]

**Input:**
- *(none)*

**Output:** `Peg`
**Pragmas:** `inline`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs the PEG newline (\n)

### newNonTerminal

[ref: #symbol-newnonterminal]

**Input:**
- `name: string`
- `line: int`
- `column: int`

**Output:** `NonTerminal`
**Pragmas:** `gcsafe`, `extern: "npegs$1"`, `gcsafe`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

constructs a nonterminal symbol


[Next](pegs_2.md)
