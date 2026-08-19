---
source_hash: 1aabfd1743eb8691
source_path: lib/pure/htmlparser.nim
---

# htmlparser

[ref: #module-htmlparser]

**NOTE**: The behaviour might change in future versions as it is not clear what "*wild* HTML the real world uses" really implies.

It can be used to parse a wild HTML document and output it as valid XHTML document (well, if you are lucky):

```
echo loadHtml("mydirty.html")
```

Every tag in the resulting tree is in lower case.

**Note:** The resulting XmlNode already uses the clientData field, so it cannot be used by clients of this library.

# [Example: Transforming hyperlinks](#examplecolon-transforming-hyperlinks)

This code demonstrates how you can iterate over all the tags in an HTML file and write back the modified version. In this case we look for hyperlinks ending with the extension .rst and convert them to .html.

```
import std/htmlparser
import std/xmltree  # To use '$' for XmlNode
import std/strtabs  # To access XmlAttributes
import std/os       # To use splitFile
import std/strutils # To use cmpIgnoreCase

proc transformHyperlinks() =
  let html = loadHtml("input.html")
  
  for a in html.findAll("a"):
    if a.attrs.hasKey "href":
      let (dir, filename, ext) = splitFile(a.attrs["href"])
      if cmpIgnoreCase(ext, ".rst") == 0:
        a.attrs["href"] = dir / filename & ".html"
  
  writeFile("output.html", $html)
```

## Examples

```nim
echo loadHtml("mydirty.html")
```

```nim
import std/htmlparser
import std/xmltree  # To use '$' for XmlNode
import std/strtabs  # To access XmlAttributes
import std/os       # To use splitFile
import std/strutils # To use cmpIgnoreCase

proc transformHyperlinks() =
  let html = loadHtml("input.html")
  
  for a in html.findAll("a"):
    if a.attrs.hasKey "href":
      let (dir, filename, ext) = splitFile(a.attrs["href"])
      if cmpIgnoreCase(ext, ".rst") == 0:
        a.attrs["href"] = dir / filename & ".html"
  
  writeFile("output.html", $html)
```

```nim
import std/unicode
doAssert entityToRune("") == Rune(0)
doAssert entityToRune("a") == Rune(0)
doAssert entityToRune("gt") == ">".runeAt(0)
doAssert entityToRune("Uuml") == "Ü".runeAt(0)
doAssert entityToRune("quest") == "?".runeAt(0)
doAssert entityToRune("#x0003F") == "?".runeAt(0)
```

```nim
const sigma = "Σ"
doAssert entityToUtf8("") == ""
doAssert entityToUtf8("a") == ""
doAssert entityToUtf8("gt") == ">"
doAssert entityToUtf8("Uuml") == "Ü"
doAssert entityToUtf8("quest") == "?"
doAssert entityToUtf8("#63") == "?"
doAssert entityToUtf8("Sigma") == sigma
doAssert entityToUtf8("#931") == sigma
doAssert entityToUtf8("#0931") == sigma
doAssert entityToUtf8("#x3A3") == sigma
doAssert entityToUtf8("#x03A3") == sigma
doAssert entityToUtf8("#x3a3") == sigma
doAssert entityToUtf8("#X3a3") == sigma
```

```nim
import std/unicode
doAssert runeToEntity(Rune(0)) == ""
doAssert runeToEntity(Rune(-1)) == ""
doAssert runeToEntity("Ü".runeAt(0)) == "#220"
doAssert runeToEntity("∈".runeAt(0)) == "#8712"
```

## Const

### BlockTags

[ref: #symbol-blocktags]

```nim
BlockTags = {tagAddress, tagBlockquote, tagCenter, tagDel, tagDir, tagDiv,
             tagDl, tagFieldset, tagForm, tagH1, tagH2, tagH3, tagH4, tagH5,
             tagH6, tagHr, tagIns, tagIsindex, tagMenu, tagNoframes,
             tagNoscript, tagOl, tagP, tagPre, tagTable, tagUl, tagCenter,
             tagDir, tagIsindex, tagMenu, tagNoframes}
```

### InlineTags

[ref: #symbol-inlinetags]

```nim
InlineTags = {tagA, tagAbbr, tagAcronym, tagApplet, tagB, tagBasefont, tagBdo,
              tagBig, tagBr, tagButton, tagCite, tagCode, tagDel, tagDfn, tagEm,
              tagFont, tagI, tagImg, tagIns, tagInput, tagIframe, tagKbd,
              tagLabel, tagMap, tagObject, tagQ, tagSamp, tagScript, tagSelect,
              tagSmall, tagSpan, tagStrong, tagSub, tagSup, tagTextarea, tagTt,
              tagVar, tagApplet, tagBasefont, tagFont, tagIframe, tagU, tagS,
              tagStrike, tagWbr}
```

### SingleTags

[ref: #symbol-singletags]

```nim
SingleTags = {tagArea, tagBase, tagBasefont, tagBr, tagCol, tagFrame, tagHr,
              tagImg, tagIsindex, tagLink, tagMeta, tagParam, tagWbr, tagSource}
```

### tagToStr

[ref: #symbol-tagtostr]

```nim
tagToStr = ["a", "abbr", "acronym", "address", "applet", "area", "article",
            "aside", "audio", "b", "base", "basefont", "bdi", "bdo", "big",
            "blockquote", "body", "br", "button", "canvas", "caption", "center",
            "cite", "code", "col", "colgroup", "command", "datalist", "dd",
            "del", "details", "dfn", "dialog", "div", "dir", "dl", "dt", "em",
            "embed", "fieldset", "figcaption", "figure", "font", "footer",
            "form", "frame", "frameset", "h1", "h2", "h3", "h4", "h5", "h6",
            "head", "header", "hgroup", "html", "hr", "i", "iframe", "img",
            "input", "ins", "isindex", "kbd", "keygen", "label", "legend", "li",
            "link", "map", "mark", "menu", "meta", "meter", "nav", "nobr",
            "noframes", "noscript", "object", "ol", "optgroup", "option",
            "output", "p", "param", "pre", "progress", "q", "rp", "rt", "ruby",
            "s", "samp", "script", "section", "select", "small", "source",
            "span", "strike", "strong", "style", "sub", "summary", "sup",
            "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time",
            "title", "tr", "track", "tt", "u", "ul", "var", "video", "wbr"]
```

## Proc

### entityToRune

[ref: #symbol-entitytorune]

**Input:**
- `entity: string`

**Output:** `Rune`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts an HTML entity name like &Uuml; or values like &#220; or &#x000DC; to its UTF-8 equivalent. Rune(0) is returned if the entity name is unknown.

### entityToUtf8

[ref: #symbol-entitytoutf8]

**Input:**
- `entity: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts an HTML entity name like &Uuml; or values like &#220; or &#x000DC; to its UTF-8 equivalent. "" is returned if the entity name is unknown. The HTML parser already converts entities to UTF-8.

### htmlTag

[ref: #symbol-htmltag]

**Input:**
- `n: XmlNode`

**Output:** `HtmlTag`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets n's tag as a HtmlTag.

### htmlTag

[ref: #symbol-htmltag]

**Input:**
- `s: string`

**Output:** `HtmlTag`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts s to a HtmlTag. If s is no HTML tag, tagUnknown is returned.

### loadHtml

[ref: #symbol-loadhtml]

**Input:**
- `path: string`
- `errors: var seq[string]`

**Output:** `XmlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, Exception]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, Exception`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Loads and parses HTML from file specified by path, and returns a XmlNode. Every occurred parsing error is added to the errors sequence.

### loadHtml

[ref: #symbol-loadhtml]

**Input:**
- `path: string`

**Output:** `XmlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, Exception]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, Exception`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Loads and parses HTML from file specified by path, and returns a XmlNode. All parsing errors are ignored.

### parseHtml

[ref: #symbol-parsehtml]

**Input:**
- `s: Stream`
- `filename: string`
- `errors: var seq[string]`

**Output:** `XmlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, Exception]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, Exception`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Parses the XML from stream s and returns a XmlNode. Every occurred parsing error is added to the errors sequence.

### parseHtml

[ref: #symbol-parsehtml]

**Input:**
- `s: Stream`

**Output:** `XmlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, Exception]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, Exception`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Parses the HTML from stream s and returns a XmlNode. All parsing errors are ignored.

### parseHtml

[ref: #symbol-parsehtml]

**Input:**
- `html: string`

**Output:** `XmlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, Exception]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, Exception`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

Parses the HTML from string html and returns a XmlNode. All parsing errors are ignored.

### runeToEntity

[ref: #symbol-runetoentity]

**Input:**
- `rune: Rune`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

converts a Rune to its numeric HTML entity equivalent.

## Type

### HtmlTag

[ref: #symbol-htmltag]

```nim
HtmlTag = enum
  tagUnknown,               ## unknown HTML element
  tagA,                     ## the HTML `a` element
  tagAbbr,                  ## the deprecated HTML `abbr` element
  tagAcronym,               ## the HTML `acronym` element
  tagAddress,               ## the HTML `address` element
  tagApplet,                ## the deprecated HTML `applet` element
  tagArea,                  ## the HTML `area` element
  tagArticle,               ## the HTML `article` element
  tagAside,                 ## the HTML `aside` element
  tagAudio,                 ## the HTML `audio` element
  tagB,                     ## the HTML `b` element
  tagBase,                  ## the HTML `base` element
  tagBdi,                   ## the HTML `bdi` element
  tagBdo,                   ## the deprecated HTML `dbo` element
  tagBasefont,              ## the deprecated HTML `basefont` element
  tagBig,                   ## the HTML `big` element
  tagBlockquote,            ## the HTML `blockquote` element
  tagBody,                  ## the HTML `body` element
  tagBr,                    ## the HTML `br` element
  tagButton,                ## the HTML `button` element
  tagCanvas,                ## the HTML `canvas` element
  tagCaption,               ## the HTML `caption` element
  tagCenter,                ## the deprecated HTML `center` element
  tagCite,                  ## the HTML `cite` element
  tagCode,                  ## the HTML `code` element
  tagCol,                   ## the HTML `col` element
  tagColgroup,              ## the HTML `colgroup` element
  tagCommand,               ## the HTML `command` element
  tagDatalist,              ## the HTML `datalist` element
  tagDd,                    ## the HTML `dd` element
  tagDel,                   ## the HTML `del` element
  tagDetails,               ## the HTML `details` element
  tagDfn,                   ## the HTML `dfn` element
  tagDialog,                ## the HTML `dialog` element
  tagDiv,                   ## the HTML `div` element
  tagDir,                   ## the deprecated HTLM `dir` element
  tagDl,                    ## the HTML `dl` element
  tagDt,                    ## the HTML `dt` element
  tagEm,                    ## the HTML `em` element
  tagEmbed,                 ## the HTML `embed` element
  tagFieldset,              ## the HTML `fieldset` element
  tagFigcaption,            ## the HTML `figcaption` element
  tagFigure,                ## the HTML `figure` element
  tagFont,                  ## the deprecated HTML `font` element
  tagFooter,                ## the HTML `footer` element
  tagForm,                  ## the HTML `form` element
  tagFrame,                 ## the HTML `frame` element
  tagFrameset,              ## the deprecated HTML `frameset` element
  tagH1,                    ## the HTML `h1` element
  tagH2,                    ## the HTML `h2` element
  tagH3,                    ## the HTML `h3` element
  tagH4,                    ## the HTML `h4` element
  tagH5,                    ## the HTML `h5` element
  tagH6,                    ## the HTML `h6` element
  tagHead,                  ## the HTML `head` element
  tagHeader,                ## the HTML `header` element
  tagHgroup,                ## the HTML `hgroup` element
  tagHtml,                  ## the HTML `html` element
  tagHr,                    ## the HTML `hr` element
  tagI,                     ## the HTML `i` element
  tagIframe,                ## the deprecated HTML `iframe` element
  tagImg,                   ## the HTML `img` element
  tagInput,                 ## the HTML `input` element
  tagIns,                   ## the HTML `ins` element
  tagIsindex,               ## the deprecated HTML `isindex` element
  tagKbd,                   ## the HTML `kbd` element
  tagKeygen,                ## the HTML `keygen` element
  tagLabel,                 ## the HTML `label` element
  tagLegend,                ## the HTML `legend` element
  tagLi,                    ## the HTML `li` element
  tagLink,                  ## the HTML `link` element
  tagMap,                   ## the HTML `map` element
  tagMark,                  ## the HTML `mark` element
  tagMenu,                  ## the deprecated HTML `menu` element
  tagMeta,                  ## the HTML `meta` element
  tagMeter,                 ## the HTML `meter` element
  tagNav,                   ## the HTML `nav` element
  tagNobr,                  ## the deprecated HTML `nobr` element
  tagNoframes,              ## the deprecated HTML `noframes` element
  tagNoscript,              ## the HTML `noscript` element
  tagObject,                ## the HTML `object` element
  tagOl,                    ## the HTML `ol` element
  tagOptgroup,              ## the HTML `optgroup` element
  tagOption,                ## the HTML `option` element
  tagOutput,                ## the HTML `output` element
  tagP,                     ## the HTML `p` element
  tagParam,                 ## the HTML `param` element
  tagPre,                   ## the HTML `pre` element
  tagProgress,              ## the HTML `progress` element
  tagQ,                     ## the HTML `q` element
  tagRp,                    ## the HTML `rp` element
  tagRt,                    ## the HTML `rt` element
  tagRuby,                  ## the HTML `ruby` element
  tagS,                     ## the deprecated HTML `s` element
  tagSamp,                  ## the HTML `samp` element
  tagScript,                ## the HTML `script` element
  tagSection,               ## the HTML `section` element
  tagSelect,                ## the HTML `select` element
  tagSmall,                 ## the HTML `small` element
  tagSource,                ## the HTML `source` element
  tagSpan,                  ## the HTML `span` element
  tagStrike,                ## the deprecated HTML `strike` element
  tagStrong,                ## the HTML `strong` element
  tagStyle,                 ## the HTML `style` element
  tagSub,                   ## the HTML `sub` element
  tagSummary,               ## the HTML `summary` element
  tagSup,                   ## the HTML `sup` element
  tagTable,                 ## the HTML `table` element
  tagTbody,                 ## the HTML `tbody` element
  tagTd,                    ## the HTML `td` element
  tagTextarea,              ## the HTML `textarea` element
  tagTfoot,                 ## the HTML `tfoot` element
  tagTh,                    ## the HTML `th` element
  tagThead,                 ## the HTML `thead` element
  tagTime,                  ## the HTML `time` element
  tagTitle,                 ## the HTML `title` element
  tagTr,                    ## the HTML `tr` element
  tagTrack,                 ## the HTML `track` element
  tagTt,                    ## the HTML `tt` element
  tagU,                     ## the deprecated HTML `u` element
  tagUl,                    ## the HTML `ul` element
  tagVar,                   ## the HTML `var` element
  tagVideo,                 ## the HTML `video` element
  tagWbr                     ## the HTML `wbr` element
```

list of all supported HTML tags; order will always be alphabetically
