# Prompt: Reference Corpus Standardization (Six-Phase Orchestration)

Copy this prompt, fill the `{{...}}` inputs, and give it to the main agent. The main agent orchestrates; subagents execute per-file work. The output is a target skill whose entire `references/` corpus conforms to the Cross-Skill Reference File & Frontmatter Standard.

## Inputs

- `{{SKILL}}` — target skill name (e.g. `security-audit`).
- `{{SKILL_PATH}}` — path to the skill directory (e.g. `security-audit/`).
- `{{TIER_NOTE}}` — optional taxonomy note (e.g. "split into required/optional tiers" or "flat references/").

## Role and binding documents

You are the main agent (orchestrator). Before any work, complete the project Startup Gate and load: `bootstrap`, `shell-protocol`, `serena-protocol`, `markdown-protocol`, `todo-protocol`, `subagents-protocol`, `kagi-search`, `read-for-comments`.

Binding documents (read them yourself; pass **paths** to subagents — subagents read skill files ONLY from the mirror `.kimi/mirror/`):

- The standard: `bootstrap/references/REFERENCE_STANDARD.md` (mirror: `.kimi/mirror/bootstrap/references/REFERENCE_STANDARD.md`). Every rule about frontmatter, cards, anchors, body skeleton, and the loader contract lives there.
- The reference implementation: `pytest-design/references/` — study 2–3 files (e.g. `required/mocking.md`, `optional/asyncio.md`) as living examples of the end state.
- Serena rules: `agent/rules` memory (frontmatter editing rules: `use_when` never repeats `problem`, `avoid_when` never opens with "Do not", the pre-save checklist).

Hard constraints:

- Subagents have NO MCP access: no Serena, no Kagi. All memory writes and all web research are yours alone.
- All reasoning, memory entries, plans, and file content in English; user-facing chat in Russian.
- Never use `AskUserQuestion` / `EnterPlanMode` / `ExitPlanMode`. Ask in plain chat and STOP until the user replies.
- Per-file approval gate: each file (or explicitly approved batch) requires the user's go-ahead before work starts.
- After every Serena memory mutation: read it back, then run `just serena-checkpoint` from the workspace root.

---

## Phase 0 — Study the skill and create the Serena plan

Do this phase yourself (or delegate pure reading to ONE `explore` subagent). No file modifications.

1. Read `{{SKILL_PATH}}/SKILL.md`, its `README.md`, and **every** file under `{{SKILL_PATH}}/references/` (use subagents for large corpora; demand a per-file report).
2. Build the inventory: for each reference file — path, line count, content type (recipe collection / narrative / lookup table), current structure (headings outline), existing `[ref: #...]` markers (if any), existing frontmatter (if any), and the logical section groups you propose.
3. Verify the entity gate: an entity card MUST exist at `entities/{{SKILL}}` in Serena memory. If missing — STOP and ask the user to create it via `project-audit`; do not proceed.
4. Write the plan memory `plans/{{SKILL}}/reference_standardization` (YAML frontmatter per the memory metadata protocol). The plan MUST contain, for EVERY reference file, the full phase checkbox list — this is the cross-session progress tracker:

```markdown
## <relative/path/to/file.md> (<lines> lines, <content type>)

- [ ] P1 formatting (H1, section grouping, `[ref]` anchors)
- [ ] P2 Kagi enrichment
- [ ] P3 validation + draft frontmatter
- [ ] P4 frontmatter polish
```

Plus global items:

```markdown
## Global

- [ ] P0 inventory complete
- [ ] P5 summary + skill loader section + skill prompts written
```

5. Present the inventory and the proposed section grouping per file to the user. STOP and wait for approval. Record the approved plan decisions in the plan memory.

---

## Phase 1 — Formatting (subagents, one per file or per approved batch)

Goal: bring every raw reference to the standard's body skeleton — WITHOUT frontmatter and WITHOUT changing technical substance. This is the phase that matters for corpora that have no anchors yet (e.g. `security-audit`); skip per-file where the corpus is already conformant (e.g. `api-design`).

