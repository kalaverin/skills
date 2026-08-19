---
source_hash: 1a1d9434a7082dc8
source_path: lib/std/effecttraits.nim
---

# effecttraits

[ref: #module-effecttraits]

This module provides access to the inferred .raises effects for Nim's macro system. **Since**: Version 1.4.

One can test for the existence of this standard module via defined(nimHasEffectTraitsModule).

## Proc

### getForbidsList

[ref: #symbol-getforbidslist]

**Input:**
- `fn: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Extracts the .forbids list of the func/proc/etc fn. fn has to be a resolved symbol of kind nnkSym. This implies that the macro that calls this proc should accept typed arguments and not untyped arguments.

### getRaisesList

[ref: #symbol-getraiseslist]

**Input:**
- `fn: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Extracts the .raises list of the func/proc/etc fn. fn has to be a resolved symbol of kind nnkSym. This implies that the macro that calls this proc should accept typed arguments and not untyped arguments.

### getTagsList

[ref: #symbol-gettagslist]

**Input:**
- `fn: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Extracts the .tags list of the func/proc/etc fn. fn has to be a resolved symbol of kind nnkSym. This implies that the macro that calls this proc should accept typed arguments and not untyped arguments.

### hasNoSideEffects

[ref: #symbol-hasnosideeffects]

**Input:**
- `fn: NimNode`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Return true if the func/proc/etc fn has noSideEffect. fn has to be a resolved symbol of kind nnkSym. This implies that the macro that calls this proc should accept typed arguments and not untyped arguments.

### isGcSafe

[ref: #symbol-isgcsafe]

**Input:**
- `fn: NimNode`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Return true if the func/proc/etc fn is gcsafe. fn has to be a resolved symbol of kind nnkSym. This implies that the macro that calls this proc should accept typed arguments and not untyped arguments.
