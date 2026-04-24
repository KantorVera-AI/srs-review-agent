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

> **Reclassification note:** If a SRS change modifies or removes the architectural isolation described above, the agent will flag a potential safety clas