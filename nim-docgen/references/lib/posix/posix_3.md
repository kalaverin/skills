---
source_hash: fcacb532bbcaa46f
source_path: lib/posix/posix.nim
---

### globfree

[ref: #symbol-globfree]

**Input:**
- `a1: ptr Glob`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<glob.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gmtime

[ref: #symbol-gmtime]

**Input:**
- `a1: var Time`

**Output:** `ptr Tm`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### gmtime_r

[ref: #symbol-gmtime-r]

**Input:**
- `a1: var Time`
- `a2: var Tm`

**Output:** `ptr Tm`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### hstrerror

[ref: #symbol-hstrerror]

**Input:**
- `herrnum: cint`

**Output:** `cstring`
**Pragmas:** `importc: "(char *)$1"`, `header: "<netdb.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### htonl

[ref: #symbol-htonl]

**Input:**
- `a1: uint32`

**Output:** `uint32`
**Pragmas:** `importc`, `header: "<arpa/inet.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### htons

[ref: #symbol-htons]

**Input:**
- `a1: uint16`

**Output:** `uint16`
**Pragmas:** `importc`, `header: "<arpa/inet.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### iconv

[ref: #symbol-iconv]

**Input:**
- `a1: Iconv`
- `a2: var cstring`
- `a3: var int`
- `a4: var cstring`
- `a5: var int`

**Output:** `int`
**Pragmas:** `importc`, `header: "<iconv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### iconv_close

[ref: #symbol-iconv-close]

**Input:**
- `a1: Iconv`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<iconv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### iconv_open

[ref: #symbol-iconv-open]

**Input:**
- `a1: cstring`
- `a2: cstring`

**Output:** `Iconv`
**Pragmas:** `importc`, `header: "<iconv.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### if_freenameindex

[ref: #symbol-if-freenameindex]

**Input:**
- `a1: ptr Tif_nameindex`

**Output:** *(none)*
**Pragmas:** `importc`, `header: "<net/if.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### if_indextoname

[ref: #symbol-if-indextoname]

**Input:**
- `a1: cint`
- `a2: cstring`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<net/if.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### if_nameindex

[ref: #symbol-if-nameindex]

**Input:**
- *(none)*

**Output:** `ptr Tif_nameindex`
**Pragmas:** `importc`, `header: "<net/if.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### if_nametoindex

[ref: #symbol-if-nametoindex]

**Input:**
- `a1: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<net/if.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### IN6_IS_ADDR_LINKLOCAL

[ref: #symbol-in6-is-addr-linklocal]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unicast link-local address.

### IN6_IS_ADDR_LOOPBACK

[ref: #symbol-in6-is-addr-loopback]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Loopback address.

### IN6_IS_ADDR_MC_GLOBAL

[ref: #symbol-in6-is-addr-mc-global]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Multicast global address.

### IN6_IS_ADDR_MC_LINKLOCAL

[ref: #symbol-in6-is-addr-mc-linklocal]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Multicast link-local address.

### IN6_IS_ADDR_MC_NODELOCAL

[ref: #symbol-in6-is-addr-mc-nodelocal]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Multicast node-local address.

### IN6_IS_ADDR_MC_ORGLOCAL

[ref: #symbol-in6-is-addr-mc-orglocal]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Multicast organization-local address.

### IN6_IS_ADDR_MC_SITELOCAL

[ref: #symbol-in6-is-addr-mc-sitelocal]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Multicast site-local address.

### IN6_IS_ADDR_MULTICAST

[ref: #symbol-in6-is-addr-multicast]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Multicast address.

### IN6_IS_ADDR_SITELOCAL

[ref: #symbol-in6-is-addr-sitelocal]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unicast site-local address.

### IN6_IS_ADDR_UNSPECIFIED

[ref: #symbol-in6-is-addr-unspecified]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Unspecified address.

### IN6_IS_ADDR_V4COMPAT

[ref: #symbol-in6-is-addr-v4compat]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

IPv4-compatible address.

### IN6_IS_ADDR_V4MAPPED

[ref: #symbol-in6-is-addr-v4mapped]

**Input:**
- `a1: ptr In6Addr`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

IPv4 mapped address.

### IN6ADDR_ANY_INIT

[ref: #symbol-in6addr-any-init]

**Input:**
- *(none)*

**Output:** `In6Addr`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### IN6ADDR_LOOPBACK_INIT

[ref: #symbol-in6addr-loopback-init]

**Input:**
- *(none)*

**Output:** `In6Addr`
**Pragmas:** `importc`, `header: "<netinet/in.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### inet_addr

[ref: #symbol-inet-addr]

**Input:**
- `a1: cstring`

**Output:** `InAddrT`
**Pragmas:** `importc`, `header: "<arpa/inet.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### inet_ntoa

[ref: #symbol-inet-ntoa]

**Input:**
- `a1: InAddr`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<arpa/inet.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### inet_ntop

[ref: #symbol-inet-ntop]

**Input:**
- `a1: cint`
- `a2: pointer | ptr InAddr | ptr In6Addr`
- `a3: cstring`
- `a4: int32`

**Output:** `cstring`
**Generic parameters:** `a2:type`

**Pragmas:** `importc: "(char *)$1"`, `header: "<arpa/inet.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### inet_pton

[ref: #symbol-inet-pton]

**Input:**
- `a1: cint`
- `a2: cstring`
- `a3: pointer | ptr InAddr | ptr In6Addr`

**Output:** `cint`
**Generic parameters:** `a3:type`

**Pragmas:** `importc`, `header: "<arpa/inet.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ioctl

[ref: #symbol-ioctl]

**Input:**
- `f: FileHandle`
- `device: uint`

**Output:** `int`
**Pragmas:** `importc: "ioctl"`, `header: "<sys/ioctl.h>"`, `varargs`, `tags: [WriteIOEffect]`, `raises: []`, `forbids: []`

**Effects:** `tags: WriteIOEffect`, `raises: `, `forbids: `

A system call for device-specific input/output operations and other operations which cannot be expressed by regular system calls

### isatty

[ref: #symbol-isatty]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### kill

[ref: #symbol-kill]

**Input:**
- `a1: Pid`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### killpg

[ref: #symbol-killpg]

**Input:**
- `a1: Pid`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<signal.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### lchmod

[ref: #symbol-lchmod]

**Input:**
- `a1: cstring`
- `a2: Mode`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### lchown

[ref: #symbol-lchown]

**Input:**
- `a1: cstring`
- `a2: Uid`
- `a3: Gid`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### link

[ref: #symbol-link]

**Input:**
- `a1: cstring`
- `a2: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### listen

[ref: #symbol-listen]

**Input:**
- `a1: SocketHandle`
- `a2: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/socket.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### localeconv

[ref: #symbol-localeconv]

**Input:**
- *(none)*

**Output:** `ptr Lconv`
**Pragmas:** `importc`, `header: "<locale.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### localtime

[ref: #symbol-localtime]

**Input:**
- `a1: var Time`

**Output:** `ptr Tm`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### localtime_r

[ref: #symbol-localtime-r]

**Input:**
- `a1: var Time`
- `a2: var Tm`

**Output:** `ptr Tm`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### lockf

[ref: #symbol-lockf]

**Input:**
- `a1: cint`
- `a2: cint`
- `a3: Off`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### lseek

[ref: #symbol-lseek]

**Input:**
- `a1: cint`
- `a2: Off`
- `a3: cint`

**Output:** `Off`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### lstat

[ref: #symbol-lstat]

**Input:**
- `a1: cstring`
- `a2: var Stat`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### makecontext

[ref: #symbol-makecontext]

**Input:**
- `a1: var Ucontext`
- `a4: proc () {.noconv.}`
- `a3: cint`

**Output:** *(none)*
**Pragmas:** `varargs`, `importc`, `header: "<ucontext.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mkdir

[ref: #symbol-mkdir]

**Input:**
- `a1: cstring`
- `a2: Mode`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Use [os.createDir()](os.html#createDir,string) and similar.

### mkdtemp

[ref: #symbol-mkdtemp]

**Input:**
- `tmpl: cstring`

**Output:** `pointer`
**Pragmas:** `importc`, `header: "<stdlib.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mkfifo

[ref: #symbol-mkfifo]

**Input:**
- `a1: cstring`
- `a2: Mode`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mknod

[ref: #symbol-mknod]

**Input:**
- `a1: cstring`
- `a2: Mode`
- `a3: Dev`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/stat.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mkostemp

[ref: #symbol-mkostemp]

**Input:**
- `tmpl: cstring`
- `oflags: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<stdlib.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mkostemps

[ref: #symbol-mkostemps]

**Input:**
- `tmpl: cstring`
- `suffixlen: cint`
- `oflags: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<stdlib.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mkstemp

[ref: #symbol-mkstemp]

Creates a unique temporary file.

**Input:**
- `tmpl: cstring`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<stdlib.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a unique temporary file.

**Warning:**
The tmpl argument is written to by mkstemp and thus can't be a string literal. If in doubt make a copy of the cstring before passing it in.

### mkstemps

[ref: #symbol-mkstemps]

Creates a unique temporary file.

**Input:**
- `tmpl: cstring`
- `suffixlen: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<stdlib.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Creates a unique temporary file.

**Warning:**
The tmpl argument is written to by mkstemps and thus can't be a string literal. If in doubt make a copy of the cstring before passing it in.

### mktime

[ref: #symbol-mktime]

**Input:**
- `a1: var Tm`

**Output:** `Time`
**Pragmas:** `importc`, `header: "<time.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mlock

[ref: #symbol-mlock]

**Input:**
- `a1: pointer`
- `a2: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mlockall

[ref: #symbol-mlockall]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mmap

[ref: #symbol-mmap]

**Input:**
- `a1: pointer`
- `a2: int`
- `a3: cint`
- `a4: cint`
- `a5: cint`
- `a6: Off`

**Output:** `pointer`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### mprotect

[ref: #symbol-mprotect]

**Input:**
- `a1: pointer`
- `a2: int`
- `a3: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### msync

[ref: #symbol-msync]

**Input:**
- `a1: pointer`
- `a2: int`
- `a3: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### munlock

[ref: #symbol-munlock]

**Input:**
- `a1: pointer`
- `a2: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### munlockall

[ref: #symbol-munlockall]

**Input:**
- *(none)*

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### munmap

[ref: #symbol-munmap]

**Input:**
- `a1: pointer`
- `a2: int`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<sys/mman.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### nanosleep

[ref: #symbol-nanosleep]

**Input:**
- `a1: var Timespec`
- `a2: var Timespec`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<time.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### nftw

[ref: #symbol-nftw]

**Input:**
- `a1: cstring`
- `a2: proc (x1: cstring; x2: ptr Stat; x3: cint; x4: ptr FTW): cint {.noconv.}`
- `a3: cint`
- `a4: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<ftw.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### nice

[ref: #symbol-nice]

**Input:**
- `a1: cint`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### nl_langinfo

[ref: #symbol-nl-langinfo]

**Input:**
- `a1: Nl_item`

**Output:** `cstring`
**Pragmas:** `importc`, `header: "<langinfo.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ntohl

[ref: #symbol-ntohl]

**Input:**
- `a1: uint32`

**Output:** `uint32`
**Pragmas:** `importc`, `header: "<arpa/inet.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ntohs

[ref: #symbol-ntohs]

**Input:**
- `a1: uint16`

**Output:** `uint16`
**Pragmas:** `importc`, `header: "<arpa/inet.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### open

[ref: #symbol-open]

**Input:**
- `a1: cstring`
- `a2: cint`
- `mode: Mode | cint = 0.Mode`

**Output:** `cint`
**Generic parameters:** `mode:type`

**Pragmas:** `inline`

### opendir

[ref: #symbol-opendir]

**Input:**
- `a1: cstring`

**Output:** `ptr DIR`
**Pragmas:** `importc`, `header: "<dirent.h>"`, `sideEffect`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pathconf

[ref: #symbol-pathconf]

**Input:**
- `a1: cstring`
- `a2: cint`

**Output:** `int`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pause

[ref: #symbol-pause]

**Input:**
- *(none)*

**Output:** `cint`
**Pragmas:** `importc`, `header: "<unistd.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### pclose

[ref: #symbol-pclose]

**Input:**
- `a: File`

**Output:** `cint`
**Pragmas:** `importc`, `header: "<stdio.h>"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Prev](posix_2.md) | [Next](posix_4.md)
