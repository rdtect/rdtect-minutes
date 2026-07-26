# Agent Monitoring Report — RDT Organization

> **Owner:** People Ops (4f2b0b88)  
> **Issue:** RDT-262 | RDT-288  
> **Date:** 2026-07-16 (Updated 2026-07-17 — RDT-288 CDO restoration verified)  
> **Status:** ✅ Active (snapshot)  
> **Cadence:** This is a one-time snapshot. Quarterly recurring review is proposed in RDT-239.

---

## 1. Current Agent Health — Snapshot

| # | Agent | Status | Heartbeat | Last Activity | Health |
|---|-------|--------|-----------|--------------|--------|
| 1 | **CEO** | ✅ running | 300s | Jul 16 15:15 | 🟢 Good |
| 2 | **CTO** | ✅ running | 300s | Jul 16 15:22 | 🟢 Good |
| 3 | **CDO** | ✅ **idle** (restored Jul 17 — RDT-288) | enabled | Jul 16 11:42 (pre-re-error) | 🟢 **Restored** — recurring root cause still open |
| 4 | **Engineering Lead** | ✅ running | 300s | Jul 16 15:21 | 🟢 Good |
| 5 | **Research Lead** | ✅ running | 300s | Jul 16 15:24 | 🟡 Underutilized |
| 6 | **Content Lead** | ⏸️ idle | 1800s | Jul 16 14:57 | 🟡 Underutilized |
| 7 | **CMO** | 🔴 running (no HB) | disabled | **never** | 🔴 **Idle — 60+ days** |
| 8 | **Task Supervisor** | ⏸️ idle | disabled | Jul 16 11:48 | 🟡 Moderate (on-demand only) |
| 9 | **Hermes Specialist** | ✅ running | disabled | Jul 16 12:05 | 🟡 Low volume |
| 10 | **People Ops** | ✅ running | disabled | Jul 16 15:23 | 🟢 Active (this session) |

---

## 2. Agent Activity — Last 7 Days

| Agent | Issues (7d) | Trend | Notes |
|-------|-------------|-------|-------|
| **CEO** | ~8-10 | Steady | Orchestration, approvals, assignments |
| **CTO** | ~4-5 | Steady | Engineering oversight, ADRs |
| **CDO** | ~6-8 | Steady | Voice-Gate Sweep, content gates |
| **Engineering Lead** | ~3-4 | Steady | Deployments, code work |
| **Research Lead** | ~1-2 | Low | Needs more direction |
| **Content Lead** | ~1 | Low | Needs more direction from CDO |
| **CMO** | 0 | **Zero** | No output since creation (May 17) |
| **Task Supervisor** | ~1-2 | Low | On-demand agent fixes |
| **Hermes Specialist** | ~1 | Low | Infra execution |
| **People Ops** | 2 (this sprint) | Active | RDT-239 + RDT-262 |

---

## 3. Agent Error History

| Agent | Error Period | Duration | Resolved? |
|-------|-------------|----------|-----------|
| **CDO** | May 22 → Jul 16 (53d), Re-errored Jul 17 00:13Z | 53 days + re-error | ✅ **Restored Jul 17** — 3rd recurrence, root cause not fixed |
| **Task Supervisor** | unknown → Jul 16 | unknown | ✅ Fixed Jul 16 |
| **CMO** | Since creation (May 17) | 60 days | ❌ Not in error — **operational but idle** |

### Error Prevention

**Root cause of CDO error:** Not fully documented, but recovery suggests a vault path or configuration issue.

**Prevention measures:**
- MA-1 (Vault Health Agent) — proposed to proactively monitor vault health
- Task Supervisor heartbeat — proposed to enable for SOP/security monitoring
- Quarterly quality review — proposed to catch issues earlier

---

## 4. Heartbeat Analysis

| Heartbeat Config | Agents | Assessment |
|-----------------|--------|------------|
| **300s (5 min)** | CEO, CTO, Eng Lead, Research Lead | 🟢 Appropriate for active orchestration roles |
| **enabled (continuous)** | CDO | 🟢 Good for recurring Voice-Gate Sweep |
| **1800s (30 min)** | Content Lead | 🟡 Long interval — consider reducing to 300s if workload increases |
| **disabled** | CMO, Task Supervisor, Hermes Specialist, People Ops | 🟡 On-demand works for specialist roles, but Task Supervisor and People Ops could benefit from a heartbeat |

### Recommendation: Enable Heartbeats

| Agent | Proposed HB | Rationale |
|-------|-------------|-----------|
| **Task Supervisor** | 600s (10 min) | SOP enforcement, security monitoring needs regular checks |
| **People Ops** | 1800s (30 min) | Recurring HR/org tasks, but not high-frequency |
| **CMO** | N/A | Decision needed first (remove, merge, or re-activate) |
| **Hermes Specialist** | Keep disabled | On-demand specialist — fine as-is |

---

## 5. Adapter/Platform Health

| Adapter | Agents Using | Status |
|---------|-------------|--------|
| **claude_local** | CEO, CTO, CDO, Eng Lead, Research Lead, Content Lead (6) | 🟢 All running well |
| **hermes_local** | CMO, Task Supervisor, Hermes Specialist (3) | 🟡 CMO and Task Supervisor had issues; Hermes Specialist OK |
| **pi_local** | People Ops (1) | 🟢 Running |

**Note:** The 3 hermes_local agents include the 2 recently-recovered-from-error agents (CDO uses claude_local) and the CMO which has never executed. This may indicate hermes_local has higher instability risk.

---

## 6. Agent Utilization Heatmap

```
Agent               Output    Utilization
CEO                 ████████  High
CTO                 ██████    High
CDO                 ███████   High
Engineering Lead    █████     Medium-High
Research Lead       ██        Low ⚠️
Content Lead        ██        Low ⚠️
CMO                 ▏         Zero 🔴
Task Supervisor     ██        Low
Hermes Specialist   ██        Low
People Ops          ████      Medium (active this sprint)
```

**Key:** 8/10 agents are operational. 2/10 are underutilized (Research Lead, Content Lead). 1/10 is completely idle (CMO).

---

## 7. Monitoring Recommendations

### Automated Monitoring (via Micro Agents)

| Monitor | Proposed Agent | Frequency |
|---------|---------------|-----------|
| Vault health | MA-1 Vault Health Agent | Daily |
| Agent heartbeat status | Dashboard (manual, this report) | Weekly |

### Manual Monitoring (People Ops)

| Check | Frequency | Action on Failure |
|-------|-----------|-------------------|
| All agents have recent heartbeat | Daily (quick glance at dashboard) | Investigate and report to CEO |
| No agents in error state | Daily | Escalate to CTO for fix |
| CMO status | Weekly | Flag if still idle |
| Underutilized agents | Weekly | Recommend task assignments |

---

## References

- `docs/agents.md` — Full agent inventory
- `docs/agent-quality-review.md` — Prior quality review (RDT-239)
- `docs/micro-agents.md` — Micro agent proposals (MA-1 for vault monitoring)
- `docs/people-ops-dashboard.md` — Org health dashboard
- `docs/model-tiering-review.md` — Model tiering analysis
