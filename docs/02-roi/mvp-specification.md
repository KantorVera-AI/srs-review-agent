**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM, advisors

---

# MVP Specification

Full detail for the initial release — UC1 and UC3. Covers the build scope, the metadata prerequisite, the Phase 1 and Phase 2 ROI, and the validation criteria the AI Architect must satisfy before the initial release is considered complete.

For the scoring rationale and parameter definitions, see `assumptions.md`. For the full release plan, see `roadmap.md`.

---

## Initial release scope

The initial release delivers two use cases:

- **UC1 — SRS monitoring and change classification** — detects every SRS change event, classifies the change type, calibrates output by IMDRF category and software item safety class, and routes findings to the appropriate document owner
- **UC3 — Risk traceability check** — for every safety-relevant SRS change, verifies that every risk control in the risk management file has a corresponding SRS requirement and flags gaps or broken links

These two use cases together deliver the complete monitoring → classification → traceability → finding workflow. They validate the core hypothesis: that automated, citation-backed SRS review produces findings that regulatory teams find useful and act on.

Everything else in the roadmap depends on this hypothesis being confirmed.

---

## Metadata prerequisite

The agent cannot produce classification-calibrated outputs without two metadata fields being present as structured data.

**Field 1 — IMDRF significance category (product level)**

What it is: the IMDRF category (I, II, III, or IV) of the device being reviewed. Determines overall output depth, routing, and escalation thresholds.

Where it lives: in the product registry, entered by the RA/PRRC role through the UI or synced from the intended use document in the DMS.

Format: integer 1–4.

What happens without it: the agent applies Category III defaults throughout and generates a High severity finding flagging the missing field to the RA/PRRC role.

**Field 2 — IEC 62304 software item safety class (item level)**

What it is: the safety class (A, B, or C) of each software item referenced in the SRS. Determines citation depth, evidence requirements, and reclassification trigger sensitivity for each individual finding.

Where it lives: in the software item registry, entered by the Software Architect through the UI or synced from the SAD via the requirements management system integration.

Format: string A, B, or C, attached to each software item identifier (SI-NNN).

What happens without it: the agent applies Class C defaults for all requirements on that product and generates a High severity finding flagging the missing field to the Software Architect.

Teams should resolve both metadata fields before using the agent's findings for any formal regulatory purpose. See `docs/03-integration/metadata-spec.md` for the full tagging specification.

---

## Phase 1 ROI — initial development and first submission

Phase 1 covers the period from project start through first regulatory submission approval.

### UC1 Phase 1

| Dimension | Estimate |
|---|---|
| Typical SRS change events | 30–80 during initial development |
| Time saved per event | 0.5–2 hours of manual classification and routing |
| Total time saving | 15–160 hours |
| At 130€/hour loaded cost | 2,000–20,800€ |
| Regulatory cost avoided | 5–15k€ |
| **Total Phase 1 value (UC1)** | **7,000–35,800€** |

### UC3 Phase 1

| Dimension | Estimate |
|---|---|
| Typical safety-relevant events | 15–30% of all SRS events = 5–24 events |
| Time saved per event | 2–6 hours of manual risk file cross-check |
| Total time saving | 10–144 hours |
| At 130€/hour loaded cost | 1,300–18,720€ |
| Regulatory cost avoided | 15–40k€ |
| **Total Phase 1 value (UC3)** | **16,300–58,720€** |

### Combined Phase 1 value

| Scenario | UC1 | UC3 | Combined |
|---|---|---|---|
| Conservative (lower bounds) | 7,000€ | 16,300€ | **~23,000€** |
| Central estimate | ~18,000€ | ~35,000€ | **~53,000€** |
| Optimistic (upper bounds) | 35,800€ | 58,720€ | **~95,000€** |

The conservative estimate assumes a small, less active product and a low deficiency probability baseline. The optimistic estimate assumes a complex product with high SRS activity and the upper cost of a major deficiency round.

For a dual-market EU/US product, the regulatory cost avoided is effectively doubled — the same gap caught before filing prevents a deficiency in both markets simultaneously.

---

## Phase 2 ROI — ongoing maintenance and change management

Phase 2 covers the ongoing period after first approval — recurring costs and savings per year.

### UC1 Phase 2

