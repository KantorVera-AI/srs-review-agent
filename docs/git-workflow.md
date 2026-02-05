# GitHub Workflow (PM + Architect)

## Kanban (1 Project)
Columns: Backlog → Ready → In progress → In review → Done
Max 2 WIP/person

## Labels
owner:pm | owner:ai-architect
type:doc | type:data | type:ml | priority:high

## Commits (no branches needed yet)
Edit → Source Control → Commit → Sync

## Architect Python setup
1. Terminal: `pip install langchain faiss-cpu sentence-transformers`
2. Jupyter: Ctrl+Shift+P → "Jupyter: Create New Jupyter Notebook"

## Agent triggers (future)
PR opened → .github/workflows/agent.yml → analyze → PR comment
