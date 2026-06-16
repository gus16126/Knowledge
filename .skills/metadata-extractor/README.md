metadata-extractor

This folder contains a simple Python script `extract_metadata.py` that searches local Knowledge folders for files matching a topic, extracts a short one-line summary, tags, last-modified date, and writes a JSON file into `.metadata/<topic-slug>.json`.

Usage example:

```
python extract_metadata.py --topic "two car hauler" \
  --folders "C:\\Users\\trans\\Documents\\Knowledge\\Training" "C:\\Users\\trans\\Documents\\Knowledge\\CarMax Leadership"
```

Output:
- Printed `Source(s):` citation line
- JSON file at `.metadata/<topic-slug>.json`

Notes:
- The script is intentionally simple and dependency-free. It uses heuristic matching and extractive summaries. For production use, consider integrating an NLP library for better summaries and tag extraction.

Environment setup:
1. Install Python 3.8 or newer.
2. Open PowerShell in this folder: `.skills\metadata-extractor`
3. Run:

```
./setup_venv.ps1
```

4. Activate the virtual environment and run the extractor:

```
.\venv\Scripts\Activate.ps1
python extract_metadata.py --topic "two car hauler" --folders "C:\Users\trans\Documents\Knowledge\Training" "C:\Users\trans\Documents\Knowledge\CarMax Leadership"
```
