---
source_hash: 8ce798ae5d636414
source_path: lib/pure/ssl_certs.nim
---

# ssl_certs

[ref: #module-ssl_certs]

Scan for SSL/TLS CA certificates on disk The default locations can be overridden using the SSL\_CERT\_FILE and SSL\_CERT\_DIR environment variables.

## Iterator

### scanSSLCertificates

[ref: #symbol-scansslcertificates]

Scan for SSL/TLS CA certificates on disk.

**Input:**
- `useEnvVars:  = false`

**Output:** `string`
**Pragmas:** `raises: []`, `tags: [ReadEnvEffect, ReadDirEffect]`, `forbids: []`

**Effects:** `raises: `, `tags: ReadEnvEffect, ReadDirEffect`, `forbids: `

Scan for SSL/TLS CA certificates on disk.

if useEnvVars is true, the SSL\_CERT\_FILE and SSL\_CERT\_DIR environment variables can be used to override the certificate directories to scan or specify a CA certificate file.
