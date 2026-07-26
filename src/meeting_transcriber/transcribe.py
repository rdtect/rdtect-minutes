"""
Transcription and speaker-diarisation engine.

Wraps OpenAI Whisper for ASR and provides hooks for diarisation
(e.g. pyannote-audio when available).  When run in --dry-run or
test mode, a file-based transcript reader is used instead.
"""

from __future__ import annotations

import os
import sys
import json
from pathlib import Path
from typing import Optional

from .models import Transcript, TranscriptLine


def transcribe(
    audio_path: str,
    model_name: str = "base",
    language: Optional[str] = None,
    device: str = "cpu",
    diarize: bool = False,
) -> Transcript:
    """
    Run Whisper transcription on *audio_path*.

    If *audio_path* is a ``.json`` or ``.txt`` file containing an
    already-prepared transcript, load that instead (useful for testing
    and for the ``--post-process`` standalone path).
    """
    ext = Path(audio_path).suffix.lower()
    if ext in (".json", ".txt"):
        return _load_transcript_file(audio_path)

    # ── Whisper transcription ──────────────────────────────────────
    try:
        import whisper  # type: ignore[import-untyped]
    except ImportError:
        print("Error: openai-whisper is required for audio transcription.", file=sys.stderr)
        print("Install with: pip install openai-whisper", file=sys.stderr)
        sys.exit(1)

    whisper_model = whisper.load_model(model_name, device=device)
    result = whisper_model.transcribe(
        audio_path,
        language=language,
        verbose=False,
    )

    transcript = Transcript(
        language=result.get("language", language or "en"),
        source=f"whisper/{model_name}",
    )

    for seg in result.get("segments", []):
        transcript.lines.append(
            TranscriptLine(
                speaker="",
                text=seg.get("text", "").strip(),
                timestamp=seg.get("start", 0.0),
                confidence=seg.get("confidence", 1.0),
            )
        )

    # ── Optional diarisation ───────────────────────────────────────
    if diarize:
        _try_diarize(transcript, audio_path)

    return transcript


def _load_transcript_file(path: str) -> Transcript:
    """Load a pre-existing transcript from JSON or plain text."""
    raw = Path(path).read_text(encoding="utf-8")
    ext = Path(path).suffix.lower()

    if ext == ".json":
        data = json.loads(raw)
        if isinstance(data, dict) and "lines" in data:
            # Re-hydrate from serialised Transcript
            transcript = Transcript(
                language=data.get("language", "en"),
                source=data.get("source", "file"),
            )
            for item in data["lines"]:
                transcript.lines.append(
                    TranscriptLine(
                        speaker=item.get("speaker", ""),
                        text=item.get("text", ""),
                        timestamp=item.get("timestamp", 0.0),
                        confidence=item.get("confidence", 1.0),
                    )
                )
            return transcript
        else:
            # Assume flat list of strings
            transcript = Transcript(source="file")
            for i, line in enumerate(data if isinstance(data, list) else [str(data)]):
                transcript.lines.append(
                    TranscriptLine(text=str(line), timestamp=float(i))
                )
            return transcript

    # Plain text — one line per transcript line
    transcript = Transcript(source="file")
    for i, line in enumerate(raw.splitlines()):
        line = line.strip()
        if line:
            transcript.lines.append(
                TranscriptLine(text=line, timestamp=float(i))
            )
    return transcript


def _try_diarize(transcript: Transcript, audio_path: str) -> None:
    """
    Attempt speaker diarisation using pyannote-audio.

    Falls back silently if the library is not installed.
    """
    try:
        from pyannote.audio import Pipeline  # type: ignore[import-untyped]

        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=os.environ.get("HUGGINGFACE_TOKEN"),
        )
        diarization = pipeline(audio_path)

        # Map diarisation segments to transcript lines by timestamp overlap
        for line in transcript.lines:
            for segment, _, speaker in diarization.itertracks(yield_label=True):
                if abs(segment.start - line.timestamp) < 2.0:  # within 2s window
                    line.speaker = speaker
                    break
    except ImportError:
        pass  # Diarisation unavailable — speakers remain empty
    except Exception:
        pass  # Silently degrade
