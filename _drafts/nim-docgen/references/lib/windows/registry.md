---
source_hash: 18d30d06c6f85c5b
source_path: lib/windows/registry.nim
---

# registry

[ref: #module-registry]

This module is experimental and its interface may change.

## Const

### HKEY_CURRENT_USER

[ref: #symbol-hkey-current-user]

```nim
HKEY_CURRENT_USER = 2147483649'u
```

### HKEY_LOCAL_MACHINE

[ref: #symbol-hkey-local-machine]

```nim
HKEY_LOCAL_MACHINE = 2147483650'u
```

## Proc

### getUnicodeValue

[ref: #symbol-getunicodevalue]

**Input:**
- `path: string`
- `key: string`
- `handle: HKEY`

**Output:** `string`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

### setUnicodeValue

[ref: #symbol-setunicodevalue]

**Input:**
- `path: string`
- `key: string`
- `val: string`
- `handle: HKEY`

**Output:** *(none)*
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

## Type

### HKEY

[ref: #symbol-hkey]

```nim
HKEY = uint
```
