# Stakeholder Workflows

**Status:** Deprecated  
**Owner:** Product Management  
**Audience:** All stakeholders



## Handling Agent Findings (All)
1. Review proposed finding + citation
2. **Disposition**: Accept / Reject / Defer / Clarify / Route / Escalate / Out of scope
3. **Rationale** (1 sentence, logged)
4. Update SRS/risk if accepted

## By role
| Role | Focus | Example action |
|------|-------|----------------|
| Requirements Engineer | Clarity, testability | "Accept SRS-011, reject ambiguous phrasing" |
| RA/Compliance | Standards | "Defer IEC62304-4.3 until next sprint" |
| Risk Manager | Hazard controls | "Reject—SRS-045 still covers RC-001" |
| QA/Validation | Verifiability | "Accept test case requirement" |
| Cybersecurity | OWASP | "Accept A01 auth requirement" |
| PRRC (EU MDR) | Regulatory compliance | "Escalate — this change may require a new submission" |
| Usability / HF Specialist | Use errors and usability obligations | "Accept — formative study finding requires SRS update" |

**Logged**: Change record reference + finding ID + disposition + rationale.
