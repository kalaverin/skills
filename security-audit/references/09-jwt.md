---
subject: "JWT vulnerability detection reference for SAST subagents: OWASP API2 context, insecure-implementation definition, CWE table, 15 weakness classes and exclusions, prevention patterns, per-stack vulnerable/secure recipes incl. FastAPI and modern jjwt/golang-jwt, kid/JWK/JKU injection, URL/storage/refresh/binding/JWE secondary patterns, three-phase execution."
index:
  - anchor: jwt-detection
    what: "Focused JWT weakness detection role using the three-phase subagent approach — lifecycle recon, batched verify, merge — gated on the architecture report."
    problem: "Codebase needs systematic sweep of every token verification, issuance, and storage site, yet unstructured hunting misses weak validators and drowns reviewers in unverified candidates; detection orchestration, phase pipeline, verified findings, audit rigor, methodical triage, candidate flood, coverage goal."
    use_when: "JWT scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-phase detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual JWT knowledge is needed, not execution."
    expected: "Verified JWT findings consolidated into the module report with false positives filtered."
  - anchor: jwt-owasp-context
    what: "OWASP API2:2023 ratings and JWT-related broken-authentication signals, plus adjacent failures: stuffing, missing re-authentication, microservice gaps, leakage."
    problem: "Audits treat token flaws as library trivia without business framing, so severity rationale stays weak and unconvincing in reports; risk framing, account takeover, business stakes, taxonomy anchor, authentication failures, impact narrative, reviewer context."
    use_when: "Writing severity rationale; explaining why token weaknesses matter beyond crypto details."
    avoid_when: "Detection mechanics are the question — see execution anchors; CWE identifiers wanted."
    expected: "Reports frame token findings as authentication-breakage with takeover impact."
  - anchor: jwt-definition
    what: "Core definition: header.payload.signature structure and the failure modes — trusting token-declared algorithms, skipped signature verification, guessable secrets, attacker-controlled key material."
    problem: "Reviewers disagree on what counts as token insecurity without shared failure modes, so decode-only paths get missed while compliant verifiers attract noise; concept baseline, shared vocabulary, classification consistency, definition anchor, signature validation, claims checks, term alignment."
    use_when: "Onboarding to the scan; deciding whether a code path belongs to JWT findings at all."
    avoid_when: "Concrete stack recipes are needed — jump to the examples anchor; execution workflow is the question."
    expected: "Everyone applies one definition: tokens trusted without proper authenticity verification."
  - anchor: jwt-cwe-mapping
    what: "CWE table per weakness class: CWE-347/345 for signature issues, CWE-798/330 for weak secrets, CWE-89/22/94/502 for kid injection, CWE-613/200/522/327/306/384 for lifecycle flaws."
    problem: "Wrong CWE assignment breaks downstream tooling and metrics, especially when key management and injection classes blur categories; weakness taxonomy, cwe 347, misclassification risk, tooling accuracy, identifier precision, reporting feeds, scanner alignment."
    use_when: "Assigning CWE identifiers to findings."
    avoid_when: "OWASP risk framing is the question — see the context anchor."
    expected: "Each finding carries the most specific CWE identifier."
  - anchor: jwt-scope-in
    what: "Fifteen weakness classes: alg:none, RS256-to-HS256 confusion, decode-only paths, weak secrets, embedded JWK, JKU/X5U, kid injection, missing claims, no revocation, URL leakage, insecure storage, refresh failures, no binding, JWKS trust, JWE weaknesses."
    problem: "Detectors under-report when weakness classes stay implicit, missing header-injection, lifecycle, and storage paths across frameworks and libraries; inclusion rules, class inventory, missed callsites, hidden vectors, recon breadth, primitive coverage, framework gaps."
    use_when: "Building or checking a recon checklist; unsure whether a construct qualifies; calibrating false negatives."
    avoid_when: "Exclusions and class boundaries are the question — see the scope-out anchor; prevention patterns wanted."
    expected: "Every token-handling weakness class is recognized during recon."
  - anchor: jwt-scope-out
    what: "Boundary rules excluding IDOR via claim tampering, XSS through rendered claims, and CSRF on cookie-carried tokens."
    problem: "Findings get misrouted when adjacent classes blur into token forgery, corrupting severity and ownership across scans; misrouting risk, class confusion, double reporting, ownership clarity, dedup discipline, triage errors, category overlap, fuzzy edges."
    use_when: "A finding could belong to another scan class; triaging overlapping categories."
    avoid_when: "Positive weaknesses are needed — see the scope-in anchor; prevention patterns wanted."
    expected: "Each candidate lands in exactly one class, with forgery separated from usage flaws."
  - anchor: jwt-prevention-patterns
    what: "Safe verification constructions: pinned algorithms per library, strong env-sourced secrets, JWKS allowlists, and claim validation."
    problem: "Verify subagents need authoritative safe patterns to avoid flagging secured verifiers, and scattered hardening knowledge produces false positives everywhere; locked algos, env secrets, jwks pinning, false-positive control, secure baseline, mitigation catalog, guard patterns."
    use_when: "Classifying a candidate as mitigated; comparing site code against known-safe forms; writing remediation notes."
    avoid_when: "Vulnerable examples per stack are the need — see the examples anchor."
    expected: "Algorithm-pinned, claim-validating verification correctly classified as not vulnerable."
  - anchor: jwt-examples
    what: "Per-stack vulnerable/secure recipe pairs: PyJWT, FastAPI, python-jose, jsonwebtoken, jose, jjwt (legacy and 0.12 APIs), golang-jwt, .NET, plus kid, embedded-JWK, URL, storage, refresh, and JWE patterns."
    problem: "Verification idioms differ per library and version, and generic token rules miss stack-specific traps like decode-vs-verify, parserBuilder removal, and archived Go modules; stack recipes, release drift, api drift, precise detection, pattern matching, call diversity, framework calls."
    use_when: "Target uses one of the covered stacks; reviewing token verification call sites."
    avoid_when: "Weakness-class catalog is the question — see the scope-in anchor; conceptual definitions wanted."
    expected: "Stack-specific dangerous calls flagged; hardened verification verified."
  - anchor: jwt-execution
    what: "Three-phase execution: JWT lifecycle mapping recon with a zero-usage early-exit gate, batched verify per verification site, merge into the final module report."
    problem: "Detection work without orchestration duplicates effort, loses batch boundaries, and merges findings inconsistently; execution model, phase overview, subagent orchestration, context passing, batch discipline, workflow entry, staging, dispatch plan, consolidation, handoff clarity."
    use_when: "Starting the JWT scan execution; dispatching or reviewing any phase."
    avoid_when: "Conceptual JWT knowledge is the need — see definition and examples anchors."
    expected: "All three phases run with shared architecture context into one consolidated report."
  - anchor: jwt-references
    what: "External link list for JWT concepts, library docs, and attack tooling."
    problem: "Agents and readers need authoritative follow-up sources beyond this file's distilled content when deeper verification is required; further reading, external canon, deep dives, vendor documentation, community knowledge, primary material, cited works, rfc pages."
    use_when: "Primary sources or extended material is needed."
    avoid_when: "Detection recipes or execution workflow are the question — the references list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
  - anchor: jwt-important-reminders
    what: "Closing operational reminders for the JWT module: phase ordering, batch discipline, library-version traps, and cleanup rules."
    problem: "Modules close with inconsistent final guidance, letting inflated ratings or weak proof slip into reports and client deliverables; closing rules, quality floor, consistency, final reminders, weak evidence, uniform endings, wrap discipline, audit closure."
    use_when: "Finalizing the module report; reviewing closing guidance."
    avoid_when: "Detection or execution is the current stage — finish those first."
    expected: "Reports close with uniform final rules applied."
