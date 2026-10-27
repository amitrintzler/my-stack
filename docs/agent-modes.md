# my-stack

A collection of **agent modes**. A mode is a self-contained set of instructions, playbooks and read-only collectors that layers on top of whichever agent runtime you already use, and encodes the things a general framework cannot know about you: your approval boundaries, your platforms, your recurring work, and what your team has already learned.

Each mode lives in its own subfolder under `modes/` and can be installed on its own. Take one, take none, or copy one and make it yours.

## Modes

| Mode | For | Status |
| --- | --- | --- |
| [`shnitzel-mode`](../modes/shnitzel-mode/) | Platform engineering and DevOps. Runtime-neutral routing, model roles instead of vendor names, 17 platform domain cards, a read-only watch harness, a feature lifecycle from PRD to retro, and scoped knowledge that cannot leak between projects. | v1.4.0, MIT |

Adding one is a folder and a pull request. See [CONTRIBUTING.md](../CONTRIBUTING.md).

## Install a mode

Everything is plain markdown and shell. There is no build step and no runtime to install.

```bash
git clone <this repo> && cd my-stack
brew install gh jq && gh auth login      # or your platform's equivalent
modes/shnitzel-mode/install.sh           # dry run, prints every planned change
modes/shnitzel-mode/install.sh --apply    # do it
```

The installer detects which runtimes you have (Claude Code, Codex, Gemini CLI, a local model with an `AGENTS.md`) and wires the mode into each one it finds. It is idempotent, it backs up any file before appending to it, and `--uninstall --apply` removes what it added.

For Claude Code you can also register the whole repository as a plugin marketplace, which makes every mode installable by name and gives you slash commands:

```
/plugin marketplace add /path/to/my-stack
/plugin install shnitzel-mode@my-stack
```

## What a mode is made of

The shape is deliberately boring so that a mode is readable by a human and by an agent.

```
modes/<name>/
├── README.md              what this mode is for
├── CAPABILITIES.md        every skill, every collector, the refusal list
├── install.sh             dry run by default, idempotent, uninstallable
├── bin/                   deterministic collectors, no mutating command in them
├── config/                example configuration, copied to ~/.agents on install
├── docs/                  design notes, adoption guide, honest review
├── schedules/             cron, launchd and scheduled task definitions
└── plugins/<name>/
    ├── skills/            the instructions themselves
    ├── commands/          one slash command stub per skill
    ├── agents/            subagent definitions
    └── hooks/             optional, and shipped inert
```

## Why modes rather than one big framework

Three reasons, learned by building the first one.

**Different people need different constraints.** A mode encodes approval boundaries and platform knowledge, and both are organisation-specific. A single framework that tried to satisfy everyone would be a framework with no opinions.

**Modes compose with upstream rather than replacing it.** `shnitzel-mode` sits on top of [pstack](https://github.com/michael-denyer/pstack-claude) and builds a pinned derived engine from the released cross-runtime port plus current original changes. Updates validate before activation; exact sources and adaptations are recorded in the mode lock.

**Deleting is cheap.** If a mode stops earning its place, remove the folder. Nothing else in the repository depends on it.

## Checks

```bash
scripts/check-all.sh
```

Runs each mode's own `bin/publish-check.sh`. That checks for absolute home directory paths, credential-shaped strings, email addresses, hardcoded vendor model slugs inside instruction files, skill frontmatter that disagrees with its directory, missing command stubs, shell syntax and JSON validity. CI runs the same script plus two behavioural checks: every collector must survive an empty config by emitting valid JSON rather than failing, and every installer dry run must write nothing.

## The article

[`article/index.html`](../article/index.html) is a written account of building the first mode, including the design decisions and the three defects a review found before a user did. Figures are in `article/images/`, and `article/social/` has the same figures rendered as square cards.

## Licence

MIT. See [LICENSE](../LICENSE).
