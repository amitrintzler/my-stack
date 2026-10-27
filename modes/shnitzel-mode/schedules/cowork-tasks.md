# Cowork scheduled tasks

Create these with the scheduled task tools in Cowork. Each firing is a fresh session with no memory of the last one, so every prompt below is self contained. Crons are UTC.

Cowork's minimum interval is hourly, which is why nothing here fires every thirty minutes. If you want a tighter loop, run it locally with launchd instead.

---

## 1. Interrupt watch

**Cron:** `0 6-16 * * 0-4`  (hourly, 09:00 to 19:00 Asia/Jerusalem, Sunday to Thursday)

**Prompt:**

> Run the shnitzel-mode watch harness in interrupt mode. Load `plugins/shnitzel-mode/skills/watch/SKILL.md` from the connected Shnitzel distribution. Run `bin/gh-collect.sh` from the shnitzel-mode kit in the connected Shnitzel distribution. Report only items at severity 1 and 2. If there are none, reply with a single line saying so and nothing else. Do not post, push, merge, or re-run anything. For a red default branch, name how long it has been red and the last green commit. For a failing pull request of mine, read the failing job log and say in one sentence what broke. Nobody is watching this run, so do not ask a question at the end.

---

## 2. Morning brief

**Cron:** `0 5 * * 0-4`  (08:00 Asia/Jerusalem, Sunday to Thursday)

**Prompt:**

> Run the shnitzel-mode watch harness in daily brief mode. Follow the `watch` skill and run `bin/gh-collect.sh --all` from the connected Shnitzel distribution. Produce the full ranked report: what is on fire, what is waiting on me, whose turn each pull request is, and one concrete first action per item at severity 3 or above. Then follow the `pr-inbox` skill for the ordering. Draft replies for any unresolved review threads using the `review-reply` skill and write them to `.watch-drafts/`, but post nothing. End with the three closing items: what was done, files written, and the logical next step. This run is unattended, so make reasonable choices and state them rather than asking.

---

## 3. Weekly hygiene

**Cron:** `0 5 * * 0`  (08:00 Asia/Jerusalem, Sunday)

**Prompt:**

> Run the shnitzel-mode weekly hygiene pass. Follow the `watch` skill and run `bin/gh-collect.sh --all` from the connected Shnitzel distribution. Report only the slow decay: pull requests of mine idle beyond the stale threshold, open high and critical security advisories, and any `cowork/*` branch with no open pull request. For each stale pull request recommend one of revive, split, or close, with a reason. For the security advisories group by package and say which are transitive. Do not open, close, or comment on anything. Unattended run, no questions.

---

## 4. Handoff sweep, optional

**Cron:** `0 15 * * 0-4`  (18:00 Asia/Jerusalem, Sunday to Thursday)

**Prompt:**

> Check `cowork-workspace` and any repo I worked in today for uncommitted work and for in-flight tasks with no handoff file. If you find work that would be hard to resume tomorrow, follow the `handoff` skill and write the handoff file, then commit it on the working branch only. Do not push. If everything is clean, reply with one line saying so.

---

## 5. Weekly tune

**Cron:** `0 6 * * 0`  (09:00 Asia/Jerusalem, Sunday, after the hygiene pass)

**Prompt:**

> Run the shnitzel-mode tune pass. Follow the `tune` skill. Read `~/.agents/shnitzel/metrics.jsonl` and `open-ages.json`, and `~/.agents/shnitzel/lessons.md`. Report which finding kinds have a mean open age over thirty days, since those are the ones I have already decided not to act on, and propose a concrete diff to `~/.agents/watch.conf` with the measurement behind each line. Promote any lesson restated three times into a skill or a check and say where it went. Do not apply the diff, show it and stop. If there are fewer than four weeks of metrics, say the sample is thin and report the numbers without proposing changes.

---

## Notes

Scheduled tasks currently do not surface on mobile. Push notification and email delivery are per task settings, so turn push on for the interrupt watch and leave it off for the weekly, otherwise the weekly trains you to ignore the notification that matters.
