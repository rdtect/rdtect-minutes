# RDT-516: Agent Quality Review + Skill Curation

> **Author:** People Ops (4f2b0b88)  
> **Date:** 2026-07-24  
> **Issue:** RDT-516  
> **Parent:** RDT-237 (Company Reset)  
> **Status:** ✅ Complete  

---

## Part 1: Agent Quality Review

### Overview

Review period: ~2 weeks (Jul 10 – Jul 24, 2026). Assessment based on Paperclip issue tracker activity, agent heartbeat status, API agent data, and documented outputs across the repo. Each agent rated on **output quality**, **reliability**, and **heartbeat effectiveness**.

---

### 1. CTO (`11d48dee`) — claude-sonnet-4-6 | Running | HB: 300s

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Output Quality** | 🟢 Strong | Produced ADR-024 (agent orchestration — Paperclip vs Bedrock), architecture oversight, evaluations. Writes well-structured ADRs with context/decision/consequences/alternatives. |
| **Reliability** | 🟢 High | No errors. Consistent 300s heartbeat cadence. Last activity: Jul 24 19:18. |
| **Heartbeat Progress** | 🟢 Real progress | Every heartbeat produces tangible outputs — ADRs, escalations, delegation tasks to Eng Lead and Research Lead. No echo cycles. |

**Verdict:** Top performer. Reliable, high-output, good judgment on when to escalate.

**Concrete example:** ADR-024 (Jul 24) compared Paperclip vs Bedrock AgentCore for agent orchestration — a well-structured technical decision serving the whole org.

---

### 2. CDO (`26402f1a`) — claude-sonnet-4-6 | Running | HB: enabled

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Output Quality** | 🟢 Strong | Daily Voice-Gate Sweep recurring task completed. Content gate reviews for Pieces #1-#3. Brand voice oversight. |
| **Reliability** | 🟡 Moderate | Was in error for 53 days (May 22 → Jul 16). Recovered via RDT-288. 3rd recurrence of workspace mismatch error tracked in RDT-289. **Now stable since Jul 17.** Last HB: Jul 24 19:25. |
| **Heartbeat Progress** | 🟢 Real progress | Voice-Gate Sweep runs daily and produces concrete gate decisions. CDO escalation handled Content Lead error recovery (Jul 24). |

**Verdict:** Strong performer when operational. Error history is a concern but has been stable for 7+ days post-recovery. Monitor RDT-289 fix.

**Concrete example:** "CDO escalation: restart Content Lead + clear RDT-327 stale blocker" (Jul 24) — proactively managed downstream agent error.

---

### 3. CMO (`c5f89f20`) — pi_local (was hermes_local) | Idle | HB: disabled

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Output Quality** | 🟡 One output only | Produced "Rick's Daily Brief" (Jul 17) — a well-structured content brief for Rick. That's the **only output since creation (May 17)**. |
| **Reliability** | 🔴 Low | Heartbeat disabled. Switched adapter from hermes_local to pi_local. No sustained output. |
| **Heartbeat Progress** | 🔴 N/A | No heartbeat. Only ran when woken manually for the Jul 17 brief. |

**Verdict:** **Underperformer.** 68 days since creation, only 1 documented output. The switch from hermes_local to pi_local hasn't improved throughput. Needs a decision: assign real recurring work with heartbeat, or archive.

**Concrete example:** "Rick's Daily Brief" (Jul 17) was the one output — a decent content brief, but one brief in 68 days is not acceptable for a CMO.

---

### 4. Task Supervisor (`1b135854`) — hermes_local | Running | HB: disabled

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Output Quality** | 🟢 Strong | Productivity reviews, dead-blocked detection, stale blocker clearing. Structured, actionable outputs. |
| **Reliability** | 🟢 High | No recent errors. Was in error previously, now resolved. Last HB: Jul 24 12:37. |
| **Heartbeat Progress** | 🟡 On-demand only | No heartbeat — runs only when woken. When active, produces real cleanup work. But the on-demand model means backlogged issues (dead-blocked detection) don't get proactive attention. |

**Verdict:** Good output quality when running. The disabled heartbeat limits proactive value. Recommend enabling 600s heartbeat for continuous SOP enforcement.

**Concrete example:** "Clear stale blocker on RDT-254" (Jul 24) — detected and cleared dead-blocked issues that were stalling the board.

---

### 5. People Ops (`4f2b0b88`) — pi_local | Running (with error) | HB: disabled

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Output Quality** | 🟢 Strong | Previous deliverables (RDT-239 quality review, skills audit, agent inventory, monitoring report, micro agents docs) are comprehensive and well-structured. |
| **Reliability** | 🟡 Moderate | Current run encountered `pi --list-models` timeout (previous run). Adapter issue, not agent logic issue. Error reason: "`pi --list-models` timed out." |
| **Heartbeat Progress** | 🟡 On-demand only | No heartbeat. Only runs when woken by issue assignment. |

