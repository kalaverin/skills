---
source_hash: c7314b291543d173
source_path: lib/wrappers/openssl.nim
---

### BIO_do_connect

[ref: #symbol-bio-do-connect]

**Input:**
- `bio: BIO`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### BIO_do_handshake

[ref: #symbol-bio-do-handshake]

**Input:**
- `bio: BIO`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### BIO_free

[ref: #symbol-bio-free]

**Input:**
- `b: BIO`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### BIO_get_ssl

[ref: #symbol-bio-get-ssl]

**Input:**
- `bio: BIO`
- `ssl: ptr SslPtr`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### BIO_new_mem_buf

[ref: #symbol-bio-new-mem-buf]

**Input:**
- `data: pointer`
- `len: cint`

**Output:** `BIO`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### BIO_new_ssl_connect

[ref: #symbol-bio-new-ssl-connect]

**Input:**
- `ctx: SslCtx`

**Output:** `BIO`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### BIO_read

[ref: #symbol-bio-read]

**Input:**
- `b: BIO`
- `data: cstring`
- `length: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### BIO_set_conn_hostname

[ref: #symbol-bio-set-conn-hostname]

**Input:**
- `bio: BIO`
- `name: cstring`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### BIO_write

[ref: #symbol-bio-write]

**Input:**
- `b: BIO`
- `data: cstring`
- `length: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### bioCtrlPending

[ref: #symbol-bioctrlpending]

**Input:**
- `b: BIO`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc: "BIO_ctrl_pending"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### bioFreeAll

[ref: #symbol-biofreeall]

**Input:**
- `b: BIO`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc: "BIO_free_all"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### bioNew

[ref: #symbol-bionew]

**Input:**
- `b: PBIO_METHOD`

**Output:** `BIO`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc: "BIO_new"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### bioRead

[ref: #symbol-bioread]

**Input:**
- `b: BIO`
- `Buf: cstring`
- `length: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc: "BIO_read"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### bioSMem

[ref: #symbol-biosmem]

**Input:**
- *(none)*

**Output:** `PBIO_METHOD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc: "BIO_s_mem"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### bioWrite

[ref: #symbol-biowrite]

**Input:**
- `b: BIO`
- `Buf: cstring`
- `length: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc: "BIO_write"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### CRYPTO_malloc_init

[ref: #symbol-crypto-malloc-init]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### d2i_X509

[ref: #symbol-d2i-x509]

**Input:**
- `px: ptr PX509`
- `i: ptr ptr uint8`
- `len: cint`

**Output:** `PX509`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### d2i_X509

[ref: #symbol-d2i-x509]

**Input:**
- `b: string`

**Output:** `PX509`
**Pragmas:** `raises: [Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: Exception`, `tags: `, `forbids: `

decode DER/BER bytestring into X.509 certificate struct

### ERR_error_string

[ref: #symbol-err-error-string]

**Input:**
- `e: culong`
- `buf: cstring`

**Output:** `cstring`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ERR_get_error

[ref: #symbol-err-get-error]

**Input:**
- *(none)*

**Output:** `culong`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ERR_load_BIO_strings

[ref: #symbol-err-load-bio-strings]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

### ERR_peek_last_error

[ref: #symbol-err-peek-last-error]

**Input:**
- *(none)*

**Output:** `culong`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ERR_print_errors_fp

[ref: #symbol-err-print-errors-fp]

**Input:**
- `fp: File`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ErrClearError

[ref: #symbol-errclearerror]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc: "ERR_clear_error"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ErrFreeStrings

[ref: #symbol-errfreestrings]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc: "ERR_free_strings"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### ErrRemoveState

[ref: #symbol-errremovestate]

**Input:**
- `pid: cint`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc: "ERR_remove_state"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_DigestFinal_ex

[ref: #symbol-evp-digestfinal-ex]

**Input:**
- `ctx: EVP_MD_CTX`
- `buffer: pointer`
- `size: ptr cuint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_DigestInit_ex

[ref: #symbol-evp-digestinit-ex]

**Input:**
- `ctx: EVP_MD_CTX`
- `typ: EVP_MD`
- `engine: SslPtr = nil`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_DigestSignFinal

[ref: #symbol-evp-digestsignfinal]

**Input:**
- `ctx: EVP_MD_CTX`
- `data: pointer`
- `len: ptr csize_t`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_DigestSignInit

[ref: #symbol-evp-digestsigninit]

**Input:**
- `ctx: EVP_MD_CTX`
- `pctx: ptr EVP_PKEY_CTX`
- `typ: EVP_MD`
- `e: ENGINE`
- `pkey: EVP_PKEY`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_DigestUpdate

[ref: #symbol-evp-digestupdate]

**Input:**
- `ctx: EVP_MD_CTX`
- `data: pointer`
- `len: cuint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_dss

[ref: #symbol-evp-dss]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_dss1

[ref: #symbol-evp-dss1]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_ecdsa

[ref: #symbol-evp-ecdsa]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_md2

[ref: #symbol-evp-md2]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_md4

[ref: #symbol-evp-md4]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_md5

[ref: #symbol-evp-md5]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_MD_CTX_cleanup

[ref: #symbol-evp-md-ctx-cleanup]

**Input:**
- `ctx: EVP_MD_CTX`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_MD_CTX_create

[ref: #symbol-evp-md-ctx-create]

**Input:**
- *(none)*

**Output:** `EVP_MD_CTX`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_MD_CTX_destroy

[ref: #symbol-evp-md-ctx-destroy]

**Input:**
- `ctx: EVP_MD_CTX`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_md_null

[ref: #symbol-evp-md-null]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_MD_size

[ref: #symbol-evp-md-size]

**Input:**
- `md: EVP_MD`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_mdc2

[ref: #symbol-evp-mdc2]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_PKEY_CTX_free

[ref: #symbol-evp-pkey-ctx-free]

**Input:**
- `pkeyCtx: EVP_PKEY_CTX`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_PKEY_CTX_new

[ref: #symbol-evp-pkey-ctx-new]

**Input:**
- `pkey: EVP_PKEY`
- `e: ENGINE`

**Output:** `EVP_PKEY_CTX`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_PKEY_free

[ref: #symbol-evp-pkey-free]

**Input:**
- `p: EVP_PKEY`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_PKEY_sign_init

[ref: #symbol-evp-pkey-sign-init]

**Input:**
- `c: EVP_PKEY_CTX`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_ripemd160

[ref: #symbol-evp-ripemd160]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_sha

[ref: #symbol-evp-sha]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_sha1

[ref: #symbol-evp-sha1]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_sha224

[ref: #symbol-evp-sha224]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_sha256

[ref: #symbol-evp-sha256]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_sha384

[ref: #symbol-evp-sha384]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_sha512

[ref: #symbol-evp-sha512]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### EVP_whirlpool

[ref: #symbol-evp-whirlpool]

**Input:**
- *(none)*

**Output:** `EVP_MD`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### getOpenSSLVersion

[ref: #symbol-getopensslversion]

**Input:**
- *(none)*

**Output:** `culong`
**Pragmas:** `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Return OpenSSL version as unsigned long or 0 if not available

### HMAC

[ref: #symbol-hmac]

**Input:**
- `evp_md: EVP_MD`
- `key: pointer`
- `key_len: cint`
- `d: cstring`
- `n: csize_t`
- `md: cstring`
- `md_len: ptr cuint`

**Output:** `cstring`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### i2d_X509

[ref: #symbol-i2d-x509]

**Input:**
- `cert: PX509`
- `o: ptr ptr uint8`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### i2d_X509

[ref: #symbol-i2d-x509]

**Input:**
- `cert: PX509`

**Output:** `string`
**Pragmas:** `raises: [Exception]`, `tags: []`, `forbids: []`

**Effects:** `raises: Exception`, `tags: `, `forbids: `

encode cert to DER string

### md5

[ref: #symbol-md5]

**Input:**
- `d: ptr uint8`
- `n: csize_t`
- `md: ptr uint8`

**Output:** `ptr uint8`
**Pragmas:** `importc: "MD5"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### md5_File

[ref: #symbol-md5-file]

**Input:**
- `file: string`

**Output:** `string`
**Pragmas:** `raises: [IOError, Exception]`, `tags: [ReadIOEffect]`, `forbids: []`

**Effects:** `raises: IOError, Exception`, `tags: ReadIOEffect`, `forbids: `

Generate MD5 hash for a file. Result is a 32 character

### md5_Final

[ref: #symbol-md5-final]

**Input:**
- `md: cstring`
- `c: var MD5_CTX`

**Output:** `cint`
**Pragmas:** `importc: "MD5_Final"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### md5_Init

[ref: #symbol-md5-init]

**Input:**
- `c: var MD5_CTX`

**Output:** `cint`
**Pragmas:** `importc: "MD5_Init"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### md5_Str

[ref: #symbol-md5-str]

**Input:**
- `str: string`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Generate MD5 hash for a string. Result is a 32 character hex string with lowercase characters

### md5_Transform

[ref: #symbol-md5-transform]

**Input:**
- `c: var MD5_CTX`
- `b: ptr uint8`

**Output:** *(none)*
**Pragmas:** `importc: "MD5_Transform"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### md5_Update

[ref: #symbol-md5-update]

**Input:**
- `c: var MD5_CTX`
- `data: pointer`
- `len: csize_t`

**Output:** `cint`
**Pragmas:** `importc: "MD5_Update"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### OpenSSL_add_all_algorithms

[ref: #symbol-openssl-add-all-algorithms]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: [LibraryError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError, Exception`, `tags: RootEffect`, `forbids: `

### OPENSSL_config

[ref: #symbol-openssl-config]

**Input:**
- `configName: cstring`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### OPENSSL_sk_num

[ref: #symbol-openssl-sk-num]

**Input:**
- `stack: PSTACK`

**Output:** `int`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### OPENSSL_sk_value

[ref: #symbol-openssl-sk-value]

**Input:**
- `stack: PSTACK`
- `index: int`

**Output:** `pointer`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### PEM_read_bio_PrivateKey

[ref: #symbol-pem-read-bio-privatekey]

**Input:**
- `bp: BIO`
- `x: ptr EVP_PKEY`
- `cb: pointer`
- `u: pointer`

**Output:** `EVP_PKEY`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### PEM_read_bio_RSA_PUBKEY

[ref: #symbol-pem-read-bio-rsa-pubkey]

**Input:**
- `bp: BIO`
- `x: ptr PRSA`
- `pw: pem_password_cb`
- `u: pointer`

**Output:** `PRSA`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### PEM_read_bio_RSAPrivateKey

[ref: #symbol-pem-read-bio-rsaprivatekey]

**Input:**
- `bp: BIO`
- `x: ptr PRSA`
- `cb: pem_password_cb`
- `u: pointer`

**Output:** `PRSA`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### PEM_read_bio_RSAPublicKey

[ref: #symbol-pem-read-bio-rsapublickey]

**Input:**
- `bp: BIO`
- `x: ptr PRSA`
- `cb: pem_password_cb`
- `u: pointer`

**Output:** `PRSA`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### PEM_read_RSA_PUBKEY

[ref: #symbol-pem-read-rsa-pubkey]

**Input:**
- `fp: pointer`
- `x: ptr PRSA`
- `cb: pem_password_cb`
- `u: pointer`

**Output:** `PRSA`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### PEM_read_RSAPrivateKey

[ref: #symbol-pem-read-rsaprivatekey]

**Input:**
- `fp: pointer`
- `x: ptr PRSA`
- `cb: pem_password_cb`
- `u: pointer`

**Output:** `PRSA`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Prev](openssl_1.md) | [Next](openssl_3.md)
