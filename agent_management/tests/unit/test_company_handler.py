"""Unit tests for company handler."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from domain.command.company_command import CreateCompany, UpdateCompany
from domain.command_handlers.company_handler import CompanyHandler

@pytest.fixture
def mock_repository():
    """Create mock repository."""
    return AsyncMock()

@pytest.fixture
def handler(mock_repository):
    """Create company handler with mock repository."""
    return CompanyHandler(mock_repository)

@pytest.mark.asyncio
async def test_create_company(handler, mock_repository):
    """Test company creation."""
    command = CreateCompany(company_name="Test Company")
    mock_repository.create.return_value = 1
    
    result = await handler.create_company(command)
    
    assert result == 1
    mock_repository.create.assert_called_once_with(command)

@pytest.mark.asyncio
async def test_update_company(handler, mock_repository):
    """Test company update."""
    command = UpdateCompany(company_id=1, company_name="Updated Company")
    mock_repository.update.return_value = True
    
    result = await handler.update_company(command)
    
    assert result is True
    mock_repository.update.assert_called_once_with(command)