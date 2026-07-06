# project-audit

Serena skill for creating and maintaining entity cards for services, libraries, repositories, and infrastructure/GitOps components.

## What this skill does

`project-audit` defines the workflow for producing a Serena entity card. It does not explore code directly; instead, it orchestrates a read-only exploration subagent and then writes the resulting card and focused findings to Serena memory. The skill provides:

- A root-agent orchestration prompt.
- A read-only exploration subagent prompt.
- A common card skeleton and agent rules.
- Type-specific templates for:
  - gRPC services.
  - REST API gateways.
  - Temporal workflow workers.
  - Infrastructure / GitOps components.
  - Libraries.

## When to use it

Use this skill when the request involves:

- Creating or updating an entity card, project card, service card, or repository card.
- Exploring or studying a project, service, repository, or library.
- Gathering information for an entity card.

The skill responds to prompts such as "create service card", "explore project", "study repository", "создай карточку сервиса", and "изучи проект".

## Repository layout

```text
project-audit/
├── references/           # Templates and subagent prompts
│   ├── 01_make_card.md           # Root-agent orchestration prompt
│   ├── 02_service_card_writer.md # Final card writing instructions
│   ├── 03_service_card_explorer.md # Read-only exploration subagent prompt
│   ├── 04_service_card_common.md # Common skeleton and agent rules
│   ├── 05_grpc_service.md        # gRPC service template
│   ├── 06_rest_gateway.md        # REST gateway template
│   ├── 07_temporal_worker.md     # Temporal worker template
│   ├── 08_infrastructure_gitops.md # Infrastructure / GitOps template
│   └── 09_library.md             # Library template
└ SKILL.md                # Skill entry point and master execution workflow
```

## How to use this skill

1. Identify the entity name (`snake_case`) and path.
2. Check whether `entities/<entity_name>` already exists.
3. Read `references/01_make_card.md` for the master workflow.
4. Read `references/02_service_card_writer.md` for final writing instructions.
5. Determine the entity type and load the matching template from `references/05_*.md` through `references/09_*.md`.
6. Collect relevant memory paths under `.serena/memories/` for the entity.
7. Launch the read-only exploration subagent using the prompt in `references/03_service_card_explorer.md`.
8. Generate the directory tree yourself using the command in `references/04_service_card_common.md`.
9. Write the final card to `entities/<entity_name>` and findings to the appropriate namespaces.
10. Verify and persist with `just agent-memory-commit`.

## Reference index

| File | Purpose |
|------|---------|
| `references/01_make_card.md` | Root-agent orchestration from verification to persistence |
| `references/02_service_card_writer.md` | Final card writing instructions and quality checklist |
| `references/03_service_card_explorer.md` | Read-only exploration subagent prompt and report schema |
| `references/04_service_card_common.md` | Common skeleton, agent rules, and omitted items |
| `references/05_grpc_service.md` | gRPC service exported interface template |
| `references/06_rest_gateway.md` | REST gateway exported interface template |
| `references/07_temporal_worker.md` | Temporal worker exported interface template |
| `references/08_infrastructure_gitops.md` | Infrastructure / GitOps exported interface template |
| `references/09_library.md` | Library exported interface template |

## Conventions

- `SKILL.md` is the single entry point.
- Entity names use `snake_case`.
- Entity cards are saved to `entities/<entity_name>` in Serena memory.
- Findings route to `bugs/<entity>/...`, `notes/<entity>/...`, `decisions/<entity>/...`, `style/<entity>/...`, or `todo/<entity>/...`.
- Entity-specific metadata (branch, commit, commit date) must come from the entity's own git repository.
- The root agent orchestrates; the subagent explores read-only.
- Do not include Sentry, Prometheus, tests, linters, CI, Makefile, Docker, or entry points in the final card.
