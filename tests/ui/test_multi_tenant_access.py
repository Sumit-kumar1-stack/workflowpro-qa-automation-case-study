import pytest
from playwright.sync_api import Page

from workflowpro.pages.dashboard_page import DashboardPage
from workflowpro.pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.live
@pytest.mark.security
def test_multi_tenant_access(page: Page, live_settings):
    """Part 1 reliability rewrite of the original Company2 test.

    The original assessment checks the tenant name in every card. In a real
    product, project names may not contain 'Company2'; stronger tests compare
    IDs/data against the tenant API. This UI test retains the supplied business
    assumption while the integration suite verifies the actual security boundary.
    """
    page.set_default_timeout(live_settings.ui_timeout_ms)
    login = LoginPage(page, live_settings.ui_timeout_ms)
    dashboard = DashboardPage(page, live_settings.ui_timeout_ms)

    login.open(live_settings.company2_web_url)
    login.login(live_settings.company2_user)

    for project_text in dashboard.visible_project_texts():
        assert "Company2" in project_text