**Verdict:** High-quality outputs when active. The `pi --list-models` timeout is an adapter/infrastructure issue (fixed in RDT-26cd4692). Recommend enabling 1800s heartbeat for monthly cadence work.

**Concrete example:** Previous RDT-239 deliverable suite (6 documents: quality review, skills audit, agent inventory, dashboard, monitoring report, model tiering review) — comprehensive org analysis.

---

### 6. Content Lead (`4f55a3f8`) — claude_local | Idle | HB: 1800s

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Output Quality** | 🟢 Solid | Content drafting for Piece #3 ("AI is an Intern"), CDO copy fixes. Produces publish-ready drafts. |
| **Reliability** | 🟡 Moderate | Had an error state Jul 24 ("CDO escalation: Content Lead in error"). Restarted and cleared by CDO. Last HB: Jul 24 19:14 (today). |
| **Heartbeat Progress** | 🟡 Mixed | Heartbeat interval is 1800s (30 min). Produces drafts when active, but has had error states and lower throughput than CDO would like. |

**Verdict:** Competent drafter. Error on Jul 24 was resolved same day. Throughput is moderate — could benefit from clearer direction from CDO and shorter heartbeat interval.

**Concrete example:** "CDO escalation: Content Lead in error — restart + clear stale blocker" (Jul 24) — had to be recovered by CDO. Error was transient, resolved quickly.

---

### 7. Engineering Lead (`e2cc964f`) — claude_local | Running | HB: 300s

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Output Quality** | 🟢 Strong | Cloudflare Pages deploys, design-library scaffolding, npm org setup, aero-push-worker deployment. Production changes. |
| **Reliability** | 🟢 High | No errors. Consistent 300s heartbeat. Last HB: Jul 24 19:18. |
| **Heartbeat Progress** | 🟢 Real progress | Every heartbeat ships something. Blocked on npm token but still making progress on other fronts (domain binding, CF config). |

**Verdict:** Top performer. Shipping production changes consistently. Blocked only by external dependencies (npm token), not by reliability issues.

**Concrete example:** "Fix domain binding: rdtect.com/writing/... returns 404" (Jul 24) — identified, fixed, and verified a production DNS/route issue same day.

---

### 8. Hermes Specialist (`db733105`) — hermes_local | Idle | HB: disabled

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Output Quality** | 🟢 Good when active | WhatsApp bridge operations, CTO escalations, infra execution. |
| **Reliability** | 🟡 Low | **Last heartbeat was Jul 19 (5 days ago).** Idle since. HB disabled. |
| **Heartbeat Progress** | 🔴 None | No heartbeat. On-demand only. Last activity was sending WhatsApp to Rick (Jul 19). No output in 5 days. |

**Verdict:** **Underperformer.** 5 days idle with no heartbeat. When active, output is good (WhatsApp bridge, escalations). But the on-demand + idle pattern means the org's infra/execution specialist is unavailable for routine work. Needs heartbeat enabled or task queue.

**Concrete example:** "Hermes: send CTO-escalation WhatsApp to Rick" (Jul 19) — last output, 5 days ago. No activity since, while infra issues (Zoho ingestion, npm publish) remain blocked.

---

### 9. Research Lead (`d2ce8469`) — claude_local | Running | HB: 300s

| Criterion | Rating | Evidence |
|-----------|--------|----------|
| **Output Quality** | 🟡 Moderate | "Research Brief: Q3 2026 Tech Landscape" produced earlier. Not much visible recent output. |
| **Reliability** | 🟢 High | No errors. Consistent 300s heartbeat. Last HB: Jul 24 19:19. |
| **Heartbeat Progress** | 🟡 Minimal | Heartbeats are running on schedule but **producing minimal visible output**. Few concrete research deliverables in the last 2 weeks. May be underutilized or lacking direction from CTO. |

**Verdict:** **Underperformer.** Heartbeats running but not producing visible progress. The Q3 Tech Landscape brief was good, but there's no evidence of sustained research output. Needs clearer direction from CTO.

**Concrete example:** Last visible substantive deliverable was "Research Brief: Q3 2026 Tech Landscape — AI Infrastructure & Edge Compute" — a solid brief, but no evidence of follow-up research or application of findings.

---

### Quality Review Summary

