**Status:** Working draft
**Owner:** Product Management
**Audience:** AI Architect

---

# OWASP ASVS — Summary Reference

Summary of OWASP Application Security Verification Standard (ASVS) v4.0 control categories relevant to SaMD cybersecurity requirements. Used by the agent's UC5 cybersecurity sub-check.

OWASP ASVS is published under Creative Commons Attribution-ShareAlike 3.0. Full text available at https://owasp.org/www-project-application-security-verification-standard/

---

## Relevant control categories for SaMD

| ASVS Category | Section | Relevance to SaMD SRS |
|---|---|---|
| Authentication | V2 | Authentication requirements for clinical users and system interfaces |
| Session Management | V3 | Session timeout and token management requirements |
| Access Control | V4 | Role-based access control for clinical data and device functions |
| Validation, Sanitization, Encoding | V5 | Input validation requirements for clinical data processing |
| Cryptography | V6 | Encryption requirements for data at rest and in transit |
| Error Handling and Logging | V7 | Audit logging requirements — relevant to regulatory audit trail |
| Data Protection | V8 | Patient data protection requirements |
| Communications | V9 | Secure communications requirements for networked devices |
| Malicious Code | V10 | Software integrity requirements |
| Business Logic | V11 | Clinical workflow logic validation requirements |
| Files and Resources | V12 | File handling requirements for SRS document uploads |
| API and Web Service | V13 | API security requirements for integration interfaces |
| Configuration | V14 | Secure configuration requirements for deployed systems |

---

## How the agent uses this reference

UC5 (cybersecurity change impact) queries this summary when UC1 classifies a SRS change as "security/data flows". The agent maps the change type (new interface, new authentication mechanism, new data flow) to the relevant ASVS category and checks whether the SRS contains the corresponding security requirement. Missing requirements generate a finding citing the ASVS section and IEC 81001-5-1 clause.
