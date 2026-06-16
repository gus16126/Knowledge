name: agent-learning
description: Captures agent feedback and experience, stores it as local memory, and retrieves lessons to adapt future project behavior.
---

# Purpose

Build a local learning layer for the agent and project. This skill captures feedback, preferences, and corrections from users, stores them in a durable vault artifact, and retrieves relevant experience when similar topics reappear.

# Operational Procedure

1. Capture feedback whenever the user corrects the agent, reports a behavior issue, or indicates a preference.
   - Store feedback with: timestamp, topic, category, tags, and user text.
   - Use the feedback store at `.skills/agent-learning/feedback.jsonl`.
2. Retrieve learning on request or when processing a matching topic.
   - Search past feedback by keyword, topic, or tag.
   - Summarize the most relevant lessons.
3. Adapt agent behavior based on retrieved feedback.
   - Prefer prior corrections over default heuristics when the topic matches.
   - Surface explicit user preferences (e.g., style, validation checks, wording).
4. Propose policy updates from accumulated experience.
   - Generate suggested guidance snippets for other skills when repeated feedback patterns emerge.

# Templates

## Feedback entry
- Topic: [short subject, e.g. "Python installation"]
- Category: [environment, style, accuracy, workflow, preference]
- Tags: [python, install, validation]
- Text: [user correction or lesson]

## Retrieval query
- If the new request mentions a known topic, search by topic and tags.
- If the user asks for agent memory, provide a concise summary of previous corrections.

# Integration

- Use `agent-learning` when a user explicitly says "remember" or "learn".
- Use `agent-learning` as a guardrail for repeated errors, especially environment or process assumptions.
- Store all feedback as a raw log, but prioritize the latest or most frequent guidance when adapting behavior.

# Governance

- Keep the learning store local and explicit; do not infer user intent without direct feedback.
- Ask for clarification when feedback is vague or conflicting.
- Provide a short summary of learned lessons before applying them to future answers.
