---
subject: "Unsafe consumption of APIs detection reference for SAST subagents; three-phase detection prompt, `API10:2023` definition with IS/IS-NOT boundaries, vulnerability conditions, prevention patterns, three OWASP attack scenarios, per-stack recipes incl. LLM API output and `RestTemplate` maintenance note, execution with zero-candidate early-exit gate, prevention guidance, references incl. `LLM01:2025` `LLM05:2025`, operational reminders."
index:
  - anchor: unsafeapiconsumption-detection
    what: "Focused unsafe-API-consumption detection role using the three-phase subagent approach — recon for outbound third-party API consumers, incoming webhooks, and supply-chain integrations, batched verify of third-party data flows, merge — gated on the architecture report."
    problem: "Codebase and integrations need systematic sweep of every outbound call, webhook endpoint, and registry interaction for over-trust, yet unstructured hunting misses stored-then-reused third-party values and buries reviewers in unverified integration candidates; detection orchestration, trust audit, discovery discipline, candidate flood, coverage goal, methodical triage, shadow consumers."
    use_when: "Unsafe-consumption scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-phase detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual knowledge of third-party trust risks is needed, not execution."
    expected: "Confirmed unsafe-integration findings consolidated into one module report with false positives filtered."
  - anchor: unsafeapiconsumption-what-is
    what: "`API10:2023` definition of unsafe API consumption with OWASP risk table, core trust patterns, IS/IS-NOT boundaries against SSRF and open redirects, vulnerability conditions, and seven prevention patterns incl. TLS enforcement, redirect allowlists, schema validation, parameterized sinks, timeouts, provider vetting, webhook signature checks."
    problem: "Reviewer cannot tell whether integration behavior counts as unsafe consumption without crisp boundaries, so SSRF-shaped calls get flagged here while blind redirect replay and unvalidated enrichment data slip past triage; definition scope, boundary rules, inclusion criteria, exclusion list, classification accuracy, trust assumptions, taxonomy anchor, dominant-issue judgment."
    use_when: "Deciding whether observed integration behavior belongs to this risk class; testing the five OWASP-listed weakness conditions against call-site reality; confirming whether TLS, redirect, validation, or timeout safeguards already protect the consumer."
    avoid_when: "User-controlled request destinations are the question — route to `03-ssrf.md`; direct injection from user input belongs to `02-sqli.md`; auth gaps on third-party endpoints belong to `10-missingauth.md`; dependency-tree version risk belongs to `23-dependencies.md`."
    expected: "Integration behavior classified against `API10:2023` with explicit boundary reasoning; dominant issue named when SSRF and consumption overlap."
  - anchor: unsafeapiconsumption-attack-scenarios
    what: "Three canonical `API10:2023` attack scenarios that dynamic tests must reproduce: malicious third-party business address carrying SQLi into local database, `308 Permanent Redirect` replaying sensitive POST body to attacker host, and malicious repository name executed as SQL."
    problem: "Findings feel abstract without canonical exploitation narratives, so reports describe misconfigurations developers shrug off while real exfiltration paths through redirects and stored third-party payloads go unproven; scenario canon, exploit chain, stakeholder impact, proof deficit, official examples, report credibility."
    use_when: "Building dynamic-test reproductions for confirmed findings; mapping observed weakness to one of the official narratives; explaining impact in report prose."
    avoid_when: "Mechanics of execution phases are the need — see the execution card; stack-specific code idioms wanted — see the examples card; user-controlled destination semantics belong to `03-ssrf.md`."
    expected: "Each confirmed finding anchors to its matching canonical scenario with reproducible attack chain described."
  - anchor: unsafeapiconsumption-vulnerable-vs-secure-examples
    what: "Per-stack vulnerable/secure recipe pairs — Python `requests` incl. sensitive-POST redirect replay, repo-name SQLi, and LLM API output handling, Node.js `fetch`/`axios`, Java Spring `RestTemplate`/`WebClient` with maintenance-mode currency note, Go `net/http`, C# `HttpClient`, Ruby `Net::HTTP`/`Faraday`, PHP `curl_exec`/`Guzzle` — covering TLS flags, redirect control, timeouts, schema validation, parameterized sinks."
    problem: "Consumption weaknesses look different per HTTP client, and generic trust rules miss stack-specific redirect defaults, certificate-verification switches, and timeout idioms that decide exploitability; stack recipes, secure idioms, precise detection, pattern matching, framework diversity, api quirks, handler review, exploit signal."
    use_when: "Target project uses one of the covered stacks; reviewing outbound call sites, webhook handlers, or registry integrations for concrete idioms; verify batch subagent needs `[TECH-STACK EXAMPLES]` selection."
    avoid_when: "Conceptual scope boundaries are the question — see the `API10:2023` definition card; direct user-input injection semantics belong to `02-sqli.md`; dependency-tree and typosquatting risk belongs to `23-dependencies.md`."
    expected: "Stack-specific unsafe integrations confirmed with matching secure counterpart; hardened call sites verified per client library."
  - anchor: unsafeapiconsumption-execution
    what: "Three-phase execution: recon discovering outbound consumers, webhooks, and supply-chain interactions with zero-candidate early-exit gate writing an empty-results report, batched verify in groups of three tracing third-party data flows, orchestrator merge with intermediate-file cleanup."
    problem: "Detection work without orchestration duplicates effort, loses batch boundaries, skips early exits, and merges verdicts inconsistently across recon and verify artifacts; execution model, phase overview, subagent orchestration, batch discipline, context passing, workflow entry, staging, dispatch plan, consolidation, handoff clarity."
    use_when: "Starting the unsafe-consumption scan execution; dispatching recon, verify batches, or merge; reviewing any phase output or the early-exit decision."
    avoid_when: "Conceptual definitions are the need — see the `API10:2023` card; concrete client idioms wanted — see the examples card."
    expected: "All phases run with shared architecture context into one consolidated report; intermediates deleted."
  - anchor: unsafeapiconsumption-prevention-guidance
    what: "Layered defense checklist: provider security-posture assessment, TLS everywhere with certificate validation, strict schema validation and output encoding, redirect allowlisting, timeouts with response-size caps and bounded retries, no raw response forwarding, webhook signature plus idempotency verification, third-party identifier validation."
    problem: "Remediation advice scattered across guides leaves gaps, and one missed control lets blind redirects, cleartext transports, or unvalidated payloads persist after fixes ship; remediation checklist, defense layers, control mapping, gap elimination, hardening steps, closure guarantee, mitigation breadth, fix completeness."
    use_when: "Writing remediation sections of findings; reviewing whether deployed defenses form complete consumption-safety coverage."
    avoid_when: "Detection mechanics are the question — see execution and example cards; dependency-upgrade guidance belongs to `23-dependencies.md`; SSRF-specific egress controls belong to `03-ssrf.md`."
    expected: "Each finding closes with layered controls that keep every third-party interaction encrypted, validated, bounded, and verified."
  - anchor: unsafeapiconsumption-references
    what: "External link list: OWASP `API10:2023` risk page, web-service, injection, input-validation, transport, and unvalidated-redirect cheat sheets, `CWE-20` `CWE-78` `CWE-200` `CWE-319` `CWE-345` `CWE-400` `CWE-502` `CWE-601`, plus `LLM01:2025` prompt injection and `LLM05:2025` improper output handling."
    problem: "Reports need authoritative follow-up sources beyond distilled file content when deeper verification, LLM-output risk detail, or canonical citation is required; further reading, external canon, deep dives, primary material, cited works, weakness identifiers, reference integrity."
    use_when: "Primary sources or extended material is needed; findings require links to OWASP, CWE, or LLM-risk taxonomy entries."
    avoid_when: "Recipe or orchestration needs route elsewhere — this list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
  - anchor: unsafeapiconsumption-important-reminders
    what: "Closing operational reminders: phase ordering with dependency gates, three-per-batch parallel dispatch, per-batch context slicing, read-only subagent discipline, structural-only recon versus data-flow verify, blocklists not counting as mitigations, stored-data taint tracking, manual-review bias, intermediate-file cleanup."
    problem: "Modules close with inconsistent final guidance, letting unverified dismissals, sequential batch runs, or leftover recon files slip into reports and client deliverables; closing rules, quality floor, final reminders, uniform endings, wrap discipline, audit closure, leftover artifacts."
    use_when: "Finalizing the module report; checking phase sequencing, taint-tracking duties, and cleanup obligations before closing the scan."
    avoid_when: "Earlier phases are still open — finish those first; sibling-risk routing belongs to `03-ssrf.md`, `02-sqli.md`, `10-missingauth.md`, or `23-dependencies.md` cards."
    expected: "Reports close with uniform final rules applied and no leftover intermediates."
