# service-layout

[ref: #sly-readme-intro]

Normative standard for how a company Python service MUST look: canonical package layout, import borders, domain models, mappings, ports/DI, errors, settings/secrets, persistence/UoW, lifecycle, observability.

## What it does

[ref: #sly-readme-what-it-does]

This skill gives the agent the Company Service Layout Standard — 47 rulings (ids L/I/D/M/P/E/S/T/Y/O), a canonical package tree per service profile, an anti-pattern registry, and a conformance checklist. On activation the full standard applies: the agent checks every ruling and reports every violation by ruling id.

## When it activates

[ref: #sly-readme-when-it-activates]

The skill loads when the conversation turns to designing a new service, scaffolding greenfield code, or reviewing an existing service's structure.

Example prompts:

- "Спроектируй новый сервис для возвратов."
- "Создай каркас stateless-гейтвея поверх трёх gRPC-апстримов."
- "Проведи ревью структуры сервиса."

## Repository layout

[ref: #sly-readme-repository-layout]

```text
_on_demand/service-layout/
├── README.md   # Human overview (this file)
└── SKILL.md    # Agent entry point: the full standard with `sly-` anchors
```
