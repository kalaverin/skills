---
subject: "Author-side obligations per Google eng-practices developer guide; CL description first line imperative standalone, informative body with context, bad versus good description examples, tags, generated descriptions, small CL definition, self-contained change, large CL exceptions, stacking splitting strategies, refactoring separation, tests same CL, build never broken, reviewer comments handled without anger."
index:
  - anchor: author-side-first-line
    what: "First-line rule for CL descriptions: short imperative complete sentence summarizing exactly what the CL does, standing alone in commit history."
    problem: "Agent judges description quality of change under review; vague first lines cripple future code search and history skimming; imperative sentence, standalone summary, imperative mood, version control record, blank line, search friendliness, commit message."
    use_when: "Evaluating author behavior in review; CL description starts vague or absent."
    avoid_when: "Reviewer-side assessment (comments.md); size evaluation (author-side-what-small)."
    expected: "Verdict states whether first line stands alone as imperative summary."
  - anchor: author-side-body
    what: "Body rule: the rest of the description fills in context — problem being solved, why this approach, its shortcomings, issue tracker numbers, benchmark results, design-doc links carrying enough context inline for future readers."
    problem: "Agent checks whether description explains why, not only what; context trapped in author head forces archaeology on every future reader; context body, rationale record, defect reference, benchmark links, external link fragility, inline context."
    use_when: "Description body empty or restates diff; links dropped without accompanying explanation; evaluating CL documentation."
    avoid_when: "First-line assessment (author-side-first-line); comment content (comments.md)."
    expected: "Verdict states whether body gives why-and-context sufficient for future readers."
  - anchor: author-side-description-examples
    what: "Canonical examples: bad one-liners versus good descriptions (functionality change, refactoring, small contextual), plus tag label rules, generated CL requirements, and re-reviewing the description before submission."
    problem: "Agent needs reference examples when judging concrete descriptions; without canonical pairs every verdict floats on intuition; bad examples, good examples, tag usage, generated description, pre-submission re-check, fix bug antipattern, phase one antipattern."
    use_when: "Scoring a concrete CL description; showing author what good looks like; tags or generated CLs involved."
    avoid_when: "Structure rules already clear (author-side-first-line, author-side-body); non-description assessment."
    expected: "Verdict cites the canonical example class the description matches or violates."
  - anchor: author-side-why-small
    what: "Why-small case: small CLs are reviewed faster and more thoroughly, introduce fewer bugs, waste less when rejected, merge easier, design better, block less, roll back simpler; reviewers may reject outright for size alone."
    problem: "Agent frames size dispute between author and reviewer; large-change authors dispute rejection without knowing reviewer discretion; review speed, thoroughness gain, bug likelihood, rejection waste, merge conflicts, rollback simplicity, outright rejection, reviewer latitude."
    use_when: "Author disputes size-based rejection; assessing whether large-CL rejection was legitimate."
    avoid_when: "Genuinely large allowed cases (author-side-large-okay); reviewer latency (process.md)."
    expected: "Verdict cites reviewer discretion to reject for size when applicable."
  - anchor: author-side-what-small
    what: "Size definition: a single focused, self-contained concern — includes related tests, stays understandable from CL plus description plus codebase, keeps the system working, and is not so tiny that implications hide; roughly 100 lines fine, 1000 too large, distribution across files counts."
    problem: "Agent measures CL size against standard definition; line-count arguments ignore conceptual focus and distribution across many files; self-contained change, one thing, hundred lines, thousand lines, file spread, API usage inclusion, system integrity."
    use_when: "Judging whether CL exceeded acceptable size; author defends large CL by line count alone."
    avoid_when: "Deletion or generated bulk (author-side-large-okay); splitting mechanics (author-side-splitting)."
    expected: "Verdict classifies the CL against the self-contained-change definition."
  - anchor: author-side-large-okay
    what: "Large-CL exceptions: whole-file deletions count as one line of review; trusted auto-refactoring output needs only verification and intent confirmation, though merge and test caveats still apply."
    problem: "Agent evaluates whether large CL legitimately claimed exemption; bulk changes disguise real logic among deletions or tool output; file removal, automated refactoring, tool trust, verification only, exemption legitimacy, hidden logic, merge caveat."
    use_when: "Large CL claims deletion or tool-generation exemption; reviewer rejected or accepted such claim."
    avoid_when: "Hand-written large logic changes (author-side-what-small); splitting strategy choice (author-side-splitting)."
    expected: "Verdict states whether the exemption claim matched the two allowed cases."
  - anchor: author-side-splitting
    what: "Splitting toolbox: stack dependent CLs, split per reviewer-owned directory sets, split horizontally by layers with isolating stubs, split vertically by full-stack features, combine both as grid of standalone CLs."
    problem: "Agent advises or assesses decomposition of large work; monolithic changes sit blocked in review without any decomposition plan and reviewers demand splits; stacking changes, file grouping, horizontal layers, vertical features, shared stubs, proto first, parallel tracks, work breakdown."
    use_when: "Author asks how to split; reviewer demanded split without guidance; evaluating split quality."
    avoid_when: "Size judgment itself (author-side-what-small); review ordering (process.md)."
    expected: "Verdict names the splitting strategy fitting the change structure."
  - anchor: author-side-refactor-tests-build
    what: "Hygiene rules: refactorings go in separate CLs from features and fixes; related test code lives in the same CL (independent test additions may precede); stacked CLs must never break the build; near-large CLs get advance reviewer consent plus extra diligence."
    problem: "Agent checks structural hygiene of author's CL series; mixed refactor-plus-feature diffs unreadable and broken intermediate states hit teammates; refactoring separation, test co-location, build integrity, stacked chain, advance consent, rename isolation, feature mixing."
    use_when: "CL mixes refactoring with behavior change; tests arrive separately from logic; dependent chain breaks build."
    avoid_when: "Small local cleanups inside feature CLs (explicitly allowed); emergency changes (conflicts.md)."
    expected: "Verdict checks separation of cleanups, tests shipped together, and green builds across the series."
  - anchor: author-side-not-personal
    what: "Don't-take-it-personally rule: critique targets code, codebase, and product — never the author's abilities; never respond in anger; walk away until calm; address non-constructive reviewers privately, then escalate."
    problem: "Agent assesses author reaction to criticism; angry replies become permanent professional breaches in review history and damage working relationships across teams; personal attack reading, angry response, permanent record, calm-down distance, private feedback, escalation path, constructive extraction."
    use_when: "Author responded emotionally; author reads critique as aimed at themselves; flame thread in review."
    avoid_when: "Reviewer rudeness assessment (comments-courtesy); content disputes (principles.md)."
    expected: "Verdict states whether author reaction stayed professional per the rule."
  - anchor: author-side-fix-code
    what: "Fix-the-code rule: when a reviewer doesn't understand code, clarify the implementation itself first; only when that fails add a source-level comment; answers posted solely in the review thread are the last resort because future readers never see them."
    problem: "Agent checks how author answered comprehension questions during review; lengthy thread explanations leave code cryptic for everyone who comes after; comprehension response, cryptic remnant, review-tool reply, source comment fallback, reader horizon, question handling."
    use_when: "Author answered clarity questions only in comments; code stayed obscure after review."
    avoid_when: "Reviewer-side explanation requests (comments-accepting-explanations); familiar-area explanations."
    expected: "Verdict states whether answers landed in code or evaporated in thread."
  - anchor: author-side-collaborate
    what: "Collaborative-thinking rule: understand what the reviewer asks before disagreeing; disagree with weighed benefits, drawbacks, and tradeoffs, asking which weighting the reviewer suggests; courtesy stays first; conflicts resolve toward consensus per the standard."
    problem: "Agent judges quality of author disagreement between both parties; refusals without argued tradeoffs stall reviews and escalate unnecessarily; collaborative disagreement, tradeoff weighing, pros cons, clarification request, flat refusal, consensus seeking, context sharing."
    use_when: "Author pushed back on comments; assessing whether pushback argued tradeoffs or refused flatly."
    avoid_when: "Reviewer-side persistence (conflicts-who-is-right); escalation mechanics (principles.md)."
    expected: "Verdict classifies disagreement as tradeoff-argued or dismissed outright."
