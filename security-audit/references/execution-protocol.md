---
subject: "Shared three-stage detection pipeline for SAST scans 02–24; stage contracts — recon with candidate split, per-batch verify, merge; extension points for domain fields; artifact lifecycle; domain files supply recon catalog and verify checklist via anchors."
index:
  - anchor: protocol-stage-model
    what: "The flat three-stage model every detection scan runs: recon subagent finds candidates and splits them into batch files, per-batch verify subagents classify them, merge subagent consolidates — all dispatched directly by the core, which tracks state through artifact files only."
    problem: "Detection scans each re-implement identical orchestration with drift — twenty-three copies of phase mechanics, batching rules, and cleanup logic desynchronize and rot; boilerplate duplication, sync decay, maintenance multiplication, protocol absence, unified mechanics, scattered ownership."
    use_when: "Running any detection scan 02–24; understanding who dispatches whom; authoring or reviewing a scan's execution behavior."
    avoid_when: "Domain content itself — patterns, examples, and heuristics live in the detection files; meta-stage contracts (screener, analysis, validator, report) live in their own files."
    expected: "One file owns all detection-stage mechanics; scans differ only in domain content."
  - anchor: protocol-recon
    what: "Stage 1 contract: the recon subagent reads the domain file's recon catalog, hunts candidates across the codebase, writes `NN_recon.md`, splits candidates into `NN_batch_1..k.md` of at most three each, or writes the final module report directly on the zero-candidate early exit."
    problem: "Orchestrator cannot batch candidates without reading full recon output into its own context — flooding it — yet batching must happen before verify dispatch; batch handoff, split ownership, recon bottleneck, orchestrator overload, queue visibility, file-driven state."
    use_when: "Dispatching or executing the recon stage of any scan; defining or reviewing recon output artifacts."
    avoid_when: "Domain-specific search patterns — those live in the scan's own recon catalog section."
    expected: "Core learns scan state from filenames alone: final report means done, batch files mean verify is due."
  - anchor: protocol-verify
    what: "Stage 2 contract: one verify subagent per batch file reads exactly one `NN_batch_N.md` plus the domain file, classifies each candidate under the scan's tag family using its verify checklist, and writes `NN_verify_N.md`."
    problem: "Unbatched verification either serializes hours of analysis into one context or forces every candidate into shallow review; verification must parallelize without losing per-candidate depth; batch isolation, context slicing, classification rigor, throughput, focused analysis, verdict quality."
    use_when: "Dispatching or executing the verify stage; batch files exist after recon."
    avoid_when: "Merging results — that is the merge stage; verify never reads other batches."
    expected: "Every candidate receives a sourced verdict in its own batch file."
  - anchor: protocol-merge
    what: "Stage 3 contract: the merge subagent reads all `NN_verify_*.md` of one scan, consolidates findings into the final `NN_<name>.md` (grouped by classification, domain merge extensions applied), then deletes all intermediates."
    problem: "Findings scattered across batch files are unusable until unified, yet core-side consolidation would drag every verdict into orchestrator context; merge ownership, result fragmentation, intermediate cleanup, consolidation boundary, artifact hygiene, single report."
    use_when: "All verify batches of one scan are complete; finalizing the module report."
    avoid_when: "Cross-scan consolidation — that belongs to `99-report.md`; merge handles exactly one scan."
    expected: "One clean module report per scan; zero intermediate files remain."
  - anchor: protocol-extension-points
    what: "The declared extension points a domain file may specify in its `## Execution` section: classification family (registry), extra required finding fields (OWASP root-cause, CWE, taint trace), merge grouping (e.g. by category), dynamic-test payload requirements, finding-field set."
    problem: "Uniform mechanics break on legitimate per-scan variation — backdoor verdicts need CWE fields, misconfiguration merges need category grouping, some findings need dynamic tests — and hardcoding variation into protocol forks it; variation handling, per-scan deltas, extension design, hardcode pressure, uniform-vs-specific tension."
    use_when: "Authoring a scan's `## Execution` section; checking whether a domain variation is legal without protocol edits."
    avoid_when: "Adding new stage mechanics — protocol changes require editing this file, never silent per-scan forks."
    expected: "All per-scan variation declares itself through the extension points; the protocol stays scan-agnostic."
  - anchor: protocol-artifacts
    what: "Artifact lifecycle: `NN_recon.md` and `NN_batch_N.md` are born at recon, `NN_verify_N.md` at verify, all three deleted by the merge subagent; only `NN_<name>.md` survives; zero-candidate recon writes the final report directly and leaves no intermediates."
    problem: "Intermediate files accumulate across twenty-three scans and leak stale candidates into later consolidation steps unless one lifecycle rule owns their birth and death; artifact litter, cleanup drift, storage hygiene, retention ambiguity, leftover candidates, state confusion."
    use_when: "Reviewing pipeline hygiene; debugging a missing or leftover intermediate; writing a new scan."
    avoid_when: "Artifacts of meta stages (`00_plan.md`, `01_architecture.md`, `98_validation.md`) — their lifecycle is defined in SKILL.md."
    expected: "After merge, each scan directory state is exactly one final module report."
  - anchor: protocol-reminders
    what: "Closing rules: subagents are read-only on the project, write only their own artifacts, receive paths not inline content, batch size is three, and ambiguous evidence classifies as `NEEDS MANUAL REVIEW` rather than dismissal."
    problem: "Shared mechanics fail silently when individual executors bend constraints — modified sources, missing verdicts, inflated batches — and drift re-enters through execution rather than content; executor discipline, boundary erosion, rule fidelity, conformance decay, uniform behavior."
    use_when: "Briefing any detection-stage subagent; reviewing protocol conformance of a scan run."
    avoid_when: "Domain-specific guardrails — each scan's own reminders section carries those."
    expected: "Every stage subagent behaves identically on mechanics; only domain content varies."
