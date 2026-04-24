**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM

---

# UC1 — SRS monitoring and change classification

**Release tier:** Initial release
**Depends on:** Nothing — this is the foundation use case
**Required by:** UC2, UC3, UC4, UC5, UC6, UC7

---

## One-line description

Detect every SRS change event, classify the change type, and route findings to the appropriate document owner.

---

## What triggers it

A change event on any SRS document — a new version submitted for review, a modification to a previously approved requirement, or a status transition (draft → review → approved → obsolete). The agent monitors the document management platform for these events and initiates analysis automatically.

For teams without an automated integration, the trigger can be submitted manually through the UI (see `docs/03-integration/ui-scope.md`, Job 1).

> **Illustrative example (not prescriptive):** In a version-controlled workflow, the trigger might be a new review request on an SRS file. In a document management system, the trigger might be a workflow state change. The specific mechanism depends on the team's tooling and integration tier.

---

## What the agent does

1. Parses the changed SRS document and identifies which requirements were added, modified, or removed
2. Classifies each change into one or more change types:
   - **Clinical** — changes to clinical function, intended population, or performance claims
   - **Risk/safety** — changes to requirements that implement risk controls or affect hazardous situations
   - **UI/workflow** — changes to user interface behaviour, user roles, or interaction sequences
   - **Security/data flows** — changes to interfaces, authentication, encryption, or data transmission
   - **AI/ML behaviour** — changes to algorithm logic, model inputs/outputs, or performance specifications
   - **Non-functional** — changes to performance, availability, logging, or audit trail requirements
3. Checks whether the change may trigger a device-level IMDRF category reclassification or a software item safety class reclassification (see `docs/01-system/output-calibration.md`)
4. Generates findings calibrated to the IMDRF category and software item safety class of the affected requirements
5. Routes findings to the document owners responsible for the affected controlled documents

---

## Who receives the output

| Output | Recipient | Condition |
|---|---|---|
| Classified change summary | Requirements Engineer (SRS owner) | Every change event |
| Risk/safety finding | Risk / Safety Engineer | Change classified as risk/safety or clinical |
| UI/workflow finding | Usability / HF Specialist | Change classified as UI/workflow |
| Security finding | Cybersecurity Engineer | Change classified as security/data flows |
| AI/ML finding | AI Engineer + RA/PRRC | Change classified as AI/ML behaviour |
| Reclassification flag | RA/PRRC + Software Architect | Reclassification trigger detected |
| Non-functional finding | QA / Validation Engineer | Change classified as non-functional |

---

## RICE score

| Risk savings | Impact | Confidence | Effort | Score |
|---|---|---|---|---|
| 4 | 4 | 0.9 | 2 | 72 |

*Risk savings of 4: reduces the probability of reviewer deficiency from missed change classification. Confidence of 0.9: the change detection approach is well-defined and test data exists. Effort of 2: the lowest build effort of any use case — reuses document ingestion infrastructure already scoped in the PRD.*

---

## Benefit breakdown

### Phase 1 — Initial development

| Dimension | Estimate |
|---|---|
| Typical events | 30–80 SRS creation/update events during initial development |
| Time saved per event | 0.5–2 hours of manual classification and routing |
| Total time saving | 15–160 hours = 2,000–20,800€ |
| Regulatory cost avoided | 5–15k€ — systematic classification reduces gaps reaching first submission |

### Phase 2 — Ongoing maintenance

| Dimension | Estimate |
|---|---|
| Annual events per product | 20–40 SRS change events per year |
| Time saved per event | 1–3 hours of manual change triage |
| Annual time saving | 20–120 hours = 2,600–15,600€ |
| Regulatory cost avoided | 5–10k€ per year — reduced deficiency probability |

---

## Key assumptions

- 20–40 annual events is calibrated against an actively developed SaMD product with multiple integrations and algorithm features. A less active product may see 8–15 events per year.
- Change classifier achieves 85%+ precision on change type detection. If precision falls below this threshold, false-positive routing will reduce adoption.
- Phase 1 event count assumes a new product built from scratch. For a product migrated to the agent mid-development, events will be lower.
- All benefit estimates assume the agent is the primary change classification mechanism. If a team already has a formal change impact assessment process, the incremental benefit is lower.

---

## Dependencies and risks

**Dependencies:** None — UC1 is the foundation. All other use cases depend on it.

**Technical risks:**
- False-positive classification is the primary adoption risk. Flagging non-safety-relevant changes for risk manager review creates noise. A precision threshold must be agreed before deployment and monitored post-deployment.
- Missing IMDRF category or software item safety class metadata degrades output calibration. The agent flags missing metadata but cannot self-correct it.

**Process risks:**
- If the document owner directory (routing configuration) is not kept current, findings will be delivered to the wrong person or not delivered at all.

---

## Validation criteria

Before marking UC1 complete in the initial release:

- [ ] Change classifier achieves ≥85% precision on the synthetic SRS v1→v2 delta test corpus
- [ ] All six change types are correctly classified on at least two test cases each
- [ ] Reclassification trigger detection fires correctly on the isolation-removal test scenario in `data/raw/`
- [ ] Findings are routed to the correct owner role in all test scenarios
- [ ] IMDRF Category I and Category IV produce visibly different output depth for the same change type
- [ ] Missing metadata fallback behaviour matches specification in `output-calibration