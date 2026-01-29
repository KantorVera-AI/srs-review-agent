# SRS Review Copilot - Repository Structure

Complete folder structure with all planned files and README placeholders.

## Repository Layout

```
srs-review-copilot/
├── docs/                    # Product & project documentation
│   ├── PRD.SRS-monitoring.md ✓
│   ├── vision-onepager.md ✓
│   ├── dataset-spec.md
│   ├── evaluation-plan.md
│   ├── stakeholder-workflow.md
│   └── workflow-git.md
├── data/                    # Sample data & reference standards
│   ├── srs/srs.md
│   ├── risk/risk.md
│   └── reference/
├── src/                     # Source code
│   ├── analysis/
│   └── integration/github/
├── experiments/             # Prototypes
└── .github/workflows/       # CI/CD
```

## To Create Remaining Structure

Use these commands locally:
```bash
mkdir -p data/srs data/risk data/reference
mkdir -p src/analysis src/integration/github
mkdir -p experiments .github/workflows
touch data/srs/README.md data/risk/README.md
touch data/reference/README.md
touch src/analysis/README.md
touch src/integration/github/README.md
touch experiments/README.md
```
