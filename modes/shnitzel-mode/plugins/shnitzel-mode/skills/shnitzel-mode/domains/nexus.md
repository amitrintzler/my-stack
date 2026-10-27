# Sonatype Nexus

Repository manager for Maven, npm, Docker, raw and more. Usually self-hosted, usually the single point of failure nobody drew on the architecture diagram.

**Lock-in class.** Shallow for the artifacts, structural for the operation. Artifacts are just files, but the repository layout, cleanup policies and routing rules are Nexus specific.

## Read only

```bash
curl -sn "$NEXUS_URL/service/rest/v1/status"
curl -sn "$NEXUS_URL/service/rest/v1/repositories"
curl -sn "$NEXUS_URL/service/rest/v1/blobstores"
curl -sn "$NEXUS_URL/service/rest/v1/components?repository=<repo>"
curl -sn "$NEXUS_URL/service/rest/v1/security/privileges"
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Blob store over 80 percent | 2 | Writes fail, which stops every build at once |
| `/status` not returning 200 | 1 | Every build that resolves a dependency is down |
| Repository with no cleanup policy | 4 | Growth is unbounded by design |
| Proxy repository with a stale remote | 3 | Builds fall back to cached artifacts and drift silently |
| Anonymous write enabled | 2 | Anyone on the network can publish an artifact your builds trust |
| Snapshot repository never purged | 4 | The usual cause of a full blob store |

## Dry run

Cleanup policies have a preview that lists what would be deleted. Always read it. Deletion here is not recoverable without a blob store restore, and a restore takes hours.

## Rollback

There is none for a delete. The rollback is the backup, so confirm the blob store backup exists and has been restored at least once before running any cleanup.

## Never without approval

Deleting a component or a repository, running a cleanup task, changing a blob store, editing security realms or privileges, or restarting the service.

## Failure modes

A full blob store presents as random build failures across unrelated teams, because writes fail before reads do.

The compact blob store task is slow and blocking. Running it during working hours degrades every build.

Group repositories resolve members in order, and a reordered group changes which artifact wins with no other visible change.

Docker repositories need their own port or a reverse proxy path, and a misconfigured one fails only on push, not on pull.
