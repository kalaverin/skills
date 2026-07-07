---
name: api-design
description: >
  MANDATORY skill for Google AIP API resource design and compliance. Covers
  resources, operations, fields, design patterns, compatibility, polish, and
  proto API structure. For Buf lint and proto schema style, use the
  protobuf-lang skill.
triggers:
  request: "openapi, swagger, graphql, grpc, rest, api design, fastapi, flask"
requires:
  - read-for-comments
  - protobuf-lang
---

# SKILL: Strict API Design & Compliance (Google AIP)

You are an expert API Architect. **This document is a binding rule set, not a recommendation.**"
"
Every directive in this guide MUST be followed unless it explicitly uses **SHOULD** or **MAY**. The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when they appear in all capitals or in bold markup.

## 1. Compliance and Default Rules

* **Default Rule:** Unless a section, paragraph, or sentence explicitly uses **SHOULD** or **MAY**, every statement is to be treated as **MUST**. You MUST NOT apply external style preferences or general API-design heuristics in place of the rules documented here.
* **Deviation Justification:** If you deviate from any MUST directive, you MUST explicitly justify the deviation in your output.
* **Skill Boundary:** This skill enforces Google AIP resource-design rules (resources, operations, fields, patterns, compatibility, polish, and proto API structure). For Buf lint and proto schema style, consult the `protobuf-lang` skill.
* **RFC Verbs:** For precise semantics of requirement-level verbs, consult the `read-for-comments` skill.

## 2. Agent Context Management (CRITICAL LAZY-LOAD PROTOCOL)

The individual chapter files linked in the index below are extremely large (hundreds of pages in aggregate). You **MUST NOT** read them in full, load them into context indiscriminately, or attempt to summarize the entire collection.

Instead, you MUST use the index below as your sole routing table:
1. Match your current task to the exact trigger in the tables.
2. Identify the specific `Target File` and the exact `Anchor`.
3. Use your file search tool (e.g., `rg`) to extract **only** the section corresponding to that Anchor/Header.
   *Example CLI command:* `rg -A 100 "\[ref: #resource-oriented-design-aip-121\]" references/04_resource_design.md` (Use the exact `[ref: #...]` marker in the search query).
4. If a task spans multiple triggers, open each referenced section in turn. Keep context usage minimal and precise.

---

## 3. Mandatory Lookups by Task (The Routing Index)

**This index is mandatory.** Do not guess, do not rely on training data, and do not skip the section because the topic seems familiar. All triggers carry the weight of MUST.

### RFC 2119 / 8174 Requirement Verbs
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Interpreting RFC 2119/8174 requirement verbs (MUST, SHOULD, MAY). | `references/rfc_verbs.md` | RFC 2119 / 8174 Requirement Verbs | `[ref: #rfc-verbs]` |

### Chapter 1 — Foundation and Process
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Creating a new AIP; deciding AIP type; approval workflow. | `references/01_foundation_and_process.md` | 1.1 AIP Purpose | `[ref: #aip-purpose-and-guidelines-aip-1]` |
| Assigning an AIP number; choosing a number block. | `references/01_foundation_and_process.md` | 1.2 AIP Numbering | `[ref: #aip-numbering-aip-2]` |
| Versioning AIPs; changelog tags; historical referencing. | `references/01_foundation_and_process.md` | 1.3 AIP Versioning | `[ref: #aip-versioning-aip-3]` |
| Violating a standard; documenting exceptions. | `references/01_foundation_and_process.md` | 1.4 Precedent | `[ref: #precedent-and-standards-exceptions-aip-200]` |
| Writing/editing an AIP document: structure, RFC keywords. | `references/01_foundation_and_process.md` | 1.5 AIP Style | `[ref: #aip-style-and-guidance-aip-8]` |
| Unclear terminology: backend/frontend, declarative client. | `references/01_foundation_and_process.md` | 1.6 Glossary | `[ref: #glossary-aip-9]` |

