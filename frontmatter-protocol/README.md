# frontmatter-protocol
[ref: #frontmatter-protocol]

The single normative standard for frontmatter (the file header) across skills, reference corpora, and Serena memories.

## What it does
[ref: #frontmatter-protocol-purpose]

This skill defines what a frontmatter is, why it exists, how to write it, and how to read it.
The core (`SKILL.md`) owns the envelope grammar, the delimiter law, and the lazy-load routing mechanics; four extensions add their own key sets and algorithms on top:

- **include** (`references/include.md`) — skill header schema, closed trigger grammar, discovery/evaluation algorithms, and the boot contract. Always loaded at startup.
- **tracking** (`references/tracking.md`) — git document tracking fields (`repo`, `branch`, `commit`, `committed_at`, `stale_since`) and the staleness/reconciliation protocol.
- **lazyload** (`references/lazyload.md`) — reference-file authoring standard with `subject` + `index` decision cards and `[ref: #<anchor>]` markers. Loaded when authoring or validating a reference corpus.
- **offline** (`references/offline.md`) — offline index/manifest building over a frontmatter corpus.

## When it activates
[ref: #frontmatter-protocol-activation]

Always active.
The system prompt force-loads it; its boot hard gate then loads the include extension, which governs how every other skill's header is evaluated.

## How to run / use it
[ref: #frontmatter-protocol-usage]

1. When authoring a `SKILL.md`, add a frontmatter with the closed key set: `name`, `description`, `triggers`, and optionally `requires`, `runtime`, `version`, or `draft`.
2. When authoring a reference corpus, load the lazyload extension and use `subject` plus `index` decision cards; align each card anchor with a `[ref: #<anchor>]` marker in the body.
3. When writing tracked memories, include the tracking field set and refresh it on every mutation.
4. To validate a lazyload reference file, run `uv run --no-project --with pyyaml python frontmatter-protocol/scripts/validate_frontmatter.py`.
5. Extract frontmatter only with the canonical awk one-liners from core §6; never split a file on the bare substring `---`.

## What it produces
[ref: #frontmatter-protocol-artifacts]

- One hard standard every frontmatter-carrying file conforms to.
- A canonical validator (`scripts/validate_frontmatter.py`, lazyload profile today; tracking and include profiles planned).
- Orchestration prompts for reference-corpus migration and card authoring.
- Stable machine-readable routing without reading document bodies.

## Dependencies and why they matter
[ref: #frontmatter-protocol-dependencies]

- `markdown-protocol` — provides the Markdown authoring rules, the headings-as-API standard, marker placement, the UTC ISO 8601 date rule, and the `errata` conformance queue that every frontmatter-carrying file must obey.
- `python` + `pyyaml` (runtime tools) — used by `scripts/validate_frontmatter.py` to validate reference-file frontmatter.

## Strengths and trade-offs
[ref: #frontmatter-protocol-tradeoffs]

- Strong sides: one standard for three consumer domains (skill entry points, reference corpora, Serena memories); extension model keeps key sets closed; canonical extraction commands avoid ad-hoc parsing.
- Weak sides / limits: the validator currently implements only the lazyload profile; tracking and include profiles are planned but not yet enforced mechanically.
- Common pitfalls / gotchas: the closing `---` delimiter is matched as an anchored whole line; never split on the bare substring `---`. Extensions activate implicitly by their keys; a skill header with `draft: true` is ignored entirely. Bare `fd` is forbidden as a `files` trigger probe.

## Repository layout
[ref: #frontmatter-protocol-layout]

```text
frontmatter-protocol/
├── prompts/
│   ├── CARD_AUTHORING.md              # Generalized prompt for authoring one reference card
│   └── REFERENCE_MIGRATION_PROMPT.md  # Six-phase orchestration prompt for standardizing a corpus
├── references/
│   ├── include.md                     # Skill header schema, trigger grammar, discovery/eval, boot contract
│   ├── lazyload.md                    # Reference-file card standard and loader contract
│   ├── offline.md                     # Offline index/manifest building algorithm
│   └── tracking.md                    # Git document tracking and staleness protocol
├── scripts/
│   ├── validate_frontmatter.py        # Canonical conformance validator (lazyload profile)
│   └── validate_memory_stub_port.py   # Memory stub-port validator
├── README.md                          # Human overview (this file)
└── SKILL.md                           # Core standard: envelope, delimiter law, extension mechanism, boot gate
```

## Reference overview
[ref: #frontmatter-protocol-references]

| File | What it covers |
|------|----------------|
| `references/include.md` | Skill header schema, closed trigger grammar, discovery/evaluation pipeline, transitive `requires` resolution, runtime re-evaluation, and the boot contract. |
| `references/lazyload.md` | Reference-file authoring standard: `subject` coarse router, `index` decision cards, anchor markers, card style rules, and the conformance checklist. |
| `references/tracking.md` | Git document tracking fields, staleness detection, reconciliation ladder, refresh-on-mutation, and timestamp semantics. |
| `references/offline.md` | Algorithm for building a pinned offline index over a frontmatter corpus: harvest, fan-out, validation, and manifest. |

## Important conventions / gotchas
[ref: #frontmatter-protocol-gotchas]

- A frontmatter is the file header (Russian: шапка файла) — never "заголовок".
- Delimiters are matched as anchored whole lines (`^---[ \t]*$`); never split on the bare substring `---`.
- Extensions activate implicitly by their keys; the validator can hard-require one with `--expect-extension` (planned).
- A skill header carrying `draft: true` is invisible to discovery and evaluation.
- What follows the frontmatter (H1, headings, markers) is owned by `markdown-protocol`.
