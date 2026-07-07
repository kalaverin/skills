---
name: python-lang
description: >
  MANDATORY skill for Python code. Use when writing, editing, refactoring, or
  reviewing Python files, modules, packages, classes, functions, type
  annotations, imports, exceptions, comprehensions, decorators, or docstrings.
  Enforces Google Python Style Guide and a strict Ruff self-linting protocol.
triggers:
  files: "fd -e py -e pyi"
requires:
  - read-for-comments
---

# SKILL: Strict Python Engineering & Compliance

You are an expert Python Engineer and a strict Code Reviewer. **This document is a binding rule set, not a recommendation.**"
"
Every directive in this guide MUST be followed unless it explicitly uses **SHOULD** or **MAY**. The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [RFC2119] [RFC8174] when they appear in all capitals or in bold markup.

## 1. Compliance and Local Style

* **Default Rule:** Unless a section, paragraph, or sentence explicitly uses **SHOULD** or **MAY**, every statement is to be treated as **MUST**. If a coding situation is covered by this guide, you MUST follow the guide. You MUST NOT apply external style preferences or general Python heuristics in place of the rules documented here.
* **Consistency:** BE CONSISTENT. If you are editing code, ALWAYS look at the code around you and you MUST match its style. Local style is VERY IMPORTANT. If code you add looks drastically different from the existing code, it throws readers out of their rhythm. Consistency applies more heavily locally and on choices unspecified by the global style.
* **Deviation Justification:** If you deviate from any MUST directive, you MUST explicitly justify the deviation in your output.
* **Skill Boundary:** This skill covers Python language and style rules. For API resource design, HTTP/gRPC routes, and proto structure, consult the `api-design` skill.
* **RFC Verbs:** For precise semantics of requirement-level verbs, consult the `read-for-comments` skill.

---

## 2. Mandatory Lookups (Lazy-Load Protocol)

**This index is mandatory.** When the trigger in the left column matches your current task, you MUST extract and read the referenced section in full before proceeding. Do not guess, do not rely on training data, and do not skip the section because the topic seems familiar. All triggers carry the weight of MUST unless the target section itself contains a SHOULD or MAY.

### ⚠️ STRICT READING CONSTRAINT (PARTIAL EXTRACTION)
You MUST NOT read the files `references/01_language_rules.md` or `references/02_style_rules.md` in their entirety. You MUST use partial extraction to preserve context memory.

**Extraction Execution:**
1. Match your task to a "Trigger / Situation" in the tables below.
2. Copy the corresponding `[ref: ...]` tag.
3. Use `rg` to extract ONLY the relevant section.
   *Example CLI command:* `rg -A 50 "\\[ref: #s1.12-default-argument-values\\]" references/01_language_rules.md`

### Table A: Python Language Rules (`references/01_language_rules.md`)

| Trigger / Situation | Section | Anchor Tag for Search |
|:---|:---|:---|
| Running/configuring linting; suppressing warnings (`pylint: disable`). | 1.1 Lint | `[ref: #s1.1-lint]` |
| Adding/reorganizing imports; absolute vs relative; import order. | 1.2 Imports | `[ref: #s1.2-imports]` |
| Creating a new package/module; `__init__.py` usage. | 1.3 Packages | `[ref: #s1.3-packages]` |
| Raising/catching exceptions; `except Exception:`; preserving tracebacks. | 1.4 Exceptions | `[ref: #s1.4-exceptions]` |
| Declaring/using global variables; mutable vs immutable state. | 1.5 Mutable Global State | `[ref: #s1.5-global-variables]` |
| Defining nested functions/classes; closures; local classes. | 1.6 Nested/Local Classes | `[ref: #s1.6-nested]` |
| Writing comprehensions (list/dict/set) or generator expressions. | 1.7 Comprehensions | `[ref: #s1.7-comprehensions]` |
| Iterating over collections; using `in` for membership testing. | 1.8 Default Iterators | `[ref: #s1.8-default-iterators-and-operators]` |
| Writing generator functions; `yield` and `yield from`. | 1.9 Generators | `[ref: #s1.9-generators]` |
| Writing one-off functions; deciding on `lambda`. | 1.10 Lambda Functions | `[ref: #s1.10-lambda-functions]` |
| Writing inline conditionals (ternary expressions). | 1.11 Conditional Expressions | `[ref: #s1.11-conditional-expressions]` |
| Defining default arguments; handling mutable defaults. | 1.12 Default Arguments | `[ref: #s1.12-default-argument-values]` |
| Implementing getters/setters; using `@property`. | 1.13 Properties | `[ref: #s1.13-properties]` |
| Empty collection checks; `None`, zero, or boolean evaluations. | 1.14 True/False Evaluations | `[ref: #s1.14-truefalse-evaluations]` |
| Referencing variables from an enclosing scope (closures). | 1.16 Lexical Scoping | `[ref: #s1.16-lexical-scoping]` |
| Applying/writing decorators; `@classmethod`, `@staticmethod`. | 1.17 Decorators | `[ref: #s1.17-function-and-method-decorators]` |
| Multi-threading; `threading`, `multiprocessing`, `concurrent.futures`. | 1.18 Threading | `[ref: #s1.18-threading]` |
| Metaclasses, reflection, or dynamic attribute access. | 1.19 Power Features | `[ref: #s1.19-power-features]` |
| Using `from __future__ import annotations` or modern idioms. | 1.20 Modern Python | `[ref: #s1.20-modern-python]` |
| Adding/evaluating type annotations (`typing`). | 1.21 Type Annotated Code | `[ref: #s1.21-type-annotated-code]` |

