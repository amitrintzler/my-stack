# Changelog

Per-mode changelogs live in each mode's folder. This file records changes to the repository itself.

## 2026-08-26

Restructured as a multi-mode repository. The kit that was a standalone tree is now `modes/shnitzel-mode/`, installable on its own or through the root marketplace file, which leaves room for a second mode without reshaping anything.

Added a root README aimed at someone arriving with no context, a contributing guide covering how to add a mode, `scripts/check-all.sh` to validate every mode with one command, and CI that runs it alongside two behavioural checks.

The article moved to `article/` with all nine figures rendered as images, plus square cards for sharing.
