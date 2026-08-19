# temporal-lang
[ref: #tl-intro]

Guides development, debugging, and management of Temporal applications.

## What it does
[ref: #tl-what]

This skill provides patterns for building durable execution systems with Temporal. It covers workflows, activities, workers, signals, queries, heartbeats, retries, versioning, continue-as-new, child workflows, saga patterns, and Temporal CLI / Server / Cloud usage. It supports Python, TypeScript, Go, Java, .NET, and Ruby SDKs.

## When it activates
[ref: #tl-when]

Activates when you build workflows or activities, debug stuck workflows, handle non-determinism errors, or operate Temporal infrastructure.

Examples:

- "Implement a Temporal workflow."
- "Debug a non-determinism error."
- "Add signals and queries to a workflow."
- "Set up a Temporal worker."

## How to run / use it
[ref: #tl-how]

The skill is reference material used while writing or reviewing Temporal code. It provides language-specific guidance, anti-patterns, testing patterns, and operational commands. Use the `SKILL.md` routing index to find the relevant SDK or operational topic, then read the corresponding reference card.

## What it produces
[ref: #tl-produces]

- Durable, deterministic workflows.
- Reliable activities with proper retry and heartbeat semantics.
- Correct signal and query handlers.
- Operational commands for workflow inspection and cluster management.

## Dependencies and why they matter
[ref: #tl-deps]

- `python-lang` or another language skill when available — provides language-specific style while this skill supplies Temporal patterns.

## Strengths and trade-offs
[ref: #tl-tradeoffs]

### Strong sides
[ref: #tl-strong]

- Covers the full Temporal lifecycle: authoring, testing, debugging, and operations.
- Multi-language support means the same durability concepts apply across SDKs.
- Includes practical patterns such as sagas, child workflows, and patching.

### Weak sides / limits
[ref: #tl-weak]

- The skill is reference, not an executable tool; you still write the Temporal code.
- SDK differences are real; always check the language-specific reference card.
- Operational commands depend on the Temporal CLI version and cluster setup.

### Common pitfalls / gotchas
[ref: #tl-pitfalls]

- Workflows must be deterministic: no randomness, no unbounded iteration, no wall-clock sleeps.
- Heavy or non-deterministic work belongs in activities, not workflows.
- Use `patch` or `workflow.GetVersion` for workflow changes in production.
- Heartbeats are required for long-running activities.
- Child workflows and continue-as-new have specific cancellation and retry rules.

## Repository layout
[ref: #tl-layout]

```text
temporal-lang/
├── references/           # SDK and operational reference cards
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: routing index and core concepts
```

## Reference overview
[ref: #tl-refs]

The `references/` directory contains language-specific and topic-specific cards for Python, TypeScript, Go, Java, .NET, Ruby, testing, debugging, and operations.

## Important conventions / gotchas
[ref: #tl-conventions]

- Keep workflows deterministic.
- Offload I/O and heavy work to activities.
- Version workflow changes before deploying to production.
- Heartbeat long-running activities.
- Use saga patterns for compensatable multi-step operations.
