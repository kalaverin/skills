## 2. Process — Design Review and Launch Stages

### 2.1 API Design Review FAQ (AIP-100)
[ref: #api-design-review-faq-aip-100]

API design review ensures a **simple**, **intuitive**, and **consistent** API experience across the entire API corpus.

#### Do I need API design approval?

**TL;DR:** You usually need API design approval if you are launching an API that users can code against (either now or in the future) at the beta or GA quality level.

API design review is fundamentally about ensuring a simple and consistent experience for users, and therefore is only expected for APIs that users code directly against.

**Decision flowchart:**

1. **Who should code directly against this API?**
   - **General public** → requires review at beta/GA.
   - **Partners only**:
     - Forever partners only → review **recommended**.
     - Will eventually be public → requires review at beta/GA.
   - **Googlers/internal tools only** → review **not required**.
   - **Anyone** (public or eventual) → evaluate release level.

2. **What release level?**
   - **Alpha** → review **optional but recommended**. Alpha may launch without approval **if** limited to a known user set. Warning: alpha without review **does not** enshrine decisions; review is **mandatory** for beta promotion.
   - **Beta** → review **required** ⚠️.
   - **GA** → evaluate changes from beta:
     - Any changes from beta? → review **required**.
     - No changes? → **FYI** only.

**Who should code directly against it?**

Design review is expected if the general public is intended to read documentation and write code that interacts with the service. The following situations **do not** require design review:

- An API which will only ever be used by internal teams or internal tools.
- An API which will only ever be called by an executable program released by the producer (even if the API could be reverse-engineered from the executable).
- An API which will only ever be called by a single customer or small set of customers under contract, and which will **never** be made more widely available. (Design review is still **recommended** in this case, but not required.)

#### Why is design review important?

**TL;DR:** Product excellence.

The design review process exists to ensure that APIs presented to customers are **simple**, **intuitive**, and **consistent**. The reviewer approaches the API from the standpoint of a naïve user, thinks through the resources and actions, and attempts to make the surface as accessible and extensible as possible.

The reviewer also checks consistency with the existing corpus of APIs. Many customers use multiple APIs; conventions and naming choices must line up with customer expectations.

#### What should I expect?

**How long does the review process take?**

Reviewers endeavor to offer feedback frequently, but begin the process early to avoid delays:

- Incremental changes to existing APIs: a few days.
- Small APIs: around a week.
- Entirely new APIs with large surfaces: no less than a week; extraordinarily large surfaces may take a month or more.

**How do reviewers approach my API?**

Reviewers focus primarily on the API surface and its user-facing documentation. They ask the types of design questions that users will ask, and nudge the API toward raising fewer of those questions.

**What is precedent?**

Precedent means decisions already made by previous APIs, which generally should be binding upon newer APIs in similar situations. The most common example is **naming**: standard fields dictate how common terms like `name`, `create_time` are used, always attaching the same name to the same concept.

Precedent also applies to **patterns**: pagination, long-running operations, import/export, etc. Once a pattern is established, implement it the same way wherever germane. The goal: once customers learn their first API, the second (and third) should be easier because patterns are consistent.

#### What should I do?

**...if I have a launch on a tight deadline?**

Engage design review as early as possible. Make reviewers aware of your timeline.

For time-sensitive **alpha** launches, an API **may** launch without design review approval, limited to a known set of users. Reviewers will provide notes for consideration at subsequent stages. **Warning:** Launching alpha with incomplete review **does not** enshrine decisions. Beta launch **will** be blocked if issues exist.

For launch stages after alpha, design review is mandatory. In rare cases where product excellence conflicts with engineering effort or deadlines, a director or VP must make an explicit choice to bypass review or disregard feedback.

**...to make my review go faster?**

- Begin API review as early as possible, and follow up frequently.
- Run the API linter beforehand. (If disabling the linter at any point, explain why.)
- Ensure every message, RPC, and field is **usefully** commented. Comments must be in valid American English and say something meaningful.
- If a reviewer asks for an explanation, add the explanation **in the proto comments**, not the review conversation. This saves round trips.

**...if one of my API reviewers is unresponsive?**

Reach out to the reviewer directly. If that fails, reach out to the other reviewer, who will coordinate. If that fails also, escalate according to AIP-1.

**...if I have a design question?**

Consult the API style guide, the AIP index, and other public APIs within the organization. Other public APIs are particularly valuable; someone has likely encountered a similar situation.

**...if I have a question not covered there?**

Reach out to the API design team with your question. This works best when seeking guidance on a specific design question with a clearly explained use case and examples. Be patient — reviewers are almost exclusively volunteers.

**...if a question is complex and languishing in a review?**

Schedule a meeting with reviewers. Most issues can be discussed in 30 minutes. Document what is discussed in the review so history is preserved.

**...if my API needs to violate a standard?**

Clearly document (using an internal comment in the proto) that you are violating an API design guideline and your rationale. The comment **must** be prefixed with `aip.dev/not-precedent`.

The rationale **should** be in accordance with one of the enumerated reasons in AIP-200. If not, work with your reviewer to determine the right course of action.

**...if a reviewer is bringing up a previously-settled issue?**

Reference the code review where the issue was decided. Reviewers usually give deference to previous reviews to avoid churn. If the reviewer believes the previous reviewer made a significant mistake, work together to determine the best course of action.

**...if the team and the reviewers strongly disagree?**

Escalate according to AIP-1.

#### Does my PA or team have any particular guidelines?

Some teams (e.g., Cloud PA, machine learning) have specific guidelines and their own reviewer pools to ensure additional uniformity. These guidelines are published as AIPs; higher AIP numbers are reserved for PA and team use (see AIP-2).

### 2.2 Beta-Blocking Changes (AIP-205)
[ref: #beta-blocking-changes-aip-205]

APIs often release an Alpha version in order to get early feedback from customers. This API is provisional and can change many times before the important feedback is incorporated and the API is made stable for Beta.

Since the purpose of Alpha is to gather feedback, the API does not need to be perfect yet, and it is not strictly necessary for API authors to address every usability concern or every point in the API standards. Often, API authors and API reviewers will not agree on the best design, and the best way to find out is by having users try out the API.

However, once the feedback has been collected and the API is going to be promoted to Beta, usability concerns and style issues **must** be addressed. In order to ensure that these issues are not forgotten, they **must** be explicitly documented in the API.

#### Guidance

If an API has usability concerns or violates API standards, and the present design should receive additional scrutiny before being carried through to the Beta version, there **must** be an internal comment linking to this document using its descriptive link (`aip.dev/beta-blocker`) to ensure that the design is corrected before the API is released to Beta.

The comment **must** also indicate what kind of change should be made for Beta.

If an exception to API standards **does** need to be carried through to Beta and GA, see AIP-200 (`aip.dev/not-precedent`).

#### Writing effective beta-blocker comments

A beta-blocker comment **must** be specific and actionable. Vague comments such as "fix this later" or "improve before Beta" are insufficient.

Good beta-blocker comments include:
- The specific change required (e.g., "Rename to...", "Convert to...", "Refactor into...").
- The reason the change is necessary, if not obvious.
- A reference to the relevant AIP or standard being violated, if applicable.

#### Examples

**Beta-blocker comment on a field:**

```protobuf
message InputConfig {
  // Parameters for input.
  // (-- aip.dev/beta-blocker: Convert well-known parameters into explicit
  //     fields before the Beta launch. --)
  map<string, string> parameters = 1;
}
```

**Beta-blocker comment on a message:**

```protobuf
// (-- aip.dev/beta-blocker: Rename this message to GetOrderRequest before
//     the Beta launch to match the method name. --)
message GetOrderReq {
  string name = 1;
}
```

**Beta-blocker comment on a method:**

```protobuf
// (-- aip.dev/beta-blocker: Refactor this into a standard List method before
//     the Beta launch. --)
rpc SearchOrders(SearchOrdersRequest) returns (SearchOrdersResponse);
```

#### Rationale

Without explicit beta-blocker comments, teams often deprioritize style and usability fixes during Alpha, intending to address them later. When launch pressure increases near the Beta date, these issues are frequently forgotten or deliberately skipped, permanently degrading the API surface. Beta-blocker comments create an auditable, in-code record that blocks promotion until resolved.

#### Relationship to other AIPs

Beta-blocker comments **must not** be used to permanently grant exceptions to API standards. If a design intentionally violates a standard and that violation is intended to persist through Beta and GA, the comment **must** use `aip.dev/not-precedent` instead, following the process described in AIP-200.

Beta-blocker comments are intended for temporary exceptions that **will** be resolved before Beta. They are not a mechanism for avoiding standards indefinitely.

#### Further reading

- [AIP-200](01_foundation_and_process.md#precedent-and-standards-exceptions-aip-200) — Precedent and Standards Exceptions
- [AIP-181](08_compatibility_and_versioning.md#stability-levels-aip-181) — Stability Levels
