---
name: feature-archival
description: "Archive a COMPLETED feature's Serena-memory footprint: extract all value via subagents, compress it into an authored record at .serena/memories/archive/<feature>/ (core summary.md + decisions.md + future.md, additive free-form part), verify by a dedicated reconciliation pass, and delete the originals recoverably (the record's archived_from_commit is the last commit where the files still existed; recovery = git show <hash>:memories/<path>). The trigger phrases only LOAD this skill; the pipeline itself starts ONLY on the user's explicit feature-closing command after production rollout ('закрываем фичу', 'заархивируй', 'archive feature'). Owns the archive/ scope (entity-protocol [ref: #entity-namespace-registry]). Never runs automatically or heuristically."
runtime: true
triggers:
  request: "закрываем фичу, закрыть фичу, закрываем feature, заархивируй фичу, архивация фичи, заархивировать фичу, фича в проде закрываем, выкатил в прод закрываем, archive feature, archive the feature, close the feature, feature archival, feature archive"
  reason: "A shipped feature's cross-scope memory footprint must be extracted, compressed into archive/<feature>/, and the originals deleted recoverably."
requires:
  - serena-protocol
  - entity-protocol
version: 0.1.0
---

# SKILL: Feature Archival
[ref: #fa-intro]

Codified pipeline for closing a COMPLETED feature in Serena memory: the cross-scope footprint is extracted, re-thought, compressed into an authored archive record, and the originals are deleted — recoverably, via git. Reference design discussion: `mem:solutions/project/feature_archival_pipeline/`.

## Paths
[ref: #fa-paths]

The memory root is `<workspace>/.serena/memories/` of the CURRENT project. The archive lives at `.serena/memories/archive/<feature>/`; all scope paths in this skill (`style/`, `repos/<repo>/rules`, `project/`, `solutions/...`) are relative to that memory root.

## Trigger discipline
[ref: #fa-trigger-discipline]

The header trigger phrases only LOAD this skill. The pipeline starts ONLY on the user's explicit closing command («закрываем `<feature>`», after production rollout). Never run automatically, never on a heuristic, never "because the feature looks done". A question ABOUT archival is not a closing command. If the feature slug is ambiguous or not derivable from the command — STOP and ask.

## Pipeline
[ref: #fa-pipeline]

```
0. Preconditions: .serena MUST be a git repository and `just serena-checkpoint` (the configured
   Serena memory persistence command — commits the .serena repo) MUST be available; otherwise STOP
   (deletion would be unrecoverable). Collision check: archive/<feature>/ must not exist (the slug
   is unique exactly within the archive/ scope; this dir-absence check IS the uniqueness check);
   if the user indicates the slug was already used for a DIFFERENT feature — STOP and pick a
   qualified slug. (Re-entry after a declined gate No.2 skips ONLY the collision check — the
   preconditions above always apply; see [ref: #fa-deletion].)
1. FULL listing of .serena/memories/ → the main agent itself judges relatedness FROM THE LISTING
   ONLY (paths/names); at this step the main agent does NOT open files — opening happens in subagents.
   The domain vocabulary is read from file NAMES and paths, not from content.
2. Ripgrep by the keyword set: the feature slug, its morphological variants (snake/camel/kebab/space
   forms — e.g. `trade_stats`, `trade-stats`, `trade stats`, `tradestats`), and 3–8 distinctive
   domain terms derived from the names/paths seen at step 1 (table/endpoint/workflow names,
   ticket ids) → additions.
3. Inventory: every candidate with its class (produced-by / touched-by / mention-only) + the keyword
   set + PROVISIONAL candidate re-homes (from listing-level judgment; confirmed by the extractors
   at step 4).
   → GATE No.1: the inventory is presented to the user as one classed list; explicit approval
   (moving items between classes allowed). Explicit approval = an unambiguous affirmative reply
   to a standalone question; anything else is NOT an approval — a partial or ambiguous reply
   refines the list and the question is re-asked. Gate No.1 covers BOTH the inventory AND the
   re-home execution of step 5.
4. The produced-by list is split across coder subagents ([ref: #fa-subagents]) → classification
   confirmation (each file's class confirmed with a verdict + an evidence quote) + extraction
   → staging.
5. Synthesis: the main agent reads the staged extractions and writes archive/<feature>/
   ([ref: #fa-record]); approved re-homes are executed (fragments are COPIED into the timeless
   scopes). Re-homes are additive and were approved at gate No.1; if gate No.2 is later declined,
   the copies STAY (they are independently valuable; rollback is a plain git operation) and the
   next entry continues the pipeline.
6. Reconciliation pass ([ref: #fa-reconciliation]): fresh clean-context subagents verify the record
   against the originals. Only a clean report (zero discrepancies) opens gate No.2.
7. GATE No.2: the user is shown the record's paths, the exact deletion list (filesystem paths of the
   produced-by files), and the recovery plan — and gives an explicit MASTER APPROVAL of the deletion
   (same approval semantics as gate No.1). Extractor flags newly approved HERE are copied to their
   re-homes IMMEDIATELY after the approval, before deletion.
   → capture `git -C <workspace>/.serena rev-parse HEAD` (the last commit where the originals exist)
   → delete ALL produced-by originals (re-homed fragments were already copied at step 5)
   → IMMEDIATELY `just serena-checkpoint`
   → write the captured pre-deletion HEAD into the record header as archived_from_commit and verify
     it: `git cat-file -e <hash>:memories/<a deleted path>` MUST succeed (the files exist at the
     recorded commit). Any failed checkpoint or failed verification = STOP: retry, then escalate
     to the user; never write or keep an unconfirmed hash.
8. Verify ([ref: #fa-deletion]).
9. Final `just serena-checkpoint` (commits the archived_from_commit header update).
```

## Detection and classes
[ref: #fa-detection]

- Recall beats precision AT DETECTION: a missed file is silent knowledge loss; precision is enforced at gate No.1, where the user prunes false positives.
- Classes:
  - `produced-by-feature`: created by the feature work (its decisions, plans, experiments, journals) → archived, then deleted.
  - `touched-by-feature`: living documents updated by the feature (`repos/*/overview`, glossaries, `project/*`) → stay.
  - `mention-only`: passing mentions → stay.
- A closing feature's `solutions/<repo>/<subject>/` journal (discuss-first `[ref: #df-solutions-journal]`) is produced-by: it is absorbed into the record; the chain survives in git per `[ref: #fa-deletion]`.

## Subagent discipline (HARD)
[ref: #fa-subagents]

- Type `coder` (staging writes need WriteFile; `explore` is read-only). Explicit `model` per subagents-protocol on EVERY launch.
- Subagent context is ~200K tokens. Prompts are SELF-CONTAINED: an explicit ban on reading AGENTS.md, bootstrap, any SKILL.md, or the skills mirror.
- Prompt template (the prompt carries EXACTLY this, nothing more):
  - the class definitions, one line each: `produced-by-feature` = created by the feature work → archived, then deleted; `touched-by-feature` = a living document updated by the feature → stays; `mention-only` = a passing mention → stays;
  - the assigned file list (absolute paths);
  - the staging path `.tmp/archival/<feature>/<NN>.md` (`NN` = chunk number);
  - the report format: per file — verdict (`produced-by` / `touched-by` / `mention-only`) + one evidence quote; NO extractions inline;
  - the staging file schema: per file — `## <path>`, the verdict, and the extracted value (decisions with reasons, requirements, experiment outcomes, open threads) re-stated in the subagent's own words.
- Chunk sizing by token estimate (`bytes/4` per file — a heuristic, not a guarantee): ≤ ~120K for reads+greps per chunk; the rest is reserved for the report. The main agent computes the split before launching.
- Every produced-by file MUST have a non-empty staging extraction before synthesis starts. A failed or empty chunk is re-run ONCE; a second failure is escalated to the user — never silently skipped.
- Extractors also flag timeless bits (repo-wide conventions, cross-feature decisions) with a one-line justification; flags NOT already approved at gate No.1 are presented at gate No.2.

## The archive record
[ref: #fa-record]

- Location: `.serena/memories/archive/<feature>/`. Flat AT THE SCOPE LEVEL: no `<repo>` level, no per-repo subdirs (a feature spans repos). The free-form part MAY grow its own subtree inside the feature dir.
- Fixed core (MANDATORY, with fixed section headers — every header present and non-empty; this is what step 8 verifies mechanically):
  - `summary.md`: `## Business requirements` (final), `## How it is built`, `## What is supported`, `## Attention` (risks; also the home of the "deletion declined" notice, `[ref: #fa-deletion]`).
  - `decisions.md`: `## Decisions` (ALL decisions taken), `## Superseded branches` (cancelled/superseded branches with brief experiment descriptions and reasons).
  - `future.md`: `## Extensions` (what else can be done; what is ready for extension).
- Free-form part: additive only, for content that resists the core schema.
- Tracking header per `frontmatter-protocol` `[ref: #tracking-fields]`, plus `archived_from_commit` (filled at step 7): the LAST commit where the deleted files still existed — the commit the record can be restored FROM.
- Compression doctrine: re-think, do not copy-paste. Observable proxy: the record is written in the agent's own words; verbatim fragments are the exception and are marked as quotes. Duplicated content collapses into one statement; chronology is explicit; later decisions visibly supersede earlier temporary ones.
- Re-homes are written via the normal serena-protocol MCP path (`[ref: #serena-memory-mutation]`) into `style/`, `repos/<repo>/rules`, or `project/` (under the memory root). The direct-write waiver of discuss-first `[ref: #df-solutions-journal]` (`mem:agent/allowed_violations`) covers ONLY solutions/ journal cards — never re-homes.

## Reconciliation pass
[ref: #fa-reconciliation]

After synthesis, BEFORE any deletion, fresh clean-context subagents — NEW instances only, never resumed/warm ones (same discipline as `[ref: #fa-subagents]`) — verify the record against the originals:

1. **Completeness** — every produced-by file's value is ported into the record.
2. **Chronology** — the timeline is not confused (dates, order of decisions, experiment sequence).
3. **Supersession** — later decisions properly overwrote temporary earlier ones; no ghosts of cancelled branches read as live decisions.

Output: a discrepancy report. "Clean" = zero discrepancies. The main agent fixes the record in ONE batch; if the batch changed more than typos, the affected aspects are re-verified. Only a clean report opens gate No.2.

## Deletion, verification, recovery
[ref: #fa-deletion]

- Gate No.2 ordering is load-bearing: approve → capture pre-deletion HEAD → delete → checkpoint → write `archived_from_commit` into the record → verify → final checkpoint. The saved hash is the LAST commit where the deleted files still existed (the commit the record can be restored FROM); the final checkpoint only commits the header update and is NEVER the recorded hash.
- Checkpoint discipline: any failed checkpoint (deletion or final) = STOP — retry, then escalate to the user (escalation = STOP and ask in the chat); `archived_from_commit` is written only for a commit confirmed by the pipeline step-7 verification (`[ref: #fa-pipeline]`).
- Verification methods (step 8): `rg --files archive/<feature>/` shows the record; each core file carries its fixed section headers from `[ref: #fa-record]`, all present and non-empty; every deleted path is absent from the memory root (`fd`/`test ! -e`); each re-home target exists and mentions the feature; `.tmp/archival/<feature>/` is removed.
- Recovery recipe, to be quoted in the record's `summary.md`: the deleted files exist AT the recorded commit — `git -C <workspace>/.serena show <hash>:<path>` for one file, `git -C <workspace>/.serena checkout <hash> -- <paths>` to restore. `<path>` here is git-repo-relative: `memories/` + the memory-root-relative path used everywhere else in this skill (e.g. `decisions/analytics_wf/trade_stats_x.md` → `memories/decisions/analytics_wf/trade_stats_x.md`).
- If gate No.2 is declined: the record stays, the originals stay, the already-executed re-homes stay (step 5; rollback, if wanted, is a plain git operation); add `deletion declined` under `## Attention` in `summary.md` and stop. A later closing command re-enters at step 7 directly (only the step-0 collision check is skipped — preconditions always apply). On re-entry, first reconcile the deletion list against the CURRENT memory state (files re-created since the decline are scraps → `[ref: #fa-scraps]`); if the record or the footprint changed materially, run a fresh reconciliation pass (`[ref: #fa-reconciliation]`) before gate No.2.

## Scraps route (maintenance)
[ref: #fa-scraps]

Stale-context agents may still write into deleted paths or old scopes after archival. Such scraps — noticed by the agent or reported by the user — are collected, summarized, and stored in `archive/<feature>/scraps.md` (or `scraps/` if it outgrows one file). This is a maintenance operation, not part of the pipeline.

## Hard rules
[ref: #fa-hard-rules]

- NEVER start the pipeline without the explicit closing command (trigger phrases only load the skill).
- NEVER delete before gate No.2's explicit master approval, and never delete anything not in the approved produced-by inventory.
- NEVER synthesize from an incomplete staging set; NEVER skip a failed chunk silently.
- NEVER skip the reconciliation pass.
- NEVER let subagents read bootstrap/AGENTS.md/skills — their context budget is the constraint.
- NEVER run the pipeline when `.serena` is not a git repository or the checkpoint command is unavailable.
- NEVER proceed past a failed checkpoint and never write `archived_from_commit` for an unconfirmed commit.
- Record language: technical English.
