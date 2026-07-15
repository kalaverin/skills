---
source_hash: cd6296c8fe8727db
source_path: lib/pure/oids.nim
---

# oids

[ref: #module-oids]

Nim OID support. An OID is a global ID that consists of a timestamp, a unique counter and a random value. This combination should suffice to produce a globally distributed unique ID.

This implementation calls initRand() for the first call of genOid.

## Examples

```nim
doAssert ($genOid()).len == 24
```

```nim
echo $genOid() # for example, "5fc7f546ddbbc84800006aaf"
```

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `oid: Oid`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts an OID to a string.

### `==`

[ref: #symbol-]

**Input:**
- `oid1: Oid`
- `oid2: Oid`

**Output:** `bool`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two OIDs for equality.

### generatedTime

[ref: #symbol-generatedtime]

**Input:**
- `oid: Oid`

**Output:** `Time`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the generated timestamp of the OID.

### genOid

[ref: #symbol-genoid]

**Input:**
- *(none)*

**Output:** `Oid`
**Pragmas:** `raises: []`, `tags: [TimeEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: TimeEffect`, `forbids: `

Generates a new OID.

### hash

[ref: #symbol-hash]

**Input:**
- `oid: Oid`

**Output:** `Hash`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generates the hash of an OID for use in hashtables.

### hexbyte

[ref: #symbol-hexbyte]

**Input:**
- `hex: char`

**Output:** `int`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### parseOid

[ref: #symbol-parseoid]

**Input:**
- `str: cstring`

**Output:** `Oid`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Parses an OID.

## Type

### Oid

[ref: #symbol-oid]

```nim
Oid = object
```

An OID.
