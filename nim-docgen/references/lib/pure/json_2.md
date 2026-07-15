---
source_hash: dcc5f23e97223090
source_path: lib/pure/json.nim
---

### getInt

[ref: #symbol-getint]

Retrieves the int value of a JInt JsonNode.

**Input:**
- `n: JsonNode`
- `default: int = 0`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the int value of a JInt JsonNode.

Returns default if n is not a JInt, or if n is nil.

### getOrDefault

[ref: #symbol-getordefault]

**Input:**
- `node: JsonNode`
- `key: string`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Gets a field from a node. If node is nil or not an object or value at key does not exist, returns nil

### getStr

[ref: #symbol-getstr]

Retrieves the string value of a JString JsonNode.

**Input:**
- `n: JsonNode`
- `default: string = ""`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the string value of a JString JsonNode.

Returns default if n is not a JString, or if n is nil.

### hash

[ref: #symbol-hash]

**Input:**
- `n: OrderedTable[string, JsonNode]`

**Output:** `Hash`
**Pragmas:** `noSideEffect`, `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

### hash

[ref: #symbol-hash]

**Input:**
- `n: JsonNode`

**Output:** `Hash`
**Pragmas:** `noSideEffect`, `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Compute the hash for a JSON node

### hasKey

[ref: #symbol-haskey]

**Input:**
- `node: JsonNode`
- `key: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if key exists in node.

### len

[ref: #symbol-len]

**Input:**
- `n: JsonNode`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

If n is a JArray, it returns the number of elements. If n is a JObject, it returns the number of pairs. Else it returns 0.

### newJArray

[ref: #symbol-newjarray]

**Input:**
- *(none)*

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new JArray JsonNode

### newJBool

[ref: #symbol-newjbool]

**Input:**
- `b: bool`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new JBool JsonNode.

### newJFloat

[ref: #symbol-newjfloat]

**Input:**
- `n: float`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new JFloat JsonNode.

### newJInt

[ref: #symbol-newjint]

**Input:**
- `n: BiggestInt`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new JInt JsonNode.

### newJNull

[ref: #symbol-newjnull]

**Input:**
- *(none)*

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new JNull JsonNode.

### newJObject

[ref: #symbol-newjobject]

**Input:**
- *(none)*

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new JObject JsonNode

### newJString

[ref: #symbol-newjstring]

**Input:**
- `s: string`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new JString JsonNode.

### parseFile

[ref: #symbol-parsefile]

**Input:**
- `filename: string`

**Output:** `JsonNode`
**Pragmas:** `raises: [IOError, OSError, JsonParsingError, ValueError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, JsonParsingError, ValueError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Parses file into a JsonNode. If file contains extra data, it will raise JsonParsingError.

### parseJson

[ref: #symbol-parsejson]

**Input:**
- `s: Stream`
- `filename: string = ""`
- `rawIntegers:  = false`
- `rawFloats:  = false`

**Output:** `JsonNode`
**Pragmas:** `raises: [IOError, OSError, IOError, OSError, JsonParsingError, ValueError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, IOError, OSError, JsonParsingError, ValueError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Parses from a stream s into a JsonNode. filename is only needed for nice error messages. If s contains extra data, it will raise JsonParsingError. This closes the stream s after it's done. If rawIntegers is true, integer literals will not be converted to a JInt field but kept as raw numbers via JString. If rawFloats is true, floating point literals will not be converted to a JFloat field but kept as raw numbers via JString.

### parseJson

[ref: #symbol-parsejson]

**Input:**
- `buffer: string`
- `rawIntegers:  = false`
- `rawFloats:  = false`

**Output:** `JsonNode`
**Pragmas:** `raises: [IOError, OSError, JsonParsingError, ValueError]`, `tags: [ReadIOEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, JsonParsingError, ValueError`, `tags: ReadIOEffect, WriteIOEffect`, `forbids: `

Parses JSON from buffer. If buffer contains extra data, it will raise JsonParsingError. If rawIntegers is true, integer literals will not be converted to a JInt field but kept as raw numbers via JString. If rawFloats is true, floating point literals will not be converted to a JFloat field but kept as raw numbers via JString.

### pretty

[ref: #symbol-pretty]

Returns a JSON Representation of node, with indentation and on multiple lines.

**Input:**
- `node: JsonNode`
- `indent:  = 2`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a JSON Representation of node, with indentation and on multiple lines.

Similar to prettyprint in Python.

### to

[ref: #symbol-to]

Unmarshals the specified node into the object type specified.

**Input:**
- `node: JsonNode`
- `t: typedesc[T]`

**Output:** `T`
**Generic parameters:** `T`, `t:type`

Unmarshals the specified node into the object type specified.

Known limitations:

* Heterogeneous arrays are not supported.
* Sets in object variants are not supported.
* Not nil annotations are not supported.

### toUgly

[ref: #symbol-tougly]

Converts node to its JSON Representation, without regard for human readability. Meant to improve $ string conversion performance.

**Input:**
- `result: var string`
- `node: JsonNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts node to its JSON Representation, without regard for human readability. Meant to improve $ string conversion performance.

JSON representation is stored in the passed result

This provides higher efficiency than the pretty procedure as it does **not** attempt to format the resulting JSON to make it human readable.

## Template

### `%`

[ref: #symbol-]

**Input:**
- `j: JsonNode`

**Output:** `JsonNode`
## Type

### JsonNode

[ref: #symbol-jsonnode]

```nim
JsonNode = ref JsonNodeObj
```

JSON node

### JsonNodeKind

[ref: #symbol-jsonnodekind]

```nim
JsonNodeKind = enum
  JNull, JBool, JInt, JFloat, JString, JObject, JArray
```

possible JSON node types

### JsonNodeObj

[ref: #symbol-jsonnodeobj]

```nim
JsonNodeObj {.acyclic.} = object
  case kind*: JsonNodeKind
  of JString:
    str*: string
  of JInt:
    num*: BiggestInt
  of JFloat:
    fnum*: float
  of JBool:
    bval*: bool
  of JNull:
    nil
  of JObject:
    fields*: OrderedTable[string, JsonNode]
  of JArray:
    elems*: seq[JsonNode]
```

[Prev](json_1.md)
