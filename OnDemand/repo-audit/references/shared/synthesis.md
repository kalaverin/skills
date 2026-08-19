---
subject: "Shared synthesis rules; contradiction resolution, no raw dumps, single vs split business report thresholds, root-drawn dependency Mermaid diagram, all-encompassing nodes, verify persist, user summary format, curated artifacts, conflict hierarchy, curation, artifact provenance."
index:
  - anchor: ra-synthesis
    what: "The root-agent synthesis rules for turning wave reports into final memory artifacts."
    problem: "Root assembles final artifacts from nine wave reports; raw dumps, contradictions, and format drift sneak into canonical memory; assembly errors, canonical pollution, paste temptation, curated loss, review burden, trust decay, store corruption."
    use_when: "After wave subagents return; writing any of the three artifacts; reviewing synthesis quality."
    avoid_when: "Wave orchestration — repo-audit/SKILL.md; subagent contracts — `[ref: #ra-subagent-base]`."
    expected: "Final artifacts synthesized, never dumped, with contradictions resolved."
  - anchor: ra-synthesis-contradictions
    what: "Contradiction resolution between fresh reports and existing memory before writing."
    problem: "Fresh report contradicts stored memory; writing both sides poisons canonical knowledge with unresolved divergence; conflicting facts, open clash, hierarchy doubt, truth fork, silent rot, knowledge split, escalation failure, memory conflict, decision vacuum."
    use_when: "Report conflicts with existing memory during synthesis; logging contradictions; hierarchy questions."
    avoid_when: "The protocol itself — `serena-protocol` `[ref: #serena-contradictions]` owns the rules; this section applies them."
    expected: "Every conflict resolved or escalated before any write."
  - anchor: ra-synthesis-no-raw-dumps
    what: "The no-raw-dumps rule: subagent output is synthesized, never pasted into memory."
    problem: "Root pastes whole subagent markdown into memory; canonical store fills with prompt-shaped noise instead of curated knowledge; noise injection, prompt residue, curated loss, dump anti-pattern, shortcut decay, bloat import, quality erosion."
    use_when: "Writing any artifact from subagent reports; reviewing artifact provenance."
    avoid_when: "Quoting evidence lines — short cited fragments are fine; whole-report dumps are not."
    expected: "Memory contains only curated synthesis."
  - anchor: ra-synthesis-single-vs-split
    what: "The single-vs-split decision for the business report (threshold-based)."
    problem: "Business report balloons into unreadable mega-memory or shatters into dozens of trivia files; fragment explosion, readability loss, threshold doubt, split confusion, granularity drift, navigation pain, cohesion decay, size dilemma, structure vacuum, reader abandonment."
    use_when: "Writing `repos/<repo>/business`; entity/process/rule counts near thresholds; naming split files."
    avoid_when: "Split file templates — `references/templates/business_writer.md` owns them."
    expected: "One business.md or a clean split model per the thresholds."
  - anchor: ra-synthesis-diagram
    what: "The root-drawn dependency diagram: all-encompassing Mermaid synthesized from three extractor reports plus the existing card."
    problem: "Diagram delegated to subagent hallucinates edges, or nodes get dropped so picture stays pretty; invented edges, node omission, pretty-over-complete, diagram defects, layout neglect, coverage lies, visual debt, completeness loss, root duty, verification duty, aesthetic trap."
    use_when: "Drawing the dependencies diagram; validating diagram completeness; handling unwieldy graphs."
    avoid_when: "Mermaid syntax rules — `[ref: #ra-conventions-mermaid]` owns them."
    expected: "Every consumer and downstream node present; layout fixes, never drops."
  - anchor: ra-synthesis-persist
    what: "The verify-and-persist step for all written artifacts."
    problem: "Run completes with artifacts written but never checkpointed; next session reads stale store and redoes everything; checkpoint skip, persistence debt, verification skip, lost work, rotten reads, repeated effort, durability gap."
    use_when: "After writing any artifact during synthesis; closing the audit run."
    avoid_when: "The protocol itself — `serena-protocol` `[ref: #serena-memory-mutation]` owns it; this section applies it."
    expected: "Every artifact read back and checkpointed."
  - anchor: ra-synthesis-user-summary
    what: "The user-facing summary format for the completed run."
    problem: "Run ends and user cannot tell what changed, where, or why; invisible outcomes, missing summary, change opacity, user confusion, result ambiguity, silent completion, handoff failure, reporting gap, outcome blindness, closure absence."
    use_when: "Reporting run results to the user; choosing summary contents."
    avoid_when: "Full artifact dumps — summary references paths, not contents."
    expected: "User sees artifacts written, decisions made, and open questions."
---

# Shared Synthesis Rules (repo-audit)

[ref: #ra-synthesis]

How the root agent combines subagent reports into final artifacts. Applies after every wave, in every run mode.

## 1. Contradiction resolution

[ref: #ra-synthesis-contradictions]

Follow `serena-protocol` `[ref: #serena-contradictions]`. The hierarchy:

1. Compare recorded dates and commit hashes of the conflicting memories.
2. A newer memory explicitly overriding an older one wins.
3. `AGENTS.md` wins over session memory unless explicitly overridden.
4. The repo's own git metadata wins over `.serena` metadata for repo-specific facts.
5. An unresolved contradiction = STOP and report to the user; never proceed with an open conflict.

Log every contradiction (resolved and unresolved) in `agent/contradictions` with the conflicting memory names, dates/branches, and the resolution.

## 2. No raw dumps

[ref: #ra-synthesis-no-raw-dumps]

Never route raw subagent output directly to memory. Synthesize, deduplicate, and edit the reports into the final artifact templates (`references/templates/`).

## 3. Single vs split business report

[ref: #ra-synthesis-single-vs-split]

Decide the `business.md` shape:

- **Single file** if: ≤5 domain entities, ≤4 processes, ≤8 rules, AND the result fits under ~300 lines.
- **Split model** otherwise: executive summary at `repos/<repo>/business.md` plus focused files under `repos/<repo>/entities/`, `repos/<repo>/processes/`, `repos/<repo>/rules/`, `repos/<repo>/integrations/`, `repos/<repo>/risks/`. These are files, not directories; names MUST use snake_case.

## 4. Root-drawn dependency diagram

[ref: #ra-synthesis-diagram]

The root agent draws the dependency Mermaid diagram itself during synthesis of `repos/<repo>/dependencies` — from the three dependency extractor reports (interface, downstream, infra) PLUS the existing `repos/<repo>/dependencies` card if present. There is no diagram subagent. The diagram is ALL-ENCOMPASSING: every upstream consumer and every downstream target from the card's tables MUST appear as a node — omitting a node is a defect; if the diagram grows unwieldy, keep all nodes and improve layout (subgraphs, grouping) instead of dropping anything. Diagram rules: `[ref: #ra-conventions]`; validation checklist: `references/checklists.md`.

## 5. Verify and persist

[ref: #ra-synthesis-persist]

Verify and persist per `serena-protocol` `[ref: #serena-memory-mutation]` (read-back + persistence command from the workspace root; the YAML frontmatter is refreshed on every mutation).

## 6. User summary format

[ref: #ra-synthesis-user-summary]

Report to the user (in the user's language):

- Repo name and detected type.
- Mode run (FULL / PARTIAL / REFRESH) and artifact counts (sections, findings by severity and category).
- Subagent counts per wave and any follow-up questions asked.
- Resolved and unresolved contradictions.
- Created vs updated artifacts (paths).
