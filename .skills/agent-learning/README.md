agent-learning

This skill provides a lightweight local learning mechanism for the agent.

It stores direct feedback and corrections in `.skills/agent-learning/feedback.jsonl`, and lets the agent retrieve and summarize lessons for future interactions.

Usage examples:

- Log feedback:

```
python .\.skills\agent-learning\agent_learning.py log \
  --topic "python install" \
  --category "environment" \
  --tags python install validation \
  --text "Verify whether the WindowsApps python stub is installed before assuming the interpreter is available."
```

- Search memory:

```
python .\.skills\agent-learning\agent_learning.py search --query "python" --limit 5
```

- Summarize lessons for a topic:

```
python .\.skills\agent-learning\agent_learning.py summary --topic "python install"
```

- Generate recommended agent policy guidance:

```
python .\.skills\agent-learning\agent_learning.py recommend --topic "python install"
```

Setup:
- If Python is installed, run `.\.skills\agent-learning\setup_venv.ps1` from PowerShell to create and activate a local venv.

References:
- This skill should reference the CarMax Vocabulary Guide at `CarMax Leadership/CarMax Vocabulary & Philosophy.md` when generating `recommend` outputs. Use the guide's approved phrases as examples in policy recommendations and surface Value labels when summarizing lessons.

Notes:
- This is not a model retraining tool. It is a local experience store and retrieval layer for agent behavior.
- Keep feedback direct and specific for the best retrieval results.
