# Stakeholder Workflows

## Handling Agent Findings (All)
1. Review proposed finding + citation
2. **Disposition**: Accept / Reject / Defer
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

**Logged**: Git commit/PR + finding ID + disposition + rationale.