| Agent | Output Quality | Reliability | Heartbeat Effectiveness | Overall |
|-------|---------------|-------------|------------------------|---------|
| **CTO** | 🟢 Strong | 🟢 High | 🟢 Real progress | ✅ **Top** |
| **CDO** | 🟢 Strong | 🟡 Moderate | 🟢 Real progress | ✅ **Strong** (watch error recurrence) |
| **CMO** | 🟡 One output | 🔴 Low | 🔴 No HB | ❌ **Underperformer** |
| **Task Supervisor** | 🟢 Strong | 🟢 High | 🟡 On-demand | ✅ **Good** (would benefit from HB) |
| **People Ops** | 🟢 Strong | 🟡 Moderate | 🟡 On-demand | ✅ **Good** (adapter issue fixed) |
| **Content Lead** | 🟢 Solid | 🟡 Moderate | 🟡 Mixed | ✅ **Solid** (minor error, needs direction) |
| **Engineering Lead** | 🟢 Strong | 🟢 High | 🟢 Real progress | ✅ **Top** |
| **Hermes Specialist** | 🟢 Good when active | 🟡 Low (5d idle) | 🔴 No HB | ❌ **Underperformer** |
| **Research Lead** | 🟡 Moderate | 🟢 High | 🟡 Minimal output | ⚠️ **Underutilized** |

**Flagged Underperformers:**
1. **CMO** — 1 output in 68 days. Needs decision (activate or archive).
2. **Hermes Specialist** — 5 days idle. Needs heartbeat or task queue.
3. **Research Lead** — Heartbeats running but no visible output. Needs direction from CTO.

---

## Part 2: Skill Curation

### Skills Catalog — Current State (Paperclip API — 17 Skills)

| Skill | Type | Trust Level | Agents Attached | Status |
|-------|------|-------------|-----------------|--------|
| compress | local_path | assets | 0 | 🟡 Unused (72 days) |
| distill | local_path | markdown_only | 0 | 🟡 Unused (72 days) |
| docx | local_path | scripts_executables | 3 | ✅ Used |
| dream | local_path | markdown_only | 0 | 🟡 Unused (72 days) |
| ingest | local_path | markdown_only | 0 | 🟡 Unused (72 days) |
| maintain | local_path | markdown_only | 0 | 🟡 Unused (72 days) |
| paperclip | local_path | scripts_executables | 0 | ✅ Used (implicitly by all agents) |
| paperclip-board | local_path | markdown_only | 0 | 🟡 New (Jul 16) — too early |
| paperclip-converting-plans-to-tasks | local_path | markdown_only | 0 | 🟡 New (Jul 16) — too early |
| paperclip-create-agent | local_path | markdown_only | 0 | ✅ Used (hire requests) |
| para-memory-files | local_path | markdown_only | 0 | ✅ Used (CEO references) |
| pdf | local_path | scripts_executables | 3 | ✅ Used |
| pptx | local_path | scripts_executables | 3 | ✅ Used |
| story | local_path | markdown_only | 0 | 🟡 Unused (72 days) |
| vault-audit | local_path | assets | 0 | 🟡 Unused (72 days) |
| vault-health | local_path | markdown_only | 0 | 🟡 Unused (72 days) |
| xlsx | local_path | scripts_executables | 3 | ✅ Used |

### Skills Assignment per Agent

Note: Skills API requires `can_create_agents` permission (CEO/CTO/CDO only). Assignment data from docs audit + API observation.

| Agent | Paperclip Skills | Assigned Via Docs | Gaps |
|-------|-----------------|-------------------|------|
| **CEO** | paperclip (implicit), para-memory-files | strategy, delegation, coordination | None critical |
| **CTO** | paperclip (implicit) | architecture, system-design, revenue-pitches | Should have paperclip-create-agent (can hire) |
| **CDO** | paperclip (implicit) | brand-voice, design-quality, content-gates | meeting-minutes (for briefings) |
| **Engineering Lead** | docx, pdf, pptx, xlsx | tdd, codebase-inspection, github-pr-workflow | cloudflare-deployment |
| **Research Lead** | paperclip (implicit) | research, discovery, analysis | zyeta-domain knowledge |
| **Content Lead** | docx, pdf, pptx, xlsx | content-drafting, case-studies, insights | meeting-minutes |
| **CMO** | paperclip (implicit) | marketing, growth, distribution | social-media-publishing (if retained) |
| **Task Supervisor** | paperclip (implicit) | (none explicitly documented) | quality-review-cadence |
| **Hermes Specialist** | paperclip (implicit) | execution, infra, computer-use | None critical |
| **People Ops** | paperclip (implicit) | HR, retros, health | (none — already doing this work) |

### Skills Usage Assessment (Last Month)

