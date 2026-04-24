**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect

---

# Metadata Specification

Defines the two classification metadata fields that must be present before the agent can produce calibrated outputs, where they come from, how they are structured, and what the agent does when they are missing.

This is a prerequisite document. The AI Architect should read it before designing the ingestion layer. Teams deploying the agent should resolve both fields before using findings for any formal regulatory purpose.

---

## Why these two fields

The agent's output calibration — which findings it generates, how deeply it cites, who it notifies, what evidence it requires — depends on two inputs per analysis run:

1. The IMDRF significance category of the device being reviewed
2. The IEC 62304 safety class of the software item the changed SRS requirement belongs to

Without these fields, the agent cannot distinguish a high-consequence finding from a low-consequence finding. It falls back to conservative defaults that produce findings of uniform depth — useful but not calibrated, and not defensible as classification-specific regulatory evidence.

These are not optional fields that can be added later. They should be resolved before the first production analysis run.

---

## Field 1 — IMDRF significance category

### Definition

The IMDRF SaMD significance category (I, II, III, or IV) of the device under analysis, based on the intersection of the healthcare situation severity and the significance of the information the software provides. See `docs/00-overview/classification-reference.md` for the full framework and national market mappings.

### Scope

One value per product. All findings generated for documents belonging to that product use this value for output calibration.

### Format

Integer: `1`, `2`, `3`, or `4`.

### Where it comes from

The IMDRF category is derived from the intended use document and the regulatory classification rationale. It must be determined by a qualified regulatory professional — it is not a field the agent infers automatically.

**Source of truth:** The intended use document or regulatory strategy document in the document management system.

**How it enters the agent:**
- Preferred: synced from the document management system if the intended use document contains a structured classification field (Tier 1 integration)
- Fallback: manually entered by the RA/PRRC role through the product registry in the agent's UI

### Schema

```json
{
  "product_id": "PROD-001",
  "product_name": "Example SaMD Product",
  "imdrf_category": 3,
  "regulatory_markets": ["EU_MDR", "FDA"],
  "ai_enabled": false,
  "classification_rationale_doc_id": "DOC-0012",
  "classification_confirmed_by": "RA/PRRC role",
  "classification_confirmed_date": "2026-04-15"
}
```

### Validation rules

- Value must be an integer between 1 and 4 inclusive
- Must be confirmed by a named individual in a qualified role (RA/PRRC minimum)
- Must reference the source document from which it was derived
- Must be reviewed when the intended use document is updated

### Multi-market products

For products targeting multiple regulatory markets, use the most stringent applicable IMDRF category. If the product is Category III in the EU and Category II under FDA, record `3`. The agent applies Category III calibration throughout — it does not split output by market within a single analysis run.

---

## Field 2 — IEC 62304 software item safety class

### Definition

The IEC 62304 safety class (A, B, or C) assigned to each software item in the product's software architecture. See `docs/00-overview/classification-reference.md` for the full safety class definitions and the isolation argument requirements.

### Scope

One value per software item. Applied at the requirement level — each SRS requirement is linked to a software item, and the agent reads the safety class of that item when generating a finding for that requirement.

### Format

String: `"A"`, `"B"`, or `"C"`.

### Where it comes from

The software item safety class is assigned by the Software Architect in the Software Architecture Document (SAD). It must be documented alongside the isolation argument that justifies any class lower than the overall device's implied class.

**Source of truth:** The Software Architecture Document (SAD), maintained as a controlled document by the Software Architect.

**How it enters the agent:**
- Preferred: synced from the requirements and traceability management system, attached to the software item record that the SRS requirement links to (Tier 1 integration)
- Fallback: manually entered by the Software Architect through the software item registry in the agent's UI

### Schema — software item record

```json
{
  "product_id": "PROD-001",
  "item_id": "SI-003",
  "item_name": "Clinical data processing module",
  "safety_class": "C",
  "isolation_argument": "Directly contributes to clinical recommendations — no isolation possible",
  "sad_reference": "SAD section 4.3",
  "assigned_by": "Software Architect",
  "assigned_date": "2026-03-10",
  "last_reviewed": "2026-04-15"
}
```

