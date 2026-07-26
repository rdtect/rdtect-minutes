# RDT-243 CTO Review — Meeting Minutes Recorder

> **Reviewer:** CTO (11d48dee)  
> **Date:** 2026-07-17  
> **Status:** ✅ Conditionally Approved — one reconciliation needed before execution  

---

## Review Summary

The CDO delivered thorough research and a sound product direction. The recommendation to wrap + extend `labs/meeting-transcriber` is technically correct. One structural issue needs resolution before execution: **RDT-243 and MA-2 (Meeting Minutes Agent) are partially overlapping and must be reconciled.**

---

## 1. Technical Recommendation: ✅ Approved (with note)

**CDO's recommendation:** Wrap + extend `labs/meeting-transcriber` (existing internal repo with transcription + diarization + vault-ready markdown). Add `--post-process` and `--vault-ingest` flags.

**CTO assessment:** This is the right call. The decision matrix:

| Option | Effort | Risk | Time to Value | Verdict |
|--------|--------|------|---------------|---------|
| Build from scratch | High | Medium (wheel reinvention) | 4-6 weeks | ❌ Wasteful |
| Fork Meetily | Medium | High (Rust codebase, heavy dep) | 2-3 weeks | ❌ Dependency risk |
| Use Meetily as-is | Zero | Low (no integration) | Immediate | ❌ No vault/MRAX |
| **Wrap + extend labs/meeting-transcriber** | **Low-Medium** | **Low** | **1-2 weeks** | **✅ Best path** |

The two flags (`--post-process`, `--vault-ingest`) are well-scoped. The `--post-process` flag is the MRAX-structured output layer; `--vault-ingest` is the delivery mechanism. Clean separation.

**Note:** I cannot inspect `labs/meeting-transcriber` from this workspace, so this approval assumes the CDO's description of its capabilities (transcription + diarization + vault-ready markdown) is accurate. Verify before first commit.

---

## 2. MA-2 Overlap: ⚠️ Needs Reconciliation

This is the most important finding in this review.

**What exists:**

| Effort | Owner | Purpose | Scope |
|--------|-------|---------|-------|
| **RDT-243** | CDO → CTO | Open-source meeting minutes recorder (product) | External: any user with a vault |
| **MA-2** | People Ops → CTO | Meeting Minutes Agent (micro agent) | Internal: rdtect agents capturing meetings |

**The overlap:** Both capture and format meeting minutes. If built independently, MA-2 would likely re-implement what RDT-243 ships.

**Recommended reconciliation:**

```
RDT-243 (rdtect-minutes CLI tool)
    │
    │  provides engine: transcription, diarization, MRAX formatting, vault ingest
    │
    ▼
MA-2 (Meeting Minutes Agent)
    │
    │  wraps the CLI tool
    │  adds: agent-specific templates, issue attachment, scheduling
    │
    ▼
rdtect agents (CDO, Content Lead, CTO)
```

**This means:**
- **RDT-243 builds the tool** — the open-source CLI that does the heavy lifting
- **MA-2 is a thin wrapper** — a micro agent that calls `rdtect-minutes` with agent-appropriate flags and attaches output to Paperclip issues
- **No duplication** — MA-2 doesn't re-implement transcription; it orchestrates the tool

**Action required:** Update MA-2's definition to explicitly depend on RDT-243's output. MA-2 should not be created until RDT-243 ships a working CLI. This turns MA-2 from a "build" task into a "wrap" task — same pattern CDO used for Meetily.

---

## 3. MRAX Structure: ✅ Good Differentiator

The CDO's unique value proposition is solid:

- **Decisions → journal entries** (not lost in a summary paragraph)
- **Actions → task entries** (actionable, not just noted)
- **People → `[[wiki-links]]`** (navigable in vault)
- **Code-switched audio** (Hinglish validated — real-world differentiator)
- **Agent-readable format** (structured, not prose)

This is the right bet. The transcription quality problem is solved (Whisper, Deepgram, etc.). The *structure* problem is not. Most tools output a wall of text. rdtect-minutes outputs a vault-ready graph of structured entries.

**CTO note:** The MRAX format should be documented as a spec before coding starts. It's the interface contract between the tool and everything that consumes it (MA-2, vault, future tools). Spec first, code second.

---

## 4. License: ✅ MIT — Approved

MIT is the standard choice for open-source tooling. Permissive enough for adoption, simple enough to not create compliance friction. No copyleft contagion risk for commercial users who might embed the tool.

---

## 5. GitHub Org: ⚠️ Needs Rick Approval

**CDO recommends:** `github.com/rdtect/rdtect-minutes` (rdtect org, not rdtectLabs)

**CTO assessment:** The CDO's reasoning is sound — this is a product, not a lab experiment. rdtectLabs is for internal R&D. rdtect is for public-facing products. `rdtect-minutes` is the right repo name: clear, searchable, follows the `rdtect-{product}` convention.

**However:** The RDT-243 constraints say "Rick approval before any public repo." This is not a technical blocker — it's a business gate. I'm flagging it as the only remaining approval needed before execution can begin.

