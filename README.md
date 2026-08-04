# WorkFlow Pro — QA Automation Case Study

A submission-ready reference implementation for the **QA Automation Engineering Intern** case study. It demonstrates flaky-test stabilization, pytest/Playwright framework design, API testing, cross-tenant security validation, responsive/mobile-browser coverage, BrowserStack integration concepts, and CI/CD strategy.

> The assessment application and credentials are treated as external test-environment inputs. No real passwords, API tokens, or BrowserStack credentials are committed.

## What is included

- Reliable rewrite of the flaky login test
- Reliable multi-tenant UI test
- API client with conservative retry behavior
- API project creation + cleanup test
- Full API → desktop UI → mobile UI → tenant isolation integration flow
- Page Object layer
- Unique parallel-safe test data factory
- Environment-based configuration
- BrowserStack Playwright matrix example
- GitHub Actions workflows
- Test plan, framework design and complete case-study reasoning
- Offline tests that run without any WorkFlow Pro account

## Repository layout

```text
workflowpro/
  api/                 API service clients
  pages/               Playwright Page Objects
  utils/               test-data utilities
  config.py            environment settings
tests/
  unit/                no external dependencies
  ui/                  browser tests
  api/                 API tests
  integration/         API + UI + security flow
config/                 non-secret environment metadata
test_data/              non-secret test datasets
docs/                   case-study response and design docs
.github/workflows/      CI pipelines
browserstack.yml        BrowserStack Automate example
```

## Prerequisites

- Python 3.11+
- Git
- Chromium/Firefox/WebKit installed through Playwright for local browser runs

## Setup — Windows CMD

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install
copy .env.example .env
```

## Setup — macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install
cp .env.example .env
```

## Run the recruiter-safe offline checks

```bash
pytest tests/unit -v
```

Generate an HTML report:

```bash
pytest tests/unit -v --html=reports/unit-report.html --self-contained-html
```

## Run live WorkFlow Pro tests

Populate `.env` with **dedicated QA credentials/tokens**, then set:

```text
RUN_LIVE_E2E=true
```

Examples:

```bash
pytest tests/api -v
pytest tests/ui -v --browser chromium
pytest tests/integration -v --browser chromium
```

Cross-browser locally:

```bash
pytest tests/ui -v --browser chromium --browser firefox --browser webkit
```

## BrowserStack

BrowserStack's current Pytest/Playwright SDK can wrap an existing pytest suite. Install its SDK package, provide `BROWSERSTACK_USERNAME` and `BROWSERSTACK_ACCESS_KEY` as environment/CI secrets, review `browserstack.yml`, then run a targeted suite with the SDK wrapper.

Example concept:

```bash
pip install -r requirements-browserstack.txt
browserstack-sdk pytest tests/integration/test_project_creation_flow.py -v
```

The checked-in matrix is intentionally small to show cost control. A real team should derive supported devices from customer/browser analytics and contracts.

### Mobile distinction

- **Mobile web:** the same Playwright test logic can run against real mobile browsers in BrowserStack Automate. The integration test also creates a local mobile-sized/touch context for fast feedback.
- **Native/hybrid Android/iOS:** use Appium + BrowserStack App Automate (or a platform-native framework). Playwright alone is not presented as native-app automation.

## CI/CD

- `.github/workflows/qa.yml`: offline tests on pushes/PRs; no secrets required.
- `.github/workflows/live-e2e.yml`: explicit/manual live run using repository secrets.
- Broader BrowserStack matrices should normally run nightly/release rather than on every commit to manage cost and feedback time.

## Why there are no hard sleeps

The supplied flaky tests assume navigation and dynamic content are ready immediately. This implementation waits on observable state using Playwright locators and retrying assertions. Increasing `sleep()` only makes flaky tests slower.

## Why POST is not automatically retried

Read-only GET/HEAD requests can tolerate a bounded retry for transient infrastructure failures. Automatically replaying project creation can create duplicates unless the product provides an idempotency key/contract, so POST failures remain visible.

## Tenant isolation

A UI-only check is insufficient. The integration test creates a Company1 project, then intentionally attempts to retrieve its ID with Company2 credentials. A `200` would represent a serious authorization defect even if the Company2 frontend hides the project.

## Full written response

Read **[`docs/CASE_STUDY_RESPONSE.md`](docs/CASE_STUDY_RESPONSE.md)** for all three assessment parts, assumptions, missing-requirement questions, architecture decisions and live-discussion rationale.
