# Micro Agents — RDT Organization

> **Owner:** People Ops (4f2b0b88)  
> **Issue:** RDT-262  
> **Status:** ✅ Active  
> **Updated:** 2026-07-16  
> **Concept:** Lightweight, single-purpose agents that handle specific recurring tasks. Main agents delegate work to micro agents via Paperclip issues, gaining efficiency through specialization.

---

## 1. What is a Micro Agent?

A **micro agent** is a focused, single-purpose agent designed to handle one specific recurring task or domain. Unlike full agents (CEO, CTO, CDO, etc.) which have broad roles and orchestration responsibilities, micro agents:

- **Do one thing well** — Each micro agent has a narrow, well-defined scope
- **Are lightweight** — No org-wide permissions; run on-demand via delegated issues
- **Are disposable/recreatable** — If one fails, a main agent can spawn a replacement
- **Require minimal instruction** — Their entire context fits in their agent definition + a single skill file

### When to Use a Micro Agent

| Use Case | Example | Better as Micro Agent? |
|----------|---------|----------------------|
| Recurring narrow task | Daily vault health check | ✅ Yes — fully defined scope |
| One-off complex task | Research Zyeta domain model | ❌ No — use a full agent (Research Lead) |
| File format conversion | Compress screenshots for a PR | ✅ Yes — no judgment needed |
| Creative/content work | Draft a blog post | ❌ No — needs Content Lead's broader context |
| Monitoring/alerting | Check heartbeat status | ✅ Yes — simple, repeatable |

---

## 2. Proposed Micro Agents

Below are the micro agents identified from the RDT-239 audit gaps and the existing unused skills. Each is prioritized by need.

### Tier 1: Immediate Need (P1)

#### MA-1: Vault Health Agent
| Field | Value |
|-------|-------|
| **Purpose** | Monitor vault health, detect errors, report status |
| **Trigger** | Daily recurring check or on-demand by CDO/Task Supervisor |
| **Skill files** | `vault-health`, `vault-audit` (both currently unused) |
| **Output** | Vault health report → issues or dashboard |
| **Delegated by** | Task Supervisor, CDO |
| **Rationale** | Vault has had errors before (CDO was in error 53 days). Proactive monitoring prevents recurrence. |

#### MA-2: Meeting Minutes Agent
| Field | Value |
|-------|-------|
| **Purpose** | Capture, format, and archive meeting minutes |
| **Trigger** | On-demand by any agent after a meeting |
| **Skill files** | `compress` (for audio/file reduction), `distill` (for summarization) |
| **Output** | Formatted meeting minutes → stored in vault/docs |
| **Delegated by** | CDO, Content Lead, CTO |
| **Rationale** | No agent currently has a meeting-minutes skill. This is a common need across the org. |

#### MA-3: Compression / File Ops Agent
| Field | Value |
|-------|-------|
| **Purpose** | Compress images, screenshots, and artifacts for PRs/issues |
| **Trigger** | On-demand when an agent needs to attach media to an issue or PR |
| **Skill files** | `compress` |
| **Output** | Compressed file artifact → attached to issue |
| **Delegated by** | Engineering Lead, any agent producing visual artifacts |
| **Rationale** | The `compress` skill exists but has never been used in 63 days. A micro agent would activate it. |

### Tier 2: Near-Term Value (P2)

#### MA-4: Content Distillation Agent
| Field | Value |
|-------|-------|
| **Purpose** | Distill long documents, research reports, or transcripts into concise summaries |
| **Trigger** | On-demand by Research Lead, Content Lead, or CTO |
| **Skill files** | `distill`, `story` (for narrative extraction) |
| **Output** | Distilled summary → attached to source issue |
| **Delegated by** | Research Lead, Content Lead, CTO |
| **Rationale** | Research Lead is underutilized; this micro agent would help process research output faster. |

#### MA-5: Social Media Publishing Agent
| Field | Value |
|-------|-------|
| **Purpose** | Format and queue social media posts from approved content |
| **Trigger** | On-demand by CMO (if retained) or CDO |
| **Skill files** | (new — `social-media-publishing` to be created) |
| **Output** | Draft posts → submitted for approval |
| **Delegated by** | CMO, CDO |
| **Rationale** | Social media distribution is a gap. This micro agent bridges it without requiring a full CMO. |

### Tier 3: Future / If Needed (P3)

#### MA-6: Cloudflare Deploy Agent
| Field | Value |
|-------|-------|
| **Purpose** | Execute Cloudflare Pages deployments from CI artifacts |
| **Trigger** | After CI passes, on-demand by Engineering Lead |
| **Skill files** | (new — `cloudflare-deployment` to be created) |
| **Output** | Deployment status → issue update |
| **Delegated by** | Engineering Lead |
| **Rationale** | Engineering Lead currently does this manually. Automation would save time. |

