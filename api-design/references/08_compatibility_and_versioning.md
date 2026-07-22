---
subject: "Compatibility and versioning corpus; `AIP-180` breaking-change taxonomy with source/wire/semantic tiers, `AIP-181` alpha/beta/stable stability levels and deprecation clocks, `AIP-182` external dependency end-of-life and LTS policy, `AIP-185` major-version encoding via channel-based, release-based, visibility-based strategies."
index:
  - anchor: backwards-compatibility-aip-180
    what: "The AIP-180 breaking-change rulebook: source, wire, and semantic compatibility tiers with add-don't-remove discipline — no new required fields, frozen defaults, stable serialization, components never renamed, moved, retyped, or shifted across `oneof` boundaries."
    problem: "Existing client code compiles and runs against deployed contract, so renaming field, flipping default, or retyping message detonates production integrations and hotfix rollbacks consume release window; breaking rename cost, compiled stub drift, default value freeze, serialization presence semantics, resource name permanence, oneof migration trap, enum growth surprise, judgment-call gray zone."
    use_when: "Change to shipped surface under review (field, enum entry, default, serialization, file layout); pagination retrofit contemplated on previously unpaginated method; gray-zone behavior shift judged for reasonable-consumer impact; deciding whether edit forces version bump."
    avoid_when: "Greenfield surface without shipped clients (change freely); component carries pre-stable stability label (08_compatibility_and_versioning › stability levels); choosing version encodings or channels (08_compatibility_and_versioning › API versioning); upstream engine lifecycle question (08_compatibility_and_versioning › external dependencies)."
    expected: "Old clients keep compiling and running against newer servers, defaults and serialization stay frozen, and questionable edits route into deprecation track or next-major planning instead."
  - anchor: backwards-compatibility-aip-180
    what: "The AIP-180 additive-evolution rules: new components permitted in-place provided defaults preserve prior behavior, request-only enums grow freely while response enums document expected growth, and generated-code name conflicts avoided."
    problem: "Planned feature extends live surface mid-version, so careless addition quietly alters behavior of untouched clients and retrofit pagination truncates results users assume complete; stealth semantic shift, additive surprise, latent truncation, generated symbol collision, enum expansion governance, default-preserving introduction, same-name sibling clash, unaware old consumer."
    use_when: "Adding field, method, message, or enum entry to in-use interface; pagination introduced after launch; enum in response or resource expected to grow; closely-named sibling component planned (e.g. `foo_value` beside `foo`)."
    avoid_when: "Removing or renaming anything (sibling card); pure bug fix restoring documented contract; stability label explicitly permits breakage (08_compatibility_and_versioning › stability levels)."
    expected: "Additions land in-place without disturbing existing callers, defaults match pre-change behavior, growing enums carry documented expansion policy, and client stubs compile clean for old and new consumers alike."
  - anchor: stability-levels-aip-181
    what: "The AIP-181 stability vocabulary: `alpha` with curated users and expected breakage, `beta` public with minimal changes behind defined deprecation period plus ~90-day timebox to promotion, `stable` banning breaking changes within major version under formal turndown process, isolated and emergency exceptions included."
    problem: "Surface ships without declared change budget, so consumers assume permanence, producers assume freedom, and first breaking edit becomes trust-destroying incident without notice channel or migration window; unlabeled maturity signal, change-budget ambiguity, user tolerance mismatch, surprise breakage incident, missing migration runway, promotion timing question, curated tester cohort, governance escalation gravity."
    use_when: "Label chosen for new or graduating surface; breaking change weighed against label promises; deprecation window and timebox defined at marking; emergency or isolated-change exception contemplated; promotion criteria set."
    avoid_when: "Classifying whether specific edit breaks compatibility (08_compatibility_and_versioning › backwards compatibility); version string encoding or channel mechanics (08_compatibility_and_versioning › API versioning); third-party engine lifecycle policy (08_compatibility_and_versioning › external dependencies)."
    expected: "Components carry explicit maturity labels, pre-GA breakage arrives with notice and transition window, and stable surfaces get version bumps or formal governance sign-off instead of silent edits."
  - anchor: external-software-dependencies-aip-182
    what: "The AIP-182 external-dependency lifecycle rules: resources creatable on any currently-supported LTS version with non-LTS optional, end-of-life versions phased out of creation under mandatory user notification, already-provisioned resources preserved, continued support meaning assumed patching duty."
    problem: "Managed service exposes database engine, OS image, or language runtime whose upstream release calendar marches toward end-of-life, so exposed versions rot into liability and forced removals blindside tenants mid-workload; vendor release lifecycle, rotting exposed version, tenant blindsiding, support burden transfer, lts selection duty, security patch ownership, legacy adoption anchor, creation-phase removal notice."
    use_when: "API lets users spin resources on third-party engines, images, or runtimes; version catalog curated by service; end-of-life phase-out policy and notification flow drafted; official support weighed for version past upstream EOL."
    avoid_when: "Service's own contract compatibility question (08_compatibility_and_versioning › backwards compatibility); maturity labeling of own components (08_compatibility_and_versioning › stability levels); dependency hidden from users (internal implementation detail)."
    expected: "Users provision on every actively maintained LTS release, EOL versions exit creation flows only after notification, already-running instances stay untouched absent critical security need, and officially continued versions come with owned patching."
  - anchor: api-versioning-aip-185
    what: "The AIP-185 versioning model: single major identifier (`v1`, never `v1.1`) at proto-package tail and URI start, in-place minor and patch evolution, parallel coexistence of majors with deprecation, plus channel-based (`v1beta`), release-based (`v1beta1`), and visibility-label strategies for pre-GA surfaces."
    problem: "Incompatible overhaul looms over live integrations, so absent coexistence plan big-bang cutover strands users and premature stability suffixes hardcode churn into every import path; forced flag day, coexistence gap, version string sprawl, minor number leakage, pre-ga suffix choice, channel superset rule, gradual migration window, acl-gated preview."
    use_when: "Pre-GA strategy chosen among channel, release, visibility; version placement in package and path decided; breaking overhaul needs parallel-run and turndown plan; preview feature gating via labels contemplated."
    avoid_when: "Judging whether specific edit is breaking (08_compatibility_and_versioning › backwards compatibility); choosing maturity promises per label (08_compatibility_and_versioning › stability levels); third-party version exposure (08_compatibility_and_versioning › external dependencies)."
    expected: "Major version encoded once at end of proto package and head of URI path, pre-GA surfaces carry stability suffixes per chosen strategy, old and new majors run side by side until deprecation completes, and deprecated functionality never graduates."
