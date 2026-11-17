---
name: shnitzel-cost
description: Show measured token usage and estimated cost per Shnitzel feature and effort tier
disable-model-invocation: true
allowed-tools: Bash(python3:*)
---

Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/usage.py" report $ARGUMENTS` (the script is `scripts/usage.py` in this plugin's folder) and show its output exactly as printed, in a code block, with no commentary. Arguments: `--days N` (0 for all time), `--by feature,tier,model,playbook,subagent,session_id`, `--json`.
