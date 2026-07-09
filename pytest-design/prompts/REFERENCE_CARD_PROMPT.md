# Prompt: Generate a Reference Card (any topic)

Use this prompt to produce a **reference card** that conforms to `REFERENCE_STANDARD.md`. The output is a single lazy-loaded recipe file: a YAML frontmatter routing index plus a pure-HOW body. The authoritative contract is the standard; this prompt operationalizes it. If anything here conflicts with the standard, the standard wins.

Copy everything from `<BEGIN PROMPT>` to `<END PROMPT>` and fill the `{{...}}` inputs.

---

<BEGIN PROMPT>

You are authoring a **reference card** — a lazy-loaded recipe file consumed in two stages: (1) an agent reads only the YAML frontmatter to decide which sections apply, then (2) loads only those `[ref: #<anchor>]` body sections. Your card MUST be routable from the frontmatter alone and MUST contain only HOW in the body.

## Inputs (fill before generating)

- `{{TOPIC}}` — the subject area of the card (e.g., "Capturing stdout/stderr/logs in tests", "Rate limiting with token buckets").
- `{{TIER}}` — `required` (universal baseline) or `optional` (activated by a dependency/framework/backend). Default `optional` unless the topic is universal.
- `{{FILENAME}}` — `<topic_slug>.md`, lowercase, words separated by underscores.
- `{{ANCHOR_PREFIX}}` — the filename slug with underscores → hyphens, or a shorter semantic prefix used consistently for every anchor (e.g., file `warning_testing.md` → `warnings`).
- `{{ANCHOR_STYLE}}` — `separate` (anchor on its own line under the heading; preferred) or `inline` (`## Heading [ref: #x]`). One form for the whole skill.
- `{{VARIETY_FORM}}` — `bold` (`**Variety booster:** ...`), `plain` (`Variety booster:` + bullet), or `heading` (`### Variety booster` with its own anchor). One form per skill.
- `{{DOMAIN_IDIOMS}}` — the language/framework conventions for code examples (imports, types, test naming, data generation). For Python/pytest use the corpus style in §C below.
- `{{LIBRARIES}}` — optional list of related packages (lowercase; keep significant pins and extras).

## Output

Produce exactly one Markdown file at `references/{{TIER}}/{{FILENAME}}` with two parts, in this order: frontmatter, then body. No other files. No README, no changelog.

---

## Part A — Frontmatter (routing index)

The frontmatter is the FIRST thing in the file: a line `---`, the YAML, a closing line `---`, then a blank line, then the `# Title`.

### A.1 Top-level fields (closed set)

Only `subject`, `index`, `libraries`. Nothing else. Forbidden: `triggers`, `description`, `decisions`.

- `subject` — required; the **file-level coarse router**. One double-quoted sentence in the firm style `<short essence>; <keyword/API cloud of every recipe area>`, 30–50 words (≥3-letter tokens), no `a`/`the`, no tier marker, identifiers backticked. Library/API names are welcome in this cloud. See §A.5.
- `index` — required; a flat list of decision cards, in the same order as the body sections.
- `libraries` — optional; flat list; preserve extras (`pkg[extra]`) and significant pins (`pkg>=X.Y`); omit entirely if none.

### A.2 Each card (closed key set)

Every card is a self-contained **decision-making system** and has EXACTLY these keys: `anchor`, `what`, `problem`, `use_when`, `avoid_when`, `expected`. One double-quoted sentence each; a reader of ONLY the card must be able to decide load-or-skip and to know the expected result.

- `anchor` — `{{ANCHOR_PREFIX}}-<recipe-slug>`, kebab-case, 1–4-word recipe slug (often embedding the API name).
- `what` — brief, concise WHAT the entity under the anchor is, framed **as applied to solving `problem`** (not a detached generic definition); name the exact `API`/technique and key parameters.
- `problem` — the agent's decision-time **situation + stake** for the case in this card (declarative), so the agent recognizes "this is my situation." Never a capability ("Assert on…"), never a goal/imperative ("Avoid…"), never the solution API (→ `what`), never the success state (→ `expected`). Ends with `; <concept/synonym keyword cloud>` (no commands, no library names). 30–50 words (≥3-letter tokens), no `a`/`the`. See §A.5.
- `use_when` — a **list of clear, precise criteria** for when this recipe MUST be loaded and used (enumerate; version gates; concrete scenarios).
- `avoid_when` — a **list of clear, precise criteria** for when this recipe MUST NOT be used (the canonical wrong forms). Fill it; empty only for a pure lookup entry.
- `expected` — the **attainability criterion**: what we expect to hold after applying the recipe (the sign that `problem` is solved). Fill it; empty only for a pure lookup entry.

