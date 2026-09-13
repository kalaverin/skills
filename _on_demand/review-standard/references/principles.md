---
subject: "Core standard of code review per Google eng-practices; code health senior principle, reviewer ownership, trade-offs progress versus quality, no perfect code only better code, `Nit:` prefix convention, mentoring function, technical facts over opinions, style guide authority, design judgment, consistency fallback, consensus then face-to-face then escalation."
index:
  - anchor: principles-core-standard
    what: "The senior principle of the whole standard: reviewers favor approving a CL once it definitely improves overall code health, even if imperfect."
    problem: "Agent judges whether reviewer was right to approve or block change; without core rule every verdict drifts into taste; approval correctness, blocking legitimacy, perfectionism dispute, improvement criterion, progress trade-off, review standard anchor."
    use_when: "Evaluating any approve/refuse decision; assessing reviewer strictness complaints; checking whether polish demands delayed an improving change."
    avoid_when: "Assessing comment wording or tone (comments.md); assessing response latency (process.md)."
    expected: "Verdict on the approve/block decision cites the code-health rule verbatim."
  - anchor: principles-mentoring
    what: "The mentoring clause: educational comments are welcome but non-critical teaching remarks must be marked `Nit:` or otherwise non-mandatory."
    problem: "Agent assesses whether reviewer mixed teaching with requirements; unlabeled educational remarks read as blockers and stall authors indefinitely; guidance, knowledge sharing, learning function, mandatory versus optional, label prefix, tone marker, extra polish."
    use_when: "Reviewer left educational comments; author complains about mandatory-sounding teaching; assessing knowledge-sharing behavior."
    avoid_when: "Comment courtesy assessment (comments.md); design-principle disputes (principles-technical-facts)."
    expected: "Teaching comments are classified mandatory-or-`Nit:` exactly as the clause requires."
  - anchor: principles-technical-facts
    what: "The four principles: technical facts overrule opinions; style guide is absolute on style; design is weighed on engineering principles; consistency with the codebase is the fallback."
    problem: "Agent must decide who is right in reviewer-author disagreement; without hierarchy of evidence verdict becomes agent opinion; style dispute, design judgment, preference clash, consistency argument, facts over taste, authority order, opinion versus data."
    use_when: "Any who-is-right dispute; style-guide versus local-consistency tension; design disagreements with multiple valid options."
    avoid_when: "Evaluating review speed (process.md); emergency classification (conflicts.md)."
    expected: "Dispute verdict follows the facts-then-style-guide-then-principles-then-consistency order."
  - anchor: principles-resolving-conflicts
    what: "The escalation ladder: consensus from the documents first, then face-to-face with results recorded on the CL, then escalation to team, TL, maintainer, or manager — never let a CL sit."
    problem: "Agent assesses stalled or heated review thread; unsure whether escalation step was proper, premature, or skipped entirely; unresolved conflict, consensus failure, ladder rung, meeting notes, blocked change, recorded discussion, team lead, video call."
    use_when: "Review thread shows unresolved disagreement; CL stalled over conflict; questioning whether escalation step was skipped."
    avoid_when: "Single-comment wording issues (comments.md); pushback about strictness (conflicts.md)."
    expected: "Verdict states which escalation step was reached and whether skipping one violated the standard."
---

# Code Review Principles (Google eng-practices)

The verbatim standard of `standard.html`, reorganized by clause. Every verdict about approve/block decisions and dispute resolution grounds here.

## The Core Standard

[ref: #principles-core-standard]

The primary purpose of code review is to make sure that the overall code health of the code base is improving over time. All of the tools and processes of code review are designed to this end. To accomplish this, a series of trade-offs has to be balanced:

- Developers must be able to _make progress_ on their tasks. If you never submit an improvement to the codebase, then the codebase never improves. Also, if a reviewer makes it very difficult for _any_ change to go in, developers are disincentivized to make improvements in the future.
- It is the duty of the reviewer to make sure that each CL is of such a quality that the overall code health of the codebase is not decreasing over time. Codebases often degrade through small decreases in code health, especially when a team is under time constraints and feels it has to take shortcuts.
- A reviewer has ownership and responsibility over the code they review: the codebase must stay consistent, maintainable, and meet everything in "What to look for in a code review" (`coverage.md`).

The rule that is the standard expected in code reviews:

**In general, reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health of the system being worked on, even if the CL isn't perfect.**

That is _the_ senior principle among all of the code review guidelines.

Limitations: if a CL adds a feature the reviewer doesn't want in the system, the reviewer can deny approval even if the code is well-designed.

There is no such thing as "perfect" code — there is only _better_ code. Reviewers should not require the author to polish every tiny piece before granting approval; the reviewer balances the need for forward progress against the importance of the suggested changes. Instead of perfection, seek _continuous improvement_. A CL that as a whole improves maintainability, readability, and understandability should not be delayed for days or weeks because it isn't "perfect."

Reviewers should _always_ feel free to leave comments that something could be better, but if it's not very important, prefix it with `Nit:` to let the author know it is a point of polish that can be ignored.

Nothing in this document justifies checking in CLs that definitely _worsen_ overall code health. The only time that happens is an emergency (see `conflicts.md`).

Sources: https://google.github.io/eng-practices/review/reviewer/standard.html

## Mentoring

[ref: #principles-mentoring]

Code review can teach developers something new about a language, a framework, or general software design principles. It is always fine to leave comments that help a developer learn; sharing knowledge is part of improving code health over time. Keep in mind: if a comment is purely educational but not critical to meeting the standard, prefix it with `Nit:` or otherwise indicate that resolving it is not mandatory in this CL.

Sources: https://google.github.io/eng-practices/review/reviewer/standard.html

## Principles

[ref: #principles-technical-facts]

- Technical facts and data overrule opinions and personal preferences.
- On matters of style, the style guide is the absolute authority. Any purely style point (whitespace, etc.) not in the style guide is personal preference. The style should be consistent with what is there; if there is no previous style, accept the author's.
- Aspects of software design are almost never a pure style issue or personal preference: they rest on underlying principles and are weighed on those principles, not opinion. Sometimes several options are valid; if the author can demonstrate (through data or solid engineering principles) that several approaches are equally valid, the reviewer accepts the author's preference. Otherwise the choice is dictated by standard principles of software design.
- If no other rule applies, the reviewer may ask the author to be consistent with the current codebase, as long as that doesn't worsen overall code health.

Sources: https://google.github.io/eng-practices/review/reviewer/standard.html

## Resolving Conflicts

[ref: #principles-resolving-conflicts]

In any conflict on a code review, the first step is always for developer and reviewer to try to come to consensus, based on this document and the other documents of the Author's Guide and the Reviewer Guide.

When consensus becomes especially difficult, a face-to-face meeting or video conference between reviewer and author helps, instead of resolving the conflict through review comments. (If you do this, record the results of the discussion as a comment on the CL, for future readers.)

If that doesn't resolve the situation, escalate: a broader team discussion, a Technical Lead weighing in, a decision from the code maintainer, or help from an Eng Manager. **Don't let a CL sit around because the author and the reviewer can't come to an agreement.**

Sources: https://google.github.io/eng-practices/review/reviewer/standard.html
