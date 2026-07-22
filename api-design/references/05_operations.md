---
subject: "Method design and execution corpus; `AIP-130` category ladder, standard methods `AIP-131` get `AIP-132` list pagination `AIP-133` create user IDs `AIP-134` update masks `AIP-135` delete, `AIP-136` custom verbs naming, `AIP-151` LRO operation metadata, batch `AIP-231` atomic get `AIP-233` create `AIP-234` update `AIP-235` delete partial-success `failed_requests`."
index:
  - anchor: method-categories-aip-130
    what: "The AIP-130 category ladder (standard, then batch or aggregate, then custom, then streaming) mapping each method shape to its automatibility across declarative clients, CLIs, UIs, and SDKs."
    problem: "Method designed by habit as streaming or free-form RPC before checking simpler categories, so declarative clients and CLIs cannot automate it and every consumer hand-writes integration; category priority order, automatibility matrix, client integration breadth, premature streaming, ad-hoc rpc shape, uniformity spectrum, handwritten fallback."
    use_when: "Fresh method under design and category undecided; tempted to reach for streaming first; auditing surface for automation-hostile shapes; explaining why mutation sits outside declarative reach."
    avoid_when: "Concrete field layout of chosen standard verb needed (05_operations › standard methods); LRO mechanics at stake; category already fixed and only naming remains."
    expected: "Every method occupies simplest viable category, standard shapes cover CRUD, custom verbs mount to resources or collections, and streaming appears only where nothing simpler fits."
  - anchor: standard-method-get-aip-131
    what: "The AIP-131 fetch contract: mandatory `Get<Resource>` RPC returning the bare resource itself over HTTP GET with lone `name` path variable, no request body, and `method_signature` of `\"name\"`."
    problem: "Resource exists but cannot be read back by name through uniform shape, so clients wrap fetches in bespoke response envelopes and orchestration cannot validate state after mutation; unreadable resource, custom read wrapper, single name variable, unwrapped result, post-mutation validation, query-parameter spill, read consistency baseline."
    use_when: "Any resource lacking fetch RPC; wiring REST gateway for retrieval; deciding whether wrapper message justified (it is not); keeping request free of extra required fields."
    avoid_when: "Collection retrieval wanted (05_operations › list); several resources fetched atomically (05_operations › batch get); partial field selection needed (07_design_patterns › partial responses)."
    expected: "Each resource retrievable through uniform `Get` RPC, response carries fully-populated resource directly, and post-mutation reads confirm steady state."
  - anchor: standard-method-list-aip-132
    what: "The AIP-132 collection read contract: `List<Resources>` over HTTP GET on the parent path with mandatory `page_size`/`page_token`/`next_page_token`, optional `filter`/`order_by`/`show_deleted`, and `total_size` caveats."
    problem: "Collection endpoint ships without pagination and later retrofits tokens, filters, ordering as breaking field additions, so early clients page through entire datasets and upgrades break them; retrofit breaking change, page token choreography, unbounded dataset dump, filter ordering afterthought, soft-deleted visibility, coerced page size, consistent snapshot paging."
    use_when: "Collection needs enumeration endpoint; pagination trio being wired for first time; weighing whether sorting or filtering justified now versus later; soft-delete visibility toggle needed."
    avoid_when: "Single-resource fetch (05_operations › get); cross-collection reading (07_design_patterns › reading across collections); exact count guarantee assumed from `total_size` estimate; ordering removed from shipped API (breaking)."
    expected: "Lists page deterministically with token contract, filtering and sort behavior documented from day one, soft-deleted entries hidden unless requested, and oversized page requests coerce to documented maximum."
  - anchor: standard-method-create-aip-133
    what: "The AIP-133 creation contract: `Create<Resource>` POSTs to the parent collection returning the new resource, caller-assigned `{resource}_id` living on the request (mandatory on management plane), and `ALREADY_EXISTS`/`PERMISSION_DENIED` duplicate handling."
    problem: "Server mints identifiers for management-plane resources, so declarative clients cannot precalculate names, retries spawn duplicates, and every referencing resource chases newly assigned ID; service-side id minting, replayed submission clone, predictable resource naming, caller-assigned id field, reference cascade churn, already-exists signaling, idempotency by construction."
    use_when: "Creation endpoint under design; deciding where ID input lives (request, never resource message); duplicate submission handling being pinned; declarative reachability of fresh resources required."
    avoid_when: "Row-like data without disambiguation need (system IDs acceptable on data plane); modification of existing resource (05_operations › update); creation exceeding unary timeout (05_operations › long-running operations)."
    expected: "Creations accept caller-assigned IDs on request messages, retries with identical ID yield `ALREADY_EXISTS` not duplicates, and references resolve final names before submission."
  - anchor: standard-method-update-aip-134
    what: "The AIP-134 mutation contract: `Update<Resource>` PATCHes `{resource}.name` with explicit `google.protobuf.FieldMask update_mask` (omitted mask implies populated fields, `*` means full replacement), side-effect-free semantics, plus `allow_missing` upsert and etag concurrency options."
    problem: "Full-replacement PUT semantics meet resource evolution, so old clients silently wipe fields added after their schema shipped and state transitions hide inside plain mutations; field-wiping put trap, mask-omission ambiguity, wildcard replacement hazard, hidden side effect, state field writability, upsert flag semantics, etag race guard."
    use_when: "Modification semantics under design; mask behavior for omitted or `*` values being pinned; field change tempted to trigger larger process (05_operations › custom methods); concurrent-writer protection via etag needed."
    avoid_when: "Creation of absent resource as primary goal without client-assigned names; significant process triggers intended (05_operations › custom methods); PUT-only replacement considered (later field additions break old clients)."
    expected: "Mutations apply exactly masked fields, absent mask covers populated values only, state stays non-writable, and concurrent writers detect races through etag `ABORTED`."
  - anchor: standard-method-delete-aip-135
    what: "The AIP-135 removal contract: `Delete<Resource>` over HTTP DELETE without body, `google.protobuf.Empty` response (or the resource for soft delete), `force` opt-in for cascading removal with `FAILED_PRECONDITION` guard, and etag or `allow_missing` options."
    problem: "Removal endpoint returns bare Empty forever and children block deletion inconsistently, so later need to convey removed payload forces breaking redesign and accidental child wipes destroy unrecoverable data; empty response foreclosure, cascading wipe hazard, explicit force gate, failed-precondition guard, soft-delete marker response, child existence blocking, protected removal etag."
    use_when: "Deletion contract being drafted; response payload choice made before launch; parent with children needs guarded cascade; absent-resource retries should no-op via flag."
    avoid_when: "Bulk filter-driven removal (07_design_patterns › criteria-based delete); soft-delete lifecycle with undelete (07_design_patterns › soft delete); singleton children assumed to block (they must not)."
    expected: "Deletion returns deliberately chosen payload, child presence vetoes removal until `force` set, singletons follow parent automatically, and repeated absent-target calls behave per documented flag."
  - anchor: custom-methods-aip-136
    what: "The AIP-136 escape hatch: custom RPCs (Archive, Publish, Cancel) for intent that CRUD cannot express, mounted on resource, collection, or scope, kept away from declarative-friendly resources except rare imperative operations like `Move`."
    problem: "Designer contorts standard verbs to approximate action like state transition, so semantics blur and clients misread side effects, or sprouts bespoke RPC where plain CRUD sufficed; action intent mismatch, intent-verb mapping, side effect transparency, crud overfit, declarative automation loss, workflow trigger action, imperative escape rarity."
    use_when: "User intent names an operation beyond CRUD vocabulary (publish, archive, cancel); mutation targets resource yet breaks standard semantics; rarely-used imperative relocation like `Move` justified; fetch across collection inexpressible via List."
    avoid_when: "Plain field update achieves goal (05_operations › update); standard verb merely feels awkward; declarative-friendly resource would adopt custom verb casually; significant duration involved (pair with LRO)."
    expected: "Every non-CRUD action rides purpose-built RPC mounted at correct level, CRUD vocabulary keeps clean semantics, and declarative surfaces stay free of unautomatable operations."
  - anchor: custom-methods-aip-136
    what: "The AIP-136 naming and mapping grammar: verb-noun RPC names without prepositions or `Async` (`LongRunning` suffix instead), GET for reads and POST for mutations, `:customVerb` URI suffix in camelCase, `body: \"*\"`, and `Request`/`Response` message suffixes."
    problem: "Custom RPC named with preposition or async marker and mapped to wrong HTTP shape, so client generators choke, faux collection segments confuse routing, and method families bloat with hyper-focused variants; preposition name sprawl, async suffix confusion, colon verb mapping, route ambiguity, verb selection get-post, wildcard body mapping, vocabulary explosion."
    use_when: "Coining name for justified custom RPC; picking HTTP verb from mutation behavior; structuring URI with colon suffix; deciding message names for request and response pair."
    avoid_when: "Justification for custom RPC itself unsettled (sibling card); standard-method mapping at stake; preposition-shaped name signaling missing field instead of method."
    expected: "Names read as crisp verb-noun pairs, reads use GET and mutations POST, URIs end with colon-suffixed action, and generators produce clean client surface."
  - anchor: long-running-operations-aip-151
    what: "The AIP-151 promise pattern: slow RPCs return `google.longrunning.Operation` immediately, clients poll the uniform `Operations` service, resources signal unusable interim state, and parallel attempts fail `ABORTED` or queue."
    problem: "Unary call blocks for minutes while provisioning finishes, so gateways time out, clients invent polling endpoints per service, and user stares at frozen request; unary timeout wall, hanging call experience, promise token pattern, per-service polling invention, mid-provisioning limbo, parallel operation abort, thirty-day expiry."
    use_when: "Work routinely exceeds ten-second rule of thumb; provisioning or fleet-scale mutation underway; clients need progress visibility mid-flight; concurrent operation attempts must reject cleanly."
    avoid_when: "Sub-second latency typical; response and metadata type design at stake (sibling card); streaming better fits continuous output."
    expected: "Slow calls hand back operation handle instantly, progress polls hit uniform service, interim resources signal pending status, and conflicting concurrent attempts abort loudly."
  - anchor: long-running-operations-aip-151
    what: "The AIP-151 `operation_info` design-time decisions: `response_type` and `metadata_type` frozen once shipped (changing either breaks clients), named empty messages instead of `google.protobuf.Empty` to keep future doors open, and validate-only mode returning done or polling operations."
    problem: "Annotation types chosen casually at launch and result payload needed later, so changing declared types becomes breaking change and Empty-typed operations can never return data; frozen type annotation, breaking type swap, stub message placeholder, future payload headroom, metadata progress channel, dry-run request handling, done flag semantics."
    use_when: "Declaring `operation_info` for first time; result data plausibly needed post-launch; progress or partial-failure reporting anticipated; validation-only requests must produce uniform handles."
    avoid_when: "Blocking behavior question itself (sibling card); types already shipped and change contemplated (breaking, needs new RPC); Delete-only flow where Empty genuinely final."
    expected: "Operations declare named types with growth room, validation returns done handles immediately, metadata streams progress while pending, and shipped annotations never mutate."
  - anchor: batch-method-get-aip-231
    what: "The AIP-231 atomic batch read: `BatchGet<Resources>` over GET with `:batchGet` suffix taking repeated `names`, all-or-nothing semantics (no per-item errors, no pagination), response order mirroring request."
    problem: "Bulk read endpoint invented with per-item error channel and pagination, so consistent-time-point snapshot guarantee dissolves and partial results masquerade as complete reads; all-or-nothing reads, itemized failure invention, transactional read boundary, positional response parity, pagination exclusion, wildcard parent dash, hoisted get fields."
    use_when: "Consistent multi-resource snapshot needed (read transaction); caller tolerates total failure on any miss; results must track request sequence; batch ceiling documented near thousand."
    avoid_when: "Missing resources acceptable (filtered List fits better); partial results desired; huge unbounded result sets requiring pages."
    expected: "Batch reads succeed wholly or fail wholly, responses preserve request order, and per-entry error channels or paging tokens never creep in."
  - anchor: batch-method-create-aip-233
    what: "The AIP-233 batch creation pattern: `BatchCreate<Resources>` POSTs repeated child `requests`, synchronous variant always atomic, asynchronous variant optionally partial via `map<int32, google.rpc.Status> failed_requests` keyed by child index."
    problem: "Bulk creation reports bare success while individual entries quietly fail, so caller believes entire batch persisted and retry logic duplicates what actually committed; silent per-entry failure, ok-implies-all fallacy, synchronous atomicity mandate, positional error map, hoisting unique-field ban, legacy partial retrofit, transient retry exclusion."
    use_when: "Bulk insertion endpoint justified; sync-versus-async shape being chosen against atomicity cost; per-item outcome reporting designed; legacy batch API adopting partial behavior (`return_partial_success` gate)."
    avoid_when: "Read snapshot wanted (05_operations › batch get); per-child unique fields hoisted (forbidden, caller IDs); partial adoption grafted onto shipped sync surface (requires new version)."
    expected: "Sync batches commit atomically, async partial mode reports failures by child position, total failure surfaces `Aborted` on operation error, and retries never duplicate committed entries."
  - anchor: batch-method-update-aip-234
    what: "The AIP-234 batch mutation pattern: `BatchUpdate<Resources>` carrying per-child `UpdateBookRequest` entries each with own `update_mask`, optional hoisted mask as convenience, and identical partial-success machinery to AIP-233."
    problem: "Bulk modification applies one shared field mask across heterogeneous items, so fields vanish on entries where mask mismatches and per-item outcomes stay invisible behind aggregate success; uniform mask misfit, heterogeneous entry sets, hidden entry results, per-child mask semantics, collective success smokescreen, mask hoisting convenience, partial machinery reuse."
    use_when: "Mass modification endpoint justified; each child entry carries distinct field set; uniform edit set might share one mask; outcome granularity per item required."
    avoid_when: "Identical mask truly fits every entry (hoist it); insertion rather than modification (05_operations › batch create); per-child unique values hoisted (forbidden)."
    expected: "Every child entry honors its own mask, common mask applies only where child omits one, and per-item failures surface through documented status map."
  - anchor: batch-method-delete-aip-235
    what: "The AIP-235 batch removal pattern: `BatchDelete<Resources>` via POST `:batchDelete` (never HTTP DELETE) taking repeated `names`, filter-based matching prohibited, soft-delete variant returning updated resources, absent-target semantics documented."
    problem: "Bulk removal exposed through filter matching and undefined absent-target behavior, so one loose predicate wipes swaths of production data and retried partial batches cannot tell success from gaps; predicate mass wipe, criteria deletion ban, absent-target ambiguity, retry gap confusion, post-not-delete verb, names-only requests, soft-delete bulk response."
    use_when: "Many resources removed together; deciding how already-absent entries count (document explicitly); soft-deleted bulk payload needed; idempotent retry of partially failed batch must work."
    avoid_when: "Criteria-driven mass removal tempting (prohibited; 07_design_patterns › criteria-based delete if truly unavoidable); HTTP DELETE verb mapped (POST required); single-resource removal (05_operations › delete)."
    expected: "Batch removal takes explicit name lists only, absent entries follow documented success-or-failure rule, soft-delete variant returns marked resources, and partial failures report per documented map."
