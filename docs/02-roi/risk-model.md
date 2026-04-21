# Risk Model (ISO 14971)

**Product metadata (required for classification-calibrated analysis):**
- IMDRF significance category: `3` *(illustrative — update to reflect actual product)*
- Primary regulatory markets: `EU MDR, FDA` *(illustrative)*

| Hazard ID | Hazard | Harm | Risk Control ID | SRS Req ID(s) | Software Item ID | Item Safety Class |
|-----------|--------|------|-----------------|---------------|------------------|-------------------|
| H-001 | Data corruption | Patient harm | RC-001 | SRS-005 | SI-003 | C |
| H-002 | Unauthorized access | Privacy breach | RC-002 | SRS-001, SRS-010 | SI-001 | B |
| H-003 | System outage | Delayed care | RC-003 | SRS-015 | SI-002 | B |

> **Reclassification note:** If a SRS change modifies or removes the architectural isolation that justifies a software item's current safety class, the agent will flag a potential reclassification. The Risk Engineer and Software Architect must jointly assess and document the outcome.
>
> **IEC 62366-1 exception:** Usability engineering obligations apply at the system level, not the software item level. A software item's Class B or A designation does not reduce the scope of the summative usability study.

**Agent checks**: Each RC has corresponding SRS req → flags gaps/changes.
