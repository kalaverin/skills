---
source_hash: c7314b291543d173
source_path: lib/wrappers/openssl.nim
---

# openssl

[ref: #module-openssl]

OpenSSL wrapper. Supports OpenSSL >= 1.1.0 dynamically (as default) or statically linked using --dynlibOverride:ssl.

-d:sslVersion=1.2.3 can be used to force an SSL version. This version must be included in the library name. -d:useOpenssl3 may be set for OpenSSL 3 instead.

There is also limited support for OpenSSL 1.0.x which may require -d:openssl10.

Build and test examples:

```
./bin/nim c -d:ssl -p:. -r tests/stdlib/tssl.nim
./bin/nim c -d:ssl --threads:on -p:. -r tests/stdlib/thttpclient_ssl.nim
./bin/nim c -d:ssl -p:. -r tests/untestable/tssl.nim
./bin/nim c -d:ssl -p:. --dynlibOverride:ssl --passl:-lcrypto --passl:-lssl -r tests/untestable/tssl.nim
./bin/nim r --putenv:NIM_TESTAMENT_REMOTE_NETWORKING:1 -d:ssl -p:testament/lib --threads:on tests/untestable/thttpclient_ssl_remotenetwork.nim
```

## Examples

```nim
./bin/nim c -d:ssl -p:. -r tests/stdlib/tssl.nim
./bin/nim c -d:ssl --threads:on -p:. -r tests/stdlib/thttpclient_ssl.nim
./bin/nim c -d:ssl -p:. -r tests/untestable/tssl.nim
./bin/nim c -d:ssl -p:. --dynlibOverride:ssl --passl:-lcrypto --passl:-lssl -r tests/untestable/tssl.nim
./bin/nim r --putenv:NIM_TESTAMENT_REMOTE_NETWORKING:1 -d:ssl -p:testament/lib --threads:on tests/untestable/thttpclient_ssl_remotenetwork.nim
```

## Const

### DLLSSLName

[ref: #symbol-dllsslname]

```nim
DLLSSLName = "(libssl-1_1-x64|ssleay64|libssl64).dll"
```

### DLLUtilName

[ref: #symbol-dllutilname]

```nim
DLLUtilName = "(libcrypto-1_1-x64|libeay64).dll"
```

### EVP_MAX_MD_SIZE

[ref: #symbol-evp-max-md-size]

```nim
EVP_MAX_MD_SIZE = 36
```

### EVP_PKEY_RSA

[ref: #symbol-evp-pkey-rsa]

```nim
EVP_PKEY_RSA = 6
```

### MD5_CBLOCK

[ref: #symbol-md5-cblock]

```nim
MD5_CBLOCK = 64
```

### MD5_DIGEST_LENGTH

[ref: #symbol-md5-digest-length]

```nim
MD5_DIGEST_LENGTH = 16
```

### MD5_LBLOCK

[ref: #symbol-md5-lblock]

```nim
MD5_LBLOCK = 16
```

### OPENSSL_DES_DECRYPT

[ref: #symbol-openssl-des-decrypt]

```nim
OPENSSL_DES_DECRYPT = 0
```

### OPENSSL_DES_ENCRYPT

[ref: #symbol-openssl-des-encrypt]

```nim
OPENSSL_DES_ENCRYPT = 1
```

### SSL_CTRL_CLEAR_NUM_RENEGOTIATIONS

[ref: #symbol-ssl-ctrl-clear-num-renegotiations]

```nim
SSL_CTRL_CLEAR_NUM_RENEGOTIATIONS = 11
```

### SSL_CTRL_EXTRA_CHAIN_CERT

[ref: #symbol-ssl-ctrl-extra-chain-cert]

```nim
SSL_CTRL_EXTRA_CHAIN_CERT = 14
```

### SSL_CTRL_GET_CLIENT_CERT_REQUEST

[ref: #symbol-ssl-ctrl-get-client-cert-request]

```nim
SSL_CTRL_GET_CLIENT_CERT_REQUEST = 9
```

### SSL_CTRL_GET_FLAGS

[ref: #symbol-ssl-ctrl-get-flags]

```nim
SSL_CTRL_GET_FLAGS = 13
```

### SSL_CTRL_GET_MAX_CERT_LIST

[ref: #symbol-ssl-ctrl-get-max-cert-list]

```nim
SSL_CTRL_GET_MAX_CERT_LIST = 50
```

### SSL_CTRL_GET_NUM_RENEGOTIATIONS

[ref: #symbol-ssl-ctrl-get-num-renegotiations]

```nim
SSL_CTRL_GET_NUM_RENEGOTIATIONS = 10
```

### SSL_CTRL_GET_READ_AHEAD

[ref: #symbol-ssl-ctrl-get-read-ahead]

```nim
SSL_CTRL_GET_READ_AHEAD = 40
```

### SSL_CTRL_GET_SESS_CACHE_MODE

[ref: #symbol-ssl-ctrl-get-sess-cache-mode]

```nim
SSL_CTRL_GET_SESS_CACHE_MODE = 45
```

### SSL_CTRL_GET_SESS_CACHE_SIZE

[ref: #symbol-ssl-ctrl-get-sess-cache-size]

```nim
SSL_CTRL_GET_SESS_CACHE_SIZE = 43
```

### SSL_CTRL_GET_SESSION_REUSED

[ref: #symbol-ssl-ctrl-get-session-reused]

```nim
SSL_CTRL_GET_SESSION_REUSED = 8
```

### SSL_CTRL_GET_TOTAL_RENEGOTIATIONS

[ref: #symbol-ssl-ctrl-get-total-renegotiations]

```nim
SSL_CTRL_GET_TOTAL_RENEGOTIATIONS = 12
```

### SSL_CTRL_MODE

[ref: #symbol-ssl-ctrl-mode]

```nim
SSL_CTRL_MODE = 33
```

### SSL_CTRL_NEED_TMP_RSA

[ref: #symbol-ssl-ctrl-need-tmp-rsa]

```nim
SSL_CTRL_NEED_TMP_RSA = 1
```

### SSL_CTRL_OPTIONS

[ref: #symbol-ssl-ctrl-options]

```nim
SSL_CTRL_OPTIONS = 32
```

### SSL_CTRL_SESS_ACCEPT

[ref: #symbol-ssl-ctrl-sess-accept]

```nim
SSL_CTRL_SESS_ACCEPT = 24
```

### SSL_CTRL_SESS_ACCEPT_GOOD

[ref: #symbol-ssl-ctrl-sess-accept-good]

```nim
SSL_CTRL_SESS_ACCEPT_GOOD = 25
```

### SSL_CTRL_SESS_ACCEPT_RENEGOTIATE

[ref: #symbol-ssl-ctrl-sess-accept-renegotiate]

```nim
SSL_CTRL_SESS_ACCEPT_RENEGOTIATE = 26
```

### SSL_CTRL_SESS_CACHE_FULL

[ref: #symbol-ssl-ctrl-sess-cache-full]

```nim
SSL_CTRL_SESS_CACHE_FULL = 31
```

### SSL_CTRL_SESS_CB_HIT

[ref: #symbol-ssl-ctrl-sess-cb-hit]

```nim
SSL_CTRL_SESS_CB_HIT = 28
```

### SSL_CTRL_SESS_CONNECT

[ref: #symbol-ssl-ctrl-sess-connect]

```nim
SSL_CTRL_SESS_CONNECT = 21
```

### SSL_CTRL_SESS_CONNECT_GOOD

[ref: #symbol-ssl-ctrl-sess-connect-good]

```nim
SSL_CTRL_SESS_CONNECT_GOOD = 22
```

### SSL_CTRL_SESS_CONNECT_RENEGOTIATE

[ref: #symbol-ssl-ctrl-sess-connect-renegotiate]

```nim
SSL_CTRL_SESS_CONNECT_RENEGOTIATE = 23
```

### SSL_CTRL_SESS_HIT

[ref: #symbol-ssl-ctrl-sess-hit]

```nim
SSL_CTRL_SESS_HIT = 27
```

### SSL_CTRL_SESS_MISSES

[ref: #symbol-ssl-ctrl-sess-misses]

```nim
SSL_CTRL_SESS_MISSES = 29
```

### SSL_CTRL_SESS_NUMBER

[ref: #symbol-ssl-ctrl-sess-number]

```nim
SSL_CTRL_SESS_NUMBER = 20
```

### SSL_CTRL_SESS_TIMEOUTS

[ref: #symbol-ssl-ctrl-sess-timeouts]

```nim
SSL_CTRL_SESS_TIMEOUTS = 30
```

### SSL_CTRL_SET_ECDH_AUTO

[ref: #symbol-ssl-ctrl-set-ecdh-auto]

```nim
SSL_CTRL_SET_ECDH_AUTO = 94
```

### SSL_CTRL_SET_MAX_CERT_LIST

[ref: #symbol-ssl-ctrl-set-max-cert-list]

```nim
SSL_CTRL_SET_MAX_CERT_LIST = 51
```

### SSL_CTRL_SET_MSG_CALLBACK

[ref: #symbol-ssl-ctrl-set-msg-callback]

```nim
SSL_CTRL_SET_MSG_CALLBACK = 15
```

### SSL_CTRL_SET_MSG_CALLBACK_ARG

[ref: #symbol-ssl-ctrl-set-msg-callback-arg]

```nim
SSL_CTRL_SET_MSG_CALLBACK_ARG = 16
```

### SSL_CTRL_SET_MTU

[ref: #symbol-ssl-ctrl-set-mtu]

```nim
SSL_CTRL_SET_MTU = 17
```

### SSL_CTRL_SET_READ_AHEAD

[ref: #symbol-ssl-ctrl-set-read-ahead]

```nim
SSL_CTRL_SET_READ_AHEAD = 41
```

### SSL_CTRL_SET_SESS_CACHE_MODE

[ref: #symbol-ssl-ctrl-set-sess-cache-mode]

```nim
SSL_CTRL_SET_SESS_CACHE_MODE = 44
```

### SSL_CTRL_SET_SESS_CACHE_SIZE

[ref: #symbol-ssl-ctrl-set-sess-cache-size]

```nim
SSL_CTRL_SET_SESS_CACHE_SIZE = 42
```

### SSL_CTRL_SET_TMP_DH

[ref: #symbol-ssl-ctrl-set-tmp-dh]

```nim
SSL_CTRL_SET_TMP_DH = 3
```

### SSL_CTRL_SET_TMP_DH_CB

[ref: #symbol-ssl-ctrl-set-tmp-dh-cb]

```nim
SSL_CTRL_SET_TMP_DH_CB = 6
```

### SSL_CTRL_SET_TMP_ECDH

[ref: #symbol-ssl-ctrl-set-tmp-ecdh]

```nim
SSL_CTRL_SET_TMP_ECDH = 4
```

### SSL_CTRL_SET_TMP_ECDH_CB

[ref: #symbol-ssl-ctrl-set-tmp-ecdh-cb]

```nim
SSL_CTRL_SET_TMP_ECDH_CB = 7
```

### SSL_CTRL_SET_TMP_RSA

[ref: #symbol-ssl-ctrl-set-tmp-rsa]

```nim
SSL_CTRL_SET_TMP_RSA = 2
```

### SSL_CTRL_SET_TMP_RSA_CB

[ref: #symbol-ssl-ctrl-set-tmp-rsa-cb]

```nim
SSL_CTRL_SET_TMP_RSA_CB = 5
```

### SSL_ERROR_NONE

[ref: #symbol-ssl-error-none]

```nim
SSL_ERROR_NONE = 0
```

### SSL_ERROR_SSL

[ref: #symbol-ssl-error-ssl]

```nim
SSL_ERROR_SSL = 1
```

### SSL_ERROR_SYSCALL

[ref: #symbol-ssl-error-syscall]

```nim
SSL_ERROR_SYSCALL = 5
```

### SSL_ERROR_WANT_ACCEPT

[ref: #symbol-ssl-error-want-accept]

```nim
SSL_ERROR_WANT_ACCEPT = 8
```

### SSL_ERROR_WANT_CONNECT

[ref: #symbol-ssl-error-want-connect]

```nim
SSL_ERROR_WANT_CONNECT = 7
```

### SSL_ERROR_WANT_READ

[ref: #symbol-ssl-error-want-read]

```nim
SSL_ERROR_WANT_READ = 2
```

### SSL_ERROR_WANT_WRITE

[ref: #symbol-ssl-error-want-write]

```nim
SSL_ERROR_WANT_WRITE = 3
```

### SSL_ERROR_WANT_X509_LOOKUP

[ref: #symbol-ssl-error-want-x509-lookup]

```nim
SSL_ERROR_WANT_X509_LOOKUP = 4
```

### SSL_ERROR_ZERO_RETURN

[ref: #symbol-ssl-error-zero-return]

```nim
SSL_ERROR_ZERO_RETURN = 6
```

### SSL_FILETYPE_ASN1

[ref: #symbol-ssl-filetype-asn1]

```nim
SSL_FILETYPE_ASN1 = 2
```

### SSL_FILETYPE_PEM

[ref: #symbol-ssl-filetype-pem]

```nim
SSL_FILETYPE_PEM = 1
```

### SSL_MODE_ACCEPT_MOVING_WRITE_BUFFER

[ref: #symbol-ssl-mode-accept-moving-write-buffer]

```nim
SSL_MODE_ACCEPT_MOVING_WRITE_BUFFER = 2
```

### SSL_MODE_AUTO_RETRY

[ref: #symbol-ssl-mode-auto-retry]

```nim
SSL_MODE_AUTO_RETRY = 4
```

### SSL_MODE_ENABLE_PARTIAL_WRITE

[ref: #symbol-ssl-mode-enable-partial-write]

```nim
SSL_MODE_ENABLE_PARTIAL_WRITE = 1
```

### SSL_MODE_NO_AUTO_CHAIN

[ref: #symbol-ssl-mode-no-auto-chain]

```nim
SSL_MODE_NO_AUTO_CHAIN = 8
```

### SSL_OP_ALL

[ref: #symbol-ssl-op-all]

```nim
SSL_OP_ALL = 0x000FFFFF
```

### SSL_OP_NO_SSLv2

[ref: #symbol-ssl-op-no-sslv2]

```nim
SSL_OP_NO_SSLv2 = 0x01000000
```

### SSL_OP_NO_SSLv3

[ref: #symbol-ssl-op-no-sslv3]

```nim
SSL_OP_NO_SSLv3 = 0x02000000
```

### SSL_OP_NO_TLSv1

[ref: #symbol-ssl-op-no-tlsv1]

```nim
SSL_OP_NO_TLSv1 = 0x04000000
```

### SSL_OP_NO_TLSv1_1

[ref: #symbol-ssl-op-no-tlsv1-1]

```nim
SSL_OP_NO_TLSv1_1 = 0x08000000
```

### SSL_RECEIVED_SHUTDOWN

[ref: #symbol-ssl-received-shutdown]

```nim
SSL_RECEIVED_SHUTDOWN = 2
```

### SSL_SENT_SHUTDOWN

[ref: #symbol-ssl-sent-shutdown]

```nim
SSL_SENT_SHUTDOWN = 1
```

### SSL_ST_ACCEPT

[ref: #symbol-ssl-st-accept]

```nim
SSL_ST_ACCEPT = 0x00002000
```

### SSL_ST_CONNECT

[ref: #symbol-ssl-st-connect]

```nim
SSL_ST_CONNECT = 0x00001000
```

### SSL_ST_INIT

[ref: #symbol-ssl-st-init]

```nim
SSL_ST_INIT = 12288
```

### SSL_TLSEXT_ERR_ALERT_FATAL

[ref: #symbol-ssl-tlsext-err-alert-fatal]

```nim
SSL_TLSEXT_ERR_ALERT_FATAL = 2
```

### SSL_TLSEXT_ERR_ALERT_WARNING

[ref: #symbol-ssl-tlsext-err-alert-warning]

```nim
SSL_TLSEXT_ERR_ALERT_WARNING = 1
```

### SSL_TLSEXT_ERR_NOACK

[ref: #symbol-ssl-tlsext-err-noack]

```nim
SSL_TLSEXT_ERR_NOACK = 3
```

### SSL_TLSEXT_ERR_OK

[ref: #symbol-ssl-tlsext-err-ok]

```nim
SSL_TLSEXT_ERR_OK = 0
```

### SSL_VERIFY_NONE

[ref: #symbol-ssl-verify-none]

```nim
SSL_VERIFY_NONE = 0x00000000
```

### SSL_VERIFY_PEER

[ref: #symbol-ssl-verify-peer]

```nim
SSL_VERIFY_PEER = 0x00000001
```

### TLSEXT_NAMETYPE_host_name

[ref: #symbol-tlsext-nametype-host-name]

```nim
TLSEXT_NAMETYPE_host_name = 0
```

### useOpenssl3

[ref: #symbol-useopenssl3]

```nim
useOpenssl3 {.booldefine.} = false
```

### X509_V_ERR_AKID_ISSUER_SERIAL_MISMATCH

[ref: #symbol-x509-v-err-akid-issuer-serial-mismatch]

```nim
X509_V_ERR_AKID_ISSUER_SERIAL_MISMATCH = 31
```

### X509_V_ERR_AKID_SKID_MISMATCH

[ref: #symbol-x509-v-err-akid-skid-mismatch]

```nim
X509_V_ERR_AKID_SKID_MISMATCH = 30
```

### X509_V_ERR_APPLICATION_VERIFICATION

[ref: #symbol-x509-v-err-application-verification]

```nim
X509_V_ERR_APPLICATION_VERIFICATION = 50
```

### X509_V_ERR_CERT_CHAIN_TOO_LONG

[ref: #symbol-x509-v-err-cert-chain-too-long]

```nim
X509_V_ERR_CERT_CHAIN_TOO_LONG = 22
```

### X509_V_ERR_CERT_HAS_EXPIRED

[ref: #symbol-x509-v-err-cert-has-expired]

```nim
X509_V_ERR_CERT_HAS_EXPIRED = 10
```

### X509_V_ERR_CERT_NOT_YET_VALID

[ref: #symbol-x509-v-err-cert-not-yet-valid]

```nim
X509_V_ERR_CERT_NOT_YET_VALID = 9
```

### X509_V_ERR_CERT_REJECTED

[ref: #symbol-x509-v-err-cert-rejected]

```nim
X509_V_ERR_CERT_REJECTED = 28
```

### X509_V_ERR_CERT_REVOKED

[ref: #symbol-x509-v-err-cert-revoked]

```nim
X509_V_ERR_CERT_REVOKED = 23
```

### X509_V_ERR_CERT_SIGNATURE_FAILURE

[ref: #symbol-x509-v-err-cert-signature-failure]

```nim
X509_V_ERR_CERT_SIGNATURE_FAILURE = 7
```

### X509_V_ERR_CERT_UNTRUSTED

[ref: #symbol-x509-v-err-cert-untrusted]

```nim
X509_V_ERR_CERT_UNTRUSTED = 27
```

### X509_V_ERR_CRL_HAS_EXPIRED

[ref: #symbol-x509-v-err-crl-has-expired]

```nim
X509_V_ERR_CRL_HAS_EXPIRED = 12
```

### X509_V_ERR_CRL_NOT_YET_VALID

[ref: #symbol-x509-v-err-crl-not-yet-valid]

```nim
X509_V_ERR_CRL_NOT_YET_VALID = 11
```

### X509_V_ERR_CRL_SIGNATURE_FAILURE

[ref: #symbol-x509-v-err-crl-signature-failure]

```nim
X509_V_ERR_CRL_SIGNATURE_FAILURE = 8
```

### X509_V_ERR_DEPTH_ZERO_SELF_SIGNED_CERT

[ref: #symbol-x509-v-err-depth-zero-self-signed-cert]

```nim
X509_V_ERR_DEPTH_ZERO_SELF_SIGNED_CERT = 18
```

### X509_V_ERR_ERROR_IN_CERT_NOT_AFTER_FIELD

[ref: #symbol-x509-v-err-error-in-cert-not-after-field]

```nim
X509_V_ERR_ERROR_IN_CERT_NOT_AFTER_FIELD = 14
```

### X509_V_ERR_ERROR_IN_CERT_NOT_BEFORE_FIELD

[ref: #symbol-x509-v-err-error-in-cert-not-before-field]

```nim
X509_V_ERR_ERROR_IN_CERT_NOT_BEFORE_FIELD = 13
```

### X509_V_ERR_ERROR_IN_CRL_LAST_UPDATE_FIELD

[ref: #symbol-x509-v-err-error-in-crl-last-update-field]

```nim
X509_V_ERR_ERROR_IN_CRL_LAST_UPDATE_FIELD = 15
```

### X509_V_ERR_ERROR_IN_CRL_NEXT_UPDATE_FIELD

[ref: #symbol-x509-v-err-error-in-crl-next-update-field]

```nim
X509_V_ERR_ERROR_IN_CRL_NEXT_UPDATE_FIELD = 16
```

### X509_V_ERR_INVALID_CA

[ref: #symbol-x509-v-err-invalid-ca]

```nim
X509_V_ERR_INVALID_CA = 24
```

### X509_V_ERR_INVALID_PURPOSE

[ref: #symbol-x509-v-err-invalid-purpose]

```nim
X509_V_ERR_INVALID_PURPOSE = 26
```

### X509_V_ERR_KEYUSAGE_NO_CERTSIGN

[ref: #symbol-x509-v-err-keyusage-no-certsign]

```nim
X509_V_ERR_KEYUSAGE_NO_CERTSIGN = 32
```

### X509_V_ERR_OUT_OF_MEM

[ref: #symbol-x509-v-err-out-of-mem]

```nim
X509_V_ERR_OUT_OF_MEM = 17
```

### X509_V_ERR_PATH_LENGTH_EXCEEDED

[ref: #symbol-x509-v-err-path-length-exceeded]

```nim
X509_V_ERR_PATH_LENGTH_EXCEEDED = 25
```

### X509_V_ERR_SELF_SIGNED_CERT_IN_CHAIN

[ref: #symbol-x509-v-err-self-signed-cert-in-chain]

```nim
X509_V_ERR_SELF_SIGNED_CERT_IN_CHAIN = 19
```

### X509_V_ERR_SUBJECT_ISSUER_MISMATCH

[ref: #symbol-x509-v-err-subject-issuer-mismatch]

```nim
X509_V_ERR_SUBJECT_ISSUER_MISMATCH = 29
```

### X509_V_ERR_UNABLE_TO_DECODE_ISSUER_PUBLIC_KEY

[ref: #symbol-x509-v-err-unable-to-decode-issuer-public-key]

```nim
X509_V_ERR_UNABLE_TO_DECODE_ISSUER_PUBLIC_KEY = 6
```

### X509_V_ERR_UNABLE_TO_DECRYPT_CERT_SIGNATURE

[ref: #symbol-x509-v-err-unable-to-decrypt-cert-signature]

```nim
X509_V_ERR_UNABLE_TO_DECRYPT_CERT_SIGNATURE = 4
```

### X509_V_ERR_UNABLE_TO_DECRYPT_CRL_SIGNATURE

[ref: #symbol-x509-v-err-unable-to-decrypt-crl-signature]

```nim
X509_V_ERR_UNABLE_TO_DECRYPT_CRL_SIGNATURE = 5
```

### X509_V_ERR_UNABLE_TO_GET_CRL

[ref: #symbol-x509-v-err-unable-to-get-crl]

```nim
X509_V_ERR_UNABLE_TO_GET_CRL = 3
```

### X509_V_ERR_UNABLE_TO_GET_CRL_ISSUER

[ref: #symbol-x509-v-err-unable-to-get-crl-issuer]

```nim
X509_V_ERR_UNABLE_TO_GET_CRL_ISSUER = 33
```

### X509_V_ERR_UNABLE_TO_GET_ISSUER_CERT

[ref: #symbol-x509-v-err-unable-to-get-issuer-cert]

```nim
X509_V_ERR_UNABLE_TO_GET_ISSUER_CERT = 2
```

### X509_V_ERR_UNABLE_TO_GET_ISSUER_CERT_LOCALLY

[ref: #symbol-x509-v-err-unable-to-get-issuer-cert-locally]

```nim
X509_V_ERR_UNABLE_TO_GET_ISSUER_CERT_LOCALLY = 20
```

### X509_V_ERR_UNABLE_TO_VERIFY_LEAF_SIGNATURE

[ref: #symbol-x509-v-err-unable-to-verify-leaf-signature]

```nim
X509_V_ERR_UNABLE_TO_VERIFY_LEAF_SIGNATURE = 21
```

### X509_V_ERR_UNHANDLED_CRITICAL_EXTENSION

[ref: #symbol-x509-v-err-unhandled-critical-extension]

```nim
X509_V_ERR_UNHANDLED_CRITICAL_EXTENSION = 34
```

### X509_V_ILLEGAL

[ref: #symbol-x509-v-illegal]

```nim
X509_V_ILLEGAL = 1
```

### X509_V_OK

[ref: #symbol-x509-v-ok]

```nim
X509_V_OK = 0
```

## Proc

### BIO_ctrl

[ref: #symbol-bio-ctrl]

**Input:**
- `bio: BIO`
- `cmd: cint`
- `larg: int`
- `arg: cstring`

**Output:** `int`
**Pragmas:** `cdecl`, `dynlib: DLLUtilName`, `importc`, `raises: []`, `tags: []`, `forbids: []`

**Effects:** `raises: `, `tags: `, `forbids: `


[Next](openssl_2.md)
