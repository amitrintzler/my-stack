#!/usr/bin/env python3
"""Report detected capabilities without claiming runtime acceptance."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess

home = Path.home()
engine = home / '.agents/shnitzel/engines/active'
report = {'version': 1, 'acceptance_report': str(Path(__file__).resolve().parents[1] / 'docs/acceptance.md'), 'engine': str(engine.resolve()) if engine.exists() else None, 'runtimes': {}}
for runtime, binary in [('claude', 'claude'), ('codex', 'codex'), ('gemini', 'gemini'), ('cursor', 'cursor-agent'), ('local', 'lms')]:
    executable, version = shutil.which(binary), None
    if executable:
        try:
            result = subprocess.run([executable, '--version'], capture_output=True, text=True, timeout=10)
            version = result.stdout.strip()[:120]
        except (OSError, subprocess.TimeoutExpired):
            pass
    report['runtimes'][runtime] = {'binary': executable, 'version': version, 'live_verified': False}
# Cursor: the engine is Cursor's own pstack plugin, so report what Shnitzel can see of it.
# Cursor also scans ~/.agents/skills and ~/.claude/skills; a second shnitzel-mode or a
# port-translated poteto-mode there is listed beside the plugin's copies.
plugin = home / '.cursor/plugins/local/shnitzel-mode'
report['runtimes']['cursor'].update({
    'shnitzel_plugin': str(plugin.resolve()) if plugin.exists() else None,
    'pstack_models_rule': (home / '.cursor/rules/pstack-models.mdc').is_file(),
    'also_scanned_by_cursor': [str(d / name) for d in (home / '.agents/skills', home / '.claude/skills')
                               for name in ('shnitzel-mode', 'poteto-mode') if (d / name).exists()],
})
# Claude Code: pstack's hook reads a repository's committed .claude/pstack-models.md in place of
# the user sheet. Without its own `session hook: off`, pstack's mandate returns in that repository.
try:
    top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, timeout=10).stdout.strip()
except (OSError, subprocess.TimeoutExpired):
    top = ''
project_sheet = Path(top or Path.cwd()) / '.claude/pstack-models.md'
if project_sheet.is_file():
    lines = project_sheet.read_text(errors='replace').lstrip('﻿').splitlines()
    report['runtimes']['claude'].update({'project_sheet': str(project_sheet),
                                         'project_sheet_hook_off': 'session hook: off' in lines})
# Usage recording (Claude Code): on through the plugin's manifest hook or the installer's settings hook.
state = Path(os.environ.get('SHNITZEL_STATE') or home / '.agents/shnitzel')
usage_dir = state / 'usage'
settings_path = Path(os.environ.get('CLAUDE_CONFIG_DIR', str(home / '.claude'))) / 'settings.json'
try:
    settings = json.loads(settings_path.read_text()) if settings_path.is_file() else {}
except ValueError:
    settings = {}
settings_hooks = settings.get('hooks') if isinstance(settings, dict) and isinstance(settings.get('hooks'), dict) else {}
installer_hook = all(any('shnitzel-mode/scripts/usage.py' in str(h.get('command', '')) for e in settings_hooks.get(event, [])
                         if isinstance(e, dict) for h in e.get('hooks', []) if isinstance(h, dict))
                     for event in ('Stop', 'SubagentStop'))
plugins = settings.get('enabledPlugins') if isinstance(settings, dict) and isinstance(settings.get('enabledPlugins'), dict) else {}
plugin_enabled = any(name.split('@')[0] == 'shnitzel-mode' and on for name, on in plugins.items())
probe = usage_dir if usage_dir.exists() else next((d for d in usage_dir.parents if d.exists()), None)
ledgers = sorted(usage_dir.glob('ledger-*.jsonl')) if usage_dir.is_dir() else []
errors = usage_dir / 'errors.jsonl'
opted_out = os.environ.get('SHNITZEL_USAGE', '').lower() in ('off', '0', 'false') or (state / 'usage.off').exists()
report['runtimes']['claude']['usage'] = {
    'hook_active': (installer_hook or plugin_enabled) and not opted_out,
    'installer_hook': installer_hook, 'plugin_enabled': plugin_enabled, 'opted_out': opted_out,
    'ledger_dir': str(usage_dir), 'ledger_writable': bool(probe and os.access(probe, os.W_OK)),
    'ledger_files': len(ledgers), 'last_record_at': None,
    'hook_errors': sum(1 for _ in errors.open()) if errors.is_file() else 0}
if ledgers and ledgers[-1].stat().st_size:
    report['runtimes']['claude']['usage']['last_record_at'] = datetime.fromtimestamp(ledgers[-1].stat().st_mtime, timezone.utc).isoformat()
report['runtimes']['cowork'] = {'app_installed': Path('/Applications/Claude.app').exists(), 'live_verified': False}
print(json.dumps(report, indent=2))
