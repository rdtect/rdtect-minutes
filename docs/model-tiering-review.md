# Model Tiering Review — RDT Organization

> **Owner:** People Ops (4f2b0b88)  
> **Issue:** RDT-262  
> **Date:** 2026-07-16  
> **Status:** ✅ Active  
> **Parent:** RDT-239 (recommendation MT-1)

---

## 1. Current Model Distribution

| Model | Agents | Count | Monthly Cost Tier |
|-------|--------|-------|-------------------|
| **claude-sonnet-4-6** | CEO, CTO, CDO, Engineering Lead, Research Lead, Content Lead | **6** | 💰💰💰 High |
| **deepseek/deepseek-v4-pro** | Hermes Specialist | **1** | 💰💰 Mid |
| **deepseek-v4-flash** | CMO, Task Supervisor, People Ops | **3** | 💰 Low |

### Current Spend Profile

```
Cost per agent:    claude-sonnet-4-6 > deepseek-v4-pro > deepseek-v4-flash
                    $$$$$             $$$                  $

6 × claude-sonnet-4-6  → ████████████████████████████  ~70% of total cost
1 × deepseek-v4-pro    → ██████                        ~15% of total cost
3 × deepseek-v4-flash  → ██████                        ~15% of total cost
```

**Key insight:** 6 out of 10 agents are on the most expensive model (claude-sonnet-4-6), which likely accounts for ~70% of total inference cost.

---

## 2. Agent-by-Agent Model Assessment

### Justified on claude-sonnet-4-6

| Agent | Justification | Recommended? |
|-------|---------------|-------------|
| **CEO** | Orchestration decisions, approvals, strategic judgment. Needs best reasoning. | ✅ Keep on claude-sonnet-4-6 |
| **CTO** | Architecture decisions, ADRs, technical evaluations. Needs high reasoning quality. | ✅ Keep on claude-sonnet-4-6 |
| **CDO** | Brand voice, content quality gates. Needs nuanced judgment. | ✅ Keep on claude-sonnet-4-6 |

### Candidates for Downgrade

| Agent | Current Model | Proposed Model | Rationale | Savings |
|-------|--------------|----------------|-----------|---------|
| **Engineering Lead** | claude-sonnet-4-6 | deepseek-v4-pro | Mostly execution: deployments, code changes, TDD. Lower reasoning needs than CTO. | 💰💰 → 💰 |
| **Research Lead** | claude-sonnet-4-6 | deepseek-v4-pro | Research and analysis — good candidate for mid-tier. Flash may be sufficient for most tasks. | 💰💰💰 → 💰💰 |
| **Content Lead** | claude-sonnet-4-6 | deepseek-v4-pro | Content drafting can use a capable mid-tier model. Flash may suffice for templates. | 💰💰💰 → 💰💰 |

### Keep as-is

| Agent | Current Model | Assessment |
|-------|--------------|------------|
| **CMO** | deepseek-v4-flash | Zero output — model irrelevant until fate decided |
| **Task Supervisor** | deepseek-v4-flash | Appropriate — monitoring/triage tasks don't need top-tier reasoning |
| **Hermes Specialist** | deepseek/deepseek-v4-pro | Appropriate — execution and infra |
| **People Ops** | deepseek-v4-flash | Appropriate — HR, retros, health checks |

---

## 3. Optimization Scenarios

### Scenario A: Conservative (downgrade 1 agent)

| Change | Engineering Lead → deepseek-v4-pro |
|--------|------------------------------------|
| Agents on claude-sonnet | 6 → 5 |
| Estimated savings | ~8-10% of total cost |

### Scenario B: Balanced (downgrade 2 agents)

| Change | Engineering Lead → deepseek-v4-pro, Research Lead → deepseek-v4-pro |
|--------|----------------------------------------------------------------------|
| Agents on claude-sonnet | 6 → 4 |
| Estimated savings | ~15-20% of total cost |

### Scenario C: Aggressive (downgrade 3 agents)

| Change | Engineering Lead → deepseek-v4-pro, Research Lead → deepseek-v4-pro, Content Lead → deepseek-v4-flash |
|--------|------------------------------------------------------------------------------------------------------|
| Agents on claude-sonnet | 6 → 3 |
| Estimated savings | ~30-35% of total cost |

---

## 4. Model Tier Recommendations for New Agents

### Micro Agent Model Tier

For the 7 proposed micro agents (RDT-262), the model tier should be:

| Tier | Model | Recommended For | Rationale |
|------|-------|-----------------|-----------|
| **Standard** | deepseek-v4-flash | MA-1 (Vault), MA-3 (Compress), MA-5 (Social) | Simple, deterministic tasks. No reasoning needed. |
| **Mid** | deepseek-v4-pro | MA-2 (Minutes), MA-4 (Distill) | Formatting/summarization benefits from mid-tier model |
| **Standard** | deepseek-v4-flash | MA-6 (Cloudflare), MA-7 (Zyeta) | Execution/lookup tasks. Flash is sufficient. |

**Rule of thumb for micro agents:**
- If the task is **deterministic** (compress, deploy, lookup) → deepseek-v4-flash
- If the task involves **formatting or summarization** (minutes, distill) → deepseek-v4-pro
- If the task requires **judgment or creativity** → claude-sonnet-4-6 (but this shouldn't be delegated to a micro agent)

---

## 5. Cost Impact Summary

| Scenario | claude-sonnet | deepseek-v4-pro | deepseek-v4-flash | Est. Cost Change |
|----------|--------------|-----------------|-------------------|-----------------|
| **Current** | 6 | 1 | 3 | Baseline |
| **Conservative** | 5 | 2 | 3 | -8-10% |
| **Balanced** | 4 | 3 | 3 | -15-20% |
| **Aggressive** | 3 | 3 | 4 | -30-35% |
| **After micro agents** | 3 | 5 | 9 | Micro agents add 7 on cheap tier |

---

## 6. Recommendation

### For Full Agents

1. **Immediately:** Move Engineering Lead to deepseek-v4-pro. Engineering tasks (deployments, code changes, TDD) don't need top-tier reasoning.
2. **Evaluate:** Move Research Lead to deepseek-v4-pro after 2 weeks — compare output quality.
3. **Consider:** If Content Lead's output quality holds on deepseek-v4-pro, migrate them too.
4. **Keep:** CEO, CTO, and CDO on claude-sonnet-4-6 — their roles require the highest reasoning quality.

### For Micro Agents

5. **Default to deepseek-v4-flash** for all micro agents.
6. **Upgrade to deepseek-v4-pro** only for MA-2 (Meeting Minutes) and MA-4 (Distillation) if output quality requires it.

### Decision Needed

| # | Decision | Options | Owner |
|---|----------|---------|-------|
| MT-1 | Downgrade Engineering Lead? | Yes → deepseek-v4-pro / No → keep claude-sonnet | CTO |
| MT-2 | Downgrade Research Lead? | Yes → deepseek-v4-pro / Evaluate first / No | CTO |
| MT-3 | Downgrade Content Lead? | Yes → deepseek-v4-flash / Yes → deepseek-v4-pro / No | CDO |
| MT-4 | Micro agent default model? | All deepseek-v4-flash / Mix (v4-flash + v4-pro) | CTO |

---

## References

- `docs/agents.md` — Full agent inventory with current models
- `docs/agent-quality-review.md` — Quality review (RDT-239)
- `docs/micro-agents.md` — Micro agent proposals (model recommendations)
- `docs/agent-monitoring-report.md` — Agent monitoring snapshot
