# project-audit

Creates and maintains structured Serena entity cards for services, libraries, repositories, and infrastructure components.

## What it does

This skill turns a codebase into a concise, structured entity card in Serena memory.
It captures the exported interface, responsibilities, dependencies, and important conventions of a project component.
The skill also produces focused finding memories for bugs, notes, decisions, style issues, and todos scoped to that entity.
A read-only exploration subagent does the heavy lifting so the root agent can orchestrate and verify results.

## When it activates

Activates when you ask about creating, updating, or studying an entity, project, service, or repository card.

Example prompts:

- "Create a card for the payment service."
- "Study the user-api repository and write an entity card."
- "Update the card for order-service."
- "Изучи сервис биллинга и создай карточку."

## How to use it

Tell the agent which component you want documented and, if possible, where it lives in the workspace.
The agent will identify the entity name, verify whether a card already exists, and choose the right template.
You do not need to open reference files or run subagents yourself.

The skill supports several entity types:

- gRPC service
- REST API gateway
- Temporal workflow worker
- Infrastructure / GitOps component
- Library

If the target entity has no card yet, the agent will ask you before creating the first one.

## What it produces

- An entity card saved to `.serena/memories/entities/<entity_name>.md`.
- Focused finding memories under `.serena/memories/bugs/<entity>/...`, `notes/<entity>/...`, `decisions/<entity>/...`, `style/<entity>/...`, and `todo/<entity>/...`.

## Repository layout

```text
project-audit/
├── references/           # Card templates and subagent prompts
│   ├── 01_make_card.md              # Root-agent orchestration from verification to persistence
│   ├── 02_service_card_writer.md    # Final card writing instructions
│   ├── 03_service_card_explorer.md  # Read-only exploration subagent prompt
│   ├── 04_service_card_common.md    # Common skeleton and agent rules
│   ├── 05_grpc_service.md           # gRPC service template
│   ├── 06_rest_gateway.md           # REST gateway template
│   ├── 07_temporal_worker.md        # Temporal worker template
│   ├── 08_infrastructure_gitops.md  # Infrastructure / GitOps template
│   └── 09_library.md                # Library template
└── SKILL.md              # Agent entry point: manifest, triggers, and routing index
```

## Reference overview

| File | What it covers |
|------|----------------|
| `references/01_make_card.md` | Root-agent orchestration from verification to persistence. |
| `references/02_service_card_writer.md` | Final card writing instructions and section order. |
| `references/03_service_card_explorer.md` | Read-only exploration subagent prompt. |
| `references/04_service_card_common.md` | Common skeleton and agent rules. |
| `references/05_grpc_service.md` | gRPC service exported interface template. |
| `references/06_rest_gateway.md` | REST API gateway exported interface template. |
| `references/07_temporal_worker.md` | Temporal workflow worker exported interface template. |
| `references/08_infrastructure_gitops.md` | Infrastructure / GitOps exported interface template. |
| `references/09_library.md` | Library exported interface template. |

## Important conventions / gotchas

- Requires the `serena-protocol` skill automatically.
- Entity names and memory paths use `snake_case` with underscores.
- The first entity card must be created explicitly before other entity-scoped memories can be written.
- The final card intentionally omits Sentry, Prometheus, tests, linters, CI, Makefile, Docker, and entry points.
- Do not expect environment variable values, defaults, examples, or secrets to appear in the card.
- All timestamps use UTC ISO 8601 format.
