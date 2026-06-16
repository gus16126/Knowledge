name: connector-audit

description: Audits Vault connector/index files for broken wiki links, missing metadata, and connector-content alignment.
---

# Purpose

Provide a rapid, read-only audit of hub Connector/index files to identify broken references, stale metadata, and missing content entries before any updates are applied.

# Operational Procedure

1. Detect hub Connector files in top-level folders under the workspace root, excluding `.skills`.
2. For each Connector file:
   - Validate `Vocabulary Guide:` and `Vocabulary Audit:` metadata lines.
   - Parse wiki-style `[[...]]` links and verify target files exist.
   - Report any missing or unresolved links.
   - Compare referenced content entries to actual `.md` files in the folder and flag orphan files.
3. Produce a summary report and optional JSON artifact.

# Output

- Console audit report showing issues by hub.
- Optional JSON report file when run with `--report`.

# Governance

- This is a read-only audit tool by default.
- It does not modify any Connector or content files unless a follow-up sync tool is explicitly requested.
