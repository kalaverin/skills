---
source_hash: 07adcb560454bd4d
source_path: lib/packages/docutils/dochelpers.nim
---

# dochelpers

[ref: #module-dochelpers]

Integration helpers between docgen.nim and rst.nim.

Function [toLangSymbol](#toLangSymbol) produces a signature docLink of [type](#type) in rst.nim, while [match](#match) matches it with generated, produced from PNode by docgen.rst.

## Examples

```nim
doAssert nimIdentBackticksNormalize("Foo_bar") == "Foobar"
doAssert nimIdentBackticksNormalize("FoO BAr") == "Foobar"
doAssert nimIdentBackticksNormalize("`Foo BAR`") == "Foobar"
doAssert nimIdentBackticksNormalize("` Foo BAR `") == "Foobar"
# not a valid identifier:
doAssert nimIdentBackticksNormalize("`_x_y`") == "_xy"
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `s: LangSymbol`

**Output:** `string`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### langSymbolGroup

[ref: #symbol-langsymbolgroup]

**Input:**
- `kind: string`
- `name: string`

**Output:** `LangSymbol`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

### match

[ref: #symbol-match]

**Input:**
- `generated: LangSymbol`
- `docLink: LangSymbol`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns true if generated can be a target for docLink. If generated is an overload group then only symKind and name are compared for success.

### nimIdentBackticksNormalize

[ref: #symbol-nimidentbackticksnormalize]

Normalizes the string s as a Nim identifier.

**Input:**
- `s: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Normalizes the string s as a Nim identifier.

Unlike nimIdentNormalize removes spaces and backticks.

**Warning:**
No checking (e.g. that identifiers cannot start from digits or '\_', or that number of backticks is even) is performed.

### toLangSymbol

[ref: #symbol-tolangsymbol]

Parses linkText into a more structured form using a state machine.

**Input:**
- `linkText: PRstNode`

**Output:** `LangSymbol`
**Pragmas:** `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Parses linkText into a more structured form using a state machine.

This proc is designed to allow link syntax with operators even without escaped backticks inside:

```
`proc *`_
`proc []`_
```

This proc should be kept in sync with the renderTypes proc from compiler/typesrenderer.nim.

## Type

### LangSymbol

[ref: #symbol-langsymbol]

```nim
LangSymbol = object
  symKind*: string           ## "proc", "const", "type", etc
  symTypeKind*: string       ## ""|enum|object|tuple -
                             ## valid only when `symKind == "type"`
  name*: string              ## plain symbol name without any parameters
  generics*: string          ## generic parameters (without brackets)
  isGroup*: bool             ## is LangSymbol a group with overloads?
  parametersProvided*: bool  ## to disambiguate `proc f`_ and `proc f()`_
  parameters*: seq[tuple[name: string, `type`: string]] ## name-type seq, e.g. for proc
  outType*: string           ## result type, e.g. for proc
```

symbol signature in Nim
