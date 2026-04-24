# Data Policy and Structure

**Owner:** AI Architect  
**Audience:** AI Architect, PM, any contributor adding files to this folder

---

## Non-negotiable rules

This repository is a public working document. Every file in `data/` must comply with the following rules without exception:

- No PHI or PII of any kind — no patient data, no clinical records, no personal identifiers
- No confidential client documents — no real SRS files, no real risk management files, no client-specific regulatory submissions
- No hospital or healthcare provider data of any kind
- No paid standards full text — IEC, ISO, and FDA guidance documents are copyrighted; only clause summaries, structure references, and publicly available mapping tables are permitted

Permitted content: synthetic documents created for testing, publicly available regulatory guidance references, self-authored clause summaries, and OWASP/open-source security references.

---

## Data classification

| Type | Description | Permitted in this repo | Examples |
|---|---|---|---|
| Synthetic | Documents created specifically for agent testing — no real product data | Yes — primary test corpus | `srs_v1.md`, `srs_v2.md`, `risk_v1.md` |
| Reference | Clause summaries, structure templates, publicly available mappings | Yes — reference corpus | `iec62304-mapping.md`, `iso14971-risk-table-example.md` |
| Production | Real product documents from an actual regulatory submission | No — never committed here | Any real client SRS, real risk file, real technical file |

If you are unsure whether a file is synthetic or production, do not commit it. Ask the AI Architect.

---

## Folder structure and naming conventions

### `raw/`

Original source documents used as the agent's test corpus. Organised by document type.

```
raw/
  srs/
    srs_v1.md          — baseline SRS (initial version for test scenarios)
    srs_v2.md          — updated SRS (post-change version for diff testing)
  risk/
    risk_v1.md         — risk management file aligned to srs_v1.md
```

Naming convention: `{document_type}_v{version}.md` — lowercase, underscores, version suffix required. Do not use dates in filenames; use version numbers. Add new versions by incrementing the suffix — do not overwrite existing versions.

### `processed/`

Machine-generated files produced by the ingest pipeline. Do not edit these files manually — they are regenerated from `raw/` on every ingest run.

```
processed/
  chunks/              — chunked and indexed fragments of raw documents
  embeddings/          — vector representations (gitignored if large)
```

The `processed/` folder is not authoritative. If a processed file looks wrong, fix the source in `raw/` and re-run the ingest pipeline. Committing manually edited processed files creates inconsistency between the raw and processed states.

### `reference/`

Reference corpus for regulatory standards and security frameworks. These files inform the agent's citation and cross-check logic.

```
reference/
  iec62304-mapping.md            — IEC 62304 clause structure and SRS requirements mapping
  iec62304-srs-requirements.md   — IEC 62304 section 5.2 software requirements analysis clauses
  iso14971-risk-table-example.md — ISO 14971 risk table structure and clause 7.3.3 reference
  owasp-asvs-summary.md          — OWASP ASVS v4.0 control categories for SaMD (UC5)
```

Naming convention: `{standard}-{descriptor}.md` — lowercase, hyphens. Add new reference files by standard acronym prefix to keep the folder scannable.

---

## Ingest pipeline

To regenerate `processed/` from `raw/`:

```
python src/analysis/ingest.py
```

The ingest script reads all `.md` files under `raw/`, chunks them, generates embeddings, and writes the output to `processed/`. Run this after any change to a raw document. The AI Architect is responsible for validating that the processed output matches expectations after each ingest run.

---

## What is validated before each release

Before the initial release: all files in `raw/` must match the test scenarios described in `docs/01-system/evaluation-plan.md`. The synthetic corpus must be sufficient to exercise all validation criteria listed in UC1 and UC3.

Before Release 2: reference corpus must include the threat model format confirmed by the AI Architect for UC5. See `docs/01-system/use-cases/uc5-cybersecurity.md` for the format requirements.

Before Release 3: `raw/` must include at least one realistic change control plan document for UC4 parser validation.
