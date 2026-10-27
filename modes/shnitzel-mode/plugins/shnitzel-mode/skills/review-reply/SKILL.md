---
name: review-reply
description: Draft answers to unresolved review threads on your pull requests. Drafts only, never posts. Use for answer PR comments, respond to review, reply to comments on my PR.
---

# Review reply

The digest reports unresolved review threads with the first comment of each. This skill decides what each one deserves and drafts it.

## Triage before drafting

Three outcomes, and the split matters more than the wording.

**Right.** The reviewer found a real problem. The reply is short, agrees, and names the fix. Then actually make the fix on the branch. A reply that promises a change and leaves the branch untouched is worse than no reply.

**Wrong, and you can show it.** Disagree with the evidence. Name the line, the test, or the run that settles it. Do not soften a correct position into a question. Candor over agreement, and no is an acceptable answer.

**Ambiguous.** Ask one specific question. Not "can you clarify", rather "do you mean the timeout on the client or the one in the ingress".

An automated review bot gets the same triage and more scepticism. Bots find real bugs and also file confident nonsense. Dismiss a non-issue with a concrete reason. Never churn code to satisfy a bot.

## Drafting

One thread, one draft. House style applies, so short declarative sentences, no long dash, no mid-sentence colon. Reply in the owner's voice: direct, technical, no hedging, no thanks-for-the-great-catch padding.

Write drafts to `.watch-drafts/pr-<number>-thread-<n>.md`, each with the thread URL at the top so posting is copy and paste. Add `.watch-drafts/` to the repo's ignore file if it is not there.

## Never post

Posting a comment is a message that leaves the machine and reaches a colleague. This skill drafts only. Posting requires an explicit user instruction authorizing that message; correctness alone is not authorization. Scheduled runs never post.
