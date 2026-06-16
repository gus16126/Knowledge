name: recognition-builder
description: Triggered when the user wants to draft a team shout-out, huddle appreciation, or a response to received recognition. If the request is ambiguous, ask for clarification before drafting.
---

# Operational Procedure
1. Attempt to load resources first:
   - Scan the local Recognition folder at `C:\Users\trans\Documents\Knowledge\Recognitions` for recent call-outs or examples.
   - Scan the local CarMax Leadership folder at `C:\Users\trans\Documents\Knowledge\CarMax Leadership` for tone guidance.
   - If the recognition request includes an operational topic or procedure, also call `metadata-extractor` to find a relevant source citation and support the message content.
   - If these resources are unavailable, respond: "I can't access the recognition folder or leadership guide. Please paste 1–3 past call-outs or describe the desired tone (e.g., professional, casual)." Then wait for user input before drafting.
2. Apply tone guidelines:
   - Use the CarMax Leadership style: professional, positive, concise, team-focused, and customer-first. Do not use slang or sarcasm.
   - If the guide is unavailable, default to supportive, professional tone with a 1–2 sentence opening, 1 sentence impact, and 1 sentence call-to-action.
3. Review historical examples:
   - Review 3–5 most recent historical examples from the Recognition folder. Prefer 4.
   - If fewer than 3 exist, review all available and note "only N examples available" before drafting.
   - If none exist, proceed using the default tone and template structure.
   - Adopt historical sentence structure and tone while preserving the template fields. Do not copy the quoted template sentences verbatim unless they match the historical voice.
4. Map user intent to templates:
   - If user asks for a public announcement, shout-out, or huddle announcement → Template 1.
   - If user received praise and asks for a reply, thank-you response, or mentions "I received" → Template 2.
   - If user asks for peer-to-peer appreciation, colleague support, or team recognition without public announcement language → Template 3.
   - If multiple intents appear, ask: "Is this a public huddle announcement, a reply to recognition, or a peer appreciation?"
   - If the user specifies tone, length, or channel, follow those constraints; if unspecified, default to tone = supportive/professional, length = 2–3 sentences for huddle/appreciation, 3–5 sentences for response, channel = huddle announcement.
   - If a relevant source citation exists from `metadata-extractor`, optionally include it for recognition drafts of technical training or procedure-based accomplishments.
5. Handle missing details before drafting:
   - If recipient name is missing, ask: "Who is the shout-out for?"
   - If action or impact details are missing, ask: "What specifically did they do (one sentence)?"
   - If multiple recipients are provided, ask: "Should these be combined into a single announcement or separate ones?"
   - If the user provides no input, generate a placeholder draft and mark missing fields with [MISSING INFORMATION].

# Approved Output Templates

## 📢 Template 1: Team Huddle Announcement (Shout-Out)
**Who:** [Name of Associate]
**The Impact:** [What they did + why it matters to operations]
**Value Aligned:** [Select one from: Customer First, Integrity, Teamwork, Excellence — or use the company's official value label; if unknown, ask user to specify or choose 'Teamwork']

"Let's give a huge shout-out to [Name] for..." (or an equivalent approved opening if the historical voice requires it)

## ✉️ Template 2: Response to Received Recognition
**Who:** [Sender Name — use the user's provided name; if none provided, ask: 'What name should appear as the sender?']
**What I Received:** [Brief summary of the accolade or comment received]
**Gratitude Statement:** [2–3 sentence thank-you focusing on team impact, collaboration, and moving forward together]

## 🤝 Template 3: Huddle Appreciation (Peer-to-Peer)
**Who:** [Name/Team — if multiple recipients, list up to three names with one-sentence impacts each, or create a team-level paragraph for more than three recipients]
**Why:** [Specific observable behavior or operational support impact]
**Call-to-Action:** [One-line inspiring suggestion or benchmark for others to follow]

## Preferred Phrases & Sign-Offs
- Use appreciation phrases from `CarMax Leadership/CarMax Vocabulary & Philosophy.md`, e.g. "I appreciate your effort.", "Thanks for the support.", "I want to recognize your focus and commitment."
- For value alignment, include a `Value Aligned:` field and select from the guide (e.g., Teamwork, Integrity, Customer Care, Safety, Development).
- Use signature standards: "— [Your Name], CarMax [Team]" for public announcements and huddles.