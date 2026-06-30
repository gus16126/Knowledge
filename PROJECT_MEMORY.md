# PROJECT_MEMORY.md

---
title: "Project Memory"
tags: [project-memory, knowledge-vault]
updated: 2026-06-07
status: active
---

A living record of work performed on the Knowledge vault. All AI agents and team members should:
- **Read this file** at session start to understand current goals and previous context
- **Record entries** after completing significant tasks to maintain continuity
- **Reference this file** when making decisions to avoid duplicate or conflicting work

---

## Summary

**Current Goal:** Build a project memory system and establish AI agent workflows for Knowledge vault maintenance.

**Active Focus Areas:**
- Create `PROJECT_MEMORY.md` structure and helper tooling
- Establish connector audit and sync workflows
- Document agent integration patterns

**Repository Type:** Markdown-based Knowledge Vault using Hub & Spoke connector architecture

---

## Recent Activity


**2026-06-30 — Updated .agent and SOUL.md profiles to match the revised AGENTS.md rules**
- Actor: VaultCommander
- Files: .agent, SOUL.md
- Summary: Updated .agent and SOUL.md profiles to match the revised AGENTS.md rules
- Notes: Aligned all agent profiles to include the latest session protocols, folder names, and communications rules.


**2026-06-30 — Updated self-evaluation draft, mapped master leadership binder file references, merged vocabulary playbook, and pushed project to GitHub**
- Actor: VaultCommander
- Files: CarMax Leadership/Gustavo Guallar-Self-Evaluation Summary - Draft.md, CarMax Leadership/CarMax Master Leadership Binder.md, CarMax Leadership/CarMax Vocabulary & Philosophy.md
- Summary: Updated self-evaluation draft, mapped master leadership binder file references, merged vocabulary playbook, and pushed project to GitHub
- Notes: Standardized terminology for Pre-Trip and Post-Trip inspections, resolved all broken links and orphan files in leadership connectors, and initialized github remote pointing to gus16126/Knowledge.


**2026-06-10 — Updated CarMax Vocabulary & Philosophy Playbook**
- Actor: VaultCommander
- Files: CarMax Leadership/CarMax Vocabulary & Philosophy.md
- Summary: Updated CarMax Vocabulary & Philosophy Playbook
- Notes: Consolidated local and downloaded copies, removing duplicates, and incorporating the official Vision/Mission, Vocabulary standards table, signature guidelines, and keeping local audience guidelines.


**2026-06-10 — Clarified communication protocols in AGENTS.md and SOUL.md**
- Actor: VaultCommander
- Files: AGENTS.md, SOUL.md
- Summary: Clarified communication protocols in AGENTS.md and SOUL.md
- Notes: Specified that CarMax values, 5-step structures, and preferred phrases apply only when drafting outbound documents, and not during direct developer/co-pilot chat communications.


**2026-06-07 — Added management communication guidelines to agent profile, vocabulary file, and project memory**
- Actor: VaultCommander
- Files: AGENTS.md, SOUL.md, CarMax Leadership/CarMax Vocabulary & Philosophy.md, PROJECT_MEMORY.md
- Summary: Added management communication guidelines to agent profile, vocabulary file, and project memory


**2026-06-07 — Completed project memory system setup** #setup #system
- Actor: AI Agent
- Files: PROJECT_MEMORY.md, .scripts/record_memory.py, .instructions.md, README.md
- Summary: Completed project memory system setup
- Notes: System fully functional: agents can now read context, record work, and maintain audit trail across sessions


**2026-06-07 — Created PROJECT_MEMORY.md and helper script** #setup #initial
- Actor: Setup Phase
- Files: PROJECT_MEMORY.md, .scripts/record_memory.py
- Summary: Created PROJECT_MEMORY.md and helper script
- Notes: Initial memory system established with security warnings

### 2026-06-07 — Setup Phase #design

**Session Start: Project Memory System Design** #design #planning
- Actor: AI Agent (initial design phase)
- Files: `PROJECT_MEMORY.md` (created), `.scripts/record_memory.py` (created)
- Summary: Designed and implemented project memory structure; created helper CLI to append entries safely
- Notes: Established that API keys should never be stored in repo files — only secure storage references in memory
- Follow-up: Test helper script and integrate with agent instructions

---

## Decisions

1. **Hub & Spoke Connector Architecture**
   - All major folders (`CarMax Leadership`, `Training`, `Communications`, `Recognitions`, `Maintenance Messages`) have central index files
   - Index files must link to all content files in that folder using `[[wiki links]]`
   - Cross-folder links only when logically necessary

2. **Local Python Environment**
   - Use `.venv` for audit and helper scripts
   - Exclude `.venv` from git via `.gitignore`
   - Python 3.14.5 (from prior setup)

3. **Security: API Keys**
   - **RULE: Never store API keys, tokens, or secrets in repo files**
   - Store secrets in system environment variables, Windows Credential Manager, or local `.env` (excluded by `.gitignore`)
   - In `PROJECT_MEMORY.md`, record only *where* the key is stored, not the value
   - Example: `"DEEPSEEK_API_KEY: stored in system env on dev machine"`

4. **Entry Format**
   - Append-only; use consistent headers
   - Include: timestamp, actor name, files changed, summary, notes, follow-ups
   - Agents call `.scripts/record_memory.py` to create validated entries

5. **Managerial Communication Tone Guidelines**
   - **Matthew Douglas (Manager):** Maintain a professional, direct, and operational tone. Focus on safety, compliance, and metrics. Never lecture or define core CarMax values (like "Doing the Right Thing") to him.

---

## Open Questions

- [ ] How frequently should AI agents record entries? (After each task? Each session?)
- [ ] Should we create a separate audit report file or keep all history in this file?
- [ ] Do we need version control/git integration for memory entries?
- [ ] How deep should agent-recorded entries be? (One-liner vs. detailed notes?)

---

## Next Actions

1. Test `.scripts/record_memory.py` helper script with sample entry
2. Add agent integration instructions to `.instructions.md` (if exists) or create `AGENT_WORKFLOW.md`
3. Document how agents should read this file at session start
4. Update `README.md` with memory usage examples
5. Run connector audit to document current state

---

## How to Use This File

### For Humans

**Recording an entry manually:**
```
### YYYY-MM-DD — Description of Work

- Actor: Your Name or Role
- Files: file1.md, file2.md
- Summary: One-line summary of what changed
- Notes: Additional context (1–2 sentences)
- Follow-up: Any pending items or next steps
```

### For AI Agents

**Reading the memory:**
1. Open this file at session start
2. Read the Summary and last 5–10 Recent Activity entries
3. Review Open Questions and Next Actions to understand context
4. Avoid duplicate work already recorded

**Recording an entry:**
```bash
python .scripts/record_memory.py \
  --actor "AgentName" \
  --action "Describe what you did" \
  --files "path1.md,path2.md" \
  --notes "Optional details"
```

**Security Reminder:**
- Never include API keys, tokens, or credentials in entries
- If referencing a secret's location, use generic language: `"stored in system env"`, `"in local .env"`

---

## Files & Tools

- **`.scripts/record_memory.py`** – CLI helper to append validated entries to this file
- **`README.md`** – Project overview and quick start
- **Connector files** (in each major folder) – Link to this memory file for context
