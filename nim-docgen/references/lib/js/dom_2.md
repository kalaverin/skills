---
source_hash: d99fa24c025b2846
source_path: lib/js/dom.nim
---

### getAttributeNode

[ref: #symbol-getattributenode]

**Input:**
- `n: Node`
- `attr: cstring`

**Output:** `Node`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getBoundingClientRect

[ref: #symbol-getboundingclientrect]

**Input:**
- `e: Node`

**Output:** `BoundingRect`
**Pragmas:** `importcpp: "getBoundingClientRect"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getComputedStyle

[ref: #symbol-getcomputedstyle]

**Warning:**

**Input:**
- `w: Window`
- `e: Node`
- `pe: Node = nil`

**Output:** `Style`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

**Warning:**
The returned Style may or may not be read-only at run-time in the browser. getComputedStyle is performance costly.

### getData

[ref: #symbol-getdata]

**Input:**
- `dt: DataTransfer`
- `format: cstring`

**Output:** `cstring`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getElementById

[ref: #symbol-getelementbyid]

**Input:**
- `id: cstring`

**Output:** `Element`
**Pragmas:** `importc: "document.getElementById"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getElementById

[ref: #symbol-getelementbyid]

**Input:**
- `d: Document`
- `id: cstring`

**Output:** `Element`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getElementsByClass

[ref: #symbol-getelementsbyclass]

**Input:**
- `n: Node`
- `name: cstring`

**Output:** `seq[Node]`
**Pragmas:** `importcpp: "#.getElementsByClassName(#)"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getElementsByClassName

[ref: #symbol-getelementsbyclassname]

**Input:**
- `d: Document`
- `name: cstring`

**Output:** `seq[Element]`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getElementsByClassName

[ref: #symbol-getelementsbyclassname]

**Input:**
- `e: Element`
- `name: cstring`

**Output:** `seq[Element]`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getElementsByName

[ref: #symbol-getelementsbyname]

**Input:**
- `d: Document`
- `name: cstring`

**Output:** `seq[Element]`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getElementsByTagName

[ref: #symbol-getelementsbytagname]

**Input:**
- `d: Document`
- `name: cstring`

**Output:** `seq[Element]`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getElementsByTagName

[ref: #symbol-getelementsbytagname]

**Input:**
- `e: Element`
- `name: cstring`

**Output:** `seq[Element]`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getItem

[ref: #symbol-getitem]

**Input:**
- `s: Storage`
- `key: cstring`

**Output:** `cstring`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getModifierState

[ref: #symbol-getmodifierstate]

**Input:**
- `ev: KeyboardEvent`
- `keyArg: cstring`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getModifierState

[ref: #symbol-getmodifierstate]

**Input:**
- `ev: MouseEvent`
- `keyArg: cstring`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getPropertyPriority

[ref: #symbol-getpropertypriority]

**Input:**
- `s: Style`
- `property: cstring`

**Output:** `cstring`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getPropertyValue

[ref: #symbol-getpropertyvalue]

**Input:**
- `s: Style`
- `property: cstring`

**Output:** `cstring`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getRangeAt

[ref: #symbol-getrangeat]

**Input:**
- `s: Selection`
- `index: int`

**Output:** `Range`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getRootNode

[ref: #symbol-getrootnode]

**Input:**
- `n: Node`
- `options: RootNodeOptions`

**Output:** `Node`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getSelection

[ref: #symbol-getselection]

**Input:**
- `n: DocumentOrShadowRoot`

**Output:** `Selection`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getSelection

[ref: #symbol-getselection]

**Input:**
- `d: Document`

**Output:** `Selection`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### go

[ref: #symbol-go]

**Input:**
- `h: History`
- `pagesToJump: int`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### handleEvent

[ref: #symbol-handleevent]

**Input:**
- `w: Window`
- `e: Event`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### handleEvent

[ref: #symbol-handleevent]

**Input:**
- `d: Document`
- `event: Event`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### handleEvent

[ref: #symbol-handleevent]

**Input:**
- `e: Element`
- `event: Event`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### hasAttribute

[ref: #symbol-hasattribute]

**Input:**
- `n: Node`
- `attr: cstring`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### hasAttributeNS

[ref: #symbol-hasattributens]

**Input:**
- `self: Node`
- `namespace: cstring`
- `localName: cstring`

**Output:** `bool`
**Pragmas:** `importjs: "(#.$1(#, #) || false)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/hasAttributeNS>

### hasChildNodes

[ref: #symbol-haschildnodes]

**Input:**
- `n: Node`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### hasPointerCapture

[ref: #symbol-haspointercapture]

**Input:**
- `self: Node`
- `pointerId: SomeNumber`

**Output:** `bool`
**Generic parameters:** `SomeNumber`

**Pragmas:** `importjs: "(#.$1(#) || false)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/hasPointerCapture>

### home

[ref: #symbol-home]

**Input:**
- `w: Window`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### id

[ref: #symbol-id]

**Input:**
- `n: Node`

**Output:** `cstring`
**Pragmas:** `importcpp: "#.id"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### id=

[ref: #symbol-id]

**Input:**
- `n: Node`
- `x: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp: "#.id = #"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### identifiedTouch

[ref: #symbol-identifiedtouch]

**Input:**
- `list: TouchList`

**Output:** `Touch`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### insertAdjacentElement

[ref: #symbol-insertadjacentelement]

**Input:**
- `self: Node`
- `position: cstring`
- `element: Node`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentElement>

### insertAdjacentHTML

[ref: #symbol-insertadjacenthtml]

**Input:**
- `self: Node`
- `position: cstring`
- `html: cstring`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentHTML>

### insertAdjacentText

[ref: #symbol-insertadjacenttext]

**Input:**
- `self: Node`
- `position: cstring`
- `data: cstring`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentText>

### insertBefore

[ref: #symbol-insertbefore]

**Input:**
- `n: Node`
- `newNode: Node`
- `before: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### insertData

[ref: #symbol-insertdata]

**Input:**
- `n: Node`
- `position: int`
- `data: cstring`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### insertNode

[ref: #symbol-insertnode]

**Input:**
- `range: Range`
- `node: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### inViewport

[ref: #symbol-inviewport]

**Input:**
- `el: Node`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isDefaultNamespace

[ref: #symbol-isdefaultnamespace]

**Input:**
- `n: Node`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isEqualNode

[ref: #symbol-isequalnode]

**Input:**
- `n: Node`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isFinite

[ref: #symbol-isfinite]

**Input:**
- `x: BiggestFloat`

**Output:** `bool`
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isNaN

[ref: #symbol-isnan]

**Input:**
- `x: BiggestFloat`

**Output:** `bool`
**Pragmas:** `importc`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

see also math.isNaN.

### isSameNode

[ref: #symbol-issamenode]

**Input:**
- `n: Node`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### item

[ref: #symbol-item]

**Input:**
- `list: TouchList`
- `i: int`

**Output:** `Touch`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### javaEnabled

[ref: #symbol-javaenabled]

**Input:**
- `h: Navigator`

**Output:** `bool`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### len

[ref: #symbol-len]

**Input:**
- `x: Node`

**Output:** `int`
**Pragmas:** `importcpp: "#.childNodes.length"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### lookupNamespaceURI

[ref: #symbol-lookupnamespaceuri]

**Input:**
- `n: Node`

**Output:** `cstring`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### lookupPrefix

[ref: #symbol-lookupprefix]

**Input:**
- `n: Node`

**Output:** `cstring`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### matches

[ref: #symbol-matches]

**Input:**
- `self: Node`
- `cssSelector: cstring`

**Output:** `bool`
**Pragmas:** `importjs: "(#.$1(#) || false)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Element/matches>

### matchMedia

[ref: #symbol-matchmedia]

**Input:**
- `w: Window`
- `mediaQueryString: cstring`

**Output:** `MediaQueryList`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### message

[ref: #symbol-message]

**Input:**
- `ex: DomException`

**Output:** `cstring`
**Pragmas:** `importcpp: "#.message"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/DOMException/message>

### moveBy

[ref: #symbol-moveby]

**Input:**
- `w: Window`
- `x: int`
- `y: int`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### moveTo

[ref: #symbol-moveto]

**Input:**
- `w: Window`
- `x: int`
- `y: int`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### name

[ref: #symbol-name]

**Input:**
- `ex: DomException`

**Output:** `cstring`
**Pragmas:** `importcpp: "#.name"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/DOMException/name>

### newDomException

[ref: #symbol-newdomexception]

**Input:**
- *(none)*

**Output:** `DomException`
**Pragmas:** `importcpp: "new DomException()"`, `constructor`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

DOM Exception constructor

### newDomParser

[ref: #symbol-newdomparser]

**Input:**
- *(none)*

**Output:** `DomParser`
**Pragmas:** `importcpp: "new DOMParser()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

DOM Parser constructor.

### newEvent

[ref: #symbol-newevent]

**Input:**
- `name: cstring`

**Output:** `Event`
**Pragmas:** `importcpp: "new Event(@)"`, `constructor`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newFileReader

[ref: #symbol-newfilereader]

**Input:**
- *(none)*

**Output:** `FileReader`
**Pragmas:** `importcpp: "new FileReader()"`, `constructor`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

File Reader constructor

### normalize

[ref: #symbol-normalize]

**Input:**
- `n: Node`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### now

[ref: #symbol-now]

**Input:**
- `p: Performance`

**Output:** `float`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### offsetHeight

[ref: #symbol-offsetheight]

**Input:**
- `e: Node`

**Output:** `int`
**Pragmas:** `importcpp: "#.offsetHeight"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### offsetLeft

[ref: #symbol-offsetleft]

**Input:**
- `e: Node`

**Output:** `int`
**Pragmas:** `importcpp: "#.offsetLeft"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### offsetTop

[ref: #symbol-offsettop]

**Input:**
- `e: Node`

**Output:** `int`
**Pragmas:** `importcpp: "#.offsetTop"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### offsetWidth

[ref: #symbol-offsetwidth]

**Input:**
- `e: Node`

**Output:** `int`
**Pragmas:** `importcpp: "#.offsetWidth"`, `nodecl`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### open

[ref: #symbol-open]

**Input:**
- `w: Window`
- `uri: cstring`
- `windowname: cstring`
- `properties: cstring = nil`

**Output:** `Window`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### open

[ref: #symbol-open]

**Input:**
- `d: Document`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### parseFromString

[ref: #symbol-parsefromstring]

**Input:**
- `this: DomParser`
- `str: cstring`
- `mimeType: cstring`

**Output:** `Document`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parse from string to Document.

### play

[ref: #symbol-play]

**Input:**
- `e: EmbedElement`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### preventDefault

[ref: #symbol-preventdefault]

**Input:**
- `ev: Event`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### print

[ref: #symbol-print]

**Input:**
- `w: Window`

**Output:** *(none)*
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### prompt

[ref: #symbol-prompt]

**Input:**
- `w: Window`
- `text: cstring`
- `default: cstring`

**Output:** `cstring`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pushState

[ref: #symbol-pushstate]

**Input:**
- `h: History`
- `stateObject: T`
- `title: cstring`
- `url: cstring`

**Output:** *(none)*
**Generic parameters:** `T`

**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### querySelector

[ref: #symbol-queryselector]

**Input:**
- `n: Node`
- `selectors: cstring`

**Output:** `Element`
**Pragmas:** `importcpp`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Prev](dom_1.md) | [Next](dom_3.md)
