# Hooks

`hooks.json.disabled` is shipped inert on purpose.

Enabling it injects roughly 135 tokens of routing mandate into every session start, resume, clear and compact, and routes every non-trivial task through `shnitzel-mode` automatically. That is convenient and it also fires on tasks that did not need it, which costs tokens and slows small work.

Enable it with `mv hooks.json.disabled hooks.json` once you have used the mode by hand for a week and know you want it always on. Disable it by renaming back. Claude Code has no per-hook disable switch, so renaming the file is the mechanism.

When pstack's own SessionStart hook is installed too, both run side by side as separate plugin hooks. Claude Code shows pstack's as `Loading pstack routing` and this one as `Loading Shnitzel routing`. The injected text says that Shnitzel admission comes first, so pstack's mandate to route multi-file work through `pstack:poteto-mode` applies only when the Shnitzel router selects it or the user names poteto-mode. To drop pstack's injection entirely, set `session hook: off` in pstack's model sheet.

Hooks are a Claude Code feature. Codex, Gemini CLI, and local runtimes ignore this directory entirely, which is why the routing mandate is duplicated in the always-on rules file that `install.sh` writes for those runtimes.
