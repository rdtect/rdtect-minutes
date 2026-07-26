"""
Data models for the MRAX (Meeting Record Action Exchange) format.

MRAX defines three core entry types extracted from meeting transcripts:
  - Decision  → journal entry with rationale and context
  - Action    → task entry with owner and deadline
  - Mention   → person/role reference → [[wiki-link]]
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Optional


# ── MRAX Entry Types ──────────────────────────────────────────────────

@dataclass
class Decision:
    """A decision made during the meeting."""
    description: str
    rationale: str = ""
    decided_by: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class Action:
    """An action item assigned during the meeting."""
    description: str
    owner: str = ""
    deadline: Optional[date] = None
    status: str = "open"  # open | in_progress | done


@dataclass
class Mention:
    """A person, role, or entity mentioned (→ [[wiki-link]])."""
    name: str
    context: str = ""
    is_speaker: bool = False


@dataclass
class Transcript:
    """Raw meeting transcript with speaker diarization lines."""
    lines: list["TranscriptLine"] = field(default_factory=list)
    language: str = "en"
    source: str = ""  # e.g. "whisper", "deepgram", "file"


@dataclass
class TranscriptLine:
    """A single line in the transcript with speaker attribution."""
    speaker: str = ""
    text: str = ""
    timestamp: float = 0.0  # seconds from start
    confidence: float = 1.0


@dataclass
class MraxDocument:
    """
    Top-level MRAX document — the structured output of --post-process.

    This is a vault-ready markdown document with frontmatter, sections,
    and wiki-link-annotated entries.
    """
    meeting_title: str = ""
    meeting_date: date = field(default_factory=date.today)
    duration_minutes: float = 0.0
    participants: list[str] = field(default_factory=list)
    decisions: list[Decision] = field(default_factory=list)
    actions: list[Action] = field(default_factory=list)
    mentions: list[Mention] = field(default_factory=list)
    raw_summary: str = ""
    language: str = "en"
    tags: list[str] = field(default_factory=list)

    # ── Serialisation ──────────────────────────────────────────────

    def to_markdown(self) -> str:
        """Render as vault-ready markdown with frontmatter."""
        lines: list[str] = []
        lines.append("---")
        lines.append(f'title: "{self.meeting_title}"')
        lines.append(f"date: {self.meeting_date.isoformat()}")
        lines.append(f"duration_minutes: {self.duration_minutes}")
        if self.participants:
            lines.append(f'participants: [{", ".join(self.participants)}]')
        if self.tags:
            lines.append(f"tags: [{', '.join(self.tags)}]")
        lines.append(f"language: {self.language}")
        lines.append("---")
        lines.append("")
        lines.append(f"# {self.meeting_title}")
        lines.append("")

        # --- Decisions ---
        if self.decisions:
            lines.append("## Decisions")
            lines.append("")
            for i, d in enumerate(self.decisions, 1):
                lines.append(f"### Decision {i}: {d.description}")
                lines.append("")
                if d.rationale:
                    lines.append(f"**Rationale:** {d.rationale}")
                    lines.append("")
                if d.decided_by:
                    lines.append(f"**Decided by:** {_wikify(d.decided_by)}")
                    lines.append("")
                if d.tags:
                    lines.append(f"**Tags:** {' '.join(f'#{t}' for t in d.tags)}")
                    lines.append("")
            lines.append("")

        # --- Actions ---
        if self.actions:
            lines.append("## Action Items")
            lines.append("")
            lines.append("| # | Action | Owner | Deadline | Status |")
            lines.append("|---|--------|-------|----------|--------|")
            for i, a in enumerate(self.actions, 1):
                deadline_str = a.deadline.isoformat() if a.deadline else "—"
                owner_str = _wikify(a.owner) if a.owner else "—"
                lines.append(f"| {i} | {a.description} | {owner_str} | {deadline_str} | {a.status} |")
            lines.append("")

        # --- Participants / Mentions ---
        if self.mentions:
            lines.append("## Participants & Mentions")
            lines.append("")
            for m in self.mentions:
                icon = "🎤" if m.is_speaker else "👤"
                link = _wikify(m.name)
                if m.context:
                    lines.append(f"- {icon} {link} — {m.context}")
                else:
                    lines.append(f"- {icon} {link}")
            lines.append("")

        # --- Raw Summary ---
        if self.raw_summary:
            lines.append("## Summary")
            lines.append("")
            lines.append(self.raw_summary)
            lines.append("")

        return "\n".join(lines)

    @classmethod
    def from_markdown(cls, text: str) -> "MraxDocument":
        """Parse a markdown string back into an MraxDocument (lossy)."""
        doc = cls()
        # Simple frontmatter parsing
        fm_match = re.match(r"^---\s*\n(.+?)\n---", text, re.DOTALL)
        if fm_match:
            for line in fm_match.group(1).split("\n"):
                if ":" in line:
                    key, _, val = line.partition(":")
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key == "title":
                        doc.meeting_title = val
                    elif key == "date":
                        try:
                            doc.meeting_date = date.fromisoformat(val)
                        except ValueError:
                            pass
                    elif key == "duration_minutes":
                        try:
                            doc.duration_minutes = float(val)
                        except ValueError:
                            pass
                    elif key == "language":
                        doc.language = val

        return doc


# ── Helpers ───────────────────────────────────────────────────────────

def _wikify(name: str) -> str:
    """Wrap a name in Obsidian-style wiki-link brackets."""
    name = name.strip()
    if name.startswith("[[") and name.endswith("]]"):
        return name
    return f"[[{name}]]"
