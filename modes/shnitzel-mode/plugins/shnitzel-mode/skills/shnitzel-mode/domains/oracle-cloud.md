# Oracle Cloud Infrastructure

Oracle's cloud. Note that OCI is also the Open Container Initiative, which is a different thing covered in `container-registries.md`. Say which one you mean in writing, every time.

**Lock-in class.** Autonomous Database and Exadata are absorbing, since neither the engine nor the operational model exists anywhere else. Compute, Object Storage and OKE are shallow. The compartment model is structural, because every policy and every resource sits inside it.

## Read only

```bash
oci iam region list
oci iam compartment list --all --query 'data[].{name:name,id:id,state:"lifecycle-state"}'
oci ce cluster list --compartment-id <ocid>
oci compute instance list --compartment-id <ocid> --lifecycle-state RUNNING
oci usage-api usage-summary request-summarized-usages \
  --tenant-id <ocid> --granularity DAILY \
  --time-usage-started <iso> --time-usage-ended <iso>
oci iam policy list --compartment-id <ocid>
oci limits value list --compartment-id <ocid> --service-name compute
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| A policy granting `manage all-resources` in the tenancy | 1 | Effectively root over everything |
| Instance in a public subnet with an open security list | 2 | Exposure now |
| Service limit near its ceiling | 3 | Provisioning fails at the worst time, and raising a limit needs a ticket |
| Autonomous Database auto-scaling far above baseline | 3 | Cost, and usually a query regression behind it |
| Backup policy absent on a block volume | 2 | No recovery path, discovered during recovery |
| Resource in the root compartment | 4 | Ungoverned, and it will not inherit the policies you think it does |

## Dry run

Terraform with the OCI provider is the practical plan step. The CLI offers `--dry-run` on few commands, and Resource Manager stacks give a plan step in the console.

## Rollback

Volume backups and boot volume backups are the real rollback for compute. Autonomous Database has point in time recovery within its retention window. Neither exists unless it was configured first.

## Never without approval

Any `create`, `delete`, `update` or `terminate`. Policy changes, security list and NSG changes, compartment moves, and anything touching a database.

Confirm the tenancy, compartment and region before acting. A compartment OCID looks like every other OCID, and acting in the wrong compartment is easy.

## Failure modes

Policies are written in a domain specific language and inherit through compartments in ways that surprise. A denial names the policy but not the missing verb.

Service limits are per region and per shape, and the default is often one, which fails the first real deployment.

Availability domain naming is tenancy specific, so a script that hardcodes an AD name works in one tenancy and fails in another.

Terminating an instance without preserving the boot volume destroys it, and the default is not what people expect.
