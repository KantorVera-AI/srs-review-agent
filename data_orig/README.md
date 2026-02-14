# Data Policy & Structure

## Rules (no exceptions)
- ❌ NO PHI/PII, client SRS, hospital data, confidential docs
- ✅ ONLY synthetic SRS/risk files + public IEC 62304/MDR templates

## Folder roles
- `raw/` → original .md files (SRS v1/v2, risk v1)
- `processed/` → indexed JSON/chunks (regenerate from raw/)
- `reference/` → IEC 62304 checklists, MDR mappings

Regenerate: `python src/analysis/ingest.py`
