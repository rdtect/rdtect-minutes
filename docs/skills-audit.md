# Skills Audit — RDT Organization

> **Author:** People Ops (4f2b0b88)  
> **Date:** 2026-07-16  
> **Issue:** RDT-239  
> **Status:** ✅ Complete  
> **Parent:** RDT-237 (Company Reset)  
> **Scope:** Full audit of company skills catalog — installed vs used vs missing vs stale.

---

## 1. Skills Catalog — Paperclip API (17 Skills)

| # | Skill | Source Type | Trust Level | Agents Attached | Last Updated | Status |
|---|-------|-------------|-------------|-----------------|-------------|--------|
| 1 | **compress** | local_path | assets | 0 | May 14 | 🟡 Unused |
| 2 | **distill** | local_path | markdown_only | 0 | May 14 | 🟡 Unused |
| 3 | **docx** | local_path | scripts_executables | 3 | Jul 16 | ✅ Used |
| 4 | **dream** | local_path | markdown_only | 0 | May 14 | 🟡 Unused |
| 5 | **ingest** | local_path | markdown_only | 0 | May 14 | 🟡 Unused |
| 6 | **maintain** | local_path | markdown_only | 0 | May 14 | 🟡 Unused |
| 7 | **paperclip** | local_path | scripts_executables | 0 | Jul 16 | ✅ Used (implicitly by all agents) |
| 8 | **paperclip-board** | local_path | markdown_only | 0 | Jul 16 | 🟡 New (Jul 16) |
| 9 | **paperclip-converting-plans-to-tasks** | local_path | markdown_only | 0 | Jul 16 | 🟡 New (Jul 16) |
| 10 | **paperclip-create-agent** | local_path | markdown_only | 0 | Jul 16 | ✅ Used |
| 11 | **para-memory-files** | local_path | markdown_only | 0 | Apr 27 | ✅ Used (CEO references it) |
| 12 | **pdf** | local_path | scripts_executables | 3 | Jul 16 | ✅ Used |
| 13 | **pptx** | local_path | scripts_executables | 3 | Jul 16 | ✅ Used |
| 14 | **story** | local_path | markdown_only | 0 | May 14 | 🟡 Unused |
| 15 | **vault-audit** | local_path | assets | 0 | May 14 | 🟡 Unused |
| 16 | **vault-health** | local_path | markdown_only | 0 | May 14 | 🟡 Unused |
| 17 | **xlsx** | local_path | scripts_executables | 3 | Jul 16 | ✅ Used |

### Key Finding: Skill Attachment Gap

**Only 3 skills have agents attached** (docx, pdf, pptx — all with 3 agents each). The remaining **14 skills have zero agents attached** in the Paperclip system. However, several are still implicitly used:

- **paperclip** — Core Paperclip interaction skill, implicitly available to all agents
- **paperclip-create-agent** — Used for hiring workflow
- **para-memory-files** — CEO's instructions explicitly reference this for memory operations
- **paperclip-board**, **paperclip-converting-plans-to-tasks** — Newly created (Jul 16), too early to assess

---

## 2. Hermes Shared Skills Layer (27 Skills)

Beyond the Paperclip catalog, agents have access to a **Hermes shared skills layer** loaded from the `strategist` profile (27 skills):

| Skill Category | Skills |
|----------------|--------|
| **Agent/Automation** | `autonomous-ai-agents`, `dogfood`, `find-skills` |
| **Development** | `software-development`, `data-science`, `mlops`, `devops`, `inference-sh` |
| **Creative** | `creative`, `diagramming`, `gaming`, `gifs`, `media`, `social-media` |
| **Knowledge** | `research`, `note-taking`, `vault`, `domain`, `productivity` |
| **Communication** | `email`, `apple`, `mcp`, `red-teaming` |
| **Infrastructure** | `agent-browser`, `smart-home`, `yuanbao`, `github` |

**Note:** These Hermes skills are loaded per-agent via their adapter profile. The Paperclip API catalog represents skills that have been explicitly registered in the Paperclip system, which is a separate layer.

---

## 3. Individual (Role-Specific) Skills

From `shared-skills.md`, each role has individual skills:

| Role | Individual Skills | Source |
|------|------------------|--------|
| CEO | strategy, delegation, coordination | shared-skills.md |
| CTO | architecture, system-design, revenue-pitches | shared-skills.md |
| CDO | brand-voice, design-quality, content-gates | shared-skills.md |
| Engineering Lead | test-driven-development, codebase-inspection, github-pr-workflow | shared-skills.md |
| Content Lead | content-drafting, case-studies, insights | shared-skills.md |
| CMO | marketing, growth, distribution | shared-skills.md |
| Research Lead | research, discovery, analysis | shared-skills.md |
| Hermes Specialist | execution, infra, computer-use | shared-skills.md |
| People Ops | HR, retros, health | shared-skills.md |

**Only CEO's instructions explicitly reference `para-memory-files` and `paperclip-create-agent`.** Other agents reference shared-skills.md but do not pin specific skills.

---

## 4. Skills Usage Assessment

### Actively Used Skills (installed + used)
| Skill | Agents | Evidence |
|-------|--------|----------|
| paperclip | All agents | Core API interaction — referenced in CEO instructions |
| paperclip-create-agent | CEO, CTO | Used for hire requests |
| para-memory-files | CEO | Explicitly referenced in CEO instructions |
| docx | 3 agents | Attached agents using this for .docx work |
| pdf | 3 agents | Attached agents using this for PDF work |
| pptx | 3 agents | Attached agents using this for .pptx work |
| xlsx | 3 agents | Attached agents using this for spreadsheet work |

