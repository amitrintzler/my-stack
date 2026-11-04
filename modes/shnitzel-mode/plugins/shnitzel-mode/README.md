# shnitzel-mode

An effort-aware overlay around a current, pinned pstack engine. Ordinary questions get direct answers. Engineering requests get brief approach choices, then the smallest workflow that meets the acceptance criteria. Explicit `/poteto-mode` still runs the full upstream pstack workflow.

## Install

Claude Code:

```bash
claude plugin marketplace add amitrintzler/my-stack
claude plugin install shnitzel-mode@my-stack
```

Codex:

```bash
codex plugin marketplace add amitrintzler/my-stack
```

Then run `/setup-shnitzel-mode` once in each runtime. A marketplace install copies only this plugin folder, so setup first runs `scripts/bootstrap.sh`, which fetches the matching tagged release of the distribution into `~/.agents/shnitzel/dist`. Setup then builds the locked pstack engine and shows the installer's dry run before it changes `CLAUDE.md` or `AGENTS.md`. Nothing is written without your go-ahead.

Requires Python 3 and Git, plus Node and Bun to build the engine.

## Credits

pstack and poteto-mode are Lauren Tan's work, published in cursor/plugins under MIT. The cross-runtime port is michael-denyer/pstack-claude. Shnitzel is an independent overlay, not an official pstack release, and it switches off pstack's automatic session hook so that its own admission rules decide when pstack runs. See the distribution's NOTICE.md for attribution.
