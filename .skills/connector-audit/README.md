# Connector Audit Skill

This skill audits Vault connector/index files for:

- broken or unresolved wiki-style `[[...]]` links
- missing or stale metadata lines like `Vocabulary Guide:` and `Vocabulary Audit:`
- content files in the folder that are not referenced in the connector

## Usage

From the workspace root:

```powershell
& "C:/Users/trans/AppData/Local/Programs/Python/Python314/python.exe" ".skills\connector-audit\audit_connectors.py"
```

To save a JSON report:

```powershell
& "C:/Users/trans/AppData/Local/Programs/Python/Python314/python.exe" ".skills\connector-audit\audit_connectors.py" --report
```

The report is written to `.skills/connector-audit/connector-audit-report.json` by default.
