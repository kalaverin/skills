---
source_hash: d96a429b4e2f6655
source_path: lib/std/jsbigints.nim
---

# jsbigints

[ref: #module-jsbigints]

Arbitrary precision integers.

* <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt>

## Examples

```nim
import std/jsbigints
block:
  let big1: JsBigInt = big"2147483647"
  let big2: JsBigInt = big"666"
  doAssert JsBigInt isnot int
  doAssert big1 != big2
  doAssert big1 > big2
  doAssert big1 >= big2
  doAssert big2 < big1
  doAssert big2 <= big1
  doAssert not(big1 == big2)
  let z = JsBigInt.default
  doAssert $z == "0n"
block:
  var a: seq[JsBigInt]
  a.setLen 2
  doAssert a == @[big"0", big"0"]
  doAssert a[^1] == big"0"
  var b: JsBigInt
  doAssert b == big"0"
  doAssert b == JsBigInt.default
```

```nim
doAssert $big"1024" == "1024n"
```

```nim
doAssert -1'big == 1'big - 2'big
# supports decimal, binary, octal, hex:
doAssert -12'big == big"-12"
doAssert 12'big == 12.big
doAssert 0b101'big == 0b101.big
doAssert 0o701'big == 0o701.big
doAssert 0xdeadbeaf'big == 0xdeadbeaf.big
doAssert 0xffffffffffffffff'big == (1'big shl 64'big) - 1'big
doAssert not compiles(static(12'big))
```

```nim
doAssert (big"42" * big"9") == big"378"
```

```nim
doAssert big"2" ** big"64" == big"18446744073709551616"
doAssert big"-2" ** big"3" == big"-8"
doAssert -big"2" ** big"2" == big"4" # parsed as: (-2n) ** 2n
doAssert big"0" ** big"0" == big"1" # edge case
var ok = false
try: discard big"2" ** big"-1" # raises foreign `RangeError`
except: ok = true
doAssert ok
```

```nim
var big1: JsBigInt = big"2"
big1 *= big"4"
doAssert big1 == big"8"
```

```nim
doAssert (big"9" + big"1") == big"10"
```

```nim
var big1: JsBigInt = big"1"
big1 += big"2"
doAssert big1 == big"3"
```

```nim
doAssert -(big"10101010101") == big"-10101010101"
```

```nim
doAssert (big"9" - big"1") == big"8"
```

```nim
var big1: JsBigInt = big"1"
big1 -= big"2"
doAssert big1 == big"-1"
```

```nim
var big1: JsBigInt = big"11"
big1 /= big"2"
doAssert big1 == big"5"
```

```nim
doAssert big"2" < big"9"
```

```nim
doAssert big"1" <= big"5"
```

```nim
doAssert big"42" == big"42"
```

```nim
doAssert (big"555" and big"2") == big"2"
```

```nim
doAssert big(1234567890) == big"1234567890"
doAssert 0b1111100111.big == 0o1747.big and 0o1747.big == 999.big
```

```nim
var big1: JsBigInt = big"2"
dec big1
doAssert big1 == big"1"
```

```nim
var big1: JsBigInt = big"1"
dec big1, big"2"
doAssert big1 == big"-1"
```

```nim
doAssert big"13" div big"3" == big"4"
doAssert big"-13" div big"3" == big"-4"
doAssert big"13" div big"-3" == big"-4"
doAssert big"-13" div big"-3" == big"4"
```

```nim
var big1: JsBigInt = big"1"
inc big1
doAssert big1 == big"2"
```

```nim
var big1: JsBigInt = big"1"
inc big1, big"2"
doAssert big1 == big"3"
```

```nim
doAssert big"13" mod big"3" == big"1"
doAssert big"-13" mod big"3" == big"-1"
doAssert big"13" mod big"-3" == big"1"
doAssert big"-13" mod big"-3" == big"-1"
```

```nim
doAssert (big"555" or big"2") == big"555"
```

```nim
doAssert (big"999" shl big"2") == big"3996"
```

```nim
doAssert (big"999" shr big"2") == big"249"
```

```nim
doAssert big"2147483647".toCstring(2) == "1111111111111111111111111111111".cstring
```

```nim
doAssert toNumber(big"2147483647") == 2147483647.int
```

```nim
doAssert (big("3") + big("2") ** big("66")).wrapToInt(13) == big("3")
```

```nim
doAssert (big("3") + big("2") ** big("66")).wrapToUint(66) == big("3")
```

```nim
doAssert (big"555" xor big"2") == big"553"
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `this: JsBigInt`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a string representation of JsBigInt.

### `&lt;=`

[ref: #symbol-lt]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `bool`
**Pragmas:** `importjs: "(# $1 #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `&lt;`

[ref: #symbol-lt]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `bool`
**Pragmas:** `importjs: "(# $1 #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `'big`

[ref: #symbol-big]

**Input:**
- `num: cstring`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "BigInt(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructor for JsBigInt.

### `**`

[ref: #symbol-]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "((#) $1 #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*=`

[ref: #symbol-]

**Input:**
- `x: var JsBigInt`
- `y: JsBigInt`

**Output:** *(none)*
**Pragmas:** `importjs: "([#][0][0] $1 #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `*`

[ref: #symbol-]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(# $1 #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+=`

[ref: #symbol-]

**Input:**
- `x: var JsBigInt`
- `y: JsBigInt`

**Output:** *(none)*
**Pragmas:** `importjs: "([#][0][0] $1 #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(# $1 #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `+`

[ref: #symbol-]

**Input:**
- `_: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `error: "See https://github.com/tc39/proposal-bigint/blob/master/ADVANCED.md#dont-break-asmjs"`

**Do NOT use.** <https://github.com/tc39/proposal-bigint/blob/master/ADVANCED.md#dont-break-asmjs>

### `-=`

[ref: #symbol-]

**Input:**
- `x: var JsBigInt`
- `y: JsBigInt`

**Output:** *(none)*
**Pragmas:** `importjs: "([#][0][0] $1 #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(# $1 #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `-`

[ref: #symbol-]

**Input:**
- `this: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "($1#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `/=`

[ref: #symbol-]

**Input:**
- `x: var JsBigInt`
- `y: JsBigInt`

**Output:** *(none)*
**Pragmas:** `importjs: "([#][0][0] $1 #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as x = x div y.

### `==`

[ref: #symbol-]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `bool`
**Pragmas:** `importjs: "(# == #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `and`

[ref: #symbol-and]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(# & #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `div`

[ref: #symbol-div]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(# / #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as div but for JsBigInt(uses JavaScript BigInt() / BigInt()).

### `mod`

[ref: #symbol-mod]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(# % #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Same as mod but for JsBigInt (uses JavaScript BigInt() % BigInt()).

### `or`

[ref: #symbol-or]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(# | #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shl`

[ref: #symbol-shl]

**Input:**
- `a: JsBigInt`
- `b: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(# << #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `shr`

[ref: #symbol-shr]

**Input:**
- `a: JsBigInt`
- `b: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(# >> #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `xor`

[ref: #symbol-xor]

**Input:**
- `x: JsBigInt`
- `y: JsBigInt`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(# ^ #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### big

[ref: #symbol-big]

**Input:**
- `integer: SomeInteger`

**Output:** `JsBigInt`
**Generic parameters:** `SomeInteger`

**Pragmas:** `importjs: "BigInt(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructor for JsBigInt.

### big

[ref: #symbol-big]

**Input:**
- `integer: cstring`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "BigInt(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Alias for 'big

### dec

[ref: #symbol-dec]

**Input:**
- `this: var JsBigInt`

**Output:** *(none)*
**Pragmas:** `importjs: "(--[#][0][0])"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### dec

[ref: #symbol-dec]

**Input:**
- `this: var JsBigInt`
- `amount: JsBigInt`

**Output:** *(none)*
**Pragmas:** `importjs: "([#][0][0] -= #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### high

[ref: #symbol-high]

**Input:**
- `_: typedesc[JsBigInt]`

**Output:** `JsBigInt`
**Generic parameters:** `_`gensym553648248:type`

**Pragmas:** `error: "Arbitrary precision integers do not have a known high."`

**Do NOT use.**

### inc

[ref: #symbol-inc]

**Input:**
- `this: var JsBigInt`

**Output:** *(none)*
**Pragmas:** `importjs: "(++[#][0][0])"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### inc

[ref: #symbol-inc]

**Input:**
- `this: var JsBigInt`
- `amount: JsBigInt`

**Output:** *(none)*
**Pragmas:** `importjs: "([#][0][0] += #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### low

[ref: #symbol-low]

**Input:**
- `_: typedesc[JsBigInt]`

**Output:** `JsBigInt`
**Generic parameters:** `_`gensym553648245:type`

**Pragmas:** `error: "Arbitrary precision integers do not have a known low."`

**Do NOT use.**

### toCstring

[ref: #symbol-tocstring]

Converts from JsBigInt to cstring representation.

**Input:**
- `this: JsBigInt`
- `radix: 2 .. 36`

**Output:** `cstring`
**Pragmas:** `importjs: "#.toString(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts from JsBigInt to cstring representation.

* radix Base to use for representing numeric values.

<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt/toString>

### toCstring

[ref: #symbol-tocstring]

**Input:**
- `this: JsBigInt`

**Output:** `cstring`
**Pragmas:** `importjs: "#.toString()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts from JsBigInt to cstring representation. <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt/toString>

### toNumber

[ref: #symbol-tonumber]

**Input:**
- `this: JsBigInt`

**Output:** `int`
**Pragmas:** `importjs: "Number(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Does not do any bounds check and may or may not return an inexact representation.

### wrapToInt

[ref: #symbol-wraptoint]

**Input:**
- `this: JsBigInt`
- `bits: Natural`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(() => { const i = #, b = #; return BigInt.asIntN(b, i) })()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Wraps this to a signed JsBigInt of bits bits in -2 ^ (bits - 1) .. 2 ^ (bits - 1) - 1. <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt/asIntN>

### wrapToUint

[ref: #symbol-wraptouint]

**Input:**
- `this: JsBigInt`
- `bits: Natural`

**Output:** `JsBigInt`
**Pragmas:** `importjs: "(() => { const i = #, b = #; return BigInt.asUintN(b, i) })()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Wraps this to an unsigned JsBigInt of bits bits in 0 .. 2 ^ bits - 1. <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt/asUintN>

## Type

### JsBigInt

[ref: #symbol-jsbigint]

```nim
JsBigInt = distinct JsBigIntImpl
```

Arbitrary precision integer for JavaScript target.
