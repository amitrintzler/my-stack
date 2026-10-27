# AWS

**Lock-in class.** Ranges from shallow to absorbing depending on the service. S3, EC2 and RDS are swappable in weeks. IAM's model, Lambda's runtime contract, DynamoDB's access patterns and Step Functions are structural. Data with egress cost attached is absorbing.

## Read only

```bash
aws sts get-caller-identity
aws iam get-account-summary
aws ce get-cost-and-usage --time-period Start=$(date -u -d '30 days ago' +%F 2>/dev/null || date -u -v-30d +%F),End=$(date -u +%F) \
  --granularity MONTHLY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE
aws eks list-clusters ; aws ecs list-clusters
aws iam list-users --query 'Users[?PasswordLastUsed==null].UserName'
aws ec2 describe-instances --filters Name=instance-state-name,Values=running \
  --query 'Reservations[].Instances[].[InstanceId,InstanceType,LaunchTime]' --output table
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Root account used recently | 1 | It should never be used after setup |
| Access key older than 90 days | 3 | Long-lived credentials are the usual breach path |
| IAM user with console access and no MFA | 2 | Same |
| Public S3 bucket not intended to be public | 1 | Data exposure now |
| Service cost up over 30 percent month on month | 3 | Something changed, usually a deploy or a retention setting |
| Untagged resources above a spend threshold | 4 | Nobody owns them, so nobody will turn them off |
| Reserved or savings plan expiring within 30 days | 3 | A cost cliff on a known date |

## Dry run

Most mutating CLI calls accept `--dry-run`. CloudFormation has change sets, and Terraform has plan. Use one of them; there is no reason to apply blind on AWS.

## Rollback

Service specific and mostly manual. CloudFormation can roll back a stack update; Terraform cannot without a revert and re-apply. Deleted data is gone unless versioning or a backup existed beforehand.

## Never without approval

Any `create`, `delete`, `modify`, `put` or `terminate`. Changing IAM policies, security groups, or bucket policies. Rotating or deleting keys. Anything in an account that is not explicitly named in the task.

Always confirm the account id and region before acting, and say both out loud. Cross-account mistakes are common and rarely reversible.

## Failure modes

IAM evaluation across SCPs, permission boundaries, resource policies and identity policies produces denials that are hard to attribute. Use the policy simulator rather than guessing.

Cross-AZ data transfer is invisible in architecture diagrams and highly visible in the bill.

Default service quotas bind at scale and the error message rarely says quota.

Deleting a security group rule takes effect instantly, with no staged rollout.
