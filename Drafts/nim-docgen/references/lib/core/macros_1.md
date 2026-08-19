---
source_hash: 83b33519860bb86d
source_path: lib/core/macros.nim
---

# macros

[ref: #module-macros]

This module contains the interface to the compiler's abstract syntax tree (AST). Macros operate on this tree.

See also:

* [macros tutorial](tut3.html)
* [macros section in Nim manual](manual.html#macros)

# [The AST in Nim](#the-ast-in-nim)

This section describes how the AST is modelled with Nim's type system. The AST consists of nodes (NimNode) with a variable number of children. Each node has a field named kind which describes what the node contains:

```
type
  NimNodeKind = enum     ## kind of a node; only explanatory
    nnkNone,             ## invalid node kind
    nnkEmpty,            ## empty node
    nnkIdent,            ## node contains an identifier
    nnkIntLit,           ## node contains an int literal (example: 10)
    nnkStrLit,           ## node contains a string literal (example: "abc")
    nnkNilLit,           ## node contains a nil literal (example: nil)
    nnkCaseStmt,         ## node represents a case statement
    ...                  ## many more
  
  NimNode = ref NimNodeObj
  NimNodeObj = object
    case kind: NimNodeKind           ## the node's kind
    of nnkNone, nnkEmpty, nnkNilLit:
      discard                        ## node contains no additional fields
    of nnkCharLit..nnkUInt64Lit:
      intVal: BiggestInt             ## the int literal
    of nnkFloatLit..nnkFloat64Lit:
      floatVal: BiggestFloat         ## the float literal
    of nnkStrLit..nnkTripleStrLit, nnkCommentStmt, nnkIdent, nnkSym:
      strVal: string                 ## the string literal
    else:
      sons: seq[NimNode]             ## the node's sons (or children)
```

For the NimNode type, the [] operator has been overloaded: n[i] is n's i-th child.

To specify the AST for the different Nim constructs, the notation nodekind(son1, son2, ...) or nodekind(value) or nodekind(field=value) is used.

Some child may be missing. A missing child is a node of kind nnkEmpty; a child can never be nil.

# [Leaf nodes/Atoms](#leaf-nodesslashatoms)

A leaf of the AST often corresponds to a terminal symbol in the concrete syntax. Note that the default float in Nim maps to float64 such that the default AST for a float is nnkFloat64Lit as below.

| Nim expression | Corresponding AST |
| --- | --- |
| 42 | nnkIntLit(intVal = 42) |
| 42'i8 | nnkInt8Lit(intVal = 42) |
| 42'i16 | nnkInt16Lit(intVal = 42) |
| 42'i32 | nnkInt32Lit(intVal = 42) |
| 42'i64 | nnkInt64Lit(intVal = 42) |
| 42'u8 | nnkUInt8Lit(intVal = 42) |
| 42'u16 | nnkUInt16Lit(intVal = 42) |
| 42'u32 | nnkUInt32Lit(intVal = 42) |
| 42'u64 | nnkUInt64Lit(intVal = 42) |
| 42.0 | nnkFloat64Lit(floatVal = 42.0) |
| 42.0'f32 | nnkFloat32Lit(floatVal = 42.0) |
| 42.0'f64 | nnkFloat64Lit(floatVal = 42.0) |
| "abc" | nnkStrLit(strVal = "abc") |
| r"abc" | nnkRStrLit(strVal = "abc") |
| """abc""" | nnkTripleStrLit(strVal = "abc") |
| ' ' | nnkCharLit(intVal = 32) |
| nil | nnkNilLit() |
| myIdentifier | nnkIdent(strVal = "myIdentifier") |
| myIdentifier | after lookup pass: nnkSym(strVal = "myIdentifier", ...) |

Identifiers are nnkIdent nodes. After the name lookup pass these nodes get transferred into nnkSym nodes.

# [Calls/expressions](#callsslashexpressions)

## [Command call](#callsslashexpressions-command-call)

Concrete syntax:

```
echo "abc", "xyz"
```

AST:

```
nnkCommand(
  nnkIdent("echo"),
  nnkStrLit("abc"),
  nnkStrLit("xyz")
)
```

## [Call with ()](#callsslashexpressions-call-with)

Concrete syntax:

```
echo("abc", "xyz")
```

AST:

```
nnkCall(
  nnkIdent("echo"),
  nnkStrLit("abc"),
  nnkStrLit("xyz")
)
```

## [Infix operator call](#callsslashexpressions-infix-operator-call)

Concrete syntax:

```
"abc" & "xyz"
```

AST:

```
nnkInfix(
  nnkIdent("&"),
  nnkStrLit("abc"),
  nnkStrLit("xyz")
)
```

Note that with multiple infix operators, the command is parsed by operator precedence.

Concrete syntax:

```
5 + 3 * 4
```

AST:

```
nnkInfix(
  nnkIdent("+"),
  nnkIntLit(5),
  nnkInfix(
    nnkIdent("*"),
    nnkIntLit(3),
    nnkIntLit(4)
  )
)
```

As a side note, if you choose to use infix operators in a prefix form, the AST behaves as a [parenthetical function call](#callsslashexpressions-call-with) with nnkAccQuoted, as follows:

Concrete syntax:

```
`+`(3, 4)
```

AST:

```
nnkCall(
  nnkAccQuoted(
    nnkIdent("+")
  ),
  nnkIntLit(3),
  nnkIntLit(4)
)
```

## [Prefix operator call](#callsslashexpressions-prefix-operator-call)

Concrete syntax:

```
? "xyz"
```

AST:

```
nnkPrefix(
  nnkIdent("?"),
  nnkStrLit("abc")
)
```

## [Postfix operator call](#callsslashexpressions-postfix-operator-call)

**Note:** There are no postfix operators in Nim. However, the nnkPostfix node is used for the *asterisk export marker* \*:

Concrete syntax:

```
identifier*
```

AST:

```
nnkPostfix(
  nnkIdent("*"),
  nnkIdent("identifier")
)
```

## [Call with named arguments](#callsslashexpressions-call-with-named-arguments)

Concrete syntax:

```
writeLine(file=stdout, "hallo")
```

AST:

```
nnkCall(
  nnkIdent("writeLine"),
  nnkExprEqExpr(
    nnkIdent("file"),
    nnkIdent("stdout")
  ),
  nnkStrLit("hallo")
)
```

## [Call with raw string literal](#callsslashexpressions-call-with-raw-string-literal)

This is used, for example, in the bindSym examples [here](manual.html#macros-bindsym) and with re"some regexp" in the regular expression module.

Concrete syntax:

```
echo"abc"
```

AST:

```
nnkCallStrLit(
  nnkIdent("echo"),
  nnkRStrLit("hello")
)
```

## [Dereference operator []](#callsslashexpressions-dereference-operator)

Concrete syntax:

```
x[]
```

AST:

```
nnkDerefExpr(nnkIdent("x"))
```

## [Addr operator](#callsslashexpressions-addr-operator)

Concrete syntax:

```
addr(x)
```

AST:

```
nnkAddr(nnkIdent("x"))
```

## [Cast operator](#callsslashexpressions-cast-operator)

Concrete syntax:

```
cast[T](x)
```

AST:

```
nnkCast(nnkIdent("T"), nnkIdent("x"))
```

## [Object access operator .](#callsslashexpressions-object-access-operator-dot)

Concrete syntax:

```
x.y
```

AST:

```
nnkDotExpr(nnkIdent("x"), nnkIdent("y"))
```

If you use Nim's flexible calling syntax (as in x.len()), the result is the same as above but wrapped in an nnkCall.

## [Array access operator []](#callsslashexpressions-array-access-operator)

Concrete syntax:

```
x[y]
```

AST:

```
nnkBracketExpr(nnkIdent("x"), nnkIdent("y"))
```

## [Parentheses](#callsslashexpressions-parentheses)

Parentheses for affecting operator precedence use the nnkPar node.

Concrete syntax:

```
(a + b) * c
```

AST:

```
nnkInfix(nnkIdent("*"),
  nnkPar(
    nnkInfix(nnkIdent("+"), nnkIdent("a"), nnkIdent("b"))),
  nnkIdent("c"))
```

## [Tuple Constructors](#callsslashexpressions-tuple-constructors)

Nodes for tuple construction are built with the nnkTupleConstr node.

Concrete syntax:

```
(1, 2, 3)
(a: 1, b: 2, c: 3)
()
```

AST:

```
nnkTupleConstr(nnkIntLit(1), nnkIntLit(2), nnkIntLit(3))
nnkTupleConstr(
  nnkExprColonExpr(nnkIdent("a"), nnkIntLit(1)),
  nnkExprColonExpr(nnkIdent("b"), nnkIntLit(2)),
  nnkExprColonExpr(nnkIdent("c"), nnkIntLit(3)))
nnkTupleConstr()
```

Since the one tuple would be syntactically identical to parentheses with an expression in them, the parser expects a trailing comma for them. For tuple constructors with field names, this is not necessary.

```
(1,)
(a: 1)
```

AST:

```
nnkTupleConstr(nnkIntLit(1))
nnkTupleConstr(
  nnkExprColonExpr(nnkIdent("a"), nnkIntLit(1)))
```

## [Curly braces](#callsslashexpressions-curly-braces)

Curly braces are used as the set constructor.

Concrete syntax:

```
{1, 2, 3}
```

AST:

```
nnkCurly(nnkIntLit(1), nnkIntLit(2), nnkIntLit(3))
```

When used as a table constructor, the syntax is different.

Concrete syntax:

```
{a: 3, b: 5}
```

AST:

```
nnkTableConstr(
  nnkExprColonExpr(nnkIdent("a"), nnkIntLit(3)),
  nnkExprColonExpr(nnkIdent("b"), nnkIntLit(5))
)
```

## [Brackets](#callsslashexpressions-brackets)

Brackets are used as the array constructor.

Concrete syntax:

```
[1, 2, 3]
```

AST:

```
nnkBracket(nnkIntLit(1), nnkIntLit(2), nnkIntLit(3))
```

## [Ranges](#callsslashexpressions-ranges)

Ranges occur in set constructors, case statement branches, or array slices. Internally, the node kind nnkRange is used, but when constructing the AST, construction with .. as an infix operator should be used instead.

Concrete syntax:

```
1..3
```

AST:

```
nnkInfix(
  nnkIdent(".."),
  nnkIntLit(1),
  nnkIntLit(3)
)
```

Example code:

```
macro genRepeatEcho() =
  result = newNimNode(nnkStmtList)
  
  var forStmt = newNimNode(nnkForStmt) # generate a for statement
  forStmt.add(ident("i")) # use the variable `i` for iteration
  
  var rangeDef = newNimNode(nnkInfix).add(
    ident("..")).add(
    newIntLitNode(3),newIntLitNode(5)) # iterate over the range 3..5
  
  forStmt.add(rangeDef)
  forStmt.add(newCall(ident("echo"), newIntLitNode(3))) # meat of the loop
  result.add(forStmt)

genRepeatEcho() # gives:
                # 3
                # 3
                # 3
```

## [If expression](#callsslashexpressions-if-expression)

The representation of the if expression is subtle, but easy to traverse.

Concrete syntax:

```
if cond1: expr1 elif cond2: expr2 else: expr3
```

AST:

```
nnkIfExpr(
  nnkElifExpr(cond1, expr1),
  nnkElifExpr(cond2, expr2),
  nnkElseExpr(expr3)
)
```

## [Documentation Comments](#callsslashexpressions-documentation-comments)

Double-hash (##) comments in the code actually have their own format, using strVal to get and set the comment text. Single-hash (#) comments are ignored.

Concrete syntax:

```
## This is a comment
## This is part of the first comment
stmt1
## Yet another
```

AST:

```
nnkCommentStmt() # only appears once for the first two lines!
stmt1
nnkCommentStmt() # another nnkCommentStmt because there is another comment
                 # (separate from the first)
```

## [Pragmas](#callsslashexpressions-pragmas)

One of Nim's cool features is pragmas, which allow fine-tuning of various aspects of the language. They come in all types, such as adorning procs and objects, but the standalone emit pragma shows the basics with the AST.

Concrete syntax:

```
{.emit: "#include <stdio.h>".}
```

AST:

```
nnkPragma(
  nnkExprColonExpr(
    nnkIdent("emit"),
    nnkStrLit("#include <stdio.h>") # the "argument"
  )
)
```

As many nnkIdent appear as there are pragmas between {..}. Note that the declaration of new pragmas is essentially the same:

Concrete syntax:

```
{.pragma: cdeclRename, cdecl.}
```

AST:

```
nnkPragma(
  nnkExprColonExpr(
    nnkIdent("pragma"), # this is always first when declaring a new pragma
    nnkIdent("cdeclRename") # the name of the pragma
  ),
  nnkIdent("cdecl")
)
```

# [Statements](#statements)

## [If statement](#statements-if-statement)

The representation of the if statement is subtle, but easy to traverse. If there is no else branch, no nnkElse child exists.

Concrete syntax:

```
if cond1:
  stmt1
elif cond2:
  stmt2
elif cond3:
  stmt3
else:
  stmt4
```

AST:

```
nnkIfStmt(
  nnkElifBranch(cond1, stmt1),
  nnkElifBranch(cond2, stmt2),
  nnkElifBranch(cond3, stmt3),
  nnkElse(stmt4)
)
```

## [When statement](#statements-when-statement)

Like the if statement, but the root has the kind nnkWhenStmt.

## [Assignment](#statements-assignment)

Concrete syntax:

```
x = 42
```

AST:

```
nnkAsgn(nnkIdent("x"), nnkIntLit(42))
```

This is not the syntax for assignment when combined with var, let, or const.

## [Statement list](#statements-statement-list)

Concrete syntax:

```
stmt1
stmt2
stmt3
```

AST:

```
nnkStmtList(stmt1, stmt2, stmt3)
```

## [Case statement](#statements-case-statement)

Concrete syntax:

```
case expr1
of expr2, expr3..expr4:
  stmt1
of expr5:
  stmt2
elif cond1:
  stmt3
else:
  stmt4
```

AST:

```
nnkCaseStmt(
  expr1,
  nnkOfBranch(expr2, nnkRange(expr3, expr4), stmt1),
  nnkOfBranch(expr5, stmt2),
  nnkElifBranch(cond1, stmt3),
  nnkElse(stmt4)
)
```

The nnkElifBranch and nnkElse parts may be missing.

## [While statement](#statements-while-statement)

Concrete syntax:

```
while expr1:
  stmt1
```

AST:

```
nnkWhileStmt(expr1, stmt1)
```

## [For statement](#statements-for-statement)

Concrete syntax:

```
for ident1, ident2 in expr1:
  stmt1
```

AST:

```
nnkForStmt(ident1, ident2, expr1, stmt1)
```

## [Try statement](#statements-try-statement)

Concrete syntax:

```
try:
  stmt1
except e1, e2:
  stmt2
except e3:
  stmt3
except:
  stmt4
finally:
  stmt5
```

AST:

```
nnkTryStmt(
  stmt1,
  nnkExceptBranch(e1, e2, stmt2),
  nnkExceptBranch(e3, stmt3),
  nnkExceptBranch(stmt4),
  nnkFinally(stmt5)
)
```

## [Return statement](#statements-return-statement)

Concrete syntax:

```
return expr1
```

AST:

```
nnkReturnStmt(expr1)
```

## [Yield statement](#statements-yield-statement)

Like return, but with nnkYieldStmt kind.

```
nnkYieldStmt(expr1)
```

## [Discard statement](#statements-discard-statement)

Like return, but with nnkDiscardStmt kind.

```
nnkDiscardStmt(expr1)
```

## [Continue statement](#statements-continue-statement)

Concrete syntax:

```
continue
```

AST:

```
nnkContinueStmt()
```

## [Break statement](#statements-break-statement)

Concrete syntax:

```
break otherLocation
```

AST:

```
nnkBreakStmt(nnkIdent("otherLocation"))
```

If break is used without a jump-to location, nnkEmpty replaces nnkIdent.

## [Block statement](#statements-block-statement)

Concrete syntax:

```
block name:
```

AST:

```
nnkBlockStmt(nnkIdent("name"), nnkStmtList(...))
```

A block doesn't need an name, in which case nnkEmpty is used.

## [Asm statement](#statements-asm-statement)

Concrete syntax:

```
asm """
  some asm
"""
```

AST:

```
nnkAsmStmt(
  nnkEmpty(), # for pragmas
  nnkTripleStrLit("some asm"),
)
```

## [Import section](#statements-import-section)

Nim's import statement actually takes different variations depending on what keywords are present. Let's start with the simplest form.

Concrete syntax:

```
import std/math
```

AST:

```
nnkImportStmt(nnkIdent("math"))
```

With except, we get nnkImportExceptStmt.

Concrete syntax:

```
import std/math except pow
```

AST:

```
nnkImportExceptStmt(nnkIdent("math"),nnkIdent("pow"))
```

Note that import std/math as m does not use a different node; rather, we use nnkImportStmt with as as an infix operator.

Concrete syntax:

```
import std/strutils as su
```

AST:

```
nnkImportStmt(
  nnkInfix(
    nnkIdent("as"),
    nnkIdent("strutils"),
    nnkIdent("su")
  )
)
```

## [From statement](#statements-from-statement)

If we use from ... import, the result is different, too.

Concrete syntax:

```
from std/math import pow
```

AST:

```
nnkFromStmt(nnkIdent("math"), nnkIdent("pow"))
```

Using from std/math as m import pow works identically to the as modifier with the import statement, but wrapped in nnkFromStmt.

## [Export statement](#statements-export-statement)

When you are making an imported module accessible by modules that import yours, the export syntax is pretty straightforward.

Concrete syntax:

```
export unsigned
```

AST:

```
nnkExportStmt(nnkIdent("unsigned"))
```

Similar to the import statement, the AST is different for export ... except.

Concrete syntax:

```
export math except pow # we're going to implement our own exponentiation
```

AST:

```
nnkExportExceptStmt(nnkIdent("math"),nnkIdent("pow"))
```

## [Include statement](#statements-include-statement)

Like a plain import statement but with nnkIncludeStmt.

Concrete syntax:

```
include blocks
```

AST:

```
nnkIncludeStmt(nnkIdent("blocks"))
```

## [Var section](#statements-var-section)

Concrete syntax:

```
var a = 3
```

AST:

```
nnkVarSection(
  nnkIdentDefs(
    nnkIdent("a"),
    nnkEmpty(), # or nnkIdent(...) if the variable declares the type
    nnkIntLit(3),
  )
)
```

Note that either the second or third (or both) parameters above must exist, as the compiler needs to know the type somehow (which it can infer from the given assignment).

This is not the same AST for all uses of var. See [Procedure declaration](macros.html#statements-procedure-declaration) for details.

## [Let section](#statements-let-section)

This is equivalent to var, but with nnkLetSection rather than nnkVarSection.

Concrete syntax:

```
let a = 3
```

AST:

```
nnkLetSection(
  nnkIdentDefs(
    nnkIdent("a"),
    nnkEmpty(), # or nnkIdent(...) for the type
    nnkIntLit(3),
  )
)
```

## [Const section](#statements-const-section)

Concrete syntax:

```
const a = 3
```

AST:

```
nnkConstSection(
  nnkConstDef( # not nnkConstDefs!
    nnkIdent("a"),
    nnkEmpty(), # or nnkIdent(...) if the variable declares the type
    nnkIntLit(3), # required in a const declaration!
  )
)
```

## [Type section](#statements-type-section)

Starting with the simplest case, a type section appears much like var and const.

Concrete syntax:

```
type A = int
```

AST:

```
nnkTypeSection(
  nnkTypeDef(
    nnkIdent("A"),
    nnkEmpty(),
    nnkIdent("int")
  )
)
```

Declaring distinct types is similar, with the last nnkIdent wrapped in nnkDistinctTy.

Concrete syntax:

```
type MyInt = distinct int
```

AST:

```
# ...
nnkTypeDef(
  nnkIdent("MyInt"),
  nnkEmpty(),
  nnkDistinctTy(
    nnkIdent("int")
  )
)
```

If a type section uses generic parameters, they are treated here:

Concrete syntax:

```
type A[T] = expr1
```

AST:

```
nnkTypeSection(
  nnkTypeDef(
    nnkIdent("A"),
    nnkGenericParams(
      nnkIdentDefs(
        nnkIdent("T"),
        nnkEmpty(), # if the type is declared with options, like
                    # ``[T: SomeInteger]``, they are given here
        nnkEmpty(),
      )
    )
    expr1,
  )
)
```

Note that not all nnkTypeDef utilize nnkIdent as their parameter. One of the most common uses of type declarations is to work with objects.

Concrete syntax:

```
type IO = object of RootObj
```

AST:

```
# ...
nnkTypeDef(
  nnkIdent("IO"),
  nnkEmpty(),
  nnkObjectTy(
    nnkEmpty(), # no pragmas here
    nnkOfInherit(
      nnkIdent("RootObj") # inherits from RootObj
    ),
    nnkEmpty()
  )
)
```

Nim's object syntax is rich. Let's take a look at an involved example in its entirety to see some of the complexities.

Concrete syntax:

```
type Obj[T] {.inheritable.} = object
  name: string
  case isFat: bool
  of true:
    m: array[100_000, T]
  of false:
    m: array[10, T]
```

AST:

```
# ...
nnkPragmaExpr(
  nnkIdent("Obj"),
  nnkPragma(nnkIdent("inheritable"))
),
nnkGenericParams(
nnkIdentDefs(
  nnkIdent("T"),
  nnkEmpty(),
  nnkEmpty())
),
nnkObjectTy(
  nnkEmpty(),
  nnkEmpty(),
  nnkRecList( # list of object parameters
    nnkIdentDefs(
      nnkIdent("name"),
      nnkIdent("string"),
      nnkEmpty()
    ),
    nnkRecCase( # case statement within object (not nnkCaseStmt)
      nnkIdentDefs(
        nnkIdent("isFat"),
        nnkIdent("bool"),
        nnkEmpty()
      ),
      nnkOfBranch(
        nnkIdent("true"),
        nnkRecList( # again, a list of object parameters
          nnkIdentDefs(
            nnkIdent("m"),
            nnkBracketExpr(
              nnkIdent("array"),
              nnkIntLit(100000),
              nnkIdent("T")
            ),
            nnkEmpty()
        )
      ),
      nnkOfBranch(
        nnkIdent("false"),
        nnkRecList(
          nnkIdentDefs(
            nnkIdent("m"),
            nnkBracketExpr(
              nnkIdent("array"),
              nnkIntLit(10),
              nnkIdent("T")
            ),
            nnkEmpty()
          )
        )
      )
    )
  )
)
```

Using an enum is similar to using an object.

Concrete syntax:

```
type X = enum
  First
```

AST:

```
# ...
nnkEnumTy(
  nnkEmpty(),
  nnkIdent("First") # you need at least one nnkIdent or the compiler complains
)
```

The usage of concept (experimental) is similar to objects.

Concrete syntax:

```
type Con = concept x,y,z
  (x & y & z) is string
```

AST:

```
# ...
nnkTypeClassTy( # note this isn't nnkConceptTy!
  nnkArgList(
    # ... idents for x, y, z
  )
  # ...
)
```

Static types, like static[int], use nnkIdent wrapped in nnkStaticTy.

Concrete syntax:

```
type A[T: static[int]] = object
```

AST:

```
# ... within nnkGenericParams
nnkIdentDefs(
  nnkIdent("T"),
  nnkStaticTy(
    nnkIdent("int")
  ),
  nnkEmpty()
)
# ...
```

In general, declaring types mirrors this syntax (i.e., nnkStaticTy for static, etc.). Examples follow (exceptions marked by \*):

| Nim type | Corresponding AST |
| --- | --- |
| static | nnkStaticTy |
| tuple | nnkTupleTy |
| var | nnkVarTy |
| ptr | nnkPtrTy |
| ref | nnkRefTy |
| distinct | nnkDistinctTy |
| enum | nnkEnumTy |
| concept | nnkTypeClassTy\* |
| array | nnkBracketExpr(nnkIdent("array"),...\* |
| proc | nnkProcTy |
| iterator | nnkIteratorTy |
| object | nnkObjectTy |

Take special care when declaring types as proc. The behavior is similar to Procedure declaration, below, but does not treat nnkGenericParams. Generic parameters are treated in the type, not the proc itself.

Concrete syntax:

```
type MyProc[T] = proc(x: T) {.nimcall.}
```

AST:

```
# ...
nnkTypeDef(
  nnkIdent("MyProc"),
  nnkGenericParams( # here, not with the proc
    # ...
  )
  nnkProcTy( # behaves like a procedure declaration from here on
    nnkFormalParams(
      # ...
    ),
    nnkPragma(nnkIdent("nimcall"))
  )
)
```

The same syntax applies to iterator (with nnkIteratorTy), but *does not* apply to converter or template.

Type class versions of these nodes generally share the same node kind but without any child nodes. The tuple type class is represented by nnkTupleClassTy, while a proc or iterator type class with pragmas has an nnkEmpty node in place of the nnkFormalParams node of a concrete proc or iterator type node.

```
type TypeClass = proc {.nimcall.} | ref | tuple
```

AST:

```
nnkTypeDef(
  nnkIdent("TypeClass"),
  nnkEmpty(),
  nnkInfix(
    nnkIdent("|"),
    nnkProcTy(
      nnkEmpty(),
      nnkPragma(nnkIdent("nimcall"))
    ),
    nnkInfix(
      nnkIdent("|"),
      nnkRefTy(),
      nnkTupleClassTy()
    )
  )
)
```

## [Mixin statement](#statements-mixin-statement)

Concrete syntax:

```
mixin x
```

AST:

```
nnkMixinStmt(nnkIdent("x"))
```

## [Bind statement](#statements-bind-statement)

Concrete syntax:

```
bind x
```

AST:

```
nnkBindStmt(nnkIdent("x"))
```

## [Procedure declaration](#statements-procedure-declaration)

Let's take a look at a procedure with a lot of interesting aspects to get a feel for how procedure calls are broken down.

Concrete syntax:

```
proc hello*[T: SomeInteger](x: int = 3, y: float32): int {.inline.} = discard
```

AST:

```
nnkProcDef(
  nnkPostfix(nnkIdent("*"), nnkIdent("hello")), # the exported proc name
  nnkEmpty(), # patterns for term rewriting in templates and macros (not procs)
  nnkGenericParams( # generic type parameters, like with type declaration
    nnkIdentDefs(
      nnkIdent("T"),
      nnkIdent("SomeInteger"),
      nnkEmpty()
    )
  ),
  nnkFormalParams(
    nnkIdent("int"), # the first FormalParam is the return type. nnkEmpty() if there is none
    nnkIdentDefs(
      nnkIdent("x"),
      nnkIdent("int"), # type type (required for procs, not for templates)
      nnkIntLit(3) # a default value
    ),
    nnkIdentDefs(
      nnkIdent("y"),
      nnkIdent("float32"),
      nnkEmpty()
    )
  ),
  nnkPragma(nnkIdent("inline")),
  nnkEmpty(), # reserved slot for future use
  nnkStmtList(nnkDiscardStmt(nnkEmpty())) # the meat of the proc
)
```

There is another consideration. Nim has flexible type identification for its procs. Even though proc(a: int, b: int) and proc(a, b: int) are equivalent in the code, the AST is a little different for the latter.

Concrete syntax:

```
proc(a, b: int)
```

AST:

```
# ...AST as above...
nnkFormalParams(
  nnkEmpty(), # no return here
  nnkIdentDefs(
    nnkIdent("a"), # the first parameter
    nnkIdent("b"), # directly to the second parameter
    nnkIdent("int"), # their shared type identifier
    nnkEmpty(), # default value would go here
  )
),
# ...
```

When a procedure uses the special var type return variable, the result is different from that of a var section.

Concrete syntax:

```
proc hello(): var int
```

AST:

```
# ...
nnkFormalParams(
  nnkVarTy(
    nnkIdent("int")
  )
)
```

## [Iterator declaration](#statements-iterator-declaration)

The syntax for iterators is similar to procs, but with nnkIteratorDef replacing nnkProcDef.

Concrete syntax:

```
iterator nonsense[T](x: seq[T]): float {.closure.} = ...
```

AST:

```
nnkIteratorDef(
  nnkIdent("nonsense"),
  nnkEmpty(),
  ...
)
```

## [Converter declaration](#statements-converter-declaration)

A converter is similar to a proc.

Concrete syntax:

```
converter toBool(x: float): bool
```

AST:

```
nnkConverterDef(
  nnkIdent("toBool"),
  # ...
)
```

## [Template declaration](#statements-template-declaration)

Templates (as well as macros, as we'll see) have a slightly expanded AST when compared to procs and iterators. The reason for this is [term-rewriting macros](manual.html#term-rewriting-macros). Notice the nnkEmpty() as the second argument to nnkProcDef and nnkIteratorDef above? That's where the term-rewriting macros go.

Concrete syntax:

```
template optOpt{expr1}(a: int): int
```

AST:

```
nnkTemplateDef(
  nnkIdent("optOpt"),
  nnkStmtList( # instead of nnkEmpty()
    expr1
  ),
  # follows like a proc or iterator
)
```

If the template does not have types for its parameters, the type identifiers inside nnkFormalParams just becomes nnkEmpty.

## [Macro declaration](#statements-macro-declaration)

Macros behave like templates, but nnkTemplateDef is replaced with nnkMacroDef.

## [Hidden Standard Conversion](#statements-hidden-standard-conversion)

```
var f: float = 1
```

The type of "f" is float but the type of "1" is actually int. Inserting int into a float is a type error. Nim inserts the nnkHiddenStdConv node around the nnkIntLit node so that the new node has the correct type of float. This works for any auto converted nodes and makes the conversion explicit.

# [Special node kinds](#special-node-kinds)

There are several node kinds that are used for semantic checking or code generation. These are accessible from this module, but should not be used. Other node kinds are especially designed to make AST manipulations easier. These are explained here.

To be written.

## Examples

```nim
type
  NimNodeKind = enum     ## kind of a node; only explanatory
    nnkNone,             ## invalid node kind
    nnkEmpty,            ## empty node
    nnkIdent,            ## node contains an identifier
    nnkIntLit,           ## node contains an int literal (example: 10)
    nnkStrLit,           ## node contains a string literal (example: "abc")
    nnkNilLit,           ## node contains a nil literal (example: nil)
    nnkCaseStmt,         ## node represents a case statement
    ...                  ## many more
  
  NimNode = ref NimNodeObj
  NimNodeObj = object
    case kind: NimNodeKind           ## the node's kind
    of nnkNone, nnkEmpty, nnkNilLit:
      discard                        ## node contains no additional fields
    of nnkCharLit..nnkUInt64Lit:
      intVal: BiggestInt             ## the int literal
    of nnkFloatLit..nnkFloat64Lit:
      floatVal: BiggestFloat         ## the float literal
    of nnkStrLit..nnkTripleStrLit, nnkCommentStmt, nnkIdent, nnkSym:
      strVal: string                 ## the string literal
    else:
      sons: seq[NimNode]             ## the node's sons (or children)
```

```nim
echo "abc", "xyz"
```

```nim
nnkCommand(
  nnkIdent("echo"),
  nnkStrLit("abc"),
  nnkStrLit("xyz")
)
```

```nim
echo("abc", "xyz")
```

```nim
nnkCall(
  nnkIdent("echo"),
  nnkStrLit("abc"),
  nnkStrLit("xyz")
)
```

```nim
"abc" & "xyz"
```

```nim
nnkInfix(
  nnkIdent("&"),
  nnkStrLit("abc"),
  nnkStrLit("xyz")
)
```

```nim
5 + 3 * 4
```

```nim
nnkInfix(
  nnkIdent("+"),
  nnkIntLit(5),
  nnkInfix(
    nnkIdent("*"),
    nnkIntLit(3),
    nnkIntLit(4)
  )
)
```

```nim
`+`(3, 4)
```

```nim
nnkCall(
  nnkAccQuoted(
    nnkIdent("+")
  ),
  nnkIntLit(3),
  nnkIntLit(4)
)
```

```nim
? "xyz"
```

```nim
nnkPrefix(
  nnkIdent("?"),
  nnkStrLit("abc")
)
```

```nim
identifier*
```

```nim
nnkPostfix(
  nnkIdent("*"),
  nnkIdent("identifier")
)
```

```nim
writeLine(file=stdout, "hallo")
```

```nim
nnkCall(
  nnkIdent("writeLine"),
  nnkExprEqExpr(
    nnkIdent("file"),
    nnkIdent("stdout")
  ),
  nnkStrLit("hallo")
)
```

```nim
echo"abc"
```

```nim
nnkCallStrLit(
  nnkIdent("echo"),
  nnkRStrLit("hello")
)
```

```nim
x[]
```

```nim
nnkDerefExpr(nnkIdent("x"))
```

```nim
addr(x)
```

```nim
nnkAddr(nnkIdent("x"))
```

```nim
cast[T](x)
```

```nim
nnkCast(nnkIdent("T"), nnkIdent("x"))
```

```nim
x.y
```

```nim
nnkDotExpr(nnkIdent("x"), nnkIdent("y"))
```

```nim
x[y]
```

```nim
nnkBracketExpr(nnkIdent("x"), nnkIdent("y"))
```

```nim
(a + b) * c
```

```nim
nnkInfix(nnkIdent("*"),
  nnkPar(
    nnkInfix(nnkIdent("+"), nnkIdent("a"), nnkIdent("b"))),
  nnkIdent("c"))
```

```nim
(1, 2, 3)
(a: 1, b: 2, c: 3)
()
```

```nim
nnkTupleConstr(nnkIntLit(1), nnkIntLit(2), nnkIntLit(3))
nnkTupleConstr(
  nnkExprColonExpr(nnkIdent("a"), nnkIntLit(1)),
  nnkExprColonExpr(nnkIdent("b"), nnkIntLit(2)),
  nnkExprColonExpr(nnkIdent("c"), nnkIntLit(3)))
nnkTupleConstr()
```

```nim
(1,)
(a: 1)
```

```nim
nnkTupleConstr(nnkIntLit(1))
nnkTupleConstr(
  nnkExprColonExpr(nnkIdent("a"), nnkIntLit(1)))
```

```nim
{1, 2, 3}
```

```nim
nnkCurly(nnkIntLit(1), nnkIntLit(2), nnkIntLit(3))
```

```nim
{a: 3, b: 5}
```

```nim
nnkTableConstr(
  nnkExprColonExpr(nnkIdent("a"), nnkIntLit(3)),
  nnkExprColonExpr(nnkIdent("b"), nnkIntLit(5))
)
```

```nim
[1, 2, 3]
```

```nim
nnkBracket(nnkIntLit(1), nnkIntLit(2), nnkIntLit(3))
```

```nim
1..3
```

```nim
nnkInfix(
  nnkIdent(".."),
  nnkIntLit(1),
  nnkIntLit(3)
)
```

```nim
macro genRepeatEcho() =
  result = newNimNode(nnkStmtList)
  
  var forStmt = newNimNode(nnkForStmt) # generate a for statement
  forStmt.add(ident("i")) # use the variable `i` for iteration
  
  var rangeDef = newNimNode(nnkInfix).add(
    ident("..")).add(
    newIntLitNode(3),newIntLitNode(5)) # iterate over the range 3..5
  
  forStmt.add(rangeDef)
  forStmt.add(newCall(ident("echo"), newIntLitNode(3))) # meat of the loop
  result.add(forStmt)

genRepeatEcho() # gives:
                # 3
                # 3
                # 3
```

```nim
if cond1: expr1 elif cond2: expr2 else: expr3
```

```nim
nnkIfExpr(
  nnkElifExpr(cond1, expr1),
  nnkElifExpr(cond2, expr2),
  nnkElseExpr(expr3)
)
```

```nim
## This is a comment
## This is part of the first comment
stmt1
## Yet another
```

```nim
nnkCommentStmt() # only appears once for the first two lines!
stmt1
nnkCommentStmt() # another nnkCommentStmt because there is another comment
                 # (separate from the first)
```

```nim
{.emit: "#include <stdio.h>".}
```

```nim
nnkPragma(
  nnkExprColonExpr(
    nnkIdent("emit"),
    nnkStrLit("#include <stdio.h>") # the "argument"
  )
)
```

```nim
{.pragma: cdeclRename, cdecl.}
```

```nim
nnkPragma(
  nnkExprColonExpr(
    nnkIdent("pragma"), # this is always first when declaring a new pragma
    nnkIdent("cdeclRename") # the name of the pragma
  ),
  nnkIdent("cdecl")
)
```

```nim
if cond1:
  stmt1
elif cond2:
  stmt2
elif cond3:
  stmt3
else:
  stmt4
```

```nim
nnkIfStmt(
  nnkElifBranch(cond1, stmt1),
  nnkElifBranch(cond2, stmt2),
  nnkElifBranch(cond3, stmt3),
  nnkElse(stmt4)
)
```

```nim
x = 42
```

```nim
nnkAsgn(nnkIdent("x"), nnkIntLit(42))
```

```nim
stmt1
stmt2
stmt3
```

```nim
nnkStmtList(stmt1, stmt2, stmt3)
```

```nim
case expr1
of expr2, expr3..expr4:
  stmt1
of expr5:
  stmt2
elif cond1:
  stmt3
else:
  stmt4
```

```nim
nnkCaseStmt(
  expr1,
  nnkOfBranch(expr2, nnkRange(expr3, expr4), stmt1),
  nnkOfBranch(expr5, stmt2),
  nnkElifBranch(cond1, stmt3),
  nnkElse(stmt4)
)
```

```nim
while expr1:
  stmt1
```

```nim
nnkWhileStmt(expr1, stmt1)
```

```nim
for ident1, ident2 in expr1:
  stmt1
```

```nim
nnkForStmt(ident1, ident2, expr1, stmt1)
```

```nim
try:
  stmt1
except e1, e2:
  stmt2
except e3:
  stmt3
except:
  stmt4
finally:
  stmt5
```

```nim
nnkTryStmt(
  stmt1,
  nnkExceptBranch(e1, e2, stmt2),
  nnkExceptBranch(e3, stmt3),
  nnkExceptBranch(stmt4),
  nnkFinally(stmt5)
)
```

```nim
return expr1
```

```nim
nnkReturnStmt(expr1)
```

```nim
nnkYieldStmt(expr1)
```

```nim
nnkDiscardStmt(expr1)
```

```nim
continue
```

```nim
nnkContinueStmt()
```

```nim
break otherLocation
```

```nim
nnkBreakStmt(nnkIdent("otherLocation"))
```

```nim
block name:
```

```nim
nnkBlockStmt(nnkIdent("name"), nnkStmtList(...))
```

```nim
asm """
  some asm
"""
```

```nim
nnkAsmStmt(
  nnkEmpty(), # for pragmas
  nnkTripleStrLit("some asm"),
)
```

```nim
import std/math
```

```nim
nnkImportStmt(nnkIdent("math"))
```

```nim
import std/math except pow
```

```nim
nnkImportExceptStmt(nnkIdent("math"),nnkIdent("pow"))
```

```nim
import std/strutils as su
```

```nim
nnkImportStmt(
  nnkInfix(
    nnkIdent("as"),
    nnkIdent("strutils"),
    nnkIdent("su")
  )
)
```

```nim
from std/math import pow
```

```nim
nnkFromStmt(nnkIdent("math"), nnkIdent("pow"))
```

```nim
export unsigned
```

```nim
nnkExportStmt(nnkIdent("unsigned"))
```

```nim
export math except pow # we're going to implement our own exponentiation
```

```nim
nnkExportExceptStmt(nnkIdent("math"),nnkIdent("pow"))
```

```nim
include blocks
```

```nim
nnkIncludeStmt(nnkIdent("blocks"))
```

```nim
var a = 3
```

```nim
nnkVarSection(
  nnkIdentDefs(
    nnkIdent("a"),
    nnkEmpty(), # or nnkIdent(...) if the variable declares the type
    nnkIntLit(3),
  )
)
```

```nim
let a = 3
```

```nim
nnkLetSection(
  nnkIdentDefs(
    nnkIdent("a"),
    nnkEmpty(), # or nnkIdent(...) for the type
    nnkIntLit(3),
  )
)
```

```nim
const a = 3
```

```nim
nnkConstSection(
  nnkConstDef( # not nnkConstDefs!
    nnkIdent("a"),
    nnkEmpty(), # or nnkIdent(...) if the variable declares the type
    nnkIntLit(3), # required in a const declaration!
  )
)
```

```nim
type A = int
```

```nim
nnkTypeSection(
  nnkTypeDef(
    nnkIdent("A"),
    nnkEmpty(),
    nnkIdent("int")
  )
)
```

```nim
type MyInt = distinct int
```

```nim
# ...
nnkTypeDef(
  nnkIdent("MyInt"),
  nnkEmpty(),
  nnkDistinctTy(
    nnkIdent("int")
  )
)
```

```nim
type A[T] = expr1
```

```nim
nnkTypeSection(
  nnkTypeDef(
    nnkIdent("A"),
    nnkGenericParams(
      nnkIdentDefs(
        nnkIdent("T"),
        nnkEmpty(), # if the type is declared with options, like
                    # ``[T: SomeInteger]``, they are given here
        nnkEmpty(),
      )
    )
    expr1,
  )
)
```

```nim
type IO = object of RootObj
```

```nim
# ...
nnkTypeDef(
  nnkIdent("IO"),
  nnkEmpty(),
  nnkObjectTy(
    nnkEmpty(), # no pragmas here
    nnkOfInherit(
      nnkIdent("RootObj") # inherits from RootObj
    ),
    nnkEmpty()
  )
)
```

```nim
type Obj[T] {.inheritable.} = object
  name: string
  case isFat: bool
  of true:
    m: array[100_000, T]
  of false:
    m: array[10, T]
```

```nim
# ...
nnkPragmaExpr(
  nnkIdent("Obj"),
  nnkPragma(nnkIdent("inheritable"))
),
nnkGenericParams(
nnkIdentDefs(
  nnkIdent("T"),
  nnkEmpty(),
  nnkEmpty())
),
nnkObjectTy(
  nnkEmpty(),
  nnkEmpty(),
  nnkRecList( # list of object parameters
    nnkIdentDefs(
      nnkIdent("name"),
      nnkIdent("string"),
      nnkEmpty()
    ),
    nnkRecCase( # case statement within object (not nnkCaseStmt)
      nnkIdentDefs(
        nnkIdent("isFat"),
        nnkIdent("bool"),
        nnkEmpty()
      ),
      nnkOfBranch(
        nnkIdent("true"),
        nnkRecList( # again, a list of object parameters
          nnkIdentDefs(
            nnkIdent("m"),
            nnkBracketExpr(
              nnkIdent("array"),
              nnkIntLit(100000),
              nnkIdent("T")
            ),
            nnkEmpty()
        )
      ),
      nnkOfBranch(
        nnkIdent("false"),
        nnkRecList(
          nnkIdentDefs(
            nnkIdent("m"),
            nnkBracketExpr(
              nnkIdent("array"),
              nnkIntLit(10),
              nnkIdent("T")
            ),
            nnkEmpty()
          )
        )
      )
    )
  )
)
```

```nim
type X = enum
  First
```

```nim
# ...
nnkEnumTy(
  nnkEmpty(),
  nnkIdent("First") # you need at least one nnkIdent or the compiler complains
)
```

```nim
type Con = concept x,y,z
  (x & y & z) is string
```

```nim
# ...
nnkTypeClassTy( # note this isn't nnkConceptTy!
  nnkArgList(
    # ... idents for x, y, z
  )
  # ...
)
```

```nim
type A[T: static[int]] = object
```

```nim
# ... within nnkGenericParams
nnkIdentDefs(
  nnkIdent("T"),
  nnkStaticTy(
    nnkIdent("int")
  ),
  nnkEmpty()
)
# ...
```

```nim
type MyProc[T] = proc(x: T) {.nimcall.}
```

```nim
# ...
nnkTypeDef(
  nnkIdent("MyProc"),
  nnkGenericParams( # here, not with the proc
    # ...
  )
  nnkProcTy( # behaves like a procedure declaration from here on
    nnkFormalParams(
      # ...
    ),
    nnkPragma(nnkIdent("nimcall"))
  )
)
```

```nim
type TypeClass = proc {.nimcall.} | ref | tuple
```

```nim
nnkTypeDef(
  nnkIdent("TypeClass"),
  nnkEmpty(),
  nnkInfix(
    nnkIdent("|"),
    nnkProcTy(
      nnkEmpty(),
      nnkPragma(nnkIdent("nimcall"))
    ),
    nnkInfix(
      nnkIdent("|"),
      nnkRefTy(),
      nnkTupleClassTy()
    )
  )
)
```

```nim
mixin x
```

```nim
nnkMixinStmt(nnkIdent("x"))
```

```nim
bind x
```

```nim
nnkBindStmt(nnkIdent("x"))
```

```nim
proc hello*[T: SomeInteger](x: int = 3, y: float32): int {.inline.} = discard
```

```nim
nnkProcDef(
  nnkPostfix(nnkIdent("*"), nnkIdent("hello")), # the exported proc name
  nnkEmpty(), # patterns for term rewriting in templates and macros (not procs)
  nnkGenericParams( # generic type parameters, like with type declaration
    nnkIdentDefs(
      nnkIdent("T"),
      nnkIdent("SomeInteger"),
      nnkEmpty()
    )
  ),
  nnkFormalParams(
    nnkIdent("int"), # the first FormalParam is the return type. nnkEmpty() if there is none
    nnkIdentDefs(
      nnkIdent("x"),
      nnkIdent("int"), # type type (required for procs, not for templates)
      nnkIntLit(3) # a default value
    ),
    nnkIdentDefs(
      nnkIdent("y"),
      nnkIdent("float32"),
      nnkEmpty()
    )
  ),
  nnkPragma(nnkIdent("inline")),
  nnkEmpty(), # reserved slot for future use
  nnkStmtList(nnkDiscardStmt(nnkEmpty())) # the meat of the proc
)
```

```nim
proc(a, b: int)
```

```nim
# ...AST as above...
nnkFormalParams(
  nnkEmpty(), # no return here
  nnkIdentDefs(
    nnkIdent("a"), # the first parameter
    nnkIdent("b"), # directly to the second parameter
    nnkIdent("int"), # their shared type identifier
    nnkEmpty(), # default value would go here
  )
),
# ...
```

```nim
proc hello(): var int
```

```nim
# ...
nnkFormalParams(
  nnkVarTy(
    nnkIdent("int")
  )
)
```

```nim
iterator nonsense[T](x: seq[T]): float {.closure.} = ...
```

```nim
nnkIteratorDef(
  nnkIdent("nonsense"),
  nnkEmpty(),
  ...
)
```

```nim
converter toBool(x: float): bool
```

```nim
nnkConverterDef(
  nnkIdent("toBool"),
  # ...
)
```

```nim
template optOpt{expr1}(a: int): int
```

```nim
nnkTemplateDef(
  nnkIdent("optOpt"),
  nnkStmtList( # instead of nnkEmpty()
    expr1
  ),
  # follows like a proc or iterator
)
```

```nim
var f: float = 1
```

```nim
macro foo(x: typed) =
  var s = copyNimNode(x)
  doAssert s.len == 0
  doAssert s.kind == nnkStmtList

foo:
  let x = 12
  echo x
```

```nim
macro foo(x: typed) =
  var s = copyNimTree(x)
  doAssert s.len == 2
  doAssert s.kind == nnkStmtList

foo:
  let x = 12
  echo x
```

```nim
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

```nim
macro FooMacro() =
  var ast = getAst(BarTemplate())
```

```nim
type
  Vec[N: static[int], T] = object
    arr: array[N, T]
  Vec4[T] = Vec[4, T]
  Vec4f = Vec4[float32]
var a: Vec4f
var b: Vec4[float32]
var c: Vec[4, float32]
macro dumpTypeImpl(x: typed): untyped =
  newLit(x.getTypeImpl.repr)
let t = """
object
  arr: array[0 .. 3, float32]"""
doAssert(dumpTypeImpl(a) == t)
doAssert(dumpTypeImpl(b) == t)
doAssert(dumpTypeImpl(c) == t)
```

```nim
type
  Vec[N: static[int], T] = object
    arr: array[N, T]
  Vec4[T] = Vec[4, T]
  Vec4f = Vec4[float32]
var a: Vec4f
var b: Vec4[float32]
var c: Vec[4, float32]
macro dumpTypeInst(x: typed): untyped =
  newLit(x.getTypeInst.repr)
doAssert(dumpTypeInst(a) == "Vec4f")
doAssert(dumpTypeInst(b) == "Vec4[float32]")
doAssert(dumpTypeInst(c) == "Vec[4, float32]")
```

```nim
newEnum(
  name    = ident("Colors"),
  fields  = [ident("Blue"), ident("Red")],
  public  = true, pure = false)

# type Colors* = Blue Red
```

```nim
var varSection = newNimNode(nnkVarSection).add(
  newIdentDefs(ident("a"), ident("string")),
  newIdentDefs(ident("b"), newEmptyNode(), newLit(3)))
# --> var
#       a: string
#       b = 3
```

```nim
result = newNimNode(nnkIdentDefs).add(
  ident("a"), ident("b"), ident("c"), ident("string"),
    newStrLitNode("Hello"))
```

```nim
newIfStmt(
  (Ident, StmtList),
  ...
)
```

```nim
macro check(ex: untyped) =
  # this is a simplified version of the check macro from the
  # unittest module.

  # If there is a failed check, we want to make it easy for
  # the user to jump to the faulty line in the code, so we
  # get the line info here:
  var info = ex.lineinfo

  # We will also display the code string of the failed check:
  var expString = ex.toStrLit

  # Finally we compose the code to implement the check:
  result = quote do:
    if not `ex`:
      echo `info` & ": Check failed: " & `expString`
check 1 + 1 == 2
```

```nim
# example showing how to define a symbol that requires backtick without
# quoting it.
var destroyCalled = false
macro bar() =
  let s = newTree(nnkAccQuoted, ident"=destroy")
  # let s = ident"`=destroy`" # this would not work
  result = quote do:
    type Foo = object
    # proc `=destroy`(a: var Foo) = destroyCalled = true # this would not work
    proc `s`(a: var Foo) = destroyCalled = true
    block:
      let a = Foo()
bar()
doAssert destroyCalled
```

```nim
# custom `op`
var destroyCalled = false
macro bar(ident) =
  var x = 1.5
  result = quote("@") do:
    type Foo = object
    let `@ident` = 0 # custom op interpolated symbols need quoted (``)
    proc `=destroy`(a: var Foo) =
      doAssert @x == 1.5
      doAssert compiles(@x == 1.5)
      let b1 = @[1,2]
      let b2 = @@[1,2]
      doAssert $b1 == "[1, 2]"
      doAssert $b2 == "@[1, 2]"
      destroyCalled = true
    block:
      let a = Foo()
bar(someident)
doAssert destroyCalled

proc `&%`(x: int): int = 1
proc `&%`(x, y: int): int = 2

macro bar2() =
  var x = 3
  result = quote("&%") do:
    var y = &%x # quoting operator
    doAssert &%&%y == 1 # unary operator => need to escape
    doAssert y &% y == 2 # binary operator => no need to escape
    doAssert y == 3
bar2()
```

```nim
dumpAstGen:
  echo "Hello, World!"
```

```nim
nnkStmtList.newTree(
  nnkCommand.newTree(
    newIdentNode("echo"),
    newLit("Hello, World!")
  )
)
```

```nim
dumpLisp:
  echo "Hello, World!"
```

```nim
(StmtList
 (Command
  (Ident "echo")
  (StrLit "Hello, World!")))
```

```nim
dumpTree:
  echo "Hello, World!"
```

```nim
StmtList
  Command
    Ident "echo"
    StrLit "Hello, World!"
```

```nim
import std/[sugar, macros]

let
  x = 10
  y = 20
expandMacros:
  dump(x + y)
```

```nim
template serializationKey(key: string) {.pragma.}
type
  MyObj {.serializationKey: "mo".} = object
    myField {.serializationKey: "mf".}: int
var o: MyObj
assert(o.myField.getCustomPragmaVal(serializationKey) == "mf")
assert(o.getCustomPragmaVal(serializationKey) == "mo")
assert(MyObj.getCustomPragmaVal(serializationKey) == "mo")
```

```nim
template myAttr() {.pragma.}
type
  MyObj = object
    myField {.myAttr.}: int

proc myProc() {.myAttr.} = discard

var o: MyObj
assert(o.myField.hasCustomPragma(myAttr))
assert(myProc.hasCustomPragma(myAttr))
```

```nim
template call1(fun: typed; args: varargs[untyped]): untyped =
  unpackVarargs(fun, args)
  # when varargsLen(args) > 0: fun(args) else: fun() # this would also work
template call2(fun: typed; args: varargs[typed]): untyped =
  unpackVarargs(fun, args)
proc fn1(a = 0, b = 1) = discard (a, b)
call1(fn1, 10, 11)
call1(fn1) # `args` is empty in this case
if false: call2(echo, 10, 11) # would print 1011
```

```nim
var res = findChild(n, it.kind == nnkPostfix and
                       it.basename.ident == ident"foo")
```

```nim
let node = mightBeEmpty() or mightAlsoBeEmpty() or fallbackNode
```


[Next](macros_2.md)
