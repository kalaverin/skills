---
source_hash: f72a58e89e2e7fa9
source_path: lib/pure/cookies.nim
---

# cookies

[ref: #module-cookies]

This module implements helper procs for parsing Cookies.

## Examples

```nim
import std/strtabs
let cookieJar = parseCookies("a=1; foo=bar")
assert cookieJar["a"] == "1"
assert cookieJar["foo"] == "bar"
```

## Proc

### parseCookies

[ref: #symbol-parsecookies]

Parses cookies into a string table.

**Input:**
- `s: string`

**Output:** `StringTableRef`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses cookies into a string table.

The proc is meant to parse the Cookie header set by a client, not the "Set-Cookie" header set by servers.

### setCookie

[ref: #symbol-setcookie]

Creates a command in the format of Set-Cookie: key=value; Domain=...; ...

**Input:**
- `key: string`
- `value: string`
- `domain:  = ""`
- `path:  = ""`
- `expires:  = ""`
- `noName:  = false`
- `secure:  = false`
- `httpOnly:  = false`
- `maxAge:  = none(int)`
- `sameSite:  = SameSite.Default`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a command in the format of Set-Cookie: key=value; Domain=...; ...

**Tip:**
Cookies can be vulnerable. Consider setting secure=true, httpOnly=true and sameSite=Strict.

### setCookie

[ref: #symbol-setcookie]

**Input:**
- `key: string`
- `value: string`
- `expires: DateTime | Time`
- `domain:  = ""`
- `path:  = ""`
- `noName:  = false`
- `secure:  = false`
- `httpOnly:  = false`
- `maxAge:  = none(int)`
- `sameSite:  = SameSite.Default`

**Output:** `string`
**Generic parameters:** `expires:type`

Creates a command in the format of Set-Cookie: key=value; Domain=...; ...

## Type

### SameSite

[ref: #symbol-samesite]

```nim
SameSite {.pure.} = enum
  Default, None, Lax, Strict
```

The SameSite cookie attribute. Default means that setCookie proc will not set SameSite attribute.
