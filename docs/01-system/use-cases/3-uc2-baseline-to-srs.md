**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM

---

# UC2 — Baseline document to SRS suggestions

**Release tier:** Release 2
**Depends on:** UC1 (ingestion infrastructure)
**Required by:** UC7 (usability engineering baseline intake uses the same mechanism)

---

## One-line description

When a regulatory document is baselined or approved, automatically generate suggested SRS requirements that should exist to support the document's scope.

---

## What triggers it

A document owner marks a document as approved or baselined in the document management platform. The agent detects this state transition and initiates baseline intake analysis.

Applicable document types that trigger UC2:
- Risk management plan or preliminary hazard analysis (generates risk control SRS suggestions)
- Usability engineering plan (generates UI and use error mitigation SRS suggestions)
- Clinical evaluation plan (generates clinical performance SRS suggestions)
- Cybersecurity risk assessment (generates security requirement SRS suggestions)
- Software architecture document — when a new software item with a safety class is added (generates item-level requirement suggestions)

For teams without an automated integration, the baseline can be submitted manually through the UI baseline submission screen.

---

## What the agent does

1. Receives the baseline approval event and ingests the approved document
2. Extracts structured elements — risk controls, use error mitigations, clinical performance thresholds, security controls — using the document type to guide extraction
3. Maps each extracted element against the current SRS to identify what is missing or not yet addressed
4. Generates a suggestion set for the SRS owner: proposed requirement additions or updates, each citing the source document element and the standard clause that requires it
5. Delivers the suggestion set to the SRS owner for review — suggestions are non-binding and require explicit acceptance before any SRS change is made

The output is a suggestion, not a finding. Suggestions are lower-friction than findings — they do not require a full disposition with rationale. The SRS owner reviews each suggestion and either accepts it (creating a tracked action to add or update the requirement) or dismisses it.

---

## Who receives the output

| Output | Recipient | Condition |
|---|---|---|
| Suggestion set | Requirements Engineer (SRS owner) | Every baseline event |
| Notification | Document owner who submitted the baseline | When suggestions are generated and when they are actioned |

---

## RICE score

| Risk savings | Impact | Confidence | Effort | Score |
|---|---|---|---|---|
| 3 | 4 | 0.75 | 3 | 30 |

*Risk savings of 3: prevents requirement gaps that arise when baseline documents are not systematically translated into SRS requirements — most impactful at Phase 1. Impact of 4: the time saving per event is significant, especially during initial development. Confidence of 0.75: lower than UC1/UC3 because suggestion quality depends heavily on the structure of the incoming baseline document. Effort of 3: requires a baseline intake parser that handles multiple document types.*

---

## Benefit breakdown

### Phase 1 — Initial development

| Dimension | Estimate |
|---|---|
| Typical events | 3–6 initial baselines during product development |
| Time saved per event | 8–20 hours of initial SRS mapping against each baseline |
| Total time saving | 24–120 hours = 3,100–15,600€ |
| Regulatory cost avoided | 10–25k€ — requirement gaps prevented before first submission |

### Phase 2 — Ongoing maintenance

| Dimension | Estimate |
|---|---|
| Annual events per product | 1–3 document baselines updated per year |
| Time saved per event | 2–8 hours (incremental update) |
| Annual time saving | 2–24 hours = 260–3,100€ |
| Regulatory cost avoided | 5–15k€ per year |

> **Phase 1 note:** The primary value of UC2 is at Phase 1 — when all regulatory documents are being baselined for the first time and the SRS is being built in parallel. For a mature product in Phase 2, the per-event benefit is lower because fewer new baselines are created.

---

## Key assumptions

- Quality of suggestions depends on the structure of the incoming baseline document. Structured documents with explicit control identifiers (e.g. RC-001, USE-ERR-003) generate precise, traceable suggestions. Narrative-style documents generate less specific suggestions requiring more human interpretation. Teams with unstructured baseline documents will see lower UC2 value.
- The suggestion acceptance rate target is lower than the finding acceptance rate — suggestions are less urgent than findings and may be deferred more frequently. This is expected behaviour.
- Over-suggestion is the primary adoption risk. If the agent generates too many low-confidence suggestions, SRS owners will begin to ignore the output. Suggestion confidence thresholds must be tuned during Release 2 validation.

---

## Dependencies and risks

**Dependencies:** UC1 ingestion infrastructure. Baseline document in a parseable format. Notification routing to the SRS owner.

**Technical risks:**
- Narrative-style baseline documents (common for clinical evaluations and some risk management plans) require more sophisticated extraction logic than structured documents. Suggestion quality for these document types may be lower in Release 2 and improve over time.
- Over-suggestion reduces adoption. A configurable confidence threshold per document type should be implemented to control suggestion volume.

**Process risks:**
- Teams must establish a process for reviewing and actioning suggestions within a defined timeframe. Suggestions that accumulate without review create a backlog that undermines the value of UC2.

---

## Regulatory basis

| Requirement | Standard | Clause |
|---|---|---|
| Risk control implementation in SRS | IEC 62304:2006 | Section 5.2.3 |
| Software requirements derived from system requirements | IEC 62304:2006 | Section 5.2.1 |
| Design input adequacy review | FDA 21 CFR 820.30(e) | Design inputs |
| Technical documentation completeness | EU MDR Annex II | Section 6.1 |
