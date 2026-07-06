# protobuf-lang

Buf Protobuf style and lint reference for agents editing `.proto` files and `buf.yaml` configurations.

## What this skill does

`protobuf-lang` provides a comprehensive Buf style and lint rule set. It is a documentation-only skill: no runtime code, no build step, no lockfiles. It covers:

- Files and packages.
- Imports.
- Enums.
- Messages.
- Services and RPCs.
- Comments and layout.
- Design recommendations.
- Buf lint rule categories (`MINIMAL`, `BASIC`, `STANDARD`, `COMMENTS`, `UNARY_RPC`).
- Rule reference.
- Quick start and `buf.yaml` configuration examples for Buf v2.

## When to use it

Load this skill when the request involves:

- Writing, editing, or reviewing `.proto` files.
- Configuring `buf.yaml` lint or breaking-change rules.
- Questions about proto packages, imports, enums, messages, services, RPCs, or comments.

> **Boundary:** Google AIP resource design is handled by the sibling `api-design` skill. Use `api-design` for resource naming, operations, and API design compliance.

## Repository layout

```text
protobuf-lang/
├── references/           # Exhaustive Buf lint/style reference
│   └── rules.md
└── SKILL.md              # Skill entry point, triggers, and lazy-load protocol
```

## How to use this skill

1. Open `SKILL.md` for the trigger conditions and lazy-load routing index.
2. Identify the relevant topic (files/packages, imports, enums, messages, services, comments, design, rule categories, rule reference, quick start, configuration).
3. Extract only the targeted `[ref: #...]` section from `references/rules.md`.
4. Apply the extracted rules to the proto schema under review.

## Reference index

| Section in `references/rules.md` | Topic |
|----------------------------------|-------|
| `#quick-start` | Quick start and default rule category |
| `#configuration` | `buf.yaml` v2 lint and breaking-change configuration |
| `#files-and-packages` | Proto file and package conventions |
| `#imports` | Import rules and ordering |
| `#enums` | Enum naming and value rules |
| `#messages` | Message field naming, numbering, and structure |
| `#services-and-rpcs` | Service and RPC naming conventions |
| `#comments-and-layout` | Comment style and file layout |
| `#design-recommendations` | Design-level recommendations |
| `#rule-categories` | Buf lint rule categories |
| `#rule-reference` | Per-rule reference |

## Conventions

- `SKILL.md` is the single entry point.
- Agents must use the lazy-load protocol and extract only the targeted section.
- Buf v2 configuration schema is used for `buf.yaml` examples.
- The default lint category is `STANDARD`.
