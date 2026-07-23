---
subject: "Lazy-load authoring extension; runtime skill-work activation gate, reference file frontmatter schema, `subject` coarse router style, `index` decision cards, six card keys, `problem` firm style, keyword cloud, cross-field dedup, convergence anchors, body skeleton, anchor markers, addenda extras, migration workflow, conformance checklist."
index:
  - anchor: lazyload-runtime-activation
    what: "The runtime gate obliging the agent to load this extension the moment session work turns toward skills — editing `SKILL.md` files, touching `references/**` corpora, or writing skill frontmatter."
    problem: "Session boots with core alone; hours later agent rewrites skill cards, migrates corpus frontmatter, invents fields — standard never loaded, drift compounds silently; late discovery, unguarded session, boot-only mindset, schema erosion, duplicate gates, stale assumptions, maintenance fallout."
    use_when: "Conversation shifts to creating or modifying any skill asset; user asks for corpus migration, card authoring, validator runs; agent plans edits under any skill directory."
    avoid_when: "Pure reading of a conformant corpus through core §7 mechanics; evaluating `SKILL.md` headers — the include extension owns that gate."
    expected: "Every skill-touching edit happens under the loaded standard; corpus stays conformant and validator-clean."
  - anchor: lazyload-scope-addenda
    what: "Scope rules: this standard governs card format and authoring rules; a skill MAY publish an addendum for domain presentation and declare extra top-level keys."
    problem: "Skills need domain flavors — terminators, tiers, metadata like AIP lists; hardcoding them into shared standard bloats it, copying standard per skill forks it; fork risk, addendum channel, declared extras, presentation choices, taxonomy tiers, metadata fields."
    use_when: "Writing a skill addendum; declaring an extra key like `aips`; checking whether a customization is legal."
    avoid_when: "Contradicting core card semantics — addenda cover presentation only and MUST defer here."
    expected: "Domain variation lives in addenda and documented extras; the shared standard stays topic-agnostic."
  - anchor: lazyload-file-layout
    what: "Layout contract: one topic per `<topic>.md` file (lowercase, underscores); the filename slug converted to hyphens becomes the default anchor prefix."
    problem: "Corpus grows organically — mega-files mixing five topics, cryptic names, prefixes shifting per section; anchors stop being guessable and files resist splitting; prefix drift, naming contract, coherent topics, file granularity, stable prefixes, underscored filenames."
    use_when: "Creating or splitting reference files; choosing anchor prefixes; auditing corpus layout."
    avoid_when: "Anchor id authoring itself — the id format has its own section under Anchors."
    expected: "Files stay focused per topic; prefixes remain stable and predictable across the corpus."
  - anchor: lazyload-frontmatter-schema
    what: "Allowed top-level fields: required `subject` and `index`, optional `libraries`, plus skill-declared extras; `subject` is the 30–50-word coarse router welcoming API names."
    problem: "File-level routing needs one line telling agents everything one file covers; vague or cloudless subjects force body reads, killing funnel; funnel breakage, coarse selection, field whitelist, legacy keys, api cloud, word band."
    use_when: "Writing a file's `subject`; choosing top-level keys; migrating legacy `triggers`/`description`/`decisions` blocks."
    avoid_when: "Card-level routing — per-section selection belongs to `index` cards, not the subject line."
    expected: "One subject line routes the whole file; the key whitelist rejects strays."
  - anchor: lazyload-cards
    what: "The `index` card: exactly six keys `{anchor, what, problem, use_when, avoid_when, expected}` forming one self-contained load-or-skip decision for one section."
    problem: "Card missing keys or carrying vague prose cannot gate anything; agent still opens body to decide, and selection criteria leak back into content; incomplete cards, decision units, key discipline, self-contained selection, gate quality, reader autonomy."
    use_when: "Authoring or reviewing any card; deciding load-or-skip from frontmatter alone."
    avoid_when: "Pure lookup sections — `avoid_when`/`expected` MAY stay empty there by convention."
    expected: "Each card alone decides load-or-skip and names the observable result."
  - anchor: lazyload-problem-style
    what: "Firm style for `problem`: declarative agent situation plus stake, 30–50 words, no articles, concept-only trailing keyword cloud, no solution or success leakage."
    problem: "Cards written as capabilities or goals ('Assert on…', 'Avoid…') give agents nothing to recognize; without concept clouds, semantic routing starves; capability phrasing, goal phrasing, recognition failure, article pollution, solution leakage, cloud discipline, word band."
    use_when: "Drafting the `problem` field; reviewing cards for style conformance; enriching thin clouds with concept hooks."
    avoid_when: "Naming APIs or libraries in the cloud — those belong in `subject` and `what` by design."
    expected: "Every problem reads as recognizable situation with stake and a clean concept cloud."
  - anchor: lazyload-dedup
    what: "Cross-field dedup and convergence: no ≥2-word prose phrase clones between a card's fields (backticked identifiers exempt); several cards MAY share one anchor with distinct selection routes."
    problem: "Fields copy phrases from each other and from cloud, collapsing five answers into one mush; or one section gets five cloned cards instead of convergent criteria; phrase cloning, identifier exemption, criteria paths, dedup discipline, singular plural, load once."
    use_when: "Polishing cards before save; scripting dedup checks; expressing multiple situations that select one section."
    avoid_when: "Scrubbing backticked identifiers — mechanism naming across fields is protected by design."
    expected: "Fields partition information cleanly; convergent cards load their shared section once."
  - anchor: lazyload-body-skeleton
    what: "Body skeleton: exactly one H1 after the frontmatter, routable `##` sections aligned 1:1 with anchors, pure HOW content, no cross-section routing tables."
    problem: "Body re-implements routing with decision tables and inline criteria blocks, duplicating frontmatter's job and drifting out of sync; duplicate routing, drift risk, skeleton discipline, content purity, section alignment, single title, sync loss."
    use_when: "Formatting or reformatting reference bodies; adding sections to a conformant file."
    avoid_when: "Intra-section lookup tables — content tables inside one section are allowed."
    expected: "Bodies hold only HOW content; every routable section maps to exactly one marker."
  - anchor: lazyload-anchors
    what: "Anchor mechanics: kebab-case `<file-prefix>-<section-slug>` ids on `[ref: #...]` marker lines partitioning the body; placement style is markdown-protocol's `marker_style` (default tight)."
    problem: "Anchors drift from filenames, markers nest or bleed, ids break kebab discipline; extraction tools miss boundaries and load halves of two sections; partition rules, slug format, marker placement, load spans, fenced code, unique markers."
    use_when: "Placing markers; choosing ids; building extraction tooling over a corpus."
    avoid_when: "Inline heading markers — legacy form that MUST NOT be introduced in new corpora."
    expected: "Markers partition the file cleanly; every card anchor matches exactly one body marker."
  - anchor: lazyload-authoring
    what: "Authoring and migration workflow: file-by-file from an approved todo list; frontmatter-only edits on existing bodies; re-validate final text after every polish."
    problem: "Bulk rewrites silently mangle bodies, markers detach from headings, and polished fields introduce fresh dedup leaks against new cloud; silent mangling, approval gates, byte-identical bodies, re-validation, file-by-file, user sign-off, content loss."
    use_when: "Migrating a corpus to this standard; editing frontmatter on existing bodies; running polish passes."
    avoid_when: "Silent body fixes for anchor mismatches — surface them to the user instead."
    expected: "Bodies stay byte-identical during frontmatter work; final text passes the full checklist."
  - anchor: lazyload-conformance
    what: "Conformance checklist and forbidden patterns, mechanically enforced by `frontmatter-protocol/scripts/validate_frontmatter.py`."
    problem: "Hand-checking cards one by one misses word bands, article leaks, cloud clones, and anchor mismatches at corpus scale; manual review, scale failure, mechanical enforcement, checklist drift, validator profiles, exit codes, silent regressions."
    use_when: "Validating a file before calling it done; wiring checks into workflows; reviewing conformance failures."
    avoid_when: "Serena memory or skill headers — those validate under tracking and include profiles, not this one."
    expected: "Every corpus file passes the scripted checklist; failures block completion."
