---
source_hash: 8f682c0a1e52b60f
source_path: lib/pure/marshal.nim
---

# marshal

[ref: #module-marshal]

This module contains procs for serialization and deserialization of arbitrary Nim data structures. The serialization format uses JSON.

**Restriction:** For objects, their type is **not** serialized. This means essentially that it does not work if the object has some other runtime type than its compiletime type.

# [Basic usage](#basic-usage)

**Note:** The to and $$ operations are available at compile-time!

# [See also](#see-also)

* [streams module](streams.html)
* [json module](json.html)

## Examples

```nim
import std/marshal
type
  A = object of RootObj
  B = object of A
    f: int

let a: ref A = new(B)
assert $$a[] == "{}" # not "{f: 0}"

# unmarshal
let c = to[B]("""{"f": 2}""")
assert typeof(c) is B
assert c.f == 2

# marshal
assert $$c == """{"f": 2}"""
```

```nim
type
  Foo = object
    id: int
    bar: string
let x = Foo(id: 1, bar: "baz")
## serialize:
let y = $$x
assert y == """{"id": 1, "bar": "baz"}"""
```

```nim
import std/streams

var s = newStringStream("[1, 3, 5]")
var a: array[3, int]
load(s, a)
assert a == [1, 3, 5]
```

```nim
import std/streams

var s = newStringStream("")
var a = [1, 3, 5]
store(s, a)
s.setPosition(0)
assert s.readAll() == "[1, 3, 5]"
```

```nim
type
  Foo = object
    id: int
    bar: string
let y = """{"id": 1, "bar": "baz"}"""
assert typeof(y) is string
## deserialize to type 'Foo':
let z = y.to[:Foo]
assert typeof(z) is Foo
assert z.id == 1
assert z.bar == "baz"
```

## Proc

### `$$`

[ref: #symbol-]

Returns a string representation of x (serialization, marshalling).

**Input:**
- `x: sink T`

**Output:** `string`
**Generic parameters:** `T`

Returns a string representation of x (serialization, marshalling).

**Note:** to serialize x to JSON use %x from the json module or jsonutils.toJson(x).

### load

[ref: #symbol-load]

**Input:**
- `s: Stream`
- `data: var T`

**Output:** *(none)*
**Generic parameters:** `T`

Loads data from the stream s. Raises IOError in case of an error.

### store

[ref: #symbol-store]

**Input:**
- `s: Stream`
- `data: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

Stores data into the stream s. Raises IOError in case of an error.

### to

[ref: #symbol-to]

**Input:**
- `data: string`

**Output:** `T`
**Generic parameters:** `T`

Reads data and transforms it to a type T (deserialization, unmarshalling).
