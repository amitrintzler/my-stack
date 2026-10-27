# JFrog Artifactory

Repository manager across many package types, often with Xray for vulnerability scanning attached.

**Lock-in class.** Structural. AQL, the permission model, build info and replication have no equivalent elsewhere, even though the artifacts themselves are portable.

## Read only

```bash
jf rt ping
jf rt curl -s /api/repositories
jf rt curl -s /api/storageinfo
jf rt search "libs-release-local/*" --limit 10
jf rt curl -s '/api/search/aql' -H 'Content-Type: text/plain' \
  -d 'items.find({"repo":"libs-release-local","created":{"$before":"90d"}}).limit(10)'
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Storage over 80 percent | 2 | Writes fail and every build stops |
| `/api/system/ping` failing | 1 | Dependency resolution is down everywhere |
| Xray critical findings on a promoted artifact | 2 | Something already in production has a known exploit |
| Replication lagging or failed | 3 | A remote site is building against stale artifacts |
| Repository with no retention or no promotion path | 4 | Unbounded growth and no provenance story |
| Artifacts published straight to a release repository | 3 | The promotion gate is being bypassed |

## Dry run

AQL queries are read-only, so build the delete criteria as an AQL search first and read the result before any cleanup. `jf rt del --dry-run` shows what would go.

## Rollback

Deleted artifacts are gone unless trash can retention is enabled and still inside its window. Check the retention setting before deleting, not after.

## Never without approval

Deleting artifacts or repositories, running cleanup, promoting a build, changing permissions or replication, and modifying Xray policies.

## Failure modes

Promotion by copy rather than by move duplicates storage and doubles the growth rate.

Virtual repository ordering silently decides which artifact resolves, and a reorder changes builds with no commit anywhere.

Checksum-based storage means deleting one artifact can leave the binary in place because another path references it, so freed space does not match deleted size and capacity planning based on it is wrong.

Xray scanning lags behind publication, so a fresh artifact is unscanned rather than clean.
