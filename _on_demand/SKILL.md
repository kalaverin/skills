---
name: ondemand
description: Runtime header-only manifest for on-demand skills. The frontmatter carries a compressed trigger registry so the agent can match requests without reading each on-demand SKILL.md header at startup.
runtime: true
triggers:
  reason: Header-only manifest; entries are evaluated during runtime re-evaluation.
requires:
- frontmatter-protocol
ondemand:
- name: atlassian-skill
  description: Read-only Jira and Confluence access via MCP. Use for issues/tickets, pages/documentation, and daily page diffs.
  triggers:
    request: jira, confluence, atlassian, issue, ticket, epic, jira issue/task, confluence page/space/doc, daily doc sync, page diff/history, джира/жира, задача в джира, тикет, конфла/конфлюенс, страница конфлюенс
    reason: User needs to read Jira issues or Confluence pages.
  runtime: true
- name: bobplus-api
  description: 'Bobplus Payments API (Africa) integration reference: auth, signing, C2B payins, B2C payouts, account services, utilities. Use for questions or code against Bobplus.'
  triggers:
    any:
      request: bobplus, bob+, bobplus api/africa, developers.bobplus.africa, бобплюс, африканские платежи, платежи африка, mobile money africa, momo payin/payout, c2b/b2c africa, m-pesa/mpesa integration
      reason: Questions or code work against the Bobplus payments platform must be answered from the captured reference corpus, not from training data.
  runtime: true
- name: code-review
  description: Thorough language-agnostic code review for any programming language. Use for code/diff/feature/project/PR review; supports diff-based and full-project modes.
  triggers:
    request: code review, review code/diff/feature/project, pull request review, pr review, ревью, код-ревью, ревью кода, проверь код/diff/изменения/проект
  runtime: true
- name: feature-archival
  description: Archive a shipped feature's Serena memory footprint into .serena/memories/archive/<feature>/, verify, then recoverably delete originals. Trigger phrases load the skill; the pipeline starts only on explicit feature-closing command after rollout.
  triggers:
    request: закрываем/закрыть фичу, закрываем feature, заархивируй/архивация фичи, фича в проде закрываем, выкатил в прод закрываем, archive/close the feature, feature archival
    reason: A shipped feature's cross-scope memory footprint must be extracted, compressed into archive/<feature>/, and the originals deleted recoverably.
  runtime: true
- name: loki-skill
  description: Query logs and service state in Grafana Loki via logcli. Use for incident response and exploration. Read-only.
  triggers:
    request: logcli, loki, grafana logs, посмотри/найди логи, логи на стейдже/проде, проверь в локи, посмотри в графане, разбор/расследование инцидента, разбор проблем, sentry, логи sentry, incident
    reason: User needs to query logs or service state through Grafana Loki.
  runtime: true
- name: protobuf-lang
  description: MANDATORY skill for Buf Protobuf lint and schema style. Use for .proto files, buf.yaml, packages, imports, enums, messages, services, RPCs, or comments.
  triggers:
    any:
      files: fd -e proto --max-results 1 | wc -l | grep -q 1
      request: protobuf, proto, buf, buf.yaml
  runtime: true
- name: pytest-design
  description: MANDATORY skill for writing, running, and reviewing Python unit/integration tests. Use for pytest, fixtures, parametrization, mocking, markers, isolation, async tests, plugins, config, coverage, xdist. Python projects only.
  triggers:
    all:
      files: fd -e py -e pyi --max-results 1 | wc -l | grep -q 1
      request: pytest, unit/integration test, test fixture, conftest, parametrization, mocking, markers, test isolation, faker in tests, async test, pytest plugin/configuration, coverage, xdist, python test, тест/тесты, юнит-тест, интеграционный тест, фикстура, параметризация, мок, маркер, покрытие тестами
  runtime: true
- name: pytest-planner
  description: 'MANDATORY skill for pytest enablement artifacts: a repo-specific test-authoring prompt and an atomic unit-test coverage plan in project or feature mode.'
  triggers:
    all:
      files: test -d .serena/memories
      request: pytest bootstrap, bootstrap tests, pytest-planner, test planning, master test plan, generate test/agent prompt, план покрытия, бутстрап тестов, сгенерируй промпт тестов, промпт pytest, планирование тестов, feature/diff/branch coverage plan, feature testing, план покрытия фичи/ветки/диффа, покрытие/тестирование фичи, покрытие ветки
