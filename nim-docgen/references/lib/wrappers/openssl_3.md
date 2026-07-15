---
source_hash: c7314b291543d173
source_path: lib/wrappers/openssl.nim
---

### PEM_read_RSAPublicKey

[ref: #symbol-pem-read-rsapublickey]

**Input:**
- `fp: pointer`
- `x: ptr PRSA`
- `cb: pem_password_cb`
- `u: pointer`

**Output:** `PRSA`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### RSA_free

[ref: #symbol-rsa-free]

**Input:**
- `rsa: PRSA`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### RSA_private_decrypt

[ref: #symbol-rsa-private-decrypt]

**Input:**
- `flen: cint`
- `fr: ptr uint8`
- `to: ptr uint8`
- `rsa: PRSA`
- `padding: PaddingType`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### RSA_private_encrypt

[ref: #symbol-rsa-private-encrypt]

**Input:**
- `flen: cint`
- `fr: ptr uint8`
- `to: ptr uint8`
- `rsa: PRSA`
- `padding: PaddingType`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### RSA_public_decrypt

[ref: #symbol-rsa-public-decrypt]

**Input:**
- `flen: cint`
- `fr: ptr uint8`
- `to: ptr uint8`
- `rsa: PRSA`
- `padding: PaddingType`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### RSA_public_encrypt

[ref: #symbol-rsa-public-encrypt]

**Input:**
- `flen: cint`
- `fr: ptr uint8`
- `to: ptr uint8`
- `rsa: PRSA`
- `padding: PaddingType`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### RSA_size

[ref: #symbol-rsa-size]

**Input:**
- `rsa: PRSA`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### RSA_verify

[ref: #symbol-rsa-verify]

**Input:**
- `kind: cint`
- `origMsg: pointer`
- `origMsgLen: cuint`
- `signature: pointer`
- `signatureLen: cuint`
- `rsa: PRSA`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_accept

[ref: #symbol-ssl-accept]

**Input:**
- `ssl: SslPtr`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_connect

[ref: #symbol-ssl-connect]

**Input:**
- `ssl: SslPtr`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_ctrl

[ref: #symbol-ssl-ctrl]

**Input:**
- `ssl: SslPtr`
- `cmd: cint`
- `larg: int`
- `parg: pointer`

**Output:** `int`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_check_private_key

[ref: #symbol-ssl-ctx-check-private-key]

**Input:**
- `ctx: SslCtx`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_ctrl

[ref: #symbol-ssl-ctx-ctrl]

**Input:**
- `ctx: SslCtx`
- `cmd: cint`
- `larg: clong`
- `parg: pointer`

**Output:** `clong`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_free

[ref: #symbol-ssl-ctx-free]

**Input:**
- `arg0: SslCtx`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_get_ex_data

[ref: #symbol-ssl-ctx-get-ex-data]

**Input:**
- `ssl: SslCtx`
- `idx: cint`

**Output:** `pointer`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_get_ex_new_index

[ref: #symbol-ssl-ctx-get-ex-new-index]

**Input:**
- `argl: clong`
- `argp: pointer`
- `new_func: pointer`
- `dup_func: pointer`
- `free_func: pointer`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_load_verify_locations

[ref: #symbol-ssl-ctx-load-verify-locations]

**Input:**
- `ctx: SslCtx`
- `CAfile: cstring`
- `CApath: cstring`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_new

[ref: #symbol-ssl-ctx-new]

**Input:**
- `meth: PSSL_METHOD`

**Output:** `SslCtx`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_set_alpn_protos

[ref: #symbol-ssl-ctx-set-alpn-protos]

**Input:**
- `ctx: SslCtx`
- `protos: cstring`
- `protos_len: cuint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_set_alpn_select_cb

[ref: #symbol-ssl-ctx-set-alpn-select-cb]

**Input:**
- `ctx: SslCtx`
- `cb: proc (ssl: SslPtr; out_proto: ptr cstring; outlen: cstring; in_proto: cstring;
      inlen: cuint; arg: pointer): cint {.cdecl.}`
- `arg: pointer`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_set_cipher_list

[ref: #symbol-ssl-ctx-set-cipher-list]

**Input:**
- `s: SslCtx`
- `ciphers: cstring`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_set_ciphersuites

[ref: #symbol-ssl-ctx-set-ciphersuites]

**Input:**
- `ctx: SslCtx`
- `str: cstring`

**Output:** `cint`
**Pragmas:** `raises: [LibraryError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError, Exception`, `tags: RootEffect`, `forbids: `

### SSL_CTX_set_ecdh_auto

[ref: #symbol-ssl-ctx-set-ecdh-auto]

Set automatic curve selection.

**Input:**
- `ctx: SslCtx`
- `onoff: cint`

**Output:** `cint`
**Pragmas:** `inline`, `raises: [Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: Exception`, `tags: RootEffect`, `forbids: `

Set automatic curve selection.

On OpenSSL >= 1.1.0 this is on by default and cannot be disabled.

### SSL_CTX_set_ex_data

[ref: #symbol-ssl-ctx-set-ex-data]

**Input:**
- `ssl: SslCtx`
- `idx: cint`
- `arg: pointer`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_set_next_proto_select_cb

[ref: #symbol-ssl-ctx-set-next-proto-select-cb]

**Input:**
- `ctx: SslCtx`
- `cb: proc (s: SslPtr; out_proto: cstring; outlen: cstring; in_proto: cstring;
      inlen: cuint; arg: pointer): cint {.cdecl.}`
- `arg: pointer`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_set_next_protos_advertised_cb

[ref: #symbol-ssl-ctx-set-next-protos-advertised-cb]

**Input:**
- `ctx: SslCtx`
- `cb: proc (ssl: SslPtr; out_proto: ptr cstring; outlen: ptr cuint; arg: pointer): cint {.
    cdecl.}`
- `arg: pointer`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_set_psk_client_callback

[ref: #symbol-ssl-ctx-set-psk-client-callback]

**Input:**
- `ctx: SslCtx`
- `callback: PskClientCallback`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set callback called when OpenSSL needs PSK (for client).

### SSL_CTX_set_psk_server_callback

[ref: #symbol-ssl-ctx-set-psk-server-callback]

**Input:**
- `ctx: SslCtx`
- `callback: PskServerCallback`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set callback called when OpenSSL needs PSK (for server).

### SSL_CTX_set_session_id_context

[ref: #symbol-ssl-ctx-set-session-id-context]

**Input:**
- `context: SslCtx`
- `sid_ctx: string`
- `sid_ctx_len: int`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_set_tlsext_servername_arg

[ref: #symbol-ssl-ctx-set-tlsext-servername-arg]

**Input:**
- `ctx: SslCtx`
- `arg: pointer`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set the pointer to be used in the callback registered to SSL\_CTX\_set\_tlsext\_servername\_callback.

### SSL_CTX_set_tlsext_servername_callback

[ref: #symbol-ssl-ctx-set-tlsext-servername-callback]

Set the callback to be used on listening SSL connections when the client hello is received.

**Input:**
- `ctx: SslCtx`
- `cb: proc (ssl: SslPtr; cb_id: int; arg: pointer): int {.cdecl.}`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set the callback to be used on listening SSL connections when the client hello is received.

The callback should return one of:

* SSL\_TLSEXT\_ERR\_OK
* SSL\_TLSEXT\_ERR\_ALERT\_WARNING
* SSL\_TLSEXT\_ERR\_ALERT\_FATAL
* SSL\_TLSEXT\_ERR\_NOACK

### SSL_CTX_set_verify

[ref: #symbol-ssl-ctx-set-verify]

**Input:**
- `s: SslCtx`
- `mode: int`
- `cb: proc (a: int; b: pointer): int {.cdecl.}`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_use_certificate_chain_file

[ref: #symbol-ssl-ctx-use-certificate-chain-file]

**Input:**
- `ctx: SslCtx`
- `filename: cstring`

**Output:** `cint`
**Pragmas:** `stdcall`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_use_certificate_file

[ref: #symbol-ssl-ctx-use-certificate-file]

**Input:**
- `ctx: SslCtx`
- `filename: cstring`
- `typ: cint`

**Output:** `cint`
**Pragmas:** `stdcall`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_use_PrivateKey_file

[ref: #symbol-ssl-ctx-use-privatekey-file]

**Input:**
- `ctx: SslCtx`
- `filename: cstring`
- `typ: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_CTX_use_psk_identity_hint

[ref: #symbol-ssl-ctx-use-psk-identity-hint]

**Input:**
- `ctx: SslCtx`
- `hint: cstring`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set PSK identity hint to use.

### SSL_free

[ref: #symbol-ssl-free]

**Input:**
- `ssl: SslPtr`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_get0_alpn_selected

[ref: #symbol-ssl-get0-alpn-selected]

**Input:**
- `ssl: SslPtr`
- `data: ptr cstring`
- `len: ptr cuint`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_get0_next_proto_negotiated

[ref: #symbol-ssl-get0-next-proto-negotiated]

**Input:**
- `s: SslPtr`
- `data: ptr cstring`
- `len: ptr cuint`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_get0_verified_chain

[ref: #symbol-ssl-get0-verified-chain]

**Input:**
- `ssl: SslPtr`

**Output:** `PSTACK`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_get_error

[ref: #symbol-ssl-get-error]

**Input:**
- `s: SslPtr`
- `ret_code: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_get_peer_certificate

[ref: #symbol-ssl-get-peer-certificate]

**Input:**
- `ssl: SslCtx`

**Output:** `PX509`
**Pragmas:** `raises: [LibraryError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError`, `tags: RootEffect`, `forbids: `

### SSL_get_psk_identity

[ref: #symbol-ssl-get-psk-identity]

**Input:**
- `ssl: SslPtr`

**Output:** `cstring`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Get PSK identity.

### SSL_get_servername

[ref: #symbol-ssl-get-servername]

**Input:**
- `ssl: SslPtr`
- `typ: cint = TLSEXT_NAMETYPE_host_name`

**Output:** `cstring`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Retrieve the server name requested in the client hello. This can be used in the callback set in SSL\_CTX\_set\_tlsext\_servername\_callback to implement virtual hosting. May return nil.

### SSL_get_shutdown

[ref: #symbol-ssl-get-shutdown]

**Input:**
- `ssl: SslPtr`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc: "SSL_get_shutdown"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_get_SSL_CTX

[ref: #symbol-ssl-get-ssl-ctx]

**Input:**
- `ssl: SslPtr`

**Output:** `SslCtx`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_get_verify_result

[ref: #symbol-ssl-get-verify-result]

**Input:**
- `ssl: SslPtr`

**Output:** `int`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_in_init

[ref: #symbol-ssl-in-init]

**Input:**
- `ssl: SslPtr`

**Output:** `cint`
**Pragmas:** `raises: [LibraryError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError, Exception`, `tags: RootEffect`, `forbids: `

### SSL_library_init

[ref: #symbol-ssl-library-init]

**Input:**
- *(none)*

**Output:** `cint`
**Pragmas:** `discardable`, `raises: [LibraryError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError, Exception`, `tags: RootEffect`, `forbids: `

Initialize SSL using OPENSSL\_init\_ssl for OpenSSL >= 1.1.0 otherwise SSL\_library\_init

### SSL_load_error_strings

[ref: #symbol-ssl-load-error-strings]

**Input:**
- *(none)*

**Output:** *(none)*
**Pragmas:** `raises: [LibraryError, Exception]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError, Exception`, `tags: RootEffect`, `forbids: `

### SSL_new

[ref: #symbol-ssl-new]

**Input:**
- `context: SslCtx`

**Output:** `SslPtr`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_pending

[ref: #symbol-ssl-pending]

**Input:**
- `ssl: SslPtr`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_read

[ref: #symbol-ssl-read]

**Input:**
- `ssl: SslPtr`
- `buf: pointer`
- `num: int`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_select_next_proto

[ref: #symbol-ssl-select-next-proto]

**Input:**
- `out_proto: ptr cstring`
- `outlen: cstring`
- `server: cstring`
- `server_len: cuint`
- `client: cstring`
- `client_len: cuint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_set_alpn_protos

[ref: #symbol-ssl-set-alpn-protos]

**Input:**
- `ssl: SslPtr`
- `protos: cstring`
- `protos_len: cuint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_set_fd

[ref: #symbol-ssl-set-fd]

**Input:**
- `ssl: SslPtr`
- `fd: SocketHandle`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_set_shutdown

[ref: #symbol-ssl-set-shutdown]

**Input:**
- `ssl: SslPtr`
- `mode: cint`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc: "SSL_set_shutdown"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_set_SSL_CTX

[ref: #symbol-ssl-set-ssl-ctx]

**Input:**
- `ssl: SslPtr`
- `ctx: SslCtx`

**Output:** `SslCtx`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_set_tlsext_host_name

[ref: #symbol-ssl-set-tlsext-host-name]

**Input:**
- `ssl: SslPtr`
- `name: cstring`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

Set the SNI server name extension to be used in a client hello. Returns 1 if SNI was set, 0 if current SSL configuration doesn't support SNI.

### SSL_shutdown

[ref: #symbol-ssl-shutdown]

**Input:**
- `ssl: SslPtr`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSL_write

[ref: #symbol-ssl-write]

**Input:**
- `ssl: SslPtr`
- `buf: cstring`
- `num: int`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSLCTXSetMode

[ref: #symbol-sslctxsetmode]

**Input:**
- `ctx: SslCtx`
- `mode: int`

**Output:** `int`
**Pragmas:** `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sslDoHandshake

[ref: #symbol-ssldohandshake]

**Input:**
- `ssl: SslPtr`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc: "SSL_do_handshake"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sslPeek

[ref: #symbol-sslpeek]

**Input:**
- `ssl: SslPtr`
- `buf: cstring`
- `num: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc: "SSL_peek"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sslRead

[ref: #symbol-sslread]

**Input:**
- `ssl: SslPtr`
- `buf: cstring`
- `num: cint`

**Output:** `cint`
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc: "SSL_read"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sslSetAcceptState

[ref: #symbol-sslsetacceptstate]

**Input:**
- `s: SslPtr`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc: "SSL_set_accept_state"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sslSetBio

[ref: #symbol-sslsetbio]

**Input:**
- `ssl: SslPtr`
- `rbio: BIO`
- `wbio: BIO`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc: "SSL_set_bio"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### sslSetConnectState

[ref: #symbol-sslsetconnectstate]

**Input:**
- `s: SslPtr`

**Output:** *(none)*
**Pragmas:** `cdecl`, `dynlib: DLLSSLName`, `importc: "SSL_set_connect_state"`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `

### SSLv23_client_method

[ref: #symbol-sslv23-client-method]

**Input:**
- *(none)*

**Output:** `PSSL_METHOD`
**Pragmas:** `raises: [LibraryError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError`, `tags: RootEffect`, `forbids: `

### SSLv23_method

[ref: #symbol-sslv23-method]

**Input:**
- *(none)*

**Output:** `PSSL_METHOD`
**Pragmas:** `raises: [LibraryError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError`, `tags: RootEffect`, `forbids: `

### SSLv2_method

[ref: #symbol-sslv2-method]

**Input:**
- *(none)*

**Output:** `PSSL_METHOD`
**Pragmas:** `raises: [LibraryError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError`, `tags: RootEffect`, `forbids: `

### SSLv3_method

[ref: #symbol-sslv3-method]

**Input:**
- *(none)*

**Output:** `PSSL_METHOD`
**Pragmas:** `raises: [LibraryError]`, `tags: [RootEffect]`, `forbids: []`

**Effects:** `raises: LibraryError`, `tags: RootEffect`, `forbids: `


[Prev](openssl_2.md) | [Next](openssl_4.md)
