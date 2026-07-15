---
source_hash: a711cdcf9dca7a5f
source_path: lib/pure/unidecode/unidecode.nim
---

# unidecode

[ref: #module-unidecode]

This module is based on Python's [Unidecode](https://pypi.org/project/Unidecode/) module by Tomaz Solc, which in turn is based on the [Text::Unidecode](https://metacpan.org/pod/Text::Unidecode) Perl module by Sean M. Burke.

It provides a [unidecode proc](#unidecode,string) that does Unicode to ASCII transliterations: It finds the sequence of ASCII characters that is the closest approximation to the Unicode string.

For example, the closest to string "Äußerst" in ASCII is "Ausserst". Some information is lost in this transformation, of course, since several Unicode strings can be transformed to the same ASCII representation. So this is a strictly one-way transformation. However, a human reader will probably still be able to guess from the context, what the original string was.

This module needs the data file unidecode.dat to work: This file is embedded as a resource into your application by default. You can also define the symbol --define:noUnidecodeTable during compile time and use the [loadUnidecodeTable proc](#loadUnidecodeTable) to initialize this module.

## Examples

```nim
doAssert unidecode("北京") == "Bei Jing "
doAssert unidecode("Äußerst") == "Ausserst"
```

## Proc

### loadUnidecodeTable

[ref: #symbol-loadunidecodetable]

**Input:**
- `datafile:  = "unidecode.dat"`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Loads the datafile that [unidecode](#unidecode,string) needs to work. This is only required if the module was compiled with the --define:noUnidecodeTable switch. This needs to be called by the main thread before any thread can make a call to unidecode.

### unidecode

[ref: #symbol-unidecode]

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Finds the sequence of ASCII characters that is the closest approximation to the UTF-8 string s.
