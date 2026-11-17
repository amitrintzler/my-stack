#!/usr/bin/env python3
"""Shnitzel usage: a Claude Code hook that records measured token usage per feature, and its report.

  usage.py hook                  Stop/SubagentStop hook; reads the hook JSON on stdin. Never fails the session.
  usage.py report [--days N]     table per feature and per effort tier, with estimated USD
  usage.py report --json         the same rows as JSON

Records only counts and labels: skill or command name, playbook file name, stated effort tier, model,
session id. Never prompts, code, tool input, file contents or reasoning. Turn it off with
`touch ~/.agents/shnitzel/usage.off` or SHNITZEL_USAGE=off.
"""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys

try:
    import fcntl
except ImportError:  # Windows: no lock, the cursor still prevents most duplicates and the report dedupes.
    fcntl = None

PLUGIN = Path(__file__).resolve().parents[1]
PRICING = PLUGIN / 'config/model-pricing.json'
TIERS = ('direct', 'focused', 'standard', 'deep')
TIER_MARK = re.compile(r'Shnitzel tier:\W{0,4}(direct|focused|standard|deep)\b', re.I)
COMMAND = re.compile(r'<command-name>/?([^<\s]+)</command-name>')
SKILL_FILE = re.compile(r'/skills/([\w.-]+)/SKILL\.md$')
PLAYBOOK_FILE = re.compile(r'/playbooks/([\w.-]+)\.md$')


def state_dir():
    return Path(os.environ.get('SHNITZEL_STATE') or Path.home() / '.agents/shnitzel') / 'usage'


def disabled():
    return (os.environ.get('SHNITZEL_USAGE', '').lower() in ('off', '0', 'false')
            or (state_dir().parent / 'usage.off').exists())


def number(value):
    return value if type(value) is int and value >= 0 else 0


def text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return '\n'.join(b.get('text', '') for b in content if isinstance(b, dict) and b.get('type') == 'text')
    return ''


def label(name):
    """A skill or command name, never free text: keep it short and plain."""
    name = str(name or '').strip().lstrip('/')
    return name[:80] if re.fullmatch(r'[\w.:@-]+', name or '-') else None


def measure(usage):
    creation = usage.get('cache_creation') if isinstance(usage.get('cache_creation'), dict) else {}
    write_1h = number(creation.get('ephemeral_1h_input_tokens'))
    write_5m = number(creation.get('ephemeral_5m_input_tokens')) if creation else number(usage.get('cache_creation_input_tokens'))
    if creation and not write_5m and not write_1h:
        write_5m = number(usage.get('cache_creation_input_tokens'))
    row = {'uncached_input_tokens': number(usage.get('input_tokens')),
           'cache_read_tokens': number(usage.get('cache_read_input_tokens')),
           'cache_write_5m_tokens': write_5m, 'cache_write_1h_tokens': write_1h,
           'output_tokens': number(usage.get('output_tokens'))}
    # Same convention as lib/budget.py normalize(): cache reads and writes are part of input.
    row['input_tokens'] = row['uncached_input_tokens'] + row['cache_read_tokens'] + write_5m + write_1h
    row['total_tokens'] = row['input_tokens'] + row['output_tokens']
    if usage.get('speed') == 'fast':
        row['speed'] = 'fast'
    return row