aips: [180, 181, 182, 185]
---

# Compatibility and Versioning

## 8. Compatibility and Versioning

### 8.1 Backwards Compatibility (AIP-180)
[ref: #backwards-compatibility-aip-180]

APIs are fundamentally contracts with users, and users often write code against APIs that is then launched into a production service with the expectation that it continues to work (unless the API has a stability level that indicates otherwise). Therefore, it is important to understand what constitutes a backwards compatible change and what constitutes a backwards incompatible change.

#### Guidance

Existing client code **must not** be broken by a service updating to a new minor or patch release. Old clients **must** be able to work against newer servers (with the same major version number).

**Important:** It is not always clear whether a change is compatible or not. The guidance here **should** be treated as indicative, rather than as a comprehensive list of every possible change.

There are three distinct types of compatibility to consider:

1. **Source compatibility:** Code written against a previous version **must** compile against a newer version, and successfully run with a newer version of the client library.
2. **Wire compatibility:** Code written against a previous version **must** be able to communicate correctly with a newer server. In other words, not only are inputs and outputs compatible, but the serialization and deserialization expectations continue to match.
3. **Semantic compatibility:** Code written against a previous version **must** continue to receive what most reasonable developers would expect. (This can be tricky in practice, however, and sometimes determining what users will expect can involve a judgment call.)

**Note:** In general, the specific guidance here assumes use of protocol buffers and JSON as transport formats. Other transport formats may have slightly different rules.

**Note:** This guidance assumes that APIs are intended to be called from a range of consumers, written in multiple languages and with no control over how and when consumers update. Any API which has a more limited scope (for example, an API which is only called by client code written by the same team as the API producer, or deployed in a way which can enforce updates) should carefully consider its own compatibility requirements.

#### Adding components

In general, new components (interfaces, methods, messages, fields, enums, or enum values) **may** be added to existing APIs in the same major version.

However, keep the following guidelines in mind when doing this:

- Code written against the previous surface (and thus is unaware of the new components) **must** continue to be treated the same way as before.
  - New required fields **must not** be added to existing request messages or resources.
  - Any field being populated by clients **must** have a default behavior matching the behavior before the field was introduced.
    - This can be tricky to do in some cases. For example, adding pagination after the fact where previously all items were returned (i.e. `page_size` is infinite, which is not advised). If the default for the new `page_size` field is *less* than what was previously returned, older clients will incorrectly assume all results were returned.
  - Any field previously populated by the server **must** continue to be populated, even if it introduces redundancy.
- For enum values specifically, be aware that it is possible that user code does not handle new values gracefully.
  - Enum values **may** be freely added to enums which are only used in request messages.
  - Enums that are used in response messages or resources and which are expected to receive new values **should** document this. Enum values still **may** be added in this situation; however, appropriate caution **should** be used.

**Note:** It is possible when adding a component closely related to an existing component (for example, `string foo_value` when `string foo` already exists) to enter a situation where generated code will conflict. Service owners **should** be aware of subtleties in the tooling they or their users are likely to use (and tool authors **should** endeavor to avoid such subtleties if possible).

#### Removing or renaming components

Existing components (interfaces, methods, messages, fields, enums, or enum values) **must not** be removed from existing APIs in the same major version. Removing a component is a backwards incompatible change.

**Important:** Renaming a component is semantically equivalent to "remove and add". In cases where these sorts of changes are desirable, a service **may** add the new component, but **must not** remove the existing one. In situations where this can allow users to specify conflicting values for the same semantic idea, the behavior **must** be clearly specified.

#### Moving components between files

Existing components **must not** be moved between files.

Moving a component from one proto file to another within the same package is wire compatible, however, the code generated for languages like C++ or Python will result in breaking change since `import` and `#include` will no longer point to the correct code location.

#### Moving into oneofs

Existing fields **must not** be moved into or out of a `oneof`. This is a backwards-incompatible change in the Go protobuf stubs.

#### Changing the type of fields

Existing fields and messages **must not** have their type changed, even if the new type is wire-compatible, because type changes alter generated code in a breaking way.

#### Changing string length

APIs **should** avoid increasing the upper bound for the size or limit (if accepted as input) of `string` fields. APIs **should** treat expected size upper bound increases as incompatible changes (see [Changing resource names](#changing-resource-names) as an example). APIs **may** pad out values with filler characters if reserving a consistent size is necessary, but this **must** be documented if done.

#### Changing resource names

A resource **must not** change its name.

Unlike most breaking changes, this affects major versions as well: in order for a client to expect to use v2.0 access a resource that was created in v1.0 or vice versa, the same resource name **must** be used in both versions.

More subtly, the set of valid resource names **should not** change either, for the following reasons:

- If resource name formats become more restrictive, a request that would previously have succeeded will now fail.
- If resource name formats become less restrictive than previously documented, then code making assumptions based on the previous documentation could break. Users are very likely to store resource names elsewhere, in ways that may be sensitive to the set of permitted characters and the length of the name. Alternatively, users might perform their own resource name validation to follow the documentation.
  - For example, Amazon gave customers a lot of warning and had a migration period when they started allowing longer EC2 resource IDs.

#### Semantic changes

Code will often depend on API behavior and semantics, *even when such behavior is not explicitly supported or documented*. Therefore, APIs **must not** change visible behavior or semantics in ways that are likely to break reasonable user code, as such changes will be seen as breaking by those users.

**Note:** This does involve some level of judgment; it is not always clear whether a proposed change is likely to break users, and an expansive reading of this guidance could ostensibly prevent *any* change (which is not the intent).

##### Changing value format or construction

APIs **must not** change the expected format or algorithm used to construct the value of an existing field — even if the field is `OUTPUT_ONLY` and populated by the API service — within an API version. Doing so requires a new API version.

For example, changing the format of a field `ip_address` conforming to IPv4 format to instead contain IPv6 values is a breaking change.

##### Default values must not change

Default values are the values set by servers for resources when they are not specified by the client. This section only applies to static default values within fields on resources and does not apply to dynamic defaults such as the default IP address of a resource.

Changing the default value is considered breaking and **must not** be done. The default behavior for a resource is determined by its default values, and this **must not** change across minor versions.

For example:

```protobuf
message Book {
  // google.api.resource and other annotations and fields

  // The genre of the book.
  // If this is not set when the book is created, the field will be given
  // a value of FICTION.
  enum Genre {
    GENRE_UNSPECIFIED = 0;
    FICTION = 1;
    NONFICTION = 2;
  }

  Genre genre = 1;
}
```

Changing to:

```protobuf
message Book {
  // google.api.resource and other annotations and fields

  // The genre of the book.
  // If this is not set when the book is created, the field will be given
  // a value of NONFICTION.
  enum Genre {
    GENRE_UNSPECIFIED = 0;
    FICTION = 1;
    NONFICTION = 2;
  }

  Genre genre = 1;
}
```

would constitute a breaking change.

##### Serializing defaults

APIs **must not** change the way a field with a default value is serialized. For example if a field does not appear in the response if the value is equal to the default, the serialization **must not** change to include the field with the default. Clients may depend on the presence or absence of a field in a resource as semantically meaningful, so a change to how serialization is done for absent values **must not** occur in a minor version.

Consider the following proto, where the default value of `wheels` is `2`:

```protobuf
// A representation of an automobile.
message Automobile {
  // google.api.resource and other annotations and fields

  // The number of wheels on the automobile.
  // The default value is 2, when no value is sent by the client.
  int32 wheels = 2;
}
```

First the proto serializes to JSON when the value of `wheels` is `2` as follows:

```json
{
  "name": "my-car"
}
```

Then, the API service changes the serialization to include `wheels` even if the value is equal to the default value, `2`, as follows:

```json
{
  "name": "my-car",
  "wheels": 2
}
```

This constitutes a change that is not backwards compatible within a major version.

#### Further reading

- For compatibility around field behavior, see [AIP-203](06_fields.md#field-behavior-documentation-aip-203).
- For compatibility around pagination, see [AIP-158](07_design_patterns.md#pagination-aip-158).
- For compatibility around long-running operations, see [AIP-151](05_operations.md#long-running-operations-aip-151).
- For understanding stability levels and expectations, see [AIP-181](#stability-levels-aip-181).
- For compatibility with client library resource name parsing, see [AIP-4231](10_protocol_buffers.md#common-components-aip-213).
- For compatibility with client library method signatures, see [AIP-4232](10_protocol_buffers.md#common-components-aip-213).
- For compatibility around field presence changes, see [AIP-149](06_fields.md#unset-field-values-aip-149).
- For compatibility around resource types, see [AIP-123](04_resource_design.md#resource-types-aip-123).

#### Rationale

##### Risk of string length changes

End users may store resource properties, like the `name`, in a dedicated database column with a limited length. If the service starts returning values for the `name` that are twice the originally documented or observed length, this may unexpectedly break the customer's database. Furthermore, string properties that appear in URLs (including query parameters) are especially likely to have client-side limits, making them more sensitive to length changes.

##### Risk of changing value format or construction

Customers often depend on the format or algorithmic construction of a field for client-side parsing, hashing, or database table construction. Changing it in an existing field could break that client-side consumption.

> **Agent extension — not part of the AIP standard.** The breaking-change list has two frequently underestimated entries: adding pagination to a previously unpaginated method changes the generated client signature and is breaking (so paginate from day one), and moving an existing field into or out of a `oneof` breaks generated code even though the wire format survives (adding a new field to an existing `oneof` is fine). Tightening `field_behavior` — for example making a field `REQUIRED` — is also a contract break clients will feel immediately.

### 8.2 Stability Levels (AIP-181)
[ref: #stability-levels-aip-181]

While different organizations (both inside Google and outside) have different product life cycles, AIPs refer to the *stability* of an API component using the following terms.

**Note:** These stability levels roughly correspond to the product launch stages (alpha, beta, GA) in Google Cloud, but are not identical. GCP imposes its own additional expectations and commitments on top of what is outlined here.

#### Alpha

An *alpha* component undergoes rapid iteration with a known set of users who **must** be tolerant of change. The number of users **should** be a curated, manageable set, such that it is feasible to communicate with all of them individually.

Breaking changes **must** be both allowed and expected in alpha components, and users **must** have no expectation of stability.

#### Beta

A *beta* component **must** be considered complete and ready to be declared stable, subject to public testing. Beta components **should** be exposed to an unknown and potentially large set of users. In other words, beta components **should not** be behind an allowlist; instead, they **should** be available to the public.

Because users of beta components tend to have a lower tolerance of change, beta components **should** be as stable as possible; however, the beta component **must** be permitted to change over time. These changes **should** be minimal but **may** include backwards-incompatible changes to beta components. Backwards-incompatible changes **must** be made only after a reasonable deprecation period to provide users with an opportunity to migrate their code. This deprecation period **must** be defined at the time of being marked beta.

Beta components **should** be time-boxed and promoted to stable if no issues are found in the specified timeframe, which **should** be specified at the time of being marked beta. A reasonable time period **may** vary, but a good rule of thumb is 90 days.

#### Stable

A *stable* component **must** be fully-supported over the lifetime of the major API version. Because users expect such stability from components marked stable, there **must** be no breaking changes to these components, subject to the caveats described below.

##### Major versions

When breaking changes become necessary, the API producer **should** create the next major version of the API, and start a deprecation clock on the existing version.

Turn-down of any version containing stable components **must** have a formal process defined at the time of being marked stable. This process **must** specify a deprecation period for users which provides them with reasonable advance warning.

##### Isolated changes

On very rare occasions, it could be preferable to make a small, isolated breaking change, if this will only cause inconvenience to a small subset of users. (Creating a new major version is an inconvenience to all users.) In this case, the API producer **may** deprecate the component, but **must** continue to support the component for the normal turndown period for a stable component.

**Important:** Making an in-place breaking change in a stable API is considered an extreme course of action, and should be treated with equal or greater gravity as creating a new major version. For example, at Google, this requires the approval of the API Governance team.

##### Emergency changes

In certain exceptional cases, such as security concerns or regulatory requirements, any API component **may** be changed in a breaking manner regardless of its stability level, and a deprecation is not promised in these situations.

> **Agent extension — not part of the AIP standard.** Stability labels set the change budget: GA admits no breaking changes, while alpha and beta allow them only with a real deprecation window and migration path — and user tolerance in beta is lower than the letter of the rule suggests. Treat every breaking change in a labeled surface as a launch event (notice, timeline, migration guide), not a routine commit.

### 8.3 External Software Dependencies (AIP-182)
[ref: #external-software-dependencies-aip-182]

Some services have a particular type of dependency on external software: they allow users to create resources that run on or expose the external software in some way. For example:

- A database admin service can allow users to create databases running on a particular version of a particular database engine (for example, PostgreSQL 13.4).
- A virtual machine service can allow users to create VMs running a particular operating system (for example, Ubuntu 20.04).
- An application or function platform service can allow users to write code that runs against a particular version of a programming language (for example, Node.js 16.6).

Services that provide external software to users in this way will eventually need to address the fact that all of these types of software have release lifecycles, and the versions they currently expose will eventually reach end-of-life.

#### Guidance

Services that expose external software dependencies **should** allow users to create resources using any currently-supported LTS (long-term support) version of the supported software, and **may** allow users to create resources using non-LTS versions.

Services **should not** indefinitely allow users to create new resources using versions that have reached end-of-life, although they **may** have a transition period between when the software version reaches end-of-life and when support for creating new resources with that version is removed.

**Note:** Restricting or removing the ability to create resources using end-of-life versions of software is **not** considered a breaking change for the service for the purpose of [AIP-181](#stability-levels-aip-181), even though it actually is one. However, because the change can break existing users' workflows, services **must** notify users who are using resources approaching end-of-life.

If possible, services **should** allow previously-created resources to remain, and **may** warn users of the risks associated with continuing to use end-of-life software. Services **should not** proactively remove resources using end-of-life software, or impose other restrictions on existing resources, unless critical security concerns require the service to do so.

#### Continued support

If supporting a version that has reached end-of-life is necessary for business reasons (usually because the end-of-life software still has significant adoption), the service **may** choose to officially support the end-of-life version, but **must** take on the responsibility of patching and maintaining the software if it does so.

> **Agent extension — not part of the AIP standard.** When an API surfaces an external dependency (database engine versions, OS images), the contract is that users can create resources on any currently supported LTS release; non-LTS versions are allowed as additions, never as replacements. Watch the dependency's own EOL calendar — a version you expose past its upstream end-of-life becomes your support problem.

### 8.4 API Versioning (AIP-185)
[ref: #api-versioning-aip-185]

This topic describes the versioning strategies used by Google APIs. In general, these strategies apply to all Google-managed services.

#### Guidance

All API interfaces **must** provide a *major version number*, which is encoded at the end of the protobuf package, and included as the first part of the URI path for REST APIs. In the event an API needs to make an incompatible change, consult [AIP-180](#backwards-compatibility-aip-180) and [AIP-181](#stability-levels-aip-181) for necessary steps based on the stability level of the surface in question.

**Note:** The use of the term "major version number" above is taken from semantic versioning. However, unlike in traditional semantic versioning, Google APIs **must not** expose minor or patch version numbers. For example, Google APIs use `v1`, not `v1.0`, `v1.1`, or `v1.4.2`. From a user's perspective, major versions are updated in place with minor/patch equivalent changes, and users receive new functionality without migration.

A new major version of an API **must not** depend on a previous major version of the same API. An API surface **must not** depend on other APIs, except for in the cases outlined in [AIP-213](10_protocol_buffers.md#common-components-aip-213) and [AIP-215](10_protocol_buffers.md#api-specific-protos-aip-215).

Different versions of the same API **must** be able to work at the same time within a single client application for a reasonable transition period. This time period allows the client to transition smoothly to the newer version. An older version **must** go through a reasonable, well-communicated deprecation period before being shut down.

For releases which have alpha or beta stability, APIs **must** append the stability level after the major version number in the protobuf package and URI path using one of these strategies:

- Channel-based versioning (recommended)
- Release-based versioning
- Visibility-based versioning

#### Channel-based versioning

A *stability channel* is a long-lived release at a given stability level that receives in-place updates. There is no more than one channel per stability level for a major version. Under this strategy, there are up to three channels available: alpha, beta, and stable.

The alpha and beta channel **must** have their stability level appended to the version, but the stable channel **must not** have the stability level appended. For example, `v1` is an acceptable version for the stable channel, but `v1beta` or `v1alpha` are not. Similarly, `v1beta` or `v1alpha` are acceptable versions for the respective beta and alpha channel, but `v1` is not acceptable for either. Each of these channels receives new features and updates "in-place".

The beta channel's functionality **must** be a superset of the stable channel's functionality, and the alpha channel's functionality **must** be a superset of the beta channel's functionality.

##### Deprecating API functionality

API elements (fields, messages, RPCs) **may** be marked deprecated in any channel to indicate that they should no longer be used:

```protobuf
// Represents a scroll. Books are preferred over scrolls.
message Scroll {
  option deprecated = true;

  // ...
}
```

Deprecated API functionality **must not** graduate from alpha to beta, nor beta to stable. In other words, functionality **must not** arrive "pre-deprecated" in any channel.

The beta channel's functionality **may** be removed after it has been deprecated for a sufficient period; we recommend 180 days. For functionality that exists only in the alpha channel, deprecation is optional, and functionality **may** be removed without notice. If functionality is deprecated in an API's alpha channel before removal, the API **should** apply the same annotation, and **may** use any timeframe it wishes.

#### Release-based versioning

**Important:** This pattern is not commonly used for new services. There are existing services that follow it, but Channel-based Versioning is the preferred mechanism.

An *individual release* is an alpha or beta release that is expected to be available for a limited time period before its functionality is incorporated into the stable channel, after which the individual release will be shut down. When using release-based versioning strategy, an API may have any number of individual releases at each stability level.

**Note:** Both the channel-based and release-based strategies update the *stable* version in-place. There is a single stable channel, rather than individual stable releases, even when using the release-based strategy.

Alpha and beta releases **must** have their stability level appended to the version, followed by an incrementing release number. For example, `v1beta1` or `v1alpha5`. APIs **should** document the chronological order of these versions in their documentation (such as comments).

Each alpha or beta release **may** be updated in place with backwards-compatible changes. For beta releases, backwards-incompatible updates **should** be made by incrementing the release number and publishing a new release with the change. For example, if the current version is `v1beta1`, then `v1beta2` is released next.

Alpha and beta releases **should** be shut down after their functionality reaches the stable channel. An alpha release **may** be shut down at any time, while a beta release **should** allow users a reasonable transition period; we recommend 180 days.

#### Visibility-based versioning

API visibility is an advanced feature provided by Google API infrastructure. It allows API producers to expose multiple external API views from one internal API surface, and each view is associated with an API *visibility label*, such as:

```protobuf
import "google/api/visibility.proto";

message Resource {
  string name = 1;

  // Preview. Do not use this feature for production.
  string display_name = 2
    [(google.api.field_visibility).restriction = "PREVIEW"];
}
```

A visibility label is a case-sensitive string that can be used to tag any API element. By convention, visibility labels should always use UPPER case. An implicit `PUBLIC` label is applied to all API elements unless an explicit visibility label is applied as in the example above.

Each visibility label is an allow-list. API producers need to grant visibility labels to API consumers for them to use API features associated with the labels. In other words, an API visibility label is like an ACL'ed API version.

Multiple visibility labels **may** be applied to an element by using a comma-separated string (e.g. `"PREVIEW,TRUSTED_TESTER"`). When multiple visibility labels are used, then the client needs only *one* of the visibility labels (logical `OR`).

By default, the visibility labels granted to the API consumer are used to verify incoming requests. However, a client can send requests with an explicit visibility label as follows:

```http
GET /v1/projects/my-project/topics HTTP/1.1
Host: pubsub.googleapis.com
Authorization: Bearer y29....
X-Goog-Visibilities: PREVIEW
```

A single API request can specify at most one visibility label.

API producers can use API visibility for API versioning, such as `INTERNAL` and `PREVIEW`. A new API feature starts with the `INTERNAL` label, then moves to the `PREVIEW` label. When the feature is stable and becomes generally available, all API visibility labels are removed from the API definition.

In general, API visibility is easier to implement than API versioning for incremental changes, but it depends on sophisticated API infrastructure support. Google Cloud APIs often use API visibility for Preview features.

> **Agent extension — not part of the AIP standard.** Encode the major version in the URI path and at the end of the proto package (`v1`), and append the stability level for pre-GA surfaces (`v1beta1`, `v2alpha1`) — package-level versioning is what lets two major versions of the same API coexist in one binary while clients migrate. One channel per stability level per major version; in-place updates inside a channel must stay backwards-compatible.
