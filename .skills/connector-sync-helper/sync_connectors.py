#!/usr/bin/env python3
"""Sync hub connector/index files with actual Markdown content files."""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

CONNECTOR_NAMES = ['Connector.md', 'index.md']
ENTRY_RE = re.compile(r'^\s*\[\[(.+?)\]\]')


def find_connector(folder):
    for name in CONNECTOR_NAMES:
        path = folder / name
        if path.exists():
            return path
    return folder / 'Connector.md'


ALLOWED_EXTENSIONS = {'.md', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.mov', '.mp4'}


def is_content_file(path):
    if not path.is_file():
        return False
    if path.suffix.lower() not in ALLOWED_EXTENSIONS:
        return False
    if path.name in CONNECTOR_NAMES:
        return False
    if path.parts and '.skills' in path.parts:
        return False
    return True


def title_from_file(path):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return path.stem
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('#'):
            return line.lstrip('#').strip()
        if line:
            return line if len(line) < 80 else line[:80].rstrip()
    return path.stem


def first_sentence(text):
    text = text.replace('\n', ' ').strip()
    if not text:
        return ''
    parts = re.split(r'[\.\!?]\s+', text)
    return parts[0].strip()


def summary_from_file(path):
    suffix = path.suffix.lower()
    if suffix == '.pdf':
        return f"PDF Document: {path.name}"
    elif suffix in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
        return f"Image File: {path.name}"
    elif suffix in {'.mov', '.mp4'}:
        return f"Video File: {path.name}"
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return ''
    sentence = first_sentence(text)
    words = re.findall(r"\w+", sentence)
    if not words:
        return ''
    if len(words) <= 20:
        return ' '.join(words)
    return ' '.join(words[:20])


def tags_from_file(path, max_tags=4):
    suffix = path.suffix.lower()
    if suffix == '.pdf':
        return ['pdf', 'document']
    elif suffix in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
        return ['image', 'media']
    elif suffix in {'.mov', '.mp4'}:
        return ['video', 'media']
    try:
        text = path.read_text(encoding='utf-8').lower()
    except Exception:
        return []
    words = re.findall(r"\w+", text)
    stopwords = {'the','and','or','of','to','a','in','for','on','with','is','are','by','that','this','be','as','it','an','at','from'}
    freq = {}
    for w in words:
        if w in stopwords or len(w) < 4:
            continue
        freq[w] = freq.get(w, 0) + 1
    tags = sorted(freq, key=lambda k: (-freq[k], k))[:max_tags]
    return tags


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def extract_metadata_for_file(root, path):
    extractor_path = root / '.skills' / 'metadata-extractor' / 'extract_metadata.py'
    if not extractor_path.exists():
        return None

    topic = path.stem
    try:
        proc = subprocess.run(
            [sys.executable, str(extractor_path), '--topic', topic, '--folders', str(path.parent)],
            capture_output=True,
            text=True,
            cwd=str(root),
        )
    except Exception:
        return None

    if proc.returncode != 0:
        return None

    metadata_file = root / '.metadata' / f"{slug(topic)}.json"
    if not metadata_file.exists():
        return None

    try:
        data = json.loads(metadata_file.read_text(encoding='utf-8'))
        candidates = data.get('candidates', [])
        if not candidates:
            return None
        candidate = candidates[0]
        return {
            'summary': candidate.get('summary', ''),
            'tags': candidate.get('tags', []),
        }
    except Exception:
        return None


def parse_connector_blocks(text):
    parts = re.split(r'(^|\n)(?=-\s*Title:)', text)
    header = ""
    blocks = []
    if parts:
        header = parts[0]
    i = 1
    while i < len(parts):
        block_text = parts[i+1] if i+1 < len(parts) else ""
        if block_text.strip():
            blocks.append(block_text)
        i += 2
    return header, blocks


def key_from_block(block_text):
    m = re.search(r'Link:\s*\[\[(.+?)\]\]', block_text)
    if m:
        link_path = m.group(1).strip()
        filename = link_path.split('/')[-1]
        return os.path.splitext(filename)[0]
    return None


def parse_connector_entries(path):
    entries = {}
    if not path.exists():
        return entries, ""
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return entries, ""
    header, blocks = parse_connector_blocks(text)
    for block in blocks:
        key = key_from_block(block)
        if key:
            entries[key] = block.strip()
    return entries, header


def build_entry_line(title, rel_path, summary, tags, date):
    return f"- Title: {title}  \n  Link: [[{rel_path}]]  \n  Summary: {summary}  \n  Tags: {', '.join(tags)}  \n  Last-modified: {date}"


def relative_path(root, path):
    return str(path.relative_to(root)).replace('\\', '/')


def scan_folder(root, folder):
    folder_path = root / folder
    if not folder_path.exists():
        return []
    files = []
    for path in folder_path.rglob('*'):
        if is_content_file(path):
            files.append(path)
    return sorted(files)


def propose_changes(root, folder, use_rich=False):
    folder_path = root / folder
    connector_path = find_connector(folder_path)
    content_files = scan_folder(root, folder)
    current_entries, header = parse_connector_entries(connector_path) if connector_path.exists() else ({}, "")

    proposals = {'added': [], 'updated': [], 'removed': []}
    actual_keys = set()

    for path in content_files:
        rel = relative_path(root, path)
        title = title_from_file(path)
        if use_rich:
            rich = extract_metadata_for_file(root, path)
            summary = rich.get('summary', '') if rich else summary_from_file(path)
            tags = rich.get('tags', []) if rich else tags_from_file(path)
        else:
            summary = summary_from_file(path)
            tags = tags_from_file(path)
        if not summary:
            summary = summary_from_file(path)
        if not tags:
            tags = tags_from_file(path)
        date = datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()
        key = os.path.splitext(path.name)[0]
        actual_keys.add(key)
        entry_line = build_entry_line(title, rel, summary, tags, date)

        if key not in current_entries:
            proposals['added'].append({'key': key, 'line': entry_line, 'path': rel})
        else:
            existing_line = current_entries[key]
            normalized_entry = re.sub(r'\s+', ' ', entry_line).strip()
            normalized_existing = re.sub(r'\s+', ' ', existing_line).strip()
            if normalized_entry != normalized_existing:
                proposals['updated'].append({'key': key, 'old': existing_line, 'new': entry_line, 'path': rel})

    for key, line in current_entries.items():
        if key not in actual_keys:
            proposals['removed'].append({'key': key, 'line': line})

    return connector_path, proposals


def print_patch(folder, connector_path, proposals):
    print(f"Hub: {folder}")
    print(f"Connector: {connector_path}")
    if not any(proposals.values()):
        print("  No changes needed.\n")
        return
    if proposals['added']:
        print("  Added:")
        for item in proposals['added']:
            print(f"    + {item['path']}")
    if proposals['updated']:
        print("  Updated:")
        for item in proposals['updated']:
            print(f"    ~ {item['path']}")
    if proposals['removed']:
        print("  Removed:")
        for item in proposals['removed']:
            print(f"    - {item['key']}")
    print()


def apply_changes(root, folder, connector_path, proposals):
    current_entries, header = parse_connector_entries(connector_path)
    
    removed_keys = {item['key'] for item in proposals['removed']}
    updated_map = {item['key']: item['new'] for item in proposals['updated']}
    added_map = {item['key']: item['line'] for item in proposals['added']}
    
    final_entries = {}
    for key, block in current_entries.items():
        if key in removed_keys:
            continue
        elif key in updated_map:
            final_entries[key] = updated_map[key]
        else:
            final_entries[key] = block
            
    for key, block in added_map.items():
        final_entries[key] = block
        
    header_clean = header.strip()
    if header_clean:
        content = header_clean + "\n\n"
    else:
        content = f"{folder} Connector\n\nVocabulary Guide: CarMax Leadership/CarMax Vocabulary & Philosophy.md\n\n"
        
    if 'Vocabulary Guide:' not in content:
        lines = content.split('\n')
        # insert at appropriate place
        lines.insert(min(2, len(lines)), 'Vocabulary Guide: CarMax Leadership/CarMax Vocabulary & Philosophy.md')
        lines.insert(min(3, len(lines)), '')
        content = '\n'.join(lines)
        
    blocks_text = "\n\n".join(final_entries.values())
    content += blocks_text + "\n"
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    connector_path.write_text(content, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Propose or apply connector/index file sync changes.')
    parser.add_argument('--root', default='.', help='Workspace root folder')
    parser.add_argument('--folders', nargs='*', help='Specific hub folders to scan')
    parser.add_argument('--dry-run', action='store_true', default=True, help='Show proposed changes without applying')
    parser.add_argument('--apply', action='store_true', help='Apply proposed connector updates')
    parser.add_argument('--rich', action='store_true', help='Enhance summaries and tags using metadata-extractor if available')
    parser.add_argument('--report', action='store_true', help='Save a connector-sync-report.json artifact')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    folders = args.folders or [p.name for p in root.iterdir() if p.is_dir() and p.name != '.skills']
    report = {}

    for folder in sorted(folders):
        connector_path, proposals = propose_changes(root, folder, use_rich=args.rich)
        print_patch(folder, connector_path, proposals)
        report[folder] = {
            'connector': str(connector_path),
            'proposals': proposals,
        }
        if args.apply:
            try:
                apply_changes(root, folder, connector_path, proposals)
            except PermissionError:
                print(f"Error: Unable to modify {connector_path}. Please grant write access or update manually.")

    if args.report:
        report_path = root / '.skills' / 'connector-sync-helper' / 'connector-sync-report.json'
        report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(f"Saved report to {report_path}")

    if not args.apply:
        print('Dry run complete. Use --apply to write proposed Connector updates.')


if __name__ == '__main__':
    main()
