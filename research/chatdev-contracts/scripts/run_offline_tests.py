"""Run archived unit/integration tests with all socket connections blocked."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--variant', choices=['pure-contract', 'inline-contract'], default='inline-contract')
    args = parser.parse_args()
    source = ROOT / 'source' / args.variant
    os.environ.update(OPENAI_API_KEY='offline-test', CHATDEV_CONTENT_ENABLED='true',
                      MPST_A2A_ROOT=str(source), JEV_ENABLED='false', TEV_ENABLED='false', PYTHONDONTWRITEBYTECODE='1')
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(source), str(source / 'integrations/ChatDev1.0')]
    os.chdir(source / 'integrations/ChatDev1.0')
    attempted_network = []

    def deny_network(*args, **kwargs):
        attempted_network.append('blocked connection')
        raise AssertionError('Network is disabled during offline verification')

    socket.socket.connect = deny_network
    socket.socket.connect_ex = deny_network
    suite = unittest.TestSuite()
    for directory in ['tests_chatdev', 'tests']:
        suite.addTests(unittest.TestLoader().discover(str(source / directory)))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    manifest = json.loads((source / 'SOURCE_MANIFEST.json').read_text(encoding='utf-8'))
    mismatches = [name for name, sha in manifest['files'].items()
                  if hashlib.sha256((source / name).read_bytes()).hexdigest() != sha]
    report = {'variant': args.variant, 'tests_run': result.testsRun, 'failures': len(result.failures),
              'errors': len(result.errors), 'skipped': len(result.skipped), 'network_attempts': len(attempted_network),
              'source_mismatches': mismatches, 'passed': result.wasSuccessful() and not attempted_network and not mismatches}
    output = ROOT / 'output'
    output.mkdir(exist_ok=True)
    (output / f'{args.variant}-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
