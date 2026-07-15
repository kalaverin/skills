---
source_hash: 02863d9f84bf0530
source_path: lib/packages/docutils/rstgen.nim
---

# rstgen

[ref: #module-rstgen]

This module implements a generator of HTML/Latex from reStructuredText (see <https://docutils.sourceforge.net/rst.html> for information on this markup syntax) and is used by the compiler's [docgen tools](docgen.html).

You can generate HTML output through the convenience proc rstToHtml, which provided an input string with rst markup returns a string with the generated HTML. The final output is meant to be embedded inside a full document you provide yourself, so it won't contain the usual <header> or <body> parts.

You can also create a RstGenerator structure and populate it with the other lower level methods to finally build complete documents. This requires many options and tweaking, but you are not limited to snippets and can generate [LaTeX documents](https://en.wikipedia.org/wiki/LaTeX) too.

[Docutils configuration files](https://docutils.sourceforge.io/docs/user/config.htm) are not supported. Instead HTML generation can be tweaked by editing file config/nimdoc.cfg.

There are stylistic difference between how this module renders some elements and how original Python Docutils does:

* Backreferences to TOC in section headings are not generated. In HTML each section is also a link that points to the section itself: this is done for user to be able to copy the link into clipboard.
* The same goes for footnotes/citations links: they point to themselves. No backreferences are generated since finding all references of a footnote can be done by simply searching for [footnoteName].

## Examples

```nim
import packages/docutils/rstgen

var gen: RstGenerator
gen.initRstGenerator(outHtml, defaultConfig(), "filename", {})
```

```nim
# ...configure gen and rst vars...
var generatedHtml = ""
renderRstToOut(gen, rst, generatedHtml)
echo generatedHtml
```

```nim
import packages/docutils/rstgen, strtabs

echo rstToHtml("*Hello* **world**!", {},
  newStringTable(modeStyleInsensitive))
# --> <em>Hello</em> <strong>world</strong>!
```

```nim
doAssert rstToLatex("*Hello* **world**", {}) == """\emph{Hello} \textbf{world}"""
```

## Const

### IndexExt

[ref: #symbol-indexext]

```nim
IndexExt = ".idx"
```

## Proc

### defaultConfig

[ref: #symbol-defaultconfig]

Returns a default configuration for embedded HTML generation.

**Input:**
- *(none)*

**Output:** `StringTableRef`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a default configuration for embedded HTML generation.

The returned StringTableRef contains the parameters used by the HTML engine to build the final output. For information on what these parameters are and their purpose, please look up the file config/nimdoc.cfg bundled with the compiler.

The only difference between the contents of that file and the values provided by this proc is the doc.file variable. The doc.file variable of the configuration file contains HTML to build standalone pages, while this proc returns just the content for procs like rstToHtml to generate the bare minimum HTML.

### esc

[ref: #symbol-esc]

**Input:**
- `target: OutputTarget`
- `s: string`
- `splitAfter:  = -1`
- `escMode:  = emText`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Escapes the HTML.

### escChar

[ref: #symbol-escchar]

**Input:**
- `target: OutputTarget`
- `dest: var string`
- `c: char`
- `escMode: EscapeMode`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### formatNamedVars

[ref: #symbol-formatnamedvars]

**Input:**
- `frmt: string`
- `varnames: openArray[string]`
- `varvalues: openArray[string]`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### initRstGenerator

[ref: #symbol-initrstgenerator]

Initializes a RstGenerator.

**Input:**
- `g: var RstGenerator`
- `target: OutputTarget`
- `config: StringTableRef`
- `filename: string`
- `findFile: FindFileHandler = nil`
- `msgHandler: MsgHandler = nil`
- `filenames:  = default(RstFileTable)`
- `hasToc:  = false`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Initializes a RstGenerator.

You need to call this before using a RstGenerator with any other procs in this module. Pass a non nil StringTableRef value as config with parameters used by the HTML output generator. If you don't know what to use, pass the results of the defaultConfig() <#defaultConfig>\_ proc.

The filename parameter will be used for error reporting and creating index hyperlinks to the file, but you can pass an empty string here if you are parsing a stream in memory. If filename ends with the .nim extension, the title for the document will be set by default to Module filename. This default title can be overridden by the embedded rst, but it helps to prettify the generated index if no title is found.

The RstParseOptions, FindFileHandler and MsgHandler types are defined in the [packages/docutils/rst module](rst.html). options selects the behaviour of the rst parser.

findFile is a proc used by the rst include directive among others. The purpose of this proc is to mangle or filter paths. It receives paths specified in the rst document and has to return a valid path to existing files or the empty string otherwise. If you pass nil, a default proc will be used which given a path returns the input path only if the file exists. One use for this proc is to transform relative paths found in the document to absolute path, useful if the rst file and the resources it references are not in the same directory as the current working directory.

The msgHandler is a proc used for user error reporting. It will be called with the filename, line, col, and type of any error found during parsing. If you pass nil, a default message handler will be used which writes the messages to the standard output.

Example:

```
import packages/docutils/rstgen

var gen: RstGenerator
gen.initRstGenerator(outHtml, defaultConfig(), "filename", {})
```

### mergeIndexes

[ref: #symbol-mergeindexes]

Merges all index files in dir and returns the generated index as HTML.

**Input:**
- `dir: string`

**Output:** `string`
**Pragmas:** `raises: [OSError, IOError, ValueError]`, `tags: [ReadDirEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: OSError, IOError, ValueError`, `tags: ReadDirEffect, ReadIOEffect`, `forbids: `

Merges all index files in dir and returns the generated index as HTML.

This proc will first scan dir for index files with the .idx extension previously created by commands like nim doc|rst2html which use the --index:on switch. These index files are the result of calls to [setIndexTerm()](#setIndexTerm,RstGenerator,string,string,string,string,string) and [writeIndexFile()](#writeIndexFile,RstGenerator,string), so they are simple tab separated files.

As convention this proc will split index files into two categories: documentation and API. API indices will be all joined together into a single big sorted index, making the bulk of the final index. This is good for API documentation because many symbols are repeated in different modules. On the other hand, documentation indices are essentially table of contents plus a few special markers. These documents will be rendered in a separate section which tries to maintain the order and hierarchy of the symbols in the index file.

To differentiate between a documentation and API file a convention is used: indices which contain one entry without the HTML hash character (#) will be considered documentation, since this hash-less entry is the explicit title of the document. Indices without this explicit entry will be considered generated API extracted out of a source .nim file.

Returns the merged and sorted indices into a single HTML block which can be further embedded into nimdoc templates.

### nextSplitPoint

[ref: #symbol-nextsplitpoint]

**Input:**
- `s: string`
- `start: int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### prettyLink

[ref: #symbol-prettylink]

**Input:**
- `file: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readIndexDir

[ref: #symbol-readindexdir]

Walks dir reading .idx files converting them in IndexEntry items.

**Input:**
- `dir: string`

**Output:** `tuple[modules: seq[string], symbols: seq[IndexEntry], docs: IndexedDocs]`
**Pragmas:** `raises: [OSError, IOError, ValueError]`, `tags: [ReadDirEffect, ReadIOEffect]`, `forbids: []`

**Effects:** `raises: OSError, IOError, ValueError`, `tags: ReadDirEffect, ReadIOEffect`, `forbids: `

Walks dir reading .idx files converting them in IndexEntry items.

Returns the list of found module names, the list of free symbol entries and the different documentation indexes. The list of modules is sorted. See the documentation of mergeIndexes for details.

### renderCodeLang

[ref: #symbol-rendercodelang]

**Input:**
- `result: var string`
- `lang: SourceLanguage`
- `code: string`
- `target: OutputTarget`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### renderIndexTerm

[ref: #symbol-renderindexterm]

Renders the string decorated within `foobar`:idx: markers.

**Input:**
- `d: PDoc`
- `n: PRstNode`
- `result: var string`

**Output:** *(none)*
**Pragmas:** `raises: [Exception, ValueError, OSError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, OSError`, `tags: RootEffect`, `forbids: `

Renders the string decorated within `foobar`:idx: markers.

Additionally adds the enclosed text to the index as a term. Since we are interested in different instances of the same term to have different entries, a table is used to keep track of the amount of times a term has previously appeared to give a different identifier value for each.

### renderNimCode

[ref: #symbol-rendernimcode]

**Input:**
- `result: var string`
- `code: string`
- `target: OutputTarget`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### renderRstToOut

[ref: #symbol-renderrsttoout]

Writes into result the rst ast n using the d configuration.

**Input:**
- `d: var RstGenerator`
- `n: PRstNode`
- `result: var string`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `raises: [Exception, ValueError, OSError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, OSError`, `tags: RootEffect`, `forbids: `

Writes into result the rst ast n using the d configuration.

Before using this proc you need to initialise a RstGenerator with initRstGenerator and parse a rst file with rstParse from the [packages/docutils/rst module](rst.html). Example:

```
# ...configure gen and rst vars...
var generatedHtml = ""
renderRstToOut(gen, rst, generatedHtml)
echo generatedHtml
```

### renderTocEntries

[ref: #symbol-rendertocentries]

**Input:**
- `d: var RstGenerator`
- `j: var int`
- `lvl: int`
- `result: var string`

**Output:** *(none)*
**Pragmas:** `raises: [Exception, ValueError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError`, `tags: RootEffect`, `forbids: `

### rstToHtml

[ref: #symbol-rsttohtml]

Converts an input rst string into embeddable HTML.

**Input:**
- `s: string`
- `options: RstParseOptions`
- `config: StringTableRef`
- `msgHandler: MsgHandler = rst.defaultMsgHandler`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: [Exception, ValueError, KeyError, OSError]`, `tags: [RootEffect, ReadIOEffect, ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, KeyError, OSError`, `tags: RootEffect, ReadIOEffect, ReadEnvEffect`, `forbids: `

Converts an input rst string into embeddable HTML.

This convenience proc parses any input string using rst markup (it doesn't have to be a full document!) and returns an embeddable piece of HTML. The proc is meant to be used in *online* environments without access to a meaningful filesystem, and therefore rst include like directives won't work. For an explanation of the config parameter see the initRstGenerator proc. Example:

```
import packages/docutils/rstgen, strtabs

echo rstToHtml("*Hello* **world**!", {},
  newStringTable(modeStyleInsensitive))
# --> <em>Hello</em> <strong>world</strong>!
```

If you need to allow the rst include directive or tweak the generated output you have to create your own RstGenerator with initRstGenerator and related procs.

### rstToLatex

[ref: #symbol-rsttolatex]

**Input:**
- `rstSource: string`
- `options: RstParseOptions`

**Output:** `string`
**Pragmas:** `inline`, `raises: [Exception, ValueError, KeyError, OSError]`, `tags: [RootEffect, ReadIOEffect, ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, KeyError, OSError`, `tags: RootEffect, ReadIOEffect, ReadEnvEffect`, `forbids: `

Convenience proc for renderRstToOut and initRstGenerator.

### setIndexTerm

[ref: #symbol-setindexterm]

Adds a term to the index using the specified hyperlink identifier.

**Input:**
- `d: var RstGenerator`
- `k: IndexEntryKind`
- `htmlFile: string`
- `id: string`
- `term: string`
- `linkTitle:  = ""`
- `linkDesc:  = ""`
- `line:  = 0`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds a term to the index using the specified hyperlink identifier.

A new entry will be added to the index using the format term<tab>file#id. The file part will come from the htmlFile parameter.

The id will be appended with a hash character only if its length is not zero, otherwise no specific anchor will be generated. In general you should only pass an empty id value for the title of standalone rst documents (they are special for the [mergeIndexes()](#mergeIndexes,string) proc, see [Index (idx) file format](docgen.html#index-idx-file-format) for more information). Unlike other index terms, title entries are inserted at the beginning of the accumulated buffer to maintain a logical order of entries.

If linkTitle or linkDesc are not the empty string, two additional columns with their contents will be added.

The index won't be written to disk unless you call [writeIndexFile()](#writeIndexFile,RstGenerator,string). The purpose of the index is documented in the [docgen tools guide](docgen.html#related-options-index-switch).

### traverseForIndex

[ref: #symbol-traverseforindex]

**Input:**
- `d: PDoc`
- `n: PRstNode`

**Output:** *(none)*
**Pragmas:** `raises: [Exception, ValueError, OSError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception, ValueError, OSError`, `tags: RootEffect`, `forbids: `

A version of [renderRstToOut](#renderRstToOut) that only fills entries for .idx files.

### writeIndexFile

[ref: #symbol-writeindexfile]

Writes the current index buffer to the specified output file.

**Input:**
- `g: var RstGenerator`
- `outfile: string`

**Output:** *(none)*
**Pragmas:** `raises: [IOError]`, `tags: [WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError`, `tags: WriteIOEffect`, `forbids: `

Writes the current index buffer to the specified output file.

You previously need to add entries to the index with the [setIndexTerm()](#setIndexTerm,RstGenerator,string,string,string,string,string) proc. If the index is empty the file won't be created.

## Type

### EscapeMode

[ref: #symbol-escapemode]

```nim
EscapeMode = enum
  emText, emOption, emUrl
```

### IndexedDocs

[ref: #symbol-indexeddocs]

Contains the index sequences for doc types.

```nim
IndexedDocs = Table[IndexEntry, seq[IndexEntry]]
```

Contains the index sequences for doc types.

The key is a *fake* IndexEntry which will contain the title of the document in the keyword field and link will contain the html filename for the document. linkTitle and linkDesc will be empty.

The value indexed by this IndexEntry is a sequence with the real index entries found in the .idx file.

### MetaEnum

[ref: #symbol-metaenum]

```nim
MetaEnum = enum
  metaNone, metaTitleRaw, metaTitle, metaSubtitle, metaAuthor, metaVersion
```

### OutputTarget

[ref: #symbol-outputtarget]

```nim
OutputTarget = enum
  outHtml, outLatex
```

which document type to generate

### RstGenerator

[ref: #symbol-rstgenerator]

```nim
RstGenerator = object of RootObj
  target*: OutputTarget
  config*: StringTableRef
  splitAfter*: int
  listingCounter*: int
  tocPart*: seq[PRstNode]
  hasToc*: bool
  findFile*: FindFileHandler
  msgHandler*: MsgHandler
  outDir*: string            ## output directory, initialized by docgen.nim
  destFile*: string          ## output (HTML) file, initialized by docgen.nim
  filenames*: RstFileTable
  filename*: string          ## source Nim or Rst file
  meta*: array[MetaEnum, string]
  id*: int                   ## A counter useful for generating IDs.
  onTestSnippet*: proc (d: var RstGenerator; filename, cmd: string; status: int;
                        content: string) {.gcsafe.}
  escMode*: EscapeMode
```
