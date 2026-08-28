---
source_hash: bc3226119f36bae8
source_path: lib/experimental/diff.nim
---

# diff

[ref: #module-diff]

This module implements an algorithm to compute the diff between two sequences of lines.

* To learn more see [Diff on Wikipedia.](https://wikipedia.org/wiki/Diff)

## Examples

```nim
import experimental/diff
assert diffInt(
  [0, 1, 2, 3, 4, 5, 6, 7, 8],
  [-1, 1, 2, 3, 4, 5, 666, 7, 42]) ==
  @[Item(startA: 0, startB: 0, deletedA: 1, insertedB: 1),
    Item(startA: 6, startB: 6, deletedA: 1, insertedB: 1),
    Item(startA: 8, startB: 8, deletedA: 1, insertedB: 1)]
```

```nim
import experimental/diff
# 2 samples of text (from "The Call of Cthulhu" by Lovecraft)
let txt0 = """
abc
def ghi
jkl2"""
let txt1 = """
bacx
abc
def ghi
jkl"""
assert diffText(txt0, txt1) ==
  @[Item(startA: 0, startB: 0, deletedA: 0, insertedB: 1),
    Item(startA: 2, startB: 3, deletedA: 1, insertedB: 1)]
```

## Proc

### diffInt

[ref: #symbol-diffint]

Find the difference in 2 arrays of integers.

**Input:**
- `arrayA: openArray[int]`
- `arrayB: openArray[int]`

**Output:** `seq[Item]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Find the difference in 2 arrays of integers.

arrayA A-version of the numbers (usually the old one)

arrayB B-version of the numbers (usually the new one)

Returns a sequence of Items that describe the differences.

### diffText

[ref: #symbol-difftext]

Find the difference in 2 text documents, comparing by textlines.

**Input:**
- `textA: string`
- `textB: string`

**Output:** `seq[Item]`
**Pragmas:** `raises: [KeyError]`, `tags: []`, `forbids: []`

**Effects:** `raises: KeyError`, `tags: `, `forbids: `

Find the difference in 2 text documents, comparing by textlines.

The algorithm itself is comparing 2 arrays of numbers so when comparing 2 text documents each line is converted into a (hash) number. This hash-value is computed by storing all textlines into a common hashtable so i can find duplicates in there, and generating a new number each time a new textline is inserted.

textA A-version of the text (usually the old one)

textB B-version of the text (usually the new one)

Returns a seq of Items that describe the differences.

## Type

### Item

[ref: #symbol-item]

```nim
Item = object
  startA*: int               ## Start Line number in Data A.
  startB*: int               ## Start Line number in Data B.
  deletedA*: int             ## Number of changes in Data A.
  insertedB*: int            ## Number of changes in Data B.
```

An Item in the list of differences.
