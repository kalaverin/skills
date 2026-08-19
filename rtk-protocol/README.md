# rtk-protocol
[ref: #rtk-protocol]

Token-saving wrapper that compacts command output before it reaches the agent's context.

## What it does
[ref: #rtk-what-it-does]

This skill tells the agent when and how to prefix shell commands with `rtk`, a Rust-based output filter. When `rtk` knows the command, it compresses the output dramatically; when it does not, the command passes through unchanged. The skill therefore acts as a transparent token-economy layer on top of normal shell work, not as a replacement for the tools selected by `mandatory-tools`.

## When it activates
[ref: #rtk-when-it-activates]

The skill activates automatically when the `rtk` binary is found on `PATH`.

Example prompts that will route through `rtk` once the skill is active:

- "Run the tests and show me only failures."
- "Show the git diff for the last commit."
- "Build the project and summarize the output."
- "List the files in this directory compactly."
- "Check why the CI job failed."

## How to run / use it
[ref: #rtk-how-to-run-use-it]

What a human must do:

1. Install `rtk` and make sure it is on `PATH`. The skill's command inventory is pinned to `rtk 0.42.4`.
2. Verify the version with `rtk --version`. If your installed version is newer, tell the agent so the skill inventory can be refreshed.

What the agent does automatically:

- Prefixes every shell command in the supported inventory with `rtk`, even inside `&&` chains.
- Falls back to normal execution when no dedicated filter exists.
- Keeps `mandatory-tools` tool selection intact: `fd`, `rg`, `lsd`, `ruplacer`, `uv`, and `ruff` remain the canonical tools, but may be `rtk`-prefixed when output is large.

Installation note: `rtk` is distributed as a standalone binary. There is no agent-side configuration file to maintain.

## What it produces
[ref: #rtk-what-it-produces]

- Condensed command output for common development tasks.
- Typical token savings of 60–90% on tests, builds, package managers, git operations, and infrastructure commands.
- A consistent prefixing habit that makes token savings automatic.

## Dependencies and why they matter
[ref: #rtk-dependencies-and-why-they-matter]

| Dependency | Why it matters |
|---|---|
| `mandatory-tools` | RTK never overrides tool selection or execution hygiene; `mandatory-tools` still decides when to use `fd`, `rg`, `lsd`, `ruplacer`, `uv`, and `ruff`. |
| `rtk` binary | The skill is inactive and its rules are moot without the binary. |

## Strengths and trade-offs
[ref: #rtk-strengths-and-trade-offs]

- **Strong sides:** Large, built-in command inventory; safe passthrough for unknown commands; significant token reduction with no workflow change.
- **Weak sides / limits:** Only helps when `rtk` is installed; newer versions require a skill refresh; it cannot replace MCP tools such as Kagi search or Serena symbolic operations.
- **Common pitfalls / gotchas:** Verbosity flags must come before the subcommand (`rtk -v git status`, not `rtk git status -v`). Do not use `rtk init`, `rtk hook`, `rtk telemetry`, or `rtk trust` unless the user explicitly asks for state-changing setup. Always prefix each command in an `&&` chain separately.

## Repository layout
[ref: #rtk-repository-layout]

```text
rtk-protocol/
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: golden rule, inventory, precedence, and version pin
```

## Important conventions / gotchas
[ref: #rtk-important-conventions-and-gotchas]

- The golden rule is **always prefix** — if the command is in the inventory, use the filter; if not, `rtk` passes it through unchanged.
- `rtk rg` is the preferred form of `rg` when large output is expected, because it runs ripgrep natively and then compacts the result.
- MCP tools take precedence: web search goes through `kagimcp`, memory and symbolic work through Serena, no matter how convenient `rtk` would be.
- If the installed `rtk` is newer than the pinned version and the inventory looks stale, report the mismatch before relying on new subcommands.
