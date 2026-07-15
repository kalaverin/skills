---
source_hash: ace26bbf795b20ce
source_path: lib/wrappers/pcre.nim
---

# pcre

[ref: #module-pcre]

## Const

### ANCHORED

[ref: #symbol-anchored]

```nim
ANCHORED = 0x00000010
```

### AUTO_CALLOUT

[ref: #symbol-auto-callout]

```nim
AUTO_CALLOUT = 0x00004000
```

### BSR_ANYCRLF

[ref: #symbol-bsr-anycrlf]

```nim
BSR_ANYCRLF = 0x00800000
```

### BSR_UNICODE

[ref: #symbol-bsr-unicode]

```nim
BSR_UNICODE = 0x01000000
```

### CASELESS

[ref: #symbol-caseless]

```nim
CASELESS = 0x00000001
```

### CONFIG_BSR

[ref: #symbol-config-bsr]

```nim
CONFIG_BSR = 8
```

### CONFIG_JIT

[ref: #symbol-config-jit]

```nim
CONFIG_JIT = 9
```

### CONFIG_JITTARGET

[ref: #symbol-config-jittarget]

```nim
CONFIG_JITTARGET = 11
```

### CONFIG_LINK_SIZE

[ref: #symbol-config-link-size]

```nim
CONFIG_LINK_SIZE = 2
```

### CONFIG_MATCH_LIMIT

[ref: #symbol-config-match-limit]

```nim
CONFIG_MATCH_LIMIT = 4
```

### CONFIG_MATCH_LIMIT_RECURSION

[ref: #symbol-config-match-limit-recursion]

```nim
CONFIG_MATCH_LIMIT_RECURSION = 7
```

### CONFIG_NEWLINE

[ref: #symbol-config-newline]

```nim
CONFIG_NEWLINE = 1
```

### CONFIG_PARENS_LIMIT

[ref: #symbol-config-parens-limit]

```nim
CONFIG_PARENS_LIMIT = 13
```

### CONFIG_POSIX_MALLOC_THRESHOLD

[ref: #symbol-config-posix-malloc-threshold]

```nim
CONFIG_POSIX_MALLOC_THRESHOLD = 3
```

### CONFIG_STACKRECURSE

[ref: #symbol-config-stackrecurse]

```nim
CONFIG_STACKRECURSE = 5
```

### CONFIG_UNICODE_PROPERTIES

[ref: #symbol-config-unicode-properties]

```nim
CONFIG_UNICODE_PROPERTIES = 6
```

### CONFIG_UTF16

[ref: #symbol-config-utf16]

```nim
CONFIG_UTF16 = 10
```

### CONFIG_UTF32

[ref: #symbol-config-utf32]

```nim
CONFIG_UTF32 = 12
```

### CONFIG_UTF8

[ref: #symbol-config-utf8]

```nim
CONFIG_UTF8 = 0
```

### DFA_RESTART

[ref: #symbol-dfa-restart]

```nim
DFA_RESTART = 0x00020000
```

### DFA_SHORTEST

[ref: #symbol-dfa-shortest]

```nim
DFA_SHORTEST = 0x00010000
```

### DOLLAR_ENDONLY

[ref: #symbol-dollar-endonly]

```nim
DOLLAR_ENDONLY = 0x00000020
```

### DOTALL

[ref: #symbol-dotall]

```nim
DOTALL = 0x00000004
```

### DUPNAMES

[ref: #symbol-dupnames]

```nim
DUPNAMES = 0x00080000
```

### ERROR_BADCOUNT

[ref: #symbol-error-badcount]

```nim
ERROR_BADCOUNT = -15
```

### ERROR_BADENDIANNESS

[ref: #symbol-error-badendianness]

```nim
ERROR_BADENDIANNESS = -29
```

### ERROR_BADLENGTH

[ref: #symbol-error-badlength]

```nim
ERROR_BADLENGTH = -32
```

### ERROR_BADMAGIC

[ref: #symbol-error-badmagic]

```nim
ERROR_BADMAGIC = -4
```

### ERROR_BADMODE

[ref: #symbol-error-badmode]

```nim
ERROR_BADMODE = -28
```

### ERROR_BADNEWLINE

[ref: #symbol-error-badnewline]

```nim
ERROR_BADNEWLINE = -23
```

### ERROR_BADOFFSET

[ref: #symbol-error-badoffset]

```nim
ERROR_BADOFFSET = -24
```

### ERROR_BADOPTION

[ref: #symbol-error-badoption]

```nim
ERROR_BADOPTION = -3
```

### ERROR_BADPARTIAL

[ref: #symbol-error-badpartial]

```nim
ERROR_BADPARTIAL = -13
```

### ERROR_BADUTF16

[ref: #symbol-error-badutf16]

```nim
ERROR_BADUTF16 = -10
```

Same for 8/16/32

### ERROR_BADUTF16_OFFSET

[ref: #symbol-error-badutf16-offset]

```nim
ERROR_BADUTF16_OFFSET = -11
```

Same for 8/16

### ERROR_BADUTF32

[ref: #symbol-error-badutf32]

```nim
ERROR_BADUTF32 = -10
```

Same for 8/16/32

### ERROR_BADUTF8

[ref: #symbol-error-badutf8]

```nim
ERROR_BADUTF8 = -10
```

Same for 8/16/32

### ERROR_BADUTF8_OFFSET

[ref: #symbol-error-badutf8-offset]

```nim
ERROR_BADUTF8_OFFSET = -11
```

Same for 8/16

### ERROR_CALLOUT

[ref: #symbol-error-callout]

```nim
ERROR_CALLOUT = -9
```

Never used by PCRE itself

### ERROR_DFA_BADRESTART

[ref: #symbol-error-dfa-badrestart]

```nim
ERROR_DFA_BADRESTART = -30
```

### ERROR_DFA_RECURSE

[ref: #symbol-error-dfa-recurse]

```nim
ERROR_DFA_RECURSE = -20
```

### ERROR_DFA_UCOND

[ref: #symbol-error-dfa-ucond]

```nim
ERROR_DFA_UCOND = -17
```

### ERROR_DFA_UITEM

[ref: #symbol-error-dfa-uitem]

```nim
ERROR_DFA_UITEM = -16
```

### ERROR_DFA_UMLIMIT

[ref: #symbol-error-dfa-umlimit]

```nim
ERROR_DFA_UMLIMIT = -18
```

### ERROR_DFA_WSSIZE

[ref: #symbol-error-dfa-wssize]

```nim
ERROR_DFA_WSSIZE = -19
```

### ERROR_INTERNAL

[ref: #symbol-error-internal]

```nim
ERROR_INTERNAL = -14
```

### ERROR_JIT_BADOPTION

[ref: #symbol-error-jit-badoption]

```nim
ERROR_JIT_BADOPTION = -31
```

### ERROR_JIT_STACKLIMIT

[ref: #symbol-error-jit-stacklimit]

```nim
ERROR_JIT_STACKLIMIT = -27
```

### ERROR_MATCHLIMIT

[ref: #symbol-error-matchlimit]

```nim
ERROR_MATCHLIMIT = -8
```

### ERROR_NOMATCH

[ref: #symbol-error-nomatch]

```nim
ERROR_NOMATCH = -1
```

### ERROR_NOMEMORY

[ref: #symbol-error-nomemory]

```nim
ERROR_NOMEMORY = -6
```

### ERROR_NOSUBSTRING

[ref: #symbol-error-nosubstring]

```nim
ERROR_NOSUBSTRING = -7
```

### ERROR_NULL

[ref: #symbol-error-null]

```nim
ERROR_NULL = -2
```

### ERROR_NULLWSLIMIT

[ref: #symbol-error-nullwslimit]

```nim
ERROR_NULLWSLIMIT = -22
```

No longer actually used

### ERROR_PARTIAL

[ref: #symbol-error-partial]

```nim
ERROR_PARTIAL = -12
```

### ERROR_RECURSELOOP

[ref: #symbol-error-recurseloop]

```nim
ERROR_RECURSELOOP = -26
```

### ERROR_RECURSIONLIMIT

[ref: #symbol-error-recursionlimit]

```nim
ERROR_RECURSIONLIMIT = -21
```

### ERROR_SHORTUTF16

[ref: #symbol-error-shortutf16]

```nim
ERROR_SHORTUTF16 = -25
```

Same for 8/16

### ERROR_SHORTUTF8

[ref: #symbol-error-shortutf8]

```nim
ERROR_SHORTUTF8 = -25
```

### ERROR_UNKNOWN_NODE

[ref: #symbol-error-unknown-node]

```nim
ERROR_UNKNOWN_NODE = -5
```

For backward compatibility

### ERROR_UNKNOWN_OPCODE

[ref: #symbol-error-unknown-opcode]

```nim
ERROR_UNKNOWN_OPCODE = -5
```

### ERROR_UNSET

[ref: #symbol-error-unset]

```nim
ERROR_UNSET = -33
```

### EXTENDED

[ref: #symbol-extended]

```nim
EXTENDED = 0x00000008
```

### EXTRA

[ref: #symbol-extra]

```nim
EXTRA = 0x00000040
```

### EXTRA_CALLOUT_DATA

[ref: #symbol-extra-callout-data]

```nim
EXTRA_CALLOUT_DATA = 0x00000004
```

### EXTRA_EXECUTABLE_JIT

[ref: #symbol-extra-executable-jit]

```nim
EXTRA_EXECUTABLE_JIT = 0x00000040
```

### EXTRA_MARK

[ref: #symbol-extra-mark]

```nim
EXTRA_MARK = 0x00000020
```

### EXTRA_MATCH_LIMIT

[ref: #symbol-extra-match-limit]

```nim
EXTRA_MATCH_LIMIT = 0x00000002
```

### EXTRA_MATCH_LIMIT_RECURSION

[ref: #symbol-extra-match-limit-recursion]

```nim
EXTRA_MATCH_LIMIT_RECURSION = 0x00000010
```

### EXTRA_STUDY_DATA

[ref: #symbol-extra-study-data]

```nim
EXTRA_STUDY_DATA = 0x00000001
```

### EXTRA_TABLES

[ref: #symbol-extra-tables]

```nim
EXTRA_TABLES = 0x00000008
```

### FIRSTLINE

[ref: #symbol-firstline]

```nim
FIRSTLINE = 0x00040000
```

### INFO_BACKREFMAX

[ref: #symbol-info-backrefmax]

```nim
INFO_BACKREFMAX = 3
```

### INFO_CAPTURECOUNT

[ref: #symbol-info-capturecount]

```nim
INFO_CAPTURECOUNT = 2
```

### INFO_DEFAULT_TABLES

[ref: #symbol-info-default-tables]

```nim
INFO_DEFAULT_TABLES = 11
```

### INFO_FIRSTBYTE

[ref: #symbol-info-firstbyte]

```nim
INFO_FIRSTBYTE = 4
```

### INFO_FIRSTCHAR

[ref: #symbol-info-firstchar]

```nim
INFO_FIRSTCHAR = 4
```

For backwards compatibility

### INFO_FIRSTCHARACTER

[ref: #symbol-info-firstcharacter]

```nim
INFO_FIRSTCHARACTER = 19
```

### INFO_FIRSTCHARACTERFLAGS

[ref: #symbol-info-firstcharacterflags]

```nim
INFO_FIRSTCHARACTERFLAGS = 20
```

### INFO_FIRSTTABLE

[ref: #symbol-info-firsttable]

```nim
INFO_FIRSTTABLE = 5
```

### INFO_HASCRORLF

[ref: #symbol-info-hascrorlf]

```nim
INFO_HASCRORLF = 14
```

### INFO_JCHANGED

[ref: #symbol-info-jchanged]

```nim
INFO_JCHANGED = 13
```

### INFO_JIT

[ref: #symbol-info-jit]

```nim
INFO_JIT = 16
```

### INFO_JITSIZE

[ref: #symbol-info-jitsize]

```nim
INFO_JITSIZE = 17
```

### INFO_LASTLITERAL

[ref: #symbol-info-lastliteral]

```nim
INFO_LASTLITERAL = 6
```

### INFO_MATCH_EMPTY

[ref: #symbol-info-match-empty]

```nim
INFO_MATCH_EMPTY = 25
```

### INFO_MATCHLIMIT

[ref: #symbol-info-matchlimit]

```nim
INFO_MATCHLIMIT = 23
```

### INFO_MAXLOOKBEHIND

[ref: #symbol-info-maxlookbehind]

```nim
INFO_MAXLOOKBEHIND = 18
```

### INFO_MINLENGTH

[ref: #symbol-info-minlength]

```nim
INFO_MINLENGTH = 15
```

### INFO_NAMECOUNT

[ref: #symbol-info-namecount]

```nim
INFO_NAMECOUNT = 8
```

### INFO_NAMEENTRYSIZE

[ref: #symbol-info-nameentrysize]

```nim
INFO_NAMEENTRYSIZE = 7
```

### INFO_NAMETABLE

[ref: #symbol-info-nametable]

```nim
INFO_NAMETABLE = 9
```

### INFO_OKPARTIAL

[ref: #symbol-info-okpartial]

```nim
INFO_OKPARTIAL = 12
```

### INFO_OPTIONS

[ref: #symbol-info-options]

```nim
INFO_OPTIONS = 0
```

### INFO_RECURSIONLIMIT

[ref: #symbol-info-recursionlimit]

```nim
INFO_RECURSIONLIMIT = 24
```

### INFO_REQUIREDCHAR

[ref: #symbol-info-requiredchar]

```nim
INFO_REQUIREDCHAR = 21
```

### INFO_REQUIREDCHARFLAGS

[ref: #symbol-info-requiredcharflags]

```nim
INFO_REQUIREDCHARFLAGS = 22
```

### INFO_SIZE

[ref: #symbol-info-size]

```nim
INFO_SIZE = 1
```

### INFO_STUDYSIZE

[ref: #symbol-info-studysize]

```nim
INFO_STUDYSIZE = 10
```

### JAVASCRIPT_COMPAT

[ref: #symbol-javascript-compat]

```nim
JAVASCRIPT_COMPAT = 0x02000000
```

### MULTILINE

[ref: #symbol-multiline]

```nim
MULTILINE = 0x00000002
```

### NEVER_UTF

[ref: #symbol-never-utf]

```nim
NEVER_UTF = 0x00010000
```

### NEWLINE_ANY

[ref: #symbol-newline-any]

```nim
NEWLINE_ANY = 0x00400000
```

### NEWLINE_ANYCRLF

[ref: #symbol-newline-anycrlf]

```nim
NEWLINE_ANYCRLF = 0x00500000
```

### NEWLINE_CR

[ref: #symbol-newline-cr]

```nim
NEWLINE_CR = 0x00100000
```

### NEWLINE_CRLF

[ref: #symbol-newline-crlf]

```nim
NEWLINE_CRLF = 0x00300000
```

### NEWLINE_LF

[ref: #symbol-newline-lf]

```nim
NEWLINE_LF = 0x00200000
```

### NO_AUTO_CAPTURE

[ref: #symbol-no-auto-capture]

```nim
NO_AUTO_CAPTURE = 0x00001000
```

### NO_AUTO_POSSESS

[ref: #symbol-no-auto-possess]

```nim
NO_AUTO_POSSESS = 0x00020000
```

### NO_START_OPTIMISE

[ref: #symbol-no-start-optimise]

```nim
NO_START_OPTIMISE = 0x04000000
```

### NO_START_OPTIMIZE

[ref: #symbol-no-start-optimize]

```nim
NO_START_OPTIMIZE = 0x04000000
```

### NO_UTF16_CHECK

[ref: #symbol-no-utf16-check]

```nim
NO_UTF16_CHECK = 0x00002000
```

### NO_UTF32_CHECK

[ref: #symbol-no-utf32-check]

```nim
NO_UTF32_CHECK = 0x00002000
```

### NO_UTF8_CHECK

[ref: #symbol-no-utf8-check]

```nim
NO_UTF8_CHECK = 0x00002000
```

### NOTBOL

[ref: #symbol-notbol]

```nim
NOTBOL = 0x00000080
```

### NOTEMPTY

[ref: #symbol-notempty]

```nim
NOTEMPTY = 0x00000400
```

### NOTEMPTY_ATSTART

[ref: #symbol-notempty-atstart]

```nim
NOTEMPTY_ATSTART = 0x10000000
```

### NOTEOL

[ref: #symbol-noteol]

```nim
NOTEOL = 0x00000100
```

### PARTIAL

[ref: #symbol-partial]

```nim
PARTIAL = 0x00008000
```

### PARTIAL_HARD

[ref: #symbol-partial-hard]

```nim
PARTIAL_HARD = 0x08000000
```

### PARTIAL_SOFT

[ref: #symbol-partial-soft]

```nim
PARTIAL_SOFT = 0x00008000
```


[Next](pcre_2.md)
