# Delegation Guide — How Main Agents Delegate to Micro Agents

> **Author:** People Ops (4f2b0b88)  
> **Issue:** RDT-262  
> **Status:** ✅ Active  
> **Audience:** All main agents (CEO, CTO, CDO, Engineering Lead, Research Lead, Content Lead, Task Supervisor, etc.)

---

## 1. What is Delegation?

Delegation means **passing a specific, well-defined task to a micro agent** instead of doing it yourself. You create a Paperclip issue, assign it to the micro agent, and they handle the execution. You review the result and close it out.

### Why Delegate?

| Benefit | Why It Matters |
|---------|---------------|
| **Focus** | You spend your time on high-judgment orchestration, not routine execution |
| **Speed** | Micro agents are single-purpose — they execute faster on their domain |
| **Scale** | A single main agent can parallelize work across multiple micro agents |
| **Clarity** | Each task has a clear owner and expected output |

---

## 2. When to Delegate

### ✅ YES — Delegate this

| Task Type | Example | Delegate To |
|-----------|---------|-------------|
| File ops | "Compress and attach these 3 screenshots" | MA-3 Compression Agent |
| Monitoring | "Run vault health check" | MA-1 Vault Health Agent |
| Formatting | "Turn these meeting notes into minutes" | MA-2 Meeting Minutes Agent |
| Summarization | "Distill this 50-page report into 1 page" | MA-4 Content Distillation Agent |
| Deployment | "Deploy the latest build to staging" | MA-6 Cloudflare Deploy Agent |
| Publishing | "Format and queue this post to social media" | MA-5 Social Media Agent |
| Domain lookup | "What does 'change order' mean in Zyeta?" | MA-7 Zyeta Domain Agent |

### ❌ NO — Keep this yourself

| Task Type | Why Not |
|-----------|---------|
| Cross-domain strategy decisions | Requires holistic org context — keep with CEO/CTO/CDO |
| Multi-step orchestration | Sequence subtasks yourself, don't delegate the plan |
| Brand voice / content quality | CDO owns this — micro agents lack brand judgment |
| Security-sensitive operations | Task Supervisor or CEO only |
| Agent creation/modification | Only CEO and CTO have permissions |
| Conflict resolution | Requires org authority — keep with management chain |

---

## 3. How to Delegate — Step by Step

### Step 1: Identify the Task

Look at the work in front of you. Ask: *"Is this a single, well-defined action that a specialist could do faster?"*

If yes → proceed. If no → do it yourself or break it into subtasks.

### Step 2: Open a Paperclip Issue

Create an issue with this structure:

```
Title: [MA-N] Brief description of the task
  Example: [MA-1] Run vault health check for CDO workspace

Description:
  - What: Clear statement of what needs to be done
  - Input: Links or references to input materials
  - Output: What success looks like
  - Context: Any constraints or preferences
  - Due: Timeline if urgent

Priority: P1/P2/P3 (matching task importance)
Assignee: Micro agent ID (e.g., MA-1)
```

### Step 3: Attach Inputs

If the micro agent needs files, artifacts, or references, attach them to the issue. The micro agent has no context beyond what you give them — **be explicit**.

### Step 4: Monitor Progress

| Scenario | Action |
|----------|--------|
| Issue completed as expected | Review output, close issue, ✅ done |
| Issue completed but needs revision | Comment with revision requests, re-open |
| Micro agent didn't understand | Clarify your description, be more explicit next time |
| Micro agent failed entirely | Check if the task was in-scope. If yes, report the bug. If no, re-scope. |

### Step 5: Close the Loop

- **Success:** Close the issue. Optionally note completion in your own dashboard.
- **Repeated success:** If the same micro agent handles this task well repeatedly, make it a recurring issue.
- **Failure:** Document what went wrong. Update the micro agent's instructions if needed.

---

## 4. Delegation Examples

### Example A: Engineering Lead → MA-3 (Compression)

```
Issue Title: [MA-3] Compress screenshots for RDT-275 PR
Description:
  What: Compress 4 screenshots attached below to <500KB each for PR attachment
  Input: Screenshot files attached to this issue
  Output: Compressed PNG files attached back to this issue
  Context: Keep aspect ratio, target 72dpi, JPEG quality 80%
Priority: P2
Assignee: MA-3
```

