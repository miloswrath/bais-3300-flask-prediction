# Research: Salary Prediction Frontend

**Branch**: `001-salary-prediction-frontend` | **Date**: 2026-04-20

---

## Decision 1: Frontend-to-Backend Communication

**Decision**: Frontend Flask app calls the backend Azure API directly from the server side (Python `requests` library), then renders the result into the Jinja2 template response.

**Rationale**: The form action cannot POST directly to the Azure backend API because (a) the API returns JSON, not HTML — the browser would display raw JSON rather than rendering the result nicely, and (b) mixing form POSTs with the Azure API URL would expose CORS issues. A server-side proxy approach: frontend receives the form POST at its own `/predict` route, forwards fields to the backend API using `requests.post()`, extracts `predicted_salary` from the JSON response, and renders it in `index.html`.

**Alternatives considered**:
- **Client-side AJAX (JavaScript fetch)**: Would work but adds JavaScript complexity not required by the assignment. Assignment says "set form action to /predict and method to POST" — server-side proxy matches this literally.
- **Direct form POST to API URL**: Does not work because the API returns JSON; the browser would show raw JSON.

---

## Decision 2: Monorepo Structure — Two Azure Web Apps

**Decision**: Keep frontend and backend in the same GitHub repo under `backend/` and `frontend/` subdirectories. Deploy to two separate Azure Web Apps (`zjgilliam-flask-prediction` for backend, `zjgilliam-flask-frontend` for frontend) on the same App Service Plan.

**Rationale**: The assignment asks to "put your front end application on Azure" separately from the API server. Two Web Apps on the same App Service Plan share compute without extra cost. Separate GitHub Actions workflows with `paths:` filters (e.g., `paths: ['backend/**']`) ensure only the changed service triggers a deploy.

**Alternatives considered**:
- **Single Azure Web App serving both**: Would require a more complex routing setup (nginx, or a single app with static file serving). Unnecessarily complex for this scope and would couple the two services.
- **Two separate repos**: Splits the assignment deliverable across two repos; the assignment asks for a GitHub repo URL for each, but both can be the same monorepo.

---

## Decision 3: GitHub Actions — Two Workflows with Path Filters

**Decision**: Create two separate workflow files: `deploy-backend.yml` and `deploy-frontend.yml`. Each uses a `paths:` filter so only the relevant service builds and deploys when files in its directory change.

```yaml
# deploy-backend.yml trigger
on:
  push:
    branches: [main]
    paths: ['backend/**']
  workflow_dispatch:

# deploy-frontend.yml trigger
on:
  push:
    branches: [main]
    paths: ['frontend/**']
  workflow_dispatch:
```

Each workflow:
1. Sets up Python 3.12
2. Creates venv, installs deps from its own `requirements.txt`
3. Validates the app import (`python -c "from app import app; print(app.url_map)"`)
4. Uploads the subdirectory as artifact
5. Deploys to its respective Azure Web App using its publish profile secret

**Rationale**: Path-filtered workflows prevent unnecessary deploys. Each service has its own publish profile secret already issued by Azure portal.

**Alternatives considered**:
- **Single workflow with matrix**: More complex YAML; path filters work better with separate files for independent deployments.
- **Reusing the existing workflow**: The existing workflow deploys everything from root — it needs to be replaced/split since files are moving into subdirectories.

---

## Decision 4: Bootstrap 5.3 Integration

**Decision**: Load Bootstrap 5.3 via CDN in `base.html`. No local install or build step required.

