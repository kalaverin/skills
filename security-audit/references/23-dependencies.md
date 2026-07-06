# Supply Chain / Dependency Security Detection

[ref: #dependencies-detection]

You are performing a focused security assessment to find **supply-chain risks in third-party dependencies**. This includes typosquatting, dependency confusion, known CVEs, abandoned packages, suspicious maintainer changes, and compromised registry packages. This skill uses a three-phase approach with subagents: **recon** (find risky dependency indicators), **batched verify** (confirm which indicators are real threats, in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

## Table of contents

- [What is supply chain / dependency risk](#what-is-supply-chain--dependency-risk)
- [Dependency Attack Taxonomy](#dependency-attack-taxonomy)
- [Vulnerable vs. Secure Examples](#vulnerable-vs-secure-examples)
- [Detection heuristics per category](#detection-heuristics-per-category)
- [Execution](#execution)
- [OWASP API Security Top 10 2023 mapping](#owasp-api-security-top-10-2023-mapping)
- [CWE references](#cwe-references)
- [Important Reminders](#important-reminders)
- [References](#references)

---

## What is supply chain / dependency risk

Modern applications depend on hundreds or thousands of third-party packages. Attackers abuse this trust by publishing malicious packages, taking over legitimate ones, exploiting known vulnerabilities, or tricking package managers into resolving internal names to public registries.

The core question: *do the dependencies in this project come from trustworthy sources, contain no known vulnerabilities, and behave only as documented?*

### What is in scope

- **Typosquatting**: package names deliberately similar to popular ones (`lodahs` vs `lodash`).
- **Dependency confusion**: public packages registered under names that match private/internal packages.
- **Known CVEs**: dependencies with publicly disclosed, exploitable vulnerabilities.
- **Abandoned packages**: dependencies that are unmaintained, have a single inactive maintainer, or lack security response.
- **Suspicious maintainer changes**: sudden ownership transfers, new versions from unknown maintainers, or MFA/policy downgrades.
- **Compromised registry packages**: legitimate packages that have had malicious versions published via stolen maintainer credentials or build-system compromise.

### What is out of scope

Do not flag these as supply-chain findings on their own:

- **License conflicts** — legal/compliance issue, not a security vulnerability.
- **Outdated but non-vulnerable packages** — update hygiene is good, but not a finding unless a CVE or exploit path exists.
- **Dependencies that are merely large or complex** — focus on trust and behavior, not code volume.
- **Internal/vendored code** — covered by other scans unless it is distributed as a package.

### Patterns that prevent supply-chain risk

When you see these patterns, the dependency posture is likely **strong**:

**1. Pinned versions with cryptographic lockfiles**
```json
// package-lock.json / yarn.lock / pnpm-lock.yaml with integrity hashes
"lodash": {
  "version": "4.17.21",
  "resolved": "https://registry.npmjs.org/lodash/-/lodash-4.17.21.tgz",
  "integrity": "sha512-..."
}
```

**2. Private registry scoping**
```ini
# .npmrc — internal scopes never fall back to public npm
@mycompany:registry=https://npm.mycompany.com
```

**3. SCA / SBOM in CI**
- Every build generates an SBOM.
- SCA tooling blocks packages with critical CVEs or untrusted maintainers.
- New dependencies require explicit approval.

---

## Dependency Attack Taxonomy

| Category | Mechanism | Typical signals |
| --- | --- | --- |
| **Typosquatting** | Attacker registers a name that looks like a popular package but is a common misspelling. | Name differs from a top package by 1-2 characters (`requesst`, `lodahs`, `colourama`); low download count; recently published; no repository link. |
| **Dependency confusion** | Attacker publishes a malicious public package with the same name as an internal/private package, often with a higher version. | Package name matches internal package but resolves to public registry; version number is suspiciously high (`100.100.100`); no source repo in the organization. |
| **Known CVEs** | Project depends on a version with a published vulnerability that may be exploitable in the application's context. | SCA scanner reports CVEs; NVD/OSV/GitHub Advisories entries; vulnerable functions reachable from application code. |
| **Abandoned packages** | Unmaintained package with a single maintainer, no releases for years, or open security issues. | Last release > 2 years ago; single maintainer with no activity; many unaddressed issues/PRs; no security policy. |
| **Suspicious maintainer changes** | New maintainer, sudden version burst, or policy change that indicates account takeover or social engineering. | Maintainer email/domain changes; MFA disabled; new versions published in rapid succession after long silence; version has no changelog or GitHub tag. |
| **Compromised registry packages** | Legitimate package has a malicious version published via stolen credentials or CI compromise. | New version contains obfuscated `postinstall` / `preinstall` scripts; unexpected network calls during install; version not reflected in source repository; inflated size or new native dependencies. |

---

## Vulnerable vs. Secure Examples

### Typosquatting

```json
// VULNERABLE: typo-squatted package in package.json
{
  "dependencies": {
    "lodash": "^4.17.21",
    "lodahs": "^1.0.0"
  }
}

// SECURE: only legitimate, verified package names
{
  "dependencies": {
    "lodash": "^4.17.21"
  }
}
```

### Dependency confusion

```ini
# VULNERABLE: internal scope can fall back to public npm
@mycompany:registry=https://npm.mycompany.com
# Missing registry for @mycompany-data → npm will query registry.npmjs.org

# SECURE: every internal scope is locked to the private registry
@mycompany:registry=https://npm.mycompany.com
@mycompany-data:registry=https://npm.mycompany.com
registry=https://registry.npmjs.org
```

### Known CVEs

```python
# VULNERABLE: log4j 2.14.1 is affected by Log4Shell (CVE-2021-44228)
# build.gradle
implementation 'org.apache.logging.log4j:log4j-core:2.14.1'

# SECURE: patched version
implementation 'org.apache.logging.log4j:log4j-core:2.17.1'
```

### Abandoned package

```json
// RISKY: package with no updates and a single inactive maintainer
{
  "dependencies": {
    "left-pad": "1.3.0"
  }
}

// SECURE: actively maintained alternative with a security policy
{
  "dependencies": {
    "pad-start": "^2.0.0"
  }
}
```

### Suspicious maintainer change

```text
# VULNERABLE: new version 99.99.99 published by an unknown maintainer
# after two years of silence, with no matching GitHub release tag

# SECURE: versions follow semver, changelog is present,
# releases are signed and published by known maintainers
```

### Compromised registry package

```json
// VULNERABLE: new version of a trusted package adds an install-time script
{
  "name": "trusted-utils",
  "version": "3.5.22",
  "scripts": {
    "postinstall": "node scripts/postinstall.js"
  }
}
// scripts/postinstall.js is obfuscated and fetches a remote payload.

// SECURE: package has no install scripts; build is reproducible and signed
{
  "name": "trusted-utils",
  "version": "3.5.21",
  "scripts": {}
}
```

---

## Detection heuristics per category

### Typosquatting

- Compare every direct dependency name to the top packages in its registry using edit distance (Levenshtein ≤ 2 is suspicious).
- Flag packages with very low download counts, no README, no repository, or recently created.
- Check for homoglyphs (`colour` vs `color`, Unicode lookalikes) and extra/missing separators.

### Dependency confusion

- Identify package names that look internal (contain company/project names) but are resolved from public registries.
- Check `.npmrc`, `.yarnrc`, `pip.conf`, `maven` settings, and `NuGet.config` for scope/registry mapping.
- Flag versions that are dramatically higher than the internal release history (`100.100.100`).
- Verify that internal scopes are pinned to private registries and cannot fall back to public indexes.

### Known CVEs

- Run SCA tooling against manifests: `package.json`, `requirements.txt`, `Pipfile.lock`, `Cargo.toml`, `pom.xml`, `build.gradle`, `go.mod`, `Gemfile.lock`, etc.
- Cross-reference findings with NVD, OSV, GitHub Security Advisories, and vendor advisories.
- Determine **exploitability in context**: a CVE in a dev-only dependency is lower risk than one in a runtime web-framework dependency.
- Check for reachable vulnerable functions using call-graph or taint analysis where possible.

### Abandoned packages

- Query registry metadata: last publish date, number of maintainers, maintainer activity, issue/PR response time.
- Flag packages whose last release is > 2 years old and whose only maintainer has no recent activity.
- Check whether the package has a security policy, responsible disclosure process, or documented ownership.
- Prefer packages with multiple active maintainers and a clear governance model for critical dependencies.

### Suspicious maintainer changes

- Compare current maintainers to historical maintainers from registry metadata or previous lockfiles.
- Flag sudden email/domain changes, removal of co-maintainers, or MFA policy changes.
- Look for version bursts after long silence, especially without corresponding source-repo tags or changelogs.
- Check whether new versions are signed with the same key as previous releases.

### Compromised registry packages

- Inspect install/lifecycle scripts (`postinstall`, `preinstall`, `setup.py`, `install` hooks) for network access, obfuscation, or dynamic code execution.
- Compare package contents to the published source repository (tag, commit hash, diff).
- Flag unexpected native extensions, new dependencies, or large size increases.
- Check whether the package makes outbound network requests during install or runtime to unknown destinations.
- Use registry audit logs (npm audit, PyPI transparency, etc.) to spot unauthorized publishes.

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Recon — Find Dependency Risk Indicators

Launch a subagent with the following instructions:

> **Goal**: Find every dependency-related supply-chain risk indicator in the project. Write results to `{{ REPORTS_ROOT }}/23_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, package manager(s), registry configuration, and internal vs. external dependency conventions.
>
> **What to search for**:
>
> 1. **Dependency manifests**:
>    - Node.js: `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
>    - Python: `requirements.txt`, `Pipfile`, `Pipfile.lock`, `pyproject.toml`, `poetry.lock`
>    - Java: `pom.xml`, `build.gradle`, `gradle.lockfile`
>    - .NET: `*.csproj`, `packages.config`, `PackageReference`
>    - Go: `go.mod`, `go.sum`
>    - Ruby: `Gemfile`, `Gemfile.lock`
>    - Rust: `Cargo.toml`, `Cargo.lock`
>
> 2. **Registry configuration**:
>    - `.npmrc`, `.yarnrc`, `.pnpmfile.cjs`, `pip.conf`, `maven` settings, `NuGet.config`
>    - Check whether internal scopes are locked to private registries.
>
> 3. **Typosquatting candidates**:
>    - Direct dependency names that are close edits to popular packages.
>    - Low-download, no-repo, or recently created direct dependencies.
>
> 4. **Dependency confusion candidates**:
>    - Package names that look internal but resolve from public registries.
>    - Inflated version numbers on internal-looking packages.
>
> 5. **Known CVEs**:
>    - Outdated dependencies with known CVEs (cross-reference NVD/OSV/GitHub Advisories).
>    - Focus on runtime dependencies first; note dev-only findings separately.
>
> 6. **Abandoned packages**:
>    - Packages whose last release is > 2 years ago.
>    - Packages with a single inactive maintainer.
>
> 7. **Suspicious maintainer changes**:
>    - New maintainers, email/domain changes, MFA downgrades, version bursts after silence.
>
> 8. **Compromised package indicators**:
>    - Install-time scripts that perform network calls or dynamic execution.
>    - Obfuscated code in dependency files.
>    - Mismatch between package version and source repository tag.
>
> **What to skip**:
> - Internal/vendored source code (not distributed as a package).
> - License-only issues.
> - Outdated packages with no CVE and no behavioral risk.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/23_recon.md`:
>
> ```markdown
> # Supply Chain / Dependency Recon: [Project Name]
>
> ## Summary
> Found [N] dependency risk indicators: [X] typosquatting, [Y] dependency confusion, [Z] CVEs, etc.
>
> ## Risk Indicators
>
> ### 1. [Descriptive name]
> - **Category**: [typosquatting / dependency-confusion / known-cve / abandoned / maintainer-change / compromised]
> - **Package**: `name@version`
> - **Manifest file**: `path/to/manifest` (lines X-Y)
> - **Indicator**: [the specific signal]
> - **Code snippet / evidence**:
>   ```
>   [relevant manifest lines or registry metadata]
>   ```
> - **Why it matters**: [one-line rationale]
>
> [Repeat for each indicator]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/23_recon.md`. If the recon found **zero risk indicators** (the summary reports "Found 0" or the "Risk Indicators" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/23_dependencies.md` and stop:

```markdown
# Supply Chain / Dependency Analysis Results

No dependency supply-chain risks found.
```

Only proceed to Phase 2 if Phase 1 found at least one risk indicator.

### Phase 2: Verify — Confirm Real Supply-Chain Threats (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/23_recon.md` and split the indicators into **batches of up to 3 indicators each**. Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned indicators and writes results to its own batch file.

**Batching procedure**:

1. Read `{{ REPORTS_ROOT }}/23_recon.md` and count the numbered indicator sections (`### 1.`, `### 2.`, etc.).
2. Divide them into batches of up to 3. For example, 8 indicators → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those indicator sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned indicators.
5. Each subagent writes to `{{ REPORTS_ROOT }}/23_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary package manager and language from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions:

> **Goal**: For each assigned dependency risk indicator, determine whether it represents a real supply-chain threat. Write results to `{{ REPORTS_ROOT }}/23_batch_[N].md`.
>
> **Your assigned indicators** (from the recon phase):
>
> [Paste the full text of the assigned indicator sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand the package manager, registry setup, and which dependencies are runtime vs. development-only.
>
> **Supply-chain reference — what to look for**:
>
> For each indicator, answer:
>
> 1. **Typosquatting**: Is the name within ≤ 2 edits of a popular package? Is it a known malicious package? Does it have a repository and legitimate usage?
> 2. **Dependency confusion**: Does the package name match an internal package? Does it resolve from a public registry? Is the version suspiciously high? Is the internal scope locked in `.npmrc`/equivalent?
> 3. **Known CVE**: Is the CVE confirmed for this version? Is the vulnerable function reachable from application code? Is a patch available?
> 4. **Abandoned package**: How old is the last release? How many active maintainers remain? Is there a security policy or replacement?
> 5. **Suspicious maintainer change**: Did the maintainer list or email change? Is there a corresponding source-repo tag/changelog? Is the version signed?
> 6. **Compromised package**: Does the package contain install-time scripts that contact the network or execute dynamic code? Does the package content match the source repository?
>
> **Vulnerable vs. secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Confirmed Threat**: A real typosquat, dependency-confusion package, exploitable CVE, abandoned critical dependency, suspicious maintainer takeover, or compromised version.
> - **Likely Threat**: Strong signal but some uncertainty (e.g., no public advisory yet, unusual but not confirmed malicious version).
> - **Low Risk / Acceptable**: CVE in dev-only dependency with no runtime path, old but well-maintained stable package, intentional internal package.
> - **Needs Manual Review**: Cannot verify from metadata alone; requires registry audit, maintainer contact, or runtime analysis.
>
> **Required fields for every finding**:
> - **OWASP API 2023 root-cause risk**: choose API8:2023 Security Misconfiguration and/or API10:2023 Unsafe Consumption of APIs, and explain why.
> - **CWE**: map to the most specific CWE from the reference (e.g., CWE-1104, CWE-1035, CWE-912, CWE-506).
> - **Verification steps**: describe how to confirm the finding safely (registry lookup, SCA scan, source-repo diff, `npm view`, `pip show`, etc.).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/23_batch_[N].md`:
>
> ```markdown
> # Supply Chain Batch [N] Results
>
> ## Findings
>
> ### [CONFIRMED THREAT] Descriptive name
> - **File**: `path/to/manifest.ext` (lines X-Y)
> - **Package**: `name@version`
> - **Category**: [typosquatting / dependency-confusion / known-cve / abandoned / maintainer-change / compromised]
> - **OWASP API 2023 root-cause risk**: [API8 / API10 / both]
> - **CWE**: [CWE-1104 / CWE-1035 / CWE-912 / CWE-506 / ...]
> - **Issue**: [e.g., "Dependency confusion: @mycompany/api resolves to public npm at v100.100.100"]
> - **Evidence**:
>   ```
>   [manifest lines, registry output, SCA result]
>   ```
> - **Impact**: [code execution, data exfiltration, DoS, etc.]
> - **Remediation**: [remove package, pin to private registry, upgrade version, rotate secrets]
> - **Verification Steps**:
>   ```
>   [safe read-only commands]
>   ```
>
> ### [LIKELY THREAT] Descriptive name
> ...
>
> ### [LOW RISK] Descriptive name
> ...
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> ...
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/23_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/23_dependencies.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/23_batch_1.md`, `{{ REPORTS_ROOT }}/23_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/23_dependencies.md` using this format:

```markdown
# Supply Chain / Dependency Analysis Results: [Project Name]

## Executive Summary
- Dependency risk indicators analyzed: [total across all batches]
- Confirmed Threat: [N]
- Likely Threat: [N]
- Needs Manual Review: [N]
- Low Risk / Acceptable: [N]

## Findings

[All findings from all batches, grouped by classification:
 CONFIRMED THREAT first, then LIKELY THREAT, then NEEDS MANUAL REVIEW, then LOW RISK.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/23_dependencies.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/23_batch_*.md`).

---

## OWASP API Security Top 10 2023 mapping

| OWASP Risk | Why Dependency Security Matters |
|---|---|
| **API8:2023 Security Misconfiguration** | Using vulnerable, abandoned, or untrusted dependencies is a configuration/hardening failure. |
| **API10:2023 Unsafe Consumption of APIs** | Malicious or compromised dependencies can abuse third-party APIs, exfiltrate data, or execute arbitrary code. |

---

## CWE references

- CWE-1104: Use of Unmaintained Third-Party Components
- CWE-1035: OWASP Top Ten 2017 Category A9 — Using Components with Known Vulnerabilities
- CWE-506: Embedded Malicious Code
- CWE-912: Hidden Functionality
- CWE-1357: OWASP Top Ten 2021 Category A06 — Vulnerable and Outdated Components
- CWE-1395: OWASP Top Ten 2021 Category A08 — Software and Data Integrity Failures

CWE-1104 and CWE-1035 are the parent weaknesses for most findings produced by this scan.

---

## Important Reminders

- **Dependency confusion is a registry misconfiguration**, not a code bug. The fix is registry scoping, not patching application logic.
- **A CVE is only a finding if it is exploitable in context.** A vulnerability in a dev-only linter that never processes attacker input is lower priority than one in a runtime HTTP parser.
- **Typosquatting detection requires edit-distance checks against top packages.** Do not rely on visual inspection alone.
- **Always inspect install/lifecycle scripts** in suspicious packages (`postinstall`, `preinstall`, `setup.py`, `install` hooks). These execute automatically and are a common payload delivery mechanism.
- **Compare package contents to source repository** when a compromised version is suspected. Mismatched tags, missing changelogs, and obfuscated scripts are strong indicators.
- **Rotate credentials** if a compromised package was installed or built in any environment.
- **Generate and review an SBOM** for the project; it is the authoritative inventory for incident response.
- Subagents are read-only: they must not modify project source code, commit changes, or run destructive commands against registries.

---

## References

- OWASP API Security Top 10 2023 — API8:2023 Security Misconfiguration
- OWASP API Security Top 10 2023 — API10:2023 Unsafe Consumption of APIs
- CWE-1104: Use of Unmaintained Third-Party Components
- CWE-1035: Using Components with Known Vulnerabilities
- CWE-1395: Software and Data Integrity Failures
- Microsoft Threat Intelligence: Malicious npm packages abuse dependency confusion to profile developer environments
- Microsoft Threat Intelligence: Typosquatted npm packages used to steal cloud and CI/CD secrets
- Checkmarx: How Supply Chain Attacks Work
- SLSA: Dependency Confusion and Typosquatting
- OSV.dev Open Source Vulnerabilities
- NVD National Vulnerability Database
