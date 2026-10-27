#!/usr/bin/env python3
"""Build a pinned pstack candidate; activate only after compatibility validation."""
import argparse
import hashlib
import io
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PORT = 'michael-denyer/pstack-claude'
ORIGINAL = 'cursor/plugins'


def bun():
    binary = os.environ.get('SHNITZEL_BUN') or shutil.which('bun')
    cached = Path.home() / '.cache/shnitzel/toolchain/node_modules/.bin/bun'
    if binary:
        return binary
    if cached.exists():
        return str(cached)
    raise ValueError('bun required for upstream generator; install bun or set SHNITZEL_BUN')


def api(repo, path):
    req = urllib.request.Request('https://api.github.com/repos/' + repo + '/' + path,
                                 headers={'User-Agent': 'shnitzel-upstream-check'})
    with urllib.request.urlopen(req, timeout=40) as response:
        return json.load(response)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2) + '\n')
    tmp.replace(path)


def snapshot(repo, sha, cache, prefix=None):
    dest = cache / (repo.replace('/', '__') + '-' + sha)
    if (dest / '.complete').exists():
        return dest
    cache.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=cache) as scratch:
        scratch = Path(scratch)
        req = urllib.request.Request(f'https://codeload.github.com/{repo}/tar.gz/{sha}',
                                     headers={'User-Agent': 'shnitzel-upstream-check'})
        with urllib.request.urlopen(req, timeout=120) as response:
            raw = response.read()
        with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
            for member in archive:
                parts = Path(member.name).parts[1:]
                if not parts or (prefix and parts[0] != prefix):
                    continue
                if '..' in parts or Path(*parts).is_absolute():
                    raise ValueError('unsafe archive path')
                target = scratch.joinpath(*parts)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                elif member.isfile():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.extractfile(member) as source:
                        target.write_bytes(source.read())
                    target.chmod(0o755 if member.mode & 0o111 else 0o644)
                elif member.issym():
                    resolved = (target.parent / member.linkname).resolve()
                    if not resolved.is_relative_to(scratch.resolve()):
                        raise ValueError('archive symlink escapes source')
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.symlink_to(member.linkname)
                else:
                    raise ValueError('unsupported archive entry')
        (scratch / '.complete').write_text(sha + '\n')
        shutil.move(str(scratch), dest)
    return dest


def resolve():
    release = api(PORT, 'releases/latest')
    tag = release['tag_name']
    port_sha = api(PORT, 'commits/' + tag)['sha']
    original_sha = api(ORIGINAL, 'commits?path=pstack&per_page=1')[0]['sha']
    return {'port': {'repository': PORT, 'tag': tag, 'sha': port_sha},
            'original': {'repository': ORIGINAL, 'sha': original_sha}}


def run(command, cwd=None):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(' '.join(map(str, command)) + '\n' + result.stdout[-4000:] + result.stderr[-4000:])
    return result.stdout


def validate(candidate):
    plugin = candidate / 'plugins/pstack'
    for path in plugin.rglob('*'):
        if path.is_symlink() and not path.resolve().is_relative_to(candidate.resolve()):
            raise ValueError('engine symlink escapes candidate')
        if path.is_file() and path.suffix in ('.md', '.mjs', '.ts', '.sh', '.json'):
            text = path.read_text(errors='replace')
            if any(line.startswith(('<<<<<<< ', '=======', '>>>>>>> ')) for line in text.splitlines()):
                raise ValueError('unresolved conflict: ' + str(path.relative_to(candidate)))
    for skill in (ROOT / 'plugins/shnitzel-mode/skills').rglob('*.md'):
        for name in set(re.findall(r'pstack:([a-z][a-z-]+)', skill.read_text())):
            if not (plugin / 'skills' / name / 'SKILL.md').is_file():
                raise ValueError('Shnitzel references missing upstream skill: ' + name)
    run([bun(), 'tools/generate.mjs'], candidate)
    run([bun(), 'tools/generate.mjs', '--check'], candidate)
    run(['node', str(plugin / 'skills/poteto-mode/scripts/check-playbooks.mjs'), str(ROOT.parents[1])])


def adapt_reference(candidate, report):
    """The port validates this inventory but does not generate new command rows."""
    path = candidate / 'docs/reference.md'
    text = path.read_text()
    added = []
    refreshed = []
    changed = {Path(entry['rel']).parent.name for entry in report['written'] if entry['rel'].endswith('/SKILL.md')}
    for skill in sorted((candidate / 'plugins/pstack/skills').glob('*/SKILL.md')):
        name = skill.parent.name
        if name.startswith('principle-') or (f'`/{name}`' in text and name not in changed):
            continue
        description = next((line.split(':', 1)[1].strip().strip('"') for line in skill.read_text().splitlines()
                            if line.startswith('description:')), 'See the skill instructions.')
        row = '| `/' + name + '` | ' + description.replace('|', '\\|') + ' |\n'
        if f'`/{name}`' in text:
            text = re.sub(r'^\| `/' + re.escape(name) + r'` \|.*$', lambda _: row.rstrip(), text, flags=re.M)
            refreshed.append(name)
        else:
            text = text.replace('\n## Runtime support', row + '\n## Runtime support', 1)
            added.append(name)
    skills = list((candidate / 'plugins/pstack/skills').glob('*/SKILL.md'))
    principles = sum(s.parent.name.startswith('principle-') for s in skills)
    text = re.sub(r'The package includes \d+ skill directories: \d+ public skills and \d+',
                  f'The package includes {len(skills)} skill directories: {len(skills)-principles} public skills and {principles}', text)
    path.write_text(text)
    return {'added': added, 'refreshed': refreshed, 'skill_count': len(skills)}


