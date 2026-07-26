# Agent Quality Review — RDT Organization

> **Reviewer:** People Ops (4f2b0b88)  
> **Date:** 2026-07-16  
> **Issue:** RDT-239  
> **Status:** ✅ Complete  
> **Parent:** RDT-237 (Company Reset)  
> **Scope:** Full audit of all 10 agents: activity, output quality, idle detection, recommendations.

---

## 1. Agent Roster — System Data

| # | Agent | ID | Role | Adapter | Model | Status | Heartbeat | Created | Last HB |
|---|-------|----|------|---------|-------|--------|-----------|---------|---------|
| 1 | **CEO** | `60bd9c45` | ceo | claude_local | claude-sonnet-4-6 | running | 300s | Apr 27 | Jul 16 15:15 |
| 2 | **CTO** | `11d48dee` | cto | claude_local | claude-sonnet-4-6 | running | 300s | Apr 27 | Jul 16 15:22 |
| 3 | **CDO** | `26402f1a` | general | claude_local | claude-sonnet-4-6 | running | enabled | Apr 27 | Jul 16 11:42 |
| 4 | **Engineering Lead** | `e2cc964f` | engineer | claude_local | claude-sonnet-4-6 | running | 300s | Apr 27 | Jul 16 15:21 |
| 5 | **Research Lead** | `d2ce8469` | researcher | claude_local | claude-sonnet-4-6 | running | 300s | Apr 27 | Jul 16 15:24 |
| 6 | **Content Lead** | `4f55a3f8` | general | claude_local | claude-sonnet-4-6 | idle | 1800s | Apr 27 | Jul 16 14:57 |
| 7 | **CMO** | `c5f89f20` | cmo | hermes_local | deepseek-v4-flash | running | disabled | May 17 | never |
| 8 | **Task Supervisor** | `1b135854` | general | hermes_local | deepseek-v4-flash | idle | disabled | May 12 | Jul 16 11:48 |
| 9 | **Hermes Specialist** | `db733105` | general | hermes_local | deepseek/deepseek-v4-pro | running | disabled | May 15 | Jul 16 12:05 |
| 10 | **People Ops** | `4f2b0b88` | general | pi_local | deepseek/deepseek-v4-flash | running | disabled | May 7 | Jul 16 15:23 |

---

## 2. Activity Analysis — Last 30 Days

Based on the Paperclip issue tracker (200+ issues), here is the task activity per agent:

| Agent | Issues Done (30d) | Issues In Progress | Last Activity | Activity Band |
|-------|------------------|-------------------|---------------|---------------|
| **CEO** | ~30 (orchestration, approvals, assignments) | 6 in_progress board-wide | Jul 16 15:15 | 🟢 High |
| **CTO** | ~15 (engineering oversight, ADRs, evaluations) | 0 direct | Jul 16 15:22 | 🟢 High |
| **CDO** | ~25 (Voice-Gate Sweep recurring, content gates) | 0 direct | Jul 16 11:42 | 🟢 High |
| **Engineering Lead** | ~10 (deployments, Cloudflare config, code work) | 2 in_review | Jul 16 15:21 | 🟢 High |
| **Research Lead** | ~5 (research tasks) | 0 direct | Jul 16 15:24 | 🟡 Moderate |
| **Content Lead** | ~3 (content tasks) | 0 direct | Jul 16 14:57 | 🟡 Moderate |
| **CMO** | 0 | 0 | never (created May 17) | 🔴 Idle |
| **Task Supervisor** | ~5 (agent fixes, SOP work) | 0 direct | Jul 16 11:48 | 🟡 Moderate |
| **Hermes Specialist** | ~3 (infra, execution tasks) | 0 direct | Jul 16 12:05 | 🟡 Moderate |
| **People Ops** | 2 (this review + previous audit) | 1 (RDT-239) | Jul 16 15:23 | 🟡 Moderate |

### Idle Agent Detection

| Agent | Status | Days Since Last HB | Tasks Completed (30d) | Verdict |
|-------|--------|-------------------|----------------------|---------|
| **CMO** | running | **NEVER had a heartbeat** | 0 | 🔴 **IDLE — ZERO OUTPUT** |
| Task Supervisor | idle | ~4 hours | ~5 | 🟡 Active today |
| Content Lead | idle | ~30 min | ~3 | 🟢 Active today |
| Others | running | <4 hours | Varies | 🟢 Active |

