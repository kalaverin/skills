---
subject: >-
  Delegated review and audit roles for subagents: seven read-only reviewer
  roles (general, domain, security, integration, test auditor, docs auditor,
  data reviewer) with unified prompt templates, plus parent integration
  workflow for accepting or rejecting findings.
index:
  - anchor: roles-reviewer
    what: >-
      General reviewer role: behavior regressions, missing or thin test
      coverage, architecture and layer-boundary violations, compatibility and
      release gaps, documentation drift.
    problem: >-
      Agent delegates general diff review; ordinary-looking changes hide
      regressions and thin tests slip through unchallenged lately; quality
      pass, behavioral regression, weak tests, layering violation, rollout
      gap, docs drift, overall quality.
    use_when: >-
      Any diff needs an overall review; user asked for review without naming
      an aspect.
    avoid_when: >-
      A named aspect fits a specialist role (other cards); full-pipeline code
      review request (code-review skill).
    expected: >-
      Findings severity-ordered with file:line anchors, or explicit
      no-findings plus residual test gaps.
  - anchor: roles-domain
    what: >-
      Domain reviewer role: allowed and invalid state transitions, audit
      trail / history / read-model changes, user-visible effects, ownership
      plus visibility constraints, domain test gaps.
    problem: >-
      Agent delegates review of stateful workflow diff; unchecked
      transitions and missing audit trail poison later phases silently;
      state machine, invalid transition, audit history, read model, side
      effect, ownership rule, visibility rule, workflow behavior.
    use_when: >-
      Diff touches stateful workflows, transitions, or user-visible behavior.
    avoid_when: >-
      General regressions (roles-reviewer); auth/access focus
      (roles-security).
    expected: >-
      Transition, side-effect, and test-gap findings with affected user group
      named.
  - anchor: roles-security
    what: >-
      Security reviewer role: authorization bypasses, access regressions,
      tenant and file/data exposure, sensitive-data leaks, missing negative
      access tests, rollback or disable options for risky behavior.
    problem: >-
      Agent delegates review of auth or data-access diff; security
      regressions hide in ordinary-looking changes and generic reviewers miss
      negative paths; auth bypass, permission regression, tenant exposure,
      secret leakage, negative tests, rollback path, access control.
    use_when: >-
      Diff touches auth, permissions, file/data access, privacy, or
      sensitive-data handling.
    avoid_when: >-
      General regressions (roles-reviewer); test strategy only
      (roles-test-auditor).
    expected: >-
      Security findings severity-ordered with file:line, negative-test gaps
      and rollback options named.
  - anchor: roles-integration
    what: >-
      Integration reviewer role: contract compatibility with external
      systems, retry/timeout/failure mapping, idempotent handling of repeated
      events, commit/acknowledge sequencing, settings, flags, and
      staggered-version rollout, observability of failures.
    problem: >-
      Agent delegates review of integration or consumer diff; distributed
      failure modes pass review while green tests hide retry and ordering
      bugs; external schema, error mapping, idempotency, duplicate events,
      ack ordering, feature flags, mixed versions, failure observability.
    use_when: >-
      Diff touches external clients, events, consumers, workers, or rollout
      behavior.
    avoid_when: >-
      Internal workflow transitions (roles-domain); pure unit-level changes.
    expected: >-
      Compatibility, retry, duplication, and observability findings plus
      recommended validation.
  - anchor: roles-test-auditor
    what: >-
      Test auditor role: coverage gaps for changed behavior, assertion
      strength, missing failure paths, over-mocked integration behavior,
      recommended scoped test commands.
    problem: >-
      Agent delegates test-strategy review of diff; coverage looks adequate
      while changed behavior and failure paths stay unverified; missing
      coverage, weak assertion, negative path, over-mocking, scoped commands,
      verification gaps, test debt, assertion quality.
    use_when: >-
      User asks whether tests suffice; diff changes behavior and tests look
      thin.
    avoid_when: >-
      General diff pass (roles-reviewer); security-specific negative tests
      (roles-security).
    expected: >-
      Required additions, nice-to-have tests, commands to run, and residual
      risk stated.
  - anchor: roles-docs-auditor
    what: >-
      Docs auditor role: spec and context consistency with the diff,
      repository language plus status taxonomy, no duplicated global rules,
      canonical-file links, compact documentation aimed at agents.
    problem: >-
      Agent delegates documentation review alongside code diff; docs drift
      silently behind tree and duplicated policy forks diverge; spec drift,
      context freshness, status vocabulary, duplicated rules, canonical
      links, compact reference, documentation gaps.
    use_when: >-
      Diff changes documented behavior; specs or context files were touched
      or should have been.
    avoid_when: >-
      Code-only review (roles-reviewer); test gaps (roles-test-auditor).
    expected: >-
      Documentation findings, duplication and drift risks, remaining gaps.
  - anchor: roles-data-reviewer
    what: >-
      Data reviewer role: nullability, defaults, and production data shape;
      backfill cost and lock risk; forward and rollback path; mixed-version
      compatibility; validation evidence on disposable data.
    problem: >-
      Agent delegates review of migration or backfill diff; data-shape
      assumptions break on real production datasets and lock risk surfaces
      only under load; migration safety, column defaults, production rows,
      job duration, table locks, revert plan, version skew, throwaway
      database.
    use_when: >-
      Diff includes migrations, backfills, or data-shape changes.
    avoid_when: >-
      Code-only changes; consumer/event ordering (roles-integration).
    expected: >-
      Rollback, nullability, lock, and mixed-version findings plus
      recommended validation on disposable data.
  - anchor: roles-parent-workflow
    what: >-
      Parent integration workflow: subagent output is evidence not truth;
      every finding accepted or rejected with reason; fixed role pairings;
      three-role cap per diff; stale findings rerun; final report names roles
      used.
    problem: >-
      Agent collects role findings after delegated reviews; unverified
      adoption imports subagent mistakes wholesale and silent dismissal
      loses auditability; evidence versus truth, accept reject, reason
      record, fixed pairings, branch cap, staleness rerun, rerun trigger,
      report naming.
    use_when: >-
      Role reviews complete and findings need triage; combining multiple
      aspects on one diff.
    avoid_when: >-
      Single direct review without delegation; implementation work (not this
      file).
    expected: >-
      Each finding resolved as fixed, deferred, or declined with stated
      reason; report lists applied roles.
