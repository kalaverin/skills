# Unrestricted Resource Consumption Detection

[ref: #resourceconsumption-detection]

You are performing a focused security assessment to find **API4:2023 Unrestricted Resource Consumption** vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **recon** (find endpoints and functions that lack resource limits), **batched verify** (confirm missing or bypassable limits in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the architecture skill first if it doesn't.

---

## API4:2023 Unrestricted Resource Consumption

An API is vulnerable when it fails to enforce limits on the resources a single client request can consume. Satisfying API requests requires network bandwidth, CPU, memory, storage, file descriptors, processes, and sometimes paid third-party API calls. Without limits, one attacker can exhaust resources, drive up cost, or cause denial of service.

An API is vulnerable if at least one of the following is **missing, misconfigured, or bypassable**:

- Per-endpoint rate limiting (by user, IP, or API key)
- Maximum request body / payload size
- Maximum upload file size
- Maximum string length and array element count for incoming parameters
- Maximum number of records returned per page
- Execution timeout, maximum memory, CPU, file descriptors, processes
- Limits on expensive operations (OTP validation, password reset, file thumbnail generation)
- Spending limits or billing alerts for third-party APIs (SMS, email, biometrics, AI, cloud storage)
- GraphQL query complexity limits and batching/aliasing controls

### What Unrestricted Resource Consumption IS

- Calling an expensive endpoint in a loop because there is no rate limit
- Requesting `?per_page=999999` and the server returns all rows
- Uploading a 10 GB file when no size limit is enforced
- POSTing a JSON array with millions of elements
- GraphQL batching many expensive mutations into a single HTTP request
- Triggering thousands of paid SMS/email/third-party API calls
- Invoking a slow report generation endpoint without timeout or concurrency limit
- Forcing catastrophic regex backtracking, XML entity expansion, or deserialization bombs on attacker-controlled input

### What Unrestricted Resource Consumption is Not

Do not flag these as resource consumption issues:

- **Normal high-traffic design**: an endpoint that is intentionally allowed to serve many requests with rate limiting in place
- **Missing authentication**: unauthenticated access is a different risk class
- **Business logic flaws**: changing `price=0` is mass assignment / business logic, not resource consumption
- **SQL injection**: an ID used to cause a slow query is SQLi, not this class

### Edge-Case Resource-Exhaustion Patterns

In addition to the common cases above, check for these auxiliary single-request exhaustion vectors. Flag them as `[LIKELY VULNERABLE]` when the matching pattern exists and no compensating control is present.

| Pattern | How it exhausts resources | Detection signal |
| --- | --- | --- |
| **ReDoS** | Catastrophic backtracking in a regular expression driven by attacker input. | Regex with nested quantifiers (`(a+)+`, `(.*)*`), user input passed to `re.match` / `RegExp` / `Pattern.compile`. |
| **XML entity expansion / billion laughs** | Malicious XML expands internal entities exponentially, consuming memory. | XML parsers without `disallow-doctype-decl`, no `entityExpansionLimit`, or DTD processing enabled on untrusted input. |
| **Deserialization bombs** | Tiny serialized payloads expand into huge in-memory object graphs. | Native deserialization of untrusted data (Java `ObjectInputStream`, Python `pickle`, PHP/Ruby `unserialize`, Node `vm`/`eval` of serialized data). |
| **JSON depth / breadth bombs** | Deeply nested or extremely wide JSON objects exhaust parser stack/heap or downstream allocators. | Missing `max_depth` / `max_size` on JSON parsers; unbounded array lengths accepted from the client. |
| **Slowloris / HTTP-layer DoS** | Slow, partial HTTP requests hold connections open indefinitely. | Server config missing request/header/body timeouts; unlimited keep-alive; no reverse-proxy connection limits. |
| **Uncontrolled queue growth** | Producer/consumer imbalance fills a queue without backpressure. | Message-queue depth unmonitored; no maximum queue length or dead-letter queue. |
| **Fork / spawn bombs** | Untrusted input triggers unbounded process creation. | `os.system`, `subprocess`, `Runtime.exec`, shell interpolations inside loops without limits. |
| **Cache-based memory leaks** | Unbounded cache keys or TTL eventually exhaust memory. | In-memory cache without eviction policy, max size, or entry expiration. |

### Limits That Prevent Resource Consumption

When you see these patterns, the endpoint or function is likely **not vulnerable**:

**1. Framework-level body/payload limits**
```python
# Django
DATA_UPLOAD_MAX_MEMORY_SIZE = 2_621_440  # 2.5 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 2_621_440
```
```javascript
// Express
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ limit: '1mb', extended: true }));
```
```java
// Spring Boot
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB
```

**2. Rate limiting / throttling**
```python
# Flask-Limiter
@limiter.limit("10/minute")
def reset_password(request): ...
```
```javascript
// Express with express-rate-limit
const limiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 100 });
app.use('/api/', limiter);
```
```java
// Spring Bucket4j
@RateLimiting(name = "api", ...)
public ResponseEntity<?> upload(...) { ... }
```

**3. Pagination / result limits**
```python
# Django REST framework pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100
```
```javascript
// Prisma
prisma.user.findMany({ take: Math.min(req.query.limit, 100) });
```

**4. Upload size / processing limits**
```python
# Flask
if len(file.read()) > MAX_SIZE:
    raise RequestEntityTooLarge()
```

**5. Container / serverless resource limits**
```yaml
# Kubernetes
resources:
  limits:
    memory: "512Mi"
    cpu: "500m"
```

**6. Third-party spending limits / alerts**
- AWS billing alerts, Twilio spend caps, SendGrid rate limits, etc.

**7. Circuit breakers and backpressure**
- Timeouts, bulkheads, and circuit-breaker libraries (e.g., Resilience4j, Polly, Hystrix, Sentinel) that fail fast when downstream resources are saturated.
- Explicit queue max-length and consumer backpressure to prevent unbounded queue growth.

### Anti-Patterns

**A. Relying only on client-side limits**
```javascript
// INSUFFICIENT: client can bypass maxlength
<input type="file" maxSize="5MB">
```

**B. Rate limiting only by IP on an authenticated endpoint**
Authenticated users can still abuse endpoints from a single session.

**C. Checking size after loading entire payload into memory**
```python
# INSUFFICIENT: memory already consumed
data = request.body.read()
if len(data) > MAX:
    raise ...
```

**D. Allowing GraphQL batching / aliases without complexity analysis**
```json
[
  { "query": "mutation { uploadPic(...) { url } }" },
  { "query": "mutation { uploadPic(...) { url } }" }
]
```

---

## Vulnerable vs. Secure Examples

### Python — Django

```python
# VULNERABLE: no rate limit, reads unbounded per_page
def list_orders(request):
    per_page = int(request.GET.get('per_page', 20))
    orders = Order.objects.all()[:per_page]
    return JsonResponse({'orders': list(orders)})

# SECURE: enforce hard maximum
def list_orders(request):
    per_page = min(int(request.GET.get('per_page', 20)), 100)
    orders = Order.objects.all()[:per_page]
    return JsonResponse({'orders': list(orders)})
```

```python
# VULNERABLE: no file size limit
def upload_avatar(request):
    file = request.FILES['avatar']
    path = default_storage.save(file.name, file)
    return JsonResponse({'path': path})

# SECURE: validate size before processing
def upload_avatar(request):
    file = request.FILES['avatar']
    if file.size > 5 * 1024 * 1024:
        return JsonResponse({'error': 'File too large'}, status=413)
    path = default_storage.save(file.name, file)
    return JsonResponse({'path': path})
```

### Python — Flask

```python
# VULNERABLE: no limit on body size or array length
@app.route('/api/bulk-import', methods=['POST'])
def bulk_import():
    items = request.get_json()  # could be millions of objects
    for item in items:
        process(item)
    return jsonify({'ok': True})

# SECURE: validate length and use streaming
@app.route('/api/bulk-import', methods=['POST'])
@limiter.limit("5/minute")
def bulk_import():
    items = request.get_json()
    if not isinstance(items, list) or len(items) > 1000:
        return jsonify({'error': 'Too many items'}), 400
    for item in items:
        process(item)
    return jsonify({'ok': True})
```

### Node.js — Express

```javascript
// VULNERABLE: no body limit, no rate limit
app.post('/api/feedback', async (req, res) => {
  const { message } = req.body;          // body can be huge
  await sendEmail(req.user.email, message); // paid third-party call
  res.json({ ok: true });
});

// SECURE: body limit + rate limit + spending alert
const feedbackLimiter = rateLimit({ windowMs: 60 * 60 * 1000, max: 3 });
app.post('/api/feedback', feedbackLimiter, express.json({ limit: '10kb' }), async (req, res) => {
  const { message } = req.body;
  if (message.length > 500) return res.status(400).json({ error: 'Too long' });
  await sendEmail(req.user.email, message);
  res.json({ ok: true });
});
```

```javascript
// VULNERABLE: pagination unbounded
app.get('/api/events', async (req, res) => {
  const limit = parseInt(req.query.limit, 10) || 20;
  const events = await Event.findAll({ limit });
  res.json(events);
});

// SECURE: enforce max page size
app.get('/api/events', async (req, res) => {
  const limit = Math.min(parseInt(req.query.limit, 10) || 20, 100);
  const events = await Event.findAll({ limit });
  res.json(events);
});
```

### Java — Spring Boot

```java
// VULNERABLE: no timeout, unbounded request body
@PostMapping("/api/reports")
public ResponseEntity<?> generateReport(@RequestBody List<Long> ids) {
    List<Report> reports = service.generate(ids); // ids can be huge
    return ResponseEntity.ok(reports);
}

// SECURE: validate size, set timeout, rate limit
@PostMapping("/api/reports")
@RateLimiting(name = "reports")
public ResponseEntity<?> generateReport(@RequestBody @Size(max = 100) List<Long> ids) {
    List<Report> reports = service.generate(ids, Duration.ofSeconds(30));
    return ResponseEntity.ok(reports);
}
```

### Go

```go
// VULNERABLE: no read timeout, unbounded body
func uploadHandler(w http.ResponseWriter, r *http.Request) {
    r.ParseMultipartForm(0) // 0 = unlimited
    file, _, _ := r.FormFile("file")
    defer file.Close()
    io.Copy(os.Create("/tmp/upload"), file)
    w.WriteHeader(200)
}

// SECURE: limit memory/file size and set timeouts
func uploadHandler(w http.ResponseWriter, r *http.Request) {
    r.Body = http.MaxBytesReader(w, r.Body, 10*1024*1024)
    r.ParseMultipartForm(10 << 20) // 10 MB
    file, _, err := r.FormFile("file")
    if err != nil { http.Error(w, err.Error(), 400); return }
    defer file.Close()
    io.Copy(os.Create("/tmp/upload"), file)
    w.WriteHeader(200)
}
```

### GraphQL

```javascript
// VULNERABLE: batching bypasses per-operation rate limit
const resolvers = {
  Mutation: {
    uploadPic: async (_, { name, base64_pic }) => {
      await generateThumbnails(base64_pic); // memory-heavy
      return { url: `/uploads/${name}` };
    },
  },
};

// SECURE: complexity limit + batch limit + operation rate limit
const schema = makeExecutableSchema({ typeDefs, resolvers });
const complexity = createComplexityLimitRule(1000);
const server = new ApolloServer({
  schema,
  validationRules: [complexity],
  plugins: [ApolloServerPluginUsageReporting()],
});
```

---

## Dynamic-Test Payload Examples

Use these payloads and curl commands as concrete proof-of-concept templates in batch findings. Replace `<HOST>`, `<TOKEN>`, and placeholder values with project-specific data.

### Unbounded pagination

```bash
curl -s -o /dev/null -w "%{http_code} %{size_download} %{time_total}\n" \
  "https://<HOST>/api/items?limit=9999999&offset=0" \
  -H "Authorization: Bearer <TOKEN>"
```
Look for HTTP 200 with a very large response body or response time spike.

### ReDoS probe

```bash
# Probe an input field that is validated with a regex containing nested quantifiers.
EXPONENT=5000
curl -s -o /dev/null -w "%{http_code} %{time_total}\n" \
  "https://<HOST>/api/validate?email=a@%s.com" \
  --compressed \
  -H "Authorization: Bearer <TOKEN>"
```
Watch for response times that grow exponentially with input length.

### GraphQL batching

```bash
# Create a JSON array file with many identical uploadPic mutations, then POST it.
cat > /tmp/batch.json <<'EOF'
[
  {"query": "mutation { uploadPic(name: \"p1\", base64_pic: \"...\") { url } }"},
  {"query": "mutation { uploadPic(name: \"p2\", base64_pic: \"...\") { url } }"}
]
EOF
# Repeat the inner object to reach 100+ operations, then:
curl -s -o /dev/null -w "%{http_code} %{time_total}\n" \
  -X POST "https://<HOST>/graphql" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d @/tmp/batch.json
```

### JSON depth bomb

```bash
python3 -c '
import json, sys
d = {}
cur = d
for _ in range(10000):
    cur["a"] = {}
    cur = cur["a"]
print(json.dumps(d))
' > /tmp/deep.json

curl -s -o /dev/null -w "%{http_code} %{time_total}\n" \
  -X POST "https://<HOST>/api/import" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <TOKEN>" \
  -d @/tmp/deep.json
```

### Large file upload

```bash
dd if=/dev/zero of=/tmp/bigupload.bin bs=1M count=110

curl -s -o /dev/null -w "%{http_code} %{time_total}\n" \
  -X POST "https://<HOST>/api/upload" \
  -H "Authorization: Bearer <TOKEN>" \
  -F "file=@/tmp/bigupload.bin" \
  -F "name=bigupload"
```
Expect HTTP 413 / "Payload Too Large" if size limits exist. HTTP 200 with slow processing indicates a missing limit.

### SMS / email cost amplification

```bash
# Forgot-password SMS abuse
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST "https://<HOST>/api/forgot-password" \
    -H "Content-Type: application/json" \
    -d '{"phone_number": "+15550000001"}'
done

# Feedback / email abuse
for i in $(seq 1 50); do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST "https://<HOST>/api/contact" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer <TOKEN>" \
    -d '{"message": "spam", "to": "attacker@example.com"}'
done
```
Look for HTTP 429 responses or per-user throttling. Success for all 50 requests without rate limiting indicates vulnerability.

### Mandatory OWASP API4:2023 dynamic-test patterns

When the matching endpoint or integration exists in the project, treat these three OWASP scenarios as mandatory dynamic-test patterns. Flag the absence of the listed controls as `[LIKELY VULNERABLE]`.

| Scenario | Attack flow | Required controls |
| --- | --- | --- |
| **SMS forgot-password abuse** | Replay `POST /initiate_forgot_password` tens of thousands of times; backend calls third-party SMS API at a per-message cost. | Per-user rate limiting on the initiating endpoint; spending cap or billing alert on the SMS provider; per-phone-number throttling. |
| **GraphQL profile-picture batch upload** | Batch `uploadPic` mutations in a single HTTP request to exhaust memory during thumbnail generation, bypassing per-request rate limits. | GraphQL operation/batch count limits; memory/CPU/process limits on image-processing workers; payload-size and per-operation caps. |
| **Cache-bypass cost spike** | Request an object larger than the cache threshold so all clients pull from origin, or request uncached large objects repeatedly. | Cache size/bypass policies; maximum object size enforcement; cloud spend alerts and maximum cost allowance. |

---

## Prevention Guidance

- **Apply per-endpoint rate limits** tuned to business needs; expensive endpoints need stricter limits than read-only listing endpoints.
- **Enforce maximum payload sizes** at the reverse proxy, framework, and application layers.
- **Limit file uploads** by size, type, and resolution; process images asynchronously with resource caps.
- **Validate array/string lengths and pagination parameters** on every request.
- **Set execution timeouts, memory limits, CPU limits, file descriptor limits, and process limits** via containers, serverless functions, or language runtime settings.
- **Throttle expensive user-triggered operations** (password reset SMS, OTP validation, email sending) per user.
- **Configure spending limits and billing alerts** for every third-party API integration.
- **Analyze GraphQL query complexity** and disable or limit batching/aliasing when it enables bypass.
- **Add circuit breakers and backpressure**: fail fast when downstream resources are saturated, cap queue lengths, and shed load before exhaustion occurs.

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Subagent Constraints (Read-Only)

All subagents used in this skill are **read-only security analysts**:

- **Do not modify project source code, configuration files, environment variables, infrastructure manifests, or database state.**
- **Do not run exploits against production systems.**
- Subagents may only write findings to the designated report files (`{{ REPORTS_ROOT }}/17_recon.md`, `{{ REPORTS_ROOT }}/17_batch_*.md`).
- If a subagent needs to test a running service, it must use safe, non-destructive requests and must stop immediately if it observes service degradation.

### Phase 1: Recon — Find Resource-Consumption Candidates

Launch a subagent with the following instructions:

> **Goal**: Find every endpoint, controller action, handler, background job, or function that consumes significant resources or lacks explicit consumption limits. Write results to `{{ REPORTS_ROOT }}/17_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, frameworks, route definitions, data access patterns, third-party integrations, and GraphQL schema.
>
> **What to search for**:
>
> 1. **Route definitions and handlers** that:
>    - Accept query parameters controlling result size: `limit`, `per_page`, `page_size`, `count`, `top`
>    - Accept arrays or bulk input in the request body
>    - Accept file uploads (`multipart/form-data`, `FILES`, `FormFile`, `MultipartFile`)
>    - Trigger expensive operations: report generation, image/video processing, bulk import/export, password reset, OTP, SMS/email sending
>    - Call third-party APIs that incur cost (SMS, email, AI, biometrics, cloud storage, payment)
>
> 2. **Framework configuration** for body/payload limits, rate limiting, and upload size limits:
>    - Missing or very large `DATA_UPLOAD_MAX_MEMORY_SIZE`, `express.json({ limit: ... })`, `spring.servlet.multipart.*`, `http.MaxBytesReader`, nginx `client_max_body_size`
>
> 3. **GraphQL endpoints**:
>    - Batching / aliasing support without complexity limits
>    - Expensive resolvers (image processing, aggregation, nested lists)
>
> 4. **Background jobs / workers** triggered by API calls without concurrency or timeout limits.
>
> 5. **Container / serverless manifests** for missing memory/CPU/time limits.
>
> 6. **Edge-case resource-exhaustion patterns**:
>    - Regex on user input with nested quantifiers (ReDoS)
>    - XML parsers with DTD/entity expansion enabled
>    - Native deserialization of untrusted data
>    - JSON parsers without depth/size limits
>    - Missing request/header timeouts (slowloris)
>    - Unbounded queues, caches, or process spawning
>
> **What to ignore**:
> - Static asset serving
> - Health checks and telemetry endpoints that are intentionally lightweight
> - Endpoints already protected by clearly documented global rate limiting and size limits (still note the limit in the candidate)
>
> **Output format** — write to `{{ REPORTS_ROOT }}/17_recon.md`:
>
> ```markdown
> # Resource Consumption Recon: [Project Name]
>
> ## Summary
> Found [N] candidate endpoints/functions with potential missing or bypassable resource limits.
>
> ## Candidates
>
> ### 1. [Descriptive name]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint/Function**: `METHOD /path` or `functionName(...)`
> - **Resource type**: [rate limit / body size / file upload / pagination / CPU/memory / third-party cost / GraphQL batching / ReDoS / XML expansion / deserialization / JSON bomb / queue growth / fork bomb / cache leak]
> - **Limit status**: [missing / misconfigured / bypassable]
> - **Code snippet**:
>   ```
>   [relevant code]
>   ```
>
> [Repeat for each candidate]
> ```

### Phase 2: Verify — Confirm Missing or Bypassable Limits (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/17_recon.md` and split the candidates into **batches of up to 3 candidates each**. Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned candidates and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/17_recon.md` and count the numbered candidate sections (### 1., ### 2., etc.).
2. Divide them into batches of up to 3. For example, 8 candidates → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those candidate sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned candidates.
5. Each subagent writes to `{{ REPORTS_ROOT }}/17_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: Verify the following Unrestricted Resource Consumption candidates and determine whether adequate limits are in place. Write results to `{{ REPORTS_ROOT }}/17_batch_[N].md`.
>
> **Subagent constraint**: This is a read-only analysis. Do not modify source code, configuration, or environment. Do not run destructive tests against production.
>
> **Your assigned candidates** (from the recon phase):
>
> [Paste the full text of the assigned candidate sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand the framework, middleware, rate-limiting, and third-party integration patterns.
>
> **Unrestricted Resource Consumption Reference — What to look for**:
>
> API4:2023 occurs when an API fails to limit the resources a single request can consume: CPU, memory, execution time, file descriptors, upload size, array/string length, pagination size, or paid third-party calls. Focus on limits that are **missing, misconfigured, or bypassable**.
>
> **What this is NOT** — do not flag these as resource consumption:
> - **Missing authentication**: that's a different risk class
> - **Business logic flaws**: changing prices or roles is mass assignment / business logic
> - **SQL injection**: a huge `id` list used to cause a slow query is SQLi
>
> **Limits that PREVENT this vulnerability** — if you see these, the candidate is likely safe:
> 1. **Framework body/payload limits** enforced at the server or reverse-proxy layer
> 2. **Rate limiting / throttling** applied to the specific endpoint (not only global IP limits)
> 3. **Hard pagination / array / string limits** validated server-side
> 4. **Upload size / type / resolution limits** enforced before processing
> 5. **Container / serverless resource limits** (memory, CPU, timeout, file descriptors)
> 6. **Third-party spending limits or billing alerts**
> 7. **GraphQL complexity analysis and batching controls**
> 8. **Circuit breakers and backpressure** that prevent cascade exhaustion
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **For each candidate, check**:
>
> 1. **Is a per-endpoint or per-user rate limit enforced?**
>    - Is the limit applied to the specific function/endpoint?
>    - Can it be bypassed by batching, GraphQL aliases, or changing headers?
>
> 2. **Are payload/body sizes bounded?**
>    - Is there a framework-level maximum request size?
>    - Does the code validate string/array length before processing?
>
> 3. **Are pagination / result-size parameters capped?**
>    - Is `limit` / `per_page` bounded by a server-side maximum?
>
> 4. **Are file uploads bounded?**
>    - Is there a maximum file size, type, and resolution check?
>    - Is size checked before loading the whole file into memory?
>
> 5. **Are expensive operations throttled or queued?**
>    - Password reset, OTP, report generation, image/video processing, bulk imports
>
> 6. **Are third-party API calls protected by spending limits or rate caps?**
>    - SMS, email, AI, biometrics, cloud storage, payment APIs
>
> 7. **For GraphQL, are query complexity and batching limited?**
>
> 8. **Edge cases to check**:
>    - Limits exist but are set extremely high (e.g., 1 GB body limit)
>    - Limits are enforced in one middleware but bypassable for a specific route
>    - Rate limit is per-IP while authentication is required
>    - Array length checked after deserialization already consumed memory
>    - Regular expressions with catastrophic backtracking on user input
>    - XML parsers with DTD/entity expansion enabled on untrusted input
>    - Native deserialization of untrusted data
>    - JSON depth/breadth bombs
>    - Missing request/header timeouts (slowloris)
>    - Unbounded queue, cache, or process growth
>
> 9. **Mandatory OWASP API4:2023 patterns** — if the project has a matching endpoint/integration, verify the controls below. Flag as `[LIKELY VULNERABLE]` if any control is missing:
>    - **SMS forgot-password abuse**: per-user rate limit on the initiating endpoint; SMS provider spending cap or billing alert; per-phone-number throttling.
>    - **GraphQL profile-picture batch upload**: GraphQL operation/batch count limits; memory/CPU/process limits on image-processing workers; payload-size and per-operation caps.
>    - **Cache-bypass cost spike**: cache size/bypass policies; maximum object size enforcement; cloud spend alerts and maximum cost allowance.
>
> **Classification**:
> - **Vulnerable**: No effective limit is enforced; a single client can exhaust resources or incur cost.
> - **Likely Vulnerable**: A limit exists but is misconfigured, conditional, or bypassable.
> - **Not Vulnerable**: Proper server-side limits are in place.
> - **Needs Manual Review**: Cannot determine with confidence (e.g., limits configured outside the codebase, complex gateway rules).
>
> **Dynamic Test guidance**:
> - For each confirmed or likely-vulnerable finding, include a concrete `curl` command or step-by-step instructions using the examples in the reference (unbounded pagination, ReDoS probe, GraphQL batching, JSON depth bomb, large file upload, SMS/email amplification).
> - Use placeholder tokens like `<HOST>`, `<TOKEN>`, `<LARGE_PAYLOAD>`.
> - State what response code, timing, or size indicates the vulnerability.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/17_batch_[N].md`:
>
> ```markdown
> # Resource Consumption Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Endpoint/Function name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint/Function**: `METHOD /path` or `functionName(...)`
> - **Issue**: [Clear description of the missing or bypassable limit]
> - **Impact**: [What an attacker can do — DoS, cost spike, memory exhaustion, etc.]
> - **Proof**: [Show the code path and explain why no effective limit exists]
> - **Remediation**: [Specific fix — add rate limit, cap limit, validate size, etc.]
> - **Dynamic Test**:
>   ```
>   [curl command or step-by-step instructions to confirm this finding on the live app.
>    Include the exact endpoint, HTTP method, headers, and what to look for in the response.
>    Use placeholder tokens like <TOKEN> and <LARGE_PAYLOAD>.]
>   ```
>
> ### [LIKELY VULNERABLE] Endpoint/Function name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint/Function**: `METHOD /path` or `functionName(...)`
> - **Issue**: [What's incomplete or bypassable about the limit]
> - **Impact**: [Why this might still be exploitable]
> - **Proof**: [Show the code path with the weak/partial limit]
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [curl command or step-by-step instructions]
>   ```
>
> ### [NOT VULNERABLE] Endpoint/Function name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint/Function**: `METHOD /path` or `functionName(...)`
> - **Issue**: Resource limits are enforced.
> - **Impact**: Not exploitable under current configuration.
> - **Proof**: [Show the code or config enforcing the limit]
> - **Remediation**: None required; maintain existing controls.
> - **Dynamic Test**: N/A
>
> ### [NEEDS MANUAL REVIEW] Endpoint/Function name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint/Function**: `METHOD /path` or `functionName(...)`
> - **Issue**: [Why automated analysis couldn't determine the status]
> - **Impact**: [Potential risk if limits are missing]
> - **Proof**: [What evidence is missing]
> - **Remediation**: [What to check manually]
> - **Dynamic Test**:
>   ```
>   [Suggested manual verification steps]
>   ```
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/17_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/17_resourceconsumption.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/17_batch_1.md`, `{{ REPORTS_ROOT }}/17_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/17_resourceconsumption.md` using this format:

```markdown
# Unrestricted Resource Consumption Results: [Project Name]

## Executive Summary
- Candidates analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]

## Prevention Guidance

[Summarize the top prevention actions for this project based on the findings.]
```

5. After writing `{{ REPORTS_ROOT }}/17_resourceconsumption.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/17_batch_*.md`).

---

## OWASP API Security Top 10 2023 Mapping

This detection reference covers **API4:2023 Unrestricted Resource Consumption** from the OWASP API Security Top 10 2023 source file `0xa4-unrestricted-resource-consumption.md`.

- OWASP API Security Top 10 2023 — **API4:2023 Unrestricted Resource Consumption**: https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/
- OWASP Web Service Security Cheat Sheet — **Availability**: https://cheatsheetseries.owasp.org/cheatsheets/Web_Service_Security_Cheat_Sheet.html#availability
- OWASP GraphQL Cheat Sheet — **DoS Prevention** and **Mitigating Batching Attacks**: https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html
- [CWE-770: Allocation of Resources Without Limits or Throttling](https://cwe.mitre.org/data/definitions/770.html)
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html)
- [CWE-799: Improper Control of Interaction Frequency](https://cwe.mitre.org/data/definitions/799.html)
- [CWE-841: Improper Enforcement of Behavioral Workflow](https://cwe.mitre.org/data/definitions/841.html)
- [CWE-834: Excessive Iteration](https://cwe.mitre.org/data/definitions/834.html)
- [CWE-405: Asymmetric Resource Consumption (Amplification)](https://cwe.mitre.org/data/definitions/405.html)
- NIST SP 800-204 — *Security Strategies for Microservices-based Application Systems*: https://csrc.nist.gov/publications/detail/sp/800-204/final

---

## Important Reminders

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 candidates per subagent**. If there are 1-3 candidates total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned candidates' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- Subagents are **read-only**. They must not modify source code, configuration, environment variables, infrastructure manifests, or database state.
- Focus on **single-request resource exhaustion** and **cost amplification**. Horizontal authorization (IDOR) is a different skill.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Trace the full code path: route → middleware → controller → service → data access → third-party API. Limits can be enforced at any layer.
- Pay attention to framework defaults. Some frameworks have no body-size limit by default; others have conservative defaults that may be overridden.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/17_recon.md` and all `{{ REPORTS_ROOT }}/17_batch_*.md` files after the final `{{ REPORTS_ROOT }}/17_resourceconsumption.md` is written.
