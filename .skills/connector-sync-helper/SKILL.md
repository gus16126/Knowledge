name: connector-sync-helper
description: Proposes and optionally applies Connector/index file updates by syncing hub folders with their detected content files and metadata.
---

# Purpose

Provide a safe, review-first workflow for keeping Vault hub Connector/index files aligned with actual content files. This skill generates proposed patch lists for added, updated, and removed entries and only applies changes after explicit user approval.

# Operational Procedure

1. Detect hub folders and Connector files.
   - A hub Connector is `Connector.md` or `index.md` in a folder root.
   - If none exists, create a draft `Connector.md` and include it in the proposal.
2. Scan each hub folder for local content files.
   - Include `.md` files, excluding `Connector.md`, `index.md`, hidden files, and the helper scripts folder.
   - Determine content files by file path and title headings.
3. Compare actual files to Connector entries.
   - Use file basename or `[[Title]]` links to match existing entries.
   - Detect added files, missing entries, outdated summaries/tags, and removed files.
4. Produce a changelist proposal.
   - Added: new content files requiring Connector entries.
   - Updated: existing entries with changed title, summary, tags, or location.
   - Removed: stale entries pointing to missing files.
5. Generate metadata for each proposed entry.
   - Title: H1 heading or filename without extension.
   - Summary: first informative sentence or 12–20 word extractive summary.
   - Tags: keyword-derived list.
   - Last-modified date: filesystem timestamp (YYYY-MM-DD).
   - If requested and available, use the vault's `metadata-extractor` to enrich summaries and tags instead of the default heuristics.
6. Present a diff-style proposal and require the user to confirm before applying changes.

# Output

- A proposed patch list in the form of added/updated/removed entries.
- Optionally updated Connector/index files when the user approves.
- A `connector-sync-report.json` artifact when requested.

# Error handling

- If a Connector file is not writable, return: "Error: Unable to modify [Connector file path]. Please grant write access or update manually."
- If a folder contains mixed content that cannot be reliably matched, return a conflict report and do not apply changes automatically.
- If a file is missing from the Connector, include it in the proposed patch rather than editing silently.

# Governance

- Never modify a top-level Connector file without explicit user approval.
- Always preserve existing Connector formatting and manual entries as much as possible.
- Use this helper as a companion to `vault-hub-manager` for audit-ready Connector maintenance.
