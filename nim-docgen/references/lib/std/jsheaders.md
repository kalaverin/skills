---
source_hash: 34e424ec65a1f46c
source_path: lib/std/jsheaders.nim
---

# jsheaders

[ref: #module-jsheaders]

* HTTP Headers for the JavaScript target: <https://developer.mozilla.org/en-US/docs/Web/API/Headers>

## Examples

```nim
import std/jsheaders

block:
  let header: Headers = newHeaders()
  header.add("key", "value")
  assert header.hasKey("key")
  assert header.keys() == @["key".cstring]
  assert header.values() == @["value".cstring]
  assert header["key"] == "value".cstring
  header["other"] = "another".cstring
  assert header["other"] == "another".cstring
  assert header.entries() == @[("key".cstring, "value".cstring), ("other".cstring, "another".cstring)]
  assert header.toCstring() == """[["key","value"],["other","another"]]""".cstring
  header.delete("other")
  assert header.entries() == @[("key".cstring, "value".cstring)]
  header.clear()
  assert header.entries() == @[]
  assert header.len == 0

block:
  let header: Headers = newHeaders()
  header.add("key", "a")
  header.add("key", "b")  ## Duplicated.
  header.add("key", "c")  ## Duplicated.
  assert header["key"] == "a, b, c".cstring
  header["key"] = "value".cstring
  assert header["key"] == "value".cstring

block:
  let header: Headers = newHeaders()
  header["key"] = "a"
  header["key"] = "b"  ## Overwrites.
  assert header["key"] == "b".cstring
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `self: Headers`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]=`

[ref: #symbol-]

**Input:**
- `self: Headers`
- `key: cstring`
- `value: cstring`

**Output:** *(none)*
**Pragmas:** `importjs: "#.set(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Do *not* allow duplicated keys, overwrites duplicated keys. <https://developer.mozilla.org/en-US/docs/Web/API/Headers/set>

### `[]`

[ref: #symbol-]

**Input:**
- `self: Headers`
- `key: cstring`

**Output:** `cstring`
**Pragmas:** `importjs: "#.get(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get *all* items with key from the headers, including duplicated values. <https://developer.mozilla.org/en-US/docs/Web/API/Headers/get>

### add

[ref: #symbol-add]

**Input:**
- `self: Headers`
- `key: cstring`
- `value: cstring`

**Output:** *(none)*
**Pragmas:** `importjs: "#.append(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Allows duplicated keys. <https://developer.mozilla.org/en-US/docs/Web/API/Headers/append>

### clear

[ref: #symbol-clear]

**Input:**
- `self: Headers`

**Output:** *(none)*
**Pragmas:** `importjs: "(() => { const header = #; Array.from(header.keys()).forEach((key) => header.delete(key)) })()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Convenience func to delete all items from Headers.

### delete

[ref: #symbol-delete]

<https://developer.mozilla.org/en-US/docs/Web/API/Headers/delete>

**Input:**
- `self: Headers`
- `key: cstring`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Headers/delete>

**Warning:**
Delete *all* items with key from the headers, including duplicated keys.

### entries

[ref: #symbol-entries]

**Input:**
- `self: Headers`

**Output:** `seq[tuple[key, value: cstring]]`
**Pragmas:** `importjs: "Array.from(#.$1())"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Headers/entries>

### hasKey

[ref: #symbol-haskey]

**Input:**
- `self: Headers`
- `key: cstring`

**Output:** `bool`
**Pragmas:** `importjs: "#.has(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Headers/has>

### keys

[ref: #symbol-keys]

**Input:**
- `self: Headers`

**Output:** `seq[cstring]`
**Pragmas:** `importjs: "Array.from(#.$1())"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Headers/keys>

### len

[ref: #symbol-len]

**Input:**
- `self: Headers`

**Output:** `int`
**Pragmas:** `importjs: "Array.from(#.entries()).length"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newHeaders

[ref: #symbol-newheaders]

**Input:**
- *(none)*

**Output:** `Headers`
**Pragmas:** `importjs: "new Headers()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Headers>

### toCstring

[ref: #symbol-tocstring]

**Input:**
- `self: Headers`

**Output:** `cstring`
**Pragmas:** `importjs: "JSON.stringify(Array.from(#.entries()))"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a cstring representation of Headers.

### values

[ref: #symbol-values]

**Input:**
- `self: Headers`

**Output:** `seq[cstring]`
**Pragmas:** `importjs: "Array.from(#.$1())"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/Headers/values>

## Type

### Headers

[ref: #symbol-headers]

```nim
Headers = ref object of JsRoot
```

HTTP Headers API.