> **🔴 CRITICAL FINDING: CMO (c5f89f20) has never executed a single heartbeat since creation (May 17, 2026 — 60 days). Zero tasks completed. Zero output.**

---

## 3. Output Quality Assessment

| Agent | Recent Deliverables | Quality Assessment |
|-------|--------------------|--------------------|
| **CEO** | Issue assignments, board approvals, escalations, company config | ✅ Strong orchestration. Active daily. |
| **CTO** | ADRs, agent manager chains, RDT-104 evaluation, hire requests | ✅ Good technical direction. ADRs well-structured. |
| **CDO** | Voice-Gate Sweep (recurring), content gates, brand oversight, CDO fix | ✅ Recurring sweep is working. Agent was in error, now fixed. |
| **Engineering Lead** | Cloudflare Pages deploy, aero-push-worker deploy, CF token config | ✅ Shipping production changes. Quality seems solid. |
| **Research Lead** | Discovery work, research tasks | ⚠️ Few concrete deliverables visible. May be underutilized. |
| **Content Lead** | Content drafting tasks | ⚠️ Low throughput. May need clearer direction from CDO. |
| **CMO** | None | ❌ No output to assess. |
| **Task Supervisor** | Agent error fixes, SOP investigations | ✅ Fixed CDO and Task Supervisor agent errors. |
| **Hermes Specialist** | Infra tasks, execution | ✅ Executing but low volume. |
| **People Ops** | Agent inventory, quality review, skills audit | ✅ In progress (this document). |

---

## 4. Agent Health Issues

| Agent | Issue | Severity | Status |
|-------|-------|----------|--------|
| **CMO** | Zero activity — 60 days with no heartbeat. May be misconfigured or unnecessary. | 🔴 P0 | New finding |
| **CDO** | Was in error state from May 22 until Jul 16 (53 days). Root cause: vault path/config issue. | 🟡 P1 | ✅ Fixed Jul 16, **verified Jul 17 (RDT-288)** — see `docs/rdt-288-cdo-restoration-verification.md` |
| **Task Supervisor** | Was in error state, recently fixed | 🟡 P1 | ✅ Fixed Jul 16 |
| **Content Lead** | Heartbeat interval is 1800s (30 min) — longest of all agents | 🟢 Info | Monitor |
| **Hermes Specialist** | No heartbeat enabled, runs on-demand only | 🟢 Info | As designed |

---

## 5. Recommendations

### Must Do (P0)
1. **🔴 CMO: Investigate and decide** — Either assign tasks, enable heartbeat, or remove/merge. 60 days with zero output is not acceptable.
2. **Assign active tasks** to Research Lead and Content Lead — both are underutilized.

### Should Do (P1)
3. **Enable heartbeat** for at least People Ops and Task Supervisor so they wake autonomously.
4. **Create Engineering Lead dashboard** in the repo for visibility.
5. **Finalize SOP documentation** (carried from G7 / RDT-99).

### Consider (P2)
6. **Merge CMO into CDO** if the marketing function overlaps with content/brand.
7. **Audit agent models** — 5 agents use claude-sonnet-4-6, 3 use deepseek-v4-flash, 1 uses deepseek-v4-pro. Consider cost optimization.
8. **Establish quarterly quality review cadence** (this is RDT-239 — make it recurring).

---

## 6. Org Health Summary

| Metric | Value |
|--------|-------|
| Total agents | 10 |
| Active (running + recent output) | 8 |
| Idle (zero output) | 1 (CMO) |
| In error | 0 |
| Recently recovered from error | 2 (CDO, Task Supervisor) |
| Issues completed (all time) | 112 |
| Issues completed (last 30 days) | ~75 |
| Issues in progress | 6 |
| Issues blocked | 6 |
| Issues in review | 13 |

---

## References

- RDT-99 Self-Organization Review → `docs/self-org-review.md`
- RDT-239 Agent Inventory → `docs/agents.md`
- RDT-239 Skills Audit → `docs/skills-audit.md`
- RDT-239 People Ops Dashboard → `docs/people-ops-dashboard.md`
