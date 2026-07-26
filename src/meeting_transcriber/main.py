"""
CLI entry point for labs/meeting-transcriber.

Usage
-----
    meeting-transcriber <audio-or-transcript> [--post-process] [--vault-ingest <vault>]
                        [--model base] [--language en] [--diarize] [--llm]
                        [--title "Meeting Title"] [--dry-run]

Examples
--------
    # Transcribe + post-process + vault-ingest (full pipeline)
    meeting-transcriber recording.mp3 \\
        --post-process --vault-ingest ~/my-vault \\
        --title "Sprint Review" --diarize

    # Post-process an existing transcript only
    meeting-transcriber transcript.json --post-process

    # Full pipeline with LLM enhancement
    meeting-transcriber recording.mp3 \\
        --post-process --vault-ingest ~/my-vault --llm
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Optional

from . import __version__
from .models import MraxDocument
from .transcribe import transcribe
from .post_process import post_process
from .vault_ingest import vault_ingest


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="meeting-transcriber",
        description="Transcribe, post-process, and vault-ingest meeting recordings.",
    )

    # Positional
    parser.add_argument(
        "input",
        type=str,
        help="Path to audio file (.mp3, .wav, .m4a) or transcript file (.json, .txt)",
    )

    # Flags
    parser.add_argument(
        "--post-process",
        action="store_true",
        dest="do_post_process",
        help="Run MRAX-structured post-processing on the transcript",
    )
    parser.add_argument(
        "--vault-ingest",
        type=str,
        default=None,
        metavar="VAULT_PATH",
        help="Ingest the MRAX document into an Obsidian vault at VAULT_PATH",
    )

    # Transcription options
    parser.add_argument(
        "--model",
        type=str,
        default="base",
        choices=("tiny", "base", "small", "medium", "large", "large-v2", "large-v3"),
        help="Whisper model size (default: base)",
    )
    parser.add_argument(
        "--language",
        type=str,
        default=None,
        help="Source language code (e.g. 'en', 'hi', 'en-hi'). Auto-detected if not set.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=("cpu", "cuda", "mps"),
        help="Compute device (default: cpu)",
    )
    parser.add_argument(
        "--diarize",
        action="store_true",
        help="Attempt speaker diarization (requires pyannote-audio)",
    )

    # Post-processing options
    parser.add_argument(
        "--llm",
        action="store_true",
        dest="use_llm",
        help="Use LLM (GPT-4o-mini) for enhanced extraction during post-processing",
    )

    # Document metadata
    parser.add_argument(
        "--title",
        type=str,
        default="",
        help="Meeting title (default: derived from filename or 'Untitled Meeting')",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Meeting date in ISO format (default: today)",
    )
    parser.add_argument(
        "--tags",
        type=str,
        default="",
        help="Comma-separated tags for the meeting note",
    )

    # Vault options
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be written without writing",
    )
    parser.add_argument(
        "--link-participants",
        action="store_true",
        default=True,
        help="Create/update participant wiki stubs (default: True)",
    )
    parser.add_argument(
        "--no-link-participants",
        action="store_false",
        dest="link_participants",
        help="Skip participant stub creation",
    )

    # Output
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        metavar="FILE",
        help="Write MRAX markdown to FILE instead of stdout",
    )

    # Version
    parser.add_argument(
        "--version",
        action="version",
        version=f"meeting-transcriber v{__version__}",
    )

    return parser


def cli(argv: Optional[list[str]] = None) -> int:
    """Main CLI entry point — called by the ``meeting-transcriber`` console script."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # ── Resolve meeting date ────────────────────────────────────────
    meeting_date = date.today()
    if args.date:
        try:
            meeting_date = date.fromisoformat(args.date)
        except ValueError:
            print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD.", file=sys.stderr)
            return 1

    # ── Resolve meeting title ───────────────────────────────────────
    meeting_title = args.title or _derive_title(args.input)

    # ── Tags ────────────────────────────────────────────────────────
    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []

    # ── Step 1: Transcribe ─────────────────────────────────────────
    print(f"📄 Processing: {args.input}", file=sys.stderr)

    transcript = transcribe(
        audio_path=args.input,
        model_name=args.model,
        language=args.language,
        device=args.device,
        diarize=args.diarize,
    )

    print(f"   ✓ Transcript: {len(transcript.lines)} lines, language={transcript.language}", file=sys.stderr)

    # ── Step 2: Post-process (optional) ────────────────────────────
    doc: MraxDocument

    if args.do_post_process:
        print(f"   🔄 Post-processing (MRAX format)...", file=sys.stderr)
        doc = post_process(
            transcript=transcript,
            meeting_title=meeting_title,
            meeting_date=meeting_date,
            language=transcript.language,
            llm_enhance=args.use_llm,
        )
        doc.tags = tags
        print(f"   ✓ Extracted: {len(doc.decisions)} decisions, {len(doc.actions)} actions", file=sys.stderr)
    else:
        # Without --post-process, build a minimal document
        doc = MraxDocument(
            meeting_title=meeting_title,
            meeting_date=meeting_date,
            language=transcript.language,
            tags=tags,
            raw_summary=" ".join(line.text for line in transcript.lines if line.text.strip()),
        )
        participants = {line.speaker for line in transcript.lines if line.speaker}
        doc.participants = sorted(participants)

    # ── Step 3: Output ─────────────────────────────────────────────
    markdown = doc.to_markdown()

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown, encoding="utf-8")
        print(f"   💾 Output written: {out_path}", file=sys.stderr)
    elif not args.vault_ingest:
        # Print to stdout only if we're not vault-ingesting (vault will be reported separately)
        print(markdown)

    # ── Step 4: Vault ingest (optional) ────────────────────────────
    if args.vault_ingest:
        vault_path = args.vault_ingest
        if not Path(vault_path).exists() and not args.dry_run:
            print(f"   ⚠ Vault path does not exist: {vault_path}", file=sys.stderr)
            return 1
        elif not Path(vault_path).exists() and args.dry_run:
            print(f"   ⚠ Vault path does not exist (dry-run, continuing): {vault_path}", file=sys.stderr)

        print(f"   📚 Ingesting into vault: {vault_path}", file=sys.stderr)

        created = vault_ingest(
            doc=doc,
            vault_path=vault_path,
            create_dirs=True,
            link_participants=args.link_participants,
            update_daily_note=True,
            dry_run=args.dry_run,
        )

        if args.dry_run:
            print(f"   🔍 DRY RUN — would create {len(created)} file(s):", file=sys.stderr)
        else:
            print(f"   ✓ Created {len(created)} file(s):", file=sys.stderr)
        for f in created:
            print(f"      - {f}", file=sys.stderr)

    print(f"✅ Done.", file=sys.stderr)
    return 0


def _derive_title(input_path: str) -> str:
    """Derive a meeting title from the input file name."""
    stem = Path(input_path).stem
    # Remove common date prefixes like "2026-07-27 " or "20260727_"
    stem = stem.lstrip("0123456789_- ")
    # Replace separators
    stem = stem.replace("_", " ").replace("-", " ").strip()
    return stem.title() if stem else "Untitled Meeting"


if __name__ == "__main__":
    sys.exit(cli())