- name: repo-audit
  description: 'MANDATORY skill for full repository audits: repo/business/dependency cards and project dependency index. Modes: FULL, PARTIAL, REFRESH. Use for entity/repo cards, project/service/repository study, business/domain analysis, dependency maps, audits, or refreshing stale cards.'
  triggers:
    request: entity card, repo card, project card, service card, create/study card, explore/study project/service/repository, изучи проект/сервис/репозиторий, создай карточку проекта/сервиса/репозитория, карточка репо, business entities, business expertise, business/domain analysis, domain events, domain model, business logic, business rules, business purpose, what business does, бизнес-сущности, бизнес-анализ, бизнес-логика, бизнес-смысл, бизнес-правила, бизнес-цель, доменная модель, зачем нужно приложение, dependency card/map, architecture/service dependencies, what does it depend on, карточка/карта зависимостей, изучи зависимости, repo audit, аудит репо/репозитория, полный аудит, обнови карточки, refresh/update stale cards
- name: security-audit
  description: Security assessment / SAST workflow aligned with OWASP API Security Top 10 2023. Orchestrates reconnaissance, screener, parallel detection, validation, and consolidated report under .serena/memories/audit/. Use for audits, SAST, vulnerability assessment, code security review, pentest-style review, OWASP API 2023, or specific vulnerability classes.
  triggers:
    request: sast, security audit, security scan, vulnerability assessment, code security review, penetration test, pentest, аудит безопасности, проверка безопасности, поиск/сканирование уязвимостей, SQL injection, SQLi, XSS, IDOR, SSRF, RCE, XXE, SSTI, JWT, file upload, path traversal, missing auth, business logic, GraphQL injection, hardcoded secrets, BOLA, BOPLA, broken object level/property authorization, resource consumption, rate limiting, inventory management, unsafe consumption of third-party APIs, security misconfiguration, OWASP API 2023, OWASP API Security Top 10
- name: service-layout
  description: 'MANDATORY normative standard for company Python service layout: canonical package layout, import borders, domain models, mappings, ports/DI, errors, settings/secrets, persistence/UoW, lifecycle, observability — ruling ids L/I/D/M/P/E/S/T/Y/O. Use for designing, scaffolding greenfield, or reviewing services. Full standard applies on activation; every violation is reported by ruling id.'
  triggers:
    request: service layout/structure/design, структура/лейаут/каркас сервиса, как должен выглядеть сервис, новый сервис, создай/создаём сервис, проектируем/спроектируй сервис, проектирование сервиса, service scaffold/scaffolding, greenfield service, company service standard, ревью/проверь сервис, service review, layout review, composition root, порты и адаптеры, hexagonal service
    reason: Design, greenfield development, and review of company services must conform to the Company Service Layout Standard.
  runtime: true
- name: session-inspector
  description: Token-cheap inspection of Kimi Code CLI sessions under ~/.kimi/sessions. Use to find/list/identify past sessions or restore context. Extraction must use the mandated script; never read session JSONL files directly.
  triggers:
    request: найди сессию, найди разговор/чат, последние сессии, прошлая/прежняя сессия, сломанная/незавершённая/завершённая сессия, какие были чаты/сессии, session id, история сессий, what sessions, find/previous/broken session, подними/восстанови контекст из сессии, продолжим с той сессии, продолжи сессию, restore session context, resume that session, трекай/следи за сессией, мониторинг сессии, track session, session counters, счётчики сессии, сколько токенов, контекст заполнен
    reason: Session questions must be answered from distilled script output, never from raw JSONL reads.
  runtime: true
- name: temporal-lang
  description: Develop, debug, and manage Temporal applications in Python, TypeScript, Go, Java, .NET, and Ruby. Use for workflows, activities, workers, SDK/server/cloud issues, and durable-execution concepts.
  triggers:
    request: temporal, temporalio, temporal workflow, temporal activity, durable execution, temporal cloud, temporal cli, temporal server, continue-as-new
  runtime: true
---

# On-Demand Skill Manifest
[ref: #ondemand-intro]

> Runtime, header-only manifest: no task rules here. The frontmatter `ondemand:` block is the compressed registry of rarely used skills in `_on_demand/<skill>/`, matched without reading every on-demand `SKILL.md` header at startup.

## How the manifest is used
[ref: #ondemand-usage]

1. At bootstrap, the `_on_demand/SKILL.md` frontmatter is batch-extracted like any skill header; `runtime: true` keeps this body unread until the user asks about the on-demand mechanism.
2. During runtime re-evaluation (every new user message, every path touch), each `ondemand:` entry with `runtime: true` is evaluated as a discovered skill header under the same trigger grammar (`any`, `all`, `files`, `request`); on a match, read `_on_demand/<name>/SKILL.md` in full and resolve its `requires`.
3. Entries without `runtime: true` evaluate once at bootstrap, never mid-session.
4. `_on_demand/<skill>/SKILL.md` bodies are read only after their manifest entry matched.

## Mapping
[ref: #ondemand-mapping]
