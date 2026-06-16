# 🏛️ CarMax Operations & Leadership Knowledge Vault

Welcome to the central command center for my professional development, team training, fleet maintenance tracking, and CarMax leadership progression. 

This repository is designed as a structured **Hub and Spoke** knowledge system, fully optimized for integration with agentic AI assistants (Antigravity, OpenCode, Hermes).

---

## 📂 Vault Architecture & Directory Map

Every folder below contains a central **Connector/Hub** file that acts as an active Table of Contents for its respective sub-files.

- **`\CarMax Leadership`** ➔ Core hub for LDP/IDP progression, management philosophy, and company vocabulary.
- **`\Training Folder`** ➔ Operational safety guides, driver checklists, and shift-huddle material.
- **`\Maintenance Folder`** ➔ Fleet status tracking, equipment logs (e.g., Cottrell QuiXspinz 2.0), and safety compliance.
- **`\Communication Folder`** ➔ Memos, managerial updates, and official team broadcast protocols.
- **`\Recognition Folder`** ➔ Documentation of peer appreciation and corporate award records.

---

## 🤖 AI Co-Pilot Integration

This workspace is fully prepared for automated assistance. The background intelligence and guardrails are isolated locally via the following root files:
- `.agent` ➔ Directs the **Antigravity** agent workspace rules.
- `AGENTS.md` ➔ Establishes task boundaries for **OpenCode** execution.
- `SOUL.md` ➔ Seeds core behaviors and persona traits for **Hermes**.

### Strict Data Guardrail
All integrated AI systems operate in a **Closed-Loop System**. They are forbidden from searching the internet or using general training datasets to fabricate protocols; they must strictly extract data from our local verified training and maintenance markdown files.

---
## 🧪 Local Python Audit Workflow

The project includes a local Python virtual environment at `.venv` for running audit tools and other workspace scripts.

1. Open PowerShell in the repo root:

```powershell
cd "c:\Users\trans\Documents\Knowledge"
```

2. Activate the local virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

3. Run the connector audit tool:

```powershell
python ".skills\connector-audit\audit_connectors.py"
```

4. To save a JSON audit report:

```powershell
python ".skills\connector-audit\audit_connectors.py" --report
```

This verifies all hub connectors, wiki links, and folder integrity from inside the project environment.

---

## 📝 Project Memory System

`PROJECT_MEMORY.md` is a living record of all work performed on this vault. It serves as the single source of truth for:
- What has been done and why
- Current goals and next actions
- Decisions and reasoning
- Open questions requiring clarification

### For AI Agents

Every AI session should:

1. **At start of session:** Read `PROJECT_MEMORY.md` (top section + last 5–10 recent activity entries) to understand context and avoid duplicate work.

2. **Record work completed:** Use the helper script to append entries:

```powershell
.venv\Scripts\python.exe .scripts\record_memory.py `
  --actor "AgentName" `
  --action "Brief description of work" `
  --files "path/to/file1.md,path/to/file2.md" `
  --notes "Optional additional context"
```

3. **At end of session:** Append a summary entry of tasks completed, findings, and recommended next steps.

### Example Entry

```
**2026-06-07 — Audited connector files**
- Actor: GitHub Copilot
- Files: CarMax Leadership/index.md, Training/Index.md, Recognitions/index.md
- Summary: Verified all hub connectors for broken wiki links and orphaned content
- Notes: Found 2 broken links in Recognitions/index.md; fixed and retested. All connectors now clean.
```

### Security Note

**Never record API keys, tokens, or passwords in PROJECT_MEMORY.md.**
- Store secrets in system environment variables or Windows Credential Manager
- In memory entries, reference only where the secret is stored: `"DEEPSEEK_API_KEY: stored in system env on dev machine"`
- The helper script will reject entries containing secret keywords

---

*"We succeed when our people succeed. Integrity is our North Star."*