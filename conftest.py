from __future__ import annotations

import pytest

from workflowpro.config import Settings
from workflowpro.utils.test_data import ProjectData, unique_project


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings.from_env()


@pytest.fixture(scope="session")
def live_settings(settings: Settings) -> Settings:
    if not settings.run_live_e2e:
        pytest.skip("Set RUN_LIVE_E2E=true to execute tests against WorkFlow Pro.")
    missing = settings.missing_live_values()
    if missing:
        pytest.skip("Missing live-test secrets: " + ", ".join(missing))
    return settings


@pytest.fixture
def project_data() -> ProjectData:
    return unique_project()
