---
source_hash: 741f9b3f7c835874
source_path: lib/pure/distros.nim
---

# distros

[ref: #module-distros]

This module implements the basics for Linux distribution ("distro") detection and the OS's native package manager. Its primary purpose is to produce output for Nimble packages, like:

```
To complete the installation, run:

sudo apt-get install libblas-dev
sudo apt-get install libvoodoo
```

The above output could be the result of a code snippet like:

```
if detectOs(Ubuntu):
  foreignDep "lbiblas-dev"
  foreignDep "libvoodoo"
```

See [packaging](packaging.html) for hints on distributing Nim using OS packages.

## Examples

```nim
if detectOs(Ubuntu):
  foreignDep "lbiblas-dev"
  foreignDep "libvoodoo"
```

## Const

### LacksDevPackages

[ref: #symbol-lacksdevpackages]

```nim
LacksDevPackages = {Distribution.Gentoo, Distribution.Slackware,
                    Distribution.ArchLinux, Distribution.Artix,
                    Distribution.Antergos, Distribution.BlackArch,
                    Distribution.ArchBang}
```

## Proc

### echoForeignDeps

[ref: #symbol-echoforeigndeps]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Writes the list of registered foreign deps to stdout.

### foreignCmd

[ref: #symbol-foreigncmd]

**Input:**
- `cmd: string`
- `requiresSudo:  = false`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Registers a foreign command to the internal list of commands that can be queried later.

### foreignDep

[ref: #symbol-foreigndep]

**Input:**
- `foreignPackageName: string`

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Registers foreignPackageName to the internal list of foreign deps. It is your job to ensure that the package name is correct.

### foreignDepInstallCmd

[ref: #symbol-foreigndepinstallcmd]

**Input:**
- `foreignPackageName: string`

**Output:** `(string, bool)`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Returns the distro's native command to install foreignPackageName and whether it requires root/admin rights.

## Template

### detectOs

[ref: #symbol-detectos]

**Input:**
- `d: untyped`

**Output:** `bool`
Distro/OS detection. For convenience, the required Distribution. qualifier is added to the enum value.

## Type

### Distribution

[ref: #symbol-distribution]

```nim
Distribution {.pure.} = enum
  Windows,                  ## some version of Windows
  Posix,                    ## some POSIX system
  MacOSX,                   ## some version of OSX
  Linux,                    ## some version of Linux
  Ubuntu, Debian, Gentoo, Fedora, RedHat, OpenSUSE, Manjaro, Elementary, Zorin,
  CentOS, Deepin, ArchLinux, Artix, Antergos, PCLinuxOS, Mageia, LXLE, Solus,
  Lite, Slackware, Androidx86, Puppy, Peppermint, Tails, AntiX, Kali,
  SparkyLinux, Apricity, BlackLab, Bodhi, TrueOS, ArchBang, KaOS, WattOS,
  Korora, Simplicity, RemixOS, OpenMandriva, Netrunner, Alpine, BlackArch,
  Ultimate, Gecko, Parrot, KNOPPIX, GhostBSD, Sabayon, Salix, Q4OS, ClearOS,
  Container, ROSA, Zenwalk, Parabola, ChaletOS, BackBox, MXLinux, Vector, Maui,
  Qubes, RancherOS, Oracle, TinyCore, Robolinux, Trisquel, Voyager, Clonezilla,
  SteamOS, Absolute, NixOS, ## NixOS or a Nix build environment
  AUSTRUMI, Arya, Porteus, AVLinux, Elive, Bluestar, SliTaz, Solaris, Chakra,
  Wifislax, Scientific, ExTiX, Rockstor, GoboLinux, Void, BSD, FreeBSD, NetBSD,
  OpenBSD, DragonFlyBSD, Haiku
```

the list of known distributions

## Var

### foreignDeps

[ref: #symbol-foreigndeps]

```nim
foreignDeps: seq[string] = @[]
```

Registered foreign deps.
