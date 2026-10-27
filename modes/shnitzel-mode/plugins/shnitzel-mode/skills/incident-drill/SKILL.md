---
name: incident-drill
description: Drive a live production incident. Use for production is down, we have an incident, sev1, users are affected, alert fired.
---

# Incident drill

Mitigate first. Understand second. Blame never.

## Steps

1. **Establish impact in one line.** Who is affected, since when, how badly. Timestamp everything in ISO 8601 UTC.
2. **Find the last change.** Deploy, config change, feature flag, certificate expiry, quota, upstream provider status. Most incidents are a change, and the change is usually recent.
3. **Mitigate before diagnosing.** Roll back, flip the flag, scale out, fail over. Mitigation is the owner's call to approve, so present the option with its own blast radius and wait.
4. **Keep a timeline as you go.** Every observation and action with its timestamp. Reconstructing it afterwards produces fiction.
5. **Verify recovery on the user-visible surface.** The metric recovering is not the same as the user being served.
6. **Root cause after recovery, not during.**
7. **Postmortem is blameless and structural.** The output is a change to a system, a check, or an alert. "Be more careful" is not an action item.

## Reply

Impact, timeline, mitigation applied and by whom, current state, root cause or the open question, and the structural fix.
