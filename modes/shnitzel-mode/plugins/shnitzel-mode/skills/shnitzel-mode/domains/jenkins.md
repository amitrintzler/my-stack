# Jenkins

Long-lived CI, usually self-hosted, usually carrying years of accumulated plugins and one Jenkinsfile nobody wants to touch.

**Lock-in class.** Structural, and the depth is in the plugins rather than the pipelines. Declarative Jenkinsfiles port reasonably; shared libraries, plugin-specific steps and credential bindings do not.

## Read only

```bash
curl -sn "$JENKINS_URL/api/json?tree=jobs[name,color,lastBuild[number,result,timestamp]]"
curl -sn "$JENKINS_URL/job/<job>/api/json?tree=builds[number,result,duration,timestamp]"
curl -sn "$JENKINS_URL/computer/api/json?tree=computer[displayName,offline,temporarilyOffline,numExecutors]"
curl -sn "$JENKINS_URL/queue/api/json"
curl -sn "$JENKINS_URL/pluginManager/api/json?depth=1&tree=plugins[shortName,version,hasUpdate,deprecated]"
```

Use `-n` with a `.netrc` entry or an API token in an environment variable. Never inline a token in a command that lands in a log or a report.

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Agents offline | 2 | Jobs queue with no failure and no alert |
| Queue depth high with idle executors | 3 | A label mismatch, not a capacity problem |
| Build duration doubled over a week | 3 | Usually disk or a noisy neighbour, rarely the code |
| Plugins with security updates pending | 2 | Jenkins plugin advisories are frequent and often remote code execution |
| Controller disk over 80 percent | 2 | Build history fills it, and a full controller corrupts jobs |
| Job with no SCM trigger and no recent build | 5 | Probably dead, and it should be archived deliberately |

## Dry run

The Replay feature runs a modified Jenkinsfile once without committing it. Treat it as a scratch pad rather than a test, since it does not prove what the committed file does.

## Rollback

Revert the Jenkinsfile or the shared library tag. Job configuration changed through the UI has no history unless the configuration-as-code or job-config-history plugin is installed, which is the reason to insist on configuration as code.

## Never without approval

Triggering or aborting a build, installing or updating plugins, restarting the controller, taking an agent offline, editing credentials, or changing job configuration through the UI.

## Failure modes

Plugin updates break pipelines in ways the changelog does not mention. Snapshot the controller before updating.

Shared library changes take effect immediately across every pipeline that consumes `@main`. Pin to a tag.

Workspace state left by a previous build is the most common cause of a build that passes locally and fails on the agent.

The controller doing real work rather than delegating to agents is the usual root cause of slowness that looks like a code problem.