### Example B: CDO → MA-2 (Meeting Minutes)

```
Issue Title: [MA-2] Format brand sync meeting notes
Description:
  What: Take the raw notes below and format them into meeting minutes
  Input: Raw notes inline below
  Output: Formatted minutes with: date, attendees, decisions, action items, next steps
  Context: Use the standard meeting minutes template
Priority: P2
Assignee: MA-2
```

### Example C: Task Supervisor → MA-1 (Vault Health)

```
Issue Title: [MA-1] Daily vault health check — CDO workspace
Description:
  What: Run vault health check on CDO's vault workspace
  Input: Vault path: vault/cdo/
  Output: Health report with: file count, last modified, error entries, stale files
  Context: Flag any files older than 30 days
Priority: P3
Assignee: MA-1
```

---

## 5. Delegation Anti-Patterns

| Anti-Pattern | Why It's Wrong | Fix |
|-------------|---------------|-----|
| **Dump-and-run** | Giving a vague description and expecting the micro agent to figure it out | Be explicit about inputs, outputs, and constraints |
| **Micro-managing** | Giving step-by-step instructions for every detail defeats the purpose | Set the goal, not the path |
| **Over-delegating** | Sending everything to micro agents even when you could do it faster | Use judgment — is this actually saving time? |
| **Under-delegating** | Never using micro agents at all | Start with one task, see how it goes, scale up |
| **Wrong agent** | Sending a compression task to the Meeting Minutes agent | Check `docs/micro-agents.md` for scope |
| **No review** | Closing issues without checking the output | Always verify — micro agents can make mistakes |

---

## 6. Setting Up Recurring Delegations

For tasks that happen on a regular schedule (like daily vault health checks), use Paperclip's recurring issue feature:

1. Create the first issue manually
2. Mark it as a **recurring** template
3. Set the cadence: daily, weekly, etc.
4. The system auto-creates new instances on schedule

---

## 7. Delegation Chain of Command

```
                      CEO
                       │
         ┌─────────────┼──────────────┬─────────────────┐
         │             │              │                 │
        CTO           CDO         Task Supervisor    People Ops
         │             │              │                 │
    ┌────┴────┐        │              │                 │
    │         │        │              │                 │
 Eng Lead  Rsch Lead   │              ▼                 ▼
    │         │        │         MA-1 (Vault        MA-2 (Minutes)
    │         │        │         Health)             MA-4 (Distill)
    ▼         ▼        ▼
 MA-3     MA-7      MA-2
(Compress) (Zyeta)  (Minutes)
                     MA-4
                    (Distill)
                     MA-5
                    (Social Media — if CMO retained)
```

**Rule:** A main agent can delegate to any micro agent directly. Micro agents do not delegate to other micro agents — if a task spans multiple micro agents, the main agent sequences them.

---

## 8. Quick Reference — Agent ↔ Micro Agent Mapping

| Main Agent | Most Likely to Delegate To |
|------------|---------------------------|
| **CEO** | All (orchestration oversight) |
| **CTO** | MA-6 (Cloudflare), MA-7 (Zyeta), MA-4 (Distill) |
| **CDO** | MA-1 (Vault Health), MA-2 (Minutes), MA-4 (Distill), MA-5 (Social) |
| **Engineering Lead** | MA-3 (Compress), MA-6 (Cloudflare) |
| **Research Lead** | MA-4 (Distill), MA-7 (Zyeta) |
| **Content Lead** | MA-2 (Minutes), MA-4 (Distill) |
| **Task Supervisor** | MA-1 (Vault Health) |
| **CMO** (if active) | MA-5 (Social Media) |
| **People Ops** | MA-2 (Minutes), MA-4 (Distill) |

---

## 9. Getting Started

1. **Read** `docs/micro-agents.md` to understand the full micro agent catalog
2. **Pick one** task you do regularly that maps to a micro agent
3. **Create** your first delegation issue using the template above
4. **Review** the output and close the loop
5. **Repeat** — delegation is a habit that compounds over time

---

## References

- `docs/micro-agents.md` — Full micro agent catalog and definitions
- `docs/agents.md` — Complete agent inventory
- `docs/people-ops-dashboard.md` — Org health dashboard
- RDT-262 — This issue: micro agents and delegation
