# subagents-protocol

Tells the agent when and how to hand work off to specialized coder, explore, or plan subagents.

## What it does

This skill governs delegation.
It lets the main agent spin up isolated workers for complex or parallel tasks instead of doing everything in one context window.
It covers which subagent type to use, how long to let it run, what context to pass, and how to bridge web search or Serena memory operations that subagents cannot perform themselves.

## When it activates

Activates when you mention subagents or delegation, and whenever the agent decides a task should be delegated.

Examples of prompts that trigger it:

- "Use a subagent to explore the codebase."
- "Delegate the refactoring to a coder subagent."
- "Plan the implementation with a plan subagent."

It also activates automatically for complex investigations, multi-file edits, or parallel exploration.

## How to use it

You do not call the protocol directly.
When a request is large enough to benefit from isolation, the agent selects the right subagent type for you.
`coder` subagents write, refactor, debug, and run commands.
`explore` subagents do read-only codebase reconnaissance.
`plan` subagents produce implementation plans before any edits happen.
Give the agent a clear goal and boundaries; it packages those into a self-contained prompt, sets a timeout, and summarizes the result for you.

## What it produces

- One or more subagent tasks and their summarized findings.
- Code changes, reports, or plans authored by the subagent and reviewed by the main agent.
- No direct artifacts from the protocol itself.

## Repository layout

```text
subagents-protocol/
├── references/           # Pre-flight checklist for every delegation
│   └── subagent-launch-checklist.md
└── SKILL.md              # Agent entry point: delegation rules and parameters
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/subagent-launch-checklist.md` | Pre-flight checklist for choosing subagent type, parameters, context, and constraints |

## Important conventions / gotchas

- Requires `bootstrap`, `shell-protocol`, and `serena-protocol`.
- Subagents have no access to MCP tools.
- The main agent must perform Serena memory, Kagi web search, and symbolic/LSP operations on their behalf.
- Pass Serena memory pages by file path, never by pasting their contents.
- Default to foreground subagents; use background only when the task can continue independently and returning early helps.
- Simple tasks get at least 10 minutes; complex investigations get at least 55 minutes.
