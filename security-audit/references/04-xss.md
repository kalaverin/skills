---
subject: "XSS detection reference for SAST subagents: definition, types, scope boundaries, API-specific contexts, prevention patterns incl. Trusted Types and Sanitizer API, context-aware output encoding, advanced variants, per-stack vulnerable/secure recipes across web frameworks and frontend stacks, three-phase execution prompts, OWASP mapping, CSP guidance, CWE."
index:
  - anchor: xss-detection
    what: "Focused XSS detection role using the three-phase subagent approach — recon, batched verify, merge — gated on the architecture report."
    problem: "Codebase needs systematic script-injection sweep across every rendering path, yet unstructured hunting misses dangerous sinks and drowns reviewers in unverified candidates; detection orchestration, phase pipeline, verified findings, audit rigor, methodical triage, candidate flood, coverage goal."
    use_when: "XSS scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-phase detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual XSS knowledge is needed, not execution."
    expected: "Verified XSS findings consolidated into the module report with false positives filtered."
  - anchor: xss-definition
    what: "Core definition: unescaped, unsanitized input reaching an HTML, JavaScript, or DOM sink, enabling script execution in victim browsers."
    problem: "Reviewers disagree on what counts as script injection without shared definition, so borderline rendering paths get classified inconsistently across engagements; concept baseline, shared vocabulary, classification consistency, definition anchor, scope clarity, common ground, term alignment."
    use_when: "Onboarding to the scan; deciding whether a rendering path belongs to XSS at all; teaching the detection boundary."
    avoid_when: "Concrete stack recipes are needed — jump to the matching example anchor; execution workflow is the question."
    expected: "Everyone applies one definition: unescaped input reaching a rendering sink."
  - anchor: xss-types
    what: "The three XSS types — reflected, stored, DOM-based — with their distinct taint paths."
    problem: "Detection strategy differs per type, and conflating reflected with stored or DOM flows produces incomplete taint tracing during verification; type taxonomy, reflected echo, stored persistence, trace strategy, classification basis, taint direction, client side."
    use_when: "Planning taint traces; deciding whether client-side only analysis suffices; classifying a confirmed finding."
    avoid_when: "Sink catalogs are the question — see the scope-in anchor; stack recipes wanted."
    expected: "Each finding is typed correctly, driving the right trace path."
  - anchor: xss-scope-in
    what: "Positive sink/source catalogs: server-side template sinks, DOM sinks, script-execution sinks, and DOM sources."
    problem: "Detectors under-report when sink catalogs stay implicit, missing modern DOM properties, execution sinks, and indirect sources across frameworks; inclusion rules, source inventory, dom apis, coverage completeness, missed sinks, hidden vectors, recon breadth."
    use_when: "Building or checking a recon sink list; unsure whether a property qualifies; calibrating false negatives."
    avoid_when: "Exclusions are the question — see the scope-out anchor; encoding rules wanted."
    expected: "Every dangerous sink and source is recognized during recon."
  - anchor: xss-api-contexts
    what: "API-specific XSS contexts: JSON rendered by frontends, error responses, file downloads, webhooks, and admin panels consuming API data."
    problem: "API-only codebases get wrongly cleared when reviewers ignore downstream rendering of API responses in browsers and dashboards; json rendering, downstream clients, error pages, hidden consumers, blind spots, dashboard views, doc uis, backoffice views."
    use_when: "Target is an API without server-rendered pages; assessing whether XSS applies."
    avoid_when: "Classic server-rendered stack — sink catalogs matter more; stack recipes wanted."
    expected: "API-driven rendering paths identified as in-scope."
  - anchor: xss-scope-out
    what: "Boundary rules separating XSS from CSRF, clickjacking, header injection, and safe `textContent`-style writes."
    problem: "Findings get misrouted when injection-adjacent classes blur into scripting, corrupting severity and ownership across scans; misrouting risk, class confusion, double reporting, ownership clarity, dedup discipline, triage errors, category overlap, fuzzy edges."
    use_when: "A finding could belong to another scan class; triaging overlapping categories; writing routing notes."
    avoid_when: "Positive sinks are needed — see scope-in; prevention patterns wanted."
    expected: "Each candidate lands in exactly one vulnerability class."
  - anchor: xss-prevention-patterns
    what: "Six constructions that prevent XSS: auto-escaping templates, explicit escaping, safe DOM properties, allowlist sanitizers, framework escaping, and browser-enforced policies with the Sanitizer API."
    problem: "Verify subagents need authoritative safe patterns to avoid flagging secured rendering, and scattered mitigation knowledge produces false positives everywhere; safe construction, escaping forms, sanitizer libraries, policy enforcement, false-positive control, secure baseline, mitigation catalog."
    use_when: "Classifying a candidate as mitigated; comparing site code against known-safe forms; writing remediation notes."
    avoid_when: "Vulnerable examples per stack are the need — see recipe anchors; CSP detail wanted."
    expected: "Escaped, sanitized, or policy-guarded rendering is correctly classified as not vulnerable."
  - anchor: xss-output-encoding
    what: "Context-aware output encoding rules: HTML body, attribute, JavaScript, URL, and CSS contexts each need their own encoder."
    problem: "Single-encoder habits fail when identical values land in script, attribute, or URL contexts, leaving bypassable sanitization behind; encoding contexts, per-context rules, attribute quoting, js strings, url encoding, css values, context mismatch, encoder choice."
    use_when: "Judging whether an encoder matches the actual output context; reviewing custom sanitizers."
    avoid_when: "Whole-framework defenses are the question — see prevention patterns; payload strings wanted."
    expected: "Encoding is validated per output context, not per blanket assumption."
  - anchor: xss-advanced-variants
    what: "Advanced variant table: mutation XSS, DOM clobbering, prototype pollution, upload/PDF XSS, SSTI-to-XSS chains, and redirect-to-XSS."
    problem: "Classic-only review misses mutation, clobbering, and chained vectors that bypass naive sanitizers and filters entirely; mxss, parser differentials, upload flows, variant coverage, exotic paths, sanitizer escape, chain attacks, edge renderers."
    use_when: "Sanitizers or unusual renderers are present; standard patterns came back clean but suspicion remains."
    avoid_when: "Basic sink analysis unfinished — cover scope-in first; stack recipes wanted."
    expected: "Exotic variants are checked before declaring a rendering path safe."
  - anchor: xss-cwe-references
    what: "CWE mapping guidance for XSS findings, CWE-79 primary with context-specific relatives."
    problem: "Wrong CWE assignment breaks downstream tooling and metrics, especially when output contexts blur categories; weakness taxonomy, cwe 79, misclassification risk, tooling accuracy, reference lookup, identifier precision, reporting feeds, consistency, scanner alignment."
    use_when: "Assigning CWE identifiers to findings."
    avoid_when: "OWASP risk mapping is the question — see the OWASP anchor."
    expected: "Each finding carries the correct CWE identifier."
  - anchor: xss-ex-flask-jinja2
    what: "Flask/Jinja2 recipe contrasting `|safe` and `Markup()` misuse with default auto-escaping."
    problem: "Jinja templates render user content through safe-filter pipes or Markup wrapping, silently disabling auto-escaping; flask jinja, pipe syntax, escape bypass, python web, template inheritance, view functions, macro calls, jinja env, string concat."
    use_when: "Target uses Flask with Jinja2; reviewing template rendering paths."
    avoid_when: "Django stack — see its recipe; API-only JSON responses — see the JSON recipe."
    expected: "Escaping-disabled template constructs flagged; auto-escaped output verified."
  - anchor: xss-ex-django
    what: "Django recipe covering `|safe`, `mark_safe`, and `format_html` usage."
    problem: "Django helpers like mark_safe and format_html bypass template escaping for convenience in admin and view code; mark safe, format html, escape controls, python framework, staff panels, template tags, concat helpers, widget rendering."
    use_when: "Target uses Django templates; reviewing rendering helpers."
    avoid_when: "Flask/Jinja2 — see its recipe; non-Python stacks."
    expected: "Explicit escape-bypass helpers flagged; default escaping verified elsewhere."
  - anchor: xss-ex-php
    what: "PHP recipe contrasting raw `echo` with `htmlspecialchars` encoding."
    problem: "PHP pages echo request data directly into markup, and correct htmlspecialchars usage with ENT_QUOTES gets applied inconsistently; ent quotes, lamp stack, legacy templates, output buffering, raw output, page scripts, form echoes."
    use_when: "Target uses PHP templates; reviewing legacy rendering."
    avoid_when: "Template-engine stacks — see their recipes; non-PHP targets."
    expected: "Raw echoes flagged; properly flagged encoding verified."
  - anchor: xss-ex-express-concat
    what: "Express recipe for string-concatenated HTML responses without any template engine."
    problem: "Handlers build HTML by concatenation, skipping every escaping layer that template engines provide by default; express concat, res send, manual html, node backend, no engine, adhoc pages, join calls, template literals, router funcs."
    use_when: "Target renders HTML via string building in Express."
    avoid_when: "Template-engine rendering — see EJS or Handlebars recipes; non-JS stacks."
    expected: "Concatenated responses flagged; escaped or engine-rendered output verified."
  - anchor: xss-ex-ejs
    what: "EJS recipe contrasting escaped `<%= %>` with raw `<%- %>` output."
    problem: "EJS raw tags look nearly identical to escaped ones, so bypasses hide in plain sight during template review; tag confusion, node rendering, view layer, percent syntax, output modes, partial includes, ejs pages, include chains."
    use_when: "Target uses EJS; reviewing template tags."
    avoid_when: "Handlebars or other engines — see their recipes; non-JS stacks."
    expected: "Raw EJS tags flagged; escaped tags verified."
  - anchor: xss-ex-handlebars
    what: "Handlebars recipe contrasting double-brace escaping with triple-brace insertion and SafeString."
    problem: "Triple braces and SafeString quietly disable escaping in Handlebars views and custom helpers; safestring, node templates, brace syntax, helper misuse, view rendering, partial output, string marking, compile paths, block helpers, layout engines."
    use_when: "Target uses Handlebars; reviewing views and helpers."
    avoid_when: "EJS — see its recipe; non-JS stacks."
    expected: "Raw-output constructs flagged; escaped bindings verified."
  - anchor: xss-ex-dom-sinks
    what: "Client-side recipe: `innerHTML`, `document.write`, `eval`, `location` assignment, and `postMessage` handlers fed by DOM sources."
    problem: "Client-side scripts route location data into dangerous properties without any server round trip, evading backend-focused review entirely; innerhtml, document write, location hash, postmessage, client taint, browser flows, fragment input, url params."
    use_when: "Target has significant client-side JavaScript; reviewing browser code."
    avoid_when: "Server-rendered stacks — see their recipes; framework components — see React or Angular."
    expected: "Source-to-sink DOM flows traced and flagged."
  - anchor: xss-ex-react
    what: "React recipe covering `dangerouslySetInnerHTML`, raw `href` URLs, and the javascript-scheme caveat."
    problem: "React's escaping lulls reviewers, yet dangerouslySetInnerHTML and unvalidated URL props reopen injection inside components; react jsx, dangerously set, href schemes, jsx props, render output, scheme checks, jsx expressions, prop drilling, dom output."
    use_when: "Target uses React; reviewing components rendering user content."
    avoid_when: "Angular or Vue — see their recipes; server-side stacks."
    expected: "Explicit hatches flagged; default JSX escaping verified."
  - anchor: xss-ex-angular
    what: "Angular recipe: `bypassSecurityTrust*` calls are the real danger, while `[innerHTML]` binding is sanitized by default."
    problem: "Angular reviews false-positive on sanitized bindings while missing explicit sanitizer bypass calls in components; trust apis, framework defaults, binding contexts, template syntax, component code, security bypass, explicit trust, pipe usage, trust bypasses, directive use."
    use_when: "Target uses Angular; reviewing components with HTML binding."
    avoid_when: "React — see its recipe; server-side stacks."
    expected: "Bypass calls flagged; default-sanitized bindings not misreported."
  - anchor: xss-ex-modern-frontend
    what: "Modern frontend recipe: Svelte `{@html}`, Alpine `x-html`, HTMX content swaps, and Vue `v-html` raw directives."
    problem: "Newer frameworks render raw HTML through dedicated directives that escape checklist-style review focused on older libraries; svelte html, alpine x-html, vue v-html, raw insertion, modern stacks, spa bundles, template files, client apps."
    use_when: "Target uses Svelte, Alpine, HTMX, or Vue; reviewing component templates."
    avoid_when: "React or Angular — see their recipes; server-side stacks."
    expected: "Raw-HTML directives flagged unless fed by sanitized content."
  - anchor: xss-ex-rails
    what: "Rails recipe covering `html_safe`, `raw()`, and `content_tag` with interpolation."
    problem: "Rails helpers like html_safe and raw mark strings as trusted, disabling escaping across view layers; content tag, erb views, helper modules, string freezing, output safety, concatenated html, safe buffers, render calls."
    use_when: "Target uses Rails views; reviewing helpers and templates."
    avoid_when: "Non-Ruby codebases; API-only Rails in JSON mode."
    expected: "Trust-marking helpers flagged; default ERB escaping verified."
  - anchor: xss-ex-jsp
    what: "JSP recipe covering scriptlet output, `<%= %>`, and JSTL escaping via `c:out`."
    problem: "JSP pages mix scriptlets with EL output, and only c:out provides consistent escaping across templates; jstl c out, java views, escape functions, legacy java, page directives, expression language, tag files, servlet containers."
    use_when: "Target uses JSP; reviewing view templates."
    avoid_when: "Thymeleaf — see its recipe; non-Java stacks."
    expected: "Scriptlet output flagged; JSTL escaping verified."
  - anchor: xss-ex-thymeleaf
    what: "Thymeleaf recipe contrasting `th:text` with `th:utext` and script-inlining mode."
    problem: "Thymeleaf's utext attribute and inlined scripts bypass escaping applied to standard text binding; escape modes, spring mvc, template engines, view resolvers, model attributes, dialect features, fragment usage, layout, th attributes, processor chains."
    use_when: "Target uses Thymeleaf; reviewing Spring views."
    avoid_when: "JSP — see its recipe; non-Java stacks."
    expected: "Unescaped attributes flagged; default escaping verified."
  - anchor: xss-ex-go-templates
    what: "Go recipe contrasting auto-escaping `html/template` with non-escaping `text/template` and `template.HTML` casts."
    problem: "Go services render user content through text/template or HTML type casts, bypassing contextual auto-escaping entirely; golang rendering, cast misuse, context escaping, template packages, buffer writes, execute calls, parse files, handler output, writer output."
    use_when: "Target uses Go templates; reviewing rendering code."
    avoid_when: "Non-Go stacks; JSON-only services."
    expected: "Non-escaping renderers and casts flagged; html/template usage verified."
  - anchor: xss-ex-razor
    what: "Razor recipe covering `@Html.Raw`, `MvcHtmlString`, and default `@var` encoding."
    problem: "Razor's Html.Raw and MvcHtmlString bypass encoding applied to normal expressions in views; aspnet views, dotnet rendering, encode helpers, page models, tag helpers, cshtml files, view components, partial renders, raw strings, mvc apps."
    use_when: "Target uses ASP.NET Razor views; reviewing cshtml."
    avoid_when: "Non-.NET stacks; Web API JSON-only endpoints."
    expected: "Raw-output helpers flagged; default encoding verified."
  - anchor: xss-ex-markdown
    what: "Markdown pipeline recipe: user markdown converted to HTML without sanitization."
    problem: "Markdown renderers pass through raw HTML unless sanitized, turning comment and wiki features into stored injection; wiki pages, sanitization gap, md libraries, rich text, html blocks, preview panes, comment forms, inline html."
    use_when: "Target renders user-supplied Markdown; reviewing comment or doc features."
    avoid_when: "Plain-text rendering — out of scope; template injection wanted instead."
    expected: "Unsanitized Markdown pipelines flagged; render-then-sanitize verified."
  - anchor: xss-ex-json-frontend
    what: "JSON-response recipe: API data later rendered by a frontend without escaping."
    problem: "APIs return user content in JSON assuming clients escape it, but downstream rendering sits outside API control entirely; frontend rendering, client escaping, contract assumptions, downstream risk, spa consumers, browser clients, data binding."
    use_when: "Target is a JSON API consumed by browsers; assessing shared responsibility."
    avoid_when: "Server-rendered stacks — see their recipes; clients known to escape."
    expected: "Unescaped-content responses documented with downstream rendering assessed."
  - anchor: xss-execution-intro
    what: "Execution overview: three phases run by subagents with the architecture report passed as context to each."
    problem: "Detection work without orchestration structure duplicates effort and loses batch boundaries across phases; execution model, phase overview, subagent orchestration, context passing, batch discipline, workflow entry, staging, dispatch plan, coordination, uniform."
    use_when: "Starting the XSS scan execution; deciding how to dispatch subagents."
    avoid_when: "Specific phase prompts are needed — jump to phase anchors."
    expected: "All three phases dispatched with shared architecture context."
  - anchor: xss-phase1-recon
    what: "Recon prompt instructing the subagent to find every sink site with per-engine patterns and skip lists."
    problem: "Unstructured searching misses sinks or floods candidates with auto-escaped code, so recon needs explicit patterns and exclusions; site discovery, skip rules, candidate quality, coverage discipline, grep scope, noise control, thorough sweep, broad net."
    use_when: "Launching the recon subagent; reviewing recon completeness."
    avoid_when: "Candidates already gathered — proceed to verify; conceptual knowledge wanted."
    expected: "Complete, de-duplicated candidate list of sink sites."
  - anchor: xss-phase1-gate
    what: "Zero-candidate short-circuit: emit a clean no-findings stub and stop when recon finds nothing."
    problem: "Pipeline without early exit wastes verify batches on empty candidate sets and leaves missing artifacts; empty recon, pipeline efficiency, artifact completeness, stop rule, graceful halt, zero results, skipped verify, idle batches."
    use_when: "Recon returned zero candidates."
    avoid_when: "Candidates exist — proceed to batched verification."
    expected: "No-findings stub written and the scan stops gracefully."
  - anchor: xss-phase2-verify
    what: "Batched taint-tracing prompt linking user input to sinks, with the mitigation decision list and classification labels."
    problem: "Unverified candidates are noise, and defenses from escaping to CSP differ in strength, so decision-list verification is required; taint tracing, batch processing, parallel analysis, evidence demand, defense tiers, label assignment, trace completeness, site verdicts."
    use_when: "Candidates confirmed present; dispatching verify subagents in batches of three."
    avoid_when: "Recon incomplete; merge stage is the need."
    expected: "Every candidate classified against its mitigation with traced evidence."
  - anchor: xss-phase3-merge
    what: "Merge procedure consolidating batch reports into the final module report with dedup and the output template."
    problem: "Parallel batch outputs overlap and diverge, and without merge discipline final reports duplicate or lose findings; result merging, dedup, consolidation, final template, partial results, report integrity, clean handoff, overlap removal, single output."
    use_when: "All verify batches finished; producing `04_xss.md`."
    avoid_when: "Batches still running; recon stage not done."
    expected: "Single consolidated module report with unique, classified findings."
  - anchor: xss-owasp-mapping
    what: "Mapping of XSS findings to OWASP API 2023 risks, routed via API8 and API10 since 2023 has no XSS category."
    problem: "Findings need correct 2023-era taxonomy, and assuming dedicated injection categories mislabels everything downstream; taxonomy mapping, risk routing, classification accuracy, edition awareness, correct tagging, traceability, category shift, compliance notes, risk labels."
    use_when: "Tagging findings with OWASP 2023 risks; writing the report's risk section."
    avoid_when: "CWE-level tagging is the question — see the CWE anchor."
    expected: "Findings mapped to the correct risks with explicit reasoning."
  - anchor: xss-csp-best-practices
    what: "CSP guidance for APIs: JSON content types, restrictive default-src for responses, nonce/hash script-src with strict-dynamic for docs UIs, nosniff, frame-ancestors, and require-trusted-types-for."
    problem: "API teams skip browser defenses assuming no rendering, leaving docs UIs and browser-opened responses unprotected; csp headers, defense in depth, docs hardening, nonce hashes, strict dynamic, browser clients, header hygiene, policy audit."
    use_when: "Writing remediation; reviewing headers on API responses and documentation interfaces."
    avoid_when: "CSP already audited as sufficient; detection mechanics are the question."
    expected: "Response and docs headers hardened with modern CSP directives."
  - anchor: xss-references
    what: "External link list for XSS concepts, guidance documents, and browser security APIs."
    problem: "Agents and readers need authoritative follow-up sources beyond this file's distilled content; further reading, external canon, deep dives, vendor documentation, community knowledge, primary material, cited works, mdn pages, owasp guides."
    use_when: "Primary sources or extended material is needed."
    avoid_when: "Detection recipes or execution workflow are the question — the references list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
  - anchor: xss-reminders
    what: "Operational guardrails: CSP alone is not a fix, bypass calls are always suspicious, evidence requirements."
    problem: "Under pressure, agents accept CSP as mitigation, miss sanitizer bypasses, or overstate severity, corrupting report quality; mitigation rigor, evidence demand, severity honesty, quality guardrails, review discipline, trap avoidance, false comfort, checklist, final pass."
    use_when: "Reviewing draft findings before merge; calibrating classifications."
    avoid_when: "Specific sink contexts or payload syntax are the question — see the sink and payload anchors; this card only guards finding quality."
    expected: "Merged findings carry proof for every claim, CSP never counted as a standalone fix, and severity matches demonstrated impact."
