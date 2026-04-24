**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, PM

---

# UC3 — Risk traceability check

**Release tier:** Initial release
**Depends on:** UC1 (change classification)
**Required by:** UC4 (change control plan check uses the same traceability infrastructure), UC6 (inspection preparation aggregates traceability data)

---

## One-line description

For every SRS change classified as safety-relevant, verify that every risk control in the risk management file still has a corresponding SRS requirement, and flag gaps or broken links.

---

## What triggers it

UC1 classifies a change as **risk/safety** or **clinical**. The traceability resolver then queries the risk-to-SRS traceability table against the current SRS to identify risk control links that are:
- **Missing** — a risk control exists in the risk management file but no SRS requirement implements it
- **Broken** — a SRS requirement previously implementing a risk control has been modified or removed
- **Ambiguous** — the link exists but the requirement no longer clearly implements the control (e.g. scope has changed)

The traceability table that UC3 reads is the same table that the Risk Engineer maintains as a controlled document — mapping risk control IDs to SRS requirement IDs. This table must be current for UC3 to produce accurate findings. Stale data generates false negatives.

---

## What the agent does

1. Receives the safety-relevant or clinical change classification from UC1
2. Identifies which SRS requirements were affected by the change
3. Queries the risk-to-SRS traceability table for all risk controls linked to those requirements
4. For each risk control, verifies that a valid, current SRS requirement implementing it still exists
5. Checks the reverse direction: for requirements that implement risk controls, verifies the risk control still exists and is current in the risk management file
6. Generates a finding for each gap, broken link, or ambiguity detected
7. Checks whether the change may affect the software item safety class of the modified item (reclassification trigger)

---

## Who receives the output

| Output | Recipient | Condition |
|---|---|---|
| Risk traceability finding | Risk / Safety Engineer | Always — primary recipient |
| RA/PRRC notification | RA / PRRC | Category III and IV products |
| Reclassification flag | RA/PRRC + Software Architect | Reclassification trigger detected |
| QA notification | QA / Validation Engineer | Broken link affects a requirement with an existing test case |

Finding format: hazard identifier, risk control identifier, expected SRS requirement identifier, finding type (missing / broken / ambiguous), standard clause citation (ISO 14971 section 7.3.3), and the IMDRF category and software item safety class that calibrated the severity.

---

## RICE score

| Risk savings | Impact | Confidence | Effort | Score |
|---|---|---|---|---|
| 5 | 4 | 0.85 | 2 | 85 |

*Risk savings of 5: broken traceability between risk controls and SRS requirements is the most common cause of regulatory reviewer deficiency rounds in SaMD submissions — consistently cited in both EU MDR notified body findings and FDA additional information requests. Confidence of 0.85: the test data and traceability table format are already defined. Effort of 2: shares infrastructure with UC1.*

---

## Benefit breakdown

### Phase 1 — Initial development

| Dimension | Estimate |
|---|---|
| Typical events | All safety-relevant SRS changes during development (typically 15–30% of all SRS events) |
| Time saved per event | 2–6 hours of manual risk file cross-check |
| Total time saving | 10–144 hours = 1,300–18,720€ |
| Regulatory cost avoided | 15–40k€ — broken traceability at first submission is among the most common deficiency causes in both EU and US markets |

### Phase 2 — Ongoing maintenance

| Dimension | Estimate |
|---|---|
| Annual events per product | 8–20 safety-relevant SRS changes per year |
| Time saved per event | 3–8 hours of manual risk file cross-check |
| Annual time saving | 24–160 hours = 3,100–20,800€ |
| Regulatory cost avoided | 15–40k€ per avoided major deficiency round |

> **Dual-market note:** For products filing simultaneously to EU and US markets, catching a traceability gap before filing prevents a deficiency in both markets simultaneously. The avoided cost is additive — one finding can prevent two deficiency rounds.

---

## Key assumptions

- The risk-to-SRS traceability table must be maintained by the Risk Engineer as a controlled document. If the table is not kept current, UC3 generates false negatives — gaps that exist are not detected.
- 15–40k€ regulatory cost avoidance assumes a moderately complex SaMD where a major deficiency round costs 50–100k€ total, and where poor traceability increases deficiency probability by 15–25%. Adjust for simpler products or lower-risk submissions.
- The risk management file must be in a structured, machine-readable format. If it is maintained in a proprietary QMS tool rather than a structured document format, an integration layer will be required before UC3 can function.

---

## Dependencies and risks

**Dependencies:** UC1 for change classification. Risk management file in a structured, queryable format. Risk-to-SRS traceability table maintained as a controlled document.

**Technical risks:**
- If the risk management file is in a proprietary QMS tool without a structured export, the integration effort required is significant and should be scoped with the AI Architect before the initial release.
- False negatives from a stale traceability table are worse than false positives — a missed broken link may pass undetected into a submission.

**Process risks:**
- The Risk Engineer must treat the traceability table as a first-class controlled document, not an informal reference. This is a process change that may require team agreement before deployment.

---

## Regulatory basis

| Requirement | Standard | Clause |
|---|---|---|
| Risk control traceability | ISO 14971:2019 | Section 7.3.3 |
| Risk control implementation in SRS | IEC 62304:2006 | Section 5.2.3 |
| Design input traceability | FDA 21 CFR 820.30(e) | Design inputs |
| Risk management file maintenance | EU MDR Annex I | GSPR 3 |

---

## Validation criteria

Before marking UC3 complete in the initial release:

- [ ] Missing risk control link detected correctly on the `risk_v1.md` test scenario (RC-001 → SRS-005 link)
- [ ] Broken link detected correctly when SRS-005 is modified in `srs_v2.md`
- [ ] Ambiguous link flagged correctly when a requirement scope changes but the link record is not updated
- [ ] Dual-direction check works: agent detects both RC→SRS and SRS→RC gaps
- [ ] Reclassification trigger fires when a change removes isolation from a software item linked to a Class C requirement
- [ ] Output depth visibly differs between