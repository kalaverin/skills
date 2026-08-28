# Protobuf Style Guide & Lint Rules Reference

This document is a compilation of [Buf's Protobuf Style Guide](https://buf.build/docs/best-practices/style-guide/) and the authoritative [Buf Lint Rules Reference](https://buf.build/docs/lint/rules/). It is intended to serve as the exhaustive, single-source-of-truth for agents working on Protobuf schemas in this repository.

Every rule here originates from the `STANDARD` lint category (which `buf lint` enforces by default), unless explicitly noted otherwise.

---

## Quick Start
[ref: #quick-start]

Turn on the complete rule set with one block in `buf.yaml`:

```yaml
version: v2
lint:
  use:
    - STANDARD
```

`STANDARD` is the default when `buf.yaml` has no `lint` section.

---

## Files and Packages
[ref: #files-and-packages]

### 1. Every file must declare a package

**Rule:** `PACKAGE_DEFINED`  
**Categories:** `MINIMAL`, `BASIC`, `STANDARD`

All `.proto` files must have a `package` declaration. Without it, downstream tooling (especially in Go, Java, and other package-based ecosystems) has no reliable namespace to map types to.

### 2. Package layout must mirror directory layout

**Rules:** `DIRECTORY_SAME_PACKAGE`, `PACKAGE_SAME_DIRECTORY`, `PACKAGE_DIRECTORY_MATCH`  
**Categories:** `MINIMAL`, `BASIC`, `STANDARD`

All files of the same package must be in the **same directory**, and every file must live in a directory that matches its package name.

For a module rooted in the `proto` directory, the expected layout is:

```
.
├── buf.yaml
└── proto
    └── foo
        └── bar
            ├── bat
            │   └── v1
            │       └── bat.proto // package foo.bar.bat.v1
            └── baz
                └── v1
                    ├── baz.proto         // package foo.bar.baz.v1
                    └── baz_service.proto // package foo.bar.baz.v1
```

This lets imports self-document their package: the path `foo/bar/bat/v1/bat.proto` contains types in `foo.bar.bat.v1`.

### 3. Packages must be `lower_snake_case`

**Rule:** `PACKAGE_LOWER_SNAKE_CASE`  
**Categories:** `BASIC`, `STANDARD`

Use `foo.bar_baz.v1`, not `foo.barBaz.v1` or `foo.BarBaz.v1`.

### 4. The last package component must be a version

**Rule:** `PACKAGE_VERSION_SUFFIX`  
**Categories:** `STANDARD`

The final component of a package must be a version string matching one of these forms:

- `v\d+` — e.g., `v1`, `v2`
- `v\d+test.*` — e.g., `v1test`, `v1testfoo`
- `v\d+(alpha|beta)\d*` — e.g., `v1alpha`, `v1alpha1`, `v1beta2`
- `v\d+p\d+(alpha|beta)\d*` — e.g., `v1p1alpha`, `v1p1beta2`

Numeric parts must be at least `1`.

**Why:** A core promise of Protobuf API development is that schemas don't introduce breaking changes. When an incompatible revision is needed, the standard pattern is to publish a new versioned package alongside the old one and migrate callers. This rule ensures the new-version path is always available.

### 5. Filenames must be `lower_snake_case.proto`

**Rule:** `FILE_LOWER_SNAKE_CASE`  
**Categories:** `STANDARD`

Examples: `foo_bar.proto`, `baz_service.proto`.

### 6. File options must be consistent within a package

**Rules:** `PACKAGE_SAME_CSHARP_NAMESPACE`, `PACKAGE_SAME_GO_PACKAGE`, `PACKAGE_SAME_JAVA_MULTIPLE_FILES`, `PACKAGE_SAME_JAVA_PACKAGE`, `PACKAGE_SAME_PHP_NAMESPACE`, `PACKAGE_SAME_RUBY_PACKAGE`, `PACKAGE_SAME_SWIFT_PREFIX`  
**Categories:** `BASIC`, `STANDARD`

The following file options must either **all have the same value** or **all be unset** across every file that shares a package:

- `csharp_namespace`
- `go_package`
- `java_multiple_files`
- `java_package`
- `php_namespace`
- `ruby_package`
- `swift_prefix`

**Example:**

`foo_one.proto`:

```proto
syntax = "proto3";

package foo.v1;

option go_package = "foov1";
option java_multiple_files = true;
option java_package = "com.foo.v1";
```

`foo_two.proto`:

```proto
syntax = "proto3";

package foo.v1;

option go_package = "foov1";
option java_multiple_files = true;
option java_package = "com.foo.v1";
```

The other options (`csharp_namespace`, `php_namespace`, etc.) must be unset in both files.

---

## Imports
[ref: #imports]

### 7. Don't use `public` or `weak` imports

**Rules:** `IMPORT_NO_PUBLIC`, `IMPORT_NO_WEAK`  
**Categories:** `BASIC`, `STANDARD` (`IMPORT_NO_PUBLIC` only)

Never declare imports as `public` or `weak`.

**Why:** `public` imports create transitive dependencies that leak through your API surface in unpredictable ways. `weak` imports are deprecated and no longer supported by `protobuf-go`. For background, see Buf's "Tip of the Week #5: Avoid import public/weak".

### 8. Every import must be used

**Rule:** `IMPORT_USED`  
**Categories:** `BASIC`, `STANDARD`

Remove any `import` statement that is not referenced in the file. Unused imports create unnecessary coupling and slow down compilation.

**Failing example:**

```proto
syntax = "proto3";

package payments.v1;

import "product.proto"; // Unused import — violates IMPORT_USED

message Payment {
  string payment_id = 1;
}
```

---

## Enums
[ref: #enums]

### 9. The first enum value must be the zero value

**Rule:** `ENUM_FIRST_VALUE_ZERO`  
**Categories:** `BASIC`, `STANDARD`

The first enum value (tag `0`) must be the zero value. `proto3` requires this; `buf lint` enforces it in `proto2` as well.

**Failing example:**

```proto
syntax = "proto2";

enum Scheme {
  // DON'T DO THIS
  SCHEME_FTP = 1;
  SCHEME_UNSPECIFIED = 0;
}
```

### 10. Don't allow enum aliases

**Rule:** `ENUM_NO_ALLOW_ALIAS`  
**Categories:** `BASIC`, `STANDARD`

Forbid the `allow_alias = true` option on enums.

**Why:** Aliased enums let multiple names share the same numeric value. This causes problems with the JSON representation, which serializes enum values by name: a binary value can deserialize as either alias, and the two are no longer interchangeable across protocols. Instead of aliasing, deprecate the existing value and add a new one.

**Failing example:**

```proto
enum Foo {
  option allow_alias = true; // DON'T DO THIS
  FOO_UNSPECIFIED = 0;
  FOO_ONE = 1;
  FOO_TWO = 1; // alias
}
```

### 11. Enum names must be `PascalCase`

**Rule:** `ENUM_PASCAL_CASE`  
**Categories:** `BASIC`, `STANDARD`

Example: `enum FooBar {}`

### 12. Enum value names must be `UPPER_SNAKE_CASE`

**Rule:** `ENUM_VALUE_UPPER_SNAKE_CASE`  
**Categories:** `BASIC`, `STANDARD`

Example: `FOO_BAR_UNSPECIFIED`, `HTTP`, `HTTPS`.

### 13. Prefix enum values with the enum name

**Rule:** `ENUM_VALUE_PREFIX`  
**Categories:** `STANDARD`

All enum value names must be prefixed with the `UPPER_SNAKE_CASE` form of the enum name.

**Why:** Protobuf enums use C++ scoping rules: two enums in the same package cannot share the same value name (except when nested inside a message, where the rule applies inside that message). Even when names look unique today, schemas evolve over years, and you often need to prefix anyway to add a related enum later.

**Example:**

```proto
enum Scheme {
  SCHEME_UNSPECIFIED = 0;
  SCHEME_HTTP = 1;
  SCHEME_HTTPS = 2;
}
```

Two years later, adding a related enum in the same package is safe:

```proto
enum SecureProtocol {
  SECURE_PROTOCOL_UNSPECIFIED = 0;
  SECURE_PROTOCOL_HTTPS = 1;
  // No collision with SCHEME_HTTPS
}
```

### 14. Suffix the zero value with `_UNSPECIFIED`

**Rule:** `ENUM_ZERO_VALUE_SUFFIX`  
**Categories:** `STANDARD`

The zero value of every enum must end in `_UNSPECIFIED`. The suffix is configurable in `buf.yaml`.

**Why:** `proto3` does not differentiate between set and unset fields: an unset enum field defaults to the zero value. If the zero value isn't explicit and descriptive, any `Uri` with `scheme` not explicitly set would default to whatever happens to be at position 0 — e.g., `SCHEME_FTP` — which is almost certainly wrong.

**Example:**

```proto
enum FooBar {
  FOO_BAR_UNSPECIFIED = 0;
  FOO_BAR_ONE = 1;
}
```

---

## Messages
[ref: #messages]

### 15. Message names must be `PascalCase`

**Rule:** `MESSAGE_PASCAL_CASE`  
**Categories:** `BASIC`, `STANDARD`

Example: `message FooBar {}`

### 16. Field names must be `lower_snake_case`

**Rule:** `FIELD_LOWER_SNAKE_CASE`  
**Categories:** `BASIC`, `STANDARD`

Example: `string foo_bar = 1;`

### 17. `oneof` names must be `lower_snake_case`

**Rule:** `ONEOF_LOWER_SNAKE_CASE`  
**Categories:** `BASIC`, `STANDARD`

Example: `oneof result {}`

### 18. Don't use `required` fields

**Rule:** `FIELD_NOT_REQUIRED`  
**Categories:** `BASIC`, `STANDARD` (v2 configurations only)

Forbids `required` labels in `proto2` and `field_presence = LEGACY_REQUIRED` in Editions. Required fields break backward compatibility because they cannot be safely removed or relaxed.

---

## Services and RPCs
[ref: #services-and-rpcs]

### 19. Service names must be `PascalCase`

**Rule:** `SERVICE_PASCAL_CASE`  
**Categories:** `BASIC`, `STANDARD`

Example: `service FooService {}`

### 20. Service names must end with `Service`

**Rule:** `SERVICE_SUFFIX`  
**Categories:** `STANDARD`

Service names must end in `Service`. The suffix is configurable (e.g., `Endpoint`).

**Why:** Service naming overlaps heavily with package naming, and a consistent suffix removes a class of small inconsistencies that creep in over time.

**Example:**

```proto
service FooService {}
service BarService {}
```

### 21. RPC names must be `PascalCase`

**Rule:** `RPC_PASCAL_CASE`  
**Categories:** `BASIC`, `STANDARD`

Example: `rpc Bar(BarRequest) returns (BarResponse);`

### 22. Every RPC must have unique request and response messages

**Rules:** `RPC_REQUEST_RESPONSE_UNIQUE`, `RPC_REQUEST_STANDARD_NAME`, `RPC_RESPONSE_STANDARD_NAME`  
**Categories:** `STANDARD`

This is one of the most important rules in modern Protobuf development.

Every RPC must have its **own** request and response messages, never shared with another RPC. Sharing a message between RPCs means every change to that message ripples across every RPC that references it.

Request and response messages must be named after the RPC, using **either** of these two patterns:

1. `MethodNameRequest` / `MethodNameResponse`
2. `ServiceNameMethodNameRequest` / `ServiceNameMethodNameResponse`

**Example:**

```proto
service FooService {
  rpc Bar(BarRequest) returns (BarResponse);
  rpc Baz(FooServiceBazRequest) returns (FooServiceBazResponse);
}
```

### 23. Don't use `google.protobuf.Empty`

Giving each RPC its own request and response message preserves maximum flexibility to evolve the RPC without breaking backward compatibility. This applies to Protobuf in general, for both gRPC and ConnectRPC.

Don't import and use `google.protobuf.Empty` when an RPC doesn't happen to have any request or response data yet. Define a custom empty request and/or response message per RPC instead. When the request or response eventually gains fields, you can add them without fear of breaking changes.

If you are modeling a message that is genuinely always empty (as opposed to one whose shape you're not yet sure about), `Empty` is acceptable. Custom empty types are more future-proof.

To use `Empty` with `buf lint`, set the corresponding flags in `buf.yaml`:

```yaml
version: v2
lint:
  use:
    - STANDARD
  rpc_allow_google_protobuf_empty_requests: true
  rpc_allow_google_protobuf_empty_responses: true
```

### 24. Avoid streaming RPCs

**Rules:** `RPC_NO_CLIENT_STREAMING`, `RPC_NO_SERVER_STREAMING`  
**Categories:** `UNARY_RPC`

Streaming RPCs are difficult to implement and call, and often require special proxy, firewall, and network configuration. Polling and pagination are usually much simpler and nearly as efficient.

For the rare cases where streaming is worth the complexity, add exceptions to your lint configuration or use the `UNARY_RPC` category to forbid them entirely.

---

## Comments and File Layout
[ref: #comments-and-layout]

### 25. Every file must declare a syntax

**Rule:** `SYNTAX_SPECIFIED`  
**Categories:** `BASIC`, `STANDARD`

Every `.proto` file must declare `syntax = "proto3";` (or `"proto2"` / Editions syntax).

### 26. Use `//` comments, not `/* */`

Use `//` for all comments. `buf format` enforces this.

### 27. Over-document with complete sentences

Write comments as complete sentences. Put documentation **above** the type, not inline.

### 28. File layout order

Lay files out in this order, matching Google's current recommendations. `buf format` enforces everything below except the first two items:

1. License header (if applicable)
2. File overview
3. `syntax`
4. `package`
5. `imports` (sorted)
6. File options
7. Everything else

### 29. Schema elements should have leading comments

**Rules:** `COMMENT_ENUM`, `COMMENT_ENUM_VALUE`, `COMMENT_FIELD`, `COMMENT_MESSAGE`, `COMMENT_ONEOF`, `COMMENT_RPC`, `COMMENT_SERVICE`  
**Categories:** `COMMENTS`

Each element type can be required to have a non-empty leading comment. Only **leading** comments count; inline comments do not satisfy these rules.

Enable them selectively in `buf.yaml`:

```yaml
version: v2
lint:
  use:
    - STANDARD
    - COMMENT_SERVICE
    - COMMENT_RPC
```

---

## Design Recommendations
[ref: #design-recommendations]

These are not enforced by `buf lint`, but Buf strongly recommends them for any production Protobuf schema.

### Set up breaking change detection from day one

See Buf's [breaking change detection](https://buf.build/docs/breaking/overview/) documentation. It is the companion check to lint, for schema evolution over time.

### Avoid keywords from popular languages

Avoid using keywords from popular languages in any type or package name. For example, a package named `foo.internal.bar` blocks importing the generated Go stubs from other Go packages, because `internal` is a reserved directory name in Go.

### Use pluralized names for repeated fields

```proto
message User {
  repeated string email_addresses = 1;
}
```

### Name fields after their type when possible

For a field of message type `FooBar`, name the field `foo_bar` unless there's a specific reason to do otherwise.

### Avoid nested enums and nested messages

You may want to reference them outside their enclosing message later, even if you don't think so now. Flatten them to the package level.

### Avoid streaming RPCs

(See [Rule 24](#24-avoid-streaming-rpcs).)

---

## Rule Categories
[ref: #rule-categories]

Buf's built-in rules belong to five categories. Three are arranged in a strictness hierarchy:

| Category | Description |
|----------|-------------|
| `MINIMAL` | Fundamental Protobuf hygiene: packages, directory matching, no import cycles. |
| `BASIC` | Widely accepted standard style: naming conventions, no `public` imports, consistent file options. |
| `STANDARD` | Buf's recommended baseline. Includes everything in `BASIC` plus versioning, service suffixes, RPC naming, protovalidate, and enum zero-value suffixes. **Default if no `lint` section is configured.** |

Anything passing `STANDARD` also passes `BASIC` and `MINIMAL`.

Two independent categories:

| Category | Description |
|----------|-------------|
| `COMMENTS` | Requires leading comments on schema elements (services, RPCs, messages, enums, fields, oneofs, enum values). Each element type is its own rule. |
| `UNARY_RPC` | Forbids client and server streaming RPCs. Useful when your transport doesn't support streaming (e.g., Twirp) or when your team has decided against it. |

### MINIMAL rules

- `DIRECTORY_SAME_PACKAGE`
- `PACKAGE_DEFINED`
- `PACKAGE_DIRECTORY_MATCH`
- `PACKAGE_NO_IMPORT_CYCLE`
- `PACKAGE_SAME_DIRECTORY`

### BASIC rules (MINIMAL + these)

- `ENUM_FIRST_VALUE_ZERO`
- `ENUM_NO_ALLOW_ALIAS`
- `ENUM_PASCAL_CASE`
- `ENUM_VALUE_UPPER_SNAKE_CASE`
- `FIELD_LOWER_SNAKE_CASE`
- `FIELD_NOT_REQUIRED`
- `IMPORT_NO_PUBLIC`
- `IMPORT_USED`
- `MESSAGE_PASCAL_CASE`
- `ONEOF_LOWER_SNAKE_CASE`
- `PACKAGE_LOWER_SNAKE_CASE`
- `PACKAGE_SAME_CSHARP_NAMESPACE`
- `PACKAGE_SAME_GO_PACKAGE`
- `PACKAGE_SAME_JAVA_MULTIPLE_FILES`
- `PACKAGE_SAME_JAVA_PACKAGE`
- `PACKAGE_SAME_PHP_NAMESPACE`
- `PACKAGE_SAME_RUBY_PACKAGE`
- `PACKAGE_SAME_SWIFT_PREFIX`
- `RPC_PASCAL_CASE`
- `SERVICE_PASCAL_CASE`
- `SYNTAX_SPECIFIED`

### STANDARD rules (BASIC + these)

- `ENUM_VALUE_PREFIX`
- `ENUM_ZERO_VALUE_SUFFIX`
- `FILE_LOWER_SNAKE_CASE`
- `PACKAGE_VERSION_SUFFIX`
- `PROTOVALIDATE`
- `RPC_REQUEST_RESPONSE_UNIQUE`
- `RPC_REQUEST_STANDARD_NAME`
- `RPC_RESPONSE_STANDARD_NAME`
- `SERVICE_SUFFIX`

---

## Complete Rule Reference
[ref: #rule-reference]

Rules are listed alphabetically with their categories and full rationale.

### `COMMENT_ENUM`
**Categories:** `COMMENTS`  
Enums must have non-empty leading comments.

### `COMMENT_ENUM_VALUE`
**Categories:** `COMMENTS`  
Enum values must have non-empty leading comments.

### `COMMENT_FIELD`
**Categories:** `COMMENTS`  
Fields must have non-empty leading comments.

### `COMMENT_MESSAGE`
**Categories:** `COMMENTS`  
Messages must have non-empty leading comments.

### `COMMENT_ONEOF`
**Categories:** `COMMENTS`  
Oneofs must have non-empty leading comments.

### `COMMENT_RPC`
**Categories:** `COMMENTS`  
RPCs must have non-empty leading comments.

### `COMMENT_SERVICE`
**Categories:** `COMMENTS`  
Services must have non-empty leading comments.

### `DIRECTORY_SAME_PACKAGE`
**Categories:** `MINIMAL`, `BASIC`, `STANDARD`  
All files in a given directory must share the same package.

### `ENUM_FIRST_VALUE_ZERO`
**Categories:** `BASIC`, `STANDARD`  
The first enum value must be the zero value. `proto3` requires this; `buf lint` enforces it in `proto2` as well.

### `ENUM_NO_ALLOW_ALIAS`
**Categories:** `BASIC`, `STANDARD`  
Forbids aliased enums. Aliasing causes problems with JSON representation because the same number can deserialize as either alias, making them non-interchangeable across protocols. Deprecate the old value and add a new one instead.

### `ENUM_PASCAL_CASE`
**Categories:** `BASIC`, `STANDARD`  
Enums must be `PascalCase`.

### `ENUM_VALUE_PREFIX`
**Categories:** `STANDARD`  
Enum value names must be prefixed with the enum name. Protobuf enums use C++ scoping rules: two enums in the same package can't have the same value name. Prefixing prevents future collisions as the schema evolves.

### `ENUM_VALUE_UPPER_SNAKE_CASE`
**Categories:** `BASIC`, `STANDARD`  
Enum values must be `UPPER_SNAKE_CASE`.

### `ENUM_ZERO_VALUE_SUFFIX`
**Categories:** `STANDARD`  
The zero value of every enum must end in `_UNSPECIFIED` (configurable). In `proto3`, unset enum fields default to the zero value; an explicit, descriptive zero value prevents accidental semantic defaults like `SCHEME_FTP = 0`.

### `FIELD_LOWER_SNAKE_CASE`
**Categories:** `BASIC`, `STANDARD`  
Field names must be `lower_snake_case`.

### `FIELD_NOT_REQUIRED`
**Categories:** `BASIC`, `STANDARD` (v2 only)  
Forbids `required` labels in `proto2` and `field_presence = LEGACY_REQUIRED` in Editions. Required fields break backward compatibility.

### `FILE_LOWER_SNAKE_CASE`
**Categories:** `STANDARD`  
`.proto` file names must be `lower_snake_case.proto`.

### `IMPORT_NO_PUBLIC`
**Categories:** `BASIC`, `STANDARD`  
Forbids `public` imports. They create leaky transitive dependencies.

### `IMPORT_NO_WEAK`
**Deprecated; no replacement.** The rule is effectively ignored: `protobuf-go` no longer supports weak imports.

### `IMPORT_USED`
**Categories:** `BASIC`, `STANDARD`  
Every declared import must be referenced. Unused imports create unnecessary coupling.

### `MESSAGE_PASCAL_CASE`
**Categories:** `BASIC`, `STANDARD`  
Messages must be `PascalCase`.

### `ONEOF_LOWER_SNAKE_CASE`
**Categories:** `BASIC`, `STANDARD`  
Oneof names must be `lower_snake_case`.

### `PACKAGE_DEFINED`
**Categories:** `MINIMAL`, `BASIC`, `STANDARD`  
Every file must declare a package.

### `PACKAGE_DIRECTORY_MATCH`
**Categories:** `MINIMAL`, `BASIC`, `STANDARD`  
A file's directory path must match its package name.

### `PACKAGE_LOWER_SNAKE_CASE`
**Categories:** `BASIC`, `STANDARD`  
Packages must be `lower_snake_case`.

### `PACKAGE_NO_IMPORT_CYCLE`
**Categories:** `MINIMAL`, `BASIC`, `STANDARD` (v2 only)  
Detects package import cycles. The Protobuf compiler forbids circular file imports, but still permits package cycles. These compile but cause problems for languages that rely on package-based imports (Go especially).

**Example of a package cycle:**

```proto
// foo/one.proto
package foo;
import "bar/three.proto";
message One { bar.Three three = 3; }

// bar/four.proto
package bar;
import "foo/one.proto";
message Four { foo.One one = 1; }
```

### `PACKAGE_SAME_<file_option>`
**Categories:** `BASIC`, `STANDARD`  
If a file option is declared, it must match across every file in the package:

- `PACKAGE_SAME_CSHARP_NAMESPACE` → `csharp_namespace`
- `PACKAGE_SAME_GO_PACKAGE` → `go_package`
- `PACKAGE_SAME_JAVA_MULTIPLE_FILES` → `java_multiple_files`
- `PACKAGE_SAME_JAVA_PACKAGE` → `java_package`
- `PACKAGE_SAME_PHP_NAMESPACE` → `php_namespace`
- `PACKAGE_SAME_RUBY_PACKAGE` → `ruby_package`
- `PACKAGE_SAME_SWIFT_PREFIX` → `swift_prefix`

### `PACKAGE_SAME_DIRECTORY`
**Categories:** `MINIMAL`, `BASIC`, `STANDARD`  
All files with a given package must live in the same directory.

### `PACKAGE_VERSION_SUFFIX`
**Categories:** `STANDARD`  
The last component of a package must be a version. This enables the standard pattern of publishing a new versioned package when an incompatible revision is needed.

Valid forms: `v1`, `v2`, `v1alpha`, `v1alpha1`, `v1beta2`, `v1p1alpha`, `v1p1beta2`, `v1test`, `v1testfoo`.

### `PROTOVALIDATE`
**Categories:** `STANDARD`  
Validates that `protovalidate` constraints are well-formed at lint time so they don't fail at runtime.

**For `buf.validate.field`:**
- `ignore` is the only option set when `ignore` is `IGNORE_ALWAYS`.
- `required` is not set when `ignore` is `IGNORE_IF_ZERO_VALUE`.
- `required` is not set when the field is part of a `oneof`.
- Neither `required` nor `IGNORE_IF_ZERO_VALUE` is set when the field is an extension.
- CEL constraints compile successfully and evaluate to `string` or `bool`.
- Each `cel_expression` entry is valid.
- Type-specific rules (`int32`, `string`, etc.) are valid for the field's type.

**For `buf.validate.message`:**
- `disabled` is the only field set when `disabled` is set.
- CEL constraints are valid.

**CEL constraint validity:**
- Expression compiles and returns `string` or `bool`.
- Non-empty `message` when expression returns `bool`.
- Empty `message` when expression returns `string`.
- Non-empty `id` of alphanumeric characters, `_`, `-`, `.` only, unique within its scope.

**Type-specific rule checks:**
- Rules' type matches the field type.
- At least one value satisfies the rules (no contradictions like `contains: "foo"` + `not_contains: "foo"`).
- No obviously redundant rules (e.g., `lt: 5` with `const: 3`).

**Numeric / timestamp / duration rules:**
- Lower and upper bounds must not be equal (replace with `const` if they are).
- Durations and timestamps in options must be valid.
- `timestamp.within` must be a positive duration.
- `timestamp.lt_now` and `timestamp.gt_now` can't both be set.

**String rules:**
- Field type is `string` or `google.protobuf.StringValue`.
- `len` is mutually exclusive with `min_len` / `max_len`.
- `len_bytes` is mutually exclusive with `min_bytes` / `max_bytes`.
- `min_len` ≤ `max_bytes`; `min_bytes` ≤ `4 * max_len`.
- `prefix` / `suffix` / `contains` lengths must not exceed `max_len` or `max_bytes`.
- `prefix` / `suffix` / `contains` values must not appear inside `not_contains`.
- If `strict` is `false`, `well_known_regex` must also be set.
- `pattern` must be a valid RE2 regular expression.

**Bytes rules:**
- Field type is `bytes` or `google.protobuf.BytesValue`.
- `len` is mutually exclusive with `min_len` / `max_len`.
- `prefix` / `suffix` / `contains` lengths must not exceed `max_len`.
- `pattern` must be a valid RE2 regular expression.

**Map rules:**
- Field type is a map.
- `min_pairs` ≤ `max_pairs`.
- `keys` rules are valid and compatible with the key type; `required` can't be set in `keys`.
- `values` rules are valid and compatible with the value type; `required` can't be set in `values`.

**Repeated rules:**
- Field carries the `repeated` label.
- `min_items` ≤ `max_items`.
- `items` rules are compatible with the element type; `required` can't be set in `items`.
- If `unique` is `true`, the element type must be a scalar or a wrapper type.

### `RPC_NO_CLIENT_STREAMING`
**Categories:** `UNARY_RPC`  
RPCs must not use client streaming.

### `RPC_NO_SERVER_STREAMING`
**Categories:** `UNARY_RPC`  
RPCs must not use server streaming.

### `RPC_PASCAL_CASE`
**Categories:** `BASIC`, `STANDARD`  
RPCs must be `PascalCase`.

### `RPC_REQUEST_RESPONSE_UNIQUE`
**Categories:** `STANDARD`  
All request and response messages must be unique across the schema. Sharing messages between RPCs couples their evolution.

### `RPC_REQUEST_STANDARD_NAME`
**Categories:** `STANDARD`  
Request messages must be named `MethodNameRequest` or `ServiceNameMethodNameRequest`.

### `RPC_RESPONSE_STANDARD_NAME`
**Categories:** `STANDARD`  
Response messages must be named `MethodNameResponse` or `ServiceNameMethodNameResponse`.

### `SERVICE_PASCAL_CASE`
**Categories:** `BASIC`, `STANDARD`  
Services must be `PascalCase`.

### `SERVICE_SUFFIX`
**Categories:** `STANDARD`  
Service names must end in `Service` (configurable, e.g., `Endpoint`). A consistent suffix prevents naming collisions and creeping inconsistencies.

### `STABLE_PACKAGE_NO_IMPORT_UNSTABLE`
**Categories:** none (opt-in)  
Files in stable versioned packages (e.g., `v1`) must not import packages with unstable versions (e.g., `alpha`, `beta`, `v1alpha1`). Enable explicitly:

```yaml
version: v2
lint:
  use:
    - STANDARD
    - STABLE_PACKAGE_NO_IMPORT_UNSTABLE
```

### `SYNTAX_SPECIFIED`
**Categories:** `BASIC`, `STANDARD`  
Every file must declare a syntax (`proto3`, `proto2`, or Editions).

---

## What Was Left Out
[ref: #what-was-left-out]

Three areas are intentionally left to your organization or to Buf check plugins:

### File option values

The Buf CLI doesn't lint specific values for file options. Language-specific options (`java_package`, `go_package`, etc.) are artifacts of code generation, not the core schema. Most have a deterministic mapping from the package name. Managed mode in `buf generate` can set these on the fly, so they don't need to be hand-written.

The `PACKAGE_SAME_<file_option>` rules still enforce internal consistency: whichever values you pick must be the same across every file in a package.

### Custom options

Built-in rules cover standard file options and Protovalidate constraints. For other custom options like `google.api` annotations, write a Buf check plugin.

### Naming opinions beyond the basics

`STANDARD` enforces only the naming rules that apply broadly: package versioning, `lower_snake_case` packages, `PascalCase` types. It does not impose conventions like a specific suffix on `google.protobuf.Timestamp` fields or restrictions on top-level package names. Buf check plugins cover the rest.

---

## Configuration
[ref: #configuration]

### Allowing `google.protobuf.Empty`

```yaml
version: v2
lint:
  use:
    - STANDARD
  rpc_allow_google_protobuf_empty_requests: true
  rpc_allow_google_protobuf_empty_responses: true
```

### Changing the service suffix

```yaml
version: v2
lint:
  service_suffix: Endpoint
```

### Changing the enum zero-value suffix

```yaml
version: v2
lint:
  enum_zero_value_suffix: _UNKNOWN
```

### Allowing same request/response types

```yaml
version: v2
lint:
  rpc_allow_same_request_response: true
```

### Requiring comments selectively

```yaml
version: v2
lint:
  use:
    - STANDARD
    - COMMENT_SERVICE
    - COMMENT_RPC
```

### Forbidding streaming RPCs

```yaml
version: v2
lint:
  use:
    - STANDARD
    - UNARY_RPC
```

### Stable packages may not import unstable packages

```yaml
version: v2
lint:
  use:
    - STANDARD
    - STABLE_PACKAGE_NO_IMPORT_UNSTABLE
```
