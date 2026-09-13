---
subject: "Review process mechanics per Google eng-practices; broad view first, main parts before details, logical file sequence, team velocity over individual speed, one business day maximum response, focused-task interruption cost, quick partial responses, cross-time-zone timing, `LGTM` with comments, large CL splitting, review acceleration over time, emergency priority."
index:
  - anchor: process-summary
    what: "The navigation summary: check the change makes sense and has a good description, examine the most important part before anything else, then review the rest in an appropriate sequence."
    problem: "Agent needs overall pass structure before step-level verdicts; reviews evaluated piecemeal miss wrong ordering across whole pass; overview triple, sense check, description gate, main part first, sequence rest, pass skeleton, holistic lens, traversal shape."
    use_when: "Starting process assessment of a review; confirming the reviewer followed any deliberate order at all."
    avoid_when: "Step-level assessment (process-broad-view, process-main-parts, process-sequence); speed questions (process-how-fast)."
    expected: "Overall ordering judgment precedes per-step verdicts."
  - anchor: process-broad-view
    what: "Step one of navigating a CL: read the description and decide whether the change should exist at all; reject misdirected work immediately and courteously, suggesting the right direction."
    problem: "Agent assesses whether reviewer validated existence of change before diving in; unwanted modifications receive line polish instead of refusal; premature approval, wasted polish, courteous no, direction suggestion, purpose gate, scope rejection, early signal, misplaced effort."
    use_when: "Review touched a system being removed; reviewer never questioned the change's existence; rejection quality assessment."
    avoid_when: "Design-fit within an accepted change (coverage-design); response timing (process-how-fast)."
    expected: "Verdict states whether purpose validation happened before detail review."
  - anchor: process-main-parts
    what: "Step two: find the main part of the CL (usually the file with most logical changes), review it first, and send major design comments immediately rather than completing a full pass."
    problem: "Agent checks pass ordering of review; late architecture remarks force rework of code built atop bad foundation; centerpiece identification, biggest file, context cascade, stacked rework, immediate escalation, nit-first trap, deadline pressure, priority inversion."
    use_when: "Reviewer commented nits before architecture; design feedback arrived after full review; CL too large to identify main part."
    avoid_when: "Single-file trivial CLs; comment wording assessment (comments.md)."
    expected: "Verdict records whether major design issues were surfaced before detail comments."
  - anchor: process-sequence
    what: "Step three: after confirming no major design problems, review remaining files in a logical sequence without missing any — tool order is fine; reading tests first can clarify intent."
    problem: "Agent verifies file-visit completeness after design sign-off; scattered jumping leaves chunks unreviewed; systematic sweep, coverage bookkeeping, tests-first order, intent clarity, traversal plan, missed chunk, hopscotch reading, final pass, residual risk."
    use_when: "Assessing whether every file got reviewed; checking review completeness claims."
    avoid_when: "First-pass design evaluation (process-main-parts); scope-split reviews (coverage-every-line)."
    expected: "Verdict confirms systematic coverage of all remaining files."
  - anchor: process-why-fast
    what: "The velocity rationale: team output speed outranks individual speed; slow reviews decrease team velocity, breed process complaints, and degrade code health through submission pressure."
    problem: "Agent evaluates chronic review slowness across team; delayed feedback breeds frustration misread as strictness and weak approvals; group throughput, latency spiral, discouragement effect, cleanup deterrence, quality erosion, morale drain, cadence failure, complaint root."
    use_when: "Assessing review cadence problems; complaints about reviewer strictness correlate with slow responses."
    avoid_when: "Single-instance latency (process-how-fast); emergency prioritization (conflicts.md)."
    expected: "Verdict ties observed friction to response-time cause where standard supports it."
  - anchor: process-how-fast
    what: "The latency rule: review shortly after it comes in unless mid-focused-task; one business day maximum for a response; multiple review rounds should fit a single day."
    problem: "Agent measures reviewer reply latency against explicit maximum; multi-day silence violates regardless of eventual thoroughness; morning deadline, acknowledgment gap, waiting author, promptness ceiling, same-day turnaround, daily cap, idle queue, unattended request."
    use_when: "Review waited days for first response; evaluating SLA conformance of reviewer behavior."
    avoid_when: "Reviewer was mid-focused-task (process-interruption); emergency reviews (conflicts.md)."
    expected: "Verdict states measured latency against the one-business-day ceiling."
  - anchor: process-interruption
    what: "The interruption exception: personal velocity trumps team velocity exactly once — never interrupt a focused coding task for review; respond at the next break point instead."
    problem: "Agent weighs reviewer claim of focus protection; exception legitimately postpones answers yet becomes excuse when permanent; deep work, flow state, context switching, resume penalty, coding immersion, task boundary, pause window, concentration guard."
    use_when: "Reviewer delayed while coding; judging whether focus exception was invoked in good faith."
    avoid_when: "Reviewer simply idle (process-how-fast ceiling applies); cross-time-zone cases (process-time-zones)."
    expected: "Verdict classifies the postponement as bona fide flow protection or ceiling breach."
  - anchor: process-fast-responses
    what: "The response-priority rule: individual responses matter more than total process time; when busy, send a quick acknowledgment with timing, alternative reviewers, or initial broad comments — but never let speed hollow out the LGTM."
    problem: "Agent distinguishes slow pipeline from slow replies; authors tolerate long thorough review when each answer arrives quickly; acknowledgment note, timing promise, initial impressions, per-round speed, duration split, responsiveness signal, silence cost."
    use_when: "Review took long overall but each round was prompt; reviewer went silent without acknowledgment."
    avoid_when: "Measuring single latency (process-how-fast); LGTM-with-comments decision (process-lgtm-with-comments)."
    expected: "Verdict separates per-response speed from end-to-end duration."
  - anchor: process-time-zones
    what: "The time-zone rule: with timezone differences, answer while the author can still respond that working day, or finish the review before their next morning."
    problem: "Agent assesses zone-aware timing; replies landing after author's workday multiply day-long cycles; geographic split, daylight window, overnight wait, calendar latency, offshore pair, response window, daily rhythm, handoff lag, clock offset, overlap hours."
    use_when: "Author and reviewer in different zones; reviews consumed multiple days purely by timing."
    avoid_when: "Same-zone latency (process-how-fast); focus-exception claims (process-interruption)."
    expected: "Verdict records whether timing respected author's working hours."
  - anchor: process-lgtm-with-comments
    what: "LGTM with comments: approve despite unresolved comments when the developer will address them, the comments are optional, or the suggestions are minor — and specify which case applies; especially valuable across time zones."
    problem: "Agent evaluates approval-with-open-comments decisions; blanket blocking over trivia wastes days while unexplained approval confuses; trust basis, minor fixes, optional remarks, intent labeling, conditional signoff, import sorting, typo class, day saving."
    use_when: "Reviewer approved with open comments; reviewer blocked over trivia; assessing stated intent of approval."
    avoid_when: "Full rejections (principles-core-standard); emergency speed (conflicts.md)."
    expected: "Verdict states whether approval conditions matched the three legitimate cases."
  - anchor: process-large-cls
    what: "The large-CL rule: ask to split oversized reviews into smaller dependent CLs; when splitting is impossible, give design comments and return for improvement — always unblock the author quickly without sacrificing code health."
    problem: "Agent checks handling of giant review; huge change stalls or receives rubber stamp instead of decomposition; piecemeal chain, dependent series, reviewability limit, size refusal, unblocking duty, superficial pass, incremental landing, staged submission, reviewer capacity."
    use_when: "CL too large to review promptly; reviewer either stalled or approved superficially."
    avoid_when: "Generated or deletion-heavy large CLs (author_side.md exemptions); normal-size reviews."
    expected: "Verdict records whether split was requested or design-first feedback given."
  - anchor: process-improvements
    what: "The compounding claim: strict fast reviews accelerate over time as developers learn and send better CLs — but never trade standard or quality for imagined velocity."
    problem: "Agent weighs long-term trajectory of review rigor; teams relax standards expecting speed and obtain neither; compounding effect, learned behavior, better submissions, ratchet quality, false economy, capability growth, latency decline, steady acceleration, habit formation."
    use_when: "Assessing whether rigor improved over months; judging proposals to soften standards for velocity."
    avoid_when: "Single-review latency verdicts (process-how-fast); emergency relaxation (conflicts.md)."
    expected: "Verdict notes trend direction and rejects quality-for-velocity trades."
