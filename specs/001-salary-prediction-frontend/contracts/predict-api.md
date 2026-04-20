# API Contract: Salary Prediction Backend

**Service**: `zjgilliam-flask-prediction` (Azure) / `localhost:5002` (local)  
**Date**: 2026-04-20

---

## Endpoints

### POST /predict

Submit a set of encoded integer inputs to receive a predicted salary.

**Request**

```
POST /predict
Content-Type: application/json
```

Body:
```json
{
  "age":          <integer 0–10>,
  "gender":       <integer 0–4>,
  "country":      <integer 0–57>,
  "highest_deg":  <integer 0–6>,
  "coding_exp":   <integer 0–6>,
  "title":        <integer 0–13>,
  "company_size": <integer 0–4>
}
```

**Response — Success (HTTP 200)**

```json
{
  "predicted_salary": <float>
}
```

Example:
```json
{
  "predicted_salary": 85000.42
}
```

**Response — Missing fields (HTTP 400)**

```json
{
  "error": "Missing one or more required fields"
}
```

**Response — Server error (HTTP 500)**

```json
{
  "error": "<exception message>"
}
```

---

### GET /health

Health check endpoint. Returns HTTP 200 when the service is running.

**Response (HTTP 200)**
```json
{
  "status": "ok"
}
```

---

### GET /

Landing page. Returns HTML confirmation that the API is live (not used by the frontend).

---

## Frontend Usage Contract

The frontend (`/frontend/app.py`) calls `POST /predict` at the configured `api_url`.

```python
# In frontend/app.py
api_url = "http://localhost:5002/predict"  # local dev
# api_url = "https://zjgilliam-flask-prediction.azurewebsites.net/predict"  # Azure

response = requests.post(api_url, json=payload, timeout=10)
```

**Timeout**: 10 seconds (covers SC-001's 5-second user-visible requirement with margin).

**Error handling**:
- Non-200 response: extract `error` from JSON; display in Bootstrap alert
- `requests.exceptions.RequestException` (timeout, connection error): display generic connectivity error message

---

## Form POST Contract (Browser → Frontend)

The HTML form POSTs to the frontend's own `/predict` route:

```
POST /predict
Content-Type: application/x-www-form-urlencoded

age=3&gender=0&country=55&highest_deg=3&coding_exp=3&title=4&company_size=1
```

The frontend `app.py` reads these via `request.form`, constructs the JSON payload, and forwards to the backend API.
