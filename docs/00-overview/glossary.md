**Status:** Working draft
**Owner:** Product Management
**Audience:** All stakeholders

---

# Glossary

Definitions of key terms used across this repository. If a term appears in a document without explanation, the definition is here.

---

| Term | Definition |
|---|---|
| **SaMD** | Software as a Medical Device. Software that performs a medical function without being part of a hardware medical device. Subject to regulatory oversight in all major markets — including EU MDR, US FDA, Health Canada, TGA (Australia), and others. |
| **SRS** | Software Requirements Specification. The controlled document that defines what the software must do. Central artefact in the IEC 62304 software lifecycle. |
| **Regulatory reviewer** | The authority responsible for assessing a submission or change. In the EU this is a Notified Body — an accredited third-party organisation. In the US this is the FDA. In other markets, equivalent national authorities apply. |
| **Submission** | A formal application to a regulatory authority to place a device on the market, or to register a significant change to an approved device. Examples: 510(k) or De Novo request (FDA); CE marking application under EU MDR. |
| **Significant change** | A change to a device that, under applicable regulations, requires a new or updated submission to the regulatory authority before the change can be implemented. Criteria differ by jurisdiction. |
| **Deficiency / deficiency round** | When a regulatory reviewer identifies gaps or inconsistencies in a submission, they issue a list of deficiencies (FDA: additional information request; EU: list of outstanding issues). Each round of deficiency resolution adds cost and delay. |
| **Technical File / DHF** | Technical File (EU MDR) or Design History File (US FDA): the complete record of evidence supporting a device's safety and performance claims. Must be kept current throughout the device lifecycle. |
| **IEC 62304** | International standard for the software lifecycle of medical device software. Defines requirements for planning, development, testing, maintenance, and change management. |
| **ISO 14971** | International standard for risk management for medical devices. Defines the process for identifying hazards, estimating and evaluating risks, and implementing risk controls. |
| **Risk control** | A measure taken to reduce the probability or severity of a harm caused by a hazard. Risk controls must be implemented in the SRS as verifiable requirements and traced throughout the technical file. |
| **MDR** | EU Medical Device Regulation 2017/745. The primary regulatory framework for medical devices in the European Union. |
| **FDA** | US Food and Drug Administration. The US federal agency responsible for regulating medical devices in the United States. |
| **PCCP** | Predetermined Change Control Plan. An FDA mechanism that allows manufacturers of AI/ML-enabled devices to pre-specify the types of changes they may make without requiring a new submission. The EU equivalent concept appears in Article 83 of the EU AI Act. |
| **PRRC** | Person Responsible for Regulatory Compliance. A mandatory role under EU MDR Article 15, responsible for ensuring regulatory obligations are met. |
| **IMDRF** | International Medical Device Regulators Forum. An international body that develops guidance to harmonise medical device regulation across markets. The IMDRF SaMD significance framework (Categories I–IV) is used throughout this repository as the primary classification spine. |
| **OWASP / ASVS** | Open Web Application Security Project / Application Security Verification Standard. A freely available framework of security requirements used to assess the security of software applications. Used as a reference corpus for UC5. |
| **IEC 81001-5-1** | International standard for cybersecurity activities in the health software lifecycle. Defines security requirements from design through maintenance. Referenced in FDA pre-market cybersecurity guidance and EU MDR Annex I GSPR 17. |
| **QMS** | Quality Management System. The set of processes, procedures, and controls a manufacturer uses to ensure consistent product quality and regulatory compliance. Often aligned with ISO 13485. |
| **RAG** | Retrieval-Augmented Generation. An AI architecture in which a language model retrieves relevant context from a document index before generating a response. Used in this agent to provide citation-backed findings. |
| **RICE** | A product prioritisation framework adapted for this product: (Risk Savings × Impact × Confidence) / Effort × 10. Standard RICE uses Reach (user count) as the value driver; this product replaces Reach with Risk Savings because the value driver is regulatory cost avoidance, not user volume. See `docs/02-roi/assumptions.md`. |
| **V-model** | A software development model in which each development phase has a corresponding verification or validation phase. Standard in regulated medical device development under IEC 62304. |
| **SOUP** | Software of Unknown Provenance. Third-party software components (libraries, frameworks, operating system elements) used in a medical device. IEC 62304 requires SOUP to be identified, evaluated, and monitored for changes. |
| **SBOM** | Software Bill of Materials. A structured inventory of all software components in a product, including SOUP items. Increasingly required by FDA and EU MDR for connected and AI-enabled devices. |
