#!/usr/bin/env python3
"""Merge collector data without treating failed queries as healthy emptiness."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def collect(name, args, directory=None):
    try:
        result = subprocess.run([str((directory or ROOT / 'bin') / (name + '.sh')), *args], capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise ValueError('collector exited ' + str(result.returncode))
        data = json.loads(result.stdout)
        if name == 'gh-collect':
            items, coverage = data['items'], data.get('coverage', {'status': 'unknown'})
        elif isinstance(data, dict):
            items, coverage = data['items'], data['coverage']
        else:
            items, coverage = data, {'status': 'observed'}
        if not isinstance(items, list) or any(not isinstance(i, dict) or not {'id', 'kind', 'severity', 'title'}.issubset(i) for i in items):
            raise ValueError('invalid collector item schema')
        return items, coverage, data
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        item = {'id': 'collector:' + name, 'kind': 'collector_unavailable', 'severity': 3, 'repo': name,
                'title': name + ' unavailable: ' + str(error), 'url': '', 'fingerprint': 'unavailable', 'detail': None}
        return [item], {'status': 'unavailable'}, None


def merge(config, all_items=False, no_state=False, directory=None):
    config_args = ['--config', str(config)]
    gh_args = config_args + (['--all'] if all_items else []) + (['--no-state'] if no_state else [])
    items, sources, github = [], {}, None
    for name, args in [('gh-collect', gh_args), ('feature-scan', config_args), ('scope-check', config_args), ('domain-scan', config_args + ['--coverage'])]:
        found, coverage, data = collect(name, args, directory)
        items.extend(found)
        sources[name] = coverage
        if name == 'gh-collect':
            github = data
        if coverage.get('status') == 'incomplete':
            items.append({'id': 'collector:' + name, 'kind': 'collector_unavailable', 'severity': 3, 'repo': name,
                          'title': name + ' has unavailable queries; absence of findings is inconclusive',
                          'url': '', 'fingerprint': 'incomplete', 'detail': coverage})
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    result = {'version': 1, 'generated_at': now, 'coverage': sources,
              'github': {k: (github or {}).get(k) for k in ['total', 'new', 'suppressed']},
              'features': {'total': sum(i['kind'].startswith('feat') for i in items)},
              'scope': {'total': sum(i['kind'].startswith('scope') for i in items)},
              'domains': {'total': sum(i.get('repo') in ['argocd', 'kubernetes', 'openshift', 'vault'] for i in items)},
              'items': sorted(items, key=lambda i: i['severity']), 'counts': dict(Counter(i['kind'] for i in items))}
    if all_items and not no_state:
        state = Path.home() / '.agents/shnitzel'
        state.mkdir(parents=True, exist_ok=True)
        path = state / 'open-ages.json'
        old = json.loads(path.read_text()) if path.exists() else {}
        complete = all(c.get('status') == 'observed' for c in sources.values())
        ages = {} if complete else dict(old)
        for item in items:
            if item['kind'] != 'collector_unavailable':
                ages[item['id']] = {'first_seen': old.get(item['id'], {}).get('first_seen', now),
                                    **{k: item[k] for k in ['kind', 'severity', 'title']}}
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(ages, indent=2) + '\n')
        tmp.replace(path)
        by_kind = {}
        for age in ages.values():
            days = (datetime.now(timezone.utc) - datetime.fromisoformat(age['first_seen'].replace('Z', '+00:00'))).total_seconds() / 86400
            by_kind.setdefault(age['kind'], []).append(days)
        with (state / 'metrics.jsonl').open('a') as stream:
            stream.write(json.dumps({'at': now, 'total': len(items), 'counts': result['counts'],
                                     'coverage_complete': complete,
                                     'age_days_by_kind': {k: int(sum(v) / len(v)) for k, v in by_kind.items()}}) + '\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=Path.home() / '.agents/watch.conf')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--no-state', action='store_true')
    parser.add_argument('--pretty', action='store_true')
    args = parser.parse_args()
    result = merge(args.config, args.all, args.no_state)
    if args.pretty:
        print('shnitzel watch  ' + result['generated_at'])
        print('coverage: ' + ', '.join(k + '=' + v.get('status', 'unknown') for k, v in result['coverage'].items()))
        for item in result['items']:
            print('  [{}] {}  {}'.format(item['severity'], item['kind'], item['title']))
    else:
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
