---
subject: "API polish corpus; `AIP-190` naming conventions for interfaces methods messages, `AIP-191` proto file and directory structure with packaging annotations, `AIP-192` public documentation comments deprecations, `AIP-193` standardized `google.rpc.Status` errors with `ErrorInfo`, `AIP-194` automatic retry policy per status code."
index:
  - anchor: naming-conventions-aip-190
    what: "The AIP-190 naming canon: American English spellings, `UpperCamelCase` definitions, intuitive-noun interface identifiers disambiguated with `Api`/`Service` suffix, `VerbNoun` method pattern, preposition-free concise message pattern, no overloading or reserved-word clashes."
    problem: "Interface or message christened hastily ships into generated clients, so renaming becomes breaking change and ambiguous overloaded vocabulary confuses consumers across ecosystem; generated surface permanence, vocabulary drift, ambiguous first-order term, keyword collision in target languages, translation friction, review scrutiny, ecosystem consistency, non-native reader burden."
    use_when: "Coining service, method, or message identifier on new surface; rename contemplated on shipped API (breaking); generic term like `Instance` or `info` shortlisted; candidate clashes with programming-language reserved word; reviewing consistency across sibling APIs."
    avoid_when: "Field-level naming decisions (06_fields › field names); enum value conventions (04_resource_design › enumerations); collection ID rules (04_resource_design › resource names); proto package or filename question (09_polish › file and directory structure)."
    expected: "Identifiers read as intuitive stable nouns and `VerbNoun` verbs, spelling follows American canon, collisions surface before freeze, and consumers navigate surface without glossary."
  - anchor: file-and-directory-structure-aip-191
    what: "The AIP-191 layout rules: `proto3` syntax, single version-suffixed package mirrored to directory, `snake_case` descriptive entry filenames (never version names), canonical component ordering, and packaging annotations (`java_package`, `java_multiple_files`, `csharp_namespace`, `go_package`) set uniformly or not at all."
    problem: "Proto files scattered across mismatched directories with arbitrary ordering, so build tooling resolves imports unpredictably and generated module names collide with language keywords; import resolution far from cause, package-directory drift, bizarre client imports, filename as module name, annotation retrofit breakage, compound namespace word breaks, reviewer friction, missing obvious entrypoint."
    use_when: "Creating or restructuring proto tree for new API; adding packaging options to shipped files (breaking-risk audit); filename becoming generated import identifier assessed; compound package segment like `accessapproval` encountered; component ordering inside file decided."
    avoid_when: "Non-protobuf IDL surface (spirit only, specifics inapplicable); field-level naming (06_fields › field names); interface or method naming (09_polish › naming conventions); `go_package` value ownership (generated-code team decides)."
    expected: "Every file sits in package-matching directory, `proto3` declared, entry file recognizable, components ordered canonically, and language annotations identical across files or absent everywhere."
  - anchor: documentation-aip-192
    what: "The AIP-192 comment contract: public comments on every component, third-person present subject-free opening sentence, brief-but-complete description checklist (units, ranges, defaults, side effects), CommonMark subset without headings tables HTML ASCII art, Markdown reference links, absolute external URLs."
    problem: "Reference documentation generated from sparse or jargon-laden comments, so consumers cannot learn semantics, formatting breaks renderers, and undocumented defaults produce misuse; comment poverty, non-native reader, terse uninformative stub, renderer incompatible markup, omitted measurement semantics, behavior-on-failure silence, idempotency ambiguity, untranslatable slang."
    use_when: "Writing or reviewing proto comments before publish; doc-generation pipeline consumes proto surface; deciding which semantics (measurement, bounds, fallback values) belong in description; linking between components or to external pages; marking non-public notes internal."
    avoid_when: "Styling Markdown files rather than proto comments (markdown-protocol skill); field shape or annotation questions (06_fields › field design); API-agnostic prose style guidance wanted; error text wording (09_polish › errors)."
    expected: "All components carry grammatical subject-free comments, generators render cleanly, deprecations pair option with migration path, and internal notes never leak into published docs."
  - anchor: documentation-aip-192
    what: "The AIP-192 deprecation mechanism: `deprecated = true` option plus comment opening with \"Deprecated: \" first line, alternative solution or explicit reason, and `(--`/`--)` wrapping for internal material."
    problem: "Legacy component must exit surface without breaking consumers overnight, so abrupt removal breaks builds and silent phase-out strands users without migration direction; sunsetting surface element, tooling-blind deprecation, comment-only invisibility, consumer notice period, alternative guidance gap, breaking removal shock, obsolete enum value, grace timeline."
    use_when: "Sunsetting service, method, message, field, or enum member; replacement component ready to recommend; tooling must detect obsolescence programmatically; internal notes mixed with public comments on same element."
    avoid_when: "Greenfield component authoring (sibling card); version-level retirement rather than component-level; internal-only annotation wanted without deprecation."
    expected: "Deprecated elements carry both machine-visible flag and human migration guidance, generated docs flag obsolescence, and removal happens only after notice."
  - anchor: errors-aip-193
    what: "The AIP-193 error envelope: `google.rpc.Status` with canonical `google.rpc.Code`, developer-facing `message` stability rules, mandatory `ErrorInfo` (`domain`, UPPER_SNAKE `reason`, evolving `metadata`), `LocalizedMessage`, `Help` links, partial-error LRO guidance, `PERMISSION_DENIED`-before-`NOT_FOUND` ordering."
    problem: "Service emits ad-hoc failure text or bare numeric codes, so every client hand-rolls parsing, message edits break deployed consumers, and dynamic values stay trapped inside prose; bespoke failure shape, centralized handling blocked, string-parsing fragility, implicit message contract, machine-readable identifier gap, localization afterthought, trust-boundary leak, support ticket flood."
    use_when: "Designing failure responses for any RPC; choosing canonical code for condition; deciding which dynamic values become `metadata`; brownfield message text frozen by compatibility; partial failure in bulk operation contemplated."
    avoid_when: "Retry policy per code (09_polish › automatic retry); authorization check ordering beyond error shape (07_design_patterns › authorization checks); LRO `Operation.error` mechanics (05_operations › long-running operations); validation annotation vocabulary (06_fields › field behavior)."
    expected: "Failures return standard envelope with stable reason-domain pairs, clients branch programmatically without parsing prose, localized text rides details, and links stay absolute and auth-free."
  - anchor: errors-aip-193
    what: "The AIP-193 diagnostic payloads: `ErrorInfo.metadata` map mirroring each templated message element, `Help` links narrowing multi-error pages via `reason`, `BadRequest` field violations, and JSON transcoding shape with HTTP `code` plus enum `status`."
    problem: "On-call engineer stares at production failure with only prose text, so root-cause hunt requires log diving, screenshot ping-pong, and guessing which zone or quota broke; incident triage, troubleshooting context starvation, dynamic value extraction, log correlation cost, multi-cause ambiguity, support escalation loop, opaque quota failure, field-level violation hunt."
    use_when: "Reproducing consumer-reported failure from returned payload; deciding which contextual values accompany new reason; multi-error troubleshooting page needs narrowing; HTTP JSON error shape reviewed for transcoding clients."
    avoid_when: "First-time envelope design (sibling card); retryability decision (09_polish › automatic retry); permission-existence ordering question (07_design_patterns › authorization checks); brownfield message stability ruling (sibling card)."
    expected: "Any returned failure self-describes with machine-readable context, on-call resolves incidents without backend log access, and transcoded clients see equivalent detail."
  - anchor: automatic-retry-configuration-aip-194
    what: "The AIP-194 retry matrix: automatic retry only for unary non-transactional idempotent calls, `UNAVAILABLE` as canonical retryable code, explicit non-retryable lists (`INVALID_ARGUMENT`, `DATA_LOSS`, `CANCELLED`, `DEADLINE_EXCEEDED`), and condition-change codes (`NOT_FOUND`, `ALREADY_EXISTS`, `FAILED_PRECONDITION`) deferred to callers."
    problem: "Client retries blindly after every failure, so duplicate mutations corrupt state, quota storms amplify outages, and unrecoverable conditions loop forever instead of surfacing; duplicate execution risk, retry storm amplification, transactional abort mishandling, billing side effect, infinite futile loop, idempotency precondition, deadline disrespect, backoff absence."
    use_when: "Classifying each status code for retryability; client-side retry policy authored or reviewed; deciding whether method is safe to repeat; transactional boundaries versus per-call retries weighed; streaming RPC scoped out (uncovered)."
    avoid_when: "Failure envelope or payload design (09_polish › errors); making non-idempotent mutation safe (07_design_patterns › request identification); long-running operation failure handling (05_operations › long-running operations); client streaming or bidi methods (outside scope)."
    expected: "Retry logic fires only on transient codes for safe methods, harmful codes surface immediately, transaction aborts escalate to block level, and repeated runs never double-apply."
