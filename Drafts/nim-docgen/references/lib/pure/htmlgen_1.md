---
source_hash: fb3f65f2f22b3ccb
source_path: lib/pure/htmlgen.nim
---

# htmlgen

[ref: #module-htmlgen]

Do yourself a favor and import the module as from std/htmlgen import nil and then fully qualify the macros.

*Note*: The Karax project (nimble install karax) has a better way to achieve the same, see <https://github.com/pragmagic/karax/blob/master/tests/nativehtmlgen.nim> for an example.

This module implements a simple XML and HTML code generator. Each commonly used HTML tag has a corresponding macro that generates a string with its HTML representation.

# [MathML](#mathml)

[MathML](https://wikipedia.org/wiki/MathML) is supported, MathML is part of HTML5. [MathML](https://wikipedia.org/wiki/MathML) is an Standard ISO/IEC 40314 from year 2015. MathML allows you to [draw advanced math on the web](https://developer.mozilla.org/en-US/docs/Web/MathML/Element/math#Examples), [visually similar to Latex math.](https://developer.mozilla.org/en-US/docs/Web/MathML/Element/semantics#Example)

# [Examples](#examples)

```
var nim = "Nim"
echo h1(a(href="https://nim-lang.org", nim))
```

Writes the string:

```
<h1><a href="https://nim-lang.org">Nim</a></h1>
```

## Examples

```nim
var nim = "Nim"
echo h1(a(href="https://nim-lang.org", nim))
```

```nim
import std/htmlgen
let nim = "Nim"
assert h1(a(href = "https://nim-lang.org", nim)) ==
  """<h1><a href="https://nim-lang.org">Nim</a></h1>"""
assert form(action = "test", `accept-charset` = "Content-Type") ==
  """<form action="test" accept-charset="Content-Type"></form>"""


assert math(
  semantics(
    mrow(
      msup(
        mi("x"),
        mn("42")
      )
    )
  )
) == "<math><semantics><mrow><msup><mi>x</mi><mn>42</mn></msup></mrow></semantics></math>"

assert math(
  semantics(
    annotation(encoding = "application/x-tex", title = "Latex on Web", r"x^{2} + y")
  )
) == """<math><semantics><annotation encoding="application/x-tex" title="Latex on Web">x^{2} + y</annotation></semantics></math>"""
```

## Const

### ariaAttr

[ref: #symbol-ariaattr]

```nim
ariaAttr = " role "
```

HTML DOM Aria Attributes

### commonAttr

[ref: #symbol-commonattr]

```nim
commonAttr = " accesskey class contenteditable dir hidden id lang spellcheck style tabindex title translate onabort onblur oncancel oncanplay oncanplaythrough onchange onclick oncuechange ondblclick ondurationchange onemptied onended onerror onfocus oninput oninvalid onkeydown onkeypress onkeyup onload onloadeddata onloadedmetadata onloadstart onmousedown onmouseenter onmouseleave onmousemove onmouseout onmouseover onmouseup onmousewheel onpause onplay onplaying onprogress onratechange onreset onresize onscroll onseeked onseeking onselect onshow onstalled onsubmit onsuspend ontimeupdate ontoggle onvolumechange onwaiting  role "
```

HTML DOM Common Attributes

### coreAttr

[ref: #symbol-coreattr]

```nim
coreAttr = " accesskey class contenteditable dir hidden id lang spellcheck style tabindex title translate "
```

HTML DOM Core Attributes

### eventAttr

[ref: #symbol-eventattr]

```nim
eventAttr = "onabort onblur oncancel oncanplay oncanplaythrough onchange onclick oncuechange ondblclick ondurationchange onemptied onended onerror onfocus oninput oninvalid onkeydown onkeypress onkeyup onload onloadeddata onloadedmetadata onloadstart onmousedown onmouseenter onmouseleave onmousemove onmouseout onmouseover onmouseup onmousewheel onpause onplay onplaying onprogress onratechange onreset onresize onscroll onseeked onseeking onselect onshow onstalled onsubmit onsuspend ontimeupdate ontoggle onvolumechange onwaiting "
```

HTML DOM Event Attributes

## Macro

### `div`

[ref: #symbol-div]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML div element.

### `object`

[ref: #symbol-object]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML object element.

### `template`

[ref: #symbol-template]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML template element.

### `var`

[ref: #symbol-var]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML var element.

### a

[ref: #symbol-a]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML a element.

### abbr

[ref: #symbol-abbr]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML abbr element.

### address

[ref: #symbol-address]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML address element.

### annotation

[ref: #symbol-annotation]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML annotation element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/semantics>

### annotation-xml

[ref: #symbol-annotation-xml]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML annotation-xml element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/semantics>

### area

[ref: #symbol-area]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML area element.

### article

[ref: #symbol-article]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML article element.

### aside

[ref: #symbol-aside]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML aside element.

### audio

[ref: #symbol-audio]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML audio element.

### b

[ref: #symbol-b]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML b element.

### base

[ref: #symbol-base]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML base element.

### bdi

[ref: #symbol-bdi]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML bdi element.

### bdo

[ref: #symbol-bdo]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML bdo element.

### big

[ref: #symbol-big]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML big element.

### blockquote

[ref: #symbol-blockquote]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML blockquote element.

### body

[ref: #symbol-body]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML body element.

### br

[ref: #symbol-br]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML br element.

### button

[ref: #symbol-button]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML button element.

### canvas

[ref: #symbol-canvas]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML canvas element.

### caption

[ref: #symbol-caption]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML caption element.

### center

[ref: #symbol-center]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML center element.

### cite

[ref: #symbol-cite]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML cite element.

### code

[ref: #symbol-code]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML code element.

### col

[ref: #symbol-col]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML col element.

### colgroup

[ref: #symbol-colgroup]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML colgroup element.

### data

[ref: #symbol-data]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML data element.

### datalist

[ref: #symbol-datalist]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML datalist element.

### dd

[ref: #symbol-dd]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML dd element.

### del

[ref: #symbol-del]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML del element.

### details

[ref: #symbol-details]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML details element.

### dfn

[ref: #symbol-dfn]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML dfn element.

### dialog

[ref: #symbol-dialog]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML dialog element.

### dl

[ref: #symbol-dl]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML dl element.

### dt

[ref: #symbol-dt]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML dt element.

### em

[ref: #symbol-em]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML em element.

### embed

[ref: #symbol-embed]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML embed element.

### fieldset

[ref: #symbol-fieldset]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML fieldset element.

### figcaption

[ref: #symbol-figcaption]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML figcaption element.

### figure

[ref: #symbol-figure]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML figure element.

### footer

[ref: #symbol-footer]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML footer element.

### form

[ref: #symbol-form]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML form element.

### h1

[ref: #symbol-h1]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML h1 element.

### h2

[ref: #symbol-h2]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML h2 element.

### h3

[ref: #symbol-h3]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML h3 element.

### h4

[ref: #symbol-h4]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML h4 element.

### h5

[ref: #symbol-h5]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML h5 element.

### h6

[ref: #symbol-h6]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML h6 element.

### head

[ref: #symbol-head]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML head element.

### header

[ref: #symbol-header]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML header element.

### hr

[ref: #symbol-hr]

**Input:**
- *(none)*

**Output:** `untyped`
Generates the HTML hr element.

### html

[ref: #symbol-html]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML html element.

### i

[ref: #symbol-i]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML i element.

### iframe

[ref: #symbol-iframe]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML iframe element.

### img

[ref: #symbol-img]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML img element.

### input

[ref: #symbol-input]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML input element.

### ins

[ref: #symbol-ins]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML ins element.

### kbd

[ref: #symbol-kbd]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML kbd element.

### keygen

[ref: #symbol-keygen]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML keygen element.

### label

[ref: #symbol-label]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML label element.

### legend

[ref: #symbol-legend]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML legend element.

### li

[ref: #symbol-li]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML li element.

### link

[ref: #symbol-link]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML link element.

### maction

[ref: #symbol-maction]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML maction element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/maction>

### main

[ref: #symbol-main]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML main element.

### map

[ref: #symbol-map]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML map element.

### mark

[ref: #symbol-mark]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mark element.

### marquee

[ref: #symbol-marquee]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML marquee element.

### math

[ref: #symbol-math]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML math element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/math#Examples>

### menclose

[ref: #symbol-menclose]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML menclose element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/menclose>

### merror

[ref: #symbol-merror]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML merror element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/merror>

### meta

[ref: #symbol-meta]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML meta element.

### meter

[ref: #symbol-meter]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML meter element.

### mfenced

[ref: #symbol-mfenced]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mfenced element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mfenced>

### mfrac

[ref: #symbol-mfrac]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mfrac element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mfrac>

### mglyph

[ref: #symbol-mglyph]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mglyph element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mglyph>

### mi

[ref: #symbol-mi]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mi element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mi>

### mlabeledtr

[ref: #symbol-mlabeledtr]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mlabeledtr element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mlabeledtr>

### mmultiscripts

[ref: #symbol-mmultiscripts]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mmultiscripts element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mmultiscripts>

### mn

[ref: #symbol-mn]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mn element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mn>

### mo

[ref: #symbol-mo]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mo element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mo>

### mover

[ref: #symbol-mover]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mover element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mover>

### mpadded

[ref: #symbol-mpadded]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mpadded element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mpadded>

### mphantom

[ref: #symbol-mphantom]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mphantom element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mphantom>

### mroot

[ref: #symbol-mroot]

**Input:**
- `e: varargs[untyped]`

**Output:** `untyped`
Generates the HTML mroot element. MathML <https://wikipedia.org/wiki/MathML> <https://developer.mozilla.org/en-US/docs/Web/MathML/Element/mroot>


[Next](htmlgen_2.md)
