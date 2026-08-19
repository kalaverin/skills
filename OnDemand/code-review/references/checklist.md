[ref: #checklist]

# Language-Agnostic Review Checklist

Use this checklist during Phase 1 of the review. Apply only the sections that are
relevant to the language and project type under review.

## 1. Correctness & Bugs

- [ ] Off-by-one errors, boundary conditions, and loop invariants.
- [ ] Null / nil / None / uninitialized values dereferenced.
- [ ] Integer overflow, division by zero, or numeric precision issues.
- [ ] Incorrect Boolean logic, inverted conditions, or unreachable branches.
- [ ] Race conditions and non-atomic read-modify-write sequences.
- [ ] Time-zone, date-format, and clock-skew bugs.
- [ ] Locale-sensitive operations that assume a single locale.
- [ ] Resource leaks: files, sockets, database connections, memory.

## 2. Security

- [ ] Hardcoded credentials, API keys, tokens, or secrets.
- [ ] SQL injection or command injection through string concatenation.
- [ ] Path traversal via file uploads or file-system operations.
- [ ] XSS, unsafe HTML rendering, or unescaped output.
- [ ] Insecure deserialization or unsafe parsing of untrusted data.
- [ ] Weak hashing, encryption, or randomness.
- [ ] Missing authentication or authorization on endpoints/functions.
- [ ] Broken object-level or property-level authorization (BOLA/BOPLA).
- [ ] Missing CSRF tokens or unsafe CORS configuration.
- [ ] JWT or session tokens without expiry / refresh strategy.
- [ ] Unvalidated file uploads (size, type, malicious content).
- [ ] Admin endpoints exposed without protection.

## 3. Resilience & Fault Tolerance

- [ ] Bare catch-all handlers that swallow errors silently.
- [ ] Generic catch blocks that do not log and re-raise/return an error.
- [ ] Expected exceptions (specific types) handled without recovery logic.
- [ ] Unexpected exceptions not logged at ERROR level with full context.
- [ ] Missing fallback for external service or dependency failures.
- [ ] Missing retry with exponential backoff for transient failures.
- [ ] Non-idempotent operations without idempotency keys or duplicate guards.
- [ ] Partial database writes without rollback or compensation.
- [ ] Unclosed connections in `finally` / destructor / defer equivalents.
- [ ] Circuit breaker or bulkhead pattern missing where appropriate.

## 4. Observability & Logging

- [ ] Missing ERROR-level log when an exception/error occurs.
- [ ] Logs lacking context (request ID, trace ID, operation name, user).
- [ ] ERROR log spam on every retry attempt.
- [ ] DEBUG logs in hot paths.
- [ ] Raw stack traces leaked to users or external APIs.
- [ ] Missing structured logging or consistent log field naming.
- [ ] Missing metrics or alerts for error conditions.
- [ ] Logs written before a transaction commits, causing false signals.

## 5. PII & Data Privacy

- [ ] Email, name, phone, SSN, tokens, passwords, geolocation, or biometric data
  in logs.
- [ ] PII in exception messages or string representations.
- [ ] PII in metrics labels, cache keys, message-queue headers, or API responses.
- [ ] Missing masking or redaction for sensitive fields.
- [ ] Sensitive data cached without encryption or TTL.
- [ ] User data returned to clients beyond the minimum required.

## 6. Performance & Scalability

- [ ] N+1 query / remote-call patterns.
- [ ] Unbounded loops, recursion, or memory growth.
- [ ] Synchronous blocking inside async/concurrent contexts.
- [ ] Missing pagination on list endpoints.
- [ ] Inefficient algorithms or data structures.
- [ ] Repeated expensive computations without memoization.
- [ ] Database transactions held longer than necessary.

## 7. Maintainability & Design

- [ ] Violations of SOLID, DRY, KISS.
- [ ] Magic numbers or undocumented constants.
- [ ] Functions/modules with excessive responsibility.
- [ ] Tight coupling or low cohesion.
- [ ] Missing or misleading comments and documentation.
- [ ] Dead code, unused imports, or unused variables.
- [ ] Public API surface larger than necessary.
- [ ] Inconsistent naming or project conventions.

## 8. Concurrency & Transactions

- [ ] Shared mutable state without synchronization.
- [ ] Incorrect lock ordering or risk of deadlock.
- [ ] Lost updates or incorrect isolation levels.
- [ ] Missing rollback in error handlers.
- [ ] Race conditions in concurrent writes.
- [ ] Idempotency keys missing for retryable operations.

## 9. Build, Deploy & Configuration

- [ ] Secrets committed to version control.
- [ ] Environment-specific values hardcoded.
- [ ] Missing or incorrect `.gitignore` entries.
- [ ] Build artifacts or dependencies checked in unintentionally.
- [ ] Configuration that disables safety features in production.

## 10. Architecture, Layers & Domain Isolation

This section is critical for codebases that follow or claim to follow layered,
hexagonal, onion, or domain-driven architecture. Apply it strictly.

### Layer boundaries and dependency direction

- [ ] Inner layers (domain) depend on outer layers (framework, UI, DB, external
  services) instead of the reverse.
- [ ] Domain entities import ORM, framework, HTTP, logging, or other
  infrastructure concerns.
- [ ] Application services contain domain logic that belongs in entities or
  domain services.
- [ ] Controllers / handlers / CLI entry points contain business rules instead
  of thin orchestration.
- [ ] Infrastructure code leaks into public API contracts (DTOs, responses,
  schemas).

### Domain model quality

- [ ] Anemic domain model: entities are only data bags with getters/setters and
  no behavior.
- [ ] Domain invariants are enforced outside entities (e.g. in application
  services, controllers, or validators far from the domain).
- [ ] Aggregates are too large, span multiple bounded contexts, or are
  inconsistently defined.
- [ ] Cross-aggregate direct references instead of identity-based references.
- [ ] Value objects are represented as primitives (strings, ints) instead of
  dedicated types.
- [ ] Missing or inconsistent ubiquitous language; domain terms differ between
  code, tests, and documentation.

### Hexagonal / ports and adapters

- [ ] Missing ports (interfaces) for external dependencies consumed by the
  application/domain.
- [ ] Adapters bypass ports and call concrete infrastructure directly.
- [ ] Application or domain code instantiates infrastructure classes instead of
  receiving them via dependency injection / constructor.
- [ ] Anti-corruption layers missing where the bounded context integrates with
  external systems or legacy models.
- [ ] Side effects (email, messaging, file system) are triggered directly from
  domain code instead of through outbound ports.

### Abstraction and isolation

- [ ] Abstractions are leaky: callers must know implementation details to use
  them correctly.
- [ ] Generic utilities / shared kernel grow domain-specific logic.
- [ ] Configuration, serialization, or persistence concerns appear in domain
  models.
- [ ] Public APIs expose internal aggregate state that should be encapsulated.
- [ ] Read models / query paths mutate domain state or bypass domain rules.
- [ ] Transaction boundaries are wider or narrower than the consistency boundary
  of the aggregate / use case.

### Transaction and isolation semantics

- [ ] Transaction isolation level is not explicitly chosen or justified for the
  use case.
- [ ] Phantom reads, non-repeatable reads, or lost updates possible due to wrong
  isolation level.
- [ ] Long-running transactions hold locks across user input, external calls, or
  unrelated operations.
- [ ] Distributed operations lack Saga / outbox / eventual-consistency plan.
- [ ] Compensation logic missing for multi-step business processes.
