**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect, RA/QA consultants

---

# Output Calibration

This document defines how the agent's outputs change based on classification inputs. It is the most technically important document for the AI Architect building the finding generation and routing layers.

The agent is product-agnostic. The same use cases and the same analysis logic apply to every product. What changes is what the agent produces — the depth of the finding, the citations included, the severity assigned, who is notified, and what evidence is required. These outputs are calibrated by two classification inputs that must be present as structured metadata before the agent can function at full depth.

---

## The two classification inputs

### Input 1 — IMDRF significance category (device level)

The IMDRF significance category (I through IV) of the device being analysed. This is determined by the clinical significance of what the software does — the state of the healthcare situation it addresses and the significance of the information it provides to clinical decision-making.

This metadata lives at the product level in the agent's product registry. One value per product. It governs the overall regulatory burden applied to all findings for that product.

Source: the intended use document and regulatory classification rationale in the team's document management system, or manually entered through the UI by the RA/PRRC role.

### Input 2 — IEC 62304 software item safety class (item level)

The IEC 62304 safety class (A, B, or C) of the specific software item that the changed SRS requirement belongs to. This is determined by the potential harm if that item fails to function as specified.

This metadata lives at the requirement level — each SRS requirement is linked to a software item via the Software Architecture Document (SAD), and that item carries a safety class. The agent reads this from the requirements management system or the manually maintained traceability table.

Source: the Software Architecture Document (SAD), maintained by the Software Architect, imported into the agent via the requirements management system integration or manually entered through the UI.

### What happens when inputs are missing

If the IMDRF category is absent: the agent applies Category III defaults (conservative but not maximum) and flags the missing metadata as a High severity finding routed to the RA/PRRC role.

If the software item safety class is absent: the agent applies Class C defaults for all findings on that product and flags the missing metadata as a High severity finding routed to the Software Architect.

If both are absent: the agent applies Category III / Class C defaults throughout and generates a single Critical finding flagging both missing fields before proceeding with analysis.

Teams should resolve missing metadata before relying on the agent's findings for any formal regulatory purpose.

---

## Output calibration matrix

The following matrix defines what the agent produces at each combination of IMDRF category and software item safety class. Read across a row for the IMDRF effect; read down a column for the software item safety class effect. When the two inputs point to different calibration levels, the more stringent applies.

### By IMDRF category

| IMDRF Category | Finding depth | Severity floor | Citation depth | Routing | Escalation |
|---|---|---|---|---|---|
| I | Advisory | Low | Clause reference only | SRS owner only | Not automatic |
| II | Standard | Low–High | Clause + section | SRS owner + document owner | On Critical only |
| III | Standard with mandatory review | Medium–Critical | Clause + section + subsection | SRS owner + document owner + RA notification | On High and Critical |
| IV | Mandatory finding | High–Critical | Clause + section + subsection + evidence requirement | SRS owner + document owner + RA/PRRC mandatory | On all findings above Low |

### By software item safety class

| IEC 62304 class | Citation depth | Verification evidence requirement | Reclassification check | Audit trail depth |
|---|---|---|---|---|
| A | Clause reference only | None required | Not applicable | Standard log entry |
| B | Clause + section | Document traceability required | Triggered if isolation argument is affected | Standard log entry + rationale required |
| C | Clause + section + subsection | Full traceability to test case required | Triggered if isolation argument is affected | Full log entry + rationale required + RA notification on Critical |

### Combined calibration rule

When an IMDRF category and a software item safety class are both present, the agent applies the more stringent of the two calibrations independently for each output dimension.

**Example:** A Category II product has a Class C software item. For a finding on a requirement belonging to that item:
- Citation depth: Class C wins (clause + section + subsection), overriding Category II (clause + section)
- Routing: Category II wins (SRS owner + document owner), not modified by Class C
- Escalation: Class C finding on a Category II product — the Class C column says "triggered if isolation argument affected"; the Category II row says "on Critical only." Both conditions apply independently.

