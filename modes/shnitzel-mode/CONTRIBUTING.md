# Contributing

## Before you open a pull request

Run `bin/publish-check.sh`. It fails on absolute home directory paths, personal identifiers, anything shaped like a credential, and skills whose frontmatter name does not match their directory. CI runs the same check, so running it first saves a round trip.

## House rules for skills

A skill is prose that an agent follows, so it is judged as prose. Keep it under about 60 lines. Say what to do and why, not what the thing is. Every rule that matters carries the reason, because an agent that knows why a rule exists handles the case the rule did not anticipate.

Name the file's directory and the frontmatter `name` identically. Add a matching command stub in `commands/`.

Never write a vendor model slug into a skill. Use a role from `references/model-roles.md`. This is the single rule most likely to be broken by accident and it is what keeps the kit portable.

Never widen a rule's scope without a named second instance. See `references/scoping.md`.

The long dash character is banned throughout, in skills, docs and commit messages.

## Collectors

Collectors under `bin/` must be deterministic and read-only remotely. Update/install commands must require explicit apply mode and preserve owned state. If a change makes a collector write to GitHub, it belongs in a skill instead, within explicit interactive authorization.

Every collector emits the same item shape: `id`, `kind`, `severity`, `repo`, `title`, `url`, `fingerprint`, `detail`. Keep it that way so `digest.sh` can merge new collectors without changes.

## Testing

There is no test framework and it would be overkill for markdown and shell. What there is: `bash -n` on every script, the publish check, the frontmatter and command parity check, and fixtures. If you change a collector, exercise it against a fixture and say in the pull request what you observed.