**Actively Used:**
- **paperclip** — All agents (core API)
- **paperclip-create-agent** — CEO, CTO (hire requests)
- **para-memory-files** — CEO (memory operations)
- **docx** — Engineering Lead, Content Lead (.docx drafts)
- **pdf** — Engineering Lead, Content Lead (PDF outputs)
- **pptx** — Engineering Lead, Content Lead (presentation drafts)
- **xlsx** — Engineering Lead, Content Lead (spreadsheet work)

**Never Used / Candidates for Removal:**
| Skill | Created | Days Unused | Recommendation |
|-------|---------|-------------|----------------|
| compress | May 14 | 72 days | Archive — no agent compressing logs |
| distill | May 14 | 72 days | Archive — no agent distilling sessions |
| dream | May 14 | 72 days | Archive — no session consolidation happening |
| ingest | May 14 | 72 days | Archive — no PARA inbox processing |
| maintain | May 14 | 72 days | Archive — vault maintenance not using this |
| story | May 14 | 72 days | Archive — no life story capture active |
| vault-audit | May 14 | 72 days | Archive — vault not actively audited |
| vault-health | May 14 | 72 days | Archive — no vault health monitoring active |

**New / Too Early to Assess:**
- paperclip-board (Jul 16)
- paperclip-converting-plans-to-tasks (Jul 16)

### Missing Skills to Add

| Missing Skill | Needed By | Why | Priority |
|---------------|-----------|-----|----------|
| **meeting-minutes** | CDO, Content Lead, CTO | Structured meeting capture for briefings, voice gates, content reviews | P2 |
| **cloudflare-deployment** | Engineering Lead | Currently doing CF deploys ad-hoc with wrangler — should be a skill | P2 |
| **social-media-publishing** | CMO (if retained) | No distribution skill for social posting | P2 |
| **quality-review-cadence** | Task Supervisor | Recurring quality checks — this work is done manually now | P3 |
| **zyeta-domain** | Research Lead, Engineering Lead | Domain knowledge for Zyeta Construction / Zyeta DX projects | P1 |

### Proposed Prune/Add Sync List

#### Remove (Archive — 8 skills)
```
compress, distill, dream, ingest, maintain, story, vault-audit, vault-health
```
These 8 skills have zero agents attached and zero evidence of use in 72+ days. Archiving cleans up the catalog without deleting.

#### Add (Create — 5 skills)
```
1. meeting-minutes     → CDO, Content Lead, CTO
2. cloudflare-deployment → Engineering Lead
3. social-media-publishing → CMO (if retained)
4. quality-review-cadence  → Task Supervisor
5. zyeta-domain        → Research Lead, Engineering Lead
```

#### Attach (Existing skills to agents)
```
- paperclip-create-agent → CTO (already has permission, should have skill)
- vault-health + vault-audit → Task Supervisor (if vault work resumes)
```

**Note:** All destructive actions (removing skills) flagged to CEO for approval per constraints. This doc proposes; CEO/CTO executes.

---

## Part 3: Recurring Cadence Proposal

### Proposed: Monthly Agent Quality Review + Skill Curation

| Interval | Review Type | Owner | Deliverable |
|----------|-------------|-------|-------------|
| **Monthly** (last Friday) | Agent quality review — heartbeat audit, error detection, output assessment | People Ops | Updated `agent-review` document + summary comment |
| **Monthly** (last Friday) | Skill curation — prune dead skills, add missing skills, update assignments | People Ops | Sync list + approval request to CEO/CTO |
| **Quarterly** (end of quarter) | Full org health audit — model tiering, permissions, micro agent lifecycle | People Ops | Full org health report |

### Process

1. **Week 1:** People Ops wakes on cadence, audits last 30 days of agent activity
2. **Week 1 Output:** Quality review doc + skill sync proposal
3. **Week 2:** CEO/CTO approves skill changes, model changes
4. **Week 2-3:** Changes implemented (CEO/CTO for destructive, People Ops for non-destructive)
5. **Week 4:** Close out, schedule next cycle

### Automation Potential

Once micro agents are approved:
- **MA-1 Vault Health Agent** could automate health checks
- **People Ops** heartbeat could automate monthly audit data collection
- **Task Supervisor** heartbeat (600s) could provide continuous quality monitoring

---

## References

- Live API data from Paperclip (agents, skills, issues) — 2026-07-24
- `docs/agent-quality-review.md` — Prior quality review (RDT-239, Jul 16)
- `docs/skills-audit.md` — Prior skills audit (RDT-239, Jul 16)
- `docs/agents.md` — Agent inventory
- `docs/agent-monitoring-report.md` — Monitoring snapshot (Jul 16-17)
- `docs/people-ops-dashboard.md` — Org health dashboard
- `docs/model-tiering-review.md` — Model tiering analysis
