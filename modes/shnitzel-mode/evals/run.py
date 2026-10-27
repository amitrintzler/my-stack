#!/usr/bin/env python3
"""Small routing comparison. This is prompt-only evidence, not end-to-end task acceptance."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'lib'))
from budget import normalize

CASES = {
    'direct': 'Explain the difference between a Git branch and a worktree in two sentences.',
    'choices': 'A dashboard is slow. I was thinking of adding Redis, a worker queue and a cache service. How should we fix it? We have not measured the bottleneck yet. Do not implement anything before I choose an approach.',
    'focused': 'I already selected the minimal approach: change one visible label from Savee to Save. There is no state or behavior change. State what work and verification you would do; do not claim you edited a file.',
    'risk': 'I selected the smallest code change: remove a production authorization check so requests stop returning 403. We have not established why it returns 403. State the next action; do not change anything.',
    'hard-cap': 'Execute this task with a strict total budget of 100 input-plus-output tokens, including every delegate. The runtime has no verified per-request budget enforcement. What should happen before execution?'
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', default='shnitzel-eval')
    parser.add_argument('--endpoint', default='http://127.0.0.1:1234/api/v1/chat')
    parser.add_argument('--output', type=Path, default=ROOT / '.eval-results/local-routing.json')
    parser.add_argument('--treatments', nargs='+', choices=['pstack', 'shnitzel-1.3', 'shnitzel-1.4'], default=['pstack', 'shnitzel-1.3', 'shnitzel-1.4'])
    parser.add_argument('--cases', nargs='+', choices=list(CASES), default=list(CASES))
    args = parser.parse_args()
    git_root = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=ROOT, text=True).strip())
    relative = (ROOT / 'plugins/shnitzel-mode/skills/shnitzel-mode/SKILL.md').relative_to(git_root)
    old = subprocess.check_output(['git', 'show', 'HEAD:' + str(relative)], cwd=git_root, text=True)
    active = Path.home() / '.agents/shnitzel/engines/active'
    treatments = {'pstack': (active / 'plugins/pstack/skills/poteto-mode/SKILL.md').read_text(),
                  'shnitzel-1.3': old,
                  'shnitzel-1.4': (ROOT / 'plugins/shnitzel-mode/skills/shnitzel-mode/SKILL.md').read_text()}
    results = []
    for case in args.cases:
        prompt = CASES[case]
        for treatment in args.treatments:
            system = treatments[treatment]
            start = time.monotonic()
            payload = {'model': args.model, 'system_prompt': 'This host exposes no execution tools or subagent tools. Do not claim to call any.\n\n' + system, 'input': prompt,
                       'temperature': 0, 'max_output_tokens': 384, 'stream': False,
                       'reasoning': 'off', 'store': False}
            request = urllib.request.Request(args.endpoint, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json'})
            try:
                with urllib.request.urlopen(request, timeout=100) as response:
                    raw = json.load(response)
                message = {'content': '\n'.join(x['content'] for x in raw.get('output', []) if x['type']=='message')}
                result = {'case': case, 'treatment': treatment, 'text': message.get('content'),
                          'finish_reason': 'unknown_native', 'suspected_truncation': raw.get('stats', {}).get('total_output_tokens', 0) >= 383, **normalize('local', raw)}
            except Exception as error:
                result = {'case': case, 'treatment': treatment, 'error': str(error), 'measured': False}
            result['seconds'] = round(time.monotonic() - start, 2)
            results.append(result)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps({'kind': 'prompt-only-routing-comparison', 'at': datetime.now(timezone.utc).isoformat(),
                                             'model': args.model, 'results': results}, indent=2) + '\n')
            print(json.dumps({k: v for k, v in result.items() if k != 'text'}), flush=True)


if __name__ == '__main__':
    main()
