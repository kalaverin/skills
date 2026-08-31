# feature-archival

[ref: #fa-readme-intro]

Closes a completed feature in Serena memory: extracts everything of value from its cross-scope footprint, compresses it into an authored archive record, and deletes the originals — recoverably.

## What it does

[ref: #fa-readme-what]

When a feature has shipped to production and you close it, this skill runs a codified pipeline: it builds a full inventory of the feature's memory footprint (listing + agent judgment + keyword ripgrep, classed as produced-by / touched-by / mention-only), gets your approval, fans extraction out to context-budgeted subagents, synthesizes a flat `archive/<feature>/` record (`summary.md` + `decisions.md` + `future.md`, plus an additive free tree), verifies it with a dedicated reconciliation pass (completeness, chronology, supersession), and only then — after your explicit master approval — deletes the originals. The record's `archived_from_commit` is the last commit where the files still existed, so everything is restorable from git at that commit directly.

## When it activates

[ref: #fa-readme-when]

Only on your explicit closing command («закрываем фичу X», "archive feature X"). Never automatically, never by heuristic.

## Layout

[ref: #fa-readme-layout]

```text
feature-archival/
├── README.md   # Human overview (this file)
└── SKILL.md    # Agent entry point: the full archival pipeline contract
```

## Design record

[ref: #fa-readme-design]

Designed via discuss-first; the complete approval trail and decision forks live in Serena memory: `solutions/project/feature_archival_pipeline/`.
