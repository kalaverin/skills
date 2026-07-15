---
source_hash: 08ca00e5c7ef7f2d
source_path: lib/pure/collections/tables.nim
---

# tables

[ref: #module-tables]

The tables module implements variants of an efficient hash table (also often named dictionary in other programming languages) that is a mapping from keys to values.

There are several different types of hash tables available:

* [Table](#Table) is the usual hash table,
* [OrderedTable](#OrderedTable) is like Table but remembers insertion order,
* [CountTable](#CountTable) is a mapping from a key to its number of occurrences

For consistency with every other data type in Nim these have **value** semantics, this means that = performs a copy of the hash table.

For [ref semantics](manual.html#types-reference-and-pointer-types) use their Ref variants: [TableRef](#TableRef), [OrderedTableRef](#OrderedTableRef), and [CountTableRef](#CountTableRef).

To give an example, when a is a Table, then var b = a gives b as a new independent table. b is initialised with the contents of a. Changing b does not affect a and vice versa:

On the other hand, when a is a TableRef instead, then changes to b also affect a. Both a and b **ref** the same data structure:

---

# [Basic usage](#basic-usage)

## [Table](#basic-usage-table)

## [OrderedTable](#basic-usage-orderedtable)

[OrderedTable](#OrderedTable) is used when it is important to preserve the insertion order of keys.

## [CountTable](#basic-usage-counttable)

[CountTable](#CountTable) is useful for counting number of items of some container (e.g. string, sequence or array), as it is a mapping where the items are the keys, and their number of occurrences are the values. For that purpose [toCountTable proc](#toCountTable,openArray[A]) comes in handy:

The same could have been achieved by manually iterating over a container and increasing each key's value with [inc proc](#inc,CountTable[A],A,int):

---

## [Hashing](#basic-usage-hashing)

If you are using simple standard types like int or string for the keys of the table you won't have any problems, but as soon as you try to use a more complex object as a key you will be greeted by a strange compiler error:

```
Error: type mismatch: got (Person)
but expected one of:
hashes.hash(x: openArray[A]): Hash
hashes.hash(x: int): Hash
hashes.hash(x: float): Hash
```

What is happening here is that the types used for table keys require to have a hash() proc which will convert them to a [Hash](hashes.html#Hash) value, and the compiler is listing all the hash functions it knows. Additionally there has to be a == operator that provides the same semantics as its corresponding hash proc.

After you add hash and == for your custom type everything will work. Currently, however, hash for objects is not defined, whereas system.== for objects does exist and performs a "deep" comparison (every field is compared) which is usually what you want. So in the following example implementing only hash suffices:

---

# [See also](#see-also)

* [json module](json.html) for table-like structure which allows heterogeneous members
* [strtabs module](strtabs.html) for efficient hash tables mapping from strings to strings
* [hashes module](hashes.html) for helper functions for hashing

## Examples

```nim
import std/tables
var
  a = {1: "one", 2: "two"}.toTable  # creates a Table
  b = a

assert a == b

b[3] = "three"
assert 3 notin a
assert 3 in b
assert a != b
```

```nim
import std/tables
var
  a = {1: "one", 2: "two"}.newTable  # creates a TableRef
  b = a

assert a == b

b[3] = "three"

assert 3 in a
assert 3 in b
assert a == b
```

```nim
import std/tables
from std/sequtils import zip

let
  names = ["John", "Paul", "George", "Ringo"]
  years = [1940, 1942, 1943, 1940]

var beatles = initTable[string, int]()

for pairs in zip(names, years):
  let (name, birthYear) = pairs
  beatles[name] = birthYear

assert beatles == {"George": 1943, "Ringo": 1940, "Paul": 1942, "John": 1940}.toTable


var beatlesByYear = initTable[int, seq[string]]()

for pairs in zip(years, names):
  let (birthYear, name) = pairs
  if not beatlesByYear.hasKey(birthYear):
    # if a key doesn't exist, we create one with an empty sequence
    # before we can add elements to it
    beatlesByYear[birthYear] = @[]
  beatlesByYear[birthYear].add(name)

assert beatlesByYear == {1940: @["John", "Ringo"], 1942: @["Paul"], 1943: @["George"]}.toTable
```

```nim
import std/tables
let
  a = [('z', 1), ('y', 2), ('x', 3)]
  ot = a.toOrderedTable  # ordered tables

assert $ot == """{'z': 1, 'y': 2, 'x': 3}"""
```

```nim
import std/tables
let myString = "abracadabra"
let letterFrequencies = toCountTable(myString)
assert $letterFrequencies == "{'a': 5, 'd': 1, 'b': 2, 'r': 2, 'c': 1}"
```

```nim
import std/tables
let myString = "abracadabra"
var letterFrequencies = initCountTable[char]()
for c in myString:
  letterFrequencies.inc(c)
assert $letterFrequencies == "{'d': 1, 'r': 2, 'c': 1, 'a': 5, 'b': 2}"
```

```nim
import std/tables
import std/hashes

type
  Person = object
    firstName, lastName: string

proc hash(x: Person): Hash =
  ## Piggyback on the already available string hash proc.
  ##
  ## Without this proc nothing works!
  result = x.firstName.hash !& x.lastName.hash
  result = !$result

var
  salaries = initTable[Person, int]()
  p1, p2: Person

p1.firstName = "Jon"
p1.lastName = "Ross"
salaries[p1] = 30_000

p2.firstName = "소진"
p2.lastName = "박"
salaries[p2] = 45_000
```

```nim
let
  a = {'a': 5, 'b': 9, 'c': 13}.toOrderedTable
  b = {'b': 9, 'c': 13, 'a': 5}.toOrderedTable
doAssert a != b
```

```nim
let
  a = {'a': 5, 'b': 9, 'c': 13}.newOrderedTable
  b = {'b': 9, 'c': 13, 'a': 5}.newOrderedTable
doAssert a != b
```

```nim
let
  a = {'a': 5, 'b': 9, 'c': 13}.toTable
  b = {'b': 9, 'c': 13, 'a': 5}.toTable
doAssert a == b
```

```nim
let
  a = {'a': 5, 'b': 9, 'c': 13}.newTable
  b = {'b': 9, 'c': 13, 'a': 5}.newTable
doAssert a == b
```

```nim
let a = {'a': 5, 'b': 9}.toOrderedTable
doAssert a['a'] == 5
doAssertRaises(KeyError):
  echo a['z']
```

```nim
let a = {'a': 5, 'b': 9}.newOrderedTable
doAssert a['a'] == 5
doAssertRaises(KeyError):
  echo a['z']
```

```nim
let a = {'a': 5, 'b': 9}.toTable
doAssert a['a'] == 5
doAssertRaises(KeyError):
  echo a['z']
```

```nim
let a = {'a': 5, 'b': 9}.newTable
doAssert a['a'] == 5
doAssertRaises(KeyError):
  echo a['z']
```

```nim
var a = newOrderedTable[char, int]()
a['x'] = 7
a['y'] = 33
doAssert a == {'x': 7, 'y': 33}.newOrderedTable
```

```nim
var a = newTable[char, int]()
a['x'] = 7
a['y'] = 33
doAssert a == {'x': 7, 'y': 33}.newTable
```

```nim
var a = initOrderedTable[char, int]()
a['x'] = 7
a['y'] = 33
doAssert a == {'x': 7, 'y': 33}.toOrderedTable
```

```nim
var a = initTable[char, int]()
a['x'] = 7
a['y'] = 33
doAssert a == {'x': 7, 'y': 33}.toTable
```

```nim
var a = {'a': 5, 'b': 9, 'c': 13}.newOrderedTable
doAssert len(a) == 3
clear(a)
doAssert len(a) == 0
```

```nim
var a = {'a': 5, 'b': 9, 'c': 13}.newTable
doAssert len(a) == 3
clear(a)
doAssert len(a) == 0
```

```nim
var a = {'a': 5, 'b': 9, 'c': 13}.toOrderedTable
doAssert len(a) == 3
clear(a)
doAssert len(a) == 0
```

```nim
var a = {'a': 5, 'b': 9, 'c': 13}.toTable
doAssert len(a) == 3
clear(a)
doAssert len(a) == 0
```

```nim
let a = {'a': 5, 'b': 9}.toOrderedTable
doAssert 'b' in a == true
doAssert a.contains('z') == false
```

```nim
let a = {'a': 5, 'b': 9}.newOrderedTable
doAssert 'b' in a == true
doAssert a.contains('z') == false
```

```nim
let a = {'a': 5, 'b': 9}.toTable
doAssert 'b' in a == true
doAssert a.contains('z') == false
```

```nim
let a = {'a': 5, 'b': 9}.newTable
doAssert 'b' in a == true
doAssert a.contains('z') == false
```

```nim
var a = {'a': 5, 'b': 9, 'c': 13}.newOrderedTable
a.del('a')
doAssert a == {'b': 9, 'c': 13}.newOrderedTable
a.del('z')
doAssert a == {'b': 9, 'c': 13}.newOrderedTable
```

```nim
var a = {'a': 5, 'b': 9, 'c': 13}.newTable
a.del('a')
doAssert a == {'b': 9, 'c': 13}.newTable
a.del('z')
doAssert a == {'b': 9, 'c': 13}.newTable
```

```nim
var a = {'a': 5, 'b': 9, 'c': 13}.toOrderedTable
a.del('a')
doAssert a == {'b': 9, 'c': 13}.toOrderedTable
a.del('z')
doAssert a == {'b': 9, 'c': 13}.toOrderedTable
```

```nim
var a = {'a': 5, 'b': 9, 'c': 13}.toTable
a.del('a')
doAssert a == {'b': 9, 'c': 13}.toTable
a.del('z')
doAssert a == {'b': 9, 'c': 13}.toTable
```

```nim
var a = toCountTable("aabbbccccc")
a.del('b')
assert a == toCountTable("aaccccc")
a.del('b')
assert a == toCountTable("aaccccc")
a.del('c')
assert a == toCountTable("aa")
```

```nim
let a = {'a': 5, 'b': 9}.toOrderedTable
doAssert a.getOrDefault('a') == 5
doAssert a.getOrDefault('z') == 0
```

```nim
let a = {'a': 5, 'b': 9}.toOrderedTable
doAssert a.getOrDefault('a', 99) == 5
doAssert a.getOrDefault('z', 99) == 99
```

```nim
let a = {'a': 5, 'b': 9}.newOrderedTable
doAssert a.getOrDefault('a') == 5
doAssert a.getOrDefault('z') == 0
```

```nim
let a = {'a': 5, 'b': 9}.newOrderedTable
doAssert a.getOrDefault('a', 99) == 5
doAssert a.getOrDefault('z', 99) == 99
```

```nim
let a = {'a': 5, 'b': 9}.toTable
doAssert a.getOrDefault('a') == 5
doAssert a.getOrDefault('z') == 0
```

```nim
let a = {'a': 5, 'b': 9}.toTable
doAssert a.getOrDefault('a', 99) == 5
doAssert a.getOrDefault('z', 99) == 99
```

```nim
let a = {'a': 5, 'b': 9}.newTable
doAssert a.getOrDefault('a') == 5
doAssert a.getOrDefault('z') == 0
```

```nim
let a = {'a': 5, 'b': 9}.newTable
doAssert a.getOrDefault('a', 99) == 5
doAssert a.getOrDefault('z', 99) == 99
```

```nim
let a = {'a': 5, 'b': 9}.toOrderedTable
doAssert a.hasKey('a') == true
doAssert a.hasKey('z') == false
```

```nim
let a = {'a': 5, 'b': 9}.newOrderedTable
doAssert a.hasKey('a') == true
doAssert a.hasKey('z') == false
```

```nim
let a = {'a': 5, 'b': 9}.toTable
doAssert a.hasKey('a') == true
doAssert a.hasKey('z') == false
```

```nim
let a = {'a': 5, 'b': 9}.newTable
doAssert a.hasKey('a') == true
doAssert a.hasKey('z') == false
```

```nim
var a = {'a': 5, 'b': 9}.newOrderedTable
if a.hasKeyOrPut('a', 50):
  a['a'] = 99
if a.hasKeyOrPut('z', 50):
  a['z'] = 99
doAssert a == {'a': 99, 'b': 9, 'z': 50}.newOrderedTable
```

```nim
var a = {'a': 5, 'b': 9}.newTable
if a.hasKeyOrPut('a', 50):
  a['a'] = 99
if a.hasKeyOrPut('z', 50):
  a['z'] = 99
doAssert a == {'a': 99, 'b': 9, 'z': 50}.newTable
```

```nim
var a = {'a': 5, 'b': 9}.toOrderedTable
if a.hasKeyOrPut('a', 50):
  a['a'] = 99
if a.hasKeyOrPut('z', 50):
  a['z'] = 99
doAssert a == {'a': 99, 'b': 9, 'z': 50}.toOrderedTable
```

```nim
var a = {'a': 5, 'b': 9}.toTable
if a.hasKeyOrPut('a', 50):
  a['a'] = 99
if a.hasKeyOrPut('z', 50):
  a['z'] = 99
doAssert a == {'a': 99, 'b': 9, 'z': 50}.toTable
```

```nim
let
  a = initOrderedTable[int, string]()
  b = initOrderedTable[char, seq[int]]()
```

```nim
let
  a = initTable[int, string]()
  b = initTable[char, seq[int]]()
```

```nim
let a = {'a': 5, 'b': 9}.toOrderedTable
doAssert len(a) == 2
```

```nim
let a = {'a': 5, 'b': 9}.newOrderedTable
doAssert len(a) == 2
```

```nim
let a = {'a': 5, 'b': 9}.toTable
doAssert len(a) == 2
```

```nim
let a = {'a': 5, 'b': 9}.newTable
doAssert len(a) == 2
```

```nim
let
  a = newCountTable("aaabbc")
  b = newCountTable("bcc")
a.merge(b)
doAssert a == newCountTable("aaabbbccc")
```

```nim
var a = toCountTable("aaabbc")
let b = toCountTable("bcc")
a.merge(b)
doAssert a == toCountTable("aaabbbccc")
```

```nim
var a = {'a': 5}.toOrderedTable
doAssert a.mgetOrPut('a') == 5
a.mgetOrPut('z').inc
doAssert a == {'a': 5, 'z': 1}.toOrderedTable
```

```nim
var a = {'a': 5, 'b': 9}.newOrderedTable
doAssert a.mgetOrPut('a', 99) == 5
doAssert a.mgetOrPut('z', 99) == 99
doAssert a == {'a': 5, 'b': 9, 'z': 99}.newOrderedTable
```

```nim
var a = {'a': 5}.newTable
doAssert a.mgetOrPut('a') == 5
a.mgetOrPut('z').inc
doAssert a == {'a': 5, 'z': 1}.newTable
```

```nim
var a = {'a': 5, 'b': 9}.newTable
doAssert a.mgetOrPut('a', 99) == 5
doAssert a.mgetOrPut('z', 99) == 99
doAssert a == {'a': 5, 'b': 9, 'z': 99}.newTable

# An example of accidentally creating a copy
var t = newTable[int, seq[int]]()
# In this example, we expect t[10] to be modified,
# but it is not.
var copiedSeq = t.mgetOrPut(10, @[10])
copiedSeq.add(20)
doAssert t[10] == @[10]
# Correct
t.mgetOrPut(25, @[25]).add(35)
doAssert t[25] == @[25, 35]
```

```nim
var a = {'a': 5}.toOrderedTable
doAssert a.mgetOrPut('a') == 5
a.mgetOrPut('z').inc
doAssert a == {'a': 5, 'z': 1}.toOrderedTable
```

```nim
var a = {'a': 5, 'b': 9}.toOrderedTable
doAssert a.mgetOrPut('a', 99) == 5
doAssert a.mgetOrPut('z', 99) == 99
doAssert a == {'a': 5, 'b': 9, 'z': 99}.toOrderedTable
```

```nim
var a = {'a': 5}.newTable
doAssert a.mgetOrPut('a') == 5
a.mgetOrPut('z').inc
doAssert a == {'a': 5, 'z': 1}.newTable
```

```nim
var a = {'a': 5, 'b': 9}.toTable
doAssert a.mgetOrPut('a', 99) == 5
doAssert a.mgetOrPut('z', 99) == 99
doAssert a == {'a': 5, 'b': 9, 'z': 99}.toTable

# An example of accidentally creating a copy
var t = initTable[int, seq[int]]()
# In this example, we expect t[10] to be modified,
# but it is not.
var copiedSeq = t.mgetOrPut(10, @[10])
copiedSeq.add(20)
doAssert t[10] == @[10]
# Correct
t.mgetOrPut(25, @[25]).add(35)
doAssert t[25] == @[25, 35]
```

```nim
let
  a = newOrderedTable[int, string]()
  b = newOrderedTable[char, seq[int]]()
```

```nim
let a = [('a', 5), ('b', 9)]
let b = newOrderedTable(a)
assert b == {'a': 5, 'b': 9}.newOrderedTable
```

```nim
let
  a = newTable[int, string]()
  b = newTable[char, seq[int]]()
```

```nim
let a = [('a', 5), ('b', 9)]
let b = newTable(a)
assert b == {'a': 5, 'b': 9}.newTable
```

```nim
var
  a = {'c': 5, 'b': 9, 'a': 13}.newOrderedTable
  i: int
doAssert a.pop('b', i) == true
doAssert a == {'c': 5, 'a': 13}.newOrderedTable
doAssert i == 9
i = 0
doAssert a.pop('z', i) == false
doAssert a == {'c': 5, 'a': 13}.newOrderedTable
doAssert i == 0
```

```nim
var
  a = {'a': 5, 'b': 9, 'c': 13}.newTable
  i: int
doAssert a.pop('b', i) == true
doAssert a == {'a': 5, 'c': 13}.newTable
doAssert i == 9
i = 0
doAssert a.pop('z', i) == false
doAssert a == {'a': 5, 'c': 13}.newTable
doAssert i == 0
```

```nim
var
  a = {'c': 5, 'b': 9, 'a': 13}.toOrderedTable
  i: int
doAssert a.pop('b', i) == true
doAssert a == {'c': 5, 'a': 13}.toOrderedTable
doAssert i == 9
i = 0
doAssert a.pop('z', i) == false
doAssert a == {'c': 5, 'a': 13}.toOrderedTable
doAssert i == 0
```

```nim
var
  a = {'a': 5, 'b': 9, 'c': 13}.toTable
  i: int
doAssert a.pop('b', i) == true
doAssert a == {'a': 5, 'c': 13}.toTable
doAssert i == 9
i = 0
doAssert a.pop('z', i) == false
doAssert a == {'a': 5, 'c': 13}.toTable
doAssert i == 0
```

```nim
var a = toCountTable("aabbbccccc")
var i = 0
assert a.pop('b', i)
assert i == 3
i = 99
assert not a.pop('b', i)
assert i == 99
```

```nim
import std/[algorithm]
var a = newOrderedTable[char, int]()
for i, c in "cab":
  a[c] = 10*i
doAssert a == {'c': 0, 'a': 10, 'b': 20}.newOrderedTable
a.sort(system.cmp)
doAssert a == {'a': 10, 'b': 20, 'c': 0}.newOrderedTable
a.sort(system.cmp, order = SortOrder.Descending)
doAssert a == {'c': 0, 'b': 20, 'a': 10}.newOrderedTable
```

```nim
import std/[algorithm]
var a = initOrderedTable[char, int]()
for i, c in "cab":
  a[c] = 10*i
doAssert a == {'c': 0, 'a': 10, 'b': 20}.toOrderedTable
a.sort(system.cmp)
doAssert a == {'a': 10, 'b': 20, 'c': 0}.toOrderedTable
a.sort(system.cmp, order = SortOrder.Descending)
doAssert a == {'c': 0, 'b': 20, 'a': 10}.toOrderedTable
```

```nim
import std/[algorithm, sequtils]
var a = toCountTable("abracadabra")
doAssert a == "aaaaabbrrcd".toCountTable
a.sort()
doAssert toSeq(a.values) == @[5, 2, 2, 1, 1]
a.sort(SortOrder.Ascending)
doAssert toSeq(a.values) == @[1, 1, 2, 2, 5]
```

```nim
let a = [('a', 5), ('b', 9)]
let b = toOrderedTable(a)
assert b == {'a': 5, 'b': 9}.toOrderedTable
```

```nim
let a = [('a', 5), ('b', 9)]
let b = toTable(a)
assert b == {'a': 5, 'b': 9}.toTable
```

```nim
import std/[sequtils, algorithm]

var a = {'a': 3, 'b': 5}.toTable
for i in 1..3: a.add('z', 10*i)
doAssert toSeq(a.pairs).sorted == @[('a', 3), ('b', 5), ('z', 10), ('z', 20), ('z', 30)]
doAssert sorted(toSeq(a.allValues('z'))) == @[10, 20, 30]
```

```nim
var a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.toOrderedTable
for k in a.keys:
  a[k].add(99)
doAssert a == {'o': @[1, 5, 7, 9, 99],
               'e': @[2, 4, 6, 8, 99]}.toOrderedTable
```

```nim
let a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.newOrderedTable
for k in a.keys:
  a[k].add(99)
doAssert a == {'o': @[1, 5, 7, 9, 99], 'e': @[2, 4, 6, 8,
    99]}.newOrderedTable
```

```nim
var a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.toTable
for k in a.keys:
  a[k].add(99)
doAssert a == {'e': @[2, 4, 6, 8, 99], 'o': @[1, 5, 7, 9, 99]}.toTable
```

```nim
let a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.newTable
for k in a.keys:
  a[k].add(99)
doAssert a == {'e': @[2, 4, 6, 8, 99], 'o': @[1, 5, 7, 9, 99]}.newTable
```

```nim
var a = toCountTable("abracadabra")
for k in keys(a):
  a[k] = 2
doAssert a == toCountTable("aabbccddrr")
```

```nim
let a = newCountTable("abracadabra")
for k in keys(a):
  a[k] = 2
doAssert a == newCountTable("aabbccddrr")
```

```nim
let a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.newOrderedTable
for k, v in a.mpairs:
  v.add(v[0] + 10)
doAssert a == {'o': @[1, 5, 7, 9, 11],
               'e': @[2, 4, 6, 8, 12]}.newOrderedTable
```

```nim
let a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.newTable
for k, v in a.mpairs:
  v.add(v[0] + 10)
doAssert a == {'e': @[2, 4, 6, 8, 12], 'o': @[1, 5, 7, 9, 11]}.newTable
```

```nim
var a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.toOrderedTable
for k, v in a.mpairs:
  v.add(v[0] + 10)
doAssert a == {'o': @[1, 5, 7, 9, 11],
               'e': @[2, 4, 6, 8, 12]}.toOrderedTable
```

```nim
var a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.toTable
for k, v in a.mpairs:
  v.add(v[0] + 10)
doAssert a == {'e': @[2, 4, 6, 8, 12], 'o': @[1, 5, 7, 9, 11]}.toTable
```

```nim
let a = newCountTable("abracadabra")
for k, v in mpairs(a):
  v = 2
doAssert a == newCountTable("aabbccddrr")
```

```nim
var a = toCountTable("abracadabra")
for k, v in mpairs(a):
  v = 2
doAssert a == toCountTable("aabbccddrr")
```

```nim
let a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.newOrderedTable
for v in a.mvalues:
  v.add(99)
doAssert a == {'o': @[1, 5, 7, 9, 99],
               'e': @[2, 4, 6, 8, 99]}.newOrderedTable
```

```nim
let a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.newTable
for v in a.mvalues:
  v.add(99)
doAssert a == {'e': @[2, 4, 6, 8, 99], 'o': @[1, 5, 7, 9, 99]}.newTable
```

```nim
var a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.toOrderedTable
for v in a.mvalues:
  v.add(99)
doAssert a == {'o': @[1, 5, 7, 9, 99],
               'e': @[2, 4, 6, 8, 99]}.toOrderedTable
```

```nim
var a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.toTable
for v in a.mvalues:
  v.add(99)
doAssert a == {'e': @[2, 4, 6, 8, 99], 'o': @[1, 5, 7, 9, 99]}.toTable
```

```nim
var a = newCountTable("abracadabra")
for v in mvalues(a):
  v = 2
doAssert a == newCountTable("aabbccddrr")
```

```nim
var a = toCountTable("abracadabra")
for v in mvalues(a):
  v = 2
doAssert a == toCountTable("aabbccddrr")
```

```nim
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

```nim
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

```nim
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

```nim
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

```nim
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

```nim
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

```nim
let a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.toOrderedTable
for v in a.values:
  doAssert v.len == 4
```

```nim
let a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.newOrderedTable
for v in a.values:
  doAssert v.len == 4
```

```nim
let a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.toTable
for v in a.values:
  doAssert v.len == 4
```

```nim
let a = {
  'o': @[1, 5, 7, 9],
  'e': @[2, 4, 6, 8]
  }.newTable
for v in a.values:
  doAssert v.len == 4
```

```nim
let a = toCountTable("abracadabra")
for v in values(a):
  assert v < 10
```

```nim
let a = newCountTable("abracadabra")
for v in values(a):
  assert v < 10
```

```nim
type
  User = object
    name: string

proc `=copy`(dest: var User, source: User) {.error.}

proc exec(t: Table[int, User]) =
  t.withValue(1, value):
    assert value.name == "Hello"
  do:
    doAssert false

  var executedElseBranch = false
  t.withValue(521, value):
    doAssert false
  do:
    executedElseBranch = true
  assert executedElseBranch

var t = initTable[int, User]()
t[1] = User(name: "Hello")
t.exec()
```

```nim
type
  User = object
    name: string

proc `=copy`(dest: var User, source: User) {.error.}

proc exec(t: Table[int, User]) =
  t.withValue(1, value):
    assert value.name == "Hello"

  t.withValue(521, value):
    doAssert false

var t = initTable[int, User]()
t[1] = User(name: "Hello")
t.exec()
```

```nim
type
  User = object
    name: string
    uid: int

var t = initTable[int, User]()
let u = User(name: "Hello", uid: 99)
t[1] = u

t.withValue(1, value):
  # block is executed only if `key` in `t`
  value.name = "Nim"
  value.uid = 1314

t.withValue(521, value):
  doAssert false
do:
  # block is executed when `key` not in `t`
  t[1314] = User(name: "exist", uid: 521)

assert t[1].name == "Nim"
assert t[1].uid == 1314
assert t[1314].name == "exist"
assert t[1314].uid == 521
```

```nim
type
  User = object
    name: string
    uid: int

var t = initTable[int, User]()
let u = User(name: "Hello", uid: 99)
t[1] = u

t.withValue(1, value):
  # block is executed only if `key` in `t`
  value.name = "Nim"
  value.uid = 1314

t.withValue(2, value):
  value.name = "No"
  value.uid = 521

assert t[1].name == "Nim"
assert t[1].uid == 1314
```


[Next](tables_2.md)
