---
name: vault-hub-manager
description: Manages Hub & Spoke connector files, enforces linking rules, and assists with cross-linking between folder hubs.
---

# Purpose
Provide automated, repeatable guidance for maintaining the Vault "Hub & Spoke" architecture. Ensure every file created or edited in a content folder is linked from that folder's Connector and that Connector files remain consistent and discoverable.

# Operational Procedure
1. Detect Connector files: a folder's Connector is named `Connector.md` or `index.md` in that folder root. If none exists, create a draft `Connector.md` and mark as DRAFT until the user reviews.
2. When creating or editing a content file inside a hub folder (e.g., `Training`, `Recognitions`, `CarMax Leadership`):
   - Add a bidirectional reference to the folder Connector using the `[[filename]]` link format in the Connector. Include a one-line summary and tags.
   - If the Connector does not exist, create a draft Connector and add the new file's entry.
3. When modifying an existing Connector file, do NOT overwrite it blindly. Prepare a proposed patch showing the new/removed entries and ask the user to confirm before applying.
4. When moving or renaming files, update all Connector entries that reference the file. Scan other hub Connectors for cross-links and update them as needed.
5. Hub-to-Hub Cross-Linking: If a file logically belongs to multiple hubs, add a cross-link to each relevant Connector and ensure the cross-reference appears in both hubs' Connector lists.
6. Deletions: When a file is deleted, remove or mark its entry in the Connector as removed (do not delete Connector files). If deletions are numerous, present a changelist and ask for approval.
7. Conflict Resolution: If multiple Connectors appear to claim ownership of a file, flag the conflict and propose a single canonical hub; include reasoning and ask the user to confirm.
8. Metadata: For every Connector entry include: Title, relative path, one-line summary (12–20 words), tags (comma-separated), and last-modified date if available.

# Templates
## Connector Entry (single line)
- Title: [Short title]  
  Link: [[path/to/file.md]]  
  Summary: [One-line summary]  
  Tags: [tag1, tag2]

## Connector Patch Example (when proposing changes)
- Added: [[Training/Pre-Trip Inspection Reinforcement Plan.md]] — Short summary
- Removed: [[Training/Old-Checklist.md]] — obsolete

# Error handling & Permissions
- If a Connector file is locked or not writable, return: "Error: Unable to modify Connector.md in [folder]. Please grant write access or update manually." Do not proceed with automatic edits.
- If multiple changes are required across hubs, present a single changelist and require user confirmation before applying.

# Governance & Approvals
- Never automatically change a top-level Connector without explicit confirmation from the user. Provide a clear diff and actionable accept/reject options.

## Vocabulary Guide Compliance
- Require all new or updated Connector entries to include a `Vocabulary: yes` audit tag when the entry's prose or summary follows the CarMax Vocabulary Guide.
- Require a cross-reference line in each Connector to `CarMax Leadership/CarMax Vocabulary & Philosophy.md`. The `connector-sync-helper` will add or propose this reference when missing.

# Notes
- This skill enforces formatting conventions and linking behavior only; it does not modify content beyond the Connector entries unless explicitly approved by the user.
- Use `connector-sync-helper` as a companion tool to generate proposed Connector/index updates and to keep folder hub listings aligned with actual content files before applying changes.