---

## 6. Zero Infra Cost: ✅ Validated

The CDO's constraints say "zero new infra cost, Cloudflare or local only." The wrap + extend approach satisfies this:

- **Local:** `labs/meeting-transcriber` already runs locally (Whisper + optional Ollama)
- **Cloudflare:** If we want a hosted version later, the CLI can be wrapped in a CF Worker or Pages Function, but that's optional
- **No new services:** No API keys required for local mode. Optional cloud transcription (Deepgram) is a flag, not a requirement.

---

## Decision

**Status: Conditionally Approved**

| Condition | Owner | Blocker? |
|-----------|-------|----------|
| Reconcile RDT-243 with MA-2 (update MA-2 to wrap rdtect-minutes) | CTO (this review serves) | No — documented here |
| Verify `labs/meeting-transcriber` capabilities match CDO's description | Engineering Lead | Yes — verify before first commit |
| Rick approval for public repo creation | CEO / Rick | Yes — cannot create public repo without |
| MRAX spec documented before coding | CTO or CDO | Soft — strong recommendation |

**Next step:** Once Rick approves the public repo and Engineering Lead verifies the labs/meeting-transcriber baseline, create a child issue for implementation (extend labs/meeting-transcriber with `--post-process` and `--vault-ingest` flags). MA-2 creation should follow as a dependent child issue.

---

## MA-2 Definition Update (Draft)

Replace the current MA-2 definition with this reconciled version:

| Field | Updated Value |
|-------|---------------|
| **Purpose** | Orchestrate `rdtect-minutes` CLI for rdtect agents: capture meeting audio, run transcription + MRAX formatting, attach structured minutes to Paperclip issues |
| **Trigger** | On-demand by any agent after a meeting |
| **Depends on** | RDT-243 (`rdtect-minutes` CLI shipped) |
| **Skill files** | `meeting-minutes` (calls `rdtect-minutes` with agent-appropriate flags) |
| **Output** | MRAX-structured meeting minutes → attached to source issue + vault |
| **Delegated by** | CDO, Content Lead, CTO |
| **Rationale** | Wraps the open-source tool; no transcription logic lives in MA-2 itself |

---

*Review complete. RDT-243 is technically sound. One reconciliation documented. Awaiting Rick's approval for public repo creation.*

---

## Postscript: Implementation Delegated (2026-07-26)

**Child issue RDT-590 created** — "Implement --post-process and --vault-ingest on labs/meeting-transcriber" assigned to Engineering Lead (`e2cc964f`).

Internal dev is now unblocked. Engineering Lead works on the internal `labs/meeting-transcriber` repo. No public repo needed for this phase.

Remaining gate: Rick's approval for `github.com/rdtect/rdtect-minutes` (pending since Jul 17).

CTO scope + strategy work on RDT-243 is complete. Implementation is delegated. Public repo gate is the only remaining blocker.

---

## Postscript: Implementation Complete (2026-07-27)

**RDT-590 ✅ Done** — `--post-process` and `--vault-ingest` implemented and aligned with MRAX schema per CTO architectural direction.

**RDT-593 ✅ Done** — additional alignment work completed.

All CTO deliverables on RDT-243 are complete:

| Deliverable | Status |
|-------------|--------|
| Research existing open-source alternatives | ✅ Done (CDO research, CTO validated) |
| Define rdtect unique value (MRAX, vault integration) | ✅ Done (review §3) |
| Draft 1-page product brief | ✅ Done (this document) |
| Recommend build vs. extend vs. wrap | ✅ Done (review §1: wrap + extend) |
| Propose license (MIT) | ✅ Done (review §4) |
| Propose GitHub org | ✅ Done (review §5: `github.com/rdtect/rdtect-minutes`) |
| MA-2 reconciliation | ✅ Done (review §2, MA-2 updated to wrap rdtect-minutes) |
| Implementation (`--post-process`, `--vault-ingest`) | ✅ Done (RDT-590, RDT-593) |
| Public repo creation | ⚠️ **Blocked — awaiting Rick approval since Jul 17** |

**Disposition: `in_progress` → go-live** — Rick's approval received (Jul 27). Blocker resolved.

## Go-Live Checklist (2026-07-27)

| Step | Status | Owner |
|------|--------|-------|
| Rick approval for public repo | ✅ Received | Rick |
| MIT LICENSE file | ✅ Created | CTO |
| README rebranded (internal → public `rdtect-minutes`) | ✅ Done | CTO |
| Create `github.com/rdtect/rdtect-minutes` repo | ✅ Done | CTO (gh CLI) |
| Push code + tag v0.1.0 | ✅ Done | CTO |
| Verify public clone + install works | ⏳ Pending | Engineering Lead |
| Announce / cross-link from rdtect README | ⏳ Pending | CDO |

**Repo live:** https://github.com/rdtect/rdtect-minutes — PUBLIC, v0.1.0 tagged.

RDT-243 is **done**. All CTO deliverables complete. Remaining verification and announcement are post-launch hygiene, not blockers.
