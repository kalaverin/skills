# api-design

Agent skill that codifies the Google API Improvement Proposal (AIP) standards for resource-oriented API design.

## What this skill does

`api-design` provides a binding rule set and a lazy-load routing index for designing and reviewing:

- Resources, resource names, and parent-child relationships.
- Standard and custom operations.
- Field design, field behavior, and common types.
- Design patterns such as soft delete, optimistic concurrency, pagination, long-running operations, and ETags.
- API compatibility and versioning policies.
- Polish: canonical errors, localized messages, and help metadata.
- Protocol Buffers API structure (`proto3`, `google.api.http`, `google.api.resource`, `google.api.field_behavior`, `google.longrunning.Operation`, `google.rpc.Status`).

The skill is consumed by other agents during API design and code-review tasks. It does not run as a service and contains no executable code.

## When to use it

Load this skill when the request involves:

- OpenAPI, Swagger, REST, or gRPC API design.
- Resource modeling, URL schemes, or API methods.
- Google AIP compliance checks.
- API review, polish, or compatibility decisions.

> **Boundary:** Buf lint and raw proto schema style live in the sibling `protobuf-lang` skill. Use `protobuf-lang` for `.proto` file linting and `buf.yaml` configuration questions.

## Repository layout

```text
api-design/
├── references/           # AIP reference sections and authoritative RFC texts
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
└── SKILL.md              # Skill entry point with lazy-load routing index
```

## How to use this skill

1. Open `SKILL.md` first. It contains the YAML manifest, trigger conditions, and the routing index.
2. Find the relevant topic in the routing index.
3. Extract only the referenced section from `references/*.md` using the `[ref: #...]` anchor.
4. Apply RFC 2119 / RFC 8174 requirement verbs (`MUST`, `SHOULD`, `MAY`) as defined in `references/rfc_verbs.md`.

## Reference index

| File | Topic |
|------|-------|
| `references/01_foundation_and_process.md` | Resource-oriented design and design process |
| `references/02_design_review.md` | Design review checklist and gate |
| `references/03_api_concepts.md` | API concepts and terminology |
| `references/04_resource_design.md` | Resource naming, parent-child, soft delete, DNS compatibility |
| `references/05_operations.md` | Standard methods, custom methods, and mutations |
| `references/06_fields.md` | Field types, formats, UUID/IP standards, field behavior |
| `references/07_design_patterns.md` | ETags, pagination, long-running operations, common flows |
| `references/08_compatibility_and_versioning.md` | Breaking vs non-breaking changes, versioning policy |
| `references/09_polish.md` | Canonical errors, `google.rpc.Status`, help and localized messages |
| `references/10_protocol_buffers.md` | Proto package, message, service, and method conventions |
| `references/rfc_verbs.md` | Definitions of `MUST`, `MUST NOT`, `REQUIRED`, `SHOULD`, etc. |
| `read-for-comments` skill | Authoritative RFC 2119 and RFC 8174 texts |

## Conventions

- `SKILL.md` is the single entry point; reference sections are lazy-loaded.
- Requirement verbs follow RFC 2119 / RFC 8174 (BCP 14).
- Resource IDs and names follow RFC 1035 / RFC 1123 DNS rules.
- ETags follow RFC 7232.
- UUIDs follow RFC 4122; IPv4/IPv6 follow RFC 791, RFC 4291, and RFC 5952.
