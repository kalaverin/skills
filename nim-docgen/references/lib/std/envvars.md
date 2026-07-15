---
source_hash: 4070fac1438bbcba
source_path: lib/std/envvars.nim
---

# envvars

[ref: #module-envvars]

The std/envvars module implements environment variable handling.

## Examples

```nim
assert not existsEnv("unknownEnv")
```

```nim
assert getEnv("unknownEnv") == ""
assert getEnv("unknownEnv", "doesn't exist") == "doesn't exist"
```

## Iterator

### envPairs

[ref: #symbol-envpairs]

Iterate over all environments variables.

**Input:**
- *(none)*

**Output:** `tuple[key, value: string]`
**Pragmas:** `tags: [ReadEnvEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadEnvEffect`, `raises: `, `forbids: `

Iterate over all environments variables.

In the first component of the tuple is the name of the current variable stored, in the second its value.

Works in native backends, nodejs and vm, like the following APIs:

* [getEnv](#getEnv)
* [existsEnv](#existsEnv)
* [putEnv](#putEnv)
* [delEnv](#delEnv)

## Proc

### delEnv

[ref: #symbol-delenv]

Deletes the environment variable named key. If an error occurs, OSError is raised.

**Input:**
- `key: string`

**Output:** *(none)*
**Pragmas:** `tags: [WriteEnvEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteEnvEffect`, `raises: OSError`, `forbids: `

Deletes the environment variable named key. If an error occurs, OSError is raised.

See also:ven

* [getEnv](#getEnv)
* [existsEnv](#existsEnv)
* [putEnv](#putEnv)
* [envPairs](#envPairs)

### existsEnv

[ref: #symbol-existsenv]

Checks whether the environment variable named key exists. Returns true if it exists, false otherwise.

**Input:**
- `key: string`

**Output:** `bool`
**Pragmas:** `tags: [ReadEnvEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadEnvEffect`, `raises: `, `forbids: `

Checks whether the environment variable named key exists. Returns true if it exists, false otherwise.

See also:

* [getEnv](#getEnv)
* [putEnv](#putEnv)
* [delEnv](#delEnv)
* [envPairs](#envPairs)

### getEnv

[ref: #symbol-getenv]

Returns the value of the environment variable named key.

**Input:**
- `key: string`
- `default:  = ""`

**Output:** `string`
**Pragmas:** `tags: [ReadEnvEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: ReadEnvEffect`, `raises: `, `forbids: `

Returns the value of the environment variable named key.

If the variable does not exist, "" is returned. To distinguish whether a variable exists or it's value is just "", call [existsEnv](#existsEnv).

See also:

* [existsEnv](#existsEnv)
* [putEnv](#putEnv)
* [delEnv](#delEnv)
* [envPairs](#envPairs)

### putEnv

[ref: #symbol-putenv]

Sets the value of the environment variable named key to val. If an error occurs, OSError is raised.

**Input:**
- `key: string`
- `val: string`

**Output:** *(none)*
**Pragmas:** `tags: [WriteEnvEffect]`, `raises: [OSError]`, `forbids: []`

**Effects:** `tags: WriteEnvEffect`, `raises: OSError`, `forbids: `

Sets the value of the environment variable named key to val. If an error occurs, OSError is raised.

See also:

* [getEnv](#getEnv)
* [existsEnv](#existsEnv)
* [delEnv](#delEnv)
* [envPairs](#envPairs)

## Type

### ReadEnvEffect

[ref: #symbol-readenveffect]

```nim
ReadEnvEffect = object of ReadIOEffect
```

Effect that denotes a read from an environment variable.

### WriteEnvEffect

[ref: #symbol-writeenveffect]

```nim
WriteEnvEffect = object of WriteIOEffect
```

Effect that denotes a write to an environment variable.
