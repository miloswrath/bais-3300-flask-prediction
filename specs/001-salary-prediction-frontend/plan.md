# Implementation Plan: Salary Prediction Frontend

**Branch**: `001-salary-prediction-frontend` | **Date**: 2026-04-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-salary-prediction-frontend/spec.md`

## Summary

Build a Flask frontend web application with Jinja2 templates and Bootstrap 5.3 that collects seven encoded integer inputs via dropdowns and POSTs to the existing salary prediction API. Reorganize the current flat repo into `/backend` (existing Flask API) and `/frontend` (new web app) directories, update GitHub Actions to build and deploy both services independently to Azure App Service.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**:
- Backend: Flask 3.1.0, flask-cors 5.0.1, joblib 1.4.2, gunicorn 23.0.0, scikit-learn 1.6.1
- Frontend: Flask 3.1.0, gunicorn, requests (for proxying); Bootstrap 5.3 via CDN; Jinja2 (Flask built-in)  
**Storage**: N/A — stateless prediction; no database required  
**Testing**: Manual browser testing; Chrome MCP for local integration smoke test  
**Target Platform**: Azure App Service (Linux, Python 3.12), two separate Web App instances on the same App Service Plan  
**Project Type**: Web application — monorepo with separate frontend and backend Flask services  
**Performance Goals**: Predicted salary returned and displayed within 5 seconds of form submission (per SC-001)  
**Constraints**:
- Both apps on the same Azure App Service Plan (cost constraint)
- API URL must be a single configurable variable in frontend `app.py` (`api_url`)
- No user authentication required
- Modern browsers only (Chrome, Firefox, Edge, Safari — current versions)  
**Scale/Scope**: Single-user school project; no concurrency or load requirements beyond basic Azure App Service defaults

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

> **Status**: The project constitution (`/.specify/memory/constitution.md`) contains only the unfilled template — no actual principles have been ratified. No gates apply. Proceeding without violations.

Post-design recheck: No new violations introduced. Design follows minimal-complexity principle appropriate for a school project.

## Project Structure

### Documentation (this feature)

```text
specs/001-salary-prediction-frontend/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   └── predict-api.md
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── app.py                    # Moved from repo root (Flask API — /predict, /health, /)
├── wsgi.py                   # Moved from repo root
├── web.config                # Moved from repo root (IIS/Azure config)
├── requirements.txt          # Backend-specific dependencies
└── salary_predict_model.pkl  # ML model file

frontend/
├── app.py                    # New Flask web app (form, proxy to backend)
├── wsgi.py                   # New WSGI entry point
├── web.config                # Azure IIS config for frontend
├── requirements.txt          # Frontend-specific deps (Flask, gunicorn, requests)
└── templates/
    ├── base.html             # Bootstrap 5.3 layout (CDN links, nav, footer)
    └── index.html            # Salary prediction form (7 dropdowns + submit + result)

.github/
└── workflows/
    ├── deploy-backend.yml    # Build + deploy backend/ to zjgilliam-flask-prediction
    └── deploy-frontend.yml   # Build + deploy frontend/ to zjgilliam-flask-frontend
```

**Structure Decision**: Option 2 (frontend + backend split). The existing flat structure (all files at repo root) will be reorganized: existing files move to `backend/`, new files go to `frontend/`. Two separate GitHub Actions workflows with `paths:` filters ensure only the changed service redeploys on push.

## Complexity Tracking

> No constitution violations to justify.
