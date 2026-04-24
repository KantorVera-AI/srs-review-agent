**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, RA/QA consultants

---

# Risk Model (Synthetic Test Data)

This is the synthetic risk management file used as test data for UC3 (risk traceability check). It is illustrative only — it does not represent any real product.

---

## Product metadata

| Field | Value | Notes |
|---|---|---|
| IMDRF significance category | 3 | Serious situation / drive clinical management — illustrative |
| Primary regulatory markets | EU MDR, FDA | Illustrative |
| IEC 62304 software safety class (system) | B | Illustrative overall classification |

---

## Software item registry

| Item ID | Description | Safety class | Isolation argument |
|---|---|---|---|
| SI-001 | User authentication module | B | Isolated from clinical algorithm — failure causes access denial, not clinical error |
| SI-002 | System availability monitor | B | Does not contribute to clinical outputs — failure causes service interruption only |
| SI-003 | Clinical data processing module | C | Directly contributes to clinical recommendations — no isolation possible |

> **Reclassification note:** If a SRS change modifies or removes the architectural isolation described above, the agent will flag a potential safety class reclassification. The Risk Engineer and Software Architect must jointly assess and document the outcome before the change is approved.

---

## Risk table

| Hazard ID | Hazard | Harm | Risk control ID | SRS Req ID(s) | Software item ID | Item safety class |
|---|---|---|---|---|---|---|
| H-001 | Data corruption | Incorrect clinical recommendation — patient harm | RC-001 | SRS-005 | SI-003 | C |
| H-002 | Unauthorised access | Privacy breach / data modification | RC-002 | SRS-001, SRS-010 | SI-001 | B |
| H-003 | System outage | Delayed care | RC-003 | SRS-015 | SI-002 | B |

**Agent checks for UC3:** Each risk control (RC-001, RC-002, RC-003) must have at least one current, valid SRS requirement implementing it. The agent flags missing links, broken links, and ambiguous links.

---

## Traceability verification

The following links are used in evaluation scenarios:

| Scenario | What is tested |
|---|---|
| Scenario 4 — RC-001 → SRS-005 | Valid link — agent confirms it exists |
| Scenario 5 — RC-001 broken | SRS-005 removed in srs_v2.md — agent detects missing link |
| Scenario 12 — SI-002 isolation removed | SRS change adds interface between SI-002 and SI-003 — agent flags reclassification risk |

---

## Notes

> **IEC 62366-1 exception:** The software item safety class assignments above do not affect usability engineering obligations. Usability engineering under IEC 62366-1 applies at the system level. The scope of the summative usability study covers the complete user interface regardless of the safety class of individual software items implementing parts of it.

> **Dual-market note:** The risk controls in this table are applicable under both ISO 14971:2019 (EU MDR harmonised) and FDA 21 CFR 820.30 design control requirements. The agent cites both frameworks when generating findings for products targeting both markets.
