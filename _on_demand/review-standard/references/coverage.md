---
subject: "What reviewer must examine per Google eng-practices; overall design, intended functionality, UI impact, concurrency safety, excess complexity, over-engineering, unit integration end-to-end tests, naming clarity, why-comments, style guide conformance, local consistency, documentation updates, every-line reading, broad context, code health direction, praising good work, reviewer checklist summary."
index:
  - anchor: coverage-design
    what: "The design checkpoint: interactions of the CL's pieces make sense, the change belongs in this codebase or a library, it integrates with the system, and now is the right time to add it."
    problem: "Agent evaluates whether reviewer examined overall design at all; reviews that skip design approve architectural damage line by line; system fit, library placement, integration sense, timing question, architecture check, module boundaries, ownership scope, upstream dependency."
    use_when: "Assessing review coverage of architecture; checking whether design concerns were raised before line-level ones."
    avoid_when: "Judging the design decision itself against engineering principles (principles.md); process ordering (process.md)."
    expected: "Coverage verdict records whether design was the reviewer's first-order concern."
  - anchor: coverage-functionality
    what: "The functionality checkpoint: the CL does what the developer intended, the intent is good for users (end-users and future developers), edge cases and concurrency are thought through, UI changes are validated by demo or patching."
    problem: "Agent checks whether reviewer verified behavior versus merely reading diffs; bugs visible only by thinking like user slip through; race conditions, deadlock risk, user perspective, intent match, behavior verification, demo request."
    use_when: "Review involved behavior changes, UI changes, or parallel programming; assessing bug-spotting diligence."
    avoid_when: "Pure refactoring reviews with tests proving no behavior change; style-only assessments (coverage-style)."
    expected: "Verdict states whether functionality reasoning (not just reading) was demonstrably applied."
  - anchor: coverage-complexity
    what: "The complexity checkpoint: the CL is no more complex than needed at line, function, and class level; over-engineering for speculative future needs is called out."
    problem: "Agent weighs whether reviewer challenged unneeded generality; abstraction towers pass unreviewed and ossify; over-engineering, future-proofing, YAGNI dispute, abstraction cost, readability speed, layered design, imagined requirements, present need, gold plating, solve now."
    use_when: "Change adds generics, layers, or features not presently needed; reviewer accepted complexity without challenge."
    avoid_when: "Evaluating naming or comments (coverage-naming, coverage-comments); size of the CL itself (process.md)."
    expected: "Verdict records whether 'solve today's problem' was enforced against speculative design."
  - anchor: coverage-tests
    what: "The tests checkpoint: appropriate unit/integration/end-to-end tests accompany the change in the same CL, and a human verified the tests are correct, sensible, useful, and maintainable."
    problem: "Agent inspects whether tests were reviewed as code, not waved through; vacuous suites enter unchallenged; assertion usefulness, false alarms, suite maintenance, human validation, coverage depth, flaky risk, integration scope, end-to-end confidence."
    use_when: "Change adds or modifies logic; review ignored test quality or accepted tests in a later CL."
    avoid_when: "Emergency changes (conflicts.md relaxes same-CL rule); documentation-only diffs."
    expected: "Verdict states whether tests arrived in the same CL and were themselves reviewed."
  - anchor: coverage-naming
    what: "The naming checkpoint: every identifier is long enough to communicate what the item is or does, without becoming hard to read."
    problem: "Agent checks whether reviewer read names critically; unclear handles pass review and confuse every future reader; pronounceable identifiers, meaning length, searchable tokens, reader comprehension, concept mapping, domain vocabulary, misleading labels."
    use_when: "Change introduces new identifiers; reviewer never commented on unclear names."
    avoid_when: "Comment-style assessment (coverage-comments); design-level naming of concepts (coverage-design)."
    expected: "Verdict records whether names were part of the review."
  - anchor: coverage-comments
    what: "The comments checkpoint: comments are clear, necessary, and explain why rather than what; unclear code is simplified instead of commented; pre-existing comments and TODOs are reconsidered."
    problem: "Agent examines whether reviewer enforced why-over-what commenting; explanatory prose accumulates instead of simplification; rationale capture, decision reasoning, TODO cleanup, prose cruft, self-explaining code, comment necessity, algorithm exception, stale notes, reader questions."
    use_when: "Change adds comments or convoluted code with explanatory prose; reviewer accepted what-comments."
    avoid_when: "Doc-comment and README coverage (coverage-documentation); review-comment tone (comments.md)."
    expected: "Verdict states whether comments were judged on necessity and why-content."
  - anchor: coverage-style
    what: "The style checkpoint: the CL follows the applicable style guide; non-guide style preferences are marked `Nit:` and never block; major reformatting is split from functional change."
    problem: "Agent decides whether style blocking was legitimate; personal taste dressed as requirement stalls submissions; whitespace wars, nitpick labeling, taste versus guide, reformat separation, preference blocking, formatter config, bikeshedding, convention source, auto-format."
    use_when: "Review contains style comments or style-based blocking; reformat mixed with logic."
    avoid_when: "Local inconsistency with existing code (coverage-consistency); design disagreements (principles.md)."
    expected: "Verdict cites whether style demands stayed inside guide authority and `Nit:` discipline."
  - anchor: coverage-consistency
    what: "The consistency checkpoint: style-guide requirements win over existing code; for recommendations it is a judgment call biased toward the guide; otherwise consistency with the codebase, plus a bug and TODO for cleanup."
    problem: "Agent weighs consistency-versus-guide rulings in review; wrong-side demands force conformity that degrades health; local convention, surrounding idioms, cleanup ticket, guide bias, confusing divergence, legacy style, uniformity pressure, migration path, mixed conventions."
    use_when: "New code diverges from surrounding style; reviewer demanded consistency or guide conformance."
    avoid_when: "Pure guide-covered style points (coverage-style); dispute escalation mechanics (principles.md)."
    expected: "Verdict records which side of the guide-versus-codebase line was chosen and why."
  - anchor: coverage-documentation
    what: "The documentation checkpoint: changes to how users build, test, interact with, or release code update the associated docs; deleted or deprecated code gets its documentation deleted; missing docs are requested."
    problem: "Agent checks whether documentation drift was caught; behavior changes ship while reference texts silently rot; README updates, user-facing surface, release notes, stale guides, docs request, build instructions, usage docs, audience shift."
    use_when: "Change alters build/test/usage/release surface or removes code; review never mentioned docs."
    avoid_when: "Inline code comments (coverage-comments); pure internal refactorings with no user-visible surface."
    expected: "Verdict states whether documentation impact was reviewed alongside code."
  - anchor: coverage-every-line
    what: "The every-line rule: review every line assigned — no skimming human-written code; exceptions only for scoped multi-reviewer splits, noted in a comment; unreadable code is sent back for clarification."
    problem: "Agent assesses reviewer thoroughness claims; partial reviews silently assume unread code is fine and miss defects; skimming risk, assigned scope, declared scoping, qualification limits, domain expertise, security privacy, sign-off honesty, line coverage."
    use_when: "Judging whether reviewer actually read the change; multi-reviewer scope splits; unreadable code handling."
    avoid_when: "Generated code or data files scanning; overall review latency (process.md)."
    expected: "Verdict states what was read, what was scoped out, and whether scoping was declared."
  - anchor: coverage-context
    what: "The context rule: view the CL in broad context — whole file, not diff neighborhood — and as system-level code health: never accept changes that degrade it, even by small increments."
    problem: "Agent evaluates whether reviewer saw beyond diff hunk; four-line additions to fifty-line monsters pass because surroundings never opened; hunk tunnel, system perspective, incremental rot, file-level reading, surrounding methods, accumulation effect, scope blindness."
    use_when: "Review shows signs of hunk-only reading; small complexity increments accumulated unchallenged."
    avoid_when: "Single-file trivial changes where context adds nothing; design-fit questions (coverage-design)."
    expected: "Verdict records whether wider file and system context informed the review."
  - anchor: coverage-good-things
    what: "The good-things rule: tell developers what they did well — encouragement and appreciation, especially for great responses to comments, are part of review and mentor better than criticism."
    problem: "Agent gauges whether review was purely negative; mistake-only feedback demoralizes and teaches less than balanced response; encouragement, appreciation, praise balance, mentoring signal, morale effect, good practice recognition, win acknowledgment, rapport building."
    use_when: "Assessing review tone and mentoring quality; long review relationships showing only criticism."
    avoid_when: "Courtesy of individual comments (comments.md); approve-block legitimacy (principles.md)."
    expected: "Verdict notes presence or absence of positive reinforcement."
  - anchor: coverage-summary
    what: "The summary checklist: the standard's own closing list of everything a review must ensure — design, functionality, UI, concurrency, complexity, tests, naming, comments, documentation, style, every line, context, code health, good things."
    problem: "Agent needs one-screen completeness check for review coverage; per-zone verdicts exist but overall statement missing; closing inventory, zone enumeration, full sweep, totality verdict, gap scan, final pass, nothing skipped, sign-off list, holistic view."
    use_when: "Final coverage verdict for a whole review; confirming no zone was skipped."
    avoid_when: "Deep assessment of one zone (that zone's own card); process speed evaluation (process.md)."
    expected: "Every zone of the checklist is marked assessed or consciously out of scope."
