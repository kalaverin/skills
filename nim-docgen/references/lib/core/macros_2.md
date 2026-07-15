---
source_hash: 83b33519860bb86d
source_path: lib/core/macros.nim
---

## Const

### AtomicNodes

[ref: #symbol-atomicnodes]

```nim
AtomicNodes = {nnkNone..nnkNilLit}
```

### CallNodes

[ref: #symbol-callnodes]

```nim
CallNodes = {nnkCall, nnkInfix, nnkPrefix, nnkPostfix, nnkCommand,
             nnkCallStrLit, nnkHiddenCallConv}
```

### nnkCallKinds

[ref: #symbol-nnkcallkinds]

```nim
nnkCallKinds = {nnkCall, nnkInfix, nnkPrefix, nnkPostfix, nnkCommand,
                nnkCallStrLit, nnkHiddenCallConv}
```

### nnkLiterals

[ref: #symbol-nnkliterals]

```nim
nnkLiterals = {nnkCharLit..nnkNilLit}
```

### nnkMutableTy

[ref: #symbol-nnkmutablety]

```nim
nnkMutableTy {.deprecated.} = nnkOutTy
```

### nnkSharedTy

[ref: #symbol-nnksharedty]

```nim
nnkSharedTy {.deprecated.} = nnkSinkAsgn
```

### RoutineNodes

[ref: #symbol-routinenodes]

```nim
RoutineNodes = {nnkProcDef, nnkFuncDef, nnkMethodDef, nnkDo, nnkLambda,
                nnkIteratorDef, nnkTemplateDef, nnkConverterDef, nnkMacroDef}
```

## Iterator

### children

[ref: #symbol-children]

**Input:**
- `n: NimNode`

**Output:** `NimNode`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over the children of the NimNode n.

### items

[ref: #symbol-items]

**Input:**
- `n: NimNode`

**Output:** `NimNode`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over the children of the NimNode n.

### pairs

[ref: #symbol-pairs]

**Input:**
- `n: NimNode`

**Output:** `(int, NimNode)`
**Pragmas:** `inline`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Iterates over the children of the NimNode n and its indices.

## Macro

### dumpAstGen

[ref: #symbol-dumpastgen]

Accepts a block of nim code and prints the parsed abstract syntax tree using the astGenRepr proc. Printing is done *at compile time*.

**Input:**
- `s: untyped`

**Output:** `untyped`
Accepts a block of nim code and prints the parsed abstract syntax tree using the astGenRepr proc. Printing is done *at compile time*.

You can use this as a tool to write macros quicker by writing example outputs and then copying the snippets into the macro for modification.

For example:

```
dumpAstGen:
  echo "Hello, World!"
```

Outputs:

```
nnkStmtList.newTree(
  nnkCommand.newTree(
    newIdentNode("echo"),
    newLit("Hello, World!")
  )
)
```

Also see dumpTree and dumpLisp.

### dumpLisp

[ref: #symbol-dumplisp]

Accepts a block of nim code and prints the parsed abstract syntax tree using the lispRepr proc. Printing is done *at compile time*.

**Input:**
- `s: untyped`

**Output:** `untyped`
Accepts a block of nim code and prints the parsed abstract syntax tree using the lispRepr proc. Printing is done *at compile time*.

You can use this as a tool to explore the Nim's abstract syntax tree and to discover what kind of nodes must be created to represent a certain expression/statement.

For example:

```
dumpLisp:
  echo "Hello, World!"
```

Outputs:

```
(StmtList
 (Command
  (Ident "echo")
  (StrLit "Hello, World!")))
```

Also see dumpAstGen and dumpTree.

### dumpTree

[ref: #symbol-dumptree]

Accepts a block of nim code and prints the parsed abstract syntax tree using the treeRepr proc. Printing is done *at compile time*.

**Input:**
- `s: untyped`

**Output:** `untyped`
Accepts a block of nim code and prints the parsed abstract syntax tree using the treeRepr proc. Printing is done *at compile time*.

You can use this as a tool to explore the Nim's abstract syntax tree and to discover what kind of nodes must be created to represent a certain expression/statement.

For example:

```
dumpTree:
  echo "Hello, World!"
```

Outputs:

```
StmtList
  Command
    Ident "echo"
    StrLit "Hello, World!"
```

Also see dumpAstGen and dumpLisp.

### expandMacros

[ref: #symbol-expandmacros]

Expands one level of macro - useful for debugging. Can be used to inspect what happens when a macro call is expanded, without altering its result.

**Input:**
- `body: typed`

**Output:** `untyped`
Expands one level of macro - useful for debugging. Can be used to inspect what happens when a macro call is expanded, without altering its result.

For instance,

```
import std/[sugar, macros]

let
  x = 10
  y = 20
expandMacros:
  dump(x + y)
```

will actually dump x + y, but at the same time will print at compile time the expansion of the dump macro, which in this case is debugEcho ["x + y", " = ", x + y].

### getCustomPragmaVal

[ref: #symbol-getcustompragmaval]

Expands to value of custom pragma cp of expression n which is expected to be nnkDotExpr, a proc or a type.

**Input:**
- `n: typed`
- `cp: typed{nkSym}`

**Output:** `untyped`
Expands to value of custom pragma cp of expression n which is expected to be nnkDotExpr, a proc or a type.

See also [hasCustomPragma](#hasCustomPragma).

```
template serializationKey(key: string) {.pragma.}
type
  MyObj {.serializationKey: "mo".} = object
    myField {.serializationKey: "mf".}: int
var o: MyObj
assert(o.myField.getCustomPragmaVal(serializationKey) == "mf")
assert(o.getCustomPragmaVal(serializationKey) == "mo")
assert(MyObj.getCustomPragmaVal(serializationKey) == "mo")
```

### hasCustomPragma

[ref: #symbol-hascustompragma]

Expands to true if expression n which is expected to be nnkDotExpr (if checking a field), a proc or a type has custom pragma cp.

**Input:**
- `n: typed`
- `cp: typed{nkSym}`

**Output:** `untyped`
Expands to true if expression n which is expected to be nnkDotExpr (if checking a field), a proc or a type has custom pragma cp.

See also [getCustomPragmaVal](#getCustomPragmaVal).

```
template myAttr() {.pragma.}
type
  MyObj = object
    myField {.myAttr.}: int

proc myProc() {.myAttr.} = discard

var o: MyObj
assert(o.myField.hasCustomPragma(myAttr))
assert(myProc.hasCustomPragma(myAttr))
```

### unpackVarargs

[ref: #symbol-unpackvarargs]

Calls callee with args unpacked as individual arguments. This is useful in 2 cases:

**Input:**
- `callee: untyped`
- `args: varargs[untyped]`

**Output:** `untyped`
Calls callee with args unpacked as individual arguments. This is useful in 2 cases:

* when forwarding varargs[T] for some typed T
* when forwarding varargs[untyped] when args can potentially be empty, due to a compiler limitation

## Proc

### `$`

[ref: #symbol-]

**Input:**
- `i: NimIdent`

**Output:** `string`
**Pragmas:** `magic: "NStrVal"`, `noSideEffect`, `deprecated: "Deprecated since version 0.18.1; Use \'strVal\' instead."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a Nim identifier to a string.

### `$`

[ref: #symbol-]

**Input:**
- `s: NimSym`

**Output:** `string`
**Pragmas:** `magic: "NStrVal"`, `noSideEffect`, `deprecated: "Deprecated since version 0.18.1; Use \'strVal\' instead."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Converts a Nim symbol to a string.

### `$`

[ref: #symbol-]

**Input:**
- `arg: LineInfo`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Return a string representation in the form filepath(line, column).

### `$`

[ref: #symbol-]

**Input:**
- `node: NimNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get the string of an identifier node.

### `==`

[ref: #symbol-]

**Input:**
- `a: NimIdent`
- `b: NimIdent`

**Output:** `bool`
**Pragmas:** `magic: "EqIdent"`, `noSideEffect`, `deprecated: "Deprecated since version 0.18.1; Use \'==\' on \'NimNode\' instead."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two Nim identifiers.

### `==`

[ref: #symbol-]

**Input:**
- `a: NimNode`
- `b: NimNode`

**Output:** `bool`
**Pragmas:** `magic: "EqNimrodNode"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compare two Nim nodes. Return true if nodes are structurally equivalent. This means two independently created nodes can be equal.

### `==`

[ref: #symbol-]

**Input:**
- `a: NimSym`
- `b: NimSym`

**Output:** `bool`
**Pragmas:** `magic: "EqNimrodNode"`, `noSideEffect`, `deprecated: "Deprecated since version 0.18.1; Use \'==(NimNode, NimNode)\' instead."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Compares two Nim symbols.

### `[]=`

[ref: #symbol-]

**Input:**
- `n: NimNode`
- `i: int`
- `child: NimNode`

**Output:** *(none)*
**Pragmas:** `magic: "NSetChild"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set n's i'th child to child.

### `[]=`

[ref: #symbol-]

**Input:**
- `n: NimNode`
- `i: BackwardsIndex`
- `child: NimNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set n's i'th child to child.

### `[]`

[ref: #symbol-]

**Input:**
- `n: NimNode`
- `i: int`

**Output:** `NimNode`
**Pragmas:** `magic: "NChild"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get n's i'th child.

### `[]`

[ref: #symbol-]

**Input:**
- `n: NimNode`
- `i: BackwardsIndex`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get n's i'th child.

### `[]`

[ref: #symbol-]

**Input:**
- `n: NimNode`
- `x: HSlice[T, U]`

**Output:** `seq[NimNode]`
**Generic parameters:** `T`, `U`

Slice operation for NimNode. Returns a seq of child of n who inclusive range [n[x.a], n[x.b]].

### add

[ref: #symbol-add]

**Input:**
- `father: NimNode`
- `child: NimNode`

**Output:** `NimNode`
**Pragmas:** `magic: "NAdd"`, `discardable`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds the child to the father node. Returns the father node so that calls can be nested.

### add

[ref: #symbol-add]

**Input:**
- `father: NimNode`
- `children: varargs[NimNode]`

**Output:** `NimNode`
**Pragmas:** `magic: "NAddMultiple"`, `discardable`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds each child of children to the father node. Returns the father node so that calls can be nested.

### addIdentIfAbsent

[ref: #symbol-addidentifabsent]

**Input:**
- `dest: NimNode`
- `ident: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Add ident to dest if it is not present. This is intended for use with pragmas.

### addPragma

[ref: #symbol-addpragma]

**Input:**
- `someProc: NimNode`
- `pragma: NimNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Adds pragma to routine definition.

### astGenRepr

[ref: #symbol-astgenrepr]

Convert the AST n to the code required to generate that AST.

**Input:**
- `n: NimNode`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Convert the AST n to the code required to generate that AST.

See also [repr](#repr), [treeRepr](#treeRepr), and [lispRepr](#lispRepr).

### basename

[ref: #symbol-basename]

**Input:**
- `a: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Pull an identifier from prefix/postfix expressions.

### basename=

[ref: #symbol-basename]

**Input:**
- `a: NimNode`
- `val: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### bindSym

[ref: #symbol-bindsym]

Creates a node that binds ident to a symbol node. The bound symbol may be an overloaded symbol. if ident is a NimNode, it must have nnkIdent kind. If rule == brClosed either an nnkClosedSymChoice tree is returned or nnkSym if the symbol is not ambiguous. If rule == brOpen either an nnkOpenSymChoice tree is returned or nnkSym if the symbol is not ambiguous. If rule == brForceOpen always an nnkOpenSymChoice tree is returned even if the symbol is not ambiguous.

**Input:**
- `ident: string | NimNode`
- `rule: BindSymRule = brClosed`

**Output:** `NimNode`
**Generic parameters:** `ident:type`

**Pragmas:** `magic: "NBindSym"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a node that binds ident to a symbol node. The bound symbol may be an overloaded symbol. if ident is a NimNode, it must have nnkIdent kind. If rule == brClosed either an nnkClosedSymChoice tree is returned or nnkSym if the symbol is not ambiguous. If rule == brOpen either an nnkOpenSymChoice tree is returned or nnkSym if the symbol is not ambiguous. If rule == brForceOpen always an nnkOpenSymChoice tree is returned even if the symbol is not ambiguous.

See the [manual](manual.html#macros-bindsym) for more details.

### body

[ref: #symbol-body]

**Input:**
- `someProc: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### body=

[ref: #symbol-body]

**Input:**
- `someProc: NimNode`
- `val: NimNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### boolVal

[ref: #symbol-boolval]

**Input:**
- `n: NimNode`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### callsite

[ref: #symbol-callsite]

**Input:**
- *(none)*

**Output:** `NimNode`
**Pragmas:** `magic: "NCallSite"`, `gcsafe`, `deprecated: "Deprecated since v0.18.1; use `varargs[untyped]` in the macro prototype instead"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the AST of the invocation expression that invoked this macro.

### copy

[ref: #symbol-copy]

**Input:**
- `node: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

An alias for [copyNimTree](#copyNimTree,NimNode).

### copyChildrenTo

[ref: #symbol-copychildrento]

**Input:**
- `src: NimNode`
- `dest: NimNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copy all children from src to dest.

### copyLineInfo

[ref: #symbol-copylineinfo]

**Input:**
- `arg: NimNode`
- `info: NimNode`

**Output:** *(none)*
**Pragmas:** `magic: "NLineInfo"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Copy lineinfo from info.

### copyNimNode

[ref: #symbol-copynimnode]

**Input:**
- `n: NimNode`

**Output:** `NimNode`
**Pragmas:** `magic: "NCopyNimNode"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new AST node by copying the node n. Note that unlike copyNimTree, child nodes of n are not copied.

### copyNimTree

[ref: #symbol-copynimtree]

**Input:**
- `n: NimNode`

**Output:** `NimNode`
**Pragmas:** `magic: "NCopyNimTree"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new AST node by recursively copying the node n. Note that unlike copyNimNode, this copies n, the children of n, etc.

### del

[ref: #symbol-del]

**Input:**
- `father: NimNode`
- `idx:  = 0`
- `n:  = 1`

**Output:** *(none)*
**Pragmas:** `magic: "NDel"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Deletes n children of father starting at index idx.

### eqIdent

[ref: #symbol-eqident]

**Input:**
- `a: string`
- `b: string`

**Output:** `bool`
**Pragmas:** `magic: "EqIdent"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Style insensitive comparison.

### eqIdent

[ref: #symbol-eqident]

**Input:**
- `a: NimNode`
- `b: string`

**Output:** `bool`
**Pragmas:** `magic: "EqIdent"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Style insensitive comparison. a can be an identifier or a symbol. a may be wrapped in an export marker (nnkPostfix) or quoted with backticks (nnkAccQuoted), these nodes will be unwrapped.

### eqIdent

[ref: #symbol-eqident]

**Input:**
- `a: string`
- `b: NimNode`

**Output:** `bool`
**Pragmas:** `magic: "EqIdent"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Style insensitive comparison. b can be an identifier or a symbol. b may be wrapped in an export marker (nnkPostfix) or quoted with backticks (nnkAccQuoted), these nodes will be unwrapped.

### eqIdent

[ref: #symbol-eqident]

**Input:**
- `a: NimNode`
- `b: NimNode`

**Output:** `bool`
**Pragmas:** `magic: "EqIdent"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Style insensitive comparison. a and b can be an identifier or a symbol. Both may be wrapped in an export marker (nnkPostfix) or quoted with backticks (nnkAccQuoted), these nodes will be unwrapped.

### error

[ref: #symbol-error]

**Input:**
- `msg: string`
- `n: NimNode = nil`

**Output:** *(none)*
**Pragmas:** `magic: "NError"`, `gcsafe`, `noreturn`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Writes an error message at compile time. The optional n: NimNode parameter is used as the source for file and line number information in the compilation error message.

### expectIdent

[ref: #symbol-expectident]

**Input:**
- `n: NimNode`
- `name: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Check that eqIdent(n,name) holds true. If this is not the case, compilation aborts with an error message. This is useful for writing macros that check the AST that is passed to them.

### expectKind

[ref: #symbol-expectkind]

**Input:**
- `n: NimNode`
- `k: NimNodeKind`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks that n is of kind k. If this is not the case, compilation aborts with an error message. This is useful for writing macros that check the AST that is passed to them.

### expectKind

[ref: #symbol-expectkind]

**Input:**
- `n: NimNode`
- `k: set[NimNodeKind]`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks that n is of kind k. If this is not the case, compilation aborts with an error message. This is useful for writing macros that check the AST that is passed to them.

### expectLen

[ref: #symbol-expectlen]

**Input:**
- `n: NimNode`
- `len: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks that n has exactly len children. If this is not the case, compilation aborts with an error message. This is useful for writing macros that check its number of arguments.

### expectLen

[ref: #symbol-expectlen]

**Input:**
- `n: NimNode`
- `min: int`
- `max: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks that n has a number of children in the range min..max. If this is not the case, compilation aborts with an error message. This is useful for writing macros that check its number of arguments.

### expectMinLen

[ref: #symbol-expectminlen]

**Input:**
- `n: NimNode`
- `min: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks that n has at least min children. If this is not the case, compilation aborts with an error message. This is useful for writing macros that check its number of arguments.

### extractDocCommentsAndRunnables

[ref: #symbol-extractdoccommentsandrunnables]

returns a nnkStmtList containing the top-level doc comments and runnableExamples in a, stopping at the first child that is neither. Example:

**Input:**
- `n: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

returns a nnkStmtList containing the top-level doc comments and runnableExamples in a, stopping at the first child that is neither. Example:

```
import std/macros
macro transf(a): untyped =
  result = quote do:
    proc fun2*() = discard
  let header = extractDocCommentsAndRunnables(a.body)
  # correct usage: rest is appended
  result.body = header
  result.body.add quote do: discard # just an example
  # incorrect usage: nesting inside a nnkStmtList:
  # result.body = quote do: (`header`; discard)

proc fun*() {.transf.} =
  ## first comment
  runnableExamples: discard
  runnableExamples: discard
  ## last comment
  discard # first statement after doc comments + runnableExamples
  ## not docgen'd
```

### floatVal

[ref: #symbol-floatval]

**Input:**
- `n: NimNode`

**Output:** `BiggestFloat`
**Pragmas:** `magic: "NFloatVal"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a float from any floating point literal.

### floatVal=

[ref: #symbol-floatval]

**Input:**
- `n: NimNode`
- `val: BiggestFloat`

**Output:** *(none)*
**Pragmas:** `magic: "NSetFloatVal"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### genSym

[ref: #symbol-gensym]

**Input:**
- `kind: NimSymKind = nskLet`
- `ident:  = ""`

**Output:** `NimNode`
**Pragmas:** `magic: "NGenSym"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generates a fresh symbol that is guaranteed to be unique. The symbol needs to occur in a declaration context.


[Prev](macros_1.md) | [Next](macros_3.md)