| Dimension | Estimate |
|---|---|
| Annual SRS change events | 20–40 |
| Time saved per event | 1–3 hours |
| Annual time saving | 20–120 hours = 2,600–15,600€ |
| Annual regulatory cost avoided | 5–10k€ |
| **Annual Phase 2 value (UC1)** | **7,600–25,600€** |

### UC3 Phase 2

| Dimension | Estimate |
|---|---|
| Annual safety-relevant events | 8–20 |
| Time saved per event | 3–8 hours |
| Annual time saving | 24–160 hours = 3,100–20,800€ |
| Annual regulatory cost avoided | 15–40k€ |
| **Annual Phase 2 value (UC3)** | **18,100–60,800€** |

### Combined annual Phase 2 value

| Scenario | UC1 | UC3 | Combined |
|---|---|---|---|
| Conservative | 7,600€ | 18,100€ | **~26,000€/yr** |
| Central estimate | ~15,000€ | ~35,000€ | **~50,000€/yr** |
| Optimistic | 25,600€ | 60,800€ | **~86,000€/yr** |

---

## Break-even analysis

The initial release represents the majority of the total build effort. Using the dependency chain from `roadmap.md`, the initial release effort is estimated at approximately 2 (UC1) + 2 (UC3) = 4 effort points on the RICE scale. At a blended senior engineer cost of 130€/hour and assuming 200 hours per effort point:

| Scenario | Build cost estimate | Phase 1 value | Break-even |
|---|---|---|---|
| Conservative | ~104,000€ | ~23,000€ | Within Phase 2 year 2–3 |
| Central | ~104,000€ | ~53,000€ | Within Phase 2 year 1–2 |
| Optimistic | ~104,000€ | ~95,000€ | Within Phase 1 |

These figures are approximate. The build cost estimate uses a simple effort-point to hours conversion — the actual cost depends on the AI Architect's rate, the team structure, and the integration tier chosen for the initial deployment.

---

## Integration requirements for the initial release

The initial release can operate at Tier 0 (manual file upload) — no system integration required. This is the fastest path to deployment.

For meaningful Phase 2 value, a Tier 1 or Tier 2 integration to the document management platform is needed — so the agent detects change events automatically rather than requiring manual submission.

Minimum viable integration for Phase 2 value:
- Document management system: Tier 1 (scheduled sync) — provides document versions and status transitions
- Requirements or risk management system: Tier 1 (scheduled sync) — provides the risk-to-SRS traceability table for UC3
- Workflow / task system: Tier 3 (handoff) — delivers findings to document owners in their existing task workflow

See `docs/03-integration/system-categories.md` for data contracts per system category and `docs/03-integration/metadata-spec.md` for the tagging specification.

---

## Validation criteria for initial release sign-off

Before the initial release is considered complete, the following criteria must all be satisfied. These are drawn from `use-cases/uc1-srs-monitoring.md` and `use-cases/uc3-risk-traceability.md`.

**UC1:**
- [ ] Change classifier achieves ≥85% precision on the synthetic SRS v1→v2 delta test corpus
- [ ] All six change types correctly classified on at least two test cases each
- [ ] Reclassification trigger fires correctly on evaluation scenarios 12 and 13
- [ ] Findings routed to the correct owner role in all test scenarios
- [ ] Category I and Category IV produce visibly different output depth for the same change type
- [ ] Missing metadata fallback behaviour matches `output-calibration.md` specification

**UC3:**
- [ ] Missing risk control link detected on the RC-001 → SRS-005 test scenario
- [ ] Broken link detected when SRS-005 is modified in srs_v2.md
- [ ] Ambiguous link flagged when a requirement scope changes without updating the link record
- [ ] Dual-direction check works: agent detects both RC→SRS and SRS→RC gaps
- [ ] Reclassification trigger fires when a change removes isolation from a software item linked to a Class C requirement
- [ ] Output depth differs between Category I and Category IV for the same gap type

**Cross-cutting:**
- [ ] Audit log is append-only and exports correctly to a structured file
- [ ] All findings in the evaluation set are delivered within 5 minutes of trigger
- [ ] Finding identifier format matches `F-{YYYYMMDD}-{SEQUENCE}` specification in `finding-lifecycle.md`
- [ ] Zero findings generated that contain risk acceptability decisions or autonomous regulatory conclusions
