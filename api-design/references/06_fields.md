## 6. Fields

### 6.1 Field Names (AIP-140)
[ref: #field-names-aip-140]

Field names are the primary interface through which users understand an API. Inconsistent, ambiguous, or overly verbose names cause confusion across APIs and complicate client generation. APIs **must** use simple, intuitive, and consistent field names.

**Clarity and precision**

Field names **should** clearly and precisely communicate the concept being presented. Avoid overly general names that are ambiguous. At the same time, field names **should** avoid unnecessary words, including adjectives that always apply and add no cognitive value. For example, prefer `proxy_settings` over `shared_proxy_settings` if there is no unshared variant.

**Important:** Field names appear in generated client surfaces. They **must** be appropriately descriptive and of suitable length.

#### Case

Field definitions in protobuf files **must** use `lower_snake_case` names. These names are mapped to an appropriate naming convention in JSON and in generated code.

Additionally, each word in the field **must not** begin with a number, because it creates ambiguity when converting between snake case and camel case. Fields **must not** contain leading, trailing, or adjacent underscores.

#### Uniformity

APIs **should** use the same name for the same concept and different names for different concepts wherever possible, including across multiple APIs that are likely to be used together.

#### Repeated fields

Repeated fields **must** use the proper plural form, such as `books` or `authors`. Non-repeated fields **should** use the singular form, such as `book` or `author`. Resource names **should** also use the singular form, since the field name should follow the resource name:

```protobuf
// Correct
message Shelf {
  repeated Book books = 1;
}

// Incorrect
message Shelf {
  repeated Books books = 1;
}
```

#### Prepositions

Field names **should not** include prepositions (such as "with", "for", "at", "by", etc.):

- `error_reason` (not `reason_for_error`)
- `author` (not `written_by`)

Prepositions in field names may indicate a design concern, such as an overly-restrictive field or a sub-optimal data type. A field named `book_with_publisher` likely indicates that the book resource is improperly structured.

**Note:** The word "per" is an exception when used as part of a unit (e.g., "miles per hour"). See AIP-141 for guidance on quantity fields.

#### Abbreviations

For well-known abbreviations among software developers, the abbreviation **should** be used instead of the full spelling:

- `config` (not `configuration`)
- `id` (not `identifier`)
- `info` (not `information`)
- `spec` (not `specification`)
- `stats` (not `statistics`)

Well-known abbreviations for units **should** also be used in field names. See AIP-141 for more guidance on quantity fields:

- `distance_km` (not `distance_kilometers`)
- `width_px` (not `width_pixels`)

#### Adjectives

Field names that contain both a noun and an adjective **should** place the adjective _before_ the noun:

- `collected_items` (not `items_collected`)
- `imported_objects` (not `objects_imported`)

#### Verbs

Field names **must not** reflect intent or action; they **must not** be verbs. The field defines the _desired value_ for mutations (Create, Update) and the _current value_ for reads (Get, List). The name **must** be a noun:

- `collected_items` (not `collect_items`)
- `disabled` (not `disable`)

Method names (standard or custom) are verbs because they change facets of resources.

#### Booleans

Boolean fields **should** omit the prefix "is":

- `disabled` (not `is_disabled`)
- `required` (not `is_required`)

**Exception:** Field names that would otherwise be reserved words. For example, `is_new` (not `new`).

#### String vs. bytes

When using `bytes`, the contents are base64-encoded when using JSON on the wire. Services **should** use `bytes` when there is a need to send binary contents over the wire, and **should not** ask the user to manually base64-encode a field into a `string`.

**Exception:** When the API handles data that is meant to be base64-encoded at rest and double base64-encoding is undesirable, services **may** use a `string`.

#### URIs

Field names representing arbitrary URIs **should** use `uri`. Note that URLs are URIs, but not all URIs are URLs. Field names that can only represent a URL **should** use `url`. A prefix **may** be used in front of `uri` as appropriate:

```protobuf
message Book {
  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  // A URL pointing to an image of the book.
  string image_url = 2;

  // A URI identifying the book. Could be an ISBN or a URL.
  string uri = 3;
}
```

**Note:** APIs that have previously used `uri` for URL fields may continue to do so to avoid unnecessary API changes and to preserve local consistency.

#### Reserved words

Field names **should** avoid names that conflict with keywords in common programming languages, such as `new`, `class`, `function`, `import`, etc. Reserved keywords cause hardship for developers using the API in that language.

#### Conflicts

Messages **should not** include a field with the same name as the enclosing message (ignoring case transformations). This causes conflicts when generating code in some languages.

#### Display names

Many resources have a human-readable name used for display in UI. This field **should** be called `display_name` and **should not** have a uniqueness requirement.

If an entity has an official, formal name (such as a company name or the title of a book), an API **may** use `title` as the field name instead. The `title` field **should not** have a uniqueness requirement.

**Note:** In this project, `display_name` **should** be limited to 63 characters.

#### Further reading

- For naming resource fields, see AIP-122.
- For naming fields representing quantities, see AIP-141.
- For naming fields representing time, see AIP-142.

#### Rationale

**URI vs. URL.** All URLs are URIs, but not all URIs are URLs. Aligning on `uri` enables a more generalizable field that handles a variety of use cases and drives standardization across APIs. The requirement is a **should** to allow more specific terms when truly merited.

### 6.2 Fields and FieldInfo (AIP-202)
[ref: #fields-and-fieldinfo-aip-202]

The `google.api.FieldInfo` type, through its accompanying extension `google.api.field_info`, enriches a field's schema with format information beyond the basic name and type.

**Key principle:** Decorating a field with `google.api.field_info` is only necessary when explicitly stated in this guide or another AIP that leverages `google.api.FieldInfo` information. The guidance below applies to those scenarios.

#### Format

Fields with a primitive type can still have a specific format. To convey that type format, the `FieldInfo.Format` enumeration is used via the `(google.api.field_info).format` extension field.

##### UUID4

The `UUID4` format represents a UUID version 4 value as governed by RFC 4122.

- It **must** only be used on a field of type `string`.
- Such a value **may** be normalized by the service to entirely lowercase letters. For example, `F47AC10B-58CC-0372-8567-0E02B2C3D479` would be normalized to `f47ac10b-58cc-0372-8567-0e02b2c3d479`.
- Equivalence comparison **must not** be done via primitive text comparison. Instead, an RFC 4122 compliant implementation **must** be used.

##### IPv4

The `IPV4` format represents an IP v4 address as governed by RFC 791.

- It **must** only be used on a field of type `string`.
- Such a value **may** be condensed by the service, with leading zeros in each octet stripped. For example, `001.022.233.040` would be condensed to `1.22.233.40`.
- Equivalence comparison **must not** be done via primitive text comparison. Instead, an RFC 791 compliant implementation **must** be used.

##### IPv6

The `IPV6` format represents an IP v6 address as governed by RFC 4291.

- It **must** only be used on a field of type `string`.
- Such a value **may** be normalized by the service to entirely lowercase letters with zeros compressed, following RFC 5952. For example, `2001:0DB8:0::0` would be normalized to `2001:db8::`.
- Equivalence comparison **must not** be done via primitive text comparison. Instead, an RFC 4291 compliant implementation **must** be used.

##### IPv4 or IPv6

The `IPV4_OR_IPV6` value indicates that the field can be either an IP v4 or v6 address, as described in the IPv4 and IPv6 sections.

#### Format compatibility

- Adding a format specifier to an existing, unspecified field **is not** backwards compatible, unless the field in question has always conformed to the format being specified.
- Changing an existing format specifier to a different one **is not** backwards compatible in all cases.

#### Extending format

Any new `FieldInfo.Format` value **must** be governed by an IETF-approved RFC or a Google-approved AIP.

#### Rationale

**Why add a format specifier?**

The format of a primitive-typed field can be critical to its usability. Some programming languages may convey a specific type format as a standalone type, as Java does with `UUID`. Most have specific structural requirements that are validated by the service, so conveying the format to the user ahead of time is critical to their experience.

**Why discourage primitive equality comparisons?**

The text representations of the supported formats have many nuances and transforming the value into a canonical representation is non-trivial. As such, aligning implementations between each consumer and each service without any issue is infeasible.

**Why document value normalizations?**

While primitive comparison is not recommended for any of the supported formats, uniform normalization of values is important to set consumer expectations and create a user-friendly surface.

**Why require an RFC or AIP for new formats?**

Those formats which are sufficiently standardized to merit an RFC or AIP are stable enough and widely enough known to be incorporated as a supported value and see usage in APIs. Requiring such extra guidance means that governing the format specification is not the responsibility of the `FieldInfo.Format` enumeration itself.

### 6.3 Field Behavior Documentation (AIP-203)
[ref: #field-behavior-documentation-aip-203]

When defining fields in protocol buffers, it is customary to explain to users certain aspects of a field's behavior (such as whether it is required or optional). Additionally, it can be useful for other tools to understand this behavior (for example, to optimize client library signatures).

#### Guidance

APIs use the `google.api.field_behavior` annotation to describe well-understood field behavior, such as a field being required or immutable.

```protobuf
// The audio data to be recognized.
RecognitionAudio audio = 2 [(google.api.field_behavior) = REQUIRED];
```

- APIs **must** apply the `google.api.field_behavior` annotation on every field on a message or sub-message used in a request.
- The annotation **must** include any `google.api.FieldBehavior` values that accurately describe the behavior of the field.
  - `FIELD_BEHAVIOR_UNSPECIFIED` **must not** be used.
- APIs **must** at minimum use one of `REQUIRED`, `OPTIONAL`, or `OUTPUT_ONLY`.

**Warning:** Although `field_behavior` does not impact proto-level behavior, many clients (e.g. CLIs and SDKs) rely on them to generate code. Thoroughly review and consider which values are relevant when adding a new field.

Fields with no annotation are interpreted as `OPTIONAL` for backwards compatibility. Nonetheless, this annotation **must not** be omitted.

**Note:** The vocabulary given in this document is for _descriptive_ purposes only, and does not itself add any validation. The purpose is to consistently document this behavior for clients.

##### Field behavior of nested messages

`google.api.field_behavior` annotations on a nested message are independent of the annotations of the parent.

For example, a nested message can have a field behavior of `REQUIRED` while the parent field can be `OPTIONAL`:

```protobuf
message Title {
  string text = 1 [(google.api.field_behavior) = REQUIRED];
}

message Slide {
  Title title = 1 [(google.api.field_behavior) = OPTIONAL];
}
```

In the case above, if a `title` is specified, the `text` field is required.

#### Vocabulary

##### Identifier

The use of `IDENTIFIER` indicates that a field within a resource message is used to identify the resource. It **must** be attached to the `name` field and **must not** be attached to any other field.

The `IDENTIFIER` value conveys that the field is not accepted as input (i.e. `OUTPUT_ONLY`) in the context of a create method, while also being considered `IMMUTABLE` and accepted as input for mutation methods that accept the resource as the primary input (e.g. Standard Update).

This annotation **must not** be applied to references to other resources within a message.

##### Immutable

The use of `IMMUTABLE` indicates that a field on a resource cannot be changed after its creation. This can apply to either fields that are inputs or outputs, required or optional.

When a service receives an immutable field in an update request (or similar), even if included in the update mask, the service **should** ignore the field if the value matches, but **should** error with `INVALID_ARGUMENT` if a change is requested.

Potential use cases for immutable fields (this is not an exhaustive list) are:

- Attributes of resources that are not modifiable for the lifetime of the application (e.g. a disk type).

**Note:** Fields which are "conditionally immutable" **must not** be given the immutable annotation.

##### Input only

The use of `INPUT_ONLY` indicates that the field is provided in requests and that the corresponding field will not be included in output.

Additionally, a field **should** only be described as input only if it is a field in a resource message or a field of a message included within a resource message. Notably, fields in request messages (a message which only ever acts as an argument to an RPC, with a name usually ending in `Request`) **should not** be described as input only because this is already implied.

Potential use cases for input only fields (this is not an exhaustive list) are:

- The `ttl` field as described in AIP-214.

**Warning:** Input only fields are rare and should be considered carefully before use.

##### Optional

The use of `OPTIONAL` indicates that a field is not required.

A field **may** be described as optional if it is a field on a request message (a message that is an argument to an RPC, usually ending in `Request`), or a field on a submessage.

##### Output only

The use of `OUTPUT_ONLY` indicates that the field is provided in responses, but that including the field in a message in a request does nothing (the server **must** clear out any value in this field and **must not** throw an error as a result of the presence of a value in this field on input). Similarly, services **must** ignore the presence of output only fields in update field masks (see AIP-161).

Additionally, a field **should** only be described as output only if it is a field in a resource message, or a field of a message farther down the tree. Notably, fields in response messages (a message which only ever acts as a return value to an RPC, usually ending in `Response`) **should not** be described as output only because this is already implied.

Output only fields **may** be set to empty values if appropriate to the API.

Potential use cases for output only fields (this is not an exhaustive list) are:

- Create or update timestamps.
- Derived or structured information based on original user input.
- Properties of a resource assigned by the service which can not be altered.

##### Required

The use of `REQUIRED` indicates that the field **must** be present (and set to a non-empty value) on the request or resource.

A field **should** only be described as required if _either_:

- It is a field on a resource that a user provides somewhere as input. In this case, the resource is only valid if a "truthy" value is _stored_.
  - When creating the resource, a value **must** be provided for the field on the create request.
  - When updating the resource, the user **may** omit the field provided that the field is also absent from the field mask, indicating no change to the field (otherwise it **must** be provided).
- It is a field on a request message (a message that is an argument to an RPC, with a name usually ending in `Request`). In this case, a value **must** be provided as part of the request, and failure to do so **must** cause an error (usually `INVALID_ARGUMENT`).

We define the term "truthy" above as follows:

- For primitives, values other than `0`, `0.0`, empty string/bytes, and `false`.
- For repeated fields and maps, values with at least one entry.
- For messages, any message with at least one "truthy" field.

Fields **should not** be described as required in order to signify:

- A field which will always be present in a response.
- A field which is conditionally required in some situations.
- A field on any message (including messages that are resources) which is never used as user input.

**Note:** In most cases, empty values (such as `false` for booleans, `0` for integers, or the unspecified value for enums) are indistinguishable from unset values, and therefore setting a required field to a falsy value yields an error. A corollary to this is that a required boolean must be set to `true`.

##### Unordered list

The use of `UNORDERED_LIST` on a repeated field of a resource indicates that the service does not guarantee the order of the items in the list.

A field **should** be described as an unordered list if the service does not guarantee that the order of the elements in the list will match the order that the user sent, including a situation where the service will sort the list on the user's behalf.

A resource with an unordered list **may** return the list in a stable order, or **may** return the list in a randomized, unstable order.

#### Backwards compatibility

Adding or changing `google.api.field_behavior` values can represent a semantic change in the API that is perceived as incompatible for existing clients.

The following are **backwards incompatible** changes:

- Adding `REQUIRED` to an existing field previously considered `OPTIONAL` (implicitly or otherwise).
- Adding a new field annotated as `REQUIRED` to an existing request message.
- Adding `OUTPUT_ONLY` to an existing field previously accepted as input.
- Adding `INPUT_ONLY` to an existing field previously emitted as output.
- Adding `IMMUTABLE` to an existing field previously considered mutable.
- Removing `OUTPUT_ONLY` from an existing field previously ignored as input.
- Removing `IDENTIFIER` from an existing field.

The following are **backwards compatible** changes:

- Adding `OPTIONAL` to an existing field.
- Adding `IDENTIFIER` to an existing `name` field.
- Changing from `REQUIRED` to `OPTIONAL` on an existing field.
- Changing from `OUTPUT_ONLY` and/or `IMMUTABLE` to `IDENTIFIER` on an existing field.
- Removing `REQUIRED` from an existing field.
- Removing `INPUT_ONLY` from an existing field previously excluded in responses.
- Removing `IMMUTABLE` from an existing field previously considered immutable.

#### Rationale

**Why a dedicated `IDENTIFIER` field behavior?**

Resource names, the primary identifiers for any compliant resource, are never fully constructed by the user on create. Such fields are typically assigned `OUTPUT_ONLY` field behavior. They are, however, also often consumed as the primary identifier in scenarios where the resource itself is the primary request payload. Such fields could not be considered `OUTPUT_ONLY`. Furthermore, in mutation requests, like Standard Update, the resource name as the primary identifier cannot be changed in place. Such fields are typically assigned `IMMUTABLE` field behavior. These conflicting and context-dependent field behaviors meant that a new value was necessary to single out and convey the behavior of the resource name field.

**Why require a minimum set of annotations?**

A field used in a request message must be either an input or an output. In the case of an output, the `OUTPUT_ONLY` annotation is sufficient. In the case of an input, a field is either required or optional, and therefore should have at least the `REQUIRED` or `OPTIONAL` annotation, respectively. Only providing `INPUT_ONLY` does not convey the necessity of the field, so specifying either `REQUIRED` or `OPTIONAL` is still necessary.

**Why require `field_behavior` at all?**

By including the field behavior annotation for each field, the overall behavior that the resource exhibits is more clearly defined. Clearly defined field behavior improves programmatic clients and user understanding. Requiring the annotation also forces the API author to explicitly consider the behavior when initially authoring the API. Modifying field behavior after initial authoring can result in backwards-incompatible changes in clients.

#### History

In 2023-05, `field_behavior` was made mandatory. Prior to this change, the annotation was often omitted. Its values are relied upon to produce high quality clients. Furthermore, adding or changing some of the `field_behavior` values after the fact within a major version can be backwards-incompatible. The benefits of requiring `field_behavior` at the time that the API is authored surpass the costs to clients and API users of not doing so.

### 6.4 Quantities (AIP-141)
[ref: #quantities-aip-141]

Many services need to represent a discrete quantity of items (number of bytes, number of miles, number of nodes, etc.).

#### Guidance

Quantities with a clear unit of measurement (such as bytes, miles, and so on) **must** include the unit of measurement as the suffix. When appropriate, units **should** use generally accepted abbreviations, and abbreviations **should not** be pluralized.

```protobuf
// A representation of a non-stop air route.
message Route {
  // The airport where the route begins.
  string origin = 1;

  // The destination airport.
  string destination = 2;

  // The distance between the origin and destination airports.
  // This value is also used to determine the credited frequent flyer miles.
  int32 distance_miles = 3;
}
```

If the quantity is a number of items (for example, the number of nodes in a cluster), then the field **should** use the suffix `_count` ( **not** the prefix `num_`):

```protobuf
// A cluster of individual nodes.
message Cluster {
  // The number of nodes in the cluster.
  int32 node_count = 1;
}
```

**Note:** Fields **must not** use unsigned integer types, because many programming languages and systems do not support them well.

##### Compound units

Quantities with compound units of measurement **may** use separating underscores between units as needed for clarity. Unabbreviated units **must** be separated. Abbreviated units **should not** be separated unless otherwise ambiguous. Compound units **should** be in plural form, with all component units in singular form except for the final component unit, which should be in plural form unless abbreviated.

- `energy_kwh` ( **not** `energy_kw_h`)
- `energy_kw_fortnights` ( **not** `energy_kwfortnight` or `energy_kw_fortnight`)

**Note:** Metric prefixes **must not** be separated from their base unit.

##### Inverse units

Quantities with units of measurement that are or include inverse units **should** indicate all inverse units as a compound unit after a compound of any non-inverse units, separated by the word "per". The inverse compound unit **should** be in singular form.

- `speed_miles_per_hour` ( **not** `speed_mph`)
- `speed_meters_per_second` ( **not** `speed_meters_per_seconds` or `speed_meter_per_second`)
- `event_count_per_hour` ( **not** `events_per_hour`, `event_counts_per_hour`, or `hourly_events`)
- `price_per_kwh` (using `google.type.Money`)

**Note:** This guidance does not apply in cases where generally accepted derived units with special names and symbols exist for inverse quantities. For example, the derived unit "hertz" **should** be used when appropriate for reciprocal time.

##### Specialized messages

It is sometimes useful to create a message that represents a particular quantity. This is particularly valuable in two situations:

- Grouping two or more individual quantities together. Example: `google.protobuf.Duration`
- Representing a common concept where the unit of measurement may itself vary. Example: `google.type.Money`

APIs **may** create messages to represent quantities when appropriate. When using these messages as fields, APIs **should** use the name of the message as the suffix for the field name if it makes intuitive sense to do so.

### 6.5 Time and Duration (AIP-142)
[ref: #time-and-duration-aip-142]

Many services need to represent the concepts surrounding time. Representing time can be challenging due to the intricacies of calendars and time zones, as well as the fact that common exchange formats (such as JSON) lack a native concept of time.

#### Guidance

Fields representing time **should** use the common, generally used components (such as `google.protobuf.Timestamp` or `google.type.Date`) for representing time or duration types. These types are common components, and using them consistently allows infrastructure and tooling to provide a better experience when interacting with time values.

| Concept | Type | Name Suffix |
|---------|------|-------------|
| Absolute timestamp | `google.protobuf.Timestamp` | `_time` (singular) or `_times` (repeated) |
| Duration/span | `google.protobuf.Duration` | `_duration` |
| Relative offset | `google.protobuf.Duration` | `_offset` (with comment explaining relative point) |
| Civil date | `google.type.Date` | `_date` |
| Wall-clock time | `google.type.TimeOfDay` | `_time` |
| Civil timestamp (with timezone) | `google.type.DateTime` | `_time` |

##### Timestamps

Fields that represent an absolute point in time (independent of any time zone or calendar) **should** use the `google.protobuf.Timestamp` type (which uses UNIX timestamps under the hood and holds nanosecond precision).

These fields **should** have names ending in `_time`, such as `create_time` or `update_time`. For repeated fields, the names **should** end in `_times` instead.

Many timestamp fields refer to an activity (for example, `create_time` refers to when the applicable resource was created). For these, the field **should** be named with the `{imperative}_time` form. For example, if a book is being published, the field storing the time when this happens would use the imperative form of the verb "to publish" ("publish") resulting in a field called `publish_time`. Fields **should not** be named using the past tense (such as `published_time`, `created_time`, or `last_updated_time`).

##### Durations

Fields that represent a span between two points in time (independent of any time zone or calendar) **should** use the `google.protobuf.Duration` type.

To illustrate the distinction between timestamps and durations, consider a flight record:

```protobuf
// A representation of a (very incomplete) flight log.
message FlightRecord {
  // The absolute point in time when the plane took off.
  google.protobuf.Timestamp takeoff_time = 1;

  // The length (duration) of the flight, from takeoff to landing.
  google.protobuf.Duration flight_duration = 2;
}
```

**Note:** Observant readers may notice that the timestamp and duration messages have the same structure (`int64 seconds` and `int32 nanos`). However, the distinction between these is important, because they have different semantic meaning. Additionally, tooling is able to base behavior off of which message is used. For example, a Python-based tool could convert timestamps to `datetime` objects and durations to `timedelta` objects.

##### Relative time segments

In some cases, it may be necessary to represent a time segment inside a stream. In these cases, the `google.protobuf.Duration` type **should** be used, and the field name **should** end with `_offset`. To ensure that the meaning is clear, the field **must** have a comment noting the point that the offset is relative to.

To illustrate this, consider a resource representing a segment of an audio stream:

```protobuf
message AudioSegment {
  // The duration relative to the start of the stream representing the
  // beginning of the segment.
  google.protobuf.Duration start_offset = 1;

  // The total length of the segment.
  google.protobuf.Duration segment_duration = 2;
}
```

##### Civil dates and times

Fields that represent a calendar date or wall-clock time **should** use the appropriate common components:

- Civil date: `google.type.Date`
- Wall-clock time: `google.type.TimeOfDay`

Fields representing civil dates **should** have names ending in `_date`, while fields representing civil times or datetimes **should** have names ending in `_time`.

**Note:** Both the `Date` and `TimeOfDay` components are timezone-naïve. Fields that require timezone-awareness **should** use `DateTime` (see below).

##### Civil timestamps

Fields that represent a civil timestamp (date and time, optionally with a time zone) **should** use the `google.type.DateTime` component, and the field name **should** end in `_time`.

#### Compatibility

Occasionally, APIs are unable to use the common structures for legacy or compatibility reasons. For example, an API may conform to a separate specification that mandates that timestamps be integers or ISO-8601 strings.

In these situations, fields **may** use other types. If possible, the following naming conventions apply:

- For integers, include the meaning (examples: `time`, `duration`, `delay`, `latency`) **and** the unit of measurement (valid values: `seconds`, `millis`, `micros`, `nanos`) as a final suffix. For example, `send_time_millis`.
- For strings, include the meaning (examples: `time`, `duration`, `delay`, `latency`) but no unit suffix.

In all cases, clearly document the expected format, and the rationale for its use.

### 6.6 Standardized Codes (AIP-143)
[ref: #standardized-codes-aip-143]

Many common concepts, such as spoken languages, countries, currency, and so on, have common codes (usually formalized by the International Organization for Standardization) that are used in data communication and processing. These codes address the issue that there are often different ways to express the same concept in written language (for example, "United States" and "USA", or "Español" and "Spanish").

#### Guidance

For concepts where a standardized code exists and is in common use, fields representing these concepts **should** use the standardized code for both input and output.

```protobuf
// A message representing a book.
message Book {
  // Other fields...

  // The IETF BCP-47 language code representing the language in which
  // the book was originally written.
  // https://en.wikipedia.org/wiki/IETF_language_tag
  string language_code = 99;
}
```

- Fields representing standardized concepts **must** use the appropriate data type for the standard code (usually `string`).
  - Fields representing standardized concepts **should not** use enums, even if they only allow a small subset of possible values. Using enums in this situation often leads to frustrating lookup tables when using multiple APIs together.
  - Fields representing standardized concepts **must** indicate which standard they follow, preferably with a link (either to the standard itself, the Wikipedia description, or something similar).
- The field name **should** end in `_code` or `_type` unless the concept has an obviously clearer suffix.
- When accepting values provided by users, validation **should** be case-insensitive unless this would introduce ambiguity (for example, accept both `en-gb` and `en-GB`). When providing values to users, APIs **should** use the canonical case (in the example above, `en-GB`).

| Concept | Standard | Field Name |
|---------|----------|------------|
| Content/media type | IANA media types | `mime_type` |
| Country/region | Unicode CLDR region codes | `region_code` |
| Currency | ISO-4217 | `currency_code` |
| Language | IETF BCP-47 | `language_code` |
| Time zone | IANA TZ codes | `time_zone` |
| UTC offset | ISO-8601 format | `utc_offset` |

##### Content types

Fields representing a content or media type **must** use IANA media types. For legacy reasons, the field **should** be called `mime_type`.

##### Countries and regions

Fields representing individual countries or nations **must** use the Unicode CLDR region codes, such as `US` or `CH`, and the field **must** be called `region_code`.

**Important:** See the rationale below for why `region_code` is required instead of `country_code`.

##### Currency

Fields representing currency **must** use ISO-4217 currency codes, such as `USD` or `CHF`, and the field **must** be called `currency_code`.

**Note:** For representing an amount of money in a particular currency, rather than the currency code itself, use `google.type.Money`.

##### Language

Fields representing spoken languages **must** use IETF BCP-47 language codes, such as `en-US` or `de-CH`, and the field **must** be called `language_code`.

##### Time zones

Fields representing a time zone **should** use the IANA TZ codes, and the field **must** be called `time_zone`.

Fields also **may** represent a UTC offset rather than a time zone (note that these are subtly different). In this case, the field **must** use the ISO-8601 format to represent this, and the field **must** be named `utc_offset`.

#### Rationale

**Why `region_code` instead of `country_code`?**

The use of `region_code` instead of `country_code` is critical to being able to convey regions that are distinct from any country and to avoid any political disputes associated with said region regarding their sovereignty or affiliation. Furthermore, many of the values supported by Unicode CLDR are not countries on their own, so using a more generic name is actually more compatible with the specification.

### 6.7 Repeated Fields (AIP-144)
[ref: #repeated-fields-aip-144]

Representing lists of data in an API is trickier than it often appears. Users often need to modify lists in place, and longer data series within a single resource pose a challenge for pagination.

#### Guidance

Resources **may** use repeated fields where appropriate.

```protobuf
message Book {
  option (google.api.resource) = {
    type: "library.googleapis.com/Book"
    pattern: "publishers/{publisher}/books/{book}"
  };

  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  repeated string authors = 2;
}
```

- Repeated fields **must** use a plural field name.
  - If the English singular and plural words are identical ("moose", "info"), the dictionary word **must** be used rather than attempting to coin a new plural form.
- Repeated fields **should** have an enforced upper bound that will not cause a single resource payload to become too large. A good rule of thumb is 100 elements.
  - If repeated data has the chance of being too large, the API **should** use a sub-resource instead.
- Repeated fields **must not** represent the body of another resource inline. Instead, the message **should** provide the resource names of the associated resources.

##### Scalars and messages

Repeated fields **should** use a scalar type (such as `string`) if they are certain that additional data will not be needed in the future, as using a message type adds significant cognitive overhead and leads to more complicated code.

However, if additional data is likely to be needed in the future, repeated fields **should** use a message instead of a scalar proactively, to avoid parallel repeated fields.

##### Update strategies

A resource **may** use two strategies to enable updating a repeated field: direct update using the standard `Update` method, or custom `Add` and `Remove` methods.

A standard `Update` method has one key limitation: the user is only able to update _the entire_ list. Field masks are unable to address individual entries in a repeated field. This means that the user must read the resource, make modifications to the repeated field value as needed, and send it back. This is fine for many situations, particularly when the repeated field is expected to have a small size (fewer than 10 or so) and race conditions are not an issue, or can be guarded against with ETags.

**Note:** Declarative-friendly resources **must** use the standard `Update` method, and not introduce `Add` and `Remove` methods. If declarative tools need to reason about particular relationships while ignoring others, consider using a subresource instead.

If atomic modifications are required, the API **should** define custom methods using the verbs `Add` and `Remove`:

**Note:** If both of these strategies are too restrictive, consider using a subresource instead.

```protobuf
rpc AddAuthor(AddAuthorRequest) returns (Book) {
  option (google.api.http) = {
    post: "/v1/{book=publishers/*/books/*}:addAuthor"
    body: "*"
  };
}

rpc RemoveAuthor(RemoveAuthorRequest) returns (Book) {
  option (google.api.http) = {
    post: "/v1/{book=publishers/*/books/*}:removeAuthor"
    body: "*"
  };
}
```

- The data being added or removed **should** be a primitive (usually a `string`).
  - For more complex data structures with a primary key, the API **should** use a map with the `Update` method instead.
- The RPC's name **must** begin with the word `Add` or `Remove`. The remainder of the RPC name **should** be the singular form of the field being added.
- The request message **must** match the RPC name, with a `Request` suffix.
- The response message **should** be the resource itself, unless there is useful context to provide in the response, in which case the response message must match the RPC name, with a `Response` suffix.
  - When the response is the resource itself, it **should** include the fully-populated resource.
- The HTTP verb **must** be `POST`, as is usual for custom methods.
- The HTTP URI **must** end with `:add*` or `:remove*`, where `*` is the snake-case singular name of the field being added or removed.
- The request message field receiving the resource name **should** map to the URI path.
  - The HTTP variable **should** be the name of the resource (such as `book`) rather than `name` or `parent`.
  - That variable **should** be the only variable in the URI path.
- The body clause in the `google.api.http` annotation **should** be `"*"`.
- If the data being added in an `Add` RPC is already present, the method **must** error with `ALREADY_EXISTS`.
- If the data being removed in a `Remove` RPC is not present, the method **must** error with `NOT_FOUND`.

##### Request message

```protobuf
message AddAuthorRequest {
  // The name of the book to add an author to.
  string book = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference).type = "library.googleapis.com/Book"
  ];

  string author = 2 [(google.api.field_behavior) = REQUIRED];
}

message RemoveAuthorRequest {
  // The name of the book to remove an author from.
  string book = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference).type = "library.googleapis.com/Book"
  ];

  string author = 2 [(google.api.field_behavior) = REQUIRED];
}
```

- A resource field **must** be included. It **should** be the name of the resource (such as `book`) rather than `name` or `parent`.
  - The field **should** be annotated as required.
  - The field **should** identify the resource type that it references.
- A field for the value being added or removed **must** be included. It **should** be the singular name of the field.
  - The field **should** be annotated as required.
- The request message **must not** contain any other required fields, and **should not** contain other optional fields except those described in this or another AIP.

### 6.8 Ranges (AIP-145)
[ref: #ranges-aip-145]

Services often need to represent ranges of discrete or continuous values. These have wide differences in meaning, and come in many types: integers, floats, and timestamps, just to name a few, and the expected meaning of a range can vary in subtle ways depending on the type of range being discussed.

#### Guidance

A resource or message representing a range **should** ordinarily use two separate fields of the same type, with prefixes `start_` and `end_`:

```protobuf
// A representation of a chapter in a book.
message Chapter {
  string title = 1;

  // The page where this chapter begins.
  int32 start_page = 2;

  // The page where the next chapter or section begins.
  int32 end_page = 3;
}
```

##### Inclusive or exclusive ranges

Fields representing ranges **should** use inclusive start values and exclusive end values (half-closed intervals) in most situations; in interval notation: `[start_xxx, end_xxx)`.

Exclusive end values are preferable for the following reasons:

- It conforms to user expectations, particularly for continuous values such as timestamps, and avoids the need to express imprecise "limit values" (e.g. `2012-04-20T23:59:59`).
- It is consistent with most common programming languages, including C++, Java, Python, and Go.
- It is easier to reason about abutting ranges: `[0, x), [x, y), [y, z)`, where values are chainable from one range to the next.

##### Timestamp intervals

The `google.type.Interval` type represents a range between two timestamps, with an inclusive start value and exclusive end value.

Ranges between two timestamps which conform to the expectations of the `Interval` message **should** use this rather than having separate start and end fields. This allows client code to be written against the `Interval` message (such as checking whether a given timestamp occurs within the interval) and reused across multiple intervals in the same API, or even across multiple APIs.

APIs **may** use start and end timestamp fields instead. In particular, if a message within an API is inherently describing an interval with extra information about that interval, the additional level of nesting introduced by using the `Interval` message may be undesirable.

##### Exceptions

In some cases, there is significant colloquial precedent for inclusive start and end values (closed intervals), to the point that using an exclusive end value would be confusing even for people accustomed to them.

For example, when discussing dates (not to be confused with timestamps), most people use inclusive end: a conference with dates "April 21-23" is expected to run for three days: April 21, April 22, and April 23. This is also true for days of the week: a business that is open "Monday through Friday" is open, not closed, on Fridays.

In this situation, the prefixes `first` and `last` **should** be used instead:

```protobuf
// A representation of a chapter in a book.
message Chapter {
  string title = 1;

  // The first page of the chapter.
  int32 first_page = 2;

  // The last page of the chapter.
  int32 last_page = 3;
}
```

Fields representing ranges with significant colloquial precedent for inclusive start and end values **should** use inclusive end values with `first_` and `last_` prefixes for those ranges only. The service **should** still use exclusive end values for other ranges where this does not apply, and **must** clearly document each range as inclusive or exclusive.

### 6.9 Generic Fields (AIP-146)
[ref: #generic-fields-aip-146]

Most fields in any API, whether in a request, a resource, or a custom response, have a specific type or schema. This schema is part of the contract that developers write their code against.

However, occasionally it is appropriate to have a generic or polymorphic field of some kind that can conform to multiple schemata, or even be entirely free-form.

#### Guidance

While generic fields are generally rare, a service **may** introduce a generic field where necessary. There are several approaches to this depending on how generic the field needs to be; in general, services **should** attempt to introduce the "least generic" approach that is able to satisfy the use case.

##### Oneof

A `oneof` **may** be used to introduce a type union: the user or service is able to specify one of the fields inside the `oneof`. Additionally, a `oneof` **may** be used with the same type (usually strings) to represent a semantic difference between the options.

Because the individual fields in the `oneof` have different keys, a developer can programmatically determine which (if any) of the fields is populated.

A `oneof` preserves the largest degree of type safety and semantic meaning for each option, and services **should** generally prefer them over other generic or polymorphic options when feasible. However, the `oneof` construct is ill-suited when there is a large (or unlimited) number of potential options, or when there is a large resource structure that would require a long series of "cascading oneofs".

**Note:** Adding additional possible fields to an existing `oneof` is a non-breaking change, but moving existing fields into or out of a `oneof` is breaking (it creates a backwards-incompatible change in Go protobuf stubs).

##### Maps

Maps **may** be used in situations where many values _of the same type_ are needed, but the keys are unknown or user-determined.

Maps are usually not appropriate for generic fields because the map values all share a type, but occasionally they are useful. In particular, a map can sometimes be suited to a situation where many objects of the same type are needed, with different behavior based on the names of their keys (for example, using keys as environment names).

##### Struct

The `google.protobuf.Struct` object **may** be used to represent arbitrary nested JSON. Keys can be strings, and values can be floats, strings, booleans, arrays, or additional nested structs, allowing for an arbitrarily nested structure that can be represented as JSON (and is automatically represented as JSON when using REST/JSON).

A `Struct` is most useful when the service does not know the schema in advance, or when a service needs to store and retrieve arbitrary but structured user data. Using a `Struct` is convenient for users in this case because they can easily get JSON objects that can be natively manipulated in their environment of choice.

If a service needs to reason about the _schema_ of a `Struct`, it **should** use JSONSchema for this purpose. Because JSONSchema is itself JSON, a valid JSONSchema document can itself be stored in a `Struct`.

##### Any

The `google.protobuf.Any` object can be used to send an arbitrary serialized protocol buffer and a type definition.

However, this introduces complexity, because an `Any` becomes useless for any task other than blind data propagation if the consumer does not have access to the proto. Additionally, even if the consumer _does_ have the proto, the consumer has to ensure the type is registered and then deserialize manually, which is an often-unfamiliar process.

Because of this, `Any` **should not** be used unless other options are infeasible.

### 6.10 Sensitive Fields (AIP-147)
[ref: #sensitive-fields-aip-147]

Sometimes APIs need to collect sensitive information such as private encryption keys meant to be _stored_ by the underlying service but not intended to be _read_ after writing due to the sensitive nature of the data. For this type of data, extra consideration is required for the representation of the sensitive data in API requests and responses.

#### Guidance

##### Required sensitive data

If the sensitive information is _required_ for the resource as a whole to exist, the data **should** be accepted as an input-only field with no corresponding output field. Because the sensitive data must be present for the resource to exist, users of the API may assume that existence of the resource implies storage of the sensitive data.

```protobuf
message SelfManagedKeypair {
  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  // The public key data in PEM-encoded form.
  bytes public_key = 2;

  // The private key data in PEM-encoded form.
  bytes private_key = 3 [
    (google.api.field_behavior) = INPUT_ONLY];
}
```

##### Optional sensitive data

If the sensitive information is _optional_ within the containing resource, an output-only boolean field with a postfix of `_set` **should** be used to indicate whether or not the sensitive information is present.

```protobuf
message Integration {
  string name = 1 [(google.api.field_behavior) = IDENTIFIER];
  string uri = 2;

  // A secret to be passed in the `Authorization` header of the webhook.
  string shared_secret = 3 [
    (google.api.field_behavior) = INPUT_ONLY];

  // True if a `shared_secret` has been set for this Integration.
  bool shared_secret_set = 4 [
    (google.api.field_behavior) = OUTPUT_ONLY];
}
```

##### Obfuscated sensitive data

If it is important to be able to identify the sensitive information without allowing it to be read back entirely, a field of the same type with an `obfuscated_` prefix **may** be used instead of the boolean `_set` field to provide contextual information about the sensitive information. The specific nature of the obfuscation is outside the scope of this AIP.

```protobuf
message AccountRecoverySettings {
  // An email to use for account recovery.
  string email = 1 [
    (google.api.field_behavior) = INPUT_ONLY];

  // An obfuscated representation of the recovery email. For example,
  // `ada@example.com` might be represented as `a**@e*****e.com`.
  string obfuscated_email = 2 [
    (google.api.field_behavior) = OUTPUT_ONLY];
}
```

### 6.11 Standard Fields (AIP-148)
[ref: #standard-fields-aip-148]

Certain concepts are common throughout any corpus of APIs. In these situations, it is useful to have a standard field name and behavior that is used consistently to communicate that concept.

#### Guidance

Standard fields **should** be used to describe their corresponding concept, and **should not** be used for any other purpose.

##### Resource names and IDs

**name**

Every resource **must** have a `string name` field, used for the resource name (AIP-122), which **should** be the first field in the resource.

**Note:** The `_name` suffix **should not** be used to describe other types of names unless otherwise covered in this AIP.

**parent**

The `string parent` field refers to the resource name of the parent of a collection, and **should** be used in most `List` (AIP-132) and `Create` (AIP-133) requests.

##### Other names

**display_name**

The `string display_name` field **must** be a mutable, user-settable field where the user can provide a human-readable name to be used in user interfaces. Declarative-friendly resources **should** include this field.

Display names **should not** have uniqueness requirements, and **should** be limited to <= 63 characters.

**title**

The `string title` field **should** be the official name of an entity, such as a company's name. This is a more formal variant of `display_name`.

**given_name**

The `string given_name` field **must** refer to a human or animal's given name. Resources **must not** use `first_name` for this concept, because the given name is not placed first in many cultures.

**family_name**

The `string family_name` field **must** refer to a human or animal's family name. Resources **must not** use `last_name` for this concept, because the family name is not placed last in many cultures.

##### Timestamps

**create_time**

The output only `google.protobuf.Timestamp create_time` field **must** represent the timestamp when the resource was created. This **may** be either the time creation was initiated or the time it was completed. Declarative-friendly resources **should** include this field.

**update_time**

The output only `google.protobuf.Timestamp update_time` field **must** represent the timestamp when the resource was most recently updated. Any change to the resource made by users **must** refresh this value; changes to a resource made internally by the service **may** refresh this value. Declarative-friendly resources **should** include this field.

**delete_time**

The output only `google.protobuf.Timestamp delete_time` field **must** represent the timestamp that a resource was soft deleted. This **may** correspond to either the time when the user requested deletion, or when the service successfully soft deleted the resource. If a resource is not soft deleted, the `delete_time` field **must** be empty.

Resources that support soft delete (AIP-164) **should** provide this field.

**expire_time**

The `google.protobuf.Timestamp expire_time` field **should** represent the time that a given resource or resource attribute is no longer useful or valid (e.g. a rotating security key). It **may** be used for similar forms of expiration as described in AIP-214.

Services **may** provide an `expire_time` value that is inexact, but the resource **must not** expire before that time.

**purge_time**

The `google.protobuf.Timestamp purge_time` field **should** represent the time when a soft deleted resource will be purged from the system (see AIP-164). It **may** be used for similar forms of expiration as described in AIP-214. Resources that support soft delete **should** include this field.

Services **may** provide a `purge_time` value that is inexact, but the resource **must not** be purged from the system before that time.

##### Annotations

To store small amounts of arbitrary data, a `map<string, string> annotations` field **may** be added.

The `annotations` field **must** use the Kubernetes limits to maintain wire compatibility, and **should** require dot-namespaced annotation keys to prevent tools from trampling over one another.

Examples of information that might be valuable to store in annotations include:

- For CI/CD, an identifier of the pipeline run or version control identifier used to propagate.

**Note:** Annotations are distinct from various forms of labels. Labels can be used by server-side policies, such as IAM conditions. Annotations exist to allow client tools to store their own state information without requiring a database.

##### Well known string fields

**IP address**

A field that represents an IP address **must** comply with the following:

- Use type `string`.
- Use the name `ip_address` or end with the suffix `_ip_address` (e.g. `resolved_ip_address`).
- Specify the IP address version format via one of the supported formats `IPV4`, `IPV6`, or if it can be either, `IPV4_OR_IPV6` (see AIP-202).

**uid**

The output only `string uid` field refers to a system-assigned unique identifier for a resource. When provided, this field **must** be a UUID4 and **must** specify this format via the `UUID4` format extension (see AIP-202). Declarative-friendly resources **should** include this field.

#### Further reading

- For standardized codes, see AIP-143.
- For the `etag` field, see AIP-154.
- For the `request_id` field, see AIP-155.
- For the `filter` field, see AIP-160.
- For fields related to resource revisions, see AIP-162.
- For the `validate_only` field, see AIP-163.
- For fields related to soft delete and undelete, see AIP-164.

#### Rationale

**Why well known string fields?**

Some fields represent very well defined concepts or artifacts that sometimes also have strict governance of their semantics. For such fields, presenting an equally standardized API surface is important. This enables development of improved API consumer tools and documentation, as well as a more unified user experience across the platform.

#### History

Before 2023-07, `purge_time` for soft-deleted resources was also called `expire_time`. `purge_time` was introduced to reduce user confusion.

### 6.12 Unset Field Values (AIP-149)
[ref: #unset-field-values-aip-149]

In many messages, many fields are optional: the user is not required to provide them, or for output fields, the service might not populate the field.

In most cases, there is no meaningful difference between setting it to a default value (such as `0`) as opposed to not setting it at all; however, occasionally this distinction is meaningful.

#### Guidance

Services defined in protocol buffers **should** use the `optional` keyword for primitives if and only if it is necessary to distinguish setting the field to its default value (`0`, `false`, or empty string) from not setting it at all:

```protobuf
// A representation of a book in a library.
message Book {
  option (google.api.resource) = {
    type: "library.googleapis.com/Book"
    pattern: "publishers/{publisher}/books/{book}"
  };

  // The name of the book.
  string name = 1 [(google.api.field_behavior) = IDENTIFIER];

  // The rating for the book, from 0 to 5.
  // 0 is distinct from no rating.
  optional int32 rating = 2;
}
```

**Important:** Services **should not** need to distinguish between the default value and unset most of the time; if an alternative design does not require such a distinction, it is usually preferred. In practice, this means `optional` **should** only ever be used for integers and floats.

**Important:** Tracking field presence is _not_ the same as documenting API field behavior as defined in AIP-203. For example, a field labeled with `optional` for presence tracking **may** also be annotated as `google.api.field_behavior = REQUIRED` if the field must be set. If you only want to document the server perceived behavior of a field, read AIP-203.

#### Backwards compatibility

It is a backwards incompatible change to add or remove the `optional` qualifier to an existing field. This is because the compiled API is changed (in some languages). For example, in Golang, adding `optional` changes the field type of primitives to be the pointer variant of their original type, e.g. a field formerly of type `string` becomes `*string`, etc. Accordingly, this change requires that both clients and servers update their usage of the changed field in unison, which is risky and error prone. Additional information is documented by Protobuf.

#### Rationale

**Field behavior and `optional`**

The field behavior annotation and `optional` label are not mutually exclusive, because they address different problems. The former, `google.api.field_behavior`, focuses on communicating the server's perception of a field within the API (e.g. if it is required or not, if it is immutable, etc.). The latter, proto3's `optional`, is a wire format and code generation option that is strictly for toggling field presence tracking. While it might be confusing for a field to be simultaneously annotated with `google.api.field_behavior = REQUIRED` and labeled as `optional`, they are unrelated in practice and can reasonably be used together.

### 6.13 States (AIP-216)
[ref: #states-aip-216]

Many API resources carry a concept of "state": ordinarily, the resource's place in its life cycle. For example, a virtual machine may be being provisioned, available for use, being spun down, or potentially be in one of several other situations. A job or query may be preparing to run, be actively running, have completed, and so on.

#### Guidance

Resources needing to communicate their state **should** use an enum, which **should** be called `State` (or, if more specificity is required, end in the word `State`). This enum **should** be nested within the message it describes when only used as a field within that message.

**Important:** We use the term `State`, and _not_ `Status` (which is reserved for the HTTP and gRPC statuses).

##### Enum values

Ideally, APIs use the same terminology throughout when expressing the same semantic concepts. There are usually many words available to express a given state, but customers often use multiple APIs together, and it is easier for them when terms are consistent.

At a high level:

- Resources that are available for use are `ACTIVE` (preferred over terms such as "ready" or "available").
- Resources that have completed a (usually terminal) requested action use past participles (usually ending in `-ED`), such as `SUCCEEDED` (not "successful"), `FAILED` (not "failure"), `DELETED`, `SUSPENDED`, and so on.
- Resources that are currently undergoing a state change use present participles (usually ending in `-ING`), such as `RUNNING`, `CREATING`, `DELETING`, and so on. In this case, it is expected that the state is temporary and will resolve to another state on its own, with no further user action.

**Note:** Remember to only add states that are useful to customers. Exposing a large number of states simply because they exist in your internal system is unnecessary and adds confusion for customers. Each state must come with a use case for why it is necessary.

##### Output only

The field referencing the `State` enum in a resource **should** behave and be documented as "Output only", in accordance with AIP-203.

APIs **should not** allow a `State` enum to be directly updated through an "update" method (or directly set through the "create" method), and **should** instead use custom state transition methods.

This is because update methods are generally not expected to have side effects, and also because updating state directly implies that it is possible to set the state to any available value, whereas states generally reflect a resource's progression through a lifecycle.

##### State transition methods

State transition methods are a special type of custom method that are responsible for transitioning a state field from one enum value to another. As part of the transition, other fields may also change, e.g. an `update_time` field. The method definition should look like the following:

```protobuf
// Publishes a book.
// The `state` of the book after publishing is `PUBLISHED`.
// `PublishBook` can be called on Books in the state `DRAFT`; Books in a
// different state (including `PUBLISHED`) returns an error.
rpc PublishBook(PublishBookRequest) returns (Book) {
  option (google.api.http) = {
    post: "/v1/{name=publishers/*/books/*}:publish"
    body: "*"
  };
}
```

- The name of the method **should** be a verb followed by the singular form of the resource's message name.
- The request message **must** match the RPC name, with a `Request` suffix.
- The response message **should** be the resource itself.
  - If the RPC is long-running, the response message **should** be a `google.longrunning.Operation` which resolves to the resource itself.
- The HTTP verb **must** be `POST`.
- The HTTP URI **must** use a `:` character followed by the custom verb (`:publish` in the above example), and the verb in the URI **must** match the verb in the name of the RPC.
  - If word separation is required, `camelCase` **must** be used.
- The `body` clause in the `google.api.http` annotation **must** be `"*"`.
- The request message field receiving the resource name **should** map to the URI path.
  - This field **should** be called `name`.
  - The `name` field **should** be the only variable in the URI path. All remaining parameters **should** map to URI query parameters.
- If the state transition is not allowed, the service **must** error with `FAILED_PRECONDITION` (HTTP 400).

The request message should look like this:

```protobuf
message PublishBookRequest {
  // The name of the book to publish.
  // Format: publishers/{publisher}/books/{book}
  string name = 1 [
    (google.api.field_behavior) = REQUIRED,
    (google.api.resource_reference) = {
      type: "library.googleapis.com/Book"
    }];
}
```

- A resource name field **must** be included. It **should** be called `name`.
- The comment for the field **should** document the resource pattern.
- Other fields **may** be included.

#### Additional guidance

##### Default value

The zero value of each state enum **should** adhere to the following convention:

```protobuf
enum State {
  // The default value. This value is used if the state is omitted.
  STATE_UNSPECIFIED = 0;

  // Other values...
}
```

Resources **should not** provide an unspecified state to users, and this value **should not** actually be used.

##### Value uniqueness

Multiple top-level enums within the same package **must** not share the same values. This is because the C++ protoc code generator flattens top-level enum values into a single namespace.

State enums **should** live inside the resource definition.

##### Prefixes

Using a `STATE_` prefix on every enum value is unnecessary. State enum values **should not** be prefixed with the enum name, except for the default value `STATE_UNSPECIFIED`.

##### Breaking changes

Even though adding states to an existing states enum _can_ break existing user code, adding states is not considered a breaking change. Consider a state with only two values: `ACTIVE` and `DELETED`. A user may add code that checks `if state == ACTIVE`, and in the else cases simply assumes the resource is deleted. If the API later adds a new state for another purpose, that code will break.

We ultimately can not control this behavior, but API documentation **should** actively encourage users to code against state enums with the expectation that they may receive new values in the future.

APIs **may** add new states to an existing State enum when appropriate, and adding a new state is _not_ considered a breaking change.

##### When to avoid states

Sometimes, a `State` enum may not be what is best for your API, particularly in situations where a state has a very small number of potential values, or when states are not mutually exclusive.

Consider the example of a state with only `ACTIVE` and `DELETED`, as discussed above. In this situation, the API may be better off exposing a `google.protobuf.Timestamp delete_time`, and instructing users to rely on whether it is set to determine deletion.

##### Common states

The following is a list of states in common use. APIs **should** consider prior art when determining state names, and **should** value local consistency above global consistency in the case of conflicting precedent.

**Resting states**

"Resting states" are lifecycle states that, absent user action, are expected to remain indefinitely. However, the user can initiate an action to move a resource in a resting state into certain other states (resting or active).

- `ACCEPTED`
- `ACTIVE`
- `CANCELLED`
- `DELETED`
- `FAILED`
- `SUCCEEDED`
- `SUSPENDED`
- `VERIFIED`

**Active states**

"Active states" are lifecycle states that typically resolve on their own into a single expected resting state.

**Note:** Remember only to expose states that are useful to customers. Active states are valuable only if the resource will be in that state for a sufficient period of time. If state changes are immediate, active states are not necessary.

- `CREATING` (usually becomes `ACTIVE`)
- `DELETING` (usually becomes `DELETED`)
- `PENDING` (usually becomes `RUNNING`)
- `REPAIRING` (usually becomes `ACTIVE`)
- `RUNNING` (usually becomes `SUCCEEDED`)
- `SUSPENDING` (usually becomes `SUSPENDED`)

#### Further reading

- For information on enums generally, see AIP-126.
