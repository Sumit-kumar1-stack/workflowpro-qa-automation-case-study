from workflowpro.utils.test_data import unique_project


def test_project_names_are_unique():
    first = unique_project()
    second = unique_project()

    assert first.name != second.name
    assert first.description
    assert first.team_members == []
