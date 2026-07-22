---
subject: "Requirement verb semantics lookup; `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY` definitions with `REQUIRED`, `SHALL`, `RECOMMENDED`, `OPTIONAL` synonyms, uppercase versus bold markup sensitivity, justification duty on deviation, BCP 14 incantation, RFC 2119, RFC 8174, interoperability on optional points."
index:
  - anchor: rfc-verbs
    what: "The BCP 14 keyword table: `MUST`/`MUST NOT`/`SHOULD`/`SHOULD NOT`/`MAY` with synonyms, uppercase-and-bold sensitivity rules, deviation-justification duties, and the standard RFC 2119/8174 incantation for adopting documents."
    problem: "Agent-facing document mixes `MUST`, `SHOULD`, `MAY` across instructions, so misreading obligation strength either skips absolute rules or wastes effort treating optional guidance as mandatory; requirement level ambiguity, keyword semantics, compliance misjudgment, bold markup meaning, uppercase sensitivity, deviation justification, synonym confusion, normative language, bcp interpretation."
    use_when: "Interpreting requirement-level keywords in any skill or instruction document; deciding whether deviation from guidance needs justification; drafting documents that adopt BCP 14 language; uppercase versus lowercase verb meaning disputed."
    avoid_when: ""
    expected: ""
aips: []
---

# RFC 2119 / 8174 — Requirement Verbs for Agent Instructions

## Requirement Verbs
[ref: #rfc-verbs]

> Interpretation of requirement-level keywords per BCP 14 (RFC 2119, updated by RFC 8174).
> These verbs apply when rendered in **ALL CAPS** or in **bold** (e.g., `**must**`, `**should**`) in agent-facing documents.

## Definitions

| Verb | Synonyms | Meaning |
|------|----------|---------|
| **MUST** | REQUIRED, SHALL | Absolute requirement. Non-compliance breaks correctness, security, or interoperability. |
| **MUST NOT** | SHALL NOT | Absolute prohibition. Violation is an error. |
| **SHOULD** | RECOMMENDED | Default path. Override only after understanding full implications and accepting the risk. |
| **SHOULD NOT** | NOT RECOMMENDED | Default is to avoid. Acceptable only after careful weighing of trade-offs. |
| **MAY** | OPTIONAL | Truly optional. Implementor decides. Two interoperable implementations may differ here. |

## Agent Usage Rules

1. **Case sensitivity and markup** — These meanings apply to UPPERCASE forms (`MUST`, not `must`) and to bold forms (`**must**`, `**should**`, `**may**`) regardless of case. Non-bold, lowercase variants carry ordinary English sense and are not normative.
2. **Use sparingly** — Reserve MUST / MUST NOT for situations where deviation causes harm (security, data loss, broken contracts). Do not use them to express mere preference.
3. **SHOULD implies justification** — When an instruction says SHOULD, the default is to obey. If the agent deviates, it MUST understand and be prepared to explain why.
4. **MAY implies negotiation** — Two agents (or two implementations) MAY differ on an optional point and MUST still interoperate, albeit with reduced functionality on the missing side.

## Standard Incantation

When a document adopts these keywords, it SHOULD include near its start:

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when they appear in all capitals or in bold markup (e.g., `**must**`).

## References

- `read-for-comments` skill — RFC 2119 (original definitions) and RFC 8174 (uppercase-only clarification, adds NOT RECOMMENDED)
