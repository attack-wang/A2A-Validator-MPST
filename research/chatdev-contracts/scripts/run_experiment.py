"""Run one fresh task with an archived adapter; this makes real model calls."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = {'baseline': 'chatdev-mpst', 'mpst': 'chatdev-mpst',
            'mpst_contract': 'pure-contract', 'inline_contract': 'inline-contract'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--condition', choices=list(VARIANTS), required=True)
    parser.add_argument('--index', type=int, required=True)
    parser.add_argument('--batch-name', required=True)
    parser.add_argument('--model', default='glm-5.3-flash:cloud')
    parser.add_argument('--base-url', default='http://127.0.0.1:11434/v1')
    parser.add_argument('--timeout', type=int, default=1500)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9._-]+', args.batch_name) or args.batch_name in {'.', '..'}:
        parser.error('batch-name must be a simple new directory name')
    if not 0 <= args.index < 30 or args.timeout <= 0:
        parser.error('index must be 0..29 and timeout must be positive')
    task = json.loads((ROOT / 'data/tasks.json').read_text(encoding='utf-8'))[args.index]
    source = ROOT / 'source' / VARIANTS[args.condition]
    chatdev = source / 'integrations/ChatDev1.0'
    output = source / 'benchmarks/programdev/runs' / args.batch_name / 'chatdev' / f"{args.index:02d}_{task['project_name']}"
    output.mkdir(parents=True, exist_ok=False)
    content = args.condition in {'mpst_contract', 'inline_contract'}
    env = os.environ.copy()
    env.update(OPENAI_API_KEY=env.get('OPENAI_API_KEY') or 'ollama', BASE_URL=args.base_url,
               CHATDEV_MODEL_NAME=args.model, CHATDEV_CONTEXT_LIMIT='32768', CHATDEV_MAX_TOKENS='8192',
               CHATDEV_REASONING_EFFORT='none', MPST_A2A_ROOT=str(source),
               CHATDEV_CONTENT_ENABLED='true' if content else 'false',
               CHATDEV_MPST_ENABLED='true' if args.condition != 'baseline' else 'false',
               CHATDEV_MPST_SCOPE='global', CHATDEV_MPST_MAX_RETRIES='2',
               JEV_ENABLED='false', TEV_ENABLED='false', PYTHONIOENCODING='utf-8',
               SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy')
    warehouse = chatdev / 'WareHouse'
    warehouse.mkdir(exist_ok=True)
    name = f"PD{args.index:02d}{task['project_name']}"
    prefix = f'{name}_{args.batch_name}_'
    existing = {p.name for p in warehouse.glob(prefix + '*')}
    command = [sys.executable, 'run.py', '--config', 'MPSTContent' if content else 'MPSTPilot',
               '--org', args.batch_name, '--task', task['description'], '--name', name, '--model', 'GPT_4O']
    start = time.monotonic()
    status, error = 'failed', None
    flags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
    with (output / 'console.log').open('w', encoding='utf-8') as stream:
        process = subprocess.Popen(command, cwd=chatdev, env=env, stdout=stream, stderr=subprocess.STDOUT,
                                   creationflags=flags, start_new_session=sys.platform != 'win32')
        try:
            code = process.wait(timeout=args.timeout)
            status = 'completed' if code == 0 else 'failed'
            error = f'exit code {code}' if code else None
        except subprocess.TimeoutExpired:
            if sys.platform == 'win32':
                subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True, creationflags=flags)
            else:
                import signal
                os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            status, error = 'timeout', f'exceeded {args.timeout} seconds'
    projects = sorted((p for p in warehouse.glob(prefix + '*') if p.name not in existing), key=lambda p: p.stat().st_mtime)
    result = {'task_index': args.index, 'project_name': task['project_name'], 'description': task['description'],
              'framework': 'ChatDev1.0', 'condition': args.condition, 'model': args.model, 'status': status,
              'error': error, 'elapsed_seconds': round(time.monotonic() - start, 3),
              'project_path': str(projects[-1]) if projects else None, 'artifact_pass': None,
              'content_contracts_enabled': content, 'session_type_enabled': args.condition != 'baseline',
              'model_decision_enabled': False, 'model_decision_calls': 0,
              'note': 'New publication runner; independent artifact evaluation has not run.'}
    (output / 'run_result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'result': str(output / 'run_result.json'), 'status': status}, ensure_ascii=False))
    return 0 if status == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
