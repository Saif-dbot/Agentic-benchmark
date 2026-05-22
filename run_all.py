"""run_all.py
Orchestrate benchmark runs for multiple frameworks and then run analysis.
Usage: python run_all.py --frameworks langchain crewai --repeats 2 --mode mock
"""
import argparse
import subprocess
import sys
import os

ROOT = os.path.dirname(__file__)
BENCH = os.path.join(ROOT, 'bench', 'benchmark.py')
ANALYZE = os.path.join(ROOT, 'bench', 'analyze.py')


def run_framework(framework, repeats, mode, output_dir, timeout, log_level):
    cmd = [
        sys.executable,
        BENCH,
        '--adapter',
        framework,
        '--repeats',
        str(repeats),
        '--mode',
        mode,
        '--output-dir',
        output_dir,
        '--timeout',
        str(timeout),
        '--log-level',
        log_level,
    ]
    print('Running:', ' '.join(cmd))
    res = subprocess.run(cmd)
    return res.returncode


def run_analysis(logs_dir, output_dir):
    cmd = [sys.executable, ANALYZE, '--logs-dir', logs_dir, '--output-dir', output_dir]
    print('Running analysis:', ' '.join(cmd))
    return subprocess.run(cmd).returncode


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--frameworks', nargs='+', default=['langchain'], help='List of frameworks to run')
    p.add_argument('--repeats', type=int, default=1)
    p.add_argument('--mode', choices=['mock', 'real'], default='mock')
    p.add_argument('--output-dir', default='logs')
    p.add_argument('--verbose', action='store_true')
    p.add_argument('--log-level', default='INFO')
    p.add_argument('--timeout', type=int, default=60)
    args = p.parse_args()

    if args.verbose:
        print('Verbose mode enabled')

    for framework in args.frameworks:
        print('=== Framework:', framework)
        code = run_framework(
            framework=framework,
            repeats=args.repeats,
            mode=args.mode,
            output_dir=args.output_dir,
            timeout=args.timeout,
            log_level=args.log_level,
        )
        if code != 0:
            print('Framework run failed:', framework)
        else:
            print('Framework completed:', framework)

    print('=== Running analysis ===')
    run_analysis(args.output_dir, 'results')
    print('All done.')
