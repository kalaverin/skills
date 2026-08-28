---
source_hash: 5a8eab3d07865953
source_path: lib/std/private/ntpath.nim
---

# ntpath

[ref: #module-ntpath]

## Examples

```nim
doAssert splitDrive("C:") == ("C:", "")
doAssert splitDrive(r"C:\") == (r"C:", r"\")
doAssert splitDrive(r"\\server\drive\foo\bar") == (r"\\server\drive", r"\foo\bar")
doAssert splitDrive(r"\\?\UNC\server\share\dir") == (r"\\?\UNC\server\share", r"\dir")
```

## Proc

### splitDrive

[ref: #symbol-splitdrive]

Splits a Windows path into a drive and path part. The drive can be e.g. C:. It can also be a UNC path (\\server\drive\path).

**Input:**
- `p: string`

**Output:** `tuple[drive, path: string]`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Splits a Windows path into a drive and path part. The drive can be e.g. C:. It can also be a UNC path (\\server\drive\path).

The equivalent splitDrive for POSIX systems always returns empty drive. Therefore this proc is only necessary on DOS-like file systems (together with Nim's doslikeFileSystem conditional variable).

This proc's use case is to extract path such that it can be manipulated like a POSIX path.
