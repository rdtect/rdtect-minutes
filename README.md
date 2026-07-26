# rdtect-minutes

> **Open-source meeting minutes recorder** for the [rdtect](https://github.com/rdtect) ecosystem.  
> Transcribes, MRAX-post-processes, and vault-ingests meeting recordings — structured for agents and humans alike.

| Status | Version | License |
|--------|---------|---------|
| ✅ Ready for public release (RDT-243) | 0.2.0 | [MIT](./LICENSE) |

---

## Features

- **Transcription** via OpenAI Whisper (`--model` tiny→large-v3)
- **Speaker diarization** (`--diarize`) via pyannote-audio (optional)
- **`--post-process`** — MRAX-structured output following CTO schema:
  - **Model (Context)** — Meeting context, background, key topics
  - **Rules (Decisions)** — Journal entries with rationale
  - **Actions** — Task entries with owner and deadline
  - **Experience (Narrative)** — Notable moments and insights
  - People → `[[wiki-links]]`
- **`--vault-ingest`** — writes structured notes into an Obsidian-compatible vault
  - Default: `2_Calendar/daily/` (per vault SOP)
  - With `--project`: `3_Efforts/<project>/meetings/`
- **Speaker mapping** (`--speaker-map`) — map `SPEAKER_00=Rick,SPEAKER_01=Amit`
- **LLM-enhanced extraction** — pick your provider:
  - `--llm claude` → Claude haiku-4-5 (requires `ANTHROPIC_API_KEY`)
  - `--llm deepseek` → DeepSeek (requires `DEEPSEEK_API_KEY`)
  - `--llm ollama` → local Ollama inference
- **Rule-based extraction** (default, no API key needed)
- **Dry-run mode** (`--dry-run`) — preview changes without writing
- File-based input (`.json`, `.txt`) for running post-processing without re-transcribing

---

## Installation

```bash
# Clone the repo
git clone https://github.com/rdtect/rdtect-minutes.git
cd rdtect-minutes

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install the package
pip install -e .

# For transcription support (optional but recommended)
pip install openai-whisper

# For speaker diarization (optional)
pip install pyannote-audio

# For LLM-enhanced extraction (optional — pick your provider)
pip install anthropic        # for --llm claude
pip install openai           # for --llm deepseek
pip install httpx            # for --llm ollama (usually pre-installed)
```

---

## Usage

### Full pipeline — transcribe + post-process + vault-ingest

```bash
meeting-transcriber recording.mp3 \
    --post-process \
    --vault-ingest ~/my-obsidian-vault \
    --title "Sprint Review" \
    --diarize
```

### With speaker mapping and Claude LLM

```bash
meeting-transcriber recording.mp3 \
    --post-process \
    --vault-ingest ~/my-obsidian-vault \
    --speaker-map "SPEAKER_00=Rick,SPEAKER_01=Amit" \
    --llm claude \
    --title "Sprint Review"
```

### Vault-ingest with project-specific path

```bash
meeting-transcriber recording.mp3 \
    --post-process \
    --vault-ingest ~/my-obsidian-vault \
    --project rdtect \
    --title "Architecture Review"
```

This writes to `3_Efforts/rdtect/meetings/` instead of the default `2_Calendar/daily/`.

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

### Dry-run (see what would be written)

```bash
meeting-transcriber recording.mp3 \
    --post-process \
    --vault-ingest ~/my-obsidian-vault \
    --dry-run
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
  --project NAME          Vault path → 3_Efforts/<NAME>/meetings/ (CTO spec)

Transcription:
  --model {tiny,base,small,medium,large,large-v2,large-v3}
                          Whisper model size (default: base)
  --language LANG         Source language code (auto-detect if omitted)
  --device {cpu,cuda,mps} Compute device (default: cpu)
  --diarize               Run speaker diarization (requires pyannote-audio)

Post-processing:
  --llm {claude,deepseek,ollama}
                          LLM provider for enhanced extraction
                          (default: rule-based, no API key needed)
  --speaker-map MAP       Map speaker IDs to names
                          e.g. "SPEAKER_00=Rick,SPEAKER_01=Amit"

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

The **MRAX (Meeting Record Action Exchange)** format structures meeting output
into four sections, as specified by the CTO architectural direction (RDT-243):

| Section | Content | Vault Representation |
|---------|---------|---------------------|
| **Model** | Context, background, meeting type, key topics | Section with context summary |
| **Rules** | Decisions made, with rationale and decider | Journal entries with [[wikilinks]] |
| **Actions** | Task items with owner, deadline, status | Tracked table with owners |
| **Experience** | Notable narrative moments, insights | Narrative moments with speakers |

### Example vault output

```
2_Calendar/daily/
├── 2026-07-27 sprint-planning.md    # Meeting note (default path)
└── 2026-07-27.md                     # Daily note with reference

People/
├── Alice.md
├── Bob.md
└── Charlie.md

3_Efforts/rdtect/meetings/           # When --project rdtect is used
└── 2026-07-27 architecture-review.md
```

### Example meeting note

```markdown
---
title: "Sprint Planning"
date: 2026-07-27
duration_minutes: 30.0
participants: [Alice, Bob]
tags: [sprint, planning]
language: en
---

# Sprint Planning

## Model — Context

**Meeting type:** planning

**Key topics:**
- Trunk-based development
- CI pipeline

## Rules — Decisions

### Rule 1: Adopt trunk-based development

**Rationale:** Faster iterations

## Actions

| # | Action | Owner | Deadline | Status |
|---|--------|-------|----------|--------|
| 1 | Update CONTRIBUTING.md | [[Alice]] | — | open |

## Experience — Narrative

### Moment 1
Team agreed on incremental migration approach
*— [[Alice]]*
*Significance: alignment*

## Participants & Mentions

- 🎤 [[Alice]] — Speaker
- 🎤 [[Bob]] — Speaker

## Raw Summary
...
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
│       ├── vault_writer.py   # Vault ingestion (--vault-ingest) — CTO path structure
│       └── vault_ingest.py   # Backward-compat wrapper
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

- **RDT-243** — Meeting Minutes Recorder (product spec / CTO architecture)
- **RDT-590** — Original implementation of `--post-process` and `--vault-ingest`
- **RDT-593** — CTO-aligned implementation (`--post-process` and `--vault-ingest`)
- **RDT-594** — [Productivity review](./docs/rdt-594-productivity-review.md) for RDT-593 ✅ Done (9.5/10, approved)
- **MA-2** — Meeting Minutes Agent (spec TBD — see RDT-594 review for handoff context)

---

## License

MIT — see LICENSE file.
