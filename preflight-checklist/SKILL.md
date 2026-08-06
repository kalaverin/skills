---
name: preflight-checklist
description: "Mandatory session-initialization closer and Startup Gate audit. Always loaded. Runs EXACTLY ONCE at session start, after all skill loading completes: verifies Startup Gate completion with evidence (mirror sync, forced import, discovery, activation, memory priming, MCP declaration, think block), runs dynamic session checks derived from the active skill set (mode states, rtk version pin, delegation readiness), and reports a compact evidence-backed verdict table to the user before the first task output. Any FAIL is fixed before proceeding."
triggers:
  always: true
  reason: "Every session must close its initialization with an evidence-backed audit of the Startup Gate."
requires:
  - bootstrap
version: 0.1.0
---

# SKILL: Pre-flight Checklist (Session Initialization Closer)

This skill is the closing ceremony of session initialization and the evidence-based audit of the Startup Gate. It runs **exactly once per session**, immediately after the Startup Gate (bootstrap §1, steps 1–8) completes and before the first task output. It is NOT a per-action check: mid-session compliance is owned by the individual skills, never by re-running preflight.

## 1. Evidence Discipline (HARD)

[ref: #pfc-evidence]

- A checklist item passes ONLY on evidence: a command output, a tool result, or a file actually read in this session. "Checked mentally" is never evidence.
- The verdict is SHOWN to the user explicitly: compact and laconic, but shown — one line per item.
- Any FAIL: fix the cause, re-run the affected item, then proceed. The user's first request stays pending until the table is all-PASS.

## 2. The Checklist

[ref: #pfc-checklist]

**Part A — Startup Gate audit (static order, every session):**

1. **Mirror sync** — evidence: `just sync-skills-mirror` output (`SYNCED`/`CREATED`). If it printed `INSYNC` while uncommitted skill edits exist, apply the documented lag workaround (`notes/project/skills_mirror_uncommitted_lag`) and re-run.
2. **Forced import** — evidence: `frontmatter-protocol/SKILL.md` and `references/include.md` read in full this session.
3. **Discovery & evaluation** — evidence: the batch header extraction ran; the loaded skill set is named (always-skills `shell-protocol`, `serena-protocol`, `read-for-comments` present among them).
4. **Project activation** — evidence: `activate_project` result received.
5. **Memory priming** — evidence: `agent/rules` and `agent/allowed_violations` read.
6. **MCP groups declared** — evidence: the think block's `applied: mcp-…` line.
7. **Think block produced** — evidence: the gate's proof-of-work block with both `applied:` lines.

**Part B — dynamic session checks (derived from the active skill set; skip what is not active):**

8. **Mode states** — every `runtime: true` skill's state declared (e.g. `discuss-first: off`); no pending user question left unanswered.
9. **rtk pin** — only when `rtk-protocol` is active — evidence: `rtk --version` output matches the skill's version pin; on mismatch, flag the refresh.
10. **Delegation readiness** — evidence: the subagent model is chosen per `subagents-protocol` `[ref: #sp-model-selection]` (the single source of model names) and passed explicitly on launches; the mirror is fresh enough for subagents (they read skills ONLY from `.kimi/mirror/`).

## 3. Verdict Format

[ref: #pfc-verdict]

Print the table to the user, one line per item, before the first task output:

```text
PREFLIGHT <YYYY-MM-DDTHH:MM:SSZ>
A1 mirror sync ........... PASS (SYNCED/INSYNC/CREATED)
A2 forced import ......... PASS (core + include)
A3 discovery ............. PASS (N skills loaded)
A4 activation ............ PASS (<project>)
A5 memory priming ........ PASS (agent/rules, agent/allowed_violations)
A6 MCP declared .......... PASS (groups…)
A7 think block ........... PASS
B8 mode states ........... PASS (discuss-first: off)
B9 delegation readiness .. PASS (model explicit; mirror fresh)
```

One line per item, evidence in parentheses, nothing else. On any FAIL: state the cause in the same line, fix it, re-print the corrected line, then continue.

## 4. Timing and Non-Repetition

[ref: #pfc-timing]

- Runs ONCE, at session start, as the last initialization act. The first user message remains pending until the table prints all-PASS.
- NEVER re-runs mid-session: compliance after initialization (model parameters, mirror lag, mode gates, MCP routing) is enforced by the owning skills at the moment of action.
- If the session's loaded set changes materially (new skill family activated), the new skill's own rules govern — preflight is not re-opened.

**Violation protocol:** if you answer the user's first request without printing the evidence-backed preflight table, halt immediately, discard the output, run the checklist, print the verdict, and only then proceed.
