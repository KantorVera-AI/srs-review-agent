# GitHub Workflow (PM + Architect)

## Kanban (1 Project)
Columns: Backlog → Ready → In progress → In review → Done
Max 2 WIP/person

## Labels
owner:pm | owner:ai-architect
type:doc | type:data | type:ml

## Commits (no branches needed yet)
Edit → Source Control → Commit → Sync

## Architect Python setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import langchain; print('langchain ok')"
```

## Agent triggers (future)

Agent triggers are defined in `docs/03-integration/operating-model.md`. The trigger model is technology-neutral — the specific implementation depends on the integration tier chosen for each source system. See `docs/03-integration/system-categories.md` for the trigger capability of each system category.
