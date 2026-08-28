# read-for-comments
[ref: #rfc-intro]

Local standards library and archival rule for technical standards and specifications.

## What it does
[ref: #rfc-what]

This skill is a standards archive and lookup procedure, not a code skill. It maintains two stores:

1. **Archive (searched FIRST):** Serena memories at `standard/<family>/<family>_<id>.md` — every standard ever fetched for this project.
2. **Seed (searched SECOND):** this skill's `references/` directory — a tiny curated set of frequently needed standards that travels with the skill mirror.

Before fetching a standard from the internet, the agent checks the archive first and the seed second. If a standard body is missing, the agent fetches it, then archives it according to the event-bound rule.

## When it activates
[ref: #rfc-when]

Activates whenever the agent needs to cite, fetch, or archive a technical standard, specification, or authoritative document.

Examples:

- You ask a question that requires citing an RFC, ISO standard, OWASP guideline, Google style guide, or similar.
- The agent needs a standard as context for a review, audit, or design decision.
- A downloaded standard must be archived locally.

## How to run / use it
[ref: #rfc-how]

If a standard is needed, the agent first searches the Serena `standard/` archive (`list_memories topic=standard` or a path probe), then this skill's `references/` seed.
If the standard is found locally, the agent uses it.
If it is missing, the agent fetches it from the authoritative source, archives it under `.serena/memories/standard/<family>/<family>_<id>.md`, and updates the manifest.
Large standards are split into logical chapters or sections and stored as separate files.
You do not need to manage the archive manually.

## What it produces
[ref: #rfc-produces]

- `read-for-comments/references/<standard>.md` files for seeded standards.
- `standard/<family>/<family>_<id>.md` memory entries for archived standards.
- Manifests that list each standard's title, version, canonical URL, and archival path.

## Dependencies and why they matter
[ref: #rfc-deps]

- `frontmatter-protocol` — provides the frontmatter conventions used by manifests and archived standards.
- `serena-protocol` — governs memory naming, formatting, and persistence for standards archived in the `standard/` namespace.
- `kagi-search` — used for the actual web fetch when both local stores miss.

## Strengths and trade-offs
[ref: #rfc-tradeoffs]

### Strong sides
[ref: #rfc-strong]

- Prevents repeated internet fetches for the same standard.
- Keeps authoritative sources under source control.
- Manifests make it easy to see which standards are available and how recent they are.

### Weak sides / limits
[ref: #rfc-weak]

- Requires discipline: the agent checks local archives before every external fetch.
- Large standards can be tedious to split and archive.
- Seeding is manual; the skill does not auto-populate the archive.

### Common pitfalls / gotchas
[ref: #rfc-pitfalls]

- Check the Serena `standard/` archive first, then this skill's `references/` seed, and only then go to the web.
- Archive the standard body after download rather than leaving it in a temporary file.
- Use the exact family name from the registered list: `rfc`, `std`, `bcp`, `pep`, `aip`, `owasp`, `w3c`, `whatwg`, `zmpc`, `cwe`, `wicg`. New families are proposed to the user before first use.
- Multi-chapter standards are split into one file per chapter.
- When citing, include the section number and the stable URL.
- `kagi_summarizer` output is a derivative and is not archived; the full body is archived instead.

## Repository layout
[ref: #rfc-layout]

```text
read-for-comments/
├── references/           # Local standards seed
│   ├── rfc2119.md
│   └── rfc8174.md
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: lookup gate, fetch/archival rules, family registry
```

## Important conventions / gotchas
[ref: #rfc-conventions]

- This is a knowledge workflow, not a code tool.
- The archive is checked first, the seed second, the web last.
- Every download must be archived event-bound.
- Large standards are split by chapter and tracked in a manifest.
- Cite by section and stable URL.