---

# Review Process (Navigate + Speed)

The verbatim standard of `navigate.html` and `speed.html`: how to move through a CL and how fast reviews must move.

## Summary

[ref: #process-summary]

The most efficient way to manage a review spread across multiple files:

1. Does the change make sense? Does it have a good description? (`author_side.md`)
2. Look at the most important part of the change first. Is it well-designed overall?
3. Look at the rest of the CL in an appropriate sequence.

Sources: https://google.github.io/eng-practices/review/reviewer/navigate.html

## Step One: Broad View

[ref: #process-broad-view]

Look at the CL description and what the CL does in general. Does this change even make sense? If this change shouldn't have happened in the first place, respond immediately with an explanation of why the change should not be happening. When you reject a change like this, suggest to the developer what they should have done instead.

For example: "Looks like you put some good work into this, thanks! However, we're actually going in the direction of removing the FooWidget system you're modifying here, and so we don't want to make any new modifications to it right now. How about instead you refactor our new BarWidget class?"

Note that the reviewer rejected the current CL, provided an alternative suggestion, and did it _courteously_. Courtesy matters: show respect for each other as developers even when disagreeing.

If you get more than a few CLs representing changes you don't want to make, consider re-working your team's development process or the posted process for external contributors, so there is more communication before CLs are written. It's better to tell people "no" before they've done a ton of work that now has to be thrown away or drastically re-written.

Sources: https://google.github.io/eng-practices/review/reviewer/navigate.html

## Step Two: Main Parts First

[ref: #process-main-parts]

Find the file or files that are the "main" part of the CL. Often there is one file with the largest number of logical changes — the major piece of the CL. Look at these major parts first: this gives context to all the smaller parts and generally accelerates the review. If the CL is too large to figure out which parts are major, ask the developer what to look at first, or ask them to split the CL.

If you see major design problems with this part of the CL, send those comments immediately, even without time to review the rest. Reviewing the rest might be a waste of time: if the design problems are significant enough, much of the other code under review will disappear anyway.

Two major reasons to send major design comments immediately:

- Developers often mail a CL and immediately start new work based on it while waiting for review. If there are major design problems in the CL you're reviewing, they'll have to re-work the later CL too. Catch them before they've done too much extra work on top of the problematic design.
- Major design changes take longer than small ones. Developers nearly all have deadlines; to make those deadlines and still have quality code, the developer needs to start any major re-work as soon as possible.

Sources: https://google.github.io/eng-practices/review/reviewer/navigate.html

## Step Three: The Rest in Sequence

[ref: #process-sequence]

Once you've confirmed there are no major design problems with the CL as a whole, figure out a logical sequence to look through the files while making sure you don't miss reviewing any file. Usually after the major files, it's simplest to go through each file in the order the code review tool presents them. Sometimes it's helpful to read the tests before the main code, because then you have an idea of what the change is supposed to be doing.

Sources: https://google.github.io/eng-practices/review/reviewer/navigate.html

## Why Reviews Must Be Fast

[ref: #process-why-fast]

**At Google, the optimization target is the speed at which a team of developers can produce a product together**, as opposed to the speed at which an individual developer writes code. Individual development speed matters, just not _as_ much as the velocity of the entire team.

When code reviews are slow:

- **The velocity of the team as a whole decreases.** The individual who doesn't respond quickly gets other work done; however, new features and bug fixes for the rest of the team are delayed by days, weeks, or months as each CL waits for review and re-review.
- **Developers start to protest the code review process.** A reviewer who responds every few days but requests major changes each time is frustrating. The same substantial changes requested with _quick_ responses tend to make complaints disappear. **Most complaints about the code review process are actually resolved by making the process faster.**
- **Code health can be impacted.** Slow reviews increase pressure to submit CLs that are not as good as they could be, and discourage cleanups, refactorings, and further improvements to existing CLs.

Sources: https://google.github.io/eng-practices/review/reviewer/speed.html

## How Fast

[ref: #process-how-fast]

If you are not in the middle of a focused task, **do a code review shortly after it comes in.**

**One business day is the maximum time it should take to respond** to a code review request (i.e., first thing the next morning).

Following these guidelines means a typical CL gets multiple rounds of review (if needed) within a single day.

Sources: https://google.github.io/eng-practices/review/reviewer/speed.html

## Speed vs. Interruption

[ref: #process-interruption]

There is one time where personal velocity trumps team velocity. **If you are in the middle of a focused task, such as writing code, don't interrupt yourself to do a code review.** Research shows it takes a long time to get back into smooth flow after an interruption; interrupting yourself while coding is actually _more_ expensive to the team than making another developer wait a bit.

Instead, wait for a break point: completed coding task, after lunch, returning from a meeting, coming back from the breakroom, etc.

Sources: https://google.github.io/eng-practices/review/reviewer/speed.html

## Fast Responses

[ref: #process-fast-responses]

Review speed means _response_ time, as opposed to how long a CL takes to get through the whole review and be submitted. The whole process should ideally be fast, but **individual responses coming quickly matters even more than the whole process happening rapidly.**

Even when the full review _process_ takes long, quick responses throughout significantly ease the frustration developers feel with "slow" reviews.

Too busy for a full review right now? Still send a quick response: when you'll get to it, which other reviewers might respond more quickly, or some initial broad comments. (This doesn't mean interrupting coding even for such a response — send it at a reasonable break point.)

**Reviewers must spend enough time on review to be certain their LGTM means "this code meets the standard."** Individual responses should still ideally be fast.

Sources: https://google.github.io/eng-practices/review/reviewer/speed.html

## Cross-Time-Zone Reviews

[ref: #process-time-zones]

With time zone differences, try to get back to the author while they still have time to respond before the end of their working hours. If they've already finished for the day, make sure your review is done before they start work the next day.

Sources: https://google.github.io/eng-practices/review/reviewer/speed.html

## LGTM With Comments

[ref: #process-lgtm-with-comments]

To speed up code reviews, a reviewer should give LGTM/Approval even while leaving unresolved comments on the CL, when at least one of these applies:

- The reviewer is confident the developer will appropriately address all remaining comments.
- The comments don't _have_ to be addressed.
- The suggestions are minor: sort imports, fix a nearby typo, apply a suggested fix, remove an unused dependency, etc.

The reviewer should specify which of these options they intend, when not otherwise clear.

LGTM With Comments is especially worth considering when developer and reviewer are in different time zones — otherwise the developer waits a whole day just to get "LGTM, Approval."

Sources: https://google.github.io/eng-practices/review/reviewer/speed.html

## Large CLs

[ref: #process-large-cls]

If somebody sends a code review so large you're not sure when you'll have time to review it, the typical response is to ask the developer to split the CL into several smaller CLs that build on each other, instead of one huge CL reviewed all at once. This is usually possible and very helpful, even if it takes additional work from the developer.

If a CL _can't_ be broken up and you don't have time to review it quickly, at least write comments on the overall design and send it back for improvement. A goal of the reviewer is to always unblock the developer or enable them to take further action quickly, without sacrificing code health.

Sources: https://google.github.io/eng-practices/review/reviewer/speed.html

## Improvement Over Time

[ref: #process-improvements]

Following these guidelines with strict code reviews makes the entire process go faster and faster over time. Developers learn what healthy code requires and send CLs that are great from the start, needing less review time; reviewers learn to respond quickly without adding latency. But **don't compromise on the code review standards or quality for an imagined improvement in velocity** — it won't actually make anything happen more quickly, in the long run.

Sources: https://google.github.io/eng-practices/review/reviewer/speed.html