### Chapter 2 — Design Review
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Formal design approval needs; release levels (Alpha/Beta). | `references/02_design_review.md` | 2.1 Design Review FAQ | `[ref: #api-design-review-faq-aip-100]` |
| Promoting Alpha to Beta; temporary violations (`beta-blocker`). | `references/02_design_review.md` | 2.2 Beta-Blocking | `[ref: #beta-blocking-changes-aip-205]` |

### Chapter 3 — API Concepts
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Management vs Data plane; declarative clients; tradeoffs. | `references/03_api_concepts.md` | 3.1 Planes | `[ref: #planes-aip-111]` |

### Chapter 4 — Resource Design
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Designing from scratch; standard vs custom methods. | `references/04_resource_design.md` | 4.1 Resource-Oriented | `[ref: #resource-oriented-design-aip-121]` |
| Forming resource names; relative vs full. | `references/04_resource_design.md` | 4.2 Resource Names | `[ref: #resource-names-aip-122]` |
| Defining `google.api.resource`; resource types. | `references/04_resource_design.md` | 4.3 Resource Types | `[ref: #resource-types-aip-123]` |
| Modeling many-to-one or many-to-many relationships. | `references/04_resource_design.md` | 4.4 Resource Association | `[ref: #resource-association-aip-124]` |
| Enums vs strings/booleans; naming enum values. | `references/04_resource_design.md` | 4.5 Enumerations | `[ref: #enumerations-aip-126]` |
| Designing for Terraform/IaC; `reconciling` fields. | `references/04_resource_design.md` | 4.6 Declarative-Friendly | `[ref: #declarative-friendly-interfaces-aip-128]` |
| Field ownership; effective/default values. | `references/04_resource_design.md` | 4.7 Server-Modified | `[ref: #server-modified-values-and-defaults-aip-129]` |
| Singleton resources (one instance per parent). | `references/04_resource_design.md` | 4.8 Singleton Resources | `[ref: #singleton-resources-aip-156]` |
| Safe rollout for policy resources; experiment preview. | `references/04_resource_design.md` | 4.9 Policy Preview | `[ref: #policy-preview-aip-236]` |

### Chapter 5 — Operations
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Method categories: standard, batch, custom, streaming. | `references/05_operations.md` | 5.1 Method Categories | `[ref: #method-categories-aip-130]` |
| Retrieval of a single resource (`Get` RPC). | `references/05_operations.md` | 5.2 Get | `[ref: #standard-method-get-aip-131]` |
| Retrieval of a collection (`List` RPC); pagination. | `references/05_operations.md` | 5.3 List | `[ref: #standard-method-list-aip-132]` |
| Resource creation (`Create` RPC); sync vs async. | `references/05_operations.md` | 5.4 Create | `[ref: #standard-method-create-aip-133]` |
| Resource update (`Update` RPC); PATCH vs PUT. | `references/05_operations.md` | 5.5 Update | `[ref: #standard-method-update-aip-134]` |
| Resource deletion (`Delete` RPC); soft vs hard delete. | `references/05_operations.md` | 5.6 Delete | `[ref: #standard-method-delete-aip-135]` |
| Custom methods (verb + noun). | `references/05_operations.md` | 5.7 Custom Methods | `[ref: #custom-methods-aip-136]` |
| Long-running operations (>10s); `Operation`. | `references/05_operations.md` | 5.8 Long-Running | `[ref: #long-running-operations-aip-151]` |
| Batch Get (multiple resources atomically). | `references/05_operations.md` | 5.9 Batch Get | `[ref: #batch-method-get-aip-231]` |
| Batch Create (multiple resources in a transaction). | `references/05_operations.md` | 5.10 Batch Create | `[ref: #batch-method-create-aip-233]` |
| Batch Update (multiple resources in a transaction). | `references/05_operations.md` | 5.11 Batch Update | `[ref: #batch-method-update-aip-234]` |
| Batch Delete (multiple resources in a transaction). | `references/05_operations.md` | 5.12 Batch Delete | `[ref: #batch-method-delete-aip-235]` |

