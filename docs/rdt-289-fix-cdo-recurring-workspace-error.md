# RDT-289: Fix CDO Recurring Workspace Error (claude_local Adapter)

> **Owner:** Unassigned — needs Engineering Lead (e2cc964f) or CTO (11d48dee)
> **Priority:** P1 — high (blocks CDO reliability; 3rd recurrence)
> **Status:** Proposed
> **Dependencies:** None
> **Blocks:** Reliable CDO operation → all voice/brand gates

---

## Problem Statement

The CDO agent (`26402f1a`) has entered an error state **three times** due to the same root cause — a workspace expectation mismatch in the `claude_local` adapter.

### Error Message (from Paperclip API)

```
Issue RDT-42 expected a project workspace, but claude_local would launch from
agent fallback cwd "/Users/rick.d/.paperclip/instances/default/workspaces/26402f1a-b6a7-46e5-8db5-63bdef202bbb".
```

### Occurrence History

| # | Date | Duration | Recovery | Context |
|---|------|----------|----------|---------|
| 1 | ~RDT-113 era (2026) | Unknown | Manual fix | First occurrence, no root cause doc |
| 2 | 2026-05-22 | 53 days (until Jul 16) | Task Supervisor restored | Vault/config fix applied but didn't address workspace config |
| 3 | 2026-07-17T00:13Z | ~1.5 hours (cleared via API) | People Ops via Paperclip API | Agent re-errored after completing RDT-276 review |

### Impact of Each Recurrence

| Impact | Description |
|--------|-------------|
| Voice/brand gates blocked | RDT-277, RDT-265, and all future sweeps stalled |
| Content Lead orphaned | Reports to CDO, receives no direction during CDO downtime |
| Manual recovery overhead | Each occurrence requires API-level intervention (board access needed) |
| Trust erosion | Cannot rely on CDO for time-sensitive reviews |

---

## Root Cause Analysis

### Technical Root Cause

The `claude_local` adapter has two code paths for determining the working directory when launching an agent:

1. **Project workspace path** — Used when the task (issue) has an explicit `projectWorkspaceId` set. Adapter resolves the workspace path and launches the agent from there.
2. **Agent fallback path** — Used when `projectWorkspaceId` is not set or cannot be resolved. Adapter falls back to the agent's home directory under `.paperclip/instances/default/workspaces/{agentId}`.

**The bug:** When a task (like RDT-42) expects a project workspace but the adapter falls back to the agent directory, a mismatch exception is thrown. This happens after the agent completes its work — likely during a post-task cleanup or workspace validation hook.

### Why It's Recurring

- The error state is reset (error cleared, agent resumed) each time
- But the underlying workspace configuration is never changed
- The next task that triggers the workspace expectation path causes the same crash
- No permanent fix has been applied to either:
  - The claude_local adapter (Option B)
  - The CDO agent's default workspace assignment (Option A)
  - The task assignment logic (Option C)

### Trigger Pattern

The error occurs **after task completion**, suggesting:
1. Agent finishes its work successfully (e.g., RDT-276 review completed)
2. Agent enters post-task cleanup / workspace validation phase
3. Workspace mismatch is detected during this phase
4. Agent is put into error state

This means the agent **can complete work** before crashing, but it cannot accept new work afterward without manual recovery.

---

## Proposed Solutions

### Option A: Assign CDO a Default Project Workspace (Recommended)

**Effort:** Low | **Risk:** Low | **Permanence:** High

Assign the CDO agent a default project workspace so the `claude_local` adapter doesn't fall back to the agent home directory.

```bash
# PATCH /api/agents/26402f1a-b6a7-46e5-8db5-63bdef202bbb
# Set defaultProjectWorkspaceId to the project's workspace ID
```

**Pros:** Simple, addresses the root cause directly, no code changes needed
**Cons:** Requires Paperclip board-level API access

### Option B: Update claude_local Adapter

**Effort:** Medium-High | **Risk:** Medium | **Permanence:** High

Modify the `claude_local` adapter to:
- Gracefully handle missing project workspace (log warning instead of crashing)
- Or create the expected workspace structure on the fly
- Or skip workspace validation when a task doesn't strictly need one

**Pros:** Fixes for all agents, not just CDO
**Cons:** Requires adapter code access, risk of unintended side effects

### Option C: Ensure Tasks Explicitly Set projectWorkspaceId

**Effort:** Medium | **Risk:** Low | **Permanence:** Medium (process-only fix)

Add a check to task creation/assignment that ensures `projectWorkspaceId` is set or that the agent can run without one.

**Pros:** No code changes needed
**Cons:** Process-only fix, easy to regress, doesn't address post-task crash

### Option D: Add Post-Task Error Recovery Hook

**Effort:** Medium | **Risk:** Low | **Permanence:** Low (mitigation, not fix)

Create a monitoring agent (e.g., MA-1 Vault Health Agent) that detects when CDO enters error state and automatically clears the error and resumes.

**Pros:** Reduces recovery time from hours to minutes
**Cons:** Doesn't fix root cause, band-aid on recurring issue

---

## Recommended Action Plan

### Phase 1: Immediate Mitigation (P0)

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Assign CDO a default project workspace (Option A) | Board/CTO | 🔴 Proposed |
| 2 | Verify CDO doesn't re-error after workspace assignment | CTO/Engineering Lead | 🔴 Pending |
| 3 | Test with a no-op task before next real review | CDO | 🔴 Pending |

### Phase 2: Engineering Fix (P1)

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 4 | Audit claude_local adapter workspace resolution code | Engineering Lead | 🔴 Proposed |
| 5 | Implement graceful fallback instead of crash (Option B) | Engineering Lead | 🔴 Proposed |
| 6 | Add workspace validation error handling test | Engineering Lead | 🔴 Proposed |

### Phase 3: Monitoring & Prevention (P2)

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 7 | Approve and deploy MA-1 Vault Health Agent | CEO/CTO | 🔴 Pending (see RDT-262) |
| 8 | Add CDO error state to monitoring dashboard | People Ops | 🔴 Proposed |
| 9 | Schedule quarterly agent health review | CEO | 🔴 Pending (from RDT-239) |

---

## Acceptance Criteria

- [ ] CDO agent does not enter error state from workspace mismatch for 30 days after fix
- [ ] claude_local adapter handles missing project workspace gracefully (logs warning instead of crashing)
- [ ] Recovery runbook updated with permanent fix steps
- [ ] Monitoring alert configured for CDO error state
- [ ] Post-task error recovery hook operational (auto-resume)

---

## Related Issues

- **RDT-288** — CDO Restoration (this issue resolves the immediate error; RDT-289 fixes root cause)
- **RDT-277** — CDO Review: Content as Income Engine (#2) (blocked until CDO reliable)
- **RDT-265** — CDO voice gate: rdtect.com O2 copy (blocked until CDO reliable)
- **RDT-262** — Micro Agents & Delegation (MA-1 Vault Health Agent would help detect recurrence)
- **RDT-239** — Quality Review (quarterly health review recommendation)

---

## Escalation

If this issue is not addressed before CDO's next real review (est. RDT-277), the CDO will likely re-error, requiring another manual recovery cycle. This creates a **reliability risk** for all voice/brand gates.

**Recommended deadline:** Before RDT-277 review assignment (currently `in_review` status)
