---
name: ondemand
description: Runtime header-only manifest for on-demand skills. The frontmatter carries a compressed trigger registry so the
  agent can match requests without reading each on-demand SKILL.md header at startup.
runtime: true
triggers:
  reason: Header-only manifest; entries are evaluated during runtime re-evaluation.
requires:
- frontmatter-protocol
ondemand:
- name: atlassian-skill
  description: "Read-only access to Atlassian Jira and Confluence via MCP. Use for reading Jira issues/tickets and Confluence pages/documentation, including daily page diffs. Triggers on mentions of Jira, Confluence, Atlassian, Jira issue, Jira ticket, Confluence page, Confluence space, daily doc sync, page diff, or page history."
  triggers:
    request: "jira, confluence, atlassian, issue, ticket, epic, jira issue, jira task, confluence page, confluence space, confluence doc, daily doc sync, page diff, page history, джира, жира, задача в джира, тикет, конфла, конфлюенс, страница конфлюенс"
    reason: "User needs to read Jira issues or Confluence pages."
  runtime: true
- name: bobplus-api
  description: Bobplus Payments API (Africa) integration knowledge covering bearer auth, RSA request signing, X-Hash, C2B
    payins, B2C payouts, account services, and utilities. Use when answering questions or writing code against the Bobplus
    API.
  triggers:
    any:
      request: bobplus, bob+, bob plus, bobplus api, bobplus africa, developers.bobplus.africa, бобплюс, африканские платежи,
        платежи африка, mobile money africa, momo payin, momo payout, c2b africa, b2c africa, m-pesa integration, mpesa africa
        payments
      reason: Questions or code work against the Bobplus payments platform must be answered from the captured reference corpus,
        not from training data.
  runtime: true
- name: code-review
  description: Language-agnostic code review for any programming language, supporting diff-based and full-project review modes.
    Enforces boilerplate file naming, branch metadata, and severity classification.
  triggers:
    request: code review, review code, review diff, review feature, review project, pull request review, pr review, ревью,
      код-ревью, ревью кода, проверь код, проверь diff, проверь изменения, проверь проект
  runtime: true
- name: loki-skill
  description: "Query logs and service state in Grafana Loki via the logcli terminal client. Use for investigating service problems, exploring labels and series, and incident response. The agent is read-only: no mutations, no writes, no deletes."
  triggers:
    request: "logcli, loki, grafana logs, посмотри логи, найди в логах, посмотри логи на стейдже, посмотри логи на проде, проверь в локи, посмотри в графане, расследование инцидентов, разбор инцидента, разбор проблем, sentry, логи sentry, incident"
    reason: "User needs to query logs or service state through Grafana Loki."
  runtime: true
- name: protobuf-lang
  description: MANDATORY skill for Buf Protobuf lint and schema style. Use when writing, editing, or reviewing `.proto` files,
    `buf.yaml` configuration, packages, imports, enums, messages, services, RPCs, or comments.
  triggers:
    any:
      files: fd -e proto --max-results 1 | wc -l | grep -q 1
      request: protobuf, proto, buf, buf.yaml
  runtime: true
- name: pytest-design
  description: MANDATORY skill for writing, editing, running, and reviewing Python unit tests, integration tests, and pytest
    suites. Use for any Python testing task.
  triggers:
    all:
      files: fd -e py -e pyi --max-results 1 | wc -l | grep -q 1
      request: pytest, unit test, integration test, test fixture, conftest, parametrization, mocking, markers, test isolation,
        faker in tests, async test, pytest plugin, pytest configuration, coverage, xdist, python test, python tests, тест,
        тесты, юнит-тест, интеграционный тест, фикстура, параметризация, мок, маркер, покрытие тестами
  runtime: true
- name: pytest-planner
  description: MANDATORY skill for producing repository-specific pytest enablement artifacts and unit-test coverage plans
    in project or feature mode.
  triggers:
    all:
      files: test -d .serena/memories
      request: pytest bootstrap, bootstrap tests, generate test prompt, test agent prompt, pytest-planner, test planning bootstrap,
        master test plan, план покрытия, бутстрап тестов, сгенерируй промпт тестов, промпт для тестов, промпт pytest, планирование
        тестов, feature coverage plan, coverage plan, diff coverage plan, feature test plan, branch coverage plan, feature
        testing, branch coverage, план покрытия фичи, покрытие фичи, план покрытия ветки, покрытие диффа, тестирование фичи,
        покрытие ветки
- name: repo-audit
  description: MANDATORY skill for full repository audits, creating repo cards, business-domain reports, dependency cards,
    and the project-level index. Supports FULL, PARTIAL, and REFRESH run modes.
  triggers:
    request: create entity card, create project card, create service card, create repository card, entity card, project card,
      service card, repository card, repo card, explore project, explore service, explore repository, study project, study
      service, study repository, изучи проект, изучи сервис, изучи репозиторий, создай карточку проекта, создай карточку сервиса,
      создай карточку репозитория, карточка репо, business entities, business expertise, domain analysis, domain events, бизнес-сущности,
      анализ бизнеса, business analysis, business domain analysis, analyze business domain, business logic analysis, business
      rules analysis, what business does, business purpose, business meaning, domain model analysis, бизнес-анализ, бизнес-логика,
      бизнес-смысл, доменная модель, бизнес-правила, зачем нужно приложение, бизнес-цель, dependency card, create dependency
      card, dependency map, create dependency map, architecture dependencies, service dependencies, what does it depend on,
      карточка зависимостей, создай карточку зависимостей, карта зависимостей, изучи зависимости, repo audit, аудит репо,
      аудит репозитория, полный аудит, обнови карточки, refresh cards, update stale cards
