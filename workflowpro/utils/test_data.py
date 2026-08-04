from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class ProjectData:
    name: str
    description: str
    team_members: list[str]


def unique_project(prefix: str = "QA Auto") -> ProjectData:
    """Create collision-resistant data so parallel workers do not share state."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    suffix = uuid4().hex[:8]
    return ProjectData(
        name=f"{prefix} {stamp}-{suffix}",
        description="Created by the WorkFlow Pro QA automation case study.",
        team_members=[],
    )