def scan(path, session, context, subagent, cursors):
    """Read new complete lines of one transcript and return (events, context). Updates the cursor file."""
    path = Path(path)
    cursor_file = cursors / (hashlib.sha256(str(path).encode()).hexdigest()[:20] + '.json')
    try:
        cursor = json.loads(cursor_file.read_text())
    except (OSError, ValueError):
        cursor = {'offset': 0, 'context': dict(context or {})}
    ctx = cursor.get('context') or {}
    if subagent and context:
        # A subagent works for whatever its parent was doing when it was spawned.
        ctx = {**context, **{k: v for k, v in ctx.items() if v}}
    offset = cursor.get('offset', 0)
    size = path.stat().st_size
    if size < offset:
        offset = 0
    with path.open('rb') as stream:
        stream.seek(offset)
        data = stream.read()
    end = data.rfind(b'\n') + 1
    events, pending = {}, dict(cursor.get('pending') or {})
    for raw in data[:end].splitlines():
        try:
            entry = json.loads(raw)
        except ValueError:
            continue
        if not isinstance(entry, dict):
            continue
        side = subagent or bool(entry.get('isSidechain'))
        message = entry.get('message') if isinstance(entry.get('message'), dict) else {}
        content = message.get('content')
        if entry.get('type') == 'user':
            if isinstance(content, list) and any(isinstance(b, dict) and b.get('type') == 'tool_result' for b in content):
                # A skill or playbook counts once its load succeeded, not when it was requested.
                for b in content:
                    if isinstance(b, dict) and b.get('type') == 'tool_result' and not b.get('is_error'):
                        ctx.update(pending.pop(b.get('tool_use_id'), {}))
                continue
            text = text_of(content)
            command = COMMAND.search(text)
            if command and label(command.group(1)):
                if not side:
                    ctx = {}
                ctx['feature'] = label(command.group(1))
            elif not side and not entry.get('isMeta') and text.strip() and not text.lstrip().startswith('<local-command'):
                ctx = {}  # a new prompt starts a new turn with nothing attributed yet
            continue
        if entry.get('type') != 'assistant':
            continue
        usage, model = message.get('usage'), message.get('model')
        blocks = content if isinstance(content, list) else []
        for block in blocks:
            if isinstance(block, dict) and block.get('type') == 'text':
                mark = TIER_MARK.search(block.get('text', ''))
                if mark:
                    ctx['tier'] = mark.group(1).lower()
        if isinstance(usage, dict) and model and model != '<synthetic>':
            key = message.get('id') or entry.get('uuid')
            if key:
                event = events.get(key)
                if event is None:
                    event = {'version': 1, 'event_id': 'cc:' + str(key), 'at': entry.get('timestamp') or now(),
                             'run_id': session, 'session_id': session, 'runtime': 'claude', 'source': 'claude_code_hook',
                             'measured': True, 'model': str(model)[:80], 'subagent': side,
                             'feature': ctx.get('feature') or 'unattributed', 'tier': ctx.get('tier'),
                             'playbook': ctx.get('playbook')}
                    events[key] = event
                # Claude Code writes one line per content block with the same id; the last carries final usage.
                event.update(measure(usage))
        # A message is charged to what was active when it was sent; what it loads applies afterwards.
        for block in blocks:
            if not isinstance(block, dict) or block.get('type') != 'tool_use':
                continue
            data_in = block.get('input') if isinstance(block.get('input'), dict) else {}
            change = {}
            if block.get('name') == 'Skill':
                name = label(data_in.get('skill') or data_in.get('command'))
                if name:
                    change = {'feature': name, 'playbook': None}
            elif block.get('name') == 'Read':
                target = str(data_in.get('file_path') or '')
                skill, playbook = SKILL_FILE.search(target), PLAYBOOK_FILE.search(target)
                if skill and label(skill.group(1)):
                    change = {'feature': label(skill.group(1))}
                elif playbook and label(playbook.group(1)):
                    change = {'playbook': label(playbook.group(1))}
            if change and block.get('id'):
                pending[block['id']] = change
    cursor = {'offset': offset + end, 'context': ctx, 'pending': dict(list(pending.items())[-20:])}
    tmp = cursor_file.with_suffix('.tmp')
    tmp.write_text(json.dumps(cursor))
    tmp.replace(cursor_file)
    return list(events.values()), ctx


def now():
    return datetime.now(timezone.utc).isoformat()


