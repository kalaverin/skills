---
subject: "Google Python style rules covering formatting, docstrings, naming, typing; semicolon ban, 80-character line length, 4-space indentation, whitespace, shebang, triple-double-quote docstrings with `Args:`/`Returns:`/`Raises:`, f-strings, lazy `logging` patterns, `with` resource cleanup, `TODO` format, import grouping, getters, `@dataclass` documentation exemption, `lower_with_under`/`CapWords` conventions, `__main__` guard, `TypeVar`/`ParamSpec`, `X | None`, `TypeAlias`, `TYPE_CHECKING` imports."
index:
  - anchor: py-st-semicolons
    what: "Ban on terminating lines with semicolons and on packing two statements onto one line via `;`."
    problem: "Agent ports code from C-style languages or compresses diffs by chaining statements; semicolon-terminated lines slip through review and clash with Google formatting canon; C habit, compacted diff, terminator pollution, line packing, idiom clash, port residue, separator misuse."
    use_when: "Writing or reviewing any Python line; merging statements to save vertical space; code arriving from brace-language backgrounds."
    avoid_when: "Shell one-liners outside source files; documenting `;`-heavy foreign syntax in prose examples."
    expected: "Every line carries exactly one statement and ends without semicolons."
  - anchor: py-st-line-length
    what: "The 80-character maximum line length with explicit exceptions (long imports, URLs in comments, unsplittable constants, pylint disables) and implicit line joining instead of backslash continuation."
    problem: "Agent generates wide expressions, chained calls, long strings; unwrapped lines overflow review panes, horizontal scrolling hides bugs, explicit continuation characters rot under edits; hidden defects, wrapping strategy, syntactic level breaking, reviewer fatigue, diff noise, narrow viewport, pane clipping."
    use_when: "Formatting any source line; breaking chained calls or long conditions; deciding whether an exception (URL, import, pylint directive) applies."
    avoid_when: "Non-Python prose files; generated code excluded from style enforcement."
    expected: "Lines stay within 80 columns via parenthesized breaks, with documented exceptions only."
  - anchor: py-st-parentheses
    what: "Sparing use of parentheses: allowed around tuples and for implied continuation, forbidden around `return` values and `if`/`while` conditions."
    problem: "Agent parenthesizes every condition and returned expression out of brace-language habit; redundant parens pile up, readers misread plain values as tuples, style checkers flag noise; spurious grouping, tuple confusion, delimiter spam, reader misinterpretation, habit import, visual clutter, bracket discipline."
    use_when: "Deciding whether parens around an expression are meaningful; cleaning up `if (x):` or `return (foo)` patterns; tuple display in question."
    avoid_when: "Continuation parens for wrapping — line-length rules govern that case; precedence grouping for clarity."
    expected: "Parentheses appear only where they change semantics or join lines; conditions and returns stay bare."
  - anchor: py-st-indentation
    what: "Four-space block indentation without tabs, vertical alignment or hanging 4-space indent for wrapped elements, plus trailing-comma rules that hint auto-formatters."
    problem: "Agent emits tabs, two-space hangs, ragged continuations, or first-line-stuffed arguments; mixed indentation breaks formatter output, misaligned code hides structure; tab infiltration, hanging indent depth, bracket parking, uneven alignment, autoformat hint, structural readability, vertical drift, structure scanning."
    use_when: "Indenting any block; wrapping arguments or collections across lines; placing closing brackets or final commas."
    avoid_when: "Fixing horizontal spacing inside one line — whitespace rules own that; line-length budget questions."
    expected: "Blocks indent by four spaces, continuations align or hang consistently, collection items land one per line under comma control."
  - anchor: py-st-blank-lines
    what: "Vertical spacing between definitions: two blank lines around top-level functions and classes, one between methods, none after a `def` line."
    problem: "Agent densifies output or scatters empty rows randomly; cramped modules read as wall of text, double gaps fragment related code, reviewers flag spacing churn; gap inconsistency, definition separation, breathing room, review friction, vertical rhythm, spacing roulette."
    use_when: "Separating module-level functions and classes, methods, or logical blocks inside bodies; placing comments near definitions."
    avoid_when: "Horizontal padding questions; docstring-internal layout — docstring sections own that."
    expected: "Top-level definitions stand clearly apart, methods sit one empty row from neighbors, and bodies start right under their `def` line."
  - anchor: py-st-whitespace
    what: "Typographic spacing around punctuation and operators: tight brackets, spaced binary operators, no spaces around `=` in keyword arguments unless annotated, no vertical alignment padding."
    problem: "Agent pads brackets, misaligns assignment columns, squeezes operators; spaced-out calls and cramped comparisons both read wrong, alignment edits rot on every rename; bracket padding, operator crowding, keyword spacing, annotation exception, column stacking, edit fragility, punctuation typography, readability tax."
    use_when: "Spacing around operators, commas, colons, or brackets in question; writing calls with named arguments or annotated defaults; tempted to align assignments into columns."
    avoid_when: "Block-level indentation depth — indentation rules own that; blank-line placement."
    expected: "Operators and punctuation carry canonical spacing, keyword defaults follow the annotation rule, and no column alignment survives a rename."
  - anchor: py-st-shebang-line
    what: "When a `#!` line is warranted: only on directly executed program entry files, `#!/usr/bin/env python3` per PEP-394."
    problem: "Agent sprinkles shebang headers on every module or omits one from true entry scripts; useless headers mislead readers about execution, missing header breaks direct invocation; entry script detection, execution intent, virtualenv resolution, misleading banner, cli launch, import path irrelevance, copy-paste drift."
    use_when: "Creating an executable entry-point file; reviewing whether a library module needs the header; choosing the env-based path."
    avoid_when: "Library or package modules only ever imported; Windows-first projects where the line is inert."
    expected: "Runnable entry points open with the correct `#!/usr/bin/env python3` line; importable modules carry none."
  - anchor: py-st-comments-and-docstrings
    what: "Chapter map for choosing the right documentation vehicle — module, function, class docstrings versus inline comments."
    problem: "Agent mixes documentation channels, dumping usage prose into inline remarks or leaving public surface undocumented; wrong vehicle hides knowledge from doc tooling and reviewers; channel mismatch, vehicle choice, prose placement, knowledge hiding, tooling extraction, reader discovery, doc taxonomy, guidance scatter."
    use_when: "Picking which doc vehicle fits a piece of knowledge; structuring module documentation surface before writing details."
    avoid_when: "Specific docstring section formats — dedicated subsection cards cover each; comment wording mechanics."
    expected: "Every fact lands in the documentation vehicle designed for it; subsections handle the concrete formats."
  - anchor: py-st-docstrings
    what: "Docstring basics per PEP 257: triple-double-quote form, summary line under 80 chars ending with terminal punctuation, blank line, then body."
    problem: "Agent writes docstrings with wrong quote style or merges summary into body; tooling cannot extract clean summaries, help output renders garbage, style linters complain; one-line overview, quote format, end mark, pydoc display, metadata harvest, first line, lint friction, doc structure."
    use_when: "Starting any docstring; choosing quote characters; laying out summary versus body."
    avoid_when: "Content rules for specific sections like `Args:` — those live in dedicated cards; inline remark style."
    expected: "Docstrings open with a one-line punctuated summary in triple quotes, separated from the aligned body by one empty row."
  - anchor: py-st-comments-in-modules
    what: "Module-level documentation: license boilerplate plus an opening docstring describing contents and usage with optional examples."
    problem: "Agent creates files that open with bare code or stale boilerplate; readers cannot grasp module purpose, license obligations go unmet, pydoc output stays empty; scope orientation, usage synopsis, legal header, onboarding cost, purpose discovery, empty overview, entry documentation, file preamble."
    use_when: "Creating or refreshing a file header; summarizing what a module offers and how to run it; adding license text."
    avoid_when: "Test files without extra run information — the test-module exemption applies; function-level documentation."
    expected: "Files open with legal text and a docstring that explains contents, exports, and typical usage."
  - anchor: py-st-test-modules
    what: "Exemption for test files: module docstrings only when they carry extra information like run instructions, unusual setup, or environment dependencies."
    problem: "Agent ritualistically prefixes test files with content-free headers; noise docstrings rot, readers skim past them and miss files where execution notes actually matter; hollow preamble, alert fatigue, setup caveats, environment prerequisites, skim blindness, signal dilution, redundant restatement."
    use_when: "Writing a test file that needs run flags, fixtures, or external services documented; trimming a vacuous test header."
    avoid_when: "Ordinary test modules with self-evident purpose; production module headers — full module rules apply there."
    expected: "Only tests carrying real extra context keep file-level docs; the rest start with imports."
  - anchor: py-st-functions-and-methods
    what: "When function docstrings are mandatory (public API, nontrivial size, non-obvious logic) and their contract-focused structure with `Args:`/`Returns:`/`Raises:` sections."
    problem: "Agent documents trivial helpers verbosely while leaving intricate public entry points bare; callers must read implementations to invoke safely, review cycles bounce on missing contracts; caller self-service, interface clarity, mandatory threshold, public surface, invocation safety, iteration churn, voice consistency, section structure."
    use_when: "Deciding whether a function needs documentation; structuring `Args:`/`Returns:`/`Raises:` blocks; picking descriptive versus imperative mood; documenting a `@property`."
    avoid_when: "Trivial self-explanatory signatures where sections add nothing; class-level documentation — the class card owns that."
    expected: "Every qualifying function carries a contract docstring sufficient to call it without reading its body."
  - anchor: py-st-doc-function-args
    what: "`Args:` section mechanics: name-colon-description per parameter, 2-or-4-space hanging indent for overflow, types only when unannotated, `*foo`/`**bar` spelled out."
    problem: "Agent omits parameters, misaligns continuation lines, duplicates annotated types; incomplete parameter docs mislead callers, drift from signatures, rot during refactors; argument coverage, stale contracts, varargs spelling, caller misdirection, maintenance decay, documentation completeness, redundant annotation, wrap formatting."
    use_when: "Documenting parameters including `*args`/`**kwargs`; deciding if unannotated types belong in text; wrapping long descriptions."
    avoid_when: "Return or exception documentation — `py-st-doc-function-returns` and `py-st-doc-function-raises` own those; functions whose signature already says everything."
    expected: "Every parameter appears once with description, clean wrapped continuation, and no restated annotation info."
  - anchor: py-st-doc-function-returns
    what: "`Returns:`/`Yields:` section mechanics: type and semantics of the outcome, banned for `None`-only functions, omittable when the summary already opens with 'Returns' or 'Yields'."
    problem: "Agent documents void functions with empty outcome sections or restates annotation text verbatim; contracts carry noise, summaries echo bodies, generator outcomes get mislabeled as ordinary values; void ceremony, duplicated typing, contract bloat, omission confusion, doc drift, reader misdirection."
    use_when: "Documenting a return value or generator yield; deciding whether the section may be omitted; complex structured outcomes worth unfolding."
    avoid_when: "Function returns only `None` — the section is banned there; parameter documentation — `py-st-doc-function-args` owns that."
    expected: "Outcome sections state type and semantics precisely; void functions carry none, generators use `Yields:`."
  - anchor: py-st-doc-function-raises
    what: "`Raises:` section scope: only interface-relevant exceptions forming the contract, never `ValueError`-style guards against caller misuse."
    problem: "Agent lists every raised exception including caller-misuse guards, or omits contractual failures entirely; callers drown in noise or meet undocumented surprises at runtime; exception inventory, contractual omission, guard leakage, interface ambiguity, runtime shock, review friction."
    use_when: "Deciding which exceptions belong in a docstring; documenting failure modes of a public API."
    avoid_when: "Programming-error guards on invalid API usage — those stay undocumented; raising and handling discipline — `py-lr-exceptions` owns that."
    expected: "Only contract-relevant exceptions appear; caller-misuse guards never enter the docstring."
  - anchor: py-st-overridden-methods
    what: "Docstring exemption for overriding methods decorated with `@override`, unless behavior materially refines the base contract."
    problem: "Agent copies base docs into every override or strips documentation from undecorated overrides; duplicated prose forks on base edits, missing decoration hides inherited contract; trivial docstring, decorator exemption, contract refinement, forked text, inheritance docs, base drift, copy rot, behavior delta."
    use_when: "Overriding a base method; deciding whether `@override` suffices or refinement needs prose; reviewing subclass documentation."
    avoid_when: "Undecorated overrides — full docstring is required there; first-definition methods with no base contract."
    expected: "Decorated overrides stay doc-free unless refining behavior; undecorated ones always carry documentation."
  - anchor: py-st-comments-in-classes
    what: "Class docstrings: one-line summary of what an instance represents, `Attributes:` section for public attributes, exception classes describing the error itself."
    problem: "Agent leaves classes undocumented or writes filler like 'class that describes'; attributes stay mysterious, exception docs narrate trigger context instead of meaning, consumers guess invariants; instance representation, attribute inventory, exception semantics, filler preamble, API archaeology, invariant hiding, boilerplate narration, meaning versus context."
    use_when: "Documenting any class; inventorying attribute docs; writing exception-class docs; deciding whether a `@dataclass` needs prose beyond its annotations."
    avoid_when: "Method-level contracts — function rules cover those; trivial dataclasses already self-describing via annotations."
    expected: "Classes open with representational summaries, attribute docs sit under `Attributes:`, exceptions describe what they mean."
  - anchor: py-st-block-and-inline-comments
    what: "Block and inline remarks for tricky code: preceding lines for complicated operations, end-of-line notes for non-obvious ones, never narrating what code says."
    problem: "Agent either leaves bitwise tricks unexplained or narrates obvious lines; reviewers stall on magic, narration comments rot into lies beside edited code; tricky logic, opaque idiom, stale commentary, comprehension block, explanation debt, remark spacing, code paraphrase, drift hazard."
    use_when: "Facing non-obvious or complicated code; choosing block versus end-of-line placement; setting `#` spacing."
    avoid_when: "Self-evident lines — narration is banned there; interface documentation belonging in docstrings."
    expected: "Tricky spots carry why-focused remarks at proper spacing; no comment merely restates its line."
  - anchor: py-st-punctuation-spelling-and-grammar
    what: "Editorial quality bar for comments: proper capitalization, punctuation, full-sentence register, informal only for short end-of-line notes."
    problem: "Agent ships typo-ridden fragments in comments; sloppy prose undermines reader trust, confuses translators and reviewers, signals careless code beneath; language standard, typo noise, sentence fragments, capitalization drift, credibility erosion, grammar discipline, translation friction, quality perception."
    use_when: "Polishing comment prose; choosing sentence versus fragment register; reviewing docs before commit."
    avoid_when: "Comment placement or content selection — block-comment rules own those; docstring structure."
    expected: "Comments read as clean narrative prose with consistent capitalization and punctuation."
  - anchor: py-st-strings
    what: "String rules: f-strings/`%`/`format` over `+` concatenation, `''.join` for loop accumulation, consistent quote choice, triple-double-quotes for multi-line, `textwrap.dedent` for indentation control, greppable error messages."
    problem: "Agent concatenates strings in loops, mixes quotes randomly, interpolates logging eagerly, embeds indentation into literals; quadratic copying slows hot paths, lazy logging dies, error text defeats grepping; concatenation cost, delimiter uniformity, deferred formatting, pattern placeholders, dedent handling, multi-line layout, greppable messages, buffer building."
    use_when: "Formatting or accumulating strings; picking quote characters; writing user-facing error messages; embedding multi-line literals."
    avoid_when: "Bytes handling; docstring layout — docstring sections own that."
    expected: "Strings use interpolation over `+`, loops join via `''.join`, logging stays lazy with pattern literals, and quotes stay uniform per file."
  - anchor: py-st-logging
    what: "Lazy `logging` discipline: pattern-string literal first, values as subsequent arguments, never f-string interpolation inside log calls."
    problem: "Agent f-strings values into log calls; every invocation pays formatting cost even when level sits disabled, queryable pattern fields vanish, output messages fragment across variants; premature rendering, disabled-level waste, pattern loss, per-call overhead, level blindness, observability tax."
    use_when: "Writing or reviewing any `logging`/`logger` call; choosing between literal-plus-arguments and interpolation; guarding expensive messages behind levels."
    avoid_when: "Greppable message wording — `py-st-strings` owns message text; f-string usage outside log calls."
    expected: "Log calls pass a literal pattern plus trailing arguments; nothing renders for disabled levels."
  - anchor: py-st-files-sockets-closeables
    what: "Explicit lifecycle for files, sockets, and similar closeables via `with` or `contextlib.closing`, never relying on `__del__`."
    problem: "Agent leaves handles to garbage collection; descriptor exhaustion crashes long-running services, finalizer timing varies across interpreters, leaked connections pile up under load; unclosed stream, fd starvation, destructor nondeterminism, garbage reliance, socket backlog, shutdown ordering, resource lifetime, implementation variance."
    use_when: "Opening files, sockets, DB connections, mmaps, or figures; choosing cleanup for objects lacking `with` support; auditing shutdown paths."
    avoid_when: "Pure in-memory objects without external state; ownership transferred to a framework-managed pool."
    expected: "Every closeable runs inside `with` or `contextlib.closing`; nothing depends on `__del__` for cleanup."
  - anchor: py-st-todo-comments
    what: "`TODO` format: all-caps keyword, colon, context link (ideally a bug), hyphen-led explanation; old parenthesized style deprecated."
    problem: "Agent drops vague reminders without context links or owner names; orphaned notes become archaeology, future maintainers cannot reconstruct intent, searches drown in inconsistent formats; debt marker, tracker URL, bug reference, abandoned note, purpose loss, searchable marker, date triggers, ownership trap."
    use_when: "Marking temporary or good-enough code; formatting reminder comments with tracker references; reviewing stale reminders."
    avoid_when: "Permanent design explanations — those belong in real comments; issues already fixed and merely awaiting cleanup."
    expected: "Every `TODO` carries tracker context plus explanation in canonical searchable shape."
  - anchor: py-st-imports-formatting
    what: "Import layout: one per line (except `typing`/`collections.abc`), placed after module docs, grouped `__future__` → stdlib → third-party → sub-package, sorted lexicographically ignoring case."
    problem: "Agent dumps unsorted multi-name import lines mid-file; dependency review becomes grep work, merge conflicts multiply, circular risks hide in chaos; import ordering, grouping tiers, lexical sort, rebase friction, dependency audit, placement discipline, line granularity, header block."
    use_when: "Writing or reordering import blocks; placing new imports into correct tier; resolving sort-order questions."
    avoid_when: "Conditional typing-only imports — dedicated typing-import rules apply; import mechanics of `__init__` re-exports."
    expected: "Imports sit tiered and lexicographically sorted, directly under the docstring block, each on its own line."
  - anchor: py-st-statements
    what: "One statement per line; single-line `if` bodies allowed only without `else`, never with `try`/`except`."
    problem: "Agent compresses logic into compound lines; condensed branches hide during review, diffs collide, debugging breakpoints cover too much at once; statement stacking, control flattening, review visibility, breakpoint granularity, diff collision, inline sprawl, line density, debug stepping."
    use_when: "Deciding whether a guard clause fits one line; splitting `try`/`except` or `if`/`else` onto separate lines."
    avoid_when: "Comprehensions and lambdas — expression rules differ; semicolon chaining — its own ban applies."
    expected: "Each statement owns its line; only else-free `if` bodies share one when everything fits."
  - anchor: py-st-accessors
    what: "When `get_foo()`/`set_foo()` accessors earn their place: complex or costly access, state invalidation on write — otherwise public attributes or properties."
    problem: "Agent wraps every attribute in trivial getter-setter pairs out of Java habit; boilerplate doubles API surface, refactors cost more, encapsulation theater hides nothing; accessor boilerplate, enterprise reflex, indirection layer, interface bloat, false privacy, invalidation logic, property alternative, visible break."
    use_when: "Getting or setting is complex, costly, or rebuilds state; migrating from property to explicit methods; naming accessor pairs."
    avoid_when: "Simple attribute reads and writes — expose the attribute publicly or use a plain property (`py-lr-properties` adjudicates that choice)."
    expected: "Accessors exist only where behavior justifies them; trivial passthroughs become public attributes."
  - anchor: py-st-naming
    what: "Descriptive naming baseline: no ambiguous abbreviations, no letter-deletion shortening, `.py` extension without dashes, with canonical case-style examples per identifier kind."
    problem: "Agent coins cryptic abbreviations or single-purpose names opaque outside project context; readers decode instead of reading, onboarding slows, reviews derail on naming debates; abbreviation ambiguity, descriptiveness scope, reader decoding, ramp cost, bike shedding, identifier taxonomy, case conventions, project jargon."
    use_when: "Coining any identifier; expanding unclear abbreviations; picking case style per identifier kind."
    avoid_when: "Established mathematical notation — the math-notation exemption governs; forbidden-name categories have their own card."
    expected: "Identifiers read descriptively at every scope; abbreviations survive only when universally understood."
  - anchor: py-st-names-to-avoid
    what: "Forbidden name categories: single characters (with enumerated exceptions like counters, `e`, `f`, private type vars), dashes, dunder-style names, offensive terms, type-encoding names like `id_to_name_dict`."
    problem: "Agent reaches for single letters, Hungarian-style type suffixes, or clever dunder names; grep becomes useless, reviews bounce, names collide with interpreter reservations; one-character opacity, grep failure, magic methods, Hungarian residue, offensive terminology, iterator exemption, scope proportionality, collision hazard."
    use_when: "Checking whether a short or unconventional name is legal; naming counters, exception handlers, file handles, or private type variables."
    avoid_when: "General descriptiveness questions — naming baseline covers those; paper-matching notation — math rules apply."
    expected: "No banned name shapes ship; permitted one-letter names stay within enumerated niches."
  - anchor: py-st-naming-conventions
    what: "Internal marking and module organization: single underscore for protected, discouraged double underscore, `CapWords` classes, `lower_with_under` modules and PEP 8 test method names."
    problem: "Agent privatizes via name mangling or splits classes one-per-module Java-style; mangled names resist testing, protected access confuses linters, scattered modules fragment cohesion; mangling fallout, protected underscore, testability loss, linter friction, package layout, class clustering, test naming, legacy casing."
    use_when: "Marking members protected or private; grouping classes into modules; naming new test methods or reconciling legacy `CapWords` tests."
    avoid_when: "Public-versus-internal casing lookup — Guido table card answers that; filename rules live elsewhere."
    expected: "Protected members wear one underscore, classes cluster cohesively per module, tests follow PEP 8 naming form."
  - anchor: py-st-file-naming
    what: "Filename rules: `.py` extension mandatory, dashes forbidden so files stay importable and unittest-discoverable, symlink or `exec` wrapper for extensionless launch."
    problem: "Agent names scripts with dashes or drops extensions for aesthetics; imports fail, test discovery skips files, tooling chokes on unresolvable module paths; command alias, collection miss, dash ban, extension requirement, wrapper indirection, tooling resolution, launch ergonomics, path validity."
    use_when: "Naming new Python files; making a script launchable without extension; fixing dash-bearing filenames."
    avoid_when: "Identifier casing inside files — naming conventions cover that; non-Python asset names."
    expected: "All modules carry dash-free `.py` names; extensionless commands exist only as symlinks or wrappers."
  - anchor: py-st-guidelines-derived-from-guidos-recommendations
    what: "Guido's public-versus-internal naming table mapping each symbol category (packages, modules, classes, constants, variables, methods, parameters) to its casing."
    problem: "Agent improvises casing for constants or internal classes; inconsistent schemes accumulate across codebase, readers cannot infer visibility from shape, reviews relitigate basics; casing lookup, visibility signal, cross-module uniformity, identifier kinds, public internal split, table reference, style reruns, convention drift."
    use_when: "Choosing casing for a symbol; marking globals, constants, or members internal; settling naming disputes quickly."
    avoid_when: "Forbidden-name decisions — the avoidance card owns those; abbreviation judgment calls."
    expected: "Each symbol follows the table; visibility reads from casing alone."
  - anchor: py-st-math-notation
    what: "Math exemption: short names matching a cited paper or algorithm beat style-guide descriptiveness in math-heavy code, with `pylint: disable=invalid-name` scoped narrowly."
    problem: "Agent forces verbose names into numerical code or uses paper letters without citation; formulas stop resembling their source, verification against reference becomes error-prone archaeology; formula fidelity, provenance link, notation matching, verification gap, disable scoping, dense numerics, reference mapping, readability inversion."
    use_when: "Naming variables in math-heavy code; deciding when paper notation overrides descriptiveness; citing notation sources; silencing name lints narrowly."
    avoid_when: "Public APIs — PEP8 names stay mandatory there; ordinary business logic without reference notation."
    expected: "Math code mirrors cited notation with source links; lint disables stay narrowly scoped."
  - anchor: py-st-main
    what: "Executable structure: `main()` function guarded by `if __name__ == '__main__':`, `app.run(main)` under `absl`, no side-effecting top-level code so `pydoc` and imports stay safe."
    problem: "Agent leaves executable logic at module top level; any import triggers side effects, pydoc crashes or hangs, tests execute CLI code during collection; execution leakage, main guard, entry function, pydoc safety, collection hazard, top-level execution, argv handling, importability contract."
    use_when: "Writing an executable script's entry point; reviewing top-level code for import safety; wiring `absl` startup."
    avoid_when: "Pure library modules with nothing to execute; notebook-style exploratory snippets."
    expected: "Executables run only through guarded `main()`; importing any module is side-effect free."
  - anchor: py-st-function-length
    what: "Function-size guidance: prefer small focused functions, no hard limit, reconsider structure past roughly 40 lines, split long ones when they resist change."
    problem: "Agent grows functions into hundred-line monoliths or fears touching legacy giants; review rounds stall, defects hide in depth, modifications become surgical ordeals; size creep, feedback latency, defect hiding, modification dread, split judgment, focused units, archaeology fear, structural pressure."
    use_when: "Sizing new functions; deciding whether a long body needs splitting; working inside an inherited giant."
    avoid_when: "Line-length formatting — separate rule; blanket hard caps — none exists here."
    expected: "Functions stay small and focused; oversized ones get split when structure allows."
  - anchor: py-st-type-annotations
    what: "Chapter hub for static typing practice across signatures, variables, generics, and typing-only imports."
    problem: "Agent approaches typing haphazardly, unsure which rules govern annotations versus imports versus generics; partial adoption leaves holes that checkers flag and readers distrust; typing taxonomy, adoption strategy, checker alignment, annotation coverage, rule routing, incremental hardening, consistency pressure, chapter map."
    use_when: "Starting typed work in a module; orienting among the typing subsections before deeper loads."
    avoid_when: "A concrete typing question — the specific subsection card routes better; untyped throwaway scripts."
    expected: "Agent reaches the right typing subsection directly; chapter scope is understood before diving in."
  - anchor: py-st-general-rules
    what: "Where annotations are due: public APIs, error-prone or hard-to-read code, stabilized surfaces; `self`/`cls` left bare or `Self`, `__init__` return unannotated, `Any` for inexpressible types."
    problem: "Agent annotates everything dogmatically or nothing at all; ceremony buries obvious functions, holes persist where bugs breed, checker value never materializes; annotation triage, public surface, error proneness, stability signal, ceremony burden, self handling, init return, selective coverage."
    use_when: "Prioritizing which functions get annotations; handling `self`, `cls`, or `__init__` signatures; falling back to `Any`."
    avoid_when: "Formatting annotated signatures — line-breaking rules apply; alias or TypeVar specifics."
    expected: "Public and risky code carries annotations; trivial paths stay clean, with `Any` marking honest gaps."
  - anchor: py-st-line-breaking
    what: "Wrapping annotated signatures: one parameter per line, comma after final parameter, breaks between variables never inside names, types kept unbroken."
    problem: "Agent wraps long signatures mid-type or crams parameters around return annotation; mangled breaks defeat readability, diffs sprawl, closing parens drift into weird alignments; column budget, parameter-per-line, trailing comma, return placement, type splitting, bracket orientation, change noise, layout entropy."
    use_when: "Reformatting an annotated `def` that overflows; placing the return type; deciding where a too-long type may break."
    avoid_when: "Unannotated signatures — general indentation rules suffice; docstring wrapping."
    expected: "Annotated signatures break cleanly per parameter with intact types and tidy terminal delimiters."
  - anchor: py-st-forward-declarations
    what: "Referencing not-yet-defined classes via `from __future__ import annotations` or quoted class names."
    problem: "Agent annotates with classes defined later in module and hits name errors at import; evaluation order breaks otherwise clean code, workarounds multiply inconsistently; undefined name, binding timing, future import, quoted annotation, load failure, self reference, definition sequencing, runtime resolution."
    use_when: "Annotating with same-module classes defined below; picking deferred evaluation versus string form."
    avoid_when: "Cross-module typing-only imports — conditional-import rules apply; Python versions already deferring evaluation."
    expected: "Annotations referencing later definitions evaluate cleanly and modules load without errors."
  - anchor: py-st-default-values
    what: "Spacing around `=` in annotated defaults: `a: int = 0` spaced, unannotated `a=0` tight, per PEP-008."
    problem: "Agent applies one spacing habit to every default; annotated signatures get cramped or unannotated ones padded, linter noise drowns real findings; kwarg layout, annotation interaction, equals padding, signature typography, style alerts, PEP-008 nuance, squeezed values, habit mismatch."
    use_when: "Writing parameters that combine annotation and default; reviewing `=` spacing in signatures."
    avoid_when: "Unannotated keyword calls — whitespace rules cover plain `=`; body-level assignments."
    expected: "Annotated defaults show spaced `=`, unannotated stay tight, consistently across signatures."
  - anchor: py-st-nonetype
    what: "Declared nullability: `X | None` (3.10+) or `Optional`/`Union`, `None` as alias for `NoneType`, implicit `a: str = None` banned."
    problem: "Agent leaves nullability implicit or defaults unannotated params to `None`; checkers miss real bugs, callers discover null crashes in production, legacy implicit style persists; explicit nullability, union syntax, unstated optionality, runtime blowup, checker blindness, legacy optional, declared contract, production surprise."
    use_when: "Declaring parameters or returns that may be `None`; choosing `|` unions versus `Optional`; modernizing legacy defaults."
    avoid_when: "Non-nullable values — no annotation ceremony needed; generic null-object patterns."
    expected: "Every nullable parameter declares `| None` explicitly; no bare `= None` on typed-as-`str` params."
  - anchor: py-st-type-aliases
    what: "Named aliases for complex types via `: TypeAlias` (3.10+), `CapWorded` public names, `_Private` for module-local ones."
    problem: "Agent repeats monstrous type expressions across signatures; drift creeps between copies, refactors touch dozens of sites, readers parse walls of brackets; alias naming, copy proliferation, divergent duplicates, refactor blast radius, nested generics, private visibility, shared vocabulary, signature economy."
    use_when: "A complex type recurs across signatures; naming shared composite types; keeping internal composites behind `_Private`."
    avoid_when: "One-off simple annotations; generic parameterization — TypeVar territory."
    expected: "Complex types have single named aliases; signatures stay short and consistent."
  - anchor: py-st-ignoring-types
    what: "Suppressing checker complaints via `# type: ignore` per line or `pytype`'s error-specific `disable` option."
    problem: "Agent silences checkers broadly to green builds; suppression blankets hide real defects, ignores accumulate unreviewed, error classes vanish from radar; suppression scope, ci greenwash, masked bugs, deadline pressure, error specificity, unreviewed debt, radar loss, targeted disable."
    use_when: "A line genuinely cannot satisfy the checker; narrowing suppression to one pytype error category."
    avoid_when: "Fixable annotation errors — fix the type instead; whole-file suppression."
    expected: "Suppressions stay line-local and error-specific; nothing real hides behind ignores."
  - anchor: py-st-typing-variables
    what: "Hub for variable-level typing: when internal variables need explicit type help and which mechanism applies."
    problem: "Agent faces variables whose types checkers cannot infer and picks mechanisms blindly; wrong tool adds noise or legacy syntax, inference gaps stay unfixed; inference failure, variable annotation, mechanism choice, outdated forms, checker limits, locals typing, noise versus signal, routing decision."
    use_when: "A local's type resists inference; choosing between annotation styles for assignments."
    avoid_when: "Parameter and return typing — signature rules apply; fully inferrable assignments."
    expected: "Hard-to-infer variables get the right explicit mechanism; inferrable ones stay bare."
  - anchor: py-st-annotated-assignments
    what: "Annotated assignment syntax (`a: Foo = expr`) for internal variables whose type is hard or impossible to infer."
    problem: "Agent leaves opaque factory results untyped; checker infers `Any`, downstream errors surface far from source, refactors lose safety net; black-box call, checker blindness, distant failures, colon syntax, refactor exposure, factory calls, explicit binding, error displacement."
    use_when: "Assigning results of undecorated or factory functions; pinning a local's type the checker cannot derive."
    avoid_when: "Easily inferred literals and constructors; comment-style typing — that legacy form is banned."
    expected: "Opaque bindings carry inline annotated types; inference-based code stays unannotated."
  - anchor: py-st-type-comments
    what: "Ban on new `# type: <name>` trailing annotations, a legacy form from before annotation syntax."
    problem: "Agent copies comment-style annotations from old code or blog posts; legacy syntax confuses modern tooling, style drifts backward, two annotation dialects coexist; comment grammar, trailing note, pre-3.6 relic, tooling confusion, style regression, dialect mixing, copied idiom, modernization debt."
    use_when: "Spotting legacy type comments during review; modernizing old code to assignment annotations."
    avoid_when: "Reading legacy files without touching them; fresh code — use annotated assignment syntax."
    expected: "No new trailing type notes enter the codebase; modernized spots use real syntax."
  - anchor: py-st-tuples-vs-lists
    what: "Homogeneity rules: `list[T]` holds one type, `tuple[int, ...]` repeats one, `tuple[int, str, float]` fixes heterogeneous positions — the common multi-value return shape."
    problem: "Agent types heterogeneous collections as lists or fixed tuples loosely; checkers allow invalid mixes, return contracts blur, callers index blindly; homogeneous list, record shape, positional contract, multi-value outcome, ellipsis repetition, mixed elements, container typing, arity mismatch."
    use_when: "Typing collections; modeling fixed-arity heterogeneous returns; choosing ellipsis versus positional tuple forms."
    avoid_when: "Untyped quick scripts; mappings — dict semantics differ entirely."
    expected: "Lists carry single element types; tuples express repetition or exact positional shapes."
  - anchor: py-st-typevars
    what: "`TypeVar`/`ParamSpec` for generics: constraints and bounds, `AnyStr` for same-type `bytes`/`str`, descriptive names mandatory unless unconstrained and private (`_T`, `_P`)."
    problem: "Agent names type variables `T` on public constrained generics or skips them for any-heavy signatures; contracts collapse to anything-goes, decorator signatures lose parameter shapes, callers get no checking; variable naming, constraint expression, paramspec preservation, anystr uniformity, wrapper typing, bound declaration, contract precision, visibility rule."
    use_when: "Writing generic functions or decorators; constraining a `TypeVar`; keeping `bytes`/`str` uniform via `AnyStr`; naming private unconstrained variables."
    avoid_when: "Concrete non-generic signatures; simple aliases — alias rules are lighter."
    expected: "Generics carry descriptive or `_T`-style variables correctly scoped; constraints and `ParamSpec` shapes survive decoration."
  - anchor: py-st-string-types
    what: "String annotation choices: `str` for text, `bytes` for binary, `AnyStr` when all string types must match; `typing.Text` banned outside 2/3 compatibility."
    problem: "Agent annotates text with `Text` from old guides or conflates bytes with strings; encoding bugs slip through, APIs accept wrong payloads, compatibility relics spread; text versus bytes, encoding boundary, relic annotation, payload confusion, same-type matching, compatibility shim, binary data, guide rot."
    use_when: "Annotating text or binary parameters and returns; needing one name for uniformly-typed string generics; purging `Text`."
    avoid_when: "Python 2/3 straddle code — the relic survives there; non-string data."
    expected: "Text APIs take `str`, binary take `bytes`, uniform generics take `AnyStr`; `Text` appears only in straddle code."
  - anchor: py-st-imports-for-typing
    what: "Import discipline for typing symbols: direct symbol imports from `typing`/`collections.abc` (multi-name allowed), `import x as y` on collisions, abstractions like `Sequence` in signatures, built-in generics over `typing.List`."
    problem: "Agent imports typing modules wholesale or reaches for deprecated parametric aliases; namespaces collide with local names, signatures overcommit to concrete containers, old aliases rot; selective import, name collision, abstract containers, legacy generics, signature flexibility, keyword treatment, tight binding, namespace hygiene."
    use_when: "Importing typing symbols; resolving identifier clashes; choosing container types for signatures; replacing `typing.List`/`typing.Tuple`."
    avoid_when: "Runtime-only imports with no typing role; conditional typing imports — the `TYPE_CHECKING` card covers placement."
    expected: "Typing symbols import directly with collision aliases; signatures prefer abstractions and native containers."
  - anchor: py-st-conditional-imports
    what: "`if TYPE_CHECKING:` blocks for typing-only imports: quoted references, placed after normal imports, sorted without blank lines, discouraged when refactoring allows top-level."
    problem: "Agent needs types at check time but runtime import costs or cycles forbid it; eager imports slow startup or crash, annotations dangle unresolvable; check-time-only symbols, import-time overhead, string references, block placement, sorted list, startup weight, cycle avoidance, last-resort pattern."
    use_when: "An annotation needs a symbol unavailable at runtime; structuring the `TYPE_CHECKING` block correctly."
    avoid_when: "Refactoring can hoist the import to top level — preferred path; runtime-needed symbols."
    expected: "Typing-only imports live in one sorted `TYPE_CHECKING` block with string annotations; runtime stays lean."
  - anchor: py-st-circular-dependencies
    what: "Typing-driven circular imports treated as smell: refactor, or alias the module to `Any` (attributes stay `Any`) when build systems block the import."
    problem: "Agent hits import cycles created purely by annotations; build graphs reject such edges, modules deadlock at load, workarounds fork per file; typing edge, dependency graph, startup freeze, design odor, any substitution, meaningful alias, blocked edge, module interlock."
    use_when: "Annotations create an import cycle; build tooling forbids the edge and refactoring is not yet viable."
    avoid_when: "A clean refactor can break the cycle — always the first choice; non-typing cycles."
    expected: "Typing cycles disappear through refactor, or an `Any` alias keeps annotations readable when blocked."
  - anchor: py-st-generics
    what: "Parameterizing generics in signatures: bare `Sequence`/`Mapping` silently mean `Any`; explicit `Sequence[Any]` still loses to `TypeVar` when positions relate."
    problem: "Agent leaves generic containers unparameterized; element types evaporate to `Any`, checker approves nonsense, call sites lose autocomplete and validation; bare generic, implicit any, parameter inference, type dissolution, false acceptance, editor blindness, relation capture, container holes."
    use_when: "Annotating with generic containers; deciding between explicit `Any` and a `TypeVar` for linked positions."
    avoid_when: "Non-generic concrete types; genuinely opaque `Any` where no relation exists."
    expected: "Generics carry parameters everywhere; related positions share a `TypeVar` instead of `Any`."
  - anchor: py-st-type-stubs
    what: "Stub `.pyi` files as the annotation vehicle for third-party or extension modules that cannot carry their own hints."
    problem: "Agent must type calls into compiled or third-party modules lacking hints; inline guesses rot against releases, checker complains or shrugs, boundaries stay opaque; stub files, compiled extensions, hint vacuum, external boundaries, release drift, untyped surface, sidecar types, vendor wrapping."
    use_when: "Annotating against third-party or compiled modules without hints; placing `.pyi` stubs."
    avoid_when: "First-party code — annotate sources directly; modules already shipping native types."
    expected: "External modules gain types through `.pyi` stubs; first-party sources stay annotated inline."
