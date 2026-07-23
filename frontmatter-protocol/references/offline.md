---
subject: "Offline index extension; corpus harvest, batch frontmatter dump, subagent fan-out, evidence-backed anchors, existence validation, hallucination guard, spot check, coverage pass, convergence dedup, pinned manifest, index building, working inventory, selection map, reusable index."
index:
  - anchor: offline-purpose
    what: "The purpose: precompute a pinned index of relevant anchors/sections for one project, so downstream agents lazy-load a known-good set instead of routing from scratch."
    problem: "Every session re-routes same corpus from zero, paying full semantic search cost and landing on slightly different anchor sets each time; repeated routing, drifting selections, startup cost, inconsistent baselines, pinned sets, precomputed relevance."
    use_when: "A project repeatedly consumes the same corpus; onboarding downstream agents to a known-good baseline."
    avoid_when: "One-off lookups — live routing via the lazyload funnel is cheaper than building an index."
    expected: "Downstream agents start from validated baseline anchors, extending only when the live task proves it necessary."
  - anchor: offline-harvest
    what: "Harvest: dump every frontmatter of the corpus into one temporary harvest file via the core batch primitive, kept outside any synced mirror."
    problem: "Index building needs whole card catalog at once; re-extracting per subagent wastes cycles, and writing inventory into synced mirrors gets it wiped; re-extraction waste, sync deletion, temp hygiene, working catalog, batch dump, inventory safety."
    use_when: "Starting any offline index; giving subagents a uniform extraction recipe."
    avoid_when: "Handing the harvest file to subagents — it is the orchestrator's working inventory; subagents harvest their own view."
    expected: "One command produces the complete card catalog, stored where sync cannot delete it."
  - anchor: offline-fanout
    what: "Fan-out: slice the target project into coherent regions and launch one read-only subagent per region to nominate anchors with justification, evidence, and signal."
    problem: "One agent cannot hold whole project against whole catalog; shallow single-pass matching misses region-specific needs that only surface with code in front of you; scale mismatch, region blindness, parallel survey, evidence requirement, nomination format, context limits."
    use_when: "The target project exceeds one context; nominations must be grounded in real code."
    avoid_when: "Tiny projects — direct main-agent survey without fan-out is simpler."
    expected: "Every region returns anchors backed by file:line evidence and a firing signal."
  - anchor: offline-validation
    what: "Aggregation and validation: union nominations, drop anchors absent from declaring cards, spot-check evidence, run a coverage pass, dedup convergence."
    problem: "Subagents hallucinate plausible-but-nonexistent anchors, cite stale evidence, and miss whole stack areas; trusting raw union bakes errors into final manifest; coverage holes, existence check, orchestrator duty, spot checking, stack signals, dedup pass."
    use_when: "Merging subagent nominations; guarding against invented anchors; finalizing the pinned set."
    avoid_when: "Skipping validation for speed — an unvalidated manifest is worse than none."
    expected: "Every pinned anchor exists in its declaring card and is backed by verified evidence."
  - anchor: offline-manifest
    what: "The manifest: the final deduplicated, validated anchor set written as a document — with tracking fields when stored as a Serena memory."
    problem: "Index lives only in chat and dies with session end, or persists without provenance so nobody can tell whether it is outdated weeks later; ephemeral results, lost work, provenance gap, persistence rules, refresh strategy, document format."
    use_when: "Persisting the validated set; deciding where the manifest lives and how it stays fresh."
    avoid_when: "Duplicating card content into the manifest — pin anchors, never inline bodies."
    expected: "The manifest persists as a tracked document; staleness is detectable via the tracking extension."
---

# Reference: offline — Offline Index Building (frontmatter-protocol extension)

Extension of `frontmatter-protocol` (core §9): algorithmic, no frontmatter keys of its own.
It generalizes how to build a **pinned offline index** (map/dictionary) over a lazy-load corpus for one concrete project — the pattern pytest-planner's bootstrap mode implements for `pytest-design`.
Domain specifics (what signals to scan for, where the manifest lives, its content structure) belong to the consuming skill; this document owns only the universal algorithm.