### Schema — SRS requirement to item link

```json
{
  "requirement_id": "SRS-045",
  "software_item_id": "SI-003",
  "link_type": "implements",
  "link_confirmed_date": "2026-03-15"
}
```

### Validation rules

- Value must be `"A"`, `"B"`, or `"C"` — no other values accepted
- Every software item with a safety class of A or B must have a documented isolation argument referencing the SAD section that supports it
- Every SRS requirement must be linked to at least one software item
- A requirement linked to multiple items takes the highest safety class of those items
- The isolation argument must be reviewed whenever a SRS change may affect the interfaces between items

### Reclassification monitoring

The agent compares the current safety class against what the SRS change implies. If the change:
- Adds a new interface between the item and a higher-class item
- Removes a defensive mechanism cited in the isolation argument
- Changes the data flow such that the item now contributes to a clinical function

...the agent generates a reclassification flag for joint review by the Software Architect and Risk Engineer. The flag does not automatically change the safety class — that requires a documented architectural reassessment.

---

## Combined traceability chain

The full chain the agent needs to produce a calibrated finding for any SRS requirement:

```
Product
  └── IMDRF category [Field 1]
        └── SRS document
              └── SRS requirement (SRS-NNN)
                    └── Software item (SI-NNN)
                          └── Safety class [Field 2]
                                └── Risk control link (RC-NNN) [for UC3]
```

All links in this chain must be present and current. A break at any point degrades the agent's ability to calibrate its output for that requirement.

---

## Fallback behaviour

When metadata is missing, the agent applies conservative defaults and generates a metadata gap finding before proceeding with analysis.

| Situation | Fallback | Finding generated |
|---|---|---|
| IMDRF category absent | Apply Category III defaults | High severity → RA/PRRC |
| IMDRF category present but invalid | Apply Category III defaults | High severity → RA/PRRC |
| Software item link absent for a requirement | Apply Class C defaults for that requirement | High severity → Software Architect |
| Software item safety class absent | Apply Class C defaults for that item | High severity → Software Architect |
| Both fields absent | Apply Category III / Class C defaults | Critical severity → RA/PRRC + Software Architect + Admin |
| No product registry entry | Halt analysis | Critical → Admin only; no findings delivered to document owners |

Fallback behaviour is conservative by design. Over-flagging produces manageable false positives. Under-flagging due to missing metadata produces missed compliance gaps.

---

## Deployment readiness checklist

Before the agent is used for production analysis on any product, confirm the following:

- [ ] Product registered in the agent's product registry with IMDRF category confirmed by RA/PRRC
- [ ] All software items listed in the SAD are entered in the agent's software item registry with safety class and isolation argument
- [ ] All SRS requirements are linked to their software item in the requirements management system or the agent's traceability table
- [ ] All risk controls are linked to the SRS requirements that implement them (for UC3)
- [ ] IMDRF category references the current version of the intended use document
- [ ] Software item safety classes reference the current version of the SAD
- [ ] At least one test run completed on a non-critical document to verify routing and output depth before production use

---

## Maintenance

Both fields are living data — they must be updated when the underlying documents change.

| Change event | Required metadata update |
|---|---|
| Intended use document updated | Review IMDRF category — confirm it still reflects the updated scope |
| SAD updated with new software item | Add item to agent's software item registry with safety class |
| SAD updated with modified isolation argument | Review and update safety class if the isolation argument changes |
| SRS requirement added or modified | Confirm requirement-to-item link is current |
| Reclassification finding accepted | Update safety class in item registry + update SAD |
| Reclassification finding rejected | Document rejection rationale — no registry update needed |

The Software Architect is responsible for keeping the software item registry current. The RA/PRRC is responsible for keeping the IMDRF category current. Both should be reviewed at every major release milestone as part of the technical file update process.
