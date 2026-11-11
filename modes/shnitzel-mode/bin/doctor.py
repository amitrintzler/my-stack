#!/usr/bin/env python3
"""Report detected capabilities without claiming runtime acceptance."""
import json
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
report['runtimes']['cowork'] = {'app_installed': Path('/Applications/Claude.app').exists(), 'live_verified': False}
print(json.dumps(report, indent=2))
