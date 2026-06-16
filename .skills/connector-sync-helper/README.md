connector-sync-helper

This helper provides a review-first way to keep hub connector/index files in sync with the actual Markdown content files in the vault.

Usage:
1. Open PowerShell in the workspace root or specify the root path.
2. Run the sync helper in dry-run mode to preview proposed connector updates:

```
python .\.skills\connector-sync-helper\sync_connectors.py --root "c:\Users\trans\Documents\Knowledge" --dry-run
```

3. To enhance summaries and tags with the existing metadata-extractor, add `--rich`:

```
python .\.skills\connector-sync-helper\sync_connectors.py --root "c:\Users\trans\Documents\Knowledge" --dry-run --rich
```

4. Review the proposed patch output.
5. Apply the changes once you approve them:

```
python .\.skills\connector-sync-helper\sync_connectors.py --root "c:\Users\trans\Documents\Knowledge" --apply
```

Output:
- Console patch proposal
- Optional `connector-sync-report.json` file with detected additions, updates, and removals

Notes:
- This script is dependency-free and uses only Python standard libraries for its default operation.
- If you use `--rich`, it will also call the existing `metadata-extractor` helper for richer summaries and tags when available.
- It will never edit Connector files unless `--apply` is supplied.
