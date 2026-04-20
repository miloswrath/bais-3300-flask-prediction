# Tasks: Salary Prediction Frontend

**Input**: Design documents from `specs/001-salary-prediction-frontend/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓, quickstart.md ✓

**Tests**: Not requested — no test tasks included.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to
- No [Story] label = Setup, Foundational, or Polish phase

---

## Phase 1: Setup (Repository Reorganization)

**Purpose**: Reorganize the flat-root repo into `backend/` and `frontend/` directories per plan.md.

- [x] T001 Create `backend/` directory and move all existing root-level files into it: `app.py` → `backend/app.py`, `wsgi.py` → `backend/wsgi.py`, `web.config` → `backend/web.config`, `requirements.txt` → `backend/requirements.txt`, `salary_predict_model.pkl` → `backend/salary_predict_model.pkl`
- [x] T002 Create `frontend/` directory and `frontend/templates/` subdirectory

**Checkpoint**: All existing API files live in `backend/`. Root is clean of Python source files.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Frontend service scaffolding that MUST be complete before any user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T003 Create `frontend/requirements.txt` with contents: `Flask==3.1.0`, `flask-cors==5.0.1`, `gunicorn`, `requests`
- [x] T004 [P] Create `frontend/wsgi.py`: import the Flask app (`from app import app`) and add `if __name__ == "__main__": app.run()` — mirrors `backend/wsgi.py` structure
- [x] T005 [P] Create `frontend/web.config` as Azure IIS config: copy the structure of `backend/web.config` (wfastcgi FastCGI handler, WSGI_HANDLER=`app.app`, PYTHONPATH pointing to wwwroot)
- [x] T006 Create `frontend/templates/base.html`: HTML5 document with Bootstrap 5.3 CDN `<link>` in `<head>`, Bootstrap JS bundle `<script>` before `</body>`, a `{% block title %}` in `<title>`, and a `{% block content %}{% endblock %}` in `<body>` for page-level content injection

**Checkpoint**: Frontend directory is scaffolded. `frontend/templates/base.html` renders a blank Bootstrap page.

---

## Phase 3: User Story 1 — Submit Form and See Prediction (Priority: P1) 🎯 MVP

**Goal**: User selects values in all 7 dropdowns, submits the form, and sees a predicted salary.

**Independent Test**: Start both services locally (`backend/` on port 5002, `frontend/` on port 5001). Open `http://localhost:5001`, select a value in each dropdown, click Submit, verify a dollar-formatted salary appears on the page.

- [x] T007 [US1] Create `frontend/templates/index.html` extending `base.html`: a `<form action="/predict" method="POST">` containing 7 `<select>` elements named exactly `age`, `gender`, `country`, `highest_deg`, `coding_exp`, `title`, `company_size`; populate each select with `<option>` tags whose `value` attributes are the integers from `data-model.md` and whose text is the corresponding label; include a result display block (e.g., `{% if predicted_salary %}<p>Predicted Salary: {{ predicted_salary }}</p>{% endif %}`); include an error display block (`{% if error %}<div class="alert alert-danger">{{ error }}</div>{% endif %}`)
- [x] T008 [US1] Create `frontend/app.py`: Flask app with `api_url = "http://localhost:5002/predict"` (single configurable variable); `GET /` route renders `index.html`; `POST /predict` route reads all 7 form fields via `request.form`, constructs a JSON dict, calls `requests.post(api_url, json=payload, timeout=10)`, extracts `predicted_salary` from the response (formatted as `f"${value:,.0f}"`), and re-renders `index.html` passing either `predicted_salary=` or `error=` based on the API response status

**Checkpoint**: User Story 1 is fully functional. End-to-end salary prediction works locally. Predicted salary in the form matches the value returned by a direct Thunder Client POST to `http://localhost:5002/predict` with identical inputs.

---

## Phase 4: User Story 2 — Required Field Validation (Priority: P2)

**Goal**: Submitting the form with any dropdown left unselected is blocked by the browser with a visible required-field indicator.

