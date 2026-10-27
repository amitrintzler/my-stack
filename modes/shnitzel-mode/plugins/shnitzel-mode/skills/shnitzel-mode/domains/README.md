# Domain cards

A playbook says what to do. A domain card says what that means here.

`platform-change` does not know whether "dry run" is `terraform plan`, `helm template`, `oc adm upgrade --dry-run` or `argocd app diff`. The card supplies that. The playbook stays vendor-neutral, which is what keeps the kit portable, and the card carries the specifics, which is what makes it useful.

## Every card has the same six sections

**Read only.** Commands that observe and change nothing. Collectors and skills may run these without asking.

**Signals.** What is worth watching, and the severity each maps to in the digest.

**Dry run.** How to see the change before making it. A platform with no dry run is a finding in itself.

**Rollback.** The exact command. Named before the change, not after.

**Never without approval.** Additions to the always-stop list, specific to this platform.

**Failure modes.** The things that actually go wrong, so time is not spent rediscovering them.

Cards also note the lock-in class, which feeds `lock-in-check`.

## Adding one

Copy `_template.md`, fill the six sections, and add a probe to `bin/domain-scan.sh` if it has a read-only health check worth running on a schedule. A card with no probe is still useful, it just does not appear in the digest.

Keep a card under about 40 lines. It is a reference consulted mid-task, not documentation.

## What is here

GitOps and clusters: `argocd`, `kubernetes`, `openshift`, `helm`.
Infrastructure: `terraform`, `vault`.
CI: `github-actions`, `jenkins`, `gitlab-ci`.
Registries: `nexus`, `artifactory`, `container-registries`.
Clouds: `aws`, `azure`, `gcp`, `oracle-cloud`.
Signals: `observability`.

A note on the abbreviation OCI, since it means two different things in this trade. `oracle-cloud.md` is Oracle Cloud Infrastructure. The OCI image and distribution specification is covered in `container-registries.md`. Getting these confused in a design document is common and expensive.
