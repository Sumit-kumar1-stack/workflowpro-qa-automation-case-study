from __future__ import annotations

from playwright.sync_api import Page, expect


class DashboardPage:
    def __init__(self, page: Page, timeout_ms: int = 15_000) -> None:
        self.page = page
        self.timeout_ms = timeout_ms
        self.welcome = page.locator(
            '.welcome-message, [data-testid="dashboard-root"]'
        ).first
        self.project_cards = page.locator(
            '[data-testid="project-card"], .project-card'
        )

    def expect_loaded(self) -> None:
        expect(self.welcome).to_be_visible(timeout=self.timeout_ms)

    def visible_project_texts(self) -> list[str]:
        # Dynamic data must have reached a stable visible state first.
        self.expect_loaded()
        if self.project_cards.count() == 0:
            return []
        expect(self.project_cards.first).to_be_visible(timeout=self.timeout_ms)
        return [text.strip() for text in self.project_cards.all_text_contents()]
