# Hooks

`hooks.json.disabled` is shipped inert on purpose.

Enabling it injects roughly 90 tokens of routing mandate into every session start, and routes every non-trivial task through `shnitzel-mode` automatically. That is convenient and it also fires on tasks that did not need it, which costs tokens and slows small work.

Enable it with `mv hooks.json.disabled hooks.json` once you have used the mode by hand for a week and know you want it always on. Disable it by renaming back. Claude Code has no per-hook disable switch, so renaming the file is the mechanism.

Hooks are a Claude Code feature. Codex, Gemini CLI, and local runtimes ignore this directory entirely, which is why the routing mandate is duplicated in the always-on rules file that `install.sh` writes for those runtimes.
