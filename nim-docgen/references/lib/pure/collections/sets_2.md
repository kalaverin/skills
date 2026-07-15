---
source_hash: dd5d94abe10b6ed9
source_path: lib/pure/collections/sets.nim
---

### incl

[ref: #symbol-incl]

Includes an element key in s.

**Input:**
- `s: var OrderedSet[A]`
- `key: A`

**Output:** *(none)*
**Generic parameters:** `A`

Includes an element key in s.

This doesn't do anything if key is already in s.

See also:

* [excl proc](#excl,OrderedSet[A],A) for excluding an element
* [incl proc](#incl,HashSet[A],OrderedSet[A]) for including other set
* [containsOrIncl proc](#containsOrIncl,OrderedSet[A],A)

### incl

[ref: #symbol-incl]

Includes all elements from the OrderedSet other into HashSet s (must be declared as var).

**Input:**
- `s: var HashSet[A]`
- `other: OrderedSet[A]`

**Output:** *(none)*
**Generic parameters:** `A`

Includes all elements from the OrderedSet other into HashSet s (must be declared as var).

See also:

* [incl proc](#incl,OrderedSet[A],A) for including an element
* [containsOrIncl proc](#containsOrIncl,OrderedSet[A],A)

### init

[ref: #symbol-init]

Initializes a hash set.

**Input:**
- `s: var HashSet[A]`
- `initialSize:  = defaultInitialSize`

**Output:** *(none)*
**Generic parameters:** `A`

Initializes a hash set.

Starting from Nim v0.20, sets are initialized by default and it is not necessary to call this function explicitly.

You can call this proc on a previously initialized hash set, which will discard all its values. This might be more convenient than iterating over existing values and calling [excl()](#excl,HashSet[A],A) on them.

See also:

* [initHashSet proc](#initHashSet)
* [toHashSet proc](#toHashSet,openArray[A])

### init

[ref: #symbol-init]

Initializes an ordered hash set.

**Input:**
- `s: var OrderedSet[A]`
- `initialSize:  = defaultInitialSize`

**Output:** *(none)*
**Generic parameters:** `A`

Initializes an ordered hash set.

Starting from Nim v0.20, sets are initialized by default and it is not necessary to call this function explicitly.

You can call this proc on a previously initialized hash set, which will discard all its values. This might be more convenient than iterating over existing values and calling [excl()](#excl,HashSet[A],A) on them.

See also:

* [initOrderedSet proc](#initOrderedSet)
* [toOrderedSet proc](#toOrderedSet,openArray[A])

### initHashSet

[ref: #symbol-inithashset]

Wrapper around [init proc](#init,HashSet[A]) for initialization of hash sets.

**Input:**
- `initialSize:  = defaultInitialSize`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

Wrapper around [init proc](#init,HashSet[A]) for initialization of hash sets.

Returns an empty hash set you can assign directly in var blocks in a single line.

Starting from Nim v0.20, sets are initialized by default and it is not necessary to call this function explicitly.

See also:

* [toHashSet proc](#toHashSet,openArray[A])

### initOrderedSet

[ref: #symbol-initorderedset]

Wrapper around [init proc](#init,OrderedSet[A]) for initialization of ordered hash sets.

**Input:**
- `initialSize:  = defaultInitialSize`

**Output:** `OrderedSet[A]`
**Generic parameters:** `A`

Wrapper around [init proc](#init,OrderedSet[A]) for initialization of ordered hash sets.

Returns an empty ordered hash set you can assign directly in var blocks in a single line.

Starting from Nim v0.20, sets are initialized by default and it is not necessary to call this function explicitly.

See also:

* [toOrderedSet proc](#toOrderedSet,openArray[A])

### initSet

[ref: #symbol-initset]

**Input:**
- `initialSize:  = defaultInitialSize`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

**Pragmas:** `deprecated: "Deprecated since v0.20, use \'initHashSet\'"`

### intersection

[ref: #symbol-intersection]

Returns the intersection of the sets s1 and s2.

**Input:**
- `s1: HashSet[A]`
- `s2: HashSet[A]`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

Returns the intersection of the sets s1 and s2.

The same as [s1 \* s2](#*,HashSet[A],HashSet[A]).

The intersection of two sets is represented mathematically as *A ∩ B* and is the set of all objects that are members of s1 and s2 at the same time.

See also:

* [union proc](#union,HashSet[A],HashSet[A])
* [difference proc](#difference,HashSet[A],HashSet[A])
* [symmetricDifference proc](#symmetricDifference,HashSet[A],HashSet[A])

### isValid

[ref: #symbol-isvalid]

**Input:**
- `s: HashSet[A]`

**Output:** `bool`
**Generic parameters:** `A`

**Pragmas:** `deprecated: "Deprecated since v0.20; sets are initialized by default"`

Returns true if the set has been initialized (with [initHashSet proc](#initHashSet) or [init proc](#init,HashSet[A])).

### len

[ref: #symbol-len]

Returns the number of elements in s.

**Input:**
- `s: HashSet[A]`

**Output:** `int`
**Generic parameters:** `A`

Returns the number of elements in s.

Due to an implementation detail you can call this proc on variables which have not been initialized yet. The proc will return zero as the length then.

### len

[ref: #symbol-len]

Returns the number of elements in s.

**Input:**
- `s: OrderedSet[A]`

**Output:** `int`
**Generic parameters:** `A`

**Pragmas:** `inline`

Returns the number of elements in s.

Due to an implementation detail you can call this proc on variables which have not been initialized yet. The proc will return zero as the length then.

### map

[ref: #symbol-map]

Returns a new set after applying op proc on each of the elements of data set.

**Input:**
- `data: HashSet[A]`
- `op: proc (x: A): B {.closure.}`

**Output:** `HashSet[B]`
**Generic parameters:** `A`, `B`

**Pragmas:** `effectsOf: op`

Returns a new set after applying op proc on each of the elements of data set.

You can use this proc to transform the elements from a set.

### missingOrExcl

[ref: #symbol-missingorexcl]

Excludes key in the set s and tells if key was already missing from s.

**Input:**
- `s: var HashSet[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Excludes key in the set s and tells if key was already missing from s.

The difference with regards to the [excl proc](#excl,HashSet[A],A) is that this proc returns true if key was missing from s. The proc will return false if key was in s and it was removed during this call.

See also:

* [excl proc](#excl,HashSet[A],A) for excluding an element
* [excl proc](#excl,HashSet[A],HashSet[A]) for excluding other set
* [containsOrIncl proc](#containsOrIncl,HashSet[A],A)

### missingOrExcl

[ref: #symbol-missingorexcl]

Excludes key in the set s and tells if key was already missing from s. Efficiency: O(n).

**Input:**
- `s: var OrderedSet[A]`
- `key: A`

**Output:** `bool`
**Generic parameters:** `A`

Excludes key in the set s and tells if key was already missing from s. Efficiency: O(n).

The difference with regards to the [excl proc](#excl,OrderedSet[A],A) is that this proc returns true if key was missing from s. The proc will return false if key was in s and it was removed during this call.

See also:

* [excl proc](#excl,OrderedSet[A],A)
* [containsOrIncl proc](#containsOrIncl,OrderedSet[A],A)

### pop

[ref: #symbol-pop]

Removes and returns an arbitrary element from the set s.

**Input:**
- `s: var HashSet[A]`

**Output:** `A`
**Generic parameters:** `A`

Removes and returns an arbitrary element from the set s.

Raises KeyError if the set s is empty.

See also:

* [clear proc](#clear,HashSet[A])

### symmetricDifference

[ref: #symbol-symmetricdifference]

Returns the symmetric difference of the sets s1 and s2.

**Input:**
- `s1: HashSet[A]`
- `s2: HashSet[A]`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

Returns the symmetric difference of the sets s1 and s2.

The same as [s1 -+- s2](#-+-,HashSet[A],HashSet[A]).

The symmetric difference of two sets is represented mathematically as *A △ B* or *A ⊖ B* and is the set of all objects that are members of s1 or s2 but not both at the same time.

See also:

* [union proc](#union,HashSet[A],HashSet[A])
* [intersection proc](#intersection,HashSet[A],HashSet[A])
* [difference proc](#difference,HashSet[A],HashSet[A])

### toHashSet

[ref: #symbol-tohashset]

Creates a new hash set that contains the members of the given collection (seq, array, or string) keys.

**Input:**
- `keys: openArray[A]`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

Creates a new hash set that contains the members of the given collection (seq, array, or string) keys.

Duplicates are removed.

See also:

* [initHashSet proc](#initHashSet)

### toOrderedSet

[ref: #symbol-toorderedset]

Creates a new hash set that contains the members of the given collection (seq, array, or string) keys.

**Input:**
- `keys: openArray[A]`

**Output:** `OrderedSet[A]`
**Generic parameters:** `A`

Creates a new hash set that contains the members of the given collection (seq, array, or string) keys.

Duplicates are removed.

See also:

* [initOrderedSet proc](#initOrderedSet)

### toSet

[ref: #symbol-toset]

**Input:**
- `keys: openArray[A]`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

**Pragmas:** `deprecated: "Deprecated since v0.20, use \'toHashSet\'"`

### union

[ref: #symbol-union]

Returns the union of the sets s1 and s2.

**Input:**
- `s1: HashSet[A]`
- `s2: HashSet[A]`

**Output:** `HashSet[A]`
**Generic parameters:** `A`

Returns the union of the sets s1 and s2.

The same as [s1 + s2](#+,HashSet[A],HashSet[A]).

The union of two sets is represented mathematically as *A ∪ B* and is the set of all objects that are members of s1, s2 or both.

See also:

* [intersection proc](#intersection,HashSet[A],HashSet[A])
* [difference proc](#difference,HashSet[A],HashSet[A])
* [symmetricDifference proc](#symmetricDifference,HashSet[A],HashSet[A])

## Type

### HashSet

[ref: #symbol-hashset]

A generic hash set.

```nim
HashSet[A] {..} = object
```

A generic hash set.

Use [init proc](#init,HashSet[A]) or [initHashSet proc](#initHashSet) before calling other procs on it.

### OrderedSet

[ref: #symbol-orderedset]

A generic hash set that remembers insertion order.

```nim
OrderedSet[A] {..} = object
```

A generic hash set that remembers insertion order.

Use [init proc](#init,OrderedSet[A]) or [initOrderedSet proc](#initOrderedSet) before calling other procs on it.

### SomeSet

[ref: #symbol-someset]

```nim
SomeSet[A] = HashSet[A] | OrderedSet[A]
```

Type union representing HashSet or OrderedSet.

[Prev](sets_1.md)
