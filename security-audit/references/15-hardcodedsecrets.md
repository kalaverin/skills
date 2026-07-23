---
subject: "Hardcoded secrets in public code detection reference for SAST subagents: public-accessibility definition, frontend/backend scope rules incl. per-framework split, regex token catalog, variable-name patterns, false-positive filters, entropy heuristic, three-phase execution, PoC commands, prevention, OWASP/CWE mapping."
index:
  - anchor: hardcodedsecrets-detection
    what: "Focused public-secret detection role using the three-phase subagent approach — candidate recon, batched two-question verify, merge — gated on the architecture report."
    problem: "Deployed applications ship credential literals across bundles, binaries, and artifacts, and unstructured hunting drowns reviewers in backend-only matches that no external attacker can reach; detection orchestration, phase pipeline, exposure-first triage, audit rigor, candidate flood, coverage goal, methodical sweep."
    use_when: "Public-secret scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-phase detection must run."
    avoid_when: "Architecture summary absent — run the analysis module first; only conceptual knowledge is needed, not execution."
    expected: "Verified public-secret findings consolidated into the module report with false positives filtered."
  - anchor: hardcodedsecrets-definition
    what: "Core definition plus the decisive test: sensitive credentials embedded as string literals, reportable only when an external attacker can extract them from the deployed application without server access — with the LLM provider key trend called out."
    problem: "Reviewers flag every API-key string regardless of reachability, so backend-only noise buries browser- and binary-extractable secrets that actually get exploited within hours; concept baseline, shared vocabulary, reachability test, classification consistency, exploit window, term alignment."
    use_when: "Onboarding to the scan; deciding whether a found string belongs to this vulnerability class at all."
    avoid_when: "Concrete token formats are needed — jump to the pattern anchors; execution workflow is the question."
    expected: "Everyone applies one test: external extractability decides reportability."
  - anchor: hardcodedsecrets-scope-in
    what: "Positive scope: code paths attackers reach after deployment — browser JavaScript/TypeScript and framework client components, mobile source, served HTML/templates, client config directories, Electron, WebAssembly glue, published source maps and doc sites."
    problem: "Detectors under-report when exposure paths stay implicit, missing client bundles, decompilable mobile code, and shipped artifacts that deliver secrets straight to anyone who looks; missed surfaces, hidden bundles, recon breadth, delivery channels, unpackable clients, inclusion rules, decompile reach."
    use_when: "Running recon or verify on candidate locations; judging whether a file path ships to outsiders."
    avoid_when: "Backend-only exclusions are the question — see the scope-out anchor; framework-by-framework split wanted."
    expected: "Every attacker-reachable code path lands on the candidate list."
  - anchor: hardcodedsecrets-scope-out
    what: "Negative scope: locations explicitly not reported — server-side handlers and API routes, environment files, server configuration, CI/CD definitions, Docker and infrastructure files, backend utilities, tests, migrations."
    problem: "Verify batches drown in false positives when exclusion rules stay unwritten, burning confirmation effort on server-side literals no external party can observe; boundary rules, misrouted findings, wasted tracing, scope discipline, reachability confusion, triage accuracy, batch noise."
    use_when: "A candidate sits in ambiguous territory; classifying borderline locations before spending trace effort."
    avoid_when: "Publicly reachable surfaces are the question — see the scope-in anchor; token format catalog wanted."
    expected: "Backend-only candidates drop out early instead of inflating findings."
  - anchor: hardcodedsecrets-frontend-backend
    what: "Per-framework split rules: Next.js client vs `app/api` and `pages/api`, Nuxt `server/`, CRA/Vite `src/` bundling, Angular, Vue, Express static directories, Django/Flask templates vs `static/`, Rails assets, mobile always-public — plus `NEXT_PUBLIC_*` / `REACT_APP_*` / `VITE_*` build-time embedding."
    problem: "Modern meta-frameworks blur server and client rendering, so identical-looking files land on opposite exposure sides and misclassification follows; framework routing, SSR blur, bundle boundaries, classification accuracy, build embedding, directory conventions, edge cases."
    use_when: "Verify must decide client vs server for a concrete file; import-chain tracing hits a shared module."
    avoid_when: "Generic inclusion or exclusion lists suffice — see scope anchors; execution phases are the question."
    expected: "Each ambiguous file resolves to client or server with a framework-correct rule."
  - anchor: hardcodedsecrets-secret-types
    what: "Map of what counts as findable material: distinctive-format tokens, suspicious variable names, entropy-flagged literals, git-history survivors, and artifact-carried secrets."
    problem: "Hunters fixate on famous key prefixes and overlook name-driven, entropy-driven, history-driven, and artifact-driven candidates that lack any recognizable format; detection breadth, format bias, blind categories, coverage map, search strategy, prefix fixation, recall goal."
    use_when: "Planning recon coverage; checking that every material kind gets searched, not just regex-famous ones."
    avoid_when: "Concrete patterns are needed — jump to the regex, variable, or entropy anchors."
    expected: "Recon spans all five candidate kinds before verify starts."
  - anchor: hardcodedsecrets-regex-patterns
    what: "High-confidence token catalog: AWS `AKIA`/`ASIA`, Google `AIza`/`GOCSPX-`, GitHub `ghp_`/`github_pat_`/`gho_`/`ghs_`/`ghu_`/`ghr_`, GitLab, Slack `xox*` families, Stripe `sk_live_`/`rk_live_`, Twilio, SendGrid, OpenAI `sk-`/`sk-proj-`/`sk-svcacct-`, Anthropic `sk-ant-`, other LLM providers, registry and PaaS tokens, private key headers, connection strings."
    problem: "Free-text searching without exact prefix formats wastes effort on generic strings while distinctive tokens hide in plain sight across configs, bundles, and comments; prefix catalog, match anchors, lookup table, match confidence, token shapes, signature strings, scan precision."
    use_when: "Recon needs grep-ready formats; confirming whether a found string matches a known provider signature."
    avoid_when: "Name-driven or entropy-driven detection is the question — see sibling anchors; false-positive filtering wanted."
    expected: "Every known provider token gets matched by exact pattern during recon."
  - anchor: hardcodedsecrets-variable-patterns
    what: "Secret-related variable and constant name list — api/key/secret/token/password/private/signing/encryption/bearer/credentials/connection/salt/iv/nonce/webhook/client/tenant families across camelCase, snake_case, SCREAMING_SNAKE_CASE — where the assigned value needs inspection."
    problem: "Credentials hide behind naming conventions rather than recognizable formats, so prefix-only scans miss assignments whose names confess their purpose across four casing styles; name signals, casing variants, assignment contexts, assignment review, purpose leaks, scan breadth, config keys."
    use_when: "Building name-based search patterns for recon; deciding whether an assignment deserves a closer look."
    avoid_when: "Format-driven matching is the question — see the regex anchor; entropy scoring wanted."
    expected: "Every secret-named assignment gets its value checked against real-credential signals."
  - anchor: hardcodedsecrets-false-positives
    what: "Exclusion list of values that are not real secrets: placeholders, empty strings, environment references, public and publishable keys, test and sandbox keys, type definitions, documentation strings, hashes, build constants."
    problem: "Reports inflate with non-findings when reviewers cannot tell placeholder, publishable, and test material from live credentials, eroding trust in every verified result; exclusion filters, noise reduction, placeholder shapes, publishable designs, trust erosion, result quality, reviewer judgment."
    use_when: "A candidate value looks suspicious but might be designed-public or fake; downgrading before verify escalates."
    avoid_when: "Real-token formats are the question — see the regex anchor; public-vs-backend routing wanted."
    expected: "Designed-public and fake values exit the pipeline before findings are written."
  - anchor: hardcodedsecrets-entropy-heuristic
    what: "Generic-secret heuristic: length ≥ 16, mixed charset, Shannon entropy ≥ 4.5 bits per character, combined with secret-related variable names, with UUIDs, hashes, and structured placeholders skipped — plus the Python entropy one-liner."
    problem: "Custom credentials without any known prefix slip past format catalogs, forcing reviewers to judge random-looking strings by gut instead of measurable randomness; entropy scoring, generic secrets, custom tokens, gut calls, statistical signal, threshold tuning, shannon cutoff."
    use_when: "A literal has no recognizable format; scoring whether it looks like generated key material."
    avoid_when: "Known provider formats match — use the regex anchor; name-driven detection suffices."
    expected: "Format-less candidates get an objective randomness verdict."
  - anchor: hardcodedsecrets-subagent-constraints
    what: "Read-only audit constraints: no source, config, `.env`, CI/CD, or infrastructure modification; no pull requests, commits, or destructive commands; writes only under `{{ REPORTS_ROOT }}/`."
    problem: "Assessment work mutating audited code destroys evidence, breaks trust, and can detonate production systems mid-scan; read-only discipline, evidence integrity, mutation bans, audit safety, scope limits, destructive risk, trust preservation, blast radius."
    use_when: "Any subagent dispatch for this scan; reviewing whether an action stays inside audit bounds."
    avoid_when: "Detection content is the question — see pattern and execution anchors."
    expected: "All audit agents operate read-only with writes confined to the reports root."
  - anchor: hardcodedsecrets-execution
    what: "Three-phase execution: codebase-wide candidate recon with a zero-candidate early-exit gate, batched two-question verify (real secret? publicly reachable?) in groups of three, orchestrator merge into the final module report."
    problem: "Detection work without orchestration duplicates effort, loses batch boundaries, skips early exits, and merges verdicts inconsistently; execution model, phase overview, batch discipline, workflow entry, staging, dispatch plan, consolidation, handoff clarity, gate logic."
    use_when: "Starting the public-secret scan execution; dispatching or reviewing any phase or gate."
    avoid_when: "Conceptual knowledge is the need — see definition and scope anchors."
    expected: "All phases run with shared architecture context into one consolidated report."
  - anchor: hardcodedsecrets-dynamic-tests
    what: "Read-only confirmation commands per surface: grep built web bundles for prefixes, `apktool`/`unzip` mobile binaries, `docker save` layer extraction, forged-JWT signing with a discovered HMAC secret, query-string key probes — always non-destructive."
    problem: "Findings without reproducible confirmation get disputed by developers, and unsafe verification attempts risk mutating live systems just to prove reachability; replay evidence, challenge defense, safe probing, bundle inspection, binary extraction, verdict demos."
    use_when: "A verified finding needs a reproducible extraction demo; choosing a non-destructive confirmation per surface."
    avoid_when: "Detection patterns are the question — see pattern anchors; remediation advice wanted."
    expected: "Each confirmed secret ships with a safe, replayable extraction proof."
  - anchor: hardcodedsecrets-prevention-guidance
    what: "Layered defense checklist: dedicated secret managers, runtime environment injection, pre-commit scanners (`detect-secrets`, `gitleaks`, `truffleHog`), continuous repo/CI/image/state scanning, immediate rotation, short-lived workload identity, origin-restricted client keys with backend proxies, random per-operation salts and IVs, private source maps."
    problem: "Remediation advice scattered across vendor docs leaves gaps that let one missed control keep leaked credentials exploitable; remediation checklist, control mapping, defense completeness, gap elimination, hardening steps, rotation discipline, systematic mitigation."
    use_when: "Writing remediation for confirmed findings; auditing whether deployed defenses are complete."
    avoid_when: "Detection mechanics are the question — see execution anchors; verification commands wanted."
    expected: "Every finding closes with a complete, layered control set."
  - anchor: hardcodedsecrets-owasp-mapping
    what: "OWASP API 2023 mapping: API2 broken authentication (forged tokens via leaked HMAC secrets), API8 misconfiguration (secrets in source, bundles, images), API10 unsafe consumption (exposed third-party integration keys)."
    problem: "Findings need correct 2023-era taxonomy for reporting, and mislabeling credential exposure misroutes everything downstream into wrong risk buckets; risk routing, classification accuracy, edition awareness, correct tagging, traceability, risk labels, label drift."
    use_when: "Tagging findings with OWASP 2023 risks; writing the report's risk section."
    avoid_when: "CWE-level tagging is the question — see the CWE anchor."
    expected: "Findings mapped to correct API risks with explicit exposure reasoning."
  - anchor: hardcodedsecrets-cwe-mapping
    what: "CWE list anchored on CWE-798 hard-coded credentials: hard-coded password CWE-259, hard-coded cryptographic key CWE-321, information exposure CWE-200, cleartext transmission CWE-319, insufficiently protected credentials CWE-522."
    problem: "Wrong weakness identifiers break downstream tooling and metrics, especially when credential, crypto-key, and exposure classes blur across one finding; weakness taxonomy, misclassification risk, tooling accuracy, identifier precision, reporting feeds, scanner alignment, cwe tagging."
    use_when: "Assigning CWE identifiers to secret-exposure findings."
    avoid_when: "OWASP risk framing is the question — see the OWASP anchor."
    expected: "Each finding carries the most specific applicable CWE."
  - anchor: hardcodedsecrets-references
    what: "External link list: OWASP API 2023 risk pages, authentication and key-management cheat sheets, web service security guidance, and the three core CWE entries."
    problem: "Agents and readers need authoritative follow-up sources beyond this file's distilled content when deeper verification or remediation detail is required; further reading, external canon, deep dives, vendor documentation, primary material, cited works, owasp pages."
    use_when: "Primary sources or extended material is needed."
    avoid_when: "Detection patterns or execution workflow are the question — this list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
  - anchor: hardcodedsecrets-important-reminders
    what: "Closing operational rules: read-only subagents, phase ordering, batch size of three, parallel dispatch, per-batch context slicing, public-accessibility primacy, import-chain tracing, mobile always public, Firebase/Stripe publishable exceptions, env-var nuance, git history, entropy, redaction, conservative classification, cleanup."
    problem: "Modules close with inconsistent final guidance, letting overbroad flags, leaked full secrets in reports, or premature deletion slip into audit runs and client deliverables; closing rules, quality floor, consistency, final reminders, weak evidence, uniform endings, wrap discipline, audit closure."
    use_when: "Finalizing the module report; reviewing operational rules before dispatch."
    avoid_when: "Detection or execution is the current stage — finish those first."
    expected: "Runs close with uniform operational rules applied."
