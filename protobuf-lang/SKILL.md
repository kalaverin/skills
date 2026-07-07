---
name: protobuf-lang
description: >
  MANDATORY skill for Buf Protobuf lint and schema style. Use when writing,
  editing, or reviewing `.proto` files, `buf.yaml` configuration, packages,
  imports, enums, messages, services, RPCs, or comments.
triggers:
  any:
    files: "fd -e proto"
    request: "protobuf, proto, buf, buf.yaml"
requires:
  - api-design
---

# SKILL: Protobuf Schema Expert

You are an expert Backend Engineer and Protobuf API Designer. This document is your authoritative source of truth for Protobuf styling, formatting, and linting rules based on the Buf STANDARD ruleset.

**Skill Boundary:** This skill enforces Buf Protobuf Style Guide and Lint Rules (packages, imports, enums, messages, services, RPCs, comments, `buf.yaml`). For Google AIP resource design, HTTP/gRPC transcoding, and API structure, consult the `api-design` skill.

## ⚠️ STRICT READING CONSTRAINT (LAZY-LOAD PROTOCOL)
You MUST NOT read the file `references/rules.md` in its entirety. You MUST use partial extraction to preserve context memory and avoid hallucinations.
"
**Extraction Execution:**"
1. Match your current task to a "Trigger / Situation" in the table below.
2. Copy the corresponding `[ref: ...]` tag.
3. Use `rg` to extract ONLY the relevant section.
   *Example CLI command:* `rg -A 80 "\\[ref: #enums\\]" references/rules.md`
4. Read the extracted rules and apply them strictly to your Protobuf schema.

---

## 📚 TRIGGER TABLE

| Trigger / Situation | Target Section | Anchor Tag for Search |
|:---|:---|:---|
| Setting up a new proto file; declaring packages; file layout. | Files and Packages | `[ref: #files-and-packages]` |
| Adding or reviewing imports; handling unused/public imports. | Imports | `[ref: #imports]` |
| Defining or modifying enums; zero values; aliasing; naming. | Enums | `[ref: #enums]` |
| Defining messages; field naming; oneofs; required fields. | Messages | `[ref: #messages]` |
| Designing RPCs; naming services/methods; request/response types. | Services and RPCs | `[ref: #services-and-rpcs]` |
| Writing comments; setting proto syntax; organizing file layout. | Comments & Layout | `[ref: #comments-and-layout]` |
| Best practices for schema evolution, naming, and nesting. | Design Recs | `[ref: #design-recommendations]` |
| Understanding rule categories (MINIMAL, BASIC, STANDARD). | Rule Categories | `[ref: #rule-categories]` |
| Looking up specific Buf lint rule definitions (e.g., PROTOVALIDATE). | Complete Rule Ref | `[ref: #rule-reference]` |
| What is left out of this guide (custom options, generation). | Left Out | `[ref: #what-was-left-out]` |
| Setting up `buf.yaml` or choosing a rule category. | Quick Start | `[ref: #quick-start]` |
| Configuring buf.yaml for linting, exceptions, or suffixes. | Configuration | `[ref: #configuration]` |

---

## ⚙️ WORKFLOW
1. **Analyze Task:** Determine what Protobuf element you are creating/editing (e.g., RPC, Enum, Message, import, `buf.yaml`).
2. **Lookup:** Find the relevant tag in the Trigger Table.
3. **Extract:** Run `rg` using the exact `[ref: #...]` marker in `references/rules.md`. Use a sufficiently large `-A` flag (e.g., 80-100) to capture code examples.
4. **Implement:** Write or refactor the Protobuf code ensuring 100% compliance with the extracted rules.
5. **Lint (if `buf.yaml` exists):** Run `buf lint` and fix any violations. Only fix code you modified.
6. **Verify:**
   - Confirm every package, enum, message, service, and RPC follows the extracted rules.
   - Confirm no contradictions exist with the `api-design` skill for AIP-level design decisions.
   - Confirm no unmodified files were changed.
