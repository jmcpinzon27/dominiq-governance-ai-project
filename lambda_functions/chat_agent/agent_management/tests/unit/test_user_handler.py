"""Unit tests for user handler."""
import pytest
from unittest.mock import AsyncMock
from domain.command.user_command import CreateUser, UpdateUser, DeleteUser, GetUser
from domain.command_handlers.user_handler import UserHandler

@pytest.fixture
def mock_repository():
    """Create mock repository."""
    return AsyncMock()

@pytest.fixture
def handler(mock_repository):
    """Create user handler with mock repository."""
    return UserHandler(mock_repository)

@pytest.mark.asyncio
async def test_create_user(handler, mock_repository):
    """Test user creation."""
    command = CreateUser(
        user_name="John Doe",
        email="john@example.com",
        role_id=1,
        company_id=1
    )
    mock_repository.create.return_value = 1
    
    result = await handler.create_user(command)
    
    assert result == 1
    mock_repository.create.assert_called_once_with(command)

@pytest.mark.asyncio
async def test_update_user(handler, mock_repository):
    """Test user update."""
    command = UpdateUser(
        user_id=1,
        user_name="John Doe",
        email="john@example.com",
        role_id=1,
        company_id=1
    )
    mock_repository.update.return_value = True
    
    result = await handler.update_user(command)
    
    assert result is True
    mock_repository.update.assert_called_once_with(command)

@pytest.mark.asyncio
async def test_delete_user(handler, mock_repository):
    """Test user deletion."""
    command = DeleteUser(user_id=1)
    mock_repository.delete.return_value = True
    
    result = await handler.delete_user(command)
    
    assert result is True
    mock_repository.delete.assert_called_once_with(command.user_id)