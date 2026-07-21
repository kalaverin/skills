---
name: bootstrap
description: >
  Canonical skill discovery and auto-loading protocol. Always active. Governs how
  the agent discovers skill directories, parses SKILL.md frontmatter, evaluates
  triggers, resolves transitive dependencies via `requires:`, and lazily loads
  reference sections. This skill is the loader for all other skills.
triggers:
  always: true
  reason: "Every session must discover and load the correct skill set before executing any task."
---

# SKILL: Skill Auto-Loading Protocol (Bootstrap)

This skill is the canonical loader. It is **always active** and **requires no other skills**.

Before executing any task, you MUST identify and load all relevant skills. Treat skill loading as a mandatory startup step, not an optional optimization.

## 1. Mandatory Skills (Always Loaded)

The following skills MUST be considered active for every task:

- **`shell-protocol`** — ALWAYS active, because every file/code operation uses CLI tools.
- **`bootstrap`** — ALWAYS active, because every session must run skill discovery and loading.

The following skill is loaded automatically when its runtime prerequisite is satisfied:

- **`serena-protocol`** — loaded when the `serena` CLI binary is available in `PATH`, because the session then uses memory and/or codebase exploration tools.

## 2. Skill Discovery

Do NOT rely on a hardcoded skill registry or hardcoded skill directories in this prompt. Discover the skill directories made available to you by the execution harness / environment.

A skill directory is any directory that contains a `SKILL.md` entry point.

### Search order

Search for skill directories in this priority order:

1. `.kimi/skills/` in the project root.
2. `.agents/skills/` in the project root.
3. Any other directories shown in the current environment or context (e.g., `~/.config/kimi/skills`, execution-harness built-in skills).

To discover candidate directories, use a shell command such as:

```bash
fd -t f SKILL.md .kimi/skills .agents/skills <other-dir-1> <other-dir-2> ... 2>/dev/null \
  | xargs -n1 dirname \
  | sort -u
```

### Reading SKILL.md files

**MUST read skills via shell calls, not `ReadFile`.** `ReadFile` is forbidden for skill discovery and batch frontmatter extraction.

Extract the YAML frontmatter from **every** discovered `SKILL.md` in a **single batch shell command**. Do NOT list skill directories separately.

Use a one-liner such as:

```bash
fd -t f SKILL.md .kimi/skills .agents/skills <other-dir-1> <other-dir-2> ... 2>/dev/null \
  | sort -u \
  | xargs -I{} sh -c 'printf "\n### {}\n"; awk "/^---$/{c++; if(c==2) exit; next} c==1{print}" "{}"'
```

The output prints each file path followed by its YAML frontmatter (the block between the first `---` and the second `---`). From this batch output, extract for each skill:
- `name` — the skill identifier.
- `description` — what the skill governs.
- `triggers` — the activation rules.
- `requires` — optional list of skill names that must also be loaded when this skill is loaded.
- `runtime` — optional boolean. If `true`, the skill's triggers must be re-evaluated after every new user message (see Section 2.5).

Then evaluate the triggers against the user's request and project context using these semantics:
   - `always: true` — load the skill for every task.
   - A single condition (e.g., `files: ...` or `request: ...`) — load if that condition matches.
   - A flat map of multiple conditions (e.g., `files: ...` + `request: ...`) — conditions are **OR**ed: load if **any** matches.
   - `any:` followed by a map of conditions — same as a flat map: load if **any** matches.
   - `all:` followed by a map of conditions — conditions are **AND**ed: load only if **every** condition matches.

Example — OR (flat map / `any:`):

```yaml
triggers:
  files: "fd -e py -e pyi"
  request: "python, .py, .pyi, ruff, uv"
```

Example — AND (`all:`):

```yaml
triggers:
  all:
    files: "fd -e py -e pyi"
    request: "refactor, lint, python style"
```

2. If the trigger matches, mark the skill for full loading.
3. For every marked skill, read its `requires` list. Mark every listed skill for full loading as well. Repeat transitively until no new skills are added.

## 2.5 Runtime Trigger Re-Evaluation (Opt-in)

By default, triggers are evaluated once at the start of a task. A skill MAY opt
into runtime re-evaluation by adding `runtime: true` to its frontmatter.

```yaml
---
name: subagents-protocol
runtime: true
triggers:
  request: "subagent, delegate, субагент, делегируй"
---
```

When `runtime: true` is set:

1. After every new user message, re-evaluate the skill's triggers against the latest message and the current project context.
2. If the trigger matches and the skill is not yet loaded, load the skill's
   `SKILL.md` in full, including its `requires:` dependencies transitively.
3. Apply the newly loaded skill's rules to all subsequent actions in the
   session.
4. Do NOT re-evaluate skills that omit `runtime:` or set `runtime: false`;
   their triggers are evaluated only at startup.

This keeps startup behavior stable while allowing meta/orchestration skills
(such as `subagents-protocol`) to activate mid-session.

## 3. Trigger Override Protocol

Triggers override your internal assumptions. If a skill's trigger matches, you MUST load that skill even if you believe the topic is already familiar.

1. Load every triggered skill's `SKILL.md` in full.
2. Follow the skill's internal lazy-load protocol (Routing Index / Trigger Table) to pull only the reference sections needed for the current sub-task.
3. If the task spans multiple domains, load ALL matching skills.

## 4. Common Triggered Skills

The project context commonly triggers skills such as:

- **`python-lang`** — triggered when the workspace contains `.py` or `.pyi` files, or the request involves Python, Ruff, or `uv`.
- **`code-review`** — triggered when the user asks for a code review, diff review, feature review, full-project review, PR review, or equivalents in Russian (`код-ревью`, `ревью`, `проверь код`, `проверь diff`, `проверь изменения`, `проверь проект`).

These examples are representative, not exhaustive. The authoritative source of triggers is the YAML frontmatter of each discovered `SKILL.md`. If a discovered skill's trigger matches, you MUST load it even if it is not listed here.

## 5. Skill Loading Verification

Before proceeding with the user's request, confirm:

1. You have read the `SKILL.md` of every triggered skill.
2. You know which skill takes precedence when rules conflict.
3. You will not use training data or general heuristics in place of the loaded skill rules.

## 6. Reference File & Frontmatter Standard

Every skill whose `references/**/*.md` files use `[ref: #<anchor>]` lazy-load routing MUST conform to the normative standard at `references/REFERENCE_STANDARD.md` (relative to this skill's directory). It governs the frontmatter card schema (`subject` + `index` decision cards), anchor mechanics, body skeleton, the two-command loading funnel, and the conformance checklist. The reference implementation of the §9 checklist lives at `scripts/validate_reference_frontmatter.py` (same directory scheme; run with `uv run --no-project --with pyyaml python`, supports `--allow-extra KEY` for skill-declared extras). Load the standard when:

- authoring or editing any reference file or its frontmatter;
- migrating a skill's references to anchor-based lazy loading;
- reviewing or validating a reference corpus for conformance.

Skill-specific presentation details (section terminators, code-example style, taxonomy tiers) belong to the owning skill's addendum, which MUST defer to that standard.

**Violation protocol:** If you produce output without discovering all skill directories, batch-extracting the frontmatter of every discovered `SKILL.md` with a single shell one-liner, loading every triggered skill, and documenting the loaded skills in the `think` block, halt immediately, discard the output, and restart the Startup Gate from skill discovery.
