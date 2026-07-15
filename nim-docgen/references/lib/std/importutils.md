---
source_hash: 3071247be4fc6a0d
source_path: lib/std/importutils.nim
---

# importutils

[ref: #module-importutils]

Utilities related to import and symbol resolution.

Experimental API, subject to change.

## Examples

```nim
# here we're importing a module containing:
# type
#   Foo = object
#     f0: int # private
#   Goo*[T] = object
#     g0: int # private
# proc initFoo*(): auto = Foo()
var f = initFoo()
block:
  assert not compiles(f.f0)
  privateAccess(f.type)
  f.f0 = 1 # accessible in this scope
  block:
    assert f.f0 == 1 # still in scope
assert not compiles(f.f0)

# this also works with generics
privateAccess(Goo)
assert Goo[float](g0: 1).g0 == 1
```

## Proc

### privateAccess

[ref: #symbol-privateaccess]

**Input:**
- `t: typedesc`

**Output:** *(none)*
**Generic parameters:** `t:type`

**Pragmas:** `magic: "PrivateAccess"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Enables access to private fields of t in current scope.
