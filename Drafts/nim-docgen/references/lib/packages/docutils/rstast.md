---
source_hash: 8509ec940b661e3c
source_path: lib/packages/docutils/rstast.nim
---

# rstast

[ref: #module-rstast]

This module implements an AST for the reStructuredText parser.

## Proc

### `==`

[ref: #symbol-]

**Input:**
- `a: FileIndex`
- `b: FileIndex`

**Output:** `bool`
**Pragmas:** `borrow`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### add

[ref: #symbol-add]

**Input:**
- `father: PRstNode`
- `son: PRstNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### add

[ref: #symbol-add]

**Input:**
- `father: PRstNode`
- `s: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### addIfNotNil

[ref: #symbol-addifnotnil]

**Input:**
- `father: PRstNode`
- `son: PRstNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### lastSon

[ref: #symbol-lastson]

**Input:**
- `n: PRstNode`

**Output:** `PRstNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### len

[ref: #symbol-len]

**Input:**
- `n: PRstNode`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newRstLeaf

[ref: #symbol-newrstleaf]

**Input:**
- `s: string`

**Output:** `PRstNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newRstNode

[ref: #symbol-newrstnode]

**Input:**
- `kind: RstNodeKind`
- `sons: seq[PRstNode] = @[]`
- `anchor:  = ""`

**Output:** `PRstNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newRstNode

[ref: #symbol-newrstnode]

**Input:**
- `kind: RstNodeKind`
- `info: TLineInfo`
- `sons: seq[PRstNode] = @[]`

**Output:** `PRstNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newRstNode

[ref: #symbol-newrstnode]

**Input:**
- `kind: RstNodeKind`
- `s: string`

**Output:** `PRstNode`
**Pragmas:** `deprecated`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### renderRstToJson

[ref: #symbol-renderrsttojson]

Writes the given RST node as JSON that is in the form

**Input:**
- `node: PRstNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Writes the given RST node as JSON that is in the form

```
{
  "kind":string node.kind,
  "text":optional string node.text,
  "level":optional int node.level,
  "sons":optional node array
}
```

### renderRstToRst

[ref: #symbol-renderrsttorst]

**Input:**
- `n: PRstNode`
- `result: var string`

**Output:** *(none)*
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

renders n into its string representation and appends to result.

### renderRstToText

[ref: #symbol-renderrsttotext]

**Input:**
- `node: PRstNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

minimal text representation of markup node

### treeRepr

[ref: #symbol-treerepr]

**Input:**
- `node: PRstNode`
- `indent:  = 0`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Writes the parsed RST node into an AST tree with compact string representation in the format (one line per every sub-node): indent - kind - [text|level|order|adType] - anchor (if non-zero) (suitable for debugging of RST parsing).

## Type

### FileIndex

[ref: #symbol-fileindex]

```nim
FileIndex = distinct int32
```

### PRstNode

[ref: #symbol-prstnode]

```nim
PRstNode = ref RstNode
```

an RST node

### RstNode

[ref: #symbol-rstnode]

```nim
RstNode {.acyclic, final.} = object
  case kind*: RstNodeKind    ## the node's kind
  of rnLeaf, rnSmiley:
    text*: string            ## string that is expected to be displayed
  of rnEnumList:
    labelFmt*: string        ## label format like "(1)"
  of rnLineBlockItem:
    lineIndent*: string      ## a few spaces or newline at the line beginning
  of rnAdmonition:
    adType*: string          ## admonition type: "note", "caution", etc. This
                             ## text will set the style and also be displayed
  of rnOverline, rnHeadline, rnMarkdownHeadline:
    level*: int              ## level of headings starting from 1 (main
                             ## chapter) to larger ones (minor sub-sections)
                             ## level=0 means it's document title or subtitle
  of rnFootnote, rnCitation, rnOptionListItem:
    order*: int              ## footnote order (for auto-symbol footnotes and
                             ## auto-numbered ones without a label)
  of rnMarkdownBlockQuoteItem:
    quotationDepth*: int     ## number of characters in line prefix
  of rnRstRef, rnPandocRef, rnSubstitutionReferences, rnInterpretedText,
     rnField, rnInlineCode, rnCodeBlock, rnFootnoteRef:
    info*: TLineInfo         ## To have line/column info for warnings at
                             ## nodes that are post-processed after parsing
  of rnNimdocRef:
    tooltip*: string
  of rnTable, rnGridTable, rnMarkdownTable:
    colCount*: int           ## Number of (not-united) cells in the table
  of rnTableRow:
    endsHeader*: bool        ## Is last row in the header of table?
  of rnTableHeaderCell, rnTableDataCell:
    span*: int               ## Number of table columns that the cell occupies
  else:
    nil
  anchor*: string            ## anchor, internal link target
                             ## (aka HTML id tag, aka Latex label/hypertarget)
  sons*: RstNodeSeq          ## the node's sons
```

AST node (result of RST parsing)

### RstNodeKind

[ref: #symbol-rstnodekind]

```nim
RstNodeKind = enum
  rnInner, rnHeadline, rnOverline, rnMarkdownHeadline, rnTransition,
  rnParagraph, rnBulletList, rnBulletItem, rnEnumList, rnEnumItem, rnDefList,
  rnMdDefList, rnDefItem, rnDefName, rnDefBody, rnFieldList, rnField,
  rnFieldName, rnFieldBody, rnOptionList, rnOptionListItem, rnOptionGroup,
  rnOption, rnOptionString, rnOptionArgument, rnDescription, rnLiteralBlock,
  rnMarkdownBlockQuote, rnMarkdownBlockQuoteItem, rnLineBlock, rnLineBlockItem,
  rnBlockQuote, rnTable, rnGridTable, rnMarkdownTable, rnTableRow,
  rnTableHeaderCell, rnTableDataCell, rnFootnote, rnCitation, rnFootnoteGroup,
  rnStandaloneHyperlink, rnHyperlink, rnRstRef, rnPandocRef, rnInternalRef,
  rnFootnoteRef, rnNimdocRef, rnDirective, rnDirArg, rnRaw, rnTitle, rnContents,
  rnImage, rnFigure, rnCodeBlock, rnAdmonition, rnRawHtml, rnRawLatex,
  rnContainer, rnIndex, rnSubstitutionDef, rnInlineCode, rnCodeFragment,
  rnUnknownRole, rnSub, rnSup, rnIdx, rnEmphasis, rnStrongEmphasis,
  rnTripleEmphasis, rnInterpretedText, rnInlineLiteral, rnInlineTarget,
  rnSubstitutionReferences, rnSmiley, rnDefaultRole, rnLeaf
```

the possible node kinds of an PRstNode

### RstNodeSeq

[ref: #symbol-rstnodeseq]

```nim
RstNodeSeq = seq[PRstNode]
```

### TLineInfo

[ref: #symbol-tlineinfo]

```nim
TLineInfo = object
  line*: uint16
  col*: int16
  fileIndex*: FileIndex
```
