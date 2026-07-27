---
subject: "Unrestricted resource consumption detection reference for SAST subagents; shared-protocol execution parameters, `API4:2023` definition with IS/IS-NOT boundaries, edge-case exhaustion table incl. LLM and SSE rows, limit patterns plus anti-patterns, per-stack recipes incl. `FastAPI` `SlowAPI` `Resilience4j`, dynamic-test payloads incl. mandatory OWASP scenarios, prevention guidance, OWASP mapping with CWE links, operational reminders."
index:
  - anchor: resourceconsumption-detection
    what: "Focused resource-exhaustion detection role executed through the shared three-stage pipeline (`execution-protocol.md`) — recon for endpoints lacking limits, batched verify, merge — gated on the architecture report."
    problem: "Codebase needs systematic sweep of every endpoint, job, and integration for missing consumption ceilings, yet unstructured hunting overlooks bypassable limits and buries reviewers in noise; detection orchestration, limit inventory, exhaustion sweep, cost amplification, audit rigor, candidate flood, coverage goal, methodical triage."
    use_when: "Resource-consumption scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-stage detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual knowledge is needed, not execution."
    expected: "Confirmed limit findings consolidated into one module report with false positives filtered."
  - anchor: resourceconsumption-api4-2023
    what: "`API4:2023` definition of unrestricted resource consumption with IS/IS-NOT boundaries, edge-case exhaustion table covering ReDoS, XML expansion, deserialization bombs, JSON depth attacks, slowloris, queue growth, fork bombs, cache leaks, LLM overuse, SSE/WebSocket drains, plus limit patterns and anti-patterns."
    problem: "Reviewer cannot tell whether odd behavior counts as consumption abuse without crisp boundaries, so intentional high-traffic design gets flagged while subtle exhaustion vectors slip past; definition scope, boundary rules, inclusion criteria, exclusion list, classification accuracy, edge cases, wallet denial, taxonomy anchor."
    use_when: "Deciding whether observed behavior belongs to this risk class; verifying listed protection patterns exist on the endpoint; checking edge-case vectors like ReDoS or LLM overuse against source code."
    avoid_when: "Auth gaps are the question — route to `10-missingauth.md`; price or role manipulation belongs to `13-businesslogic.md`; SQL injection semantics belong to `02-sqli.md`; pure upload validation depth belongs to `11-fileupload.md`."
    expected: "Behavior classified against `API4:2023` with explicit boundary reasoning; every listed exhaustion vector either confirmed or excluded."
  - anchor: resourceconsumption-vulnerable-vs-secure-examples
    what: "Per-stack vulnerable/secure recipe pairs — Django, Flask, `FastAPI` with `SlowAPI`, Express, Spring Boot with `Resilience4j`, Go, GraphQL — covering page-size ceilings, chunked upload validation, payload limits, throttling, and complexity rules."
    problem: "Enforcement idioms differ per framework, and generic consumption rules miss stack-specific caps, streaming checks, and middleware quirks that decide exploitability; stack recipes, secure idioms, precise detection, pattern matching, framework diversity, middleware defaults, handler review, exploit signal."
    use_when: "Target project uses one of the covered stacks; reviewing flow-critical handlers where pagination, uploads, or expensive calls occur; verify stage applies the file's per-stack examples when judging candidates."
    avoid_when: "Conceptual boundaries are the question — see the definition card; upload-only validation depth belongs to `11-fileupload.md`; GraphQL injection semantics beyond batching belong to `14-graphql.md`."
    expected: "Stack-specific missing caps flagged; enforced ceilings and streaming checks verified per framework."
  - anchor: resourceconsumption-dynamic-test-payload-examples
    what: "Concrete `curl` command set for proving findings — unbounded pagination, ReDoS probe, GraphQL batching, JSON depth bomb, oversized upload, SMS/email cost amplification — plus the three mandatory OWASP scenario checks."
    problem: "Findings without reproducible proof get disputed by developers, and handcrafted probes vary wildly across reviewers, weakening every reported weakness; dynamic proof, payload templates, reproducible evidence, timing signals, response codes, live confirmation, dispute risk, proof gap."
    use_when: "Confirmed or likely-vulnerable finding needs live-test instructions; batch subagent builds its `Dynamic Test` block; one of the required OWASP patterns matches an existing endpoint."
    avoid_when: "Static review only with no live testing requested; pure upload-validation depth belongs to `11-fileupload.md`; GraphQL injection semantics rather than batching abuse belong to `14-graphql.md`."
    expected: "Every confirmed finding carries executable proof with status, timing, or size indicator to watch."
  - anchor: resourceconsumption-prevention-guidance
    what: "Layered defense checklist: per-endpoint throttling, payload ceilings at every layer, upload caps, length validation, execution timeouts, container quotas, third-party spend alerts, complexity analysis, circuit breakers, backpressure."
    problem: "Remediation advice scattered across guides leaves gaps, and one missed control lets attackers reopen exhaustion or cost abuse after fixes ship; remediation checklist, defense layers, control mapping, gap elimination, hardening steps, closure guarantee, mitigation breadth, fix completeness."
    use_when: "Writing remediation sections of findings; reviewing whether deployed defenses form complete coverage."
    avoid_when: "Detection mechanics are the question — see execution and example cards; price or role manipulation fixes belong to `13-businesslogic.md`."
    expected: "Each finding closes with layered controls that block reopening of the same abuse path."
  - anchor: resourceconsumption-execution
    what: "Domain execution parameters for the shared three-stage protocol: recon catalog of resource-consumption sites, per-candidate verify checklist, classification rubric, and the finding-field set with mandatory dynamic-test payloads."
    problem: "Consumption hunting without precise domain criteria lets recon miss bypassable limits and verify apply generic checklists that overlook stack quirks; criteria ownership, domain parameters, search catalog, checklist precision, detection quality, class specifics."
    use_when: "Dispatching or executing any pipeline stage for this scan; reviewing whether recon and verify criteria cover current resource-consumption vectors."
    avoid_when: "Stage mechanics — batching, gating, merging — belong to `execution-protocol.md`; conceptual definition belongs to the `API4:2023` definition card; only payload templates wanted — see the dynamic-test card."
    expected: "Stage subagents apply exact resource-consumption criteria without inheriting generic templates."
  - anchor: resourceconsumption-owasp-mapping
    what: "Canonical source links for `API4:2023`: OWASP risk page, availability and GraphQL cheat sheets, `CWE-770`, `CWE-400`, `CWE-799`, `CWE-841`, `CWE-834`, `CWE-405`, NIST `SP 800-204`, and `LLM10:2025` unbounded consumption."
    problem: "Reports need correct 2023-era taxonomy and authoritative citations, and mislabeled findings break downstream triage metrics and reader trust; taxonomy mapping, risk routing, citation canon, classification accuracy, weakness identifiers, traceability, tagging discipline, reference integrity."
    use_when: "Tagging findings with OWASP 2023 risks or CWE identifiers; adding authoritative citations to the final report."
    avoid_when: "Recipe or workflow needs route elsewhere — see the definition, examples, and execution cards; this section is follow-up sourcing, not procedure."
    expected: "Findings carry correct `API4:2023` and CWE tagging with primary sources attached."
  - anchor: resourceconsumption-important-reminders
    what: "Closing operational reminders: phase ordering, three-per-batch parallelism, scoped context handoff, read-only discipline, manual-review bias, full code-path tracing, framework-default awareness, intermediate cleanup."
    problem: "Modules close with inconsistent final guidance, letting unverified candidates, weak proof, or leftover files slip into reports and client deliverables; closing rules, quality floor, final reminders, weak evidence, uniform endings, wrap discipline, audit closure, leftover artifacts."
    use_when: "Finalizing the module report; checking phase sequencing and cleanup obligations before closing the scan."
    avoid_when: "Earlier phases are still open — finish those first; sibling-risk routing belongs to `10-missingauth.md`, `13-businesslogic.md`, or `14-graphql.md` cards."
    expected: "Reports close with uniform final rules applied and no leftover intermediates."
