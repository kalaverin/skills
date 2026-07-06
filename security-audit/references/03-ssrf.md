# Server-Side Request Forgery (SSRF) Detection

[ref: #ssrf-detection]

You are performing a focused security assessment to find SSRF vulnerabilities in a codebase. This assessment maps to **OWASP API Security Top 10 2023 — API7:2023 Server Side Request Forgery**. This skill uses a three-phase approach with subagents: **recon** (find all places that make outbound TCP, DNS, or HTTP requests), **batched verify** (trace whether user-supplied input reaches those call sites, in parallel batches of 3), and **merge** (consolidate batch reports into one file).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

## Table of contents

- [What is SSRF](#what-is-ssrf)
- [Vulnerable vs. Secure Examples](#vulnerable-vs-secure-examples)
- [SSRF variants, bypasses, and test cases](#ssrf-variants-bypasses-and-test-cases)
- [Execution](#execution)
- [References](#references)
- [Important Reminders](#important-reminders)

---

## What is SSRF

SSRF occurs when an attacker can cause the server to make outbound network requests to an arbitrary destination — including internal services, cloud metadata endpoints, or other external targets — by supplying or influencing the URL, hostname, IP, port, or scheme used in a server-side request.

The core pattern: *unvalidated, user-controlled input reaches the destination argument of an outbound network call.*

OWASP API7:2023 stresses that modern application concepts make SSRF both more common and more dangerous:

- **More common**: webhooks, file fetching from URLs, URL previews, custom SSO integrations, import-from-URL features, PDF renderers, image proxies, and notification channels all encourage developers to access a remote resource based on user input.
- **More dangerous**: cloud providers, Kubernetes, and Docker expose management and control channels over HTTP on predictable, well-known paths. Those channels are easy targets once an application can be coerced into making an outbound request.

### What SSRF IS

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

Do not flag these:

- **Open redirects**: Redirecting the browser (HTTP 302) to a user-supplied URL — that's a client-side redirect, not a server-side request
- **XSS via URL**: Rendering a user-supplied URL in an `<a>` tag without escaping — that's XSS
- **IDOR**: Accessing another user's data by changing an object ID — separate vulnerability class
- **Hardcoded outbound calls**: HTTP requests to fixed, fully hardcoded URLs with no user influence — not SSRF
- **Local service-to-service calls with a hardcoded localhost address**: e.g., a health-check call to `http://127.0.0.1:8080/ready` where neither host nor port is influenced by user input

### Patterns That Prevent SSRF

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

**5. URL scheme and port allowlists; disabling HTTP redirects**
Enforce an allowlist of permitted schemes (usually `https`) and ports. Disable automatic HTTP redirect following in the HTTP client, or validate any redirected destination against the same allowlist. Redirects can turn a trusted URL into an internal or attacker-controlled endpoint.

**6. URL parser confusion defenses**
Attackers bypass naive validation with alternative IP representations (`127.0.0.1`, `0177.1`, `2130706433`, `[::1]`), IDN homographs, the `@`-trick (`https://attacker.com@internal/`), open-redirect chaining, or double-parsing mismatches. Use a well-tested URL parser, validate the final parsed hostname/IP against the allowlist, and reject any URL whose parser-normalized form does not match the allowed destination.

**7. Do not forward raw third-party responses**
The response from an outbound request is treated as untrusted input. Do not stream it unchanged to the client; sanitize, validate, or transform the content before use. Returning raw responses can leak internal data or act as an open proxy.

> **Note**: IP blocklists (blocking `169.254.0.0/16`, `10.0.0.0/8`, etc.) are **not** sufficient protection — they can be bypassed via DNS rebinding, URL encoding, IPv6 notation, decimal IP representation, or redirect chains. Do not treat a blocklist as making a site safe; classify it as Likely Vulnerable.

---

## Vulnerable vs. Secure Examples

### Python — requests

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

### Node.js — fetch / axios

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

```javascript
// VULNERABLE: host and path from query string
app.get('/proxy', (req, res) => {
  const { host, path } = req.query;
  http.get({ host, path }, (proxyRes) => proxyRes.pipe(res));
});
```

### Ruby on Rails — Net::HTTP / OpenURI

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

```php
// VULNERABLE: file_get_contents with http:// wrapper and user input
$url = $_GET['source'];
$data = file_get_contents($url);  // fetches remote URL if scheme is http/https/ftp
```

### Java — Spring / OkHttp

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

---

## SSRF variants, bypasses, and test cases

Subagents should treat any feature that fetches a remote resource from user input as at least `[LIKELY VULNERABLE]` unless strict allowlisting and network isolation are proven.

### Mandatory OWASP API7 test cases

| Scenario | Attack flow | Detection target |
| --- | --- | --- |
| Profile picture from URL | `POST /api/profile/upload_picture` accepts `picture_url`; attacker sends `localhost:8080` to port-scan internally. Response time or error differentiates open/closed ports. | Any endpoint that fetches a user-supplied URL and returns or processes the response. |
| Webhook test request to cloud metadata | GraphQL `createNotificationChannel` sends a test request to attacker-supplied URL; attacker targets `http://169.254.169.254/latest/meta-data/iam/security-credentials/...` and the response is leaked. | Webhook/notification endpoints that make outbound requests and echo the response; cloud metadata endpoints accessible from the server. |
| URL preview / link expansion | Endpoint accepts a user URL, fetches it, and returns a title/image/summary. Attacker points it at `http://169.254.169.254/latest/meta-data/` or an internal service. | Link-expansion, oEmbed, or "unfurl" features. |
| Import from URL | File import, document conversion, or media processing accepts a remote URL and fetches it server-side. | Import, CSV load, PDF generation, image resize, or video transcode pipelines. |
| Custom SSO / OAuth callback | OAuth or custom SSO flow allows a user-influenced `redirect_uri` or `state` URL that is later fetched server-side. | Authentication integrations that fetch tokens or metadata from a user-supplied endpoint. |

### Bypass and variant catalog

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

Beyond the classic `169.254.169.254`, subagents should test for these metadata endpoints when the deployment environment suggests them:

| Platform | Endpoint | Exposure |
| --- | --- | --- |
| AWS EC2 / Lambda (IMDSv1/v2) | `http://169.254.169.254/latest/meta-data/` | Credentials, IAM roles, user-data, instance identity. |
| AWS ECS | `http://169.254.170.2/v2/credentials/<GUID>` | Task role credentials. |
| GCP | `http://metadata.google.internal/computeMetadata/v1/` | Project info, access tokens, service-account keys. Requires `Metadata-Flavor: Google` header. |
| Azure | `http://169.254.169.254/metadata/instance?api-version=...` | Instance metadata, identity tokens. Requires `Metadata: true` header. |
| Azure Container Instances | `http://169.254.169.254/metadata/instance` | Container instance metadata. |
| DigitalOcean | `http://169.254.169.254/metadata/v1.json` | Droplet metadata, user-data, SSH keys. |
| Alibaba Cloud (ECS) | `http://100.100.100.200/latest/meta-data/` | Instance metadata, RAM credentials. |
| Oracle Cloud (OCI) | `http://169.254.169.254/opc/v1/instance/` | Instance metadata. |
| Hetzner Cloud | `http://169.254.169.254/hetzner/v1/metadata` | Instance metadata, user-data. |
| Kubernetes | `https://kubernetes.default.svc` / `http://<service>.<namespace>` | Service account tokens, internal services. |
| Docker | `http://172.17.0.1:2375/` | Docker daemon if exposed without TLS. |
| HashiCorp Vault | `http://127.0.0.1:8200/v1/...` | Vault API if reachable from the application. |
| Local cloud-init / metadata | `http://169.254.169.254/` on many clouds | Standard link-local metadata service. |

### Blind SSRF detection techniques

When the server does not return the response body to the attacker, use these techniques to confirm SSRF:

- **Out-of-band (OOB) callbacks**: direct the target to an attacker-controlled server (e.g., Burp Collaborator, Interactsh, a private request-bin) and watch for DNS/HTTP hits. Example payload: `http://<unique>.burpcollaborator.net/` or `http://<unique>.oast.pro/`.
- **Time delays**: use payloads that cause the target database or service to sleep if the parameter is injectable into a secondary request. Example: `http://internal-service/slow-endpoint` or, for some protocols, a URL that hangs.
- **Error / differential analysis**: send a URL that should fail quickly (closed port) versus one that should succeed (open internal service); compare response times or error messages. Example: `http://localhost:22/` vs `http://localhost:8080/`.
- **DNS rebinding probes**: verify whether validation is performed only once by changing the DNS record between verification and fetch. If the application validates the URL at time T0 but fetches at T1, a DNS record swap can bypass host-based checks.
- **Protocol-specific side channels**: some internal services (Redis, Memcached, Elasticsearch, SMTP) return distinctive errors or banners that leak through generic error pages or response times.
- **Collab + redirect chains**: host a redirect on an allowed domain that points to an OOB callback or internal target. If the application follows redirects, the callback confirms the request reached the attacker-controlled chain.

### Webhook verification bypass patterns

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

SSRF findings can also represent other OWASP API 2023 risks:

- **API8:2023 Security Misconfiguration** — permissive egress rules, open redirects, weak URL-parser configuration, permissive scheme handling, unpatched HTTP clients that follow redirects by default, or inconsistent request parsing that enables request smuggling.
- **API10:2023 Unsafe Consumption of APIs** — blind forwarding of third-party responses to clients, over-trusting upstream webhooks without verification, following redirects from third-party APIs without re-validation, or treating data fetched from an integrated API as safe.

Each finding should note any API8/API10 root-cause conditions that apply in addition to API7.

### SSRF prevention checklist (from OWASP API7)

Subagents should verify whether the following controls are present and effective:

1. **Network isolation**: resource-fetching components run in a separate network segment with no access to internal services or metadata endpoints.
2. **Allowlists**: remote origins, URL schemes, ports, and accepted media types are explicitly allowlisted.
3. **Disable redirects**: automatic HTTP redirection is disabled, or every redirected destination is re-validated.
4. **Well-tested URL parser**: validation uses a maintained parser and re-parses the URL after any normalization.
5. **Input validation and sanitization**: all client-supplied URL components are validated before use.
6. **No raw response forwarding**: responses from outbound requests are not streamed unchanged to the client.

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Find All Outbound Network Call Sites

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
>    - `urllib.request.urlopen(url)`, `urllib2.urlopen(url)`
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

After Phase 1 completes, read `{{ REPORTS_ROOT }}/03_recon.md`. If the recon found **zero outbound call sites** (the summary reports "Found 0" or the "Outbound Call Sites" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/03_ssrf.md` and stop:

```markdown
# SSRF Analysis Results

No vulnerabilities found.
```

Only proceed to Phase 2 if Phase 1 found at least one outbound call site.

### Phase 2: Verify — Trace User Input to Outbound Call Sites (Batched)

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

- [OWASP API Security Top 10 2023 - API7:2023 Server Side Request Forgery](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/)
- [OWASP API Security Top 10 2023 - API8:2023 Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP API Security Top 10 2023 - API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)
- [OWASP Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [CWE-918: Server-Side Request Forgery (SSRF)](https://cwe.mitre.org/data/definitions/918.html)
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- [CWE-319: Cleartext Transmission of Sensitive Information](https://cwe.mitre.org/data/definitions/319.html)
- [CWE-444: Inconsistent Interpretation of HTTP Requests](https://cwe.mitre.org/data/definitions/444.html)
- [Snyk — URL confusion vulnerabilities](https://snyk.io/blog/url-confusion-vulnerabilities/)

---

## Important Reminders

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
