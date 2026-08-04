from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable

from dotenv import load_dotenv


@dataclass(frozen=True)
class Credentials:
    email: str
    password: str
    totp: str | None = None


@dataclass(frozen=True)
class Settings:
    api_base_url: str
    company1_web_url: str
    company2_web_url: str
    company1_id: str
    company2_id: str
    company1_admin: Credentials
    company2_user: Credentials
    company1_token: str
    company2_token: str
    ui_timeout_ms: int
    api_timeout_seconds: float
    run_live_e2e: bool

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        return cls(
            api_base_url=os.getenv(
                "WORKFLOWPRO_API_BASE_URL",
                "https://app.workflowpro.com/api/v1",
            ).rstrip("/"),
            company1_web_url=os.getenv(
                "WORKFLOWPRO_COMPANY1_WEB_URL",
                "https://company1.workflowpro.com",
            ).rstrip("/"),
            company2_web_url=os.getenv(
                "WORKFLOWPRO_COMPANY2_WEB_URL",
                "https://company2.workflowpro.com",
            ).rstrip("/"),
            company1_id=os.getenv("WORKFLOWPRO_COMPANY1_ID", "company1"),
            company2_id=os.getenv("WORKFLOWPRO_COMPANY2_ID", "company2"),
            company1_admin=Credentials(
                email=os.getenv(
                    "WORKFLOWPRO_COMPANY1_ADMIN_EMAIL",
                    "admin@company1.com",
                ),
                password=os.getenv("WORKFLOWPRO_COMPANY1_ADMIN_PASSWORD", ""),
                totp=os.getenv("WORKFLOWPRO_COMPANY1_ADMIN_TOTP") or None,
            ),
            company2_user=Credentials(
                email=os.getenv(
                    "WORKFLOWPRO_COMPANY2_USER_EMAIL",
                    "user@company2.com",
                ),
                password=os.getenv("WORKFLOWPRO_COMPANY2_USER_PASSWORD", ""),
                totp=os.getenv("WORKFLOWPRO_COMPANY2_USER_TOTP") or None,
            ),
            company1_token=os.getenv("WORKFLOWPRO_COMPANY1_TOKEN", ""),
            company2_token=os.getenv("WORKFLOWPRO_COMPANY2_TOKEN", ""),
            ui_timeout_ms=int(os.getenv("WORKFLOWPRO_UI_TIMEOUT_MS", "15000")),
            api_timeout_seconds=float(
                os.getenv("WORKFLOWPRO_API_TIMEOUT_SECONDS", "15")
            ),
            run_live_e2e=os.getenv("RUN_LIVE_E2E", "false").lower()
            in {"1", "true", "yes"},
        )

    def missing_live_values(self) -> list[str]:
        values: Iterable[tuple[str, str]] = (
            ("WORKFLOWPRO_COMPANY1_ADMIN_PASSWORD", self.company1_admin.password),
            ("WORKFLOWPRO_COMPANY2_USER_PASSWORD", self.company2_user.password),
            ("WORKFLOWPRO_COMPANY1_TOKEN", self.company1_token),
            ("WORKFLOWPRO_COMPANY2_TOKEN", self.company2_token),
        )
        return [name for name, value in values if not value]
