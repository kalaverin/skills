# pytest-planner
[ref: #ptp-intro]

Produces repository-specific pytest enablement artifacts: a test-authoring prompt and an atomic coverage plan.

## What it does
[ref: #ptp-what]

This skill creates two artifacts for a Python project. The first is a per-repo test-authoring and research prompt pinned to the exact `pytest-design` reference anchors a downstream agent must lazy-load. The second is an iteration-ready unit-test coverage plan split into atomic work items. It supports two branches: **bootstrap** (create the prompt in Serena memory) and **planning** (create a coverage plan in `project` or `feature` mode).

## When it activates
[ref: #ptp-when]

Activates when the agent needs to bootstrap testing for a Python repo or create a coverage plan for a feature branch.

Examples:

- "Create a test plan for this project."
- "Plan pytest coverage for the auth feature."
- "What should we test next?"
- "Бутстрап тестов."
- "План покрытия фичи."

## How to run / use it
[ref: #ptp-how]

Tell the agent what you need.
The agent resolves the entity/repo name, verifies preconditions, and runs the correct generator from `prompts/`:

- **Bootstrap** — for requests about a test prompt or bootstrapping tests: reads `prompts/BOOTSTRAP.md` and writes the generated prompt to Serena memory `agent/tests`.
- **Planning** — for requests about a coverage plan: resolves the mode (`project` on `main`/`master`, otherwise asks), reads `prompts/PLANNING.md` (`project`) or `prompts/FEATURE.md` (`feature`), and writes the plan to Serena memory `plans/<entity>/tests/coverage` or `plans/<entity>/tests/feature_coverage[_<suffix>]`.

In `project` mode the existing `agent/tests` prompt is a hard precondition. In `feature` mode it is optional.

## What it produces
[ref: #ptp-produces]

- A repository-specific test-authoring prompt stored in Serena memory at `agent/tests`.
- A machine-readable coverage plan stored in Serena memory at `plans/<entity>/tests/coverage` (project) or `plans/<entity>/tests/feature_coverage[_<suffix>]` (feature).

## Dependencies and why they matter
[ref: #ptp-deps]

- `pytest-design` — the plan's purpose is to drive work that conforms to this skill's rules.
- `entity-protocol` — defines the repo concept and the canonical `repos/` memory layout used to key generated plans.
- `frontmatter-protocol` — provides the lazy-load routing and frontmatter-harvest mechanics used during bootstrap.
- `repo-audit` — produces the technical (`repos/<repo>/overview`) and business (`repos/<repo>/business`) cards that are mandatory inputs.
- `serena-protocol` — governs memory mutation and persistence for generated artifacts.
- `subagents-protocol` — defines the read-only `explore` subagents used to survey the codebase.
- `todo-protocol` — governs the iteration planning workflow.

## Strengths and trade-offs
[ref: #ptp-tradeoffs]

### Strong sides
[ref: #ptp-strong]

- Gives future agents a clear, repo-specific testing contract.
- Atomic work items make incremental progress easy to track.
- Feature mode avoids re-planning for code that is already covered.

### Weak sides / limits
[ref: #ptp-weak]

- Requires an existing understanding of the repo structure.
- The plan itself is not executable; an agent still has to implement each item.
- Feature mode depends on a clean git diff and a known base branch.
- Cannot start without the repo cards created by `repo-audit`.

### Common pitfalls / gotchas
[ref: #ptp-pitfalls]

- Always pin exact `pytest-design` reference anchors in the generated prompt.
- Keep work items small and testable.
- In `feature` mode, base the plan strictly on the diff, not the whole repo.
- Store the final artifact in `.serena/memories/`; do not write prompt files to the skill directory.
- Never guess the plan mode outside the `main`/`master` → `project` default.

## Repository layout
[ref: #ptp-layout]

```text
_on_demand/pytest-planner/
├── prompts/              # Plan-generation prompts
│   ├── BOOTSTRAP.md      # Test-authoring prompt generator
│   ├── PLANNING.md       # Project-mode coverage plan generator
│   └── FEATURE.md        # Feature-mode coverage plan generator
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point: modes, deliverables, and routing index
```

## Important conventions / gotchas
[ref: #ptp-conventions]

- Two branches: **bootstrap** (prompt) and **planning** (coverage plan).
- Two planning modes: `project` (whole repo) and `feature` (diff-scoped).
- Every generated artifact must reference exact anchors from `pytest-design`.
- Work items must be atomic and independently completable.
- Persist the final artifact in Serena memory.
