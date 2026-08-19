# api-design
[ref: #ad-intro]

Mandatory rules for Google AIP-compliant API resource design and compatibility.

## What it does
[ref: #ad-what]

This skill enforces Google AIP design patterns when the agent designs or reviews APIs. It covers resource naming, standard operations, fields, pagination, filtering, sorting, long-running operations, errors, versioning, and backward compatibility. For proto schema style, use `protobuf-lang`.

## When it activates
[ref: #ad-when]

Activates whenever the agent designs API resources, writes or reviews RPCs, plans proto services, or discusses API compatibility.

Examples:

- "Design the API for orders."
- "Review this gRPC service."
- "Is this change backward compatible?"
- "Add pagination to the list endpoint."

## How to run / use it
[ref: #ad-how]

The skill applies automatically during API design and review. It lazy-loads AIP rules from `references/` by rule number.
When writing protobuf, combine this skill with `protobuf-lang`: `api-design` owns resource design, `protobuf-lang` owns schema style.
Use `api-design/references/` to look up specific AIP rules by number or topic.

## What it produces
[ref: #ad-produces]

- AIP-compliant resource models and method sets.
- Consistent naming, pagination, and error semantics.
- Backward-compatible change assessments.
- Optional machine-readable design artifacts stored in `.serena/memories/`.

## Dependencies and why they matter
[ref: #ad-deps]

- `frontmatter-protocol` — provides the lazy-load routing funnel used to consume the large AIP reference corpus.
- `read-for-comments` — archives the Google AIP corpus and the RFC 2119/8174 requirement-level keywords.

## Strengths and trade-offs
[ref: #ad-tradeoffs]

### Strong sides
[ref: #ad-strong]

- Aligns APIs with Google's widely adopted AIP standard.
- Separates design concerns from proto syntax concerns.
- Compatibility rules prevent breaking changes from being introduced silently.

### Weak sides / limits
[ref: #ad-weak]

- Not every AIP rule applies to every API; the agent must select rules by context.
- AIP is Google-centric; external constraints may require deviations.
- Does not enforce proto linting; use `protobuf-lang` and `buf` for that.

### Common pitfalls / gotchas
[ref: #ad-pitfalls]

- Resource names use collection identifiers and resource IDs, e.g., `projects/123/orders/456`.
- Standard methods are `List`, `Get`, `Create`, `Update`, `Delete`, and `Batch*` variants.
- Custom methods must use a colon suffix and a verb, e.g., `orders/456:cancel`.
- `Update` uses field masks; `Create` does not.
- List responses are wrapped in a response message with `repeated` results and a `next_page_token`.

## Repository layout
[ref: #ad-layout]

```text
api-design/
├── prompts/              # API design prompts
├── references/           # Google AIP rule reference cards
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: AIP rules, compatibility, and routing index
```

## Reference overview
[ref: #ad-refs]

The `references/` directory contains AIP rule cards organized by AIP number. Lazy-load the cards you need via the `frontmatter-protocol` lazy-load funnel (`[ref: #lazy-load-routing]`) rather than reading every file.

## Important conventions / gotchas
[ref: #ad-conventions]

- Resource design lives here; proto syntax lives in `protobuf-lang`.
- Use standard methods and custom methods consistently.
- Assess backward compatibility before approving changes.
- Store final design decisions in memory when the project uses Serena.
