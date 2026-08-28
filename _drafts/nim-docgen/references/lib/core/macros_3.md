---
source_hash: 83b33519860bb86d
source_path: lib/core/macros.nim
---

### getAlign

[ref: #symbol-getalign]

**Input:**
- `arg: NimNode`

**Output:** `int`
**Pragmas:** `magic: "NSizeOf"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the same result as system.alignof if the alignment is known by the Nim compiler. It works on NimNode for use in macro context. Returns a negative value if the Nim compiler does not know the alignment.

### getAst

[ref: #symbol-getast]

Obtains the AST nodes returned from a macro or template invocation. See also genasts.genAst. Example:

**Input:**
- `macroOrTemplate: untyped`

**Output:** `NimNode`
**Pragmas:** `magic: "ExpandToAst"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Obtains the AST nodes returned from a macro or template invocation. See also genasts.genAst. Example:

```
macro FooMacro() =
  var ast = getAst(BarTemplate())
```

### getImpl

[ref: #symbol-getimpl]

**Input:**
- `symbol: NimNode`

**Output:** `NimNode`
**Pragmas:** `magic: "GetImpl"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns a copy of the declaration of a symbol or nil.

### getImpl

[ref: #symbol-getimpl]

**Input:**
- `s: NimSym`

**Output:** `NimNode`
**Pragmas:** `magic: "GetImpl"`, `noSideEffect`, `deprecated: "use `getImpl: NimNode -> NimNode` instead"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getImplTransformed

[ref: #symbol-getimpltransformed]

**Input:**
- `symbol: NimNode`

**Output:** `NimNode`
**Pragmas:** `magic: "GetImplTransf"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

For a typed proc returns the AST after transformation pass; this is useful for debugging how the compiler transforms code (e.g.: defer, for) but note that code transformations are implementation dependent and subject to change. See an example in tests/macros/tmacros\_various.nim.

### getOffset

[ref: #symbol-getoffset]

**Input:**
- `arg: NimNode`

**Output:** `int`
**Pragmas:** `magic: "NSizeOf"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the same result as system.offsetof if the offset is known by the Nim compiler. It expects a resolved symbol node from a field of a type. Therefore it only requires one argument instead of two. Returns a negative value if the Nim compiler does not know the offset.

### getProjectPath

[ref: #symbol-getprojectpath]

Returns the path to the currently compiling project.

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the path to the currently compiling project.

This is not to be confused with [system.currentSourcePath](system.html#currentSourcePath.t) which returns the path of the source file containing that template call.

For example, assume a dir1/foo.nim that imports a dir2/bar.nim, have the bar.nim print out both getProjectPath and currentSourcePath outputs.

Now when foo.nim is compiled, the getProjectPath from bar.nim will return the dir1/ path, while the currentSourcePath will return the path to the bar.nim source file.

Now when bar.nim is compiled directly, the getProjectPath will now return the dir2/ path, and the currentSourcePath will still return the same path, the path to the bar.nim source file.

The path returned by this proc is set at compile time.

See also:

* [getCurrentDir proc](os.html#getCurrentDir)

### getSize

[ref: #symbol-getsize]

**Input:**
- `arg: NimNode`

**Output:** `int`
**Pragmas:** `magic: "NSizeOf"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the same result as system.sizeof if the size is known by the Nim compiler. Returns a negative value if the Nim compiler does not know the size.

### getType

[ref: #symbol-gettype]

**Input:**
- `n: NimNode`

**Output:** `NimNode`
**Pragmas:** `magic: "NGetType"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

With 'getType' you can access the node's type. A Nim type is mapped to a Nim AST too, so it's slightly confusing but it means the same API can be used to traverse types. Recursive types are flattened for you so there is no danger of infinite recursions during traversal. To resolve recursive types, you have to call 'getType' again. To see what kind of type it is, call typeKind on getType's result.

### getType

[ref: #symbol-gettype]

**Input:**
- `n: typedesc`

**Output:** `NimNode`
**Generic parameters:** `n:type`

**Pragmas:** `magic: "NGetType"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Version of getType which takes a typedesc.

### getTypeImpl

[ref: #symbol-gettypeimpl]

**Input:**
- `n: NimNode`

**Output:** `NimNode`
**Pragmas:** `magic: "NGetType"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the type of a node in a form matching the implementation of the type. Any intermediate aliases are expanded to arrive at the final type implementation. You can instead use getImpl on a symbol if you want to find the intermediate aliases.

### getTypeImpl

[ref: #symbol-gettypeimpl]

**Input:**
- `n: typedesc`

**Output:** `NimNode`
**Generic parameters:** `n:type`

**Pragmas:** `magic: "NGetType"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Version of getTypeImpl which takes a typedesc.

### getTypeInst

[ref: #symbol-gettypeinst]

**Input:**
- `n: NimNode`

**Output:** `NimNode`
**Pragmas:** `magic: "NGetType"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the type of a node in a form matching the way the type instance was declared in the code.

### getTypeInst

[ref: #symbol-gettypeinst]

**Input:**
- `n: typedesc`

**Output:** `NimNode`
**Generic parameters:** `n:type`

**Pragmas:** `magic: "NGetType"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Version of getTypeInst which takes a typedesc.

### hasArgOfName

[ref: #symbol-hasargofname]

**Input:**
- `params: NimNode`
- `name: string`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Search nnkFormalParams for an argument.

### hint

[ref: #symbol-hint]

**Input:**
- `msg: string`
- `n: NimNode = nil`

**Output:** *(none)*
**Pragmas:** `magic: "NHint"`, `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Writes a hint message at compile time.

### ident

[ref: #symbol-ident]

**Input:**
- `n: NimNode`

**Output:** `NimIdent`
**Pragmas:** `magic: "NIdent"`, `noSideEffect`, `deprecated: "Deprecated since version 0.18.1; All functionality is defined on \'NimNode\'."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ident

[ref: #symbol-ident]

**Input:**
- `name: string`

**Output:** `NimNode`
**Pragmas:** `magic: "StrToIdent"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new ident node from a string.

### ident=

[ref: #symbol-ident]

**Input:**
- `n: NimNode`
- `val: NimIdent`

**Output:** *(none)*
**Pragmas:** `magic: "NSetIdent"`, `noSideEffect`, `deprecated: "Deprecated since version 0.18.1; Generate a new \'NimNode\' with \'ident(string)\' instead."`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### infix

[ref: #symbol-infix]

**Input:**
- `a: NimNode`
- `op: string`
- `b: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### insert

[ref: #symbol-insert]

**Input:**
- `a: NimNode`
- `pos: int`
- `b: NimNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Insert node b into node a at pos.

### internalErrorFlag

[ref: #symbol-internalerrorflag]

**Input:**
- *(none)*

**Output:** `string`
**Pragmas:** `magic: "NError"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Some builtins set an error flag. This is then turned into a proper exception. **Note**: Ordinary application code should not call this.

### intVal

[ref: #symbol-intval]

**Input:**
- `n: NimNode`

**Output:** `BiggestInt`
**Pragmas:** `magic: "NIntVal"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns an integer value from any integer literal or enum field symbol.

### intVal=

[ref: #symbol-intval]

**Input:**
- `n: NimNode`
- `val: BiggestInt`

**Output:** *(none)*
**Pragmas:** `magic: "NSetIntVal"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### isExported

[ref: #symbol-isexported]

**Input:**
- `n: NimNode`

**Output:** `bool`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns whether the symbol is exported or not.

### isInstantiationOf

[ref: #symbol-isinstantiationof]

**Input:**
- `instanceProcSym: NimNode`
- `genProcSym: NimNode`

**Output:** `bool`
**Pragmas:** `magic: "SymIsInstantiationOf"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Checks if a proc symbol is an instance of the generic proc symbol. Useful to check proc symbols against generic symbols returned by bindSym.

### kind

[ref: #symbol-kind]

**Input:**
- `n: NimNode`

**Output:** `NimNodeKind`
**Pragmas:** `magic: "NKind"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the kind of the node n.

### last

[ref: #symbol-last]

**Input:**
- `node: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Return the last item in nodes children. Same as node[^1].

### len

[ref: #symbol-len]

**Input:**
- `n: NimNode`

**Output:** `int`
**Pragmas:** `magic: "NLen"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the number of children of n.

### lineInfo

[ref: #symbol-lineinfo]

**Input:**
- `arg: NimNode`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Return line info in the form filepath(line, column).

### lineInfoObj

[ref: #symbol-lineinfoobj]

**Input:**
- `n: NimNode`

**Output:** `LineInfo`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns LineInfo of n, using absolute path for filename.

### lispRepr

[ref: #symbol-lisprepr]

Convert the AST n to a human-readable lisp-like string.

**Input:**
- `n: NimNode`
- `indented:  = false`

**Output:** `string`
**Pragmas:** `gcsafe`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Convert the AST n to a human-readable lisp-like string.

See also repr, [treeRepr](#treeRepr), and [astGenRepr](#astGenRepr).

### name

[ref: #symbol-name]

**Input:**
- `someProc: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### name=

[ref: #symbol-name]

**Input:**
- `someProc: NimNode`
- `val: NimNode`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### nestList

[ref: #symbol-nestlist]

**Input:**
- `op: NimNode`
- `pack: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Nests the list pack into a tree of call expressions: [a, b, c] is transformed into op(a, op(c, d)). This is also known as fold expression.

### nestList

[ref: #symbol-nestlist]

**Input:**
- `op: NimNode`
- `pack: NimNode`
- `init: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Nests the list pack into a tree of call expressions: [a, b, c] is transformed into op(a, op(c, d)). This is also known as fold expression.

### newAssignment

[ref: #symbol-newassignment]

**Input:**
- `lhs: NimNode`
- `rhs: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### newBlockStmt

[ref: #symbol-newblockstmt]

**Input:**
- `label: NimNode`
- `body: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new block statement with label.

### newBlockStmt

[ref: #symbol-newblockstmt]

**Input:**
- `body: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new block: stmt.

### newCall

[ref: #symbol-newcall]

**Input:**
- `theProc: NimNode`
- `args: varargs[NimNode]`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new call node. theProc is the proc that is called with the arguments args[0..].

### newCall

[ref: #symbol-newcall]

**Input:**
- `theProc: NimIdent`
- `args: varargs[NimNode]`

**Output:** `NimNode`
**Pragmas:** `deprecated: "Deprecated since v0.18.1; use \'newCall(string, ...)\' or \'newCall(NimNode, ...)\' instead"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new call node. theProc is the proc that is called with the arguments args[0..].

### newCall

[ref: #symbol-newcall]

**Input:**
- `theProc: string`
- `args: varargs[NimNode]`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new call node. theProc is the proc that is called with the arguments args[0..].

### newColonExpr

[ref: #symbol-newcolonexpr]

**Input:**
- `a: NimNode`
- `b: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create new colon expression. newColonExpr(a, b) -> a: b

### newCommentStmtNode

[ref: #symbol-newcommentstmtnode]

**Input:**
- `s: string`

**Output:** `NimNode`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a comment statement node.

### newConstStmt

[ref: #symbol-newconststmt]

**Input:**
- `name: NimNode`
- `value: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new const stmt.

### newDotExpr

[ref: #symbol-newdotexpr]

**Input:**
- `a: NimNode`
- `b: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create new dot expression. a.dot(b) -> a.b

### newEmptyNode

[ref: #symbol-newemptynode]

**Input:**
- *(none)*

**Output:** `NimNode`
**Pragmas:** `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new empty node.

### newEnum

[ref: #symbol-newenum]

Creates a new enum. name must be an ident. Fields are allowed to be either idents or EnumFieldDef:

**Input:**
- `name: NimNode`
- `fields: openArray[NimNode]`
- `public: bool`
- `pure: bool`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new enum. name must be an ident. Fields are allowed to be either idents or EnumFieldDef:

```
newEnum(
  name    = ident("Colors"),
  fields  = [ident("Blue"), ident("Red")],
  public  = true, pure = false)

# type Colors* = Blue Red
```

### newFloatLitNode

[ref: #symbol-newfloatlitnode]

**Input:**
- `f: BiggestFloat`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a float literal node from f.

### newIdentDefs

[ref: #symbol-newidentdefs]

Creates a new nnkIdentDefs node of a specific kind and value.

**Input:**
- `name: NimNode`
- `kind: NimNode`
- `default:  = newEmptyNode()`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a new nnkIdentDefs node of a specific kind and value.

nnkIdentDefs need to have at least three children, but they can have more: first comes a list of identifiers followed by a type and value nodes. This helper proc creates a three node subtree, the first subnode being a single identifier name. Both the kind node and default (value) nodes may be empty depending on where the nnkIdentDefs appears: tuple or object definitions will have an empty default node, let or var blocks may have an empty kind node if the identifier is being assigned a value. Example:

```
var varSection = newNimNode(nnkVarSection).add(
  newIdentDefs(ident("a"), ident("string")),
  newIdentDefs(ident("b"), newEmptyNode(), newLit(3)))
# --> var
#       a: string
#       b = 3
```

If you need to create multiple identifiers you need to use the lower level newNimNode:

```
result = newNimNode(nnkIdentDefs).add(
  ident("a"), ident("b"), ident("c"), ident("string"),
    newStrLitNode("Hello"))
```

### newIdentNode

[ref: #symbol-newidentnode]

**Input:**
- `i: NimIdent`

**Output:** `NimNode`
**Pragmas:** `deprecated: "use ident(string)"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates an identifier node from i.

### newIdentNode

[ref: #symbol-newidentnode]

**Input:**
- `i: string`

**Output:** `NimNode`
**Pragmas:** `magic: "StrToIdent"`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates an identifier node from i. It is simply an alias for ident(string). Use that, it's shorter.

### newIfStmt

[ref: #symbol-newifstmt]

Constructor for if statements.

**Input:**
- `branches: varargs[tuple[cond, body: NimNode]]`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Constructor for if statements.

```
newIfStmt(
  (Ident, StmtList),
  ...
)
```

### newIntLitNode

[ref: #symbol-newintlitnode]

**Input:**
- `i: BiggestInt`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates an int literal node from i.

### newLetStmt

[ref: #symbol-newletstmt]

**Input:**
- `name: NimNode`
- `value: NimNode`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Create a new let stmt.

### newLit

[ref: #symbol-newlit]

**Input:**
- `c: char`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new character literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `i: int`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new integer literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `i: int8`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new integer literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `i: int16`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new integer literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `i: int32`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new integer literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `i: int64`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new integer literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `i: uint`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new unsigned integer literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `i: uint8`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new unsigned integer literal node.

### newLit

[ref: #symbol-newlit]

**Input:**
- `i: uint16`

**Output:** `NimNode`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Produces a new unsigned integer literal node.


[Prev](macros_2.md) | [Next](macros_4.md)