For each file, launch a `coder` subagent (timeout ≥ 10 min, foreground or parallel batches) whose prompt MUST contain:

1. **Paths, not contents**: the target file path (real path for editing) and the mirror paths to read: `.kimi/mirror/bootstrap/references/REFERENCE_STANDARD.md` §3, §5, §6 and one conformant example `.kimi/mirror/pytest-design/references/required/mocking.md`.
2. **The transformation contract**:
   - Exactly one `# Title` H1 at the top (no frontmatter yet — Phase 3 adds it).
   - Group the content into logical `##` sections: one rule/recipe/technique/decision per section. Split oversized mixed sections; merge trivial fragments into their parent topic. Preserve ALL technical content — restructure, do not rewrite; no substance changes, no deletions of meaning.
   - Under every routable section heading place the marker `[ref: #<file-prefix>-<section-slug>]` at column 0, on its own line, with a blank line above and below. kebab-case ids; `<file-prefix>` = filename with underscores → hyphens (one consistent prefix per file); `<section-slug>` = 1–4 words.
   - Markers partition the file cleanly: no nesting, no body text bleeding past the next marker, no markers inside fenced code blocks.
   - Remove any cross-section routing/decision tables (report them instead of deleting if they carry unique content — move that content into the relevant section first).
   - Remove any inline `**Selection criteria / anti-patterns:**`-style blocks (their content is frontmatter material — quote them verbatim in the subagent's report for Phase 3 reuse).
   - Follow `markdown-protocol`: one logical line = one source line, no soft wrapping.
3. **Self-verification commands the subagent MUST run and paste results of**:
   - `rg -c '^\[ref: #' <file>` — marker count;
   - `rg -n '^#\s' <file>` — exactly one H1;
   - `rg -n '^.+\[ref: #' <file>` — zero inline markers (all at column 0);
   - `git diff --stat <file>` plus a manual diff scan proving no technical content was lost.
4. **Report format**: sections created (heading + anchor id per line), markers count, content-preservation confirmation, list of removed routing tables / inline criteria blocks (with verbatim text).

After each subagent returns: verify its claims yourself (spot-check the diff), check the box in the Serena plan memory (`- [ ] P1` → `- [x] P1`), checkpoint, and report to the user before the next file/batch.

---

## Phase 2 — Kagi enrichment (main agent researches, subagents write)

Goal: bring each reference up to current best practices. Skip files the user marks as already exhaustive.

Per file:

1. You (main agent) identify the enrichment questions from the file's content: outdated APIs, missing modern alternatives, version drift, absent best practices.
2. You run the Kagi research (`kagi_search_fetch` / `kagi_extract` / `kagi_fastgpt`, narrow queries, low limits, authoritative domains first). Before fetching any standard, check `read-for-comments/references/` for a local copy.
3. You distill findings into facts (with source URLs) and pass them explicitly in a `coder` subagent prompt — never ask the subagent to "search the web".
4. The subagent integrates the facts into the file's existing sections (or proposes a new section with its own anchor when the material is a distinct technique), respecting the Phase 1 structure: every new example follows the host skill's conventions; every identifier backticked; markdown-protocol line discipline; markers stay valid.
5. If a subagent discovers it needs more web data, it reports the exact query back to you; you run it and resume the subagent with the distilled answer.
6. Verify the diff, check `- [x] P2` in the plan memory, checkpoint, report.

---

## Phase 3 — Validation + draft frontmatter (subagent drafts, main agent validates)

Goal: every file gets a **planned** (draft) frontmatter per the standard §4.

Per file, a `coder` subagent prompt MUST contain:

1. Mirror paths to the standard (§4 in full: `subject`, card six-key schema, firm styles, dedup, convergence) and to 1–2 conformant pytest-design examples.
2. The file path; instruction to read it fully and enumerate every `[ref]` anchor.
3. Draft requirements:
   - `subject`: 30–50 words (≥3-letter tokens), no articles `a`/`the`, `<essence>; <cloud>` form, cloud enumerates EVERY section area, APIs/library names welcome and backticked.
   - One card per anchor minimum; convergence cards (same anchor, distinct criteria paths) where multiple situations select one section.
   - Every card: exactly `{anchor, what, problem, use_when, avoid_when, expected}`; `problem` = declarative situation + stake, 30–50 words, no articles, concept-only trailing cloud (no commands, no library names); `use_when`/`avoid_when` = semicolon-separated criterion clauses with varied openers (never "Load when"/"Use when", never "Do not"/"Never"); `expected` = observable success state; `avoid_when`/`expected` may be empty only for pure lookup sections.
   - Cross-field dedup: no ≥2-word phrase cloned between fields of one card (check singular/plural both ways).
4. The subagent writes the frontmatter at the top of the file (delimited by `---` lines, blank line, then the H1) and reports card count + per-anchor mapping.
5. You validate mechanically before accepting: YAML parses; closed key set; card key sets exact; word bands; article scan; cloud-leak scan (every cloud phrase grepped against the card's other fields); every card anchor ↔ exactly one body marker and vice versa; `subject` covers all section areas. Fix or bounce back to the subagent.
6. Check `- [x] P3`, checkpoint, report.

---

## Phase 4 — Frontmatter polish (whole-corpus pass)

Goal: from "valid draft" to "ideal". Work file by file with the user; this phase is where cross-file consistency is enforced.

1. Re-read all frontmatters of the corpus in one batch (Command 2 of the loader funnel). Check cross-file consistency: prefix conventions, card granularity (no 1-line sections with 5 cards, no 300-line section with 1 thin card), convergence usage, uniform field voice.
2. For each file, launch a `coder` subagent (or do focused edits yourself) to polish: strengthen weak `problem` situations, enrich thin clouds with body-facet hooks (gotchas, anti-patterns, use-case angles — never situation paraphrases), vary openers, sharpen `use_when` into real selection criteria, make `expected` observable.
3. Re-run the full mechanical validation from Phase 3 step 5 on the FINAL text (polished fields can introduce new leaks against the new cloud).
4. End-to-end loader rehearsal: run Command 1 (`rg -N -H '^subject:'`), shortlist 2–3 files against a realistic request, run Command 2, select cards, and extract one section with the bounded `awk` extractor from the standard §7 — prove the funnel works on this corpus.
5. Check `- [x] P4` per file, checkpoint, report.

---

## Phase 5 — Summary and skill wiring

1. Update `{{SKILL_PATH}}/SKILL.md`: replace any static routing tables with the two-command funnel and the semantic context-aware routing rules (standard §7); point to the standard; keep the skill's own mandatory rules.
2. Write the skill's prompts: `{{SKILL_PATH}}/prompts/` gets (a) an addendum documenting skill-specific presentation choices (title style, section terminator convention, tier layout per `{{TIER_NOTE}}`), deferring to the cross-skill standard; (b) if useful, a per-skill card-authoring prompt modeled on `pytest-design/prompts/REFERENCE_CARD_PROMPT.md`.
3. Update `{{SKILL_PATH}}/README.md` (layout, reference overview, loading protocol).
4. Write the summary report memory `reports/{{SKILL}}/reference_standardization`: corpus stats (files, sections, cards, convergence), phase outcomes, deviations from the standard and why, remaining risks.
5. Check the global plan boxes, final `just serena-checkpoint`, and present the summary to the user.

---

## Progress persistence rules (all phases)

- **Strict phase isolation (HARD RULE):** phases run strictly sequentially. A phase processes the ENTIRE reference file list before the next phase starts; never mix phases on any file or batch (e.g. do not enrich a file while another file is still unformatted). The only exception is a file the user explicitly excludes from a phase.
- The Serena plan memory `plans/{{SKILL}}/reference_standardization` is the single source of truth for progress: full file list × full phase checkbox list, updated immediately after every file completes a phase.
- Use the session todo list (`SetTodoList`) for the current phase's active batch only; never let it replace the Serena plan.
- If the session breaks, the next session resumes by reading the plan memory and continuing from the first unchecked box — no re-inventory.
