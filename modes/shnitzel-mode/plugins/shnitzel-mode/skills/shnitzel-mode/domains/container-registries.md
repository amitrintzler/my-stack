# Container registries and the OCI specification

Where images live: GHCR, ECR, ACR, Google Artifact Registry, Harbor, Quay, or a Docker repository inside Nexus or Artifactory.

A note on the abbreviation. OCI here is the Open Container Initiative, the image and distribution specification every one of these implements. Oracle Cloud Infrastructure is a different thing entirely and has its own card, `oracle-cloud.md`. Confusing the two in a design document is common and expensive.

**Lock-in class.** Shallow, and this is one of the genuinely portable layers. The OCI spec means images move between registries with a copy. Signing, scanning and lifecycle policies do not.

## Read only

```bash
crane ls <registry>/<repo>            # or: skopeo list-tags docker://<registry>/<repo>
crane digest <registry>/<repo>:<tag>
crane manifest <registry>/<repo>:<tag>
aws ecr describe-images --repository-name <repo>
az acr repository show-tags -n <registry> --repository <repo>
gcloud artifacts docker images list <region>-docker.pkg.dev/<project>/<repo>
gh api /orgs/{org}/packages?package_type=container
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| A production deployment referencing a mutable tag | 2 | What runs is not what was tested. Pin the digest |
| `latest` referenced anywhere in a manifest | 3 | The same class of problem, more visibly |
| No lifecycle or retention policy | 4 | Cost grows quietly and forever |
| Critical vulnerabilities in a running image | 2 | Exploitable now, not theoretically |
| Unsigned images where signing is required | 3 | The admission policy will reject them, usually at the worst time |
| Base image older than 90 days | 4 | Accumulating known CVEs by default |

## Dry run

`crane copy --dry-run` where supported, otherwise copy to a scratch repository first. Verify the digest before and after any promotion. The digest is the only identity that means anything.

## Rollback

Redeploy the previous digest. This is the cleanest rollback in the entire stack, and it only works if you recorded the digest rather than the tag.

## Never without approval

Deleting images or tags, running a retention policy, retagging (which silently changes what a tag means), pushing to a production repository, and changing registry permissions.

## Failure modes

Retag as rollback rewrites history and nobody can tell afterwards what ran when.

Multi-architecture manifests confuse tooling that assumes one image per tag, and an arm64 node pulling an amd64-only image fails with an unhelpful error.

Pull rate limits on public registries fail builds at random times of day, which reads as flakiness.

Deleting a tag does not free storage while another tag references the same digest.