- name: security-audit
  description: Security assessment / SAST workflow aligned with OWASP API Security Top 10 2023. Produces a consolidated final
    report under `.serena/memories/audit/`.
  triggers:
    request: sast, security audit, vulnerability assessment, code security review, penetration test, pentest, security scan,
      аудит безопасности, поиск уязвимостей, сканирование уязвимостей, проверка безопасности, SQL injection, SQLi, XSS, IDOR,
      SSRF, RCE, XXE, SSTI, JWT, file upload, path traversal, missing auth, business logic, GraphQL injection, hardcoded secrets,
      BOLA, BOPLA, broken object level authorization, broken object property level authorization, resource consumption, rate
      limiting, inventory management, unsafe consumption of APIs, third-party API, security misconfiguration, OWASP API 2023,
      OWASP API Security Top 10
- name: session-inspector
  description: Token-cheap inspection of Kimi Code CLI session files under ~/.kimi/sessions. Governs script-based extraction
    and prohibits direct reads of session JSONL files.
  triggers:
    request: найди сессию, последние сессии, прошлая сессия, прежняя сессия, сломанная сессия, незавершённая сессия,
      завершённая сессия, какие были чаты, какие были сессии, session id, найди разговор, найди чат, история сессий, what
      sessions, find session, previous session, broken session, подними контекст, подними контекст из сессии, продолжим с той
      сессии, продолжи сессию, восстанови контекст сессии, restore session context, resume that session, трекай сессию,
      отслеживай сессию, track session, tracking session, session counters, token usage, context usage, live session,
      wire.jsonl, следи за сессией, мониторинг сессии, сколько токенов, контекст заполнен, счётчики сессии
    reason: Session questions must be answered from distilled script output, never from raw JSONL reads.
  runtime: true
- name: temporal-lang
  description: Develop, debug, and manage Temporal applications across Python, TypeScript, Go, Java, .NET, and Ruby. Use for
    workflows, activities, workers, Temporal CLI/Server/Cloud, and durable execution concepts.
  triggers:
    request: temporal, temporalio, temporal workflow, temporal activity, durable execution, temporal cloud, temporal cli,
      temporal server, continue-as-new
  runtime: true
---

# On-Demand Skill Manifest
[ref: #ondemand-intro]

This skill is a **runtime, header-only manifest**. It does not contain task rules; it carries a registry of rarely used skills stored in `_on_demand/<skill>/` so the agent can match requests without reading every on-demand `SKILL.md` header at startup.

## How the manifest is used
[ref: #ondemand-usage]

1. At bootstrap, `_on_demand/SKILL.md` is discovered and its frontmatter is batch-extracted like any other skill header.
2. Because it carries `runtime: true`, its body is not read until the user explicitly asks about the on-demand mechanism.
3. During runtime re-evaluation (after every new user message and path touch), evaluate each entry in `ondemand:` that carries `runtime: true` as if it were a discovered skill header:
   - apply the same trigger grammar (`any`, `all`, `files`, `request`);
   - if an entry matches, read `_on_demand/<name>/SKILL.md` in full and resolve its `requires`.
   - entries without `runtime: true` are evaluated once at bootstrap and are not re-evaluated mid-session.
4. Do not read `_on_demand/<skill>/SKILL.md` bodies unless their manifest entry matched.

## Mapping
[ref: #ondemand-mapping]

| Skill | Runtime | Description |
|-------|---------|-------------|
| `atlassian-skill` | yes | Read-only access to Atlassian Jira and Confluence via MCP. Use for reading Jira issues/tickets and Confluence pages/documentation, including daily page diffs. Triggers on mentions of Jira, Confluence, Atlassian, Jira issue, Jira ticket, Confluence page, Confluence space, daily doc sync, page diff, or page history. |
| `bobplus-api` | yes | Bobplus Payments API (Africa) integration knowledge covering bearer auth, RSA request signing, X-Hash, C2B payins, B2C payouts, account services, and utilities. Use when answering questions or writing code against the Bobplus API. |
| `code-review` | yes | Language-agnostic code review for any programming language, supporting diff-based and full-project review modes. Enforces boilerplate file naming, branch metadata, and severity classification. |
| `loki-skill` | yes | Query logs and service state in Grafana Loki via the logcli terminal client. Use for investigating service problems, exploring labels and series, and incident response. The agent is read-only: no mutations, no writes, no deletes. |
| `protobuf-lang` | yes | MANDATORY skill for Buf Protobuf lint and schema style. Use when writing, editing, or reviewing `.proto` files, `buf.yaml` configuration, packages, imports, enums, messages, services, RPCs, or comments. |
| `pytest-design` | yes | MANDATORY skill for writing, editing, running, and reviewing Python unit tests, integration tests, and pytest suites. Use for any Python testing task. |
| `pytest-planner` | no | MANDATORY skill for producing repository-specific pytest enablement artifacts and unit-test coverage plans in project or feature mode. |
| `repo-audit` | no | MANDATORY skill for full repository audits, creating repo cards, business-domain reports, dependency cards, and the project-level index. Supports FULL, PARTIAL, and REFRESH run modes. |
| `security-audit` | no | Security assessment / SAST workflow aligned with OWASP API Security Top 10 2023. Produces a consolidated final report under `.serena/memories/audit/`. |
| `session-inspector` | yes | Token-cheap inspection of Kimi Code CLI session files under ~/.kimi/sessions. Governs script-based extraction and prohibits direct reads of session JSONL files. |
| `temporal-lang` | yes | Develop, debug, and manage Temporal applications across Python, TypeScript, Go, Java, .NET, and Ruby. Use for workflows, activities, workers, Temporal CLI/Server/Cloud, and durable execution concepts. |