**Independent Test**: Load `http://localhost:5001`, click Submit without selecting any options — verify the browser prevents submission and shows required-field indicators on all empty dropdowns.

- [x] T009 [US2] In `frontend/templates/index.html`, add `required` attribute to each of the 7 `<select>` elements; add an empty first `<option value="">-- Select an option --</option>` as the default selected option in each dropdown so the browser treats an unselected dropdown as unfilled

**Checkpoint**: User Story 2 is complete. The browser blocks form submission and shows validation indicators when any dropdown is left at its empty default. Only filled-dropdown errors are shown for partially-complete forms.

---

## Phase 5: User Story 3 — Responsive Layout (Priority: P3)

**Goal**: The form layout adapts correctly from desktop (1440px) to mobile (375px) without horizontal scrolling or hidden elements.

**Independent Test**: Open `http://localhost:5001` and resize the browser from full desktop width down to 375px mobile width — all dropdowns and the submit button remain visible, accessible, and properly reflowed at every width.

- [x] T010 [US3] In `frontend/templates/index.html`, wrap the form in Bootstrap grid classes (`container`, `row`, `justify-content-center`, `col-md-8 col-lg-6`); apply `form-label` to all `<label>` elements, `form-select mb-3` to all `<select>` elements, and `btn btn-primary btn-lg w-100 mt-2` to the submit `<button>`; wrap the result and error display in a `mt-4` div
- [x] T011 [US3] Verify responsive layout using Chrome MCP: navigate to `http://localhost:5001`, resize browser window across breakpoints (375px, 768px, 1024px, 1440px), confirm form reflows correctly and no horizontal scrollbar appears at any width

**Checkpoint**: User Story 3 is complete. The form is styled with Bootstrap 5.3 and is fully usable at all tested viewport widths.

---

## Phase 6: User Story 4 — Application Available on Azure (Priority: P4)

**Goal**: Both frontend and backend are deployed to Azure and the end-to-end prediction flow works via public Azure URLs.

**Independent Test**: Visit `https://zjgilliam-flask-frontend.azurewebsites.net`, fill all dropdowns, submit — verify the predicted salary appears and matches a direct Thunder Client POST to `https://zjgilliam-flask-prediction.azurewebsites.net/predict` with the same inputs.

- [x] T012 [P] [US4] Create `.github/workflows/deploy-backend.yml`: trigger on push to `main` with `paths: ['backend/**']` and on `workflow_dispatch`; job steps: checkout, set up Python 3.12, create venv + install `backend/requirements.txt`, validate `backend/app.py` import (`python -c "from app import app; print(app.url_map)"`), upload `backend/` (excluding antenv/) as artifact named `python-app-backend`, deploy artifact to Azure Web App `zjgilliam-flask-prediction` using secret `AZUREAPPSERVICE_PUBLISHPROFILE_6241F5B1D7FB4D65BF7497FFE5BD7903`
- [x] T013 [P] [US4] Create `.github/workflows/deploy-frontend.yml`: trigger on push to `main` with `paths: ['frontend/**']` and on `workflow_dispatch`; job steps: checkout, set up Python 3.12, create venv + install `frontend/requirements.txt`, validate `frontend/app.py` import, upload `frontend/` (excluding antenv/) as artifact named `python-app-frontend`, deploy to Azure Web App `zjgilliam-flask-frontend` using secret `AZUREAPPSERVICE_PUBLISHPROFILE_FRONTEND` (placeholder — real secret name comes from Azure portal download)
- [x] T014 [US4] Delete `.github/workflows/main_zjgilliam-flask-prediction.yml` (superseded by `deploy-backend.yml`)
- [x] T015 [US4] Update `api_url` in `frontend/app.py` from `http://localhost:5002/predict` to `https://zjgilliam-flask-prediction.azurewebsites.net/predict` before pushing the final frontend deployment commit — Azure URL documented as comment in `frontend/app.py`; uncomment line before deploying

