#!/usr/bin/env python3
"""Owned Shnitzel installation. Dry run unless --apply is supplied."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BEGIN, END = '<!-- shnitzel-mode:begin -->', '<!-- shnitzel-mode:end -->'
ROLES = ['feature, refactoring', 'bug-fix', 'perf-issue', 'hillclimb', 'judgment and prose', 'strongest judgment', 'how explorer', 'how explainer', 'why investigators', 'why synthesizer', 'reflect tooling', 'reflect judgment, divergent, synthesizer', 'swarm workers']
PANELS = ['arena runners', 'arena cross-judge pool', 'architect runners', 'interrogate reviewers']


def block(text, body):
    replacement = BEGIN + '\n' + body.strip() + '\n' + END if body else ''
    if text.count(BEGIN) != text.count(END) or text.count(BEGIN) > 1:
        raise ValueError('malformed or duplicate Shnitzel block')
    if BEGIN in text:
        return re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END), lambda _: replacement, text, flags=re.S)
    return text + ('\n' if text and not text.endswith('\n') else '') + replacement + ('\n' if replacement else '')


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def install(home, targets, apply=False, uninstall=False, engine=None, local_root=None, all_skills=False):
    state, skills = home / '.agents/shnitzel', home / '.agents/skills'
    own_path = state / 'install-ownership.json'
    own = json.loads(own_path.read_text()) if own_path.exists() else {'version': 1, 'links': {}, 'sheets': {}}
    if own.get('version') != 1:
        raise ValueError('unsupported ownership version')
    engine = engine or state / 'engines/active'
    own['links'] = {str(Path(k) if Path(k).is_absolute() else skills / k): v for k, v in own['links'].items()}
    rules = {'claude': Path(os.environ.get('CLAUDE_CONFIG_DIR', str(home / '.claude'))) / 'CLAUDE.md',
             'codex': Path(os.environ.get('CODEX_HOME', str(home / '.codex'))) / 'AGENTS.md',
             'gemini': home / '.gemini/GEMINI.md', 'cowork': state / 'cowork/START.md',
             'local': (local_root or Path.cwd()) / 'AGENTS.md'}
    sheets = {k: p.parent / 'pstack-models.md' for k, p in rules.items()}
    sheets['local'] = (local_root or Path.cwd()) / '.agents/pstack-models.md'
    writes, links, removes = {}, {}, []
    for target in targets:
        path, sheet = rules[target], sheets[target]
        before = path.read_text() if path.exists() else ''
        instruction = (f'Shnitzel admission: answer ordinary questions directly. '
                       'For implementation show brief meaningful approaches unless the user already selected one. '
                       'For a clear bounded reversible change this paragraph is sufficient: after the approach is selected, make the smallest change and verify its behavior. Do not read the full router or config for such focused work. Use no feature documents, delegates or unrequested commits. Risk overrides diff size. '
                       'Honor explicit task authorization and host/repository permissions. Explicit hard caps require verified enforcement.\n'
                       f'For standard/deep, uncertain or capped work read {skills}/shnitzel-mode/SKILL.md, then use relevant workflows at {engine}/plugins/pstack. Read model roles from {sheet} only when dispatching. '
                       'Read only relevant references. Explicit poteto-mode selects the full upstream workflow.')
        after = block(before, '' if uninstall else instruction)
        if before != after:
            writes[path] = after
        before = sheet.read_text() if sheet.exists() else ''
        if uninstall:
            held = own['sheets'].get(str(sheet))
            if held:
                if sha(before) != held['installed_sha256']:
                    raise ValueError('model sheet changed; preserve and remove managed hook setting manually: ' + str(sheet))
                if held['existed']:
                    writes[sheet] = held['original']
                else:
                    removes.append(sheet)
        else:
            defaults = '# pstack model configuration\n\n' + '\n'.join(r + ': inherit-parent' for r in ROLES)
            defaults += '\n' + '\n'.join(r + ': inherit-parent, inherit-parent' for r in PANELS) + '\ndefault effort: session\n'
            after = re.sub(r'^session hook:.*(?:\n|$)', '', before or defaults, flags=re.M).rstrip() + '\nsession hook: off\n'
            if before != after:
                writes[sheet] = after
                if str(sheet) not in own['sheets']:
                    own['sheets'][str(sheet)] = {'existed': sheet.exists(), 'original': before}
                own['sheets'][str(sheet)]['installed_sha256'] = sha(after)
    target_keys = {('local:' + str((local_root or Path.cwd()).resolve())) if t == 'local' else t for t in targets}
    installed_targets = set(own.get('runtimes', []))
    remaining_targets = installed_targets - target_keys if uninstall else installed_targets | target_keys
    if uninstall:
        removable_roots = ([skills] if not remaining_targets else [])
        if 'claude' in targets:
            removable_roots.append(rules['claude'].parent / 'skills')
        if 'gemini' in targets:
            removable_roots.append(home / '.gemini/skills')
        for name, dest in own['links'].items():
            link = Path(name)
            if link.parent in removable_roots and link.is_symlink() and os.readlink(link) == dest:
                removes.append(link)
    elif not uninstall:
        sources = list((ROOT / 'plugins/shnitzel-mode/skills').iterdir())
        if (engine / 'plugins/pstack/skills').exists():
            sources += list((engine / 'plugins/pstack/skills').iterdir())
        planned_names = {}
        for source in sources:
            if not (source / 'SKILL.md').is_file():
                continue
            if not all_skills and source.name not in {'shnitzel-mode', 'setup-shnitzel-mode', 'poteto-mode'}:
                continue
            if source.name in planned_names and planned_names[source.name] != str(source):
                raise ValueError('upstream/Shnitzel skill-name collision: ' + source.name)
            planned_names[source.name] = str(source)
            locations = [skills]
            if 'claude' in remaining_targets:
                locations.append(rules['claude'].parent / 'skills')
            if 'gemini' in remaining_targets:
                locations.append(home / '.gemini/skills')
            for location in locations:
                link, dest = location / source.name, str(source)
                if link.exists() or link.is_symlink():
                    if link.is_symlink() and os.readlink(link) == dest:
                        own['links'][str(link)] = dest
                        continue
                    if not (link.is_symlink() and own['links'].get(str(link)) == os.readlink(link)):
                        raise ValueError('skill collision; refusing to replace ' + str(link))
                links[str(link)] = dest
                own['links'][str(link)] = dest
        legacy, proposal = home / '.agents/model-roles.md', state / 'legacy-model-roles-proposal.md'
        if legacy.is_file() and not proposal.exists():
            writes[proposal] = '# Legacy roles, proposal only\n\nValidate models per runtime before importing. Original retained.\n\n' + legacy.read_text()
        conf = home / '.agents/watch.conf'
        if not conf.exists():
            writes[conf] = (ROOT / 'config/watch.example.conf').read_text()
    plan = {'writes': [str(p) for p in writes], 'links': dict(links),
            'removes': [str(p) for p in removes], 'engine_available': (engine / 'plugins/pstack/skills').is_dir(),
            'applied': apply, 'model_defaults': 'inherit parent, reduced diversity until configured'}
    if apply:
        backups = state / 'backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        for path, content in writes.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            if path.exists():
                backups.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, backups / (sha(str(path))[:12] + '-' + path.name))
            tmp = path.with_name(path.name + '.shnitzel-tmp')
            tmp.write_text(content)
            tmp.replace(path)
        for name, dest in links.items():
            link = Path(name)
            link.parent.mkdir(parents=True, exist_ok=True)
            link.unlink(missing_ok=True)
            link.symlink_to(dest)
        for path in removes:
            path.unlink(missing_ok=True)
        if uninstall:
            for target in targets:
                own['sheets'].pop(str(sheets[target]), None)
            own['links'] = {n: d for n, d in own['links'].items() if Path(n).is_symlink() and os.readlink(n) == d}
        state.mkdir(parents=True, exist_ok=True)
        own['runtimes'] = sorted(remaining_targets)
        tmp = own_path.with_suffix('.tmp')
        tmp.write_text(json.dumps(own, indent=2) + '\n')
        tmp.replace(own_path)
    return plan


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('runtime', nargs='?', choices=['all', 'claude', 'codex', 'gemini', 'cowork', 'local'], default='all')
    p.add_argument('--apply', action='store_true')
    p.add_argument('--uninstall', action='store_true')
    p.add_argument('--home', type=Path, default=Path.home())
    p.add_argument('--engine', type=Path)
    p.add_argument('--local-root', type=Path)
    p.add_argument('--all-skills', action='store_true', help='discover every optional skill; increases standing metadata')
    a = p.parse_args()
    targets = ['claude', 'codex', 'gemini', 'cowork'] if a.runtime == 'all' else [a.runtime]
    print(json.dumps(install(a.home, targets, a.apply, a.uninstall, a.engine, a.local_root, a.all_skills), indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        raise SystemExit(str(error))
