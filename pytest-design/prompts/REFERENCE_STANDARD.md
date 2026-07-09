# Reference Card Standard

A strict, normative specification for the reference-card format used by the `pytest-design` skill under `pytest-design/references/`. Every rule below is derived from the current files in that directory (27 cards: 13 in `required/`, 14 in `optional/`) and from the loading mechanic in `pytest-design/SKILL.md` §3. Nothing here is invented; where the corpus shows variation, the variation is named and bounded.

This standard is topic-agnostic. It defines the **card format**, not the pytest domain. Use it to author a reference card on **any** subject.

Normative keywords (`MUST`, `SHOULD`, `MAY`) follow RFC 2119.

---

## 1. Purpose and Mental Model

A reference card is a **lazy-loaded recipe file**. It is read in two stages:

1. **Routing (frontmatter only).** An agent batch-extracts the YAML frontmatter of every card in one shell command and decides, purely from that frontmatter, **which sections** it needs. It never reads a whole file to decide relevance.
2. **Loading (anchor sections only).** The agent loads only the body sections marked by the anchors it selected, reading each from its `[ref: #<anchor>]` marker to the next marker.

Two consequences shape the entire format:

- The frontmatter is the **selection layer**. Its sole job is to let the agent decide **which recipe(s) to load**; the agent never opens a body to make this choice. Each card is the selection gate for ONE recipe: `use_when` states when that recipe is needed and its opposite `avoid_when` states when that recipe must NOT be applied.
- The body is the **content layer**: pure HOW for the recipe that was already selected. A recipe is self-contained and MAY carry rich information — prose, code, **and tables that are that recipe's own reference content** (a scope/mode/parameter lookup, a symptom→cause→fix table inside a Common-Errors recipe, an anti-pattern→correct table inside an Anti-patterns recipe).
- The only obsolete pattern is a **cross-recipe decision/routing table** in the body: a table whose job is to select among recipes or techniques. That selection is the frontmatter's function, and duplicating it in the body is the legacy "decision table / routing table" that MUST NOT be created.

Routing is **semantic and context-aware**, never substring/keyword. The matching input is the user's request **plus** the session work the agent infers (the code it is about to write, the questions the problem implies). Cards MUST be written so that semantic matching works: each card states the concept, the problem it solves, and crisp positive/negative applicability.

---

## 2. File Layout and Taxonomy

### 2.1 Two-tier directory

Cards are split into exactly two buckets:

- `references/required/` — core, must-know techniques every practitioner needs. Filenames in the current corpus: `data_assertions`, `exceptions`, `faker`, `fixtures`, `isolation`, `markers`, `mocking`, `parametrization`, `pyproject`, `skip_xfail`, `temporary_files`, `testing_practices`, `time_control`.
- `references/optional/` — situational or advanced techniques activated by context (a dependency, a framework, a backend). Filenames: `assertion_plugins`, `asyncio`, `capture_fixtures`, `cli_testing`, `database_mocking`, `frameworks`, `internals`, `logging`, `patterns`, `performance`, `reporting`, `version_specific`, `warning_testing`, `xdist`.

A new card MUST be placed in `required/` only if it is universal baseline knowledge; otherwise it belongs in `optional/`.

### 2.2 Filename

- One topic area per file. Filename = `<topic>.md`, lowercase, words separated by **underscores** (`time_control.md`, `database_mocking.md`, `version_specific.md`).
- The filename slug (with underscores replaced by hyphens) is the default **anchor prefix** for the file (see §6.2). A semantic shortening MAY be used when it reads better (`warning_testing.md` → `warnings-...`, `version_specific.md` → `version-...`); once chosen, it MUST be used consistently for every anchor in the file.

### 2.3 File size and granularity

- A file holds **one topic area** decomposed into **recipes**. Each recipe (one API, one technique, or one decision) is one `##` section and is addressed by one or more frontmatter cards.
- Observed card counts per file range from **3 to 22**. Keep a file focused; split into a second file when a topic grows past one coherent area.
- Keep the body under roughly **500 lines** when practical; push variant-specific detail into the `### Variety booster` or a sibling file rather than inflating one section.

---

## 3. Frontmatter Contract (Normative)

The frontmatter is the **first** thing in the file, delimited by a line `---`, the YAML block, and a closing line `---`. It is followed by a blank line and then the `# Title`.

### 3.1 Allowed top-level fields (closed set)

