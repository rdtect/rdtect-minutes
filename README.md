# RDT — Meeting Transcriber

> **Internal tool** (part of `labs/meeting-transcriber`).  
> Transcribes, MRAX-post-processes, and vault-ingests meeting recordings.

| Status | Version | License |
|--------|---------|---------|
| ✅ Active development | 0.1.0 | MIT |

---

## Features

- **Transcription** via OpenAI Whisper (`--model` tiny→large-v3)
- **Speaker diarization** (`--diarize`) via pyannote-audio (optional)
- **`--post-process`** — MRAX-structured output: decisions→journal entries, actions→task entries, people→`[[wiki-links]]`
- **`--vault-ingest`** — writes structured notes into an Obsidian-compatible vault (meeting notes, people stubs, daily note references)
- **Rule-based extraction** (default) or **LLM-enhanced extraction** (`--llm`, requires `OPENAI_API_KEY`)
- **Dry-run mode** (`--dry-run`) — preview changes without writing
- File-based input (`.json`, `.txt`) for running post-processing without re-transcribing

---

## Installation

```bash
# Clone the repo
cd labs/meeting-transcriber

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the package
pip install -e .

# For transcription support (optional but recommended)
pip install openai-whisper

# For speaker diarization (optional)
pip install pyannote-audio
```

---

## Usage

### Quick start — transcribe + post-process + vault-ingest

```bash
meeting-transcriber recording.mp3 \
    --post-process \
    --vault-ingest ~/my-obsidian-vault \
    --title "Sprint Review" \
    --diarize
```

### Post-process an existing transcript only (no audio)

```bash
meeting-transcriber transcript.json --post-process
```

The transcript JSON format:

```json
{
  "language": "en",
  "source": "whisper/base",
  "lines": [
    {"speaker": "Alice", "text": "Hello everyone.", "timestamp": 0.0},
    {"speaker": "Bob",   "text": "Hi Alice!",    "timestamp": 5.0}
  ]
}
```

### Vault-ingest only (with pre-processed markdown)

```bash
meeting-transcriber transcript.json \
    --post-process \
    --vault-ingest ~/my-obsidian-vault \
    --title "Team Sync" \
    --tags "team,sync"
```

### Dry-run (see what would be written)

```bash
meeting-transcriber recording.mp3 \
    --post-process \
    --vault-ingest ~/my-obsidian-vault \
    --dry-run
```

### LLM-enhanced extraction

```bash
export OPENAI_API_KEY="sk-..."
meeting-transcriber transcript.json \
    --post-process \
    --llm \
    --vault-ingest ~/my-obsidian-vault
```

---

## CLI Reference

```
meeting-transcriber <input> [options]

Positional:
  input                   Audio file (.mp3, .wav, .m4a) or transcript (.json, .txt)

Core flags:
  --post-process          Run MRAX-structured post-processing
  --vault-ingest PATH     Ingest output into Obsidian vault at PATH

Transcription:
  --model {tiny,base,small,medium,large,large-v2,large-v3}
                          Whisper model size (default: base)
  --language LANG         Source language code (auto-detect if omitted)
  --device {cpu,cuda,mps} Compute device (default: cpu)
  --diarize               Run speaker diarization (requires pyannote-audio)

Post-processing:
  --llm                   Use GPT-4o-mini for enhanced extraction

Metadata:
  --title TITLE           Meeting title
  --date YYYY-MM-DD       Meeting date (default: today)
  --tags TAGS             Comma-separated tags

Vault:
  --dry-run               Preview without writing
  --output FILE           Write MRAX markdown to FILE
  --no-link-participants  Skip participant wiki-stub creation

Other:
  --version               Show version
  --help                  Show this help
```

---

## MRAX Format

The **MRAX (Meeting Record Action Exchange)** format structures meeting output into:

| Element | Vault Representation |
|---------|---------------------|
| **Decisions** | Journal entries with rationale, decider, and tags |
| **Actions** | Tracked task items with owner, deadline, status |
| **People** | `[[wiki-links]]` to participant stubs |
| **Summary** | Raw transcript summary |

Example vault output:

```
Meetings/
├── 2026-07-27 sprint-planning.md
People/
├── Alice.md
├── Bob.md
└── Charlie.md
Daily/
└── 2026-07-27.md
```

---

## Project Structure

```
.
├── src/
│   └── meeting_transcriber/
│       ├── __init__.py       # Package metadata
│       ├── main.py           # CLI entry point
│       ├── models.py         # MRAX data models + markdown serialisation
│       ├── transcribe.py     # Whisper transcription + diarisation
│       ├── post_process.py   # MRAX post-processing (--post-process)
│       └── vault_ingest.py   # Vault ingestion (--vault-ingest)
├── tests/
│   ├── test_models.py
│   ├── test_post_process.py
│   └── test_vault_ingest.py
├── docs/
├── scripts/
└── pyproject.toml
```

---

## Development

```bash
# Install in editable mode
pip install -e .

# Run tests
python -m pytest tests/ -v

# Run with a sample transcript
python -m meeting_transcriber.main path/to/transcript.json --post-process
```

---

## Related

- **RDT-243** — Meeting Minutes Recorder (product spec)
- **RDT-590** — `--post-process` and `--vault-ingest` implementation (this issue)
- **MA-2** — Meeting Minutes Agent (micro-agent wrapping this CLI)

---

## License

MIT — see LICENSE file.
