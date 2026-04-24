**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect

---

# ISO 14971 Risk Table — Illustrative Reference

Synthetic reference document illustrating the ISO 14971:2019 risk management table structure used in the agent's UC3 test corpus. It is illustrative only — it does not represent any real product.

---

## Risk table structure

| Field | Description | Example |
|---|---|---|
| Hazard ID | Unique identifier for the hazard | H-001 |
| Hazard | The potential source of harm | Data corruption |
| Hazardous situation | Sequence of events leading to harm | Corrupted data displayed to clinician |
| Harm | Injury or damage to health | Incorrect clinical decision — patient harm |
| Probability (P1) | Likelihood of hazardous situation occurring | 3 (occasional) |
| Severity (S) | Severity of harm if it occurs | 4 (critical) |
| Initial risk | P1 × S before controls | 12 — unacceptable |
| Risk control ID | Identifier of the risk control measure | RC-001 |
| Risk control | The measure implemented to reduce risk | Encrypt and validate data on write and read |
| SRS Req ID(s) | SRS requirements implementing the control | SRS-005 |
| Software item ID | Software item implementing the requirement | SI-003 |
| Item safety class | IEC 62304 safety class of the item | C |
| Residual risk | Estimated risk after control | 4 — acceptable |
| Verification reference | Evidence that the control is implemented | Test case TC-0047 |

---

## Clause reference

| Obligation | ISO 14971:2019 clause |
|---|---|
| Hazard identification | 5.4 |
| Risk estimation | 5.5 |
| Risk evaluation | 5.6 |
| Risk control | 6.2 |
| Residual risk evaluation | 6.4 |
| Risk control traceability | 7.3.3 |
| Risk management file | 4.5 |

The agent uses clause 7.3.3 as the primary citation when generating UC3 traceability gap findings.
