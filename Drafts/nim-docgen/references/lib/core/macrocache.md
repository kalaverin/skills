---
source_hash: bf8277c764abbc2b
source_path: lib/core/macrocache.nim
---

# macrocache

[ref: #module-macrocache]

This module provides an API for macros to collect compile-time information across module boundaries. It should be used instead of global {.compileTime.} variables as those break incremental compilation.

The main feature of this module is that if you create CacheTables or any other Cache types with the same name in different modules, their content will be shared, meaning that you can fill a CacheTable in one module, and iterate over its contents in another.

## Examples

```nim
import std/macrocache
import std/macros

const mcTable = CacheTable"myTable"
const mcSeq = CacheSeq"mySeq"
const mcCounter = CacheCounter"myCounter"

static:
  # add new key "val" with the value `myval`
  let myval = newLit("hello ic")
  mcTable["val"] = myval
  assert mcTable["val"].kind == nnkStrLit

# Can access the same cache from different static contexts
# All the information is retained
static:
  # get value from `mcTable` and add it to `mcSeq`
  mcSeq.add(mcTable["val"])
  assert mcSeq.len == 1

static:
  assert mcSeq[0].strVal == "hello ic"

  # increase `mcCounter` by 3
  mcCounter.inc(3)
  assert mcCounter.value == 3
```

```nim
import std/macros

const mySeq = CacheSeq"backTest"
static:
  mySeq &= newLit(42)
  mySeq &= newLit(7)
  assert mySeq[^1].intVal == 7  # Last item
  assert mySeq[^2].intVal == 42 # Second last item
```

```nim
import std/macros

const mySeq = CacheSeq"subTest"
static:
  mySeq.add(newLit(42))
  assert mySeq[0].intVal == 42
```

```nim
import std/macros

const mcTable = CacheTable"subTest"
static:
  mcTable["toAdd"] = newStmtList()

  # get the NimNode back
  assert mcTable["toAdd"].kind == nnkStmtList
```

```nim
import std/macros

const mcTable = CacheTable"subTest"
static:
  # assign newLit(5) to the key "value"
  mcTable["value"] = newLit(5)

  # check that we can get the value back
  assert mcTable["value"].kind == nnkIntLit
```

```nim
import std/macros
const mySeq = CacheSeq"addTest"

static:
  mySeq.add(newLit(5))
  mySeq.add(newLit("hello ic"))

  assert mySeq.len == 2
  assert mySeq[1].strVal == "hello ic"
```

```nim
import std/macros
const mcTable = CacheTable"containsEx"
static:
  mcTable["foo"] = newEmptyNode()
  # Will be true since we gave it a value before
  assert "foo" in mcTable
```

```nim
import std/macros
const mcTable = CacheTable"hasKeyEx"
static:
  assert not mcTable.hasKey("foo")
  mcTable["foo"] = newEmptyNode()
  # Will now be true since we inserted a value
  assert mcTable.hasKey("foo")
```

```nim
static:
  let counter = CacheCounter"incTest"
  inc counter
  inc counter, 5

  assert counter.value == 6
```

```nim
import std/macros
const mySeq = CacheSeq"inclTest"

static:
  mySeq.incl(newLit(5))
  mySeq.incl(newLit(5))

  # still one element
  assert mySeq.len == 1
```

```nim
import std/macros

const mySeq = CacheSeq"lenTest"
static:
  let val = newLit("helper")
  mySeq.add(val)
  assert mySeq.len == 1

  mySeq.add(val)
  assert mySeq.len == 2
```

```nim
import std/macros

const dataTable = CacheTable"lenTest"
static:
  dataTable["key"] = newLit(5)
  assert dataTable.len == 1
```

```nim
static:
  let counter = CacheCounter"valTest"
  # default value is 0
  assert counter.value == 0

  inc counter
  assert counter.value == 1
```

```nim
import std/macros
const myseq = CacheSeq"itemsTest"

static:
  myseq.add(newLit(5))
  myseq.add(newLit(42))

  for val in myseq:
    # check that all values in `myseq` are int literals
    assert val.kind == nnkIntLit
```

```nim
import std/macros
const mytabl = CacheTable"values"

static:
  mytabl["intVal"] = newLit(5)
  mytabl["otherVal"] = newLit(6)
  for key, val in mytabl:
    # make sure that we actually get the same keys
    assert key in ["intVal", "otherVal"]

    # all vals are int literals
    assert val.kind == nnkIntLit
```

## Iterator

### items

[ref: #symbol-items]

**Input:**
- `s: CacheSeq`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over each item in s.

### pairs

[ref: #symbol-pairs]

**Input:**
- `t: CacheTable`

**Output:** `(string, NimNode)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over all (key, value) pairs in t.

## Proc

### `[]=`

[ref: #symbol-]

Inserts a (key, value) pair into t.

**Input:**
- `t: CacheTable`
- `key: string`
- `value: NimNode`

**Output:** *(none)*
**Pragmas:** `magic: "NctPut"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Inserts a (key, value) pair into t.

**Warning:**
key has to be unique! Assigning value to a key that is already in the table will result in a compiler error.

### `[]`

[ref: #symbol-]

**Input:**
- `s: CacheSeq`
- `i: int`

**Output:** `NimNode`
**Pragmas:** `magic: "NcsAt"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the ith value from s.

### `[]`

[ref: #symbol-]

**Input:**
- `s: CacheSeq`
- `i: BackwardsIndex`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the ith last value from s.

### `[]`

[ref: #symbol-]

**Input:**
- `t: CacheTable`
- `key: string`

**Output:** `NimNode`
**Pragmas:** `magic: "NctGet"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the NimNode value at t[key].

### add

[ref: #symbol-add]

**Input:**
- `s: CacheSeq`
- `value: NimNode`

**Output:** *(none)*
**Pragmas:** `magic: "NcsAdd"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds value to s.

### contains

[ref: #symbol-contains]

**Input:**
- `t: CacheTable`
- `key: string`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Alias of [hasKey](#hasKey(CacheTable, string)) for use with the in operator.

### hasKey

[ref: #symbol-haskey]

Returns true if key is in the table t.

**Input:**
- `t: CacheTable`
- `key: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if key is in the table t.

See also:

* [contains proc](#contains(CacheTable, string)) for use with the in operator

### inc

[ref: #symbol-inc]

**Input:**
- `c: CacheCounter`
- `by:  = 1`

**Output:** *(none)*
**Pragmas:** `magic: "NccInc"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Increments the counter c with the value by.

### incl

[ref: #symbol-incl]

Adds value to s.

**Input:**
- `s: CacheSeq`
- `value: NimNode`

**Output:** *(none)*
**Pragmas:** `magic: "NcsIncl"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds value to s.

**Hint:**
This doesn't do anything if value is already in s.

### len

[ref: #symbol-len]

**Input:**
- `s: CacheSeq`

**Output:** `int`
**Pragmas:** `magic: "NcsLen"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the length of s.

### len

[ref: #symbol-len]

**Input:**
- `t: CacheTable`

**Output:** `int`
**Pragmas:** `magic: "NctLen"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of elements in t.

### value

[ref: #symbol-value]

**Input:**
- `c: CacheCounter`

**Output:** `int`
**Pragmas:** `magic: "NccValue"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the value of a counter c.

## Type

### CacheCounter

[ref: #symbol-cachecounter]

```nim
CacheCounter = distinct string
```

Compile-time counter, uses int for storing the count.

### CacheSeq

[ref: #symbol-cacheseq]

```nim
CacheSeq = distinct string
```

Compile-time sequence of NimNodes.

### CacheTable

[ref: #symbol-cachetable]

Compile-time table of key-value pairs.

```nim
CacheTable = distinct string
```

Compile-time table of key-value pairs.

Keys are strings and values are NimNodes.
