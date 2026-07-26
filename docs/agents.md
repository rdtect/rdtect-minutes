# Agent Inventory — RDT Organization

> **Owner:** People Ops (4f2b0b88)  
> **Last Updated:** 2026-07-17 (RDT-288 — CDO restored via API | RDT-289 — Follow-up created for recurring workspace error)  
> **Status:** ✅ Active — **CDO restored and idle; recurring root cause tracked in RDT-289**  
> **Related:** RDT-288 CDO Restoration | RDT-289 Fix Recurring Workspace Error | RDT-239 Quality Review + Skills Audit | RDT-99 Self-Org Review | RDT-237 Company Reset | RDT-262 Micro Agents | RDT-267 Implementation

---

## Agent Roster — System Data (Paperclip API)

| # | Agent | ID (short) | Role | Adapter | Model | Status | Heartbeat | Created | Last Activity |
|---|-------|-----------|------|---------|-------|--------|-----------|---------|---------------|
| 1 | **CEO** | `60bd9c45` | ceo | claude_local | claude-sonnet-4-6 | running | 300s | Apr 27 | Jul 16 15:15 |
| 2 | **CTO** | `11d48dee` | cto | claude_local | claude-sonnet-4-6 | running | 300s | Apr 27 | Jul 16 15:22 |
| 3 | **CDO** | `26402f1a` | general | claude_local | claude-sonnet-4-6 | ✅ **idle** (restored Jul 17 — RDT-288) | enabled | Apr 27 | Jul 16 11:42 (pre-re-error) |
| 4 | **Engineering Lead** | `e2cc964f` | engineer | claude_local | **claude-haiku-4-5-20251001** | running | 300s | Apr 27 | Jul 16 15:21 |
| 5 | **Research Lead** | `d2ce8469` | researcher | claude_local | **claude-haiku-4-5-20251001** | running | 300s | Apr 27 | Jul 16 15:24 |
| 6 | **Content Lead** | `4f55a3f8` | general | claude_local | **claude-haiku-4-5-20251001** | idle | 1800s | Apr 27 | Jul 16 14:57 |
| 7 | **CMO** | `c5f89f20` | cmo | hermes_local | deepseek-v4-flash | running | disabled | May 17 | **never** |
| 8 | **Task Supervisor** | `1b135854` | general | hermes_local | deepseek-v4-flash | idle | disabled | May 12 | Jul 16 11:48 |
| 9 | **Hermes Specialist** | `db733105` | general | hermes_local | deepseek/deepseek-v4-pro | running | disabled | May 15 | Jul 16 12:05 |
| 10 | **People Ops** | `4f2b0b88` | general | pi_local | deepseek/deepseek-v4-flash | running | disabled | May 7 | Jul 16 15:23 |

---

## Org Hierarchy (from system data)

```
                    CEO (60bd9c45) — claude-sonnet-4-6
                           │
              ┌────────────┼────────────┬──────────────┐
              ▼            ▼            ▼              ▼
          CTO (11d48dee)  CDO (26402f1a)  CMO (c5f89f20)  Task Supervisor
          claude-sonnet   claude-sonnet   deepseek-flash  (1b135854)
              │            │                              deepseek-flash
         ┌────┴────┐       ▼
         ▼         ▼    Content Lead
     Eng Lead    Research  (4f55a3f8)
     (e2cc964f)  Lead     claude-haiku
     claude-haiku (d2ce8469)
                  claude-haiku

     Hermes Specialist (db733105) — deepseek-v4-pro — reports to CEO
     People Ops (4f2b0b88) — deepseek-flash — reports to CEO
```

---

## Agent Detail

### 1. CEO (`60bd9c45`)
- **Role:** ceo | **Adapter:** claude_local | **Model:** claude-sonnet-4-6
- **Reports to:** None (top of org)
- **Status:** running | **Heartbeat:** 300s interval
- **Created:** Apr 27 | **Last HB:** Jul 16 15:15
- **Skills:** strategy, delegation, coordination, paperclip, para-memory-files
- **Permissions:** Can create agents, can create skills

### 2. CTO (`11d48dee`)
- **Role:** cto | **Adapter:** claude_local | **Model:** claude-sonnet-4-6
- **Reports to:** CEO
- **Status:** running | **Heartbeat:** 300s interval
- **Created:** Apr 27 | **Last HB:** Jul 16 15:22
- **Skills:** architecture, system-design, revenue-pitches, paperclip
- **Reports to:** CEO | **Directs:** Engineering Lead, Research Lead
- **Permissions:** Can create agents, can create skills

