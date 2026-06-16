#!/usr/bin/env python3
"""Generate a recognition message using metadata from the extractor.

Usage:
  python generate_recognition.py --topic "pre-trip inspection" --who "Alex"
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
EXTRACTOR_META = ROOT / '.skills' / 'metadata-extractor' / '.metadata'
INTEGRATOR = ROOT / '.skills' / 'metadata-integration' / 'integrate_metadata.py'


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def load_metadata(topic):
    meta_file = EXTRACTOR_META / (slug(topic) + '.json')
    if meta_file.exists():
        try:
            return json.loads(meta_file.read_text(encoding='utf-8'))
        except Exception:
            return None
    # call integrator
    if INTEGRATOR.exists():
        proc = subprocess.run([sys.executable, str(INTEGRATOR), '--topic', topic], capture_output=True, text=True)
        if proc.returncode == 0:
            try:
                out = json.loads(proc.stdout)
                meta = out.get('metadata') or {}
                return meta
            except Exception:
                return None
    return None


TEMPLATE = '''**Who:** {who}
**The Impact:** {impact}
**Value Aligned:** {value}

"{opening}"

**Gratitude Statement:** {gratitude}

**Signature:** — {signoff}

**Source(s):** {sources}
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', required=True)
    parser.add_argument('--who', required=True)
    args = parser.parse_args()

    meta = load_metadata(args.topic)
    if not meta:
        print('No metadata available for topic:', args.topic)
        sys.exit(2)

    who = args.who
    value = (meta.get('value_labels') or ['Teamwork'])[0]
    sources = meta.get('citation_line','')
    suggested = meta.get('suggested_phrases', [])
    opening = suggested[0] if suggested else f'I want to recognize {who} for their contribution.'
    gratitude = f'Thanks, {who}, for your focus and commitment to our team and customers.'
    signoff = 'Your Name, CarMax Delivery Team'
    impact = 'Improved safety and consistency in pre-trip checks.'

    out = TEMPLATE.format(
        who=who,
        impact=impact,
        value=value,
        opening=opening,
        gratitude=gratitude,
        signoff=signoff,
        sources=sources or 'Multiple site standards — see admin for full source list.'
    )

    print(out)


if __name__ == '__main__':
    main()
