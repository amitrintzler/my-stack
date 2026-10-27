# HLD: <title>

Feature <id> · links to [PRD](01-prd.md)

## Shape of the data

The core types and how state is organised, before any logic. A state machine, a typed model, a table or registry, a boundary. Name it here and the implementation stops inventing three versions of it.

## Components and boundaries

What is added, what is changed, what is deleted. Where the trust boundary sits, where validation happens, what stays pure.

## Alternatives rejected

At least one, with the reason. A design with no rejected alternative was not designed, it was the first idea written down.

| Option | Why not |
| --- | --- |

## Failure modes

What breaks under load, partial failure, retry, or a bad deploy. What the rollback is.

## Vendor coupling

Run the **lock-in-check** skill. Record the depth class and the exit price here, even when the answer is none.

## Review

Who argued with this, when, and what changed as a result. A model panel counts, and so does one senior engineer. Both is better. An HLD with an empty review section has not passed its gate.

## Rough phases

Three to ten lines, one per intended phase. The real plan comes next, in `03-plan/`.
