---
source_hash: 916f12f6129345ae
source_path: lib/pure/ssl_config.nim
---

# ssl_config

[ref: #module-ssl_config]

This module contains SSL configuration parameters obtained from [Mozilla OpSec](https://wiki.mozilla.org/Security/Server_Side_TLS).

The configuration file used to generate this module: <https://ssl-config.mozilla.org/guidelines/5.4.json>

## Const

### CiphersIntermediate

[ref: #symbol-ciphersintermediate]

An OpenSSL-compatible list of secure ciphers for intermediate compatibility per Mozilla's recommendations.

```nim
CiphersIntermediate = "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384"
```

An OpenSSL-compatible list of secure ciphers for intermediate compatibility per Mozilla's recommendations.

Oldest clients supported by this list:

* Firefox 27
* Android 4.4.2
* Chrome 31
* Edge
* IE 11 on Windows 7
* Java 8u31
* OpenSSL 1.0.1
* Opera 20
* Safari 9

### CiphersModern

[ref: #symbol-ciphersmodern]

An OpenSSL-compatible list of secure ciphers for modern compatibility per Mozilla's recommendations.

```nim
CiphersModern = "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256"
```

An OpenSSL-compatible list of secure ciphers for modern compatibility per Mozilla's recommendations.

Oldest clients supported by this list:

* Firefox 63
* Android 10.0
* Chrome 70
* Edge 75
* Java 11
* OpenSSL 1.1.1
* Opera 57
* Safari 12.1

### CiphersOld

[ref: #symbol-ciphersold]

An OpenSSL-compatible list of secure ciphers for old compatibility per Mozilla's recommendations.

```nim
CiphersOld = "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA256:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA"
```

An OpenSSL-compatible list of secure ciphers for old compatibility per Mozilla's recommendations.

Oldest clients supported by this list:

* Firefox 1
* Android 2.3
* Chrome 1
* Edge 12
* IE8 on Windows XP
* Java 6
* OpenSSL 0.9.8
* Opera 5
* Safari 1
