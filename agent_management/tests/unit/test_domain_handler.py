"""Unit tests for domain handler."""
import pytest
from unittest.mock import AsyncMock
from domain.command.domain_command import CreateDomain, UpdateDomain, DeleteDomain, GetDomain
from domain.command_handlers.domain_handler import DomainHandler


@pytest.fixture
def mock_repository():
    """Create mock repository."""
    return AsyncMock()


@pytest.fixture
def handler(mock_repository):
    """Create domain handler with mock repository."""
    return DomainHandler(mock_repository)


@pytest.mark.asyncio
async def test_create_domain(handler, mock_repository):
    """Test domain creation."""
    command = CreateDomain(domain_name="Test Domain")
    mock_repository.create.return_value = 1

    result = await handler.create_domain(command)

    assert result == 1
    mock_repository.create.assert_called_once_with(command)


@pytest.mark.asyncio
async def test_update_domain(handler, mock_repository):
    """Test domain update."""
    command = UpdateDomain(domain_id=1, domain_name="Updated Domain")
    mock_repository.update.return_value = True

    result = await handler.update_domain(command)

    assert result is True
    mock_repository.update.assert_called_once_with(command)


@pytest.mark.asyncio
async def test_delete_domain(handler, mock_repository):
    """Test domain deletion."""
    command = DeleteDomain(domain_id=1)
    mock_repository.delete.return_value = True

    result = await handler.delete_domain(command)

    assert result is True
    mock_repository.delete.assert_called_once_with(command.domain_id)
