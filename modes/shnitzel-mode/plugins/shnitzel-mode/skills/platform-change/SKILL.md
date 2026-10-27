---
name: platform-change
description: Playbook for any change that alters running infrastructure. Terraform, Kubernetes, Helm, CI workflows, cloud IAM, DNS. Use for infra change, terraform change, k8s rollout, helm upgrade, pipeline change.
---

# Platform change

Infrastructure changes are the ones where a bad diff costs an outage rather than a revert. The plan is the artifact under review, not the apply.

## Steps

1. **Blast radius first.** Name every environment, cluster, account, and consumer the change can reach. Write it down before reading the code. If you cannot enumerate it, that is the finding.
2. **Read the current state.** `terraform plan`, `kubectl get -o yaml`, `helm get values`, the live workflow file. Never design against the repo alone. Drift is normal.
3. **Name the rollback before the change.** A change with no rollback path is a change that needs a different design. Write the exact rollback command.
4. **Write the smallest diff.** No opportunistic refactors in an infra PR. They hide the real change from the reviewer.
5. **Dry run.** `terraform plan`, `kubectl diff`, `helm template` or `helm upgrade --dry-run`, `act` or a workflow branch run. Paste the real output into the PR body.
6. **Check lock-in.** Route to the **lock-in-check** skill if the change introduces a managed service, a provider-specific resource, or a vendor SDK.
7. **Stop.** Apply, deploy, and merge are always the owner's action. Present the plan output, the rollback command, and the blast radius, then wait.
8. **After apply, verify on the real surface.** The resource exists, the pod is ready, the endpoint answers, the alert cleared. A successful apply is not verification.

## Reply

Blast radius, the diff in one sentence, the dry run output location, the rollback command, and what is still unverified.
