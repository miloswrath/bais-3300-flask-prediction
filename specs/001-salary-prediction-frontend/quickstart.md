# Quickstart: Salary Prediction Frontend

**Branch**: `001-salary-prediction-frontend` | **Date**: 2026-04-20

---

## Local Development

### Prerequisites

- Python 3.12 installed
- Two terminal windows

### Step 1 — Start the backend

```bash
cd backend/
python -m venv antenv
source antenv/bin/activate   # Windows: antenv\Scripts\activate
pip install -r requirements.txt
python app.py
# Backend runs on http://localhost:5002
```

### Step 2 — Start the frontend

In a second terminal:

```bash
cd frontend/
python -m venv antenv
source antenv/bin/activate
pip install -r requirements.txt
python app.py
# Frontend runs on http://localhost:5001
```

### Step 3 — Test locally

1. Open `http://localhost:5001` in a browser
2. Select a value in each of the 7 dropdowns
3. Click **Submit**
4. Verify a predicted salary appears

**Validation tests:**
- Click Submit with no dropdowns selected → browser should block with required-field indicators
- Try submitting with only some dropdowns filled → only empty fields show errors
- Use Thunder Client (or curl) to POST directly to `http://localhost:5002/predict` with the same values → confirm identical salary returned

**Responsiveness test:**
- Resize browser window from full desktop → tablet → mobile width → form should reflow without horizontal scroll

---

## Switching API URL

The frontend's `api_url` variable in `frontend/app.py` controls which backend is called:

```python
# Local dev (default)
api_url = "http://localhost:5002/predict"

# Azure (change before deploying the frontend)
api_url = "https://zjgilliam-flask-prediction.azurewebsites.net/predict"
```

---

## Azure Deployment

### Prerequisites

- Azure account with existing App Service Plan
- `zjgilliam-flask-prediction` Web App already exists (backend)
- A new Web App `zjgilliam-flask-frontend` created on the same App Service Plan (Python 3.12, Linux)
- Two publish profile secrets in the GitHub repo:
  - `AZUREAPPSERVICE_PUBLISHPROFILE_<BACKEND_ID>` — already exists in the current workflow
  - `AZUREAPPSERVICE_PUBLISHPROFILE_<FRONTEND_ID>` — download from Azure portal for the new frontend app

### Deploy backend

1. Ensure `backend/` contains `app.py`, `wsgi.py`, `web.config`, `requirements.txt`, `salary_predict_model.pkl`
2. Push to `main` branch — `deploy-backend.yml` triggers on `paths: ['backend/**']`
3. Monitor the Actions tab; verify the build passes the `Validate app import` step

### Deploy frontend

1. Update `api_url` in `frontend/app.py` to the Azure backend URL
2. Ensure `frontend/` contains `app.py`, `wsgi.py`, `web.config`, `requirements.txt`, and `templates/`
3. Push to `main` branch — `deploy-frontend.yml` triggers on `paths: ['frontend/**']`
4. Monitor the Actions tab

### Post-deployment verification

1. Visit `https://zjgilliam-flask-frontend.azurewebsites.net` — form should load
2. Fill all dropdowns and submit — salary prediction should appear
3. Use Thunder Client: POST to `https://zjgilliam-flask-prediction.azurewebsites.net/predict` with the same inputs → verify identical salary value (SC-002)

---

## Directory Structure Reference

```
repo root/
├── backend/
│   ├── app.py                   # Flask API (/predict, /health)
│   ├── wsgi.py
│   ├── web.config
│   ├── requirements.txt
│   └── salary_predict_model.pkl
├── frontend/
│   ├── app.py                   # Flask web app (renders form, proxies to backend)
│   ├── wsgi.py
│   ├── web.config
│   ├── requirements.txt
│   └── templates/
│       ├── base.html            # Bootstrap 5.3 layout
│       └── index.html           # Form + result display
└── .github/workflows/
    ├── deploy-backend.yml
    └── deploy-frontend.yml
```
