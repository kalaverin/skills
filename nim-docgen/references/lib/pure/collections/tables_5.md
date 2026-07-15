---
source_hash: 08ca00e5c7ef7f2d
source_path: lib/pure/collections/tables.nim
---

### withValue

[ref: #symbol-withvalue]

Retrieves the value at t[key].

**Input:**
- `t: var Table[A, B]`
- `key: A`
- `value: untyped`
- `body1: untyped`
- `body2: untyped`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Retrieves the value at t[key].

value can be modified in the scope of the withValue call.

### withValue

[ref: #symbol-withvalue]

**Input:**
- `t: Table[A, B]`
- `key: A`
- `value: untyped`
- `body1: untyped`
- `body2: untyped`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] if it exists, assigns it to the variable value and executes body

### withValue

[ref: #symbol-withvalue]

**Input:**
- `t: Table[A, B]`
- `key: A`
- `value: untyped`
- `body: untyped`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Retrieves the value at t[key] if it exists, assigns it to the variable value and executes body

## Type

### CountTable

[ref: #symbol-counttable]

Hash table that counts the number of each key. Unlike [Table](#Table), this uses a zero count to signal "empty" & so does not cache hash values for comparison reduction or resize acceleration.

```nim
CountTable[A] = object
```

Hash table that counts the number of each key. Unlike [Table](#Table), this uses a zero count to signal "empty" & so does not cache hash values for comparison reduction or resize acceleration.

For creating an empty CountTable, use [initCountTable proc](#initCountTable).

### CountTableRef

[ref: #symbol-counttableref]

Ref version of [CountTable](#CountTable).

```nim
CountTableRef[A] = ref CountTable[A]
```

Ref version of [CountTable](#CountTable).

For creating a new empty CountTableRef, use [newCountTable proc](#newCountTable).

### OrderedTable

[ref: #symbol-orderedtable]

Hash table that remembers insertion order.

```nim
OrderedTable[A; B] = object
```

Hash table that remembers insertion order.

For creating an empty OrderedTable, use [initOrderedTable proc](#initOrderedTable).

### OrderedTableRef

[ref: #symbol-orderedtableref]

Ref version of [OrderedTable](#OrderedTable).

```nim
OrderedTableRef[A; B] = ref OrderedTable[A, B]
```

Ref version of [OrderedTable](#OrderedTable).

For creating a new empty OrderedTableRef, use [newOrderedTable proc](#newOrderedTable).

### Table

[ref: #symbol-table]

Generic hash table, consisting of a key-value pair.

```nim
Table[A; B] = object
```

Generic hash table, consisting of a key-value pair.

data and counter are internal implementation details which can't be accessed.

For creating an empty Table, use [initTable proc](#initTable).

### TableRef

[ref: #symbol-tableref]

Ref version of [Table](#Table).

```nim
TableRef[A; B] = ref Table[A, B]
```

Ref version of [Table](#Table).

For creating a new empty TableRef, use [newTable proc](#newTable).

[Prev](tables_4.md)
