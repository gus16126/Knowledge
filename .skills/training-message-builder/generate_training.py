#!/usr/bin/env python3
"""Generate a training message using metadata from the extractor.

Usage:
  python generate_training.py --topic "pre-trip inspection"

If metadata is missing, the script will call the metadata-integration helper to run the extractor.
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


TEMPLATE = '''## 📢 Team Training Update: {topic}
**Target Focus:** {focus}

### 🔍 What You Need to Know
- **The Core Issue:** {core}
- **Key Detail:** {key}

### 🛠️ Action Steps
1. **{step1}**
2. **{step2}**

> **Important Reminder:** {reminder}

**Close:** {close}

**Signature:** — {signoff}

**Source(s):** {sources}
'''


def short_paragraph(text, max_words=30):
    words = re.findall(r"\w+", text)
    return ' '.join(words[:max_words]) if words else text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', required=True)
    args = parser.parse_args()

    meta = load_metadata(args.topic)
    if not meta:
        print('No metadata available for topic:', args.topic)
        sys.exit(2)

    # derive fields
    topic = meta.get('topic', args.topic)
    focus = (meta.get('value_labels') or ['Equipment Safety'])[0]
    sources = meta.get('citation_line', '')
    suggested = meta.get('suggested_phrases', [])
    primary = meta.get('primary_suggestion') or (suggested[0] if suggested else '')

    # Simple heuristics for core/key/steps
    core = short_paragraph(meta.get('candidates',[{}])[0].get('summary',''), 20)
    key = short_paragraph('Refer to the site standard and confirm checks before departure.', 12)
    step1 = 'Complete the pre-trip checklist and verify all items.'
    step2 = 'Report any exceptions to your manager before departure.'
    reminder = 'Confirm load and securement before moving the vehicle.'
    signoff = 'Your Name, CarMax Delivery Team'

    out = TEMPLATE.format(
        topic=topic.title(),
        focus=focus,
        core=core or 'Review the site pre-trip procedures.',
        key=key,
        step1=step1,
        step2=step2,
        reminder=reminder,
        close=primary,
        signoff=signoff,
        sources=sources or 'Multiple site standards — see admin for full source list.'
    )

    print(out)


if __name__ == '__main__':
    main()
