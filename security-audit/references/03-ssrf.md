---
subject: "SSRF detection reference for SAST subagents: definition and scope boundaries, prevention patterns incl. resolve-and-pin, per-stack vulnerable/secure recipes (Python, FastAPI, Node.js, Rails, PHP, Java, Go, C#), LLM agent and MCP fetch surface, OWASP API7 mandatory test cases, bypass catalog, cloud metadata endpoints, blind SSRF techniques, webhook bypasses, three-phase execution prompts, references."
index:
  - anchor: ssrf-detection
    what: "Focused SSRF detection role mapped to OWASP API7:2023, using the three-phase subagent approach — recon, batched verify, merge — gated on the architecture report."
    problem: "Codebase needs systematic request-forgery sweep across every outbound feature, yet unstructured hunting misses call sites and drowns reviewers in unverified candidates; detection orchestration, egress sweep, phase pipeline, verified findings, audit rigor, methodical triage, forgery hunt."
    use_when: "SSRF scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-phase detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual SSRF knowledge is needed, not execution."
    expected: "Verified SSRF findings consolidated into the module report with false positives filtered."
  - anchor: ssrf-definition
    what: "Core definition: attacker-controlled destination reaching an outbound network call, amplified by cloud metadata channels and webhook-era fetch features."
    problem: "Reviewers disagree on what counts as request forgery without shared definition, so borderline fetch features and webhook flows get classified inconsistently across audits; concept baseline, destination control, shared vocabulary, classification consistency, definition anchor, scope clarity, common ground."
    use_when: "Onboarding to the scan; deciding whether a feature belongs to SSRF at all; teaching the detection boundary."
    avoid_when: "Concrete stack recipes are needed — jump to the matching example anchor; execution workflow is the question."
    expected: "Everyone applies one definition: user-influenced destination in a server-side outbound call."
  - anchor: ssrf-scope-in
    what: "Positive scope list: HTTP clients, DNS lookups, webhook dispatches, URL previews, file-from-URL, and custom SSO fetches driven by user input."
    problem: "Detectors under-report when positive fetch patterns stay implicit, missing webhooks, unfurlers, import-from-URL features, and custom SSO flows entirely; inclusion rules, fetch catalog, callback dispatch, link expansion, coverage completeness, missed sinks, hidden fetchers."
    use_when: "Building or checking a recon sink list; unsure whether a feature qualifies; calibrating false negatives."
    avoid_when: "Exclusions are the question — see the scope-out anchor; stack-specific syntax wanted."
    expected: "Every qualifying fetch feature is recognized and flagged during recon."
  - anchor: ssrf-scope-out
    what: "Boundary rules separating SSRF from open redirects, XSS-via-URL, and hardcoded destinations."
    problem: "Findings get misrouted when redirect and rendering classes blur into forgery, corrupting severity and ownership across scans; misrouting risk, class confusion, double reporting, ownership clarity, dedup discipline, category overlap, triage errors."
    use_when: "A finding could belong to another scan class; triaging overlapping categories; writing cross-scan routing notes."
    avoid_when: "Positive patterns are needed — see scope-in; concrete per-stack examples wanted."
    expected: "Each candidate lands in exactly one vulnerability class."
  - anchor: ssrf-prevention-patterns
    what: "Eight constructions that prevent SSRF: host and prefix allowlists, hardcoded destinations, network isolation, scheme/port limits with redirect policy, parser-confusion defenses, response sanitization, and resolve-and-pin with its TOCTOU caveat."
    problem: "Verify subagents need authoritative safe patterns to avoid flagging secured fetchers, and scattered mitigation knowledge produces false positives; safe construction, egress policy, allowlist forms, isolation design, pinning discipline, false-positive control, secure baseline."
    use_when: "Classifying a candidate as mitigated; comparing site code against known-safe forms; writing remediation notes."
    avoid_when: "Vulnerable examples per stack are the need — see recipe anchors; bypass techniques wanted."
    expected: "Allowlisted, isolated, or pinned fetchers are correctly classified as not vulnerable."
  - anchor: ssrf-ex-python-requests
    what: "Python `requests` recipe contrasting user-controlled URLs with allowlisted, validated fetches."
    problem: "Flask-era endpoints pass request data straight into `requests.get` without any destination check, opening direct forgery against internal services; python requests, flask routes, sync client, user url, classic stack, view functions, query args."
    use_when: "Target uses `requests` for outbound calls; reviewing Python fetch features."
    avoid_when: "Async Python — see the httpx or FastAPI recipes; non-Python stacks."
    expected: "Unvalidated `requests` destinations flagged; allowlist-gated fetches verified."
  - anchor: ssrf-ex-python-urllib
    what: "`urllib` recipe covering `urlopen` with user input and the legacy `urllib2` signal."
    problem: "Stdlib fetchers escape framework-style review, and urllib2 sightings mark legacy codebases whose defenses predate modern guidance; urllib urlopen, legacy signal, python2 remnant, opener chains, direct sockets, request objects, build opener, install handlers."
    use_when: "Target uses stdlib urllib; `urllib2` appears in old modules."
    avoid_when: "Third-party clients — see requests or httpx recipes; non-Python stacks."
    expected: "Stdlib destinations validated the same way as third-party clients."
  - anchor: ssrf-ex-python-httpx-aiohttp
    what: "`httpx`/`aiohttp` recipe contrasting unvalidated async fetches with allowlist-gated clients."
    problem: "Async clients interpolate user URLs into awaited calls, and reviewers wrongly treat coroutine-based fetching as inherently safer; httpx asyncclient, aiohttp session, async endpoints, event loop, modern python, await patterns, connection pooling."
    use_when: "Target uses httpx or aiohttp; async services under review."
    avoid_when: "Sync requests — see its recipe; FastAPI webhook flows — see the FastAPI recipe."
    expected: "Async fetch destinations validated identically to sync ones."
  - anchor: ssrf-ex-fastapi
    what: "FastAPI recipe for webhook registration and background-task fetch with scheme/host allowlisting."
    problem: "Webhook registration and deferred tasks fetch user URLs after response completion, hiding forgery behind async scheduling; callback registration, delayed dispatch, path operations, post-response jobs, notification flows, starlette style, pydantic models, dependency wiring."
    use_when: "Target framework is FastAPI; notification or callback features exist."
    avoid_when: "Plain Flask or sync Python — see the requests recipe; non-Python stacks."
    expected: "Webhook destinations gated by scheme and host allowlists before dispatch."
  - anchor: ssrf-ex-llm-agent-fetch
    what: "Recipe for LLM agent URL-fetch tools and MCP fetch servers, covering prompt-injection-driven egress and parser-differential bypasses."
    problem: "Agent stacks fetch URLs from model output without human review, and injected content steers those tools at internal targets; prompt injection, tool poisoning, parser differential, autonomous egress, confused deputy, retrieval content."
    use_when: "LLM frameworks or MCP components present; fetch-like tools registered."
    avoid_when: "No AI integration — classic client recipes suffice."
    expected: "Fetch tools enforce egress policy outside the model path."
  - anchor: ssrf-ex-nodejs-fetch-axios
    what: "Node.js recipe for `fetch`/`axios` with user-controlled URLs versus validated clients."
    problem: "Express handlers forward request fields into fetch calls, and axios conveniences hide missing destination validation entirely; axios get, promise chains, javascript backend, undici client, route logic, json bodies, middleware layers, env configs."
    use_when: "Target runs Node.js with axios or native fetch; reviewing callback-style features."
    avoid_when: "Raw http.request — see its recipe; non-JS stacks."
    expected: "Client call destinations validated before dispatch."
  - anchor: ssrf-ex-nodejs-http-request
    what: "Raw `http.request` recipe where manual URL construction skips client-level helpers."
    problem: "Low-level request building skips library conveniences, so destination validation rarely gets added anywhere at all; http request, raw client, url parse, manual headers, socket level, net modules, write streams, agent options, listen sockets."
    use_when: "Target builds requests with core http/https modules."
    avoid_when: "Higher-level clients — see fetch/axios recipe; non-JS stacks."
    expected: "Manual request destinations validated equivalently to library clients."
  - anchor: ssrf-ex-rails
    what: "Rails recipe for `Net::HTTP` and `OpenURI` with user-influenced destinations."
    problem: "Ruby features like avatar upload-by-URL or feed import pass params into Net::HTTP or open-uri, and open-uri follows redirects silently; rails net http, open uri, redirect opacity, param flow, controller actions, gem clients."
    use_when: "Target uses Rails; import-from-URL or feed features exist."
    avoid_when: "Non-Ruby codebases; background jobs only without user URLs."
    expected: "Ruby fetch destinations validated with redirect policy."
  - anchor: ssrf-ex-php-curl
    what: "cURL recipe contrasting user-set `CURLOPT_URL` with validated requests."
    problem: "PHP services copy request fields into curl options, and flexible handle configuration masks missing destination checks; curlopt url, lamp stack, legacy endpoints, handle reuse, option arrays, exec calls, transfer flags."
    use_when: "Target uses PHP with cURL; reviewing legacy fetch features."
    avoid_when: "file_get_contents flows — see its recipe; non-PHP stacks."
    expected: "cURL destinations validated with scheme and redirect limits."
  - anchor: ssrf-ex-php-file-get-contents
    what: "PHP `file_get_contents` recipe covering stream wrappers as hidden network clients."
    problem: "Stream wrappers turn file functions into network clients, escaping fetch-oriented review entirely; file get contents, stream contexts, php includes, wrapper abuse, hidden client, allow url fopen, remote reads, phar vectors."
    use_when: "Target uses PHP file functions with URLs; stream wrappers enabled."
    avoid_when: "cURL-based fetching — see its recipe; non-PHP stacks."
    expected: "Wrapper-based fetches identified and destination-validated."
  - anchor: ssrf-ex-java-spring-okhttp
    what: "Java recipe for Spring `RestTemplate` and OkHttp with user-built URLs."
    problem: "Java services concatenate paths into RestTemplate or OkHttp calls, and URI builders create false confidence about safety; resttemplate, okhttp, builder pattern, java backend, exchange calls, interceptor chains, retrofit style, http entities."
    use_when: "Target uses Spring MVC-era HTTP clients or OkHttp."
    avoid_when: "Reactive WebClient — see its recipe; non-JVM stacks."
    expected: "Java client destinations validated before execution."
  - anchor: ssrf-ex-java-webclient
    what: "WebClient recipe for reactive fetches with user-influenced URIs."
    problem: "Reactive chains bury destination construction deep inside operators, escaping line-by-line review during audits; webclient, reactor chains, mono flux, uri spec, reactor netty, operator pipelines, flatmap nesting, subscribe sites, backpressure gaps."
    use_when: "Target uses Spring WebFlux WebClient."
    avoid_when: "Servlet-era clients — see the Spring/OkHttp recipe; non-JVM stacks."
    expected: "Reactive fetch destinations validated at chain entry."
  - anchor: ssrf-ex-go-net-http
    what: "Go `net/http` recipe contrasting formatted URLs with validated clients."
    problem: "Go services fmt-build URLs into http.Get, and custom transports rarely add any destination validation at all; golang net http, fmt urls, transport config, backend go, client timeout, round tripper, handler funcs, serve mux, dial context."
    use_when: "Target uses Go for outbound HTTP; reviewing proxy or webhook code."
    avoid_when: "Non-Go stacks; gRPC-only services."
    expected: "Go client destinations validated and redirects controlled."
  - anchor: ssrf-ex-csharp-httpclient
    what: "C# `HttpClient` recipe covering concatenated request URIs."
    problem: "C# services build request URIs by concatenation, and shared HttpClient instances spread risk across layers; csharp httpclient, uri strings, dotnet backend, async tasks, microsoft stack, message handlers, base address, di registration, send async, handler chain."
    use_when: "Target uses .NET HttpClient; reviewing service-layer calls."
    avoid_when: "Non-.NET stacks; SDK-wrapped clients with fixed endpoints."
    expected: "Request URIs validated before sending."
  - anchor: ssrf-variants-intro
    what: "Framing rule: any feature fetching remote resources from user input starts at least `[LIKELY VULNERABLE]` until strict allowlisting and isolation are proven."
    problem: "Fetch features get benefit of doubt without an explicit presumption rule, letting weak validations pass as safe; proof burden, conservative bias, verdict floor, triage policy, guilty until, assume weak, leniency trap, undeserved trust, soft pass."
    use_when: "Starting variant analysis; deciding initial classification of a fetch feature."
    avoid_when: "Specific bypass or test-case detail is needed — see the following anchors."
    expected: "Every fetch feature is presumed weak until defenses are demonstrated."
  - anchor: ssrf-mandatory-test-cases
    what: "OWASP API7 scenario table: metadata credential theft, link-preview exploitation, internal port scanning, and webhook test-request leaks."
    problem: "Audits skip canonical scenarios without checklists, missing flows that OWASP explicitly calls out for this risk; canonical cases, metadata theft, scan flows, checklist discipline, engagement scope, coverage gaps, skipped vectors."
    use_when: "Building the test plan; verifying engagement covers canonical flows."
    avoid_when: "Bypass mechanics are the question — see the bypass catalog."
    expected: "All applicable OWASP scenarios appear in the test plan."
  - anchor: ssrf-bypass-catalog
    what: "Catalog of validation bypasses: DNS rebinding, parser confusion, dangerous schemes, IPv6/CIDR tricks, IDNA, decimal IP, chained redirects, CRLF, smuggling, and document-processor SSRF."
    problem: "Defenses look solid until bypass classes get enumerated, and naive checks fail on encoding, scheme, or parser tricks; bypass techniques, rebinding, scheme abuse, parser gaps, decimal notation, smuggling vectors, idna homographs, octal forms."
    use_when: "Evaluating whether a validation is actually robust; building adversarial tests."
    avoid_when: "High-level scenarios wanted — see mandatory test cases; stack recipes needed."
    expected: "Validations are stress-tested against every applicable bypass class."
  - anchor: ssrf-metadata-endpoints
    what: "Lookup of cloud and infrastructure metadata services: AWS (incl. IPv6 IMDS), ECS, GCP, Azure, DigitalOcean, Alibaba, OCI, Hetzner, Kubernetes, Docker, Vault, and CI runners."
    problem: "Impact assessment and payloads need exact metadata endpoints per platform, which nobody memorizes reliably; imds variants, runner endpoints, credential paths, environment lookup, link local, cloud internals, token theft, instance identity, role creds."
    use_when: "Choosing test destinations; assessing blast radius of a confirmed forgery."
    avoid_when: "Bypass mechanics wanted — see bypass catalog; blind detection needed."
    expected: "Correct metadata services selected per deployment environment."
  - anchor: ssrf-blind-techniques
    what: "Blind SSRF detection: out-of-band callbacks, DNS-based signalling, timing deltas, and error-channel inference."
    problem: "No-response fetches stay invisible without out-of-band proof, so blind variants get dismissed as unexploitable; blind detection, oob callback, timing oracle, error channels, proof strategy, interactsh style, delayed beacon, silent hits, burp collaborator."
    use_when: "Target returns no response content; confirming suspected blind forgery."
    avoid_when: "Responses are reflected — direct evidence suffices."
    expected: "Blind candidates confirmed or refuted via out-of-band signals."
  - anchor: ssrf-webhook-bypasses
    what: "Webhook verification bypass patterns: test-ping leaks, rebind-during-verification, and credential disclosure in test responses."
    problem: "Webhook flows verify one request and fetch another, leaking headers or hitting internal targets through timing gaps; test ping, verification race, callback abuse, registration flow, header leakage, rebind window, secret hints."
    use_when: "Webhook registration or test features exist; reviewing verification logic."
    avoid_when: "No webhook features in scope; generic bypasses wanted instead."
    expected: "Webhook verification gaps identified with concrete abuse paths."
  - anchor: ssrf-owasp-cross-mapping
    what: "Cross-mapping of SSRF findings to API8 and API10 when misconfiguration or third-party reliance drives the issue."
    problem: "Findings rooted in config gaps or partner reliance need dual taxonomy, and single-label habits lose causal chains; dual mapping, taxonomy routing, config origin, label accuracy, cause tracking, multi risk, joined labels, label pairs."
    use_when: "Tagging findings whose cause spans categories; writing risk sections."
    avoid_when: "Pure destination-control cases — plain API7 label suffices."
    expected: "Cross-root findings carry both labels with reasoning."
  - anchor: ssrf-prevention-checklist
    what: "OWASP API7 prevention checklist condensed for remediation advice."
    problem: "Reports need actionable remediation beyond single fixes, and piecemeal advice misses defense in depth; remediation list, checklist form, fix guidance, hardening advice, report quality, action items, depth layers, stacked controls, owner actions."
    use_when: "Writing remediation sections; reviewing an existing defense-in-depth design."
    avoid_when: "Detection mechanics are the question — see execution anchors."
    expected: "Remediation advice covers network, application, and response layers."
  - anchor: ssrf-execution-intro
    what: "Execution overview: three phases run by subagents with the architecture report passed as context to each."
    problem: "Detection work without orchestration structure duplicates effort and loses batch boundaries across phases; execution model, phase overview, subagent orchestration, context passing, batch discipline, workflow entry, staging, dispatch plan, coordination, uniform."
    use_when: "Starting the SSRF scan execution; deciding how to dispatch subagents."
    avoid_when: "Specific phase prompts are needed — jump to phase anchors."
    expected: "All three phases dispatched with shared architecture context."
  - anchor: ssrf-phase1-recon
    what: "Recon prompt instructing the subagent to find every outbound network call site with per-library patterns and skip lists."
    problem: "Unstructured searching misses call sites or floods candidates with safe code, so recon needs explicit patterns and exclusions; site discovery, skip rules, candidate quality, coverage discipline, grep scope, noise control, thorough sweep."
    use_when: "Launching the recon subagent; reviewing recon completeness."
    avoid_when: "Candidates already gathered — proceed to verify; conceptual knowledge wanted."
    expected: "Complete, de-duplicated candidate list of outbound call sites."
  - anchor: ssrf-phase1-gate
    what: "Zero-candidate short-circuit: emit a clean no-findings stub and stop when recon finds nothing."
    problem: "Pipeline without early exit wastes verify batches on empty candidate sets and leaves missing artifacts; empty recon, pipeline efficiency, artifact completeness, stop rule, graceful halt, zero results, skipped verify, idle batches."
    use_when: "Recon returned zero candidates."
    avoid_when: "Candidates exist — proceed to batched verification."
    expected: "No-findings stub written and the scan stops gracefully."
  - anchor: ssrf-phase2-verify
    what: "Batched taint-tracing prompt linking user input to outbound call sites, with safeguard-tier decision rules and classification labels."
    problem: "Unverified candidates are noise, and safeguard quality varies from strict allowlists to cosmetic blocklists, so tiered verification is required; taint tracing, batch processing, parallel analysis, evidence demand, tier judgment, label assignment, tier mapping, site verdicts."
    use_when: "Candidates confirmed present; dispatching verify subagents in batches of three."
    avoid_when: "Recon incomplete; merge stage is the need."
    expected: "Every candidate classified against its safeguard tier with traced evidence."
  - anchor: ssrf-phase3-merge
    what: "Merge procedure consolidating batch reports into the final module report with dedup and the output template."
    problem: "Parallel batch outputs overlap and diverge, and without merge discipline final reports duplicate or lose findings; result merging, dedup, consolidation, final template, partial results, report integrity, clean handoff, overlap removal, single output."
    use_when: "All verify batches finished; producing `03_ssrf.md`."
    avoid_when: "Batches still running; recon stage not done."
    expected: "Single consolidated module report with unique, classified findings."
  - anchor: ssrf-references
    what: "External reference list for SSRF concepts, bypass research, and cloud metadata documentation."
    problem: "Agents and readers need authoritative follow-up sources beyond this file's distilled content; further reading, research links, external canon, deep dives, vendor documentation, community knowledge, primary material, cited works, owasp pages."
    use_when: "Primary sources or extended material is needed."
    avoid_when: "Detection recipes or execution workflow are the question — the references list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
  - anchor: ssrf-reminders
    what: "Operational guardrails: blocklists are not mitigations, evidence requirements, report discipline."
    problem: "Under pressure, agents accept blocklists as fixes, skip evidence, or overstate severity, corrupting report quality; mitigation rigor, evidence demand, severity honesty, quality guardrails, review discipline, trap avoidance, false comfort, checklist, final review."
    use_when: "Reviewing draft findings before merge; calibrating classifications."
    avoid_when: "Specific bypass techniques or payload syntax are the question — see the bypass and payload anchors; this card only guards finding quality."
    expected: "Merged findings carry proof for every claim, blocklists never counted as a fix, and severity matches demonstrated impact."