---

# Hardcoded Secrets in Public Code Detection

[ref: #hardcodedsecrets-detection]

You are performing a focused security assessment to find hardcoded sensitive data that is exposed in publicly accessible code. This skill uses a three-phase approach with subagents: **recon** (find all potential secret candidates), **batched verify** (confirm each is a real secret in publicly reachable code, in parallel batches of 3), and **merge** (consolidate batch reports into one file).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

***

## What Are Hardcoded Secrets in Public Code
[ref: #hardcodedsecrets-definition]

Hardcoded secrets are sensitive credentials — API keys, access tokens, private keys, passwords, signing secrets, database connection strings — embedded directly in source code as string literals.

This skill focuses specifically on secrets that end up in **publicly accessible code**, meaning an attacker can extract them **without any server-side access**. A secret hardcoded in backend server code is bad practice but not directly exploitable by an external attacker inspecting the deployed application. A secret hardcoded in frontend JavaScript or a mobile app binary **is** directly extractable.

**2024–2026 trend — LLM provider keys**: OpenAI, Anthropic, Google AI, Cohere, Groq, and Replicate keys are now among the most frequently leaked secrets in client-side JavaScript, mobile binaries, and public repositories. Because LLM usage is billed per token, leaked keys are exploited within hours by attackers running massive inference workloads — treat AI provider keys in client-reachable code as the highest-priority candidates.

The core question: *Can an external attacker obtain this secret from the deployed application without server access?*

### What to Report (Publicly Accessible Code)
[ref: #hardcodedsecrets-scope-in]

These code paths are accessible to attackers after deployment:

- **Frontend JavaScript/TypeScript** — any `.js`, `.ts`, `.jsx`, `.tsx` file that runs in the browser. This includes:
  - React, Angular, Vue, Svelte components and pages
  - Next.js client components (files with `"use client"` or files under `app/` without `"use server"`)
  - Nuxt.js pages and client plugins
  - Vanilla JS in `public/`, `static/`, or `assets/` directories
  - Webpack/Vite/Rollup entry points and their imported modules
  - Any file imported by a client-side entry point (even if it lives in a `utils/` or `lib/` folder)
- **Mobile application code** — extractable via reverse engineering (decompiling APK, inspecting IPA):
  - Android: Java/Kotlin source files
  - iOS: Swift/Objective-C source files
  - React Native: JavaScript bundles
  - Flutter: Dart source files
  - Xamarin: C# source files
- **HTML files and templates served to clients** — inline `<script>` blocks, `data-` attributes, meta tags
- **Client-side configuration files** — files in `public/`, `static/`, `assets/`, `www/` directories
- **Electron/desktop app source** — extractable from ASAR archives
- **WebAssembly source/companion JS** — secrets in JS glue code or extractable from WASM
- **Published source maps and documentation sites** — `.js.map` files and Storybook/Docusaurus examples can reconstruct or expose original secrets

### What NOT to Report (Backend-Only Code)
[ref: #hardcodedsecrets-scope-out]

Do not flag secrets in these locations — they are not publicly accessible:

- **Server-side application code** — Express route handlers (server-only), Django views, Flask routes, Spring controllers, Rails controllers, Go HTTP handlers, PHP controllers — code that runs exclusively on the server
- **Server-side API route files** — Next.js `app/api/` routes, Nuxt server routes, SvelteKit `+server.ts` files
- **Environment files** — `.env`, `.env.local`, `.env.production` (unless served statically)
- **Server-side configuration** — `config/database.yml`, `settings.py`, `application.properties`, `appsettings.json`
- **CI/CD pipeline files** — `.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml`
- **Docker/infrastructure files** — `Dockerfile`, `docker-compose.yml`, Kubernetes manifests
- **Backend utility/service files** — files that are only imported by server-side code
- **Test files** — test fixtures and test configuration (unless the test files are shipped to the client)
- **Migration files** — database migrations

### Distinguishing Frontend from Backend
[ref: #hardcodedsecrets-frontend-backend]

This is critical and requires understanding the project architecture:

**Next.js**: Files under `app/` with `"use client"` directive or without `"use server"` are client components. Files under `app/api/` are server-only. Files under `pages/api/` are server-only. Files under `pages/` (non-api) render on both server and client — secrets here ARE exposed. `next.config.js` runs server-side only but `NEXT_PUBLIC_*` env vars are embedded in client bundles.

**Nuxt.js**: Files under `pages/`, `components/`, `composables/` are client-accessible. Files under `server/` are server-only.

**React (CRA/Vite)**: Everything in `src/` is bundled for the client. `REACT_APP_*` and `VITE_*` env vars are embedded in client builds.

**Angular**: Everything in `src/` is bundled for the client.

**Vue (Vite)**: Everything in `src/` is bundled for the client. `VITE_*` env vars are embedded.

**Express/Fastify/Koa**: All server-side unless serving static files from a `public/` or `static/` directory.

**Django/Flask**: Python code is server-side. Templates are rendered server-side (secrets in template context don't reach the client unless explicitly rendered into JS). Static files in `static/` are client-accessible.

**Rails**: Ruby code is server-side. Assets in `app/assets/javascripts/` or `app/javascript/` are client-accessible.

**Mobile apps**: ALL source code is considered publicly accessible via reverse engineering.

***

## Types of Secrets to Look For
[ref: #hardcodedsecrets-secret-types]

### High-Confidence Patterns (Regex-Identifiable)
[ref: #hardcodedsecrets-regex-patterns]

These have distinctive formats that make them identifiable with high confidence:

| Secret Type | Pattern |
|---|---|
| AWS Access Key ID | `AKIA[0-9A-Z]{16}` (long-term), `ASIA[0-9A-Z]{16}` (temporary session credentials — equally sensitive) |
| AWS Secret Access Key | 40-character base64 string near an `AKIA` key |
| Google API Key | `AIza[0-9A-Za-z\-_]{35}` |
| Google OAuth Client Secret | `GOCSPX-[0-9A-Za-z\-_]{28}` |
| GitHub Personal Access Token | `ghp_[0-9A-Za-z]{36}`, `github_pat_[0-9A-Za-z_]{82}` |
| GitHub OAuth / Server / User / Refresh Tokens | `gho_[0-9A-Za-z]{36}`, `ghs_[0-9A-Za-z]{36}` (server-to-server), `ghu_[0-9A-Za-z]{36}` (user-to-server), `ghr_[0-9A-Za-z]{36}` (refresh) |
| GitLab Personal Access Token | `glpat-[0-9A-Za-z\-_]{20}` |
| Slack Bot/User Token | `xoxb-[0-9A-Za-z\-]+`, `xoxp-[0-9A-Za-z\-]+`, `xoxc-[0-9A-Za-z\-]+` / `xoxd-[0-9A-Za-z\-]+` (client tokens + cookies), `xoxe` / `xoxe.xoxp-` (enterprise) |
| Slack Webhook URL | `hooks.slack.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+` |
| Stripe Secret Key | `sk_live_[0-9A-Za-z]{24,}`, `rk_live_[0-9A-Za-z]{24,}` (restricted keys — still secret) |
| Stripe Publishable Key | `pk_live_[0-9A-Za-z]{24,}` (publishable keys are designed for client-side — skip unless paired with a secret key) |
| Twilio Account SID + Auth Token | `AC[0-9a-f]{32}` (SID), 32-hex auth token nearby |
| SendGrid API Key | `SG\.[0-9A-Za-z\-_]{22}\.[0-9A-Za-z\-_]{43}` |
| Mailgun API Key | `key-[0-9a-zA-Z]{32}` |
| Firebase Config | `apiKey`, `authDomain`, `projectId` together in a config object — only flag if it includes a server/admin key, not the standard client config |
| Private RSA/EC/SSH Key | `-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----` |
| JWT Secret / Signing Key | String assigned to variables like `JWT_SECRET`, `jwt_secret`, `signingKey`, `HMAC_KEY` |
| Database Connection String with Password | `postgresql://user:pass@`, `mysql://user:pass@`, `mongodb://user:pass@`, `redis://:pass@` |
| Generic API Key Assignment | Variable named `*api_key*`, `*apiKey*`, `*API_KEY*`, `*secret*`, `*SECRET*`, `*token*`, `*TOKEN*`, `*password*`, `*PASSWORD*` assigned a string literal that looks like a real credential |
| Heroku API Key | `[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}` in a Heroku context |
| Azure Storage Key | Base64 string ~88 chars assigned to storage account key variables |
| OpenAI API Key | `sk-[A-Za-z0-9]{48}` (legacy user keys), `sk-proj-[A-Za-z0-9\-_]{100,}` (project keys), `sk-svcacct-[A-Za-z0-9\-_]+` (service accounts), `sk-None-[A-Za-z0-9\-_]+` (new-format user keys) |
| Anthropic API Key | `sk-ant-[A-Za-z0-9\-_]{90,}` |
| Other AI/LLM Provider Keys | Groq `gsk_[A-Za-z0-9]{52}`, Replicate `r8_[A-Za-z0-9]{37}`, Hugging Face `hf_[A-Za-z0-9]{30,}`, Cohere / Google AI Studio keys in client config — LLM keys are billed per token and exploited within hours of leaking |
| Hardcoded Salt / IV / Nonce | Variable named `salt`, `iv`, `nonce` assigned a fixed hex or base64 value; AES IVs are 16 bytes, GCM nonces 12 bytes |
| Token/Key in Comment or Log | `// TODO: token=...`, `console.log("secret:", ...)`, debug output containing high-entropy strings |
| GCP Service Account Key | JSON block with `"type": "service_account"`, `private_key`, `client_email` |
| Azure AD / Service Principal Secret | `client_id`, `tenant_id`, `client_secret` together; Azure Storage key ~88 chars |
| Package Registry Tokens | npm `npm_[A-Za-z0-9]{36}`, PyPI `pypi-AgEIcHlwaS5vcmc[A-Za-z0-9\-_]{50,}` |
| Cloud / PaaS Tokens | DigitalOcean `dop_v1_[0-9a-f]{64}`, Supabase `sbp_[0-9a-f]{40}`, Doppler `dp.pt.[A-Za-z0-9\-_]{40,}`, PlanetScale `pscale_tkn_[A-Za-z0-9\-_]{30,}` |
| Generic Webhook Signing Secret | `whsec_[...]`, `X-Hub-Signature-256` context, `sha256=...`, variables named `webhook_secret` |
| API Key in URL Query Parameter | URLs containing `?api_key=...`, `?token=...`, `?key=...`, `?secret=...` |

### Variable Name Patterns (Require Value Inspection)
[ref: #hardcodedsecrets-variable-patterns]

Search for variables/constants with these name patterns and check if the assigned value looks like a real credential:

- `api_key`, `apiKey`, `API_KEY`, `ApiKey`
- `secret`, `SECRET`, `secret_key`, `secretKey`, `SECRET_KEY`
- `access_token`, `accessToken`, `ACCESS_TOKEN`
- `auth_token`, `authToken`, `AUTH_TOKEN`
- `private_key`, `privateKey`, `PRIVATE_KEY`
- `password`, `PASSWORD`, `passwd`, `PASSWD`
- `client_secret`, `clientSecret`, `CLIENT_SECRET`
- `signing_key`, `signingKey`, `SIGNING_KEY`
- `encryption_key`, `encryptionKey`, `ENCRYPTION_KEY`
- `bearer_token`, `BEARER_TOKEN`
- `credentials`, `CREDENTIALS`
- `connection_string`, `connectionString`, `DATABASE_URL`
- `salt`, `SALT`, `iv`, `IV`, `nonce`, `NONCE`
- `webhook_secret`, `WEBHOOK_SECRET`, `signing_secret`, `SIGNING_SECRET`
- `client_id`, `CLIENT_ID`, `tenant_id`, `TENANT_ID`

### What is NOT a Real Secret (False Positives to Ignore)
[ref: #hardcodedsecrets-false-positives]

- **Placeholder values**: `"your-api-key-here"`, `"TODO"`, `"xxx"`, `"changeme"`, `"REPLACE_ME"`, `"INSERT_KEY"`, `"<api_key>"`, `"dummy"`, `"test"`, `"example"`, `"sample"`, `"placeholder"`
- **Empty strings**: `""`, `''`
- **Environment variable references**: `process.env.API_KEY`, `os.environ["SECRET"]`, `ENV["KEY"]` — these read from the environment at runtime, not hardcoded
- **Public keys**: Public keys (not private) are designed to be shared — not a secret
- **Publishable/public API keys**: Stripe `pk_test_*`, `pk_live_*`; Firebase client config `apiKey` (designed for client-side use); Google Maps client key (restricted by HTTP referrer)
- **Test/development keys**: `sk_test_*` (Stripe test), sandbox credentials, keys in test fixtures
- **Type definitions / interfaces**: TypeScript `interface Config { apiKey: string }` — no actual value
- **Documentation strings**: Comments explaining what a key looks like
- **Hash values**: SHA256/MD5 hashes that are not secrets (e.g., content hashes, checksums)
- **Build-time constants**: Version strings, build IDs, commit hashes

### Generic Secret Entropy Heuristic
[ref: #hardcodedsecrets-entropy-heuristic]

When no distinctive prefix exists, use this heuristic to flag high-entropy string literals that may be generic secrets:

- Minimum length: 16 characters.
- Character set: mixed alphanumeric + symbols.
- Shannon entropy ≥ 4.5 bits per character.
- Combine entropy with variable-name signals (`api_key`, `secret`, `token`, `password`, `private_key`, `webhook_secret`).
- Skip UUIDs used as database primary keys, content hashes, version strings, and obviously structured placeholders.

A Python one-liner to estimate Shannon entropy:

```python
import math, collections
s = "CANDIDATE_STRING"
entropy = -sum((c/len(s)) * math.log2(c/len(s)) for c in collections.Counter(s).values())
```

***

## Subagent Constraints (Read-Only Audit)
[ref: #hardcodedsecrets-subagent-constraints]

All subagents used in this skill are read-only security assessors. They MUST NOT:

- Modify project source code, configuration files, `.env` files, CI/CD pipelines, or infrastructure definitions.
- Open pull requests, commit changes, push branches, or rewrite/delete source files.
- Run destructive commands against the repository, production systems, or live APIs.
- Delete or overwrite files outside `{{ REPORTS_ROOT }}`.

Subagents may only write audit artifacts under `{{ REPORTS_ROOT }}/` (`15_recon.md`, `15_batch_N.md`, `15_hardcodedsecrets.md`).

## Execution
[ref: #hardcodedsecrets-execution]

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context. All subagents are read-only: they must not modify source code or open pull requests.

### Phase 1: Recon — Find Secret Candidates

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where a hardcoded secret (API key, access token, private key, password, signing secret, connection string) appears as a string literal. Write results to `{{ REPORTS_ROOT }}/15_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, project structure, and which files are frontend vs. backend.
>
> **Read-only constraint**: Do not modify source code, configuration files, CI/CD definitions, or open pull requests. Write only to `{{ REPORTS_ROOT }}/15_recon.md`.
>
> **What to search for**:
>
> Scan the entire codebase. At this stage, flag ALL potential secrets regardless of whether they are in frontend or backend code — the filtering happens in Phase 2.
>
> 1. **High-confidence regex patterns** — search for these distinctive formats:
>    - AWS keys: `AKIA[0-9A-Z]{16}` (long-term), `ASIA[0-9A-Z]{16}` (temporary session credentials)
>    - Google API keys: `AIza[0-9A-Za-z\-_]{35}`
>    - GitHub tokens: `ghp_`, `github_pat_`, `gho_`, `ghs_`, `ghu_`, `ghr_`
>    - Slack tokens: `xoxb-`, `xoxp-`, `xoxa-`, `xoxr-`, `xoxc-`, `xoxd-`, `xoxe`
>    - Stripe secret keys: `sk_live_`, `rk_live_`, `sk_test_`
>    - SendGrid keys: `SG\.`
>    - OpenAI keys: `sk-` followed by 48+ alphanumeric characters, `sk-proj-`, `sk-svcacct-`, `sk-None-`
>    - Anthropic keys: `sk-ant-`
>    - Other AI/LLM provider keys: `gsk_` (Groq), `r8_` (Replicate), `hf_` (Hugging Face)
>    - Package registry tokens: `npm_` (npm), `pypi-` (PyPI)
>    - Cloud/PaaS tokens: `dop_v1_` (DigitalOcean), `sbp_` (Supabase), `dp.pt.` (Doppler), `pscale_tkn_` (PlanetScale)
>    - Private key headers: `-----BEGIN.*PRIVATE KEY-----`
>    - Connection strings with embedded passwords: `://[^:]+:[^@]+@`
>    - GCP service account JSON: `"type": "service_account"`
>    - Azure AD / Service Principal: `client_secret`, `tenant_id`, `client_id`
>    - Webhook signing secrets: `whsec_`, `X-Hub-Signature-256`, `sha256=`
>    - API keys in URL query parameters: `?api_key=`, `?token=`, `?key=`
>
> 2. **Variable assignment patterns** — search for variables with secret-related names assigned string literal values:
>    - Search for patterns like: `apiKey = "..."`, `api_key = '...'`, `API_KEY: "..."`, `secret: "..."`, `token = "..."`, `password = "..."`, `client_secret = "..."`, `salt = "..."`, `iv = "..."`, `nonce = "..."`, `webhook_secret = "..."`
>    - Include all casing conventions: camelCase, snake_case, SCREAMING_SNAKE_CASE, PascalCase
>    - Look in JS/TS objects, JSON files, YAML/TOML config, Python dicts, environment-like configs
>
> 3. **Inline string literals** that match known key formats:
>    - Long random alphanumeric strings (32+ characters) assigned to auth-related variables
>    - Base64-encoded strings in authentication contexts
>    - Hex strings (64+ characters) used as keys or secrets
>    - UUIDs used as API keys or secrets
>
> 4. **Entropy-based generic secret detection** — when no distinctive prefix is present, flag string literals that meet ALL of the following:
>    - Length ≥ 16 characters
>    - Mixed alphanumeric + symbols
>    - Shannon entropy ≥ 4.5 bits per character
>    - Assigned to a variable with a secret-related name (`api_key`, `secret`, `token`, `password`, `private_key`, `webhook_secret`)
>
> 5. **Git history scanning** — secrets removed from current `HEAD` often remain in `.git/`:
>    - Run `git log -p -S'<high-entropy string or prefix>'` for each candidate prefix.
>    - Run `git log --all --full-history -p -- <path>` for suspicious files.
>    - Look for deleted `.env`, `config.json`, or credential files in commit history.
>    - If `truffleHog` or `gitleaks` is available, run them against the repository and include confirmed hits.
>
> 6. **Modern exfiltration vectors** — inspect artifacts that may ship secrets even when current source files look clean. Only report these if they are publicly reachable:
>    - **Docker images**: built image layers, `docker history`, exported tarballs.
>    - **Kubernetes manifests**: `Secret`, `ConfigMap`, Helm values files.
>    - **Terraform state**: `.tfstate`, `.tfplan`, and state backups.
>    - **CI/CD logs and artifacts**: workflow outputs, caches, uploaded bundles.
>    - **Browser storage**: code that writes API keys/tokens to `localStorage`/`sessionStorage`.
>    - **Source maps / minified bundles**: `.js.map` files that reconstruct original source.
>    - **Storybook / documentation sites**: published docs that include live examples with real keys.
>
> **What to skip during recon**:
> - Environment variable reads: `process.env.*`, `os.environ[*]`, `ENV[*]`, `System.getenv(*)` — these are not hardcoded
> - Type definitions with no values: `apiKey: string`, `type Config = { secret: string }`
> - Obvious placeholders: `"your-key-here"`, `"TODO"`, `"xxx"`, `"changeme"`, `"REPLACE_ME"`, `"<api_key>"`, `"dummy"`, `"test-key"`, `"example"`, `"sample"`, empty strings
> - Comments that merely describe or document secrets
> - Public keys (non-private cryptographic keys)
> - Hash values used as checksums or content identifiers
> - Files in `.git/`, `node_modules/`, `vendor/`, `venv/`, `__pycache__/`, `dist/`, `build/` directories
>
> **Output format** — write to `{{ REPORTS_ROOT }}/15_recon.md`:
>
> ```markdown
> # Hardcoded Secrets Recon: [Project Name]
>
> ## Summary
> Found [N] potential hardcoded secret candidates.
>
> ## Candidates
>
> ### 1. [Descriptive name — e.g., "AWS Access Key in API config"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Secret type**: [AWS key / Google API key / Generic API key / Private key / Password / JWT secret / Connection string / etc.]
> - **Variable/context**: [variable name or context where the secret appears]
> - **Detection method**: [regex match / variable name pattern / inline literal / entropy / git history / artifact]
> - **Code snippet**:
>   ```
>   [Show the line(s) containing the secret — REDACT the middle portion of the actual value, e.g., "AKIA****EXAMPLE" or "sk_live_****abcd"]
>   ```
>
> [Repeat for each candidate]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/15_recon.md`. If the recon found **zero candidates** (the summary reports "Found 0" or the "Candidates" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/15_hardcodedsecrets.md` and stop:

```markdown
# Hardcoded Secrets Analysis Results

No vulnerabilities found.
```

Only proceed to Phase 2 if Phase 1 found at least one candidate.

### Phase 2: Verify — Confirm Real Secrets in Public Code (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/15_recon.md` and split the candidates into **batches of up to 3 candidates each**. Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned candidates and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/15_recon.md` and count the numbered candidate sections (### 1., ### 2., etc.).
2. Divide them into batches of up to 3. For example, 8 candidates -> 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those candidate sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned candidates.
5. Each subagent writes to `{{ REPORTS_ROOT }}/15_batch_N.md` where N is the 1-based batch number.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: Verify the following hardcoded secret candidates. For each one, determine (1) whether it is a real secret and (2) whether it is in publicly accessible code. Write results to `{{ REPORTS_ROOT }}/15_batch_[N].md`.
>
> **Your assigned candidates** (from the recon phase):
>
> [Paste the full text of the assigned candidate sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, frontend/backend separation, build pipeline, and which directories contain client-side vs. server-side code.
>
> **Read-only constraint**: Do not modify source code, configuration files, CI/CD definitions, or open pull requests. Write only to `{{ REPORTS_ROOT }}/15_batch_[N].md`.
>
> **For each candidate, answer TWO questions:**
>
> **Question 1: Is this a real secret?**
>
> Check whether the value is an actual credential vs. a false positive:
> - Does the string have the entropy and format of a real key/token? (Real API keys are typically 20+ random characters)
> - Is it a known placeholder or example value? ("your-key-here", "changeme", "test", "example", "TODO", "xxx", "REPLACE_ME", etc.)
> - Is it a test/development key? (Stripe `sk_test_*`, sandbox credentials, keys in test fixtures)
> - Is it a public/publishable key by design? (Stripe `pk_live_*`, Firebase client `apiKey`, Google Maps browser key)
> - Is it actually an environment variable reference that got picked up by mistake?
> - Is it a hash, checksum, or non-secret identifier?
> - For salts/IVs/nonces: is the value fixed across operations instead of randomly generated per use?
>
> If the value is NOT a real secret, classify as **Not Vulnerable** and explain why.
>
> **Question 2: Is this in publicly accessible code?**
>
> Determine whether an external attacker can extract this secret from the deployed application:
>
> **PUBLICLY ACCESSIBLE (report these):**
> - Frontend JavaScript/TypeScript that runs in the browser (React, Angular, Vue, Svelte components/pages)
> - Next.js client components (files with `"use client"` or client-rendered pages)
> - Nuxt.js `pages/`, `components/`, client-side `plugins/`
> - Any `.js`/`.ts` file that is imported by a client-side entry point (trace the import chain)
> - Files in `public/`, `static/`, `assets/`, `www/` directories that are served directly
> - HTML files with inline `<script>` blocks
> - Mobile app source code — Android (Java/Kotlin), iOS (Swift/Objective-C), React Native JS, Flutter Dart, Xamarin C# — ALL mobile code is extractable via reverse engineering
> - Electron app source (extractable from ASAR)
> - Client-side configuration objects embedded in JavaScript (e.g., Firebase config, analytics init)
> - Public Docker images, public source maps, published Storybook/documentation sites, public CI logs/artifacts
>
> **NOT PUBLICLY ACCESSIBLE (do not report):**
> - Server-side route handlers (Express, Django, Flask, Rails, Spring, Go, PHP controllers)
> - Server-side API routes (Next.js `app/api/`, Nuxt `server/`, SvelteKit `+server.ts`)
> - Backend services, middleware, utilities only imported by server code
> - `.env` files, server config files, Docker/CI files — unless the artifact is publicly published
> - Test files and fixtures not shipped to clients
> - Database migrations
> - Build scripts and tooling
>
> **How to determine if a file is client-side:**
> 1. Check the file path — is it under a client-side directory? (`src/` in CRA/Vite React, `pages/` in Next.js, `app/` in Angular, `src/` in Vue)
> 2. Trace the import chain — is this file imported (directly or transitively) by a client-side entry point?
> 3. Check for server-only markers — `"use server"` directive, file under `api/` or `server/` directories
> 4. Check `{{ REPORTS_ROOT }}/01_architecture.md` for the project's frontend/backend separation pattern
> 5. For ambiguous cases (e.g., shared utility files), err on the side of caution — if it COULD be bundled for the client, treat it as publicly accessible
>
> If the secret is NOT in publicly accessible code, classify as **Not Vulnerable** and explain why (e.g., "Server-side only — Express route handler").
>
> **Classification**:
> - **Vulnerable**: Confirmed real secret in confirmed publicly accessible code. An attacker can extract this from the deployed application.
> - **Likely Vulnerable**: Appears to be a real secret and the file is likely client-accessible, but cannot fully confirm one or both conditions (e.g., ambiguous import chain, uncertain if the value is a real production key).
> - **Not Vulnerable**: Either not a real secret (placeholder, test key, public key) OR not in publicly accessible code (backend-only).
> - **Needs Manual Review**: Cannot determine if the value is a real secret or if the file reaches the client — requires human judgment.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/15_batch_[N].md`:
>
> ```markdown
> # Hardcoded Secrets Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Secret type**: [AWS key / Google API key / etc.]
> - **Exposure path**: [How an attacker extracts it — e.g., "Bundled into client JS via Webpack, visible in browser DevTools Sources tab" or "Embedded in Android APK, extractable via `apktool d app.apk`"]
> - **Issue**: [Clear description — e.g., "AWS access key hardcoded in React component that is bundled for the browser"]
> - **Impact**: [What an attacker can do with this secret — e.g., "Full access to AWS S3 buckets, potential data exfiltration", "Send emails via SendGrid on behalf of the organization", "Access user data via the API"]
> - **Evidence**:
>   ```
>   [Code snippet with the secret value partially redacted]
>   ```
> - **Remediation**: [Move the secret to a server-side environment variable. If the client needs to call this API, proxy through your backend. For mobile apps, use a backend proxy or OAuth flow instead of embedding keys.]
> - **Verification Steps**:
>   ```
>   [How to confirm this finding:
>    - For web apps: "Open browser DevTools > Sources > search for 'AKIA' in bundled JS files"
>    - For mobile apps: "Run `apktool d app.apk` and grep for the key pattern"
>    - For Electron: "Extract ASAR archive and search for the key"
>    - For Docker: "Run `docker history --no-trunc` or export layers and grep"]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Secret type**: [type]
> - **Exposure path**: [Best guess at how it reaches the client]
> - **Issue**: [What's uncertain]
> - **Concern**: [Why it's still a risk]
> - **Evidence**:
>   ```
>   [Code snippet]
>   ```
> - **Remediation**: [Fix recommendation]
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Reason**: [e.g., "Placeholder value — 'your-api-key-here'" or "Server-side only — Django view, never reaches the client" or "Stripe publishable key — designed for client use"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Uncertainty**: [Why automated analysis couldn't determine the status]
> - **Suggestion**: [What to check manually]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/15_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/15_hardcodedsecrets.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/15_batch_1.md`, `{{ REPORTS_ROOT }}/15_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/15_hardcodedsecrets.md` using this format:

```markdown
# Hardcoded Secrets Analysis Results: [Project Name]

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
```

5. After writing `{{ REPORTS_ROOT }}/15_hardcodedsecrets.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/15_batch_*.md`).

***

## Dynamic-Test / Proof-of-Concept Commands
[ref: #hardcodedsecrets-dynamic-tests]

Use these reproducible checks to confirm that a discovered secret is reachable and valid. Only run non-destructive, read-only probes; never mutate production data or abuse live services.

### Web bundles

```bash
# Search built artifacts for known secret prefixes
grep -R -E "sk_live_|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|AIza[0-9A-Za-z\-_]{35}|xoxb-[A-Za-z0-9\-]+|sk-ant-[A-Za-z0-9\-_]+|whsec_[A-Za-z0-9]+" dist/ build/ .next/static/ public/static/

# Inspect the running application bundle
curl -s https://app.example.com/static/js/main.*.js | grep -oE "sk_live_[A-Za-z0-9]+"
```

### Mobile binaries

```bash
# Android APK
apktool d app.apk -o app_unpacked
rg -oE "sk_live_[A-Za-z0-9_\-]+|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z\-_]{35}|ghp_[A-Za-z0-9]{36}" app_unpacked/

# iOS IPA
unzip -q app.ipa -d app_payload
rg -oE "sk_live_[A-Za-z0-9_\-]+|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z\-_]{35}|ghp_[A-Za-z0-9]{36}" app_payload/Payload/

# React Native / Flutter bundled assets
rg -oE "AIza[0-9A-Za-z\-_]{35}|ghp_[A-Za-z0-9]{36}|xoxb-[A-Za-z0-9\-]+" app_unpacked/assets/
```

### Docker images

```bash
docker pull target/image:tag
docker save target/image:tag -o image.tar
mkdir image_layers && tar -xf image.tar -C image_layers
rg -oE "sk_live_[A-Za-z0-9_\-]+|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z\-_]{35}" image_layers/

# Inspect build-time environment variables baked into layers
docker history --no-trunc target/image:tag
```

### JWT secrets

```bash
# Sign a forged token with a discovered HMAC secret
python3 - "$HMAC_SECRET" <<'PY'
import sys, jwt, time
secret = sys.argv[1]
token = jwt.encode(
    {"sub": "attacker", "iat": time.time(), "exp": time.time() + 3600},
    secret,
    algorithm="HS256"
)
print(token)
PY

# Attempt to access a protected endpoint with the forged token
curl -s -H "Authorization: Bearer $TOKEN" https://api.example.com/protected
```

### API keys in URL query parameters

```bash
# Check whether a query-string key is accepted
curl -s "https://api.example.com/v1/users?api_key=$DISCOVERED_KEY" -o /dev/null -w "%{http_code}\n"

# Search access logs, proxy history, or browser Network tab for URLs containing keys
grep -RE "\?api_key=|\?token=|\?key=|\?secret=" logs/ har_files/
```

***

## Prevention Guidance
[ref: #hardcodedsecrets-prevention-guidance]

- Store secrets in a dedicated secret manager: AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, HashiCorp Vault, Doppler, or 1Password Secrets Automation.
- Inject secrets via environment variables at runtime; never commit them to source control.
- Use pre-commit hooks (`detect-secrets`, `gitleaks`, `truffleHog`) to block commits containing secrets.
- Scan repositories, CI logs, container images, and Terraform state continuously.
- Rotate compromised keys immediately and audit key usage logs.
- Use short-lived credentials and workload identity where possible (OIDC, IAM roles, managed identities).
- Restrict client-side keys by origin/IP and scope; proxy sensitive integrations through backend APIs.
- Never hardcode salts, IVs, or nonces; generate them randomly per cryptographic operation.
- Keep source maps and debug symbols private; do not publish them alongside production bundles.

***

## OWASP API Security Top 10 2023 Mapping
[ref: #hardcodedsecrets-owasp-mapping]

This scan supports the following OWASP API Security Top 10 2023 risks:

| OWASP Risk | Why Hardcoded Secrets Matter |
|---|---|
| **API2:2023 Broken Authentication** | Hardcoded JWT HMAC secrets, session signing keys, or API keys let attackers forge tokens or impersonate users. |
| **API8:2023 Security Misconfiguration** | Secrets committed to source control, embedded in client bundles, or shipped in Docker images are a configuration/hardening failure. |
| **API10:2023 Unsafe Consumption of APIs** | Third-party API keys/secrets in code are used to call integrated services; if exposed, attackers can abuse those integrations. |

***

## CWE References
[ref: #hardcodedsecrets-cwe-mapping]

- CWE-798: Use of Hard-coded Credentials
- CWE-259: Use of Hard-coded Password
- CWE-321: Use of Hard-coded Cryptographic Key
- CWE-200: Exposure of Sensitive Information to an Unauthorized Actor
- CWE-319: Cleartext Transmission of Sensitive Information
- CWE-522: Insufficiently Protected Credentials

CWE-798 is the parent weakness for most findings produced by this scan.

***

## References
[ref: #hardcodedsecrets-references]

- OWASP API Security Top 10 2023 — API2:2023 Broken Authentication
- OWASP API Security Top 10 2023 — API8:2023 Security Misconfiguration
- OWASP API Security Top 10 2023 — API10:2023 Unsafe Consumption of APIs
- OWASP Authentication Cheat Sheet
- OWASP Key Management Cheat Sheet
- OWASP Web Service Security Cheat Sheet
- CWE-798: Use of Hard-coded Credentials
- CWE-259: Use of Hard-coded Password
- CWE-321: Use of Hard-coded Cryptographic Key

***

## Important Reminders
[ref: #hardcodedsecrets-important-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- **Subagents are read-only**: they must not modify project source code, configuration files, CI/CD pipelines, or open pull requests.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 candidates per subagent**. If there are 1-3 candidates total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned candidates' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **The key distinction is public accessibility**: a hardcoded AWS key in a Django view is bad practice but NOT a finding for this skill (it's server-side). The same key in a React component IS a finding because it ships to the browser.
- **Trace the import chain when uncertain**: A file at `src/utils/config.ts` might be imported by both server and client code. Check who imports it. If ANY client-side code path imports it, the secrets are exposed.
- **Mobile apps are always public**: All source code in Android, iOS, React Native, Flutter, and Xamarin apps should be treated as extractable. APKs can be decompiled with `apktool`/`jadx`, IPAs can be inspected, JS bundles in React Native are plaintext.
- **Firebase client config is generally NOT a secret**: The standard Firebase client config (`apiKey`, `authDomain`, `projectId`, etc.) is designed for client-side use and protected by Firebase Security Rules. Only flag Firebase **admin/service account** keys or **server keys** (e.g., `FIREBASE_ADMIN_SDK`, service account JSON with `private_key`).
- **Stripe publishable keys are NOT secrets**: `pk_live_*` and `pk_test_*` are designed for client-side use. Only flag `sk_live_*` and `sk_test_*` (secret keys).
- **`NEXT_PUBLIC_*`, `REACT_APP_*`, `VITE_*` env vars**: These are embedded into client bundles at build time. If the code references `process.env.NEXT_PUBLIC_API_KEY`, that IS client-accessible — but the actual hardcoded value would be in the `.env` file, which is typically gitignored. Only flag if the actual secret value is hardcoded in source code, not if it's read from an env var.
- **Scan git history**: Secrets removed from current `HEAD` often survive in `.git/`. Use `git log -p -S'...'`, `git log --all --full-history`, or tools like `truffleHog`/`gitleaks`.
- **Inspect artifacts, not just source**: Docker image layers, Kubernetes manifests, Terraform state, CI logs, source maps, and published documentation sites can all leak secrets.
- **Apply entropy heuristics for generic secrets**: Shannon entropy ≥ 4.5 bits/char, length ≥ 16, mixed charset, combined with secret-related variable names.
- **Redact secrets in output**: When showing code snippets, always partially redact the secret value (e.g., `AKIA****WXYZ`, `sk_live_****abcd`). Never write the full secret value in the results file.
- When in doubt about public accessibility, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/15_recon.md` and all `{{ REPORTS_ROOT }}/15_batch_*.md` files after the final `{{ REPORTS_ROOT }}/15_hardcodedsecrets.md` is written.
