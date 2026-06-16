#!/usr/bin/env python3
"""Integration helper for metadata-extractor.

This script invokes the existing extractor and returns a structured bridge output for other skill workflows.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACTOR = ROOT / '.skills' / 'metadata-extractor' / 'extract_metadata.py'


def slug(s):
    return ''.join(c if c.isalnum() else '-' for c in s.lower()).strip('-')


def call_extractor(topic, folders):
    if not EXTRACTOR.exists():
        raise FileNotFoundError(f"Metadata extractor not found at {EXTRACTOR}")

    args = [sys.executable, str(EXTRACTOR), '--topic', topic]
    for folder in folders:
        args.extend(['--folders', folder])
    # run the extractor from its own folder so .metadata is created there
    proc = subprocess.run(args, capture_output=True, text=True, cwd=str(EXTRACTOR.parent))
    if proc.returncode != 0:
        return {
            'status': 'error',
            'message': proc.stdout.strip() or proc.stderr.strip(),
            'stdout': proc.stdout,
            'stderr': proc.stderr,
        }

    citation_line = None
    # extractor writes metadata to its working folder under .metadata/<slug>.json
    metadata_path = EXTRACTOR.parent / '.metadata' / (slug(topic) + '.json')
    for line in proc.stdout.splitlines():
        if line.startswith('Source(s):'):
            citation_line = line[len('Source(s):'):].strip()
            break

    metadata_content = None
    if metadata_path.exists():
        try:
            metadata_content = json.loads(metadata_path.read_text(encoding='utf-8'))
        except Exception:
            metadata_content = None

    return {
        'status': 'success',
        'citation_line': citation_line or '',
        'metadata_path': str(metadata_path),
        'metadata': metadata_content or {},
        'stdout': proc.stdout,
        'stderr': proc.stderr,
    }


def main():
    parser = argparse.ArgumentParser(description='Call the metadata extractor and return integration output.')
    parser.add_argument('--topic', required=True)
    parser.add_argument('--folders', nargs='+', default=[
        str(ROOT / 'Training'),
        str(ROOT / 'Recognitions'),
        str(ROOT / 'CarMax Leadership'),
    ])
    args = parser.parse_args()

    result = call_extractor(args.topic, args.folders)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
