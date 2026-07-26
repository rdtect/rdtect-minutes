# People Ops Dashboard

> **Owner:** People Ops (4f2b0b88)  
> **Updated:** 2026-07-17  
> **Issues:** RDT-288 (Complete — CDO restoration verified) | RDT-289 (Proposed — Fix recurring workspace error) | RDT-239 (Complete) | RDT-262 (Active)  
> **Status:** ✅ Active

---

## Agent Roster (10 Full Agents + 7 Micro Agents)

### Full Agents

| Agent | Role | Status | Model | Last Activity |
|-------|------|--------|-------|--------------|
| CEO | ceo | ✅ running | claude-sonnet-4-6 | Jul 16 15:15 |
| CTO | cto | ✅ running | claude-sonnet-4-6 | Jul 16 15:22 |
| CDO | general | ✅ **idle** (restored Jul 17 — RDT-288; recurring root cause tracked in RDT-289) | claude-sonnet-4-6 | Jul 16 11:42 (pre-re-error) |
| Engineering Lead | engineer | ✅ running | claude-sonnet-4-6 | Jul 16 15:21 |
| Research Lead | researcher | ✅ running | claude-sonnet-4-6 | Jul 16 15:24 |
| Content Lead | general | ⏸️ idle | claude-sonnet-4-6 | Jul 16 14:57 |
| CMO | cmo | 🔴 no output | deepseek-v4-flash | **never** |
| Task Supervisor | general | ⏸️ idle | deepseek-v4-flash | Jul 16 11:48 |
| Hermes Specialist | general | ✅ running | deepseek/deepseek-v4-pro | Jul 16 12:05 |
| People Ops | general | ✅ running | deepseek/deepseek-v4-flash | Jul 16 15:23 |

### Proposed Micro Agents

| # | Agent | Purpose | Status | Delegated By |
|---|-------|---------|--------|-------------|
| MA-1 | Vault Health Agent | Monitor vault health | 📝 Proposed | Task Supervisor, CDO |
| MA-2 | Meeting Minutes Agent | Format meeting minutes | 📝 Proposed | CDO, Content Lead, CTO |
| MA-3 | Compression Agent | File/artifact compression | 📝 Proposed | Engineering Lead |
| MA-4 | Content Distillation Agent | Summarize long docs | 📝 Proposed | Research Lead, Content Lead |
| MA-5 | Social Media Agent | Queue social posts | 📝 Proposed | CMO/CDO (pending CMO decision) |
| MA-6 | Cloudflare Deploy Agent | CF Pages deployments | 📝 Proposed | Engineering Lead |
| MA-7 | Zyeta Domain Agent | Zyeta domain context | 📝 Proposed | Research Lead, Eng Lead |

→ Full detail: [`docs/agents.md`](agents.md) | [`docs/micro-agents.md`](micro-agents.md)

---

## Deliverables

### RDT-239 (Quality Review) — Complete

| Document | Description | Status |
|----------|-------------|--------|
| `docs/agents.md` | Agent inventory with roles, models, status | ✅ Complete |
| `docs/agent-quality-review.md` | Quality review — activity, output, idle detection | ✅ Complete |
| `docs/skills-audit.md` | Skills catalog audit — installed vs used vs missing | ✅ Complete |
| `docs/people-ops-dashboard.md` | This dashboard | ✅ Complete |
| `docs/rdt-239-recommendations-for-ceo.md` | CEO-facing recommendations requiring approval | ✅ Complete |
| `docs/self-org-review.md` | Prior org review (RDT-99) | ✅ Complete |

### RDT-262 (Micro Agents & Delegation) — In Progress

| Document | Description | Status |
|----------|-------------|--------|
| `docs/micro-agents.md` | Micro agent definitions, lifecycle, delegation patterns | ✅ Created |
| `docs/delegation-guide.md` | Delegation guide — how main agents delegate to micro agents | ✅ Created |
| `docs/agents.md` (Micro section) | Micro agent inventory added to agent roster | ✅ Updated |
| `docs/people-ops-dashboard.md` | This dashboard (RDT-262 tracking) | ✅ Updated |
| `docs/agent-monitoring-report.md` | Agent monitoring snapshot — health, activity, errors | ✅ Created |
| `docs/model-tiering-review.md` | Model tiering analysis — cost, performance, recommendations | ✅ Created |
| `docs/rdt-262-summary.md` | Summary and handoff to CEO/CTO for next steps | ✅ Created |

