# Runtime primitives

Discover command execution, skill loading, user questions and independent subagent dispatch from the actual runtime's exposed tools. Use native equivalents instead of translating tool names by guesswork. A config directory does not prove which runtime is executing this session.

Claude Code uses its current Agent, command, skill and question tools. Codex resolves through its available spawn, shell, skill and input tools; the installed pstack Codex mapping supplies additional guidance but does not override the host's tool catalog. Gemini can expose skills, hooks and subagents; check rather than assuming absence. Cowork supports connected folders; verify folder access in the app. Local hosts vary, so state which host is actually tested.

Read the current runtime's pstack-models.md. Use only reachable models and accepted effort values. If a tool is missing, label the limitation once. An exploration pass may run sequentially; required independent review cannot be replaced with the author's own review. A hard-cap request without verified end-to-end enforcement stops before execution.

In a skills-only install, plugin-namespaced agent types are not registered. Use an actually available generic agent type and pass the exact pstack skill path in its brief. Load nested skills by their real files when there is no native skill invocation. A required reviewer must still be independent. Native plugin registration is optional and increases discoverable metadata; do not pretend it happened.
