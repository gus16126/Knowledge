#!/usr/bin/env python3
"""Audit vault connector/index files for metadata and broken wiki links."""
import argparse
import json
import re
from pathlib import Path

CONNECTOR_NAMES = ['Connector.md', 'index.md', 'Index.md']
LINK_RE = re.compile(r'\[\[([^\]]+)\]\]')


def find_connector(folder: Path):
    for name in CONNECTOR_NAMES:
        path = folder / name
        if path.exists():
            return path
    return None


def is_content_file(path: Path):
    if not path.is_file() or path.suffix.lower() != '.md':
        return False
    if path.name in CONNECTOR_NAMES or path.name.lower() in {name.lower() for name in CONNECTOR_NAMES}:
        return False
    if '.skills' in path.parts:
        return False
    return True


def scan_content_files(folder: Path):
    return sorted([p for p in folder.rglob('*.md') if is_content_file(p)])


def normalize_link_target(raw: str):
    target = raw.split('|', 1)[0].strip()
    if target.lower().endswith('.md'):
        target = target[:-3].strip()
    return target


def find_workspace_file(root: Path, target: str):
    lower_target = target.lower()
    for path in root.rglob('*.md'):
        if path.is_file():
            name = path.stem
            if name.lower() == lower_target:
                return path.resolve()
            if str(path).lower().endswith(f"{lower_target}.md") and '/' in target:
                return path.resolve()
    return None


def resolve_link(root: Path, connector: Path, target: str):
    connector_dir = connector.parent
    candidate = target
    if candidate.startswith('/'):
        candidate = candidate[1:]
    if candidate == '':
        return None

    possible = []
    if '/' in candidate:
        possible.append(root / f"{candidate}.md")
        possible.append(root / candidate)
    else:
        possible.append(connector_dir / f"{candidate}.md")
        possible.append(connector_dir / candidate)
        possible.append(root / f"{candidate}.md")
        possible.append(root / candidate)
    for path in possible:
        if path.exists():
            return path.resolve()

    return find_workspace_file(root, candidate)


def parse_metadata_lines(lines):
    metadata = {'Vocabulary Guide': None, 'Vocabulary Audit': None}
    for line in lines:
        text = line.strip()
        if text.startswith('Vocabulary Guide:'):
            metadata['Vocabulary Guide'] = text[len('Vocabulary Guide:'):].strip()
        elif text.startswith('Vocabulary Audit:'):
            metadata['Vocabulary Audit'] = text[len('Vocabulary Audit:'):].strip()
        if all(value is not None for value in metadata.values()):
            break
    return metadata


def parse_links(lines):
    links = []
    for line in lines:
        for match in LINK_RE.finditer(line):
            raw = match.group(1).strip()
            if raw:
                links.append(raw)
    return links


def audit_connector(root: Path, connector_path: Path):
    text = connector_path.read_text(encoding='utf-8')
    lines = text.splitlines()
    metadata = parse_metadata_lines(lines[:20])
    links = parse_links(lines)
    broken = []
    resolved = []
    for raw in links:
        target = normalize_link_target(raw)
        resolved_path = resolve_link(root, connector_path, target)
        if resolved_path is None:
            broken.append({'link': raw, 'target': target})
        else:
            resolved.append({'link': raw, 'target': target, 'path': str(resolved_path)})

    folder = connector_path.parent
    content_files = [str(p.resolve()) for p in scan_content_files(folder)]
    # Determine which referenced local files are in the folder
    referenced_files = []
    for item in resolved:
        if str(item['path']).startswith(str(folder.resolve())):
            referenced_files.append(str(item['path']))
    orphan_files = [f for f in content_files if f not in referenced_files]

    return {
        'connector': str(connector_path.resolve()),
        'metadata': metadata,
        'broken_links': broken,
        'resolved_links': resolved,
        'orphan_content_files': orphan_files,
        'content_file_count': len(content_files),
        'link_count': len(links),
    }


def collect_hubs(root: Path):
    hubs = []
    for path in sorted(root.iterdir()):
        if not path.is_dir() or path.name == '.skills' or path.name.startswith('.'):
            continue
        connector = find_connector(path)
        if connector:
            hubs.append((path.name, connector))
    return hubs


def print_summary(results):
    print('Connector Audit Summary')
    print('=======================')
    for hub, data in results.items():
        print(f'Hub: {hub}')
        print(f"  Connector: {data['connector']}")
        print(f"  Content files: {data['content_file_count']}")
        print(f"  Total wiki links: {data['link_count']}")
        print(f"  Broken links: {len(data['broken_links'])}")
        print(f"  Orphan content files: {len(data['orphan_content_files'])}")
        print(f"  Vocabulary Guide: {data['metadata']['Vocabulary Guide'] or '<missing>'}")
        audit_value = data['metadata']['Vocabulary Audit'] if data['metadata']['Vocabulary Audit'] is not None else '<missing>'
        print(f"  Vocabulary Audit: {audit_value}")
        if data['broken_links']:
            print('    Broken links:')
            for item in data['broken_links']:
                print(f"      - [[{item['link']}]] -> {item['target']}")
        if data['orphan_content_files']:
            print('    Orphans:')
            for file_path in data['orphan_content_files']:
                print(f"      - {file_path}")
        print()


def main():
    parser = argparse.ArgumentParser(description='Audit connector/index files for metadata and broken wiki links.')
    parser.add_argument('--root', default='.', help='Workspace root folder')
    parser.add_argument('--report', action='store_true', help='Write a JSON audit report')
    parser.add_argument('--report-path', default='.skills/connector-audit/connector-audit-report.json', help='Path for JSON report')
    args = parser.parse_args()

    root = Path(args.root).resolve()
    results = {}
    for hub, connector in collect_hubs(root):
        results[hub] = audit_connector(root, connector)
    print_summary(results)
    if args.report:
        report_file = root / args.report_path
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(json.dumps(results, indent=2), encoding='utf-8')
        print(f'Wrote report to {report_file}')


if __name__ == '__main__':
    main()
