---
title: SRS & Risk Review Agent
status: MVP v1.1 – Portfolio
owner: Product Management
---

# Tool Scope (First)
**Decision‑support only**. Generates **non‑binding findings** for human review. Does **not** create/approve SRS or replace formal sign‑offs. [file:44]

# 1. Purpose
GitHub‑integrated AI agent that reviews **SRS/risk files** on PRs, approvals, obsolescence. Posts citation‑backed findings as PR comments/checks.

# 2. Problem Statement
SRS/risk files change via Git PRs/branches/tags, but quality checks remain manual → gaps, audit risks.

# 3. MVP Scope
## In scope
- **Git triggers**: PR opened/updated, "approved"/"obsolete" labels/tags
- Analyze SRS/risk vs IEC 62304/MDR/ISO 14971/OWASP
- Post findings to PR comments/checks with SRS ID + citation
- Track accept/reject/defer per finding

## Out of scope
- SRS generation, risk acceptability, code analysis

# 4. Key Use Cases (Git‑specific)
**UC1**: PR modifies SRS → Agent comments findings  
**UC2**: Risk file PR → Agent flags hazard gaps  
**UC3**: "Approved" label → Pre‑approval summary  
**UC4**: "Obsolete" → Successor verification  

# 5. Stakeholders & Workflow
| Role | What they do with findings |
|------|---------------------------|
| Requirements Engineer | Disposition + update SRS |
| RA/QA | Standards/process gaps |
| Risk Manager | Hazard control verification |
| Cybersecurity | OWASP coverage |

# 6. Functional Requirements
FR1: GitHub Actions trigger on PR/label/tag  
FR2: Ingest SRS/risk with stable IDs  
FR3: RAG → citation‑backed findings  
FR4: Post to PR + log decisions  

# 7. Success Criteria
| Metric | Target |
|--------|--------|
| Citation validity | ≥90% |
| PR findings acceptance | ≥80% |
| Hallucination rate | <5% |

# 8. Principles
1. Non‑binding proposals only
2. Every finding cites clause/ID
3. Human approval gates
4. Audit trail (Git → finding → decision)

See [risk model](risk-model.md)
