---
source_hash: f944b3113bdbd1de
source_path: lib/pure/hashes.nim
---

# hashes

[ref: #module-hashes]

This module implements efficient computations of hash values for diverse Nim types. All the procs are based on these two building blocks:

* [!& proc](#!&,Hash,int) used to start or mix a hash value, and
* [!$ proc](#!$,Hash) used to finish the hash value.

If you want to implement hash procs for your custom types, you will end up writing the following kind of skeleton of code:

If your custom types contain fields for which there already is a hash proc, you can simply hash together the hash values of the individual fields:

**Important:**
Use -d:nimPreviewHashRef to enable hashing refs. It is expected that this behavior becomes the new default in upcoming versions.

**Note:**
If the type has a == operator, the following must hold: If two values compare equal, their hashes must also be equal.

# [See also](#see-also)

* [md5 module](md5.html) for the MD5 checksum algorithm
* [base64 module](base64.html) for a Base64 encoder and decoder
* [sha1 module](sha1.html) for the SHA-1 checksum algorithm
* [tables module](tables.html) for hash tables

## Examples

```nim
import std/hashes
type
  Something = object
    foo: int
    bar: string

iterator items(x: Something): Hash =
  yield hash(x.foo)
  yield hash(x.bar)

proc hash(x: Something): Hash =
  ## Computes a Hash from `x`.
  var h: Hash = 0
  # Iterate over parts of `x`.
  for xAtom in x:
    # Mix the atom with the partial hash.
    h = h !& xAtom
  # Finish the hash.
  result = !$h
```

```nim
import std/hashes
type
  Something = object
    foo: int
    bar: string

proc hash(x: Something): Hash =
  ## Computes a Hash from `x`.
  var h: Hash = 0
  h = h !& hash(x.foo)
  h = h !& hash(x.bar)
  result = !$h
```

```nim
var a = "abracadabra"
doAssert hash(a, 0, 3) == hash(a, 7, 10)
```

```nim
doAssert hash(cstring"abracadabra") == hash("abracadabra")
doAssert hash(cstring"AbracadabrA") == hash("AbracadabrA")
doAssert hash(cstring"abracadabra") != hash(cstring"AbracadabrA")
```

```nim
doAssert hash("abracadabra") != hash("AbracadabrA")
```

```nim
let a = [1, 2, 5, 1, 2, 6]
doAssert hash(a, 0, 1) == hash(a, 3, 4)
```

```nim
# for `tuple|object`, `hash` must be defined for each component of `x`.
type Obj = object
  x: int
  y: string
type Obj2[T] = object
  x: int
  y: string
assert hash(Obj(x: 520, y: "Nim")) != hash(Obj(x: 520, y: "Nim2"))
# you can define custom hashes for objects (even if they're generic):
proc hash(a: Obj2): Hash = hash((a.x))
assert hash(Obj2[float](x: 520, y: "Nim")) == hash(Obj2[float](x: 520, y: "Nim2"))
```

```nim
# proc
proc fn1() = discard
const fn1b = fn1
assert hash(fn1b) == hash(fn1)

# closure
proc outer =
  var a = 0
  proc fn2() = a.inc
  assert fn2 is "closure"
  let fn2b = fn2
  assert hash(fn2b) == hash(fn2)
  assert hash(fn2) != hash(fn1)
outer()
```

```nim
var a: array[10, uint8]
assert a[0].addr.hash != a[1].addr.hash
assert cast[pointer](a[0].addr).hash == a[0].addr.hash
```

```nim
type A = ref object
  x: int
let a = A(x: 3)
let ha = a.hash
assert ha != A(x: 3).hash # A(x: 3) is a different ref object from `a`.
a.x = 4
assert ha == a.hash # the hash only depends on the address
```

```nim
# you can overload `hash` if you want to customize semantics
type A[T] = ref object
  x, y: T
proc hash(a: A): Hash = hash(a.x)
assert A[int](x: 3, y: 4).hash == A[int](x: 3, y: 5).hash
```

```nim
var a = "ABracadabRA"
doAssert hashIgnoreCase(a, 0, 3) == hashIgnoreCase(a, 7, 10)
```

```nim
doAssert hashIgnoreCase("ABRAcaDABRA") == hashIgnoreCase("abRACAdabra")
doAssert hashIgnoreCase("abcdefghi") != hash("abcdefghi")
```

```nim
var a = "ABracada_b_r_a"
doAssert hashIgnoreStyle(a, 0, 3) == hashIgnoreStyle(a, 7, a.high)
```

```nim
doAssert hashIgnoreStyle("aBr_aCa_dAB_ra") == hashIgnoreStyle("abracadabra")
doAssert hashIgnoreStyle("abcdefghi") != hash("abcdefghi")
```

## Proc

### `!$`

[ref: #symbol-]

Finishes the computation of the hash value.

**Input:**
- `h: Hash`

**Output:** `Hash`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Finishes the computation of the hash value.

This is only needed if you need to implement a hash proc for a new datatype.

### `!&amp;`

[ref: #symbol-amp]

Mixes a hash value h with val to produce a new hash value.

**Input:**
- `h: Hash`
- `val: int`

**Output:** `Hash`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Mixes a hash value h with val to produce a new hash value.

This is only needed if you need to implement a hash proc for a new datatype.

### hash

[ref: #symbol-hash]

**Input:**
- `x: T`

**Output:** `Hash`
**Generic parameters:** `T`

**Pragmas:** `inline`

Efficient hashing of integers.

### hash

[ref: #symbol-hash]

**Input:**
- `x: pointer`

**Output:** `Hash`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Efficient hash overload.

### hash

[ref: #symbol-hash]

**Input:**
- `x: ptr [T]`

**Output:** `Hash`
**Generic parameters:** `T`

**Pragmas:** `inline`

Efficient hash overload.

### hash

[ref: #symbol-hash]

Efficient hash overload.

**Input:**
- `x: ref [T]`

**Output:** `Hash`
**Generic parameters:** `T`

**Pragmas:** `inline`

Efficient hash overload.

**Important:**
Use -d:nimPreviewHashRef to enable hashing refs. It is expected that this behavior becomes the new default in upcoming versions.

### hash

[ref: #symbol-hash]

**Input:**
- `x: float`

**Output:** `Hash`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Efficient hashing of floats.

### hash

[ref: #symbol-hash]

**Input:**
- `x: openArray[A]`

**Output:** `Hash`
**Generic parameters:** `A`

### hash

[ref: #symbol-hash]

**Input:**
- `x: set[A]`

**Output:** `Hash`
**Generic parameters:** `A`

### hash

[ref: #symbol-hash]

Efficient hashing of strings.

**Input:**
- `x: string`

**Output:** `Hash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Efficient hashing of strings.

**See also:**

* [hashIgnoreStyle](#hashIgnoreStyle,string)
* [hashIgnoreCase](#hashIgnoreCase,string)

### hash

[ref: #symbol-hash]

**Input:**
- `x: cstring`

**Output:** `Hash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Efficient hashing of null-terminated strings.

### hash

[ref: #symbol-hash]

Efficient hashing of a string buffer, from starting position sPos to ending position ePos (included).

**Input:**
- `sBuf: string`
- `sPos: int`
- `ePos: int`

**Output:** `Hash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Efficient hashing of a string buffer, from starting position sPos to ending position ePos (included).

hash(myStr, 0, myStr.high) is equivalent to hash(myStr).

### hash

[ref: #symbol-hash]

**Input:**
- `x: T`

**Output:** `Hash`
**Generic parameters:** `T`

Efficient hash overload.

### hash

[ref: #symbol-hash]

Efficient hashing of portions of arrays and sequences, from starting position sPos to ending position ePos (included). There must be a hash proc defined for the element type A.

**Input:**
- `aBuf: openArray[A]`
- `sPos: int`
- `ePos: int`

**Output:** `Hash`
**Generic parameters:** `A`

Efficient hashing of portions of arrays and sequences, from starting position sPos to ending position ePos (included). There must be a hash proc defined for the element type A.

hash(myBuf, 0, myBuf.high) is equivalent to hash(myBuf).

### hashData

[ref: #symbol-hashdata]

**Input:**
- `data: pointer`
- `size: int`

**Output:** `Hash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Hashes an array of bytes of size size.

### hashIdentity

[ref: #symbol-hashidentity]

**Input:**
- `x: T`

**Output:** `Hash`
**Generic parameters:** `T`

**Pragmas:** `inline`

The identity hash, i.e. hashIdentity(x) = x.

### hashIgnoreCase

[ref: #symbol-hashignorecase]

Efficient hashing of strings; case is ignored.

**Input:**
- `x: string`

**Output:** `Hash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Efficient hashing of strings; case is ignored.

**Note:** This uses a different hashing algorithm than hash(string).

**See also:**

* [hashIgnoreStyle](#hashIgnoreStyle,string)

### hashIgnoreCase

[ref: #symbol-hashignorecase]

Efficient hashing of a string buffer, from starting position sPos to ending position ePos (included); case is ignored.

**Input:**
- `sBuf: string`
- `sPos: int`
- `ePos: int`

**Output:** `Hash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Efficient hashing of a string buffer, from starting position sPos to ending position ePos (included); case is ignored.

**Note:** This uses a different hashing algorithm than hash(string).

hashIgnoreCase(myBuf, 0, myBuf.high) is equivalent to hashIgnoreCase(myBuf).

### hashIgnoreStyle

[ref: #symbol-hashignorestyle]

Efficient hashing of strings; style is ignored.

**Input:**
- `x: string`

**Output:** `Hash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Efficient hashing of strings; style is ignored.

**Note:** This uses a different hashing algorithm than hash(string).

**See also:**

* [hashIgnoreCase](#hashIgnoreCase,string)

### hashIgnoreStyle

[ref: #symbol-hashignorestyle]

Efficient hashing of a string buffer, from starting position sPos to ending position ePos (included); style is ignored.

**Input:**
- `sBuf: string`
- `sPos: int`
- `ePos: int`

**Output:** `Hash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Efficient hashing of a string buffer, from starting position sPos to ending position ePos (included); style is ignored.

**Note:** This uses a different hashing algorithm than hash(string).

hashIgnoreStyle(myBuf, 0, myBuf.high) is equivalent to hashIgnoreStyle(myBuf).

### hashWangYi1

[ref: #symbol-hashwangyi1]

Wang Yi's hash\_v1 for 64-bit ints (see <https://github.com/rurban/smhasher> for more details). This passed all scrambling tests in Spring 2019 and is simple.

**Input:**
- `x: int64 | uint64 | Hash`

**Output:** `Hash`
**Generic parameters:** `x:type`

**Pragmas:** `inline`

Wang Yi's hash\_v1 for 64-bit ints (see <https://github.com/rurban/smhasher> for more details). This passed all scrambling tests in Spring 2019 and is simple.

**Note:** It's ok to define proc(x: int16): Hash = hashWangYi1(Hash(x)).

## Type

### Hash

[ref: #symbol-hash]

```nim
Hash = int
```

A hash value. Hash tables using these values should always have a size of a power of two so they can use the and operator instead of mod for truncation of the hash value.