### Installed But Unused (no agents attached, no evidence of use)
| Skill | Created | Days Unused |
|-------|---------|-------------|
| compress | May 14 | 63 days |
| distill | May 14 | 63 days |
| dream | May 14 | 63 days |
| ingest | May 14 | 63 days |
| maintain | May 14 | 63 days |
| story | May 14 | 63 days |
| vault-audit | May 14 | 63 days |
| vault-health | May 14 | 63 days |

### New / Too Early to Assess
| Skill | Created | Note |
|-------|---------|------|
| paperclip-board | Jul 16 | Created same day as audit |
| paperclip-converting-plans-to-tasks | Jul 16 | Created same day as audit |

---

## 5. Missing Skills

Based on the project's needs (rdtect-os, RapidAI, Zyeta DX, content operations), the following skills would fill gaps:

| Missing Skill | Why Needed | Priority | Gap Reference |
|---------------|-----------|----------|---------------|
| **meeting-minutes** | No agent has a structured meeting capture skill. CDO/Content Lead would benefit. | P2 | RDT-239 S4 |
| **z-build / zyeta-domain** | Domain knowledge for Zyeta Construction / Zyeta DX projects. No agent has this context built in. | P1 | RDT-239 S2 |
| **cloudflare-deployment** | Engineering Lead is deploying to Cloudflare but skill is ad-hoc. | P2 | New |
| **social-media-publishing** | CMO (if kept) needs a distribution skill. Currently none exists. | P2 | RDT-239 S1 |
| **quality-review-cadence** | No recurring quality review skill. This audit is one-off. | P3 | RDT-239 S6 |

---

## 6. Stale / Candidate for Removal

| Skill | Reason | Recommendation |
|-------|--------|----------------|
| **dream** | 63 days unused. Consolidate-session-learning concept may be superseded by para-memory-files. | Consider archiving |
| **maintain** | 63 days unused. Vault maintenance not happening via this skill. vault-health covers some of this. | Consider archiving |
| **story** | 63 days unused. Life story capture not relevant to current projects. | Archive unless vault work resumes |
| **ingest** | 63 days unused. PARA inbox processing not active. | Archive unless vault work resumes |

---

## 7. Agent-Skill Matrix

| Agent | Paperclip Skills | Hermes Shared Skills | Individual Skills | Gaps |
|-------|-----------------|---------------------|-------------------|------|
| **CEO** | paperclip, para-memory-files | 27 shared skills | strategy, delegation, coordination | None critical |
| **CTO** | paperclip (implicit) | 27 shared skills | architecture, system-design, revenue-pitches | None critical |
| **CDO** | paperclip (implicit) | 27 shared skills | brand-voice, design-quality, content-gates | meeting-minutes |
| **Engineering Lead** | paperclip (implicit), docx, pdf, pptx, xlsx | 27 shared skills | tdd, codebase-inspection, github-pr-workflow | cloudflare-deployment |
| **Research Lead** | paperclip (implicit) | 27 shared skills | research, discovery, analysis | zyeta-domain knowledge |
| **Content Lead** | paperclip (implicit), docx, pdf, pptx, xlsx | 27 shared skills | content-drafting, case-studies, insights | meeting-minutes |
| **CMO** | paperclip (implicit) | 27 shared skills | marketing, growth, distribution | social-media-publishing (if kept) |
| **Task Supervisor** | paperclip (implicit) | 27 shared skills | (none listed explicitly) | quality-review-cadence |
| **Hermes Specialist** | paperclip (implicit) | 27 shared skills | execution, infra, computer-use | None critical |
| **People Ops** | paperclip (implicit) | 27 shared skills | HR, retros, health | None critical |

---

## 8. Summary & Recommendations

### Skills Health Dashboard

| Category | Count |
|----------|-------|
| Total skills in Paperclip catalog | 17 |
| Skills with attached agents | 3 (docx, pdf, pptx — each 3 agents) |
| Skills with 0 attached agents | 14 |
| Skills actively used (by evidence) | 7 |
| Skills unused for 60+ days | 8 |
| New skills (today) | 2 |
| Hermes shared skills (all agents) | 27 |
| Missing skills identified | 5 |

### Recommended Actions

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| S1 | **Attach paperclip skill to all agents** in Paperclip config for proper tracking | CTO/CEO | P1 |
| S2 | **Create meeting-minutes skill** for CDO/Content Lead | CDO | P2 |
| S3 | **Add zyeta-domain / z-build domain skill** for Research Lead & Engineering Lead | CTO | P1 |
| S4 | **Archive stale skills** (dream, story, maintain, ingest) after confirming no active need | CDO | P2 |
| S5 | **Attach vault-health + vault-audit** to Task Supervisor or CDO if vault work resumes | CDO | P2 |
| S6 | **Consider creating cloudflare-deployment skill** for Engineering Lead | CTO | P2 |
| S7 | **Audit agent models** — 5 agents on claude-sonnet-4-6, 3 on deepseek-v4-flash, 1 on deepseek-v4-pro. Ensure tiering is intentional. | CTO | P2 |

---

## References

- RDT-99 Self-Organization Review → `docs/self-org-review.md`
- RDT-239 Agent Inventory → `docs/agents.md`
- RDT-239 Quality Review → `docs/agent-quality-review.md`
- RDT-239 People Ops Dashboard → `docs/people-ops-dashboard.md`
- Paperclip API: `/api/companies/.../skills` (17 skills)
- Hermes shared context: `shared-skills.md` (27 Hermes skills + individual skills)