---

# Review Coverage (What to Look For)

The verbatim standard of `looking-for.html`, one section per checkpoint. The core standard of `principles.md` governs every checkpoint here.

## Design

[ref: #coverage-design]

The most important thing to cover in a review is the overall design of the CL. Do the interactions of various pieces of code in the CL make sense? Does this change belong in your codebase, or in a library? Does it integrate well with the rest of your system? Is now a good time to add this functionality?

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Functionality

[ref: #coverage-functionality]

Does this CL do what the developer intended? Is what the developer intended good for the users of this code? The "users" are usually both end-users (when they are affected by the change) and developers (who will have to "use" this code in the future).

Mostly, developers are expected to test CLs well enough that they work correctly by the time they get to code review. However, as the reviewer you should still be thinking about edge cases, looking for concurrency problems, trying to think like a user, and making sure that there are no bugs that you see just by reading the code.

You _can_ validate the CL if you want — the time when it's most important for a reviewer to check a CL's behavior is when it has a user-facing impact, such as a **UI change**. It's hard to understand how some changes will impact a user when you're just reading the code. For changes like that, you can have the developer give you a demo of the functionality if it's too inconvenient to patch in the CL and try it yourself.

Another time when it's particularly important to think about functionality during a code review is if there is some sort of **parallel programming** going on in the CL that could theoretically cause deadlocks or race conditions. These sorts of issues are very hard to detect by just running the code and usually need somebody (both the developer and the reviewer) to think through them carefully to be sure that problems aren't being introduced. (Note that this is also a good reason not to use concurrency models where race conditions or deadlocks are possible — it can make it very complex to do code reviews or understand the code.)

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Complexity

[ref: #coverage-complexity]

Is the CL more complex than it should be? Check this at every level of the CL — are individual lines too complex? Are functions too complex? Are classes too complex? "Too complex" usually means **"can't be understood quickly by code readers."** It can also mean **"developers are likely to introduce bugs when they try to call or modify this code."**

A particular type of complexity is **over-engineering**, where developers have made the code more generic than it needs to be, or added functionality that isn't presently needed by the system. Reviewers should be especially vigilant about over-engineering. Encourage developers to solve the problem they know needs to be solved _now_, not the problem that the developer speculates _might_ need to be solved in the future. The future problem should be solved once it arrives and you can see its actual shape and requirements in the physical universe.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Tests

[ref: #coverage-tests]

Ask for unit, integration, or end-to-end tests as appropriate for the change. In general, tests should be added in the same CL as the production code unless the CL is handling an emergency (`conflicts.md`).

Make sure that the tests in the CL are correct, sensible, and useful. Tests do not test themselves, and we rarely write tests for our tests — a human must ensure that tests are valid.

Will the tests actually fail when the code is broken? If the code changes beneath them, will they start producing false positives? Does each test make simple and useful assertions? Are the tests separated appropriately between different test methods?

Remember that tests are also code that has to be maintained. Don't accept complexity in tests just because they aren't part of the main binary.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Naming

[ref: #coverage-naming]

Did the developer pick good names for everything? A good name is long enough to fully communicate what the item is or does, without being so long that it becomes hard to read.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Comments

[ref: #coverage-comments]

Did the developer write clear comments in understandable English? Are all of the comments actually necessary? Usually comments are useful when they **explain why** some code exists, and should not be explaining _what_ some code is doing. If the code isn't clear enough to explain itself, then the code should be made simpler. There are some exceptions (regular expressions and complex algorithms often benefit greatly from comments that explain what they're doing, for example) but mostly comments are for information that the code itself can't possibly contain, like the reasoning behind a decision.

It can also be helpful to look at comments that were there before this CL. Maybe there is a TODO that can be removed now, a comment advising against this change being made, etc.

Note that comments are different from _documentation_ of classes, modules, or functions, which should instead express the purpose of a piece of code, how it should be used, and how it behaves when used.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Style

[ref: #coverage-style]

We have style guides at Google for all of our major languages, and even for most of the minor languages. Make sure the CL follows the appropriate style guide.

If you want to improve some style point that isn't in the style guide, prefix your comment with `Nit:` to let the developer know that it's a nitpick that you think would improve the code but isn't mandatory. Don't block CLs from being submitted based only on personal style preferences.

The author of the CL should not include major style changes combined with other changes. It makes it hard to see what is being changed in the CL, makes merges and rollbacks more complex, and causes other problems. For example, if the author wants to reformat the whole file, have them send you just the reformatting as one CL, and then send another CL with their functional changes after that.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Consistency

[ref: #coverage-consistency]

What if the existing code is inconsistent with the style guide? Per the code review principles (`principles.md`), the style guide is the absolute authority: if something is required by the style guide, the CL should follow the guidelines.

In some cases, the style guide makes recommendations rather than declaring requirements. In these cases, it's a judgment call whether the new code should be consistent with the recommendations or the surrounding code. Bias towards following the style guide unless the local inconsistency would be too confusing.

If no other rule applies, the author should maintain consistency with the existing code.

Either way, encourage the author to file a bug and add a TODO for cleaning up existing code.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Documentation

[ref: #coverage-documentation]

If a CL changes how users build, test, interact with, or release code, check to see that it also updates associated documentation, including READMEs, g3doc pages, and any generated reference docs. If the CL deletes or deprecates code, consider whether the documentation should also be deleted. If documentation is missing, ask for it.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Every Line

[ref: #coverage-every-line]

In the general case, look at _every_ line of code that you have been assigned to review. Some things like data files, generated code, or large data structures you can scan over sometimes, but don't scan over a human-written class, function, or block of code and assume that what's inside of it is okay. Obviously some code deserves more careful scrutiny than other code — that's a judgment call — but you should at least be sure that you _understand_ what all the code is doing.

If it's too hard for you to read the code and this is slowing down the review, then let the developer know and wait for them to clarify it before you try to review it. At Google, we hire great software engineers, and you are one of them. If you can't understand the code, it's very likely that other developers won't either. So you're also helping future developers understand this code when you ask the developer to clarify it.

If you understand the code but you don't feel qualified to do some part of the review, make sure there is a reviewer on the CL who is qualified, particularly for complex issues such as privacy, security, concurrency, accessibility, internationalization, etc.

### Exceptions

What if it doesn't make sense for you to review every line? For example, you are one of multiple reviewers on a CL and may be asked to review only certain files that are part of a larger change, or to review only certain aspects of the CL, such as the high-level design, privacy or security implications.

In these cases, note in a comment which parts you reviewed. Prefer giving LGTM with comments (`process.md`). If you instead wish to grant LGTM after confirming that other reviewers have reviewed other parts of the CL, note this explicitly in a comment to set expectations. Aim to respond quickly once the CL has reached the desired state.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Context

[ref: #coverage-context]

It is often helpful to look at the CL in a broad context. Usually the code review tool will only show you a few lines of code around the parts that are being changed. Sometimes you have to look at the whole file to be sure that the change actually makes sense. For example, you might see only four new lines being added, but when you look at the whole file, you see those four lines are in a 50-line method that now really needs to be broken up into smaller methods.

It's also useful to think about the CL in the context of the system as a whole. Is this CL improving the code health of the system or is it making the whole system more complex, less tested, etc.? **Don't accept CLs that degrade the code health of the system.** Most systems become complex through many small changes that add up, so it's important to prevent even small complexities in new changes.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Good Things

[ref: #coverage-good-things]

If you see something nice in the CL, tell the developer, especially when they addressed one of your comments in a great way. Code reviews often just focus on mistakes, but they should offer encouragement and appreciation for good practices, as well. It's sometimes even more valuable, in terms of mentoring, to tell a developer what they did right than to tell them what they did wrong.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html

## Summary

[ref: #coverage-summary]

In doing a code review, you should make sure that:

- The code is well-designed.
- The functionality is good for the users of the code.
- Any UI changes are sensible and look good.
- Any parallel programming is done safely.
- The code isn't more complex than it needs to be.
- The developer isn't implementing things they _might_ need in the future but don't know they need now.
- Code has appropriate unit tests.
- Tests are well-designed.
- The developer used clear names for everything.
- Comments are clear and useful, and mostly explain _why_ instead of _what_.
- Code is appropriately documented (generally in g3doc).
- The code conforms to the style guides.

Make sure to review **every line** of code you've been asked to review, look at the **context**, make sure you're **improving code health**, and compliment developers on **good things** that they do.

Sources: https://google.github.io/eng-practices/review/reviewer/looking-for.html
