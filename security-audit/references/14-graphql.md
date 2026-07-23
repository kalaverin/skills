---
subject: "GraphQL injection detection reference for SAST subagents: document-assembly definition with scope exclusions, surface-issues table, per-stack vulnerable/secure recipes incl. FastAPI, prevention patterns and guidance, CWE list, three-phase execution with early-exit gates, advanced patterns incl. MCP/AI exposure, OWASP API mapping."
index:
  - anchor: graphql-detection
    what: "Focused GraphQL-injection detection role using the three-phase subagent approach — technology recon, batched taint verify, merge — gated on the architecture report."
    problem: "Codebase may assemble GraphQL operation documents from user input anywhere across servers, gateways, and BFF proxies, and unstructured hunting misses assembly sites while flooding reviewers with unverified candidates; detection orchestration, phase pipeline, document taint, audit rigor, coverage goal, methodical triage, reviewer fatigue."
    use_when: "GraphQL scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-phase detection must run."
    avoid_when: "Architecture summary absent — run the analysis module first; only conceptual knowledge is needed, not execution."
    expected: "Verified injection findings consolidated into the module report with false positives filtered."
  - anchor: graphql-definition
    what: "Core definition: user-controlled data embedded into the GraphQL operation document text itself, letting attacker syntax reach the parser instead of staying inside the variables map."
    problem: "Reviewers disagree on what counts as document injection versus ordinary argument passing, so resolver SQLi and variable binding get flagged while real text-assembly flaws slip; concept baseline, shared vocabulary, parser trust boundary, classification consistency, definition anchor, term alignment."
    use_when: "Onboarding to the scan; deciding whether a behavior belongs to this vulnerability class at all."
    avoid_when: "Concrete code recipes are needed — jump to the examples anchor; execution workflow is the question."
    expected: "Everyone applies one test: user input must never alter operation text, only variable values."
  - anchor: graphql-scope-in
    what: "Positive scope: construction patterns that count as injection — concatenation or interpolation into operation strings, dynamic `gql` template literals, forwarded bodies re-wrapped, persisted-query maps without allowlisting."
    problem: "Detectors under-report when inclusion rules stay implicit, missing string-built documents across HTTP proxies, server wrappers, and downstream gateway clients; assembly patterns, missed sites, hidden vectors, recon breadth, forwarding paths, template misuse, candidate recall, coverage gaps."
    use_when: "Running recon for candidate assembly sites; judging whether a found code shape qualifies."
    avoid_when: "Exclusion boundaries are the question — see the scope-out anchor; prevention design wanted."
    expected: "Every unsafe document-assembly pattern is captured during recon."
  - anchor: graphql-scope-out
    what: "Negative scope: patterns explicitly not flagged here — resolver SQL/NoSQL injection, IDOR through variables on static documents, normal variable binding, introspection exposure, depth and complexity denial of service."
    problem: "Verify batches drown in false positives when boundary rules stay unwritten, burning taint-tracing effort on authorization gaps and resolver bugs owned by other modules; misrouted findings, wasted tracing, scope discipline, class confusion, triage accuracy, batch noise, ownership boundaries."
    use_when: "A candidate looks like injection but might be authorization or resolver-layer; classifying borderline patterns."
    avoid_when: "Inclusion patterns are the question — see the scope-in anchor; surface-hardening issues are wanted."
    expected: "Borderline candidates route to the correct module instead of inflating injection findings."
  - anchor: graphql-surface-issues
    what: "Twelve-row surface-issue table: introspection, field suggestions, debug UIs, depth and complexity abuse, batching, resolver and subscription auth gaps, directive injection, CSRF, uploads, federation trust, cache poisoning, MCP/AI exposure — each with detection focus and OWASP mapping."
    problem: "Recon focused only on document assembly misses hardening gaps that let attackers map schemas, bypass rate limits, or reach resolvers sideways, leaving reports blind to non-injection GraphQL risk; schema mapping, sideways access, visibility gaps, exposure inventory, adjacent risk, recon breadth, limit evasion."
    use_when: "Phase 1 recon must record GraphQL-specific surface findings; reviewing whether a hardening gap belongs in the report."
    avoid_when: "Injection candidate hunting is the current step — see scope anchors; remediation checklist wanted."
    expected: "Recon records every applicable surface issue with classification and evidence."
  - anchor: graphql-prevention-patterns
    what: "Seven numbered prevention patterns with code: static documents plus variables, single-parse server handlers, persisted-query allowlists, `Source` with `variableValues`, introspection disabled, depth and cost limits, per-resolver authorization."
    problem: "Remediation advice without canonical safe shapes leaves implementers guessing which construction idiom is actually acceptable, so fixes reintroduce string assembly under new wrappers; reference idioms, fix guidance, wrapper drift, secure defaults, implementation clarity, remediation patterns, hardening baseline."
    use_when: "Designing or reviewing fix patterns for flagged assembly sites; onboarding to secure GraphQL construction."
    avoid_when: "Vulnerable counterparts are needed for comparison — see the examples anchor; the checklist form is wanted."
    expected: "Fixes adopt variable-bound idioms instead of rewrapped string building."
  - anchor: graphql-examples
    what: "Per-stack vulnerable/secure recipe pairs: Node.js proxy, Python format-into-`execute`, Apollo Server, graphql-js, Strawberry, Graphene, FastAPI, graphql-java, Sangria — each pairing string assembly with the variable-bound fix."
    problem: "Framework execution idioms differ wildly, and generic injection rules miss how each stack actually feeds document text into parsers, executors, and HTTP bodies; executor diversity, precise detection, pattern matching, call shapes, binding styles, parser entry, taint anchors."
    use_when: "Target uses one of the covered stacks; reviewing resolvers, proxy endpoints, or gateway clients."
    avoid_when: "Conceptual scope is the question — see definition anchors; prevention checklist wanted."
    expected: "Stack-specific assembly sites flagged; variable-bound forms verified safe."
  - anchor: graphql-prevention-guidance
    what: "Layered hardening checklist: static documents with variables, fragment allowlists, introspection off, depth and complexity limits, complexity-based rate limiting, per-field authorization, subscription auth, persisted queries, upstream response validation, debug UIs removed, CSRF controls, upload limits, federation hardening, MCP endpoint authentication."
    problem: "Remediation scattered across framework docs leaves gaps that let one missing control reopen document injection or adjacent abuse; control mapping, defense completeness, gap elimination, hardening steps, systematic mitigation, closure guarantee, audit-ready fixes."
    use_when: "Writing remediation for confirmed findings; auditing whether deployed defenses are complete."
    avoid_when: "Detection mechanics are the question — see execution anchors; canonical code shapes wanted."
    expected: "Every finding closes with a complete, layered control set."
  - anchor: graphql-cwe-mapping
    what: "CWE list per GraphQL weakness: input validation, injection, SQL downstream, information exposure, authorization, CSRF, resource consumption, user-controlled key bypass, allocation limits, dynamic attribute modification, SSRF."
    problem: "Wrong weakness identifiers break downstream tooling and metrics, especially when injection, authorization, and resource classes blur across one finding; weakness taxonomy, misclassification risk, tooling accuracy, identifier precision, reporting feeds, scanner alignment, cwe tagging."
    use_when: "Assigning CWE identifiers to GraphQL findings."
    avoid_when: "OWASP risk framing is the question — see the OWASP anchor."
    expected: "Each finding carries the most specific applicable CWE."
  - anchor: graphql-execution
    what: "Three-phase execution: technology recon with dual early-exit gates (no GraphQL, zero candidates), batched taint verify in groups of three sites, orchestrator merge into the final module report."
    problem: "Detection work without orchestration duplicates effort, loses batch boundaries, skips early exits, and merges findings inconsistently; execution model, phase overview, batch discipline, workflow entry, staging, dispatch plan, consolidation, handoff clarity, gate logic."
    use_when: "Starting the GraphQL scan execution; dispatching or reviewing any phase or gate."
    avoid_when: "Conceptual knowledge is the need — see definition and scope anchors."
    expected: "All phases run with shared architecture context into one consolidated report."
  - anchor: graphql-advanced-patterns
    what: "Less-obvious attack patterns: cost-analysis abuse, live query and subscription leaks, federation stitching trust, GET-based CSRF, multipart uploads, cache poisoning, directive injection, alias overloading, MCP/AI tool exposure, engine-level CVEs."
    problem: "Standard sweeps catch obvious string assembly yet miss quiet vectors where expensive resolvers, trusted gateways, or AI tool bridges expose data without any injected syntax; second-order abuse, federation risks, cost evasion, cache risks, exotic paths, resolver strain."
    use_when: "Recon needs depth beyond textbook injection; manual review of odd architectures, gateways, subscriptions, or AI integrations."
    avoid_when: "Basic candidate hunting is unfinished — finish recon first; remediation checklist wanted."
    expected: "Non-obvious exposure paths surface alongside classic injection candidates."
  - anchor: graphql-owasp-mapping
    what: "OWASP API 2023 mapping table: API1 BOLA, API2 authentication, API4 resource consumption, API5 function authorization, API8 misconfiguration, API10 unsafe consumption — with GraphQL manifestations and source-file citations."
    problem: "Findings need correct 2023-era taxonomy for reporting, and mislabeling GraphQL-specific manifestations misroutes everything downstream into wrong risk buckets; risk routing, classification accuracy, edition awareness, correct tagging, traceability, risk labels, label drift."
    use_when: "Tagging findings with OWASP 2023 risks; writing the report's risk section."
    avoid_when: "CWE-level tagging is the question — see the CWE anchor."
    expected: "Findings mapped to correct API risks with explicit GraphQL reasoning."
  - anchor: graphql-important-reminders
    what: "Closing operational constraints: read-only subagents, phase ordering, gate behavior, batch size of three, parallel dispatch, per-batch context slicing, taint only in verify, resolver issues routed out, conservative classification, intermediate cleanup."
    problem: "Modules close with inconsistent final guidance, letting unverified traces, giant contexts, or premature deletion slip into audit runs and client deliverables; closing rules, quality floor, consistency, final reminders, weak evidence, uniform endings, wrap discipline, audit closure."
    use_when: "Finalizing the module report; reviewing operational constraints before dispatch."
    avoid_when: "Detection or execution is the current stage — finish those first."
    expected: "Runs close with uniform operational rules applied."
  - anchor: graphql-references
    what: "External link list: OWASP cheat sheets, Apollo MCP Server documentation, Apollo Server migration guide, and the OWASP API 2023 source files this reference cites."
    problem: "Agents and readers need authoritative follow-up sources beyond this file's distilled content when deeper verification or version details are required; further reading, external canon, deep dives, vendor documentation, primary material, cited works, owasp pages."
    use_when: "Primary sources or extended material is needed."
    avoid_when: "Detection recipes or execution workflow are the question — this list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
