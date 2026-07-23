---
subject: "Architecture reconnaissance subagent producing `01_architecture.md` for SAST audit: mission scope, technology recon across languages, frameworks, serialization, package managers, JVM, infrastructure, databases, authn, integrations, entry points, LLM/AI, limits, security config, API inventory; architecture mapping of boundaries, flows, privileges, data, secrets, logging, CI/CD; downstream routing, OWASP map, output template."
index:
  - anchor: codebase-analysis
    what: "First-phase reconnaissance role that builds deep understanding of the target codebase and emits the single `01_architecture.md` reference document without hunting vulnerabilities yet."
    problem: "Security assessment launched against unfamiliar codebase risks shallow scans and missed exposure because later phases lack shared architecture knowledge; recon entry, discovery phase, truth source, blind scanning, orientation gap, onboarding cost, cold start, guesswork."
    use_when: "Audit starts and no architecture report exists; screener or detection phases need technology, entry-point, and data-flow context; `{{ REPORTS_ROOT }}/01_architecture.md` must be created."
    avoid_when: "Architecture report already written — consume it instead; specific vulnerability classes are the task, that is detection-phase work."
    expected: "`{{ REPORTS_ROOT }}/01_architecture.md` exists, complete enough that later phases never re-explore blindly."
  - anchor: analysis-mission
    what: "Scope contract declaring the report as single source of truth for screener, scans, and final report, with explicit must and must-NOT lists."
    problem: "Recon phase without firm boundaries drifts into premature vulnerability reporting, code modification, or incomplete handoff that forces later phases to re-explore; scope discipline, mission boundary, premature findings, handoff contract, re-exploration waste, drift control."
    use_when: "Recon agent needs its mandate and forbidden actions stated; completeness expectations for downstream consumers must be set; judging whether an activity belongs to this phase."
    avoid_when: "Operational checklists are needed — those live in the recon and mapping category anchors; output formatting is the question."
    expected: "The phase produces maximal completeness without vulnerability claims, source edits, or risk ratings."
  - anchor: analysis-phase1-intro
    what: "Working method for technology reconnaissance: manifests and configs first, source confirmation after, priority to entry points and security-sensitive flows, concrete values with evidence."
    problem: "Recon over large codebase without systematic approach drowns in line-by-line reading and yields vague claims stripped of versions, paths, or evidence; proof discipline, priority triage, manifest-first workflow, ambiguity handling, exhaustiveness trap, token budget, holistic."
    use_when: "Starting the technology inventory; deciding how to sequence reading; unsure how concrete each recorded value must be."
    avoid_when: "Category checklists themselves are wanted — each has its own recon anchor; architecture synthesis is the need, that is Phase 2."
    expected: "Every recorded technology value carries name, version, path, and explicit ambiguity notes where uncertain."
  - anchor: analysis-recon-languages
    what: "Checklist for identifying programming languages and versions from `.python-version`, `pyproject.toml`, `package.json` engines, `go.mod`, `pom.xml`, `Cargo.toml`, `Gemfile`, Dockerfiles, CI matrixes, plus cross-runtime seams."
    problem: "Version-sensitive security behavior gets misjudged when languages and runtimes are assumed rather than evidenced from version sources and manifest files; runtime inventory, version provenance, polyglot boundary, language detection, build matrix, interpreter drift."
    use_when: "Beginning recon; runtime versions influence later scan selection; data crosses language or runtime borders."
    avoid_when: "Frameworks and libraries are the question — see the frameworks anchor; deployment topology is wanted, see infrastructure."
    expected: "All languages and versions recorded with their evidence sources and every polyglot crossing named."
  - anchor: analysis-recon-frameworks
    what: "Checklist for web frameworks, GraphQL servers and gateways, RPC layers, ORMs, template engines, task queues, and testing frameworks that shape security behavior."
    problem: "Scan relevance depends on framework-specific sinks, yet generic stack guesses miss rendering stacks, ORM raw methods, queues, and mock servers exposing debug endpoints; framework inventory, sink surface, ORM detection, template injection, queue workers, debug exposure."
    use_when: "Mapping the stack before scan selection; framework-driven vulnerability classes (SSTI, ORM injection, debug endpoints) must be scoped; selecting stack-matched examples later."
    avoid_when: "Dependency supply-chain detail is needed — that is the package-managers anchor; raw language versions are the question."
    expected: "Every framework family present is named with version and the security-relevant facilities it brings."
  - anchor: analysis-recon-serialization
    what: "Checklist for serializers, auto-binding and mass-assignment libraries, PATCH handlers, GraphQL resolver patterns, parsers with strictness settings, and DTO definitions."
    problem: "BOPLA and injection findings stay invisible when binding and serialization behavior is undocumented, because property exposure depends on serializer and parser strictness; data binding, over-posting, DTO mapping, resolver exposure, parser config, binding laxity."
    use_when: "Request/response shaping must be understood; mass-assignment or excessive-exposure scans are anticipated; GraphQL field-level access needs scoping."
    avoid_when: "Auth mechanism detail is the need — see the authn anchor; database models themselves are wanted."
    expected: "Binding, serialization, and parser behavior recorded precisely enough to route BOPLA and injection scans."
  - anchor: analysis-recon-package-managers
    what: "Checklist for lockfiles, registry scoping, private package names, security-relevant dependencies, install scripts, update freshness, maintainer metadata, and supply-chain integrity controls."
    problem: "Dependency-confusion and supply-chain risk cannot be scoped without knowing manifests, registry pinning, lifecycle hooks, and integrity controls actually configured; lockfile inventory, maintainer trust, typosquatting, provenance attestations, install hooks, unsigned artifacts, slopsquatting."
    use_when: "Supply-chain scan (23) relevance is being decided; private packages exist; postinstall scripts or unattested artifacts are suspected."
    avoid_when: "Framework-level sink analysis is wanted — see frameworks; runtime CVE triage is detection-phase work."
    expected: "Manifests, registries, integrity controls, and risky dependency metadata documented end to end."
  - anchor: analysis-recon-jvm
    what: "Checklist of JVM-specific facilities: serialization and polymorphic typing, JNDI, class loading, native code, reflection, compiler plugins, scripting engines, RMI/JMX, instrumentation, dynamic invocation, unsafe access."
    problem: "Kotlin and Java stacks hide entire vulnerability classes behind deserialization, JNDI, ClassLoader, and reflection facilities that generic recon never inventories; JVM attack surface, deserialization sinks, JNDI usage, classloading, native bridges, dynamic dispatch."
    use_when: "The stack includes Java or Kotlin; JVM-anomaly scan (24) routing needs evidence; logging frameworks with lookup substitution are present."
    avoid_when: "No JVM language in the stack; non-JVM scripting is the concern — see frameworks or languages."
    expected: "Every dangerous JVM facility in use is catalogued with its configuration and exposure path."
  - anchor: analysis-recon-infrastructure
    what: "Checklist for Dockerfiles, compose files, Kubernetes manifests, Helm, Terraform, Pulumi, CI configs, base images, ports, runtime users, capabilities, service mesh, proxies, gateways, IAM."
    problem: "Misconfiguration and inventory scans need deployment facts, yet container users, exposed ports, capabilities, and gateway presence stay unknown without infra recon; deployment surface, container hardening, gateway topology, IAM posture, manifest inventory, network exposure."
    use_when: "Cloud, container, or IaC artifacts exist; misconfiguration scan (20) scoping needs deployment topology; entry-point exposure depends on proxies."
    avoid_when: "Application-level frameworks are the question; CI pipeline security detail belongs to the CI/CD mapping anchor."
    expected: "Deployment topology and hardening-relevant settings captured with file paths."
  - anchor: analysis-recon-databases
    what: "Checklist for SQL and NoSQL databases, caches, brokers, connection strings, ORM models, migrations, query builders, raw SQL files, and storage backends."
    problem: "Injection and data-exposure scans stall without knowing which stores exist, how they are reached, and where raw queries or migrations live; datastore inventory, query surfaces, connection config, migration files, cache layers, blob storage."
    use_when: "Any persistence exists; SQLi/NoSQLi scan routing needs store types; file-storage backends affect upload and traversal scans."
    avoid_when: "Serializer behavior is the question — see serialization; secret storage mechanics belong to secret management."
    expected: "Every datastore, access path, and raw-query location recorded."
  - anchor: analysis-recon-authn
    what: "Checklist for auth libraries and middleware, token issuance through revocation, session configuration, roles and permissions, admin panels, endpoint visibility, plus modern mechanisms: passkeys, OAuth 2.1, FAPI 2.0, DPoP, token exchange, SPIFFE."
    problem: "Authentication scans need mechanism-level truth, but vague notes like 'uses JWT' hide validation, refresh, revocation, and session-flag details that decide real risk; auth mechanism inventory, token lifecycle, session hardening, role model, passkey adoption, identity protocols."
    use_when: "Any authentication exists; JWT or missing-auth scans (09, 10) need routing evidence; passkeys or FAPI adoption may be in play."
    avoid_when: "Object-level authorization specifics are wanted — that is detection-phase IDOR work; role enforcement mapping is wanted — see privilege-levels anchor."
    expected: "Mechanisms, token handling, sessions, and roles documented with library and config precision."
  - anchor: analysis-recon-integrations
    what: "Checklist for third-party APIs, payment and messaging providers, webhook handlers with signature verification, outbound HTTP clients and destinations, service-to-service trust."
    problem: "SSRF and unsafe-consumption scans require knowing every outbound destination and webhook ingress, which stays hidden until integration recon enumerates clients and trust assumptions; outbound inventory, webhook verification, provider mesh, egress clients, implicit trust, partner exposure."
    use_when: "External calls or webhooks exist; SSRF (03) or API10 (19) routing is being decided; signature verification on ingress must be assessed."
    avoid_when: "LLM provider integrations are the topic — see the LLM/AI anchor; internal service boundaries belong to Phase 2."
    expected: "All outbound clients, destinations, and ingress signature checks listed."
  - anchor: analysis-recon-entry-points
    what: "Checklist for HTTP routes, GraphQL operations, gRPC services, CLI commands, WebSocket handlers, SSE streams, MCP endpoints, webhook ingress, scheduled jobs, serverless triggers, with per-point auth and object-ID notes."
    problem: "Every downstream scan keys off entry points, yet incomplete enumeration leaves entire request and message surfaces unexamined across routes, streams, and jobs; route inventory, handler catalog, stream endpoints, job triggers, hidden exposure, attack map."
    use_when: "Building the attack-surface map; per-point authentication and object-identifier acceptance must be recorded; IDOR and missing-auth scans need targets."
    avoid_when: "Internal call chains between services are the question — see data flow; infrastructure listeners belong to infrastructure."
    expected: "Complete entry-point table with method, auth requirement, and identifier acceptance per point."
  - anchor: analysis-recon-llm-ai
    what: "Checklist for model providers, prompt assembly sites, agent frameworks and tool wiring, MCP servers, RAG stores, and model-output-to-sink flows."
    problem: "AI-integrated systems acquire prompt-injection and confused-deputy exposure that classic recon categories never ask about, leaving agent tools and RAG pipelines unmapped; indirect injection, tool authorization, vector stores, output handling, AI perimeter, model egress."
    use_when: "LLM providers, agent frameworks, MCP, or embeddings databases appear in manifests or code; model output reaches SQL, templates, execution, or outbound calls."
    avoid_when: "No AI integration exists in the stack; classic third-party APIs without models belong to integrations."
    expected: "AI surface mapped: model vendors, assembly points, authorized tools, MCP handlers, vector pipelines, output flows."
  - anchor: analysis-recon-resource-limits
    what: "Checklist for rate limits, pagination ceilings, payload and upload sizes, timeouts, memory and process limits, and quotas on paid resources."
    problem: "Resource-consumption scan verdicts depend on documented limits, and missing catalog of ceilings and quotas makes API4 exposure impossible to judge; throttling config, timeout coverage, spending quotas, exhaustion posture, budget drain, unbounded input, availability."
    use_when: "Any endpoint accepts variable-size input; paid third-party resources are consumed; resource-consumption scan (17) routing needs facts."
    avoid_when: "Business-flow abuse rather than volume is the concern — that is API6 territory; server config hardening belongs to security-config."
    expected: "Every limit type recorded with framework, value, and coverage gaps."
  - anchor: analysis-recon-security-config
    what: "Checklist for TLS setup, security headers, CORS policy, debug mode, framework hardening flags, IAM roles, network policies, and logging configuration including PII handling."
    problem: "Misconfiguration scanning needs current hardening posture, yet headers, CORS, debug flags, and logging exposure stay scattered across configs nobody aggregates; header coverage, origin policy, debug leakage, logging hygiene, baseline drift, fragmented settings."
    use_when: "Misconfiguration scan (20) is anticipated; TLS, header, or CORS weaknesses suspected; log contents may include sensitive data."
    avoid_when: "Limit and quota settings are the question — see resource-limits; deployment manifests belong to infrastructure."
    expected: "Configuration baseline captured per topic with file references."
  - anchor: analysis-recon-api-inventory
    what: "Checklist for API versions and negotiation, schema artifacts and their generation, debug and admin interfaces, staging and production hosts, documentation freshness, deprecated endpoints."
    problem: "Inventory-management findings require knowing versions, specs, hosts, and stale endpoints, information normally absent from application code alone; schema freshness, documentation drift, shadow endpoints, retirement plan, spec divergence, beta hosts, sunset dates."
    use_when: "Multiple versions or environments exist; OpenAPI/GraphQL schemas may be stale; inventory scan (18) routing needs evidence."
    avoid_when: "Runtime framework detail is wanted — see frameworks; CI deployment flow belongs to CI/CD mapping."
    expected: "Versions, schemas, hosts, and retired-surface catalogued with freshness notes."
  - anchor: analysis-phase2-intro
    what: "Bridge instruction turning Phase-1 facts into an architecture mental model documented across the eight mapping categories."
    problem: "Facts collected without synthesis yield flat inventory that downstream phases cannot reason about trust, privilege, and flow with; synthesis step, model building, fact digestion, architecture reasoning, mapping transition, context assembly."
    use_when: "Technology reconnaissance is complete; relationships between components must be documented before reporting."
    avoid_when: "Category facts are still missing — finish Phase 1 first; report formatting is the question, see output template."
    expected: "Phase-1 findings organized into the mapping structure ready for documentation."
  - anchor: analysis-map-service-boundaries
    what: "Prompt for classifying the system as monolith, modular monolith, microservices, serverless, or hybrid, with components and protocols between them."
    problem: "Scan scoping differs radically between monolith and distributed systems, and unmapped component boundaries hide service-to-service weaknesses that later phases never suspect; topology classification, component map, inter-service protocols, boundary discovery, structural context, mesh sprawl."
    use_when: "System shape is unknown or assumed; service-to-service calls exist; microservice trust questions feed later scans."
    avoid_when: "Request-level data movement is the question — see data flow; deployment artifacts belong to infrastructure recon."
    expected: "Architecture style and component interaction map documented."
  - anchor: analysis-map-data-flow
    what: "Prompt for tracing registration, login, reset, business actions, upload, payment, and admin flows through parsing, validation, transformation, and serialization stages."
    problem: "Injection and validation findings depend on knowing where input is parsed and transformed, which remains guesswork without journey mapping; input lifecycle, validation points, transformation stages, taint path, processing map, parse order, handler chain, sanitization."
    use_when: "Primary user flows exist; downstream injection scans need taint-relevant paths; parsing and validation locations must be pinned."
    avoid_when: "Static technology facts are missing — return to Phase 1; trust transitions between networks belong to trust boundaries."
    expected: "Each primary flow documented with its parse-validate-transform-serialize stages."
  - anchor: analysis-map-trust-boundaries
    what: "Prompt for locating transitions between trusted and untrusted contexts — user to backend, backend to database, service to service, server to client, internal to external — with controls at each."
    problem: "Unmapped trust transitions leave unclear where validation, authentication, or encryption must exist, so weaknesses surface only during exploitation; boundary mapping, control placement, context transition, encryption points, perimeter shifts, zone crossing, assurance, segmentation."
    use_when: "Multiple zones of trust exist; deciding where controls should be verified by later scans; third-party egress crosses boundaries."
    avoid_when: "Concrete flow steps are wanted — see data flow; infrastructure-level segmentation belongs to infrastructure recon."
    expected: "Every boundary listed with the authentication, validation, or encryption applied there."
  - anchor: analysis-map-privilege-levels
    what: "Prompt for documenting roles, permissions, groups, tenants, enforcement mechanisms, admin panels, impersonation, and centralization of checks."
    problem: "Authorization scans need privilege-model truth, and scattered or duplicated checks across handlers stay invisible until enforcement mapping happens; role hierarchy, enforcement points, tenant separation, admin surface, check duplication, vertical escalation, impersonation."
    use_when: "Roles or tenants exist; BFLA/IDOR scan routing needs the enforcement picture; admin or impersonation features present."
    avoid_when: "Authentication mechanisms are the question — see authn recon; function-level findings themselves are detection work."
    expected: "Role model and enforcement architecture documented, including duplication hotspots."
  - anchor: analysis-map-sensitive-data
    what: "Prompt for inventorying PII, credentials, tokens, financial and health data, their storage, access paths, protections, and leakage into logs, URLs, or errors."
    problem: "Data-exposure assessment stalls without knowing which sensitive types exist, where they live, and whether they leak into logs or URLs; data classification, storage map, leakage channels, protection posture, PII inventory, exposure surface."
    use_when: "Regulated or sensitive data exists; BOPLA and misconfiguration scans need storage and leakage context; logging hygiene must be judged."
    avoid_when: "Secret storage mechanics are the question — see secret management; flow tracing belongs to data flow."
    expected: "Sensitive data types catalogued with storage, access, protection, and leakage notes."
  - anchor: analysis-map-secret-management
    what: "Prompt for documenting how secrets are stored, injected, rotated, and accessed across environments."
    problem: "Hardcoded-secret and misconfiguration scans need to know intended secret handling across environments before flagging deviations in storage, injection, or rotation; key custody, rotation practice, injection method, environment spread, vault usage, credential lifecycle, kms."
    use_when: "Credentials, keys, or certificates exist anywhere; secret scan (15) or misconfiguration scan (20) needs the baseline."
    avoid_when: "Sensitive business data rather than secrets is the topic — see sensitive-data; dependency credentials belong to package managers."
    expected: "Secret types, locations, rotation, and injection mechanisms documented."
  - anchor: analysis-map-logging
    what: "Prompt for capturing logging and monitoring setup: destinations, content, retention, alerting, and whether security events and PII appear."
    problem: "Monitoring gaps and log-borne leakage remain unevaluated when logging topology, destinations, and content were never mapped during recon; observability posture, retention policy, alerting coverage, event visibility, leakage risk, audit trail, siem integration."
    use_when: "Logs or monitoring exist; misconfiguration and design-checklist phases need evidence; PII in logs is suspected."
    avoid_when: "Security configuration flags are the question — see security-config; flow-level tracing belongs to data flow."
    expected: "Logging and monitoring landscape documented with content and retention detail."
  - anchor: analysis-map-cicd
    what: "Prompt for documenting build pipelines, IaC, deployment approvals, credential handling in pipelines, and rollback procedures."
    problem: "Supply-chain and misconfiguration findings need pipeline context, yet build systems, review gates, and credential injection paths are usually undocumented; pipeline inventory, build security, artifact signing, rollback practice, deployment flow, provenance."
    use_when: "CI/CD exists; dependency and misconfiguration scans need build-time context; release pipelines or signing are in play."
    avoid_when: "Runtime infrastructure manifests are the question — see infrastructure recon; dependency manifests belong to package managers."
    expected: "Pipeline stages, gates, and secret handling documented."
  - anchor: analysis-downstream-data
    what: "Lookup table mapping each architecture data item to the scan references that consume it and why."
    problem: "Recon could collect facts nobody uses while missing exact items detection scans require, leaving reports simultaneously bloated and incomplete; consumer mapping, required fields, downstream contract, collection focus, report usefulness, gap prevention."
    use_when: "Planning what to collect; checking that each gathered fact serves a consuming scan; validating report completeness before writing."
    avoid_when: "Category checklists themselves are wanted; OWASP risk rationale is the question — see the OWASP mapping anchor."
    expected: "Collection effort aligns exactly with what downstream scans consume."
  - anchor: analysis-owasp-mapping
    what: "Lookup table mapping architecture data items to OWASP API 2023 risks with the reasoning for each link."
    problem: "Report readers need risk relevance per finding, and ad-hoc tagging produces inconsistent or missing OWASP linkage across recorded items; taxonomy alignment, relevance reasoning, consistent tagging, framework mapping, audit traceability, citation discipline."
    use_when: "Findings must be annotated with OWASP 2023 risks; screener needs risk-to-evidence alignment; reviewing whether a data item justifies a scan."
    avoid_when: "The consuming-scan table is the question — see downstream-data; per-risk trigger detail lives in the screener reference."
    expected: "Every recorded item carries its risk mapping with explicit reasoning."
  - anchor: analysis-output-template
    what: "Exact `01_architecture.md` format: technology stack table, architecture overview, data flow, entry points, auth endpoints, roles, trust boundaries, sensitive data, limits, security config, API inventory, uploads, secrets, CI/CD, supply chain, dynamic loading, JVM, LLM/AI, open questions."
    problem: "Architecture report written in free format breaks downstream consumption and screener parsing, so exact structure and rationale fields matter; report schema, template fidelity, consumer parsing, completeness checklist, format discipline, placeholder marking, schema drift."
    use_when: "All findings gathered and the report must be emitted; a field is unknown or inapplicable and needs correct marking."
    avoid_when: "Recon findings are still incomplete — finish the phase sections first; the meaning of one recon category is the question — see its recon anchor."
    expected: "`01_architecture.md` follows the template section-for-section, with gaps honestly marked and reasons attached."
  - anchor: analysis-reminders
    what: "Guardrails: no vulnerability claims, no source modification, thorough source reading, priority to security-sensitive areas, concrete paths and versions, explicit unknowns."
    problem: "Recon agents drift into speculation, vague claims, or early verdicts under time pressure, corrupting every downstream phase consuming its handoff; speculation control, vagueness ban, evidence demand, scope honesty, quality guardrail, discipline."
    use_when: "Drafting or reviewing the architecture report; tempted to state unverified details; deciding whether to mark something unknown."
    avoid_when: "Specific recon content or template layout is the question — see the recon, mapping, and output anchors; this card only guards report discipline."
    expected: "The report contains only verified, concrete statements, unknowns declared explicitly, and zero vulnerability verdicts or source edits."