### Chapter 6 — Fields
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Naming a field; string vs bytes; `display_name`. | `references/06_fields.md` | 6.1 Field Names | `[ref: #field-names-aip-140]` |
| Annotating format (UUID4, IPv4) via `field_info`. | `references/06_fields.md` | 6.2 FieldInfo | `[ref: #fields-and-fieldinfo-aip-202]` |
| Documenting behavior (`REQUIRED`, `OPTIONAL`). | `references/06_fields.md` | 6.3 Field Behavior | `[ref: #field-behavior-documentation-aip-203]` |
| Naming quantity fields; unit suffixes. | `references/06_fields.md` | 6.4 Quantities | `[ref: #quantities-aip-141]` |
| Time representation (`Timestamp`, `Duration`). | `references/06_fields.md` | 6.5 Time and Duration | `[ref: #time-and-duration-aip-142]` |
| Standardized codes (language, region, currency). | `references/06_fields.md` | 6.6 Standardized Codes | `[ref: #standardized-codes-aip-143]` |
| Repeated fields (scalar vs message). | `references/06_fields.md` | 6.7 Repeated Fields | `[ref: #repeated-fields-aip-144]` |
| Modeling ranges (`start_`/`end_`). | `references/06_fields.md` | 6.8 Ranges | `[ref: #ranges-aip-145]` |
| Generic fields (`oneof`, `map`, `Struct`, `Any`). | `references/06_fields.md` | 6.9 Generic Fields | `[ref: #generic-fields-aip-146]` |
| Sensitive data (secrets, keys). | `references/06_fields.md` | 6.10 Sensitive Fields | `[ref: #sensitive-fields-aip-147]` |
| Standard field names (`name`, `parent`, etc.). | `references/06_fields.md` | 6.11 Standard Fields | `[ref: #standard-fields-aip-148]` |
| Default vs unset values; `optional` keyword. | `references/06_fields.md` | 6.12 Unset Fields | `[ref: #unset-field-values-aip-149]` |
| Resource state enum (`ACTIVE`, `SUCCEEDED`). | `references/06_fields.md` | 6.13 States | `[ref: #states-aip-216]` |

### Chapter 7 — Design Patterns
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Configurable tasks; `Job` resources; `Run` custom methods. | `references/07_design_patterns.md` | 7.1 Jobs | `[ref: #jobs-aip-152]` |
| Bulk import or export of data. | `references/07_design_patterns.md` | 7.2 Import/Export | `[ref: #import-and-export-aip-153]` |
| Optimistic concurrency control; `etag` field. | `references/07_design_patterns.md` | 7.3 Freshness | `[ref: #resource-freshness-validation-aip-154]` |
| Request idempotency; `request_id` field. | `references/07_design_patterns.md` | 7.4 Request ID | `[ref: #request-identification-aip-155]` |
| Partial responses; field masks vs view enums. | `references/07_design_patterns.md` | 7.5 Partial Responses | `[ref: #partial-responses-aip-157]` |
| Pagination (`page_size`, `page_token`). | `references/07_design_patterns.md` | 7.6 Pagination | `[ref: #pagination-aip-158]` |
| Reading across multiple collections (wildcard `-`). | `references/07_design_patterns.md` | 7.7 Reading Across | `[ref: #reading-across-collections-aip-159]` |
| Filter queries on `List` methods; syntax. | `references/07_design_patterns.md` | 7.8 Filtering | `[ref: #filtering-aip-160]` |
| Partial updates; `google.protobuf.FieldMask`. | `references/07_design_patterns.md` | 7.9 Field Masks | `[ref: #field-masks-aip-161]` |
| Revision history; `{Resource}Revision`; `rollback`. | `references/07_design_patterns.md` | 7.10 Resource Revisions | `[ref: #resource-revisions-aip-162]` |
| Validate-only mode; `validate_only` field. | `references/07_design_patterns.md` | 7.11 Change Validation | `[ref: #change-validation-aip-163]` |
| Soft delete with recovery (`Undelete` method). | `references/07_design_patterns.md` | 7.12 Soft Delete | `[ref: #soft-delete-aip-164]` |
| Criteria-based delete (Purge method). | `references/07_design_patterns.md` | 7.13 Criteria Delete | `[ref: #criteria-based-delete-aip-165]` |
| Unicode limits, uniqueness, normalization. | `references/07_design_patterns.md` | 7.14 Unicode | `[ref: #unicode-aip-210]` |
| Authorization checks (`PERMISSION_DENIED`). | `references/07_design_patterns.md` | 7.15 Authorization | `[ref: #authorization-checks-aip-211]` |
| Resource expiration (`expire_time` vs `ttl`). | `references/07_design_patterns.md` | 7.16 Resource Expiration| `[ref: #resource-expiration-aip-214]` |
| Temporarily unreachable resources. | `references/07_design_patterns.md` | 7.17 Unreachable | `[ref: #unreachable-resources-aip-217]` |

