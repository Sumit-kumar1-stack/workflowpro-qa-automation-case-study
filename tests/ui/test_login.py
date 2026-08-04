import pytest
from playwright.sync_api import Page, expect

from workflowpro.pages.dashboard_page import DashboardPage
from workflowpro.pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.live
def test_user_login_reliable(page: Page, live_settings):
    """Corrected version of the flaky login test from Part 1."""
    page.set_default_timeout(live_settings.ui_timeout_ms)
    login = LoginPage(page, live_settings.ui_timeout_ms)
    dashboard = DashboardPage(page, live_settings.ui_timeout_ms)

    login.open(live_settings.company1_web_url)
    login.login(live_settings.company1_admin)

    # Playwright assertions auto-wait; URL accepts redirects/query parameters.
    expect(page).to_have_url("**/dashboard*", timeout=live_settings.ui_timeout_ms)
    dashboard.expect_loaded()
