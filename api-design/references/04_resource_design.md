---
subject: "Resource-oriented API design corpus; `AIP-121` nouns standard methods stateless consistency, `AIP-122` names hierarchy IDs full URIs, `AIP-123` types annotations patterns, `AIP-124` associations canonical parent many-to-many, `AIP-126` enums, `AIP-128` declarative-friendly reconciliation, `AIP-129` field ownership effective values normalization, `AIP-156` singletons, `AIP-236` policy preview experiments."
index:
  - anchor: resource-oriented-design-aip-121
    what: "The AIP-121 resource-oriented paradigm: model APIs as hierarchies of named resources manipulated by a small set of standard methods over a stateless protocol, with strong consistency after mutations and an acyclic resource graph."
    problem: "API modeled around verbs and bespoke RPC shapes forces consumers to relearn every service, so client generation, declarative tooling, and orchestration pipelines break across teams; noun verb imbalance, per-service rpc dialects, cognitive load, tooling payoff loss, database schema mirroring, cyclic reference trap, read-after-write gap."
    use_when: "Greenfield API taking shape; noun set and hierarchy being sketched before methods; evaluating whether custom verb justified over standard set; weighing consistency guarantees clients need after mutation."
    avoid_when: "Pure data-plane streaming or analytics surface where resource model fits poorly; existing RPC-style API under maintenance-only stewardship; method-level details needed rather than paradigm choice (05_operations › standard methods)."
    expected: "Surface organizes around named resources and shared verbs, every mutation reaches steady state before completion, references form acyclic graph, and generic tooling consumes API uniformly."
  - anchor: resource-names-aip-122
    what: "The AIP-122 naming rules for structure: relative names alternate plural camelCase collection identifiers with IDs, `name` and `parent` string fields carry them with `google.api.resource_reference` annotations, and cross-resource fields use snake-case references rather than embedded messages."
    problem: "Resources identified by ad-hoc tuples, embedded messages, or self-links force consumers to juggle opaque identifiers, so logging, access control, and reusable interfaces fail to understand references; anonymous tuple burden, identifier opacity, payload nesting coupling, permission bypass, canonical name storage, collection hierarchy shape, reference field convention."
    use_when: "Naming new resource or request message; deciding how one resource points at another; choosing collection segment words; reserving `name` field semantics against display-title misuse."
    avoid_when: "ID character rules or user-settable identifiers at stake (sibling card); cross-API or versioned URI form needed (sibling card); internal-only API embedding resources under tight lifecycle exception."
    expected: "Every resource exposes canonical string `name`, references travel as annotated strings, collections read as plural lowercase-led segments, and tuple or self-link identification never leaks into surface."
  - anchor: resource-names-aip-122
    what: "The AIP-122 resource ID rules: user-specified IDs follow RFC-1034-derived lowercase hyphenated format (`^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$`) documented by the API, system-generated IDs document basic shape, and aliases like `users/me` map onto canonical IDs."
    problem: "User-chosen identifiers accepted without documented format allow embedded slashes, unicode, or uppercase through, so URLs break, percent-encoding proliferates, and stored names become unusable in DNS contexts; undocumented id format, url-hostile characters, sixty-three character cap, lowercase hyphen pattern, alias lookup shortcut, create-time id field, dns compatibility."
    use_when: "Create request accepts caller-chosen identifier; alias shortcut like `users/me` under consideration; documentation of accepted identifier shape overdue; distinguishing idempotency `request_id` from resource identifier."
    avoid_when: "Whole-name structure or hierarchy question (sibling card); cross-API full-name form at stake (sibling card); tuple-based legacy identification under migration (whole-name rules apply first)."
    expected: "User-specified IDs validate against documented RFC-1034-style regex, aliases resolve to canonical form in responses, and `book_id`-style create fields land as final name component only."
  - anchor: resource-names-aip-122
    what: "The AIP-122 distinction between relative names, full resource names (schemeless `//service.googleapis.com/...` URIs without version, stable across versions and endpoints), and access URIs carrying protocol, version, and endpoint."
    problem: "Field references resources across multiple APIs with owning service ambiguous, so relative strings misresolve and version-pinned URIs baked into stored data rot on upgrade; cross-api ambiguity, schemeless uri form, version persistence trap, endpoint regionalization drift, authority hostname, persisted uri decay, multi-endpoint convention."
    use_when: "Field may point into arbitrary external API; deciding whether version belongs in persisted reference; regional or mTLS endpoints multiply; choosing between relative and schemeless form for given context."
    avoid_when: "Owning API obvious from context (relative form suffices); intra-service naming or ID format at stake (sibling cards); full access URL construction needed rather than identity form."
    expected: "Cross-API fields carry schemeless version-free full names, intra-service fields stay relative, and stored references survive major version upgrades and endpoint changes."
  - anchor: resource-types-aip-123
    what: "The AIP-123 globally-unique type name (`{Service Name}/{Type}`, PascalCase singular matching the message) plus the `google.api.resource` annotation contract: `pattern` ordering stability, snake_case variables without `_id`, `singular`/`plural` lower-camel forms."
    problem: "Tools spanning providers like Kubernetes or GraphQL cannot distinguish identically-named messages from different APIs, so generic integrations collide and later pattern edits break generated clients; global type uniqueness, multi-provider tooling collision, message alignment payoff, append-only pattern list, annotation variable casing, singular plural derivation."
    use_when: "Registering resource annotation for new message; adding secondary pattern to existing type; deriving `singular`/`plural` noun forms; checking variable naming inside braces."
    avoid_when: "Plain intra-API naming questions without tooling identity concerns; pattern removal or reorder contemplated (forbidden, additions at end only); association structure between types at stake."
    expected: "Each resource declares PascalCase type under service namespace, annotation patterns append-only with well-formed variables, and Kubernetes-style tools resolve type identity across providers."
  - anchor: resource-association-aip-124
    what: "The AIP-124 association rules: exactly one canonical parent per resource, secondary many-to-one links via annotated reference fields plus `filter`, and many-to-many via repeated name fields or a metadata-bearing sub-resource."
    problem: "Resource legitimately belongs under two hierarchies and List demands both parents at once, so routing, authorization, pagination, and caching tangle into exponential complexity; dual parent trap, parentage election, many-to-many modeling, join table misfit, association metadata carrier, filter-based lookup, repeated reference list."
    use_when: "Entity relates to several parents many-to-one; relationship itself carries attributes; choosing between repeated field and association sub-resource; List must stay single-parent with secondary filtering."
    avoid_when: "Simple tree hierarchy expressible directly; cross-API reference format at stake (04_resource_design › resource names); repeated-field atomicity question (06_fields › repeated fields)."
    expected: "Single parentage anchors each pattern, secondary associations ride annotated fields or filters, many-to-many uses name lists unless metadata justifies sub-resource."
  - anchor: enumerations-aip-126
    what: "The AIP-126 enum rules: `UPPER_SNAKE_CASE` values with `<NAME>_UNSPECIFIED` zero, nested versus package-level placement with prefixing to dodge hoisting collisions, documented frozen-or-evolving stance, and string or boolean alternatives for fast-changing or standards-covered value sets."
    problem: "Field accepts discrete values but chosen representation changes weekly, so enum additions ripple breaking changes into client code and proto3 zero default silently acquires meaning; enum evolution asymmetry, breaking rename renumber, unspecified zero value, hoisting namespace collision, kebab-case string fallback, widely-adopted standard clash, boolean inflexibility."
    use_when: "Value set stable for year-plus horizon; deciding inline versus shared placement; proto3 default must stay explicit; weighing enum against string when standard representation exists."
    avoid_when: "Values churn faster than yearly cadence (string with documented kebab-case); competing ISO-style standard already defines representation; genuine two-state flag with `false` default suffices."
    expected: "Enums carry explicit `<NAME>_UNSPECIFIED` default, values stay append-only with documented growth policy, placement avoids hoisted collisions, and volatile sets ship as documented strings."
  - anchor: declarative-friendly-interfaces-aip-128
    what: "The AIP-128 declarative-friendly contract: strongly-consistent standard lifecycle methods only, `style: DECLARATIVE_FRIENDLY` designation, output-only `bool reconciling` exposing in-flight convergence, and `Get` returning actual current state."
    problem: "Terraform-style client reconciles desired configuration against reads, but server-injected defaults and read-after-write lag make plan diffs report phantom changes forever; ghost plan noise, server default injection, convergence visibility gap, intended versus actual state, generic automation uniformity, configuration as code, drift correction cycle."
    use_when: "Resource targets IaC ecosystem; updates take more than seconds to materialize; generic lifecycle automation expected without per-resource glue; deciding whether designation annotation warranted."
    avoid_when: "Data-plane imperative operation surface; custom-method-heavy design that cannot honor lifecycle uniformity; ephemeral resources outside IaC-driven workflows."
    expected: "Reads reflect live truth, `reconciling` flags unfinished convergence, lifecycle runs on standard methods alone, and post-apply comparisons stay empty."
  - anchor: server-modified-values-and-defaults-aip-129
    what: "The AIP-129 ownership and normalization rules: every field has single owner (`OUTPUT_ONLY` marks server-owned), server-decided fallbacks split into mutable input plus `effective_`-prefixed output twin, and documented `google.api.field_info` normalizations (`uuid`, `ipv4`, `ipv6`, `email`)."
    problem: "Server silently rewrites client-supplied values or injects defaults without marking ownership, so declarative tools fight endless correction loops and echoed fields get rejected on update; ownership ambiguity, undocumented value rewrite, server overwrite battle, effective value twin, output-only marking, round-trip update failure, documented comparison method."
    use_when: "Service allocates or computes fallback when client omits value; input canonicalized for storage (case folding, CIDR shortening); deciding which side owns each field; choosing companion field name for service-decided outcome."
    avoid_when: "Pure client-owned payload with no server touch; normalization beyond allowed annotation formats invented ad hoc; intended-state semantics wanted (04_resource_design › declarative-friendly interfaces)."
    expected: "Ownership is unambiguous for every field, service-decided results live in `effective_` twins, normalizations declared via `google.api.field_info`, and echoed updates never bounce."
  - anchor: singleton-resources-aip-156
    what: "The AIP-156 singleton pattern: exactly one instance per parent addressed by static trailing segment without ID (e.g. `users/{user}/config`), only `Get`/`Update` (never `Create`/`Delete`), mandatory `singular`/`plural` declaration, and pseudo-collection `List` per AIP-159."
    problem: "Per-parent configuration object modeled as regular collection forces fake IDs and create-delete lifecycle onto something that always exists, so clients handle NotFound for unavoidable entity; fake id ceremony, config object shape, constant final segment, implicit lifecycle, orphaned instance risk, pseudo-collection listing, collection lint misfire."
    use_when: "Exactly one settings-style entity exists for each parent; create-delete semantics meaningless because existence ties to parent; listing across parents desirable despite singularity; wondering whether `Update` allowed when fields output-only."
    avoid_when: "Multiple instances under one parent plausible later (real collection safer); user-chosen identifier needed; entity lifecycle independent from parent."
    expected: "Singleton addressed by parent name plus static segment, lifecycle limited to get-update, both noun forms declared, and cross-parent listing works via pseudo-collection."
  - anchor: policy-preview-aip-236
    what: "The AIP-236 preview mechanism: candidate policy configuration stored as nested `*Experiment` resource, evaluated against production traffic via `startPreview`/`stopPreview` with `log_prefix`-tagged evaluation logs, and promoted atomically by etag-guarded `commit`."
    problem: "Access-rule change shipped straight to production can lock out legitimate users or expose sensitive resources, with no way to observe effect on real traffic beforehand; blast-radius lockout, unvalidated rollout, live traffic evaluation gap, experiment nesting, preview metadata lifecycle, etag-guarded promotion, comparison log isolation."
    use_when: "Firewall-style rule resource needs safe rollout path; customer must observe proposed effect before activation; multiple candidate configurations compared concurrently; promotion requires atomic swap with version guard."
    avoid_when: "Non-policy resource rollout (explicit non-goal); plain validation of syntax rather than traffic effect; experiment already promoted and only policy CRUD remains."
    expected: "Experiments nest under live policy, preview logs tagged with `log_prefix` isolate candidate behavior, `commit` swaps atomically behind matching etag, and failed promotion leaves both sides untouched."
