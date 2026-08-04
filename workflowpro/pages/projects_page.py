from __future__ import annotations

from playwright.sync_api import Page, expect


class ProjectsPage:
    def __init__(self, page: Page, timeout_ms: int = 15_000) -> None:
        self.page = page
        self.timeout_ms = timeout_ms
        self.project_cards = page.locator(
            '[data-testid="project-card"], .project-card'
        )

    def open(self, tenant_web_url: str) -> None:
        self.page.goto(
            f"{tenant_web_url.rstrip('/')}/projects",
            wait_until="domcontentloaded",
        )
        self.page.locator("body").wait_for(state="visible", timeout=self.timeout_ms)

    def card_for(self, project_name: str):
        return self.project_cards.filter(has_text=project_name).first

    def expect_project_visible(self, project_name: str) -> None:
        expect(self.card_for(project_name)).to_be_visible(timeout=self.timeout_ms)

    def expect_project_absent(self, project_name: str) -> None:
        expect(self.card_for(project_name)).to_have_count(0, timeout=self.timeout_ms)