## Purpose

[ref: #offline-purpose]

Live routing (the core §7 loader mechanics, `[ref: #lazy-load-routing]`) answers "what applies to this request right now".
An offline index answers "what applies to THIS PROJECT, always": a precomputed, validated, pinned set of anchors that downstream agents load as their baseline, extending only when the live task proves it necessary.
Build one when a project consumes the same corpus repeatedly; skip it for one-off lookups.

**Design lineage.** The offline index is the curated-context counterpart of per-query retrieval: the same argument that moves agent engineering away from vector RAG toward deterministic, tool-based retrieval (2024–2026 agent-architecture discussions) applies here — a pinned, validated, byte-identical baseline beats probabilistic per-query fetching on determinism, cost, and reliability.

## Harvest

[ref: #offline-harvest]

1. Enter the corpus (for mirror-based setups: the in-root `.kimi/mirror/<skill>/` copy — HARD STOP if the mirror is missing).
2. Dump every frontmatter into a working inventory file with the core batch primitive (core §6, Form 2):

```bash
fd -t f . references/ 2>/dev/null | LC_ALL=C sort -u | while IFS= read -r f; do printf '\n### %s\n' "$f"; awk '/^---[ \t]*$/{c++; if(c==2) exit; next} c==1{print}' "$f"; done > <HARVEST_FILE>
```

3. The harvest file is the orchestrator's working inventory:
   - NEVER write it inside a synced mirror (`--delete` syncs wipe foreign files).
   - NEVER hand it to subagents; subagents produce their own view of the corpus.
   - Filter fields only when the consumer documents why (e.g. dropping `expected:` lines to slim the survey input).

## Fan-Out

[ref: #offline-fanout]

1. Slice the **target project** (not the corpus) into coherent regions — by directory, module, or subsystem — including each region's tests/config where relevant.
2. Launch one read-only subagent per region, in parallel, per `subagents-protocol` (paths, not contents; no MCP for subagents).
3. Each subagent surveys the corpus itself (from the mirror copy, batch-extracting frontmatter and reading sections by their markers) and nominates anchors its region will need.
4. Required nomination format per hit:
   - `anchor` — the exact slug from the declaring card (no `#` prefix);
   - `justification` — one sentence on why it applies to the region;
   - `evidence` — `file:line` proving the trigger;
   - `signal` — the concrete feature that fired (an API, a pattern, a dependency).
5. A subagent returns only evidence-backed anchors; it must not invent anchors and must not summarize cards.

## Validation & Aggregation

[ref: #offline-validation]

The orchestrator (main agent) owns quality:

1. **Union** all nominations.
2. **Existence check (hallucination guard).** Drop any anchor not present BOTH as an `index[].anchor` entry and as a `[ref: #<slug>]` body marker in its declaring file. A nonexistent anchor is a critical failure of the nomination.
3. **Evidence spot-check.** Open a sample of cited `file:line` locations and confirm the signal is real.
4. **Coverage pass.** Walk the project's stack signals (frameworks, async/sync, I/O clients, storage, time handling, CLI, logging, isolation needs, etc. — the consuming skill defines the signal catalog) and confirm each is covered by at least one anchor; add missing anchors yourself.
5. **Convergence dedup.** Several cards sharing one anchor keep the anchor once; preserve the anchor → declaring-file mapping for the manifest.
6. Finalize the deduplicated, validated set.

## Manifest

[ref: #offline-manifest]

1. Persist the pinned set as a **document** — never leave it in chat. Group anchors by declaring file.
2. Pin anchors only: NEVER inline card bodies or rule prose into the manifest; loading stays with the corpus.
3. State the baseline contract: these anchors are mandatory baseline loading; the live task may add more.
4. When the manifest is stored as a Serena memory (or any tracked document), the **tracking extension applies**: stamp `repo`/`branch`/`commit`/`committed_at` at write time, and treat later drift per the staleness protocol.
5. The manifest's own frontmatter, content structure, and storage location are defined by the consuming skill (e.g. pytest-planner writes `agent/tests`).
