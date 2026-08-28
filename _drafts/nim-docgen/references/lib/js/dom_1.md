---
source_hash: d99fa24c025b2846
source_path: lib/js/dom.nim
---

# dom

[ref: #module-dom]

Declaration of the Document Object Model for the [JavaScript backend](backends.html#backends-the-javascript-target).

# [Document Ready](#document-ready)

* Basic example of a document ready:

* This example runs 5 seconds after the document ready:

# [Document onUnload](#document-onunload)

* Simple example of how to implement code that runs when the page unloads:

# [Document Autorefresh](#document-autorefresh)

* Minimal example of a document autorefresh:

* For more examples, see <https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener>

## Examples

```nim
import std/dom
proc example(e: Event) = echo "Document is ready"
document.addEventListener("DOMContentLoaded", example)  # You can also use "load" event.
```

```nim
import std/dom
proc example() = echo "5 seconds after document ready"
proc domReady(e: Event) = discard setTimeout(example, 5_000) # Document is ready.
document.addEventListener("DOMContentLoaded", domReady)
```

```nim
import std/dom
proc example(e: Event) = echo "Document is unloaded"
document.addEventListener("unload", example)  # You can also use "beforeunload".
```

```nim
import std/dom
proc example() = window.location.reload()
discard setTimeout(example, 5_000)
```

```nim
let prsr = newDomParser()
discard prsr.parseFromString("<html><marquee>Hello World</marquee></html>".cstring, "text/html".cstring)
```

## Const

### DomApiVersion

[ref: #symbol-domapiversion]

```nim
DomApiVersion = 3
```

the version of DOM API we try to follow. No guarantees though.

### fileReaderDone

[ref: #symbol-filereaderdone]

```nim
fileReaderDone = 2'u
```

### fileReaderEmpty

[ref: #symbol-filereaderempty]

```nim
fileReaderEmpty = 0'u
```

### fileReaderLoading

[ref: #symbol-filereaderloading]

```nim
fileReaderLoading = 1'u
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `s: Selection`

**Output:** `string`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]`

[ref: #symbol-]

**Input:**
- `x: Node`
- `idx: int`

**Output:** `Element`
**Pragmas:** `importcpp: "#.childNodes[#]"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### abort

[ref: #symbol-abort]

**Input:**
- `f: FileReader`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.abort()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FileReader/abort>

### add

[ref: #symbol-add]

**Input:**
- `c: ClassList`
- `class: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### addEventListener

[ref: #symbol-addeventlistener]

**Input:**
- `et: EventTarget`
- `ev: cstring`
- `cb: proc (ev: Event)`
- `useCapture: bool = false`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### addEventListener

[ref: #symbol-addeventlistener]

**Input:**
- `et: EventTarget`
- `ev: cstring`
- `cb: proc (ev: Event)`
- `options: AddEventListenerOptions`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### after

[ref: #symbol-after]

**Input:**
- `self: Node`
- `element: Node`

**Output:** `Node`
**Pragmas:** `importjs: "#.$1(@)"`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/after>

### alert

[ref: #symbol-alert]

**Input:**
- `w: Window`
- `msg: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### append

[ref: #symbol-append]

**Input:**
- `self: Node`
- `element: Node`

**Output:** `Node`
**Pragmas:** `importjs: "#.$1(@)"`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/append>

### appendChild

[ref: #symbol-appendchild]

**Input:**
- `n: Node`
- `child: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### appendData

[ref: #symbol-appenddata]

**Input:**
- `n: Node`
- `data: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### assignedElements

[ref: #symbol-assignedelements]

**Input:**
- `n: HTMLSlotElement`
- `options: SlotOptions`

**Output:** `seq[Element]`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### assignedNodes

[ref: #symbol-assignednodes]

**Input:**
- `n: HTMLSlotElement`
- `options: SlotOptions`

**Output:** `seq[Node]`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### attachShadow

[ref: #symbol-attachshadow]

**Input:**
- `n: Element`

**Output:** `ShadowRoot`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### back

[ref: #symbol-back]

**Input:**
- `w: Window`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### back

[ref: #symbol-back]

**Input:**
- `h: History`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### before

[ref: #symbol-before]

**Input:**
- `self: Node`
- `element: Node`

**Output:** `Node`
**Pragmas:** `importjs: "#.$1(@)"`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/before>

### blur

[ref: #symbol-blur]

**Input:**
- `w: Window`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### blur

[ref: #symbol-blur]

**Input:**
- `e: Element`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cancelAnimationFrame

[ref: #symbol-cancelanimationframe]

**Input:**
- `w: Window`
- `id: int`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### canShare

[ref: #symbol-canshare]

**Input:**
- `self: Navigator`
- `data: cstring`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Navigator/canShare>

### checked

[ref: #symbol-checked]

**Input:**
- `n: Node`

**Output:** `bool`
**Pragmas:** `importcpp: "#.checked"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### checked=

[ref: #symbol-checked]

**Input:**
- `n: Node`
- `v: bool`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.checked = #"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### checkValidity

[ref: #symbol-checkvalidity]

**Input:**
- `e: FormElement`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### checkValidity

[ref: #symbol-checkvalidity]

**Input:**
- `e: InputElement`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### class

[ref: #symbol-class]

**Input:**
- `n: Node`

**Output:** `cstring`
**Pragmas:** `importcpp: "#.className"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### class=

[ref: #symbol-class]

**Input:**
- `n: Node`
- `v: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.className = #"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clear

[ref: #symbol-clear]

**Input:**
- `s: Storage`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clearData

[ref: #symbol-cleardata]

**Input:**
- `dt: DataTransfer`
- `format: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clearInterval

[ref: #symbol-clearinterval]

**Input:**
- `i: Interval`

**Output:** *(none)*
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clearInterval

[ref: #symbol-clearinterval]

**Input:**
- `w: Window`
- `interval: Interval`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clearTimeout

[ref: #symbol-cleartimeout]

**Input:**
- `t: TimeOut`

**Output:** *(none)*
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clearTimeout

[ref: #symbol-cleartimeout]

**Input:**
- `w: Window`
- `timeout: TimeOut`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### click

[ref: #symbol-click]

**Input:**
- `e: Element`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clientHeight

[ref: #symbol-clientheight]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `importcpp: "(window.innerHeight || document.documentElement.clientHeight)@"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### clientWidth

[ref: #symbol-clientwidth]

**Input:**
- *(none)*

**Output:** `int`
**Pragmas:** `importcpp: "(window.innerWidth || document.documentElement.clientWidth)@"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### cloneNode

[ref: #symbol-clonenode]

**Input:**
- `n: Node`
- `copyContent: bool`

**Output:** `Node`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### close

[ref: #symbol-close]

**Input:**
- `w: Window`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### closest

[ref: #symbol-closest]

**Input:**
- `self: Node`
- `cssSelector: cstring`

**Output:** `Node`
**Pragmas:** `importjs: "#.$1(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/closest>

### compareDocumentPosition

[ref: #symbol-comparedocumentposition]

**Input:**
- `n: Node`
- `otherNode: Node`

**Output:** `int`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### confirm

[ref: #symbol-confirm]

**Input:**
- `w: Window`
- `msg: cstring`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### contains

[ref: #symbol-contains]

**Input:**
- `n: Node`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### contains

[ref: #symbol-contains]

**Input:**
- `c: ClassList`
- `class: cstring`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createAttribute

[ref: #symbol-createattribute]

**Input:**
- `d: Document`
- `identifier: cstring`

**Output:** `Node`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createComment

[ref: #symbol-createcomment]

**Input:**
- `d: Document`
- `data: cstring`

**Output:** `Node`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createElement

[ref: #symbol-createelement]

**Input:**
- `d: Document`
- `identifier: cstring`

**Output:** `Element`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createElementNS

[ref: #symbol-createelementns]

**Input:**
- `d: Document`
- `namespaceURI: cstring`
- `qualifiedIdentifier: cstring`

**Output:** `Element`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### createTextNode

[ref: #symbol-createtextnode]

**Input:**
- `d: Document`
- `identifier: cstring`

**Output:** `Node`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### decodeURI

[ref: #symbol-decodeuri]

**Input:**
- `uri: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### decodeURIComponent

[ref: #symbol-decodeuricomponent]

**Input:**
- `uri: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### deleteData

[ref: #symbol-deletedata]

**Input:**
- `n: Node`
- `start: int`
- `len: int`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### deleteFromDocument

[ref: #symbol-deletefromdocument]

**Input:**
- `s: Selection`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### disabled=

[ref: #symbol-disabled]

**Input:**
- `n: Node`
- `v: bool`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.disabled = #"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### disableExternalCapture

[ref: #symbol-disableexternalcapture]

**Input:**
- `w: Window`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dispatchEvent

[ref: #symbol-dispatchevent]

**Input:**
- `et: EventTarget`
- `ev: Event`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### elementFromPoint

[ref: #symbol-elementfrompoint]

**Input:**
- `n: DocumentOrShadowRoot`
- `x: float`
- `y: float`

**Output:** `Element`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### elementsFromPoint

[ref: #symbol-elementsfrompoint]

**Input:**
- `n: DocumentOrShadowRoot`
- `x: float`
- `y: float`

**Output:** `seq[Element]`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### enableExternalCapture

[ref: #symbol-enableexternalcapture]

**Input:**
- `w: Window`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### encodeURI

[ref: #symbol-encodeuri]

**Input:**
- `uri: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### encodeURIComponent

[ref: #symbol-encodeuricomponent]

**Input:**
- `uri: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### error

[ref: #symbol-error]

**Input:**
- `f: FileReader`

**Output:** `DomException`
**Pragmas:** `importcpp: "#.error"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FileReader/error>

### escape

[ref: #symbol-escape]

**Input:**
- `uri: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### find

[ref: #symbol-find]

**Input:**
- `w: Window`
- `text: cstring`
- `caseSensitive:  = false`
- `backwards:  = false`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### focus

[ref: #symbol-focus]

**Input:**
- `w: Window`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### focus

[ref: #symbol-focus]

**Input:**
- `e: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### focus

[ref: #symbol-focus]

**Input:**
- `e: Element`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### forward

[ref: #symbol-forward]

**Input:**
- `w: Window`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### forward

[ref: #symbol-forward]

**Input:**
- `h: History`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getAsFile

[ref: #symbol-getasfile]

**Input:**
- `dti: DataTransferItem`

**Output:** `File`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getAttribute

[ref: #symbol-getattribute]

**Input:**
- `n: Node`
- `attr: cstring`

**Output:** `cstring`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Next](dom_2.md)
