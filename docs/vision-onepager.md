# SRS & Risk File Review Copilot – Product Vision

## The Challenge

Medical device software teams operating under EU MDR, FDA, and international standards (ISO 13485, IEC 62304, ISO 14971, IEC 81001‑5‑1) face a critical documentation challenge:

- **SRS and risk files** are configuration‑controlled, version‑managed artifacts
- They must continuously align with evolving standards, internal SOPs, and security best practices
- Manual reviews are slow, error‑prone, and resource‑intensive
- Git/GitHub workflows manage versions, but quality checks remain manual
- Missed gaps lead to audit findings, delays, and rework

---

## Our Solution

An **AI‑powered documentation copilot** that embeds directly into your Git/GitHub workflow:

### What It Does

✅ **Monitors SRS and risk files** in GitHub repos  
✅ **Triggers on lifecycle events**: PR updates, approval labels, version tags  
✅ **Analyzes against standards**: IEC 62304, ISO 14971, OWASP security checklists, your SOPs  
✅ **Generates findings with citations**: traceable references to specific clauses  
✅ **Proposes corrections**: actionable suggestions, not just problems  
✅ **Routes to stakeholders**: RA, QA, Risk, Cybersecurity, Clinical teams  
✅ **Logs decisions**: full audit trail tied to Git history

### What It Doesn't Do

❌ No autonomous regulatory decisions  
❌ No clinical decision support  
❌ No automated risk acceptance  
❌ Always requires human review and approval

---

## Value Proposition

### For Requirements Owners & System Engineers
- Catch gaps before peer review
- Get instant feedback on completeness and clarity
- Reduce review cycles and rework

### For Regulatory Affairs & QA
- Systematic, repeatable SRS quality checks
- Documented evidence of compliance due diligence
- Faster preparation for audits and submissions

### For Risk Management
- Ensure risk files stay aligned with SRS changes
- Identify missing hazard/harm/control mappings
- Maintain ISO 14971 traceability

### For Cybersecurity Teams
- Proactive detection of missing security requirements
- OWASP‑aligned gap analysis
- IEC 81001‑5‑1 compliance support

### For the Organization
- **Faster time to approval**: reduce manual review bottlenecks
- **Lower audit risk**: catch issues early, not during inspections
- **Scalable quality**: maintain high standards as team and complexity grow
- **Knowledge capture**: embed organizational standards into the workflow

---

## Designed for Regulated Environments

🔒 **Non‑binding**: all outputs are proposals, not decisions  
🔒 **Traceable**: every finding links to source clauses and Git commits  
🔒 **Auditable**: full decision log for regulatory inspection  
🔒 **Explainable**: clear reasoning and citations for every recommendation  
🔒 **Human‑centric**: supports expert judgment, doesn't replace it

---

## Portfolio MVP Scope

For this demonstrator project, we focus on:

- **Monitoring SRS and risk files** in GitHub
- **Detecting changes** via pull requests and labels
- **Analyzing against** IEC 62304, ISO 14971, and security checklists
- **Generating findings** with citations and proposed corrections
- **Demonstrating metrics** for both Product and AI Architecture success

This establishes the foundation for a production‑ready compliance automation platform.
