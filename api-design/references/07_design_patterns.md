## 7. Design Patterns

### 7.1 Jobs (AIP-152)
[ref: #jobs-aip-152]

Occasionally, APIs may need to expose a task that takes significant time to complete, and where a transient long-running operation is not appropriate. For example, a task could need to run repeatedly, or have separate permissions for configuring the task as opposed to running it.

#### Guidance

An API **may** define a `Job` resource to represent a particular task with distinct setup, configuration, and execution:

```protobuf
message WriteBookJob {
  option (google.api.resource) = {
    type: "library.googleapis.com/WriteBookJob"
    pattern: "publishers/{publisher}/writeBookJobs/{write_book_job}"
  };

  // Name and other fields...
}
```

- The name of the resource **must** end with the word `Job`.
  - The prefix **should** be a valid RPC name, with a verb and a noun.
- The service **should** define all five of the standard methods ([AIP-131](05_operations.md#standard-method-get-aip-131), [AIP-132](05_operations.md#standard-method-list-aip-132), [AIP-133](05_operations.md#standard-method-create-aip-133), [AIP-134](05_operations.md#standard-method-update-aip-134), [AIP-135](05_operations.md#standard-method-delete-aip-135)), and use them as the primary way to configure the job.

#### Run method

The service **should** define a `Run` custom method that executes the job immediately:

```protobuf
rpc RunWriteBookJob(RunWriteBookJobRequest)
    returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{name=publishers/*/writeBookJobs/*}:run"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "RunWriteBookJobResponse"
    metadata_type: "RunWriteBookJobMetadata"
  };
}
```

- The RPC's name **must** begin with the word `Run`. The remainder of the RPC name **should** be the singular form of the job resource being run.
- The request message **must** match the RPC name, with a `Request` suffix.
- The method **should** return a long-running operation, which **must** resolve to a response message that includes the result of running the job.
  - The response message name **must** match the RPC name, with a `Response` suffix.
  - The method **may** use any metadata message it wishes.
- The HTTP verb **must** be `POST`, as is usual for custom methods.
- The body clause in the `google.api.http` annotation **should** be `"*"`.
- The URI path **should** contain a single `name` variable corresponding to the name of the job resource being run.
- The URI path **must** end with `:run`.
- Errors that prevent execution of the job from *starting* **must** return an error response ([AIP-193](09_polish.md#errors-aip-193)), similar to any other method. Errors that occur over the course of the job execution **may** be placed in the metadata message. The errors themselves **must** still be represented with a `google.rpc.Status` object.

#### Run request message

Run methods implement a common request message pattern:

```protobuf
message RunWriteBookJobRequest {
  // The name of the job to run.
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/WriteBookJob"
    }];
}
```

- A singular `string name` field **must** be included.
  - The field **should** be annotated as required.
  - The field **should** identify the resource type that it references.

#### Executions and results

Ordinarily, the API **should** provide results to the user as the final response of the `Run` method. However, this is sometimes insufficient; for example, a job that runs on a recurring schedule in the background can not deliver results to the user in this way.

The service **may** store resources representing individual executions along with their result as a sub-collection of resources under the job, which allows the user to list *past* job executions. A service that does this **should** define the `Get`, `List`, and `Delete` methods for the execution resources:

```protobuf
message WriteBookJobExecution {
  option (google.api.resource) = {
    type: "library.googleapis.com/WriteBookJobExecution"
    pattern: "publishers/{publisher}/writeBookJobs/{write_book_job}/executions/{execution}"
  };

  // Name and other information about the execution, such as metadata, the
  // result, error information, etc.
}
```

In this case, the operation returned by the job's `Run` method **should** refer to the child resource.

### 7.2 Import and Export (AIP-153)
[ref: #import-and-export-aip-153]

Many users want to be able to load data into an API, or get their existing data out of an API. This is particularly important for enterprise users, who are often concerned about vendor lock-in.

#### Guidance

APIs **may** support import and export operations, which **may** create multiple new resources, or they **may** populate data into a single resource.

#### Multiple resources

Services **may** support importing and exporting multiple resources into or out of an API, and **should** implement a common pattern to do so:

```protobuf
rpc ImportBooks(ImportBooksRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books:import"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "ImportBooksResponse"
    metadata_type: "ImportBooksMetadata"
  };
}

rpc ExportBooks(ExportBooksRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books:export"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "ExportBooksResponse"
    metadata_type: "ExportBooksMetadata"
  };
}
```

- The method **must** return a long-running operation (see [AIP-151](05_operations.md#long-running-operations-aip-151)) unless the service can guarantee that it will *never* need more than a few seconds to complete.
- The HTTP verb **must** be `POST`, and the `body` **must** be `"*"`.
- A `parent` field **should** be included as part of the URI.
  - If importing into or exporting from multiple resources is required, the API **should** keep the `parent` field and allow the user to use the `-` character to indicate multiple parents (see [AIP-159](07_design_patterns.md#reading-across-collections-aip-159)).
  - On import, if the user provides a specific parent, the API **must** reject any imported resources that would be added to a different parent.
- The URI suffix **should** be `:import` or `:export`.

#### Data for a single resource

Services **may** support importing and exporting data into or out of a single resource, and **should** implement a common pattern to do so:

```protobuf
rpc ImportPages(ImportPagesRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{book=publishers/*/books/*}:importPages"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "ImportPagesResponse"
    metadata_type: "ImportPagesMetadata"
  };
}

rpc ExportPages(ExportPagesRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{book=publishers/*/books/*}:exportPages"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "ExportPagesResponse"
    metadata_type: "ExportPagesMetadata"
  };
}
```

- The method **must** return a long-running operation (see [AIP-151](05_operations.md#long-running-operations-aip-151)) unless the service can guarantee that it will *never* need more than a few seconds to complete.
- The HTTP verb **must** be `POST`, and the `body` **must** be `"*"`.
- A field representing the resource that data is being imported into **should** be included as part of the URI. The field **should** be named after the resource (and **should not** be called `name`).
- The URI suffix **should** include both the verb and a noun for the data itself, such as `:importPages` or `:exportPages`.

#### Request object

Imports and exports often require two fundamentally different types of configuration:

1. Configuration specific to the source or destination.
2. Configuration regarding the imported or exported data itself.

Source or destination configuration should be grouped into a single message and placed inside a `oneof`:

```protobuf
message ImportBooksRequest {
  string parent = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];
  oneof source {
    AuthorSource author_source = 2;
    TranslatorSource translator_source = 3;
  }
  string isbn_prefix = 4;
}

message ExportBooksRequest {
  string parent = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];
  oneof destination {
    PrinterDestination printer_destination = 2;
    TranslatorDestination translator_destination = 3;
  }
  string filter = 4;
}
```

- The source configuration messages **must** be placed within a `oneof source` (for import) or `oneof destination` (for export), even if there is only one. (This maintains flexibility to add more later.)
- Configuration related to the data itself (and therefore common across all sources) **must** be placed at the top-level of the request message.

**Note:** The configuration for import and export **may** be different from one another. (For example, it would be sensible to import from a file but export to a directory.)

#### Inline sources

APIs **may** also permit import and export "inline", where the contents to be imported or exported are provided in the request or response.

```protobuf
message InlineSource {
  repeated Book books = 1;
}
```

- The source or destination **should** be named `InlineSource` or `InlineDestination`.
- The message **should** include a repeated field representing the resource. However, if the resource structure is complex, the API **may** use a separate inline representation. In this situation, the same format **must** be used for both import and export.

#### Partial failures

While partial failures are normally discouraged, import and export RPCs **should** include partial failure information in the metadata object. Each individual error **should** be a `google.rpc.Status` object describing the error. For more on errors, see [AIP-193](09_polish.md#errors-aip-193).

### 7.3 Resource Freshness Validation (AIP-154)
[ref: #resource-freshness-validation-aip-154]

APIs often need to validate that a client and server agree on the current state of a resource before taking some kind of action on that resource. For example, two processes updating the same resource in parallel could create a race condition, where the latter process "stomps over" the effort of the former one.

ETags provide a way to deal with this, by allowing the server to send a checksum based on the current content of a resource; when the client sends that checksum back, the server can ensure that the checksums match before acting on the request.

#### Guidance

A resource **may** include an `etag` field on any resource where it is important to ensure that the client has an up to date resource before acting on certain requests:

```protobuf
// A representation of a book.
message Book {
  // Other fields...

  // This checksum is computed by the server based on the value of other
  // fields, and may be sent on update and delete requests to ensure the
  // client has an up-to-date value before proceeding.
  string etag = 99;
}
```

- The `etag` field **must** be a `string`, and **must** be named `etag`.
- The `etag` field on the *resource* **should not** be given any behavior annotations.
- The `etag` field **must** be provided by the server on output, and values **should** conform to RFC 7232.
- If a user sends back an `etag` which matches the current `etag` value, the service **must** permit the request (unless there is some other reason for failure).
- If a user sends back an `etag` which does not match the current `etag` value, the service **must** send an `ABORTED` error response (unless another error takes precedence, such as `PERMISSION_DENIED` if the user is not authorized).
- If the user does not send an `etag` value at all, the service **should** permit the request. However, services with strong consistency or parallelism requirements **may** require users to send etags all the time and reject the request with an `INVALID_ARGUMENT` error in this case.

**Note:** ETag values **should** include quotes as described in RFC 7232. For example, a valid etag is `"foo"`, not `foo`.

#### Declarative-friendly resources

A resource that is declarative-friendly ([AIP-128](04_resource_design.md#declarative-friendly-interfaces-aip-128)) **must** include an `etag` field.

#### Etags on request methods

In some situations, the `etag` needs to belong on a request message rather than the resource itself. For example, an `Update` standard method can "piggyback" off the `etag` field on the resource, but the `Delete` standard method can not:

```protobuf
message DeleteBookRequest {
  // The name of the book.
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/Book"
    }];

  // The current etag of the book.
  // If an etag is provided and does not match the current etag of the book,
  // deletion will be blocked and an ABORTED error will be returned.
  string etag = 2 [(google.api.field_behavior) = OPTIONAL];
}
```

On a request message, the `etag` field **should** be given a behavior annotation — either `REQUIRED` or `OPTIONAL`. See [AIP-203](06_fields.md#field-behavior-documentation-aip-203) for more information.

An `etag` field **may** also be used on custom methods, similar to the example above.

#### Strong and weak etags

ETags can be either "strongly validated" or "weakly validated":

- A strongly validated etag means that two resources bearing the same etag are byte-for-byte identical.
- A weakly validated etag means that two resources bearing the same etag are equivalent, but may differ in ways that the service does not consider to be important.

Resources **may** use either strong or weak etags, as it sees fit, but **should** document the behavior. Additionally, weak etags **must** have a `W/` prefix as mandated by RFC 7232.

### 7.4 Request Identification (AIP-155)
[ref: #request-identification-aip-155]

It is sometimes useful for an API to have a unique, customer-provided identifier for particular requests. This can be useful for several purposes, such as de-duplicating requests from parallel processes, ensuring the safety of retries, or auditing.

The most important purpose for request IDs is to provide idempotency guarantees: allowing the same request to be issued more than once without subsequent calls having any effect. In the event of a network failure, the client can retry the request, and the server can detect duplication and ensure that the request is only processed once.

#### Guidance

APIs **may** add a `string request_id` parameter to request messages (including those of standard methods) in order to uniquely identify particular requests.

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

  // A unique identifier for this request. Restricted to 36 ASCII characters.
  // A random UUID is recommended.
  // This request is only idempotent if a `request_id` is provided.
  string request_id = 4 [(google.api.field_info).format = UUID4];
}
```

- Providing a request ID **must** guarantee idempotency.
  - If a duplicate request is detected, the server **should** return the response for the previously successful request, because the client most likely did not receive the previous response.
  - APIs **may** choose any reasonable timeframe for honoring request IDs.
- The `request_id` field **must** be provided on the request message to which it applies (and it **must not** be a field on resources themselves).
- Request IDs **should** be optional.
- Request IDs **should** be able to be UUIDs, and **may** allow UUIDs to be the only valid format. The format restrictions for request IDs **must** be documented.
  - Request IDs that are UUIDs **must** be annotated with the `google.api.FieldInfo.Format` value `UUID4` using the extension `(google.api.field_info).format = UUID4`. See [AIP-202](06_fields.md#fields-and-fieldinfo-aip-202) for more.

#### Stale success responses

In some unusual situations, it may not be possible to return an identical success response. For example, a duplicate request to create a resource may arrive after the resource has not only been created, but subsequently updated; because the service has no other need to retain the historical data, it is no longer feasible to return an identical success response.

In this situation, the method **may** return the current state of the resource instead. In other words, it is permissible to substitute the historical success response with a similar response that reflects more current data.

#### Rationale

##### Using UUIDs for request identification

When a value is required to be unique, leaving the format open-ended can lead to API consumers incorrectly providing a duplicate identifier. As such, standardizing on a universally unique identifier drastically reduces the chance for collisions when done correctly.

### 7.5 Partial Responses (AIP-157)
[ref: #partial-responses-aip-157]

Sometimes, a resource can be either large or expensive to compute, and the API needs to give the user control over which fields it sends back.

#### Guidance

APIs **may** support partial responses in one of two ways:

#### Field masks parameter

Field masks (`google.protobuf.FieldMask`) can be used for granting the user fine-grained control over what fields are returned. An API **should** support the mask in a side channel. For example, the parameter can be specified either using an HTTP query parameter, an HTTP header, or a gRPC metadata entry.

Field masks **should not** be specified in the request message.

- The value of the field mask parameter **must** be a `google.protobuf.FieldMask`.
- The field mask parameter **must** be optional:
  - An explicit value of `"*"` **should** be supported, and **must** return all fields.
  - If the field mask parameter is omitted, it **must** default to `"*"`, unless otherwise documented.
- An API **may** allow read masks with non-terminal repeated fields (unlike update masks), but is not obligated to do so.

**Note:** Changing the default value of the field mask parameter is a breaking change.

#### View enumeration

Alternatively, an API **may** support partial responses with view enums. View enums are useful for situations where an API only wants to expose a small number of permutations to the user:

```protobuf
enum BookView {
  // The default / unset value.
  // The API will default to the BASIC view.
  BOOK_VIEW_UNSPECIFIED = 0;

  // Include basic metadata about the book, but not the full contents.
  // This is the default value (for both ListBooks and GetBook).
  BOOK_VIEW_BASIC = 1;

  // Include everything.
  BOOK_VIEW_FULL = 2;
}
```

- The enum **should** be specified as a `view` field on the request message.
- The enum **should** be named something ending in `View`.
- The enum **should** at minimum have values named `BASIC` and `FULL` (although it **may** have values other than these).
- The `UNSPECIFIED` value **must** be valid (not an error), and the API **must** document what the unspecified value will do.
  - For List RPCs, the effective default value **should** be `BASIC`.
  - For the following RPC types, the effective default value **should** be either `BASIC` or `FULL`:
    - Get
    - Create
    - Update
    - Soft Delete
    - Custom Method
- The enum **should** be defined at the top level of the proto file (as it is likely to be needed in multiple requests, e.g. both `Get` and `List`). See [AIP-126](04_resource_design.md#enumerations-aip-126) for more guidance on top-level enumerations.
- APIs **may** add fields to a given view over time. APIs **must not** remove a field from a given view (this is a breaking change).

**Note:** If a service requires (or might require) multiple views with overlapping but distinct values, there is a potential for a namespace conflict. In this situation, the service **should** nest the view enum within the individual resource.

**Note:** Having a partial response be the default of standard methods can degrade the effectiveness of declarative clients. Providing a mechanism to request the full resource be populated in the response, like this View pattern, is preferred if partial responses are deemed necessary.

#### Read masks as a request field

**Warning:** Read mask as a single, explicit field on the request message is **DEPRECATED**. The system parameter **must** be used instead. The following guidance is for the benefit of existing legacy and external usage.

An API **may** support read masks as a single field on the request message: `google.protobuf.FieldMask read_mask`.

- The read mask **must** be a `google.protobuf.FieldMask` and **should** be named `read_mask`.
- The field mask **should** be optional:
  - An explicit value of `"*"` **should** be supported, and **must** return all fields.
  - If the field mask parameter is not provided, all fields **must** be returned.
- An API **may** allow read masks with non-terminal repeated fields (unlike update masks), but is not obligated to do so.

#### Rationale

##### Deprecating `read_mask` in request messages

As mentioned, API infrastructure implements a service-wide response field filtering mechanism, so there is no need for individual API methods to specify a `read_mask` in their request schema. Doing so is both redundant and a potential point of conflict for the client or service.

### 7.6 Pagination (AIP-158)
[ref: #pagination-aip-158]

APIs often need to provide collections of data, most commonly in the List standard method. However, collections can often be arbitrarily sized, and also often grow over time, increasing lookup time as well as the size of the responses being sent over the wire. Therefore, it is important that collections be paginated.

#### Guidance

RPCs returning collections of data **must** provide pagination *at the outset*, as it is a backwards-incompatible change to add pagination to an existing method.

```protobuf
// The request structure for listing books.
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

// The response structure from listing books.
message ListBooksResponse {
  // The books from the specified publisher.
  repeated Book books = 1;

  // A token that can be sent as `page_token` to retrieve the next page.
  // If this field is omitted, there are no subsequent pages.
  string next_page_token = 2;
}
```

- Request messages for collections **should** define an `int32 page_size` field, allowing users to specify the maximum number of results to return.
  - The `page_size` field **must not** be required.
  - If the user does not specify `page_size` (or specifies `0`), the API chooses an appropriate default, which the API **should** document. The API **must not** return an error.
  - If the user specifies `page_size` greater than the maximum permitted by the API, the API **should** coerce down to the maximum permitted page size.
  - If the user specifies a negative value for `page_size`, the API **must** send an `INVALID_ARGUMENT` error.
  - The API **may** return fewer results than the number requested (including zero results), even if not at the end of the collection.
- Request messages for collections **should** define a `string page_token` field, allowing users to advance to the next page in the collection.
  - The `page_token` field **must not** be required.
  - If the user changes the `page_size` in a request for subsequent pages, the service **must** honor the new page size.
  - The user is expected to keep all other arguments to the RPC the same; if any arguments are different, the API **should** send an `INVALID_ARGUMENT` error.
- The response **must not** be a streaming response.
- Response messages for collections **should** define a `string next_page_token` field, providing the user with a page token that may be used to retrieve the next page.
  - The field containing pagination results **should** be the first field in the message and have a field number of `1`. It **should** be a repeated field containing a list of resources constituting a single page of results.
  - If the end of the collection has been reached, the `next_page_token` field **must** be empty. This is the *only* way to communicate "end-of-collection" to users.
  - If the end of the collection has not been reached (or if the API can not determine in time), the API **must** provide a `next_page_token`.
- Response messages for collections **may** provide an `int32 total_size` field, providing the user with the total number of items in the list.
  - This total **may** be an estimate (but the API **should** explicitly document that).

#### Skipping results

The request definition for a paginated operation **may** define an `int32 skip` field to allow the user to skip results.

The `skip` value **must** refer to the number of individual resources to skip, not the number of pages.

For example:

- A request with no page token and a `skip` value of `30` returns a single page of results starting with the 31st result.
- A request with a page token corresponding to the 51st result (because the first 50 results were returned on the first page) and a `skip` value of `30` returns a single page of results starting with the 81st result.

If a `skip` value is provided that cannot be fulfilled e.g. due to latency of querying a massive data set, the response **must** be `200 OK` with an empty result set. If it is *known* to put the cursor beyond the total size of the collection, the response **must not** include a `next_page_token`.

#### Opacity

Page tokens provided by APIs **must** be opaque (but URL-safe) strings, and **must not** be user-parseable. This is because if users are able to deconstruct these, *they will do so*. This effectively makes the implementation details of your API's pagination become part of the API surface, and it becomes impossible to update those details without breaking users.

**Warning:** Base-64 encoding an otherwise-transparent page token is **not** a sufficient obfuscation mechanism.

For page tokens which do not need to be stored in a database, and which do not contain sensitive data, an API **may** obfuscate the page token by defining an internal protocol buffer message with any data needed, and send the serialized proto, base-64 encoded.

Page tokens **must** be limited to providing an indication of where to continue the pagination process only. They **must not** provide any form of authorization to the underlying resources, and authorization **must** be performed on the request as with any other regardless of the presence of a page token.

#### Expiring page tokens

Many APIs store page tokens in a database internally. In this situation, APIs **may** expire page tokens a reasonable time after they have been sent, in order not to needlessly store large amounts of data that is unlikely to be used. It is not necessary to document this behavior.

**Note:** While a reasonable time may vary between APIs, a good rule of thumb is three days.

#### Backwards compatibility

Adding pagination to an existing RPC is a backwards-incompatible change. This may seem strange; adding fields to proto messages is generally backwards compatible. However, this change is *behaviorally* incompatible.

Consider a user whose collection has 75 resources, and who has already written and deployed code. If the API later adds pagination fields, and sets the default to 50, then that user's code breaks; it was getting all resources, and now is only getting the first 50 (and does not know to advance pagination). Even if the API set a higher default limit, such as 100, the user's collection could grow, and *then* the code would break.

Additionally, client libraries implement automatic pagination, typically representing paginated RPCs using different method signatures to unpaginated ones. This means that adding pagination to a previously-unpaginated method causes a breaking change in those libraries.

For this reason, it is important to always add pagination to RPCs returning collections *up front*; they are consistently important, and they can not be added later without causing problems for existing users.

**Warning:** This also entails that, in addition to presenting the pagination fields, they **must** be *actually implemented* with a non-infinite default value. Implementing an in-memory version (which might fetch everything then paginate) is reasonable for initially-small collections.

#### Rationale

##### Degraded `skip` response

Large collections, complex queries, and globally distributed data can all contribute to a paginated method being unable to quickly or confidently fulfill a given `skip` request. Backend queries can timeout, data collation can take time, and the end user experience need not suffer as a result. In such cases, the pagination interface can be leveraged to keep the client engaged by providing a `next_page_token`, while the service collects an appropriate result. When the service has definitively determined that the requested `skip` exceeds the available results, the pagination interface is again applied and `next_page_token` is omitted to signal the end of results.

### 7.7 Reading Across Collections (AIP-159)
[ref: #reading-across-collections-aip-159]

Sometimes, it is useful for a user to be able to retrieve resources across multiple collections, or retrieve a single resource without needing to know what collection it is in.

#### Guidance

APIs **may** support reading resources across multiple collections by allowing users to specify a `-` (the hyphen or dash character) as a wildcard character in a standard `List` method:

```
GET /v1/publishers/-/books?filter=...
```

- The URI pattern **must** still be specified with `*` and permit the collection to be specified; a URI pattern **must not** hard-code the `-` character.
- The method **must** explicitly document that this behavior is supported.
- The resources provided in the response **must** use the canonical name of the resource, with the actual parent collection identifiers (instead of `-`).
- Services **may** support reading across collections on `List` requests regardless of whether the identifiers of the child resources are guaranteed to be unique. However, services **must not** support reading across collections on `Get` requests if the child resources might have a collision.
- Cross-parent requests **should not** support `order_by`. If they do, the field **must** document that it is best effort. This is because cross-parent requests introduce ambiguity around ordering, especially if there is difficulty reaching a parent (see [AIP-217](07_design_patterns.md#unreachable-resources-aip-217)).

**Important:** If listing across multiple collections introduces the possibility of partial failures due to unreachable parents (such as when listing across locations), the method **must** indicate this following the guidance in [AIP-217](07_design_patterns.md#unreachable-resources-aip-217).

#### Unique resource lookup

Sometimes, a resource within a sub-collection has an identifier that is unique across parent collections. In this case, it may be useful to allow a `Get` method to retrieve that resource without knowing which parent collection contains it. In such cases, APIs **may** allow users to specify the wildcard collection ID `-` (the hyphen or dash character) to represent any parent collection:

```
GET https://example.googleapis.com/v1/publishers/-/books/{book}
```

- The URI pattern **must** still be specified with `*` and permit the collection to be specified; a URI pattern **must not** hard-code the `-` character.
- The method **must** explicitly document that this behavior is supported.
- The resource name in the response **must** use the canonical name of the resource, with actual parent collection identifiers (instead of `-`). For example, the request above returns a resource with a name like `publishers/123/books/456`, *not* `publishers/-/books/456`.
- The resource ID **must** be unique within parent collections.

### 7.8 Filtering (AIP-160)
[ref: #filtering-aip-160]

Often, when listing resources (using a list method as defined in [AIP-132](05_operations.md#standard-method-list-aip-132) or something reasonably similar), it is desirable to filter over the collection and only return results that the user is interested in.

It is tempting to define a structure to handle the precise filtering needs for each API. However, filtering requirements evolve frequently, and therefore it is prudent to use a string field with a structured syntax accessible to a non-technical audience. This allows updates to be able to be made transparently, without waiting for UI or client updates.

**Note:** Because list filters are intended for a potentially non-technical audience, they sometimes borrow from patterns of colloquial speech rather than common patterns found in code.

#### Guidance

APIs **may** provide filtering to users on `List` methods (or similar methods to query a collection, such as `Search`). If they choose to do so, they **should** follow the common specification for filters discussed here. The syntax is formally defined in the EBNF grammar.

When employing filtering, a request message **should** have exactly one filtering field, `string filter`. Filtering of related objects is handled through traversal or functions.

**Note:** List Filters have fuzzy matching characteristics with support for result ranking and scoring. For developers interested in deterministic evaluation of list filters, see CEL.

#### Literals

A bare literal value (examples: "42", "Hugo") is a value to be matched against. Literals appearing alone (with no specified field) **should** usually be matched anywhere it may appear in an object's field values.

However, a service **may** choose to only consider certain fields; if so, it **must** document which fields it considers. A service **may** include new fields over time, but **should** do so judiciously and consider impact on existing users.

**Note:** Literals separated by whitespace are considered to have a fuzzy variant of `AND`. Therefore, `Victor Hugo` is roughly equivalent to `Victor AND Hugo`.

#### Logical operators

Filtering implementations **should** provide the binary operators:

| Operator | Example | Meaning |
|----------|---------|---------|
| `AND` | `a AND b` | True if `a` and `b` are true. |
| `OR` | `a OR b OR c` | True if any of `a`, `b`, `c` are true. |

**Note:** To match common patterns of speech, the `OR` operator has higher precedence than `AND`, unlike what is found in most programming languages. The expression `a AND b OR c` evaluates: `a AND (b OR c)`. API documentation and examples **should** encourage the use of explicit parentheses to avoid confusion, but **should not** require explicit parentheses.

#### Negation operators

Filtering implementations **should** provide the unary operators `NOT` and `-`. These are used interchangeably, and a service that supports negation **must** support both formats.

| Operator | Example | Meaning |
|----------|---------|---------|
| `NOT` | `NOT a` | True if `a` is not true. |
| `-` | `-a` | True if `a` is not true. |

#### Comparison operators

Filtering implementations **should** provide the binary comparison operators `=`, `!=`, `<`, `>`, `<=`, and `>=` for string, numeric, timestamp, and duration fields (but **should not** provide them for booleans or enums).

| Operator | Example | Meaning |
|----------|---------|---------|
| `=` | `a = true` | True if `a` is true. |
| `!=` | `a != 42` | True unless `a` equals 42. |
| `<` | `a < 42` | True if `a` is a numeric value below 42. |
| `>` | `a > "foo"` | True if `a` is lexically ordered after "foo". |
| `<=` | `a <= "foo"` | True if `a` is "foo" or lexically before it. |
| `>=` | `a >= 42` | True if `a` is a numeric value of 42 or higher. |

**Note:** Unlike in most programming languages, field names **must** appear on the left-hand side of a comparison operator; the right-hand side only accepts literals and logical operators.

Because filters are accepted as query strings, type conversion takes place to translate the string to the appropriate strongly-typed value:

- Enums expect the enum's string representation (case-sensitive).
- Booleans expect `true` and `false` literal values.
- Numbers expect the standard integer or float representations. For floats, exponents are supported (e.g. `2.997e9`).
- Durations expect a numeric representation followed by an `s` suffix (for seconds). Examples: `20s`, `1.2s`.
- Timestamps expect an RFC-3339 formatted string (e.g. `2012-04-21T11:30:00-04:00`). UTC offsets are supported.

**Warning:** The identifiers `true`, `false`, and `null` only carry intrinsic meaning when used in the context of a typed field reference.

Additionally, when comparing strings for equality, services **should** support wildcards using the `*` character; for example, `a = "*.foo"` is true if `a` *ends with* ".foo".

#### Traversal operator

Filtering implementations **should** provide the `.` operator, which indicates traversal through a message, map, or struct.

| Example | Meaning |
|---------|---------|
| `a.b = true` | True if `a` has a boolean `b` field that is true. |
| `a.b > 42` | True if `a` has a numeric `b` field that is above 42. |
| `a.b.c = "foo"` | True if `a.b` has a string `c` field that is "foo". |

Traversal **must** be written using the field names from the resource. If a service wishes to support "implicit fields" of some kind, they **must** do so through well-documented functions. A service **may** specify a subset of fields that are supported for traversal.

If a user attempts to traverse to a field that is not defined on the message, the service **should** return an error with `INVALID_ARGUMENT`. A service **may** permit traversal to undefined keys on maps and structs, and **should** document how it behaves in this situation.

When evaluating an expression involving a traversal, if any non-primitive field in the chain is not set on the entry being evaluated, the entry **should** be skipped i.e. not match the filter expression. This applies even when the comparison is a `!=`, which would imply matching on empty values. In the examples above, if resource field `a` is not set on the resource instance, that instance is skipped as a non-match.

**Important:** The `.` operator **must not** be used to traverse through a repeated field or list, except for specific use with the `:` operator.

#### Has operator

Filtering implementations **must** provide the `:` operator, which means "has". It is usable with collections (repeated fields or maps) as well as messages, and behaves slightly differently in each case.

Repeated fields query to see if the repeated structure contains a matching element:

| Example | Meaning |
|---------|---------|
| `r:42` | True if `r` contains 42. |
| `r.foo:42` | True if `r` contains an element `e` such that `e.foo = 42`. |

**Important:** Filters can not query a *specific* element on a repeated field for a value. For example, `e.0.foo = 42` and `e[0].foo = 42` are **not** valid filters.

Maps, structs, messages can query either for the presence of a field in the map or a specific value:

| Example | Meaning |
|---------|---------|
| `m:foo` | True if `m` contains the key "foo". |
| `m.foo:*` | True if `m` contains the key "foo". |
| `m.foo:42` | True if `m.foo` is 42. |

There are two slight distinctions when parsing messages:

- When traversing messages, a field is only considered to be present if it has a non-default value.
- When traversing messages, field names are snake case, although implementations **may** choose to support automatic conversion between camel case and snake case.

For all aforementioned types, simply checking for the presence of a top-level resource field is possible with the `*` value:

| Example | Meaning |
|---------|---------|
| `r:*` | True if `repeated` field `r` is present. |
| `p:*` | True if `map` field `p` is present. |
| `m:*` | True if `message` field `m` is present. |

**Note:** For `map` and `repeated` fields, there is no semantic difference between an unset field and "set with empty value" — they both resolve to "not present".

#### Functions

The filtering language supports a function call syntax in order to support API-specific extensions. An API **may** define a function using the `call(arg...)` syntax, and **must** document any specific functions it supports.

#### Limitations

A service **may** specify further structure or limitations for filter queries, above what is defined here. For example, a service may support the logical operators but only permit a certain number of them (to avoid "queries of death" or other performance concerns).

Further structure or limitations **must** be clearly documented, and **must not** violate requirements set forth in this document.

#### Validation

If a non-compliant or schematically invalid `filter` string is specified, the API **should** error with `INVALID_ARGUMENT`. Wherever validation is relaxed for `filter`, the API **must** document the difference.

Schematic validation refers, but is not limited to, the following:

- Fields referenced in the `filter` **must** exist on the filtered schema.
- Field values provided in the `filter` **must** align to the type of the field.
  - For example, for a field `int32 age` a `filter` like `"age=hello"` is invalid.
- Field values for bounded data types e.g. `enum` provided in the `filter` **must** be a valid value in the set.
- Field values for standardized types e.g. `Timestamp` **must** conform to the documented standard (see Comparison Operators for a list of such types).

### 7.9 Field Masks (AIP-161)
[ref: #field-masks-aip-161]

Often, when updating resources (using an update method as defined in [AIP-134](05_operations.md#standard-method-update-aip-134) or something reasonably similar), it is desirable to specify exactly which fields are being updated, so that the service can ignore the rest, even if the user sends new values.

It is tempting to define a mask format to handle the precise needs for each API. However, masking requirements evolve, and therefore it is prudent to use a structured syntax. This allows updates to be able to be made transparently, without waiting for UI or client updates.

#### Guidance

These masks of field names are called "field masks". Fields representing a field mask **must** use the `google.protobuf.FieldMask` type. Field masks are most common on Update requests ([AIP-134](05_operations.md#standard-method-update-aip-134)).

Field masks **must** always be relative to the resource.

**Warning:** Read masks as a single field on the request message, for example: `google.protobuf.FieldMask read_mask` are **DEPRECATED**. Instead, see [AIP-157](07_design_patterns.md#partial-responses-aip-157).

```protobuf
message UpdateBookRequest {
  // The book to update.
  //
  // The book's `name` field is used to identify the book to update.
  // Format: publishers/{publisher}/books/{book}
  Book book = 1 [(google.api.field_behavior) = REQUIRED];

  // The list of fields to update.
  // Fields are specified relative to the book
  // (e.g. `title`, `rating`; *not* `book.title` or `book.rating`).
  google.protobuf.FieldMask update_mask = 2;
}
```

#### Read-write consistency

Read and write behavior for field masks **must** be self-consistent if a mask is present:

- If a user updates a resource with a given mask, and then reads the same resource with the same mask, the exact same data **must** be returned.
  - Exception: Output only fields.
- Similarly, reading a resource with a given mask and then updating the resource with the returned data and the same mask **must** be a no-op.

**Note:** This implies that any mask that is valid for either read or write **must** be valid for both.

#### Specifying specific fields

Field masks **must** permit the specification of specific fields in a defined struct, using the `.` character for traversal.

Because field masks are always relative to the resource, direct fields on the resource require no traversal (examples: `title`, `rating`). Traversal is used when resources contain messages (example: `author.given_name`).

**Note:** A user **must** be able to specify either a field as a whole, or one of its subfields: `author` and `author.given_name` are both valid.

#### Map fields

Field masks **may** permit the specification of specific fields in a map, if and only if the map's keys are either strings or integers, using the `.` character for traversal.

Field masks **should** support string keys that contain characters that are problematic for the field mask syntax, using the backtick character.

```protobuf
message Book {
  // The name of the book.
  // Format: publishers/{publisher}/books/{book}
  string name = 1;

  // Reviews for the back cover. The key is the author of the review,
  // and the value is the text of the review.
  //
  // Valid field masks: reviews, reviews.smith, reviews.`John Smith`
  map<string, string> reviews = 2;
}
```

#### Wildcards

Field masks **may** permit the use of the `*` character on a repeated field or map to indicate the specification of particular sub-fields in the collection:

```protobuf
message Book {
  option (google.api.resource) = {
    type: "library.googleapis.com/Book"
    pattern: "publishers/{publisher}/books/{book}"
  };

  // The name of the book.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  // The author or authors of the book.
  // Valid field masks: authors, authors.*.given_name, authors.*.family_name
  // Invalid field masks: authors.0, authors.0.given_name
  repeated Author authors = 2;
}

message Author {
  // The author's given name.
  string given_name = 1;

  // The author's family name.
  string family_name = 2;
}
```

**Note:** Field masks **must not** permit accessing a particular element of a repeated field by index, and **must** return an `INVALID_ARGUMENT` error if this is attempted.

#### Output only fields

If a user includes an output only field in an update mask indirectly (by using a wildcard or specifying an overall message that includes an output-only subfield), the service **must** ignore any output only fields provided as input, even if they are cleared or modified.

If a user directly specifies an output only field in an update mask, the service **must** ignore the output only fields provided as input, even if they are cleared or modified, to permit the same field mask to be used for input and output.

#### Invalid field mask entries

When reading data, field masks **may** ignore entries that point to a value that can not exist (either a field that does not exist, or a map key that the service considers invalid).

When writing data, field masks **should** return an `INVALID_ARGUMENT` error if an entry points to a value that can not exist; however, the service **may** permit deletions.

### 7.10 Resource Revisions (AIP-162)
[ref: #resource-revisions-aip-162]

Some APIs need to have resources with a revision history, where users can reason about the state of the resource over time. There are several reasons for this:

- Users may want to be able to roll back to a previous revision, or diff against a previous revision.
- An API may create data which is derived in some way from a resource at a given point in time. In these cases, it may be desirable to snapshot the resource for reference later.

**Note:** We use the word *revision* to refer to a historical reference for a particular resource, and intentionally avoid the term *version*, which refers to the version of an API as a whole.

#### Guidance

APIs **may** store a revision history for a resource. Examples of when it is useful include:

- When it is valuable to expose older versions of a resource via an API. This can avoid the overhead of the customers having to write their own API to store and enable retrieval of revisions.
- Other resources depend on different revisions of a resource.
- There is a need to represent the change of a resource over time.

APIs implementing resources with a revision history **should** abstract resource revisions as nested collection of the resource. Sometimes, the revisions collection can be a top level collection, exceptions include:

- If resource revisions are meant to have longer lifespan than the parent resource. In other words, resource revisions exist after resource deletion.

```protobuf
message BookRevision {
  // The name of the book revision.
  string name = 1;

  // The snapshot of the book.
  Book snapshot = 2
    [(google.api.field_behavior) = OUTPUT_ONLY];

  // The timestamp that the revision was created.
  google.protobuf.Timestamp create_time = 3
    [(google.api.field_behavior) = OUTPUT_ONLY];

  // Other revision IDs that share the same snapshot.
  repeated string alternate_ids = 4
    [(google.api.field_behavior) = OUTPUT_ONLY];
}
```

- The `message` **must** be annotated as a resource ([AIP-123](04_resource_design.md#resource-types-aip-123)).
- The `message` name **must** be named `{ResourceType}Revision`.
- The resource revision **must** contain a field with a message type of the parent resource, with a field name of `snapshot`.
  - The value of `snapshot` **must** be the configuration of the parent at the point in time the revision was created.
- The resource revision **must** contain a `create_time` field (see [AIP-142](06_fields.md#time-and-duration-aip-142)).
- The resource revision **may** contain a repeated field `alternate_ids`, which would contain a list of resource IDs that the revision is also known by (e.g. `latest`).

#### Creating revisions

Depending on the resource, different APIs may have different strategies for creating revisions:

- Create a new revision any time that there is a change to the parent resource.
- Create a new revision when important system state changes.
- Create a new revision when specifically requested.

APIs **may** use any of these strategies. APIs **must** document their revision creation strategy.

#### Resource names for revisions

When referring to specific revision of a resource, the subcollection name **must** be named `revisions`. Resource revisions have names with the format `{resource_name}/revisions/{revision_id}`. For example:

```
publishers/123/books/les-miserables/revisions/c7cfa2a8
```

#### Server-specified aliases

Services **may** reserve specific IDs to be aliases (e.g. `latest`). These are read-only and managed by the service.

```
GET /v1/publishers/{publisher}/books/{book}/revisions/{revision_id}
```

- If a `latest` ID exists, it **must** represent the most recently created revision. The content of `publishers/{publisher}/books/{book}/revisions/latest` and `publishers/{publisher}/books/{book}` can differ, as the latest revision may be different from the current state of the resource.

#### User-specified aliases

APIs **may** provide a mechanism for users to assign an alias ID to an existing revision with a custom method `alias`:

```protobuf
rpc AliasBookRevision(AliasBookRevisionRequest) returns (Book) {
  option (google.api.http) = {
    post: "/v1/{name=publishers/*/books/*/revisions/*}:alias"
    body: "*"
  };
}
```

```protobuf
message AliasBookRevisionRequest {
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/BookRevision"
    }];

  // The ID of the revision to alias to, e.g. `CURRENT` or a semantic
  // version.
  string alias_id = 2 [(google.api.field_behavior) = REQUIRED];
}
```

- The request message **must** have a `name` field:
  - The field **must** be annotated as required.
  - The field **must** identify the resource type that it references.
- The request message **must** have an `alias_id` field:
  - The field **must** be annotated as required.
- If the user calls the method with an existing `alias_id`, the request **must** succeed and the alias will be updated to refer to the provided revision. This allows users to write code against a specific alias (e.g. `published`) and the revision can change with no code change.

#### Rollback

A common use case for a resource with a revision history is the ability to roll back to a given revision. APIs **should** handle this with a `Rollback` custom method:

```protobuf
rpc RollbackBook(RollbackBookRequest) returns (BookRevision) {
  option (google.api.http) = {
    post: "/v1/{name=publishers/*/books/*/revisions/*}:rollback"
    body: "*"
  };
}
```

- The method **must** use the `POST` HTTP verb.
- The method **should** return a resource revision.

```protobuf
message RollbackBookRequest {
  // The revision that the book should be rolled back to.
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/BookRevision"
    }];
}
```

- The request message **must** have a `name` field, referring to the resource revision whose configuration the resource should be rolled back to.
  - The field **must** be annotated as required.
  - The field **must** identify the resource type that it references.

#### Child resources

Resources with a revision history **may** have child resources. If they do, there are two potential variants:

- Child resources where each child resource is a child of the parent resource as a whole.
- Child resources where each child resource is a child of *a single revision* *of* the parent resource.

APIs **should not** include multiple levels of resources with revisions, as this quickly becomes difficult to reason about.

#### Standard methods

Any standard methods **must** implement the corresponding AIPs ([AIP-131](05_operations.md#standard-method-get-aip-131), [AIP-132](05_operations.md#standard-method-list-aip-132), [AIP-133](05_operations.md#standard-method-create-aip-133), [AIP-134](05_operations.md#standard-method-update-aip-134), [AIP-135](05_operations.md#standard-method-delete-aip-135)), with the following additional behaviors:

- List methods: By default, revisions in the list response **must** be ordered in reverse chronological order. User can supply `order_by` to override the default behavior.
- If the revision supports aliasing, a delete method with the resource name of the alias (e.g. `revisions/1.0.2`) **must** remove the alias instead of deleting the resource.

As revisions are nested under the resource, also see cascading delete.

#### Rationale

##### Abstract revisions as nested collection

Revisions being resources under nested collection make revisions a first class citizen.

- Revisions can offer standard get, list, and delete methods.
- It retains the flexibility of extending new fields to revision in addition to the resource message.

##### Tagging to aliases

Previously, a concept of `tag` existed. This concept was redundant with that of an alias, and the terms were consolidated to reduce complexity in the AIPs.

##### Output only resource configuration

Although it was an option to have the revision take in the resource configuration as part of the create method, doing so would have allowed users to submit resource configuration for a revision that the resource was never in.

`OUTPUT_ONLY` and requiring that a created revision represents the resource at current point in time eliminates that issue.

#### History

##### Switching from a collection extension to a subcollection

In 2023-09, revisions are abstracted as a nested resource collection. Prior to this, revisions are more like extension of an existing resource by using `@` symbol. List and delete revisions were custom methods on the resource collection. A single Get method was used to retrieve either the resource revision, or the resource.

Its primary advantage was allowing a resource reference to seamlessly refer to a resource, or its revision.

It also had several disadvantages:

- List revisions is a custom method (`:listRevisions`) on the resource collection.
- Delete revision is a custom method on the resource collection.
- Not visible in API discovery doc.
- Resource ID cannot use `@`.

The guidance was modified ultimately to enable revisions to behave like a resource, which reduces the users cognitive load and allows resource-oriented clients to easily list, get, create, and update revisions.

##### Using resource ID instead of tag

In the previous design, revisions had a separate identifer for a revision known as a `tag`, that would live in a revision.

Tags were effectively a shadow resource ID, requiring methods to create, get and filter revisions based on the value of the tag.

By consolidating the concept of a tag into the revision ID, the user no longer needs to be familiar with a second set of retrieval and identifier methods.

### 7.11 Change Validation (AIP-163)
[ref: #change-validation-aip-163]

Occasionally, a user wants to validate an intended change to see what the result will be before actually making the change. For example, a request to provision new servers in a fleet will have an impact on the overall fleet size and cost, and could potentially have unexpected downstream effects.

#### Guidance

APIs **may** provide an option to validate, but not actually execute, a request, and provide the same response (status code, headers, and response body) that it would have provided if the request was actually executed.

To provide this option, the method **should** include a `bool validate_only` field in the request message:

```protobuf
message ReviewBookRequest {
  string name = 1 [(google.api.resource_reference) = {
    type: "library.googleapis.com/Book"
  }];
  int32 rating = 2;
  string comment = 3;

  // If set, validate the request and preview the review, but do not actually
  // post it.
  bool validate_only = 4;
}
```

The API **must** perform permission checks and any other validation that would be performed on a "live" request; a request using `validate_only` **must** fail if it determines that the actual request would fail.

**Note:** It may occasionally be infeasible to provide the full output. For example, if creating a resource would create an auto-generated ID, it does not make sense to do this on validation. APIs **should** omit such fields on validation requests in this situation.

#### Declarative-friendly resources

A resource that is declarative-friendly ([AIP-128](04_resource_design.md#declarative-friendly-interfaces-aip-128)) **must** include a `validate_only` field on methods that mutate the resource.

### 7.12 Soft Delete (AIP-164)
[ref: #soft-delete-aip-164]

There are several reasons why a client could desire soft delete and undelete functionality, but one over-arching reason stands out: recovery from mistakes. A service that supports undelete makes it possible for users to recover resources that were deleted by accident.

#### Guidance

APIs **may** support the ability to "undelete", to allow for situations where users mistakenly delete resources and need the ability to recover.

If a resource needs to support undelete, the `Delete` method **must** simply mark the resource as having been deleted, but not completely remove it from the system. If the method behaves this way, it **should** return the updated resource instead of `google.protobuf.Empty`.

Resources that support soft delete **should** have both a `delete_time` and `purge_time` field as described in [AIP-148](06_fields.md#standard-fields-aip-148). Additionally, resources **should** include a `DELETED` state value if the resource includes a `state` field ([AIP-216](06_fields.md#states-aip-216)).

#### Undelete

A resource that supports soft delete **should** provide an `Undelete` method:

```protobuf
rpc UndeleteBook(UndeleteBookRequest) returns (Book) {
  option (google.api.http) = {
    post: "/v1/{name=publishers/*/books/*}:undelete"
    body: "*"
  };
}
```

- The HTTP verb **must** be `POST`.
- The `body` clause **must** be `"*"`.
- The response message **must** be the resource itself. There is no `UndeleteBookResponse`.
  - The response **should** include the fully-populated resource unless it is infeasible to do so.
  - If the undelete RPC is long-running, the response message **must** be a `google.longrunning.Operation` which resolves to the resource itself.

#### Undelete request message

Undelete methods implement a common request message pattern:

```protobuf
message UndeleteBookRequest {
  // The name of the deleted book.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference).type = "library.googleapis.com/Book"];
}
```

- A `name` field **must** be included. It **should** be called `name`.
  - The field **should** be annotated as required.
  - The field **should** identify the resource type that it references.
  - The comment for the field **should** document the resource pattern.
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.

#### Long-running undelete

Some resources take longer to undelete a resource than is reasonable for a regular API request. In this situation, the API **should** use a long-running operation ([AIP-151](05_operations.md#long-running-operations-aip-151)) instead:

```protobuf
rpc UndeleteBook(UndeleteBookRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{name=publishers/*/books/*}:undelete"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "Book"
    metadata_type: "OperationMetadata"
  };
}
```

- The response type **must** be set to the resource (what the return type would be if the RPC was not long-running).
- Both the `response_type` and `metadata_type` fields **must** be specified.

#### Expunge

Resources that support soft delete **may** provide an `Expunge` custom method to allow users to trigger immediate permanent deletion of a resource. This method can operate on resources that are currently in a `CREATING`, `READY` or `SOFT_DELETED` state (e.g., `delete_time` is set).

```protobuf
// Permanently deletes a soft-deleted Book.
rpc ExpungeBook(ExpungeBookRequest) returns (google.protobuf.Empty) {
  option (google.api.http) = {
    post: "/v1/{name=publishers/*/books/*}:expunge"
    body: "*"
  };
  option (google.api.method_signature) = "name";
}
```

- The URI must use a custom method with the `:expunge` suffix.
- The HTTP verb must be `POST` and the body clause must be `"*"`.
- The response message must be `google.protobuf.Empty` or a `google.longrunning.Operation`.

#### Long-running expunge

If the expunge process takes significant time, the method **may** be a `google.longrunning.Operation` ([AIP-151](05_operations.md#long-running-operations-aip-151)) instead:

```protobuf
// Permanently deletes a soft-deleted Book.
rpc ExpungeBook(ExpungeBookRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{name=publishers/*/books/*}:expunge"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "google.protobuf.Empty"
    metadata_type: "OperationMetadata"
  };
  option (google.api.method_signature) = "name";
}
```

#### Expunge request message

Expunge methods implement a common request message pattern:

```protobuf
message ExpungeBookRequest {
  // The name of the soft-deleted book to expunge.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference).type = "library.googleapis.com/Book"
  ];
}
```

- The request message **must** refer to the resource to be expunged by name.
- There **should not** be any other request fields.

#### List and Get

Soft-deleted resources **should not** be returned in `List` ([AIP-132](05_operations.md#standard-method-list-aip-132)) responses by default (unless `bool show_deleted` is true). `Get` ([AIP-131](05_operations.md#standard-method-get-aip-131)) requests for soft-deleted resources **should** return the resource (rather than a `NOT_FOUND` error).

APIs that soft delete resources **may** choose a reasonable strategy for purging those resources, including automatic purging after a reasonable time (such as 30 days), allowing users to set an expiry time ([AIP-214](07_design_patterns.md#resource-expiration-aip-214)), or retaining the resources indefinitely. Regardless of what strategy is selected, the API **should** document when soft deleted resources will be completely removed.

#### Declarative-friendly resources

Soft-deletable resources have a poorer experience than hard-deleted resources in declarative clients: since an ID on a soft-deleted resource is not re-usable unless a custom method (undelete) is called, an imperative client must be introduced or hand-written code is required to incorporate the usage of the custom method.

#### Errors

If the user does not have permission to access the resource, regardless of whether or not it exists, the service **must** error with `PERMISSION_DENIED` (HTTP 403). Permission **must** be checked prior to checking if the resource exists.

If the user does have proper permission, but the requested resource does not exist (either it was never created or already expunged), the service **must** error with `NOT_FOUND` (HTTP 404).

If the user calling a soft `Delete` has proper permission, but the requested resource is already deleted, the service **must** succeed if `allow_missing` is `true`, and **should** error with `NOT_FOUND` (HTTP 404) if `allow_missing` is `false`.

If the user calling `Undelete` has proper permission, but the requested resource is not deleted, the service **must** respond with `ALREADY_EXISTS` (HTTP 409).

If the user calling `Expunge` requests a resource that does not exist (was never created or already expunged), the method **must** return `NOT_FOUND` (HTTP 404).

If the resource exists but is not in a ready or soft-deleted state, the method **must** return `FAILED_PRECONDITION` (HTTP 400).

Standard permission errors (`PERMISSION_DENIED`) apply. Services **must** require an explicit expunge permission that is separate from standard delete permissions (e.g., `<service>.<resource>.expunge`).

### 7.13 Criteria-Based Delete (AIP-165)
[ref: #criteria-based-delete-aip-165]

Occasionally, an API may need to provide a mechanism to delete a large number of resources based on some set of filter parameters, rather than requiring the individual resource name of the resources to be deleted.

This is a rare case, reserved for situations where users need to delete thousands or more resources at once, in which case the normal Batch Delete pattern ([AIP-235](05_operations.md#batch-method-delete-aip-235)) becomes unwieldy and inconvenient.

#### Guidance

**Important:** Most APIs **should** use only Delete ([AIP-135](05_operations.md#standard-method-delete-aip-135)) or Batch Delete ([AIP-235](05_operations.md#batch-method-delete-aip-235)) for deleting resources, and **should not** implement deleting based on criteria. This is because deleting is generally irreversible and this type of operation makes it easy for a user to accidentally lose significant amounts of data.

An API **may** implement a Purge method to permit deleting a large number of resources based on a filter string; however, this **should** only be done if the Batch Delete pattern is insufficient to accomplish the desired goal:

```protobuf
rpc PurgeBooks(PurgeBooksRequest) returns (google.longrunning.Operation) {
  option (google.api.http) = {
    post: "/v1/{parent=publishers/*}/books:purge"
    body: "*"
  };
  option (google.longrunning.operation_info) = {
    response_type: "PurgeBooksResponse"
    metadata_type: "PurgeBooksMetadata"
  };
}
```

- The RPC's name **must** begin with the word `Purge`. The remainder of the RPC name **should** be the plural form of the resource being purged.
- The request message **must** match the RPC name, with a `Request` suffix.
- The response type **must** be a `google.longrunning.Operation` (see [AIP-151](05_operations.md#long-running-operations-aip-151)) that resolves to a message whose name matches the RPC name, with a `Response` suffix.
- The HTTP verb **must** be `POST`, and the `body` **must** be `"*"`.
- The URI path **should** represent the collection for the resource.
- The `parent` field **should** be included in the URI. If the API wishes to support deletion across multiple parents, it **should** accept the `-` character consistent with [AIP-159](07_design_patterns.md#reading-across-collections-aip-159).

#### Request message

Purge methods implement a common request message pattern:

```protobuf
message PurgeBooksRequest {
  // The publisher to purge books from.
  // To purge books across publishers, send "publishers/-".
  string parent = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      child_type: "library.googleapis.com/Book"
    }];

  // A filter matching the books to be purged.
  string filter = 2 [(google.api.field_behavior) = REQUIRED];

  // Actually perform the purge.
  // If `force` is set to false, the method will return a sample of
  // resource names that would be deleted.
  bool force = 3;
}
```

- A singular `string parent` field **should** be included, unless the resource is top-level.
  - The field **should** be annotated as required.
  - The field **should** identify the resource type that it references.
- A singular `string filter` field **must** be included and **must** follow the same semantics as in List methods ([AIP-160](07_design_patterns.md#filtering-aip-160)).
  - It **should** be annotated as required.
  - A wildcard value of `"*"` **may** be supported for deleting everything.
- A singular `bool force` field **must** be included. If it is not set, the API **must** return a count of the resources that would be deleted as well as a sample of those resources, without actually performing the deletion.

#### Response message

Purge methods implement a common response message pattern:

```protobuf
message PurgeBooksResponse {
  // The number of books that this request deleted (or, if `force` is false,
  // the number of books that will be deleted).
  int32 purge_count = 1;

  // A sample of the resource names of books that will be deleted.
  // Only populated if `force` is set to false.
  repeated string purge_sample = 2 [(google.api.resource_reference) = {
    type: "library.googleapis.com/Book"
  }];
}
```

- A singular `int32 purge_count` field **should** be included, and provide the number of resources that were deleted (or would be deleted). This count **may** be an estimate similar to `total_size` in [AIP-158](07_design_patterns.md#pagination-aip-158) (but the service **should** document this if so).
- A `repeated string purge_sample` field **should** be included: If `force` is `false`, it **should** provide a sample of resource names that will be deleted. If `force` is true, this field **should not** be populated.
  - The sample **should** be a sufficient size to catch clearly obvious mistakes: A good rule of thumb is 100. The API **should** document the size, and **should** document that it is a maximum (it is possible to send fewer).
  - The sample **may** be random or **may** be deterministic (such as the first matched resource names). The API **should** document which approach is used.
  - The field **should** identify the resource type that it references.

**Note:** Even if `purge_count` and `purge_sample` are not included, the `force` field **must** still be included in the request.

### 7.14 Unicode (AIP-210)
[ref: #unicode-aip-210]

APIs should be consistent on how they explain, limit, and bill for string values and their encodings. This ranges from little ambiguities (like fields "limited to 1024 characters") all the way to billing confusion (are names and values of properties billed based on characters or bytes?).

In general, if we talk about limits measured in bytes, we are discriminating against non-ASCII text since it takes up more space. On the other hand, if we talk about "characters", we are ambiguous about whether those are Unicode "code points", "code units" for a particular encoding (e.g. UTF-8 or UTF-16), "graphemes", or "grapheme clusters".

#### Unicode primer

Character encoding tends to be an area we often gloss over, so a quick primer:

- Strings are just bytes that represent numbers according to some encoding format.
- When we talk about **characters**, we sometimes mean Unicode **code points**, which are numbers in the Unicode spec (up to 21 bits).
- Other times we might mean **graphemes** or **grapheme clusters**, which may have multiple numeric representations and may be represented by more than one code point. For example, `á` may be represented as a composition of `U+0061 + U+0301` (the `a` + the accent combining mark) or as a single code point, `U+00E1`.
- Protocol buffers uses **UTF-8** ("Unicode Transformation Format") which is a variable-length encoding scheme using up to 4 **code units** (8-bit bytes) per code point.

#### Guidance

##### Character definition

**TL;DR:** In our APIs, "characters" means "Unicode code points".

In API documentation (e.g., API reference documents, blog posts, marketing documentation, billing explanations, etc), "character" **must** be defined as a Unicode code point.

##### Length units

**TL;DR:** Set size limits in "characters" (as defined above).

All string field length limits defined in API comments **must** be measured and enforced in characters as defined above. This means that there is an underlying maximum limit of (`4 * characters`) bytes, though this limit will only be hit when using exclusively characters that consist of 4 UTF-8 code units (32 bits).

If you use a database system which allows you to define a limit in characters, it is safe to assume that this byte-defined requirement is handled by the underlying storage system.

##### Billing units

APIs **may** use either code points or bytes (using the UTF-8 encoding) as the unit for billing or quota measurement. If an API does not define this, the assumption is that the unit of billing is characters (e.g., $0.01 *per character*, not $0.01 *per byte*).

##### Unique identifiers

**TL;DR:** Unique identifiers **should** limit to ASCII, generally only letters, numbers, hyphens, and underscores, and **should not** start with a number.

Strings used as unique identifiers **should** limit inputs to ASCII characters, typically letters, numbers, hyphens, and underscores (`[a-zA-Z][a-zA-Z0-9_-]*`). This ensures that there are never accidental collisions due to normalization. If an API decides to allow all valid Unicode characters in unique identifiers, the API **must** reject any inputs that are not in Normalization Form C. Generally, unique identifiers **should not** start with a number as that prefix is reserved for generated identifiers and gives an easy way to check whether a unique numeric ID was generated or whether the ID was chosen by a user.

Unique identifiers **should** use a maximum length of 64 characters, though this limit may be expanded as necessary. 64 characters should be sufficient for most purposes as even UUIDs only require 36 characters.

**Note:** See [AIP-122](04_resource_design.md#resource-names-aip-122) for recommendations about resource ID segments.

##### Normalization

**TL;DR:** Unicode values **should** be stored in Normalization Form C.

Values **should** always be normalized into Normalization Form C. Unique identifiers **must** always be stored in Normalization Form C (see the next section).

Imagine we're dealing with Spanish input "estar **é**" (the accented part will be bolded throughout). This text has what we might visualize as 6 "characters" (in this case, they are grapheme clusters). It has two possible Unicode representations:

- Using 6 code points: `U+0065` `U+0073` `U+0074` `U+0061` `U+0072` **`U+00E9`**
- Using 7 code points: `U+0065` `U+0073` `U+0074` `U+0061` `U+0072` **`U+0065` `U+0301`**

Further, when encoding to UTF-8, these code points have two different serialized representations:

- Using 7 code-units (7 bytes): `0x65` `0x73` `0x74` `0x61` `0x72` **`0xC3` `0xA9`**
- Using 8 code-units (8 bytes): `0x65` `0x73` `0x74` `0x61` `0x72` **`0x65` `0xCC` `0x81`**

To avoid this discrepancy in size (both code units and code points), use Normalization Form C which provides a canonical representation for strings.

##### Uniqueness

**TL;DR:** Unicode values **must** be normalized to Normalization Form C before checking uniqueness.

For the purposes of unique identification (e.g., `name`, `id`, or `parent`), the value **must** be normalized into Normalization Form C (which happens to be the most compact). Otherwise we may have what is essentially "the same string" used to identify two entirely different resources.

In our example above, there are two ways of representing what is essentially the same text. This raises the question about whether the two representations should be treated as equivalent or not. In other words, if someone were to use both of those byte sequences in a string field that acts as a unique identifier, would it violate a uniqueness constraint?

The W3C recommends using Normalization Form C for all content moving across the internet. It is the most compact normalized form on Unicode text, and avoids most interoperability problems. If we were to treat two Unicode byte sequences as different when they have the same representation in NFC, we'd be required to reply to possible "Get" requests with content that is **not** in normalized form. Since that is definitely unacceptable, we **must** treat the two as identical by transforming any incoming string data into Normalized Form C or rejecting identifiers not in the normalized form.

There is some debate about whether we should view strings as sequences of code points represented as bytes (leading to uniqueness determined based on the byte-representation of said string) or to interpret strings as a higher level abstraction having many different possible byte-representations. The stance taken here is that we already have a field type for handling that: `bytes`. Fields of type `string` already express an opinion of the validity of an input (it must be valid UTF-8). As a result, treating two inputs that have identical normalized forms as different due to their underlying byte representation seems to go against the original intent of the `string` type. This distinction typically doesn't matter for strings that are opaque to our services (e.g., `description` or `display_name`), however when we rely on strings to uniquely identify resources, we are forced to take a stance.

Put differently, our goal is to allow someone with text in any encoding (ASCII, UTF-16, UTF-32, etc) to interact with our APIs without a lot of "gotchas".

### 7.15 Authorization Checks (AIP-211)
[ref: #authorization-checks-aip-211]

The majority of operations, whether reads or writes, require authorization: permission to do the thing the user is asking to do. Additionally, it is important to be careful how much information is provided to *unauthorized* users, since leaking information can be a security concern.

#### Guidance

Services **must** check authorization before validating any request, to ensure both a secure API surface and a consistent user experience. An operation **may** require multiple permissions or preconditions in order to grant authorization.

If a request can not pass the authorization check for any reason, the service **must** error with `PERMISSION_DENIED`, and the corresponding error message **should** look like: "Permission '`{p}`' denied on resource '`{r}`' (or it might not exist)." This avoids leaking resource existence.

If it is not possible to determine authorization for a resource because the resource does not exist, the service **should** check authorization to read children on the parent resource, and return `NOT_FOUND` if the authorization check passes.

#### Multiple operations

A service could encounter a situation where it has two different operations with two different permissions, either of which would reveal the existence of a resource if called, but a user only has permission to call one of them.

In this situation, the service **should** still only check for authorization applicable to the operation being called, and **should not** try to "help out" by checking for related authorization that would provide permission to reveal existence, because such algorithms are complicated to implement correctly and prone to accidental leaks.

For example, posit a scenario where:

- A resource exists within a given collection that a user is unable to read.
- The user *does* have the ability to create other resources, and the collection uses user-specified IDs (meaning that a failure because of a duplicate ID would reveal existence).

In this situation, the get or create methods **should** still only check *their* permissions when determining what error to return, and not one another's.

#### Rationale

RFC 7231 §6.5.3 states that services are permitted to use `404 Not Found` in lieu of `403 Forbidden` in situations where the service does not want to divulge existence, whereas this AIP argues for the use of `PERMISSION_DENIED` (which corresponds to `403 Forbidden` in HTTP) instead. We take this position for the following reasons:

- The practice of "getting `404 Not Found` until you have enough permission to get `403 Forbidden`" is counter-intuitive and increases the difficulty of troubleshooting.
  - A service *could* ameliorate this by sending information about missing permissions while still using the `404 Not Found` status code, but this constitutes a mixed message.
- While `403 Forbidden` is essentially always an error requiring manual action, `404 Not Found` is often a valid response that the application can handle (e.g. "get or create"); overloading it for permission errors deprives applications of this benefit.
- RFC 7231 §6.5.4 states that `404 Not Found` results are cacheable, but permission errors are not generally cacheable. Sending explicit cache controls on a conditional basis could ameliorate this, but would defeat the purpose.
- The guidance here is more consistent with most other real-world authorization systems.

### 7.16 Resource Expiration (AIP-214)
[ref: #resource-expiration-aip-214]

Customers often want to provide the time that a given resource or resource attribute is no longer useful or valid (e.g. a rotating security key). Currently we recommend that customers do this by specifying an exact "expiration time" into a `google.protobuf.Timestamp expire_time` field; however, this adds additional strain on the user when they want to specify a relative time offset until expiration rather than a specific time until expiration.

Furthermore, the world understands the concept of a "time-to-live", often abbreviated to TTL, but the typical format of this field (an integer, measured in seconds) results in a sub-par experience when using an auto-generated client library.

#### Guidance

1. APIs wishing to convey an expiration **must** rely on a `google.protobuf.Timestamp` field called `expire_time`.
2. APIs wishing to allow a relative expiration time **must** define a `oneof` called `expiration` (or `{something}_expiration`) containing both the `expire_time` field and a separate `google.protobuf.Duration` field called `ttl`, the latter marked as input only.
3. APIs **must** always return the expiration time in the `expire_time` field and leave the `ttl` field blank when retrieving the resource.
4. APIs that rely on the specific semantics of a "time to live" (e.g., DNS which must represent the TTL as an integer) **may** use an `int64 ttl` field (and **should** provide an `aip.dev/not-precedent` comment in this case).

#### Example

```protobuf
message ExpiringResource {
  // google.api.resource and other annotations and fields

  oneof expiration {
    // Timestamp in UTC of when this resource is considered expired.
    // This is *always* provided on output, regardless of what was sent
    // on input.
    google.protobuf.Timestamp expire_time = 2;

    // Input only. The TTL for this resource.
    google.protobuf.Duration ttl = 3 [(google.api.field_behavior) = INPUT_ONLY];
  }
}
```

#### Rationale

##### Alternatives considered

###### A new standard field called `ttl`

We considered allowing a standard field called `ttl` as an alternative way of defining the expiration, however doing so would require that API services continually update the field, like a clock counting down. This could potentially cause problems with the read-modify-write lifecycle where a resource is being processed for some time, and effectively has its life extended as a result of that processing time.

###### Always use `expire_time`

This is the current state of the world with a few exceptions. In this scenario, we could potentially push the computation of `now + ttl = expire_time` into client libraries; however, this leads to a somewhat frustrating experience in the command-line and using REST/JSON. Leaving things as they are is typically the default, but it seems many customers want the ability to define relative expiration times as it is quite a bit easier and removes questions of time zones, stale clocks, and other silly mistakes.

### 7.17 Unreachable Resources (AIP-217)
[ref: #unreachable-resources-aip-217]

Occasionally, a user may ask for a list of resources, and some set of resources in the list are temporarily unavailable. The most typical use case is while supporting Reading Across Collections. For example, a user may ask to list resources across multiple parent locations, but one of those locations is temporarily unreachable. In this situation, it is still desirable to provide the user with all the available resources, while indicating that something is missing.

#### Guidance

If a method to retrieve data is capable of partially failing due to one or more resources being temporarily unreachable, the response message **must** include a field to indicate this:

```protobuf
message ListBooksResponse {
  // The books matching the request.
  repeated Book books = 1;

  // The next page token, if there are more books matching the
  // request.
  string next_page_token = 2;

  // Unreachable resources.
  repeated string unreachable = 3 [
    (google.api.field_behavior) = UNORDERED_LIST
  ];
}
```

- The field **must** be a repeated string, and **should** be named `unreachable`.
- The field **must** contain the resource names of the resources that are unreachable or those that impede reaching the requested collection, such as the parent resource of the collection that could not be reached.
  - For example, if an entire location is unreachable, preventing access to the localized collection of resources requested, the location resource is included.
- The field **must** contain *service-relative* resource names, and **must not** contain full resource names, resource URIs, or simple resource IDs. See [AIP-122](04_resource_design.md#resource-names-aip-122) for definitions.
  - For example, if a `Book` resource is unreachable, the *service-relative* resource name `"shelves/scifi1/books/starwars4"` is included in `unreachable`, as opposed to the *full* resource name `"//library.googleapis.com/shelves/scifi1/books/starwars4"`, the *parent-relative* resource `"books/starwars4"`, the resource ID `"starwars4"`, or the resource URI.
- The response **must not** provide any other information about the issue(s) that made the listed resources unreachable.
  - For example, the response cannot contain an extra field with error reasons for each `unreachable` entry.
- The service **must** provide a way for the user to make a more specific request and receive an error with additional information e.g. via a Standard Get or a Standard List targeted at the unreachable collection parent.
  - The service **must** also allow the user to repeat the original call with more restrictive parameters.
- The resource names that appear in `unreachable` **may** be heterogeneous.
  - The `unreachable` field definition **should** document what potential resources could be provided in this field, and note that it might expand later.
  - For example, if both an entire location and a specific resource in a different location are unreachable, the unreachable location's name e.g. `"projects/example123/locations/us-east1"` and the unreachable resource's name e.g. `"projects/example123/locations/europe-west2/instances/example456"` will both appear in `unreachable`.
- The `unreachable` field **must not** have semantically meaningful ordering or structure within the list. Put differently, `unreachable` **must** be an unordered list.
  - As such, the `unreachable` field **must** be annotated with `UNORDERED_LIST` field behavior (see [AIP-203](06_fields.md#field-behavior-documentation-aip-203)).

**Important:** If a single unreachable location or resource prevents returning any data by definition (for example, a list request for a single publisher where that publisher is unreachable), the service **must** fail the entire request with an error.

While preparing a page of results to fulfill a page fetch RPC e.g. an [AIP-132](05_operations.md#standard-method-list-aip-132) Standard List call, if the service encounters any unreachable resources or collections they **must** do the following:

- Include the resource name for the unreachable resource in the `unreachable` response field.
  - The resource name **must** be the most appropriately scoped for the unreachable resource or collection.
    - For example, if a specific zone within a region is unreachable, the unreachable resource name would be a zonal Location e.g. `projects/example/locations/us-west1-a`, but if an entire region is unreachable, the resource name would be a regional Location e.g. `projects/example/locations/us-west1`.
  - The resource name **must** be included, regardless of restrictive paging parameters e.g. `order_by`, when it is identified as unreachable.
- Populate results that were previously considered unreachable on a following page if their availability is restored and the paging parameters allow for their inclusion.
  - Determining inclusion eligibility based on paging parameters also includes any documented default ordering behavior in the absence of user-specified ordering in the request.
  - For example, if region `projects/example/locations/us-west1` was unavailable in the first page of an ordered paging call, and including its resources would violate the ordering, those out-of-order resources are not included in the following page.
  - Similarly, if the same exact request is made, and resources previously considered unreachable are available again, they **must** be populated, within the constraints of the paging parameters.
- Limit the number of unreachable resource names returned in a given response if, even after up-scoping the unreachable resource name, the number of unreachable resource names exceeds a documented maximum.
  - This maximum **must** be documented in the `unreachable` field comments directly.
  - This is independent of the `page_size` set by the caller.

#### Retaining previous behavior

Services **may** continue with previously implemented `unreachable` pagination behavior where changing it would induce an incompatible change as per [AIP-180](08_compatibility_and_versioning.md#backwards-compatibility-aip-180), but **must** document said behavior on the `unreachable` field(s) directly.

#### Adopting partial success

In order for an existing API that has a default behavior *differing* from the aforementioned guidance i.e. the API call returns an error status instead of a partial result, to adopt the `unreachable` pattern the API **must** do the following:

- The default behavior **must** be retained to avoid incompatible behavioral changes.
  - For example, if the default behavior is to return an error if any location is unreachable, that default behavior **must** be retained.
- The request message **must** have a `bool return_partial_success` field.
- The response message **must** have the standard `repeated string unreachable` field.
- The two aforementioned fields **must** be added simultaneously.

When the `bool return_partial_success` field is set to `true` in a request, the API **must** behave as described in the aforementioned guidance with regards to populating the `repeated string unreachable` response field.

```protobuf
message ListBooksRequest {
  // Standard List request fields...

  // Setting this field to `true` will opt the request into returning the
  // resources that are reachable, and into including the names of those that
  // were unreachable in the [ListBooksResponse.unreachable] field. This can
  // only be `true` when reading across collections e.g. when `parent` is set to
  //  `"projects/example/locations/-"`.
  bool return_partial_success = 4;
}

message ListBooksResponse {
  // Standard List Response fields...

  // Unreachable resources. Populated when the request opts into
  // `return_partial_success` and reading across collections e.g. when
  // attempting to list all resources across all supported locations.
  repeated string unreachable = 3 [
    (google.api.field_behavior) = UNORDERED_LIST
  ];
}
```

#### Partial success granularity

If the `bool return_partial_success` field is set to `true` in a request that is scoped beyond the supported granularity of the API's ability to reasonably report unreachable resources, the API **should** return an `INVALID_ARGUMENT` error with details explaining the issue. For example, if the API only supports `return_partial_success` when Reading Across Collections, it returns an `INVALID_ARGUMENT` error when given a request scoped to a specific parent resource collection. The supported granularity **must** be documented on the `return_partial_success` field.

#### Rationale

##### Using service-relative resource names

In general, relative resource names, as defined in [AIP-122](04_resource_design.md#resource-names-aip-122), are the best practice for referring to resources by name *within* a service and in other services when that other service is obvious. The full resource name format is strictly less consumable (e.g., requires extra parsing client side), and over-specified for the uses of `unreachable`. Resource URIs are not transport agnostic, as they are unusable in standard methods for gRPC users, and simple resource IDs do not provide enough information about exactly which resource was unreachable in a heterogenous list of resources.

The context in which an unreachable resource is discovered may be sensitive and the state of the system fluid between calls. As such, it is preferred to defer to the service by making a more specific RPC to get more details about a specific resource or parent. This allows the parent to handle all necessary RPC checks and system state resolution on at time of request, rather than by shoehorning potentially privileged or stale information into the broader list call it was unreachable for.

##### Unordered `unreachable` contents

It is important for broad API consistency that the contents of `unreachable` not have a specific or order semantic structure. If each API baked a specific ordering into a standard field, no single implementation, client or server side, would be correct.

##### Per page `unreachable` resources

Populating `unreachable` resources on a per page basis allows end users to identify immediately when a page is incomplete, rather than *after* paging through all results. Paging to completion is not guaranteed, so it is important to communicate as soon as possible when there are unreachable resource missing from a given page. Furthermore, it allows users to identify when there is a potential issue that they need to account for in subsequent calls. Finally, retaining unreachable resources until the end of paging results requires services to retain the state for what should be indepedent and fully isolated API calls.

##### Using request field to opt-in

Introducing a new request field as means of opting into the partial success behavior is the best way to communicate user intent while keeping the default behavior backwards compatible. The alternative, changing the default behavior with the introduction of the `unreachable` response field, presents a backwards incompatible change. Users that previously expected failure when any resource was unreachable, assume the successful response means all resources are accounted for in the response.

##### Introducing fields simultaneously

Introducing the request and response fields simultaneously is to prevent an invalid intermediate state that is presented by only adding one or the other. If only `unreachable` is added, then it could be assumed that it being empty means all resources were returned when that may not be true. If only `return_partial_success` is added, then the user wouldn't have a means of knowing which resources were unreachable.

##### Partial success granularity limitations

At a certain level of request scope granularity, an API is simply unable to enumerate the resources that are unreachable. For example, global-only APIs may be unable to provide granularity at a localized collection level. In such a case, preemptively returning an error when `return_partial_success=true` protects the user from the risks of the alternative - expecting unreachable resources if there was an issue, but not getting any, thus falsely assuming everything was retrieved. This aligns with guidance herein that suggests failing requests that cannot be fulfilled preemptively.

#### History

The original guidance for how to populate the `unreachable` field revolved around consuming the contents as if they were the paged results. This meant that paged resources and unreachable resources couldn't be returned in the same response i.e. page, and users needed to completely page through all results in order to see if any were unreachable. See the Rationale section for the reasoning around the changes.
