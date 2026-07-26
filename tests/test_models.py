"""Tests for data models and MRAX serialisation."""

from datetime import date

from meeting_transcriber.models import (
    MraxDocument,
    Decision,
    Action,
    Mention,
)


class TestMraxDocument:
    def test_empty_document_to_markdown(self):
        doc = MraxDocument(meeting_title="Test Meeting")
        md = doc.to_markdown()
        assert "Test Meeting" in md
        assert "---" in md  # frontmatter
        assert "date:" in md

    def test_document_with_decisions_and_actions(self):
        doc = MraxDocument(
            meeting_title="Sprint Review",
            meeting_date=date(2026, 7, 27),
            duration_minutes=45.0,
            participants=["Alice", "Bob"],
        )
        doc.decisions.append(Decision(
            description="Use Python 3.12 for the project",
            rationale="Better performance and typing",
            decided_by="Alice",
        ))
        doc.actions.append(Action(
            description="Set up CI pipeline",
            owner="Bob",
            deadline=date(2026, 8, 1),
        ))
        doc.mentions.append(Mention(name="Charlie", context="Guest", is_speaker=False))

        md = doc.to_markdown()

        # Frontmatter
        assert "title: \"Sprint Review\"" in md
        assert "date: 2026-07-27" in md
        assert "duration_minutes: 45.0" in md

        # Decisions section
        assert "## Decisions" in md
        assert "Use Python 3.12" in md
        assert "[[Alice]]" in md

        # Actions section
        assert "## Action Items" in md
        assert "Set up CI pipeline" in md
        assert "[[Bob]]" in md
        assert "2026-08-01" in md

        # Mentions
        assert "## Participants & Mentions" in md
        assert "[[Charlie]]" in md

    def test_roundtrip_markdown(self):
        doc = MraxDocument(
            meeting_title="Roundtrip Test",
            meeting_date=date(2026, 7, 27),
        )
        md = doc.to_markdown()
        parsed = MraxDocument.from_markdown(md)
        assert parsed.meeting_title == "Roundtrip Test"
        assert parsed.meeting_date == date(2026, 7, 27)