---

# GraphQL Injection Detection

[ref: #graphql-detection]

You are performing a focused security assessment to find GraphQL injection vulnerabilities and related GraphQL security weaknesses. This skill uses a three-phase approach with subagents: **recon** (confirm GraphQL usage, find every location where a GraphQL operation document is assembled unsafely, and record GraphQL-specific security surface issues), **batched verify** (trace whether user-supplied input reaches those assembly sites, in parallel batches of up to 3 sites each), and **merge** (consolidate batch results and surface findings into the final report).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

***

## What is GraphQL Injection
[ref: #graphql-definition]

GraphQL injection occurs when user-controlled data is embedded into the **GraphQL document** (the query, mutation, or subscription string) rather than passed only through the **variables** map. The parser then interprets attacker-controlled syntax — new fields, aliases, directives, fragments, or entire operations — which can bypass intent, reach unauthorized resolvers, or change server-side behavior when that document is executed or forwarded.

The core pattern: *unvalidated user input alters the structure or text of the GraphQL operation string passed to `execute`, `graphql`, a gateway client, or an HTTP body `query` field built from string operations.*

### What GraphQL Injection IS
[ref: #graphql-scope-in]

- Concatenating or interpolating user input into an operation string: `` `query { user(id: "${id}") { name } }` ``, `"query { user(id: \"" + id + "\") { name } }"`
- Building the JSON `query` field for a downstream GraphQL HTTP request with string concat from request body or params
- Forwarding `req.body.query` (or similar) into another interpolated template that wraps or extends the operation
- Dynamic `gql` / `graphql-tag` template literals where a non-static expression changes document structure (not just a bound variable value inside a static document)
- Server-side code that selects or assembles operation text from user input (including "persisted query" ID → document maps without allowlisting)
- Wrappers around `graphql.execute()`, `graphqlHTTP`, Yoga/Apollo request pipeline where the first argument (document/source) is built from variables that could be user-influenced
- Injecting attacker-controlled fragments, aliases, directives, or operation names that change which resolvers run or how results are shaped

### What GraphQL Injection is Not
[ref: #graphql-scope-out]

Do not flag these as GraphQL injection:

- **SQL injection in resolvers**: Resolver code that builds SQL from `args` — that is **SQL injection** (`sast-sqli`), not this skill
- **NoSQL / command injection in resolvers**: Same — use the appropriate SAST skill
- **IDOR via GraphQL arguments**: Passing another user's ID in a **variables** JSON with a **static** document — authorization flaw, not document injection
- **Normal variable binding**: Static document with `{"query": "query($id: ID!) { user(id: $id) { name } }", "variables": {"id": userInput}}` — values are bound as variables; the document structure is fixed (still verify authorization in resolvers)
- **Introspection / field suggestion enabled**: Information disclosure and hardening topic; only flag as GraphQL injection if the finding is specifically about **injecting into the operation string**
- **Query depth / complexity DoS**: Rate limiting and cost analysis — different class, but record it as a GraphQL-specific surface finding

### GraphQL-Specific Security Issues to Consider
[ref: #graphql-surface-issues]

GraphQL is not a standalone OWASP API Top 10 2023 category, but it amplifies several risks because clients can shape queries and mutations. During recon, record these issues as **surface findings** even when they are not document-injection flaws. Use the same classification labels (`Vulnerable`, `Likely Vulnerable`, `Not Vulnerable`, `Needs Manual Review`).

| Issue | Detection focus | Typical OWASP mapping |
|-------|-----------------|-----------------------|
| **Introspection enabled in production** | `__schema`, `__type`, `__typename` queries are accepted from unauthenticated callers; `introspection: true` or missing `ApolloServerPluginLandingPageDisabled` | API8:2023 Security Misconfiguration |
| **Field suggestions enabled** | The server suggests field names (`did you mean`) to unauthenticated callers, helping attackers map the schema | API8:2023 Security Misconfiguration |
| **GraphiQL / Playground / Apollo Sandbox in production** | Debug/landing UI reachable at the GraphQL endpoint or a known path | API8:2023 Security Misconfiguration |
| **Query depth / complexity abuse** | No `MaxQueryDepth` / complexity validation rule; clients request deeply nested or wide trees | API4:2023 Unrestricted Resource Consumption |
| **Batching / alias overloading** | Endpoint accepts JSON arrays of operations or many aliases in one operation, bypassing request-count rate limits | API4:2023 Unrestricted Resource Consumption |
| **Unauthorized mutations / resolver-level auth gaps** | Mutation resolvers or sensitive query resolvers do not enforce object/function-level authorization | API1:2023 BOLA / API5:2023 BFLA |
| **Subscription auth gaps** | WebSocket/subscription handshake does not authenticate or authorize the connection before accepting operations | API2:2023 Broken Authentication / API5:2023 BFLA |
| **Directive injection** | Custom directive arguments reach unsafe evaluation (file system, shell, eval, downstream URLs) or directives are used to bypass field-level guards | Varies (often API1/API5/API7/API8) |
| **CSRF via GraphQL** | State-changing mutations accepted over `GET`, or with simple content-types, without CSRF tokens / `SameSite` protections | API2:2023 Broken Authentication / API8:2023 Security Misconfiguration |
| **File upload via multipart spec** | GraphQL multipart requests are accepted without file-size, type, or count limits; uploads stored under web root or executed | API8:2023 Security Misconfiguration / API10:2023 Unsafe Consumption of APIs |
| **Federation / gateway auth and stitching** | Gateway forwards client operations to subgraphs without propagating identity, or subgraphs trust gateway headers blindly | API10:2023 Unsafe Consumption of APIs |
| **Cache poisoning** | Cache keys depend on user-controlled query shape/variables and upstream responses are cached without validation | API8:2023 Security Misconfiguration / API10:2023 Unsafe Consumption of APIs |
| **MCP / AI agent exposure** | GraphQL operations are exposed to AI agents as MCP tools (e.g. Apollo MCP Server) through an unauthenticated MCP endpoint, introspection-driven dynamic tool generation, or an over-broad persisted-query manifest | API2:2023 Broken Authentication / API8:2023 Security Misconfiguration |

### Patterns That Prevent GraphQL Injection
[ref: #graphql-prevention-patterns]

**1. Static operation documents with variables**

```javascript
const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) { name }
  }
`;
// execute(schema, GET_USER, null, context, { id: userId });
```

**2. Server uses standard HTTP handler; client sends document; server parses once**

The risk is not the mere presence of `req.body.query` on the server if the server only parses and executes it as the client's operation — injection in *that* path is client-side. Flag **server-side** construction of a **new** document that incorporates user strings before `execute` or before forwarding.

**3. Persisted queries / allowlisted operation IDs**

Document looked up by ID from a server-side registry; client cannot inject arbitrary document text.

**4. graphql-js `Source` with static string; dynamic values only in variableValues**

```javascript
graphql({ schema, source: staticQueryString, variableValues: { id: userId } });
```

**5. Disable introspection and field suggestions in production**

Configure the framework to reject `__schema`/`__type` queries and disable field suggestions for unauthenticated callers.

**6. Enforce depth, complexity, and cost limits**

Add validation rules / instrumentation so a single operation cannot exhaust resources.

**7. Per-field and per-resolver authorization**

Every resolver that returns or mutates an object or a property must enforce object-level and function-level authorization checks.

***

## Vulnerable vs. Secure Examples
[ref: #graphql-examples]

### Node.js — dynamic document for downstream API

```javascript
// VULNERABLE: user input in operation text
app.post('/proxy', async (req, res) => {
  const fragment = req.body.fragment;
  const query = `query { me { ${fragment} } }`;
  const data = await fetch('https://api.internal/graphql', {
    method: 'POST',
    body: JSON.stringify({ query }),
  });
});

// SECURE: static operation, user data only in variables
const PROXY_QUERY = `query ProxyMe { me { id name email } }`;
app.post('/proxy', async (req, res) => {
  const data = await fetch('https://api.internal/graphql', {
    method: 'POST',
    body: JSON.stringify({ query: PROXY_QUERY }),
  });
});
```

### Python — string format into execute

```python
# VULNERABLE
def run_custom_query(user_gql: str):
    document = f"query {{ user {{ {user_gql} }} }}"
    return graphql_sync(schema, document)

# SECURE: validate against allowlist of named operations or use static documents only
ALLOWED = {"id", "name", "email"}
fields = [f for f in requested_fields if f in ALLOWED]
document = "query { user { " + " ".join(ALLOWED.intersection(set(requested_fields))) + " } }"
# Better: fixed FieldNodes, not string building from user input
```

### Apollo Server

```javascript
// VULNERABLE: building a document from request input before sending to Apollo Client / Server
app.post('/profile', async (req, res) => {
  const fields = req.body.fields; // attacker-controlled fragment
  const query = `query { me { ${fields} } }`;
  const { data } = await apolloClient.query({ query: gql`${query}` });
  res.json(data);
});

// SECURE: static operation, variables bound safely, introspection disabled in production
import { ApolloServer } from '@apollo/server';
import { ApolloServerPluginLandingPageDisabled } from '@apollo/server/disabled';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: false,
  plugins: [ApolloServerPluginLandingPageDisabled()],
});

const GET_ME = gql`query GetMe { me { id name email } }`;
app.post('/profile', async (req, res) => {
  const { data } = await apolloClient.query({ query: GET_ME });
  res.json(data);
});
```

> **Version note (verified 2026-07):** Apollo Server 5 is current — Apollo Server 4 is EOL since 2026-01-26, and v3 (`apollo-server-express`) since 2024-10-22. In v5 the Express integration moved out of `@apollo/server`: `expressMiddleware` is imported from `@as-integrations/express4` (or `@as-integrations/express5`), and `status400ForVariableCoercionErrors` now defaults to `true`. The `introspection: false` + `ApolloServerPluginLandingPageDisabled` hardening shown above is unchanged in v5.

### graphql-js

```javascript
// VULNERABLE
const userId = req.params.id;
const result = await graphql({
  schema,
  source: `query { user(id: "${userId}") { name } }`,
});

// SECURE
const result = await graphql({
  schema,
  source: 'query GetUser($id: ID!) { user(id: $id) { name } }',
  variableValues: { id: req.params.id },
});
```

### Strawberry (Python)

```python
# VULNERABLE
result = await schema.execute(
    f'query {{ user(id: "{user_id}") {{ name }} }}'
)

# SECURE
result = await schema.execute(
    'query GetUser($id: ID!) { user(id: $id) { name } }',
    variable_values={"id": user_id},
)
```

### Graphene (Python)

```python
# VULNERABLE
result = schema.execute(
    f'query {{ user(id: "{user_id}") {{ name }} }}'
)

# SECURE
result = schema.execute(
    'query GetUser($id: ID!) { user(id: $id) { name } }',
    variables={"id": user_id},
)
```

### FastAPI (Python)

```python
# VULNERABLE: document text built from the JSON request body
from fastapi import FastAPI, Request
from graphql import graphql_sync

app = FastAPI()

@app.post("/report")
async def report(request: Request):
    body = await request.json()
    document = f'query {{ user(id: "{body["user_id"]}") {{ name }} }}'
    result = graphql_sync(schema, document)
    return result.formatted

# SECURE: static document with bound variables; Strawberry router serves /graphql
import strawberry
from strawberry.fastapi import GraphQLRouter

schema = strawberry.Schema(query=Query)
app.include_router(GraphQLRouter(schema), prefix="/graphql")
```

### graphql-java

```java
// VULNERABLE
ExecutionInput input = ExecutionInput.newExecutionInput()
    .query("query { user(id: \"" + userId + "\") { name } }")
    .build();

// SECURE
ExecutionInput input = ExecutionInput.newExecutionInput()
    .query("query GetUser($id: ID!) { user(id: $id) { name } }")
    .variables(Collections.singletonMap("id", userId))
    .build();
```

### Sangria (Scala)

```scala
// VULNERABLE
val query = s"query { user(id: \"$userId\") { name } }"
val result = Executor.execute(schema, QueryParser.parse(query).get)

// SECURE
val query = graphql"query GetUser($$id: ID!) { user(id: $$id) { name } }"
val result = Executor.execute(
  schema,
  query,
  variables = JsObject("id" -> JsString(userId))
)
```

***

## Prevention Guidance
[ref: #graphql-prevention-guidance]

- **Static documents + variables**: Never build operation text from user input. Pass user data only in the `variables` / `variableValues` map.
- **Allowlist dynamic fragments**: If the client must select fields, validate against a server-side allowlist before assembling any text.
- **Disable introspection and field suggestions in production**: Set `introspection: false`, remove `ApolloServerPluginLandingPageGraphQLPlayground`, and disable field suggestions.
- **Enforce query depth and complexity limits**: Use `graphql-depth-limit`, `graphql-query-complexity`, Apollo Server validation rules, Java `MaxQueryDepthInstrumentation`, or Sangria complexity reducers.
- **Rate limit by complexity, not just request count**: Account for aliases, batching, and expensive resolvers. Reject batched arrays that exceed a size limit.
- **Per-field and per-resolver authorization**: Check object-level and function-level authorization in every resolver that touches sensitive data or mutations.
- **Authenticate subscriptions and machine-to-machine GraphQL APIs**: Enforce auth on the WebSocket handshake and on every operation.
- **Persisted queries / allowlist**: Use a server-side registry of allowed operation IDs for high-risk or public endpoints.
- **Validate upstream GraphQL responses**: When forwarding to or consuming another GraphQL service, treat the response as untrusted input.
- **Disable GraphiQL / Playground / Apollo Sandbox in production**: Use disabled landing-page plugins and remove debug routes.
- **CSRF protections**: Reject state-changing mutations over `GET`; require non-simple content types or CSRF tokens; use `SameSite` cookies.
- **File upload limits**: For GraphQL multipart uploads, enforce max file size, count, and allowed MIME types; store uploads outside the web root and never execute them.
- **Federation / gateway hardening**: Propagate authentication context to subgraphs, validate subgraph responses, and do not trust internal headers blindly.
- **MCP / AI agent endpoints**: Authenticate the MCP endpoint (OAuth 2.1 with PKCE, RFC 9728), generate tools from operation files or persisted-query manifests rather than live introspection, and scope manifests to the minimum operations the agent needs.

***

## CWE References
[ref: #graphql-cwe-mapping]

- **CWE-20**: Improper Input Validation
- **CWE-74**: Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')
- **CWE-89**: SQL Injection (resolver SQL/NoSQL injection from GraphQL arguments)
- **CWE-200**: Information Exposure (introspection, field suggestions, excessive property exposure)
- **CWE-285**: Improper Authorization
- **CWE-352**: Cross-Site Request Forgery (CSRF)
- **CWE-400**: Uncontrolled Resource Consumption
- **CWE-639**: Authorization Bypass Through User-Controlled Key
- **CWE-770**: Allocation of Resources Without Limits or Throttling
- **CWE-915**: Improperly Controlled Modification of Dynamically-Determined Object Attributes
- **CWE-918**: Server-Side Request Forgery (SSRF)

***

## Execution
[ref: #graphql-execution]

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: GraphQL Technology Recon and Injection Candidate Sites

Launch a subagent with the following instructions:

> **Goal**: (1) Determine whether this codebase uses GraphQL at all. (2) If it does, find every location where a GraphQL **operation document** (query/mutation/subscription source string) is built using string concatenation, interpolation, formatting, or dynamic assembly such that a variable could change the **document text** (not merely `variables` JSON). (3) Record GraphQL-specific security surface issues. Write results to `{{ REPORTS_ROOT }}/14_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it for stack, API layout, and BFF/gateway patterns.
>
> **Constraint**: You are **read-only**. Do not modify project source code, configuration files, tests, or dependencies. Do not run `git commit`, `git push`, package installs, or any destructive commands.
>
> **Part A — Is GraphQL used?**
>
> Search for:
> - Dependencies: `graphql` (graphql-js; v17 released 2026-06, v16 still widespread), `@apollo/server` (v5 current; v4 EOL 2026-01-26), `@as-integrations/express4` / `@as-integrations/express5`, `apollo-server-express` (legacy, EOL 2024-10-22), `@nestjs/graphql`, `graphql-yoga`, `@graphql-yoga/node`, `mercurius`, `strawberry-graphql`, `graphene`, `ariadne`, `sangria`, `gqlgen`, `async-graphql`, `juniper`, `graphql-ruby`, Hot Chocolate / `GraphQL.Server`, Spring for GraphQL (`spring-boot-starter-graphql`), Apollo MCP Server, etc.
> - Schema artifacts: `*.graphql`, `*.graphqls`, codegen config (e.g. GraphQL Code Generator)
> - Server routes or plugins mounting `/graphql` or similar
>
> Set the summary to exactly one of:
> - `GraphQL is used in this codebase.` (list libraries and main entry points)
> - `GraphQL is not used in this codebase.`
>
> **Part B — Injection candidate sites (only if GraphQL is used)**
>
> If GraphQL is **not** used, omit the "Injection Candidate Sites" section or state there are none. Do not invent candidates.
>
> If GraphQL **is** used, search for **unsafe document construction**:
>
> 1. **String concatenation / interpolation into operation text**:
>    - `` `query { ... ${x} ...}` ``, `"mutation { " + userFragment + " }"`
>    - `sprintf`, `format`, `%` formatting, `.format()` building `query` or `source` arguments
>
> 2. **Calls where the document argument is not a compile-time constant**:
>    - `graphql(schema, dynamicString, ...)`, `execute({ schema, document: parsedDynamic, ...})` where the string feeding `parse` or `execute` is built from non-static parts
>    - `graphqlHTTP({ schema, rootValue, context: (req) => ({ query: req.body.query + something }) })` patterns that **mutate** or **wrap** the query string with user data
>
> 3. **HTTP clients forwarding a constructed GraphQL body**:
>    - `JSON.stringify({ query: \`...${userPart}...\` })`, `axios.post(url, { query: builtFromInput })`
>
> 4. **Unsafe persisted / stored query lookup**:
>    - Operation text loaded by key from user input without allowlist → file path or DB value becomes document source
>
> **What to skip** (do not flag as Phase 1 candidates):
> - Fully static `source` / `query` strings; only `variableValues` / `variables` come from the request
> - Schema definition with `buildSchema` / SDL files with no user interpolation
> - Resolver implementations that only use args with parameterized DB APIs (optional: note "resolver uses ORM" but not a GraphQL injection candidate unless the **document** is built unsafely)
>
> **Part C — GraphQL-specific security surface findings (only if GraphQL is used)**
>
> Record findings under "GraphQL Surface Findings" using the classification labels. For each issue, state whether it is present, absent, or uncertain. If present, include file/config location and impact.
>
> - Introspection enabled in production
> - Field suggestions enabled
> - GraphiQL / Playground / Apollo Sandbox exposed
> - Missing query depth / complexity / cost limits
> - Batching / alias overloading accepted without limits
> - Resolver-level authorization gaps on sensitive queries, mutations, or subscriptions
> - Subscription / WebSocket authentication gaps
> - Custom directive injection candidates
> - CSRF-vulnerable mutation handling
> - File upload via multipart without limits
> - Federation / gateway trust issues
> - Cache poisoning risk from query-shape cache keys
> - MCP / AI agent exposure (unauthenticated MCP endpoint, introspection-driven tool generation, over-broad persisted-query manifest)
>
> **Output format** — write to `{{ REPORTS_ROOT }}/14_recon.md`:
>
> ```markdown
> # GraphQL Recon: [Project Name]
>
> ## Summary
> GraphQL is [used / not used] in this codebase.
> [If used: libraries, main server files, typical endpoint paths]
> Found [N] injection candidate site(s) where operation documents may be built unsafely. [If not used, say N/A or 0 and skip candidate list]
> Found [M] GraphQL-specific surface finding(s).
>
> ## GraphQL Surface (only if used)
> - **Libraries / frameworks**: ...
> - **Entry points**: ...
> - **Notable files**: ...
>
> ## Injection Candidate Sites
>
> ### 1. [Descriptive name]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: ...
> - **Execution / call pattern**: [graphql.execute / fetch with body / gql template / etc.]
> - **Construction pattern**: [concat / template literal / format / forwarded body mutation]
> - **Interpolated variable(s)**: ...
> - **Code snippet**:
>   ```
>   ...
>   ```
>
> [Repeat for each site; if none, write "No injection candidate sites found." under the heading]
>
> ## GraphQL Surface Findings
>
> ### [LIKELY VULNERABLE] Introspection enabled in production
> - **File / config**: ...
> - **Issue**: ...
> - **Evidence**: ...
> - **Remediation**: disable introspection in production
>
> [Repeat for each surface finding; if none, write "No surface findings."]
> ```

### After Phase 1: Gates Before Phase 2

After Phase 1 completes, read `{{ REPORTS_ROOT }}/14_recon.md`.

**Gate 1 — No GraphQL technology**

If the summary states GraphQL is **not used** (or equivalent: no GraphQL libraries, no schema, no server — clear absence), **skip Phases 2 and 3**. Write the following to `{{ REPORTS_ROOT }}/14_graphql.md` and stop:

```markdown
# GraphQL Injection Analysis Results

No GraphQL technology detected in this codebase.
```

**Gate 2 — GraphQL used but no injection candidates**

If GraphQL **is** used but there are **zero** injection candidate sites (summary reports 0 candidates, or the "Injection Candidate Sites" section states none found / is empty), **skip Phases 2 and 3**. Still include any surface findings from Phase 1 in `{{ REPORTS_ROOT }}/14_graphql.md`. If there are no surface findings either, write:

```markdown
# GraphQL Injection Analysis Results

No vulnerabilities found.
```

**Otherwise** proceed to Phase 2.

### Phase 2: Trace User Input to Injection Candidate Sites (Batched)

After Phase 1 completes and both gates pass (GraphQL used and at least one candidate site), read `{{ REPORTS_ROOT }}/14_recon.md` and split the **Injection Candidate Sites** into **batches of up to 3 sites each** (each `### N.` section is one site). Launch **one subagent per batch in parallel**. Each subagent traces taint only for its assigned sites and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/14_recon.md` and count the numbered candidate sections under "Injection Candidate Sites" (`### 1.`, `### 2.`, etc.).
2. Divide them into batches of up to 3. For example, 8 sites → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those candidate sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned candidate sections (plus architecture context).
5. Each subagent writes to `{{ REPORTS_ROOT }}/14_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project uses Node.js, include the "Node.js — dynamic document for downstream API" and "Apollo Server" examples; if Python, include "Python — string format into execute", "Strawberry", and "Graphene". Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned injection candidate site, determine whether user-supplied data can reach the dynamic part of the operation document. Our goal is to find GraphQL injection vulnerabilities. Write results to `{{ REPORTS_ROOT }}/14_batch_[N].md`.
>
> **Constraint**: You are **read-only**. Do not modify source code, configuration, tests, or dependencies. Do not run destructive commands.
>
> **Your assigned candidate sites** (from the recon phase):
>
> [Paste the full text of the assigned candidate sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it for API layout, request handling, and BFF/gateway patterns.
>
> **GraphQL injection reference — What to look for**:
>
> User-controlled data must not alter the **GraphQL document text** (query/mutation/subscription source) except through bound **variables** on a static document. Flag when taint reaches string assembly of the operation.
>
> **What GraphQL injection is NOT** — do not flag these here:
> - **SQL/NoSQL injection in resolvers** — other SAST skills
> - **IDOR with static document + variables** — authorization, not document injection
> - **Normal variable binding** on a fixed document string
> - **Introspection enabled** — unless the finding is specifically operation-string injection
> - **Query depth/complexity DoS** — different class
>
> **Mitigations that reduce risk**:
> - Allowlist of fields or operation IDs before any string assembly
> - Parser validation that rejects unexpected definitions (still prefer no user-controlled document structure)
>
> **Vulnerable vs. secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **For each assigned site, trace dynamic values backward**:
>
> 1. **Direct user input** — query params, path params, JSON body fields (including nested `query` if re-wrapped), headers, cookies
> 2. **Indirect user input** — helpers, middleware, context builders
> 3. **Second-order** — stored preferences or DB fields later used to build a document; trace write path
> 4. **Server-only** — config, env, hardcoded fragments — not exploitable from the client
>
> **Classification**:
> - **Vulnerable**: User-controlled data reaches document construction with no effective mitigation
> - **Likely Vulnerable**: Probable taint or weak sanitization
> - **Not Vulnerable**: Server-side-only or effective allowlist / static document path
> - **Needs Manual Review**: Opaque flow
>
> **Output format** — write to `{{ REPORTS_ROOT }}/14_batch_[N].md`:
>
> ```markdown
> # GraphQL Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: ...
> - **Issue**: ...
> - **Taint trace**: ...
> - **Impact**: [e.g., unauthorized fields, gateway bypass, SSRF-style behavior to internal GraphQL]
> - **Remediation**: [static operations; variables only; persisted query allowlist]
> - **Dynamic Test**:
>   ```
>   [curl or in-browser GraphQL request showing injected fragment/directive/field]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: ...
> - **Endpoint / function**: ...
> - **Issue**: ...
> - **Taint trace**: ...
> - **Concern**: ...
> - **Remediation**: ...
> - **Dynamic Test**:
>   ```
>   ...
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: ...
> - **Endpoint / function**: ...
> - **Reason**: ...
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: ...
> - **Endpoint / function**: ...
> - **Uncertainty**: ...
> - **Suggestion**: ...
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/14_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/14_graphql.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/14_batch_1.md`, `{{ REPORTS_ROOT }}/14_batch_2.md`, ... files.
2. Read the Phase 1 surface findings from `{{ REPORTS_ROOT }}/14_recon.md`.
3. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
4. Count totals across all batches for the executive summary.
5. Write the merged report to `{{ REPORTS_ROOT }}/14_graphql.md` using this format:

```markdown
# GraphQL Injection Analysis Results: [Project Name]

## Executive Summary
- Candidate sites analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]
- Surface findings from Phase 1: [M]

## Findings

[All injection findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]

## GraphQL Surface Findings

[All Phase 1 surface findings, grouped and classified.]
```

6. After writing `{{ REPORTS_ROOT }}/14_graphql.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/14_batch_*.md`).

***

## Advanced Patterns
[ref: #graphql-advanced-patterns]

Look for these less-obvious GraphQL security issues during recon and manual review:

- **Query cost analysis abuse**: Attackers craft operations with low depth but expensive resolvers (e.g., heavy aggregations) to evade depth limits while still causing DoS.
- **Live query / subscription abuse**: Subscriptions or live queries stream updates; missing auth or unbounded filters can leak data or exhaust connections.
- **Federation / gateway auth and stitching**: Gateway trusts subgraph headers, or auth context is dropped between gateway and subgraphs; subgraphs may be reachable directly.
- **CSRF via GraphQL**: Mutations served over `GET`, or POST with `Content-Type: text/plain`, allow cross-site forged requests from simple `<form>` or `<img>` tags.
- **File upload via multipart spec**: GraphQL multipart requests bypass traditional upload controls; validate file size, count, MIME type, and storage path.
- **Cache poisoning**: Shared caches key responses by `query` + `variables`; attacker injects a field or alias that pollutes the cache for other users.
- **Directive injection**: Custom directives evaluate arguments in unsafe contexts (e.g., `@exec(cmd: ...)`) or directives override authorization decisions.
- **Alias overloading / batching**: JSON arrays of operations or many aliased fields in one request bypass per-request rate limits and amplify brute force or resource exhaustion.
- **MCP / AI agent access**: Apollo MCP Server and similar bridges turn GraphQL operations into MCP tools for AI agents; an unauthenticated MCP endpoint, introspection-driven dynamic tool generation, or an over-broad persisted-query manifest lets an agent (or a prompt-injected user) reach resolvers the HTTP API never meant to expose. Require OAuth 2.1 with PKCE on the MCP endpoint (RFC 9728 Protected Resource Metadata) and generate tools from operation files or manifests, not live introspection.
- **Engine-level CVEs**: track parser/library bugs in addition to application flaws — graphql-ruby schema-from-JSON deserialization RCE (CVE-2025-27407; patched in 1.11.8, 1.12.25, 1.13.24, 2.0.32, 2.1.14, 2.2.17, 2.3.21) and Spring for GraphQL unsafe deserialization in paginated queries (CVE-2026-41699, RCE).

***

## OWASP API Security Top 10 2023 Mapping
[ref: #graphql-owasp-mapping]

This scan supports the following OWASP API Security Top 10 2023 risks:

| OWASP API 2023 risk | GraphQL manifestation | OWASP source file |
|---|---|---|
| **API1:2023 Broken Object Level Authorization** | Mutations or queries acting on object IDs without verifying ownership; e.g., deleting a document by ID without authorization | `0xa1-broken-object-level-authorization.md` |
| **API2:2023 Broken Authentication** | GraphQL query batching bypasses login rate limiting; missing authentication on subscription/WebSocket connections | `0xa2-broken-authentication.md` |
| **API4:2023 Unrestricted Resource Consumption** | Missing query depth/complexity/cost limits; batching/alias overloading; resource-intensive file upload abuse | `0xa4-unrestricted-resource-consumption.md` |
| **API5:2023 Broken Function Level Authorization** | Unauthorized mutations; resolver-level function or role checks missing; subscription paths not enforcing function-level access | `0xa5-broken-function-level-authorization.md` |
| **API8:2023 Security Misconfiguration** | Introspection, field suggestions, GraphiQL/Playground/Apollo Sandbox, debug interfaces, missing depth limits | `0xa8-security-misconfiguration.md` |
| **API10:2023 Unsafe Consumption of APIs** | Forwarding user-controlled fragments or operation strings to downstream GraphQL APIs; federation/gateway trust; cache poisoning from upstream responses | `0xaa-unsafe-consumption-of-apis.md` |

**Additional cross-reference**: `0xa3-broken-object-property-level-authorization.md` contains a GraphQL example of excessive data exposure / mass assignment and should be considered when reviewing resolver-level property authorization.

***

## Subagent Constraints and Important Reminders
[ref: #graphql-important-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- **Subagents are read-only**. They must not modify project source code, configuration files, tests, or dependencies. They must not run `git commit`, `git push`, package installs, or any destructive commands.
- **If Phase 1 finds no GraphQL technology, skip Phases 2 and 3** — write the "No GraphQL technology detected" results file.
- **If GraphQL is used but Phase 1 finds no injection candidates, skip Phases 2 and 3** — include any surface findings in `{{ REPORTS_ROOT }}/14_graphql.md`; if none, write "No vulnerabilities found."
- Phase 2 must run **after** Phase 1 completes — it depends on the recon output.
- Phase 3 must run **after** all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 candidate sites per subagent**. If there are 1-3 sites total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned candidates' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- Phase 1 does **not** trace taint; Phase 2 does.
- Resolver-layer SQL/NoSQL issues belong to other skills; this skill targets **operation document** construction.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable".
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/14_recon.md` and all `{{ REPORTS_ROOT }}/14_batch_*.md` files after the final `{{ REPORTS_ROOT }}/14_graphql.md` is written.

***

## References
[ref: #graphql-references]

- OWASP GraphQL Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html
- OWASP Authorization Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Authorization Testing Automation Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Testing_Automation_Cheat_Sheet.html
- OWASP Authentication Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- OWASP Mass Assignment Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html
- OWASP Server-Side Request Forgery Prevention Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Server-Side_Request_Forgery_Prevention_Cheat_Sheet.html
- Apollo MCP Server documentation — https://www.apollographql.com/docs/apollo-mcp-server
- Migrating from Apollo Server 4 to 5 — https://www.apollographql.com/docs/apollo-server/migration
- OWASP API Security Top 10 2023 source files used in this reference:
  - `0xa1-broken-object-level-authorization.md`
  - `0xa2-broken-authentication.md`
  - `0xa3-broken-object-property-level-authorization.md`
  - `0xa4-unrestricted-resource-consumption.md`
  - `0xa5-broken-function-level-authorization.md`
  - `0xa7-server-side-request-forgery.md`
  - `0xa8-security-misconfiguration.md`
  - `0xaa-unsafe-consumption-of-apis.md`
  - `0xb0-next-devs.md`
