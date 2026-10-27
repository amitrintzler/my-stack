# Google Cloud

**Lock-in class.** GKE and GCS are shallow. IAM's resource hierarchy, BigQuery's pricing and access model, and Cloud Run's contract are structural. BigQuery with large stored data and egress cost is absorbing.

## Read only

```bash
gcloud auth list
gcloud config list
gcloud projects list
gcloud container clusters list
gcloud artifacts repositories list
gcloud projects get-iam-policy <project> --flatten='bindings[].members' \
  --format='table(bindings.role,bindings.members)'
gcloud logging read 'severity>=ERROR' --limit 20 --freshness 1h
bq ls --format=pretty
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| `roles/owner` or `roles/editor` on a service account | 2 | Editor is far broader than almost any workload needs |
| Service account key file that exists at all | 2 | Workload identity removes the need for one, and keys leak |
| `allUsers` or `allAuthenticatedUsers` in a binding | 1 | Public access, usually accidental |
| GKE cluster on a version past end of support | 3 | Auto-upgrade will act eventually, on its schedule not yours |
| Budget threshold crossed | 3 | Usually BigQuery scanning or an idle cluster |
| Firewall rule allowing 0.0.0.0/0 to a non-public port | 2 | Exposure now |
| BigQuery query scanning terabytes on a schedule | 3 | The single most common surprise line on a GCP bill |

## Dry run

`gcloud ... --dry-run` where offered, `bq query --dry_run` for the byte estimate before running a query, and Terraform plan for infrastructure. The BigQuery dry run costs nothing and prevents the expensive mistake.

## Rollback

Deployment Manager is deprecated, so in practice rollback means Terraform revert and re-apply, or a redeploy of the previous revision on Cloud Run. Deleted projects are recoverable within 30 days; deleted resources inside them usually are not.

## Never without approval

Any `create`, `delete`, `update`, or `set-iam-policy`. Changing firewall rules, org policies, or budget alerts. Running a BigQuery job that scans a large table.

Confirm the project before every command. `gcloud config get project` first, and say it.

## Failure modes

`set-iam-policy` replaces the whole policy. Use `add-iam-policy-binding` unless you intend to overwrite, and read back afterwards.

Org policy constraints inherited from a folder deny at deploy time with a message that names the constraint but not the fix.

Quotas are per project and per region, and the default is often lower than the first real workload needs.

BigQuery on-demand pricing charges for bytes scanned, so an unpartitioned table turns a cheap query into an expensive one with no warning.