---

# Author Side of Review

The verbatim standard of the CL Author's Guide: descriptions, small CLs, and handling reviewer comments. Used when evaluating the author's behavior in a review, not the reviewer's.

## First Line of the Description

[ref: #author-side-first-line]

The **first line** of a CL description is a short summary of _specifically_ **what** _is being done by the CL_, followed by a blank line. This is what appears in version control history summaries, so it should be informative enough that future code searchers don't have to read the CL or its whole description to understand what your CL actually _did_ or how it differs from other CLs. The first line should stand alone, allowing readers to skim through code history much faster.

Keep the first line short, focused, and to the point. Clarity and utility to the reader are the top concern.

By tradition, the first line is a complete sentence, written as though it were an order (an imperative sentence). For example, say "**Delete** the FizzBuzz RPC and **replace** it with the new system" instead of "**Deleting** the FizzBuzz RPC and **replacing** it with the new system." The rest of the description doesn't have to be imperative.

A CL description is a public record of change: **what** is being changed and **why**. It becomes a permanent part of version control history, possibly read by hundreds of people over the years. Future developers will search for your CL based on its description; someone might look for your change because of a faint memory of its relevance but without the specifics handy. Reading source code may reveal what software does but not why it exists — which matters when deciding whether code can be moved (Chesterton's fence).

Sources: https://google.github.io/eng-practices/review/developer/cl-descriptions.html

## Body Is Informative

[ref: #author-side-body]

The rest of the description should be informative: a brief description of the problem being solved and why this is the best approach. If there are shortcomings to the approach, mention them. If relevant, include background information such as bug numbers, benchmark results, and links to design documents.

If you include links to external resources, consider that they may not be visible to future readers due to access restrictions or retention policies. Where possible, include enough context for reviewers and future readers to understand the CL.

Even small CLs deserve a little attention to detail. Put the CL in context.

Sources: https://google.github.io/eng-practices/review/developer/cl-descriptions.html

## Description Examples, Tags, Generated CLs

[ref: #author-side-description-examples]

Bad CL descriptions: "Fix bug", "Fix build", "Add patch", "Moving code from A to B", "Phase 1", "Add convenience functions", "kill weird URLs" — short, but without enough useful information.

Good descriptions:

Functionality change:

> RPC: Remove size limit on RPC server message freelist.
>
> Servers like FizzBuzz have very large messages and would benefit from reuse. Make the freelist larger, and add a goroutine that frees the freelist entries slowly over time, so that idle servers eventually release all freelist entries.

The first few words describe what the CL actually does; the rest talks about the problem being solved, why this is a good solution, and more about the implementation.

Refactoring:

> Construct a Task with a TimeKeeper to use its TimeStr and Now methods.
>
> Add a Now method to Task, so the borglet() getter method can be removed (which was only used by OOMCandidate to call borglet's Now method). This replaces the methods on Borglet that delegate to a TimeKeeper.
>
> Allowing Tasks to supply Now is a step toward eliminating the dependency on Borglet. Eventually, collaborators that depend on getting Now from the Task should be changed to use a TimeKeeper directly, but this has been an accommodation to refactoring in small steps.
>
> Continuing the long-range goal of refactoring the Borglet Hierarchy.

The first line describes what the CL does and how this changes the past; the rest talks about the specific implementation, the context, that the solution isn't ideal, and possible future direction — and explains _why_.

Small CL needing context:

> Create a Python3 build rule for status.py.
>
> This allows consumers who are already using this as in Python3 to depend on a rule that is next to the original status build rule instead of somewhere in their own tree. It encourages new consumers to use Python3 if they can, instead of Python2, and significantly simplifies some automated build file refactoring tools being worked on currently.

The first sentence describes what's actually being done; the rest explains _why_, giving the reviewer a lot of context.

**Tags** are manually entered labels to categorize CLs (`[tag]`, `#tag`, `tag:`), optional, and should be limited in the first line — long or numerous tags overwhelm it; move them into the body. Examples:

Good — short tags stay readable:

```txt
[banana] Peel the banana before eating.
Peel the #banana before eating.
#banana #apple: Assemble a fruit basket.
```

Bad — too many or too long tags overwhelm the first line; move them into the description body or shorten them:

```txt
[banana peeler factory factory][apple picking service] Assemble a fruit basket.
```

**Generated CL descriptions**: CLs produced by tools should follow the same advice whenever possible — short standalone first line, informative body.

**Review the description before submitting**: CLs can undergo significant change during review; re-check that the description still reflects what the CL does before submitting.

Sources: https://google.github.io/eng-practices/review/developer/cl-descriptions.html

## Why Small CLs

[ref: #author-side-why-small]

Small, simple CLs are:

- **Reviewed more quickly.** A reviewer finds five minutes several times more easily than a 30-minute block for one large CL.
- **Reviewed more thoroughly.** Large changes frustrate reviewers and authors with volumes of detailed commentary shifting back and forth — important points get missed or dropped.
- **Less likely to introduce bugs.** Fewer changes make it easier to reason effectively about impact.
- **Less wasted work if rejected.** A huge CL rejected for direction wastes a lot of work.
- **Easier to merge.** Large CLs take long, producing frequent conflicts.
- **Easier to design well.** Polishing a small change's design and code health beats refining every detail of a large one.
- **Less blocking on reviews.** Self-contained portions let you keep coding while waiting.
- **Simpler to roll back.** Large CLs touch files updated between submission and rollback, complicating it.

Note that **reviewers have discretion to reject your change outright for the sole reason of it being too large.** Usually they thank you for the contribution but request a series of smaller changes. Splitting after the fact is a lot of work; write small CLs in the first place.

Sources: https://google.github.io/eng-practices/review/developer/small-cls.html

## What Is Small

[ref: #author-side-what-small]

The right size for a CL is **one self-contained change**:

- The CL makes a minimal change that addresses **just one thing** — usually one part of a feature, not the whole feature. Err on the side of too small versus too large. Work with your reviewer on acceptable size.
- The CL includes related test code.
- Everything the reviewer needs to understand the CL (except future development) is in the CL, its description, the existing codebase, or a CL they've already reviewed.
- The system continues to work well for users and developers after the CL lands.
- The CL is not so small that its implications become hard to understand: adding a new API should include a usage of it in the same CL, so reviewers see how it will be used (this also prevents checking in unused APIs).

No hard rules about "too large": 100 lines is usually reasonable, 1000 lines usually too large — reviewer judgment decides. File spread matters too: a 200-line change in one file might be okay; spread across 50 files it would usually be too large.

The reviewer often has no context: what seems acceptably sized to you might overwhelm them. When in doubt, write CLs smaller than you think you need. Reviewers rarely complain about CLs being too small.

Sources: https://google.github.io/eng-practices/review/developer/small-cls.html

## When Large CLs Are Okay

[ref: #author-side-large-okay]

A few situations where large changes aren't as bad:

- Deletion of an entire file usually counts as just one line of change — it doesn't take the reviewer long.
- A large CL generated by an automatic refactoring tool you trust completely, where the reviewer's job is only to verify and confirm intent — these can be larger, though merge and testing caveats still apply.

Sources: https://google.github.io/eng-practices/review/developer/small-cls.html

## Splitting CLs

[ref: #author-side-splitting]

Strategies for splitting work into different CLs:

- **Stacking multiple changes:** write one small CL, send it for review, then immediately start another CL _based_ on the first. Most version control systems allow this.
- **Splitting by files:** group files requiring different reviewers but otherwise self-contained (e.g. one CL for protocol-buffer modifications, another for code using the proto; or one CL for code, another for the configuration or experiment using it — easier to roll back). Inform both reviewer sets about the other CL.
- **Splitting horizontally:** create shared code or stubs isolating changes between layers of the tech stack (e.g. a shared proto signature abstracts service and data-model layers; an API stub splits client implementation from service code).
- **Splitting vertically:** break code into smaller full-stack features — independent parallel implementation tracks, each moving while others await review.
- **Horizontally and vertically combined:** chart the implementation as a grid where each cell (layer × feature) is its own standalone CL, starting from the model up to the client.

Writing small CLs efficiently: writing a small CL and then idly waiting for approval wastes time — work in multiple projects, find immediately available reviewers, do in-person reviews, pair-program, or split so you can continue working immediately.

Sources: https://google.github.io/eng-practices/review/developer/small-cls.html

## Refactoring Separation, Tests, Build Integrity

[ref: #author-side-refactor-tests-build]

**Separate out refactorings:** refactorings go in a different CL from feature changes or bug fixes — moving or renaming a class belongs in a different CL from fixing a bug in that class. Small cleanups (fixing a local variable name) can ride inside a feature or bug-fix CL; developer and reviewer judgment decides when a refactoring grows large enough to harm the current review.

**Keep related test code in the same CL:** smallness here refers to the conceptual idea that the CL should be focused — not a simplistic function of line count. Tests are expected for all changes. A CL that adds or changes logic comes with new or updated tests for the new behavior. Pure refactoring CLs (not intended to change behavior) should also be covered by tests — ideally existing ones; otherwise add them. _Independent_ test modifications can go into separate CLs first: validating pre-existing code with new tests before refactoring, refactoring test code itself, or introducing larger test-framework code.

**Don't break the build:** with several CLs depending on each other, the whole system must keep working after each CL is submitted — otherwise you break the build for fellow developers between submissions.

**Can't make it small enough:** this is very rarely true. Before writing a large CL, consider whether a preceding refactoring-only CL could pave the way; talk to teammates about decomposition. If all options fail (extremely rare), get consent from your reviewers in advance, expect a long review process, be vigilant about bugs, and be extra diligent about tests.

Sources: https://google.github.io/eng-practices/review/developer/small-cls.html

## Don't Take It Personally

[ref: #author-side-not-personal]

The goal of review is maintaining codebase and product quality. When a reviewer critiques your code, think of it as an attempt to help you, the codebase, and the company — not a personal attack on you or your abilities.

Sometimes reviewers feel frustrated and express it in their comments. This isn't good practice for reviewers, but be prepared: ask yourself "What is the constructive thing the reviewer is trying to communicate?" and operate as though that's what they actually said.

**Never respond in anger to code review comments.** That is a serious breach of professional etiquette that lives forever in the code review tool. Too angry or annoyed to respond kindly — walk away from the computer or work on something else until calm enough to reply politely.

If a reviewer isn't providing feedback constructively and politely, explain it to them in person or on a video call; otherwise send a private email, kindly explaining what you don't like and what they'd do differently. If that discussion goes nowhere, escalate to your manager as appropriate.

Sources: https://google.github.io/eng-practices/review/developer/handling-comments.html

## Fix the Code

[ref: #author-side-fix-code]

If a reviewer says they don't understand something in your code, your first response should be to clarify the code itself. If the code can't be clarified, add a code comment explaining why the code is there. Only if a comment seems pointless should your response be an explanation in the code review tool.

If a reviewer didn't understand some piece of your code, likely other future readers won't either. A response in the code review tool doesn't help future code readers; clarifying your code or adding code comments does.

Sources: https://google.github.io/eng-practices/review/developer/handling-comments.html

## Think Collaboratively

[ref: #author-side-collaborate]

Writing a CL is a lot of work, and receiving comments asking for changes — especially ones you disagree with — is frustrating. Step back and consider whether the reviewer is providing valuable feedback. Your first question to yourself should always be "Do I understand what the reviewer is asking for?" If you can't answer, ask for clarification.

If you understand the comments but disagree, think collaboratively, not combatively or defensively:

Bad — flat refusal, no reasoning:

```txt
"No, I'm not going to do that."
```

Good — disagreement argued through tradeoffs:

```txt
"I went with X because of [these pros/cons] with [these tradeoffs]
My understanding is that using Y would be worse because of [these reasons].
Are you suggesting that Y better serves the original tradeoffs, that we should
weigh the tradeoffs differently, or something else?"
```

Courtesy and respect always stay a first priority. If you disagree, find ways to collaborate: ask for clarifications, discuss pros/cons, explain why your method is better for the codebase, users, and company. Sometimes you know something about the users, codebase, or CL that the reviewer doesn't — fix the code where appropriate and engage the reviewer with more context. Usually you can come to consensus based on technical facts. If consensus fails, see the conflict-resolution standard (`principles.md`).

Sources: https://google.github.io/eng-practices/review/developer/handling-comments.html
