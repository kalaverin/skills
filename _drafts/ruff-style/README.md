# ruff-style
[ref: #rs-intro]

Ruff rule corpus and enforcement reference for Python code style.

## What it does
[ref: #rs-what]

This skill collects and explains the Ruff lint and format rules that `python-lang` enforces. It is a living reference for why each rule exists, when it applies, and how to fix violations.

**DRAFT:** this skill is currently marked `draft: true` in `SKILL.md`, so it is invisible to automatic skill discovery. It is read manually only while under construction.

## When it activates
[ref: #rs-when]

Activates when the agent needs detailed Ruff rule guidance beyond what `python-lang` provides, or when adding new Ruff rules to the project configuration.

Examples:

- "Why is Ruff rule E501 triggered here?"
- "Add Ruff rule selection for this project."
- "Explain the Ruff rules we enforce."

## How to run / use it
[ref: #rs-how]

Read the rule cards in `references/` for specific rules or categories.
Use it alongside `python-lang`, which owns the mandatory `ruff format` and `ruff check` pipeline.

## What it produces
[ref: #rs-produces]

- Clear explanations of Ruff rule categories and individual rules.
- Project-specific Ruff configuration guidance.

## Dependencies and why they matter
[ref: #rs-deps]

- `python-lang` — this skill is a supplement to `python-lang`'s Ruff mandate.

## Strengths and trade-offs
[ref: #rs-tradeoffs]

### Strong sides
[ref: #rs-strong]

- Centralizes Ruff rule knowledge.
- Helps diagnose non-obvious lint failures.
- Useful when onboarding a project to stricter Ruff settings.

### Weak sides / limits
[ref: #rs-weak]

- Draft status: coverage is incomplete, and the skill is invisible to automatic discovery.
- Not a replacement for running `ruff` or reading upstream docs.

### Common pitfalls / gotchas
[ref: #rs-pitfalls]

- This skill does not define the pipeline; `python-lang` does.
- Rule codes and behavior change with Ruff versions; pin the version in your project.

## Repository layout
[ref: #rs-layout]

```text
ruff-style/
├── references/           # 28 theme cards plus a security/ subfolder
│   ├── 01_async.md
│   ├── 02_classes.md
│   ├── 03_collections.md
│   ├── 04_common.md
│   ├── 05_comparisons.md
│   ├── 06_comprehensions.md
│   ├── 07_datetime.md
│   ├── 08_docstrings.md
│   ├── 09_exceptions.md
│   ├── 10_flow.md
│   ├── 11_functions.md
│   ├── 12_generics.md
│   ├── 13_hygiene.md
│   ├── 14_imports.md
│   ├── 15_iterators.md
│   ├── 16_lint-suppression.md
│   ├── 17_logging.md
│   ├── 18_mutable-defaults.md
│   ├── 19_naming.md
│   ├── 20_numbers.md
│   ├── 21_pathlib.md
│   ├── 22_pytest.md
│   ├── 23_resources.md
│   ├── 24_scope.md
│   ├── 25_simplification.md
│   ├── 26_string-formatting.md
│   ├── 27_strings.md
│   ├── 28_typing.md
│   └── security/         # Security-focused rule cards
├── scripts/
│   └── ruff_rules_dump.py
├── README.md                # Human overview (this file)
└── SKILL.md              # Agent entry point and rule index
```

## Reference overview
[ref: #rs-refs]

| File | Topic |
|------|-------|
| `references/01_async.md` | Async |
| `references/02_classes.md` | Classes |
| `references/03_collections.md` | Collections |
| `references/04_common.md` | Common |
| `references/05_comparisons.md` | Comparisons and truthiness |
| `references/06_comprehensions.md` | Comprehensions |
| `references/07_datetime.md` | Datetime |
| `references/08_docstrings.md` | Docstrings |
| `references/09_exceptions.md` | Exceptions |
| `references/10_flow.md` | Control flow |
| `references/11_functions.md` | Functions |
| `references/12_generics.md` | Generics and type variables |
| `references/13_hygiene.md` | Hygiene |
| `references/14_imports.md` | Imports |
| `references/15_iterators.md` | Iterators |
| `references/16_lint-suppression.md` | Lint suppression |
| `references/17_logging.md` | Logging |
| `references/18_mutable-defaults.md` | Mutable Defaults |
| `references/19_naming.md` | Naming |
| `references/20_numbers.md` | Numbers |
| `references/21_pathlib.md` | Pathlib |
| `references/22_pytest.md` | Pytest |
| `references/23_resources.md` | Resources and environment |
| `references/24_scope.md` | Scope |
| `references/25_simplification.md` | Simplification |
| `references/26_string-formatting.md` | String formatting |
| `references/27_strings.md` | Strings |
| `references/28_typing.md` | Typing |
| `references/security/01_content.md` | Security: Content |
| `references/security/02_crypto.md` | Security: Crypto |
| `references/security/03_injection.md` | Security: Injection |
| `references/security/04_network.md` | Security: Network |
| `references/security/05_runtime.md` | Security: Runtime |

## Important conventions / gotchas
[ref: #rs-conventions]

- Use as a supplement to `python-lang`.
- Pin the Ruff version in `pyproject.toml` or `requirements-dev.txt`.
- Refer to upstream Ruff docs for the latest rule behavior.
