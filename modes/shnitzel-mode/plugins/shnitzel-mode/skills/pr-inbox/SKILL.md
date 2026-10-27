---
name: pr-inbox
description: Turn the watch digest into a ranked list of pull requests with a recommended first action for each. Use for pr inbox, what PRs need me, review queue, my open PRs, whose turn is it.
---

# PR inbox

The question behind every version of "check my PRs" is whose turn it is. Answer that first, per PR, then everything else.

## Turn holder

For each pull request, decide the holder from the digest, not from a feeling.

- Unresolved review thread addressed to you, or failing checks on your PR: **your turn**.
- Approved, green, no conflicts: **your turn**, and the only remaining action is a merge, which is yours to perform.
- Changes requested and you have pushed since: **their turn**, and it is worth a nudge if it has been over a day.
- Review requested from you: **your turn**, ranked by how long they have waited, not by how interesting the PR is.
- Draft with no activity: **nobody's turn**, and that is the finding. Revive it, split it, or close it.

## Recommended first action

Every item gets exactly one, concrete and small enough to start now. Not "look at PR 41". Rather "read the failing `unit` job on PR 41, it is one assertion" or "answer dana's thread about the retry hiding a race, she is right".

Where the action is a review you are being asked to give, say roughly how long it will take, from the diff size in the digest. A twelve line change and a four hundred line change are different decisions about your afternoon.

## Ordering

Order by whose turn plus how long they have waited. A colleague blocked for three days outranks your own PR that is merely idle. People before machines, because a machine waiting costs nothing.

## Never

Do not post, merge, close, request changes, or nudge anyone from inside this skill. Draft the comment, name the file, hand it over.
