# api-design

Enforces Google AIP rules when you design or review resource-oriented APIs.

## What it does

This skill gives you a binding, Google AIP-driven reference for resource-oriented API design.
It covers resource naming, parent-child relationships, standard and custom operations, field design, pagination, filtering, field masks, soft delete, ETags, compatibility, versioning, deprecation, naming conventions, documentation, errors, retry configuration, and Protocol Buffers API structure.
Use it to keep REST, gRPC, OpenAPI, Swagger, and GraphQL designs consistent with Google's API Improvement Proposals.

## When it activates

Activates when you ask about API design, resource modeling, URL schemes, method definitions, Google AIP compliance, or API versioning.
Examples:
- "Review this API design"
- "Is this resource name AIP-compliant?"
- "How should I model batch operations?"
- "Design a gRPC API for orders and order items"

## How to use it

Ask the agent to design or review your API.
Place your `.proto`, OpenAPI, or schema files in the repo so the agent can inspect them.
The agent will apply the AIP rules automatically and route any `.proto` file questions to the `protobuf-lang` skill for Buf lint and schema style.
No manual skill loading is required.

## What it produces

- AIP-compliant API designs and design reviews.
- Corrected resource names, routes, request/response shapes, field semantics, and error behavior.
- For `.proto` files, coordination with `protobuf-lang` for Buf lint and schema style.

## Repository layout

```text
api-design/
├── prompts/
│   └── REFERENCE_STANDARD_ADDENDUM.md  # Skill-specific presentation choices, defers to the cross-skill standard
├── references/           # AIP reference sections with routing frontmatter, plus authoritative RFC verbs
│   ├── 01_foundation_and_process.md
│   ├── 02_design_review.md
│   ├── 03_api_concepts.md
│   ├── 04_resource_design.md
│   ├── 05_operations.md
│   ├── 06_fields.md
│   ├── 07_design_patterns.md
│   ├── 08_compatibility_and_versioning.md
│   ├── 09_polish.md
│   ├── 10_protocol_buffers.md
│   └── rfc_verbs.md
└── SKILL.md              # Agent entry point: manifest, triggers, and the lazy-load routing funnel
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/01_foundation_and_process.md` | AIP purpose, numbering, versioning, precedent, style, and glossary |
| `references/02_design_review.md` | Design review FAQ and beta-blocking changes |
| `references/03_api_concepts.md` | Management vs data planes and declarative clients |
| `references/04_resource_design.md` | Resource orientation, names, types, associations, enumerations, singletons |
| `references/05_operations.md` | Standard, batch, custom, and long-running operations |
| `references/06_fields.md` | Field names, behavior, quantities, time, codes, repeated fields, ranges |
| `references/07_design_patterns.md` | Jobs, import/export, ETags, pagination, filtering, field masks, soft delete |
| `references/08_compatibility_and_versioning.md` | Backwards compatibility, stability levels, and API versioning |
| `references/09_polish.md` | Naming, file structure, documentation, errors, and retry configuration |
| `references/10_protocol_buffers.md` | HTTP/gRPC transcoding, common components, and API-specific protos |
| `references/rfc_verbs.md` | Definitions of `MUST`, `MUST NOT`, `SHOULD`, `MAY`, etc. |

## How the agent loads references

Each reference file opens with YAML frontmatter: a `subject` line naming the chapter and its section areas, an `index` of decision cards (one selection gate per section), and an `aips` list of covered AIP numbers. The agent routes in three steps without reading whole files:

1. **Subject map** — one coarse routing line per file (Command 1 of the canonical funnel).
2. **Frontmatter dump** — the full frontmatter of the shortlisted files only (Command 2); the agent matches every card's `what`/`use_when`/`avoid_when` semantically against the request and marks anchors (duplicates converge on one section).
3. **Bounded extraction** — each chosen section is read exactly from its `[ref: #<anchor>]` marker to the next marker.

The exact commands and routing rules live in `frontmatter-protocol` `[ref: #lazy-load-routing]` (referenced from `SKILL.md` §2); the normative format lives in `frontmatter-protocol/references/lazyload.md` with api-design specifics in `prompts/REFERENCE_STANDARD_ADDENDUM.md`.

## Important conventions / gotchas

- Requires the `read-for-comments` and `protobuf-lang` skills.
- Reference files MUST NOT be read in full; routing goes through frontmatter cards only.
- After editing any reference frontmatter, run `uv run --no-project --with pyyaml python frontmatter-protocol/scripts/validate_frontmatter.py --aips references/<FILE>.md` from the workspace root — it MUST pass.
- This skill enforces AIP resource-design rules; it does not handle Buf lint or raw `.proto` schema style.
- Buf lint and `.proto` style questions are handled by `protobuf-lang`.
- Requirement verbs follow RFC 2119 / RFC 8174.
