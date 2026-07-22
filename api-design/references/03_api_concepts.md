---
subject: "Management and data plane taxonomy from `AIP-111`; provisioning configure audit lifecycle, uniform resource-oriented interface, user data operations, throughput latency availability, consistency tradeoffs, blast radius, declarative clients Terraform exclusivity, plane determination heuristics, management-plane contract, `AIP-131..135` standard methods, `AIP-128` declarative-friendly."
index:
  - anchor: planes-aip-111
    what: "The AIP-111 plane taxonomy: management resources provision, configure, and audit infrastructure via uniform resource-oriented APIs, while data methods operate on user content, plus heuristics for assigning any resource or method to its plane."
    problem: "Designer mixes configuration lifecycle with user-content operations inside one surface, so uniform tooling breaks and awkward resource-oriented wrappers throttle high-throughput paths; plane classification, provisioning versus content, infrastructure prerequisite, critical path latency, mixed taxonomy confusion, scope creep, declarative boundary."
    use_when: "Deciding whether new resource belongs with provisioning APIs; splitting one service into two surfaces; checking if method qualifies as uniform standard-method target; evaluating whether IaC tools will manage the element."
    avoid_when: "Control or power planes from networking architecture sought (out of AIP scope); cross-references to standard methods needed directly (05_operations › standard methods); plane already evident and only field-level naming guidance wanted."
    expected: "Every resource and method carries explicit plane assignment, configuration lives behind uniform resource-oriented surface, and user-content operations stay free of provisioning constraints."
  - anchor: planes-aip-111
    what: "The AIP-111 distinctions table: management planes favor uniformity and consistency with system-wide failure impact and exclusive declarative-client access, data planes favor throughput, availability, and low latency, and data resources exposed via management APIs must satisfy the management-plane contract (`AIP-131..135`, `AIP-128`)."
    problem: "Team exposes queue or table rows through strict standard-method interface expecting Terraform support, so imperative stateful traffic fights declarative reconciliation and consistency guarantees silently weaken; tooling fit mismatch, desired state drift, reconciliation conflict, availability consistency tradeoff, blast radius scope, throughput latency pressure, exposed resource contract."
    use_when: "Choosing between strict consistency and uptime for new API; deciding whether Terraform or Kubernetes controllers should manage element; setting performance budget for user-facing path; exposing data resource through management surface and needing its obligations."
    avoid_when: "Plane of element still undetermined (sibling card); pure throughput tuning with no tooling or consistency question; networking control-plane concepts expected."
    expected: "Design states consistency-versus-availability priority explicitly, declarative tooling targets only provisioning APIs, and every such published element satisfies standard methods plus declarative-friendliness."
aips: [111]
---

# API Concepts

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

> **Agent extension — not part of the AIP standard.** The plane distinction drives concrete design choices. Management-plane APIs are the exclusive domain of declarative clients (Terraform, Kubernetes controllers): those clients reconcile desired state, so management resources need predictable standard methods and robust user-specified IDs, and the plane favors consistency over availability — a failed operation is better than an inconsistent or insecure configuration; its blast radius is system-wide. Data-plane APIs optimize for throughput, availability, and low latency with resource-scoped blast radius and fall outside declarative tooling. If data-plane resources are exposed through a management API, they must still satisfy the management-plane contract (standard methods AIP-131..135, declarative-friendliness per AIP-128).
