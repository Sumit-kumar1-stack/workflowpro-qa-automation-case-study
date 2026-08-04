from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from workflowpro.utils.test_data import ProjectData


@dataclass(frozen=True)
class Project:
    id: int | str
    name: str
    status: str


class ProjectApiClient:
    """Small API client with conservative retry semantics.

    GET/HEAD may be retried for transient failures. Mutating requests are not
    automatically retried because a repeated POST could create duplicate data
    unless the product exposes an idempotency contract.
    """

    def __init__(
        self,
        base_url: str,
        token: str,
        tenant_id: str,
        timeout_seconds: float = 15,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "X-Tenant-ID": tenant_id,
                "Accept": "application/json",
            }
        )
        retry = Retry(
            total=2,
            connect=2,
            read=2,
            backoff_factor=0.3,
            status_forcelist=(429, 502, 503, 504),
            allowed_methods=frozenset({"GET", "HEAD"}),
            respect_retry_after_header=True,
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.mount("http://", HTTPAdapter(max_retries=retry))

    def create_project(self, data: ProjectData) -> Project:
        response = self.session.post(
            f"{self.base_url}/projects",
            json={
                "name": data.name,
                "description": data.description,
                "team_members": data.team_members,
            },
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload: dict[str, Any] = response.json()
        assert payload.get("id") is not None, "Create response must contain id"
        assert payload.get("name") == data.name
        assert payload.get("status") == "active"
        return Project(
            id=payload["id"],
            name=payload["name"],
            status=payload["status"],
        )

    def get_project_response(self, project_id: int | str) -> requests.Response:
        return self.session.get(
            f"{self.base_url}/projects/{project_id}",
            timeout=self.timeout_seconds,
        )

    def list_projects(self) -> list[dict[str, Any]]:
        response = self.session.get(
            f"{self.base_url}/projects",
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        if isinstance(payload, list):
            return payload
        return payload.get("items", payload.get("projects", []))

    def delete_project(self, project_id: int | str) -> None:
        response = self.session.delete(
            f"{self.base_url}/projects/{project_id}",
            timeout=self.timeout_seconds,
        )
        if response.status_code not in {200, 202, 204, 404}:
            response.raise_for_status()
