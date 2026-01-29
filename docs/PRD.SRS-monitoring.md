# SRS & Risk File Review Copilot – Product Requirements Document

**Domain**  
Software as a Medical Device (SaMD) / medical device software – global (EU MDR, FDA, ISO 13485, IEC 62304, ISO 14971, IEC 81001‑5‑1, security best practices such as OWASP).

**Product Category**  
AI‑assisted documentation review tool integrated into a version‑controlled SRS/risk management process.

**Owner**  
Product Management

**Status**  
Draft v1.1 – Portfolio MVP

---

## 1. Purpose

The SRS & Risk File Review Copilot automatically reviews version‑controlled **Software Requirements Specifications (SRS)** and, optionally, **risk files** at key lifecycle states (draft, ready for review/approval, modified, or made obsolete).

It runs as part of the Git/GitHub workflow and generates traceable, citation‑backed, non‑binding findings about gaps or weaknesses, plus proposed corrections, for human review.

---

## 2. Problem Statement

In regulated environments, SRS and risk files are configuration‑controlled artifacts and must be kept aligned with standards, SOPs, and security expectations.

Today, approvals and version changes happen in Git/GitHub (branches, pull requests, tags), but SRS quality checks still depend on manual reviews, risking missed gaps and inconsistent documentation.

---

## 3. Product Vision (this MVP slice)

Provide an **SRS‑aware AI companion** embedded in the Git/GitHub workflow that:

- Detects when SRS/risk file changes occur (e.g., PRs, merges, tags, state labels).
- Automatically analyzes the new or changed SRS/risk file against standards, SOPs, and security guidance.
- Produces **proposed findings and correction suggestions**, with citations, before or alongside human approval.

The copilot supports but does not replace human decision‑making, and it is intended to be acceptable for both EU MDR and FDA documentation workflows.

---

## 4. Scope (MVP)

### In scope

- SRS and risk file stored in GitHub (markdown or similar text), managed through branches/PRs/labels.
- Detection of relevant events:
  - New SRS/risk draft created.
  - SRS/risk file updated in a PR.
  - SRS marked as "approved" or "obsolete" (e.g., via label, branch, or tag).
- For each such event, automatic analysis of:
  - SRS completeness and clarity against standards and templates.
  - Risk file adequacy vs ISO 14971 / IEC 62304 expectations.
  - Security requirement coverage vs OWASP‑like checklists.
- Generation of **proposed findings** and **proposed corrections**, attached to the Git context (e.g., PR comment, check report):
  - Each finding references SRS/risk item IDs and relevant clauses/guidance.
  - Findings are labelled by stakeholder (Requirements owner, RA, QA, Risk, Cybersecurity, Clinical).
- Tracking of user decisions (accept/reject/defer) for each finding, in a way that can be tied back to Git history.

### Out of scope (for this MVP)

- Automated creation or full rewrite of SRS/risk files.
- Code/test/SBOM analysis.
- Automated risk acceptability decisions or regulatory approvals.
- Clinical decision support.

---

## 5. Target Users and Stakeholders

**Primary:**
- Software requirements owners / system engineers (own SRS).
- Risk Management / Safety engineers (own risk files).

**Secondary:**
- Regulatory Affairs, Quality Assurance, Cybersecurity/InfoSec, Clinical/Medical Affairs (consume findings and ensure process alignment).

---

## 6. Key Use Cases

### UC‑1 – SRS PR review assistant

When a PR modifies the SRS file, the copilot runs automatically and posts findings and suggested corrections as comments or a report in the PR.

### UC‑2 – Risk file PR review assistant (optional)

Similar, for changes to risk file(s).

### UC‑3 – Pre‑approval gate

Before tagging an SRS version as "approved," the copilot runs a full check and provides a summary of open findings.

### UC‑4 – Obsolescence sanity check

When marking SRS as obsolete, the copilot verifies that successor SRS or documentation exists to cover affected functions.

---

## 7. Functional Requirements (tech‑agnostic)

- The system shall ingest SRS and risk files from a Git/GitHub repository in a structured way (with requirement/risk IDs).
- The system shall detect configured Git/GitHub events on these files (e.g., PR opened/updated, tag created, label applied) and trigger analysis.
- The system shall ingest reference sources (standards/templates/SOPs/security checklists) with clause IDs.
- For each triggered event, the system shall generate proposed findings and correction suggestions with:
  - References to specific SRS/risk IDs and line ranges.
  - Citations to reference clauses.
  - Stakeholder labels and severity/priority (at least coarse).
- The system shall publish findings into the Git context (e.g., PR review comments or a status check report).
- The system shall record user decisions (accept/reject/defer) associated with specific findings and Git commits/PRs.

---

## 8. Non‑Functional Constraints

- Outputs must be explainable and traceable for audits (link Git history ↔ SRS/risk versions ↔ findings ↔ references).
- The tool must clearly present itself as decision‑support only, with no autonomous approvals.

---

## 9. Success Criteria

- ≥90% of findings contain valid, resolvable citations.
- ≥80% of accepted findings rated "useful" or "very useful" in test runs.
- Demonstrated reduction in manual SRS/risk review effort in Git‑based workflows (measured in PR review time/iterations).