`use_when` and `avoid_when` are opposite **lists of criteria** that together form the **selection gate for ONE recipe**: they decide whether the agent loads *this* recipe or a different one. Write them as crisp criteria, not as the recipe's teaching content.

**All selection, decision, and routing (WHEN/WHY) lives here and nowhere else.** If you find yourself wanting a body "decision table" or "routing table", put that logic into the cards instead.

### A.3 Convergence (anchors may repeat)

Several cards MAY share one `anchor` when distinct selection criteria collapse onto one recipe section. Do not invent a separate mechanism — repeat the anchor. The loader deduplicates.

### A.4 Frontmatter template

```yaml
---
subject: "<Short essence of {{TOPIC}}; <comma-separated keyword/API cloud of EVERY recipe area> — 30–50 words (≥3-letter tokens), no a/the, no tier marker; library/API names welcome in the cloud.>"
index:
  - anchor: {{ANCHOR_PREFIX}}-<recipe-slug>
    what: "<The entity under the anchor, concisely, framed as applied to `problem`.>"
    problem: "<Situation + stake: <concrete situation in test/code>; <naïve path> → <what breaks/flakes/costs>; <concept/synonym keyword cloud> — 30–50 words (≥3-letter tokens), no a/the, NO Python commands or library names in the cloud; solution API belongs in `what`, success language in `expected`.>"
    use_when: "<List of clear, precise criteria: load and use when …; when …; when …>"
    avoid_when: "<List of clear, precise criteria: do NOT use when …; never when …>"
    expected: "<Attainability criterion: what holds after applying; the sign that `problem` is solved.>"
  - anchor: {{ANCHOR_PREFIX}}-<recipe-slug>      # MAY repeat a prior anchor (convergence)
    what: "..."
    problem: "..."
    use_when: "..."
    avoid_when: "..."
    expected: "..."
libraries:                                        # optional; omit if none
  - package-name
  - pinned-package>=X.Y
  - package[extra]
---
```

### A.5 Firm style for `subject` and `problem` (binding)

These two fields carry most of the routing weight, so their shape is fixed, not free-form. The full normative rules live in `REFERENCE_STANDARD.md` §3.2 (`subject`) and §3.3 (`problem`); the operational summary below is what you apply while generating.

#### `subject` — file-level coarse router

- **Form:** `"<short essence of the topic>; <comma-separated keyword/API cloud of every recipe area>"`.
- **Length:** 30–50 words, counting only tokens of **≥3 letters** (short function words are free). Pad the **cloud**, not the essence.
- **No articles:** no `a`, no `the`. **No tier marker:** never `CORE`/`EXTENDED` (the directory carries the tier). **Identifiers in backticks.**
- **Library/API names are WELCOME** in the `subject` cloud — naming them is the point of coarse routing.

Good:

- `"Write reliable async tests: pick \`pytest-asyncio\` for pure asyncio or \`pytest-anyio\` for multi-backend, set \`asyncio_mode\` and matching \`scope\`/\`loop_scope\`, share event loops across async fixtures, mock coroutines with \`AsyncMock\`, guard hangs with \`asyncio.timeout\`/\`pytest-timeout\`, and verify gather/TaskGroup/ThreadPoolExecutor race invariants."`

Bad: `"Core recipes for pytest fixtures."` (no recipe-area cloud, 5 words); `"CORE — fixtures, scopes, cleanup."` (tier marker + no cloud).

#### `problem` — card-level situation + stake

