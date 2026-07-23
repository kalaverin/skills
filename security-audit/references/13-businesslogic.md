---
subject: "Business logic vulnerability detection reference for SAST subagents: OWASP API6 mapping, CWE table, definition and exclusions, 13 attack categories, dynamic scenario generation, per-stack vulnerable/secure recipes incl. FastAPI, prevention guidance, compensating-controls detection, three-phase execution."
index:
  - anchor: businesslogic-detection
    what: "Focused business-logic detection role using the three-phase subagent approach — domain recon, batched scenario verify, merge — gated on the architecture report."
    problem: "Codebase needs systematic sweep of every money, entitlement, and state flow for rule enforcement, yet unstructured hunting misses logic gaps and drowns reviewers in unverified scenarios; detection orchestration, phase pipeline, verified findings, audit rigor, methodical triage, candidate flood, coverage goal."
    use_when: "Business-logic scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-phase detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual knowledge is needed, not execution."
    expected: "Verified logic findings consolidated into the module report with false positives filtered."
  - anchor: businesslogic-owasp-mapping
    what: "OWASP API6:2023 Unrestricted Access to Sensitive Business Flows mapping with ratings, flow examples, and anti-automation context."
    problem: "Findings need correct 2023-era taxonomy for reporting, and confusing logic abuse with implementation bugs mislabels everything downstream; taxonomy mapping, risk routing, classification accuracy, edition awareness, correct tagging, traceability, api6, risk labels."
    use_when: "Tagging findings with OWASP 2023 risks; writing the report's risk section."
    avoid_when: "CWE-level tagging is the question — see the CWE anchor."
    expected: "Findings mapped to API6 with explicit flow-abuse reasoning."
  - anchor: businesslogic-cwe-mapping
    what: "CWE table per logic weakness: improper enforcement of business rules, race conditions, insufficient verification, price manipulation."
    problem: "Wrong CWE assignment breaks downstream tooling and metrics, especially when concurrency and workflow classes blur together; weakness taxonomy, cwe 840, cwe 367, misclassification risk, tooling accuracy, identifier precision, reporting feeds, scanner alignment."
    use_when: "Assigning CWE identifiers to findings."
    avoid_when: "OWASP risk framing is the question — see the OWASP anchor."
    expected: "Each finding carries the most specific CWE identifier."
  - anchor: businesslogic-definition
    what: "Core definition: attackers abusing legitimate functionality — valid requests that violate business rules the code never enforces."
    problem: "Reviewers disagree on what counts as logic vulnerability without shared frame, so design-intended flows get flagged while real rule gaps slip; concept baseline, shared vocabulary, classification consistency, definition anchor, rule enforcement, intended use, term alignment."
    use_when: "Onboarding to the scan; deciding whether a behavior belongs to logic findings at all."
    avoid_when: "Attack categories are needed — jump to the categories anchor; execution workflow is the question."
    expected: "Everyone applies one definition: valid requests breaking unenforced business rules."
  - anchor: businesslogic-attack-categories
    what: "Thirteen attack categories: price/payment, quantity limits, workflow bypass, coupon abuse, race conditions, refunds, referrals, entitlements, auctions, inventory, time logic, transfers, automated flow abuse."
    problem: "Detectors under-report when abuse categories stay implicit, missing concurrency, entitlement, and automation paths across domains and stacks; inclusion rules, category inventory, missed flows, hidden vectors, recon breadth, scenario coverage, domain gaps."
    use_when: "Generating attack scenarios in recon; checking whether a flow type was considered."
    avoid_when: "Boundary rules are the question — see the definition anchor; prevention guidance wanted."
    expected: "Every relevant abuse category yields at least one evaluated scenario."
  - anchor: businesslogic-examples
    what: "Per-stack vulnerable/secure recipe pairs: Django, FastAPI, Express, Spring, Go — covering price trust, coupon races, TOCTOU, workflow skipping, and entitlement caching."
    problem: "Enforcement idioms differ per framework, and generic logic rules miss stack-specific atomicity and validation tools like SELECT FOR UPDATE, compare-and-swap, and dependency injection; stack recipes, atomicity patterns, validation styles, precise detection, pattern matching, call diversity, orm features."
    use_when: "Target uses one of the covered stacks; reviewing flow-critical handlers."
    avoid_when: "Attack categories are the question — see that anchor; conceptual definitions wanted."
    expected: "Stack-specific unenforced rules flagged; atomic or validated flows verified."
  - anchor: businesslogic-prevention-guidance
    what: "Layered defense checklist: server-side validation, atomic operations, idempotency keys, state machines, locking, rate limits, monitoring, fingerprinting, CAPTCHA, proxy blocking, M2M limits."
    problem: "Remediation advice scattered across guides leaves gaps that let one missed control reopen flow abuse; remediation checklist, control mapping, defense completeness, gap elimination, hardening steps, anti automation, systematic mitigation, closure guarantee."
    use_when: "Writing remediation; reviewing whether defenses are complete."
    avoid_when: "Detection mechanics are the question — see execution anchors."
    expected: "Every finding closes with a complete, layered control set."
  - anchor: businesslogic-compensating-controls
    what: "Detection guide for compensating controls — evidence that a seemingly vulnerable flow is actually guarded by monitoring, limits, or downstream reconciliation."
    problem: "Verify subagents flag flows as exploitable when unseen compensating controls already neutralize abuse, inflating false positives across batches; control discovery, guard evidence, reconciliation checks, monitoring signals, downgrade discipline, verification rigor, defense in depth."
    use_when: "A scenario looks vulnerable; before confirming, hidden mitigations must be ruled out."
    avoid_when: "No control evidence exists at all — classify directly; prevention checklist wanted."
    expected: "Findings confirmed only after compensating controls are searched and excluded."
  - anchor: businesslogic-execution
    what: "Three-phase execution: domain recon generating attack scenarios with a zero-scenario early-exit gate, batched verify in groups of three, merge into the final module report."
    problem: "Detection work without orchestration duplicates effort, loses batch boundaries, and merges findings inconsistently; execution model, phase overview, subagent orchestration, context passing, batch discipline, workflow entry, staging, dispatch plan, consolidation, handoff clarity."
    use_when: "Starting the logic scan execution; dispatching or reviewing any phase."
    avoid_when: "Conceptual knowledge is the need — see definition and categories anchors."
    expected: "All three phases run with shared architecture context into one consolidated report."
  - anchor: businesslogic-references
    what: "External link list for business-logic abuse concepts, OWASP material, and case studies."
    problem: "Agents and readers need authoritative follow-up sources beyond this file's distilled content when deeper verification is required; further reading, external canon, deep dives, vendor documentation, community knowledge, primary material, cited works, owasp pages."
    use_when: "Primary sources or extended material is needed."
    avoid_when: "Detection recipes or execution workflow are the question — the references list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
  - anchor: businesslogic-important-reminders
    what: "Closing operational reminders: phase ordering, batch discipline, domain-first thinking, and cleanup rules."
    problem: "Modules close with inconsistent final guidance, letting unverified scenarios or weak proof slip into reports and client deliverables; closing rules, quality floor, consistency, final reminders, weak evidence, uniform endings, wrap discipline, audit closure."
    use_when: "Finalizing the module report; reviewing closing guidance."
    avoid_when: "Detection or execution is the current stage — finish those first."
    expected: "Reports close with uniform final rules applied."
---

# Business Logic Vulnerability Detection

