## 10. Protocol Buffers

### 10.1 HTTP and gRPC Transcoding (AIP-127)
[ref: #http-and-grpc-transcoding-aip-127]

APIs that follow resource-oriented design are defined using RPCs, but the resource-oriented design framework allows them to also be presented as APIs that largely follow REST/JSON conventions. This is important in order to help developers use their existing knowledge: over 80% of the public APIs available follow most REST conventions, and developers are accustomed to that pattern.

APIs **must** provide HTTP definitions for each RPC that they define, except for bi-directional streaming RPCs, which can not be natively supported using HTTP/1.1. When providing a bi-directional streaming method, an API **should** also offer an alternative method that does not rely on bi-directional streaming.

**Note:** Bi-directional streaming RPCs should not include a `google.api.http` annotation at all. If feasible, the service **should** provide non-streaming equivalent RPCs.

#### HTTP method and path

When using protocol buffers, each RPC **must** define the HTTP method and path using the `google.api.http` annotation:

```protobuf
rpc CreateBook(CreateBookRequest) returns (Book) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books"
    body: "book"
  };
}

message CreateBookRequest {
  // The publisher who will publish this book.
  // When using HTTP/JSON, this field is automatically populated based
  // on the URI, because of the `{parent=publishers/*}` syntax.
  string parent = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // The book to create.
  // When using HTTP/JSON, this field is populated based on the HTTP body,
  // because of the `body: "book"` syntax.
  Book book = 2 [(google.api.field_behavior) = REQUIRED];

  // The user-specified ID for the book.
  // When using HTTP/JSON, this field is populated based on a query string
  // argument, such as `?bookId=foo`. This is the fallback for fields that
  // are not included in either the URI or the body.
  // Note that clients use camelCase format to communicate the field names
  // to the service.
  string book_id = 3;
}
```

- The first key (`post` in this example) corresponds to the HTTP method. RPCs **may** use `get`, `post`, `patch`, or `delete`.
  - RPCs **must** use the prescribed HTTP verb for each standard method, as discussed in AIP-131, AIP-132, AIP-133, AIP-134, and AIP-135.
  - RPCs **should** use the prescribed HTTP verb for custom methods, as discussed in AIP-136.
  - RPCs **should not** use `put` or `custom`.
- The corresponding value represents the URI.
  - URIs **must** use the `{foo=bar/*}` syntax to represent a variable that should be populated in the request proto. When extracting a resource name, the variable **must** include the entire resource name, not just the ID component.
  - URIs **may** use nested fields for their variable names. (Additionally, AIP-134 mandates this for `Update` requests.)
  - URIs **must** use the `*` character to represent ID components, which matches all URI-safe characters except for `/`. URIs **may** use `**` as the final segment of a URI if matching `/` is required.
- The `body` key defines which single top-level field in the request will be sent as the HTTP body. If the body is `*`, then this indicates that the request object itself is the HTTP body. The request body is encoded as JSON as defined by protocol buffers' canonical JSON encoding.
  - RPCs **must not** define a `body` at all for RPCs that use the `GET` or `DELETE` HTTP verbs.
  - RPCs **must** use the prescribed `body` for Create (AIP-133) and Update (AIP-134) requests.
  - RPCs **should** use the prescribed `body` for custom methods (AIP-136).
  - The `body` **must not** contain a nested field (or use the `.` character).
  - The `body` **must not** be the same as a URI parameter.
  - The `body` **must not** be a `repeated` field.
  - Fields **should not** use the `json_name` annotation to alter the field name in JSON, unless doing so for backwards-compatibility reasons.

#### Multiple URI bindings

Occasionally, an RPC needs to correspond to more than one URI:

```protobuf
rpc CreateBook(CreateBookRequest) returns (Book) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books"
    body: "book"
    additional_bindings: {
      post: "/v1/{parent=authors/*}/books"
      body: "book"
    }
    additional_bindings: {
      post: "/v1/books"
      body: "book"
    }
  };
}
```

- RPCs **may** define any number of additional bindings. The structure is identical to the `google.api.http` annotation (in fact, it is a recursive reference).
- RPCs **must not** define an additional binding within an additional binding.
- The `body` clause **must** be identical in the top-level annotation and each additional binding.

### 10.2 Common Components (AIP-213)
[ref: #common-components-aip-213]

As specified in AIP-215, APIs **must** be self-contained except for the use of "common component" packages which are intended for use by multiple APIs.

There are two kinds of common component packages:

- **Organization-specific common components**, covering organization-specific concepts such as a "viewport" in Maps.
- **Global common components** which are generic (i.e. not domain-specific), such as "timestamp" or "postal address".

Where it is safe to share a single representation across multiple APIs, common components can make it easier for clients to interact with those APIs. Concept-specific client code can be written once, and messages can be used from the response of one API in the request of another without clunky copying, for example.

This benefit comes with significant restrictions and limitations, however, and should not be attempted lightly.

Note that even if the _domain_ of a component is common, the requirements of a component may be organization-specific. For example, some organizations may have particular requirements of how financial values are represented, leading to multiple finance-oriented organization-specific common components — because any global common component would either not meet the organization-specific requirements, or be too complex for general use.

#### Guidance

- Organization-wide common component packages **must** end with `.type`, e.g. `google.geo.type` or `google.shopping.type`.
- Organizations **must** consult the API design team before creating a new organization-wide common component package.
- Organization-wide common component packages **must** be published in the `googleapis` repository.
- Organizations creating and publishing a new organization-wide common component package **must** update this AIP to include it in the list below.
- Organizations **must not** define generic components in organization-specific common component packages, instead preferring global common components.
- Common components **must not** be "moved" (that is, deleted from one common component package and added to a different one) from an organization-specific common component package to a global common component package or vice versa.
  - A common component **may** be copied from an organization-specific common component package to a global common component package (without deleting the original component) if it is found to be more widely-applicable than originally expected.
- Fields **should not** be added to existing messages.
- Values **should not** be added to existing enums.
- Fields **must not** be removed from existing messages.
- Values **must not** be removed from existing enums.
- While documentation **may** be clarified, it **should not** change the meanings of existing values, including the validity of any given message or set of messages.
- New proto messages and enums **may** be added to common component packages.
  - API teams **should** allow sufficient time for propagation to clients before using the new messages and enums in their APIs. Fields may take some time for any changes to propagate through publication to client libraries and other surfaces.
  - API teams **should** consult widely within their organization, and ideally with the API design team, before adding a new message or enum, due to the limitations listed above.

#### Existing global common components

The global common components, which public-facing protos for an API **may** safely import, are as follows:

- `google.api.*` (but _not_ subpackages of `google.api`)
- `google.longrunning.Operation`
- `google.protobuf.*`
- `google.rpc.*`
- `google.type.*`

Note that some common components may have internal-only fields. APIs **should** generally only rely on fields which have been released into open source.

Google APIs **may** also import `google.iam.v1.*`, which provides the IAM messages used throughout Google.

**Note:** Many APIs also import components from other packages for internal-only use (e.g. to apply visibility labels or provide instructions to internal infrastructure). This is acceptable provided that the _public_ components do not contain such references.

##### Protobuf types

The `google.protobuf` package is somewhat special in that it is shipped with protocol buffers itself, rather than with API tooling. (For most API designers, this should be an implementation detail).

This package includes a small library of types useful for representing common programming language constructs:

- `google.protobuf.Duration`: Durations, with nanosecond-level precision. The protobuf runtime provides helper functions to convert to and from language-native duration objects where applicable (such as Python's `timedelta`).
- `google.protobuf.Struct`: JSON-like structures (a dictionary of primitives, lists, and other dictionaries). The protobuf runtime provides helper functions in most languages to convert struct objects to and from JSON.
- `google.protobuf.Timestamp`: Timestamps, with nanosecond-level precision. The protobuf runtime provides helper functions in most languages to convert to and from language-native timestamp objects (such as Python's `datetime`).

##### API Types

The `google.type` package provides a "standard library" of types useful for representing common concepts in APIs. While types are added from time to time and the definitive list is always the code, several types deserve note:

- `google.type.Color`: RGB or RGBA colors.
- `google.type.Date`: Calendar dates, with no time or time zone component.
- `google.type.DayOfWeek`: The day of the week, with no other date, time, or time zone component.
- `google.type.LatLng`: Geographic coordinates.
- `google.type.Money`: Currency.
- `google.type.PostalAddress`: Postal addresses in most countries.
- `google.type.TimeOfDay`: Wall-clock time, with no date or time zone component.

#### Adding to common protos

Occasionally, it may be useful to add protos to these packages or to add to the list of commonly-available protos. In order to do this, open an issue on the AIP repository in GitHub, noting the guidelines above.

#### Existing organization-specific common component packages

The following organization-specific common component packages exist and conform with the above guidance:

- `google.apps.script.type`
  Common component package for Google Apps Script.
- `google.geo.type`
  Common component package for Google Maps and the Geo organization.
- `google.actions.type`
  Common component package for Actions on Google APIs.

#### Non-conformant common component packages

The following common component packages exist, but do not conform with the above guidance, and do not form a precedent for further such packages.

- `google.cloud.common`:
  This does not conform to the requirement for the package name to end in `.type`. (This would otherwise be acceptable, and this package should be considered as the Cloud common component package.)
- `google.logging.type`:
  This appears to be API-specific, although it's used from multiple APIs; some aspects should probably be global or in a Cloud common component package.
- `google.cloud.workflows.type`:
  API-specific types.
- `google.cloud.oslogin.common`:
  API-specific types, and a non-conformant name.
- `google.identity.accesscontextmanager.type`:
  API-specific types.
- `google.networking.trafficdirector.type`:
  API-specific types.

#### Rationale

Common components are effectively unversioned: APIs evolve independently of each other, both in terms of definition and implementation. A change such as adding a field is backward-compatible and predictable in specific APIs, and the API team can ensure that the server implementation is available before the API definition is published. By contrast, a change in a common component would effectively be universally available even if most API implementations did not take it into account.

Adding a new message or enum is backward-compatible, as it does not affect existing APIs that may import other messages or enums from the same common component package.

Consultation with the API design team is required for global common components and suggested for organization-specific common components as the border between "generic" and "organization-specific" is a gray area; some generic _concepts_ have organization-specific use cases which surface through the components.

### 10.3 API-Specific Protos (AIP-215)
[ref: #api-specific-protos-aip-215]

APIs are mostly defined in terms of protos which are API-specific, with occasional dependencies on common components. Keeping APIs isolated from each other avoids versioning problems and client library packaging problems.

#### Guidance

- All protos specific to an API **must** be within a package with a major version (e.g., `google.library.v1`).
- References to resources in other APIs **must** be expressed in terms of resource names (AIP-122), rather than using the resource messages.
- When two versions of an API use effectively the same (API-specific) proto, that proto **must** be duplicated in each version. (In other words, APIs **must not** create their own "API-specific common component" packages.)
- Organization-specific common components **may** be placed in a common package, as described in AIP-213, but **must not** be used by any API outside that organization.
- Global common components (also described in AIP-213) **may** be freely used by any API.

#### Rationale

When one API depends on protos defined by another API, this introduces uncertainty in terms of customer-expected behavior and client library dependency management. Suppose `google.cloud.library.v1` depends on the protos (rather than abstract resources) in `google.cloud.movies.v2`. Any change to `google.cloud.movies.v2` can cause problems.

For example:

- If a field is added to a message in `google.cloud.movies.v2`, should customers using `google.cloud.library.v1` expect to see it? If so, how soon after the field has been added? What about other API changes?
- If the whole major version `google.cloud.movies.v2` is deprecated (typically after v3 has been released), does that mean `google.cloud.library.v1` has to change to use `google.cloud.movies.v3`, and if so, does that require a new major version for the library API as well?
- How should client library versioning reflect changes to dependent APIs?

Keeping APIs isolated from each other, with a limited set of common components which are maintained in a highly disciplined way, reduces a lot of the issues with dependencies.

API-specific common components shared across versions add complexity for client library generation and packaging, and are inflexible in terms of versioning. When protos are duplicated because they _start_ off the same in multiple versions, they can still diverge over time as they are isolated from each other.
