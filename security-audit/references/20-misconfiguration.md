# Security Misconfiguration Detection

[ref: #misconfiguration-detection]

You are performing a focused security assessment to find **security misconfiguration** vulnerabilities in a codebase and its deployment configuration. This skill uses a three-phase approach with subagents: **recon** (find configuration files, header definitions, error handlers, and dependency manifests), **batched verify** (check each misconfiguration indicator in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

---

## OWASP Mapping

This scan maps to **API8:2023 – Security Misconfiguration** from the OWASP API Security Top 10 2023.

Security misconfiguration can occur at any layer of the API stack: network, platform, web server, container orchestrator, framework, or application code. It includes missing hardening, insecure defaults, unnecessary features, missing security headers, permissive CORS, inconsistent TLS, verbose error messages, and unpatched or outdated components.

### OWASP Risk Summary

| Threat agents / Attack vectors | Security Weakness | Impacts |
|---|---|---|
| API Specific: Exploitability **Easy** | Prevalence **Widespread**: Detectability **Easy** | Technical **Severe**: Business Specific |
| Attackers look for unpatched flaws, common endpoints, services with insecure defaults, or unprotected files and directories. | Misconfiguration can happen at any level of the API stack, from the network to the application. Automated tools can detect and exploit unnecessary services or legacy options. | Misconfigurations expose sensitive user data and system details that can lead to full server compromise. |

### Is the API Vulnerable?

API8:2023 says the API is likely vulnerable when any of the following are true:

- Security hardening is missing across any part of the API stack, or cloud-service permissions are improperly configured.
- The latest security patches are missing, or systems are out of date.
- Unnecessary features are enabled (e.g., HTTP verbs, logging features).
- Incoming requests are processed inconsistently across servers in the HTTP chain.
- TLS is missing or inconsistently applied.
- Security or cache-control directives are not sent to clients.
- CORS policy is missing or improperly set.
- Error messages include stack traces or expose other sensitive information.

---

## What to Look For

### Missing Security Headers

APIs and web applications should send security headers that reduce the attack surface for clients. At minimum, check for:

- **Strict-Transport-Security (HSTS)** — Enforces HTTPS for a defined period.
- **X-Content-Type-Options: nosniff** — Prevents MIME-type sniffing.
- **X-Frame-Options** or CSP `frame-ancestors` — Prevents clickjacking via framing.
- **Content-Security-Policy** — Restricts script/style sources and other resource loads.

Also check for **Cache-Control** and **Pragma** headers on sensitive responses. Missing cache directives can cause private data to be stored in browser or intermediate caches.

### Overly Permissive CORS

A CORS policy that allows arbitrary origins (`*`), permits credentials with wildcard origins, or reflects the request `Origin` header without validation can let attacker-controlled websites make authenticated cross-origin requests.

### Missing or Inconsistent TLS

All API communications, including internal service-to-service traffic, should use TLS. Look for:

- Hard-coded `http://` URLs or disabled certificate validation.
- Weak TLS versions or cipher suites (e.g., TLS 1.0/1.1).
- Missing HSTS or mixed-content behavior.
- Inconsistent TLS termination across proxies, load balancers, and backend servers.

### Verbose Error Messages and Stack Traces

Error responses that include stack traces, SQL snippets, internal paths, framework versions, or detailed debug information help attackers understand the system and craft targeted attacks.

### Unnecessary HTTP Verbs and Features

Enable only the HTTP methods and features the endpoint actually needs. Extra verbs (e.g., `TRACE`, `OPTIONS`, `HEAD`, `PUT`, `DELETE`) and debug endpoints increase the attack surface.

### Insecure Defaults in Frameworks, Orchestration, and Cloud Services

Frameworks and platforms often ship with unsafe defaults. Look for:

- Debug mode enabled in production (`DEBUG=True`, `NODE_ENV=development`, `app.run(debug=True)`).
- Default credentials, admin accounts, or tokens.
- Containers running as root, privileged containers, or missing resource limits.
- Overly permissive IAM roles, bucket ACLs, or network security groups.
- Wide `allow`/`deny` rules in firewalls, ingress, or service mesh.

### Missing Patches and Outdated Components

Dependency manifests, base images, and package lists should not contain known-vulnerable versions. Look for:

- Old framework, server, or library versions.
- Base images with known CVEs.
- Missing lockfile or manifest updates.

### Log4j-Style JNDI / Lookup Injection (OWASP Scenario #1)

A logging utility with placeholder expansion and JNDI lookups enabled by default can turn a logged request header into remote code execution. Look for:

- Logging libraries with JNDI/lookup features enabled (Log4j 2.x before 2.17.0, Logback, etc.).
- Request headers, query parameters, or bodies logged without sanitization.
- Permissive outbound network policies that let the server reach attacker-controlled LDAP/RMI/DNS servers.
- Usage of message lookup patterns such as `${jndi:ldap://...}`, `${env:...}`, or `${sys:...}` in log formats or logged data.

### Missing Cache-Control on Sensitive Responses (OWASP Scenario #2)

Private API responses that lack cache directives can be stored by browsers or intermediate proxies. Verify that endpoints returning PII, authentication tokens, private messages, health records, or session data send `Cache-Control: no-store` (and ideally `Pragma: no-cache` for HTTP/1.0 compatibility).

### HTTP Request Smuggling / Desync (CWE-444)

Inconsistent interpretation of HTTP requests across the server chain can lead to request smuggling or desync attacks. Recon should flag:

- Conflicting `Content-Length` and `Transfer-Encoding` handling.
- Header normalization differences (e.g., case, whitespace, folded headers) between proxies and backends.
- Path or encoding inconsistencies (`..;foo/bar`, `%2f`, chunk extensions).
- Front-end and back-end using different HTTP parsers or timeout policies.

### Cloud-Native and Infrastructure-as-Code Misconfigurations

Cloud and IaC templates frequently contain unsafe defaults. Check:

- S3 bucket ACLs or policies granting public read/write access.
- IAM policies with wildcard actions (`*`) or resources (`*`).
- Security group rules allowing `0.0.0.0/0` to sensitive ports.
- Unencrypted storage, databases, or queues.
- Missing logging, monitoring, or versioning on storage buckets.
- Default VPC settings or public subnets used unintentionally.

### Content-Type and Data-Format Restrictions

Restrict incoming content types and data formats to those the endpoint actually requires. Look for:

- Endpoints accepting `*/*` or arbitrary content types.
- Missing content-type validation or deserialization of untrusted formats.
- Unnecessary request parsers (XML, YAML, pickle, Java serialization) enabled.

### Missing OpenAPI / JSON Schema Validation

Define and enforce response payload schemas, including error responses. Look for:

- No OpenAPI, JSON Schema, or protobuf schema defining responses.
- Error handlers that return unvalidated objects, stack traces, or exception details.
- Schema validation disabled or bypassed in production.

### Verbose or Debug Logging Features

Unnecessary logging features can leak sensitive data or expand untrusted input. Look for:

- Debug-level logging in production.
- Request or response bodies logged verbatim, including credentials, tokens, or PII.
- Verbose exception pages (`Whitelabel Error Page`, Django debug page, ASP.NET `UseDeveloperExceptionPage`).
- Logging of raw SQL queries, internal paths, or environment variables.

---

## Vulnerable vs. Secure Examples

### Python — Flask

```python
# VULNERABLE: permissive CORS, debug mode, no security headers, verbose errors
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

@app.route("/api/orders/<int:order_id>")
def get_order(order_id):
    return jsonify({"id": order_id})

if __name__ == "__main__":
    app.run(debug=True)

# SECURE: restricted CORS, production debug off, security headers, generic errors
from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = False
CORS(app, resources={r"/api/*": {"origins": "https://app.example.com"}})

@app.after_request
def set_headers(response):
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.errorhandler(Exception)
def handle_error(e):
    app.logger.exception("Unhandled error")
    return jsonify({"error": "Internal server error"}), 500
```

### Python — Django

```python
# VULNERABLE: debug on, all hosts allowed, all CORS origins, weak TLS settings
# settings.py
DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# SECURE: hardened production settings
# settings.py
DEBUG = False
ALLOWED_HOSTS = ["api.example.com"]
CORS_ALLOWED_ORIGINS = ["https://app.example.com"]
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Python — FastAPI

```python
# VULNERABLE: permissive CORS, debug exception pages, no security headers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def debug_handler(request, exc):
    return {"error": str(exc), "traceback": __import__("traceback").format_exc()}

@app.get("/api/users/me")
def read_user_me():
    return {"id": 1, "email": "user@example.com"}

# SECURE: restricted CORS, generic errors, security headers
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(debug=False)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.exception_handler(Exception)
async def generic_handler(request, exc):
    return JSONResponse(status_code=500, content={"error": "Internal server error"})
```

### Node.js — Express

```javascript
// VULNERABLE: no Helmet, wildcard CORS, detailed error stack, HTTP only
const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors({ origin: "*" }));

app.get("/api/orders/:id", (req, res) => {
  throw new Error("Database connection failed: " + req.params.id);
});

app.use((err, req, res, next) => {
  res.status(500).json({ error: err.message, stack: err.stack });
});

app.listen(3000);

// SECURE: Helmet, restricted CORS, generic errors, HTTPS enforcement
const express = require("express");
const helmet = require("helmet");
const cors = require("cors");

const app = express();
app.use(helmet());
app.use(cors({ origin: "https://app.example.com", credentials: true }));

app.get("/api/orders/:id", (req, res) => {
  // ...
});

app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ error: "Internal server error" });
});

