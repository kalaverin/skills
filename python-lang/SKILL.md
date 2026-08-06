---
name: python-lang
description: MANDATORY skill for Python code. Use when writing, editing, refactoring, or reviewing Python files, modules, packages, classes, functions, type annotations, imports, exceptions, comprehensions, decorators, or docstrings. Enforces Google Python Style Guide and a mandatory, unconditional Ruff format+check pipeline scoped strictly to the agent's own changes.
triggers:
  files: "fd -e py -e pyi --max-results 1 | grep -q ."
requires:
  - frontmatter-protocol
  - read-for-comments
---

# SKILL: Strict Python Engineering & Compliance

You are an expert Python Engineer and a strict Code Reviewer. **This document is a binding rule set, not a recommendation.**
Every directive in this guide MUST be followed unless it explicitly uses **SHOULD** or **MAY**. The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when they appear in all capitals or in bold markup.

## 1. Compliance and Local Style

* **Default Rule:** Unless a section, paragraph, or sentence explicitly uses **SHOULD** or **MAY**, every statement is to be treated as **MUST**. If a coding situation is covered by this guide, you MUST follow the guide. You MUST NOT apply external style preferences or general Python heuristics in place of the rules documented here.
* **Consistency:** BE CONSISTENT. If you are editing code, ALWAYS look at the code around you and you MUST match its style. Local style is VERY IMPORTANT. If code you add looks drastically different from the existing code, it throws readers out of their rhythm. Consistency applies more heavily locally and on choices unspecified by the global style.
* **Deviation Justification:** If you deviate from any MUST directive, you MUST explicitly justify the deviation in your output.
* **Skill Boundary:** This skill covers Python language and style rules. For API resource design, HTTP/gRPC routes, and proto structure, consult the `api-design` skill.
* **RFC Verbs:** For precise semantics of requirement-level verbs, consult the `read-for-comments` skill.

***

## 2. Mandatory Lookups (Lazy-Load Protocol)

**This routing is mandatory.** When the task touches Python language or style rules, you MUST route through the corpus frontmatter before reading any body. Do not guess, do not rely on training data, and do not skip routing because the topic seems familiar. You MUST NOT read the reference files in their entirety.

**Corpus:**

- `references/01_language_rules.md` — Google language rules; 20 routable sections, anchors `py-lr-*`.
- `references/02_style_rules.md` — Google style rules; 53 routable sections including the subsection-level chapters 2.8 / 2.10 / 2.16 / 2.19, anchors `py-st-*`.
- `references/03_personal_rules.md` — project-specific rules that EXTEND and OVERRIDE the Google corpora on conflict, anchors `py-pr-*`. Its frontmatter is small: shortlist it on EVERY funnel pass so overrides are never missed.

**Toolchain precedence (HARD):** the corpus reproduces upstream Google text that references `pylint` and `pytype`. Those references are historical context only. The governing local toolchain is Ruff for lint/format (§3, mandatory) and mypy for type checking (`03_personal_rules.md`). Where a corpus section and this skill's §3 conflict, §3 wins; say so per §1 (Deviation Justification).

**Skill addendum (lazyload):** `prompts/REFERENCE_STANDARD_ADDENDUM.md` declares the two-tier anchor prefixes (`py-lr-`, `py-st-`, `py-pr-`), the tight `marker_style`, the Google-canon numbered-headings exemption, and the pseudo-heading legalization. Corpus frontmatter schema and card semantics defer to `frontmatter-protocol/references/lazyload.md`.

**Routing Funnel (per `frontmatter-protocol` `[ref: #lazy-load-routing]`):**
1. Run the subject map (Command 1) over `references/` and shortlist candidate files semantically — the request plus inferred session work; shortlist generously.
2. Read the full frontmatter of shortlisted files — `03_personal_rules.md` is always shortlisted — and match every card's `what` / `use_when` / `avoid_when` semantically (OR semantics); mark each matching card's `anchor`.
3. Deduplicate anchors, then extract each selected section with the canonical bounded extraction — never a blind `rg -A N` window.
4. Apply the extracted rules strictly.

