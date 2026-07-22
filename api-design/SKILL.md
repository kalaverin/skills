---
name: api-design
description: >
  MANDATORY skill for Google AIP API resource design and compliance. Covers
  resources, operations, fields, design patterns, compatibility, polish, and
  proto API structure. For Buf lint and proto schema style, use the
  protobuf-lang skill.
triggers:
  request: "openapi, swagger, graphql, grpc, rest, api design, fastapi, flask"
requires:
  - read-for-comments
  - protobuf-lang
---

# SKILL: Strict API Design & Compliance (Google AIP)

You are an expert API Architect. **This document is a binding rule set, not a recommendation.**
Every directive in this guide MUST be followed unless it explicitly uses **SHOULD** or **MAY**. The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when they appear in all capitals or in bold markup.

## 1. Compliance and Default Rules

* **Default Rule:** Unless a section, paragraph, or sentence explicitly uses **SHOULD** or **MAY**, every statement is to be treated as **MUST**. You MUST NOT apply external style preferences or general API-design heuristics in place of the rules documented here.
* **Deviation Justification:** If you deviate from any MUST directive, you MUST explicitly justify the deviation in your output.
* **Skill Boundary:** This skill enforces Google AIP resource-design rules (resources, operations, fields, patterns, compatibility, polish, and proto API structure). For Buf lint and proto schema style, consult the `protobuf-lang` skill.
* **RFC Verbs:** For precise semantics of requirement-level verbs, consult the `read-for-comments` skill.

## 2. Reference Corpus and Lazy-Load Protocol (CRITICAL)

The `references/` corpus is extremely large (7,300+ lines across 11 files). You **MUST NOT** read reference files in full, load them into context indiscriminately, or summarize the collection. Every reference file opens with YAML frontmatter — a `subject` line (file-level coarse router) plus an `index` of decision cards (each card is the selection gate for ONE body section) — and every routable body section is addressed by a `[ref: #<anchor>]` marker. You MUST route through the frontmatter, never through full-body reads.

### 2.1 The Two-Command Routing Funnel

Run both commands (and the extraction in §2.3) **from the skill directory** — the directory containing this SKILL.md — so that the relative `references/` path resolves. If the session working directory is fixed elsewhere, prefix every `references/` path with the skill directory path.

**Command 1 — subject map** (coarse routing, one line per file):

```bash
rg -N -H '^subject:' references/ | sed -E 's/:subject:[[:space:]]*/\t/'
```

**Command 2 — full frontmatter of shortlisted files only** (`<FILE-1> … <FILE-n>` are the chosen paths):

```bash
for f in "<FILE-1>" "<FILE-2>" ...; do printf '\n### %s\n' "$f"; awk '/^---[ \t]*$/{c++; if(c==2) exit; next} c==1{print}' "$f"; done
```

### 2.2 Semantic Routing Rules

Routing is **semantic and context-aware**, never substring/keyword matching:

1. Shortlist candidate files from the subject map using `subject` plus the request **plus inferred session work** (the artifact you are about to produce, the questions the problem implies). Shortlist generously — when uncertain, expand the file list and re-run Command 2.
2. Within shortlisted frontmatter, read **every** card and match `what`/`use_when`/`avoid_when` semantically (OR semantics within and across files). Mark each matching card's `anchor`.
3. **Deduplicate** anchors: several cards MAY share one anchor (convergence); load the shared section once.
4. Routing stays in the **main agent**: inferred session context cannot be serialized to a subagent without loss. Subagents receive already-selected material.
5. Cross-references inside card fields point to better alternatives: `(sibling card)` = another card for the same anchor in the same file; `(<NN>_<name> › <topic>)` = a section in the named corpus file (e.g. `(07_design_patterns › soft delete)`).

### 2.3 Bounded Section Extraction (MANDATORY)

Never use a blind fixed window like `rg -A 100` — it truncates large sections and over-reads small ones. Extract exactly from the target marker to the next marker:

```bash
awk '/^\[ref: #<ANCHOR>\]$/{f=1;print;next} f&&/^\[ref: #/{exit} f' references/<FILE>.md
```

When the anchor id is needed first, `rg -n '^\[ref: #' references/<FILE>.md` lists all marker line numbers.

**Frontmatter extraction warning:** match delimiters as anchored whole lines (`^---\s*$`; in awk: `^---[ \t]*$`). Never split on the bare substring `---` — bodies legitimately contain `---` inside code, and a naive split truncates the frontmatter with false YAML errors.

### 2.4 Frontmatter Schema Notes

- Top-level keys: `subject`, `index`, `aips` (skill-extra, below). Cards carry exactly `{anchor, what, problem, use_when, avoid_when, expected}`.
- `aips` — **api-design skill-extra field** (declared per the cross-skill reference standard, `bootstrap/references/REFERENCE_STANDARD.md` §2): a sorted list of the AIP numbers covered by the file, mechanically cross-checked against body section headings. Use it for coarse filtering when the request cites an AIP number directly.
- `avoid_when` and `expected` are empty only for pure lookup sections (Glossary, RFC verbs) that have no anti-pattern and no success state.
- The normative frontmatter schema, card semantics, and conformance checklist live in `bootstrap/references/REFERENCE_STANDARD.md`; api-design presentation choices live in `prompts/REFERENCE_STANDARD_ADDENDUM.md`.

## 3. Master Execution Workflow

1. **Analyze Design Task:** Identify the API component (resource, method, field, relationship, error model, etc.) you are creating or reviewing.
2. **Route via the Funnel:** Run Command 1, shortlist generously, run Command 2, and select cards semantically (§2.2). Load `references/rfc_verbs.md` (anchor `rfc-verbs`) first if any requirement-level verb is ambiguous.
3. **Extract Rules:** For each selected anchor, run the bounded extraction (§2.3) and read only that section. Do not load full reference files into context.
4. **Apply Rules:** Draft or review routes, resource names, request/response shapes, field semantics, and error behavior so that every element complies with the extracted AIP section.
5. **Proto Review (if applicable):** If the change touches `.proto` files, invoke the `protobuf-lang` skill for Buf lint and proto schema style. Do not duplicate those rules here.
6. **Verify:**
   - Confirm every route, method, field, and resource mentioned in the design complies with the extracted AIP section.
   - Confirm no contradictions exist between referenced sections.
   - Confirm any `.proto` changes were reviewed with `protobuf-lang`.
   - Confirm no unmodified files were changed.