aips: [121, 122, 123, 124, 126, 128, 129, 156, 236]
---

# Resource Design

## 4. Resource Design

### 4.1 Resource-Oriented Design (AIP-121)
[ref: #resource-oriented-design-aip-121]

Resource-oriented design is a pattern for specifying RPC APIs, based on several high-level design principles (most of which are common to recent public HTTP APIs):

- The fundamental building blocks of an API are individually-named **resources** (nouns) and the relationships and hierarchy that exist between them.
- A small number of **standard methods** (verbs) provide the semantics for most common operations. Custom methods are available in situations where the standard methods do not fit.
- **Stateless protocol**: each interaction between the client and the server is independent, and both the client and server have clear roles.

Readers might notice similarities between these principles and some principles of REST; resource-oriented design borrows many principles from REST, while also defining its own patterns where appropriate.

#### Guidance

When designing an API, consider the following (roughly in logical order):

1. The resources (nouns) the API will provide.
2. The relationships and hierarchies between those resources.
3. The schema of each resource.
4. The methods (verbs) each resource provides, relying as much as possible on the standard verbs.

##### Resources

A resource-oriented API **should** generally be modeled as a resource hierarchy, where each node is either a simple resource or a collection of resources.

A **collection** contains resources of **the same type**. For example, a publisher has the collection of books that it publishes. A resource usually has fields, and resources may have any number of sub-resources (usually collections).

**Note:** While there is some conceptual alignment between storage systems and APIs, a service with a resource-oriented API is not necessarily a database, and has enormous flexibility in how it interprets resources and methods. API designers **should not** expect that their API will be reflective of their database schema. In fact, having an API that is identical to the underlying database schema is actually an anti-pattern, as it tightly couples the surface to the underlying system.

##### Methods

Resource-oriented APIs emphasize resources (data model) over the methods performed on those resources (functionality). A typical resource-oriented API exposes a large number of resources with a small number of methods on each resource. The methods can be either the standard methods (`Get`, `List`, `Create`, `Update`, `Delete`), or custom methods.

If the request to or the response from a standard method (or a custom method in the same **service**) **is** the resource or **contains** the resource, the resource schema for that resource across all methods **must** be the same.

| Standard method | Request | Response |
|----------------|---------|----------|
| Create | Contains the resource | Is the resource |
| Get | None | Is the resource |
| Update | Contains the resource | Is the resource |
| Delete | None | None |
| List | None | Contains the resources |

The table above describes each standard method's relationship to the resource, where "None" indicates that the resource neither **is** nor **is contained in** the request or the response.

A resource **must** support at minimum **Get**: clients must be able to validate the state of resources after performing a mutation such as `Create`, `Update`, or `Delete`.

A resource **must** also support **List**, except for singleton resources where more than one resource is not possible.

**Note:** A custom method in resource-oriented design does **not** entail defining a new or custom HTTP verb. Custom methods use traditional HTTP verbs (usually `POST`) and define the custom verb in the URI.

APIs **should** prefer standard methods over custom methods; the purpose of custom methods is to define functionality that does not cleanly map to any of the standard methods. Custom methods offer the same design freedom as traditional RPC APIs, which can be used to implement common programming patterns, such as database transactions, import and export, or data analysis.

##### Strong Consistency

For methods that operate on the **management plane**, the completion of those operations (either successful or with an error, long-running operation, or synchronous) **must** mean that the state of the resource's existence and all user-settable values have reached a steady-state.

Output-only values unrelated to the resource state **should** also have reached a steady-state for values that are related to the resource state.

Examples include:

- Following a successful `Create` that is the latest mutation on a resource, a `Get` request for a resource **must** return the resource.
- Following a successful `Update` that is the latest mutation on a resource, a `Get` request for a resource **must** return the final values from the update request.
- Following a successful `Delete` that is the latest mutation on a resource, a `Get` request for a resource **must** return `NOT_FOUND` (or the resource with the `DELETED` state value in the case of soft delete).

Clients of resource-oriented APIs often need to orchestrate multiple operations in sequence (e.g., create resource A, create resource B which depends on A), and ensuring that resources immediately reflect steady user state after an operation is complete ensures clients can rely on method completion as a signal to begin the next operation.

Output-only fields ideally would follow the same guidelines, but as these fields can often represent a resource's live state, it is sometimes necessary for these values to change after a successful mutation operation to reflect a state change.

##### Stateless Protocol

As with most public APIs available today, resource-oriented APIs **must** operate over a stateless protocol: the fundamental behavior of any individual request is independent of other requests made by the caller. This is to say, each request happens in isolation of other requests made by that client or another, and resources exposed by an API are directly addressable without needing to apply a series of specific requests to "reach" the desired resource.

In an API with a stateless protocol, the server has the responsibility for persisting data, which may be shared between multiple clients, while clients have sole responsibility and authority for maintaining the application state.

##### Cyclic References

The relationship between resources, such as with resource references, **must** be representable via a **directed acyclic graph**. The parent-child relationship also **must** be acyclic, and as per AIP-124 a given resource instance will only have one canonical parent resource.

A cyclic relationship between resources increases the complexity of managing resources. Consider resources A and B that refer to each other. The process to create said resources is:

1. Create resource A without a reference to B. Retrieve ID for resource A.
2. Create resource B with a reference to A. Retrieve ID for resource B.
3. Update resource A with the reference to B.

The delete operation may also become more complex, due to reasoning about which resource must be dereferenced first for a successful deletion.

This requirement does not apply to relationships that are expressed via output-only fields, as they do not require the user to specify the values and in turn do not increase resource management complexity.

#### Rationale

Resource-oriented design provides a uniform, predictable interface that reduces cognitive load for API consumers. By standardizing on a small set of verbs applied to a rich hierarchy of nouns, clients can learn the patterns once and apply them across the entire API surface. This consistency is what enables declarative tooling, automated client generation, and reliable orchestration.

The stateless requirement ensures that resources are directly addressable and cacheable, while the acyclic requirement keeps the resource graph traversable and prevents circular dependency nightmares in lifecycle management.

#### Further reading

- [AIP-122](04_resource_design.md#resource-names-aip-122) — Resource Names
- [AIP-124](04_resource_design.md#resource-association-aip-124) — Resource Association
- [AIP-128](04_resource_design.md#declarative-friendly-interfaces-aip-128) — Declarative-Friendly Interfaces
- [AIP-131](05_operations.md#standard-method-get-aip-131) through [AIP-135](05_operations.md#standard-method-delete-aip-135) — Standard Methods
- [AIP-136](05_operations.md#custom-methods-aip-136) — Custom Methods

> **Agent extension — not part of the AIP standard.** Resource-oriented design pays off mechanically: when an API is modeled as resources with standard methods, the Google API Linter can enforce most of the AIP rule set in CI against the proto surface, catching design drift before code generation. Modeling around verbs instead of nouns forfeits that tooling and typically resurfaces later as inconsistent method shapes across teams.

### 4.2 Resource Names (AIP-122)
[ref: #resource-names-aip-122]

Most APIs expose **resources** (their primary nouns) which users are able to create, retrieve, and manipulate. Additionally, resources are **named**: each resource has a unique identifier that users use to reference that resource, and these names are what users should **store** as the canonical names for the resources.

#### Guidance

All resource names defined by an API **must** be unique within that API. (See the section on full resource names below for more information on referring to resources across APIs.)

Resource names are formatted according to the URI path schema, but without the leading slash:

```
publishers/123/books/les-miserables
users/vhugo1802
```

- Resource name components **should** usually alternate between collection identifiers (e.g., `publishers`, `books`, `users`) and resource IDs (e.g., `123`, `les-miserables`, `vhugo1802`).
- Resource names **must** use the `/` character to separate individual segments of the resource name.
  - Non-terminal segments of a resource name **must not** contain a `/` character.
  - The terminal segment of a resource name **should not** contain a `/` character.
- Resource names **should** only use characters available in DNS names, as defined by RFC-1123.
  - Additionally, resource IDs **should not** use upper-case letters.
  - If additional characters are necessary, resource names **should not** use characters that require URL-escaping, or characters outside of ASCII.
  - If Unicode characters can not be avoided, resource names **must** be stored in Normalization Form C (see AIP-210).

**Note:** Resource names as described here are used within the scope of a single API (or else in situations where the owning API is clear from the context), and are only required to be unique within that scope. For this reason, they are sometimes called **relative resource names** to distinguish them from **full resource names** (discussed below).

##### Required fields

- Resources **must** expose a `name` field that contains its resource name.
- Resources **may** provide the resource ID as a separate field (e.g., `book_id`). This field **must** apply the `OUTPUT_ONLY` field behavior classification.
- Resources **may** expose a separate, system-generated unique ID field (`uid`). This field **must** apply the `OUTPUT_ONLY` field behavior classification.
- Resources **must not** expose tuples, self-links, or other forms of resource identification.
- All ID fields **should** be strings.

##### Collection identifiers

The collection identifier segments in a resource name **must** be the plural form of the noun used for the resource. (For example, a collection of `Publisher` resources is called `publishers` in the resource name.)

- Collection identifiers **must** be concise American English terms.
- Collection identifiers **must** be in `camelCase`.
- Collection identifiers **must** begin with a lower-cased letter and contain only ASCII letters and numbers (`/[a-z][a-zA-Z0-9]*/`).
- Collection identifiers **must** be plural.
  - In situations where there is no plural word (`info`), or where the singular and plural terms are the same (`moose`), the non-pluralized (singular) form is correct. Collection segments **must not** "coin" words by adding "s" in such cases (e.g., avoid `infos`).
- Within any given single resource name, collection identifiers **must** be unique. (e.g., `people/xyz/people/abc` is invalid.)

###### Nested collections

If a resource name contains multiple levels of a hierarchy, and a parent collection's name is used as a prefix for the child resource's name, the child collection's name **may** omit the prefix. For example, given a collection of `UserEvent` resources that would normally be nested underneath `users`:

```
users/vhugo1802/userEvents/birthday-dinner-226
```

An API **should** use the less-redundant form:

```
users/vhugo1802/events/birthday-dinner-226
```

In this situation, the **message** and **resource type** are still called `UserEvent`; only the collection and resource identifiers in the pattern(s) are shortened. Since the **resource type** is not shortened, the `singular` and `plural` are similarly **not shortened**.

```protobuf
message UserEvent {
  option (google.api.resource) = {
    type: "example.googleapis.com/UserEvent"
    // Only the collection & resource identifiers in the `pattern` are shortened.
    pattern: "projects/{project}/users/{user}/events/{event}"
    singular: "userEvent"
    plural: "userEvents"
  };

  string name = 1;
}
```

**Note:** APIs wishing to do this **must** follow this format consistently throughout all of its `pattern` entries defined and anywhere else the resource is referenced in the API, or else not at all.

##### Resource ID segments

A resource ID segment identifies the resource within its parent collection. In the resource name `publishers/123/books/les-miserables`, `123` is the resource ID for the publisher, and `les-miserables` is the resource ID for the book.

- If resource IDs are user-specified, the API **must** document allowed formats. User-specified resource IDs **should** conform to RFC-1034; which restricts to letters, numbers, and hyphen, with the first character a letter, the last a letter or a number, and a 63 character maximum.
  - Additionally, user-specified resource IDs **should** restrict letters to lower-case (`^[a-z]([a-z0-9-]{0,61}[a-z0-9])?$`).
  - Characters outside of ASCII **should not** be permitted; however, if Unicode characters are necessary, APIs **must** follow guidance in AIP-210.
- If resource IDs are not user-settable, the API **should** document the basic format, and any upper boundaries (for example, "at most 63 characters").
- For more information, see the `Create` standard method.

##### Resource ID aliases

It is sometimes valuable to provide an alias for common lookup patterns for resource IDs. For example, an API with `users` at the top of its resource hierarchy may wish to provide `users/me` as a shortcut for retrieving information for the authenticated user.

APIs **may** provide programmatic aliases for common lookup patterns. However, all data returned from the API **must** use the canonical resource name.

##### Full resource names

In most cases, resource names are used within a single API only, or else they are used in contexts where the owning API is clear (for example, `string pubsub_topic`).

However, sometimes it is necessary for services to refer to resources in an arbitrary API. In this situation, the service **should** use the **full resource name**, a schemeless URI with the owning API's service name, followed by the relative resource name:

```
//library.googleapis.com/publishers/123/books/les-miserables
//calendar.googleapis.com/users/vhugo1802
```

**Note:** The full resource name **should not** be used for cross-API references where the owning API is clear; it is only used if a field refers to resources in multiple APIs where ambiguity is possible.

##### Resource URIs

The full resource name is a schemeless URI, but slightly distinct from the full URIs we use to access a resource. The latter includes the protocol (HTTPS), the API version, and the specific service endpoint to target:

```
https://library.googleapis.com/v1/publishers/123/books/les-miserables
https://calendar.googleapis.com/v3/users/vhugo1802
```

The version is not included in the full resource name because the full resource name is expected to persist from version to version. Even though the API surface may change between major versions, multiple major versions of the same API are expected to use the same underlying data.

**Note:** The correlation between the full resource name and the service's endpoint is by convention. In particular, one service is able to have multiple endpoints (example use cases include regionalization, mTLS, and private access), and the full resource name does not change between these.

##### Fields representing resource names

When defining a resource, the first field **should** be the resource name, which **must** be of type `string` and **must** be called `name` for the resource name. The message **should** include a `google.api.resource` annotation declaring the type (see AIP-123 for more on this).

```protobuf
// A representation of a book in the library.
message Book {
  option (google.api.resource) = {
    type: "library.googleapis.com/Book"
    pattern: "publishers/{publisher}/books/{book}"
  };

  // The resource name of the book.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  // Other fields...
}
```

When defining a method that retrieves or acts on an already-existing resource (such as `GetBook` or `ArchiveBook`), the first field of the request message **should** be the resource name, which **must** be of type `string` and **must** be called `name` for the resource name. The field **should** also be annotated with the `google.api.resource_reference` annotation, referencing the resource type (AIP-123).

```protobuf
// Request message for ArchiveBook.
message ArchiveBookRequest {
  // The book to archive.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/Book"
    }];

  // Other fields...
}
```

**Note:** Fields **must not** be called `name` except for this purpose. For other use cases, either use a different term or prepend an adjective (for example: `display_name`).

##### Fields representing a resource's parent

When defining a method that retrieves resources from a collection or adds a new resource to a collection (such as `ListBooks` or `CreateBook`), the first field of the request message **should** be of type `string` and **should** be called `parent` for the resource name of the collection. The `parent` field **should** also be annotated with the `google.api.resource_reference` annotation, referencing the parent's resource type (AIP-123).

```protobuf
// Request message for ListBooks.
message ListBooksRequest {
  // The publisher to list books from.
  // Format: publishers/{publisher_id}
  string parent = 1 [(google.api.resource_reference) = {
    type: "library.googleapis.com/Publisher"
  }];

  // Other fields (e.g., page_size, page_token, filter, etc.)...
}
```

If there is more than one possible parent type, the `parent` field **should** be annotated with the `child_type` key on `google.api.resource_reference` instead:

```protobuf
// Request message for ListBooks.
message ListBooksRequest {
  // The parent to list books from.
  // Format:
  //   - publishers/{publisher_id}
  //   - authors/{author_id}
  string parent = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // Other fields (e.g., page_size, page_token, filter, etc.)...
}
```

**Note:** Fields **should not** be called `parent` except for this purpose. For other use cases, use a synonymous term if possible.

##### Fields representing another resource

When a field represents another resource, the field **should** be of type `string` and accept the resource name of the other resource. The field name **should** be equivalent to the corresponding message's name in snake case.

- Field names **may** include a leading adjective if appropriate (such as `string dusty_book`).
- Field names **should not** use the `_name` suffix unless the field would be ambiguous without it (e.g., `crypto_key_name`).
- Fields representing another resource **should** provide the `google.api.resource_reference` annotation with the resource type being referenced.
- If using the resource name is not possible and using the ID component alone is strictly necessary, the field **should** use an `_id` suffix (e.g., `shelf_id`).

The field **should not** be of type `message` using the `message` that implements the resource, **except** for one of the following conditions:

- The API is internal-only, has tight lifecycle relationships, and has a permission model that enables inherited access to embedded resources.
- The embedding of the resource is done as part of the AIP-162 revisions pattern.

Example of a resource reference:

```protobuf
// A representation of a book in a library.
message Book {
  option (google.api.resource) = {
    type: "library.googleapis.com/Book"
    pattern: "publishers/{publisher}/books/{book}"
  };

  // Name of the book.
  // Format is `publishers/{publisher}/books/{book}`
  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  // The shelf where the book currently sits.
  // Format is `shelves/{shelf}`.
  string shelf = 2 [(google.api.resource_reference) = {
    type: "library.googleapis.com/Shelf"
  }];

  // Other fields...
}
```

#### Rationale

##### Using names instead of IDs

For any large system, there are many kinds of resources. To use simple resource IDs to identify a resource, we'd actually need to use a resource-specific tuple to reliably identify it, such as `(bucket, object)` or `(user, album, photo)`. This creates several issues:

- Developers have to understand and remember such anonymous tuples.
- Passing tuples is generally harder than passing strings.
- Centralized infrastructures, such as logging and access control systems, don't understand specialized tuples.
- Specialized tuples limit API design flexibility, such as providing reusable API interfaces. For example, Long Running Operations can work with many other API interfaces because they use flexible resource names.

##### Standardizing on `name`

The concept of resource names is not a new one, and is formalized in Uniform Resource Names (URN) in conjunction with Uniform Resource Identifiers (URI) and Uniform Resource Locators (URL). Considering that the term "name" is so heavily overloaded in general, usage outside of a very well-defined meaning would be confusing for developers. So, the field name `name` is reserved in the context of AIP-compliant APIs so as to eliminate any confusion with resource names, and force other would-be "name" fields to use a more specific field name.

##### Disallowing embedding of resources

Using a resource message directly as the type of a field within another resource is problematic for a number of reasons:

- **Complicates the resource lifecycle:** If the dependency resource is deleted, what happens to the embedded reference in the dependent resource? Data retention and clean-up operations will be significantly complicated.
- **Bypasses permissions:** If every resource has its own set of permissions, a user with read permission on the dependent resource that doesn't have the same permission on the dependency resource suddenly cannot see the full resource.
- **Tightly couples resources in all aspects:** Changing the requirements in the schema, permissions, or otherwise for either resource impacts the other, significantly increasing complexity of rollouts.

Referencing by name, as is recommended, eliminates all of this complexity by preventing resource data duplication, and forcing the owning service to be involved in the resolution of the reference (via Standard Methods), guaranteeing isolation of logical concerns per-resource.

#### Further reading

- [AIP-123](04_resource_design.md#resource-types-aip-123) — Resource Types
- [AIP-162](07_design_patterns.md#resource-revisions-aip-162) — Resource Revisions
- [AIP-180](08_compatibility_and_versioning.md#backwards-compatibility-aip-180) — Backwards Compatibility

> **Agent extension — not part of the AIP standard.** Practical naming pitfalls that recur in reviews: keep resource IDs URL-friendly (avoid embedded slashes or percent-encoded characters); treat a user-specified ID (the `book_id` field of a Create request) as the final name component, never as a whole name; return full resource names in responses and cross-resource references, reserving relative names for intra-service contexts; and do not confuse the idempotency `request_id` (AIP-155) with the resource ID — the linter checks them separately.

### 4.3 Resource Types (AIP-123)
[ref: #resource-types-aip-123]

Most APIs expose **resources** (their primary nouns) which users are able to create, retrieve, and manipulate. APIs are allowed to name their resource types reasonably freely (within the requirements of this AIP), and are only required to ensure uniqueness within that API. This means that it is possible (and often desirable) for different APIs to use the same type name. For example, a Memcache and Redis API would both want to use `Instance` as a type name.

When mapping the relationships between APIs and their resources, however, it becomes important to have a single, globally-unique type name. Additionally, tools such as Kubernetes or GraphQL interact with APIs from multiple providers.

#### Terminology

In the guidance below, we use the following terms:

- **Service Name:** This is the name defined in the service configuration. This usually (but not necessarily) matches the hostname that users use to call the service. Example: `pubsub.googleapis.com`. This is equivalent to an API Group in Kubernetes.
- **Type:** This is the name used for the type within the API, e.g., the name of the Protobuf `message`. This is equivalent to an Object in Kubernetes.

#### Guidance

APIs **must** define a resource type for each resource in the API, according to the following pattern: `{Service Name}/{Type}`. The type name **must**:

- Match the containing API type's name.
- Start with an uppercase letter.
- Only contain alphanumeric characters.
- Be of the singular form of the noun.
- Use PascalCase (UpperCamelCase).

##### Examples

Examples of resource types include:

- `pubsub.googleapis.com/Topic`
- `pubsub.googleapis.com/Subscription`
- `spanner.googleapis.com/Database`
- `spanner.googleapis.com/Instance`
- `networking.istio.io/Instance`

##### Annotating resource types

APIs **should** annotate the resource types for each resource in the API using the `google.api.resource` annotation:

```protobuf
// A representation of a Pub/Sub topic.
message Topic {
  option (google.api.resource) = {
    type: "pubsub.googleapis.com/Topic"
    pattern: "projects/{project}/topics/{topic}"
    singular: "topic"
    plural: "topics"
  };

  // Name and other fields...
}
```

- Patterns **must** correspond to the resource name.
- Pattern variables (the segments within braces) **must** use `snake_case`, and **must not** use an `_id` suffix.
- Pattern variables **must** conform to the format `[a-z][_a-z0-9]*[a-z0-9]`.
- Pattern variables **must** be unique within any given pattern. (e.g., `projects/{abc}/topics/{abc}` is invalid; this is usually a natural corollary of collection identifiers being unique within a pattern.)
- Resources with multiple patterns **must** preserve ordering: new patterns **must** be added at the end of the list, and existing patterns **must not** be removed or re-ordered, as this breaks client library backward compatibility.
- **Singular** **must** be the lower camel case of the type.
  - Pattern variables **must** be the singular form of the resource type, e.g., a pattern variable representing a `Topic` resource ID is named `{topic}`.
- **Plural** **must** be the lower camel case plural of the singular.
  - Pattern collection identifier segments **must** match the plural of the resources, except in the case of nested collections.

##### Pattern uniqueness

When multiple patterns are defined within a resource, these patterns **must** be mutually unique, where uniqueness is defined as being by-character identical once all resource ID path segments have been removed, leaving all `/` separators.

Therefore the following two patterns **must not** be defined within the same resource:

- `user/{user}`
- `user/{user_part_1}~{user_part_2}`

#### Rationale

##### Type and message name alignment

In addition to simple schema-resource coherence and alignment, a number of consumers benefit from the `{Type}` and `message` names matching. Consumers have simpler lookups, client libraries get the same in addition to aligned user experience where resource-oriented code has naming aligned with the generated `message` code, generated reference documentation aligns resources with `message` docs, etc.

##### Singular and Plural

Well-defined singular and plurals of a resource enable clients to determine the proper name to use in code and documentation.

`lowerCamelCase` can be translated into other common forms of a resource name such as `UpperCamelCase` and `snake_case`.

#### Further reading

- [AIP-122](04_resource_design.md#resource-names-aip-122) — Resource Names
- [AIP-124](04_resource_design.md#resource-association-aip-124) — Resource Association

### 4.4 Resource Association (AIP-124)
[ref: #resource-association-aip-124]

APIs sometimes have resource hierarchies that can not be cleanly expressed in the usual tree structure. For example, a resource may have a many-to-one relationship with two other resource types instead of just one. Alternatively, a resource may have a many-to-many relationship with another resource type.

#### Guidance

A resource **must** have at most one canonical parent, and `List` requests **must not** require two distinct "parents" to work.

##### Multiple many-to-one associations

If a resource has a many-to-one relationship with multiple resource types, it **must** choose at most one of them to be the canonical parent. The resource **may** be associated with other resources through other fields on the resource.

```protobuf
message Book {
  // The resource name pattern for Book indicates that Publisher is the
  // canonical parent.
  option (google.api.resource) = {
    type: "library.googleapis.com/Book"
    pattern: "publishers/{publisher}/books/{book}"
  };

  // The resource name for the book.
  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  // The resource name for the book's author.
  string author = 2 [(google.api.resource_reference) = {
    type: "library.googleapis.com/Author"
  }];
}
```

When listing resources with multiple associations in this way, the RPC **must** treat the `string parent` field as required as discussed in AIP-132, and **must not** add additional required arguments. The RPC **should** include a `string filter` field that allows users to filter by other resource associations as discussed in AIP-160.

**Note:** Resource reference fields **must** accept the same resource name format that is used in the `name` field of the referenced resource.

##### Many-to-many associations

Many-to-many associations are less common in APIs than they are in relational databases, in part because they are more difficult to model and present over network interfaces.

An API **may** contain many-to-many relationships, and **should** use a repeated field containing a list of resource names, following the principles described for repeated fields in AIP-144.

```protobuf
message Book {
  option (google.api.resource) = {
    type: "library.googleapis.com/Book"
    pattern: "publishers/{publisher}/books/{book}"
  };

  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  // The resource names for the book's authors.
  repeated string authors = 2 [(google.api.resource_reference) = {
    type: "library.googleapis.com/Author"
  }];
}
```

**Note:** See AIP-144 for more information on repeated fields, including how to handle common issues such as atomic changes.

If the use of a repeated field is too restrictive, or if more metadata is required along with the association, an API **may** model a many-to-many relationship using a sub-resource with two one-to-many associations.

```protobuf
message BookAuthor {
  // The resource pattern for BookAuthor indicates that Book is the
  // canonical parent.
  option (google.api.resource) = {
    type: "library.googleapis.com/BookAuthor"
    pattern: "publishers/{publisher}/books/{book}/authors/{book_author}"
  };

  // The resource name for the book-author association.
  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  // The resource name for the author.
  string author = 2 [(google.api.resource_reference) = {
    type: "library.googleapis.com/Author"
  }];

  // Other fields...
}
```

**Note:** Using subresources to model an association between resources is only recommended if additional metadata is required in the relationship, or if the restrictions around the use of a repeated field preclude the use of that approach.

#### Rationale

The restriction to a single canonical parent simplifies routing, authorization, and caching. When a resource has multiple parents, every List request must specify which parent is primary; requiring two parents simultaneously would make pagination, filtering, and permission checks exponentially more complex.

Many-to-many relationships in relational databases rely on join tables and foreign keys, which do not map cleanly to resource-oriented APIs over network interfaces. The repeated field approach preserves the simplicity of resource-oriented design while still expressing the relationship. The sub-resource approach adds complexity and should be reserved for cases where the relationship itself carries data.

#### Further reading

- [AIP-132](05_operations.md#standard-method-list-aip-132) — Standard Method: List
- [AIP-144](06_fields.md#repeated-fields-aip-144) — Repeated Fields
- [AIP-160](07_design_patterns.md#filtering-aip-160) — Filtering

### 4.5 Enumerations (AIP-126)
[ref: #enumerations-aip-126]

It is common for a field to only accept or provide a discrete and limited set of values. In these cases, it can be useful to use enumerations (generally abbreviated "enums") in order to clearly communicate what the set of allowed values are.

#### Guidance

APIs **may** expose enum objects for sets of values that are expected to change infrequently:

```protobuf
// A representation of a book.
message Book {
  // Other fields...

  // Possible formats in which the book may be published.
  enum Format {
    // Default value. This value is unused.
    FORMAT_UNSPECIFIED = 0;

    // The printed format, in hardback.
    HARDBACK = 1;

    // The printed format, in paperback.
    PAPERBACK = 2;

    // An electronic book format.
    EBOOK = 3;

    // An audio recording.
    AUDIOBOOK = 4;
  }

  // The format of the book.
  Format format = 99;

  // Other fields...
}
```

- All enum values **must** use `UPPER_SNAKE_CASE`.
- The first value of the enum **should** be the name of the enum itself followed by the suffix `_UNSPECIFIED`.
  - An exception to this rule is if there is a clearly useful zero value. In particular, if an enum needs to present an `UNKNOWN`, it is usually clearer and more useful for it to be a zero value rather than having both. The `UNKNOWN` value **may** be prefixed by the enum name as is typical for avoiding enum value name collisions.
- Enums which will only be used in a single message **should** be nested within that message. In this case, the enum **should** be declared immediately before it is used.
  - The non-zero values of such a nested enum definition **should not** be prefixed by the name of the enum itself. This generally requires users to write `MyState.MYSTATE_ACTIVE` in their code, which is unnecessarily verbose.
- Enums which will be used by multiple messages **should** be defined at the package level and **should** be defined at the bottom of the proto file (see AIP-191).
  - Some languages (including C++) hoist enum values into the parent namespace, which can result in conflicts for enums with the same values in the same proto package. To avoid sharing values, APIs **should** prefix package-level enum values with the name of the enum.
- Enums **should** document whether the enum is frozen or they expect to add values in the future.

##### When to use enums

Enums can be more accessible and readable than strings or booleans in many cases, but they do add overhead when they change. Therefore, enums **should** receive new values infrequently. While the definition of "infrequently" may change based on individual use cases, a good rule of thumb is no more than once a year. For enums that change frequently, the API **should** use a string and document the format.

Additionally, enums **should not** be used when there is a competing, widely-adopted standard representation (such as with language codes or media types).

**Note:** If an enumerated value needs to be shared across APIs, an enum **may** be used, but the assignment between enum values and their corresponding integers **must** match.

##### Alternatives

For enumerated values where the set of allowed values changes frequently, APIs **should** use a `string` field instead, and **must** document the allowed values. String fields with enumerated values **should** use `kebab-case` for their values.

For enumerated values where there is a competing, widely-adopted standard representation (generally, but not necessarily, a string), that standard representation **should** be used. This is true even if only a small subset of values are permitted, because using enums in this situation often leads to frustrating lookup tables when trying to use multiple APIs together.

Boolean fields **may** be used in situations where it is clear that no further flexibility will be needed. The default value **must** be `false`.

**Note:** When using protocol buffers, it is impossible to distinguish between `false` and unset. If this is a requirement, an enum **may** be a better design choice (although `google.protobuf.BoolValue` is also available).

#### Further reading

- [AIP-191](09_polish.md#file-and-directory-structure-aip-191) — File and Directory Structure
- [AIP-216](06_fields.md#states-aip-216) — States

> **Agent extension — not part of the AIP standard.** Enum evolution is asymmetric: adding new values is generally safe, while renaming, renumbering, or removing existing values is a breaking change. Always keep a `0` value (`<NAME>_UNSPECIFIED`) so proto3 defaults are explicit rather than silently meaningful, and define enums at package level when more than one message could use them — nested enums collide in generated-code namespaces surprisingly often.

### 4.6 Declarative-Friendly Interfaces (AIP-128)
[ref: #declarative-friendly-interfaces-aip-128]

Many services need to interact with common DevOps tools, particularly those that create and manage network-addressable resources (such as virtual machines, load balancers, database instances, and so on). These tools revolve around the principle of "configuration as code": the user specifies the complete intended landscape, and tooling is responsible for making whatever changes are necessary to achieve the user's specification.

These tools are **declarative**: rather than specifying specific **actions** to take, they specify the desired **outcome**, with the actions being derived based on the differences between the current landscape and the intended one.

Furthermore, there are numerous popular DevOps tools, with more being introduced each year. Integrating hundreds of resource types with multiple tools requires uniformity, so that integration can be automated.

#### Guidance

##### Resources

Resources that are declarative-friendly **must** use only strongly-consistent standard methods for managing resource lifecycle, which allows tools to support these resources generically, as well as conforming to other declarative-friendly guidance (see further reading).

Declarative-friendly resources **should** designate that they follow the declarative-friendly style:

```protobuf
message Book {
  option (google.api.resource) = {
    type: "library.googleapis.com/Book"
    pattern: "publishers/{publisher}/books/{book}"
    style: DECLARATIVE_FRIENDLY
  };

  // Name and other fields...
}
```

##### Reconciliation

If a resource takes time (more than a few seconds) for updates to be realized, the resource **should** include a `bool reconciling` field to disclose that changes are in flight. This field **must** be output only.

A resource **must** set the `reconciling` field to `true` if the current state of the resource does not match the user's intended state, and the system is working to reconcile them. This is regardless of whether the root cause of going into reconciliation was user or system action.

**Note:** Services responding to a `GET` request **must** return the resource's current state (not the intended state).

##### Further reading

A significant amount of guidance is more strict for declarative-friendly interfaces, due to the focus on automation on top of these resources. This list is a comprehensive reference to declarative-friendly guidance in other AIPs:

- Resources **should not** employ custom methods: see [AIP-136](05_operations.md#custom-methods-aip-136).
- Resources **must** use the `Update` method for repeated fields: see [AIP-144](06_fields.md#repeated-fields-aip-144).
- Resources **must** include certain standard fields: see [AIP-148](06_fields.md#standard-fields-aip-148).
- Resources **must** have an `etag` field: see [AIP-154](07_design_patterns.md#resource-freshness-validation-aip-154).
- Resources **should** provide change validation: see [AIP-163](07_design_patterns.md#change-validation-aip-163).
- Resources **should not** implement soft-delete. If the ID cannot be re-used, the resource **must** implement soft-delete and the undelete RPC: see [AIP-164](07_design_patterns.md#soft-delete-aip-164).

##### Annotations

For declarative-friendly annotations, see [AIP-148](06_fields.md#standard-fields-aip-148).

> **Agent extension — not part of the AIP standard.** Declarative clients (Terraform, Kubernetes controllers) live or die on two properties: `Get` must return the actual current state rather than the intended state, and long-running updates must surface an output-only `reconciling` boolean so the client knows the system is still converging. The two classic failure modes are persistent drift (server-injected defaults in `Get` responses that the user never configured) and read-after-write inconsistency (an update not visible in the immediately following `Get`), both of which make IaC tools report phantom changes.

### 4.7 Server-Modified Values and Defaults (AIP-129)
[ref: #server-modified-values-and-defaults-aip-129]

Services often provide default values for resource fields, and occasionally normalize the user input before returning it in the response. The guidance herein describes how services document such behavior for the benefit of consumers.

#### Guidance

##### Single owner fields

Fields **must** have a single owner, whether that is the client or the server. Server-owned fields **must** be indicated with the `OUTPUT_ONLY` field behavior. All other types of fields **must** be considered to be owned by the client. The server **must** respect the value (or lack thereof) for all client-owned fields and not modify them.

##### Effective values

There are instances where a service will allocate, generate, or calculate a value if the client chooses not to specify one. For example: a client creates a virtual machine without specifying a static IP address for the virtual machine to be available on. Such a scenario is opting into dynamic IP address allocation.

Some examples of these types of fields are ones that are:

- **generated** (UUID)
- **allocated** (dynamic IP address)
- **assigned** (most recent software package version)

An attribute with an effective value **must** be expressed as two fields in the API:

- a mutable field that can be optionally set by the user and **must not** be modified by the service
- an `OUTPUT_ONLY` field that records the effective value decided on by the service

Example:

```protobuf
message VirtualMachine {
  // ...
  string ip_address = 4;
  string effective_ip_address = 5 [
    (google.api.field_behavior) = OUTPUT_ONLY
  ];
}
```

###### Naming

Effective values **must** be named by prefixing `effective_` to the mutable field's name.

##### User-specified fields

For user-specified fields, the value in response from the service **must** be the same as provided by the create or update request. For string fields this means returning the value unchanged, with one exception:

- When a string field has a data type annotation, a normalized string that represents the given value **may** be returned.

##### Normalizations

A field that is normalized by the service **must** be annotated with the `google.api.field_info` extension. See [AIP-202](06_fields.md#fields-and-fieldinfo-aip-202) for guidance on using this extension. The allowed set of normalizations includes the following formats:

- `uuid`
- `ipv4`
- `ipv6`
- `email`

Normalizations on fields **must** be described using the `google.api.field_info` annotation.

#### Rationale

Server-modified and default values often make it harder to implement declarative clients. These clients are often unable to tell when their desired state matches the current state for these fields, as the rules by which a server may modify and return values are complex, not public, and not repeatable.

##### Rationale for single owner fields

When fields do not have a single owner they can cause issues for declarative clients. These clients may attempt to set values for fields that are overwritten by server-set values, leading to the client entering an infinite loop to correct the change.

##### Rationale for naming

Consistent naming is important for identifying standard behavior across APIs and fields. Programmatic association between user-specified and effective values depends on consistent naming.

##### Rationale for normalizations

Normalizations are important to allow services to store and return values in a standard way while communicating to clients what changes are semantically identical. Normalizing a value on the service side allows the service to accept a wider range of semantically identical inputs without needing to maintain every value as a raw string. Surfacing the normalization that is being applied to clients allows for client-side comparison of sent and retrieved values to check for differences.

For example, in a resource that accepts an email address on a particular field, a client may specify a given email address in a variety of ways. For the email `ada@example.com` a client may choose to specify `ADA@example.com`, `aDa@example.com`, or `AdA@example.com`. These are semantically identical and **should** all be accepted by the service. The service then may choose to normalize the email address for storage and retrieval through downcasing or canonicalization. Importantly, the information surfaced to clients on the normalization of a field will not describe the normalization algorithm itself, but instead the comparison method used to accurately compute if two values should be considered equal.

##### Rationale for field value handling

For fields not using an allowed normalization, declarative clients will not be able to identify which changes are semantically meaningful. When a declarative client sends a particular value it will ensure that the value is being returned by the service to validate it was set correctly.

#### Further reading

- [AIP-128](04_resource_design.md#declarative-friendly-interfaces-aip-128) — Declarative-Friendly Interfaces
- [AIP-202](06_fields.md#fields-and-fieldinfo-aip-202) — Fields and FieldInfo

> **Agent extension — not part of the AIP standard.** Server-owned values must be marked output-only; if a declarative client echoes a server-populated field back in an update, strict services correctly reject it. Input normalization (canonicalizing case, shortening CIDR blocks) is the subtle cousin: if the server rewrites input without documenting it, the client's next plan diff shows a phantom change. AIP-129 was substantially clarified in 2023 around field ownership precisely to make these drift sources explicit.

### 4.8 Singleton Resources (AIP-156)
[ref: #singleton-resources-aip-156]

APIs sometimes need to represent a resource where exactly one instance of the resource always exists within any given parent. A common use case for this is for a config object.

#### Guidance

An API **may** define **singleton resources**. A singleton resource **must** always exist by virtue of the existence of its parent, with one and exactly one per parent.

For example:

```protobuf
message Config {
  option (google.api.resource) = {
    type: "api.googleapis.com/Config"
    pattern: "users/{user}/config"
    singular: "config"
    plural: "configs"
  };

  // additional fields including name
}
```

The `Config` singleton would have the following RPCs:

```protobuf
rpc GetConfig(GetConfigRequest) returns (Config) {
  option (google.api.http) = {
    get: "/v1/{name=users/*/config}"
  };
}

rpc UpdateConfig(UpdateConfigRequest) returns (Config) {
  option (google.api.http) = {
    patch: "/v1/{config.name=users/*/config}"
    body: "config"
  };
}
```

- Singleton resources **must not** have a user-provided or system-generated ID; their resource name includes the name of their parent followed by one static segment.
  - Example: `users/1234/config`
- Singleton resources are always singular.
  - Example: `users/1234/thing`
- Singleton resource definitions **must** provide both the `singular` and `plural` fields (see above example).
- Singleton resources **may** parent other resources.
- Singleton resources **must not** define the `Create` or `Delete` standard methods. The singleton is implicitly created or deleted when its parent is created or deleted.
- Singleton resources **should** define the `Get` and `Update` methods, and **may** define custom methods as appropriate.
  - However, singleton resources **must not** define the `Update` method if all fields on the resource are output only.
- Singleton resources **may** define the `List` method, but **must** implement it according to AIP-159. See the example below.
  - The trailing segment in the path pattern that typically represents the collection **should** be the `plural` form of the singleton resource, e.g., `/v1/{parent=users/*}/configs`.
  - If a parent resource ID is provided instead of the hyphen `-` as per AIP-159, then the service **should** return a collection of one singleton resource corresponding to the specified parent resource.

```protobuf
rpc ListConfigs(ListConfigsRequest) returns (ListConfigsResponse) {
  option (google.api.http) = {
    get: "/v1/{parent=users/*}/configs"
  };
}

message ListConfigsRequest {
  // To list all configs, use `-` as the user id.
  // Formats:
  // * `users/-`
  // * `users/{user}`
  //
  // Note: Specifying an actual user id will return a collection of one config.
  // Use GetConfig instead.
  string parent = 1 [
    (google.api.resource_reference).child_type = "api.googleapis.com/Config"];

  // other standard pagination fields...
}
```

#### Rationale

##### Support for standard list

While singleton resources are not directly part of a collection themselves, they can be viewed as part of their parent's collection. The one-to-one relationship of parent-to-singleton means that for every one parent there is one singleton instance, naturally enabling some collection-based methods when combined with the pattern of reading across collections. The singleton can present as a collection to the API consumer as it is indirectly one based on its parent. Furthermore, presenting the singleton resource as a pseudo-collection in such methods enables future expansion to a real collection, should a singleton be found lacking.

##### Including `plural` definition

While a singleton is by definition singular, there are certain cases where a singleton resource may appear in a plural form, e.g., if the service supports standard list (as defined here). As such, it is better to forward declare the plural form of the singleton resource type than to not have it when needed.

#### Further reading

- [AIP-131](05_operations.md#standard-method-get-aip-131) — Standard Method: Get
- [AIP-134](05_operations.md#standard-method-update-aip-134) — Standard Method: Update
- [AIP-159](07_design_patterns.md#reading-across-collections-aip-159) — Reading Across Collections

> **Agent extension — not part of the AIP standard.** Singleton names use a constant final segment instead of an ID (for example `projects/{project}/config`), and since the 2024 revision singleton resource definitions must still declare both `singular` and `plural` names even though only one instance exists. Deleting the parent is expected to clean up the singleton — orphaned singletons become unreachable but continue to exist. Collection-oriented lint rules sometimes misfire on singletons; treat those findings as candidates for a documented `aip.dev/not-precedent` disable.

### 4.9 Policy Preview (AIP-236)
[ref: #policy-preview-aip-236]

A policy is a resource that provides rules that admit or deny access to other resources. Generally, the outcome of a policy can be evaluated to a specific set of outcomes.

Changes to policies without proper validation may have unintended consequences that can severely impact a customer's overall infrastructure setup. To safely update resources, it is beneficial to test these changes via policy rollout APIs.

Preview is a rollout safety mechanism for policy resources, which gives the customer the ability to validate the effect of their proposed changes against production traffic prior to the changes going live. The result of the policy evaluation against traffic is logged in order to give the customer the data required to test the correctness of the change.

Firewall policies exemplify a case that is suitable for previewing. A new configuration can be evaluated against traffic to observe which IPs would be allowed or denied. This gives the customer the data to guide a decision on whether to promote the proposed changes to live.

The expected flow for previewing a policy is as follows:

1. The user creates an experiment containing a new policy configuration intended to replace the live policy.
2. The user uses the `startPreview` method to start generating logs which compare the live and experiment policy evaluations against live traffic.
3. The user inspects the logs to determine whether the experiment has the intended result.
4. The user uses the `commit` method to promote the experiment to live.

#### Guidance

##### Non-goals

This proposal is for a safety mechanism for policy rollouts only. Safe rollouts for non-policy resources are not in scope.

##### Experiments

A new configuration of a policy to be previewed is stored as a nested collection under the policy. These nested collections are known as experiments.

A hypothetical policy resource called `Policy` is used throughout. It has the following resource name pattern:

```
projects/{project}/locations/{location}/policies/{policy}
```

The experimental versions of the resource used for previewing or other safe rollout practices are represented as a nested collection under `Policy` using a new resource type. The resource type **must** follow the naming convention: *RegularResourceType* `Experiment`.

The following pattern is used for the experiment collection:

```
projects/{project}/locations/{location}/policies/{policy}/experiments/{experiment}
```

A proto used to represent an experiment **must** contain the following:

1. The required top-level fields for a resource, like `name` and `etag`.
2. The policy message that is being tested itself.
3. The field, `preview_metadata`, which contains metadata specific to previewing the experiment of a specific resource type.

```protobuf
message PolicyExperiment {
  // google.api.resource, name, and other annotations and fields

  // The policy experiment. This Policy will be used to preview the effects of
  // the change but will not affect live traffic.
  Policy policy = 2;

  // The metadata associated with this policy experiment.
  PolicyPreviewMetadata preview_metadata = 3
      [(google.api.field_behavior) = OUTPUT_ONLY];

  // Allows clients to store small amounts of arbitrary data.
  map<string, string> annotations = 4;
}
```

- The experiment proto **must** have a top-level field with the same type as the live policy.
  - It **must** be named as the live resource type. For example, if the experiment is for `FirewallPolicy`, then this field **must** be named `firewall_policy`.
  - The name inside the embedded `policy` message **must** be the name of the live policy.
- When the user is ready to promote an experiment, they **must** copy the `policy` message into the live policy and delete the experiment. This can be done manually or via a `commit` custom method.
- A product **may** support multiple experiments concurrently being previewed for a single live policy.
  - Each experiment must generate logs having each entry preceded by `log_prefix` so that the user can compare the results of the experiment with the behavior of the live policy.
  - The number of experimental configurations for a given live policy **may** be capped at a certain number and the cap **must** be documented.
- Cascading deletes **must** occur: if the live policy is deleted, all experiments **must** also be deleted.
- `map<string, string>` annotations **must** allow clients to store small amounts of arbitrary data.

##### Metadata

`preview_metadata` tracks all metadata of previewing the experiment. The messages **must** follow the convention: *RegularResourceType* `PreviewMetadata`. This is so the proto can be defined uniquely for each resource type in the same service with experiments.

```protobuf
message PolicyPreviewMetadata {
  // Possible values of the state of previewing the experiment.
  enum State {
    // Default value. This value is unused.
    STATE_UNDEFINED = 0;

    // The experiment is actively previewing.
    ACTIVE = 1;

    // The previewing of the experiment has been stopped.
    SUSPENDED = 2;
  }

  // The state of previewing the experiment.
  State state = 1;

  // An identifying string common to all logs generated when previewing the
  // experiment. Searching all logs for this string will isolate the results.
  string log_prefix = 2;

  // The most recent time at which this experiment started previewing.
  google.protobuf.Timestamp start_time = 3;

  // The most recent time at which this experiment stopped previewing.
  google.protobuf.Timestamp stop_time = 4;
}
```

- `PolicyPreviewMetadata` **must** have the fields defined in the proto above.
  - It **may** have additional fields if the service or resource requires it.
- When an experiment is first previewed, `preview_metadata` **must** be absent.
  - It is present on the experiment once the `startPreview` method is used.
- All `preview_metadata` fields **must** be output only.
- `state` changes between `ACTIVE` and `SUSPENDED` when previewing is started or stopped. This happens when the `startPreview` or `stopPreview` custom methods are invoked, respectively.
- The first time the `startPreview` custom method is used, the system **must** create `preview_metadata` and do the following:
  - It **must** set the `state` to `ACTIVE`.
  - It **must** populate `start_time` with the current time.
    - `start_time` **must** be updated every time `state` is changed to `ACTIVE`.
  - It **must** set a system-generated `log_prefix` string, which is a predefined constant hard coded by the system developers.
  - The same value is used for previewing experiments for the given resource type. For example, `"FirewallPolicyPreviewLog"` for `FirewallPolicy`.
- When the `stopPreview` custom method is used, the system **must** do the following:
  - It **must** set the `state` to `SUSPENDED`.
  - It **must** populate the `stop_time` with the current time.

##### Methods

###### Create

- The resource **must** be created using long-running `Create` and `google.longrunning.operation_info.response_type` **must** be `PolicyExperiment`.
- Creating a new experiment to preview **must** support the following use cases:
  - Preview a new policy.
  - Preview an update to an already live policy.
  - Preview a deletion of a current policy.
- For the update and delete use cases, the `policy` field in the experiment **must** have the full payload of the live policy copied into it, including the name.
  - The user **must** set the rules to the new intended state to preview an update.
  - The user **must** set the rules to represent a no-op to preview a delete.
- To preview a new policy, the system must do the following:
  - If the system does not support a nested collection without a live policy, the user **must** create a live policy and set the rules to represent a no-op. For example, the rules of a no-op policy **may** be empty.
    - An experiment is created as a child of the no-op policy.
- If the system supports previewing multiple experiments for a live policy, calling `create` more than once **must** create multiple experiments.

###### Update

- The resource **must** be updated using long-running `Update` and `google.longrunning.operation_info.response_type` **must** be `PolicyExperiment`.
- The name inside `policy` **must not** change but the other fields can in order to change the experiment being previewed because this `policy` is intended to replace the live policy, and the name of the live policy **must not** change.
- The system **must** set the `state` to `SUSPENDED` if the `state` was `ACTIVE` at the time of an update.
  - This is so the user can easily distinguish between different versions of the experiment being previewed.

###### Get

- The standard method, `Get`, **must** be included for `PolicyExperiment` resource types.

###### List

- The standard method, `List`, **must** be included for `PolicyExperiment` resource types.
- Filtering on `PolicyPreviewMetadata` indicates which experiments are actively previewed.
  - For example, the following filter string returns a `List` response with experiments being previewed: `preview_metadata.state = ACTIVE`.

###### Delete

- The resource **must** be deleted using long-running `Delete` and `google.longrunning.operation_info.response_type` **must** be `PolicyExperiment`.

###### startPreview

```protobuf
// Starts previewing a PolicyExperiment. This triggers the system to start
// generating logs to evaluate the PolicyExperiment.
rpc StartPreviewPolicyExperiment(StartPreviewPolicyExperimentRequest)
    returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{name=policies/*/experiments/*}:startPreview"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "PolicyExperiment"
    metadata_type: "StartPreviewPolicyExperimentMetadata"
  };
}

// The request message for the startPreview custom method.
message StartPreviewPolicyExperimentRequest {
  // The name of the PolicyExperiment.
  string name = 1;
}
```

- This custom method is required.
- `google.longrunning.Operation.metadata_type` **must** follow guidance on long-running operations.
- This method **must** trigger the system to start generating logs to preview the experiment.
- Whenever the method is called successfully, the system **must** set the following values in the `PolicyPreviewMetadata`:
  - `log_prefix` to the predefined constant.
  - `start_time` to the current time.
  - `state` to `ACTIVE`.
- If the method is called on an experiment with the rules representing a no-op, then the system **must** preview the deletion of the live policy.

###### stopPreview

```protobuf
// Stops previewing a PolicyExperiment. This triggers the system to stop
// generating logs to evaluate the PolicyExperiment.
rpc StopPreviewPolicyExperiment(StopPreviewPolicyExperimentRequest)
    returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{name=policies/*/experiments/*}:stopPreview"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "PolicyExperiment"
    metadata_type: "StopPreviewPolicyExperimentMetadata"
  };
}

// The request message for the stopPreview custom method.
message StopPreviewPolicyExperimentRequest {
  // The name of the PolicyExperiment.
  string name = 1;
}
```

- This custom method is required.
- `google.longrunning.Operation.metadata_type` **must** follow guidance on long-running operations.
- This method **must** trigger the system to stop generating logs to preview the experiment.
- Whenever the method is called successfully, the system **must** set the following values in the `PolicyPreviewMetadata`:
  - `stop_time` to the current time.
  - `state` to `SUSPENDED`.

###### commit

The resource **may** expose a new custom method called `commit` to promote an experiment. The system copies `policy` from the experiment into the live policy and then deletes the experiment.

Declarative clients **may** manually copy fields from an experiment into the live policy and then delete the experiment rather than calling `commit` if preferable.

```protobuf
// Commits a PolicyExperiment. This copies the PolicyExperiment's policy message
// to the live policy then deletes the PolicyExperiment.
rpc CommitPolicyExperiment(CommitPolicyExperimentRequest)
    returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{name=policies/*/experiments/*}:commit"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "google.protobuf.Empty"
    metadata_type: "CommitPolicyExperimentMetadata"
  };
}

// The request message for the commit custom method.
message CommitPolicyExperimentRequest {
  string name = 1;
  string etag = 2;
  string parent_etag = 3;
}
```

- `google.longrunning.Operation.metadata_type` **must** follow guidance on long-running operations.
- The method **must** atomically copy `policy` from the experiment into the live policy, and then delete the experiment.
- If any experiment fails `commit`, previewing it **must not** stop, and the live policy **must not** be updated.
- The method can be called on an experiment in any state.
- The `etag` **must** match that of the experiment in order for commit to be successful. This is so the user does not commit an unintended version of the experiment.
  - If no `etag` is provided, the API **must not** succeed to prevent the user from unintentionally committing a different version of the experiment as intended.
  - A `parent_etag` **may** be provided to guarantee that the experiment overwrites a specific version of the live policy.
- The method is not idempotent and calling it twice on the same experiment **must** return a `404 NOT_FOUND` as the experiment is deleted as part of the first call.

##### Changes to live policy API methods

###### Delete

- A delete of the live policy **must** delete all experiments.
- To maintain the experiments while negating the effect of the live policy, the live policy **must** be changed to a no-op policy instead of using this method.

##### Logging

Logging is crucial for the user to evaluate whether an experiment should be promoted to live.

Logs **must** contain the results of the evaluated experiment, the `etag` associated with that experiment alongside that of the live policy, and be preceded by the value of `log_prefix`.

- The `etag` fields help the user identify which configurations of the live and experiment are evaluated in the log.
- `log_prefix` helps the user separate logs specifically generated for previewing the experiment from other use cases.

Overall, these logs help the user make a decision about whether to promote the experiment to live.

#### Rationale

Policy resources govern access and permissions; an incorrect policy change can lock out legitimate users or expose sensitive resources. Preview provides a safe mechanism to validate changes against real traffic without affecting live behavior. The experiment-as-nested-resource pattern allows multiple concurrent experiments, version tracking via `etag`, and clean promotion or discard workflows.

#### Further reading

- [AIP-135](05_operations.md#standard-method-delete-aip-135) — Standard Method: Delete
- [AIP-151](05_operations.md#long-running-operations-aip-151) — Long-Running Operations
- [AIP-160](07_design_patterns.md#filtering-aip-160) — Filtering

> **Agent extension — not part of the AIP standard.** A policy preview is only useful if it is fast enough to gate a rollout: return or log the predicted outcome synchronously so that CI and IaC pipelines can block a dangerous change automatically (firewall and IAM policies are the canonical cases). Treat the preview as a dry-run contract — its result must match what the real apply would do, or users learn to ignore it.