aips: [190, 191, 192, 193, 194]
---

# Polish

## 9. Polish

### 9.1 Naming Conventions (AIP-190)
[ref: #naming-conventions-aip-190]

This topic describes the naming conventions used in Google APIs. In general, these conventions apply to all Google-managed services.

#### Guidance

In order to provide consistent developer experience across many APIs and over a long period of time, all names used by an API **should** be:

- straightforward
- intuitive
- consistent

This includes names of interfaces, resources, collections, methods, and messages.

Since English is a second language for many developers, one goal of these naming conventions is to make every API name understandable to the majority of developers. It does this by encouraging the use of a simple, consistent, and small vocabulary when naming methods and resources.

**General rules**

- Names used in APIs **should** be in correct American English. For example, `license` (instead of `licence`), `color` (instead of `colour`).
- Commonly accepted short forms or abbreviations of long words **may** be used for brevity. For example, `API` is preferred over `Application Programming Interface`.
- Unless otherwise specified, definitions **must** use `UpperCamelCase` names, as defined by [Google Java Style](https://google.github.io/styleguide/javaguide.html#s5.3-camel-case).
- Use intuitive, familiar terminology where possible. For example, when describing removing (and destroying) a resource, `delete` is preferred over `erase`.
- Use the same name or term for the same concept, including for concepts shared across APIs.
- Avoid name overloading. Use different names for different concepts.
- Avoid overly general names that are ambiguous within the context of the API and the larger ecosystem of Google APIs. They can lead to misunderstanding of API concepts. Rather, choose specific names that accurately describe the API concept. This is particularly important for names that define first-order API elements, such as resources. There is no definitive list of names to avoid, as every name must be evaluated in the context of other names. `Instance`, `info`, and `service` are examples of names that have been problematic in the past. Names chosen should describe the API concept clearly (for example: instance of what?) and distinguish it from other relevant concepts (for example: does "alert" mean the rule, the signal, or the notification?).
- Carefully consider use of names that may conflict with keywords in common programming languages. Such names **may** be used but will likely trigger additional scrutiny during API review. Use them judiciously and sparingly.

**Interface names**

To avoid confusion with Service Names such as `pubsub.googleapis.com`, the term _interface name_ refers to the name used when defining a `service` in a `.proto` file:

```protobuf
// Library is the interface name.
service Library {
  rpc ListBooks(...) returns (...);
  rpc ...
}
```

You can think of the _service name_ as a reference to the actual implementation of a set of APIs, while the _interface name_ refers to the abstract definition of an API.

An interface name **should** use an intuitive noun such as `Calendar` or `BlobStore`. The name **should not** conflict with any well-established concepts in programming languages and their runtime libraries (for example, `File`).

In the rare case where an _interface name_ would conflict with another name within the API, a suffix (for example `Api` or `Service`) **should** be used to disambiguate.

**Method names**

A service **may**, in its IDL specification, define one or more API methods that correspond to methods on collections and resources. The method names **should** follow the naming convention of `VerbNoun` in `UpperCamelCase`, where the noun is typically the resource type.

Standard methods, and their Batch variants, define their naming guidance in the following documents:

| Method | Standard | Batch |
|--------|----------|-------|
| `Get` | [AIP-131](05_operations.md#standard-method-get-aip-131) | [AIP-231](05_operations.md#batch-method-get-aip-231) |
| `List` | [AIP-132](05_operations.md#standard-method-list-aip-132) | N/A |
| `Create` | [AIP-133](05_operations.md#standard-method-create-aip-133) | [AIP-233](05_operations.md#batch-method-create-aip-233) |
| `Update` | [AIP-134](05_operations.md#standard-method-update-aip-134) | [AIP-234](05_operations.md#batch-method-update-aip-234) |
| `Delete` | [AIP-135](05_operations.md#standard-method-delete-aip-135) | [AIP-235](05_operations.md#batch-method-delete-aip-235) |

All other methods are considered Custom Methods and adhere to [AIP-136](05_operations.md#custom-methods-aip-136) naming guidance.

**Message names**

Message names **should** be short and concise. Avoid unnecessary or redundant words. Adjectives can often be omitted if there is no corresponding message without the adjective. For example, the `Shared` in `SharedProxySettings` is unnecessary if there are no _unshared_ proxy settings.

Message names **should not** include prepositions (e.g. "With", "For"). Generally, message names with prepositions are better represented with optional fields on the message.

#### Request and response messages

For request and response message names, see [AIP-136](05_operations.md#custom-methods-aip-136) for custom methods and the appropriate AIP for standard methods.

#### Further reading

- For proto and language package naming, see [AIP-191](09_polish.md#file-and-directory-structure-aip-191).
- For collection ID naming conventions, see [AIP-122](04_resource_design.md#resource-names-aip-122).
- For Enum names, see [AIP-126](04_resource_design.md#enumerations-aip-126).
- For field names, see [AIP-140](06_fields.md#field-names-aip-140).
- For repeated field names, see [AIP-140](06_fields.md#field-names-aip-140).
- For fields representing times and durations, see [AIP-142](06_fields.md#time-and-duration-aip-142).
- For fields representing dates and times of day, see [AIP-142](06_fields.md#time-and-duration-aip-142).
- For fields representing a quantity, see [AIP-141](06_fields.md#quantities-aip-141).
- For the canonical `List` method `filter` field, see [AIP-132](05_operations.md#standard-method-list-aip-132).
- For the canonical `List` response message, see [AIP-132](05_operations.md#standard-method-list-aip-132).
- For well known abbreviations, see [AIP-140](06_fields.md#field-names-aip-140).

> **Agent extension — not part of the AIP standard.** Service names should be intuitive nouns that do not collide with programming-language primitives — disambiguate with an `Api` or `Service` suffix when they would (`BlobStore`, not `String`). Name collisions surface late (in generated clients, not in the proto), so run new interface names past the target languages' keyword lists before freezing them.

### 9.2 File and Directory Structure (AIP-191)
[ref: #file-and-directory-structure-aip-191]

A consistent file and directory structure, while making minimal difference technically, makes API surface definitions easier for users and reviewers to read.

#### Guidance

**Note:** The following guidance applies to APIs defined in protocol buffers, such as those used throughout Google. While the spirit of this guidance applies to APIs defined using other specification languages or formats, some of the particular recommendations might be irrelevant.

**Syntax**

APIs defined in protocol buffers **must** use `proto3` syntax.

**Single package**

APIs defined in protocol buffers **must** define each individual API in a single package, which **must** end in a version component. For example:

```protobuf
syntax = "proto3";

package google.cloud.translation.v3;
```

Google APIs **must** reside in a directory that matches the protocol buffer `package` directive. For example, the package above dictates that the directory be `google/cloud/translation/v3`.

**File names**

It is often useful to divide API definitions into multiple files. File names **must** use `snake_case`.

APIs **should** have an obvious "entry" file, generally named after the API itself. An API with a small number of discrete services (Google Cloud Pub/Sub's `Publisher` and `Subscriber` is a good example) **may** have a separate entry file per service.

APIs with only one file **should** use a filename corresponding to the name of the API.

API `service` definitions and associated RPC request and response `message` definitions **should** be defined in the same file.

Bear in mind that the file names often become module names in client libraries, and customers use them in `import` or `use` statements. Therefore, choosing a descriptive and language keyword-free filename does matter. For example, a file called `import.proto` may be problematic in Python.

**Note:** The version **must not** be used as a filename, because this creates bizarre imports in client libraries. Filenames such as `v3.proto` or `v1beta1.proto` are prohibited.

**File layout**

Individual files **should** place higher level and more important definitions before lower level and less important definitions.

In a proto file, components **should** be in the following order, and each of these **should** be separated by a blank line:

- Copyright and license notice (if applicable).
- The proto `syntax` statement.
- The proto `package` statement.
- Any `import` statements, in alphabetical order.
- Any file-level `option` statements.
- Any `service` definitions.
  - Methods **should** be grouped by the resource they impact, and standard methods **should** precede custom methods.
- Resource `message` definitions. A parent resource **must** be defined before its child resources.
- The RPC request and response `message` definitions, in the same order of the corresponding methods. Each request message **must** precede its corresponding response message (if any).
- Any remaining `message` definitions.
- Any top-level `enum` definitions.

**Packaging annotations**

Protocol buffers ships with annotations to declare the package or namespace (depending on the vocabulary of the target language) of the generated files. For example, setting `go_package` or `csharp_namespace` will override the inferred package name.

When defining APIs, the following rules apply:

- **Java**
  - The `java_package` annotation **must** be set. The correct value is usually the proto package with the appropriate TLD prefixed. Example: `com.google.example.v1`.
  - The `java_multiple_files` annotation **must** be set to `true`.
  - The `java_outer_classname` annotation **must** be set, and **should** be set to the name of the proto filename, in `PascalCase`, with `Proto` appended. Example: `LibraryProto`.
- **Other languages**
  - Package or namespace directives for other languages **must** be set either in every file in the proto package, or none of them. If they are set, the values **must** be identical in every file.
  - If any part of the protobuf package is a compound name (such as `accessapproval`), C#, Ruby and PHP options **must** be specified in order to take account of the word breaks using PascalCase (UpperCamelCase). Example:

    ```protobuf
    option csharp_namespace = "Google.Cloud.AccessApproval.V1";
    option php_namespace = "Google\\Cloud\\AccessApproval\\V1";
    option ruby_package = "Google::Cloud::AccessApproval::V1";
    ```

  - The `go_package` value depends directly on how the Go code is managed i.e. if the module name is based on the VCS provider or using a remote import path, but often has a consistent structure.
    - The module **may** differ based on product area e.g. `google.cloud.accessapproval.v1` would be in module `cloud.google.com/go/accessapproval`.
    - The package import path **should** be derived from the proto package.
    - An API version in the proto package **should** be prefixed with `api` e.g. the proto package segment `v1` becomes `apiv1`.
    - The terminal import path segment **should** be based on the product name found within the proto package and **must** be suffixed with `pb` e.g. `accessapproval` becomes `accessapprovalpb`.
    - This value **should** be left to the team owning the generated code to decide on.

All packaging annotations **should** be specified in alphabetical order of name. Refer to the Protobuf documentation for more about language package options.

**Important:** While languages other than Java have sensible defaults for APIs which don't include compound names, be aware that _adding_ this annotation (with a value not equivalent to the default) constitutes a breaking change in that language. When releasing protos, be sure that omissions are intentional.

#### Rationale

**Java packaging options**

Set the option, `java_multiple_files`, to true to get a cleaner file structure. Doing so instructs `protoc` to create one output file per Protobuf type, which allows for more fine-grained imports. The option, `java_outer_classname`, is required in combination with `java_multiple_files`. It instructs `protoc` to wrap each compiled Protobuf type in a Java class whose name is the value of the option. This prevents potential naming collisions between generated types.

**Go packaging option**

The Go packaging option needs to be decided by the team that owns the generated code, because it is directly tied to the source code management practices of the team. Allowing every proto package to decide on their own Go package creates inconsistencies and friction in management of the code. Within that owning team, having a consistent structure in the Go package naming is critical to a consistent end user experience.

> **Agent extension — not part of the AIP standard.** Keep the proto `package` mirrored to the directory layout (`google.library.v1` ↔ `google/library/v1`), use `snake_case` filenames, and give each API a recognizable entry file named after the API. Build tooling (buf, bazel, the linter) resolves imports predictably only when this mirroring holds — breaking it produces import errors far from the cause.

### 9.3 Documentation (AIP-192)
[ref: #documentation-aip-192]

Documentation is one of the most critical aspects of API design. Users of your API are unable to dig into the implementation to understand the API better; often, the API surface definition and its corresponding documentation will be the only things a user has. Therefore, it is important that documentation be as clear, complete, and unambiguous as possible.

#### Guidance

In APIs defined in protocol buffers, public comments **must** be included over every component (service, method, message, field, enum, and enum value) using the protocol buffers comment format. This is important even in cases where the comment is terse and uninteresting, as numerous tools read these comments and use them.

Services, in particular, **should** have descriptive comments that explain what the service is and what users are able to do with it.

**Note:** Many readers will not be native English speakers. Comments **should** avoid jargon, slang, complex metaphors, pop culture references, or anything else that will not easily translate. Additionally, many readers will have different backgrounds and viewpoints; if writing examples involving people, comments **should** use people who are non-controversial and no longer alive.

#### Style

Comments **should** be in grammatically correct American English. However, the first sentence of each comment **should** omit the subject and be in the third-person present tense:

```protobuf
// Creates a book under the given publisher.
rpc CreateBook(CreateBookRequest) returns (Book) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books"
    body: "book"
  };
}
```

#### Descriptions

Descriptions of messages and fields **should** be brief but complete. Sometimes comments are necessarily perfunctory because there is little to be said; however, before jumping to that conclusion, consider whether some of the following questions are relevant:

- What is it?
- How do you use it?
- What does it do if it succeeds? What does it do if it fails?
- Is it idempotent?
- What are the units? (Examples: meters, degrees, pixels)
- What are the side effects?
- What are common errors that may break it?
  - What is the expected input format?
  - What range of values does it accept? (Examples: `[0.0, 1.0)`, `[1, 10]`)
    - Is the range inclusive or exclusive?
  - For strings, what is the minimum and maximum length, and what characters are allowed?
    - If a value is above the maximum length, do you truncate or send an error?
- Is it always present? (Example: "Container for voting information. Present only when voting information is recorded.")
- Does it have a default setting? (Example: "If `page_size` is omitted, the default is 50.")

#### Formatting

Any formatting in comments **must** be in CommonMark. Headings and tables **must not** be used, as these cause problems for several tools, and are unsuitable for client library reference documentation.

Comments **should** use `code font` for field or method names and for literals (such as `true`).

Raw HTML **must not** be used.

"ASCII art" attempts to present a diagram within the protos **must not** be used. The Markdown within the protos is consumed by a large number of renderers, and any ASCII art is very unlikely to be well-presented by all of them. If a diagram is useful in order to understand the API, include a link to a documentation page containing the diagram as an image.

#### Cross-references

A comment can "link" to another component (service, method, message, field, enum, or enum value) as a Markdown reference link. The reference **must** be one of the following forms:

- The fully-qualified name of the element e.g. `[Book][google.example.v1.Book]`
- A scope-relative reference qualified e.g. `[Sci-Fi genre][Genre.GENRE_SCI_FI]`
- An implied reference e.g. `[Book][]` which equates to `[Book][Book]`

These references are resolved as per name resolution rules.

Containing fields names **must not** be used in references. They will not resolve. The original definition **must** be referenced instead. For example, `[author][Book.author.family_name]` where `author` is a field of `Book`, will not resolve, but `[author][Author.family_name]` will.

#### External links

Comments **may** link to external pages to provide background information beyond what is described in the public comments themselves. External links **must** use absolute (rather than relative) URLs, including the protocol (usually `https`), and **should not** assume the documentation is located on any particular host. For example: `[Spanner Documentation](https://cloud.google.com/spanner/docs)`

#### Trademarked names

When referring to the proper, trademarked names of companies or products in comments, acronyms **should not** be used, unless the acronym is such dominant colloquial use that avoiding it would obscure the reference (example: IBM).

Comments **should** spell and capitalize trademarked names consistent with the trademark owner's current branding.

#### Deprecations

To deprecate a component (service, method, message, field, enum, or enum value), the `deprecated` option **must** be set to `true`, and the first line of the respective comment **must** start with `"Deprecated: "` and provide alternative solutions for developers. If there is no alternative solution, a deprecation reason **must** be given.

#### Internal content

Comments **may** be explicitly marked as internal by wrapping internal content in `(--` and `--)`.

Non-public links, internal implementation notes (such as `TODO` and `FIXME` directives), and other such material **must** be marked as internal.

**Note:** Comments **should** use only leading comments (not trailing comments or detached comments). In particular, comments **must not** use both a leading and trailing comment to describe any component, because this is a common source of inadvertent omissions of the internal content annotation.

> **Agent extension — not part of the AIP standard.** Deprecation is a two-part act: set `deprecated = true` AND start the comment with `Deprecated:` plus a concrete migration path — the option without the comment leaves users guessing, the comment without the option leaves tooling blind. Keep proto comments free of Markdown tables and raw HTML; doc generators across languages render only a conservative subset reliably.

### 9.4 Errors (AIP-193)
[ref: #errors-aip-193]

Effective error communication is an important part of designing simple and intuitive APIs. Services returning standardized error responses enable API clients to construct centralized common error handling logic. This common logic simplifies API client applications and eliminates the need for cumbersome custom error handling code.

#### Guidance

Services **must** return a `google.rpc.Status` message when an API error occurs, and **must** use the canonical error codes defined in `google.rpc.Code`. More information about the particular codes is available in the gRPC status code documentation.

Error messages **should** help a reasonably technical user _understand_ and _resolve_ the issue, and **should not** assume that the user is an expert in your particular API. Additionally, error messages **must not** assume that the user will know anything about its underlying implementation.

Error messages **should** be brief but actionable. Any extra information **should** be provided in the `details` field. If even more information is necessary, you **should** provide a link where a reader can get more information or ask questions to help resolve the issue. It is also important to set the right tone when writing messages.

The following sections describe the fields of `google.rpc.Status`.

#### Status.message

The `message` field is a developer-facing, human-readable "debug message" which **should** be in English. (Localized messages are expressed using a `LocalizedMessage` within the `details` field. See `LocalizedMessage` for more details.) Any dynamic aspects of the message **must** be included as metadata within the `ErrorInfo` that appears in `details`.

The message is considered a problem description. It is intended for developers to understand the problem and is more detailed than `ErrorInfo.reason`, discussed later.

Messages **should** use simple descriptive language that is easy to understand (without technical jargon) to clearly state the problem that results in an error, and offer an actionable resolution to it.

For pre-existing (brownfield) APIs which have previously returned errors without machine-readable identifiers, the value of `message` **must** remain the same for any given error. For more information, see [Changing error messages](#changing-error-messages).

#### Status.code

The `code` field is the status code, which **must** be the numeric value of one of the elements of the `google.rpc.Code` enum.

For example, the value `5` is the numeric value of the `NOT_FOUND` enum element.

#### Status.details

The `details` field allows messages with additional error information to be included in the error response, each packed in a `google.protobuf.Any` message.

Google defines a set of standard detail payloads for error details, which cover most common needs for API errors. Services **should** use these standard detail payloads when feasible.

Each type of detail payload **must** be included at most once. For example, there **must not** be more than one `BadRequest` message in the `details`, but there **may** be a `BadRequest` and a `PreconditionFailure`.

All error responses **must** include an `ErrorInfo` within `details`. This provides machine-readable identifiers so that users can write code against specific aspects of the error.

The following sections describe the most common standard detail payloads.

#### ErrorInfo

The `ErrorInfo` message is the primary way to send a machine-readable identifier. Contextual information **should** be included in `metadata` in `ErrorInfo` and **must** be included if it appears within an error message.

The `reason` field is a short UPPER_SNAKE_CASE description of the cause of the error. Error reasons are unique within a particular domain of errors. The reason **must** be at most 63 characters and match a regular expression of `[A-Z][A-Z0-9_]+[A-Z0-9]`. (This is UPPER_SNAKE_CASE, without leading or trailing underscores, and without leading digits.)

The reason **should** be terse, but meaningful enough for a human reader to understand what the reason refers to.

Good examples:

- `CPU_AVAILABILITY`
- `NO_STOCK`
- `CHECKED_OUT`
- `AVAILABILITY_ERROR`

Bad examples:

- `THE_BOOK_YOU_WANT_IS_NOT_AVAILABLE` (overly verbose)
- `ERROR` (too general)

The `domain` field is the logical grouping to which the `reason` belongs. The domain **must** be a globally unique value, and is typically the name of the service that generated the error, e.g. `pubsub.googleapis.com`.

The (reason, domain) pair form a machine-readable way of identifying a particular error. Services **must** use the same (reason, domain) pair for the same error, and **must not** use the same (reason, domain) pair for logically different errors. The decision about whether two errors are "the same" or not is not always clear, but **should** generally be considered in terms of the expected action a client might take to resolve them.

The `metadata` field is a map of key/value pairs providing additional dynamic information as context. Each key within `metadata` **must** be at most 64 characters long, and conform to the regular expression `[a-z][a-zA-Z0-9-_]+`.

Any request-specific information which contributes to the `Status.message` or `LocalizedMessage.message` messages **must** be represented within `metadata`. This practice is critical so that machine actors do not need to parse error messages to extract information.

For example consider the following message:

> An <e2-medium> VM instance with <local-ssd=3,nvidia-t4=2> is currently unavailable in the <us-east1-a> zone. Consider trying your request in the <us-central1-f,us-central1-c> zone(s), which currently has/have capacity to accommodate your request. Alternatively, you can try your request again with a different VM hardware configuration or at a later time. For more information, see the troubleshooting documentation.

The `ErrorInfo.metadata` map for the same error could be:

- `"zone": "us-east1-a"`
- `"vmType": "e2-medium"`
- `"attachment": "local-ssd=3,nvidia-t4=2"`
- `"zonesWithCapacity": "us-central1-f,us-central1-c"`

Additional contextual information that does not appear in an error message **may** also be included in `metadata` to allow programmatic use by the client.

The metadata included for any given (reason, domain) pair can evolve over time:

- New keys **may** be included.
- All keys that have been included **must** continue to be included (but may have empty values).

In other words, once a user has observed a given key for a (reason, domain) pair, the service **must** allow them to rely on it continuing to be present in the future.

The set of keys provided in each (reason, domain) pair is independent from other pairs, but services **should** aim for consistent key naming. For example, two error reasons within the same domain should not use metadata keys of `vmType` and `virtualMachineType`.

#### LocalizedMessage

`google.rpc.LocalizedMessage` is used to provide an error message which **should** be localized to a user-specified locale where possible.

If the `Status.message` field has a sub-optimal value which cannot be changed due to the constraints in the [Changing error messages](#changing-error-messages) section, `LocalizedMessage` **may** be used to provide a better error message even when no user-specified locale is available.

Regardless of how the locale for the message was determined, both the `locale` and `message` fields **must** be populated.

The `locale` field specifies the locale of the message, following IETF BCP-47 (Tags for Identifying Languages). Example values: `"en-US"`, `"fr-CH"`, `"es-MX"`.

The `message` field contains the localized text itself. This **should** include a brief description of the error and a call to action to resolve the error. The message **should** include contextual information to make the message as specific as possible. Any contextual information in the message **must** be included in `ErrorInfo.metadata`. See `ErrorInfo` for more details of how contextual information may be included in a message and the corresponding metadata.

The `LocalizedMessage` payload **should** contain the complete resolution to the error. If more information is needed than can reasonably fit in this payload, then additional resolution information **must** be provided in a `Help` payload. See the [Help](#help) section for guidance.

#### Help

When other textual error messages (in `Status.message` or `LocalizedMessage.message`) don't provide the user sufficient context or actionable next steps, or if there are multiple points of failure that need to be considered in troubleshooting, a link to supplemental troubleshooting documentation **must** be provided in the `Help` payload.

Provide this information in addition to a clear problem definition and actionable resolution, not as an alternative to them. The linked documentation **must** clearly relate to the error. If a single page contains information about multiple errors, the `ErrorInfo.reason` value **must** be used to narrow down the relevant information.

The `description` field is a textual description of the linked information. This **must** be suitable to display to a user as text for a hyperlink. This **must** be plain text (not HTML, Markdown etc).

Example `description` value: `"Troubleshooting documentation for STOCKOUT errors"`

The `url` field is the URL to link to. This **must** be an absolute URL, including scheme.

Example `url` value: `"https://cloud.google.com/compute/docs/resource-error"`

For publicly-documented services, even those with access controls on actual usage, the linked content **must** be accessible without authentication.

For privately-documented services, the linked content **may** require authentication.

#### Error messages

Textual error messages can be present in both `Status.message` and `LocalizedMessage.message` fields. Messages **should** be succinct but actionable, with request-specific information (such as a resource name or region) providing precise details where appropriate. Any request-specific details **must** be present in `ErrorInfo.metadata`.

#### Changing error messages

Changing the content of `Status.message` over time must be done carefully, to avoid breaking clients who have previously had to rely on the message for all information. See the [Rationale](#rationale) section for more details.

For a given RPC:

- If the RPC has _always_ returned `ErrorInfo` with machine-readable information, the content of `Status.message` **may** change over time. (For example, the API producer may provide a clearer explanation, or more request-specific information.)
- Otherwise, the content of `Status.message` **must** be stable, providing the same text with the same request-specific information. Instead of changing `Status.message`, the API **should** include a `LocalizedMessage` within `Status.details`.

Even if an RPC has always returned `ErrorInfo`, the API **may** keep the existing `Status.message` stable and add a `LocalizedMessage` within `Status.details`.

The content of `LocalizedMessage.message` **may** change over time.

#### Partial errors

APIs **should not** support partial errors. Partial errors add significant complexity for users, because they usually sidestep the use of error codes, or move those error codes into the response message, where the user **must** write specialized error handling logic to address the problem.

However, occasionally partial errors are necessary, particularly in bulk operations where it would be hostile to users to fail an entire large request because of a problem with a single entry.

Methods that require partial errors **should** use long-running operations, and the method **should** put partial failure information in the metadata message. The errors themselves **must** still be represented with a `google.rpc.Status` object.

#### Permission Denied

If the user does not have permission to access the resource or parent, regardless of whether or not it exists, the service **must** error with `PERMISSION_DENIED` (HTTP 403). Permission **must** be checked prior to checking if the resource or parent exists.

If the user does have proper permission, but the requested resource or parent does not exist, the service **must** error with `NOT_FOUND` (HTTP 404).

#### HTTP/1.1+JSON representation

When clients use HTTP/1.1 as per [AIP-127](10_protocol_buffers.md#http-and-grpc-transcoding-aip-127), the error information is returned in the body of the response, as a JSON object. For backward compatibility reasons, this does not map precisely to `google.rpc.Status`, but contains the same core information. The schema is defined in the following proto:

```protobuf
message Error {
  message Status {
    // The HTTP status code that corresponds to `google.rpc.Status.code`.
    int32 code = 1;
    // This corresponds to `google.rpc.Status.message`.
    string message = 2;
    // This is the enum version for `google.rpc.Status.code`.
    google.rpc.Code status = 4;
    // This corresponds to `google.rpc.Status.details`.
    repeated google.protobuf.Any details = 5;
  }

  Status error = 1;
}
```

The most important difference is that the `code` field in the JSON is an HTTP status code, _not_ the direct value of `google.rpc.Status.code`. For example, a `google.rpc.Status` message with a `code` value of 5 would be mapped to an object including the following code-related fields (as well as the message, details etc):

```json
{
  "error": {
    "code": 404,          // The HTTP status code for "not found"
    "status": "NOT_FOUND" // The name in google.rpc.Code for value 5
  }
}
```

The following JSON shows a fully populated HTTP/1.1+JSON representation of an error response.

```json
{
  "error": {
    "code": 429,
    "message": "The zone 'us-east1-a' does not have enough resources available to fulfill the request. Try a different zone, or try again later.",
    "status": "RESOURCE_EXHAUSTED",
    "details": [
      {
        "@type": "type.googleapis.com/google.rpc.ErrorInfo",
        "reason": "RESOURCE_AVAILABILITY",
        "domain": "compute.googleapis.com",
        "metadata": {
          "zone": "us-east1-a",
          "vmType": "e2-medium",
          "attachment": "local-ssd=3,nvidia-t4=2",
          "zonesWithCapacity": "us-central1-f,us-central1-c"
        }
      },
      {
        "@type": "type.googleapis.com/google.rpc.LocalizedMessage",
        "locale": "en-US",
        "message": "An <e2-medium> VM instance with <local-ssd=3,nvidia-t4=2> is currently unavailable in the <us-east1-a> zone. Consider trying your request in the <us-central1-f,us-central1-c> zone(s), which currently has/have capacity to accommodate your request. Alternatively, you can try your request again with a different VM hardware configuration or at a later time. For more information, see the troubleshooting documentation."
      },
      {
        "@type": "type.googleapis.com/google.rpc.Help",
        "links": [
          {
            "description": "Additional information on this error",
            "url": "https://cloud.google.com/compute/docs/resource-error"
          }
        ]
      }
    ]
  }
}
```

#### Rationale

**Requiring ErrorInfo**

`ErrorInfo` is required because it further identifies an error. With only approximately twenty available values for `Status.status`, it is difficult to disambiguate one error from another across an entire API Service.

Also, error messages often contain dynamic segments that express variable information, so there needs to be machine-readable component of _every_ error response that enables clients to use such information programmatically.

**Including LocalizedMessage**

`LocalizedMessage` was selected as the location to present alternate error messages. While `LocalizedMessage` **may** use a locale specified in the request, a service **may** provide a `LocalizedMessage` even without a user-specified locale, typically to provide a better error message in situations where `Status.message` cannot be changed. Where the locale is not specified by the user, it **should** be `en-US` (US English).

A service **may** include `LocalizedMessage` even when the same message is provided in `Status.message` and when localization into a user-specified locale is not supported. Reasons for this include:

- An intention to support user-specified localization in the near future, allowing clients to consistently use `LocalizedMessage` and not change their error-reporting code when the functionality is introduced.
- Consistency across all RPCs within a service: if some RPCs include `LocalizedMessage` and some only use `Status.message` for error messages, clients have to be aware of which RPCs will do what, or implement a fall-back mechanism. Providing `LocalizedMessage` on all RPCs allows simple and consistent client code to be written.

**Updating Status.message**

If a client has ever observed an error with `Status.message` populated (which it always will be) but without `ErrorInfo`, the developer of that client may well have had to resort to parsing `Status.message` in order to find out information beyond just what `Status.code` conveys. That information may be found by matching specific text (e.g. "Connection closed with unknown cause") or by parsing the message to find out metadata values (e.g. a region with insufficient resources). At that point, `Status.message` is implicitly part of the API contract, so **must not** be updated — that would be a breaking change. This is one reason for introducing `LocalizedMessage` into the `Status.details`.

RPCs which have **always** included `ErrorInfo` are in a better position: the contract is then more about the stability of `ErrorInfo` for any given error. The reason and domain need to be consistent over time, and the metadata provided for any given (reason, domain) can only be expanded. It's still possible that clients could be parsing `Status.message` instead of using `ErrorInfo`, but they will always have had a more robust option available to them.

#### Further reading

- For which error codes to retry, see [AIP-194](09_polish.md#automatic-retry-configuration-aip-194).
- For how to retry errors in client libraries, see AIP-4221.

> **Agent extension — not part of the AIP standard.** `google.rpc.ErrorInfo` is the machine-readable contract (stable `domain`/`reason`) that lets clients branch without parsing human-readable messages; pair it with `BadRequest` for field-level validation and `LocalizedMessage` for display text. Two recurring gaps: LRO failures must surface through `Operation.error` in the same Status shape, and error messages must never embed stack traces or internal identifiers — they cross a trust boundary.

### 9.5 Automatic Retry Configuration (AIP-194)
[ref: #automatic-retry-configuration-aip-194]

RPCs sometimes fail. When one does, the client performing the RPC needs to know whether it is safe to retry the operation. When status codes are used consistently across multiple APIs, clients can respond to failures appropriately.

#### Guidance

Clients **should** automatically retry requests for which repeated runs would not cause unintended state changes, which are non-transactional, and which are unary.

Clients **should not** automatically retry transactional requests; instead these requests **should** have application-level retry logic that retries the entire transaction block from the start.

Clients **should not** automatically retry requests in which repeated runs would cause unintended state changes.

**Note:** This AIP does not cover client streaming or bi-directional streaming.

**Note:** For client side retry behavior in the client libraries, see AIP-4221.

#### Retryable codes

For methods listed as retryable above, clients **should** retry the following error codes:

- `UNAVAILABLE`: This code generally results from network hiccups, and is generally transient. It is retryable under the expectation that the connection will become available (soon).

#### Non-retryable codes

The following codes **should not** be automatically retried for any request:

- `OK`: The request succeeded.
- `CANCELLED`: An application can cancel a request, which **must** be honored.
- `DEADLINE_EXCEEDED`: An application can set a deadline, which **must** be honored.
- `INVALID_ARGUMENT`: Retrying a request with an invalid argument will never succeed.
- `DATA_LOSS`: This is an unrecoverable error and **must** immediately be surfaced to the application.

#### Generally non-retryable codes

The following codes generally **should not** be automatically retried for any request:

- `RESOURCE_EXHAUSTED`: This code may be a signal that quota is exhausted. Retries therefore may not be expected to work for several hours; meanwhile the retries may have billing implications. If `RESOURCE_EXHAUSTED` is used for other reasons than quota and the expected time for the resource to become available is much shorter, it may be retryable.
- `INTERNAL`: This code generally means that some internal part of the system has failed, and usually means a bug should be filed against the system. These **should** immediately be surfaced to the application.
- `UNKNOWN`: Unlike `INTERNAL`, this code is reserved for truly unknown-to-the-system errors, and therefore may not be safe to retry. These **should** immediately be surfaced to the application.
- `ABORTED`: This code typically means that the request failed due to a sequencer check failure or transaction abort. These **should not** be retried for an individual request; they **should** be retried at a level higher (the entire transaction, for example).

Some codes **may** be automatically retried if a system is designed without synchronization or signaling between various components. For example, client might retry `NOT_FOUND` on a read operation, which is designed to hang forever until the resource is created. However, these types of systems are generally discouraged.

Therefore, the following codes **should not** be automatically retried for any request:

- `NOT_FOUND`: A client **should not** retry until a resource is created.
- `ALREADY_EXISTS`: A client **should not** retry until a resource is deleted.
- `PERMISSION_DENIED`: A client **should not** retry until it has permission.
- `UNAUTHORIZED`: A client **should not** retry until it is authorized.
- `UNAUTHENTICATED`: A client **should not** retry until it is authenticated.
- `FAILED_PRECONDITION`: A client **should not** retry until system state changes.
- `OUT_OF_RANGE`: A client **should not** retry until the range is extended.
- `UNIMPLEMENTED`: A client **should not** retry until the RPC is implemented.

#### Further reading

- For parallel or retried request disambiguation, see [AIP-154](07_design_patterns.md#resource-freshness-validation-aip-154).

> **Agent extension — not part of the AIP standard.** Automatic retry is safe only for unary, non-transactional, idempotent calls with exponential backoff and jitter; `INVALID_ARGUMENT` and `DATA_LOSS` must never be retried — the first can never succeed, the second must not be repeated. Where idempotency is not natural, make it true with AIP-155 request IDs rather than narrowing the retry policy to "never".