There is no averaging. Each dimension is evaluated separately and the more stringent value applies.

---

## Output depth in practice

### What "citation depth" means concretely

**Clause reference only** (Category I / Class A):
> "IEC 62304 section 5.2 — software requirements content may be incomplete."

**Clause + section** (Category II / Class B):
> "IEC 62304 section 5.2.2 — software requirements content: the requirement does not specify acceptance criteria as required by this clause."

**Clause + section + subsection** (Category III–IV / Class C):
> "IEC 62304 section 5.2.2(b) — software requirements content: the requirement SRS-045 does not specify the functional and performance requirements of the software item SI-003 (Class C). Under IEC 62304 section 5.2.2, requirements for Class C items must include measurable acceptance criteria. The current text 'system shall process data accurately' does not meet this standard."

### What "verification evidence requirement" means concretely

**None required** (Class A):
The finding notes the gap and routes it to the SRS owner. No specific evidence is required in the disposition.

**Document traceability required** (Class B):
The finding must be closed with a disposition that includes a reference to the document that addresses the gap — for example, the test case ID that verifies the requirement, or the risk control ID that the requirement implements.

**Full traceability to test case required** (Class C):
The finding must be closed with a disposition that includes: the SRS requirement ID, the test case ID that verifies it, the risk control ID it implements (if safety-relevant), and confirmation that the test case has been updated to reflect any requirement change.

### What "routing" means concretely

**SRS owner only** (Category I):
One notification to the Requirements Engineer. No other stakeholders are notified unless the finding is escalated manually.

**SRS owner + document owner** (Category II):
Two notifications — the Requirements Engineer and the owner of the most affected controlled document (Risk Engineer, Cybersecurity Engineer, Usability Specialist, or Clinical Affairs, depending on the change type).

**SRS owner + document owner + RA notification** (Category III):
Three notifications — as above, plus an informational notification to the Regulatory Affairs Specialist. RA does not need to take action on every finding but is kept informed of all findings at this level.

**SRS owner + document owner + RA/PRRC mandatory** (Category IV):
Three notifications — as above, but the RA/PRRC notification is mandatory and the finding cannot reach Resolved or Closed state until the RA/PRRC role has acknowledged it. This acknowledgement is logged as a separate audit trail entry.

---

## Reclassification trigger logic

The agent checks for two types of potential reclassification on every analysis run.

### Device-level reclassification check

Triggered when a SRS change:
- Adds a new clinical function not present in the current intended use
- Changes the significance of the software's output (from "inform" to "drive" or "treat/diagnose")
- Expands the target patient population or the clinical conditions addressed
- Adds an autonomous decision-making function where one did not previously exist

When triggered, the agent generates a reclassification finding with mandatory acknowledgement (see `finding-lifecycle.md`). The finding cites: the current IMDRF category, the specific SRS change that may affect it, and the classification criteria that the change potentially crosses.

The finding is routed to the RA/PRRC role. No other findings from the same analysis run are surfaced until the reclassification finding has been acknowledged.

### Software item safety class check

Triggered when a SRS change:
- Adds a new interface between the affected software item and an item of higher safety class
- Removes a defensive mechanism (validation, error handling, fallback) that formed part of the isolation argument
- Changes the data flow such that the item now contributes to a function it previously did not
- Modifies the failure mode of the item such that a previously Class A or B outcome could now result in patient harm

When triggered, the agent generates a reclassification finding routed jointly to the Software Architect and the Risk Engineer. The finding cites: the current safety class of the affected item, the SAD section that documents the isolation argument, and the specific SRS change that may affect the argument.

### Downward reclassification

The agent also checks for cases where a SRS change introduces new isolation — a new safety mechanism, a new monitoring layer, or a new architectural boundary — that may justify reducing a software item's safety class. When detected, the agent generates an advisory finding (Low severity) noting the potential downgrade opportunity. The Software Architect and RA/PRRC must jointly evaluate and document the isolation argument before any safety class reduction is applied.

### IEC 62366-1 exception

