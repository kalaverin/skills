---
subject: "Pushback handling and emergency exceptions per Google eng-practices; developer disagreement evaluation, politeness under insistence, cleanup-later refusal, strictness complaints fade with speed, conflict consensus ladder, emergency definition, small emergency CL scope, non-emergency list, hard deadline criteria, post-emergency thorough review."
index:
  - anchor: conflicts-who-is-right
    what: "Who-is-right procedure: first consider that the developer may be correct (they are closer to the code); if the suggestion still improves code health, keep advocating politely with explanations that show the reply was heard."
    problem: "Agent judges reviewer persistence during disagreement; dropping valid points at first resistance degrades health, stubborn wrong insistence wastes trust; disagreement evaluation, developer rightness, polite insistence, small steps, advocacy persistence, hearing versus agreeing, explanation rounds."
    use_when: "Reviewer dropped valid point after pushback; reviewer insisted without engaging author's argument."
    avoid_when: "General escalation ladders (principles-resolving-conflicts); comment tone only (comments.md)."
    expected: "Verdict states whether persistence matched code-health justification and stayed polite."
  - anchor: conflicts-upsetting
    what: "The upsetting-developers finding: insistence rarely actually upsets developers when comments stay polite; upsets trace to how comments are written, not to insisting on quality."
    problem: "Agent weighs reviewer fear of upsetting author; anticipated offense dilutes legitimate demands without evidence; politeness shield, insistence anxiety, quality demands, gratitude later, imagined conflict, tone versus substance, appeasement instinct, withdrawal risk, groundless worry."
    use_when: "Reviewer softened or withdrew demands citing author's feelings; assessing whether fear was grounded."
    avoid_when: "Actually rude comments (comments-courtesy); emergency pressure (conflicts-emergency-definition)."
    expected: "Verdict separates wording-caused friction from insistence-caused friction."
  - anchor: conflicts-cleanup-later
    what: "The cleanup-later rule: refuse 'I will clean it up later' — later cleanups almost never happen; new complexity must be cleaned before submission; exposed surrounding problems get a filed bug assigned to the author plus an optional TODO."
    problem: "Agent assesses deferred-cleanup bargains in review; approved-with-promises complexity rots in codebase forever; cleanup promise, deferred work, rotting complexity, bug filing, assigned follow-up, TODO reference, submission gate, forgotten fixes, debt accumulation, broken promise, tracking discipline."
    use_when: "CL approved on promise of later fix; new complexity present at submission; reviewer let debt in."
    avoid_when: "Pre-existing surrounding problems (bug + TODO path applies); genuine emergencies (conflicts-emergency-definition)."
    expected: "Verdict records whether cleanup happened before submission or was properly tracked."
  - anchor: conflicts-strictness-complaints
    what: "The strictness-complaints finding: developers complain loudly when lax reviews become strict; faster reviews make complaints fade over months until value becomes visible."
    problem: "Agent evaluates complaints about newly strict reviewer; volume of complaint misread as evidence of reviewer wrongness; strictness transition, loud complaints, fading period, speed remedy, value recognition, process maturity, protest interpretation, adaptation period, reform resistance."
    use_when: "Author complains reviewer is too strict; team transitioned from lax to strict reviews."
    avoid_when: "Concrete incorrect demands (conflicts-who-is-right); genuinely slow reviews (process.md)."
    expected: "Verdict distinguishes strictness complaints from correctness complaints."
  - anchor: conflicts-emergency-definition
    what: "Emergency definition: a small CL that unblocks a major launch, fixes a production bug significantly affecting users, handles a pressing legal issue, or closes a major security hole — reviewed for speed and correctness above all, then re-reviewed thoroughly afterwards."
    problem: "Agent classifies claimed urgency in review; everyday pressure wears emergency costume to skip standards; urgency classification, production outage, legal pressure, launch blocker, small change scope, correctness focus, post-hoc review, outage scope, urgent correctness, launch rescue."
    use_when: "Review was rushed citing emergency; assessing whether situation qualified under the standard."
    avoid_when: "Normal speed assessment (process.md); routine deadline pressure (conflicts-non-emergency)."
    expected: "Verdict states whether the emergency claim matched the qualifying categories."
  - anchor: conflicts-non-emergency
    what: "The non-emergency list: wanting to launch this week, long feature work, reviewer timezones, Friday evening, manager's soft deadline, and rollback of test-failing CLs are explicitly NOT emergencies."
    problem: "Agent deflates false urgency claims in review; soft deadlines and calendar pressure masquerade as emergencies to bypass quality gates; friday merge, timezone wait, rollback case, launch preference, convenience claim, bypass attempt, review shortcut, weekend rush, manager word, habit stack."
    use_when: "Emergency claim rests on schedule preference or convenience; manager pressure without hard deadline."
    avoid_when: "Real production outages or security holes (conflicts-emergency-definition); hard contractual dates (conflicts-hard-deadline)."
    expected: "Verdict names which non-emergency category the claim falls into."
  - anchor: conflicts-hard-deadline
    what: "Hard deadline criteria: a deadline is hard only when missing it is disastrous — contractual obligation, total marketplace failure, once-a-year hardware windows; most deadlines are soft and never justify sacrificing code health."
    problem: "Agent weighs deadline claims behind rushed review; ordinary milestones inflated into disasters to justify shallow approval; disaster criterion, market failure, soft milestone, release cycle, technical debt spiral, catastrophe test, partner agreement, annual shipment, health sacrifice."
    use_when: "Deadline invoked to justify skipping review quality; assessing whether claimed deadline was hard."
    avoid_when: "Immediate production emergencies (conflicts-emergency-definition); non-deadline pressure (conflicts-non-emergency)."
    expected: "Verdict classifies the deadline as hard or soft with the disaster test."
