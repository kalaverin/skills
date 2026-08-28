---
source_hash: 08ca00e5c7ef7f2d
source_path: lib/pure/collections/tables.nim
---

### `[]=`

[ref: #symbol-]

Inserts a (key, value) pair into t.

**Input:**
- `t: CountTableRef[A]`
- `key: A`
- `val: int`

**Output:** *(none)*
**Generic parameters:** `A`

Inserts a (key, value) pair into t.

See also:

* [[] proc](#[],CountTableRef[A],A) for retrieving a value of a key
* [inc proc](#inc,CountTableRef[A],A,int) for incrementing a value of a key

### `[]`

[ref: #symbol-]

Retrieves the value at t[key].

**Input:**
- `t: Table[A, B]`
- `key: A`

**Output:** `lent B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key].

If key is not in t, the KeyError exception is raised. One can check with [hasKey proc](#hasKey,Table[A,B],A) whether the key exists.

See also:

* [getOrDefault proc](#getOrDefault,Table[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,Table[A,B],A,B) to return a custom value if the key doesn't exist
* [[]= proc](#[]=,Table[A,B],A,sinkB) for inserting a new (key, value) pair in the table
* [hasKey proc](#hasKey,Table[A,B],A) for checking if a key is in the table

### `[]`

[ref: #symbol-]

Retrieves the value at t[key]. The value can be modified.

**Input:**
- `t: var Table[A, B]`
- `key: A`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key]. The value can be modified.

If key is not in t, the KeyError exception is raised.

See also:

* [getOrDefault proc](#getOrDefault,Table[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,Table[A,B],A,B) to return a custom value if the key doesn't exist
* [[]= proc](#[]=,Table[A,B],A,sinkB) for inserting a new (key, value) pair in the table
* [hasKey proc](#hasKey,Table[A,B],A) for checking if a key is in the table

### `[]`

[ref: #symbol-]

Retrieves the value at t[key].

**Input:**
- `t: TableRef[A, B]`
- `key: A`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key].

If key is not in t, the KeyError exception is raised. One can check with [hasKey proc](#hasKey,TableRef[A,B],A) whether the key exists.

See also:

* [getOrDefault proc](#getOrDefault,TableRef[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,TableRef[A,B],A,B) to return a custom value if the key doesn't exist
* [[]= proc](#[]=,TableRef[A,B],A,sinkB) for inserting a new (key, value) pair in the table
* [hasKey proc](#hasKey,TableRef[A,B],A) for checking if a key is in the table

### `[]`

[ref: #symbol-]

Retrieves the value at t[key].

**Input:**
- `t: OrderedTable[A, B]`
- `key: A`

**Output:** `lent B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key].

If key is not in t, the KeyError exception is raised. One can check with [hasKey proc](#hasKey,OrderedTable[A,B],A) whether the key exists.

See also:

* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A,B) to return a custom value if the key doesn't exist
* [[]= proc](#[]=,OrderedTable[A,B],A,sinkB) for inserting a new (key, value) pair in the table
* [hasKey proc](#hasKey,OrderedTable[A,B],A) for checking if a key is in the table

### `[]`

[ref: #symbol-]

Retrieves the value at t[key]. The value can be modified.

**Input:**
- `t: var OrderedTable[A, B]`
- `key: A`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key]. The value can be modified.

If key is not in t, the KeyError exception is raised.

See also:

* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A,B) to return a custom value if the key doesn't exist
* [[]= proc](#[]=,OrderedTable[A,B],A,sinkB) for inserting a new (key, value) pair in the table
* [hasKey proc](#hasKey,OrderedTable[A,B],A) for checking if a key is in the table

### `[]`

[ref: #symbol-]

Retrieves the value at t[key].

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key].

If key is not in t, the KeyError exception is raised. One can check with [hasKey proc](#hasKey,OrderedTableRef[A,B],A) whether the key exists.

See also:

* [getOrDefault proc](#getOrDefault,OrderedTableRef[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,OrderedTableRef[A,B],A,B) to return a custom value if the key doesn't exist
* [[]= proc](#[]=,OrderedTableRef[A,B],A,sinkB) for inserting a new (key, value) pair in the table
* [hasKey proc](#hasKey,OrderedTableRef[A,B],A) for checking if a key is in the table

### `[]`

[ref: #symbol-]

Retrieves the value at t[key] if key is in t. Otherwise 0 is returned.

**Input:**
- `t: CountTable[A]`
- `key: A`

**Output:** `int`
**Generic parameters:** `A`

Retrieves the value at t[key] if key is in t. Otherwise 0 is returned.

See also:

* [getOrDefault](#getOrDefault,CountTable[A],A,int) to return a custom value if the key doesn't exist
* [[]= proc](#[]%3D,CountTable[A],A,int) for inserting a new (key, value) pair in the table
* [hasKey proc](#hasKey,CountTable[A],A) for checking if a key is in the table

### `[]`

[ref: #symbol-]

Retrieves the value at t[key] if key is in t. Otherwise 0 is returned.

**Input:**
- `t: CountTableRef[A]`
- `key: A`

**Output:** `int`
**Generic parameters:** `A`

Retrieves the value at t[key] if key is in t. Otherwise 0 is returned.

See also:

* [getOrDefault](#getOrDefault,CountTableRef[A],A,int) to return a custom value if the key doesn't exist
* [inc proc](#inc,CountTableRef[A],A,int) to inc even if missing
* [[]= proc](#[]%3D,CountTableRef[A],A,int) for inserting a new (key, value) pair in the table
* [hasKey proc](#hasKey,CountTableRef[A],A) for checking if a key is in the table

### add

[ref: #symbol-add]

Puts a new (key, value) pair into t even if t[key] already exists.

**Input:**
- `t: var Table[A, B]`
- `key: A`
- `val: sink B`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

**Pragmas:** `deprecated: "Deprecated since v1.4; it was more confusing than useful, use `[]=`"`

Puts a new (key, value) pair into t even if t[key] already exists.

**This can introduce duplicate keys into the table!**

Use [[]= proc](#[]=,Table[A,B],A,sinkB) for inserting a new (key, value) pair in the table without introducing duplicates.

### add

[ref: #symbol-add]

Puts a new (key, value) pair into t even if t[key] already exists.

**Input:**
- `t: TableRef[A, B]`
- `key: A`
- `val: sink B`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

**Pragmas:** `deprecated: "Deprecated since v1.4; it was more confusing than useful, use `[]=`"`

Puts a new (key, value) pair into t even if t[key] already exists.

**This can introduce duplicate keys into the table!**

Use [[]= proc](#[]=,TableRef[A,B],A,sinkB) for inserting a new (key, value) pair in the table without introducing duplicates.

### add

[ref: #symbol-add]

Puts a new (key, value) pair into t even if t[key] already exists.

**Input:**
- `t: var OrderedTable[A, B]`
- `key: A`
- `val: sink B`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

**Pragmas:** `deprecated: "Deprecated since v1.4; it was more confusing than useful, use `[]=`"`

Puts a new (key, value) pair into t even if t[key] already exists.

**This can introduce duplicate keys into the table!**

Use [[]= proc](#[]=,OrderedTable[A,B],A,sinkB) for inserting a new (key, value) pair in the table without introducing duplicates.

### add

[ref: #symbol-add]

Puts a new (key, value) pair into t even if t[key] already exists.

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`
- `val: sink B`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

**Pragmas:** `deprecated: "Deprecated since v1.4; it was more confusing than useful, use `[]=`"`

Puts a new (key, value) pair into t even if t[key] already exists.

**This can introduce duplicate keys into the table!**

Use [[]= proc](#[]=,OrderedTableRef[A,B],A,sinkB) for inserting a new (key, value) pair in the table without introducing duplicates.

### clear

[ref: #symbol-clear]

Resets the table so that it is empty.

**Input:**
- `t: var Table[A, B]`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Resets the table so that it is empty.

See also:

* [del proc](#del,Table[A,B],A)
* [pop proc](#pop,Table[A,B],A,B)

### clear

[ref: #symbol-clear]

Resets the table so that it is empty.

**Input:**
- `t: TableRef[A, B]`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Resets the table so that it is empty.

See also:

* [del proc](#del,Table[A,B],A)
* [pop proc](#pop,Table[A,B],A,B)

### clear

[ref: #symbol-clear]

Resets the table so that it is empty.

**Input:**
- `t: var OrderedTable[A, B]`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Resets the table so that it is empty.

See also:

* [del proc](#del,OrderedTable[A,B],A)
* [pop proc](#pop,OrderedTable[A,B],A,B)

### clear

[ref: #symbol-clear]

Resets the table so that it is empty.

**Input:**
- `t: OrderedTableRef[A, B]`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Resets the table so that it is empty.

See also:

* [del proc](#del,OrderedTableRef[A,B],A)

### clear

[ref: #symbol-clear]

Resets the table so that it is empty.

**Input:**
- `t: var CountTable[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Resets the table so that it is empty.

See also:

* [del proc](#del,CountTable[A],A)
* [pop proc](#pop,CountTable[A],A,int)

### clear

[ref: #symbol-clear]

Resets the table so that it is empty.

**Input:**
- `t: CountTableRef[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Resets the table so that it is empty.

See also:

* [del proc](#del,CountTableRef[A],A)
* [pop proc](#pop,CountTableRef[A],A,int)

### contains

[ref: #symbol-contains]

**Input:**
- `t: Table[A, B]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Alias of [hasKey proc](#hasKey,Table[A,B],A) for use with the in operator.

### contains

[ref: #symbol-contains]

**Input:**
- `t: TableRef[A, B]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Alias of [hasKey proc](#hasKey,TableRef[A,B],A) for use with the in operator.

### contains

[ref: #symbol-contains]

**Input:**
- `t: OrderedTable[A, B]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Alias of [hasKey proc](#hasKey,OrderedTable[A,B],A) for use with the in operator.

### contains

[ref: #symbol-contains]

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Alias of [hasKey proc](#hasKey,OrderedTableRef[A,B],A) for use with the in operator.

### contains

[ref: #symbol-contains]

**Input:**
- `t: CountTable[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Alias of [hasKey proc](#hasKey,CountTable[A],A) for use with the in operator.

### contains

[ref: #symbol-contains]

**Input:**
- `t: CountTableRef[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Alias of [hasKey proc](#hasKey,CountTableRef[A],A) for use with the in operator.

### del

[ref: #symbol-del]

Deletes key from hash table t. Does nothing if the key does not exist.

**Input:**
- `t: var Table[A, B]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Deletes key from hash table t. Does nothing if the key does not exist.

**Warning:**
If duplicate keys were added (via the now deprecated add proc), this may need to be called multiple times.

See also:

* [pop proc](#pop,Table[A,B],A,B)
* [clear proc](#clear,Table[A,B]) to empty the whole table

### del

[ref: #symbol-del]

Deletes key from hash table t. Does nothing if the key does not exist.

**Input:**
- `t: TableRef[A, B]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Deletes key from hash table t. Does nothing if the key does not exist.

**Warning:**
If duplicate keys were added (via the now deprecated add proc), this may need to be called multiple times.

See also:

* [pop proc](#pop,TableRef[A,B],A,B)
* [clear proc](#clear,TableRef[A,B]) to empty the whole table

### del

[ref: #symbol-del]

Deletes key from hash table t. Does nothing if the key does not exist.

**Input:**
- `t: var OrderedTable[A, B]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Deletes key from hash table t. Does nothing if the key does not exist.

O(n) complexity.

See also:

* [pop proc](#pop,OrderedTable[A,B],A,B)
* [clear proc](#clear,OrderedTable[A,B]) to empty the whole table

### del

[ref: #symbol-del]

Deletes key from hash table t. Does nothing if the key does not exist.

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Deletes key from hash table t. Does nothing if the key does not exist.

See also:

* [clear proc](#clear,OrderedTableRef[A,B]) to empty the whole table

### del

[ref: #symbol-del]

Deletes key from table t. Does nothing if the key does not exist.

**Input:**
- `t: var CountTable[A]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`

Deletes key from table t. Does nothing if the key does not exist.

See also:

* [pop proc](#pop,CountTable[A],A,int)
* [clear proc](#clear,CountTable[A]) to empty the whole table

### del

[ref: #symbol-del]

Deletes key from table t. Does nothing if the key does not exist.

**Input:**
- `t: CountTableRef[A]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`

Deletes key from table t. Does nothing if the key does not exist.

See also:

* [pop proc](#pop,CountTableRef[A],A,int)
* [clear proc](#clear,CountTableRef[A]) to empty the whole table

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the value at t[key] if key is in t. Otherwise, the default initialization value for type B is returned (e.g. 0 for any integer type).

**Input:**
- `t: Table[A, B]`
- `key: A`

**Output:** `B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] if key is in t. Otherwise, the default initialization value for type B is returned (e.g. 0 for any integer type).

See also:

* [[] proc](#[],Table[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,Table[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,Table[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,Table[A,B],A,B)
* [getOrDefault proc](#getOrDefault,Table[A,B],A,B) to return a custom value if the key doesn't exist

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the value at t[key] if key is in t. Otherwise, def is returned.

**Input:**
- `t: Table[A, B]`
- `key: A`
- `def: B`

**Output:** `B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] if key is in t. Otherwise, def is returned.

See also:

* [[] proc](#[],Table[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,Table[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,Table[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,Table[A,B],A,B)
* [getOrDefault proc](#getOrDefault,Table[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the value at t[key] if key is in t. Otherwise, the default initialization value for type B is returned (e.g. 0 for any integer type).

**Input:**
- `t: TableRef[A, B]`
- `key: A`

**Output:** `B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] if key is in t. Otherwise, the default initialization value for type B is returned (e.g. 0 for any integer type).

See also:

* [[] proc](#[],TableRef[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,TableRef[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,TableRef[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,TableRef[A,B],A,B)
* [getOrDefault proc](#getOrDefault,TableRef[A,B],A,B) to return a custom value if the key doesn't exist

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the value at t[key] if key is in t. Otherwise, def is returned.

**Input:**
- `t: TableRef[A, B]`
- `key: A`
- `def: B`

**Output:** `B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] if key is in t. Otherwise, def is returned.

See also:

* [[] proc](#[],TableRef[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,TableRef[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,TableRef[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,TableRef[A,B],A,B)
* [getOrDefault proc](#getOrDefault,TableRef[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the value at t[key] if key is in t. Otherwise, the default initialization value for type B is returned (e.g. 0 for any integer type).

**Input:**
- `t: OrderedTable[A, B]`
- `key: A`

**Output:** `B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] if key is in t. Otherwise, the default initialization value for type B is returned (e.g. 0 for any integer type).

See also:

* [[] proc](#[],OrderedTable[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,OrderedTable[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,OrderedTable[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,OrderedTable[A,B],A,B)
* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A,B) to return a custom value if the key doesn't exist

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the value at t[key] if key is in t. Otherwise, def is returned.

**Input:**
- `t: OrderedTable[A, B]`
- `key: A`
- `def: B`

**Output:** `B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] if key is in t. Otherwise, def is returned.

See also:

* [[] proc](#[],OrderedTable[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,OrderedTable[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,OrderedTable[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,OrderedTable[A,B],A,B)
* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the value at t[key] if key is in t. Otherwise, the default initialization value for type B is returned (e.g. 0 for any integer type).

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`

**Output:** `B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] if key is in t. Otherwise, the default initialization value for type B is returned (e.g. 0 for any integer type).

See also:

* [[] proc](#[],OrderedTableRef[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,OrderedTableRef[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,OrderedTableRef[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,OrderedTableRef[A,B],A,B)
* [getOrDefault proc](#getOrDefault,OrderedTableRef[A,B],A,B) to return a custom value if the key doesn't exist

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the value at t[key] if key is in t. Otherwise, def is returned.

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`
- `def: B`

**Output:** `B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] if key is in t. Otherwise, def is returned.

See also:

* [[] proc](#[],OrderedTableRef[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,OrderedTableRef[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,OrderedTableRef[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,OrderedTableRef[A,B],A,B)
* [getOrDefault proc](#getOrDefault,OrderedTableRef[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the value at t[key] if key is in t. Otherwise, the integer value of def is returned.

**Input:**
- `t: CountTable[A]`
- `key: A`
- `def: int = 0`

**Output:** `int`
**Generic parameters:** `A`

Retrieves the value at t[key] if key is in t. Otherwise, the integer value of def is returned.

See also:

* [[] proc](#[],CountTable[A],A) for retrieving a value of a key
* [hasKey proc](#hasKey,CountTable[A],A) for checking if a key is in the table

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the value at t[key] if key is in t. Otherwise, the integer value of def is returned.

**Input:**
- `t: CountTableRef[A]`
- `key: A`
- `def: int`

**Output:** `int`
**Generic parameters:** `A`

Retrieves the value at t[key] if key is in t. Otherwise, the integer value of def is returned.

See also:

* [[] proc](#[],CountTableRef[A],A) for retrieving a value of a key
* [hasKey proc](#hasKey,CountTableRef[A],A) for checking if a key is in the table

### hash

[ref: #symbol-hash]

**Input:**
- `s: Table[K, V]`

**Output:** `Hash`
**Generic parameters:** `K`, `V`

### hash

[ref: #symbol-hash]

**Input:**
- `s: OrderedTable[K, V]`

**Output:** `Hash`
**Generic parameters:** `K`, `V`

### hash

[ref: #symbol-hash]

**Input:**
- `s: CountTable[V]`

**Output:** `Hash`
**Generic parameters:** `V`

### hasKey

[ref: #symbol-haskey]

Returns true if key is in the table t.

**Input:**
- `t: Table[A, B]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Returns true if key is in the table t.

See also:

* [contains proc](#contains,Table[A,B],A) for use with the in operator
* [[] proc](#[],Table[A,B],A) for retrieving a value of a key
* [getOrDefault proc](#getOrDefault,Table[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,Table[A,B],A,B) to return a custom value if the key doesn't exist

### hasKey

[ref: #symbol-haskey]

Returns true if key is in the table t.

**Input:**
- `t: TableRef[A, B]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Returns true if key is in the table t.

See also:

* [contains proc](#contains,TableRef[A,B],A) for use with the in operator
* [[] proc](#[],TableRef[A,B],A) for retrieving a value of a key
* [getOrDefault proc](#getOrDefault,TableRef[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,TableRef[A,B],A,B) to return a custom value if the key doesn't exist

### hasKey

[ref: #symbol-haskey]

Returns true if key is in the table t.

**Input:**
- `t: OrderedTable[A, B]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Returns true if key is in the table t.

See also:

* [contains proc](#contains,OrderedTable[A,B],A) for use with the in operator
* [[] proc](#[],OrderedTable[A,B],A) for retrieving a value of a key
* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A,B) to return a custom value if the key doesn't exist

### hasKey

[ref: #symbol-haskey]

Returns true if key is in the table t.

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Returns true if key is in the table t.

See also:

* [contains proc](#contains,OrderedTableRef[A,B],A) for use with the in operator
* [[] proc](#[],OrderedTableRef[A,B],A) for retrieving a value of a key
* [getOrDefault proc](#getOrDefault,OrderedTableRef[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,OrderedTableRef[A,B],A,B) to return a custom value if the key doesn't exist

### hasKey

[ref: #symbol-haskey]

Returns true if key is in the table t.

**Input:**
- `t: CountTable[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if key is in the table t.

See also:

* [contains proc](#contains,CountTable[A],A) for use with the in operator
* [[] proc](#[],CountTable[A],A) for retrieving a value of a key
* [getOrDefault proc](#getOrDefault,CountTable[A],A,int) to return a custom value if the key doesn't exist


[Prev](tables_2.md) | [Next](tables_4.md)
