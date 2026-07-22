---
subject: "Google AIP system foundation and governance process; proposal purpose, lifecycle states, editor workflow, `AIP-1` types, number assignment, reserved blocks, `AIP-2` reference format, date-based `YYYY-MM-DD` versioning, changelog, `AIP-3`, precedent violations, standards exceptions, `aip.dev/not-precedent` comments, `AIP-200`, authoring style, document structure, front matter, requirement keywords, `AIP-8`, API terminology glossary, `AIP-9`."
index:
  - anchor: aip-purpose-and-guidelines-aip-1
    what: "The AIP-1 charter defining what an API Improvement Proposal is, its `Draft`/`Reviewing`/`Approved` lifecycle states, escalation ladder (producer, editors, TL), and consensus workflow for proposing and accepting guidance."
    problem: "Team ships API design based on unapproved draft proposal or writes guidance that duplicates existing corpus, so standards fragment and reviewers argue from inconsistent baselines; draft versus approved state, consensus process, editor signoff, stakeholder escalation, guidance duplication, proposal lifecycle, withdrawn replaced deferred."
    use_when: "Evaluating whether cited AIP is binding best practice; deciding whom to approach about disputed design ruling; drafting new entry for the corpus; tracking proposal through review toward approval."
    avoid_when: "Guidance treated as binding while state is `Draft` or `Reviewing`; rejected corpus entries mined for current rules; local team policy contradicting approved AIPs upheld without escalation."
    expected: "Only `Approved` AIPs serve as review baseline, proposals advance through consensus signoff, and every state transition is recorded by editors."
  - anchor: aip-numbering-aip-2
    what: "The AIP-2 numbering scheme: editors assign every proposal an arbitrary number at draft intake, the space partitions into scoped ranges (meta `1–99`, general `100–999`, product areas like `2500–2599`), and citations use bare unpadded form like `AIP-8`."
    problem: "Design documents cite proposals inconsistently with zero-padded or invented identifiers, so cross-references break and domain-scoped guidance gets mistaken for general rules; zero padding, bare number citation, reserved block allocation, index collision, scope routing, editor assignment, mnemonic numbering."
    use_when: "Citing any AIP in prose, code comments, or review feedback; requesting dedicated number range for team-scoped guidance; interpreting which corpus range covers given topic area; deciding whether identifier refers to meta process or design rule."
    avoid_when: "Numbers minted by authors instead of editors; padding added for sorting (`AIP-0008`); block boundaries assumed to signal normative weight rather than scope."
    expected: "Every identifier appears exactly as assigned without padding, domain proposals live inside their allocated range, and the index distinguishes approved entries from drafts."
  - anchor: aip-versioning-aip-3
    what: "The AIP-3 date-based versioning scheme: one universal corpus version stamped `YYYY-MM-DD`, tagged `v{version}` in source control, bumped on significant change, with per-AIP changelog entries."
    problem: "API designed under older guidance cannot justify its choices after rules reverse, because corpus evolved without fixed reference points and per-document versions tangle cross-references; guidance reversal, historical justification, date stamp tagging, snapshot date, changelog audit, design archaeology, combinatorial pinning."
    use_when: "Pinning design decision to guidance in force at authoring date; cutting release tag after significant corpus edit; auditing why old API diverges from current rules; choosing between per-document and corpus-wide scheme."
    avoid_when: "Semantic versions invented for AIPs; per-AIP version pins multiplied across cross-references; changelog skipped after significant edit."
    expected: "Corpus carries one date tag per notable revision, each AIP lists its changelog, and any past design choice can be traced to guidance valid at that date."
  - anchor: precedent-and-standards-exceptions-aip-200
    what: "The AIP-200 not-precedent policy: existing violations never justify new ones, every intentional deviation carries an internal `aip.dev/not-precedent` comment explaining what and why, and single-API consistency may outweigh global style."
    problem: "Legacy API violating standards gets cited as precedent for new surfaces, so contra-standard patterns multiply silently and original rationale disappears; undocumented exception, copy propagation, not-precedent marker, local consistency tradeoff, oauth conformance, expediency waiver, historical mistake."
    use_when: "Inheriting interface that predates current guidance; weighing deviation for external spec conformance (OAuth), partner-system fit, hard deadline, or technical constraint; documenting deliberate rule break so future designers see it."
    avoid_when: "Pre-beta API treated as precedent source (only beta/GA sets precedent); violation copied without linking comment; global pattern broken mid-API where internal uniformity matters more."
    expected: "Each deliberate break carries linking `aip.dev/not-precedent` comment with reason, new APIs follow standards despite legacy counterexamples, and in-API uniformity stays intact."
  - anchor: aip-style-and-guidance-aip-8
    what: "The AIP-8 authoring standard for AIPs themselves: one-subject mandate, Markdown file `NNNN.md` with required metadata header (`id`, `state`, `created`, `permalink`), noun title plus `## Guidance` layout, bold lower-case RFC-2119 keywords, and protobuf-based examples."
    problem: "Drafted design proposal uses imperative title, embeds normative rules inside rationale prose, or misuses requirement keywords, so editors bounce it and readers cannot cite actionable clauses; discrete topic scope, front matter fields, heading skeleton, bold keyword casing, guidance versus rationale, length discipline, protobuf example style."
    use_when: "Authoring or editing any corpus entry; formatting file header and four-digit filename for publication; deciding where normative text ends and background justification begins; choosing obligation keyword strength with documented escape cases."
    avoid_when: "Anti-pattern-only content proposed as standalone entry; RFC-2119 terms placed inside rationale section; imperative verb title chosen over noun phrase; conditional pattern documented without stating applicability conditions."
    expected: "Entry covers one narrow subject in roughly two pages, header and heading layout conform, keywords stay properly cased with override examples, and rationale stays free of obligations."
  - anchor: glossary-aip-9
    what: "The AIP-9 shared glossary pinning canonical meanings for terms like `API service`, `API definition`, `API producer`/`API consumer`, `client` vs `user`, and `declarative client` across all AIPs."
    problem: "Discussion or review mixes terms like service, definition, product, backend, frontend, so participants argue past each other and documents read inconsistently; terminology ambiguity, producer consumer confusion, client versus user, network api boundary, declarative infrastructure automation, service endpoint naming."
    use_when: "Any term from shared vocabulary needs exact definition; writing or reviewing text that distinguishes an API's producer side from its consumer side or interface from implementation; interpreting which entity owns billing, deployment, or naming."
    avoid_when: ""
    expected: ""
