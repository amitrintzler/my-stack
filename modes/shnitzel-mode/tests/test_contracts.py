import concurrent.futures
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'lib'))
import budget
import digest
import install
import upstream


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'budget.sqlite'
        self.ledger = budget.BudgetLedger(self.path)
        self.addCleanup(self.ledger.db.close)

    def test_concurrent_reservations_share_budget(self):
        self.ledger.create('task', max_tokens=100)
        def reserve(_):
            ledger = budget.BudgetLedger(self.path)
            try:
                ledger.reserve('task', 30, 30)
                return True
            except ValueError:
                return False
            finally:
                ledger.db.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            self.assertEqual(sum(pool.map(reserve, range(4))), 1)
        self.assertEqual(self.ledger.status('task')['committed_tokens'], 60)

    def test_settle_returns_unused_and_incomplete_blocks(self):
        self.ledger.create('task', 100, '0.03')
        first = self.ledger.reserve('task', 20, 30, '0.02')
        self.ledger.settle(first, 20, 10, '0.01')
        second = self.ledger.reserve('task', 30, 20, '0.02')
        self.ledger.settle(second, 30, 5, '0.01', complete=False)
        self.assertTrue(self.ledger.status('task')['blocked'])
        with self.assertRaises(ValueError):
            self.ledger.reserve('task', 1, 1, '0')

    def test_unknown_usage_keeps_reservation_and_blocks(self):
        self.ledger.create('task', 100)
        held = self.ledger.reserve('task', 10, 20)
        with self.assertRaises(ValueError):
            self.ledger.settle(held)
        self.assertEqual(self.ledger.status('task')['committed_tokens'], 30)
        self.assertTrue(self.ledger.status('task')['blocked'])

    def test_overshoot_blocks_and_double_settlement_rejected(self):
        self.ledger.create('task', 100)
        held = self.ledger.reserve('task', 10, 20)
        with self.assertRaises(ValueError):
            self.ledger.settle(held, 10, 21)
        self.assertTrue(self.ledger.status('task')['blocked'])
        self.ledger.create('other', 100)
        held = self.ledger.reserve('other', 10, 20)
        self.ledger.settle(held, 10, 10)
        with self.assertRaises(ValueError):
            self.ledger.settle(held, 10, 10)

    def test_unknown_cost_cannot_reserve_dollar_budget(self):
        self.ledger.create('task', max_cost_usd='0.01')
        with self.assertRaises(ValueError):
            self.ledger.reserve('task', 1, 1)

    def test_native_hard_cap_requests_fail_before_execution(self):
        for runtime in ['claude', 'codex', 'cowork', 'gemini', 'local']:
            self.assertFalse(budget.preflight(runtime, 'interactive', 100)['allowed'])
            self.assertTrue(budget.preflight(runtime, 'interactive')['allowed'])

    def test_normalization_preserves_unknown_and_avoids_double_counting(self):
        self.assertIsNone(budget.normalize('cowork', {})['total_tokens'])
        raw = {'usage': {'input_tokens': 100, 'cached_input_tokens': 60, 'output_tokens': 20}}
        self.assertEqual(budget.normalize('codex', raw)['total_tokens'], 120)
        raw['usage'].update(cache_read_input_tokens=30, cache_creation_input_tokens=10)
        self.assertEqual(budget.normalize('claude', raw)['total_tokens'], 160)
        self.assertEqual(budget.normalize('gemini', {'stats': {'models': {'m': {'tokens': {'prompt': 10, 'candidates': 5, 'thoughts': 2}}}}})['total_tokens'], 17)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='shnitzel home ')
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.env = patch.dict(os.environ, {'CLAUDE_CONFIG_DIR': str(self.home / '.claude'), 'CODEX_HOME': str(self.home / '.codex')})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_dry_run_no_files(self):
        install.install(self.home, ['claude', 'codex'])
        self.assertEqual(list(self.home.iterdir()), [])

    def test_idempotency_preserves_rules_and_user_model_choices(self):
        rules = self.home / '.claude/CLAUDE.md'
        rules.parent.mkdir()
        rules.write_text('Personal instructions\n')
        sheet = rules.parent / 'pstack-models.md'
        sheet.write_text('judgment and prose: chosen-model\nsession hook: on\n')
        install.install(self.home, ['claude'], apply=True)
        result = install.install(self.home, ['claude'], apply=True)
        self.assertEqual(result['writes'], [])
        self.assertEqual(result['links'], {})
        self.assertIn('chosen-model', sheet.read_text())
        self.assertIn('session hook: off', sheet.read_text())
        rules.write_text(rules.read_text() + 'Later unrelated rule\n')
        install.install(self.home, ['claude'], apply=True, uninstall=True)
        self.assertIn('Personal instructions', rules.read_text())
        self.assertIn('Later unrelated rule', rules.read_text())
        self.assertNotIn(install.BEGIN, rules.read_text())
        self.assertEqual(sheet.read_text(), 'judgment and prose: chosen-model\nsession hook: on\n')

    def test_collision_does_not_partially_modify_rules(self):
        collision = self.home / '.agents/skills/shnitzel-mode'
        collision.mkdir(parents=True)
        (collision / 'SKILL.md').write_text('owned by somebody else')
        with self.assertRaisesRegex(ValueError, 'collision'):
            install.install(self.home, ['codex'], apply=True)
        self.assertFalse((self.home / '.codex').exists())
        self.assertTrue(collision.exists())

    def test_uninstall_does_not_delete_foreign_link_or_other_runtime(self):
        install.install(self.home, ['claude', 'codex'], apply=True)
        link = self.home / '.agents/skills/shnitzel-mode'
        install.install(self.home, ['codex'], apply=True, uninstall=True)
        self.assertTrue(link.is_symlink())
        link.unlink()
        link.symlink_to(self.home / 'foreign')
        install.install(self.home, ['claude'], apply=True, uninstall=True)
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), str(self.home / 'foreign'))

    def test_modified_model_sheet_blocks_uninstall_before_any_write(self):
        install.install(self.home, ['codex'], apply=True)
        sheet = self.home / '.codex/pstack-models.md'
        sheet.write_text(sheet.read_text() + 'custom: new\n')
        with self.assertRaisesRegex(ValueError, 'model sheet changed'):
            install.install(self.home, ['codex'], apply=True, uninstall=True)
        self.assertIn(install.BEGIN, (self.home / '.codex/AGENTS.md').read_text())

    def test_marked_block_updates_instead_of_duplicate(self):
        old = 'Keep\n' + install.BEGIN + '\nold policy\n' + install.END + '\nOther\n'
        updated = install.block(old, 'new policy')
        self.assertNotIn('old policy', updated)
        self.assertEqual(updated.count(install.BEGIN), 1)
        self.assertIn('Other', updated)

    def test_native_discovery_roots_and_partial_uninstall(self):
        install.install(self.home, ['claude', 'gemini'], apply=True)
        claude = self.home / '.claude/skills/shnitzel-mode'
        gemini = self.home / '.gemini/skills/shnitzel-mode'
        shared = self.home / '.agents/skills/shnitzel-mode'
        self.assertTrue(claude.is_symlink())
        self.assertTrue(gemini.is_symlink())
        install.install(self.home, ['claude'], apply=True, uninstall=True)
        self.assertFalse(claude.is_symlink())
        self.assertTrue(gemini.is_symlink())
        self.assertTrue(shared.is_symlink())

    def test_two_local_projects_do_not_lose_shared_links(self):
        first, second = self.home / 'first', self.home / 'second'
        install.install(self.home, ['local'], apply=True, local_root=first)
        install.install(self.home, ['local'], apply=True, local_root=second)
        install.install(self.home, ['local'], apply=True, uninstall=True, local_root=first)
        self.assertTrue((self.home / '.agents/skills/shnitzel-mode').is_symlink())
        self.assertIn(install.BEGIN, (second / 'AGENTS.md').read_text())


