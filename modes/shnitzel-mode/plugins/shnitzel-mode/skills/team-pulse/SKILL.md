---
name: team-pulse
description: Read how work is actually flowing through the team from real artifacts rather than from standup. Use for team pulse, how is the team doing, who is blocked, review latency, are we shipping.
---

# Team pulse

Standup tells you what people say. This tells you what the repositories say. Run both, and pay attention when they disagree.

## Signals worth reading

Review latency per person, from request to first review. This is the number that quietly decides whether a distributed team feels fast, and it is invisible in a standup.

Work in progress per person. More than two open pull requests usually means blocked, not productive.

Time to merge after approval. A large gap means the merge step is the bottleneck, which is a process problem and cheap to fix.

Reviewer concentration. If one person is on 70 percent of reviews, that is a bus factor and a burnout risk in the same number.

Pull requests with no reviewer for more than a day, split by whose timezone could have picked them up.

## Timezones are structural, not trivia

A team split across four countries shares few working hours. A review that waits eleven hours because it was raised at the end of one country's day is not a slow reviewer, it is a handoff pattern. Read `~/.agents/shnitzel/profile/people.md` before calling anyone slow, and separate wait caused by overlap from wait caused by attention.

## Reporting

Lead with what one decision from you would unblock. Then patterns, not individuals. Name a person only for a fact that helps them, never as a ranking.

Never turn this into a productivity score. Counting pull requests per engineer measures who splits their work, not who does more of it, and the moment the team suspects you are counting, they will optimise the count.

## Scope

Reads the digest and the people profile. Never reads a feature ledger, since individual features are not the subject here. See `shnitzel-mode/references/scoping.md`.
