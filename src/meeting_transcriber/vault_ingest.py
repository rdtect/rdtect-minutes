"""
Vault-ingest engine (``--vault-ingest`` flag).

Writes MRAX-structured meeting documents into an Obsidian-compatible
vault directory, creating:
  - A dated markdown file under ``Meetings/``
  - Wiki-linked cross-references for participants
  - Optional daily note entry updates
"""

from __future__ import annotations

import os
import re
from datetime import date
from pathlib import Path
from typing import Optional

from .models import MraxDocument


def vault_ingest(
    doc: MraxDocument,
    vault_path: str,
    create_dirs: bool = True,
    link_participants: bool = True,
    update_daily_note: bool = False,
    dry_run: bool = False,
) -> list[str]:
    """
    Ingest an *MraxDocument* into an Obsidian vault at *vault_path*.

    Returns a list of file paths that were created (or would be created
    in dry-run mode).

    Steps:
      1. Write the meeting note to ``{vault_path}/Meetings/``
      2. Create/update participant stub files in ``{vault_path}/People/``
      3. Optionally append a reference to the daily note
    """
    vault = Path(vault_path)
    if not vault.exists() and not dry_run:
        raise FileNotFoundError(f"Vault path does not exist: {vault_path}")

    created: list[str] = []

    # ── 1. Meeting note ─────────────────────────────────────────────
    meeting_dir = vault / "Meetings"
    if create_dirs and not meeting_dir.exists():
        if not dry_run:
            meeting_dir.mkdir(parents=True, exist_ok=True)

    slug = _slugify(doc.meeting_title or "untitled-meeting")
    date_str = doc.meeting_date.isoformat()
    filename = f"{date_str} {slug}.md"
    filepath = meeting_dir / filename

    if not dry_run:
        filepath.write_text(doc.to_markdown(), encoding="utf-8")
    created.append(str(filepath))

    # ── 2. Participant stubs ────────────────────────────────────────
    if link_participants:
        people_dir = vault / "People"
        if create_dirs and not people_dir.exists():
            if not dry_run:
                people_dir.mkdir(parents=True, exist_ok=True)

        for participant in doc.participants:
            stub_path = people_dir / f"{participant}.md"
            if not stub_path.exists() and not dry_run:
                stub_content = (
                    f"---\n"
                    f"name: \"{participant}\"\n"
                    f"---\n"
                    f"\n# {participant}\n\n"
                )
                stub_path.write_text(stub_content, encoding="utf-8")
            created.append(str(stub_path))

    # ── 3. Daily note update ────────────────────────────────────────
    if update_daily_note:
        daily_dir = vault / "Daily"
        if create_dirs and not daily_dir.exists():
            if not dry_run:
                daily_dir.mkdir(parents=True, exist_ok=True)

        daily_path = daily_dir / f"{date_str}.md"
        # Use relative path for wiki-links so they work in Obsidian
        meeting_rel = str(filepath.relative_to(vault))
        if not dry_run:
            _append_to_daily(daily_path, doc, meeting_rel)
        created.append(str(daily_path))

    return created


def _append_to_daily(daily_path: Path, doc: MraxDocument, meeting_rel: str) -> None:
    """Append a meeting reference to the daily note."""
    link = f"[[{meeting_rel}|{doc.meeting_title}]]"
    entry = (
        f"\n---\n### Meeting: {link}\n"
        f"- **Duration:** {doc.duration_minutes:.0f} min\n"
        f"- **Participants:** {', '.join(f'[[{p}]]' for p in doc.participants)}\n"
    )
    if doc.decisions:
        entry += f"- **Decisions:** {len(doc.decisions)}\n"
    if doc.actions:
        entry += f"- **Actions:** {len(doc.actions)}\n"

    if daily_path.exists():
        existing = daily_path.read_text(encoding="utf-8")
        if meeting_rel not in existing:  # avoid duplicates
            daily_path.write_text(existing + entry, encoding="utf-8")
    else:
        daily_path.write_text(
            f"---\ntitle: \"{doc.meeting_date.isoformat()}\"\n---\n"
            f"\n# {doc.meeting_date.isoformat()}\n\n{entry}\n",
            encoding="utf-8",
        )


def _slugify(text: str) -> str:
    """Convert text to a filesystem-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s-]+", "-", slug)
    return slug.strip("-")
