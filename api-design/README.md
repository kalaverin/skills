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
├── references/           # AIP reference sections and authoritative RFC verbs
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
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
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

## Important conventions / gotchas

- Requires the `read-for-comments` and `protobuf-lang` skills.
- This skill enforces AIP resource-design rules; it does not handle Buf lint or raw `.proto` schema style.
- Buf lint and `.proto` style questions are handled by `protobuf-lang`.
- Requirement verbs follow RFC 2119 / RFC 8174.