[ref: #businesslogic-detection]

You are performing a focused security assessment to find business logic vulnerabilities in a codebase. This skill maps directly to **OWASP API Security Top 10 2023 — API6:2023 Unrestricted Access to Sensitive Business Flows**: automated or excessive access to business flows that should be protected against abuse. This skill uses a three-phase approach with subagents: **reconnaissance** (understand the domain and generate attack scenarios), **batched verify** (check whether scenarios are vulnerable in parallel batches of 3), and **merge** (consolidate batch results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

***

## OWASP API6:2023 Mapping
[ref: #businesslogic-owasp-mapping]

This reference implements the detection guidance for **API6:2023 — Unrestricted Access to Sensitive Business Flows**.

### Risk Summary

| Threat agents / Attack vectors | Security Weakness | Impacts |
| - | - | - |
| API Specific : Exploitability **Easy** | Prevalence **Widespread** : Detectability **Average** | Technical **Moderate** : Business Specific |
| Exploitation usually involves understanding the business model backed by the API, finding sensitive business flows, and automating access to these flows, causing harm to the business. | Lack of a holistic view of the API in order to fully support business requirements tends to contribute to the prevalence of this issue. Attackers manually identify what resources (e.g. endpoints) are involved in the target workflow and how they work together. If mitigation mechanisms are already in place, attackers need to find a way to bypass them. | In general technical impact is not expected. Exploitation might hurt the business in different ways, for example: prevent legitimate users from purchasing a product, or lead to inflation in the internal economy of a game. |

Source: OWASP API Security Top 10 2023, API6:2023.

### Sensitive Business Flows

API6:2023 calls out flows that are especially sensitive to automated or excessive access. The table below maps OWASP's examples to the attack categories used in this reference.

| Sensitive flow | Risk of excessive / automated access | Relevant attack category in this reference |
|---|---|---|
| Purchasing a product | An attacker buys all stock of a high-demand item at once and resells for a higher price (scalping). | Inventory & Stock Logic; Automated Exploitation of Sensitive Business Flows |
| Creating a comment / post | An attacker spams the system, degrading quality or exhausting moderation capacity. | Automated Exploitation of Sensitive Business Flows |
| Making a reservation | An attacker reserves all available time slots and prevents legitimate users from booking. | Automated Exploitation of Sensitive Business Flows; Inventory & Stock Logic |
| Referral / signup programs | An attacker automates registration to farm credits, bonuses, or rewards. | Reward, Referral & Loyalty Abuse; Automated Exploitation of Sensitive Business Flows |

### OWASP Example Attack Scenarios

The following scenarios are taken directly from API6:2023 and must be considered during threat modeling:

**Scenario #1 — Scalping a limited product**
A technology company announces they are going to release a new gaming console on Thanksgiving. The product has a very high demand and the stock is limited. An attacker writes code to automatically buy the new product and complete the transaction. On the release day, the attacker runs the code distributed across different IP addresses and locations. The API doesn't implement the appropriate protection and allows the attacker to buy the majority of the stock before other legitimate users. Later on, the attacker sells the product on another platform for a much higher price.

**Scenario #2 — Reservation blocking and late cancellation**
An airline company offers online ticket purchasing with no cancellation fee. A user with malicious intentions books 90% of the seats of a desired flight. A few days before the flight the malicious user canceled all the tickets at once, which forced the airline to discount the ticket prices in order to fill the flight. At this point, the user buys herself a single ticket that is much cheaper than the original one.

**Scenario #3 — Referral program abuse**
A ride-sharing app provides a referral program — users can invite their friends and gain credit for each friend who has joined the app. This credit can be later used as cash to book rides. An attacker exploits this flow by writing a script to automate the registration process, with each new user adding credit to the attacker's wallet. The attacker can later enjoy free rides or sell the accounts with excessive credits for cash.

### OWASP Prevention Mapping

API6:2023 splits mitigation into two layers:

1. **Business layer** — identify the business flows that might harm the business if they are excessively used.
2. **Engineering layer** — choose the right protection mechanisms to mitigate the business risk.

The engineering controls emphasized by OWASP are:

- **Device fingerprinting**: deny service to unexpected client devices (e.g. headless browsers), raising the cost for attackers.
- **Human detection**: use CAPTCHA or more advanced biometric solutions (e.g. typing patterns).
- **Non-human pattern detection**: analyze the user flow to detect non-human patterns (e.g. the user accessed "add to cart" and "complete purchase" in less than one second).
- **Block Tor exit nodes and well-known proxies**: reduce anonymity for automated abuse.
- **Secure and limit access to machine-to-machine APIs**: developer and B2B APIs often lack the protections applied to user-facing flows.

These controls are evaluated in the **Compensating Controls Detection** section below.

***

## CWE Mapping
[ref: #businesslogic-cwe-mapping]

Business logic flaws map to multiple CWE entries. Use these mappings when classifying findings, writing reports, or correlating with other tooling.

| CWE | Name | Relevant business logic flaw |
|---|---|---|
| CWE-841 | Improper Enforcement of Behavioral Workflow | Workflow bypass, multi-step process abuse, state-machine violations, skipping mandatory steps. |
| CWE-770 | Allocation of Resources Without Limits or Throttling | Automated abuse, scalping, spamming, reservation blocking, excessive referral signup, lack of rate limits. |
| CWE-20 | Improper Input Validation | Negative prices, negative quantities, out-of-range ratings/scores, arbitrary price override, currency confusion. |
| CWE-362 | Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') | Double-spending, inventory TOCTOU, concurrent coupon redemption, parallel withdrawal exceeding balance. |
| CWE-408 | Incorrect Behavior Order: Early Amplification | Performing an action before prerequisites are verified (e.g. completing checkout before payment). |
| CWE-691 | Insufficient Control Flow Management | Missing or bypassed state-machine guards, unintended transitions between workflow states. |
| CWE-1339 | Insufficient Precision or Accuracy of a Real Number | Floating-point precision abuse in monetary arithmetic, rounding exploits across micro-transactions. |
| CWE-837 | Improper Enforcement of a Single, Unique Action | Reusing single-use coupons/vouchers/idempotency keys, duplicate redemption, duplicate submission. |

***

## What are Business Logic Vulnerabilities
[ref: #businesslogic-definition]

Business logic vulnerabilities arise when an application's intended workflow, rules, or constraints can be manipulated to produce unintended outcomes — without exploiting technical flaws like injection or memory corruption. The attacker operates within the application's own features but uses them in ways the developers did not anticipate.

The core pattern: *the application accepts input that is syntactically valid and passes authentication/authorization, but violates a business rule that was never enforced in code.*

### What Business Logic Vulnerabilities ARE

- Submitting a negative quantity to a purchase endpoint, receiving a credit instead of a charge
- Applying the same one-time discount coupon multiple times in parallel requests
- Skipping the payment step in a multi-step checkout by replaying a later step's request
- Posting a rating of 9999 to a movie rating endpoint that should cap ratings at 5
- Transferring a negative amount to move money from the recipient to the sender
- Redeeming a referral bonus by referring yourself with a second account
- Re-using a single-use reset token or voucher that was never invalidated
- Purchasing an item that is out of stock due to a race condition between inventory check and reservation
- Accessing a premium subscription feature after downgrading to a free plan
- Winning an auction by retracting a high bid after others have been eliminated

### What Business Logic Vulnerabilities are Not

Do not flag these as business logic issues:

- **SQL injection, XSS, RCE, XXE, SSRF, SSTI**: These are injection/technical flaws — separate skills cover them
- **Missing authentication**: Endpoint requires no login at all → that's "Unauthenticated Access"
- **IDOR**: Accessing another user's resource by changing an ID → that's a separate access-control class
- **Brute-force / rate limiting**: Generic rate-limit bypass on login → that's not a business logic flaw unless it enables specific business rule circumvention

***

## Business Logic Attack Categories
[ref: #businesslogic-attack-categories]

Use these categories to guide threat modeling. Not all categories apply to every application — identify which ones are relevant based on the architecture summary.

### 1. Price & Payment Manipulation
- Negative prices or zero prices on purchase endpoints
- Arbitrary price override in request body (mass assignment of price field)
- Currency or unit confusion (e.g., cents vs. dollars)
- Floating-point precision abuse in monetary arithmetic
- Applying discounts that reduce total below zero

### 2. Quantity & Numeric Limit Violations
- Negative quantities (ordering −5 items to receive a credit)
- Quantities exceeding per-user or per-order limits
- Integer overflow/underflow in quantity or balance calculations
- Out-of-range values for bounded fields (ratings, scores, percentages)

### 3. Workflow & Multi-Step Process Bypass
- Skipping mandatory steps in a sequential process (payment, email verification, ID check)
- Replaying a completion token from a previous successful flow to bypass steps
- Direct-access to a later-stage endpoint without completing earlier stages
- Submitting a terminal state transition without going through intermediate states (state machine violations)

### 4. Coupon, Discount & Voucher Abuse
- Applying the same coupon multiple times (single-use not enforced)
- Stacking discounts that were not intended to be combined
- Using an expired coupon or voucher
- Generating or guessing valid coupon codes

### 5. Race Conditions & Concurrency Abuse
- Double-spending: sending two concurrent purchase requests to consume a balance once
- Concurrent coupon redemption draining credit beyond allowed amount
- TOCTOU (time-of-check / time-of-use) on inventory: check passes for both requests, both reservations succeed
- Parallel withdrawal/transfer requests exceeding account balance

### 6. Refund & Chargeback Abuse
- Requesting a refund after the digital good has been consumed or downloaded
- Partial refund on an already-partially-refunded order
- Refund without returning physical item (if logic is not enforced server-side)

### 7. Reward, Referral & Loyalty Abuse
- Self-referral using a second account to earn a referral bonus
- Earning signup bonuses multiple times across multiple accounts
- Loyalty point farming through artificial activity
- Sharing or transferring non-transferable rewards

### 8. Subscription & Entitlement Bypass
- Accessing paid/premium features after downgrading or cancelling
- Trial period abuse (repeatedly creating new accounts for trial access)
- Feature flag or plan check performed only at subscription creation, not at feature access time
- Entitlement cached at session start and not re-evaluated after plan change

### 9. Auction & Bidding Logic
- Retracting a winning bid after competing bids have been rejected
- Shill bidding: artificially inflating price with controlled accounts
- Bypass of reserve price enforcement
- Bid manipulation via concurrent requests

### 10. Inventory & Stock Logic
- Purchasing out-of-stock items due to missing stock validation
- Reserving more stock than available via concurrent requests
- Negative inventory resulting from refund-without-restock logic
- Phantom inventory: item appears available but cannot be fulfilled

### 11. Time & Date Logic
- Using time-limited offers after expiration (expiry checked client-side or weakly server-side)
- Backdating transactions or bookings
- Exploiting "grace period" logic to extend benefits indefinitely
- System clock manipulation if server trusts client-supplied timestamps

### 12. Transfer & Balance Logic
- Transferring a negative amount (sender receives money from recipient)
- Self-transfer to exploit bonus or fee logic
- Transferring more than the available balance due to missing server-side check
- Rounding errors exploited across many micro-transactions

### 13. Automated Exploitation of Sensitive Business Flows
- Scalping or hoarding limited-availability goods, tickets, or reservations through automated requests
- Spamming submissions that degrade service quality or exhaust human-review capacity
- Reservation blocking or no-show abuse that denies availability to legitimate users
- Referral, signup, or promotional bonus abuse orchestrated across many accounts or scripts
- Content scraping or data harvesting at scale against endpoints meant for individual users
- Credential stuffing or account takeover against business flows (login, checkout, transfer) to monetize accounts

***

## Vulnerable vs. Secure Examples
[ref: #businesslogic-examples]

The examples below show common business logic flaws in four major stacks. Use them as patterns when reviewing code. In every case, the secure version enforces the rule server-side, atomically, and at the point of use.

### Python / Django

#### Negative price / quantity

```python
# VULNERABLE: trusts the client-supplied price and does not reject negative quantities.
@api_view(["POST"])
def create_order(request):
    product_id = request.data["product_id"]
    quantity = request.data["quantity"]
    price = request.data["price"]  # attacker can send a negative price
    total = Decimal(price) * quantity
    Order.objects.create(product_id=product_id, quantity=quantity, total=total)
```

```python
# SECURE: price is taken from the product record; quantity is validated; Decimal is used.
from django.db.models import F
from rest_framework.exceptions import ValidationError

@api_view(["POST"])
def create_order(request):
    product = Product.objects.get(id=request.data["product_id"])
    quantity = int(request.data["quantity"])
    if quantity <= 0:
        raise ValidationError("Quantity must be positive.")
    total = product.price * Decimal(quantity)
    Order.objects.create(product=product, quantity=quantity, total=total)
```

#### Coupon reuse

```python
# VULNERABLE: check-and-use is not atomic; concurrent requests can redeem the same coupon twice.
@transaction.atomic
def apply_coupon(request, code):
    coupon = Coupon.objects.get(code=code, used=False)
    order = Order.objects.get(user=request.user, id=request.data["order_id"])
    order.discount = coupon.amount
    order.save()
    coupon.used = True
    coupon.save()
```

```python
# SECURE: SELECT FOR UPDATE ensures only one transaction can redeem the coupon.
@transaction.atomic
def apply_coupon(request, code):
    coupon = Coupon.objects.select_for_update().get(code=code, used=False)
    order = Order.objects.select_for_update().get(user=request.user, id=request.data["order_id"])
    order.discount = coupon.amount
    order.save()
    coupon.used = True
    coupon.save()
```

#### Inventory race condition

```python
# VULNERABLE: TOCTOU between the read and the write.
@transaction.atomic
def purchase(request):
    product = Product.objects.get(id=request.data["product_id"])
    quantity = request.data["quantity"]
    if product.stock >= quantity:
        product.stock -= quantity
        product.save()
        Order.objects.create(...)
```

```python
# SECURE: atomic compare-and-swap decrement; exactly one concurrent request wins.
from django.db.models import F

@transaction.atomic
def purchase(request):
    quantity = int(request.data["quantity"])
    if quantity <= 0:
        raise ValidationError("Quantity must be positive.")
    updated = Product.objects.filter(
        id=request.data["product_id"], stock__gte=quantity
    ).update(stock=F("stock") - quantity)
    if updated == 0:
        raise ValidationError("Insufficient stock.")
    Order.objects.create(...)
```

#### Workflow bypass

```python
# VULNERABLE: the completion endpoint does not verify prior steps.
@api_view(["POST"])
def complete_checkout(request):
    order = Order.objects.get(id=request.data["order_id"])
    order.status = "completed"
    order.save()
    ship_order(order)
```

```python
# SECURE: state machine enforces that only "paid" orders can be completed.
VALID_TRANSITIONS = {"paid": "completed", "pending": "cancelled"}

@api_view(["POST"])
def complete_checkout(request):
    order = Order.objects.select_for_update().get(id=request.data["order_id"])
    if order.status != "paid":
        raise ValidationError("Order must be paid before completion.")
    order.status = "completed"
    order.save()
    ship_order(order)
```

#### Subscription entitlement

```python
# VULNERABLE: entitlement is cached in the session at login and never re-evaluated.
def premium_feature(request):
    if request.session.get("plan") == "premium":
        return premium_content()
```

```python
# SECURE: current subscription is checked on every sensitive feature access.
def premium_feature(request):
    subscription = request.user.subscription
    if not subscription or subscription.plan != "premium" or subscription.is_expired():
        raise PermissionDenied("Premium subscription required.")
    return premium_content()
```

### Python / FastAPI

```python
# VULNERABLE: client-controlled price accepted via Pydantic model
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class OrderIn(BaseModel):
    product_id: int
    price: float  # attacker sets the price
    quantity: int

@app.post("/api/orders")
def create_order(order: OrderIn):
    total = order.price * order.quantity
    charge_card(total)
    return {"total": total}

# SECURE: price comes from the product record; quantity bounded; Decimal arithmetic
from decimal import Decimal
from fastapi import HTTPException

class OrderIn(BaseModel):
    product_id: int
    quantity: int

@app.post("/api/orders")
def create_order(order: OrderIn):
    if not 1 <= order.quantity <= 100:
        raise HTTPException(status_code=400)
    product = db.get_product(order.product_id)
    total = product.price * Decimal(order.quantity)  # server-side price only
    charge_card(total)
    return {"total": str(total)}
```

### Node.js / Express

#### Negative price / quantity

```javascript
// VULNERABLE: trusts req.body.price and req.body.quantity.
app.post("/api/orders", async (req, res) => {
  const { productId, quantity, price } = req.body;
  const total = price * quantity;
  await Order.create({ productId, quantity, total });
  res.json({ ok: true });
});
```

```javascript
// SECURE: price fetched from product; quantity validated.
app.post("/api/orders", async (req, res) => {
  const { productId, quantity } = req.body;
  if (!Number.isInteger(quantity) || quantity <= 0) {
    return res.status(400).json({ error: "Invalid quantity." });
  }
  const product = await Product.findById(productId);
  const total = product.price * quantity;
  await Order.create({ productId, quantity, total });
  res.json({ ok: true });
});
```

#### Coupon reuse

```javascript
// VULNERABLE: read then update allows parallel redemption.
app.post("/api/coupons/apply", async (req, res) => {
  const coupon = await Coupon.findOne({ code: req.body.code, used: false });
  if (!coupon) return res.status(400).json({ error: "Invalid coupon." });
  await Order.updateOne({ _id: req.body.orderId }, { discount: coupon.amount });
  coupon.used = true;
  await coupon.save();
  res.json({ ok: true });
});
```

```javascript
// SECURE: atomic find-and-update with a status condition.
app.post("/api/coupons/apply", async (req, res) => {
  const coupon = await Coupon.findOneAndUpdate(
    { code: req.body.code, used: false },
    { used: true },
    { new: true }
  );
  if (!coupon) return res.status(400).json({ error: "Invalid or already used coupon." });
  await Order.updateOne({ _id: req.body.orderId }, { discount: coupon.amount });
  res.json({ ok: true });
});
```

#### Inventory race condition

```javascript
// VULNERABLE: read-modify-write race.
app.post("/api/purchase", async (req, res) => {
  const product = await Product.findById(req.body.productId);
  if (product.stock >= req.body.quantity) {
    product.stock -= req.body.quantity;
    await product.save();
    await Order.create({ productId: product._id, quantity: req.body.quantity });
    res.json({ ok: true });
  } else {
    res.status(400).json({ error: "Out of stock." });
  }
});
```

```javascript
// SECURE: atomic decrement with $inc and stock guard.
app.post("/api/purchase", async (req, res) => {
  const quantity = req.body.quantity;
  if (!Number.isInteger(quantity) || quantity <= 0) {
    return res.status(400).json({ error: "Invalid quantity." });
  }
  const product = await Product.findOneAndUpdate(
    { _id: req.body.productId, stock: { $gte: quantity } },
    { $inc: { stock: -quantity } },
    { new: true }
  );
  if (!product) return res.status(400).json({ error: "Out of stock." });
  await Order.create({ productId: product._id, quantity });
  res.json({ ok: true });
});
```

#### Workflow bypass

```javascript
// VULNERABLE: any order can be completed.
app.post("/api/orders/:id/complete", async (req, res) => {
  await Order.updateOne({ _id: req.params.id }, { status: "completed" });
  res.json({ ok: true });
});
```

```javascript
// SECURE: only paid orders can be completed.
app.post("/api/orders/:id/complete", async (req, res) => {
  const order = await Order.findOneAndUpdate(
    { _id: req.params.id, status: "paid" },
    { status: "completed" },
    { new: true }
  );
  if (!order) return res.status(400).json({ error: "Order is not in paid state." });
  res.json({ ok: true });
});
```

#### Subscription entitlement

```javascript
// VULNERABLE: plan cached in JWT/session.
app.get("/api/premium", (req, res) => {
  if (req.user.plan === "premium") {
    return res.json(premiumContent());
  }
  res.status(403).json({ error: "Premium required." });
});
```

```javascript
// SECURE: subscription re-evaluated on every request.
app.get("/api/premium", async (req, res) => {
  const subscription = await Subscription.findOne({ userId: req.user.id });
  if (!subscription || subscription.plan !== "premium" || subscription.expiresAt < new Date()) {
    return res.status(403).json({ error: "Premium subscription required." });
  }
  res.json(premiumContent());
});
```

### Java / Spring

#### Negative price / quantity

```java
// VULNERABLE: no server-side validation; price from request.
@PostMapping("/orders")
public ResponseEntity<?> createOrder(@RequestBody OrderRequest req) {
    BigDecimal total = req.getPrice().multiply(BigDecimal.valueOf(req.getQuantity()));
    orderRepository.save(new Order(req.getProductId(), req.getQuantity(), total));
    return ResponseEntity.ok().build();
}
```

```java
// SECURE: quantity validated; price fetched from product record.
@PostMapping("/orders")
public ResponseEntity<?> createOrder(@Valid @RequestBody OrderRequest req) {
    if (req.getQuantity() <= 0) {
        return ResponseEntity.badRequest().body("Quantity must be positive.");
    }
    Product product = productRepository.findById(req.getProductId()).orElseThrow();
    BigDecimal total = product.getPrice().multiply(BigDecimal.valueOf(req.getQuantity()));
    orderRepository.save(new Order(product, req.getQuantity(), total));
    return ResponseEntity.ok().build();
}

public class OrderRequest {
    @NotNull @Positive
    private Integer quantity;
    @NotNull
    private Long productId;
}
```

#### Coupon reuse

```java
// VULNERABLE: no locking; race condition between check and update.
@Transactional
@PostMapping("/coupons/{code}/apply")
public ResponseEntity<?> applyCoupon(@PathVariable String code) {
    Coupon coupon = couponRepository.findByCodeAndUsedFalse(code)
        .orElseThrow(() -> new BadRequestException("Invalid coupon"));
    coupon.setUsed(true);
    couponRepository.save(coupon);
    return ResponseEntity.ok().build();
}
```

```java
// SECURE: optimistic locking via @Version; only one transaction commits.
@Entity
public class Coupon {
    @Id private Long id;
    @Version private Long version;
    private String code;
    private boolean used;
    // ...
}

@Transactional
@PostMapping("/coupons/{code}/apply")
public ResponseEntity<?> applyCoupon(@PathVariable String code) {
    Coupon coupon = couponRepository.findByCodeAndUsedFalse(code)
        .orElseThrow(() -> new BadRequestException("Invalid coupon"));
    coupon.setUsed(true);
    try {
        couponRepository.save(coupon);
    } catch (OptimisticLockingFailureException e) {
        throw new BadRequestException("Coupon was already used.");
    }
    return ResponseEntity.ok().build();
}
```

#### Inventory race condition

```java
// VULNERABLE: read-then-write allows overselling.
@Transactional
@PostMapping("/purchase")
public ResponseEntity<?> purchase(@RequestBody PurchaseRequest req) {
    Product product = productRepository.findById(req.getProductId()).orElseThrow();
    if (product.getStock() >= req.getQuantity()) {
        product.setStock(product.getStock() - req.getQuantity());
        productRepository.save(product);
        orderRepository.save(new Order(product, req.getQuantity()));
        return ResponseEntity.ok().build();
    }
    return ResponseEntity.badRequest().body("Out of stock.");
}
```

```java
// SECURE: atomic JPQL update with stock guard.
@Transactional
@Modifying
@Query("UPDATE Product p SET p.stock = p.stock - :qty WHERE p.id = :id AND p.stock >= :qty")
int decrementStock(@Param("id") Long id, @Param("qty") int qty);

@PostMapping("/purchase")
public ResponseEntity<?> purchase(@RequestBody PurchaseRequest req) {
    if (req.getQuantity() <= 0) {
        return ResponseEntity.badRequest().body("Invalid quantity.");
    }
    int updated = productRepository.decrementStock(req.getProductId(), req.getQuantity());
    if (updated == 0) {
        return ResponseEntity.badRequest().body("Out of stock.");
    }
    orderRepository.save(new Order(productRepository.findById(req.getProductId()).orElseThrow(), req.getQuantity()));
    return ResponseEntity.ok().build();
}
```

#### Workflow bypass

```java
// VULNERABLE: status can be set directly to completed.
@PostMapping("/orders/{id}/complete")
public ResponseEntity<?> completeOrder(@PathVariable Long id) {
    Order order = orderRepository.findById(id).orElseThrow();
    order.setStatus("completed");
    orderRepository.save(order);
    return ResponseEntity.ok().build();
}
```

```java
// SECURE: state transition guarded inside the domain object.
@Entity
public class Order {
    // ...
    public void complete() {
        if (!"paid".equals(status)) {
            throw new IllegalStateException("Order must be paid before completion.");
        }
        this.status = "completed";
    }
}

@PostMapping("/orders/{id}/complete")
public ResponseEntity<?> completeOrder(@PathVariable Long id) {
    Order order = orderRepository.findById(id).orElseThrow();
    order.complete();
    orderRepository.save(order);
    return ResponseEntity.ok().build();
}
```

#### Subscription entitlement

```java
// VULNERABLE: entitlement resolved from JWT claim set at login.
@GetMapping("/premium")
public ResponseEntity<?> premiumFeature(@AuthenticationPrincipal Jwt jwt) {
    if ("premium".equals(jwt.getClaimAsString("plan"))) {
        return ResponseEntity.ok(premiumContent());
    }
    return ResponseEntity.status(403).body("Premium required.");
}
```

```java
// SECURE: current subscription loaded and checked on each request.
@GetMapping("/premium")
public ResponseEntity<?> premiumFeature(@AuthenticationPrincipal User user) {
    Subscription sub = subscriptionRepository.findActiveByUserId(user.getId())
        .orElseThrow(() -> new AccessDeniedException("Premium subscription required."));
    if (!sub.isActive()) {
        return ResponseEntity.status(403).body("Subscription expired.");
    }
    return ResponseEntity.ok(premiumContent());
}
```

### Go

#### Negative price / quantity

```go
// VULNERABLE: price parsed from request; no validation.
func CreateOrder(w http.ResponseWriter, r *http.Request) {
    var req struct {
        ProductID int64   `json:"product_id"`
        Quantity  int     `json:"quantity"`
        Price     float64 `json:"price"`
    }
    json.NewDecoder(r.Body).Decode(&req)
    total := req.Price * float64(req.Quantity)
    db.Exec("INSERT INTO orders (product_id, quantity, total) VALUES ($1, $2, $3)", req.ProductID, req.Quantity, total)
    w.WriteHeader(http.StatusCreated)
}
```

```go
// SECURE: price from database; quantity validated; integer cents used.
func CreateOrder(w http.ResponseWriter, r *http.Request) {
    var req struct {
        ProductID int64 `json:"product_id"`
        Quantity  int   `json:"quantity"`
    }
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Quantity <= 0 {
        http.Error(w, "Invalid quantity.", http.StatusBadRequest)
        return
    }
    var priceCents int64
    if err := db.QueryRow("SELECT price_cents FROM products WHERE id = $1", req.ProductID).Scan(&priceCents); err != nil {
        http.Error(w, "Product not found.", http.StatusNotFound)
        return
    }
    totalCents := priceCents * int64(req.Quantity)
    db.Exec("INSERT INTO orders (product_id, quantity, total_cents) VALUES ($1, $2, $3)", req.ProductID, req.Quantity, totalCents)
    w.WriteHeader(http.StatusCreated)
}
```

#### Coupon reuse

```go
// VULNERABLE: SELECT then UPDATE is not atomic.
func ApplyCoupon(w http.ResponseWriter, r *http.Request) {
    var req struct{ Code string `json:"code"` }
    json.NewDecoder(r.Body).Decode(&req)
    var coupon Coupon
    db.QueryRow("SELECT id, used FROM coupons WHERE code = $1", req.Code).Scan(&coupon.ID, &coupon.Used)
    if coupon.Used {
        http.Error(w, "Coupon used.", http.StatusBadRequest)
        return
    }
    db.Exec("UPDATE coupons SET used = true WHERE id = $1", coupon.ID)
    w.WriteHeader(http.StatusOK)
}
```

```go
// SECURE: single UPDATE with RETURNING and condition ensures one redemption.
func ApplyCoupon(w http.ResponseWriter, r *http.Request) {
    var req struct{ Code string `json:"code"` }
    json.NewDecoder(r.Body).Decode(&req)
    var id int64
    err := db.QueryRow(`
        UPDATE coupons SET used = true
        WHERE code = $1 AND used = false
        RETURNING id
    `, req.Code).Scan(&id)
    if err != nil {
        http.Error(w, "Invalid or already used coupon.", http.StatusBadRequest)
        return
    }
    w.WriteHeader(http.StatusOK)
}
```

#### Inventory race condition

```go
// VULNERABLE: read then write allows overselling.
func Purchase(w http.ResponseWriter, r *http.Request) {
    var req struct {
        ProductID int64 `json:"product_id"`
        Quantity  int   `json:"quantity"`
    }
    json.NewDecoder(r.Body).Decode(&req)
    var stock int
    db.QueryRow("SELECT stock FROM products WHERE id = $1", req.ProductID).Scan(&stock)
    if stock >= req.Quantity {
        db.Exec("UPDATE products SET stock = stock - $1 WHERE id = $2", req.Quantity, req.ProductID)
        db.Exec("INSERT INTO orders (product_id, quantity) VALUES ($1, $2)", req.ProductID, req.Quantity)
        w.WriteHeader(http.StatusCreated)
    } else {
        http.Error(w, "Out of stock.", http.StatusBadRequest)
    }
}
```

```go
// SECURE: single UPDATE with WHERE stock >= quantity.
func Purchase(w http.ResponseWriter, r *http.Request) {
    var req struct {
        ProductID int64 `json:"product_id"`
        Quantity  int   `json:"quantity"`
    }
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Quantity <= 0 {
        http.Error(w, "Invalid quantity.", http.StatusBadRequest)
        return
    }
    res, err := db.Exec(`
        UPDATE products SET stock = stock - $1
        WHERE id = $2 AND stock >= $1
    `, req.Quantity, req.ProductID)
    if err != nil {
        http.Error(w, "Database error.", http.StatusInternalServerError)
        return
    }
    rows, _ := res.RowsAffected()
    if rows == 0 {
        http.Error(w, "Out of stock.", http.StatusBadRequest)
        return
    }
    db.Exec("INSERT INTO orders (product_id, quantity) VALUES ($1, $2)", req.ProductID, req.Quantity)
    w.WriteHeader(http.StatusCreated)
}
```

#### Workflow bypass

```go
// VULNERABLE: status set directly without checking prerequisites.
func CompleteOrder(w http.ResponseWriter, r *http.Request) {
    var req struct{ OrderID int64 `json:"order_id"` }
    json.NewDecoder(r.Body).Decode(&req)
    db.Exec("UPDATE orders SET status = 'completed' WHERE id = $1", req.OrderID)
    w.WriteHeader(http.StatusOK)
}
```

```go
// SECURE: UPDATE guards the current state; only paid orders become completed.
func CompleteOrder(w http.ResponseWriter, r *http.Request) {
    var req struct{ OrderID int64 `json:"order_id"` }
    json.NewDecoder(r.Body).Decode(&req)
    res, err := db.Exec(`
        UPDATE orders SET status = 'completed'
        WHERE id = $1 AND status = 'paid'
    `, req.OrderID)
    if err != nil {
        http.Error(w, "Database error.", http.StatusInternalServerError)
        return
    }
    rows, _ := res.RowsAffected()
    if rows == 0 {
        http.Error(w, "Order is not in paid state.", http.StatusBadRequest)
        return
    }
    w.WriteHeader(http.StatusOK)
}
```

#### Subscription entitlement

```go
// VULNERABLE: plan from context/token set at login.
func PremiumFeature(w http.ResponseWriter, r *http.Request) {
    user := r.Context().Value("user").(User)
    if user.Plan != "premium" {
        http.Error(w, "Premium required.", http.StatusForbidden)
        return
    }
    json.NewEncoder(w).Encode(premiumContent())
}
```

```go
// SECURE: current subscription loaded per request.
func PremiumFeature(w http.ResponseWriter, r *http.Request) {
    user := r.Context().Value("user").(User)
    var active bool
    err := db.QueryRow(`
        SELECT EXISTS(
            SELECT 1 FROM subscriptions
            WHERE user_id = $1 AND plan = 'premium' AND expires_at > now()
        )
    `, user.ID).Scan(&active)
    if err != nil || !active {
        http.Error(w, "Premium subscription required.", http.StatusForbidden)
        return
    }
    json.NewEncoder(w).Encode(premiumContent())
}
```

***

## How to Prevent
[ref: #businesslogic-prevention-guidance]

Preventing business logic flaws requires enforcing rules on the server, atomically, and at the point of use. The following controls are mandatory for any sensitive business flow.

### Server-Side Validation

Never trust the client. All business constraints must be validated on the server:

- Reject out-of-range, negative, zero, or nonsensical values for price, quantity, balance, rating, score, percentage, and similar numeric fields.
- Use strongly typed models and explicit allow-lists instead of mass-assigning request fields directly to database entities.
- Validate enums, status values, and state transitions against an authoritative allow-list.
- Re-validate prerequisites at every step, not just once at the beginning of a flow.
- Use integer arithmetic for money (cents) or `Decimal` / `BigDecimal` types; never use floating-point currency.

### Atomic Database Operations

Race conditions are among the highest-impact business logic flaws. Eliminate check-then-act patterns:

- Combine the check and the mutation in a single database statement (e.g., `UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?`).
- Use database transactions that wrap the validation, mutation, and side effects.
- Rely on affected-row counts to confirm that the condition held.
- Enforce unique constraints at the database level (e.g., one redemption per user/coupon pair).

### Idempotency Keys

Protect against duplicate submission and replay:

- Require clients to send an idempotency key (`Idempotency-Key` header or similar) for any state-changing operation that must happen at most once.
- Store processed keys with their outcome; reject or return the cached outcome for duplicate keys.
- Set key expiration appropriate to the business flow.

### State Machines for Workflows

Multi-step flows must be modeled as explicit state machines:

- Define every legal state and every legal transition.
- Store the current state server-side, not in client tokens or hidden form fields.
- Each endpoint must verify that the current state allows the requested transition.
- Do not allow terminal states to be reached from arbitrary earlier states.

### Optimistic and Pessimistic Locking

Choose the right concurrency control:

- **Pessimistic locking** (`SELECT FOR UPDATE`) is appropriate when contention is high and the cost of a conflict is large (e.g., inventory reservation, coupon redemption).
- **Optimistic locking** (`@Version`, version column) is appropriate when conflicts are rare; handle `OptimisticLockException` by retrying or returning a conflict response.
- Use database-level constraints as a final safety net.

### Per-User and Per-Device Rate Limits

Restrict how often a single actor can invoke a sensitive flow:

- Apply per-user rate limits for flows such as purchase, booking, referral, withdrawal, and review.
- Apply per-device or per-session limits to slow down scripted attacks even when the attacker rotates accounts.
- Use sliding-window or token-bucket algorithms; return `429 Too Many Requests` with a `Retry-After` header.
- Distinguish between read and write limits; write-heavy flows need tighter limits.

### Business-Flow Monitoring and Alerting

Detect abuse in real time:

- Log every sensitive business action with user ID, device fingerprint, IP, timestamp, and outcome.
- Define thresholds for anomalies: unusual velocity, geographic impossibility, repeated failures, or sudden spikes.
- Alert when thresholds are exceeded and trigger step-up authentication, manual review, or temporary blocks.
- Retain logs long enough to support incident response and chargeback disputes.

### Device Fingerprinting

Identify and challenge unexpected clients:

- Collect stable device signals such as TLS fingerprint, user-agent consistency, screen resolution (for browser clients), and installed fonts/canvas hash where appropriate.
- Compare the current fingerprint against the account's historical fingerprints; flag or block mismatches for sensitive actions.
- Treat headless browsers, automation frameworks, and missing JavaScript as high-risk signals.

### CAPTCHA and Human Detection

Add deliberate friction for high-risk actions:

- Require CAPTCHA or reCAPTCHA on signup, login, password reset, purchase, referral, and booking flows.
- Consider invisible/behavioral CAPTCHA to minimize user friction while still blocking automation.
- For high-value flows, use stronger human-detection mechanisms such as email/SMS verification, biometric checks, or typing-pattern analysis.

### Non-Human Pattern Detection

Behavioral analysis catches automation that bypasses simple rate limits:

- Measure timing between sequential steps (e.g., add-to-cart to checkout completed in under one second).
- Detect repetitive request signatures, identical payloads, or predictable timing intervals.
- Flag accounts that always perform actions in the exact same order or with identical headers.
- Use anomaly-detection models trained on normal user behavior.

### Blocking Tor Exit Nodes and Well-Known Proxies

Reduce anonymity for attackers:

- Maintain an up-to-date blocklist of Tor exit nodes, public proxies, VPN endpoints, and hosting-provider IP ranges.
- Apply the blocklist selectively to sensitive flows rather than site-wide, to avoid blocking legitimate privacy users from read-only access.
- Log and alert when requests from these sources attempt business actions.

### Secure and Limit Machine-to-Machine APIs

B2B and developer APIs are frequent targets:

- Require strong authentication (mTLS, scoped API keys, OAuth 2.0 client credentials) for every M2M endpoint.
- Apply strict per-client rate limits and quotas, including daily/hourly spending or resource budgets.
- Scope M2M credentials to the minimum business flows required; avoid all-or-nothing access.
- Audit M2M usage regularly for unusual patterns.

***

## Compensating Controls Detection
[ref: #businesslogic-compensating-controls]

When reviewing sensitive business flows, also flag missing compensating controls that mitigate automated or excessive abuse. These are especially relevant for API6:2023. A flow is at higher risk when several of the following are absent:

- **Device fingerprinting**: No collection or comparison of device identifiers, headers, TLS fingerprints, or browser characteristics
- **CAPTCHA / human-detection**: No challenge-response mechanism on high-risk actions (signup, login, purchase, referral, password reset)
- **Non-human pattern detection**: No detection of velocity spikes, headless browser signatures, missing/consistent user-agent strings, or programmatic request timing
- **Tor/proxy/VPN blocking**: No checks against known anonymization networks for sensitive flows
- **Machine-to-machine API limits and velocity checks**: No per-client, per-account, or per-IP rate limiting on business-critical endpoints
- **Behavioral analytics / step-up challenges**: No risk-based re-authentication, email/phone verification, or friction increase for anomalous behavior

Classify compensating-control gaps using the same labels:
- **[VULNERABLE]** when a sensitive flow has neither compensating controls nor server-side business-rule enforcement
- **[LIKELY VULNERABLE]** when controls exist but are bypassable, inconsistent, or not applied to the flow in question
- **[NOT VULNERABLE]** when adequate controls are present and enforced
- **[NEEDS MANUAL REVIEW]** when the control status cannot be determined from code alone

***

## Execution
[ref: #businesslogic-execution]

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

**Subagent constraint**: All subagents must treat this assessment as read-only. They must write findings only to the report files specified below and must **never modify project source code**.

### Phase 1: Reconnaissance — Domain Analysis & Attack Scenario Generation

Launch a subagent with the following instructions:

> **Goal**: Analyze the codebase to understand its business domain and generate a concrete, prioritized list of business logic attack scenarios specific to this application. Write results to `{{ REPORTS_ROOT }}/13_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand what the application does, what features it has, and what business rules it is supposed to enforce. Focus entirely on understanding the domain — do not verify vulnerabilities yet.
>
> **Constraints**: Do not modify project source code. Write findings only to `{{ REPORTS_ROOT }}/13_recon.md`.
>
> **Step 1 — Identify the business domain and features**:
>
> Read `{{ REPORTS_ROOT }}/01_architecture.md` and then explore the codebase to answer:
> - What does this application do? (e-commerce, marketplace, SaaS, social platform, fintech, gaming, booking, etc.)
> - What financial or transactional features exist? (payments, subscriptions, credits, tokens, wallets, invoices, refunds)
> - What quantitative limits or rules exist? (ratings, scores, quantities, usage limits, quotas)
> - What multi-step workflows exist? (checkout, onboarding, KYC, booking, auctions)
> - What promotional or reward features exist? (coupons, referrals, loyalty points, bonuses, vouchers)
> - What role or tier distinctions exist? (free vs. paid, user vs. premium, trial vs. full)
> - What inventory or capacity constraints exist? (stock, seats, slots, bandwidth)
>
> To discover features, search for:
> - Route/endpoint definitions and their names
> - Model/entity names (Order, Payment, Subscription, Coupon, Wallet, Bid, etc.)
> - Business-rule-related field names (price, quantity, balance, rating, score, limit, quota, expiry, status)
> - Validation logic or constraint-related code
>
> **Step 2 — Generate attack scenarios**:
>
> For each relevant business domain area found, generate specific attack scenarios. Each scenario must be:
> - **Specific to this codebase** — name the actual endpoint, model, or feature involved
> - **Actionable** — describe exactly what an attacker would send/do
> - **Grounded** — reference the code or data model that makes this scenario plausible
>
> Use the attack categories below as a checklist. Only include categories that are relevant to this application:
>
> - **Price/payment manipulation**: Can a user send an arbitrary price in the request? Is price trusted from client?
> - **Quantity/value out of range**: Can a user send negative quantities, zero, or values exceeding defined limits?
> - **Workflow bypass**: Can a user skip a mandatory step in a multi-step process?
> - **Coupon/discount abuse**: Can a coupon be used multiple times or after expiration?
> - **Race conditions**: Are there check-then-act patterns on shared resources (inventory, balance, coupon usage)?
> - **Refund abuse**: Can a refund be requested after the product is consumed?
> - **Reward/referral abuse**: Can referral or signup bonuses be farmed?
> - **Entitlement bypass**: Are premium features checked at access time or only at subscription time?
> - **Transfer/balance logic**: Can negative transfers or self-transfers be made?
> - **Time/date logic**: Are time-limited offers enforced server-side?
> - **Inventory logic**: Is stock validated atomically before reservation?
> - **Automated abuse of sensitive business flows**: Are high-value flows (purchase, booking, referral, content access) protected against bots, scripts, and coordinated abuse?
>
> **Output format** — write to `{{ REPORTS_ROOT }}/13_recon.md`:
>
> ```markdown
> # Business Logic Threat Model: [Project Name]
>
> ## Application Domain
> [2–3 sentence summary of what the application does and its key business features]
>
> ## Business Features Identified
> - [Feature 1]: [brief description, relevant models/endpoints]
> - [Feature 2]: ...
>
> ## Attack Scenarios
>
> ### 1. [Short title, e.g. "Negative quantity purchase for credit"]
> - **Category**: [e.g. Quantity & Numeric Limit Violations]
> - **Target**: [Endpoint or feature, e.g. `POST /api/orders`]
> - **Description**: [What an attacker would do and what outcome they expect]
> - **Relevant code**: [File and line range where the relevant logic lives]
> - **Business rule that should be enforced**: [What the application is supposed to do]
> - **Risk level**: [High / Medium / Low]
>
> ### 2. ...
>
> [Use sequential numbering ### 3., ### 4., ... for every scenario — required for batching in Phase 2.]
>
> ## Categories Not Applicable
> [List any categories from the checklist that are not relevant to this application and why]
> ```

### After Phase 1: Check for Scenarios Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/13_recon.md`. If the recon produced **zero attack scenarios** (the scenario list is empty and every category is listed as not applicable), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/13_businesslogic.md`, **delete** `{{ REPORTS_ROOT }}/13_recon.md`, and stop:

```markdown
# Business Logic Analysis Results

No vulnerabilities found.
```

Only proceed to Phase 2 if Phase 1 produced at least one attack scenario.

### Phase 2: Verify — Check Whether Scenarios Are Vulnerable (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/13_recon.md` and split the attack scenarios into **batches of up to 3 scenarios each**. Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned scenarios and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/13_recon.md` and count the numbered scenario sections (`### 1.`, `### 2.`, etc.).
2. Divide them into batches of up to 3. For example, 8 scenarios → 3 batches (1–3, 4–6, 7–8).
3. For each batch, extract the full text of those scenario sections from the threats file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned scenarios.
5. Each subagent writes to `{{ REPORTS_ROOT }}/13_batch_N.md` where N is the 1-based batch number.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned attack scenario, determine whether the business rule is properly enforced in code or whether the scenario is vulnerable. Our goal is to find business logic vulnerabilities. Write results to `{{ REPORTS_ROOT }}/13_batch_[N].md`.
>
> **Your assigned scenarios** (from the threat modeling phase):
>
> [Paste the full text of the assigned scenario sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand validation patterns, ORM usage, and where business rules are typically enforced. Trace the code paths referenced in each scenario.
>
> **Constraints**: Do not modify project source code. Write findings only to `{{ REPORTS_ROOT }}/13_batch_[N].md`.
>
> **What business logic flaws are NOT** — do not flag these here:
> - **SQL injection, XSS, RCE, XXE, SSRF, SSTI**: separate skills
> - **Missing authentication**: Unauthenticated Access
> - **IDOR**: another access-control class
> - **Generic brute-force** unless it clearly circumvents a business rule
>
> **For each scenario, perform the following checks**:
>
> **1. Is the business rule enforced server-side?**
> - Is the constraint validated in the backend handler, service layer, or ORM/database?
> - Or is it only validated client-side (frontend form validation, JavaScript min/max attributes)?
> - Client-side-only validation = vulnerable.
>
> **2. Is the validation complete and covers all edge cases?**
> - Does it check for negative values where applicable?
> - Does it check upper bounds, not just lower bounds?
> - Does it handle concurrent requests (is the check atomic, or is there a TOCTOU window)?
> - Does it re-validate at the point of use, not just at an earlier step?
>
> **3. For workflow bypass scenarios**:
> - Does each step verify that previous required steps were completed?
> - Are step completion flags stored server-side (not just in a cookie or session that can be replayed)?
> - Can a terminal endpoint be called directly without going through earlier steps?
>
> **4. For coupon/voucher scenarios**:
> - Is the coupon marked as used atomically with the transaction (in the same DB transaction)?
> - Is concurrent redemption protected (SELECT FOR UPDATE, optimistic locking, atomic compare-and-swap)?
> - Is the expiry date checked server-side at redemption time?
>
> **5. For race condition scenarios**:
> - Is stock/balance check and decrement done atomically (in a single DB transaction or with row-level locking)?
> - Is there any idempotency key or deduplication logic to prevent duplicate concurrent requests?
>
> **6. For entitlement/subscription scenarios**:
> - Is the user's current plan/tier checked at the point of feature access?
> - Or is it cached at login/session start and never re-evaluated?
>
> **7. For transfer/balance scenarios**:
> - Is there a server-side check that the transfer amount is positive?
> - Is there a server-side check that the sender has sufficient balance?
> - Are these checks done within a database transaction to prevent race conditions?
>
> **Classification**:
> - **Vulnerable**: The business rule is absent, bypassable, or only enforced client-side.
> - **Likely Vulnerable**: The rule exists but has gaps (race condition window, missing edge case, bypassable condition).
> - **Not Vulnerable**: Proper server-side enforcement exists and covers edge cases.
> - **Needs Manual Review**: Cannot determine with confidence (complex logic, external service dependency, etc.).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/13_batch_[N].md`:
>
> ```markdown
> # Business Logic Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Scenario title
> - **Category**: [Attack category]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path`
> - **Business Rule Violated**: [What rule the application should enforce]
> - **Issue**: [Clear description of what validation is missing or broken]
> - **Impact**: [What an attacker can achieve — free goods, financial loss, unfair advantage, etc.]
> - **Proof**: [Show the code path demonstrating the missing enforcement]
> - **Remediation**: [Specific fix for this scenario]
> - **Dynamic Test**:
>   ```
>   [Step-by-step instructions or curl commands to confirm the finding on the live app.
>    Include exact HTTP method, endpoint, headers, and request body.
>    Describe what response or side effect confirms the vulnerability.]
>   ```
>
> ### [LIKELY VULNERABLE] Scenario title
> - **Category**: [Attack category]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path`
> - **Business Rule Violated**: [What rule should be enforced]
> - **Issue**: [What enforcement gap or race condition exists]
> - **Concern**: [Why this is likely vulnerable despite partial enforcement]
> - **Proof**: [Show the code path with the weak/partial check]
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [Step-by-step instructions or curl commands, e.g. two concurrent requests, to confirm.]
>   ```
>
> ### [NOT VULNERABLE] Scenario title
> - **Category**: [Attack category]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Business Rule**: [What the application is supposed to enforce]
> - **Protection**: [How it is enforced — server-side validation, DB constraint, atomic transaction, etc.]
>
> ### [NEEDS MANUAL REVIEW] Scenario title
> - **Category**: [Attack category]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Uncertainty**: [Why automated analysis couldn't determine the status]
> - **Suggestion**: [What to examine manually or test dynamically]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/13_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/13_businesslogic.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/13_batch_1.md`, `{{ REPORTS_ROOT }}/13_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/13_businesslogic.md` using this format:

```markdown
# Business Logic Analysis Results: [Project Name]

## Executive Summary
- Scenarios analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/13_businesslogic.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/13_batch_*.md`).

***

## References
[ref: #businesslogic-references]

- OWASP API Security Top 10 2023 — API6:2023 Unrestricted Access to Sensitive Business Flows: https://owasp.org/API-Security/editions/2023/en/0xa6-unrestricted-access-to-sensitive-business-flows/
- OWASP Business Logic Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Business_Logic_Security_Cheat_Sheet.html
- OWASP Automated Threats to Web Applications: https://owasp.org/www-project-automated-threats-to-web-applications/
- CWE-841: Improper Enforcement of Behavioral Workflow: https://cwe.mitre.org/data/definitions/841.html
- CWE-770: Allocation of Resources Without Limits or Throttling: https://cwe.mitre.org/data/definitions/770.html
- CWE-20: Improper Input Validation: https://cwe.mitre.org/data/definitions/20.html
- CWE-362: Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition'): https://cwe.mitre.org/data/definitions/362.html
- CWE-408: Incorrect Behavior Order: Early Amplification: https://cwe.mitre.org/data/definitions/408.html
- CWE-691: Insufficient Control Flow Management: https://cwe.mitre.org/data/definitions/691.html
- CWE-1339: Insufficient Precision or Accuracy of a Real Number: https://cwe.mitre.org/data/definitions/1339.html
- CWE-837: Improper Enforcement of a Single, Unique Action: https://cwe.mitre.org/data/definitions/837.html

***

## Important Reminders
[ref: #businesslogic-important-reminders]

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Phase 2 must run **after** Phase 1 completes — it depends on the threat model output.
- Phase 3 must run **after** all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 scenarios per subagent**. If there are 1–3 scenarios total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned scenarios' text from the threats file, not the entire threats file. This keeps each subagent's context small and focused.
- Focus strictly on **business logic flaws** — do not flag injection bugs, auth bypass, or IDOR issues here.
- Threat modeling in Phase 1 should be **application-specific**: generic scenarios not grounded in the actual codebase are not useful.
- Server-side validation is the only valid protection. Client-side validation, frontend form constraints, and API documentation that says "must be positive" are not security controls.
- Race conditions on financial operations are high-severity even if they appear to require exact timing — automated tools (Turbo Intruder, concurrent curl) make them trivial to exploit.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives in a security assessment are worse than false positives.
- Pay attention to ORM and database-level constraints (CHECK constraints, unique indexes, transactions with locking) — these can provide enforcement that is not visible in application code alone.
- **Do not modify project source code.** This reference is read-only. Subagents must write all findings to `{{ REPORTS_ROOT }}/` report files and leave the codebase untouched.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/13_recon.md` and all `{{ REPORTS_ROOT }}/13_batch_*.md` files after the final `{{ REPORTS_ROOT }}/13_businesslogic.md` is written.
