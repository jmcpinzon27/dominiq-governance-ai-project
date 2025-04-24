"""Unit tests for project handler."""
import pytest
from unittest.mock import AsyncMock
from domain.command.project_command import CreateProject, UpdateProject, DeleteProject, GetProject
from domain.command_handlers.project_handler import ProjectHandler


@pytest.fixture
def mock_repository():
    """Create mock repository."""
    return AsyncMock()


@pytest.fixture
def handler(mock_repository):
    """Create project handler with mock repository."""
    return ProjectHandler(mock_repository)


@pytest.mark.asyncio
async def test_create_project(handler, mock_repository):
    """Test project creation."""
    command = CreateProject(
        project_name="Test Project",
        company_id=1,
        description="Test Description"
    )
    mock_repository.create.return_value = 1

    result = await handler.create_project(command)

    assert result == 1
    mock_repository.create.assert_called_once_with(command)


@pytest.mark.asyncio
async def test_update_project(handler, mock_repository):
    """Test project update."""
    command = UpdateProject(
        project_id=1,
        project_name="Updated Project",
        company_id=1,
        description="Updated Description"
    )
    mock_repository.update.return_value = True

    result = await handler.update_project(command)

    assert result is True
    mock_repository.update.assert_called_once_with(command)


@pytest.mark.asyncio
async def test_delete_project(handler, mock_repository):
    """Test project deletion."""
    command = DeleteProject(project_id=1)
    mock_repository.delete.return_value = True

    result = await handler.delete_project(command)

    assert result is True
    mock_repository.delete.assert_called_once_with(command.project_id)
