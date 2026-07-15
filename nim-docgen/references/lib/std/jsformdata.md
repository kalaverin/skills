---
source_hash: 034b56748bf7f314
source_path: lib/std/jsformdata.nim
---

# jsformdata

[ref: #module-jsformdata]

* FormData for the JavaScript target: <https://developer.mozilla.org/en-US/docs/Web/API/FormData>

## Examples

```nim
import std/jsformdata
let data: FormData = newFormData()
data["key0"] = "value0".cstring
data.add("key1".cstring, "value1".cstring)
data.delete("key1")
assert data.hasKey("key0")
assert data["key0"] == "value0".cstring
data.clear()
assert data.len == 0
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `self: FormData`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]=`

[ref: #symbol-]

**Input:**
- `self: FormData`
- `name: cstring`
- `value: SomeNumber | bool | cstring | Blob`

**Output:** *(none)*
**Generic parameters:** `value:type`

**Pragmas:** `importjs: "#.set(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/set>

### `[]`

[ref: #symbol-]

**Input:**
- `self: FormData`
- `name: cstring`

**Output:** `cstring`
**Pragmas:** `importjs: "#.get(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/get>

### add

[ref: #symbol-add]

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/append>

**Input:**
- `self: FormData`
- `name: cstring`
- `value: SomeNumber | bool | cstring | Blob`

**Output:** *(none)*
**Generic parameters:** `value:type`

**Pragmas:** `importjs: "#.append(#, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/append>

**Hint:**
Duplicate keys are allowed and order is preserved.

### add

[ref: #symbol-add]

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/append>

**Input:**
- `self: FormData`
- `name: cstring`
- `value: SomeNumber | bool | cstring | Blob`
- `filename: cstring`

**Output:** *(none)*
**Generic parameters:** `value:type`

**Pragmas:** `importjs: "#.append(#, #, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/append>

**Hint:**
Duplicate keys are allowed and order is preserved.

### clear

[ref: #symbol-clear]

**Input:**
- `self: FormData`

**Output:** *(none)*
**Pragmas:** `importjs: "(() => { const frmdt = #; Array.from(frmdt.keys()).forEach((key) => frmdt.delete(key)) })()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Convenience func to delete all items from FormData.

### delete

[ref: #symbol-delete]

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/delete>

**Input:**
- `self: FormData`
- `name: cstring`

**Output:** *(none)*
**Pragmas:** `importjs: "#.$1(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/delete>

**Warning:**
Deletes *all items* with the same key name.

### getAll

[ref: #symbol-getall]

**Input:**
- `self: FormData`
- `name: cstring`

**Output:** `seq[cstring]`
**Pragmas:** `importjs: "#.$1(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/getAll>

### hasKey

[ref: #symbol-haskey]

**Input:**
- `self: FormData`
- `name: cstring`

**Output:** `bool`
**Pragmas:** `importjs: "#.has(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/has>

### keys

[ref: #symbol-keys]

**Input:**
- `self: FormData`

**Output:** `seq[cstring]`
**Pragmas:** `importjs: "Array.from(#.$1())"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/keys>

### len

[ref: #symbol-len]

**Input:**
- `self: FormData`

**Output:** `int`
**Pragmas:** `importjs: "Array.from(#.entries()).length"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newFormData

[ref: #symbol-newformdata]

**Input:**
- *(none)*

**Output:** `FormData`
**Pragmas:** `importjs: "new FormData()"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pairs

[ref: #symbol-pairs]

**Input:**
- `self: FormData`

**Output:** `seq[tuple[key, val: cstring]]`
**Pragmas:** `importjs: "Array.from(#.entries())"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/entries>

### put

[ref: #symbol-put]

**Input:**
- `self: FormData`
- `name: cstring`
- `value: SomeNumber | bool | cstring | Blob`
- `filename: cstring`

**Output:** *(none)*
**Generic parameters:** `value:type`

**Pragmas:** `importjs: "#.set(#, #, #)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/set>

### toCstring

[ref: #symbol-tocstring]

**Input:**
- `self: FormData`

**Output:** `cstring`
**Pragmas:** `importjs: "JSON.stringify(#)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### values

[ref: #symbol-values]

**Input:**
- `self: FormData`

**Output:** `seq[cstring]`
**Pragmas:** `importjs: "Array.from(#.$1())"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

<https://developer.mozilla.org/en-US/docs/Web/API/FormData/values>

## Type

### FormData

[ref: #symbol-formdata]

```nim
FormData = ref object of JsRoot
```

FormData API.
