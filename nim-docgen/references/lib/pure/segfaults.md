---
source_hash: fe6792e21ce0321b
source_path: lib/pure/segfaults.nim
---

# segfaults

[ref: #module-segfaults]

This modules registers a signal handler that turns access violations / segfaults into a NilAccessDefect exception. To be able to catch a NilAccessDefect all you have to do is to import this module.

Tested on these OSes: Linux, Windows, OSX
