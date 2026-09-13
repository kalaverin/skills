---
subject: "Comment-writing rules per Google eng-practices; courtesy toward developer, comment on code never on person, explain reasoning behind remarks, balance explicit directions with pointing problems, developer owns fix, severity labels `Nit:` `Optional` `Consider` `FYI`, praise good work, unclear code rewritten instead of tool explanations."
index:
  - anchor: comments-summary
    what: "The page summary: be kind, explain your reasoning, balance explicit directions with pointing out problems, and encourage simplifying code over explaining complexity."
    problem: "Agent needs quick completeness check of comment-writing duties; four headline obligations get lost among detailed sections; kindness duty, reasoning duty, direction balance, simplify encouragement, headline list, opening inventory, remark quality, quick scan."
    use_when: "Opening assessment of comment quality; confirming which top-level duties exist before deep checks."
    avoid_when: "Deep assessment of one duty (that duty's own card); author-side comment handling (author_side.md)."
    expected: "All four headline duties are enumerated before zone-level assessment."
  - anchor: comments-courtesy
    what: "The courtesy rule: be courteous and respectful while clear and helpful; comment on the code, never on the developer — especially for anything potentially upsetting or contentious."
    problem: "Agent assesses tone of review remarks; person-addressed accusations poison discussion and trigger defensiveness instead of fixes; respectful phrasing, code not author, accusatory tone, upsetting wording, contentious remark, professional civility, respectful disagreement, mutual respect."
    use_when: "Review comments address the author personally; frustration visible in wording; complaint about reviewer rudeness."
    avoid_when: "Comment content correctness (principles.md); severity labeling (comments-severity)."
    expected: "Verdict judges wording against the code-not-developer pattern with examples."
  - anchor: comments-explain-why
    what: "The explain-why rule: comments help the developer understand why the remark is made — intent, the best practice being followed, or how the suggestion improves code health."
    problem: "Agent checks whether remarks carry reasoning; bare orders without rationale breed cargo-cult fixes and repeat errors; rationale inclusion, intent explanation, health improvement, repeating mistakes, teaching moment, context sharing, motive clarity."
    use_when: "Comments are bare imperatives; author repeatedly misunderstands reviewer intent; assessing educational value of remarks."
    avoid_when: "Obvious trivial fixes needing no rationale; tone assessment (comments-courtesy)."
    expected: "Verdict notes presence or absence of reasoning in non-trivial remarks."
  - anchor: comments-guidance
    what: "The guidance balance: fixing the CL is the developer's responsibility, not the reviewer's; balance pointing out problems (developer decides) against direct instructions, suggestions, or code — and praise what is done well."
    problem: "Agent weighs how much direction reviewer gave; over-prescribing steals learning, under-guiding leaves author stranded; fix ownership, learning versus prescribing, concrete patch, pointer balance, helplessness gap, micromanagement, exemplary praise, skill growth, autonomy respect."
    use_when: "Reviewer wrote full solutions or none; assessing whether guidance level fit the situation."
    avoid_when: "Approving-with-comments decisions (process.md); dispute resolution (principles.md)."
    expected: "Verdict classifies guidance as over-prescribed, balanced, or absent."
  - anchor: comments-severity
    what: "Severity labels: mark comment criticality — `Nit:` (minor, technically should), `Optional`/`Consider` (good idea, not required), `FYI` (future thought) — so authors prioritize and don't read every remark as mandatory."
    problem: "Agent inspects whether remark criticality was signaled; unlabeled optional notes read as blockers and stall merges over trivia; severity signaling, nit prefix, optional marker, fyi note, priority clarity, mandatory misreading, requirement illusion, labeling duty."
    use_when: "Review mixes blockers and trivia without labels; author treated optional note as requirement."
    avoid_when: "Reviewer used a different explicit label set consistently (note the divergence, still assess); comment tone assessment (comments-courtesy)."
    expected: "Verdict states whether severity labeling matched the standard's label set."
  - anchor: comments-accepting-explanations
    what: "The explanation rule: when a reviewer asks to explain unclear code, the right response is rewriting the code more clearly (occasionally a code comment) — explanations only in the review tool are lost to future readers."
    problem: "Agent evaluates how comprehension requests resolved; answers living only in discussion vanish for posterity; rewrite clarity, lost context, clarification handling, thread-only answer, reader persistence, simplification response, ephemeral reply, knowledge decay, documentation gap, permanent record."
    use_when: "Long explanations sit in review with code unchanged; assessing author response to clarity questions."
    avoid_when: "Genuinely unfamiliar reviewer territory where explanation suffices; comment tone (comments-courtesy)."
    expected: "Verdict states whether clarity was moved into code or left in the tool."
