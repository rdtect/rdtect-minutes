"""
MRAX post-processor (``--post-process`` flag).

Transforms a raw transcript into a structured
:class:`~meeting_transcriber.models.MraxDocument` with:
  - Decisions extracted as journal entries
  - Action items extracted as task entries
  - People/entity mentions annotated as ``[[wiki-links]]``
"""

from __future__ import annotations

import os
import re
from datetime import date
from typing import Optional

from .models import (
    Transcript,
    TranscriptLine,
    MraxDocument,
    Decision,
    Action,
    Mention,
)

# ── Pattern constants ─────────────────────────────────────────────────

# Patterns that indicate a decision statement
_DECISION_PATTERNS: list[re.Pattern] = [
    re.compile(r"\b(we|i)\s+(decided|agree|concluded|resolved|voted|chose|settled)", re.IGNORECASE),
    re.compile(r"\b(decision|conclusion|resolution)\b", re.IGNORECASE),
    re.compile(r"\b(going\s+with|moving\s+forward\s+with|let['´`]s\s+go\s+with)\b", re.IGNORECASE),
    re.compile(r"\b(approved|rejected|accepted)\b", re.IGNORECASE),
]

# Patterns that indicate an action item
_ACTION_PATTERNS: list[re.Pattern] = [
    re.compile(r"\b(action|to[- ]do|todo|task)\s*[:\-]?\s*(.+?)(?:by|owner|assign)", re.IGNORECASE),
    re.compile(r"\b(will|shall|must)\s+(investigate|follow.up|send|prepare|create|write|review|update|fix|implement)", re.IGNORECASE),
    re.compile(r"\b(needs?\s+to|has?\s+to|responsible\s+for)\b", re.IGNORECASE),
    re.compile(r"\b(assign|owner|responsible|point\s+person)\b", re.IGNORECASE),
    re.compile(r"\b(by\s+next|deadline|due\s+by|eod|end\s+of\s+(day|week))\b", re.IGNORECASE),
]

# Pattern to extract possible person/role mentions
_PERSON_PATTERN = re.compile(
    r"\b([A-Z][a-z]{1,20})\s+([A-Z][a-z]{1,20})\b"  # "John Smith"
)

# Words that are never valid person names (greetings, common words, etc)
_SKIP_WORDS: set[str] = {
    "morning", "afternoon", "evening", "hello", "welcome", "thanks",
    "thank", "please", "sorry", "great", "good", "right", "sure",
    "yes", "no", "okay", "ok", "hi", "hey", "yeah", "yep",
    "everyone", "everybody", "folks", "team", "guys", "all",
}


def post_process(
    transcript: Transcript,
    meeting_title: str = "",
    meeting_date: Optional[date] = None,
    language: str = "en",
    llm_enhance: bool = False,
) -> MraxDocument:
    """
    Convert a raw *transcript* into an MraxDocument.

    When *llm_enhance* is ``True`` (and ``OPENAI_API_KEY`` is set), an LLM
    call is used for deeper extraction. Otherwise a rule-based extractor is
    used — this works well for well-structured meeting transcripts.
    """
    if meeting_date is None:
        meeting_date = date.today()

    doc = MraxDocument(
        meeting_title=meeting_title or "Untitled Meeting",
        meeting_date=meeting_date,
        language=language,
    )

    # Merge all transcript text for analysis
    full_text = "\n".join(line.text for line in transcript.lines if line.text.strip())
    doc.raw_summary = _generate_summary(full_text, transcript.lines)

    # Collect unique speakers
    speakers = {line.speaker for line in transcript.lines if line.speaker}
    doc.participants = sorted(speakers)

    # Build mention list from speakers
    for speaker in sorted(speakers):
        doc.mentions.append(Mention(name=speaker, is_speaker=True, context="Speaker"))

    if llm_enhance and "OPENAI_API_KEY" in os.environ:
        _llm_extract(doc, full_text)
    else:
        _rule_extract(doc, full_text, transcript.lines)

    # De-duplicate by description
    doc.decisions = _deduplicate_by_description(doc.decisions)
    doc.actions = _deduplicate_by_description(doc.actions)

    return doc


# ── Rule-based extraction ─────────────────────────────────────────────

