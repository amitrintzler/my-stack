---
name: lock-in-check
description: Check an architecture or vendor decision for single-vendor lock-in and name the exit cost. Use for vendor decision, should we use managed X, cloud choice, lock-in, portability review.
---

# Lock-in check

This kit assumes several clouds on purpose. Lock-in is not forbidden, it is priced. This skill makes the price visible before the decision, not after.

## Steps

1. **Name the dependency precisely.** The specific managed service, provider resource, SDK, proprietary query language, or model vendor.
2. **Classify the depth.**
   - Shallow: swappable behind an interface in days. Object storage, managed Postgres, container runtime.
   - Structural: a rewrite of a component. Proprietary queue semantics, vendor IAM model, serverless runtime, vendor-specific data warehouse.
   - Absorbing: the data or the operating model moves in and does not come back out. Proprietary formats, egress-priced data lakes, vendor-specific orchestration.
3. **Price the exit.** Engineer-weeks to migrate, data egress cost, and the calendar time under dual-run.
4. **Name the portable alternative** and what it costs in speed or money to choose it now.
5. **Say the recommendation out loud** with the depth class and the exit price. A structural or absorbing dependency accepted knowingly is fine. One accepted silently is the failure.

## Reply

Dependency, depth class, exit price, portable alternative, recommendation. Five sentences is usually enough.
