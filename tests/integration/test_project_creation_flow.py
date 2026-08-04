from __future__ import annotations

import pytest
from playwright.sync_api import Browser

from workflowpro.api.project_client import ProjectApiClient
from workflowpro.pages.login_page import LoginPage
from workflowpro.pages.projects_page import ProjectsPage


@pytest.mark.integration
@pytest.mark.live
@pytest.mark.security
@pytest.mark.browserstack
def test_project_creation_flow(browser: Browser, live_settings, project_data):
    """API -> desktop UI -> mobile-responsive UI -> tenant isolation.

    BrowserStack execution runs this same test across the configured desktop and
    real mobile-browser platform matrix. Locally, an additional mobile context
    provides fast responsive-layout feedback; it is not presented as a substitute
    for a real device.
    """
    company1_api = ProjectApiClient(
        live_settings.api_base_url,
        live_settings.company1_token,
        live_settings.company1_id,
        live_settings.api_timeout_seconds,
    )
    company2_api = ProjectApiClient(
        live_settings.api_base_url,
        live_settings.company2_token,
        live_settings.company2_id,
        live_settings.api_timeout_seconds,
    )

    project = None
    contexts = []
    try:
        # 1) API: create isolated, unique test data.
        project = company1_api.create_project(project_data)

        # 2) Desktop web: authenticate as Company1 and wait for the project.
        desktop_context = browser.new_context(viewport={"width": 1440, "height": 900})
        contexts.append(desktop_context)
        desktop_page = desktop_context.new_page()
        login = LoginPage(desktop_page, live_settings.ui_timeout_ms)
        login.open(live_settings.company1_web_url)
        login.login(live_settings.company1_admin)
        projects = ProjectsPage(desktop_page, live_settings.ui_timeout_ms)
        projects.open(live_settings.company1_web_url)
        projects.expect_project_visible(project.name)

        # 3) Mobile web: fast local responsive check. BrowserStack's configured
        # Android device supplies the real-device browser validation in cloud runs.
        mobile_context = browser.new_context(
            viewport={"width": 390, "height": 844},
            is_mobile=True,
            has_touch=True,
        )
        contexts.append(mobile_context)
        mobile_page = mobile_context.new_page()
        mobile_login = LoginPage(mobile_page, live_settings.ui_timeout_ms)
        mobile_login.open(live_settings.company1_web_url)
        mobile_login.login(live_settings.company1_admin)
        mobile_projects = ProjectsPage(mobile_page, live_settings.ui_timeout_ms)
        mobile_projects.open(live_settings.company1_web_url)
        mobile_projects.expect_project_visible(project.name)

        # 4a) Security boundary at API layer: a foreign tenant must never fetch it.
        foreign_response = company2_api.get_project_response(project.id)
        assert foreign_response.status_code in {403, 404}, (
            "Tenant isolation failure: Company2 could access a Company1 project; "
            f"status={foreign_response.status_code}"
        )

        # 4b) Defense in depth: the project must also be absent from Company2 UI.
        company2_context = browser.new_context(viewport={"width": 1280, "height": 800})
        contexts.append(company2_context)
        company2_page = company2_context.new_page()
        company2_login = LoginPage(company2_page, live_settings.ui_timeout_ms)
        company2_login.open(live_settings.company2_web_url)
        company2_login.login(live_settings.company2_user)
        company2_projects = ProjectsPage(company2_page, live_settings.ui_timeout_ms)
        company2_projects.open(live_settings.company2_web_url)
        company2_projects.expect_project_absent(project.name)
    finally:
        for context in reversed(contexts):
            context.close()
        if project is not None:
            # Cleanup belongs in finally so failures do not pollute later runs.
            company1_api.delete_project(project.id)
