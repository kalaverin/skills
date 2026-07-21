# Cross-Skill Reference File & Frontmatter Standard

A strict, normative specification for every skill reference file that uses `[ref: #<anchor>]` lazy-load routing, and for the YAML frontmatter that routes to those anchors. It applies to any `references/**/*.md` corpus in any skill (current conformant implementations: `pytest-design/references/`, `api-design/references/`). It is topic-agnostic: it defines the **card format and the loader contract**, not any domain.

Normative keywords (`MUST`, `SHOULD`, `MAY`) follow RFC 2119 / RFC 8174 (by `read-for-comments` skill).

---

## 1. Purpose and Mental Model

A reference file is a **lazy-loaded recipe/rule file**. It is read in two stages:

1. **Routing (frontmatter only).** The agent extracts YAML frontmatter without opening bodies and decides, purely from that frontmatter, **which sections** it needs. It never reads a whole file to decide relevance.
2. **Loading (anchor sections only).** The agent loads only the body sections marked by the selected anchors, reading each from its `[ref: #<anchor>]` marker to the next marker.

Two consequences shape the entire format:

- The frontmatter is the **selection layer**. Its sole job is to let the agent decide **which section(s) to load**. Each card is the selection gate for ONE section: `use_when` states when that section is needed and `avoid_when` states when it must NOT be applied.
- The body is the **content layer**: pure HOW/WHAT for the section that was already selected. A section is self-contained and MAY carry rich content — prose, code, and tables that are that section's own reference material.
- The one forbidden body pattern is a **cross-section decision/routing table**: a table whose job is to select among sections or techniques. That selection is the frontmatter's function; duplicating it in the body is non-conformant.

Routing is **semantic and context-aware**, never substring/keyword. The matching input is the user's request **plus** the session work the agent infers (the artifact it is about to produce, the questions the problem implies). Cards MUST be written so semantic matching works: each card states the concept, the problem it solves, and crisp positive/negative applicability.

---

## 2. Scope and Skill-Specific Addenda

- This standard governs: frontmatter schema and style, card semantics, anchor mechanics, body skeleton, loader protocol, and conformance checking.
- A skill MAY publish an **addendum** (e.g. `pytest-design/prompts/REFERENCE_STANDARD.md`) covering domain-specific presentation: section terminator conventions, code-example style, title style, taxonomy tiers. An addendum MUST defer to this document for everything covered here and MUST NOT contradict it.
- A skill MAY declare **additional optional top-level frontmatter keys** (e.g. an `aips` list for a standards corpus). Every additional key MUST be declared and documented in that skill's `SKILL.md`; the required core keys below stay unchanged.

---

## 3. File Layout and Naming

- One topic area per file. Filename = `<topic>.md`, lowercase, words separated by underscores (`time_control.md`, `database_mocking.md`).
- The filename slug (underscores → hyphens) is the default **anchor prefix** (§6.2). A semantic shortening MAY be used when it reads better (`warning_testing.md` → `warnings-…`); once chosen, it MUST be used consistently for every anchor in the file.
- A file decomposes its topic into **sections** (one rule, one recipe, one technique, or one decision per section). Each routable section is addressed by one or more frontmatter cards.
- Keep a file focused; split when a topic grows past one coherent area. A body under roughly 500 lines is a healthy target, not a hard cap.
- A skill MAY split its corpus into tiers (e.g. `references/required/` and `references/optional/`); the tier convention belongs to the skill's addendum, and tier markers MUST NOT leak into frontmatter text.

---

## 4. Frontmatter Contract (Normative)

The frontmatter is the **first** thing in the file, delimited by a line `---`, the YAML block, and a closing line `---`. It is followed by a blank line and then the `# Title`.

### 4.1 Allowed top-level fields (closed set)

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
- Skill-declared extras — **optional**, only as documented in the owning skill's `SKILL.md` (§2).

**Forbidden** top-level keys: `triggers`, `description`, `decisions` — legacy forms consolidated into `index`. A file carrying any of them is non-conformant.

