---
source_hash: d99fa24c025b2846
source_path: lib/js/dom.nim
---

### querySelector

[ref: #symbol-queryselector]

**Input:**
- `d: Document`
- `selectors: cstring`

**Output:** `Element`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### querySelectorAll

[ref: #symbol-queryselectorall]

**Input:**
- `n: Node`
- `selectors: cstring`

**Output:** `seq[Element]`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### querySelectorAll

[ref: #symbol-queryselectorall]

**Input:**
- `d: Document`
- `selectors: cstring`

**Output:** `seq[Element]`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### readAsBinaryString

[ref: #symbol-readasbinarystring]

**Input:**
- `f: FileReader`
- `b: Blob`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.readAsBinaryString(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsBinaryString>

### readAsDataURL

[ref: #symbol-readasdataurl]

**Input:**
- `f: FileReader`
- `b: Blob`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.readAsDataURL(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsDataURL>

### readAsText

[ref: #symbol-readastext]

**Input:**
- `f: FileReader`
- `b: Blob | File`
- `encoding:  = cstring"UTF-8"`

**Output:** *(none)*
**Generic parameters:** `b:type`

**Pragmas:** `importcpp: "#.readAsText(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readAsText>

### readyState

[ref: #symbol-readystate]

**Input:**
- `f: FileReader`

**Output:** `FileReaderState`
**Pragmas:** `importcpp: "#.readyState"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FileReader/readyState>

### registerProtocolHandler

[ref: #symbol-registerprotocolhandler]

**Input:**
- `self: Navigator`
- `scheme: cstring`
- `url: cstring`
- `title: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Navigator/registerProtocolHandler>

### releasePointerCapture

[ref: #symbol-releasepointercapture]

**Input:**
- `self: Node`
- `pointerId: SomeNumber`

**Output:** *(none)*
**Generic parameters:** `SomeNumber`

**Pragmas:** `importjs: "#.$1(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/releasePointerCapture>

### reload

[ref: #symbol-reload]

**Input:**
- `loc: Location`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### remove

[ref: #symbol-remove]

**Input:**
- `child: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### remove

[ref: #symbol-remove]

**Input:**
- `c: ClassList`
- `class: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### removeAllRanges

[ref: #symbol-removeallranges]

**Input:**
- `s: Selection`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### removeAttribute

[ref: #symbol-removeattribute]

**Input:**
- `n: Node`
- `attr: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### removeAttributeNode

[ref: #symbol-removeattributenode]

**Input:**
- `n: Node`
- `attr: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### removeAttributeNS

[ref: #symbol-removeattributens]

**Input:**
- `self: Node`
- `namespace: cstring`
- `attributeName: cstring`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/removeAttributeNS>

### removeChild

[ref: #symbol-removechild]

**Input:**
- `n: Node`
- `child: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### removeEventListener

[ref: #symbol-removeeventlistener]

**Input:**
- `et: EventTarget`
- `ev: cstring`
- `cb: proc (ev: Event)`
- `useCapture: bool = false`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### removeEventListener

[ref: #symbol-removeeventlistener]

**Input:**
- `et: EventTarget`
- `ev: cstring`
- `cb: proc (ev: Event)`
- `options: AddEventListenerOptions`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### removeItem

[ref: #symbol-removeitem]

**Input:**
- `s: Storage`
- `key: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### removeProperty

[ref: #symbol-removeproperty]

**Input:**
- `s: Style`
- `property: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### replace

[ref: #symbol-replace]

**Input:**
- `loc: Location`
- `s: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### replaceChild

[ref: #symbol-replacechild]

**Input:**
- `n: Node`
- `newNode: Node`
- `oldNode: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### replaceChildren

[ref: #symbol-replacechildren]

**Input:**
- `self: Node`
- `replacements: Node`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1(@)"`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/replaceChildren>

### replaceData

[ref: #symbol-replacedata]

**Input:**
- `n: Node`
- `start: int`
- `len: int`
- `text: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### replaceWith

[ref: #symbol-replacewith]

**Input:**
- `self: Node`
- `replacements: Node`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1(@)"`, `varargs`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/replaceWith>

### reportValidity

[ref: #symbol-reportvalidity]

**Input:**
- `e: FormElement`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### requestAnimationFrame

[ref: #symbol-requestanimationframe]

**Input:**
- `w: Window`
- `function: proc (time: float)`

**Output:** `int`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### requestPointerLock

[ref: #symbol-requestpointerlock]

**Input:**
- `self: Node`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/requestPointerLock>

### reset

[ref: #symbol-reset]

**Input:**
- `f: FormElement`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### resizeBy

[ref: #symbol-resizeby]

**Input:**
- `w: Window`
- `x: int`
- `y: int`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### resizeTo

[ref: #symbol-resizeto]

**Input:**
- `w: Window`
- `x: int`
- `y: int`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### resultAsString

[ref: #symbol-resultasstring]

**Input:**
- `f: FileReader`

**Output:** `cstring`
**Pragmas:** `importcpp: "#.result"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FileReader/result>

### routeEvent

[ref: #symbol-routeevent]

**Input:**
- `w: Window`
- `event: Event`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### routeEvent

[ref: #symbol-routeevent]

**Input:**
- `d: Document`
- `event: Event`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### scrollBy

[ref: #symbol-scrollby]

**Input:**
- `w: Window`
- `x: int`
- `y: int`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### scrollHeight

[ref: #symbol-scrollheight]

**Input:**
- `e: Node`

**Output:** `int`
**Pragmas:** `importcpp: "#.scrollHeight"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### scrollIntoView

[ref: #symbol-scrollintoview]

**Input:**
- `n: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### scrollIntoView

[ref: #symbol-scrollintoview]

**Input:**
- `n: Node`
- `options: ScrollIntoViewOptions`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### scrollIntoViewIfNeeded

[ref: #symbol-scrollintoviewifneeded]

**Input:**
- `self: Node`
- `centerIfNeeded: bool`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoViewIfNeeded>

### scrollLeft

[ref: #symbol-scrollleft]

**Input:**
- `e: Node`

**Output:** `int`
**Pragmas:** `importcpp: "#.scrollLeft"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### scrollTo

[ref: #symbol-scrollto]

**Input:**
- `w: Window`
- `x: int`
- `y: int`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### scrollTop

[ref: #symbol-scrolltop]

**Input:**
- `e: Node`

**Output:** `int`
**Pragmas:** `importcpp: "#.scrollTop"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### scrollTop=

[ref: #symbol-scrolltop]

**Input:**
- `e: Node`
- `value: int`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.scrollTop = #"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### scrollWidth

[ref: #symbol-scrollwidth]

**Input:**
- `e: Node`

**Output:** `int`
**Pragmas:** `importcpp: "#.scrollWidth"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### select

[ref: #symbol-select]

**Input:**
- `e: Element`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sendBeacon

[ref: #symbol-sendbeacon]

**Input:**
- `self: Navigator`
- `url: cstring`
- `data: cstring`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon>

### setAttr

[ref: #symbol-setattr]

**Input:**
- `n: Node`
- `key: cstring`
- `val: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.setAttribute(@)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setAttribute

[ref: #symbol-setattribute]

**Input:**
- `n: Node`
- `name: cstring`
- `value: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setAttributeNode

[ref: #symbol-setattributenode]

**Input:**
- `n: Node`
- `attr: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setCustomValidity

[ref: #symbol-setcustomvalidity]

**Input:**
- `e: InputElement`
- `error: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setData

[ref: #symbol-setdata]

**Input:**
- `dt: DataTransfer`
- `format: cstring`
- `data: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setDragImage

[ref: #symbol-setdragimage]

**Input:**
- `dt: DataTransfer`
- `img: Element`
- `xOffset: int`
- `yOffset: int`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setHTML

[ref: #symbol-sethtml]

**Input:**
- `self: Node`
- `html: cstring`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTML>

### setInterval

[ref: #symbol-setinterval]

**Input:**
- `action: proc ()`
- `ms: int`

**Output:** `Interval`
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setInterval

[ref: #symbol-setinterval]

**Input:**
- `w: Window`
- `code: cstring`
- `pause: int`

**Output:** `Interval`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setInterval

[ref: #symbol-setinterval]

**Input:**
- `w: Window`
- `function: proc ()`
- `pause: int`

**Output:** `Interval`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setItem

[ref: #symbol-setitem]

**Input:**
- `s: Storage`
- `key: cstring`
- `value: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setProperty

[ref: #symbol-setproperty]

**Input:**
- `s: Style`
- `property: cstring`
- `value: cstring`
- `priority:  = ""`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setRangeText

[ref: #symbol-setrangetext]

**Input:**
- `e: InputElement`
- `replacement: cstring`
- `startindex: int = 0`
- `endindex: int = 0`
- `selectionMode: cstring = "preserve"`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setSelectionRange

[ref: #symbol-setselectionrange]

**Input:**
- `e: InputElement`
- `selectionStart: int`
- `selectionEnd: int`
- `selectionDirection: cstring = "none"`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setTimeout

[ref: #symbol-settimeout]

**Input:**
- `action: proc ()`
- `ms: int`

**Output:** `TimeOut`
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setTimeout

[ref: #symbol-settimeout]

**Input:**
- `w: Window`
- `code: cstring`
- `pause: int`

**Output:** `TimeOut`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setTimeout

[ref: #symbol-settimeout]

**Input:**
- `w: Window`
- `function: proc ()`
- `pause: int`

**Output:** `Interval`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### slice

[ref: #symbol-slice]

**Input:**
- `e: Blob`
- `startindex: int = 0`
- `endindex: int = e.size`
- `contentType: cstring = ""`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### stop

[ref: #symbol-stop]

**Input:**
- `w: Window`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### stop

[ref: #symbol-stop]

**Input:**
- `e: EmbedElement`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### stopImmediatePropagation

[ref: #symbol-stopimmediatepropagation]

**Input:**
- `ev: Event`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### stopPropagation

[ref: #symbol-stoppropagation]

**Input:**
- `ev: Event`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### submit

[ref: #symbol-submit]

**Input:**
- `f: FormElement`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toggle

[ref: #symbol-toggle]

**Input:**
- `c: ClassList`
- `class: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toggleAttribute

[ref: #symbol-toggleattribute]

**Input:**
- `self: Node`
- `name: cstring`
- `force:  = false`

**Output:** `bool`
**Pragmas:** `importjs: "(#.$1(#, #) || false)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/toggleAttribute>


[Prev](dom_2.md) | [Next](dom_4.md)
