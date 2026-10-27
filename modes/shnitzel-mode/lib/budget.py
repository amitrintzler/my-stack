#!/usr/bin/env python3
"""Atomic model-token reservations for request-intercepting hosts, not a CLI cap."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
from decimal import Decimal, ROUND_CEILING
import json
import math
from pathlib import Path
import sqlite3
import uuid

ROOT = Path(__file__).resolve().parents[1]


def integer(value):
    if type(value) is not int or value < 0:
        raise ValueError('usage must be a nonnegative integer')
    return value


def money(value):
    number = Decimal(str(value))
    if not number.is_finite() or number < 0:
        raise ValueError('cost must be finite and nonnegative')
    return int((number * 10**9).to_integral_value(rounding=ROUND_CEILING))


class BudgetLedger:
    """All dispatches must first reserve; the host must enforce the reserved maximum."""
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, timeout=20, isolation_level=None)
        self.db.executescript('''
          CREATE TABLE IF NOT EXISTS runs (
            id TEXT PRIMARY KEY, token_cap INTEGER, cost_cap INTEGER, blocked INTEGER NOT NULL DEFAULT 0);
          CREATE TABLE IF NOT EXISTS reservations (
            id TEXT PRIMARY KEY, run_id TEXT NOT NULL, tokens INTEGER NOT NULL, cost INTEGER,
            settled INTEGER NOT NULL DEFAULT 0);
        ''')

    @contextmanager
    def transaction(self):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            yield
            self.db.execute('COMMIT')
        except BaseException:
            self.db.execute('ROLLBACK')
            raise

    def create(self, run_id, max_tokens=None, max_cost_usd=None):
        if max_tokens is None and max_cost_usd is None:
            raise ValueError('a budget is required')
        tokens = integer(max_tokens) if max_tokens is not None else None
        cost = money(max_cost_usd) if max_cost_usd is not None else None
        self.db.execute('INSERT INTO runs(id,token_cap,cost_cap) VALUES(?,?,?)', (run_id, tokens, cost))

    def reserve(self, run_id, input_tokens, max_output_tokens, max_cost_usd=None):
        tokens = integer(input_tokens) + integer(max_output_tokens)
        cost = money(max_cost_usd) if max_cost_usd is not None else None
        with self.transaction():
            run = self.db.execute('SELECT token_cap,cost_cap,blocked FROM runs WHERE id=?', (run_id,)).fetchone()
            if run is None or run[2]:
                raise ValueError('run missing or blocked')
            used = self.db.execute('SELECT COALESCE(SUM(tokens),0),COALESCE(SUM(cost),0) FROM reservations WHERE run_id=?', (run_id,)).fetchone()
            if (run[0] is not None and used[0] + tokens > run[0]) or (run[1] is not None and (cost is None or used[1] + cost > run[1])):
                raise ValueError('insufficient budget or unknown maximum cost')
            reservation = str(uuid.uuid4())
            self.db.execute('INSERT INTO reservations(id,run_id,tokens,cost) VALUES(?,?,?,?)', (reservation, run_id, tokens, cost))
        return reservation

    def settle(self, reservation, input_tokens=None, output_tokens=None, cost_usd=None, complete=True):
        error = None
        with self.transaction():
            held = self.db.execute('SELECT run_id,tokens,cost,settled FROM reservations WHERE id=?', (reservation,)).fetchone()
            if held is None or held[3]:
                raise ValueError('unknown or already settled reservation')
            try:
                tokens = integer(input_tokens) + integer(output_tokens)
                cost = money(cost_usd) if cost_usd is not None else None
                if tokens > held[1] or (held[2] is not None and (cost is None or cost > held[2])):
                    # Keep uncertain costs reserved, but never hide a known overrun.
                    self.db.execute('UPDATE reservations SET tokens=?,cost=? WHERE id=?',
                                    (max(tokens, held[1]), max(cost, held[2] or 0) if cost is not None else held[2], reservation))
                    raise ValueError('usage exceeds reservation or cost is unknown')
                self.db.execute('UPDATE reservations SET tokens=?,cost=?,settled=1 WHERE id=?', (tokens, cost, reservation))
            except (ValueError, ArithmeticError) as exc:
                error = str(exc)
            if error or not complete:
                self.db.execute('UPDATE runs SET blocked=1 WHERE id=?', (held[0],))
        if error:
            raise ValueError(error)

    def status(self, run_id):
        run = self.db.execute('SELECT token_cap,cost_cap,blocked FROM runs WHERE id=?', (run_id,)).fetchone()
        if run is None:
            raise ValueError('run missing')
        used = self.db.execute('SELECT COALESCE(SUM(tokens),0),COALESCE(SUM(cost),0),SUM(1-settled) FROM reservations WHERE run_id=?', (run_id,)).fetchone()
        return dict(max_tokens=run[0], max_cost_nanousd=run[1], blocked=bool(run[2]),
                    committed_tokens=used[0], committed_cost_nanousd=used[1], outstanding=used[2] or 0)


def preflight(runtime, mode, tokens=None, cost=None):
    capabilities = json.loads((ROOT / 'config/budget-capabilities.json').read_text())['runtimes']
    info = capabilities.get(runtime, {'enforced_units': [], 'reason': 'Runtime not verified.'})
    if tokens is not None:
        integer(tokens)
    if cost is not None:
        money(cost)
    required = ({'tokens'} if tokens is not None else set()) | ({'usd'} if cost is not None else set())
    enforced = bool(required) and required.issubset(set(info['enforced_units'])) and mode in info.get('verified_modes', [])
    return {'runtime': runtime, 'mode': mode, 'hard_requested': bool(required), 'enforced': enforced,
            'allowed': not required or enforced, 'reason': info['reason'],
            'alternative': 'Use adaptive execution without a hard cap, or a verified request-intercepting host using BudgetLedger.'}


def normalize(runtime, raw):
    """Normalize one completed event. Cached input is a subset, not an extra total."""
    usage = raw.get('usage')
    if runtime == 'local' and usage is None and 'stats' in raw:
        stats = raw['stats']
        usage = {'input_tokens': stats.get('input_tokens'), 'output_tokens': stats.get('total_output_tokens')}
    if runtime == 'gemini' and usage is None:
        models = raw.get('stats', {}).get('models', {})
        if models:
            tokens = [m.get('tokens', {}) for m in models.values()]
            if all('prompt' in t and 'candidates' in t and 'thoughts' in t for t in tokens):
                usage = {'input_tokens': sum(integer(t['prompt']) for t in tokens),
                         'output_tokens': sum(integer(t['candidates']) + integer(t['thoughts']) for t in tokens)}
    if not isinstance(usage, dict):
        return {'input_tokens': None, 'output_tokens': None, 'total_tokens': None, 'measured': False}
    incoming = usage.get('input_tokens', usage.get('prompt_tokens'))
    outgoing = usage.get('output_tokens', usage.get('completion_tokens'))
    if incoming is None or outgoing is None:
        return {'input_tokens': None, 'output_tokens': None, 'total_tokens': None, 'measured': False}
    incoming, outgoing = integer(incoming), integer(outgoing)
    if runtime == 'claude':
        # Claude's input_tokens excludes cache reads and writes.
        incoming += integer(usage.get('cache_read_input_tokens', 0)) + integer(usage.get('cache_creation_input_tokens', 0))
    return {'input_tokens': incoming, 'output_tokens': outgoing, 'total_tokens': incoming + outgoing, 'measured': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    check = sub.add_parser('preflight')
    check.add_argument('--runtime', required=True)
    check.add_argument('--mode', default='interactive')
    check.add_argument('--max-tokens', type=int)
    check.add_argument('--max-cost-usd')
    rec = sub.add_parser('record')
    rec.add_argument('--runtime', required=True)
    rec.add_argument('--run-id', required=True)
    rec.add_argument('--source', type=Path, required=True)
    rec.add_argument('--ledger', type=Path, required=True)
    rec.add_argument('--estimate-tokens', type=int)
    summary = sub.add_parser('summary')
    summary.add_argument('--ledger', type=Path, required=True)
    args = parser.parse_args()
    if args.action == 'preflight':
        result = preflight(args.runtime, args.mode, args.max_tokens, args.max_cost_usd)
        print(json.dumps(result))
        return 0 if result['allowed'] else 3
    if args.action == 'record':
        raw = json.loads(args.source.read_text())
        event = {'version': 1, 'event_id': raw.get('event_id', str(uuid.uuid4())),
                 'at': datetime.now(timezone.utc).isoformat(), 'run_id': args.run_id, 'runtime': args.runtime,
                 'source': 'runtime_usage', **normalize(args.runtime, raw)}
        if args.estimate_tokens is not None:
            event['estimated_tokens'] = integer(args.estimate_tokens)
        args.ledger.parent.mkdir(parents=True, exist_ok=True)
        # One append write preserves each small event across concurrent writers.
        with args.ledger.open('a') as stream:
            stream.write(json.dumps(event) + '\n')
        print(json.dumps(event))
    else:
        rows = [json.loads(line) for line in args.ledger.read_text().splitlines() if line.strip()]
        unique = {row['event_id']: row for row in rows}.values()
        measured = [r for r in unique if r.get('measured')]
        print(json.dumps({'measured_tokens': sum(r['total_tokens'] for r in measured),
                          'measured_events': len(measured), 'unknown_events': sum(not r.get('measured') for r in unique),
                          'estimated_tokens': sum(r.get('estimated_tokens', 0) for r in unique)}))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as error:
        raise SystemExit(str(error))