// require HTTPS in production
if (process.env.NODE_ENV === "production") {
  app.use((req, res, next) => {
    if (req.headers["x-forwarded-proto"] !== "https") {
      return res.redirect(301, "https://" + req.headers.host + req.url);
    }
    next();
  });
}
```

### Java — Spring Boot

```java
// VULNERABLE: CORS allows all origins, debug logging, no cache control
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("*")
                .allowedMethods("*")
                .allowCredentials(true);
    }
}

// application.properties
logging.level.org.springframework.web=DEBUG
server.error.include-stacktrace=always

// SECURE: restricted CORS, generic errors, security headers
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .headers(headers -> headers
                .httpStrictTransportSecurity(hsts -> hsts.includeSubDomains(true).maxAgeInSeconds(31536000))
                .contentTypeOptions()
                .frameOptions(frame -> frame.deny())
                .contentSecurityPolicy(csp -> csp.policyDirectives("default-src 'self'"))
            )
            .cors(cors -> cors.configurationSource(corsConfigurationSource()));
        return http.build();
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(List.of("https://app.example.com"));
        config.setAllowedMethods(List.of("GET", "POST"));
        config.setAllowCredentials(true);
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/api/**", config);
        return source;
    }
}

// application.properties
server.error.include-stacktrace=never
server.error.include-message=never
logging.level.org.springframework.web=WARN
```

### C# — ASP.NET Core

```csharp
// VULNERABLE: developer exception page, permissive CORS, no HSTS
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseDeveloperExceptionPage();
app.UseCors(policy => policy.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());

app.MapGet("/api/users/{id}", (int id) => new { id, email = "user@example.com" });

app.Run();

// SECURE: production exception handling, restricted CORS, HSTS, security headers
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseCors(policy => policy
    .WithOrigins("https://app.example.com")
    .WithMethods("GET", "POST")
    .WithHeaders("Authorization", "Content-Type")
    .AllowCredentials());

app.Use(async (context, next) =>
{
    context.Response.Headers.Append("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Append("X-Frame-Options", "DENY");
    context.Response.Headers.Append("Content-Security-Policy", "default-src 'self'");
    context.Response.Headers.Append("Cache-Control", "no-store");
    await next();
});

app.MapGet("/error", () => Results.Json(new { error = "Internal server error" }, statusCode: 500));
app.MapGet("/api/users/{id}", (int id) => new { id, email = "user@example.com" });

app.Run();
```

### Ruby on Rails

```ruby
# VULNERABLE: debug on, permissive CORS, verbose errors
# config/environments/production.rb
Rails.application.configure do
  config.consider_all_requests_local = true
  config.log_level = :debug
end

# config/initializers/cors.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins "*"
    resource "*", headers: :any, methods: :any
  end
end

# SECURE: production mode, restricted CORS, security headers
# config/environments/production.rb
Rails.application.configure do
  config.consider_all_requests_local = false
  config.log_level = :warn
  config.force_ssl = true
  config.ssl_options = { hsts: { expires: 1.year, subdomains: true } }
end

# config/initializers/cors.rb
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins "https://app.example.com"
    resource "/api/*", headers: :any, methods: [:get, :post], credentials: true
  end
end

# config/initializers/security_headers.rb
Rails.application.config.content_security_policy do |policy|
  policy.default_src :self
end

Rails.application.config.action_dispatch.default_headers.merge!(
  "X-Content-Type-Options" => "nosniff",
  "X-Frame-Options" => "DENY",
  "Cache-Control" => "no-store"
)
```

### Go

```go
// VULNERABLE: permissive CORS, no security headers, verbose errors
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

func main() {
    http.HandleFunc("/api/orders/", func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Credentials", "true")
        w.WriteHeader(http.StatusOK)
        json.NewEncoder(w).Encode(map[string]string{"id": r.URL.Path})
    })

    http.HandleFunc("/error", func(w http.ResponseWriter, r *http.Request) {
        http.Error(w, "panic: "+r.URL.Query().Get("msg"), http.StatusInternalServerError)
    })

    log.Fatal(http.ListenAndServe(":8080", nil))
}

// SECURE: restricted CORS, security headers, generic errors
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

func secureHeaders(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        w.Header().Set("X-Content-Type-Options", "nosniff")
        w.Header().Set("X-Frame-Options", "DENY")
        w.Header().Set("Content-Security-Policy", "default-src 'self'")
        w.Header().Set("Cache-Control", "no-store")
        next.ServeHTTP(w, r)
    })
}

func cors(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        origin := r.Header.Get("Origin")
        if origin == "https://app.example.com" {
            w.Header().Set("Access-Control-Allow-Origin", origin)
            w.Header().Set("Access-Control-Allow-Credentials", "true")
            w.Header().Set("Access-Control-Allow-Methods", "GET, POST")
            w.Header().Set("Access-Control-Allow-Headers", "Authorization, Content-Type")
        }
        next.ServeHTTP(w, r)
    })
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/api/orders/", func(w http.ResponseWriter, r *http.Request) {
        json.NewEncoder(w).Encode(map[string]string{"id": r.URL.Path})
    })

    handler := secureHeaders(cors(mux))
    log.Fatal(http.ListenAndServeTLS(":8443", "cert.pem", "key.pem", handler))
}
```

### Nginx

```nginx
# VULNERABLE: weak TLS, missing security headers, exposes version
server {
    listen 443 ssl;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers LOW:EXPORT;
    server_tokens on;

    location / {
        add_header X-Frame-Options none;  # allows framing
        proxy_pass http://backend;
    }
}

# SECURE: modern TLS, security headers, no version disclosure
server {
    listen 443 ssl http2;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:...';
    ssl_prefer_server_ciphers off;
    server_tokens off;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-Frame-Options DENY always;
    add_header Content-Security-Policy "default-src 'self'" always;
    add_header Cache-Control "no-store" always;

    location / {
        proxy_pass http://backend;
    }
}
```

### Apache

```apache
# VULNERABLE: server signature on, weak TLS, missing headers, trace enabled
ServerTokens Full
ServerSignature On
TraceEnable on
SSLProtocol all -SSLv3
SSLCipherSuite LOW:EXPORT

<VirtualHost *:443>
    Header always set X-Frame-Options "SAMEORIGIN"
</VirtualHost>

# SECURE: hardened defaults, modern TLS, security headers, trace disabled
ServerTokens Prod
ServerSignature Off
TraceEnable off
SSLProtocol -all +TLSv1.2 +TLSv1.3
SSLCipherSuite HIGH:!aNULL:!MD5
SSLHonorCipherOrder on

<VirtualHost *:443>
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options DENY
    Header always set Content-Security-Policy "default-src 'self'"
    Header always set Cache-Control "no-store"
</VirtualHost>
```

### Kubernetes

```yaml
# VULNERABLE: root container, privileged, no resource limits, latest tag
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  template:
    spec:
      containers:
        - name: api
          image: myregistry/api:latest
          securityContext:
            privileged: true
            runAsRoot: true
          resources: {}

# SECURE: non-root, read-only root fs, limits, pinned image, network policy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: api
          image: myregistry/api:1.2.3-sha256:abc...
          imagePullPolicy: Always
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            capabilities:
              drop: ["ALL"]
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-deny-ingress
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: gateway
      ports:
        - protocol: TCP
          port: 8080
```

### Docker

```dockerfile
# VULNERABLE: latest tag, root user, secrets in image, unnecessary tools
FROM python:latest
RUN apt-get update && apt-get install -y curl netcat telnet
ENV DB_PASSWORD=SuperSecret123
USER root
EXPOSE 22 80 443

# SECURE: pinned base image, minimal user, no secrets, least privilege
FROM python:3.11.4-slim@sha256:...
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*
RUN groupadd -r app && useradd -r -g app app
WORKDIR /app
COPY --chown=app:app . .
USER app
EXPOSE 8080
```

### Terraform

```hcl
# VULNERABLE: public S3 bucket, open security group, overly permissive IAM
resource "aws_s3_bucket" "logs" {
  bucket = "api-logs-bucket"
}

resource "aws_s3_bucket_public_access_block" "logs" {
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_security_group" "api" {
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_iam_policy_document" "api" {
  statement {
    actions   = ["*"]
    resources = ["*"]
    effect    = "Allow"
  }
}

# SECURE: private S3 bucket, least-privilege security group and IAM
resource "aws_s3_bucket" "logs" {
  bucket = "api-logs-bucket"
}

resource "aws_s3_bucket_public_access_block" "logs" {
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_security_group" "api" {
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"]
  }
}

data "aws_iam_policy_document" "api" {
  statement {
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.logs.arn}/*"]
    effect    = "Allow"
  }
}
```

### CloudFormation

```yaml
# VULNERABLE: public S3 bucket, open ingress, no encryption
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  ApiBucket:
    Type: AWS::S3::Bucket
    Properties:
      AccessControl: PublicRead
      PublicAccessBlockConfiguration:
        BlockPublicAcls: false
        BlockPublicPolicy: false
        IgnorePublicAcls: false
        RestrictPublicBuckets: false

  ApiSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 0
          ToPort: 65535
          CidrIp: 0.0.0.0/0

# SECURE: private S3 bucket, encrypted, least-privilege ingress
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  ApiBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  ApiSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 10.0.0.0/8
```

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

> **Subagent constraint**: All subagents must **investigate only**. They are prohibited from modifying project source files, committing changes, opening pull requests, or running destructive commands against the repository or its environments.

### Phase 1: Recon — Find Configuration Artifacts

Launch a subagent with the following instructions:

> **Goal**: Find configuration files, header definitions, error handlers, and dependency manifests that may indicate security misconfiguration. Write results to `{{ REPORTS_ROOT }}/20_recon.md`.
>
> **Constraint**: Investigate only. Do not modify project source files or open pull requests.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, frameworks, web servers, container orchestration, and cloud services.
>
> **What to search for**:
>
> 1. **Web / application server configuration**:
>    - Nginx: `nginx.conf`, `sites-available/*`, `sites-enabled/*`
>    - Apache: `httpd.conf`, `.htaccess`, `apache2.conf`, `sites-enabled/*`
>    - Application frameworks: `settings.py`, `application*.yml`, `config/*.py`, `app.js`, `server.js`, `Program.cs`, `Startup.cs`
>
> 2. **Security header definitions**:
>    - Look for `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, `Cache-Control`, `Pragma`
>    - Framework middleware or `after_request` / `setHeaders` equivalents
>    - Web server `add_header` / `Header` directives
>
> 3. **CORS configuration**:
>    - Wildcard origins (`*`), reflected origins, `Access-Control-Allow-Credentials: true` with wildcard
>    - Flask-CORS, Django-CORS-Headers, Express `cors`, Spring `@CrossOrigin`, FastAPI `CORSMiddleware`, Rails `Rack::Cors`, etc.
>
> 4. **TLS / HTTPS configuration**:
>    - `ssl_protocols`, `SSLProtocol`, `ssl_ciphers`, `SSLCipherSuite`
>    - `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`
>    - Hard-coded `http://` URLs or disabled certificate validation
>
> 5. **Error handlers and debug mode**:
>    - Global exception handlers that return `stack`, `traceback`, or raw exception messages
>    - `DEBUG=True`, `debug=True`, `NODE_ENV=development`, `app.Environment.IsDevelopment()`, `app.run(debug=True)` in production contexts
>    - Detailed error pages or developer exception pages
>
> 6. **Unnecessary features / HTTP verbs**:
>    - `TRACE`, `OPTIONS`, `HEAD`, `PUT`, `DELETE` enabled without need
>    - Admin panels, debug endpoints, or health endpoints exposed publicly
>
> 7. **Container / orchestration configuration**:
>    - `Dockerfile`, `docker-compose.yml`, Kubernetes manifests, Helm charts
>    - `runAsRoot`, `privileged: true`, missing resource limits, `latest` image tags
>    - Missing `NetworkPolicy`, overly broad `Service` or `Ingress` rules
>
> 8. **Dependency manifests**:
>    - `requirements.txt`, `Pipfile.lock`, `package.json`, `package-lock.json`, `yarn.lock`
>    - `pom.xml`, `build.gradle`, `go.mod`, `Cargo.toml`, `Gemfile.lock`
>    - Outdated or known-vulnerable versions (note the version and package name)
>
> 9. **Cloud / platform configuration**:
>    - Terraform, CloudFormation, Pulumi, ARM templates
>    - S3 bucket ACLs, IAM policies, security group rules, overly permissive roles
>
> 10. **Log4j-style JNDI / lookup injection indicators**:
>    - Logging libraries with JNDI or placeholder lookup features (Log4j, Logback)
>    - Request headers, query parameters, or bodies logged without sanitization
>    - Outbound network policies allowing unrestricted egress
>
> 11. **HTTP request smuggling / desync indicators**:
>    - Conflicting `Content-Length` / `Transfer-Encoding` handling
>    - Header normalization differences across proxies and backends
>    - Path/encoding inconsistencies
>
> 12. **Content-type and schema validation**:
>    - Endpoints accepting `*/*` or arbitrary content types
>    - Missing OpenAPI / JSON Schema / protobuf response schemas
>    - Error handlers returning unvalidated objects
>
> **What to ignore**:
> - Local development-only configuration that is clearly not used in production
> - Static asset serving where no sensitive data is involved
> - Third-party dependency source code (focus on the project's own configuration)
>
> **Output format** — write to `{{ REPORTS_ROOT }}/20_recon.md`:
>
> ```markdown
> # Security Misconfiguration Recon: [Project Name]
>
> ## Summary
> Found [N] configuration artifacts or indicators that require verification.
>
> ## Candidates
>
> ### 1. [Descriptive name]
> - **Category**: [headers / cors / tls / errors / verbs / defaults / patches / container / cloud / jndi / smuggling / content-type / schema]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Issue summary**: [One-line description]
> - **Relevant snippet**:
>   ```
>   [relevant code or config]
>   ```
>
> [Repeat for each candidate]
> ```

### Phase 2: Verify — Check Misconfiguration Indicators (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/20_recon.md` and split the candidates into **batches of up to 3 candidates each**. Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned candidates and writes results to its own batch file.

