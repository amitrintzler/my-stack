# Upstream updates

Run `bin/upstream-check.sh --check` to compare current releases and the tracked lock. No update runs as a side effect of a normal task.

`--build` downloads immutable source snapshots into the user cache, builds a separate candidate and validates it. `--apply` additionally activates the validated candidate and records `config/upstream-lock.json`. `--locked --build` rebuilds the recorded source revisions. `--rollback` switches back to the previous engine. Install/update needs Python 3, Git, Node/npm, and Bun for the port's generator. No upstream scripts run in the Cowork repository.

The source snapshots remain pristine. A candidate starts from the released cross-runtime port. The updater uses that port's substitution rules, three-way merge and fork registry to apply changes from original pstack's recorded pin through the latest original revision. The manifest lists included files and exclusions with the port's reasons. Original docs and runtime-only assets are retained in the source cache rather than blindly installed as executable skills.

Conflicts, undeclared forks, denylist violations, broken links or generator errors prevent activation. A failed candidate remains for inspection; the previous engine is untouched. Exact-base-hash resolution patches can be registered in `patches/upstream/resolutions.json`. They apply only to their recorded original revision and expected input, and must carry a replacement checksum. When the port incorporates a patch, its resolved input no longer needs it; remove the stale patch rather than applying it blindly.

Shnitzel's effort and authorization policy is separate from original-content patches. The managed entry instruction routes focused work without loading pstack's full router. Explicit poteto-mode retains the complete upstream behavior. Project playbook changes must pass the installed engine's check-playbooks validator. Updating a source does not establish live runtime compatibility; acceptance is a separate step.
