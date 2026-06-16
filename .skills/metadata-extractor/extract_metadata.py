#!/usr/bin/env python3
"""Simple metadata extractor for the Knowledge vault.

Usage:
  python extract_metadata.py --topic "two car hauler" \
    --folders "C:\\Users\\trans\\Documents\\Knowledge\\Training" "C:\\Users\\trans\\Documents\\Knowledge\\CarMax Leadership"

Outputs a human citation line and writes a JSON file to .metadata/<topic-slug>.json
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime

STOPWORDS = set([
    'the','and','or','of','to','a','in','for','on','with','is','are','by','that','this','be','as','it','an'
])


def slug(s):
    return re.sub(r'[^a-z0-9]+','-', s.lower()).strip('-')


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ''


def title_from_text(text, filename):
    # Look for first Markdown H1 or H2
    m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # fallback: filename without extension
    return os.path.splitext(os.path.basename(filename))[0]


def first_sentence(text):
    # naive: split on period, exclamation, question
    s = re.split(r'[\.!?]\s+', text.strip())
    return s[0] if s else ''


def summarize_sentence(sent, min_words=12, max_words=20):
    words = re.findall(r"\w+", sent)
    if not words:
        return ''
    if len(words) <= max_words:
        return ' '.join(words[:max_words])
    return ' '.join(words[:max_words])


def extract_tags(text, top_n=3):
    words = re.findall(r"\w+", text.lower())
    words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    c = Counter(words)
    return [w for w,_ in c.most_common(top_n)]


VALUE_KEYWORDS = {
    'Teamwork': ['team','we','together','collaboration'],
    'Safety': ['safety','safe','inspection','pre-trip','dot','secure','risk'],
    'Integrity': ['integrity','accur','accuracy','right','compli'],
    'Improvement': ['improv','train','learning','coach','develop'],
    'Appreciation': ['thank','appreciat','recognit','recognize']
}

PHRASE_EXAMPLES = {
    'Teamwork': 'We Win Together when everyone stays consistent with the process.',
    'Safety': 'Safety first — take a moment to double-check before moving.',
    'Integrity': 'Doing the Right Thing means following this process end-to-end.',
    'Improvement': 'Let\'s Go For Greatness by incorporating this improvement.',
    'Appreciation': 'I appreciate your effort and the support you provided.'
}


def file_mtime(path):
    try:
        return datetime.fromtimestamp(os.path.getmtime(path)).date().isoformat()
    except Exception:
        return ''


def find_candidates(topic_keywords, folders):
    candidates = []
    for folder in folders:
        if not os.path.isdir(folder):
            continue
        for root,_,files in os.walk(folder):
            for fn in files:
                if not fn.lower().endswith(('.md','.txt')):
                    continue
                path = os.path.join(root, fn)
                text = read_file(path)
                score = 0
                name = fn.lower()
                for kw in topic_keywords:
                    if kw.lower() in name:
                        score += 5
                    if kw.lower() in text.lower():
                        score += 1 + text.lower().count(kw.lower())
                if score > 0:
                    candidates.append((path, score))
    # sort by mtime then score
    candidates_sorted = sorted(candidates, key=lambda x: (os.path.getmtime(x[0]), x[1]), reverse=True)
    return [p for p,_ in candidates_sorted]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', required=True)
    parser.add_argument('--folders', nargs='+', required=False,
                        default=[
                            r'C:\Users\trans\Documents\Knowledge\Training',
                            r'C:\Users\trans\Documents\Knowledge\Recognitions',
                            r'C:\Users\trans\Documents\Knowledge\CarMax Leadership'
                        ])
    parser.add_argument('--max-candidates', type=int, default=5)
    args = parser.parse_args()

    keywords = re.findall(r"\w+", args.topic)
    candidates = find_candidates(keywords, args.folders)[:args.max_candidates]

    results = []
    for path in candidates:
        text = read_file(path)
        tit = title_from_text(text, path)
        sent = first_sentence(text)
        summary = summarize_sentence(sent)
        tags = extract_tags(text)
        wc = len(re.findall(r"\w+", text))
        # derive value labels and suggested phrases based on content keywords
        value_labels = []
        low = text.lower()
        for label, kws in VALUE_KEYWORDS.items():
            for kw in kws:
                if kw in low:
                    value_labels.append(label)
                    break

        suggested_phrases = [PHRASE_EXAMPLES[l] for l in value_labels if l in PHRASE_EXAMPLES][:3]

        results.append({
            'title': tit,
            'path': os.path.relpath(path, os.getcwd()).replace('\\\\','/'),
            'last_modified': file_mtime(path),
            'summary': summary,
            'tags': tags,
            'word_count': wc,
            'value_labels': value_labels,
            'suggested_phrases': suggested_phrases
        })

    out = {}
    if not results:
        print(f'No local source found for "{args.topic}". Please provide source or allow internet resources.')
        sys.exit(2)

    # primary citations: up to two
    primary = results[:2]
    if len(primary) == 1:
        citation = f"{primary[0]['title']}.md ({primary[0]['last_modified']})"
    else:
        citation = f"{primary[0]['title']}.md ({primary[0]['last_modified']}); {primary[1]['title']}.md ({primary[1]['last_modified']})"

    # write JSON
    meta_dir = os.path.join(os.getcwd(), '.metadata')
    os.makedirs(meta_dir, exist_ok=True)
    slug_topic = slug(args.topic)
    out_path = os.path.join(meta_dir, f"{slug_topic}.json")
    # aggregate top-level suggested phrases and value labels from primary candidates
    top_value_labels = []
    top_suggested_phrases = []
    for p in primary:
        for c in results:
            if c['path'] == p['path']:
                for vl in c.get('value_labels', []):
                    if vl not in top_value_labels:
                        top_value_labels.append(vl)
                for ph in c.get('suggested_phrases', []):
                    if ph not in top_suggested_phrases:
                        top_suggested_phrases.append(ph)

    out = {
        'topic': args.topic,
        'citation_line': citation,
        'candidates': results,
        'value_labels': top_value_labels,
        'suggested_phrases': top_suggested_phrases,
        'primary_suggestion': top_suggested_phrases[0] if top_suggested_phrases else '',
        'tone_hint': ', '.join(top_value_labels) if top_value_labels else '',
        'notes': ''
    }
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)

    print('Source(s):', citation)
    print('Wrote metadata to', out_path)


if __name__ == '__main__':
    main()
