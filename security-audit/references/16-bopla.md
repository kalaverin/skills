# Broken Object Property Level Authorization (BOPLA) Detection

[ref: #bopla-detection]

You are performing a focused security assessment to find Broken Object Property Level Authorization (BOPLA) vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **recon** (find serialization/auto-binding/mass-assignment sites), **batched verify** (check property-level authorization in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

**OWASP mapping**: This scan maps to **API3:2023 – Broken Object Property Level Authorization**.

**Subagent constraint**: All subagents launched by this skill are **read-only**. They must analyze code, write findings to the report files below, and **must never modify project source code**, tests, configuration files, or dependencies. If a finding needs a code change, describe the fix in the report; do not apply it.

---

## What is BOPLA

BOPLA occurs when an API exposes or allows modification of object properties that the authenticated caller should not be able to read or write. It combines two older risks:

- **Excessive Data Exposure** — the API returns sensitive object properties (e.g., `role`, `is_admin`, `password_hash`, `internal_notes`) through generic serialization.
- **Mass Assignment** — the API automatically binds client input to internal object fields, letting the caller overwrite read-only or sensitive properties (e.g., `role=admin`, `is_admin=true`, `total_stay_price=1000000`, `blocked=false`).

The core pattern: *the API uses a whole internal object or generic serializer for an endpoint that should only expose or accept a subset of its properties.*

### What BOPLA IS

- Returning a full ORM model / entity via `to_json()`, `model_to_dict()`, or `res.json(user)` that leaks sensitive fields.
- Updating a record with `User.objects.create(**request.data)`, `Object.assign(doc, req.body)`, or `@RequestBody User user` without an allowlist.
- A request body containing `role`, `is_admin`, `total_stay_price`, `blocked`, or similar fields and the server accepting them.
- GraphQL resolvers returning all object fields by default or mutations writing arbitrary input fields to the backing object.
- PATCH endpoints that accept a partial document and apply it to internal objects without field-level authorization.
- JSON:API sparse fieldsets or GraphQL fragments used to request sensitive fields the client should not see.
- ORM lazy-loading leakage where nested relations expose extra properties because the response serializer traverses them.

### What BOPLA is Not

Do not flag these as BOPLA:

- **IDOR/BOLA**: Changing an object ID to access another user's record — that's object-level authorization, not property-level.
- **Missing authentication**: An endpoint requiring no login at all — that's "Unauthenticated Access".
- **SQL injection**: Untrusted input reaching a SQL query string — that's SQLi.
- **XSS**: Stored scripts later rendered unescaped — that's XSS.
- **Business logic flaws in computed values**: e.g., price calculation logic errors not caused by unauthorized field writes.

### Patterns That Prevent BOPLA

When you see these patterns, the code is likely **not vulnerable**:

**1. Explicit response allowlist / DTO**
```python
return JsonResponse({"id": user.id, "name": user.name})   # only intended fields
```

**2. Explicit request allowlist / strong parameters**
```python
serializer = UserUpdateSerializer(data=request.data)       # fields declared in serializer
```
```ruby
params.require(:user).permit(:name, :email)
```

**3. Schema-based response validation**
- OpenAPI response schemas enforced in tests or by a gateway.
- Marshmallow / pydantic / Joi / Zod / class-validator response objects.

**4. Deny unknown / unexpected fields**
- Serializer configured with `unknown=EXCLUDE` or `raise` (Marshmallow), `additionalProperties: false` (JSON Schema), `@JsonIgnoreProperties(ignoreUnknown = false)`.
- Strong parameters rejecting unpermitted keys.

**5. Separate read and write models / DTOs**
- The request DTO only contains modifiable fields; the response DTO only contains exposable fields.

---

## Vulnerable vs. Secure Examples

### Python — Django

```python
# VULNERABLE: generic serialization leaks password hash and role
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return JsonResponse(model_to_dict(user))   # exposes is_staff, is_superuser, password, etc.

# VULNERABLE: mass assignment accepts any model field
def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    for key, value in request.POST.items():
        setattr(user, key, value)
    user.save()
    # Attacker can send role=admin or is_superuser=1

# SECURE: explicit response fields + explicit update allowlist
from django.forms import model_to_dict

def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    return JsonResponse({"id": user.id, "username": user.username, "email": user.email})

def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    allowed = {"first_name", "last_name", "email"}
    for key in allowed:
        if key in request.POST:
            setattr(user, key, request.POST[key])
    user.save(update_fields=allowed)
```

### Python — Django REST Framework

```python
# VULNERABLE: serializer exposes all model fields by default
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"   # leaks password, is_staff, is_superuser, groups, etc.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# VULNERABLE: update endpoint accepts any writable model field
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # Attacker can PATCH {"total_stay_price": 1000000}

# SECURE: explicit fields, read-only/internal fields excluded, unknown fields rejected
class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        extra_kwargs = {
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "is_superuser": {"read_only": True},
        }

class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["comment"]   # only fields the host may update
        read_only_fields = ["total_stay_price", "approved", "guest", "created_at"]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()

    def get_serializer_class(self):
        if self.action in ["update", "partial_update", "create"]:
            return BookingUpdateSerializer
        return BookingPublicSerializer
```

### Python — Flask / SQLAlchemy

```python
# VULNERABLE: returns full SQLAlchemy object
@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())   # may leak password_hash, role, internal_notes

# VULNERABLE: merges entire JSON body into the model
@app.route('/api/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    user = User.query.get_or_404(user_id)
    for key, value in request.json.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.to_dict())

# SECURE: explicit DTOs / schemas
from marshmallow import Schema, fields, EXCLUDE

class UserResponseSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()

class UserUpdateSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Email()
    class Meta:
        unknown = EXCLUDE   # reject role, is_admin, etc.

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return UserResponseSchema().dump(user)

@app.route('/api/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    user = User.query.get_or_404(user_id)
    data = UserUpdateSchema().load(request.get_json())
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return UserResponseSchema().dump(user)
```

### Node.js — Express / Mongoose

```javascript
// VULNERABLE: returns whole Mongoose document including passwordHash and role
router.get('/api/users/:id', auth, async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user);   // leaks internal fields
});

// VULNERABLE: spreads entire body into update
router.patch('/api/users/:id', auth, async (req, res) => {
  const user = await User.findByIdAndUpdate(
    req.params.id,
    req.body,        // attacker can send role: 'admin' or isAdmin: true
    { new: true }
  );
  res.json(user);
});

// SECURE: explicit projection and $set with allowlist
router.get('/api/users/:id', auth, async (req, res) => {
  const user = await User.findById(req.params.id).select('username email createdAt');
  if (!user) return res.status(404).json({ error: 'Not found' });
  res.json(user);
});

router.patch('/api/users/:id', auth, async (req, res) => {
  const allowed = ['firstName', 'lastName', 'email'];
  const updates = {};
  for (const key of allowed) {
    if (req.body[key] !== undefined) updates[key] = req.body[key];
  }
  const user = await User.findByIdAndUpdate(req.params.id, { $set: updates }, { new: true });
  res.json(user);
});
```

### Java — Spring Boot

```java
// VULNERABLE: returns JPA entity with sensitive fields
@GetMapping("/api/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepo.findById(id).orElseThrow();   // may expose password, role, internalId
}

// VULNERABLE: auto-binds request JSON directly into JPA entity
@PutMapping("/api/users/{id}")
public User updateUser(@PathVariable Long id, @RequestBody User user) {
    user.setId(id);
    return userRepo.save(user);   // attacker can send role, isAdmin, totalStayPrice
}

// SECURE: use DTOs, @JsonView, and explicit field binding
public record UserResponse(Long id, String username, String email) {}
public record UserUpdate(String firstName, String lastName, String email) {}

@GetMapping("/api/users/{id}")
public UserResponse getUser(@PathVariable Long id) {
    User user = userRepo.findById(id).orElseThrow();
    return new UserResponse(user.getId(), user.getUsername(), user.getEmail());
}

@PutMapping("/api/users/{id}")
public UserResponse updateUser(@PathVariable Long id, @RequestBody UserUpdate dto) {
    User user = userRepo.findById(id).orElseThrow();
    user.setFirstName(dto.firstName());
    user.setLastName(dto.lastName());
    user.setEmail(dto.email());
    return new UserResponse(user.getId(), user.getUsername(), user.getEmail());
}
```

### C# — ASP.NET Core

```csharp
// VULNERABLE: returns full EF Core entity with sensitive fields
[HttpGet("/api/users/{id}")]
public User GetUser(int id)
{
    return _db.Users.Find(id);   // exposes PasswordHash, Role, InternalNotes
}

// VULNERABLE: auto-binds request JSON directly into EF Core entity
[HttpPut("/api/users/{id}")]
public User UpdateUser(int id, [FromBody] User user)
{
    user.Id = id;
    _db.Users.Update(user);
    _db.SaveChanges();
    return user;   // attacker can send role=admin or isAdmin=true
}

// VULNERABLE: PATCH merges partial JSON into tracked entity
[HttpPatch("/api/users/{id}")]
public async Task<IActionResult> PatchUser(int id, [FromBody] JsonPatchDocument<User> patch)
{
    var user = await _db.Users.FindAsync(id);
    patch.ApplyTo(user);   // may apply ops to Role, IsAdmin, PasswordHash
    await _db.SaveChangesAsync();
    return Ok(user);
}

// SECURE: explicit response DTO, update DTO, and field-level allowlist
public record UserResponse(int Id, string Username, string Email);
public record UserUpdate(string FirstName, string LastName, string Email);

[HttpGet("/api/users/{id}")]
public ActionResult<UserResponse> GetUser(int id)
{
    var user = _db.Users.Find(id);
    if (user is null) return NotFound();
    return new UserResponse(user.Id, user.Username, user.Email);
}

[HttpPut("/api/users/{id}")]
public ActionResult<UserResponse> UpdateUser(int id, [FromBody] UserUpdate dto)
{
    var user = _db.Users.Find(id);
    if (user is null) return NotFound();
    user.FirstName = dto.FirstName;
    user.LastName = dto.LastName;
    user.Email = dto.Email;
    _db.SaveChanges();
    return new UserResponse(user.Id, user.Username, user.Email);
}

// SECURE PATCH: apply only allowed operations
[HttpPatch("/api/users/{id}")]
public async Task<IActionResult> PatchUser(int id, [FromBody] JsonPatchDocument<UserUpdate> patch)
{
    var user = await _db.Users.FindAsync(id);
    if (user is null) return NotFound();
    var dto = new UserUpdate(user.FirstName, user.LastName, user.Email);
    patch.ApplyTo(dto);
    user.FirstName = dto.FirstName;
    user.LastName = dto.LastName;
    user.Email = dto.Email;
    await _db.SaveChangesAsync();
    return Ok(new UserResponse(user.Id, user.Username, user.Email));
}
```

### Ruby on Rails

```ruby
# VULNERABLE: renders full model including encrypted_password and role
def show
  @user = User.find(params[:id])
  render json: @user
end

# VULNERABLE: updates without strong parameters
def update
  @user = User.find(params[:id])
  @user.update(params[:user])   # attacker can send role, admin, blocked
  render json: @user
end

# SECURE: explicit serialization + strong parameters
def show
  @user = User.find(params[:id])
  render json: @user.as_json(only: [:id, :username, :email])
end

def update
  @user = User.find(params[:id])
  @user.update(user_params)
  render json: @user.as_json(only: [:id, :username, :email])
end

private

def user_params
  params.require(:user).permit(:first_name, :last_name, :email)
end
```

### GraphQL

```python
# VULNERABLE: resolver returns the whole backing object; all fields are selectable
class UserType(graphene.ObjectType):
    class Meta:
        model = User
        fields = "__all__"   # exposes password_hash, role, is_admin

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_user(root, info, id):
        return User.objects.get(id=id)   # caller can request passwordHash

# VULNERABLE: mutation writes arbitrary input fields to the backing object
class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = graphene.JSONString(required=True)

    user = graphene.Field(UserType)

    def mutate(root, info, id, input):
        user = User.objects.get(id=id)
        for key, value in json.loads(input).items():
            setattr(user, key, value)   # attacker can send role, isAdmin
        user.save()
        return UpdateUser(user=user)

# SECURE: explicit field allowlists on types, input objects, and field-level guards
class UserPublicType(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    email = graphene.String()

class UserUpdateInput(graphene.InputObjectType):
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()

class Query(graphene.ObjectType):
    user = graphene.Field(UserPublicType, id=graphene.Int(required=True))

    def resolve_user(root, info, id):
        user = User.objects.get(id=id)
        return user   # only UserPublicType fields are selectable

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserUpdateInput(required=True)

    user = graphene.Field(UserPublicType)

    def mutate(root, info, id, input):
        user = User.objects.get(id=id)
        if not info.context.user.is_authenticated or info.context.user.id != id:
            raise Exception("unauthorized")
        user.first_name = input.first_name
        user.last_name = input.last_name
        user.email = input.email
        user.save()
        return UpdateUser(user=user)
```

---

## Advanced Patterns

Look for these less-obvious BOPLA variants during recon and verification.

### JSON:API sparse fieldsets abuse

APIs that support `?fields[type]=field1,field2` may allow a client to request sensitive fields (e.g., `?fields[user]=password_hash,role`) if the implementation does not enforce a server-side allowlist.

- **Signal**: request parsers that parse `fields[...]` query parameters and pass them directly to a serializer or ORM `.only(...)` call.
- **Check**: is there a server-side allowlist that rejects unknown field names before constructing the field list?

### Nested object mass assignment

A request body may contain nested objects or arrays. If the handler recursively assigns nested properties to related models without filtering, an attacker can overwrite child object fields they should not touch.

```json
{
  "name": "Alice",
  "profile": {
    "bio": "Hi",
    "is_verified": true
  }
}
```

Look for recursive `setattr`, `Object.assign` over nested objects, or nested serializer `create`/`update` methods that accept arbitrary keys.

### GraphQL fragment abuse for sensitive fields

Fragments and inline selections let clients request any field exposed by a type, even if the web UI never uses it. A type that includes `internal_notes`, `ssn`, or `role` is vulnerable unless field-level authorization guards every sensitive field.

- **Check**: does the resolver/object type expose the field at all? If yes and the field is not protected by role checks, it is a finding.
- **Secure pattern**: split into separate public/private types or use field-level `@authorized` guards.

### ORM lazy-loading leakage

A response serializer may implicitly trigger lazy loads of related objects and include them. For example, returning a Django/DRF serializer with `depth = 1` or a Spring entity with `@OneToMany` can expose the related object's sensitive fields.

- **Signal**: serializers with `depth`, `select_related`, `prefetch_related`, `FetchType.EAGER`, or Jackson default serialization of entity relations.
- **Check**: are related objects projected to a DTO, or is the whole related entity serialized?

### PATCH / partial-update abuse

PATCH endpoints and JSON Patch / JSON Merge Patch handlers are high-risk because they are explicitly designed to accept partial updates. If the patch document is applied directly to a persistence entity without an allowlist, the client can modify read-only fields.

- **Signal**: `JsonPatchDocument<T>`, `merge_patch`, `Object.assign(entity, req.body)`, serializers used for both POST and PATCH without `read_only_fields`.
- **Secure pattern**: apply patches to a dedicated update DTO or whitelist, then copy only allowed fields to the entity.

### OpenAPI response schema validation

An OpenAPI document can be used as a response allowlist. If the API gateway or test suite validates that every response matches a published schema that excludes sensitive fields, whole-entity serialization is less likely to leak data.

- **Signal**: tests calling `validate_response(schema, response)`, middleware that compares responses to `components.schemas`, or gateways that strip undeclared fields.
- **Check**: is response validation actually enforced for the endpoint in question, or is the OpenAPI document only documentation?

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Recon — Find Serialization and Mass-Assignment Sites

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where an API response may expose too many object properties, or where client input may be auto-bound/mass-assigned to internal objects. Write results to `{{ REPORTS_ROOT }}/16_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, frameworks, serializers, and request-handling patterns.
>
> **Subagent constraint**: You are read-only. Do not modify project source code, tests, configuration, or dependencies under any circumstances. Record findings in the report only.
>
> **What to search for**:
>
> 1. **Generic serialization / response leakage**:
>    - Returning whole ORM models/entities: `res.json(model)`, `jsonify(obj)`, `render json: @obj`, `model_to_dict(...)`, `to_json`, `to_dict`, `serialize()`
>    - GraphQL resolvers returning full objects by default
>    - Response objects that include fields like `password`, `password_hash`, `role`, `is_admin`, `is_superuser`, `internal_notes`, `blocked`, `total_stay_price`, `secrets`, `tokens`
>
> 2. **Mass assignment / auto-binding of request input**:
>    - Direct spread/merge of request body into a model: `Object.assign(entity, req.body)`, `{ ...req.body }`, `**request.data`, `**request.POST`
>    - ORM create/update with unfiltered input: `Model.create(req.body)`, `Model.update(req.body)`, `user.update(request.json)`, `User.objects.create(**request.POST)`
>    - Framework auto-binding of request JSON to entities: `@RequestBody User user`, `@ModelAttribute`, Rails `update(params)` without `permit`
>    - Serializers/forms that do not explicitly list fields or that allow unknown fields
>
> 3. **Sensitive property writes via request body**:
>    - Request handlers accepting fields such as `role`, `is_admin`, `is_superuser`, `blocked`, `total_stay_price`, `owner_id`, `created_at`, `id`, `password`, `permissions`
>    - Code that iterates `for key in request.body` and assigns to the model
>
> 4. **Weak or missing schema validation**:
>    - Serializers with `unknown=INCLUDE` or no `unknown` setting
>    - JSON Schema without `additionalProperties: false`
>    - Jackson `@JsonIgnoreProperties(ignoreUnknown = true)` on entity used for writes
>
> 5. **Advanced patterns**:
>    - JSON:API sparse fieldsets parsed from query parameters without server-side allowlist
>    - Nested object assignment (recursive spread/merge into child objects)
>    - GraphQL fragment access to sensitive fields, whole-object resolvers, mutations writing arbitrary input
>    - ORM lazy-loading / eager relation leakage
>    - PATCH / JSON Patch endpoints applied directly to persistence entities
>    - OpenAPI response schemas that are documented but not enforced
>
> **What to ignore**:
> - Endpoints that are intentionally public and read-only (e.g., public listings)
> - Admin-only endpoints where admin access is already verified by role-based checks
> - Fields explicitly intended to be user-writable for that endpoint
>
> **Output format** — write to `{{ REPORTS_ROOT }}/16_recon.md`:
>
> ```markdown
> # BOPLA Recon: [Project Name]
>
> ## Summary
> Found [N] candidate sites with potential property-level authorization issues.
>
> ## Candidates
>
> ### 1. [Descriptive name]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Issue type**: [response exposure / mass assignment / both / advanced pattern]
> - **Object / model**: [model name]
> - **Sensitive properties involved**: [e.g., role, is_admin, password_hash]
> - **Code snippet**:
>   ```
>   [relevant code]
>   ```
>
> [Repeat for each candidate]
> ```

### Phase 2: Verify — Check Property-Level Authorization (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/16_recon.md` and split the candidates into **batches of up to 3 candidates each**. Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned candidates and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/16_recon.md` and count the numbered candidate sections (### 1., ### 2., etc.).
2. Divide them into batches of up to 3. For example, 8 candidates → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those candidate sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned candidates.
5. Each subagent writes to `{{ REPORTS_ROOT }}/16_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: Verify the following Broken Object Property Level Authorization (BOPLA) candidates and determine whether the endpoint properly restricts exposed and modifiable object properties. Write results to `{{ REPORTS_ROOT }}/16_batch_[N].md`.
>
> **Your assigned candidates** (from the recon phase):
>
> [Paste the full text of the assigned candidate sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand the serializers, request-handling layer, and authorization patterns.
>
> **Subagent constraint**: You are read-only. Do not modify project source code, tests, configuration, or dependencies under any circumstances. Record findings in the report only.
>
> **BOPLA Reference — What to look for**:
>
> BOPLA occurs when an API:
> 1. Returns sensitive object properties that the caller should not see (excessive data exposure), or
> 2. Allows the caller to write object properties that should be read-only or restricted (mass assignment).
>
> **What BOPLA is NOT** — do not flag these as BOPLA:
> - Changing an object ID to access another user's data → that's IDOR/BOLA
> - Missing authentication on an endpoint → that's Unauthenticated Access
> - Untrusted input in SQL strings → that's SQLi
> - Stored scripts rendered unescaped → that's XSS
>
> **Protection patterns that PREVENT BOPLA** — if you see these, the site is likely safe:
> 1. **Explicit response allowlist / DTO**: only intended fields are returned
> 2. **Explicit request allowlist / strong parameters / serializer fields**: only intended fields are accepted
> 3. **Schema-based response validation**: responses are validated against a schema
> 4. **Deny unknown fields**: serializer/schema rejects unexpected properties
> 5. **Separate read and write DTOs**
> 6. **Field-level guards on GraphQL types and sensitive ORM relations**
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **For each candidate, check**:
>
> 1. **Response exposure**:
>    - Does the response construction use a generic serializer or return the whole entity?
>    - Are sensitive fields (`role`, `is_admin`, `password_hash`, `internal_notes`, `blocked`, `total_stay_price`, etc.) reachable in a normal API response?
>    - Is there a response schema / DTO that strips them?
>
> 2. **Mass assignment / input binding**:
>    - Does the handler accept a request body and assign it wholesale to the model (`**body`, `Object.assign`, `@RequestBody Entity`, `update(params[:user])`)?
>    - Are sensitive fields accepted and persisted if the client sends them?
>    - Is there an allowlist of writable fields (serializer Meta.fields, strong parameters, explicit `$set`, DTO)?
>
> 3. **Unknown-field handling**:
>    - Does the serializer/schema reject unexpected keys, or silently ignore/accept them?
>    - Is `ignoreUnknown=true` or `additionalProperties: true` used on write paths?
>
> 4. **PATCH / partial update abuse**:
>    - Is the PATCH or JSON Patch handler applied directly to a persistence entity?
>    - Is there a dedicated DTO or allowlist that limits which fields the patch can affect?
>
> 5. **GraphQL specifics** (if applicable):
>    - Are all object fields resolvable by default?
>    - Are mutations writing arbitrary input fields to the backing object?
>    - Are sensitive fields protected by type splitting or field-level authorization?
>
> 6. **Advanced patterns**:
>    - JSON:API sparse fieldsets without server-side allowlist
>    - Nested object mass assignment
>    - GraphQL fragment abuse for sensitive fields
>    - ORM lazy-loading / eager relation leakage
>    - OpenAPI response schemas that are documented but not enforced
>
> **Classification**:
> - **Vulnerable**: Sensitive properties are exposed, or client input can overwrite read-only/sensitive properties, with no effective allowlist or schema protection.
> - **Likely Vulnerable**: An allowlist or schema exists but appears incomplete, bypassable, or only partially applied (e.g., ignored for certain content types, or missing on one mutation).
> - **Not Vulnerable**: Explicit response and request allowlists are in place, or the endpoint uses separate read/write DTOs with unknown-field rejection.
> - **Needs Manual Review**: Cannot determine with confidence (e.g., custom serialization framework, complex middleware, authorization delegated to an uninspectable layer).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/16_batch_[N].md`:
>
> ```markdown
> # BOPLA Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / Function**: `METHOD /path` or function name
> - **Issue**: [Clear description of the property-level authorization failure]
> - **Impact**: [What an attacker can do — read sensitive fields, escalate privileges, modify prices, unblock content, etc.]
> - **Proof**: [Show the code path: response construction or input binding that exposes/accepts the sensitive property]
> - **Remediation**: [Specific fix for this endpoint — use a DTO, add an allowlist, enforce schema validation, deny unknown fields]
> - **Dynamic Test**:
>   ```
>   [curl command or step-by-step instructions to confirm this finding on the live app.
>    Include the exact endpoint, HTTP method, headers, and payload.
>    For exposure: show which sensitive field appears in the response.
>    For mass assignment: show the extra field sent and how the response/state changes.]
>   ```
>
> ### [LIKELY VULNERABLE] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / Function**: `METHOD /path` or function name
> - **Issue**: [What's incomplete about the protection]
> - **Impact**: [Why this might still be exploitable]
> - **Proof**: [Show the code path with the partial/weak protection]
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [payload to attempt property exposure or assignment]
>   ```
>
> ### [NOT VULNERABLE] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / Function**: `METHOD /path` or function name
> - **Protection**: [How it's protected — response allowlist, request allowlist, DTOs, schema validation]
>
> ### [NEEDS MANUAL REVIEW] Endpoint name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / Function**: `METHOD /path` or function name
> - **Uncertainty**: [Why automated analysis couldn't determine the status]
> - **Suggestion**: [What to look at manually]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/16_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/16_bopla.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/16_batch_1.md`, `{{ REPORTS_ROOT }}/16_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/16_bopla.md` using this format:

```markdown
# BOPLA Analysis Results: [Project Name]

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
```

5. After writing `{{ REPORTS_ROOT }}/16_bopla.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/16_batch_*.md`).

---

## Prevention Guidance

For every endpoint that handles object properties:

1. **Use explicit allowlists for both response and request fields.**
   - Define exactly which properties each endpoint may expose and which it may accept.
   - Never rely on generic `to_json()`, `model_to_dict()`, or whole-entity serialization.

2. **Use dedicated Data Transfer Objects (DTOs) / serializers / view models.**
   - Separate read DTOs from write DTOs.
   - The write DTO must contain only user-modifiable fields.

3. **Deny unknown / unexpected fields.**
   - Configure serializers/schemas to reject unexpected keys on input.
   - Use `additionalProperties: false` in JSON Schema, `unknown = EXCLUDE/RAISE` in Marshmallow, `@JsonIgnoreProperties(ignoreUnknown = false)` where appropriate, and strong parameters in Rails.
   - In DRF, avoid `fields = "__all__"` on write serializers; prefer explicit field lists and `read_only_fields`.

4. **Harden PATCH and partial-update endpoints.**
   - Do not apply JSON Patch or merge-patch documents directly to persistence entities.
   - Validate patches against a dedicated update DTO or allowlist before copying values to the entity.
   - Treat `partial_update` actions with the same strict field controls as full updates.

5. **Implement schema-based response validation.**
   - Validate that every API response conforms to an approved schema that excludes sensitive internal fields.
   - Enforce the schema in CI, contract tests, or at the gateway — do not rely on documentation alone.

6. **Never bind request bodies directly to persistence entities.**
   - Avoid `@RequestBody User user` with a JPA entity, `Model.create(req.body)`, or `**request.POST` into an ORM model.
   - In ASP.NET Core, use `JsonPatchDocument<UpdateDto>` rather than `JsonPatchDocument<Entity>`.

7. **Mark truly internal fields as non-writable and non-serializable.**
   - Use `@JsonIgnore`, `write_only=True`, `JsonIgnore`, or equivalent controls for secrets and internal state.

8. **Add regression tests that send forbidden fields.**
   - Assert that `role=admin`, `is_admin=true`, `blocked=false`, etc. are rejected or have no effect.
   - Assert that sensitive fields do not appear in responses for each role.

---

## OWASP API Security Top 10 2023 mapping

This scan maps to:

- **API3:2023 – Broken Object Property Level Authorization** — exposing or allowing modification of object properties without proper authorization, as defined in `0xa3-broken-object-property-level-authorization.md`.

---

## References

- OWASP API Security Top 10 2023 — **API3:2023 Broken Object Property Level Authorization (BOPLA)** (`0xa3-broken-object-property-level-authorization.md`): https://owasp.org/API-Security/editions/2023/en/0xa3-broken-object-property-level-authorization/
- OWASP Mass Assignment Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html
- [CWE-213: Exposure of Sensitive Information Due to Incompatible Policies](https://cwe.mitre.org/data/definitions/213.html)
- [CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes](https://cwe.mitre.org/data/definitions/915.html)
- OWASP API Security Top 10 2019 — API3:2019 Excessive Data Exposure: https://owasp.org/API-Security/editions/2019/en/0xa3-excessive-data-exposure/
- OWASP API Security Top 10 2019 — API6:2019 Mass Assignment: https://owasp.org/API-Security/editions/2019/en/0xa6-mass-assignment/

---

## Important Reminders

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- **Subagents must not modify project source code.** They analyze and report only.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 candidates per subagent**. If there are 1-3 candidates total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned candidates' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- Distinguish BOPLA from IDOR/BOLA: BOPLA is about properties of an object, not access to the object itself.
- Focus on both directions: what the API returns (exposure) and what the API accepts (mass assignment).
- Generic serialization is a strong signal; treat whole-entity responses as likely vulnerable until proven otherwise.
- Unknown-field acceptance is a strong signal for mass assignment.
- PATCH / partial-update endpoints and GraphQL whole-object resolvers are high-risk patterns; scrutinize them carefully.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/16_recon.md` and all `{{ REPORTS_ROOT }}/16_batch_*.md` files after the final `{{ REPORTS_ROOT }}/16_bopla.md` is written.