---

## Open Org Actions (Awaiting CEO/CTO)

### From RDT-239 (Carried Forward)

| # | Action | Priority | Status |
|---|--------|----------|--------|
| CMO-1 | Decide CMO fate: remove, merge, or re-activate | P0 | 🔴 Awaiting decision |
| RL-1 | Assign tasks to Research Lead | P1 | 🔴 Awaiting decision |
| CL-1 | Assign tasks to Content Lead | P1 | 🔴 Awaiting decision |
| SK-1 | Archive stale skills (dream, story, maintain, ingest) | P2 | 🔴 Awaiting approval |
| SK-2 | Create meeting-minutes skill | P2 | 🔴 Awaiting approval |
| SK-3 | Create zyeta-domain knowledge skill | P1 | 🔴 Awaiting approval |
| MT-1 | Review model tiering — see `docs/model-tiering-review.md` | P2 | 🔴 Awaiting review |
| HB-1 | Enable heartbeats for Task Supervisor, People Ops | P2 | 🔴 Awaiting decision |

### From RDT-262 (Micro Agents & Delegation)

| # | Action | Priority | Status |
|---|--------|----------|--------|
| MA-D1 | Create first micro agents in Paperclip (CEO/CTO action) | P1 | 🔴 Awaiting creation |
| MA-D2 | Review and approve micro agent proposals | P1 | 🔴 Awaiting CEO/CTO review |
| MA-D3 | Decide micro agent model tier — recommend deepseek-v4-flash default | P2 | 🔴 Awaiting decision |
| MA-D4 | Establish delegation cadence — on-demand or scheduled | P2 | 🔴 Awaiting decision |

### From RDT-262 (Model Tiering — `docs/model-tiering-review.md`)

| # | Action | Priority | Status |
|---|--------|----------|--------|
| MT-2 | Downgrade Engineering Lead to deepseek-v4-pro? | P2 | 🔴 Awaiting CTO decision |
| MT-3 | Downgrade Research Lead to deepseek-v4-pro? | P2 | 🔴 Awaiting CTO decision |
| MT-4 | Downgrade Content Lead to deepseek-v4-pro/flash? | P2 | 🔴 Awaiting CDO decision |
| MT-5 | Micro agent default model: all deepseek-v4-flash or mix? | P2 | 🔴 Awaiting CTO decision |

---

## Org Health Metrics

### RDT-288 (CDO Restoration) — ✅ Complete

| Document | Description | Status |
|----------|-------------|--------|
| `docs/rdt-288-cdo-restoration-verification.md` | CDO restoration verification + final resolution (§13) | ✅ Complete — agent idle |
| `docs/rdt-288-cdo-voice-gate-review-forty-nine-sessions.md` | Voice gate review (performed during brief restoration window) | ✅ Archived |
| `scripts/verify-cdo-agent.sh` | Verification script (now updated for idle status) | ✅ Updated |
| `docs/agents.md` (CDO entry updated) | CDO status updated to idle with RDT-289 reference | ✅ Updated |
| `docs/agent-monitoring-report.md` | Monitoring report updated | ✅ Updated |
| `docs/people-ops-dashboard.md` | This dashboard (RDT-288/RDT-289 tracking) | ✅ Updated |

### RDT-289 (Fix CDO Recurring Workspace Error) — 📝 Proposed

| Document | Description | Status |
|----------|-------------|--------|
| `docs/rdt-289-fix-cdo-recurring-workspace-error.md` | Root cause analysis, proposed solutions, action plan | ✅ Created |
| `docs/agents.md` (CDO entry updated) | References RDT-289 for recurring root cause | ✅ Updated |

---

## Open Org Actions (Awaiting CEO/CTO)

### From RDT-239 (Carried Forward)

