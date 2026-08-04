import os

from workflowpro.config import Settings


def test_settings_have_safe_defaults(monkeypatch):
    monkeypatch.delenv("RUN_LIVE_E2E", raising=False)
    monkeypatch.delenv("WORKFLOWPRO_COMPANY1_TOKEN", raising=False)
    settings = Settings.from_env()

    assert settings.api_base_url.endswith("/api/v1")
    assert settings.run_live_e2e is False
    assert "WORKFLOWPRO_COMPANY1_TOKEN" in settings.missing_live_values()


def test_live_flag_accepts_true(monkeypatch):
    monkeypatch.setenv("RUN_LIVE_E2E", "true")
    assert Settings.from_env().run_live_e2e is True
