---
name: pipeline-fix
description: Fix a red or flaky CI pipeline. Use for broken build, failing CI, flaky test, GitHub Actions failure, pipeline is red.
---

# Pipeline fix

## Steps

1. **Read the actual failure.** Fetch the run log and quote the first real error, not the last line. `gh run view --log-failed` where `gh` is available.
2. **Classify before fixing.** Genuine break, environment drift, flake, or an upstream dependency change. The fix differs completely and guessing wrong wastes a day.
3. **Reproduce locally where possible.** Same container image, same command, same env vars. If it only fails in CI, the difference between the two environments is the bug.
4. **Flake means quarantine plus a root cause task, never a blanket retry.** A retry that hides a race ships the race to production. Retries are allowed only with a linked issue naming the race.
5. **Fix the cause.** Pin the dependency, fix the shared state, fix the test, in that order of preference.
6. **Prove it.** Run the job green twice on the branch. One green run on a flaky job proves nothing.
7. **Encode the lesson.** If this failure mode can recur, add the lint, the version pin, or the check. A second instruction in prose is a missing check.

## Reply

The class of failure, the root cause in one sentence, the fix, the two green runs, and the check that stops it recurring.