---

# Writing Review Comments

The verbatim standard of `comments.html`: how reviewer remarks must be written.

## Summary

[ref: #comments-summary]

- Be kind.
- Explain your reasoning.
- Balance giving explicit directions with just pointing out problems and letting the developer decide.
- Encourage developers to simplify code or add code comments instead of just explaining the complexity to you.

Sources: https://google.github.io/eng-practices/review/reviewer/comments.html

## Courtesy

[ref: #comments-courtesy]

In general, be courteous and respectful while also being very clear and helpful to the developer whose code you are reviewing. One way is to be sure you always make comments about the _code_ and never about the _developer_. You don't always have to follow this practice, but definitely use it when saying something that might otherwise be upsetting or contentious. For example:

Bad: "Why did **you** use threads here when there's obviously no benefit to be gained from concurrency?"

Good: "The concurrency model here is adding complexity to the system without any actual performance benefit that I can see. Because there's no performance benefit, it's best for this code to be single-threaded instead of using multiple threads."

Sources: https://google.github.io/eng-practices/review/reviewer/comments.html

## Explain Why

[ref: #comments-explain-why]

The "good" example above helps the developer understand _why_ you are making your comment. You don't always need this information in review comments, but sometimes it's appropriate to give a bit more explanation around your intent, the best practice you're following, or how your suggestion improves code health.

Sources: https://google.github.io/eng-practices/review/reviewer/comments.html

## Giving Guidance

[ref: #comments-guidance]

**In general it is the developer's responsibility to fix a CL, not the reviewer's.** You are not required to do detailed design of a solution or write code for the developer.

This doesn't mean the reviewer should be unhelpful. Strike an appropriate balance between pointing out problems and providing direct guidance. Pointing out problems and letting the developer decide often helps the developer learn and makes reviews easier. It can also result in a better solution, because the developer is closer to the code than the reviewer is.

However, sometimes direct instructions, suggestions, or even code are more helpful. The primary goal of code review is to get the best CL possible. A secondary goal is improving developers' skills so they require less and less review over time.

Remember that people learn from reinforcement of what they do well, not just what they could do better. If you see things you like in the CL, comment on those too! Examples: the developer cleaned up a messy algorithm, added exemplary test coverage, or you as the reviewer learned something from the CL. Just as with all comments, include why you liked something, further encouraging the developer to continue good practices.

Sources: https://google.github.io/eng-practices/review/reviewer/comments.html

## Label Comment Severity

[ref: #comments-severity]

Consider labeling the severity of your comments, differentiating required changes from guidelines or suggestions. Examples:

> Nit: This is a minor thing. Technically you should do it, but it won't hugely impact things.

> Optional (or Consider): I think this may be a good idea, but it's not strictly required.

> FYI: I don't expect you to do this in this CL, but you may find this interesting to think about for the future.

This makes review intent explicit and helps authors prioritize the importance of various comments. It also helps avoid misunderstandings: without comment labels, authors may interpret all comments as mandatory, even when some are merely informational or optional.

Sources: https://google.github.io/eng-practices/review/reviewer/comments.html

## Accepting Explanations

[ref: #comments-accepting-explanations]

If you ask a developer to explain a piece of code you don't understand, that should usually result in them **rewriting the code more clearly**. Occasionally, adding a comment in the code is also an appropriate response, as long as it's not just explaining overly complex code.

**Explanations written only in the code review tool are not helpful to future code readers.** They are acceptable only in a few circumstances, such as when you are reviewing an area you are not very familiar with and the developer explains something that normal readers of the code would have already known.

Sources: https://google.github.io/eng-practices/review/reviewer/comments.html
