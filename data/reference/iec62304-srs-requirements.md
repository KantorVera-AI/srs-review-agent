**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect

---

# IEC 62304 SRS Requirements Checklist

Synthetic checklist of IEC 62304:2006+A1:2015 requirements applicable to Software Requirements Specifications. Used as a reference corpus for UC1 and UC3 finding generation.

---

## Section 4 — General requirements

| Clause | Requirement | Safety class |
|---|---|---|
| 4.3 | Software items shall be assigned a software safety class (A, B, or C) based on the potential severity of harm if the item fails | All |
| 4.3 | Class A: no injury possible. Class B: non-serious injury possible. Class C: death or serious injury possible | All |
| 4.3 | Isolation argument must be documented for any item assigned a lower class than the overall device implies | B, C |

## Section 5.2 — Software requirements analysis

| Clause | Requirement | Safety class |
|---|---|---|
| 5.2.1 | Software requirements shall be defined from system requirements | All |
| 5.2.2 | Software requirements shall include functional and capability requirements | All |
| 5.2.2 | Software requirements shall include performance requirements | All |
| 5.2.2 | Software requirements shall include interface requirements | All |
| 5.2.2 | Software requirements shall include safety requirements derived from risk management | B, C |
| 5.2.2 | Software requirements shall include security requirements | All |
| 5.2.3 | Software requirements shall include risk controls identified in the risk management process | B, C |
| 5.2.4 | Software requirements shall be evaluated for correctness, consistency, completeness, and verifiability | All |
| 5.2.5 | Software requirements shall be updated as the software design evolves | All |
| 5.2.6 | Software requirements content shall be documented | All |

## Section 5.7 — Software configuration management

| Clause | Requirement | Safety class |
|---|---|---|
| 5.7.1 | A software configuration management plan shall be established | All |
| 5.7.2 | All items under configuration management shall be uniquely identified | All |

## Section 5.8 — Software problem resolution

| Clause | Requirement | Safety class |
|---|---|---|
| 5.8.1 | A process shall exist for analysing and resolving software problems | All |
| 5.8.7 | The impact of problem resolution on safety shall be evaluated | B, C |

## Section 6 — Software maintenance process

| Clause | Requirement | Safety class |
|---|---|---|
| 6.2.1 | A software modification shall be analysed to determine potential impact on safety | All |
| 6.2.4 | Software problem reports shall be evaluated to determine whether they affect safety | B, C |

---

> **Note:** Section 4.3 covers software safety classification — not SRS content requirements. SRS content requirements are in section 5.2. This distinction is critical for correct citation in agent findings.