---

# Cross-Site Scripting (XSS) Detection

[ref: #xss-detection]

You are performing a focused security assessment to find Cross-Site Scripting vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **recon** (find sink sites), **batched verify** (trace taint for parallel batches of up to 3 sinks each), and **merge** (consolidate batch results into one report).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

**Subagent constraint for this reference**: This is a detection reference. Subagents perform scanning, tracing, and reporting only. They must **not modify any project source file** unless a separate remediation task is explicitly authorized.

***

## What is XSS
[ref: #xss-definition]

XSS occurs when user-supplied input is incorporated into a web page's HTML, JavaScript, or DOM without proper escaping or sanitization. This allows attackers to inject and execute arbitrary scripts in victims' browsers, leading to session hijacking, credential theft, defacement, and malware distribution.

The core pattern: *unescaped, unsanitized user input reaches an HTML/JS/DOM output sink.*

### XSS Types
[ref: #xss-types]

- **Reflected XSS**: User input is immediately echoed back in the HTTP response (e.g., a search term rendered directly into the page HTML).
- **Stored XSS**: User input is saved to persistent storage (database, file) and later rendered in HTML for other users.
- **DOM-based XSS**: Client-side JavaScript reads from an attacker-controlled source (`location.search`, `location.hash`, `document.cookie`) and writes to a dangerous DOM sink (`innerHTML`, `eval`, `document.write`) without server involvement.

### What XSS IS
[ref: #xss-scope-in]

**Server-side HTML sinks** — rendering user data into HTML responses without escaping:
- Python/Jinja2: `{{ var | safe }}`, `{% autoescape off %}...{{ var }}...{% endautoescape %}`
- Python/Django: `mark_safe(var)`, `format_html(...)` with `%s` and unescaped input, `{{ var | safe }}` in templates
- Python/Flask: `Markup(var)`, `render_template_string(f"...{var}...")`
- PHP: `echo $var`, `print $var`, `<?= $var ?>` without `htmlspecialchars()`
- Ruby/Rails: `raw(var)`, `var.html_safe`, `<%= raw var %>`, `content_tag` with `.html_safe`
- Java/JSP: `<%= var %>`, `${var}` without `<c:out>` or `fn:escapeXml()`
- Java/Thymeleaf: `th:utext="${var}"` (unescaped), `[(${var})]`
- Go/html-template misuse: using `template.HTML(var)`, `template.JS(var)`, `template.URL(var)` to bypass auto-escaping
- C#/Razor: `@Html.Raw(var)`, `MvcHtmlString.Create(var)`
- Node.js/EJS: `<%- var %>` (unescaped), vs `<%= var %>` (safe)
- Node.js/Handlebars: `{{{ var }}}` (triple-brace, unescaped)
- Node.js/Pug: `!{var}` (unescaped)
- Express: `res.send("<html>..." + var + "...")`, `res.write("<p>" + var + "</p>")`

**Client-side DOM sinks** — JavaScript writing user-controlled data to the DOM unsafely:
- `element.innerHTML = var`
- `element.outerHTML = var`
- `document.write(var)`, `document.writeln(var)`
- `element.insertAdjacentHTML('beforeend', var)`
- jQuery: `$(element).html(var)`, `$(element).append(var)` (when var contains HTML), `$('<div>' + var + '</div>')`
- React: `dangerouslySetInnerHTML={{ __html: var }}`
- Angular: `[innerHTML]="var"`, `bypassSecurityTrustHtml(var)`, `bypassSecurityTrustScript(var)`, `bypassSecurityTrustUrl(var)`
- Vue: `v-html="var"`

**JavaScript execution sinks** — user-controlled data evaluated as code:
- `eval(var)`
- `setTimeout(var, delay)` / `setInterval(var, delay)` when `var` is a string
- `new Function(var)()`
- `element.setAttribute('onclick', var)`, `element.setAttribute('href', 'javascript:' + var)`
- `location.href = var`, `location.replace(var)`, `location.assign(var)` (when var is user-controlled and can be `javascript:...`)
- `element.src = var`, `element.action = var` (script injection via `javascript:` URIs)
- `scriptElement.text = var`, `scriptElement.textContent = var`

**DOM-based sources** — attacker-controlled inputs read by client-side JavaScript:
- `location.search` (URL query string)
- `location.hash` (URL fragment)
- `location.href`
- `document.referrer`
- `document.URL`, `document.documentURI`
- `document.cookie`
- `postMessage` event data (`event.data`)
- `window.name`
- `localStorage.getItem(...)`, `sessionStorage.getItem(...)` (if populated from URL or postMessage)

### API-Specific XSS Contexts
[ref: #xss-api-contexts]

API-first codebases expose additional XSS vectors that do not fit the traditional server-rendered page model. Flag these when the API response or documentation interface is rendered by a browser.

| Context | Example | Detection signal |
| --- | --- | --- |
| JSON responses rendered by frontend | `{"message": "Hello <script>alert(1)</script>"}` | API returns HTML-like strings inside JSON that an SPA renders with `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, or `[innerHTML]`. |
| OpenAPI/Swagger UI injection | Parameter descriptions or examples rendered as HTML in Swagger UI | User-controlled strings in OpenAPI spec annotations, YAML/JSON spec files, or doc strings rendered by Swagger UI. |
| GraphQL introspection/playground UI | Malicious type/field descriptions or default values | Introspection or GraphQL Playground enabled in production; schema descriptions reflect unsanitized input. |
| API error pages echoing request paths/headers | `404 — /api/<script>alert(1)</script> not found` | Error handlers that echo `request.path`, `request.url`, or header values without encoding. |
| Markdown/rendered content | API stores markdown and renders it to clients | Missing sanitization of markdown HTML output (e.g., `markdown-it` without `html: false` and an allowlist). |
| File upload XSS | Uploaded SVG/HTML/PDF with embedded JS served from API domain | Upload endpoints that serve files with `Content-Type: text/html`, inline SVG, or `Content-Disposition: inline`. |
| API docs/static pages | Custom API documentation pages that echo query parameters or paths | Same detection signals as reflected XSS, but on docs/playground endpoints. |

### What XSS is NOT
[ref: #xss-scope-out]

Do not flag these as XSS:

- **CSRF**: Forging requests on behalf of a user — a separate vulnerability class
- **SQLi via XSS**: Injecting SQL through an XSS vector — the SQL injection itself is the primary finding
- **Clickjacking**: Embedding pages in iframes — different vulnerability class
- **Header injection**: Injecting newlines into HTTP response headers — separate class (HTTP Response Splitting)
- **Safe template output**: Auto-escaped `{{ var }}` in Jinja2/Django/Twig/Blade/Handlebars double-brace syntax with auto-escaping on — these are safe
- **`textContent` / `innerText`**: These write plain text only; no HTML parsing occurs — safe

### Patterns That Prevent XSS
[ref: #xss-prevention-patterns]

When you see these patterns, the code is likely **not vulnerable**:

**1. Context-aware auto-escaping (most template engines default)**
```
# Jinja2 / Django (auto-escape on by default)
{{ var }}          # HTML-escaped → safe

# EJS
<%= var %>         # HTML-escaped → safe

# Handlebars
{{ var }}          # HTML-escaped → safe

# Pug
= var              # HTML-escaped → safe

# Thymeleaf
th:text="${var}"   # HTML-escaped → safe

# Razor (C#)
@var               # HTML-encoded → safe
```

**2. Explicit escaping before output**
```php
// PHP
echo htmlspecialchars($var, ENT_QUOTES, 'UTF-8');
```
```ruby
# Rails
<%= h(var) %>
<%= ERB::Util.html_escape(var) %>
```
```java
// JSP with JSTL
<c:out value="${var}"/>
// or fn:escapeXml()
${fn:escapeXml(var)}
```
```go
// html/template — auto-escapes by context (HTML, JS, URL, CSS)
{{.Var}}   // safe inside html/template
```

**3. DOM manipulation using safe properties**
```javascript
element.textContent = userInput;   // plain text, no HTML parsing — safe
element.innerText = userInput;     // plain text — safe
```

**4. Sanitization with an allowlisted HTML library**
```javascript
// DOMPurify
element.innerHTML = DOMPurify.sanitize(userInput);

// sanitize-html with strict config
const clean = sanitizeHtml(userInput, { allowedTags: [], allowedAttributes: {} });
```

**5. React / Angular / Vue auto-escaping**
Framework JSX/templates escape interpolated values by default; only explicit escape hatches (`dangerouslySetInnerHTML`, `bypassSecurityTrust*`, `v-html`) are dangerous.

**6. Trusted Types (Baseline since 2026) and the Sanitizer API (standardized, limited availability)**
Trusted Types (`require-trusted-types-for 'script'` CSP directive + a `trustedTypes` policy) blocks DOM-XSS at the sink: assignments to `innerHTML`/`eval`-family properties throw unless the value comes from a sanitizing policy. Baseline across all major engines since early 2026 (Chrome/Edge 83+, Safari 26+, Firefox 148+). The Sanitizer API's `Element.setHTML(input)` sanitizes markup natively before insertion — prefer it over `innerHTML` for user-influenced HTML. Caveat: as of 2026-07 the Sanitizer API is standardized but shipped only in Firefox 148+ (2026-02) — MDN classes it as limited availability, not Baseline; other engines still need an allowlist library (DOMPurify, `sanitize-html`), so do not treat `setHTML` alone as a portable mitigation yet.
```jsx
// React JSX — auto-escaped
return <div>{userInput}</div>;
```
```html
<!-- Angular — auto-escaped -->
<div>{{ userInput }}</div>
<!-- Vue — auto-escaped -->
<div>{{ userInput }}</div>
```

### Context-Aware Output Encoding
[ref: #xss-output-encoding]

XSS prevention depends on the exact output context. The same variable may be safe in an HTML body with HTML-encoding, but dangerous in a JavaScript string literal, URL attribute, or CSS context. Subagents must classify sinks according to the context in which the variable is rendered.

| Output context | Encoding / handling requirement | Example unsafe → safe |
| --- | --- | --- |
| HTML body | HTML-encode `<`, `>`, `&`, `"`, `'` | `<script>` → `&lt;script&gt;` |
| HTML attribute | Attribute-encode; quote attributes with single or double quotes | `onclick=alert(1)` → `onclick="alert&#40;1&#41;"` |
| JavaScript string literal | JavaScript-encode the string; do not inject via template interpolation | `"'; alert(1)//` → `\x22\x3b\x20alert\x281\x29\x2f\x2f` |
| URL (`href`, `src`, action) | URL-encode; validate scheme is `http:`, `https:`, or expected safe scheme; reject `javascript:`, `data:`, `vbscript:` | `javascript:alert(1)` → reject or encode to safe URL |
| CSS | CSS-hex-encode or reject dangerous constructs | `expression(alert(1))` → reject or encode |
| JSON | JSON-serialize without HTML-breaking characters; set `Content-Type: application/json` | Use `JSON.stringify()` rather than string concatenation. |
| Markdown | Render with HTML disabled or pass through an allowlist sanitizer; strip script tags and event handlers | Raw markdown → sanitized HTML only |

Important context rules:
- **HTML attribute unquoted context** is especially dangerous: `value={{ var }}` can be broken with a space. Always quote attributes.
- **JavaScript template literals** (backticks) are vulnerable if user input is interpolated: `` const x = `${userInput}`; ``. Use library encoders or avoid interpolation.
- **`data:` URIs** in `src`/`href` can carry HTML or JavaScript. Treat them as executable content.
- **JSONP endpoints** that wrap user-controlled input in a JavaScript callback are inherently XSS-prone.

### Advanced XSS Variant Patterns
[ref: #xss-advanced-variants]

Subagents must also watch for these non-obvious XSS variants:

| Variant | Mechanism | Detection signal |
| --- | --- | --- |
| **mXSS / mutation XSS** | InnerHTML mutates sanitization-safe markup into executable code after parser mutation. | DOMPurify config missing `SANITIZE_DOM`, `KEEP_CONTENT` misuse, or output passed back through `innerHTML` after sanitization. |
| **DOM clobbering** | HTML `id`/`name` attributes shadow JavaScript variables on `window`/`document`, altering script behavior. | Client code reads from `window` / `document` without `hasOwnProperty` checks; forms or anchors with attacker-controlled `id`/`name`. |
| **Prototype pollution → DOM XSS** | Polluted `Object.prototype` properties reach DOM sinks or control flow. | `Object.assign`, `lodash.merge`, recursive `merge` with user input on `Object.prototype`; later use in sink arguments. |
| **XSS via file uploads** | SVG with `<script>`, HTML upload served same-origin, or PDF with JavaScript action. | Upload directory served with wrong MIME type; `Content-Disposition: inline`; no content-type validation; user-controlled filenames rendered without escaping. |
| **PDF XSS** | PDF with JavaScript action opens in browser and executes. | API generates or serves PDFs with user-controlled content or metadata. |
| **Template injection → XSS** | Server-side template injection (SSTI) produces raw HTML/JS output. | `render_template_string` with f-strings, `eval`-like template engines, or user-controlled template source. |
| **Open redirect → XSS** | User-controlled redirect target is a `javascript:` URI or data URI. | `location.href = redirectUrl` where `redirectUrl` is attacker-controlled. |

### CWE References
[ref: #xss-cwe-references]

Map XSS findings to the appropriate CWE entries:

- **CWE-79**: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') — primary XSS mapping.
- **CWE-80**: Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS).
- **CWE-81**: Improper Neutralization of Script in an Error Message Web Page.
- **CWE-83**: Improper Neutralization of Script in Attributes in a Web Page.
- **CWE-116**: Improper Encoding or Escaping of Output.
- **CWE-692**: Incomplete Denylist to Cross-Site Scripting — flag when custom regex blacklisting or incomplete sanitization is used.

***

## Vulnerable vs. Secure Examples

### Python — Flask / Jinja2
[ref: #xss-ex-flask-jinja2]

```python
# VULNERABLE: Markup() bypasses Jinja2 auto-escaping
@app.route('/greet')
def greet():
    name = request.args.get('name', '')
    return render_template_string(f"<h1>Hello, {name}!</h1>")   # raw f-string, no template escaping

# VULNERABLE: mark_safe equivalent
@app.route('/profile')
def profile():
    bio = request.args.get('bio', '')
    return render_template('profile.html', bio=Markup(bio))      # Markup() marks it as safe, bypassing escaping

# SECURE: use template with auto-escaping (never pass Markup around user input)
@app.route('/greet')
def greet():
    name = request.args.get('name', '')
    return render_template('greet.html', name=name)              # template: {{ name }} — auto-escaped
```

### Python — Django
[ref: #xss-ex-django]

```python
# VULNERABLE: mark_safe() with user input
def user_bio(request):
    bio = request.GET.get('bio', '')
    safe_bio = mark_safe(bio)   # user input bypasses Django's auto-escaping
    return render(request, 'bio.html', {'bio': safe_bio})

# SECURE: pass raw string; template handles escaping
def user_bio(request):
    bio = request.GET.get('bio', '')
    return render(request, 'bio.html', {'bio': bio})   # template: {{ bio }} — auto-escaped
```

### PHP
[ref: #xss-ex-php]

```php
// VULNERABLE: echo without escaping
function showUsername($username) {
    echo "<p>Welcome, " . $username . "</p>";
}

// SECURE: htmlspecialchars
function showUsername($username) {
    echo "<p>Welcome, " . htmlspecialchars($username, ENT_QUOTES, 'UTF-8') . "</p>";
}
```

### Node.js — Express (string concatenation)
[ref: #xss-ex-express-concat]

```javascript
// VULNERABLE: user input concatenated into HTML response
app.get('/search', (req, res) => {
  const query = req.query.q;
  res.send(`<h1>Results for: ${query}</h1>`);
});

// SECURE: use a template engine with auto-escaping, or escape manually
const escapeHtml = require('escape-html');
app.get('/search', (req, res) => {
  const query = req.query.q;
  res.send(`<h1>Results for: ${escapeHtml(query)}</h1>`);
});
```

### Node.js / EJS
[ref: #xss-ex-ejs]

```html
<!-- VULNERABLE: unescaped output -->
<div><%- userInput %></div>

<!-- SECURE: escaped output -->
<div><%= userInput %></div>
```

### Node.js / Handlebars
[ref: #xss-ex-handlebars]

```html
<!-- VULNERABLE: triple-brace, unescaped -->
<div>{{{ userInput }}}</div>

<!-- SECURE: double-brace, auto-escaped -->
<div>{{ userInput }}</div>
```

### JavaScript — DOM Sinks
[ref: #xss-ex-dom-sinks]

```javascript
// VULNERABLE: innerHTML with URL fragment
const name = location.hash.substring(1);
document.getElementById('greeting').innerHTML = 'Hello, ' + name;

// SECURE: textContent
const name = location.hash.substring(1);
document.getElementById('greeting').textContent = 'Hello, ' + name;
```

```javascript
// VULNERABLE: eval with postMessage data
window.addEventListener('message', (event) => {
  eval(event.data);
});

// SECURE: parse and validate; never eval postMessage data
window.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  // handle data safely
});
```

### React
[ref: #xss-ex-react]

```jsx
// VULNERABLE: dangerouslySetInnerHTML with user input
function Comment({ content }) {
  return <div dangerouslySetInnerHTML={{ __html: content }} />;
}

// SECURE: render as text (auto-escaped by React)
function Comment({ content }) {
  return <div>{content}</div>;
}
```

Also check URL props: `href={userUrl}` accepts `javascript:` URLs in older React versions (≥16.9 only warns) — validate the scheme (`https?:` allowlist) before rendering user-controlled links.

### Angular
[ref: #xss-ex-angular]

```typescript
// VULNERABLE: bypassing Angular's DomSanitizer
constructor(private sanitizer: DomSanitizer) {}
getUserHtml(input: string): SafeHtml {
  return this.sanitizer.bypassSecurityTrustHtml(input);  // unsafe if input is user-controlled
}
```

```html
<!-- NOT vulnerable by itself: Angular sanitizes [innerHTML] bindings via DomSanitizer by default (scripts/handlers stripped) -->
<div [innerHTML]="userInput"></div>

<!-- VULNERABLE: explicitly bypassing the sanitizer -->
<div [innerHTML]="sanitizer.bypassSecurityTrustHtml(userInput)"></div>

<!-- SECURE: use interpolation (auto-escaped) -->
<div>{{ userInput }}</div>
```

### Modern frontend — Svelte / Alpine.js / HTMX / Vue
[ref: #xss-ex-modern-frontend]

```svelte
<!-- VULNERABLE: Svelte {@html} renders raw HTML with NO sanitization -->
<p>{@html userComment}</p>

<!-- SECURE: plain interpolation escapes by default -->
<p>{userComment}</p>
```

```html
<!-- VULNERABLE: Alpine.js x-html sets innerHTML directly (docs warn: trusted content only) -->
<div x-data="{ comment: userInput }" x-html="comment"></div>

<!-- VULNERABLE: HTMX swaps use innerHTML semantics — a server response built from user input executes -->
<div hx-get="/comment/123" hx-trigger="load"></div>

<!-- VULNERABLE: Vue v-html bypasses escaping (Vue 3 same rule) -->
<div v-html="userComment"></div>
```

Detection rule for all four: raw-HTML directives (`{@html}`, `x-html`, `v-html`, `hx-*` with server-rendered fragments) are safe only when the injected HTML is built from trusted, already-sanitized content.

### Ruby on Rails
[ref: #xss-ex-rails]

```erb
<%# VULNERABLE: raw() or html_safe with user input %>
<%= raw(@user.bio) %>
<%= @user.bio.html_safe %>

<%# SECURE: default ERB escaping %>
<%= @user.bio %>
```

### Java — JSP
[ref: #xss-ex-jsp]

```jsp
<%-- VULNERABLE: scriptlet echo --%>
<p>Hello, <%= request.getParameter("name") %></p>

<%-- VULNERABLE: EL without c:out --%>
<p>Hello, ${param.name}</p>

<%-- SECURE: c:out escaping --%>
<p>Hello, <c:out value="${param.name}"/></p>
```

### Java — Thymeleaf
[ref: #xss-ex-thymeleaf]

```html
<!-- VULNERABLE: unescaped th:utext -->
<div th:utext="${userInput}"></div>

<!-- VULNERABLE: unescaped inline expression -->
<div>[[${userInput}]]</div>

<!-- SECURE: escaped th:text -->
<div th:text="${userInput}"></div>
```

### Go — html/template vs. text/template
[ref: #xss-ex-go-templates]

```go
// VULNERABLE: using text/template (no HTML escaping)
import "text/template"
tmpl := template.Must(template.New("").Parse("<h1>Hello, {{.Name}}!</h1>"))
tmpl.Execute(w, data)

// VULNERABLE: using template.HTML() cast to bypass escaping
import "html/template"
name := template.HTML(r.URL.Query().Get("name"))   // bypasses auto-escaping

// SECURE: html/template with plain string value
import "html/template"
tmpl := template.Must(template.New("").Parse("<h1>Hello, {{.Name}}!</h1>"))
tmpl.Execute(w, data)   // .Name is a plain string — auto-escaped
```

### C# — Razor / ASP.NET MVC
[ref: #xss-ex-razor]

```html
<!-- VULNERABLE: Html.Raw with user-controlled input -->
<div>@Html.Raw(userInput)</div>

<!-- VULNERABLE: MvcHtmlString.Create with user input -->
@{
    var html = MvcHtmlString.Create(userInput);
}
@html

<!-- SECURE: default Razor HTML encoding -->
<div>@userInput</div>

<!-- SECURE: explicit HTML encoding -->
<div>@Html.Encode(userInput)</div>
```

### Markdown Rendering
[ref: #xss-ex-markdown]

```python
# VULNERABLE: rendering user markdown with HTML enabled
import markdown
html = markdown.markdown(user_markdown)   # html=True by default in some versions

# SECURE: disable raw HTML and use an allowlist extension
import markdown
html = markdown.markdown(user_markdown, extensions=['mdx_bleach'])   # or sanitize after render
```

### JSON Response Rendered by Frontend
[ref: #xss-ex-json-frontend]

```javascript
// VULNERABLE: API returns JSON with HTML-like string, SPA renders it as HTML
// API:
app.get('/greeting', (req, res) => {
  res.json({ message: req.query.name });   // no escaping
});

// SPA:
element.innerHTML = data.message;

// SECURE: SPA treats JSON value as text, or API encodes if intended for HTML
element.textContent = data.message;
```

***

## Execution
[ref: #xss-execution-intro]

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Find XSS Sink Sites
[ref: #xss-phase1-recon]

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where data is rendered into HTML, JavaScript, or the DOM in a way that could allow script injection — any unescaped or explicitly-marked-safe output, any dangerous DOM property assignment, any JavaScript execution sink. Write results to `{{ REPORTS_ROOT }}/04_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the frontend stack, template engines, server-side rendering frameworks, and any client-side JavaScript patterns.
>
> **What to search for — vulnerable sink patterns**:
>
> Flag ANY dynamic variable passed to a dangerous output sink. You are not yet checking whether the variable is user-controlled — that is Phase 2's job.
>
> **1. Server-side template unescaped output**:
>    - Jinja2/Django: `{{ var | safe }}`, `{% autoescape off %}`, `Markup(var)`, `mark_safe(var)`, `format_html(...)` with direct user-controlled format args
>    - EJS: `<%- var %>`
>    - Handlebars/Mustache: `{{{ var }}}`
>    - Pug: `!{var}`
>    - Thymeleaf: `th:utext="${var}"`, `[(${var})]`
>    - Twig: `{{ var | raw }}`
>    - Blade (Laravel): `{!! $var !!}`
>    - Rails ERB: `raw(var)`, `var.html_safe`, `<%= raw var %>`
>    - PHP: `echo $var`, `print $var`, `<?= $var ?>` without `htmlspecialchars()`
>    - Go: `template.HTML(var)`, `template.JS(var)`, `template.URL(var)`, usage of `text/template` for HTML output
>    - C#/Razor: `@Html.Raw(var)`, `MvcHtmlString.Create(var)`
>
> **2. Direct HTML string construction in server-side code**:
>    - String concatenation or interpolation building an HTML response: `res.send("<p>" + var + "</p>")`, `f"<h1>{var}</h1>"`, `"<div>" + var + "</div>"`
>    - `render_template_string(f"...{var}...")` in Flask
>
> **3. Client-side DOM sinks**:
>    - `element.innerHTML = var`
>    - `element.outerHTML = var`
>    - `document.write(var)`, `document.writeln(var)`
>    - `element.insertAdjacentHTML(position, var)`
>    - jQuery: `$(el).html(var)`, `$(el).append(var)`, `$('<tag>' + var + '</tag>')`, `$.parseHTML(var)` passed to DOM
>    - React: `dangerouslySetInnerHTML={{ __html: var }}`
>    - Angular: `[innerHTML]="var"`, `bypassSecurityTrustHtml(var)`, `bypassSecurityTrustScript(var)`, `bypassSecurityTrustUrl(var)`, `bypassSecurityTrustStyle(var)`, `bypassSecurityTrustResourceUrl(var)`
>    - Vue: `v-html="var"`
>
> **4. JavaScript execution sinks**:
>    - `eval(var)`
>    - `setTimeout(var, ...)` / `setInterval(var, ...)` where `var` is a string variable (not a function reference)
>    - `new Function(var)()`
>    - `scriptElement.text = var`, `scriptElement.textContent = var`
>    - `element.setAttribute('onclick', var)`, `element.setAttribute('href', 'javascript:' + var)`, and similar event-handler attribute assignments
>    - URL-based sinks where `javascript:` URIs could execute: `location.href = var`, `location.replace(var)`, `element.src = var`, `element.action = var`
>
> **5. DOM-based XSS patterns** — client-side code reading from attacker-controlled sources and passing to any sink above:
>    - Reading from: `location.search`, `location.hash`, `location.href`, `document.referrer`, `document.URL`, `document.cookie`, `window.name`, `postMessage` handler (`event.data`), `URLSearchParams`
>    - Then passing to an HTML or JS sink without escaping
>
> **6. API-specific XSS contexts**:
>    - JSON responses that contain HTML/JS strings later rendered by a browser client via `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, or `[innerHTML]`
>    - OpenAPI/Swagger UI parameter descriptions, examples, or spec content derived from user input
>    - GraphQL introspection or Playground UI descriptions/default values derived from user input
>    - API error pages that echo `request.path`, `request.url`, headers, or query parameters
>    - Markdown rendering endpoints that return unsanitized HTML
>    - File upload endpoints serving SVG, HTML, or PDF with inline disposition or wrong MIME type
>
> **What to skip** (these are safe output patterns — do not flag):
> - Auto-escaped template output: `{{ var }}` in Jinja2 (auto-escape on), `<%= var %>` in EJS, `{{ var }}` in Handlebars double-brace, `@var` in Razor, `th:text` in Thymeleaf
> - `element.textContent = var` and `element.innerText = var` — no HTML parsing, safe
> - React JSX `{var}` — auto-escaped
> - Angular `{{ var }}` interpolation — auto-escaped
> - Vue `{{ var }}` interpolation — auto-escaped
> - `DOMPurify.sanitize(var)` wrapping an innerHTML assignment — typically safe (verify config)
> - `sanitize-html`, `xss`, or similar allowlist sanitizer library wrapping output
>
> **Output format** — write to `{{ REPORTS_ROOT }}/04_recon.md`:
>
> ```markdown
> # XSS Recon: [Project Name]
>
> ## Summary
> Found [N] locations where data is rendered into HTML/JS/DOM without guaranteed escaping.
>
> ## Sink Sites
>
> ### 1. [Descriptive name — e.g., "innerHTML assignment in search results handler"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint / component**: [function name, route, or component]
> - **Sink type**: [server-side template / HTML string concat / DOM innerHTML / eval / JS execution sink / DOM-based source-to-sink / API-specific]
> - **Sink call**: [the exact API or property used — e.g., `innerHTML`, `mark_safe()`, `<%- %>`]
> - **Interpolated variable(s)**: `var_name` — [brief note, e.g., "unknown origin" or "looks like user profile field"]
> - **Output context**: [HTML body / HTML attribute / JS string / URL / CSS / JSON / Markdown]
> - **XSS type**: [Reflected / Stored / DOM-based / API-specific — best guess at this stage]
> - **Code snippet**:
>   ```
>   [the vulnerable sink code]
>   ```
>
> [Repeat for each site]
> ```

### After Phase 1: Check for Candidates Before Proceeding
[ref: #xss-phase1-gate]

After Phase 1 completes, read `{{ REPORTS_ROOT }}/04_recon.md`. If the recon found **zero sink sites** (the summary reports "Found 0" or the "Sink Sites" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/04_xss.md` and stop (you may delete `{{ REPORTS_ROOT }}/04_recon.md` after writing):

```markdown
# XSS Analysis Results

No vulnerabilities found.
```

Only proceed to Phase 2 if Phase 1 found at least one sink site.

### Phase 2: Verify — Trace User Input to Sinks (Batched)
[ref: #xss-phase2-verify]

After Phase 1 completes, read `{{ REPORTS_ROOT }}/04_recon.md` and split the sink sites into **batches of up to 3 sink sites each**. Launch **one subagent per batch in parallel**. Each subagent traces taint only for its assigned sinks and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/04_recon.md` and count the numbered sink sections (### 1., ### 2., etc.).
2. Divide them into batches of up to 3. For example, 8 sinks → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those sink sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sinks.
5. Each subagent writes to `{{ REPORTS_ROOT }}/04_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project uses React with an Express API, include the relevant Node.js and React examples. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned XSS sink site, determine whether a user-supplied value reaches the output variable. Write results to `{{ REPORTS_ROOT }}/04_batch_[N].md`.
>
> **Your assigned sink sites** (from the recon phase):
>
> [Paste the full text of the assigned sink sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand request entry points, data flows, middleware, and client-side data sources.
>
> **For each sink site, trace the interpolated variable(s) backwards to their origin**:
>
> **User-controlled sources to look for:**
>
> 1. **HTTP request sources** (server-side):
>    - Query parameters: `request.GET.get(...)`, `req.query.x`, `params[:x]`, `$_GET['x']`, `c.Query("x")`, `r.URL.Query().Get("x")`
>    - Path parameters: `request.path_params['id']`, `req.params.id`, `params[:id]`, `$_GET['id']`
>    - Request body / form fields: `request.POST.get(...)`, `req.body.x`, `request.form.get(...)`, `$_POST['x']`
>    - HTTP headers: `request.headers.get(...)`, `req.headers['x']`, `$_SERVER['HTTP_X_CUSTOM']`
>    - Cookies: `request.COOKIES.get(...)`, `req.cookies.x`, `$_COOKIE['x']`
>    - File upload filenames or content: `request.files['x'].filename`
>
> 2. **Attacker-controlled DOM sources** (client-side / DOM-based XSS):
>    - `location.search`, `location.hash`, `location.href`, `document.referrer`, `document.URL`
>    - `window.name`, `document.cookie`
>    - `postMessage` event: `window.addEventListener('message', (e) => { ... e.data ... })`
>    - `URLSearchParams` values derived from `location.search`
>    - `localStorage` / `sessionStorage` values written from URL or postMessage
>
> 3. **Stored (second-order) input** — the variable is read from persistent storage (database, file, cache), but the stored value originally came from user input:
>    - Find the write path: where was this field stored? Was it user-supplied at write time?
>    - Was any escaping or sanitization applied at write time? (Note: HTML-escaping at write time is fragile — it may be double-encoded or stripped elsewhere)
>    - Stored XSS is still a vulnerability even if it was validated or stored safely; track whether the read-back path escapes before rendering
>
> 4. **Third-party / integrated API data** (API10:2023 Unsafe Consumption of APIs):
>    - Data returned from external APIs, webhooks, or upstream services that is forwarded to DOM/template sinks
>    - Treat this as user-controlled unless the API contract proves otherwise
>
> 5. **Server-side / hardcoded value** — the variable comes from config, environment, a hardcoded constant, or server-side logic with no user influence — this site is NOT exploitable.
>
> **For each sink site, also check for mitigations that would prevent exploitation**:
> - Is the output explicitly escaped with a safe function just before the sink? (`htmlspecialchars()`, `escapeHtml()`, `h()`, `fn:escapeXml()`)
> - Is a sanitization library applied with a strict allowlist config? (`DOMPurify.sanitize(input)` — check if the config strips scripts)
> - Is the HTTP response `Content-Type` set to `application/json` or `text/plain` (no HTML rendering)?
> - Is a Content Security Policy header present that blocks inline scripts? (CSP reduces impact but is not a full fix)
> - Is there a WAF or input validation that strictly allowlists the expected format (e.g., a numeric ID)?
> - Does the output context require a different encoding than the one applied? (e.g., HTML-escaping applied to a JS string literal is insufficient)
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Vulnerable**: User input demonstrably reaches the sink with no effective escaping or sanitization.
> - **Likely Vulnerable**: User input probably reaches the sink (indirect/stored flow) or only weak mitigation is present (CSP-only, WAF-only, partial sanitization, incomplete allowlist).
> - **Not Vulnerable**: The variable is server-side only with no user influence, OR proper context-aware escaping is applied immediately before the sink.
> - **Needs Manual Review**: Cannot determine the variable's origin with confidence (opaque helpers, complex conditional flows, external libraries, or cross-service data flows).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/04_batch_[N].md`:
>
> ```markdown
> # XSS Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function / component**: [route, function, or component name]
> - **XSS type**: [Reflected / Stored / DOM-based / API-specific]
> - **Output context**: [HTML body / HTML attribute / JS string / URL / CSS / JSON / Markdown]
> - **Issue**: [e.g., "HTTP query param `q` flows directly into innerHTML without escaping"]
> - **Taint trace**: [Step-by-step from source to sink — e.g., "req.query.q → query → `<h1>${query}</h1>` → res.send()"]
> - **CWE mapping**: [e.g., CWE-79, CWE-80, CWE-116, CWE-692]
> - **Impact**: [What an attacker can do — session hijacking, credential theft, keylogging, defacement, redirects to malicious sites, etc.]
> - **Remediation**: [Specific fix — escape with the correct function for the context, switch to textContent, use auto-escaping template syntax, apply DOMPurify, validate URL scheme, set correct Content-Type]
> - **Dynamic Test**:
>   ```
>   [curl command or browser payload to confirm the finding.
>    Show the exact parameter, payload, and what to observe.
>    Example: curl "https://app.example.com/search?q=<script>alert(1)</script>"
>    Or: Visit https://app.example.com/#<img src=x onerror=alert(1)> and observe alert box]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function / component**: [route, function, or component name]
> - **XSS type**: [Reflected / Stored / DOM-based / API-specific]
> - **Output context**: [HTML body / HTML attribute / JS string / URL / CSS / JSON / Markdown]
> - **Issue**: [e.g., "Stored user bio likely rendered via innerHTML; write path confirmed from user input"]
> - **Taint trace**: [Best-effort trace, with uncertain steps identified]
> - **Concern**: [Why it's still a risk — e.g., "Sanitization library present but configured to allow script-capable tags"]
> - **CWE mapping**: [e.g., CWE-79, CWE-692]
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [payload to attempt]
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function / component**: [route, function, or component name]
> - **Reason**: [e.g., "Output wrapped in htmlspecialchars() before echo" or "Variable is a hardcoded server constant"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function / component**: [route, function, or component name]
> - **Uncertainty**: [Why the variable's origin or escaping status could not be determined]
> - **Suggestion**: [What to trace manually — e.g., "Follow `buildProfileHtml()` in utils.js to check where its return value originates"]
> ```

### Phase 3: Merge — Consolidate Batch Results
[ref: #xss-phase3-merge]

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/04_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/04_xss.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/04_batch_1.md`, `{{ REPORTS_ROOT }}/04_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary (total sink sites analyzed equals the number from recon; counts per classification sum across batches).
4. Write the merged report to `{{ REPORTS_ROOT }}/04_xss.md` using this format:

```markdown
# XSS Analysis Results: [Project Name]

## Executive Summary
- Sink sites analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/04_xss.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/04_batch_*.md`).

***

## OWASP API Security Top 10 2023 mapping
[ref: #xss-owasp-mapping]

This scan supports the following OWASP API Security Top 10 2023 risks:

- **API8:2023 Security Misconfiguration** — User input is rendered into HTML, JavaScript, or DOM sinks without output encoding, auto-escaping, an effective Content Security Policy, or secure error handling. Debug/spec interfaces (Swagger UI, GraphQL Playground) enabled in production also fall under this risk.
- **API10:2023 Unsafe Consumption of APIs** — Data from third-party or user-controlled sources is written to DOM or template sinks without sanitization.

Cross-mapping guidance:

| Root cause | OWASP risk | When to cross-map |
| --- | --- | --- |
| API returns unsanitized user input that a browser client renders | API8:2023 Security Misconfiguration | Missing output encoding, missing CSP, permissive CORS, debug error pages. |
| API returns unsanitized data from a third-party API | API10:2023 Unsafe Consumption of APIs | Third-party content forwarded to clients without sanitization. |
| Swagger UI / GraphQL Playground reflects user input | API8:2023 Security Misconfiguration | Debug/spec interfaces enabled in production. |

***

## Content Security Policy Best Practices for APIs
[ref: #xss-csp-best-practices]

Even APIs that are not directly rendered as HTML should ship defensive headers for browser clients and documentation interfaces:

- Use `Content-Type: application/json` for JSON responses so browsers do not sniff HTML.
- For pure API responses that might be opened in a browser, set `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'`.
- For Swagger UI / GraphQL Playground / API docs, enforce a restrictive `script-src` and `style-src`; avoid `unsafe-inline` and `unsafe-eval` — prefer nonces or hashes (`'nonce-…'`, `'sha256-…'`) with `'strict-dynamic'` over host allowlists.
- Add `require-trusted-types-for 'script'` where DOM clients render API-driven content (Trusted Types is Baseline since 2026).
- Use `X-Content-Type-Options: nosniff` to prevent MIME-type sniffing.
- Use `frame-ancestors 'none'` (or equivalent X-Frame-Options) to prevent clickjacking of API docs and playgrounds.

CSP is a defense-in-depth measure, not a substitute for proper encoding or sanitization.

***

## References
[ref: #xss-references]

- OWASP XSS Prevention Cheat Sheet — output-encoding rules per context.
- OWASP DOM based XSS Prevention Cheat Sheet — safe sink/source guidance.
- PortSwigger Web Security Academy — XSS labs and context taxonomy.
- MDN — Trusted Types API, HTML Sanitizer API (`Element.setHTML()`), CSP `script-src` directives.
- CWE-79: Improper Neutralization of Input During Web Page Generation.

## Important Reminders
[ref: #xss-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 sink sites per subagent**. If there are 1-3 sinks total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned sinks' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **Phase 1 is purely structural**: flag any dynamic variable passed to an HTML/JS/DOM sink, regardless of origin. Do not attempt to trace user input in Phase 1 — that is Phase 2's job.
- **Phase 2 is purely taint analysis**: for each sink found in Phase 1, trace the variable back to its origin. If it comes from a user-controlled source with no effective escaping, the site is a real vulnerability.
- Context matters: the same variable may be safe in one output context (HTML body with escaping) and dangerous in another (JavaScript string literal, URL attribute, or event handler attribute). Check the exact rendering context.
- Custom sanitization (homegrown regex stripping, blacklisting `<script>`, etc.) is **not** sufficient — flag as Likely Vulnerable. Only DOMPurify with a strict config or equivalent allowlist library is acceptable.
- Stored XSS is easy to miss: trace the write path to confirm the field is user-supplied, then separately verify the read/render path lacks escaping. Both legs must be true for the vulnerability to be exploitable.
- DOM-based XSS lives entirely in client-side JavaScript: look for `location.*`, `document.referrer`, `event.data`, and other attacker-controlled properties flowing into DOM sinks without passing through the server.
- API-specific XSS requires tracing data across the HTTP boundary: API response field → frontend code that renders it. The sink may be in a different repository or language than the source.
- CSP headers reduce XSS exploitability but are **not** a fix — still flag the underlying injection point.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Angular's `DomSanitizer.bypassSecurityTrust*` methods are always suspicious — flag them whenever the argument is not a hardcoded constant.
- For JavaScript execution sinks (`eval`, `setTimeout` with string arg), even seemingly innocuous data (error messages, IDs) can be dangerous if an attacker can influence them.
- Subagents must not modify project source code. They scan, trace, and report only.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/04_recon.md` and all `{{ REPORTS_ROOT }}/04_batch_*.md` files after the final `{{ REPORTS_ROOT }}/04_xss.md` is written.
