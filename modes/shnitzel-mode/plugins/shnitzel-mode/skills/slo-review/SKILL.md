---
name: slo-review
description: Review error budgets and alert quality, and decide what changes as a result. Use for SLO review, error budget, are our alerts any good, alert fatigue, reliability review.
---

# SLO review

Two questions. Is the service as reliable as we promised, and are the alerts telling us the truth.

## Error budget

For each SLO: the target, actual, budget consumed, and burn rate. Then the part that matters, which is what the number means for the next four weeks.

Budget exhausted means reliability work outranks feature work until it recovers. Say that plainly, because an error budget nobody acts on is a dashboard, not a policy.

Budget barely touched over two quarters is also a finding. The target is too loose, and a target that cannot be missed provides no signal and no permission to take risk.

## Alert quality

For every alert that fired: did a human act, and did it need a human. Those two answers put every alert into one of four boxes, and three of them are bugs.

Fired and acted on is the only healthy one. Fired and ignored means delete it or lower it. Fired but automation could have fixed it means write the automation. Did not fire when it should have is the expensive one, and it is found only by walking backwards from incidents.

Rank alerts by how often they fire without action. That list is your alert fatigue, measured rather than complained about.

## Alerts must be symptom based

Alert on what users experience, not on what a machine is doing. High CPU is not an incident. Requests failing is. Every cause based alert you delete makes the remaining ones more believable.

## Output

Budget status per SLO with the decision it implies, the alerts to delete or demote with their fire and action counts, the gaps found by walking back from incidents, and one target to retune with the reason.

Route anything that becomes work to the relevant playbook. Changing an alert is a **platform-change**.
