---
source_hash: 08ca00e5c7ef7f2d
source_path: lib/pure/collections/tables.nim
---

## Const

### defaultInitialSize

[ref: #symbol-defaultinitialsize]

```nim
defaultInitialSize = 32
```

## Iterator

### allValues

[ref: #symbol-allvalues]

Iterates over any value in the table t that belongs to the given key.

**Input:**
- `t: Table[A, B]`
- `key: A`

**Output:** `B`
**Generic parameters:** `A`, `B`

**Pragmas:** `deprecated: "Deprecated since v1.4; tables with duplicated keys are deprecated"`

Iterates over any value in the table t that belongs to the given key.

Used if you have a table with duplicate keys (as a result of using [add proc](#add,Table[A,B],A,sinkB)).

### keys

[ref: #symbol-keys]

Iterates over any key in the table t.

**Input:**
- `t: Table[A, B]`

**Output:** `lent A`
**Generic parameters:** `A`, `B`

Iterates over any key in the table t.

See also:

* [pairs iterator](#pairs.i,Table[A,B])
* [values iterator](#values.i,Table[A,B])

### keys

[ref: #symbol-keys]

Iterates over any key in the table t.

**Input:**
- `t: TableRef[A, B]`

**Output:** `lent A`
**Generic parameters:** `A`, `B`

Iterates over any key in the table t.

See also:

* [pairs iterator](#pairs.i,TableRef[A,B])
* [values iterator](#values.i,TableRef[A,B])

### keys

[ref: #symbol-keys]

Iterates over any key in the table t in insertion order.

**Input:**
- `t: OrderedTable[A, B]`

**Output:** `lent A`
**Generic parameters:** `A`, `B`

Iterates over any key in the table t in insertion order.

See also:

* [pairs iterator](#pairs.i,OrderedTable[A,B])
* [values iterator](#values.i,OrderedTable[A,B])

### keys

[ref: #symbol-keys]

Iterates over any key in the table t in insertion order.

**Input:**
- `t: OrderedTableRef[A, B]`

**Output:** `lent A`
**Generic parameters:** `A`, `B`

Iterates over any key in the table t in insertion order.

See also:

* [pairs iterator](#pairs.i,OrderedTableRef[A,B])
* [values iterator](#values.i,OrderedTableRef[A,B])

### keys

[ref: #symbol-keys]

Iterates over any key in the table t.

**Input:**
- `t: CountTable[A]`

**Output:** `lent A`
**Generic parameters:** `A`

Iterates over any key in the table t.

See also:

* [pairs iterator](#pairs.i,CountTable[A])
* [values iterator](#values.i,CountTable[A])

### keys

[ref: #symbol-keys]

Iterates over any key in the table t.

**Input:**
- `t: CountTableRef[A]`

**Output:** `A`
**Generic parameters:** `A`

Iterates over any key in the table t.

See also:

* [pairs iterator](#pairs.i,CountTable[A])
* [values iterator](#values.i,CountTable[A])

### mpairs

[ref: #symbol-mpairs]

Iterates over any (key, value) pair in the table t (must be declared as var). The values can be modified.

**Input:**
- `t: var Table[A, B]`

**Output:** `(A, var B)`
**Generic parameters:** `A`, `B`

Iterates over any (key, value) pair in the table t (must be declared as var). The values can be modified.

See also:

* [pairs iterator](#pairs.i,Table[A,B])
* [mvalues iterator](#mvalues.i,Table[A,B])

### mpairs

[ref: #symbol-mpairs]

Iterates over any (key, value) pair in the table t. The values can be modified.

**Input:**
- `t: TableRef[A, B]`

**Output:** `(A, var B)`
**Generic parameters:** `A`, `B`

Iterates over any (key, value) pair in the table t. The values can be modified.

See also:

* [pairs iterator](#pairs.i,TableRef[A,B])
* [mvalues iterator](#mvalues.i,TableRef[A,B])

### mpairs

[ref: #symbol-mpairs]

Iterates over any (key, value) pair in the table t (must be declared as var) in insertion order. The values can be modified.

**Input:**
- `t: var OrderedTable[A, B]`

**Output:** `(A, var B)`
**Generic parameters:** `A`, `B`

Iterates over any (key, value) pair in the table t (must be declared as var) in insertion order. The values can be modified.

See also:

* [pairs iterator](#pairs.i,OrderedTable[A,B])
* [mvalues iterator](#mvalues.i,OrderedTable[A,B])

### mpairs

[ref: #symbol-mpairs]

Iterates over any (key, value) pair in the table t in insertion order. The values can be modified.

**Input:**
- `t: OrderedTableRef[A, B]`

**Output:** `(A, var B)`
**Generic parameters:** `A`, `B`

Iterates over any (key, value) pair in the table t in insertion order. The values can be modified.

See also:

* [pairs iterator](#pairs.i,OrderedTableRef[A,B])
* [mvalues iterator](#mvalues.i,OrderedTableRef[A,B])

### mpairs

[ref: #symbol-mpairs]

Iterates over any (key, value) pair in the table t (must be declared as var). The values can be modified.

**Input:**
- `t: var CountTable[A]`

**Output:** `(A, var int)`
**Generic parameters:** `A`

Iterates over any (key, value) pair in the table t (must be declared as var). The values can be modified.

See also:

* [pairs iterator](#pairs.i,CountTable[A])
* [mvalues iterator](#mvalues.i,CountTable[A])

### mpairs

[ref: #symbol-mpairs]

Iterates over any (key, value) pair in the table t. The values can be modified.

**Input:**
- `t: CountTableRef[A]`

**Output:** `(A, var int)`
**Generic parameters:** `A`

Iterates over any (key, value) pair in the table t. The values can be modified.

See also:

* [pairs iterator](#pairs.i,CountTableRef[A])
* [mvalues iterator](#mvalues.i,CountTableRef[A])

### mvalues

[ref: #symbol-mvalues]

Iterates over any value in the table t (must be declared as var). The values can be modified.

**Input:**
- `t: var Table[A, B]`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Iterates over any value in the table t (must be declared as var). The values can be modified.

See also:

* [mpairs iterator](#mpairs.i,Table[A,B])
* [values iterator](#values.i,Table[A,B])

### mvalues

[ref: #symbol-mvalues]

Iterates over any value in the table t. The values can be modified.

**Input:**
- `t: TableRef[A, B]`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Iterates over any value in the table t. The values can be modified.

See also:

* [mpairs iterator](#mpairs.i,TableRef[A,B])
* [values iterator](#values.i,TableRef[A,B])

### mvalues

[ref: #symbol-mvalues]

Iterates over any value in the table t (must be declared as var) in insertion order. The values can be modified.

**Input:**
- `t: var OrderedTable[A, B]`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Iterates over any value in the table t (must be declared as var) in insertion order. The values can be modified.

See also:

* [mpairs iterator](#mpairs.i,OrderedTable[A,B])
* [values iterator](#values.i,OrderedTable[A,B])

### mvalues

[ref: #symbol-mvalues]

Iterates over any value in the table t in insertion order. The values can be modified.

**Input:**
- `t: OrderedTableRef[A, B]`

**Output:** `var B`
**Generic parameters:** `A`, `B`

Iterates over any value in the table t in insertion order. The values can be modified.

See also:

* [mpairs iterator](#mpairs.i,OrderedTableRef[A,B])
* [values iterator](#values.i,OrderedTableRef[A,B])

### mvalues

[ref: #symbol-mvalues]

Iterates over any value in the table t (must be declared as var). The values can be modified.

**Input:**
- `t: var CountTable[A]`

**Output:** `var int`
**Generic parameters:** `A`

Iterates over any value in the table t (must be declared as var). The values can be modified.

See also:

* [mpairs iterator](#mpairs.i,CountTable[A])
* [values iterator](#values.i,CountTable[A])

### mvalues

[ref: #symbol-mvalues]

Iterates over any value in the table t. The values can be modified.

**Input:**
- `t: CountTableRef[A]`

**Output:** `var int`
**Generic parameters:** `A`

Iterates over any value in the table t. The values can be modified.

See also:

* [mpairs iterator](#mpairs.i,CountTableRef[A])
* [values iterator](#values.i,CountTableRef[A])

### pairs

[ref: #symbol-pairs]

Iterates over any (key, value) pair in the table t.

**Input:**
- `t: Table[A, B]`

**Output:** `(A, B)`
**Generic parameters:** `A`, `B`

Iterates over any (key, value) pair in the table t.

See also:

* [mpairs iterator](#mpairs.i,Table[A,B])
* [keys iterator](#keys.i,Table[A,B])
* [values iterator](#values.i,Table[A,B])

**Examples:**

```
let a = {
  'o': [1, 5, 7, 9],
  'e': [2, 4, 6, 8]
  }.toTable

for k, v in a.pairs:
  echo "key: ", k
  echo "value: ", v

# key: e
# value: [2, 4, 6, 8]
# key: o
# value: [1, 5, 7, 9]
```

### pairs

[ref: #symbol-pairs]

Iterates over any (key, value) pair in the table t.

**Input:**
- `t: TableRef[A, B]`

**Output:** `(A, B)`
**Generic parameters:** `A`, `B`

Iterates over any (key, value) pair in the table t.

See also:

* [mpairs iterator](#mpairs.i,TableRef[A,B])
* [keys iterator](#keys.i,TableRef[A,B])
* [values iterator](#values.i,TableRef[A,B])

**Examples:**

```
let a = {
  'o': [1, 5, 7, 9],
  'e': [2, 4, 6, 8]
  }.newTable

for k, v in a.pairs:
  echo "key: ", k
  echo "value: ", v

# key: e
# value: [2, 4, 6, 8]
# key: o
# value: [1, 5, 7, 9]
```

### pairs

[ref: #symbol-pairs]

Iterates over any (key, value) pair in the table t in insertion order.

**Input:**
- `t: OrderedTable[A, B]`

**Output:** `(A, B)`
**Generic parameters:** `A`, `B`

Iterates over any (key, value) pair in the table t in insertion order.

See also:

* [mpairs iterator](#mpairs.i,OrderedTable[A,B])
* [keys iterator](#keys.i,OrderedTable[A,B])
* [values iterator](#values.i,OrderedTable[A,B])

**Examples:**

```
let a = {
  'o': [1, 5, 7, 9],
  'e': [2, 4, 6, 8]
  }.toOrderedTable

for k, v in a.pairs:
  echo "key: ", k
  echo "value: ", v

# key: o
# value: [1, 5, 7, 9]
# key: e
# value: [2, 4, 6, 8]
```

### pairs

[ref: #symbol-pairs]

Iterates over any (key, value) pair in the table t in insertion order.

**Input:**
- `t: OrderedTableRef[A, B]`

**Output:** `(A, B)`
**Generic parameters:** `A`, `B`

Iterates over any (key, value) pair in the table t in insertion order.

See also:

* [mpairs iterator](#mpairs.i,OrderedTableRef[A,B])
* [keys iterator](#keys.i,OrderedTableRef[A,B])
* [values iterator](#values.i,OrderedTableRef[A,B])

**Examples:**

```
let a = {
  'o': [1, 5, 7, 9],
  'e': [2, 4, 6, 8]
  }.newOrderedTable

for k, v in a.pairs:
  echo "key: ", k
  echo "value: ", v

# key: o
# value: [1, 5, 7, 9]
# key: e
# value: [2, 4, 6, 8]
```

### pairs

[ref: #symbol-pairs]

Iterates over any (key, value) pair in the table t.

**Input:**
- `t: CountTable[A]`

**Output:** `(A, int)`
**Generic parameters:** `A`

Iterates over any (key, value) pair in the table t.

See also:

* [mpairs iterator](#mpairs.i,CountTable[A])
* [keys iterator](#keys.i,CountTable[A])
* [values iterator](#values.i,CountTable[A])

**Examples:**

```
let a = toCountTable("abracadabra")

for k, v in pairs(a):
  echo "key: ", k
  echo "value: ", v

# key: a
# value: 5
# key: b
# value: 2
# key: c
# value: 1
# key: d
# value: 1
# key: r
# value: 2
```

### pairs

[ref: #symbol-pairs]

Iterates over any (key, value) pair in the table t.

**Input:**
- `t: CountTableRef[A]`

**Output:** `(A, int)`
**Generic parameters:** `A`

Iterates over any (key, value) pair in the table t.

See also:

* [mpairs iterator](#mpairs.i,CountTableRef[A])
* [keys iterator](#keys.i,CountTableRef[A])
* [values iterator](#values.i,CountTableRef[A])

**Examples:**

```
let a = newCountTable("abracadabra")

for k, v in pairs(a):
  echo "key: ", k
  echo "value: ", v

# key: a
# value: 5
# key: b
# value: 2
# key: c
# value: 1
# key: d
# value: 1
# key: r
# value: 2
```

### values

[ref: #symbol-values]

Iterates over any value in the table t.

**Input:**
- `t: Table[A, B]`

**Output:** `lent B`
**Generic parameters:** `A`, `B`

Iterates over any value in the table t.

See also:

* [pairs iterator](#pairs.i,Table[A,B])
* [keys iterator](#keys.i,Table[A,B])
* [mvalues iterator](#mvalues.i,Table[A,B])

### values

[ref: #symbol-values]

Iterates over any value in the table t.

**Input:**
- `t: TableRef[A, B]`

**Output:** `lent B`
**Generic parameters:** `A`, `B`

Iterates over any value in the table t.

See also:

* [pairs iterator](#pairs.i,TableRef[A,B])
* [keys iterator](#keys.i,TableRef[A,B])
* [mvalues iterator](#mvalues.i,TableRef[A,B])

### values

[ref: #symbol-values]

Iterates over any value in the table t in insertion order.

**Input:**
- `t: OrderedTable[A, B]`

**Output:** `lent B`
**Generic parameters:** `A`, `B`

Iterates over any value in the table t in insertion order.

See also:

* [pairs iterator](#pairs.i,OrderedTable[A,B])
* [keys iterator](#keys.i,OrderedTable[A,B])
* [mvalues iterator](#mvalues.i,OrderedTable[A,B])

### values

[ref: #symbol-values]

Iterates over any value in the table t in insertion order.

**Input:**
- `t: OrderedTableRef[A, B]`

**Output:** `lent B`
**Generic parameters:** `A`, `B`

Iterates over any value in the table t in insertion order.

See also:

* [pairs iterator](#pairs.i,OrderedTableRef[A,B])
* [keys iterator](#keys.i,OrderedTableRef[A,B])
* [mvalues iterator](#mvalues.i,OrderedTableRef[A,B])

### values

[ref: #symbol-values]

Iterates over any value in the table t.

**Input:**
- `t: CountTable[A]`

**Output:** `int`
**Generic parameters:** `A`

Iterates over any value in the table t.

See also:

* [pairs iterator](#pairs.i,CountTable[A])
* [keys iterator](#keys.i,CountTable[A])
* [mvalues iterator](#mvalues.i,CountTable[A])

### values

[ref: #symbol-values]

Iterates over any value in the table t.

**Input:**
- `t: CountTableRef[A]`

**Output:** `int`
**Generic parameters:** `A`

Iterates over any value in the table t.

See also:

* [pairs iterator](#pairs.i,CountTableRef[A])
* [keys iterator](#keys.i,CountTableRef[A])
* [mvalues iterator](#mvalues.i,CountTableRef[A])

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `t: Table[A, B]`

**Output:** `string`
**Generic parameters:** `A`, `B`

The $ operator for hash tables. Used internally when calling echo on a table.

### `$`

[ref: #symbol-]

**Input:**
- `t: TableRef[A, B]`

**Output:** `string`
**Generic parameters:** `A`, `B`

The $ operator for hash tables. Used internally when calling echo on a table.

### `$`

[ref: #symbol-]

**Input:**
- `t: OrderedTable[A, B]`

**Output:** `string`
**Generic parameters:** `A`, `B`

The $ operator for ordered hash tables. Used internally when calling echo on a table.

### `$`

[ref: #symbol-]

**Input:**
- `t: OrderedTableRef[A, B]`

**Output:** `string`
**Generic parameters:** `A`, `B`

The $ operator for hash tables. Used internally when calling echo on a table.

### `$`

[ref: #symbol-]

**Input:**
- `t: CountTable[A]`

**Output:** `string`
**Generic parameters:** `A`

The $ operator for count tables. Used internally when calling echo on a table.

### `$`

[ref: #symbol-]

**Input:**
- `t: CountTableRef[A]`

**Output:** `string`
**Generic parameters:** `A`

The $ operator for count tables. Used internally when calling echo on a table.

### `==`

[ref: #symbol-]

**Input:**
- `s: Table[A, B]`
- `t: Table[A, B]`

**Output:** `bool`
**Generic parameters:** `A`, `B`

The == operator for hash tables. Returns true if the content of both tables contains the same key-value pairs. Insert order does not matter.

### `==`

[ref: #symbol-]

**Input:**
- `s: TableRef[A, B]`
- `t: TableRef[A, B]`

**Output:** `bool`
**Generic parameters:** `A`, `B`

The == operator for hash tables. Returns true if either both tables are nil, or neither is nil and the content of both tables contains the same key-value pairs. Insert order does not matter.

### `==`

[ref: #symbol-]

**Input:**
- `s: OrderedTable[A, B]`
- `t: OrderedTable[A, B]`

**Output:** `bool`
**Generic parameters:** `A`, `B`

The == operator for ordered hash tables. Returns true if both the content and the order are equal.

### `==`

[ref: #symbol-]

**Input:**
- `s: OrderedTableRef[A, B]`
- `t: OrderedTableRef[A, B]`

**Output:** `bool`
**Generic parameters:** `A`, `B`

The == operator for ordered hash tables. Returns true if either both tables are nil, or neither is nil and the content and the order of both are equal.

### `==`

[ref: #symbol-]

**Input:**
- `s: CountTable[A]`
- `t: CountTable[A]`

**Output:** `bool`
**Generic parameters:** `A`

The == operator for count tables. Returns true if both tables contain the same keys with the same count. Insert order does not matter.

### `==`

[ref: #symbol-]

**Input:**
- `s: CountTableRef[A]`
- `t: CountTableRef[A]`

**Output:** `bool`
**Generic parameters:** `A`

The == operator for count tables. Returns true if either both tables are nil, or neither is nil and both contain the same keys with the same count. Insert order does not matter.

### `[]=`

[ref: #symbol-]

Inserts a (key, value) pair into t.

**Input:**
- `t: var Table[A, B]`
- `key: A`
- `val: sink B`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Inserts a (key, value) pair into t.

See also:

* [[] proc](#[],Table[A,B],A) for retrieving a value of a key
* [hasKeyOrPut proc](#hasKeyOrPut,Table[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,Table[A,B],A,B)
* [del proc](#del,Table[A,B],A) for removing a key from the table

### `[]=`

[ref: #symbol-]

Inserts a (key, value) pair into t.

**Input:**
- `t: TableRef[A, B]`
- `key: A`
- `val: sink B`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Inserts a (key, value) pair into t.

See also:

* [[] proc](#[],TableRef[A,B],A) for retrieving a value of a key
* [hasKeyOrPut proc](#hasKeyOrPut,TableRef[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,TableRef[A,B],A,B)
* [del proc](#del,TableRef[A,B],A) for removing a key from the table

### `[]=`

[ref: #symbol-]

Inserts a (key, value) pair into t.

**Input:**
- `t: var OrderedTable[A, B]`
- `key: A`
- `val: sink B`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Inserts a (key, value) pair into t.

See also:

* [[] proc](#[],OrderedTable[A,B],A) for retrieving a value of a key
* [hasKeyOrPut proc](#hasKeyOrPut,OrderedTable[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,OrderedTable[A,B],A,B)
* [del proc](#del,OrderedTable[A,B],A) for removing a key from the table

### `[]=`

[ref: #symbol-]

Inserts a (key, value) pair into t.

**Input:**
- `t: OrderedTableRef[A, B]`
- `key: A`
- `val: sink B`

**Output:** *(none)*
**Generic parameters:** `A`, `B`

Inserts a (key, value) pair into t.

See also:

* [[] proc](#[],OrderedTableRef[A,B],A) for retrieving a value of a key
* [hasKeyOrPut proc](#hasKeyOrPut,OrderedTableRef[A,B],A,B)
* [mgetOrPut proc](#mgetOrPut,OrderedTableRef[A,B],A,B)
* [del proc](#del,OrderedTableRef[A,B],A) for removing a key from the table

### `[]=`

[ref: #symbol-]

Inserts a (key, value) pair into t.

**Input:**
- `t: var CountTable[A]`
- `key: A`
- `val: int`

**Output:** *(none)*
**Generic parameters:** `A`

Inserts a (key, value) pair into t.

See also:

* [[] proc](#[],CountTable[A],A) for retrieving a value of a key
* [inc proc](#inc,CountTable[A],A,int) for incrementing a value of a key


[Prev](tables_1.md) | [Next](tables_3.md)