---

# Codebase Analysis

[ref: #codebase-analysis]

You are performing the first phase of a security assessment. Your goal is to deeply understand the codebase. You are NOT looking for specific vulnerabilities yet. This is pure reconnaissance.

Create the `{{ REPORTS_ROOT }}/` folder in the project root if it does not already exist. This phase produces exactly one output file inside it:

`{{ REPORTS_ROOT }}/01_architecture.md` — technology stack, architecture, entry points, data flows

## Scope and mission
[ref: #analysis-mission]

The `01_architecture.md` report is the single source of truth for every later phase of this audit: the screener, all detection scan references, and the final report. A detection subagent must be able to read `01_architecture.md` and immediately know where to look, what technologies to expect, and which OWASP API Security Top 10 2023 risks are relevant. Be maximally complete. Do not assume a later phase will re-explore the codebase to fill gaps.

This phase must:

- Identify every technology, framework, and library that affects security behavior.
- Map every entry point that accepts untrusted input.
- Trace the lifecycle of user input through the system.
- Inventory roles, permissions, authentication mechanisms, and sensitive data.
- Record resource limits, security configuration, API inventory, and deployment details.
- Map each finding to the OWASP API Security Top 10 2023 risks it enables.

This phase must NOT:

- Report specific vulnerabilities such as "line 42 has SQL injection".
- Modify project source code or configuration files.
- Run exploits, scanners, or tests that alter state.
- Make risk ratings or business-impact judgments.

## Phase 1: Technology Reconnaissance
[ref: #analysis-phase1-intro]

Start by reading dependency manifests, project configs, and directory structure. Then drill into source code to confirm findings. If the codebase is large, prioritize entry points, configuration, and security-sensitive flows rather than exhaustive line-by-line review.

For each category below, record concrete values: names, versions, file paths, and configuration files. When a value is ambiguous, state the ambiguity explicitly and list the evidence.

### Languages
[ref: #analysis-recon-languages]

- All programming languages used and their versions if specified.
- Version sources: `.python-version`, `pyproject.toml`, `package.json` `engines`, `go.mod`, `pom.xml`, `Cargo.toml`, `Gemfile`, `Dockerfile` base images, CI matrixes.
- Note any polyglot boundaries where data crosses between languages or runtimes.

### Frameworks
[ref: #analysis-recon-frameworks]

- Web frameworks (e.g., FastAPI, Django, Flask, Express, NestJS, Fastify, Hono, Spring Boot, Micronaut, Quarkus, Ktor, ASP.NET Core, Ruby on Rails, Gin, Echo, Fiber, Axum).
- GraphQL servers and gateways (e.g., Apollo Server/Router, graphql-yoga, Hasura, PostGraphile, gqlgen, Strawberry, Ariadne, spring-graphql).
- RPC/API layers (e.g., tRPC, gRPC, Connect-RPC, JSON-RPC).
- ORM layers (e.g., SQLAlchemy, Django ORM, Hibernate, Prisma, GORM, Entity Framework).
- Template engines (e.g., Jinja2, Thymeleaf, EJS, Handlebars).
- Task queues and background workers (e.g., Celery, Sidekiq, Bull, RQ, Temporal).
- Testing frameworks and mock servers that may expose debug endpoints.

### Serialization and data binding
[ref: #analysis-recon-serialization]

- Generic serializers (e.g., Pydantic, Marshmallow, Django REST Framework serializers, Jackson, Gson).
- Auto-binding and mass-assignment libraries.
- PATCH, partial-update, or merge handlers.
- GraphQL resolver patterns and field-level access controls.
- Form parsers, multipart handlers, JSON/XML/YAML parsers, and their strictness settings.
- DTO/Request/Command classes and where they are defined.

### Package managers and dependencies
[ref: #analysis-recon-package-managers]

- Lock files and dependency manifests: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `requirements.txt`, `requirements.lock`, `uv.lock`, `poetry.lock`, `go.mod`, `go.sum`, `Gemfile.lock`, `pom.xml`, `Cargo.lock`, `composer.lock`, etc.
- Registry configuration and scope pinning: `.npmrc`, `.yarnrc`, `pip.conf`, `maven` settings, `NuGet.config`, private registry URLs.
- Internal/private package names and whether their scopes are locked to a private registry (dependency-confusion exposure).
- Direct and transitive dependencies with known security relevance: authentication libraries, HTTP clients, template engines, XML parsers, PDF/image processors, cryptography libraries.
- Install/lifecycle scripts (`postinstall`, `preinstall`, `setup.py` hooks) declared by dependencies.
- Dependency-update cadence and whether automated scanning (SCA/SBOM) is configured.
- Supply-chain integrity controls: lockfile enforcement in CI (`npm ci`, `--ignore-scripts`), package provenance attestations (Sigstore, npm provenance), artifact signing, checksum pinning (`pip install --require-hashes`, Go checksum database).
- Maintainer metadata for critical dependencies: number of maintainers, MFA policy, recent activity, signed releases.

### JVM-specific facilities (Kotlin / Java)
[ref: #analysis-recon-jvm]

- Serialization libraries and configurations: `ObjectInputStream`, Jackson `ObjectMapper` default typing / `@JsonTypeInfo`, XStream, Kryo, SnakeYAML, Fastjson, Gson, JSON-B, JAXB, RMI/JRMP, HTTP invoker.
- JNDI usage: `InitialContext.lookup`, `DirContext.search`, `NamingManager.getObjectInstance`; logging framework lookup substitution settings.
- Class loading: custom `ClassLoader` subclasses, `URLClassLoader`, `MethodHandles.Lookup.defineClass`, bytecode generation libraries (`ByteBuddy`, `ASM`, `Javassist`, `cglib`).
- Native code: JNI declarations, `System.loadLibrary`, `Runtime.load`, `ProcessBuilder` compiling native code.
- Reflection: Java `java.lang.reflect` and Kotlin `KClass`, `KCallable.callBy`, `memberFunctions`, `declaredMemberProperties`.
- Compiler plugins and code generation: KSP `SymbolProcessor`, Java `AbstractProcessor`, code generation driven by schemas or external files.
- Scripting: `ScriptEngine`, `GroovyShell`, `KotlinScriptEngine`, Nashorn (removed from the JDK since 15 — relevant only on JDK ≤14 or via the standalone `nashorn-core` artifact; GraalJS is the modern replacement).
- Remote management: RMI registries, `JMXConnectorServer`, exported MBeans.
- Instrumentation: `java.lang.instrument`, `premain`/`agentmain`, attach API.
- Dynamic invocation: `MethodHandle`, `invokedynamic`, `LambdaMetafactory`, dynamic proxies.
- Low-level access: `sun.misc.Unsafe`, `VarHandle`, `MemorySegment`, `Arena`, Panama foreign-function API.

### Infrastructure hints
[ref: #analysis-recon-infrastructure]

- Dockerfiles, docker-compose files, Kubernetes manifests, Helm charts, Terraform, Pulumi, CI/CD configs.
- Base images, exposed ports, runtime users, capabilities, read-only filesystem settings.
- Service mesh, reverse proxy, load balancer, WAF, or API gateway presence.
- Cloud provider services and IAM roles.

### Databases and storage
[ref: #analysis-recon-databases]

- SQL databases (e.g., PostgreSQL, MySQL, SQL Server, SQLite).
- NoSQL databases (e.g., MongoDB, DynamoDB, Redis, Cassandra, Elasticsearch).
- Cache layers and message brokers (e.g., Redis, Memcached, RabbitMQ, Kafka, SQS).
- Connection strings, ORM models, migration files, query builders, raw SQL files.
- File storage backends (local filesystem, S3, GCS, Azure Blob, MinIO).

### Authentication and authorization
[ref: #analysis-recon-authn]

- Auth libraries, middleware, and decorators (e.g., OAuth2, OIDC, JWT, session cookies, API keys, HMAC, mTLS).
- Token issuance, validation, refresh, revocation, and expiry configuration.
- Session configs: store, cookie flags (`HttpOnly`, `Secure`, `SameSite`), TTL.
- Role/permission models, access-control lists, attribute-based access control, policy engines.
- Admin panel presence and how admin privileges are granted.
- Modern authentication mechanisms: passkeys/WebAuthn (baseline since ~2024), OAuth 2.1 (still an IETF Internet-Draft as of 2026-07 — `draft-ietf-oauth-v2-1-15`, 2026-03; PKCE mandatory; obsoletes RFC 6749/6750 once published), FAPI 2.0 (Final Specification since 2025-02), DPoP/sender-constrained tokens (RFC 9449), token exchange (RFC 8693), workload identity (SPIFFE/SPIRE).
- Public, authenticated, and internal-only endpoints.

### External integrations
[ref: #analysis-recon-integrations]

- Third-party APIs, payment processors, email services, SMS gateways, cloud SDKs.
- Webhook handlers and signature verification methods.
- Outbound HTTP clients and destinations (e.g., `requests`, `httpx`, `axios`, `fetch`, `RestTemplate`, `HttpClient`).
- Service-to-service authentication and trust assumptions.

### Entry points
[ref: #analysis-recon-entry-points]

- HTTP routes and route tables.
- GraphQL schemas, queries, mutations, subscriptions.
- gRPC service definitions and proto files.
- CLI commands and their arguments.
- WebSocket handlers and message formats.
- Server-Sent Events (SSE) streams.
- MCP (Model Context Protocol) server endpoints: tool calls, resources, prompts, and their transports (stdio, Streamable HTTP; the HTTP+SSE transport from protocol 2024-11-05 is deprecated since 2025-03-26 — new implementations use Streamable HTTP).
- Webhook ingress endpoints and their signature verification.
- Scheduled jobs, cron expressions, and message consumers.
- Serverless functions, event triggers, and hooks.

For each entry point, record: path/pattern, HTTP method or message type, whether authentication is required, and whether it accepts user-supplied object IDs or slugs.

### LLM/AI integration
[ref: #analysis-recon-llm-ai]

- Model endpoints and providers: OpenAI, Anthropic, Azure OpenAI, Bedrock, Vertex, self-hosted (vLLM, Ollama, TGI); streaming responses.
- Prompt construction sites: templates, system prompts, and every place where user input, retrieved documents, or tool results are concatenated into prompts (direct and indirect prompt-injection surface).
- Agent frameworks and tool wiring: LangChain/LangGraph, LlamaIndex, CrewAI, AutoGen, OpenAI Agents SDK, Google ADK; which tools (file system, shell, HTTP fetch, database) agents may call and how those calls are authorized.
- MCP servers and clients: `mcp` SDK usage, tool registrations, resource and prompt definitions, transport, and authentication on tool-call handlers.
- RAG stores and vector databases: pgvector, Qdrant, Weaviate, Pinecone, Milvus, Chroma; ingestion pipelines processing untrusted documents.
- Guardrails and output handling: where model output reaches sinks (SQL, templates, code execution, outbound requests) without validation.

### Resource limits and rate limiting
[ref: #analysis-recon-resource-limits]

- Framework-level rate limits per route, user, IP, or global.
- Pagination parameters and maximum page sizes.
- Max body/payload sizes.
- Max upload sizes.
- Execution timeouts per request, job, or query.
- Memory, CPU, process, connection, and queue-size limits.
- Quotas for paid resources such as SMS, email, or biometric checks.

### Security configuration
[ref: #analysis-recon-security-config]

- HTTPS/TLS setup and minimum TLS version.
- Security headers (`HSTS`, `X-Frame-Options`, `CSP`, `X-Content-Type-Options`, etc.).
- CORS policy: allowed origins, methods, headers, credentials.
- Debug mode, stack-trace exposure, and verbose error pages.
- Framework hardening settings (e.g., `DEBUG`, `SECRET_KEY`, CSRF protection, clickjacking protection).
- Cloud/container IAM roles and network policies.
- Logging configuration: what is logged, where, retention, and whether PII is included.

### API inventory and environments
[ref: #analysis-recon-api-inventory]

- API versions and version negotiation strategy.
- OpenAPI, AsyncAPI, GraphQL schemas, and whether they are generated from code or maintained manually.
- Debug endpoints, health checks, metrics, and admin interfaces.
- Production, staging, development, and review-app hosts.
- Documentation freshness and divergence from code.
- Deprecated endpoints that remain deployed.

## Phase 2: Architecture Mapping
[ref: #analysis-phase2-intro]

Based on Phase 1, build a mental model and document the following.

### Service boundaries
[ref: #analysis-map-service-boundaries]

- Is this a monolith, modular monolith, microservices, serverless, or hybrid?
- What are the major components, services, or modules?
- What talks to what, and over which protocols?

### Data flow
[ref: #analysis-map-data-flow]

- How does user input enter the system, get processed, get stored, and get returned?
- Trace primary flows such as registration, login, password reset, core business actions, file upload, payment, and admin operations.
- Identify where input is parsed, validated, transformed, and serialized.

### Trust boundaries
[ref: #analysis-map-trust-boundaries]

- Where does the system transition between trusted and untrusted contexts?
  - User input to backend.
  - Backend to database.
  - Service to service.
  - Server to client.
  - Internal network to external API.
- What authentication, validation, or encryption applies at each boundary?

### Privilege levels
[ref: #analysis-map-privilege-levels]

- What roles, permissions, groups, tenants, or organizations exist?
- How are they enforced? Middleware, decorators, explicit checks, policy engines?
- Is there an admin panel, superuser role, or impersonation feature?
- Are privilege checks centralized or duplicated across handlers?

### Sensitive data inventory
[ref: #analysis-map-sensitive-data]

- PII, credentials, tokens, financial data, health records, secrets, session identifiers.
- Where each type is stored, how it is accessed, and what protection is applied at rest and in transit.
- Whether sensitive data appears in logs, URLs, query parameters, or error messages.

### Secret management
[ref: #analysis-map-secret-management]

- Where API keys, database credentials, signing keys, certificates, and encryption keys are stored.
- Distinguish between env vars, secret managers (e.g., Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager), source code, config files, and CI variables.
- Note rotation policy hints and key derivation practices.

### Logging and monitoring
[ref: #analysis-map-logging]

- Which security events are logged: authentication success/failure, authorization failures, input-validation failures, rate-limit hits, file uploads, sensitive data access.
- Whether logs include PII, tokens, or passwords.
- Whether failed auth, access-control, or input-validation events trigger alerts.
- Log aggregation, SIEM, or observability tooling.

### CI/CD and deployment
[ref: #analysis-map-cicd]

- Build pipelines and their stages.
- Infrastructure-as-Code and environment separation.
- Container hardening, image scanning, and runtime security.
- Dependency-update cadence and automated security scanning.
- Deployment approvals, secrets injection, and rollback procedures.

## Data items required by downstream references
[ref: #analysis-downstream-data]

The table below links each architecture data item to the detection references that consume it. If a data item is missing, downstream detection may miss vulnerabilities.

| Data item | Required by | Why it matters |
|---|---|---|
| Object-ID access patterns in entry points | `08-idor.md`, `00-screener.md` | BOLA exists when functions accept object IDs without per-object authorization. |
| Auth endpoints, session/token mechanisms, role model | `10-missingauth.md`, `09-jwt.md`, `00-screener.md` | Weak or missing auth allows account takeover and privilege escalation. |
| Serializers / auto-binding / mass-assignment frameworks | `16-bopla.md`, `00-screener.md` | Unrestricted data binding leaks or mutates sensitive object properties. |
| Rate limits, pagination, payload size, resource budgets | `17-resourceconsumption.md`, `10-missingauth.md` | Missing limits enable resource exhaustion and brute force. |
| Role/permission model and admin endpoint inventory | `08-idor.md`, `10-missingauth.md`, `00-screener.md` | Complex roles without clear separation lead to horizontal/vertical privilege escalation. |
| Sensitive business flow endpoints | `13-businesslogic.md`, `00-screener.md` | Automated abuse of flows harms business without being an implementation bug. |
| Outbound HTTP clients and third-party integrations | `03-ssrf.md`, `19-unsafeapiconsumption.md`, `00-screener.md` | Unvalidated outbound URIs and over-trusted third-party data enable SSRF and supply-chain attacks. |
| Security configuration (TLS, headers, CORS, debug mode) | `20-misconfiguration.md`, `00-screener.md` | Default/verbose configurations expose the API to multiple attack classes. |
| API versions, specs, debug endpoints, non-prod hosts | `18-inventory.md`, `20-misconfiguration.md`, `00-screener.md` | Undocumented or deprecated endpoints bypass security controls and monitoring. |
| File upload handling and storage patterns | `11-fileupload.md`, `12-pathtraversal.md`, `17-resourceconsumption.md`, `00-screener.md` | Insecure upload handling leads to code execution, path traversal, and resource abuse. |
| Secret management and hardcoded credentials | `15-hardcodedsecrets.md`, `09-jwt.md`, `00-screener.md` | Exposed secrets enable authentication bypass and data decryption. |
| Logging and monitoring | `20-misconfiguration.md`, `99-report.md` | Incomplete logging hides attacks and complicates incident response. |
| Input validation and query building patterns | `02-sqli.md`, `04-xss.md`, `12-pathtraversal.md`, `00-screener.md` | Validation gaps and unsafe query construction enable injection attacks. |
| Dependency manifests, registry config, internal scopes, install scripts, update cadence | `23-dependencies.md`, `00-screener.md` | Typosquatting, dependency confusion, known CVEs, abandoned packages, maintainer takeovers, and compromised packages are detected from dependency metadata. |
| Dynamic loading, reflection, plugin/extension systems, runtime code generation | `21-backdoors.md`, `05-rce.md`, `00-screener.md` | Deliberate malicious code and unauthorized execution surfaces hide behind dynamic invocation. |
| Obfuscation patterns: encoded strings, control-flow flattening, decryption loops, encrypted payloads | `22-obfuscation.md`, `21-backdoors.md`, `00-screener.md` | Obfuscation can conceal backdoors, C2 addresses, and malicious payloads. |
| JVM-specific facilities (deserialization, JNDI, ClassLoaders, JNI, Kotlin reflection, KSP, scripting, RMI/JMX, instrumentation, MethodHandle, Unsafe) | `24-jvm-anomalies.md`, `05-rce.md`, `00-screener.md` | JVM-specific mechanisms can bypass type safety and execute attacker-controlled code. |
| CI/CD and deployment practices | `20-misconfiguration.md`, `15-hardcodedsecrets.md`, `23-dependencies.md` | Pipeline weaknesses introduce supply-chain and configuration risks. |

## OWASP API Security Top 10 2023 mapping
[ref: #analysis-owasp-mapping]

The architecture data items below are the single source of truth for the screener and all detection references. Map each item to the OWASP API 2023 risks it enables.

| Architecture data item | OWASP API 2023 risk(s) | Why it matters |
|---|---|---|
| Object-ID access patterns in entry points | API1:2023 Broken Object Level Authorization | BOLA exists because functions accept object IDs without per-object authorization checks. |
| Auth endpoints, session/token mechanisms, role model | API2:2023 Broken Authentication, API5:2023 Broken Function Level Authorization | Weak auth or missing function-level checks allow account takeover and privilege escalation. |
| Serializers / auto-binding / mass-assignment frameworks | API3:2023 Broken Object Property Level Authorization | Unrestricted data binding leaks or mutates sensitive object properties. |
| Rate limits, pagination, payload size, resource budgets | API4:2023 Unrestricted Resource Consumption | Missing limits let attackers exhaust resources or run up costs. |
| Role/permission model and admin endpoint inventory | API5:2023 Broken Function Level Authorization | Complex roles without clear separation lead to horizontal/vertical privilege escalation. |
| Sensitive business flow endpoints (purchase, post, book) | API6:2023 Unrestricted Access to Sensitive Business Flows | Automated abuse of flows harms business without being an implementation bug. |
| Outbound HTTP clients and third-party integrations | API7:2023 Server Side Request Forgery, API10:2023 Unsafe Consumption of APIs | Unvalidated outbound URIs and over-trusted third-party data enable SSRF and supply-chain attacks. |
| Security configuration (TLS, headers, CORS, debug mode) | API8:2023 Security Misconfiguration | Default/verbose configurations expose the API to multiple attack classes. |
| Dynamic loading, reflection, plugin systems, install scripts, obfuscated dependency code | API8:2023 Security Misconfiguration, API10:2023 Unsafe Consumption of APIs | Deliberate implants and obfuscated payloads hide in dynamic execution paths and third-party code. |
| Dependency supply chain (registry scoping, manifests, lockfiles, maintainer trust, known CVEs) | API8:2023 Security Misconfiguration, API10:2023 Unsafe Consumption of APIs | Vulnerable, abandoned, typosquatted, confused, or compromised dependencies introduce supply-chain risk. |
| JVM-specific facilities (deserialization, JNDI, reflection, ClassLoaders, JNI, KSP, scripting, RMI/JMX, instrumentation, MethodHandle, Unsafe) | API5:2023 Broken Function Level Authorization, API8:2023 Security Misconfiguration, API10:2023 Unsafe Consumption of APIs | JVM mechanisms can invoke privileged functions, load untrusted classes, or execute third-party payloads without adequate hardening. |
| LLM/AI integration (prompt construction, agent tool wiring, MCP servers, model output reaching sinks) | API5:2023 Broken Function Level Authorization, API7:2023 Server Side Request Forgery, API10:2023 Unsafe Consumption of APIs | Unvalidated model output and over-privileged agent tools enable injection, request forgery, and unauthorized actions. |
| API versions, specs, debug endpoints, non-prod hosts | API9:2023 Improper Inventory Management | Undocumented or deprecated endpoints bypass security controls and monitoring. |

## Output template
[ref: #analysis-output-template]

Write the results of Phase 1 and Phase 2 to `{{ REPORTS_ROOT }}/01_architecture.md` using exactly this format. Replace bracketed placeholders with concrete findings. If a field is not applicable, write "N/A" and briefly explain why. If a field is unknown, write "Unknown" and describe what evidence is missing.

```markdown
# Architecture: [Project Name]

## Technology Stack

| Category | Details |
|---|---|
| Languages | ... |
| Frameworks | ... |
| Databases | ... |
| Auth mechanism | ... |
| Infrastructure | ... |
| External services | ... |
| Serialization & data binding | ... |

## Architecture Overview

[Describe the architecture: monolith vs microservices, how components interact,
main modules and their responsibilities. Mention any API gateway, reverse proxy,
load balancer, or service mesh.]

## Data Flow

[Trace how user input enters the system, gets processed, stored, and returned.
Cover the primary flows such as registration, login, password reset, core
business actions, file upload, payment, and admin operations. Identify parsing,
validation, transformation, and serialization steps.]

## Entry Points

| Entry Point | Type | Auth Required | User-Supplied Object IDs/Slugs | Description |
|---|---|---|---|---|
| ... | HTTP/GraphQL/WS/etc. | Yes/No | Yes/No — field name | ... |

## Authentication Endpoints

| Endpoint | Type | Purpose | Notes |
|---|---|---|---|
| ... | ... | login/register/reset/2FA/etc. | ... |

## Role & Permission Model

[Roles, permissions, how they are enforced, admin panel presence, and any
role hierarchy or group/tenant separation. List admin, internal, or privileged
endpoints separately if applicable.]

## Trust Boundaries

[List each trust boundary and what crosses it: user input to backend,
backend to database, service to service, server to client, internal to external
API. Include the authentication/validation/encryption applied at each.]

## Sensitive Data Inventory

| Data Type | Where Stored | How Accessed | Protection |
|---|---|---|---|
| ... | ... | ... | ... |

## Resource Limits & Rate Limiting

| Limit Type | Framework/Config | Value/Behavior | Notes |
|---|---|---|---|
| Rate limiting | ... | ... | ... |
| Pagination max | ... | ... | ... |
| Max payload/body | ... | ... | ... |
| Max upload size | ... | ... | ... |
| Execution timeout | ... | ... | ... |
| Memory/CPU/process limits | ... | ... | ... |

## Security Configuration

| Topic | Current State | Notes |
|---|---|---|
| HTTPS/TLS | ... | ... |
| Security headers | ... | ... |
| CORS policy | ... | ... |
| Debug mode | ... | ... |
| Framework hardening | ... | ... |
| Cloud/container IAM | ... | ... |
| Logging/monitoring | ... | ... |

## API Inventory & Environments

| Item | Details |
|---|---|
| API versions | ... |
| OpenAPI/AsyncAPI/GraphQL schemas | ... |
| Debug endpoints | ... |
| Production hosts | ... |
| Staging/dev/review hosts | ... |
| Documentation freshness | ... |

## File Upload Handling

| Aspect | Details |
|---|---|
| Upload endpoints | ... |
| Storage backend | ... |
| File-type/size validation | ... |
| Path construction | ... |

## Secret Management

| Secret Type | Storage Location | Rotation/Notes |
|---|---|---|
| API keys | ... | ... |
| DB credentials | ... | ... |
| Signing keys / certificates | ... | ... |

## CI/CD & Deployment

[Build pipelines, Infrastructure-as-Code, container hardening, dependency-update
cadence, deployment approvals, secrets injection, and rollback procedures.]

## Dependency Supply Chain

| Aspect | Details |
|---|---|
| Package manager(s) | ... |
| Registry configuration / scope pinning | ... |
| Internal/private package names and scopes | ... |
| Dependency-update cadence | ... |
| SCA/SBOM tooling | ... |
| Known risky dependencies | ... |
| Install/lifecycle scripts in dependencies | ... |

## Dynamic Loading / Reflection / Plugin Systems

| Aspect | Details |
|---|---|
| Dynamic module loading patterns | ... |
| Reflection APIs in use | ... |
| Plugin/extension system and allowlist | ... |
| Runtime code generation or eval/exec sinks | ... |
| Obfuscation or encoded payload patterns | ... |

## JVM-Specific Facilities

| Aspect | Details |
|---|---|
| Java/Kotlin serialization and polymorphic typing | ... |
| JNDI usage and lookup substitution in logging | ... |
| Custom ClassLoaders / bytecode generation | ... |
| JNI / native library loading | ... |
| Kotlin reflection and dynamic dispatch | ... |
| KSP / compiler plugins and code generation inputs | ... |
| Scripting engines (JS, Groovy, Kotlin script) | ... |
| RMI / JMX exposure and authentication | ... |
| Instrumentation / agents | ... |
| MethodHandle / invokedynamic / dynamic proxies | ... |
| Unsafe / off-heap / foreign-function access | ... |

## LLM/AI Integration

| Aspect | Details |
|---|---|
| Model providers / endpoints | ... |
| Prompt construction sites (user input, RAG, tool results) | ... |
| Agent frameworks and authorized tools | ... |
| MCP servers / tool-call authentication | ... |
| RAG stores / vector databases | ... |
| Model-output-to-sink flows | ... |

## Open Questions and Ambiguities

[List any architectural details that could not be determined, the evidence you
examined, and what a later phase should verify.]
```

## Important reminders
[ref: #analysis-reminders]

- Do NOT report specific vulnerabilities (like "line 42 has SQL injection"). That comes in later phases.
- Do NOT modify project source code. Write only to `{{ REPORTS_ROOT }}/01_architecture.md`.
- Be thorough in exploration. Read actual source code, not just config files. Look at how auth middleware is applied, how queries are built, how file uploads are handled, and how outbound requests are constructed.
- If the codebase is large, prioritize security-sensitive areas: auth, payment, data access, file handling, admin functionality.
- Record concrete file paths, configuration keys, and versions whenever possible. Vague statements such as "uses JWT" are insufficient; specify the library, configuration file, and token handling flow.
- Mark unknowns explicitly. Do not invent details to make the report look complete.
- Preserve the placeholder `{{ REPORTS_ROOT }}` exactly as written; do not substitute it with a literal path in this reference.
