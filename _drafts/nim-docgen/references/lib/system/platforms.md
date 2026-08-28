---
source_hash: d92ce91eb4dc6e9c
source_path: lib/system/platforms.nim
---

# platforms

[ref: #module-platforms]

Platform detection for NimScript. This module is included by the system module! Do not import it directly!

## Const

### targetCPU

[ref: #symbol-targetcpu]

```nim
targetCPU = CpuPlatform.arm64
```

the CPU this program will run on.

### targetOS

[ref: #symbol-targetos]

```nim
targetOS = OsPlatform.macosx
```

the OS this program will run on.

## Type

### CpuPlatform

[ref: #symbol-cpuplatform]

```nim
CpuPlatform {.pure.} = enum
  none,                     ## unknown CPU
  i386,                     ## 32 bit x86 compatible CPU
  m68k,                     ## M68k based processor
  alpha,                    ## Alpha processor
  powerpc,                  ## 32 bit PowerPC
  powerpc64,                ## 64 bit PowerPC
  powerpc64el,              ## Little Endian 64 bit PowerPC
  sparc,                    ## Sparc based processor
  sparc64,                  ## 64-bit Sparc based processor
  hppa,                     ## HP PA-RISC
  ia64,                     ## Intel Itanium
  amd64,                    ## x86_64 (AMD64); 64 bit x86 compatible CPU
  mips,                     ## Mips based processor
  mipsel,                   ## Little Endian Mips based processor
  mips64,                   ## 64-bit MIPS processor
  mips64el,                 ## Little Endian 64-bit MIPS processor
  arm,                      ## ARM based processor
  arm64,                    ## ARM64 based processor
  vm,                       ## Some Virtual machine: Nim's VM or JavaScript
  avr,                      ## AVR based processor
  msp430,                   ## TI MSP430 microcontroller
  riscv32,                  ## RISC-V 32-bit processor
  riscv64,                  ## RISC-V 64-bit processor
  wasm32,                   ## WASM, 32-bit
  e2k,                      ## MCST Elbrus 2000
  loongarch64,              ## LoongArch 64-bit processor
  s390x,                    ## IBM Z
  wasm64                     ## WASM, 64-bit
```

the CPU this program will run on.

### OsPlatform

[ref: #symbol-osplatform]

```nim
OsPlatform {.pure.} = enum
  none, dos, windows, os2, linux, morphos, skyos, solaris, irix, netbsd,
  freebsd, openbsd, aix, palmos, qnx, amiga, atari, netware, macos, macosx,
  haiku, android, js, standalone, nintendoswitch
```

the OS this program will run on.