aips: [130, 131, 132, 133, 134, 135, 136, 151, 231, 233, 234, 235]
---

# Operations

## 5. Operations

### 5.1 Method Categories (AIP-130)
[ref: #method-categories-aip-130]

An API is composed of one or more methods, which represent a specific operation that a service can perform on behalf of the consumer.

**Categories of Methods**

| Category Name | Related AIPs | Declarative client integration | CLI / UI integration | SDK integration |
|---|---|---|---|---|
| _Standard Methods_ | | | | |
| **Standard collection methods**: operate on a collection of resources (List or Create). | AIP-121, AIP-132, AIP-133 | automatable | automatable | automatable |
| **Standard resource methods**: fetch or mutate a single resource (Get, Update, Delete). | AIP-121, AIP-131, AIP-134, AIP-135 | automatable | automatable | automatable |
| **Batch resource methods**: fetch or mutate multiple resources in a collection by name. | AIP-231, AIP-233, AIP-234, AIP-235 | may be used to optimize queries | automatable | automatable |
| **Aggregated list methods**: fetch or mutate multiple resources of the same type across multiple collections. | AIP-159 | not useful nor automatable | automatable | automatable |
| _Custom Fetch Methods_ | | | | |
| **Custom collection fetch methods**: fetch information across a collection that cannot be expressed via a standard method. | AIP-136 | handwritten | automatable | automatable |
| **Custom resource fetch methods**: fetch information for a single resource that cannot be expressed via a standard method. | AIP-136 | handwritten | automatable | automatable |
| _Custom Mutation Methods_ | | | | |
| **Backing up a resource**: storing a copy of a resource at a particular point in time. | AIP-162 | unused or handwritten | automatable | automatable |
| **Restoring a resource**: setting a resource to a version from a particular point in time. | AIP-162 | unused or handwritten | automatable | automatable |
| **Renaming a resource**: modify the resource's name or id while preserving configuration and data. | AIP-136 | unused or handwritten | automatable | automatable |
| **Custom collection mutation methods**: perform an imperative operation referencing a collection that may mutate one or more resources within that collection in a fashion that cannot be easily achieved by standard methods (e.g. state transitions). | AIP-136 | unused or handwritten | automatable | automatable |
| **Custom resource mutation methods**: perform an imperative operation on a resource that may mutate it in a way a standard method cannot (e.g. state transitions). | AIP-136 | unused or handwritten | automatable | automatable |
| _Misc Custom Methods_ | | | | |
| **Stateless Methods**: a method that has no permanent effect on any data within the API (e.g. translating text). | AIP-136 | unused or handwritten | automatable | automatable |
| _None of the above_ | | | | |
| **Streaming methods**: methods that communicate via client, server, or bi-directional streams. | | handwritten | handwritten | automatable |

**Choosing a method category**

When designing a method, API authors **should** choose from the defined categories in the following priority order:

1. **Standard methods** (on collections and resources).
2. **Standard batch or aggregate methods**.
3. **Custom methods** (on collections, resources, or stateless).
4. **Streaming methods**.

**Rationale**

Resource-oriented standard and custom methods are recommended first, as they can be expressed in the widest variety of clients (declarative clients, CLIs, UIs, and so on), and offer the most uniform experience that allows users to apply their knowledge of one API to another.

If a standard method is unsuitable, then custom methods (that are mounted to a resource or collection) offer a lesser, but still valuable level of consistency, helping the user reason about the scope of the action and the object whose configuration is read to inform that action. Although mutative custom methods are not uniform enough to have an automated integration with exclusively resource-oriented clients such as declarative clients, they are still a pattern that can be easily recognized by CLIs, UIs, and SDKs.

If one cannot express their APIs in a resource-oriented fashion at all, then the operation falls in a category where the lack of uniformity makes it difficult for any client aside from SDKs to model the operation. This category is preferred last due to the fact that a user cannot rely on their knowledge of similar APIs, as well as the issue that integration with many clients will likely have to be hand-written.

### 5.2 Standard Method: Get (AIP-131)
[ref: #standard-method-get-aip-131]

In REST APIs, it is customary to make a `GET` request to a resource's URI in order to retrieve that resource. Resource-oriented design (AIP-121) honors this pattern through the `Get` method. APIs **must** provide a get method for resources.

**Purpose:** Return data from a single resource.

```protobuf
rpc GetBook(GetBookRequest) returns (Book) {
  option (google.api.http) = {
    get: "/v1/{name=publishers/*/books/*}"
  };
  option (google.api.method_signature) = "name";
}
```

**Rules:**
- The RPC's name **must** begin with `Get`. The remainder of the RPC name **should** be the singular form of the resource's message name.
- The request message **must** match the RPC name, with a `Request` suffix.
- The response message **must** be the resource itself. (There is no `GetBookResponse`.)
  - The response **should** usually include the fully-populated resource unless there is a reason to return a partial response (see AIP-157).
- The HTTP verb **must** be `GET`.
- The URI **should** contain a single variable field corresponding to the resource name.
  - This field **should** be called `name`.
  - The URI **should** have a variable corresponding to this field.
  - The `name` field **should** be the only variable in the URI path. All remaining parameters **should** map to URI query parameters.
- There **must not** be a `body` key in the `google.api.http` annotation.
- There **should** be exactly one `google.api.method_signature` annotation, with a value of `"name"`.

**Request message**

```protobuf
message GetBookRequest {
  // The name of the book to retrieve.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/Book"
    }];
}
```

- A resource name field **must** be included. It **should** be called `name`.
  - The field **should** be annotated as required.
  - The field **must** identify the resource type that it references.
- The comment for the `name` field **should** document the resource pattern.
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in another AIP.

**Note:** The `name` field in the request object corresponds to the `name` variable in the `google.api.http` annotation on the RPC. This causes the `name` field in the request to be populated based on the value in the URL when the REST/JSON interface is used.

**Errors**

See [AIP-193](09_polish.md#errors-aip-193), in particular when to use `PERMISSION_DENIED` and `NOT_FOUND` errors.

### 5.3 Standard Method: List (AIP-132)
[ref: #standard-method-list-aip-132]

In REST APIs, it is customary to make a `GET` request to a collection's URI (for example, `/v1/publishers/1/books`) in order to retrieve a list of resources, each of which lives within that collection. Resource-oriented design (AIP-121) honors this pattern through the `List` method. APIs **must** provide a `List` method for resources unless the resource is a singleton.

**Purpose:** Return data from a finite collection (generally singular unless the operation supports reading across collections).

```protobuf
rpc ListBooks(ListBooksRequest) returns (ListBooksResponse) {
  option (google.api.http) = {
    get: "/v1/{parent=publishers/*}/books"
  };
  option (google.api.method_signature) = "parent";
}
```

**Rules:**
- The RPC's name **must** begin with `List`. The remainder of the RPC name **should** be the plural form of the resource being listed.
- The request and response messages **must** match the RPC name, with `Request` and `Response` suffixes.
- The HTTP verb **must** be `GET`.
- The collection whose resources are being listed **should** map to the URI path.
  - The collection's parent resource **should** be called `parent`, and **should** be the only variable in the URI path. All remaining parameters **should** map to URI query parameters.
  - The collection identifier (`books` in the above example) **must** be a literal string.
- The `body` key in the `google.api.http` annotation **must** be omitted.
- If the resource being listed is not a top-level resource, there **should** be exactly one `google.api.method_signature` annotation, with a value of `"parent"`. If the resource being listed is a top-level resource, there **should** be either no `google.api.method_signature` annotation, or exactly one `google.api.method_signature` annotation, with a value of `""`.

**Request message**

```protobuf
message ListBooksRequest {
  // The parent, which owns this collection of books.
  // Format: publishers/{publisher}
  string parent = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // The maximum number of books to return. The service may return fewer than
  // this value.
  // If unspecified, at most 50 books will be returned.
  // The maximum value is 1000; values above 1000 will be coerced to 1000.
  int32 page_size = 2;

  // A page token, received from a previous `ListBooks` call.
  // Provide this to retrieve the subsequent page.
  //
  // When paginating, all other parameters provided to `ListBooks` must match
  // the call that provided the page token.
  string page_token = 3;
}
```

- A `parent` field **must** be included unless the resource being listed is a top-level resource. It **should** be called `parent`.
  - The field **should** be annotated as required.
  - The field **must** identify the resource type of the resource being listed.
- The `page_size` and `page_token` fields, which support pagination, **must** be specified on all list request messages. For more information, see AIP-158.
  - The comment above the `page_size` field **should** document the maximum allowed value, as well as the default value if the field is omitted (or set to `0`). If preferred, the API **may** state that the server will use a sensible default. This default **may** change over time.
  - If a user provides a value greater than the maximum allowed value, the API **should** coerce the value to the maximum allowed.
  - If a user provides a negative or other invalid value, the API **must** send an `INVALID_ARGUMENT` error.
- The `page_token` field **must** be included on all list request messages.
- The request message **may** include fields for common design patterns relevant to list methods, such as `string filter` and `string order_by`.
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.

**Note:** List methods **should** return the same results for any user that has permission to make a successful List request on the collection. Search methods are more relaxed on this.

**Response message**

```protobuf
message ListBooksResponse {
  // The books from the specified publisher.
  repeated Book books = 1;

  // A token, which can be sent as `page_token` to retrieve the next page.
  // If this field is omitted, there are no subsequent pages.
  string next_page_token = 2;
}
```

- The response message **must** include one repeated field corresponding to the resources being returned, and **should not** include any other repeated fields unless described in another AIP (for example, AIP-217).
  - The response **should** usually include fully-populated resources unless there is a reason to return a partial response (see AIP-157).
- The `next_page_token` field, which supports pagination, **must** be included on all list response messages. It **must** be set if there are subsequent pages, and **must not** be set if the response represents the final page. For more information, see AIP-158.
- The message **may** include a `int32 total_size` (or `int64 total_size`) field with the number of items in the collection.
  - The value **may** be an estimate (the field **should** clearly document this if so).
  - If filtering is used, the `total_size` field **should** reflect the size of the collection _after_ the filter is applied.

**Ordering**

`List` methods **may** allow clients to specify sorting order; if they do, the request message **should** contain a `string order_by` field.

- Values **should** be a comma separated list of fields. For example: `"foo,bar"`.
- The default sorting order is ascending. To specify descending order for a field, users append a `" desc"` suffix; for example: `"foo desc, bar"`.
- Redundant space characters in the syntax are insignificant. `"foo, bar desc"`, `" foo , bar desc "`, and `"foo,bar desc"` are all equivalent.
- Subfields are specified with a `.` character, such as `foo.bar` or `address.street`.
- The resulting list order **should** be based on the field type's natural comparator (e.g. numerics ordered numerically, strings ordered lexicographically, etc.). However, APIs **may** choose to use a different ordering; if so, it **must** be documented in the `order_by` definition.
  - Furthermore, well-known types, like `Timestamp` and `Duration`, are compared as their representative type; `Timestamp` is compared as time (e.g. before or after), `Duration` is compared as a quantity (e.g. more or less).

**Note:** Only include ordering if there is an established need to do so. It is always possible to add ordering later, but removing it is a breaking change.

**Filtering**

List methods **may** allow clients to specify filters; if they do, the request message **should** contain a `string filter` field. Filtering is described in more detail in AIP-160.

**Note:** Only include filtering if there is an established need to do so. It is always possible to add filtering later, but removing it is a breaking change.

**Soft-deleted resources**

Some APIs need to "soft delete" resources, marking them as deleted or pending deletion (and optionally purging them later).

APIs that do this **should not** include deleted resources by default in list requests. APIs with soft deletion of a resource **should** include a `bool show_deleted` field in the list request that, if set, will cause soft-deleted resources to be included.

**Errors**

See [AIP-193](09_polish.md#errors-aip-193), in particular when to use `PERMISSION_DENIED` and `NOT_FOUND` errors.

**Further reading**

- For details on pagination, see [AIP-158](07_design_patterns.md#pagination-aip-158).
- For listing across multiple parent collections, see [AIP-159](07_design_patterns.md#reading-across-collections-aip-159).

> **Agent extension — not part of the AIP standard.** List rarely stands alone in production: pair it with pagination (AIP-158), filtering (AIP-160), and partial responses (AIP-157) from the start, because retrofitting them onto a shipped List method forces awkward field additions later. Like Get, List uses HTTP GET and therefore must not define a request body — all parameters travel in the query string.

### 5.4 Standard Method: Create (AIP-133)
[ref: #standard-method-create-aip-133]

In REST APIs, it is customary to make a `POST` request to a collection's URI (for example, `/v1/publishers/{publisher}/books`) in order to create a new resource within that collection. Resource-oriented design (AIP-121) honors this pattern through the `Create` method. APIs **should** generally provide a create method for resources unless it is not valuable for users to do so.

**Purpose:** Create a new resource in an already-existing collection.

```protobuf
rpc CreateBook(CreateBookRequest) returns (Book) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books"
    body: "book"
  };
  option (google.api.method_signature) = "parent,book,book_id";
}
```

**Rules:**
- The RPC's name **must** begin with `Create`. The remainder of the RPC name **should** be the singular form of the resource being created.
- The request message **must** match the RPC name, with a `Request` suffix.
- The response message **must** be the resource itself. There is no `CreateBookResponse`.
  - The response **should** include the fully-populated resource, and **must** include any fields that were provided unless they are input only (see AIP-203) or there is a reason to return a partial response (see AIP-157).
  - If the create RPC is long-running, the response message **must** be a `google.longrunning.Operation` which resolves to the resource itself.
- The HTTP verb **must** be `POST`.
- The collection where the resource is being added **should** map to the URI path.
  - The collection's parent resource **should** be called `parent`, and **should** be the only variable in the URI path.
  - The collection identifier (`books` in the above example) **must** be a literal string.
- There **must** be a `body` key in the `google.api.http` annotation, and it **must** map to the resource field in the request message.
  - All remaining fields **should** map to URI query parameters.
- There **should** be exactly one `google.api.method_signature` annotation, with a value of `"parent,{resource},{resource}_id"`, or `"parent,{resource}"` if the resource ID is not required.
- If the API is operating on the management plane, the operation should have strong consistency: the completion of a create operation **must** mean that all user-settable values and the existence of the resource have reached a steady-state and reading resource state returns a consistent response.

**Request message**

```protobuf
message CreateBookRequest {
  // The parent resource where this book will be created.
  // Format: publishers/{publisher}
  string parent = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // The ID to use for the book, which will become the final component of
  // the book's resource name.
  //
  // This value should be 4-63 characters, and valid characters
  // are /[a-z][0-9]-/.
  string book_id = 2 [(google.api.field_behavior) = REQUIRED];

  // The book to create.
  Book book = 3 [(google.api.field_behavior) = REQUIRED];
}
```

- A `parent` field **must** be included unless the resource being created is a top-level resource. It **should** be called `parent`.
  - The field **should** be annotated as required.
  - The field **must** identify the resource type of the resource being created.
- A `{resource}_id` field **must** be included for management plane resources, and **should** be included for data plane resources.
- The resource field **must** be included and **must** map to the POST body.
- The request message **must not** contain any other required fields and **should not** contain other optional fields except those described in this or another AIP.

**Long-running create**

Some resources take longer to create than is reasonable for a regular API request. In this situation, the API **should** use a long-running operation (AIP-151) instead:

```protobuf
rpc CreateBook(CreateBookRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books"
    body: "book"
  };
  option (google.longrunning.operation_info) = {
    response_type: "Book"
    metadata_type: "OperationMetadata"
  };
}
```

- The response type **must** be set to the resource (what the return type would be if the RPC was not long-running).
- Both the `response_type` and `metadata_type` fields **must** be specified.

**Important:** Declarative-friendly resources (AIP-128) **should** use long-running operations. The service **may** return an LRO that is already set to done if the request is effectively immediate.

**User-specified IDs**

An API **must** allow a user to specify the ID component of a resource (the last segment of the resource name) on creation if the API is operating on the management plane.

On the data plane, an API **should** allow a user to specify the ID. Exceptional cases should have the following behavior:

- The data plane resource allows identical records without a need to disambiguate between the two (e.g. rows in a table with no primary key).
- The data plane resource will not be exposed in declarative clients.

An API **may** allow the `{resource}_id` field to have the field behavior `OPTIONAL`, and generate a system-generated ID if one is not specified.

For example:

```
// Using user-specified IDs.
publishers/lacroix/books/les-miserables

// Using system-generated IDs.
publishers/012345678-abcd-cdef/books/12341234-5678-abcd
```

- The `{resource}_id` field **must** exist on the request message, not the resource itself.
  - The field **may** be required or optional. If it is required, it **should** include the corresponding annotation.
- The `name` field on the resource **must** be ignored.
- There **should** be exactly one `google.api.method_signature` annotation on the RPC, with a value of `"parent,{resource},{resource}_id"` if the resource being created is not a top-level resource, or with a value of `"{resource},{resource}_id"` if the resource being created is a top-level resource.
- The documentation **should** explain what the acceptable format is, and the format **should** follow the guidance for resource name formatting in AIP-122.
- If a user tries to create a resource with an ID that would result in a duplicate resource name, the service **must** error with `ALREADY_EXISTS`.
  - However, if the user making the call does not have permission to see the duplicate resource, the service **must** error with `PERMISSION_DENIED` instead.

**Note:** For REST APIs, the user-specified ID field, `{resource}_id`, is provided as a query parameter on the request URI.

**Errors**

See [AIP-193](09_polish.md#errors-aip-193), in particular when to use `PERMISSION_DENIED` and `NOT_FOUND` errors.

**Further reading**

- For ensuring idempotency in `Create` methods, see [AIP-155](07_design_patterns.md#request-identification-aip-155).
- For naming resources involving Unicode, see [AIP-210](07_design_patterns.md#unicode-aip-210).

**Rationale**

***Requiring user-specified IDs***

Declarative clients use the resource ID as a way to identify a resource for applying updates and for conflict resolution. The lack of a user-specified ID means a client is unable to find the resource unless they store the identifier locally, and can result in re-creating the resource. This in turn has a downstream effect on all resources that reference it, forcing them to update to the ID of the newly-created resource.

Having a user-specified ID also means the client can precalculate the resource name and use it in references from other resources.

> **Agent extension — not part of the AIP standard.** Create maps to HTTP POST on the parent collection and returns the created resource. When the API accepts user-specified IDs, Create becomes effectively idempotent per AIP-155: a retried request with the same ID must not spawn a duplicate resource — design for this deliberately instead of relying on the client not to retry. Name messages `<Method><Resource>Request` / `<Resource>` so generated docs and lint rules line up.

### 5.5 Standard Method: Update (AIP-134)
[ref: #standard-method-update-aip-134]

In REST APIs, it is customary to make a `PATCH` or `PUT` request to a resource's URI (for example, `/v1/publishers/{publisher}/books/{book}`) in order to update that resource. Resource-oriented design (AIP-121) honors this pattern through the `Update` method (which mirrors the REST `PATCH` behavior). APIs **should** generally provide an update method for resources unless it is not valuable for users to do so.

**Purpose:** Make changes to a resource without causing side effects.

```protobuf
rpc UpdateBook(UpdateBookRequest) returns (Book) {
  option (google.api.http) = {
    patch: "/v1/{book.name=publishers/*/books/*}"
    body: "book"
  };
  option (google.api.method_signature) = "book,update_mask";
}
```

**Rules:**
- The RPC's name **must** begin with `Update`. The remainder of the RPC name **should** be the singular form of the resource's message name.
- The request message **must** match the RPC name, with a `Request` suffix.
- The response message **must** be the resource itself. (There is no `UpdateBookResponse`.)
  - The response **should** include the fully-populated resource, and **must** include any fields that were sent and included in the update mask unless they are input only (see AIP-203) or there is a reason to return a partial response (see AIP-157).
  - If the update RPC is long-running, the response message **must** be a `google.longrunning.Operation` which resolves to the resource itself.
- The method **should** support partial resource update, and the HTTP verb **should** be `PATCH`.
  - If the method will only ever support full resource replacement, then the HTTP verb **may** be `PUT`. However, this is strongly discouraged because it becomes a backwards-incompatible change to add fields to the resource.
- The resource's `name` field **should** map to the URI path.
  - The `{resource}.name` field **should** be the only variable in the URI path.
- There **must** be a `body` key in the `google.api.http` annotation, and it **must** map to the resource field in the request message.
  - All remaining fields **should** map to URI query parameters.
- There **should** be exactly one `google.api.method_signature` annotation, with a value of `"{resource},update_mask"`.
- If the API is operating on the management plane, the operation should have strong consistency: the completion of an update operation **must** mean that all user-settable values and the existence of the resource have reached a steady-state and reading resource state returns a consistent response.

**Note:** Unlike the other four standard methods, the URI path here references a nested field (`book.name` in the example). If the resource field has a word separator, `snake_case` is used.

**Request message**

```protobuf
message UpdateBookRequest {
  // The book to update.
  //
  // The book's `name` field is used to identify the book to update.
  // Format: publishers/{publisher}/books/{book}
  Book book = 1 [(google.api.field_behavior) = REQUIRED];

  // The list of fields to update.
  google.protobuf.FieldMask update_mask = 2;
}
```

- The request message **must** contain a field for the resource.
  - The field **must** map to the `PATCH` body.
  - The field **should** be annotated as required.
  - A `name` field **must** be included in the resource message. It **should** be called `name`.
  - The field **must** identify the resource type of the resource being updated.
- If partial resource update is supported, a field mask **must** be included. It **must** be of type `google.protobuf.FieldMask`, and it **must** be called `update_mask`.
  - The fields used in the field mask correspond to the resource being updated (not the request message).
  - The field **must** be optional, and the service **must** treat an omitted field mask as an implied field mask equivalent to all fields that are populated (have a non-empty value).
  - Update masks **must** support a special value `*`, meaning full replacement (the equivalent of `PUT`).
    - API producers need to be conscious of how adding new, mutable fields to a resource will be handled when consumers use `*` without knowledge of said new, mutable fields. Likewise consumers need to use `*` only when the risks of doing so are acceptable. In general, it is safest to explicitly specify the fields to update rather than use `*`.
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.

**Side effects**

In general, update methods are intended to update the data within the resource. Update methods **should not** trigger other side effects. Instead, side effects **should** be triggered by custom methods.

In particular, this entails that state fields **must not** be directly writable in update methods.

**PATCH and PUT**

Google APIs generally use the `PATCH` HTTP verb only, and do not support `PUT` requests.

`PATCH` is standardized because APIs update stable APIs in place with backwards-compatible improvements. It is often necessary to add a new field to an existing resource, but this becomes a breaking change when using `PUT`.

To illustrate this, consider a `PUT` request to a `Book` resource:

```
PUT /v1/publishers/123/books/456

{"title": "Mary Poppins", "author": "P.L. Travers"}
```

Next consider that the resource is later augmented with a new field (here we add `rating`):

```protobuf
message Book {
  string title = 1;
  string author = 2;

  // Subsequently added to v1 in place...
  int32 rating = 3;
}
```

If a rating is set on a book and the existing `PUT` request was executed, it would wipe out the book's rating. In essence, a `PUT` request unintentionally wiped out data because the previous version did not know about it.

**Long-running update**

Some resources take longer to update than is reasonable for a regular API request. In this situation, the API **should** use a long-running operation (AIP-151) instead:

```protobuf
rpc UpdateBook(UpdateBookRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    patch: "/v1/{book.name=publishers/*/books/*}"
    body: "book"
  };
  option (google.longrunning.operation_info) = {
    response_type: "Book"
    metadata_type: "OperationMetadata"
  };
}
```

- The response type **must** be set to the resource (what the return type would be if the RPC was not long-running).
- Both the `response_type` and `metadata_type` fields **must** be specified.

**Note:** Declarative-friendly resources (AIP-128) **should** use long-running update.

**Create or update**

If the service uses client-assigned resource names, `Update` methods **may** expose a `bool allow_missing` field, which will cause the method to succeed in the event that the user attempts to update a resource that is not present (and will create the resource in the process):

```protobuf
message UpdateBookRequest {
  // The book to update.
  //
  // The book's `name` field is used to identify the book to be updated.
  // Format: publishers/{publisher}/books/{book}
  Book book = 1 [(google.api.field_behavior) = REQUIRED];

  // The list of fields to be updated.
  google.protobuf.FieldMask update_mask = 2;

  // If set to true, and the book is not found, a new book will be created.
  // In this situation, `update_mask` is ignored.
  bool allow_missing = 3;
}
```

More specifically, the `allow_missing` flag triggers the following behavior:

- If the method call is on a resource that does not exist, the resource is created. All fields are applied regardless of any provided field mask.
  - However, if any required fields are missing or fields have invalid values, an `INVALID_ARGUMENT` error is returned.
- If the method call is on a resource that already exists, and all fields match, the existing resource is returned unchanged.
- If the method call is on a resource that already exists, only fields declared in the field mask are updated.

The user **must** have the update permissions to call `Update` even with `allow_missing` set to `true`. For customers that want to prevent users from creating resources using the update method, IAM conditions **should** be used.

**Etags**

An API may sometimes need to allow users to send update requests which are guaranteed to be made against the most current data (a common use case for this is to detect and avoid race conditions). Resources which need to enable this do so by including a `string etag` field, which contains an opaque, server-computed value representing the content of the resource.

In this situation, the resource **should** contain a `string etag` field:

```protobuf
message Book {
  option (google.api.resource) = {
    type: "library.googleapis.com/Book"
    pattern: "publishers/{publisher}/books/{book}"
  };

  // The resource name of the book.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  // The title of the book.
  // Example: "Mary Poppins"
  string title = 2;

  // The author of the book.
  // Example: "P.L. Travers"
  string author = 3;

  // The etag for this book.
  // If this is provided on update, it must match the server's etag.
  string etag = 4;
}
```

The `etag` field **may** be either required or optional. If it is set, then the request **must** succeed if and only if the provided etag matches the server-computed value, and **must** fail with an `ABORTED` error otherwise. The `update_mask` field in the request does not affect the behavior of the `etag` field, as it is not a field _being_ updated.

**Expensive fields**

APIs sometimes encounter situations where some fields on a resource are expensive or impossible to reliably return.

This can happen in a few situations:

- A resource may have some fields that are very expensive to compute, and that are generally not useful to the customer on update requests.
- A single resource sometimes represents an amalgamation of data from multiple underlying (and eventually consistent) data sources. In these situations, it is impossible to return authoritative information on the fields that were not changed.

In this situation, an API **may** return back only the fields that were updated, and omit the rest, and **should** document this behavior if they do so.

**Errors**

See [AIP-193](09_polish.md#errors-aip-193), in particular when to use `PERMISSION_DENIED` and `NOT_FOUND` errors.

In addition, if the user does have proper permission, but the requested resource does not exist, the service **must** error with `NOT_FOUND` (HTTP 404) unless `allow_missing` is set to `true`.

> **Agent extension — not part of the AIP standard.** Update maps to HTTP PATCH with an explicit `update_mask`: the mask is what prevents a client that only wants to rename a resource from accidentally wiping every other field it happened to leave unset. Keep Update free of significant side effects — if a field change must trigger a larger process, that process is usually a custom method (AIP-136) or a long-running operation (AIP-151), not a silent consequence of PATCH.

### 5.6 Standard Method: Delete (AIP-135)
[ref: #standard-method-delete-aip-135]

In REST APIs, it is customary to make a `DELETE` request to a resource's URI (for example, `/v1/publishers/{publisher}/books/{book}`) in order to delete that resource. Resource-oriented design (AIP-121) honors this pattern through the `Delete` method. APIs **should** generally provide a delete method for resources unless it is not valuable for users to do so.

**Purpose:** Remove a resource.

```protobuf
rpc DeleteBook(DeleteBookRequest) returns (google.protobuf.Empty) {
  option (google.api.http) = {
    delete: "/v1/{name=publishers/*/books/*}"
  };
  option (google.api.method_signature) = "name";
}
```

**Rules:**
- The RPC's name **must** begin with `Delete`. The remainder of the RPC name **should** be the singular form of the resource's message name.
- The request message **must** match the RPC name, with a `Request` suffix.
- The response message **should** be `google.protobuf.Empty`.
  - If the resource is soft deleted, the response message **should** be the resource itself (see AIP-164).
  - If the delete RPC is long-running, the response message **must** be a `google.longrunning.Operation` which resolves to the correct response.
- The HTTP verb **must** be `DELETE`.
- The request message field receiving the resource name **should** map to the URI path.
  - This field **should** be called `name`.
  - The `name` field **should** be the only variable in the URI path. All remaining parameters **should** map to URI query parameters.
- There **must not** be a `body` key in the `google.api.http` annotation.
- There **should** be exactly one `google.api.method_signature` annotation, with a value of `"name"`. If an `etag` or `force` field are used, they **may** be included in the signature.
- If the API is operating on the management plane, the operation should have strong consistency: the completion of a delete operation **must** mean that the existence of the resource has reached a steady-state and reading resource state returns a consistent response.
- The API **must** fail with a `FAILED_PRECONDITION` error if child resources are present. See guidance on Cascading Delete if forcing deletion of parent and child resources is necessary.
  - If the only child resource type is a Singleton, deletion **must** be allowed, because the lifecycle of a Singleton is tied to that of its parent resource. This applies even if there are multiple different Singleton resource types for the same parent resource.
- The Delete method **should** succeed if and only if a resource was present and was successfully deleted. If the resource did not exist, the method **should** send a `NOT_FOUND` error.

**Request message**

```protobuf
message DeleteBookRequest {
  // The name of the book to delete.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/Book"
    }];
}
```

- A `name` field **must** be included. It **should** be called `name`.
  - The field **should** be annotated as required.
  - The field **must** identify the resource type that it references.
- The comment for the field **should** document the resource pattern.
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.

**Long-running delete**

Some resources take longer to delete than is reasonable for a regular API request. In this situation, the API **should** use a long-running operation (AIP-151) instead:

```protobuf
rpc DeleteBook(DeleteBookRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    delete: "/v1/{name=publishers/*/books/*}"
  };
  option (google.longrunning.operation_info) = {
    response_type: "google.protobuf.Empty"
    metadata_type: "OperationMetadata"
  };
}
```

- The response type **must** be set to the appropriate return type if the RPC was not long-running: `google.protobuf.Empty` for most Delete RPCs, or the resource itself for soft delete (AIP-164).
- Both the `response_type` and `metadata_type` fields **must** be specified (even if they are `google.protobuf.Empty`).

**Cascading delete**

Sometimes, it may be necessary for users to be able to delete a resource as well as all applicable child resources. However, since deletion is usually permanent, it is also important that users not do so accidentally, as reconstructing wiped-out child resources may be quite difficult.

If an API allows deletion of a resource that may have child resources, the API **should** provide a `bool force` field on the request, which the user sets to explicitly opt in to a cascading delete:

```protobuf
message DeletePublisherRequest {
  // The name of the publisher to delete.
  // Format: publishers/{publisher}
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/Publisher"
    }];

  // If set to true, any books from this publisher will also be deleted.
  // (Otherwise, the request will only work if the publisher has no books.)
  bool force = 2;
}
```

The API **must** fail with a `FAILED_PRECONDITION` error if the `force` field is `false` (or unset) and child resources are present.

**Protected delete**

Sometimes, it may be necessary for users to ensure that no changes have been made to a resource that is being deleted. If a resource provides an etag, the delete request **may** accept the etag (as either required or optional):

```protobuf
message DeleteBookRequest {
  // The name of the book to delete.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/Book"
    }];

  // Optional. The etag of the book.
  // If this is provided, it must match the server's etag.
  string etag = 2;
}
```

If the etag is provided and does not match the server-computed etag, the request **must** fail with an `ABORTED` error code.

**Note:** Declarative-friendly resources (AIP-128) **must** provide the `etag` field for Delete requests.

**Delete if existing**

If the service uses client-assigned resource names, `Delete` methods **may** expose a `bool allow_missing` field, which will cause the method to succeed in the event that the user attempts to delete a resource that is not present (in which case the request is a no-op):

```protobuf
message DeleteBookRequest {
  // The book to delete.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference).type = "library.googleapis.com/Book"
  ];

  // If set to true, and the book is not found, the request will succeed
  // but no action will be taken on the server
  bool allow_missing = 2;
}
```

More specifically, the `allow_missing` flag triggers the following behavior:

- If the method call is on a resource that does not exist, the request is a no-op.
  - The `etag` field is ignored.
- If the method call is on a resource that already exists, the resource is deleted (subject to other checks).

**Note:** Declarative-friendly resources (AIP-128) **should** expose the `bool allow_missing` field.

**Errors**

If the user does not have permission to access the resource, regardless of whether or not it exists, the service **must** error with `PERMISSION_DENIED` (HTTP 403). Permission **must** be checked prior to checking if the resource exists.

If the user does have proper permission, but the requested resource does not exist, the service **must** error with `NOT_FOUND` (HTTP 404) unless `allow_missing` is set to `true`.

**Further reading**

- For soft delete and undelete, see [AIP-164](07_design_patterns.md#soft-delete-aip-164).
- For bulk deleting large numbers of resources based on a filter, see [AIP-165](07_design_patterns.md#criteria-based-delete-aip-165).

> **Agent extension — not part of the AIP standard.** Delete maps to HTTP DELETE and must not define a request body. Choose the response type deliberately: `google.protobuf.Empty` forecloses ever returning data (a breaking limitation discovered later), while returning the deleted resource helps clients confirm what was removed — and if the resource uses soft delete (AIP-164), Delete marks rather than erases, which changes what the response should convey. For long-running deletes, the LRO `response_type` carries the same Empty-versus-message decision.

### 5.7 Custom Methods (AIP-136)
[ref: #custom-methods-aip-136]

Resource-oriented design (AIP-121) uses custom methods to provide a means to express arbitrary actions that are difficult to model using only the standard methods. Custom methods are important because they provide a means for an API's vocabulary to adhere to user intent.

**Purpose:** Provide functionality that can not be easily expressed via standard methods.

Custom methods **should** only be used for functionality that can not be easily expressed via standard methods; prefer standard methods if possible, due to their consistent semantics. (Of course, this only applies if the functionality in question actually conforms to the normal semantics; it is not a good idea to contort things to endeavor to make the standard methods "sort of work".)

While custom methods vary widely in how they are designed, many principles apply consistently:

```protobuf
// Archives the given book.
rpc ArchiveBook(ArchiveBookRequest) returns (ArchiveBookResponse) {
  option (google.api.http) = {
    post: "/v1/{name=publishers/*/books/*}:archive"
    body: "*"
  };
}
```

**Note:** The pattern above shows a custom method that operates on a specific resource. Custom methods can be associated with resources, collections, or services. The bullets below apply in all three cases.

- The name of the method **should** be a verb followed by a noun.
  - The name **must not** contain prepositions ("for", "with", etc.).
  - The verb in the name **should not** contain any of the standard method verbs (`Get`, `List`, `Create`, `Update`, `Delete`).
  - The name **must not** include the term `Async`. Instead, if the intention is to differentiate between immediate and long-running RPCs, the suffix `LongRunning` **may** be used for this purpose. For example, to create a long-running book creation RPC (if the standard `CreateBook` method was designed before long-running aspects were considered), a custom `CreateBookLongRunning` method could be introduced.
- The HTTP method **must** be `GET` or `POST`:
  - `GET` **must** be used for methods retrieving data or resource state.
  - `POST` **must** be used if the method has side effects or mutates resources or data.
- The HTTP URI **must** use a `:` character followed by the custom verb (`:archive` in the above example), and the verb in the URI **must** match the verb in the name of the RPC.
  - If word separation is required, `camelCase` **must** be used.
- The `body` clause in the `google.api.http` annotation **should** be `"*"`.
- Custom methods **should** take a request message matching the RPC name, with a `Request` suffix.
- Custom methods **should** return a response message matching the RPC name, with a `Response` suffix.
  - When operating on a specific resource, a custom method **may** return the resource itself.

**Resource-based custom methods**

Custom methods **must** operate on a resource if the API can be modeled as such:

```protobuf
// Archives the given book.
rpc ArchiveBook(ArchiveBookRequest) returns (ArchiveBookResponse) {
  option (google.api.http) = {
    post: "/v1/{name=publishers/*/books/*}:archive"
    body: "*"
  };
}
```

- The parameter for the resource's name **must** be called `name`, and be the only variable in the URI path.

**Collection-based custom methods**

While most custom methods operate on a single resource, some custom methods **may** operate on a collection instead:

```protobuf
// Sorts the books from this publisher.
rpc SortBooks(SortBooksRequest) returns (SortBooksResponse) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books:sort"
    body: "*"
  };
}
```

- If the collection's resource has a parent, that resource **must** be called `parent` and be the only variable in the URI path.
- The collection key (`books` in the above example) **must** be literal.

**Stateless methods**

Some custom methods are not attached to resources at all. These methods are generally _stateless_: they accept a request and return a response, and have no permanent effect on data within the API.

```protobuf
// Translates the provided text from one language to another.
rpc TranslateText(TranslateTextRequest) returns (TranslateTextResponse) {
  option (google.api.http) = {
    post: "/v1/{project=projects/*}:translateText"
    body: "*"
  };
}
```

- If the method runs in a particular scope (such as a project, as in the above example), the field name in the request message **should** be the name of the scope resource. If word separators are necessary, `snake_case` **must** be used.
- The URI **should** place both the verb and noun after the `:` separator (avoid a "faux collection key" in the URI in this case, as there is no collection). For example, `:translateText` is preferable to `text:translate`.
- Stateless methods **must** use `POST` if they involve billing.

**Declarative-friendly resources**

Declarative-friendly resources usually **should not** employ custom methods (except specific declarative-friendly custom methods discussed in other AIPs), because declarative-friendly tools are unable to automatically determine what to do with them.

An exception to this is for rarely-used, fundamentally imperative operations, such as a `Move` or `Rename` operation, for which there would not be an expectation of declarative support.

**Rationale**

***HTTP path***

Similar to standard methods, a custom method that operates on a resource or collection needs a `name` or `parent` parameter to indicate the resource that it operates on. This convention allows clients to map custom methods to the appropriate resource.

***HTTP methods***

Allowing both `GET` and `POST` HTTP verbs allows a clear distinction for which methods do not mutate data, and which ones do. Methods that only read data have first-class concepts in some clients (DataSources in Terraform) and clearly indicate to a user which methods can be called without risk of runtime impact.

***Disallowing prepositions***

Generally, method names with prepositions indicate that a new method is being used where a field should instead be added to an existing method, or the method should use a distinct verb. For example, if a `CreateBook` message already exists and you are considering adding `CreateBookFromDictation`, consider a `TranscribeBook` method instead. Similarly, if there is desire for a property-specific look-up method, instead of `GetBookByAuthor` consider a `SearchBooks` with an `author` field as a search dimension. This helps prevent an explosion of hyper-focused methods that bloat API and client surfaces, and add complexity to both managing and consuming the API.

***RPC name***

The term "async" is commonly used in programming languages to indicate whether a specific method call is synchronous or asynchronous, including for making RPCs. That sync/async aspect is at a different abstraction level to whether the RPC itself is intended to start a long-running operation. Using "async" within the RPC name itself causes confusion, and can even cause issues for client libraries which generate both synchronous and asynchronous methods to call the RPC in some languages.

> **Agent extension — not part of the AIP standard.** Custom methods are justified when user intent does not map cleanly onto CRUD (Publish, Archive, Cancel) — do not contort a standard method to avoid one. Naming guidance hardened in May 2023: the word `async` is prohibited in RPC names, and HTTP mapping for custom methods (verb choice, `body: "*"` for POST-style actions) follows AIP-127 explicitly. A custom method that takes significant time should still return an LRO rather than block.

### 5.8 Long-Running Operations (AIP-151)
[ref: #long-running-operations-aip-151]

Occasionally, an API may need to expose a method that takes a significant amount of time to complete. In these situations, it is often a poor user experience to simply block while the task runs; rather, it is better to return some kind of promise to the user and allow the user to check back in later.

The long-running operations pattern is roughly analogous to a Python `Future`, or a Node.js `Promise`. Essentially, the user is given a token that can be used to track progress and retrieve the result.

**Purpose:** Methods that might take a significant amount of time to complete.

Individual API methods that might take a significant amount of time to complete **should** return a `google.longrunning.Operation` object instead of the ultimate response message.

**Note:** User expectations can vary on what is considered "a significant amount of time" depending on what work is being done. A good rule of thumb is 10 seconds.

```protobuf
// Create a book.
rpc CreateBook(CreateBookRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books"
    body: "book"
  };
  option (google.longrunning.operation_info) = {
    response_type: "Book"
    metadata_type: "OperationMetadata"
  };
}
```

**Rules:**
- The response type **must** be `google.longrunning.Operation`. The `Operation` proto definition **must not** be copied into individual APIs.
  - The response **must not** be a streaming response.
- The method **must** include a `google.longrunning.operation_info` annotation, which **must** define both response and metadata types.
  - The response and metadata types **must** be defined in the file where the RPC appears, or a file imported by that file.
  - If the response and metadata types are defined in another package, the fully-qualified message name **must** be used.
  - The response type **should not** be `google.protobuf.Empty` (except for `Delete` methods), unless it is certain that response data will _never_ be needed. If response data might be added in the future, define an empty message for the RPC response and use that.
  - The metadata type is used to provide information such as progress, partial failures, and similar information on each `GetOperation` call. The metadata type **should not** be `google.protobuf.Empty`, unless it is certain that metadata will _never_ be needed. If metadata might be added in the future, define an empty message for the RPC metadata and use that.
- APIs with messages that return `Operation` **must** implement the `Operations` service. Individual APIs **must not** define their own interfaces for long-running operations to avoid non-uniformity.
- If an RPC supports a validate-only mode, the response to a validation request **must** be one of the following:
  - A successful response with an `Operation` which is already complete, with the `done` field set to `true`, and a valid (but potentially empty) response message in the `response` field, wrapped in a `google.protobuf.Any` message. The `name` field **may** be empty, to avoid the service having to maintain state for successful validation.
  - An immediate error response (typically "bad request").
  - An `Operation` with the `done` field set to `false`, to indicate long-running validation. In this case, the `name` field **must** be set, to allow clients to poll the long-running validation operation until it has completed. Successful validation **must** eventually be represented by an operation with `done=true` and a valid (but potentially empty) wrapped response message in the `response` field. Unsuccessful validation **must** eventually be represented by an operation with `done=true` and the error details provided in the `error` field.

**Standard methods**

APIs **may** return an `Operation` from the `Create`, `Update`, or `Delete` standard methods if appropriate. In this case, the response type in the `operation_info` annotation **must** be the standard and expected response type for that standard method.

When creating or deleting a resource with a long-running operation, the resource **should** be included in `List` and `Get` calls; however, the resource **should** indicate that it is not usable, generally with a state enum.

**Parallel operations**

A resource **may** accept multiple operations that will work on it in parallel, but is not obligated to do so:

- Resources that accept multiple parallel operations **may** place them in a queue rather than work on the operations simultaneously.
- Resources that do not permit multiple operations in parallel (denying any new operation until the one that is in progress finishes) **must** return `ABORTED` if a user attempts a parallel operation, and include an error message explaining the situation.
- Resources with declarative-friendly APIs **may** allow subsequent updates to preempt existing operations. In this case, the latest update begins processing and previous operations are marked as `ABORTED` with an error message explaining the situation.

**Expiration**

APIs **may** allow their operation resources to expire after sufficient time has elapsed after the operation completed.

**Note:** A good rule of thumb for operation expiry is 30 days.

**Errors**

Errors that prevent a long-running operation from _starting_ **must** return an error response (AIP-193), similar to any other method.

Operations that fail during their execution phase **must** return an error response (AIP-193), placed in the `Operation.error` `google.rpc.Status` field.

Non-terminal errors that occur over the course of an operation **may** be placed in the metadata message and the field(s) **must** be AIP-193 compliant `google.rpc.Status`.

**Backwards compatibility**

Changing either the `response_type` or `metadata_type` of a long-running operation is a breaking change.

**Rationale**

***Validate-only behavior***

The guidance for validate-only responses comes from a tension between clients, which benefit from "fully formed" operations that can be treated uniformly, and servers, which don't wish to maintain additional state for trivial operations. It seems counterintuitive that just validating a request should generate more state, but a full operation response that can be fetched later would either require that or "special" singleton operation IDs. The guidance provided is a compromise: by returning a "done" operation, clients can use existing logic to check that the operation has completed successfully (and therefore doesn't need to be fetched for an updated status) but servers don't need to maintain any additional state.

> **Agent extension — not part of the AIP standard.** The `google.longrunning.operation_info` annotation must declare both `response_type` and `metadata_type`, and changing either later is a breaking change — decide them at design time. `metadata` streams progress while `done == false`; `response` is populated only on completion. Avoid `google.protobuf.Empty` as `response_type` unless result data will never be needed — an empty named message keeps the door open. In practice, official client libraries wrap LROs in futures and handle polling; document the expected polling interval for raw-HTTP clients.

### 5.9 Batch Method: Get (AIP-231)
[ref: #batch-method-get-aip-231]

Some APIs need to allow users to get a specific set of resources at a consistent time point (e.g. using a read transaction). A batch get method provides this functionality. APIs **may** support Batch Get using the following pattern.

**Purpose:** Get multiple resources atomically at a consistent time point.

```protobuf
rpc BatchGetBooks(BatchGetBooksRequest) returns (BatchGetBooksResponse) {
  option (google.api.http) = {
    get: "/v1/{parent=publishers/*}/books:batchGet"
  };
}
```

**Rules:**
- The RPC's name **must** begin with `BatchGet`. The remainder of the RPC name **should** be the plural form of the resource being retrieved.
- The request and response messages **must** match the RPC name, with `Request` and `Response` suffixes.
- The HTTP verb **must** be `GET`.
- The HTTP URI **must** end with `:batchGet`.
- The URI path **should** represent the collection for the resource, matching the collection used for simple CRUD operations. If the operation spans parents, a dash (`-`) **may** be accepted as a wildcard.
- There **must not** be a `body` key in the `google.api.http` annotation.
- The operation **must** be atomic: it **must** fail for all resources or succeed for all resources (no partial success). For situations requiring partial failures, `List` (AIP-132) methods **should** be used.
  - If the operation covers multiple locations and at least one location is down, the operation **must** fail.

**Request message**

The request for a batch get method **should** be specified with the following pattern:

```protobuf
message BatchGetBooksRequest {
  // The parent resource shared by all books being retrieved.
  // Format: publishers/{publisher}
  // If this is set, the parent of all of the books specified in `names`
  // must match this field.
  string parent = 1 [
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // The names of the books to retrieve.
  // A maximum of 1000 books can be retrieved in a batch.
  // Format: publishers/{publisher}/books/{book}
  repeated string names = 2 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/Book"
    }];
}
```

- A `parent` field **should** be included, unless the resource being retrieved is a top-level resource, to facilitate inclusion in the URI as well as to permit a single permissions check. If a caller sets this field, and the parent collection in the name of any resource being retrieved does not match, the request **must** fail.
  - This field **should** be required if only 1 parent per request is allowed.
  - The field **should** identify the resource type that it references.
  - The comment for the field **should** document the resource pattern.
- The request message **must** include a repeated field which accepts the resource names specifying the resources to retrieve. The field **should** be named `names`.
  - If no resource names are provided, the API **should** error with `INVALID_ARGUMENT`.
  - The field **should** be required.
  - The field **should** identify the resource type that it references.
  - The comment for the field **should** document the resource pattern.
- Other fields besides `name` **may** be "hoisted" from the standard Get request. There is no way to allow for these fields to accept different values for different resources; if this is needed, use the alternative request message form.
- Batch get **should not** support pagination because transactionality across API calls would be extremely difficult to implement or enforce, and the request defines the exact scope of the response anyway.
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.
- The comment above the `names` field **should** document the maximum number of requests allowed.

**Response message**

The response for a batch get method **should** be specified with the following pattern:

```protobuf
message BatchGetBooksResponse {
  // Books requested.
  repeated Book books = 1;
}
```

- The response message **must** include one repeated field corresponding to the resources being retrieved.
- The order of books in the response **must** be the same as the names in the request.

**Nested request objects**

If the standard Get request message contains a field besides the resource name that needs to be different between different resources being requested, the batch message **may** alternatively hold a `repeated` field of the standard Get request message. This is generally discouraged unless your use case really requires it.

The request for a batch get method using this approach **should** be specified with the following pattern:

```protobuf
message BatchGetBooksRequest {
  // The parent resource shared by all books being retrieved.
  // Format: publishers/{publisher}
  // If this is set, the parent field in the GetBookRequest messages
  // must either be empty or match this field.
  string parent = 1 [
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // The requests specifying the books to retrieve.
  // A maximum of 1000 books can be retrieved in a batch.
  repeated GetBookRequest requests = 2
    [(google.api.field_behavior) = REQUIRED];
}
```

- A `parent` field **should** be included. If a caller sets this field, and the parent collection in the name of any resource being retrieved does not match, the request **must** fail.
  - This field **should** be required if only 1 parent per request is allowed.
  - The field **should** identify the resource type that it references.
  - The comment for the field **should** document the resource pattern.
- The request message **must** include a repeated field which accepts the request messages specifying the resources to retrieve, as specified for standard Get methods. The field **should** be named `requests`.
  - The field **should** be required.
- Other fields **may** be "hoisted" from the standard Get request, which means that the field can be set at either the batch level or child request level. Similar to `parent`, if both the batch level and child request level are set for the same field, the values **must** match.
- Batch get **should not** support pagination because transactionality across API calls would be extremely difficult to implement or enforce, and the request defines the exact scope of the response anyway.
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.
- The comment above the `requests` field **should** document the maximum number of requests allowed.

> **Agent extension — not part of the AIP standard.** Batch Get is atomic: either every requested resource is returned or the whole call fails — there is no partial-success mode. Clients that can tolerate missing resources should use repeated Get calls or a filtered List instead; do not invent a per-item error channel for Batch Get.

### 5.10 Batch Method: Create (AIP-233)
[ref: #batch-method-create-aip-233]

Some APIs need to allow users to create multiple resources in a single transaction. A batch create method provides this functionality. APIs **may** support Batch Create using the following two patterns.

**Purpose:** Create multiple resources in a single transaction.

Returning the response synchronously:

```protobuf
rpc BatchCreateBooks(BatchCreateBooksRequest) returns (BatchCreateBooksResponse) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books:batchCreate"
    body: "*"
  };
}
```

Returning an `Operation` which resolves to the response asynchronously:

```protobuf
rpc BatchCreateBooks(BatchCreateBooksRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books:batchCreate"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "BatchCreateBooksResponse"
    metadata_type: "BatchCreateBooksOperationMetadata"
  };
}
```

**Rules:**
- The RPC's name **must** begin with `BatchCreate`. The remainder of the RPC name **should** be the plural form of the resource being created.
- The request and response messages **must** match the RPC name, with `Request` and `Response` suffixes.
- If the batch method returns a `google.longrunning.Operation`, both the `response_type` and `metadata_type` fields **must** be specified.
- The HTTP verb **must** be `POST`.
- The HTTP URI **must** end with `:batchCreate`.
- The URI path **should** represent the collection for the resource, matching the collection used for simple CRUD operations. If the operation spans parents, a dash (`-`) **may** be accepted as a wildcard.
- The `body` clause in the `google.api.http` annotation **should** be `"*"`.

**Atomic vs. Partial Success**

The batch create method **may** support atomic (all resources created or none are) or partial success behavior. To make a choice, consider the following factors:

- **Complexity of Ensuring Atomicity:** Operations that are simple passthrough database transactions **should** use an atomic operation, while operations that manage complex resources **should** use partial success operations.
- **End-User Experience:** Consider the perspective of the API consumer. Would atomic behavior be preferable for the given use case, even if it means that a large batch could fail due to issues with a single or a few entries?

- Synchronous batch create **must** be atomic.
- Asynchronous batch create **may** support atomic or partial success.
  - If supporting partial success, see Operation metadata message requirements.

**Request message**

The request for a batch create method **should** be specified with the following pattern:

```protobuf
message BatchCreateBooksRequest {
  // The parent resource shared by all books being created.
  // Format: publishers/{publisher}
  // If this is set, the parent field in the CreateBookRequest messages
  // must either be empty or match this field.
  string parent = 1 [
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // The request message specifying the resources to create.
  // A maximum of 1000 books can be created in a batch.
  repeated CreateBookRequest requests = 2
    [(google.api.field_behavior) = REQUIRED];
}
```

- A `parent` field **should** be included, unless the resource being created is a top-level resource. If a caller sets this field, and the `parent` field of any child request message does not match, the request **must** fail. The `parent` field of child request messages can be omitted if the `parent` field in this request is set.
  - This field **should** be required if only 1 parent per request is allowed.
  - The field **should** identify the resource type that it references.
  - The comment for the field **should** document the resource pattern.
- The request message **must** include a repeated field which accepts the request messages specifying the resources to create, as specified for standard Create methods. The field **should** be named `requests`.
  - The field **should** be required.
- Other fields **may** be "hoisted" from the standard Create request, which means that the field can be set at either the batch level or child request level. Similar to `parent`, if both the batch level and child request level are set for the same field, the values **must** match.
  - Fields which must be unique cannot be hoisted (e.g. customer-provided ID fields).
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.
- The comment above the `requests` field **should** document the maximum number of requests allowed.

**Response message**

The response for a batch create method **should** be specified with the following pattern:

```protobuf
message BatchCreateBooksResponse {
  // Books created.
  repeated Book books = 1;
}
```

- The response message **must** include one repeated field corresponding to the resources that were created.

**Operation metadata message**

- The `metadata_type` message **must** either match the RPC name with `OperationMetadata` suffix, or be named with `Batch` prefix and `OperationMetadata` suffix if the type is shared by multiple Batch methods.
- If the batch create method supports partial success, the metadata message **must** include a `map<int32, google.rpc.Status> failed_requests` field to communicate the partial failures.
  - The key in this map is the index of the request in the `requests` field in the batch request.
  - The value in each map entry **must** mirror the error(s) that would normally be returned by the singular standard Create method.
  - If a failed request can eventually succeed due to server side retries, such transient errors **must not** be communicated using `failed_requests`.
  - When all requests in the batch fail, `Operation.error` **must** be set with `code = google.rpc.Code.Aborted` and `message = "None of the requests succeeded, refer to the BatchCreateBooksOperationMetadata.failed_requests for individual error details"`.
- The metadata message **may** include other fields to communicate the operation progress.

**Adopting Partial Success**

In order for an existing Batch API to adopt the partial success pattern, the API must do the following:

- The default behavior must be retained to avoid incompatible behavioral changes.
- If the API returns an `Operation`:
  - The request message **must** have a `bool return_partial_success` field.
  - The `Operation` `metadata_type` **must** include a `map<int32, google.rpc.Status> failed_requests` field.
  - When the `bool return_partial_success` field is set to `true` in a request, the API should allow partial success behavior, otherwise it should continue with atomic behavior as default.
- If the API returns a direct response synchronously:
  - Since the existing clients will treat a success response as an atomic operation, the existing version of the API **must not** adopt the partial success pattern.
  - A new version **must** be created instead that returns an `Operation` and follows the partial success pattern described in this AIP.

**Rationale**

***Restricting synchronous batch methods to be atomic***

The restriction that synchronous batch methods must be atomic is a result of the following considerations.

The previous iteration of this AIP recommended batch methods must be atomic. There is no clear way to convey partial failure in a sync response status code because an `OK` implies it all worked. Therefore, adding a new field to the response to indicate partial failure would be a breaking change because the existing clients would interpret an `OK` response as all resources created.

On the other hand, as described in AIP-193, Operations are more capable of presenting partial states. The response status code for an `Operation` does not convey anything about the outcome of the underlying operation and a client has to check the response body to determine if the operation was successful.

***Communicating partial failures***

The AIP recommends using a `map<int32, google.rpc.Status> failed_requests` field to communicate partial failures, where the key is the index of the failed request in the original batch request. The other options considered were:

- A `repeated google.rpc.Status` field. This was rejected because it is not clear which entry corresponds to which request.
- A `map<string, google.rpc.Status>` field, where the key is the request ID of the failed request. This was rejected because:
  - Client will need to maintain a map of request_id -> request in order to use the partial success response.
  - Populating a request ID for the purpose of communicating errors could conflict with AIP-155 if the service can not guarantee idempotency for an individual request across multiple batch requests.
- A `repeated FailedRequest` field, where `FailedRequest` contains the individual create request and the `google.rpc.Status`. This was rejected because echoing the request payload back in response is discouraged due to additional challenges around user data sensitivity.

> **Agent extension — not part of the AIP standard.** For batch mutations the ecosystem has settled on partial success over all-or-nothing transactions: report per-item failures with a `map<int32, google.rpc.Status> failed_requests` field keyed by the index of the failed request, or make the batch method long-running and convey per-item outcomes in the LRO metadata. A bare `200 OK` with silent per-item failures is the anti-pattern this convention exists to prevent.

### 5.11 Batch Method: Update (AIP-234)
[ref: #batch-method-update-aip-234]

Some APIs need to allow users to modify a set of resources in a single transaction. A batch update method provides this functionality. APIs **may** support Batch Update using the following two patterns.

**Purpose:** Update multiple resources in a single transaction.

Returning the response synchronously:

```protobuf
rpc BatchUpdateBooks(BatchUpdateBooksRequest) returns (BatchUpdateBooksResponse) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books:batchUpdate"
    body: "*"
  };
}
```

Returning an `Operation` which resolves to the response asynchronously:

```protobuf
rpc BatchUpdateBooks(BatchUpdateBooksRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books:batchUpdate"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "BatchUpdateBooksResponse"
    metadata_type: "BatchUpdateBooksOperationMetadata"
  };
}
```

**Rules:**
- The RPC's name **must** begin with `BatchUpdate`. The remainder of the RPC name **should** be the plural form of the resource being updated.
- The request and response messages **must** match the RPC name, with `Request` and `Response` suffixes.
- If the batch method returns a `google.longrunning.Operation`, both the `response_type` and `metadata_type` fields **must** be specified.
- The HTTP verb **must** be `POST`.
- The HTTP URI **must** end with `:batchUpdate`.
- The URI path **should** represent the collection for the resource, matching the collection used for simple CRUD operations. If the operation spans parents, a dash (`-`) **may** be accepted as a wildcard.
- The `body` clause in the `google.api.http` annotation **should** be `"*"`.

**Atomic vs. Partial Success**

The batch update method **may** support atomic (all resources updated or none are) or partial success behavior. To make a choice, consider the following factors:

- **Complexity of Ensuring Atomicity:** Operations that are simple passthrough database transactions **should** use an atomic operation, while operations that manage complex resources **should** use partial success operations.
- **End-User Experience:** Consider the perspective of the API consumer. Would atomic behavior be preferable for the given use case, even if it means that a large batch could fail due to issues with a single or a few entries?

- Synchronous batch update **must** be atomic.
- Asynchronous batch update **may** support atomic or partial success.
  - If supporting partial success, see Operation metadata message requirements.

**Request message**

The request for a batch update method **should** be specified with the following pattern:

```protobuf
message BatchUpdateBooksRequest {
  // The parent resource shared by all books being updated.
  // Format: publishers/{publisher}
  // If this is set, the parent field in the UpdateBookRequest messages
  // must either be empty or match this field.
  string parent = 1 [
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // The request message specifying the resources to update.
  // A maximum of 1000 books can be modified in a batch.
  repeated UpdateBookRequest requests = 2
    [(google.api.field_behavior) = REQUIRED];
}
```

- A `parent` field **should** be included, unless the resource being updated is a top-level resource. If a caller sets this field, and the parent collection in the name of any resource being updated does not match, the request **must** fail.
  - This field **should** be required if only 1 parent per request is allowed.
  - The field **should** identify the resource type that it references.
  - The comment for the field **should** document the resource pattern.
- The request message **must** include a repeated field which accepts the request messages specifying the resources to update, as specified for standard Update methods. The field **should** be named `requests`.
  - The field **should** be required.
- Other fields **may** be "hoisted" from the standard Update request, which means that the field can be set at either the batch level or child request level. Similar to `parent`, if both the batch level and child request level are set for the same field, the values **must** match.
  - The `update_mask` field is a good candidate for hoisting.
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.
- The comment above the `requests` field **should** document the maximum number of requests allowed.

**Response message**

The response for a batch update method **should** be specified with the following pattern:

```protobuf
message BatchUpdateBooksResponse {
  // Books updated.
  repeated Book books = 1;
}
```

- The response message **must** include one repeated field corresponding to the resources that were updated.

**Operation metadata message**

- The `metadata_type` message **must** either match the RPC name with `OperationMetadata` suffix, or be named with `Batch` prefix and `OperationMetadata` suffix if the type is shared by multiple Batch methods.
- If the batch update method supports partial success, the metadata message **must** include a `map<int32, google.rpc.Status> failed_requests` field to communicate the partial failures.
  - The key in this map is the index of the request in the `requests` field in the batch request.
  - The value in each map entry **must** mirror the error(s) that would normally be returned by the singular standard Update method.
  - If a failed request can eventually succeed due to server side retries, such transient errors **must not** be communicated using `failed_requests`.
  - When all requests in the batch fail, `Operation.error` **must** be set with `code = google.rpc.Code.Aborted` and `message = "None of the requests succeeded, refer to the BatchUpdateBooksOperationMetadata.failed_requests for individual error details"`.
- The metadata message **may** include other fields to communicate the operation progress.

**Adopting Partial Success**

In order for an existing Batch API to adopt the partial success pattern, the API must do the following:

- The default behavior must be retained to avoid incompatible behavioral changes.
- If the API returns an `Operation`:
  - The request message **must** have a `bool return_partial_success` field.
  - The `Operation` `metadata_type` **must** include a `map<int32, google.rpc.Status> failed_requests` field.
  - When the `bool return_partial_success` field is set to `true` in a request, the API should allow partial success behavior, otherwise it should continue with atomic behavior as default.
- If the API returns a direct response synchronously:
  - Since the existing clients will treat a success response as an atomic operation, the existing version of the API **must not** adopt the partial success pattern.
  - A new version **must** be created instead that returns an `Operation` and follows the partial success pattern described in this AIP.

**Rationale**

***Restricting synchronous batch methods to be atomic***

The restriction that synchronous batch methods must be atomic is a result of the following considerations.

The previous iteration of this AIP recommended batch methods must be atomic. There is no clear way to convey partial failure in a sync response status code because an `OK` implies it all worked. Therefore, adding a new field to the response to indicate partial failure would be a breaking change because the existing clients would interpret an `OK` response as all resources updated.

On the other hand, as described in AIP-193, Operations are more capable of presenting partial states. The response status code for an `Operation` does not convey anything about the outcome of the underlying operation and a client has to check the response body to determine if the operation was successful.

***Communicating partial failures***

The AIP recommends using a `map<int32, google.rpc.Status> failed_requests` field to communicate partial failures, where the key is the index of the failed request in the original batch request. The other options considered were:

- A `repeated google.rpc.Status` field. This was rejected because it is not clear which entry corresponds to which request.
- A `map<string, google.rpc.Status>` field, where the key is the request ID of the failed request. This was rejected because:
  - Client will need to maintain a map of request_id -> request in order to use the partial success response.
  - Populating a request ID for the purpose of communicating errors could conflict with AIP-155 if the service can not guarantee idempotency for an individual request across multiple batch requests.
- A `repeated FailedRequest` field, where `FailedRequest` contains the individual update request and the `google.rpc.Status`. This was rejected because echoing the request payload back in response is discouraged due to additional challenges around user data sensitivity.

> **Agent extension — not part of the AIP standard.** Batch Update follows the same partial-success convention as Batch Create (AIP-233): `map<int32, google.rpc.Status> failed_requests` for synchronous calls or LRO metadata for asynchronous ones. Each item in the batch carries its own `update_mask` semantics — a single shared mask for heterogeneous items is a design smell.

### 5.12 Batch Method: Delete (AIP-235)
[ref: #batch-method-delete-aip-235]

Some APIs need to allow users to delete a set of resources in a single transaction. A batch delete method provides this functionality. APIs **may** support Batch Delete using the following two patterns.

**Purpose:** Delete multiple resources in a single transaction.

Returning the response synchronously:

```protobuf
rpc BatchDeleteBooks(BatchDeleteBooksRequest) returns (google.protobuf.Empty) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books:batchDelete"
    body: "*"
  };
}
```

Returning an `Operation` which resolves to the response asynchronously:

```protobuf
rpc BatchDeleteBooks(BatchDeleteBooksRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books:batchDelete"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "google.protobuf.Empty"
    metadata_type: "BatchDeleteBooksOperationMetadata"
  };
}
```

**Rules:**
- The RPC's name **must** begin with `BatchDelete`. The remainder of the RPC name **should** be the plural form of the resource being deleted.
- The request message **must** match the RPC name, with a `Request` suffix.
- The response message **should** be `google.protobuf.Empty`.
  - If the resource is soft deleted, the response message **should** be a response message containing the updated resources.
- If the batch method returns a `google.longrunning.Operation`, both the `response_type` and `metadata_type` fields **must** be specified.
  - If the resource is soft deleted, the `response_type` **should** be a response message containing the updated resources.
- The HTTP verb **must** be `POST` (not `DELETE`).
- The HTTP URI **must** end with `:batchDelete`.
- The URI path **should** represent the collection for the resource, matching the collection used for simple CRUD operations. If the operation spans parents, a dash (`-`) **may** be accepted as a wildcard.
- The `body` clause in the `google.api.http` annotation **should** be `"*"`.

**Atomic vs. Partial Success**

The batch delete method **may** support atomic (all resources deleted or none are) or partial success behavior. To make a choice, consider the following factors:

- **Complexity of Ensuring Atomicity:** Operations that are simple passthrough database transactions **should** use an atomic operation, while operations that manage complex resources **should** use partial success operations.
- **End-User Experience:** Consider the perspective of the API consumer. Would atomic behavior be preferable for the given use case, even if it means that a large batch could fail due to issues with a single or a few entries?

- Synchronous batch delete **must** be atomic.
- Asynchronous batch delete **may** support atomic or partial success.
  - If supporting partial success, see Operation metadata message requirements.

**Request message**

The request for a batch delete method **should** be specified with the following pattern:

```protobuf
message BatchDeleteBooksRequest {
  // The parent resource shared by all books being deleted.
  // Format: publishers/{publisher}
  // If this is set, the parent of all of the books specified in `names`
  // must match this field.
  string parent = 1 [
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // The names of the books to delete.
  // A maximum of 1000 books can be deleted in a batch.
  // Format: publishers/{publisher}/books/{book}
  repeated string names = 2 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/Book"
    }];
}
```

- A `parent` field **should** be included, unless the resource being deleted is a top-level resource. If a caller sets this field, and the parent collection in the name of any resource being deleted does not match, the request **must** fail.
  - This field **should** be required if only 1 parent per request is allowed.
  - The field **should** identify the resource type that it references.
  - The comment for the field **should** document the resource pattern.
- The request message **must** include a repeated field which accepts the resource names specifying the resources to delete. The field **should** be named `names`.
  - The field **should** be required.
  - The field **should** identify the resource type that it references.
  - The comment for the field **should** document the resource pattern.
- Other fields besides `name` **may** be "hoisted" from the standard Delete request. There is no way to allow for these fields to accept different values for different resources; if this is needed, use the alternative request message form.
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.
- The comment above the `names` field **should** document the maximum number of requests allowed.
- Filter-based matching **must not** be supported.

**Request message containing standard delete request messages**

If the standard Delete request message contains a field besides the resource name that needs to be different between different resources being requested, the batch message **may** alternatively hold a `repeated` field of the standard Delete request message. This is generally discouraged unless your use case really requires it.

The request for a batch delete method using this approach **should** be specified with the following pattern:

```protobuf
message BatchDeleteBooksRequest {
  // The parent resource shared by all books being deleted.
  // Format: publishers/{publisher}
  // If this is set, the parent of all of the books specified in the
  // DeleteBookRequest messages must match this field.
  string parent = 1 [
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // The requests specifying the books to delete.
  // A maximum of 1000 books can be deleted in a batch.
  repeated DeleteBookRequest requests = 2
    [(google.api.field_behavior) = REQUIRED];
}
```

- A `parent` field **should** be included. If a caller sets this field, and the parent collection in the name of any resource being deleted does not match, the request **must** fail.
  - This field **should** be required if only 1 parent per request is allowed.
  - The field **should** identify the resource type that it references.
  - The comment for the field **should** document the resource pattern.
- The request message **must** include a repeated field which accepts the request messages specifying the resources to delete, as specified for standard Delete methods. The field **should** be named `requests`.
  - The field **should** be required.
- Other fields **may** be "hoisted" from the standard Delete request, which means that the field can be set at either the batch level or child request level. Similar to `parent`, if both the batch level and child request level are set for the same field, the values **must** match.
  - Fields which must be unique cannot be hoisted (e.g. `etag`).
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.
- The comment above the `requests` field **should** document the maximum number of requests allowed.
- Filter-based matching **must not** be supported unless it is infeasible to support critical use cases without it, because it makes it too easy for users to accidentally delete important data. If it is unavoidable, see [AIP-165](07_design_patterns.md#criteria-based-delete-aip-165).

**Response message (soft-delete only)**

In the case where a response message is necessary because the resource is soft-deleted, the response **should** be specified with the following pattern:

```protobuf
message BatchDeleteBooksResponse {
  // Books deleted.
  repeated Book books = 1;
}
```

- The response message **must** include one repeated field corresponding to the resources that were soft-deleted.

**Operation metadata message**

- The `metadata_type` message **must** either match the RPC name with `OperationMetadata` suffix, or be named with `Batch` prefix and `OperationMetadata` suffix if the type is shared by multiple Batch methods.
- If the batch delete method supports partial success, the metadata message **must** include a `map<int32, google.rpc.Status> failed_requests` field to communicate the partial failures.
  - The key in this map is the index of the request in the `requests` field in the batch request.
  - The value in each map entry **must** mirror the error(s) that would normally be returned by the singular standard Delete method.
  - If a failed request can eventually succeed due to server side retries, such transient errors **must not** be communicated using `failed_requests`.
  - When all requests in the batch fail, `Operation.error` **must** be set with `code = google.rpc.Code.Aborted` and `message = "None of the requests succeeded, refer to the BatchDeleteBooksOperationMetadata.failed_requests for individual error details"`.
- The metadata message **may** include other fields to communicate the operation progress.

**Adopting Partial Success**

In order for an existing Batch API to adopt the partial success pattern, the API must do the following:

- The default behavior must be retained to avoid incompatible behavioral changes.
- If the API returns an `Operation`:
  - The request message **must** have a `bool return_partial_success` field.
  - The `Operation` `metadata_type` **must** include a `map<int32, google.rpc.Status> failed_requests` field.
  - When the `bool return_partial_success` field is set to `true` in a request, the API should allow partial success behavior, otherwise it should continue with atomic behavior as default.
- If the API returns a direct response synchronously:
  - Since the existing clients will treat a success response as an atomic operation, the existing version of the API **must not** adopt the partial success pattern.
  - A new version **must** be created instead that returns an `Operation` and follows the partial success pattern described in this AIP.

**Rationale**

***Restricting synchronous batch methods to be atomic***

The restriction that synchronous batch methods must be atomic is a result of the following considerations.

The previous iteration of this AIP recommended batch methods must be atomic. There is no clear way to convey partial failure in a sync response status code because an `OK` implies it all worked. Therefore, adding a new field to the response to indicate partial failure would be a breaking change because the existing clients would interpret an `OK` response as all resources deleted.

On the other hand, as described in AIP-193, Operations are more capable of presenting partial states. The response status code for an `Operation` does not convey anything about the outcome of the underlying operation and a client has to check the response body to determine if the operation was successful.

***Communicating partial failures***

The AIP recommends using a `map<int32, google.rpc.Status> failed_requests` field to communicate partial failures, where the key is the index of the failed request in the original batch request. The other options considered were:

- A `repeated google.rpc.Status` field. This was rejected because it is not clear which entry corresponds to which request.
- A `map<string, google.rpc.Status>` field, where the key is the request ID of the failed request. This was rejected because:
  - Client will need to maintain a map of request_id -> request in order to use the partial success response.
  - Populating a request ID for the purpose of communicating errors could conflict with AIP-155 if the service can not guarantee idempotency for an individual request across multiple batch requests.
- A `repeated FailedRequest` field, where `FailedRequest` contains the individual delete request and the `google.rpc.Status`. This was rejected because echoing the request payload back in response is discouraged due to additional challenges around user data sensitivity.

> **Agent extension — not part of the AIP standard.** Batch Delete shares the partial-success reporting pattern (`failed_requests` index map or LRO metadata). Decide explicitly whether deleting an already-absent resource counts as success or as a per-item `NOT_FOUND` failure, and document the choice — idempotent retries of a partially failed batch depend on it.
