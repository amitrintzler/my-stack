# Schedules

Three ways to fire the harness. Same collector underneath, so the reports are identical whichever one runs.

All local times are Asia/Jerusalem. Every scheduler below takes UTC, so the crons are pre-converted at UTC+3, which is summer time. Israel moves to UTC+2 in late October, and these will drift one hour later in local terms until you shift them. Set a reminder rather than discovering it in November.

The work week is Sunday to Thursday, so the day-of-week fields read `0-4`, not `1-5`.

## 1. Cowork scheduled tasks, for the unattended runs

The right home for anything that must fire while the laptop is shut. Each firing starts a fresh cloud session, so the prompt has to stand alone. Definitions are in `cowork-tasks.md`, ready to paste.

## 2. launchd, for the local machine

`launchd/com.shnitzel.watch.daily.plist` runs the collector on your Mac and writes the digest to a file. No model attached, so it costs nothing and leaves a JSON file for whichever session you open next. Install with `launchctl load`. See the header in the plist.

## 3. Continuous, while you work

Not a schedule. After you push, tail the run until it settles, then stop. `pstack:babysit` does this well if pstack is installed. Otherwise:

```bash
gh run watch "$(gh run list --branch "$(git branch --show-current)" --limit 1 --json databaseId --jq '.[0].databaseId')"
```

Bounded by the run finishing. Never leave an unbounded poll running.

## What each one must not do

Scheduled runs remain read-only even when an interactive session has write authorization. It reports, it drafts, it stops. If a scheduled task ever posts a comment or pushes a branch, the harness has failed, whatever the report says.
