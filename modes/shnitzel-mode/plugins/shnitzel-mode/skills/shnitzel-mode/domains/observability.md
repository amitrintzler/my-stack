# Observability

Prometheus, Grafana, Alertmanager, and whichever commercial platform sits alongside them. Grouped as one domain because the questions are the same regardless of vendor.

**Lock-in class.** PromQL and OpenTelemetry are shallow, and instrumenting with OTel is the single best portability decision available here. Vendor-specific agents, proprietary query languages and stored history are structural, and years of retained data is absorbing.

## Read only

```bash
curl -s "$PROM_URL/api/v1/rules" | jq '.data.groups[].rules[] | select(.type=="alerting") | {name,state}'
curl -s "$PROM_URL/api/v1/alerts" | jq '.data.alerts[] | {name:.labels.alertname,state}'
curl -s "$PROM_URL/api/v1/targets" | jq '.data.activeTargets[] | select(.health!="up") | {job:.labels.job,err:.lastError}'
amtool alert query --alertmanager.url="$AM_URL"
amtool silence query --alertmanager.url="$AM_URL"
curl -s "$PROM_URL/api/v1/status/tsdb" | jq '.data.headStats'
```

## Signals

| Signal | Severity | Means |
| --- | --- | --- |
| Scrape target down | 2 | You are blind to that service, and alerts on it will not fire |
| Silence expiring within an hour on a firing alert | 2 | The alert is about to reappear, possibly at 03:00 |
| Silence with no expiry | 3 | An alert permanently disabled and forgotten |
| Alert firing continuously for over a week | 3 | It is furniture now, and it trains people to ignore the panel |
| Alert rule with no runbook annotation | 4 | It will page someone who does not know what to do |
| Cardinality growing sharply | 3 | A label with unbounded values, and it will take Prometheus down |
| Recording rule failing | 3 | Dashboards silently show nothing rather than an error |

## Dry run

`promtool check rules` validates syntax, and `promtool test rules` runs unit tests against sample series. Alert rules deserve tests exactly as much as code does, and almost never get them.

## Rollback

Revert the rule or dashboard definition in Git. Dashboards edited in the Grafana UI have no version history worth relying on, which is the argument for provisioning them as code.

## Never without approval

Creating or expiring a silence, editing or deleting alert rules, changing retention, restarting a Prometheus instance, and modifying a dashboard that others rely on.

## Failure modes

Alerting on causes rather than symptoms produces pages nobody can act on. High CPU is not an incident. Failing requests are.

A `for` duration that is too short produces flapping, and one that is too long delays the page past the point of usefulness.

Cardinality explosions from a user id or a request id in a label take the whole instance down, and the query that reveals it is itself expensive.

A dashboard that reads from a recording rule shows an empty panel rather than an error when the rule fails, so the absence of data reads as the absence of a problem.
