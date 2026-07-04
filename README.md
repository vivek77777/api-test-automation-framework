# API Test Automation Framework

[![Python API Tests](https://github.com/vivek77777/api-test-automation-framework/actions/workflows/api-tests.yml/badge.svg)](https://github.com/vivek77777/api-test-automation-framework/actions/workflows/api-tests.yml)

A Python-based REST API test automation framework using FastAPI, pytest, reusable API clients, fixtures, schema validation, negative testing, HTML reports, JUnit reports, and GitHub Actions CI/CD.

This project demonstrates how to design a maintainable API testing framework that validates REST endpoints, status codes, response schemas, authentication, error handling, and data-driven test scenarios.

---

## Tech Stack

- Python
- FastAPI
- pytest
- httpx / FastAPI TestClient
- jsonschema
- pytest-html
- pytest-xdist
- GitHub Actions

---

## API Features

The sample REST API includes:

- Health check endpoint
- Tenant creation
- Tenant retrieval
- Duplicate tenant validation
- Maintenance ticket creation
- Maintenance ticket retrieval
- Maintenance ticket status update
- Authentication validation
- Error handling for invalid and missing data

---

## Test Coverage

The test suite covers:

### Health

- Health endpoint returns OK

### Tenants

- Create tenant successfully
- Get tenant by ID
- Validate tenant response schema
- Unauthorized tenant creation returns 401
- Duplicate tenant email returns 409
- Missing required email returns 422
- Invalid email returns 422
- Unknown tenant returns 404

### Maintenance Tickets

- Create maintenance ticket successfully
- Get maintenance ticket by ID
- Validate ticket response schema
- Update ticket status successfully
- Create ticket for unknown tenant returns 404
- Unknown ticket returns 404
- Invalid ticket status returns 400
- Unauthorized ticket creation returns 401

---

## Framework Architecture

```text
api-test-automation-framework
│
├── .github
│   └── workflows
│       └── api-tests.yml
│
├── app
│   ├── __init__.py
│   └── main.py
│
├── tests
│   ├── api
│   │   ├── test_health.py
│   │   ├── test_tenants.py
│   │   └── test_tickets.py
│   │
│   ├── clients
│   │   ├── base_client.py
│   │   ├── tenants_client.py
│   │   └── tickets_client.py
│   │
│   ├── data
│   │   └── payloads.py
│   │
│   ├── schemas
│   │   ├── tenant_schema.json
│   │   └── ticket_schema.json
│   │
│   └── conftest.py
│
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Design Decisions

### Reusable API Clients

The framework uses reusable client classes to keep endpoint calls separate from test logic.

Examples:

- `TenantsClient`
- `TicketsClient`
- `BaseClient`

This makes tests cleaner and avoids repeating request logic.

---

### Pytest Fixtures

The framework uses pytest fixtures for:

- Creating the FastAPI test client
- Creating reusable API clients
- Clearing test data before each test
- Creating prerequisite tenant data for ticket tests

This keeps tests independent and safe for repeated execution.

---

### Data-Driven Test Payloads

Test payloads are stored separately in:

```text
tests/data/payloads.py
```

This keeps request data separate from test assertions and makes the framework easier to maintain.

---

### Schema Validation

JSON schema files are stored in:

```text
tests/schemas
```

The tests validate API responses against expected schemas using `jsonschema`.

---

### Negative Testing

The framework includes negative and error-handling tests for:

- Missing authorization
- Duplicate records
- Missing required fields
- Invalid email format
- Unknown resource IDs
- Invalid ticket status

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vivek77777/api-test-automation-framework.git
cd api-test-automation-framework
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the API Locally

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/health
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

---

## Running Tests

### Run full API test suite

```bash
pytest
```

### Run smoke tests

```bash
pytest -m smoke
```

### Run regression tests

```bash
pytest -m regression
```

### Run negative tests

```bash
pytest -m negative
```

---

## Reporting

The framework generates:

- HTML report
- JUnit XML report

Reports are created under:

```text
reports/
```

The HTML report can be opened from:

```text
reports/api-test-report.html
```

---

## CI/CD

The project includes a GitHub Actions workflow:

```text
.github/workflows/api-tests.yml
```

The workflow runs on:

- Push to `main`
- Pull request to `main`

The CI pipeline:

1. Checks out the repository
2. Sets up Python
3. Installs dependencies
4. Runs the full pytest suite
5. Uploads API test reports as artifacts

---

## Skills Demonstrated

This project demonstrates:

- REST API test automation
- Python pytest framework design
- Reusable API client design
- Pytest fixture usage
- Data-driven test payloads
- JSON schema validation
- Status code validation
- Error response validation
- Negative testing
- HTML and JUnit reporting
- GitHub Actions CI/CD integration

---

## Future Improvements

Potential future enhancements:

- Add authentication token fixture
- Add API contract testing
- Add performance tests with k6 or Locust
- Add Docker support
- Add test coverage reporting
- Add more schema validations
- Add API test metrics dashboard

---

## Author

Vivek Korukonda    
GitHub: [vivek77777](https://github.com/vivek77777)