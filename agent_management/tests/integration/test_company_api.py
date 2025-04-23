"""Integration tests for company API."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from main import app
from adapters.postgres.models import Base
from adapters.postgres.config import get_session

@pytest.fixture
async def test_db():
    """Create test database."""
    # Setup test database
    engine = create_test_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(test_db):
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_company(client):
    """Test company creation endpoint."""
    response = await client.post(
        "/companies/",
        json={"company_name": "Test Company"}
    )
    
    assert response.status_code == 200
    assert isinstance(response.json(), int)

@pytest.mark.asyncio
async def test_get_company(client):
    """Test get company endpoint."""
    # First create a company
    create_response = await client.post(
        "/companies/",
        json={"company_name": "Test Company"}
    )
    company_id = create_response.json()
    
    # Then get it
    response = await client.get(f"/companies/{company_id}")
    
    assert response.status_code == 200
    assert response.json()["company_name"] == "Test Company"