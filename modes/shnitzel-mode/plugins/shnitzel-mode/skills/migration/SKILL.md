---
name: migration
description: Run a large migration across many call sites or repositories, converging on the target rather than preserving compatibility forever. Use for migration, move everything to, deprecate and replace, cutover, rewrite this across the codebase.
---

# Migration

A migration fails in one of two ways. It stalls half done and leaves two systems forever, or it goes big bang and breaks something nobody predicted. The design is about avoiding both at once.

## Steps

1. **Enumerate every call site.** Grep, then verify the grep, because dynamic dispatch and generated code hide from it. The count is the plan's denominator and an unknown denominator means an unknown end date.
2. **Name the end state exactly**, including what is deleted. A migration with no deletion is an addition, and it doubles the surface permanently.
3. **Decide the shape.** Strangler with both paths live and a flag, or migrate callers then delete in one wave. Traffic and rollback needs decide this, not preference. Both are legitimate, drifting between them is not.
4. **Build the lever.** A codemod or generator for the repetitive part. Hand editing eighty call sites produces eighty chances to be inconsistent, and the reviewer cannot check it.
5. **Sequence into verifiable units.** Each unit ends in a check that runs. Order so the sequence proves itself: the riskiest reversible step early, the irreversible step last and alone.
6. **Isolate parallel work.** One worktree per stream when several run at once. Shared mutable state between migration streams is the thing that turns a long migration into a stalled one.
7. **Track the count.** Sites migrated over sites total, in a ledger, updated as you go. This is the only honest progress number a migration has.
8. **Delete.** The migration is done when the old path is gone, not when the new path works. Book the deletion as its own step with its own date, or it will never happen.

## Stalling

A migration stuck above ten percent and below ninety is the worst state, because both systems are live and neither is trusted. If the count has not moved in two weeks, stop and decide: finish it, or revert and accept the old system. Do not leave it.

## Scope

Findings stay with the repository or call site they came from. A workaround one service needed is not a fact about the others.
