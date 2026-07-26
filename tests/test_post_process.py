"""Tests for the MRAX post-processor."""

from datetime import date

from meeting_transcriber.models import Transcript, TranscriptLine
from meeting_transcriber.post_process import post_process


def _make_transcript(lines: list[tuple[str, str]]) -> Transcript:
    """Build a Transcript from (speaker, text) pairs."""
    t = Transcript()
    for i, (speaker, text) in enumerate(lines):
        t.lines.append(TranscriptLine(
            speaker=speaker,
            text=text,
            timestamp=float(i) * 10.0,
        ))
    return t


class TestPostProcess:
    def test_empty_transcript(self):
        t = _make_transcript([])
        doc = post_process(t, meeting_title="Empty", meeting_date=date(2026, 1, 1))
        assert doc.meeting_title == "Empty"
        assert len(doc.decisions) == 0
        assert len(doc.actions) == 0

    def test_basic_transcript_no_speakers(self):
        t = _make_transcript([
            ("", "Hello everyone, welcome to the meeting."),
            ("", "We decided to move forward with Python 3.12."),
            ("", "Bob will set up the CI pipeline by next week."),
        ])
        doc = post_process(t, meeting_title="Team Sync")
        assert len(doc.decisions) >= 1
        assert "Python 3.12" in doc.decisions[0].description or "move forward" in doc.decisions[0].description

    def test_decision_extraction(self):
        t = _make_transcript([
            ("Alice", "I think we should go with PostgreSQL."),
            ("Bob", "Agreed. We decided to use PostgreSQL for the new service."),
        ])
        doc = post_process(t)
        decisions = [d.description for d in doc.decisions]
        assert any("PostgreSQL" in d for d in decisions)

    def test_action_extraction(self):
        t = _make_transcript([
            ("Alice", "Bob will investigate the authentication issue."),
            ("Bob", "Sure, I'll follow up on that and send a report."),
        ])
        doc = post_process(t)
        actions = [a.description for a in doc.actions]
        assert any("investigate" in a.lower() or "authentication" in a.lower() for a in actions)

    def test_speaker_detection(self):
        t = _make_transcript([
            ("Alice", "Hello everyone."),
            ("Bob", "Hi Alice, glad to be here."),
            ("Charlie", "Let's get started."),
        ])
        doc = post_process(t)
        assert "Alice" in doc.participants
        assert "Bob" in doc.participants
        assert "Charlie" in doc.participants
        # All speakers should be mentions with is_speaker=True
        speaker_mentions = {m.name for m in doc.mentions if m.is_speaker}
        assert "Alice" in speaker_mentions

    def test_language_passthrough(self):
        t = _make_transcript([("", "Hola, ¿cómo están?")])
        doc = post_process(t, language="es")
        assert doc.language == "es"
