---
source_hash: 1b9c6ffddfbf4b45
source_path: lib/pure/collections/critbits.nim
---

# critbits

[ref: #module-critbits]

This module implements a crit bit tree which is an efficient container for a sorted set of strings, or for a sorted mapping of strings. Based on the [excellent paper by Adam Langley](https://www.imperialviolet.org/binary/critbit.pdf). (A crit bit tree is a form of radix tree or patricia trie.)

## Examples

```nim
import std/critbits
from std/sequtils import toSeq

var critbitAsSet: CritBitTree[void] = ["kitten", "puppy"].toCritBitTree
doAssert critbitAsSet.len == 2
critbitAsSet.incl("")
doAssert "" in critbitAsSet
critbitAsSet.excl("")
doAssert "" notin critbitAsSet
doAssert toSeq(critbitAsSet.items) == @["kitten", "puppy"]
let same = ["puppy", "kitten", "puppy"].toCritBitTree
doAssert toSeq(same.keys) == toSeq(critbitAsSet.keys)

var critbitAsDict: CritBitTree[int] = {"key1": 42}.toCritBitTree
doAssert critbitAsDict.len == 1
critbitAsDict["key2"] = 0
doAssert "key2" in critbitAsDict
doAssert critbitAsDict["key2"] == 0
critbitAsDict.excl("key1")
doAssert "key1" notin critbitAsDict
doAssert toSeq(critbitAsDict.pairs) == @[("key2", 0)]
```

```nim
doAssert $CritBitTree[int].default == "{:}"
doAssert $toCritBitTree({"key1": 1, "key2": 2}) == """{"key1": 1, "key2": 2}"""
doAssert $CritBitTree[void].default == "{}"
doAssert $toCritBitTree(["key1", "key2"]) == """{"key1", "key2"}"""
```

```nim
var c: CritBitTree[void]
doAssert c.commonPrefixLen == 0
incl(c, "key1")
doAssert c.commonPrefixLen == 4
incl(c, "key2")
doAssert c.commonPrefixLen == 3
```

```nim
var c: CritBitTree[void]
incl(c, "key")
doAssert c.contains("key")
```

```nim
block:
  var c: CritBitTree[void]
  doAssert not c.containsOrIncl("key")
  doAssert c.contains("key")
block:
  var c: CritBitTree[void]
  incl(c, "key")
  doAssert c.containsOrIncl("key")
```

```nim
block:
  var c: CritBitTree[int]
  doAssert not c.containsOrIncl("key", 42)
  doAssert c.contains("key")
block:
  var c: CritBitTree[int]
  incl(c, "key", 21)
  doAssert c.containsOrIncl("key", 42)
  doAssert c["key"] == 21
```

```nim
var c: CritBitTree[void]
incl(c, "key")
excl(c, "key")
doAssert not c.contains("key")
```

```nim
var c: CritBitTree[int]
c["key"] = 1
inc(c, "key")
doAssert c["key"] == 2
```

```nim
var c: CritBitTree[void]
incl(c, "key")
doAssert c.hasKey("key")
```

```nim
var c: CritBitTree[int]
incl(c, "key", 42)
doAssert c["key"] == 42
```

```nim
let c = ["key1", "key2"].toCritBitTree
doAssert c.len == 2
```

```nim
block:
  var c: CritBitTree[void]
  doAssert c.missingOrExcl("key")
block:
  var c: CritBitTree[void]
  incl(c, "key")
  doAssert not c.missingOrExcl("key")
  doAssert not c.contains("key")
```

```nim
doAssert ["a", "b", "c"].toCritBitTree is CritBitTree[void]
```

```nim
doAssert {"a": "0", "b": "1", "c": "2"}.toCritBitTree is CritBitTree[string]
doAssert {"a": 0, "b": 1, "c": 2}.toCritBitTree is CritBitTree[int]
```

```nim
from std/sequtils import toSeq

let c = {"key1": 1, "key2": 2}.toCritBitTree
doAssert toSeq(c.keys) == @["key1", "key2"]
```

```nim
from std/sequtils import toSeq

let c = {"key1": 42, "key2": 43}.toCritBitTree
doAssert toSeq(c.keysWithPrefix("key")) == @["key1", "key2"]
```

```nim
from std/sequtils import toSeq

let c = {"key1": 1, "key2": 2}.toCritBitTree
doAssert toSeq(c.pairs) == @[(key: "key1", val: 1), (key: "key2", val: 2)]
```

```nim
from std/sequtils import toSeq

let c = {"key1": 42, "key2": 43}.toCritBitTree
doAssert toSeq(c.pairsWithPrefix("key")) == @[(key: "key1", val: 42), (key: "key2", val: 43)]
```

```nim
from std/sequtils import toSeq

let c = {"key1": 1, "key2": 2}.toCritBitTree
doAssert toSeq(c.values) == @[1, 2]
```

```nim
from std/sequtils import toSeq

let c = {"key1": 42, "key2": 43}.toCritBitTree
doAssert toSeq(c.valuesWithPrefix("key")) == @[42, 43]
```

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `c: CritBitTree[T]`

**Output:** `string`
**Generic parameters:** `T`

Alias for [keys](#keys.i,CritBitTree[T]).

### itemsWithPrefix

[ref: #symbol-itemswithprefix]

**Input:**
- `c: CritBitTree[T]`
- `prefix: string`

**Output:** `string`
**Generic parameters:** `T`

Alias for [keysWithPrefix](#keysWithPrefix.i,CritBitTree[T],string).

### keys

[ref: #symbol-keys]

**Input:**
- `c: CritBitTree[T]`

**Output:** `string`
**Generic parameters:** `T`

Yields all keys in lexicographical order.

### keysWithPrefix

[ref: #symbol-keyswithprefix]

**Input:**
- `c: CritBitTree[T]`
- `prefix: string`

**Output:** `string`
**Generic parameters:** `T`

Yields all keys starting with prefix.

### mpairs

[ref: #symbol-mpairs]

Yields all (key, value)-pairs of c in the lexicographical order of the corresponding keys. The yielded values can be modified.

**Input:**
- `c: var CritBitTree[T]`

**Output:** `tuple[key: string, val: var T]`
**Generic parameters:** `T`

Yields all (key, value)-pairs of c in the lexicographical order of the corresponding keys. The yielded values can be modified.

**See also:**

* [pairs iterator](#pairs.i,CritBitTree[T])

### mpairsWithPrefix

[ref: #symbol-mpairswithprefix]

Yields all (key, value)-pairs of c starting with prefix. The yielded values can be modified.

**Input:**
- `c: var CritBitTree[T]`
- `prefix: string`

**Output:** `tuple[key: string, val: var T]`
**Generic parameters:** `T`

Yields all (key, value)-pairs of c starting with prefix. The yielded values can be modified.

**See also:**

* [pairsWithPrefix iterator](#pairsWithPrefix.i,CritBitTree[T],string)

### mvalues

[ref: #symbol-mvalues]

Yields all values of c in the lexicographical order of the corresponding keys. The values can be modified.

**Input:**
- `c: var CritBitTree[T]`

**Output:** `var T`
**Generic parameters:** `T`

Yields all values of c in the lexicographical order of the corresponding keys. The values can be modified.

**See also:**

* [values iterator](#values.i,CritBitTree[T])

### mvaluesWithPrefix

[ref: #symbol-mvalueswithprefix]

Yields all values of c starting with prefix of the corresponding keys. The values can be modified.

**Input:**
- `c: var CritBitTree[T]`
- `prefix: string`

**Output:** `var T`
**Generic parameters:** `T`

Yields all values of c starting with prefix of the corresponding keys. The values can be modified.

**See also:**

* [valuesWithPrefix iterator](#valuesWithPrefix.i,CritBitTree[T],string)

### pairs

[ref: #symbol-pairs]

Yields all (key, value)-pairs of c in the lexicographical order of the corresponding keys.

**Input:**
- `c: CritBitTree[T]`

**Output:** `tuple[key: string, val: T]`
**Generic parameters:** `T`

Yields all (key, value)-pairs of c in the lexicographical order of the corresponding keys.

**See also:**

* [mpairs iterator](#mpairs.i,CritBitTree[T])

### pairsWithPrefix

[ref: #symbol-pairswithprefix]

Yields all (key, value)-pairs of c starting with prefix.

**Input:**
- `c: CritBitTree[T]`
- `prefix: string`

**Output:** `tuple[key: string, val: T]`
**Generic parameters:** `T`

Yields all (key, value)-pairs of c starting with prefix.

**See also:**

* [mpairsWithPrefix iterator](#mpairsWithPrefix.i,CritBitTree[T],string)

### values

[ref: #symbol-values]

Yields all values of c in the lexicographical order of the corresponding keys.

**Input:**
- `c: CritBitTree[T]`

**Output:** `lent T`
**Generic parameters:** `T`

Yields all values of c in the lexicographical order of the corresponding keys.

**See also:**

* [mvalues iterator](#mvalues.i,CritBitTree[T])

### valuesWithPrefix

[ref: #symbol-valueswithprefix]

Yields all values of c starting with prefix of the corresponding keys.

**Input:**
- `c: CritBitTree[T]`
- `prefix: string`

**Output:** `lent T`
**Generic parameters:** `T`

Yields all values of c starting with prefix of the corresponding keys.

**See also:**

* [mvaluesWithPrefix iterator](#mvaluesWithPrefix.i,CritBitTree[T],string)

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `c: CritBitTree[T]`

**Output:** `string`
**Generic parameters:** `T`

Turns c into a string representation.

### `[]=`

[ref: #symbol-]

Alias for [incl](#incl,CritBitTree[T],string,T).

**Input:**
- `c: var CritBitTree[T]`
- `key: string`
- `val: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

Alias for [incl](#incl,CritBitTree[T],string,T).

**See also:**

* [[] proc](#[],CritBitTree[T],string)
* [[] proc](#[],CritBitTree[T],string_2)

### `[]`

[ref: #symbol-]

Retrieves the value at c[key]. If key is not in t, the KeyError exception is raised. One can check with hasKey whether the key exists.

**Input:**
- `c: CritBitTree[T]`
- `key: string`

**Output:** `lent T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Retrieves the value at c[key]. If key is not in t, the KeyError exception is raised. One can check with hasKey whether the key exists.

**See also:**

* [[] proc](#[],CritBitTree[T],string_2)
* [[]= proc](#[]=,CritBitTree[T],string,T)

### `[]`

[ref: #symbol-]

Retrieves the value at c[key]. The value can be modified. If key is not in t, the KeyError exception is raised.

**Input:**
- `c: var CritBitTree[T]`
- `key: string`

**Output:** `var T`
**Generic parameters:** `T`

**Pragmas:** `inline`

Retrieves the value at c[key]. The value can be modified. If key is not in t, the KeyError exception is raised.

**See also:**

* [[] proc](#[],CritBitTree[T],string)
* [[]= proc](#[]=,CritBitTree[T],string,T)

### commonPrefixLen

[ref: #symbol-commonprefixlen]

**Input:**
- `c: CritBitTree[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the length of the longest common prefix of all keys in c. If c is empty, returns 0.

### contains

[ref: #symbol-contains]

**Input:**
- `c: CritBitTree[T]`
- `key: string`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns true if c contains the given key.

### containsOrIncl

[ref: #symbol-containsorincl]

Returns true if c contains the given key. If the key does not exist, c[key] = val is performed.

**Input:**
- `c: var CritBitTree[T]`
- `key: string`
- `val: sink T`

**Output:** `bool`
**Generic parameters:** `T`

Returns true if c contains the given key. If the key does not exist, c[key] = val is performed.

**See also:**

* [incl proc](#incl,CritBitTree[void],string)
* [incl proc](#incl,CritBitTree[T],string,T)
* [containsOrIncl proc](#containsOrIncl,CritBitTree[void],string)
* [missingOrExcl proc](#missingOrExcl,CritBitTree[T],string)

### containsOrIncl

[ref: #symbol-containsorincl]

Returns true if c contains the given key. If the key does not exist, it is inserted into c.

**Input:**
- `c: var CritBitTree[void]`
- `key: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if c contains the given key. If the key does not exist, it is inserted into c.

**See also:**

* [incl proc](#incl,CritBitTree[void],string)
* [incl proc](#incl,CritBitTree[T],string,T)
* [containsOrIncl proc](#containsOrIncl,CritBitTree[T],string,T)
* [missingOrExcl proc](#missingOrExcl,CritBitTree[T],string)

### excl

[ref: #symbol-excl]

Removes key (and its associated value) from the set c. If the key does not exist, nothing happens.

**Input:**
- `c: var CritBitTree[T]`
- `key: string`

**Output:** *(none)*
**Generic parameters:** `T`

Removes key (and its associated value) from the set c. If the key does not exist, nothing happens.

**See also:**

* [incl proc](#incl,CritBitTree[void],string)
* [incl proc](#incl,CritBitTree[T],string,T)

### hasKey

[ref: #symbol-haskey]

**Input:**
- `c: CritBitTree[T]`
- `key: string`

**Output:** `bool`
**Generic parameters:** `T`

**Pragmas:** `inline`

Alias for [contains](#contains,CritBitTree[T],string).

### inc

[ref: #symbol-inc]

**Input:**
- `c: var CritBitTree[int]`
- `key: string`
- `val: int = 1`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Increments c[key] by val.

### incl

[ref: #symbol-incl]

Includes key in c.

**Input:**
- `c: var CritBitTree[void]`
- `key: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Includes key in c.

**See also:**

* [excl proc](#excl,CritBitTree[T],string)
* [incl proc](#incl,CritBitTree[T],string,T)

### incl

[ref: #symbol-incl]

Inserts key with value val into c.

**Input:**
- `c: var CritBitTree[T]`
- `key: string`
- `val: sink T`

**Output:** *(none)*
**Generic parameters:** `T`

Inserts key with value val into c.

**See also:**

* [excl proc](#excl,CritBitTree[T],string)
* [incl proc](#incl,CritBitTree[void],string)

### len

[ref: #symbol-len]

**Input:**
- `c: CritBitTree[T]`

**Output:** `int`
**Generic parameters:** `T`

**Pragmas:** `inline`

Returns the number of elements in c in O(1).

### missingOrExcl

[ref: #symbol-missingorexcl]

Returns true if c does not contain the given key. If the key does exist, c.excl(key) is performed.

**Input:**
- `c: var CritBitTree[T]`
- `key: string`

**Output:** `bool`
**Generic parameters:** `T`

Returns true if c does not contain the given key. If the key does exist, c.excl(key) is performed.

**See also:**

* [excl proc](#excl,CritBitTree[T],string)
* [containsOrIncl proc](#containsOrIncl,CritBitTree[T],string,T)
* [containsOrIncl proc](#containsOrIncl,CritBitTree[void],string)

### toCritBitTree

[ref: #symbol-tocritbittree]

**Input:**
- `pairs: sink openArray[(string, T)]`

**Output:** `CritBitTree[T]`
**Generic parameters:** `T`

Creates a new CritBitTree that contains the given pairs.

### toCritBitTree

[ref: #symbol-tocritbittree]

**Input:**
- `items: sink openArray[string]`

**Output:** `CritBitTree[void]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new CritBitTree that contains the given items.

## Type

### CritBitTree

[ref: #symbol-critbittree]

```nim
CritBitTree[T] = object
```

The crit bit tree can either be used as a mapping from strings to some type T or as a set of strings if T is void.