### 4.2 `subject`

`subject` is the **file-level coarse router**: the agent reads only this line to decide whether the whole file is relevant. It MUST name the topic **and** enumerate every section area with the concrete APIs/techniques/concepts, so semantic routing hits without opening the body.

**Firm style (binding):**

- **Form:** one double-quoted sentence shaped as `<short essence of the file topic>; <comma-separated keyword/API cloud of every section area>`.
- **Length:** 30–50 words, counting only tokens of **≥3 letters** (short function words are free). Pad the **cloud**, never the essence.
- **No articles:** the tokens `a` and `the` MUST NOT appear. Keep them only inside backticked code.
- **No tier marker:** never write `CORE` / `EXTENDED` / tier names in `subject`; the tier is the directory.
- **Identifiers in backticks:** every API, flag, value, and version is inline-coded.
- **APIs and library names are WELCOME in the `subject` cloud** — naming them is the point of coarse routing. (Opposite of the `problem` cloud, §4.4, where they are forbidden.)

Bad — and why: `"Core recipes for fixtures."` — vague essence, **no section-area cloud**, far under 30 words; an agent cannot route from it.

### 4.3 `index` — the card list

`index` is a **flat list** of self-contained decision cards — the single catalog of the file. List order SHOULD mirror body section order. **Each card is a self-contained decision-making system** and the selection gate for ONE section. Any number of cards MAY share one `anchor` (§4.6).

A card is a mapping with **exactly** these six keys (closed set):

| Key | Required | Content |
|---|---|---|
| `anchor` | yes | The body-section id this card routes to (§6.2). |
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
- `problem` follows the firm style in §4.4. It is never a capability ("Assert on …"), never a goal/imperative ("Avoid …", "Keep …"), never the solution API (→ `what`), and never the success state (→ `expected`).
- `use_when` is a positive criteria list. Include version gates and concrete scenarios. **`use_when` MUST NOT open with uniform lead-ins like "Load when" / "Use when"** — the field name already implies it; openers vary across cards.
- `avoid_when` is a negative criteria list naming the canonical wrong situations, pointing to a better alternative where possible. **`avoid_when` MUST NOT open with "Do not" / "Don't" / "Never"** — phrase each item as a direct criterion clause.
- **`use_when` MUST NOT restate or paraphrase `problem`.** It is the section's **selection criterion** ("pick this section when …"), not a rewording of the situation. If removing `problem` makes `use_when` lose meaning, the gate is a restatement and MUST be rewritten from the reader's decision perspective.
- `avoid_when` MUST NOT merely negate `problem` either; it names the boundary where the section is inapplicable or harmful.
- All fields may reference the same nouns, but each field MUST add distinct semantic value.

### 4.4 Firm style for `problem` (binding)

- **Role:** `problem` lets the agent recognize *"this is exactly my situation right now."* Write a declarative **agent situation + concrete stake** (what breaks, flakes, leaks, or costs), not what the section can do.
- **Form:** one double-quoted sentence shaped as `"<concrete situation>; <naïve path> → <what breaks / flakes / costs>; <keyword cloud>"`. After the situation add `; ` and a comma-separated **keyword cloud** of concepts, synonyms, and triggers to strengthen semantic routing.
- **Length:** 30–50 words, counting only tokens of **≥3 letters**. Reach the floor by enriching the **cloud** and situation detail — never filler.
- **No articles:** `a` and `the` MUST NOT appear anywhere in `problem`. Keep them only inside backticked code.
- **No solution leakage:** do not name the answer API/technique (→ `what`); do not state the success outcome (→ `expected`).
- **Cloud discipline:** concepts, synonyms, triggers only — NO commands and NO library/tool names (those belong in `subject` and `what`). Every cloud token MUST be a distinct routing hook: synonym re-wordings collapse to one token, and the cloud MUST NOT paraphrase the card's own situation sentence.
- **Banned openers:** `"Assert on …"`, `"Verify …"`, `"Exercise …"`, `"Avoid …"`, `"Keep …"`, `"Provide …"` — rewrite as neutral situation + stake.
- **Identifiers in backticks** whenever an identifier is unavoidable in the situation.

