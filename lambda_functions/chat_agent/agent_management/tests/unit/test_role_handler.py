"""Unit tests for role handler."""
import pytest
from unittest.mock import AsyncMock
from domain.command.role_command import CreateRole, UpdateRole, DeleteRole, GetRole
from domain.command_handlers.role_handler import RoleHandler


@pytest.fixture
def mock_repository():
    """Create mock repository."""
    return AsyncMock()


@pytest.fixture
def handler(mock_repository):
    """Create role handler with mock repository."""
    return RoleHandler(mock_repository)


@pytest.mark.asyncio
async def test_create_role(handler, mock_repository):
    """Test role creation."""
    command = CreateRole(role_name="Admin", description="Administrator role")
    mock_repository.create.return_value = 1

    result = await handler.create_role(command)

    assert result == 1
    mock_repository.create.assert_called_once_with(command)


@pytest.mark.asyncio
async def test_update_role(handler, mock_repository):
    """Test role update."""
    command = UpdateRole(role_id=1, role_name="Admin",
                         description="Updated description")
    mock_repository.update.return_value = True

    result = await handler.update_role(command)

    assert result is True
    mock_repository.update.assert_called_once_with(command)


@pytest.mark.asyncio
async def test_delete_role(handler, mock_repository):
    """Test role deletion."""
    command = DeleteRole(role_id=1)
    mock_repository.delete.return_value = True

    result = await handler.delete_role(command)

    assert result is True
    mock_repository.delete.assert_called_once_with(command.role_id)
