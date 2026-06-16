name: metadata-integration
description: Integrates metadata-extractor results into other vault skill workflows, providing consistent citations and metadata artifacts for training, recognition, and connector workflows.
---

# Purpose

Provide a reusable integration layer that calls `metadata-extractor` and returns:
- a human-friendly `Source(s):` citation line
- the path to the generated `.metadata/<topic-slug>.json` artifact
- any conflict or ambiguity notes detected during extraction

# Operational Procedure

1. Receive a topic and optional folders to search.
2. Call `metadata-extractor` (via script or internal wrapper) using the same folder defaults as other skills.
3. If extraction succeeds, return:
   - `citation_line`
   - `metadata_path`
   - `status: success`
4. If no local source is found, return:
   - `status: no_source`
   - `message: No local source found for [topic]. Please provide source or allow internet sources.`
5. If a source file is inaccessible or corrupt, return:
   - `status: error`
   - `message: Error: Unable to access [filename]. Please grant access or provide an alternative document.`
6. If multiple source documents conflict on procedural details, set:
   - `conflict: true`
   - `notes: Confirm with SME`

# Integration Contract

When called by other skills, use the returned citation line verbatim in the final note body.

When the user asks for a draft, the calling skill should:
- perform metadata extraction first
- then use the citation line in `Source(s):`
- preserve `metadata_path` for audit or follow-up workflows
- surface `notes` when ambiguity or conflict exists

# Usage

- `training-message-builder` uses this skill to populate `Source(s):` and create an audit artifact.
- `recognition-builder` uses this skill when the recognition request references a technical procedure or documented operational accomplishment.
- `vault-hub-manager` may use this skill to attach summaries and source citations to Connector entries.