---

# Conflicts and Emergencies

The verbatim standard of `pushback.html` and `emergencies.html`: handling disagreement and defining true emergencies.

## Who Is Right

[ref: #conflicts-who-is-right]

Sometimes a developer will push back on a code review: either they will disagree with your suggestion, or they will complain that you are being too strict in general.

When a developer disagrees with your suggestion, first take a moment to consider whether they are correct. Often they are closer to the code than you are, and might really have better insight about certain aspects of it. Does their argument make sense from a code health perspective? If so, let them know they are right and let the issue drop.

However, developers are not always right. In this case the reviewer should further explain why they believe their suggestion is correct. A good explanation demonstrates both an understanding of the developer's reply and additional information about why the change is being requested.

In particular, when the reviewer believes their suggestion will improve code health, they should continue to advocate for the change, if they believe the resulting code quality improvement justifies the additional work requested. **Improving code health tends to happen in small steps.**

Sometimes it takes a few rounds of explaining a suggestion before it really sinks in. Just make sure to always stay polite and let the developer know that you _hear_ what they're saying, you just don't _agree_.

Sources: https://google.github.io/eng-practices/review/reviewer/pushback.html

## Upsetting Developers

[ref: #conflicts-upsetting]

Reviewers sometimes believe the developer will be upset if the reviewer insists on an improvement. Sometimes developers do become upset, but it is usually brief, and they become very thankful later that you helped them improve the quality of their code. Usually, if you are polite in your comments, developers actually don't become upset at all, and the worry is just in the reviewer's mind. Upsets are usually more about the way comments are written than about the reviewer's insistence on code quality.

Sources: https://google.github.io/eng-practices/review/reviewer/pushback.html

## Cleaning It Up Later

[ref: #conflicts-cleanup-later]

A common source of pushback is that developers (understandably) want to get things done. They don't want another round of review just to get this CL in. So they say they will clean something up in a later CL, and thus you should LGTM _this_ CL now. Some developers are very good about this and will immediately write a follow-up CL. However, experience shows that as more time passes after the developer writes the original CL, the less likely this clean up is to happen. In fact, usually unless the developer does the clean up _immediately_ after the present CL, it never happens. This isn't because developers are irresponsible, but because they have a lot of work to do and the cleanup gets lost or forgotten in the press of other work. Thus, it is usually best to insist that the developer clean up their CL _now_, before the code is in the codebase and "done." Letting people "clean things up later" is a common way for codebases to degenerate.

If a CL introduces new complexity, it must be cleaned up before submission unless it is an emergency. If the CL exposes surrounding problems and they can't be addressed right now, the developer should file a bug for the cleanup and assign it to themselves so that it doesn't get lost. They can optionally also write a TODO comment in the code that references the filed bug.

Sources: https://google.github.io/eng-practices/review/reviewer/pushback.html

## General Complaints About Strictness

[ref: #conflicts-strictness-complaints]

If you previously had fairly lax code reviews and you switch to having strict reviews, some developers will complain very loudly. Improving the speed of your code reviews usually causes these complaints to fade away.

Sometimes it takes months for these complaints to fade, but eventually developers tend to see the value of strict code reviews as they see what great code they help generate. Sometimes the loudest protesters even become your strongest supporters once something happens that causes them to really see the value you're adding by being strict.

Sources: https://google.github.io/eng-practices/review/reviewer/pushback.html

## What Is an Emergency

[ref: #conflicts-emergency-definition]

An emergency CL is a **small** change that: allows a major launch to continue instead of rolling back, fixes a bug significantly affecting users in production, handles a pressing legal issue, closes a major security hole, etc.

In emergencies we really do care about the speed of the entire code review process, not just the speed of response. In this case _only_, the reviewer should care more about the speed of the review and the correctness of the code (does it actually resolve the emergency?) than anything else. Also, such reviews take priority over all other code reviews when they come up.

However, after the emergency is resolved, look over the emergency CLs again and give them a more thorough review.

The speed standard adds: in an emergency, CLs must pass through the _whole_ review process very quickly, and the quality guidelines would be relaxed — but only for situations that actually qualify as emergencies (see the non-emergency list below).

Sources: https://google.github.io/eng-practices/review/emergencies.html, https://google.github.io/eng-practices/review/reviewer/speed.html

## What Is NOT an Emergency

[ref: #conflicts-non-emergency]

To be clear, the following cases are _not_ an emergency:

- Wanting to launch this week rather than next week (unless there is an actual hard deadline for launch such as a partner agreement).
- The developer has worked on a feature for a very long time and really wants to get the CL in.
- The reviewers are all in another timezone where it is currently nighttime, or they are away on an off-site.
- It is the end of the day on Friday and it would be great to get this CL in before the developer leaves for the weekend.
- A manager says this review has to be complete and the CL checked in today because of a soft (not hard) deadline.
- Rolling back a CL that is causing test failures or build breakages.

Sources: https://google.github.io/eng-practices/review/emergencies.html

## What Is a Hard Deadline

[ref: #conflicts-hard-deadline]

A hard deadline is one where **something disastrous would happen** if you miss it. For example:

- Submitting your CL by a certain date is necessary for a contractual obligation.
- Your product will completely fail in the marketplace if not released by a certain date.
- Some hardware manufacturers only ship new hardware once a year; missing the deadline to submit code to them could be disastrous, depending on what type of code you're trying to ship.

Delaying a release for a week is not disastrous. Missing an important conference might be disastrous, but often is not.

Most deadlines are soft deadlines, not hard deadlines. They represent a desire for a feature to be done by a certain time. They are important, but you shouldn't sacrifice code health to make them.

With a long release cycle (several weeks) it can be tempting to sacrifice code review quality to get a feature in before the next cycle. This pattern, repeated, is a common way for projects to build up overwhelming technical debt. If developers routinely submit CLs near the end of the cycle that "must get in" with only superficial review, the team should modify its process so that large feature changes happen early in the cycle with enough time for good review.

Sources: https://google.github.io/eng-practices/review/emergencies.html