### Chapter 8 — Compatibility and Versioning
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Backwards compatibility; adding/removing fields. | `references/08_compatibility_and_versioning.md` | 8.1 Backwards Compat | `[ref: #backwards-compatibility-aip-180]` |
| Stability levels (alpha, beta, stable); deprecation. | `references/08_compatibility_and_versioning.md` | 8.2 Stability Levels | `[ref: #stability-levels-aip-181]` |
| External software versions; EOL management. | `references/08_compatibility_and_versioning.md` | 8.3 External Dependencies| `[ref: #external-software-dependencies-aip-182]` |
| API versioning strategy; package naming; URIs. | `references/08_compatibility_and_versioning.md` | 8.4 API Versioning | `[ref: #api-versioning-aip-185]` |

### Chapter 9 — Polish
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| Naming conventions (services, methods); abbreviations. | `references/09_polish.md` | 9.1 Naming Conventions | `[ref: #naming-conventions-aip-190]` |
| File/directory structure; package names; languages. | `references/09_polish.md` | 9.2 File Structure | `[ref: #file-and-directory-structure-aip-191]` |
| Public comments; CommonMark; deprecation notices. | `references/09_polish.md` | 9.3 Documentation | `[ref: #documentation-aip-192]` |
| Designing error responses (`ErrorInfo`, status codes). | `references/09_polish.md` | 9.4 Errors | `[ref: #errors-aip-193]` |
| Automatic retry configuration; retryable errors. | `references/09_polish.md` | 9.5 Retry Configuration | `[ref: #automatic-retry-configuration-aip-194]` |

### Chapter 10 — Protocol Buffers
| Trigger / Situation | Target File | Section Header | Anchor |
|---|---|---|---|
| HTTP and gRPC transcoding; URI mapping. | `references/10_protocol_buffers.md` | 10.1 HTTP Transcoding | `[ref: #http-and-grpc-transcoding-aip-127]` |
| Common components; global vs org-specific packages. | `references/10_protocol_buffers.md` | 10.2 Common Components | `[ref: #common-components-aip-213]` |
| Structuring API-specific protos; major versioning. | `references/10_protocol_buffers.md` | 10.3 API-Specific Protos| `[ref: #api-specific-protos-aip-215]` |

---

## 4. Master Execution Workflow
1. **Analyze Design Task:** Identify the API component (resource, method, field, relationship, error model, etc.) you are creating or reviewing.
2. **Consult the Index:** Locate every row in the Routing Index that matches the component or decision. Read `references/rfc_verbs.md` first if any requirement-level verb is ambiguous.
3. **Extract Rules:** For each matched row, run a precise `rg` search using the `[ref: #...]` marker in the `Target File` and read only that section. Do not load full reference files into context.
4. **Apply Rules:** Draft or review routes, resource names, request/response shapes, field semantics, and error behavior so that every element complies with the extracted AIP section.
5. **Proto Review (if applicable):** If the change touches `.proto` files, invoke the `protobuf-lang` skill for Buf lint and proto schema style. Do not duplicate those rules here.
6. **Verify:**
   - Confirm every route, method, field, and resource mentioned in the design complies with the extracted AIP section.
   - Confirm no contradictions exist between referenced sections.
   - Confirm any `.proto` changes were reviewed with `protobuf-lang`.
   - Confirm no unmodified files were changed.
