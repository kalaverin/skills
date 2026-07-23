---
name: preflight-checklist
description: Mandatory pre-flight compliance check. Always loaded. Before executing any task, verify that the `shell-protocol` and `serena-protocol` skills have been discovered and loaded.
triggers:
  always: true
  reason: "Every session must confirm the two core mandatory skills are active."
requires:
  - bootstrap
---

# SKILL: Pre-flight Checklist

This skill is a short compliance gate. It does not replace the Startup Gate in
`AGENTS.md`; it augments it.

Before producing output for any user request, confirm:

- [ ] `shell-protocol` was discovered during Skill Discovery and its
  `SKILL.md` is loaded.
- [ ] `serena-protocol` was discovered during Skill Discovery and its
  `SKILL.md` is loaded.
- [ ] `read-for-comments` was discovered during Skill Discovery and its `SKILL.md` is loaded.

If either skill is missing from the loaded set, halt, load it, and restart the
Startup Gate from Section 1, step 5.
