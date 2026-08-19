---
source_hash: 2dc68f55f4b39cfe
source_path: lib/pure/xmltree.nim
---

### newElement

[ref: #symbol-newelement]

Creates a new XmlNode of kind xnElement with the given tag.

**Input:**
- `tag: sink string`

**Output:** `XmlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new XmlNode of kind xnElement with the given tag.

See also:

* [newXmlTree proc](#newXmlTree,string,openArray[XmlNode],XmlAttributes)
* [<> macro](#<>.m,untyped)

### newEntity

[ref: #symbol-newentity]

**Input:**
- `entity: string`

**Output:** `XmlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new XmlNode of kind xnEntity with the text entity.

### newText

[ref: #symbol-newtext]

**Input:**
- `text: sink string`

**Output:** `XmlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new XmlNode of kind xnText with the text text.

### newVerbatimText

[ref: #symbol-newverbatimtext]

**Input:**
- `text: sink string`

**Output:** `XmlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new XmlNode of kind xnVerbatimText with the text text. **Since**: Version 1.3.

### newXmlTree

[ref: #symbol-newxmltree]

Creates a new XML tree with tag, children and attributes.

**Input:**
- `tag: sink string`
- `children: openArray[XmlNode]`
- `attributes: XmlAttributes = nil`

**Output:** `XmlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new XML tree with tag, children and attributes.

See also:

* [newElement proc](#newElement,string)
* [<> macro](#<>.m,untyped)

### rawTag

[ref: #symbol-rawtag]

Returns the underlying 'tag' string by reference.

**Input:**
- `n: XmlNode`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the underlying 'tag' string by reference.

This is only used for speed hacks.

### rawText

[ref: #symbol-rawtext]

Returns the underlying 'text' string by reference.

**Input:**
- `n: XmlNode`

**Output:** `string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the underlying 'text' string by reference.

This is only used for speed hacks.

### replace

[ref: #symbol-replace]

Replaces the i'th child of n with replacement openArray.

**Input:**
- `n: XmlNode`
- `i: Natural`
- `replacement: openArray[XmlNode]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Replaces the i'th child of n with replacement openArray.

n must be of xnElement kind.

See also:

* [replace proc](#replace.XmlNode,Slice[int],openArray[XmlNode])
* [add proc](#add,XmlNode,XmlNode)
* [add proc](#add,XmlNode,openArray[XmlNode])
* [delete proc](#delete,XmlNode,Natural)
* [delete proc](#delete.XmlNode,Slice[int])
* [insert proc](#insert,XmlNode,XmlNode,int)
* [insert proc](#insert,XmlNode,openArray[XmlNode],int)

### replace

[ref: #symbol-replace]

Deletes the items n[slice] of n.

**Input:**
- `n: XmlNode`
- `slice: Slice[int]`
- `replacement: openArray[XmlNode]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Deletes the items n[slice] of n.

n must be of xnElement kind.

See also:

* [replace proc](#replace.XmlNode,int,openArray[XmlNode])
* [add proc](#add,XmlNode,XmlNode)
* [add proc](#add,XmlNode,openArray[XmlNode])
* [delete proc](#delete,XmlNode,Natural)
* [delete proc](#delete.XmlNode,Slice[int])
* [insert proc](#insert,XmlNode,XmlNode,int)
* [insert proc](#insert,XmlNode,openArray[XmlNode],int)

### tag

[ref: #symbol-tag]

Gets the tag name of n.

**Input:**
- `n: XmlNode`

**Output:** `lent string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the tag name of n.

n has to be an xnElement node.

See also:

* [text proc](#text,XmlNode) for text getter
* [text= proc](#text=,XmlNode,string) for text setter
* [tag= proc](#tag=,XmlNode,string) for tag setter
* [innerText proc](#innerText,XmlNode)

### tag=

[ref: #symbol-tag]

Sets the tag name of n.

**Input:**
- `n: XmlNode`
- `tag: sink string`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the tag name of n.

n has to be an xnElement node.

See also:

* [text proc](#text,XmlNode) for text getter
* [text= proc](#text=,XmlNode,string) for text setter
* [tag proc](#tag,XmlNode) for tag getter

### text

[ref: #symbol-text]

Gets the associated text with the node n.

**Input:**
- `n: XmlNode`

**Output:** `lent string`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the associated text with the node n.

n can be a CDATA, Text, comment, or entity node.

See also:

* [text= proc](#text=,XmlNode,string) for text setter
* [tag proc](#tag,XmlNode) for tag getter
* [tag= proc](#tag=,XmlNode,string) for tag setter
* [innerText proc](#innerText,XmlNode)

### text=

[ref: #symbol-text]

Sets the associated text with the node n.

**Input:**
- `n: XmlNode`
- `text: sink string`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the associated text with the node n.

n can be a CDATA, Text, comment, or entity node.

See also:

* [text proc](#text,XmlNode) for text getter
* [tag proc](#tag,XmlNode) for tag getter
* [tag= proc](#tag=,XmlNode,string) for tag setter

### toXmlAttributes

[ref: #symbol-toxmlattributes]

**Input:**
- `keyValuePairs: varargs[tuple[key, val: string]]`

**Output:** `XmlAttributes`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts {key: value} pairs into XmlAttributes.

## Type

### XmlAttributes

[ref: #symbol-xmlattributes]

An alias for a string to string mapping.

```nim
XmlAttributes = StringTableRef
```

An alias for a string to string mapping.

Use [toXmlAttributes proc](#toXmlAttributes,varargs[tuple[string,string]]) to create XmlAttributes.

### XmlNode

[ref: #symbol-xmlnode]

An XML tree consisting of XML nodes.

```nim
XmlNode = ref XmlNodeObj
```

An XML tree consisting of XML nodes.

Use [newXmlTree proc](#newXmlTree,string,openArray[XmlNode],XmlAttributes) for creating a new tree.

### XmlNodeKind

[ref: #symbol-xmlnodekind]

```nim
XmlNodeKind = enum
  xnText,                   ## a text element
  xnVerbatimText, xnElement, ## an element with 0 or more children
  xnCData,                  ## a CDATA node
  xnEntity,                 ## an entity (like ``&thing;``)
  xnComment                  ## an XML comment
```

Different kinds of XML nodes.

[Prev](xmltree_1.md)
