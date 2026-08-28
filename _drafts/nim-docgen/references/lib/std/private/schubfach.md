---
source_hash: 466ccf4db8f44359
source_path: lib/std/private/schubfach.nim
---

# schubfach

[ref: #module-schubfach]

Copyright 2020 Alexander Bolz

Distributed under the Boost Software License, Version 1.0. (See accompanying file LICENSE\_1\_0.txt or copy at <https://www.boost.org/LICENSE_1_0.txt>)

This file contains an implementation of the Schubfach algorithm as described in

[1] Raffaello Giulietti, "The Schubfach way to render doubles", <https://drive.google.com/open?id=1luHhyQF9zKlM8yJ1nebU0OgVYhfC6CBN>

Returns floor(x / 2^n).

Technically, right-shift of negative integers is implementation defined... Should easily be optimized into SAR (or equivalent) instruction.

Returns floor(log\_10(2^e))

```
static inline int32_t FloorLog10Pow2(int32_t e)
{
    SF_ASSERT(e >= -1500);
    SF_ASSERT(e <=  1500);
    return FloorDivPow2(e * 1262611, 22);
}
```

Returns floor(log\_10(3/4 2^e))

```
static inline int32_t FloorLog10ThreeQuartersPow2(int32_t e)
{
    SF_ASSERT(e >= -1500);
    SF_ASSERT(e <=  1500);
    return FloorDivPow2(e * 1262611 - 524031, 22);
}
```

Returns floor(log\_2(10^e))

Returns whether value is divisible by 2^e2

# ToChars

## Examples

```nim
static inline int32_t FloorLog10Pow2(int32_t e)
{
    SF_ASSERT(e >= -1500);
    SF_ASSERT(e <=  1500);
    return FloorDivPow2(e * 1262611, 22);
}
```

```nim
static inline int32_t FloorLog10ThreeQuartersPow2(int32_t e)
{
    SF_ASSERT(e >= -1500);
    SF_ASSERT(e <=  1500);
    return FloorDivPow2(e * 1262611 - 524031, 22);
}
```

## Proc

### float32ToChars

[ref: #symbol-float32tochars]

**Input:**
- `buffer: var openArray[char]`
- `v: float32`
- `forceTrailingDotZero:  = false`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `
