from __future__ import annotations

from playwright.sync_api import Page, expect

from workflowpro.config import Credentials


class LoginPage:
    def __init__(self, page: Page, timeout_ms: int = 15_000) -> None:
        self.page = page
        self.timeout_ms = timeout_ms
        self.email = page.locator('[data-testid="login-email"], #email').first
        self.password = page.locator('[data-testid="login-password"], #password').first
        self.submit = page.locator('[data-testid="login-submit"], #login-btn').first
        self.two_factor = page.locator(
            '[data-testid="two-factor-code"], #two-factor-code'
        ).first
        self.two_factor_submit = page.locator(
            '[data-testid="two-factor-submit"], #two-factor-submit'
        ).first
        self.post_login_or_2fa = page.locator(
            '.welcome-message, [data-testid="dashboard-root"], '
            '[data-testid="two-factor-code"], #two-factor-code'
        ).first

    def open(self, tenant_web_url: str) -> None:
        self.page.goto(
            f"{tenant_web_url.rstrip('/')}/login",
            wait_until="domcontentloaded",
        )
        expect(self.email).to_be_visible(timeout=self.timeout_ms)

    def login(self, credentials: Credentials) -> None:
        self.email.fill(credentials.email)
        self.password.fill(credentials.password)
        self.submit.click()

        # Wait for an application state, not an arbitrary sleep.
        self.post_login_or_2fa.wait_for(state="visible", timeout=self.timeout_ms)

        if self.two_factor.is_visible():
            if not credentials.totp:
                raise RuntimeError(
                    "This test user requires 2FA. Provide a dedicated test TOTP "
                    "or use an approved test-account 2FA bypass."
                )
            self.two_factor.fill(credentials.totp)
            self.two_factor_submit.click()

        self.page.wait_for_url("**/dashboard*", timeout=self.timeout_ms)
        expect(
            self.page.locator(
                '.welcome-message, [data-testid="dashboard-root"]'
            ).first
        ).to_be_visible(timeout=self.timeout_ms)
