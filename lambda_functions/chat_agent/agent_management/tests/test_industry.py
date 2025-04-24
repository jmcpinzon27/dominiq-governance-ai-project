"""Tests for industry operations."""
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from domain.command.industry_command import CreateIndustry, UpdateIndustry, IndustryResponse
from adapters.postgres.models.industry import Industry
from adapters.postgres.repositories.industry_repository import IndustryRepository


@pytest.mark.asyncio
async def test_create_industry(app: FastAPI, client: AsyncClient, test_session):
    """Test creating a new industry."""
    # Arrange
    repository = IndustryRepository(test_session)
    industry_data = {
        "industry_name": "Test Industry"
    }
    
    # Act
    response = await client.post("/industries/", json=industry_data)
    
    # Assert
    assert response.status_code == 201
    industry_id = response.json()
    assert isinstance(industry_id, int)
    
    # Verify in database
    industry = await repository.get_by_id(industry_id)
    assert industry is not None
    assert industry.industry_name == industry_data["industry_name"]


@pytest.mark.asyncio
async def test_get_industry(app: FastAPI, client: AsyncClient, test_session):
    """Test getting an industry by ID."""
    # Arrange
    repository = IndustryRepository(test_session)
    industry = Industry(
        industry_name="Test Industry"
    )
    test_session.add(industry)
    await test_session.commit()
    await test_session.refresh(industry)
    
    # Act
    response = await client.get(f"/industries/{industry.industry_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["industry_id"] == industry.industry_id
    assert data["industry_name"] == industry.industry_name


@pytest.mark.asyncio
async def test_update_industry(app: FastAPI, client: AsyncClient, test_session):
    """Test updating an industry."""
    # Arrange
    repository = IndustryRepository(test_session)
    industry = Industry(
        industry_name="Test Industry"
    )
    test_session.add(industry)
    await test_session.commit()
    await test_session.refresh(industry)
    
    update_data = {
        "industry_name": "Updated Industry"
    }
    
    # Act
    response = await client.put(f"/industries/{industry.industry_id}", json=update_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify in database
    updated_industry = await repository.get_by_id(industry.industry_id)
    assert updated_industry.industry_name == update_data["industry_name"]


@pytest.mark.asyncio
async def test_delete_industry(app: FastAPI, client: AsyncClient, test_session):
    """Test deleting an industry."""
    # Arrange
    repository = IndustryRepository(test_session)
    industry = Industry(
        industry_name="Test Industry"
    )
    test_session.add(industry)
    await test_session.commit()
    await test_session.refresh(industry)
    
    # Act
    response = await client.delete(f"/industries/{industry.industry_id}")
    
    # Assert
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify in database
    deleted_industry = await repository.get_by_id(industry.industry_id)
    assert deleted_industry is None


@pytest.mark.asyncio
async def test_list_industries(app: FastAPI, client: AsyncClient, test_session):
    """Test listing all industries."""
    # Arrange
    repository = IndustryRepository(test_session)
    industries = [
        Industry(industry_name="Industry 1"),
        Industry(industry_name="Industry 2"),
        Industry(industry_name="Industry 3")
    ]
    for industry in industries:
        test_session.add(industry)
    await test_session.commit()
    
    # Act
    response = await client.get("/industries/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "industries" in data
    assert len(data["industries"]) == len(industries)
    
    # Verify industry data
    industry_names = [i["industry_name"] for i in data["industries"]]
    assert "Industry 1" in industry_names
    assert "Industry 2" in industry_names
    assert "Industry 3" in industry_names
