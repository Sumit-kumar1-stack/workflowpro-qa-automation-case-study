import pytest

from workflowpro.api.project_client import ProjectApiClient


@pytest.mark.api
@pytest.mark.live
def test_project_create_and_cleanup(live_settings, project_data):
    client = ProjectApiClient(
        live_settings.api_base_url,
        live_settings.company1_token,
        live_settings.company1_id,
        live_settings.api_timeout_seconds,
    )
    project = None
    try:
        project = client.create_project(project_data)
        response = client.get_project_response(project.id)
        response.raise_for_status()
        assert response.json()["name"] == project_data.name
    finally:
        if project is not None:
            client.delete_project(project.id)