| # | Action | Priority | Status |
|---|--------|----------|--------|
| CMO-1 | Decide CMO fate: remove, merge, or re-activate | P0 | 🔴 Awaiting decision |
| RL-1 | Assign tasks to Research Lead | P1 | 🔴 Awaiting decision |
| CL-1 | Assign tasks to Content Lead | P1 | 🔴 Awaiting decision |
| SK-1 | Archive stale skills (dream, story, maintain, ingest) | P2 | 🔴 Awaiting approval |
| SK-2 | Create meeting-minutes skill | P2 | 🔴 Awaiting approval |
| SK-3 | Create zyeta-domain knowledge skill | P1 | 🔴 Awaiting approval |
| MT-1 | Review model tiering — see `docs/model-tiering-review.md` | P2 | 🔴 Awaiting review |
| HB-1 | Enable heartbeats for Task Supervisor, People Ops | P2 | 🔴 Awaiting decision |

### From RDT-262 (Micro Agents & Delegation)

| # | Action | Priority | Status |
|---|--------|----------|--------|
| MA-D1 | Create first micro agents in Paperclip (CEO/CTO action) | P1 | 🔴 Awaiting creation |
| MA-D2 | Review and approve micro agent proposals | P1 | 🔴 Awaiting CEO/CTO review |
| MA-D3 | Decide micro agent model tier — recommend deepseek-v4-flash default | P2 | 🔴 Awaiting decision |
| MA-D4 | Establish delegation cadence — on-demand or scheduled | P2 | 🔴 Awaiting decision |

### From RDT-262 (Model Tiering — `docs/model-tiering-review.md`)

| # | Action | Priority | Status |
|---|--------|----------|--------|
| MT-2 | Downgrade Engineering Lead to deepseek-v4-pro? | P2 | 🔴 Awaiting CTO decision |
| MT-3 | Downgrade Research Lead to deepseek-v4-pro? | P2 | 🔴 Awaiting CTO decision |
| MT-4 | Downgrade Content Lead to deepseek-v4-pro/flash? | P2 | 🔴 Awaiting CDO decision |
| MT-5 | Micro agent default model: all deepseek-v4-flash or mix? | P2 | 🔴 Awaiting CTO decision |

### From RDT-288 (CDO Restoration) — ✅ Complete

| # | Action | Priority | Status |
|---|--------|----------|--------|
| CDO-A1 | CDO to confirm voice gate parameters (briefing questions) | P0 | ⏳ Awaiting CDO response — due 7/18 |
| CDO-A2 | Content Lead to receive task direction from CDO | P1 | ⏳ Awaiting CDO direction |
| CDO-A3 | Approve MA-1 Vault Health Agent (prevent recurrence) | P1 | 🔴 Awaiting CEO/CTO approval |
| CDO-A4 | Enable Task Supervisor heartbeat for proactive monitoring | P2 | 🔴 Awaiting CEO decision |

### From RDT-289 (Fix Recurring Workspace Error) — 📝 Proposed

| # | Action | Priority | Status |
|---|--------|----------|--------|
| CDO-R1 | Assign CDO default project workspace (Option A) | P0 | 🔴 Proposed — see RDT-289 doc §Recommended |
| CDO-R2 | Audit claude_local adapter workspace resolution code | P1 | 🔴 Proposed — Engineering Lead |
| CDO-R3 | Implement graceful fallback instead of crash | P1 | 🔴 Proposed — Engineering Lead |
| CDO-R4 | Test with no-op task before next real review | P1 | 🔴 Pending workspace fix |

---

## Org Health Metrics

| Metric | Current |
|--------|---------|
| Total full agents | 10 |
| Proposed micro agents | 7 |
| Active (output today) | 8 |
| Idle (zero output) | 1 (CMO) |
| In error | 0 |
| Recently recovered (verified) | 2 (CDO — RDT-288 ✅, Task Supervisor) |
| Issues completed (all time) | 113 |
| Issues updated last 7 days | 71 |
| Skills in catalog | 17 |
| Skills with attached agents | 3 |
| Unused skills (60+ days) | 8 |
| Missing skills identified | 5 |
| Micro agents documented | 7 (all proposed) |

---

## Review Cadence (Proposed)

| Interval | Review Type | Owner |
|----------|-------------|-------|
| Monthly | New hire check-in (first 30 days) | People Ops |
| Quarterly | Full agent quality review | People Ops |
| Ad-hoc | CEO-triggered reviews | CEO |
