# Agent Requirements

## 1. 🔒 BOOTSTRAP MANDATE (HARD — NO VARIANTS, NO DEVIATIONS)

Before ANY output, you MUST execute the **`bootstrap` skill — HARD, without variants, without deviations, without interpretation.** Entry point: read `bootstrap/SKILL.md` in full and follow it exactly.

Inside bootstrap, the **Startup Gate** (its §1) is executed HARDEST, with zero tolerance for deviation: no reordering, no skipping, no partial completion, no softened preconditions. The user's first message is **PENDING** until the Startup Gate completes. **No output until done.**

**Violation protocol:** if you attempt to output a response without executing bootstrap and completing the Startup Gate, halt immediately, discard the output, execute bootstrap, and restart from its first step.

## 2. User Preferences

### Language & Communication

- **ALL internal reasoning, thinking, analysis, code exploration, code generation, comments, and memory entries MUST be in English.**
- **Communication with the user MUST be in Russian.**
- **No exceptions.** Technical content (code, architecture notes, bug reports, decisions) is always in English. Russian is used exclusively for the user-facing chat interface.