Exactly these three top-level keys are permitted. No others.

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
- `libraries` — **optional**, a flat list of related packages/plugins.

**Forbidden** top-level keys (measured across all 27 files: zero occurrences): `triggers`, `description`, `decisions`. They were consolidated into `index`. A card carrying any of them is non-conformant.

### 3.2 `subject`

`subject` is the **file-level coarse router**: an agent reads only this line to decide whether the whole file is relevant to the request. It MUST therefore name the topic **and** enumerate every recipe area with the concrete APIs/techniques, so semantic routing hits without opening the body.

**Firm style (binding):**

- **Form:** one double-quoted sentence shaped as `<short essence of the file topic>; <comma-separated keyword/API cloud of every recipe area>`. Lead with a short declarative essence, then `; `, then the cloud.
- **Length:** 30–50 words, counting only tokens of **≥3 letters** (short function words are free). Pad the **cloud**, never the essence.
- **No articles:** the tokens `a` and `the` MUST NOT appear (they add routing noise). Keep them only inside backticked code, where they are rare anyway.
- **No tier marker:** never write `CORE` / `EXTENDED` in `subject`; the tier is the directory (`required/` vs `optional/`).
- **Identifiers in backticks:** every API, flag, value, and version is inline-coded.
- **APIs and library names are WELCOME in the `subject` cloud** — naming them is the entire point of coarse routing. (This is the opposite of the `problem` cloud in §3.3, where library/command names are forbidden.)

Good — real corpus lines:

- `"Write reliable async tests: pick \`pytest-asyncio\` for pure asyncio or \`pytest-anyio\` for multi-backend, set \`asyncio_mode\` and matching \`scope\`/\`loop_scope\`, share event loops across async fixtures, mock coroutines with \`AsyncMock\`, guard hangs with \`asyncio.timeout\`/\`pytest-timeout\`, and verify gather/TaskGroup/ThreadPoolExecutor race invariants."`
- `"Assert error contracts precisely: \`pytest.raises(Exc, match=...)\` with specific regex (\`re.escape\` for literals), capture \`ExceptionInfo\` and inspect \`.type\`/\`.value\`/attributes (\`exc_info.type is ExactException\`), parametrize cases, \`pytest.deprecated_call\`/\`pytest.warns\`, \`xfail(raises=...)\`, and manual \`ExceptionGroup\` inspection; never \`match='.*'\`, broad \`Exception\`, or \`exc_info.typename\`."`

Bad — and why:

- `"Core recipes for pytest fixtures."` — vague essence, **no recipe-area cloud**, far under 30 words; an agent cannot route from it.
- `"CORE — everything about fixtures, scopes, and cleanup."` — carries a **tier marker** (belongs in the directory) and still omits the API/area cloud.

### 3.3 `index` — the card list

`index` is a **flat list** of self-contained decision cards. It is the single catalog of the file. The list order SHOULD mirror the body section order. **Each card is a self-contained decision-making system** and the selection gate for ONE recipe: `use_when` (when this recipe is needed) and `avoid_when` (when this recipe must NOT be applied) are opposite **lists of criteria** that together decide whether the agent loads this recipe or a different one. Any number of cards MAY share one `anchor` (see §3.4).

Each card binds **one** `anchor` to its full `WHEN`/`WHY` criteria. A card is a mapping with **exactly** these six keys (closed set; measured uniform across all files):