---

# Role Library: delegated review and audit roles

Seven read-only review roles plus the parent integration workflow. Each role
runs as `subagent_type: explore` (physically read-only) with the model chosen
per [ref: #sp-model-selection] in `../SKILL.md`. Web data, if needed, is
fetched by the main agent and passed into the prompt (§6).

Adapted from `agent-coding-policy/docs/agent-playbooks/subagents.md`
(internal GitLab, branch v1), adjusted to this protocol: explore-only launch,
model table reference, unified prompt skeleton, answer budget.

***

## Reviewer (general)

[ref: #roles-reviewer]

**When:** any diff needs a general quality pass; the user asked for review
without naming an aspect. Default role when intent is unclear.

**Output contract:** findings ordered by severity with `file:line` anchors;
if no findings, say so and list residual test gaps.

**Prompt template:**

```text
Role: Reviewer. Review only — you are read-only; do not edit files.

Scope under review:
<diff / branch / file paths>

Context (reference only, never permission to expand scope):
<spec / docs / memory paths>

Focus:
- Behavioral regressions
- Missing or weak tests
- Architecture/layering violations
- Compatibility and rollout gaps
- Documentation drift

Rules:
- Findings first, ordered by severity, with file:line anchors.
- No style nits a linter already covers.
- If there are no findings, say so and list residual test gaps.
- Answer budget: at most 8 findings, each at most 2 sentences.

Report format: Findings / Residual gaps / Unavailable operations.
```

***

## Domain reviewer

[ref: #roles-domain]

**When:** diff touches stateful workflows, transitions, or user-visible
behavior.

**Output contract:** transition, side-effect, and test-gap findings; each
finding names the affected user group or system.

**Prompt template:**

```text
Role: Domain reviewer. Review only — you are read-only; do not edit files.

Scope under review:
<workflow/domain code diff>

Context (reference only, never permission to expand scope):
<spec / docs / memory paths>

Focus:
- Allowed state transitions and invalid transitions
- Audit/history/read-model changes
- User-visible side effects
- Ownership and visibility rules
- Missing domain tests

Rules:
- Findings first, ordered by severity, with file:line anchors.
- Name the affected user group or system per finding.
- No style nits a linter already covers.
- If there are no findings, say so and list residual test gaps.
- Answer budget: at most 8 findings, each at most 2 sentences.

Report format: Findings / Residual gaps / Unavailable operations.
```

***

## Security reviewer

[ref: #roles-security]

**When:** diff touches auth, permissions, file/data access, privacy, or
sensitive-data handling.

**Output contract:** security findings ordered by severity with exact
anchors; negative-test gaps and rollback/disable options named.

**Prompt template:**

```text
Role: Security reviewer. Review only — you are read-only; do not edit files.

Scope under review:
<auth/access/privacy code diff>

Context (reference only, never permission to expand scope):
<spec / docs / memory paths>

Focus:
- Auth bypass or permission regression
- Ownership, tenant, or file/data exposure
- Sensitive data in logs, tests, fixtures, events, or docs
- Negative auth/access tests
- Rollback or disable path for risky behavior

Rules:
- Findings first, ordered by severity, with file:line anchors.
- No style nits a linter already covers.
- If there are no findings, say so and list residual gaps.
- Answer budget: at most 8 findings, each at most 2 sentences.

Report format: Findings / Residual gaps / Unavailable operations.
```

***

## Integration reviewer

[ref: #roles-integration]

**When:** diff touches external clients, events, consumers, workers, or
rollout behavior.

**Output contract:** compatibility, retry, idempotency, and observability
findings plus recommended validation.

**Prompt template:**

```text
Role: Integration reviewer. Review only — you are read-only; do not edit files.

Scope under review:
<integration/consumer/worker code diff>

Context (reference only, never permission to expand scope):
<spec / docs / memory paths>

Focus:
- External schema compatibility
- Retry, timeout, and error mapping
- Idempotency and duplicate event behavior
- Transaction and acknowledgement/commit ordering
- Settings, feature flags, and mixed-version rollout
- Observability for failures

Rules:
- Findings first, ordered by severity, with file:line anchors.
- No style nits a linter already covers.
- If there are no findings, say so and list residual gaps.
- Answer budget: at most 8 findings, each at most 2 sentences.

Report format: Findings / Residual gaps / Unavailable operations.
```

***

## Test auditor

[ref: #roles-test-auditor]

**When:** user asks whether tests suffice; diff changes behavior and tests
look thin.

**Output contract:** required test additions, nice-to-have tests, scoped
commands to run, residual risk if tests are not added.

**Prompt template:**

```text
Role: Test auditor. Review only — you are read-only; do not edit files.

Scope under review:
<code diff and tests>

Context (reference only, never permission to expand scope):
<spec / docs / memory paths>

Focus:
- Missing tests for changed behavior
- Weak assertions
- Missing negative paths
- Over-mocked integration behavior
- Recommended scoped test commands from project docs

Rules:
- Findings first, ordered by severity, with file:line anchors.
- Separate required additions from nice-to-have tests.
- No style nits a linter already covers.
- If there are no findings, say so and list residual risk.
- Answer budget: at most 8 findings, each at most 2 sentences.

Report format: Findings / Residual gaps / Unavailable operations.
```

***

## Docs auditor

[ref: #roles-docs-auditor]

**When:** diff changes documented behavior; specs or context files were
touched — or should have been.

**Output contract:** documentation findings, duplication or drift risks,
remaining documentation gaps.

**Prompt template:**

```text
Role: Docs auditor. Review only — you are read-only; do not edit files.

Scope under review:
<code diff plus related spec/context docs>

Context (reference only, never permission to expand scope):
<spec / docs / memory paths>

Focus:
- Spec/context consistency with the diff
- Repository's documented language and status vocabulary
- No duplicated global rules
- Links to canonical policy files
- Docs kept compact and agent-facing

Rules:
- Findings first, ordered by severity, with file:line anchors.
- No style nits a linter already covers.
- If there are no findings, say so and list remaining documentation gaps.
- Answer budget: at most 8 findings, each at most 2 sentences.

Report format: Findings / Residual gaps / Unavailable operations.
```

***

## Data reviewer

[ref: #roles-data-reviewer]

**When:** diff includes migrations, backfills, or data-shape changes.

**Output contract:** rollback, nullability, lock, and mixed-version findings
plus recommended validation on disposable data.

**Prompt template:**

```text
Role: Data reviewer. Review only — you are read-only; do not edit files.

Scope under review:
<migration/backfill/data-shape diff>

Context (reference only, never permission to expand scope):
<spec / docs / memory paths>

Focus:
- Nullability, defaults, and existing production data shape
- Backfill cost and lock risk
- Forward and rollback/mitigation path
- Mixed-version compatibility
- Validation evidence on disposable data

Rules:
- Findings first, ordered by severity, with file:line anchors.
- No style nits a linter already covers.
- If there are no findings, say so and list residual gaps.
- Answer budget: at most 8 findings, each at most 2 sentences.

Report format: Findings / Residual gaps / Unavailable operations.
```

***

## Parent integration workflow

[ref: #roles-parent-workflow]

Subagent output is **evidence, not truth**. The parent agent owns the final
decision, integration, validation, and report.

**Triage rules:**

- Every finding is either accepted (fix applied or documented as deferred)
  or rejected with a stated reason.
- Final validation runs in the parent context or is clearly marked
  unverified.
- The final report names which roles reviewed the work.

**Fixed pairings per diff type:**

| Diff type | Roles |
| --- | --- |
| API / schema contract change | Reviewer + Test auditor |
| Stateful workflow change | Domain reviewer + Test auditor |
| Consumer / job / worker change | Integration reviewer + Test auditor |
| File / data-access change | Security reviewer + Test auditor |
| Migration / data change | Data reviewer + Test auditor |

**Caps and freshness:**

- At most 3 roles per diff; one Reviewer is enough for routine changes.
- After the diff changes materially, stale findings are discarded; rerun the
  role if the risk remains.
