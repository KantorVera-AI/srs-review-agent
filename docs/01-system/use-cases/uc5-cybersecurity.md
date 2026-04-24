**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM

---

# UC5 — Cybersecurity change impact

**Release tier:** Release 2
**Depends on:** UC1 (change classification), UC2 (baseline intake — threat model baseline)
**Required by:** Nothing downstream

---

## One-line description

When a SRS change introduces or modifies interfaces, data flows, authentication, or encryption requirements, verify coverage against IEC 81001-5-1 controls and OWASP ASVS, and route findings to the Cybersecurity Engineer.

---

## What triggers it

UC1 classifies a change as **security/data flows**. The cybersecurity sub-check then:
- Queries the OWASP ASVS structured checklist for the relevant security control categories
- Queries IEC 81001-5-1 clause summaries for the relevant lifecycle security activities
- Cross-checks against the threat model document to identify threats that are not yet mitigated in the SRS

For the cross-check against the threat model to produce high-quality findings, the threat model must be available in a structured, machine-readable format. If the threat model is a narrative document, the agent can still generate OWASP/IEC 81001-5-1 findings but cannot correlate them with specific threat identifiers.

---

## What the agent does

1. Receives the security/data flows classification from UC1
2. Identifies the specific SRS change — new interface, modified data flow, authentication change, encryption requirement, audit logging requirement
3. Checks the change against the OWASP ASVS control categories relevant to the identified change type
4. Checks the change against IEC 81001-5-1 clause summaries for the corresponding lifecycle activity
5. If the threat model is available in structured format: checks whether the new or modified element is covered by an existing threat model entry and whether that entry has a corresponding SRS mitigation requirement
6. Generates findings for gaps: missing security requirements, uncovered threat model entries, or OWASP controls not addressed
7. Checks whether the change may affect software item safety class (reclassification trigger, particularly relevant when a new external interface is added to a previously isolated item)

---

## Who receives the output

| Output | Recipient | Condition |
|---|---|---|
| Security finding | Cybersecurity Engineer | Always — primary recipient |
| RA/PRRC notification | RA / PRRC | Category III and IV products |
| Reclassification flag | RA/PRRC + Software Architect | New interface added to a previously isolated software item |

---

## RICE score

| Risk savings | Impact | Confidence | Effort | Score |
|---|---|---|---|---|
| 3 | 3 | 0.70 | 3 | 21 |

*Risk savings of 3: cybersecurity gaps are a growing source of regulatory deficiencies under both FDA cybersecurity guidance (updated 2026) and EU MDR Annex I GSPR 17, but the per-finding cost avoidance is lower than risk traceability gaps. Confidence of 0.70: lower than UC1/UC3 because finding quality depends on the structure and availability of the threat model, which varies significantly by organisation. Effort of 3: requires a cybersecurity sub-check module and the OWASP/IEC corpus.*

---

## Benefit breakdown

### Phase 1 — Initial development

| Dimension | Estimate |
|---|---|
| Typical events | 5–15 SRS changes touching interfaces or security requirements during development |
| Time saved per event | 2–5 hours of manual security requirement cross-check |
| Total time saving | 10–75 hours = 1,300–9,750€ |
| Regulatory cost avoided | 8–20k€ — cybersecurity gaps at first submission are a growing deficiency source |

### Phase 2 — Ongoing maintenance

| Dimension | Estimate |
|---|---|
| Annual events per product | 2–8 security-relevant SRS changes per year |
| Time saved per event | 3–8 hours |
| Annual time saving | 6–64 hours = 780–8,300€ |
| Regulatory cost avoided | 5–10k€ per year |

---

## Key assumptions

- OWASP ASVS is freely available and can be incorporated into the reference corpus without licensing restrictions.
- IEC 81001-5-1 reference corpus is built from clause summaries and publicly available mapping tables rather than the full normative text (paid standard). Finding citation depth will be somewhat lower than UC3 as a result.
- The threat model must be in a structured, machine-readable format for the highest-quality findings. If not, the additional parsing effort must be scoped with the AI Architect before Release 2.
- Security sub-checks trigger on every interface-related SRS change. If the classifier precision is insufficient, notification fatigue will reduce the Cybersecurity Engineer's responsiveness. A precision threshold must be agreed before deployment.

---

## Dependencies and risks

**Dependencies:** UC1 for change classification. OWASP ASVS and IEC 81001-5-1 clause summaries in the reference corpus (`data/reference/`). Threat model document in a structured format (preferred) or as an uploaded document (fallback).

**Technical risks:**
- Threat model format variability is the primary quality risk. Organisations use widely different formats — from structured tables to narrative prose. The agent's extraction capability must be validated against the specific format the team uses.
- False positives from security sub-checks are more disruptive than false positives in other use cases because the Cybersecurity Engineer typically works across multiple products. Noise will degrade adoption quickly.

**Process risks:**
- SBOM-aware SOUP vulnerability monitoring (flagging when a SOUP component update may require SRS changes) is a natural extension of UC5 but is out of scope for Release 2. It is noted as a backlog candidate.

---

## Regulatory basis

| Requirement | Standard | Clause |
|---|---|---|
| Cybersecurity activities in health software lifecycle | IEC 81001-5-1:2021 | Multiple — architecture, requirements, maintenance |
| Security requirements for networked devices | EU MDR Annex I | GSPR 17 |
| Cybersecurity in premarket submissions | FDA cybersecurity guidance | 2023/2026 |
| Application security verification | OWASP ASVS | v4.0 |
