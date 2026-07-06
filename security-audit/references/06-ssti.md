# Server-Side Template Injection (SSTI) Detection

[ref: #ssti-detection]

You are performing a focused security assessment to find Server-Side Template Injection vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **recon** (find candidate rendering sites where the template string is dynamic), **batched verify** (trace whether user input reaches each site's template argument, in parallel batches of 3), and **merge** (consolidate batch results into the final report).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

---

## What is SSTI

Server-Side Template Injection occurs when user-supplied input is embedded directly into a template string that is then evaluated by a template engine. Unlike passing user data as *context variables* to a static template, SSTI means the user can write template syntax that the engine will execute — leading to arbitrary code execution, file read, or full server compromise.

The core pattern: *unvalidated user input is used as the template string passed to a template engine's render/compile/evaluate function.*

### CWE References

SSTI findings should be cross-referenced with the following CWE entries:

- **CWE-94: Improper Control of Generation of Code ("Code Injection")** — the template engine generates and executes code based on attacker-controlled input.
- **CWE-95: Eval Injection** — template expressions evaluate arbitrary code or commands supplied by the attacker.
- **CWE-116: Improper Encoding or Escaping of Output** — reliance on manual escaping instead of contextual auto-escaping or safe context passing.
- **CWE-1336: Improper Neutralization of Special Elements Used in a Template Engine** — the canonical CWE for template injection when untrusted data reaches a template processor.
- **CWE-20 (additional): Improper Input Validation** — when user input reaches templates without validation or allowlisting.

### Engine Probe Payload Matrix

Use the matrix below to quickly identify an unknown template engine during verification. Subagents should start with a harmless math probe; if the output matches the expected result, the engine is confirmed and an RCE payload can be selected from the examples later in this reference.

| Engine | Probe payload | Expected output |
| --- | --- | --- |
| Jinja2 / Flask | `{{ 7*7 }}` | `49` |
| Django | `{% debug %}` | Template debug output |
| Mako | `${ 7*7 }` | `49` |
| EJS / Nunjucks | `<%- 7*7 %>` | `49` |
| Handlebars | `{{#with "s" as \|string\|}}{{#with "e"}}{{../string.constructor.constructor("return process")()}}{{/with}}{{/with}}` | Server-side object access (if not sandboxed) |
| Pug / Jade | `#{7*7}` | `49` |
| Lodash / Underscore | `<%= 7*7 %>` | `49` |
| Ruby ERB | `<%= 7*7 %>` | `49` |
| Ruby Liquid | `{{ 7 | times: 7 }}` | `49` (when not logic-less restricted) |
| FreeMarker | `${7*7}` | `49` |
| Velocity | `#set($x = 7 * 7)$x` | `49` |
| Thymeleaf | `${7*7}` | `49` |
| JSP / JSTL / EL | `${7*7}` | `49` |
| PHP Twig | `{{ 7*7 }}` | `49` |
| PHP Smarty | `{7*7}` | `49` |
| ASP.NET Razor | `@(7*7)` | `49` |
| Go text/template | `{{7*7}}` | `49` |
| Scriban | `{{ 7 * 7 }}` | `49` |
| Mustache | `{{value}}` | Context-dependent (logic-less, no execution) |

### What SSTI IS

- Passing user input as the template string to be compiled or rendered:
  - `Template(user_input).render()` — Jinja2
  - `env.from_string(user_input).render()` — Jinja2
  - `render_template_string(user_input)` — Flask
  - `ejs.render(user_input, ctx)` — EJS (Node.js)
  - `nunjucks.renderString(user_input, ctx)` — Nunjucks
  - `Handlebars.compile(user_input)(ctx)` — Handlebars
  - `pug.render(user_input, ctx)` — Pug/Jade
  - `_.template(user_input)(ctx)` — Lodash/Underscore
  - `Velocity.evaluate(ctx, writer, logTag, user_input)` — Apache Velocity (Java)
  - `new Template("anon", new StringReader(user_input), cfg).process(...)` — FreeMarker (Java)
  - `new ST(user_input).render()` — StringTemplate4 (Java)
  - `thymeleafEngine.process(user_input, ctx)` — Thymeleaf (Java)
  - `\Twig\Environment::createTemplate(user_input)->render(ctx)` — Twig (PHP)
  - `$smarty->fetch("string:" . user_input)` — Smarty (PHP)
  - `Liquid::Template.parse(user_input).render(ctx)` — Liquid (Ruby)
  - `ERB.new(user_input).result(binding)` — ERB (Ruby)
  - `t, _ := template.New("x").Parse(user_input); t.Execute(w, data)` — Go `text/template`
  - `Template.fromString(user_input).render(ctx)` — Pebble (Java)
  - `TemplateEngine.evaluate(ctx, sw, "name", new StringReader(user_input))` — Apache Velocity with `TemplateEngine`
  - `RequestDispatcher` / JSP `out.print(user_input)` with EL `${...}` rendered server-side — JSP / JSTL (Java)
  - `RazorViewEngine.CreateView(controllerContext, user_input, ...)` or Razor parsing of attacker-controlled markup — ASP.NET Razor / MVC
  - `Template(user_input).render(ctx)` — Django templates (Python)
  - `django.template.loader.render_to_string(user_input, ctx)` when the template name is user-controlled — Django template path injection

- Dynamic template name construction where the name itself comes from user input and the engine resolves arbitrary files:
  - `render_template(user_input)` (Flask) where `user_input` is not validated against a safe list
  - `res.render(req.query.template)` (Express) where the template name is user-controlled
  - `return "user/" + lang + "/welcome"` (Spring/Thymeleaf) where `lang` is user-controlled
  - `View(user_input, model)` (ASP.NET MVC) where the view name is user-controlled

### What SSTI is NOT

Do not flag these patterns:

- **User input as context data** (safe — the template is static, only the data changes):
  ```
  render_template("profile.html", name=request.args.get("name"))
  env.get_template("report.html").render(user=user_obj)
  res.render("dashboard", { title: req.body.title })
  ```
- **XSS via template output**: If the template outputs unsanitized user data that is then rendered in a browser — that's XSS, not SSTI
- **Static templates with dynamic filenames validated against an allowlist**: If the template name comes from user input but is strictly validated against a hardcoded set of allowed template names, it's not SSTI
- **Sandboxed template engines configured with a restricted environment**: Liquid, Mustache, and similar logic-less engines cannot execute arbitrary code even if the template string comes from user input — but still flag them as "Needs Manual Review" unless you can confirm the engine is logic-less

### Patterns That Prevent SSTI

When you see these patterns, the code is likely **not vulnerable**:

**1. Static template file with dynamic context (most common safe pattern)**
```python
# Flask — static template, user input only in context dict
return render_template("user_profile.html", username=request.args.get("name"))

# Express — static view name
res.render("dashboard", { user: req.user })
```

**2. Allowlist validation for template names**
```python
ALLOWED_TEMPLATES = {"invoice.html", "receipt.html", "summary.html"}
template_name = request.args.get("tmpl", "invoice.html")
if template_name not in ALLOWED_TEMPLATES:
    abort(400)
return render_template(template_name)
```

**3. Logic-less / sandboxed engines that don't support code execution**
```javascript
// Mustache — logic-less, cannot execute arbitrary code even if template is user-supplied
const output = Mustache.render(userTemplate, ctx);  // lower risk, but still flag for review
```

---

## Vulnerable vs. Secure Examples

### Python — Flask / Jinja2

```python
# VULNERABLE: user input rendered as template string
@app.route('/greet')
def greet():
    name = request.args.get('name', '')
    template = f"<h1>Hello {name}!</h1>"
    return render_template_string(template)
    # Payload: ?name={{7*7}} → renders "49"
    # RCE:    ?name={{config.__class__.__init__.__globals__['os'].popen('id').read()}}

# SECURE: user input passed as context variable to a static template
@app.route('/greet')
def greet():
    name = request.args.get('name', '')
    return render_template("greet.html", name=name)
```

```python
# VULNERABLE: env.from_string with user-controlled template
@app.route('/preview')
def preview():
    tmpl = request.form.get('template')
    return Environment().from_string(tmpl).render()

# SECURE: load template from trusted file, pass user data as context
@app.route('/preview')
def preview():
    data = request.form.get('data')
    return env.get_template("preview.html").render(data=data)
```

### Python — Django Templates

```python
# VULNERABLE: user input used as the template string
from django.template import Template

def preview(request):
    tmpl = request.GET.get('tmpl', '')
    t = Template(tmpl)
    return HttpResponse(t.render(Context({})))
    # Probe: ?tmpl={% debug %}
    # RCE is limited by Django's sandboxed expression engine, but
    # leaked settings/secret-key and template filter abuse are possible.

# SECURE: render a static template with user data in context
def profile(request):
    return render(request, 'profile.html', {'name': request.GET.get('name')})
```

```python
# VULNERABLE: template name from user input without allowlisting (template path injection)
def report(request):
    page = request.GET.get('page')
    return render(request, f"reports/{page}.html")

# SECURE: allowlist the template name
ALLOWED_PAGES = {"summary", "detail"}

def report(request):
    page = request.GET.get('page', 'summary')
    if page not in ALLOWED_PAGES:
        raise Http404
    return render(request, f"reports/{page}.html")
```

```django
<!-- VULNERABLE template markup: |safe disables auto-escaping for user data -->
<p>{{ user_input|safe }}</p>

<!-- SECURE: rely on Django auto-escaping -->
<p>{{ user_input }}</p>
```

### Node.js — EJS

```javascript
// VULNERABLE: user input as template string
app.get('/render', (req, res) => {
  const tmpl = req.query.template;
  res.send(ejs.render(tmpl, { user: req.user }));
  // Payload: ?template=<%- global.process.mainModule.require('child_process').execSync('id') %>
});

// SECURE: user input only in context data
app.get('/render', (req, res) => {
  res.render('report', { content: req.query.content });
});
```

### Node.js — Nunjucks

```javascript
// VULNERABLE: renderString with user-controlled template
app.post('/preview', (req, res) => {
  const output = nunjucks.renderString(req.body.tmpl, { user: req.user });
  res.send(output);
  // Payload: {{ range.constructor("return global.process.mainModule.require('child_process').execSync('id').toString()")() }}
});

// SECURE: render from a file, user input only as context
app.post('/preview', (req, res) => {
  res.render('preview.html', { content: req.body.content });
});
```

### Node.js — Handlebars

```javascript
// VULNERABLE: compile with user-supplied template string
app.get('/email', (req, res) => {
  const template = Handlebars.compile(req.query.tmpl);
  res.send(template({ user: req.user }));
  // Payload: {{#with "s" as |string|}}{{#with "e"}}{{../string.constructor.constructor("return process")()}}{{/with}}{{/with}}
});

// SECURE: compile static template, user data in context
const template = Handlebars.compile(fs.readFileSync('email.hbs', 'utf8'));
app.get('/email', (req, res) => {
  res.send(template({ name: req.query.name }));
});
```

### Ruby — ERB

```ruby
# VULNERABLE: user input passed to ERB constructor
get '/render' do
  tmpl = params[:template]
  ERB.new(tmpl).result(binding)
  # Payload: <%= `id` %>
end

# SECURE: static ERB file, user data in binding only
get '/render' do
  @name = params[:name]
  erb :profile
end
```

### Java — FreeMarker

```java
// VULNERABLE: template string sourced from user input
@PostMapping("/preview")
public String preview(@RequestParam String tmplStr, Model model) throws Exception {
    Template t = new Template("preview", new StringReader(tmplStr), cfg);
    StringWriter out = new StringWriter();
    t.process(model.asMap(), out);
    return out.toString();
    // Payload: <#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
}

// SECURE: load template from classpath, user data only in model
@GetMapping("/report")
public String report(@RequestParam String userId, Model model) {
    model.addAttribute("user", userService.findById(userId));
    return "report";  // resolves to templates/report.ftl
}
```

### Java — Velocity

```java
// VULNERABLE: user input evaluated as template
public String render(String userTemplate) {
    VelocityContext ctx = new VelocityContext();
    StringWriter sw = new StringWriter();
    Velocity.evaluate(ctx, sw, "template", userTemplate);
    return sw.toString();
    // Payload: #set($e="")#set($x=$e.class.forName("java.lang.Runtime"))...
}

// SECURE: load template from file
Template t = Velocity.getTemplate("report.vm");
t.merge(ctx, sw);
```

### Java — Thymeleaf (Spring)

```java
// VULNERABLE: user input used as template expression evaluated by Thymeleaf
@GetMapping("/hello")
public String hello(@RequestParam String lang, Model model) {
    return "user/" + lang + "/welcome";  // path traversal + SSTI if lang is e.g. "__${T(java.lang.Runtime).getRuntime().exec('id')}__"
}

// SECURE: validate lang against an allowlist
private static final Set<String> ALLOWED_LANGS = Set.of("en", "fr", "de");

@GetMapping("/hello")
public String hello(@RequestParam String lang, Model model) {
    if (!ALLOWED_LANGS.contains(lang)) return "error";
    return "user/" + lang + "/welcome";
}
```

### Java — JSP / JSTL

```jsp
<!-- VULNERABLE: user input rendered through Expression Language -->
<% String name = request.getParameter("name"); %>
<p>Hello ${name}</p>
<!-- Probe: ?name=${7*7} -->
<!-- RCE: ?name=${pageContext.request.getSession().getServletContext().getRealPath('/')}
          or via classloader gadgets in legacy containers -->

<!-- SECURE: use JSTL <c:out> which escapes EL and HTML -->
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<c:out value="${param.name}" />
```

```java
// VULNERABLE: user input used as the JSP view name
@RequestMapping("/page")
public String page(@RequestParam String view) {
    return view;  // e.g. ?view=redirect:/attacker or arbitrary view resolution
}

// SECURE: allowlist the view name
private static final Set<String> ALLOWED_VIEWS = Set.of("home", "profile");

@RequestMapping("/page")
public String page(@RequestParam String view) {
    return ALLOWED_VIEWS.contains(view) ? view : "error";
}
```

### C# — ASP.NET Razor / MVC

```csharp
// VULNERABLE: user input parsed as a Razor template
public IActionResult Preview(string tmpl)
{
    var engine = new RazorViewEngine(...);
    var result = engine.Render(tmpl, Model); // if such a helper exists or uses RazorLight
    return Content(result);
    // Probe: ?tmpl=@(7*7)
    // RCE: ?tmpl=@(System.Diagnostics.Process.Start("cmd","/c whoami").StartInfo.FileName)
}

// VULNERABLE: @Html.Raw with unsanitized user input in the view
// In .cshtml:
@Html.Raw(Model.UserInput)

// SECURE: use Razor's default HTML encoding
@Model.UserInput

// SECURE: static view name with user data in the model
public IActionResult Profile(string name)
{
    return View("Profile", new ProfileModel { Name = name });
}
```

### PHP — Twig

```php
// VULNERABLE: user input as template string
$app->get('/render', function (Request $request) use ($twig) {
    $tmpl = $request->query->get('template');
    return $twig->createTemplate($tmpl)->render([]);
    // Payload: {{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
});

// SECURE: static template, user data in context array
$app->get('/profile', function (Request $request) use ($twig) {
    return $twig->render('profile.html.twig', ['name' => $request->query->get('name')]);
});
```

### PHP — Smarty

```php
// VULNERABLE: user-controlled template string via fetch("string:...")
$template = $_GET['tmpl'];
$smarty->fetch("string:" . $template);
// Payload: {php}echo shell_exec('id');{/php}

// SECURE: pass user data as template variable
$smarty->assign('name', $_GET['name']);
$smarty->display('profile.tpl');
```

### Go — text/template

```go
// VULNERABLE: user input parsed as template
func handler(w http.ResponseWriter, r *http.Request) {
    tmpl := r.URL.Query().Get("tmpl")
    t, _ := template.New("x").Parse(tmpl)
    t.Execute(w, data)
    // Payload: {{.Func "os/exec" "id"}} — depends on data methods exposed
}

// SECURE: static template string or file; user input only in data
func handler(w http.ResponseWriter, r *http.Request) {
    t := template.Must(template.ParseFiles("tmpl/page.html"))
    t.Execute(w, map[string]string{"Name": r.URL.Query().Get("name")})
}
// Note: Go's html/template auto-escapes output, but text/template does not.
// Even html/template is vulnerable to SSTI if user input reaches .Parse().
```

---

## Specialized SSTI Contexts

Template-like evaluation happens outside traditional view engines. Treat the following contexts as SSTI when untrusted data reaches the processing function.

| Context | Example | Detection signal |
| --- | --- | --- |
| **PDF generators** (wkhtmltopdf, WeasyPrint, Puppeteer) | HTML template with `{{ user_input }}` converted to PDF | User input in HTML-to-PDF templates; probe with `{{7*7}}` if the generator parses template syntax before rendering. |
| **LaTeX processors** | `\input{<user>}` or `\include{<user>}` in `.tex` source compiled server-side | User input in LaTeX source passed to `pdflatex` or a wrapper; look for read/write primitives (`\openout`, `\write18`). |
| **Markdown processors with template syntax** | Markdown rendered by a templating engine before HTML conversion | Markdown content treated as template; e.g. Jinja2 preprocessing of README/user content. |
| **JSON/YAML config templating** | Config file rendered with user-provided variables before parsing | User values interpolated into config before `json.load` / `yaml.safe_load`; probe with `${7*7}` or `{{7*7}}`. |
| **Serverless / infrastructure template injection** | CloudFormation / SAM / ARM / Terraform templates built from user input | User input in infrastructure templates; can lead to IAM policy injection or resource provisioning outside the account. |
| **Nested template evaluation** | Template renders another template string | Double-evaluation of template content, e.g. first render produces `{{payload}}` which is rendered again. |

### PDF Generators

```python
# VULNERABLE: user input reaches an HTML template rendered to PDF
from weasyprint import HTML

def invoice(request):
    html = f"<h1>Invoice for {request.GET.get('name')}</h1>"
    return HttpResponse(HTML(string=html).write_pdf(), content_type='application/pdf')
    # Probe: ?name={{7*7}}

# SECURE: static HTML template, user data only as context
from django.template.loader import render_to_string
def invoice(request):
    html = render_to_string('invoice.html', {'name': request.GET.get('name')})
    return HttpResponse(HTML(string=html).write_pdf(), content_type='application/pdf')
```

### LaTeX Processors

```python
# VULNERABLE: user input concatenated into a LaTeX source document
import subprocess

def render(request):
    user = request.GET.get('user')
    tex = f"\\documentclass{{article}}\\begin{{document}}\\input{{{user}}}\\end{{document}}"
    subprocess.run(['pdflatex', '-jobname', 'out', tex])
    # Attack: ?user=../../../etc/passwd%00 or \write18 commands if shell-escape is enabled.

# SECURE: validate and escape the filename; disable shell escape
ALLOWED = {"header", "footer"}
def render(request):
    user = request.GET.get('user')
    if user not in ALLOWED:
        raise ValueError("invalid fragment")
    tex = f"...\\input{{{user}}}..."
    subprocess.run(['pdflatex', '-no-shell-escape', '-jobname', 'out', tex])
```

### Markdown with Template Syntax

```python
# VULNERABLE: Markdown content preprocessed as Jinja2 before conversion
import markdown
from jinja2 import Template

def preview(request):
    md = request.POST.get('markdown')
    html = Template(md).render()  # user input is the template
    return HttpResponse(markdown.markdown(html))

# SECURE: parse Markdown directly without templating
html = markdown.markdown(request.POST.get('markdown'))
```

### JSON / YAML Config Templating

```python
# VULNERABLE: user-controlled values injected into a config string
import json

def load_config(request):
    value = request.GET.get('value')
    config_str = f'{{"setting": "{value}"}}'
    return json.loads(config_str)
    # If the project uses a template engine for config files, probe with {{7*7}}.

# SECURE: build the data structure directly; avoid string templating
return json.dumps({"setting": request.GET.get('value')})
```

### Serverless / Infrastructure Templates

```yaml
# VULNERABLE CloudFormation fragment built from user input (example)
Resources:
  Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: "{{ user_input }}"  # user_input reaches the template engine
```

Treat any API that accepts values later inserted into CloudFormation, SAM, ARM, Terraform, or Pulumi templates as a potential template-injection surface. The impact is not RCE on the application server but privilege escalation, resource creation, or data exfiltration through the infrastructure provider.

### Nested Template Evaluation

```python
# VULNERABLE: rendered output is rendered again
first = Template(user_input).render()
second = Template(first).render()  # second evaluation executes payloads from the first

# SECURE: render once; escape output before any secondary use
```

---

## Engine-Specific Prevention / Hardening

The most reliable prevention is to **never use untrusted input as a template string**. When dynamic templates are unavoidable, apply engine-specific hardening.

| Engine | Dangerous feature | Safe configuration |
| --- | --- | --- |
| **FreeMarker** | `?new` built-in, `freemarker.template.utility.Execute` | Disable `?new` (`Configuration.setNewBuiltinClassResolver(TemplateClassResolver.SAFER_RESOLVER)` or disallow); restrict class loader; avoid `Configuration.setAPIBuiltinEnabled(true)` unnecessarily. |
| **Velocity** | Class loading via `ClassTool`, `ApplicationAttribute`, event handlers | Use `org.apache.velocity.runtime.resource.util.StringResourceRepository` only; sandbox context objects; avoid `Velocity.evaluate` on untrusted strings; configure `runtime.references.strict` and disable dangerous introspection. |
| **Thymeleaf** | Expression access to `T(...)` (Spring EL type references) | Use `StandardDialect` without unrestricted expression execution; disable preprocessing expressions (`thymeleaf.expression.preprocessor`); validate controller view names against an allowlist. |
| **Jinja2** | `\|attr`, `__class__`, `__subclasses__`, `{% import %}` of arbitrary modules | Use `jinja2.sandbox.SandboxedEnvironment`; enable auto-escaping; restrict `Environment.globals`; avoid `from_string` on user input. |
| **Django** | `\|safe`, `{% autoescape off %}`, `mark_safe` on user data | Keep auto-escaping enabled; validate template names against an allowlist; never pass user input to `Template()`. |
| **Handlebars** (server-side) | `Handlebars.create()` with helpers exposing `process`/`require` | Run in a VM or sandbox with `console`/`process`/`require` disabled; do not compile user templates server-side; use a restricted helper allowlist. |
| **Twig** | `sandbox` disabled, `include` from arbitrary paths | Enable the sandbox extension with a strict policy; disable `raw` filter for user data; validate template names. |
| **Smarty** | `{php}`, `{include_php}`, `fetch("string:...")` | Disable `allow_php_tag` and `allow_php_templates`; use `security_settings` to restrict resource types. |
| **Go text/template** | Method calls on context objects, `html/template` parsing user strings | Never parse user input with `template.Parse`; pass user data only as typed struct fields; prefer `html/template` for output contexts but still avoid user input as template source. |
| **ASP.NET Razor** | `@Html.Raw`, dynamic view names | Avoid `@Html.Raw` on untrusted data; allowlist view names; do not compile user strings with RazorLight/RazorEngine unless fully sandboxed. |
| **JSP / JSTL** | EL expression evaluation, scriptlets | Escape output with `<c:out>`; disable scriptlets in `web.xml`; use a strict EL resolver; validate view names. |

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

**Subagent constraint**: Subagents must perform read-only analysis. They are forbidden from modifying project source code, configuration files, tests, or any other file under the repository root.

### Phase 1: Find Template Rendering Sites Using Dynamic Strings

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where a template engine renders, compiles, or evaluates a **dynamically built string** as the template itself — rather than loading a static template file. Write results to `{{ REPORTS_ROOT }}/06_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, template engines in use, and how views/responses are rendered.
>
> **What to search for — vulnerable template rendering patterns**:
>
> Flag any call where the first argument (the template string) is a variable, a concatenated string, or any non-literal value. You are not yet checking whether that variable comes from user input — that is Phase 2's job.
>
> 1. **Python — Jinja2 / Flask**:
>    - `render_template_string(var)` — any non-literal argument
>    - `Environment().from_string(var)` or `env.from_string(var)`
>    - `jinja2.Template(var).render(...)`
>    - `Template(var)` where Template is imported from jinja2
>
> 2. **Python — Mako**:
>    - `Template(var).render(...)` where Template is from `mako.template`
>    - `mako.template.Template(var)`
>
> 3. **Python — Django**:
>    - `django.template.Template(var)` with non-literal `var`
>    - `render(request, var, ...)` or `render_to_string(var, ...)` where `var` is user-controlled
>    - `django.template.loader.get_template(var)` with non-literal `var`
>
> 4. **Node.js — EJS**:
>    - `ejs.render(var, ...)` or `ejs.renderFile(var, ...)` where var is not a static string literal
>
> 5. **Node.js — Nunjucks**:
>    - `nunjucks.renderString(var, ...)` — any non-literal first argument
>    - `env.renderString(var, ...)`
>
> 6. **Node.js — Handlebars**:
>    - `Handlebars.compile(var)` — any non-literal argument
>    - `Handlebars.precompile(var)`
>
> 7. **Node.js — Pug/Jade**:
>    - `pug.render(var, ...)` — any non-literal argument
>    - `pug.compile(var, ...)`
>
> 8. **Node.js — Lodash/Underscore**:
>    - `_.template(var)` — any non-literal argument
>    - `Handlebars.compile(var)`
>
> 9. **Node.js — Swig / Twig.js**:
>    - `swig.render(var, ...)`
>    - `twig({ data: var })`
>
> 10. **Ruby — ERB**:
>     - `ERB.new(var).result(...)` — any non-literal argument
>     - `ERB.new(var).result_with_hash(...)`
>
> 11. **Ruby — Liquid**:
>     - `Liquid::Template.parse(var).render(...)` — any non-literal argument
>
> 12. **Java — FreeMarker**:
>     - `new Template(name, new StringReader(var), cfg)` — var is not a literal
>     - `cfg.getTemplate(var)` where var is not a literal (potential template path injection)
>
> 13. **Java — Velocity**:
>     - `Velocity.evaluate(ctx, writer, logTag, var)` — any non-literal fourth argument
>     - `ve.evaluate(ctx, writer, logTag, var)`
>
> 14. **Java — StringTemplate / ST4**:
>     - `new ST(var)` — any non-literal argument
>     - `new STGroup(var, ...)` with non-literal path
>
> 15. **Java — Thymeleaf**:
>     - Controller methods returning a view name built by string concatenation: `return "user/" + var + "/page"` or `return String.format("prefix/%s/suffix", var)`
>     - `templateEngine.process(var, ctx)` with non-literal var
>
> 16. **Java — JSP / JSTL**:
>     - `RequestDispatcher.forward(request, response)` to a user-controlled path
>     - Controller returning a view name built from user input
>     - Scriptlets or EL expressions that include user input without `<c:out>`
>
> 17. **C# — ASP.NET Razor / MVC**:
>     - `View(var, model)` or `return View(var)` where `var` is user-controlled
>     - RazorLight / RazorEngine compiling user input
>     - `@Html.Raw(Model.UserInput)` in `.cshtml` files
>
> 18. **PHP — Twig**:
>     - `$twig->createTemplate($var)->render(...)` — any non-literal argument
>     - `$environment->createTemplate($var)`
>
> 19. **PHP — Smarty**:
>     - `$smarty->fetch("string:" . $var)` or `$smarty->display("string:" . $var)`
>     - `$smarty->fetch($var)` where var may contain a "string:" prefix
>
> 20. **PHP — Blade / Laravel**:
>     - `Blade::render($var, ...)` — any non-literal argument
>     - `\Illuminate\Support\Facades\View::make($var, ...)` with non-literal name (template path injection)
>
> 21. **Go — text/template or html/template**:
>     - `template.New(name).Parse(var)` — any non-literal argument to Parse
>     - `t.Parse(var)` on any template variable
>     - `t.ParseFiles(var)` with non-literal var (template path injection)
>
> 22. **C# — Scriban / Handlebars.Net / DotLiquid / Fluid**:
>     - `Template.Parse(var)` (Scriban) — non-literal
>     - `Handlebars.Compile(var)` — non-literal
>     - `DotLiquid.Template.Parse(var)` — non-literal
>     - `FluidParser.TryParse(var, ...)` — non-literal
>
> 23. **Specialized contexts**:
>     - PDF generators (`weasyprint.HTML(string=var)`, `pdfkit.from_string(var)`, Puppeteer `page.setContent(var)`)
>     - LaTeX wrappers that concatenate user input into `.tex` source
>     - Markdown preprocessors that run a template engine before conversion
>     - JSON/YAML config builders that use string templating with user values
>     - Serverless / infrastructure template assemblers (CloudFormation, SAM, ARM, Terraform)
>     - Nested template evaluation: output of one template passed to another parser
>
> **What to skip** (safe patterns — do not flag):
> - Calls where the first argument is a **string literal**: `render_template_string("<h1>Hello</h1>")`, `ejs.render("<p>static</p>", ctx)`
> - Calls where a file path is loaded from a trusted constant and user input only appears in context: `render_template("profile.html", user=user_obj)`
> - Template engine configuration calls that do not render user-supplied content: `env = Environment(loader=FileSystemLoader("templates/"))`
>
> **Output format** — write to `{{ REPORTS_ROOT }}/06_recon.md`:
>
> ```markdown
> # SSTI Recon: [Project Name]
>
> ## Summary
> Found [N] locations where a template engine renders a dynamic (non-literal) string as the template.
>
> ## Candidate Rendering Sites
>
> ### 1. [Descriptive name — e.g., "render_template_string in /greet endpoint"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [function name or route]
> - **Template engine**: [Jinja2 / EJS / Handlebars / FreeMarker / Twig / ERB / etc.]
> - **Rendering call**: [render_template_string / from_string / ejs.render / Handlebars.compile / etc.]
> - **Dynamic argument**: `var_name` — [brief note on what it appears to represent, e.g., "looks like it comes from a form field" or "unknown origin"]
> - **Code snippet**:
>   ```
>   [the rendering call with the dynamic argument]
>   ```
>
> [Repeat for each site]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/06_recon.md`. If the recon found **zero candidate rendering sites** (the summary reports "Found 0" or the "Candidate Rendering Sites" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/06_ssti.md` and stop:

```markdown
# SSTI Analysis Results

No vulnerabilities found.
```

Only proceed to Phase 2 if Phase 1 found at least one candidate rendering site.

### Phase 2: Verify — Trace User Input (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/06_recon.md` and split the candidate rendering sites into **batches of up to 3 candidates each**. Launch **one subagent per batch in parallel**. Each subagent traces taint for only its assigned candidates and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/06_recon.md` and count the numbered candidate sections under "Candidate Rendering Sites" (`### 1.`, `### 2.`, etc.).
2. Divide them into batches of up to 3. For example, 8 candidates → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those candidate sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned candidates.
5. Each subagent writes to `{{ REPORTS_ROOT }}/06_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project uses Python/Flask with Jinja2, include only the "Python — Flask / Jinja2" examples. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned candidate rendering site, determine whether a user-supplied value reaches the dynamic template string argument. Our goal is to find SSTI vulnerabilities.Write results to `{{ REPORTS_ROOT }}/06_batch_[N].md`.
>
> **Your assigned candidates** (from the recon phase):
>
> [Paste the full text of the assigned candidate sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand request entry points, middleware, and how data flows through the application.
>
> **SSTI reference — what to trace**:
>
> For each rendering site, trace the **dynamic template argument** backwards to its origin.
>
> 1. **Direct user input** — the argument is assigned directly from a request source with no transformation:
>    - HTTP query params: `request.GET.get(...)`, `req.query.x`, `params[:x]`, `$_GET['x']`, `c.Query("x")`
>    - Path parameters: `request.path_params['id']`, `req.params.id`, `params[:id]`
>    - Request body / form fields: `request.POST.get(...)`, `req.body.x`, `params[:x]`, `$_POST['x']`
>    - HTTP headers: `request.headers.get(...)`, `req.headers['x']`
>    - Cookies: `request.COOKIES.get(...)`, `req.cookies.x`
>    - File upload content: if a file's content is read and passed as the template string
>
> 2. **Indirect user input** — the argument is derived from user input through transformations, function calls, or intermediate assignments. Trace the full chain:
>    - Variable assigned from a function return value → check that function's parameter origin
>    - Variable passed as a function argument → check the call site(s)
>    - Variable read from a class attribute or shared state set elsewhere → find the setter
>    - Variable conditionally assigned — check all branches
>
> 3. **Second-order input** — the template string is read from the database, a config store, or a file, but the stored value originally came from user input (e.g., user-submitted "custom email template" feature):
>    - Find where this value was written — was it stored from a user-supplied field?
>    - Was it sanitized before storage? Note: sanitizing SSTI payloads is unreliable — still flag.
>
> 4. **Server-side / hardcoded value** — the template string comes from a file loaded at startup, a hardcoded constant, or server-side logic with no user influence — this site is NOT exploitable.
>
> **Template engine risk level**:
> - **Critical**: Jinja2, Mako, Twig, Smarty, FreeMarker, Velocity, ERB, Pug, EJS, Go `text/template`, Thymeleaf, JSP/JSTL — full code execution possible
> - **High**: Handlebars (with prototype pollution gadgets), Nunjucks, Lodash `_.template`, Blade, Razor
> - **Medium / Logic-less**: Mustache, Liquid (without dangerous tags enabled) — arbitrary code execution not typically possible, but still check for data leakage
>
> **Mitigations to check**:
> - Is the template engine running in a sandboxed mode? (e.g., Jinja2 `SandboxedEnvironment`, Twig `sandbox` extension with strict policy)
> - Is the input validated or filtered before being used as a template? Note: blocklist-based filtering of template syntax characters (`{`, `}`, `%`) is **not** a reliable mitigation — attackers can often bypass it.
> - Is the result of rendering passed directly to the response, or is it used in a non-dangerous context?
>
> **Vulnerable vs. secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Vulnerable**: User input demonstrably reaches the template string argument with no effective mitigation, using a critical/high-risk engine.
> - **Likely Vulnerable**: User input probably reaches the template string (indirect flow or second-order), or a medium-risk engine is used, or only blocklist filtering is applied.
> - **Not Vulnerable**: The template string is server-side only (file, constant, hardcoded), OR a properly configured sandbox is confirmed in place.
> - **Needs Manual Review**: Cannot determine the argument's origin with confidence, or a logic-less engine is used and data leakage scope is unclear.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/06_batch_[N].md`:
>
> ```markdown
> # SSTI Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Template engine**: [Jinja2 / FreeMarker / Twig / ERB / etc.] (severity: Critical/High)
> - **Issue**: [e.g., "HTTP query param `tmpl` flows directly into render_template_string()"]
> - **Taint trace**: [Step-by-step from entry point to the rendering call — e.g., "request.args.get('tmpl') → tmpl → render_template_string(tmpl)"]
> - **Impact**: Remote code execution — attacker can execute arbitrary OS commands, read files, exfiltrate secrets, or pivot internally.
> - **Proof-of-concept payload**:
>   ```
>   [Template syntax payload appropriate for the engine.
>    Example for Jinja2: ?tmpl={{config.__class__.__init__.__globals__['os'].popen('id').read()}}
>    Example for FreeMarker: ?tmpl=<#assign+ex="freemarker.template.utility.Execute"?new()>${ex("id")}
>    Example for Twig: ?tmpl={{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
>    Example for ERB: ?tmpl=<%= `id` %>
>    Example for EJS: ?tmpl=<%- global.process.mainModule.require('child_process').execSync('id') %>
>    Example for JSP/EL: ?tmpl=${7*7} then escalate to classloader gadgets
>    Example for Razor: ?tmpl=@(7*7) then @System.Diagnostics.Process.Start("cmd","/c whoami")
>    Example for Django: ?tmpl={% debug %} then filter/sandbox abuse]
>   ```
> - **Remediation**: Never use user input as a template string. Pass user data as context variables to a static template. If dynamic templates are a product requirement, use a sandboxed logic-less engine (e.g., Mustache, Liquid with safe config) and enforce strict input validation.
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Template engine**: [engine name] (severity: High/Medium)
> - **Issue**: [e.g., "Template string likely sourced from user input via helper function" or "Second-order: user-submitted template stored in DB then evaluated server-side"]
> - **Taint trace**: [Best-effort trace with the uncertain step identified]
> - **Concern**: [Why it's still a risk — e.g., "Second-order SSTI: user can craft payload at submission time that executes when the template is rendered later"]
> - **Proof-of-concept payload**:
>   ```
>   [payload for the engine]
>   ```
> - **Remediation**: [Specific fix]
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Reason**: [e.g., "Template string is loaded from a hardcoded file path" or "Jinja2 SandboxedEnvironment confirmed in use with restricted globals"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Uncertainty**: [Why the argument's origin could not be determined]
> - **Suggestion**: [What to trace manually — e.g., "Follow `get_custom_template()` in services/email.py to check where its return value originates"]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/06_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/06_ssti.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/06_batch_1.md`, `{{ REPORTS_ROOT }}/06_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/06_ssti.md` using this format:

```markdown
# SSTI Analysis Results: [Project Name]

## Executive Summary
- Rendering sites analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/06_ssti.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/06_batch_*.md`).

---

## OWASP API Security Top 10 2023 mapping

This scan supports the following OWASP API Security Top 10 2023 risks:

- **API8:2023 Security Misconfiguration** — Template engines are configured to accept dynamic template strings or run without sandboxing, allowing attacker-supplied template syntax to execute. This includes insecure defaults such as auto-escaping disabled, dangerous built-ins enabled (FreeMarker `?new`, Velocity `ClassTool`), or scriptlets/EL left active in JSP.
- **API10:2023 Unsafe Consumption of APIs** — User-controlled or third-party data is used as the template source rather than only as context variables. Data pulled from partner APIs, webhooks, files, or storage and then passed to a template engine can trigger SSTI if it contains template syntax.

### Cross-mapping table

| Root cause | OWASP risk | When to cross-map |
| --- | --- | --- |
| User input rendered through a server-side template engine | API8:2023 Security Misconfiguration | Template engine enabled with dangerous features; auto-escaping disabled. |
| Data from a third-party API rendered through a template | API10:2023 Unsafe Consumption of APIs | Upstream data is trusted and passed to a template without sanitization. |
| PDF/LaTeX/markdown processor uses template syntax on user data | API8/API10 | Processor configuration allows embedded expressions. |

---

## Important Reminders

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- **Subagents must not modify project source code**. This skill is read-only. Subagents may only write analysis reports under `{{ REPORTS_ROOT }}/`.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 candidates per subagent**. If there are 1-3 candidates total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned candidates' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **Phase 1 is purely structural**: flag any dynamic (non-literal) variable used as the template string argument. Do not attempt to trace user input in Phase 1 — that is Phase 2's job.
- **Phase 2 is purely taint analysis**: for each site assigned to a batch, trace the dynamic template argument back to its origin. If it comes from a user-controlled source, the site is a real vulnerability.
- The critical distinction is **template string vs. template context**: user input passed as a *variable name/value* inside `render_template("page.html", user=input)` is safe. User input passed as the *template string itself* to `render_template_string(input)` is dangerous.
- **Second-order SSTI is easy to miss**: a "custom template" feature may let users store Jinja2/Twig syntax in the database. When that stored template is later loaded and rendered server-side without sandboxing, it's SSTI. In Phase 2, treat DB-read template strings as potentially tainted.
- **Thymeleaf fragment expressions**: in Spring Boot, if a controller returns a view name constructed from user input (e.g., `return "user/" + lang + "/view"`), Thymeleaf may process Spring EL expressions embedded in the path segment, enabling RCE. Flag any controller that builds a view name string using user-supplied values.
- **JSP / JSTL EL injection**: `${7*7}` is a reliable probe. Legacy containers may allow classloader gadgets leading to RCE. Always verify whether `<c:out>` is used for output and whether scriptlets are disabled.
- **ASP.NET Razor**: `@(7*7)` confirms expression evaluation. `@Html.Raw()` on user data is XSS, but compiling attacker-controlled strings with Razor is SSTI/RCE.
- **Django templates**: Django's expression language is more restricted than Jinja2, but `{% debug %}` leaks settings and `|safe` disables auto-escaping. Template-path injection is also possible when the template name is user-controlled.
- **Blocklist filtering is not a mitigation**: attempts to strip `{{`, `}}`, `<%`, `%>`, `${`, `@(`, etc. from user input are routinely bypassed via encoding, alternate syntax, or nested expressions. Do not classify a finding as "Not Vulnerable" solely because filtering is present.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Include engine-appropriate proof-of-concept payloads for all Vulnerable and Likely Vulnerable findings. Payloads should first test with a math expression (e.g., `{{7*7}}`, `${7*7}`, `@(7*7)`, `{% debug %}`) to confirm template execution before escalating to RCE payloads.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/06_recon.md` and all `{{ REPORTS_ROOT }}/06_batch_*.md` files after the final `{{ REPORTS_ROOT }}/06_ssti.md` is written.
