# Data Model: Salary Prediction Frontend

**Branch**: `001-salary-prediction-frontend` | **Date**: 2026-04-20

---

## Entities

### PredictionRequest

Sent from the frontend to the backend `/predict` endpoint.

| Field        | Type    | Values            | Required | Notes                                      |
|--------------|---------|-------------------|----------|--------------------------------------------|
| age          | integer | 0–10              | Yes      | Encodes age range buckets                  |
| gender       | integer | 0–4               | Yes      | Encodes gender identity                    |
| country      | integer | 0–57              | Yes      | Encodes country/region                     |
| highest_deg  | integer | 0–6               | Yes      | Encodes highest education degree           |
| coding_exp   | integer | 0–6               | Yes      | Encodes years of coding experience         |
| title        | integer | 0–13              | Yes      | Encodes current job title                  |
| company_size | integer | 0–4               | Yes      | Encodes employer size bucket               |

**Validation rules**:
- All 7 fields must be present; missing any field returns HTTP 400 from the API
- All values must be integers (API casts via `int()`)
- Range enforcement is implicit in the model; out-of-range values are not rejected but produce unreliable predictions
- HTML `required` attribute + empty default value enforces completeness at the browser level before the request is sent

---

### PredictionResponse

Returned by the backend `/predict` endpoint on success.

| Field             | Type    | Notes                                     |
|-------------------|---------|-------------------------------------------|
| predicted_salary  | float   | Predicted annual salary in USD            |

**On error** (HTTP 400 or 500):

| Field  | Type   | Notes                              |
|--------|--------|------------------------------------|
| error  | string | Human-readable error description   |

---

### DropdownOption

A single selectable item within a dropdown field on the form.

| Field    | Type    | Notes                                                           |
|----------|---------|-----------------------------------------------------------------|
| value    | integer | The integer encoding the model expects for this option          |
| label    | string  | Human-readable text displayed to the user                       |
| field    | string  | Which input this option belongs to (e.g., `age`, `title`)      |

**Default/empty option** (required per FR-002):
- `value`: `""` (empty string — HTML attribute omitted)
- `label`: `"-- Select an option --"`
- The `required` attribute on the `<select>` treats an empty value as unfilled

---

## State Transitions

The frontend page has a single lifecycle:

```
[Loaded — form empty]
        ↓  user fills dropdowns
[Form ready — all required]
        ↓  user clicks Submit
[Submitting — POST to /predict]
        ↓ success            ↓ error
[Result displayed]    [Error message displayed]
        ↓  (page reloads or user re-fills)
[Loaded — form empty]
```

No session state is stored. Each submission is independent.

---

## Field Value Maps (complete)

Sourced from `../../../notes.txt` (parent directory).

### age
```
0: 18-21 | 1: 22-24 | 2: 25-29 | 3: 30-34 | 4: 35-39
5: 40-44 | 6: 45-49 | 7: 50-54 | 8: 55-59 | 9: 60-69 | 10: 70+
```

### gender
```
0: Man | 1: Nonbinary | 2: Prefer not to say | 3: Prefer to self-describe | 4: Woman
```

### country (58 entries)
```
0: Algeria | 1: Argentina | 2: Australia | 3: Bangladesh | 4: Belgium
5: Brazil | 6: Cameroon | 7: Canada | 8: Chile | 9: China
10: Colombia | 11: Czech Republic | 12: Ecuador | 13: Egypt | 14: Ethiopia
15: France | 16: Germany | 17: Ghana | 18: Hong Kong (S.A.R.) | 19: I do not wish to disclose my location
20: India | 21: Indonesia | 22: Iran, Islamic Republic of... | 23: Ireland | 24: Israel
25: Italy | 26: Japan | 27: Kenya | 28: Malaysia | 29: Mexico
30: Morocco | 31: Nepal | 32: Netherlands | 33: Nigeria | 34: Other
35: Pakistan | 36: Peru | 37: Philippines | 38: Poland | 39: Portugal
40: Romania | 41: Russia | 42: Saudi Arabia | 43: Singapore | 44: South Africa
45: South Korea | 46: Spain | 47: Sri Lanka | 48: Taiwan | 49: Thailand
50: Tunisia | 51: Turkey | 52: Ukraine | 53: United Arab Emirates
54: United Kingdom of Great Britain and Northern Ireland
55: United States of America | 56: Viet Nam | 57: Zimbabwe
```

### highest_deg
```
0: Bachelor's degree | 1: Doctoral degree | 2: I prefer not to answer
3: Master's degree | 4: No formal education past high school
5: Professional doctorate | 6: Some college/university study without earning a bachelor's degree
```

### coding_exp
```
0: 1-3 years | 1: 10-20 years | 2: 20+ years | 3: 3-5 years
4: 5-10 years | 5: < 1 year | 6: I have never written code
```

### title
```
0: Data Administrator | 1: Data Analyst (Business, Marketing, Financial, Quantitative, etc)
2: Data Architect | 3: Data Engineer | 4: Data Scientist | 5: Developer Advocate
6: Engineer (non-software) | 7: Machine Learning/ MLops Engineer
8: Manager (Program, Project, Operations, Executive-level, etc) | 9: Other
10: Research Scientist | 11: Software Engineer | 12: Statistician | 13: Teacher / professor
```

### company_size
```
0: 0-49 employees | 1: 10,000 or more employees | 2: 1,000-9,999 employees
3: 250-999 employees | 4: 50-249 employees
```
