# Feature Specification: Salary Prediction Frontend

**Feature Branch**: `001-salary-prediction-frontend`  
**Created**: 2026-04-20  
**Status**: Draft  
**Input**: User description: "Build a Flask frontend web application for salary prediction that collects user inputs via dropdowns, submits to a ML prediction API, and displays the result, styled with Bootstrap 5.3 and deployable to Azure"

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Submit Form and See Prediction (Priority: P1)

A user visits the salary prediction web page, selects values from seven dropdown menus (age, gender, country, education level, coding experience, job title, and company size), submits the form, and sees a predicted salary displayed on the screen.

**Why this priority**: This is the core value of the entire application — without it, there is nothing else to test or demonstrate. Every other story depends on this flow working correctly.

**Independent Test**: Open the form in a browser, select valid options in all dropdowns, submit, and verify a dollar value appears as the predicted salary.

**Acceptance Scenarios**:

1. **Given** the form is fully loaded with all dropdowns, **When** the user selects a value in each dropdown and clicks Submit, **Then** a predicted salary value is returned and displayed on the page.
2. **Given** the form is submitted with valid selections, **When** the backend API processes the request, **Then** the predicted salary matches the value returned by calling the API directly with the same inputs.
3. **Given** the user submits the form, **When** the API returns a result, **Then** the salary is shown in a readable, formatted way (e.g., currency format).

---

### User Story 2 - Required Field Validation (Priority: P2)

A user attempts to submit the form without filling in all dropdowns. The browser prevents submission and visually indicates which fields are missing.

**Why this priority**: The assignment explicitly requires all fields to be marked as required and to show indicators when not selected. This protects the API from receiving incomplete data.

**Independent Test**: Load the form and click Submit without making any selections — verify the browser shows validation errors on all empty dropdowns.

**Acceptance Scenarios**:

1. **Given** the form is loaded and no dropdowns have been selected, **When** the user clicks Submit, **Then** the browser blocks submission and highlights each empty dropdown with a required-field indicator.
2. **Given** only some dropdowns are filled, **When** the user submits, **Then** only the unfilled dropdowns show validation errors.
3. **Given** all dropdowns have the default "choose a value" placeholder selected (empty value), **When** the user submits, **Then** the form is treated as incomplete and submission is blocked.

---

### User Story 3 - Responsive Layout on Different Screen Sizes (Priority: P3)

A user accesses the salary prediction form on a mobile phone, tablet, or desktop browser. The layout adjusts gracefully to each screen size without breaking the form or hiding content.

**Why this priority**: The assignment requires Bootstrap 5.3 styling with responsiveness tested by resizing the browser window. A non-responsive form would fail the grading criteria.

**Independent Test**: Open the form and resize the browser from full desktop width down to a narrow mobile width — verify the layout reflows correctly without horizontal scrolling or obscured elements.

**Acceptance Scenarios**:

1. **Given** the form is displayed on a desktop browser, **When** the window is resized to a tablet width, **Then** the layout adjusts and all dropdowns and the submit button remain visible and usable.
2. **Given** the form is displayed at mobile width, **When** the user interacts with dropdowns, **Then** all inputs remain selectable and the form is fully functional.

---

### User Story 4 - Application Available on Azure (Priority: P4)

A user accesses the salary prediction frontend application through a public Azure URL. The form loads, submissions are processed by the API also running on Azure, and predicted salaries are returned correctly.

**Why this priority**: The final deliverable requires the frontend to be deployed and functional on Azure, connected to the Azure-hosted API. This is the production acceptance test.

**Independent Test**: Visit the Azure frontend URL in a browser, fill out the form, and verify a salary prediction is returned — matching the result from a direct API call with the same inputs.

**Acceptance Scenarios**:

1. **Given** the frontend is deployed to Azure, **When** the user visits the Azure overview URL, **Then** the salary prediction form loads completely.
2. **Given** the Azure frontend is loaded, **When** the user submits the form with valid selections, **Then** the Azure-hosted API processes the request and the predicted salary is displayed.
3. **Given** both frontend and backend are on Azure, **When** the same inputs are sent via the form and via a direct API tool (e.g., Thunder Client), **Then** both return identical predicted salary values.

