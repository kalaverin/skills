# protobuf-lang
[ref: #pb-intro]

Mandatory rules for writing, editing, and reviewing Protocol Buffers schema and `buf` configuration.

## What it does
[ref: #pb-what]

This skill enforces Buf-style protobuf conventions. It covers package names, file layout, imports, enums, messages, services, RPCs, field naming, comments, and lint configuration. When `api-design` is also active, this skill handles schema style while `api-design` handles resource design.

## When it activates
[ref: #pb-when]

Activates whenever the agent writes, edits, or reviews `.proto` files, `buf.yaml` configuration, packages, imports, enums, messages, services, RPCs, or proto comments.

Examples:

- "Define a protobuf schema."
- "Review the proto files."
- "Set up buf lint."
- "Add a gRPC service."

## How to run / use it
[ref: #pb-how]

The skill applies automatically during proto editing. To validate:

```bash
buf lint
buf format -w
```

Use the package structure and naming rules from this skill and the resource patterns from `api-design`.

## What it produces
[ref: #pb-produces]

- Clean, lint-free `.proto` files.
- Consistent package and message naming.
- Properly configured `buf.yaml` lint configuration.
- Clear proto comments.

## Dependencies and why they matter
[ref: #pb-deps]

- `api-design` — owns Google AIP resource design when both skills are triggered.

## Strengths and trade-offs
[ref: #pb-tradeoffs]

### Strong sides
[ref: #pb-strong]

- Buf lint catches style and compatibility issues early.
- Consistent proto style makes generated code predictable across languages.
- Clear separation between schema style (`protobuf-lang`) and resource design (`api-design`).

### Weak sides / limits
[ref: #pb-weak]

- Requires `buf` CLI to be installed.
- Strict conventions may conflict with legacy proto files.
- Does not replace API design review; use `api-design` for resource modeling.

### Common pitfalls / gotchas
[ref: #pb-pitfalls]

- Package names use lowercase and reverse-domain style.
- File names use `snake_case.proto`.
- Message names use `PascalCase`; field names use `snake_case`.
- Enum names use `UPPER_SNAKE_CASE`; the first value must be `*_UNSPECIFIED = 0`.
- Services and RPCs use `PascalCase`; request/response messages are named `<RPC>Request` and `<RPC>Response`.

## Repository layout
[ref: #pb-layout]

```text
_on_demand/protobuf-lang/
├── README.md  # Human overview (this file)
└── SKILL.md   # Atomic agent entry point: proto style rules, lint reference, configuration
```

## Important conventions / gotchas
[ref: #pb-conventions]

- Run `buf lint` and `buf format -w` after proto changes.
- Keep schema style in this skill; keep resource design in `api-design`.
- Use `*_UNSPECIFIED = 0` as the first enum value.
- Name request and response messages consistently.
