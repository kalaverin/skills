# frontmatter-protocol

The single normative standard for frontmatter (the file шапка / header) across all skills, reference corpora, and Serena memories.

## What it does

This skill defines what a frontmatter is, why it exists, how to write it, and how to read it.
The core (`SKILL.md`) owns the envelope grammar, the delimiter law, and the lazy-load routing mechanics (§7); four extensions add their own key sets and algorithms:

- **include** (`references/include.md`) — skill header schema, closed trigger grammar, discovery and evaluation algorithms, boot contract. Boot-mandatory.
- **tracking** (`references/tracking.md`) — git document tracking: `repo`/`branch`/`commit`/`committed_at` fields, `stale_since` staleness protocol, reconciliation ladder.
- **lazyload** (`references/lazyload.md`) — reference-card authoring standard: `subject` + `index` decision cards, firm styles, dedup, anchor authoring, conformance checklist. Loaded lazily for authoring/validation; reading a corpus needs only core §7.
- **offline** (`references/offline.md`) — offline index/manifest building over a frontmatter corpus (harvest → fan-out → validation → pinned manifest).

## When it activates

Always active.
The system prompt force-loads it; its boot hard gate then loads the include extension, which governs how every other skill's header is evaluated.

## How to use it

You do not invoke it directly.
Any time you author or read a file with a YAML frontmatter — a `SKILL.md`, a reference file, a Serena memory — the rules of this protocol apply.
Load the specific extension when working in its domain (e.g. load `lazyload` when authoring reference cards, `tracking` when writing memories).

## What it produces

- One hard standard every frontmatter conforms to.
- A canonical validator (`scripts/validate_frontmatter.py`, lazyload profile; tracking/include profiles planned).
- Orchestration prompts: reference corpus migration and card authoring.

## Repository layout

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
│   └── validate_frontmatter.py        # Canonical conformance validator (lazyload profile)
└── SKILL.md                           # Core standard: envelope, delimiter law, extension mechanism, boot gate
```

## Important conventions / gotchas

- A frontmatter is a header (Russian: шапка файла) — never a "заголовок".
- Delimiters are matched as anchored whole lines (`^---[ \t]*$`); never split on the bare substring `---`.
- Extensions activate implicitly by their keys; the validator can hard-require one with `--expect-extension` (planned).
- A skill header with `draft: true` is ignored by loaders — it is purely in development.
- What follows the frontmatter (H1, marker typography) is markdown-protocol's domain.
