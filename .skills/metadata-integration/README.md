metadata-integration

This skill provides a reusable integration layer for the metadata extractor. It is designed to be called by other vault skills to produce consistent citations and JSON audit artifacts.

How it works:
1. The calling skill sends a `topic` and optional search folders.
2. The integration layer invokes the metadata extractor located at `.skills/metadata-extractor/extract_metadata.py`.
3. The extractor writes `.metadata/<topic-slug>.json` and returns a citation line.
4. The calling skill uses the citation line verbatim in the final `Source(s):` line.

This layer also handles:
- `no_source` cases where there are no relevant local documents
- `error` cases when a source file cannot be accessed
- `conflict` detection when candidate sources disagree on procedure

Example caller workflow:
- `metadata-integration` finds a source for "two car hauler"
- `training-message-builder` drafts the update using that citation
- `recognition-builder` can optionally cite the same source when praising an operational achievement