### 3. CDO (`26402f1a`)
- **Role:** general | **Adapter:** claude_local | **Model:** claude-sonnet-4-6
- **Reports to:** CEO
- **Status:** ✅ **idle** (restored 2026-07-17 via RDT-288 API recovery) | **Heartbeat:** enabled
- **Created:** Apr 27 | **Last HB:** Jul 16 11:42 (pre-re-error)
- **Skills:** brand-voice, design-quality, content-gates, paperclip
- **Reports to:** CEO | **Directs:** Content Lead
- **Permissions:** Can create agents, can create skills
- **Recovery history:**
  - **Error #1:** May 22 → Jul 16 (53 days, vault/config issue). Fixed by Task Supervisor Jul 16.
  - **Brief restoration:** Completed RDT-276 review at 22:20 Jul 16 (conditional-approved).
  - **Error #2:** 2026-07-17T00:13Z — re-errored after review. Workspace mismatch cleared via API.
  - **⚠️ Recurring pattern:** Agent errors after completing a task — workspace expectation mismatch in claude_local adapter. **3rd occurrence.** Root cause tracked in **RDT-289**.
- **Verification note:** Previous verification scripts (`scripts/verify-cdo-agent.sh` and voice gate review doc) were created during the brief restoration window but are now stale — the agent has re-errored.
- ✅ **Unblocked:** RDT-277 (CDO Review #2), RDT-265 (voice gate: rdtect.com O2) — CDO restored.
- **Recovery plan:** See RDT-288 restoration doc §13 for final recovery steps. Recurring root cause: see **RDT-289**.

### 4. Engineering Lead (`e2cc964f`)
- **Role:** engineer | **Adapter:** claude_local | **Model:** claude-haiku-4-5-20251001
- **Reports to:** CTO
- **Status:** running | **Heartbeat:** 300s interval
- **Created:** Apr 27 | **Last HB:** Jul 16 15:21
- **Skills:** tdd, codebase-inspection, github-pr-workflow, docx, pdf, pptx, xlsx
- **Permissions:** Cannot create agents, can create skills

### 5. Research Lead (`d2ce8469`)
- **Role:** researcher | **Adapter:** claude_local | **Model:** claude-haiku-4-5-20251001
- **Reports to:** CTO
- **Status:** running | **Heartbeat:** 300s interval
- **Created:** Apr 27 | **Last HB:** Jul 16 15:24
- **Skills:** research, discovery, analysis, paperclip
- **Permissions:** Cannot create agents, can create skills

### 6. Content Lead (`4f55a3f8`)
- **Role:** general | **Adapter:** claude_local | **Model:** claude-haiku-4-5-20251001
- **Reports to:** CDO
- **Status:** idle | **Heartbeat:** 1800s interval
- **Created:** Apr 27 | **Last HB:** Jul 16 14:57
- **Skills:** content-drafting, case-studies, insights, docx, pdf, pptx, xlsx
- **Permissions:** Cannot create agents, can create skills

### 7. CMO (`c5f89f20`)
- **Role:** cmo | **Adapter:** hermes_local | **Model:** deepseek-v4-flash
- **Reports to:** CEO
- **Status:** running | **Heartbeat:** disabled
- **Created:** May 17 | **Last HB:** **never** ⚠️
- **Skills:** marketing, growth, distribution, paperclip
- **Permissions:** Cannot create agents, can create skills
- **⚠️ Issue:** Zero activity in 60 days. Needs review.

### 8. Task Supervisor (`1b135854`)
- **Role:** general | **Adapter:** hermes_local | **Model:** deepseek-v4-flash
- **Reports to:** CEO
- **Status:** idle | **Heartbeat:** disabled
- **Created:** May 12 | **Last HB:** Jul 16 11:48
- **Skills:** (SOP enforcement, security monitoring — no individual skills listed)
- **Permissions:** Cannot create agents, can create skills

### 9. Hermes Specialist (`db733105`)
- **Role:** general | **Adapter:** hermes_local | **Model:** deepseek/deepseek-v4-pro
- **Reports to:** CEO
- **Status:** running | **Heartbeat:** disabled
- **Created:** May 15 | **Last HB:** Jul 16 12:05
- **Skills:** execution, infra, computer-use, paperclip
- **Permissions:** Cannot create agents, can create skills

### 10. People Ops (`4f2b0b88`)
- **Role:** general | **Adapter:** pi_local | **Model:** deepseek/deepseek-v4-flash
- **Reports to:** CEO
- **Status:** running | **Heartbeat:** disabled
- **Created:** May 7 | **Last HB:** Jul 16 15:23
- **Skills:** HR, retros, health, paperclip
- **Permissions:** Cannot create agents, can create skills

---

## Micro Agents

Micro agents are lightweight, single-purpose agents designed for specific recurring tasks. Main agents delegate work to them via Paperclip issues. See [`docs/micro-agents.md`](micro-agents.md) for full details.

| # | Agent | ID | Model | Purpose | Status | Approval | Delegated By |
|---|-------|-----|-------|---------|--------|----------|-------------|
| MA-1 | **Vault Health Agent** | `5fe0caf1` | deepseek-v4-flash | Monitor vault health, detect errors | 🟡 Pending Approval | [ad59177a](/RDT/approvals/ad59177a-9c0a-433d-8865-998ab90b467c) | Task Supervisor, CDO |
| MA-2 | **Meeting Minutes Agent** | `97cd2b4e` | deepseek-v4-pro | Capture and format meeting minutes | 🟡 Pending Approval | [d9cf45dc](/RDT/approvals/d9cf45dc-9962-4d90-9829-8b2825776676) | CDO, Content Lead, CTO |
| MA-3 | **Compression Agent** | `ba88f57c` | deepseek-v4-flash | Compress files/artifacts for PRs/issues | 🟡 Pending Approval | [f36b44b2](/RDT/approvals/f36b44b2-c5ba-45ff-a852-c72f52b073e9) | Engineering Lead, any agent |
| MA-4 | **Content Distillation Agent** | `0cfd2343` | deepseek-v4-pro | Distill long docs into summaries | 🟡 Pending Approval | [c9e80494](/RDT/approvals/c9e80494-f6e2-46d6-9e3f-7f3e45398906) | Research Lead, Content Lead |
| MA-5 | **Social Media Agent** | `36041b2d` | deepseek-v4-flash | Format/queue social posts | 🟡 Pending Approval | [ca9d3a57](/RDT/approvals/ca9d3a57-a6b2-498c-a022-2d8780432c2f) | CDO |
| MA-6 | **Cloudflare Deploy Agent** | `f5ab9d04` | deepseek-v4-flash | Execute CF Pages deployments | 🟡 Pending Approval | [07fc50c4](/RDT/approvals/07fc50c4-8300-4476-be0b-2d57eb5ee5ce) | Engineering Lead |
| MA-7 | **Zyeta Domain Agent** | `b634362c` | deepseek-v4-flash | Zyeta domain context lookups | 🟡 Pending Approval | [c412cfa8](/RDT/approvals/c412cfa8-70b3-4966-88b4-536238250ecb) | Research Lead, Engineering Lead |

**Status Key:** 📝 Proposed → 🟡 Pending Approval → ✅ Active → ❌ Archived

---

## Documents Index

| Document | Description | Status |
|----------|-------------|--------|
| `docs/agents.md` | Agent inventory (this file) | ✅ Updated Jul 16 |
| `docs/agent-quality-review.md` | Quality review — activity, output, idle detection | ✅ Updated Jul 16 |
| `docs/skills-audit.md` | Skills catalog audit — installed, used, missing, stale | ✅ Updated Jul 16 |
| `docs/micro-agents.md` | Micro agent definitions and lifecycle | ✅ Created Jul 16 (RDT-262) |
| `docs/delegation-guide.md` | Delegation patterns — how main agents delegate to micro agents | ✅ Created Jul 16 (RDT-262) |
| `docs/agent-monitoring-report.md` | Agent monitoring snapshot — health, activity, errors | ✅ Created Jul 16 (RDT-262) |
| `docs/model-tiering-review.md` | Model tiering analysis — cost, performance, recommendations | ✅ Created Jul 16 (RDT-262) |
| `docs/people-ops-dashboard.md` | People Ops dashboard | ✅ Updated Jul 16 |
| `docs/self-org-review.md` | Previous org review (RDT-99) | ✅ Complete May 14 |
