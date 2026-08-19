---
source_hash: 7a3e266b14995fd1
source_path: lib/std/jsonutils.nim
---

# jsonutils

[ref: #module-jsonutils]

This module implements a hookable (de)serialization for arbitrary types using JSON. Design goal: avoid importing modules where a custom serialization is needed; see strtabs.fromJsonHook,toJsonHook for an example.

## Examples

```nim
import std/jsonutils
import std/[strtabs,json]
type Foo = ref object
  t: bool
  z1: int8
let a = (1.5'f32, (b: "b2", a: "a2"), 'x', @[Foo(t: true, z1: -3), nil], [{"name": "John"}.newStringTable])
let j = a.toJson
assert j.jsonTo(typeof(a)).toJson == j
assert $[NaN, Inf, -Inf, 0.0, -0.0, 1.0, 1e-2].toJson == """["nan","inf","-inf",0.0,-0.0,1.0,0.01]"""
assert 0.0.toJson.kind == JFloat
assert Inf.toJson.kind == JString
```

```nim
import std/[strtabs, json]
var t = newStringTable(modeCaseSensitive)
let jsonStr = """{"mode": 0, "table": {"name": "John", "surname": "Doe"}}"""
fromJsonHook(t, parseJson(jsonStr))
assert t[] == newStringTable("name", "John", "surname", "Doe",
                             modeCaseSensitive)[]
```

```nim
import std/[sets, json]
var foo: tuple[hs: HashSet[string], os: OrderedSet[string]]
fromJson(foo, parseJson("""
      {"hs": ["hash", "set"], "os": ["ordered", "set"]}"""))
assert foo.hs == ["hash", "set"].toHashSet
assert foo.os == ["ordered", "set"].toOrderedSet
```

```nim
import std/[tables, json]
var foo: tuple[t: Table[string, int], ot: OrderedTable[string, int]]
fromJson(foo, parseJson("""
      {"t":{"two":2,"one":1},"ot":{"one":1,"three":3}}"""))
assert foo.t == [("one", 1), ("two", 2)].toTable
assert foo.ot == [("one", 1), ("three", 3)].toOrderedTable
```

```nim
import std/[options, json]
var opt: Option[string]
fromJsonHook(opt, parseJson("\"test\""))
assert get(opt) == "test"
fromJson(opt, parseJson("null"))
assert isNone(opt)
```

```nim
import std/[strtabs, json]
let t = newStringTable("name", "John", "surname", "Doe", modeCaseSensitive)
let jsonStr = """{"mode": "modeCaseSensitive",
                      "table": {"name": "John", "surname": "Doe"}}"""
assert toJson(t) == parseJson(jsonStr)
```

```nim
import std/[sets, json]
let foo = (hs: ["hash"].toHashSet, os: ["ordered", "set"].toOrderedSet)
assert $toJson(foo) == """{"hs":["hash"],"os":["ordered","set"]}"""
```

```nim
import std/[tables, json, sugar]
let foo = (
  t: [("two", 2)].toTable,
  ot: [("one", 1), ("three", 3)].toOrderedTable)
assert $toJson(foo) == """{"t":{"two":2},"ot":{"one":1,"three":3}}"""
# if keys are not string|cstring, you can use this:
let a = {10: "foo", 11: "bar"}.newOrderedTable
let a2 = collect: (for k,v in a: (k,v))
assert $toJson(a2) == """[[10,"foo"],[11,"bar"]]"""
```

```nim
import std/[options, json]
let optSome = some("test")
assert $toJson(optSome) == "\"test\""
let optNone = none[string]()
assert $toJson(optNone) == "null"
```

## Proc

### fromJson

[ref: #symbol-fromjson]

**Input:**
- `a: var T`
- `b: JsonNode`
- `opt:  = Joptions()`

**Output:** *(none)*
**Generic parameters:** `T`

### fromJsonHook

[ref: #symbol-fromjsonhook]

Enables fromJson for Table and OrderedTable types.

**Input:**
- `t: var (Table[K, V] | OrderedTable[K, V])`
- `jsonNode: JsonNode`
- `opt:  = Joptions()`

**Output:** *(none)*
**Generic parameters:** `K`, `V`, `t:type`

Enables fromJson for Table and OrderedTable types.

See also:

* [toJsonHook proc](#toJsonHook)

### fromJsonHook

[ref: #symbol-fromjsonhook]

Enables fromJson for HashSet and OrderedSet types.

**Input:**
- `s: var SomeSet[A]`
- `jsonNode: JsonNode`
- `opt:  = Joptions()`

**Output:** *(none)*
**Generic parameters:** `A`

Enables fromJson for HashSet and OrderedSet types.

See also:

* [toJsonHook proc](#toJsonHook,SomeSet[A])

### fromJsonHook

[ref: #symbol-fromjsonhook]

Enables fromJson for Option types.

**Input:**
- `self: var Option[T]`
- `jsonNode: JsonNode`
- `opt:  = Joptions()`

**Output:** *(none)*
**Generic parameters:** `T`

Enables fromJson for Option types.

See also:

* [toJsonHook proc](#toJsonHook,Option[T])

### fromJsonHook

[ref: #symbol-fromjsonhook]

Enables fromJson for StringTableRef type.

**Input:**
- `a: var StringTableRef`
- `b: JsonNode`

**Output:** *(none)*
**Pragmas:** `raises: [ValueError, KeyError, JsonKindError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: ValueError, KeyError, JsonKindError`, `tags: RootEffect`, `forbids: `

Enables fromJson for StringTableRef type.

See also:

* [toJsonHook proc](#toJsonHook,StringTableRef)

### initToJsonOptions

[ref: #symbol-inittojsonoptions]

**Input:**
- *(none)*

**Output:** `ToJsonOptions`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

initializes ToJsonOptions with sane options.

### jsonTo

[ref: #symbol-jsonto]

**Input:**
- `b: JsonNode`
- `T: typedesc`
- `opt:  = Joptions()`

**Output:** `T:type`
**Generic parameters:** `T:type`

### toJson

[ref: #symbol-tojson]

serializes a to json; uses toJsonHook(a: T) if it's in scope to customize serialization, see strtabs.toJsonHook for an example.

**Input:**
- `a: T`
- `opt:  = initToJsonOptions()`

**Output:** `JsonNode`
**Generic parameters:** `T`

serializes a to json; uses toJsonHook(a: T) if it's in scope to customize serialization, see strtabs.toJsonHook for an example.

**Note:**
With -d:nimPreviewJsonutilsHoleyEnum, toJson now can serialize/deserialize holey enums as regular enums (via ord) instead of as strings. It is expected that this behavior becomes the new default in upcoming versions.

### toJsonHook

[ref: #symbol-tojsonhook]

Enables toJson for Table and OrderedTable types.

**Input:**
- `t: (Table[K, V] | OrderedTable[K, V])`
- `opt:  = initToJsonOptions()`

**Output:** `JsonNode`
**Generic parameters:** `K`, `V`, `t:type`

Enables toJson for Table and OrderedTable types.

See also:

* [fromJsonHook proc](#fromJsonHook,,JsonNode)

### toJsonHook

[ref: #symbol-tojsonhook]

Enables toJson for HashSet and OrderedSet types.

**Input:**
- `s: SomeSet[A]`
- `opt:  = initToJsonOptions()`

**Output:** `JsonNode`
**Generic parameters:** `A`

Enables toJson for HashSet and OrderedSet types.

See also:

* [fromJsonHook proc](#fromJsonHook,SomeSet[A],JsonNode)

### toJsonHook

[ref: #symbol-tojsonhook]

Enables toJson for Option types.

**Input:**
- `self: Option[T]`
- `opt:  = initToJsonOptions()`

**Output:** `JsonNode`
**Generic parameters:** `T`

Enables toJson for Option types.

See also:

* [fromJsonHook proc](#fromJsonHook,Option[T],JsonNode)

### toJsonHook

[ref: #symbol-tojsonhook]

Enables toJson for StringTableRef type.

**Input:**
- `a: StringTableRef`

**Output:** `JsonNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Enables toJson for StringTableRef type.

See also:

* [fromJsonHook proc](#fromJsonHook,StringTableRef,JsonNode)

## Type

### EnumMode

[ref: #symbol-enummode]

```nim
EnumMode = enum
  joptEnumOrd, joptEnumSymbol, joptEnumString
```

### Joptions

[ref: #symbol-joptions]

```nim
Joptions = object
  allowExtraKeys*: bool ## If `true` Nim's object to which the JSON is parsed is not required to
                        ## have a field for every JSON key.
  allowMissingKeys*: bool ## If `true` Nim's object to which JSON is parsed is allowed to have
                          ## fields without corresponding JSON keys.
```

Options controlling the behavior of fromJson.

### JsonNodeMode

[ref: #symbol-jsonnodemode]

```nim
JsonNodeMode = enum
  joptJsonNodeAsRef,        ## returns the ref as is
  joptJsonNodeAsCopy,       ## returns a deep copy of the JsonNode
  joptJsonNodeAsObject       ## treats JsonNode as a regular ref object
```

controls toJson for JsonNode types

### ToJsonOptions

[ref: #symbol-tojsonoptions]

```nim
ToJsonOptions = object
  enumMode*: EnumMode
  jsonNodeMode*: JsonNodeMode
```