---

# 2. Python Style Rules

## 2.1 Semicolons
[ref: #py-st-semicolons]

- Do NOT terminate lines with semicolons.
- Do NOT use semicolons to put two statements on the same line.

---

## 2.2 Line Length
[ref: #py-st-line-length]

- Maximum line length is **80 characters**.
- Explicit exceptions:
  - Long import statements.
  - URLs, pathnames, or long flags in comments.
  - Long string module-level constants not containing whitespace (e.g., URLs or pathnames) that would be inconvenient to split.
  - Pylint disable comments (e.g., `# pylint: disable=invalid-name`).
- Do NOT use a backslash for explicit line continuation. Use Python's implicit line joining inside parentheses, brackets, and braces. If necessary, add an extra pair of parentheses around an expression.
- Backslash-escaped newlines within strings are allowed.
- When a literal string won't fit on one line, use parentheses for implicit line joining.
- Prefer to break lines at the highest possible syntactic level. If you must break a line twice, break it at the same syntactic level both times.
- Within comments, put long URLs on their own line if necessary.
- Docstring summary lines must remain within the 80 character limit.
- If Black or Pyink cannot bring a line below 80, the line may exceed the limit; authors should manually break the line when sensible.

```python
# Yes
foo_bar(self, width, height, color='black', design=None, x='foo',
        emphasis=None, highlight=0)

if (width == 0 and height == 0 and
        color == 'red' and emphasis == 'strong'):

    (bridge_questions.clarification_on
     .average_airspeed_of.unladen_swallow) = 'African or European?'

    with (
        very_long_first_expression_function() as spam,
        very_long_second_expression_function() as beans,
        third_thing() as eggs,
    ):
        place_order(eggs, beans, spam, beans)

# No
if width == 0 and height == 0 and \
        color == 'red' and emphasis == 'strong':

    bridge_questions.clarification_on \
        .average_airspeed_of.unladen_swallow = 'African or European?'

    with very_long_first_expression_function() as spam, \
          very_long_second_expression_function() as beans, \
          third_thing() as eggs:
        place_order(eggs, beans, spam, beans)
```

Prefer to break lines at the highest possible syntactic level. If you must break a line twice, break it at the same syntactic level both times.

```python
# Yes
bridgekeeper.answer(
    name="Arthur", quest=questlib.find(owner="Arthur", perilous=True))

answer = (a_long_line().of_chained_methods()
          .that_eventually_provides().an_answer())

if (
    config is None
    or 'editor.language' not in config
    or config['editor.language'].use_spaces is False
):
    use_tabs()

# No
bridgekeeper.answer(name="Arthur", quest=questlib.find(
        owner="Arthur", perilous=True))

answer = a_long_line().of_chained_methods().that_eventually_provides(
    ).an_answer()

if (config is None or 'editor.language' not in config or config[
    'editor.language'].use_spaces is False):
    use_tabs()
```

Within comments, put long URLs on their own line if necessary.

```python
# Yes
# See details at
# http://www.example.com/us/developer/documentation/api/content/v2.0/csv_file_name_extension_full_specification.html

# No
# See details at
# http://www.example.com/us/developer/documentation/api/content/\
# v2.0/csv_file_name_extension_full_specification.html
```

---

## 2.3 Parentheses
[ref: #py-st-parentheses]

- Use parentheses sparingly.
- It is fine, though not required, to use parentheses around tuples.
- Do NOT use them in return statements or conditional statements unless using parentheses for implied line continuation or to indicate a tuple.

```python
# Yes
if foo:
    bar()
while x:
    x = bar()
if x and y:
    bar()
if not x:
    bar()
onesie = (foo,)
return foo
return spam, beans
return (spam, beans)
for (x, y) in dict.items(): ...

# No
if (x):
    bar()
if not(x):
    bar()
return (foo)
```

---

## 2.4 Indentation
[ref: #py-st-indentation]

- Indent code blocks with **4 spaces**.
- Never use tabs.
- Implied line continuation should align wrapped elements vertically, or use a hanging 4-space indent.
- Closing brackets can be placed at the end of the expression or on separate lines, but if on separate lines they should be indented the same as the line with the corresponding opening bracket.

```python
# Yes — Aligned with opening delimiter
foo = long_function_name(var_one, var_two,
                         var_three, var_four)
meal = (spam,
        beans)

foo = {
    'long_dictionary_key': value1 +
                           value2,
    ...
}

# Yes — 4-space hanging indent; nothing on first line
foo = long_function_name(
    var_one, var_two, var_three,
    var_four)
meal = (
    spam,
    beans)

# Yes — 4-space hanging indent; closing parenthesis on new line
foo = long_function_name(
    var_one, var_two, var_three,
    var_four
)
meal = (
    spam,
    beans,
)

# Yes — 4-space hanging indent in dictionary
foo = {
    'long_dictionary_key':
        long_dictionary_value,
    ...
}

# No — Stuff on first line forbidden
foo = long_function_name(var_one, var_two,
    var_three, var_four)
meal = (spam,
    beans)

# No — 2-space hanging indent forbidden
foo = long_function_name(
  var_one, var_two, var_three,
  var_four)

# No — No hanging indent in dictionary
foo = {
    'long_dictionary_key':
    long_dictionary_value,
    ...
}
```

### 2.4.1 Trailing Commas in Sequences of Items
- Trailing commas are recommended only when the closing container token `]`, `)`, or `}` does not appear on the same line as the final element, as well as for tuples with a single element.
- The presence of a trailing comma is also used as a hint to auto-formatters (Black/Pyink) to format the container to one item per line.

```python
# Yes
golomb3 = [0, 1, 3]
golomb4 = [
    0,
    1,
    4,
    6,
]

# No
golomb4 = [
    0,
    1,
    4,
    6,]
```

---

## 2.5 Blank Lines
[ref: #py-st-blank-lines]

- Two blank lines between top-level definitions (function or class).
- One blank line between method definitions and between the docstring of a `class` and the first method.
- No blank line following a `def` line.
- Use single blank lines as appropriate within functions or methods.
- Blank lines need not be anchored to the definition. Related comments immediately preceding definitions can make sense; consider if the comment might be more useful as part of the docstring.

---

## 2.6 Whitespace
[ref: #py-st-whitespace]

Follow standard typographic rules for spaces around punctuation.

- No whitespace inside parentheses, brackets, or braces.
- No whitespace before a comma, semicolon, or colon.
- Do use whitespace after a comma, semicolon, or colon, except at the end of a line.
- No whitespace before the open paren/bracket that starts an argument list, indexing, or slicing.
- No trailing whitespace.
- Surround binary operators with a single space on either side for assignment (`=`), comparisons (`==`, `<`, `>`, `!=`, `<=`, `>=`, `in`, `not in`, `is`, `is not`), and Booleans (`and`, `or`, `not`).
- Use judgment for arithmetic operators (`+`, `-`, `*`, `/`, `//`, `%`, `**`, `@`).
- NEVER use spaces around `=` when passing keyword arguments or defining a default parameter value, **except** when a type annotation is present — then DO use spaces around the `=` for the default parameter value.
- Do NOT use spaces to vertically align tokens on consecutive lines (applies to `:`, `#`, `=`, etc.).

```python
# Yes
spam(ham[1], {'eggs': 2}, [])

if x == 4:
    print(x, y)
x, y = y, x

spam(1)
dict['key'] = list[index]

x == 1

def complex(real, imag=0.0): return Magic(r=real, i=imag)
def complex(real, imag: float = 0.0): return Magic(r=real, i=imag)

foo = 1000  # comment
long_name = 2  # comment that should not be aligned

dictionary = {
    'foo': 1,
    'long_name': 2,
}

# No
spam( ham[ 1 ], { 'eggs': 2 }, [ ] )

if x == 4 :
    print(x , y)
x , y = y , x

spam (1)
dict ['key'] = list [index]

x<1

def complex(real, imag = 0.0): return Magic(r = real, i = imag)
def complex(real, imag: float=0.0): return Magic(r = real, i = imag)

foo       = 1000  # comment
long_name = 2     # comment that should not be aligned

dictionary = {
    'foo'      : 1,
    'long_name': 2,
}
```

---

## 2.7 Shebang Line
[ref: #py-st-shebang-line]

- Most `.py` files do not need a `#!` line.
- Start the main file of a program with `#!/usr/bin/env python3` (supports virtualenvs) or `#!/usr/bin/python3` per PEP-394.
- This line is ignored by Python when importing modules. It is only necessary on a file intended to be executed directly.

---

## 2.8 Comments and Docstrings
[ref: #py-st-comments-and-docstrings]

Use the right style for module, function, method docstrings, and inline comments.

### 2.8.1 Docstrings
[ref: #py-st-docstrings]

- Python uses docstrings to document code. A docstring is the first statement in a package, module, class, or function.
- Always use the three-double-quote `"""` format (PEP 257).
- A docstring should be organized as:
  1. Summary line (one physical line, not exceeding 80 characters), terminated by a period, question mark, or exclamation point.
  2. Blank line.
  3. Rest of the docstring starting at the same cursor position as the first quote of the first line.
- There are more formatting guidelines below.

### 2.8.2 Modules
[ref: #py-st-comments-in-modules]

- Every file should contain license boilerplate appropriate for the project license.
- Files should start with a docstring describing the contents and usage of the module.

```python
"""A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.function_bar()
"""
```

#### 2.8.2.1 Test Modules
[ref: #py-st-test-modules]

- Module-level docstrings for test files are not required.
- Include them only when there is additional information (how to run the test, unusual setup, external environment dependencies, etc.).
- Docstrings that do not provide any new information should not be used.

```python
"""Tests for foo.bar."""
```

### 2.8.3 Functions and Methods
[ref: #py-st-functions-and-methods]

In this section, "function" means method, function, generator, or property.

- A docstring is **mandatory** for every function that has one or more of:
  - being part of the public API
  - nontrivial size
  - non-obvious logic
- The docstring must give enough information to write a call to the function without reading its code.
- Describe calling syntax and semantics, not implementation details, unless those details are relevant to usage (e.g., side effects on arguments).
- The docstring may be descriptive-style (`"""Fetches rows from a Bigtable."""`) or imperative-style (`"""Fetch rows from a Bigtable."""`), but the style must be consistent within a file.
- The docstring for a `@property` data descriptor should use the same style as for an attribute or function argument (`"""The Bigtable path."""`, not `"""Returns the Bigtable path."""`).
- Special sections (Args, Returns, Raises, Yields, etc.) begin with a heading line ending with a colon.
- All sections other than the heading should maintain a hanging indent of two or four spaces (be consistent within a file).
- These sections can be omitted when the function's name and signature are informative enough.

#### Args:
[ref: #py-st-doc-function-args]

- List each parameter by name. A description follows the name, separated by a colon and space or newline.
- If the description is too long for an 80-character line, use a hanging indent of 2 or 4 spaces more than the parameter name (be consistent with the rest of the file).
- Include required type(s) if the code does not contain a corresponding type annotation.
- If a function accepts `*foo` (variable length argument lists) or `**bar`, document those as `*foo` and `**bar`.

#### Returns: (or Yields: for generators)
[ref: #py-st-doc-function-returns]

- Describe the type and semantics of the return value.
- Must not be present if the function only returns `None`.
- May be omitted if the docstring starts with "Returns" or "Yields" (e.g., `"""Returns the row from the dataset."""`).
- For complex return types, describe the structure if not obvious.

#### Raises:
[ref: #py-st-doc-function-raises]

- List all exceptions that are relevant to the interface and that the caller should be aware of.
- Do NOT document `ValueError` raised on invalid API usage if that is a programming error; only document exceptions that are part of the contract.

```python
def fetch_smalltable_rows(
    table_handle: smalltable.Table,
    keys: Sequence[bytes | str],
    require_all_keys: bool = False,
) -> Mapping[bytes, tuple[str, ...]]:
    """Fetches rows from a Smalltable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by table_handle.  String keys will be UTF-8 encoded.

    Args:
        table_handle: An open smalltable.Table instance.
        keys: A sequence of strings representing the key of each table
          row to fetch.  String keys will be UTF-8 encoded.
        require_all_keys: If True only rows with values set for all keys will be
          returned.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {b'Serak': ('Rigel VII', 'Preparer'),
         b'Zim': ('Irk', 'Invader'),
         b'Lrrr': ('Omicron Persei 8', 'Emperor')}

        Returned keys are always bytes.  If a key from the keys argument is
        missing from the dictionary, then that row was not found in the
        table (and require_all_keys must have been False).

    Raises:
        IOError: An error occurred accessing the smalltable.
    """
```

#### 2.8.3.1 Overridden Methods
[ref: #py-st-overridden-methods]

- A method that overrides a base class method does **not** need a docstring if it is explicitly decorated with `@override` (from `typing_extensions` or `typing`), **unless** the overriding method's behavior materially refines the base method's contract or additional details are needed (e.g., side effects).
- If the overriding method is not decorated with `@override`, a docstring is required.
- A trivial docstring like `"""See base class."""` is acceptable when `@override` is present but not sufficient on its own without `@override`.

```python
from typing_extensions import override

class Parent:
    def do_something(self):
        """Parent method, includes docstring."""

class Child(Parent):
    @override
    def do_something(self):
        pass

# Child class, but without @override decorator, a docstring is required.
class Child(Parent):
    def do_something(self):
        pass

# Docstring is trivial; @override is sufficient to indicate that docs can be
# found in the base class.
class Child(Parent):
    @override
    def do_something(self):
        """See base class."""
```

### 2.8.4 Classes
[ref: #py-st-comments-in-classes]

- Classes should have a docstring below the class definition describing the class.
- Public attributes (excluding properties) should be documented in an `Attributes` section, following the same formatting as a function's `Args`.
- All class docstrings should start with a one-line summary describing what the class instance represents.
- Subclasses of `Exception` should describe what the exception represents, not the context in which it might occur.
- Do NOT repeat unnecessary information (e.g., "class that describes...").

```python
class SampleClass:
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam: bool = False):
        """Initializes the instance based on spam preference.

        Args:
          likes_spam: Defines if instance exhibits this preference.
        """
        self.likes_spam = likes_spam
        self.eggs = 0

    @property
    def butter_sticks(self) -> int:
        """The number of butter sticks we have."""

# Yes
class CheeseShopAddress:
    """The address of a cheese shop.

    ...
    """

class OutOfCheeseError(Exception):
    """No more cheese is available."""

# No
class CheeseShopAddress:
    """Class that describes the address of a cheese shop.

    ...
    """

class OutOfCheeseError(Exception):
    """Raised when no more cheese is available."""
```

### 2.8.5 Block and Inline Comments
[ref: #py-st-block-and-inline-comments]

- Add comments to tricky parts of the code. If you will have to explain it at the next code review, comment it now.
- Complicated operations get a few lines of comments before they commence.
- Non-obvious operations get comments at the end of the line.
- Comments should start at least 2 spaces away from the code, with `#` followed by at least one space.
- NEVER describe the code. Assume the reader knows Python better than you do.

```python
# We use a weighted dictionary search to find out where i is in
# the array.  We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.

if i & (i-1) == 0:  # True if i is 0 or a power of 2.
```

```python
# BAD COMMENT: Now go through the b array and make sure whenever i occurs
# the next element is i+1
```

### 2.8.6 Punctuation, Spelling, and Grammar
[ref: #py-st-punctuation-spelling-and-grammar]

- Pay attention to punctuation, spelling, and grammar.
- Comments should be as readable as narrative text, with proper capitalization and punctuation.
- Complete sentences are more readable than sentence fragments.
- Shorter end-of-line comments can be less formal, but be consistent.
- Source code must maintain a high level of clarity and readability.

---

## 2.10 Strings
[ref: #py-st-strings]

- Use an f-string, the `%` operator, or the `format` method for formatting strings, even when the parameters are all strings.
- Use your best judgment to decide between formatting options.
- A single join with `+` is okay, but do NOT format with `+`.
- Avoid using `+` and `+=` to accumulate a string within a loop. Use a list and `''.join`, or an `io.StringIO` buffer.
- Be consistent with your choice of string quote character within a file. Pick `'` or `"` and stick with it.
- It is okay to use the other quote character to avoid backslash-escaping quotes within the string.
- Prefer `"""` for multi-line strings rather than `'''`. Projects may choose to use `'''` for all non-docstring multi-line strings if and only if they also use `'` for regular strings.
- Docstrings MUST use `"""` regardless.
- Multi-line strings do not flow with the indentation of the rest of the program. If you need to avoid embedding extra space, use concatenated single-line strings or a multi-line string with `textwrap.dedent()`.
- Note that using a backslash inside string literals to escape newlines does not violate the prohibition against explicit line continuation.

```python
# Yes
x = f'name: {name}; score: {n}'
x = '%s, %s!' % (imperative, expletive)
x = '{}, {}'.format(first, second)
x = 'name: %s; score: %d' % (name, n)
x = 'name: %(name)s; score: %(score)d' % {'name': name, 'score': n}
x = 'name: {}; score: {}'.format(name, n)
x = a + b

items = ['<table>']
for last_name, first_name in employee_list:
    items.append('<tr><td>%s, %s</td></tr>' % (last_name, first_name))
items.append('</table>')
employee_table = ''.join(items)

Python('Why are you hiding your eyes?')
Gollum("I'm scared of lint errors.")
Narrator('"Good!" thought a happy Python reviewer.')

long_string = """This is fine if your use case can accept
    extraneous leading spaces."""

long_string = ("And this is fine if you cannot accept\n" +
               "extraneous leading spaces.")

long_string = ("And this too is fine if you cannot accept\n"
               "extraneous leading spaces.")

import textwrap
long_string = textwrap.dedent("""\
    This is also fine, because textwrap.dedent()
    will collapse common leading spaces in each line.""")

# No
x = first + ', ' + second
x = 'name: ' + name + '; score: ' + str(n)

employee_table = '<table>'
for last_name, first_name in employee_list:
    employee_table += '<tr><td>%s, %s</td></tr>' % (last_name, first_name)
employee_table += '</table>'

Python("Why are you hiding your eyes?")
Gollum('The lint. It burns. It burns us.')
Gollum("Always the great lint. Watching. Watching.")

long_string = """This is pretty ugly.
Don't do this.
"""
```

### 2.10.1 Logging
[ref: #py-st-logging]
- For logging functions that expect a pattern-string (with `%-placeholders`) as their first argument: ALWAYS call them with a string literal (NOT an f-string!) as the first argument, with pattern-parameters as subsequent arguments.
- Some logging implementations collect the unexpanded pattern-string as a queryable field.
- This prevents rendering a message that no logger is configured to output.

```python
# Yes
import tensorflow as tf
logger = tf.get_logger()
logger.info('TensorFlow Version is: %s', tf.__version__)

import os
from absl import logging
logging.info('Current $PAGER is: %s', os.getenv('PAGER', default=''))

homedir = os.getenv('HOME')
if homedir is None or not os.access(homedir, os.W_OK):
    logging.error('Cannot write to home directory, $HOME=%r', homedir)

# No
import os
from absl import logging
logging.info('Current $PAGER is:')
logging.info(os.getenv('PAGER', default=''))

homedir = os.getenv('HOME')
if homedir is None or not os.access(homedir, os.W_OK):
    logging.error(f'Cannot write to home directory, $HOME={homedir!r}')
```

### 2.10.2 Error Messages
Error messages (e.g., on exceptions like `ValueError`, or messages shown to the user) must follow three guidelines:

1. The message needs to precisely match the actual error condition.
2. Interpolated pieces need to always be clearly identifiable as such.
3. They should allow simple automated processing (e.g., grepping).

```python
# Yes
if not 0 <= p <= 1:
    raise ValueError(f'Not a probability: {p=}')

try:
    os.rmdir(workdir)
except OSError as error:
    logging.warning('Could not remove directory (reason: %r): %r',
                    error, workdir)

# No
if p < 0 or p > 1:  # PROBLEM: also false for float('nan')!
    raise ValueError(f'Not a probability: {p=}')

try:
    os.rmdir(workdir)
except OSError:
    # PROBLEM: Message makes an assumption that might not be true:
    # Deletion might have failed for some other reason, misleading
    # whoever has to debug this.
    logging.warning('Directory already was deleted: %s', workdir)

try:
    os.rmdir(workdir)
except OSError:
    # PROBLEM: The message is harder to grep for than necessary, and
    # not universally non-confusing for all possible values of `workdir`.
    # Imagine someone calling a library function with such code
    # using a name such as workdir = 'deleted'. The warning would read:
    # "The deleted directory could not be deleted."
    logging.warning('The %s directory could not be deleted.', workdir)
```

---

## 2.11 Files, Sockets, and Similar Stateful Resources
[ref: #py-st-files-sockets-closeables]

- Explicitly close files and sockets when done.
- This extends to closeable resources that internally use sockets (DB connections) and other resources needing similar shutdown (mmap mappings, h5py File objects, matplotlib.pyplot figure windows).
- Do NOT rely on `__del__` for cleanup:
  - No guarantee when `__del__` is invoked.
  - Different Python implementations use different memory management.
  - Unexpected references may keep objects alive longer than intended.
- The preferred way is using the `with` statement.
- For file-like objects that do not support `with`, use `contextlib.closing()`.
- In rare cases where context-based resource management is infeasible, document clearly how resource lifetime is managed.

```python
with open("hello.txt") as hello_file:
    for line in hello_file:
        print(line)

import contextlib
with contextlib.closing(urllib.urlopen("http://www.python.org/")) as front_page:
    for line in front_page:
        print(line)
```

---

## 2.12 TODO Comments
[ref: #py-st-todo-comments]

- Use `TODO` comments for temporary code, short-term solutions, or good-enough-but-not-perfect code.
- A `TODO` comment begins with `TODO` in all caps, a following colon, and a link to a resource containing context (ideally a bug reference).
- Follow the context with an explanatory string introduced with a hyphen `-`.
- Purpose: consistent `TODO` format searchable for more details.

```python
# TODO: crbug.com/192795 - Investigate cpufreq optimizations.
```

- Old style (formerly recommended, now discouraged for new code):
  ```python
  # TODO(crbug.com/192795): Investigate cpufreq optimizations.
  # TODO(yourusername): Use a "*" here for concatenation operator.
  ```
- Avoid TODOs that refer to an individual or team as the context.
- If the TODO is of the form "At a future date do something", include a very specific date or a very specific event that future maintainers will comprehend. Issues are ideal for tracking this.

---

## 2.13 Imports Formatting
[ref: #py-st-imports-formatting]

- Imports should be on separate lines; exceptions for `typing` and `collections.abc` imports are allowed.
- Imports are always put at the top of the file, just after any module comments and docstrings, and before module globals and constants.
- Group imports from most generic to least generic:
  1. Python future import statements (e.g., `from __future__ import annotations`).
  2. Python standard library imports (e.g., `import sys`).
  3. Third-party module or package imports (e.g., `import tensorflow as tf`).
  4. Code repository sub-package imports (e.g., `from otherproject.ai import mind`).
  5. Deprecated: application-specific imports that are part of the same top-level sub-package as this file. New code is encouraged not to bother with this; treat application-specific sub-package imports the same as other sub-package imports.
- Within each grouping, imports should be sorted lexicographically, ignoring case, according to each module's full package path.
- Code may optionally place a blank line between import sections.

```python
# Yes
from collections.abc import Mapping, Sequence
import os
import sys
from typing import Any, NewType

# No
import os, sys
```

```python
import collections
import queue
import sys

from absl import app
from absl import flags
import bs4
import cryptography
import tensorflow as tf

from book.genres import scifi
from myproject.backend import huxley
from myproject.backend.hgwells import time_machine
from myproject.backend.state_machine import main_loop
from otherproject.ai import body
from otherproject.ai import mind
from otherproject.ai import soul
```

---

## 2.14 Statements
[ref: #py-st-statements]

- Generally only one statement per line.
- You may put the result of a test on the same line as the test only if the entire statement fits on one line.
- You can NEVER do so with `try`/`except` since `try` and `except` can't both fit on the same line.
- You can only do so with an `if` if there is no `else`.

```python
# Yes
if foo: bar(foo)

# No
if foo: bar(foo)
else:   baz(foo)

try:               bar(foo)
except ValueError: baz(foo)

try:
    bar(foo)
except ValueError: baz(foo)
```

---

## 2.15 Accessors (Getters and Setters)
[ref: #py-st-accessors]

- Getter and setter functions should be used when they provide a meaningful role or behavior for getting or setting a variable's value.
- Use them when getting or setting is complex or the cost is significant.
- If a pair simply reads and writes an internal attribute, make the internal attribute public instead.
- If setting a variable invalidates or rebuilds state, it should be a setter function.
- Alternatively, properties may be an option when simple logic is needed.
- Getters and setters should follow Naming guidelines: `get_foo()` and `set_foo()`.
- If past behavior allowed access through a property, do NOT bind the new getter/setter functions to the property. Any code still attempting to access by the old method should break visibly.

---

## 2.16 Naming
[ref: #py-st-naming]

Names should be descriptive. Avoid abbreviation. Do not use abbreviations that are ambiguous or unfamiliar to readers outside your project, and do not abbreviate by deleting letters within a word. Always use a `.py` filename extension. Never use dashes.

Format examples: `module_name`, `package_name`, `ClassName`, `method_name`, `ExceptionName`, `function_name`, `GLOBAL_CONSTANT_NAME`, `global_var_name`, `instance_var_name`, `function_parameter_name`, `local_var_name`, `query_proper_noun_for_thing`, `send_acronym_via_https`.

### 2.16.1 Names to Avoid
[ref: #py-st-names-to-avoid]

- Single character names, EXCEPT for specifically allowed cases:
  - Counters or iterators (e.g., `i`, `j`, `k`, `v`, et al.)
  - `e` as an exception identifier in `try/except` statements.
  - `f` as a file handle in `with` statements.
  - Private type variables with no constraints (e.g., `_T = TypeVar("_T")`, `_P = ParamSpec("_P")`).
  - Names matching established notation in a reference paper or algorithm.
  - Be mindful not to abuse single-character naming. Descriptiveness should be proportional to the name's scope of visibility.
- Dashes (`-`) in any package/module name.
- `__double_leading_and_trailing_underscore__` names (reserved by Python).
- Offensive terms.
- Names that needlessly include the type of the variable (e.g., `id_to_name_dict`).

### 2.16.2 Naming Conventions
[ref: #py-st-naming-conventions]

- "Internal" means internal to a module, or protected or private within a class.
- Prepending a single underscore (`_`) has some support for protecting module variables and functions (linters will flag protected member access). It is okay for unit tests to access protected constants from modules under test.
- Prepending a double underscore (`__` aka "dunder") to an instance variable or method effectively makes it private (name mangling); discourage its use as it impacts readability and testability. Prefer a single underscore.
- Place related classes and top-level functions together in a module. Unlike Java, there is no need to limit yourself to one class per module.
- Use `CapWords` for class names, but `lower_with_under.py` for module names. Old `CapWords.py` modules exist but are now discouraged.
- New unit test files follow PEP 8 compliant `lower_with_under` method names: `test_<method_under_test>_<state>`. For consistency with legacy modules using `CapWords` function names, underscores may appear in method names starting with `test` to separate logical components (e.g., `test<MethodUnderTest>_<state>`).

### 2.16.3 File Naming
[ref: #py-st-file-naming]

- Python filenames must have a `.py` extension and must not contain dashes (`-`).
- This allows them to be imported and unittested.
- If you want an executable accessible without the extension, use a symbolic link or a simple bash wrapper containing `exec "$0.py" "$@"`.

### 2.16.4 Guidelines Derived from Guido's Recommendations
[ref: #py-st-guidelines-derived-from-guidos-recommendations]

| Type | Public | Internal |
|---|---|---|
| Packages | `lower_with_under` | |
| Modules | `lower_with_under` | `_lower_with_under` |
| Classes | `CapWords` | `_CapWords` |
| Exceptions | `CapWords` | |
| Functions | `lower_with_under()` | `_lower_with_under()` |
| Global/Class Constants | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER` |
| Global/Class Variables | `lower_with_under` | `_lower_with_under` |
| Instance Variables | `lower_with_under` | `_lower_with_under` (protected) |
| Method Names | `lower_with_under()` | `_lower_with_under()` (protected) |
| Function/Method Parameters | `lower_with_under` | |
| Local Variables | `lower_with_under` | |

### 2.16.5 Mathematical Notation
[ref: #py-st-math-notation]

- For mathematically-heavy code, short variable names that would otherwise violate the style guide are preferred when they match established notation in a reference paper or algorithm.
- Cite the source of naming conventions, preferably with a hyperlink, in a comment or docstring.
- Prefer PEP8-compliant `descriptive_names` for public APIs.
- Use a narrowly-scoped `pylint: disable=invalid-name` directive to silence warnings.

---

## 2.17 Main
[ref: #py-st-main]

- `pydoc` and unit tests require modules to be importable.
- If a file is meant to be used as an executable, its main functionality should be in a `main()` function.
- Always check `if __name__ == '__main__':` before executing the main program.
- When using `absl`, use `app.run`:

```python
from absl import app
...

def main(argv: Sequence[str]):
    # process non-flag arguments
    ...

if __name__ == '__main__':
    app.run(main)
```

- Otherwise:

```python
def main():
    ...

if __name__ == '__main__':
    main()
```

- Be careful not to call functions, create objects, or perform other operations at the top level that should not execute when the file is being `pydoc`ed.

---

## 2.18 Function Length
[ref: #py-st-function-length]

- Prefer small and focused functions.
- No hard limit on function length.
- If a function exceeds about 40 lines, think about whether it can be broken up without harming program structure.
- Keeping functions short and simple makes them easier to read and modify.
- Do not be intimidated by modifying existing long functions; if working with such a function proves difficult, consider breaking it into smaller pieces.

---

## 2.19 Type Annotations
[ref: #py-st-type-annotations]

### 2.19.1 General Rules
[ref: #py-st-general-rules]

- Familiarize yourself with type hints.
- Annotating `self` or `cls` is generally not necessary. `Self` can be used if necessary for proper type information.
- Do NOT feel compelled to annotate the return value of `__init__` (where `None` is the only valid option).
- If any other variable or returned type should not be expressed, use `Any`.
- You are not required to annotate all functions in a module.
  - At least annotate your public APIs.
  - Use judgment to balance safety/clarity vs. flexibility.
  - Annotate code prone to type-related errors (previous bugs or complexity).
  - Annotate code that is hard to understand.
  - Annotate code as it becomes stable from a types perspective.

```python
from typing import Self

class BaseClass:
    @classmethod
    def create(cls) -> Self:
        ...

    def difference(self, other: Self) -> float:
        ...
```

### 2.19.2 Line Breaking
[ref: #py-st-line-breaking]

- Follow existing indentation rules.
- After annotating, many function signatures become "one parameter per line".
- To ensure the return type gets its own line, place a comma after the last parameter.
- Always prefer breaking between variables, not between variable names and type annotations.
- If everything fits on one line, keep it on one line.
- If the combination of function name, last parameter, and return type is too long, indent by 4 in a new line.
- When using line breaks, prefer putting each parameter and the return type on their own lines, aligning the closing parenthesis with `def`.
- Optionally, the return type may be put on the same line as the last parameter.
- `pylint` allows moving the closing parenthesis to a new line and aligning with the opening one, but this is less readable.
- Prefer not to break types. If they are too long, keep sub-types unbroken.
- If a single name and type is too long, consider using a type alias. The last resort is to break after the colon and indent by 4.

```python
# Yes
def my_method(
    self,
    first_var: int,
    second_var: Foo,
    third_var: Bar | None,
) -> int:
    ...

# Yes (fits on one line)
def my_method(self, first_var: int) -> int:
    ...

# Yes
def my_method(
    self,
    other_arg: MyLongType | None,
) -> tuple[MyLongType1, MyLongType1]:
    ...

# Okay
def my_method(
    self,
    first_var: int,
    second_var: int) -> dict[OtherLongType, MyLongType]:
    ...

# No
def my_method(self,
              other_arg: MyLongType | None,
             ) -> dict[OtherLongType, MyLongType]:
    ...

# Yes (type too long, break after colon)
def my_function(
    long_variable_name:
        long_module_name.LongTypeName,
) -> None:
    ...

# No
def my_function(
    long_variable_name: long_module_name.
        LongTypeName,
) -> None:
    ...
```

As in the examples above, prefer not to break types. However, sometimes they are too long to be on a single line (try to keep sub-types unbroken).

```python
def my_method(
    self,
    first_var: tuple[list[MyLongType1],
                     list[MyLongType2]],
    second_var: list[dict[
        MyLongType3, MyLongType4]],
) -> None:
    ...
```

### 2.19.3 Forward Declarations
[ref: #py-st-forward-declarations]

- If you need to use a class name from the same module that is not yet defined, either use `from __future__ import annotations` or use a string for the class name.

```python
# Yes
from __future__ import annotations

class MyClass:
    def __init__(self, stack: Sequence[MyClass], item: OtherClass) -> None:
        ...

class OtherClass:
    ...

# Yes
class MyClass:
    def __init__(self, stack: Sequence['MyClass'], item: 'OtherClass') -> None:
        ...

class OtherClass:
    ...
```

### 2.19.4 Default Values
[ref: #py-st-default-values]

- As per PEP-008, use spaces around the `=` only for arguments that have both a type annotation and a default value.

```python
# Yes
def func(a: int = 0) -> int:
    ...

# No
def func(a:int=0) -> int:
    ...
```

### 2.19.5 NoneType
[ref: #py-st-nonetype]

- `NoneType` is a first-class type. For typing purposes, `None` is an alias for `NoneType`.
- If an argument can be `None`, it MUST be declared.
- Use `|` union type expressions (recommended in Python 3.10+), or older `Optional` and `Union` syntaxes.
- Use explicit `X | None` instead of implicit.
- Earlier type checkers allowed `a: str = None` to mean `a: str | None = None`; this is no longer preferred.

```python
# Yes
def modern_or_union(a: str | int | None, b: str | None = None) -> str:
    ...

def union_optional(a: Union[str, int, None], b: Optional[str] = None) -> str:
    ...

# No
def nullable_union(a: Union[None, str]) -> str:
    ...

def implicit_optional(a: str = None) -> str:
    ...
```

### 2.19.6 Type Aliases
[ref: #py-st-type-aliases]

- You can declare aliases of complex types.
- The name of an alias should be `CapWorded`.
- If the alias is used only in this module, it should be `_Private`.
- Note that `: TypeAlias` annotation is only supported in Python 3.10+.

```python
from typing import TypeAlias

_LossAndGradient: TypeAlias = tuple[tf.Tensor, tf.Tensor]
ComplexTFMap: TypeAlias = Mapping[str, _LossAndGradient]
```

### 2.19.7 Ignoring Types
[ref: #py-st-ignoring-types]

- You can disable type checking on a line with `# type: ignore`.
- `pytype` has a disable option for specific errors (similar to lint):
  ```python
  # pytype: disable=attribute-error
  ```

### 2.19.8 Typing Variables
[ref: #py-st-typing-variables]

#### Annotated Assignments:
[ref: #py-st-annotated-assignments]

- If an internal variable has a type that is hard or impossible to infer, specify its type with an annotated assignment: a colon and type between the variable name and value.

```python
a: Foo = SomeUndecoratedFunction()
```

#### Type Comments:
[ref: #py-st-type-comments]

- Do NOT add new uses of `# type: <type name>` comments. They were necessary before Python 3.6.

```python
# Do not add new instances of this:
a = SomeUndecoratedFunction()  # type: Foo
```

### 2.19.9 Tuples vs Lists
[ref: #py-st-tuples-vs-lists]

- Typed lists can only contain objects of a single type.
- Typed tuples can either have a single repeated type or a set number of elements with different types. The latter is commonly used as the return type from a function.

```python
a: list[int] = [1, 2, 3]
b: tuple[int, ...] = (1, 2, 3)
c: tuple[int, str, float] = (1, "2", 3.5)
```

### 2.19.10 Type Variables
[ref: #py-st-typevars]

- Use `TypeVar` and `ParamSpec` for generics.
- A `TypeVar` can be constrained.
- Use `AnyStr` for multiple annotations that can be `bytes` or `str` and must all be the same type.
- A type variable must have a descriptive name, UNLESS it meets ALL of the following:
  - not externally visible
  - not constrained

```python
from collections.abc import Callable
from typing import ParamSpec, TypeVar

_P = ParamSpec("_P")
_T = TypeVar("_T")

def next(l: list[_T]) -> _T:
    return l.pop()

def print_when_called(f: Callable[_P, _T]) -> Callable[_P, _T]:
    def inner(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        print("Function was called")
        return f(*args, **kwargs)
    return inner

# Constrained
AddableType = TypeVar("AddableType", int, float, str)
def add(a: AddableType, b: AddableType) -> AddableType:
    return a + b

# AnyStr
from typing import AnyStr
def check_length(x: AnyStr) -> AnyStr:
    if len(x) <= 42:
        return x
    raise ValueError()

# Yes
_T = TypeVar("_T")
_P = ParamSpec("_P")
AddableType = TypeVar("AddableType", int, float, str)
AnyFunction = TypeVar("AnyFunction", bound=Callable)

# No
T = TypeVar("T")
P = ParamSpec("P")
_T = TypeVar("_T", int, float, str)  # constrained must be descriptive
_F = TypeVar("_F", bound=Callable)
```

### 2.19.11 String Types
[ref: #py-st-string-types]

- Do NOT use `typing.Text` in new code. It is only for Python 2/3 compatibility.
- Use `str` for string/text data.
- Use `bytes` for binary data.
- If all string types of a function are always the same, use `AnyStr`.

```python
def deals_with_text_data(x: str) -> str:
    ...

def deals_with_binary_data(x: bytes) -> bytes:
    ...
```

### 2.19.12 Imports For Typing
[ref: #py-st-imports-for-typing]

- For symbols from `typing` or `collections.abc` used to support static analysis and type checking, always import the symbol itself.
- You are explicitly allowed to import multiple specific symbols on one line from `typing` and `collections.abc`.
- Treat names from `typing` or `collections.abc` similarly to keywords; do not define them in your Python code.
- If there is a collision between a type and an existing name, import it using `import x as y`.
- When annotating function signatures, prefer abstract container types like `collections.abc.Sequence` over concrete types like `list`.
- If you need a concrete type (e.g., a tuple of typed elements), prefer built-in types like `tuple` over parametric type aliases from `typing` (e.g., `typing.Tuple`).

```python
from collections.abc import Mapping, Sequence
from typing import Any, Generic, cast, TYPE_CHECKING

from typing import Any as AnyType

# Prefer abstract containers
def transform_coordinates(original: Sequence[tuple[float, float]]) -> Sequence[tuple[float, float]]:
    ...
```

```python
# No — prefer built-in generic types over typing module aliases
from typing import List, Tuple

def transform_coordinates(original: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    ...
```

### 2.19.13 Conditional Imports
[ref: #py-st-conditional-imports]

- Use conditional imports only in exceptional cases where additional imports needed for type checking must be avoided at runtime.
- This pattern is discouraged; prefer refactoring to allow top-level imports.
- Imports needed only for type annotations can be placed within `if TYPE_CHECKING:`.
- Conditionally imported types need to be referenced as strings, to be forward compatible with Python 3.6 where annotation expressions are evaluated.
- Only entities used solely for typing should be defined here (including aliases).
- The block should be right after all normal imports.
- There should be no empty lines in the typing imports list.
- Sort this list as if it were a regular imports list.

```python
import typing
if typing.TYPE_CHECKING:
    import sketch

def f(x: "sketch.Sketch"): ...
```

### 2.19.14 Circular Dependencies
[ref: #py-st-circular-dependencies]

- Circular dependencies caused by typing are code smells. Refactor if possible.
- If technically necessary but build systems prevent it, replace the module with `Any`.
- Set a meaningful alias and use the real type name from this module (any attribute of `Any` is `Any`).
- Alias definitions should be separated from the last import by one line.

```python
from typing import Any

some_mod = Any  # some_mod.py imports this module.
...

def my_method(self, var: "some_mod.SomeType") -> None:
    ...
```

### 2.19.15 Generics
[ref: #py-st-generics]

- When annotating, prefer to specify type parameters for generic types in a parameter list; otherwise parameters will be assumed to be `Any`.
- If the best type parameter for a generic is `Any`, make it explicit, but consider whether `TypeVar` might be more appropriate.

```python
# Yes
def get_names(employee_ids: Sequence[int]) -> Mapping[int, str]:
    ...

# No — interpreted as Sequence[Any] -> Mapping[Any, Any]
def get_names(employee_ids: Sequence) -> Mapping:
    ...

# No — Any is explicit but TypeVar is better
def get_names(employee_ids: Sequence[Any]) -> Mapping[Any, str]:
    """Returns a mapping from employee ID to employee name for given IDs."""

# Yes
_T = TypeVar('_T')
def get_names(employee_ids: Sequence[_T]) -> Mapping[_T, str]:
    """Returns a mapping from employee ID to employee name for given IDs."""
```

### 2.19.16 Build Dependencies
[ref: #py-st-type-stubs]

- Type annotations can be placed in stub `.pyi` files for third-party or extension modules.
- For code within the same repository, prefer inline annotations.
