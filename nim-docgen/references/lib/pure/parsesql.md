---
source_hash: 622331e7328b6764
source_path: lib/pure/parsesql.nim
---

# parsesql

[ref: #module-parsesql]

The parsesql module implements a high performance SQL file parser. It parses PostgreSQL syntax and the SQL ANSI standard.

Unstable API.

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `n: SqlNode`

**Output:** `string`
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

an alias for renderSql.

### `[]`

[ref: #symbol-]

**Input:**
- `n: SqlNode`
- `i: int`

**Output:** `SqlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### `[]`

[ref: #symbol-]

**Input:**
- `n: SqlNode`
- `i: BackwardsIndex`

**Output:** `SqlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### add

[ref: #symbol-add]

**Input:**
- `father: SqlNode`
- `n: SqlNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### len

[ref: #symbol-len]

**Input:**
- `n: SqlNode`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newNode

[ref: #symbol-newnode]

**Input:**
- `k: SqlNodeKind`

**Output:** `SqlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newNode

[ref: #symbol-newnode]

**Input:**
- `k: SqlNodeKind`
- `s: string`

**Output:** `SqlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newNode

[ref: #symbol-newnode]

**Input:**
- `k: SqlNodeKind`
- `sons: seq[SqlNode]`

**Output:** `SqlNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### parseSql

[ref: #symbol-parsesql]

**Input:**
- `input: Stream`
- `filename: string`
- `considerTypeParams:  = false`

**Output:** `SqlNode`
**Pragmas:** `raises: [IOError, OSError, IOError, OSError, ValueError, SqlParseError,
         Exception]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, IOError, OSError, ValueError, SqlParseError, Exception`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

parses the SQL from input into an AST and returns the AST. filename is only used for error messages. Syntax errors raise an SqlParseError exception.

### parseSql

[ref: #symbol-parsesql]

**Input:**
- `input: string`
- `filename:  = ""`
- `considerTypeParams:  = false`

**Output:** `SqlNode`
**Pragmas:** `raises: [IOError, OSError, ValueError, SqlParseError, Exception]`, `tags: [ReadIOEffect, RootEffect, WriteIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, OSError, ValueError, SqlParseError, Exception`, `tags: ReadIOEffect, RootEffect, WriteIOEffect`, `forbids: `

parses the SQL from input into an AST and returns the AST. filename is only used for error messages. Syntax errors raise an SqlParseError exception.

### renderSql

[ref: #symbol-rendersql]

**Input:**
- `n: SqlNode`
- `upperCase:  = false`

**Output:** `string`
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Converts an SQL abstract syntax tree to its string representation.

### treeRepr

[ref: #symbol-treerepr]

**Input:**
- `s: SqlNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### SqlLexer

[ref: #symbol-sqllexer]

```nim
SqlLexer = object of BaseLexer
```

the parser object.

### SqlNode

[ref: #symbol-sqlnode]

```nim
SqlNode = ref SqlNodeObj
```

an SQL abstract syntax tree node

### SqlNodeKind

[ref: #symbol-sqlnodekind]

```nim
SqlNodeKind = enum
  nkNone, nkIdent, nkQuotedIdent, nkStringLit, nkBitStringLit, nkHexStringLit,
  nkIntegerLit, nkNumericLit, nkPrimaryKey, nkForeignKey, nkNotNull, nkNull,
  nkStmtList, nkDot, nkDotDot, nkPrefix, nkInfix, nkCall, nkPrGroup,
  nkColumnReference, nkReferences, nkDefault, nkCheck, nkConstraint, nkUnique,
  nkIdentity, nkColumnDef,  ## name, datatype, constraints
  nkInsert, nkUpdate, nkDelete, nkSelect, nkSelectDistinct, nkSelectColumns,
  nkSelectPair, nkAsgn, nkFrom, nkFromItemPair, nkJoin, nkNaturalJoin, nkUsing,
  nkGroup, nkLimit, nkOffset, nkHaving, nkOrder, nkDesc, nkUnion, nkIntersect,
  nkExcept, nkColumnList, nkValueList, nkWhere, nkCreateTable,
  nkCreateTableIfNotExists, nkCreateType, nkCreateTypeIfNotExists,
  nkCreateIndex, nkCreateIndexIfNotExists, nkEnumDef
```

kind of SQL abstract syntax tree

### SqlNodeObj

[ref: #symbol-sqlnodeobj]

```nim
SqlNodeObj = object
  case kind*: SqlNodeKind    ## kind of syntax tree
  of LiteralNodes:
    strVal*: string          ## AST leaf: the identifier, numeric literal
                             ## string literal, etc.
  else:
    sons*: seq[SqlNode]      ## the node's children
```

an SQL abstract syntax tree node

### SqlParseError

[ref: #symbol-sqlparseerror]

```nim
SqlParseError = object of ValueError
```

Invalid SQL encountered

### SqlParser

[ref: #symbol-sqlparser]

```nim
SqlParser = object of SqlLexer
```

SQL parser object