---

# Unsafe Consumption of APIs Detection

[ref: #unsafeapiconsumption-detection]

You are performing a focused security assessment to find **Unsafe Consumption of APIs** vulnerabilities in a codebase. This assessment maps to **OWASP API Security Top 10 2023 — API10:2023 Unsafe Consumption of APIs**. This skill uses a three-phase approach with subagents: **recon** (find all outbound third-party API consumers, incoming webhooks, and supply-chain integrations), **batched verify** (trace how third-party data is consumed, in parallel batches of 3), and **merge** (consolidate batch reports into one file).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

***

## What is Unsafe Consumption of APIs
[ref: #unsafeapiconsumption-what-is]

Applications increasingly rely on third-party APIs for data enrichment, identity, payments, storage, analytics, and more. **Unsafe Consumption of APIs** occurs when the application trusts those integrations too much: it sends sensitive data over unencrypted channels, follows redirects blindly, fails to validate or sanitize data received from the third party, and does not impose timeouts or resource limits on the interaction.

| Threat agents / Attack vectors | Security Weakness | Impacts |
| - | - | - |
| API Specific : Exploitability **Easy** | Prevalence **Common** : Detectability **Average** | Technical **Severe** : Business Specific |
| Exploiting this issue requires attackers to identify and potentially compromise other APIs/services the target API integrated with. Usually, this information is not publicly available or the integrated API/service is not easily exploitable. | Developers tend to trust and not verify the endpoints that interact with external or third-party APIs, relying on weaker security requirements such as those regarding transport security, authentication/authorization, and input validation and sanitization. Attackers need to identify services the target API integrates with (data sources) and, eventually, compromise them. | The impact varies according to what the target API does with pulled data. Successful exploitation may lead to sensitive information exposure to unauthorized actors, many kinds of injections, or denial of service. |

The core patterns:

- *Outbound calls to third-party APIs without TLS* (`http://`, `verify=False`, disabled certificate validation).
- *Blindly following redirects* returned by third-party services.
- *Using third-party data without validation or sanitization* before SQL queries, template rendering, `eval`, deserialization, downstream API calls, or direct output to clients.
- *Missing timeouts, retries, or resource limits* when interacting with third-party services.
- *Over-trusting integrated services* — treating data from known providers as safe input.
- *Incoming webhooks treated as trusted* — third parties push data to the application without signature verification, idempotency checks, or authentication.
- *Supply-chain integrations executing third-party identifiers* — package or repository names flowing into SQL, shell commands, or deserialization.
- *LLM/AI API output treated as trusted* — model responses (indirect-prompt-injection-influenced) flowing into SQL, shell commands, template rendering, or downstream API calls without validation.

### What Unsafe Consumption of APIs IS

- Calling a third-party API over `http://` or with TLS certificate validation disabled.
- Forwarding a third-party redirect (`3xx`) to a new destination without validating the `Location`.
- Inserting third-party JSON/XML/string data directly into SQL queries, command execution, template engines, `eval`, `pickle.loads`, `yaml.unsafe_load`, or XML deserialization.
- Returning raw third-party responses to clients without validation or sanitization.
- Fetching third-party data with no request/response size limits and no socket/read timeouts.
- Storing third-party data verbatim and later using it in security-sensitive operations.
- Passing third-party API responses to downstream internal APIs or microservices without re-validation.
- Consuming incoming webhooks without signature verification, replay/idempotency checks, or authentication.
- Using third-party package, repository, or artifact identifiers in SQL, shell commands, or deserialization without validation.
- Passing LLM/AI model output to SQL, shell commands, template rendering, `eval`, or downstream API calls without validation.

### What Unsafe Consumption of APIs is Not

Do not flag these:

- **SSRF**: User-controlled destination of an outbound request — that is API7:2023 Server-Side Request Forgery. Unsafe Consumption focuses on how the application interacts with *intended* third-party APIs and how their responses are handled. A single call site can be both SSRF and unsafe consumption; classify based on the dominant issue.
- **Missing authentication on a third-party endpoint**: That is an integration/configuration problem, not necessarily unsafe consumption.
- **Hardcoded, TLS-protected calls to well-known APIs whose responses are validated**: Not a vulnerability.
- **Open redirects sent to the browser**: Client-side redirects are a separate class.

### Vulnerability Conditions

The API is likely vulnerable when any of the following are true:

- It interacts with other APIs over an unencrypted channel.
- It does not properly validate and sanitize data gathered from other APIs prior to processing it or passing it to downstream components.
- It blindly follows redirections.
- It does not limit the number of resources available to process third-party services responses.
- It does not implement timeouts for interactions with third-party services.

### Patterns That Prevent Unsafe Consumption of APIs

When you see these patterns, the code is likely **not vulnerable**:

**1. TLS enforced and certificate validation enabled**
```python
response = requests.get("https://api.example.com/data")  # https, verify=True (default)
```

**2. Redirects disabled or allowlisted**
```python
response = requests.get(url, allow_redirects=False)
# OR validate the final destination against an allowlist before following redirects
```

**3. Third-party data validated before use**
```python
data = response.json()
# Schema validation, type checks, length limits, and output encoding before use
validated = AddressSchema().load(data)
```

**4. Parameterized queries / safe templating**
```python
cursor.execute("SELECT * FROM orders WHERE id = %s", (data["id"],))
```

**5. Timeouts and resource limits configured**
```python
response = requests.get(url, timeout=(connect_timeout, read_timeout))
```

**6. Security assessment of providers**
Vetting third-party API providers, reviewing their security posture, and monitoring for reported breaches or unexpected redirect behavior.

**7. Webhook signatures verified and idempotency keys used**
```python
payload = request.get_data()
sig = request.headers.get("X-Signature")
if not hmac.compare_digest(sig, hmac.new(WEBHOOK_SECRET, payload, hashlib.sha256).hexdigest()):
    abort(401)
# Process idempotency key to prevent replay
```

***

## OWASP API10:2023 Attack Scenarios
[ref: #unsafeapiconsumption-attack-scenarios]

The following scenarios from the official API10 entry must be reproducible in dynamic tests and example code.

### Scenario #1 — Malicious third-party business address (SQLi)

An API relies on a third-party service to enrich user-provided business addresses. When an address is supplied, it is sent to the third-party service and the returned data is stored in a local SQL-enabled database. Attackers store an SQLi payload in the third-party service associated with a business they created, then trick the vulnerable API into pulling that "malicious business". The SQLi payload is executed by the database, exfiltrating data to an attacker-controlled server.

**Detection target**: outbound call results are used in raw SQL/templates/eval/deserialization without validation.

### Scenario #2 — Sensitive POST body exfiltrated via 308 redirect

An API integrates with a third-party service provider to safely store sensitive user medical information:

```
POST /user/store_phr_record
{
  "genome": "ACTAGTAG__TTGADDAAIICCTT…"
}
```

The third-party API is compromised and starts responding with:

```
HTTP/1.1 308 Permanent Redirect
Location: https://attacker.com/
```

Because the API blindly follows redirects, it repeats the exact same request — including the sensitive request body — to the attacker's server.

**Detection target**: redirect following is enabled without an allowlist; the request body contains PII/sensitive data.

### Scenario #3 — Malicious repository/package name

An attacker prepares a git repository named `'; drop db;--`. When the attacked application integrates with the malicious repository, the repository name is used in an SQL query as if it were safe input, causing SQL injection.

**Detection target**: third-party identifiers (repo names, package names, artifact names) flow into SQL, commands, templates, or deserialization sinks.

***

## Vulnerable vs. Secure Examples
[ref: #unsafeapiconsumption-vulnerable-vs-secure-examples]

### Python — requests

```python
# VULNERABLE: unencrypted endpoint, no timeout, no validation of response
@app.route('/enrich')
def enrich():
    user_input = request.args.get('address')
    r = requests.get(f"http://api.geo.example.com/lookup?q={user_input}")
    data = r.json()
    cursor.execute(f"INSERT INTO addresses VALUES ('{data['city']}')")
    return data

# SECURE: TLS, timeout, schema validation, parameterized query
@app.route('/enrich')
def enrich():
    user_input = request.args.get('address')
    r = requests.get(
        "https://api.geo.example.com/lookup",
        params={"q": user_input},
        timeout=(3, 10),
        allow_redirects=False,
    )
    r.raise_for_status()
    data = AddressSchema().load(r.json())
    cursor.execute("INSERT INTO addresses (city) VALUES (%s)", (data.city,))
    return {"city": data.city}
```

### Python — sensitive POST body forwarded blindly

```python
# VULNERABLE: follows redirects, replays sensitive body
def store_phr_record(user_id, genome):
    r = requests.post(
        "https://third-party-health.example.com/store",
        json={"user_id": user_id, "genome": genome},
        allow_redirects=True,
    )
    return r.json()

# SECURE: no automatic redirect follow; validate Location before resending
def store_phr_record(user_id, genome):
    r = requests.post(
        "https://third-party-health.example.com/store",
        json={"user_id": user_id, "genome": genome},
        allow_redirects=False,
    )
    if r.is_redirect:
        allowed = is_redirect_allowed(r.headers["Location"])
        if not allowed:
            raise UnsafeRedirectError(r.headers["Location"])
        r = requests.post(
            r.headers["Location"],
            json={"user_id": user_id, "genome": genome},
            allow_redirects=False,
        )
    return r.json()
```

### Python — malicious repo name reaching SQL

```python
# VULNERABLE: repo name from third party used in raw SQL
def sync_repo(owner, repo_name):
    clone_repo(owner, repo_name)
    cursor.execute(f"INSERT INTO repos (name) VALUES ('{repo_name}')")

# SECURE: repo name validated/escaped and parameterized
def sync_repo(owner, repo_name):
    if not REPO_NAME_REGEX.match(repo_name):
        raise ValueError("invalid repo name")
    clone_repo(owner, repo_name)
    cursor.execute("INSERT INTO repos (name) VALUES (?)", (repo_name,))
```

### Python — LLM API output

```python
# VULNERABLE: LLM response (attacker-influenceable via indirect prompt injection) reaching SQL and shell
@app.route('/summarize')
def summarize():
    text = request.args.get('text')
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Extract the city from: {text}"}],
    )
    city = completion.choices[0].message.content
    cursor.execute(f"INSERT INTO addresses (city) VALUES ('{city}')")
    subprocess.run(f"notify-send '{city}'", shell=True)
    return {"city": city}

# SECURE: JSON-mode output validated against a strict schema, parameterized sinks, dangerous actions gated
@app.route('/summarize')
def summarize():
    text = request.args.get('text')
    completion = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Extract the city from: {text}"}],
        response_format={"type": "json_object"},
    )
    result = CityExtraction.model_validate_json(completion.choices[0].message.content)
    if result.city not in KNOWN_CITIES:
        raise ValueError("city not in allowlist")
    cursor.execute("INSERT INTO addresses (city) VALUES (%s)", (result.city,))
    return {"city": result.city}
```

### Node.js — fetch / axios

```javascript
// VULNERABLE: follows redirects, no timeout, trusts third-party JSON
app.get('/profile', async (req, res) => {
  const { data } = await axios.get(
    `http://payments.example.com/user/${req.user.id}`,
    { maxRedirects: 5 }
  );
  res.render('profile', data);  // third-party data straight into template
});

// SECURE: https, no redirects, schema validation, safe template use
app.get('/profile', async (req, res) => {
  const { data } = await axios.get(
    `https://payments.example.com/user/${req.user.id}`,
    {
      maxRedirects: 0,
      timeout: 5000,
      maxBodyLength: 10000,
    }
  );
  const profile = ProfileSchema.validate(data);
  res.render('profile', { city: escapeHtml(profile.city) });
});
```

### Java — Spring / RestTemplate / WebClient

```java
// VULNERABLE: http URL, no timeout, raw response used in SQL
@GetMapping("/enrich")
public String enrich(@RequestParam String address) {
    RestTemplate rt = new RestTemplate();
    String city = rt.getForObject(
        "http://api.geo.example.com/lookup?q=" + address, JsonNode.class)
        .get("city").asText();
    jdbcTemplate.execute("INSERT INTO addresses (city) VALUES ('" + city + "')");
    return city;
}

// NOTE: RestTemplate is in maintenance mode (formal @Deprecated planned for Spring 7.1); prefer RestClient (sync, 6.1+) or WebClient (reactive) for new code — RestTemplate stays a detection target in existing codebases
// SECURE: https, timeouts, no redirect follow, validated response
@GetMapping("/enrich")
public ResponseEntity<String> enrich(@RequestParam String address) {
    SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
    factory.setConnectTimeout(3000);
    factory.setReadTimeout(10000);
    RestTemplate rt = new RestTemplate(factory);
    rt.setErrorHandler(new DefaultResponseErrorHandler());

    URI uri = UriComponentsBuilder
        .fromUriString("https://api.geo.example.com/lookup")
        .queryParam("q", address)
        .build().toUri();

    ResponseEntity<JsonNode> resp = rt.exchange(
        new RequestEntity<>(HttpMethod.GET, uri),
        JsonNode.class
    );

    AddressDto dto = addressValidator.validate(resp.getBody());
    jdbcTemplate.update("INSERT INTO addresses (city) VALUES (?)", dto.getCity());
    return ResponseEntity.ok(dto.getCity());
}
```

### Go — net/http

```go
// VULNERABLE: no timeout, disabled TLS verification, follows redirects
func enrich(address string) error {
    tr := &http.Transport{
        TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
    }
    client := &http.Client{Transport: tr}
    resp, err := client.Get("http://api.geo.example.com/lookup?q=" + address)
    if err != nil { return err }
    defer resp.Body.Close()
    // ... use resp.Body in SQL without validation
    return nil
}

// SECURE: timeout, TLS verification, redirect control
func enrich(address string) error {
    client := &http.Client{
        Timeout: 10 * time.Second,
        CheckRedirect: func(req *http.Request, via []*http.Request) error {
            return http.ErrUseLastResponse  // disable automatic redirect follow
        },
    }
    resp, err := client.Get("https://api.geo.example.com/lookup?q=" + url.QueryEscape(address))
    if err != nil { return err }
    defer resp.Body.Close()
    // validate response against schema before use
    return nil
}
```

### C# — HttpClient

```csharp
// VULNERABLE: auto redirect, no cert revocation check, no timeout
using var client = new HttpClient();
var response = await client.GetAsync("http://api.geo.example.com/lookup?q=" + address);
var json = await response.Content.ReadAsStringAsync();
// json inserted into SQL without validation

// SECURE: manual redirect validation, cert validation, timeout
var handler = new HttpClientHandler
{
    AllowAutoRedirect = false,
    CheckCertificateRevocationList = true,
};
using var client = new HttpClient(handler)
{
    Timeout = TimeSpan.FromSeconds(10),
};
var response = await client.GetAsync("https://api.geo.example.com/lookup?q=" + Uri.EscapeDataString(address));
if ((int)response.StatusCode >= 300 && (int)response.StatusCode < 400)
{
    var location = response.Headers.Location?.ToString();
    if (!IsRedirectAllowed(location)) throw new UnsafeRedirectException();
}
// validate response before use
```

### Ruby — Net::HTTP / Faraday

```ruby
# VULNERABLE: no TLS verification, no timeout, follows redirects
uri = URI("http://api.geo.example.com/lookup?q=#{address}")
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = false
http.verify_mode = OpenSSL::SSL::VERIFY_NONE
response = http.get(uri.request_uri)
city = JSON.parse(response.body)["city"]
ActiveRecord::Base.connection.execute("INSERT INTO addresses (city) VALUES ('#{city}')")

# SECURE: TLS verification, timeout, no automatic redirect follow
uri = URI("https://api.geo.example.com/lookup?q=#{URI.encode_www_form_component(address)}")
http = Net::HTTP.start(
  uri.host, uri.port,
  use_ssl: true,
  verify_mode: OpenSSL::SSL::VERIFY_PEER,
  read_timeout: 10,
  open_timeout: 3,
)
request = Net::HTTP::Get.new(uri)
response = http.request(request)
raise "redirect not allowed" if response.is_a?(Net::HTTPRedirection)
validated = AddressSchema.validate!(JSON.parse(response.body))
ActiveRecord::Base.connection.execute("INSERT INTO addresses (city) VALUES (?)", validated.city)
```

### PHP — curl_exec / Guzzle

```php
<?php
// VULNERABLE: disabled peer verification, follows redirects, no timeout
$ch = curl_init("http://api.geo.example.com/lookup?q=" . urlencode($address));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
$response = curl_exec($ch);
$data = json_decode($response, true);
mysqli_query($conn, "INSERT INTO addresses (city) VALUES ('{$data['city']}')");

// SECURE: TLS verification, no automatic redirect, timeout
$ch = curl_init("https://api.geo.example.com/lookup?q=" . urlencode($address));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 3);
$response = curl_exec($ch);
if (curl_errno($ch)) { throw new Exception(curl_error($ch)); }
$data = AddressSchema::validate(json_decode($response, true));
$stmt = $conn->prepare("INSERT INTO addresses (city) VALUES (?)");
$stmt->bind_param("s", $data->city);
$stmt->execute();
```

***

## Execution
[ref: #unsafeapiconsumption-execution]

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Recon — Find Third-Party API Consumers

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where the application consumes a third-party API or external service, receives incoming webhooks, or interacts with package/artifact registries. Record the call site, transport configuration, and how the response is used. Write results to `{{ REPORTS_ROOT }}/19_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, HTTP client libraries, integrations, webhook endpoints, and any data-enrichment or CI/CD components.
>
> **What to search for — third-party API consumers**:
>
> 1. **Outbound HTTP client calls** to external domains (not internal service mesh/localhost):
>    - Python: `requests.get/post/put`, `httpx`, `aiohttp`, `urllib`, LLM SDKs (`openai`, `anthropic`, `litellm`)
>    - Node.js: `fetch`, `axios.*`, `http.request`, `https.request`, `got`, `superagent`
>    - Java: `RestTemplate`, `RestClient`, `WebClient`, `OkHttp`, `HttpURLConnection`, `Apache HttpClient`
>    - Go: `net/http.Get/Post`, `resty`
>    - C#: `HttpClient`, `WebRequest`, `WebClient`
>    - Ruby: `Net::HTTP`, `Faraday`, `HTTParty`
>    - PHP: `curl_exec`, `Guzzle`, `file_get_contents` with remote URL
>
> 2. **Transport security configuration**:
>    - URLs using `http://` instead of `https://`
>    - `verify=False` (Python requests/httpx)
>    - `rejectUnauthorized: false` (Node.js)
>    - Disabled certificate pinning or custom `TrustManager` that accepts all certificates (Java)
>    - `CURLOPT_SSL_VERIFYPEER => false` (PHP cURL)
>    - `InsecureSkipVerify: true` (Go)
>
> 3. **Redirect handling**:
>    - `allow_redirects=True` (Python default) without destination validation
>    - `maxRedirects` > 0 without allowlist (Node.js)
>    - Default redirect following in `RestTemplate`/`WebClient` without validation
>    - `CURLOPT_FOLLOWLOCATION => true` (PHP) without allowlist
>    - `AllowAutoRedirect = true` (C#) without validation
>
> 4. **Timeout and resource limits**:
>    - Missing `timeout` argument
>    - Missing `maxBodyLength` / `maxContentLength`
>    - Missing connection/read timeouts in Spring `ClientHttpRequestFactory`
>    - Missing `http.Client.Timeout` (Go)
>    - Missing `HttpClient.Timeout` (C#)
>
> 5. **Consumption of third-party responses**:
>    - Passed to SQL/query builders (string concatenation, `.format`, f-strings, template literals)
>    - Passed to template engines (`render`, `render_template`, `res.render`)
>    - Passed to `eval`, `exec`, `Function`, `setTimeout`/`setInterval` with string
>    - Passed to deserialization: `pickle.loads`, `yaml.unsafe_load`, `ObjectInputStream.readObject`, `JSON.parse` → `new Function`, `Marshal.load`, `unserialize`
>    - Passed to downstream API calls or internal microservices without re-validation
>    - LLM/AI model output passed to SQL, shell commands, templates, `eval`, or downstream APIs
>    - Returned raw to the client
>
> 6. **Third-party data stored and later used**:
>    - Values from external APIs saved to databases, caches, or files and later consumed in security-sensitive operations.
>
> **What to search for — incoming webhooks**:
>
> 1. **Webhook endpoints** accepting POST/PUT/PATCH from third parties (Stripe, GitHub, Twilio, etc.).
> 2. **Missing signature verification**:
>    - No `stripe-signature`, `X-Hub-Signature-256`, `X-Twilio-Signature`, or equivalent header check.
>    - No HMAC comparison using a shared secret.
> 3. **Replay / idempotency issues**:
>    - No idempotency key tracking (`Idempotency-Key`, `X-Idempotency-Key`).
>    - No timestamp/nonce validation allowing old events to be replayed.
> 4. **Webhook endpoints without authentication**:
>    - Publicly exposed routes that accept webhook payloads with only source-IP trust or no authentication.
> 5. **Trusting webhook metadata for security decisions**:
>    - Using `event_type`, `action`, or other payload metadata to skip authentication/authorization.
> 6. **Webhook payloads reaching dangerous sinks**:
>    - Webhook body inserted into SQL/templates/eval/deserialization.
>    - Webhook payload passed to `os.system`, `exec`, `eval`, or shell commands.
>
> **What to search for — supply-chain and package-manager API interactions**:
>
> 1. **Registry/client calls**:
>    - `npm install`, `pip install`, `gem install`, `cargo install`, `nuget install` or library equivalents driven by user/third-party input.
>    - HTTP clients calling npm, PyPI, RubyGems, Cargo, NuGet, or private artifact registry APIs.
> 2. **Git-clone integrations**:
>    - `git clone <user_input>` or library equivalent.
>    - Repository URL/name from a third-party API used in `git` commands.
> 3. **CI/CD API calls**:
>    - Build parameters from third-party APIs or webhooks reaching shell commands (`os.system`, `exec`, backticks).
> 4. **Artifact repository downloads**:
>    - Downloaded blobs deserialized with `pickle.load`, `ObjectInputStream`, `Marshal.load`, `yaml.unsafe_load`, etc.
> 5. **Typosquatting / dependency confusion signals**:
>    - Package names in `package.json`, `requirements.txt`, `Cargo.toml`, `Gemfile`, `*.csproj` that are close to well-known package names but not the canonical name.
>
> **What to skip**:
> - Internal service-to-service calls inside the same trust boundary (unless they cross unencrypted channels or follow redirects).
> - Fully hardcoded, HTTPS-only calls whose responses are validated before use and that have timeouts.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/19_recon.md`:
>
> ```markdown
> # Unsafe Consumption of APIs Recon: [Project Name]
>
> ## Summary
> Found [N] third-party API consumers.
>
> ## Third-Party API Consumers
>
> ### 1. [Descriptive name — e.g., "Payment service lookup"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [function name or route]
> - **Library / method**: [requests.get / axios.get / RestTemplate.getForObject / etc.]
> - **Destination**: `url_expression`
> - **TLS**: [ok / http / verify disabled / certificate validation bypassed]
> - **Redirects**: [disabled / allowed without allowlist / unknown]
> - **Timeouts / limits**: [configured / missing]
> - **Response usage**: [SQL / template / eval / deserialization / downstream API / raw return / stored / validated]
> - **Code snippet**:
>   ```
>   [the outbound call and the lines immediately before/after showing configuration and response use]
>   ```
>
> [Repeat for each consumer]
>
> ## Incoming Webhooks
>
> ### 1. [Webhook name]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: [route]
> - **Signature verification**: [present / missing]
> - **Authentication**: [present / missing / ip-based only]
> - **Idempotency / replay protection**: [present / missing]
> - **Dangerous sinks reached**: [SQL / template / eval / command / deserialization / none]
> - **Code snippet**:
>   ```
>   [webhook handler and payload usage]
>   ```
>
> [Repeat for each webhook]
>
> ## Supply-Chain / Package-Manager Interactions
>
> ### 1. [Integration name]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Integration type**: [registry call / git clone / CI/CD API / artifact download / dependency declaration]
> - **Third-party identifier**: [package name / repo URL / artifact URL expression]
> - **Dangerous sink**: [SQL / command / deserialization / none]
> - **Code snippet**:
>   ```
>   [integration code]
>   ```
>
> [Repeat for each integration]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/19_recon.md`. If the recon found **zero third-party API consumers, incoming webhooks, and supply-chain interactions** (the summary reports "Found 0" or all relevant sections are empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/19_unsafeapiconsumption.md`, **delete** `{{ REPORTS_ROOT }}/19_recon.md`, and stop:

```markdown
# Unsafe Consumption of APIs Analysis Results: [Project Name]

## Executive Summary
- Candidates analyzed: 0
- Scope reviewed: [third-party API consumers, incoming webhooks, and supply-chain interactions reviewed]
- No unsafe-consumption candidates were found: no unencrypted transports, blind redirect following, missing timeouts, unverified webhooks, or unvalidated third-party data flows identified in the reviewed scope.
```

Only proceed to Phase 2 if Phase 1 found at least one candidate.

### Phase 2: Verify — Trace Third-Party Data Flows (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/19_recon.md` and split the candidates into **batches of up to 3 sites each**. Launch **one subagent per batch in parallel**. Each subagent traces data flows only for its assigned consumers and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/19_recon.md` and count the numbered consumer sections (### 1., ### 2., etc.) across all three categories (outbound consumers, incoming webhooks, supply-chain interactions).
2. Divide them into batches of up to 3. For example, 8 candidates → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those candidate sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned candidates.
5. Each subagent writes to `{{ REPORTS_ROOT }}/19_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned third-party API consumer, webhook, or supply-chain interaction, determine whether the integration is unsafe: unencrypted transport, blind redirect following, missing timeouts/limits, missing webhook verification, or third-party response data reaching dangerous sinks without validation. Write results to `{{ REPORTS_ROOT }}/19_batch_[N].md`.
>
> **Your assigned candidates** (from the recon phase):
>
> [Paste the full text of the assigned candidate sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand entry points, data flows, validation helpers, and dangerous sinks.
>
> **Unsafe Consumption of APIs reference — what to look for**:
>
> This vulnerability is about trusting third-party APIs too much. Focus on these areas:
>
> 1. **Transport security**
>    - Is the destination `http://` or `https://`?
>    - Is TLS certificate validation disabled (`verify=False`, `rejectUnauthorized: false`, permissive `TrustManager`, `InsecureSkipVerify`, `CURLOPT_SSL_VERIFYPEER => false`)?
>
> 2. **Redirect handling**
>    - Does the client follow redirects automatically?
>    - Is there an allowlist of permitted redirect destinations?
>    - Could a compromised or malicious third party redirect the request to an attacker-controlled server?
>    - For POST requests with sensitive bodies, could a 308 redirect cause the body to be replayed to an attacker?
>
> 3. **Validation and sanitization of third-party data**
>    - Is the response parsed and validated against a strict schema?
>    - Is any part of the response inserted into SQL, templates, `eval`, command execution, deserialization, or passed to downstream APIs without validation?
>    - Is LLM/AI output treated as untrusted (indirect prompt injection) before SQL, shell, template, or downstream use?
>    - Is raw response data returned to the client?
>
> 4. **Timeouts and resource limits**
>    - Are connection and read timeouts set?
>    - Are response body size limits enforced?
>    - Are retry/back-off policies bounded?
>
> 5. **Incoming webhooks**
>    - Is the webhook signature verified with a shared secret?
>    - Is there idempotency/replay protection?
>    - Is the webhook endpoint authenticated beyond source-IP trust?
>    - Is `event_type` or other metadata trusted to make security decisions?
>    - Does the payload reach SQL, templates, `eval`, command execution, or deserialization?
>
> 6. **Supply-chain integrations**
>    - Do package/repo/artifact identifiers from third parties reach SQL, shell commands, templates, or deserialization?
>    - Are downloaded artifacts verified (checksums, signatures) before deserialization or execution?
>
> **What Unsafe Consumption is NOT** — do not flag these:
> - **SSRF**: User-controlled destination of an outbound request → classify under API7:2023 SSRF unless the dominant issue is unsafe handling of an intended integration.
> - **Open redirects to the browser** → separate class.
> - **Fully validated HTTPS calls with no dangerous sinks** → not vulnerable.
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Vulnerable**: A clear unsafe pattern is present (unencrypted transport, disabled cert validation, blind redirect following, third-party data reaches a dangerous sink without validation, missing webhook verification, or missing timeouts/limits in a way that enables DoS or data exposure).
> - **Likely Vulnerable**: An unsafe pattern probably exists but the full data flow could not be confirmed (e.g., response stored in a variable and later used in a sink not visible in the immediate snippet).
> - **Not Vulnerable**: HTTPS with cert validation enabled, redirects disabled or allowlisted, response validated before use, timeouts and limits configured, webhooks verified and idempotent.
> - **Needs Manual Review**: Cannot determine the configuration or data flow with confidence (opaque helpers, external libraries, complex conditional flows).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/19_batch_[N].md`:
>
> ```markdown
> # Unsafe Consumption of APIs Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Issue**: [e.g., "Third-party JSON inserted into SQL via f-string" or "HTTP redirect following enabled with no allowlist"]
> - **Taint trace**: [Step-by-step from third-party response to the dangerous sink]
> - **Impact**: [What an attacker can do — SQL injection, XSS, data exfiltration via redirect, DoS, etc.]
> - **Mitigation present**: [None / partial — explain why insufficient]
> - **Remediation**: [Enforce TLS, validate response schema, disable/allowlist redirects, add timeouts/limits]
> - **Dynamic Test**:
>   ```
>   [curl command, payload, or step-by-step instructions to confirm the finding.
>    Example: supply a third-party response payload or use a local redirect server.]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Issue**: [What's probably unsafe]
> - **Concern**: [Why it's still a risk]
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [payload or step to attempt]
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Protection**: [e.g., "HTTPS with cert validation, redirects disabled, response validated against AddressSchema, timeouts configured"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Uncertainty**: [Why the configuration or data flow could not be determined]
> - **Suggestion**: [What to trace manually]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/19_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/19_unsafeapiconsumption.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/19_batch_1.md`, `{{ REPORTS_ROOT }}/19_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/19_unsafeapiconsumption.md` using this format:

```markdown
# Unsafe Consumption of APIs Analysis Results: [Project Name]

## Executive Summary
- Third-party API consumers, webhooks, and supply-chain interactions analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/19_unsafeapiconsumption.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/19_batch_*.md`).

***

## Prevention Guidance
[ref: #unsafeapiconsumption-prevention-guidance]

- **Assess third-party API security posture**: When evaluating service providers, assess their API security posture and monitor for incidents or unexpected behavioral changes.
- **Use TLS for all integrations**: Always prefer `https://`. Never disable certificate validation in production.
- **Validate and sanitize external data**: Treat data from third-party APIs as untrusted input. Use strict schema validation, type checks, length limits, and output encoding before using it in SQL, templates, commands, deserialization, or downstream APIs.
- **Control redirects**: Disable automatic redirect following, or maintain an allowlist of well-known locations integrated APIs may redirect to.
- **Enforce timeouts and resource limits**: Set connection and read timeouts, maximum response body sizes, and bounded retry policies to prevent denial of service.
- **Do not forward raw third-party responses**: Sanitize or transform responses before returning them to clients or storing them for later use.
- **Verify webhook signatures and use idempotency keys**: Verify HMAC signatures from webhook providers and use idempotency keys to prevent replay attacks.
- **Treat package/repo names from third parties as untrusted input**: Validate identifiers before using them in SQL, shell commands, templates, or deserialization.

***

## References
[ref: #unsafeapiconsumption-references]

- [OWASP API Security Top 10 2023 - API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)
- [OWASP Web Service Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Web_Service_Security_Cheat_Sheet.html)
- [OWASP Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)
- [OWASP Injection Flaws Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Flaws_Cheat_Sheet.html)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [OWASP Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
- [OWASP Unvalidated Redirects and Forwards Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)
- [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html)
- [CWE-319: Cleartext Transmission of Sensitive Information](https://cwe.mitre.org/data/definitions/319.html)
- [CWE-345: Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html)
- [CWE-502: Deserialization of Untrusted Data](https://cwe.mitre.org/data/definitions/502.html)
- [CWE-601: URL Redirection to Untrusted Site](https://cwe.mitre.org/data/definitions/601.html)
- [OWASP LLM Top 10 2025 — LLM01:2025 Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP LLM Top 10 2025 — LLM05:2025 Improper Output Handling](https://genai.owasp.org/llmrisk/llm05-improper-output-handling/)

***

## Important Reminders
[ref: #unsafeapiconsumption-important-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- **Subagents must NOT modify project source code.** Subagents must only write report files under `{{ REPORTS_ROOT }}` and must not edit, patch, or commit any source file in the project.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 candidates per subagent**. If there are 1-3 candidates total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned candidates' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **Phase 1 is purely structural**: flag any third-party API consumer, webhook, or supply-chain interaction, regardless of whether the response reaches a dangerous sink. Do not attempt full taint analysis in Phase 1 — that is Phase 2's job.
- **Phase 2 is purely data-flow analysis**: for each candidate in its batch, trace how the response is used and whether transport/redirect/timeout/webhook/supply-chain configuration is unsafe.
- **Blocklists are not mitigations**: IP blocklists do not fix unsafe consumption; the issue is trust in the third-party API and handling of its data.
- **Stored third-party data is tainted**: if a response value is saved and later consumed, trace the later consumption. Lack of validation at either storage or later use makes it vulnerable.
- **Subprocess curl/wget to third parties counts too**: shell-outs that fetch external data and then process it are subject to the same risks.
- **Incoming webhooks are third-party data**: a webhook payload must be validated exactly like an outbound API response before it reaches any dangerous sink.
- **Supply-chain identifiers are third-party data**: repository names, package names, and artifact URLs from external APIs must be validated before use in SQL, commands, or deserialization.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/19_recon.md` and all `{{ REPORTS_ROOT }}/19_batch_*.md` files after the final `{{ REPORTS_ROOT }}/19_unsafeapiconsumption.md` is written.
