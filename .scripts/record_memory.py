#!/usr/bin/env python3
"""
Helper script to record entries in PROJECT_MEMORY.md

Usage:
  python record_memory.py --actor "AgentName" --action "Description" --files "f1.md,f2.md" --notes "optional"

Security Note:
  This script validates that no API keys or tokens are included in the entry.
  Secrets should NEVER be recorded in PROJECT_MEMORY.md.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
MEMORY_FILE = REPO_ROOT / "PROJECT_MEMORY.md"
SECURITY_KEYWORDS = ["api_key", "apikey", "secret_key", "secretkey", "token", "password", "auth_token"]


def validate_no_secrets(text: str) -> bool:
    """Check if text contains suspicious secret patterns."""
    text_lower = text.lower()
    for keyword in SECURITY_KEYWORDS:
        if keyword in text_lower:
            # Allow mention of where secrets are stored (e.g., "stored in system env")
            if "stored in" not in text_lower and "in environment" not in text_lower:
                return False
    return True


def format_entry(actor: str, action: str, files: list[str], notes: str = "") -> str:
    """Create a formatted memory entry."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    entry = f"\n**{date_str} — {action}**\n"
    entry += f"- Actor: {actor}\n"
    
    if files:
        entry += f"- Files: {', '.join(files)}\n"
    
    entry += f"- Summary: {action}\n"
    
    if notes:
        entry += f"- Notes: {notes}\n"
    
    return entry


def append_to_memory(entry: str) -> bool:
    """Append entry to PROJECT_MEMORY.md under Recent Activity section."""
    if not MEMORY_FILE.exists():
        print(f"Error: {MEMORY_FILE} not found", file=sys.stderr)
        return False
    
    content = MEMORY_FILE.read_text(encoding="utf-8")
    
    # Find the "Recent Activity" section
    marker = "## Recent Activity"
    if marker not in content:
        print(f"Error: '{marker}' section not found in PROJECT_MEMORY.md", file=sys.stderr)
        return False
    
    # Insert entry after the header and first blank line
    parts = content.split(marker, 1)
    header_part = parts[0] + marker
    rest = parts[1]
    
    # Find the first double newline after the header
    lines = rest.split("\n", 2)
    if len(lines) < 2:
        print(f"Error: Unexpected format in Recent Activity section", file=sys.stderr)
        return False
    
    # Reconstruct with entry inserted
    new_content = header_part + "\n" + lines[0] + "\n" + entry + "\n".join(lines[1:])
    
    MEMORY_FILE.write_text(new_content, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Record a project memory entry",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python record_memory.py --actor "GitHub Copilot" --action "Audited connectors" --files "Recognitions/index.md,Training/Index.md"
  python record_memory.py --actor "Agent" --action "Fixed broken wiki links" --files "CarMax Leadership/index.md" --notes "Updated 5 broken links in connector"
        """
    )
    
    parser.add_argument("--actor", required=True, help="Name of who/what performed the action (e.g., 'GitHub Copilot', 'Gustavo Guallar')")
    parser.add_argument("--action", required=True, help="Short description of what was done")
    parser.add_argument("--files", default="", help="Comma-separated list of changed files (optional)")
    parser.add_argument("--notes", default="", help="Additional notes or context (optional)")
    
    args = parser.parse_args()
    
    # Validate inputs
    if not validate_no_secrets(args.action) or not validate_no_secrets(args.notes):
        print(
            "Error: Entry contains secret keywords.\n"
            "   API keys, tokens, and passwords should NEVER be stored in PROJECT_MEMORY.md.\n"
            "   Record only where secrets are stored (e.g., 'stored in system env').",
            file=sys.stderr
        )
        return 1
    
    # Parse files
    files = [f.strip() for f in args.files.split(",") if f.strip()] if args.files else []
    
    # Create and append entry
    entry = format_entry(args.actor, args.action, files, args.notes)
    
    if not append_to_memory(entry):
        return 1
    
    print(f"Success: Entry recorded for {args.actor}")
    print(f"  Action: {args.action}")
    if files:
        print(f"  Files: {', '.join(files)}")
    if args.notes:
        print(f"  Notes: {args.notes}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