Good (32 words, no articles, concept-only cloud):

- `"Computed numeric result drifts from exact value under floating-point rounding and exact-equality assertion flakes across runs; tolerance, relative delta, absolute delta, rounding noise, decimal drift, representation error, recursive compare, near-equal, collection compare, computed value."`

Bad — and the rule each breaks:

- `"Assert on float results within tolerance."` — **capability** opener, no situation, no cloud, 5 words.
- `"Avoid flaky float assertions in tests."` — **goal/imperative** opener, no situation, 5 words.
- `"Use \`pytest.approx\` to compare floats so that assertions stay green."` — **leaks the solution API** (→ `what`) **and the success state** (→ `expected`).
- `"A test needs the faker value to stay unique; faker, unique, the registry."` — **articles** (`a`, `the`) **and a library name** (`faker`) inside the cloud.

### 4.5 Cross-field dedup (binding)

- The keyword cloud appears **exactly once per card** — at the tail of `problem`. `what` / `use_when` / `avoid_when` / `expected` carry no trailing clouds.
- Information is partitioned across fields: mechanism+API → `what`; situation+stake+cloud → `problem`; positive criteria → `use_when`; anti-criteria → `avoid_when`; observable outcome → `expected`. **No verbatim phrase (≥2 words) may be cloned between fields of one card** — watch singular/plural inflection (`X` ⊂ `Xs`), the most common leak shape; grep both forms of every cloud phrase against all four other fields.
- No library/tool names in the `problem` cloud — including names not listed in `libraries` (the mechanical check only covers listed ones; editorial attention covers the rest).

### 4.6 Anchors are not unique (convergence)

Several cards MAY share the **same** `anchor`. This expresses **converging selection criteria** pointing to one section. The loader deduplicates anchors and loads the shared section once. Convergence cards MUST state distinct criteria paths, not cloned text. Do **not** create a separate mechanism for convergence.

### 4.7 `libraries`

- Optional flat list of related packages/plugins, lowercase canonical install names.
- Keep **significant version pins** where behavior depends on them (`pytest-asyncio>=0.23`).
- Preserve **extras** when a recipe needs them (`testcontainers[postgresql]`).
- Omit the field entirely when the corpus needs no external packages.

### 4.8 Canonical frontmatter template

```yaml
---
subject: "<One sentence naming the topic and enumerating its section areas; cloud.>"
index:
  - anchor: <file-prefix>-<section-slug>
    what: "<The entity under the anchor, concisely, framed as applied to `problem`.>"
    problem: "<Situation + stake the agent recognizes; <keyword cloud>.>"
    use_when: "<Criterion clause; criterion clause; criterion clause.>"
    avoid_when: "<Criterion clause; criterion clause.>"
    expected: "<Observable success state after applying the section.>"
  - anchor: <file-prefix>-<section-slug>      # MAY repeat a prior anchor (convergence)
    what: "..."
    problem: "..."
    use_when: "..."
    avoid_when: "..."
    expected: "..."
libraries:                                     # optional; omit if none
  - package-name
  - pinned-package>=X.Y
  - package[extra]
---
```

---

## 5. Body Skeleton

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