---

### Edge Cases

- What happens when the API is unreachable or returns an error? The frontend should display a user-friendly error message rather than a blank page or raw error.
- What if a user manipulates a dropdown to send a non-numeric or out-of-range value? The API should reject the request gracefully with an informative error.
- What happens if the user's browser does not support HTML5 required-field validation? The form should still behave reasonably (this is an assumption: modern browsers are assumed).
- What if the Azure API URL is misconfigured in the frontend app? The form submission should fail clearly, not silently.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The web application MUST present a single-page form with dropdown inputs for: age range, gender, country, highest education degree, coding experience, job title, and company size.
- **FR-002**: Each dropdown MUST include an empty default option with instructional placeholder text (e.g., "-- Select an option --") and must have an empty value so the field is treated as unfilled.
- **FR-003**: Each dropdown MUST be marked as required, preventing form submission if any field is left at its default empty value.
- **FR-004**: The form MUST submit user selections to the prediction endpoint using the HTTP POST method.
- **FR-005**: The application MUST display the predicted salary returned by the API after a successful form submission.
- **FR-006**: The application MUST display a clear, user-readable error message if the API call fails or returns an error.
- **FR-007**: The frontend application MUST be structured with a shared base layout template and a separate index page template.
- **FR-008**: The application MUST be styled using Bootstrap 5.3 and must be visually responsive at desktop, tablet, and mobile widths.
- **FR-009**: The frontend MUST be deployable as a standalone web service on Azure, with the API URL configurable via a single variable in the application code.
- **FR-010**: The backend API code MUST be reorganized into a dedicated `/backend` directory, and the frontend code MUST live in a dedicated `/frontend` directory, with both correctly integrated.
- **FR-011**: The CI/CD pipeline MUST be updated so that both the frontend and backend pass automated build checks and deploy correctly to Azure.
- **FR-012**: The numeric values sent for each dropdown field MUST match the encoding expected by the prediction model (i.e., dropdown option values must be integers corresponding to the model's training labels).

### Key Entities

- **Prediction Request**: A set of seven encoded integer fields (age, gender, country, highest_deg, coding_exp, title, company_size) submitted to the API.
- **Prediction Response**: A single numeric salary value returned by the API after processing a prediction request.
- **Dropdown Option**: A human-readable label paired with a numeric integer value that the model understands; each of the seven inputs has its own option set.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can select values in all seven dropdowns and receive a predicted salary in under 5 seconds on a standard internet connection.
- **SC-002**: The predicted salary shown in the form exactly matches the salary returned by submitting the same inputs directly to the API (zero discrepancy).
- **SC-003**: Submitting the form with any dropdown left at its empty default value is blocked 100% of the time by the browser, with at least one visible field indicator shown.
- **SC-004**: The form layout is fully usable (no overlapping, hidden, or clipped elements) at viewport widths ranging from 375px (mobile) to 1440px (desktop).
- **SC-005**: The frontend application loads and accepts form submissions via the public Azure URL without manual intervention or reconfiguration after deployment.
- **SC-006**: Both frontend and backend services pass automated CI/CD pipeline checks and deploy successfully in a single workflow run.

---

## Assumptions

- The existing API (`/predict` endpoint) running on Azure accepts a JSON body with the seven integer-encoded fields and returns `{"predicted_salary": <number>}` — no changes to the API contract are required.
- Dropdown option integer values will be manually verified against the model's label encoding (referenced in the original notes/mapping used when building the API); the spec does not define those mappings.
- The frontend service will run on the same Azure App Service Plan as the backend, as a separate web app instance.
- Modern browsers (Chrome, Firefox, Edge, Safari — current versions) are assumed; no legacy browser support is required.
- The API URL for the frontend to call will be stored in a single configurable variable in the frontend application code (`api_url`), making it easy to switch between local and Azure targets.
- Local development testing will be done with both services running simultaneously on different ports.
- The frontend does not require user authentication — the form is publicly accessible.
- Deployment instructions will be provided as written documentation alongside the code.