| Key | Required | Content |
|---|---|---|
| `anchor` | yes | The body-section id this card routes to (see §6.2). |
| `what` | yes | Brief, concise description of WHAT the entity under the anchor IS, framed **as applied to solving the task in `problem`** — not a detached generic definition. |
| `problem` | yes | What the **case described in the card** solves (the agent's decision-time problem) — NOT a generic statement of what the recipe under the anchor solves. |
| `use_when` | yes | A **list of clear, precise criteria** for when this recipe MUST be loaded and used. |
| `avoid_when` | yes* | A **list of clear, precise criteria** for when this recipe MUST NOT be used. |
| `expected` | yes* | The **attainability criterion**: what we expect to hold after applying the recipe — the observable sign that `problem` is solved. |

\* `avoid_when` and `expected` are present on every card in the corpus. They MAY be empty only for a pure lookup entry that has no anti-pattern and no success state, but the corpus fills them for nearly every card; authors SHOULD fill them.

Authoring rules for each field:

- The whole card is one decision unit: `problem` states the case's problem, `what` names the entity as it addresses that problem, `use_when`/`avoid_when` give the positive/negative criteria lists, `expected` gives the success criterion. A reader of **only** the card MUST be able to decide load-or-skip and to know the expected result — without the body.
- **One sentence each**, double-quoted, specific, and self-contained. `use_when` and `avoid_when` read as **lists of crisp criteria** (enumerate them; separate with semicolons), not vague prose.
- Use backticks for every identifier, API, flag, and value (`pytest.approx`, `loop_scope`, `>=0.23`).
- `what` names the concrete mechanism (with key parameters where relevant) **in terms of the problem it solves here** — e.g. `pytest.approx(expected, rel=..., abs=..., nan_ok=...)` as the tolerance that keeps a computed-number assertion from flaking.
- `problem` states the **case's** problem in the strict **situation + stake** form defined in the firm-style block below. It is never a capability ("Assert on …"), never a goal/imperative ("Avoid …", "Keep …"), never the solution API (that belongs in `what`), and never the success state (that belongs in `expected`).
- `use_when` is a positive criteria list ("Use when …; when …; when …"). Include version gates and concrete scenarios.
- `avoid_when` is a negative criteria list naming the canonical wrong forms ("Do not use when …; never when …").
- `expected` states the attainable success state ("numerical assertions pass within the configured tolerance and recurse over collections instead of flaking").

**Firm style for `problem` (binding):**

- **Role:** `problem` lets the agent recognize *"this is exactly my situation right now."* Write a declarative **agent situation + the concrete stake** (what breaks, flakes, leaks, or costs), not what the recipe can do.
- **Form:** one double-quoted sentence shaped as `"<concrete situation in the test/code>; <naïve path> → <what breaks / flakes / costs>; <keyword cloud>"`. After the situation sentence add `; ` and a comma-separated **keyword cloud** of concepts, synonyms, and triggers to strengthen semantic routing.
- **Length:** 30–50 words, counting only tokens of **≥3 letters** (short function words are free). Reach the floor by enriching the **cloud** and the situation detail — never by padding with filler.
- **No articles:** the tokens `a` and `the` MUST NOT appear anywhere in `problem` (they add routing noise). Keep them only inside backticked code.
- **No solution leakage:** do not name the answer API/technique in the situation ("use `pytest.approx`") — the mechanism lives in `what`. Do not state the success outcome ("so that … reports together") — that lives in `expected`.
- **Cloud discipline:** the keyword cloud contains **concepts, synonyms, and triggers only** — NO Python commands and NO library names (for example `caplog`, `faker`, `pytest.approx` are forbidden there). Naming libraries/APIs belongs in `subject` (§3.2) and `what`, never in the `problem` cloud.
- **Banned openers** (capability/goal/imperative): `"Assert on …"`, `"Verify …"`, `"Exercise …"`, `"Avoid …"`, `"Keep …"`, `"Provide …"`. Rewrite each as a neutral situation + stake.
- **Identifiers in backticks** whenever an identifier is unavoidable in the situation.

Good — conforms (32 words, no articles, concept-only cloud):

- `"Fixture declared \`scope='session'\` without \`loop_scope='session'\` recreates event loop for every test and breaks resources tied to original loop; loop mismatch, attached future, cross-loop resource, scope alignment, runtime error, shared loop lifetime, reused fixture."`
- `"Computed numeric result drifts from exact value under floating-point rounding and exact-equality assertion flakes across runs; tolerance, relative delta, absolute delta, rounding noise, decimal drift, representation error, recursive compare, near-equal, collection compare, computed value."`

Bad — and the specific rule each breaks:

- `"Assert on float results within tolerance."` — **capability** opener, no situation, no cloud, 5 words.
- `"Avoid flaky float assertions in tests."` — **goal/imperative** opener, no situation, 5 words.
- `"Use \`pytest.approx\` to compare floats so that assertions stay green."` — **leaks the solution API** (→ `what`) **and the success state** (→ `expected`).
- `"A test needs the faker value to stay unique; faker, unique, the registry."` — contains **articles** (`a`, `the`) **and a library name** (`faker`) inside the cloud.

### 3.4 Anchors are not unique (convergence)

Several cards MAY share the **same** `anchor`. This expresses **converging selection criteria** that point to one recipe section. The loader deduplicates anchors and loads the shared section once. Measured convergence occurs in `markers.md`, `asyncio.md`, `internals.md`, `performance.md`, and `pyproject.md` (e.g., `pyproject.md` repeats six anchors across 22 cards). Use convergence when distinct `what`/`use_when` paths legitimately collapse onto a single body section; do **not** create a separate mechanism for it.

### 3.5 `libraries`

- Optional flat list of related packages/plugins, lowercase PyPI-style names.
- Keep **significant version pins** where behavior depends on them (`pytest-asyncio>=0.23`, `click>=8.4`, `sqlalchemy>=2.0`, `pytest-cov>=5.0`).
- Preserve **extras** when a recipe needs them (`fakeredis[lua]`, `py-pglite[sqlalchemy]`, `testcontainers[postgresql]`).
- Omit the field entirely when the card needs no external package (several corpus files have no `libraries`).

### 3.6 Canonical frontmatter template

```yaml
---
subject: "<One sentence naming the topic and enumerating its recipe areas.>"
index:
  - anchor: <file-prefix>-<recipe-slug>
    what: "<The entity under the anchor, concisely, framed as applied to `problem`.>"
    problem: "<What the case in this card solves — the agent's decision-time problem; NOT the recipe's abstract purpose.>"
    use_when: "<List of clear, precise criteria: load and use when …; when …; when …>"
    avoid_when: "<List of clear, precise criteria: do NOT use when …; never when …>"
    expected: "<Attainability criterion: what holds after applying; the sign that `problem` is solved.>"
  - anchor: <file-prefix>-<recipe-slug>      # MAY repeat a prior anchor (convergence)
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

## 4. Body Skeleton

After the frontmatter, the body is:

```
# <TITLE>

<optional one-line intro>

## <Recipe Heading>

[ref: #<anchor>]

<recipe HOW>

## <Recipe Heading>

[ref: #<anchor>]

<recipe HOW>
...
```

### 4.1 Title (`#`)

- Exactly **one** H1 per file, placed immediately after the frontmatter.
- Style is thematic. The corpus shows two acceptable forms:
  - **ALL-CAPS**, often with a tier suffix in `required/`: `# DATA & ASSERTIONS — CORE`, `# FIXTURE HIERARCHY — CORE`, `# MOCKING`, `# TIME CONTROL`. The optional counterpart of a required topic MAY use `— EXTENDED` (`# DATA & ASSERTIONS — EXTENDED` in `assertion_plugins.md`).
  - **Title Case**, common in `optional/`: `# Framework-Specific Appendices`, `# Advanced pytest Internals`, `# Parallel Execution with pytest-xdist`, `# Python 3.12+ Specifics`, `# Reporting and CI`.
- Pick one form and keep it consistent within a skill. For a CORE/EXTENDED pair, reuse the same base title with the `— CORE` / `— EXTENDED` suffix.

### 4.2 Optional intro

A single short line MAY sit between the H1 and the first `##` to tell the reader how to activate the file (e.g., `frameworks.md`: *"Activate the relevant appendix by scanning `pyproject.toml` dependencies and `src/` imports."*). Keep it to one or two sentences; never restate selection criteria (those belong in cards).

### 4.3 Recipe sections (`##`)

- Each recipe is a `##` heading. Headings are short noun phrases or `<API> for <purpose>` forms (`` `pytest.approx` for Numeric Comparisons ``, `Scope Placement Rules`, `Factory Fixtures and Nested Transaction Rollback`).
- Heading text is in **Title Case**; inline code is used for APIs inside headings (`` `mocker.patch.object` versus `mocker.patch` ``).
- The set of `##` headings in a file SHOULD align 1:1 with the distinct anchors declared in `index` (modulo convergence, where several cards share one anchor).

### 4.4 Sub-sections (`###`)

`###` is used sparingly for sub-recipes inside a larger `##` (observed in `frameworks.md`, `logging.md`, `internals.md`, `parametrization.md`, `version_specific.md`). Sub-sections that are independently routable (e.g., a `### Variety booster`) carry their **own** anchor; purely illustrative sub-headings need none.

---

## 5. Section Anatomy (the HOW)

A recipe section is pure HOW. Its typical shape, in order:

1. **Lead prose** (1–6 sentences). Imperative, present tense. States the rule and the core do/don't, names defaults and edge cases. Opens with a verb (`Use ...`, `Mirror ...`, `Annotate ...`, `Design ...`, `Drive ...`) or, in some optional files, with `"This section covers/explains ..."`. Inline-code every identifier.
2. **Code and, where it is the recipe's own content, tables** — the substance (see §7–§8). Multiple code blocks per section are common; each is introduced by a one-line lead sentence ending in a colon (`"Near-zero values need an explicit absolute tolerance:"`, `"Usage in tests:"`, `"Collections and dicts are compared recursively:"`).
3. **Contrast pairs** (optional). When showing a wrong vs right form, label the blocks inline and place each label directly before its fence:
   - `Bad — <reason>:` / `Good — <reason>:`
   - `Wrong — <reason>:` / `Correct — <reason>:`
4. **Variety booster** (near-universal terminator). See §5.1.

Selection criteria and anti-patterns MUST NOT appear as an inline `**Selection criteria / anti-patterns:**` block inside a recipe, because the recipe's `use_when`/`avoid_when` gate already lives in its frontmatter card. Body `## Anti-patterns` / `## Common Errors` sections are ordinary recipes (each with its own anchor and card); their tables are their own content (see §5.2).

### 5.1 Variety booster (terminator)

Almost every section ends with a **variety booster**: a short note on how to parametrize or extend the recipe so one assertion body covers many cases. The corpus uses **three** typographic forms; pick per skill and stay consistent:

1. **Bold inline paragraph** (dominant in `required/`):
   `**Variety booster:** <one sentence or short paragraph.>`
2. **Plain label + bullet(s)** (e.g., `asyncio.md`):
   `Variety booster:` newline `- <bullet>`.
3. **Dedicated heading with its own anchor** (e.g., `frameworks.md` as `### Variety booster [ref: #...-variety-booster]`; other optional files use `## Variety Booster`). Use this form when the booster carries a fuller code example and is independently routable.

The booster SHOULD suggest combining dimensions (roles × statuses × methods), reusing one assertion body, or lifting a literal into a parameter.

### 5.2 Special anchored sections

These file-level sections are ordinary recipes — each has its own anchor and its own card that decides when the agent loads it:

- `## Anti-patterns` / `## Common Anti-Patterns` — a recipe whose content is a `"Do not ..."` bullet list and/or a `| Anti-pattern | Correct approach |` table. Its card's `use_when` selects it for fixture/code review; the table is the recipe's own teaching, not a router to other recipes.
- `## Common Errors` — a recipe whose content is a `| Symptom | Cause | Fix |` table plus a short clarifying example. Its card's `use_when` selects it when a failure matches a listed symptom; the table is the recipe's content.
- `## Variety Booster` / `## Variety Booster: <Topic>` — a consolidated parametrization example (see §5.1 form 3).

---

## 6. Anchors

### 6.1 Placement

- The anchor marker is the literal line `[ref: #<anchor>]`.
- **Dominant form (25 of 27 files):** the marker sits on its **own line** directly under the `## Heading`, with a blank line above and below:

  ```
  ## Scope Placement Rules

  [ref: #fixtures-scope-placement]

  | Scope | Where to define | Examples |
  ```

- **Minority form (`cli_testing.md`, `database_mocking.md`):** the marker is **inline** on the heading line: `## argparse CLIs [ref: #cli-testing-argparse]`.
- A skill MUST choose **one** form and apply it to every section of every card. Prefer the dominant separate-line form for new skills.

### 6.2 Anchor id format

- `<file-prefix>-<recipe-slug>`, **kebab-case**, lowercase.
  - `<file-prefix>` = filename with underscores → hyphens, or its chosen semantic shortening (§2.2).
  - `<recipe-slug>` = 1–4 words, often embedding the API name (`pytest-approx`, `loop-scope`, `mock-open`, `factory-rollback`).
- The card's `anchor` value MUST equal the body's `[ref: #<anchor>]` exactly (the frontmatter `anchor` omits the leading `#`; the body marker includes it).
- Examples: frontmatter `anchor: data-assertions-pytest-approx` ↔ body `[ref: #data-assertions-pytest-approx]`.

### 6.3 Load boundary

A section body runs from its `[ref: #<anchor>]` marker to the **next** `[ref: #...]` marker or the end of the relevant sub-section. Authors MUST ensure markers partition the file cleanly: every routable unit has exactly one marker, and markers never nest.

---

## 7. Tables

Tables are a normal part of a recipe's self-contained content. The deciding test is **what the table does**:

- **Allowed — intra-recipe content.** The table is the substance of an already-selected recipe: a scope/mode/parameter lookup, a `| Symptom | Cause | Fix |` table inside a Common-Errors recipe, an `| Anti-pattern | Correct approach |` table inside an Anti-patterns recipe, a `| Scope | Where to define | Examples |` table inside a scope recipe. Standard Markdown, header + `|---|` separator, short cells, inline code for APIs/flags/values. A table MAY be the entire body of such a recipe (followed by a variety booster).
- **Forbidden — cross-recipe routing/decision.** A body table whose function is to select **which recipe or technique to load** duplicates the frontmatter's selection layer and MUST NOT be created. If a table answers "given situation X, which recipe do I use?", that logic belongs in the cards (each recipe's `use_when`/`avoid_when`), not in the body.

Observed corpus tables (e.g., in `fixtures.md`, `capture_fixtures.md`, `asyncio.md`, `xdist.md`, `parametrization.md`) are intra-recipe content and are legitimate models.

---

## 8. Code Blocks

- Fenced with triple backticks and a **language tag**. `python` dominates; `toml` for configuration, `bash` for CLI, `text` for directory trees and output, `ini`/`yaml` rarely.
- Each fence is introduced by a lead sentence ending in a colon (§5). Contrasting pairs use the `Bad/Good` or `Wrong/Correct` labels (§5 item 3).
- Code is **self-contained and realistic**: show imports, types, and the minimal surrounding fixture/class so the example reads as runnable. Implied helpers (e.g., `dashboard.is_visible_to`) are acceptable when their role is obvious.

### 8.1 Python code style inside examples (corpus-consistent)

When the card's domain is Python/pytest, examples uniformly follow:

- **Imports** grouped stdlib → third-party, blank-line separated; `from collections.abc import Generator, Callable`, `from enum import StrEnum`, `from datetime import UTC`, `from typing import Any`, `import pytest`, `from faker import Faker`, and explicit pytest fixture types `from pytest import CaptureFixture, LogCaptureFixture`.
- **Tests** annotated `-> None`, named `test_<unit>_<condition>_<expected>`, with a triple-quoted **Given/When/Then** docstring and **AAA** divider comments (`# --- Arrange ---`, `# --- Act ---`, `# --- Assert ---`).
- **Test data via Faker only**: `fake.uuid4()`, `fake.sentence()`, `fake.pyfloat(min_value=..., max_value=..., positive=True)`, `fake.pyint(...)`, `fake.unique.word()`, `fake.fake_email()`, `fake.boolean(chance_of_getting_true=ACTIVATION_CHANCE)`, `fake.date_time_between(start_date="-1y", end_date="now", tzinfo=UTC)`. No stdlib `random`; magic chances lifted to **named constants** (`ACTIVATION_CHANCE = 90`).
- **Types everywhere**: fixtures typed `Generator[X, None, None]` (teardown) / `-> X` (no teardown) / `Callable[..., T]` (factories); built-in fixtures typed (`capsys: CaptureFixture[str]`, `caplog: LogCaptureFixture`, `monkey: pytest.MonkeyPatch`, `request: pytest.FixtureRequest`).
- **Data shapes**: `@dataclass(frozen=True)` and `StrEnum`/`IntEnum` for categories; value equality via generated `__eq__`/`__repr__`.

These rules mirror the host skill; a card on a **different** domain substitutes that domain's idioms but keeps the same presentation discipline (imports shown, types shown, runnable shape, labeled contrasts).

---

## 9. Writing Style

- **Voice:** imperative, second person implied, present tense ("Use", "Prefer", "Do not", "Never").
- **Density:** one idea per sentence; short paragraphs; lead sentences that set up the next block end in a colon.
- **Emphasis:** bold for the `Bad`/`Good`/`Wrong`/`Correct` labels and the `**Variety booster:**` label; inline backticks for every identifier, flag, value, and version.
- **No duplication of routing data:** never restate `use_when`/`avoid_when` as an inline block inside a recipe. The body demonstrates; the cards decide.
- **Cross-references:** use the `[ref: #<anchor>]` marker syntax for anchor targets. References between cards/files use the same id form.
- **Standards before web:** when a card cites an external standard, prefer a local copy over a web fetch (host-skill convention).

---

## 10. Loader Contract (how the frontmatter routes)

The card format exists to serve this loader behavior (from `SKILL.md` §3):

1. Batch-extract every card's frontmatter in one command.
2. Use `subject` to select relevant files (coarse).
3. Within each selected file, read **every** `index` card and match `what`/`use_when`/`avoid_when` against the request **plus inferred session work** (semantic, OR semantics across cards). Mark each matching card's `anchor`.
4. **Deduplicate** anchors (convergence), then load each `[ref: #<anchor>]` section to the next marker.

Authors MUST write cards so this works: self-contained fields, crisp positive/negative applicability, exact anchor equality, and bodies that contain only HOW. **Selection among recipes is entirely a frontmatter function** — there is no separate routing artifact and no cross-recipe body routing table. A selected recipe's body may still contain its own content tables (§7).

---

## 11. Forbidden Patterns (Conformance Breakers)

A card is non-conformant if it:

- Uses any top-level frontmatter key other than `subject`, `index`, `libraries` (no `triggers`/`description`/`decisions`).
- Adds/removes/renames any card key (the set is exactly `anchor, what, problem, use_when, avoid_when, expected`).
- Restates selection criteria or anti-patterns as an inline block inside a recipe body.
- Declares an `anchor` that has no matching `[ref: #<anchor>]` (or mismatches it), or places a `[ref:]` marker with no declaring card.
- Nests `[ref:]` markers or lets one section's body bleed past the next marker.
- Contains a **cross-recipe** decision/routing table in the body — a table whose function is to select among recipes or techniques (the selection the frontmatter already performs). Intra-recipe content tables (scope/mode/parameter lookups, symptom→cause→fix, anti-pattern→correct) are allowed.
- Mixes anchor-placement forms within a skill (pick separate-line **or** inline, uniformly).
- Leaves `subject` vague (it must name the topic **and** enumerate the recipe areas).
- Writes `subject` without its keyword/API cloud, with a `CORE`/`EXTENDED` tier marker, with the articles `a`/`the`, or outside the 30–50-word band (≥3-letter tokens).
- Writes `problem` as a capability/goal/imperative ("Assert on…", "Avoid…"), leaks the solution API (→ `what`) or the success state (→ `expected`), uses the articles `a`/`the`, falls outside the 30–50-word band, or puts Python commands / library names in its keyword cloud.

---

## 12. Conformance Checklist (Validator Recipe)

Run from the skill directory. For each `references/**/*.md`:

1. Frontmatter opens/closes with `---`; top-level keys ⊆ `{subject, index, libraries}`.
   - Extract the frontmatter by matching the delimiter as an **anchored whole line** (`^---\s*$`) and taking the text between the first and second such lines. Do **not** split on the bare substring `---` (e.g. `text.split('---', 2)`): card text legitimately contains `---` inside backticks such as `` `# --- Arrange ---` `` and the AAA dividers `# --- Act ---` / `# --- Assert ---`, which an unanchored split misreads as the closing delimiter and truncates the frontmatter (false “unexpected end of stream” YAML errors).
2. `subject` present, double-quoted, one sentence naming topic + recipe areas.
3. Every `index` item has exactly the keys `{anchor, what, problem, use_when, avoid_when, expected}`; each a non-empty (except the two optional) double-quoted sentence.
4. For every card `anchor`, a body line `[ref: #<anchor>]` exists exactly once; for every body `[ref: #<x>]`, a declaring card exists.
5. Anchors kebab-case `<file-prefix>-<recipe-slug>`; consistent prefix within the file.
6. One anchor-placement form used throughout the skill.
7. Exactly one `#` H1; recipes are `##` (routable) with optional `###` sub-units; markers partition the file with no nesting.
8. No inline `**Selection criteria / anti-patterns:**` blocks inside recipe bodies.
9. Every recipe section ends (where applicable) with a variety booster in the skill's chosen typographic form.
10. Every body table is intra-recipe content, not a cross-recipe router; selection among recipes lives only in the frontmatter cards.
11. `libraries` (if present) uses lowercase names, preserves extras, and keeps significant pins.
12. `subject` follows the firm style: `<essence>; <keyword/API cloud>`, 30–50 words (≥3-letter tokens), no `a`/`the`, no tier marker, identifiers backticked; library/API names are allowed in this cloud.
13. Every `problem` follows the firm style: declarative **situation + stake** (not capability/goal/imperative), no solution-API (→ `what`) and no success language (→ `expected`), 30–50 words (≥3-letter tokens), no `a`/`the`, and a concept/synonym-only keyword cloud with no Python commands or library names.