- Exactly **one** H1 per file, immediately after the frontmatter. Title style (ALL-CAPS vs Title Case, tier suffixes) is a per-skill choice, consistent within the skill.
- A single short intro line MAY sit between H1 and the first `##` (how to activate the file). Never restate selection criteria there.
- Each routable section is a `##` (or a deliberately routable `###`) heading, short noun-phrase style, inline code for APIs. The set of routable headings SHOULD align 1:1 with the distinct anchors declared in `index` (modulo convergence).
- Section content is pure HOW: lead prose (imperative, present tense), then code/tables, each fence introduced by a lead sentence ending in a colon. Contrast pairs use labeled blocks (`Bad — <reason>:` / `Good — <reason>:`).
- Selection criteria and anti-patterns MUST NOT appear as an inline `**Selection criteria / anti-patterns:**` block — that gate already lives in the frontmatter card. Body `## Anti-patterns` / `## Common Errors` sections are ordinary sections with their own anchor and card; their tables are their own content.
- **Tables:** intra-section content tables (lookups, `| Symptom | Cause | Fix |`, `| Anti-pattern | Correct approach |`) are allowed; cross-section routing/decision tables are forbidden (§1).
- **Code blocks:** fenced with a language tag, self-contained and realistic (imports, types, minimal context shown). Domain code style is defined by the host skill's addendum.
- A skill MAY define a per-section terminator convention (e.g. pytest-design's "Variety booster") in its addendum.

---

## 6. Anchors

### 6.1 Placement

- The marker is the literal line `[ref: #<anchor>]`, at **column 0**, on its **own line** directly under the section heading, with a blank line above and below:

  ```
  ## Scope Placement Rules

  [ref: #fixtures-scope-placement]

  | Scope | Where to define | Examples |
  ```

- A skill MUST choose **one** placement form and apply it uniformly. The separate-line form above is the required form for all new corpora; inline heading markers (`## Heading [ref: #x]`) are a legacy variant that MUST NOT be introduced.
- Parsers MUST skip fenced code blocks when scanning headings or markers (a ```markdown example can legitimately contain `#`-lines).

### 6.2 Anchor id format

- `<file-prefix>-<section-slug>`, **kebab-case**, lowercase.
  - `<file-prefix>` = filename with underscores → hyphens, or its chosen semantic shortening (§3).
  - `<section-slug>` = 1–4 words, often embedding the API/concept name.
- The card's `anchor` value MUST equal the body's marker exactly, minus the `#`: frontmatter `anchor: data-assertions-pytest-approx` ↔ body `[ref: #data-assertions-pytest-approx]`.

### 6.3 Load boundary

A section body runs from its marker to the **next** `[ref: #...]` marker or end of file. Markers MUST partition the file cleanly: every routable unit has exactly one marker; markers never nest; no body text bleeds past the next marker.

---

## 7. Loader Contract (how the frontmatter routes)

The card format exists to serve this loader behavior. A conformant skill's `SKILL.md` MUST implement this funnel (or a documented equivalent):

**Command 1 — subject map** (coarse routing, one line per file):

```bash
rg -N -H '^subject:' references/ | sed -E 's/:subject:[[:space:]]*/\t/'
```

**Command 2 — full frontmatter of shortlisted files only** (`<FILE-1> … <FILE-n>` are the chosen paths):

```bash
for f in "<FILE-1>" "<FILE-2>" ...; do printf '\n### %s\n' "$f"; awk '/^---[ \t]*$/{c++; if(c==2) exit; next} c==1{print}' "$f"; done
```

**Routing rules:**

1. Shortlist candidate files from the subject map using `subject` plus the request **plus inferred session work**; shortlist generously — if uncertain, expand the file list (up to a whole tier) and re-run Command 2.
2. Within shortlisted frontmatter, read **every** card and match `what`/`use_when`/`avoid_when` semantically (OR semantics within and across files). Mark each matching card's `anchor`.
3. **Deduplicate** anchors (convergence), then load each section.
4. Routing stays in the **main agent**: the inferred session context cannot be serialized to a subagent without loss. Subagents receive already-selected material.

**Bounded section extraction** (never a blind fixed `rg -A N` window):

```bash
awk '/^\[ref: #<ANCHOR>\]$/{f=1;print;next} f&&/^\[ref: #/{exit} f' references/<FILE>.md
```

This prints exactly from the target marker to the line before the next marker. (When the anchor id is needed first: `rg -n '^\[ref: #' references/<FILE>.md` lists all marker line numbers.)

**Frontmatter extraction warning:** match delimiters as anchored whole lines (`^---\s*$`; in awk: `^---[ \t]*$`). Never split on the bare substring `---` — bodies legitimately contain `---` inside code (e.g. `# --- Arrange ---`), and a naive split truncates the frontmatter with false YAML errors.

---

## 8. Authoring & Migration Workflow

1. Work file by file from an explicit todo list; each file requires user approval before work starts.
2. Read the whole file → audit → write/rewrite frontmatter → verify (§9 checklist, preferably scripted) → mark done.
3. When adding frontmatter to an existing body: edit ONLY the frontmatter (plus adding the single H1 if absent); body sections and `[ref]` markers stay byte-identical. Surface anchor↔marker mismatches to the user instead of silently fixing the body.
4. When enriching a body: keep every `[ref]` marker attached to its heading; never introduce cross-section routing tables; never re-introduce inline criteria blocks.
5. After any frontmatter edit, re-run the conformance check on the FINAL text of all fields — rewritten fields can introduce new dedup leaks against the new cloud.

---

## 9. Conformance Checklist (Validator Recipe)

A reference implementation of this checklist lives at `bootstrap/scripts/validate_reference_frontmatter.py` (`uv run --no-project --with pyyaml python`; `--allow-extra KEY` declares skill-extra top-level keys, `--aips` enables the api-design AIP cross-check). Skills MAY maintain hardened local ports of this implementation (e.g. `api-design/scripts/validate_reference_frontmatter.py`); the bootstrap copy stays the canonical reference. Run from the skill directory. For each `references/**/*.md`:

1. Frontmatter opens/closes with anchored `^---\s*$` lines; top-level keys ⊆ `{subject, index, libraries}` plus skill-declared extras.
2. `subject` present, double-quoted, one sentence: `<essence>; <cloud>`, 30–50 words (≥3-letter tokens), no `a`/`the`, no tier marker, identifiers backticked; covers every section area of the file.
3. Every `index` item has exactly the keys `{anchor, what, problem, use_when, avoid_when, expected}`; each a non-empty (except the two optional) double-quoted sentence.
4. Every `problem` follows §4.4: declarative situation + stake, no banned opener, no solution-API, no success language, 30–50 words (≥3-letter tokens), no `a`/`the`, concept-only cloud with no commands or library names.
5. `use_when` does not open with "Load when"/"Use when"; `avoid_when` does not open with "Do not"/"Don't"/"Never"; openers vary across cards; neither field restates `problem`.
6. Cross-field dedup: no ≥2-word cloud phrase appears verbatim in the card's other fields (check singular/plural both ways); cloud tokens are pairwise distinct.
7. For every card `anchor`, a body line `[ref: #<anchor>]` exists exactly once; for every body marker, a declaring card exists.
8. Anchors kebab-case `<file-prefix>-<section-slug>`; consistent prefix within the file; one placement form throughout the skill.
9. Exactly one `#` H1; routable sections are `##` (or deliberately routable `###`); markers partition the file with no nesting (scan outside fenced code).
10. No inline `**Selection criteria / anti-patterns:**` blocks; no cross-section routing/decision tables in bodies.
11. `libraries` (if present): lowercase canonical names, extras preserved, significant pins kept.
12. Convergence cards on one anchor state distinct criteria paths (no cloned text).

---

## 10. Forbidden Patterns (Conformance Breakers)

A file is non-conformant if it:

- Uses any top-level frontmatter key outside the closed set (+ skill-declared extras), or any legacy key (`triggers`/`description`/`decisions`).
- Adds/removes/renames any card key.
- Restates selection criteria or anti-patterns as an inline block inside a body section.
- Declares an `anchor` with no matching body marker, mismatches it, or places a marker with no declaring card.
- Nests markers or lets one section's body bleed past the next marker.
- Contains a cross-section decision/routing table in the body.
- Mixes anchor-placement forms within a skill, or introduces inline heading markers.
- Leaves `subject` vague, cloudless, tier-marked, article-bearing, or outside the 30–50-word band.
- Writes `problem` as capability/goal/imperative, leaks the solution or the success state, uses articles, falls outside the word band, or pollutes its cloud with commands/library names.
- Writes `use_when`/`avoid_when` as a restatement of `problem`, or with banned uniform openers.