### Table B: Python Style Rules (`references/02_style_rules.md`)

| Trigger / Situation | Section | Anchor Tag for Search |
|:---|:---|:---|
| Multiple statements per line; semicolon usage. | 2.1 Semicolons | `[ref: #s2.1-semicolons]` |
| Breaking long lines (> 80 chars); explicit backslash vs parens. | 2.2 Line Length | `[ref: #s2.2-line-length]` |
| Parentheses for grouping, tuples, or line continuation. | 2.3 Parentheses | `[ref: #s2.3-parentheses]` |
| Indentation rules; hanging indents; trailing commas. | 2.4 Indentation | `[ref: #s2.4-indentation]` |
| Blank lines between top-level definitions or logical sections. | 2.5 Blank Lines | `[ref: #s2.5-blank-lines]` |
| Whitespace around operators, commas, colons; spacing in types. | 2.6 Whitespace | `[ref: #s2.6-whitespace]` |
| Adding/editing shebangs (`#!/usr/bin/env python3`). | 2.7 Shebang Line | `[ref: #s2.7-shebang-line]` |
| Writing docstrings (Args/Returns/Raises) and inline comments. | 2.8 Comments & Docstrings | `[ref: #s2.8-comments-and-docstrings]` |
| String formatting (f-string, `%`, `.format()`); log messages. | 2.10 Strings | `[ref: #s2.10-strings]` |
| Managing resources (files, sockets); using `with`. | 2.11 Files/Sockets | `[ref: #s2.11-files-sockets-closeables]` |
| Writing TODO comments; correct format and issue linking. | 2.12 TODO Comments | `[ref: #s2.12-todo-comments]` |
| Formatting and grouping import blocks. | 2.13 Imports Formatting | `[ref: #s2.13-imports-formatting]` |
| Combining small statements on a single line. | 2.14 Statements | `[ref: #s2.14-statements]` |
| Choosing between public attributes and accessor methods. | 2.15 Accessors | `[ref: #s2.15-accessors]` |
| Naming conventions (modules, classes, vars); PEP 8 constraints. | 2.16 Naming | `[ref: #s2.16-naming]` |
| Script entry points; `if __name__ == '__main__':`. | 2.17 Main | `[ref: #s2.17-main]` |
| Evaluating function length; extracting smaller functions. | 2.18 Function Length | `[ref: #s2.18-function-length]` |
| Type annotation style; line breaks; generics; conditional imports. | 2.19 Type Annotations | `[ref: #s2.19-type-annotations]` |

---

## 3. Agent Self-Linting Protocol

**MANDATORY:** Before declaring any Python editing task complete, the agent MUST run `ruff check` on all files it modified.

### Hard Constraint: No Unmodified Code Changes
* **ONLY** fix violations in code you explicitly wrote or modified.
* **NEVER** change unmodified code to satisfy the linter.
* If a violation exists in unmodified code, ignore it completely.
* If the linter suggests moving or refactoring that would affect unmodified code, skip the suggestion.

### Step 3.1: Discover Target Python Version
Determine the project's target Python version before linting by executing:
```bash
uv run python -c "import sys; print(f'py{sys.version_info.major}{sys.version_info.minor}')"
```
*Use this exact value for `<PYVER>` in the subsequent steps.*

### Step 3.2: Read Linter Suggestions
Run the following command targeting **ONLY the files you modified**:
```bash
uvx ruff check --select ALL --ignore D,CPY,DOC,EM101,ERA001,FBT001,FBT002,FIX001,FIX002,TD001,TD002,TD003,TD004,TD005,TRY003 --target-version <PYVER> --output-format concise <changed_files>
```
Read every suggestion carefully. Apply fixes ONLY to the code you altered.

### Step 3.3: Verify Diff Scope
After applying fixes, verify the diff touches **ONLY changed code**:
```bash
uvx ruff check --select ALL --ignore D,CPY,DOC,EM101,ERA001,FBT001,FBT002,FIX001,FIX002,TD001,TD002,TD003,TD004,TD005,TRY003 --target-version <PYVER> --diff <changed_files>
```

### Step 3.4: Rule Lookup
If you are uncertain about any rule code generated by the linter, use:
```bash
uvx ruff rule <RULE_CODE>
```
*(Example: `uvx ruff rule E501`)*

---

## 4. Master Execution Workflow
1. **Analyze Task:** Determine the specific Python operations required.
2. **Trigger Match:** Locate the relevant rows in Table A and Table B.
3. **Partial Read:** Run `rg` on the specific `[ref: ...]` tags in `references/01_language_rules.md` and `references/02_style_rules.md`.
4. **Code Generation:** Write the code strictly adhering to the extracted rules AND local file consistency.
5. **Self-Linting:** Execute the 4-step Agent Self-Linting Protocol.
6. **Final Verification:** Confirm no unmodified code was altered before concluding the task.
