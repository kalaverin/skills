# IDOR (Insecure Direct Object Reference) Detection

[ref: #idor-detection]

You are performing a focused security assessment to find IDOR vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **recon** (find candidate endpoints), **batched verify** (check authorization in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

---

## Subagent Constraints

Subagents used in this skill are **read-only investigators**. They must **never modify project source code, configuration files, tests, or any repository file**. Subagents may only create and update the audit report files under `{{ REPORTS_ROOT }}/` (`08_recon.md`, `08_batch_*.md`, and `08_idor.md`). If a subagent asks to edit code, reject the request and remind it to document the finding instead.

---

## IDOR, BOLA, and BFLA

The terms **IDOR** and **Broken Object Level Authorization (BOLA)** describe the same class of vulnerability: an application uses a client-supplied identifier to access an object **without verifying that the requesting user is authorized to access that specific object**. OWASP API Security Top 10 2023 calls this risk **API1:2023 – Broken Object Level Authorization (BOLA)**. This file and the scan output still use the name **IDOR** for backwards compatibility.

BOLA is **object-level**: the user is allowed to call the endpoint or function, but can manipulate an object ID to access another user's data (for example, changing `/api/orders/1001` to `/api/orders/1002`).

**Broken Function Level Authorization (BFLA)** is a different, function-level problem: the user is not allowed to invoke an endpoint or function at all (for example, a regular user calling `POST /admin/reset-password`). BFLA is vertical privilege escalation, not IDOR/BOLA. Do not classify BFLA findings under this scan.

> **BFLA cross-reference**: If you discover function-level privilege escalation — e.g., a non-admin user reaching an admin endpoint, or a user invoking a function their role should not allow — route that finding to scan 10 (`[ref: #missingauth-detection]` / `references/10-missingauth.md`), not here. Only object-level authorization bypasses belong in this IDOR/BOLA scan.

## The BOLA Rule

**Every function that uses a client-supplied ID to access a record must perform an object-level authorization check.** Authenticating the caller or verifying that the caller is a valid user is not enough. The code must verify that the caller is authorized to access the specific record identified by the supplied ID.

## What is IDOR

IDOR occurs when an application uses a user-supplied identifier (ID, slug, filename, etc.) to directly access an object **without verifying the requesting user is authorized to access that specific object**. The application authenticates the user but fails to check ownership or permissions on the requested resource.

The core pattern: *authenticated user A can access or modify resources belonging to user B by changing an identifier in the request.*

### What IDOR IS

- Changing `/api/orders/1001` to `/api/orders/1002` and seeing another user's order
- Sending `DELETE /api/documents/555` to delete a document you don't own
- Modifying `{"account_id": 789}` in a request body to transfer money from someone else's account
- Changing a file download parameter `?file_id=42` to access another user's private file
- Updating another user's profile via `PUT /api/users/other-user-id`

### What IDOR is NOT

Do not flag these as IDOR:

- **Missing authentication**: Endpoint requires no login at all → that's "Unauthenticated Access", a different class
- **Broken function-level access control**: Regular user accessing `/admin/dashboard` → that's vertical privilege escalation, not IDOR. Route to scan 10 / `[ref: #missingauth-detection]`.
- **Public resources**: Accessing `/api/posts/123` where posts are intentionally public is not IDOR
- **Parameter tampering on non-object fields**: Changing `role=admin` or `price=0` in a request → that's mass assignment or business logic, not IDOR
- **SQL injection via ID fields**: `?id=1 OR 1=1` → that's SQLi, not IDOR

### Authorization Patterns That Prevent IDOR

When you see these patterns, the endpoint is likely **not vulnerable**:

**1. Query scoped to current user (most common fix)**
```
# The query itself ensures only the user's own records are returned
Order.objects.filter(id=order_id, user=request.user)       # Django
current_user.orders.find(params[:id])                       # Rails
Order.findOne({ _id: orderId, userId: req.user.id })        # Mongoose
SELECT * FROM orders WHERE id = ? AND user_id = ?           # Raw SQL
```

**2. Explicit ownership check after fetch**
```
order = Order.find(order_id)
if order.user_id != current_user.id:
    raise Forbidden
```

**3. Policy / ability / authorization middleware**
```
authorize('view', order)                    # Laravel Policy
can?(:read, @order)                         # CanCanCan (Rails)
@PreAuthorize("@auth.ownsOrder(#orderId)")  # Spring Security
```

**4. Tenant/organization scoping**
```
# Multi-tenant apps that scope all queries to the tenant
tenant = get_current_tenant(request)
Order.objects.filter(id=order_id, tenant=tenant)
```

**5. Centralized authorization architecture**
```
# A single authorization module is invoked by every business function,
# rather than scattering ownership checks across controllers and services.
authz.require(request.user, 'read', resource='order', resource_id=order_id)
```
A consistent, centralized authorization module — invoked from all business functions and backed by explicit grants — is the strongest architectural prevention for BOLA. This is especially important in microservices, where duplicated ownership checks tend to drift and leave gaps. Prefer a dedicated authorization service or library (e.g., Oso, Casbin, SpiceDB, OpenFGA, or an internal policy engine) over ad-hoc checks in each handler.

**6. Unpredictable object identifiers**
Prefer random, non-sequential GUIDs/UUIDs for object IDs. Predictable integer IDs make BOLA easier to exploit, but GUIDs are a defense-in-depth measure, **not** a replacement for authorization checks.

**7. Authorization regression tests**
Write tests that exercise object access with two different users' credentials and each other's object IDs. Fail the build if one user can read, update, or delete another user's object.

### Authorization Anti-Patterns

These patterns look like protection but do **not** prevent IDOR/BOLA:

**A. Comparing the session user ID to a request parameter without verifying object ownership**
```
# INSUFFICIENT: only checks that the request mentions the current user,
# not that the requested object belongs to them.
if request.GET['user_id'] == str(request.user.id):
    order = Order.objects.get(id=order_id)
```
The check validates the wrong thing. An attacker can supply their own `user_id` while changing `order_id`. The authorization decision must use the object's stored ownership field, not a client-supplied user identifier.

**B. Trusting a client-supplied tenant or organization ID**
```
# INSUFFICIENT: tenant_id comes from the request body without server-side verification
Invoice.objects.filter(id=invoice_id, tenant_id=request.data['tenant_id'])
```
If the user can choose any `tenant_id`, the scoping check is bypassable.

**C. Checking authorization only on reads but not writes**
A `GET` endpoint may be scoped while the paired `PUT`, `PATCH`, or `DELETE` endpoint for the same object is not. Every function that uses a client-supplied ID must perform the check, regardless of HTTP method.

---

## Advanced Detection Patterns

Beyond basic route parameters, look for these higher-risk patterns that frequently hide BOLA.

### 1. Predictable identifiers as a detection signal

IDs that are easy to enumerate lower the bar for exploitation and should raise the confidence of a finding:

- Sequential integers: `/api/invoices/1001`, `/api/invoices/1002`
- Short numeric slugs: `/api/orders/42`
- Auto-increment values exposed in JSON: `{ "order_id": 12345 }`
- Predictable timestamps or hashes derived from public data

> **Note**: Random UUIDs/GUIDs are a defense-in-depth mitigation, not a replacement for authorization checks. Do not mark an endpoint safe solely because it uses UUIDs.

**Example**: An endpoint `GET /api/receipts/{receiptId}` accepts a numeric `receiptId`. Even if the value is large, if it is sequential an attacker can iterate over a range and read other users' receipts unless each lookup is scoped to the caller.

### 2. Bulk and export endpoints

Endpoints that operate on collections multiply the impact of a single missing check:

- `GET /api/users/export` — may export all users if not scoped to the caller's tenant/organization.
- `POST /api/reports/bulk_delete` — deleting many objects by ID without per-object ownership checks.
- `POST /api/messages/bulk_read` — marking other users' messages as read.
- GraphQL mutations with list arguments: `deleteReports(reportKeys: [...])`.

**What to verify**: For each item in the bulk input, does the code verify the caller owns it (or is authorized to act on it)? A batch-level check is insufficient if the attacker can include arbitrary object IDs in the list.

### 3. File storage IDOR

File access is a common IDOR variant. Treat any parameter that names or identifies a stored object as a potential object ID:

- `GET /api/download?file_id=...`
- `GET /api/documents?document_key=...`
- `GET /api/files/?path=...`
- Presigned URL parameters (`?signature=...&key=...`) where the key is the access key
- Cloud storage keys passed through the API (`s3://bucket/user-uploads/...`)

**Example**: `GET /api/attachments?file_id=abc123` returns a redirect to S3. If the API accepts any `file_id` and the S3 object is not additionally restricted, an attacker can iterate file IDs and download other users' attachments.

### 4. WebSocket and GraphQL subscription IDOR

Real-time channels may skip object-level checks because the connection is authenticated once at handshake time:

- WebSocket event streams that push data based on a room/channel ID supplied by the client
- GraphQL subscriptions (`subscription { documentUpdates(documentId: "...") }`) that do not re-verify ownership per message
- Socket.IO rooms joined via a user-controlled room name that maps to sensitive objects

**Example**: A chat app lets users join `room:project-123`. If the server adds the socket to the room without checking whether the user is a member of project 123, any authenticated user can subscribe to any project's messages.

### 5. Indirect reference maps

An API may accept a client-supplied lookup key that maps to an internal ID. If the mapping is not authorized, the result is still BOLA:

- `GET /api/shortlinks/{slug}` where `slug` maps to a private resource
- `POST /api/lookup` with `{ "reference": "INV-2024-001" }` that resolves to an invoice
- Hash IDs or encoded values (`hashid`) that obscure but do not authorize access

**Example**: `GET /api/public-forms/{formSlug}` returns a form by slug. If slugs are guessable and the form is not marked public, an attacker can enumerate slugs to access private forms.

---

## Vulnerable vs. Secure Examples

### Python — Django

```python
# VULNERABLE: fetches any order by ID, no ownership check
def get_order(request, order_id):
    order = Order.objects.get(id=order_id)
    return JsonResponse(model_to_dict(order))

# SECURE: query scoped to requesting user
def get_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return JsonResponse(model_to_dict(order))
```

### Python — Flask / SQLAlchemy

```python
# VULNERABLE
@app.route('/api/documents/<int:doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    return jsonify(doc.serialize())

# SECURE
@app.route('/api/documents/<int:doc_id>')
@login_required
def get_document(doc_id):
    doc = Document.query.filter_by(id=doc_id, owner_id=current_user.id).first_or_404()
    return jsonify(doc.serialize())
```

### Node.js — Express / Mongoose

```javascript
// VULNERABLE
router.get('/api/orders/:id', auth, async (req, res) => {
  const order = await Order.findById(req.params.id);
  res.json(order);
});

// SECURE
router.get('/api/orders/:id', auth, async (req, res) => {
  const order = await Order.findOne({ _id: req.params.id, userId: req.user.id });
  if (!order) return res.status(404).json({ error: 'Not found' });
  res.json(order);
});
```

### Node.js — Express / Prisma

```javascript
// VULNERABLE
router.get('/api/invoices/:id', auth, async (req, res) => {
  const invoice = await prisma.invoice.findUnique({ where: { id: req.params.id } });
  res.json(invoice);
});

// SECURE
router.get('/api/invoices/:id', auth, async (req, res) => {
  const invoice = await prisma.invoice.findFirst({
    where: { id: req.params.id, userId: req.user.id }
  });
  if (!invoice) return res.status(404).json({ error: 'Not found' });
  res.json(invoice);
});
```

### Ruby on Rails

```ruby
# VULNERABLE
def show
  @order = Order.find(params[:id])
end

# SECURE
def show
  @order = current_user.orders.find(params[:id])
end
```

### Java — Spring Boot

```java
// VULNERABLE
@GetMapping("/api/accounts/{id}")
public Account getAccount(@PathVariable Long id) {
    return accountRepo.findById(id).orElseThrow();
}

// SECURE
@GetMapping("/api/accounts/{id}")
public Account getAccount(@PathVariable Long id, Authentication auth) {
    Account acct = accountRepo.findById(id).orElseThrow();
    if (!acct.getOwnerId().equals(auth.getName()))
        throw new AccessDeniedException("Forbidden");
    return acct;
}
```

### Go

```go
// VULNERABLE
func GetOrder(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    order, _ := db.GetOrder(id)
    json.NewEncoder(w).Encode(order)
}

// SECURE
func GetOrder(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    userID := r.Context().Value("userID").(string)
    order, _ := db.GetOrderByUser(id, userID)
    json.NewEncoder(w).Encode(order)
}
```

### PHP — Laravel

```php
// VULNERABLE
public function show($id) {
    return Invoice::findOrFail($id);
}

// SECURE (scoped query)
public function show($id) {
    return auth()->user()->invoices()->findOrFail($id);
}

// SECURE (policy)
public function show($id) {
    $invoice = Invoice::findOrFail($id);
    $this->authorize('view', $invoice);
    return $invoice;
}
```

### C# — ASP.NET Core

```csharp
// VULNERABLE
[HttpGet("api/profiles/{id}")]
public async Task<IActionResult> GetProfile(int id) {
    var profile = await _db.Profiles.FindAsync(id);
    return Ok(profile);
}

// SECURE
[HttpGet("api/profiles/{id}")]
public async Task<IActionResult> GetProfile(int id) {
    var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
    var profile = await _db.Profiles.FirstOrDefaultAsync(p => p.Id == id && p.UserId == userId);
    if (profile == null) return NotFound();
    return Ok(profile);
}
```

### GraphQL — Batch object lookups and mutations

```javascript
// VULNERABLE: mutation trusts reportKeys and deletes without ownership checks
const resolvers = {
  Mutation: {
    deleteReports: async (_, { reportKeys }, { user }) => {
      await Report.deleteMany({ key: { $in: reportKeys } });
      return { ok: true };
    },
  },
};

// VULNERABLE: batch query returns objects by ID without verifying ownership
const resolvers = {
  Query: {
    reports: async (_, { ids }, { user }) => {
      return await Report.find({ _id: { $in: ids } });
    },
  },
};
```

```javascript
// SECURE: verify each requested object belongs to the caller
const resolvers = {
  Mutation: {
    deleteReports: async (_, { reportKeys }, { user }) => {
      const allowed = await Report.find({ key: { $in: reportKeys }, ownerId: user.id });
      if (allowed.length !== reportKeys.length) throw new ForbiddenError('Forbidden');
      await Report.deleteMany({ key: { $in: reportKeys }, ownerId: user.id });
      return { ok: true };
    },
  },
  Query: {
    reports: async (_, { ids }, { user }) => {
      return await Report.find({ _id: { $in: ids }, ownerId: user.id });
    },
  },
};
```

OWASP API1:2023 gives the `deleteReports(reportKeys: [...])` mutation as a classic BOLA example: a user can delete another user's documents because the API trusts the supplied keys and deletes the matching records without verifying ownership. Treat every resolver that uses a client-supplied ID the same way you would a REST endpoint.

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Recon — Find Candidate Endpoints

Launch a subagent with the following instructions:

> **Goal**: Find every endpoint, controller action, or handler that retrieves, modifies, or deletes a specific object using a user-supplied identifier. Write results to `{{ REPORTS_ROOT }}/08_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, frameworks, route definitions, and data access patterns.
>
> **Constraints**: You are a read-only investigator. Do not modify any project source code, configuration, or tests. Only write to `{{ REPORTS_ROOT }}/08_recon.md`.
>
> **What to search for**:
>
> 1. **Route definitions** that contain ID parameters:
>    - Path parameters: `:id`, `{id}`, `<int:id>`, `[id]`
>    - Search patterns: route/path/endpoint definitions with parameter placeholders
>
> 2. **Controller/handler methods** that accept ID arguments and use them to fetch or mutate objects:
>    - ORM lookups: `find(id)`, `findById()`, `get(id=)`, `objects.get()`, `findOne()`, `findUnique()`, `findFirst()`, `query.get()`, `where(id:)`
>    - Raw queries: `SELECT ... WHERE id = ?`, etc.
>    - Also look for delete, update operations with user-supplied IDs
>
> 3. **Request body or query parameter IDs** used in operations:
>    - `req.body.userId`, `req.query.id`, `request.data['account_id']`, etc.
>
> 4. **GraphQL resolvers and mutations** that accept ID arguments
>
> 5. **File/resource access by user-supplied path or filename** (e.g., `?file_id=...`, `?document_key=...`, `?path=...`)
>
> 6. **Bulk/export endpoints** that operate on collections: `export`, `bulk_delete`, `bulk_update`, etc.
>
> 7. **WebSocket/GraphQL subscriptions** that use client-supplied room, channel, or object IDs
>
> 8. **Indirect reference maps** where a client-supplied slug, code, or reference maps to an internal object ID
>
> **What to ignore**:
> - Endpoints that are intentionally public (no auth required by design)
> - Admin-only endpoints behind role-based checks (these are a different class; route BFLA to scan 10 / `[ref: #missingauth-detection]`)
> - Endpoints where the only ID used is the authenticated user's own ID (e.g., `GET /api/me/profile`)
> - Static asset serving
>
> **Output format** — write to `{{ REPORTS_ROOT }}/08_recon.md`:
>
> ```markdown
> # IDOR Recon: [Project Name]
>
> ## Summary
> Found [N] candidate endpoints that use user-supplied identifiers to access objects.
>
> ## Candidates
>
> ### 1. [Descriptive name]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path/:param`
> - **Identifier source**: [path param / query param / body field]
> - **Operation**: [read / update / delete]
> - **Object accessed**: [model/table name]
> - **Code snippet**:
>   ```
>   [relevant code]
>   ```
>
> [Repeat for each candidate]
> ```

### Phase 2: Verify — Check Authorization (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/08_recon.md` and split the candidates into **batches of up to 3 candidates each**. Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned candidates and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/08_recon.md` and count the numbered candidate sections (### 1., ### 2., etc.).
2. Divide them into batches of up to 3. For example, 8 candidates → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those candidate sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned candidates.
5. Each subagent writes to `{{ REPORTS_ROOT }}/08_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project uses Node.js/Express with Prisma, include only the "Node.js — Express / Prisma" and "Node.js — Express / Mongoose" examples. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: Verify the following IDOR (Insecure Direct Object Reference) candidates and determine whether adequate authorization checks exist. Our goal is to find IDOR vulnerabilities. Write results to `{{ REPORTS_ROOT }}/08_batch_[N].md`.
>
> **Your assigned candidates** (from the recon phase):
>
> [Paste the full text of the assigned candidate sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand the auth mechanism, middleware stack, and ORM patterns.
>
> **Constraints**: You are a read-only investigator. Do not modify any project source code, configuration, or tests. Only write to `{{ REPORTS_ROOT }}/08_batch_[N].md`.
>
> **IDOR Reference — What to look for**:
>
> IDOR occurs when an authenticated user can access or modify resources belonging to another user by changing an identifier in the request. Focus on **horizontal privilege escalation** (user-to-user).
>
> **What IDOR is NOT** — do not flag these as IDOR:
> - **Missing authentication**: Endpoint requires no login at all → that's "Unauthenticated Access", not IDOR
> - **Broken function-level access control**: Regular user accessing `/admin/dashboard` → that's vertical privilege escalation, not IDOR. Route to scan 10 / `[ref: #missingauth-detection]`.
> - **Public resources**: Accessing `/api/posts/123` where posts are intentionally public is not IDOR
> - **Parameter tampering on non-object fields**: Changing `role=admin` or `price=0` → that's mass assignment or business logic, not IDOR
> - **SQL injection via ID fields**: `?id=1 OR 1=1` → that's SQLi, not IDOR
>
> **Authorization patterns that PREVENT IDOR** — if you see these, the endpoint is likely safe:
> 1. **Query scoped to current user**: The query filters by the authenticated user's ID (e.g., `WHERE id = ? AND user_id = ?`, `current_user.orders.find(id)`, `Order.findOne({ _id: id, userId: req.user.id })`, `Order.objects.filter(id=order_id, user=request.user)`)
> 2. **Explicit ownership check after fetch**: Code fetches the object then compares `resource.user_id == current_user.id` before returning
> 3. **Policy / ability / authorization middleware**: Framework authorization like `authorize('view', order)`, `can?(:read, @order)`, `@PreAuthorize("@auth.ownsOrder(#orderId)")`
> 4. **Tenant/organization scoping**: All queries scoped to the current tenant/org
> 5. **Centralized authorization module**: A single authorization service or library invoked consistently across business functions
>
> **Advanced patterns to double-check**:
> - **Predictable IDs**: sequential integers, short slugs, or auto-increment values make enumeration trivial
> - **Bulk/export endpoints**: `export`, `bulk_delete`, `bulk_update` — verify per-item ownership, not just a batch gate
> - **File storage IDOR**: `?file_id=...`, `?document_key=...`, `?path=...` — treat storage keys as object IDs
> - **WebSocket / GraphQL subscription IDOR**: real-time channels joined via client-supplied IDs
> - **Indirect reference maps**: client-supplied slugs/codes that map to internal IDs without authorization
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **For each candidate endpoint, check**:
>
> 1. **Is the database query scoped to the authenticated user?**
>    - Does the query include a `user_id` / `owner_id` / `tenant_id` filter matching the current user?
>    - Is the query done through an association (e.g., `current_user.orders.find(id)`)?
>
> 2. **Is there an explicit ownership/permission check after fetching?**
>    - Does the code compare `resource.user_id == current_user.id` (or equivalent)?
>    - Is there a policy/ability/authorization check?
>
> 3. **Is there authorization middleware applied to this route?**
>    - Is there middleware that verifies object ownership before the handler runs?
>    - Trace the middleware chain — don't assume a middleware name implies it checks ownership
>
> 4. **For mutations (update/delete), are the same checks present?**
>    - Sometimes read endpoints are protected but write endpoints are not
>
> 5. **Edge cases to check**:
>    - Does the auth check exist but only run conditionally (e.g., skipped for certain content types)?
>    - Is the check present in one branch of an if/else but missing in another?
>    - Can the check be bypassed by sending the ID in an alternative field?
>    - Are bulk/batch endpoints checked per-item or just at the batch level?
>
> **Classification**:
> - **Vulnerable**: No authorization check found for the specific object. User A can access User B's resources.
> - **Likely Vulnerable**: Auth check exists but appears incomplete, bypassable, or conditional.
> - **Not Vulnerable**: Proper authorization check is in place.
> - **Needs Manual Review**: Cannot determine with confidence (e.g., complex middleware chain, authorization happens in a service layer that's hard to trace).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/08_batch_[N].md`:
>
> ```markdown
> # IDOR Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path/:param`
> - **Issue**: [Clear description of what's missing]
> - **Impact**: [What an attacker can do — read other users' X, delete other users' Y, etc.]
> - **Proof**: [Show the code path — from route to DB query — highlighting the missing check]
> - **Remediation**: [Specific fix for this endpoint]
> - **Dynamic Test**:
>   ```
>   [curl command or step-by-step instructions to confirm this finding on the live app.
>    Include the exact endpoint, HTTP method, headers, and what to look for in the response.
>    Use placeholder tokens like <USER_B_TOKEN> and <USER_A_RESOURCE_ID>.]
>   ```
>
> ### [LIKELY VULNERABLE] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path/:param`
> - **Issue**: [What's incomplete about the check]
> - **Concern**: [Why this might still be exploitable]
> - **Proof**: [Show the code path with the weak/partial check]
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [curl command or step-by-step instructions to confirm this finding on the live app.
>    Include the exact endpoint, HTTP method, headers, and what to look for in the response.
>    Use placeholder tokens like <USER_B_TOKEN> and <USER_A_RESOURCE_ID>.]
>   ```
>
> ### [NOT VULNERABLE] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path/:param`
> - **Protection**: [How it's protected — scoped query / ownership check / policy]
>
> ### [NEEDS MANUAL REVIEW] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint**: `METHOD /path/:param`
> - **Uncertainty**: [Why automated analysis couldn't determine the status]
> - **Suggestion**: [What to look at manually]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/08_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/08_idor.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/08_batch_1.md`, `{{ REPORTS_ROOT }}/08_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/08_idor.md` using this format:

```markdown
# IDOR Analysis Results: [Project Name]

## Executive Summary
- Candidates analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]

## Real-World Impact References

The following OWASP API1:2023 attack scenarios illustrate the business impact of BOLA findings like those above:

1. **Shop revenue charts** (`/shops/{shopName}/revenue_data.json`): A predictable, user-supplied shop identifier grants access to other tenants' sales data.
2. **Vehicle remote-control API**: The API accepts a Vehicle Identification Number (VIN) but fails to verify that the VIN belongs to the logged-in owner, allowing remote control of another user's vehicle.
3. **Document storage GraphQL mutation** (`deleteReports(reportKeys: [...])`): A user can delete another user's documents because the mutation trusts supplied keys without verifying ownership.

Use these scenarios when describing impact and when designing dynamic validation tests.
```

5. After writing `{{ REPORTS_ROOT }}/08_idor.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/08_batch_*.md`).

---

## Dynamic Test Ideas

When writing the dynamic test for a finding, model it on these real-world BOLA patterns from OWASP API1:2023:

- **Predictable ID enumeration**: Log in as User A, capture a resource ID, then log in as User B and request the same ID. Sequential integers or short slugs make this easy to automate.
- **Tenant/shop boundary crossing**: Replace a tenant-scoped identifier (e.g., `shopName`) with another tenant's identifier and observe whether the API returns foreign data.
- **Vehicle / device ownership bypass**: Supply an object identifier (e.g., VIN, device serial) that belongs to another user and verify the API rejects the action.
- **GraphQL document deletion**: Send a mutation with another user's document/report keys and confirm whether the operation is rejected or succeeds.

Example curl template:

```bash
# As User B, attempt to access a resource owned by User A
curl -H "Authorization: Bearer <USER_B_TOKEN>" \
     https://<host>/api/resources/<USER_A_RESOURCE_ID>
```

If the response contains User A's data (or a success response to a mutation on User A's object), the finding is confirmed.

---

## References

- OWASP API Security Top 10 2023 — **API1:2023 Broken Object Level Authorization (BOLA)**: https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/
- OWASP API Security Top 10 2023 — **API5:2023 Broken Function Level Authorization (BFLA)**: https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/
- [CWE-285: Improper Authorization](https://cwe.mitre.org/data/definitions/285.html)
- [CWE-639: Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html)
- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP Authorization Testing Automation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Testing_Automation_Cheat_Sheet.html

---

## Important Reminders

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 candidates per subagent**. If there are 1-3 candidates total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned candidates' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- Focus on **horizontal privilege escalation** (user-to-user). Vertical escalation (user-to-admin) is a different skill.
- Function-level privilege escalation findings belong to scan 10 / `[ref: #missingauth-detection]` — do not classify them here.
- Subagents are read-only. They must **never modify project source code or configuration**; they may only write audit report files under `{{ REPORTS_ROOT }}/`.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Trace the full code path: route → middleware → controller → service → data access. Authorization can happen at any layer.
- Pay attention to framework conventions. In Rails, `current_user.orders.find(id)` is safe. In Express, just having `auth` middleware doesn't mean ownership is checked.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/08_recon.md` and all `{{ REPORTS_ROOT }}/08_batch_*.md` files after the final `{{ REPORTS_ROOT }}/08_idor.md` is written.
