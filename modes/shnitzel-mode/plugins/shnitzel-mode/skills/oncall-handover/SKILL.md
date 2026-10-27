---
name: oncall-handover
description: Hand the on-call shift across timezones so the next person starts informed instead of paging you. Use for oncall handover, shift handover, passing the pager, end of shift.
---

# On-call handover

The pager moves between timezones with little or no overlap. The next engineer starts cold, often with no chance to ask you anything. What you write is all they get.

## Write

`HANDOVER-YYYY-MM-DD-HHmm.md` in the on-call repo or runbook location, committed.

State the system's current condition in one line: normal, degraded and how, or actively broken. Then anything still open with what has been tried, and this matters more than what caused it. An incident half diagnosed is worse than an unknown one if the next person repeats the first three hours.

List what is suppressed or silenced and when it expires. A silenced alert nobody knows about is how a second outage happens inside the first one.

Name what is deploying or frozen, and any change window in the next twelve hours.

Flag alerts that fired and were noise, because the pattern matters even when each instance did not.

Finish with what you would watch if you were staying on. That single sentence is usually the most valuable thing in the document.

## Do not

Do not hand over a diagnosis you have not evidenced. Say what you observed and what you suspect, kept separate. A confident wrong theory costs the next shift more than no theory.

Do not leave state only in the chat thread. The next person may not have access to it, and they certainly will not read forty messages at 03:00.

## After the shift

Alerts that were noise go to the **slo-review** skill. Anything unresolved becomes a tracked item, not a memory. Anything that will recur becomes a runbook entry, since the third time you explain something in a handover it should have been written down twice ago.
