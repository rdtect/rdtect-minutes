"""
meeting_transcriber — Meeting transcription, MRAX post-processing, and vault ingestion.

Two primary CLI flags:
  --post-process   Transform raw transcript into MRAX-structured markdown
                   (decisions → journal entries, actions → task entries,
                    people → [[wiki-links]])
  --vault-ingest   Write MRAX-structured output into an Obsidian-compatible vault
"""

__version__ = "0.1.0"
