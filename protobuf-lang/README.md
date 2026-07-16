# protobuf-lang

Enforces Buf Protobuf style and lint rules when you write, edit, or review `.proto` files and `buf.yaml` configuration.

## What it does

This skill keeps Protobuf schemas consistent with the Buf STANDARD ruleset.
It covers proto file and package conventions, import ordering, enum naming and values, message field naming and numbering, service and RPC naming, comment style, file layout, schema evolution, and `buf.yaml` v2 lint configuration.
The agent looks up only the relevant rule section for the task at hand.

## When it activates

Activates automatically when the project contains `.proto` files.
It also activates when you ask about protobuf, proto, buf, or `buf.yaml`.

Example prompts:

- "Review my protobuf schema."
- "Add a new RPC to the payment service."
- "Configure buf lint for this repo."
- "Are these enum values named correctly?"

## How to use it

Place your `.proto` files in the repository and add a `buf.yaml` if you want linting.
When you ask the agent to write or review proto code, it applies the Buf rules automatically.
If `buf` is available, the agent runs `buf lint` on the files it changed and fixes only those files.

## What it produces

- Lint-compliant `.proto` files.
- A `buf.yaml` configuration matching your chosen rule category.
- Optional `buf lint` output when the tool is present.

## Repository layout

```text
protobuf-lang/
├── references/           # Exhaustive Buf lint and style reference
│   └── rules.md
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/rules.md` | Quick start, `buf.yaml` configuration, file and package conventions, imports, enums, messages, services and RPCs, comments and layout, design recommendations, rule categories, per-rule reference, and intentionally excluded topics. |

## Important conventions / gotchas

- Requires the `api-design` skill automatically.
- Google AIP resource design, HTTP/gRPC transcoding, and overall API structure live in `api-design`, not here.
- The default lint category is `STANDARD`.
- The agent fixes only code it explicitly modified; pre-existing lint violations in untouched files are left alone.