Software item safety class decomposition does not apply to usability engineering obligations. The scope of the summative usability study is determined by the complete user interface of the device — it cannot be reduced by arguing that a particular UI software item is Class B. The agent applies this rule in UC7 regardless of the safety class of the requirement being changed. A UC7 finding on a Class A UI component carries the same usability engineering obligation as a UC7 finding on a Class C component.

---

## AI-enabled product overlay

For products where the IMDRF product registry entry includes an AI-enabled flag, the agent applies an additional calibration layer on top of the standard IMDRF + safety class matrix.

### Additional finding categories for AI-enabled products

| Finding category | Trigger | Citation | Routes to |
|---|---|---|---|
| Human oversight requirement | SRS change modifies or removes a human oversight mechanism | EU AI Act Article 14 / FDA AI guidance | RA/PRRC mandatory |
| Change control plan boundary | SRS change may exceed PCCP or Article 83 boundaries | FDA PCCP guidance / EU AI Act Article 83 | RA/PRRC mandatory + AI Architect |
| Algorithmic transparency requirement | SRS change affects how AI outputs are communicated to users | FDA AI guidance | Requirements Engineer + Clinical Affairs |
| AI performance specification | SRS change modifies accuracy or robustness thresholds | EU AI Act Article 15 / FDA AI guidance | AI Engineer + Clinical Affairs |
| Training data governance | SRS change implies a model update with training data implications | EU AI Act Annex IV / FDA PCCP guidance | AI Engineer + RA/PRRC |

These categories are in addition to, not instead of, the standard findings for the underlying change type. An AI performance specification change may also trigger a risk traceability finding (UC3) and a cybersecurity finding (UC5) — all three are generated independently and routed to their respective owners.

### Change control plan boundary check output

When the agent's UC4 analysis detects that a proposed SRS change may exceed PCCP or Article 83 boundaries, the finding includes:

1. The specific PCCP or Article 83 section that bounds the type of change
2. The specific aspect of the SRS change that appears to exceed the bound
3. An assessment of whether the exceedance is definitive or ambiguous
4. For definitive exceedances: a mandatory RA/PRRC escalation with a hold recommendation
5. For ambiguous cases: a mandatory clarification request to the RA/PRRC role before the analysis can be closed

---

## Fallback behaviour

When the agent cannot determine the correct calibration due to missing or inconsistent metadata, it applies the following fallbacks in order:

1. **Missing IMDRF category** → apply Category III defaults, flag as High severity finding to RA/PRRC
2. **Missing software item link for a requirement** → apply Class C defaults for that requirement, flag as High severity finding to Software Architect
3. **Inconsistent safety class** (item exists in registry but class is missing) → apply Class C defaults, flag as Medium severity finding to Software Architect
4. **No product registry entry for the document being analysed** → halt analysis, generate a Critical finding to system administrator, do not proceed until the product is registered

Fallback behaviour is conservative by design. The cost of over-flagging is a manageable number of false positives. The cost of under-flagging due to missing metadata is a missed compliance gap.

---

## Calibration configuration

The calibration logic described in this document is implemented as configuration in the agent's analysis engine, not hardcoded. The following parameters are configurable per product:

| Parameter | Default | Configurable by |
|---|---|---|
| IMDRF category | None (must be set) | RA/PRRC via product registry |
| Software item safety classes | None (must be set) | Software Architect via item registry |
| AI-enabled flag | False | RA/PRRC via product registry |
| Escalation targets by severity | Default roles | Admin via routing configuration |
| Mandatory acknowledgement threshold | Category IV and reclassification findings | Admin (not recommended to lower) |
| Fallback calibration tier | Category III / Class C | Admin (not recommended to lower) |

The mandatory acknowledgement threshold and fallback calibration tier have a recommended minimum. Lowering these settings reduces the agent's conservatism and increases the risk of a missed high-consequence finding. Any change to these settings should be documented as a configuration decision with a rationale and reviewed by the RA/PRRC role.