- **Form:** `"<concrete situation in the test/code>; <naïve path> → <what breaks/flakes/costs>; <comma-separated concept/synonym keyword cloud>"`.
- **Voice:** declarative **agent situation + stake**, never capability ("Assert on…", "Verify…", "Exercise…"), never goal/imperative ("Avoid…", "Keep…", "Provide…"). The agent should think *"this is exactly my situation."*
- **No leakage:** the answer API/technique belongs in `what` (do not write "use `pytest.approx`"); the success outcome belongs in `expected` (do not trail off with "so that … reports together").
- **Length:** 30–50 words, counting only tokens of **≥3 letters**. Reach the floor with richer situation detail and a denser concept cloud — never filler.
- **No articles:** no `a`, no `the` anywhere (keep only inside backticked code).
- **Cloud discipline:** concepts, synonyms, and triggers only — **NO Python commands and NO library names** (`caplog`, `faker`, `pytest.approx` are forbidden in the cloud). Name libraries/APIs in `subject` and `what` instead.

Good (32 words, no articles, concept-only cloud):

- `"Fixture declared \`scope='session'\` without \`loop_scope='session'\` recreates event loop for every test and breaks resources tied to original loop; loop mismatch, attached future, cross-loop resource, scope alignment, runtime error, shared loop lifetime, reused fixture."`
- `"Computed numeric result drifts from exact value under floating-point rounding and exact-equality assertion flakes across runs; tolerance, relative delta, absolute delta, rounding noise, decimal drift, representation error, recursive compare, near-equal, collection compare, computed value."`

Bad — and the rule each breaks:

- `"Assert on float results within tolerance."` — capability opener, no situation/cloud, 5 words.
- `"Avoid flaky float assertions in tests."` — goal/imperative opener, no situation, 5 words.
- `"Use \`pytest.approx\` to compare floats so that assertions stay green."` — leaks solution API (→ `what`) and success state (→ `expected`).
- `"A test needs the faker value to stay unique; faker, unique, the registry."` — articles (`a`, `the`) and a library name (`faker`) inside the cloud.

---

## Part B — Body (pure HOW)

### B.1 Skeleton

```
# <TITLE>

<optional one-line intro>

## <Recipe Heading>
                                  # separate style:
[ref: #{{ANCHOR_PREFIX}}-slug]    # (blank line above and below)
                                  # inline style:  ## <Recipe Heading> [ref: #prefix-slug]
<recipe HOW: lead prose → code → (contrast pairs) → variety booster>

## <Recipe Heading>
...
```

### B.2 Title (`#`)

Exactly one H1, immediately after the frontmatter. Thematic ALL-CAPS (with `— CORE` / `— EXTENDED` for required/extended pairs) or Title Case — match the host skill and stay consistent. A single one-line intro MAY follow the H1 to say how the file activates; never restate selection criteria here.

### B.3 Recipe section anatomy (in order)

1. **Lead prose** — 1–6 imperative present-tense sentences stating the rule and core do/don't, naming defaults and edge cases. Open with a verb (`Use`, `Prefer`, `Design`, `Drive`) or `This section covers/explains …`. Inline-code every identifier. Do NOT restate `use_when`/`avoid_when` here.
2. **Code** — the substance. One or more fenced, language-tagged blocks; each introduced by a one-line lead sentence ending in a colon. Self-contained and realistic (imports, types, minimal surrounding fixture/class) so it reads as runnable.
3. **Contrast pairs** (optional) — `Bad — <reason>:` / `Good — <reason>:` or `Wrong — <reason>:` / `Correct — <reason>:`, each label directly before its fence.
4. **Variety booster** — near-universal terminator, in `{{VARIETY_FORM}}`. Suggest combining dimensions so one assertion/recipe body covers many cases.

### B.4 Selection vs content (hard rule)

The frontmatter is the **selection layer**: it decides WHICH recipe the agent loads. The body is the **content layer**: pure HOW for the already-selected recipe, and it MAY include that recipe's own tables (scope/mode/parameter lookups, symptom→cause→fix inside a Common-Errors recipe, anti-pattern→correct inside an Anti-patterns recipe). The ONLY forbidden body table is a **cross-recipe decision/routing table** — one whose job is to select among recipes or techniques; that selection belongs in the cards. `## Anti-patterns` and `## Common Errors` are ordinary recipes (each with its own anchor and card); their tables are their own content and are allowed.

### B.5 Anchors

- Each recipe `##` is addressed by exactly one `[ref: #<anchor>]` marker; the marker text equals a card `anchor` with a leading `#`.
- Place markers per `{{ANCHOR_STYLE}}` (separate-line preferred); never mix styles within the skill.
- A section body runs from its marker to the next `[ref:]` marker or end of sub-section. Markers partition the file with no nesting and no bleed.

### B.6 Body section template

