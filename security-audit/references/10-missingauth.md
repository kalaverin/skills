# Missing Authentication & Broken Function-Level Authorization Detection

[ref: #missingauth-detection]

You are performing a focused security assessment to find missing authentication and broken function-level authorization vulnerabilities in a codebase, mapping to OWASP API Security Top 10 2023 **API2:2023 Broken Authentication** and **API5:2023 Broken Function Level Authorization**. This skill uses a three-phase approach with subagents: **recon** (map endpoints and the permission system), **batched verify** (check authentication and authorization in parallel batches of 3 endpoints each), and **merge** (consolidate batch results into the final report).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

---

## OWASP Mapping

This reference implements detection guidance for two OWASP API Security Top 10 2023 risk classes.

### API2:2023 — Broken Authentication

| Threat agents / Attack vectors | Security weakness | Impacts |
| --- | --- | --- |
| API Specific : Exploitability **Easy** | Prevalence **Common** : Detectability **Easy** | Technical **Severe** : Business Specific |
| Authentication mechanisms are exposed to everyone and are an easy target; exploitation tools are widely available. | Misconceptions about authentication boundaries and implementation complexity make these issues common; detection methodologies are easy to create. | Attackers can gain complete control of other users' accounts, read personal data, and perform sensitive actions on their behalf; systems may not distinguish attacker actions from legitimate ones. |

**Direct citations from OWASP API2:2023**:

- "Forgot password / reset password should be treated the same way as authentication mechanisms."
- "Permits credential stuffing ... brute force ... without presenting captcha/account lockout mechanism."
- "Allows users to change their email address, current password, or do any other sensitive operations without asking for password confirmation."
- "Doesn't validate the authenticity of tokens. Accepts unsigned/weakly signed JWT tokens ... Doesn't validate the JWT expiration date."
- "A microservice is vulnerable if other microservices can access it without authentication or uses weak or predictable tokens."

### API5:2023 — Broken Function Level Authorization

| Threat agents / Attack vectors | Security weakness | Impacts |
| --- | --- | --- |
| API Specific : Exploitability **Easy** | Prevalence **Common** : Detectability **Easy** | Technical **Severe** : Business Specific |
| Attackers send legitimate API calls to endpoints they should not access as anonymous or regular users; exposed endpoints are easily exploited. | Authorization checks are managed via configuration or code; complex roles/groups/hierarchies make implementation confusing; APIs are structured, making function guessing predictable. | Unauthorized access to functionality; administrative functions are key targets and may lead to disclosure, loss, corruption, or service disruption. |

**Direct citations from OWASP API5:2023**:

- "Don't assume that an API endpoint is regular or administrative only based on the URL path."
- "Can a regular user access administrative endpoints?"
- "Can a user perform sensitive actions ... by simply changing the HTTP method (e.g. from `GET` to `DELETE`)?"
- "Can a user from group X access a function that should be exposed only to users from group Y, by simply guessing the endpoint URL and parameters?"
- "The enforcement mechanism(s) should deny all access by default, requiring explicit grants to specific roles for access to every function."

**Relationship to this skill**: Use the API2 checklist when evaluating authentication strength, brute-force/lockout protections, token authenticity, and microservice authentication. Use the API5 checklist when evaluating whether a privileged function requires the correct role/permission.

## What This Skill Covers

### Missing Authentication
An endpoint performs a sensitive action but requires **no login at all** — any anonymous HTTP request can trigger it.

### Broken Function-Level Authorization
An endpoint requires authentication (user must be logged in) but **does not check whether the authenticated user has the required role or permission** to invoke that function. The classic example: a regular user calling an admin-only API.

### What This Skill Is NOT

Do not conflate missing/broken authentication and function-level authorization with the following adjacent problems. When you encounter them, route them to the correct security-audit reference and do **not** report them under this skill:

- **IDOR / Horizontal privilege escalation / BOLA**: Authenticated user A accessing user B's resource by changing an ID, UUID, or path parameter. This skill covers **vertical** privilege escalation (regular user → admin) and **unauthenticated** access. Route IDOR/BOLA findings to the IDOR/BOLA scan.
- **JWT cryptographic attacks** (e.g., key confusion, algorithm-confusion `alg: none`, weak signing keys, missing `exp`/`iss`/`aud` validation, token smuggling). Route advanced JWT-only attacks to sast-jwt. Token authenticity checks such as rejection of `alg: none`, expiration/claim validation, and weak signing keys are **in scope** for this skill when they appear as part of the authentication gate, but deep JWT crypto analysis belongs to sast-jwt.
- **Business logic flaws**: Price manipulation, workflow bypass, abuse of legitimate flows (e.g., negative quantity, race conditions), and domain-rule violations. These are covered by the business-logic scan.
- **Security misconfiguration**: Debug/admin endpoints exposed due to framework defaults, verbose error messages, CORS misconfiguration, insecure cookie flags, or missing security headers. While an unauthenticated `/admin` endpoint may be reported here if the only issue is missing auth, the underlying misconfiguration category (CORS, debug mode, header issues) is covered by sast-misconfiguration.
- **Injection vulnerabilities**: SQL injection, command injection, SSRF, XSS, SSTI, etc., that may be reachable through an authenticated endpoint. Route these to their respective security-audit references.
- **Session fixation / insecure session management bugs** (e.g., predictable session IDs, missing `HttpOnly`/`Secure`/`SameSite`) are primarily covered by sast-misconfiguration and sast-session, although they may be mentioned here as bypass patterns.
- **OAuth / OIDC / SAML protocol implementation flaws** (e.g., missing PKCE, redirect_uri mismatch, SAML signature wrapping) are covered by sast-auth-protocol when such a reference exists; otherwise treat as "Needs Manual Review" with a pointer to the relevant cheat sheet.

When a finding overlaps multiple categories (for example, an admin endpoint that is both unauthenticated and returns verbose stack traces), report the missing-auth issue here and note the related category in the "Concern" or "Remediation" field.

## CWE Mapping

The following CWE entries are relevant to the vulnerability classes in this skill. Cite the most specific CWE in each finding.

| CWE | Name | Where it applies in this skill |
| --- | --- | --- |
| [CWE-287](https://cwe.mitre.org/data/definitions/287.html) | Improper Authentication | Any endpoint that performs a sensitive action without verifying the caller's identity (Classes 1, 6, 7). |
| [CWE-306](https://cwe.mitre.org/data/definitions/306.html) | Missing Authentication for Critical Function | Sensitive admin/user-management/config endpoints reachable without login (Classes 1, 2). |
| [CWE-307](https://cwe.mitre.org/data/definitions/307.html) | Improper Restriction of Excessive Authentication Attempts | Login, forgot-password, and password-reset endpoints without rate limiting, lockout, or CAPTCHA (Class 4). |
| [CWE-204](https://cwe.mitre.org/data/definitions/204.html) | Observable Response Discrepancy | Authentication endpoints that return different error messages or timing for valid vs. invalid usernames, enabling user enumeration. |
| [CWE-798](https://cwe.mitre.org/data/definitions/798.html) | Use of Hard-coded Credentials | Static/hardcoded/predictable service tokens, API keys, or default passwords used for microservice or internal authentication (Class 7). |
| [CWE-862](https://cwe.mitre.org/data/definitions/862.html) | Missing Authorization | Authenticated endpoint that does not verify the caller has permission to invoke the function (Classes 2, 3). |
| [CWE-285](https://cwe.mitre.org/data/definitions/285.html) | Improper Authorization | Incorrect or bypassable role checks, inverted comparisons, or checks conditional on attacker-controlled input (Classes 2, 3). |
| [CWE-352](https://cwe.mitre.org/data/definitions/352.html) | Cross-Site Request Forgery (CSRF) | State-changing endpoints that rely only on session cookies without anti-CSRF tokens or SameSite protections; overlaps with missing/insufficient authentication for web clients. |
| [CWE-384](https://cwe.mitre.org/data/definitions/384.html) | Session Fixation | Authentication flows that do not rotate session identifiers after login. |
| [CWE-521](https://cwe.mitre.org/data/definitions/521.html) | Weak Password Requirements | Password policies that allow weak or breached passwords (Class 4). |
| [CWE-522](https://cwe.mitre.org/data/definitions/522.html) | Insufficiently Protected Credentials | Passwords stored or transmitted in plaintext, weakly hashed, or logged. |
| [CWE-639](https://cwe.mitre.org/data/definitions/639.html) | Authorization Bypass Through User-Controlled Key | Role/permission check that depends on a user-controlled header, parameter, or claim. |
| [CWE-918](https://cwe.mitre.org/data/definitions/918.html) | Server-Side Request Forgery (SSRF) | Internal service endpoints that accept attacker-influenced target URLs and lack caller authentication (Class 7). |

Use the primary mappings (CWE-287, CWE-306, CWE-307, CWE-798, CWE-862, CWE-285) in the final report unless a more specific entry clearly fits the observed pattern.

---

## Vulnerability Classes

### Class 1: Unauthenticated Sensitive Endpoint
The endpoint modifies data, returns private information, or performs an administrative action — with no authentication required.

```
GET /api/admin/users          → returns full user list, no token needed
DELETE /api/admin/users/5     → deletes a user, no token needed
POST /api/settings/smtp       → updates server config, no token needed
```

### Class 2: Authenticated but Missing Role Check
The endpoint requires a valid session/token but performs no role or permission check. Any authenticated user — regardless of role — can invoke admin or privileged functions.

```
Regular user sends:
DELETE /api/admin/users/5
Authorization: Bearer <regular_user_token>
→ Server deletes the user without checking if the caller is an admin
```

### Class 3: Incomplete or Bypassable Authorization
Authorization logic is present but can be bypassed:
- Role check exists in the GET handler but not in the corresponding DELETE/POST handler
- Role check is conditional on a request header or parameter the attacker controls
- Middleware is registered but the route is mounted before the middleware applies

### Class 4: Missing Anti-Brute-Force / Account Lockout / CAPTCHA / Weak Password Policy
Authentication endpoints (login, password recovery / forgot-password, password reset) allow unlimited credential-stuffing or brute-force attempts against the same account, lack account lockout or CAPTCHA/human-verification, or accept weak passwords.

### Class 5: Missing Re-authentication for Sensitive Operations
Endpoints that change account ownership or security settings — email address, current password, 2FA/OTP configuration, API key regeneration — do not require the user to re-prove their identity (current password, MFA, or step-up authentication).

### Class 6: Broken Token Authenticity Validation
Token verification accepts unsigned/weakly signed JWTs (`{"alg":"none"}`), ignores expiration (`exp`) or other required claims (`iss`, `aud`, `nbf`), or uses weak encryption/signing keys.

### Class 7: Missing or Weak Microservice-to-Microservice Authentication
Internal/service-to-service endpoints require no authentication, accept predictable/static service tokens, or use insecurely managed service accounts (long-lived shared secrets, overly broad permissions, no rotation).

---

## Authorization Patterns That PREVENT Vulnerabilities

When you see these patterns, the endpoint is likely **not vulnerable**:

**1. Authentication + role-check middleware on a route group**
```javascript
// Express: all /admin routes protected
router.use('/admin', auth, requireRole('admin'));
router.delete('/admin/users/:id', deleteUser);   // protected by above

// Flask-Login + custom decorator
@app.route('/admin/users')
@login_required
@admin_required
def list_users(): ...
```

**2. Declarative role annotations (Java / Spring)**
```java
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/api/admin/users/{id}")
public ResponseEntity<?> deleteUser(@PathVariable Long id) { ... }
```

**3. In-handler role check before sensitive action**
```python
# Django
@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    User.objects.filter(id=user_id).delete()
    return HttpResponse(status=204)
```

**4. Middleware gate applied to entire prefix**
```go
// Chi router — admin group protected
r.Group(func(r chi.Router) {
    r.Use(AdminOnly)
    r.Delete("/admin/users/{id}", deleteUser)
})
```

**5. Policy/Gate objects**
```php
// Laravel Gate
Gate::define('admin-action', fn($user) => $user->role === 'admin');
// In controller
$this->authorize('admin-action');
```

---

## How to Prevent

Use the following prevention checklist when evaluating code and writing remediation guidance. Items marked **(API2)** derive from OWASP API2:2023 Broken Authentication; items marked **(API5)** derive from OWASP API5:2023 Broken Function Level Authorization.

### Authentication fundamentals

- Know every authentication flow (mobile, web, deep links, one-click, machine-to-machine) and document them. Ask engineers which flows the design review missed. **(API2)**
- Use standards and battle-tested libraries for authentication, token generation, and password storage. Do not invent custom crypto or session schemes. **(API2)**
- Treat credential recovery / forgot-password / reset-password endpoints with the same brute-force, rate-limit, lockout, and monitoring controls as login endpoints. **(API2)**
- Require re-authentication (current password, MFA/OTP, step-up token, or biometric confirmation) before sensitive operations: changing email address, current password, 2FA/OTP/phone number, API key regeneration, ownership transfer, or security settings. **(API2)**
- Implement multi-factor authentication (MFA) wherever feasible, and enforce it for privileged accounts. **(API2)**

### Brute-force and account-takeover protections

- Implement anti-brute-force controls on authentication endpoints that are stricter than general API rate limiting: per-account lockout, progressive delays, CAPTCHA/reCAPTCHA/human-verification challenges after repeated failures, and IP/device reputation checks. **(API2)**
- Implement weak-password checks: minimum length (e.g., 12+ characters), complexity recommendations, and breach-list screening against known-compromised passwords (e.g., Have I Been Pwned). **(API2)**
- Return identical generic error messages for invalid username and invalid password to prevent user enumeration. **(API2 / CWE-204)**
- Log and alert on credential-stuffing patterns (high velocity, distributed attempts, known password lists).

### Token and session management

- Validate token authenticity: reject unsigned JWTs (`{"alg":"none"}`), unsafe algorithms (`none`, `HS256` with symmetric key confusion), and tokens with missing or invalid signatures. **(API2)**
- Validate all required claims (`exp`, `nbf`, `iss`, `aud`) and reject expired or not-yet-valid tokens. **(API2)**
- Use strong, randomly generated signing/encryption keys; never ship default, hardcoded, or short keys. Rotate keys on a schedule and after suspected compromise. **(API2)**
- Use secure session management: cryptographically random session IDs, secure transmission (TLS), `HttpOnly`/`Secure`/`SameSite=Strict` or `Lax` cookies, short session timeouts, idle timeouts, and session rotation after authentication elevation. Do not put session identifiers in URLs.
- Avoid JWT-vs-session confusion: the application should use one primary session/token mechanism per endpoint class and reject unexpected token types. Do not accept a session cookie as a fallback when a JWT is missing without equivalent validation.
- Do not log API keys, tokens, passwords, or session identifiers in application logs, reverse-proxy logs, or exception traces. If logging is required, log only a redacted prefix or a token hash. **(API2 / operational)**

### Function-level authorization

- Adopt a **deny-by-default** authorization model: every function must explicitly grant access to specific roles/groups; absence of a grant means deny. **(API5)**
- Centralize authorization enforcement in a single module, middleware, policy engine, or abstract administrative controller that is invoked from all business functions. **(API5)**
- Review every endpoint against function-level authorization flaws, considering the user hierarchy, groups, sub-users, and multi-role users. **(API5)**
- Ensure administrative functions inside regular controllers perform role checks just like functions in dedicated admin controllers. **(API5)**
- Do not rely solely on URL path conventions (`/admin/`) to hide privileged endpoints; enforce checks in code for every method. **(API5)**
- Protect all HTTP methods of a resource consistently; a `DELETE` or `POST` must not be unguarded just because `GET` is protected.

### OAuth / OIDC / SAML

- For OAuth/OIDC public clients, require PKCE and validate the `code_challenge`/`code_verifier` pair. **(API2 / OAuth)**
- Enforce exact-match redirect URI validation; do not allow wildcards, partial matches, or open redirectors. **(API2 / OAuth)**
- Validate ID tokens (signature, issuer, audience, expiration) and do not use them as access tokens.
- For SAML, enforce strict signature validation, reject unsigned assertions, and use a hardened XML parser to prevent comment injection, signature wrapping, and XSW attacks.

### GraphQL and API surface

- Disable anonymous GraphQL access unless it is explicitly intended and limited to public fields.
- Disable introspection (`__schema`, `__type`) in production unless required and protected.
- Apply authz checks at resolver level, not just at the HTTP edge; batched or aliased queries can bypass per-request controls.
- Treat GraphQL query/mutation batching as a brute-force amplifier: apply the same per-account lockout and rate limits to batched login/password-reset operations as to individual requests.

### Internal / debug / admin endpoints

- Protect debug, admin, management, actuator, Swagger/OpenAPI, and health-detail endpoints with authentication and authorization appropriate to their sensitivity. Do not rely on "obscurity" or non-production ports.
- Remove or disable debug/admin routes and verbose error handlers in production builds.
- Authenticate all microservice-to-microservice calls with short-lived, scoped tokens (e.g., mTLS, SPIFFE/SPIRE, workload identity, or signed service tokens). Avoid static shared secrets. Rotate service credentials and follow least-privilege service accounts.

### Operational checks

- Review infrastructure configuration (reverse proxy, API gateway, WAF, load balancer) to ensure auth enforcement is not bypassed by path normalization, case variations, trailing slashes, or host-header rewriting.
- Monitor for authentication/authorization anomalies: privilege-escalation attempts, method-switching, and requests to undocumented endpoints.

## Vulnerable vs. Secure Examples

### Python — Django

```python
# VULNERABLE: No authentication at all
def list_all_users(request):
    users = User.objects.values('id', 'email', 'is_staff')
    return JsonResponse(list(users), safe=False)

# VULNERABLE: Authenticated but no role check
@login_required
def delete_user(request, user_id):
    User.objects.filter(id=user_id).delete()
    return HttpResponse(status=204)

# SECURE
@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    User.objects.filter(id=user_id).delete()
    return HttpResponse(status=204)
```

### Python — Flask

```python
# VULNERABLE: No auth decorator
@app.route('/admin/users')
def list_users():
    return jsonify([u.to_dict() for u in User.query.all()])

# VULNERABLE: Login required but no role check
@app.route('/admin/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# SECURE
@app.route('/admin/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        abort(403)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
```

### Node.js — Express

```javascript
// VULNERABLE: No auth middleware
router.get('/api/admin/users', async (req, res) => {
    const users = await User.find({});
    res.json(users);
});

// VULNERABLE: Auth middleware present but no role check
router.delete('/api/admin/users/:id', auth, async (req, res) => {
    await User.findByIdAndDelete(req.params.id);
    res.sendStatus(204);
});

// SECURE
const requireAdmin = (req, res, next) => {
    if (req.user.role !== 'admin') return res.sendStatus(403);
    next();
};
router.delete('/api/admin/users/:id', auth, requireAdmin, async (req, res) => {
    await User.findByIdAndDelete(req.params.id);
    res.sendStatus(204);
});
```

### Ruby on Rails

```ruby
# VULNERABLE: No before_action
def destroy
    User.find(params[:id]).destroy
    head :no_content
end

# VULNERABLE: Authenticated but no admin check
before_action :authenticate_user!
def destroy
    User.find(params[:id]).destroy
    head :no_content
end

# SECURE
before_action :authenticate_user!
before_action :require_admin

def destroy
    User.find(params[:id]).destroy
    head :no_content
end

private

def require_admin
    head :forbidden unless current_user.admin?
end
```

### Java — Spring Boot

```java
// VULNERABLE: No security annotation
@DeleteMapping("/api/admin/users/{id}")
public ResponseEntity<?> deleteUser(@PathVariable Long id) {
    userRepo.deleteById(id);
    return ResponseEntity.noContent().build();
}

// VULNERABLE: Authenticated but wrong role
@DeleteMapping("/api/admin/users/{id}")
@Secured("ROLE_USER")  // any user can call this
public ResponseEntity<?> deleteUser(@PathVariable Long id) {
    userRepo.deleteById(id);
    return ResponseEntity.noContent().build();
}

// SECURE
@DeleteMapping("/api/admin/users/{id}")
@PreAuthorize("hasRole('ADMIN')")
public ResponseEntity<?> deleteUser(@PathVariable Long id) {
    userRepo.deleteById(id);
    return ResponseEntity.noContent().build();
}
```

### Go

```go
// VULNERABLE: No auth middleware on route
r.Delete("/admin/users/{id}", deleteUser)

// VULNERABLE: Auth middleware but no role check in handler
r.With(AuthMiddleware).Delete("/admin/users/{id}", deleteUser)

func deleteUser(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    db.DeleteUser(id)  // no role check
    w.WriteHeader(http.StatusNoContent)
}

// SECURE
r.Group(func(r chi.Router) {
    r.Use(AuthMiddleware)
    r.Use(AdminOnlyMiddleware)
    r.Delete("/admin/users/{id}", deleteUser)
})
```

### PHP — Laravel

```php
// VULNERABLE: No auth middleware
Route::delete('/admin/users/{id}', [AdminController::class, 'destroy']);

// VULNERABLE: Auth but no role gate
Route::middleware('auth')->delete('/admin/users/{id}', [AdminController::class, 'destroy']);

// SECURE
Route::middleware(['auth', 'role:admin'])->delete('/admin/users/{id}', [AdminController::class, 'destroy']);

// SECURE (using Gate in controller)
public function destroy($id) {
    Gate::authorize('admin-action');
    User::findOrFail($id)->delete();
    return response()->noContent();
}
```

### C# — ASP.NET Core

```csharp
// VULNERABLE: No authorization attribute
[HttpDelete("api/admin/users/{id}")]
public async Task<IActionResult> DeleteUser(int id) {
    await _userService.DeleteAsync(id);
    return NoContent();
}

// VULNERABLE: [Authorize] but no role
[Authorize]
[HttpDelete("api/admin/users/{id}")]
public async Task<IActionResult> DeleteUser(int id) {
    await _userService.DeleteAsync(id);
    return NoContent();
}

// SECURE
[Authorize(Roles = "Admin")]
[HttpDelete("api/admin/users/{id}")]
public async Task<IActionResult> DeleteUser(int id) {
    await _userService.DeleteAsync(id);
    return NoContent();
}
```

---

## Modern Bypass Patterns & Watch-outs

The following patterns are either in scope for this skill as bypasses or are strong signals that authentication/authorization is broken. For each pattern, verify in code and, where possible, provide a dynamic-test PoC.

### 1. CORS wildcard with credentials allowed

**Vulnerable configuration**

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
```

Browsers reject `*` with credentials in theory, but misconfigured servers may echo the `Origin` header and still allow credentials, enabling cross-origin authenticated requests from attacker-controlled sites.

**Dynamic PoC**

```html
<script>
fetch('https://<target>/api/admin/users', {
  credentials: 'include',
  headers: {'X-Requested-With': 'XMLHttpRequest'}
})
.then(r => r.json())
.then(data => exfiltrate(data));
</script>
```

**Watch-out**: CORS misconfiguration itself is covered by sast-misconfiguration; flag the missing-auth/authz impact here only when the cross-origin request succeeds against a privileged endpoint.

### 2. API keys, tokens, or passwords in logs

**Vulnerable code**

```python
# Vulnerable: full token logged on every request
logger.info(f"Incoming request with Authorization: {request.headers.get('Authorization')}")
```

**Why it matters**: Reverse proxies, application logs, exception trackers, and CI artifacts that capture tokens let attackers reuse them after a log leak.

**Dynamic PoC**

```bash
# Trigger an error or inspect access logs
curl -i -H "Authorization: Bearer <SECRET_TOKEN>" https://<target>/api/admin/users
# Then grep logs for the literal token string
grep "<SECRET_TOKEN>" /var/log/app/access.log
```

**Watch-out**: If a token is found in logs, classify the finding as **Likely Vulnerable** or **Vulnerable** depending on log exposure; reference CWE-532 / CWE-522.

### 3. Insecure session management

**Vulnerable patterns**

- Predictable session IDs (`sess_0001`, sequential integers, weak RNG).
- Session cookies without `HttpOnly`, `Secure`, or `SameSite`.
- Session identifiers in URL query strings.
- No session rotation after login or privilege elevation.

**Dynamic PoC**

```bash
# 1. Authenticate and capture the session cookie.
# 2. Predict or brute-force another session ID:
for i in $(seq 1000 1100); do
  curl -b "sessionid=sess_$i" https://<target>/api/account
done
```

If a guessed session ID returns another user's data, authentication is broken.

### 4. OAuth / OIDC missing PKCE or loose redirect_uri

**Vulnerable code / config**

- Public mobile/SPA clients using authorization-code flow without PKCE.
- `redirect_uri` validation that allows subdomains or wildcards.

**Logic exploit**

An attacker who obtains a client_id can start an authorization flow, supply their own redirect_uri, and capture the authorization code on a domain they control.

**Dynamic PoC**

```bash
# Attempt authorization without code_challenge
curl -G "https://<target>/oauth/authorize" \
  -d "response_type=code" \
  -d "client_id=public-client" \
  -d "redirect_uri=https://attacker.example/callback" \
  -d "scope=admin"

# If the server redirects to the attacker URI, redirect_uri validation is broken.
```

**Routing**: Deep OAuth/OIDC protocol analysis belongs to sast-auth-protocol; report the missing-auth/authz impact here if the broken flow grants tokens to unauthorized parties.

### 5. SAML authentication bypass

**Vulnerable patterns**

- SAML response accepted without a valid signature.
- XML parser that allows comment injection or signature wrapping.
- Assertion attributes (e.g., `NameID`, `Role`) extracted from unsigned portions.

**Logic exploit**

An attacker crafts a SAML response that claims admin privileges while omitting or wrapping the signature.

**Dynamic PoC**

Capture a legitimate SAMLResponse (Base64), decode it, duplicate the signed assertion, inject an unsigned assertion with `Role="admin"`, re-encode, and POST it to the SAML ACS endpoint. If the parser selects the attacker assertion and creates an admin session, authentication is bypassed.

**Routing**: Complex SAML/XML attacks belong to sast-auth-protocol; flag the authentication-bypass impact here.

### 6. JWT-vs-session confusion

**Vulnerable code**

```python
@app.route('/api/admin/users')
def list_users():
    if 'session' in request.cookies:
        user = load_session(request.cookies['session'])
    elif 'Authorization' in request.headers:
        user = decode_jwt(request.headers['Authorization'])
    if user:
        return jsonify(all_users())
```

If the JWT verifier is stronger than the session loader (or vice versa), an attacker can switch mechanisms to bypass the stricter check.

**Dynamic PoC**

```bash
# 1. Obtain a low-privilege JWT.
# 2. Obtain a high-privilege session cookie (e.g., from XSS or leaked log).
# 3. Call the admin endpoint with the session cookie but no JWT, or with a forged JWT and no session:
curl -b "session=<HIGH_PRIV_SESSION>" https://<target>/api/admin/users
curl -H "Authorization: Bearer <FORGED_JWT>" https://<target>/api/admin/users
```

If either succeeds because the alternate path is weaker, report as **Vulnerable**.

### 7. GraphQL anonymous access and introspection

**Vulnerable configuration**

```yaml
# Apollo / graphql-config style
introspection: true
context: ({ req }) => ({ user: req.user || anonymousUser })
```

**Logic exploit**

An unauthenticated caller queries `__schema { types { name fields { name } } }` to map all mutations, then invokes an admin mutation without a token.

**Dynamic PoC**

```bash
# Anonymous introspection
curl -X POST https://<target>/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name fields { name } } } }"}'

# Anonymous admin mutation
curl -X POST https://<target>/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { deleteUser(id: 5) }"}'
```

If either succeeds, the GraphQL surface is missing authentication or function-level authorization.

### 8. Debug / admin endpoints without authentication

**Vulnerable code**

```python
if app.config['DEBUG']:
    @app.route('/debug/config')
    def debug_config():
        return jsonify(app.config)
```

**Logic exploit**

Debug routes may be registered in production because the `DEBUG` flag is inherited from environment defaults, or because the route is mounted outside the production auth group.

**Dynamic PoC**

```bash
# Probe common debug/admin paths
for path in /debug/config /actuator/env /admin /api/admin /swagger-ui.html /_debug; do
  curl -s -o /dev/null -w "%{http_code} $path\n" "https://<target>$path"
done
```

Any response other than `401`/`403`/`404` (when the route should not exist) on a privileged/debug endpoint is a missing-auth finding.

**Routing**: Debug-endpoint exposure may also be reported by sast-misconfiguration; report the missing-authentication impact here and note the overlap.

### 9. HTTP method switching on the same path

**Vulnerable code**

```python
@app.route('/api/users', methods=['GET'])
@login_required
def list_users(): ...

@app.route('/api/users', methods=['DELETE'])
def delete_all_users(): ...
```

**Dynamic PoC**

```bash
curl -X DELETE https://<target>/api/users -H "Authorization: Bearer <REGULAR_USER_TOKEN>"
```

If `DELETE` succeeds while `GET` is protected, the function-level authorization check is missing for that method.

### 10. Path normalization / case variation bypass

**Vulnerable configuration**

API gateway blocks `/admin` but the origin server also accepts `/ADMIN`, `/admin/`, `/admin//users`, or `/api/../admin/users`.

**Dynamic PoC**

```bash
curl -k https://<target>/ADMIN/users
curl -k https://<target>/admin//users
curl -k https://<target>/api/../admin/users
```

If any variant bypasses the gateway authz layer, the origin endpoint is **Likely Vulnerable** or **Vulnerable** depending on exploitability.

**Routing**: Path-normalization issues may overlap with sast-misconfiguration or gateway configuration reviews; still flag the authentication bypass here.

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Recon — Map Endpoints and Permission System

Launch a subagent with the following instructions:

> **Goal**: Build a complete map of (1) all application endpoints/routes and their current authentication/authorization posture, and (2) the role/permission system. Write results to `{{ REPORTS_ROOT }}/10_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, frameworks, route definitions, and the auth/authz strategy.
>
> **What to search for**:
>
> 1. **All route/endpoint definitions** — collect every HTTP handler, REST endpoint, GraphQL mutation/query, RPC method, or WebSocket handler:
>    - Express/Koa: `router.get/post/put/delete/patch/use`
>    - Django: `urlpatterns`, `path()`, `re_path()`
>    - Flask: `@app.route`, `@blueprint.route`
>    - Rails: `routes.rb` — `get`, `post`, `resources`, `namespace`
>    - Spring: `@GetMapping`, `@PostMapping`, `@RequestMapping`, `@DeleteMapping`, `@PutMapping`
>    - Go/Chi: `r.Get`, `r.Post`, `r.Delete`, `r.Handle`
>    - Laravel: `Route::get/post/put/delete`
>    - FastAPI: `@router.get/post/put/delete`
>    - ASP.NET: `[HttpGet]`, `[HttpPost]`, `[HttpDelete]`, `[HttpPut]`
>
> 2. **Authentication middleware and decorators** currently applied:
>    - Identify the pattern used: `@login_required`, `auth` middleware, `[Authorize]`, `authenticate_user!`, JWT verification middleware, session checks
>    - Note which routes or route groups they are applied to
>    - Note any routes explicitly excluded from auth (e.g., `except: [:index, :show]`)
>
> 3. **Role/permission system** — identify how roles are defined and checked:
>    - Role constants/enums: `ROLE_ADMIN`, `'admin'`, `UserRole.ADMIN`, `is_staff`, `is_superuser`
>    - Permission decorators: `@admin_required`, `@roles_required`, `@PreAuthorize`, `requireRole()`
>    - Middleware: `AdminOnly`, `requireAdmin`, `role:admin`
>    - Policy/Gate/Ability objects: `Gate::define`, `Policy`, `CanCanCan`, `Pundit`
>    - In-handler checks: `if user.role != 'admin'`, `if not current_user.is_admin`
>
> 4. **Sensitive/privileged endpoints** to flag — any endpoint that:
>    - Has an `/admin`, `/management`, `/internal`, `/api/admin`, `/superadmin`, `/system`, `/ops` path prefix
>    - Performs user management: create/update/delete users, change roles, reset passwords for others
>    - Manages application configuration: settings, feature flags, SMTP, secrets, environment variables
>    - Accesses financial/billing data: invoices, payments, subscriptions for all users
>    - Triggers system actions: sending emails to all users, running background jobs, clearing caches
>    - Returns aggregate or sensitive data: all users, all orders, audit logs, error logs
>
> 5. **For each endpoint, note**:
>    - Whether an auth middleware/decorator is present
>    - Whether a role/permission check is present
>    - The HTTP method(s) it handles
>    - Whether it reads, writes, or deletes data
>
> 6. **Authentication endpoints and anti-brute-force controls** — locate login, password recovery / forgot-password, and password-reset endpoints; note whether they implement:
>    - Rate limiting stricter than general API limits
>    - Account lockout after repeated failures
>    - CAPTCHA or other human-verification challenges
>    - Weak-password policy checks (length, complexity, breach-list screening)
>
> 7. **Sensitive-operation endpoints** — locate functions that change account ownership or security settings:
>    - Email address change, password change, 2FA/OTP / phone-number update, API key regeneration
>    - Note whether the handler requires re-authentication (current password, MFA, step-up token) before executing
>
> 8. **Token authenticity and validation logic** — locate JWT/API-key/token verification code:
>    - Rejection of `{"alg":"none"}` and other unsafe algorithms
>    - Validation of `exp`, `nbf`, `iss`, `aud`, and signature
>    - Strength of signing/encryption keys (no weak/default keys)
>
> 9. **Microservice / internal service communication** — locate service-to-service endpoints and clients:
>    - Internal APIs, sidecar proxies, gRPC/HTTP service calls, background-job callbacks
>    - Whether caller authentication is enforced
>    - Whether service tokens are static/hardcoded/predictable or rotated and scoped
>    - Whether service accounts follow least-privilege and are not shared across environments
>
> **What to ignore**:
> - Publicly intended endpoints: login, register, password reset request, public content (blog posts, product listings)
> - Static asset serving, health-check endpoints (`/health`, `/ping`, `/status`)
>
> **Output format** — write to `{{ REPORTS_ROOT }}/10_recon.md`:
>
> ```markdown
> # Missing Auth Recon: [Project Name]
>
> ## Permission System Summary
> - Roles identified: [list roles, e.g. admin, moderator, user]
> - Auth mechanism: [JWT / session / API key / OAuth]
> - Auth decorators/middleware: [list names, e.g. @login_required, auth, requireAdmin]
>
> ## Endpoint Inventory
>
> ### 1. [Endpoint name / description]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path`
> - **Operation**: [read / write / delete / admin-action]
> - **Auth present**: [yes / no]
> - **Role check present**: [yes / no / partial]
> - **Code snippet**:
>   ```
>   [route registration + handler signature]
>   ```
>
> [Repeat for each endpoint]
> ```

### Phase 2: Verify — Check Authentication and Authorization (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/10_recon.md` and split the endpoint inventory into **batches of up to 3 endpoints each** (each numbered `### N.` under **Endpoint Inventory**). Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned endpoints and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/10_recon.md` and count the numbered endpoint sections under **Endpoint Inventory** (`### 1.`, `### 2.`, etc.).
2. Divide them into batches of up to 3. For example, 8 endpoints → 3 batches (1–3, 4–6, 7–8).
3. For each batch, extract the full text of those endpoint sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned endpoints.
5. Each subagent writes to `{{ REPORTS_ROOT }}/10_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project uses Python/Django, include only the "Python — Django" (and if relevant, Flask) examples. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: Verify the following endpoints for missing authentication and broken function-level authorization vulnerabilities. Write results to `{{ REPORTS_ROOT }}/10_batch_[N].md`.
>
> **Your assigned endpoints** (from the recon phase):
>
> [Paste the full text of the assigned endpoint sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand the middleware ordering, role definitions, and auth patterns.
>
> **Missing auth / broken function-level auth — what to look for**:
>
> - **Missing authentication**: Sensitive action with no login/session/token required.
> - **Broken function-level authorization**: Authentication is required but no role/permission check on a privileged endpoint (vertical escalation).
>
> **What this skill is NOT** — do not flag these here:
> - **IDOR / horizontal escalation**: User A accessing user B's resource by changing an ID → covered by the IDOR skill.
> - **JWT crypto/verification bugs** → covered by sast-jwt.
>
> **Authorization patterns that PREVENT issues** — if you see these, the endpoint is likely safe:
> 1. **Authentication + role-check middleware on a route group** (e.g., `router.use('/admin', auth, requireRole('admin'))`)
> 2. **Declarative role annotations** (e.g., `@PreAuthorize("hasRole('ADMIN')")`)
> 3. **In-handler role check** before sensitive action
> 4. **Middleware gate on entire prefix** (e.g., Chi `r.Group` with `AdminOnly`)
> 5. **Policy/Gate** objects enforcing privileged actions
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **For each assigned endpoint, evaluate**:
>
> 1. **Authentication check** — is a valid login/session/token required?
>    - Is there an auth middleware, decorator, or guard on this route or its parent group?
>    - Trace the middleware chain — confirm the auth middleware runs BEFORE the handler, not after
>    - Check if the route is accidentally mounted outside an auth-protected group
>
> 2. **Role/permission check** — if the endpoint is privileged, is a role or permission verified?
>    - Look for: `is_admin`, `is_staff`, `role == 'admin'`, `hasRole('ADMIN')`, `@PreAuthorize`, `requireRole`, `can?(:manage, ...)`, `Gate::allows`, `authorize('admin-action')`
>    - Verify the check runs on every HTTP method — a DELETE may be unguarded even if GET is protected
>    - Check that the role comparison is not inverted or trivially bypassable
>
> 3. **Edge cases**:
>    - Is the check conditional on a user-controlled header, parameter, or query string?
>    - Does the auth gate apply to the route group but the specific route is excluded via an `except` list?
>    - Is there a secondary unauthenticated path to the same function (e.g., an internal API alias)?
>    - Does the middleware apply only to some environments (e.g., skipped in test mode)?
>
> 4. **Privilege identification**:
>    - Does the endpoint path suggest it is admin/privileged (`/admin/`, `/manage/`, `/internal/`)?
>    - Does the operation affect other users' data, system configuration, or aggregate records?
>    - If yes to either, a role/permission check should be present
>
> 5. **Authentication endpoint protections** — for login, forgot-password, and password-reset endpoints:
>    - Is there stricter rate limiting or account lockout on this endpoint compared to general API routes?
>    - Is there a CAPTCHA or human-verification challenge after repeated failures?
>    - Are weak passwords accepted (no length/complexity/breach checks)?
>    - Classify as Vulnerable if credential stuffing or brute force is possible without effective mitigation.
>
> 6. **Sensitive-operation re-authentication** — for email change, password change, 2FA/OTP update, API key regeneration:
>    - Does the handler require the current password, MFA code, or a step-up token before making the change?
>    - Classify as Vulnerable if a stolen session token alone is sufficient to change ownership/security settings.
>
> 7. **Token authenticity checks** — for token verification middleware or handlers:
>    - Are unsigned JWTs (`{"alg":"none"}`) rejected?
>    - Are `exp`, `nbf`, `iss`, `aud` claims validated, and is the signature verified?
>    - Is the signing/encryption key strong and not a default/weak value?
>    - Classify as Vulnerable if any of these checks are missing or weak.
>
> 8. **Microservice-to-microservice authentication** — for internal/service endpoints and clients:
>    - Does the service endpoint require caller authentication, or can any internal caller invoke it?
>    - Are service tokens static, hardcoded, predictable, or shared across services/environments?
>    - Are service accounts scoped to least privilege and are rotated regularly?
>    - Classify as Vulnerable if services trust each other implicitly or use weak/static credentials.
>
> **Classification**:
> - **Vulnerable**: No authentication required; authenticated but role check is entirely absent on a privileged endpoint; authentication endpoints lack brute-force/lockout/CAPTCHA protection or weak-password checks; sensitive operations lack re-authentication; token verification accepts unsafe tokens; service endpoints trust any internal caller or use weak/static credentials.
> - **Likely Vulnerable**: Auth and/or role check exists but appears incomplete, bypassable, or misapplied (e.g., wrong role, wrong HTTP method, conditional skip); anti-brute-force or re-auth controls are present but weak or easily bypassed; token validation is partial; service tokens are long-lived or broadly scoped.
> - **Not Vulnerable**: Proper authentication, role/permission, anti-brute-force, re-authentication, token authenticity, and service-to-service checks are in place.
> - **Needs Manual Review**: Cannot determine with confidence (e.g., complex middleware chain, dynamic role loading, authorization delegated to a service layer, rate limiting enforced outside the codebase).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/10_batch_[N].md`:
>
> ```markdown
> # Missing Auth Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path`
> - **Issue**: [Missing authentication / Missing role check for privileged action]
> - **Impact**: [What an unauthenticated or low-privilege attacker can do]
> - **Proof**: [Show the route definition and handler — highlight the missing check]
> - **Remediation**: [Specific fix — add auth middleware, add role decorator, etc.]
> - **Dynamic Test**:
>   ```
>   [curl command or step-by-step to confirm on the live app.
>    For missing auth: show the request with NO token succeeding.
>    For missing role: show the request with a regular user token succeeding on an admin endpoint.
>    Use placeholders like <REGULAR_USER_TOKEN>, <ADMIN_ENDPOINT>.]
>   ```
>
> ### [LIKELY VULNERABLE] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path`
> - **Issue**: [What's incomplete about the check]
> - **Concern**: [Why this might still be exploitable]
> - **Proof**: [Show the code path with the weak/partial check]
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [curl command or step-by-step instructions to confirm this finding on the live app.]
>   ```
>
> ### [NOT VULNERABLE] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path`
> - **Protection**: [How it's protected — auth middleware + role decorator / @PreAuthorize / Gate, etc.]
>
> ### [NEEDS MANUAL REVIEW] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path`
> - **Uncertainty**: [Why automated analysis couldn't determine the status]
> - **Suggestion**: [What to look at manually]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/10_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/10_missingauth.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/10_batch_1.md`, `{{ REPORTS_ROOT }}/10_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/10_missingauth.md` using this format:

```markdown
# Missing Auth/Authz Analysis Results: [Project Name]

## Executive Summary
- Endpoints analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/10_missingauth.md`, **delete all intermediate files**: `{{ REPORTS_ROOT }}/10_recon.md` and `{{ REPORTS_ROOT }}/10_batch_*.md`.

---

## Important Reminders

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 endpoints per subagent**. If there are 1–3 endpoints total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned endpoints' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- Focus on **vertical privilege escalation** (user → admin) and **unauthenticated access**. Horizontal escalation (user A → user B's resource) is covered by the IDOR skill.
- Authentication (you are who you say you are) and authorization (you are allowed to do this) are separate concerns — check both.
- Middleware order matters: a middleware registered after the route handler will NOT protect the route.
- A missing auth or role check on one HTTP method (e.g., DELETE) is a full vulnerability even if GET is protected.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Pay attention to route grouping: a `use('/admin', adminRouter)` pattern protects all routes in `adminRouter`, but routes mounted outside that group are not protected.
- Authentication endpoint protections (rate limiting, lockout, CAPTCHA, weak-password checks), sensitive-operation re-authentication, token authenticity (`alg: none`, expired/weakly signed tokens), and microservice-to-microservice authentication are all in scope for this skill.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/10_recon.md` and all `{{ REPORTS_ROOT }}/10_batch_*.md` files after the final `{{ REPORTS_ROOT }}/10_missingauth.md` is written.

## References

- OWASP API Security Top 10 2023 — [API2:2023 Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/) and [API5:2023 Broken Function Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/).
- OWASP [Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html).
- OWASP [Access Control Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Access_Control_Cheat_Sheet.html).
- OWASP [Key Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html).
- OWASP [Credential Stuffing](https://owasp.org/www-community/attacks/Credential_stuffing).
- OWASP [Forced Browsing](https://owasp.org/www-community/attacks/Forced_browsing).
- OWASP [Access Control](https://owasp.org/www-community/Access_Control).
- CWE-287: Improper Authentication — <https://cwe.mitre.org/data/definitions/287.html>
- CWE-306: Missing Authentication for Critical Function — <https://cwe.mitre.org/data/definitions/306.html>
- CWE-307: Improper Restriction of Excessive Authentication Attempts — <https://cwe.mitre.org/data/definitions/307.html>
- CWE-204: Observable Response Discrepancy — <https://cwe.mitre.org/data/definitions/204.html>
- CWE-798: Use of Hard-coded Credentials — <https://cwe.mitre.org/data/definitions/798.html>
- CWE-862: Missing Authorization — <https://cwe.mitre.org/data/definitions/862.html>
- CWE-285: Improper Authorization — <https://cwe.mitre.org/data/definitions/285.html>
- CWE-352: Cross-Site Request Forgery (CSRF) — <https://cwe.mitre.org/data/definitions/352.html>
- CWE-384: Session Fixation — <https://cwe.mitre.org/data/definitions/384.html>
- CWE-521: Weak Password Requirements — <https://cwe.mitre.org/data/definitions/521.html>
- CWE-522: Insufficiently Protected Credentials — <https://cwe.mitre.org/data/definitions/522.html>

## Subagent Constraints

**Do not modify project source code.** Subagents running this skill are authorized only to read code, analyze it, and write findings to the designated report files under `{{ REPORTS_ROOT }}`. They must **not** apply patches, edit source files, run `git commit`, or change configuration files in the target repository. All remediation guidance must be written into the report; any code examples shown are illustrative only.

