---
name: artifact-registry
description: Work with Nexus, Artifactory or a container registry. Check capacity and retention, trace what is actually deployed, and promote through environments without losing provenance. Use for nexus, artifactory, jfrog, registry, ECR, ACR, GHCR, image promotion, retention policy, which image is running.
---

# Artifact registry

Two questions come up repeatedly. What is actually running in production, and why is storage full.

Domain detail is in [`domains/nexus.md`](../shnitzel-mode/domains/nexus.md), [`domains/artifactory.md`](../shnitzel-mode/domains/artifactory.md) and [`domains/container-registries.md`](../shnitzel-mode/domains/container-registries.md).

## The digest is the only identity

A tag is a pointer someone can move. A digest is the artifact. When tracing what is running, resolve to the digest and compare digests, never tags. Most "but we deployed the fix" conversations end the moment someone resolves the digest.

Deployments should reference digests. Where they reference tags, that is a finding worth writing down even when nothing is currently broken.

## Promotion

Build once, promote the same artifact through environments. Rebuilding per environment means the thing in production was never the thing that was tested, however identical the inputs looked.

Promotion should be a copy or a move between repositories with the digest preserved, not a rebuild and not a retag. Publishing straight into a release repository bypasses the gate and is worth flagging.

## Storage is an availability problem

A full blob store or a full storage volume fails writes before reads, so it presents as scattered build failures across unrelated teams rather than as a storage alert. Check capacity first when several teams report unrelated CI failures at once.

Every repository needs a retention or cleanup policy. A repository without one grows without bound by design, and snapshot repositories are almost always the largest.

## Before deleting anything

Read the preview. Nexus cleanup policies and `jf rt del --dry-run` both list what would go. Deletion is not recoverable without a blob store restore, so confirm the backup exists and has actually been restored at least once. A backup nobody has restored is a hypothesis.

Checksum-based storage means freed space rarely matches deleted size, because another path may reference the same binary. Capacity plans built on deleted size are wrong.

## Never

Deleting artifacts or repositories, running cleanup, promoting a build, retagging, changing permissions or replication, and restarting the service. Retagging deserves its own line, since it rewrites what a tag means and destroys the record of what ran when.
