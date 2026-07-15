---
source_hash: ba21606c34192437
source_path: lib/pure/strmisc.nim
---

# strmisc

[ref: #module-strmisc]

This module contains various string utility routines that are uncommonly used in comparison to the ones in [strutils](strutils.html).

## Examples

```nim
doAssert expandTabs("\t", 4) == "    "
doAssert expandTabs("\tfoo\t", 4) == "    foo "
doAssert expandTabs("a\tb\n\txy\t", 3) == "a  b\n   xy "
```

```nim
doAssert partition("foo:bar:baz", ":") == ("foo", ":", "bar:baz")
doAssert partition("foo:bar:baz", ":", right = true) == ("foo:bar", ":", "baz")
doAssert partition("foobar", ":") == ("foobar", "", "")
doAssert partition("foobar", ":", right = true) == ("", "", "foobar")
```

```nim
doAssert rpartition("foo:bar:baz", ":") == ("foo:bar", ":", "baz")
doAssert rpartition("foobar", ":") == ("", "", "foobar")
```

## Proc

### expandTabs

[ref: #symbol-expandtabs]

Expands tab characters in s, replacing them by spaces.

**Input:**
- `s: string`
- `tabSize: int = 8`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Expands tab characters in s, replacing them by spaces.

The amount of inserted spaces for each tab character is the difference between the current column number and the next tab position. Tab positions occur every tabSize characters. The column number starts at 0 and is increased with every single character and inserted space, except for newline, which resets the column number back to 0.

### partition

[ref: #symbol-partition]

Splits the string at the first (if right is false) or last (if right is true) occurrence of sep into a 3-tuple.

**Input:**
- `s: string`
- `sep: string`
- `right: bool = false`

**Output:** `(string, string, string)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string at the first (if right is false) or last (if right is true) occurrence of sep into a 3-tuple.

Returns a 3-tuple of strings, (beforeSep, sep, afterSep) or (s, "", "") if sep is not found and right is false or ("", "", s) if sep is not found and right is true.

**See also:**

* [rpartition proc](#rpartition,string,string)

### rpartition

[ref: #symbol-rpartition]

Splits the string at the last occurrence of sep into a 3-tuple.

**Input:**
- `s: string`
- `sep: string`

**Output:** `(string, string, string)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits the string at the last occurrence of sep into a 3-tuple.

Returns a 3-tuple of strings, (beforeSep, sep, afterSep) or ("", "", s) if sep is not found. This is the same as partition(s, sep, right = true).

**See also:**

* [partition proc](#partition,string,string,bool)
