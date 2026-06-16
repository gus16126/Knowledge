name: training-message-builder
description: Triggered when the user wants to draft operational updates, huddle safety notes, or team training broadcasts. If the user's topic maps to multiple documents, list the top 3 candidate sources and ask the user to confirm which to use before drafting. If the user's request remains ambiguous or an edge case is not covered by these rules, ask for clarification before drafting.
---

# Operational Procedure (Priority-Ordered Checklist)

**Priority 1: Source Selection & Access**
1. Scan and extract source information from the Training Folder located at `C:\Users\trans\Documents\Knowledge\Training` (and the Maintenance Folder at `C:\Users\trans\Documents\Knowledge\Maintenance Messages` if it is a vehicle-specific safety issue).
1a. Use `metadata-extractor` to generate a human-friendly `Source(s):` citation line and a `.metadata/<topic-slug>.json` artifact for the selected topic.
2. **Error Handling – Inaccessible or Corrupted Files:** If a required source file is inaccessible or corrupted, stop and output: "Error: Unable to access [filename]. Please grant access or provide an alternative document." Do not use internet sources as a replacement.
3. **Error Handling – No Relevant Documents Found:** If no relevant local documents are found, respond exactly: "No local source found for [topic]. Please provide the source document or confirm permission to use internet sources." Do not draft the message without sources.

**Priority 2: Handling Conflicting Information**
- If multiple source documents conflict on a procedure, prefer the most recent site standard (the QuiXspinz Ratcheting System guide or Pre-Trip Inspection Reinforcement Plan) unless an SME article explicitly supersedes it.
- If still unclear after comparing sources, flag the conflict and include the two possible actions with a "Confirm with SME" remark.

**Priority 3: Formatting & Tone (Constant Elements)**
- Use active voice and second-person imperative throughout.
- For all prose sentences in the body sections ('What You Need to Know', 'Key Detail', 'Important Reminder', and numbered Action Steps), keep sentences to 10–15 words maximum; allow up to 20 words only when needed for clarity. Do not apply this limit to headings, labels, or the 'Source(s):' line.
- Use single blank lines between sections.
- Bullet style: '-' followed by one space.
- Include exactly two numbered action steps by default. Add a third and fourth action step only if the source documents explicitly list more than two discrete sequential actions; otherwise do not exceed two.
- Preserve technical tone and terminology consistent with the source documents.

**Priority 4: Vocabulary Rotation (Variable Elements)**
- Vary only the opening sentence and transitional connectors; keep terminology and imperative voice consistent.
- Find documents in the Training Folder whose filenames or content contain the user's topic keywords, sort matches by last-modified date descending, and select the five newest matches for comparison.
- Avoid verbatim reuse of the first sentence. Paraphrases are allowed if meaning is identical; when rephrasing the opening sentence, ensure at least half of the non-stopwords (nouns, verbs, adjectives, adverbs) differ from the most recent similar message's opening sentence.

**Priority 5: Output Structure & Length**
- Produce 120–180 words for the entire message body excluding headings, labels, and the 'Source(s):' line; count only user-facing prose inside the template sections.
- If the sentence-length target conflicts with clarity or accuracy, prioritize a complete message with clear instructions over strict word counts.
- Do not omit any template sections (What You Need to Know, Action Steps, Important Reminder).
- If additional details are needed, add a single optional "Notes" bullet with maximum 30 words.
- Include a "Source(s):" line at the end listing filenames and last-modified dates of the documents used (max two entries); if more than two documents are needed, list the two highest-priority filenames and append "Plus X additional documents (see admin for full source list)." If attachments are not allowed, state "Multiple site standards — see admin for full source list."

**Priority 6: Vocabulary Guide**
- Align all phrasing with the project's `CarMax Leadership/CarMax Vocabulary & Philosophy.md` where applicable.
- Use the guide's approved openings, value-aligned language, and signature standards for closes and sign-offs.

# Approved Output Template

## 📢 Team Training Update: [Topic Name]
**Target Focus:** [e.g., Equipment Safety, Fleet Compliance, Loading Protocol]

### 🔍 What You Need to Know
- **The Core Issue:** [Brief 1-2 sentence explanation of why this matters right now]
- **Key Detail:** [Highlight any crucial operational settings, numbers, or configurations]

### 🛠️ Action Steps
1. **[Step 1]:** [Clear, direct action verb instruction]
2. **[Step 2]:** [Clear, direct action verb instruction]

> **Important Reminder:** [Insert a high-priority safety warning or critical takeaway here]

**Close:** [Positive close connecting to CarMax values]

**Signature:** — [Your Name], CarMax [Team]

**Source(s):** [List filenames and dates, e.g., "QuiXspinz Ratcheting System.md (2026-01-15)" or "Multiple site standards"]
