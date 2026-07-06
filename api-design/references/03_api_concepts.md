## 3. API Concepts

### 3.1 Planes (AIP-111)
[ref: #planes-aip-111]

Resources and methods on an API can be divided into the **plane** that they reside on or perform operations upon.

The term "plane" originates from networking architecture. Although system and network architecture often defines additional planes (e.g., control plane or power planes), as the AIPs are focused on the interface, they are not defined here.

#### Guidance

##### Management Plane

Management resources and methods exist primarily to **provision**, **configure**, and **audit** the resources that the data plane interfaces with.

Management plane APIs are uniform and resource-oriented. They provide a consistent interface for creating, updating, retrieving, and deleting resources.

**Examples of management resources:**
- virtual machines
- virtual private networks
- virtual disks
- blob store instances
- projects or accounts

##### Data Plane

Methods on the data plane operate on **user data** in a variety of data formats, and generally interface with a resource provisioned via a management plane API.

**Examples of data plane operations:**
- writing and reading rows in a table
- pushing to or pulling from a message queue
- uploading blobs to or downloading blobs from a blob store instance

Data plane APIs **may** be heterogeneous across a larger API surface, due to requirements including high throughput, low latency, or the need to adhere to an existing interface specification (e.g., ANSI SQL).

For convenience, resources and methods that operate on the data plane **may** expose themselves via resource-oriented management APIs. If so, those resources and methods **must** adhere to the requirements of the management plane as specified in the other AIPs (AIP-131 through AIP-135).

#### Major Distinctions Between Management and Data Planes

The following distinctions govern how each plane is designed, operated, and consumed:

- **Declarative clients operate on the management plane exclusively.** Tools such as Terraform, infrastructure-as-code systems, and configuration management agents interact only with management plane APIs. Data plane operations are imperative and stateful; they cannot be managed declaratively.

- **Data planes are often on the critical path of user-facing functionality**, and therefore:
  - Have **higher availability requirements** than management planes.
  - Are **more performance-sensitive** than management planes.
  - Require **higher throughput** than management planes.

- **Management planes prioritize uniformity and consistency** over raw performance. The same user should be able to interact with virtual machines, networks, and storage using identical patterns (standard methods, consistent field naming, uniform pagination).

- **Data planes may sacrifice uniformity for performance.** When low latency or high throughput is required, the API may use custom methods, streaming, binary protocols, or non-standard interfaces (e.g., SQL over gRPC).

#### Determining the Plane of a Resource or Method

When designing an API, use the following heuristics to determine which plane a resource or method belongs to:

- If the resource represents **infrastructure or configuration** that must exist before user data can be processed → **management plane**.
- If the method operates on **user-generated content or transactional data** → **data plane**.
- If the resource is managed by **IaC tools or declarative clients** → **management plane**.
- If the operation is on the **critical path of user-facing latency** → **data plane**.

A single service often exposes **both** planes. For example, a database service may have a management plane API to create and configure database instances, and a separate data plane API to execute queries against those instances.

#### Rationale

The plane distinction exists because the design constraints and operational requirements of configuration APIs and data APIs are fundamentally different. Attempting to force a high-throughput data operation into the strict resource-oriented constraints of the management plane results in poor performance and awkward interfaces. Conversely, allowing management resources to bypass standard patterns creates inconsistency across the API corpus and breaks declarative tooling.

Explicitly classifying every resource and method by plane prevents scope creep, guides technology choices (e.g., caching, load balancing, rate limiting), and ensures that the correct reliability and performance guarantees are applied.

#### Further reading

- [AIP-121](04_resource_design.md#resource-oriented-design-aip-121) — Resource-Oriented Design
- [AIP-131](05_operations.md#standard-method-get-aip-131) through [AIP-135](05_operations.md#standard-method-delete-aip-135) — Standard Methods
- [AIP-128](04_resource_design.md#declarative-friendly-interfaces-aip-128) — Declarative-Friendly Interfaces
