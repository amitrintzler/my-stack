---
name: cost-review
description: Explain what changed in cloud spend and what to do about it, across whichever providers are in use. Use for cost review, cloud spend, why is the bill higher, cost optimisation, FinOps.
---

# Cost review

A bill is a design document written in arrears. Read it that way.

## Start from the delta

Total spend is background. The question is what changed since last month and why. Sort by absolute change, not by size, because a service that doubled from a small base is often the leading indicator, and a large flat line is not news.

Tie every material change to an event: a deploy, a traffic change, a retention policy, a new environment, a region added. A change with no known cause is the finding, and it is usually a leak: an environment nobody turned off, logs nobody set a retention on, a cluster that scaled up and never came back down.

## The usual four

Idle and forgotten resources, which is almost always the largest single win and the least interesting work. Data transfer, especially cross-region and cross-zone, which is invisible in architecture diagrams and very visible in the bill. Storage and log retention set once and never revisited. Overprovisioned capacity kept for a peak that has not happened in a year.

## Multi-cloud, deliberately

The owner runs several providers on purpose. Never recommend consolidating onto one to save money without pricing the lock-in that buys, so route the recommendation through the **lock-in-check** skill and state the depth class. A discount in exchange for a structural dependency is a trade, not a saving, and it should be made knowingly.

Compare providers on the workload, not on list price. Egress pricing and committed use discounts change the answer more than instance cost does.

## Output

Three to five actions ranked by monthly saving over effort, each with the number attached and who owns it. Then one paragraph on what will drift back within a quarter unless a check exists, because cost work that is not encoded as a check gets redone every year.

Never delete or resize anything. Produce the list.