#### MA-7: Zyeta Domain Agent
| Field | Value |
|-------|-------|
| **Purpose** | Domain-specific knowledge base for Zyeta Construction / Zyeta DX projects |
| **Trigger** | On-demand by Research Lead or Engineering Lead |
| **Skill files** | (new — `zyeta-domain` to be created) |
| **Output** | Domain context summaries, term lookups |
| **Delegated by** | Research Lead, Engineering Lead |
| **Rationale** | Zyeta domain knowledge is a known gap (RDT-239 S3). A dedicated micro agent is lighter than retraining all agents. |

---

## 3. Micro Agent Lifecycle

```
┌─────────────┐
│  1. CREATE   │  Main agent defines the micro agent's purpose, skills, and delegation rules
└──────┬──────┘
       ▼
┌─────────────┐
│  2. REGISTER │  Micro agent is documented in this file + agents.md inventory
└──────┬──────┘
       ▼
┌─────────────┐
│  3. DELEGATE │  Main agent creates a Paperclip issue assigned to the micro agent
└──────┬──────┘
       ▼
┌─────────────┐
│  4. EXECUTE  │  Micro agent completes the task, updates the issue
└──────┬──────┘
       ▼
┌─────────────┐
│  5. REVIEW   │  Main agent reviews output, closes issue, or re-delegates
└─────────────┘
```

### Creating a Micro Agent

Currently, only **CEO** and **CTO** have `Can create agents` permission. A micro agent is created via:

1. **Define** the agent's purpose and scope (use this document as template)
2. **Register** by adding to `docs/agents.md` under "Micro Agents" section
3. **Create** the agent via Paperclip API (CEO/CTO action)
4. **Assign** any skill files needed
5. **Announce** to the org so main agents know to delegate

---

## 4. Delegation Patterns

### Pattern A: Simple Delegate (Fire-and-Forget)

```
Main Agent → Creates issue for micro agent → Micro agent completes → Issue closed
```

**Best for:** Compression, file ops, social media posting
**Example:** "MA-3: Compress these 3 screenshots and attach to RDT-123"

### Pattern B: Delegate-and-Review

```
Main Agent → Creates issue for micro agent → Micro agent completes + reports → Main reviews → Issue accepted/revised
```

**Best for:** Meeting minutes, content distillation
**Example:** "MA-2: Take these meeting notes and format them into minutes"

### Pattern C: Standing Delegate (Recurring)

```
Main Agent → Creates recurring issue → Micro agent runs on schedule → Auto-updates
```

**Best for:** Vault health checks, heartbeat monitoring
**Example:** "MA-1: Run vault health check daily at 0900 UTC"

---

## 5. How Main Agents Learn to Delegate

### Updated Instructions for Each Agent

When a main agent encounters a task that matches a micro agent's scope, they should:

1. **Check** `docs/micro-agents.md` to see if a micro agent exists for the task
2. **Create** a Paperclip issue with:
   - **Title prefix:** `[MA-N]` (e.g., `[MA-1] Run vault health check`)
   - **Assignee:** The micro agent's ID
   - **Priority:** Matching the task priority
   - **Description:** Clear, complete input (what the micro agent needs to do its job)
3. **Attach** any input files/resources to the issue
4. **Set** the due date if time-sensitive
5. **Monitor** the issue for completion (or set a watch)

### What NOT to Delegate

- **Orchestration decisions** — Keep with main agents (CEO, CTO, CDO)
- **Cross-domain tasks** — If a task spans multiple micro agents, the main agent should sequence them
- **High-judgment content** — Brand voice decisions stay with CDO
- **Security-sensitive operations** — Stay with Task Supervisor or CEO

---

## 6. Micro Agent Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task completion rate | >90% within expected time | Issue close rate per micro agent |
| Re-delegation rate | <10% (low rework) | Issues reopened / re-assigned |
| Delegation adoption | >50% of applicable tasks use micro agent | Audit issue titles for `[MA-N]` prefix |
| Time saved | >20% reduction in main agent task time | Before/after comparison |

---

## 7. Open Decisions (Awaiting CEO/CTO)

| # | Decision | Options | Asked By |
|---|----------|---------|----------|
| MD-1 | Who creates micro agents in Paperclip? CEO only, or delegate to CTO? | CEO, CTO, or both | People Ops |
| MD-2 | Should MA-5 (Social Media) exist if CMO is removed? | Yes (replace CMO), No (merge to CDO) | People Ops |
| MD-3 | Heartbeat interval for micro agents? | None (on-demand only) or periodic | People Ops |
| MD-4 | Micro agent model tier — all on deepseek-flash, or mix? | deepseek-flash only (cheap) or vary by task | People Ops |

---

## References

- `docs/agents.md` — Full agent inventory (including micro agents, once added)
- `docs/agent-quality-review.md` — Quality review that identified gaps
- `docs/skills-audit.md` — Skills audit showing 8 unused skills
- `docs/people-ops-dashboard.md` — People Ops dashboard
- RDT-239 — Parent quality review issue
- RDT-99 — Self-organization review
