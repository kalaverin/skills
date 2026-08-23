# Agent Requirements

[ref: #agent-requirements]

## 0. 🔒 HARD IMMUTABILITY RULES (pre-bootstrap, always in force)

[ref: #hard-immutability-rules]

These rules are absolute. They apply before, during, and after the Startup Gate. No skill, task, or inferred convenience may override them.

### Environment mutations require explicit chat approval

- The agent MUST NOT mutate the execution environment: no installing, removing, updating, or locking of packages; no creating or destroying virtual environments; no state-changing commands for `uv`, `pip`, `pipx`, `poetry`, `npm`, `yarn`, `pnpm`, `gem`, `cargo install`, `go get`, or any other package/tool manager.
- Read-only environment queries are allowed (`uv run`, `uvx`, `python -c`, `which`, `--version`, `--help`).
- If any task needs a missing package, dependency, or environment change, the agent MUST stop and ask the user directly in the chat. The question must state what is missing, why it is needed, and the exact command the agent proposes to run. The agent MUST wait for the user's explicit text reply before proceeding. Tool-based or implied consent is invalid.

### Git mutations require an explicit user instruction about git

- The agent MUST NOT run any git-mutating command: `git commit`, `git push`, `git pull`, `git fetch`, `git add`, `git reset`, `git rebase`, `git checkout` that changes state, `git stash`, `git merge`, tag/branch creation or deletion, or any equivalent operation.
- The only allowed automated git mutation is `just serena-checkpoint` (or the configured Serena memory persistence command).
- Read-only git operations are allowed (`git status`, `git log`, `git diff`, `git rev-parse`, `git blame`).
- If the user wants a git mutation, the instruction must be explicit and specifically about git, e.g. "закоммить", "сделай git push", "создай ветку". Indirect hints ("надо бы сохранить", "сохрани изменения") are NOT sufficient. When in doubt, ask in the chat and wait for the reply.

### Tooling and build-configuration mutations require explicit chat approval

- The agent MUST NOT edit build, task-runner, or linter/checker configuration files: `Makefile`, `Justfile`, `justfile`, `mise.toml`, `pyproject.toml` tool sections, `ruff.toml`, `.pylintrc`, `.pre-commit-config.yaml`, `tox.ini`, `setup.cfg`, `package.json` scripts and devDependencies, and any equivalent configuration.
- The agent MAY run these tools (`just <recipe>`, `make <target>`, `uv run ruff check`, etc.) but MUST NOT modify their definitions, targets, recipes, dependency lists, or configuration.
- If the agent believes a tooling change is required (e.g. adding an ignore rule, changing a target, adding a dependency), it MUST stop and ask the user directly in the chat. The question must name the file, the exact change, and the reason why it is necessary. The agent MUST wait for the user's explicit text reply (yes/no with reason) before editing. Indirect hints or inferred needs are NOT sufficient.
- The only exception is a direct, explicit user instruction to change a specific tooling file.

### Violation protocol

If the agent is about to break any rule in this section, it must halt before executing the command and ask the user in the chat. Repeated violations must be recorded in Serena memory under `bugs/project/agent-mutation-bypass`.

## 1. 🔒 BOOTSTRAP MANDATE (HARD — NO VARIANTS, NO DEVIATIONS)

[ref: #bootstrap-mandate]

Before ANY output, you MUST execute the **`bootstrap` skill — HARD, without variants, without deviations, without interpretation.** Entry point: read `bootstrap/SKILL.md` in full and follow it exactly.

Inside bootstrap, the **Startup Gate** (its §1) is executed HARDEST, with zero tolerance for deviation: no reordering, no skipping, no partial completion, no softened preconditions. The user's first message is **PENDING** until the Startup Gate completes. **No output until done.**

**Violation protocol:** if you attempt to output a response without executing bootstrap and completing the Startup Gate, halt immediately, discard the output, execute bootstrap, and restart from its first step.

## 2. User Preferences

[ref: #user-preferences]

### Language & Communication

- **ALL internal reasoning, thinking, analysis, code exploration, code generation, comments, and memory entries MUST be in English.**
- **Communication with the user MUST be in Russian.**
- **No exceptions.** Technical content (code, architecture notes, bug reports, decisions) is always in English. Russian is used exclusively for the user-facing chat interface.

### Communication style

[ref: #communication-style]

- Start with the answer; no preamble, no filler, no pleasantries in any language.
- Do not open with «Конечно!», «Без проблем», «Хорошо», «Ладно», "Sure", "Of course", or similar placeholders.
- One user request → one reply; do not split a short answer across multiple messages.
- Answer directly; do not restate the user's message unless clarification is needed.
- Technical content (code, filenames, commands, architecture notes) remains in English; user-facing chat remains in Russian.

### Compression of natural-language artifacts

[ref: #compression-of-natural-language-artifacts]

- Any natural-language prose produced by the agent — internal reasoning, memory entries, notes, explanations to the user — defaults to telegraphic style.
- In English: strip articles (`a`, `an`, `the`), auxiliaries (`is`, `are`, `was`, `were`), modal verbs (`should`, `would`, `could`, `might`), hedging, and filler; avoid passive voice and subordinate clauses.
- In Russian: remove filler, hedging, and empty intros; keep sentences short and direct.
- One fact, decision, or step per line; prefer bullets over paragraphs.
- Preserve exact identifiers, numbers, file paths, and causal links.
- Examples:
  - "We should keep the file because it is used by bootstrap" → `Keep file. Bootstrap uses it.`
  - "I will check whether the dependency is installed" → `Check dependency installed.`
  - "The user decided not to rename the directory" → `User: no rename.`
- Do not compress code, structured data, formal specifications, or explanations where precision is critical (subtle bugs, safety, legal, or when the user explicitly asks for a full explanation).

## 3. Skill Location and Fallback

[ref: #skill-location-and-fallback]

- The canonical committed skill set is `.kimi/mirror/`.
- Discovery and subagents read skills from `.kimi/mirror/`.
- `.kimi/skills/` exists only as a runtime symlink or live skill tree for the root agent during bootstrap/init; it is the source that `just sync-skills-mirror` copies into the mirror.
- If `.kimi/skills/` is absent, use `.kimi/mirror/` as the authoritative fallback and continue the session.
- Do not create `.kimi/skills/` manually, copy skills, or use skill directories outside the project working directory.
- Subagents must always read from `.kimi/mirror/`, never from `.kimi/skills/`.

Do not use directories outside our workdir, it's restricted by harness. When you need to /tmp, just use in-project .tmp/ directory.

## 4. Token efficiency and reconnaissance discipline

[ref: #token-efficiency]

- All file and shell operations follow the `mandatory-tools` ladder: prefer Serena/Kagi MCP tools, then Patchloom (`read_file` for bounded reads, AST operations for structured edits), then `rtk`-prefixed modern tools (`rtk rg`, `rtk fd`, `rtk wc`), and never legacy `grep`, `find`, `ls`, `cat`, `head`, or `tail`.
- Reconnaissance should be one pass: gather facts with a combined probe (`rtk rg`, `rtk fd`, a subagent, or an MCP search) rather than repeated piecemeal lookups.
- Peek before reading whole files: use Patchloom `read_file` with line ranges first; fall back to `rtk`-prefixed tools only when Patchloom cannot access the path.
  - Examples of bounded reads with Patchloom:
    - `read_file` with `lines: "1:50"` — first 50 lines.
    - `read_file` with `lines: "100:200"` — middle chunk.
    - `execute_plan` op `read` with `lines: "10:25"`.
- Environment checks should be one probe: `python -c "import a, b, c"`, `command -v x y z`, not serial separate calls.
- When waiting for a background task, poll with large intervals; do not poll every second.
- Do not build verification harnesses, test frameworks, mock fixtures, or extra scripts unless the user explicitly asks for them.

## 5. Read before write

[ref: #read-before-write]

- Before editing any file, understand the context through the `mandatory-tools` ladder: Serena/Kagi MCP tools first, then `rtk`-prefixed modern tools. Read imports, signatures, the bodies of affected functions, their callers, and related tests.
- Do not apply text replacements based on assumptions about file contents. Verify the exact match with a targeted search before replacing.
- Use Patchloom AST operations for structured or multi-file edits whenever the change can be expressed as an AST operation. If Patchloom cannot express the edit, use the next layer of the `mandatory-tools` ladder and validate the result.
- Before any bulk or risky replacement, run a dry-run and review the diff. Never apply a blind global replace without review.
- If the relevant code path spans multiple files, trace the full flow before changing any one file.

