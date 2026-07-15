---
source_hash: 83b33519860bb86d
source_path: lib/core/macros.nim
---

### newLit

[ref: #symbol-newlit]

**Input:**
- `i: uint32`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new unsigned integer literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `i: uint64`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new unsigned integer literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `b: bool`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new boolean literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `s: string`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new string literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `f: float32`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new float literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `f: float64`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new float literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `arg: enum`

**Output:** `NimNode`
**Generic parameters:** `arg:type`

### newLit

[ref: #symbol-newlit]

**Input:**
- `arg: array[N, T]`

**Output:** `NimNode`
**Generic parameters:** `N`, `T`

### newLit

[ref: #symbol-newlit]

**Input:**
- `arg: seq[T]`

**Output:** `NimNode`
**Generic parameters:** `T`

### newLit

[ref: #symbol-newlit]

**Input:**
- `s: set[T]`

**Output:** `NimNode`
**Generic parameters:** `T`

### newLit

[ref: #symbol-newlit]

**Input:**
- `arg: T`

**Output:** `NimNode`
**Generic parameters:** `T`

### newLit

[ref: #symbol-newlit]

**Input:**
- `arg: object`

**Output:** `NimNode`
**Generic parameters:** `arg:type`

### newLit

[ref: #symbol-newlit]

**Input:**
- `arg: ref object`

**Output:** `NimNode`
**Generic parameters:** `arg:type`

produces a new ref type literal node.

### newNilLit

[ref: #symbol-newnillit]

**Input:**
- *(none)*

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

New nil literal shortcut.

### newNimNode

[ref: #symbol-newnimnode]

Creates a new AST node of the specified kind.

**Input:**
- `kind: NimNodeKind`
- `lineInfoFrom: NimNode = nil`

**Output:** `NimNode`
**Pragmas:** `magic: "NNewNimNode"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new AST node of the specified kind.

The lineInfoFrom parameter is used for line information when the produced code crashes. You should ensure that it is set to a node that you are transforming.

### newPar

[ref: #symbol-newpar]

**Input:**
- `exprs: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new parentheses-enclosed expression.

### newPar

[ref: #symbol-newpar]

**Input:**
- `exprs: varargs[NimNode]`

**Output:** `NimNode`
**Pragmas:** `deprecated: "don\'t use newPar/nnkPar to construct tuple expressions; use nnkTupleConstr instead"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new parentheses-enclosed expression.

### newProc

[ref: #symbol-newproc]

Shortcut for creating a new proc.

**Input:**
- `name:  = newEmptyNode()`
- `params: openArray[NimNode] = [newEmptyNode()]`
- `body: NimNode = newStmtList()`
- `procType:  = nnkProcDef`
- `pragmas: NimNode = newEmptyNode()`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Shortcut for creating a new proc.

The params array must start with the return type of the proc, followed by a list of IdentDefs which specify the params.

### newStmtList

[ref: #symbol-newstmtlist]

**Input:**
- `stmts: varargs[NimNode]`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new statement list.

### newStrLitNode

[ref: #symbol-newstrlitnode]

**Input:**
- `s: string`

**Output:** `NimNode`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a string literal node from s.

### newTree

[ref: #symbol-newtree]

**Input:**
- `kind: NimNodeKind`
- `children: varargs[NimNode]`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new node with children.

### newVarStmt

[ref: #symbol-newvarstmt]

**Input:**
- `name: NimNode`
- `value: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new var stmt.

### nodeID

[ref: #symbol-nodeid]

**Input:**
- `n: NimNode`

**Output:** `int`
**Pragmas:** `magic: "NodeId"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the id of n, when the compiler has been compiled with the flag -d:useNodeids, otherwise returns -1. This proc is for the purpose to debug the compiler only.

### owner

[ref: #symbol-owner]

Accepts a node of kind nnkSym and returns its owner's symbol. The meaning of 'owner' depends on sym's NimSymKind and declaration context. For top level declarations this is an nskModule symbol, for proc local variables an nskProc symbol, for enum/object fields an nskType symbol, etc. For symbols without an owner, nil is returned.

**Input:**
- `sym: NimNode`

**Output:** `NimNode`
**Pragmas:** `magic: "SymOwner"`, `noSideEffect`, `deprecated`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Accepts a node of kind nnkSym and returns its owner's symbol. The meaning of 'owner' depends on sym's NimSymKind and declaration context. For top level declarations this is an nskModule symbol, for proc local variables an nskProc symbol, for enum/object fields an nskType symbol, etc. For symbols without an owner, nil is returned.

See also:

* [symKind proc](#symKind,NimNode) to get the kind of a symbol
* [getImpl proc](#getImpl,NimNode) to get the declaration of a symbol

### params

[ref: #symbol-params]

**Input:**
- `someProc: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### params=

[ref: #symbol-params]

**Input:**
- `someProc: NimNode`
- `params: NimNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### parseExpr

[ref: #symbol-parseexpr]

**Input:**
- `s: string`
- `filename: string = ""`

**Output:** `NimNode`
**Pragmas:** `noSideEffect`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Compiles the passed string to its AST representation. Expects a single expression. Raises ValueError for parsing errors. A filename can be given for more informative errors.

### parseStmt

[ref: #symbol-parsestmt]

**Input:**
- `s: string`
- `filename: string = ""`

**Output:** `NimNode`
**Pragmas:** `noSideEffect`, `raises: [ValueError]`, `tags: []`, `forbids: []`

**Effects:** `raises: ValueError`, `tags: `, `forbids: `

Compiles the passed string to its AST representation. Expects one or more statements. Raises ValueError for parsing errors. A filename can be given for more informative errors.

### postfix

[ref: #symbol-postfix]

**Input:**
- `node: NimNode`
- `op: string`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pragma

[ref: #symbol-pragma]

**Input:**
- `someProc: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get the pragma of a proc type. These will be expanded.

### pragma=

[ref: #symbol-pragma]

**Input:**
- `someProc: NimNode`
- `val: NimNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set the pragma of a proc type.

### prefix

[ref: #symbol-prefix]

**Input:**
- `node: NimNode`
- `op: string`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### quote

[ref: #symbol-quote]

Quasi-quoting operator. Accepts an expression or a block and returns the AST that represents it. Within the quoted AST, you are able to interpolate NimNode expressions from the surrounding scope. If no operator is given, quoting is done using backticks. Otherwise, the given operator must be used as a prefix operator for any interpolated expression. The original meaning of the interpolation operator may be obtained by escaping it (by prefixing it with itself) when used as a unary operator: e.g. @ is escaped as @@, &% is escaped as &%&% and so on; see examples.

**Input:**
- `bl: typed`
- `op:  = "``"`

**Output:** `NimNode`
**Pragmas:** `magic: "QuoteAst"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Quasi-quoting operator. Accepts an expression or a block and returns the AST that represents it. Within the quoted AST, you are able to interpolate NimNode expressions from the surrounding scope. If no operator is given, quoting is done using backticks. Otherwise, the given operator must be used as a prefix operator for any interpolated expression. The original meaning of the interpolation operator may be obtained by escaping it (by prefixing it with itself) when used as a unary operator: e.g. @ is escaped as @@, &% is escaped as &%&% and so on; see examples.

A custom operator interpolation needs accent quoted (``) whenever it resolves to a symbol.

See also [genasts](genasts.html) which avoids some issues with quote.

### sameType

[ref: #symbol-sametype]

**Input:**
- `a: NimNode`
- `b: NimNode`

**Output:** `bool`
**Pragmas:** `magic: "SameNodeType"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two Nim nodes' types. Return true if the types are the same, e.g. true when comparing alias with original type.

### setLineInfo

[ref: #symbol-setlineinfo]

**Input:**
- `arg: NimNode`
- `file: string`
- `line: int`
- `column: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the line info on the NimNode. The file needs to exists, but can be a relative path. If you want to attach line info to a block using quote you'll need to add the line information after the quote block.

### setLineInfo

[ref: #symbol-setlineinfo]

**Input:**
- `arg: NimNode`
- `lineInfo: LineInfo`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

See [setLineInfo proc](#setLineInfo,NimNode,string,int,int)

### signatureHash

[ref: #symbol-signaturehash]

**Input:**
- `n: NimNode`

**Output:** `string`
**Pragmas:** `magic: "NSigHash"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a stable identifier derived from the signature of a symbol. The signature combines many factors such as the type of the symbol, the owning module of the symbol and others. The same identifier is used in the back-end to produce the mangled symbol name.

### strVal

[ref: #symbol-strval]

Returns the string value of an identifier, symbol, comment, or string literal.

**Input:**
- `n: NimNode`

**Output:** `string`
**Pragmas:** `magic: "NStrVal"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the string value of an identifier, symbol, comment, or string literal.

See also:

* [strVal= proc](#strVal=,NimNode,string) for setting the string value.

### strVal=

[ref: #symbol-strval]

Sets the string value of a string literal or comment. Setting strVal is disallowed for nnkIdent and nnkSym nodes; a new node must be created using ident or bindSym instead.

**Input:**
- `n: NimNode`
- `val: string`

**Output:** *(none)*
**Pragmas:** `magic: "NSetStrVal"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Sets the string value of a string literal or comment. Setting strVal is disallowed for nnkIdent and nnkSym nodes; a new node must be created using ident or bindSym instead.

See also:

* [strVal proc](#strVal,NimNode) for getting the string value.
* [ident proc](#ident,string) for creating an identifier.
* [bindSym proc](#bindSym%2C%2CBindSymRule) for binding a symbol.

### symBodyHash

[ref: #symbol-symbodyhash]

**Input:**
- `s: NimNode`

**Output:** `string`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a stable digest for symbols derived not only from type signature and owning module, but also implementation body. All procs/variables used in the implementation of this symbol are hashed recursively as well, including magics from system module.

### symbol

[ref: #symbol-symbol]

**Input:**
- `n: NimNode`

**Output:** `NimSym`
**Pragmas:** `magic: "NSymbol"`, `noSideEffect`, `deprecated: "Deprecated since version 0.18.1; All functionality is defined on \'NimNode\'."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### symbol=

[ref: #symbol-symbol]

**Input:**
- `n: NimNode`
- `val: NimSym`

**Output:** *(none)*
**Pragmas:** `magic: "NSetSymbol"`, `noSideEffect`, `deprecated: "Deprecated since version 0.18.1; Generate a new \'NimNode\' with \'genSym\' instead."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### symKind

[ref: #symbol-symkind]

**Input:**
- `symbol: NimNode`

**Output:** `NimSymKind`
**Pragmas:** `magic: "NSymKind"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### toNimIdent

[ref: #symbol-tonimident]

**Input:**
- `s: string`

**Output:** `NimIdent`
**Pragmas:** `magic: "StrToIdent"`, `noSideEffect`, `deprecated: "Deprecated since version 0.18.0: Use \'ident\' or \'newIdentNode\' instead."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructs an identifier from the string s.

### toStrLit

[ref: #symbol-tostrlit]

**Input:**
- `n: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts the AST n to the concrete Nim code and wraps that in a string literal node.

### treeRepr

[ref: #symbol-treerepr]

Convert the AST n to a human-readable tree-like string.

**Input:**
- `n: NimNode`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Convert the AST n to a human-readable tree-like string.

See also repr, [lispRepr](#lispRepr), and [astGenRepr](#astGenRepr).

### typeKind

[ref: #symbol-typekind]

**Input:**
- `n: NimNode`

**Output:** `NimTypeKind`
**Pragmas:** `magic: "NGetType"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the type kind of the node 'n' that should represent a type, that means the node should have been obtained via getType.

### unpackInfix

[ref: #symbol-unpackinfix]

**Input:**
- `node: NimNode`

**Output:** `tuple[left: NimNode, op: string, right: NimNode]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### unpackPostfix

[ref: #symbol-unpackpostfix]

**Input:**
- `node: NimNode`

**Output:** `tuple[node: NimNode, op: string]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### unpackPrefix

[ref: #symbol-unpackprefix]

**Input:**
- `node: NimNode`

**Output:** `tuple[node: NimNode, op: string]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### warning

[ref: #symbol-warning]

**Input:**
- `msg: string`
- `n: NimNode = nil`

**Output:** *(none)*
**Pragmas:** `magic: "NWarning"`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Writes a warning message at compile time.

## Template

### `or`

[ref: #symbol-or]

Evaluate x and when it is not an empty node, return it. Otherwise evaluate to y. Can be used to chain several expressions to get the first expression that is not empty.

**Input:**
- `x: NimNode`
- `y: NimNode`

**Output:** `NimNode`
Evaluate x and when it is not an empty node, return it. Otherwise evaluate to y. Can be used to chain several expressions to get the first expression that is not empty.

```
let node = mightBeEmpty() or mightAlsoBeEmpty() or fallbackNode
```

### findChild

[ref: #symbol-findchild]

Find the first child node matching condition (or nil).

**Input:**
- `n: NimNode`
- `cond: untyped`

**Output:** `NimNode`
**Pragmas:** `dirty`

Find the first child node matching condition (or nil).

```
var res = findChild(n, it.kind == nnkPostfix and
                       it.basename.ident == ident"foo")
```

## Type

### BindSymRule

[ref: #symbol-bindsymrule]

```nim
BindSymRule = enum
  brClosed,                 ## only the symbols in current scope are bound
  brOpen,                   ## open for overloaded symbols, but may be a single
                             ## symbol if not ambiguous (the rules match that of
                             ## binding in generics)
  brForceOpen                ## same as brOpen, but it will always be open even
                             ## if not ambiguous (this cannot be achieved with
                             ## any other means in the language currently)
```

Specifies how bindSym behaves. The difference between open and closed symbols can be found in <manual.html#symbol-lookup-in-generics-open-and-closed-symbols>

### LineInfo

[ref: #symbol-lineinfo]

```nim
LineInfo = object
  filename*: string
  line*, column*: int
```

### NimIdent

[ref: #symbol-nimident]

```nim
NimIdent {.deprecated.} = object of RootObj
```

Represents a Nim identifier in the AST. **Note**: This is only rarely useful, for identifier construction from a string use ident"abc".

### NimNodeKind

[ref: #symbol-nimnodekind]

```nim
NimNodeKind = enum
  nnkNone, nnkEmpty, nnkIdent, nnkSym, nnkType, nnkCharLit, nnkIntLit,
  nnkInt8Lit, nnkInt16Lit, nnkInt32Lit, nnkInt64Lit, nnkUIntLit, nnkUInt8Lit,
  nnkUInt16Lit, nnkUInt32Lit, nnkUInt64Lit, nnkFloatLit, nnkFloat32Lit,
  nnkFloat64Lit, nnkFloat128Lit, nnkStrLit, nnkRStrLit, nnkTripleStrLit,
  nnkNilLit, nnkComesFrom, nnkDotCall, nnkCommand, nnkCall, nnkCallStrLit,
  nnkInfix, nnkPrefix, nnkPostfix, nnkHiddenCallConv, nnkExprEqExpr,
  nnkExprColonExpr, nnkIdentDefs, nnkVarTuple, nnkPar, nnkObjConstr, nnkCurly,
  nnkCurlyExpr, nnkBracket, nnkBracketExpr, nnkPragmaExpr, nnkRange, nnkDotExpr,
  nnkCheckedFieldExpr, nnkDerefExpr, nnkIfExpr, nnkElifExpr, nnkElseExpr,
  nnkLambda, nnkDo, nnkAccQuoted, nnkTableConstr, nnkBind, nnkClosedSymChoice,
  nnkOpenSymChoice, nnkHiddenStdConv, nnkHiddenSubConv, nnkConv, nnkCast,
  nnkStaticExpr, nnkAddr, nnkHiddenAddr, nnkHiddenDeref, nnkObjDownConv,
  nnkObjUpConv, nnkChckRangeF, nnkChckRange64, nnkChckRange, nnkStringToCString,
  nnkCStringToString, nnkAsgn, nnkFastAsgn, nnkGenericParams, nnkFormalParams,
  nnkOfInherit, nnkImportAs, nnkProcDef, nnkMethodDef, nnkConverterDef,
  nnkMacroDef, nnkTemplateDef, nnkIteratorDef, nnkOfBranch, nnkElifBranch,
  nnkExceptBranch, nnkElse, nnkAsmStmt, nnkPragma, nnkPragmaBlock, nnkIfStmt,
  nnkWhenStmt, nnkForStmt, nnkParForStmt, nnkWhileStmt, nnkCaseStmt,
  nnkTypeSection, nnkVarSection, nnkLetSection, nnkConstSection, nnkConstDef,
  nnkTypeDef, nnkYieldStmt, nnkDefer, nnkTryStmt, nnkFinally, nnkRaiseStmt,
  nnkReturnStmt, nnkBreakStmt, nnkContinueStmt, nnkBlockStmt, nnkStaticStmt,
  nnkDiscardStmt, nnkStmtList, nnkImportStmt, nnkImportExceptStmt,
  nnkExportStmt, nnkExportExceptStmt, nnkFromStmt, nnkIncludeStmt, nnkBindStmt,
  nnkMixinStmt, nnkUsingStmt, nnkCommentStmt, nnkStmtListExpr, nnkBlockExpr,
  nnkStmtListType, nnkBlockType, nnkWith, nnkWithout, nnkTypeOfExpr,
  nnkObjectTy, nnkTupleTy, nnkTupleClassTy, nnkTypeClassTy, nnkStaticTy,
  nnkRecList, nnkRecCase, nnkRecWhen, nnkRefTy, nnkPtrTy, nnkVarTy, nnkConstTy,
  nnkOutTy, nnkDistinctTy, nnkProcTy, nnkIteratorTy, nnkSinkAsgn, nnkEnumTy,
  nnkEnumFieldDef, nnkArgList, nnkPattern, nnkHiddenTryStmt, nnkClosure,
  nnkGotoState, nnkState, nnkBreakState, nnkFuncDef, nnkTupleConstr, nnkError, ## erroneous AST node
  nnkModuleRef, nnkReplayAction, nnkNilRodNode, ## internal IC nodes
  nnkOpenSym
```

### NimNodeKinds

[ref: #symbol-nimnodekinds]

```nim
NimNodeKinds = set[NimNodeKind]
```

### NimSym

[ref: #symbol-nimsym]

```nim
NimSym {.deprecated.} = ref NimSymObj
```

Represents a Nim *symbol* in the compiler; a *symbol* is a looked-up *ident*.

### NimSymKind

[ref: #symbol-nimsymkind]

```nim
NimSymKind = enum
  nskUnknown, nskConditional, nskDynLib, nskParam, nskGenericParam, nskTemp,
  nskModule, nskType, nskVar, nskLet, nskConst, nskResult, nskProc, nskFunc,
  nskMethod, nskIterator, nskConverter, nskMacro, nskTemplate, nskField,
  nskEnumField, nskForVar, nskLabel, nskStub
```

### NimTypeKind

[ref: #symbol-nimtypekind]

```nim
NimTypeKind = enum
  ntyNone, ntyBool, ntyChar, ntyEmpty, ntyAlias, ntyNil, ntyExpr, ntyStmt,
  ntyTypeDesc, ntyGenericInvocation, ntyGenericBody, ntyGenericInst,
  ntyGenericParam, ntyDistinct, ntyEnum, ntyOrdinal, ntyArray, ntyObject,
  ntyTuple, ntySet, ntyRange, ntyPtr, ntyRef, ntyVar, ntySequence, ntyProc,
  ntyPointer, ntyOpenArray, ntyString, ntyCString, ntyForward, ntyInt, ntyInt8,
  ntyInt16, ntyInt32, ntyInt64, ntyFloat, ntyFloat32, ntyFloat64, ntyFloat128,
  ntyUInt, ntyUInt8, ntyUInt16, ntyUInt32, ntyUInt64, ntyUnused0, ntyUnused1,
  ntyUnused2, ntyVarargs, ntyUncheckedArray, ntyError, ntyBuiltinTypeClass,
  ntyUserTypeClass, ntyUserTypeClassInst, ntyCompositeTypeClass, ntyInferred,
  ntyAnd, ntyOr, ntyNot, ntyAnything, ntyStatic, ntyFromExpr, ntyOptDeprecated,
  ntyVoid
```

### TNimSymKinds

[ref: #symbol-tnimsymkinds]

```nim
TNimSymKinds {.deprecated.} = set[NimSymKind]
```

### TNimTypeKinds

[ref: #symbol-tnimtypekinds]

```nim
TNimTypeKinds {.deprecated.} = set[NimTypeKind]
```

[Prev](macros_3.md)
