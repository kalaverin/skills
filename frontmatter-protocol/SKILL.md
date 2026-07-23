---
name: frontmatter-protocol
description: "MANDATORY core standard for frontmatter (the file шапка / header): what it is, why it exists, how to write it, how to read it. Owns the extension mechanism, the lazy-load routing mechanics (core §7), and four extensions: include (skill-frontmatter evaluation, boot-mandatory), tracking (git document tracking), lazyload (reference-card authoring; runtime-mandatory the moment session work touches skills or their references), offline (offline index/manifest building). Every skill, memory, or document that carries a YAML frontmatter conforms to this protocol."
triggers:
  always: true
  reason: "Every skill header, reference file, and Serena memory carries a frontmatter; this protocol is the single standard governing all of them."
runtime: true
requires:
  - markdown-protocol
version: 0.1.0
---

# SKILL: Frontmatter Protocol (Core Standard)

This skill is the single normative source for everything a frontmatter is and does.
A frontmatter (synonyms: **header**, Russian: **шапка файла** — never "заголовок") is the machine-readable YAML block at the very start of a file.
This document is the CORE: it is always read whole.
Its four extensions live in `references/` and add their own key sets and algorithms on top of the core rules.

Normative keywords (`MUST`, `SHOULD`, `MAY`) follow RFC 2119 / RFC 8174 (by `read-for-comments` skill).

## 1. BOOT HARD GATE (read this first)

