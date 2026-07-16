# pytest-planner

Tailors the generic `pytest-design` playbook to a specific Python repository and turns it into an executable test plan.

## What it does

This skill produces repository-specific pytest enablement artifacts.
It analyzes the target repo once and writes a reusable test-authoring prompt plus an atomic unit-test coverage plan.
That saves future agents from rediscovering the repository's domain model, stack, and relevant pytest recipes every time they write tests.
It keeps the actual test-writing rules in `pytest-design`; it only pins which rules matter for this repository.

## When it activates

Activates when you ask for test bootstrapping, a test agent prompt, or a test coverage plan.

Examples of prompts that trigger it:

- "Create a test prompt for the billing service."
- "Bootstrap tests for this repository."
- "Build a unit-test coverage plan for merchant-api."
- "Plan the test development for the order domain."

## How to use it

First make sure the repository has its technical and business cards in place.
You create those with `project-audit` (entity card) and `business-audit` (business cards and glossaries).
Then ask the agent to produce the artifact you need.
For a reusable authoring prompt, say "Create a test prompt for `<entity>`".
For a concrete work plan, say "Create a unit-test coverage plan for `<entity>`".
The agent may ask you to name the entity if several exist, and it may ask runtime questions such as how deep mutation testing should go or whether to include a security audit.
You do not edit files manually; the agent writes everything to Serena memory.

## What it produces

- Serena memory `agent/tests` — a repository-specific pytest authoring and research prompt.
- Serena memory `plans/<entity>/tests/coverage` — an iteration-ready list of atomic unit-test work items.
- A list of any missing dependencies that block the planned tests.
- Validated, deduplicated anchors pointing back to the relevant `pytest-design` recipe cards.

## Repository layout

```text
pytest-planner/
├── prompts/              # Prompt generators
│   ├── BOOTSTRAP.md      # Repository-specific test-authoring prompt
│   └── PLANNING.md       # Iteration-ready unit-test coverage plan
└── SKILL.md              # Agent entry point, routing, and workflow
```

## Reference overview

| File | What it covers |
|------|----------------|
| `prompts/BOOTSTRAP.md` | Generating the repository-specific pytest agent prompt stored in `agent/tests` |
| `prompts/PLANNING.md` | Building the atomic unit-test coverage plan stored in `plans/<entity>/tests/coverage` |

## Important conventions / gotchas

- Requires `business-audit`, `project-audit`, `pytest-design`, `serena-protocol`, `subagents-protocol`, and `todo-protocol`.
- Hard preconditions are `entities/<entity>`, `logic/<entity>/...`, `project/glossary`, and `logic/<entity>/glossary`.
- The in-root skill mirror `.kimi/mirror/` must exist and contain the skill tree.
- Planning depends on bootstrapping: `agent/tests` must already exist before creating a coverage plan.
- The skill writes only to Serena memory; it does not generate test code directly.
- It never duplicates the `pytest-design` rule prose; it only pins the anchors that apply.
