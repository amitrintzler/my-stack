# Azure

**Lock-in class.** Entra ID is absorbing once it is your identity provider, since every application and every RBAC assignment binds to it. AKS, Storage and VMs are shallow. Logic Apps, Functions bindings and Azure Policy are structural.

## Read only

```bash
az account show
az account list --query '[].{name:name,id:id,state:state}' -o table
az consumption usage list --start-date $(date -u -d '30 days ago' +%F 2>/dev/null || date -u -v-30d +%F) --end-date $(date -u +%F) --query '[].{svc:meterDetails.meterCategory,cost:pretaxCost}' -o tsv
az aks list -o table
az acr repository list -n <registry>
az advisor recommendation list --query '[].{cat:category,impact:impact,problem:shortDescription.problem}' -o table
az role assignment list --all --query "[?principalType=='User'].{p:principalName,r:roleDefinitionName,s:scope}" -o table
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Owner assigned at subscription scope to a user | 2 | Almost always broader than intended |
| Guest account with a standing role assignment | 2 | External identity with production access |
| Service principal secret expiring within 30 days | 2 | A dated outage, and it takes down CI first |
| AKS version out of support | 3 | No patches, and the upgrade window is not optional |
| Public network access enabled on a data service | 2 | The default is more open than people assume |
| Cost anomaly flagged by Advisor | 3 | Usually a forgotten environment |
| Resource without an owner tag | 4 | Nobody will turn it off |

## Dry run

`az deployment group what-if` is the closest to a real plan and it is genuinely good. Bicep and ARM both support it. Terraform plan otherwise.

## Rollback

Deployments in a resource group keep a history and a previous template can be redeployed. That is not an undo, since it does not restore deleted data or reverse a data-plane change.

## Never without approval

Any `create`, `delete`, `update` or `set`. Role assignments, network security group rules, policy assignments, key vault access policies, and anything touching Entra ID.

Confirm the subscription before every command. `az account show` first, and say which subscription you are on.

## Failure modes

Management group policy inherits downward and denies deployments with an error that names the policy rather than the intent.

Resource providers must be registered per subscription, and an unregistered provider fails a deployment that works elsewhere in the same tenant.

Soft delete on Key Vault and Storage means a recreate with the same name fails until the purge completes.

Regional capacity constraints on specific VM sizes surface as deployment failures rather than as quota errors.
