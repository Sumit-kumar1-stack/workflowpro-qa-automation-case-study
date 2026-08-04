# Framework Design Notes

```text
Tests (business intent)
   |-- Page Objects --------> Playwright browser
   |-- API Clients ---------> REST services
   |-- Fixtures ------------> config + isolated test data
   |-- Assertions ----------> UI state + API/security state

CI
   |-- PR: unit + fast API/smoke
   |-- nightly: cross-browser + BrowserStack
   |-- release: critical real-device + tenant security
```

## Design choices
- pytest fixtures over deep base-test inheritance.
- Page Objects only for interaction mechanics; assertions stay close to tests.
- API for setup/cleanup to keep UI journeys short and deterministic.
- Environment-driven secrets and tenant metadata.
- Stable selectors should use roles/labels/test IDs; CSS IDs/classes are fallback only because the assessment supplies them.
- Retry reads conservatively; do not hide product defects behind blanket test retries.
- Markers allow cost-aware suites (`unit`, `api`, `ui`, `integration`, `browserstack`, `security`).
