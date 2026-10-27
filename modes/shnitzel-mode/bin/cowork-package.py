#!/usr/bin/env python3
"""Build a self-contained connected-folder payload; no host-home links inside."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def package(destination, engine):
    if destination.exists() and not (destination / '.shnitzel-owned').is_file():
        raise ValueError('destination is not an owned Shnitzel payload')
    if not (engine / 'shnitzel-manifest.json').is_file():
        raise ValueError('validated engine missing')
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as temp:
        folder = Path(temp) / 'payload'
        folder.mkdir()
        shutil.copytree(engine / 'plugins/pstack', folder / 'plugins/pstack', symlinks=False)
        shutil.copytree(ROOT / 'plugins/shnitzel-mode', folder / 'plugins/shnitzel-mode', symlinks=False)
        for name in ['effort-policy.json', 'budget-capabilities.json', 'upstream-lock.json']:
            (folder / 'config').mkdir(exist_ok=True)
            shutil.copy2(ROOT / 'config' / name, folder / 'config' / name)
        for name in ['lib/budget.py', 'bin/budget.py']:
            path = folder / name
            path.parent.mkdir(exist_ok=True)
            shutil.copy2(ROOT / name, path)
        for path in engine.glob('*'):
            if path.is_file() and path.name.startswith(('LICENSE', 'NOTICE')):
                shutil.copy2(path, folder / path.name)
        shutil.copy2(ROOT / 'NOTICE.md', folder / 'NOTICE-shnitzel.md')
        (folder / 'START.md').write_text('''# Shnitzel connected-folder entry

Treat this folder as the distribution root. Answer ordinary questions directly. For a clear bounded reversible edit, offer brief approaches unless already selected, make the smallest chosen change and verify it. No full router, feature documents or delegates are needed for focused work. Risk overrides diff size.

For uncertain, standard/deep or capped work read plugins/shnitzel-mode/skills/shnitzel-mode/SKILL.md. Pstack is at plugins/pstack. Nested skills are loaded by their actual files when native invocation is unavailable. No host-home paths are required. Explicit hard caps are unsupported until the native capability registry is independently verified. Scheduled work is read-only.

Runtime model roles must be configured using reachable models in this Cowork session. Host CLI model availability does not prove Cowork access. Do not invent calls or claim verification without observing the result.
''')
        (folder / '.shnitzel-owned').write_text('version: 1\n')
        if destination.exists():
            previous = destination.with_name(destination.name + '.previous')
            if previous.exists():
                if not (previous / '.shnitzel-owned').is_file():
                    raise ValueError('previous payload is not owned')
                shutil.rmtree(previous)
            destination.rename(previous)
        shutil.move(str(folder), destination)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '.runtime/cowork')
    parser.add_argument('--engine', type=Path, default=Path.home() / '.agents/shnitzel/engines/active')
    args = parser.parse_args()
    print(package(args.output, args.engine))