---

# Unrestricted Resource Consumption Detection

[ref: #resourceconsumption-detection]

You are performing a focused security assessment to find **API4:2023 Unrestricted Resource Consumption** vulnerabilities in a codebase. This skill uses a three-stage pipeline with subagents: **recon** (find endpoints and functions that lack resource limits), **batched verify** (confirm missing or bypassable limits in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the architecture skill first if it doesn't.

***

## API4:2023 Unrestricted Resource Consumption
[ref: #resourceconsumption-api4-2023]

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
| **LLM/AI unbounded consumption** | Pay-per-token endpoints without per-user quotas enable variable-length input floods and Denial of Wallet; runaway agent loops burn unbounded reasoning/tool-calling iterations. | LLM completion endpoints without per-user quota, `max_tokens`/`max_iterations` caps, or spend alerts. |
| **Long-lived connection exhaustion (SSE/WebSocket)** | Held-open streaming connections accumulate until file descriptors or workers exhaust. | SSE/WebSocket endpoints without connection-duration, concurrency, or idle-timeout limits. |

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
// Spring Boot + Resilience4j
@RateLimiter(name = "api")
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
- Timeouts, bulkheads, and circuit-breaker libraries (e.g., Resilience4j, Polly, Sentinel, Failsafe — Hystrix is legacy/archived) that fail fast when downstream resources are saturated.
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

***

## Vulnerable vs. Secure Examples
[ref: #resourceconsumption-vulnerable-vs-secure-examples]

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

### Python — FastAPI

```python
# VULNERABLE: uncapped pagination, upload saved without size validation
@app.get("/api/items")
def list_items(per_page: int = Query(20)):
    return items[:per_page]  # per_page can be 999999

@app.post("/api/upload")
def upload(file: UploadFile):
    path = save_file(file.file)  # no size check; FastAPI has no built-in body limit
    return {"path": path}

# SECURE: cap pagination, rate limit expensive endpoints, validate upload size in chunks
@app.get("/api/items")
def list_items(per_page: int = Query(20, le=100)):  # or: min(per_page, 100)
    return items[:per_page]

@app.post("/api/expensive")
@limiter.limit("5/minute")  # SlowAPI; returns HTTP 429
def expensive(request: Request):
    ...

@app.post("/api/upload")
def upload(file: UploadFile):
    size = 0
    while chunk := file.file.read(1024 * 1024):  # 1 MB chunks
        size += len(chunk)
        if size > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large")
    file.file.seek(0)
    path = save_file(file.file)
    return {"path": path}
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
@RateLimiter(name = "reports")
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

***

## Dynamic-Test Payload Examples
[ref: #resourceconsumption-dynamic-test-payload-examples]

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

***

## Prevention Guidance
[ref: #resourceconsumption-prevention-guidance]

- **Apply per-endpoint rate limits** tuned to business needs; expensive endpoints need stricter limits than read-only listing endpoints.
- **Enforce maximum payload sizes** at the reverse proxy, framework, and application layers.
- **Limit file uploads** by size, type, and resolution; process images asynchronously with resource caps.
- **Validate array/string lengths and pagination parameters** on every request.
- **Set execution timeouts, memory limits, CPU limits, file descriptor limits, and process limits** via containers, serverless functions, or language runtime settings.
- **Throttle expensive user-triggered operations** (password reset SMS, OTP validation, email sending) per user.
- **Configure spending limits and billing alerts** for every third-party API integration.
- **Analyze GraphQL query complexity** and disable or limit batching/aliasing when it enables bypass.
- **Add circuit breakers and backpressure**: fail fast when downstream resources are saturated, cap queue lengths, and shed load before exhaustion occurs.

***

## Execution
[ref: #resourceconsumption-execution]

This scan runs via the shared three-stage pipeline in `references/execution-protocol.md` (recon+split → per-batch verify → merge, core-dispatched). The domain parameters below plug into its stage contracts. Final artifact: `{{ REPORTS_ROOT }}/17_resourceconsumption.md`; classification family: standard (`[VULNERABLE]` / `[LIKELY VULNERABLE]`).

Dynamic-test safety: do not run exploits against production systems; if a subagent needs to test a running service, it must use safe, non-destructive requests and must stop immediately if it observes service degradation.

### Recon catalog

Search for these resource-consumption sites:

1. **Route definitions and handlers** that:
   - Accept query parameters controlling result size: `limit`, `per_page`, `page_size`, `count`, `top`
   - Accept arrays or bulk input in the request body
   - Accept file uploads (`multipart/form-data`, `FILES`, `FormFile`, `MultipartFile`)
   - Trigger expensive operations: report generation, image/video processing, bulk import/export, password reset, OTP, SMS/email sending
   - Call third-party APIs that incur cost (SMS, email, AI, biometrics, cloud storage, payment)
   - Expose LLM/AI completion endpoints (pay-per-token cost, runaway agent loops)
   - Open long-lived streaming connections (SSE/WebSocket) without duration or concurrency limits

2. **Framework configuration** for body/payload limits, rate limiting, and upload size limits:
   - Missing or very large `DATA_UPLOAD_MAX_MEMORY_SIZE`, `express.json({ limit: ... })`, `spring.servlet.multipart.*`, `http.MaxBytesReader`, nginx `client_max_body_size`

3. **GraphQL endpoints**:
   - Batching / aliasing support without complexity limits
   - Expensive resolvers (image processing, aggregation, nested lists)

4. **Background jobs / workers** triggered by API calls without concurrency or timeout limits.

5. **Container / serverless manifests** for missing memory/CPU/time limits.

6. **Edge-case resource-exhaustion patterns**:
   - Regex on user input with nested quantifiers (ReDoS)
   - XML parsers with DTD/entity expansion enabled
   - Native deserialization of untrusted data
   - JSON parsers without depth/size limits
   - Missing request/header timeouts (slowloris)
   - Unbounded queues, caches, or process spawning

**Recon exclusions** — do not report:

- Static asset serving
- Health checks and telemetry endpoints that are intentionally lightweight
- Endpoints already protected by clearly documented global rate limiting and size limits (still note the limit in the candidate)

### Verify checklist

For each candidate, check:

1. **Is a per-endpoint or per-user rate limit enforced?**
   - Is the limit applied to the specific function/endpoint?
   - Can it be bypassed by batching, GraphQL aliases, or changing headers?

2. **Are payload/body sizes bounded?**
   - Is there a framework-level maximum request size?
   - Does the code validate string/array length before processing?

3. **Are pagination / result-size parameters capped?**
   - Is `limit` / `per_page` bounded by a server-side maximum?

4. **Are file uploads bounded?**
   - Is there a maximum file size, type, and resolution check?
   - Is size checked before loading the whole file into memory?

5. **Are expensive operations throttled or queued?**
   - Password reset, OTP, report generation, image/video processing, bulk imports

6. **Are third-party API calls protected by spending limits or rate caps?**
   - SMS, email, AI, biometrics, cloud storage, payment APIs

7. **For GraphQL, are query complexity and batching limited?**

8. **Edge cases to check**:
   - Limits exist but are set extremely high (e.g., 1 GB body limit)
   - Limits are enforced in one middleware but bypassable for a specific route
   - Rate limit is per-IP while authentication is required
   - Array length checked after deserialization already consumed memory
   - Regular expressions with catastrophic backtracking on user input
   - XML parsers with DTD/entity expansion enabled on untrusted input
   - Native deserialization of untrusted data
   - JSON depth/breadth bombs
   - Missing request/header timeouts (slowloris)
   - Unbounded queue, cache, or process growth
   - LLM/AI endpoints without per-user quota, `max_tokens`/`max_iterations` caps, or spend alerts
   - SSE/WebSocket endpoints without connection-duration, concurrency, or idle-timeout limits

9. **Mandatory OWASP API4:2023 patterns** — if the project has a matching endpoint/integration, verify the controls below. Flag as `[LIKELY VULNERABLE]` if any control is missing:
   - **SMS forgot-password abuse**: per-user rate limit on the initiating endpoint; SMS provider spending cap or billing alert; per-phone-number throttling.
   - **GraphQL profile-picture batch upload**: GraphQL operation/batch count limits; memory/CPU/process limits on image-processing workers; payload-size and per-operation caps.
   - **Cache-bypass cost spike**: cache size/bypass policies; maximum object size enforcement; cloud spend alerts and maximum cost allowance.

### Classification

- **Vulnerable**: No effective limit is enforced; a single client can exhaust resources or incur cost.
- **Likely Vulnerable**: A limit exists but is misconfigured, conditional, or bypassable.
- **Not Vulnerable**: Proper server-side limits are in place.
- **Needs Manual Review**: Cannot determine with confidence (e.g., limits configured outside the codebase, complex gateway rules).

### Finding fields

Every finding block carries: classification tag, file/lines, endpoint or function, issue, impact, proof (code path), remediation, and a **Dynamic Test**. This scan REQUIRES a dynamic-test payload per finding — that requirement is the scan's dynamic-test extension under the shared protocol, and the payload source is this file's own `## Dynamic-Test Payload Examples` section (curl PoC catalog plus the mandatory OWASP API4 scenarios table). For each confirmed or likely-vulnerable finding, include a concrete `curl` command or step-by-step instructions drawn from that catalog (unbounded pagination, ReDoS probe, GraphQL batching, JSON depth bomb, large file upload, SMS/email amplification); use placeholder tokens like `<HOST>`, `<TOKEN>`, `<LARGE_PAYLOAD>`; state what response code, timing, or size indicates the vulnerability.

***

## OWASP API Security Top 10 2023 Mapping
[ref: #resourceconsumption-owasp-mapping]

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
- OWASP LLM Top 10 2025 — **LLM10:2025 Unbounded Consumption**: https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/

***

## Important Reminders
[ref: #resourceconsumption-important-reminders]

- The verify stage must run AFTER the recon stage completes — it depends on the recon output.
- The merge stage must run AFTER all verify batches complete — it depends on all batch outputs.
- Subagents are **read-only**. They must not modify source code, configuration, environment variables, infrastructure manifests, or database state.
- Focus on **single-request resource exhaustion** and **cost amplification**. Horizontal authorization (IDOR) is a different skill.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Trace the full code path: route → middleware → controller → service → data access → third-party API. Limits can be enforced at any layer.
- Pay attention to framework defaults. Some frameworks have no body-size limit by default; others have conservative defaults that may be overridden.
- Intermediate-file lifecycle is owned by `execution-protocol.md`: the merge stage deletes `17_recon.md`, `17_batch_*.md`, and `17_verify_*.md`; only the final `{{ REPORTS_ROOT }}/17_resourceconsumption.md` persists.
