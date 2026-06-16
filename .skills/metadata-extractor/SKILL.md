---
name: metadata-extractor
description: Extracts concise source metadata and generates human-friendly `Source(s):` lines plus machine-readable JSON metadata for training, recognition, and connector workflows.
---

# Purpose
Provide a consistent, auditable way to surface source citations and short summaries for messages, Connector entries, and audits.

# Operational Procedure
1. Locate candidate documents: search specified folders (default: `C:\Users\trans\Documents\Knowledge\Training`, `C:\Users\trans\Documents\Knowledge\Recognitions`, `C:\Users\trans\Documents\Knowledge\CarMax Leadership`) for files whose filename or content matches user topic keywords.
2. Rank matches by last-modified date (descending) and text similarity. Select up to five candidates; prefer the two newest for citation.
3. Extract metadata from each candidate:
   - Title: top-level heading or filename without extension.
   - Last-modified: filesystem timestamp (YYYY-MM-DD).
   - One-line summary: 12–20 word extractive summary (prefer first informative sentence; truncate/normalize to 12–20 words).
   - Tags: 3–5 short tags derived from headings and keywords.
   - Word count: approximate token/word count.
4. Resolve conflicts: if candidates contradict on procedural details, mark `conflict:true` and include both citations with a `Confirm with SME` note.
5. Output formats:
   - Human citation line: up to two primary sources formatted as `Title.md (YYYY-MM-DD)` or `Multiple site standards — see admin for full source list`.
   - JSON export: write `.metadata/<topic-slug>.json` with fields: title, path, last_modified, summary, tags, word_count, conflict (bool), notes.
6. Return the citation line and embed JSON metadata when requested by calling skills (e.g., `training-message-builder`, `recognition-builder`, `vault-hub-manager`).

# Templates
Human citation line examples:
- `QuiXspinz Ratcheting System.md (2026-01-15)`
- `Multiple site standards — see admin for full source list`

JSON schema (example):
{
  "title": "QuiXspinz Ratcheting System",
  "path": "Training/QuiXspinz Ratcheting System.md",
  "last_modified": "2026-01-15",
  "summary": "Step-by-step ratchet inspection and torque guidance for two-car haulers.",
  "tags": ["straps","inspection","safety"],
  "word_count": 1420,
  "conflict": false,
  "notes": ""
}

# Error handling
- If a file is inaccessible: return `Error: Unable to access [filename].` and request user action.
- If no relevant documents are found: return `No local source found for [topic]. Please provide source or allow internet resources.`
- If more than two sources are required for accuracy, list two primary sources and append `Plus X additional documents (see admin for full source list).`

# Integration & Usage
- Called by `training-message-builder` to populate `Source(s):` lines and produce `.metadata` artifacts.
- Called by `recognition-builder` to support citations in announcements when applicable.
- Used by `vault-hub-manager` when generating Connector entries to populate summaries/tags.

# Governance
- Always include a short `notes` field if any ambiguity or conflict is detected. Do not substitute web sources unless explicitly allowed by the user.
