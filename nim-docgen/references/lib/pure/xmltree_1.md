---
source_hash: 2dc68f55f4b39cfe
source_path: lib/pure/xmltree.nim
---

# xmltree

[ref: #module-xmltree]

A simple XML tree generator. **See also:**

* [xmlparser module](xmlparser.html) for high-level XML parsing
* [parsexml module](parsexml.html) for low-level XML parsing
* [htmlgen module](htmlgen.html) for html code generator

## Examples

```nim
import std/xmltree
var g = newElement("myTag")
g.add newText("some text")
g.add newComment("this is comment")

var h = newElement("secondTag")
h.add newEntity("some entity")

let att = {"key1": "first value", "key2": "second value"}.toXmlAttributes
let k = newXmlTree("treeTag", [g, h], att)

doAssert $k == """<treeTag key1="first value" key2="second value">
  <myTag>some text<!-- this is comment --></myTag>
  <secondTag>&some entity;</secondTag>
</treeTag>"""
```

```nim
var f = newElement("myTag")
f.add newElement("first")
f.insert(newElement("second"), 0)
assert $f[1] == "<first />"
assert $f[0] == "<second />"
```

```nim
var f = newElement("myTag")
f.add newText("my text")
f.add newElement("sonTag")
f.add newEntity("my entity")
assert $f == "<myTag>my text<sonTag />&my entity;</myTag>"
```

```nim
var f = newElement("myTag")
f.add(@[newText("my text"), newElement("sonTag"), newEntity("my entity")])
assert $f == "<myTag>my text<sonTag />&my entity;</myTag>"
```

```nim
var
  a = newElement("firstTag")
  b = newText("my text")
  c = newComment("my comment")
  s = ""
s.add(c)
s.add(a)
s.add(b)
assert s == "<!-- my comment --><firstTag />my text"
```

```nim
var j = newElement("myTag")
let att = {"key1": "first value", "key2": "second value"}.toXmlAttributes
j.attrs = att
assert j.attr("key1") == "first value"
assert j.attr("key2") == "second value"
```

```nim
var j = newElement("myTag")
assert j.attrs == nil
let att = {"key1": "first value", "key2": "second value"}.toXmlAttributes
j.attrs = att
assert j.attrs == att
```

```nim
var j = newElement("myTag")
assert j.attrs == nil
let att = {"key1": "first value", "key2": "second value"}.toXmlAttributes
j.attrs = att
assert j.attrs == att
```

```nim
var j = newElement("myTag")
assert j.attrsLen == 0
let att = {"key1": "first value", "key2": "second value"}.toXmlAttributes
j.attrs = att
assert j.attrsLen == 2
```

```nim
var f = newElement("myTag")
f.add newElement("firstSon")
f.add newElement("secondSon")
f.add newElement("thirdSon")
assert $(f.child("secondSon")) == "<secondSon />"
```

```nim
var g = newElement("myTag")
g.add newText("some text")
g.add newComment("this is comment")

var h = newElement("secondTag")
h.add newEntity("some entity")

let att = {"key1": "first value", "key2": "second value"}.toXmlAttributes
var k = newXmlTree("treeTag", [g, h], att)

doAssert $k == """<treeTag key1="first value" key2="second value">
  <myTag>some text<!-- this is comment --></myTag>
  <secondTag>&some entity;</secondTag>
</treeTag>"""

clear(k)
doAssert $k == """<treeTag key1="first value" key2="second value" />"""
```

```nim
var f = newElement("myTag")
f.add newElement("first")
f.insert(newElement("second"), 0)
f.delete(0)
assert $f == """<myTag>
  <first />
</myTag>"""
```

```nim
var f = newElement("myTag")
f.add newElement("first")
f.insert([newElement("second"), newElement("third")], 0)
f.delete(0..1)
assert $f == """<myTag>
  <first />
</myTag>"""
```

```nim
var
  b = newElement("good")
  c = newElement("bad")
  d = newElement("BAD")
  e = newElement("GOOD")
b.add newText("b text")
c.add newText("c text")
d.add newText("d text")
e.add newText("e text")
let a = newXmlTree("father", [b, c, d, e])
assert $(a.findAll("good")) == "@[<good>b text</good>]"
assert $(a.findAll("BAD")) == "@[<BAD>d text</BAD>]"
assert $(a.findAll("good", caseInsensitive = true)) == "@[<good>b text</good>, <GOOD>e text</GOOD>]"
assert $(a.findAll("BAD", caseInsensitive = true)) == "@[<bad>c text</bad>, <BAD>d text</BAD>]"
```

```nim
var
  b = newElement("good")
  c = newElement("bad")
  d = newElement("BAD")
  e = newElement("GOOD")
b.add newText("b text")
c.add newText("c text")
d.add newText("d text")
e.add newText("e text")
let a = newXmlTree("father", [b, c, d, e])
var s = newSeq[XmlNode]()
a.findAll("good", s)
assert $s == "@[<good>b text</good>]"
s.setLen(0)
a.findAll("good", s, caseInsensitive = true)
assert $s == "@[<good>b text</good>, <GOOD>e text</GOOD>]"
s.setLen(0)
a.findAll("BAD", s)
assert $s == "@[<BAD>d text</BAD>]"
s.setLen(0)
a.findAll("BAD", s, caseInsensitive = true)
assert $s == "@[<bad>c text</bad>, <BAD>d text</BAD>]"
```

```nim
var f = newElement("myTag")
f.add newText("my text")
f.add newComment("my comment")
f.add newEntity("my entity")
assert $f == "<myTag>my text<!-- my comment -->&my entity;</myTag>"
assert innerText(f) == "my textmy entity"
```

```nim
var f = newElement("myTag")
f.add newElement("first")
f.insert(newElement("second"), 0)
assert $f == """<myTag>
  <second />
  <first />
</myTag>"""
```

```nim
var f = newElement("myTag")
f.add newElement("first")
f.insert([newElement("second"), newElement("third")], 0)
assert $f == """<myTag>
  <second />
  <third />
  <first />
</myTag>"""
```

```nim
var a = newElement("firstTag")
assert a.kind == xnElement
var b = newText("my text")
assert b.kind == xnText
```

```nim
var f = newElement("myTag")
f.add newElement("first")
f.insert(newElement("second"), 0)
assert len(f) == 2
```

```nim
var d = newCData("my cdata")
assert d.kind == xnCData
assert $d == "<![CDATA[my cdata]]>"
```

```nim
var c = newComment("my comment")
assert c.kind == xnComment
assert $c == "<!-- my comment -->"
```

```nim
var a = newElement("firstTag")
a.add newElement("childTag")
assert a.kind == xnElement
assert $a == """<firstTag>
  <childTag />
</firstTag>"""
```

```nim
var e = newEntity("my entity")
assert e.kind == xnEntity
assert $e == "&my entity;"
```

```nim
var b = newText("my text")
assert b.kind == xnText
assert $b == "my text"
```

```nim
var g = newElement("myTag")
g.add newText("some text")
g.add newComment("this is comment")
var h = newElement("secondTag")
h.add newEntity("some entity")
let att = {"key1": "first value", "key2": "second value"}.toXmlAttributes
let k = newXmlTree("treeTag", [g, h], att)

doAssert $k == """<treeTag key1="first value" key2="second value">
  <myTag>some text<!-- this is comment --></myTag>
  <secondTag>&some entity;</secondTag>
</treeTag>"""
```

```nim
var f = newElement("myTag")
f.add newElement("first")
f.insert(newElement("second"), 0)
f.replace(0, @[newElement("third"), newElement("fourth")])
assert $f == """<myTag>
  <third />
  <fourth />
  <first />
</myTag>"""
```

```nim
var f = newElement("myTag")
f.add newElement("first")
f.insert([newElement("second"), newElement("fifth")], 0)
f.replace(0..1, @[newElement("third"), newElement("fourth")])
assert $f == """<myTag>
  <third />
  <fourth />
  <first />
</myTag>"""
```

```nim
var a = newElement("firstTag")
a.add newElement("childTag")
assert $a == """<firstTag>
  <childTag />
</firstTag>"""
assert a.tag == "firstTag"
```

```nim
var a = newElement("firstTag")
a.add newElement("childTag")
assert $a == """<firstTag>
  <childTag />
</firstTag>"""
a.tag = "newTag"
assert $a == """<newTag>
  <childTag />
</newTag>"""
```

```nim
var c = newComment("my comment")
assert $c == "<!-- my comment -->"
assert c.text == "my comment"
```

```nim
var e = newEntity("my entity")
assert $e == "&my entity;"
e.text = "a new entity text"
assert $e == "&a new entity text;"
```

```nim
let att = {"key1": "first value", "key2": "second value"}.toXmlAttributes
var j = newElement("myTag")
j.attrs = att

doAssert $j == """<myTag key1="first value" key2="second value" />"""
```

```nim
var g = newElement("myTag")
g.add newText("some text")
g.add newComment("this is comment")

var h = newElement("secondTag")
h.add newEntity("some entity")
g.add h

assert $g == "<myTag>some text<!-- this is comment --><secondTag>&some entity;</secondTag></myTag>"

# for x in g: # the same as `for x in items(g):`
#   echo x

# some text
# <!-- this is comment -->
# <secondTag>&some entity;<![CDATA[some cdata]]></secondTag>
```

```nim
<>a(href="https://nim-lang.org", newText("Nim rules."))
```

## Const

### xmlHeader

[ref: #symbol-xmlheader]

```nim
xmlHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
```

Header to use for complete XML output.

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `n: XmlNode`

**Output:** `XmlNode`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over all direct children of n.

### mitems

[ref: #symbol-mitems]

**Input:**
- `n: var XmlNode`

**Output:** `var XmlNode`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over all direct children of n so that they can be modified.

## Macro

### `&lt;&gt;`

[ref: #symbol-lt-gt]

Constructor macro for XML. Example usage:

**Input:**
- `x: untyped`

**Output:** `untyped`
Constructor macro for XML. Example usage:

```
<>a(href="https://nim-lang.org", newText("Nim rules."))
```

Produces an XML tree for:

```
<a href="https://nim-lang.org">Nim rules.</a>
```

## Proc

### `$`

[ref: #symbol-]

Converts n into its string representation.

**Input:**
- `n: XmlNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts n into its string representation.

No <$xml ...$> declaration is produced, so that the produced XML fragments are composable.

### `[]`

[ref: #symbol-]

**Input:**
- `n: XmlNode`
- `i: int`

**Output:** `XmlNode`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the i'th child of n.

### `[]`

[ref: #symbol-]

**Input:**
- `n: var XmlNode`
- `i: int`

**Output:** `var XmlNode`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the i'th child of n so that it can be modified.

### add

[ref: #symbol-add]

Adds the child son to father. father must be of xnElement type

**Input:**
- `father: XmlNode`
- `son: XmlNode`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds the child son to father. father must be of xnElement type

See also:

* [add proc](#add,XmlNode,openArray[XmlNode])
* [insert proc](#insert,XmlNode,XmlNode,int)
* [insert proc](#insert,XmlNode,openArray[XmlNode],int)
* [delete proc](#delete,XmlNode,Natural)
* [delete proc](#delete.XmlNode,Slice[int])
* [replace proc](#replace.XmlNode,int,openArray[XmlNode])
* [replace proc](#replace.XmlNode,Slice[int],openArray[XmlNode])

### add

[ref: #symbol-add]

Adds the children sons to father. father must be of xnElement type

**Input:**
- `father: XmlNode`
- `sons: openArray[XmlNode]`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds the children sons to father. father must be of xnElement type

See also:

* [add proc](#add,XmlNode,XmlNode)
* [insert proc](#insert,XmlNode,XmlNode,int)
* [insert proc](#insert,XmlNode,openArray[XmlNode],int)
* [delete proc](#delete,XmlNode,Natural)
* [delete proc](#delete.XmlNode,Slice[int])
* [replace proc](#replace.XmlNode,int,openArray[XmlNode])
* [replace proc](#replace.XmlNode,Slice[int],openArray[XmlNode])

### add

[ref: #symbol-add]

**Input:**
- `result: var string`
- `n: XmlNode`
- `indent:  = 0`
- `indWidth:  = 2`
- `addNewLines:  = true`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds the textual representation of n to string result.

### addEscaped

[ref: #symbol-addescaped]

**Input:**
- `result: var string`
- `s: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The same as [result.add(escape(s))](#escape,string), but more efficient.

### attr

[ref: #symbol-attr]

Finds the first attribute of n with a name of name. Returns "" on failure.

**Input:**
- `n: XmlNode`
- `name: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Finds the first attribute of n with a name of name. Returns "" on failure.

See also:

* [attrs proc](#attrs,XmlNode) for XmlAttributes getter
* [attrs= proc](#attrs=,XmlNode,XmlAttributes) for XmlAttributes setter
* [attrsLen proc](#attrsLen,XmlNode) for number of attributes

### attrs

[ref: #symbol-attrs]

Gets the attributes belonging to n.

**Input:**
- `n: XmlNode`

**Output:** `XmlAttributes`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the attributes belonging to n.

Returns nil if attributes have not been initialised for this node.

See also:

* [attrs= proc](#attrs=,XmlNode,XmlAttributes) for XmlAttributes setter
* [attrsLen proc](#attrsLen,XmlNode) for number of attributes
* [attr proc](#attr,XmlNode,string) for finding an attribute

### attrs=

[ref: #symbol-attrs]

Sets the attributes belonging to n.

**Input:**
- `n: XmlNode`
- `attr: XmlAttributes`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the attributes belonging to n.

See also:

* [attrs proc](#attrs,XmlNode) for XmlAttributes getter
* [attrsLen proc](#attrsLen,XmlNode) for number of attributes
* [attr proc](#attr,XmlNode,string) for finding an attribute

### attrsLen

[ref: #symbol-attrslen]

Returns the number of n's attributes.

**Input:**
- `n: XmlNode`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of n's attributes.

See also:

* [attrs proc](#attrs,XmlNode) for XmlAttributes getter
* [attrs= proc](#attrs=,XmlNode,XmlAttributes) for XmlAttributes setter
* [attr proc](#attr,XmlNode,string) for finding an attribute

### child

[ref: #symbol-child]

**Input:**
- `n: XmlNode`
- `name: string`

**Output:** `XmlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Finds the first child element of n with a name of name. Returns nil on failure.

### clear

[ref: #symbol-clear]

**Input:**
- `n: var XmlNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Recursively clears all children of an XmlNode.

### clientData

[ref: #symbol-clientdata]

Gets the client data of n.

**Input:**
- `n: XmlNode`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the client data of n.

The client data field is used by the HTML parser and generator.

### clientData=

[ref: #symbol-clientdata]

Sets the client data of n.

**Input:**
- `n: XmlNode`
- `data: int`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the client data of n.

The client data field is used by the HTML parser and generator.

### delete

[ref: #symbol-delete]

Deletes the i'th child of n.

**Input:**
- `n: XmlNode`
- `i: Natural`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Deletes the i'th child of n.

See also:

* [delete proc](#delete.XmlNode,Slice[int])
* [add proc](#add,XmlNode,XmlNode)
* [add proc](#add,XmlNode,openArray[XmlNode])
* [insert proc](#insert,XmlNode,XmlNode,int)
* [insert proc](#insert,XmlNode,openArray[XmlNode],int)
* [replace proc](#replace.XmlNode,int,openArray[XmlNode])
* [replace proc](#replace.XmlNode,Slice[int],openArray[XmlNode])

### delete

[ref: #symbol-delete]

Deletes the items n[slice] of n.

**Input:**
- `n: XmlNode`
- `slice: Slice[int]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Deletes the items n[slice] of n.

See also:

* [delete proc](#delete.XmlNode,int)
* [add proc](#add,XmlNode,XmlNode)
* [add proc](#add,XmlNode,openArray[XmlNode])
* [insert proc](#insert,XmlNode,XmlNode,int)
* [insert proc](#insert,XmlNode,openArray[XmlNode],int)
* [replace proc](#replace.XmlNode,int,openArray[XmlNode])
* [replace proc](#replace.XmlNode,Slice[int],openArray[XmlNode])

### escape

[ref: #symbol-escape]

Escapes s for inclusion into an XML document.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Escapes s for inclusion into an XML document.

Escapes these characters:

| char | is converted to |
| --- | --- |
| < | &lt; |
| > | &gt; |
| & | &amp; |
| " | &quot; |
| ' | &apos; |

You can also use [addEscaped proc](#addEscaped,string,string).

### findAll

[ref: #symbol-findall]

Iterates over all the children of n returning those matching tag.

**Input:**
- `n: XmlNode`
- `tag: string`
- `result: var seq[XmlNode]`
- `caseInsensitive:  = false`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over all the children of n returning those matching tag.

Found nodes satisfying the condition will be appended to the result sequence.

### findAll

[ref: #symbol-findall]

**Input:**
- `n: XmlNode`
- `tag: string`
- `caseInsensitive:  = false`

**Output:** `seq[XmlNode]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

A shortcut version to assign in let blocks.

### innerText

[ref: #symbol-innertext]

Gets the inner text of n:

**Input:**
- `n: XmlNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the inner text of n:

* If n is xnText or xnEntity, returns its content.
* If n is xnElement, runs recursively on each child node and concatenates the results.
* Otherwise returns an empty string.

See also:

* [text proc](#text,XmlNode)

### insert

[ref: #symbol-insert]

Inserts the child son to a given position in father.

**Input:**
- `father: XmlNode`
- `son: XmlNode`
- `index: int`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Inserts the child son to a given position in father.

father must be of xnElement kind.

See also:

* [insert proc](#insert,XmlNode,openArray[XmlNode],int)
* [add proc](#add,XmlNode,XmlNode)
* [add proc](#add,XmlNode,openArray[XmlNode])
* [delete proc](#delete,XmlNode,Natural)
* [delete proc](#delete.XmlNode,Slice[int])
* [replace proc](#replace.XmlNode,int,openArray[XmlNode])
* [replace proc](#replace.XmlNode,Slice[int],openArray[XmlNode])

### insert

[ref: #symbol-insert]

Inserts the children openArray[`sons`](#`sons`) to a given position in father.

**Input:**
- `father: XmlNode`
- `sons: openArray[XmlNode]`
- `index: int`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Inserts the children openArray[`sons`](#`sons`) to a given position in father.

father must be of xnElement kind.

See also:

* [insert proc](#insert,XmlNode,XmlNode,int)
* [add proc](#add,XmlNode,XmlNode)
* [add proc](#add,XmlNode,openArray[XmlNode])
* [delete proc](#delete,XmlNode,Natural)
* [delete proc](#delete.XmlNode,Slice[int])
* [replace proc](#replace.XmlNode,int,openArray[XmlNode])
* [replace proc](#replace.XmlNode,Slice[int],openArray[XmlNode])

### kind

[ref: #symbol-kind]

**Input:**
- `n: XmlNode`

**Output:** `XmlNodeKind`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns n's kind.

### len

[ref: #symbol-len]

**Input:**
- `n: XmlNode`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of n's children.

### newCData

[ref: #symbol-newcdata]

**Input:**
- `cdata: sink string`

**Output:** `XmlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new XmlNode of kind xnCData with the text cdata.

### newComment

[ref: #symbol-newcomment]

**Input:**
- `comment: sink string`

**Output:** `XmlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new XmlNode of kind xnComment with the text comment.


[Next](xmltree_2.md)
