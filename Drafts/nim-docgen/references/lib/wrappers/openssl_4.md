---
source_hash: c7314b291543d173
source_path: lib/wrappers/openssl.nim
---

### sslWrite

[ref: #symbol-sslwrite]

**Input:**
- `ssl: SslPtr`
- `buf: cstring`
- `num: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc: "SSL_write"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### TLS_client_method

[ref: #symbol-tls-client-method]

**Input:**
- *(none)*

**Output:** `PSSL_METHOD`
**Pragmas:** `raises: [LibraryError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError`, `tags: RootEffect`, `forbids: `

### TLS_method

[ref: #symbol-tls-method]

**Input:**
- *(none)*

**Output:** `PSSL_METHOD`
**Pragmas:** `raises: [LibraryError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError`, `tags: RootEffect`, `forbids: `

### TLS_server_method

[ref: #symbol-tls-server-method]

**Input:**
- *(none)*

**Output:** `PSSL_METHOD`
**Pragmas:** `raises: [LibraryError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError`, `tags: RootEffect`, `forbids: `

### TLSv1_method

[ref: #symbol-tlsv1-method]

**Input:**
- *(none)*

**Output:** `PSSL_METHOD`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_check_host

[ref: #symbol-x509-check-host]

**Input:**
- `cert: PX509`
- `name: cstring`
- `namelen: cint`
- `flags: cuint`
- `peername: cstring`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_free

[ref: #symbol-x509-free]

**Input:**
- `cert: PX509`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_get_issuer_name

[ref: #symbol-x509-get-issuer-name]

**Input:**
- `a: PX509`

**Output:** `PX509_NAME`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_get_subject_name

[ref: #symbol-x509-get-subject-name]

**Input:**
- `a: PX509`

**Output:** `PX509_NAME`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_NAME_get_text_by_NID

[ref: #symbol-x509-name-get-text-by-nid]

**Input:**
- `subject: cstring`
- `NID: cint`
- `buf: cstring`
- `size: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_NAME_oneline

[ref: #symbol-x509-name-oneline]

**Input:**
- `a: PX509_NAME`
- `buf: cstring`
- `size: cint`

**Output:** `cstring`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_OBJECT_free

[ref: #symbol-x509-object-free]

**Input:**
- `a: PX509_OBJECT`

**Output:** *(none)*
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_OBJECT_new

[ref: #symbol-x509-object-new]

**Input:**
- *(none)*

**Output:** `PX509_OBJECT`
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_STORE_add_cert

[ref: #symbol-x509-store-add-cert]

**Input:**
- `ctx: PX509_STORE`
- `x: PX509`

**Output:** `cint`
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_STORE_free

[ref: #symbol-x509-store-free]

**Input:**
- `v: PX509_STORE`

**Output:** *(none)*
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_STORE_lock

[ref: #symbol-x509-store-lock]

**Input:**
- `ctx: PX509_STORE`

**Output:** `cint`
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_STORE_new

[ref: #symbol-x509-store-new]

**Input:**
- *(none)*

**Output:** `PX509_STORE`
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_STORE_set_flags

[ref: #symbol-x509-store-set-flags]

**Input:**
- `ctx: PX509_STORE`
- `flags: culong`

**Output:** `cint`
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_STORE_set_purpose

[ref: #symbol-x509-store-set-purpose]

**Input:**
- `ctx: PX509_STORE`
- `purpose: cint`

**Output:** `cint`
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_STORE_set_trust

[ref: #symbol-x509-store-set-trust]

**Input:**
- `ctx: PX509_STORE`
- `trust: cint`

**Output:** `cint`
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_STORE_unlock

[ref: #symbol-x509-store-unlock]

**Input:**
- `ctx: PX509_STORE`

**Output:** `cint`
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### X509_STORE_up_ref

[ref: #symbol-x509-store-up-ref]

**Input:**
- `v: PX509_STORE`

**Output:** `cint`
**Pragmas:** `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

## Type

### BIO

[ref: #symbol-bio]

```nim
BIO = SslPtr
```

### DES_cblock

[ref: #symbol-des-cblock]

```nim
DES_cblock = array[0 .. 7, int8]
```

### des_key_schedule

[ref: #symbol-des-key-schedule]

```nim
des_key_schedule = array[1 .. 16, des_ks_struct]
```

### des_ks_struct

[ref: #symbol-des-ks-struct]

```nim
des_ks_struct {.final.} = object
  ks*: DES_cblock
  weak_key*: cint
```

### ENGINE

[ref: #symbol-engine]

```nim
ENGINE = SslPtr
```

### EVP_MD

[ref: #symbol-evp-md]

```nim
EVP_MD = SslPtr
```

### EVP_MD_CTX

[ref: #symbol-evp-md-ctx]

```nim
EVP_MD_CTX = SslPtr
```

### EVP_PKEY

[ref: #symbol-evp-pkey]

```nim
EVP_PKEY = SslPtr
```

### EVP_PKEY_CTX

[ref: #symbol-evp-pkey-ctx]

```nim
EVP_PKEY_CTX = SslPtr
```

### MD5_CTX

[ref: #symbol-md5-ctx]

```nim
MD5_CTX = object
```

### MD5_LONG

[ref: #symbol-md5-long]

```nim
MD5_LONG = cuint
```

### PaddingType

[ref: #symbol-paddingtype]

```nim
PaddingType = enum
  RSA_PKCS1_PADDING = 1, RSA_SSLV23_PADDING = 2, RSA_NO_PADDING = 3,
  RSA_PKCS1_OAEP_PADDING = 4, RSA_X931_PADDING = 5, RSA_PKCS1_PSS_PADDING = 6
```

### PASN1_cInt

[ref: #symbol-pasn1-cint]

```nim
PASN1_cInt = SslPtr
```

### PASN1_UTCTIME

[ref: #symbol-pasn1-utctime]

```nim
PASN1_UTCTIME = SslPtr
```

### PBIO_METHOD

[ref: #symbol-pbio-method]

```nim
PBIO_METHOD = SslPtr
```

### PDES_cblock

[ref: #symbol-pdes-cblock]

```nim
PDES_cblock = ptr DES_cblock
```

### pem_password_cb

[ref: #symbol-pem-password-cb]

```nim
pem_password_cb = proc (buf: cstring; size, rwflag: cint; userdata: pointer): cint {.
    cdecl.}
```

### PFunction

[ref: #symbol-pfunction]

```nim
PFunction = proc () {.cdecl.}
```

### PPasswdCb

[ref: #symbol-ppasswdcb]

```nim
PPasswdCb = SslPtr
```

### PRSA

[ref: #symbol-prsa]

```nim
PRSA = SslPtr
```

### PskClientCallback

[ref: #symbol-pskclientcallback]

```nim
PskClientCallback = proc (ssl: SslPtr; hint: cstring; identity: cstring;
                          max_identity_len: cuint; psk: ptr uint8;
                          max_psk_len: cuint): cuint {.cdecl.}
```

### PskServerCallback

[ref: #symbol-pskservercallback]

```nim
PskServerCallback = proc (ssl: SslPtr; identity: cstring; psk: ptr uint8;
                          max_psk_len: cint): cuint {.cdecl.}
```

### PSSL_METHOD

[ref: #symbol-pssl-method]

```nim
PSSL_METHOD = SslPtr
```

### PSslPtr

[ref: #symbol-psslptr]

```nim
PSslPtr = ptr SslPtr
```

### PSTACK

[ref: #symbol-pstack]

```nim
PSTACK = SslPtr
```

### PX509

[ref: #symbol-px509]

```nim
PX509 = SslPtr
```

### PX509_NAME

[ref: #symbol-px509-name]

```nim
PX509_NAME = SslPtr
```

### PX509_OBJECT

[ref: #symbol-px509-object]

```nim
PX509_OBJECT = SslPtr
```

### PX509_STORE

[ref: #symbol-px509-store]

```nim
PX509_STORE = SslPtr
```

### SslCtx

[ref: #symbol-sslctx]

```nim
SslCtx = SslPtr
```

### SslPtr

[ref: #symbol-sslptr]

```nim
SslPtr = ptr SslStruct
```

[Prev](openssl_3.md)
