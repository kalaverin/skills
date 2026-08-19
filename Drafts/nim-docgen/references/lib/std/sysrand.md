---
source_hash: 6947410dd4b0b083
source_path: lib/std/sysrand.nim
---

# sysrand

[ref: #module-sysrand]

**Warning:**
This module was added in Nim 1.6. If you are using it for cryptographic purposes, keep in mind that so far this has not been audited by any security professionals, therefore may not be secure.

std/sysrand generates random numbers from a secure source provided by the operating system. It is a cryptographically secure pseudorandom number generator and should be unpredictable enough for cryptographic applications, though its exact quality depends on the OS implementation.

| Targets | Implementation |
| --- | --- |
| Windows | [BCryptGenRandom](https://docs.microsoft.com/en-us/windows/win32/api/bcrypt/nf-bcrypt-bcryptgenrandom) |
| Linux | [getrandom](https://man7.org/linux/man-pages/man2/getrandom.2.html) |
| MacOSX | [SecRandomCopyBytes](https://developer.apple.com/documentation/security/1399291-secrandomcopybytes?language=objc) |
| iOS | [SecRandomCopyBytes](https://developer.apple.com/documentation/security/1399291-secrandomcopybytes?language=objc) |
| OpenBSD | [getentropy openbsd](https://man.openbsd.org/getentropy.2) |
| FreeBSD | [getrandom freebsd](https://www.freebsd.org/cgi/man.cgi?query=getrandom&manpath=FreeBSD+12.0-stable) |
| JS (Web Browser) | [getRandomValues](https://www.w3.org/TR/WebCryptoAPI/#Crypto-method-getRandomValues) |
| Node.js | [randomFillSync](https://nodejs.org/api/crypto.html#crypto_crypto_randomfillsync_buffer_offset_size) |
| Other Unix platforms | [/dev/urandom](https://en.wikipedia.org/wiki//dev/random) |

On a Linux target, a call to the getrandom syscall can be avoided (e.g. for targets running kernel version < 3.17) by passing a compile flag of -d:nimNoGetRandom. If this flag is passed, sysrand will use /dev/urandom as with any other POSIX compliant OS.

# [See also](#see-also)

* [random module](random.html)

## Examples

```nim
import std/sysrand
doAssert urandom(0).len == 0
doAssert urandom(113).len == 113
doAssert urandom(1234) != urandom(1234) # unlikely to fail in practice
```

## Proc

### urandom

[ref: #symbol-urandom]

Fills dest with random bytes suitable for cryptographic use. If the call succeeds, returns true.

**Input:**
- `dest: var openArray[byte]`

**Output:** `bool`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Fills dest with random bytes suitable for cryptographic use. If the call succeeds, returns true.

If dest is empty, urandom immediately returns success, without calling the underlying operating system API.

**Warning:**
The code hasn't been audited by cryptography experts and is provided as-is without guarantees. Use at your own risks. For production systems we advise you to request an external audit.

### urandom

[ref: #symbol-urandom]

Returns random bytes suitable for cryptographic use.

**Input:**
- `size: Natural`

**Output:** `seq[byte]`
**Pragmas:** `inline`, `raises: [OSError]`, `tags: []`, `forbids: []`

**Effects:** `raises: OSError`, `tags: `, `forbids: `

Returns random bytes suitable for cryptographic use.

**Warning:**
The code hasn't been audited by cryptography experts and is provided as-is without guarantees. Use at your own risks. For production systems we advise you to request an external audit.