---

# Server-Side Request Forgery (SSRF) Detection

[ref: #ssrf-detection]

You are performing a focused security assessment to find SSRF vulnerabilities in a codebase. This assessment maps to **OWASP API Security Top 10 2023 — API7:2023 Server Side Request Forgery**. This skill uses a three-phase approach with subagents: **recon** (find all places that make outbound TCP, DNS, or HTTP requests), **batched verify** (trace whether user-supplied input reaches those call sites, in parallel batches of 3), and **merge** (consolidate batch reports into one file).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

## What is SSRF
[ref: #ssrf-definition]

SSRF occurs when an attacker can cause the server to make outbound network requests to an arbitrary destination — including internal services, cloud metadata endpoints, or other external targets — by supplying or influencing the URL, hostname, IP, port, or scheme used in a server-side request.

The core pattern: *unvalidated, user-controlled input reaches the destination argument of an outbound network call.*

OWASP API7:2023 stresses that modern application concepts make SSRF both more common and more dangerous:

- **More common**: webhooks, file fetching from URLs, URL previews, custom SSO integrations, import-from-URL features, PDF renderers, image proxies, and notification channels all encourage developers to access a remote resource based on user input.
- **More dangerous**: cloud providers, Kubernetes, and Docker expose management and control channels over HTTP on predictable, well-known paths. Those channels are easy targets once an application can be coerced into making an outbound request.

### What SSRF IS
[ref: #ssrf-scope-in]

- HTTP client calls where the URL or host is built from user input: `requests.get(user_url)`
- Fetching a resource whose location is provided by the client: `fetch(req.body.webhook_url)`
- DNS lookups on a hostname supplied by the user: `dns.lookup(req.query.host)`
- Raw TCP connections to a host/port derived from user input: `socket.connect((user_host, user_port))`
- File-fetching functions used with HTTP/FTP URLs from user input: `file_get_contents($user_url)`
- URL redirectors that forward to a user-supplied destination without validation
- Webhooks, import-from-URL, screenshot services, PDF renderers, image proxies, video transcoders — any feature that fetches a remote resource on behalf of the user
- Server-side XML/JSON parsers, document converters, or media processors that fetch external resources while processing user-supplied content
- Subprocess invocations of `curl`, `wget`, `nc`, or similar tools with a user-influenced target

### What SSRF is NOT
[ref: #ssrf-scope-out]

Do not flag these:

- **Open redirects**: Redirecting the browser (HTTP 302) to a user-supplied URL — that's a client-side redirect, not a server-side request
- **XSS via URL**: Rendering a user-supplied URL in an `<a>` tag without escaping — that's XSS
- **IDOR**: Accessing another user's data by changing an object ID — separate vulnerability class
- **Hardcoded outbound calls**: HTTP requests to fixed, fully hardcoded URLs with no user influence — not SSRF
- **Local service-to-service calls with a hardcoded localhost address**: e.g., a health-check call to `http://127.0.0.1:8080/ready` where neither host nor port is influenced by user input

### Patterns That Prevent SSRF
[ref: #ssrf-prevention-patterns]

When you see these patterns, the code is likely **not vulnerable**:

**1. Strict allowlist of permitted destinations**
```python
ALLOWED_HOSTS = {"api.example.com", "cdn.example.com"}
parsed = urlparse(user_url)
if parsed.hostname not in ALLOWED_HOSTS:
    raise ValueError("Destination not allowed")
requests.get(user_url)
```

**2. Allowlist of permitted URL prefixes / schemes**
```python
ALLOWED_PREFIXES = ["https://api.example.com/", "https://cdn.example.com/"]
if not any(user_url.startswith(p) for p in ALLOWED_PREFIXES):
    abort(400)
requests.get(user_url)
```

**3. No user influence on the destination**
```python
# Destination fully hardcoded — no user input involved
response = requests.get("https://api.thirdparty.com/data")
```

**4. Network isolation of resource-fetching components**
Place fetchers, webhooks, and image proxies in dedicated subnets or isolated execution environments. Block access to cloud metadata endpoints (e.g., `169.254.169.254`), internal IP ranges, and unnecessary egress. Network controls reduce blast radius even if application-level validation fails.

On AWS, enforce **IMDSv2** (`HttpTokens=required`): metadata access then requires a session token obtained via a `PUT` request with a custom header, which a plain SSRF `GET` cannot perform; keep `HttpPutResponseHopLimit=1` (raise to `2` only for containerized workloads) so token requests cannot cross network hops. GCP and Azure metadata services likewise require special headers (`Metadata-Flavor: Google`, `Metadata: true`) that simple SSRF cannot forge — flag any deployment where metadata is reachable without them.

**5. URL scheme and port allowlists; disabling HTTP redirects**
Enforce an allowlist of permitted schemes (usually `https`) and ports. Disable automatic HTTP redirect following in the HTTP client, or validate any redirected destination against the same allowlist. Redirects can turn a trusted URL into an internal or attacker-controlled endpoint.

**6. URL parser confusion defenses**
Attackers bypass naive validation with alternative IP representations (`127.0.0.1`, `0177.1`, `2130706433`, `[::1]`), IDN homographs, the `@`-trick (`https://attacker.com@internal/`), open-redirect chaining, or double-parsing mismatches. Use a well-tested URL parser, validate the final parsed hostname/IP against the allowlist, and reject any URL whose parser-normalized form does not match the allowed destination.

**7. Do not forward raw third-party responses**
The response from an outbound request is treated as untrusted input. Do not stream it unchanged to the client; sanitize, validate, or transform the content before use. Returning raw responses can leak internal data or act as an open proxy.

**8. Resolve-and-pin (DNS resolution + validated-IP connection)**
Resolve the hostname once, validate the resulting IP against the destination policy, then connect to that pinned IP while preserving the original `Host` header/SNI. This defeats DNS rebinding where the hostname flips to an internal address between validation and fetch. Residual TOCTOU weakness: if the client library or OS re-resolves the hostname at connect time instead of using the pinned IP, the check is void — verify the pinning actually happens at the socket level (custom resolver, `Connection`-pinned pool), not just at URL-validation time.

> **Note**: IP blocklists (blocking `169.254.0.0/16`, `10.0.0.0/8`, etc.) are **not** sufficient protection — they can be bypassed via DNS rebinding, URL encoding, IPv6 notation, decimal IP representation, or redirect chains. Do not treat a blocklist as making a site safe; classify it as Likely Vulnerable.

***

## Vulnerable vs. Secure Examples

### Python — requests
[ref: #ssrf-ex-python-requests]

```python
# VULNERABLE: URL fully controlled by user
@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    response = requests.get(url)
    return response.text

# SECURE: strict allowlist on destination host
ALLOWED = {"api.example.com"}
@app.route('/fetch')
def fetch():
    url = request.args.get('url')
    if urlparse(url).hostname not in ALLOWED:
        abort(403)
    response = requests.get(url)
    return response.text
```

### Python — urllib
[ref: #ssrf-ex-python-urllib]

```python
# VULNERABLE: user controls the URL passed to urlopen
def preview(request):
    target = request.GET.get('target')
    data = urllib.request.urlopen(target).read()
    return HttpResponse(data)

# SECURE: only allow https scheme to a hardcoded host
def preview(request):
    target = request.GET.get('target')
    parsed = urlparse(target)
    if parsed.scheme != 'https' or parsed.hostname != 'media.example.com':
        return HttpResponse(status=400)
    data = urllib.request.urlopen(target).read()
    return HttpResponse(data)
```

### Python — httpx / aiohttp
[ref: #ssrf-ex-python-httpx-aiohttp]

```python
# VULNERABLE: user-controlled URL in async client
async def preview(request):
    target = request.query_params.get('target')
    async with httpx.AsyncClient() as client:
        r = await client.get(target)
        return r.text

# VULNERABLE: user-controlled URL in aiohttp
async def webhook(req):
    url = req.query['url']
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return web.Response(text=await resp.text())

# SECURE: allowlist + disabled redirects
async def safe_preview(request):
    target = request.query_params.get('target')
    parsed = urlparse(target)
    if parsed.scheme != 'https' or parsed.hostname not in ALLOWED_HOSTS:
        raise HTTPException(status_code=403)
    async with httpx.AsyncClient(follow_redirects=False) as client:
        r = await client.get(target)
        return r.text
```

### Python — FastAPI (webhooks & async fetch)
[ref: #ssrf-ex-fastapi]

```python
from fastapi import FastAPI, BackgroundTasks
import httpx

app = FastAPI()

# VULNERABLE: user-supplied webhook URL fetched server-side
@app.post("/webhooks")
async def register_webhook(url: str, background: BackgroundTasks):
    background.add_task(httpx.AsyncClient().post, url, json={"event": "test"})
    return {"registered": url}

# SECURE: scheme + host allowlist, resolved and pinned before dispatch
ALLOWED_SCHEMES = {"https"}
@app.post("/webhooks")
async def register_webhook(url: str, background: BackgroundTasks):
    parsed = httpx.URL(url)
    if parsed.scheme not in ALLOWED_SCHEMES or not is_allowed_host(parsed.host):
        raise HTTPException(400, "destination not allowed")
    background.add_task(deliver, parsed)
    return {"registered": url}
```

FastAPI path operations often wrap outbound calls in `BackgroundTasks` — taint is just as real even though the fetch happens after the response.

### LLM agent URL-fetch tools & MCP fetch servers
[ref: #ssrf-ex-llm-agent-fetch]

```python
# VULNERABLE: agent tool fetches arbitrary URLs from model output
@tool
def fetch_url(url: str) -> str:
    return requests.get(url).text          # prompt injection → internal scan

# SECURE: fetch tool with egress policy enforced outside the model
@tool
def fetch_url(url: str) -> str:
    require_allowed_destination(url)        # scheme/host allowlist + resolve-and-pin
    return requests.get(url, timeout=5).text
```

LLM/agent stacks create SSRF without a human in the loop: indirect prompt injection in fetched content can drive the agent's own URL-fetch tool against internal targets. MCP fetch servers often run with broader network privileges than the LLM client — an exposed MCP `fetch` endpoint is itself an SSRF oracle. URL parsing also differs across the agent → MCP client → HTTP library → DNS resolver chain, enabling parser-differential bypasses no single layer rejects.

### Node.js — fetch / axios
[ref: #ssrf-ex-nodejs-fetch-axios]

```javascript
// VULNERABLE: webhook URL comes directly from request body
app.post('/webhook/test', async (req, res) => {
  const { url } = req.body;
  const result = await fetch(url);
  res.json(await result.json());
});

// SECURE: allowlist check before fetch
const ALLOWED_HOSTS = new Set(['hooks.example.com']);
app.post('/webhook/test', async (req, res) => {
  const { url } = req.body;
  const { hostname } = new URL(url);
  if (!ALLOWED_HOSTS.has(hostname)) return res.status(403).send('Forbidden');
  const result = await fetch(url, { redirect: 'manual' });
  res.json(await result.json());
});
```

### Node.js — http.request
[ref: #ssrf-ex-nodejs-http-request]

```javascript
// VULNERABLE: host and path from query string
app.get('/proxy', (req, res) => {
  const { host, path } = req.query;
  http.get({ host, path }, (proxyRes) => proxyRes.pipe(res));
});
```

### Ruby on Rails — Net::HTTP / OpenURI
[ref: #ssrf-ex-rails]

```ruby
# VULNERABLE: open() fetches arbitrary URL
def import
  url = params[:url]
  content = URI.open(url).read  # also triggers for open(url) via Kernel#open
  # ...
end

# SECURE: restrict scheme and host
def import
  url = params[:url]
  uri = URI.parse(url)
  raise "Forbidden" unless uri.is_a?(URI::HTTPS) && uri.host == "data.example.com"
  content = uri.open.read
  # ...
end
```

### PHP — cURL
[ref: #ssrf-ex-php-curl]

```php
// VULNERABLE: user-supplied URL piped into curl
function fetch_preview($url) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}
// Called as: fetch_preview($_GET['url'])

// SECURE: validate URL against allowlist before curl
function fetch_preview($url) {
    $allowed = ['https://cdn.example.com/'];
    foreach ($allowed as $prefix) {
        if (strpos($url, $prefix) === 0) {
            // ... proceed with curl
        }
    }
    throw new Exception("Destination not allowed");
}
```

### PHP — file_get_contents
[ref: #ssrf-ex-php-file-get-contents]

```php
// VULNERABLE: file_get_contents with http:// wrapper and user input
$url = $_GET['source'];
$data = file_get_contents($url);  // fetches remote URL if scheme is http/https/ftp
```

### Java — Spring / OkHttp
[ref: #ssrf-ex-java-spring-okhttp]

```java
// VULNERABLE: RestTemplate with user-controlled URL
@GetMapping("/proxy")
public ResponseEntity<String> proxy(@RequestParam String url) {
    RestTemplate restTemplate = new RestTemplate();
    return restTemplate.getForEntity(url, String.class);
}

// VULNERABLE: OkHttp with user-controlled host
public String fetch(String host, String path) {
    Request request = new Request.Builder()
        .url("https://" + host + path)
        .build();
    return client.newCall(request).execute().body().string();
}
```

### Java — WebClient
[ref: #ssrf-ex-java-webclient]

```java
// VULNERABLE: user-controlled URI in WebClient
public Mono<String> preview(@RequestParam String url) {
    return WebClient.create().get().uri(url).retrieve().bodyToMono(String.class);
}

// SECURE: allowlist + no redirects
public Mono<String> safePreview(@RequestParam String url) {
    URI uri = URI.create(url);
    if (!"https".equals(uri.getScheme()) || !ALLOWED_HOSTS.contains(uri.getHost())) {
        return Mono.error(new ResponseStatusException(HttpStatus.FORBIDDEN));
    }
    return WebClient.create().get().uri(uri).retrieve().bodyToMono(String.class);
}
```

### Go — net/http
[ref: #ssrf-ex-go-net-http]

```go
// VULNERABLE: user-supplied URL passed to http.Get
func proxyHandler(w http.ResponseWriter, r *http.Request) {
    target := r.URL.Query().Get("url")
    resp, err := http.Get(target)
    if err != nil {
        http.Error(w, err.Error(), 500)
        return
    }
    io.Copy(w, resp.Body)
}

// VULNERABLE: user controls host in net.Dial
func dialHandler(w http.ResponseWriter, r *http.Request) {
    host := r.URL.Query().Get("host")
    port := r.URL.Query().Get("port")
    conn, _ := net.Dial("tcp", host+":"+port)
    // ...
}
```

### C# — HttpClient
[ref: #ssrf-ex-csharp-httpclient]

```csharp
// VULNERABLE: user-supplied URL passed to HttpClient
[HttpGet("proxy")]
public async Task<IActionResult> Proxy([FromQuery] string url)
{
    var response = await _httpClient.GetAsync(url);
    var content = await response.Content.ReadAsStringAsync();
    return Content(content);
}
```

***

## SSRF variants, bypasses, and test cases
[ref: #ssrf-variants-intro]

Subagents should treat any feature that fetches a remote resource from user input as at least `[LIKELY VULNERABLE]` unless strict allowlisting and network isolation are proven.

### Mandatory OWASP API7 test cases
[ref: #ssrf-mandatory-test-cases]

| Scenario | Attack flow | Detection target |
| --- | --- | --- |
| Profile picture from URL | `POST /api/profile/upload_picture` accepts `picture_url`; attacker sends `localhost:8080` to port-scan internally. Response time or error differentiates open/closed ports. | Any endpoint that fetches a user-supplied URL and returns or processes the response. |
| Webhook test request to cloud metadata | GraphQL `createNotificationChannel` sends a test request to attacker-supplied URL; attacker targets `http://169.254.169.254/latest/meta-data/iam/security-credentials/...` and the response is leaked. | Webhook/notification endpoints that make outbound requests and echo the response; cloud metadata endpoints accessible from the server. |
| URL preview / link expansion | Endpoint accepts a user URL, fetches it, and returns a title/image/summary. Attacker points it at `http://169.254.169.254/latest/meta-data/` or an internal service. | Link-expansion, oEmbed, or "unfurl" features. |
| Import from URL | File import, document conversion, or media processing accepts a remote URL and fetches it server-side. | Import, CSV load, PDF generation, image resize, or video transcode pipelines. |
| Custom SSO / OAuth callback | OAuth or custom SSO flow allows a user-influenced `redirect_uri` or `state` URL that is later fetched server-side. | Authentication integrations that fetch tokens or metadata from a user-supplied endpoint. |

### Bypass and variant catalog
[ref: #ssrf-bypass-catalog]

| Bypass / variant | Technique | Detection signal |
| --- | --- | --- |
| DNS rebinding | Host resolves to public IP initially, then to internal IP on second lookup. | URL validation performed at fetch time only; no DNS pinning; time-of-check vs time-of-use gap. |
| URL parser confusion | `http://attacker.com@internal/`, `http://internal#attacker.com`, `http://0x7f000001`, `http://127.1`, `http://0177.0.0.1`. | Custom URL validation instead of a well-tested parser; parser differences between validator and fetcher. |
| Dangerous schemes | `gopher://`, `file://`, `dict://`, `ldap://`, `jar://`, `expect://`, `ftp://`, `tftp://`, `ssh://`. | Scheme not restricted to `http`/`https`; URL parser accepts arbitrary schemes. |
| IPv6 / CIDR bypass | `http://[::1]/`, `http://[0:0:0:0:0:0:ffff:127.0.0.1]/`, `http://0177.0.0.01/`, `http://[::ffff:169.254.169.254]`. | IP blocklist only covers IPv4 dotted-quad; no IPv6 or octal/hex handling. |
| IDNA / Unicode homoglyphs | `http://ⓔⓧⓐⓜⓟⓛⓔ.ⓒⓞⓜ` resolving to attacker-controlled domain. | Hostname validation does not normalize Unicode before check. |
| Decimal / hexadecimal IP | `http://2130706433/` (127.0.0.1), `http://0x7f000001/`, `http://0251.0376.0317.0371/`. | Validation only checks dotted-decimal IPv4. |
| Open-redirect chaining | Application follows a redirect from an allowed host to an internal/metadata host. | Redirect following enabled; redirected destination not re-validated. |
| CRLF / header injection in URL | URL contains `%0d%0a` causing the HTTP client to inject headers. | User input embedded directly in request line or headers. |
| Path traversal in assembled URL | `"https://api.example.com/" + user_path` where `user_path` is `../attacker.com/`. | Concatenation-based URL construction without final parser validation. |
| SSRF via HTTP request smuggling | Smuggled request triggers internal fetch. | Conflicting `Content-Length`/`Transfer-Encoding` handling across proxy/backend. |
| Outbound XXE | DTD/entity declaration forces parser to fetch external URL. | XML parser with external entities enabled; see `07-xxe.md`. |
| SSRF in file/document processors | ImageMagick, LibreOffice, FFmpeg, PDF generators, Pandoc, or DOCX renderers fetch remote resources during processing. | Processor invoked on user-supplied files/URLs without sandboxing or URL allowlists. |
| SSRF via PDF / SVG / font external references | User-uploaded document embeds external images, fonts, or stylesheets that the server fetches during rendering. | Server-side rendering of user-supplied rich documents. |
| SSRF via user-controlled proxy | Application offers a proxy endpoint or uses a user-supplied proxy configuration for outbound requests. | Proxy URL derived from user input. |
| SSRF via user-controlled callback URL | OAuth, payment, or webhook registration stores a URL that the server calls later. | Stored URL accepted without allowlist validation at write time. |

### Container and cloud metadata endpoints
[ref: #ssrf-metadata-endpoints]

Beyond the classic `169.254.169.254`, subagents should test for these metadata endpoints when the deployment environment suggests them:

| Platform | Endpoint | Exposure |
| --- | --- | --- |
| AWS EC2 / Lambda (IMDSv1/v2) | `http://169.254.169.254/latest/meta-data/` | Credentials, IAM roles, user-data, instance identity. |
| AWS EC2 IPv6 (Nitro) | `http://[fd00:ec2::254]/latest/meta-data/` | Same IMDS over IPv6 — bypasses IPv4-only blocklists. |
| GitHub Actions / GitLab runner | `http://169.254.169.254/` from CI jobs | Runner identity tokens, job metadata, OIDC endpoints. |
| AWS ECS | `http://169.254.170.2/v2/credentials/<GUID>` | Task role credentials. |
| GCP | `http://metadata.google.internal/computeMetadata/v1/` | Project info, access tokens, service-account keys. Requires `Metadata-Flavor: Google` header. |
| Azure | `http://169.254.169.254/metadata/instance?api-version=...` | Instance metadata, identity tokens. Requires `Metadata: true` header. |
| Azure Container Instances | `http://169.254.169.254/metadata/instance` | Container instance metadata. |
| DigitalOcean | `http://169.254.169.254/metadata/v1.json` | Droplet metadata, user-data, SSH keys. |
| Alibaba Cloud (ECS) | `http://100.100.100.200/latest/meta-data/` | Instance metadata, RAM credentials. |
| Oracle Cloud (OCI) | `http://169.254.169.254/opc/v1/instance/` or `http://192.0.0.192/` | Instance metadata. |
| Hetzner Cloud | `http://169.254.169.254/hetzner/v1/metadata` | Instance metadata, user-data. |
| Kubernetes | `https://kubernetes.default.svc` / `http://<service>.<namespace>` | Service account tokens, internal services. |
| Docker | `http://172.17.0.1:2375/` | Docker daemon if exposed without TLS. |
| HashiCorp Vault | `http://127.0.0.1:8200/v1/...` | Vault API if reachable from the application. |
| Local cloud-init / metadata | `http://169.254.169.254/` on many clouds | Standard link-local metadata service. |

### Blind SSRF detection techniques
[ref: #ssrf-blind-techniques]

When the server does not return the response body to the attacker, use these techniques to confirm SSRF:

- **Out-of-band (OOB) callbacks**: direct the target to an attacker-controlled server (e.g., Burp Collaborator, Interactsh, a private request-bin) and watch for DNS/HTTP hits. Example payload: `http://<unique>.burpcollaborator.net/` or `http://<unique>.oast.pro/`.
- **Time delays**: use payloads that cause the target database or service to sleep if the parameter is injectable into a secondary request. Example: `http://internal-service/slow-endpoint` or, for some protocols, a URL that hangs.
- **Error / differential analysis**: send a URL that should fail quickly (closed port) versus one that should succeed (open internal service); compare response times or error messages. Example: `http://localhost:22/` vs `http://localhost:8080/`.
- **DNS rebinding probes**: verify whether validation is performed only once by changing the DNS record between verification and fetch. If the application validates the URL at time T0 but fetches at T1, a DNS record swap can bypass host-based checks.
- **Protocol-specific side channels**: some internal services (Redis, Memcached, Elasticsearch, SMTP) return distinctive errors or banners that leak through generic error pages or response times.
- **Collab + redirect chains**: host a redirect on an allowed domain that points to an OOB callback or internal target. If the application follows redirects, the callback confirms the request reached the attacker-controlled chain.

### Webhook verification bypass patterns
[ref: #ssrf-webhook-bypasses]

| Pattern | Abuse |
| --- | --- |
| Test-ping webhooks | Attacker registers a URL that receives a test request containing internal headers/secrets. |
| Host-header injection during verification | Verification request uses a different `Host` header than the fetch request. |
| DNS rebind during verification | Verification resolves to allowed origin, fetch resolves to internal target. |
| Time-of-check/time-of-use gap | URL validated once, fetched later after TTL expiration or DNS update. |
| Verification-only allowlist | Application verifies the URL by fetching it once, then stores it and later fetches without re-checking after a DNS update. |
| Partial URL control in webhook path | Attacker controls only the path or query of an otherwise allowlisted base URL, enabling open-redirect-style internal fetches. |
| Webhook secret leakage in test responses | Test-ping responses may echo headers, body, or signature computation details that reveal how the app verifies webhooks. |

### OWASP API8/API10 cross-mapping
[ref: #ssrf-owasp-cross-mapping]

SSRF findings can also represent other OWASP API 2023 risks:

- **API8:2023 Security Misconfiguration** — permissive egress rules, open redirects, weak URL-parser configuration, permissive scheme handling, unpatched HTTP clients that follow redirects by default, or inconsistent request parsing that enables request smuggling.
- **API10:2023 Unsafe Consumption of APIs** — blind forwarding of third-party responses to clients, over-trusting upstream webhooks without verification, following redirects from third-party APIs without re-validation, or treating data fetched from an integrated API as safe.

Each finding should note any API8/API10 root-cause conditions that apply in addition to API7.

### SSRF prevention checklist (from OWASP API7)
[ref: #ssrf-prevention-checklist]

Subagents should verify whether the following controls are present and effective:

1. **Network isolation**: resource-fetching components run in a separate network segment with no access to internal services or metadata endpoints.
2. **Allowlists**: remote origins, URL schemes, ports, and accepted media types are explicitly allowlisted.
3. **Disable redirects**: automatic HTTP redirection is disabled, or every redirected destination is re-validated.
4. **Well-tested URL parser**: validation uses a maintained parser and re-parses the URL after any normalization.
5. **Input validation and sanitization**: all client-supplied URL components are validated before use.
6. **No raw response forwarding**: responses from outbound requests are not streamed unchanged to the client.

***

## Execution
[ref: #ssrf-execution-intro]

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Find All Outbound Network Call Sites
[ref: #ssrf-phase1-recon]

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where the application makes an outbound network request — HTTP, HTTPS, FTP, TCP, UDP, or DNS — regardless of whether that destination is user-controlled. Write results to `{{ REPORTS_ROOT }}/03_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, HTTP client libraries in use, and any networking or webhook-related components.
>
> **What to search for — outbound request call sites**:
>
> You are looking for any code that opens a network connection or fetches a remote resource. Flag ANY call where a non-trivially-hardcoded URL, host, or address value is passed as an argument. You are not yet tracing whether that value is user-controlled; that is Phase 2's job.
>
> 1. **Python HTTP clients**:
>    - `requests.get(url)`, `requests.post(url)`, `requests.put(url)`, `requests.request(method, url)`, `requests.Session().get(url)`
>    - `urllib.request.urlopen(url)`, `urllib2.urlopen(url)` (Python 2 only — dead on any modern codebase; treat its presence as legacy-code signal)
>    - `httpx.get(url)`, `httpx.post(url)`, `httpx.AsyncClient().get(url)`
>    - `aiohttp.ClientSession().get(url)`, `aiohttp.ClientSession().post(url)`
>
> 2. **Python socket / DNS**:
>    - `socket.connect((host, port))`, `socket.create_connection((host, port))`
>    - `dns.resolver.resolve(name)`, `socket.getaddrinfo(host, ...)`
>
> 3. **Python file-fetching with remote schemes**:
>    - `urllib.request.urlopen(url)` where url may be http/https/ftp
>    - `open(url)` via `from urllib.request import urlopen` or similar (flag if url may be remote)
>
> 4. **Node.js / JavaScript HTTP clients**:
>    - `fetch(url)`, `node-fetch(url)`
>    - `axios.get(url)`, `axios.post(url)`, `axios.request({url})`
>    - `http.get(url)`, `https.get(url)`, `http.request(options)`, `https.request(options)`
>    - `got(url)`, `superagent.get(url)`, `needle.get(url)`, `undici.request(url)`
>    - `require('request')(options)`
>
> 5. **Node.js socket / DNS**:
>    - `net.createConnection({host, port})`, `net.connect(port, host)`
>    - `dns.lookup(hostname, ...)`, `dns.resolve(hostname, ...)`, `dns.resolve4(hostname)`
>
> 6. **Ruby HTTP clients**:
>    - `Net::HTTP.get(uri)`, `Net::HTTP.start(host, ...)`, `Net::HTTP.get_response(url)`
>    - `URI.open(url)`, `open(url)` (Kernel#open / OpenURI)
>    - `RestClient.get(url)`, `RestClient::Resource.new(url)`
>    - `Faraday.new(url).get(path)`, `HTTParty.get(url)`
>    - `Typhoeus::Request.new(url)`
>
> 7. **PHP HTTP clients and file functions**:
>    - `curl_setopt($ch, CURLOPT_URL, $url)` followed by `curl_exec($ch)`
>    - `file_get_contents($url)` — flag when `$url` may be an http/https/ftp URL
>    - `fopen($url, 'r')` with a remote URL scheme
>    - `Guzzle`: `$client->request('GET', $url)`, `$client->get($url)`
>    - `Symfony HttpClient`: `$client->request('GET', $url)`
>
> 8. **Java HTTP clients**:
>    - `new URL(url).openConnection()`, `new URL(url).openStream()`
>    - `HttpURLConnection` / `HttpsURLConnection` with a dynamic URL
>    - `OkHttpClient().newCall(new Request.Builder().url(url)...)`
>    - `RestTemplate.getForObject(url, ...)`, `RestTemplate.getForEntity(url, ...)`
>    - `WebClient.get().uri(url)`, `WebClient.create(url)`
>    - `Apache HttpClient`: `httpClient.execute(new HttpGet(url))`
>
> 9. **Go HTTP clients and network dials**:
>    - `http.Get(url)`, `http.Post(url, ...)`, `http.NewRequest("GET", url, ...)`
>    - `net.Dial("tcp", addr)`, `net.DialTCP(...)`, `net.DialTimeout("tcp", addr, ...)`
>    - `net.LookupHost(hostname)`, `net.LookupAddr(addr)`, `net.ResolveIPAddr(...)`
>    - `net.ResolveTCPAddr("tcp", addr)`
>
> 10. **C# / .NET HTTP clients**:
>     - `HttpClient.GetAsync(url)`, `HttpClient.PostAsync(url, ...)`, `HttpClient.SendAsync(request)`
>     - `WebRequest.Create(url)`, `WebClient.DownloadString(url)`, `WebClient.DownloadData(url)`
>     - `HttpWebRequest` with a dynamic URL
>
> 11. **Shell-out to network tools** (via subprocess, exec, system, etc.):
>     - `subprocess.run(["curl", url, ...])`, `subprocess.Popen(["wget", url, ...])`
>     - `os.system("curl " + url)`, `exec("wget " + url)`
>     - Any `curl`, `wget`, `nc`, `ncat`, `nmap` invocation where the target is a variable
>
> 12. **Document/media processors that fetch remote resources**:
>     - ImageMagick `convert`, `identify` on a URL
>     - LibreOffice / unoconv on remote documents
>     - FFmpeg on remote streams
>     - PDF generators (wkhtmltopdf, Puppeteer, Playwright) on remote HTML/URLs
>     - DOCX/XLSX renderers that resolve external images/stylesheets
>
> **What to skip** (these are safe — do not flag):
> - Calls where the entire URL and hostname are fully hardcoded string literals with no dynamic parts: `requests.get("https://api.example.com/data")`
> - Internal loopback connections to `localhost` or `127.0.0.1` that are clearly part of service-to-service architecture (e.g., connecting to a local queue) — flag these if the address is dynamic
>
> **Output format** — write to `{{ REPORTS_ROOT }}/03_recon.md`:
>
> ```markdown
> # SSRF Recon: [Project Name]
>
> ## Summary
> Found [N] outbound network call sites.
>
> ## Outbound Call Sites
>
> ### 1. [Descriptive name — e.g., "HTTP GET in webhook dispatcher"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [function name or route]
> - **Call type**: [HTTP GET / HTTP POST / TCP dial / DNS lookup / subprocess curl / etc.]
> - **Library / method**: [requests.get / fetch / http.Get / curl_exec / etc.]
> - **Destination argument**: `var_name` or `url_expression` — [brief note, e.g., "assembled from query param" or "partially hardcoded path with variable host"]
> - **Code snippet**:
>   ```
>   [the outbound call and the lines immediately before it that construct the destination]
>   ```
>
> [Repeat for each site]
> ```

### After Phase 1: Check for Candidates Before Proceeding
[ref: #ssrf-phase1-gate]

After Phase 1 completes, read `{{ REPORTS_ROOT }}/03_recon.md`. If the recon found **zero outbound call sites** (the summary reports "Found 0" or the "Outbound Call Sites" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/03_ssrf.md` and stop:

```markdown
# SSRF Analysis Results

No vulnerabilities found.
```

Only proceed to Phase 2 if Phase 1 found at least one outbound call site.

### Phase 2: Verify — Trace User Input to Outbound Call Sites (Batched)
[ref: #ssrf-phase2-verify]

After Phase 1 completes, read `{{ REPORTS_ROOT }}/03_recon.md` and split the outbound call sites into **batches of up to 3 sites each**. Launch **one subagent per batch in parallel**. Each subagent traces taint only for its assigned sites and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/03_recon.md` and count the numbered site sections (### 1., ### 2., etc.) under "Outbound Call Sites".
2. Divide them into batches of up to 3. For example, 8 sites → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those site sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sites.
5. Each subagent writes to `{{ REPORTS_ROOT }}/03_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project uses Node.js with fetch/axios, include only the "Node.js — fetch / axios" and "Node.js — http.request" examples. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned outbound network call site, determine whether a user-supplied value controls or influences the destination (URL, host, path, port, or scheme). Our goal is to find SSRF vulnerabilities. Write results to `{{ REPORTS_ROOT }}/03_batch_[N].md`.
>
> **Your assigned outbound call sites** (from the recon phase):
>
> [Paste the full text of the assigned site sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand entry points, middleware, and how data flows through the application.
>
> **SSRF reference — what to look for**:
>
> SSRF occurs when user-controlled input reaches the destination argument of a server-side outbound network call without an effective allowlist on where the server may connect.
>
> **What SSRF is NOT** — do not flag these as SSRF:
> - **Open redirects**: HTTP 302 to a user URL — client-side redirect, not a server-side request
> - **XSS via URL**: User URL rendered in HTML without escaping — XSS
> - **IDOR**: Object ID tampering — separate class
> - **Fully hardcoded outbound URLs** with no user influence — not SSRF
>
> **For each outbound call site, trace the destination argument(s) backwards to their origin**:
>
> 1. **Direct user input** — the destination is assigned directly from a request source with no transformation:
>    - HTTP query params: `request.GET.get('url')`, `req.query.url`, `params[:url]`, `$_GET['url']`, `c.Query("url")`
>    - Request body / JSON fields: `request.json['webhook_url']`, `req.body.target`, `params[:source]`
>    - Path parameters: `req.params.host`, `params[:endpoint]`
>    - HTTP headers: `request.headers.get('X-Forwarded-For')`, `req.headers['destination']`
>    - Cookies: `req.cookies.redirect_url`
>
> 2. **Indirect / assembled destination** — the URL is built by concatenating a hardcoded prefix with a user-supplied suffix or path:
>    - `"https://example.com/" + user_path` — may still be exploitable via path traversal or scheme injection depending on the HTTP client
>    - `base_url + user_query` — user controls the query string, potentially injectable
>    - Flag these as Likely Vulnerable and note which portion is user-controlled
>
> 3. **User input stored and later fetched** — the destination was previously saved from user input (e.g., a stored webhook URL) and is now retrieved from the database to make a request:
>    - Find where the stored value was written — was it accepted from user input without allowlist validation at write time?
>    - Was any validation applied at read time before the request?
>    - If validation happened only at write time, check whether the stored value can be updated later without re-validation.
>
> 4. **Server-side / hardcoded value** — the destination comes from config, an environment variable, a hardcoded constant, or server-side logic with no user influence — this site is NOT exploitable.
>
> **For each call site, also check for mitigations**:
> - **Strict allowlist of hosts/prefixes**: A hardcoded set of permitted hostnames or URL prefixes that the destination is validated against before the request is made — this is an effective mitigation. Mark as Not Vulnerable.
> - **Scheme-only restriction** (e.g., only allow `https://`): Partial mitigation — reduces impact but does not prevent SSRF to arbitrary HTTPS hosts. Still flag as Likely Vulnerable.
> - **Blocklist of private IP ranges / metadata endpoints**: `169.254.169.254`, `10.0.0.0/8`, `192.168.0.0/16`, etc. — **not** sufficient. Bypassable via DNS rebinding, alternate IP representations, and redirect chains. Flag as Likely Vulnerable.
> - **DNS resolution + IP check** (resolve hostname first, then check resolved IP against blocklist): Stronger than a pure blocklist, but still susceptible to DNS rebinding between the check and the request (TOCTOU). Flag as Likely Vulnerable unless the same resolved IP is explicitly pinned for the request.
> - **Network isolation / no egress to metadata or internal ranges**: Strong compensating control. If proven (e.g., dedicated fetcher subnet, firewall rules), mark as Not Vulnerable or note the control.
> - **Disabled redirects**: Positive control, but insufficient alone if the original URL is still attacker-controlled. Combine with host allowlist for effective mitigation.
>
> **Vulnerable vs. secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Vulnerable**: User input demonstrably reaches the outbound request destination with no effective mitigation (no allowlist or only a blocklist/scheme check).
> - **Likely Vulnerable**: User input probably reaches the destination (indirect flow or partial construction), or only weak mitigation is present (blocklist, scheme-only check, partial URL prefix).
> - **Not Vulnerable**: The destination is fully server-side, OR a strict host/prefix allowlist is enforced before the request, OR the fetcher is provably network-isolated from internal/metadata endpoints.
> - **Needs Manual Review**: Cannot determine the destination's origin with confidence (opaque helpers, complex conditional flows, or external libraries that resolve the URL).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/03_batch_[N].md`:
>
> ```markdown
> # SSRF Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Issue**: [e.g., "HTTP query param `url` flows directly into requests.get()"]
> - **Taint trace**: [Step-by-step from entry point to the call site — e.g., "request.args.get('url') → target_url → requests.get(target_url)"]
> - **Impact**: [What an attacker can do — access cloud metadata at 169.254.169.254, pivot to internal services, port scan the internal network, exfiltrate data, bypass firewalls, etc.]
> - **Mitigation present**: [None / Blocklist only / Scheme check only — explain why it's insufficient]
> - **Remediation**: [Strict host allowlist, or remove user control over destination entirely]
> - **Dynamic Test**:
>   ```
>   [curl command or payload to confirm the finding.
>    Show the parameter, payload, and what to look for.
>    Example: curl "https://app.example.com/fetch?url=http://169.254.169.254/latest/meta-data/"
>    or for internal pivot: curl "https://app.example.com/fetch?url=http://internal-db:5432/"]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Issue**: [e.g., "User controls the path portion of a partially hardcoded URL" or "Stored webhook URL accepted without allowlist at write time"]
> - **Taint trace**: [Best-effort trace with the uncertain or partial-control step identified]
> - **Concern**: [Why it's still a risk — e.g., "Attacker may be able to redirect to an internal host via path traversal" or "Blocklist is bypassable via DNS rebinding"]
> - **Remediation**: [Strict allowlist or remove user control]
> - **Dynamic Test**:
>   ```
>   [payload to attempt — e.g., path traversal or DNS rebinding scenario]
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Reason**: [e.g., "URL is fully hardcoded" or "Strict host allowlist enforced before request"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Uncertainty**: [Why the destination's origin could not be determined]
> - **Suggestion**: [What to trace manually — e.g., "Follow `resolve_target()` in helpers.py to check where the URL originates"]
> ```

### Phase 3: Merge — Consolidate Batch Results
[ref: #ssrf-phase3-merge]

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/03_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/03_ssrf.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/03_batch_1.md`, `{{ REPORTS_ROOT }}/03_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary (total sites analyzed equals the number from recon / sum of assigned sites).
4. Write the merged report to `{{ REPORTS_ROOT }}/03_ssrf.md` using this format:

```markdown
# SSRF Analysis Results: [Project Name]

## Executive Summary
- Outbound call sites analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/03_ssrf.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/03_batch_*.md`).

## References
[ref: #ssrf-references]

- [OWASP API Security Top 10 2023 - API7:2023 Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/)
- [OWASP API Security Top 10 2023 - API8:2023 Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP API Security Top 10 2023 - API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)
- [OWASP Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [CWE-918: Server-Side Request Forgery (SSRF)](https://cwe.mitre.org/data/definitions/918.html)
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- [CWE-319: Cleartext Transmission of Sensitive Information](https://cwe.mitre.org/data/definitions/319.html)
- [CWE-444: Inconsistent Interpretation of HTTP Requests](https://cwe.mitre.org/data/definitions/444.html)
- [Snyk — URL confusion vulnerabilities](https://snyk.io/blog/url-confusion-vulnerabilities/)

***

## Important Reminders
[ref: #ssrf-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 outbound call sites per subagent**. If there are 1-3 sites total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned sites' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **Phase 1 is purely structural**: flag any call site where the destination argument is dynamic (a variable, expression, or assembled string), regardless of whether user input flows there. Do not attempt to trace user input in Phase 1 — that is Phase 2's job.
- **Phase 2 is purely taint analysis**: for each site in its batch, trace the destination argument back to its origin. If it comes from a user-controlled source without an effective allowlist, the site is a real vulnerability.
- **Blocklists are not mitigations**: IP blocklists for private ranges and cloud metadata endpoints are easily bypassed. Always classify such sites as Vulnerable or Likely Vulnerable, not as safe.
- **Partial URL control is still dangerous**: even if the attacker only controls the path or query string portion of the URL, flag it as Likely Vulnerable — depending on the HTTP client behavior, redirect following, and target service, partial control can be enough.
- **Stored destinations are tainted**: if a URL or hostname was accepted from user input at write time and is later used for an outbound request, trace the write-time acceptance. Lack of allowlist validation at write time makes it SSRF.
- **Subprocess curl/wget is SSRF too**: shell-outs that run `curl` or `wget` with a user-supplied URL are just as dangerous as HTTP client calls. Check for these, especially in image-processing, import, or download features.
- **Document and media processors can be SSRF vectors**: ImageMagick, LibreOffice, FFmpeg, wkhtmltopdf, Puppeteer, and DOCX renderers can fetch remote resources. Flag user-supplied inputs to these tools.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- DNS rebinding note: for findings where only a DNS-resolution-then-blocklist check is present, note the TOCTOU window explicitly in the finding — this is a known bypass technique.
- **Do NOT modify project source code. This is a read-only audit.**
- Preserve intermediate files (`{{ REPORTS_ROOT }}/03_recon.md` and all `{{ REPORTS_ROOT }}/03_batch_*.md`) until the final consolidated report (`{{ REPORTS_ROOT }}/report.md`) has been written. Delete them only after `references/99-report.md` has finished.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/03_recon.md` and all `{{ REPORTS_ROOT }}/03_batch_*.md` files after the final `{{ REPORTS_ROOT }}/report.md` is written.
