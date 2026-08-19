# Agent Requirements

[ref: #agent-requirements]

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

## 3. Skill Location and Fallback

[ref: #skill-location-and-fallback]

- The canonical committed skill set is `.kimi/mirror/`.
- Discovery and subagents read skills from `.kimi/mirror/`.
- `.kimi/skills/` exists only as a runtime symlink or live skill tree for the root agent during bootstrap/init; it is the source that `just sync-skills-mirror` copies into the mirror.
- If `.kimi/skills/` is absent, use `.kimi/mirror/` as the authoritative fallback and continue the session.
- Do not create `.kimi/skills/` manually, copy skills, or use skill directories outside the project working directory.
- Subagents must always read from `.kimi/mirror/`, never from `.kimi/skills/`.

Do not use directories outside our workdir, it's restricted by harness. When you need to /tmp, just use in-project .tmp/ directory.