class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.bin = self.home / 'bin'
        self.bin.mkdir()
        self.config = self.home / 'watch.conf'
        self.config.write_text('REPOS="example/demo"\nCHECK_SECURITY=0\n')
        self.env = dict(os.environ, HOME=str(self.home), PATH=str(self.bin) + os.pathsep + os.environ['PATH'])

    def gh(self, check='pending', unavailable=False):
        fake = self.bin / 'gh'
        fake.write_text('''#!/usr/bin/env python3
import json,sys
args=sys.argv[1:]
if UNAVAILABLE: sys.exit(1)
if args[:2]==['run','list']:
 print('[]')
elif args[:2]==['pr','list']:
 c = CHECK
 checks=[] if c=='missing' else [{'status':'COMPLETED' if c=='success' else 'IN_PROGRESS','conclusion':'SUCCESS' if c=='success' else None}]
 print(json.dumps([{'number':1,'title':'demo','url':'https://example.test/pr','updatedAt':'2099-01-01T00:00:00Z','isDraft':False,'mergeStateStatus':'CLEAN','reviewDecision':'APPROVED','headRefOid':'abc','statusCheckRollup':checks}]))
elif args[:2]==['api','graphql']:
 print('{"data":{"repository":{"pullRequest":{"reviewThreads":{"nodes":[]}}}}}')
else: print('[]')
'''.replace('UNAVAILABLE', repr(unavailable)).replace('CHECK', repr(check)))
        fake.chmod(0o755)

    def collect(self):
        result = subprocess.run([str(ROOT / 'bin/gh-collect.sh'), '--config', str(self.config), '--all', '--no-state'], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_pending_and_missing_checks_never_green(self):
        for status in ['pending', 'missing']:
            self.gh(status)
            result = self.collect()
            self.assertNotIn('my_pr_ready', [i['kind'] for i in result['items']])
        self.assertFalse((self.home / '.agents/watch-state.json').exists())

    def test_completed_success_is_ready(self):
        self.gh('success')
        self.assertIn('my_pr_ready', [i['kind'] for i in self.collect()['items']])

    def test_api_failure_is_incomplete(self):
        self.gh(unavailable=True)
        self.assertEqual(self.collect()['coverage']['status'], 'incomplete')

    def test_failed_or_malformed_collector_is_not_empty_healthy(self):
        collector = self.bin / 'feature-scan.sh'
        collector.write_text('#!/bin/sh\nprintf broken\n')
        collector.chmod(0o755)
        items, coverage, _ = digest.collect('feature-scan', [], self.bin)
        self.assertEqual(items[0]['kind'], 'collector_unavailable')
        self.assertEqual(coverage['status'], 'unavailable')

    def test_sealed_vault_exit_two_still_reports_sealed(self):
        vault = self.bin / 'vault'
        vault.write_text('#!/bin/sh\nprintf \'%s\\n\' \'{"sealed":true}\'\nexit 2\n')
        vault.chmod(0o755)
        self.config.write_text('DOMAINS="vault"\n')
        result = subprocess.run([str(ROOT / 'bin/domain-scan.sh'), '--config', str(self.config), '--coverage'], env=self.env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIn('vault_sealed', [i['kind'] for i in data['items']])
        self.assertEqual(data['coverage']['status'], 'observed')

    def test_invalid_vault_schema_is_not_healthy(self):
        vault = self.bin / 'vault'
        vault.write_text("#!/bin/sh\nprintf '%s\\n' '{}'\n")
        vault.chmod(0o755)
        self.config.write_text('DOMAINS="vault"\n')
        result = subprocess.run([str(ROOT / 'bin/domain-scan.sh'), '--config', str(self.config), '--coverage'], env=self.env, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout)['coverage']['status'], 'incomplete')


class CoworkPackageTests(unittest.TestCase):
    def test_payload_is_self_contained_and_preserves_previous(self):
        spec = importlib.util.spec_from_file_location('cowork_package', ROOT / 'bin/cowork-package.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            engine = temp / 'engine'
            skill = engine / 'plugins/pstack/skills/demo/SKILL.md'
            skill.parent.mkdir(parents=True)
            skill.write_text('Demo skill')
            (engine / 'shnitzel-manifest.json').write_text('{}')
            output = temp / 'cowork'
            module.package(output, engine)
            self.assertEqual((output / 'plugins/pstack/skills/demo/SKILL.md').read_text(), 'Demo skill')
            self.assertFalse(any(p.is_symlink() for p in output.rglob('*')))
            self.assertIn('No host-home paths', (output / 'START.md').read_text())
            module.package(output, engine)
            self.assertTrue((temp / 'cowork.previous/.shnitzel-owned').exists())

    def test_foreign_destination_is_never_replaced(self):
        spec = importlib.util.spec_from_file_location('cowork_package', ROOT / 'bin/cowork-package.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / 'user-folder'
            destination.mkdir()
            (destination / 'user.txt').write_text('keep')
            with self.assertRaises(ValueError):
                module.package(destination, Path(temp) / 'missing-engine')
            self.assertEqual((destination / 'user.txt').read_text(), 'keep')


class UpstreamTests(unittest.TestCase):
    def test_unresolved_conflict_blocks_validation(self):
        with tempfile.TemporaryDirectory() as temp:
            candidate = Path(temp)
            path = candidate / 'plugins/pstack/skills/demo/SKILL.md'
            path.parent.mkdir(parents=True)
            path.write_text('<<<<<<< local\nconflict\n=======\nupstream\n>>>>>>> upstream\n')
            with self.assertRaisesRegex(ValueError, 'unresolved conflict'):
                upstream.validate(candidate)

    def test_activation_and_rollback_preserve_old_engine(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp)
            old, new = state / 'old', state / 'new'
            old.mkdir(); new.mkdir()
            upstream.activate(old, state)
            upstream.activate(new, state)
            self.assertEqual((state / 'previous').resolve(), old.resolve())
            self.assertTrue(old.exists())
            previous = (state / 'previous').resolve()
            upstream.activate(previous, state)
            self.assertEqual((state / 'active').resolve(), old.resolve())
            self.assertEqual((state / 'previous').resolve(), new.resolve())


if __name__ == '__main__':
    unittest.main()
