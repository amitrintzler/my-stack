# Publishing Shnitzel

How to release a version that other people can install, and how to list it in the public directories. The marketplace files already exist: `.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json` at the repository root list this plugin under the marketplace name `my-stack`.

## Every release

1. Bump `version` in the plugin's `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`, in all four marketplace files, in `docs/agent-modes.md`, and add a CHANGELOG entry. Claude Code keeps users on the old copy when the version does not change.
2. Run the checks locally:

   ```bash
   bash scripts/check-all.sh
   python3 -m unittest discover -s modes/shnitzel-mode/tests
   claude plugin validate --strict ./modes/shnitzel-mode/plugins/shnitzel-mode
   claude plugin validate .
   ```

3. Merge to main, then tag the release from the plugin folder. The bootstrap fetches exactly this tag, so a version without its tag cannot be set up from a marketplace install.

   ```bash
   cd modes/shnitzel-mode/plugins/shnitzel-mode
   claude plugin tag --push      # creates shnitzel-mode--v<version>
   ```

4. Install it the way a stranger would, on a machine with no checkout:

   ```bash
   claude plugin marketplace add amitrintzler/my-stack
   claude plugin install shnitzel-mode@my-stack
   ```

   Run `/setup-shnitzel-mode`, confirm the bootstrap reports `fetched`, the engine builds, and `bin/doctor.py` finds it.

## Before the first public listing

- Add a square PNG icon, 512 to 2048 px, at the plugin's `.claude-plugin/icon.png`. The directory takes the icon once, at first submission, so choose it before submitting.
- Tell Lauren Tan and Michael Denyer before listing widely. Shnitzel turns off pstack's automatic session hook, and their users will meet that behavior.
- Keep the description an overlay on pstack, never official pstack. NOTICE.md carries the attribution and must ship unchanged.
- Decide whether the marketplace should stay in this repository. Its root README is a personal tech radar, which is what a directory reviewer and every new user see first. A dedicated repository would also let the marketplace name match the plugin.

## Directories

- Anthropic: submit from the developer portal at claude.ai/directory/manage. It needs a paid claude.ai plan and reviews every version. A listing also reaches claude.ai and Cowork, where only some plugin components load; Shnitzel's scripts and managed instruction block work in Claude Code. The official marketplace takes no open submissions.
- OpenAI: the plugin submission portal publishes to the directory shared by ChatGPT and Codex. Plugins with lifecycle hooks are not eligible, so keep `hooks/hooks.json.disabled` disabled.
- Cursor: cursor.directory is the community route. Confirm the current official route before submitting, because Cursor has changed it.
