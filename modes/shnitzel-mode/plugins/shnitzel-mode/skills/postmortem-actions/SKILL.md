---
name: postmortem-actions
description: Track incident action items until they are actually done, and report the ones that have been open too long. Use for postmortem actions, incident follow ups, did we fix that, action item review, are we repeating incidents.
---

# Postmortem actions

The postmortem is not the output of an incident. The changed system is. Most organisations write good postmortems and close very few of the actions, and then hold the same incident again a year later.

## The ledger

Actions live in a tracked file, not in the postmortem prose. One line each: what, who, by when, current state, and the incident it came from.

An action with no owner is not an action. An action with no date is not an action. An action phrased as "be more careful" or "add more monitoring" is not an action either, because nobody can tell when it is finished. Rewrite it into a specific change, or drop it and say you dropped it.

## What to report

Open actions past their date, oldest first, with the incident and how long. Actions with no owner or no date, which are the ones quietly dying. Actions from incidents that have since recurred, which is the strongest possible argument for doing them. And the completion rate over the last quarter, because a rate under half means the postmortem process is theatre and that is worth knowing.

## Prevent the recurrence properly

For each action ask whether it prevents this incident or the class of incident. A fix for this exact failure is worth less than a check that catches the family. Where an action is instance specific, note what the class level version would be, even if you do not do it.

Close the loop the other way as well. When an incident recurs, find the action from last time and say what happened to it. Either it was never done, or it was done and did not work, and those lead to completely different conversations.

## Never

Never close an action on someone's behalf. Never quietly drop one. Dropping is a decision and it gets written down with a reason, which is what makes it different from forgetting.
