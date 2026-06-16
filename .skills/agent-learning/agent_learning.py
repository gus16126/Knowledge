#!/usr/bin/env python3
"""Agent learning helper for local feedback capture and retrieval."""
import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STORAGE = ROOT / 'feedback.jsonl'


def ensure_storage():
    if not STORAGE.exists():
        STORAGE.parent.mkdir(parents=True, exist_ok=True)
        STORAGE.write_text('', encoding='utf-8')


def now_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'


def normalize_tags(tags):
    return [t.strip().lower() for t in tags if t.strip()]


def log_feedback(topic, category, tags, text, source='user'):
    ensure_storage()
    entry = {
        'timestamp': now_iso(),
        'topic': topic.strip().lower(),
        'category': category.strip().lower(),
        'tags': normalize_tags(tags),
        'text': text.strip(),
        'source': source,
    }
    with STORAGE.open('a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    print('Logged feedback for topic:', entry['topic'])


def load_entries():
    ensure_storage()
    entries = []
    with STORAGE.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def search_entries(query, limit=10):
    query = query.strip().lower()
    entries = load_entries()
    matches = []
    for entry in entries:
        text = ' '.join([entry.get('topic', ''), entry.get('category', ''), ' '.join(entry.get('tags', [])), entry.get('text', '')]).lower()
        if query in text:
            matches.append(entry)
    return matches[:limit]


def summarize_topic(topic, limit=5):
    topic = topic.strip().lower()
    entries = [e for e in load_entries() if topic in e.get('topic', '') or topic in ' '.join(e.get('tags', []))]
    if not entries:
        return None

    summary = {
        'topic': topic,
        'count': len(entries),
        'categories': {},
        'top_lessons': [],
    }
    for entry in entries:
        cat = entry.get('category', 'general')
        summary['categories'][cat] = summary['categories'].get(cat, 0) + 1
    summary['top_lessons'] = [e['text'] for e in entries[:limit]]
    return summary


def recommend_policy(topic, limit=5):
    summary = summarize_topic(topic, limit=limit)
    if not summary:
        return None
    guidance = [
        f"Topic: {summary['topic']}",
        f"Lessons captured: {summary['count']}",
        "Recommended behavior updates:",
    ]
    for i, lesson in enumerate(summary['top_lessons'], start=1):
        guidance.append(f"{i}. {lesson}")
    return '\n'.join(guidance)


def print_entry(entry):
    print('---')
    print('Timestamp:', entry.get('timestamp'))
    print('Topic:', entry.get('topic'))
    print('Category:', entry.get('category'))
    print('Tags:', ', '.join(entry.get('tags', [])))
    print('Text:', entry.get('text'))
    print('Source:', entry.get('source'))


def main():
    parser = argparse.ArgumentParser(description='Agent learning feedback helper.')
    sub = parser.add_subparsers(dest='command', required=True)

    log_parser = sub.add_parser('log', help='Log feedback into the agent memory store')
    log_parser.add_argument('--topic', required=True)
    log_parser.add_argument('--category', required=True)
    log_parser.add_argument('--tags', nargs='*', default=[])
    log_parser.add_argument('--text', required=True)
    log_parser.add_argument('--source', default='user')

    search_parser = sub.add_parser('search', help='Search past feedback entries')
    search_parser.add_argument('--query', required=True)
    search_parser.add_argument('--limit', type=int, default=10)

    summary_parser = sub.add_parser('summary', help='Summarize lessons for a topic')
    summary_parser.add_argument('--topic', required=True)
    summary_parser.add_argument('--limit', type=int, default=5)

    recommend_parser = sub.add_parser('recommend', help='Generate recommended policy guidance')
    recommend_parser.add_argument('--topic', required=True)
    recommend_parser.add_argument('--limit', type=int, default=5)

    list_parser = sub.add_parser('list', help='List all stored feedback entries')
    list_parser.add_argument('--limit', type=int, default=20)

    args = parser.parse_args()

    if args.command == 'log':
        log_feedback(args.topic, args.category, args.tags, args.text, source=args.source)
    elif args.command == 'search':
        entries = search_entries(args.query, limit=args.limit)
        if not entries:
            print('No feedback entries matched query:', args.query)
            return
        for entry in entries:
            print_entry(entry)
    elif args.command == 'summary':
        summary = summarize_topic(args.topic, limit=args.limit)
        if not summary:
            print('No feedback found for topic:', args.topic)
            return
        print('Topic:', summary['topic'])
        print('Entries found:', summary['count'])
        for i, lesson in enumerate(summary['top_lessons'], start=1):
            print(f'{i}. {lesson}')
    elif args.command == 'recommend':
        recommendation = recommend_policy(args.topic, limit=args.limit)
        if not recommendation:
            print('No feedback found for topic:', args.topic)
            return
        print(recommendation)
    elif args.command == 'list':
        entries = load_entries()[:args.limit]
        if not entries:
            print('No feedback has been logged yet.')
            return
        for entry in entries:
            print_entry(entry)


if __name__ == '__main__':
    main()
