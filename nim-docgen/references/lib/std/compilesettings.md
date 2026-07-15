---
source_hash: f4533d0bab43e94c
source_path: lib/std/compilesettings.nim
---

# compilesettings

[ref: #module-compilesettings]

This module allows querying the compiler about diverse configuration settings. See also compileOption.

## Examples

```nim
const nimcache = querySetting(SingleValueSetting.nimcacheDir)
```

```nim
const nimblePaths = querySettingSeq(MultipleValueSetting.nimblePaths)
```

## Proc

### querySetting

[ref: #symbol-querysetting]

Can be used to get a string compile-time option.

**Input:**
- `setting: SingleValueSetting`

**Output:** `string`
**Pragmas:** `compileTime`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Can be used to get a string compile-time option.

See also:

* [compileOption](system.html#compileOption,string) for on|off options
* [compileOption](system.html#compileOption,string,string) for enum options

### querySettingSeq

[ref: #symbol-querysettingseq]

Can be used to get a multi-string compile-time option.

**Input:**
- `setting: MultipleValueSetting`

**Output:** `seq[string]`
**Pragmas:** `compileTime`, `noSideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Can be used to get a multi-string compile-time option.

See also:

* [compileOption](system.html#compileOption,string) for on|off options
* [compileOption](system.html#compileOption,string,string) for enum options

## Type

### MultipleValueSetting

[ref: #symbol-multiplevaluesetting]

```nim
MultipleValueSetting {.pure.} = enum
  nimblePaths,              ## the nimble path(s)
  searchPaths,              ## the search path for modules
  lazyPaths,                ## experimental: even more paths
  commandArgs,              ## the arguments passed to the Nim compiler
  cincludes,                ## the #include paths passed to the C/C++ compiler
  clibs                      ## libraries passed to the C/C++ compiler
```

settings resulting in a seq of string values

### SingleValueSetting

[ref: #symbol-singlevaluesetting]

```nim
SingleValueSetting {.pure.} = enum
  arguments,                ## experimental: the arguments passed after '-r'
  outFile,                  ## experimental: the output file
  outDir,                   ## the output directory
  nimcacheDir,              ## the location of the 'nimcache' directory
  projectName,              ## the project's name that is being compiled
  projectPath,              ## experimental: some path to the project that is being compiled
  projectFull,              ## the full path to the project that is being compiled
  command, ## experimental: the command (e.g. 'c', 'cpp', 'doc') passed to
            ## the Nim compiler
  commandLine,              ## experimental: the command line passed to Nim
  linkOptions,              ## additional options passed to the linker
  compileOptions,           ## additional options passed to the C/C++ compiler
  ccompilerPath,            ## the path to the C/C++ compiler
  backend, ## the backend (eg: c|cpp|objc|js); both `nim doc --backend:js`
            ## and `nim js` would imply backend=js
  libPath,                  ## the absolute path to the stdlib library, i.e. nim's `--lib`, since 1.5.1
  gc {.deprecated.},        ## gc selected
  mm                         ## memory management selected
```

settings resulting in a single string value