**Checkpoint**: User Story 4 is complete. Both GitHub Actions workflows pass. Both Azure Web Apps are live and functional. Form submission on Azure returns the same prediction as a direct API call with identical inputs.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Verification and cleanup spanning multiple user stories.

- [x] T016 [P] Manually verify all 7 dropdown integer-to-label mappings in `frontend/templates/index.html` against `../../../notes.txt`: confirm `coding_exp` options use notes.txt's `code_experience mapping`, `title` options use `current_title mapping`, and all integer values are correct
- [x] T017 [P] Run full local end-to-end smoke test per `quickstart.md`: start `backend/` on port 5002 and `frontend/` on port 5001, submit the form, confirm prediction matches a direct API POST via Thunder Client (SC-002), confirm required-field validation blocks empty submission (SC-003)
- [x] T018 Run Chrome MCP full integration test: record a GIF of the complete user flow (load form → fill dropdowns → submit → view predicted salary → resize to mobile width) to verify SC-001 (under 5 seconds), SC-004 (responsive at 375px–1440px)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — **BLOCKS** all user stories
- **US1 (Phase 3)**: Depends on Phase 2 — no dependencies on US2/US3/US4
- **US2 (Phase 4)**: Depends on Phase 3 (edits the same index.html created in T007)
- **US3 (Phase 5)**: Depends on Phase 3 (edits the same index.html and base.html) — can start after Phase 3
- **US4 (Phase 6)**: Depends on Phase 3 (frontend/app.py must exist); T015 should be last before Azure push
- **Polish (Phase 7)**: Depends on Phases 3–6 complete

### User Story Dependencies

- **US1 (P1)**: Depends on Foundational only — no other story dependencies
- **US2 (P2)**: Depends on US1 (adds to T007's index.html)
- **US3 (P3)**: Depends on US1 (adds to T007's index.html and T006's base.html)
- **US4 (P4)**: Depends on US1 (frontend/app.py must exist); T012/T013 can be created in parallel with US2/US3

### Within Each Phase

- Models/templates before services/routes
- Route logic before end-to-end verification
- Local testing before Azure deployment

### Parallel Opportunities

- T004 and T005 can run in parallel (different files)
- T012 and T013 can run in parallel (different workflow files)
- T016 and T017 and T018 can run in parallel (independent verification tasks)
- US2 and US3 can be worked in parallel if both start from the US1 checkpoint (same file — coordinate edits)
- US4 workflow files (T012, T013) can be created while US2/US3 are in progress

---

## Parallel Example: Foundational Phase

```bash
# T004 and T005 can run simultaneously:
Task: "Create frontend/wsgi.py"
Task: "Create frontend/web.config"
# Then T006 (base.html) after both complete
```

## Parallel Example: US4 Workflows

```bash
# T012 and T013 can run simultaneously:
Task: "Create .github/workflows/deploy-backend.yml"
Task: "Create .github/workflows/deploy-frontend.yml"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (repo reorganization)
2. Complete Phase 2: Foundational (frontend scaffold)
3. Complete Phase 3: US1 (working prediction form)
4. **STOP and VALIDATE**: Fill all dropdowns locally, verify salary prediction appears and matches direct API call
5. MVP is complete and demonstrable

### Incremental Delivery

1. Setup + Foundational → scaffold ready
2. US1 (Phase 3) → prediction works end-to-end (**MVP**)
3. US2 (Phase 4) → form validation enforced
4. US3 (Phase 5) → Bootstrap responsive styling complete
5. US4 (Phase 6) → Azure deployment live
6. Polish (Phase 7) → verified and validated

---

## Notes

- [P] tasks = different files, no conflicting dependencies
- [Story] label maps each task to its user story for traceability
- The `required` attribute + empty `value=""` default option is the complete validation implementation for US2 — no JavaScript required
- The `api_url` variable in `frontend/app.py` is the single switch between local and Azure targets
- Field names in the HTML form (`name` attributes) MUST exactly match the API field names: `age`, `gender`, `country`, `highest_deg`, `coding_exp`, `title`, `company_size` — not the notes.txt key names
- Commit after each phase checkpoint for clean rollback points
