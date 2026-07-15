---
source_hash: 7e0122c737f8cf45
source_path: lib/pure/strtabs.nim
---

# strtabs

[ref: #module-strtabs]

The strtabs module implements an efficient hash table that is a mapping from strings to strings. Supports a case-sensitive, case-insensitive and style-insensitive mode.String tables can be created from a table constructor:When using the style insensitive mode (modeStyleInsensitive), all letters are compared case insensitively within the ASCII range and underscores are ignored.An efficient string substitution operator [%](#%25,string,StringTableRef,set[FormatFlag]) for the string table is also provided.**See also:**

* [tables module](tables.html) for general hash tables
* [sharedtables module](sharedtables.html) for shared hash table support
* [strutils module](strutils.html) for common string functions
* [json module](json.html) for table-like structure which allows heterogeneous members

## Examples

```nim
import std/strtabs
var t = newStringTable()
t["name"] = "John"
t["city"] = "Monaco"
doAssert t.len == 2
doAssert t.hasKey "name"
doAssert "name" in t
```

```nim
import std/strtabs
var t = {"name": "John", "city": "Monaco"}.newStringTable
```

```nim
import std/strtabs
var x = newStringTable(modeStyleInsensitive)
x["first_name"] = "John"
x["LastName"] = "Doe"

doAssert x["firstName"] == "John"
doAssert x["last_name"] == "Doe"
```

```nim
import std/strtabs
var t = {"name": "John", "city": "Monaco"}.newStringTable
doAssert "${name} lives in ${city}" % t == "John lives in Monaco"
```

```nim
var t = {"name": "John", "city": "Monaco"}.newStringTable
doAssert "${name} lives in ${city}" % t == "John lives in Monaco"
```

```nim
var t = {"name": "John", "city": "Monaco"}.newStringTable
doAssert t["name"] == "John"
doAssertRaises(KeyError):
  echo t["occupation"]
```

```nim
var t = {"name": "John", "city": "Monaco"}.newStringTable
t["occupation"] = "teacher"
doAssert t.hasKey("occupation")
```

```nim
var t = {"name": "John", "city": "Monaco"}.newStringTable
clear(t, modeCaseSensitive)
doAssert len(t) == 0
doAssert "name" notin t
doAssert "city" notin t
```

```nim
var t = {"name": "John", "city": "Monaco"}.newStringTable
doAssert "name" in t
doAssert "occupation" notin t
```

```nim
var t = {"name": "John", "city": "Monaco"}.newStringTable
t.del("name")
doAssert len(t) == 1
doAssert "name" notin t
doAssert "city" in t
```

```nim
var t = {"name": "John", "city": "Monaco"}.newStringTable
doAssert t.getOrDefault("name") == "John"
doAssert t.getOrDefault("occupation") == ""
doAssert t.getOrDefault("occupation", "teacher") == "teacher"
doAssert t.getOrDefault("name", "Paul") == "John"
```

```nim
var t = {"name": "John", "city": "Monaco"}.newStringTable
doAssert t.hasKey("name")
doAssert not t.hasKey("occupation")
```

```nim
var mytab = newStringTable("key1", "val1", "key2", "val2",
                           modeCaseInsensitive)
```

```nim
var
  mytab1 = newStringTable({"key1": "val1", "key2": "val2"}, modeCaseInsensitive)
  mytab2 = newStringTable([("key3", "val3"), ("key4", "val4")])
```

## Iterator

### keys

[ref: #symbol-keys]

**Input:**
- `t: StringTableRef`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over every key in the table t.

### pairs

[ref: #symbol-pairs]

**Input:**
- `t: StringTableRef`

**Output:** `tuple[key, value: string]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over every (key, value) pair in the table t.

### values

[ref: #symbol-values]

**Input:**
- `t: StringTableRef`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over every value in the table t.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `t: StringTableRef`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nstDollar"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

The $ operator for string tables. Used internally when calling echo on a table.

### `%`

[ref: #symbol-]

**Input:**
- `f: string`
- `t: StringTableRef`
- `flags: set[FormatFlag] = {}`

**Output:** `string`
**Pragmas:** `gcsafe`, `extern: "nstFormat"`, `raises: [ValueError]`, `tags: [ReadEnvEffect]`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: ReadEnvEffect`, `forbids: `

The % operator for string tables.

### `[]=`

[ref: #symbol-]

Inserts a (key, value) pair into t.

**Input:**
- `t: StringTableRef`
- `key: string`
- `val: string`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nstPut"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Inserts a (key, value) pair into t.

See also:

* [[] proc](#[],StringTableRef,string) for retrieving a value of a key
* [del proc](#del,StringTableRef,string) for removing a key from the table

### `[]`

[ref: #symbol-]

Retrieves the location at t[key].

**Input:**
- `t: StringTableRef`
- `key: string`

**Output:** `var string`
**Pragmas:** `gcsafe`, `extern: "nstTake"`, `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Retrieves the location at t[key].

If key is not in t, the KeyError exception is raised. One can check with [hasKey proc](#hasKey,StringTableRef,string) whether the key exists.

See also:

* [getOrDefault proc](#getOrDefault,StringTableRef,string,string)
* [[]= proc](#[]=,StringTableRef,string,string) for inserting a new (key, value) pair in the table
* [hasKey proc](#hasKey,StringTableRef,string) for checking if a key is in the table

### clear

[ref: #symbol-clear]

Resets a string table to be empty again, perhaps altering the mode.

**Input:**
- `s: StringTableRef`
- `mode: StringTableMode`

**Output:** *(none)*
**Pragmas:** `gcsafe`, `extern: "nst$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Resets a string table to be empty again, perhaps altering the mode.

See also:

* [del proc](#del,StringTableRef,string) for removing a key from the table

### clear

[ref: #symbol-clear]

**Input:**
- `s: StringTableRef`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Resets a string table to be empty again without changing the mode.

### contains

[ref: #symbol-contains]

**Input:**
- `t: StringTableRef`
- `key: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Alias of [hasKey proc](#hasKey,StringTableRef,string) for use with the in operator.

### del

[ref: #symbol-del]

Removes key from t.

**Input:**
- `t: StringTableRef`
- `key: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Removes key from t.

See also:

* [clear proc](#clear,StringTableRef,StringTableMode) for resetting a table to be empty
* [[]= proc](#[]=,StringTableRef,string,string) for inserting a new (key, value) pair in the table

### getOrDefault

[ref: #symbol-getordefault]

Retrieves the location at t[key].

**Input:**
- `t: StringTableRef`
- `key: string`
- `default: string = ""`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the location at t[key].

If key is not in t, the default value is returned (if not specified, it is an empty string ("")).

See also:

* [[] proc](#[],StringTableRef,string) for retrieving a value of a key
* [hasKey proc](#hasKey,StringTableRef,string) for checking if a key is in the table
* [[]= proc](#[]=,StringTableRef,string,string) for inserting a new (key, value) pair in the table

### hasKey

[ref: #symbol-haskey]

Returns true if key is in the table t.

**Input:**
- `t: StringTableRef`
- `key: string`

**Output:** `bool`
**Pragmas:** `gcsafe`, `extern: "nst$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if key is in the table t.

See also:

* [getOrDefault proc](#getOrDefault,StringTableRef,string,string)
* [contains proc](#contains,StringTableRef,string)

### len

[ref: #symbol-len]

**Input:**
- `t: StringTableRef`

**Output:** `int`
**Pragmas:** `gcsafe`, `extern: "nst$1"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of keys in t.

### mode

[ref: #symbol-mode]

**Input:**
- `t: StringTableRef`

**Output:** `StringTableMode`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newStringTable

[ref: #symbol-newstringtable]

Creates a new empty string table.

**Input:**
- `mode: StringTableMode`

**Output:** `owned(StringTableRef)`
**Pragmas:** `gcsafe`, `extern: "nst$1"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new empty string table.

See also:

* [newStringTable(keyValuePairs) proc](#newStringTable,varargs[tuple[string,string]],StringTableMode)

### newStringTable

[ref: #symbol-newstringtable]

Creates a new string table with given key, value string pairs.

**Input:**
- `keyValuePairs: varargs[string]`
- `mode: StringTableMode`

**Output:** `owned(StringTableRef)`
**Pragmas:** `gcsafe`, `extern: "nst$1WithPairs"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new string table with given key, value string pairs.

StringTableMode must be specified.

### newStringTable

[ref: #symbol-newstringtable]

Creates a new string table with given (key, value) tuple pairs.

**Input:**
- `keyValuePairs: varargs[tuple[key, val: string]]`
- `mode: StringTableMode = modeCaseSensitive`

**Output:** `owned(StringTableRef)`
**Pragmas:** `gcsafe`, `extern: "nst$1WithTableConstr"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new string table with given (key, value) tuple pairs.

The default mode is case sensitive.

## Type

### FormatFlag

[ref: #symbol-formatflag]

```nim
FormatFlag = enum
  useEnvironment,           ## Use environment variable if the ``$key``
                             ## is not found in the table.
                             ## Does nothing when using `js` target.
  useEmpty,                 ## Use the empty string as a default, thus it
                             ## won't throw an exception if ``$key`` is not
                             ## in the table.
  useKey                     ## Do not replace ``$key`` if it is not found
                             ## in the table (or in the environment).
```

Flags for the % operator.

### StringTableMode

[ref: #symbol-stringtablemode]

```nim
StringTableMode = enum
  modeCaseSensitive,        ## the table is case sensitive
  modeCaseInsensitive,      ## the table is case insensitive
  modeStyleInsensitive       ## the table is style insensitive
```

Describes the tables operation mode.

### StringTableObj

[ref: #symbol-stringtableobj]

```nim
StringTableObj = object of RootObj
```

### StringTableRef

[ref: #symbol-stringtableref]

```nim
StringTableRef = ref StringTableObj
```