def hook(stdin=sys.stdin):
    if disabled():
        return
    base = state_dir()
    try:
        payload = json.loads(stdin.read() or '{}')
        session = str(payload.get('session_id') or '')[:80] or None
        main, agent = payload.get('transcript_path'), payload.get('agent_transcript_path')
        cursors = base / 'cursors'
        cursors.mkdir(parents=True, exist_ok=True)
        with (base / '.lock').open('a') as lock:
            if fcntl:
                fcntl.flock(lock, fcntl.LOCK_EX)
            events, ctx = scan(main, session, None, False, cursors) if main and Path(main).is_file() else ([], {})
            agents = [Path(agent)] if agent and agent != main and Path(agent).is_file() else []
            if main:
                # Subagent transcripts can still be written after their SubagentStop (background agents),
                # so every Stop also picks up what is new in this session's subagent files.
                agents += sorted(p for p in (Path(main).with_suffix('') / 'subagents').glob('*.jsonl') if p not in agents)
            for path in agents:
                more, _ = scan(path, session, ctx, True, cursors)
                events += more
            if events:
                ledger = base / ('ledger-' + datetime.now(timezone.utc).strftime('%Y-%m') + '.jsonl')
                with ledger.open('a') as out:
                    out.write(''.join(json.dumps(e, separators=(',', ':')) + '\n' for e in events))
    except Exception as error:  # a usage hook must never break or slow the session
        try:
            base.mkdir(parents=True, exist_ok=True)
            with (base / 'errors.jsonl').open('a') as out:
                out.write(json.dumps({'at': now(), 'error': type(error).__name__}) + '\n')
        except OSError:
            pass


def load(base, since=None, session=None):
    rows = {}
    for ledger in sorted(base.glob('ledger-*.jsonl')):
        with ledger.open() as stream:
            for line in stream:
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if since and str(row.get('at', '')) < since:
                    continue
                if session and row.get('session_id') != session:
                    continue
                rows[row.get('event_id')] = row  # the last record of an event wins
    return list(rows.values())


def model_key(model):
    key = str(model or '').lower().split('/')[-1]
    key = re.sub(r'^(?:[a-z]{2,4}\.)?anthropic\.', '', key)
    key = re.sub(r'(?:\[[^\]]*\]|@.*|-v\d+(?::\d+)?|-\d{8})+$', '', key)
    return key[len('claude-'):] if key.startswith('claude-') else key


def price(row, table):
    rates = table['models'].get(model_key(row.get('model')))
    if not rates:
        return None
    if row.get('speed') == 'fast':
        rates = rates.get('fast')
        if not rates:
            return None
    long = rates.get('long_context')
    if long and row.get('input_tokens', 0) > long['above_input_tokens']:
        rates = {**rates, **long}
    rate_in = rates['input']
    mult = table['cache_multipliers']
    cache_read = rates.get('cache_read', rate_in * mult['read'])
    write_5m = rates.get('cache_write_5m', rate_in * mult['write_5m'])
    write_1h = rates.get('cache_write_1h', rate_in * mult['write_1h'])
    return (row.get('uncached_input_tokens', 0) * rate_in + row.get('cache_read_tokens', 0) * cache_read
            + row.get('cache_write_5m_tokens', 0) * write_5m + row.get('cache_write_1h_tokens', 0) * write_1h
            + row.get('output_tokens', 0) * rates['output']) / 1e6


FIELDS = ('calls', 'uncached_input_tokens', 'cache_read_tokens', 'cache_write_tokens', 'output_tokens', 'total_tokens')


def group(rows, key, table):
    out = {}
    for row in rows:
        name = row.get(key)
        if key == 'tier':
            name = name or 'not stated'
        elif key == 'subagent':
            name = 'subagent' if name else 'main'
        name = str(name or 'none')
        agg = out.setdefault(name, dict.fromkeys(FIELDS, 0) | {'usd_estimate': 0.0, 'unpriced_calls': 0})
        agg['calls'] += 1
        for field in ('uncached_input_tokens', 'cache_read_tokens', 'output_tokens', 'total_tokens'):
            agg[field] += row.get(field, 0)
        agg['cache_write_tokens'] += row.get('cache_write_5m_tokens', 0) + row.get('cache_write_1h_tokens', 0)
        cost = price(row, table)
        if cost is None:
            agg['unpriced_calls'] += 1
        else:
            agg['usd_estimate'] += cost
    return dict(sorted(out.items(), key=lambda item: (-item[1]['usd_estimate'], -item[1]['total_tokens'])))


