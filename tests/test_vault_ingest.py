"""Tests for vault ingestion."""

import tempfile
from datetime import date
from pathlib import Path

from meeting_transcriber.models import MraxDocument, Decision, Action
from meeting_transcriber.vault_ingest import vault_ingest


def _make_minimal_doc() -> MraxDocument:
    doc = MraxDocument(
        meeting_title="Sprint Planning",
        meeting_date=date(2026, 7, 27),
        duration_minutes=30.0,
        participants=["Alice", "Bob"],
    )
    doc.decisions.append(Decision(
        description="Adopt trunk-based development",
        rationale="Faster iterations",
    ))
    doc.actions.append(Action(
        description="Update CONTRIBUTING.md",
        owner="Alice",
    ))
    return doc


class TestVaultIngest:
    def test_basic_ingest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = Path(tmpdir)
            doc = _make_minimal_doc()
            created = vault_ingest(doc, str(vault), create_dirs=True, link_participants=False)

            # Should create the meeting note
            meeting_files = list((vault / "Meetings").glob("*.md"))
            assert len(meeting_files) == 1
            assert "sprint-planning" in meeting_files[0].name

            # Verify content
            content = meeting_files[0].read_text(encoding="utf-8")
            assert "Sprint Planning" in content
            assert "Adopt trunk-based development" in content
            assert "Update CONTRIBUTING.md" in content

            # Returned paths
            assert len(created) == 1  # only the meeting note

    def test_participant_stubs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = Path(tmpdir)
            doc = _make_minimal_doc()
            vault_ingest(doc, str(vault), create_dirs=True, link_participants=True)

            people_files = list((vault / "People").glob("*.md"))
            names = {f.stem for f in people_files}
            assert "Alice" in names
            assert "Bob" in names

    def test_dry_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = Path(tmpdir)
            doc = _make_minimal_doc()
            created = vault_ingest(doc, str(vault), dry_run=True)

            # No files should be created in dry-run
            meeting_files = list((vault / "Meetings").glob("*.md"))
            assert len(meeting_files) == 0

            # But paths should still be reported
            assert len(created) >= 1

    def test_nonexistent_vault_raises(self):
        import pytest
        doc = _make_minimal_doc()
        with pytest.raises(FileNotFoundError):
            vault_ingest(doc, "/nonexistent/path")

    def test_daily_note_update(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            vault = Path(tmpdir)
            doc = _make_minimal_doc()
            vault_ingest(doc, str(vault), create_dirs=True, update_daily_note=True)

            daily_files = list((vault / "Daily").glob("*.md"))
            assert len(daily_files) == 1
            content = daily_files[0].read_text(encoding="utf-8")
            assert "Sprint Planning" in content
            assert "Alice" in content
            assert "Bob" in content
