---
name: dep-sweep
description: Upgrade a dependency or runtime across many repositories as one coordinated sweep with verification at each step. Use for dependency upgrade, bump version across repos, patch everything, node upgrade, base image bump, CVE remediation.
---

# Dependency sweep

The same change in fifteen repositories is not fifteen tasks. It is one task with fifteen verifications, and the difference is whether you build the tool or do it by hand.

## Steps

1. **Inventory first.** Which repositories actually use it, at which versions, direct or transitive. Write the list down before changing anything. The list is what tells you the sweep is finished.
2. **Read the change.** Breaking changes, deprecations, the migration guide. One repository will hit the sharp edge and it is cheaper to know which edge exists.
3. **Pick the pilot.** The repository with the best test coverage and the lowest blast radius. Do it fully there, including the verification, before touching a second one.
4. **Build the lever.** The pilot tells you the shape of the change. Write the codemod, script or generator rather than repeating the edit. The tool is the artifact a reviewer reruns, and it is also what makes the sweep auditable.
5. **Fan out with isolation.** One worktree per repository so parallel work cannot collide. Each gets its own branch and its own pull request. A single pull request across repositories is not reviewable.
6. **Verify per repository.** Build and tests green in each, on its own terms. A sweep is only as done as its least verified repository.
7. **Track it.** A checklist with a line per repository, in a ledger, not in your head. A sweep abandoned at eleven of fifteen leaves the worst possible state, which is inconsistency nobody has written down.

## Stop points

Merging is yours, per repository. A sweep does not earn bulk approval, and the fifth repository is exactly where a surprise appears.

If more than one repository fails in the same way, stop the sweep. That is a signal about the upgrade, not about those repositories, and pushing through means fixing the same thing fifteen times.

## Scope

Each repository's findings stay with that repository. A workaround needed in one is not a fact about the others, and copying it forward is how a sweep spreads a hack.