```
## <Recipe Heading>            # (+ inline [ref] if ANCHOR_STYLE=inline)

[ref: #{{ANCHOR_PREFIX}}-slug]  # omit this line if inline

<Lead prose: rule + core do/don't, defaults/edge cases, imperative.>

<Lead sentence for example 1:>

```<lang>
<self-contained realistic example>
```

Bad — <why it is wrong>:

```<lang>
<wrong form>
```

Good — <why it is right>:

```<lang>
<correct form>
```

**Variety booster:** <how to parametrize/extend so one body covers many cases>
```

---

## Part C — Code example idioms

Use `{{DOMAIN_IDIOMS}}`. For Python/pytest cards, follow the corpus style:

- Imports grouped stdlib → third-party, blank-line separated (`from collections.abc import Generator, Callable`; `from enum import StrEnum`; `import pytest`; `from faker import Faker`; `from pytest import CaptureFixture, LogCaptureFixture`).
- Tests annotated `-> None`, named `test_<unit>_<condition>_<expected>`, with a triple-quoted Given/When/Then docstring and AAA comments (`# --- Arrange ---`, `# --- Act ---`, `# --- Assert ---`).
- Test data via Faker only (no stdlib `random`); magic values lifted to named constants; categories via `StrEnum`/`IntEnum`; value objects via `@dataclass(frozen=True)`.
- Fixtures typed `Generator[X, None, None]` (teardown) / `-> X` (no teardown) / `Callable[..., T]` (factories); built-in fixtures typed (`capsys: CaptureFixture[str]`, `monkey: pytest.MonkeyPatch`, `request: pytest.FixtureRequest`).

For other domains, substitute that domain's idioms but keep the same discipline: imports shown, types shown, runnable shape, labeled contrasts.

---

## Procedure (follow in order)

1. **Decompose** `{{TOPIC}}` into recipes (one API / technique / decision each). Each recipe → one body `##` → one or more cards.
2. **Name** the file (`{{FILENAME}}`), choose `{{ANCHOR_PREFIX}}`, and draft each recipe's anchor slug.
3. **Write the cards first.** For each recipe, fill `what`/`problem`/`use_when`/`avoid_when`/`expected` so the card is fully self-contained. Put every WHEN/WHY/decision here. Use anchor repetition for convergence.
4. **Write `subject`** enumerating the recipe areas; add `libraries` if any.
5. **Write the body** per §B: lead prose → code → contrasts → variety booster, pure HOW, no routing/decision content, no tables.
6. **Verify anchor equality**: every card `anchor` has exactly one matching `[ref: #<anchor>]`; every body marker has a declaring card; markers partition cleanly.
7. **Self-check** with the list below. Fix every failure before finishing.

## Self-check (must all pass)

- Frontmatter top-level keys ⊆ `{subject, index, libraries}`; no `triggers`/`description`/`decisions`.
- `subject` follows the firm style: `<essence>; <keyword/API cloud>`, 30–50 words (≥3-letter tokens), no `a`/`the`, no tier marker, identifiers backticked; library/API names allowed in the cloud.
- Every card has exactly the six keys, each a non-empty (avoid_when/expected may be empty only for pure lookups) double-quoted sentence; backticks on every identifier/flag/value/version.
- Every `problem` follows the firm style: declarative **situation + stake** (not capability/goal/imperative), no solution API (→ `what`) and no success language (→ `expected`), 30–50 words (≥3-letter tokens), no `a`/`the`, and a concept/synonym-only keyword cloud with no Python commands or library names.
- Every decision/routing/selection fact is in a card; the body has none of it.
- Every body table is intra-recipe content, not a cross-recipe router; selection among recipes lives only in the cards. `## Anti-patterns`/`## Common Errors` (if any) carry their own anchor and card.
- Anchors kebab-case `<prefix>-<slug>`, consistent prefix; card `anchor` == body `[ref: #anchor]`; convergence expressed by repeating anchors; markers partition the file (no nesting/bleed).
- One anchor-placement style throughout; one variety-booster style throughout.
- Exactly one `#` H1; recipes are `##`; code fences are language-tagged and self-contained; lead sentences end in a colon; contrast pairs labeled Bad/Good or Wrong/Correct.
- `libraries` (if present) lowercase, extras preserved, significant pins kept; omitted if none.

<END PROMPT>
