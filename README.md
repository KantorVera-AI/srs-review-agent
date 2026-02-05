# SRS & Risk Review Agent (MVP)

AI decision‑support agent for reviewing Software Requirements Specifications (SRS) and risk files against standards (IEC 62304, MDR, ISO 14971).

## Problem
SaMD teams manually map SRS/risk docs to standards → error‑prone, audit risks.

## MVP Scope
- Ingest SRS + risk file + IEC 62304 templates
- Detect gaps/misalignments with citations
- Propose findings for RA/QA/Risk/Cybersecurity (non‑binding)
- Log decisions for audit trail

**Out**: SRS generation, risk classification, clinical decisions.

## Structure
docs/          → PRD, specs, risk model
data/          → synthetic SRS v1/v2, risk files, templates
src/           → RAG pipeline, finding generation
experiments/   → eval results

## Get started
1. Open Codespace
2. `cd data/raw && ls` → see SRS examples
3. `python src/analysis/ingest.py` → index corpus

See [PRD](docs/prd-srs-risk-agent.md)
