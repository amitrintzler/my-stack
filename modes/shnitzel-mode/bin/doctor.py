#!/usr/bin/env python3
"""Report detected capabilities without claiming runtime acceptance."""
import json
from pathlib import Path
import shutil
import subprocess

home = Path.home()
engine = home / '.agents/shnitzel/engines/active'
report = {'version': 1, 'acceptance_report': str(Path(__file__).resolve().parents[1] / 'docs/acceptance.md'), 'engine': str(engine.resolve()) if engine.exists() else None, 'runtimes': {}}
for runtime, binary in [('claude', 'claude'), ('codex', 'codex'), ('gemini', 'gemini'), ('local', 'lms')]:
    executable, version = shutil.which(binary), None
    if executable:
        try:
            result = subprocess.run([executable, '--version'], capture_output=True, text=True, timeout=10)
            version = result.stdout.strip()[:120]
        except (OSError, subprocess.TimeoutExpired):
            pass
    report['runtimes'][runtime] = {'binary': executable, 'version': version, 'live_verified': False}
report['runtimes']['cowork'] = {'app_installed': Path('/Applications/Claude.app').exists(), 'live_verified': False}
print(json.dumps(report, indent=2))
