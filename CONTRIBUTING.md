# Contributing

## Adding a mode

A mode is a folder under `modes/`. Copy an existing one, delete what does not apply, and keep the structure, because the structure is what makes a mode readable by someone who has never seen it.

Minimum for a mode to be accepted:

- `README.md` saying who it is for and what it refuses to do.
- `bin/publish-check.sh`, so `scripts/check-all.sh` can validate it. Copy the existing one; it is generic.
- `install.sh` that is dry run by default, idempotent, and supports `--uninstall`.
- An entry in the root `.claude-plugin/marketplace.json` and in the mode guide at `docs/agent-modes.md`, linked from the root `README.md`.

## House rules for instruction files

An instruction file is prose that an agent follows, so it is judged as prose. Keep it under about 60 lines. Say what to do and why, not what the thing is. Every rule that matters carries its reason, because an agent that knows why a rule exists handles the case the rule did not anticipate.

Name the directory and the frontmatter `name` identically, and add a matching command stub.

**Never write a vendor model name into an instruction file.** Use a role. This is the rule most often broken by accident and it is what keeps a mode portable across runtimes.

**Never widen a rule's scope without a named second instance.** Knowledge earns its way up from project, to repository, to global.

The long dash character is banned throughout, in instructions, docs and commit messages.

## Collectors

Anything under `bin/` must be deterministic, read-only, and runnable with no model attached. If a change would make a collector write to a remote system, it belongs in an instruction file instead, behind that mode's approval list.

Every collector emits the same item shape: `id`, `kind`, `severity`, `repo`, `title`, `url`, `fingerprint`, `detail`. Keep it that way so a digest can merge new collectors without changes.

**Absence of data must never be representable as a value.** If a probe cannot answer, it says so. A missing field must not become zero, an unparseable date must not become a very old date, and a missing binary must not become an empty string. All three of those shipped in the first mode and all three were silent.

## Testing

Run `python3 -m unittest discover -s modes/shnitzel-mode/tests -v` for installer, budget and collector behavior contracts. Additional checks: `bash -n` on every script, the publish check, frontmatter and command parity, and fixtures. If you change a collector, exercise it against a fixture and say in the pull request what you observed.