---

# JWT Vulnerability Detection

[ref: #jwt-detection]

You are performing a focused security assessment to find insecure JSON Web Token (JWT) implementations, mapped to **API2:2023 Broken Authentication** in the OWASP API Security Top 10 2023. This skill uses a three-phase approach with subagents: **recon** (map the full JWT lifecycle — issuance, verification, and configuration), **batched verify** (one focused analysis subagent per verification site), and **merge** (consolidate all findings into the final report).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

> **Subagent constraint**: Subagents must NOT modify project source code. They may only read code and write report files under `{{ REPORTS_ROOT }}/`.

***

## Why This Matters (OWASP API2:2023 Context)
[ref: #jwt-owasp-context]

API2:2023 Broken Authentication is rated:

| Dimension | Rating |
|-----------|--------|
| Exploitability | **Easy** |
| Prevalence | **Common** |
| Detectability | **Easy** |
| Technical Impact | **Severe** |

Authentication endpoints are exposed to everyone, making them high-value targets. OWASP explicitly lists the following JWT-related conditions as signs of broken authentication:

- Accepts unsigned/weakly signed JWTs (`{"alg":"none"}`)
- Doesn't validate the JWT expiration date
- Doesn't validate token authenticity
- Uses weak encryption keys

JWT weaknesses also intersect with broader authentication failures:

- **Credential stuffing / brute force**: Weak rate limiting or account lockout on login/password-recovery endpoints lets attackers brute force tokens or passwords.
- **Missing re-authentication**: Sensitive operations (email change, password change, 2FA update, API key regeneration) performed without re-verifying the user's identity.
- **Microservice authentication gaps**: Services accepting tokens from each other without authentication, or using weak/predictable tokens.
- **Token leakage**: Sending tokens in URLs or storing them insecurely exposes them to logs and XSS.

The core pattern remains: *the server does not fully verify the JWT's authenticity and integrity before trusting its claims.*

***

## What is an Insecure JWT Implementation
[ref: #jwt-definition]

JWTs consist of three Base64URL-encoded parts: `header.payload.signature`. The header declares the signing algorithm (`alg`), the payload carries claims (e.g., `sub`, `role`, `exp`), and the signature is a cryptographic proof of integrity. Vulnerabilities arise when the server trusts the token's own claims about how it was signed, fails to verify the signature at all, uses a guessable secret, or trusts attacker-controlled key material embedded in the token itself.

The core pattern: *the server does not fully verify the JWT's authenticity and integrity before trusting its claims.*

***

## CWE Mapping
[ref: #jwt-cwe-mapping]

Map each weakness class to the relevant CWE. Use this table to label findings consistently in the final report.

| Weakness class | Primary CWE(s) | CWE description |
|----------------|----------------|-----------------|
| `alg: none` accepted / missing signature verification | CWE-347, CWE-345 | Improper Verification of Cryptographic Signature; Insufficient Verification of Data Authenticity |
| RS256 → HS256 algorithm confusion | CWE-347, CWE-345 | Improper Verification of Cryptographic Signature; Insufficient Verification of Data Authenticity |
| Weak or hardcoded HMAC secret | CWE-798, CWE-330 | Use of Hard-coded Credentials; Use of Insufficiently Random Values |
| Embedded JWK / JKU / X5U header injection | CWE-347, CWE-345 | Improper Verification of Cryptographic Signature; Insufficient Verification of Data Authenticity |
| `kid` header SQL injection | CWE-89 | SQL Injection |
| `kid` header path traversal / file inclusion | CWE-22, CWE-98 | Improper Limitation of a Pathname to a Restricted Directory; Improper Control of Filename for Include/Require Statement |
| `kid` header code injection / unsafe deserialization | CWE-94, CWE-502 | Improper Control of Generation of Code; Deserialization of Untrusted Data |
| Missing `exp` / token revocation | CWE-613 | Insufficient Session Expiration |
| Missing `iss` / `aud` / `sub` validation | CWE-345 | Insufficient Verification of Data Authenticity |
| Token leakage in URL / insecure storage | CWE-200, CWE-522 | Information Exposure; Insufficiently Protected Credentials |
| Refresh token reuse without rotation / detection | CWE-613, CWE-798 | Insufficient Session Expiration; Use of Hard-coded Credentials (if hardcoded) |
| JWE weak encryption / `dir` direct encryption | CWE-327, CWE-347 | Use of a Broken or Risky Cryptographic Algorithm; Improper Verification of Cryptographic Signature |
| Missing authentication between microservices | CWE-306 | Missing Authentication for Critical Function |
| Token not bound to channel / device | CWE-384 | Session Fixation / insecure session binding |

## What JWT Vulnerabilities ARE
[ref: #jwt-scope-in]

**1. Algorithm confusion — `alg: none`**
The server accepts a JWT whose header declares `"alg": "none"`, bypassing signature verification entirely. An attacker crafts an arbitrary payload, sets `alg` to `none`, and omits the signature. If the library processes it, the forged token is accepted.

**2. Algorithm confusion — RS256 → HS256**
A server configured for RS256 (asymmetric: sign with private key, verify with public key) can be tricked into HS256 mode if the library allows the algorithm to be specified by the token. Since the public key is often retrievable, the attacker signs a forged token with HS256 using the server's public key as the HMAC secret. The server verifies the HMAC using the same public key and accepts the token.

**3. Missing or disabled signature verification**
The server decodes the JWT payload without actually verifying the signature. Common patterns:
- Python (PyJWT): `jwt.decode(token, options={"verify_signature": False})`
- Node.js (jsonwebtoken): `jwt.decode(token)` instead of `jwt.verify(token, secret)`
- Manual base64 decode of the payload with no signature check
- `algorithms=["none"]` accepted in the decode call

**4. Weak or hardcoded HMAC secret**
The server signs tokens with a short, guessable, or hardcoded secret (e.g., `"secret"`, `"password"`, `"changeme"`, `"jwt-secret-key"`). An attacker who captures a valid token can brute-force the secret offline with tools like `hashcat` or `jwt_tool`, then forge arbitrary tokens.

**5. Embedded JWK (`jwk` header injection)**
The token header contains an embedded JSON Web Key (`jwk` parameter). If the verification code trusts the embedded key to verify the token's own signature, an attacker generates their own key pair, signs a forged token with their private key, and embeds their public key in the header. The server verifies the signature using the attacker's embedded public key and accepts the token.

**6. JKU / X5U header injection**
The `jku` (JWK Set URL) or `x5u` (X.509 certificate URL) header value is used to fetch the verification key from a URL. If the server does not validate the URL against an allowlist, the attacker can point it to their own server hosting a crafted key set.

**7. Key ID (`kid`) header injection**
The `kid` header is used to look up the signing key, often from a database or the filesystem. If the `kid` value is interpolated into a SQL query without sanitization, it becomes an SQL injection vector. If it is concatenated into a file path, it becomes a path traversal vector. If it is passed to an unsafe evaluator or deserializer, it can become code execution.

**8. Missing claim validation**
- `exp` not checked → expired tokens remain valid forever
- `iss` (issuer) not checked → tokens issued by other services are accepted
- `sub` (subject) not checked → tokens bound to another identity are accepted
- `aud` (audience) not checked → tokens intended for other services are accepted
- `nbf` (not-before) not checked → tokens used before their valid window

**9. No token revocation**
There is no token blacklist or revocation mechanism. Stolen or logged-out tokens remain valid until they expire. This matters most when token lifetimes are long.

**10. Token leakage in URL query parameters**
Tokens are read from query strings (`?token=...`). URLs are logged by browsers, proxies, servers, and may be leaked through the `Referer` header.

**11. Insecure token storage**
Access tokens stored in `localStorage` or `sessionStorage` are accessible to any XSS payload. Refresh tokens stored without `httpOnly`, `Secure`, or `SameSite` cookie flags are vulnerable to XSS and CSRF.

**12. Refresh token rotation / reuse detection failures**
Refresh tokens are long-lived and reused indefinitely, or the same refresh token is accepted multiple times without invalidation. An attacker who steals a refresh token can maintain access even after the access token expires.

**13. Missing token binding**
The token is not bound to the TLS channel, client certificate, device fingerprint, or IP address. A stolen token can be replayed from any location or device.

**14. JWKS endpoint trust confusion / poor key rotation**
The application fetches signing keys from a JWKS URL but does not pin or allowlist the URL, does not validate the TLS certificate, or does not handle key rotation safely. An attacker who can influence the JWKS endpoint or perform a man-in-the-middle attack can supply malicious keys.

**15. JWE weaknesses**
JSON Web Encryption is used with weak algorithms or `dir` (direct) encryption using a symmetric key that is short, hardcoded, or shared. An attacker who obtains the encryption key can decrypt all tokens.

### What JWT Vulnerabilities are NOT
[ref: #jwt-scope-out]

Do not flag these as JWT vulnerabilities:

- **IDOR**: Changing a `user_id` claim to access another user's data is an authorization flaw, not a JWT forgery — only flag if the token itself can be forged
- **XSS via JWT payload**: Injecting `<script>` into a claim that is later rendered unescaped — that's XSS, not a JWT bug
- **CSRF**: JWT in cookies without `SameSite` — that's a CSRF concern, not a JWT integrity issue
- **Properly restricted verification**: `jwt.verify(token, secret, { algorithms: ['HS256'] })` with a strong secret — not vulnerable

***

## Patterns That Prevent JWT Vulnerabilities
[ref: #jwt-prevention-patterns]

**1. Algorithm allowlist in verification call**
```python
# Python — PyJWT: explicitly specify allowed algorithms
payload = jwt.decode(token, secret, algorithms=["HS256"])

# Node.js — jsonwebtoken: restrict algorithms
jwt.verify(token, secret, { algorithms: ['HS256'] })

# Java — jjwt: specify expected algorithm
Jwts.parserBuilder().setSigningKey(key).build().parseClaimsJws(token)
# (jjwt does not use the header's alg; it uses the key type)
```

**2. Strong, randomly generated secret**
```python
# Strong secret: at least 256 bits of entropy, not hardcoded
import secrets
SECRET_KEY = secrets.token_hex(32)  # load from env in production
```

**3. Full claim validation**
```python
payload = jwt.decode(
    token, secret, algorithms=["HS256"],
    options={"require": ["exp", "iss", "aud"]},
    issuer="https://myapp.example.com",
    audience="myapp-api"
)
```

**4. Asymmetric keys with no algorithm ambiguity**
```javascript
// Use RS256 with public key for verification; never accept HS256 on the same endpoint
jwt.verify(token, publicKey, { algorithms: ['RS256'] })
```

**5. JWK/JKU URL allowlist**
```python
# Only fetch keys from a known, trusted JWKS endpoint
ALLOWED_JWKS_URLS = {"https://accounts.google.com/.well-known/jwks.json"}
if jku not in ALLOWED_JWKS_URLS:
    raise ValueError("Untrusted JWK URL")
```

**6. Key rotation and secure key storage**
- Store signing keys in a KMS, HSM, or dedicated secret manager (HashiCorp Vault, AWS KMS, Azure Key Vault, GCP KMS).
- Rotate keys regularly and support multiple active keys during transition windows.
- Never commit keys to source control or hardcode them in configuration files.

**7. Token lifecycle hardening**
- Use short-lived access tokens (minutes, not hours) and secure refresh-token rotation with reuse detection.
- Require re-authentication for sensitive operations (email change, password change, 2FA update, API key regeneration).
- Implement rate limiting, account lockout, and CAPTCHA on login, register, and password-recovery endpoints.

**8. Secure token transport and storage**
- Send tokens in `Authorization: Bearer` headers, never in URL query parameters.
- Store refresh tokens in `httpOnly`, `Secure`, `SameSite=Strict` cookies.
- Avoid storing access tokens in `localStorage` or `sessionStorage`.

**9. Token binding where appropriate**
- Bind tokens to a TLS session, client certificate, or device fingerprint for high-security contexts.
- Validate that the token is used from the same channel or device it was issued to.

***

## Vulnerable vs. Secure Examples
[ref: #jwt-examples]

### Python — PyJWT

```python
# VULNERABLE: signature verification disabled
def get_current_user(token: str):
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload["user_id"]

# VULNERABLE: accepts alg:none because no algorithm restriction
def get_current_user(token: str):
    payload = jwt.decode(token, SECRET_KEY)  # PyJWT < 2.x default: accepts any alg
    return payload["user_id"]

# VULNERABLE: weak hardcoded secret
SECRET_KEY = "secret"
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

# SECURE: algorithm restricted, strong secret from env
SECRET_KEY = os.environ["JWT_SECRET"]  # strong, random, from environment
def get_current_user(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload["user_id"]
```

### Python — python-jose / jose

```python
from jose import jwt

# VULNERABLE: weak hardcoded secret and no algorithm restriction
SECRET = "secret"
token = jwt.encode({"user_id": 1}, SECRET, algorithm="HS256")
payload = jwt.decode(token, SECRET)

# VULNERABLE: decode-only path
payload = jwt.get_unverified_claims(token)

# SECURE: algorithm restricted, strong secret from env, claims validated
import os
from jose import jwt, ExpiredSignatureError

SECRET = os.environ["JWT_SECRET"]
payload = jwt.decode(
    token,
    SECRET,
    algorithms=["HS256"],
    options={"require": ["exp"]}
)
```

### Python — FastAPI

```python
# VULNERABLE: signature verification disabled or alg:none accepted
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer
import jwt

app = FastAPI()
bearer = HTTPBearer()

@app.get("/me")
def me(creds=Depends(bearer)):
    payload = jwt.decode(creds.credentials, options={"verify_signature": False})
    return payload

@app.get("/me2")
def me2(creds=Depends(bearer)):
    payload = jwt.decode(creds.credentials, SECRET, algorithms=["HS256", "none"])  # alg:none accepted
    return payload

# SECURE: algorithm pinned, strong secret from env, claims validated
import os
from fastapi import HTTPException
from jwt import PyJWTError

SECRET = os.environ["JWT_SECRET"]

@app.get("/me")
def me(creds=Depends(bearer)):
    try:
        payload = jwt.decode(
            creds.credentials, SECRET,
            algorithms=["HS256"],
            audience="myapp-api",
            issuer="https://myapp.example.com",
        )  # exp verified by default
    except PyJWTError:
        raise HTTPException(status_code=401)
    return payload
```

### Node.js — jsonwebtoken

```javascript
// VULNERABLE: jwt.decode() — no signature verification
function getUser(token) {
  const payload = jwt.decode(token);  // decode only, never verify
  return payload.userId;
}

// VULNERABLE: algorithms not restricted — susceptible to alg:none or RS256→HS256
function getUser(token) {
  const payload = jwt.verify(token, SECRET);  // no algorithms option
  return payload.userId;
}

// VULNERABLE: weak hardcoded secret
const SECRET = "password123";
jwt.verify(token, SECRET, { algorithms: ['HS256'] });

// SECURE: algorithm restricted, strong secret from env
const SECRET = process.env.JWT_SECRET;
function getUser(token) {
  const payload = jwt.verify(token, SECRET, { algorithms: ['HS256'] });
  return payload.userId;
}
```

### Node.js — jose

```javascript
const { jwtVerify, decodeJwt, importSPKI } = require('jose');

// VULNERABLE: decode-only path
function getUser(token) {
  const payload = decodeJwt(token);  // no signature verification
  return payload.sub;
}

// VULNERABLE: no algorithm restriction (older code or misconfiguration)
async function getUser(token, publicKey) {
  const { payload } = await jwtVerify(token, publicKey);  // missing algorithms
  return payload.sub;
}

// SECURE: verify with algorithm allowlist and issuer/audience checks
async function getUser(token, publicKey) {
  const { payload } = await jwtVerify(token, publicKey, {
    algorithms: ['RS256'],
    issuer: 'https://myapp.example.com',
    audience: 'myapp-api'
  });
  return payload.sub;
}
```

### Java — jjwt

```java
// VULNERABLE: deprecated parser (accepts alg from header)
Jwts.parser().setSigningKey(key).parseClaimsJws(token);

// VULNERABLE: no expiry check — the library default may not enforce exp
Claims claims = Jwts.parserBuilder()
    .setSigningKey(key).build()
    .parseClaimsJws(token).getBody();
// claims.getExpiration() never checked

// SECURE (jjwt ≤ 0.11.x, legacy API): parserBuilder (does not trust header alg; uses key type)
Claims claims = Jwts.parserBuilder()
    .requireIssuer("myapp")
    .requireAudience("myapp-api")
    .setSigningKey(key)
    .build()
    .parseClaimsJws(token)
    .getBody();

// SECURE (jjwt ≥ 0.12): verifyWith + parseSignedClaims — parserBuilder removed, setSigningKey deprecated
Claims claims = Jwts.parser()
    .requireIssuer("myapp")
    .requireAudience("myapp-api")
    .verifyWith(key)
    .build()
    .parseSignedClaims(token)
    .getPayload();
```

### Go — golang-jwt

```go
// VULNERABLE: accepts any algorithm including "none"
token, _ := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
    return []byte(secret), nil  // no algorithm check
})

// VULNERABLE: weak secret
var jwtKey = []byte("secret")

// SECURE: validate signing method before returning key
token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
    if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
        return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
    }
    return jwtKey, nil
})
```

Note: `github.com/dgrijalva/jwt-go` is archived and unmaintained (CVE-2020-26160 — `aud` claim verification bypass); the maintained fork is `github.com/golang-jwt/jwt` (v5+). Flag any `go.mod` still importing dgrijalva.

### C# — System.IdentityModel.Tokens.Jwt

```csharp
// VULNERABLE: read token without signature validation
var handler = new JwtSecurityTokenHandler();
var token = handler.ReadJwtToken(tokenString);
var identity = new ClaimsIdentity(token.Claims);

// VULNERABLE: no algorithm restriction
var validationParameters = new TokenValidationParameters
{
    ValidateIssuerSigningKey = true,
    IssuerSigningKey = new SymmetricSecurityKey(key)
};
handler.ValidateToken(tokenString, validationParameters, out _);

// SECURE: algorithm restricted, full claim validation
var validationParameters = new TokenValidationParameters
{
    ValidateIssuerSigningKey = true,
    IssuerSigningKey = new SymmetricSecurityKey(key),
    ValidAlgorithms = new[] { "HS256" },
    ValidateIssuer = true,
    ValidIssuer = "https://myapp.example.com",
    ValidateAudience = true,
    ValidAudience = "myapp-api",
    ValidateLifetime = true,
    RequireExpirationTime = true
};
handler.ValidateToken(tokenString, validationParameters, out _);
```

### kid header SQL injection

```python
# VULNERABLE: kid used in SQL query without sanitization
def get_signing_key(kid):
    result = db.execute(f"SELECT key FROM jwt_keys WHERE id = '{kid}'")
    return result.fetchone()[0]

token_header = jwt.get_unverified_header(token)
key = get_signing_key(token_header["kid"])  # attacker controls kid
jwt.decode(token, key, algorithms=["HS256"])

# SECURE: kid validated against allowlist or parameterized lookup
def get_signing_key(kid):
    result = db.execute("SELECT key FROM jwt_keys WHERE id = %s", (kid,))
    row = result.fetchone()
    if not row:
        raise ValueError("Unknown key id")
    return row[0]
```

### Embedded JWK injection

```javascript
// VULNERABLE: trusts the jwk embedded in the token header
const { publicKey } = getPublicKeyFromHeader(decoded.header);  // attacker-supplied
jwt.verify(token, publicKey);

// SECURE: only use keys from a pre-configured, trusted source
const trustedKey = loadKeyFromConfig();
jwt.verify(token, trustedKey, { algorithms: ['RS256'] });
```

### Token leakage in URL

```python
# VULNERABLE: token accepted from query string
@app.route("/api/data")
def get_data():
    token = request.args.get("token")  # logged by proxies, browsers, referrers
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    return ...

# SECURE: token from Authorization header only
@app.route("/api/data")
def get_data():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401)
    token = auth[7:]
    payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    return ...
```

### Insecure token storage

```javascript
// VULNERABLE: storing tokens in localStorage exposes them to XSS
localStorage.setItem("access_token", token);

// SECURE: store refresh token in httpOnly, Secure, SameSite cookie
// (access tokens may still be kept in memory only)
res.cookie("refresh_token", refreshToken, {
  httpOnly: true,
  secure: true,
  sameSite: "strict",
  maxAge: 7 * 24 * 60 * 60 * 1000
});
```

### Refresh token rotation

```python
# VULNERABLE: refresh token reused indefinitely
@app.route("/refresh", methods=["POST"])
def refresh():
    refresh_token = request.json.get("refresh_token")
    user_id = validate_refresh_token(refresh_token)  # token never invalidated
    return jsonify(access_token=create_access_token(user_id))

# SECURE: rotate refresh token and detect reuse
@app.route("/refresh", methods=["POST"])
def refresh():
    refresh_token = request.json.get("refresh_token")
    stored = db.get_refresh_token(refresh_token)
    if not stored or stored["revoked"]:
        # If token was already rotated, possible replay attack
        db.revoke_all_user_tokens(stored["user_id"])
        abort(401)
    new_refresh = issue_refresh_token(stored["user_id"])
    db.revoke_refresh_token(refresh_token)
    db.store_refresh_token(new_refresh)
    return jsonify(
        access_token=create_access_token(stored["user_id"]),
        refresh_token=new_refresh
    )
```

### JWE weak encryption

```javascript
const { jwtEncrypt, jwtDecrypt, importJWK } = require('jose');

// VULNERABLE: dir (direct) encryption with a short symmetric key
const jwe = await new EncryptJWT(payload)
  .setProtectedHeader({ alg: 'dir', enc: 'A128CBC-HS256' })
  .encrypt(Buffer.from('secret'))

// SECURE: use robust key-wrapping algorithm and strong key
const jwe = await new EncryptJWT(payload)
  .setProtectedHeader({ alg: 'RSA-OAEP-256', enc: 'A256GCM' })
  .encrypt(publicKey)
```

***

## Execution
[ref: #jwt-execution]

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

> **Subagent constraint reminder**: Subagents must NOT modify project source code. They may only write report files under `{{ REPORTS_ROOT }}/`.

### Phase 1: Map the JWT Lifecycle

Launch a subagent with the following instructions:

> **Goal**: Map how the application creates, transmits, and verifies JWTs. Identify every JWT issuance and verification site, the library used, the signing algorithm and key/secret configuration, and the claims that are used for authorization. Write results to `{{ REPORTS_ROOT }}/09_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, authentication layer, and middleware patterns.
>
> **What to search for**:
>
> **1. JWT library imports** — identify which JWT library is in use:
> - Python: `import jwt`, `from jose import`, `from authlib import`, `import python_jose`
> - Node.js: `require('jsonwebtoken')`, `import jwt from 'jsonwebtoken'`, `jose`, `@nestjs/jwt`
> - Java: `io.jsonwebtoken`, `com.auth0.jwt`, `nimbus-jose-jwt`
> - Go: `github.com/golang-jwt/jwt`, `github.com/dgrijalva/jwt-go` (archived — CVE-2020-26160; flag the import itself), `github.com/lestrrat-go/jwx`
> - Ruby: `jwt` gem (`require 'jwt'`)
> - PHP: `firebase/php-jwt`, `lcobucci/jwt`
> - C#: `System.IdentityModel.Tokens.Jwt`, `Microsoft.AspNetCore.Authentication.JwtBearer`
>
> **2. JWT signing / issuance sites** — where tokens are created:
> - `jwt.encode(...)`, `jwt.sign(...)`, `Jwts.builder().signWith(...)`, `JWT.create().sign(...)`
> - Note the algorithm used (`HS256`, `RS256`, etc.) and where the secret/key comes from (env var, config, hardcoded)
>
> **3. JWT verification / decoding sites** — where tokens are consumed:
> - `jwt.decode(...)`, `jwt.verify(...)`, `Jwts.parserBuilder()...parseClaimsJws(...)`, `JWT::decode(...)`
> - Note what options are passed: `algorithms`, `options`, `verify_signature`, `verify_exp`
> - Note if it's a raw `decode` (no verification) vs. a `verify` call
>
> **4. Token extraction** — where the token is read from the incoming request:
> - Authorization header: `request.headers.get("Authorization")`, `req.headers['authorization']`
> - Cookie: `request.cookies.get("token")`, `req.cookies.token`
> - Query parameter: `request.args.get("token")`, `req.query.token`
>
> **5. Authorization middleware / decorators** — centralized JWT checks:
> - `@jwt_required`, `@login_required`, `requireAuth`, `JwtAuthGuard`, `[Authorize]`, middleware functions
> - Note which routes are protected and which are unprotected
>
> **6. Signing secret / key configuration**:
> - Where the HMAC secret or RSA/EC key is defined and loaded (env var, config file, hardcoded string)
> - Whether it looks strong (long random string) or weak (short, common word)
>
> **7. Claim usage**:
> - Which claims are extracted and used for authorization (`user_id`, `role`, `permissions`, `sub`)
> - Whether `exp`, `iss`, `aud`, `nbf` are checked
>
> **Output format** — write to `{{ REPORTS_ROOT }}/09_recon.md`:
>
> ```markdown
> # JWT Recon: [Project Name]
>
> ## Summary
> JWT is [used / not used] in this codebase.
> Library: [library name and version if visible]
> Algorithm(s): [HS256 / RS256 / etc.]
>
> ## Issuance Sites
>
> ### 1. [Descriptive name — e.g., "Token generation in login endpoint"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [function name or route]
> - **Algorithm**: [e.g., HS256]
> - **Secret/key source**: [env var name / hardcoded string / config key]
> - **Claims set**: [list of claims added to the payload]
> - **Code snippet**:
>   ```
>   [the signing call]
>   ```
>
> ## Verification Sites
>
> ### 1. [Descriptive name — e.g., "Token verification in auth middleware"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / middleware**: [function name]
> - **Verification call**: [jwt.decode / jwt.verify / parseClaimsJws / etc.]
> - **Algorithm restriction**: [algorithms=["HS256"] / no restriction / unknown]
> - **Signature verification**: [enabled / disabled / unclear]
> - **Claims validated**: [exp / iss / aud / none / unknown]
> - **Token source**: [Authorization header / cookie / query param]
> - **kid/jwk/jku used**: [yes — describe how / no]
> - **Code snippet**:
>   ```
>   [the verification call and surrounding context]
>   ```
>
> ## Secret / Key Configuration
> - **Secret source**: [env var / hardcoded / config file]
> - **Apparent strength**: [strong (long random) / weak (short/common) / unknown]
> - **Code snippet** (if hardcoded or suspicious):
>   ```
>   [relevant code]
>   ```
>
> ## Authorization Middleware Coverage
> - **Protected routes**: [list or description]
> - **Unprotected routes**: [list or "none observed"]
> ```

### After Phase 1: Check for JWT Usage Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/09_recon.md`. If the summary states JWT is **not used** (no issuance or verification sites were found), **skip Phases 2 and 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/09_jwt.md` and stop:

```markdown
# JWT Analysis Results

No JWT usage detected in this codebase.
```

Only proceed to Phase 2 if Phase 1 found at least one JWT verification site.

### Phase 2: Batched Verify — Analyze Each Verification Site

For **each** JWT verification site listed in `{{ REPORTS_ROOT }}/09_recon.md`, launch a separate subagent with the following instructions. Number batch files sequentially: `{{ REPORTS_ROOT }}/09_batch_1.md`, `{{ REPORTS_ROOT }}/09_batch_2.md`, etc.

> **Goal**: Analyze the single JWT verification site assigned to you. Determine whether it is exploitable. Check for algorithm confusion, missing signature verification, weak secrets, header injection attacks, missing claim validation, token leakage, insecure storage, refresh token reuse, and JWKS trust confusion. Write results to `{{ REPORTS_ROOT }}/09_batch_N.md`.
>
> **Context**: You will be given the project's architecture summary and the Phase 1 recon output. Focus only on the verification site assigned to you.
>
> **Checks to perform**:
>
> **Check 1 — Algorithm restriction**
> - Is the allowed algorithm explicitly specified in the verification call?
> - If no algorithm restriction is present, can the token's `alg` header be set to `none` to skip signature verification?
> - If the server uses an asymmetric algorithm (RS256, ES256), does the verification code also accept HMAC algorithms (HS256)? If so, the server may be vulnerable to the RS256→HS256 confusion attack.
>
> **Check 2 — Signature verification enabled**
> - Is the token passed through a verify/parse call that actually checks the signature, or only through a decode-only call?
> - Look for options like `verify_signature: False`, `complete=False`, or the use of `jwt.decode()` (Node.js) instead of `jwt.verify()`
> - Manual base64-decode of the payload without any signature check is always vulnerable
>
> **Check 3 — HMAC secret strength**
> - Is the secret hardcoded in source code? If so, is it a common word or short string?
> - Is the secret loaded from an environment variable or config? Even then, note if the default or example value is weak
> - A secret shorter than 32 characters or composed of dictionary words is likely brute-forceable
>
> **Check 4 — Embedded JWK / JKU / X5U header injection**
> - Does the verification code read the `jwk` field from the token header and use it to verify the same token?
> - Does the code fetch a key from a URL specified in the `jku` or `x5u` header without validating the URL against an allowlist?
> - If either is true, the verification is fully bypassable
>
> **Check 5 — `kid` header injection**
> - Is the `kid` header value extracted from the token before verification and used to look up a key?
> - Is the `kid` value interpolated into a SQL query without parameterization? → SQL injection
> - Is the `kid` value used to construct a file path without sanitization? → path traversal / key substitution
>
> **Check 6 — Claim validation**
> - Is `exp` (expiry) checked? If not, expired tokens are valid forever
> - Is `iss` (issuer) checked? If not, tokens from other issuers are accepted
> - Is `aud` (audience) checked? If not, tokens for other services are accepted
> - Are security-sensitive claims like `role` or `permissions` present but not validated against a server-side source?
>
> **Check 7 — Token revocation**
> - Is there a token blacklist, revocation endpoint, or short-lived token + refresh-token pattern?
> - If tokens are long-lived (hours or more) with no revocation mechanism, stolen tokens remain valid
>
> **Check 8 — Token leakage and storage**
> - Is the token ever read from a URL query parameter?
> - Is the token stored in `localStorage` or `sessionStorage` on the frontend?
>
> **Check 9 — Refresh token rotation**
> - Are refresh tokens rotated and invalidated after use?
> - Is reuse of an already-rotated refresh token detected and rejected?
>
> **Check 10 — JWKS endpoint trust**
> - If the site fetches keys from a JWKS URL, is the URL pinned or allowlisted?
> - Is TLS certificate validation performed?
>
> **Classification**:
> - **[VULNERABLE]**: The weakness is clearly present with no effective mitigation — the attack path is directly exploitable.
> - **[LIKELY VULNERABLE]**: The weakness is probably present but requires confirming a secondary condition (e.g., library version behavior, default option value).
> - **[NOT VULNERABLE]**: The implementation correctly addresses this check.
> - **[NEEDS MANUAL REVIEW]**: Cannot determine the vulnerability status with confidence from static analysis alone.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/09_batch_N.md`:
>
> ```markdown
> # JWT Batch Analysis: [Site Name]
>
> ## Site
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / middleware**: [function name]
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **Vulnerability class**: [e.g., "Missing signature verification" / "alg:none accepted" / "Weak HMAC secret" / "JWK header injection" / "kid SQL injection" / "Missing exp validation"]
> - **Issue**: [Clear description of what is wrong]
> - **Attack scenario**: [Step-by-step: what the attacker does, what token they craft or modify, what access they gain]
> - **Impact**: [What an attacker can achieve — forge arbitrary identity, escalate privileges, access other users' data, etc.]
> - **Remediation**: [Specific fix — add algorithms restriction, enable verify_signature, load secret from env, pin JWKS URL, parameterize kid lookup, add exp validation, etc.]
> - **Dynamic Test**:
>   ```
>   [Proof-of-concept using jwt_tool, hashcat, or curl.
>    Show the exact command to reproduce the issue.
>    Examples:
>    - jwt_tool <token> -X a   (test alg:none)
>    - jwt_tool <token> -X s   (test RS256→HS256 confusion)
>    - hashcat -a 0 -m 16500 <token> wordlist.txt   (brute-force HMAC secret)
>    - Manual: modify payload, set alg:none, send to endpoint]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **Vulnerability class**: [class]
> - **Issue**: [What appears to be wrong]
> - **Uncertainty**: [What needs to be confirmed — e.g., "Library version determines default behavior"]
> - **Remediation**: [Fix]
> - **Dynamic Test**:
>   ```
>   [payload or command to attempt exploitation]
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **Reason**: [e.g., "Algorithm restricted to HS256 with strong env-loaded secret; exp validated"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **Uncertainty**: [Why the vulnerability status cannot be determined statically]
> - **Suggestion**: [What to inspect manually — e.g., "Confirm what JWT library version is installed; older versions of PyJWT accept alg:none by default"]
> ```

### Phase 3: Merge Batch Findings into the Final Report

After all Phase 2 subagents complete, read every `{{ REPORTS_ROOT }}/09_batch_*.md` file and consolidate them into `{{ REPORTS_ROOT }}/09_jwt.md`.

The merged report must include:

```markdown
# JWT Analysis Results: [Project Name]

## Executive Summary
- Verification sites analyzed: [N]
- [VULNERABLE]: [N]
- [LIKELY VULNERABLE]: [N]
- [NOT VULNERABLE]: [N]
- [NEEDS MANUAL REVIEW]: [N]

## Findings

[paste findings from each batch file, grouped by verification site]

## Secondary Patterns Checked
- Token leakage in URL query parameters: [yes / no — details]
- Insecure token storage (`localStorage`, missing `httpOnly`): [yes / no — details]
- Refresh token rotation / reuse detection: [yes / no — details]
- Token binding (TLS / device): [yes / no — details]
- JWKS endpoint trust / key rotation: [yes / no — details]
- JWE weak encryption: [yes / no — details]

## Recommendations
- Prioritize [VULNERABLE] findings first.
- Treat [LIKELY VULNERABLE] findings as high priority until confirmed.
- For [NEEDS MANUAL REVIEW] findings, note the missing information and assign for manual verification.
```

***

## References
[ref: #jwt-references]

- [OWASP API Security Top 10 2023 — API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Key Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html)
- [CWE-204: Observable Response Discrepancy](https://cwe.mitre.org/data/definitions/204.html)
- [CWE-306: Missing Authentication for Critical Function](https://cwe.mitre.org/data/definitions/306.html)
- [CWE-307: Improper Restriction of Excessive Authentication Attempts](https://cwe.mitre.org/data/definitions/307.html)
- [CWE-330: Use of Insufficiently Random Values](https://cwe.mitre.org/data/definitions/330.html)
- [CWE-345: Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)
- [CWE-347: Improper Verification of Cryptographic Signature](https://cwe.mitre.org/data/definitions/347.html)
- [CWE-384: Session Fixation](https://cwe.mitre.org/data/definitions/384.html)
- [CWE-522: Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html)
- [CWE-613: Insufficient Session Expiration](https://cwe.mitre.org/data/definitions/613.html)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [CWE-94: Improper Control of Generation of Code](https://cwe.mitre.org/data/definitions/94.html)
- [CWE-98: Improper Control of Filename for Include/Require Statement in PHP Program](https://cwe.mitre.org/data/definitions/98.html)
- [CWE-200: Information Exposure](https://cwe.mitre.org/data/definitions/200.html)
- [CWE-327: Use of a Broken or Risky Cryptographic Algorithm](https://cwe.mitre.org/data/definitions/327.html)

***

## Important Reminders
[ref: #jwt-important-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Subagents must NOT modify project source code; they may only write report files under `{{ REPORTS_ROOT }}/`.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete.
- **Phase 1 is purely discovery**: locate every JWT issuance, verification, and configuration site. Do not attempt to assess security in Phase 1 — that is Phase 2's job.
- **Phase 2 is purely analysis**: for each verification site found in Phase 1, systematically check every vulnerability class. Do not search for new sites in Phase 2 — focus on what Phase 1 found.
- If no JWT usage is found in Phase 1, skip Phases 2 and 3 entirely and write a "No JWT usage detected" result file.
- The most critical checks are: signature verification disabled, algorithm not restricted (alg:none / RS256→HS256 confusion), and weak or hardcoded HMAC secret. These lead directly to full authentication bypass.
- `jwt.decode()` in Node.js's `jsonwebtoken` library is a decode-only function — it never verifies the signature. Only `jwt.verify()` validates the signature. Confusing the two is a common and critical mistake.
- In Python's PyJWT, versions before 2.0 accepted `alg: none` by default and did not require an `algorithms` parameter. If the codebase does not pin the version or restrict algorithms, flag it.
- Algorithm confusion (RS256→HS256) requires: (a) the server uses RS256 with a key pair, (b) the public key is accessible, and (c) the verification code does not restrict the algorithm. All three must be present.
- `kid` injection is often overlooked: always check how the key lookup is implemented when `kid` is present in the token header.
- Do not forget secondary patterns: tokens in URLs, insecure storage, refresh token reuse, and JWKS trust confusion can be just as impactful as algorithm confusion.
- When in doubt, classify as `[NEEDS MANUAL REVIEW]` rather than `[NOT VULNERABLE]`. False negatives are worse than false positives in security assessment.