---

# Detection Execution Protocol (shared by scans 02–24)

[ref: #protocol-stage-model]

Every detection scan runs the same three stages, dispatched directly by the core agent (flat model — no nested orchestration). The core tracks progress through artifact filenames only and never reads recon, batch, or verify files.

- **Stage 1 — recon (+split):** one subagent → `NN_recon.md` + `NN_batch_1..k.md` (≤3 candidates each), or the final `NN_<name>.md` on zero candidates.
- **Stage 2 — verify:** one subagent per batch file → `NN_verify_N.md`.
- **Stage 3 — merge:** one subagent per scan → `NN_<name>.md`, then deletes all intermediates.

Conventions: `NN` is the two-digit scan id from `references/registry.md`; the final artifact name (`NN_<name>.md`) and classification family come from the registry row; domain parameters live in the scan's `## Execution` section under `### Recon catalog` and `### Verify checklist`; batch size is 3 candidates.

## Stage 1 — Recon and split

[ref: #protocol-recon]

Dispatch one `coder` subagent with: the scan's reference file path, this protocol file path, and `{{ REPORTS_ROOT }}`. Brief it:

> **Goal**: find every candidate site for the scan's vulnerability class. Read `{{ REPORTS_ROOT }}/01_architecture.md` for stack context, then apply the **Recon catalog** section of the scan reference.
>
> **Subagent constraint**: read-only on the project. You write only under `{{ REPORTS_ROOT }}/`.
>
> **Output — candidates found**: write `{{ REPORTS_ROOT }}/NN_recon.md` (summary + numbered candidate sections: file, lines, endpoint/function, issue type, sensitive properties, code snippet, one-line rationale). Then split the numbered candidates into batch files `{{ REPORTS_ROOT }}/NN_batch_1.md … NN_batch_k.md`, at most **3 candidates per file**, copying each candidate's full text verbatim.
>
> **Output — zero candidates**: write the final module report `{{ REPORTS_ROOT }}/NN_<name>.md` directly with an executive summary (candidates analyzed: 0; scope reviewed; no candidates found), delete `NN_recon.md` if created, and stop.
>
> Return one line: candidate count and the number of batch files written (or `final report written, zero candidates`).

## Stage 2 — Verify (one subagent per batch)

[ref: #protocol-verify]

For each `NN_batch_N.md`, dispatch one `coder` subagent (parallel slots per the core's limit) with: the scan's reference file path, the batch file path, and `{{ REPORTS_ROOT }}`. Brief it:

> **Goal**: verify every candidate in `{{ REPORTS_ROOT }}/NN_batch_N.md`. Read `{{ REPORTS_ROOT }}/01_architecture.md` for context, apply the **Verify checklist** and the tech-stack examples of the scan reference, and classify each candidate under the scan's classification family.
>
> **Subagent constraint**: read-only on the project. You write only `{{ REPORTS_ROOT }}/NN_verify_N.md`.
>
> **Output**: one finding block per candidate — classification tag, file/lines, endpoint, issue, impact, proof, remediation, dynamic test (where the scan's finding fields require it), plus any domain extension fields (see the scan's `## Execution`).

## Stage 3 — Merge (one subagent per scan)

[ref: #protocol-merge]

After all verify batches of a scan complete, dispatch one `coder` subagent with: the scan's reference file path and `{{ REPORTS_ROOT }}`. Brief it:

> **Goal**: read every `{{ REPORTS_ROOT }}/NN_verify_*.md` and consolidate into `{{ REPORTS_ROOT }}/NN_<name>.md`: executive summary (totals per classification), findings grouped by classification (highest severity family first, per the scan's ordering rule), domain merge extensions applied (e.g. grouping by category when the scan declares it). Preserve every field verbatim.
>
> Then **delete** `NN_recon.md`, all `NN_batch_*.md`, and all `NN_verify_*.md` for this scan.

## Extension points

[ref: #protocol-extension-points]

A scan's `## Execution` section MAY declare, and stage subagents MUST honor:

- **Classification family** — from the registry row (standard / backdoor / obfuscation / threat); verdict tags and the ⚠ "likely" marker follow the family.
- **Extra required finding fields** — e.g. OWASP API 2023 root-cause risk and CWE (scans 21–23), taint trace (scan 19).
- **Merge grouping** — e.g. scan 20 groups findings by category inside each classification tier.
- **Dynamic-test payloads** — scans whose findings require concrete PoC commands (e.g. scan 17) name their payload section as the source.
- **Finding-field set** — the scan's `## Execution` lists the exact fields every finding block carries.

A scan MUST NOT introduce new stages, gates, or artifact types outside these extension points; changes to mechanics belong to this protocol file.

## Artifact lifecycle

[ref: #protocol-artifacts]

| Artifact | Born at | Dies at |
|---|---|---|
| `NN_recon.md` | recon (candidates > 0) | merge (or recon itself on the zero-candidate path) — audit/debug trail only: no stage reads it; state flows through batch files |
| `NN_batch_N.md` | recon split | merge |
| `NN_verify_N.md` | verify | merge |
| `NN_<name>.md` | merge (or recon on zero candidates) | persists |

The core detects scan state from filenames alone: `NN_<name>.md` present → scan done; `NN_batch_*.md` present without verifies → verify is due; verifies complete without the final report → merge is due.

## Important reminders

[ref: #protocol-reminders]

- Stage subagents are read-only on the project: no source, test, or configuration edits, ever.
- Every artifact a stage writes (`NN_<name>.md`, `NN_findings.yaml`) starts with the tracked-document header per `frontmatter-protocol` `[ref: #tracking-fields]` (repo = audited entity or `generic`, git identity from the audited repository), followed by the H1 for markdown artifacts.
- Pass paths, never inline reference content, to subagents.
- Batch size is at most 3 candidates; every candidate's full text travels verbatim into its batch file.
- A verify subagent sees exactly one batch — never the whole recon output.
- When evidence is ambiguous, classify as the family's review tag (`[NEEDS MANUAL REVIEW]`), never silently drop.
- Original family labels are preserved end-to-end; the merge never renames tags.
