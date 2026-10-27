---
name: access-review
description: Audit who and what can reach production, and what needs rotating. Use for access review, permissions audit, IAM review, who has access, token rotation, secrets audit, offboarding check.
---

# Access review

The two questions worth asking quarterly: who can reach production, and what could reach production if it leaked.

## What to enumerate

Human access, per environment, with the path they used to get it. Group membership counts, and it is where the surprises live.

Machine access: service accounts, CI tokens, deploy keys, webhooks. These outnumber humans, outlive the person who created them, and almost never get reviewed.

Age and last use for every credential. A token unused for six months is not in use, it is a liability with a login.

Repository level: who can merge to protected branches, who can bypass, who can edit workflow files. Workflow write access is production access in a trench coat, and it is routinely granted as if it were not.

Leavers. Anyone who left in the review window, and everything that was theirs. Check the machine credentials they created, not just their user.

## Report

Grouped by what you would do about it, not by system. Revoke now, rotate now, needs an owner, keep and document.

Every finding names the person or service and the specific grant. "Broad permissions in staging" is not actionable. "The `ci-deploy` service account has owner on the production project, created 2024-03, last used 2025-11" is.

Say which findings are structural, meaning the same gap will reappear next quarter unless something changes. Those are the only findings that make the next review shorter.

## Never

No revoking, no rotating, no membership changes. Locking someone out of production at the wrong moment is its own outage. This skill produces the list and the owner executes it, one item at a time.

Never write a credential, token or key into any file, ledger or report, including a partial one. Reference it by name and location only.