```html
<!-- In base.html <head> -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- Before </body> -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

**Rationale**: CDN approach matches the assignment instructions ("use the Bootstrap documentation"). No build tooling required. The assignment is a school project — CDN is idiomatic for this context.

**Alternatives considered**:
- **pip install flask-bootstrap**: Outdated package, not maintained for Bootstrap 5. Rejected.
- **Local static files**: Unnecessary complexity; CDN is faster and simpler.

---

## Decision 5: Field Name Mapping (Form → API)

**Decision**: The HTML form `<select name="...">` attributes must match the field names expected by the backend API (`app.py`). The API uses: `age`, `gender`, `country`, `highest_deg`, `coding_exp`, `title`, `company_size`.

**Note**: The notes.txt label file uses slightly different key names (`code_experience`, `current_title`) for human readability. The form must use the API field names, not the notes.txt key names.

| Form Field Name | API Field Name | Notes.txt Key     |
|-----------------|----------------|-------------------|
| age             | age            | age mapping       |
| gender          | gender         | gender mapping    |
| country         | country        | country mapping   |
| highest_deg     | highest_deg    | highest_deg mapping |
| coding_exp      | coding_exp     | code_experience mapping |
| title           | title          | current_title mapping |
| company_size    | company_size   | company_size mapping |

**Dropdown values** (integer → label, sourced from `notes.txt`):

### age (0–10)
| Value | Label |
|-------|-------|
| 0 | 18-21 |
| 1 | 22-24 |
| 2 | 25-29 |
| 3 | 30-34 |
| 4 | 35-39 |
| 5 | 40-44 |
| 6 | 45-49 |
| 7 | 50-54 |
| 8 | 55-59 |
| 9 | 60-69 |
| 10 | 70+ |

### gender (0–4)
| Value | Label |
|-------|-------|
| 0 | Man |
| 1 | Nonbinary |
| 2 | Prefer not to say |
| 3 | Prefer to self-describe |
| 4 | Woman |

### country (0–57)
58 countries/regions — see notes.txt for full mapping. Key entries:
| Value | Label |
|-------|-------|
| 2 | Australia |
| 7 | Canada |
| 15 | France |
| 16 | Germany |
| 20 | India |
| 26 | Japan |
| 55 | United States of America |
| 54 | United Kingdom of Great Britain and Northern Ireland |
| ... | (all 58 entries from notes.txt) |

### highest_deg (0–6)
| Value | Label |
|-------|-------|
| 0 | Bachelor's degree |
| 1 | Doctoral degree |
| 2 | I prefer not to answer |
| 3 | Master's degree |
| 4 | No formal education past high school |
| 5 | Professional doctorate |
| 6 | Some college/university study without earning a bachelor's degree |

### coding_exp (0–6)
| Value | Label |
|-------|-------|
| 0 | 1-3 years |
| 1 | 10-20 years |
| 2 | 20+ years |
| 3 | 3-5 years |
| 4 | 5-10 years |
| 5 | < 1 year |
| 6 | I have never written code |

### title (0–13)
| Value | Label |
|-------|-------|
| 0 | Data Administrator |
| 1 | Data Analyst (Business, Marketing, Financial, Quantitative, etc) |
| 2 | Data Architect |
| 3 | Data Engineer |
| 4 | Data Scientist |
| 5 | Developer Advocate |
| 6 | Engineer (non-software) |
| 7 | Machine Learning/ MLops Engineer |
| 8 | Manager (Program, Project, Operations, Executive-level, etc) |
| 9 | Other |
| 10 | Research Scientist |
| 11 | Software Engineer |
| 12 | Statistician |
| 13 | Teacher / professor |

### company_size (0–4)
| Value | Label |
|-------|-------|
| 0 | 0-49 employees |
| 1 | 10,000 or more employees |
| 2 | 1,000-9,999 employees |
| 3 | 250-999 employees |
| 4 | 50-249 employees |

---

## Decision 6: Local Development Setup

**Decision**: Run both services simultaneously on different ports. Backend on port 5002 (existing default), frontend on port 5001. `api_url` in frontend `app.py` defaults to `http://localhost:5002/predict` for local dev, and is changed to the Azure backend URL before deployment.

**Rationale**: The spec explicitly requires `api_url` to be a single configurable variable for easy switching between local and Azure targets (per FR-009 and Assumptions).

**Alternatives considered**:
- **Environment variable for api_url**: More robust but adds complexity not required by the assignment. Can be done in a follow-up if needed.

---

## Decision 7: Error Display

**Decision**: When the backend API returns an error (non-200 status or exception), the frontend renders the same `index.html` with an error message displayed in a Bootstrap alert component instead of the predicted salary.

**Rationale**: Per FR-006 and SC per edge cases — the user should see a readable error, not a blank page or stack trace.
