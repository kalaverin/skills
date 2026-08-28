---
source_hash: ed5588f6914898a5
source_path: lib/pure/collections/sharedtables.nim
---

# sharedtables

[ref: #module-sharedtables]

Shared table support for Nim. Use plain old non GC'ed keys and values or you'll be in trouble. Uses a single lock to protect the table, lockfree implementations welcome but if lock contention is so high that you need a lockfree hash table, you're doing it wrong.

Unstable API.

## Examples

```nim
# If value exists, decrement it.
# If it becomes zero or less, delete the key
t.withKey(1'i64) do (k: int64, v: var int, pairExists: var bool):
  if pairExists:
    dec v
    if v <= 0:
      pairExists = false
```

```nim
var table: SharedTable[string, string]
init(table)

table["a"] = "x"
table["b"] = "y"
table["c"] = "z"


table.withValue("a", value):
  value[] = "m"

var flag = false
table.withValue("d", value):
  discard value
  doAssert false
do: # if "d" notin table
  flag = true

if flag:
  table["d"] = "n"

assert table.mget("a") == "m"
assert table.mget("d") == "n"
```

```nim
var table: SharedTable[string, string]
init(table)

table["a"] = "x"
table["b"] = "y"
table["c"] = "z"

table.withValue("a", value):
  assert value[] == "x"

table.withValue("b", value):
  value[] = "modified"

table.withValue("b", value):
  assert value[] == "modified"

table.withValue("nonexistent", value):
  assert false # not called
```

## Const

### defaultInitialSize

[ref: #symbol-defaultinitialsize]

```nim
defaultInitialSize = 32
```

## Proc

### `[]=`

[ref: #symbol-]

**Input:**
- `t: var SharedTable[A, B]`
- `key: A`
- `val: B`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Puts a (key, value)-pair into t.

### add

[ref: #symbol-add]

**Input:**
- `t: var SharedTable[A, B]`
- `key: A`
- `val: B`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Puts a new (key, value)-pair into t even if t[key] already exists. This can introduce duplicate keys into the table!

### deinitSharedTable

[ref: #symbol-deinitsharedtable]

**Input:**
- `t: var SharedTable[A, B]`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

### del

[ref: #symbol-del]

**Input:**
- `t: var SharedTable[A, B]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Deletes key from hash table t.

### hasKeyOrPut

[ref: #symbol-haskeyorput]

**Input:**
- `t: var SharedTable[A, B]`
- `key: A`
- `val: B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Returns true if key is in the table, otherwise inserts value.

### init

[ref: #symbol-init]

Creates a new hash table that is empty.

**Input:**
- `t: var SharedTable[A, B]`
- `initialSize:  = 32`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Creates a new hash table that is empty.

This proc must be called before any other usage of t.

### len

[ref: #symbol-len]

**Input:**
- `t: var SharedTable[A, B]`

**Output:** `int`
**Generic parameters:** `A`, `B`

Number of elements in t.

### mget

[ref: #symbol-mget]

**Input:**
- `t: var SharedTable[A, B]`
- `key: A`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key]. The value can be modified. If key is not in t, the KeyError exception is raised.

### mgetOrPut

[ref: #symbol-mgetorput]

**Input:**
- `t: var SharedTable[A, B]`
- `key: A`
- `val: B`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves value at t[key] or puts val if not present, either way returning a value which can be modified. **Note**: This is inherently unsafe in the context of multi-threading since it returns a pointer to B.

### withKey

[ref: #symbol-withkey]

Computes a new mapping for the key with the specified mapper procedure.

**Input:**
- `t: var SharedTable[A, B]`
- `key: A`
- `mapper: proc (key: A; val: var B; pairExists: var bool)`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Computes a new mapping for the key with the specified mapper procedure.

The mapper takes 3 arguments:

1. key - the current key, if it exists, or the key passed to withKey otherwise;
2. val - the current value, if the key exists, or default value of the type otherwise;
3. pairExists - true if the key exists, false otherwise.

The mapper can can modify val and pairExists values to change the mapping of the key or delete it from the table. When adding a value, make sure to set pairExists to true along with modifying the val.

The operation is performed atomically and other operations on the table will be blocked while the mapper is invoked, so it should be short and simple.

Example usage:

```
# If value exists, decrement it.
# If it becomes zero or less, delete the key
t.withKey(1'i64) do (k: int64, v: var int, pairExists: var bool):
  if pairExists:
    dec v
    if v <= 0:
      pairExists = false
```

## Template

### withValue

[ref: #symbol-withvalue]

**Input:**
- `t: var SharedTable[A, B]`
- `key: A`
- `value: untyped`
- `body: untyped`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Retrieves the value at t[key]. value can be modified in the scope of the withValue call.

### withValue

[ref: #symbol-withvalue]

**Input:**
- `t: var SharedTable[A, B]`
- `key: A`
- `value: untyped`
- `body1: untyped`
- `body2: untyped`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Retrieves the value at t[key]. value can be modified in the scope of the withValue call.

## Type

### SharedTable

[ref: #symbol-sharedtable]

```nim
SharedTable[A; B] = object
```

generic hash SharedTable