**Batching procedure** (you, the orchestrator, do this — not a subagent):

1. Read `{{ REPORTS_ROOT }}/20_recon.md` and count the numbered candidate sections (### 1., ### 2., etc.).
2. Divide them into batches of up to 3. For example, 8 candidates → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those candidate sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned candidates.
5. Each subagent writes to `{{ REPORTS_ROOT }}/20_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary language/framework and infrastructure from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions (substitute the batch-specific values):

> **Goal**: Verify the following security misconfiguration candidates and determine whether each is actually vulnerable. Write results to `{{ REPORTS_ROOT }}/20_batch_[N].md`.
>
> **Constraint**: Investigate only. Do not modify project source files or open pull requests.
>
> **Your assigned candidates** (from the recon phase):
>
> [Paste the full text of the assigned candidate sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand the runtime environment, framework conventions, and deployment topology.
>
> **Security Misconfiguration Reference — What to look for**:
>
> Security misconfiguration occurs when any layer of the API stack lacks secure hardening, uses insecure defaults, exposes unnecessary features, or leaks information. Focus on issues that are observable from configuration or code.
>
> **What is IN scope**:
> - Missing or incorrectly set security headers (`HSTS`, `X-Content-Type-Options`, `X-Frame-Options`, `Content-Security-Policy`, `Cache-Control`)
> - Overly permissive CORS (wildcard origin, reflected origin, credentials with wildcard)
> - Missing, weak, or inconsistent TLS
> - Verbose error messages, stack traces, or debug information returned to clients
> - Unnecessary HTTP verbs or features enabled
> - Insecure framework defaults, debug mode in production, default credentials
> - Insecure container/orchestration/cloud settings (root containers, privileged mode, open buckets, broad IAM)
> - Missing patches or outdated components with known vulnerabilities
> - Log4j-style JNDI / lookup injection via logged request data
> - Missing `Cache-Control` on sensitive responses
> - HTTP request smuggling / desync indicators (CWE-444)
> - Overly permissive content-type / data-format handling
> - Missing OpenAPI / JSON Schema response validation, including error responses
> - Verbose or debug logging that leaks sensitive data or expands untrusted input
>
> **What is NOT in scope for this scan**:
> - Missing authentication (route has no auth at all) → covered by the unauthenticated access scan
> - Business logic flaws → covered by the business logic scan
> - Injection vulnerabilities in request parameters → covered by injection scans
>
> **Vulnerable vs. Secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **For each candidate, check**:
>
> 1. **Is the configuration actually used in the production path?**
>    - Is there a separate production config that overrides the finding?
>    - Is the file in a `dev/`, `test/`, or `local/` directory that is excluded from production?
>
> 2. **Headers**
>    - Are the expected security headers defined anywhere (application code, middleware, or reverse proxy)?
>    - Are they sent on **all** responses, including errors?
>    - Is `Cache-Control` set correctly on sensitive responses?
>
> 3. **CORS**
>    - Is the allowed origin a wildcard (`*`)?
>    - Does the server reflect the request `Origin` without validation?
>    - Is `Access-Control-Allow-Credentials: true` combined with a wildcard or untrusted origin?
>
> 4. **TLS**
>    - Is HTTPS enforced (HSTS, redirects, secure cookies)?
>    - Are weak protocols/ciphers enabled?
>    - Is there mixed HTTP/HTTPS traffic or disabled certificate validation?
>
> 5. **Error handling**
>    - Do error responses include stack traces, SQL, internal paths, or framework versions?
>    - Is debug mode enabled in a production-looking configuration?
>
> 6. **Features and defaults**
>    - Are unnecessary HTTP verbs enabled?
>    - Are there debug endpoints, admin panels, or default accounts exposed?
>    - Are framework/orchestrator defaults hardened?
>
> 7. **Dependencies and patches**
>    - Is the component version known to be vulnerable? (If yes, cite the CVE if known.)
>    - Is there a lockfile ensuring reproducible builds?
>
> 8. **JNDI / lookup injection**
>    - Are logging libraries with JNDI/lookup features used in vulnerable versions?
>    - Are request headers or parameters logged without sanitization?
>    - Is outbound egress permissive?
>
> 9. **HTTP request smuggling / desync**
>    - Are there conflicting `Content-Length` / `Transfer-Encoding` behaviors?
>    - Do proxies and backends normalize headers differently?
>
> 10. **Content-type and schema validation**
>    - Do endpoints accept arbitrary content types?
>    - Are response schemas (including error responses) defined and enforced?
>
> 11. **Verbose logging**
>    - Is debug logging enabled in production?
>    - Are request/response bodies or sensitive fields logged verbatim?
>
> **Classification**:
> - **Vulnerable**: A clear misconfiguration is present and exploitable in the production path.
> - **Likely Vulnerable**: A misconfiguration indicator exists, but context (e.g., a compensating proxy control) prevents a definitive conclusion.
> - **Not Vulnerable**: The configuration is hardened correctly or the candidate is in a non-production path.
> - **Needs Manual Review**: Automated analysis cannot determine the status (e.g., configuration pulled from environment at runtime, complex multi-layer header chain).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/20_batch_[N].md`:
>
> ```markdown
> # Security Misconfiguration Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Configuration name
> - **Category**: [headers / cors / tls / errors / verbs / defaults / patches / container / cloud / jndi / smuggling / content-type / schema]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Issue**: [Clear description of the misconfiguration]
> - **Impact**: [What an attacker can do — leak data, bypass security controls, fingerprint the stack, etc.]
> - **Proof**: [Show the relevant configuration or code path]
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [curl command, request example, or step-by-step instructions to confirm on the live app.
>    Include exact endpoint/URL, headers to send or observe, and what to look for in the response.]
>   ```
>
> ### [LIKELY VULNERABLE] Configuration name
> - **Category**: [headers / cors / tls / errors / verbs / defaults / patches / container / cloud / jndi / smuggling / content-type / schema]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Issue**: [What's suspicious]
> - **Concern**: [Why this might still be exploitable]
> - **Proof**: [Show the relevant configuration or code path]
> - **Remediation**: [Specific fix]
> - **Dynamic Test**:
>   ```
>   [curl command or step-by-step confirmation instructions]
>   ```
>
> ### [NOT VULNERABLE] Configuration name
> - **Category**: [headers / cors / tls / errors / verbs / defaults / patches / container / cloud / jndi / smuggling / content-type / schema]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Protection**: [Why it is safe]
>
> ### [NEEDS MANUAL REVIEW] Configuration name
> - **Category**: [headers / cors / tls / errors / verbs / defaults / patches / container / cloud / jndi / smuggling / content-type / schema]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Uncertainty**: [Why automated analysis couldn't determine the status]
> - **Suggestion**: [What to look at manually]
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/20_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/20_misconfiguration.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/20_batch_1.md`, `{{ REPORTS_ROOT }}/20_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Group findings by category (headers, CORS, TLS, errors, verbs, defaults, patches, container, cloud, jndi, smuggling, content-type, schema) within each classification group.
5. Write the merged report to `{{ REPORTS_ROOT }}/20_misconfiguration.md` using this format:

```markdown
# Security Misconfiguration Analysis Results: [Project Name]

## Executive Summary
- Candidates analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Not Vulnerable: [N]
- Needs Manual Review: [N]

## Findings

[VULNERABLE findings first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then NOT VULNERABLE.
Preserve every field from the batch results exactly as written.]

## Prevention Guidance

[Summarize the hardening checklist, automated scanning recommendations, request-processing uniformity advice, content-type/schema restrictions, and logging hardening from the Prevention section below.]
```

6. After writing `{{ REPORTS_ROOT }}/20_misconfiguration.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/20_batch_*.md`).

---

## Prevention Guidance

### Hardening Checklist

- Establish a repeatable hardening process for every environment (dev, staging, production).
- Disable debug mode, verbose error pages, and development-only features in production.
- Send a consistent set of security headers on every response, including error responses:
  - `Strict-Transport-Security`
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options` or CSP `frame-ancestors`
  - `Content-Security-Policy`
  - `Cache-Control` for sensitive responses
- Enforce HTTPS for all client-to-API and internal service-to-service communication.
- Use modern TLS protocols (1.2+) and strong cipher suites; disable weak protocols and ciphers.
- Restrict CORS to specific, trusted origins and avoid combining credentials with wildcard origins.
- Disable unnecessary HTTP verbs and features; expose only what the API requires.
- Remove or protect default accounts, admin interfaces, and sample applications.
- Harden containers and orchestration:
  - Run as non-root
  - Drop unnecessary capabilities
  - Use read-only root filesystems
  - Pin image tags and use minimal base images
  - Apply least-privilege network policies and IAM roles
- Keep all components patched and use lockfiles for reproducible builds.
- Harden logging libraries:
  - Disable JNDI / message lookup features where not required.
  - Do not log unsanitized request headers, query parameters, or bodies.
  - Restrict outbound egress to required destinations only.
- Set `Cache-Control: no-store` on responses containing PII, tokens, or private data.
- Uniformly process incoming requests across the entire HTTP server chain to avoid HTTP request smuggling and desync issues.
- Restrict incoming content types and data formats to those required by the API.
- Define and enforce API response payload schemas, including error responses, to prevent stack traces and information leakage.

### Automated Configuration Scanning

- Integrate configuration scanners into CI/CD:
  - Static analysis for infrastructure-as-code (Checkov, tfsec, Terrascan, cfn-lint)
  - Container image scanning (Trivy, Grype, Clair)
  - Dependency vulnerability scanning (Snyk, OWASP Dependency-Check, npm audit)
  - Web server and header scanners (Mozilla Observatory, securityheaders.com)
- Continuously assess configuration effectiveness across all environments.
- Fail builds on high-severity misconfigurations and outdated vulnerable components.

### Uniform Request Processing

- Ensure every server in the HTTP chain (load balancers, reverse proxies, WAFs, forward proxies, and backend servers) processes incoming requests consistently.
- Normalize headers, encoding, and path parsing to avoid HTTP request smuggling and desync issues.
- Use a single source of truth for security headers and TLS policy, applied as close to the client as practical, and verify end-to-end behavior.

---

## References

- OWASP API Security Top 10 2023 — **API8:2023 Security Misconfiguration**: https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/
- OWASP Secure Headers Project: https://owasp.org/www-project-secure-headers/
- WSTG — Configuration and Deployment Management Testing: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/02-Configuration_and_Deployment_Management_Testing/README
- WSTG — Testing for Error Handling: https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/08-Testing_for_Error_Handling/README
- NIST SP 800-123 — Guide to General Server Security: https://csrc.nist.gov/publications/detail/sp/800-123/final
- Let's Encrypt: https://letsencrypt.org/
- [CWE-2: Environmental Security Flaws](https://cwe.mitre.org/data/definitions/2.html)
- [CWE-16: Configuration](https://cwe.mitre.org/data/definitions/16.html)
- [CWE-209: Generation of Error Message Containing Sensitive Information](https://cwe.mitre.org/data/definitions/209.html)
- [CWE-319: Cleartext Transmission of Sensitive Information](https://cwe.mitre.org/data/definitions/319.html)
- [CWE-388: Error Handling](https://cwe.mitre.org/data/definitions/388.html)
- [CWE-444: Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling')](https://cwe.mitre.org/data/definitions/444.html)
- [CWE-942: Permissive Cross-domain Policy with Untrusted Domains](https://cwe.mitre.org/data/definitions/942.html)
- [CWE-1117: Improper Use of Uninitialized Container](https://cwe.mitre.org/data/definitions/1117.html)

---

## Important Reminders

- Read `{{ REPORTS_ROOT }}/01_architecture.md` and pass its content to all subagents as context.
- Phase 2 must run AFTER Phase 1 completes — it depends on the recon output.
- Phase 3 must run AFTER all Phase 2 batches complete — it depends on all batch outputs.
- Batch size is **3 candidates per subagent**. If there are 1-3 candidates total, use a single subagent. If there are 10, use 4 subagents (3+3+3+1).
- Launch all batch subagents **in parallel** — do not run them sequentially.
- Each batch subagent receives only its assigned candidates' text from the recon file, not the entire recon file. This keeps each subagent's context small and focused.
- Subagents must **investigate only** and are prohibited from modifying project source files, committing changes, opening pull requests, or running destructive commands.
- Distinguish production configuration from development/test configuration; only production-relevant findings should be classified as Vulnerable.
- When in doubt, classify as "Needs Manual Review" rather than "Not Vulnerable". False negatives are worse than false positives in security assessment.
- Check the full request/response path: headers may be added or stripped by reverse proxies, load balancers, or CDNs. The absence of a header in application code does not always mean it is missing in production.
- Verify that error handlers return generic messages to clients while logging detailed diagnostics server-side.
- Clean up intermediate files: delete `{{ REPORTS_ROOT }}/20_recon.md` and all `{{ REPORTS_ROOT }}/20_batch_*.md` files after the final `{{ REPORTS_ROOT }}/20_misconfiguration.md` is written.
