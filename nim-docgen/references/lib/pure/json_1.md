---
source_hash: dcc5f23e97223090
source_path: lib/pure/json.nim
---

# json

[ref: #module-json]

This module implements a simple high performance JSON parser. JSON (JavaScript Object Notation) is a lightweight data-interchange format that is easy for humans to read and write (unlike XML). It is easy for machines to parse and generate. JSON is based on a subset of the JavaScript Programming Language, Standard ECMA-262 3rd Edition - December 1999.

# [See also](#see-also)

* [std/parsejson](parsejson.html)
* [std/jsonutils](jsonutils.html)
* [std/marshal](marshal.html)
* [std/jscore](jscore.html)

# [Overview](#overview)

## [Parsing JSON](#overview-parsing-json)

JSON often arrives into your program (via an API or a file) as a string. The first step is to change it from its serialized form into a nested object structure called a JsonNode.

The parseJson procedure takes a string containing JSON and returns a JsonNode object. This is an object variant and it is either a JObject, JArray, JString, JInt, JFloat, JBool or JNull. You check the kind of this object variant by using the kind accessor.

For a JsonNode who's kind is JObject, you can access its fields using the [] operator. The following example shows how to do this:

```
import std/json

let jsonNode = parseJson("""{"key": 3.14}""")

doAssert jsonNode.kind == JObject
doAssert jsonNode["key"].kind == JFloat
```

## [Reading values](#overview-reading-values)

Once you have a JsonNode, retrieving the values can then be achieved by using one of the helper procedures, which include:

* getInt
* getFloat
* getStr
* getBool

To retrieve the value of "key" you can do the following:

```
import std/json

let jsonNode = parseJson("""{"key": 3.14}""")

doAssert jsonNode["key"].getFloat() == 3.14
```

**Important:** The [] operator will raise an exception when the specified field does not exist.

## [Handling optional keys](#overview-handling-optional-keys)

By using the {} operator instead of [], it will return nil when the field is not found. The get-family of procedures will return a type's default value when called on nil.

```
import std/json

let jsonNode = parseJson("{}")

doAssert jsonNode{"nope"}.getInt() == 0
doAssert jsonNode{"nope"}.getFloat() == 0
doAssert jsonNode{"nope"}.getStr() == ""
doAssert jsonNode{"nope"}.getBool() == false
```

## [Using default values](#overview-using-default-values)

The get-family helpers also accept an additional parameter which allow you to fallback to a default value should the key's values be null:

```
import std/json

let jsonNode = parseJson("""{"key": 3.14, "key2": null}""")

doAssert jsonNode["key"].getFloat(6.28) == 3.14
doAssert jsonNode["key2"].getFloat(3.14) == 3.14
doAssert jsonNode{"nope"}.getFloat(3.14) == 3.14 # note the {}
```

## [Unmarshalling](#overview-unmarshalling)

In addition to reading dynamic data, Nim can also unmarshal JSON directly into a type with the to macro.

Note: Use [Option](options.html#Option) for keys sometimes missing in json responses, and backticks around keys with a reserved keyword as name.

```
import std/json
import std/options

type
  User = object
    name: string
    age: int
    `type`: Option[string]

let userJson = parseJson("""{ "name": "Nim", "age": 12 }""")
let user = to(userJson, User)
if user.`type`.isSome():
  assert user.`type`.get() != "robot"
```

# [Creating JSON](#creating-json)

This module can also be used to comfortably create JSON using the %\* operator:

```
import std/json

var hisName = "John"
let herAge = 31
var j = %*
  [
    { "name": hisName, "age": 30 },
    { "name": "Susan", "age": herAge }
  ]

var j2 = %* {"name": "Isaac", "books": ["Robot Dreams"]}
j2["details"] = %* {"age":35, "pi":3.1415}
echo j2
```

See also: std/jsonutils for hookable json serialization/deserialization of arbitrary types.

## Examples

```nim
import std/json

let jsonNode = parseJson("""{"key": 3.14}""")

doAssert jsonNode.kind == JObject
doAssert jsonNode["key"].kind == JFloat
```

```nim
import std/json

let jsonNode = parseJson("""{"key": 3.14}""")

doAssert jsonNode["key"].getFloat() == 3.14
```

```nim
import std/json

let jsonNode = parseJson("{}")

doAssert jsonNode{"nope"}.getInt() == 0
doAssert jsonNode{"nope"}.getFloat() == 0
doAssert jsonNode{"nope"}.getStr() == ""
doAssert jsonNode{"nope"}.getBool() == false
```

```nim
import std/json

let jsonNode = parseJson("""{"key": 3.14, "key2": null}""")

doAssert jsonNode["key"].getFloat(6.28) == 3.14
doAssert jsonNode["key2"].getFloat(3.14) == 3.14
doAssert jsonNode{"nope"}.getFloat(3.14) == 3.14 # note the {}
```

```nim
import std/json
import std/options

type
  User = object
    name: string
    age: int
    `type`: Option[string]

let userJson = parseJson("""{ "name": "Nim", "age": 12 }""")
let user = to(userJson, User)
if user.`type`.isSome():
  assert user.`type`.get() != "robot"
```

```nim
import std/json

var hisName = "John"
let herAge = 31
var j = %*
  [
    { "name": hisName, "age": 30 },
    { "name": "Susan", "age": herAge }
  ]

var j2 = %* {"name": "Isaac", "books": ["Robot Dreams"]}
j2["details"] = %* {"age":35, "pi":3.1415}
echo j2
```

```nim
import std/json
## Note: for JObject, key ordering is preserved, unlike in some languages,
## this is convenient for some use cases. Example:
type Foo = object
  a1, a2, a0, a3, a4: int
doAssert $(%* Foo()) == """{"a1":0,"a2":0,"a0":0,"a3":0,"a4":0}"""
```

```nim
assert $(%[NaN, Inf, -Inf, 0.0, -0.0, 1.0, 1e-2]) == """["nan","inf","-inf",0.0,-0.0,1.0,0.01]"""
assert (%NaN).kind == JString
assert (%0.0).kind == JFloat
```

```nim
let
  j = parseJson("[1,2,3,4,5]")

doAssert j[^1].getInt == 5
doAssert j[^2].getInt == 4
```

```nim
import std/json
let arr = %[0,1,2,3,4,5]
doAssert arr[2..4] == %[2,3,4]
doAssert arr[2..^2] == %[2,3,4]
doAssert arr[^4..^2] == %[2,3,4]
```

```nim
let j = %* {"name": "Isaac", "books": ["Robot Dreams"],
            "details": {"age": 35, "pi": 3.1415}}
doAssert pretty(j) == """
{
  "name": "Isaac",
  "books": [
    "Robot Dreams"
  ],
  "details": {
    "age": 35,
    "pi": 3.1415
  }
}"""
```

```nim
let jsonNode = parseJson("""
      {
        "person": {
          "name": "Nimmer",
          "age": 21
        },
        "list": [1, 2, 3, 4]
      }
    """)

type
  Person = object
    name: string
    age: int

  Data = object
    person: Person
    list: seq[int]

var data = to(jsonNode, Data)
doAssert data.person.name == "Nimmer"
doAssert data.person.age == 21
doAssert data.list == @[1, 2, 3, 4]
```

```nim
var myjson = %* {"parent": {"child": {"grandchild": 1}}}
doAssert myjson{"parent", "child", "grandchild"} == newJInt(1)
```

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `node: JsonNode`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterator for the items of node. node has to be a JArray.

### keys

[ref: #symbol-keys]

**Input:**
- `node: JsonNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterator for the keys in node. node has to be a JObject.

### mitems

[ref: #symbol-mitems]

**Input:**
- `node: var JsonNode`

**Output:** `var JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterator for the items of node. node has to be a JArray. Items can be modified.

### mpairs

[ref: #symbol-mpairs]

**Input:**
- `node: var JsonNode`

**Output:** `tuple[key: string, val: var JsonNode]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterator for the child elements of node. node has to be a JObject. Values can be modified

### pairs

[ref: #symbol-pairs]

**Input:**
- `node: JsonNode`

**Output:** `tuple[key: string, val: JsonNode]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterator for the child elements of node. node has to be a JObject.

### parseJsonFragments

[ref: #symbol-parsejsonfragments]

**Input:**
- `s: Stream`
- `filename: string = ""`
- `rawIntegers:  = false`
- `rawFloats:  = false`

**Output:** `JsonNode`
**Pragmas:** `raises: [IOError, OSError, IOError, OSError, JsonParsingError, ValueError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, IOError, OSError, JsonParsingError, ValueError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Parses from a stream s into JsonNodes. filename is only needed for nice error messages. The JSON fragments are separated by whitespace. This can be substantially faster than the comparable loop for x in splitWhitespace(s): yield parseJson(x). This closes the stream s after it's done. If rawIntegers is true, integer literals will not be converted to a JInt field but kept as raw numbers via JString. If rawFloats is true, floating point literals will not be converted to a JFloat field but kept as raw numbers via JString.

## Macro

### `%*`

[ref: #symbol-]

**Input:**
- `x: untyped`

**Output:** `untyped`
Convert an expression to a JsonNode directly, without having to specify % for every element.

### isRefSkipDistinct

[ref: #symbol-isrefskipdistinct]

**Input:**
- `arg: typed`

**Output:** `untyped`
internal only, do not use

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `node: JsonNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts node to its JSON Representation on one line.

### `%`

[ref: #symbol-]

**Input:**
- `s: string`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for JSON data. Creates a new JString JsonNode.

### `%`

[ref: #symbol-]

**Input:**
- `n: uint`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for JSON data. Creates a new JInt JsonNode.

### `%`

[ref: #symbol-]

**Input:**
- `n: int`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for JSON data. Creates a new JInt JsonNode.

### `%`

[ref: #symbol-]

**Input:**
- `n: BiggestUInt`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for JSON data. Creates a new JInt JsonNode.

### `%`

[ref: #symbol-]

**Input:**
- `n: BiggestInt`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for JSON data. Creates a new JInt JsonNode.

### `%`

[ref: #symbol-]

**Input:**
- `n: float`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for JSON data. Creates a new JFloat JsonNode.

### `%`

[ref: #symbol-]

**Input:**
- `b: bool`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for JSON data. Creates a new JBool JsonNode.

### `%`

[ref: #symbol-]

**Input:**
- `keyVals: openArray[tuple[key: string, val: JsonNode]]`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generic constructor for JSON data. Creates a new JObject JsonNode

### `%`

[ref: #symbol-]

**Input:**
- `elements: openArray[T]`

**Output:** `JsonNode`
**Generic parameters:** `T`

Generic constructor for JSON data. Creates a new JArray JsonNode

### `%`

[ref: #symbol-]

**Input:**
- `table: Table[string, T] | OrderedTable[string, T]`

**Output:** `JsonNode`
**Generic parameters:** `T`, `table:type`

Generic constructor for JSON data. Creates a new JObject JsonNode.

### `%`

[ref: #symbol-]

**Input:**
- `opt: Option[T]`

**Output:** `JsonNode`
**Generic parameters:** `T`

Generic constructor for JSON data. Creates a new JNull JsonNode if opt is empty, otherwise it delegates to the underlying value.

### `%`

[ref: #symbol-]

**Input:**
- `o: T`

**Output:** `JsonNode`
**Generic parameters:** `T`

Construct JsonNode from tuples and objects.

### `%`

[ref: #symbol-]

**Input:**
- `o: ref object`

**Output:** `JsonNode`
**Generic parameters:** `o:type`

Generic constructor for JSON data. Creates a new JObject JsonNode

### `%`

[ref: #symbol-]

**Input:**
- `o: enum`

**Output:** `JsonNode`
**Generic parameters:** `o:type`

Construct a JsonNode that represents the specified enum value as a string. Creates a new JString JsonNode.

### `==`

[ref: #symbol-]

**Input:**
- `a: JsonNode`
- `b: JsonNode`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Check two nodes for equality

### `[]=`

[ref: #symbol-]

**Input:**
- `obj: JsonNode`
- `key: string`
- `val: JsonNode`

**Output:** *(none)*
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets a field from a JObject.

### `[]`

[ref: #symbol-]

**Input:**
- `node: JsonNode`
- `name: string`

**Output:** `JsonNode`
**Pragmas:** `inline`, `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Gets a field from a JObject, which must not be nil. If the value at name does not exist, raises KeyError.

### `[]`

[ref: #symbol-]

**Input:**
- `node: JsonNode`
- `index: int`

**Output:** `JsonNode`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the node at index in an Array. Result is undefined if index is out of bounds, but as long as array bound checks are enabled it will result in an exception.

### `[]`

[ref: #symbol-]

Gets the node at array.len-i in an array through the ^ operator.

**Input:**
- `node: JsonNode`
- `index: BackwardsIndex`

**Output:** `JsonNode`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets the node at array.len-i in an array through the ^ operator.

i.e. j[^i] is a shortcut for j[j.len-i].

### `[]`

[ref: #symbol-]

Slice operation for JArray.

**Input:**
- `a: JsonNode`
- `x: HSlice[U, V]`

**Output:** `JsonNode`
**Generic parameters:** `U`, `V`

Slice operation for JArray.

Returns the inclusive range [a[x.a], a[x.b]]:

### `{}=`

[ref: #symbol-]

**Input:**
- `node: JsonNode`
- `keys: varargs[string]`
- `value: JsonNode`

**Output:** *(none)*
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Traverses the node and tries to set the value at the given location to value. If any of the keys are missing, they are added.

### `{}`

[ref: #symbol-]

Traverses the node and gets the given value. If any of the keys do not exist, returns nil. Also returns nil if one of the intermediate data structures is not an object.

**Input:**
- `node: JsonNode`
- `keys: varargs[string]`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Traverses the node and gets the given value. If any of the keys do not exist, returns nil. Also returns nil if one of the intermediate data structures is not an object.

This proc can be used to create tree structures on the fly (sometimes called autovivification):

### `{}`

[ref: #symbol-]

**Input:**
- `node: JsonNode`
- `index: varargs[int]`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Traverses the node and gets the given value. If any of the indexes do not exist, returns nil. Also returns nil if one of the intermediate data structures is not an array.

### `{}`

[ref: #symbol-]

**Input:**
- `node: JsonNode`
- `key: string`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets a field from a node. If node is nil or not an object or value at key does not exist, returns nil

### add

[ref: #symbol-add]

**Input:**
- `father: JsonNode`
- `child: JsonNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds child to a JArray node father.

### add

[ref: #symbol-add]

**Input:**
- `obj: JsonNode`
- `key: string`
- `val: JsonNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets a field from a JObject.

### contains

[ref: #symbol-contains]

**Input:**
- `node: JsonNode`
- `key: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if key exists in node.

### contains

[ref: #symbol-contains]

**Input:**
- `node: JsonNode`
- `val: JsonNode`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: RootEffect`, `forbids: `

Checks if val exists in array node.

### copy

[ref: #symbol-copy]

**Input:**
- `p: JsonNode`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Performs a deep copy of p.

### delete

[ref: #symbol-delete]

**Input:**
- `obj: JsonNode`
- `key: string`

**Output:** *(none)*
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Deletes obj[key].

### escapeJson

[ref: #symbol-escapejson]

**Input:**
- `s: string`
- `result: var string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a string s to its JSON representation with quotes. Appends to result.

### escapeJson

[ref: #symbol-escapejson]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a string s to its JSON representation with quotes.

### escapeJsonUnquoted

[ref: #symbol-escapejsonunquoted]

**Input:**
- `s: string`
- `result: var string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a string s to its JSON representation without quotes. Appends to result.

### escapeJsonUnquoted

[ref: #symbol-escapejsonunquoted]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a string s to its JSON representation without quotes.

### getBiggestInt

[ref: #symbol-getbiggestint]

Retrieves the BiggestInt value of a JInt JsonNode.

**Input:**
- `n: JsonNode`
- `default: BiggestInt = 0`

**Output:** `BiggestInt`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the BiggestInt value of a JInt JsonNode.

Returns default if n is not a JInt, or if n is nil.

### getBool

[ref: #symbol-getbool]

Retrieves the bool value of a JBool JsonNode.

**Input:**
- `n: JsonNode`
- `default: bool = false`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the bool value of a JBool JsonNode.

Returns default if n is not a JBool, or if n is nil.

### getElems

[ref: #symbol-getelems]

Retrieves the array of a JArray JsonNode.

**Input:**
- `n: JsonNode`
- `default: seq[JsonNode] = @[]`

**Output:** `seq[JsonNode]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the array of a JArray JsonNode.

Returns default if n is not a JArray, or if n is nil.

### getFields

[ref: #symbol-getfields]

Retrieves the key, value pairs of a JObject JsonNode.

**Input:**
- `n: JsonNode`
- `default:  = initOrderedTable[string, JsonNode](2)`

**Output:** `OrderedTable[string, JsonNode]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the key, value pairs of a JObject JsonNode.

Returns default if n is not a JObject, or if n is nil.

### getFloat

[ref: #symbol-getfloat]

Retrieves the float value of a JFloat JsonNode.

**Input:**
- `n: JsonNode`
- `default: float = 0.0`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the float value of a JFloat JsonNode.

Returns default if n is not a JFloat or JInt, or if n is nil.


[Next](json_2.md)