***

## 3. Mandatory Lint & Format Pipeline (Unconditional Gate)

**MANDATORY — ALWAYS, WITHOUT REMINDERS:** For EVERY Python file the agent writes, creates, or edits, the agent MUST run this pipeline before declaring the task complete. This gate is unconditional: it applies in addition to — and independently of — any project-level linting, formatter configuration, pre-commit hooks, or CI checks present in the target project. The agent MUST NOT skip it because "the project has its own linting", MUST NOT wait for the user to ask, and MUST NOT consider the task done until both stages pass on the agent's own changes.

The pipeline is Ruff-only (`black`, `flake8`, and `isort` are forbidden per the `shell-protocol` skill) and has two mandatory stages, executed in this exact order:

1. **Format** — `ruff format` (black-compatible automatic formatting).
2. **Lint** — `ruff check --fix` (full-rule diagnostics WITH automatic in-place fixes; fixes scoped to the agent's own edits).

**`--fix` is a mandatory part of the pipeline (HARD):** the lint stage's FIRST invocation MUST carry `--fix`, letting Ruff rewrite auto-fixable violations in place. The agent MUST NOT hand-edit what `ruff check --fix` repairs mechanically — manual fixing of auto-fixable violations wastes tokens and energy and is a pipeline violation. Manual edits are reserved for diagnostics that `--fix` cannot repair.

**The `[*]` reminder rule (HARD):** the output line `[*] fixable with the \`--fix\` option.` means the previous run forgot `--fix`. On seeing it the agent MUST: (1) immediately recall that the first pass ALWAYS runs with `--fix`, and (2) immediately re-run the same command with `--fix` — before reading or hand-fixing any diagnostic. Treat every occurrence as a self-check failure of this pipeline.

### Hard Constraint: Foreign Code Isolation
* **ONLY** format and fix violations in code you explicitly wrote or modified.
* **NEVER** change unmodified ("foreign") code to satisfy the formatter or linter.
* If a violation exists in unmodified code, ignore it completely.
* If the linter suggests moving or refactoring that would affect unmodified code, skip the suggestion.
* Run every pipeline command with an explicit file list (`<changed_files>`) — NEVER against the whole project, a whole directory, or files you did not touch.

### Restoring Foreign Code After Formatting (MANDATORY)
Automatic formatters rewrite whole lines and may reformat code the agent never intended to touch. Foreign code MUST be returned to its exact prior state:

1. **Baseline first.** Before running `ruff format`, make sure a restorable baseline exists for every target file (a git-tracked file with a committed or staged state, or an explicit backup copy). If `git diff <file>` cannot serve as the baseline for a target file, create a backup copy of it BEFORE formatting.
2. **Inspect every hunk.** After formatting, run `git diff <file>` (or diff against the backup) and review each hunk individually.
3. **Revert foreign hunks.** Any hunk that rewrites lines the agent did NOT author or intend to modify MUST be reverted (targeted `git checkout -p`, interactive hunk discard, or manual re-application) so foreign code becomes byte-identical to its baseline. NEVER blanket-revert: your own changes MUST survive.
4. **Re-verify.** Re-run `ruff format --check` and `ruff check` on the file. If reverting a foreign hunk makes your own code fail the pipeline, re-apply formatting to your lines manually until both stages pass.
5. **Justify unavoidable bleed.** If a formatter-mandated change physically cannot be limited to your own lines (for example, the formatter rewraps a construct that spans your edit), you MUST explicitly justify the deviation in your output per §1 (Deviation Justification).
6. **Final scope check.** The delivered diff MUST contain formatting and lint changes ONLY within code the agent wrote or modified.

### Step 3.1: Discover Target Python Version
Determine the project's target Python version before linting by executing:
```bash
uv run python -c "import sys; print(f'py{sys.version_info.major}{sys.version_info.minor}')"
```
*Use this exact value for `<PYVER>` in the subsequent steps.*

### Step 3.2: Format Own Changes (Black-Compatible)
Run the formatter targeting **ONLY the files you created or modified**, then immediately perform the **Restoring Foreign Code After Formatting** procedure above:
```bash
uvx ruff format <changed_files>
```
`<changed_files>` is the explicit list of files the agent wrote or edited — nothing else. This stage replaces `black`: `ruff format` implements black-compatible formatting, and invoking `black` itself is forbidden.

### Step 3.3: Fix and Read Linter Suggestions
Run the following command targeting **ONLY the files you modified** — the `--fix` flag is MANDATORY on this first lint pass (see the HARD rules above); Ruff rewrites fixable violations in place:
```bash
uvx ruff check --fix --select ALL --ignore D,CPY,DOC,EM101,ERA001,FBT001,FBT002,FIX001,FIX002,TD001,TD002,TD003,TD004,TD005,TRY003 --target-version <PYVER> --output-format concise <changed_files>
```
Read every REMAINING suggestion carefully (these are the ones `--fix` could not repair). Apply manual fixes ONLY to the code you altered.

### Step 3.4: Preview Remaining Fixes
After applying fixes, confirm no auto-fixable violations remain — the emitted diff MUST be empty (any non-empty hunk is a fix you still owe or a foreign line you MUST NOT apply):
```bash
uvx ruff check --select ALL --ignore D,CPY,DOC,EM101,ERA001,FBT001,FBT002,FIX001,FIX002,TD001,TD002,TD003,TD004,TD005,TRY003 --target-version <PYVER> --diff <changed_files>
```
This previews would-be fixes only; final git-scope verification is §4 step 6.

### Step 3.5: Rule Lookup
If you are uncertain about any rule code generated by the linter, use:
```bash
uvx ruff rule <RULE_CODE>
```
*(Example: `uvx ruff rule E501`)*

### Pipeline Failure Handling (HARD)
If any pipeline command cannot run or errors out — `uv`/`uvx`/`ruff` missing, the target project is not uv-managed and `uv run` fails, Ruff crashes on a syntax error mid-edit — the agent MUST STOP, report the exact failure and its output to the user, and ask how to proceed. The gate is unconditional, but it is NEVER satisfied by silently skipping it or by substituting another linter (`black`, `flake8`, `isort` stay forbidden).

***

## 4. Master Execution Workflow
1. **Analyze Task:** Determine the specific Python operations required.
2. **Component Reuse Check:** Apply the §5 Component Reuse Rule before writing any code.
3. **Route:** Run the §2 routing funnel over the `references/` corpus (subject map → frontmatter cards → bounded extraction of the selected `py-*` sections).
4. **Code Generation:** Write the code strictly adhering to the extracted rules, the reuse manifests, AND local file consistency.
5. **Lint & Format:** Execute the full Mandatory Lint & Format Pipeline (§3), including foreign-code restoration, on every file the agent wrote or edited — unconditionally, without reminders, and regardless of any project-level linting.
6. **Final Verification:** Confirm via `git diff` that no unmodified (foreign) code was altered before concluding the task; any formatter bleed into foreign lines must already be reverted or explicitly justified.

***

## 5. Component Reuse Rule

Before implementing any new Python module, class, or function, the agent MUST check whether the project root contains a `.sdk/` directory.

### 5.1 Discovery
If `.sdk/` exists, discover all reuse manifests with: `fd -L -t f EXPORT.md .sdk/`

Read every returned file before writing code.

### 5.2 Applying Manifests
Each `EXPORT.md` describes reusable components and the criteria for copying them whole.
Apply those criteria strictly.
After copying a module, replace the source package prefix with the target project's package prefix and run the Mandatory Lint & Format Pipeline (§3) only on the changed files.