aips: [1, 2, 3, 8, 9, 200]
---

# Foundation and Process

## 1. Meta — Foundation and Process

### 1.1 AIP Purpose and Guidelines (AIP-1)
[ref: #aip-purpose-and-guidelines-aip-1]

AIP stands for **API Improvement Proposal**: a design document providing high-level, concise documentation for API development. AIPs serve as the source of truth for API-related documentation and the means by which API teams discuss and come to consensus on API guidance. AIPs are maintained as Markdown files in the AIP repository, and each covers a single, discrete topic with clear, actionable guidance.

**Key principles for agents:**
- AIPs **must not** duplicate or contradict guidance in another AIP.
- API producers **should** rely primarily on AIPs in the **approved** state.
- The AIP process is consensus-driven: proposals require concrete references, well-defined examples, and prior art.

**AIP types**

There are two primary types of AIPs:

- **Guidance** — Describe standards and recommendations for API design. These provide instruction for API producers to help write simple, intuitive, and consistent APIs, and are used by API reviewers as a basis for review comments.
- **Process** — Describe procedures surrounding API design, including the AIP process itself. These enhance the way AIPs are proposed, reviewed, and maintained.

**Stakeholders**

The AIP process involves multiple stakeholders, with the following escalation path:

1. **API producer** — The author or team proposing an AIP.
2. **AIP editors** — Designated approvers responsible for the administrative and editorial aspects of shepherding AIPs. They manage the pipeline, assign proposal numbers, set AIP states, and ensure AIPs are readable. Editors are the final decision-makers on process matters.
3. **TL (Technical Lead)** — The final point of escalation for domain-specific or contentious decisions. At minimum, the TL with responsibility over the domain covered by the AIP **must** approve the proposal for it to advance to the approved state.

**Domain-specific AIPs**

Some AIPs apply only to a particular domain (for example, a specific product area or team). These AIPs are assigned a dedicated block of numbers in accordance with [AIP Numbering (AIP-2)](#aip-numbering-aip-2) and **must** clearly indicate their restricted scope in the document.

**AIP states**

At any given time, an AIP exists in exactly one of the following states. API producers **should** treat only **approved** AIPs as best current practice.

- **Draft** — The initial state. The AIP is being discussed and iterated upon, primarily by the original authors. Significant high-level iteration **should** occur outside the repository (e.g., in a shared document) before entering the Draft state.
- **Reviewing** — The authors have reached general consensus and the editors are now formally involved. At this stage, editors may request changes or suggest alternatives. To enter this state, one approver (other than the author) **must** provide formal signoff, and there **must not** be formal objections from other approvers.
- **Approved** — The AIP is agreed upon and considered best current practice. To enter this state, two approvers (other than the author) **must** provide formal signoff, and there **must not** be formal objections from other approvers. If an editor is the primary author, at least two *other* editors **must** approve it.
- **Withdrawn** — The author or champion has withdrawn the AIP. A withdrawn AIP may be taken up by another champion later.
- **Rejected** — The AIP editors have rejected the AIP. Rejected AIPs remain in the corpus as reference to inform future discussions.
- **Deferred** — The editors have marked the AIP as inactive because it has not been acted upon for a significant period of time.
- **Replaced** — The AIP has been superseded by another AIP. The replacement AIP **must** clearly explain the rationale; the replaced AIP remains accessible and links to its successor.

**Workflow**

The following rules govern the lifecycle of an AIP from proposal to acceptance or retirement.

*Proposing an AIP.* Before writing a full AIP, open an issue to circulate the fundamental idea for initial feedback. Proposals **should** reference prior art and/or concrete example use cases. Appropriate material includes existing external RFCs or standards, a corpus of APIs that have aligned on a similar pattern, or a concrete use case that has yet to be solved.

Once ready, create a pull request adding a new file (typically under `aip/new.md`) and ensure it is editable by maintainers. The editors will assign an AIP number and usually set the state to **Reviewing**. The editors may reject an AIP outright if it is fundamentally unsound or was previously discussed and rejected.

*Discussing an AIP.* The author is responsible for championing the AIP and pushing towards consensus. This may involve iterative revisions via follow-up commits and discussion in scheduled review meetings.

*Accepting an AIP.* To gain final approval, an AIP **must** be approved by the domain TL and at least one other editor, with no editors actively requesting changes. Once approved, the editors update the state to **Approved** and merge.

*Withdrawing or rejecting an AIP.* The author may withdraw an AIP by updating the pull request with a notice of withdrawal and rationale. If the group cannot reach consensus, the editors may reject the AIP by amending the pull request with a notice of rejection and rationale. In both cases, the editors update the state accordingly.

*Replacing an AIP.* In rare cases, an AIP may be replaced by another. This is **not** general practice: minor edits to approved AIPs are the common way to tweak guidance. However, if new guidance fundamentally alters the old guidance, the editors create a new AIP that, once approved, causes the old one to enter the **Replaced** state. The old AIP links to the new one.

> **Agent extension — not part of the AIP standard.** AIP lifecycle states are `Draft`, `Reviewing`, and `Approved` (plus inactive/suspended states for retired guidance); API producers should rely only on `Approved` AIPs. Moving a draft to `Reviewing` requires formal signoff from at least one AIP approver other than the author, after which AIP editors approve the final pull request. Much of the AIP guidance for protobuf APIs is mechanically enforceable with the Google API Linter (https://linter.aip.dev, `github.com/googleapis/api-linter`): it checks proto surfaces against AIP rules in CI, every rule has its own documentation page, and individual rules can be disabled with a leading comment. The linter is an aid, not a substitute for reading the AIPs — not all guidance is expressible as lint rules.

### 1.2 AIP Numbering (AIP-2)
[ref: #aip-numbering-aip-2]

The AIP numbering system provides a mechanism to index API Improvement Proposals and maintain a single source of truth. It enables collaborative, transparent iteration on API standards. This section describes how AIP numbers are assigned and how the number space is organized into blocks.

**Assigning AIP Numbers**

AIP editors (see [AIP-1](#aip-purpose-and-guidelines-aip-1)) are responsible for assigning a number to each AIP when it is accepted as a draft for review. Importantly, **all** AIPs receive numbers — not only approved ones. The AIP Index clearly delineates which AIPs are approved and binding and which remain under discussion.

Editors may reserve a specific block of numbers for groups of AIPs that are related in some way (for example, AIPs scoped to a specific product area or team). Beyond this, AIP numbers are assigned arbitrarily. In general, editors take the next available number off the stack to assign to a draft AIP, but occasionally may use a special or mnemonic number if useful.

**AIP Blocks**

The AIP number space is divided into the following recognized blocks:

*Generally Applicable*

| Block | Scope |
|-------|-------|
| **1–99** | Meta-AIPs (process-related). |
| **100–999** | General API design guidance. |

*Google Product Areas*

| Block | Scope |
|-------|-------|
| **2500–2599** | Cloud |
| **2700–2799** | Apps (Google Workspace) |
| **3000–3099** | Actions on Google |
| **3200–3299** | Firebase |
| **4100–4199** | Auth libraries |
| **4200–4299** | Client libraries |
| **4600–4699** | Geo |

To request a block for a specific team that is publishing API guidance or documentation germane to that team, reach out to the AIP editors.

**Reference Format**

Agents **must** reference AIPs by their bare number without zero-padding (e.g., `AIP-8`, not `AIP-0008`).

### 1.3 AIP Versioning (AIP-3)
[ref: #aip-versioning-aip-3]

This section defines the versioning scheme for AIPs.

**Version Format**

- AIPs **must** be versioned by date, using the ISO-8601 format `YYYY-MM-DD`, corresponding to the date the version was added.
- AIP versions **must** be available as tags on the source control system used to store the AIPs, using the format `v{version}`. For example: `v2023-03-28`.
- The AIPs **must** receive a new version when there is a significant change to one or more AIPs.
- Each AIP **must** include a changelog section with the date the change was made and a short description.

**Rationale**

Versions serve as reference points to AIPs at a specific point in time. They are crucial because guidance on an AIP can be reversed or include significant changes such that it no longer resembles the original design. APIs using AIPs may need to reference older AIP guidance to justify a design choice.

Date-based versioning allows a client to easily find the AIP guidance at the time an API was authored.

An alternative to a universal version is to attach specific versions to each AIP individually. However, AIPs often cross-reference one another. If each AIP had a specific version, cross-references would also have to specify specific versions of those referenced AIPs to provide complete guidance. A universal date-based version avoids this combinatorial complexity.

### 1.4 Precedent and Standards Exceptions (AIP-200)
[ref: #precedent-and-standards-exceptions-aip-200]

APIs are often written in ways that do not match guidance added to standards after those APIs have already been released. Additionally, it sometimes makes sense to intentionally violate standards for particular reasons, such as maintaining consistency with established systems, meeting stringent performance requirements, or other practical concerns. Finally, despite careful review, mistakes can slip through before release.

Since it is often not feasible to fix past mistakes or make standards serve every use case, APIs may retain these exceptions for quite some time. Further, since new APIs often base their designs on existing APIs, a standards violation in one API can spill over into others, even if the original reason for the exception does not apply. This makes it critical to "stop the bleeding" of standards exceptions into new APIs, and to document the reasons for each exception so historical wisdom is not lost.

**Stop the bleeding**

Existing APIs that violate standards **must never** be cited as precedent for new APIs. The mere fact that an API was previously approved does not justify repeating a standards violation.

**Documenting exceptions**

If an API violates AIP standards for any reason, there **must** be an internal comment linking to `aip.dev/not-precedent`. The comment **should** include an explanation of what violates standards and why it is necessary. For example:

```protobuf
message DailyMaintenanceWindow {
  // Time within the maintenance window to start the maintenance operations.
  // It must use the format "HH MM", where HH : [00-23] and MM : [00-59] GMT.
  // (-- aip.dev/not-precedent: This was designed for consistency with crontab,
  //     and preceded the AIP standards.
  //     Ordinarily, this type should be `google.type.TimeOfDay`. --)
  string start_time = 2;

  // Output only. Duration of the time window, automatically chosen to be
  // smallest possible in the given scenario.
  // (-- aip.dev/not-precedent: This preceded the AIP standards.
  //     Ordinarily, this type should be `google.protobuf.Duration`. --)
  string duration = 3;
}
```

**Important:** APIs are only considered to be precedent-setting if they are in **beta** or **GA**.

**Local consistency**

If an API violates a standard throughout, it would be jarring and frustrating to users to break the existing pattern only for the sake of adhering to the global standard.

For example, if all of an API's resources use `creation_time` (instead of the standard field `create_time` described in AIP-142), a new resource in that API **should** continue to follow the local pattern. However, others who might otherwise copy that API **must** be made aware that this is contra-standard and not something to cite as precedent when launching new APIs.

```protobuf
// ...
message Book {
  // (-- aip.dev/not-precedent: This field was present before there was a
  //     standard field.
  //     Ordinarily, it should be spelled `create_time`. --)
  google.protobuf.Timestamp creation_time = 1;
}

// ...
message Author {
  // (-- aip.dev/not-precedent: `Book` had `creation_time` before there was
  //     a standard field, so we match that here for consistency. Ordinarily,
  //     this would be spelled `create_time`. --)
  google.protobuf.Timestamp creation_time = 1;
}
```

**Pre-existing functionality**

Standards violations are sometimes overlooked before launching, resulting in APIs that become stable and therefore can not easily be modified. Additionally, a stable API may pre-date a standards requirement.

In these scenarios, it is difficult to make the API fit the standard. However, the API **should** still cite that the functionality is contra-standard so that other APIs do not copy the mistake and cite the existing API as a reason why their design **should** be approved.

**Adherence to external specification**

Occasionally, APIs **must** violate standards because specific requests are implementations of an external specification (for example, OAuth), and that specification may be at odds with AIP guidelines. In this case, it is likely to be appropriate to follow the external specification.

**Adherence to existing systems**

Similar to adherence to an external specification, it may be proper for an API to violate AIP guidelines to fit in with an existing system in some way. This is a fundamentally similar case where it is wise to meet the customer where they are. A potential example of this might be integration with or similarity to a partner API.

**Expediency**

Sometimes there are users who need an API surface by a very hard deadline or money walks away. Since most APIs serve a business purpose, there will be times when an API could be better but cannot be made so and delivered to users before the deadline. In those cases, API review councils **may** grant exceptions to ship APIs that violate guidelines due to time and business constraints.

**Technical concerns**

Internal systems sometimes have very specific implementation needs (e.g., they rely on operation transforms that speak UTF-16, not UTF-8) and adhering to AIP guidelines would require extra work that does not add significant value to API consumers. Future systems which are likely to expose an API at some point **should** bear this in mind to avoid building underlying infrastructure which makes it difficult to follow AIP guidelines.

> **Agent extension — not part of the AIP standard.** The practical companion of the not-precedent policy is the `aip.dev/not-precedent` comment convention used with the Google API Linter: when a rule violation is intentional, the rule is disabled with a leading comment above the element and an `aip.dev/not-precedent` comment documents why the deviation exists. This keeps justified exceptions recorded at the exact point of violation instead of letting them become silent precedent for future designs.

### 1.5 AIP Style and Guidance (AIP-8)
[ref: #aip-style-and-guidance-aip-8]

AIPs are design documents providing high-level, concise documentation for API design and development. Their goal is to serve as the source of truth for API-related documentation and the means by which API teams discuss and come to consensus on API guidance. AIPs are most useful when they are clear and concise, and cover a single topic well. In the same way that AIPs describe consistent patterns and style for use in APIs, they also follow consistent patterns and style.

**Guidance scope**

- AIPs **must** cover a single, discrete topic, and provide clear, actionable guidance.
- AIPs **must not** duplicate or contradict guidance in another AIP.
- AIPs **may** also cover what not to do, but **should not** cover only anti-patterns.
- If AIP guidance is conditional (e.g., a design pattern such as Jobs), the guidance **must** clearly explain under what conditions the guidance **should** be followed.

**Beneficiaries**

Guidance contained within an AIP **must** be beneficial to one or more types of clients or their authors, including but not limited to:

- Asset inventories which can be used to audit and analyze resources.
- Command line interfaces for exploration and simple automation.
- Custom controllers (e.g., auto-scalers) which poll live state and adjust resource configuration accordingly.
- Infrastructure-as-Code clients for orchestration and automation of multiple resources.
- Recommendation tools which provide guidance on which APIs are useful for specific use cases, and how to use them.
- SDKs to interact with an API from a programming language, often used heavily for data-plane operations.
- Security orchestration, automation, and remediation tools.
- Simple scripts to automate or orchestrate tasks.
- Test frameworks.
- Tools that operate on resource data at rest.
- Visual user interfaces for visualization and one-off manual actions.
- Users.

AIP guidance **must not** be a significant detriment to a client's usability, implementation difficulty, or maintenance difficulty. Examples of detriments include:

- Introduction of a non-uniform pattern in a standard method such that all clients must introduce additional code without sufficient benefit (e.g., List behaves one way except for resources that start with a particular name).
- Renames of well-established fields for minor improvements in readability (e.g., renaming `expire_time` to `lapse_time`).

While the length of AIPs will necessarily vary based on complexity, most AIPs **should** be able to cover their content in roughly two printed pages.

**File structure**

- AIPs **must** be written in Markdown.
- AIPs **must** be named using their four-digit number (e.g., `0008.md`).
- AIPs that serve a specific scope **must** be in the subdirectory for that scope.
- AIPs **must** have appropriate front matter:
  - `id`: Required. The ID for the given AIP, as an integer.
  - `state`: Required. The current state in all lower-case (e.g., `draft`, `reviewing`, `approved`).
  - `created`: Required. The ISO-8601 date (`YYYY-MM-DD`) when the AIP was originally drafted.
  - `updated`: The ISO-8601 date when the AIP was last revised.
  - `scope`: The scope for the AIP. Required for AIPs with IDs >= 1000, prohibited otherwise.
  - `permalink`: Required. Set to `/{scope}/{id}` or `/{id}` if no scope.
  - `redirect_from`: A list of permutations readers might enter, including `/{id}` and zero-padded variants (e.g., `/08`, `/008`, `/0008`).

**Document structure**

AIPs **must** begin with a top-level heading with the AIP's title (`# Title`). The title **should** be a noun, not an imperative. For example, "Bad API precedents", not "Avoid breaking API precedent".

AIPs **should** then begin with an introduction (with no additional heading), followed by a `## Guidance` heading. If necessary, the AIP **may** include any of the following after the guidance, in this order:

- `## Further reading` — a bulleted list of links to other AIPs useful to fully understand the current AIP.
- `## Appendices` — further explanation, relatively rare but important when an AIP requires extensive justification (e.g., alternatives considered).
- `## Changelog` — a bulleted list of changes in reverse chronological order.

The guidance section **may** include subsections that elaborate further on details. Subsections will automatically create entries in the table of contents and anchors for citations.

AIPs **should** attempt to follow this overall format, but **may** deviate from it if necessary (in particular, if the AIP would be more difficult to understand, even for a reader already accustomed to reading AIPs in the usual format).

**Important:** Except for the title, AIPs **must** only use the second heading level (`##`) and above. AIPs **should** only use the second and third heading levels (`##`, `###`).

Below is an example AIP shell that uses each major section:

```markdown
# AIP title

The introductory text explains the background and reason why the AIP exists. It lays out the basic question, but does not tell the reader what to do.

## Guidance

The "guidance" section helps the reader know what to do. A common format for the guidance section is a high-level imperative, followed by an example, followed by a bulleted list explaining the example.

### Subsection

Individual subsections can be cited individually, and further elaborate details.

## Rationale

The "rationale" section is optional, and helps the reader understand the motivation behind specific guidance within the AIP.

Deeper explanations of design justification and tradeoffs **must** be in the rationale instead of other sections, to ensure the rest of the document acts as an easily actionable reference.

## History

The "history" section is optional, and documents events and context around a significant edit to an AIP. For example, explanation of a rewrite would be included in this section.

While the changelog is a dotted list of one-line summaries of changes to an AIP, the history section should elaborate on significant events in a descriptive format.

The section **must not** be used to exhaustively enumerate all changes. This is what the changelog provides.

## Further reading

A bulleted list of (usually) other AIPs, in the following format:

- [AIP-1](/1): AIP purpose and guidelines

## Changelog

A bulleted list of changes in reverse chronological order, using the following format:

- **2020-02-18**: Specified ordering.
- **2019-07-01**: Added a subsection clarifying XYZ.
```

**Requirement keywords**

- AIPs **should** use the following requirement level keywords: **must**, **must not**, **should**, **should not**, **may**, which are to be interpreted as described in RFC 2119.
- When using these terms in AIPs, they **must** be lower-case and **bold**.
- These terms **should not** be used in other ways.
- If **should** or **should not** are used, they **must** include valid examples of where other concerns may override the guidance.

**Important:** If a rationale section is used, it exists to provide background and a more complete understanding, but **must not** contain guidance (and RFC-2119 terms **must not** be used in rationale).

**Code examples**

- API design examples in AIPs **should** use Protocol Buffers syntax.
- Examples **should** cover only enough syntax to explain the concept.
- When using RPCs in examples, a `google.api.http` annotation **should** be included.

**Referencing AIPs**

- When AIPs reference other AIPs, the prose **must** use the format `AIP-XXXX` without zero-padding (e.g., `AIP-8`, not `AIP-0008`).
- AIP references **must** link to the relevant AIP.
- AIP links **may** point to a particular section of the AIP if appropriate.
- AIP links **must** use the relative path to the file in the repository; this ensures that the link works both on the AIP site, when viewing the Markdown file, using a local development server, or a branch.

**Rationale**

API guidance, similar to any software, is most beneficial when there is a clear purpose and target beneficiary. The beneficiaries of improved API design are users. These users interact with APIs via a variety of clients, depending on their use case as enumerated above. API guidance must in turn consider the impact broadly across these clients.

### 1.6 Glossary (AIP-9)
[ref: #glossary-aip-9]

In the name of brevity, this section defines common terminology here rather than in each section individually. The following terminology **should** be used consistently throughout this guide.

**API**

Application programming interface. This can be a local interface (such as a client library) or a Network API (defined below).

**API backend**

A set of servers and related infrastructure that implements the business logic for an API service. An individual API backend server is often called an API server.

**API consumer**

The entity that consumes an API service. Typically, this is a project that owns the client application or the server resource.

**API definition**

The definition of an API, usually defined in a Protocol Buffer service. An API definition can be implemented by any number of API services.

**API frontend**

A set of servers plus related infrastructure that provides common functionality across API services, such as load balancing and authentication. An individual API frontend server is often called an API proxy.

**Note:** The API frontend and the API backend may run next to each other or far away from each other. In some cases, they can be compiled into a single application binary and run inside a single process.

**API interface**

The element of an API specification IDL that groups API methods, such as a Protocol Buffers `service` definition. It is typically mapped to a similar high-level grouping mechanism in most programming languages, like a `class` or `interface`.

**API method**

An individual operation within an API. It is typically represented in Protocol Buffers by an `rpc` definition, and is mapped to a function in the API in most programming languages.

**API producer**

The entity that produces an API service.

**API product**

An API service and its related components, such as Terms of Service, documentation, client libraries, and service support, are collectively presented to customers as an API product. For example, Google Calendar API.

**Note:** People sometimes refer to an API product simply as an API.

**API service**

A deployed implementation of one or more APIs, exposed on one or more network addresses. For example, the Cloud Pub/Sub API.

**API service definition**

The combination of API definitions (`.proto` files) and API service configurations (`.yaml` files) used to define an API service. The schema for the API service definition is `google.api.Service`.

**API service endpoint**

Refers to a network address that an API service uses to handle incoming API requests. One API service may have multiple API service endpoints, such as `https://pubsub.googleapis.com` and `https://content-pubsub.googleapis.com`.

**API service name**

Refers to the logical identifier of an API service. APIs use RFC 1035 DNS-compatible names as their API service names, such as `pubsub.googleapis.com`.

**API title**

Refers to the user-facing product title of an API service, such as "Cloud Pub/Sub API".

**API request**

A single invocation of an API method. It is often used as the unit for billing, logging, monitoring, and rate limiting.

**API version**

The version of an API or a group of APIs if they are defined together. An API version is often represented by a string, such as "v1", and is present in API requests and Protocol Buffers package names.

**Client**

Clients are programs that perform specific tasks by calling an API or generic tools, such as CLIs, that expose the API in a user-accessible fashion or operate on resource data at rest.

Examples of clients include the following:

- Command line interfaces
- Libraries, such as an SDK for a particular programming language
- Scripts that operate on a JSON representation of a resource after reading it from an API
- Tools, such as declarative clients
- Visual UIs, such as a web application

**Declarative client**

Declarative clients, also known as Infrastructure as Code (IaC), describe a category of clients that consumes a markup language or code that represents resources exposed by an API, and executes the appropriate imperative actions to drive the resource to that desired state. To determine what changes to make and if a set of updates was successful, a declarative client compares server-side resource attributes with client-defined values. The comparison feature ensures accuracy of a creation or an update, but it requires services to treat the client-set fields as read-only and diligently preserve those values.

Examples of complexities that declarative clients abstract away include:

- Determining the appropriate imperative action (create / update / delete) to achieve desired state.
- Ordering of these imperative actions.

Terraform is an example of such a client.

**User**

A human being who is using an API directly, such as with cURL. This term is defined to differentiate usage in the AIPs between a human *user* and a programmatic *client*.

**Network API**

An API that operates across a network of computers. Network APIs communicate using network protocols including HTTP, and are frequently produced by organizations separate from those that consume them.
