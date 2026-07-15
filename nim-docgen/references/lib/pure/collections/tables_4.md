---
source_hash: 08ca00e5c7ef7f2d
source_path: lib/pure/collections/tables.nim
---

### hasKey

[ref: #symbol-haskey]

Returns true if key is in the table t.

**Input:**
- `t: CountTableRef[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Returns true if key is in the table t.

See also:

* [contains proc](#contains,CountTableRef[A],A) for use with the in operator
* [[] proc](#[],CountTableRef[A],A) for retrieving a value of a key
* [getOrDefault proc](#getOrDefault,CountTableRef[A],A,int) to return a custom value if the key doesn't exist

### hasKeyOrPut

[ref: #symbol-haskeyorput]

Returns true if key is in the table, otherwise inserts value.

**Input:**
- `t: var Table[A, B]`
- `key: A`
- `val: B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Returns true if key is in the table, otherwise inserts value.

See also:

* [hasKey proc](#hasKey,Table[A,B],A)
* [[] proc](#[],Table[A,B],A) for retrieving a value of a key
* [getOrDefault proc](#getOrDefault,Table[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,Table[A,B],A,B) to return a custom value if the key doesn't exist

### hasKeyOrPut

[ref: #symbol-haskeyorput]

Returns true if key is in the table, otherwise inserts value.

**Input:**
- `t: TableRef[A, B]`
- `key: A`
- `val: B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Returns true if key is in the table, otherwise inserts value.

See also:

* [hasKey proc](#hasKey,TableRef[A,B],A)
* [[] proc](#[],TableRef[A,B],A) for retrieving a value of a key
* [getOrDefault proc](#getOrDefault,TableRef[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,TableRef[A,B],A,B) to return a custom value if the key doesn't exist

### hasKeyOrPut

[ref: #symbol-haskeyorput]

Returns true if key is in the table, otherwise inserts value.

**Input:**
- `t: var OrderedTable[A, B]`
- `key: A`
- `val: B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Returns true if key is in the table, otherwise inserts value.

See also:

* [hasKey proc](#hasKey,OrderedTable[A,B],A)
* [[] proc](#[],OrderedTable[A,B],A) for retrieving a value of a key
* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A,B) to return a custom value if the key doesn't exist

### hasKeyOrPut

[ref: #symbol-haskeyorput]

Returns true if key is in the table, otherwise inserts value.

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`
- `val: B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Returns true if key is in the table, otherwise inserts value.

See also:

* [hasKey proc](#hasKey,OrderedTableRef[A,B],A)
* [[] proc](#[],OrderedTableRef[A,B],A) for retrieving a value of a key
* [getOrDefault proc](#getOrDefault,OrderedTableRef[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,OrderedTableRef[A,B],A,B) to return a custom value if the key doesn't exist

### inc

[ref: #symbol-inc]

**Input:**
- `t: var CountTable[A]`
- `key: A`
- `val:  = 1`

**Output:** *(none)*
**Generic parameters:** `A`

### inc

[ref: #symbol-inc]

**Input:**
- `t: CountTableRef[A]`
- `key: A`
- `val:  = 1`

**Output:** *(none)*
**Generic parameters:** `A`

### indexBy

[ref: #symbol-indexby]

**Input:**
- `collection: A`
- `index: proc (x: B): C`

**Output:** `Table[C, B]`
**Generic parameters:** `A`, `B`, `C`

Index the collection with the proc provided.

### initCountTable

[ref: #symbol-initcounttable]

Creates a new count table that is empty.

**Input:**
- `initialSize:  = defaultInitialSize`

**Output:** `CountTable[A]`
**Generic parameters:** `A`

Creates a new count table that is empty.

Starting from Nim v0.20, tables are initialized by default and it is not necessary to call this function explicitly.

See also:

* [toCountTable proc](#toCountTable,openArray[A])
* [newCountTable proc](#newCountTable) for creating a CountTableRef

### initOrderedTable

[ref: #symbol-initorderedtable]

Creates a new ordered hash table that is empty.

**Input:**
- `initialSize:  = defaultInitialSize`

**Output:** `OrderedTable[A, B]`
**Generic parameters:** `A`, `B`

Creates a new ordered hash table that is empty.

Starting from Nim v0.20, tables are initialized by default and it is not necessary to call this function explicitly.

See also:

* [toOrderedTable proc](#toOrderedTable,openArray[])
* [newOrderedTable proc](#newOrderedTable) for creating an OrderedTableRef

### initTable

[ref: #symbol-inittable]

Creates a new hash table that is empty.

**Input:**
- `initialSize:  = defaultInitialSize`

**Output:** `Table[A, B]`
**Generic parameters:** `A`, `B`

Creates a new hash table that is empty.

Starting from Nim v0.20, tables are initialized by default and it is not necessary to call this function explicitly.

See also:

* [toTable proc](#toTable,openArray[])
* [newTable proc](#newTable) for creating a TableRef

### largest

[ref: #symbol-largest]

Returns the (key, value) pair with the largest val. Efficiency: O(n)

**Input:**
- `t: CountTable[A]`

**Output:** `tuple[key: A, val: int]`
**Generic parameters:** `A`

Returns the (key, value) pair with the largest val. Efficiency: O(n)

See also:

* [smallest proc](#smallest,CountTable[A])

### largest

[ref: #symbol-largest]

Returns the (key, value) pair with the largest val. Efficiency: O(n)

**Input:**
- `t: CountTableRef[A]`

**Output:** `tuple[key: A, val: int]`
**Generic parameters:** `A`

Returns the (key, value) pair with the largest val. Efficiency: O(n)

See also:

* [smallest proc](#smallest,CountTable[A])

### len

[ref: #symbol-len]

**Input:**
- `t: Table[A, B]`

**Output:** `int`
**Generic parameters:** `A`, `B`

Returns the number of keys in t.

### len

[ref: #symbol-len]

**Input:**
- `t: TableRef[A, B]`

**Output:** `int`
**Generic parameters:** `A`, `B`

Returns the number of keys in t.

### len

[ref: #symbol-len]

**Input:**
- `t: OrderedTable[A, B]`

**Output:** `int`
**Generic parameters:** `A`, `B`

**Pragmas:** `inline`

Returns the number of keys in t.

### len

[ref: #symbol-len]

**Input:**
- `t: OrderedTableRef[A, B]`

**Output:** `int`
**Generic parameters:** `A`, `B`

**Pragmas:** `inline`

Returns the number of keys in t.

### len

[ref: #symbol-len]

**Input:**
- `t: CountTable[A]`

**Output:** `int`
**Generic parameters:** `A`

Returns the number of keys in t.

### len

[ref: #symbol-len]

**Input:**
- `t: CountTableRef[A]`

**Output:** `int`
**Generic parameters:** `A`

Returns the number of keys in t.

### merge

[ref: #symbol-merge]

**Input:**
- `s: var CountTable[A]`
- `t: CountTable[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Merges the second table into the first one (must be declared as var).

### merge

[ref: #symbol-merge]

**Input:**
- `s: CountTableRef[A]`
- `t: CountTableRef[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Merges the second table into the first one.

### mgetOrPut

[ref: #symbol-mgetorput]

Retrieves value at t[key] or puts val if not present, either way returning a value which can be modified.

**Input:**
- `t: var Table[A, B]`
- `key: A`
- `val: B`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves value at t[key] or puts val if not present, either way returning a value which can be modified.

Note that while the value returned is of type var B, it is easy to accidentally create a copy of the value at t[key]. Remember that seqs and strings are value types, and therefore cannot be copied into a separate variable for modification. See the example below.

See also:

* [[] proc](#[],Table[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,Table[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,Table[A,B],A,B)
* [getOrDefault proc](#getOrDefault,Table[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,Table[A,B],A,B) to return a custom value if the key doesn't exist

### mgetOrPut

[ref: #symbol-mgetorput]

**Input:**
- `t: var Table[A, B]`
- `key: A`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] or puts the default initialization value for type B (e.g. 0 for any integer type).

### mgetOrPut

[ref: #symbol-mgetorput]

Retrieves value at t[key] or puts val if not present, either way returning a value which can be modified.

**Input:**
- `t: TableRef[A, B]`
- `key: A`
- `val: B`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves value at t[key] or puts val if not present, either way returning a value which can be modified.

Note that while the value returned is of type var B, it is easy to accidentally create an copy of the value at t[key]. Remember that seqs and strings are value types, and therefore cannot be copied into a separate variable for modification. See the example below.

See also:

* [[] proc](#[],TableRef[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,TableRef[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,TableRef[A,B],A,B)
* [getOrDefault proc](#getOrDefault,TableRef[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,TableRef[A,B],A,B) to return a custom value if the key doesn't exist

### mgetOrPut

[ref: #symbol-mgetorput]

**Input:**
- `t: TableRef[A, B]`
- `key: A`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] or puts the default initialization value for type B (e.g. 0 for any integer type).

### mgetOrPut

[ref: #symbol-mgetorput]

Retrieves value at t[key] or puts val if not present, either way returning a value which can be modified.

**Input:**
- `t: var OrderedTable[A, B]`
- `key: A`
- `val: B`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves value at t[key] or puts val if not present, either way returning a value which can be modified.

See also:

* [[] proc](#[],OrderedTable[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,OrderedTable[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,OrderedTable[A,B],A,B)
* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,OrderedTable[A,B],A,B) to return a custom value if the key doesn't exist

### mgetOrPut

[ref: #symbol-mgetorput]

**Input:**
- `t: var OrderedTable[A, B]`
- `key: A`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] or puts the default initialization value for type B (e.g. 0 for any integer type).

### mgetOrPut

[ref: #symbol-mgetorput]

Retrieves value at t[key] or puts val if not present, either way returning a value which can be modified.

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`
- `val: B`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves value at t[key] or puts val if not present, either way returning a value which can be modified.

See also:

* [[] proc](#[],OrderedTableRef[A,B],A) for retrieving a value of a key
* [hasKey proc](#hasKey,OrderedTableRef[A,B],A)
* [hasKeyOrPut proc](#hasKeyOrPut,OrderedTableRef[A,B],A,B)
* [getOrDefault proc](#getOrDefault,OrderedTableRef[A,B],A) to return a default value (e.g. zero for int) if the key doesn't exist
* [getOrDefault proc](#getOrDefault,OrderedTableRef[A,B],A,B) to return a custom value if the key doesn't exist

### mgetOrPut

[ref: #symbol-mgetorput]

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] or puts the default initialization value for type B (e.g. 0 for any integer type).

### newCountTable

[ref: #symbol-newcounttable]

Creates a new ref count table that is empty.

**Input:**
- `initialSize:  = defaultInitialSize`

**Output:** `CountTableRef[A]`
**Generic parameters:** `A`

Creates a new ref count table that is empty.

See also:

* [newCountTable proc](#newCountTable,openArray[A]) for creating a CountTableRef from a collection
* [initCountTable proc](#initCountTable) for creating a CountTable

### newCountTable

[ref: #symbol-newcounttable]

**Input:**
- `keys: openArray[A]`

**Output:** `CountTableRef[A]`
**Generic parameters:** `A`

Creates a new ref count table with every member of a container keys having a count of how many times it occurs in that container.

### newOrderedTable

[ref: #symbol-neworderedtable]

Creates a new ordered ref hash table that is empty.

**Input:**
- `initialSize:  = defaultInitialSize`

**Output:** `OrderedTableRef[A, B]`
**Generic parameters:** `A`, `B`

Creates a new ordered ref hash table that is empty.

See also:

* [newOrderedTable proc](#newOrderedTable,openArray[]) for creating an OrderedTableRef from a collection of (key, value) pairs
* [initOrderedTable proc](#initOrderedTable) for creating an OrderedTable

### newOrderedTable

[ref: #symbol-neworderedtable]

Creates a new ordered ref hash table that contains the given pairs.

**Input:**
- `pairs: openArray[(A, B)]`

**Output:** `OrderedTableRef[A, B]`
**Generic parameters:** `A`, `B`

Creates a new ordered ref hash table that contains the given pairs.

pairs is a container consisting of (key, value) tuples.

See also:

* [newOrderedTable proc](#newOrderedTable)
* [toOrderedTable proc](#toOrderedTable,openArray[]) for an OrderedTable version

### newTable

[ref: #symbol-newtable]

Creates a new ref hash table that is empty.

**Input:**
- `initialSize:  = defaultInitialSize`

**Output:** `TableRef[A, B]`
**Generic parameters:** `A`, `B`

Creates a new ref hash table that is empty.

See also:

* [newTable proc](#newTable,openArray[]) for creating a TableRef from a collection of (key, value) pairs
* [initTable proc](#initTable) for creating a Table

### newTable

[ref: #symbol-newtable]

Creates a new ref hash table that contains the given pairs.

**Input:**
- `pairs: openArray[(A, B)]`

**Output:** `TableRef[A, B]`
**Generic parameters:** `A`, `B`

Creates a new ref hash table that contains the given pairs.

pairs is a container consisting of (key, value) tuples.

See also:

* [newTable proc](#newTable)
* [toTable proc](#toTable,openArray[]) for a Table version

### newTableFrom

[ref: #symbol-newtablefrom]

**Input:**
- `collection: A`
- `index: proc (x: B): C`

**Output:** `TableRef[C, B]`
**Generic parameters:** `A`, `B`, `C`

Index the collection with the proc provided.

### pop

[ref: #symbol-pop]

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

**Input:**
- `t: var Table[A, B]`
- `key: A`
- `val: var B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

**Warning:**
If duplicate keys were added (via the now deprecated add proc), this may need to be called multiple times.

See also:

* [del proc](#del,Table[A,B],A)
* [clear proc](#clear,Table[A,B]) to empty the whole table

### pop

[ref: #symbol-pop]

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

**Input:**
- `t: TableRef[A, B]`
- `key: A`
- `val: var B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

**Warning:**
If duplicate keys were added (via the now deprecated add proc), this may need to be called multiple times.

See also:

* [del proc](#del,TableRef[A,B],A)
* [clear proc](#clear,TableRef[A,B]) to empty the whole table

### pop

[ref: #symbol-pop]

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

**Input:**
- `t: var OrderedTable[A, B]`
- `key: A`
- `val: var B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

O(n) complexity.

See also:

* [del proc](#del,OrderedTable[A,B],A)
* [clear proc](#clear,OrderedTable[A,B]) to empty the whole table

### pop

[ref: #symbol-pop]

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`
- `val: var B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

See also:

* [del proc](#del,OrderedTableRef[A,B],A)
* [clear proc](#clear,OrderedTableRef[A,B]) to empty the whole table

### pop

[ref: #symbol-pop]

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

**Input:**
- `t: var CountTable[A]`
- `key: A`
- `val: var int`

**Output:** `bool`
**Generic parameters:** `A`

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

See also:

* [del proc](#del,CountTable[A],A)
* [clear proc](#clear,CountTable[A]) to empty the whole table

### pop

[ref: #symbol-pop]

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

**Input:**
- `t: CountTableRef[A]`
- `key: A`
- `val: var int`

**Output:** `bool`
**Generic parameters:** `A`

Deletes the key from the table. Returns true, if the key existed, and sets val to the mapping of the key. Otherwise, returns false, and the val is unchanged.

See also:

* [del proc](#del,CountTableRef[A],A)
* [clear proc](#clear,CountTableRef[A]) to empty the whole table

### smallest

[ref: #symbol-smallest]

Returns the (key, value) pair with the smallest val. Efficiency: O(n)

**Input:**
- `t: CountTable[A]`

**Output:** `tuple[key: A, val: int]`
**Generic parameters:** `A`

Returns the (key, value) pair with the smallest val. Efficiency: O(n)

See also:

* [largest proc](#largest,CountTable[A])

### smallest

[ref: #symbol-smallest]

Returns the (key, value) pair with the smallest val. Efficiency: O(n)

**Input:**
- `t: CountTableRef[A]`

**Output:** `tuple[key: A, val: int]`
**Generic parameters:** `A`

Returns the (key, value) pair with the smallest val. Efficiency: O(n)

See also:

* [largest proc](#largest,CountTableRef[A])

### sort

[ref: #symbol-sort]

Sorts t according to the function cmp.

**Input:**
- `t: var OrderedTable[A, B]`
- `cmp: proc (x, y: (A, B)): int`
- `order:  = SortOrder.Ascending`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

**Pragmas:** `effectsOf: cmp`

Sorts t according to the function cmp.

This modifies the internal list that kept the insertion order, so insertion order is lost after this call but key lookup and insertions remain possible after sort (in contrast to the [sort proc](#sort,CountTable[A]) for count tables).

### sort

[ref: #symbol-sort]

Sorts t according to the function cmp.

**Input:**
- `t: OrderedTableRef[A, B]`
- `cmp: proc (x, y: (A, B)): int`
- `order:  = SortOrder.Ascending`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

**Pragmas:** `effectsOf: cmp`

Sorts t according to the function cmp.

This modifies the internal list that kept the insertion order, so insertion order is lost after this call but key lookup and insertions remain possible after sort (in contrast to the [sort proc](#sort,CountTableRef[A]) for count tables).

### sort

[ref: #symbol-sort]

Sorts the count table so that, by default, the entry with the highest counter comes first.

**Input:**
- `t: var CountTable[A]`
- `order:  = SortOrder.Descending`

**Output:** *(none)*
**Generic parameters:** `A`

Sorts the count table so that, by default, the entry with the highest counter comes first.

**Warning:**
This is destructive! Once sorted, you must not modify t afterwards!

You can use the iterators [pairs](#pairs.i,CountTable[A]), [keys](#keys.i,CountTable[A]), and [values](#values.i,CountTable[A]) to iterate over t in the sorted order.

### sort

[ref: #symbol-sort]

Sorts the count table so that, by default, the entry with the highest counter comes first.

**Input:**
- `t: CountTableRef[A]`
- `order:  = SortOrder.Descending`

**Output:** *(none)*
**Generic parameters:** `A`

Sorts the count table so that, by default, the entry with the highest counter comes first.

**This is destructive! You must not modify `t` afterwards!**

You can use the iterators [pairs](#pairs.i,CountTableRef[A]), [keys](#keys.i,CountTableRef[A]), and [values](#values.i,CountTableRef[A]) to iterate over t in the sorted order.

### take

[ref: #symbol-take]

Alias for:

**Input:**
- `t: var Table[A, B]`
- `key: A`
- `val: var B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

**Pragmas:** `inline`

Alias for:

* [pop proc](#pop,Table[A,B],A,B)

### take

[ref: #symbol-take]

Alias for:

**Input:**
- `t: TableRef[A, B]`
- `key: A`
- `val: var B`

**Output:** `bool`
**Generic parameters:** `A`, `B`

**Pragmas:** `inline`

Alias for:

* [pop proc](#pop,TableRef[A,B],A,B)

### toCountTable

[ref: #symbol-tocounttable]

**Input:**
- `keys: openArray[A]`

**Output:** `CountTable[A]`
**Generic parameters:** `A`

Creates a new count table with every member of a container keys having a count of how many times it occurs in that container.

### toOrderedTable

[ref: #symbol-toorderedtable]

Creates a new ordered hash table that contains the given pairs.

**Input:**
- `pairs: openArray[(A, B)]`

**Output:** `OrderedTable[A, B]`
**Generic parameters:** `A`, `B`

Creates a new ordered hash table that contains the given pairs.

pairs is a container consisting of (key, value) tuples.

See also:

* [initOrderedTable proc](#initOrderedTable)
* [newOrderedTable proc](#newOrderedTable,openArray[]) for an OrderedTableRef version

### toTable

[ref: #symbol-totable]

Creates a new hash table that contains the given pairs.

**Input:**
- `pairs: openArray[(A, B)]`

**Output:** `Table[A, B]`
**Generic parameters:** `A`, `B`

Creates a new hash table that contains the given pairs.

pairs is a container consisting of (key, value) tuples.

See also:

* [initTable proc](#initTable)
* [newTable proc](#newTable,openArray[]) for a TableRef version

## Template

### withValue

[ref: #symbol-withvalue]

Retrieves the value at t[key].

**Input:**
- `t: var Table[A, B]`
- `key: A`
- `value: untyped`
- `body: untyped`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Retrieves the value at t[key].

value can be modified in the scope of the withValue call.


[Prev](tables_3.md) | [Next](tables_5.md)
