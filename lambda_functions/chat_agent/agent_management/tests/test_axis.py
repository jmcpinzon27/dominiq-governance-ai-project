"""Tests for axis operations."""
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from domain.command.axis_command import CreateAxis, UpdateAxis, AxisResponse
from adapters.postgres.models.axis import Axis
from adapters.postgres.repositories.axis_repository import AxisRepository


@pytest.mark.asyncio
async def test_create_axis(app: FastAPI, client: AsyncClient, test_session):
    """Test creating a new axis."""
    # Arrange
    axis_data = {
        "axis_name": "Test Axis"
    }
    
    # Act
    response = await client.post("/axes/", json=axis_data)
    
    # Assert
    assert response.status_code == 201
    axis_id = response.json()
    assert isinstance(axis_id, int)
    
    # Verify in database
    repository = AxisRepository(test_session)
    axis = await repository.get_by_id(axis_id)
    assert axis is not None
    assert axis.axis_name == axis_data["axis_name"]


@pytest.mark.asyncio
async def test_get_axis(app: FastAPI, client: AsyncClient, test_session):
    """Test getting an axis by ID."""
    # Arrange
    repository = AxisRepository(test_session)
    axis = Axis(
        axis_name="Test Axis"
    )
    test_session.add(axis)
    await test_session.commit()
    await test_session.refresh(axis)
    
    # Act
    response = await client.get(f"/axes/{axis.axis_id}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["axis_id"] == axis.axis_id
    assert data["axis_name"] == axis.axis_name


@pytest.mark.asyncio
async def test_update_axis(app: FastAPI, client: AsyncClient, test_session):
    """Test updating an axis."""
    # Arrange
    repository = AxisRepository(test_session)
    axis = Axis(
        axis_name="Test Axis"
    )
    test_session.add(axis)
    await test_session.commit()
    await test_session.refresh(axis)
    
    update_data = {
        "axis_name": "Updated Axis"
    }
    
    # Act
    response = await client.put(f"/axes/{axis.axis_id}", json=update_data)
    
    # Assert
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify in database
    updated_axis = await repository.get_by_id(axis.axis_id)
    assert updated_axis.axis_name == update_data["axis_name"]


@pytest.mark.asyncio
async def test_delete_axis(app: FastAPI, client: AsyncClient, test_session):
    """Test deleting an axis."""
    # Arrange
    repository = AxisRepository(test_session)
    axis = Axis(
        axis_name="Test Axis"
    )
    test_session.add(axis)
    await test_session.commit()
    await test_session.refresh(axis)
    
    # Act
    response = await client.delete(f"/axes/{axis.axis_id}")
    
    # Assert
    assert response.status_code == 200
    assert response.json() is True
    
    # Verify in database
    deleted_axis = await repository.get_by_id(axis.axis_id)
    assert deleted_axis is None


@pytest.mark.asyncio
async def test_list_axes(app: FastAPI, client: AsyncClient, test_session):
    """Test listing all axes."""
    # Arrange
    repository = AxisRepository(test_session)
    axes = [
        Axis(axis_name="Axis 1"),
        Axis(axis_name="Axis 2"),
        Axis(axis_name="Axis 3")
    ]
    for axis in axes:
        test_session.add(axis)
    await test_session.commit()
    
    # Act
    response = await client.get("/axes/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "axes" in data
    assert len(data["axes"]) == len(axes)
    
    # Verify axis data
    axis_names = [a["axis_name"] for a in data["axes"]]
    assert "Axis 1" in axis_names
    assert "Axis 2" in axis_names
    assert "Axis 3" in axis_names
