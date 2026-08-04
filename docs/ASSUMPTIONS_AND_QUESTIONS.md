# Assumptions and Open Questions

See `CASE_STUDY_RESPONSE.md` for the full rationale. Key unresolved items before productionizing:

1. Exact tenant-routing and authorization contract.
2. Exact role-permission matrix.
3. Supported browsers/devices and minimum versions.
4. Whether mobile means mobile web, native, hybrid, or all.
5. Deterministic QA 2FA mechanism.
6. API cleanup/reset capability and eventual-consistency window.
7. CI provider, expected runtime SLA and BrowserStack concurrency budget.
8. Reporting/test-management integration.
9. Performance SLAs, rate limits and test-environment load limits.
10. PII/data-retention constraints for automated test data.