def apply_resolutions(candidate, report, original_sha):
    registry = ROOT / 'patches/upstream/resolutions.json'
    resolutions = json.loads(registry.read_text()) if registry.exists() else []
    applied = []
    for entry in resolutions:
        path = candidate / entry['path']
        if entry['original_sha'] != original_sha:
            continue
        if not path.is_file() or digest(path) != entry['expected_sha256']:
            raise ValueError('resolution base changed: ' + entry['path'])
        replacement = ROOT / 'patches/upstream' / entry['replacement']
        if digest(replacement) != entry['replacement_sha256']:
            raise ValueError('resolution content changed: ' + entry['path'])
        shutil.copyfile(replacement, path)
        applied.append(entry['path'])
    return applied


def build(selection, state, cache):
    pristine = snapshot(PORT, selection['port']['sha'], cache)
    spec = json.loads((pristine / 'tools/upstream.json').read_text())['components']['pstack']
    base = snapshot(ORIGINAL, spec['sha'], cache, 'pstack')
    latest = snapshot(ORIGINAL, selection['original']['sha'], cache, 'pstack')
    name = selection['port']['tag'] + '-' + selection['original']['sha'][:12]
    candidates = state / 'candidates'
    candidates.mkdir(parents=True, exist_ok=True)
    candidate = Path(tempfile.mkdtemp(prefix=name + '-', dir=candidates))
    shutil.copytree(pristine, candidate, symlinks=True, dirs_exist_ok=True)
    run(['npm', 'install', '--ignore-scripts', '--no-audit', '--no-fund', '--omit=optional'], candidate)
    report_file = candidate / 'shnitzel-sync-report.json'
    result = subprocess.run([bun(), str(ROOT / 'lib/sync-upstream.mjs'), str(candidate),
                             str(base / 'pstack'), str(latest / 'pstack'), str(report_file)],
                            text=True, capture_output=True)
    if not report_file.exists():
        raise RuntimeError(result.stderr or result.stdout)
    report = json.loads(report_file.read_text())
    if result.returncode:
        raise RuntimeError('upstream sync blocked; inspect ' + str(report_file) + '\n' + result.stderr[-2000:])
    applied = apply_resolutions(candidate, report, selection['original']['sha'])
    unresolved = [entry for entry in report['conflicts'] if 'plugins/pstack/' + entry['rel'] not in applied]
    if unresolved:
        raise ValueError('unresolved upstream conflicts; inspect ' + str(report_file))
    reference_rows = adapt_reference(candidate, report)
    validate(candidate)
    original_version = json.loads((latest / 'pstack/plugin.json').read_text())['version']
    manifest = {'version': 1, **selection, 'original_version': original_version,
                'port_original_pin': spec['sha'], 'resolutions': applied,
                'port_adaptations': {'reference_inventory': reference_rows},
                'changed_files': report['written'], 'deleted_files': report['deleted'],
                'excluded_paths': spec['exclude'], 'excluded_reason': 'Port runtime exclusions; original retained in pristine snapshot.',
                'checks': ['upstream-three-way-sync', 'generator', 'generator-check', 'project-playbooks'],
                'policy': 'Shnitzel admission precedes pstack; explicit poteto-mode retains full workflow.'}
    dump(candidate / 'shnitzel-manifest.json', manifest)
    return candidate, manifest


def activate(candidate, state):
    active, previous = state / 'active', state / 'previous'
    if active.exists() and not active.is_symlink():
        raise ValueError('active engine is not an owned symlink')
    if previous.exists() and not previous.is_symlink():
        raise ValueError('previous engine is not an owned symlink')
    if active.is_symlink():
        previous.unlink(missing_ok=True)
        previous.symlink_to(active.resolve())
    next_link = state / 'active.next'
    next_link.unlink(missing_ok=True)
    next_link.symlink_to(candidate.resolve())
    next_link.replace(active)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument('--check', action='store_true')
    action.add_argument('--build', action='store_true', help='build and validate without activation')
    action.add_argument('--apply', action='store_true')
    action.add_argument('--rollback', action='store_true')
    parser.add_argument('--locked', action='store_true', help='use recorded exact revisions offline after source caching')
    parser.add_argument('--state-dir', type=Path, default=Path.home() / '.agents/shnitzel/engines')
    parser.add_argument('--cache-dir', type=Path, default=Path.home() / '.cache/shnitzel/sources')
    args = parser.parse_args()
    lock = ROOT / 'config/upstream-lock.json'
    if args.rollback:
        previous = args.state_dir / 'previous'
        if not previous.is_symlink() or not previous.resolve().exists():
            parser.error('no previous engine')
        activate(previous.resolve(), args.state_dir)
        print('restored ' + str((args.state_dir / 'active').resolve()))
        return
    selection = json.loads(lock.read_text()) if args.locked else resolve()
    if selection.get('version', 1) != 1 or any(not re.fullmatch(r'[0-9a-f]{40}', selection[key]['sha']) for key in ['port', 'original']):
        raise ValueError('unsupported lock version or invalid source revision')
    if not (args.apply or args.build):
        print(json.dumps({'latest': selection, 'locked': json.loads(lock.read_text()) if lock.exists() else None}, indent=2))
        return
    candidate, manifest = build(selection, args.state_dir, args.cache_dir)
    if args.apply:
        activate(candidate, args.state_dir)
        dump(lock, manifest)
    print(json.dumps({'candidate': str(candidate), 'activated': args.apply, 'manifest': manifest}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError) as error:
        raise SystemExit(str(error))
