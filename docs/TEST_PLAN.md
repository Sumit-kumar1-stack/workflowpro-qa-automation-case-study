# Test Plan

## Objective
Validate authentication reliability, project lifecycle behavior, cross-platform presentation, role/tenant authorization boundaries, and API/UI consistency for a multi-tenant B2B SaaS platform.

## Scope
- Login, including deterministic test 2FA path
- Project creation/read/display/cleanup
- Company1 vs Company2 tenant isolation
- Desktop cross-browser smoke
- Mobile web responsiveness and selected real-device coverage
- API functional and authorization checks

## Out of scope without additional requirements
- Production load generation
- Native app automation when no APK/IPA/app contract is supplied
- Real customer 2FA inbox/SMS automation
- Destructive production testing

## Test levels
1. Unit/framework: configuration and test-data helpers.
2. API: fast service behavior and authorization.
3. UI: critical browser behavior.
4. Integration: API-created state observed through UI and challenged cross-tenant.
5. Cross-platform: BrowserStack selected matrix.

## Entry criteria
- Stable QA environment
- Dedicated test tenants/users
- Secrets available in CI secret store
- Test cleanup mechanism
- Known supported browser/device matrix

## Exit criteria
- Critical smoke passes
- No open tenant-isolation defects
- Agreed pass rate across supported browser/device matrix
- Failed tests have artifacts sufficient for diagnosis

## Risk priorities
P0: cross-tenant data leakage, authentication bypass.
P1: cannot login/create/view projects.
P2: role permission errors, browser-specific critical defects.
P3: cosmetic responsive differences.
