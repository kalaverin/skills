---
source_hash: bd24f2d04fe269cf
source_path: lib/pure/random.nim
---

# random

[ref: #module-random]

Nim's standard random number generator (RNG).

Its implementation is based on the xoroshiro128+ (xor/rotate/shift/rotate) library.

* More information: <https://xoroshiro.di.unimi.it>
* C implementation: <https://xoroshiro.di.unimi.it/xoroshiro128plus.c>

**Do not use this module for cryptographic purposes!**

# [Basic usage](#basic-usage)

These examples all use the default RNG. The [Rand type](#Rand) represents the state of an RNG. For convenience, this module contains a default Rand state that corresponds to the default RNG. Most procs in this module which do not take in a Rand parameter, including those called in the above examples, use the default generator. Those procs are **not** thread-safe.

Note that the default generator always starts in the same state. The [randomize proc](#randomize) can be called to initialize the default generator with a seed based on the current time, and it only needs to be called once before the first usage of procs from this module. If randomize is not called, the default generator will always produce the same results.

RNGs that are independent of the default one can be created with the [initRand proc](#initRand,int64).

Again, it is important to remember that this module must **not** be used for cryptographic applications.

# [See also](#see-also)

* [std/sysrand module](sysrand.html) for a cryptographically secure pseudorandom number generator
* [math module](math.html) for basic math routines
* [stats module](stats.html) for statistical analysis
* [list of cryptographic and hashing modules](lib.html#pure-libraries-hashing) in the standard library

## Examples

```nim
import std/random
# Call randomize() once to initialize the default random number generator.
# If this is not called, the same results will occur every time these
# examples are run.
randomize()

# Pick a number in 0..100.
let num = rand(100)
doAssert num in 0..100

# Roll a six-sided die.
let roll = rand(1..6)
doAssert roll in 1..6

# Pick a marble from a bag.
let marbles = ["red", "blue", "green", "yellow", "purple"]
let pick = sample(marbles)
doAssert pick in marbles

# Shuffle some cards.
var cards = ["Ace", "King", "Queen", "Jack", "Ten"]
shuffle(cards)
doAssert cards.len == 5
```

```nim
from std/times import getTime, toUnix, nanosecond

var r1 = initRand(123)
let now = getTime()
var r2 = initRand(now.toUnix * 1_000_000_000 + now.nanosecond)
```

```nim
var r = initRand(2019)
assert r.next() == 13223559681708962501'u64 # implementation defined
assert r.next() == 7229677234260823147'u64 # ditto
```

```nim
randomize(234)
let f = rand(1.0) # 8.717181376738381e-07
```

```nim
randomize(123)
assert [rand(100), rand(100)] == [96, 63] # implementation defined
```

```nim
var r = initRand(123)
if false:
  assert r.rand(100) == 96 # implementation defined
```

```nim
var r = initRand(234)
let f = r.rand(1.0) # 8.717181376738381e-07
```

```nim
var r = initRand(345)
assert r.rand(1..5) <= 5
assert r.rand(-1.1 .. 1.2) >= -1.1
```

```nim
randomize(345)
assert rand(1..6) <= 6
```

```nim
randomize(567)
type E = enum a, b, c, d

assert rand(E) in a..d
assert rand(char) in low(char)..high(char)
assert rand(int8) in low(int8)..high(int8)
assert rand(uint32) in low(uint32)..high(uint32)
assert rand(range[1..16]) in 1..16
```

```nim
from std/times import getTime, toUnix, nanosecond

randomize(123)

let now = getTime()
randomize(now.toUnix * 1_000_000_000 + now.nanosecond)
```

```nim
from std/math import cumsummed

let marbles = ["red", "blue", "green", "yellow", "purple"]
let count = [1, 6, 8, 3, 4]
let cdf = count.cumsummed
randomize(789)
assert sample(marbles, cdf) in marbles
```

```nim
from std/math import cumsummed

let marbles = ["red", "blue", "green", "yellow", "purple"]
let count = [1, 6, 8, 3, 4]
let cdf = count.cumsummed
var r = initRand(789)
assert r.sample(marbles, cdf) in marbles
```

```nim
let marbles = ["red", "blue", "green", "yellow", "purple"]
randomize(456)
assert sample(marbles) in marbles
```

```nim
let marbles = ["red", "blue", "green", "yellow", "purple"]
var r = initRand(456)
assert r.sample(marbles) in marbles
```

```nim
var r = initRand(987)
let s = {1, 3, 5, 7, 9}
assert r.sample(s) in s
```

```nim
randomize(987)
let s = {1, 3, 5, 7, 9}
assert sample(s) in s
```

```nim
var cards = ["Ace", "King", "Queen", "Jack", "Ten"]
var r = initRand(678)
r.shuffle(cards)
import std/algorithm
assert cards.sorted == @["Ace", "Jack", "King", "Queen", "Ten"]
```

```nim
var cards = ["Ace", "King", "Queen", "Jack", "Ten"]
randomize(678)
shuffle(cards)
import std/algorithm
assert cards.sorted == @["Ace", "Jack", "King", "Queen", "Ten"]
```

```nim
import std/random

const numbers = 100000

var
  thr: array[0..3, Thread[(Rand, int)]]
  vals: array[0..3, int]

proc randomSum(params: tuple[r: Rand, index: int]) {.thread.} =
  var r = params.r
  var s = 0 # avoid cache thrashing
  for i in 1..numbers:
    s += r.rand(0..10)
  vals[params.index] = s

var r = initRand(2019)
for i in 0..<thr.len:
  createThread(thr[i], randomSum, (r, i))
  r.skipRandomNumbers()

joinThreads(thr)

for val in vals:
  doAssert abs(val - numbers * 5) / numbers < 0.1

doAssert vals == [501737, 497901, 500683, 500157]
```

## Proc

### gauss

[ref: #symbol-gauss]

**Input:**
- `r: var Rand`
- `mu:  = 0.0`
- `sigma:  = 1.0`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a Gaussian random variate, with mean mu and standard deviation sigma using the given state.

### gauss

[ref: #symbol-gauss]

Returns a Gaussian random variate, with mean mu and standard deviation sigma.

**Input:**
- `mu:  = 0.0`
- `sigma:  = 1.0`

**Output:** `float`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a Gaussian random variate, with mean mu and standard deviation sigma.

If [randomize](#randomize) has not been called, the order of outcomes from this proc will always be the same.

This proc uses the default RNG. Thus, it is **not** thread-safe.

### initRand

[ref: #symbol-initrand]

Initializes a new [Rand](#Rand) state using the given seed.

**Input:**
- `seed: int64`

**Output:** `Rand`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Initializes a new [Rand](#Rand) state using the given seed.

Providing a specific seed will produce the same results for that seed each time.

The resulting state is independent of the default RNG's state. When seed == 0, we internally set the seed to an implementation defined non-zero value.

**See also:**

* [initRand proc](#initRand) that uses the current time
* [randomize proc](#randomize,int64) that accepts a seed for the default RNG
* [randomize proc](#randomize) that initializes the default RNG using the current time

### next

[ref: #symbol-next]

Computes a random uint64 number using the given state.

**Input:**
- `r: var Rand`

**Output:** `uint64`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Computes a random uint64 number using the given state.

**See also:**

* [rand proc](#rand,Rand,Natural) that returns an integer between zero and a given upper bound
* [rand proc](#rand,Rand,range[]) that returns a float
* [rand proc](#rand,Rand,HSlice[T: Ordinal or float or float32 or float64,T: Ordinal or float or float32 or float64]) that accepts a slice
* [rand proc](#rand,typedesc[T]) that accepts an integer or range type
* [skipRandomNumbers proc](#skipRandomNumbers,Rand)

### rand

[ref: #symbol-rand]

Returns a random integer in the range 0..max using the given state.

**Input:**
- `r: var Rand`
- `max: Natural`

**Output:** `int`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a random integer in the range 0..max using the given state.

**See also:**

* [rand proc](#rand,int) that returns an integer using the default RNG
* [rand proc](#rand,Rand,range[]) that returns a float
* [rand proc](#rand,Rand,HSlice[T: Ordinal or float or float32 or float64,T: Ordinal or float or float32 or float64]) that accepts a slice
* [rand proc](#rand,typedesc[T]) that accepts an integer or range type

### rand

[ref: #symbol-rand]

Returns a random integer in the range 0..max.

**Input:**
- `max: int`

**Output:** `int`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a random integer in the range 0..max.

If [randomize](#randomize) has not been called, the sequence of random numbers returned from this proc will always be the same.

This proc uses the default RNG. Thus, it is **not** thread-safe.

**See also:**

* [rand proc](#rand,Rand,Natural) that returns an integer using a provided state
* [rand proc](#rand,float) that returns a float
* [rand proc](#rand,HSlice[T: Ordinal or float or float32 or float64,T: Ordinal or float or float32 or float64]) that accepts a slice
* [rand proc](#rand,typedesc[T]) that accepts an integer or range type

### rand

[ref: #symbol-rand]

Returns a random floating point number in the range 0.0..max using the given state.

**Input:**
- `r: var Rand`
- `max: range[0.0 .. high(float)]`

**Output:** `float`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a random floating point number in the range 0.0..max using the given state.

**See also:**

* [rand proc](#rand,float) that returns a float using the default RNG
* [rand proc](#rand,Rand,Natural) that returns an integer
* [rand proc](#rand,Rand,HSlice[T: Ordinal or float or float32 or float64,T: Ordinal or float or float32 or float64]) that accepts a slice
* [rand proc](#rand,typedesc[T]) that accepts an integer or range type

### rand

[ref: #symbol-rand]

Returns a random floating point number in the range 0.0..max.

**Input:**
- `max: float`

**Output:** `float`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a random floating point number in the range 0.0..max.

If [randomize](#randomize) has not been called, the sequence of random numbers returned from this proc will always be the same.

This proc uses the default RNG. Thus, it is **not** thread-safe.

**See also:**

* [rand proc](#rand,Rand,range[]) that returns a float using a provided state
* [rand proc](#rand,int) that returns an integer
* [rand proc](#rand,HSlice[T: Ordinal or float or float32 or float64,T: Ordinal or float or float32 or float64]) that accepts a slice
* [rand proc](#rand,typedesc[T]) that accepts an integer or range type

### rand

[ref: #symbol-rand]

For a slice a..b, returns a value in the range a..b using the given state.

**Input:**
- `r: var Rand`
- `x: HSlice[T, T]`

**Output:** `T`
**Generic parameters:** `T`

For a slice a..b, returns a value in the range a..b using the given state.

Allowed types for T are integers, floats, and enums without holes.

**See also:**

* [rand proc](#rand,HSlice[T: Ordinal or float or float32 or float64,T: Ordinal or float or float32 or float64]) that accepts a slice and uses the default RNG
* [rand proc](#rand,Rand,Natural) that returns an integer
* [rand proc](#rand,Rand,range[]) that returns a float
* [rand proc](#rand,typedesc[T]) that accepts an integer or range type

### rand

[ref: #symbol-rand]

For a slice a..b, returns a value in the range a..b.

**Input:**
- `x: HSlice[T, T]`

**Output:** `T`
**Generic parameters:** `T`

For a slice a..b, returns a value in the range a..b.

Allowed types for T are integers, floats, and enums without holes.

If [randomize](#randomize) has not been called, the sequence of random numbers returned from this proc will always be the same.

This proc uses the default RNG. Thus, it is **not** thread-safe.

**See also:**

* [rand proc](#rand,Rand,HSlice[T: Ordinal or float or float32 or float64,T: Ordinal or float or float32 or float64]) that accepts a slice and uses a provided state
* [rand proc](#rand,int) that returns an integer
* [rand proc](#rand,float) that returns a floating point number
* [rand proc](#rand,typedesc[T]) that accepts an integer or range type

### rand

[ref: #symbol-rand]

Returns a random Ordinal in the range low(T)..high(T).

**Input:**
- `r: var Rand`
- `t: typedesc[T]`

**Output:** `T`
**Generic parameters:** `T`, `t:type`

Returns a random Ordinal in the range low(T)..high(T).

If [randomize](#randomize) has not been called, the sequence of random numbers returned from this proc will always be the same.

**See also:**

* [rand proc](#rand,int) that returns an integer
* [rand proc](#rand,float) that returns a floating point number
* [rand proc](#rand,HSlice[T: Ordinal or float or float32 or float64,T: Ordinal or float or float32 or float64]) that accepts a slice

### rand

[ref: #symbol-rand]

Returns a random Ordinal in the range low(T)..high(T).

**Input:**
- `t: typedesc[T]`

**Output:** `T`
**Generic parameters:** `T`, `t:type`

Returns a random Ordinal in the range low(T)..high(T).

If [randomize](#randomize) has not been called, the sequence of random numbers returned from this proc will always be the same.

This proc uses the default RNG. Thus, it is **not** thread-safe.

**See also:**

* [rand proc](#rand,int) that returns an integer
* [rand proc](#rand,float) that returns a floating point number
* [rand proc](#rand,HSlice[T: Ordinal or float or float32 or float64,T: Ordinal or float or float32 or float64]) that accepts a slice

### randomize

[ref: #symbol-randomize]

Initializes the default random number generator with the given seed.

**Input:**
- `seed: int64`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Initializes the default random number generator with the given seed.

Providing a specific seed will produce the same results for that seed each time.

**See also:**

* [initRand proc](#initRand,int64) that initializes a Rand state with a given seed
* [randomize proc](#randomize) that uses the current time instead
* [initRand proc](#initRand) that initializes a Rand state using the current time

### randomize

[ref: #symbol-randomize]

Initializes the default random number generator with a seed based on random number source.

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Initializes the default random number generator with a seed based on random number source.

This proc only needs to be called once, and it should be called before the first usage of procs from this module that use the default RNG.

**Note:** Does not work for the compile-time VM.

**See also:**

* [randomize proc](#randomize,int64) that accepts a seed
* [initRand proc](#initRand) that initializes a Rand state using the current time
* [initRand proc](#initRand,int64) that initializes a Rand state with a given seed

### sample

[ref: #symbol-sample]

Returns a random element from the set s using the given state.

**Input:**
- `r: var Rand`
- `s: set[T]`

**Output:** `T`
**Generic parameters:** `T`

Returns a random element from the set s using the given state.

**See also:**

* [sample proc](#sample,set[T]) that uses the default RNG
* [sample proc](#sample,Rand,openArray[T]) for openArrays
* [sample proc](#sample,Rand,openArray[T],openArray[U]) that uses a cumulative distribution function

### sample

[ref: #symbol-sample]

Returns a random element from the set s.

**Input:**
- `s: set[T]`

**Output:** `T`
**Generic parameters:** `T`

Returns a random element from the set s.

If [randomize](#randomize) has not been called, the order of outcomes from this proc will always be the same.

This proc uses the default RNG. Thus, it is **not** thread-safe.

**See also:**

* [sample proc](#sample,Rand,set[T]) that uses a provided state
* [sample proc](#sample,openArray[T]) for openArrays
* [sample proc](#sample,openArray[T],openArray[U]) that uses a cumulative distribution function

### sample

[ref: #symbol-sample]

Returns a random element from a using the given state.

**Input:**
- `r: var Rand`
- `a: openArray[T]`

**Output:** `T`
**Generic parameters:** `T`

Returns a random element from a using the given state.

**See also:**

* [sample proc](#sample,openArray[T]) that uses the default RNG
* [sample proc](#sample,Rand,openArray[T],openArray[U]) that uses a cumulative distribution function
* [sample proc](#sample,Rand,set[T]) for sets

### sample

[ref: #symbol-sample]

Returns a random element from a.

**Input:**
- `a: openArray[T]`

**Output:** `lent T`
**Generic parameters:** `T`

Returns a random element from a.

If [randomize](#randomize) has not been called, the order of outcomes from this proc will always be the same.

This proc uses the default RNG. Thus, it is **not** thread-safe.

**See also:**

* [sample proc](#sample,Rand,openArray[T]) that uses a provided state
* [sample proc](#sample,openArray[T],openArray[U]) that uses a cumulative distribution function
* [sample proc](#sample,set[T]) for sets

### sample

[ref: #symbol-sample]

Returns an element from a using a cumulative distribution function (CDF) and the given state.

**Input:**
- `r: var Rand`
- `a: openArray[T]`
- `cdf: openArray[U]`

**Output:** `T`
**Generic parameters:** `T`, `U`

Returns an element from a using a cumulative distribution function (CDF) and the given state.

The cdf argument does not have to be normalized, and it could contain any type of elements that can be converted to a float. It must be the same length as a. Each element in cdf should be greater than or equal to the previous element.

The outcome of the [cumsum](math.html#cumsum,openArray[T]) proc and the return value of the [cumsummed](math.html#cumsummed,openArray[T]) proc, which are both in the math module, can be used as the cdf argument.

**See also:**

* [sample proc](#sample,openArray[T],openArray[U]) that also utilizes a CDF but uses the default RNG
* [sample proc](#sample,Rand,openArray[T]) that does not use a CDF
* [sample proc](#sample,Rand,set[T]) for sets

### sample

[ref: #symbol-sample]

Returns an element from a using a cumulative distribution function (CDF).

**Input:**
- `a: openArray[T]`
- `cdf: openArray[U]`

**Output:** `T`
**Generic parameters:** `T`, `U`

Returns an element from a using a cumulative distribution function (CDF).

This proc works similarly to [sample](#sample,Rand,openArray[T],openArray[U]). See that proc's documentation for more details.

If [randomize](#randomize) has not been called, the order of outcomes from this proc will always be the same.

This proc uses the default RNG. Thus, it is **not** thread-safe.

**See also:**

* [sample proc](#sample,Rand,openArray[T],openArray[U]) that also utilizes a CDF but uses a provided state
* [sample proc](#sample,openArray[T]) that does not use a CDF
* [sample proc](#sample,set[T]) for sets

### shuffle

[ref: #symbol-shuffle]

Shuffles a sequence of elements in-place using the given state.

**Input:**
- `r: var Rand`
- `x: var openArray[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Shuffles a sequence of elements in-place using the given state.

**See also:**

* [shuffle proc](#shuffle,openArray[T]) that uses the default RNG

### shuffle

[ref: #symbol-shuffle]

Shuffles a sequence of elements in-place.

**Input:**
- `x: var openArray[T]`

**Output:** *(none)*
**Generic parameters:** `T`

Shuffles a sequence of elements in-place.

If [randomize](#randomize) has not been called, the order of outcomes from this proc will always be the same.

This proc uses the default RNG. Thus, it is **not** thread-safe.

**See also:**

* [shuffle proc](#shuffle,Rand,openArray[T]) that uses a provided state

### skipRandomNumbers

[ref: #symbol-skiprandomnumbers]

The jump function for the generator.

**Input:**
- `s: var Rand`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The jump function for the generator.

This proc is equivalent to 2^64 calls to [next](#next,Rand), and it can be used to generate 2^64 non-overlapping subsequences for parallel computations.

When multiple threads are generating random numbers, each thread must own the [Rand](#Rand) state it is using so that the thread can safely obtain random numbers. However, if each thread creates its own Rand state, the subsequences of random numbers that each thread generates may overlap, even if the provided seeds are unique. This is more likely to happen as the number of threads and amount of random numbers generated increases.

If many threads will generate random numbers concurrently, it is better to create a single Rand state and pass it to each thread. After passing the Rand state to a thread, call this proc before passing it to the next one. By using the Rand state this way, the subsequences of random numbers generated in each thread will never overlap as long as no thread generates more than 2^64 random numbers.

**See also:**

* [next proc](#next,Rand)

## Template

### randState

[ref: #symbol-randstate]

**Input:**
- *(none)*

**Output:** `untyped`
Makes the default Rand state accessible from other modules. Useful for module authors.

## Type

### Rand

[ref: #symbol-rand]

State of a random number generator.

```nim
Rand = object
```

State of a random number generator.

Create a new Rand state using the [initRand proc](#initRand,int64).

The module contains a default Rand state for convenience. It corresponds to the default RNG's state. The default Rand state always starts with the same values, but the [randomize proc](#randomize) can be used to seed the default generator with a value based on the current time.

Many procs have two variations: one that takes in a Rand parameter and another that uses the default generator. The procs that use the default generator are **not** thread-safe!