def compact(value):
    for unit, size in (('B', 1e9), ('M', 1e6), ('k', 1e3)):
        if value >= size:
            return f'{value / size:.1f}{unit}'
    return str(value)


def usd_text(value):
    return f'{value:.2f}' if value >= 0.995 or value == 0 else f'{value:.3f}'


def table_text(title, groups):
    head = ('calls', 'input', 'cache read', 'cache write', 'output', 'total', 'est. USD')
    rows = [(name, str(g['calls']), compact(g['uncached_input_tokens']), compact(g['cache_read_tokens']),
             compact(g['cache_write_tokens']), compact(g['output_tokens']), compact(g['total_tokens']),
             (usd_text(g['usd_estimate']) + ('*' if g['unpriced_calls'] else ''))) for name, g in groups.items()]
    if not rows:
        return ''
    total = {f: sum(g[f] for g in groups.values()) for f in FIELDS}
    usd = sum(g['usd_estimate'] for g in groups.values())
    rows.append(('total', str(total['calls']), compact(total['uncached_input_tokens']), compact(total['cache_read_tokens']),
                 compact(total['cache_write_tokens']), compact(total['output_tokens']), compact(total['total_tokens']),
                 usd_text(usd)))
    widths = [max(len(title), *(len(r[0]) for r in rows))] + [max(len(h), *(len(r[i + 1]) for r in rows)) for i, h in enumerate(head)]
    line = lambda cells: '  '.join([cells[0].ljust(widths[0])] + [c.rjust(w) for c, w in zip(cells[1:], widths[1:])])
    return '\n'.join([line((title,) + head)] + [line(r) for r in rows])


def report(args):
    table = json.loads(PRICING.read_text())
    since = None if args.days == 0 else (datetime.now(timezone.utc) - timedelta(days=args.days)).isoformat()
    rows = load(state_dir(), since, args.session)
    groups = {key: group(rows, key, table) for key in args.by}
    if args.json:
        print(json.dumps({'measured_events': len(rows), 'since': since, 'pricing_as_of': table['as_of'],
                          'usd_is_estimate': True, 'groups': groups}, indent=2))
        return 0
    period = 'all time' if since is None else f'last {args.days} days'
    if not rows:
        state = 'off (usage.off or SHNITZEL_USAGE=off)' if disabled() else 'on'
        print(f'No measured usage yet ({period}). Recording is {state}; it fills in after the next Claude Code turn.')
        return 0
    print(f'Shnitzel usage, {period}: {len(rows)} measured model calls from Claude Code.')
    print(f"Tokens are measured. USD is an API-price estimate from model-pricing.json (prices as of {table['as_of']}), "
          'not a bill; on a subscription plan you are not charged per token.')
    titles = {'feature': 'feature', 'tier': 'effort tier', 'model': 'model', 'playbook': 'playbook',
              'subagent': 'agent', 'session_id': 'session'}
    for key in args.by:
        print('\n' + table_text(titles.get(key, key), groups[key]))
    if any(g['unpriced_calls'] for groups_ in groups.values() for g in groups_.values()):
        print('\n* includes calls on a model with no price in model-pricing.json; their tokens count, their USD does not.')
    if 'tier' in args.by:
        print("'not stated' tier: the turn named no tier (Direct and Focused work usually never opens the router).")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('hook')
    rep = sub.add_parser('report')
    rep.add_argument('--days', type=int, default=30, help='0 for all time (default 30)')
    rep.add_argument('--session')
    rep.add_argument('--by', default='feature,tier', type=lambda s: [p for p in s.split(',') if p],
                     help='comma list of feature, tier, model, playbook, subagent, session_id')
    rep.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    if args.action == 'hook':
        hook()
        return 0
    bad = set(args.by) - {'feature', 'tier', 'model', 'playbook', 'subagent', 'session_id'}
    if bad:
        parser.error('unknown --by: ' + ', '.join(sorted(bad)))
    return report(args)


if __name__ == '__main__':
    raise SystemExit(main())
