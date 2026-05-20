"""run_all.py
Simple runner to execute benchmark for multiple adapters and then run analysis.
Usage: python run_all.py --adapters mock openai --repeats 2
"""
import argparse
import subprocess
import sys
import os

ROOT = os.path.dirname(__file__)
BENCH = os.path.join(ROOT, 'bench', 'benchmark.py')
ANALYZE = os.path.join(ROOT, 'bench', 'analyze.py')


def run_adapter(adapter, repeats):
    cmd = [sys.executable, BENCH, '--adapter', adapter, '--repeats', str(repeats)]
    print('Running:', ' '.join(cmd))
    res = subprocess.run(cmd)
    return res.returncode


def run_analysis():
    cmd = [sys.executable, ANALYZE]
    print('Running analysis:', ' '.join(cmd))
    return subprocess.run(cmd).returncode


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--adapters', nargs='+', default=['mock'], help='List of adapters to run')
    p.add_argument('--repeats', type=int, default=1)
    args = p.parse_args()

    for a in args.adapters:
        print('=== Adapter:', a)
        code = run_adapter(a, args.repeats)
        if code != 0:
            print('Adapter run failed:', a)
    print('=== Running analysis ===')
    run_analysis()
    print('All done.')