[ref: #fm-boot-gate]

If you are an agent reading this text, you MUST **immediately load `references/include.md` WHOLE** and apply its algorithms before evaluating any other skill's frontmatter.
The boot chain is: system prompt → `bootstrap` (the Startup Gate it owns) → this `SKILL.md` → `references/include.md` → evaluation of all other skills' headers.
Only include is always loaded (it evaluates every skill header); the lazy-load routing mechanics needed to CONSUME reference corpora live in this core (§7); tracking, lazyload, and offline load per the registry (§8).

## 2. What a Frontmatter Is and Why

[ref: #fm-what-is]

- A frontmatter is a YAML mapping placed at the **very beginning** of a file, delimited by an opening line `---` and a closing line `---`.
- It is the file's **machine-readable layer**: it exists so an agent can route (decide what to load), track (decide whether content is stale), and evaluate (decide whether a skill applies) **without reading the body**.
- The body below the frontmatter is the human/prose layer. What the body looks like (its H1, headings, typography) is governed by `markdown-protocol`, not by this protocol.
- Three consumer domains exist today: skill entry points (`SKILL.md`), lazy-loaded reference corpora (`references/**/*.md`), and Serena memory files. All three conform to this core; each adds an extension.

## 3. Envelope Grammar (binding)

[ref: #fm-envelope]

1. The opening delimiter MUST be the **first line** of the file: exactly `---` (trailing whitespace tolerated, nothing else).
2. The YAML block follows: a single YAML **mapping** (keys → values), parseable by a standard YAML parser, encoded in UTF-8.
3. The closing delimiter MUST be a line containing exactly `---` (same tolerance).
4. Exactly **one** frontmatter block per file. Nothing precedes the opening delimiter — no blank lines, no comments, no BOM-driven content.
5. The core mandates **no keys**. Every key a file carries comes from an active extension (§8, §9) or from declared extras.

## 4. The Delimiter Law (binding)

[ref: #fm-delimiter-law]

- Delimiters MUST be matched as **anchored whole lines**: regex `^---[ \t]*$` (in awk: `/^---[ \t]*$/`).
- You MUST NEVER split a file on the bare substring `---`. Bodies legitimately contain `---` inside code, comments, and horizontal rules; a naive split truncates the frontmatter and produces false YAML errors.
- This law applies to every reader: shell one-liners, scripts, validators, and manual extraction alike.

## 5. How to Write (binding)

[ref: #fm-write-rules]

1. The YAML MUST parse cleanly with a standard parser. If it does not parse, the file is non-conformant, period.
2. The key set is **closed**: a file carries only the keys of its active extensions plus extras declared through the mechanism in §9. No stray keys, no commented-out keys, no "just in case" keys.
3. Scalar style is plain YAML; extensions MAY tighten it (e.g. lazyload requires double-quoted one-sentence strings).
4. Keep the frontmatter a pure metadata layer: no prose paragraphs, no markdown, no instructions that belong in the body.

## 6. How to Read (binding)

[ref: #fm-read-primitive]

Extract the frontmatter without opening the body, using the delimiter law. Two canonical forms — the ONLY sanctioned dialect:

**Form 1 — explicit file list:**

```bash
for f in "<FILE-1>" "<FILE-2>" ...; do printf '\n### %s\n' "$f"; awk '/^---[ \t]*$/{c++; if(c==2) exit; next} c==1{print}' "$f"; done
```

**Form 2 — dynamic file list** (while-read feeder; `LC_ALL=C` for byte-deterministic ordering; safe for paths with spaces):

```bash
fd <FD-ARGS> 2>/dev/null | LC_ALL=C sort -u | while IFS= read -r f; do printf '\n### %s\n' "$f"; awk '/^---[ \t]*$/{c++; if(c==2) exit; next} c==1{print}' "$f"; done
```

- These two forms are the ONLY sanctioned dialect. Deprecated legacy variants: `xargs` wrappers (nested quoting, empty-input quirks on BSD), `$(...)` command-substitution feeders (word-splitting), and looser awk patterns such as `/^---$/` (violates the delimiter law).
- Documented limits: line-based feeders cannot handle filenames containing newlines (impossible in conformant workspaces; NUL-based variants are rejected — `sort -z` and `read -d` are not portable to macOS/BSD). `fd` prints an error for missing directory arguments but continues with the valid roots — `2>/dev/null` covers absent optional roots.
- Extensions build their loaders on top of these primitives (e.g. the §7 funnel, include's skill-discovery extraction).

## 7. Lazy-Load Routing (Loader Mechanics)

[ref: #lazy-load-routing]

This section is the COMPLETE instruction set for **consuming** a conformant reference corpus (`references/**/*.md` carrying `subject`+`index` frontmatter per the lazyload extension). Authoring or validating such corpora requires the lazyload extension (§8) — a reader needs only this section.

**Mental model.** A reference file is read in two stages: (1) **routing** — decide from frontmatter alone WHICH sections to load; (2) **loading** — read only the selected `[ref: #<anchor>]` sections. Never read a whole reference file to decide relevance.

**Card anatomy (reader's view).** `subject` is the file-level coarse router: one line naming every section area of the file. `index` is a flat list of decision cards; each card gates ONE body anchor and carries `what` / `problem` / `use_when` / `avoid_when` / `expected`. Several cards MAY share one anchor (convergence) — load the shared section once.

**Command 1 — subject map** (coarse routing, one line per file; awk instead of sed — BSD sed does not interpret `\t` in replacements):

```bash
rg -N -H '^subject:' references/ | awk '{sub(/:subject:[[:space:]]*/,"\t"); print}' | LC_ALL=C sort
```

**Command 2 — full frontmatter of shortlisted files only** (the §6 primitives: Form 1 for an explicit list, Form 2 for a dynamic one).

**Routing rules:**

1. Shortlist candidate files from the subject map using `subject` plus the request **plus inferred session work**; shortlist generously.
2. Within shortlisted frontmatter, read **every** card and match `what`/`use_when`/`avoid_when` semantically (OR semantics within and across files). Mark each matching card's `anchor`.
3. **Deduplicate** anchors (convergence), then load each section.
4. Routing stays in the **main agent**: subagents receive already-selected material.

**Markers and load boundary.** A routable section opens with the literal marker line `[ref: #<anchor>]` at column 0 and runs to the next marker **outside fenced code blocks** or end of file. Bounded section extraction (fence-aware, anchor matched as an exact string — never a blind `rg -A N` window):

```bash
awk -v a="<ANCHOR>" '/^```/{fence=!fence;if(f)print;next} !fence&&$0=="[ref: #"a"]"{f=1;print;next} !fence&&f&&/^\[ref: #/{exit} f' references/<FILE>.md
```

Multi-anchor extraction from one file (one pass per anchor, labeled output):

```bash
for a in <A1> <A2> ...; do printf '\n### [ref: #%s]\n' "$a"; awk -v a="$a" '/^```/{fence=!fence;if(f)print;next} !fence&&$0=="[ref: #"a"]"{f=1;print;next} !fence&&f&&/^\[ref: #/{exit} f' references/<FILE>.md; done
```

(When the anchor id is needed first, the marker index is `rg -n '^\[ref: #' references/<FILE>.md`.)

## 8. Extension Registry

[ref: #fm-extension-registry]

| Extension | File | Activation (implicit-by-keys) | Load when |
|---|---|---|---|
| **include** | `references/include.md` | boot-mandatory (§1) | Always — it evaluates every other skill's header. |
| **tracking** | `references/tracking.md` | any of `repo`, `branch`, `commit`, `committed_at`, `stale_since` | Reading/writing documents with git-tracking fields (Serena memories, user markdowns). |
| **lazyload** | `references/lazyload.md` | `subject` and/or `index` | **Runtime-mandatory on skill work:** the moment the agent realizes the task touches skills at all — authoring or editing a `SKILL.md`, its `references/**` corpus, skill frontmatter, or skill tooling — it MUST load this extension BEFORE the first write. Also mandatory for authoring or validating any reference corpus (writing cards, migrating, running the validator). Pure §7 consumption of a corpus needs only the core. |
| **offline** | `references/offline.md` | — (algorithmic, no keys) | Building an offline index/manifest over a frontmatter corpus. |

## 9. Extension Mechanism (binding)

[ref: #fm-extension-mechanism]

1. **Implicit activation by keys.** Seeing an extension's keys in a frontmatter activates that extension's full rule set for the file. No explicit opt-in key is required; existing documents conform unchanged.
2. **Validator expectation (planned).** The validator (`scripts/validate_frontmatter.py`) is planned to accept `--expect-extension <name>` to hard-require an extension: it will then error on incomplete or contradictory extension field sets (e.g. `branch` without `commit`). Until the flag lands (tracked in the project backlog), only the lazyload profile is enforced mechanically; the other extensions conform editorially.
3. **Skill-declared extras.** A skill MAY declare additional top-level keys for its own files. Every extra key MUST be declared and documented in that skill's `SKILL.md` (see lazyload §2 for the reference-corpus case).
4. Extensions MUST NOT contradict the core. A skill addendum MUST NOT contradict an extension it uses.

## 10. Conformance and Validator

[ref: #fm-conformance]

- The reference validator is `scripts/validate_frontmatter.py` (run with `uv run --no-project --with pyyaml python`). It currently implements the **lazyload** profile; `tracking` and `include` profiles are planned growth (recorded in the project backlog).
- A file is conformant when: the envelope grammar (§3) holds, the delimiter law (§4) was used to read it, its key set is closed per §9, and every active extension's rules pass.

**Violation protocol:** If you read or write a frontmatter while violating the envelope grammar, the delimiter law, the closed key set, or the boot hard gate, halt immediately, discard the offending operation, reload the violated section, and redo the operation correctly.
