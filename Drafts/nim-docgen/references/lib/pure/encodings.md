---
source_hash: 6e858aecca4cf852
source_path: lib/pure/encodings.nim
---

# encodings

[ref: #module-encodings]

Routines for converting between different character encodings. On UNIX, this uses the iconv library, on Windows the Windows API.

The following example shows how to change character encodings.

The example below uses a reuseable EncodingConverter object which is created by open with destEncoding and srcEncoding specified. You can use convert on this object multiple times.

## Examples

```nim
import std/encodings
when defined(windows):
  let
    orig = "öäüß"
    # convert `orig` from "UTF-8" to "CP1252"
    cp1252 = convert(orig, "CP1252", "UTF-8")
    # convert `cp1252` from "CP1252" to "ibm850"
    ibm850 = convert(cp1252, "ibm850", "CP1252")
    current = getCurrentEncoding()
  assert orig == "\195\182\195\164\195\188\195\159"
  assert ibm850 == "\148\132\129\225"
  assert convert(ibm850, current, "ibm850") == orig
```

```nim
import std/encodings
when defined(windows):
  var fromGB2312 = open("utf-8", "gb2312")
  let first = "\203\173\197\194\163\191\210\187" &
      "\203\242\209\204\211\234\200\206\198\189\201\250"
  assert fromGB2312.convert(first) == "谁怕？一蓑烟雨任平生"

  let second = "\211\208\176\215\205\183\200\231" &
      "\208\194\163\172\199\227\184\199\200\231\185\202"
  assert fromGB2312.convert(second) == "有白头如新，倾盖如故"
```

## Proc

### close

[ref: #symbol-close]

**Input:**
- `c: EncodingConverter`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Frees the resources the converter c holds.

### convert

[ref: #symbol-convert]

Converts s to destEncoding that was given to the converter c. It assumes that s is in srcEncoding.

**Input:**
- `c: EncodingConverter`
- `s: string`

**Output:** `string`
**Pragmas:** `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Converts s to destEncoding that was given to the converter c. It assumes that s is in srcEncoding.

**Warning:**
UTF-16BE and UTF-32 conversions are not supported on Windows.

### convert

[ref: #symbol-convert]

Converts s to destEncoding. It assumed that s is in srcEncoding. This opens a converter, uses it and closes it again and is thus more convenient but also likely less efficient than re-using a converter.

**Input:**
- `s: string`
- `destEncoding:  = "UTF-8"`
- `srcEncoding:  = "CP1252"`

**Output:** `string`
**Pragmas:** `raises: [EncodingError, OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: EncodingError, OSError`, `tags: `, `forbids: `

Converts s to destEncoding. It assumed that s is in srcEncoding. This opens a converter, uses it and closes it again and is thus more convenient but also likely less efficient than re-using a converter.

**Warning:**
UTF-16BE and UTF-32 conversions are not supported on Windows.

### getCurrentEncoding

[ref: #symbol-getcurrentencoding]

**Input:**
- `uiApp:  = false`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieves the current encoding. On Unix, "UTF-8" is always returned. The uiApp parameter is Windows specific. If true, the UI's code-page is returned, if false, the Console's code-page is returned.

### open

[ref: #symbol-open]

**Input:**
- `destEncoding:  = "UTF-8"`
- `srcEncoding:  = "CP1252"`

**Output:** `EncodingConverter`
**Pragmas:** `raises: [EncodingError]`, `tags: []`, `forbids: []`

**Effects:** `raises: EncodingError`, `tags: `, `forbids: `

Opens a converter that can convert from srcEncoding to destEncoding. Raises EncodingError if it cannot fulfill the request.

## Type

### EncodingConverter

[ref: #symbol-encodingconverter]

```nim
EncodingConverter = ptr ConverterObj
```

Can convert between two character sets.

### EncodingError

[ref: #symbol-encodingerror]

```nim
EncodingError = object of ValueError
```

Exception that is raised for encoding errors.
