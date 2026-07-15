---
source_hash: b317a8186f2a9a1a
source_path: lib/pure/nimprof.nim
---

# nimprof

[ref: #module-nimprof]

Profiling support for Nim. This is an embedded profiler that requires --profiler:on. You only need to import this module to get a profiling report at program exit. See [Embedded Stack Trace Profiler](estp.html) for usage.Timer support for the realtime GC. Based on <https://github.com/jckarter/clay/blob/master/compiler/hirestimer.cpp>

## Proc

### disableProfiling

[ref: #symbol-disableprofiling]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### enableProfiling

[ref: #symbol-enableprofiling]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### setSamplingFrequency

[ref: #symbol-setsamplingfrequency]

**Input:**
- `intervalInUs: int`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

set this to change the sampling frequency. Default value is 5ms. Set it to 0 to disable time based profiling; it uses an imprecise instruction count measure instead then.