---

# Reference: lazyload — Reference File & Card Routing Standard (frontmatter-protocol extension)

Extension of `frontmatter-protocol` (core §9): activated implicitly by `subject` and/or `index` in a frontmatter; loaded when AUTHORING or VALIDATING a reference corpus — and, at runtime, the moment any session work touches skills or their `references/**` corpora in a writing capacity (see Runtime Activation).
Reading a conformant corpus needs only the loader mechanics in the core (§7) — this file is the authoring standard.
A strict, normative specification for every reference file that uses `[ref: #<anchor>]` lazy-load routing, and for the YAML frontmatter that routes to those anchors.
It applies to any `references/**/*.md` corpus in any skill and is topic-agnostic: it defines the **card format and the authoring rules**, not any domain.
The envelope (delimiters, extraction primitive, key closure) and the loader contract (funnel, routing rules, bounded extraction) live in the protocol core and are not repeated here.

**Design lineage.** This standard is the progressive-disclosure pattern (Nielsen Norman Group; named by Anthropic Engineering as the core philosophy of agent context management) applied to reference corpora: `subject` is the coarse disclosure layer, `index` cards the decision layer, and body sections the on-demand deep layer — nothing enters the agent's context before it is selected.

Normative keywords (`MUST`, `SHOULD`, `MAY`) follow RFC 2119 / RFC 8174 (by `read-for-comments` skill).