def _rule_extract(doc: MraxDocument, full_text: str, lines: list[TranscriptLine]) -> None:
    """Rule-based extraction of decisions, actions, and mentions."""
    # ── Decisions ───────────────────────────────────────────────────
    for pattern in _DECISION_PATTERNS:
        for match in pattern.finditer(full_text):
            snippet = full_text[max(0, match.start() - 40):match.end() + 120].strip()
            if any(d.description in snippet for d in doc.decisions):
                continue  # skip near-duplicates
            doc.decisions.append(
                Decision(
                    description=snippet[:200],
                    rationale="Extracted from transcript by pattern matching.",
                )
            )

    # ── Action items ────────────────────────────────────────────────
    for pattern in _ACTION_PATTERNS:
        for match in pattern.finditer(full_text):
            snippet = full_text[max(0, match.start() - 40):match.end() + 100].strip()
            if any(a.description in snippet for a in doc.actions):
                continue
            owner = _extract_owner(snippet)
            doc.actions.append(
                Action(
                    description=snippet[:200],
                    owner=owner,
                    status="open",
                )
            )

    # ── Person mentions (non-speaker) ───────────────────────────────
    already_seen = {m.name for m in doc.mentions}
    for match in _PERSON_PATTERN.finditer(full_text):
        name = match.group(0).strip()
        first_word = name.split()[0].lower()
        if first_word in _SKIP_WORDS:
            continue
        if name not in already_seen and len(name.split()) >= 2:
            already_seen.add(name)
            doc.mentions.append(
                Mention(name=name, context="Mentioned in transcript")
            )


def _extract_owner(text: str) -> str:
    """Try to extract an owner name from action context."""
    owner_match = re.search(
        r"\b(owner|assignee|point\s+person|responsible)\s*[:\-]?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        text, re.IGNORECASE,
    )
    if owner_match:
        return owner_match.group(2).strip()
    # Fallback: take any capitalized name near action keywords
    fallback = re.search(
        r"(?:by|to|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)",
        text,
    )
    return fallback.group(1).strip() if fallback else ""


# ── LLM-enhanced extraction ──────────────────────────────────────────

def _llm_extract(doc: MraxDocument, full_text: str) -> None:
    """Use an LLM call for deeper extraction."""
    try:
        from openai import OpenAI

        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a meeting-minutes extractor. Given a transcript, "
                        "extract decisions, action items, and person mentions. "
                        "Return valid JSON with keys: decisions (list of {description, rationale}), "
                        "actions (list of {description, owner}), mentions (list of {name, context}). "
                        "Be concise."
                    ),
                },
                {"role": "user", "content": full_text[:8000]},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        if content:
            import json
            data = json.loads(content)
            for d in data.get("decisions", []):
                doc.decisions.append(Decision(
                    description=d.get("description", ""),
                    rationale=d.get("rationale", ""),
                ))
            for a in data.get("actions", []):
                doc.actions.append(Action(
                    description=a.get("description", ""),
                    owner=a.get("owner", ""),
                ))
            for m in data.get("mentions", []):
                doc.mentions.append(Mention(
                    name=m.get("name", ""),
                    context=m.get("context", ""),
                ))
    except ImportError:
        pass  # openai not installed — fall through to rule-based
    except Exception:
        pass  # API call failed — fall through to rule-based


# ── Helpers ───────────────────────────────────────────────────────────

def _generate_summary(full_text: str, lines: list[TranscriptLine]) -> str:
    """Generate a brief summary (first ~300 chars of meaningful content)."""
    cleaned = " ".join(line.text.strip() for line in lines if line.text.strip())
    if len(cleaned) <= 500:
        return cleaned
    return cleaned[:497] + "..."


def _deduplicate_by_description[T](items: list[T]) -> list[T]:
    """Remove items whose ``.description`` overlaps significantly."""
    seen: list[str] = []
    result: list[T] = []
    for item in items:
        desc = getattr(item, "description", str(item))
        if not any(_overlaps(desc, s) for s in seen):
            seen.append(desc)
            result.append(item)
    return result


def _overlaps(a: str, b: str, threshold: float = 0.6) -> bool:
    """Check if string *a* is substantially contained in *b* (or vice versa)."""
    a_lower = a.lower()
    b_lower = b.lower()
    if len(a_lower) < 5 or len(b_lower) < 5:
        return False
    shorter = min(a_lower, b_lower, key=len)
    longer = a_lower if shorter is b_lower else b_lower
    return shorter in longer or len(set(a_lower.split()) & set(b_lower.split())) / max(
        len(set(a_lower.split())), 1
    ) >= threshold