## Runtime Activation

[ref: #lazyload-runtime-activation]

- This extension is lazy by default, but one trigger is unconditional once recognized: **the moment session work turns toward skills in a writing capacity**, the agent MUST route this file's frontmatter and load the needed sections BEFORE the first edit — regardless of what was loaded at bootstrap.
- Covered situations: creating or editing a `SKILL.md` body or anything under its `references/**`; writing, migrating, or polishing reference-card frontmatter; running or wiring the validator; building tooling that reads or writes corpus files.
- Not covered: pure consumption of a conformant corpus (core §7 suffices) and `SKILL.md` header evaluation (owned by the include extension).
- The trigger is semantic and mid-session: after every user message, if the conversation has reached skill work and this extension is not yet loaded, load it now.

## Scope and Skill Addenda

[ref: #lazyload-scope-addenda]

- This standard governs: frontmatter schema and style, card semantics, anchor mechanics, body skeleton, and conformance checking. The loader contract lives in the protocol core (§7) and is not repeated here.
- A skill MAY publish an **addendum** (e.g. `api-design/prompts/REFERENCE_STANDARD_ADDENDUM.md`) covering domain-specific presentation: section terminator conventions, code-example style, title style, taxonomy tiers. An addendum MUST defer to this document for everything covered here and MUST NOT contradict it.
- A skill MAY declare **additional optional top-level frontmatter keys** (e.g. an `aips` list for a standards corpus). Every additional key MUST be declared and documented in that skill's `SKILL.md` (core §9 skill-declared extras); the required core keys below stay unchanged.

## File Layout and Naming

[ref: #lazyload-file-layout]

- One topic area per file. Filename = `<topic>.md`, lowercase, words separated by underscores (`time_control.md`, `database_mocking.md`).
- The filename slug (underscores → hyphens) is the default **anchor prefix**. A semantic shortening MAY be used when it reads better (`warning_testing.md` → `warnings-…`); once chosen, it MUST be used consistently for every anchor in the file.
- A file decomposes its topic into **sections** (one rule, one recipe, one technique, or one decision per section). Each routable section is addressed by one or more frontmatter cards.
- Keep a file focused; split when a topic grows past one coherent area. A body under roughly 500 lines is a healthy target, not a hard cap.
- A skill MAY split its corpus into tiers (e.g. `references/required/` and `references/optional/`); the tier convention belongs to the skill's addendum, and tier markers MUST NOT leak into frontmatter text.

## Frontmatter Schema

[ref: #lazyload-frontmatter-schema]

The envelope follows the protocol core (§3–§6 there). Allowed top-level fields (closed set):

```yaml
---
subject: "..."
index:
  - anchor: ...
    what: "..."
    problem: "..."
    use_when: "..."
    avoid_when: "..."
    expected: "..."
libraries:
  - package-name
---
```

- `subject` — **required**, string.
- `index` — **required**, a flat list of decision cards.
- `libraries` — **optional**, flat list of related packages/plugins (omit for corpora with no code dependencies).
- Skill-declared extras — **optional**, only as documented in the owning skill's `SKILL.md`.

**Forbidden** top-level keys: `triggers`, `description`, `decisions` — legacy forms consolidated into `index`. A file carrying any of them is non-conformant.

### `subject`

`subject` is the **file-level coarse router**: the agent reads only this line to decide whether the whole file is relevant. It MUST name the topic **and** enumerate every section area with the concrete APIs/techniques/concepts, so semantic routing hits without opening the body.

**Firm style (binding):**

- **Form:** one double-quoted sentence shaped as `<short essence of the file topic>; <comma-separated keyword/API cloud of every section area>`.
- **Length:** 30–50 words, counting only tokens of **≥3 letters** (short function words are free). Pad the **cloud**, never the essence.
- **No articles:** the tokens `a` and `the` MUST NOT appear. Keep them only inside backticked code.
- **No tier marker:** never write `CORE` / `EXTENDED` / tier names in `subject`; the tier is the directory.
- **Identifiers in backticks:** every API, flag, value, and version is inline-coded.
- **APIs and library names are WELCOME in the `subject` cloud** — naming them is the point of coarse routing. (Opposite of the `problem` cloud, where they are forbidden.)

### `libraries`

- Optional flat list of related packages/plugins, lowercase canonical install names.
- Keep **significant version pins** where behavior depends on them (`pytest-asyncio>=0.23`).
- Preserve **extras** when a recipe needs them (`testcontainers[postgresql]`).
- Omit the field entirely when the corpus needs no external packages.

## Index Cards

[ref: #lazyload-cards]

`index` is a **flat list** of self-contained decision cards — the single catalog of the file. List order SHOULD mirror body section order. **Each card is a self-contained decision-making system** and the selection gate for ONE section. Any number of cards MAY share one `anchor` (see Dedup & Convergence). Routing against cards is semantic and context-aware (never substring): write each card so semantic matching works — concept, recognizable problem, crisp positive/negative applicability.

A card is a mapping with **exactly** these six keys (closed set):

| Key | Required | Content |
|---|---|---|
| `anchor` | yes | The body-section id this card routes to. |
| `what` | yes | WHAT the entity under the anchor IS, framed **as applied to solving the task in `problem`** — not a detached generic definition. |
| `problem` | yes | The agent's decision-time problem this card recognizes — situation + stake, NOT the section's abstract purpose. |
| `use_when` | yes | A **list of clear, precise criteria** for when this section MUST be loaded and used. |
| `avoid_when` | yes* | A **list of clear, precise criteria** for when this section MUST NOT be used. |
| `expected` | yes* | The **attainability criterion**: what holds after applying the section — the observable sign that `problem` is solved. |

\* `avoid_when` and `expected` SHOULD be filled. They MAY be empty only for a pure lookup entry (glossary, verb table) that has no anti-pattern and no success state.

Authoring rules for each field:

- The whole card is one decision unit. A reader of **only** the card MUST be able to decide load-or-skip and to know the expected result — without the body.
- **One sentence each**, double-quoted, specific, self-contained. `use_when` and `avoid_when` read as **lists of crisp criteria** separated by semicolons, not vague prose.
- Use backticks for every identifier, API, flag, and value.
- `what` names the concrete mechanism **in terms of the problem it solves here**.
- `use_when` is a positive criteria list. Include version gates and concrete scenarios. **`use_when` MUST NOT open with uniform lead-ins like "Load when" / "Use when"** — the field name already implies it; openers vary across cards.
- `avoid_when` is a negative criteria list naming the canonical wrong situations, pointing to a better alternative where possible. **`avoid_when` MUST NOT open with "Do not" / "Don't" / "Never"** — phrase each item as a direct criterion clause.
- **`use_when` MUST NOT restate or paraphrase `problem`.** It is the section's **selection criterion** ("pick this section when …"), not a rewording of the situation.
- `avoid_when` MUST NOT merely negate `problem` either; it names the boundary where the section is inapplicable or harmful.
- All fields may reference the same nouns, but each field MUST add distinct semantic value.

Canonical card template:

```yaml
  - anchor: <file-prefix>-<section-slug>
    what: "<The entity under the anchor, concisely, framed as applied to `problem`.>"
    problem: "<Situation + stake the agent recognizes; <keyword cloud>.>"
    use_when: "<Criterion clause; criterion clause; criterion clause.>"
    avoid_when: "<Criterion clause; criterion clause.>"
    expected: "<Observable success state after applying the section.>"
```

## Firm Style for `problem`

[ref: #lazyload-problem-style]

- **Role:** `problem` lets the agent recognize *"this is exactly my situation right now."* Write a declarative **agent situation + concrete stake** (what breaks, flakes, leaks, or costs), not what the section can do.
- **Form:** one double-quoted sentence shaped as `"<concrete situation>; <naïve path> → <what breaks / flakes / costs>; <keyword cloud>"`. After the situation add `; ` and a comma-separated **keyword cloud** of concepts, synonyms, and triggers to strengthen semantic routing.
- **Length:** 30–50 words, counting only tokens of **≥3 letters**. Reach the floor by enriching the **cloud** and situation detail — never filler.
- **No articles:** `a` and `the` MUST NOT appear anywhere in `problem`. Keep them only inside backticked code.
- **No solution leakage:** do not name the answer API/technique (→ `what`); do not state the success outcome (→ `expected`).
- **Cloud discipline:** concepts, synonyms, triggers only — NO commands and NO library/tool names (those belong in `subject` and `what`). Every cloud token MUST be a distinct routing hook: synonym re-wordings collapse to one token, and the cloud MUST NOT paraphrase the card's own situation sentence.
- **Banned openers:** `"Assert on …"`, `"Verify …"`, `"Exercise …"`, `"Avoid …"`, `"Keep …"`, `"Provide …"` — rewrite as neutral situation + stake.
- **Identifiers in backticks** whenever an identifier is unavoidable in the situation.

## Dedup & Convergence

[ref: #lazyload-dedup]

**Cross-field dedup (binding):**

- The keyword cloud appears **exactly once per card** — at the tail of `problem`. `what` / `use_when` / `avoid_when` / `expected` carry no trailing clouds.
- Information is partitioned across fields: mechanism+API → `what`; situation+stake+cloud → `problem`; positive criteria → `use_when`; anti-criteria → `avoid_when`; observable outcome → `expected`. **No verbatim phrase (≥2 words) may be cloned between fields of one card** — watch singular/plural inflection (`X` ⊂ `Xs`), the most common leak shape; grep both forms of every cloud phrase against all four other fields.
- No library/tool names in the `problem` cloud — including names not listed in `libraries` (the mechanical check only covers listed ones; editorial attention covers the rest).
- **Identifier exemption:** the clone ban targets *prose phrases*. A backticked identifier MAY repeat across fields of one card — naming the mechanism is each field's job, and scrubbing identifiers from `expected`/`use_when` destroys semantic routing. The exemption covers the identifier token itself plus its immediate generic shadow noun (`comment`, `field`, `operation`); it does NOT cover surrounding prose, which MUST still be deduplicated.

**Convergence:**

Several cards MAY share the **same** `anchor`. This expresses **converging selection criteria** pointing to one section. The loader deduplicates anchors and loads the shared section once. Convergence cards MUST state distinct criteria paths, not cloned text. Do **not** create a separate mechanism for convergence.

## Body Skeleton

[ref: #lazyload-body-skeleton]

After the frontmatter:

```
# <TITLE>

<optional one-line intro>

## <Section Heading>
[ref: #<anchor>]

<section HOW>

## <Section Heading>
[ref: #<anchor>]

<section HOW>
...
```

- Exactly **one** H1 per file, immediately after the frontmatter (H1 typography itself is markdown-protocol's domain).
- A single short intro line MAY sit between H1 and the first `##` (how to activate the file). Never restate selection criteria there.
- Each routable section is a `##` (or a deliberately routable `###`) heading, short noun-phrase style, inline code for APIs. The set of routable headings SHOULD align 1:1 with the distinct anchors declared in `index` (modulo convergence).
- Section content is pure HOW: lead prose (imperative, present tense), then code/tables, each fence introduced by a lead sentence ending in a colon. Contrast pairs use labeled blocks (`Bad — <reason>:` / `Good — <reason>:`).
- Selection criteria and anti-patterns MUST NOT appear as an inline `**Selection criteria / anti-patterns:**` block — that gate already lives in the frontmatter card. Body `## Anti-patterns` / `## Common Errors` sections are ordinary sections with their own anchor and card.
- **Tables:** intra-section content tables are allowed; cross-section routing/decision tables are forbidden.
- **Code blocks:** fenced with a language tag, self-contained and realistic. Domain code style is defined by the host skill's addendum.
- A skill MAY define a per-section terminator convention in its addendum.

## Anchors

[ref: #lazyload-anchors]

**Placement.** The marker is the literal line `[ref: #<anchor>]`, at **column 0**, on its **own line** directly under the section heading. Visual placement style (blank lines around the marker) is governed by markdown-protocol's `marker_style` rule: `separate | tight`, default **tight** — marker directly under the heading, one blank line below. A skill MUST choose one form and apply it uniformly, declaring non-default choices in its addendum. Inline heading markers (`## Heading [ref: #x]`) are a legacy variant that MUST NOT be introduced.

Parsers MUST skip fenced code blocks when scanning headings or markers.

**Id format.**

- `<file-prefix>-<section-slug>`, **kebab-case**, lowercase.
  - `<file-prefix>` = filename with underscores → hyphens, or its chosen semantic shortening.
  - `<section-slug>` = 1–4 words, often embedding the API/concept name.
- The card's `anchor` value MUST equal the body's marker exactly, minus the `#`: frontmatter `anchor: data-assertions-pytest-approx` ↔ body `[ref: #data-assertions-pytest-approx]`.

**Load boundary.** A section body runs from its marker to the **next** `[ref: #...]` marker or end of file (the reader-facing extraction mechanics live in core §7). Markers MUST partition the file cleanly: every routable unit has exactly one marker; markers never nest; no body text bleeds past the next marker.

## Authoring & Migration Workflow

[ref: #lazyload-authoring]

1. Work file by file from an explicit todo list; each file requires user approval before work starts.
2. Read the whole file → audit → write/rewrite frontmatter → verify (conformance checklist, preferably scripted) → mark done.
3. When adding frontmatter to an existing body: edit ONLY the frontmatter (plus adding the single H1 if absent); body sections and `[ref]` markers stay byte-identical. Surface anchor↔marker mismatches to the user instead of silently fixing the body.
4. When enriching a body: keep every `[ref]` marker attached to its heading; never introduce cross-section routing tables; never re-introduce inline criteria blocks.
5. After any frontmatter edit, re-run the conformance check on the FINAL text of all fields — rewritten fields can introduce new dedup leaks against the new cloud.

The full six-phase orchestration prompt lives at `frontmatter-protocol/prompts/REFERENCE_MIGRATION_PROMPT.md`.

## Conformance

[ref: #lazyload-conformance]

The reference validator is `frontmatter-protocol/scripts/validate_frontmatter.py` — this copy is the ONLY canonical reference (local ports were retired 2026-07-23). Run it per file or per directory from the workspace root:

```bash
uv run --no-project --with pyyaml python frontmatter-protocol/scripts/validate_frontmatter.py [--allow-extra KEY]... <FILE.md | DIR>...
```

`--aips` enables the api-design AIP cross-check. The include and tracking profiles are planned growth (backlog F17); today only the lazyload profile is enforced mechanically. The operational authoring companion is `frontmatter-protocol/prompts/CARD_AUTHORING.md`. Run from the skill directory when validating a whole corpus. For each `references/**/*.md`:

1. Envelope per the protocol core; top-level keys ⊆ `{subject, index, libraries}` plus skill-declared extras.
2. `subject` present, double-quoted, one sentence: `<essence>; <cloud>`, 30–50 words (≥3-letter tokens), no `a`/`the`, no tier marker, identifiers backticked; covers every section area of the file.
3. Every `index` item has exactly the keys `{anchor, what, problem, use_when, avoid_when, expected}`; each a non-empty (except the two optional) double-quoted sentence.
4. Every `problem` follows the firm style: declarative situation + stake, no banned opener, no solution-API, no success language, 30–50 words, no `a`/`the`, concept-only cloud with no commands or library names.
5. `use_when` does not open with "Load when"/"Use when"; `avoid_when` does not open with "Do not"/"Don't"/"Never"; openers vary across cards; neither field restates `problem`.
6. Cross-field dedup: no ≥2-word cloud phrase appears verbatim in the card's other fields (check singular/plural both ways); cloud tokens are pairwise distinct; no ≥2-word *prose* phrase is cloned between any two fields of one card, with backticked identifiers exempt.
7. For every card `anchor`, a body line `[ref: #<anchor>]` exists exactly once; for every body marker, a declaring card exists.
8. Anchors kebab-case `<file-prefix>-<section-slug>`; consistent prefix within the file; one placement form throughout the skill (markdown-protocol `marker_style`).
9. Exactly one `#` H1; routable sections are `##` (or deliberately routable `###`); markers partition the file with no nesting (scan outside fenced code).
10. No inline `**Selection criteria / anti-patterns:**` blocks; no cross-section routing/decision tables in bodies.
11. `libraries` (if present): lowercase canonical names, extras preserved, significant pins kept.
12. Convergence cards on one anchor state distinct criteria paths (no cloned text).

**Forbidden patterns (conformance breakers):** any top-level key outside the closed set (+ extras); any legacy key (`triggers`/`description`/`decisions`); added/removed/renamed card keys; inline criteria blocks in bodies; anchor/marker mismatches; nested markers or bleeding bodies; cross-section routing tables; mixed placement forms or inline heading markers; vague/cloudless/tier-marked/article-bearing subjects outside the word band; `problem` as capability/goal/imperative or with leaked solution/success/articles/commands; `use_when`/`avoid_when` restating `problem` or opening with banned lead-ins.
